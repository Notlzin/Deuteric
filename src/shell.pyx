# shell.py, basically removing the old launchShell into shell.py #
import time, sys, random
from procman cimport simulateCPUUsage, initProcesses, processes
from memman cimport totalMem, usedMem

# build that kali linux style looking prompt thing
def buildPrompt(user="|root|", distro="deuteric", cwd="~"):
    # ANSI colors (optional) also this is GPT-5mini LOL #
    CYAN = "\033[36m"
    YELLOW = "\033[33m"
    RESET = "\033[0m"

    # build multiline prompt thingy #
    top = f"{CYAN}{user}{RESET}"
    pipeline = f"│"
    inputLine = f"╰─> {YELLOW}{distro}:{cwd}$ {RESET}"

    # combine with newlines to look it more... uhh idk #
    return f"{top}\n{pipeline}\n{inputLine}"

def launchShell():
    cwd='~'
    while True:
        try:
            prompt=buildPrompt(cwd=cwd)
            cmd = input(prompt).strip()
            if cmd == "help":
                print("help:commands: help, echo, time, ps, mem, exit")
            elif cmd.startswith("echo "):
                print(cmd[5:])
            elif cmd == "time":
                print(time.ctime())
            elif cmd == "ps":
                simulateCPUUsage()
                for p in processes:
                    print(f"{p.pid:02d} {p.name} CPU:{p.cpu_usage}%")
            elif cmd == "mem":
                print(f"memory-usage: {usedMem}/{totalMem} MB")
            elif cmd == "exit":
                print("shutting down the kernel...")
                sys.exit(0)
            else:
                print(f"command not found: {cmd} error: 0x0000000F")
        except KeyboardInterrupt:
            print("\nnote: use 'exit' command to exit kernel.")
