# the procman.pxd woohoo #
# procman.pxd #
cdef class Process:
    cdef public int pid
    cdef public str name
    cdef public int cpu_usage

cdef void initProcesses(int n)
cdef void simulateCPUUsage()
cdef list processes
