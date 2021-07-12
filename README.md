# oscDebugger

window title describe execution state(running/wait)

F2 Set/Remove breakpoint(place cursor in desired line in desired code to select)

F5 Run(disable f5,f6,f7,f8 until breakpoint or f9 pressed)
F6 Step in
F7 Step over(instruction except end of code)
F8 Step out(of code except init,frame and frame_ai)

F9 Enter Step Mode

two dropdown->
1 code type(init frame frame_ai macro trigger)
2 code name(enables when code type macro or trigger)
Goto IP -> Switch currently viewed code to the code with the next instruction to execute(only if state wait)

Now `(T.L.<triggerName>)` , `(T.F.<triggerName>)` `(M.V.<sysMacroName>)` don't work properly
system variables empty and doesn't update during execution
there no correct macro name visibility check
triggers never invoked(non sound and they too)
not every command checked for their error report
predefined local variables access doesn't track
<details>
<summary>i know</summary>
My english is very well))
</details>