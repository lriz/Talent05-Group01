# This class reads a data file with m-scheme two-body matrix elements
# and then makes it possible for our program to search in it
from single_particle_state_class import single_particle_state
import numpy as np

class GeneralHamiltonian(object):
    def __init__(self,filepotentialname):
        inputfile = open(filepotentialname,"r")
        # Skip all comments
        all_lines = [line for line in inputfile if line[0] != "#"]
        inputfile.close()
        # get how many single particle energies,
        len_sing = int(all_lines[0])
        # and store them
        self.sp_energies = []
        self.sp_states = []
        for i in range(1,len_sing+1):
            line_split = all_lines[i].split()
            self.sp_energies.append(float(line_split[-1]))
            state = single_particle_state(int(line_split[1]),
                                          int(line_split[1]),
                                          int(line_split[2]),
                                          int(line_split[3]),
                                          int(line_split[4]),
                                          int(line_split[0]))
            self.sp_states.append(state)
        
            
        self.tp_matelems = np.zeros((len_sing,len_sing,len_sing,len_sing))
        # get how many two particle matrix elements there are
        len_tpme = int(all_lines[1+len_sing])
        # read all two particle matrix elements
        for i in range(len_sing+2,len_sing+len_tpme+2):
            line_split = all_lines[i].split()
            a = int(line_split[0])-1
            b = int(line_split[1])-1
            c = int(line_split[2])-1
            d = int(line_split[3])-1
            elem = float(line_split[4])
            self.tp_matelems[a,b,c,d] = elem

    def get_element(self,a,b,c,d):
        return self.tp_matelems[a-1,b-1,c-1,d-1]
            
        
