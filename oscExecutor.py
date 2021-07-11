from register8 import Register8
from oscInstruction import Instruction
from oscProgram import Program
from oscCode import Code
from oscInstructionSet import InstructionSet
from loopStack8 import LoopStack8
import codeView

class Executor:
    sysvars=[
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
    ]
    #sysvars=[i.lower() for i in sysvars]
    roadvehicle_varlist=[
        "refresh_strings",
        "envir_brightness",
        "streetcond",
        "spot_select",
        "colorscheme",
        "m_wheel",
        "n_wheel",
        "throttle",
        "brake",
        "clutch",
        "brakeforce",
        "velocity",
        "velocity_ground",
        "tank_percent",
        "kmcounter_km",
        "kmcounter_m",
        "relrange",
        "driver_seat_verttransl",
        "wheel_rotation_0_l",
        "wheel_rotation_0_r",
        "wheel_rotation_1_l",
        "wheel_rotation_1_r",
        "wheel_rotation_2_l",
        "wheel_rotation_2_r",
        "wheel_rotation_3_l",
        "wheel_rotation_3_r",
        "wheel_rotationspeed_0_l",
        "wheel_rotationspeed_0_r",
        "wheel_rotationspeed_1_l",
        "wheel_rotationspeed_1_r",
        "wheel_rotationspeed_2_l",
        "wheel_rotationspeed_2_r",
        "wheel_rotationspeed_3_l",
        "wheel_rotationspeed_3_r",
        "axle_suspension_0_l",
        "axle_suspension_0_r",
        "axle_suspension_1_l",
        "axle_suspension_1_r",
        "axle_suspension_2_l",
        "axle_suspension_2_r",
        "axle_suspension_3_l",
        "axle_suspension_3_r",
        "axle_steering_0_l",
        "axle_steering_0_r",
        "axle_steering_1_l",
        "axle_steering_1_r",
        "axle_steering_2_l",
        "axle_steering_2_r",
        "axle_steering_3_l",
        "axle_steering_3_r",
        "axle_springfactor_0_l",
        "axle_springfactor_0_r",
        "axle_springfactor_1_l",
        "axle_springfactor_1_r",
        "axle_springfactor_2_l",
        "axle_springfactor_2_r",
        "axle_springfactor_3_l",
        "axle_springfactor_3_r",
        "axle_brakeforce_0_l",
        "axle_brakeforce_0_r",
        "axle_brakeforce_1_l",
        "axle_brakeforce_1_r",
        "axle_brakeforce_2_l",
        "axle_brakeforce_2_r",
        "axle_brakeforce_3_l",
        "axle_brakeforce_3_r",
        "debug_0",
        "debug_1",
        "debug_2",
        "debug_3",
        "debug_4",
        "debug_5",
        "a_trans_x",
        "a_trans_y",
        "a_trans_z",
        "ai_blinker_l",
        "ai_blinker_r",
        "ai_light",
        "ai_interiorlight",
        "ai_brakelight",
        "ai_engine",
        "ai_target_index",
        "ai_scheduled_atstation",
        "ai",
        "pax_entry0_open",
        "pax_entry1_open",
        "pax_entry2_open",
        "pax_entry3_open",
        "pax_entry4_open",
        "pax_entry5_open",
        "pax_entry6_open",
        "pax_entry7_open",
        "pax_exit0_open",
        "pax_exit1_open",
        "pax_exit2_open",
        "pax_exit3_open",
        "pax_exit4_open",
        "pax_exit5_open",
        "pax_exit6_open",
        "pax_exit7_open",
        "pax_entry0_req",
        "pax_entry1_req",
        "pax_entry2_req",
        "pax_entry3_req",
        "pax_entry4_req",
        "pax_entry5_req",
        "pax_entry6_req",
        "pax_entry7_req",
        "pax_exit0_req",
        "pax_exit1_req",
        "pax_exit2_req",
        "pax_exit3_req",
        "pax_exit4_req",
        "pax_exit5_req",
        "pax_exit6_req",
        "pax_exit7_req",
        "giventicket",
        "humans_count",
        "ff_vib_period",
        "ff_vib_amp",
        "snd_outsidevol",
        "snd_microphone",
        "snd_radio",
        "cabinair_temp",
        "cabinair_relhum",
        "cabinair_abshum",
        "preciprate",
        "preciptype",
        "dirtrate",
        "dirt_norm",
        "target_index_int",
        "schedule_active",
        "train_frontcoupling",
        "train_backcoupling",
        "train_me_reverse",
        "trafficpriority",
        "trafficprioritywarningneeded",
        "wearlifespan"
    ]
    def __init__(self,program:Program) -> None:
        #self.iset=InstructionSet()
        self.codeView:'codeView.CodeView'=False
        self.program=program
        self.isalive=False
        self.stepmode=False
        self.float_stack=LoopStack8()
        self.string_stack=LoopStack8(True)
        self.register=Register8()
        self.float_local={}
        self.string_local={}
        self.breakpoints=[]
        self.allowbreakpoints=False
        self.ipstack=[]
        self.error={}
        self.system_variables={k:float(0) for k in Executor.sysvars}
        self.float_constants={k:v for k,v in self.program.constants.items()}
        self.extendedIf=not self.program.reducedif
        for i in program.varnames:
            self.float_local[i]=0.0
        for i in Executor.roadvehicle_varlist:
            self.float_local[i]=0.0
        if self.program.init:
            self.ip=self.program.init.entryPoint
        else:
            self.ip=False
    def setBreakpoint(self,inst:Instruction):
        if inst not in self.breakpoints:
            self.allowbreakpoints=True
            self.breakpoints.append(inst)
    def removeBreakpoint(self,inst:Instruction):
        self.breakpoints.remove(inst)
        if len(self.breakpoints)==0:
            self.allowbreakpoints=False
    def attachCodeView(self,codeView:'codeView.CodeView'):
        self.codeView=codeView
        self.updateCodeView()
    def next(self):
        self.ip=self.ip.next
    def getCode(self):
        if self.codeType=='macro':
            return self.program.macros[self.codeName]
        elif self.codeType=='trigger':
            return self.program.triggers[self.codeName]
        elif self.codeType=='init':
            return self.program.init
        elif self.codeType=='frame':
            return self.program.frame
        elif self.codeType=='frame_ai':
            return self.program.frame_ai
        return False
    def updateCodeView(self):
        if self.isalive and self.stepmode and self.codeView:
            self.codeView.loadCode(self.getCode(),self.breakpoints,self.codeType,self.codeName)
    def debugOutput(self,text:str,key:str=''):
        print(f"[debug]{key}:{text}")    
    def execute(self,codetype:str,codename:str=""):
        self.codeType=codetype
        self.codeName=codename
        print(self.codeType,self.codeName)
        self.ip=self.getCode().entryPoint
        self.updateCodeView()
        while self.isalive and self.ip:
            if self.extendedIf and self.ip.id in [8,9]:
                self.next()
                continue
            if self.allowbreakpoints and self.ip in self.breakpoints:
                self.stepmode=True
                self.updateCodeView()
            if self.stepmode:
                if self.codeView:
                    if self.ip.id==7:
                        self.codeView.selectIf(self.ip)
                    else:
                        self.codeView.selectInstruction(self.ip)
                yield self.ip
            _=InstructionSet[self.ip](self)
            if _!=None:
                yield from _
    def run(self,ai:bool=False):
        if self.isalive:raise Exception
        self.isalive=True
        self.ipstack=[]
        if self.program.init:
            yield from self.execute('init')
        if ai:
            if self.program.frame_ai:
                while self.isalive:
                    yield from self.execute('frame_ai')    
        else:
            if self.program.frame:
                while self.isalive:
                    yield from self.execute('frame')
    def stop(self):
        self.isalive=False