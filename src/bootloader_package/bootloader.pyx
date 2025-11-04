# bootloader.py, yes its copy pasted #
import time
from vCPU import vCPU, encodeCMD
from vGPU import vGPU
from BIOS import BIOS
import sys

cdef class Bootloader:
    # attributes [theres none of it LOL] #
    #   |
    #   V
    def __init__(self):
        self.devices =  ["CPU","Memory","Disk","Keyboard","Display"]
        self.kernelModule = "kernel"    # the kernel.py #
        self.cpu = vCPU()
        self.gpu = vGPU()
        self.deviceMap = {"GPU":self.gpu}

    # rest of the cpdef functions #
    cpdef void bootMsg(self,str msg,double d):
         # method assigning #
        if d == 0.0:
            d = <double>0.4
        cdef double delay = d
        sys.stdout.write(msg+'\n')
        sys.stdout.flush()
        time.sleep(<float>delay)

    cpdef void runBIOS(self):
        self.bootMsg("[bootloader.py]: running BIOS...", <double>0.2)
        bios = BIOS(self.cpu, self.deviceMap)
        bios.runBIOS()
        self.bootMsg("[bootloader.py]: BIOS finished, devices ready.\n", <double>0.2)

    cpdef void runPost(self):
        self.bootMsg("[bootloader.py] starting the bootloader...",<double>0.1)
        self.bootMsg("[bootloader.py] performing POST (Power-on self test)...",<double>0.0)
        for device in self.devices:
            self.bootMsg(f"[bootloader.py] initializing {device}....OK",<double>0.3)
        self.bootMsg("[bootloader.py] POST complete.\n",<double>0.4)

    cpdef object loadKernel(self):
        self.bootMsg("[bootloader.py] loading kernel.pyx...",<double>0.6)
        try:
            kernel = __import__(self.kernelModule)
            self.bootMsg("[bootloader.py] kernel loaded successfully.\n",<double>0.2)
            return kernel
        except ImportError as e:
            self.bootMsg(f"[bootloader.py] kernel unfound. error: {hex(len('kernel'))} and import error: {hex(len(str(e)))}",<double>0.3)

    cpdef void startKernel(self):
        cdef object kernel = self.loadKernel()
        if kernel is not None:
            self.bootMsg("[bootloader.py] transferring control to kernel...\n", <double>0.4)
            if hasattr(kernel, 'start'):
                getattr(kernel, "start")(self.cpu,self.gpu)
        else:
            self.bootMsg(f"[bootloader.py] bootloader failed. HLT activated. "
                         f"error: {hex(id('bootloader') & 0xFFFF)}", <double>0.4)
            sys.exit(1)

# main loop + Boot function #
cpdef Boot():
    boot_loader = Bootloader()
    boot_loader.runBIOS()
    boot_loader.runPost()
    boot_loader.startKernel()

if __name__ == "__main__":
    Boot()
