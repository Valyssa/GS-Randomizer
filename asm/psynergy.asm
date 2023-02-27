	mov r1, #0x95 ; Retreat
	mov r0, #0x0  ; Isaac
	bl TEACH
	mov r1, #0x8c ; Move
	mov r0, #0x0  ; Isaac
	bl TEACH
	mov r1, #0x8c ; Move
	mov r0, #0x1  ; Garet
	bl TEACH
	mov r1, #0xc  ; Growth
	mov r0, #0x1  ; Garet
	bl TEACH
	mov r1, #0x96 ; Avoid
	mov r0, #0x1  ; Garet
	bl TEACH
	mov r1, #0x8d ; Mindread
	mov r0, #0x2  ; Ivan
	bl TEACH
	mov r1, #0x4e ; Whirlwind
	mov r0, #0x2  ; Ivan
	bl TEACH
	mov r1, #0x5d ; Ply
	mov r0, #0x3  ; Mia
	bl TEACH
	ldr r2, =0x08078077
	bx r2

TEACH:
	ldr r2, =0x08078e29
	bx r2
	
	.pool
