import numpy as np

class ResultPrinter(object):
    def __init__(self, energies, j_values,sp_states,m_scheme_basis):
        self.energies = energies
        self.j_values = j_values
        self.sp_states = sp_states
        self.m_scheme_basis = m_scheme_basis
        assert len(self.energies) == len(self.j_values), "there must be an equal number of energies and j_values"
             
    def _generate_sp_state_output(self):
        output="Single particle states:\n"
        output+="Nr\tn\tl\tj\tm\n"
        for i,s in enumerate(self.sp_states):
            output+="{}\t{}\t{}\t{}\t{}\n".format(i+1,s.get_n(),s.get_l(),s.get_j(),s.get_m_j())
        return output

    def _generate_m_scheme_output(self):
        output="\n\nM-Scheme basis\n"
        output+="nr\t"
        A = len(self.m_scheme_basis[0])
        output+=''.join(["|p{}\t".format(i) for i in range(1,A+1)])+"\n"
        output+=''.join([("{}\t".format(i+1)+''.join(["|{}\t".format(p) for p in state])+"\n") for i,state in enumerate(self.m_scheme_basis)])
        return output
    
    def _generate_output(self):
        output="\n\nEnergies and J:\n"
        output+="Nr\tE\tJ_tot\n"
        for i in range(len(self.energies)):
            output+="{}\t{:>6}\t{:>6}\n".format(i+1,np.round(self.energies[i],3),np.round(self.j_values[i],3))
        return output
        
    def print_all_to_screen(self):
        print(self._generate_sp_state_output())
        print(self._generate_m_scheme_output())
        print(self._generate_output())

    def print_all_to_file(self,filename):
        outputfile = open(filename,"w")
        outputfile.write(self._generate_sp_state_output())
        outputfile.write(self._generate_m_scheme_output())
        outputfile.write(self._generate_output())
        outputfile.close()
