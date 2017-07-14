from itertools import permutations
from numpy import array
"""
This function generates all Slater determinants from
a single particle basis
"""
def generate_many_body_basis(sp_basis,A):
    mp_basis=[]
    for l in permutations(sp_basis,A):
        mp_basis.append(list(l))
    return array(mp_basis)
    
