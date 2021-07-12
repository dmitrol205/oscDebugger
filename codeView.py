import codePicker
import tkinter as tk
from tkinter import font as tkFont
from tkinter.constants import INSERT
from oscCode import Code
from oscInstruction import Instruction
from idlelib.redirector import WidgetRedirector


class CodeView(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_font = tkFont.nametofont(self.cget("font"))

        em = self.default_font.measure("m")
        #print(self.default_font.)
        #default_size = default_font.cget("size")
        bold_font = tkFont.Font(**self.default_font.configure())
        bold_font.configure(weight="bold")
        self.tag_configure("cip", font=bold_font,foreground=self.cget('background'),background=self.cget('foreground'))
        self.tag_configure("then", foreground='black',background='blue')
        self.tag_configure("else", foreground='black',background='red')
        self.tag_configure("endif", foreground='black',background='yellow')

        lmargin2 = em + self.default_font.measure("\u2022 ")
        self.tag_configure("breakpoint", lmargin1=em, lmargin2=lmargin2)

        #self.loadedCodes={}
        self.currentCode=["",""]
        self.redirector=WidgetRedirector(self)
        self.write=self.redirector.register('insert',lambda *args,**kwargs:"break")
        self.remove=self.redirector.register('delete',lambda *args,**kwargs:"break")
    def insert_bullet(self,index:'str|int'):
        self.write(index, f"\u2022 ", "bullet")
    def remove_tags(self,tag:str):
        _=self.tag_ranges(tag)
        if len(_)>0:
            for i in range(int(len(_)/2)):
                self.tag_remove(tag,_[i*2].string,_[i*2+1].string)
    def selectInstruction(self,inst:'Instruction'):
        self.remove_tags('cip')
        self.remove_tags('then')
        self.remove_tags('else')
        self.remove_tags('endif')
        self.tag_add('cip',inst.position[0],inst.position[1])
        #preview code
        self.see(f"{inst.position[0]}+10l")
        self.see(inst.position[0])
    def selectIf(self,inst:'Instruction'):
        self.selectInstruction(inst)
        self.tag_add('then',inst.next.position[0],inst.next.position[1])
        if inst.ifelse!=inst.ifend:
            self.tag_add('else',inst.ifelse.position[0],inst.ifelse.position[1])
        if inst.ifend:
            self.tag_add('endif',inst.ifend.position[0],inst.ifend.position[1])
    def isCurrentCode(self,ct:str='init',cn:str=''):
        return ct==self.currentCode[0] and cn==self.currentCode[1]
    def loadCode(self,code:'Code',breakpoints:'list[Instruction]'=[],ct:str='init',cn:str=''):
        #self.lineEnd=[]
        #posupdate=True
        '''if self.currentCode[0]==ct and self.currentCode[1]==cn:
            return
        self.currentCode=[ct,cn]'''
        self.currentCode=[ct,cn]
        if self.codePicker:
            self.codePicker.setCode(*self.currentCode)
        #self.winfo_toplevel().title(f"{ct} {cn}")
        self.remove("1.0","end")
        '''if ct in self.loadedCodes:
            if cn in self.loadedCodes[ct]:
                posupdate=False'''
        for i in code:
            #if posupdate:
            if i in breakpoints:
                self.insert_bullet("end")
            else:
                self.write("end","  ")
            i.position[0]=self.index("end-1c")
            self.write("end",f"{i.reverse}")
            i.position[1]=self.index(f"end-1c")        
            self.write("end","\n")
                #self.lineEnd.append()
    def setBreakpoint(self,inst:Instruction):
        _=self.index(f'{inst.position[0]} linestart')
        self.remove(_,self.index(f'{_}+2c'))
        self.insert_bullet(_)
    def removeBreakpoint(self,inst:Instruction):
        _=self.index(f'{inst.position[0]} linestart')
        self.remove(_,self.index(f'{_}+2c'))
        self.write(_,"  ")
    def attachCodePicker(self,cp:'codePicker.CodePicker'):
        self.codePicker=cp