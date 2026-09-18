*** Settings ***
Resource          ${RENODEKEYWORDS}
Resource          resources/io.resource
Suite Setup       Setup
Suite Teardown    Teardown
Test Setup        Create Candidate Platform
Test Teardown     Reset Emulation
Test Timeout      30 seconds

*** Test Cases ***
Platform Has Expected Devices
    ${pc}=    Execute Command    cpu PC
    Should Not Be Empty    ${pc}
    FOR    ${address}    ${name}    IN
    ...    0x08000000    flash
    ...    0x0807FFFC    flash
    ...    0x20000000    sram
    ...    0x2001FFFC    sram
    ...    0x40020000    gpioA
    ...    0x40020400    gpioB
    ...    0x40020800    gpioC
    ...    0x40023800    rcc
    ...    0x4001204C    ADC1
        ${device}=    Execute Command    sysbus WhatIsAt ${address}
        Should Contain    ${device}    ${name}
    END

SRAM Boundaries Are Independent
    Execute Command    sysbus WriteDoubleWord 0x20000000 0x12345678
    Execute Command    sysbus WriteDoubleWord 0x2001FFFC 0x87654321
    ${first}=    Read Word    0x20000000
    ${last}=    Read Word    0x2001FFFC
    Should Be Equal As Integers    ${first}    0x12345678
    Should Be Equal As Integers    ${last}    0x87654321

GPIO Input And Output Can Be Observed
    # Enable GPIOA/B clocks and configure PA4 as output; no CPU execution.
    Execute Command    sysbus WriteDoubleWord 0x40023830 0x3
    Execute Command    sysbus WriteDoubleWord 0x40020000 0x100
    Execute Command    sysbus WriteDoubleWord 0x40020018 0x10
    ${leds}=    Read LED Bits
    Should Be Equal As Integers    ${leds}    1
    Execute Command    sysbus.gpioB OnGPIO 0 true
    ${idr}=    Read Word    0x40020410
    Should Be True    ($idr & 1) == 1
    Execute Command    sysbus.gpioB OnGPIO 0 false
    ${idr}=    Read Word    0x40020410
    Should Be True    ($idr & 1) == 0

Single ADC Injection Updates DR And EOC
    FOR    ${input}    IN    0    2048    4095
        Inject AnalogInput0    ${input}
        ${dr}=    Read Word    0x4001204C
        ${sr}=    Read Word    0x40012000
        Should Be Equal As Integers    ${dr}    ${input}
        Should Be Equal As Integers    ${sr}    2
    END
    Run Keyword And Expect Error    *0..4095*    Inject AnalogInput0    -1
    Run Keyword And Expect Error    *0..4095*    Inject AnalogInput0    4096
