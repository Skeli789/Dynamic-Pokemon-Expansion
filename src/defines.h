#pragma once

#include "../include/types.h"
#include "../include/species.h"

#define EVOS_PER_MON 16

#define FALSE 0
#define TRUE 1

#define ARRAY_COUNT(array) (sizeof(array) / sizeof((array)[0]))

#define SPECIES_TABLES_TERMIN 0xFEFE

//CHANGE THESE IF YOU WANT
#define EXPAND_LEARNSETS //If you're using this feature, make sure you insert the Complete Fire Red Upgrade 
//                         afterwards or the game will crash when selecting certain Pokemon. Comment out this
//                         line if you're using the CFRU to expand movesets.

//#define INCLUDE_FOOTPRINTS //If you uncomment this line, make sure to uncomment gMonFootprintTable in "repoints", and remove the footprint remover in "bytereplacement"

#define NUM_TMSHMS 128
#define NUM_MOVE_TUTOR_MOVES 128