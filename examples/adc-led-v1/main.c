/*
 * Reference implementation of the adc-led-v1 injection contract.
 *
 * This example is provided to illustrate the firmware-side contract used by
 * tests/renode/scenarios/adc-led-v1.robot.
 *
 * No vendor headers, startup code, or linker scripts are included.
 */
#include <stdint.h>

#define REG32(address) (*(volatile uint32_t *)(uintptr_t)(address))
#define RCC_AHB1ENR REG32(0x40023830u)
#define GPIOA_MODER REG32(0x40020000u)
#define GPIOA_OTYPER REG32(0x40020004u)
#define GPIOA_PUPDR REG32(0x4002000cu)
#define GPIOA_BSRR REG32(0x40020018u)
#define ADC1_SR REG32(0x40012000u)
#define ADC1_DR REG32(0x4001204cu)

#define LED_MASK (0xffu << 4)
#define LED_MODE_MASK (0xffffu << 8)

int main(void)
{
    RCC_AHB1ENR |= 1u; /* GPIOA clock enable. */
    (void)RCC_AHB1ENR; /* Read back before accessing GPIOA. */
    GPIOA_BSRR = LED_MASK << 16; /* Initial LED state: all off. */
    GPIOA_OTYPER &= ~LED_MASK;
    GPIOA_PUPDR &= ~LED_MODE_MASK;
    GPIOA_MODER = (GPIOA_MODER & ~LED_MODE_MASK) | (0x5555u << 8);

    for (;;) {
        if ((ADC1_SR & 2u) != 0u) {
            const uint32_t adc = ADC1_DR & 0xfffu;
            const uint32_t leds = (adc >> 4) & 0xffu;
            const uint32_t pins = leds << 4;
            /* Set/reset only PA4..PA11, leaving other output pins alone. */
            GPIOA_BSRR = ((LED_MASK & ~pins) << 16) | pins;
        }
        /* The injection stub does not clear EOC on DR reads. Repeated reads
         * are intentional; each later injection replaces DR with a new value.
         */
    }
}
