[日本語](ja/installation-wsl.md)


# WSL installation (under evaluation)

This is a validation outline, not a completed classroom installation standard. Renode 1.17.0 regression and user-reported GUI operation have been confirmed on WSL.

- Install Renode separately using its [official instructions](https://renode.readthedocs.io/en/latest/introduction/installing.html). Record the actual version/runtime.
- ELF-only execution requires Renode. Robot tests additionally require that release's test requirements and `renode-test`.
- GUI requires Python 3.10+ standard library and a browser; no external Python/JS packages. Use `python3 gui/app.py` from the repository root.
- Keep Renode, its bridge and GUI Python server in the same WSL environment. Open http://localhost:8001 after [GUI startup](gui-status.md). Windows browser access to WSL requires local forwarding; do not solve it by binding to all interfaces.
- Git/editor choice does not affect the ELF boundary. PlatformIO, ARM GCC, VS Code and USB hardware setup are not runtime prerequisites.

In a fresh Renode Monitor (not PowerShell/bash), replace this placeholder with your real external file:

```text
$global.elf = @/absolute/path/to/firmware.elf
include @renode/scripts/run-gui.resc
```

Paths containing spaces/non-ASCII characters and the final classroom configuration still require human validation. [Tests](testing.md), [shutdown and ports](gui-status.md), [limitations](simulation-limitations.md).
