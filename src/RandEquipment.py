import random
from Table import Table

class Equipment(Table):
    def __init__(self, buffer, address, name, description):
        self.buffer = buffer
        self.address = address - 0x08000000

        self.name = name # "Gaia Blade"
        self.item = description.split(':')[0] # "Long Sword"
        if ':' in description: # ": ...", remove curse
            self.description = description.split(': ')[1].split('(cursed)')[0]
        else:
            self.description = '' 
            
        self._offsets = {}
        self._offsets['Price']     = 0
        self._offsets['Cursed']    = 0x3
        self._offsets['Equipping'] = 0x4
        self._offsets['Attack']    = 0x8
        self._offsets['Defense']   = 0xa
        self._offsets['Effects']   = 0x18
        self._offsets['Unleash']   = 0xb
        self._offsets['Use']       = 0xc

        
        self.equipping = self._read_equipping()
        self.attack    = self._read_attack()
        self.defense   = self._read_defense()
        self.price     = self._read_price()
        self.effects   = self._read_effects()
        self.unleash   = self._read_unleash()
        self.cursed    = self._read_cursed()
        self.use       = self._read_use()
        
    def update_description(self):
        # Priority to unleash (hide effects and use if it unleashes)
        self.description = self.unleash['Description']
        if self.description == '':
            self.description = self.effects['Description']
        if self.description == '':
            self.description = self.use['Description']
        if self.cursed:
            self.description += ' (cursed)'
        
    def get_full_description(self):
        if self.description == '':
            description = self.item
        elif self.description == ' (cursed)':
            description = '{}{}'.format(self.item, self.description)            
        else:
            description = '{}: {}'.format(self.item, self.description)
        if len(description) > 40:
            description = description.split(': ')[-1]
        return description
            
    def _read_equipping(self):
        address = self.address + self._offsets['Equipping']
        return self.read(address)

    def _read_attack(self):
        address = self.address + self._offsets['Attack']
        return self.read(address, size=2)

    def _read_defense(self):
        address = self.address + self._offsets['Defense']
        return self.read(address)

    def _read_price(self):
        address = self.address + self._offsets['Price']
        return self.read(address, size=2)

    def _read_effects(self):
        address = self.address + self._offsets['Effects']
        effects = self.read(address  , num=4, stride=2)
        values  = self.read(address+1, num=4, stride=2)
        if effects != [0]*4 and self.description.split(' ')[0] != 'Unleashes':
            description = self.description
        else:
            description = ''
        return {'Effects': effects, 'Values': values, 'Description': description}

    def _read_unleash(self):
        address = self.address + self._offsets['Unleash']
        rate    = self.read(address  )
        unleash = self.read(address+3)
        if unleash > 0:
            description = self.description
        else:
            description = ''
        return {'Rate': rate, 'Unleash': unleash, 'Description': description}

    def _read_cursed(self):
        address = self.address + self._offsets['Cursed']
        cursed = self.read(address)
        return cursed & 0x3 == 0x3

    def _read_use(self):
        address = self.address + self._offsets['Use']
        use = self.read(address)
        effect = self.read(address+0x1c, size=2)
        if use > 0 and self.description.split(' ')[0] != 'Unleashes':
            description = self.description
        else:
            description = ''
        return {'Use': use, 'Effect': effect, 'Description': description}
        
    def _write_equipping(self):
        address = self.address + self._offsets['Equipping']
        self.patch(self.equipping, address)
    
    def _write_attack(self):
        address = self.address + self._offsets['Attack']
        self.patch(self.attack, address)
    
    def _write_defense(self):
        address = self.address + self._offsets['Defense']
        self.patch(self.defense, address)
    
    def _write_price(self):
        address = self.address + self._offsets['Price']
        self.patch(self.price, address, size=2)
    
    def _write_effects(self):
        address = self.address + self._offsets['Effects']
        self.patch(self.effects['Effects'], address, stride=2)
        self.patch(self.effects['Values'], address+1, stride=2)
    
    def _write_unleash(self):
        address = self.address + self._offsets['Unleash']
        self.patch(self.unleash['Rate'], address)
        self.patch(self.unleash['Unleash'], address+3)

    def _write_cursed(self):
        address = self.address + self._offsets['Cursed']
        cursed = self.read(address) & ~0x3 # Remove curse if default
        if self.cursed:
            cursed += 0x3
        self.patch(cursed, address)
        
    def _write_use(self):
        address = self.address + self._offsets['Use']
        self.patch(self.use['Use'], address)
        self.patch(self.use['Effect'], address+0x1c, size=2)
        
    def write(self):
        self._write_equipping()
        self._write_attack()
        self._write_defense()
        self._write_price()
        self._write_effects()
        self._write_unleash()
        self._write_cursed()
        self._write_use()
        
    
