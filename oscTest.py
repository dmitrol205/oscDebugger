from debuggerView import DebuggerView
from loopStack8View import LoopStack8View
from oscInstruction import Instruction
import time
from tkinter import Event, Misc, Tk
from oscProgram import Program
from oscExecutor import Executor
from datParser import parse
from bus import Bus
from codeView import CodeView
import threading
import traceback

def main():
    g=Program()
    g.loadScript(r'D:\Program Files (x86)\OMSI 2.2.027\Vehicles\MAN Lions City Euro 6\Script\churakrueger\VMatrix.osc')
    #g.loadScript(r'D:\Program Files (x86)\OMSI 2.2.027\Vehicles\Trabant\script\Trabant_AI.osc')
    e=Executor(g)
    e.execute(next(iter(g.macros.items()))[1])
    '''print(g.macros)
    print(g.triggers)
    print(g.init)
    print(g.frame)
    print(g.ai_frame)
    '''
        
def main2():
    #g=Bus(r"D:\Program Files (x86)\OMSI 2.2.027\Vehicles\Trabant\Trabant.ovh")
    #g=Bus(r"D:\Program Files (x86)\OMSI 2.2.027\Vehicles\MAN Lions City Euro 6\A21_206.bus")
    #g=Bus(r"D:\Program Files (x86)\OMSI 2.2.027\Vehicles\MAN_NL_NG\MAN_GN92_main.bus")
    g=Bus(r"D:\Program Files (x86)\OMSI 2.2.027\Vehicles\MB_O305\O305_E2H_84.bus")
    #g=Bus(r"D:\Program Files (x86)\OMSI 2.2.027\Vehicles\VW_Golf_2\debug_golf.bus")
    root=Tk()
    j=CodeView(root,width=50,height=30)
    j.grid(column=1,row=0)
    #j.pack(fill="x",expand=True)
    sv=LoopStack8View(root,"Float Stack",width=10,height=10)
    #sv.pack(fill='x',expand=True)
    sv.grid(column=0,row=0)
    #j.loadCode(g.scripts.init)
    #print(j.get("1.0","1.end"))
    
    #root.mainloop()
    #return
    t=Executor(g.scripts)
    
    t.attachCodeView(j)
    e=t.run()
    t.stepmode=True
    '''t.stepmode=False
    for _ in e:
        print(_)
    return'''
    def kek():
        for i in e:
            print (i)
            input('[continue...]')
    keyfix=True
    def stepin(_:'Event[Misc]'):
        #nonlocal keyfix
        #if keyfix:
            #keyfix=False
            try:
                _1=time.time()
                _=next(e)
                _2=time.time()
            except StopIteration:
                return
            print(f"{(_2-_1):5.2f}",_)
    def stepover(_:'Event[Misc]'):
        _0=t.ip.next
        if not _0:
            stepin(_)
            return
        t.setBreakpoint(_0)
        t.stepmode=False
        try:
            _1=time.time()
            _=next(e)
            _2=time.time()
        except StopIteration:
            return
        t.removeBreakpoint(_0)
        print(f"{(_2-_1):5.2f}",_)
    def stepout(_:'Event[Misc]'):
        if len(t.ipstack)==0:
            stepin(_)
            return
        _0=t.ipstack[-1][0]            
        t.setBreakpoint(_0)
        t.stepmode=False
        try:
            _1=time.time()
            _=next(e)
            _2=time.time()
        except StopIteration:
            return
        t.removeBreakpoint(_0)
        print(f"{(_2-_1):5.2f}",_)
    def stepinUp(_:'Event[Misc]'):
        nonlocal keyfix
        keyfix=True
    root.bind('<KeyPress-F6>',stepin)
    root.bind('<KeyPress-F7>',stepover)
    root.bind('<KeyPress-F8>',stepout)
    #root.bind('<KeyRelease-F6>',stepinUp)
    #threading.Thread(None,kek).start()
    root.mainloop()
    return
    for i in g.scripts.macros.keys():
        print(i)
    return
    g.scripts.checkUndeclaredNames()
    return
    import collections
    g.scripts.constants = collections.OrderedDict(sorted(g.scripts.constants.items(), key=lambda kv: kv[0]))
    del collections
    for k,v in g.scripts.constants.items():
        print(k,v)
    '''g=g.script
    print(g.macros)
    print(g.triggers)
    print(g.init)
    print(g.frame)
    print(g.ai_frame)'''

def main3():
    g=Bus(r"D:\Program Files (x86)\OMSI 2.2.027\Vehicles\VW_Golf_2\debug_golf.bus")
    
    for i in g.scripts.init:
        i:Instruction
        print(i.reverse)

def main4():
    #g=Bus(r"D:\Program Files (x86)\OMSI 2.2.027\Vehicles\MB_O305\O305_E2H_84.bus")
    g=DebuggerView("Debugger")
    g.loadBus(r"D:\Program Files (x86)\OMSI 2.2.027\Vehicles\MB_O305\O305_E2H_84.bus")
    g.mainloop()
if __name__=='__main__':main4()