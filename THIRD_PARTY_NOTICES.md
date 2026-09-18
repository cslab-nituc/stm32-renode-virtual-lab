# Third-party notices and provenance

## Project-authored material

Project code and documentation are licensed under [MIT](LICENSE). The maintainer specified the holders **Makoto Tanabe, Yamamoto, and Arakawa** and year range **2025–2026**.

| Material | Provenance / treatment |
|---|---|
| `renode/platforms/*.repl`, `renode/scripts/*.resc` | Created within this project from scratch, as confirmed by the maintainer; not copies of official Renode samples. Use of Renode syntax/APIs is an external dependency, not evidence of copied code. |
| `bridge/*.py`, `gui/app.py`, `gui/static/app.js` | Project GUI/bridge implementation; standard-library and Renode API usage, no vendored framework. |
| `gui/index.html`, `gui/static/style.css` | Adapted from this project's student-designed training-kit GUI; original design intent retained. External Milligram and Socket.IO CDN dependencies are not included. |
| `tests/renode/` | Project tests; Renode keywords imported from the installed runtime, not copied. |
| `examples/adc-led-v1/main.c` | Project reference implementation using only external standard `stdint.h`; not an ST/CMSIS sample copy. |
| README/docs, `.gitignore` | Project documentation/configuration. |

## Bundled images

| Asset | Provenance | Redistribution status |
|---|---|---|
| `gui/static/img/stm32f446re.png` | Created specifically for this project by a family member of a former student | Research/educational use and redistribution in this repository approved; see the separate permission notice below. |
| `gui/static/img/fan.png` | New original asset created and supplied for this public release | Replacement completed; included under the project MIT policy. No old fan file or reference remains in this candidate. |

### Board illustration permission notice

Created specifically for this project by a family member of a former student. Used with permission for research and educational use. Redistribution in this repository has been approved by the creator through the former student, as confirmed by the maintainer.

The illustration should not be assumed to be covered by the repository MIT License unless explicitly stated. Its inclusion records the permission described here, not an automatic relicensing under MIT or a grant of unrestricted downstream reuse.

Board image provenance and repository redistribution permission are confirmed. No remaining asset provenance blocker is known. The fan is separately treated as the original release asset under the project MIT policy.
 The board depicts ST marks; MIT does not grant trademark rights or imply endorsement. LED, switch, panel and 7-segment graphics are project HTML/CSS, not extra image files. No external image URL is used.

## External runtime dependencies (not bundled)

- **Renode**: external emulator and embedded Python/.NET API runtime. Its [upstream LICENSE](https://github.com/renode/renode/blob/master/LICENSE) states MIT for Renode and separate licenses for its libraries. Check the installed distribution when redistributing it; this repository does not vendor Renode.
- **Renode test support / Robot Framework / Python**: external test environment. `${RENODEKEYWORDS}` comes from that installation. [Renode test documentation](https://renode.readthedocs.io/en/latest/introduction/testing.html).
- **GUI Python 3.10+**: standard library only (`http.server`, `socket`, `threading`, `json`, `pathlib`, `os`, `sys`). Browser JavaScript/CSS has no external library, npm package or CDN requirement. No GUI `requirements.txt` is needed.

No CMSIS, ST device headers, startup, system initialization source, linker scripts, HAL/LL, SVD, GNU Arm toolchain, external firmware runtime, ELF or BIN is included. The reference main.c's GPIO initialization is project code, not vendor system initialization code. A user's external ELF may contain third-party code; its distribution must be reviewed separately.

## Redistribution

Retain the MIT copyright, permission and warranty text when redistributing project code or substantial portions. MIT does not require a separate modification notice; retaining provenance/change records is recommended. The new original fan asset follows the project MIT policy. The board illustration is used and redistributed under the separate permission notice above, not automatically under MIT.

License text reference: [OSI MIT License](https://opensource.org/license/mit).
