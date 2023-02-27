	/* Prevent softlock when dialogue is supressed
	Overwritten by py scripts when not used.
	*/
	ldr r0, =0x02000400
	ldrb r5, [r0]

	cmp r5, #0x8f
	beq COLOSSO1
	cmp r5, #0x90
	beq COLOSSO2
	cmp r5, #0x91
	beq COLOSSO3
	cmp r5, #0x87
	beq @TOLBI		; 'Missing Person' cutscene

	
	bx lr

COLOSSO1:
	ldr r2, =0x02009bc5
	mov r3, #0xd0 	; say no
	strb r3, [r2]
	bx lr
	
COLOSSO2:
	ldr r2, =0x02009e5d
	mov r3, #0xd0 	; say no
	strb r3, [r2]
	bx lr
	
COLOSSO3:
	ldr r2, =0x0200a8f5
	mov r3, #0xd0 	; say no
	strb r3, [r2]
	bx lr

@TOLBI:
	ldr r2, =0x02000158
	ldrb r1, [r2]
	mov r3, #0x1
	orr r1, r3
	strb r1, [r2]
	bx lr
	.pool
