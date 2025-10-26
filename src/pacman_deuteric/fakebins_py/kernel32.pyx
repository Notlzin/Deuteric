# fakebins/kernel32.pyx #
# fake kernel32 before converting to DLL LOL #

#ifndef kernel32.pyx
#define kernel32.pyx
VERSION_KERNEL = "kernel32|v1.0.0.0"

cpdef str getVersion():
    return <str>VERSION_KERNEL

cpdef str getLocation():
    return <str>"location of kernel: root/kernel32"

cpdef void doPatch():
    # fake patching LOL #
    print("[kernel32.dll & kernel32.pyd] applying patch... done.")

# endif
