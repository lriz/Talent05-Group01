import numpy as np
from math import *

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
            
