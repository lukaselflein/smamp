#!/usr/bin/env python   
""" Map point charges obtained by GPAW and HORTON on the original GROMACS topology.
Copyright 2019 Simulation Lab
University of Freiburg
Author: Johannes Hoermann <johannes.hoermann@imtek.uni-freiburg.de>
Modified: Lukas Elflein <elfleinl@cs.uni-freiburg.de>
"""

import ast
import h5py
import ase.io
from ase.io.cube import read_cube_data
import parmed as pmd
from parmed import gromacs
from smamp.insertHbyList import insertHbyList

import warnings
import argparse

def main():
    parser = argparse.ArgumentParser(\
        description='Converts an all-atom cube file into united-atom'
            ' representation based on certain replacement rules')
    #parser.add_argument('-c', '--charge',metavar='INTEGER_CHARGE',
    #        type=int,nargs='?', const=1, default=0)
    #parser.add_argument('infile', nargs='?')
    parser.add_argument('infile_pdb', nargs='?', metavar='infile.pdb',
            default='system.pdb',
            help="Original .pdb file, before insertion of implicit hydrogen.")
    parser.add_argument('infile_top', nargs='?', metavar='infile.top',
            default='system.top', help="Original GROMACS .top file")
    parser.add_argument('infile_cube', nargs='?', metavar='infile.cube',
            default='esp.cube',
            help="ESP descrition (or other scalar field) in all-atom cube file.")
    parser.add_argument('outfile_cube', nargs='?', metavar='outfile.cube', 
            default='esp_fitted_system.top', help="Output truncated by atoms only"
            "present in all-atoms description")
    parser.add_argument('-i','--insertion-rules',
            default="{'CD4':1,'CD3':1,'CA2':2,'CA3':2,'CB2':2,'CB3':2}",
            help="A string representation of a python dictionary, describing how "
            "many implicit hydrogens have been inserted at which atom. Example: "
            "{'CD4':1,'CD3':1,'CA2':2,'CA3':2,'CB2':2,'CB3':2}")
    args = parser.parse_args()

    print('Using replacement rules "{}"...'.format(args.insertion_rules))
    #implicitHbondingPartners = ast.literal_eval(args.insertion_rules)
    
    aa2ua_cube(args.infile_pdb, args.infile_top, args.infile_cube, 
               args.outfile_cube,implicitHbondingPartners=implicitHbondingPartners)


def aa2ua_cube(infile_pdb, infile_top, infile_cube,
               outfile_cube, implicitHbondingPartners):

    ase_struct=ase.io.read(infile_pdb)
    pmd_struct = pmd.load_file(infile_pdb)

    with warnings.catch_warnings():
         warnings.simplefilter('ignore')
         # throws some warnings on angle types, does not matter for bonding info
         pmd_top = gromacs.GromacsTopologyFile(infile_top,parametrize=False)

    pmd_top.strip(':SOL,CL') # strip water and electrolyte from system
    pmd_top.box = pmd_struct.box # Needed because .prmtop contains box info
    pmd_top.positions = pmd_struct.positions

    new_ase_struct, new_pmd_struct, names, residues = insertHbyList(
        ase_struct,pmd_top,implicitHbondingPartners,1.0)


    surplus_atoms = len(new_ase_struct) - len(ase_struct)
    # print("{} atoms are going to be truncated from file "
    #       "{} ...".format(surplus_atoms,infile_cube))
    # hdf5 = h5py.File(infile_h5,'r')
    cube_data, cube_atoms = read_cube_data(infile_cube)
    # print("Truncated atoms: {}".format(cube_atoms[len(ase_struct):]))
    ase.io.write(outfile_cube, cube_atoms[0:len(ase_struct)], data=cube_data)
    # ATTENTION: this script just truncates atoms based on total count difference
    # in UA and AA representations

if __name__ == '__main__':
    main()
