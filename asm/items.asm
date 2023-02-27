	push {lr}
	ldr r0, =0x02000400
	ldrb r5, [r0]

	bl ITEMSWAP
	bl FLAGSWAP
	pop {pc}


READTABLE:
	ldr r1, =0x08890a00
	mov r0, #0x0
LOOP:	
	ldrb r3, [r1,r0]
	add r0, #0x2
	cmp r2, r3
	bne LOOP
	sub r0, #0x1
	ldrb r2, [r1,r0]
	bx lr

	.pool
	

ITEMSWAP:
	push {lr}
	cmp r5, #0x5
	beq CATCHBEADS
	cmp r5, #0x33
	beq EMPTYGLASS
	cmp r5, #0x40
	beq DRAGONSEYE
	cmp r5, #0x42
	beq ORBOFFORCE
	cmp r5, #0x4d
	beq FROSTJEWEL
	cmp r5, #0x56
	beq LIFTINGGEM
	cmp r5, #0x5e
	beq HALTGEM
	cmp r5, #0x6c
	beq BOATTICKET
	cmp r5, #0x6e
	beq ANCHORCHARM
	cmp r5, #0x75
	beq REDKEY
	cmp r5, #0x8a
	beq CLOAKBALL
	cmp r5, #0x97
	beq MYSTICDRAUGHT
	cmp r5, #0xa1
	beq CELLKEY
	cmp r5, #0xb6
	beq CARRYSTONE
	cmp r5, #0xb4
	beq BLACKORB
	pop {pc}

CATCHBEADS:
	mov r2, #0xcf
	bl READTABLE
	ldr r0, =0x02009ea4
	strb r2, [r0]
	pop {pc}

EMPTYGLASS:
	mov r2, #0xb9
	bl READTABLE	
	ldr r0, =0x0200b054
	strb r2, [r0]
	pop {pc}

DRAGONSEYE:
	mov r2, #0xe6
	bl READTABLE
	ldr r0, =0x02009BB2
	strb r2, [r0]
	ldr r0, =0x02009b70
	strb r2, [r0]
	pop {pc}


ORBOFFORCE:	
	mov r2, #0xc8
	bl READTABLE
	ldr r0, =0x0200b174
	strb r2, [r0]
	pop {pc}

FROSTJEWEL:	
	mov r2, #0xca
	bl READTABLE
	ldr r0, =0x0200ad9a
	strb r2, [r0]
	ldr r0, =0x0200ada4
	strb r2, [r0]
	pop {pc}

	
LIFTINGGEM:	
	mov r2, #0xcb
	bl READTABLE
	ldr r0, =0x0200d140
	strb r2, [r0]
	pop {pc}

HALTGEM:	
	mov r2, #0xcc
	bl READTABLE
	ldr r0, =0x0200a5cc
	strb r2, [r0]
	pop {pc}

BOATTICKET:	
	mov r2, #0xeb
	bl READTABLE
	ldr r0, =0x0200864c
	strb r2, [r0]
	pop {pc}

ANCHORCHARM:	
	mov r2, #0xe8
	bl READTABLE
	ldr r0, =0x02008216
	strb r2, [r0]
	ldr r0, =0x02008220
	strb r2, [r0]
	pop {pc}

REDKEY:	
	mov r2, #0xf3
	bl READTABLE
	ldr r0, =0x020092d6
	strb r2, [r0]
	ldr r0, =0x020092e8
	strb r2, [r0]
	ldr r0, =0x0200a192
	strb r2, [r0]
	pop {pc}

CLOAKBALL:
	mov r2, #0xcd
	bl READTABLE
	ldr r0, =0x02008646
	strb r2, [r0]
	ldr r0, =0x02008656
	strb r2, [r0]
	ldr r0, =0x0200c182
	strb r2, [r0]
	pop {pc}

MYSTICDRAUGHT:
	mov r2, #0xed
	bl READTABLE
	ldr r0, =0x0200c8dc
	strb r2, [r0]
	pop {pc}

CELLKEY:
	mov r2, #0xea
	bl READTABLE
	ldr r0, =0x020090d8
	strb r2, [r0]
	ldr r0, =0x020090ea
	strb r2, [r0]
	pop {pc}


CARRYSTONE:
	mov r2, #0xce
	bl READTABLE
	ldr r0, =0x0200f0d4
	strb r2, [r0]
	pop {pc}

