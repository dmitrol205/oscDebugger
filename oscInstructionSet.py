import math
from oscSystemMacros import SystemMacros
from oscInstruction import Instruction
from random import randint
import oscExecutor

class __InstructionSet(type):
    def __getitem__(cls,inst:Instruction):
        #print('get f'+str(inst.id),inst.reverse)
        if inst.id<100:
            return getattr(InstructionSet,'f'+str(inst.id))
        else:
            if inst.id<108:#load from register
                return getattr(InstructionSet,'f100')
            elif inst.id<116:#store to register
                return getattr(InstructionSet,'f101')

class InstructionSet(object,metaclass=__InstructionSet):
    def f2(self:"oscExecutor.Executor"):
        self.string_stack.push(self.ip.value)
        self.next()
    def f7(self:"oscExecutor.Executor"):
        if self.float_stack.peek()==float(0):
            self.ip=self.ip.ifelse
        else:
            self.next()
    ''''def f8(self:"oscExecutor.Executor"):
        self.next()
    def f9(self:"oscExecutor.Executor"):
        self.next()'''
    def f10(self:"oscExecutor.Executor"):
        if self.float_stack.pop()==float(0) or self.float_stack.pop()==float(0):
            self.float_stack.push(float(0))
        else:
            self.float_stack.push(float(1))
        self.next()
    def f11(self:"oscExecutor.Executor"):
        if self.float_stack.pop()==float(0) and self.float_stack.pop()==float(0):
            self.float_stack.push(float(0))
        else:
            self.float_stack.push(float(1))
        self.next()
    def f12(self:"oscExecutor.Executor"):
        if self.float_stack.pop()==float(0):
            self.float_stack.push(float(1))
        else:
            self.float_stack.push(float(0))
        self.next()
    def f13(self:"oscExecutor.Executor"):
        self.float_stack.push(self.float_stack.pop()+self.float_stack.pop())
        self.next()
    def f14(self:"oscExecutor.Executor"):
        _=self.float_stack.pop()
        self.float_stack.push(self.float_stack.pop()-_)
        self.next()
    def f15(self:"oscExecutor.Executor"):
        self.float_stack.push(self.float_stack.pop()*self.float_stack.pop())
        self.next()
    def f16(self:"oscExecutor.Executor"):
        _=self.float_stack.pop()
        if _==float(0):
            self.float_stack.pop()
            self.float_stack.push(float(0))    
        else:
            self.float_stack.push(self.float_stack.pop()/_)
        self.next()
    def f17(self:"oscExecutor.Executor"):
        _=self.float_stack.pop()
        if _==0.0:
            self.float_stack.pop()
            self.float_stack.push(float(0))    
        else:
            self.float_stack.push(self.float_stack.pop()%_)
        self.next()
    def f18(self:"oscExecutor.Executor"):
        self.float_stack.push(-self.float_stack.pop())
        self.next()
    def f19(self:"oscExecutor.Executor"):
        self.float_stack.push(float(1) if self.float_stack.pop()==self.float_stack.pop() else float(0))
        self.next()
    def f20(self:"oscExecutor.Executor"):
        self.float_stack.push(float(1) if self.float_stack.pop()<self.float_stack.pop() else float(0))
        self.next()
    def f21(self:"oscExecutor.Executor"):
        self.float_stack.push(float(1) if self.float_stack.pop()>self.float_stack.pop() else float(0))
        self.next()
    def f22(self:"oscExecutor.Executor"):
        self.float_stack.push(float(1) if self.float_stack.pop()<=self.float_stack.pop() else float(0))
        self.next()
    def f23(self:"oscExecutor.Executor"):
        self.float_stack.push(float(1) if self.float_stack.pop()>=self.float_stack.pop() else float(0))
        self.next()
    def f24(self:"oscExecutor.Executor"):
        self.float_stack.push(float(1) if self.string_stack.pop()==self.string_stack.pop() else float(0))
        self.next()
    def f25(self:"oscExecutor.Executor"):
        self.float_stack.push(float(1) if self.string_stack.pop()<self.string_stack.pop() else float(0))
        self.next()
    def f26(self:"oscExecutor.Executor"):
        self.float_stack.push(float(1) if self.string_stack.pop()>self.string_stack.pop() else float(0))
        self.next()
    def f27(self:"oscExecutor.Executor"):
        self.float_stack.push(float(1) if self.string_stack.pop()<=self.string_stack.pop() else float(0))
        self.next()
    def f28(self:"oscExecutor.Executor"):
        self.float_stack.push(float(1) if self.string_stack.pop()>=self.string_stack.pop() else float(0))
        self.next()
    def f29(self:"oscExecutor.Executor"):
        self.float_stack.push(math.sin(self.float_stack.pop()))
        self.next()
    def f30(self:"oscExecutor.Executor"):
        self.float_stack.push(math.asin(self.float_stack.pop()))
        self.next()
    def f31(self:"oscExecutor.Executor"):
        self.float_stack.push(math.atan(self.float_stack.pop()))
        self.next()
    def f32(self:"oscExecutor.Executor"):
        self.float_stack.push(min(self.float_stack.pop(),self.float_stack.pop()))
        self.next()
    def f33(self:"oscExecutor.Executor"):
        self.float_stack.push(max(self.float_stack.pop(),self.float_stack.pop()))
        self.next()
    def f34(self:"oscExecutor.Executor"):
        self.float_stack.push(math.exp(self.float_stack.pop()))
        self.next()
    def f35(self:"oscExecutor.Executor"):
        self.float_stack.push(math.sqrt(self.float_stack.pop()))
        self.next()
    def f36(self:"oscExecutor.Executor"):
        self.float_stack.push(self.float_stack.pop()**2)
        self.next()
    def f37(self:"oscExecutor.Executor"):
        _=self.float_stack.pop()
        _=1. if _>0 else float(-1) if _<0 else float(0)
        self.float_stack.push(_)
        self.next()
    def f38(self:"oscExecutor.Executor"):
        self.float_stack.push(math.pi)
        self.next()
    def f39(self:"oscExecutor.Executor"):
        _=int(self.float_stack.pop())-1
        _=float(0) if _<0 else float(randint(0,_))
        self.float_stack.push(_)
        self.next()
    def f40(self:"oscExecutor.Executor"):
        self.float_stack.push(math.fabs(self.float_stack.pop()))
        self.next()
    def f41(self:"oscExecutor.Executor"):
        self.float_stack.push(math.trunc(self.float_stack.pop()))
        self.next()
    def f42(self:"oscExecutor.Executor"):
        _=self.string_stack.pop()
        self.string_stack.push(self.string_stack.pop()+_)
        self.next()
    def f43(self:"oscExecutor.Executor"):
        _=self.string_stack.pop()
        _1=self.float_stack.pop()
        _2=_
        while len(_2)<_1:
            _2+=_
        self.string_stack.push(_2[:_1])
        self.next()
    def f44(self:"oscExecutor.Executor"):
        self.float_stack.push(len(self.string_stack.peek()))
        self.next()
    def f45(self:"oscExecutor.Executor"):
        self.string_stack.push(self.string_stack.pop()[int(self.float_stack.pop()):])
        self.next()
    def f46(self:"oscExecutor.Executor"):
        self.string_stack.push(self.string_stack.pop()[:-int(self.float_stack.pop())])
        self.next()
    def f47(self:"oscExecutor.Executor"):
        _=int(self.float_stack.peek())
        _1=self.string_stack.pop()
        if len(_1)>_:
            _1=_1[-_:]
        else:
            _2="{:>"+str(_)+"s}"
            _1=f"{_1:>{_}s}"
        self.string_stack.push(_1)
        self.next()
    def f48(self:"oscExecutor.Executor"):
        _=int(self.float_stack.peek())
        _1=self.string_stack.pop()
        if len(_1)>_:
            _2=(len(_1)-_)/2
            _1=_1[math.floor(_2):-math.ceil(_2)]
        else:
            _1=f"{_1:^{_}s}"
        self.string_stack.push(_1)
        self.next()
    def f49(self:"oscExecutor.Executor"):
        _=int(self.float_stack.peek())
        _1=self.string_stack.pop()
        if len(_1)>_:
            _1=_1[:_]
        else:
            _1=f"{_1:<{_}s}"
        self.string_stack.push(_1)
        self.next()
    def f50(self:"oscExecutor.Executor"):
        self.string_stack.push(str(int(self.float_stack.pop())))
        self.next()
    def f51(self:"oscExecutor.Executor"):
        _=self.string_stack.pop()
        _1=str(int(self.float_stack.pop()))
        try:
            _2=int(_[1:])
        except ValueError:
            self.string_stack.push(_)
            self.next()
            return
        if len(_1)>_2:
            _1=f"{_1[:_2-1]}#"
        else:
            _1=f"{_1:{_[0]}>{_2}}"
        self.string_stack.push(_1)
        self.next()
    def f52(self:"oscExecutor.Executor"):
        try:
            _=float(self.string_stack.pop())
        except ValueError:
            _=float(-1)
        self.float_stack.push(_)
        self.next()
    def f53(self:"oscExecutor.Executor"):        
        self.string_stack.push(self.string_stack.pop().strip())
        self.next()
    def f54(self:"oscExecutor.Executor"):
        self.float_stack.push(self.float_stack.peek())
        self.next()
    def f55(self:"oscExecutor.Executor"):
        self.string_stack.push(self.string_stack.peek())
        self.next()
    def f56(self:"oscExecutor.Executor"):
        self.debugOutput(self.string_stack.peek(),'$msg')
        self.next()
    def f57(self:"oscExecutor.Executor"):
        self.debugOutput("Information: Stack Dump")
        self.debugOutput("")
        for i in range(8):
            self.debugOutput(f"Stack Nr.{i}: {self.float_stack[i]:f}")
        self.next()
    def f88(self:"oscExecutor.Executor"):
        try:
            self.program.macros[self.ip.value]
        except KeyError:
            print('no such macro',self.ip.value)
            self.error={'ip':self.ip,'calls':self.ipstack}
            self.isalive=False
            self.ipstack=[]
            self.ip=False
            return
        self.ipstack.append([self.ip.next,self.codeType,self.codeName])
        for _ in self.execute('macro',self.ip.value):
            _:'Instruction'
            yield _
        try:
            self.ip,self.codeType,self.codeName=self.ipstack.pop()
        except IndexError:
            self.ip=False
            return
        #self.updateViews()
    def f89(self:"oscExecutor.Executor"):#todo
        #call sys macro
        SystemMacros[self.ip](self)
        self.next()
        #################################
    def f90(self:"oscExecutor.Executor"):
        self.float_stack.push(self.system_variables[self.ip.value])
        self.next()
    def f91(self:"oscExecutor.Executor"):
        self.float_stack.push(self.float_local[self.ip.value])
        self.next()
    def f92(self:"oscExecutor.Executor"):
        self.string_stack.push(self.string_local[self.ip.value])
        self.next()
    def f93(self:"oscExecutor.Executor"):
        self.float_local[self.ip.value]=self.float_stack.peek()
        self.next()
    def f94(self:"oscExecutor.Executor"):
        self.string_local[self.ip.value]=self.string_stack.peek()
        self.next()
    def f95(self:"oscExecutor.Executor"):
        self.float_stack.push(self.float_constants[self.ip.value])
        self.next()
    def f96(self:"oscExecutor.Executor"):
        self.float_stack.push(self.program.function(self.ip.value,self.float_stack.pop()))
        self.next()
    def f97(self:"oscExecutor.Executor"):#todo#load and play sound
        #self.float_stack.push(self.program.function(self.ip.value,self.float_stack.pop()))
        _=self.string_stack.pop()
        self.next()
    def f98(self:"oscExecutor.Executor"):#todo#play sound
        #self.float_stack.push(self.program.function(self.ip.value,self.float_stack.pop()))
        
        self.next()
    def f99(self:"oscExecutor.Executor"):
        self.float_stack.push(self.ip.value)
        self.next()
    def f100(self:"oscExecutor.Executor"):
        self.float_stack.push(self.register[self.ip.id-100])
        self.next()
    def f101(self:"oscExecutor.Executor"):
        self.register[self.ip.id-108]=self.float_stack.peek()
        self.next()
