import math

def weisskopf_units(l,A):
    """
    The Weisskopf single-particle units for B(E,Lambda).
    :param l: multipolarity (e.g. E1, l=1, E2: l=2...).
    :param A: Mass number.
    :return: the Weisskopf single-particle B(E,Lambda).
    """
    return (1./(4*math.pi)) * (3./(l+3))**2 * (1.2)**(2*l) * A**((float(2*l)/3))