import random

def randomize_battle_palettes(rom, seed, flags):
    if not flags['Palettes']:
        return

    random.seed(seed)
    for i in range(164):
        rom.write_to_rom(135033955+i*8, [random.randrange(0,11,2)], byte_length=1)
