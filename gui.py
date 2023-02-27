from tkinter import *
from tkinter import filedialog
from randomizer import randomizer
import random
import sys
from os import path
import hjson

global filename
filename = ''

master = Tk()
master.title("Golden Sun Randomizer")

# CHANGE SIZE
master.geometry('760x856')

# Stuff
flags = {}
flags['File'] = StringVar()
flags['Seed'] = StringVar()
flags['Items'] = BooleanVar()
flags['Music'] = BooleanVar()
flags['CutDialogue'] = BooleanVar()
flags['PrologueSkip'] = BooleanVar()
flags['Coins'] = StringVar()
flags['Exp'] = StringVar()
flags['BossCoins'] = StringVar()
flags['BossExp'] = StringVar()
flags['Djinn'] = {'Djinn': BooleanVar(), 'Stats': BooleanVar(), 'DjinnBattles': BooleanVar(), 'DjinnAbilities': BooleanVar()}
flags['Summons'] = {'Djinn': BooleanVar(), 'Power': BooleanVar()}
flags['Equipment'] = {'Equipping': BooleanVar(), 'Price': BooleanVar(),
                      'Attack': BooleanVar(), 'Defense': BooleanVar(),
                      'Effects': BooleanVar(), 'Cursed': BooleanVar(),
                      'Unleashes': BooleanVar(), 'Uses': BooleanVar()}
flags['Classes'] = {'Stats': BooleanVar(), 'Psynergy': StringVar(),
                    'Levels': {'Random': BooleanVar(), 'Noise': BooleanVar(), 'Balanced': BooleanVar()}}
flags['PC'] = {'Elements': StringVar(), 'Stats': BooleanVar(),
               'Levels': {'Isaac': StringVar(), 'Garet': StringVar(),
                          'Ivan': StringVar(), 'Mia': StringVar()}}

flags['LuckGrowth'] = BooleanVar()
flags['Seed'].set(str(random.randint(0,999999)))
flags['Avoid'] = BooleanVar()
flags['AvoidCost'] = StringVar()
flags['Retreat'] = BooleanVar()
flags['RetreatCost'] = StringVar()
flags['Solo'] = BooleanVar()
flags['ExpensiveConsumables'] = BooleanVar()
flags['Inns'] = BooleanVar()
flags['Unsellable'] = BooleanVar()
flags['Palettes'] = BooleanVar()
flags['EnemyMovepools'] = BooleanVar()
flags['EnemyStats'] = BooleanVar()
flags['EnemyElements'] = BooleanVar()
flags['Names'] = BooleanVar()
flags['Portraits'] = BooleanVar()
flags['ExpensiveSummons'] = BooleanVar()
flags['NoDamageSummons'] = BooleanVar()
flags['LowDamageSummons'] = BooleanVar()
flags['BalancedDamageSummons'] = BooleanVar()
flags['NoPortableRevives'] = BooleanVar()
flags['AbilityPower'] = BooleanVar()
flags['AbilityCost'] = BooleanVar()
flags['AbilityRange'] = BooleanVar()
flags['NoElement'] = BooleanVar()
flags['PsynergyItems'] = BooleanVar()
flags['ShuffleConsumables'] = BooleanVar()


def call_randomizer():
    settings = {}
    flags2json(settings, flags)
    randomizer(settings)
    master.destroy()
    sys.exit()

def flags2json(d, f):
    for k, v in f.items():
        if isinstance(v, dict):
            d[k] = {}
            flags2json(d[k], v)
            continue
        if k in ['Seed', 'Isaac', 'Garet', 'Ivan', 'Mia']:
            d[k] = int(v.get())
        else:
            d[k] = v.get()

def json2flags(d, f):
    for k, v in d.items():
        if isinstance(v, dict):
            json2flags(v, f[k])
            continue
        f[k].set(v)

def load_settings(v):
    getfile(v, [('json', '*.json')])
    if v.get() == '':
        return

    with open(v.get(), 'r') as file:
        settings = hjson.load(file)

    json2flags(settings, flags)
    if flags['Classes']['Psynergy'].get() == 'None':
        pass
    else:
        psyn(1)
    if flags['PC']['Elements'].get() == 'None':
        pass
    else:
        elem(1)

def generate_new_seed():
    flags['Seed'].set(str(random.randint(0,999999)))


