import os
import threading
from variableView import VariableView
from codePicker import CodePicker
import time
from oscExecutor import Executor
from bus import Bus
from codeView import CodeView
from tkinter import Event, Menu, Misc, Text, Tk, filedialog as fd, ttk
from loopStack8View import LoopStack8View
import gc

class DebuggerView(Tk):
    def __init__(self,*args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.filename=r'D:\Program Files (x86)\OMSI 2.2.027\Vehicles\None'
        self.thread=threading.Thread()
        self.thread.start()
        #
        self.codeView=CodeView(self)
        self.stringValuesView=ttk.Notebook(self)
        self.stringLocalView=VariableView(True,self.stringValuesView)
        self.stacks=[
            LoopStack8View(self,"Float Stack",'stack'),
            LoopStack8View(self.stringValuesView,"String Stack",'stack'),
            LoopStack8View(self,"Registers",'register')
            ]
        self.codePicker=CodePicker(self)
        self.menu=Menu(self)
        self.menufile=Menu(self.menu,tearoff=0)
        self.floatValuesView=ttk.Notebook(self)
        self.floatLocalView=VariableView(False,self.floatValuesView)
        self.floatSystemView=VariableView(False,self.floatValuesView)
        self.floatConstantView=VariableView(False,self.floatValuesView)
        #
        self.configure(menu=self.menu)
        self.menu.add_cascade(label="File",menu=self.menufile)        
        def openFile():
            filetypes = (
                ('omsi bus/vehicle/scene object','*.bus;*.ovh;*.sco'),
                ('omsi bus', '*.bus'),
                ('omsi vehicle','*.ovh'),
                ('omsi scene object','*.sco'),
            )

            filename = fd.askopenfilename(
                title='Open a file',
                initialdir=os.path.split(self.filename)[0],
                filetypes=filetypes)
            if filename!="":
                self.filename=filename
                self.loadBus(filename)
        self.menufile.add_command(label="Open...",command=openFile)
        self.menufile.add_separator()
        self.menufile.add_command(label="Exit",command=self.quit)
        self.floatValuesView.add(self.floatLocalView,text="Local Floats")
        self.floatValuesView.add(self.floatSystemView,text="System Floats")
        self.floatValuesView.add(self.floatConstantView,text="Constant Floats")
        self.stringValuesView.add(self.stacks[1],text="String Stack",sticky='nsew')
        '''def upd(_):
            self.stringLocalView.onFrameConfigure(None)
        self.stringValuesView.bind('<Button-1>',upd)'''
        #self.stringLocalView.canvas.configure(scrollregion=self.stacks[1].bbox('all'))
        self.stringValuesView.add(self.stringLocalView,text="Local Strings",sticky='ew')
        #
        self.codeView.attachCodePicker(self.codePicker)
        #
        self.stringValuesView.grid(column=0,columnspan=2,row=4,sticky='ew')
        self.floatValuesView.grid(column=2,row=0,rowspan=5,sticky='nsew')
        self.codeView.grid(column=1,row=0,rowspan=4,sticky='nsew')
        self.stacks[0].grid(column=0,row=1,sticky='ew')
        self.stacks[2].grid(column=0,row=2,sticky='ew')
        self.codePicker.grid(row=0,column=0,sticky='ew')
        #
        self.rowconfigure(0,weight=1)
        self.columnconfigure(1,weight=20)
        #self.rowconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        #self.rowconfigure(4,weight=1)
        #self.columnconfigure(0,weight=1)
    def loadBus(self,name:str):
        self.bus=Bus(name)
        self.executor=Executor(self.bus.scripts)
        self.executor.attachCodeView(self.codeView)
        self.executor.float_stack.attachView(self.stacks[0])
        self.executor.string_stack.attachView(self.stacks[1])
        self.executor.register.attachView(self.stacks[2])
        self.executor.string_local.attachView(self.stringLocalView)
        self.executor.float_local.attachView(self.floatLocalView)
        self.executor.system_variables.attachView(self.floatSystemView)
        self.executor.float_constants.attachView(self.floatConstantView)
        self.codePicker.loadCodes(self.bus.scripts)
        self.codePicker.attachExecutor(self.executor)
        #
        self.executor.stepmode=True
        self.execution=self.executor.run()
        def stepin(_:'Event[Misc]'):
            if self.thread.is_alive():
                return
            try:
                _1=time.perf_counter()
                _=next(self.execution)
                _2=time.perf_counter()
            except StopIteration:
                return
            print(f"{(_2-_1):f}",_)
        def stepover(_:'Event[Misc]'):
            if self.thread.is_alive():
                return
            if self.executor.ip.id==7:
                _0=self.executor.ip.ifend
                while _0 and _0.id==9:
                    _0=_0.next
                #if not _0:#maybe cycleref
                    #stepout(_)
            else:
                _0=self.executor.ip.next
            if not _0:
                stepin(_)
                return
            self.executor.setBreakpoint(_0)
            self.executor.stepmode=False
            try:
                _1=time.perf_counter()
                _=next(self.execution)
                _2=time.perf_counter()
            except StopIteration:
                return
            self.executor.removeBreakpoint(_0)
            print(f"{(_2-_1):f}",_)
        def stepout(_:'Event[Misc]'):
            if self.thread.is_alive():
                return
            if len(self.executor.ipstack)!=0 and not self.executor.ipstack[-1][0]:
                stepover(_)
                return
            if len(self.executor.ipstack)==0:
                if self.executor.codeType=='init':
                    try:
                        if self.executor.aimode:
                            _0=self.executor.program.frame_ai.entryPoint
                        else:
                            _0=self.executor.program.frame.entryPoint
                    except AttributeError:
                        stepover(_)
                        return
                else:
                    _0=self.executor.getCode().entryPoint
            else:
                _0=self.executor.ipstack[-1][0]
            self.executor.setBreakpoint(_0)
            self.executor.stepmode=False
            try:
                _1=time.perf_counter()
                _=next(self.execution)
                _2=time.perf_counter()
            except StopIteration:
                return
            self.executor.removeBreakpoint(_0)
            print(f"{(_2-_1):f}",_)
        def resume(_:'Event[Misc]'):
            if self.thread.is_alive():
                return
            self.executor.stepmode=False
            def remote():
                try:
                    _1=time.perf_counter()
                    _=next(self.execution)
                    _2=time.perf_counter()
                except StopIteration:
                    return
                print(f"{(_2-_1):8f}",_)
            g=threading.Thread(target=remote)
            g.setDaemon(True)
            g.start()
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
        def pause(_:'Event[Misc]'):
            self.executor.stepmode=True
        self.bind('<KeyPress-F5>',resume)
        self.bind('<KeyPress-F6>',stepin)
        self.bind('<KeyPress-F7>',stepover)
        self.bind('<KeyPress-F8>',stepout)
        self.bind('<KeyPress-F9>',pause)
        self.bind('<KeyPress-F2>',bpsc)
        self.codeView.currentCode=['','']
        stepin(None)
        gc.collect()
        