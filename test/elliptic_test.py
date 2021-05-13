import math
from elliptic import EllipticK, EllipticE, EllipseCircumference, use_series
from lwtest import run, assert_equal, raises
from pdb import set_trace as xx

have_scipy = False
try:
    from scipy.special import ellipk, ellipe
    have_scipy = True
except Exception:
    pass
pi = math.pi
#======================================================================
# Routines from pycephes (python translation of Moshier's elliptic
# functions).
MACHEP   = 1.11022302462515654042E-16           # 2**(-53)
P = (1.37982864606273237150E-4, 2.28025724005875567385E-3,
     7.97404013220415179367E-3, 9.85821379021226008714E-3,
     6.87489687449949877925E-3, 6.18901033637687613229E-3,
     8.79078273952743772254E-3, 1.49380448916805252718E-2,
     3.08851465246711995998E-2, 9.65735902811690126535E-2,
     1.38629436111989062502E0)
Q = (2.94078955048598507511E-5, 9.14184723865917226571E-4,
     5.94058303753167793257E-3, 1.54850516649762399335E-2,
     2.39089602715924892727E-2, 3.01204715227604046988E-2,
     3.73774314173823228969E-2, 4.88280347570998239232E-2,
     7.03124996963957469739E-2, 1.24999999999870820058E-1,
     4.99999999999999999821E-1)
C1 = 1.3862943611198906188E0 # log(4)
Pe = (1.53552577301013293365E-4, 2.50888492163602060990E-3,
      8.68786816565889628429E-3, 1.07350949056076193403E-2,
      7.77395492516787092951E-3, 7.58395289413514708519E-3,
      1.15688436810574127319E-2, 2.18317996015557253103E-2,
      5.68051945617860553470E-2, 4.43147180560990850618E-1,
      1.00000000000000000299E0)
Qe = (3.27954898576485872656E-5, 1.00962792679356715133E-3,
      6.50609489976927491433E-3, 1.68862163993311317300E-2,
      2.61769742454493659583E-2, 3.34833904888224918614E-2,
      4.27180926518931511717E-2, 5.85936634471101055642E-2,
      9.37499997197644278445E-2, 2.49999999999888314361E-1)
def polevl(x, coef):
    '''polevl(x, coef)
    Evaluates the polynomial 
                            2          N
        y  =  C  + C x + C x  +...+ C x
               0    1     2          N
    The coefficients are stored in reverse order as coef[0] = C , 
                                                               N
    coef[1] = C   , etc.
               N-1
    '''
    x = float(x)
    ans = float(coef[0])
    i = len(coef) - 1
    index = 1
    while i:
        ans = ans*x + coef[index]
        index += 1
        i -= 1
    return ans
def p1evl(x, coef):
    '''p1evl(x, coef)
                                              N
    Same as polevl except the coefficient of C  is 1.0 and thus
    omitted from the array coef.
    '''
    x = float(x)
    ans = x + coef[0]
    i = len(coef) - 1
    index = 1
    while i:
        ans = ans*x + coef[index]
        index += 1
        i -= 1
    return ans
def ellpe(x):
    '''ellpe(x)
    Complete elliptic integral of the first kind.
    '''
    x = 1.0 - x  # Was added in the ellpe.c file that was used by scipy.
                 # This lets the function return values that agree
                 # with Abramowitz & Stegun.
    if (x <= 0.0) or (x > 1.0):
        if x == 0.0:
            return 1.0
        raise Exception("Domain error")
    return polevl(x, Pe) - math.log(x)*(x*polevl(x, Qe))
def ellpk(x):
    '''ellpk(x)
    Complete elliptic integral of the second kind.
    '''
    x = 1.0 - x  # Was added in the ellpe.c file that was used by scipy.
                 # This lets the function return values that agree
                 # with Abramowitz & Stegun.
    if (x < 0.0) or (x > 1.0):
        raise Exception("Domain error")
    if x > MACHEP:
        return polevl(x, P) - math.log(x)*polevl(x, Q)
    else:
        if x == 0.0:
            raise Exception("Singularity")
        else:
            return C1 - 0.5*math.log(x)
def TestUsingScipy():
    def EllipticTest(weaver, scipys, use_series_imp=False):
        # Check Weaver's function against SciPy's
        use_series = use_series_imp
        max_diff = 0
        for deg in range(0, 81, 1):
            k = math.sin(deg*math.pi/180)
            w, sp = weaver(k), scipys(k**2)
            try:
                diff = abs(w - sp)/sp
            except DivisionByZeroError:
                continue
            else:
                max_diff = max(max_diff, diff)
        assert max_diff < 1e-15
    if have_scipy:
        EllipticTest(EllipticK, ellipk, use_series_imp=False)
        EllipticTest(EllipticK, ellipk, use_series_imp=True)
        EllipticTest(EllipticE, ellipe, use_series_imp=False)
        EllipticTest(EllipticE, ellipe, use_series_imp=True)
def TestUsingPycephes():
    def EllipticTest(weaver, pycephes, use_series_imp=False):
        # Check Weaver's function against pycephes
        max_diff = 0
        for deg in range(0, 81, 1):
            k = math.sin(deg*math.pi/180)
            w, sp = weaver(k), pycephes(k**2)
            try:
                diff = abs(w - sp)/sp
            except DivisionByZeroError:
                continue
            else:
                max_diff = max(max_diff, diff)
        assert max_diff < 1e-15
    EllipticTest(EllipticK, ellpk)
    EllipticTest(EllipticK, ellpk)
    EllipticTest(EllipticE, ellpe, use_series_imp=False)
    EllipticTest(EllipticE, ellpe, use_series_imp=True)
    # Compare Paul Bourke's python implementation to Weaver's
    E = lambda a, b:  EllipseCircumference(a, b)/(2*a)
    a = 1
    for i in range(101):
        b = i/100
        i_bourke = E(a, b)
        ecc = math.sqrt(1 - (b/a)**2)
        i_weaver = EllipticE(ecc)
        assert(abs((i_bourke - i_weaver)/i_weaver) < 1e-15)
def Test():
    TestUsingPycephes()
    TestUsingScipy()

if __name__ == "__main__":
    exit(run(globals())[0])