def randomize_equipment(rom, flags, cheatfile, text):

    seed = flags['Seed']
    flag = flags['Equipment']

    keys = text.lines[387:558]
    keys = list(map(lambda ki: ki.split('}')[-1], keys))

    # Extract text
    descriptions = text.lines[118:289]

    # Equipment list
    equipment = {}
    for i, (ki,di) in enumerate(zip(keys,descriptions)):
        # if ki == '':
        if '?' in di:
            continue
        address = 0x0807b6d4 + i*0x2c
        equipment[ki] = Equipment(rom.buffer, address, ki, di)

    # Overwrite specific descriptions
    equipment['Gaia Blade'].effects['Description'] = 'Boosts Earth power; resists Earth'
    equipment['Swift Sword'].effects['Description'] = 'Boosts Wind power'
    equipment['Righteous Mace'].effects['Description'] = 'HP recovery'    
    equipment["Asura's Armor"].effects['Description'] = 'Replenishes HP'    
    equipment["Spiked Armor"].effects['Description'] = 'Boosts Critical Hits'    
    equipment["Feathered Robe"].effects['Description'] = 'Boosts Wind power & agility; resists Wind'
    equipment["Earth Shield"].effects['Description'] = 'Resists Earth'
    equipment["Spirit Armlet"].effects['Description'] = 'Boosts Earth & Water power'
    equipment["Virtuous Armlet"].effects['Description'] = 'Boosts Fire & Wind power'
    equipment['Lure Cap'].item = 'Hat'
    equipment['Lure Cap'].description = 'Increases random battles'

    # Separate weapons and armor
    weapons = []
    armor = []
    for ei in equipment.values():
        if ei.attack > ei.defense:
            weapons.append(ei)
        else:
            armor.append(ei)
    
    # Randomize equipping
    if flag['Equipping']:
        print('Randomizing equipping weapons and armor')
        random.seed(seed)
        for ei in equipment.values():
            vi  = ei.equipping
            vi -= vi%16
            ei.equipping = vi + random.randint(1,15)

    # Randomize price
    if flag['Price']:
        print('Randomizing equipment price')
        random.seed(seed)
        for ei in equipment.values():
            pi = ei.price
            ei.price = max(10, int(pi * random.uniform(0.8, 1.2) / 10) * 10)
        
    # Randomize stats
    if flag['Attack']:
        print('Randomizing weapon attack')
        random.seed(seed)
        for ei in equipment.values():
            ei.attack  = int(ei.attack  * random.uniform(0.8, 1.2))

    if flag['Defense']:
        print('Randomizing armor defense')
        random.seed(seed)
        for ei in equipment.values():
            ei.defense = int(ei.defense * random.uniform(0.8, 1.2))

    # Shuffle unleashes
    if flag['Unleashes']:
        print('Shuffling weapon unleashes')
        random.seed(seed)
        u = [wi.unleash for wi in weapons]
        random.shuffle(u)
        for wi, ui in zip(weapons, u):
            wi.unleash = ui

    # Shuffle effects
    if flag['Effects']:
        print('Shuffling equipment effects')
        random.seed(seed)
        # Mostly armor for equipment
        effects = []
        for ei in equipment.values():
            if ei.effects['Effects'] != [0]*4:
                effects.append(ei.effects)

        # Sample 2-8 effects for weapons
        n = random.randint(2, 8)
        e4w = random.sample(effects, n)
        # Remaining effects for armor
        e4a = list(filter(lambda ei: ei not in e4w, effects))

        # Fill lists
        noeffects = equipment['Long Sword'].effects # No effects by default
        e4w += [noeffects]*(len(weapons)-len(e4w))
        e4a += [noeffects]*(len(armor)-len(e4a))
        
        # Shuffle and store
        random.shuffle(e4w)
        random.shuffle(e4a)
        for ei, wi in zip(e4w, weapons):
            wi.effects = ei
        for ei, ai in zip(e4a, armor):
            ai.effects = ei

    # Shuffle uses
    if flag['Uses']:
        print('Shuffling equipment uses')
        random.seed(seed)
        u = [ei.use for ei in equipment.values()]
        random.shuffle(u)
        for ei, ui in zip(equipment.values(), u):
            ei.use = ui
            
    # Shuffle curses
    if flag['Cursed']:
        print('Shuffling equipment curses')
        random.seed(seed)
        curses = []
        for ei in equipment.values():
            curses.append(ei.cursed)
            # vi = ei.cursed
            # curses.append(vi & 0x3 == 0x3)
            # ei.cursed = vi - (vi & 0x3)
        random.shuffle(curses)
        for ei, ci in zip(equipment.values(), curses):
            ei.cursed = ci
            # ei.cursed += ci * 0x3
        # UPDATE TEXT

    # Update text
    full_desc = []
    for i, (ki,di) in enumerate(zip(keys,descriptions)):
        if '?' in di:
            continue
        equipment[ki].update_description()
        text.lines[118+i] = equipment[ki].get_full_description()
    
    # Assert text is less than max length
    # Measure max lenght of inits
            
    # Patch rom
    for ei in equipment.values():
        ei.write()
    
    # Print log
    print_equipping(cheatfile, equipment)



