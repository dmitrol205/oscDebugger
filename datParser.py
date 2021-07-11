from io import TextIOWrapper
from datToken import Token


def parse(file:TextIOWrapper):
    for s in file.readlines():
        last=len(s)-1 if s[-1]=='\n' else len(s)
        if s[0]=='\t' or s[0]=='\n' or s[0]==' ': 
            yield Token(1,s[:last])
            continue
        if s[0]=='[':
            if s[last-1]==']':
                yield Token(2,s[1:last-1])
            else:
                yield Token(1,s[:last])
            continue
        yield Token(0,s[:last])
        