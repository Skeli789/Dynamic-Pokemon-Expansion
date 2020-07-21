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
	EVO_CRITICAL_HIT, // successfully land 3 critical hits in one battle
	EVO_NATURE_HIGH, // evolution based on high key nature at a certain level
	EVO_NATURE_LOW, // evolution based on low key nature at a certain level
	EVO_DAMAGE_LOCATION // recieve 49+ damage in battle without fainting, walk to specific tile
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

#define MAP_NAME_ROUTE_1 0x65
#define MAP_NAME_ROUTE_2 0x66
#define MAP_NAME_FLOWER_PARADISE 0x88
#define MAP_NAME_GRIM_WOODS 0x7E
#define MAP_NAME_ROUTE_4 0x63
#define MAP_NAME_CINDER_VOLCANO 0x7F
#define MAP_NAME_ROUTE_5 0x69
#define MAP_NAME_VALLEY_CAVE 0x83
#define MAP_NAME_ROUTE_6 0x6A
#define MAP_NAME_ROUTE_7 0x6B
#define MAP_NAME_ROUTE_8 0x6C
#define MAP_NAME_FROST_MOUNTAIN 0x82
#define MAP_NAME_BLIZZARD_CITY 0x5C
#define MAP_NAME_ROUTE_9 0x6D
#define MAP_NAME_ROUTE_10 0x64
#define MAP_NAME_ROUTE_11 0x6F
#define MAP_NAME_THUNDERCAP_MT 0x8A
#define MAP_NAME_ROUTE_12 0x70
#define MAP_NAME_VIVILL_WOODS 0x8C
#define MAP_NAME_ROUTE_16 0x74
#define MAP_NAME_ROUTE_17 0x75
