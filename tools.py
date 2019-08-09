import os
from fitparse import FitFile
import numpy as np

from scipy.special import binom as binomial

import scipy.sparse as spr

def non_negative(v):
    ids = np.where(v<0)
    v[ids] = 0
    return v


def forward_convolution(data,conv_amplitude,conv_function):
    assert data.ndim==1, "data should be one dimensional arrays"

    m = get_forward_convolution_matrix(data.shape[0],conv_amplitude,conv_function)

    return m.dot(data)


def get_forward_convolution_matrix(matrix_size,conv_amplitude,conv_function):

    m = spr.dia_matrix((matrix_size, matrix_size),dtype=np.float64)

    for i in range(conv_amplitude):

        data = conv_function(i)*np.ones((m.shape[0],),dtype=np.float64)

        d = spr.dia_matrix((data,i), shape=m.shape)

        m+=d

    return m

def bernstein_polynomial(n,i):
    assert i in range(n+1), 'i out of range: [0,n)'
    def func(n,i,t):
        poly = binomial(n,i)*t**(i)*(1.-t)**(n-i)
        return poly
    return lambda t : func(n,i,t)

def normalize_function(v):
    v_min = np.amin(v)
    v_max = np.amax(v)
    return lambda x : (x - v_min)/(v_max-v_min)

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

def get_bernsetin_order_one():
    return [lambda x : 1-x,
            lambda x : x]

def get_bernsetin_derivs_order_one():
    return [lambda x : -1.,
            lambda x : 1.]

def get_bernsetin_order_two():
    return [lambda x : (1-x)*(1-x),
            lambda x : 2*x*(1-x),
            lambda x : x*x]

def get_bernsetin_derivs_order_two():
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

def interpolate_and_get_derivative(x,y):
    space = get_bernsetin_order_one()
    space_prime = get_bernsetin_derivs_order_one()
    coeffs = least_squares(x,y,space)
    return get_function(coeffs,space_prime)

def linear_regression(x,y):
    space = get_bernsetin_order_one()
    coeffs = least_squares(x,y,space)
    slope = np.abs(coeffs[0]-coeffs[1])
    slope =  slope/(np.amax(x)-np.amin(x))
    return slope
