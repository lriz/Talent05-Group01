import matplotlib.pyplot as plt
from weisskopf_units import weisskopf_units

def main():
    """
    A program that plots B(E2)'s between different init. and fin. states of the Oxygen-18-26 isotopes as a function
    of nucleon (neutron) number A (N)
    """
    A = [18,20,22,24,26]
    twop_zerop_usda = [3.069,3.950,3.765,1.845,2.066]  # Single-particle units.
    twop_zerop_usda_weis = [x/weisskopf_units(2,a) for x,a in zip(twop_zerop_usda,A)]  # Weisskopf units.
    twop_zerop_usdb = [3.263,4.117,3.968,1.666,2.190]  # Single-particle units.
    twop_zerop_usdb_weis = [x/weisskopf_units(2,a) for x,a in zip(twop_zerop_usdb,A)]  # Weisskopf units.
    twop_zerop_ccei = [3.499,4.261,4.228,1.643,2.550]  # Single-particle units.
    twop_zerop_ccei_weis = [x/weisskopf_units(2,a) for x,a in zip(twop_zerop_ccei,A)]  # Weisskopf units.
    twop_zerop_exp = [3.32,1.80,1.2]  # W.u.
    error_exp = [0.09,0.07,0.5]

    plt.plot(A,twop_zerop_usda_weis,'o-',color='red',label='USDA')
    plt.plot(A,twop_zerop_usdb_weis,'o-',color='blue',label='USDB')
    plt.plot(A,twop_zerop_ccei_weis,'o-',color='orange',label='CCEI')
    plt.plot(A[:3],twop_zerop_exp,'o-',color='black',label='Exp.')
    plt.errorbar(A[:3],twop_zerop_exp,yerr=error_exp,color='black',capsize=5)
    #plt.title('Oxygen isotopes')
    plt.xlabel('$A$',fontsize=20)
    plt.ylabel('$B(E2;2_1^+ \\rightarrow 0_1^+)$(W.u.)',fontsize=20)
    plt.legend(fontsize=20)
    plt.tick_params(labelsize=18)
    plt.savefig('../../figures/oxygen-be2.pdf',format='pdf',bbox_inches='tight')

if __name__=='__main__':
    main()