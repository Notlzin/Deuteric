# procman.pyx, copy pasted as you know #
from libc.stdlib cimport rand

cdef class Process:
    def __init__(self, int pid, name):
        self.pid = pid
        self.name = name
        self.cpu_usage = 0

# fake process manager part #
cdef list processes = []

cdef void initProcesses(int n):
    cdef int i
    for i in range(n):
        processes.append(Process(i, f"proc{i}"))

cdef void simulateCPUUsage():
    cdef int i
    for i in range(len(processes)):
        processes[i].cpu_usage = rand() % 100

# wrapper functions for shell.py [not anymore]
# def pyinitProcesses(int n):
#    initProcesses(n)

# def pysimulateCPUUsage():
#   simulateCPUUsage()
