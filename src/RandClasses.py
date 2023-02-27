import random
from Table import Table

class Classes(Table):
    def __init__(self, buffer, address, names):
        self.buffer = buffer
        self.address = address-0x08000000
        self.names = names
        
        self._offsets = {}
        self._offsets['Type']     = 0
        self._offsets['Class']    = 0x54
        self._offsets['Elements'] = 0x4
        self._offsets['Boosts']   = 0x8
        self._offsets['Psynergy'] = 0x10
        self._offsets['Levels']   = 0x11
        
        self.elements = self._read_elements()
        self.boosts   = self._read_boosts()
        self.psynergy = self._read_psynergy()
        self.levels   = self._read_levels()

        # Total djinn required
        self.costs = list(map(sum, self.elements))

        
    def _read_table(self, address, num, size=1, stride=1):
        table = []
        for i, _ in enumerate(self.names):
            ai = address + i*self._offsets['Class']
            table.append(self.read(ai, num, size, stride))
        return table
            
    def _write_table(self, values, address, size=1, stride=1):
        for i, vi in enumerate(values):
            ai = address + i*self._offsets['Class']
            self.patch(vi, ai, size, stride)
        return
    
    def _read_elements(self):
        address = self.address + self._offsets['Elements']
        return self._read_table(address, num=4)

    def _read_boosts(self):
        address = self.address + self._offsets['Boosts']
        return self._read_table(address, num=6)

    def _read_psynergy(self):
        address = self.address + self._offsets['Psynergy']
        return self._read_table(address, num=16, stride=4)

    def _read_levels(self):
        address = self.address + self._offsets['Levels']
        return self._read_table(address, num=16, stride=4)
    
    def _write_elements(self):
        address = self.address + self._offsets['Elements']
        self._write_table(self.elements, address)
    
    def _write_boosts(self):
        address = self.address + self._offsets['Boosts']
        self._write_table(self.boosts, address)
    
    def _write_psynergy(self):
        address = self.address + self._offsets['Psynergy']
        self._write_table(self.psynergy, address, stride=4)

    def _write_levels(self):
        address = self.address + self._offsets['Levels']
        self._write_table(self.levels, address, stride=4)
        
    def write(self):
        self._write_elements()
        self._write_boosts()
        self._write_psynergy()
        self._write_levels()

        
    
def randomize_classes(rom, flags, cheatfile, text):

    seed = flags['Seed']
    flag = flags['Classes']
    
    names = [['Squire', 'Knight', 'Gallant', 'Lord', 'Slayer'],
             ['Guard', 'Soldier', 'Warrior', 'Champion', 'Hero'],
             ['Wind Seer', 'Magician', 'Mage', 'Magister', 'Sorcerer'],
             ['Water Seer', 'Scribe', 'Cleric', 'Paragon', 'Angel'],
             ['Swordsman 1', 'Defender 1', 'Cavalier 1', 'Guardian', 'Protector'],
             ['Swordsman 2', 'Defender 2', 'Cavalier 2', 'Luminier', 'Radiant'],
             ['Dragoon', 'Templar', 'Paladin'],
             ['Apprentice', 'Illusionist 1', 'Enchanter 1', 'Conjurer 1', 'War Adept 1'],
             ['Page', 'Illusionist 2', 'Enchanter 2', 'Conjurer 2', 'War Adept 2'],
             ['Ninja', 'Disciple', 'Master'],
             ['Seer 1', 'Diviner 1', 'Shaman 1', 'Druid 1', 'Oracle 1'],
             ['Seer 2', 'Diviner 2', 'Shaman 2', 'Druid 2', 'Oracle 2'],
             ['Medium', 'Dark Mage', 'Death Mage'],
             ['Pilgrim 1', 'Wanderer 1', 'Ascetic 1', 'Water Monk', 'Guru 1'],
             ['Pilgrim 2', 'Wanderer 2', 'Ascetic 2', 'Fire Monk', 'Guru 2'],
             ['Ranger', 'Bard', 'Warlock'],
             ['Brute', 'Ruffian', 'Savage', 'Barbarian', 'Berserker', 'Chaos Lord'],
             ['Samurai', 'Ronin'],
             ['Hermit', 'Elder', 'Scholar', 'Savant', 'Sage', 'Wizard'],
             ['White Mage', 'Pure Mage']]

    classes = {}
    classes['Squire'] = Classes(rom.buffer, 0x08084b70, names[0])
    for i, ni in enumerate(names[1:]):
        address = 0x08084e64 + i*0x348
        classes[ni[0]] = Classes(rom.buffer, address, ni)

    # Stat boosts
    if flag['Stats']:
        print('Shuffling classline stat boosts')
        # random.seed(seed)
        randomize_boosts(classes, flags['Seed'])

    # Psynergy
    random.seed(seed)
    if flag['Psynergy'] == 'Shuffle':
        print('Shuffling class skillsets')
        # random.seed(seed)
        randomize_psynergy_skillset(classes, flags['Seed'])
    elif flag['Psynergy'] == 'Random':
        print('Shuffling class psynergy')
        # random.seed(seed)
        randomize_psynergy_random(classes, flags['Seed'])
    else:
        pass
        
    # Levels
    if flag['Levels']['Random']:
        print('Shuffling class psynergy levels')
        # random.seed(seed)
        levels_shuffle(classes, flags['Seed'])

    if flag['Levels']['Noise']:
        print('Randomizing class psynergy levels')
        # random.seed(seed)
        levels_add_noise(classes, flags['Seed'])

    if flag['Levels']['Balanced']:
        print('Balancing class psynergy levels')
        levels_balance(classes, flags['Seed'])

    # Sort -- must be done AFTER levels
    if flag['Psynergy'] == 'Random':
        sort_psynergy(classes)
        
    # Patch rom
    for ci in classes.values():
        ci.write()

    # Print
    print_classes(classes, names, cheatfile, text)
        
    return
    
