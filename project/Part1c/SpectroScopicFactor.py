import numpy as np
from sympy import S
from sympy.physics.wigner import clebsch_gordan
# computes the spectroscopic factors for two nuclei where N differ with one and Z is the same
class SpectroscopicFactor(object):
    def __init__(self,nucleus1,nucleus2):
        in_A = nucleus1.get_num_particles()+16
        out_A = nucleus2.get_num_particles()+16
        if (in_A-out_A != 1):
            print("To compute a spectro scopic factor, the two nuclei has to have a A difference of 1")
            exit(1)
        self.nucleus1 = nucleus1
        self.nucleus2 = nucleus2
    def compute_s(self,shell):
        shell = shell.copy()
        shell.m_j = 1/2
        in_states = self.nucleus1.get_eigenstates()
        out_states = self.nucleus2.get_eigenstates()
        in_j = self.nucleus1.get_total_j()
        out_j = self.nucleus2.get_total_j()
        in_basis = self.nucleus1.get_m_scheme_basis()
        out_basis = self.nucleus2.get_m_scheme_basis()
        # Enough to compute it for m = 1/2 and then use Wigner-Eckart
        # Therefore the code now determines which states contains shell
        filtered_in_basis = [(list(out_basis).index(np.array([s for s in state if s != shell])),i,list(state).index(shell)) for i,state in enumerate(np.transpose(in_basis)) if shell in state]
        print("filtered_in_basis = {}".format(filtered_in_basis))

        print in_basis
        
        #for i in xrange(len(in_basis)):
        #    if shell in in_basis(
        

        specs=[]
        #for i,inv in enumerate(in_states):
        i = 0
        inv = in_states[:,0]
        cur_specs = []
        for j in xrange(len(out_states)):
            outv = out_states[:,j]
            print "|{1}-{2}|<={0}<={1}+{2}".format(shell.get_j()/2.0,in_j[i],out_j[j])
            if shell.get_j()<= 2*abs(in_j[i]-out_j[j]) or shell.get_j()>=2*(in_j[i]+out_j[j]):
                continue
            Sm = np.sum(np.array([outv[comp[0]]*inv[comp[1]]*((-1)**comp[2]) for comp in filtered_in_basis]))
            print "Sm = {}".format(Sm)
            cur_specs.append((Sm/(clebsch_gordan(S(int(2*out_j[j]))/2,
                                                 S(shell.get_j())/2,
                                                 S(int(2*in_j[i]))/2,
                                                 S(self.nucleus2.get_m())/2,
                                                 S(shell.get_m_j())/2,
                                                 S(self.nucleus1.get_m())/2).evalf(10)))**2)
        specs.append(cur_specs)
        return specs

        
        
