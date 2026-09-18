# -*- coding: utf-8 -*-
"""Include inside Renode Monitor after platform creation. Loopback TCP only."""
from __future__ import print_function
import os
import sys
import json
import socket
import threading
import time
from System import UInt32, UInt64

_bridge_dir = os.path.dirname(os.path.abspath(__file__))
if _bridge_dir not in sys.path:
    sys.path.insert(0, _bridge_dir)
from protocol import SWITCH_PINS, DisplayLatch, motor_state, validate_input


class VirtualLabBridge(object):
    def __init__(self, machine, port):
        self.machine = machine
        self.bus = machine.SystemBus
        self.lock = threading.RLock()
        self.done = threading.Event()
        self.latch = DisplayLatch()
        self.pushed = set()
        self.last_request = time.time()
        self.error = None
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind(('127.0.0.1', port))
        self.listener.listen(1)
        self.listener.settimeout(0.3)

    def read(self, address):
        return int(self.bus.ReadDoubleWord(UInt64(address)))

    def write(self, address, value):
        self.bus.WriteDoubleWord(UInt64(address), UInt32(value))

    def release_pushes(self):
        with self.lock:
            for signal in list(self.pushed):
                self.machine['sysbus.gpioB'].OnGPIO(SWITCH_PINS[signal], False)
            self.pushed.clear()

    def sample_loop(self):
        while not self.done.is_set():
            try:
                with self.lock:
                    now = time.time()
                    self.latch.sample(self.read(0x40020814), now)
                    if now - self.last_request > 1.0:
                        self.release_pushes()
                    self.error = None
            except Exception:
                self.error = 'Renode I/O unavailable; restart the GUI session after resetting the machine'
            self.done.wait(0.002)

    def snapshot(self):
        if self.error:
            raise ValueError(self.error)
        gpio_c = self.read(0x40020814)
        inputs = self.read(0x40020410)
        self.latch.sample(gpio_c, time.time())
        return {'leds': (self.read(0x40020014) >> 4) & 255,
                'adc': self.read(0x4001204c) & 4095,
                'switches': dict((name, bool(inputs & (1 << pin)))
                                 for name, pin in SWITCH_PINS.items()),
                'digits': self.latch.digits(time.time()),
                'motor': motor_state(gpio_c), 'gpio_c': gpio_c}

    def request(self, data):
        with self.lock:
            self.last_request = time.time()
            if data == {'op': 'state'}:
                return self.snapshot()
            if not isinstance(data, dict) or set(data) != set(['op', 'signal', 'value']) or data['op'] != 'input':
                raise ValueError('Only state and input operations are supported')
            signal, value = validate_input({'signal': data['signal'], 'value': data['value']})
            if signal == 'AnalogInput0':
                self.write(0x4001204c, value)
                self.write(0x40012000, 2)
            else:
                self.machine['sysbus.gpioB'].OnGPIO(SWITCH_PINS[signal], value)
                if signal.startswith('PSW'):
                    if value:
                        self.pushed.add(signal)
                    else:
                        self.pushed.discard(signal)
            return self.snapshot()

    def serve(self):
        while not self.done.is_set():
            try:
                conn, _ = self.listener.accept()
            except socket.timeout:
                continue
            except socket.error:
                break
            try:
                conn.settimeout(0.3)
                pending = b''
                while not self.done.is_set():
                    try:
                        block = conn.recv(2048)
                    except socket.timeout:
                        if time.time() - self.last_request > 3.0:
                            break
                        continue
                    if not block:
                        break
                    pending += block
                    if len(pending) > 4096:
                        break
                    while b'\n' in pending:
                        line, pending = pending.split(b'\n', 1)
                        try:
                            state = self.request(json.loads(line.decode('utf-8')))
                            reply = {'ok': True, 'state': state}
                        except (ValueError, TypeError, KeyError):
                            reply = {'ok': False, 'error': 'Invalid request or unavailable I/O'}
                        conn.sendall((json.dumps(reply) + '\n').encode('utf-8'))
            except Exception:
                pass
            finally:
                conn.close()
                self.release_pushes()

    def start(self):
        for target in (self.sample_loop, self.serve):
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()

    def stop(self):
        self.done.set()
        self.listener.close()
        self.release_pushes()


if 'vlab_bridge' in globals():
    vlab_bridge.stop()
_port = int(os.environ.get('VLAB_BRIDGE_PORT', '4567'))
if not 1024 <= _port <= 65535:
    raise ValueError('VLAB_BRIDGE_PORT must be in 1024..65535')
vlab_bridge = VirtualLabBridge(self.Machine, _port)
vlab_bridge.start()
print('[Virtual Lab] bridge listening on 127.0.0.1:{0}'.format(_port))
