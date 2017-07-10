import numpy as np
def hamiltonian_unperturbed(m_scheme_basis):
    """
    The unperturbed Hamiltonian.
    :param m_scheme_basis: a basis of sps in m_scheme.
    :return: the Hamiltonian matrix.
    """
    print "hamiltonian_unperturbed"
    h_matrix = np.array([])  # the unperturbed  Hamiltonian matrix.
    for eig in m_scheme_basis:
        h_matrix = np.append(h_matrix, sum([int(i.get_p())-1 for i in eig]))
