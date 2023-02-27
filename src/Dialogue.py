def dialogue(rom, flags):

    if flags['CutDialogue']:
        print('Supressing most dialogue')
        rom.write_to_rom(0x08092F84, [0x4770]) # Text box
        rom.write_to_rom(0x08092C40, [0x4770]) # Yes/No (?)
        rom.write_to_rom(0x08091C7C, [0x4770]) # Yes/No (?)
        rom.write_to_rom(0x080931ec, [0x4770]) # Multiple text boxes
    else:
        rom.write_to_rom(0x08890800, [0x4770])
        
    return
