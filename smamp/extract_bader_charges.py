""" Extract atomic charges from Bader Charge Analysis output.
Copyright 2019 Simulation Lab
University of Freiburg
Author: ?
Modified: Lukas Elflein <elfleinl@cs.uni-freiburg.de>
"""

import ase
from parmed import gromacs
import numpy as np
import warnings

from smamp.insertHbyList import insertHbyList
from smamp.tools import read_atom_numbers

def extract(snapshot_path='snapshot.pdb', top_path='example.top', bader_path='ACF.dat',
	    out_path='bader_charges.csv', hydrogen_path='hydrogen_per_atom.csv'):
	""" Execute everything."""
	# Read the atomic structure
	ase_struct = ase.io.read(snapshot_path)

	# Read the toplogy
	with warnings.catch_warnings():  # supress warnings
		warnings.simplefilter("ignore")
		pmd_top = gromacs.GromacsTopologyFile(top_path, parametrize=False)

	# Read number of hydrogen per atom from configuration file table
	implicitHbondingPartners = read_atom_numbers(path=hydrogen_path)

	new_ase_struct, new_pmd_top, names, residues = insertHbyList(ase_struct, pmd_top, 
								     implicitHbondingPartners)
	#atomic_number = new_ase_struct.get_atomic_numbers()

	bader_charges = np.genfromtxt(bader_path,skip_header=2,skip_footer=4,usecols=4)
	atomic_number = ase_struct.get_atomic_numbers()

	missing_hydrogens = len(bader_charges) - atomic_number.shape[0] 
	charges = np.ones((missing_hydrogens, ))
	atomic_number = np.concatenate((atomic_number, charges), axis=0)
	atomic_charges = atomic_number - bader_charges  # this inverts the sign of the bader charges

	results =[]
	for i in range(len(atomic_charges)):
		results.append((names[i], residues[i], atomic_charges[i],
				atomic_number[i],bader_charges[i]))

	# find the summed charges of carbon atoms and corresponding H atoms
	# print(implicitHbondingPartners)
	#list_of_C_atoms = ['CD3', 'CD4', 'CA2', 'CA3', 'CB2', 'CB3']
	#list_of_C_atoms += ['CF2', 'CA4']
	list_of_C_atoms = list(implicitHbondingPartners.keys())

	atom_res_totq = []  # list of [C-atom, residue, total_charge]
	nra = np.array([names,residues,atomic_charges])

	total_charge_results = np.array(results)[:,:4]
	total_charge_results[:,3] = total_charge_results[:,2]

	terminal_names = np.unique(nra[1])
	terminal_names = np.delete(terminal_names, np.argwhere(terminal_names == 'SOL'))
	terminal_names = np.delete(terminal_names, np.argwhere(terminal_names == 'CL'))
	for term in terminal_names:
		residue = np.where(nra[1] == str(term))
		print(residue)
		nra_for_one_residue = nra[:,residue[0]]

		# find all carbon atoms and the belonging H atoms
		for c_atom in list_of_C_atoms:
			C_H_positions = np.flatnonzero(np.core.defchararray.find(
							nra_for_one_residue[0], str(c_atom))!=-1)
			C_H_atoms = nra_for_one_residue[:, C_H_positions]
			total_charge = (C_H_atoms[2]).astype(np.float).sum()
			atom_res_totq.append([c_atom, term, total_charge])

			#overwrite the charge of list_of_C_atoms in results with total_charge
			res_position = np.where((total_charge_results[:,0]==c_atom) 
						& (total_charge_results[:,1]==term))
			#print(res_position+(2,))
			total_charge_results[res_position+(3,)] = total_charge

	with open(out_path, 'w') as f:
		f.write("atom,\t residue,\t q"+ '\n')
		for line in total_charge_results:
			f.write(', \t '.join(line[:-1])+'\n')

def main():
	extract()

if __name__ == '__main__':
	main()
