def decompress(rom):

    # Point to decompression script
    rom.write_to_rom(0x0808ab48, [0xb500, 0xb401, 0x4800, 0x4700, 0x0101, 0x0889])
