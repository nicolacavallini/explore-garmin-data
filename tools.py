import os
from fitparse import FitFile
import numpy as np

from scipy.special import binom as binomial

def bernstein_polynomial(n,i):
    assert i in range(n+1), 'i out of range: [0,n)'
    def func(n,i,t):
        poly = binomial(n,i)*t**(i)*(1.-t)**(n-i)
        return poly
    return lambda t : func(n,i,t)

def normalize(v):
    v = v - np.amin(v)
    v = v/np.amax(v)
    return v

def least_squares(x,y,space):
    xn = normalize(x)
    A = np.zeros((0,xn.shape[0]))

    for f in space:
        A = np.vstack((A,f(xn)))

    b = np.reshape(y,(y.shape[0],1))
    b = A.dot(b)

    A = A.dot(A.T)

    coeffs = np.linalg.solve(A, b)
    return coeffs

def get_get_bernsetin_orede_two():
    return [lambda x : (1-x)*(1-x),
            lambda x : 2*x*(1-x),
            lambda x : x*x]

def get_get_bernsetin_derivs_orede_two():
    return [lambda x : -2*(1-x),
            lambda x : 2*(1-2*x),
            lambda x : 2*x]

def get_function(coeffs,space):
    def func(coeffs,space,sample):
        if type(sample) is np.ndarray:
            function = np.zeros(sample.shape)
        else:
             function = 0
        for f,c in zip(space,coeffs.flatten()):
            function += c*f(sample)
        return function
    return lambda x : func(coeffs,space,x)
