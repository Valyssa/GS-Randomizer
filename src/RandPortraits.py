import random

party_portraits = [0x80367E6, 0x80367EE, 0x80367F6, 0x80367FA]

def randomize_party_portraits(rom, seed, flags):
    if not flags['Portraits']:
        return

    random.seed(seed)
    valid_portraits = [*range(0,8)] + [*range(17,41)]
    # print(valid_portraits)
    for i in range(len(party_portraits)):
        rom.write_to_rom(party_portraits[i], [random.choice(valid_portraits)], byte_length=1)
    print("Randomizing party portraits")