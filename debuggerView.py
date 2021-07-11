import time
from oscExecutor import Executor
from bus import Bus
from codeView import CodeView
from tkinter import Event, Menu, Misc, Tk, filedialog as fd
from loopStack8View import LoopStack8View
import gc

class DebuggerView(Tk):
    def __init__(self,*args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.codeView=CodeView(self)
        self.stacks=[
            LoopStack8View(self,"Float Stack",'stack'),
            LoopStack8View(self,"String Stack",'stack'),
            LoopStack8View(self,"Registers",'register')
            ]
        self.codeView.grid(column=1,row=0,rowspan=4,sticky='nsew')
        self.stacks[0].grid(column=0,row=1,sticky='ew')
        self.stacks[1].grid(column=0,columnspan=2,row=4,sticky='ew')
        self.stacks[2].grid(column=0,row=2,sticky='ew')
        self.rowconfigure(0,weight=1)
        #self.rowconfigure(1,weight=1)
        #self.columnconfigure(0,pad=1)
        self.columnconfigure(1,weight=20)
        self.menu=Menu(self)
        self.configure(menu=self.menu)
        self.menufile=Menu(self.menu,tearoff=0)
        self.menu.add_cascade(label="File",menu=self.menufile)
        def openFile():
            filetypes = (
                ('omsi bus', '*.bus'),
                ('omsi vehicle','*.ovh'),
                ('omsi scene object','*.sco'),
            )

            filename = fd.askopenfilename(
                title='Open a file',
                initialdir=r'D:\Program Files (x86)\OMSI 2.2.027\Vehicles',
                filetypes=filetypes)
            if filename!="":
                self.loadBus(filename)
        self.menufile.add_command(label="Open...",command=openFile)
        self.menufile.add_separator()
        self.menufile.add_command(label="Exit",command=self.quit)
    def loadBus(self,name:str):
        self.bus=Bus(name)
        self.executor=Executor(self.bus.scripts)
        self.executor.attachCodeView(self.codeView)
        self.executor.float_stack.attachView(self.stacks[0])
        self.executor.string_stack.attachView(self.stacks[1])
        self.executor.register.attachView(self.stacks[2])
        self.executor.stepmode=True
        self.execution=self.executor.run()
        def stepin(_:'Event[Misc]'):
            try:
                _1=time.time()
                _=next(self.execution)
                _2=time.time()
            except StopIteration:
                return
            print(f"{(_2-_1):5.2f}",_)
        def stepover(_:'Event[Misc]'):
            _0=self.executor.ip.next
            if not _0:
                stepin(_)
                return
            self.executor.setBreakpoint(_0)
            self.executor.stepmode=False
            try:
                _1=time.time()
                _=next(self.execution)
                _2=time.time()
            except StopIteration:
                return
            self.executor.removeBreakpoint(_0)
            print(f"{(_2-_1):5.2f}",_)
        def stepout(_:'Event[Misc]'):
            if len(self.executor.ipstack)==0:
                stepin(_)
                return
            _0=self.executor.ipstack[-1][0]            
            self.executor.setBreakpoint(_0)
            self.executor.stepmode=False
            try:
                _1=time.time()
                _=next(self.execution)
                _2=time.time()
            except StopIteration:
                return
            self.executor.removeBreakpoint(_0)
            print(f"{(_2-_1):5.2f}",_)
        def resume(_:'Event[Misc]'):
            self.executor.stepmode=False
            try:
                _1=time.time()
                _=next(self.execution)
                _2=time.time()
            except StopIteration:
                return
            print(f"{(_2-_1):5.2f}",_)
        def bpsc(_:'Event[Misc]'):
            _1=self.codeView.index('insert linestart+2c')
            _2=self.codeView.index('end')
            if _1==_2:
                _1=self.codeView.index(f'{_1}-2l+2c')
            #self.codeView.mark_set('insert',_1)
            for i in self.executor.getCode(*self.codeView.currentCode):
                if i.position[0]==_1:
                    if self.executor.setBreakpoint(i,True):
                        self.codeView.setBreakpoint(i)
                    else:
                        self.codeView.removeBreakpoint(i)
            #self.codeView.
        self.bind('<KeyPress-F5>',resume)
        self.bind('<KeyPress-F6>',stepin)
        self.bind('<KeyPress-F7>',stepover)
        self.bind('<KeyPress-F8>',stepout)
        self.bind('<KeyPress-F2>',bpsc)
        stepin(None)
        gc.collect()
        