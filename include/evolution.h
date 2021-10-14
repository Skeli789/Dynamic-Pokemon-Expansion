#pragma once

#define MON_MALE       0x00
#define MON_FEMALE     0xFE

struct Evolution
{
    u16 method;
    u16 param;
    u16 targetSpecies;
	u16 unknown; // used for mega evo, Dawn Stone, level in EVO_TYPE_IN_PARTY, or time range in EVO_LEVEL_SPECIFIC_TIME_RANGE
};

enum EvolutionMethods
{
	EVO_NONE = 0,
	EVO_FRIENDSHIP,
	EVO_FRIENDSHIP_DAY,
	EVO_FRIENDSHIP_NIGHT,
	EVO_LEVEL,
	EVO_TRADE,
	EVO_TRADE_ITEM,
	EVO_ITEM,		// for dawn stone, add MON_MALE(0x0) or MON_FEMALE(0xFF) to .unknown in evo table entry
	EVO_LEVEL_ATK_GT_DEF,
	EVO_LEVEL_ATK_EQ_DEF,
	EVO_LEVEL_ATK_LT_DEF,
	EVO_LEVEL_SILCOON,
	EVO_LEVEL_CASCOON,
	EVO_LEVEL_NINJASK,
	EVO_LEVEL_SHEDINJA,
	EVO_BEAUTY,
	// new evolutions
	EVO_RAINY_FOGGY_OW,		// raining or foggy in overworld
	EVO_MOVE_TYPE,	// knows a move with a specific type (eg. sylveon: fairy type move). Param is the move type
	EVO_TYPE_IN_PARTY,	//specific type (param) in party after given level (unknown).
	EVO_MAP, 	// specific map evolution. bank in param, map in unknown
	EVO_MALE_LEVEL,		// above given level if male
	EVO_FEMALE_LEVEL,	// above given level if female	
	EVO_LEVEL_NIGHT,	// above given level at night
	EVO_LEVEL_DAY,		// above given level during day
	EVO_HOLD_ITEM_NIGHT,	// level up holding item at night (eg. sneasel)
	EVO_HOLD_ITEM_DAY,	// level up while holding a specific item during the day (eg. happiny)
	EVO_MOVE,	// knows a given move
	EVO_OTHER_PARTY_MON,	//another poke in the party, arg is a specific species
	EVO_LEVEL_SPECIFIC_TIME_RANGE, // above given level with a range (unknown is [start][end]. eg lycanroc -> 1700-1800 hrs -> 0x1112)
	EVO_FLAG_SET, //If a certain flag is set. Can be used for touching the Mossy/Icy Rock for Leafeon/Glaceon evolutions
	EVO_CRITICAL_HIT, // successfully land 3 critical hits in one battle
	EVO_NATURE_HIGH, // evolution based on high key nature at a certain level
	EVO_NATURE_LOW, // evolution based on low key nature at a certain level
	EVO_DAMAGE_LOCATION, // recieve 49+ damage in battle without fainting, walk to specific tile
	EVO_ITEM_LOCATION, // Stand on a tile with a certain behaviour and use an item on a Pokemon
};

#define EVO_GIGANTAMAX 0xFD
#define EVO_MEGA 0xFE

enum MegaEvoVariants
{
	MEGA_VARIANT_STANDARD,
	MEGA_VARIANT_PRIMAL,
	MEGA_VARIANT_WISH, //Rayquaza
	MEGA_VARIANT_ULTRA_BURST, //Necrozma
};

#define MB_SHALLOW_WATER 0x17 //For Alolan Raichu

#define MAPSEC_POWER_PLANT 0x8E
#define MAPSEC_ICEFALL_CAVE 0xB1
