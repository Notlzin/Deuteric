# memman.pyx #
# memory manager LOL #

totalMem = 1024  # MB
usedMem = 0

cdef void allocateMemory(int mb):
    global usedMem
    if usedMem + mb <= totalMem:
        usedMem += mb
    else:
        used_memory = totalMem

cdef void freeMemory(int mb):
    global usedMem
    usedMem -= mb
    if usedMem < 0:
        usedMem = 0

# also another python wrapper for shell.py #
def pyAllocateMem(int mb):
    allocateMemory(mb)

def pyFreeMem(int mb):
    freeMemory(mb)
