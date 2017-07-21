import numpy as np
import matplotlib.pyplot as plt
from math import *
from SingleParticleState import SingleParticleState
from itertools import combinations
from TwoBodyOperator import TwoBodyOperator
from sympy import S
from sympy.physics.wigner import clebsch_gordan


def comp_shell(a,b):
    return a.get_n() == b.get_n() and a.get_l() == b.get_l() and a.get_j() == b.get_j()

class JSquaredOperator(object):
    def __init__(self):
        pass
    def get_matrix_element(self,p,q,r,s):
        if ((comp_shell(p,r) and comp_shell(q,s)) and
            (p.get_m_j()-r.get_m_j())==2 and
            (q.get_m_j()-s.get_m_j())==-2):
            print("(p ~ r +)(q ~ s -) sqrt(({0}-{1})({0}+{1}+1)({2}+{3})({2}-{3}+1))".format(r.get_j()/2.0,r.get_m_j()/2.0,s.get_j()/2.0,s.get_m_j()/2.0))
            return sqrt((r.get_j()*0.5-r.get_m_j()*0.5)*
                        (r.get_j()*0.5+r.get_m_j()*0.5+1)*
                        (s.get_j()*0.5+s.get_m_j()*0.5)*
                        (s.get_j()*0.5-s.get_m_j()*0.5+1))
        elif ((comp_shell(p,r) and comp_shell(q,s)) and
              (p.get_m_j()-r.get_m_j())==-2 and
              (q.get_m_j()-s.get_m_j())==2):
            print("(p ~ r -)(q ~ s +) sqrt(({0}+{1})({0}-{1}+1)({2}-{3})({2}+{3}+1))".format(r.get_j()/2.0,r.get_m_j()/2.0,s.get_j()/2.0,s.get_m_j()/2.0))
            return sqrt((r.get_j()*0.5+r.get_m_j()*0.5)*
                        (r.get_j()*0.5-r.get_m_j()*0.5+1)*
                        (s.get_j()*0.5-s.get_m_j()*0.5)*
                        (s.get_j()*0.5+s.get_m_j()*0.5+1))
        elif ((comp_shell(p,s) and comp_shell(q,r)) and
              (p.get_m_j()-s.get_m_j())==2 and
              (q.get_m_j()-r.get_m_j())==-2):
            print("(p ~ s +)(q ~ r -) sqrt(({0}-{1})({0}+{1}+1)({2}+{3})({2}-{3}+1))".format(s.get_j()/2.0,s.get_m_j()/2.0,r.get_j()/2.0,r.get_m_j()/2.0))
            return -sqrt((s.get_j()*0.5-s.get_m_j()*0.5)*
                         (s.get_j()*0.5+s.get_m_j()*0.5+1)*
                         (r.get_j()*0.5+r.get_m_j()*0.5)*
                         (r.get_j()*0.5-r.get_m_j()*0.5+2))
        elif ((comp_shell(p,s) and comp_shell(q,r)) and
              (p.get_m_j()-s.get_m_j())==-2 and
              (q.get_m_j()-r.get_m_j())==2):
            print("(p ~ s -)(q ~ r +) sqrt(({0}+{1})({0}-{1}+1)({2}-{3})({2}+{3}+1))".format(s.get_j()/2.0,s.get_m_j()/2.0,r.get_j()/2.0,r.get_m_j()/2.0))
            return -sqrt((s.get_j()*0.5+s.get_m_j()*0.5)*
                         (s.get_j()*0.5-s.get_m_j()*0.5+1)*
                         (r.get_j()*0.5-r.get_m_j()*0.5)*
                         (r.get_j()*0.5+r.get_m_j()*0.5+1))
        else:
            return 0

    def get_single_body_contribution(self,m_scheme_basis):
        diagonal = [np.sum(np.array([a.get_j()*(a.get_j()+2)*0.25 for a in state])) for state in m_scheme_basis]
        return np.diag(diagonal)


