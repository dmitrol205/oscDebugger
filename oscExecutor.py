import random
from variablePool import VariablePool
from register8 import Register8
from oscInstruction import Instruction
from oscProgram import Program
from oscCode import Code
from oscInstructionSet import InstructionSet
from loopStack8 import LoopStack8
import codeView

class Executor:
    sysvars={
        "timegap",
        "gettime",
        "nosound",
        "pause",
        "time",
        "day",
        "month",
        "year",
        "dayofyear",
        "mouse_x",
        "mouse_y",
        "preciptype",
        "preciprate",
        "coll_pos_x",
        "coll_pos_y",
        "coll_pos_z",
        "coll_energy",
        "weather_temperature",
        "weather_abshum",
        "wearlifespan",
        "autoclutch",
        "sunalt"
    }
    #sysvars=[i.lower() for i in sysvars]
    roadvehicle_varlist={
        "refresh_strings":False,
        "envir_brightness":True,
        "streetcond":True,
        "spot_select":True,
        "colorscheme":True,
        "m_wheel":False,
        "n_wheel":True,
        "throttle":True,
        "brake":True,
        "clutch":True,
        "brakeforce":False,
        "velocity":True,
        "velocity_ground":True,
        "tank_percent":False,
        "kmcounter_km":True,
        "kmcounter_m":True,
        "relrange":True,
        "driver_seat_verttransl":True,
        "wheel_rotation_0_l":True,
        "wheel_rotation_0_r":True,
        "wheel_rotation_1_l":True,
        "wheel_rotation_1_r":True,
        "wheel_rotation_2_l":True,
        "wheel_rotation_2_r":True,
        "wheel_rotation_3_l":True,
        "wheel_rotation_3_r":True,
        "wheel_rotationspeed_0_l":True,
        "wheel_rotationspeed_0_r":True,
        "wheel_rotationspeed_1_l":True,
        "wheel_rotationspeed_1_r":True,
        "wheel_rotationspeed_2_l":True,
        "wheel_rotationspeed_2_r":True,
        "wheel_rotationspeed_3_l":True,
        "wheel_rotationspeed_3_r":True,
        "axle_suspension_0_l":True,
        "axle_suspension_0_r":True,
        "axle_suspension_1_l":True,
        "axle_suspension_1_r":True,
        "axle_suspension_2_l":True,
        "axle_suspension_2_r":True,
        "axle_suspension_3_l":True,
        "axle_suspension_3_r":True,
        "axle_steering_0_l":True,
        "axle_steering_0_r":True,
        "axle_steering_1_l":True,
        "axle_steering_1_r":True,
        "axle_steering_2_l":True,
        "axle_steering_2_r":True,
        "axle_steering_3_l":True,
        "axle_steering_3_r":True,
        "axle_springfactor_0_l":False,
        "axle_springfactor_0_r":False,
        "axle_springfactor_1_l":False,
        "axle_springfactor_1_r":False,
        "axle_springfactor_2_l":False,
        "axle_springfactor_2_r":False,
        "axle_springfactor_3_l":False,
        "axle_springfactor_3_r":False,
        "axle_brakeforce_0_l":False,
        "axle_brakeforce_0_r":False,
        "axle_brakeforce_1_l":False,
        "axle_brakeforce_1_r":False,
        "axle_brakeforce_2_l":False,
        "axle_brakeforce_2_r":False,
        "axle_brakeforce_3_l":False,
        "axle_brakeforce_3_r":False,
        "debug_0":False,
        "debug_1":False,
        "debug_2":False,
        "debug_3":False,
        "debug_4":False,
        "debug_5":False,
        "a_trans_x":True,
        "a_trans_y":True,
        "a_trans_z":True,
        "ai_blinker_l":True,
        "ai_blinker_r":True,
        "ai_light":True,
        "ai_interiorlight":True,
        "ai_brakelight":True,
        "ai_engine":True,
        "ai_target_index":True,
        "ai_scheduled_atstation":True,
        "ai":True,
        "pax_entry0_open":False,
        "pax_entry1_open":False,
        "pax_entry2_open":False,
        "pax_entry3_open":False,
        "pax_entry4_open":False,
        "pax_entry5_open":False,
        "pax_entry6_open":False,
        "pax_entry7_open":False,
        "pax_exit0_open":False,
        "pax_exit1_open":False,
        "pax_exit2_open":False,
        "pax_exit3_open":False,
        "pax_exit4_open":False,
        "pax_exit5_open":False,
        "pax_exit6_open":False,
        "pax_exit7_open":False,
        "pax_entry0_req":False,
        "pax_entry1_req":False,
        "pax_entry2_req":False,
        "pax_entry3_req":False,
        "pax_entry4_req":False,
        "pax_entry5_req":False,
        "pax_entry6_req":False,
        "pax_entry7_req":False,
        "pax_exit0_req":False,
        "pax_exit1_req":False,
        "pax_exit2_req":False,
        "pax_exit3_req":False,
        "pax_exit4_req":False,
        "pax_exit5_req":False,
        "pax_exit6_req":False,
        "pax_exit7_req":False,
        "giventicket":False,
        "humans_count":True,
        "ff_vib_period":False,
        "ff_vib_amp":False,
        "snd_outsidevol":False,
        "snd_microphone":False,
        "snd_radio":False,
        "cabinair_temp":False,
        "cabinair_relhum":True,
        "cabinair_abshum":False,
        "preciprate":True,
        "preciptype":True,
        "dirtrate":True,
        "dirt_norm":True,
        "target_index_int":False,
        "schedule_active":True,
        "train_frontcoupling":True,
        "train_backcoupling":True,
        "train_me_reverse":True,
        "trafficpriority":False,
        "trafficprioritywarningneeded":True,
        "wearlifespan":True,
    }
    roadvehicle_stringvarlist={
        "ident":True,
        "number":True,
        "act_route":False,
        "act_busstop":True,
        "setlineto":True,
        "yard":True,
        "file_schedule":True,
    }
    def __init__(self,program:Program) -> None:
        #self.iset=InstructionSet()
        self.codeView:'codeView.CodeView'=False
        self.program=program
        self.isalive=False
        self.stepmode=False
        self.float_stack=LoopStack8()
        self.string_stack=LoopStack8(True)
        self.register=Register8()
        self.float_local=VariablePool()
        self.string_local=VariablePool()
        self.system_variables=VariablePool()
        self.float_constants=VariablePool()
        self.breakpoints=set()
        self.allowbreakpoints=False
        self.ipstack=[]
        self.error={}
        
        self.extendedIf=not self.program.reducedif
        for k,v in self.program.constants.items():
            self.float_constants[k]=v,True
        for k in Executor.sysvars:
            self.system_variables[k]=float(0),True
        for i in program.varnames:
            self.float_local[i]=float(0),False
        for k,v in Executor.roadvehicle_varlist.items():
            self.float_local[k]=float(0),v
        for i in program.stringvarnames:
            self.string_local[i]='',False
        for k,v in Executor.roadvehicle_stringvarlist.items():
            self.string_local[k]='',v
        if self.program.init:
            self.ip=self.program.init.entryPoint
        else:
            self.ip=False
    def setBreakpoint(self,inst:Instruction,swap:bool=False):
        if inst not in self.breakpoints:
            self.allowbreakpoints=True
            self.breakpoints.add(inst)
            return True
        else:
            if swap:
                self.removeBreakpoint(inst)
            return False
    def removeBreakpoint(self,inst:Instruction):
        self.breakpoints.remove(inst)
        if len(self.breakpoints)==0:
            self.allowbreakpoints=False
    def attachCodeView(self,codeView:'codeView.CodeView'):
        self.codeView=codeView
    def next(self):
        self.ip=self.ip.next
    def getCode(self,ct:str="",cn:str="")->Code:
        if ct=="" and cn=="":
            ct=self.codeType
            cn=self.codeName
        if ct=='macro':
            return self.program.macros[cn]
        elif ct=='trigger':
            return self.program.triggers[cn]
        elif ct=='init':
            return self.program.init
        elif ct=='frame':
            return self.program.frame
        elif ct=='frame_ai':
            return self.program.frame_ai
        return False
    def updateViews(self):
        if self.isalive and self.stepmode:
            if self.codeView:
                if not self.codeView.isCurrentCode(self.codeType,self.codeName):
                    self.codeView.loadCode(self.getCode(),self.breakpoints,self.codeType,self.codeName)
                if self.ip.id==7:
                    self.codeView.selectIf(self.ip)
                else:
                    self.codeView.selectInstruction(self.ip)
            self.register.updateView()
            self.float_stack.updateView()
            self.string_stack.updateView()
            self.float_constants.updateView()
            self.float_local.updateView()
            self.string_local.updateView()
            self.system_variables.updateView()
    def updateFrame(self):
        self.system_variables.update('timegap',0.011+random.random()/100)
    def debugOutput(self,text:str,key:str=''):
        print(f"[debug]{key}:{text}")    
    def execute(self,codetype:str,codename:str=""):
        self.codeType=codetype
        self.codeName=codename
        #print(self.codeType,self.codeName)
        self.ip=self.getCode().entryPoint
        #if self.stepmode:
            #self.updateViews()
        while self.isalive and self.ip:
            if self.extendedIf and self.ip.id in [8,9]:
                self.next()
                continue
            if self.allowbreakpoints and self.ip in self.breakpoints:
                self.stepmode=True
            if self.stepmode:
                self.updateViews() 
                if self.codeView:
                    self.codeView.winfo_toplevel().title("idle")
                yield self.ip
                if self.codeView:
                    self.codeView.winfo_toplevel().title("running")
            _=InstructionSet[self.ip](self)
            if _!=None:
                yield from _
    def run(self,ai:bool=False):
        self.aimode=ai
        if self.isalive:raise Exception
        self.isalive=True
        self.ipstack=[]
        if self.program.init:
            yield from self.execute('init')
        if ai:
            if self.program.frame_ai:
                while self.isalive:
                    self.updateFrame()
                    yield from self.execute('frame_ai') 
        else:
            if self.program.frame:
                while self.isalive:
                    self.updateFrame()
                    yield from self.execute('frame')
        self.isalive=False
    def stop(self):
        self.isalive=False
    def getCodeNameOfInstruction(self,inst:Instruction):
        if self.program.init:
            for i in self.program.init:
                if i is inst:
                    return ['init','']
        if self.program.frame:
            for i in self.program.frame:
                if i is inst:
                    return ['frame','']
        if self.program.frame_ai:
            for i in self.program.frame_ai:
                if i is inst:
                    return ['frame_ai','']
        for n,o in self.program.macros.items():
            for i in o:
                if i is inst:
                    return ['macro',n]
        for n,o in self.program.triggers.items():
            for i in o:
                if i is inst:
                    return ['trigger',n]
        return False
