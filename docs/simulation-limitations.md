[日本語](ja/simulation-limitations.md)


# Simulation limitations

This is not a complete STM32F446RE simulation or a complete physical hardware simulation. The GUI shows observable I/O behavior only where supported.

| Area | Limitation |
|---|---|
| ADC | DR/SR injection only; no voltage, conversion timing, channel selection, automatic EOC clear or scan/DMA |
| ADC memory | 0x400 bytes required for Renode guest page alignment; not a full ADC peripheral |
| FLASH control | Plain mapped memory; no erase/program/wait-state/protection/busy behavior |
| Clock/SysTick | SysTick configured at 16 MHz; complete PLL/APB propagation and interrupts not guaranteed |
| RTC | Present only as RCC collaborator; not supported |
| TIM3/TIM6, UART/DMA/USB | Unsupported |
| GPIO | No electrical characteristics, load, wiring delay or contact bounce |
| 7-segment/GUI | Host polling can miss short pulses or multiplex selections; about 2 ms sampling, 0.5 s digit retention |
| Motor | Rotation direction/state visualization only; no torque, load, inertia or speed simulation |
| Encoder feedback | Unsupported |
| Debug mailbox/scope | Visible but unsupported; no SRAM reservation or reads |
| Timing | Virtual time differs from wall clock; no hardware instruction-cycle or interrupt-latency guarantee |

The 1 ms firmware-load smoke test checks vector/PC bounds and recorded CFSR/HFSR status. It cannot detect all faults, cleared faults or infinite exception loops, and is not proof of correct firmware or real-hardware compatibility. The ELF-free platform test does not establish instruction execution correctness. Physical-board validation remains separate.

Renode 1.17.0 runtime testing exposed two issues not caught by the earlier static audit: `.repl` uses `//` comments, not `#`; ADC Memory.MappedMemory requires `size: 0x400`, not `0x100`. Only ADC1 SR/DR behavior is defined in that range.
