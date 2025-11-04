# kernel.pyx and also vibecoded LOL and ctrl+c and ctrl+v #
import sys
import time
from shell import launchShell
from procman cimport initProcesses
from memman cimport allocateMemory
from usrland cimport startUsrland # type: ignore

# entry point part #
def start(cpu=None,gpu=None):
    global _cpu, _gpu
    _cpu, _gpu = cpu, gpu

    print("\nstarting kernel...")
    time.sleep(0.2)

    print("initializing subsystems...")
    time.sleep(0.1)
    initProcesses(5)
    allocateMemory(200)
    print("Process Manager [ProcMan|procman.pyx]... OK")
    print("Memory Manager [MemMan|memman.pyx]... OK")
    print("File System [FS|FAT.fs.pyx]... OK")
    print("Network Stack [NetSt|NetSt.virtual_net.py]... OK\n")
    time.sleep(0.2)

    print("kernel ready. launching shell...\n")
    try:
        # hmmmm uhhh this is optional but lets do it #
        # sorry launchShell()..
        # launchShell()
        startUsrland()
    except KeyboardInterrupt:
        print("\nkernel interruption (0xAAAAA:warning). use 'exit' command in shell to shut kernel down.")
    except Exception as e:
        print(f"[KERNEL_PANIC] failed launching shell: {e}:{hex(172)}")
        sys.exit(1)
