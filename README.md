# Dynamic-Pokemon-Expansion

## What is this:
A dynamic data inserter for expanding Pokemon in FireRed.

## Features:
* Dynamic insertion, meaning no worrying about repointing ever!
* Support for as many different Pokemon (regular Pokemon, forms, etc.) as you'd like.
* Support for different gendered forms.
* Support for different form Pokedex entries like in Sun/Moon.
* Support for up to 999 different Pokedex entries (not including alternate forms).
* Support for Pokemon sprite and icon insertion.
* Support for cry insertion (increases first time compilation, but always compiles quickly after that).

**NOTE** It is highly recommended to apply the [Complete Fire Red Upgrade](https://github.com/Skeli789/Complete-Fire-Red-Upgrade) following the insertion of this hack. Otherwise, make sure to comment out the  line ``#define EXPAND_LEARNSETS`` in the defines file or your game will crash.  Additonally, if you're **not** using the Complete Fire Red Upgrade, in [bytereplacement] (https://github.com/Skeli789/Dynamic-Pokemon-Expansion/blob/master/bytereplacement), find the changes for the seen  and caught flag ram, and change it to some free  save space. Make sure to apply a saveblock hack first, though.

## Installation Instructions:
```
1. Download devkitpro. Follow the instructions.
(Note: you can only install devkitARM)
For Windows users, follows steps 4-6 from this tutorial:
https://www.pokecommunity.com/showpost.php?p=8825585&postcount=96

2. Download the latest version of python (3.7.2).
After downloading and before proceeding to install make sure that the 'add to path' 
checkbox is ticked, otherwise you'll have to add the python path in the environment 
variables manually.

**NOTE**: If a python version lower than 3.6 is installed, you'll need to uninstall it and manually
remove it from your path before installing the newer version of Python.

3. Download the master folder from this github page.
(click 'Clone or Download', then 'Download Zip')

4. Get your ROM, rename it BPRE0.gba and 
place it the main (master) folder.

5. To decide the offsets where you want to insert the code:

a) In the 'make.py' file in the folder 'scripts' change OFFSET_TO_PUT=YYY to the location 
   you want to insert the data (let it be X). Don't worry about changing 'insert.py' also.
   'make.py' automatically updates the 'insert.py' file and linker file.
 
7. Run cmd.exe in the main folder. You can do this by typing 'cmd' and hitting enter in the 
url address or selecting 'run command prompt from here' from right clciking on empty space 
while holding the shift key.

8. In command prompt window, type 'python scripts//data_extractor.py'
This extracts the graphics data from BPRE0.gba and places it in the
directory *extracted*. Make sure to update the files in *src* with
this extracted data. Do not overwrite the files in *src*. Only replace
Pokemmon that are in your hack. Leave the expanded graphics data alone.

9. Once you're done editing the source files, in the command prompt window, 
type 'python scripts//make.py'
  
A new gba file will appear named as test.gba and an offsets.ini file.
That is your resultant file.
```
## Inserting Sprites:
There are two ways of inserting sprites with this hack. 
1. The first is to place the image file in the appropriate section found in [graphics](https://github.com/Skeli789/Dynamic-Pokemon-Expansion/tree/master/graphics). Images placed there will be compiled automatically by the compiler. To refer to any of the images in the code, first place a reference near the top of the file to the image with the following format: ``extern u32 [IMAGE_NAME]Tiles;``. For example, if you have a *Charmander* front sprite named ``CharmanderFront.png``, the reference would look like this: ``extern u32 CharmanderFrontTiles;``. Then, replace the old front pic table entry for *Charmander*, with a new entry like this: ``[SPECIES_CHARMANDER] = {CharmanderFrontTiles, 0x800, SPECIES_CHARMANDER},``. Palettes can similarly be done by replacing ``Tiles`` with ``Pal``. This method may be convenient, however, many of the sprites found online will not be in the required format to do this easily. Therefore, the second method is recommened.
2. The second method involves using the [Advance Series](https://hackromtools.altervista.org/advance-series/) to insert sprites. If you would like to use this, open up the generated ``offsets.ini`` found in the root, and edit the offsets in the A-Series ini to resemble the following (where the ``**`` refer to offsets found in ``offsets.ini``):
```
GameCode=BPRE
FrontSpriteTable=**gMonFrontPicTable**
BackSpriteTable=**gMonBackPicTable**
FrontPaletteTable=**gMonPaletteTable**
BackPaletteTable=**gMonShinyPaletteTable**
EnemyYTable=**gMonFrontPicCoords**
PlayerYTable=**gMonBackPicCoords**
EnemyAltitudeTable=**gEnemyMonElevation**
IconSpriteTable=**gMonIconTable**
IconPaletteTable=**gMonIconPaletteIndices**
IconPalettes=0x3D3740
SpeciesNames=**gSpeciesNames**
TotalSpecies=[The same NUMBER as NUM_SPECIES found in include/species.h]
```
Once you are content with your sprite data, and you'd like to continue editing offsets with this hack without overwriting the offsets set by A-Series, then make sure you take a look at ``Extracting Data`` below.

Different pokemon sprites that can be used with A-Series:
* [Pokemon Sprites Gens 1 - 5](https://www.pokecommunity.com/showthread.php?t=267728)
* [Pokemon Sprites Gen 6](https://www.pokecommunity.com/showthread.php?t=314422)
* [Pokemon Sprites Gen 7](https://www.pokecommunity.com/showthread.php?t=368703)
* [Pokemon Sprites Sugimori Palettes](https://www.pokecommunity.com/showthread.php?t=336945)

## Extracting Data:
When inserting Pokemon sprites, you may find it easier to use the Advance Series. If so, and you wish to keep modifying the data with this engine, you will need to extract the new graphics data pointers from your rom. To to do this, overwrite the ``BRPE0.gba`` file in the root with this new rom that has the updated graphics data (always make a backup first!). Then, open [scripts/data_extractor.py](https://github.com/Skeli789/Dynamic-Pokemon-Expansion/blob/master/scripts/data_extractor.py) and change the line ``NumberOfPokemon`` to the number of species in your rom + 1. Go back to the root, open the command line, and type ``python scripts//data_extractor.py``. Extracted graphics and cry data will be pulled from your rom and placed in a new folder ``extracted``. Copy the contents of the **tables** found in these files and overwrite the **tables** found in the equivalent files found in [src](https://github.com/Skeli789/Dynamic-Pokemon-Expansion/tree/master/src). Now, the next time you insert this hack, all of your graphics and cry pointers will remain unchanged, allowing you to make changes to things such as the Pokedex data and level-up movesets without worrying about repointing anything.
