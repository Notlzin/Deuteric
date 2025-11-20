# BIOS.py
class BIOS:
    def __init__(self, cpu, devices=None):
        self.cpu = cpu
        self.devices = devices or {}
        self.memory_initialized = False
        self.devices_initialized = False

    # initialize memory #
    def initMemory(self):
        print("[BIOS.py] Initializing virtual memory (vmem)...")
        self.cpu.memory = [0] * len(self.cpu.memory)
        self.memory_initialized = True

    # initialize devices #
    def initDevices(self):
        print("[BIOS.py] Initializing virtual devices (vdev) ...")
        for name, dev in self.devices.items():
            print(f"[BIOS] Device '{name}' initialized.")
        self.devices_initialized = True

    # fake CPU testing in bios #
    def runCpuTest(self):
        print("[BIOS.py] Running ceremonial CPU test...")
        # Fake test program (LOAD 5 into R0, send to vGPU, HLT), yes this is GPT-5 generated, dont ask #
        testProgram = [
            0x10, 0x0, 0x5,                                 # LOAD R0, 5 #
            0x40, 0x0, 0x3, ord('G'), ord('P'), ord('U'),   # OUT R0, "GPU" #
            0x01                                            # HLT #
        ]
        self.cpu.loadProg(testProgram)
        self.cpu.run()
        print("[BIOS.py] CPU test completed successfully.")

    # installation for devices and bootloader.pyx including kernel.pyx and VirtualNIC network stack #
    def fakeInstallation(self):
        print("[BIOS.py] Running ceremonial installation...")
        steps = ["Kernel", "VirtualNIC", "vGPU", "Bootloader"]
        for step in steps:
            print(f"[BIOS.py] Installing {step}...")
        print("[BIOS.py] Installation complete!")

    # boots it duh #
    def bootOS(self):
        print("[BIOS.py] Handing control to bootloader.pyx...")
        # In real Deuteric, bootloader would load kernel next
        print("[BIOS.py] Deuteric is now running!")

    # run bios "tests" #
    def runBIOS(self):
        self.initMemory()
        self.initDevices()
        self.runCpuTest()
        self.fakeInstallation()
        self.bootOS()

# usage cases for this bios.py and in bootloader.pyx
if __name__ == "__main__":
    from vCPU import vCPU
    from vGPU import vGPU
    cpu = vCPU()
    gpu = vGPU()
    bios = BIOS(cpu, {"GPU": gpu})
    bios.runBIOS()
