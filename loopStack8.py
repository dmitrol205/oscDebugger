import loopStack8View


class LoopStack8:
    def __init__(self,isstr:bool=False) -> None:
        self.stack=['' if isstr else float(0) for _ in range(8)]
        self.pointer=7
        self.view=False
    def push(self,value:'str|float'):
        self.pointer+=9
        self.pointer%=8
        self.stack[self.pointer]=value
        #self.updateView()
    def peek(self)->'str|float':
        return self.stack[self.pointer]
    def pop(self)->'str|float':
        _=self.stack[self.pointer]
        self.stack[self.pointer]=float(0) if type(_).__name__=='float' else ''
        self.pointer+=7
        self.pointer%=8
        #self.updateView()
        return _
    def __getitem__(self,index:int):
        return self.stack[(self.pointer-index+8)%8]
    def attachView(self,view:'loopStack8View.LoopStack8View'):
        self.view=view
        self.updateView()
    def updateView(self):
        if self.view:
            self.view.updateView(self)