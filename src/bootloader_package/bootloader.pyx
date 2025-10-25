# bootloader.py, yes its copy pasted #
import time
import sys

cdef class Bootloader:
    # attributes [theres none of it LOL] #
    #   |
    #   V
    def __init__(self):
        self.devices =  ["CPU","Memory","Disk","Keyboard","Display"]
        self.kernelModule = "kernel"    # the kernel.py #

    # rest of the cpdef functions #
    cpdef void bootMsg(self,str msg,double d):
         # method assigning #
        if d == 0.0:
            d = <double>0.4
        cdef double delay = d
        sys.stdout.write(msg+'\n')
        sys.stdout.flush()
        time.sleep(<float>delay)

    cpdef void runPost(self):
        self.bootMsg("starting the bootloader...",<double>0.1)
        self.bootMsg("performing POST (Power-on self test)...",<double>0.0)
        for device in self.devices:
            self.bootMsg(f"initializing {device}....OK",<double>0.3)
        self.bootMsg("POST complete.\n",<double>0.4)

    cpdef object loadKernel(self):
        self.bootMsg("loading kernel.pyx...",<double>0.6)
        try:
            kernel = __import__(self.kernelModule)
            self.bootMsg("kernel loaded successfully.\n",<double>0.2)
            return kernel
        except ImportError as e:
            self.bootMsg(f"kernel unfound. error: {hex(len('kernel'))} and import error: {hex(len(str(e)))}",<double>0.3)

    cpdef void startKernel(self):
        cdef object kernel = self.loadKernel()
        if kernel is not None:
            self.bootMsg("transferring control to kernel...\n", <double>0.4)
            getattr(kernel, 'start')()
        else:
            self.bootMsg(f"bootloader failed. HLT activated. "
                         f"error: {hex(id('bootloader') & 0xFFFF)}", <double>0.4)
            sys.exit(1)

# main loop + Boot function #
cpdef Boot():
    boot_loader = Bootloader()
    boot_loader.runPost()
    boot_loader.startKernel()

if __name__ == "__main__":
    Boot()
