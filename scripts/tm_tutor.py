import os
import sys
from glob import glob

# Data
TM_HM_COUNT = 128
TUTOR_COUNT = 128
SPECIES_COUNT = 0x4F3 + 1

TM_OUTPUT = "assembly/generated/tm_compatibility.s"
TUTOR_OUTPUT = "assembly/generated/tutor_compatibility.s"
TM_COMPATIBILITY = "src/tm_compatibility"
TUTOR_COMPATIBILITY = "src/tutor_compatibility"
SPECIES_DEFINES = "include/species.h"


# Uses pre-made files corresponding to each TM to build species TM Data
def TMDataBuilder():
    DataBuilder(TM_COMPATIBILITY, TM_HM_COUNT, TM_OUTPUT, "TMHM")


def TutorDataBuilder():
    DataBuilder(TUTOR_COMPATIBILITY, TUTOR_COUNT, TUTOR_OUTPUT, "Tutor")


def DataBuilder(directory: str, numEntries: int, outputFile: str, dataType: str):
    fileList = [file for file in glob(directory + "**/*.txt", recursive=True)]
    if os.path.isfile(outputFile) and max(list(map(os.path.getmtime, fileList))) < os.path.getmtime(outputFile):
        return

    print("Processing {} Data.".format(dataType))
    output = open(outputFile, 'w')
    compatibilityTable = PokemonDataListInitializer(numEntries)

    for filePath in fileList:
        try:
            if sys.platform.startswith('win'):
                delimiter = '\\'
            else:  # OSX, Linux
                delimiter = '/'
            tmId = filePath.split()[0].split(delimiter)
            tmId = int(tmId[len(tmId) - 1])
            tmId -= 1

            if tmId >= numEntries:
                print('Ignoring file: "{}"\nTM number not valid.'.format(filePath))
                continue  # Don't process this file if not valid
        except ValueError:
            print('Ignoring file: "{}"\nNot valid TM file.'.format(filePath))
            continue  # Don't process this file if not proper TM file

        with open(filePath, 'r') as file:
            for i, line in enumerate(file):
                if ':' not in line:  # Aka not the first line
                    try:
                        lineContents = int(line)  # Species entered as integer
                        compatibilityTable[lineContents][tmId] = 1
                    except ValueError:
                        try:
                            lineContents = int(ReverseSpeciesDict[line.strip()])  # Species entered as species name
                            compatibilityTable[lineContents][tmId] = 1
                        except ValueError:
                            lineContents = int(line, 16)  # Species entered as hex
                            compatibilityTable[lineContents][tmId] = 1
                        except KeyError:  # Species name was not found
                            try:

                                lineContents = int(ReverseSpeciesDict["SPECIES_" + line.strip()])
                                compatibilityTable[lineContents][tmId] = 1
                            except KeyError:
                                print('Error with key: {} on line {} in: {}'.format(line.strip(), i + 1, filePath))

    output.write(".thumb\n.align 2\n\n@THIS IS A GENERATED FILE! DO NOT MODIFY IT!\n\n"
                 ".global g{}Learnsets\ng{}Learnsets:\n".format(dataType, dataType))
    for i, mon in enumerate(compatibilityTable):
        output.write(".byte ")
        data = FixEndian(''.join(str(a) for a in mon))

        byte = ""
        for j, bit in enumerate(data):
            byte += bit
            if j % 8 == 7:
                byte = int(byte, 2)
                if j + 1 >= len(data):
                    output.write(hex(byte))  # End of line
                else:
                    output.write(hex(byte) + ",")
                byte = ""

        output.write("\n")

    output.close()


# Utility Functions
def FixEndian(string: str) -> str:  # Converts bitlist from big endian to little endian
    index, newString = 0, ''
    for a in range(len(string) + 1):
        if index % 8 == 0 and index != 0:
            newString += ReverseString(string[index - 8:index])
        index += 1
    return newString


def ReverseString(string: str) -> str:
    return ''.join(string[len(string)-a-1] for a in range(len(string)))


def PokemonDataListInitializer(numEntries: int) -> [[]]:
    outerList = []
    for a in range(int(SPECIES_COUNT)):
        innerList = [0] * numEntries
        outerList.append(innerList)
    return outerList


def DefinesDictMaker(definesFile: str) -> {}:
    definesDict = {}
    with open(definesFile, 'r') as file:
        for line in file:
            if '#define ' in line:
                lineList = line.split()
                try:
                    definesDict[int(lineList[2])] = lineList[1]
                except:
                    try:
                        definesDict[int(lineList[2], 16)] = lineList[1]
                    except:
                        pass
    return definesDict


def ReverseDict(dictionary: {}):
    reverseDict = {}
    for key in dictionary:
        reverseDict[dictionary[key]] = key

    return reverseDict


def ChangeFileLine(filePath: str, lineToChange: int, replacement: str):
    with open(filePath, 'r') as file:
        copy = file.read()
        file.seek(0x0)
        lineNum = 1
        for line in file:
            if lineNum == lineToChange:
                copy = copy.replace(line, replacement)
                break
            lineNum += 1

    with open(filePath, 'w') as file:
        file.write(copy)


SpeciesDict = DefinesDictMaker(SPECIES_DEFINES)
ReverseSpeciesDict = ReverseDict(SpeciesDict)

if __name__ == '__main__':
    TMDataBuilder()
    TutorDataBuilder()