def print_equipping(cheatfile, equipment):

    # Print out changes
    keys = equipment.keys()
    size = 5 + max([len(k) for k in keys])
    with open(cheatfile,'a') as f:
        f.write('\n\n\n\n\n')
        f.write('=========\n')
        f.write('EQUIPMENT\n')
        f.write('=========\n')
        f.write('\n')
        string = ''.ljust(size)
        string += ' Equip '
        string += 'Price'.rjust(9)
        string += 'Attack'.rjust(9)
        string += 'Defense'.rjust(9)
        string += 'Cursed'.rjust(10)
        string += 'Unleash'.rjust(16)
        string += 'Effect'.rjust(29)
        string += 'Use'.rjust(33)
        string += '\n\n'
        f.write(string)
        f.write(''.ljust(size)+'I G I M   \n\n')
        for key, value in list(equipment.items()):
            ei = value.equipping
            t = bin(ei % 16 + 16)[-4:]
            equip = ['Y' if f == '1' else 'N' for f in t]
            equip.reverse()

            string = key.ljust(size)
            string += ' '.join(equip)
            string += str(value.price).rjust(9)
            string += str(value.attack).rjust(9)
            string += str(value.defense).rjust(9)

            if value.cursed:# & 0x3 == 0x3:
                cursed = 'Cursed'
            else:
                cursed = '  --  '
            string += str(cursed).center(14)

            if value.unleash['Description'] == '':
                unleash = '---'.center(17,' ')
            else:
                unleash = value.unleash['Description'].split('Unleashes ')[1].center(17)
            string += unleash

            if value.effects['Description'] == '':
                effects = '------'
            else:
                effects = value.effects['Description']
            string += effects.center(41)

            if value.use['Description'] == '':
                use = '-----'
            else:
                use = value.use['Description']
            string += use.center(29)

            

            string += '\n'
            f.write(string)
