from itertools import combinations
from numpy import array
"""
This function generates all Slater determinants from
a single particle basis
"""
def generate_many_body_basis(sp_basis,a):
    mp_basis=[]
    for l in combinations(sp_basis,a):
        mp_basis.append(list(l))
    return array(mp_basis)
    
