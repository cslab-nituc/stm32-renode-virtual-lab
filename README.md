# STM32F446RE Virtual Lab

[日本語](README.ja.md)

A Renode-based teaching environment for running externally built STM32F446RE firmware and observing virtual I/O through a Web GUI or Robot tests. The GUI preserves the original student-designed training-kit layout.

The input boundary is an **external ELF**. No firmware build system, toolchain, CMSIS/ST headers, startup code, linker script, HAL/LL, or ELF/BIN is bundled. The [reference main.c](examples/adc-led-v1/main.c) belongs in your own STM32 build environment.

## Devices

| Device | Support |
|---|---|
| AnalogInput0 | 12-bit ADC1 DR/SR injection |
| PSW0–3 / TSW0–3 | GPIO inputs |
| LED0–7 | GPIO output display |
| Four-digit 7-segment display | Sampled multiplexed GPIO display |
| Motor | Direction/state visualization only; no torque, load, inertia or speed simulation |
| Encoder feedback | Unsupported |
| AnalogInput1/2, debug mailbox/scope | Visible placeholders, unsupported |

## Quick start

Install Renode separately. Tested runtime: Renode 1.17.0, build `1.17.0+20260906gitf1dd1b4af`, .NET 8.0.31 on WSL. Windows/WSL are not yet selected as the standard classroom environment. See [Windows](docs/installation-windows.md) or [WSL](docs/installation-wsl.md).

1. Open a terminal in this repository's root and run `renode`.
2. In the **Renode Monitor**, replace the placeholder below with the actual external ELF path:

```text
$global.elf = @/absolute/path/to/firmware.elf
include @renode/scripts/run-gui.resc
```

3. In a second terminal at the same root, start the GUI server with Python 3.10+:

```bash
python3 gui/app.py
```

4. Open **http://localhost:8001** in a browser. Run Renode and the Python server in the same OS environment. HTTP listens on `127.0.0.1:8001`, bridge on `127.0.0.1:4567`.
5. Stop the server with Ctrl+C and exit Renode. Use a fresh Renode session when loading another machine/ELF. Repeating the script in an existing session is not the supported restart procedure.

The GUI can be opened before Renode but shows disconnected state and disables inputs. It does not build or select firmware. For Monitor-only execution, use [run.resc](renode/scripts/run.resc) instead. With no ELF, [platform.resc](renode/scripts/platform.resc) creates the platform without starting the CPU.

See [GUI status/startup](docs/gui-status.md), [firmware interface](docs/firmware-interface.md) and [architecture](docs/architecture.md).

## Robot tests

Install the testing dependencies required by your Renode distribution. From this root:

```bash
renode-test tests/renode/platform.robot
renode-test --variable ELF:/absolute/path/to/firmware.elf tests/renode/firmware-load.robot
renode-test --variable ELF:/absolute/path/to/firmware.elf tests/renode/scenarios/adc-led-v1.robot
```

Replace ELF placeholders with a real file outside this repository. Only the scenario requires the `adc-led-v1` behavior contract: ADC `0 / 2048 / 4095 / 0` produces LED `0 / 128 / 255 / 0`. [Reference example](examples/adc-led-v1/README.md).

Regression on 2026-09-18: platform **4/4 PASS**, firmware-load **1/1 PASS**, scenario **1/1 PASS**, using an external ELF. GUI device operation is **user-reported manual verification**, not automated browser verification. Four verification levels and output handling are described in [testing](docs/testing.md). Generated test output is not publication content.

## Structure

```text
renode/      platform and execution/injection scripts
bridge/      Renode-side TCP bridge and shared I/O contract
gui/         local HTTP server, training-kit UI and assets
tests/       platform, firmware-load and scenario Robot tests
examples/    reference firmware source; no build environment
docs/        English documentation
docs/ja/     Japanese counterparts
```

## Limitations

This is neither a complete STM32F446RE model nor a physical hardware simulator. ADC is injection-based; the `0x400` backing memory satisfies Renode page alignment and is not a complete ADC peripheral. Short GPIO pulses/multiplexed digits may be missed by host polling. Motor rotation is an illustrative direction indicator, not a measured speed. Encoder is unsupported. See [simulation limitations](docs/simulation-limitations.md).

## License

Project code and documentation: [MIT License](LICENSE), copyright 2025–2026 Makoto Tanabe, Yamamoto, and Arakawa. Renode is an external dependency, not vendored. The board illustration was created for this project by a family member of a former student. Permission for research/educational use and redistribution in this repository is confirmed through the former student. The illustration is not automatically covered by the repository MIT License; its separate permission is recorded in THIRD_PARTY_NOTICES.md. The fan is a new original asset created for this release and already replaces the old image. See [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md).

Latest independent placement with GUI: **PASS** (user-reported manual verification). The candidate plus an external ELF started without parent private GUI, scripts or source code. All three Robot suites, run-gui.resc, ELF loading, browser display and GUI/Renode integration passed.
