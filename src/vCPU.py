# vCPU.py #
# obviously vibe coded and pushed GPT into a huge stress test #
from array import array
from vGPU import vGPU

class vCPU:
    __slots__ = ("registers", "pc", "sp", "flags", "memory", "devices", "halted")
    def __init__(self, memSize=256):
        # 8-bit registers #
        self.registers = array('B', [0] * 4)
        self.pc = 0
        self.sp = memSize - 1
        self.flags = {"Z": 0, "C": 0}
        self.memory = array('B', [0] * memSize)
        self.devices = {}
        self.halted = False

    def connectDevice(self, name: str, device):
        self.devices[name] = device

    def loadProg(self, prog, startAddr=0):
        self.memory[startAddr:startAddr + len(prog)] = array('B', prog)

    def fetch(self):
        val = self.memory[self.pc]
        self.pc += 1
        return val

    def run(self):
        mem = self.memory
        regs = self.registers
        flags = self.flags
        devices = self.devices
        pc = self.pc

        while not self.halted:
            opcode = mem[pc]
            pc += 1

            # HLT #
            if opcode == 0x01:
                self.halted = True

            # LOAD #
            elif opcode == 0x10:
                reg = mem[pc]
                val = mem[pc + 1]
                regs[reg] = val
                flags["Z"] = int(val == 0)
                pc += 2

            # MOV #
            elif opcode == 0x11:
                regDst = mem[pc]
                regSrc = mem[pc + 1]
                val = regs[regSrc]
                regs[regDst] = val
                flags["Z"] = int(val == 0)
                pc += 2

            # ADD #
            elif opcode == 0x20:
                regDst = mem[pc]
                regSrc = mem[pc + 1]
                res = regs[regDst] + regs[regSrc]
                flags["C"] = int(res > 255)
                res &= 0xFF
                regs[regDst] = res
                flags["Z"] = int(res == 0)
                pc += 2

            # SUB #
            elif opcode == 0x21:
                regDst = mem[pc]
                regSrc = mem[pc + 1]
                res = regs[regDst] - regs[regSrc]
                flags["C"] = int(res < 0)
                res &= 0xFF
                regs[regDst] = res
                flags["Z"] = int(res == 0)
                pc += 2

            # JMP #
            elif opcode == 0x30:
                pc = mem[pc]

            # JZ #
            elif opcode == 0x31:
                addr = mem[pc]
                if flags["Z"]:
                    pc = addr
                else:
                    pc += 1

            # OUT #
            elif opcode == 0x40:
                reg = mem[pc]
                name_len = mem[pc + 1]
                device_name = "".join(chr(mem[pc + 2 + i]) for i in range(name_len))
                device = devices.get(device_name)
                if device:
                    device.receive(regs[reg])
                else:
                    print(f"[vCPU]: unknown device '{device_name}'")
                pc += 2 + name_len

            else:
                print(f"[vCPU]: unknown opcode 0x{opcode:02X} at PC={pc-1}")
                self.halted = True

        self.pc = pc  # save back pc[program counter] #

# encoding the commands into hexadecimal #
def encodeCMD(cpu, cmd: str, reg=0, deviceName="GPU"):
    # preallocation part #
    cmdLen = len(cmd)
    hexCMD =  bytearray(cmdLen+1)
    for i in range(cmdLen):
        hexCMD[i] = ord(cmd[i])  # store integer (0 to 255 for 8 bit because 2^8) #
    hexCMD[cmdLen] = 0 # string terminator handler #

    # build hex strings (ofcourse joined) #
    hexString = ' '.join(f'0x{b:02X}' for b in hexCMD)
    print(f"[vCPU]:executed prompt to hex => {hexString}")

    # send to device only once #
    dev = cpu.devices.get(deviceName)
    if dev:
        dev.receive(cpu.registers[reg])


# usage cases #
if __name__ == "__main__":
    cpu = vCPU()
    gpu = vGPU()
    cpu.connectDevice("GPU", gpu)

    cmd = "help"
    encodeCMD(cpu, cmd) # prints on hex and on vGPU #
