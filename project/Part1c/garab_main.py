import numpy as np
import matplotlib.pyplot as plt
import json
import argparse
from collections import OrderedDict
from single_particle_state_class import single_particle_state
from hamiltonian_unperturbed import hamiltonian_unperturbed
from hamiltonian_unperturbed import hamiltonian_unperturbed_pairing
from sps_generator import sps_generator
from interaction_hamiltonian import TwoBodyInteraction
from pairing_potential import PairingPotential
from general_potential import GeneralHamiltonian
from generate_many_body_basis import generate_many_body_basis
from level_ploter import LevelPloter

A = 20
n = A-16

# Read the potential
V = GeneralHamiltonian("sdshellint.dat")
V.read_file_sps()
V.read_file_interaction()
mp_basis = generate_many_body_basis(V.get_sps_list(),n)

mp_basis_m0 = np.array([state for state in mp_basis if np.sum([a.get_m_j() for a in state])==0])

print("dim: {0}".format(len(mp_basis_m0)))
tbi = TwoBodyInteraction(V.get_sps_list(),mp_basis_m0,V)
print("Computes interaction hamiltonian")
tbi.compute_matrix()
print("Computes unperturbed hamiltonain")
H0 = hamiltonian_unperturbed(mp_basis_m0,V.get_sp_energies())
HI = tbi.get_matrix()
if np.sum(np.sum(np.abs(HI - np.transpose(HI))))>1e-10:
    print("Interaction hamiltonian is not symmetric")
    exit(1)
factor = (18.0/(16.0+n))**0.3
H=H0+factor*HI

eigs_0,vecs_0 = np.linalg.eig(H0) 
print("The H0 eigien values:")
print(np.diag(H0))
eigs,vecs = np.linalg.eig(np.array(H))
print("The eigen values:")
print(np.sort(eigs))

level_diagram = LevelPloter(np.sort(eigs))
level_diagram.plotLevels()

values=[]
for i,e in enumerate(eigs):
    jj = np.dot(vecs[:,i],np.dot(jjmat,vecs[:,i]))
    values.append((e,np.round(jj,3),np.round(np.roots([1,1,-jj])[-1])))

values = sorted(values,key=lambda k : k[0])
for tup in values:
    print "E: {} J(J+1): {} J: {}".format(*tup)

