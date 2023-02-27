import Utilities

class Text():
    ''' 
    Decompression with Huffman trees.
    Contributed by Dyrati.
    '''
    def __init__(self, buffer):
        self.buffer = buffer
        self.huffman_pntr = 0x03842c
        self.cmprssd_base = 0x0736b8
        
        self.charTrees = []
        self.charLists = []
        self.get_trees()
        self.lines = list(map(self.DcmprssTxt, range(0x29e2)))

    # Reads rom
    def read(self,addr,size):
        return int.from_bytes(self.buffer[addr:addr+size], 'little')

    def get_trees(self):
        char_data_base = self.read(self.huffman_pntr,3)
        tree_offset_tbl = self.read(self.huffman_pntr + 4,3)

        # Constructs the char trees and char lists for each char up to 0xFF
        # each tree is modified: +1 for each node, -1 for each leaf
        # each char list is a dictionary in the format: {tree_leaf_index : char_num}
        for i in range(0x100):
            tree_offset = self.read(tree_offset_tbl + 2*i,2)
            tree_addr = char_data_base + tree_offset

            tree = []
            chars = {}
            depth = 0
            charPos = 0
            for count in range(64):
                byte = self.buffer[tree_addr + count]
                for j in range(8):
                    if byte & 1:
                        depth -= 1
                        charPos += 1.5 # i.e. 12 bits
                        c = self.read(tree_addr - int(charPos + 0.5),2)
                        if charPos != int(charPos):
                            chars[8*count+j] = c >> 4
                        else:
                            chars[8*count+j] = c & 0xFFF
                    else:
                        depth += 1

                    tree.append(depth)
                    if depth == -1:
                        break

                    byte >>= 1

                if depth == -1:
                    break

            self.charTrees.append(tree)
            self.charLists.append(chars)


    def DcmprssTxt(self,textIndex):
        indexAddr = self.cmprssd_base + (textIndex >> 8 << 3)
        cmprssd_data_addr = self.read(indexAddr,3)
        byte_len_tbl = self.read(indexAddr + 4,3)
        textIndex &= 0xFF

        i = 0
        while i < textIndex:
            byte_len = self.buffer[byte_len_tbl + i]
            cmprssd_data_addr += byte_len
            if byte_len != 0xFF: i += 1

        out = ""
        previousChar = 0
        data = 0x100 | self.buffer[cmprssd_data_addr]

        while True:
            tree = self.charTrees[previousChar]
            chars = self.charLists[previousChar]

            treePos = 0
            depth = 0
            while tree[treePos] >= depth:
                if data & 1:
                    treePos = tree.index(depth,treePos+1)
                else:
                    depth += 1
                data >>= 1
                if data == 1:
                    cmprssd_data_addr += 1
                    data = 0x100 | self.buffer[cmprssd_data_addr]
                treePos += 1

            previousChar = chars[treePos]
            char = previousChar & 0xFF
            if char == 0:
                break
            elif char >= 32 and char <= 127:
                out += chr(char)
            else:
                out += "{" + str(char) + "}"

        return out

    # Patches rom with decompressed text:
    # - Offset table for reading text
    # - Decompressed text
    def write(self):

        offset = 0x800000
        addr_start = 0x80a7f0
        addr = addr_start

        for ti in self.lines:

            # Write offsets
            self.buffer[offset:offset+4] = (addr-addr_start).to_bytes(4, byteorder='little')
            offset += 4

            # Write text
            t1 = ti.split('{')
            for tj in t1:
                t2 = tj.split('}')
                for tk in t2:
                    if tk.isdigit():
                        self.buffer[addr] = int(tk)
                        addr += 1
                    else:
                        l = len(tk)
                        self.buffer[addr:addr+l] = bytearray(tk,'ascii')
                        addr += l
            self.buffer[addr] = 0
            addr += 1



def decompress(rom):

    #######################################
    # Patch rom to read decompressed text #
    #######################################

    hack = Utilities.open_bin('asm/text.bin')
    addr = 0x15430
    size = len(hack)
    rom.buffer[addr:addr+size] = hack

    hack = Utilities.open_bin('asm/arguments.bin')
    addr = 0x15570
    size = len(hack)
    rom.buffer[addr:addr+size] = hack

    ###################
    # Decompress text #
    ###################

    text = Text(rom.buffer)

    return text
