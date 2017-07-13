import numpy as np
def hamiltonian_unperturbed(m_scheme_basis):
    """
    The unperturbed Hamiltonian.
    :param m_scheme_basis: a basis of sps in m_scheme.
    :return: the Hamiltonian matrix.
    """
    dim = len(m_scheme_basis)
    h_matrix = np.zeros((dim, dim))  # the unperturbed  Hamiltonian matrix.
    for i, eig in enumerate(m_scheme_basis):
        s = np.sum([int(j.get_p())-1 for j in eig])
        h_matrix[i,i] = s
    return h_matrix