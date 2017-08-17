import matplotlib.pyplot as plt
import numpy as np
#from weisskopf_units import weisskopf_units

def main():
    """
    A program that plots E(2+)-E(0+) of the Oxygen-18-26 isotopes as a function
    of nucleon (neutron) number A (N)
    """
    A = [18,20,22,24,26]
    twop_usda = np.array([-9.764,-21.701,-31.285,-36.222,-38.989])
    zerop_usda = np.array([-11.787,-23.510,-34.479,-41.394,-40.893])
    twop_zerop_usda = twop_usda - zerop_usda
    #twop_zerop_usda_weis = [x/weisskopf_units(2,a) for x,a in zip(twop_zerop_usda,A)]  # Weisskopf units.
    twop_usdb = np.array([-9.933,-21.886,-31.340,-36.182,-38.758])
    zerop_usdb = np.array([-11.932,-23.632,-34.498,-41.225,-40.869])
    twop_zerop_usdb = twop_usdb - zerop_usdb
    #twop_zerop_usdb_weis = [x/weisskopf_units(2,a) for x,a in zip(twop_zerop_usdb,A)]  # Weisskopf units.
    twop_ccei = np.array([-9.273,-19.899,-28.036,-30.807,-31.752])
    zerop_ccei = np.array([-10.549,-20.955,-30.655,-36.506,-33.164])
    twop_zerop_ccei = twop_ccei - zerop_ccei 
    #twop_zerop_ccei_weis = [x/weisskopf_units(2,a) for x,a in zip(twop_zerop_ccei,A)]  # Weisskopf units.
    twop_zerop_exp = [1.982,1.674,3.199,4.790,1.277]
    #error_exp = [0.09,0.07,0.5]

    plt.plot(A,twop_zerop_usda,'o-',color='red',label='USDA')
    plt.plot(A,twop_zerop_usdb,'o-',color='blue',label='USDB')
    plt.plot(A,twop_zerop_ccei,'o-',color='orange',label='CCEI')
    plt.plot(A,twop_zerop_exp,'o-',color='black',label='Exp.')
    #plt.errorbar(A[:3],twop_zerop_exp,yerr=error_exp,color='black',capsize=5)
    #plt.title('Oxygen isotopes')
    plt.xlabel('$A$',fontsize=20)
    plt.ylabel('$E(2_1^+)-E(0_1^+)$(MeV)',fontsize=20)
    plt.legend(fontsize=20)
    plt.tick_params(labelsize=18)
    plt.savefig('2+_over_0+.pdf',format='pdf',bbox_inches='tight')

if __name__=='__main__':
    main()