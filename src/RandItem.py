import random
import Router

def randomize_items(rom, flags, cheatfile, text):

    items = {}
    items['Catch Beads'] = 0xcf
    items['Empty Bottle'] = 0xb9
    items['Dragons Eye'] = 0xe6
    items['Orb of Force'] = 0xc8
    items['Frost Jewel'] = 0xca
    items['Lifting Gem'] = 0xcb
    items['Halt Gem'] = 0xcc
    items['Boat Ticket'] = 0xeb
    items['Anchor'] = 0xe8
    items['Red Key'] = 0xf3
    items['Cloak Ball'] = 0xcd
    items['Mystic Draught'] = 0xed
    items['Cell Key'] = 0xea
    items['Carry Stone'] = 0xce
    items['Black Orb'] = 0xf2
    items['Douse Drop'] = 0xc9
    
    if flags['Items']:
        print('Shuffling key items')
        random.seed(flags['Seed'])
        swaps = Router.swapper(flags['Seed'], cheatfile)
        set_boss_drop(rom, items, swaps)
    else:
        swaps = {ki : ki for ki in items.keys()}

    # Item table
    table = []
    for ki in list(items.keys())[:-1]: # Exclude Douse Drop
        table += [items[ki], items[swaps[ki]]]
    rom.write_to_rom(0x08890a00, table, byte_length=1)

    # Update text
    for i in [9042, 9044, 9045, 9046, 9048]:
        text.lines[i] = text.lines[i].replace('Cloak Ball', swaps['Cloak Ball'])
    text.lines[9043] = text.lines[9043].replace('Cloak{3}Ball', swaps['Cloak Ball']+'{3}')
        
def set_boss_drop(rom, items, swaps):
    bosses = {}
    # bosses['Bandit']        = 529914
    # bosses['Tret']          = 539826
    # bosses['Saturos']       = 537810
    bosses['KillerApe']     = 534030
    # bosses['LivingStatue']  = 538398
    # bosses['HydrosStatue']  = 538482
    bosses['Kraken']        = 537642
    bosses['Toadonpa']      = 539322
    bosses['StormLizard']   = 539658
    # bosses['TempestLizard'] = 539742
    bosses['Deadbeard']     = 539994
    
    # Don't drop Douse Drop
    rom.buffer[bosses['KillerApe']] = 0
    
    # Set new item for boss to drop
    for key in swaps.keys():
        if key in bosses.keys():
            rom.buffer[bosses[key]] = items[swaps[key]]
