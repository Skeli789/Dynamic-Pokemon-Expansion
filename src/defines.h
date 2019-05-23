#pragma once

#include "../include/types.h"
#include "../include/species.h"

//#define INCLUDE_FOOTPRINTS //If you uncomment this line, make sure to uncomment gMonFootprintTable in repoints, and remove the footprint remover in bytereplacement

#define EVOS_PER_MON 16

#define FALSE 0
#define TRUE 1

#define ARRAY_COUNT(array) (sizeof(array) / sizeof((array)[0]))

#define SPECIES_TABLES_TERMIN 0xFEFE