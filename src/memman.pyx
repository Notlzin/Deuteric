# memman.pyx #
# memory manager LOL #

totalMem = 16777216  # MB
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

# also another python wrapper for shell.py [totally unused] #
def pyAllocateMem(int mb):
    allocateMemory(mb)

def pyFreeMem(int mb):
    freeMemory(mb)