lf = LabelFrame(master, text='')
lf.grid(row=0, columnspan=15, sticky='nsew',\
        padx=5, pady=5, ipadx=5, ipady=5)


def getfile(textvar, filetypes):
    global filename
    filename = filedialog.askopenfilename(initialdir=path.dirname(__file__), filetypes=filetypes)
    textvar.set(filename)

# ROM    
inRomLbl = Label(lf, text='Select Rom:')
inRomLbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)

inRomGBA = Entry(lf, textvariable=flags['File'])
inRomGBA.grid(row=0, column=1, columnspan=4, sticky='WE', pady=3)

inRomBtn = Button(lf, text='Browse ...', command=lambda: getfile(flags['File'], [('GBA', '*.gba')]))
inRomBtn.grid(row=0, column=5, sticky='W', padx=5, pady=2)

# JSON        
inSetLbl = Label(lf, text='Load Settings:')
inSetLbl.grid(row=1, column=0, sticky='E', padx=5, pady=2)

v = StringVar()
inSetGBA = Entry(lf, textvariable=v)
inSetGBA.grid(row=1, column=1, columnspan=4, sticky='WE', pady=3)

inSetBtn = Button(lf, text='Browse ...', command=lambda: load_settings(v))
inSetBtn.grid(row=1, column=5, sticky='W', padx=5, pady=2)

# Seed
Label(lf, text='Seed:').grid(row=0, column=9, sticky=W, padx=30)
Spinbox(lf, from_ = 0, to = 999999, width=7, textvariable=flags['Seed']).grid(row=0, column=10, sticky=W)
Button(lf, text='Generate new seed', command=generate_new_seed).grid(row=1, column=9, columnspan=2, sticky=W, padx=30, ipadx=30)

# Run
patch = Button(lf, text='Randomize ROM', command=call_randomizer).grid(row=0, rowspan=2, column=12, columnspan=3, sticky=W, padx=30, ipadx=30, ipady=15)


labelfonts = ('Helvetica', 14, 'bold')


lf = LabelFrame(master, text='Cosmetic', font=labelfonts)
lf.grid(row=1, rowspan=2, column=10, columnspan=5, sticky='nsew', padx=5, pady=5, ipadx=5, ipady=5)
Checkbutton(lf, text='Shuffle music', variable=flags['Music']).grid(row=0, sticky=W)
Checkbutton(lf, text='Random enemy palettes', variable=flags['Palettes']).grid(row=1, sticky=W)
Checkbutton(lf, text='Random character names', variable=flags['Names']).grid(row=2, sticky=W)
Checkbutton(lf, text='Shuffle character portraits', variable=flags['Portraits']).grid(row=3, sticky=W)

lf = LabelFrame(master, text='Djinn', font=labelfonts)
lf.grid(row=2, column=0, columnspan=5, sticky='nsew', padx=5, pady=5, ipadx=5, ipady=5)
djinn = flags['Djinn']
Checkbutton(lf, text='Shuffle djinn', variable=djinn['Djinn']).grid(row=0, sticky=W)
Checkbutton(lf, text='Sort fights by difficulty', variable=djinn['DjinnBattles']).grid(row=0, column=1, sticky=W)
Checkbutton(lf, text='Shuffle stat boosts', variable=djinn['Stats']).grid(row=1, sticky=W)
Checkbutton(lf, text='Randomize Djinn abilities', variable=djinn['DjinnAbilities']).grid(row=1, column=1, sticky=W)

lf = LabelFrame(master, text='Summons', font=labelfonts)
lf.grid(row=2, column=5, columnspan=5, sticky='nsew', padx=5, pady=5, ipadx=5, ipady=5)
summons = flags['Summons']
Checkbutton(lf, text='Shuffle summon requirements', variable=summons['Djinn']).grid(row=0, sticky=W)
Checkbutton(lf, text='Randomize ability power\u00b9', variable=summons['Power']).grid(row=1, sticky=W)

lf = LabelFrame(master, text='Classes', font=labelfonts)
lf.grid(row=3, column=0, columnspan=5, sticky='nsew', padx=5, pady=5, ipadx=5, ipady=5)
classes = flags['Classes']
Checkbutton(lf, text='Shuffle stat boosts', variable=classes['Stats']).grid(row=0, sticky=W)

