"""Virtual Lab v1: fixed I/O contract, usable by CPython and IronPython.

New implementation of the existing training-board wiring/decoding rules.
Publication rights/license: see THIRD_PARTY_NOTICES.md.
"""
try:
    INTEGER_TYPES = (int, long)
except NameError:
    INTEGER_TYPES = (int,)

SWITCH_PINS = dict([('PSW%d' % i, i) for i in range(4)] +
                   [('TSW%d' % i, i + 5) for i in range(4)])


def validate_input(data):
    if not isinstance(data, dict) or set(data) != set(['signal', 'value']):
        raise ValueError('Expected signal and value only')
    signal, value = data['signal'], data['value']
    if signal == 'AnalogInput0':
        if isinstance(value, bool) or not isinstance(value, INTEGER_TYPES) or not 0 <= value <= 4095:
            raise ValueError('AnalogInput0 must be an integer in 0..4095')
    elif isinstance(signal, str) and signal in SWITCH_PINS:
        if type(value) is not bool:
            raise ValueError('Switch value must be boolean')
    else:
        # IronPython JSON strings may be unicode, so accept known keys directly.
        try:
            known_switch = signal in SWITCH_PINS
        except TypeError:
            known_switch = False
        if not known_switch or type(value) is not bool:
            raise ValueError('Unknown input signal')
    return signal, value


def motor_state(gpio_c):
    enabled = bool(gpio_c & (1 << 10))
    min1, min2 = bool(gpio_c & (1 << 9)), bool(gpio_c & (1 << 8))
    if enabled and min1 and not min2:
        return 'forward'
    if enabled and min2 and not min1:
        return 'reverse'
    return 'stop'


class DisplayLatch(object):
    """Retain sampled multiplexed digits briefly; not cycle-accurate capture."""
    def __init__(self):
        self.values = [None] * 4
        self.seen = [-1.0] * 4

    def sample(self, gpio_c, now):
        select = gpio_c & 15
        # Ignore transients with multiple active digit selectors.
        if select in (1, 2, 4, 8):
            bit = (1, 2, 4, 8).index(select)
            index = 3 - bit
            self.values[index] = (gpio_c >> 4) & 15
            self.seen[index] = now

    def digits(self, now):
        return [v if 0 <= now - t < 0.5 else None
                for v, t in zip(self.values, self.seen)]
