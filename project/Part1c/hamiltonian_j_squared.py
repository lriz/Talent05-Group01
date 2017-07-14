import numpy as np
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