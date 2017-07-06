from numpy import *
from decimal import Decimal

#PROJECT 1c) First implementation (a bit by hand):

Nparticles=4
Npairs=Nparticles/2

NspLevels=8 #includes spin
NpairLevels=8/2

BreakingPairs=0  #0=no pair breaking   #1=yes   by pair we mean here s=0

def combinatorial(n,r):   #n>r
    f = math.factorial
    return f(n) / f(r) / f(n-r)


if BreakingPairs==0:
    Mtotal=0
    NSlaterDet=combinatorial(NpairLevels,Npairs)
else:
    NSlaterDet=combinatorial(NspLevels,Nparticles)



H=zeros(NSlaterDet)

g=1.0


# for i in range(0,NSlaterDet):
#     for j in range(0,NSlaterDet):
#         H[i][j]=-g

# tuple = ('a','b','c')
# list = ['a','b','c']
# dict = {'a':1, 'b': true, 'c': "name"}

#SD=[]
p=range(1,NpairLevels+1)


sd1=[1]*Npairs
SD=[sd1]

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

imprime_ordenado(combinaciones([1, 2, 3, 4], 2))







