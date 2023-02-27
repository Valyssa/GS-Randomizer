import random
from Table import Table

class Music(Table):
    def __init__(self, buffer, address):
        self.buffer = buffer
        self.address = address-0x08000000+6 # Music
        self.tune = self.read(self.address, size=2)

    def write(self):
        self.patch(self.tune, self.address, size=2)

def randomize_music(rom, flags):

    address = 0x0809d9f0
    music = []
    while address < 0x0809ddd0:
        music.append(Music(rom.buffer, address))
        address += 8
    
    if flags['Music']:
        print("Shuffling music")
        tunes = [mi.tune for mi in music]
        random.shuffle(tunes)
        for mi, ti in zip(music, tunes):
            mi.tune = ti

    for mi in music:
        mi.write()
    
    return
