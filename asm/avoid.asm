	;; .org 0x08891600
	ldr r1, =0x02000486
	ldrh r1, [r1]
	cmp r1, #0x0
	beq TEXTAVOIDOFF
TEXTAVOIDON:
	ldr r0, =0x922
	b CONTINUE1
	.pool
TEXTAVOIDOFF:
	ldr r0, =0x29e2
CONTINUE1:	
	mov r1, #0x1
	bl PRINT
	ldr r0, =0x0809b7d3
	bx r0
PRINT:
	ldr r4, =0x0801776d
	bx r4
	.pool

	.org 0x08891700
	;; Set step count
	ldr r5, =0x02000486
	ldrh r2, [r5]
	cmp r2, #0x0
	beq AVOIDON
AVOIDOFF:
	mov r2, #0x0
	b CONTINUE2
AVOIDON:
	mov r2, #0x1
CONTINUE2:
	strh r2, [r5]
	ldr r0, =0x0809b6e9
	bx r0
	.pool
