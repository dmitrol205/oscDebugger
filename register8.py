import loopStack8View

class Register8:
    def __init__(self) -> None:
        self.data=[float(0) for _ in range(8)]
    def __getitem__(self,indx:int)->float:
        return self.data[indx]
    def __setitem__(self,indx:int,value:float):
        self.data[indx]=value
        #self.updateView()
    def attachView(self,view:'loopStack8View.LoopStack8View'):
        self.view=view
        self.updateView()
    def updateView(self):
        if self.view:
            self.view.updateView(self)