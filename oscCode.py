from oscToken import Token
from typing import Generator
from oscInstruction import Instruction

class Code():
    @staticmethod
    def __iter(entryPoint:Instruction,endPoint:Instruction):
        while entryPoint and entryPoint.next!=endPoint:
            if entryPoint.id==7:
                yield entryPoint
                if entryPoint.ifelse!=entryPoint.ifend:
                    yield from Code.__iter(entryPoint.next,entryPoint.ifend)
                    yield from Code.__iter(entryPoint.ifelse,entryPoint.ifend)
                else:
                    yield from Code.__iter(entryPoint.next,entryPoint.ifend)
                entryPoint=entryPoint.ifend
            else:
                yield entryPoint
                entryPoint=entryPoint.next
        if entryPoint:
            yield entryPoint
    def __iter__(self):
        for i in Code.__iter(getattr(self,'entryPoint'),False):
            yield i
    #def __next__(self):
        
        raise StopIteration
    def checkForUndeclaredVarNames(self,varnames:'list[str]',methodName:str):
        from oscExecutor import Executor
        for i in self.getUndeclaredVarNames(varnames):
            if i not in Executor.roadvehicle_varlist:
                print('Undeclared varname',i,'in',methodName,'in:',self.filename)
                #if i not in constnames:
                #    print('Undeclared varname',i,'in',methodName,'in:',self.filename)
                #else:
                    #print('defined like a constant',i)
        del Executor
    def getUndeclaredVarNames(self,varnames:'list[str]'):
        for i in self:
            #i:Instruction
            if i.id==91 or i.id==93:
                if i.value not in varnames:
                    yield i.value
    @staticmethod
    def __remove_else_endif_instructions__(entryPoint:Instruction,endPoint:Instruction=False):
        while entryPoint and entryPoint.next!=endPoint:
            if entryPoint.id==7:
                #print(entryPoint.__repr__())
                '''if entryPoint.next.id in [8,9]:
                    entryPoint.next=entryPoint.ifend.next
                    entryPoint.ifelse=entryPoint.ifelse.next
                    entryPoint.ifend=entryPoint.ifend.next'''
                #shitty bug pass begin
                if not entryPoint.ifelse or not entryPoint.ifend:
                    entryPoint=entryPoint.ifend
                    continue
                if entryPoint.ifelse.id not in [8,9] or entryPoint.ifend.id!=9:
                    entryPoint=entryPoint.ifend
                    continue
                #shitty bug pass end
                if entryPoint.ifelse!=entryPoint.ifend:
                    _0=Code.__hasnext(entryPoint.next,entryPoint.ifelse)
                    if _0:
                        _0.next=entryPoint.ifend.next
                    else:
                        raise Exception("check __remove_else_endif_instructions then(with else)")
                    _1=Code.__hasnext(entryPoint.ifelse.next,entryPoint.ifend)
                    if _1:
                        _1.next=entryPoint.ifend.next
                    else:
                        raise Exception("check __remove_else_endif_instructions else")
                    entryPoint.ifelse=entryPoint.ifelse.next
                    entryPoint.ifend=entryPoint.ifend.next
                    Code.__remove_else_endif_instructions__(entryPoint.next,_0.next)
                    Code.__remove_else_endif_instructions__(entryPoint.ifelse.next,_1.next)
                else:
                    _0=Code.__hasnext(entryPoint.next,entryPoint.ifend)
                    if _0:
                        _0.next=entryPoint.ifend.next
                    else:
                        raise Exception("check __remove_else_endif_instructions then(without else)")
                    entryPoint.ifelse=entryPoint.ifelse.next
                    entryPoint.ifend=entryPoint.ifend.next
                    Code.__remove_else_endif_instructions__(entryPoint.next,_0.next)
                entryPoint=entryPoint.ifend
            else:
                entryPoint=entryPoint.next
    @staticmethod
    def __hasnext(entryPoint:Instruction,endPoint:Instruction=False):
        while entryPoint and entryPoint.next!=endPoint:
            entryPoint=entryPoint.next
        if entryPoint:
            return entryPoint
        else:
            return False
    @staticmethod
    def __fix_if(entryPoint:Instruction,endPoint:Instruction=False):
        while entryPoint and entryPoint.next!=endPoint:
            if entryPoint.id==7:
                if entryPoint.ifelse!=entryPoint.ifend:
                    _0=Code.__hasnext(entryPoint.next,entryPoint.ifelse)
                    if _0:
                        _0.next=entryPoint.ifend
                    else:
                        raise Exception("check __fix if")
                    Code.__fix_if(entryPoint.ifelse.next,entryPoint.ifend)
                Code.__fix_if(entryPoint.next,entryPoint.ifend)
                entryPoint=entryPoint.ifend
            else:
                entryPoint=entryPoint.next
    def __init__(self,code:Generator[Token,None,None],filename:str="?",hideElseAndEnd:bool=True) -> None:
        self.filename=filename
        #if token.type not in[3,4,5,80,81]:raise Exception("wrong token")   
        ifstack:list[Instruction]=[]
        current=False
        self.entryPoint=False
        for i in code:
            if i.type<2:continue
            if i.type==6:break
            if not current:
                self.entryPoint=Instruction(i,ifstack)
                current=self.entryPoint
                current.next=False
                continue
            current.next=Instruction(i,ifstack)
            current=current.next
        if current:
            current.next=False
            if hideElseAndEnd:
                Code.__remove_else_endif_instructions__(self.entryPoint)
            else:
                Code.__fix_if(self.entryPoint)
