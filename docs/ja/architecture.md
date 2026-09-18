[English](../architecture.md)


# 構成

```text
外部build -> 外部ELF
                |
     run.resc または run-gui.resc
                |
 platform.resc -> stm32f446re.repl -> Renode
                |                    |
          Monitor/Robot       bridge/renode_bridge.py
                                     | localhost TCP :4567
                                 gui/app.py
                                     | localhost HTTP :8001
                                   Browser
```

`platform.resc`はmachine生成のみでCPU開始・socket待受は行いません。`run.resc`は`$global.elf`をロードして実行します。`run-gui.resc`はRenode内Python bridgeも読み込みます。HTTPサーバは別のPython 3.10以上のプロセスです。GUIの外部Python package・JS libraryは不要です。Renode側のPython/.NET API環境はRenodeが提供します。

bridgeは[firmware仕様](firmware-interface.md)の固定GPIO/ADC契約を使い、JSONのstateと検証済みinputだけを受け付けます。任意Monitor APIは公開しません。RobotはGUI/bridgeから独立し、仮想時間の`emulation RunFor`を使います。GUIはホスト時間でpolling（bridge約2ms、browser約200ms。精度保証なし）します。

コードと画像の参照はrepository内で完結します。Renodeと利用者のELFだけが外部依存です。firmwareのdownload/buildは行いません。[参考ソース](../../examples/adc-led-v1/README.ja.md)は外部build環境へ組み込みます。debug mailboxのSRAM予約・読み出しはありません。
