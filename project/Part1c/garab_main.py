import argparse
import json
from collections import OrderedDict

import matplotlib.pyplot as plt
import numpy as np
from interaction_hamiltonian import TwoBodyInteraction

from hamiltonian_unperturbed import hamiltonian_unperturbed_pairing
from project.Part1c.PairingPotential import PairingPotential


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
parser.add_argument('-f','--file',help='a json input file name for the program', type=str,required=True)  # Define a command line operation.
args = parser.parse_args()
#################### Argparse ####################

folder_name = 'input_files/'  # Folder of input files.
with open("".join((folder_name,args.file))) as data_file:
        input_dict = json.load(data_file)  # A dictionary. Keys are the name of input, values are the value of input.

#################### Global parameters ####################
shell_configurations_list = shell_configurations()
# Ordering the dictionary according to P values.
input_dict["shell-orbit P-levels"] = OrderedDict(sorted(input_dict["shell-orbit P-levels"].iteritems(), key=lambda x: x[0]))
#################### Global parameters ####################

#################### Get m_scheme_basis ####################
sps_generator_obj = sps_generator(input_dict)
sps_generator_obj.calc_m_broken_basis(shell_configurations_list)
m_broken_basis = sps_generator_obj.get_m_broken_basis()
get_all_sps_list = sps_generator_obj.get_all_sps_list()
sps_generator_obj.calc_m_scheme_basis(m_broken_basis)
m_scheme_basis = np.array(sps_generator_obj.get_m_scheme_basis())

#################### Get m_scheme_basis ####################

#################### Print ####################
print(get_all_sps_list)
sps_generator_obj.print_sps()
print
print "Number of general {}-particle states:".format(input_dict["number of particles"]),len(m_broken_basis)
sps_generator_obj.print_m_scheme_basis()
print hamiltonian_unperturbed_pairing(m_scheme_basis)
#################### Print ####################

#TODO: change names so we'd remember in the future.
gl = np.linspace(-1,1)
energies=[];
#for g in gl:
g = 1
V = PairingPotential(g)
#V = GeneralHamiltonian("sdshellint.dat")
#V.read_file_sps()
#V.read_file_interaction()
tbi = TwoBodyInteraction(get_all_sps_list,m_scheme_basis,V)
#mp_basis = generate_many_body_basis(V.get_sps_list(),3)
#print("dim: {0}".format(len(mp_basis)))
#tbi = TwoBodyInteraction(V.get_sps_list(),mp_basis,V)
print("Computes interaction hamiltonian")
tbi.compute_matrix()
print("Computes unperturbed hamiltonain")
H0 = hamiltonian_unperturbed_pairing(m_scheme_basis)
HI = tbi.get_matrix()
print "Total Hamiltonian for g = 1:"
print H0+HI
#print HI
for g in gl:
    H = H0+g*HI
    #print("Hamiltonian:")
    #print H

    eigs,vecs = np.linalg.eig(np.array(H))
    #print("The eigen values:")
    #print(np.sort(eigs))
    energies.append(np.sort(eigs))

energies = np.array(energies)
for i in range(0,len(m_scheme_basis)):
    plt.plot(gl,energies[:,i])
plt.xlabel(r"$g \in [-1,1]$")
plt.ylabel(r"$E$")
plt.show()

