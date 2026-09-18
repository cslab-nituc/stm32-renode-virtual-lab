[English](../installation-wsl.md)


# WSL導入（評価中）

完成した実習標準手順ではなく、導入確認の骨組みです。WSL上のRenode 1.17.0回帰テストと利用者によるGUI確認の実績があります。

- [公式導入手順](https://renode.readthedocs.io/en/latest/introduction/installing.html)に従ってRenodeを別途導入し、版/runtimeを記録。
- ELF実行だけならRenode、Robotにはその版のrequirementsと`renode-test`が必要。
- GUIはPython 3.10以上の標準ライブラリとbrowserのみ。外部Python/JS package不要。ルートから`python3 gui/app.py`を実行。
- Renode/bridge/GUI serverを同じWSL環境へ置き、[起動順序](gui-status.md)に従ってhttp://localhost:8001を開く。Windows browserからの転送設定を確認し、全interface bindへ変更しない。
- Git/editorは任意。PlatformIO、ARM GCC、VS Code、実機USB設定はELF入力後の実行要件ではない。

新しいRenode Monitor内（PowerShell/bashではない）で、仮パスを実ELFへ置換して実行します。

```text
$global.elf = @/absolute/path/to/firmware.elf
include @renode/scripts/run-gui.resc
```

空白・非ASCIIパスと実習標準環境はhuman testで要確認。[テスト](testing.md)、[終了方法・port](gui-status.md)、[制約](simulation-limitations.md)。
