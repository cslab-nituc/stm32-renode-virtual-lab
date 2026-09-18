# adc-led-v1参考実装

[English](README.md)

[main.c](main.c)は[adc-led-v1.robot](../../tests/renode/scenarios/adc-led-v1.robot)のfirmware側契約を示す[MIT](../../LICENSE)の自作ソースです。完成したbuild projectではありません。外部C環境の標準`stdint.h`のみを参照し、vendor header/source、startup、linkerは同梱しません。

STM32F446REで、注入された12-bit ADC1 DR/SRからLED0–7（PA4–11）へ`(ADC >> 4) & 255`を出します。0→0、2048→128、4095→255、再び0→0。初期化10ms以内、注入後10ms以内の仮想時間で反映します。

GPIOA BSRRでPA4–11だけを更新します。EOCをpollし、簡易モデルではDR読出しでEOCがclearされないため同値再読込みを許容します。実ADCの初期化・変換開始は行わず、そのまま実機ADC例として動くとは主張しません。

利用者のSTM32 build環境（PlatformIO / Make / CMake / CubeIDE等）へ組み込みます。toolchain、C runtime、startup、memory配置、main呼出しは外部環境の責任です。これらやELF/BINは提供しません。

ルートから実ELFを指定します。

```bash
renode-test --variable ELF:/absolute/path/to/firmware.elf tests/renode/scenarios/adc-led-v1.robot
```

この参考ソースを外部PlatformIOでbuildしたELFのscenario PASSは利用者報告として確認済みです。指定済み外部adc-led-v1 ELFも2026-09-18の再実行でPASSしました。今回ソースからのbuild再現は行っていません。ELF同梱・期待値変更はありません。別の段階的表示firmwareの不一致はplatform欠陥ではありません。[firmware仕様](../../docs/ja/firmware-interface.md)・[テスト](../../docs/ja/testing.md)参照。
