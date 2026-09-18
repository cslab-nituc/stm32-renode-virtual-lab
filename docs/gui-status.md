[日本語](ja/gui-status.md)


# GUI startup and verification status

The original student-created training-kit design is retained. The board illustration was created for this project by a family member of a former student. Permission for research/educational use and redistribution in this repository is confirmed through the former student. The illustration is not automatically covered by the repository MIT License; its separate permission is recorded in THIRD_PARTY_NOTICES.md. The fan is a new original asset created for this release; the old fan is no longer included. The GUI uses Python 3.10+ standard library, plain JavaScript, local CSS and two local PNG files. No Flask, Socket.IO, CDN, pip requirements or external images are required.

## Startup and shutdown

1. In the repository root run `renode`.
2. In its Monitor set the **actual external ELF path**, then load the GUI script:

```text
$global.elf = @/absolute/path/to/firmware.elf
include @renode/scripts/run-gui.resc
```

3. In another terminal in the same root run `python3 gui/app.py` (Windows: `python gui/app.py` with Python 3.10+).
4. Open http://localhost:8001. The server alone can display the disconnected UI but cannot perform I/O. The ELF must implement the corresponding device contract.
5. Ctrl+C stops HTTP; exit Renode to stop its bridge. Start a fresh Renode session for machine/ELF replacement. If ports are occupied, stop your earlier session; do not kill unrelated processes.

Run both processes in one OS environment. `VLAB_HTTP_PORT` (8001) and `VLAB_BRIDGE_PORT` (4567) can select ports 1024–65535; set the same bridge port in both process environments. Bind is always 127.0.0.1. A browser accessing WSL from Windows depends on the local forwarding configuration; native Windows execution is not verified here.

## Support versus evidence

| Component | Implementation | Evidence |
|---|---|---|
| AnalogInput0 | 0–4095, single DR/SR injection; slider submits on release/change | user-reported manual verification |
| PSW0–3 | PB0–3, separate ON/OFF buttons retained from original GUI | user-reported manual verification |
| TSW0–3 | PB5–8, lever toggles | user-reported manual verification |
| LED0–7 | PA4–11 ODR display | user-reported manual verification |
| 7-segment | PC0–3 selector, PC4–7 numeric code; PC0 rightmost | user-reported manual verification |
| Motor | PC10 enable, PC9/PC8 direction; other states stop | user-reported manual verification; visualization only |
| Encoder feedback | Unsupported; no input/feedback API | Not applicable |
| AnalogInput1/2 | Visible disabled controls; no independent channels | Not applicable |
| Debug mailbox/scope | Visible unsupported placeholders; no SRAM reading | Not applicable |

The user reported these GUI operations; this audit did not run automated browser/firmware GUI tests. Regression Robot tests do not establish GUI behavior. The reference adc-led-v1 ELF alone is not a test of switches, 7-segment or Motor.

Motor animation indicates direction/state only: **no physical motor dynamics, torque, load, inertia or speed simulation**. Approximately 2 ms host sampling and 0.5 s digit retention can miss multiplexed pulses. PSW is released on browser blur or after bridge requests cease for about one second; background throttling may release it. Toggles retain their input state. Use one local user and one browser; there is no multi-client coordination.

## Final human test

1. Copy only approved candidate files to an independent directory; keep the ELF outside it.
2. Run each applicable Robot suite. Start HTTP alone: confirm all panels, disconnected status and disabled live inputs.
3. Follow the startup sequence. With adc-led-v1 ELF, move the slider to 0/2048/4095/0, release it and observe LED values 0/128/255/0.
4. With suitable firmware, verify PSW ON/OFF, focus-loss release, each TSW, every 7-segment digit and Motor forward/reverse/stop.
5. Confirm Encoder/other placeholders are clearly unsupported.
6. Stop Renode: confirm disconnection indication and restart/reconnection behavior. Record OS, browser, Renode version, ELF hash and per-device results outside the publication tree.

## Local security model

HTTP Host/Origin and input names/types/ranges are restricted. No wildcard CORS, fixed secret, arbitrary Monitor RPC or firmware-path logging is present. The raw TCP bridge is unauthenticated and reachable by other local processes. Loopback is not a boundary against other users on the same host. This is not a network service or a production HTTP server.

## Latest independent placement result

**PASS — user-reported manual verification.** The latest candidate, including the new fan image, was tested independently with an external ELF. All three Robot suites, Web GUI/run-gui startup, ELF loading, browser display and GUI/Renode integration passed without parent private code. This was not Codex browser automation.
