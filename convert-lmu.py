import os, subprocess, sys
from pathlib import Path


lcf2xml = os.path.join(os.path.dirname(__file__), 'lcf2xml.exe')
if os.path.isfile(lcf2xml):
	print('lcf2xml: ', lcf2xml)
else:
	sys.exit(1)

lmu2png = os.path.join(os.path.dirname(__file__), 'lmu2png.exe')
if os.path.isfile(lmu2png):
	print('lmu2png: ', lmu2png)
else:
	sys.exit(1)

work_dir = os.getcwd()
ldb_file = os.path.join(work_dir, 'RPG_RT.ldb')
if not os.path.isfile(ldb_file):
	print('This script must be executed inside the game directory (containing \'RPG_RT.ldb\').')
	sys.exit(1)


lmu_files = []

for file in os.listdir(work_dir):
    if file.endswith(".lmu"):
        lmu_files.append(os.path.join(work_dir, file))

print('Number of maps found: ', len(lmu_files))

image_dir = os.path.join(os.path.dirname(__file__), 'docs', 'images')
os.makedirs(image_dir, exist_ok=True)

temp_dir =  os.path.join(os.path.dirname(__file__), 'temp')
os.makedirs(temp_dir, exist_ok=True)

subprocess.run([lcf2xml, ldb_file], capture_output=True, check=True)
edb_path = Path(ldb_file.replace('.ldb', '.edb'))
edb_path.rename(os.path.join(temp_dir, 'RPG_RT.xml'))

for count, lmu in enumerate(lmu_files):
	png_filename = os.path.basename(lmu).replace('.lmu', '.png')
	subprocess.run([lmu2png, lmu, '-o', os.path.join(image_dir, png_filename)], capture_output=True, check=True)
	
	subprocess.run([lcf2xml, lmu], capture_output=True, check=True)
	emu_path = Path(lmu.replace('.lmu', '.emu'))
	xml_filename = os.path.join(temp_dir, os.path.basename(lmu).replace('.lmu', '.xml'))
	emu_path.rename(xml_filename)

	print(f'Completed {count + 1} of {len(lmu_files)}')
