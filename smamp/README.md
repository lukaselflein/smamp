# Code snippets for charge optimization

* `__init__.py`: Import the snippets into the module namespace. Any snippets you remove from there will be invisible to imports.
* `aa2ua_cube.py`: Map point charges obtained by GPAW and HORTON on the original GROMACS topology.
* `charges_to_rtp.py`: Transfer Charges from CSV table to .rft file
* `convert_UA_to_AA.py`: Change structure with implicit Hydrogen to one with explicitely defined H-atoms
* `extract_bader_charges.py`: Extract atomic charges from Bader Charge Analysis output.
* `insertHbyList.py`: Add explicit hydrogens around carbon with implicit hydrogens.
* `tools.py`: Misc tools, file system operations
