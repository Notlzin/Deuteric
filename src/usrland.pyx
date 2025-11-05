# usrland.pyx
# the userland part
# basically in OS: its a layer between kernel and the shell

import os, time
from shell import launchShell
from pacman_deuteric.repo import Repo

# process
cdef class Process:
    cdef str name
    cdef object exec_func
    cdef str status

    def __init__(self, name:str, exec_func) -> None:
        self.name = name
        self.exec_func = exec_func
        self.status = "OK"

    def run(self):
        print(f"[usrland.pyx]: starting process: '{self.name}'.")
        self.status = "RUNNING"
        try:
            if callable(self.exec_func):
                self.exec_func()
        except Exception as ex:
            print(f"[usrland.pyx] process '{self.name}' crashed: {ex}")
        finally:
            self.status = "TERMINATED"
            print(f"[usrland.pyx] process '{self.name}' exited.\n")

cdef class UsrLand:
    cdef dict fs
    cdef list proc_table
    cdef object repo
    cdef bint env_ready

    def __init__(self):
        self.fs = {}
        self.proc_table = []
        self.repo = Repo()
        self.env_ready = <bint>False
    def mountFs(self):
        self.fs["/usr"] = {}
        self.fs["/bin"] = {}
        print("[usrland.pyx] mounted fs: /usr and /bin")

    def registerProgram(self, name:str, func):
        # register binary-like command
        self.fs['/bin'][name] = func
        print(f"[usrland.pyx] registered program: '{name}'")

    def startProgram(self, name:str):
        if name not in self.fs['/bin']:
            print(f"[usrland.pyx] command: '{name}' unfound. error: {hex(len('ERROR_CMD_UNFOUND'))}")
            return
        prog = Process(name, self.fs['/bin'][name])
        self.proc_table.append(prog)
        prog.run()

    def listProcesses(self):
        print("[usrland.pyx] proccess table:")
        for proc in self.proc_table:
            print(f" - {proc.name}({proc.status})")

    def initEnv(self):
        print("[usrland.pyx] intializing environment...")
        self.mountFs()
        self.env_ready =  <bint>True

        # register programs
        self.registerProgram("pacman", lambda: os.system("python pacman.py"))
        self.registerProgram("repoList", lambda: self.repo.listPackages()) # type: ignore

        print("[usrland.pyx] environment is ready for user access.")

cpdef void startUsrland():
    print("[usrland.pyx] booting into user space...")
    time.sleep(0.2)
    env = UsrLand()
    env.initEnv()
    # preload demo programs.
    env.startProgram("repoList")
    print("[usrland.pyx] transferring control to shell.pyx..\n")
    launchShell()
