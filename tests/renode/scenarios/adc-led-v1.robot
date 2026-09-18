*** Settings ***
Documentation     Only for an ELF implementing the adc-led-v1 contract in docs/testing.md.
Resource          ${RENODEKEYWORDS}
Resource          ../resources/io.resource
Suite Setup       Setup
Suite Teardown    Teardown
Test Teardown     Reset Emulation
Test Timeout      30 seconds

*** Test Cases ***
ADC High Byte Is Reflected On LED0 Through LED7
    Load External Firmware
    # Contract: firmware initializes within 10 ms, then polls ADC1.
    Execute Command    emulation RunFor "0.010"
    FOR    ${input}    ${expected}    IN    0    0    2048    128    4095    255    0    0
        Inject AnalogInput0    ${input}
        Execute Command    emulation RunFor "0.010"
        ${leds}=    Read LED Bits
        Should Be Equal As Integers    ${leds}    ${expected}
        Assert No Recorded CPU Fault
    END