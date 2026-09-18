[日本語](ja/architecture.md)


# Architecture

```text
External build -> external ELF (outside this repository)
                         |
            run.resc or run-gui.resc
                         |
        platform.resc -> stm32f446re.repl -> Renode
                         |                   |
                   Monitor/Robot       bridge/renode_bridge.py
                                             | localhost TCP :4567
                                         gui/app.py
                                             | localhost HTTP :8001
                                           Browser
```

`platform.resc` creates a fresh machine without starting the CPU or opening sockets. `run.resc` loads `$global.elf` and starts execution. `run-gui.resc` additionally includes the Python bridge inside Renode. The HTTP server is a separate Python 3.10+ process. No external Python packages or JavaScript libraries are needed for the GUI. Renode supplies its embedded Python/.NET API environment.

The bridge uses fixed GPIO/ADC mappings in [firmware-interface](firmware-interface.md); it exposes only JSON `state` and validated `input` operations. No arbitrary Monitor API is exposed. Robot tests are independent of GUI/bridge and use virtual-time `emulation RunFor`. GUI observations use host-time polling (approximately 2 ms in the bridge and 200 ms in the browser, not timing guarantees).

All code/assets are resolved within this repository. Renode and the user-supplied ELF are external dependencies. No firmware is downloaded or compiled. The [reference source](../examples/adc-led-v1/README.md) belongs in an external build environment. No debug mailbox memory is reserved or read.
