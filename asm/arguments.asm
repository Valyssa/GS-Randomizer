	.gba
	.arm
	.create "arguments.bin",0x0
	.word 0xe59f201c
	.word 0xe59f301c
	mov r1, r1, lsl #0x2
	ldr r2, [r2,r1]
	add r2, r2, r3
	mov r1, #0x0
	mov r3, #0x0
	stmia r0, {r1-r3}
	bx lr
	.word 0x08800000
	.word 0x0880a7f0
	.close
