import random
from Table import Table

class SummonCost(Table):
    def __init__(self, buffer, address):
        self.buffer = buffer
        self.address = address-0x08000000

        self.cost = self._read_cost()

    def _read_cost(self):
        return self.read(self.address, num=4)

    def write(self):
        self.patch(self.cost, self.address)
        

class SummonAbilities(Table):
    def __init__(self, buffer, address):
        self.buffer = buffer
        self.address = address - 0x08000000

        self._offsets = {}
        self._offsets['Elements'] = 0x0
        self._offsets['Power']    = 0x8

        self.elements = self._read_elements()
        self.power    = self._read_power()

    def _read_elements(self):
        address = self.address + self._offsets['Elements']
        return self.read(address, num=1)

    def _read_power(self):
        address = self.address + self._offsets['Power']
        return self.read(address, num=1, size=2)

    def _write_elements(self):
        address = self.address + self._offsets['Elements']
        self.patch(self.elements, address)

    def _write_power(self):
        address = self.address + self._offsets['Power']
        self.patch(self.power, address, size=2)

    def write(self):
        self._write_elements()
        self._write_power()
        
        
def randomize_summons(rom, flags, cheatfile, djinn):

    seed = flags['Seed']
    flag = flags['Summons']
    
    # Ability order
    names = ['Venus', 'Ramses', 'Cybele', 'Judgment',
             'Mercury', 'Nereid', 'Neptune', 'Boreas',
             'Mars', 'Kirin', 'Tiamat', 'Meteor',
             'Jupiter', 'Atalanta', 'Procne', 'Thor']
    cost = {}
    abil = {}
    for i, ni in enumerate(names):
        j = i%4
        k = int(i/4)

        address = 0x0808061a + j*0x10 + k*0x60
        abil[ni] = SummonAbilities(rom.buffer, address)
        
        address = 0x08084aa0 + (4*j+k)*8
        cost[ni] = SummonCost(rom.buffer, address)
        
    # Randomize djinn requirements
    if flag['Djinn']:
        random.seed(seed)
        for ci in list(cost.values()):
            random.shuffle(ci.cost)
        
    # Ensure "Flint" has summon
    elem = djinn['Flint'].elem
    cost[names[elem*4]].cost = [0,0,0,0]
    cost[names[elem*4]].cost[elem] = 1
        
    # Match element with requirements
    for ni in names:
        ci = cost[ni].cost
        idx = ci.index(max(ci))
        abil[ni].elements = idx

    # Make summons do no damage, only raise elemental power
    summon_ability_start = 0x84A9C
    summon_offset = 0x8
    if flags['NoDamageSummons']:
        for i in range(16):
            rom.write_to_rom(summon_ability_start+(i*summon_offset), [0], byte_length=2)
        print('No Damage Summons Enabled')

    # Make summons very weak
    if flags['LowDamageSummons']:
        low_damage = [20,40,60,80]*4
        for ai in list(abil.values()):
            ai.power = low_damage.pop(0)
        print('Low Damage Summons Enabled (20/40/60/80)')

    # Make summons more balanced (i.e. weaker)
    if flags['BalancedDamageSummons']:
        balanced_damage = [30, 50, 90, 150]*4
        for ai in list(abil.values()):
            ai.power = balanced_damage.pop(0)
        print('Balanced Damage Summons Enabled (30/50/80/120)')

    # Noisy power
    if flag['Power']:
        random.seed(seed)
        for ai in list(abil.values()):
            ai.power = int(ai.power * random.uniform(0.8, 1.2))

    # Write
    for ni in names:
        cost[ni].write()
        abil[ni].write()

    # Print summons
    print_summons(cheatfile, cost, abil)
    
    return

def print_summons(cheatfile, cost, abil):
    with open(cheatfile, 'a') as f:

        f.write('\n\n\n\n\n')
        f.write('=======\n')
        f.write('SUMMONS\n')
        f.write('=======\n')
        f.write('\n')
        f.write(''.rjust(10))
        for vi in ['V', 'M', 'R', 'J']:
            f.write(vi.rjust(3))
        f.write('Element'.rjust(10))
        f.write('Power'.rjust(10))
        f.write('\n')

        names = list(cost.keys())
        elements = ['Earth', 'Water', 'Fire', 'Wind', 'None']
        
        for i, ni in enumerate(names):
            if i%4 == 0:
                f.write('\n')
            f.write(ni.rjust(10))
            j = int(i / 4)
            k = i % 4
            for si in cost[ni].cost:
                if si == 0:
                    f.write('-'.rjust(3))
                else:
                    f.write(str(si).rjust(3))

            f.write(str(elements[abil[ni].elements]).rjust(10))
            f.write(str(abil[ni].power).rjust(10))
            
            f.write('\n')
        f.write('\n\n\n')

    return
