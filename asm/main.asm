	.gba
	.create "main.bin",0x08800000

	;; Randomizer stuff
	.org 0x08890000
	.include "psynergy.asm"

	.org 0x08890100
	.include "decompress.asm"

	.org 0x08890200		; Table
	.org 0x08890350		; Scripts
	.include "djinn.asm"

	.org 0x08890800
	.include "dialogue.asm"

	.org 0x08890900
	.include "maps.asm"

	.org 0x08890a00		; Table
	.org 0x08890a50		; Scripts
	.include "items.asm"

	.org 0x08890f00
	.include "retreat.asm"

	.org 0x08891400
	.include "prologue.asm"

	.org 0x08891600
	.include "avoid.asm"
	
	.close
