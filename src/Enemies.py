from Table import Table
import random, math
import Abilities

valid_abilities = []
boss_abilities_to_exclude = [99, 100, 116, 117, 118, 128, 129, 191, 325, 480, 489, 498, 499, 500, 501, 502, 503, 504, 505, 508] # Exclude weak/otherwise unfit abilities
defense_moves = [2, 301, 345, 502, 506, 507]
revive_moves = [101, 302, 326]

# Bosses/mandatory battles
bosses = ['Bandit','Thief','Brigand',
          'Killer Ape',
          'Manticore',
          'Kraken',
          'Saturos','Menardi',
          'Living Statue','Hydros Statue',
          'Azart','Satrage','Navampa',
          'Toadonpa',
          'Tornado Lizard','Storm Lizard', 'Tempest Lizard',
          'Tret',
          'Fusion Dragon',
          # Tolbi Boat
          "Man o' War", 'Virago',
          'Lizard Fighter','Rabid Bat',
          # CROSSBONE ISLE
          'Hobgoblin','Virago',
          'Succubus','Grisly',
          'Lich','Fiendish Ghoul',
          'Gryphon',
          'Lizard King','Harridan','Stone Soldier',
          'Chimera',
          'Earth Lizard',
          'Poison Toad','Thunder Lizard',
          'Cerebus',
          'Deadbeard']

pattern_based = ['Saturos', 'Manticore']

class Enemies(Table):
    def __init__(self, buffer, address):
        self.buffer = buffer
        self.address = address-0x08000000

        self._offsets = {}
        self._offsets['Level']        = 0x0
        self._offsets['HP']           = 0x1
        self._offsets['PP']           = 0x3
        self._offsets['Attack']       = 0x5
        self._offsets['Defense']      = 0x7
        self._offsets['Agility']      = 0x9
        self._offsets['Luck']         = 0xb
        self._offsets['Turns']        = 0xc
        self._offsets['HP Regen']     = 0xd
        self._offsets['PP Regen']     = 0xe
        self._offsets['Items']        = 0xf
        self._offsets['Item Amounts'] = 0x17
        self._offsets['Moves']        = 0x29
        self._offsets['Coins']        = 0x3d
        self._offsets['Exp']          = 0x43

        self.level        = self._read_level()
        self.hp           = self._read_hp()
        self.pp           = self._read_pp()
        self.attack       = self._read_attack()
        self.defense      = self._read_defense()
        self.agility      = self._read_agility()
        self.luck         = self._read_luck()
        self.turns        = self._read_turns()
        self.hp_regen     = self._read_hp_regen()
        self.pp_regen     = self._read_pp_regen()
        self.items        = self._read_items()
        self.item_amounts = self._read_item_amounts()
        self.moves        = self._read_moves()
        self.coins        = self._read_coins()
        self.exp          = self._read_exp()
        
    def _read_level(self):
        address = self.address + self._offsets['Level']
        return self.read(address)

    def _read_hp(self):
        address = self.address + self._offsets['HP']
        return self.read(address, size=2)

    def _read_pp(self):
        address = self.address + self._offsets['PP']
        return self.read(address, size=2)

    def _read_attack(self):
        address = self.address + self._offsets['Attack']
        return self.read(address, size=2)
    
    def _read_defense(self):
        address = self.address + self._offsets['Defense']
        return self.read(address, size=2)

    def _read_agility(self):
        address = self.address + self._offsets['Agility']
        return self.read(address, size=2)

    def _read_luck(self):
        address = self.address + self._offsets['Luck']
        return self.read(address)

    def _read_turns(self):
        address = self.address + self._offsets['Turns']
        return self.read(address)
    
    def _read_hp_regen(self):
        address = self.address + self._offsets['HP Regen']
        return self.read(address)

    def _read_pp_regen(self):
        address = self.address + self._offsets['PP Regen']
        return self.read(address)

    def _read_items(self):
        address = self.address + self._offsets['Items']
        temp_item_list = []
        for i in range(4):
            temp_item_list.append(self.read(address+i*2, size=2))
        return temp_item_list

    def _read_item_amounts(self):
        address = self.address + self._offsets['Item Amounts']
        temp_amounts_list = []
        for i in range(4):
            temp_amounts_list.append(self.read(address+i, size=1))
        return temp_amounts_list

    def _read_moves(self):
        address = self.address + self._offsets['Moves']
        temp_moves_list = []
        for i in range(8):
            temp_moves_list.append(self.read(address+i*2, size=2))
        return temp_moves_list

    def _read_coins(self):
        address = self.address + self._offsets['Coins']
        return self.read(address, size=2)

    def _read_exp(self):
        address = self.address + self._offsets['Exp']
        return self.read(address, size=2)

    def _write_level(self):
        address = self.address + self._offsets['Level']
        self.patch(self.level, address, size=1)

    def _write_hp(self):
        address = self.address + self._offsets['HP']
        self.patch(self.hp, address, size=2)

    def _write_pp(self):
        address = self.address + self._offsets['PP']
        self.patch(self.pp, address, size=2)

    def _write_attack(self):
        address = self.address + self._offsets['Attack']
        self.patch(self.attack, address, size=2)

    def _write_defense(self):
        address = self.address + self._offsets['Defense']
        self.patch(self.defense, address, size=2)

    def _write_agility(self):
        address = self.address + self._offsets['Agility']
        self.patch(self.agility, address, size=2)

    def _write_luck(self):
        address = self.address + self._offsets['Luck']
        self.patch(self.luck, address, size=1)

    def _write_hp_regen(self):
        address = self.address + self._offsets['HP Regen']
        self.patch(self.hp_regen, address, size=1)

    def _write_pp_regen(self):
        address = self.address + self._offsets['PP Regen']
        self.patch(self.pp_regen, address, size=1)

    def _write_items(self):
        address = self.address + self._offsets['Items']
        for i in range(4):
            self.patch((self.items[i]), address+i*2, size=2)

    def _write_item_amounts(self):
        address = self.address + self._offsets['Item Amounts']
        for i in range(4):
            self.patch((self.item_amounts[i]), address+i, size=1)

    def _write_moves(self):
        address = self.address + self._offsets['Moves']
        for i in range(8):
            self.patch((self.moves[i]), address+i*2, size=2)

    def _write_coins(self):
        address = self.address + self._offsets['Coins']
        self.patch(self.coins, address, size=2)

    def _write_exp(self):
        address = self.address + self._offsets['Exp']
        self.patch(self.exp, address, size=2)

    def write(self):
        self._write_level()
        self._write_hp()
        self._write_pp()
        self._write_attack()
        self._write_defense()
        self._write_agility()
        self._write_luck()
        self._write_hp_regen()
        self._write_pp_regen()
        self._write_items()
        self._write_item_amounts()
        self._write_moves()
        self._write_coins()
        self._write_exp()

