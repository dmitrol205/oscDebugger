from oscToken import Token


class Instruction:
    def __init__(self,token:Token,branch:"list[Instruction]") -> None:
        self.next=self
        self.position=["1.0","1.end"]
        if token.type<2:
            self.id=0
            return
        self.id=token.type
        if token.type==7:
            branch.append(self)
            self.ifelse:Instruction=False
            self.ifend:Instruction=False
            return
        if token.type==8:
            branch[len(branch)-1].ifelse=self
            return
        if token.type==9:
            try:
                cond=branch.pop()
            except IndexError:
                from inspect import stack as s
                print('unexpected endif at',s()[2].frame.f_locals['tokens'].gi_frame.f_locals['o']+1,'line in file:',s()[1].frame.f_locals['filename'])
                del s
                return
            if not cond.ifelse:cond.ifelse=self
            cond.ifend=self
            return
        if token.type==99:
            self.value=token.number
            return
        if token.type==2:
            self.value=token.string
            return
        if self.id>=88 and self.id<99:
            self.value=token.string.lower()
            return
        #if token.type in Token.revkeywords:
        #return
    def __str__(self) -> str:
        if self.id==7:
            if self.ifelse==self.ifend:
                return 'if stackTop!=0 then '+str(self.next)
            else:
                return 'if stackTop!=0 then '+str(self.next)+' else '+str(self.ifelse)
        if self.id==2:
            return '"'+self.value+'"'
        if self.id==99:
            return str(self.value)
        if self.id>=88 and self.id<99:
            return Token.tags[self.id]+' '+self.value
        return Token.tags[self.id]
    @property
    def reverse(self):
        if self.id==99:
            return str(self.value)
        if self.id==2:
            return f'"{self.value}"'
        if self.id>=88 and self.id<99:
            return f"({Token.revvarprefix[self.id]}.{self.value})"
        
        try:
            return Token.revkeywords[self.id]
        except KeyError:
            return '___'+str(self.id)