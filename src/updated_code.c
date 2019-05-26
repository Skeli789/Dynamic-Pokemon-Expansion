#include "defines.h"
#include "../include/evolution.h"
#include "../include/graphics.h"
#include "../include/main.h"
#include "../include/pokedex.h"

//Backsprite battle start

extern const u16 gSpeciesIdToCryId[];
extern const u16 gSpeciesToNationalPokedexNum[];
extern const struct AlternateDexEntries gAlternateDexEntries[];
extern const struct CompressedSpriteSheet gMonBackPicTable[];
extern const struct CompressedSpriteSheet gMonFrontPicTable[];
extern const struct CompressedSpritePalette gMonPaletteTable[];
extern const struct CompressedSpritePalette gMonShinyPaletteTable[];

const u16 gNumSpecies = NUM_SPECIES;
const u16 gNumDexEntries = NUM_DEX_ENTRIES;

u8 __attribute__((long_call)) GetGenderFromSpeciesAndPersonality(u16 species, u32 personality);
u8  __attribute__((long_call)) GetUnownLetterFromPersonality(u32 personality);
void __attribute__((long_call)) break_func(u32);

//This file's functions
u16 TryGetFemaleGenderedSpecies(u16 species, u32 personality);

u16 SpeciesToCryId(u16 species)
{
    return species + 1;
}

u16 NationalPokedexNumToSpecies(u16 nationalNum)
{
    u16 species;

    if (!nationalNum)
        return 0;

    species = 0;

    while (species < (NUM_SPECIES - 1) && gSpeciesToNationalPokedexNum[species] != nationalNum)
        species++;

    if (species == NUM_SPECIES - 1)
        return 0;

    return species + 1;
}

const u8* TryLoadAlternateDexEntry(u16 species)
{
	for (int i = 0; gAlternateDexEntries[i].species != SPECIES_TABLES_TERMIN; ++i)
	{
		if (gAlternateDexEntries[i].species == species)
			return gAlternateDexEntries[i].description;
	}
	
	return 0;
}

void LoadSpecialPokePic(const struct CompressedSpriteSheet* src, void* dest, u16 species, u32 personality, bool8 isFrontPic)
{
	u16 oldSpecies = species;
	const struct CompressedSpriteSheet* table = isFrontPic ? gMonFrontPicTable : gMonBackPicTable;

	species = TryGetFemaleGenderedSpecies(species, personality);
	if (species != oldSpecies) //Updated sprite
		src = &table[species];
	
    if (species == SPECIES_UNOWN)
    {
        u16 i = GetUnownLetterFromPersonality(personality);

        // The other Unowns are separate from Unown A.
        if (i == 0)
            i = SPECIES_UNOWN;
        else
            i += SPECIES_UNOWN_B - 1;

        if (!isFrontPic)
            LZ77UnCompWram((void*) gMonBackPicTable[i].data, dest);
        else
            LZ77UnCompWram((void*) gMonFrontPicTable[i].data, dest);
    }
    else if (species > NUM_SPECIES) // is species unknown? draw the ? icon
        LZ77UnCompWram((void*) gMonFrontPicTable[0].data, dest);
    else
        LZ77UnCompWram((void*) src->data, dest);

    DrawSpindaSpots(species, personality, dest, isFrontPic);
}

const u32* GetFrontSpritePalFromSpeciesAndPersonality(u16 species, u32 otId, u32 personality)
{
    u32 shinyValue;
	
	species = TryGetFemaleGenderedSpecies(species, personality);
	
    if (species > NUM_SPECIES)
        return (u32*) gMonPaletteTable[0].data;

    shinyValue = HIHALF(otId) ^ LOHALF(otId) ^ HIHALF(personality) ^ LOHALF(personality);
    if (shinyValue < 8)
        return (u32*) gMonShinyPaletteTable[species].data;
    else
        return (u32*) gMonPaletteTable[species].data;
}

const struct CompressedSpritePalette* GetMonSpritePalStructFromOtIdPersonality(u16 species, u32 otId , u32 personality)
{
    u32 shinyValue;
	species = TryGetFemaleGenderedSpecies(species, personality);

    shinyValue = HIHALF(otId) ^ LOHALF(otId) ^ HIHALF(personality) ^ LOHALF(personality);
    if (shinyValue < 8)
        return &gMonShinyPaletteTable[species];
    else
        return &gMonPaletteTable[species];
}

u16 TryGetFemaleGenderedSpecies(u16 species, u32 personality)
{
	if (GetGenderFromSpeciesAndPersonality(species, personality) == MON_FEMALE)
	{
		switch (species) {
			case SPECIES_HIPPOPOTAS:
				species = SPECIES_HIPPOPOTAS_F;
				break;
			case SPECIES_HIPPOWDON:
				species = SPECIES_HIPPOWDON_F;
				break;
			case SPECIES_UNFEZANT:
				species = SPECIES_UNFEZANT_F;
				break;
			case SPECIES_FRILLISH:
				species = SPECIES_FRILLISH_F;
				break;
			case SPECIES_JELLICENT:
				species = SPECIES_JELLICENT_F;
				break;
			case SPECIES_PYROAR:
				species = SPECIES_PYROAR_FEMALE;
				break;
		}
	}
	else if (species == SPECIES_XERNEAS && !gMain.inBattle)
		species = SPECIES_XERNEAS_NATURAL;
	
	return species;
}