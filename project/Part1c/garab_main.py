import numpy as np
import matplotlib.pyplot as plt
import json
import argparse
from collections import OrderedDict
from SingleParticleState import SingleParticleState
from hamiltonian_unperturbed import hamiltonian_unperturbed
from hamiltonian_unperturbed import hamiltonian_unperturbed_pairing
from SPSGenerator import SPSGenerator
from TwoBodyOperator import TwoBodyOperator
from PairingPotential import PairingPotential
from GeneralHamiltonian import GeneralHamiltonian
from generate_many_body_basis import generate_many_body_basis
from LevelPloter import LevelPloter

A = 18
n = A-16

# Read the potential
V = GeneralHamiltonian("sdshellint.dat")
V.read_file_sps()
V.read_file_interaction()
mp_basis = generate_many_body_basis(V.get_sps_list(),n)

mp_basis_m0 = np.array([state for state in mp_basis if np.sum([a.get_m_j() for a in state])==0])

print("dim: {0}".format(len(mp_basis_m0)))
tbi = TwoBodyOperator(V.get_sps_list(),mp_basis_m0,V)
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

#level_diagram = LevelPloter(np.sort(eigs))
#level_diagram.plotLevels()
