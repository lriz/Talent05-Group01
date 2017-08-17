import numpy as np


def comp_shell(a,b):
    return a.get_n() == b.get_n() and a.get_l() == b.get_l() and a.get_j() == b.get_j()


def occupation(shell,state,mp_basis):
    members=[i for i,s in enumerate(mp_basis) if any([comp_shell(sps,shell) for sps in s])]
    weights=np.array([len([a for a in s if comp_shell(a,shell)]) for s in mp_basis[members]])
    return np.sum(weights*state[members]**2)
