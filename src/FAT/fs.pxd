# FAT/fs.pxd #
cdef class File:
    cdef public str Name
    cdef public bytes Content

cdef class Directory:
    cdef public str Name
    cdef public list Files
    cdef public list Dirs
    cdef public object parentDir

# global root and cwd
cdef Directory root
cdef Directory cwd
cwd = root

# directory operations
cpdef void mkdir(str Name)
cpdef void ls(str folderName)
cpdef void cd(str Name)
