import numpy as np
import os
from ShellOutput import shell_output
from LatexTableGenerator import LatexTableGenerator

class ResultPrinter(object):
    def __init__(self, energies,
                 j_values,
                 sp_states,
                 m_scheme_basis,
                 nushellx_folder,
                 num_of_particles,
                 Z,
                 occupation_nums):
        self.energies = energies
        self.j_values = j_values
        self.sp_states = sp_states
        self.m_scheme_basis = m_scheme_basis
        self.nushellx_folder = nushellx_folder
        self.num_of_particles = num_of_particles
        self.Z = Z
        self.degeneracy_index = []
        self.occupation_nums = occupation_nums
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

    def _generate_sp_state_latex(self):
        output="\\begin{table}[ht!]\n"
        # TODO: Add caption later

        output+="\\begin{tabular}{r||r||r||r||r||r}\n"
        output+="$i$ & $p$ & $n$ & $l$ & $2l$ & $2 m_j$ "
        hline_="\\hline"
        for sps in self.sp_states:
            output+="\\\\\n{} {} & {} & {} & {} & {} & {} ".format(hline_,sps.index, sps.p, sps.n, sps.l, sps.j, sps.m_j)
            hline_=""
        output+="\n"
        output+="\\end{tabular}\n"
        output+="\\end{table}"
        return output
        
    def _generate_m_scheme_output(self):
        output="\n\nM-Scheme basis:\n"
        output+="nr\t"
        A = len(self.m_scheme_basis[0])
        output+=''.join(["|p{}\t".format(i) for i in range(1,A+1)])+"\n"
        output+=''.join([("{}\t".format(i+1)+''.join(["|{}\t".format(p) for p in state])+"\n") for i,state in enumerate(self.m_scheme_basis)])
        return output

    def _generate_occupation_num_output(self):
        shell_list=[]
        def comp_shell(a,b):
            return a.get_n() == b.get_n() and a.get_l() == b.get_l() and a.get_j() == b.get_j()
        for current in self.sp_states:
            if not any([comp_shell(current,sh) for sh in shell_list]):
                shell_list.append(current)
        output="\n\nOccupation Numbers:\n"
        output+="state:  {} || tot:\n".format("".join(["|| {}:  ".format(shell_output(shell)) for shell in shell_list]))
        for i,occs in enumerate(self.occupation_nums):
            output+="{:<5}   {} || {}\n".format(i+1,"".join(["|| {:>9}  ".format(np.round(ocn,2)) for ocn in occs]),np.sum(occs))
        return output

    def _generate_occupation_num_latex(self):
        shell_list=[]
        def comp_shell(a,b):
            return a.get_n() == b.get_n() and a.get_l() == b.get_l() and a.get_j() == b.get_j()
        for current in self.sp_states:
            if not any([comp_shell(current,sh) for sh in shell_list]):
                shell_list.append(current)
        shell_list = sorted(shell_list, key = lambda s:s.get_n())
        #latex_generator = LatexTableGenerator(30)
        output="\\begin{table}[ht!]\n"
        output+="\\caption{Occupation numbers for the computed states}\n"
        output+="\\begin{tabular}{|c|"+("".join(["c|" for shell in shell_list])+"c|}")
        output+="\\hline state: {} & tot:\\\\\n".format("".join(["& {}:  ".format(shell_output(shell)) for shell in shell_list]))
        output+="\\hline "
        endl = "\\\\"
        for i,occs in enumerate(self.occupation_nums):
            #if i == len(self.occupation_nums)-1:
             #   endl = ""
            output+="{:<5}   {} & {} {}\n".format(i+1,"".join(["& {:>9}  ".format(np.round(ocn,2)) for ocn in occs]),np.sum(occs),endl)
        output+="\\hline\n"
        output+="\\end{tabular}\n"
        output+="\\end{table}\n"
        return output
    
    def _generate_output(self):
        output=''
        nushellx_file = list(open("".join((self.nushellx_folder,"/o_",str(self.num_of_particles+self.Z),"b.lpt"))))[6:]  # open file as a list and take out the first 6 rows.
        nushellx_energies = [line.split()[2] for line in nushellx_file]  # extract energies from the lines.
        new_nushellx_energies = []
        for j,e in enumerate(self.energies):
            bool = False
            value = '-'
            for i,e_nu in enumerate(nushellx_energies):
                if abs(e - float(e_nu)) <= 0.01:
                    value = e_nu
                    break
            new_nushellx_energies.append(value)

        output="\n\nEnergies and J:\n"
        output+="Nr\t||\tE\t||\tJ_tot\t||\tE(NushellX)\n"
        output+="".join(("-"*60,'\n'))
        for i,e_nush in zip(range(len(self.energies)),new_nushellx_energies):
            output+="{:<3}\t||  {:>7}\t||{:>7}\t||\t{:>7}\n".format(i+1,np.round(self.energies[i],3), np.round(self.j_values[i],3), e_nush)#np.round(self.j_values[i],3))
        return output

    def _generate_energies_latex(self):
        latex_table = LatexTableGenerator(30)
        nushellx_file = list(open("".join((self.nushellx_folder,"/o_",str(self.num_of_particles+self.Z),"b.lpt"))))[6:]  # open file as a list and take out the first 6 rows.
        nushellx_energies = [line.split()[2] for line in nushellx_file]  # extract energies from the lines.
        nushellx_j = [line.split()[4] for line in nushellx_file] # extract j from lines.
        new_nushellx_energies = []
        new_nushellx_j = []
        for j,e in enumerate(self.energies):
            bool = False
            value = '-'
            value_j = '-'
            for i,e_nu in enumerate(nushellx_energies):
                if abs(e - float(e_nu)) <= 0.01:
                    value = e_nu
                    value_j = nushellx_j[i]
                    break
            new_nushellx_energies.append(value)
            new_nushellx_j.append(value_j)
        latex_table.add_entry("Nr","Nr")
        latex_table.add_entry("E","\\(E\\)")
        latex_table.add_entry("J","\\(J_{L}\\)")
        latex_table.add_entry("Enu","\\(E_{\\rm{NuShellX}}\\)")
        latex_table.add_entry("Jnu","\\(J_{N}\\)")
        for i,e_nush in zip(range(len(self.energies)),new_nushellx_energies):
            latex_table.add_to_entry("Nr","{:<3}".format(i+1))
            latex_table.add_to_entry("E","{:>7}".format(np.round(self.energies[i],3)))
            j = np.round(self.j_values[i],3)
            if float(int(j))==j:
                latex_table.add_to_entry("J","{:>7}".format(int(j)))
            else:
                latex_table.add_to_entry("J","{:>7}/2".format(int(2*j)))
            latex_table.add_to_entry("Enu",e_nush)
            latex_table.add_to_entry("Jnu",new_nushellx_j[i])
        latex_table.update_grid()
        return latex_table.get_latex()
        
    def print_all_to_screen(self):
        print(self._generate_sp_state_latex())
        print(self._generate_m_scheme_output())
        print(self._generate_output())
        print(self._generate_occupation_num_output())

    def print_all_to_file(self,filename):
        outputfile = open(filename,"w")
        outputfile.write(self._generate_sp_state_output())
        outputfile.write(self._generate_m_scheme_output())
        outputfile.write(self._generate_energies_latex())
        outputfile.write(self._generate_occupation_num_latex())
        outputfile.close()
