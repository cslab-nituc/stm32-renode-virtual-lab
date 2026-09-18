*** Settings ***
Resource          ${RENODEKEYWORDS}
Resource          resources/io.resource
Suite Setup       Setup
Suite Teardown    Teardown
Test Teardown     Reset Emulation
Test Timeout      30 seconds

*** Test Cases ***
External ELF Loads And Runs For A Short Interval
    Load External Firmware
    ${sp}=    Read Word    0x08000000
    ${reset}=    Read Word    0x08000004
    Should Be True    0x20000000 < $sp <= 0x20020000 and $sp % 8 == 0
    Should Be True    ($reset & 1) == 1 and 0x08000000 <= ($reset & ~1) < 0x08080000
    Execute Command    emulation RunFor "0.001"
    ${raw_pc}=    Execute Command    cpu PC
    ${pc}=    Convert To Integer    ${raw_pc}    16
    Should Be True    0x08000000 <= $pc < 0x08080000 or 0x20000000 <= $pc < 0x20020000
    Assert No Recorded CPU Fault
