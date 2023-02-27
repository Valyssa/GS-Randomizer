import random
import os
import sys
import hjson
sys.path.append('src')
from Rom import LocalRom
import Abilities
import Avoid
import Decompress
import Dialogue
import Enemies
import Items
import Prologue
import Psynergy
import RandClasses
import RandDjinn
import RandEquipment
import RandItem
import RandMusic
import RandPC
import RandSummons
import Retreat
import Utilities
import Text
import RandPortraits
import Nuzlocke
import RandSprites
import RandNames

def randomizer(flags):
    
    # Load rom
    file = flags['File']
    rom = LocalRom(file)

    # Print seed
    print('Seed', flags['Seed'])

    # Log directory
    cheatdir = './cheat'
    os.makedirs(cheatdir, exist_ok=True)

    # Log file
    cheatfile = '{}/cheater_{}.txt'.format(cheatdir, flags['Seed'])
    if os.path.isfile(cheatfile):
        os.remove(cheatfile)

    # Load hack
    hack = Utilities.open_bin('asm/main.bin')
    rom.buffer += hack

    ###################
    # Decompress Text #
    ###################

    text = Text.decompress(rom)

    ######################
    # Pointers, QOL, ... #
    ######################

    Psynergy.defaults(rom)
    Decompress.decompress(rom)
    Dialogue.dialogue(rom, flags)
    Retreat.retreat(rom, flags)
    Avoid.avoid(rom, text, flags)
    Prologue.prologue(rom, flags)
    
    ############################
    # Randomize/Shuffle tables #
    ############################

    Abilities.randomize_abilities(rom, flags, text)
    Enemies.enemy_mod(rom, flags, text)
    Items.item_mod(rom, flags, text)
    RandItem.randomize_items(rom, flags, cheatfile, text)
    djinn = RandDjinn.randomize_djinn(rom, flags, cheatfile, text)
    RandPC.randomize_pc(rom, flags, cheatfile)
    RandClasses.randomize_classes(rom, flags, cheatfile, text)
    RandEquipment.randomize_equipment(rom, flags, cheatfile, text)
    RandMusic.randomize_music(rom, flags)
    RandSprites.randomize_battle_palettes(rom, flags['Seed'], flags)
    RandPortraits.randomize_party_portraits(rom, flags['Seed'], flags)
    Nuzlocke.ironman(rom, flags)
    Nuzlocke.expensive_inns(rom, flags)
    Nuzlocke.summon_requirements(rom, flags)
    Nuzlocke.luck_growth(rom, flags)
    RandSummons.randomize_summons(rom, flags, cheatfile, djinn)
    RandNames.random_party_names(rom, text, flags['Seed'], flags)

    ##############
    # Patch Text #
    ##############

    text.write()

    ###########
    # Outputs #
    ###########

    # Write rom
    output = 'patched_{}'.format(flags['Seed'])
    rom.write_to_file(output+'.gba')

    # Write settings
    with open(output+'.json', 'w') as file:
        hjson.dump(flags, file, indent=4)


def main():
    if len(sys.argv) > 2:
        print('Usage: python randomizer.py [template.json]')
        sys.exit()
    elif len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as file:
            flags = hjson.load(file)
    else:
        flags = {}
        flags['File'] = 'GOLDEN_SUN_A_AGSE00.gba'
        flags['Seed'] = random.randint(0, 999999)
        flags['CutDialogue'] = True
        flags['Items'] = True
        flags['PrologueSkip'] = True
        flags['Music'] = True
        flags['Coins'] = 1
        flags['Exp'] = 1
        flags['Djinn'] = {'Djinn': True,
                          'Stats': True}
        flags['Summons'] = {'Djinn': True,
                            'Power': True}
        flags['Equipment'] = {'Equipping': True,
                              'Cursed': True,
                              'Effects': True,
                              'Unleashes': True,
                              'Uses': True,
                              'Price': True,
                              'Attack': True,
                              'Defense': True}
        flags['Classes'] = {'Stats': True,
                            'Psynergy': 'Random',         # Choices: None, 'Random', 'Skillsets'
                            'Levels': {'Random': True,
                                       'Noise': True}}
        flags['PC'] = {'Elements': True,
                       'Stats': True,
                       'Levels': {'Isaac': 1,
                                  'Garet': 1,
                                  'Ivan':  4,
                                  'Mia':   10}}

    randomizer(flags)


if __name__ == '__main__':
    main()
