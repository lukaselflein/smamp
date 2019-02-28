""" Misc tools
Copyright 2019 Simulation Lab
University of Freiburg
Author: Lukas Elflein <elfleinl@cs.uni-freiburg.de>
"""

import os 

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def check_existence(path, neccessary_files, verbose=True):
	"""
	Check if all neccessary files exist in path, print warning for missing files.

	Arguments:
	path: string, the path to search
	neccessary_files: list of strings, check if they exist in path
	verbose: Bool, controls amount of printing

	Returns:
	String warning xor None 
	"""
	with cd(path):
		# Files should be here
		# if verbose:
		#	print([f for s, d, f in os.walk('.')])

		for f in neccessary_files:
			if not (os.path.islink(f) or os.path.isfile(f)):
				warning = 'File not found: {}'.format(f)
				if verbose:
					print(Warning(warning))
				return warning
	return None

