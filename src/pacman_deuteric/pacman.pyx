# pacman.pyx for trit #

# fake database LOL #
cdef list installedPac = []

# API core #
cpdef void installPac(str package):
    # install a fake package into Deuteric shell #
    global installedPac
    if package in installedPac:
        print(f"[pacman:trit] package '{package} already existing. error: {hex(len('existing_error_pkg'))}")
    installedPac.append(package)
    print(f"[pacman:trit] installing: '{package}'..")
    # pretend working #
    print(f"[pacman:trit] package '{package}' has installed successfully.")

cpdef void removePac(str package):
    # removes a fake package #
    global installedPac
    if package not in installedPac:
        print(f"[pacman:trit] package '{package}' is unfounded. err: {hex(len('unfound_pkg_err'))}")
    installedPac.remove(package)
    print(f"[pacman:trit] package '{package}' removed.")

cpdef void listInstalled():
    # lists all installed packages #
    print("[pacman:trit] installed packages:")
    if not installedPac:
        print("     (none)")
    else:
        for package in installedPac:
            print(f"    -{package}")

cpdef bint isInstalled(str package):
    # return true if the package is installed aka installer checker #
    cdef bint result = package in installedPac
    return result

cpdef void resolveDeps(str package):
    # fake dependency resolver #
    print(f"[pacman:trit] resolving dependencies for: '{package}'")
    # connected with repo.py or manifest.json #
    print(f"[pacman:trit] dependencies resolved.")

# resets packages part #
cpdef void reset():
    # clear all installed packages [like a factory reset] #
    global installedPac
    installedPac.clear()
    print("[pacman:trit] all packages cleared (resetted).")
