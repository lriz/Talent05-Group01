import numpy as np
import matplotlib.pyplot as plt

class LevelPloter(object):
    def __init__(self, energies):
        self.energies = (energies-np.min(energies))

    def plotLevels(self):
        for e in self.energies:
            if (e>6):
                break
            plt.plot([0,2],[e,e])
        plt.ylim([-0.5,6])
        plt.yticks(np.arange(-0.5,6,0.5))
        plt.show()
