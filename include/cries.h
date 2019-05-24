#pragma once

struct ToneData
{
    u8 type;
    u8 key;
    u8 length; // sound length (compatible sound)
    u8 pan_sweep; // pan or sweep (compatible sound ch. 1)
    u8* wav; //struct WaveData *wav;
    u8 attack;
    u8 decay;
    u8 sustain;
    u8 release;
};