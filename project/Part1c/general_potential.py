# This class reads a data file with m-scheme two-body matrix elements
# and then makes it possible for our program to search in it
from single_particle_state_class import single_particle_state


class GeneralHamiltonian(object):
    def __init__(self,filepotentialname):
        inputfile = open(filepotenialname,"r")
        # Skip all comments
        all_lines = [line for line in inputfile if line[0] != "#"]
        inputfile.close()
        # get how many single particle energies,
        len_sing = None # Change this
        # and store them
        
        

        
        # get how many two particle matrix elements there are
        # 

        
