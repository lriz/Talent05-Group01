

class JClass(object):
    """
    Class which calculates the different J^2 elements - Jz^2, J+ and J-
    """
    def __init__(self, n, jj_choice):
        """
        :param n: number of valance nucleons.
        :param jj_choice: the type of J we wish to calculate - JzJz ('zz'), J+J- ('+-') or J-J+ ('-+').
        """
        self.jj_choice = jj_choice
        self.n = n

    def get_matrix_element(self,p,q,s,r):
        """
        Get the appropriate matrix element.
        :param p:
        :param q:
        :param s:
        :param r:
        :return:
        """
        if self.jj_choice == '+-':
            return self.Jplus_Jminus_element(p,q,s,r)
        elif self.jj_choice == '-+':
            return self.Jminus_Jplus_element(p,q,s,r)
        elif self.jj_choice == 'zz':
            return self.j_z_j_z_element(p,q,s,r)

    def j_z_j_z_element(self,p,q,s,r):
        if q == s and p == r:
            return pow(s.get_m_j()+r.get_m_j(), 2)
        elif p == s and q == r:
            return -pow(s.get_m_j()+r.get_m_j(), 2)
        else:
            return 0

    def Jminus_Jplus_element(self,p,q,s,r):
        matrix_element_1 = 0
        matrix_element_2 = 0
        # Part 1:
        # Check if Mj(r)-1 exists.
        if r.get_m_j()+2 > r.get_j():  # The new Mj(r)-1 does NOT exists.
            matrix_element_1 += 0
        else:  # The new Mj(r)+1 exists.
            # Add the |s r> according to phase (+1 for <p q|q p> and -1 for <p q| p q>).
            if q == s and p == r:  # +1 phase.
                matrix_element_1 += self.alpha_j(r.get_j(), r.get_m_j()+2, '-')
            elif q == r and p == s:  # -1 phase.
                matrix_element_1 += -self.alpha_j(r.get_j(), r.get_m_j()+2, '-')
            # Check if Mj(s)-1 exists and if so add it to the matrix element.
            if s.get_m_j()-2 < -s.get_j(): # The new Mj(s)-1 does NOT exists.
                matrix_element_1 += 0
            else:  # the new Mj(s)-1 exists.
                if s.equate(q, -1) and r.equate(p, +1):  # +1 phase
                    matrix_element_1 += self.alpha_j(s.get_j(), s.get_m_j(), '-')
                elif s.equate(p, -1) and r.equate(q, +1):  # -1 phase
                    matrix_element_1 += -self.alpha_j(s.get_j(), s.get_m_j(), '-')
        matrix_element_1 = matrix_element_1*self.alpha_j(r.get_j(), r.get_m_j(), '+')
        # End of Part 1.

        # Part 2:
        if s.get_m_j()+2 > s.get_j():  # The new Mj(s)-1 does NOT exists.
            matrix_element_2 += 0
        else:  # The new Mj(s)-1 exists.
            # Add the |s r> according to phase (+1 for <p q|q p> and -1 for <p q| p q>).
            if q == s and p == r:  # +1 phase.
                matrix_element_2 += self.alpha_j(s.get_j(), s.get_m_j()+2, '-')
            elif q == r and p == s:  # -1 phase.
                matrix_element_2 += -self.alpha_j(s.get_j(), s.get_m_j()+2, '-')
            # Check if Mj(r)+1 exists and if so add it to the matrix element.
            if r.get_m_j()-2 < -r.get_j(): # The new Mj(r)+1 does NOT exists.
                matrix_element_2 += 0
            else:  # the new Mj(r)+1 exists.
                if s.equate(q, +1) and r.equate(p, -1):  # +1 phase
                    matrix_element_2 += self.alpha_j(r.get_j(), r.get_m_j(), '-')
                elif s.equate(p, +1) and r.equate(q, -1):  # -1 phase
                    matrix_element_2 += -self.alpha_j(r.get_j(), r.get_m_j(), '-')
        matrix_element_2 = matrix_element_2*self.alpha_j(s.get_j(), s.get_m_j(), '+')
        # End of Part 2.
        print 'Jminus_Jplus_element'
        print matrix_element_1+matrix_element_2
        return matrix_element_1+matrix_element_2

    def Jplus_Jminus_element(self,p,q,s,r):
        print 'test'
        matrix_element_1 = 0
        matrix_element_2 = 0
        # Part 1:
        # Check if Mj(r)-1 exists.
        if r.get_m_j()-2 < -r.get_j():  # The new Mj(r)-1 does NOT exists.
            print '1'
            matrix_element_1 += 0
        else:  # The new Mj(r)-1 exists.
            print '2'
            # Add the |s r> according to phase (+1 for <p q|q p> and -1 for <p q| p q>).
            if q == s and p == r:  # +1 phase.
                print '3'
                matrix_element_1 += self.alpha_j(r.get_j(), r.get_m_j()-2, '+')
            elif q == r and p == s:  # -1 phase.
                print '4'
                matrix_element_1 += -self.alpha_j(r.get_j(), r.get_m_j()-2, '+')
            # Check if Mj(s)+1 exists and if so add it to the matrix element.
            if s.get_m_j()+2 > s.get_j(): # The new Mj(s)+1 does NOT exists.
                print '5'
                matrix_element_1 += 0
            else:  # the new Mj(s)+1 exists.
                print '6'
                if s.equate(q, +1) and r.equate(p, -1):  # +1 phase
                    print '7'
                    matrix_element_1 += self.alpha_j(s.get_j(), s.get_m_j(), '+')
                elif s.equate(p, +1) and r.equate(q, -1):  # -1 phase
                    print '8'
                    matrix_element_1 += -self.alpha_j(s.get_j(), s.get_m_j(), '+')
        matrix_element_1 = matrix_element_1*self.alpha_j(r.get_j(), r.get_m_j(), '-')
        # End of Part 1.

        # Part 2:
        if s.get_m_j()-2 < -s.get_j():  # The new Mj(s)-1 does NOT exists.
            print '9'
            matrix_element_2 += 0
        else:  # The new Mj(s)-1 exists.
            print '10'
            # Add the |s r> according to phase (+1 for <p q|q p> and -1 for <p q| p q>).
            if q == s and p == r:  # +1 phase.
                print '11'
                matrix_element_2 += self.alpha_j(s.get_j(), s.get_m_j()-2, '+')
            elif q == r and p == s:  # -1 phase.
                print '12'
                matrix_element_2 += -self.alpha_j(s.get_j(), s.get_m_j()-2, '+')
            # Check if Mj(r)+1 exists and if so add it to the matrix element.
            if r.get_m_j()+2 > r.get_j(): # The new Mj(r)+1 does NOT exists.
                print '13'
                matrix_element_2 += 0
            else:  # the new Mj(r)+1 exists.
                print '14'
                if s.equate(q, -1) and r.equate(p, +1):  # +1 phase
                    print '15'
                    matrix_element_2 += self.alpha_j(r.get_j(), r.get_m_j(), '+')
                elif s.equate(p, -1) and r.equate(q, +1):  # -1 phase
                    print '16'
                    matrix_element_2 += -self.alpha_j(r.get_j(), r.get_m_j(), '+')
        matrix_element_2 = matrix_element_2*self.alpha_j(s.get_j(), s.get_m_j(), '-')
        # End of Part 2.
        print 'Jplus_Jminus_element'
        print matrix_element_1+matrix_element_2
        return matrix_element_1+matrix_element_2

    def alpha_j(self,j,m_j,j_type):
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
        if j_type == '+':
            return pow(0.25*(j-m_j)*(j+m_j+2)/(self.n-1), 0.5)
        elif j_type == '-':
            return pow(0.25*(j+m_j)*(j-m_j+2)/(self.n-1), 0.5)
