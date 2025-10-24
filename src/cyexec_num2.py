#!/usr/bin/env python #
# testing ground also #
# cyexec.py #
# and yes unused to [unused-unused] #
import os, sys, subprocess, time, pyximport, importlib

# main function:loop #
def runCython(path):
    path = os.path.abspath(path)
    if not os.path.exists(path):
        print(f"[cyexec] file not found: {path}")
        return

    # allow .dy as alias for .pyx
    base, ext = os.path.splitext(path)
    if ext == ".dy":
        pyx_path = base + ".pyx"
        if not os.path.exists(pyx_path):
            os.rename(path, pyx_path)
        path = pyx_path
        base = base
    name = os.path.basename(base)

    build_dir = os.path.join(os.path.dirname(path), "__cycache__")
    os.makedirs(build_dir, exist_ok=True)
    target_stub = os.path.join(build_dir, f"{name}.pyd")

    # Vibe: pretend-build step (calls cython for visible output) but no heavy pip nonsense
    print(f"[cyexec.py] preparing to run {path}")
    print(f"[cyexec.py] compiling {name}.pyx -> {target_stub}")
    subprocess.run([sys.executable, "-m", "cython", "-3", path], check=False)

    # Install pyximport with our build cache so import will build if needed
    pyximport.install(language_level=3, build_dir=build_dir, inplace=False)

    # Ensure module dir is importable
    mod_dir = os.path.dirname(path) or os.getcwd()
    if mod_dir not in sys.path:
        sys.path.insert(0, mod_dir)
    if build_dir not in sys.path:
        sys.path.insert(0, build_dir)

    # Import the module (pyximport will compile+load)
    print(f"[cyexec.py] launching module:{name}...\n")
    try:
        mod = importlib.import_module(name)
    except Exception as e:
        print(f"[cyexec.py] import failed: {e}")
        return

    # Run entrypoint if present
    for entry in ("Boot", "main"):
        if hasattr(mod, entry):
            try:
                getattr(mod, entry)()
            except SystemExit:
                raise
            except Exception as e:
                print(f"[cyexec.py] error running {entry}(): {e}")
            return

    print(f"[cyexec.py] {name} imported (no Boot()/main() found).")

# main REAL loop #
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: cyexec.py <file.pyx|file.dy>")
        sys.exit(1)
    runCython(sys.argv[1])
