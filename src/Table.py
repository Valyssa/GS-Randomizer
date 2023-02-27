# Consider moving this to the Rom class
# Functions would be called in Summons from self.rom.read, self.rom.patch, etc.
class Table:

    def read(self, address, num=1, size=1, stride=None):
        if stride is None:
            stride = size
        t = []
        for i in range(num):
            ai = address + i*stride
            t.append(int.from_bytes(self.buffer[ai:ai+size], byteorder='little'))
        if num == 1:
            return t[0]
        return t

    def patch(self, values, address, size=1, stride=None):
        if stride is None:
            stride = size
        if not isinstance(values, list):
            values = [values]
        for i, vi in enumerate(values):
            ai = address + i*stride
            self.buffer[ai:ai+size] = vi.to_bytes(size, byteorder='little')
        return
    

