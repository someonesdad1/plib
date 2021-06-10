'''
Inverse normal CDF approximation (relative error about 1e-9)
'''

import math

def inverse_normal_cdf(p):
    '''Compute the inverse CDF for the normal distribution.  Retrieved 28
    Feb 2012 from
    http://home.online.no/~pjacklam/notes/invnorm/impl/field/ltqnorm.txt.
    This link was provided by the algorithm's developer:
    http://home.online.no/~pjacklam/notes/invnorm/.
 
    DP:  I've made minor changes to formatting, etc.
 
    ---------------------------------------------------------------------------
    The original docstring follows:
 
    Modified from the author's original perl code (original comments follow
    below) by dfield@yahoo-inc.com.  May 3, 2004.
 
    Lower tail quantile for standard normal distribution function.
 
    This function returns an approximation of the inverse cumulative
    standard normal distribution function.  I.e., given P, it returns
    an approximation to the X satisfying P = Pr{Z <= X} where Z is a
    random variable from the standard normal distribution.
 
    The algorithm uses a minimax approximation by rational functions
    and the result has a relative error whose absolute value is less
    than 1.15e-9.
 
    Author:      Peter John Acklam
    Time-stamp:  2000-07-19 18:26:14
    E-mail:      pjacklam@online.no
    WWW URL:     http://home.online.no/~pjacklam
    '''
    if not (0 < p < 1):
        raise ValueError("Argument to inverse_normal_cdf must be in open "
                         "interval (0,1)")
    # Coefficients in rational approximations.
    a = (-3.969683028665376e+01, 2.209460984245205e+02,
         -2.759285104469687e+02, 1.383577518672690e+02,
         -3.066479806614716e+01, 2.506628277459239e+00)
    b = (-5.447609879822406e+01, 1.615858368580409e+02,
         -1.556989798598866e+02, 6.680131188771972e+01,
         -1.328068155288572e+01)
    c = (-7.784894002430293e-03, -3.223964580411365e-01,
         -2.400758277161838e+00, -2.549732539343734e+00,
         4.374664141464968e+00, 2.938163982698783e+00)
    d = (7.784695709041462e-03, 3.224671290700398e-01,
         2.445134137142996e+00, 3.754408661907416e+00)
    # Define break-points
    plow = 0.02425
    phigh = 1 - plow
    # Rational approximation for lower region:
    if p < plow:
        q = math.sqrt(-2*math.log(p))
        return ((((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) /
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1))
    # Rational approximation for upper region:
    if phigh < p:
        q = math.sqrt(-2*math.log(1-p))
        return -((((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) /
                ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1))
    # Rational approximation for central region:
    q = p - 0.5
    r = q*q
    return ((((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q /
           (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1))
def invnormal_as(p):
    '''26.2.22 from Abramowitz and Stegun; absolute error is < 3e-3.
    '''
    if not (0 < p < 1):
        raise ValueError("p must be in (0, 1)")
    if p > 0.5:
        sign = 1
        p = 1 - p
    else:
        sign = -1
    t = math.sqrt(math.log(1/p**2))
    return sign*(t - (2.30753 + 0.27061*t)/(1 + 0.99229*t + 0.04481*t**2))
if __name__ == "__main__": 
    from lwtest import run, assert_equal, raises, Assert
    try:
        import scipy.stats
        have_scipy = True
    except ImportError:
        have_scipy = False
        print("invnorm_test.py:  Warning:  scipy not available")
    from frange import frange
    def Test_with_scipy():
        'Test at P values of 1/n to 1 in steps of 1/n'
        if not have_scipy:
            return
        ppf, tol_ack, tol_as = scipy.stats.norm.ppf, 1.15e-9, 3e-3
        n = 100
        for p in frange(1/n, 1, 1/n):
            exact = ppf(p)
            # Acklam's algorithm
            approx = inverse_normal_cdf(p)
            if p != 0.5:
                rel_error = abs((approx - exact)/exact)
                Assert(rel_error < tol_ack)
            else:
                Assert(abs(approx - exact) < tol_ack)
            # Rational approximation in Abramowitz & Stegun
            approx = invnormal_as(p)
            Assert(abs(approx - exact) < tol_as)
        raises(ValueError, inverse_normal_cdf, 0)
        raises(ValueError, inverse_normal_cdf, 1)
    def Test_without_scipy():
        '''I used scipy from my winpython36 installation to generate
        100 test points.
        '''
        if have_scipy:
            return
        tol_ack = 1.15e-9
        data = '''
            0.01 -2.3263478740408408
            0.02 -2.053748910631823
            0.03 -1.880793608151251
            0.04 -1.75068607125217
            0.05 -1.6448536269514729
            0.06 -1.5547735945968535
            0.07 -1.4757910281791706
            0.08 -1.4050715603096329
            0.09 -1.3407550336902165
            0.1 -1.2815515655446004
            0.11 -1.2265281200366098
            0.12 -1.1749867920660904
            0.13 -1.1263911290388007
            0.14 -1.0803193408149558
            0.15 -1.0364333894937898
            0.16 -0.994457883209753
            0.17 -0.9541652531461943
            0.18 -0.915365087842814
            0.19 -0.8778962950512288
            0.2 -0.8416212335729142
            0.21 -0.8064212470182404
            0.22 -0.7721932141886848
            0.23 -0.7388468491852137
            0.24 -0.7063025628400874
            0.25 -0.6744897501960817
            0.26 -0.643345405392917
            0.27 -0.6128129910166272
            0.28 -0.5828415072712162
            0.29 -0.5533847195556729
            0.3 -0.5244005127080409
            0.31 -0.4958503473474533
            0.32 -0.46769879911450823
            0.33 -0.4399131656732338
            0.34 -0.41246312944140473
            0.35 -0.38532046640756773
            0.36 -0.3584587932511938
            0.37 -0.33185334643681663
            0.38 -0.3054807880993974
            0.39 -0.27931903444745415
            0.4 -0.2533471031357997
            0.41 -0.22754497664114948
            0.42 -0.20189347914185088
            0.43 -0.17637416478086135
            0.44 -0.15096921549677725
            0.45 -0.12566134685507402
            0.46 -0.10043372051146975
            0.47 -0.0752698620998299
            0.48 -0.05015358346473367
            0.49 -0.02506890825871106
            0.5 0.0
            0.51 0.02506890825871106
            0.52 0.05015358346473367
            0.53 0.0752698620998299
            0.54 0.10043372051146988
            0.55 0.12566134685507416
            0.56 0.1509692154967774
            0.57 0.1763741647808612
            0.58 0.20189347914185074
            0.59 0.22754497664114934
            0.6 0.2533471031357997
            0.61 0.27931903444745415
            0.62 0.3054807880993974
            0.63 0.33185334643681663
            0.64 0.3584587932511938
            0.65 0.38532046640756773
            0.66 0.41246312944140495
            0.67 0.4399131656732339
            0.68 0.4676987991145084
            0.69 0.4958503473474532
            0.7 0.5244005127080407
            0.71 0.5533847195556727
            0.72 0.5828415072712162
            0.73 0.6128129910166272
            0.74 0.643345405392917
            0.75 0.6744897501960817
            0.76 0.7063025628400874
            0.77 0.7388468491852137
            0.78 0.7721932141886848
            0.79 0.8064212470182404
            0.8 0.8416212335729143
            0.81 0.8778962950512289
            0.82 0.9153650878428138
            0.83 0.9541652531461943
            0.84 0.994457883209753
            0.85 1.0364333894937898
            0.86 1.0803193408149558
            0.87 1.1263911290388007
            0.88 1.1749867920660904
            0.89 1.2265281200366105
            0.9 1.2815515655446004
            0.91 1.3407550336902165
            0.92 1.4050715603096329
            0.93 1.475791028179171
            0.94 1.5547735945968535
            0.95 1.6448536269514722
            0.96 1.7506860712521692
            0.97 1.8807936081512509
            0.98 2.0537489106318225
            0.99 2.3263478740408408
        '''[1:-1]
        for line in data.split("\n"):
            if not line.strip():
                continue
            p, exact = [float(i) for i in line.split()]
            approx = inverse_normal_cdf(p)
            if p != 0.5:
                rel_error = abs((approx - exact)/exact)
                Assert(rel_error < tol_ack)
            else:
                Assert(abs(approx - exact) < tol_ack)
    exit(run(globals(), halt=1)[0])
