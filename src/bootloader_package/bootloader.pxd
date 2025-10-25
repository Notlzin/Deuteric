# GPT-5mini bootloader.pxd LOL #
# bootloader.pxd #

cdef class Bootloader:
    # attributes #
    cdef object cpu
    cdef object gpu
    cdef dict deviceMap
    cdef list devices
    cdef str kernelModule

    # methods #
    cpdef void bootMsg(self, str msg, double d)
    cpdef void runBIOS(self)
    cpdef void runPost(self)
    cpdef object loadKernel(self)
    cpdef void startKernel(self)

# also declare the top-level Boot function #
cpdef Boot()
