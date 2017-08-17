class SingleParticleState(object):
    """

    """
    def __init__(self, p, n, l, j, m_j, index):
        self.p = p
        self.n = n
        self.l = l
        self.j = j
        self.m_j = m_j
        self.index = index

    def __repr__(self):
        return str(self.index)

    

    def copy(self):
        return SingleParticleState(self.p,
                                   self.n,
                                   self.l,
                                   self.j,
                                   self.m_j,
                                   self.index)
    def get_p(self): return self.p
    def get_n(self): return self.n
    def get_l(self): return self.l
    def get_j(self): return self.j
    def get_m_j(self): return self.m_j
    def get_index(self): return self.index
    def equate(self, p, m):
        """
        Equate all the different quantum numbers between this sps and 'p', where 'm' is value to add to m_j when comparing.
        :param p: an sps object to compare with.
        :param m: a value to add to m_j when comparing.
        :return: bool.
        """
        return p.get_n() == self.get_n() and p.get_l() == self.get_l() and p.get_j() == self.get_j() and p.get_m_j() == self.get_m_j()+m
    def __eq__(self, other):
        return self.equate(other,0)
    
    def __neq__(self, other):
        return not self.__eq__(other)
