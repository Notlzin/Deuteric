# shell.py, basically removing the old launchShell into shell.py #
import time, sys
from procman cimport simulateCPUUsage, processes
from memman cimport totalMem, usedMem
from FAT.fs cimport File, Directory, mkdir, ls, cd
import FAT.fs as pyfs

def buildPrompt(user="[root]", distro="deuteric", cwd="~"):
    # folder name changing #
    folder_name = "~"
    try:
        # if cwd is a string path
        if isinstance(cwd, str):
            # keep last path component, treat "/" as root
            if cwd == "/" or cwd == "":
                folder_name = "/"
            else:
                folder_name = cwd.split("/")[-1] or "/"
        else:
            # not a str: try to get Name (cdef attr) or name (py attr)
            folder_name = getattr(cwd, "Name", None) or getattr(cwd, "name", None)
            if folder_name is None:
                # fallback to str(cwd)
                folder_name = str(cwd)
            # show "/" as "~" if the root has Name == "/"
            if folder_name == "/":
                folder_name = "/"
    except Exception:
        folder_name = "~"

    # ANSI colors (optional) also this is GPT-5mini LOL #
    CYAN = "\033[36m"
    # YELLOW = "\033[33m"
    RESET = "\033[0m"
    GREEN = "\033[32m"
    BRIGHT_GREEN = "\033[92m"
    RED = "\033[31m"
    BRIGHT_RED = "\033[91m"
    # BLUE = "\033[34m"
    BRIGHT_BLUE = "\033[94m"

    # build multiline prompt thingy #
    top = f"{CYAN}{user}{RESET}"
    topline = f"{GREEN}╭─{RESET}"
    pipeline = f"{BRIGHT_RED}│{RESET}"
    inputLine = f"{CYAN}╰─> {BRIGHT_BLUE}{distro}:{folder_name}$ {RESET}"

    # combine with newlines to look it more... uhh idk [note: better] #
    return f"{topline}{top}\n{pipeline}\n{inputLine}"

def launchShell():
    cwd='~'
    while True:
        try:
            try:
                currDir = pyfs.GetCWDName()
            except Exception:
                currDir = "~"
            prompt=buildPrompt(cwd=currDir)
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
            elif cmd.startswith("ls "):
                folderName = cmd[len("ls "):].strip()
                if folderName:
                    ls(folderName)
                else:
                    ls("") # empty thing WOOHOO #
            elif cmd.startswith("mkdir "):
                folderName = cmd[len("mkdir "):].strip()
                if folderName:
                    mkdir(folderName)
                else:
                    print("mkdir_err: missing operand")
            elif cmd.startswith("cd "):
                folderName = cmd[len("cd "):].strip()
                if folderName:
                    cd(folderName)
                else:
                    print("cd_err: missing operand")
            elif cmd == "exit":
                print("shutting down the kernel...")
                sys.exit(0)
            else:
                print(f"command not found: {cmd} error: 0x0000000F")
        except KeyboardInterrupt:
            print("\nnote: use 'exit' command to exit kernel.")
