[日本語](ja/testing.md)


# Testing

## Four verification levels

| Level | Target | ELF | Status |
|---|---|---|---|
| 1: Platform | [platform.robot](../tests/renode/platform.robot) | None | 4/4 PASS, re-run 2026-09-18 |
| 2: Firmware load | [firmware-load.robot](../tests/renode/firmware-load.robot) | External | 1/1 PASS, re-run 2026-09-18 |
| 3: Scenario | [adc-led-v1.robot](../tests/renode/scenarios/adc-led-v1.robot) | Contract-compatible external ELF | 1/1 PASS, re-run 2026-09-18 |
| 4: GUI | [Manual I/O verification](gui-status.md) | Feature-compatible external ELF | user-reported manual verification |

The re-run used WSL, Renode 1.17.0 (`1.17.0+20260906gitf1dd1b4af`), .NET 8.0.31 and Robot Framework 6.1. GUI verification is not an automated browser test and is not implied by the three Robot suites. The latest GUI-integrated candidate also passed an independent-directory test: all three Robot suites, Web GUI startup, run-gui.resc, external ELF loading, browser display and GUI/Renode integration (user-reported manual verification). Only the candidate and an external ELF were used; no parent private code was required.

Use the `renode-test` and test requirements shipped with your Renode distribution, not standalone `robot`: `${RENODEKEYWORDS}` and the Renode connection are supplied by that runner.

```bash
renode-test tests/renode/platform.robot
renode-test --variable ELF:/absolute/path/to/firmware.elf tests/renode/firmware-load.robot
renode-test --variable ELF:/absolute/path/to/firmware.elf tests/renode/scenarios/adc-led-v1.robot
```

Run from the repository root; replace the placeholder with a real external ELF. On Windows use the actual Windows path, e.g. `ELF:C:/firmware/firmware.elf` (placeholder). Missing ELF is a failure in levels 2/3, not a skipped/pass result. Choose suites intentionally rather than running all with an arbitrary ELF. Tests reset emulation after each case.

## Scenario contract

The [reference main.c](../examples/adc-led-v1/main.c) and adc-led-v1 scenario correspond directly. User-reported successful external PlatformIO build/testing of that source is recorded; PlatformIO is not a repository dependency. Firmware initializes within 10 ms and reflects each injected ADC value within 10 ms of virtual time. LED0–7 = PA4–11 = `(ADC >> 4) & 255`.

| ADC | LED |
|---|---|
| 0 | 0 |
| 2048 | 128 |
| 4095 | 255 |
| 0 again | 0 |

The contract and expected values were not changed. An older firmware implementing a different stepped display is a contract mismatch, not a platform failure. The load test checks vectors, PC and CFSR/HFSR over 1 ms; it does not prove application correctness or physical compatibility.

## Keep output private

Robot output may contain ELF paths and other local information. Do not distribute logs, HTML/XML, snapshots, pyc or ELF. `.gitignore` does not remove existing files. Prefer a separate results working directory and pass absolute suite/ELF paths; the suite resolves its resources relative to itself. The audit used that method. Use an approved-file export list for publication, not a blind directory/Git-history copy.

[Renode testing documentation](https://renode.readthedocs.io/en/latest/introduction/testing.html)
