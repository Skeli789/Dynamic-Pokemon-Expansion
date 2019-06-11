#!/usr/bin/env python3

from glob import glob
from pathlib import Path
import os
import itertools
import hashlib
import subprocess
import sys
from datetime import datetime
from string import StringFileConverter

PathVar = os.environ.get('Path')
Paths = PathVar.split(';')
PATH = ""
for candidatePath in Paths:
    if "devkitARM" in candidatePath:
        PATH = candidatePath
        break
if PATH == "":
	print('DevKit does not exist in your Path variable.\nChecking default location.')
	PATH = 'C://devkitPro//devkitARM//bin'
	if os.path.isdir(PATH) == False:
		print("...\nDevkit not found.")
		sys.exit(1)
	else:
		print("Devkit found.")

PREFIX = '/arm-none-eabi-'
AS = (PATH + PREFIX + 'as')
CC = (PATH + PREFIX + 'gcc')
LD = (PATH + PREFIX + 'ld')
GR = ("deps/grit.exe")
WAV2AGB = ("deps/wav2agb.exe")
ARP = ('armips')
OBJCOPY = (PATH + PREFIX + 'objcopy')
SRC = './src'
GRAPHICS = './graphics'
ASSEMBLY = './assembly'
STRINGS = './strings'
AUDIO = './audio'
BUILD = './build'
IMAGES = '\Images'
ASFLAGS = ['-mthumb', '-I', ASSEMBLY]
LDFLAGS = ['BPRE.ld', '-T', 'linker.ld']
CFLAGS = ['-mthumb', '-mno-thumb-interwork', '-mcpu=arm7tdmi', '-mtune=arm7tdmi',
'-mno-long-calls', '-march=armv4t', '-Wall', '-Wextra','-Os', '-fira-loop-pressure', '-fipa-pta']

PrintedCompilingAudio = False #Used to tell the script whether or not the strings "Compiling Cries" has been printed

def run_command(cmd):
	try:
		subprocess.check_output(cmd)
	except subprocess.CalledProcessError as e:
		print(e.output.decode(), file = sys.stderr)
		sys.exit(1)

def make_output_file(filename):
	'''Return hash of filename to use as object filename'''
	m = hashlib.md5()
	m.update(filename.encode())
	newfilename = os.path.join(BUILD, m.hexdigest() + '.o')
	
	if not os.path.isfile(filename):
		return [newfilename, False]
	
	fileExists = os.path.isfile(newfilename)
	
	if fileExists and os.path.getmtime(newfilename) > os.path.getmtime(filename): #If the object file was created after the file was last modified
		return [newfilename, False]
	
	return [newfilename, True]

def make_output_img_file(filename):
	'''Return "IMG" + hash of filename to use as object filename'''
	if "frontspr" in filename:
		newfilename = os.path.join(BUILD, 'IMG_Front' + filename.split("Sprite")[1].split(".s")[0] + '.o')
	elif "backspr" in filename:
		newfilename = os.path.join(BUILD, 'IMG_Back' + filename.split("Sprite")[1].split(".s")[0] + '.o')
	else:
		m = hashlib.md5()
		m.update(filename.encode())
		newfilename = os.path.join(BUILD, 'IMG_' + m.hexdigest() + '.o')
	
	if not os.path.isfile(filename):
		return [newfilename, False]
	
	fileExists = os.path.isfile(newfilename)
	
	if fileExists and os.path.getmtime(newfilename) > os.path.getmtime(filename): #If the object file was created after the file was last modified
		return [newfilename, False]
	
	return [newfilename, True]

def make_output_audio_file(filename):
	'''Return "AUDIO" + hash of filename to use as object filename'''
	newfilename = os.path.join(BUILD, 'SND_' + filename.split("gCry")[1].split(".s")[0] + '.o')
	
	if not os.path.isfile(filename):
		return [newfilename, False]
	
	fileExists = os.path.isfile(newfilename)
	
	if fileExists and os.path.getmtime(newfilename) > os.path.getmtime(filename): #If the object file was created after the file was last modified
		return [newfilename, False]
	
	return [newfilename, True]

