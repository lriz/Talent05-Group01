import matplotlib.pyplot as plt
from weisskopf_units import weisskopf_units

def main():
    """
    A program that plots B(E2)'s between different init. and fin. states of the Oxygen-18-26 isotopes as a function
    of nucleon (neutron) number A (N)
    """
    twop_zerop_theo = [3.263,4.117,3.968,1.666,2.190]  # Single-particle units.
    twop_zerop_exp = [3.32,1.80,1.2]
    error_exp = [0.09,0.07,0.5]
    A = [18,20,22,24,26]
    twop_zerop_theo_weis = [x/weisskopf_units(2,a) for x,a in zip(twop_zerop_theo,A)]  # Weisskopf units.
    error_exp_weis = [x/weisskopf_units(2,a) for x,a in zip(error_exp,A[:3])]  # Weisskopf units.
    plt.plot(A,twop_zerop_theo_weis,'o-',color='blue',label='USDB')
    plt.plot(A[:3],twop_zerop_exp,'o-',color='orange',label='Exp.')
    plt.errorbar(A[:3],twop_zerop_exp,yerr=error_exp_weis,color='orange',capsize=5)
    #plt.title('Oxygen isotopes')
    plt.xlabel('$A$',fontsize=20)
    plt.ylabel('$B(E2;2_1^+ \\rightarrow 0_1^+)$(W.u.)',fontsize=20)
    plt.legend(fontsize=20)
    plt.tick_params(labelsize=18)
    plt.savefig('../../figures/oxygen-be2.pdf',format='pdf',bbox_inches='tight')

if __name__=='__main__':
    main()