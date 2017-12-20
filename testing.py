import tools as tls
import numpy as np

import matplotlib.pyplot as plt

def test_interpolation():
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


    plt.plot(np.linspace(np.amin(x),np.amax(x)),f(sample))
    plt.plot(np.linspace(np.amin(x),np.amax(x)),taylor,'-g')
    plt.plot(x,y,'or')
    plt.show()


if __name__ == "__main__":
    test_interpolation()
