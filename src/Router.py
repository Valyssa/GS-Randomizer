import random

class Items():
    def __init__(self):

        self.items = ['Catch Beads','Lifting Gem','Carry Stone',
                      'Halt Gem','Cloak Ball','Orb of Force','Frost Jewel',
                      'Reveal',
                      'Douse Drop', 
                      'Empty Bottle', 'Cell Key', 'Boat Ticket',
                      'Anchor', 'Red Key', 'Mystic Draught', 'Dragons Eye', 'Black Orb']

        self.requirements = {}
        self.requirements['Catch Beads'] = []
        self.requirements['Empty Bottle'] = []
        self.requirements['Dragons Eye'] = ['Empty Bottle']
        self.requirements['Orb of Force'] = ['Empty Bottle', 'Dragons Eye']
        self.requirements['Frost Jewel'] = ['Empty Bottle']
        self.requirements['Lifting Gem'] = ['Empty Bottle', 'Frost Jewel']
        self.requirements['Reveal'] = [ # NOT RANDOMIZED, INCLUDED MAINLY FOR LOG
            'Empty Bottle', 'Lifting Gem', 'Frost Jewel',
        ]
        self.requirements['Boat Ticket'] = [
            'Empty Bottle', 'Lifting Gem', 'Frost Jewel',
            'Reveal',
        ]
        self.requirements['Anchor'] = [
            'Empty Bottle', 'Lifting Gem', 'Frost Jewel',
            'Reveal', 'Boat Ticket',
        ]
        self.requirements['Mystic Draught'] = [
            'Empty Bottle', 'Lifting Gem', 'Frost Jewel',
            'Reveal', 'Boat Ticket', 'Anchor',
        ]
        self.requirements['Cloak Ball'] = [
            'Empty Bottle', 'Lifting Gem', 'Frost Jewel',
            'Reveal', 'Boat Ticket', 'Anchor',
            'Mystic Draught',
        ]
        self.requirements['Carry Stone'] = [
            'Empty Bottle', 'Lifting Gem', 'Frost Jewel',
            'Reveal', 'Boat Ticket', 'Anchor',
            'Mystic Draught', 'Douse Drop',
        ]
        self.requirements['Halt Gem'] = ['Lifting Gem', 'Reveal']
        self.requirements['Cell Key'] = [
            ['Frost Jewel', 'Cloak Ball', 'Catch Beads'],
            ['Frost Jewel', 'Cloak Ball', 'Cell Key'],
        ]
        self.requirements['Red Key'] = [
            'Empty Bottle', 'Lifting Gem', 'Frost Jewel',
            'Reveal', 'Boat Ticket', 'Anchor',
            'Douse Drop', 'Catch Beads',
        ]
        self.requirements['Black Orb'] = [
            'Empty Bottle', 'Lifting Gem', 'Frost Jewel',
            'Reveal', 'Boat Ticket', 'Anchor',
            'Mystic Draught', 'Douse Drop', 'Carry Stone',
        ]

        self.bosses = {}
        self.bosses['Kraken'] = [
            'Empty Bottle', 'Lifting Gem', 'Frost Jewel',
            'Reveal', 'Boat Ticket', 'Anchor',
        ]
        self.bosses['StormLizard'] = [
            'Empty Bottle', 'Lifting Gem', 'Frost Jewel',
            'Reveal', 'Boat Ticket', 'Anchor', 'Douse Drop',
        ]
        self.bosses['Toadonpa'] = [
            'Frost Jewel', 'Cloak Ball', 'Catch Beads',
            'Cell Key', 'Reveal',
        ]
        self.bosses['Deadbeard'] = [
            'Empty Bottle', 'Lifting Gem', 'Frost Jewel',
            'Reveal', 'Boat Ticket', 'Anchor', 'Douse Drop',
            'Red Key', 'Cloak Ball', 'Carry Stone',
        ]

        # TO BE FILLED
        self.swap = {} # Location : Item

    def _accessible(self, v):
        def filter_list(x):
            return list(filter(lambda xi: xi not in self.swap.values(), x))

        if any(isinstance(vi, list) for vi in v):
            # Multiple routes
            m = list(map(filter_list, v))
            return any(mi == [] for mi in m)
        else:
            # Single route
            return filter_list(v) == []
        
    def accessible(self, v):
        r = []
        for vi in v:
            if vi in self.bosses:
                acc = self._accessible(self.bosses[vi])
            else:
                acc = self._accessible(self.requirements[vi])

            if acc:
                r.append(vi)
        return r
    
    def remaining(self):
        return list(filter(lambda x: x not in self.swap.values(), self.items))

    def empty(self):
        locations = list(self.requirements.keys()) + list(self.bosses.keys())
        return list(filter(lambda x: x not in self.swap, locations))

    def one_boss_only(self, boss):
        for key in list(self.bosses.keys()):
            if not key == boss:
                self.bosses.pop(key)

    def allowed_items(self, l, v):
        if l == 'Reveal':
            return ['Reveal']
        else:
            return list(filter(lambda vi: vi != 'Reveal', v))
                
    def completed(self):
        r = self.requirements['Black Orb'] + ['Black Orb']
        missing = list(filter(lambda x: x not in self.swap.values(), r))
        if missing == []:
            return True
        else:
            return False

                
