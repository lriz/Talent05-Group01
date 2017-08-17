
import numpy as np
from TwoBodyOperator import TwoBodyOperator
from hamiltonian_unperturbed import hamiltonian_unperturbed,hamiltonian_unperturbed_pairing
from JSquaredOperator import JSquaredOperator
from OccupationNumber import occupation

class NucleusManager(object):
    def __init__(self,
                 sps_object,
                 sps_list,
                 potential):
        self.sps_object = sps_object
        self.sps_list = sps_list
        self.potential = potential
        self.num_particles = 0
        self.m = 0
        self.m_scheme_basis=None
        self.energies = None
        self.eigenstates = None
        self.total_j = None
        self.occupation_nums = None
        
    def set_num_particles(self,n):
        self.num_particles = n
        self.sps_object.calc_m_broken_basis(self.sps_list,n)
        self.m_scheme_basis=self.sps_object.get_m_broken_basis()

    def set_total_m(self,m,orbit_separation=None,orbit_dict=None):
        self.m = m
        if orbit_separation == None or orbit_dict == None:
            self.sps_object.calc_m_scheme_basis_no_orbit_separation(self.m_scheme_basis,m)
        else:
            self.sps_object.calc_m_scheme_basis(self.m_scheme_basis,m,
                                                orbit_dict,
                                                orbit_separation)
        self.m_scheme_basis = self.sps_object.get_m_scheme_basis()
        
    def compute_eigen_spectrum(self,pairing_case=False):
        self.m_scheme_basis = np.array(self.m_scheme_basis)
        hamil_operator = TwoBodyOperator(self.sps_list,
                                         self.m_scheme_basis,
                                         self.potential)
        hamil_operator.compute_matrix()
        if pairing_case:
            H0 = hamiltonian_unperturbed_pairing(self.m_scheme_basis)
        else:
            H0 = hamiltonian_unperturbed(self.m_scheme_basis,
                                         self.potential.get_sp_energies())
        HI = hamil_operator.get_matrix()

        factor = (18.0/(16.0+self.num_particles))**0.3
        if (pairing_case):
            factor = 1
        H=H0+factor*HI
        self.energies, self.eigenstates = np.linalg.eigh(H)
        energyzip=[]
        for i,e in enumerate(self.energies):
            energyzip.append((e,self.eigenstates[:,i]))
        energyzip = sorted(energyzip,key=lambda k:k[0])
        en,ev = zip(*energyzip)
        self.energies = np.array(list(en))
        self.eigenstates = np.array(list(ev))

    def compute_j_squared(self):
        jsquared_potential = JSquaredOperator()
        jsquared_operator = TwoBodyOperator(self.sps_list,
                                            self.m_scheme_basis,
                                            jsquared_potential)
        jsquared_operator.compute_matrix()
        jsquared_matrix = jsquared_operator.get_matrix()
        jsquared_matrix-=jsquared_potential.get_single_body_contribution(self.m_scheme_basis)*(self.num_particles-2)
        self.total_j=[]
        js = {}
        for es in self.eigenstates:
            jj = np.dot(es,np.dot(jsquared_matrix,es))
            j = 0.5*(np.sqrt(4*jj+1)-1)
            if int(2*j+0.5) in js:
                js[int(2*j+0.5)]+=1
            else:
                js[int(2*j+0.5)]=1
            self.total_j.append(0.5*(np.sqrt(4*jj+1)-1))
        total = 0
        for key in js:
            print("{} : {}".format(float(key)/2.0,js[key]))
            total+=js[key]
        print("total = {}".format(total))
        self.total_j = np.array(self.total_j)

    def compute_occupation_numbers(self):
        shell_list =[]
        def comp_shell(a,b):
            return a.get_n() == b.get_n() and a.get_l() == b.get_l() and a.get_j() == b.get_j()
        for current in self.sps_list:
            if not any([comp_shell(current,sh) for sh in shell_list]):
                shell_list.append(current)
        shell_list = sorted(shell_list, key = lambda s:s.get_n())
        self.occupation_nums = []
        for es in self.eigenstates:
            occs=[]
            for shell in shell_list:
                occs.append(occupation(shell,es,self.m_scheme_basis))
            self.occupation_nums.append(occs)


    def get_energies(self):
        return self.energies

    def get_eigenstates(self):
        return self.eigenstates

    def get_total_j(self):
        return self.total_j

    def get_occupation_nums(self):
        return self.occupation_nums

    def get_m_scheme_basis(self):
        return self.m_scheme_basis

    def get_num_particles(self):
        return self.num_particles
    def get_m(self):
        return self.m
