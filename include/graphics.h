#pragma once

// Extracts the upper 16 bits of a 32-bit number
#define HIHALF(n) (((n) & 0xFFFF0000) >> 16)

// Extracts the lower 16 bits of a 32-bit number
#define LOHALF(n) ((n) & 0xFFFF)

struct MonCoords
{
    // This would use a bitfield, but some function
    // uses it as a u8 and casting won't match.
    u8 size; // u8 width:4, height:4;
    u8 y_offset;
	u16 unused;
};

struct CompressedSpriteSheet
{
    const u8* data;  // LZ77 compressed pixel data
    u16 size;        // Uncompressed size of pixel data
    u16 tag;
};

struct CompressedSpritePalette
{
    const u8* data;  // LZ77 compressed palette data
    u16 tag;
	u16 unused;
};

void __attribute__((long_call)) LZ77UnCompWram(const void *src, void *dest);
void __attribute__((long_call)) DrawSpindaSpots(u16, u32, u8*, u8);
