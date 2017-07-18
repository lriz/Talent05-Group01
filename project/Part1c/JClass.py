

class JClass(object):
    """
    Class which calculates the different J^2 elements - Jz^2, J+ and J-
    """
    def __init__(self, j_type):
        """
        :param j_type: the type of J we wish to calculate - Jz ('z'), J+ ('+') or J- ('-').
        """
        self.j_type = j_type

    def get_matrix_element(self):