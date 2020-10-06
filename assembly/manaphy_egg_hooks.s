.thumb
.align 2

.pool
@0x8122214 with r0
PartyMenuManaphyEggHook:
	lsl r4, #0x10
	lsr r4, #0x10
	mov r0, r5 @Mon
	mov r1, r4 @Species
	bl TryReplaceSpeciesWithManaphyEgg
	mov r4, r0
	mov r0, r5
	mov r1, #0x0
	ldr r2, =0x812221C | 1
bxr2:
	bx r2

.pool
@0x8139978 with r1
SummaryScreenManaphyEggHook:
	lsl r0, r0, #0x10
	lsr r7, r0, #0x10
	ldr r0, [r5]
	add r0, r4 @Mon
	mov r1, r7 @Species
	bl TryReplaceSpeciesWithManaphyEgg
	mov r7, r0
	ldr r0, [r5]
	add r0, r4
	ldr r1, =0x8139980 | 1
bxr1:
	bx r1

.pool
@0x80471A8 with r0
EggHatchManaphyEggHook:
	ldr r0, =sEggHatchData
	ldr r0, [r0]
	ldrb r0, [r0, #0x4] @partyId
	bl IsPartyMonManaphy
	cmp r0, #0x0
	bne EggHatchLoadManaphyEggSprite
	ldr r0, =0x826011C @EggHatch_Sheet
	ldr r1, =LoadSpriteSheet
	bl bxr1
	ldr r0, =0x8260124 @EggShards_Sheet
	ldr r1, =0x080471B0 | 1
	bx r1

EggHatchLoadManaphyEggSprite:
	ldr r0, =sManaphyEgg_Sheet
	ldr r1, =LoadSpriteSheet
	bl bxr1
	ldr r0, =sManaphyEggShards_Sheet
	ldr r1, =LoadSpriteSheet
	bl bxr1
	ldr r0, =sManaphyEgg_SpritePalette
	ldr r1, =LoadSpritePalette
	bl bxr1
	ldr r0, =0x804724A | 1
bxr0:
	bx r0

.align 2
sManaphyEgg_Sheet:
.word ManaphyEggHatchTiles
.hword 2048, 12345

sManaphyEggShards_Sheet:
.word ManaphyEggShardsTiles
.hword 128, 23456

sManaphyEgg_SpritePalette:
.word ManaphyEggHatchPal
.hword 54321, 0

.pool
@0x809008E with r1
PokemonStorageSystemManaphyEggHook1:
	mov r1, r0 @Species
	mov r0, r4 @Mon
	bl TryReplaceSpeciesWithManaphyEgg
	mov r4, r0
	ldr r0, =0x8090058 | 1
	bl bxr0
	ldr r1, =0x8090098 | 1
	bx r1

.pool
@0x80900F4 with r0
PokemonStorageSystemManaphyEggHook2:
	mov r0, r9 @Box Id
	mov r1, r6 @Box Position
	bl GetBoxMonSpeciesAt_HandleManaphyEgg
	ldr r1, =0x80900FE | 1
	bx r1

.pool
@0x80901F8 with r0
PokemonStorageSystemManaphyEggHook3:
	mov r0, r7 @Box Position
	bl GetCurrentBoxMonSpeciesAt_HandleManaphyEgg
	ldr r1, =0x8090200 | 1
	bx r1

.pool
@0x80907B2 with r0
PokemonStorageSystemManaphyEggHook4:
	mov r0, r6 @Box Id
	mov r1, r4 @Box Position
	bl GetBoxMonSpeciesAt_HandleManaphyEgg
	ldr r1, =0x80907BC | 1
	bx r1

.pool
@0x80908A4 with r1
PokemonStorageSystemManaphyEggHook5:
	mov r1, r0 @Species
	mov r0, r4 @Mon
	bl TryReplaceSpeciesWithManaphyEgg
	mov r5, r0
	mov r0, r4
	mov r1, #0x0
	ldr r2, =0x80908AC | 1
	bx r2

.pool
@0x80908E0 with r2
PokemonStorageSystemManaphyEggHook6:
	ldr r2, =GetMonData
	bl bxr2
	mov r1, r0 @Species
	mov r0, r4 @Mon
	bl TryReplaceSpeciesWithManaphyEgg
	mov r5, r0
	ldr r0, =0x80908E8 | 1
	bx r0

.pool
@0x80956BC with r0
PokemonStorageSystemManaphyEggHook7:
	mov r0, r4 @Box Position
	bl GetCurrentBoxMonSpeciesAt_HandleManaphyEgg
	ldr r1, =0x80956C4 | 1
	bx r1

.pool
@0x80440C8 with r1
PokemonStorageSystemManaphyEggHook8: @Mon Pic Palette in Party
	mov r1, r0 @Species
	mov r0, r5 @Mon
	bl TryReplaceSpeciesWithManaphyEgg
	mov r4, r0
	mov r0, r5
	ldr r1, =0x080440D0 | 1
	bx r1

.pool
@0x8093C94 with r3
PokemonStorageSystemManaphyEggHook9: @Mon Pic Palette in Box
	str r2, [r0]
	sub r4, #0xA
	add r1, r4
	ldrh r0, [r1]
	push {r0-r2}
	mov r1, r0 @Species
	mov r0, r7 @Mon
	bl TryReplaceSpeciesWithManaphyEgg
	mov r3, r0
	pop {r0-r2}
	mov r0, r3
	ldr r1, =0x8093C9C | 1
	bx r1

.pool
@0x808F414 with r1
PokemonStorageSystemManaphyEggHook10: @Mon Pic Gfx
	push {r3}
	ldr r0, [r6]
	ldr r1, =.xCD8
	ldr r1, [r1]
	add r0, r1
	ldr r0, [r0]
	mov r1, r2
	bl ChangeSpeciesIfManaphyEggPalette
	mov r2, r0 @Species
	pop {r3}
	lsl r0, r2, #0x3
	ldr r1, =gMonFrontPicTable
	add r0, r1
	ldr r5, =.x22BC
	ldr r5, [r5]
	add r1, r4, r5
	ldr r4, =0x808F41C | 1
	bx r4

.align 2
.x22BC: .word 0x22BC
.xCD8: .word 0xCD8
