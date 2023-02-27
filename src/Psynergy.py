def defaults(rom):

    # Point to psynergy script
    rom.write_to_rom(0x08078056, [0x4801, 0x4700, 0x0, 0x0001, 0x0889])
    
