[日本語](ja/firmware-interface.md)


# External firmware interface

This is an input contract, not a build guide. Platform, load and adc-led-v1 regressions passed on Renode 1.17.0; physical hardware equivalence is unverified.

## CPU and ELF

- STM32F446RE / Cortex-M4, little-endian Thumb code; linked 32-bit ARM ELF, not relocatable objects, BIN/HEX or a dynamically linked application.
- Loadable sections and initial data must fit the FLASH/SRAM map below.
- Avoid reliance on FPU instructions until instruction/exception/CPACR compatibility is checked. Hard/soft ABI alone does not establish compatibility.
- Tests do not require symbols/DWARF; actual loading of stripped ELF is not separately verified.
- No reliance on semihosting, OS services or unmodelled peripherals.

| Item | Contract |
|---|---|
| FLASH | 0x08000000–0x0807FFFF (512 KiB) |
| SRAM | 0x20000000–0x2001FFFF (128 KiB); no mailbox reservation |
| Vector table | 0x08000000; bootloader offset layouts outside this contract |
| Initial SP | First vector word; 0x20000000 < SP <= 0x20020000, 8-byte aligned |
| Reset handler | Second vector word; Thumb bit set, actual address in FLASH |
| VTOR | Firmware sets the required vector location; do not assume automatic setup |
| .data / .bss | Firmware startup must copy/zero these and call main |
| ELF entry | Consistent with reset handler; loading/reset semantics must be checked for other ELF layouts |

Startup and linker scripts are external. The top-of-stack address may be one byte beyond SRAM. Clock/GPIO initialization is the firmware's responsibility. Start with minimal initialization compatible with HSI 16 MHz; RCC presence does not imply complete PLL/APB timing emulation.

## Devices and wiring

| Device | Address / contract |
|---|---|
| GPIOA/B/C | 0x40020000 / 0x40020400 / 0x40020800; 0x400 each |
| LED0–7 | PA4–11, active-high; ODR bits 4–11 observed |
| PSW0–3 | PB0–3, active-high |
| TSW0–3 | PB5–8, active-high |
| 7-segment | PC0–3 select digit (PC0 rightmost); PC4–7 encode 0–15 |
| Motor | PC10=MST, PC9=MIN1, PC8=MIN2; enabled 1/0 forward, 0/1 reverse, otherwise stop |
| Encoder | Unsupported |
| RCC | 0x40023800, Renode STM32F4_RCC |
| NVIC/SysTick | 0xE000E000, configured SysTick 16 MHz; full interrupt behavior unverified |
| RTC | 0x40002800, RCC collaborator only; unsupported teaching API |
| FLASH control | 0x40023C00, 0x400 bytes of plain mapped memory |
| ADC1 injection | 0x40012000, 0x400 bytes of plain mapped memory |
| TIM3/TIM6, UART/DMA/USB | Not supported |

Configure GPIO clock, mode and pulls in firmware. Voltage, wiring delay and switch bounce are not modelled. GUI Motor is direction/state only, not physical dynamics.

## AnalogInput0

A single integer 0–4095, logically PA0/ADC1 channel 0 for teaching. [inject-adc.resc](../renode/scripts/inject-adc.resc) writes DR (0x4001204C) then replaces SR (0x40012000) with 0x2 (EOC). Other SR bits are not preserved. Bridge input uses the same two writes.

No real analog conversion, channel selection, AnalogInput1/2 or ADC2/3 is implemented. DR reads do not automatically clear EOC; SWSTART, scan, DMA and continuous conversion are not simulated. Firmware must accept this injection contract.

The 0x400 allocation is required by Renode 1.17.0 guest page alignment (0x100 failed at runtime). It does not implement a complete ADC peripheral or neighboring ADC devices; only SR/DR have defined injection meaning.

## Debug mailbox and behavior

No mailbox is reserved or read. Visible debug placeholders have no firmware contract. A loadable ELF is not necessarily [adc-led-v1 compatible](testing.md). The [reference main.c](../examples/adc-led-v1/README.md) is specific to this injection contract, not a physical ADC driver.
