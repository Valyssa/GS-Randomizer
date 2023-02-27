/*
	Decompress maps and overwrite as needed.
	- Djinn
	- Dialogue
	- Maps
	- Items
*/		

	pop {r0}	; DECOMPRESSION SETUP, 	0x0808ab48
	ldr r3, =0x02000240
	mov r1, #0xe0
	lsl r1, r1, #0x01
	add r3, r3, r1
	mov r1, #0x0
	ldsh r3, [r3, r1]
	ldr r2, =0x0809f1a8
	lsl r3, r3, #0x03
	ldsh r0, [r3, r2]
	ldr r1, =0x02008000
	bl DECOMPRESS
	
	push {r1-r6} 	; OVERWRITE DECOMPRESSED MAP
	bl DJINN
	bl DIALOGUE
	bl MAPS
	bl ITEMS
	bl PROLOGUE
	pop {r1-r6}
	pop {r0}
	bx r0

DECOMPRESS:
	ldr r4, =0x08002fb1
	bx r4

DJINN:
	ldr r0, =0x08890351
	bx r0

DIALOGUE:
	ldr r0, =0x08890801
	bx r0

MAPS:
	ldr r0, =0x08890901
	bx r0

ITEMS:
	ldr r0, =0x08890a51
	bx r0

PROLOGUE:
	ldr r0, =0x08891401
	bx r0
	
	.pool
