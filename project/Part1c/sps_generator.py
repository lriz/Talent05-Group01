from single_particle_state_class import single_particle_state
from collections import OrderedDict
import numpy as np

class sps_generator(object):
    """

    """
    def __init__(self, input_dict):
        self.input_dict = input_dict
        self.m_scheme_basis = []
        self.m_broken_basis = []
        self.sps_list = []

    def calc_m_broken_basis(self, shell_configurations_list):
        sps_index = 1
        for p_level_index in self.input_dict["shell-orbit P-levels"].keys():
            level_name = self.input_dict["shell-orbit P-levels"][p_level_index]["name"]
            N_number = [shell['N'] for shell in  shell_configurations_list  if shell['name'] == level_name][-1] #TODO: check that not empty.
            j_total = self.input_dict["shell-orbit P-levels"][p_level_index]["2J-total"]
            for m_j in range(-j_total, j_total+1, 2):
                self.sps_list.append(single_particle_state(p_level_index,
                                                             N_number,
                                                             self.input_dict["shell-orbit P-levels"][p_level_index]["angular momentum"],
                                                             j_total,
                                                             m_j,
                                                             sps_index))
                sps_index += 1

        self.m_broken_basis = np.array([list(x) for x in self.choose_iter(self.sps_list, self.input_dict["number of particles"])])

    def get_m_broken_basis(self):
        return self.m_broken_basis

    def get_sps_list(self):
        return self.sps_list

    def choose_iter(self, elements, length):
        """
        Generate all possible elements from a list given a wanted length. e.g. number of states and number of particles.
        :param elements: the number of states.
        :param length: the number of particles.
        :return:
        """
        for i in xrange(len(elements)):
            if length == 1:
                yield (elements[i],)
            else:
                for next in self.choose_iter(elements[i+1:len(elements)], length-1):
                    yield (elements[i],) + next
    def choose(self, l, k):
        return list(self.choose_iter(l, k))

    #TODO: change for class inheretence.
    def calc_m_scheme_basis(self, m_broken_basis):
        if self.input_dict["use input file"]:
            self.calc_m_scheme_basis_orbit_separation(m_broken_basis)
        else:
            self.calc_m_scheme_basis_no_orbit_separation(m_broken_basis)

    def calc_m_scheme_basis_orbit_separation(self, m_broken_basis):
        for sps in m_broken_basis:
            sps_temp_dict = OrderedDict()
            for p in self.input_dict["shell-orbit P-levels"]:
                sps_p_list = []
                for i in sps:
                    if i.get_p() == p:
                        sps_p_list.append(i)
                sps_temp_dict[p] = sps_p_list
            sps_temp_dict = OrderedDict((k, v) for k, v in sps_temp_dict.iteritems() if v)
            m_bool = True
            for p, value in sps_temp_dict.iteritems():
                if sum([v.get_m_j() for v in value]) in self.input_dict["shell-orbit P-levels"][p]["2M-total"]:
                    continue
                else:
                    m_bool = False
            if m_bool:
                self.m_scheme_basis.append(sps)

    def calc_m_scheme_basis_no_orbit_separation(self, m_broken_basis):
        for sps in m_broken_basis:
            if sum([i.get_m_j() for i in sps]) in self.input_dict["2M-total"]:
                self.m_scheme_basis.append(sps)

    def get_m_scheme_basis(self):
        return self.m_scheme_basis

    def print_sps(self):
        print
        print "{:>3} || {:>2} || {:>2} || {:>2} || {:>2} || {:>3}".format("i", "p", "N", "L", "2J", "2M_J")
        print "".join((" ","-"*34))
        for sps in self.sps_list:
            print "{:>3} || {:>2} || {:>2} || {:>2} || {:>2} || {:>3}".format(sps.index, sps.p, sps.n, sps.l, sps.j, sps.m_j)

    def print_m_scheme_basis(self):
        print
        #m_total_list = [(self.input_dict["2M-total"], self.input_dict["shell-orbit P-levels"][p]["name"]) for p in self.input_dict["shell-orbit P-levels"]]
        m_total_list = []
        for p in self.input_dict["shell-orbit P-levels"]:
            m_total_list.append(self.input_dict["2M-total"])
            m_total_list.append("".join(("(",self.input_dict["shell-orbit P-levels"][p]["name"],")")))
        print "".join(("sps with 2M-total = ","{} "*len(m_total_list))).format(*m_total_list)
        print 'Basis length:', len(self.m_scheme_basis)
        print self.m_scheme_basis

