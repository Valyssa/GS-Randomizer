import random
from Table import Table
import Abilities

# Vanilla Djinn encounter table
djinn_encounters = [[0x168, 0x168, 0x168, 0x169, 0x169, 0x169, 0x16a],
                    [0x16d, 0x16d, 0x16d, 0x16e, 0x16f, 0x16f, 0x170],
                    [0x173, 0x173, 0x174, 0x174, 0x174, 0x175, 0x175],
                    [0x178, 0x178, 0x179, 0x179, 0x179, 0x17a, 0x17b]]

class Djinn(Table):
    def __init__(self, buffer, name, elem, num):
        self.buffer = buffer
        self.address = 0x8926c + elem*0xf0 + num*0xc

        self.name = name
        self.elem = elem
        self.num = num

        self._offsets = {}
        self._offsets['Ability'] = 0x0
        self._offsets['Stats']   = 0x4

        self.ability = self._read_ability()
        self.stats   = self._read_stats()
        
    def _read_ability(self):
        return self.read(self.address, size=2)

    def _read_stats(self):
        address = self.address + self._offsets['Stats']
        stats = {}
        stats['HP']      = self.read(address)
        stats['PP']      = self.read(address+1)
        stats['Attack']  = self.read(address+2)
        stats['Defense'] = self.read(address+3)
        stats['Agility'] = self.read(address+4)
        stats['Luck']    = self.read(address+5)
        return stats

    def _write_ability(self):
        self.patch(self.ability, self.address, size=2)

    def _write_stats(self):
        address = self.address + self._offsets['Stats']
        self.patch(self.stats['HP'     ], address)
        self.patch(self.stats['PP'     ], address+1)
        self.patch(self.stats['Attack' ], address+2)
        self.patch(self.stats['Defense'], address+3)
        self.patch(self.stats['Agility'], address+4)
        self.patch(self.stats['Luck'   ], address+5)

    def write(self):
        self._write_ability()
        self._write_stats()

        