def enemy_mod(rom, flags, text):
    names = text.lines[0x290:0x332]
    
    address = 0x8080f2b
    enemies = []
    while address < 0x8084453:
        enemies.append(Enemies(rom.buffer, address))
        address += 0x54

    # Scale coins and experience
    scale_coins = int(flags['Coins'])
    scale_exp = int(flags['Exp'])
    scale_boss_coins = int(flags['BossCoins'])
    scale_boss_exp = int(flags['BossExp'])
    for ei, ni in zip(enemies, names):
        if not ni in bosses:
            ei.coins = min(int(ei.coins*scale_coins), 0xffff)
            ei.exp = min(int(ei.exp*scale_exp), 0xffff)
        elif ni in bosses:
            ei.coins = min(int(ei.coins*scale_boss_coins), 0xffff)
            ei.exp = min(int(ei.exp*scale_boss_exp), 0xffff)

    # Determine valid abilities
    all_abilities = Abilities.get_abilities(rom, text)
    for ability in all_abilities:
        if ability.index >= 250 and ability.index <= 270: # Item abilities
            pass
        elif ability.index in revive_moves: # Revive never works since monsters disintegrate
            pass
        else:
            valid_abilities.append(ability)

    if flags['EnemyStats']:
        random.seed(flags['Seed'])
        for ei in enemies:
            ei.hp = int(ei.hp * random.uniform(0.8, 1.2))
            ei.pp = int(ei.pp * random.uniform(0.8, 1.2))
            ei.attack = int(ei.attack * random.uniform(0.8, 1.2))
            ei.defense = int(ei.defense * random.uniform(0.8, 1.2))
            ei.agility = int(ei.agility * random.uniform(0.8, 1.2))
            ei.luck = int(ei.luck * random.uniform(0.8, 1.2))
            ei.hp_regen = int(ei.hp_regen * random.uniform(0.8, 1.2))
            ei.pp_regen = int(ei.pp_regen * random.uniform(0.8, 1.2))
        print("Randomized enemy stats")

    if flags['EnemyMovepools']:
        random.seed(flags['Seed'])
        bossBool = False
        patternBool = False
        for ei, ni in zip(enemies, names):
            if ni in bosses:
                bossBool = True
                if ni in pattern_based:
                    patternBool = True
            randomize_enemy_moves(rom, ei, bossBool, patternBool)
        print("Randomized enemy movepools")

    # Write new stats/abilities to enemy
    for ei in enemies:
        ei.write()



def randomize_enemy_moves(rom, enemy, boss, pattern):
    # Randomize amount of non-attack moves.
    # Moves have to meet a certain minimum and maximum of power to somewhat be appropriate for the enemy's strength

    valid_moves_this_enemy = []
    for ability in valid_abilities:
        if boss and ability.index in boss_abilities_to_exclude: # Skip if boss and ability not fit for bosses
            pass
        elif pattern and ability.index in defense_moves: # Skip defense moves if pattern based enemy since it breaks pattern
            pass
        elif ability.ppcost <= enemy.pp:
            if ability.type > 128:
                if (ability.type%16) == 5 or (ability.type%16) == 6 or (ability.type%16) == 8: # If Base Damage, BD Diminishing or Summon
                    if ability.power > enemy.attack*0.2 and ability.power < enemy.attack*0.5:
                        valid_moves_this_enemy.append(ability)
                elif (ability.type%16) == 3: # If added damage
                    if ability.power > enemy.attack*0.1 and ability.power < enemy.attack*0.3:
                        valid_moves_this_enemy.append(ability)
                elif (ability.type%16) == 1: # If healing
                    if ability.power > enemy.attack*0.3 and ability.power < enemy.attack:
                        valid_moves_this_enemy.append(ability)
                elif (ability.type%16) == 2: # If Effect Only
                    if ability.power < enemy.attack*0.5:
                        valid_moves_this_enemy.append(ability)
                else:
                    valid_moves_this_enemy.append(ability)

    new_moves_this_enemy = []
    guaranteed_moves = min(8, 2+math.floor(enemy.level/8)+boss) # Higher level guarantees more non-attacks, but everyone has at least 2. Bosses 1 extra
    attacks_to_insert = random.randint(0, 8-guaranteed_moves)
    for i in range(0, attacks_to_insert):
        new_moves_this_enemy.append(1)
    while len(new_moves_this_enemy) < 8:
        picked_ability = random.choice(valid_moves_this_enemy)
        new_moves_this_enemy.append(picked_ability.index)

    random.shuffle(new_moves_this_enemy)
    enemy.moves = new_moves_this_enemy
