	push {lr}

	; Load map ID
	ldr r0, =0x02000400
	ldrb r6, [r0]

	bl VENUS
	bl MERCURY
	bl MARS
	bl JUPITER
	bl @OVERWORLD
	
	pop {pc}

	.pool

TABLELOOKUP:
	/*
	INPUT
	  r2 - nth halfword of table
	RETURNS
	  r3 - Element (0-3)
	  r4 - Djinn (0-6)
	*/
	ldr r1, =0x08890200
	mov r3, #0x2
	mul r2, r3
	ldrb r3, [r1,r2]
	add r2, #0x1
	ldrb r4, [r1,r2]
	bx lr

	
DJINNVALS:	
	/*
	INPUT
	  r2 - nth halfword of table
	RETURNS
	  r1 - Sprite (0x5a-0x5d)
	  r2 - Flag
	  r3 - Element
	  r4 - Djinn (0-6)
	  r5 - Flag-Offset
	*/
	push {lr}

	bl TABLELOOKUP

	; Sprite
	mov r1, #0x5a
	add r1, r3

	; Flag
	mov r5, #0x14
	mul r5, r3
	add r5, r4
	mov r2, #0x30
	add r2, r5
	pop {pc}
	
VENUS:
	push {lr}
	cmp r6, #0x24
	beq V2_GRANITE
	cmp r6, #0x45
	beq V3_QUARTZ
	cmp r6, #0x14
	beq V5_SAP1
	cmp r6, #0x17
	beq V5_SAP2
	cmp r6, #0x6b
	beq V6_GROUND
	cmp r6, #0x78
	beq V7_BANE
	pop {pc}

