""" Test if all imports work properly
Copyright 2019 Simulation Lab
University of Freiburg
Author: Lukas Elflein <elfleinl@cs.uni-freiburg.de>
"""

import sys
import smamp 

print('{} modules successfully loaded.'.format(len(sys.modules.keys())))
