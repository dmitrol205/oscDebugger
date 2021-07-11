from io import TextIOWrapper
from oscToken import Token

def parse(file:TextIOWrapper):
    lines=file.readlines()
    for o in range(len(lines)):
        s=lines[o]
        if s[-1]!='\n':s+='\n'
        start=0
        if s[0]=='\'': 
            yield Token(1,s[:-1])
            continue
        strStart=False
        for i in range(len(s)):
            if i==start and s[i]=='"':
                strStart=True
                continue
            if strStart:
                if i!=start and s[i]=='"':
                    strStart=False
                    yield Token(2,s[start+1:i])
                    i+=1
                    start=i
            else:
                if s[i]==' ' or s[i]=='\t' or s[i]=='\n':
                    if i!=start:
                        yield Token(0,s[start:i])
                    start=i+1
        if strStart:
            raise Exception("Multiline strings not supported")
        #yield s

def main():

    #g=parse(open(r'D:\Program Files (x86)\OMSI 2.2.027\Vehicles\Trabant\script\Trabant_AI.osc','r'))
    g=parse(open(r'D:\Program Files (x86)\OMSI 2.2.027\Vehicles\MAN Lions City Euro 6\Script\churakrueger\VMatrix.osc','r'))
    print(type(g))
    c=0
    for i in g:
        if i.type!=1:
            print(i.type_name,'"'+i.string+'"')
            c+=1
        if c>20:break
        

if __name__=='__main__':main()