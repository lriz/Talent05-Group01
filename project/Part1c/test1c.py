import numpy as np
from decimal import Decimal

#PROJECT Part (1c) First implementation (a bit by hand):

Nparticles=4 #TODO: generalize for input.
Npairs=Nparticles/2

NspLevels=8 # Includes spin
NLevels=8/2 # TODO: NspLevels/Npairs

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
    print 'eneter potencia'
    """Calcula y devuelve el conjunto potencia del
       conjunto c.
    """
    print 'c',c
    if len(c) == 0:
        return [[]]
    r = potencia(c[:-1])
    print 'return',r + [s + [c[-1]] for s in r]
    return r + [s + [c[-1]] for s in r]

def imprime_ordenado(c):
    print 'imprime_ordenado'
    print 'c',c
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

imprime_ordenado(combinaciones([1, 2, 3, 4], 2))


def format_for_function_example(a,b,c):
    """
    function description.
    Args:
        a: description.
        b: description.
        c: description.

    Returns:
        description.
    """
    pass