def randomize_djinn(rom, flags, cheatfile, text):
    seed = flags['Seed']
    flag = flags['Djinn']
    
    names = ['Flint', 'Granite', 'Quartz', 'Vine', 'Sap', 'Ground', 'Bane',
             'Fizz', 'Sleet', 'Mist', 'Spritz', 'Hail', 'Tonic', 'Dew',
             'Forge', 'Fever', 'Corona', 'Scorch', 'Ember', 'Flash', 'Torch',
             'Gust', 'Breeze', 'Zephyr', 'Smog', 'Kite', 'Squall', 'Luff']

    djinn = {}
    djinn_list = []
    for i, ni in enumerate(names):
        djinn[ni] = Djinn(rom.buffer, name=ni, elem=int(i/7), num=i%7)
        djinn_list.append(djinn[ni])

    # Randomize djinn
    if flag['Djinn']:
        print('Shuffling djinn')
        random.seed(seed)
        values = list(djinn.values())
        random.shuffle(values)
        for ki, vi in zip(djinn.keys(), values):
            djinn[ki] = vi

    # Order assigned Djinn battles from weak to strong in approximate order of meeting them
    if flag['DjinnBattles']:
        print('Ordering Djinn Battles')
        i=0
        for djinni in djinn.values():
            battle = djinn_encounters[djinni.elem][i%7]
            rom.write_to_rom(0x9D104+(djinni.elem*0x1C)+(djinni.num*2), [battle], byte_length=2)
            # print(djinni.name, battle)
            i+=1

    # Randomize stat boosts
    if flag['Stats']:
        print('Shuffling djinn stat boosts')
        random.seed(seed)
        randomize_stats(djinn)

    # Randomize Djinn abilities
    if flag['DjinnAbilities']:
        attacking_djinn = ['Flint', 'Sap', 'Bane', 'Sleet', 'Mist', 'Hail', 'Fever', 'Scorch', 'Torch', 'Gust', 'Smog', 'Squall']
        effect_djinn = ['Granite', 'Quartz', 'Vine', 'Ground', 'Tonic', 'Dew', 'Forge', 'Corona', 'Flash', 'Breeze', 'Zephyr', 'Kite', 'Luff']
        recovery_djinn = ['Fizz', 'Spritz', 'Ember']
        unfit_abilities = [99, 100, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 116, 117, 118, 128, 129, 191,
                           250, 251, 252, 253, 254, 255, 256, 257, 258, 267, 268, 269, 270] # Items, duplicates, non-functional and weak abilities
        all_abilities = Abilities.get_abilities(rom, text)
        attacking_abilities = []
        effect_abilities = []
        recovery_abilities = []
        for ability in all_abilities:
            if ability.index not in unfit_abilities:
                if ability.type%16 == 3 or ability.type%16 == 4: # Added Damage or Multiplier
                    attacking_abilities.append(ability)
                elif ability.type%16 == 2 or ability.type%16 == 7: # Effect Only or Effect Only (goes first)
                    effect_abilities.append(ability)
                elif ability.type%16 == 1 or ability.type%16 == 11: # Healing or Psynergy Recovery
                    recovery_abilities.append(ability)
        random.shuffle(attacking_abilities) # Shuffle list so we can pop first element
        random.shuffle(effect_abilities)
        random.shuffle(recovery_abilities)
        for dj in djinn_list:
            if dj.name in attacking_djinn:
                new_ability = attacking_abilities.pop(0)
                dj.ability = new_ability.index
                text.lines[1638 + dj.elem*20 + dj.num] = str("Unleashes " + new_ability.name)
            elif dj.name in effect_djinn:
                new_ability = effect_abilities.pop(0)
                dj.ability = new_ability.index
                text.lines[1638 + dj.elem*20 + dj.num] = str("Unleashes " + new_ability.name)
            elif dj.name in recovery_djinn:
                new_ability = recovery_abilities.pop(0)
                dj.ability = new_ability.index
                text.lines[1638 + dj.elem*20 + dj.num] = str("Unleashes " + new_ability.name)
            dj.write()
        print("Djinn abilities randomized")
            
    # Update hack
    table = []
    for di in djinn.values():
        table += [di.elem, di.num]
    rom.write_to_rom(0x08890200, table, byte_length=1)

    # Flint update
    rom.buffer[0xabe62] = djinn['Flint'].elem
    rom.buffer[0xabe64] = djinn['Flint'].num
    rom.buffer[0xabe6c] = djinn['Flint'].elem
    rom.buffer[0xabe6e] = djinn['Flint'].num

    # Flint text
    def replace_flint_element(t, idx):
        tl = t.split('Venus')
        elements = ['Venus', 'Mercury', 'Mars', 'Jupiter']
        return tl[0] + elements[idx] + tl[1]
    
    text.lines[3156] = replace_flint_element(text.lines[3156], djinn['Flint'].elem)
    text.lines[3172] = replace_flint_element(text.lines[3172], djinn['Flint'].elem)
    
    # Print cheat file
    print_djinn_swap(djinn, cheatfile)

    return djinn


def randomize_stats(djinn):
    keys = list(djinn.values())[0].stats.keys()
    stats = [[] for _ in keys]
    for di in djinn.values():
        for i, ki in enumerate(keys):
            stats[i].append(di.stats[ki])

    for i in range(len(keys)):
        random.shuffle(stats[i])

    for i, di in enumerate(djinn.values()):
        for j, kj in enumerate(keys):
            di.stats[kj] = stats[j][i]
        

def print_djinn_swap(djinn, cheatfile):
    size = 7
    with open(cheatfile,'a') as file:
        file.write('\n\n\n\n\n')
        file.write('=====\n')
        file.write('DJINN\n')
        file.write('=====\n')
        file.write('\n\n')
        file.write('Djinn'.ljust(size)+' became  '+' ???\n')
        file.write('------------------------\n')
        for i, (ki, vi) in enumerate(djinn.items()):
            if i%7 == 0: file.write('\n')
            file.write(str(ki.ljust(size))+'  <----  '+str(vi.name.ljust(size))+'\n')
        file.write('\n')
