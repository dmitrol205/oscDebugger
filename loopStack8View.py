from tkinter import Entry, Frame, Label
class LoopStack8View(Frame):
    def __init__(self,*args,**kwargs) -> None:
        '''__init__(self,name,itemname,args,kwargs)'''        
        super(LoopStack8View,self).__init__(*args[3:],**kwargs)
        Label(self,text=args[1]).grid(column=0,columnspan=2,row=0)
        self.labels=[Label(self,text=f"{args[2]} {i}: ") for i in range(8)]
        for i in range(8):
            self.labels[i].grid(column=0,row=i+1,sticky='w')
        self.values=[Entry(self) for _ in range(8)]
        for i in range(8):
            self.values[i].insert('end',str(float(0)))
            self.values[i].grid(column=1,row=i+1,sticky='ew')
        self.columnconfigure(0,weight=0)
        self.columnconfigure(1,weight=1)
    def updateView(self,data):
        vpointer=0
        for i in self.values:
            i.delete('0','end')
            i.insert('end',str(data[vpointer]))
            vpointer+=1