def print_classes(classes, names, cheatfile, text):
    abilities = text.lines[819:1016]
    # abilities = [
    #     '',
    #     'Attack','Defend',
    #     'Quake','Earthquake','Quake Sphere',
    #     'Spire','Clay Spire','Stone Spire',
    #     'Gaia','Mother Gaia','Grand Gaia',
    #     'Growth','Mad Growth','Wild Growth',
    #     'Thorn','Briar','Nettle',
    #     '','','','','','',
    #     'Frost','Tundra','Glacier',
    #     'Ice','Ice Horn','Ice Missile',
    #     'Prism','Hail Prism','Freeze Prism',
    #     'Douse','Drench','Deluge',
    #     'Froth','Froth Sphere','Froth Spiral',
    #     '','','','','','',
    #     'Flare','Flare Wall','Flare Storm',
    #     'Fire','Fireball','Inferno',
    #     'Volcano','Eruption','Pyroclasm',
    #     'Blast','Mad Blast','Fiery Blast',
    #     'Blast','Nova','Supernova',
    #     '','','','','','',
    #     'Bolt','Flash Bolt','Blue Bolt',
    #     'Ray','Storm Ray','Destruct Ray',
    #     'Plasma','Shine Plasma','Spark Plasma',
    #     'Slash','Wind Slash','Sonic Slash',
    #     'Whirlwind','Tornado','Tempest',
    #     '','','','','','','','','',
    #     'Cure','Cure Well','Potent Cure',
    #     'Ply','Ply Well','Pure Ply',
    #     'Wish','Wish Well','Pure Wish',
    #     'Cure Poison','Restore','Revive',
    #     'Impact','High Impact',
    #     'Dull','Blunt',
    #     'Guard','Protect',
    #     'Impair','Debilitate',
    #     'Ward','Resist',
    #     'Weaken','Enfeeble',
    #     'Taint','Poison',
    #     'Delude','Confuse',
    #     'Charm','Paralyze',
    #     'Sleep','Bind',
    #     'Haunt','Curse','Condemn',
    #     'Drain','Psy Drain',
    #     'Break',
    #     '','',
    #     '','','','','','','','','','',
    #     'Move','Mind Read','Force','Lift',
    #     'Reveal','Halt','Cloak','Carry',
    #     'Catch','Retreat','Avoid',
    #     '','','','','','','','','',
    #     'Dragon Cloud',
    #     'Demon Night',
    #     'Helm Splitter',
    #     'Quick Strike',
    #     'Rockfall','Rockslide','Avalanche',
    #     'Lava Shower','Molten Bath','Magma Storm',
    #     'Demon Spear','Angel Spear',
    #     'Guardian','Protector',
    #     'Magic Shell','Magic Shield',
    #     'Death Plunge',
    #     'Shuriken',
    #     'Annihilation',
    #     'Punji','Punji Trap','Punji Strike',
    #     'Fire Bomb','Cluster Bomb','Carpet Bomb',
    #     'Gale','Typhoon','Hurricane',
    #     'Thunderclap','Thunderbolt','Thunderstorm',
    #     'Mist',
    #     'Ragnarok',
    #     'Cutting Edge',
    #     'Heat Wave',
    #     'Astral Blast',
    #     'Planet Diver',
    # ]
    
    def print_psynergy(psynergy, levels, name, file):
        for p, lvl, n in zip(psynergy, levels, name):
            cols = ['Levels', 'Abilities']
            file.write(n.ljust(18)+'  '.join(cols)+'\n')
            for pi, li in zip(p, lvl):
                if pi == 0:
                    continue
                s = ' '*22 + str(li).rjust(2).ljust(4)+abilities[pi]+'\n'
                file.write(s)
            file.write('\n')
        file.write('\n'*5)
        
                
    def print_boosts(boosts, name, file):
        stats = ['HP', 'PP', 'ATK', 'DEF', 'AGIL', 'LUCK']
        s = ' '.ljust(21) + '  '.join([si.rjust(4) for si in stats])
        s.join(' ')
        file.write('\n')
        file.write(s)
        file.write('\n')
        for b, n in zip(boosts, name):
            file.write(n.rjust(16)+'   ')
            for bi in b:
                s = str(bi*10)+'%'
                file.write(s.rjust(6))
            file.write('\n')

    with open(cheatfile, 'a') as f:
        f.write('\n\n\n\n\n')
        f.write('=======\n')
        f.write('CLASSES\n')
        f.write('=======\n')
        f.write('\n\n\n')
        f.write('CLASS BOOSTS\n')
        for ci, ni in zip(classes.values(), names):
            print_boosts(ci.boosts, ni, f)
        f.write('\n\n\n')
        f.write('CLASS PSYNERGY\n\n')
        for ci, ni in zip(classes.values(), names):
            print_psynergy(ci.psynergy, ci.levels, ni, f)
        f.write('\n\n\n')


    