def update_state_psynergy(lst):
    if lst[0]['state'] == 'normal':
        for li in lst:
            li.config(state=DISABLED)
        flags['Classes']['Psynergy'].set('None')
    else:
        for li in lst:
            li.config(state=NORMAL)
    for li in lst:
        li.grid()

swap_class_psynergy = IntVar()
def psyn(val=None):
    if val is not None:
        swap_class_psynergy.set(True)
    lst = [psyn1, psyn2]
    update_state_psynergy(lst)
    
psyn1 = Radiobutton(lf, text="Shuffle classlines", variable=flags['Classes']['Psynergy'], value='Shuffle', padx=15, state=DISABLED)
psyn1.grid(row=2, sticky=W, padx=15)
psyn2 = Radiobutton(lf, text="Completely randomize", variable=flags['Classes']['Psynergy'], value='Random', padx=15, state=DISABLED)
psyn2.grid(row=3, sticky=W, padx=15)
flags['Classes']['Psynergy'].set(None)

Checkbutton(lf, text="Shuffle psynergy skillsets", variable=swap_class_psynergy, command=psyn).grid(row=1, sticky=W)

levels = classes['Levels']
Label(lf, text="Levels for learning psynergy:").grid(row=4, column=0, padx=10, sticky=W)
Checkbutton(lf, text='Shuffle levels', variable=levels['Random']).grid(row=5, column=0, padx=30, sticky=W)
Checkbutton(lf, text='Randomize levels\u00b9', variable=levels['Noise']).grid(row=6, column=0, padx=30, sticky=W)
Checkbutton(lf, text='Balance levels\u00b3', variable=levels['Balanced']).grid(row=7, column=0, padx=30, sticky=W)


lf = LabelFrame(master, text='Equipment', font=labelfonts)
lf.grid(row=3, column=5, columnspan=5, sticky='nsew', padx=5, pady=5, ipadx=5, ipady=5)
equipment = flags['Equipment']
Checkbutton(lf, text='Randomize equipping flags', variable=equipment['Equipping']).grid(row=0, sticky=W)
Checkbutton(lf, text='Randomize price\u00b9', variable=equipment['Price']).grid(row=1, column=0, sticky=W)
Checkbutton(lf, text='Randomize attack\u00b9', variable=equipment['Attack']).grid(row=2, column=0, sticky=W)
Checkbutton(lf, text='Randomize defense\u00b9', variable=equipment['Defense']).grid(row=3, column=0, sticky=W)
Checkbutton(lf, text='Shuffle curses', variable=equipment['Cursed']).grid(row=4, sticky=W)
Checkbutton(lf, text='Shuffle effects', variable=equipment['Effects']).grid(row=5, sticky=W)
Checkbutton(lf, text='Shuffle unleashes', variable=equipment['Unleashes']).grid(row=6, sticky=W)
Checkbutton(lf, text='Shuffle uses', variable=equipment['Uses']).grid(row=7, sticky=W)


lf = LabelFrame(master, text='Enemy Reward Multiplier', font=labelfonts)
lf.grid(row=4, column=0, columnspan=5, sticky='nsew', padx=5, pady=5, ipadx=5, ipady=5)
Label(lf, text="Normal enemy coins:").grid(row=0, column=0, sticky='w',padx=5)
Label(lf, text="Normal enemy exp:").grid(row=1, column=0, sticky='w',padx=5)
flags['BossCoins'].set("1")
flags['BossExp'].set("1")
Spinbox(lf, from_ = 0, to = 99, width=3, textvariable=flags['BossCoins']).grid(row=0, column=1, sticky=W)
Spinbox(lf, from_ = 0, to = 99, width=3, textvariable=flags['BossExp']).grid(row=1, column=1, sticky=W) 
Label(lf, text="Boss coins:").grid(row=0, column=2, sticky='w',padx=5)
Label(lf, text="Boss exp:").grid(row=1, column=2, sticky='w',padx=5)
flags['Coins'].set("1")
flags['Exp'].set("1")
Spinbox(lf, from_ = 0, to = 99, width=3, textvariable=flags['Coins']).grid(row=0, column=3, sticky=W)
Spinbox(lf, from_ = 0, to = 99, width=3, textvariable=flags['Exp']).grid(row=1, column=3, sticky=W)


