; optimizer.asm
; VIBE to the CODED.
format ELF64 executable
entry _start

segment readable writeable
    py_lib db "/usr/lib/x86_64-linux-gnu/libpython3.13.so",0
    py_init db "Py_Initialize",0
    py_run db "PyRun_SimpleString",0
    py_fin db "Py_Finalize",0
    pycode db "print('Deuteric inline Python!')",0

segment readable executable
    extern dlopen
    extern dlsym
    extern dlclose

_start:
    ; rdi = path, rsi = RTLD_NOW (2)
    mov rdi, py_lib
    mov rsi, 2
    call dlopen
    mov rbx, rax

    ; get function pointers
    mov rdi, rbx
    mov rsi, py_init
    call dlsym
    call rax

    mov rdi, rbx
    mov rsi, py_run
    call dlsym
    mov rdi, pycode
    call rax

    mov rdi, rbx
    mov rsi, py_fin
    call dlsym
    call rax

    ; exit
    mov rax, 60
    xor rdi, rdi
    syscall
