from SingleParticleState import SingleParticleState
from collections import OrderedDict
from itertools import combinations
import numpy as np

class SPSGenerator(object):
    """

    """
    def __init__(self):
        super(SPSGenerator,self).__init__()
        self.m_scheme_basis = []
        self.m_broken_basis = []
        self.sps_list = []
        self.shell_list = []


    def calc_sps_list(self, shell_configurations_list, orbits_dict):
        sps_index = 1
        shell_index = 1
        for p_level_index in orbits_dict.keys():
            level_name = orbits_dict[p_level_index]["name"]
            N_number = [shell['N'] for shell in  shell_configurations_list  if shell['name'] == level_name][-1] #TODO: check that not empty.
            j_total = orbits_dict[p_level_index]["2J-total"]
            self.shell_list.append(SingleParticleState(p_level_index,
                                                       N_number,
                                                       orbits_dict[p_level_index]["angular momentum"],
                                                       j_total,
                                                       0,
                                                       shell_index))
            shell_index += 1
            for m_j in range(-j_total, j_total+1, 2):
                self.sps_list.append(SingleParticleState(p_level_index,
                                                         N_number,
                                                         orbits_dict[p_level_index]["angular momentum"],
                                                         j_total,
                                                         m_j,
                                                         sps_index))
                sps_index += 1

    def calc_m_broken_basis(self,sps_list, n):
        """
        Calculate all Slater determinants from a single particle basis.
        :param sps_list: a list of all the single particle states.
        :param n: number of particles to couple together.
        :return: a numpy array of all slater determinants with all possible M-values.
        """
        self.m_broken_basis=[]
        for l in combinations(sps_list, n):
            self.m_broken_basis.append(list(l))
        return np.array(self.m_broken_basis)

    def calc_m_scheme_basis(self, m_broken_basis, M_total, orbits_dict, orbits_separation):
        if orbits_separation:
            self.calc_m_scheme_basis_orbit_separation(m_broken_basis, orbits_dict, M_total)
        else:
            self.calc_m_scheme_basis_no_orbit_separation(m_broken_basis, M_total)

    def calc_m_scheme_basis_orbit_separation(self, m_broken_basis, orbits_dict, M_total):
        for sps in m_broken_basis:
            sps_temp_dict = OrderedDict()
            for p in orbits_dict:
                sps_p_list = []
                for i in sps:
                    if i.get_p() == p:
                        sps_p_list.append(i)
                sps_temp_dict[p] = sps_p_list
            sps_temp_dict = OrderedDict((k, v) for k, v in sps_temp_dict.iteritems() if v)
            m_bool = True
            for p, value in sps_temp_dict.iteritems():
                if sum([v.get_m_j() for v in value]) in M_total:
                    continue
                else:
                    m_bool = False
            if m_bool:
                self.m_scheme_basis.append(sps)

    def calc_m_scheme_basis_no_orbit_separation(self, m_broken_basis, M_total):
        for sps in m_broken_basis:
            if sum([i.get_m_j() for i in sps]) in M_total:
                self.m_scheme_basis.append(sps)

    def get_m_broken_basis(self):
        return self.m_broken_basis

    def get_sps_list(self):
        return self.sps_list

    def get_shell_list(self):
        return self.shell_list
    
    def get_m_scheme_basis(self):
        return np.array(self.m_scheme_basis)

    def set_sps_list(self, sps_list):
        self.sps_list = sps_list

    def print_sps(self):
        print
        print "{:>3} || {:>2} || {:>2} || {:>2} || {:>2} || {:>3}".format("i", "p", "N", "L", "2J", "2M_J")
        print "".join((" ","-"*34))
        for sps in self.sps_list:
            print "{:>3} || {:>2} || {:>2} || {:>2} || {:>2} || {:>3}".format(sps.index, sps.p, sps.n, sps.l, sps.j, sps.m_j)

    def print_m_scheme_basis(self):
        print
        print '#'*100
        print "M-scheme Basis"
        #m_total_list = [(self.input_dict["2M-total"], self.input_dict["shell-orbit P-levels"][p]["name"]) for p in self.input_dict["shell-orbit P-levels"]]
        m_total_list = []
        for p in self.input_dict["shell-orbit P-levels"]:
            m_total_list.append(self.input_dict["2M-total"])
            m_total_list.append("".join(("(",self.input_dict["shell-orbit P-levels"][p]["name"],")")))
        print "".join(("sps with 2M-total = ","{} "*len(m_total_list))).format(*m_total_list)
        print 'Basis length:', len(self.m_scheme_basis)
        print self.m_scheme_basis
        print '#'*100
	

