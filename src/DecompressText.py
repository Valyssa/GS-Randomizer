# import sys
# sys.path.append('./src')
# import Rom


# rom = Rom.LocalRom(sys.argv[1])

# rom = []
# with open(sys.argv[1],"rb") as f:
#     rom = f.read()


class Text():
    def __init__(self, buffer):
        self.buffer = buffer
        self.HUFFMAN_PNTR = 0x03842c # table of addresses related to tree and char data, indexed by (previousChar >> 8)
        self.CMPRSSD_BASE = 0x0736b8 # table of addresses related to compressed data, indexed by (textIndex >> 8)
        self.charTrees = []
        self.charLists = []
        self.get_trees()
        self.lines = list(map(self.DcmprssTxt, range(0x29e2)))

    def read(self,addr,size): #assumes rom is arranged in little endian; reads "size" bytes at address "addr"
        return sum(self.buffer[addr + i] << 8*i for i in range(size))

    def get_trees(self):
        #previousChar is always less than 0x100 in GS though, so I didn't use it for indexing HUFFMAN_PNTR here
        char_data_base = self.read(self.HUFFMAN_PNTR,3)
        tree_offset_tbl = self.read(self.HUFFMAN_PNTR + 4,3) #table of 2-byte offsets relative to char_data_base, indexed by (previousChar & 0xFF)    

        #Constructs the char trees and char lists for each char up to 0xFF
        # charTrees = [] #list of trees; each tree is modified: +1 for each node, -1 for each leaf
        # charLists = [] #list of char lists; each char list is a dictionary in the format: {tree_leaf_index : char_num}
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
                        charPos += 1.5 #each char is allocated 12 bits (1.5 bytes), and are located relative to tree_addr
                        c = self.read(tree_addr - int(charPos + 0.5),2)
                        if charPos != int(charPos): chars[8*count+j] = c >> 4
                        else: chars[8*count+j] = c & 0xFFF
                    else: depth += 1
                    tree.append(depth)
                    if depth == -1: break
                    byte >>= 1
                if depth == -1: break
            self.charTrees.append(tree)
            self.charLists.append(chars)


    def DcmprssTxt(self,textIndex):
        #CMPRSSD_BASE is a table of pairs of pointers, which point to compressed data, and byte length tables
        indexAddr = self.CMPRSSD_BASE + (textIndex >> 8 << 3)
        cmprssd_data_addr = self.read(indexAddr,3)
        byte_len_tbl = self.read(indexAddr + 4,3)
        textIndex &= 0xFF

        #Navigates to address of compressed data by adding byte lengths of entries with lower textIndices
        i = 0
        while i < textIndex:
            byte_len = self.buffer[byte_len_tbl + i]
            cmprssd_data_addr += byte_len
            if byte_len != 0xFF: i += 1

        out = ""
        previousChar = 0
        data = 0x100 | self.buffer[cmprssd_data_addr] #first byte of compressed data; prepends a 1 to account for leading zeroes

        while True:
            tree = self.charTrees[previousChar]
            chars = self.charLists[previousChar]

            treePos = 0 #Current position in the tree
            depth = 0 #Each 0 in data increases depth by 1; each 1 jumps to the next treePos with equal depth

            while tree[treePos] >= depth: #if tree[treePos] < depth, then you've landed on a tree leaf
                if data & 1: treePos = tree.index(depth,treePos+1)
                else: depth += 1
                data >>= 1
                if data == 1:
                    cmprssd_data_addr += 1
                    data = 0x100 | self.buffer[cmprssd_data_addr]
                treePos += 1

            previousChar = chars[treePos]
            char = previousChar & 0xFF
            if char == 0: break
            elif char >= 32 and char <= 127: out += chr(char)
            else: out += "{" + str(char) + "}"

        return out


def decompress(rom):
    text = Text(rom.buffer)
    return text
    
# rom = Rom.LocalRom(sys.argv[1])
# text = Text(rom.buffer)
    
# # x = list(map(DcmprssTxt, range(0x29e2)))
# with open('gs_text.txt','w') as file:
#     for xi in text.lines:
#         file.write(xi)
#         file.write('\n')