#####################
# BOOST RANDOMIZERS #
#####################

def compute_growth_rates(boosts):
    gr = []
    for bi in boosts:
        gi = [float(h-l) / len(bi) for l, h in zip(bi[0], bi[-1])]
        gr.append(gi)
    return gr


def rescale_boosts(boosts, mb, gr):
    for i, bi in enumerate(boosts):
        for j, bj in enumerate(bi):
            n = len(bi)
            bj[:] = [int(mj - (n-1-j)*gj) for mj, gj in zip(mb[i], gr[i])]
    

def randomize_boosts(classes, seed):
    random.seed(seed)
    boosts = [ci.boosts for ci in classes.values()]

    # Growth rates in each group of classes
    gr = compute_growth_rates(boosts)
        
    # Shuffle max boosts
    maxes = [bi[-1] for bi in boosts]
    random.shuffle(maxes)
    
    # Rescale boosts
    rescale_boosts(boosts, maxes, gr)


########################
# PSYNERGY RANDOMIZERS #
########################

def randomize_psynergy_skillset(classes, seed):
    random.seed(seed)
    
    # List of default skillsets
    skills = [[si.costs, si.psynergy, si.levels] for si in classes.values()]
    random.shuffle(skills)

    # Randomize class skillsets
    for ci, [ri, pi, li] in zip(classes.values(), skills):
        def index(i):
            for j, rj in enumerate(ri):
                if rj+1 >= ci.costs[i]:
                    break
            return j
        for i in range(len(ci.names)):
            idx = index(i)
            ci.psynergy[i] = pi[idx]
            ci.levels[i] = li[idx]


