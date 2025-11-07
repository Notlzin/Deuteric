; optimizer.asm — Deuteric Optimizer (pure FASM Linux ELF64)
; Build instantly:
;     fasm optimizer.asm optimizer
; Usage:
;     ./optimizer kernel.bin optimized.bin

format ELF64 executable 3
entry _start

segment readable writeable
    msg_start db "[optimizer]: Starting optimization...",10,0
    msg_read  db "[optimizer]: Reading input file...",10,0
    msg_write db "[optimizer]: Writing output file...",10,0
    msg_done  db "[optimizer]: Done optimizing.",10,0
    msg_usage db "usage: optimizer <input> <output>",10,0

    inbuf  rb 4096
    outbuf rb 4096

segment readable executable
_start:
    ; argc is at [rsp], argv[0] at [rsp+8], argv[1] at [rsp+16], argv[2] at [rsp+24]
    mov rbx, [rsp]
    cmp rbx, 3
    jl usage

    mov rsi, [rsp+16]    ; argv[1] input path
    mov rdi, [rsp+24]    ; argv[2] output path

    ; print start message
    mov rax, 1
    mov rdi, 1
    mov rsi, msg_start
    mov rdx, 38
    syscall

    ; open input file (O_RDONLY = 0)
    mov rax, 2
    mov rdi, rsi
    xor rsi, rsi
    syscall
    mov r12, rax      ; fd_in

    ; read 4KB into buffer
    mov rax, 0
    mov rdi, r12
    mov rsi, inbuf
    mov rdx, 4096
    syscall
    mov r13, rax      ; bytes read

    ; optimization pass: remove 0x90 (NOP)
    xor rcx, rcx
    xor rbx, rbx
.loop:
    cmp rcx, r13
    jge .done_opt
    mov al, [inbuf + rcx]
    cmp al, 0x90
    je .skip
    mov [outbuf + rbx], al
    inc rbx
.skip:
    inc rcx
    jmp .loop

.done_opt:
    ; open output file (O_WRONLY|O_CREAT|O_TRUNC = 577)
    mov rax, 2
    mov rdi, [rsp+24]
    mov rsi, 577
    mov rdx, 0644o
    syscall
    mov r12, rax      ; fd_out

    ; write result
    mov rax, 1
    mov rdi, r12
    mov rsi, outbuf
    mov rdx, rbx
    syscall

    ; print done
    mov rax, 1
    mov rdi, 1
    mov rsi, msg_done
    mov rdx, 29
    syscall

exit:
    mov rax, 60
    xor rdi, rdi
    syscall

usage:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg_usage
    mov rdx, 38
    syscall
    jmp exit
