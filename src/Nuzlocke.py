isaac_base_luck = 3
garet_base_luck = 2
ivan_base_luck = 4
mia_base_luck = 5
isaac_luck_address = 0x84578
garet_luck_address = 0x8462C
ivan_luck_address = 0x846E0
mia_luck_address = 0x84794


def ironman(rom, flags):
    if flags['Solo']:
        rom.write_to_rom(0x845F0, [0], byte_length=12) # Set Garet Max HP growth to 0
        rom.write_to_rom(0x846A4, [0], byte_length=12) # Set Ivan Max HP growth to 0
        rom.write_to_rom(0x84758, [0], byte_length=12) # Set Mia Max HP growth to 0
        rom.write_to_rom(0x848C0, [0], byte_length=12) # Set Jenna Max HP growth to 0
        print("Solo Isaac Mode Enabled")
    return

def luck_growth(rom, flags):
    if not flags['LuckGrowth']:
        return

    for i in range(6):
        rom.write_to_rom((isaac_luck_address+i), [isaac_base_luck+isaac_base_luck*i], byte_length=1) # Assign luck growth to Isaac
        rom.write_to_rom((garet_luck_address+i), [garet_base_luck+garet_base_luck*i], byte_length=1) # Assign luck growth to Garet
        rom.write_to_rom((ivan_luck_address+i), [ivan_base_luck+ivan_base_luck*i], byte_length=1) # Assign luck growth to Ivan
        rom.write_to_rom((mia_luck_address+i), [mia_base_luck+mia_base_luck*i], byte_length=1) # Assign luck growth to Mia
    print("Assigned luck growth to PCs")

def expensive_inns(rom, flags):
    if not flags['Inns']:
        return
    inn_address = 0xB4AB6
    for i in range(12):
        rom.write_to_rom(inn_address+i, [10*(i+1)], byte_length=1)
    print('Expensive Inns Enabled')

def summon_requirements(rom, flags):
    if flags['ExpensiveSummons']:
        new_cost = [1,1,1,1,2,2,2,2,4,4,4,4,6,6,6,6]
        for i in range(16):
            rom.write_to_rom(0x84AA0+(i%4)+(i*0x8), [new_cost[i]], byte_length=1)
        print('Expensive Summons Enabled')
