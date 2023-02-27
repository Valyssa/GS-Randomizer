def avoid(rom, text, flags):
    rom.write_to_rom(0x807f7c1, [int(flags['AvoidCost'])], byte_length=1) # Set Avoid PP cost to the selected amount

    if flags['Avoid']:
        # Step counter
        rom.write_to_rom(0x0808c15c, [0x0]) # Don't decrease step counter
        rom.write_to_rom(0x0809b6da, [0x4d01,  # ldr r5, =0x08891601
                                      0x4728]) # bx r5
        rom.write_to_rom(0x0809b6e0, [0x08891701], byte_length=4) # Pointer

        # Prints
        rom.write_to_rom(0x0809b7cc, [0x4700])
        rom.write_to_rom(0x0809b800, [0x08891601], byte_length=4) # Replace text line with pointer

        # Any level
        rom.write_to_rom(0x0808af14, [0xe000]) # b $0808af18

        # Text
        text.lines[0x922] = "Monsters won't attack{3}anymore.{2}"
        text.lines.append("Avoid's effects wore off.{2}")
    return
