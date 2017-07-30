from numpy import array
class PairingPotential(object):
    def __init__(self,g):
        self.g = g

    def get_matrix_element(self,p,q,r,s):
        if p.get_index()%2==1  and p.get_index()==q.get_index()-1 and r.get_index()%2==1 and r.get_index()==s.get_index()-1:
            return -self.g
        else:
            return 0
        
