# GPT-5mini bootloader.pxd LOL #
# bootloader.pxd #
# useless.

cdef class Bootloader:
    # attributes #
    cdef object cpu
    cdef object gpu
    cdef dict deviceMap
    cdef list devices
    cdef str kernelModule

    # methods #
    cpdef void bootMsg(self, str msg, double d) # type: ignore
    cpdef void runBIOS(self) # type: ignore
    cpdef void runPost(self) # type: ignore
    cpdef object loadKernel(self) # type: ignore
    cpdef void startKernel(self) # type: ignore

# also declare the top-level Boot function #
cpdef Boot()