V2_GRANITE:
	mov r2, #0x1
	bl DJINNVALS
	ldr r0, =0x0200b2a8
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x02008278
	strb r3, [r0]
	strb r4, [r0,#0x2]
	pop {pc}

V3_QUARTZ:
	mov r2, #0x2
	bl DJINNVALS
	ldr r0, =0x0200b880
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x02008cc4
	strb r5, [r0]
	pop {pc}

V4_VINE:

V5_SAP1:
	mov r2, #0x4
	bl DJINNVALS
	ldr r0, =0x0200a24c
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x0200a3e4
	strb r1, [r0]
	strb r2, [r0,#0x2]
	pop {pc}

V5_SAP2:	
	mov r2, #0x4
	bl DJINNVALS
	ldr r0, =0x2009710
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x2008d78
	strb r3, [r0]
	strb r4, [r0,#0x2]
	ldr r0, =0x02008ff2
	strb r2, [r0]
	pop {pc}

V6_GROUND:
	mov r2, #0x5
	bl DJINNVALS
	ldr r0, =0x2009b74
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x2009c4c
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x2008034
	strb r3, [r0]
	strb r4, [r0,#0x2]
	pop {pc}

V7_BANE:
	mov r2, #0x6
	bl DJINNVALS
	ldr r0, =0x200ab78
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x20089e0
	strb r3, [r0]
	strb r4, [r0,#0x2]

	mov r3, #0xf
	ldr r0, =0x0200ae2a
LOOP1:	
	strb r2, [r0]
	add r0, #0xc
	sub r3, #0x1
	cmp r3, #0x0
	bne LOOP1
	
	pop {pc}
	
	
MERCURY:
	push {lr}
	cmp r6, #0x36
	beq M1_FIZZ
	cmp r6, #0x37
	beq M2_SLEET
	cmp r6, #0x48
	beq M3_MIST
	cmp r6, #0x53
	beq M4_SPRITZ
	cmp r6, #0xa1
	beq M6_TONIC
	cmp r6, #0xaa
	beq M7_DEW
	pop {pc}

M1_FIZZ:
	mov r2, #0x7
	bl DJINNVALS
	ldr r0, =0x200cbd8
	strb r3, [r0]
	strb r4, [r0,#0x2]
	ldr r0, =0x200cbd2
	strb r2, [r0]
	pop {pc}
	
M2_SLEET:
	mov r2, #0x8
	bl DJINNVALS
	ldr r0, =0x200e808
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x02008cc4
	strb r5, [r0]
	pop {pc}
	
M3_MIST:
	mov r2, #0x9
	bl DJINNVALS
	ldr r0, =0x2009a50
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x2008318
	strb r3, [r0]
	strb r4, [r0,#0x2]
	pop {pc}
	
M4_SPRITZ:
	mov r2, #0xa
	bl DJINNVALS
	ldr r0, =0x200cb38
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x02008034
	strb r5, [r0]
	pop {pc}
	
M6_TONIC:
	mov r2, #0xc
	bl DJINNVALS
	ldr r0, =0x200edd8
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x200cb6c
	strb r3, [r0]
	strb r4, [r0,#0x2]
	pop {pc}
	
M7_DEW:
	mov r2, #0xd
	bl DJINNVALS
	ldr r0, =0x2008c20
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x02008034
	strb r5, [r0]
	pop {pc}

	
MARS:
	push {lr}
	cmp r6, #0x1b
	beq R1_FORGE
	cmp r6, #0x34
	beq R2_FEVER
	cmp r6, #0x9c
	beq R4_SCORCH
	cmp r6, #0x87
	beq R5_EMBER
	cmp r6, #0xa5
	beq R6_FLASH
	cmp r6, #0xb2
	beq R7_TORCH
	pop {pc}

R1_FORGE:
	mov r2, #0xe
	bl DJINNVALS
	ldr r0, =0x020097cc
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x020089f6
	strb r5, [r0]
	pop {pc}

R2_FEVER:
	mov r2, #0xf
	bl DJINNVALS
	ldr r0, =0x200a9bc
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x2008034
	strb r3, [r0]
	strb r4, [r0,#0x2]
	pop {pc}
	
R3_CORONA:

R4_SCORCH:
	mov r2, #0x11
	bl DJINNVALS
	ldr r0, =0x200cbb8
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x2008034
	strb r3, [r0]
	strb r4, [r0,#0x2]
	pop {pc}

R5_EMBER:
	mov r2, #0x12
	bl DJINNVALS
	ldr r0, =0x2009460
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x2008034
	strb r3, [r0]
	strb r4, [r0,#0x2]
	pop {pc}

R6_FLASH:
	mov r2, #0x13
	bl DJINNVALS
	ldr r0, =0x2009760
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x02008318
	strb r5, [r0]
	pop {pc}

R7_TORCH:
	mov r2, #0x14
	bl DJINNVALS
	ldr r0, =0x2009a68
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x2008034
	strb r3, [r0]
	strb r4, [r0,#0x2]
	pop {pc}
	
JUPITER:	
	push {lr}
	cmp r6, #0x20
	beq J1_GUST
	cmp r6, #0x2e
	beq J2_BREEZE
	cmp r6, #0x3f
	beq J3_ZEPHYR
	cmp r6, #0x5a
	beq J4_SMOG
	cmp r6, #0x5e
	beq J5_KITE
	cmp r6, #0x95
	beq J6_SQUALL
	cmp r6, #0xaf
	beq J7_LUFF
	pop {pc}
	
J1_GUST:
	mov r2, #0x15
	bl DJINNVALS
	ldr r0, =0x2009708
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x2008110
	strb r3, [r0]
	strb r4, [r0,#0x2]
	pop {pc}

J2_BREEZE:
	mov r2, #0x16
	bl DJINNVALS
	ldr r0, =0x2008474
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x02008034
	strb r5, [r0]
	pop {pc}

	
J3_ZEPHYR:
	mov r2, #0x17
	bl DJINNVALS
	ldr r0, =0x200aa94
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x02008044
	strb r5, [r0]
	pop {pc}

J4_SMOG:
	mov r2, #0x18
	bl DJINNVALS
	ldr r0, =0x200a488
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x2008318
	strb r3, [r0]
	strb r4, [r0,#0x2]
	pop {pc}

J5_KITE:
	mov r2, #0x19
	bl DJINNVALS
	ldr r0, =0x200a2c4
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x2008cc4
	strb r3, [r0]
	strb r4, [r0,#0x2]


	mov r3, #0xe
	ldr r0, =0x0200a516
LOOP2:	
	strb r2, [r0]
	add r0, #0xc
	sub r3, #0x1
	cmp r3, #0x0
	bne LOOP2
	pop {pc}
	
	
J6_SQUALL:
	mov r2, #0x1a
	bl DJINNVALS
	ldr r0, =0x200c2e8
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x020089e0
	strb r5, [r0]
	pop {pc}

J7_LUFF:	
	mov r2, #0x1b
	bl DJINNVALS
	ldr r0, =0x200b754
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x02008cc4
	strb r5, [r0]
	pop {pc}

@OVERWORLD:
	cmp r6, #0x2
	beq OVERWORLDDJINN
	pop {pc}

OVERWORLDDJINN:	
	;; If no djinn, do Flint
	ldr r0, =0x02000046
	ldr r1, [r0]
	mov r2, #0x5
	ldr r2, [r0,r2]
	add r1, r2
	cmp r1, #0x0
	beq FLINT

	;; If have djinn, skip Flint scene! (even without Vine)
	ldr r0, =0x02009ca4
	ldr r1, =0x4770
	strh r1, [r0]
	
	; Vine
	mov r2, #0x3
	bl DJINNVALS
	ldr r0, =0x200db84
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x200e436
	strb r2, [r0]
	ldr r0, =0x2008064
	strb r5, [r0]
	ldr r0, =0x0200e3fa
	strb r2, [r0]
	ldr r0, =0x02008254
	strb r2, [r0]

	mov r1, #0xd0          ; Flint/Vine fix
	ldr r0, =0x0200825d
	strb r1, [r0]
	
	; Hail
	mov r2, #0xb
	bl DJINNVALS
	ldr r0, =0x200dbb4
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x200e44e
	strb r2, [r0]
	ldr r0, =0x20080fa
	strb r5, [r0]

	; Corona
	mov r2, #0x10
	bl DJINNVALS
	ldr r0, =0x200db9c
	strb r1, [r0]
	strb r2, [r0,#0x2]
	ldr r0, =0x200e442
	strb r2, [r0]
	ldr r0, =0x20080b2
	strb r5, [r0]
	
	pop {pc}

FLINT:
	mov r2, #0x0
	bl DJINNVALS

	ldr r0, =0x200db84
	strb r1, [r0]
	ldr r0, =0x02009d1e
	strb r3, [r0]
	strb r4, [r0,#0x2]
	ldr r0, =0x02009d28
	strb r3, [r0]
	strb r4, [r0,#0x2]
	ldr r0, =0x0200a214
	strb r3, [r0]
	strb r4, [r0,#0x2]
	ldr r0, =0x0200e3fa
	strb r2, [r0]
	ldr r0, =0x02008254
	strb r2, [r0]

	;; Name in text -- first time
	ldr r0, =0x2009ed8
	mov r1, #0xfc
	strb r1, [r0]
	ldr r0, =0x2009eda
	strb r2, [r0]
	mov r1, #0x30
	strb r1, [r0,#0x1]
	
	;; Name in text -- second time
	ldr r0, =0x200a044
	mov r1, #0xfc
	strb r1, [r0]
	ldr r0, =0x200a048
	strb r2, [r0]
	mov r1, #0x30
	strb r1, [r0,#0x1]

	pop {pc}
	.pool
