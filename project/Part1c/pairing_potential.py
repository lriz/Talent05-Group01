class PairingPotential(object):
    def __init__(self,g):
        self.g = g
    def get_matrix_element(self,p,q,r,s):
        if p%2==1  and p==q-1 and r%2==1 and r==s-1:
            return -self.g
        else:
            return 0
