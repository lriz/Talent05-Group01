import numpy as np

class ResultPrinter(object):
    def __init__(self, energies, j_values):
        self.energies = energies
        self.j_values = j_values
        assert len(self.energies) == len(self.j_values), "there must be an equal number of energies and j_values"
             
        
    def _generate_output(self):
        output="Nr\tE\tJ_tot\n"
        for i in range(len(self.energies)):
            output+="{}\t{:>6}\t{:>6}\n".format(i+1,np.round(self.energies[i],3),np.round(self.j_values[i],3))
        return output
        
    def print_to_screen(self):
        print(self._generate_output())

    def print_to_file(self,filename):
        outputfile = open(filename,"w")
        outputfile.write(self._generate_output())
        outputfile.close()
