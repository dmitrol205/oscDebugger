import oscExecutor
from oscInstruction import Instruction

class __SystemMacros(type):
    def __getitem__(cls,inst:Instruction):
        try:      
            return getattr(SystemMacros,inst.value)
        except AttributeError:
            print('unimplemented sys macros',inst.value)
            return getattr(SystemMacros,'_error_stub_')

class SystemMacros(object,metaclass=__SystemMacros):
    def _error_stub_(self:"oscExecutor.Executor"):
        #todo when code is loading and there an undefined sys macro 
        #-> make record in log file
        self.float_stack.pop()
        self.float_stack.push(float(-1))
    def getrouteindex(self:"oscExecutor.Executor"):
        self.float_stack.pop()
        #todo if route code exists return route index else -1
        self.float_stack.push(float(-1))
    def nrspecrandom(self:"oscExecutor.Executor"):
        _=self.float_stack.pop()
        #todo random number from vehicle number and seed
        self.float_stack.push(_)
    def getheightabovepoint(self:"oscExecutor.Executor"):
        self.float_stack.pop()#z
        self.float_stack.pop()#y
        self.float_stack.pop()#x
        #todo (x,y,z)->height
        self.float_stack.push(float(0))
    def getfontindex(self:"oscExecutor.Executor"):
        self.string_stack.pop()
        #todo get font index by name
        self.float_stack.push(float(1))
    def getterminusindex(self:"oscExecutor.Executor"):
        self.float_stack.pop()
        #todo teminus code(zero-based)->terminus index(zero-based)
        self.float_stack.push(float(0))
    def getterminusstring(self:"oscExecutor.Executor"):
        self.float_stack.pop()
        self.float_stack.pop()
        #todo (teminus index(zero-based),string index(zero-based))->terminus string et (last bus stop index,line index)->line
        self.string_stack.push('Terminus Line')
    def getterminuscode(self:"oscExecutor.Executor"):
        self.float_stack.pop()
        #todo terminus index(zero-based)->teminus code(zero-based)
        self.float_stack.push(float(0))
    