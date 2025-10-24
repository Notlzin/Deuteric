# the FAT of this OS LOL, fs.pyx #
from FAT.fs cimport Directory, File, root, cwd

cdef class File:
    def __init__(self, str Name, bytes content=b""):
        self.Name = Name
        self.content = content

cdef class Directory:
    def __init__(self, str Name, parentDir=None):
        self.Name = Name
        self.Files = []
        self.Dirs = []
        self.parentDir = parentDir

# root dir #
cdef Directory root = Directory("/")

# current working dir (cwd) #
cdef Directory cwd = root

# dir ops #
cpdef void mkdir(str Name):
    # create new subdir on current dir (cwd) #
    global cwd
    for d in cwd.Dirs:
        if d.Name == Name:
            print(f"mkdir: cannot create directory '{Name}': file exists")
    newDir = Directory(Name, parentDir=cwd)
    cwd.Dirs.append(newDir)
    print(f"Directory '{Name}' created.")

cpdef void ls(str folderName):
    # lists content in cwd (current working directory) #
    global cwd
    target = cwd
    if folderName != "":
        for d in cwd.Dirs:
            if d.Name == folderName:
                target = d
                break
        else:
            print(f"ls_err: no such directory: {folderName}")

    print("Directories:")
    for d in target.Dirs:
        print(f"|-[D] {d.Name}")
    print("Files:")
    for f in target.Files:
        print(f"|-[F] {f.Name}")

cpdef void cd(str Name):
    # change current working dir #
    found = False
    global cwd
    if Name == "..":
        if cwd.parentDir is not None:
            cwd = <Directory>cwd.parentDir
            found = True
    elif Name == "/":
        cwd = root
    else:
        for d in cwd.Dirs:
            if d.Name == Name:
                cwd = d
                found = True
                break
        else:
            print(f"cd: no such directory: {Name}")

cpdef str GetCWDName():
    return cwd.Name
