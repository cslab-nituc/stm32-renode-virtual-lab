# adc-led-v1 reference example

[日本語](README.ja.md)

[main.c](main.c) implements the firmware-side contract of [adc-led-v1.robot](../../tests/renode/scenarios/adc-led-v1.robot). It is project source under the [MIT License](../../LICENSE), not a complete firmware project. Only the external C environment's standard `stdint.h` is included; no vendor header/source, startup or linker script is bundled.

Target: STM32F446RE. AnalogInput0: injected 12-bit ADC1 DR/SR. Output: PA4–11 (LED0–7) = `(ADC >> 4) & 255`: 0→0, 2048→128, 4095→255, 0→0 again. Initialize within 10 ms and reflect each injection within another 10 ms of virtual time.

GPIOA BSRR updates only PA4–11. The example polls EOC; repeated DR reads are intentional because the injection stub does not clear EOC. It does not configure/start a physical ADC conversion and is not claimed to run unchanged as a real-board ADC example.

Integrate this file into your own STM32 build environment (PlatformIO, Make, CMake, CubeIDE or another). That environment supplies toolchain, C runtime, startup, memory layout and main entry. This repository does not provide those components or distribute the resulting ELF/BIN.

From the repository root, replace the placeholder with your external ELF:

```bash
renode-test --variable ELF:/absolute/path/to/firmware.elf tests/renode/scenarios/adc-led-v1.robot
```

An external PlatformIO build of this reference source has passed the scenario (user-reported). The supplied external adc-led-v1 ELF also passed the 2026-09-18 regression. The source-to-binary build was not reproduced in this audit. No ELF was copied into this repository and expected values were not changed. An unrelated stepped-display firmware is not evidence of a platform defect. See [firmware interface](../../docs/firmware-interface.md) and [testing](../../docs/testing.md).
