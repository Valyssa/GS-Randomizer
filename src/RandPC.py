import random
from Table import Table

class PC(Table):
    def __init__(self, buffer, address):
        self.buffer = buffer
        self.address = address - 0x08000000
        
        self._offsets = {}
        self._offsets['Stats'] = 0x0
        self._offsets['Elem']  = 0x42

        self.stats = self._read_stats()
        self.elem  = self._read_elem()

    def _read_stats(self):
        address = self.address
        stats = {}
        stats['HP']      = self.read(address,       num=6, size=2)
        stats['PP']      = self.read(address+1*0xc, num=6, size=2)
        stats['Attack']  = self.read(address+2*0xc, num=6, size=2)
        stats['Defense'] = self.read(address+3*0xc, num=6, size=2)
        stats['Agility'] = self.read(address+4*0xc, num=6, size=2)
        stats['Luck']    = self.read(address+5*0xc, num=6, size=1)
        return stats
    
    def _read_elem(self):
        address = self.address + self._offsets['Elem']
        return self.read(address, num=4, size=1)

    def _write_elem(self):
        address = self.address + self._offsets['Elem']
        self.patch(self.elem, address, size=1)

    def _write_stats(self):
        address = self.address + self._offsets['Stats']
        self.patch(self.stats['HP'     ], address,       size=2)
        self.patch(self.stats['PP'     ], address+1*0xc, size=2)
        self.patch(self.stats['Attack' ], address+2*0xc, size=2)
        self.patch(self.stats['Defense'], address+3*0xc, size=2)
        self.patch(self.stats['Agility'], address+4*0xc, size=2)
        self.patch(self.stats['Luck'   ], address+5*0xc, size=1)
        
    def write(self):
        self._write_stats()
        self._write_elem()
    
    
def randomize_pc(rom, flags, cheatfile):

    seed = flags['Seed']
    flag = flags['PC']
    
    names = ['Isaac', 'Garet', 'Ivan', 'Mia']
    pc = {}
    for i, ni in enumerate(names):
        address = 0x0808453c + i*0xb4
        pc[ni] = PC(rom.buffer, address)

    if flag['Stats']:
        print('Shuffling PC stats')
        random.seed(seed)
        randomize_stats(pc)

    if flag['Elements'] == 'Shuffle':
        print('Shuffling PC elements')
        random.seed(seed)
        shuffle_elements(pc)
    elif flag['Elements'] == 'Random':
        print('Randomizing PC elements')
        random.seed(seed)
        randomize_elements(pc)

    # Default levels
    rom.buffer[0x84582] = flag['Levels']['Isaac']
    rom.buffer[0x84636] = flag['Levels']['Garet']
    rom.buffer[0x846ea] = flag['Levels']['Ivan']
    rom.buffer[0x8479e] = flag['Levels']['Mia']
    
    # Patch rom
    for pi in pc.values():
        pi.write()
        

def randomize_stats(pc):

    # Get stats
    keys = pc['Isaac'].stats.keys()
    stats = [[] for _ in keys]
    for pi in pc.values():
        for j, kj in enumerate(keys):
            stats[j].append(pi.stats[kj])

    # Shuffle stats
    for i in range(len(keys)):
        random.shuffle(stats[i])

    # Update stats
    for i, pi in enumerate(pc.values()):
        for j, kj in enumerate(keys):
            pi.stats[kj] = stats[j][i]

# No repeats
def shuffle_elements(pc):

    # Get elements
    elem = [pi.elem for pi in pc.values()]

    # Shuffle elements
    random.shuffle(elem)

    # Update elements
    for i, vi in enumerate(pc.values()):
        vi.elem = elem[i]

# Allows for repeats    
def randomize_elements(pc):

    # Get elements
    elem = [pi.elem for pi in pc.values()]

    # Shuffle elements
    for ei in elem:
        random.shuffle(ei)

    # Update elements
    for i, vi in enumerate(pc.values()):
        vi.elem = elem[i]

    
# def print_elem_inits(file, pc):
    
#     with open(file, 'a') as f:
#         f.write('\n\n\n\n\n')
#         f.write('==============\n')
#         f.write('PARTY DEFAULTS\n')
#         f.write('==============\n')
#         f.write('\n\n\n')
#         f.write('Party Elements:\n\n')
#         f.write('                 V  M  R  J\n\n')
#         for key, value in pc.items():
#             e = [str(int(ej / 10)).rjust(3) for ej in value.elem]
#             f.write(key.rjust(15))
#             for ej in value.elem:
#                 ej = int(ej / 10)
#                 if ej == 0:
#                     f.write('-'.rjust(3))
#                 else:
#                     f.write(str(ej).rjust(3))
#             f.write('\n')
#         f.write('\n\n')

#     return
