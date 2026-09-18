[English](../firmware-interface.md)

# External firmware interface

Status: Renode 1.17.0のplatform/load/scenario再実行成功。実機照合は未確認。

これはビルド手順ではなく、入力ELFに要求する条件です。PlatformIO / Make / CubeIDE等には依存しません。

## CPU and image

- Target: STM32F446RE / Cortex-M4、little-endian、Thumbコード。
- 入力は実行アドレスが確定した32-bit ARM ELFを想定。再配置可能な`.o`、BIN、HEX、動的リンク実行環境は対象外。
- ELFのロード対象がモデルのFLASH/SRAMへ収まり、必要な初期化イメージを含むこと。
- FPU: 元の対象はM4Fだが、命令・例外・CPACR初期化を含む互換性は要確認。初期の検証用ELFでは浮動小数点命令への依存を避ける。hard/soft ABIだけで実行互換を保証しない。
- シンボル/DWARFは本候補のテスト要件ではない。レジスタ・固定アドレスだけを使う。strip済みELFの実ロードは要確認。
- semihosting、外部OSサービス、未配置peripheralへの依存を持たないこと。

## Memory and reset

| 項目 | 契約 |
|---|---|
| FLASH | `0x08000000..0x0807FFFF`、512 KiB |
| SRAM | `0x20000000..0x2001FFFF`、128 KiB。mailbox予約なし |
| Vector table | 初期版は`0x08000000`を要求。bootloaderによるオフセット配置は対象外 |
| initial SP | ベクタ先頭word。`0x20000000 < SP <= 0x20020000`、8-byte aligned |
| Reset Handler | ベクタ第2word。bit 0が1（Thumb）、実アドレスがFLASH内 |
| VTOR | firmwareが必要なvector table位置を設定。ロード時の自動設定に依存しない設計を推奨。採用Renode版の挙動は要確認 |
| `.data` | FLASH側初期値をSRAMへコピーする処理はfirmwareの責任 |
| `.bss` | ゼロ初期化はfirmwareの責任 |
| ELF entry | Reset Handlerとの整合を要求。PC/SPのLoadELF時設定とreset後の再読込みは採用版で要確認 |

リンカスクリプトやstartupは提供しません。SP上限値はメモリ終端の1バイト先を指すスタック頂点として認めます。

## Clock and peripherals

clock initializationとGPIO initializationはfirmwareの責任です。RCCモデルはありますが、実機と同じPLL/APB変化が全モデルへ反映される保証はありません。まずHSI 16 MHzを想定した最小初期化で確認してください。

| 機能 | アドレス/状態 |
|---|---|
| GPIOA/B/C | `0x40020000` / `0x40020400` / `0x40020800`、各`0x400`領域 |
| RCC | `0x40023800`、Renode STM32F4_RCC |
| SysTick/NVIC | `0xE000E000`、SysTick周波数16 MHz固定設定。割込み動作は要確認 |
| RTC | `0x40002800`、RCCの参照先として残す。教材の対応機能には含めない |
| FLASH control | `0x40023C00`から`0x400`バイト、単なるメモリ |
| ADC1 slot | `0x40012000`から`0x400`バイト、page-alignedな単なるメモリ |
| TIM3/TIM6 | 初期候補から除外 |
| UART/DMA/USB等 | 未対応。STM32型名だけで利用可能とは判断しない |

## GPIO mapping

- LED0..7: PA4..PA11。active-high。RobotではGPIOA ODRのbit 4..11を観測。
- Monitorによる入力例: PB0。`sysbus.gpioB OnGPIO 0 true/false`。
- PSW0–3: PB0–3。TSW0–3: PB5–8。active-high。
- 7セグ: PC0–3が桁選択（PC0が右端）、PC4–7が4-bit数値。
- Motor: PC10=MST、PC9=MIN1、PC8=MIN2。MST=1でMIN1/MIN2=1/0なら正転、0/1なら逆転。それ以外は停止。方向・状態のみ。Encoder未対応。
- GPIO clock、mode、pull等を必要に応じてfirmwareが設定する。物理配線・電圧・接点バウンスは再現しない。

## AnalogInput0

単一の12-bit整数値（0..4095）だけを扱います。PA0/ADC1 channel 0相当の教材入力という論理名であり、実際のアナログ端子から変換するモデルではありません。

`inject-adc.resc`はDR (`0x4001204C`)へ値を書き、SR (`0x40012000`)を`0x2`（EOCのみ）に置き換えます。チャネル引数、AnalogInput1/2、ADC2/3はありません。SRの他のbitは保持しません。

firmware側はこの簡易DR/SR契約に対応する必要があります。読み出しによるEOC自動clear、SWSTARTからの自動変換、scan/DMA等を前提とする処理は対象外です。入力注入の時点と期待出力はシナリオごとに決めます。

Renode 1.17.0のguest page alignment要件により`0x400`バイトを確保します。当初の`0x100`は実行時にalignmentエラーとなりました。領域全体のADC peripheral実装を意味せず、意味を定義しているのは上記SR/DRだけです。範囲には他ADC相当アドレスも含まれますが、ADC2/ADC3等は契約上未対応です。

## Debug mailbox

初期版にはありません。SRAM末尾も通常のfirmware領域で、常時読出しや予約を要求しません。将来追加する場合は明示的な有効化、領域予約、データ型、更新規約を別契約にします。

## Behavior contracts

ロード可能なELFと、特定のシナリオに合格するELFは別です。[テスト仕様](testing.md)の`adc-led-v1`は入力値の上位8bitをLEDへ出す専用契約であり、従来教材を含む任意のELFへ適用しません。

[参考実装](../../examples/adc-led-v1/README.ja.md)はこの値注入契約専用です。startupや実ADCの変換開始処理は提供しません。
