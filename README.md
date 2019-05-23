# Dynamic-Pokemon-Expansion

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
