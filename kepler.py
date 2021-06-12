'''
Functions to calculate a solution to Kepler's equation 
    Ref. Meeus "Astronomical Algorithms", pg 206.

    The equation is E = M + e*sin(E).  E is to be solved for given M and
    e.  M will be between 0 and 2*pi and e >= 0.

    The iterative methods include a third parameter precision, which is
    what two successive iterations must be less than for the function to
    return.

    The individual SolveKepler? functions return a tuple (E, n) where E
    is the eccentric anomaly and n is the number of iterations to get
    the answer.  The test examples demonstrate how much faster Newton's
    method is over plain iteration.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2002 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <math> Functions to calculate a solution to Kepler's equation from
    # Meeus "Astronomical Algorithms", pg 206.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    import math
if 1:   # Custom imports
    try:
        from root import RootFinder
        _have_rootfinder = True
    except ImportError:
        _have_rootfinder = False
if 1:   # Global variables
    all = ["Kepler"]
    allowed_iterations = 120
    d2r = math.pi/180
    twopi = 2*math.pi
    pio2 = math.pi/2
    signum = lambda x: 0 if not x else -1 if x < 0 else 1
def Kepler(m, e, abstol=1e-8, algorithm=3):
    '''Call one of the Kepler equation solving methods.  Return the
    value of E (eccentric anomaly) and the number of iterations
    required.
    '''
    def SolveKepler0(m, e, abstol=abstol):
        '''Use simple iteration to the indicated precision.
        '''
        E0, E, count = m/2, m, 0
        while abs(E - E0) > abstol/10 and count <= allowed_iterations:
            E0 = E
            count += 1
            E = m + e*math.sin(E0)
        if count > allowed_iterations:
            msg = "Too many iterations ({0}) in SolveKepler1"
            raise ValueError(msg.format(count))
        return (E, count)
    def SolveKepler1(m, e, abstol=abstol):
        '''Use Newton's method to solve for the root.
        '''
        E0, E, count = m/2, m, 0
        while abs(E - E0) > abstol and count <= allowed_iterations:
            E0 = E
            count += 1
            E = E0 + (m+e*math.sin(E0)-E0)/(1-e*math.cos(E0))
        if count > allowed_iterations:
            msg = "Too many iterations ({0}) in SolveKepler2"
            raise ValueError(msg.format(count))
        return (E, count)
    def SolveKepler2(m, e, abstol=abstol):
        '''SolveKepler3 uses Sinnott's binary search algorithm.  abstol is
        ignored.
        '''
        m, f = math.fmod(m, twopi), 1
        m = m + twopi if m < 0 else m
        if m > math.pi:
            m, f = twopi - m, -1
        e0, d = pio2, pio2/2
        for i in range(1, 54, 1):
            m1 = e0 - e*math.sin(e0)
            e0 = e0 + d*signum(m - m1)
            d = d/2
        return (e0*f, 54)
    def SolveKepler3(m, e, abstol=abstol):
        '''Translated from C code at
        http://www.projectpluto.com/kepler.htm.  "Meeus" refers to
        "Astronomical Algorithms" by J. Meeus.  I've modified the routine
        slightly for e < 0.3 because it was not converging to the desired
        precision.  It also required adding checks for too many iterations.
        '''
        neg, count, thresh = False, 0, abstol*math.fabs(1 - e)
        if not m:
            return (0, 0)
        if e < 0.3:     # Low-eccentricity formula from Meeus, p. 195
            curr = math.atan2(math.sin(m), math.cos(m) - e)
            err = curr - e*math.sin(curr) - m
            while math.fabs(err) > thresh:
                curr -= err/(1 - e*math.cos(curr))
                err = curr - e*math.sin(curr) - m
                if count > allowed_iterations:
                    msg = ("Too many iterations ({0}) in SolveKepler3 "
                           "for e < 0.3 case")
                    raise ValueError(msg.format(count))
                count += 1
            return (curr, count)
        if m < 0:
            m = -m
            neg = True
        curr = m
        if e > 0.8 and m < math.pi/3 or e > 1:  # Up to 60 degrees
            trial = m/math.fabs(1 - e)
            if trial**2 > 6*math.fabs(1 - e):   # Cubic term is dominant
                if m < math.pi:
                    trial = (6*m)**(1/3)
                else:  # Hyperbolic w/ 5th & higher-order terms predominant
                    trial = asinh(m/e)
            curr = trial
        if e < 1:
            err = curr - e*math.sin(curr) - m
            while math.fabs(err) > thresh:
                curr -= err/(1 - e*math.cos(curr))
                err = curr - e*math.sin(curr) - m
                if count > allowed_iterations:
                    msg = ("Too many iterations ({0}) in SolveKepler3 "
                           "for e < 1 case")
                    raise ValueError(msg.format(count))
                count += 1
        else:
            err = e*math.sinh(curr) - curr - m
            while math.fabs(err) > thresh:
                curr -= err/(e*math.cosh(curr) - 1)
                err = e*math.sinh(curr) - curr - m
                if count > allowed_iterations:
                    msg = ("Too many iterations ({0}) in SolveKepler3 "
                           "for e >= 1 case")
                    raise ValueError(msg.format(count))
                count += 1
        curr = -curr if neg else curr
        return (curr, count)
    def SolveKepler4(m, e, abstol=abstol):
        '''Use RootFinder, which is Jack Crenshaw's enhancements to 
        an older IBM FORTRAN routine that uses inverse parabolic
        interpolation.
        '''
        f = lambda E: m + e*math.sin(E) - E
        # Need to find a reliable way to bracket the root
        root, count = RootFinder(m/2, m, f, eps=abstol)
        return root
    if algorithm == 0:
        return SolveKepler0(m, e, abstol=abstol)
    elif algorithm == 1:
        return SolveKepler1(m, e, abstol=abstol)
    elif algorithm == 2:
        return SolveKepler2(m, e, abstol=abstol)
    elif algorithm == 3:
        return SolveKepler3(m, e, abstol=abstol)
    #elif algorithm == 4:
    #    return SolveKepler4(m, e, abstol=abstol)
    else:
        raise ValueError("Bad algorithm number")
def Show(m, e, p):
    def P(N, E, n, p, s):
        digits = int(math.log10(1/p)) + 1
        msg = "  Algorithm {N} = {E:.{digits}f} n = {n:2}  ({s})"
        print(msg.format(**locals()))
    E, n = Kepler(m*d2r, e, p, algorithm=0)
    P(0, E, n, p, "Simple iteration")
    E, n = Kepler(m*d2r, e, p, algorithm=1)
    P(1, E, n, p, "Newton's method")
    E, n = Kepler(m*d2r, e, algorithm=2)
    P(2, E, n, p, "Sinnott's binary search")
    E, n = Kepler(m*d2r, e, p, algorithm=3)
    P(3, E, n, p, "Projectpluto algorithm")
    #E, n = Kepler(m*d2r, e, p, algorithm=4)
    #P(4, E, n, p, "Inverse parabolic interpolation")
    print()
if __name__ == "__main__":
    from lwtest import run, assert_equal
    from frange import frange
    def TestCases():
        '''Run a variety of test cases on the different algorithms and show
        they all produce answers essentially equal to each other.
        '''
        tol = 1e-12
        for theta in range(5, 91):
            radians = theta*d2r
            for ecc in frange("0.1", "1.0", "0.1"):
                E = []
                for alg in range(4):
                    try:
                        e, n = Kepler(radians, ecc, tol, algorithm=alg)
                    except ValueError:
                        print("Too many iterations {0}".format(allowed_iterations))
                        print("theta = {theta}, ecc = {ecc:.1f}".
                            format(**locals()))
                        print("algorithm =", alg)
                        exit(1)
                    E.append(e)
                actual, n = Kepler(radians, ecc, tol/100, algorithm=3)
                for i, e in enumerate(E):
                    if abs(e - actual) > tol:
                        print("theta = {theta}, ecc = {ecc:.1f}".
                            format(**locals()))
                        print("E =")
                        for j, k in enumerate(E):
                            print(" ", j, "    ", k)
                        print("actual =", actual)
                        print("Error for i =", i)
                        print("  E[i] - actual =", E[i] - actual)
                        exit(1)
    exit(run(globals(), halt=1)[0])
