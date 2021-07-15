# oscDebugger
[![Windows Executable Build](https://github.com/dmitrol205/oscDebugger/actions/workflows/build.yml/badge.svg?branch=dev)](https://github.com/dmitrol205/oscDebugger/actions/workflows/build.yml)
---
Window title describe execution state(running/idle)

Keys
+ F2 Set/Remove breakpoint
    +place cursor in desired line in desired code to select

+ F5 Run
    + disable f5,f6,f7,f8 until breakpoint or f9 pressed
+ F6 Step in
+ F7 Step over
    + perform till next instruction in codeView invoked
    + can skip if statement
+ F8 Step out
    + when in init end up its and stops at beggining of frame or frame_ai
    + when in frame or frame_ai end up its iteration and stops at beggining

+ F9 Enter Step Mode

Two dropdowns:
+ code type
    + init
    + frame 
    + frame_ai 
    + macro 
    + trigger
+ code name
    + enables when code type:
        + macro
        + trigger
+ Goto IP
    + switches currently viewed code to the code with the next instruction to execute
    + works only when state is idle

Now `(T.L.<triggerName>)` , `(T.F.<triggerName>)` `(M.V.<sysMacroName>)` don't work properly
+ system variables empty and doesn't update during execution
+ no correct macro name visibility check
+ triggers never invoked
    + non sound and they too
+ not every command checked for their error report
+ variables access can be incorrect in some cases(ai mode for example)
