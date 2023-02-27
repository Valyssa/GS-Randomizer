def prologue(rom, flags):
    
    if flags['PrologueSkip']:
        # Music
        rom.write_to_rom(0x0809d9f6+21*8, [0x2a])
    else:
        rom.write_to_rom(0x08891400,[0x4770])
    return
