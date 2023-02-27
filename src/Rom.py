class LocalRom():

    def __init__(self, file):
        with open(file, 'rb') as stream:
            self.buffer = read_rom(stream)
        return


    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)
        return

    def write_to_rom(self, address, instructions, byte_length=2):
        if address > 0x08000000:
            address -= 0x08000000

        for i, inst in enumerate(instructions):
            bl = inst.to_bytes(byte_length, byteorder='little')
            add = address + i*byte_length
            self.buffer[add:add+len(bl)] = bl
        return
            
def read_rom(stream):
    buffer = bytearray(stream.read())
    return buffer
