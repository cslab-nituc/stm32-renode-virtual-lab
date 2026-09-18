# STM32F446RE Virtual Lab

[English](README.md)

外部で生成したSTM32F446RE firmwareをRenodeで動かし、Web GUIまたはRobotテストで仮想入出力を観測する教材環境です。卒研学生が実習キットを意識して作った元GUIのデザインを継承します。

境界は**外部ELF**です。ビルドシステム、toolchain、CMSIS/ST header、startup、linker、HAL/LL、ELF/BINは同梱しません。[参考main.c](examples/adc-led-v1/main.c)は利用者の外部STM32ビルド環境へ組み込みます。

## 対応デバイス

| 項目 | 対応 |
|---|---|
| AnalogInput0 | ADC1 DR/SRへの12-bit値注入 |
| PSW0–3 / TSW0–3 | GPIO入力 |
| LED0–7 | GPIO出力表示 |
| 4桁7セグ | 多重化GPIOのサンプリング表示 |
| Motor | 方向・状態の可視化のみ。トルク・負荷・慣性・速度の物理simulationなし |
| Encoder feedback | 未対応 |
| AnalogInput1/2、debug mailbox/scope | 表示のみ・未対応 |

## Quick Start

Renodeは別途導入します。確認環境: WSL / Renode 1.17.0、build `1.17.0+20260906gitf1dd1b4af`、.NET 8.0.31。Windows/WSLの正式採用は未決定です。[Windows](docs/ja/installation-windows.md) / [WSL](docs/ja/installation-wsl.md) を参照してください。

1. このrepositoryのルートで `renode` を起動します。
2. **Renode Monitor**で以下を入力します。ELFの仮パスは実在する外部ELFのパスへ置換してください。

```text
$global.elf = @/absolute/path/to/firmware.elf
include @renode/scripts/run-gui.resc
```

3. 同じルートで別ターミナルを開き、Python 3.10以上で起動します。

```bash
python3 gui/app.py
```

4. ブラウザで **http://localhost:8001** を開きます。RenodeとPythonサーバは同じOS環境で起動します。HTTPは `127.0.0.1:8001`、bridgeは `127.0.0.1:4567` です。
5. サーバをCtrl+Cで停止し、Renodeも終了します。別machine/ELFへ切替える際はRenodeを新規起動してください。同じセッションでのスクリプト再実行は推奨起動手順ではありません。

GUIだけ先に起動すると未接続表示・入力無効になります。GUIはfirmwareをビルド・選択しません。Monitorのみの実行は [run.resc](renode/scripts/run.resc) を使います。ELF不要の [platform.resc](renode/scripts/platform.resc) はCPUを開始しません。

[GUI手順・状態](docs/ja/gui-status.md)、[firmware仕様](docs/ja/firmware-interface.md)、[構成](docs/ja/architecture.md)も参照してください。

## Robotテスト

採用Renodeが要求するテスト依存を別途導入し、ルートから実行します。

```bash
renode-test tests/renode/platform.robot
renode-test --variable ELF:/absolute/path/to/firmware.elf tests/renode/firmware-load.robot
renode-test --variable ELF:/absolute/path/to/firmware.elf tests/renode/scenarios/adc-led-v1.robot
```

ELFは候補外の実ファイルを指定します。scenarioだけはADC `0 / 2048 / 4095 / 0` → LED `0 / 128 / 255 / 0` の専用契約を要求します。[参考実装](examples/adc-led-v1/README.ja.md)。

2026-09-18の再実行: platform **4/4 PASS**、firmware-load **1/1 PASS**、scenario **1/1 PASS**（外部ELF）。GUIは **user-reported manual verification（利用者による手動確認）** であり、自動ブラウザ検証ではありません。[4段階の検証と結果保存](docs/ja/testing.md)を参照してください。テスト生成物は公開対象外です。

## 構成

```text
renode/      platform・実行/値注入スクリプト
bridge/      Renode TCP bridge・共有I/O契約
gui/         ローカルHTTP・実習キットGUI・画像
tests/       platform / load / scenario Robotテスト
examples/    参考ソースのみ（ビルド環境なし）
docs/        英語標準文書
docs/ja/     対応する日本語文書
```

## 制約

STM32F446RE全体・物理実機全体を再現しません。ADCは値注入で、`0x400`はRenodeページ整列要件のための確保サイズです。全領域をADCとして実装していません。ホストpollingでは短いGPIOパルス・多重化表示を取り逃がす場合があります。Motorの回転は方向表現で速度測定ではなく、Encoderは未対応です。[制約一覧](docs/ja/simulation-limitations.md)。

## License

自作コード・文書は [MIT License](LICENSE)、copyright 2025–2026 Makoto Tanabe, Yamamoto, and Arakawa。Renodeは外部依存で、本体を同梱しません。基板画像は卒業生の家族が本project用に作成したものです。研究・教育用途の使用と本repositoryでの再配布について、卒業生を通じて作成者の許諾を確認済みです。画像自体にrepositoryのMIT Licenseが自動適用されるものではなく、THIRD_PARTY_NOTICES.mdに別の許諾として記載しています。ファンは本release用の新作オリジナル画像へ差替え済みです。[THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md)。

GUI追加後の最新版の独立配置: **PASS**（user-reported manual verification）。候補と外部ELFのみで起動し、親privateのGUI・script・sourceには依存しません。Robot 3 suite、run-gui.resc、ELFロード、ブラウザ表示、GUI/Renode連携すべてPASSです。
