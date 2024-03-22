import os, subprocess, sys

lcfviz = os.path.join(os.path.dirname(__file__), 'lcfviz.exe')
if os.path.isfile(lcfviz):
	print('lcfviz: ', lcfviz)
else:
	sys.exit(1)
	
work_dir = os.getcwd()
if not os.path.isfile(os.path.join(work_dir, 'RPG_RT.ldb')):
	print('This script must be executed inside the game directory (containing \'RPG_RT.ldb\').')
	sys.exit(1)

dot_file = os.path.join(os.path.dirname(__file__), 'out', 'temp', 'map-tree.dot')
subprocess.run([lcfviz, '-o', dot_file], capture_output=True, check=True)
print(f'Saved map tree to: {dot_file}')
