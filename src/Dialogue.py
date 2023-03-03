def dialogue(rom, flags):

    if flags['CutDialogue']:
        print('Supressing most dialogue')
        # Cutscene skip function: jump over keypad and debug mode checks
        rom.write_to_rom(0x080915F2, [0xE014])
    else:
        rom.write_to_rom(0x08890800, [0x4770])
        
    return
