from busModels import Models
import os
from typing import Generator
from datParser import parse
from oscProgram import Program
from datToken import Token
class Bus(object):
    tags={
        10:'_script',
        9:'_varnamelist',
        7:'_model',
        39:'_couple_back',
        11:'_constfile',
    }
    def __getitem__(self,token:Token):
        return getattr(self,Bus.tags[token.type])
    def _couple_back(self,tokens:Generator[Token,None,None]):
        print('\nheh\n')
        i=next(tokens)
        if i.type!=3:
            print("expected path to script",str(i))
            return
        self.back=Bus(self.path+os.path.sep+i.string,self.scripts)
        i=next(tokens)
        if i.type!=3:
            print("expected false or true",str(i))
            self.bback=False
            return 
        self.bback=bool(i.string)
    def _model(self,tokens:Generator[Token,None,None]):
        i=next(tokens)
        if i.type!=3:
            print("expected path to script",str(i))
            return
        self.models.loadModels(self.path+os.path.sep+i.string)
    def _script(self,tokens:Generator[Token,None,None]):
        i=next(tokens)
        if i.type!=2:
            print("wrong script amount",str(i))
            return 
        for _ in range(int(i.value)):
            i=next(tokens)
            if i.type!=3:
                print("expected path to script",str(i))
                return
            self.scripts.loadScript(self.path+os.path.sep+i.string)
    def _varnamelist(self,tokens:Generator[Token,None,None]):
        i=next(tokens)
        if i.type!=2:
            print("wrong varnamelist amount",str(i))
            return 
        for _ in range(int(i.value)):
            i=next(tokens)
            if i.type!=3:
                print("expected path to varnamelist",str(i))
                return
            self.scripts.loadVarNames(self.path+os.path.sep+i.string)
    def _constfile(self,tokens:Generator[Token,None,None]):
        i=next(tokens)
        if i.type!=2:
            print("wrong constfile amount",str(i))
            return 
        for _ in range(int(i.value)):
            i=next(tokens)
            if i.type!=3:
                print("expected path to constfile",str(i))
                return
            self.scripts.loadConstants(self.path+os.path.sep+i.string)
    def __init__(self,filename:str,sharedscripts:Program=False) -> None:
        print('loading',filename)
        self.path,self.filename=os.path.split(filename)
        with open(filename,'r') as file:
            tokens=parse(file)
            if not sharedscripts:
                self.scripts=Program(False)
            else: 
                self.scripts=sharedscripts
            self.models=Models()
            self.back:'Bus'=False
            for i in tokens:
                if i.type==0:
                    print('unknown tag',i,'in',filename)
                try:
                    self[i](tokens)
                except KeyError:
                    pass
                    
                
        pass