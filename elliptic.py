'''
Complete elliptic functions
    From Robert Weaver's website:
        http://electronbunker.sasktelwebsite.net/CalcMethods2c.html

    Bob commented in an email that it's more efficient to calculate
    these functions using the arithmetic-geometric mean as used in the
    Nagaoka function in calculating the inductance of coils.  He sent me
    his javascript implementations of those, so I've included them too
    (they are used by default).  Change use_series to True to use the
    series calculation method.

    The series algorithm comes from
    http://electronbunker.sasktelwebsite.net/DL/KelvinEllipticCalcs.pdf.
    These are included here to allow checks of the faster algorithms.

    Update May 2022:  the above URLs are defunct.

    28 Oct 2022:  The formula from
    http://paulbourke.net/geometry/ellipsecirc/python.code is a
    quadratically-converging algorithm for the circumference of an ellipse
    and is fast.  I made it the basis of the default EllipticE function.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2010, 2014 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞# # <math> Complete elliptic functions #∞what∞#
        #∞test∞# run #∞test∞#
        pass
    if 1:   # Standard imports
        import math
    if 1:   # Custom imports
        from color import t
        from lwtest import Assert
    if 1:   # Global variables
        t.dbg = t("ornl")
        # Set to true to see colorized debug output
        debug = False
        use_series = False
if use_series:
    def EllipticK(k, eps=1e-15):
        '''Calculate the complete elliptic integral of the first kind with
        modulus k.  Uses series expansion; based on Dwight's formulas 773.2
        & 773.3.  Translated from Basic code by Robert Weaver, 2009-10-26.
        '''
        kp2 = 1-k*k
        kp = math.sqrt(kp2)     # complementary modulus
        count, value = 1, 0
        if k <= 0.91:
            # if k <= .91 use formula 773.2
            m = (1 - kp)/(1 + kp)
            m2 = m*m
            term = 1.0      # the zeroth term is 1.0
            sum = term
            for n in range(2, 101, 2):
                # calc nth coefficient
                termi = ((n - 1)/(n))**2*m2
                term = term*termi
                sum = sum + term
                if term/sum < eps:
                    break
                count += 1
            value = math.pi*sum/2*(m + 1)
        else:
            # if k > .91 use formula 773.3
            term = math.log(4/kp)
            coeff = 1.0
            sum = term
            for n in range(2, 101, 2):
                coeff = coeff*((n - 1)/n)**2*kp2
                termi = 2/((n - 1)*n)
                term = term-termi
                sum = sum+coeff*term
                if (coeff*term/sum) < eps:
                    break
                count += 1
            value = sum
        if debug:
            print("EllipticK(%.6f) =" % k, value, "in", count, "steps")
        return value
    def EllipticE(k, eps=1e-15):
        '''Calculate the complete elliptic integral of the second kind with
        modulus k.  Uses series expansion.  Based on H. B. Dwight's formulae
        774.2 & 774.3.  Adapted from Basic code by Robert Weaver, 2009-10-26
        '''
        kp2 = 1 - k*k
        kp = math.sqrt(kp2)     # complementary modulus
        m, count = (1 - kp)/(1 + kp), 1
        if k == 1:
            # This prevents a divide by zero problem
            value = 1
        elif k < 0.93:
            # formula 774.2
            term = 1.0      # the zeroth term is 1.0
            sum = term
            coeff = 1.0     # the zeroth coefficient is 1
            for n in range(2, 101, 2):
                termi = m*(n - 3)/n
                term = term*termi*termi
                sum = sum + term
                if term/sum < eps:
                    break
                count += 1
            value = math.pi*sum/(2*m + 2)
        else:
            # formula 774.3
            tio = 0
            cio = 1
            coeff = 1
            term = math.log(4/kp)
            sum = 1
            for n in range(2, 101, 2):
                cin = (n - 1)/n
                coeff = coeff*cio*cin*kp2
                cio = cin
                tin = 1/((n - 1)*n)
                term = term - tio - tin
                tio = tin
                sum = sum + term*coeff
                if term*coeff/sum < eps:
                    break
                count += 1
            value = sum
        if debug:
            print("EllipticE(%.6f) =" % k, sum, "in", count, "steps")
        return value
else:
    def EllipticK(k):
        '''Returns the complete elliptic integral of the 1st kind for
        modulus k.
        The integral is \int_0^{\pi/2} 1/\sqrt(1 - m*\sin^2 t) dt
        '''
        Assert(0 <= k <= 1)
        m, a = k*k, 1
        b = math.sqrt(1 - m)
        c, co = a - b, 2*(a - b)
        while c < co:
            co = c
            c = (a - b)/2
            ao = (a + b)/2
            b = math.sqrt(a*b)
            a = ao
        return math.pi/(a + a)
    def EllipticE(k, weaver=True):
        '''Returns the complete elliptic integral of the 2nd kind for
        modulus k.  If weaver is True, use Bob Weaver's implementation.
        Otherwise the fast algorithm in EllipseCircumference is used.

        The integral is \int_0^{\pi/2} \sqrt(1 - k*\sin^2 t) dt
        '''
        Assert(0 <= k <= 1)
        if k == 1:
            return 1
        if weaver:
            kk, c, a, ci, co = k*k, 1, 1, 1, 2
            b = math.sqrt(1 - kk)
            E = 1 - kk/2
            while c < co:
                co = c
                c = (a - b)/2
                E = E - ci*c*c
                ao = (a + b)/2
                b = math.sqrt(a*b)
                ci *= 2
                a = ao
            return E*math.pi/(a + a)
        else:
            raise ValueError("oops")
def EllipseCircumference(A, B, debug=False):
    '''Calculate the circumference of an ellipse with major diameter A and
    minor diameter B.  Relative accuracy is about 0.5^53 (about 1e-16).
    Downloaded Mon 26 May 2014 from
    http://paulbourke.net/geometry/ellipsecirc/python.code; also see the
    page http://paulbourke.net/geometry/ellipsecirc/.  This series
    converges quadratically and was first proposed by J. Ivory in 1798 (see
    https://en.wikipedia.org/wiki/James_Ivory_(mathematician)).

    The formula for the circumference of an ellipse is 2*a*E(e) where a is
    the major semidiameter, e is the eccentricity, and E is the complete
    elliptic integral of the second kind.  Thus, this function can also be
    used to calculate E.

    A quick check showed that Ivory's formula iterates about half as
    much as Weaver's EllipticE.  Since they agree in the tests to
    floating point precision, this method is preferred.
    '''
    if A < 0 or B < 0:
        raise ValueError("A and B must be >= 0")
    # Note the original formula is in terms of the 'semi-axes';
    # hence the division by 2.
    a, b = A/2, B/2
    x, y = max(a, b), min(a, b)
    digits = 53
    tol = math.sqrt(math.pow(0.5, digits))
    if digits*y < tol*x:
        return 4*x
    s, m = 0, 1
    while x - y > tol*y:
        x, y = 0.5*(x + y), math.sqrt(x*y)
        m *= 2
        s += m*math.pow(x - y, 2)
        if debug:
            val = math.pi*(math.pow(a + b, 2) - s)/(x + y)
            t.print(f"{t.dbg}EllipseCircumference({A}, {B}, {val}")
    return math.pi*(math.pow(a + b, 2) - s)/(x + y)

if __name__ == "__main__": 
    '''
    Testing strategy: There are three basic methods used to validate the
    complete elliptic integrals of the first and second kinds:
            * Compare to elliptic functions from pycephes
            * Compare to elliptic functions from scipy
            * Compare to elliptic functions from mpmath
    '''
    from lwtest import run, assert_equal, raises
    from pdb import set_trace as xx
    try:
        from scipy.special import ellipk as spellipk, ellipe as spellipe
        have_scipy = True
    except Exception:
        have_scipy = False
    try:
        from mpmath import ellipk as mpellipk, ellipe as mpellipe
        have_mpmath = True
    except Exception:
        have_mpmath = False
    pi = math.pi
    def TestUsingPycephes():
        # Routines from pycephes (python translation of Moshier's elliptic
        # functions).
        MACHEP = 1.11022302462515654042E-16           # 2**(-53)
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
        C1 = 1.3862943611198906188E0    # log(4)
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
            Assert(max_diff < 1e-15)
        EllipticTest(EllipticK, ellpk)
        EllipticTest(EllipticK, ellpk)
        EllipticTest(EllipticE, ellpe, use_series_imp=False)
        EllipticTest(EllipticE, ellpe, use_series_imp=True)
    def TestUsingScipyMpmath():
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
            Assert(max_diff < 1e-15)
        if have_scipy:
            t.print(f"{t.dbg}Testing using scipy in elliptic.py")
            EllipticTest(EllipticK, spellipk, use_series_imp=False)
            EllipticTest(EllipticK, spellipk, use_series_imp=True)
            EllipticTest(EllipticE, spellipe, use_series_imp=False)
            EllipticTest(EllipticE, spellipe, use_series_imp=True)
        else:
            t.print(f"{t.dbg}Not tested using scipy in elliptic.py")
        if have_mpmath:
            t.print(f"{t.dbg}Testing using mpmath in elliptic.py")
            EllipticTest(EllipticK, mpellipk, use_series_imp=False)
            EllipticTest(EllipticK, mpellipk, use_series_imp=True)
            EllipticTest(EllipticE, mpellipe, use_series_imp=False)
            EllipticTest(EllipticE, mpellipe, use_series_imp=True)
        else:
            t.print(f"{t.dbg}Not tested using mpmath in elliptic.py")
    def TestUsingBourke():
        # Compare using EllipseCircumference to Weaver's
        def E(a, b):
            return EllipseCircumference(a, b)/(2*a)
        a = 1
        for i in range(1, 101):
            b = i/100
            i_bourke = E(a, b)
            ecc = math.sqrt(1 - (b/a)**2)
            i_weaver = EllipticE(ecc)
            Assert(abs((i_bourke - i_weaver)/i_weaver) < 1e-15)
    exit(run(globals())[0])
