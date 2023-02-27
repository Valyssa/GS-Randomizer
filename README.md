**VERSION 2.0 CHANGES**

The original randomizer was made by MarvinXLII, but has now been
expanded upon by Valyssa. Minor changes were made but mostly options
were added. Marvin has given me permission to update and release this
updated version of the randomizer and was even kind enough to share
the source code with me.

**CHANGES COMPARED TO THE ORIGINAL**

- The altered functionality of Avoid (working as a full-proof encounter
toggle) was made optional and added variable PP cost.

- The altered functionality of Retreat (world map teleportation+works
everywhere) was made optional and added variable PP cost.

**MAJOR NEW FEATURES**

- Enemy movesets can be randomized. Low level mobs tend to have more
attack slots filled with basic attacks, while high level mobs are
guaranteed to have more abilities to make them more threatening.
Bosses have a smaller pool of random abilities to make them more
dangerous and exclude moves that wouldn't work for most bosses, such
as ally search.
There is logic in place to limit damaging moves based on the enemy's
Attack stat, to ensure their abilities aren't too strong or too weak.

- Your own psynergy learning curve can be rebalanced to ensure early
access to abilities, and ensuring everything is learned by level 30
at most.

- Psynergy can be randomized too, such as making 1/5 abilities
non-elemental or randomizing ability ranges by +- 1 step. Random
psynergy can also be assigned to psynergy items, so for example Oil
Drop could end up casting Eruption.

- Luck growth can be assigned to the playable characters so that it
slightly grows by level as normal stats do.

- When shuffling djinn, there is now an option to sort fights by
difficulty to ensure weaker djinn are fought earlier in the game and
tougher djinn later. Note that the weakest Venus djinni is still much
stronger than the weakest Mars Djinni, so be wary.

- Separate fields were implemented to scale coins/exp for bosses,
rather than always being 1x like before.

- Cosmetic randomizations, such as character portraits, names and
enemy colour palettes are available!

- Consumables can be shuffled around entirely, so your starting Herbs
can be different items, and shop contents will be different too. This
is a super basic form of drop/chest/hidden item randomization, but has
some fun possibilities in its own right!

