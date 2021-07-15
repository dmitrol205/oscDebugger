import collections
from tkinter import Canvas, Entry, Frame, Label, Scrollbar
import tkinter

class VariableView(Frame):
    def __init__(self,exp,*args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.exp=exp
        self.canvas = Canvas(self, borderwidth=0, background=self.cget('background'),
        highlightthickness=0
        )
        self.frame = Frame(self.canvas, background=self.cget('background'))
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.pack(side="left", fill="both")
        self.vsb.pack(side="right", fill="y")
        self.canvas.create_window((0,0), window=self.frame, anchor="center",tags="self.frame")
        
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.onFrameConfigure(None)
        def mw(_):#free mouse scroll don't work
            _1=self.vsb.get()
            _2=(_1[1]-_1[0])/3
            _2*=1 if _.delta<0 else -1
            self.canvas.yview_moveto(self.vsb.get()[0]+_2)
        def ebsc(_):
            self.canvas.bind_all("<MouseWheel>", mw)
        def lusc(_):
            self.canvas.unbind_all('<MouseWheel>')
        self.bind('<Enter>',ebsc)
        self.bind('<Leave>',lusc)
        if self.exp:
            self.canvas.config(height=170)
        else:
            self.canvas.config(width=100)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        if self.exp:
            self.canvas.configure(width=self.frame.winfo_width())
        else:
            self.canvas.configure(width=self.frame.winfo_reqwidth())
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def attachVariables(self,vars:'dict[str,float|str]'):
        self.elements:dict[str,Entry]={}
        counter=0
        for k,v in vars.items():
            Label(self.frame,text=k).grid(row=counter,column=0,sticky='w')
            _1=Entry(self.frame)
            _1.insert("end",repr(v))
            _1.grid(row=counter,column=1,sticky='ew')
            self.elements[k]=_1
            counter+=1
        self.frame.columnconfigure(1,weight=1)
        #
        if self.exp:
            self.canvas.itemconfigure('self.frame',width=self.frame.grid_bbox(0,self.frame.grid_size()[1],0,0)[2]+700)
        else:
            self.frame.update()
            self.canvas.itemconfigure('self.frame',width=self.frame.grid_bbox(0,self.frame.grid_size()[1],0,0)[2]+100)
        self.frame.event_generate('<Configure>')
    def updateView(self,vars:dict):
        for k,v in vars.items():
            _1=self.elements[k]
            _1.delete('0','end')
            _1.insert('end',repr(v))
        self.canvas.update()