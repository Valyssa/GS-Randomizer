from Table import Table
import random, math, copy
import Abilities

class Items(Table):
    def __init__(self, buffer, address):
        self.buffer = buffer
        self.address = address-0x08000000

        self._offsets = {}
        self._offsets['Price']       = 0x0 # Short
        self._offsets['ItemType']    = 0x2 # Byte
        self._offsets['ItemFlags']   = 0x3 # Byte
        ''' Item Flags
        0x01 = Curses when equipped.
        0x02 = Can’t be removed.
        0x04 = A rare item. (If dropped, can be bought back from shops.)
        0x08 = An important item. (Can’t be dropped.)
        0x10 = Carry up to 30.
        0x20 = Transfer-denied. (Items cannot be transferred from GS1 to GS2.)
        0x40 = Unused
        0x80 = Unused
        '''
        self._offsets['EquipBy']     = 0x4 # Byte
        # self._offsets['Unknown1']    = 0x5 # Byte
        self._offsets['Icon']        = 0x6 # Short
        self._offsets['Attack']      = 0x8 # Short
        self._offsets['Defense']     = 0xA # Byte
        self._offsets['UnleashRate'] = 0xB # Byte
        self._offsets['UseType']     = 0xC # Byte
        # self._offsets['Unknown2']    = 0xD # Byte
        self._offsets['UnleashAbil'] = 0xE # Short
        # self._offsets['Unknown3']    = 0xF # Word
        self._offsets['Attribute']   = 0x13 # Word
        '''
        Equipped effects: (x4)
         BYTE = Effect while equipped
         BYTE = Value
         SHORT = May or may not be unused/part of above value.
        '''
        self._offsets['UseAbility'] = 0x28 # Short
        # self._offsets['Unknown4']   = 0x2A # Short

        self.price        = self._read_price()
        self.itemtype     = self._read_itemtype()
        self.itemflags    = self._read_itemflags()
        self.equipby      = self._read_equipby()
        self.icon         = self._read_icon()
        self.attack       = self._read_attack()
        self.defense      = self._read_defense()
        self.unleashrate  = self._read_unleashrate()
        self.usetype      = self._read_usetype()
        self.unleashabil  = self._read_unleashabil()
        self.attribute    = self._read_attribute()
        self.useability   = self._read_useability()
        self.index        = 0
        self.name         = ""
        self.fullname     = ""
        self.description  = ""
        
    def _read_price(self):
        address = self.address + self._offsets['Price']
        return self.read(address, size=2)

    def _read_itemtype(self):
        address = self.address + self._offsets['ItemType']
        return self.read(address, size=1)

    def _read_itemflags(self):
        address = self.address + self._offsets['ItemFlags']
        return self.read(address, size=1)

    def _read_equipby(self):
        address = self.address + self._offsets['EquipBy']
        return self.read(address, size=1)

    def _read_icon(self):
        address = self.address + self._offsets['Icon']
        return self.read(address, size=2)

    def _read_attack(self):
        address = self.address + self._offsets['Attack']
        return self.read(address, size=2)

    def _read_defense(self):
        address = self.address + self._offsets['Defense']
        return self.read(address, size=1)

    def _read_unleashrate(self):
        address = self.address + self._offsets['UnleashRate']
        return self.read(address, size=1)

    def _read_usetype(self):
        address = self.address + self._offsets['UseType']
        return self.read(address, size=1)

    def _read_unleashabil(self):
        address = self.address + self._offsets['UnleashAbil']
        return self.read(address, size=2)

    def _read_attribute(self):
        address = self.address + self._offsets['Attribute']
        return self.read(address, size=4)

    def _read_useability(self):
        address = self.address + self._offsets['UseAbility']
        return self.read(address, size=2)

    def _write_price(self):
        address = self.address + self._offsets['Price']
        self.patch(self.price, address, size=2)

    def _write_itemtype(self):
        address = self.address + self._offsets['ItemType']
        self.patch(self.itemtype, address, size=1)

    def _write_itemflags(self):
        address = self.address + self._offsets['ItemFlags']
        self.patch(self.itemflags, address, size=1)

    def _write_equipby(self):
        address = self.address + self._offsets['EquipBy']
        self.patch(self.equipby, address, size=1)

    def _write_icon(self):
        address = self.address + self._offsets['Icon']
        self.patch(self.icon, address, size=2)

    def _write_attack(self):
        address = self.address + self._offsets['Attack']
        self.patch(self.attack, address, size=2)

    def _write_defense(self):
        address = self.address + self._offsets['Defense']
        self.patch(self.defense, address, size=1)

    def _write_unleashrate(self):
        address = self.address + self._offsets['UnleashRate']
        self.patch(self.unleashrate, address, size=1)

    def _write_usetype(self):
        address = self.address + self._offsets['UseType']
        self.patch(self.usetype, address, size=1)

    def _write_unleashabil(self):
        address = self.address + self._offsets['UnleashAbil']
        self.patch(self.unleashabil, address, size=2)

    def _write_attribute(self):
        address = self.address + self._offsets['Attribute']
        self.patch(self.attribute, address, size=4)

    def _write_useability(self):
        address = self.address + self._offsets['UseAbility']
        self.patch(self.useability, address, size=2)

    def write(self):
        self._write_price()
        self._write_itemtype()
        self._write_itemflags()
        self._write_equipby()
        self._write_icon()
        self._write_attack()
        self._write_defense()
        self._write_unleashrate()
        self._write_usetype()
        self._write_unleashabil()
        self._write_attribute()
        self._write_useability()

