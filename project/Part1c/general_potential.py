from single_particle_state_class import single_particle_state
import numpy as np

class GeneralHamiltonian(object):
    """
    This class reads a data file with m-scheme two-body matrix elements
    and then makes it possible for our program to search in it.
    """
    def __init__(self,interaction_filename):
        """
        :param interaction_filename: the interaction filename. Opened from 'input_file/' directory.
        self.input_file: the opened interaction filename.
        self.file_list: a list of the interaction filename, comments refined out.
        self.sps_length: number of single particle states.
        :return:
        """
        folder_name = 'input_files/'  # Folder of input files.
        self.input_file = open("".join((folder_name, interaction_filename)))
        self.file_list = []
        self.sps_length = 0

    def refine_comments(self):
        """
        Skip all comments.
        :return: (alters self)
        """
        self.file_list = [line for line in self.input_file if line[0] != "#"]
        self.input_file.close()

    def read_file_sps(self):
        self.refine_comments()
        # get how many single particle energies.
        self.sps_length = int(self.file_list[0])
        # and store them
        self.sp_energies = []
        self.sp_states = []
        for i in range(1, self.sps_length+1):
            line_split = self.file_list[i].split()
            self.sp_energies.append(float(line_split[-1]))
            state = single_particle_state(int(line_split[1]),
                                          int(line_split[1]),
                                          int(line_split[2]),
                                          int(line_split[3]),
                                          int(line_split[4]),
                                          int(line_split[0]))
            self.sp_states.append(state)

    def read_file_interaction(self):
        self.tp_matelems = np.zeros((self.sps_length, self.sps_length, self.sps_length, self.sps_length))
        # get how many two particle matrix elements there are
        len_tpme = int(self.file_list[1+self.sps_length])
        # read all two particle matrix elements
        for i in range(self.sps_length+2,self.sps_length+len_tpme+2):
            line_split = self.file_list[i].split()
            a = int(line_split[0])-1
            b = int(line_split[1])-1
            c = int(line_split[2])-1
            d = int(line_split[3])-1
            elem = float(line_split[4])
            self.tp_matelems[a,b,c,d] = elem

    def get_element(self,a,b,c,d):
        return self.tp_matelems[a-1,b-1,c-1,d-1]
            
        