BLACKORB:
	;; Beaten lighthouse?
	ldr r0, =0x02000174
	ldrb r1, [r0]
	mov r0, #0x80
	and r1, r0
	cmp r1, r0
	bne BLACKORB_END
	
	;; Overwrite end of script of conversation with Iodem
	;; Prevents setting flag
	ldr r2, =0x4770
	ldr r0, =0x02008468
	strh r2, [r0]

	;; Iodem gives Isaac Black Orb early
	ldr r0, =0x02008452
	ldr r1, =0x2000
	strh r1, [r0]
	ldr r1, =0x4800
	strh r1, [r0,#0x2]
	ldr r1, =0x4700
	strh r1, [r0,#0x4]
	ldr r1, =0x08890e01
	mov r2, #0x6
	str r1, [r0, r2]

	;; Prevent ladder exit
	ldr r0, =0x02009708
	ldr r1, =0x016160b4
	str r1, [r0]
	
BLACKORB_END:	
	pop {pc}

	.pool
	

FLAGSWAP:
	push {lr}

	mov r2, #0xeb
	cmp r5, #0x6c
	beq FLAG_GETBOATTICKET
	cmp r5, #0x6b
	beq FLAG_BOATTICKET

	mov r2, #0xed
	cmp r5, #0x97
	beq FLAG_GETMYSTICDRAUGHT
	cmp r5, #0x93
	beq FLAG_MYSTICDRAUGHT
	
	cmp r5, #0xb2
	beq FLAG_LALIVERO

	mov r2, #0xc8
	cmp r5, #0x42
	beq FLAG_GETORBOFFORCE
	cmp r5, #0x55
	beq FLAG_ORBOFFORCE
	
	pop {pc}

	
FLAG_GETBOATTICKET:
	;; Ensure can be bought if post ship
	ldr r3, =0x02000167
	ldrb r4, [r3]
	mov r1, #0x40
	bic r4, r1
	strb r4, [r3]
	;; Allow purchase if without item
	bl READTABLE	        ; Get swapped item value 
	bl CHECKITEM	        ; Item in inventory?
	mov r0, #0x20           ; Flag
	ldr r2, =0x02000154	; Address
	bl UPDATEFLAG	        ; Update flag accordingly
	pop {pc}

FLAG_BOATTICKET:
	;; Check if post ship -- beaten Kraken
	ldr r3, =0x02000165
	ldrb r4, [r3]
	mov r1, #0x8
	and r4, r1
	cmp r4, r1
	bne CONTINUE_BOATTICKET
	;; Ensure boat cannot be entered if post ship
	ldr r3, =0x02000167
	ldrb r4, [r3]
	mov r1, #0x40
	orr r4, r1
	strb r4, [r3]
	pop {pc}
CONTINUE_BOATTICKET:	
	bl CHECKITEM	        ; Item in inventory?
	mov r0, #0x20           ; Flag
	ldr r2, =0x02000154	; Address
	bl UPDATEFLAG	        ; Update flag accordingly
	pop {pc}


	
FLAG_GETMYSTICDRAUGHT:
	bl READTABLE
FLAG_MYSTICDRAUGHT:
	bl CHECKITEM
	mov r0, #0x01
	ldr r2, =0x02000226
	bl UPDATEFLAG
	pop {pc}

	
FLAG_LALIVERO:
	mov r4, #0x0
	mov r0, #0x80
	ldr r2, =0x02000174
	bl UPDATEFLAG	
	pop {pc}

	
FLAG_GETORBOFFORCE:
	bl READTABLE
FLAG_ORBOFFORCE:	
	bl CHECKITEM
	mov r0, #0x10
	ldr r2, =0x02000222
	bl UPDATEFLAG
	pop {pc}
	
	
CHECKITEM:
	;; INPUT:  r2 item number
	;; RETURN: r4 = 1 if have item, 0 otherwise
	push {lr}
	mov r4, #0x0 
	ldr r1, =0x020005d8
	ldr r6, =0x014c	; Loop over PCs
CHECKITEM_LOOP:
	mov r0, #0x0
	bl SLOT_LOOP
	add r1, r6
	add r4, #0x1
	cmp r4, #0x4
	blt CHECKITEM_LOOP
	mov r4, #0x0	; Don't have item
	pop {pc}
HAVE:
	mov r4, #0x1    ; Have item
	pop {pc}
SLOT_LOOP:
	ldrb r3, [r1,r0]
	cmp r3, r2
	beq HAVE
	add r0, #0x2
	cmp r0, #0x1e
	blt SLOT_LOOP
	bx lr


UPDATEFLAG:
	;;  INPUT: r0 flag
	;;         r2 memory
	;;         r4 true?
	ldrb r1, [r2]
	cmp r4, #0x0 ; false --> remove flag
	beq RMFLAG
ADDFLAG:
	orr r1, r0
	b UPDATEEND
RMFLAG:
	bic r1, r0
UPDATEEND:
	strb r1, [r2]
	bx lr


.org 0x08890e00
LALIVERO:
	; Finished default cutscene in house
	mov r0, #0x1e
	bl b4_1
	bl b4_2

	; Cutscene from outside
	mov r2, #0xf2
	bl READTABLE
	mov r0, r2
	mov r1, #0x0
	bl b2_1
	mov r0, #0xa
	bl b2_2

	; Add flag for event outside
	ldr r0, =0x02000177
	ldrb r1, [r0]
	add r1, #0x4
	strb r1, [r0]
	
	; Return
	pop {r0}
	bx r0

b4_1:
	ldr r4, =0x0808a011
	bx r4

b4_2:
	ldr r4, =0x0808a021
	bx r4
	
b2_1:
	ldr r4, =0x0808a061
	bx r4

b2_2:
	ldr r4, =0x0808a011
	bx r4

	.pool
