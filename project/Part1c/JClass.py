

class JClass(object):
    """
    Class which calculates the different J^2 elements - Jz^2, J+ and J-
    """
    def __init__(self, n, j_type):
        """
        :param n: number of valance nucleons.
        :param j_type: the type of J we wish to calculate - Jz ('z'), J+ ('+') or J- ('-').
        """
        self.j_type = j_type

    def get_matrix_element(self,p,q,s,r):
        """
        Get the appropriate matrix element.
        :param p:
        :param q:
        :param s:
        :param r:
        :return:
        """
        if q == s:
            print 'q=s'
            print 'p','2J', p.get_j(), '2Mj',p.get_m_j(), 'r', '2J', r.get_j(), '2Mj', r.get_m_j()
            if (p.get_j() == r.get_j()) and (p.get_m_j()+2 == r.get_m_j() or p.get_m_j()-2 == r.get_m_j()):
                print 'get q=s'
                return self.alpha_j(p.get_j(), r.get_m_j())
            else:
                return 0
        elif p == r:
            print 'p=r'
            print 'q','2J', q.get_j(), '2Mj',q.get_m_j(), 's', '2J', s.get_j(), '2Mj', s.get_m_j()
            if (q.get_j() == s.get_j()) and (q.get_m_j()+2 == s.get_m_j() or q.get_m_j()-2 == s.get_m_j()):
                print 'get p=r'
                return self.alpha_j(q.get_j(), s.get_m_j())
            else:
                return 0
        elif p == s:
            print 'p=s'
            print 'q','J', q.get_j(), 'Mj',q.get_m_j(), 'r', '2J', r.get_j(), '2Mj', r.get_m_j(), 'sum', q.get_m_j()+2 +r.get_m_j()
            if (q.get_j() == r.get_j()) and ((q.get_m_j()+2 == r.get_m_j()) or (q.get_m_j()-2 == r.get_m_j())):
                print 'get p=s'
                return -1*self.alpha_j(q.get_j(), r.get_m_j())  # the minus one comes from a phase.
            else:
                return 0
        elif q == r:
            print 'q=r'
            print 'p','J', p.get_j(), 'Mj',p.get_m_j(), 'r', '2J', s.get_j(), '2Mj', s.get_m_j()
            if (p.get_j() == s.get_j()) and (p.get_m_j()+2 == s.get_m_j() or p.get_m_j()-2 == s.get_m_j()):
                print 'get q=r'
                return -1*self.alpha_j(p.get_j(), s.get_m_j()) # the minus one comes from a phase.
            else:
                return 0
        else:
            return 0

    def alpha_j(self,j,m_j):
        print 'alpha_j'
        """
        Calculates the J, J- coefficients.
        We divide by (n-1) since we calculate matrix elements for a two-body force:
                sum_{kjmx} alpha_J/(n-1) a+_{kjm+-1}a+_{x}a_{x}a_{kjm}.
        The sum_{x}a+_{x}a_{x} part is the number operator. We thus annihilate with a_{kjm} a state, count the number of
        states, which is n-1, and act again a+_{kjm+-1}. This is exactly like taking
                sum_{kjm} alpha_J a+_{kjm+-1}a_{kjm}.
        :param j: the chosen j.
        :param m_j: the chosen m_j.
        :return:
        """
        if self.j_type == '+':
            print 'mult',0.25*(j-m_j)*(j+m_j+2)/(self.n-1)
            return pow(0.25*(j-m_j)*(j+m_j+2)/(self.n-1),0.5)
        elif self.j_type == '-':
            return pow(0.25*(j+m_j)*(j-m_j+2)/(self.n-1), 0.5)
