# BIOS.py #
class BIOS:
    def __init__(self, cpu, devices=None):
        self.cpu = cpu
        self.devices = devices or {}
        self.memory_initialized = False
        self.devices_initialized = False

    def initMemory(self):
        print("[BIOS.py] Initializing virtual memory...")
        self.cpu.memory = [0] * len(self.cpu.memory)
        self.memory_initialized = True

    def initDevices(self):
        print("[BIOS.py] Initializing virtual devices...")
        for name, dev in self.devices.items():
            print(f"[BIOS] Device '{name}' initialized.")
        self.devices_initialized = True

    def runCpuTest(self):
        print("[BIOS.py] Running ceremonial CPU test...")
        # Fake test program (LOAD 5 into R0, send to vGPU, HLT)
        program = [
            0x10, 0x0, 0x5,          # LOAD R0, 5
            0x40, 0x0, 0x3, ord('G'), ord('P'), ord('U'),  # OUT R0, "GPU"
            0x01                      # HLT
        ]
        self.cpu.loadProg(program)
        self.cpu.run()
        print("[BIOS.py] CPU test completed successfully.")

    def fakeInstallation(self):
        print("[BIOS.py] Running ceremonial installation...")
        steps = ["Kernel", "VirtualNIC", "vGPU", "Bootloader"]
        for step in steps:
            print(f"[BIOS.py] Installing {step}...")
        print("[BIOS.py] Installation complete!")

    def bootOS(self):
        print("[BIOS.py] Handing control to bootloader/OS...")
        # In real Deuteric, bootloader would load kernel next
        print("[BIOS.py] OS is now running!")

    def run(self):
        self.initMemory()
        self.initDevices()
        self.runCpuTest()
        self.fakeInstallation()
        self.bootOS()


# usage case LOL #
if __name__ == "__main__":
    from vCPU import vCPU
    from vGPU import vGPU

    cpu = vCPU()
    gpu = vGPU()
    bios = BIOS(cpu, {"GPU": gpu})
    bios.run()
