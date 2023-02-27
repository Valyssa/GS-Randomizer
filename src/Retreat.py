def retreat(rom, flags):
    rom.write_to_rom(0x807f7b1, [int(flags['RetreatCost'])], byte_length=1)

    if flags['Retreat']:
      # Modify script in Rom
      rom.write_to_rom(0x0808e724, [0x4c00, # ldr r4
                                    0x4720, # bx r4
                                    0x0f01,
                                    0x0889,
                                    ], byte_length=2)
      
      # Point to Retreat script
      rom.write_to_rom(0x08015144, [0x08890f41], byte_length=4)

      # Point to Retreat location update
      rom.write_to_rom(0x080153c4, [0x08890f81], byte_length=4)

      # Change text of Bilibin Barricade to Crossbone Isle
      rom.write_to_rom(0x0809decc, [0x3b], byte_length=1)

      # World map from crossbone isle (nowhere on map)
      rom.write_to_rom(0x0809C224, [0xda03], byte_length=2)
