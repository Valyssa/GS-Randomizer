	push {lr}

	;; Load map ID
	ldr r0, =0x02000400
	ldrb r0, [r0]

	;; Start a farewell cutscene
	cmp r0, #0x1
	beq FAREWELL

	;; Skips djinn tutorial
	cmp r0, #0x2
	beq DJINNTUTORIAL
	
	;; PCs, flags, and misc prologue stuff
	cmp r0, #0x5
	beq @PROLOGUE
	
@END:	
	pop {pc}

FAREWELL:
	;; Map -- Vale
	mov r2, #0x5
	ldr r1, =0x020086f8
	strb r2, [r1]
	;; Door -- Vale entrance
	mov r2, #0xc
	ldr r1, =0x02008574
	strb r2, [r1]
	b @END

DJINNTUTORIAL:	
	;; Skip djinn tutorial
	ldr r0, =MAPCODE
	ldr r1, =0x02009d70
	ldmia r0!, {r2-r3}
	stmia r1!, {r2-r3}
	b @END
	.pool
	
MAPCODE:
	;; Skip to collecting djinn
	ldr r4, =0x0200a215
	bx r4
	.pool
	
@PROLOGUE:
	;; Check if flags are already set
	ldr r0, =0x02000140
	ldrb r0, [r0]
	mov r1, #0x17
	and r0, r1
	cmp r0, r1
	beq @END

	;; Grown up Isaac; swap Machete with Short Sword; misc other stuff
	bl @SETUP
	;; Add Garet to party
	mov r0, #0x1
	bl ADDTOPARTY
	;; Set flags
	bl SETFLAGS
	;; Set sanctum warp
	bl SETSANCTUM
	b @END

@SETUP:
	ldr r4, =0x08077f71
	bx r4
	
ADDTOPARTY:
	ldr r4, =0x0807961d
	bx r4

SETSANCTUM:
	ldr r0, =0x02000404
	ldr r1, =0x00010009
	str r1, [r0]
	bx lr
	
SETFLAGS:
	ldr r0, =0x02000140
	ldr r1, =FLAGS
	ldmia r1!, {r3-r6}
	stmia r0!, {r3-r6}
	ldmia r1!, {r3-r6}
	stmia r0!, {r3-r6}
	ldmia r1!, {r3-r6}
	stmia r0!, {r3-r6}
	ldmia r1!, {r3-r6}
	stmia r0!, {r3-r6}
	bx lr

	.aligna
FLAGS:
	.word 0x07db7f17, 0xfd8d83ea, 0x00000007, 0xfa000000
	.word 0x00400000, 0x00000000, 0x00000000, 0x00000000
	.word 0x00000003, 0x00000000, 0x00000000, 0x00000000
	.word 0x00000000, 0x00000000, 0x00000000, 0x00010000
	.pool