lf = LabelFrame(master, text='Items', font=labelfonts)
lf.grid(row=4, column=5, columnspan=5, sticky='nsew', padx=5, pady=5, ipadx=5, ipady=5)
Checkbutton(lf, text='Randomize key items', variable=flags['Items']).grid(row=0, sticky=W)
Checkbutton(lf, text='Shuffle similar basic items', variable=flags['ShuffleConsumables']).grid(row=1, sticky=W)


lf = LabelFrame(master, text='Quality of Life', font=labelfonts)
lf.grid(row=4, column=10, columnspan=5, sticky='nsew', padx=5, pady=5, ipadx=5, ipady=5)
Checkbutton(lf, text='Suppress (most) dialogue', variable=flags['CutDialogue']).grid(row=0, sticky=W)
Checkbutton(lf, text='Skip prologue and djinn tutorial', variable=flags['PrologueSkip']).grid(row=1, sticky=W)


lf = LabelFrame(master, text='Abilities', font=labelfonts)
lf.grid(row=5, column=10, columnspan=5, sticky='nsew', padx=5, pady=5, ipadx=5, ipady=5)
Checkbutton(lf, text='Randomize ability power\u00b9', variable=flags['AbilityPower']).grid(row=0, sticky=W)
Checkbutton(lf, text='Randomize ability PP cost\u00b9', variable=flags['AbilityCost']).grid(row=1, sticky=W)
Checkbutton(lf, text='Randomize range by +-1', variable=flags['AbilityRange']).grid(row=2, sticky=W)
Checkbutton(lf, text='1/5 abilities are non-elemental', variable=flags['NoElement']).grid(row=3, sticky=W)
Checkbutton(lf, text='Randomize psy item abilities', variable=flags['PsynergyItems']).grid(row=4, sticky=W)


lf = LabelFrame(master, text='Playable Characters', font=labelfonts)
lf.grid(row=5, column=0, columnspan=10, sticky='nsew', padx=5, pady=5, ipadx=5, ipady=5)
li = Label(lf, text=82*' ', state='disabled')
li.grid(row=0, column=0)

pc = flags['PC']
Checkbutton(lf, text='Shuffle stats', variable=pc['Stats']).grid(row=0, columnspan=5, sticky=W)

def update_state_elements(lst):
    if lst[0]['state'] == 'normal':
        for li in lst:
            li.config(state=DISABLED)
        flags['PC']['Elements'].set('None')
    else:
        for li in lst:
            li.config(state=NORMAL)
    for li in lst:
        li.grid()

swap_pc_elements = IntVar()
def elem(val=None):
    if val is not None:
        swap_pc_elements.set(True)
    lst = [elem1, elem2]
    update_state_elements(lst)

elem1 = Radiobutton(lf, text="Shuffle (no repeats)", variable=flags['PC']['Elements'], value='Shuffle', padx=15, state=DISABLED)
elem1.grid(row=2, sticky=W, padx=15)
elem2 = Radiobutton(lf, text="Randomize (allow repeats)", variable=flags['PC']['Elements'], value='Random', padx=15, state=DISABLED)
elem2.grid(row=3, sticky=W, padx=15)
flags['PC']['Elements'].set(None)

Checkbutton(lf, text="PC Elements", variable=swap_pc_elements, command=elem).grid(row=1, sticky=W)
Checkbutton(lf, text="Assign luck growth", variable=flags['LuckGrowth']).grid(row=4, sticky=W)


Label(lf, text="Starting Levels:").grid(row=0, column=1, sticky=E)
Label(lf, text="Isaac:    ").grid(row=1, column=1, sticky='news')
Label(lf, text="Garet:    ").grid(row=2, column=1, sticky='news')
Label(lf, text="Ivan:     ").grid(row=3, column=1, sticky='news')
Label(lf, text="Mia:      ").grid(row=4, column=1, sticky='news')
levels = pc['Levels']
levels['Isaac'].set("1")
levels['Garet'].set("1")
levels['Ivan'].set("4")
levels['Mia'].set("10")
w4 = Spinbox(lf, from_ = 1, to = 99, width=3, textvariable=levels['Isaac']).grid(row=1, column=2, sticky=W)
w5 = Spinbox(lf, from_ = 1, to = 99, width=3, textvariable=levels['Garet']).grid(row=2, column=2, sticky=W) 
w6 = Spinbox(lf, from_ = 1, to = 99, width=3, textvariable=levels['Ivan']).grid(row=3, column=2, sticky=W)
w7 = Spinbox(lf, from_ = 1, to = 99, width=3, textvariable=levels['Mia']).grid(row=4, column=2, sticky=W)
lf.columnconfigure(4, weight=1)

