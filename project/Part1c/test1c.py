import numpy as np
import json
import argparse
from decimal import Decimal

# PROJECT Part (1c) First implementation (a bit by hand):
# To run, example:
# $ python test1c.py -f test_input.json

# Argparse: insert arguments to code using the command line.
parser = argparse.ArgumentParser(description='None')  # Generate a parser.
parser.add_argument('-f','--file',help='a json input file name for the program', type=str,required=True)  # Define a command line operation.
args = parser.parse_args()

folder_name = 'input_files/'  # Folder of input files.

with open("".join((folder_name,args.file))) as data_file:
        input_dict = json.load(data_file)  # A dictionary. Keys are the name of input, values are the value of input.


Nparticles=input_dict["number of particles"] #TODO: generalize for input.
Npairs=Nparticles/2

NspLevels=input_dict["number of single-particle states"] # Includes spin
NLevels=NspLevels/Npairs # TODO: NspLevels/Npairs

BreakingPairs=0  #0=no pair breaking   #1=yes   by pair we mean here s=0

def combinatorial(n,r):   #n>r
    f = np.math.factorial
    return f(n) / f(r) / f(n-r)


if BreakingPairs==0:
    Mtotal=0
    NSlaterDet=combinatorial(NLevels,Npairs)
else:
    NSlaterDet=combinatorial(NspLevels,Nparticles)

H=np.zeros(NSlaterDet)

g=1.0  # Interaction constant.  #TODO: generalize for input.


# for i in range(0,NSlaterDet):
#     for j in range(0,NSlaterDet):
#         H[i][j]=-g

# tuple = ('a','b','c')
# list = ['a','b','c']
# dict = {'a':1, 'b': true, 'c': "name"}

#SD=[]
p=range(1,NLevels+1) # List of levels.


sd1=[1]*Npairs  # General slater determinant.  #TODO: rename.
SD=[sd1]  #TODO: explain.

def potencia(c):
    """Calcula y devuelve el conjunto potencia del
       conjunto c.
    """
    if len(c) == 0:
        return [[]]
    r = potencia(c[:-1])
    return r + [s + [c[-1]] for s in r]

def imprime_ordenado(c):
    for e in sorted(c, key=lambda s: (len(s), s)):
        print(e)

#imprime_ordenado(potencia([1, 2, 3, 4]))

def combinaciones(c, n):
    """Calcula y devuelve una lista con todas las
       combinaciones posibles que se pueden hacer
       con los elementos contenidos en c tomando n
       elementos a la vez.
    """
    return [s for s in potencia(c) if len(s) == n]

# Aqui utilizamos una lista por comprension, 
# la cual se puede leer asi: para cada subconjunto s que pertenece al resultado 
# del conjunto potencia de c, conservar solo aquellos valores de s 
# en donde su cardinalidad sea igual a n. 

imprime_ordenado(combinaciones(range(1,NspLevels+1), 2))


def function_format_example(a,b,c):
    """
    Name of creator: Noam.
    Please change comments and functions names to english :)
    Function description.

    Args:
        a: description.
        b: description.
        c: description.

    Returns:
        Description.
    """
    pass




