import tools as tls
import numpy as np

from cycling import Cycling

import matplotlib.pyplot as plt

def test_interpolation_00():
    x = np.arange(3.,7.)
    y = np.array([2.,1.,1.,2.])

    space = tls.get_bernsetin_order_two()#[tls.bernstein_polynomial(2,i) for i in range(3)]
    space_prime = tls.get_bernsetin_derivs_orde_two()

    coeffs = tls.least_squares(x,y,space)


    f = tls.get_function(coeffs,space)
    df = tls.get_function(coeffs,space_prime)

    x0 = .3
    sample = np.linspace(0,1)
    taylor = f(x0) + df(x0) * (sample-x0)


    plt.plot(np.linspace(np.amin(x),
             np.amax(x)),f(sample))
    plt.plot(np.linspace(
             np.amin(x),np.amax(x)),
             taylor,'-g')
    plt.plot(x,y,'or')
    plt.show()

def test_interpolation_01():
    x = np.array([ 1., 2., 4., 7., 9., 11.])
    normalize = tls.normalize_function(x)
    y = np.array([ 4.38,8.98, 18.46, 33.23, 43.89, 54.7 ])
    y_prime = np.array([4.255, 4.535, 4.936, 5.076 ,5.095, 5.104])

    space = tls.get_bernsetin_order_two()#[tls.bernstein_polynomial(2,i) for i in range(3)]
    space_prime = tls.get_bernsetin_derivs_order_two()

    coeffs = tls.least_squares(x,y,space)
    print(coeffs)

    f = tls.get_function(coeffs,space)
    df = tls.get_function(coeffs,space_prime)


    print("df(.0) = ",df(.5))
    print(" f(.0) = ", f(.5))

    x0 = normalize(np.amin(x))
    sample = np.linspace(0,1)
    taylor = f(x0) + df(x0) * (sample-x0)
    #print(df(x0))

    x0 = np.linspace(0,1,10)

    w = np.amax(x)-np.amin(x)

    plt.plot(x0 * w + np.amin(x),f(x0),"b")
    plt.plot(x0 * w + np.amin(x),df(x0)/w,"r")
    plt.plot(x,y,'ob')
    plt.plot(x,y_prime,'or')
    plt.show()

def test_iterator():
    av = Cycling()
    av.read_data('7C9A5608.FIT')
    f = av.interpolate_and_derive_data()
    print(f[:6])
    print(av.data["timestamp"][:6])
    print(av.data["distance"][:6])
    print(av.data["speed"][:6])



if __name__ == "__main__":
    test_interpolation_01()
    #test_iterator()