def expected_JJ2b(mp_basis):
    if (len(mp_basis[0]) != 2):
        print "Expects a 2 body basis"
        exit(1)
    mat = np.zeros((len(mp_basis),len(mp_basis)))
    for i,a in enumerate(mp_basis):
        min_jta = abs(a[0].get_j()-a[1].get_j())
        max_jta = a[0].get_j()+a[1].get_j()
        paulia = False
        Na=1
        if comp_shell(a[0],a[1]):
            Na = 1/sqrt(2)
            paulia = True
        for j,b in enumerate(mp_basis):
            min_jtb = abs(b[0].get_j()-b[1].get_j())
            max_jtb = b[0].get_j()+b[1].get_j()
            Nb = 1
            paulib = False
            if comp_shell(b[0],b[1]):
                Nb = 1/sqrt(2)
                paulib = True
            if comp_shell(a[0],b[0]) and comp_shell(a[1],b[1]):
                for J_tot in range(max(min_jta,min_jtb),
                                   min(max_jta,max_jtb)+1,2):
                    if (paulia or paulib) and (J_tot/2)%2 == 0:
                        continue
                    cg1 = clebsch_gordan(S(a[0].get_j())/2,
                                         S(a[1].get_j())/2,
                                         S(J_tot)/2,
                                         S(a[0].get_m_j())/2,
                                         S(a[1].get_m_j())/2,
                                         S(a[0].get_m_j()+
                                           a[1].get_m_j())/2).evalf(8)
                    if (abs(cg1)<1e-5):
                        continue
                    cg2 = clebsch_gordan(S(b[0].get_j())/2,
                                         S(b[1].get_j())/2,
                                         S(J_tot)/2,
                                         S(b[0].get_m_j())/2,
                                         S(b[1].get_m_j())/2,
                                         S(b[0].get_m_j()+
                                           b[1].get_m_j())/2).evalf(8)
                    if (abs(cg2)<1e-5):
                        continue
                    mat[i,j]+=cg1*cg2*J_tot*(J_tot+1)
    return mat
    
if __name__=="__main__":
    # Setting up a single particle basis
    Nmax = 1
    i = 1
    sp_basis=[]
    for N in range(Nmax+1):
        for l in range(N%2,N+1,2):
            n = (N-l)/2
            for j in range(abs(2*l-1),2*l+2,2):
                for m in range(-j,j+1,2):
                    sp_basis.append(SingleParticleState(0,n,l,j,m,i))
                    i+=1
    #end of for loops
    sp_basis = np.array(sp_basis)
    print("The single particle basis\n")
    for sp in sp_basis:
        print("{}: {} {} {} {}".format(sp.get_index(),sp.get_n(),sp.get_l(), sp.get_j(), sp.get_m_j()))
    n = 2
    # Setting up a many particle basis
    mp_basis=np.array([a for a in combinations(sp_basis,n) if np.sum([p.get_m_j() for p in a]) == 0])
    #mp_basis=np.array([a for a in combinations(sp_basis,n)])
    print("The many particle basis\n")
    for mp in mp_basis:
        print(mp)
    
    jsqop = JSquaredOperator()
    jstbop = TwoBodyOperator(sp_basis,mp_basis,jsqop)
    jstbop.compute_matrix()
    jsqmat = jstbop.get_matrix()
    jsqmat += jsqop.get_single_body_contribution(mp_basis) 

    print "What we got:"
    print jsqmat

    jsqmat_exp = expected_JJ2b(mp_basis)
    print "What we expect"
    print jsqmat_exp

    eig_val_exp,eig_vec_exp = np.linalg.eig(jsqmat_exp)
    print(np.sort(np.real(eig_val_exp)))
    
    f,ax = plt.subplots(1,3)
    ax[0].matshow(jsqmat)
    ax[1].matshow(jsqmat_exp)
    ax[2].matshow(np.abs(jsqmat-jsqmat_exp))
    plt.show()
    if np.sum(np.sum(np.abs(jsqmat-np.transpose(jsqmat))))>1e-10:
        print("The j_square_matrix is not symmetric, but it should be")
        exit(1)

    jsq_eig_vals,jsq_eig_vecs = np.linalg.eig(jsqmat)

    print(np.sort(jsq_eig_vals))


    
    for ev in jsq_eig_vals:
        if abs(ev-float(int(ev)))>1e-5:
            print "The eigenvalues of the j_square_matrix are not whole numbers"
            exit(1)
    
