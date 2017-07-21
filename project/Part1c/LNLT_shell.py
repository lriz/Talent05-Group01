import argparse
import json
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
from PairingPotential import PairingPotential

from ReadMatrixElementsFile import ReadMatrixElementsFile
from SPSGenerator import SPSGenerator
from TwoBodyOperator import TwoBodyOperator
from hamiltonian_unperturbed import hamiltonian_unperturbed, hamiltonian_unperturbed_pairing
from LevelPloter import LevelPloter
from ResultPrinter import ResultPrinter
from JSquaredOperator import JSquaredOperator
from NumberOperatorSquare import NumberOperatorSquare



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
parser.add_argument('-o','--output_file',help='specify output file',default='/dev/null',type=str,required=False)
args = parser.parse_args()
#################### Argparse ####################

sps_object = SPSGenerator()
shell_configurations_list = shell_configurations()
folder_name = 'input_files/'  # Folder of input files.

if args.orbits_file:
    with open("".join((folder_name, args.orbits_file)), 'rb') as data_file:
        orbits_dict = json.load(data_file)["shell-orbit P-levels"]
        orbits_dict = OrderedDict(sorted(orbits_dict.iteritems(), key=lambda x: x[0]))  # A sorted dictionary.
                                                                                        # Keys are the "p-levels" (the index of the orbit)
                                                                                        # and values several parameters (see file itself).
    sps_object.calc_sps_list(shell_configurations_list, orbits_dict)
    sps_list = sps_object.get_sps_list()
    
    V = PairingPotential(1)

else:
    interaction_file = open("".join((folder_name, args.interaction_file)), 'rb')
    # Read the potential
    V = ReadMatrixElementsFile(interaction_file)
    V.read_file_sps()
    V.read_file_interaction()
    sps_list = V.get_sps_list()

sps_object.calc_m_broken_basis(sps_list, args.num_of_particles)
m_broken_basis = sps_object.get_m_broken_basis()

# Calculate the m_scheme_basis according to whether we have a matrix elements input file or a json orbits file.
if args.M_total:
    if args.orbits_file:
        sps_object.calc_m_scheme_basis(m_broken_basis, args.M_total, orbits_dict, args.orbits_separation)
    else:
        sps_object.calc_m_scheme_basis_no_orbit_separation(m_broken_basis, args.M_total)
    m_scheme_basis = sps_object.get_m_scheme_basis()
    print 'm_scheme_basis',m_scheme_basis
else:
    m_scheme_basis = np.array(m_broken_basis)
sps_object.set_sps_list(sps_list)
sps_object.print_sps()

print("dim: {0}".format(len(m_scheme_basis)))

tbi = TwoBodyOperator(sps_list, m_scheme_basis, V)
print("Computes interaction hamiltonian")
tbi.compute_matrix()
print("Computes unperturbed hamiltonain")
if args.orbits_file:
    H0=hamiltonian_unperturbed_pairing(m_scheme_basis)
else:
    H0 = hamiltonian_unperturbed(m_scheme_basis, V.get_sp_energies())

HI = tbi.get_matrix()
if np.sum(np.sum(np.abs(HI - np.transpose(HI))))>1e-10:
    print("Interaction hamiltonian is not symmetric")
    exit(1)
factor = (18.0/(16.0+args.num_of_particles))**0.3
if args.orbits_file:
    factor =1
H=H0+factor*HI

energies, eig_vectors_list = np.linalg.eig(np.array(H))

energyzip = zip(energies.tolist(),eig_vectors_list.tolist())
energyzip = sorted(energyzip,key=lambda k: k[0])
en,ev =zip(*energyzip)
energies = list(en)
eig_vectors_list = list(ev)

jjop = JSquaredOperator()
jjopmb = TwoBodyOperator(sps_list,m_scheme_basis,jjop)
jjopmb.compute_matrix()
jjop1bmat = jjop.get_single_body_contribution(m_scheme_basis)
jjopmat = jjopmb.get_matrix()
out_str = ""
for r in jjopmat:
    for e in r:
        out_str+="{} ".format(np.round(e,3))
    out_str+="\n"
print(out_str)

out_str = ""
for r in jjop1bmat:
    for e in r:
        out_str+="{} ".format(np.round(e,3))
    out_str+="\n"
print(out_str)

jjopmat=jjopmat+jjop1bmat

plt.matshow(jjopmat)
plt.show()

jj_diag,jj_Q = np.linalg.eig(jjopmat)
print("J^2 eigen values:\n")
print(np.sort(jj_diag))
#for e in jj_diag:
#    if (e != float(int(e))):
#        print("the eigenvalues of J^2 should be an integer")
#        exit(1)


#Number operator squared
num = NumberOperatorSquare()
nummb = TwoBodyOperator(sps_list,m_scheme_basis,num)
nummb.compute_matrix()
nummat = nummb.get_matrix()+num.get_single_particle(m_scheme_basis)




#jjopmat_transf = np.zeros((len(eig_vectors_list),len(eig_vectors_list)))

#for i,v1 in enumerate(eig_vectors_list):
#    for j,v2 in enumerate(eig_vectors_list):
#        jjopmat_transf[i,j]=np.dot(v1,np.dot(jjopmat,v2))

#print("min: {}".format(np.min(np.min(np.abs(jjopmat_transf)))))
#plt.matshow(jjopmat_transf)
#plt.colorbar()
#plt.show()




j_list = []
for ev in eig_vectors_list:
    jj = np.dot(ev,np.dot(nummat,ev))
    #j_list.append(np.roots([1,1,-jj]))
    j_list.append(jj)
rp = ResultPrinter(energies,
                   j_list,
                   sps_list,
                   m_scheme_basis)
rp.print_all_to_screen()
if args.output_file:
    rp.print_all_to_file(args.output_file)

#print("The eigen values:")

#print(np.sort(energies))

#level_diagram = LevelPloter(np.sort(energies))
#level_diagram.plotLevels()

plt.plot(eig_vectors_list[0])
plt.show()
