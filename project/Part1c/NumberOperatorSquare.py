import numpy as np
class NumberOperatorSquare(object):
    def __init__(self):
        pass

    def get_matrix_element(self,a,b,c,d):
        if (a == c and b == d):
            return 1
        else:
            return 0

    def get_single_particle(self,m_scheme_basis):
        return np.diag([len(state) for state in m_scheme_basis])
