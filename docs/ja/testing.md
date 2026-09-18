[English](../testing.md)


# テスト

## 4段階の確認

| 段階 | 対象 | ELF | 状態 |
|---|---|---|---|
| 1: Platform | [platform.robot](../../tests/renode/platform.robot) | 不要 | 2026-09-18再実行 4/4 PASS |
| 2: Load | [firmware-load.robot](../../tests/renode/firmware-load.robot) | 外部指定 | 同日再実行 1/1 PASS |
| 3: Scenario | [adc-led-v1.robot](../../tests/renode/scenarios/adc-led-v1.robot) | 契約適合外部ELF | 同日再実行 1/1 PASS |
| 4: GUI | [手動I/O確認](gui-status.md) | 各機能に対応するELF | user-reported manual verification |

再実行環境はWSL、Renode 1.17.0 (`1.17.0+20260906gitf1dd1b4af`)、.NET 8.0.31、Robot Framework 6.1です。GUIは利用者による手動確認で、自動ブラウザテストではありません。Robot成功からGUI全体の成功を推定しません。GUI統合後の最新版も独立directoryで最終確認済みです。Robot 3 suite、Web GUI起動、run-gui.resc、外部ELFロード、ブラウザ表示、GUI/Renode連携すべてPASS（user-reported manual verification）。候補と外部ELFのみを使い、親privateコードへの依存なしで起動しました。

採用Renode付属の`renode-test`とrequirementsを使います。単体の`robot`では`${RENODEKEYWORDS}`や接続が用意されません。

```bash
renode-test tests/renode/platform.robot
renode-test --variable ELF:/absolute/path/to/firmware.elf tests/renode/firmware-load.robot
renode-test --variable ELF:/absolute/path/to/firmware.elf tests/renode/scenarios/adc-led-v1.robot
```

repositoryルートから実行し、仮ELFパスを実ファイルへ置換します。Windowsでは例 `ELF:C:/firmware/firmware.elf` を実パスへ置換します。Level 2/3でELF未指定はFAILで、未実施をPASSにしません。任意ELFで全suiteをまとめて実行せず、適合するsuiteを選択します。各case後にemulationをresetします。

## Scenario契約

[参考main.c](../../examples/adc-led-v1/main.c)とadc-led-v1 scenarioは1対1対応です。このソースを外部PlatformIOでbuildしたELFの成功実績は利用者報告として確認済みです。PlatformIO自体は必須依存ではありません。firmwareは10ms以内に初期化し、注入後10ms以内の仮想時間でLEDへ反映します。LED0–7 = PA4–11 = `(ADC >> 4) & 255`。

| ADC | LED |
|---|---|
| 0 | 0 |
| 2048 | 128 |
| 4095 | 255 |
| 再び0 | 0 |

契約・期待値は変更していません。以前の段階的表示firmwareの不一致は別契約でありplatform failureではありません。Loadテストは1msのvector/PC/CFSR/HFSR検査で、アプリの正しさや実機互換を保証しません。

## 生成物を公開しない

Robot出力にはELFパス等のローカル情報が入ります。ログ、HTML/XML、snapshot、pyc、ELFを配布しません。`.gitignore`は存在済みファイルを消しません。別の結果directoryを作業場所にし、suiteとELFを絶対パス指定する方式を推奨します。suite内部の相対参照は自身の位置から解決します。今回もその方法で実行しました。公開は承認済みファイルの選別方式とし、directoryやGit履歴を全面コピーしません。

[Renode testing documentation](https://renode.readthedocs.io/en/latest/introduction/testing.html)
