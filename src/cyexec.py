# cyexec.py, wrapper launcher and yes vibecoded idrc this is just a damn hobby project #
# probably unused[yes its unused] #
import sys, subprocess, os, pyximport, importlib, shutil

# main function loop #
def runCython(file):
    # some things #
    name = os.path.splitext(os.path.basename(file))[0]
    fileDir = os.path.dirname(file) or os.getcwd()
    build_dir = "__cycache__"
    os.makedirs(build_dir, exist_ok=True)
    target = os.path.join(build_dir, f"{name}.pyd")

    # [fake]compiler output????? #
    print(f"[cyexec.py] compiling:{file} -> {target}")
    subprocess.run([sys.executable, "-m", "cython", "-3", file], check=False)
    print(f"[cyexec.py] building native extension for: {name}...")
    pyximport.install(language_level=3, inplace=True)

    # import module #
    mod = importlib.import_module(name=name)

    # finding the compiled one (.pyd or .so) #
    compiled = next(
        (f for f in os.listdir(os.path.dirname(file))
            if f.startswith(name)
            and (f.endswith(".pyd")
            or f.endswith(".so"))),
            None
        )
    if compiled:
        src = os.path.join(os.path.dirname(file),compiled)
        dst = os.path.join(build_dir,compiled)
        shutil.move(src=src,dst=dst)
        print(f"[cyexec.py] moved:{compiled} to {build_dir}/")

    # loading via pyximport package #
    pyximport.install(build_dir=build_dir, inplace=True)
    print(f"[cyexec.py] launching module:{name}...\n")
    __import__(name)

# main loop #
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: cyexec.py <file.pyx>")
    else:
        runCython(sys.argv[1])