- Optional challenge modifiers were added, such as rebalancing prices
of inns or consumables, and the option to disable selling of items.
There are options to make summons cost more djinn, be weaker or even do
Nothing except raise elemental power.
There's also a single character challenge available, where Garet, Ivan
and Mia have 0 max HP. Most of these challenges are part of the IronSUN
ruleset! (https://docs.google.com/document/d/1tlf_IM8l9saSeFlMpE4S76A6L9mpcASt2XBjZdG5qIA/)

**RECOMMENDATIONS**

If you want the optimal gameplay-focussed experience, you should first
make a ROM with Marvin's standalone No Cutscene Patch and use that as
the base for randomization, as the built-in dialogue suppression option
doesn't work as well as the patch.
If you want to run the randomizer from source I recommend using Python
version 3.10.1. Running gui.py will start the application.

**DISCLAIMER**

Valyssa is an amateur programmer, so a lot of this code is not optimal.
Features were tested pretty thoroughly though and they should all work
as intended. Just don't judge the quality of the code too hard pls and
run the software at your own risk.
Also none of these new features write to the cheat logs, so if you want
to investigate enemy movesets or stats, you're best off throwing the
ROM into the Golden Sun TLA Editor and viewing them there.

**FUTURE IDEAS**

I do have more ideas for this project, but they would require a lot more
work which I'm not sure I'll end up doing. Here's some:
- More/scaling Djinn fights, so there's a properly tuned fight for each
element at each location
- Proper chest/hidden item randomization (with some logic)
- Skipping more cutscenes entirely by pre-emptively setting flags
- Better/cleaner implementation of some existing feature
- More cosmetic stuff like random class and item/gear names

**KNOWN ISSUES**
- Sometimes an item description describes an effect that's not fully
present, such as "Resists all elements" but it only resists 2. This is
due to how some effects are transferred to weapons instead
- Item use effects aren't described if there's an equip effect. This was
done due to the description length limitation, but it would still be nice
to fix eventually
- Shirts, boots and rings aren't currently added to the pool of gear
customization
- Bilibin Barricade had been removed to make room for a Crossbone Isle map
dot. Inherently this is inconvenient as it misses out on Jill's reward,
but I'd at least like for it to be restored if the altered Retreat
functionality isn't used.

Original Readme Below
-----------------------------------------------

**ABOUT**

This is a randomizer for Golden Sun. It randomizes key items, djinn,
summons, classes, PC stats, and equipment characteristics. It also
features use of Retreat in the overworld to facilitate backtracking,
and dialogue suppression to speed up cutscenes.


**CHANGES TO THE BASE GAME:**

Several changes are made regardless of any options chosen:

- Additional default psynergy: Garet knows Growth and Avoid; Ivan
  knows Whirlwind; and Mia knows Ply.

- Avoid costs 0 PP, toggles on/off, and works anywhere at any PC level.

- Retreat costs 0 PP, works everywhere (except Colosso and the Tolbi
  boat), and works like Teleport in the Overworld.

- The Bilibin Barricade is removed to make a dot on the World Map for
  Crossbone Isle. After your first visit, you can easily return with
  Retreat.

- Various modifications are made to Lalivero, primarily so that after
  completing Venus Lighthouse, an item (Black Orb by default) will be
  collected from Iodem and you can still leave Lalivero.


**ITEMS:**

The item randomizer shuffles key items: Catch Beads, Empty Bottle,
Dragon's Eye, Orb of Force, Douse Drop, Frost Jewel, Lifting Gem, Boat
Ticket, Anchor Charm, Mystic Draught, Cloak Ball, Halt Gem, Cell Key,
Red Key, Carry Stone, and the Black Orb. Instead of the Killer Ape
dropping Douse Drop, one of the following bosses will drop one item:
Kraken, Toadonpa, Storm Lizard, or Deadbeard. The game is beatable
once you have completed Venus Lighthouse and have the Black Orb.


**DJINN:**

Djinn and their stat bonuses can be shuffled.


**SUMMONS:**

Summon costs can be shuffled by element (e.g. Boreas could cost 4 Mars
djinn), and attack power can be randomly rescaled by up to 20%.


**CLASSES:**

The class randomizer shuffles psynergy either by swapping skillsets
between classlines or by completely randomizing them. Levels when
psynergy are learned can also be randomized (either shuffled or
rescaled by up to 20%). Stat boosts can also be shuffled between
classlines.

N.B.: Shuffling psynergy levels is not everyone's cup of tea. You can
acquire powerful psynergy really early, making bosses a bit too easy
and random battles too tedious with high PP costs.


**EQUIPMENT:**

Equipment is randomized by who can equip what along with price,
attack, and defense. Other options to shuffle unleashes, effects,
uses, and curses are included. Text descriptions are updated, giving
priority to unleashes, then effects, then uses. Detailed description
in game will always include effects. Check the cheat log for uses.


**PLAYABLE CHARACTERS:**

PC elements and their stats can be shuffled, and their starting levels
can be modifed as needed.


**DIALOGUE:**

There is an option to suppress most dialogue during cutscenes. This
mainly lessens button mashing, but also allows you to speed through
cutscenes in turbo mode.


**RANDOM ENCOUNTERS:**

These can be turned on and off with Avoid, i.e. when off, cast Avoid
again to turn them back on. To reduce grinding, money and experience
earned from battles can be rescaled from 0 to 99 times. This only
applies to random battles, not mandatory boss battles, in Lunpa, on
the Tolbi Boat, the Storm and Tornado Lizards of Suhulla Desert, and
in Crossbone Isle. A few of the enemies in Crossbone Isle are found
elsewhere, and the scalings still won't apply to them (at least for
now). These enemies are well spread out, so it's not as problematic as
you might think.


**MUSIC:**

Music can be shuffled. Right now it only works for towns, caves,
overworld, etc. not in random battles. 


**PROLOGUE/DJINN TUTORIAL:**

These can both be skipped. If selected, you start at the farewell
cutscene in Vale. The first djinn (Flint by default) will join your
party as soon as you walk by it.


**RUNNING FROM SOURCE:**

Running the randomizer requires Python 3.6+. Once installed, run

```py -3.6 -m pip install hjson``` (Windows)

```python3 -m pip install hjson``` (Mac/Linux)

Settings can be selected by modifying "template.json" and running

```py -3.6 randomizer.py template.json``` (Windows)

```python3 randomizer.py template.json``` (Mac/Linux)

You can also run the graphical user interface with

```py -3.6 gui.py``` (Windows)

```python3 gui.py``` (Mac/Linux)

If desired, you can generate your own exe of the gui:

```py -3.6 -m pip install pywin32-ctypes==0.2.0``` (Windows)

```py -3.6 -m pip install pyinstaller```

```py -3.6 -m PyInstaller randomizer.spec```

The exe will be in the ```dist``` directory.