def item_mod(rom, flags, text):
    names = text.lines[386:655]
    descriptions = text.lines[117:386]
    address = 0x807B6A8
    items = []
    i = 0
    while address < 0x807EE58:
        items.append(Items(rom.buffer, address))
        address += 0x2C

    for ii, ni, di in zip(items, names, descriptions):
        ii.description = di
        ii.fullname = ni
        ii.index = i
        if ni[0] == "{":
            ii.name = ni[7:]
        else:
            ii.name = ni
        i += 1

    if flags['PsynergyItems']: # Assigns new psynergy to the 4 psynergy items (Oil Drop etc.)
        ability_list = Abilities.get_abilities(rom, text)
        venus_options = []
        mercury_options = []
        mars_options = []
        jupiter_options = []
        disappearing_party_types = [9, 10, 11, 164, 165, 166] # If an item casts these, it doesn't get consumed

        for ability in ability_list:
            if ((ability.type%16) == 5 or (ability.type%16) == 6) and ability.power > 40: # Base Damage (+Diminishing) only
                if ability.element == 0:
                    if ability.index not in disappearing_party_types:
                        venus_options.append(ability)
                elif ability.element == 1:
                    mercury_options.append(ability)
                elif ability.element == 2:
                    mars_options.append(ability)
                elif ability.element == 3:
                    jupiter_options.append(ability)

        # Pick a random ability from the options
        random.seed(flags['Seed'])
        venus_replacement = random.choice(venus_options)
        mercury_replacement = random.choice(mercury_options)
        mars_replacement = random.choice(mars_options)
        jupiter_replacement = random.choice(jupiter_options)

        # Set Use ability to the new ability
        items[240].useability = venus_replacement.index
        items[240].description = str("Casts " + venus_replacement.name)
        items[241].useability = mercury_replacement.index
        items[241].description = str("Casts " + mercury_replacement.name)
        items[238].useability = mars_replacement.index
        items[238].description = str("Casts " + mars_replacement.name)
        items[239].useability = jupiter_replacement.index
        items[239].description = str("Casts " + jupiter_replacement.name)
        print("Psynergy Items randomized")

    if flags['ExpensiveConsumables']:
        items[180].price = 30   # Herb
        items[182].price = 700  # Vial
        items[183].price = 1000 # Potion
        items[187].price = 60   # Antidote
        items[188].price = 60   # Elixir
        items[236].price = 200  # Sacred Feather
        print("Expensive Consumables Enabled")

    if flags['Unsellable']:
        rom.write_to_rom(0xB19CC, [0x2000], byte_length=2)
        rom.write_to_rom(0xB19CE, [0x4770], byte_length=2)
        print("Unsellable items enabled")

    if flags['Solo'] or flags['NoPortableRevives']:
        items[189].useability = 0   # Make Water of Life do nothing
        items[189].itemflags = 16   # Make WoL not rare and droppable even if Unsellable is on
        items[189].price = 0        # Make WoL not worth anything, since it doesn't do anything!
        items[189].description = 'Does nothing'
        rom.write_to_rom(134739121, [255], byte_length=1) # Set Revive cost to 255
        rom.write_to_rom(0x7F4AB, [0], byte_length=1) # Set Revive ability effect to Nothing
        rom.write_to_rom(0x8013B, [0], byte_length=1) # Make Quartz not revive
        rom.write_to_rom(0x802BB, [0], byte_length=1) # Make Dew not revive
        text.lines[306] = 'Does nothing'
        text.lines[1439] = 'Does nothing'
        text.lines[1640] = 'Does nothing'
        text.lines[1664] = 'Does nothing'
        print("Portable revival means nullified")

    if flags['ShuffleConsumables']:
        if flags['ExpensiveConsumables']: # Make more consumables expensive
            ''' Not necessary yet
            stat_booster_price = 1500
            psynergy_item_price = 100
            items[191].price = stat_booster_price
            items[192].price = stat_booster_price
            items[193].price = stat_booster_price
            items[194].price = stat_booster_price
            items[195].price = stat_booster_price
            items[196].price = stat_booster_price

            items[238].price = psynergy_item_price
            items[239].price = psynergy_item_price
            items[240].price = psynergy_item_price
            items[241].price = psynergy_item_price
            '''

            items[233].price = 80 # Corn
        items[233].itemflags += 0x10 # Make Corn stackable

        random.seed(flags['Seed'])
        healing_items = [items[180], items[181], items[182], items[183], items[233]]
        common_items = [items[187], items[188], items[226], items[227]] # Antidote, Elixir, Smoke Bomb, Sleep Bomb
        uncommon_items = [items[186], items[189]] # Psy Crystal, Water of Life
        if not flags['Avoid']:
            uncommon_items.append(items[236]) # Add Sacred Feather only if no Altered Avoid functionality
        stat_items = [items[191], items[192], items[193], items[194], items[195], items[196]]
        gambling_items = [items[228], items[229]] # Game Ticket, Lucky Medal
        psynergy_items = [items[238], items[239], items[240], items[241]]

        single_use_items = [healing_items, common_items, uncommon_items, stat_items, gambling_items, psynergy_items]
        items_copy = copy.deepcopy(single_use_items)

        for i in range(0, len(single_use_items)):
            random.shuffle(single_use_items[i]) # Shuffle sub-list
            for j in range(0, len(single_use_items[i])):
                single_use_items[i][j].address = items_copy[i][j].address
                text.lines[386+items_copy[i][j].index] = single_use_items[i][j].fullname
                text.lines[117+items_copy[i][j].index] = single_use_items[i][j].description
        print("Consumables shuffled")

    for ii in items:
        ii.write()
