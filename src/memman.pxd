# memman.pxd #
cdef int totalMem  # MB
cdef int usedMem
cdef void allocateMemory(int mb)
cdef void freeMemory(int mb)
