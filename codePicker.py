import oscExecutor
from tkinter import Button, Event, Frame
from tkinter.ttk import Combobox

from idlelib.redirector import WidgetRedirector
from oscProgram import Program

class CodePicker(Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.codeType=Combobox(self,state='disabled')
        self.codeName=Combobox(self,state='disabled')
        self.codeType.grid(row=0,column=0,sticky='ew')
        self.codeName.grid(row=1,column=0,sticky='ew')
        self.columnconfigure(0,weight=1)
        def ctlistener(_):           
            _=self.codeType.get()
            if _=='init' or _=='frame' or _=='frame_ai':
                self.codeName.config(values=[],state='disabled')
                if self.codeType.get()==self.executor.codeView.currentCode[0]: 
                    return
                self.executor.codeView.loadCode(self.executor.getCode(_),self.executor.breakpoints,_,'')
            elif _=='macro':
                self.codeName.set("")
                if len(self.program.macros)==0:
                    self.codeName.config(values=[],state='disabled')
                else:
                    self.codeName.config(values=list(self.program.macros.keys()),state='normal')
            elif _=='trigger':
                self.codeName.set("")
                if len(self.program.triggers)==0:
                    self.codeName.config(values=[],state='disabled')
                else:
                    self.codeName.config(values=list(self.program.triggers.keys()),state='normal')
        def cnlistener(_):
            if self.codeName.get()==self.executor.codeView.currentCode[1]:
                return
            _2=self.codeName.get()
            _1=self.codeType.get()
            self.executor.codeView.loadCode(self.executor.getCode(_1,_2),self.executor.breakpoints,_1,_2)
        def dropdown(_:'Event[Combobox]'):
            _.widget.focus()
            _.widget.event_generate('<Down>')
        self.codeType.bind('<<ComboboxSelected>>',ctlistener)
        self.codeType.bind('<Button-1>',dropdown)
        self.codeName.bind('<Button-1>',dropdown)
        self.codeName.bind('<<ComboboxSelected>>',cnlistener)
        self.ctrd=WidgetRedirector(self.codeType)
        self.ctrd.register('insert',lambda *args,**kwargs:"break")
        self.ctrd.register('delete',lambda *args,**kwargs:"break")
        self.cnrd=WidgetRedirector(self.codeName)
        self.cnrd.register('insert',lambda *args,**kwargs:"break")
        self.cnrd.register('delete',lambda *args,**kwargs:"break")
        def cip():
            if hasattr(self,'executor'):
                self.executor.updateViews()
        self.button=Button(self,text="Goto IP",command=cip)
        self.button.grid(row=2,column=0,sticky="ew")
    def attachExecutor(self,e:'oscExecutor.Executor'):
        self.executor=e

    def loadCodes(self,program:Program):
        self.program=program
        self.codeType.config(state='normal')
        
        ct=[]
        if self.program.init:
            ct.append('init')
        if self.program.frame:
            ct.append('frame')
        if self.program.frame_ai:
            ct.append('frame_ai')
        ct.append('macro')
        ct.append('trigger')
        self.codeType['values']=ct
    def setCode(self,ct:str,cn:str):
        self.codeType.set(ct)
        self.codeType.event_generate('<<ComboboxSelected>>')
        self.codeName.set(cn)
        self.codeName.event_generate('<<ComboboxSelected>>')
        #print(self.codeType.getvar('value'))
        #print()
        pass
