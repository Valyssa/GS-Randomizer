	;; Miscellaneous map edits
	push {lr}

	;; Load map ID
	ldr r0, =0x02000400
	ldrb r5, [r0]

	;; Set flag for Venus Lighthouse
	cmp r5, #0xb5
	beq VENUS_LIGHTHOUSE_ENTRY
	
	;; Set flag for overworld map
	cmp r5, #0x71
	beq CROSSBONE_ISLE
	
	;; Overworld stuff
	cmp r5, #0x2
	beq @OVERWORLD

	;; Lalivero
	cmp r5, #0xb2
	beq @LALIVERO
	
	pop {pc}

VENUS_LIGHTHOUSE_ENTRY:
	ldr r1, =0x02000077
	ldrb r2, [r1]
	mov r3, #0x3
	orr r2, r3
	strb r2, [r1]
	pop {pc}
	
CROSSBONE_ISLE:
	mov r3, #0x4
	ldr r1, =0x02000071
	ldrb r2, [r1]
	orr r2, r3
	strb r2, [r1]
	pop {pc}
	
@OVERWORLD:
	;; Flags -- Iodem giving Isaac Black Orb (near boat before Lalivero)
	;; Skip cutscene to prevent stealing the Black Orb with Retreat!
	ldr r1, =0x0200014b
	ldrb r2, [r1]
	mov r3, #0x20
	orr r2, r3
	strb r2, [r1]

	;; Move Bilibin Barracks to Crossbone Isle
	ldr r1, =0x0200dd94
	ldr r2, =0x011c
	strh r2, [r1]
	ldr r2, =0x14a8
	strh r2, [r1,#0xa]
	ldr r2, =0x0952
	strh r2, [r1,#0x12]

	;; Ensure you can return to Crossbone Isle if reached on Tolbi Ship
	ldr r1, =0x02000154
	ldrb r1, [r1]
	mov r2, #0x1
	and r1, r2
	cmp r1, r2
	beq CROSSBONE_ISLE
	
	pop {pc}

@LALIVERO:
	;; After lighthouse?
	ldr r1, =0x02000177
	ldrb r1, [r1]
	mov r2, #0x10
	and r1, r2
	cmp r1, r2
	bne @LALIVERO_END

	;; Move soldier blocking boat
	ldr r1, =0x020099f0
	mov r2, #0x67
	strb r2, [r1,#0xa]
	mov r2, #0xaa
	strb r2, [r1,#0x12]
	
@LALIVERO_END:
	pop {pc}
	
	.pool
