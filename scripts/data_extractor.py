#!/usr/bin/env python3

import os 

############
#Options go here.
############

ROM_NAME = "BPRE0.gba"  #the name of your rom
NumberOfPokemon = 440 #Change to total number of species in original rom

OutputFolder = os.getcwd() + "/extracted/"
SpeciesDefines = os.getcwd() + "/include/species.h"

############
#Code
############

def GeneralTableExtractor(dynamicOffset, definesDict, definesDict2, outputPath, tableType, tableName, 
                          indexOffset, tableLengthName, startIndex, numEntries, entryLength, alignData):
    output = open(outputPath, 'w')
    startIndexName = ""
    
    if startIndex != 0:
        startIndexName = " - " + indexOffset
    
    dataAlignment = 0
    if alignData:
        dataAlignment = GetLengthOfLongestValue(definesDict)
    
    with open(ROM_NAME, 'rb') as binary_file:
    
    #Load Dynamic Pointer to Table
        binary_file.seek(dynamicOffset)
        line = binary_file.read(3)
        TablePointer = ExtractPointer(line)
        
        output.write('#include "defines.h"\n\n')
        output.write(tableType + ' ' + tableName + '[' + tableLengthName + startIndexName + '] =\n{\n')
        
        for i in range(startIndex, numEntries):
            binary_file.seek(TablePointer + ((i - startIndex) * entryLength))
            byteList = binary_file.read(entryLength)
            
            if i in definesDict:
                output.write('\t[' + definesDict[i] + startIndexName + '] = ')
                lenEntry = len(definesDict[i] + startIndexName)
            else:
                output.write('\t[' + str(i) + startIndexName + '] = ')
                lenEntry = len(str(i) + startIndexName)
                
            while lenEntry < dataAlignment: #Align Data
                output.write(' ')
                lenEntry += 1
                
            data = ExtractPointer(byteList)
            if definesDict2 is not False and data in definesDict2:
                data = definesDict2[data]
            else:
                data = hex(data)
            
            output.write(data + ',\n')
            
        output.write('};\n')
    
    output.close()
    print("Success!")

def GeneralStructTableExtractor(dynamicOffset, definesDict, outputPath, tableType, tableName, tableLengthName, 
                                numEntries, structLength, memberNames, memberLengths, memberDicts, useMemberNames,
                                loadDictDataFromIndex, offsetForForce):
    assert(len(memberNames) == len(memberLengths) or not useMemberNames)
    output = open(outputPath, 'w')
    with open(ROM_NAME, 'rb') as binary_file:
    
    #Load Dynamic Pointer to Table
        binary_file.seek(dynamicOffset)
        line = binary_file.read(3)
        TablePointer = ExtractPointer(line)
        
        output.write('#include "defines.h"\n\n')
        output.write(tableType + ' ' + tableName + '[' + tableLengthName + '] =\n{\n')
        
        for i in range(numEntries):
            binary_file.seek(TablePointer + (i * structLength))
            byteList = binary_file.read(structLength)
            
            lenName = 0
            if i in definesDict:
                output.write('\t[' + definesDict[i] + '] =')
                lenName = len(definesDict[i])
            else:
                output.write('\t[' + str(i) + '] =')
                lenName = len(str(i))

            if useMemberNames:
                output.write('\n\t{\n')
            else:
                while lenName < 28: #Align structs
                    output.write(' ')
                    lenName += 1

                output.write(' {')
             
            for j in range(len(memberLengths)):
                data = int(ExtractPointer(byteList[:memberLengths[j]]))
                if memberDicts != [] and memberDicts[j] is not False:
                    if loadDictDataFromIndex: 
                        if i in memberDicts[j]:
                            data = memberDicts[j][i]
                        else:
                            data = hex(data)
                            
                        if offsetForForce > 0:
                            data += ' + ' + str(offsetForForce)
                    elif data in memberDicts[j]:
                        data = memberDicts[j][data]
                    else:
                        data = hex(data)
                else:
                    data = hex(data)
                
                if useMemberNames:
                    output.write('\t\t.' + memberNames[j] + ' = ' + str(data) + ',\n')
                elif j + 1 < len(memberLengths):
                    output.write(str(data) + ', ')
                else:
                    output.write(str(data))
                    
                byteList = byteList[memberLengths[j]:]
                
            if i + 1 == numEntries: #Last iteration of loop
                if useMemberNames:
                    output.write('\t},\n};\n')
                else:
                    output.write('},\n};\n')
            else:
                if useMemberNames:
                    output.write('\t},\n')
                else:
                    output.write('},\n')
    
    output.close()
    print("Success!")

