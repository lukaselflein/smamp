""" Increase version number by .01
Copyright 2019 Simulation Lab
University of Freiburg
Author: Lukas Elflein <elfleinl@cs.uni-freiburg.de>
"""

outstring = ''
with open('setup.py', 'r') as infile:
	for line in infile:
		if 'version' in line:
			version = float(line[-7:-3])
			version += 0.01
			line = line[:-7] + str(version) + line[-3:]
		outstring += line

with open('setup.py', 'w') as outfile:
	outfile.write(outstring)
