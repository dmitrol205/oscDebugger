from math import inf, nan
from oscParser import parse
from datParser import parse as dparse
from oscCode import Code

class Program:
    def __init__(self,reducedIf:bool=True) -> None:
        self.macros:dict[str,Code]={}
        self.triggers:dict[str,Code]={}
        self.init=False
        self.frame=False
        self.frame_ai=False
        self.varnames=[]
        self.constants={}
        self.reducedif=reducedIf
        self.curves:dict[str,list[list[float,float]]]={}
    def loadScript(self,filename:str):
        with open(filename,'r') as file:
            tokens=parse(file)
            for i in tokens:
                if i.type<2:continue
                if i.type==3:
                    if self.init:
                        print('multiple init, redefinition from',filename)
                        #return False
                    self.init=Code(tokens,filename,self.reducedif)
                    continue
                if i.type==4:
                    if self.frame:
                        print('multiple frame, redefinition from',filename)
                        #return False
                    self.frame=Code(tokens,filename,self.reducedif)
                    continue
                if i.type==5:
                    if self.frame_ai:
                        print('multiple frame_ai, redefinition from',filename)
                        #return False
                    self.frame_ai=Code(tokens,filename,self.reducedif)
                    continue
                if i.type==80:
                    if i.string.lower() in self.macros:
                        print('multiple macro:'+i.string.lower()+', redefinition from',filename)
                        #return False
                    self.macros[i.string.lower()]=Code(tokens,filename,self.reducedif)
                    continue
                if i.type==81:
                    if i.string.lower() in self.triggers:
                        print('multiple trigger:'+i.string.lower()+', redefinition from',filename)
                        #return False
                    self.triggers[i.string.lower()]=Code(tokens,filename,self.reducedif)
                    continue
                print("script unknown token",i.type_name,i.string)
        return True
    def loadVarNames(self,filename:str):
        with open(filename,'r') as file:
            tokens=dparse(file)
            for i in tokens:
                if i.type==3:
                    if i.string.lower() not in self.varnames:
                        self.varnames.append(i.string.lower())
                    else:
                        pass
    def loadConstants(self,filename:str):
        with open(filename,'r') as file:
            tokens=dparse(file)
            curvename=False
            for i in tokens:
                if i.type<4:
                    continue
                if i.type==74:
                    curvename=False
                    i=next(tokens)
                    if i.type!=3:
                        print("error in tag const in",filename)
                        continue
                    _=i.string.lower()
                    i=next(tokens)
                    if i.type!=2:
                        print("error in tag const in",_,"in",filename)
                        continue
                    if _ not in self.constants:
                        self.constants[_]=i.value
                    else:
                        pass
                        #print('varnamelist['+filename+'] redeclare name',i.string)
                elif i.type==91:
                    i=next(tokens)
                    if i.type!=3:
                        print("expected [newcurve] name",i)
                        continue
                    curvename=i.string.lower()
                    self.curves[curvename]=[]
                elif i.type==92:
                    if not curvename:
                        print('tag [pnt] require previous [newcurve] definition')
                        continue
                    _=next(tokens)
                    if _.type!=2:
                        print('expected x of [pnt]',_)
                        continue
                    i=next(tokens)
                    if i.type!=2:
                        print('expected y of [pnt]',i)
                        continue
                    self.curves[curvename].append([_.value,i.value])
                else:
                    print('load constants unimplemented tag',i)
    def checkUndeclaredNames(self):
        for k,v in self.macros.items():
            v.checkForUndeclaredVarNames(self.varnames,k)
        for k,v in self.triggers.items():
            v.checkForUndeclaredVarNames(self.varnames,k)
        if self.init:
            self.init.checkForUndeclaredVarNames(self.varnames,'init')
        if self.frame:
            self.frame.checkForUndeclaredVarNames(self.varnames,'frame')
        if self.frame_ai:
            self.frame_ai.checkForUndeclaredVarNames(self.varnames,'frame_ai')
    def function(self,name:str,x:float):
        curve=self.curves[name]
        if curve==[]:
            raise Exception("empty curve",name)
        if curve[0][0]>x:
            return self.curves[name][0][1]
        for i in range(1,len(self.curves[name])):
            if x<curve[i][0]:
                if curve[i][1]==curve[i-1][1]:
                    return curve[i][1]
                else:
                    return ((x-curve[i-1][0])*curve[i][1]+(curve[i][0]-x)*curve[i-1][1])/(curve[i][1]-curve[i-1][1])
        return curve[len(curve)-1][1]
        