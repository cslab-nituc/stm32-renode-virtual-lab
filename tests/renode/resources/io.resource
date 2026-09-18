*** Settings ***
Library         OperatingSystem
Library         String

*** Variables ***
${CANDIDATE_ROOT}    ${CURDIR}/../../..
${ELF}              ${EMPTY}

*** Keywords ***
Create Candidate Platform
    ${root}=    Evaluate    pathlib.Path($CANDIDATE_ROOT).resolve().as_posix()    modules=pathlib
    Should Not Contain    ${root}    "
    Should Not Contain    ${root}    \n
    Should Not Contain    ${root}    \r
    Set Test Variable    ${SCRIPT_ROOT}    ${root}/renode/scripts
    Execute Command    include "${SCRIPT_ROOT}/platform.resc"

Load External Firmware
    Should Not Be Empty    ${ELF}    Supply external ELF using renode-test --variable ELF:<absolute-path>.
    File Should Exist    ${ELF}
    ${elf_path}=    Evaluate    pathlib.Path($ELF).resolve().as_posix()    modules=pathlib
    Should Not Contain    ${elf_path}    "
    Should Not Contain    ${elf_path}    \n
    Should Not Contain    ${elf_path}    \r
    Create Candidate Platform
    Execute Command    machine Reset
    Execute Command    sysbus LoadELF "${elf_path}"

Read Word
    [Arguments]    ${address}
    ${raw}=    Execute Command    sysbus ReadDoubleWord ${address}
    ${value}=    Convert To Integer    ${raw}    16
    RETURN    ${value}

Inject AnalogInput0
    [Arguments]    ${value}
    ${value}=    Convert To Integer    ${value}
    Should Be True    0 <= $value <= 4095    AnalogInput0 must be in 0..4095.
    Execute Command    $adc=${value}
    Execute Command    include "${SCRIPT_ROOT}/inject-adc.resc"

Read LED Bits
    ${odr}=    Read Word    0x40020014
    ${leds}=    Evaluate    ($odr >> 4) & 255
    RETURN    ${leds}

Assert No Recorded CPU Fault
    ${cfsr}=    Read Word    0xE000ED28
    ${hfsr}=    Read Word    0xE000ED2C
    Should Be Equal As Integers    ${cfsr}    0
    Should Be Equal As Integers    ${hfsr}    0
    # These registers are only a bounded smoke check, not proof of correctness.