def randomize_psynergy_random(classes, seed):
    random.seed(seed)

    psyn = [ci.psynergy for ci in classes.values()]
    lvls = [ci.levels for ci in classes.values()]

    abilities = []; levels = []
    for pi, li in zip(psyn, lvls):
        for pj, lj in zip(pi[-1], li[-1]):
            if pj == 0:
                continue
            else:
                abilities.append(pj)
                levels.append(lj)

    # Sample psynergy & levels without psynergy repeats
    # List allowed to have repeats instead of weights
    def unique_sample(p, l, n):
        y = []
        lst = list(zip(p, l))
        for _ in range(n):
            t = random.sample(lst, 1)[0]
            y.append(t)
            lst = list(filter(lambda li: li[0] != t[0], lst))
        return map(list, zip(*y))

    # Copy psyergy or levels
    # Skips empty slots in table
    def copy_skip_zero(x, lst):
        j = 0
        for i, xi in enumerate(x):
            if xi > 0:
                x[i] = lst[j]
                j += 1

    # Sample and store
    for pi, li in zip(psyn, lvls):
        n = sum(list(map(lambda x: x > 0, pi[-1])))
        p, l = unique_sample(abilities, levels, n)
        copy_skip_zero(pi[-1], p)
        copy_skip_zero(li[-1], l)
        
    # Copy through classlines
    copy_up_classline(psyn)
    copy_up_classline(lvls)

    
def sort_psynergy(classes):
    psyn = [ci.psynergy for ci in classes.values()]
    lvls = [ci.levels for ci in classes.values()]
    
    # Sort -- keep groups together, e.g. Ply and Ply Well
    for pi, li in zip(psyn, lvls):
        for pj, lj in zip(pi, li):
            z = list(zip(*sorted(zip(pj, lj))))
            pj[:] = list(z[0])
            lj[:] = list(z[1])


#####################
# LEVEL RANDOMIZERS #
#####################

def levels_shuffle(classes, seed):
    random.seed(seed)
    levels = [ci.levels for ci in classes.values()]
    lev = []
    for li in levels:
        for lj in li[-1]:
            lev.append(lj)
    l0  = list(filter(lambda x: x > 0, lev))

    # Shuffle
    random.shuffle(l0)

    # Overwrite last class in each class line
    k = 0
    for li in levels:
        for j, lj in enumerate(li[-1]):
            if lj > 0:
                li[-1][j] = l0[k]
                k += 1
    
    # Copy through classlines
    copy_up_classline(levels)


def levels_balance(classes, seed):
    random.seed(seed)
    levels = [ci.levels for ci in classes.values()]

    # Generate list of new levels
    for li in levels:
        new_levels = []
        for level in li[-1]: # Generate list of new levels
            if level == 0:
                new_levels.append(0)
        balanced_levels = [
        1, random.randint(2,3), random.randint(4,5),
        random.randint(6,10), random.randint(6,10), random.randint(6,10),
        random.randint(11,15), random.randint(11,15), random.randint(11,15),
        random.randint(16,20), random.randint(16,20), random.randint(16,20),
        random.randint(21,25), random.randint(21,25),
        random.randint(26,30), random.randint(26,30)
        ]
        while len(new_levels) < 16:
            new_levels.append(balanced_levels.pop(0))
        replaced_levels = [0]*16
        old_levels = li[-1]
        for i in range(16): # Loop 16 times, finding and replacing the lowest value each time
            lowest_old_level = min(old_levels)
            index_of_new = new_levels.index(min(new_levels))
            index_of_lowest = li[-1].index(lowest_old_level)
            replaced_levels[index_of_lowest] = new_levels[new_levels.index(min(new_levels))]

            # Set values we just used to 99 so it's not picked up as lowest again
            old_levels[old_levels.index(lowest_old_level)] = 99
            new_levels[index_of_new] = 99
        for j, lj in enumerate(li[-1]):
            li[-1][j] = replaced_levels[j]

    # Copy through classlines
    copy_up_classline(levels)

def levels_add_noise(classes, seed):
    random.seed(seed)
    levels = [ci.levels for ci in classes.values()]

    # Add noise and store to last class in each class line
    for li in levels:
        for j, lj in enumerate(li[-1]):
            if lj > 0:
                ri = max(1, int(lj * random.uniform(0.8, 1.2)))
            else:
                ri = 0
            li[-1][j] = ri

    # Copy through classlines
    copy_up_classline(levels)


#############
# UTILITIES #
#############

def copy_up_classline(lst):
    for li in lst:
        for lj in li[:-1]:
            lj[:] = [ll if lk > 0 else 0 for ll, lk in zip(li[-1], lj)]
