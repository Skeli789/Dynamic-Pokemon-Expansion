.thumb
.align 2

.pool
@0x800ECF2 with r4
LoadSpecialPokePicHook:
	mov r7, r8
	push {r7}
	ldr r4, [sp, #0x18]
	sub sp, #0x4
	str r4, [sp, #0x0]
	bl LoadSpecialPokePic
	add sp, #0x4
	pop {r7}
	mov r8, r7
	pop {r4-r7}
	pop {r0}
	bx r0

.pool
@0x8080344E4 with r0
BattleLoadPlayerMonSpriteGfxHook:
	mov r0, r5
	mov r1, r4
	bl TryGetFemaleGenderedSpecies
	mov r5, r0
@Prep return
	mov r0, r6
	mov r1, #0x1 @;Trainer Id
	ldr r2, =GetMonData
	bl bxr2
	ldr r1, =0x080344EC | 1
	bx r1

.pool
@0x803436C with r0
BattleLoadOpponentMonSpriteGfxHook:
	mov r0, r5
	mov r1, r6
	bl TryGetFemaleGenderedSpecies
	mov r5, r0
@Prep return
	mov r0, r4
	mov r1, #0x1 @;Trainer Id
	ldr r2, =GetMonData
	bl bxr2
	ldr r1, =0x08034374 | 1
bxr1:
	bx r1

/*
.pool
@0x80747B4 with r0
GetBattlerSpriteFinalYHook:
	lsl r2, r2, #0x18
	lsr r7, r2, #0x18
	mov r0, r6
	lsr r1, r1, #0x10
	bl TryGetFemaleGenderedSpeciesFromBank

	mov r0, r6
	ldr r1, =0x80747BC | 1
	bx r1
*/

.pool
@0x8096E38 with r2
GenderedMonIconHook:
	lsr r7, r3, #0x10
	lsl r0, #0x18
	lsr r0, #0x18
	mov r9, r0

	mov r0, r4
	ldr r1, [sp, #0x50] @Personality
	bl TryGetFemaleGenderedSpecies
	mov r4, r0

	ldr r1, [sp, #0x50] @Personality
	ldr r0, =0x8096E40 | 1
	bx r0

.pool
@0x8139DDC with r1
SummaryScreenIconPalHook:
	mov r4, r0
	mov r1, r0
	mov r0, r5
	bl TryGetFemaleGenderedSpecies
	mov r5, r0
	ldr r1, =SafeLoadMonIconPalette
	bl bxr1
	ldr r0, =0x8139DE4 | 1
	bx r0

.pool
@0x808398C with r1
CreateMonSprite_PicBoxHook:
	mov r4, r0
	mov r1, #0x0
	mov r2, #0x80
	lsl r2, #0x8 @0x8000
	bl GetMonSpritePalStructFromOtIdPersonality
	mov r1, r0
	mov r0, r4
	mov r4, r1 @Backup palette struct
	ldrh r1, [r4, #0x4] @Tag
	mov r3, #0x80
	lsl r3, #0x8 @0x8000
	ldr r2, =0x8083994 | 1
bxr2:
	bx r2

.pool
@0x80CDF10 with r1
EvolutionSceneHook1:
	mov r9, r0
	mov r0, r5 @currSpecies
	mov r1, r9 @personality
	bl TryGetFemaleGenderedSpecies
	lsl r0, #0x3
	ldr r1, =gMonFrontPicTable
	add r0, r1
	ldr r2, =0x80CDF18 | 1
	bx r2

.pool
@0x80CDF88 with r2
EvolutionSceneHook2:
	strb r0, [r1]
	mov r0, r10 @speciesToEvolve
	mov r1, r9 @personality
	bl TryGetFemaleGenderedSpecies
	lsl r0, #0x3
	ldr r2, =gMonFrontPicTable
	add r0, r2
	ldr r2, =0x80CDF92 | 1
	bx r2

.pool
@0x80CE1C0 with r2
EvolutionSceneHook3:
	strb r0, [r1]
	mov r0, r5 @postEvoSpecies
	mov r1, r6 @personality
	bl TryGetFemaleGenderedSpecies
	lsl r0, #0x3
	ldr r1, =gMonFrontPicTable
	add r0, r1
	ldr r2, =0x80CE1C8 | 1
	bx r2
