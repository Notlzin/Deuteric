# the API for pacman.pyx #
# pacmanAPI.py #
import sys
sys.path.append(r"D:/Deuteric/src/pacman_deuteric/")

try:
    import pacman
except ImportError:
    import os
    sys.path.append(os.path.dirname(__file__))
    import pacman

from repo import Repo

repo = Repo()  # instantiate the repo

def main():
    if len(sys.argv) < 2:
        print("[pacmanAPI] Usage: pacmanAPI.py [install|remove|list|reset|repo-list] [package]")
        return

    cmd = sys.argv[1]
    pkg = sys.argv[2] if len(sys.argv) > 2 else None

    if cmd == "install" and pkg:
        if repo.getVer(pkg) is None:
            print(f"[pacmanAPI] package '{pkg}' not found in repo.")
            return
        pacman.resolveDeps(pkg)
        pacman.installPac(pkg)

    elif cmd == "remove" and pkg:
        pacman.removePac(pkg)

    elif cmd == "list":
        pacman.listInstalled()

    elif cmd == "reset":
        pacman.reset()

    elif cmd == "repo-list":
        repo.listPackages()

    else:
        print("[pacmanAPI] Invalid command or missing package.")

if __name__ == "__main__":
    main()
