.thumb
.align 2

@0x81025E8 with r0
PokedexMemoryAllocationHook:
	ldr r0, [r5]
	strb r4, [r0]
	bl IsInBattle
	cmp r0, #0x0
	bne RegularPokedexMemoryAlloc
	ldr r0, .ExpandedPokedexSize
	b PokedexMemoryAllocReturn

RegularPokedexMemoryAlloc:
	ldr r0, .RegularPokedexSize

PokedexMemoryAllocReturn:
	ldr r1, =0x81025F0 | 1
bxr1:
	bx r1

.align 2
.RegularPokedexSize: .word 0xC10
.ExpandedPokedexSize: .word 999 * 8

@0x8104A66 with r1
DisplayRegionalDexNumHook:
	mov r5, r0
	ldr r1, =IsNationalPokedexEnabled
	bl bxr1
	cmp r0, #0x0
	beq UseRegionalDexOrdering
	ldr r0, =0x203ACF0
	ldr r0, [r0]
	add r0, #0xC
	ldr r0, [r0]
	cmp r0, #0x9	@;Check if looking at regional dex
	beq UseRegionalDexOrdering
	mov r0, r5
	ldr r1, =SpeciesToNationalPokedexNum
	bl bxr1
	b DisplayDexNumberReturn

UseRegionalDexOrdering:
	mov r0, r5
	bl SpeciesToRegionalDexNum
	
DisplayDexNumberReturn:
	mov r5, r0
	ldr r0, =0x8104A70 | 1
	bx r0

.pool
@0x8105CBC with r0
AlternateDexEntriesHook:
	lsl r2, r2, #0x18
	lsr r5, r2, #0x18
	lsl r3, r3, #0x18
	lsr r7, r3, #0x18
	mov r0, r1
	mov r4, r1
	bl TryLoadAlternateDexEntry
	cmp r0, #0x0
	bne AlternateDexEntriesReturn
	mov r0, r4
	ldr r1, =0x8105CC6 | 1
	bx r1

AlternateDexEntriesReturn:
	push {r0}
	mov r0, r4
	ldr r1, =SpeciesToNationalPokedexNum
	bl bxr1
	mov r4, r0
	mov r1, #0x1
	mov r2, #0x0
	bl DexFlagCheckCall
	lsl r0, #0x18
	cmp r0, #0x0
	pop {r0}
	beq DontDisplayDesc
	mov r1, r0
	ldr r0, =0x8105CEA | 1
	bx r0

DontDisplayDesc:
	ldr r0, =0x8105D5C | 1
	bx r0

DexFlagCheckCall:
	ldr r3, =0x8104AB0 | 1
	bx r3

