from datParser import parse
from o3dModel import Model

class Models:
    def __init__(self) -> None:
        self.lods:dict[float,list[Model]]={}
    def loadModels(self,filename:str):
        with open(filename,'r') as file:
            tokens=parse(file)
            for i in tokens:
                if i.type==0:
                    print('unknown tag',i,'in',filename)
