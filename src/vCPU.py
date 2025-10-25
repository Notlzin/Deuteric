# vCPU.py program #
# a virtual and fake CPU thing #
from vGPU import vGPU

class vCPU:
    def __init__(self,memSize=256):
        # registers #
        self.registers = [0]*4
        self.pc = 0 # program counter #
        self.sp = memSize-1 # stack pointer [kinda-optional] #
        self.flags = {"Z":0,"C":0} # zero + carry flags #
        # memory #
        self.memory = [0]*memSize
        # devices (vGPU but prob later) #
        self.devices = {}
        self.halted = False

    def connectDevice(self,name,device):
        self.devices[name]=device

    def loadProg(self,prog,startAddr=0):
        for i,byte in enumerate(prog):
            self.memory[startAddr+i]=byte

    def fetch(self):
        instructions = self.memory[self.pc]
        self.pc += 1
        return instructions

    def run(self):
        while not self.halted:
            opcode = self.fetch()
            self.execution(opcode)

    def execution(self,opcode):
        # HLT #
        if opcode == 0x01:
            self.halted = True # halted #

        # LOAD #
        elif opcode == 0x10:
            reg = self.fetch()
            value = self.fetch()
            self.registers[reg]=value
            self.flags["Z"] = int(value==0)

        # MOV #
        elif opcode == 0x11:
            regDst = self.fetch()
            regSrc = self.fetch()
            self.registers[regDst]=self.registers[regSrc]
            self.flags["Z"]=int(self.registers[regDst]==0)

        # ADD #
        elif opcode == 0x20:
            regDst = self.fetch()
            regSrc = self.fetch()
            res = self.registers[regDst]+self.registers[regSrc]
            self.flags["C"] = int(res>255)
            res &= 0xFF # keeping 8 bit #
            self.registers[regDst]=res
            self.flags["Z"]=int(res==0)

        # SUB #
        elif opcode == 0x21:
            reg_dst = self.fetch()
            reg_src = self.fetch()
            res = self.registers[reg_dst] - self.registers[reg_src]
            self.flags["C"] = int(res < 0)
            res &= 0xFF
            self.registers[reg_dst] = res
            self.flags["Z"] = int(res == 0)

        # JMP #
        elif opcode == 0x30:
            addr = self.fetch()
            self.pc = addr

        # JZ #
        elif opcode == 0x31:
            addr = self.fetch()
            if self.flags["Z"]:
                self.pc = addr

        # OUT #
        elif opcode == 0x40:
            reg = self.fetch()
            deviceNameLen = self.fetch()
            deviceName = ""
            for _ in range(deviceNameLen):
                deviceName += chr(self.fetch())
            if deviceName in self.devices:
                self.devices[deviceName].receive(self.registers[reg])
            else:
                print(f"[vCPU]:unknown device: {deviceName}")

        else:
            print(f"[vCPU]:unknown opcode {opcode:02X} at pc={self.pc-1}")

# example device stub: #
# class vGPU:
#    def receive(self,val):
#        print(f"[vGPU] received value: {val}")
# no more class vGPU stub

# extra functions for commands encoded into hex #
def encodeCMD(cpu:vCPU,cmd: str,reg=0,deviceName="GPU"):
    # basically: convert whole prompt into 8-bit integers #
    # returns: [len, b0, b1, ..., b_n] #
    # prefix length so vCPU knows how much bytes #
    hexCMD = ' '.join(f'0x{ord(c):02X}' for c in cmd)
    print(f"[vCPU]:executed prompt to instructions => {hexCMD}")
    if deviceName in cpu.devices:
        cpu.devices[deviceName].receive(cpu.registers[reg])

# example usage #
if __name__ == "__main__":
    # test two #
    cpu = vCPU()
    gpu = vGPU()
    cpu.connectDevice("GPU", gpu)

    cmd = "help"
    encodeCMD(cpu, cmd)  # prints hex AND renders on vGPU
