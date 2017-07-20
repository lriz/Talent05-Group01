import numpy as np
import os

class ResultPrinter(object):
    def __init__(self, energies, j_values,sp_states,m_scheme_basis,nushellx_folder,num_of_particles,Z):
        self.energies = energies
        self.j_values = j_values
        self.sp_states = sp_states
        self.m_scheme_basis = m_scheme_basis
        self.nushellx_folder = nushellx_folder
        self.num_of_particles = num_of_particles
        self.Z = Z
        self.degeneracy_index = []
        assert len(self.energies) == len(self.j_values), "there must be an equal number of energies and j_values"

    def _generate_intro(self):
        output="Welcome!\n"
        output+="".join(('Run for O-',str(self.Z+self.num_of_particles),'\n\n'))
        return output

    def _generate_sp_state_output(self):
        output="Single particle states:\n"
        output+="{:>3} || {:>2} || {:>2} || {:>2} || {:>2} || {:>3}\n".format("i", "p", "N", "L", "2J", "2M_J")
        output+="".join((" ","-"*34,'\n'))
        for sps in self.sp_states:
            output+="{:>3} || {:>2} || {:>2} || {:>2} || {:>2} || {:>3}\n".format(sps.index, sps.p, sps.n, sps.l, sps.j, sps.m_j)
        return output

    def _generate_m_scheme_output(self):
        output="\n\nM-Scheme basis\n"
        output+="nr\t"
        A = len(self.m_scheme_basis[0])
        output+=''.join(["|p{}\t".format(i) for i in range(1,A+1)])+"\n"
        output+=''.join([("{}\t".format(i+1)+''.join(["|{}\t".format(p) for p in state])+"\n") for i,state in enumerate(self.m_scheme_basis)])
        return output
    
    def _generate_output(self):
        output=''
        nushellx_file = list(open("".join((self.nushellx_folder,"/o_",str(self.num_of_particles+self.Z),"b.lpt"))))[6:]  # open file as a list and take out the first 6 rows.
        nushellx_energies = [line.split()[2] for line in nushellx_file]  # extract energies from the lines.
        if len(nushellx_energies) != len(self.energies):
           output+='Number of energies in program does no match NushellX!'
        output="\n\nEnergies and J:\n"
        output+="Nr\t||\tE\t||\tJ_tot\t||\tE(NushellX)\n"
        output+="".join(("-"*60,'\n'))
        for i,e_nush in zip(range(len(self.energies)),nushellx_energies):
            output+="{:<3}\t||  {:>7}\t||{:>7}\t||\t{:>7}\n".format(i+1,np.round(self.energies[i],3), "-", e_nush)#np.round(self.j_values[i],3))
            if abs(self.energies[i] - float(e_nush)) > 0.01:
                self.degeneracy_index.append(i+1)
        return output
    def _generate_degeneracy(self):
        output='Differences from NushellX\n'
        output+="".join(["{}, ".format(index) for index in  self.degeneracy_index[:-1]])
        if self.degeneracy_index:
            output+='{}'.format(str(self.degeneracy_index[-1]))
        return output

    def print_all_to_screen(self):
        print(self._generate_sp_state_output())
        print(self._generate_m_scheme_output())
        print(self._generate_output())

    def print_all_to_file(self,filename):
        outputfile = open(filename,"w")
        outputfile.write(self._generate_intro())
        outputfile.write(self._generate_sp_state_output())
        outputfile.write(self._generate_m_scheme_output())
        outputfile.write(self._generate_output())
        outputfile.write(self._generate_degeneracy())
        outputfile.close()
