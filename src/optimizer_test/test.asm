; test.asm for testing optimizations ;

; consecutive additions to R1 (simplified via the optimizer) ;
ADD R1, 14
ADD R1, 7
ADD R1, 8
ADD R1, 52

; different registers, shouldnt merge for testing ;
MOV R3, 4
MOV R2, 9

; consecutive addition to R2 ;
ADD R2, 7
ADD R2, 6
ADD R2, 8
ADD R2, 14
ADD R2, 10

; random instruction ;
jmp start
