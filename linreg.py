'''
Linear regression for y = m*x + b
'''

from f import flt

def LinearRegression(x, y):
    'Return (m, b, Rsquared) for a simple linear regression'
    if len(x) != len(y):
        raise ValueError("x and y are not same length")
    n = len(x)
    sx = sum(x)
    sxx = sum([i*i for i in x])
    sy = sum(y)
    syy = sum([i*i for i in y])
    sxy = sum([i*j for i, j in zip(x, y)])
    m = flt((n*sxy - sx*sy)/(n*sxx - sx**2))
    b = flt((sy - m*sx)/n)
    Rsquared = flt((n*sxy - sx*sy)**2/((n*sxx - sx**2)*(n*syy - sy**2)))
    return (m, b, Rsquared)

if __name__ == "__main__": 
    # Test case checked against HP-42s
    x = [1, 2, 3]
    y = [1, 2, 3.1]
    m, b, Rsq = LinearRegression(x, y)
    assert m == 1.0500000000000018
    assert b == -0.06666666666667058
    assert Rsq == 0.9992447129909383
