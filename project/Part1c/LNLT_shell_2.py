import argparse
import json
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
from PairingPotential import PairingPotential
from JClass import JClass  # Noam's Jsqaured
from ReadMatrixElementsFile import ReadMatrixElementsFile
from SPSGenerator import SPSGenerator
from TwoBodyOperator import TwoBodyOperator
from hamiltonian_unperturbed import hamiltonian_unperturbed, hamiltonian_unperturbed_pairing
from LevelPloter import LevelPloter
from ResultPrinter import ResultPrinter
from JSquaredOperator import JSquaredOperator  # Tor's Jsquared
from NumberOperatorSquare import NumberOperatorSquare
from OccupationNumber import occupation
from ShellOutput import shell_output
from NucleusManager import NucleusManager
from SpectroScopicFactor import SpectroscopicFactor


np.set_printoptions(threshold='nan')



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
parser = argparse.ArgumentParser(description='Input for shell-model program')
group = parser.add_mutually_exclusive_group()
parser.add_argument('-n','--num_of_particles', help='the number of particles we wish to work with.', default=2, type=int, required=True)
parser.add_argument('-M','--M_total', help='the total M value for constructing an m-scheme basis.', default=0, type=int, required=False, nargs='*')
parser.add_argument('-os','--orbits_separation', help='in case we choose an orbits file, choose also whether to have '
                                                      'separation of orbits in the m-scheme or not. Used only when -of '
                                                      'is used', default=False, type=bool, required=False)
group.add_argument('-if','--interaction_file', help='interaction file name.', default=False, type=str, required=False)
group.add_argument('-of','--orbits_file', help='json file name for defining the wanted orbits.', default=False, type=str, required=False)
parser.add_argument('-o','--output_file',help='specify output file',default='\dev\null',type=str,required=False)
parser.add_argument('-nu','--nushellx_folder',help='specify nushellx lpt directory to compare our results to',default='\dev\null',type=str,required=False)
parser.add_argument('-Z','--protons_number',help='the number of protons',default=16,type=int,required=False)
parser.add_argument('-s','--spec_factors',help='computes the spectroscopic factors to the nucleus with n-1 valence nucleons',default=False,type=bool,required=False)
args = parser.parse_args()
#################### Argparse ####################



sps_object = SPSGenerator()
shell_configurations_list = shell_configurations()
#folder_name = 'input_files/'  # Folder of input files. # Just in the way

shell_list = [] 

if args.orbits_file:
    #with open("".join((folder_name, args.orbits_file)), 'rb') as data_file:
    with open(args.orbits_file, 'rb') as data_file:
        orbits_dict = json.load(data_file)["shell-orbit P-levels"]
        orbits_dict = OrderedDict(sorted(orbits_dict.iteritems(), key=lambda x: x[0]))  # A sorted dictionary.
                                                                                        # Keys are the "p-levels" (the index of the orbit)
                                                                                        # and values several parameters (see file itself).
    sps_object.calc_sps_list(shell_configurations_list, orbits_dict)
    sps_list = sps_object.get_sps_list()
    #shell_list = sps_object.get_shell_list()
    V = PairingPotential(1)

else:
    #interaction_file = open("".join((folder_name, args.interaction_file)), 'rb')
    interaction_file = open(args.interaction_file, 'rb')
    # Read the potential
    V = ReadMatrixElementsFile(interaction_file)
    V.read_file_sps()
    V.read_file_interaction()
    sps_list = V.get_sps_list()


 

def comp_shell(a,b):
    return a.get_n() == b.get_n() and a.get_l() == b.get_l() and a.get_j() == b.get_j()
for current in sps_list:
    if not any([comp_shell(current,sh) for sh in shell_list]):
        shell_list.append(current)


            
current_nucleus = NucleusManager(sps_object,
                                 sps_list,
                                 V)
current_nucleus.set_num_particles(args.num_of_particles)

# Calculate the m_scheme_basis according to whether we have a matrix elements input file or a json orbits file.
if args.M_total:
    if args.orbits_file:
        current_nucleus.set_total_m(args.M_total,orbits_dict, args.orbits_separation)
    else:
        current_nucleus.set_total_m(args.M_total)

if args.orbits_file:
    current_nucleus.compute_eigen_spectrum(True)
else:
    current_nucleus.compute_eigen_spectrum(False)
        

# Setting up and compute the relevant J**2 matrix

current_nucleus.compute_j_squared()

current_nucleus.compute_occupation_numbers()

    
# Prints the result
rp = ResultPrinter(current_nucleus.get_energies(),
                   current_nucleus.get_total_j(),
                   sps_list,
                   current_nucleus.get_m_scheme_basis(),
                   args.nushellx_folder,
                   args.num_of_particles,
                   args.protons_number,
                   current_nucleus.get_occupation_nums())
rp.print_all_to_screen()
if args.output_file:
    rp.print_all_to_file(args.output_file)

if args.spec_factors:
    daughter_nucleus = NucleusManager(sps_object,
                                      sps_list,
                                      V)
    daughter_nucleus.set_num_particles(args.num_of_particles-1)

    if args.M_total:
        if args.orbits_file:
            daughter_nucleus.set_total_m(args.M_total+((args.num_of_particles-1)%2),orbits_dict, args.orbits_separation)
        else:
            print "args.M_total type:{}".format(type(args.M_total))
            print "args.num_of_particles type:{}".format(type(args.num_of_particles))
            daughter_nucleus.set_total_m(args.M_total+((args.num_of_particles-1)%2))
    if args.orbits_file:
        daughter_nucleus.compute_eigen_spectrum(True)
    else:
        daughter_nucleus.compute_eigen_spectrum(False)

    daughter_nucleus.compute_j_squared()

    specs = SpectroscopicFactor(current_nucleus,daughter_nucleus)

    for shell in shell_list:
        th_spec = specs.compute_s(shell)
        print "For: {}".format(shell_output(shell))
        print th_spec