def ExtractPointer(line):
    offset = 0
    for i in range(len(line)):
        offset += (line[i] << (8 * i))
    return offset

def DefinesDictMaker(definesFile):
    definesDict = {}
    with open(definesFile, 'r') as file:
        for line in file:
            if '#define ' in line:
                linelist = line.split()
                try:
                    definesDict[int(linelist[2])] = linelist[1]
                except:
                    try:
                        definesDict[int(linelist[2], 16)] = linelist[1]
                    except:
                        pass
    return definesDict

def GetLengthOfLongestValue(dicty):
    maxim = ""
    for key in dicty:
        if len(dicty[key]) > len(maxim):
            maxim = dicty[key]
            
    return len(maxim)

#Code Execution Begins Here
try:
	os.makedirs(OutputFolder)
except FileExistsError:
	pass

SpeciesDict = DefinesDictMaker(SpeciesDefines)

GeneralStructTableExtractor(0x128, SpeciesDict, OutputFolder + "Front_Pic_Table.c", "const struct CompressedSpriteSheet", "gMonFrontPicTable", "NUM_SPECIES", NumberOfPokemon, 8, [], [4, 2, 2], [False, False, SpeciesDict], False, True, 0)
GeneralStructTableExtractor(0x12C, SpeciesDict, OutputFolder + "Back_Pic_Table.c", "const struct CompressedSpriteSheet", "gMonBackPicTable", "NUM_SPECIES", NumberOfPokemon, 8, [], [4, 2, 2], [False, False, SpeciesDict], False, True, 0)
GeneralStructTableExtractor(0x130, SpeciesDict, OutputFolder + "Palette_Table.c", "const struct CompressedSpritePalette", "gMonPaletteTable", "NUM_SPECIES", NumberOfPokemon, 8, [], [4, 2, 2], [False, SpeciesDict, False], False, True, 0)
GeneralStructTableExtractor(0x134, SpeciesDict, OutputFolder + "Shiny_Palette_Table.c", "const struct CompressedSpritePalette", "gMonShinyPaletteTable", "NUM_SPECIES", NumberOfPokemon, 8, [], [4, 2, 2], [False, SpeciesDict, False], False, True, 1500)
GeneralStructTableExtractor(0x11F4C, SpeciesDict, OutputFolder + "Front_Pic_Coords_Table.c", "const struct MonCoords", "gMonFrontPicCoords", "NUM_SPECIES", NumberOfPokemon, 4, ["size", "y_offset"], [1, 1], [], True, False, 0)
GeneralStructTableExtractor(0x74634, SpeciesDict, OutputFolder + "Back_Pic_Coords_Table.c", "const struct MonCoords", "gMonBackPicCoords", "NUM_SPECIES", NumberOfPokemon, 4, ["size", "y_offset"], [1, 1], [], True, False, 0)
GeneralTableExtractor(0x356F8, SpeciesDict, False, OutputFolder + "Enemy_Elevation_Table.c", "const u8", "gEnemyMonElevation", "", "NUM_SPECIES", 0, NumberOfPokemon, 1, False)
GeneralTableExtractor(0x138, SpeciesDict, False, OutputFolder + "Icon_Table.c", "const u32", "gMonIconTable", "", "NUM_SPECIES", 0, NumberOfPokemon, 4, False)
GeneralTableExtractor(0x13C, SpeciesDict, False, OutputFolder + "Icon_Palette_Table.c", "const u8", "gMonIconPaletteIndices", "", "NUM_SPECIES", 0, NumberOfPokemon, 1, False)
GeneralTableExtractor(0x105E14, SpeciesDict, False, OutputFolder + "Footprint_Table.c", "const u32", "gMonFootprintTable", "", "NUM_SPECIES", 0, NumberOfPokemon, 4, False)