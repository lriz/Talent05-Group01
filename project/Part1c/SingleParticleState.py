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

    def __eq__(self, other):
        return self.index == other.index

    def get_p(self): return self.p
    def get_n(self): return self.n
    def get_l(self): return self.l
    def get_j(self): return self.j
    def get_m_j(self): return self.m_j
    def get_index(self): return self.index
