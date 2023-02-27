	/* Setup for Retreat
	Currently all maps are allowed except for Colosso maps.
	*/
	ldr r0, =0x02000400
	ldrb r0, [r0]
	cmp r0, #0x6d		; Boat
	beq NOTALLOWED
	cmp r0, #0x6e		; Boat
	beq NOTALLOWED
	cmp r0, #0x6f		; Boat
	beq NOTALLOWED
	cmp r0, #0x8f		; Colosso 1
	beq NOTALLOWED
	cmp r0, #0x90		; Colosso 2
	beq NOTALLOWED
	cmp r0, #0x91		; Colosso 3
	beq NOTALLOWED
ALLOWED:
	ldr r4, =0x0808e741
	bx r4
NOTALLOWED:	
	ldr r4, =0x0808e72d
	bx r4


	/* Updates Retreat location
	   - mainly for overworld Retreats
	   - tweak a few other Retreats

	NB. This script gets called from some, if not all, Yes/No
	questions too (e.g. Colosso). These should be skipped with
	CONTINUE.

	*/
.org 0x08890f40
	;; World Map only
	ldr r4, =0x02000400
	ldrb r4, [r4]
	cmp r4, #0x2
	beq SETUP
	;; OTHERWISE
	b COMPARE_MAPS
	
SETUP:
	push {r0-r5, lr}
	cmp r0, #0x0  ;; Say yes?
	bne SETUPEND
	mov r0, r8
	cmp r0, #0x95 ;; Retreat?
	bne SETUPEND

	;; Closes text box
	bl CONTINUE

	;; Load world map & update Retreat location
	bl WORLDMAP
	
SETUPEND:
	bl CONTINUE
	pop {r0-r5, pc}

CONTINUE:	
	ldr r4, =0x08019a55
	bx r4

WORLDMAP:
	ldr r4, =0x0809c139
	bx r4

.org 0x08890f80
UPDATE:
	ldr r1, =0x984
	cmp r0, r1
	beq SKIP

	;; Setup
	sub r0, r0, r3
	push {r1-r5}

	;; Compare r0
	b COMPARE_STRINGS
	
	
OVERWRITE:	
	ldr r1, =0x02000480
	strb r3, [r1,#0x2]
END:
	pop {r1-r5}
	add r0, r0, r3
SKIP:
	ldr r4, =0x08018791
	bx r4

COMPARE_MAPS:
	;; Change Retreat location for a few specific instances
	push {r1-r5}
	cmp r4, #0x4
	beq VALE_MAP
	cmp r4, #0x5
	beq VALE_MAP
	cmp r4, #0x6
	beq VALE_MAP
	cmp r4, #0x3a
	beq MERCURY_LIGHTHOUSE_AERIE
	cmp r4, #0x8a
	beq TOLBI_MAP
	cmp r4, #0x8b
	beq TOLBI_MAP
	pop {r1-r5}
	b CONTINUE

OVERWRITE_MAPS:
	ldr r1, =0x02000480
	strb r2, [r1]
	strb r3, [r1,#0x2]
	pop {r1-r5}
	b CONTINUE
	
MERCURY_LIGHTHOUSE_AERIE:
	mov r2, #0x39
	mov r3, #0xb
	b OVERWRITE_MAPS

TOLBI_MAP:
	mov r2, #0x87
	mov r3, #0x1
	b OVERWRITE_MAPS

VALE_MAP:
	mov r2, #0x5
	mov r3, #0xa
	b OVERWRITE_MAPS
	
COMPARE_STRINGS:
	cmp r0, #0xd
	beq SOL_SANCTUM

	cmp r0, #0xa
	beq VALE

	cmp r0, #0x10
	beq VAULT

	cmp r0, #0x14
	beq BILIBIN

	cmp r0, #0x3b
	beq BILIBIN_BARRICADE ;; NOW CROSSBONE ISLE

	cmp r0, #0x18
	beq KOLIMA
	
	cmp r0, #0x19
	beq KOLIMA_BRIDGE
	
	cmp r0, #0x1f
	beq IMIL
	
	cmp r0, #0x22
	beq MERCURY_LIGHTHOUSE
	
	cmp r0, #0x25
	beq FUSCHIN_TEMPLE
	
	cmp r0, #0x28
	beq XIAN
	
	cmp r0, #0x2a
	beq ALTIN
	
	cmp r0, #0x2c
	beq LAMA_TEMPLE

	cmp r0, #0x32
	beq KALAY
	
	cmp r0, #0x38
	beq KALAY_DOCKS
	
	cmp r0, #0x3f
	beq TOLBI
	
	cmp r0, #0x3a
	beq TOLBI_DOCKS
	
	cmp r0, #0x49
	beq GONDOWAN_PASSAGE
	
	cmp r0, #0x51
	beq SUHALLA
	
	cmp r0, #0x5e
	beq VENUS_LIGHTHOUSE

	cmp r0, #0x5a
	beq @LALIVERO

	cmp r0, #0x58
	beq BABI_LIGHTHOUSE
	
	cmp r0, #0x35
	beq LUNPA

	b END

SOL_SANCTUM:	
VALE:
	mov r3, #0x1
	b OVERWRITE

VAULT:
	mov r3, #0x3
	b OVERWRITE

BILIBIN:
	mov r3, #0x5
	b OVERWRITE

BILIBIN_BARRICADE:
	;; Replace with Crossbone Isle
	mov r3, #0x4c 
	b OVERWRITE

KOLIMA:
	mov r3, #0x7
	b OVERWRITE
	
IMIL:
	mov r3, #0x9
	b OVERWRITE
	
MERCURY_LIGHTHOUSE:
	mov r3, #0xa
	b OVERWRITE

KOLIMA_BRIDGE:	
	mov r3, #0xb
	b OVERWRITE
	
FUSCHIN_TEMPLE:	
	mov r3, #0xc
	b OVERWRITE
	
XIAN:	
	mov r3, #0xe
	b OVERWRITE
	
ALTIN:	
	mov r3, #0x10
	b OVERWRITE
	
LAMA_TEMPLE:
	mov r3, #0x11
	b OVERWRITE
	
KALAY:
	mov r3, #0x14
	b OVERWRITE
	
KALAY_DOCKS:
	mov r3, #0x15
	b OVERWRITE
	
TOLBI_DOCKS:
	mov r3, #0x16
	b OVERWRITE
	
TOLBI:
	mov r3, #0x17
	b OVERWRITE
	
GONDOWAN_PASSAGE:
	mov r3, #0x19
	b OVERWRITE
	
SUHALLA:
	mov r3, #0x1b
	b OVERWRITE
	
@LALIVERO:
	mov r3, #0x1e
	b OVERWRITE

BABI_LIGHTHOUSE:
	mov r3, #0x1f
	b OVERWRITE

VENUS_LIGHTHOUSE:
	mov r3, #0x20
	b OVERWRITE
	
LUNPA:
	mov r3, #0x22
	b OVERWRITE

	.pool
