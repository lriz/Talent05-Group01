import numpy as np
import matplotlib.pyplot as plt
import json
import argparse
from collections import OrderedDict
from SingleParticleState import SingleParticleState
from hamiltonian_unperturbed import hamiltonian_unperturbed
from hamiltonian_unperturbed import hamiltonian_unperturbed_pairing
from SPSGenerator import SPSGenerator
from TwoBodyInteraction import TwoBodyInteraction
from pairing_potential import PairingPotential
from GeneralHamiltonian import GeneralHamiltonian
from generate_many_body_basis import generate_many_body_basis
from j_operator import get_JJ_operator
from LevelPloter import LevelPloter

A = 18
n = A-16


def hamiltonian_j_squared(eig_vectors_list, m_scheme_basis):
    """
    The j(j+1) Hamiltonian.
    :param m_scheme_basis: a basis of sps in m_scheme.
    :param eig_vectors_list: a list of all eigenvectors of the diagonalized matrix.
    :return: the Hamiltonian matrix.
    """
    #TODO: check len(m_scheme_basis) == len(eig_vectors)
    dim = len(eig_vectors_list)
    j_squared_matrix = np.zeros((dim, dim))  # the unperturbed  Hamiltonian matrix.
    j_state = np.array([])  # j(j+1) calculated for each eig in m_scheme_basis.
    # Calculate the j(j+1) value for each m_scheme_basis state and store it in the corresponding index.
    for m_state in m_scheme_basis:
        j_state = np.append(j_state, np.sum([l.get_j()*(l.get_j()+1) for l in m_state]))
    for i, eig_i in enumerate(eig_vectors_list):
        eig_mult_j = np.multiply(eig_i, j_state)  # Multiply corresponding components of j_state with eig_i - returns a new np.array (not a dot product).
        for j, eig_j in enumerate(eig_vectors_list):
            dot_prod = np.dot(eig_mult_j, eig_j)
            j_squared_matrix[i,j] = dot_prod
    return j_squared_matrix

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


jjmat =  get_JJ_operator(V.get_sp_energies(),mp_basis_m0)
print jjmat

values=[]
for i,e in enumerate(eigs):
    jj = np.dot(vecs[:,i],np.dot(jjmat,vecs[:,i]))
    values.append((e,np.round(jj,3),np.round(np.roots([1,1,-jj])[-1])))

values = sorted(values,key=lambda k : k[0])
for tup in values:
    print "E: {} J(J+1): {} J: {}".format(*tup)

