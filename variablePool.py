import collections
from tkinter.constants import S
import variableView

class Variable:
    def __init__(self,value,accessMode) -> None:
        self.__value=value
        self.__accessMode=accessMode
    @property
    def x(self):
        return self.__value
    @x.setter
    def x(self,value):
        if self.__accessMode:
            self.__value=value
    def update(self,value):
        self.__value=value
    @property
    def accessmode(self):
        return self.__accessMode


class VariablePool:
    def __init__(self):
        self.view=False
        self.__vars:dict[str,Variable]={}
        self.__changed:set[str]=set()
    def getsortedVars(self):
        return collections.OrderedDict(sorted(self.getchanged().items(), key=lambda kv: kv[0]))
    def getchanged(self,erase:bool=True):
        _={k:self.__vars[k].x for k in self.__changed}
        if erase:self.__changed=set()
        return _
    def __getitem__(self,key):
        return self.__vars[key].x
    def update(self,key,value):
        self.__vars[key].update(value)
        self.__changed.add(key)
    def __setitem__(self,key,value):
        '''print(value,isinstance(value,tuple),end=' ')
        if isinstance(value,tuple):
            print(len(value)>1,end=' ')
            if len(value)>1:
                print(isinstance(value[1],bool),end=' ')
        print()'''
        if isinstance(value,tuple) and len(value)>1 and isinstance(value[1],bool):
            self.__vars[key]=Variable(value[0],not value[1])
            self.__changed.add(key)
        else:
            self.update(key,value)
            return
            if self.__vars[key].accessmode:
                self.__vars[key].x=value
                self.__changed.add(key)
            else:
                import traceback
                traceback.print_stack()
                print(f'Access Denied name:{key}')               
                del traceback
    def attachView(self,view:'variableView.VariableView'):
        self.view=view
        view.attachVariables(self.getsortedVars())
    def updateView(self):
        if self.view:
            self.view.updateView(self.getchanged())