# Randomizes key items and asserts game is beatable.
def swapper(seed, cheatfile):

    random.seed(seed)
    items = Items()

    # Improves likelihood of non-Kraken boss drops
    boss = random.choice(list(items.bosses.keys()))
    items.one_boss_only(boss)

    # Randomize items
    item_placement(items)
    make_all_accessible(items)

    # Log
    print_route(items, cheatfile)
    
    return items.swap

    
# Randomizer -- recursive forward algorithm
# I know, assumed fill is better, but that didn't work so well here....
def item_placement(items):
    
    # List accessible areas
    locations = items.empty()
    locations = items.accessible(locations)
    if locations == []:
        return 

    # Randomize
    random.shuffle(locations)
    for li in locations:
        remaining_items = items.remaining()
        remaining_items = items.allowed_items(li, remaining_items)
        random.shuffle(remaining_items)
        for ri in remaining_items:
            items.swap[li] = ri
            item_placement(items)
            if items.completed():
                return
            items.swap.popitem()

    return
                

# Ensure all items are accessible
def make_all_accessible(items):
    # Switchable items
    switchable = ['Orb of Force', 'Halt Gem']
    while True:
        empty = items.empty()
        if empty == []:
            break
            
        # Find/Make accessible locations
        locations = items.accessible(empty)
        if locations == []:
            # Remove switchable items
            removable = [si for si in switchable if si in items.swap.values()]
            keys = [ki for ki, vi in items.swap.items() if vi in removable]
            list(map(items.swap.pop, keys))
            locations += keys

        # Fill in accessible locations
        locations = items.accessible(locations)
        missing = items.remaining()
        random.shuffle(missing)
        for li, mi in zip(locations, missing):
            items.swap[li] = mi

    return

def print_route(items_filled, cheatfile):

    items = Items()
    boss = list(items_filled.bosses.keys())[0]
    items.one_boss_only(boss)

    with open(cheatfile, 'a') as file:
        file.write('===============\n')
        file.write('SUGGESTED ROUTE\n')
        file.write('===============\n')
        
        def print_item_swaps(locations):
            file.write('\n')
            file.write('Accessible Areas:\n')
            for li in locations:
                item = items_filled.swap[li]
                if li in items_filled.bosses:
                    file.write(' '*8+li.ljust(18, ' ')+' drops '.ljust(16, ' ')+item+'\n')
                elif li == item:
                    file.write(' '*8+li.ljust(18, ' ')+' unchanged'.ljust(16, ' ')+'\n')
                else:
                    file.write(' '*8+li.ljust(18, ' ')+' swapped with '.ljust(16, ' ')+item+'\n')

        def sphere_loop():
            locations = items.empty()
            locations = items.accessible(locations)
            print_item_swaps(locations)
            for li in locations:
                items.swap[li] = items_filled.swap[li]
                    
        while not items.completed():
            sphere_loop()

        file.write('\n\n')
        file.write('Game is beatable!\n')
        file.write('\n\n\n')
        while not items.swap == items_filled.swap:
            sphere_loop()

        missing = items.remaining()
        if not missing == []:
            file.write('\nInaccessible items:\n')
            locations = items.empty()
            print_item_swaps(locations)
                
        file.write('\n')
