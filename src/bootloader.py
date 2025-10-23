# bootloader.py, yes its copy pasted #
import time
import sys

class Bootloader:
    def __init__(self):
        self.devices =  ["CPU","Memory","Disk","Keyboard","Display"]
        self.kernelModule = "kernel"    # the kernel.py #

    def bootMsg(self,msg,d=0.4):
        sys.stdout.write(msg+'\n')
        sys.stdout.flush()
        time.sleep(d)

    def runPost(self):
        self.bootMsg("staring the bootloader...")
        self.bootMsg("performing POST (Power-on self test)...")
        for device in self.devices:
            self.bootMsg(f"initializing {device}....OK",0.3)
        self.bootMsg("POST complete.\n")

    def loadKernel(self):
        self.bootMsg("loading kernel.pyx...")
        try:
            kernel = __import__(self.kernelModule)
            self.bootMsg("kernel loaded successfully.\n")
            return kernel
        except ImportError as e:
            self.bootMsg(f"kernel unfound. error: {hex(len("kernel"))} and import error: {hex(len(str(e)))}")
            return None

    def startKernel(self):
        kernel = self.loadKernel()
        if kernel is not None:
            self.bootMsg("transferring control to kernel...\n")
            kernel.start()
        else:
            self.bootMsg(f"bootloader failed. HLT activated. error: {hex(id("bootloader") & 0xFFFF)}")
            sys.exit(1)

# main loop + Boot function #
def Boot():
    boot_loader = Bootloader()
    boot_loader.runPost()
    boot_loader.startKernel()

if __name__ == "__main__":
    Boot()
