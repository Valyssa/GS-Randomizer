from Table import Table
import random

class Abilities(Table):
    def __init__(self, buffer, address):
        self.buffer = buffer
        self.address = address-0x08000000

        self._offsets = {}
        self._offsets['Target']   = 0x0
        self._offsets['Type']     = 0x1
        self._offsets['Element']  = 0x2
        self._offsets['Animation']= 0x4
        self._offsets['Range']    = 0x8
        self._offsets['PPCost']   = 0x9
        self._offsets['Power']    = 0xa
        self._offsets['Utility']  = 0xc

        self.target    = self._read_target()
        self.type      = self._read_type()
        self.element   = self._read_element()
        self.animation = self._read_animation()
        self.range     = self._read_range()
        self.ppcost    = self._read_ppcost()
        self.power     = self._read_power()
        self.utility   = self._read_utility()
        self.index     = 0
        self.name      = ''
        
    def _read_target(self):
        address = self.address + self._offsets['Target']
        return self.read(address, size=1)

    def _read_type(self):
        address = self.address + self._offsets['Type']
        return self.read(address, size=1)

    def _read_element(self):
        address = self.address + self._offsets['Element']
        return self.read(address, size=1)

    def _read_animation(self):
        address = self.address + self._offsets['Animation']
        return self.read(address, size=1)
    
    def _read_range(self):
        address = self.address + self._offsets['Range']
        return self.read(address, size=1)

    def _read_ppcost(self):
        address = self.address + self._offsets['PPCost']
        return self.read(address, size=1)

    def _read_power(self):
        address = self.address + self._offsets['Power']
        return self.read(address, size=2)

    def _read_utility(self):
        address = self.address + self._offsets['Utility']
        return self.read(address, size=1)

    def _write_target(self):
        address = self.address + self._offsets['Target']
        self.patch(self.target, address, size=1)

    def _write_type(self):
        address = self.address + self._offsets['Type']
        self.patch(self.type, address, size=1)

    def _write_element(self):
        address = self.address + self._offsets['Element']
        self.patch(self.element, address, size=1)

    def _write_animation(self):
        address = self.address + self._offsets['Animation']
        self.patch(self.animation, address, size=1)

    def _write_range(self):
        address = self.address + self._offsets['Range']
        self.patch(self.range, address, size=1)

    def _write_ppcost(self):
        address = self.address + self._offsets['PPCost']
        self.patch(self.ppcost, address, size=1)

    def _write_power(self):
        address = self.address + self._offsets['Power']
        self.patch(self.power, address, size=2)

    def _write_utility(self):
        address = self.address + self._offsets['Utility']
        self.patch(self.utility, address, size=1)

    def write(self):
        self._write_target()
        self._write_type()
        self._write_element()
        self._write_animation()
        self._write_range()
        self._write_ppcost()
        self._write_power()

def get_abilities(rom, text):
    address = 0x807EE58
    ability_list = []
    names = text.lines[819:1338]
    i = 0
    while address < 0x8080EC8:
        current_ability=Abilities(rom.buffer,address)
        current_ability.index = i
        current_ability.name = names[i]
        if current_ability.type==0x00: # ? Ability
            pass
        elif current_ability.type==0x85 and current_ability.ppcost==0 and current_ability.power==0: # = Ability
            pass
        else:
            ability_list.append(current_ability)
        address += 0x10
        i += 1
    return ability_list

def randomize_abilities(rom, flags, text):
    if flags['AbilityPower'] or flags['NoElement'] or flags['AbilityRange'] or flags['AbilityCost']:
        random.seed(flags['Seed'])
        all_abilities = get_abilities(rom, text) # All abilities including items, djinn and summons

        if flags['AbilityPower']: # Randomize ability power by 0.8-1.2x
            for ability in all_abilities:
                if ability.power > 0 and (ability.index < 380 or ability.index > 395) and (ability.index < 250 or ability.index > 270) : # Exclude summons since they're handled separately and items
                    ability.power = int(ability.power * random.uniform(0.8, 1.2))
            print("Ability power randomized")

        if flags['NoElement']: # 1/5 chance for any ability to be non-elemental
            for ability in all_abilities:
                if random.randrange(0,5) == 0:
                    ability.element = 4
            print("1/5 abilities made non-elemental")

        if flags['AbilityRange']: # Add or subtract 1 step from Range
            for ability in all_abilities:
                if ability.index > 2 and ability.range > 1: # Exclude single target attacks
                    new_range = min(ability.range, 7)+random.randrange(-1,2) # Make FF (all) into 7 (unused) temporarily then add noise
                    if new_range >= 7: # If range was previously FF or is now 1 step bigger, make into FF
                        new_range = 0xFF
                    ability.range = max(new_range,1) # Ensure range always minimum 1
            print("Ability range randomized")

        if flags['AbilityCost']: # Randomize ability PP cost by 0.8-1.2x
            for ability in all_abilities:
                if ability.ppcost > 0 and (ability.index < 140 or ability.index > 150) :
                    ability.ppcost = int(ability.ppcost * random.uniform(0.8, 1.2))
            print("Ability PP cost randomized")

        for ability in all_abilities:
            ability.write()
    else:
        return