def process_assembly(in_file):
	'''Assemble'''
	out_file_list = make_output_file(in_file)
	out_file = out_file_list[0]
	if out_file_list[1] is False:
		return out_file #No point in recompiling file
	
	try:
		print ('Assembling %s' % in_file)
		cmd = [AS] + ASFLAGS + ['-c', in_file, '-o', out_file]
		run_command(cmd)
		
	except FileNotFoundError:
		print('Error! The assembler could not be located.\nAre you sure you set up your path to devkitPro/devkitARM/bin correctly?')
		sys.exit()
		
	return out_file
	
def process_c(in_file):
	'''Compile C'''
	out_file_list = make_output_file(in_file)
	out_file = out_file_list[0]
	if out_file_list[1] is False:
		return out_file #No point in recompiling file
	
	try:
		print ('Compiling %s' % in_file)
		cmd = [CC] + CFLAGS + ['-c', in_file, '-o', out_file]
		run_command(cmd)

	except FileNotFoundError:
		print('Error! The C compiler could not be located.\nAre you sure you set up your path to devkitPro/devkitARM/bin correctly?')
		sys.exit()
	
	return out_file

def process_string(filename):
    '''Build Strings'''
    out_file = filename.split(".string")[0] + '.s'
    object_file = make_output_file(out_file)[0]

    fileExists = os.path.isfile(object_file)

    if fileExists and os.path.getmtime(object_file) > os.path.getmtime(filename): #If the .o file was created after the image was last modified
        return make_output_file(out_file)[0]

    print ('Building Strings %s' % filename)
    StringFileConverter(filename)

    out_file_list = make_output_file(out_file)
    new_out_file = out_file_list[0]
    if out_file_list[1] == False:
        os.remove(out_file)
        return new_out_file	#No point in recompiling file

    cmd = [AS] + ASFLAGS + ['-c', out_file, '-o', new_out_file]
    run_command(cmd)
    os.remove(out_file)
    return new_out_file

def ProcessSpriteGraphics():
	with open(GRAPHICS + "/backspriteflags.grit", "r") as file:
		for line in file:
			backflags = line.split()
			break
			
	with open(GRAPHICS + "/frontspriteflags.grit", "r") as file:
		for line in file:
			frontflags = line.split()
			break

	with open(GRAPHICS + "/iconspriteflags.grit", "r") as file:
		for line in file:
			iconflags = line.split()
			break

	try:
		os.makedirs(SRC + "/generated")
	except FileExistsError:
		pass
	
	backsprites = [file for file in glob(GRAPHICS + "/backspr" + "**/*.png", recursive=True)]
	frontsprites = [file for file in glob(GRAPHICS + "/frontspr" + "**/*.png", recursive=True)]
	iconsprites = [file for file in glob(GRAPHICS + "/pokeicon" + "**/*.png", recursive=True)]

	print("Processing Front Sprites")
	combinedFile = open(os.path.join('SRC', 'generated', 'frontsprites.s'), 'w')
	for sprite in frontsprites:
		assembled = sprite.split('.png')[0] + '.s'

		if (not os.path.isfile(assembled)
		or os.path.getmtime(sprite) > os.path.getmtime(assembled)):
			run_command([GR, sprite] + frontflags + ['-o', assembled])

		with open(assembled, 'r') as tempFile:
			combinedFile.write(tempFile.read())
	combinedFile.close()

	print("Processing Back Sprites")
	combinedFile = open(os.path.join('SRC', 'generated', 'backsprites.s'), 'w')
	for sprite in backsprites:
		assembled = sprite.split('.png')[0] + '.s'

		if (not os.path.isfile(assembled)
		or os.path.getmtime(sprite) > os.path.getmtime(assembled)):
			run_command([GR, sprite] + backflags + ['-o', assembled])

		with open(assembled, 'r') as tempFile:
			combinedFile.write(tempFile.read())
	combinedFile.close()
	
	print("Processing Icon Sprites")
	combinedFile = open(os.path.join('SRC', 'generated', 'iconsprites.s'), 'w')
	for sprite in iconsprites:
		assembled = sprite.split('.png')[0] + '.s'

		if (not os.path.isfile(assembled)
		or os.path.getmtime(sprite) > os.path.getmtime(assembled)):
			run_command([GR, sprite] + iconflags + ['-o', assembled])

		with open(assembled, 'r') as tempFile:
			combinedFile.write(tempFile.read())
	combinedFile.close()