lf = LabelFrame(master, text='Utility', font=labelfonts)
lf.grid(row=1, column=0, columnspan=5, sticky='nsew', padx=5, pady=5, ipadx=5, ipady=5)
Checkbutton(lf, text='Avoid toggles encounters', variable=flags['Avoid']).grid(row=0, sticky=W)
Label(lf, text="Avoid PP:").grid(row=0, column=1, sticky='w', padx=5)
flags['AvoidCost'].set("5")
Spinbox(lf, from_ = 0, to = 255, width=3, textvariable=flags['AvoidCost']).grid(row=0, column=2, sticky='w')
#Checkbutton(lf, text='0 PP Avoid', variable=flags['FreeAvoid']).grid(row=0, column=1, sticky=W)
Checkbutton(lf, text='Retreat anywhere + teleport', variable=flags['Retreat']).grid(row=1, sticky=W)
Label(lf, text="Retreat PP:").grid(row=1, column=1, sticky='w', padx=5)
flags['RetreatCost'].set("6")
Spinbox(lf, from_ = 0, to = 255, width = 3, textvariable=flags['RetreatCost']).grid(row=1, column=2, sticky='w')
#Checkbutton(lf, text='0 PP Retreat', variable=flags['FreeRetreat']).grid(row=1, column=1, sticky=W)

lf = LabelFrame(master, text='Challenge', font=labelfonts)
lf.grid(row=3, column=10, columnspan=5, sticky='nsew', padx=5, pady=5, ipadx=5, ipady=5)
Checkbutton(lf, text='No Portable Revives', variable=flags['NoPortableRevives']).grid(row=0, columnspan=3, sticky=W)
Checkbutton(lf, text='Solo Isaac', variable=flags['Solo']).grid(row=1, columnspan=3, sticky=W)
Checkbutton(lf, text='Unsellable Items', variable=flags['Unsellable']).grid(row=2, columnspan=3, sticky=W)
Checkbutton(lf, text='Expensive Consumables', variable=flags['ExpensiveConsumables']).grid(row=3, columnspan=3, sticky=W)
Checkbutton(lf, text='Expensive Inns', variable=flags['Inns']).grid(row=4, columnspan=3, sticky=W)
Checkbutton(lf, text='Expensive Summons (1/2/4/6)', variable=flags['ExpensiveSummons']).grid(row=5, columnspan=3, sticky=W)
Label(lf, text="Summon damage:").grid(row=6, column=0, columnspan=3, padx=10, sticky=W)
Checkbutton(lf, text='None', variable=flags['NoDamageSummons']).grid(row=7, column=0, sticky=W)
Checkbutton(lf, text='Low', variable=flags['LowDamageSummons']).grid(row=7, column=1, sticky=W)
Checkbutton(lf, text='Balanced', variable=flags['BalancedDamageSummons']).grid(row=7, column=2, sticky=W)

lf = LabelFrame(master, text='Enemies', font=labelfonts)
lf.grid(row=1, column=5, columnspan=5, sticky='nsew', padx=5, pady=5, ipadx=5, ipady=5)
Checkbutton(lf, text='Randomize Movepools\u00b2', variable=flags['EnemyMovepools']).grid(row=0, sticky=W)
Checkbutton(lf, text='Randomize Enemy Stats\u00b9', variable=flags['EnemyStats']).grid(row=1, sticky=W)
#Checkbutton(lf, text='Shuffle Elemental Affinity', variable=flags['EnemyElements']).grid(row=2, sticky=W)

canvas=Canvas()
canvas.grid(row=6, column=0, columnspan=10)
L = Label(canvas, text='\u00b9 Randomly computes a new value between 80%-120% of the original value'+' '*42)
L.grid(row=1, columnspan=10, sticky='w')
L = Label(canvas, text='\u00b2 Has logic to prevent completely unfair situations'+' '*42)
L.grid(row=2, columnspan=10, sticky='w')
L = Label(canvas, text='\u00b3 Learn new psynergy consistently and ensure everything learned by level 30'+' '*42)
L.grid(row=3, columnspan=10, sticky='w')


mainloop()
