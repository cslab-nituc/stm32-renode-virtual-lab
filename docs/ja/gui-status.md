[English](../gui-status.md)


# GUI起動と確認状況

卒研学生による実習キット型デザインを維持します。基板画像は卒業生の家族が本project用に作成したものです。研究・教育用途の使用と本repositoryでの再配布について、卒業生を通じて作成者の許諾を確認済みです。画像自体にrepositoryのMIT Licenseが自動適用されるものではなく、THIRD_PARTY_NOTICES.mdに別の許諾として記載しています。ファンは本release用の新作オリジナルへ差替え済みです。GUIはPython 3.10以上の標準ライブラリ、素のJavaScript、ローカルCSS、PNG2点を使います。Flask、Socket.IO、CDN、pip requirements、外部画像は不要です。

## 起動・終了

1. repositoryルートで`renode`を起動。
2. Monitorで**実際の外部ELFパス**を指定し、GUIスクリプトを読み込みます。

```text
$global.elf = @/absolute/path/to/firmware.elf
include @renode/scripts/run-gui.resc
```

3. 同じルートの別ターミナルで`python3 gui/app.py`（WindowsはPython 3.10以上の`python gui/app.py`）。
4. http://localhost:8001 を開く。HTTPのみでも未接続画面は表示可能ですが、I/Oには各デバイス契約に対応するELFが必要です。
5. HTTPはCtrl+C、bridgeはRenode終了で停止。machine/ELF切替時は新規Renodeセッションを使用します。port競合時は自分の前のセッションを止め、無関係なprocessは終了しないでください。

両processは同じOS環境で起動します。`VLAB_HTTP_PORT`（8001）、`VLAB_BRIDGE_PORT`（4567）で1024–65535のportを指定可能です。bridge portは両processで合わせます。bindは常に127.0.0.1です。WindowsブラウザからWSLへの接続は転送設定に依存します。native Windows実行は今回未確認です。

## 対応と根拠

| 項目 | 実装 | 確認根拠 |
|---|---|---|
| AnalogInput0 | 0–4095単一DR/SR値注入。slider解放/change時送信 | user-reported manual verification |
| PSW0–3 | PB0–3、元GUIのON/OFFボタン | user-reported manual verification |
| TSW0–3 | PB5–8、レバー切替 | user-reported manual verification |
| LED0–7 | PA4–11 ODR表示 | user-reported manual verification |
| 7セグ | PC0–3桁選択、PC4–7数値。PC0が右端 | user-reported manual verification |
| Motor | PC10有効、PC9/PC8方向。それ以外は停止 | user-reported manual verification（可視化のみ） |
| Encoder feedback | 未対応、入力・feedback APIなし | 対象外 |
| AnalogInput1/2 | 表示のみ・操作無効。独立チャネルなし | 対象外 |
| Debug mailbox/scope | 未対応表示、SRAM読み出しなし | 対象外 |

利用者から上記GUI操作の成功報告を受けています。今回の監査ではbrowser/firmwareのGUI自動テストは行っていません。Robot成功はGUI検証の代替ではありません。参考adc-led-v1 ELFだけではswitch・7セグ・Motorの確認はできません。

Motorは方向・状態のみ。**物理挙動・トルク・負荷・慣性・速度simulationなし**。約2msのホストsamplingと0.5秒の桁保持で多重化パルスを取り逃がす場合があります。PSWはブラウザfocus離脱、またはbridgeへの要求が約1秒途絶えると解放されます。背景tabの抑制でも解放され得ます。TSWは状態を保持します。単一利用者・単一ブラウザ用で複数clientの協調制御はありません。

## 最終human test

1. 承認済みファイルだけを別directoryへコピーし、ELFはその外に保持。
2. 各Robot suiteを実行。HTTPのみ起動し、各panel・未接続表示・入力無効を確認。
3. 上記順序で起動。adc-led-v1 ELFでsliderを0/2048/4095/0へ動かして解放し、LED 0/128/255/0を確認。
4. 適切なfirmwareでPSW ON/OFF、focus離脱、全TSW、7セグ全桁、Motor正逆転/停止を確認。
5. Encoder等の未対応表示を確認。
6. Renode停止時の未接続、再起動・再接続を確認。OS/browser/Renode版/ELF hash/機能別結果は公開tree外へ記録。

## ローカル安全性

HTTP Host/Origin、入力名・型・範囲を制限します。wildcard CORS、固定secret、任意Monitor RPC、ELFパスのログ記録はありません。TCP bridgeは認証を持たず、同じPC上のprocessから接続可能です。loopbackは同一hostの別利用者に対する隔離境界ではありません。ネットワーク公開用・production HTTP serverではありません。

## 最新の独立配置結果

**PASS — user-reported manual verification。** 新ファン画像を含む最新候補と外部ELFで、Robot 3 suite、Web GUI/run-gui起動、ELFロード、ブラウザ表示、GUI/Renode連携を独立配置で確認済みです。親privateコードへの依存はありません。Codexのbrowser automationではありません。