def process_audio(in_file):
	'''Compile Audio'''
	out_file = in_file.split('.wav')[0] + '.s'

	cmd = [WAV2AGB, in_file] + [out_file, '-c']
	
	out_file_list = make_output_audio_file(out_file)
	new_out_file = out_file_list[0]
	try:
		if os.path.getmtime(new_out_file) > os.path.getmtime(in_file): #If the .o file was created after the image was last modified
			return new_out_file
		else:
			run_command(cmd)
	
	except FileNotFoundError:
		run_command(cmd) #No .o file has been created

	global PrintedCompilingAudio
	if (PrintedCompilingAudio is False):
		print ('Compiling Cries')
		PrintedCompilingAudio = True
	
	out_file_list = make_output_audio_file(out_file)
	new_out_file = out_file_list[0]
	if out_file_list[1] == False:
		os.remove(out_file)
		return new_out_file	#No point in recompiling file

	cmd = [AS] + ASFLAGS + ['-c', out_file, '-o', new_out_file]
	run_command(cmd)
	os.remove(out_file)
	return new_out_file

def link(objects):
	'''Link objects into one binary'''
	linked = 'build/linked.o'
	cmd = [LD] + LDFLAGS + ['-o', linked] + list(objects)
	run_command(cmd)
	return linked
	
def objcopy(binary):
	cmd = [OBJCOPY, '-O', 'binary', binary, 'build/output.bin']
	run_command(cmd)
	
def run_glob(globstr, fn):
	'''Glob recursively and run the processor function on each file in result'''
	if globstr == '**/*.png' or globstr == '**/*.bmp': #Search the graphics location
		return run_glob_graphics(globstr, fn)
	elif globstr == '**/*.wav':
		return run_glob_audio(globstr, fn)
	
	if sys.version_info > (3, 4):
		files = glob(os.path.join(SRC, globstr), recursive = True)
		return map(fn, files)
	else:
		files = Path(SRC).glob(globstr)
		return map(fn, map(str, files))

def run_glob_graphics(globstr, fn):
	'''Glob recursively and run the processor function on each file in result'''
	if sys.version_info > (3, 4):
		files = glob(os.path.join(GRAPHICS, globstr), recursive = True)
		return map(fn, files)
	else:
		files = Path(GRAPHICS).glob(globstr)
		return map(fn, map(str, files))

def run_glob_audio(globstr, fn):
	'''Glob recursively and run the processor function on each file in result'''
	if sys.version_info > (3, 4):
		files = glob(os.path.join(AUDIO, globstr), recursive = True)
		return map(fn, files)
	else:
		files = Path(AUDIO).glob(globstr)
		return map(fn, map(str, files))

def main():
	starttime = datetime.now()
	globs = {
			'**/*.s': process_assembly,
			'**/*.c': process_c,
			'**/*.string': process_string,
			#'**/*.png': process_image,
			#'**/*.bmp': process_image,
			'**/*.wav': process_audio,
	}
		
	# Create output directory
	try:
		os.makedirs(BUILD)
	except FileExistsError:
		pass
	
	ProcessSpriteGraphics()

	# Gather source files and process them
	objects = itertools.starmap(run_glob, globs.items())
	
	# Link and extract raw binary
	linked = link(itertools.chain.from_iterable(objects))
	objcopy(linked)
	
	#Build special_inserts.asm
	if not os.path.isfile('build/special_inserts.bin') or os.path.getmtime('build/special_inserts.bin') < os.path.getmtime('special_inserts.asm'): #If the binary file was created after the file was last modified):
		cmd = cmd = [AS] + ASFLAGS + ['-c', 'special_inserts.asm', '-o', 'build/special_inserts.o']
		run_command(cmd)
		
		cmd = [OBJCOPY, '-O', 'binary', 'build/special_inserts.o', 'build/special_inserts.bin']
		run_command(cmd)
		
		print ('Assembling special_inserts.asm')
	
	print('Built in ' + str(datetime.now() - starttime) + '.')
	
if __name__ == '__main__':
	main()
