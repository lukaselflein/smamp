""" Increase version number by .01
Copyright 2019 Simulation Lab
University of Freiburg
Author: Lukas Elflein <elfleinl@cs.uni-freiburg.de>
"""

outstring = ''
with open('setup.py', 'r') as infile:
	for line in infile:
		if 'version' in line:
			split = line.split("'")
			version = split[1]
			version = float(version)		
			version += 0.01
			version = '{:.2f}'.format(version)
			line = split[0] + "'" + version + "'" + split[2]
			print(line)
		outstring += line

with open('setup.py', 'w') as outfile:
	outfile.write(outstring)
