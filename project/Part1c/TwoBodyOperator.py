import numpy as np
from math import *

def find_index(m_scheme_basis,state):
    res = [i for i ,l in enumerate(m_scheme_basis) if all([(a in l) for a in state])]
    if res==[]:
        return None
    else:
        return res[0]

class TwoBodyOperator(object):
    def __init__(self,sp_basis,m_scheme_basis,potential):

        self.sp_basis = sp_basis
        self.m_scheme_basis = m_scheme_basis
        self.potential = potential
        self.matrix = np.zeros((len(m_scheme_basis),len(m_scheme_basis)))


    def _compute_matrix_elements(self,state,ind_i):
        """
        Calculate H_I|SD> for a single slater determinant |SD>.
        :param state:
        :param ind_i:
        :return:
        """
        # annihilate two particles at place i and j (i<j)
        for i in range(0,len(state)-1):
            for j in range(i+1,len(state)):
                state_a = np.copy(state)
                c = state_a[i]
                d = state_a[j]
                state_a[i] = None
                state_a[j] = None
                state_a = np.array([e for e in state_a if e != None])
                # The j particle is taken out of a state with A-1 particles
                # rather than A particles therefore the subtraction of one
                # in the phase computation
                phase_a = i+j-1
                #print("{}= {} a_{} a_{} {}".format(state_a,(-1)**(phase_a),d,c,state))
                # create two particles with sp states a and b
                for a in range(1,len(self.sp_basis)):
                    if self.sp_basis[a-1] in state_a:
                        continue
                    a_s = self.sp_basis[a-1]
                    # Inserts the new particles, and remember the phase
                    # important to clone state_prime first
                    state_b = None  # needed?
                    phase_b = None  # needed?
                    for k in range(0,len(state_a)):
                        if (a<state_a[k].get_index()):
                            state_b = np.insert(state_a,k,self.sp_basis[a-1])
                            phase_b = k
                            break
                    else: # only necessary for [1,2]?
                        phase_b = len(state_a)
                        state_b = np.append(state_a,self.sp_basis[a-1])
                    #print("{}= {}ad_{} a_{} a_{} {}".format(state_b,(-1)**(phase_a+phase_b),a,d,c,state))
                    for b in range(a+1,len(self.sp_basis)+1):
                        if self.sp_basis[b-1] in state_b:
                            continue
                        b_s = self.sp_basis[b-1]
                        state_c = None # needed?
                        phase_c = None # needed?
                        for k in range(0,len(state_b)):
                            if (b<state_b[k].get_index()):
                                state_c = np.insert(state_b,k,self.sp_basis[b-1])
                                phase_c = k
                                break
                        else:
                            phase_c = len(state_b)
                            state_c = np.append(state_b,self.sp_basis[b-1])
                        ind_j = 0
                        if state_c in self.m_scheme_basis:
                            ind_j = find_index(self.m_scheme_basis.tolist(),state_c)
                            if ind_j == None:
                                continue
                        else:
                            continue
                        #print("{}= {} ad_{} ad_{} a_{} a_{} {}".format(state_c,(-1)**(phase_a+phase_b+phase_c),b,a,d,c,state))
                        #print("state: {0}".format(state))
                        #print("state_c: {0}".format(state_c))
                        #print("({0}, {1}): {2}".format(ind_i,ind_j,self.potential.get_element(a,b,c.get_index(),d.get_index())))
                        print(ind_i,ind_j)
                        self.matrix[ind_i,ind_j]-=self.potential.get_matrix_element(a_s,b_s,c,d)*(1-((phase_a+phase_b+phase_c)%2)*2)

    def compute_matrix(self):
        for i,ket in enumerate(self.m_scheme_basis):
            self._compute_matrix_elements(ket,i)


    def get_matrix(self):
        return self.matrix

