; optimizer.asm - Windows x86-64 pure assembly
; input: test.asm
; output: test_optimized.asm
; Uses WinAPI only

default rel
extern CreateFileA
extern ReadFile
extern WriteFile
extern CloseHandle
extern ExitProcess

section .data
input_file db "test.asm",0
output_file db "test_optimized.asm",0
line_buf rb 256
prev_reg db 0
prev_val dq 0
bytes_read dq 0

section .text
global mainCRTStartup

mainCRTStartup:

    ; -----------------------
    ; Open input file
    mov rcx, input_file          ; LPCSTR lpFileName
    mov rdx, 0                   ; DWORD dwDesiredAccess = GENERIC_READ
    mov r8, 0                    ; DWORD dwShareMode
    mov r9, 0                    ; LPSECURITY_ATTRIBUTES lpSecurityAttributes
    push 3                        ; DWORD dwCreationDisposition = OPEN_EXISTING
    push 0                        ; DWORD dwFlagsAndAttributes = FILE_ATTRIBUTE_NORMAL
    call CreateFileA
    mov r12, rax                 ; input handle

    ; -----------------------
    ; Create output file
    mov rcx, output_file          ; LPCSTR lpFileName
    mov rdx, 0x40000000           ; GENERIC_WRITE
    mov r8, 0                     ; no share
    mov r9, 0                     ; security
    push 2                        ; CREATE_ALWAYS
    push 0                        ; normal attributes
    call CreateFileA
    mov r13, rax                  ; output handle

    ; -----------------------
    ; Initialize previous instruction
    mov byte [prev_reg], 0
    mov qword [prev_val], 0

read_loop:
    ; -----------------------
    ; Read one byte for simplicity
    mov rcx, r12                  ; hFile
    lea rdx, [line_buf]           ; buffer
    mov r8, 1                     ; bytes to read
    lea r9, [bytes_read]          ; pointer to variable for bytes read
    call ReadFile
    cmp qword [bytes_read], 0
    je finish

    ; -----------------------
    ; TODO: parse line_buf, detect "add REG, NUM"
    ; For testing, just write input to output

    mov rcx, r13                  ; hFile
    lea rdx, [line_buf]           ; buffer
    mov r8, 1                     ; bytes to write
    lea r9, [bytes_read]          ; pointer to bytes written
    call WriteFile

    jmp read_loop

finish:
    ; -----------------------
    ; Close handles
    mov rcx, r12
    call CloseHandle
    mov rcx, r13
    call CloseHandle

    ; Exit
    xor ecx, ecx
    call ExitProcess
