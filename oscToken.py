class Token:
    keywords={
        '{init}':3,
        '{frame}':4,
        '{frame_ai}':5,
        '{end}':6,
        '{if}':7,
        '{else}':8,
        '{endif}':9,
        '&&':10,
        '||':11,
        '!':12,
        '+':13,
        '-':14,
        '*':15,
        '/':16,
        '%':17,
        '/-/':18,
        '=':19,
        '>':20,
        '<':21,
        '>=':22,
        '<=':23,
        '$=':24,
        '$>':25,
        '$<':26,
        '$>=':27,
        '$<=':28,
        'sin':29,
        'arcsin':30,
        'arctan':31,
        'min':32,
        'max':33,
        'exp':34,
        'sqrt':35,
        'sqr':36,
        'sgn':37,
        'pi':38,
        'random':39,
        'abs':40,
        'trunc':41,
        '$+':42,
        '$*':43,
        '$length':44,
        '$cutBegin':45,
        '$cutEnd':46,
        '$SetLengthR':47,
        '$SetLengthC':48,
        '$SetLengthL':49,
        '$IntToStr':50,
        '$IntToStrEnh':51,
        '$StrToFloat':52,
        '$RemoveSpaces':53,
        'd':54,
        '$d':55,
        '$msg':56,
        '%stackdump%':57,
        'l0':100,
        'l1':101,
        'l2':102,
        'l3':103,
        'l4':104,
        'l5':105,
        'l6':106,
        'l7':107,
        's0':108,
        's1':109,
        's2':110,
        's3':111,
        's4':112,
        's5':113,
        's6':114,
        's7':115,
        }
    revkeywords={v:k for k,v in keywords.items()}
    tags={
        0:'none',
        1:'comment',
        2:'string',
        3:'init',
        4:'frame',
        5:'ai frame',
        6:'end',
        7:'if',
        8:'else',
        9:'end if',
        10:'and',
        11:'or',
        12:'not',
        13:'add',
        14:'substract',
        15:'multiply',
        16:'divide',
        17:'modulo',
        18:'flip sign',
        19:'equal',
        20:'greater',
        21:'lesser',
        22:'greater or equal',
        23:'lesser or equal',
        24:'string equal',
        25:'string greater',
        26:'string lesser',
        27:'string greater or equal',
        28:'string lesser or equal',
        29:'sin',
        30:'arcsin',
        31:'arctan',
        32:'min',
        33:'max',
        34:'exp',
        35:'sqrt',
        36:'sqr',
        37:'sgn',
        38:'pi',
        39:'random',
        40:'abs',
        41:'trunc',
        42:'string concatenate',
        43:'string repeat until length',
        44:'string length',
        45:'string cut begin',
        46:'string cut end',
        47:'string set length align right',
        48:'string set length align center',
        49:'string set length align left',
        50:'integer to string',
        51:'integer to string enhanced',
        52:'string to float',
        53:'string remove spaces',
        54:'float duplicate',
        55:'string duplicate',
        56:'top string stack dump',
        57:'float stack dump',
        80:'macros',
        81:'trigger',
        88:'call macros',
        89:'call system macros',
        90:'load from system var',
        91:'load from local var',
        92:'load from string var',
        93:'store to local var',
        94:'store to string var',
        95:'load from constant',
        96:'call function',
        97:'play sound',
        98:'change sound',
        99:'number',
        100:'load reg0',
        101:'load reg1',
        102:'load reg2',
        103:'load reg3',
        104:'load reg4',
        105:'load reg5',
        106:'load reg6',
        107:'load reg7',
        108:'store reg0',
        109:'store reg1',
        110:'store reg2',
        111:'store reg3',
        112:'store reg4',
        113:'store reg5',
        114:'store reg6',
        115:'store reg7',
        }
    description={
        39:'random integer between 0 and stack top',
    }
    varprefix={
        'M.L':88,
        'M.V':89,
        'L.S':90,
        'L.L':91,
        'L.$':92,
        'S.L':93,
        'S.$':94,
        'C.L':95,
        'F.L':96,
        'T.L':97,
        'T.F':98
    }
    revvarprefix={v:k for k,v in varprefix.items()}
    def __init__(self,type:int,value:str) -> None:
        if type==0:
            if self.check(value):return
        self.type=type
        self.string=value
    def check(self,value:str)->bool:
        if value in self.keywords:
            self.type=self.keywords[value]
            self.string=''
            #self.string=value
            return True
        if value[0]=='(':
            if value[-1]!=')':
                return False
            if value[1:4] in self.varprefix:
                self.type=self.varprefix[value[1:4]]
                self.string=value[5:-1]
                return True
        if value[0]=='{':
            if value[-1]!='}':
                return False
            if value[1:7]=='macro:':
                self.type=80
                self.string=value[7:-1]
                return True
            if value[1:9]=='trigger:':
                self.type=81
                self.string=value[9:-1]
                return True
        try:
            self.number=float(value)
            self.type=99
            self.string=value
            return True
        except ValueError:
            from inspect import stack as s
            print('cannot parse "'+value+'"->skipped in file:',s()[4].frame.f_locals['filename'])
            del s
            
        return False
    @property
    def type_name(self):
        return self.tags[self.type]