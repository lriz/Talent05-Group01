from itertools import combinations
from numpy import array

def generate_many_body_basis(sps_list, n):
    """
    Calculate all Slater determinants from a single particle basis.
    :param sps_list: a list of all the single particle state.
    :param n: number of particles to couple together.
    :return:
    """
    mp_basis=[]
    for l in combinations(sps_list, n):
        mp_basis.append(list(l))
    return array(mp_basis)
    
