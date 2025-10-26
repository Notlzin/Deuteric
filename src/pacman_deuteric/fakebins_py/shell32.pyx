# fakebins/shell32.pyx #
VERSION_SHELL = "shell32|v1.0.0"

cpdef str getVersion():
    return <str>VERSION_SHELL

cpdef str doPatch():
    # fake patching on shell LOL #
    print("[shell32.dll & shell32.pyd] applying patch... done.")
