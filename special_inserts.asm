.text
.align 2
.thumb

.equ NUM_SPECIES, 1102
.equ EVOS_PER_MON, 16
.equ NUM_DEX_ENTRIES, 809

.equ SEEN_DEX_FLAGS, 0x203C700
.equ CAUGHT_DEX_FLAGS, (SEEN_DEX_FLAGS + (NUM_DEX_ENTRIES / 8) + 1)

@@Fix Num Evolutions@@
.org 0x4598A, 0xFF
mov r5, #EVOS_PER_MON * 8
mov r3, r12
add r3, #EVOS_PER_MON * 8

@@Fix Egg Hatching Time@@
.org 0x46204, 0xFF
.word gBaseStats + 0x11

.org 0x462A8, 0xFF
.word gBaseStats + 0x11

@@Fix New Game Dex Flags Clear@@
.org 0x549B0, 0xFF
	mov r0, r4
	mov r8, r8
	mov r1, #0x0
	mov r2, #(NUM_DEX_ENTRIES / 8) + 1

.org 0x549BC, 0xFF
	mov r0, r4
	add r0, #(NUM_DEX_ENTRIES / 8) + 1
	mov r1, #0x0
	mov r2, #(NUM_DEX_ENTRIES / 8) + 1
	
.org 0x549D0, 0xFF
.word SEEN_DEX_FLAGS

@@Fix Dex Views@@
.org 0x88EA4, 0xFF @Pokedex Count
.word NUM_DEX_ENTRIES - 1

.org 0x1037D4, 0xFF @Weight View
.word NUM_DEX_ENTRIES - 1

.org 0x103870, 0xFF @Height View
.word NUM_DEX_ENTRIES - 1

.org 0x103920, 0xFF @General
.word NUM_DEX_ENTRIES - 1

.org 0x104B10, 0xFF
.word SEEN_DEX_FLAGS

.org 0x104B5C, 0xFF
.word CAUGHT_DEX_FLAGS

.org 0x104B94, 0xFF
.word SEEN_DEX_FLAGS

.org 0x104BB8, 0xFF
.word CAUGHT_DEX_FLAGS

.org 0x104C28, 0xFF
.word NUM_DEX_ENTRIES - 1
