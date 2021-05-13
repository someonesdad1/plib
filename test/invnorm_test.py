from invnorm import inverse_normal_cdf, invnormal_as
from lwtest import run, assert_equal, raises
try:
    import scipy.stats
except ImportError:
    print("invnorm_test.py:  scipy not available")
    exit(0)
from frange import frange

def Test():
    '''Test at P values of 1/n to 1 in steps of 1/n.
    '''
    ppf, n, tol_ack, tol_as = scipy.stats.norm.ppf, 1000, 1.15e-9, 3e-3
    n = 1000
    for p in frange(1/n, 1, 1/n):
        exact = ppf(p)
        # Acklam's algorithm
        approx = inverse_normal_cdf(p)
        if p != 0.5:
            rel_error = abs((approx - exact)/exact)
            assert(rel_error < tol_ack)
        else:
            assert(abs(approx - exact) < tol_ack)
        # Rational approximation in Abramowitz & Stegun
        approx = invnormal_as(p)
        assert(abs(approx - exact) < tol_as)
    raises(ValueError, inverse_normal_cdf, 0)
    raises(ValueError, inverse_normal_cdf, 1)

if __name__ == "__main__":
    exit(run(globals())[0])
