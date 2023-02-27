	.gba
	.arm
	.create "text.bin",0x0
	ldmia r0, {r1-r3}
	ldrb r1, [r2], #0x1
	stmia r0, {r1-r3}
	mov r0, r1
	bx lr
	.close
