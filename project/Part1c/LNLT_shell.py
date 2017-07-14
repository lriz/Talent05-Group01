import numpy as np
import matplotlib.pyplot as plt
import json
import argparse
from collections import OrderedDict
from single_particle_state_class import single_particle_state
from hamiltonian_unperturbed import hamiltonian_unperturbed
from hamiltonian_j_squared import hamiltonian_j_squared
from sps_generator import sps_generator
from interaction_hamiltonian import TwoBodyInteraction
from pairing_potential import PairingPotential
from general_potential import GeneralHamiltonian
from generate_many_body_basis import generate_many_body_basis


def shell_configurations():
    return [{'name': '0s1/2', 'N': 0},
            {'name': '0p3/2', 'N': 1},
            {'name': '0p1/2', 'N': 1},
            {'name': '0d5/2', 'N': 2},
            {'name': '1s1/2', 'N': 2},
            {'name': '0d3/2', 'N': 2},
            {'name': '0f7/2', 'N': 3},
            {'name': '1p3/2', 'N': 3},
            {'name': '0f5/2', 'N': 3},
            {'name': '1p1/2', 'N': 3},
            {'name': '0g9/2', 'N': 4}]

#################### Argparse ####################
# get arguments from the command line.
parser = argparse.ArgumentParser(description='None')  # Generate a parser.
#parser.add_argument('-c','--config',help='a json config file name for the program', type=str,required=True)  # Define a command line operation.
#group = parser.add_mutually_exclusive_group(required=True)
# Only one of these can appear in the terminal (mutually exclusive)
#group.add_argument('-f','--file',help='a json input file name for the program', type=str)  # a command line operation.
#group.add_argument('-i','--interaction_file',help='a text input file name to a given interaction file', type=str)  # a command line operation.
parser.add_argument('-f','--file',help='a json input file name for the program', type=str)  # a command line operation.
args = parser.parse_args()
#################### Argparse ####################

folder_name = 'input_files/'  # Folder of input files.
with open("".join((folder_name,args.file))) as data_file:
        orbits_dict = json.load(data_file)  # A dictionary. Keys are the name of input, values are the value of input.

#with open("".join((folder_name,args.config))) as data_file:
#        config_dict = json.load(data_file)  # A dictionary. Keys are the name of input, values are the value of input.

#################### Global parameters ####################
shell_configurations_list = shell_configurations()
# Ordering the dictionary according to P values.
orbits_dict["shell-orbit P-levels"] = OrderedDict(sorted(orbits_dict["shell-orbit P-levels"].iteritems(), key=lambda x: x[0]))
#################### Global parameters ####################

#################### Get m_scheme_basis ####################
sps_generator_obj = sps_generator(orbits_dict)
sps_generator_obj.calc_m_broken_basis(shell_configurations_list)
m_broken_basis = sps_generator_obj.get_m_broken_basis()
sps_list = sps_generator_obj.get_sps_list()
sps_generator_obj.calc_m_scheme_basis(m_broken_basis)
m_scheme_basis = np.array(sps_generator_obj.get_m_scheme_basis())
#################### Get m_scheme_basis ####################

#################### Print ####################
print(sps_list)
sps_generator_obj.print_sps()
print
print "Number of general {}-particle states:".format(orbits_dict["number of particles"]),len(m_broken_basis)
sps_generator_obj.print_m_scheme_basis()
print hamiltonian_unperturbed_pairing(m_scheme_basis)
#################### Print ####################

#TODO: change names so we'd remember in the future.
gl = np.linspace(-1,1)
energies=[];
#for g in gl:
g = 1
#V = PairingPotential(g)
V = GeneralHamiltonian("sdshellint.dat")
V.read_file_sps()
V.read_file_interaction()
#tbi = TwoBodyInteraction(get_all_sps_list,m_scheme_basis,V)
mp_basis = generate_many_body_basis(V.get_sps_list(),3)
print("dim: {0}".format(len(mp_basis)))
tbi = TwoBodyInteraction(get_all_sps_list,mp_basis,V)
print("Computes interaction hamiltonian")
tbi.compute_matrix()
print("Computes unperturbed hamiltonain")
H0 = hamiltonian_unperturbed(mp_basis,V.get_sp_energies())
HI = tbi.get_matrix()
#print HI
#for g in gl:
H = H0+HI
    #print("Hamiltonian:")
    #print H

energies, eig_vectors_list = np.linalg.eig(np.array(H))
print("The eigen values:")
print(np.sort(energies))
#np.set_printoptions(threshold='nan')  # Command to print entire matrix.
H_j = hamiltonian_j_squared(eig_vectors_list, m_scheme_basis)
# Count num. of off-diagonal elements (search for degeneracies)
# Remove the diagonal part of H_j and then count non-zero elements.
print np.count_nonzero(H_j - np.diag(np.diagonal(H_j)))
print np.diagonal(H_j)  # Look at the diagonal part of H_j.
for j in np.diagonal(H_j):
        print j, np.roots([1,1,-j])[-1]
#np.count_nonzero(h_j - np.diag(np.diagonal(h_j)))
#    energies.append(np.sort(eigs))

#energies = np.array(energies)
#for i in range(0,len(m_broken_basis)):
#    plt.plot(gl,energies[:,i])
#plt.show()
