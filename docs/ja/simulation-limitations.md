[English](../simulation-limitations.md)


# シミュレーションの制約

STM32F446RE全体や物理実機全体のsimulationではありません。GUIは対応範囲の観測可能なI/O挙動を表示します。

| 項目 | 制約 |
|---|---|
| ADC | DR/SR値注入のみ。電圧・変換時間・チャネル選択・EOC自動clear・scan/DMAなし |
| ADC memory | 0x400はRenode guest page alignmentのため。領域全体をADC peripheralとして実装していない |
| FLASH control | 単なるmemory。erase/program/wait state/保護/busyなし |
| Clock/SysTick | SysTick設定16MHz。PLL/APB全体への反映・全割込み動作は保証しない |
| RTC | RCC参照先として存在するが対応対象外 |
| TIM3/TIM6、UART/DMA/USB | 未対応 |
| GPIO | 電気特性・負荷・配線遅延・接点bounceなし |
| 7セグ/GUI | ホストpollingで短いパルス・桁選択を取り逃がす可能性。約2ms sampling・0.5秒保持 |
| Motor | 方向・状態の可視化のみ。トルク・負荷・慣性・速度simulationなし |
| Encoder feedback | 未対応 |
| Debug mailbox/scope | 表示のみ・未対応。SRAM予約・読み出しなし |
| Timing | 仮想時間とwall clockは別。実機の命令周期・割込み遅延は保証しない |

1msのload smoke testはvector/PC範囲とCFSR/HFSR記録を検査するだけです。すべてのfault、clear済fault、例外内無限ループを検出できず、firmwareの正しさ・実機互換の証明ではありません。ELF不要のplatformテストも命令実行の正しさを証明しません。実機検証は別途必要です。

Renode 1.17.0実行時に、以前の静的検査で検出できなかった問題を確認しました。`.repl`コメントは`#`ではなく`//`を使います。ADCのMemory.MappedMemoryは`0x100`ではなく`size: 0x400`が必要です。この領域で定義する挙動はADC1 SR/DRだけです。
