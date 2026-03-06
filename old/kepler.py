'''
Functions to calculate a solution to Kepler's equation
    [1] Meeus "Astronomical Algorithms", pg 206.
    [2] https://www.projectpluto.com/kepler.htm
    
    The equation is E = M + e*sin(E).  E is to be solved for given M and
    e.  M will be between 0 and 2*pi and e >= 0.
    
    The iterative methods include a third parameter precision, which is
    what two successive iterations must be less than for the function to
    return.
    
    The individual SolveKepler* functions return a tuple (E, n) where E
    is the eccentric anomaly and n is the number of iterations to get
    the answer.  The test examples demonstrate how much faster Newton's
    method is over plain iteration.
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Functions to calculate a solution to Kepler's equation oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2002 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ sci oo>
        <oo test ∞ run oo>
        <oo todo ∞ oo>
    '''
    if 1:  # Standard imports
        import enum
        import math
    if 1:  # Custom imports
        from dpmath import signum
        try:
            from root import RootFinder
            _have_rootfinder = True
        except ImportError:
            _have_rootfinder = False
    if 1:  # Global variables
        class G:
            pass
        g = G()
        __all__ = ["Kepler"]
        g.N = 120
if 1:  # Classes
    class Alg(enum.Enum):
        iteration = enum.auto()
        newton = enum.auto()
        binary_search = enum.auto()
        c_code = enum.auto()
        root_finder = enum.auto()
if 1:  # Core functionality
    def Kepler(m, e, abstol=1e-8, algorithm=Alg.binary_search):
        '''Call one of the Kepler equation solving methods.  Return the value of E
        (eccentric anomaly) and the number of iterations required.
        '''
        def SolveKeplerIteration(m, e, abstol=abstol):
            '''Use simple iteration to the indicated precision.'''
            E0, E, count = m/2, m, 0
            while abs(E - E0) > abstol/10 and count <= g.N:
                E0 = E
                count += 1
                E = m + e*math.sin(E0)
            if count > g.N:
                msg = "Too many iterations ({0}) in SolveKeplerIteration"
                raise ValueError(msg.format(count))
            return (E, count)
        def SolveKeplerNewton(m, e, abstol=abstol):
            '''Use Newton's method to solve for the root.'''
            E0, E, count = m/2, m, 0
            while abs(E - E0) > abstol and count <= g.N:
                E0 = E
                count += 1
                E = E0 + (m + e*math.sin(E0) - E0)/(1 - e*math.cos(E0))
            if count > g.N:
                msg = "Too many iterations ({0}) in SolveKeplerNewton"
                raise ValueError(msg.format(count))
            return (E, count)
        def SolveKeplerBinarySearch(m, e, abstol=abstol):
            '''Uses Sinnott's binary search algorithm.  abstol is
            ignored.
            '''
            m, f = math.fmod(m, math.tau), 1
            m = m + math.tau if m < 0 else m
            if m > math.pi:
                m, f = math.tau - m, -1
            e0, d = math.pi/2, math.pi/4
            for i in range(1, 54, 1):
                m1 = e0 - e*math.sin(e0)
                e0 = e0 + d*signum(m - m1)
                d = d/2
            return (e0*f, 54)
        def SolveKeplerCCode(m, e, abstol=abstol):
            '''Translated from C code at
            http://www.projectpluto.com/kepler.htm (note 1).  "Meeus" refers to
            "Astronomical Algorithms" by J. Meeus.  I've modified the routine
            slightly for e < 0.3 because it was not converging to the desired
            precision.  It also required adding checks for too many iterations.
            
            Note 1:  https://github.com/Bill-Gray/lunar/blob/master/astfuncs.cpp is to
            be consulted for later code.
            '''
            neg, count, thresh = False, 0, abstol*math.fabs(1 - e)
            if not m:
                return (0, 0)
            if e < 0.3:  # Low-eccentricity formula from Meeus, p. 195
                curr = math.atan2(math.sin(m), math.cos(m) - e)
                err = curr - e*math.sin(curr) - m
                while math.fabs(err) > thresh:
                    curr -= err/(1 - e*math.cos(curr))
                    err = curr - e*math.sin(curr) - m
                    if count > g.N:
                        msg = "Too many iterations ({0}) in SolveKeplerCCode for e < 0.3 case"
                        raise ValueError(msg.format(count))
                    count += 1
                return (curr, count)
            if m < 0:
                m = -m
                neg = True
            curr = m
            if e > 0.8 and m < math.pi/3 or e > 1:  # Up to 60 degrees
                trial = m/math.fabs(1 - e)
                if trial**2 > 6*math.fabs(1 - e):  # Cubic term is dominant
                    if m < math.pi:
                        trial = (6*m) ** (1/3)
                    else:  # Hyperbolic w/ 5th & higher-order terms predominant
                        trial = math.asinh(m/e)
                curr = trial
            if e < 1:
                err = curr - e*math.sin(curr) - m
                while math.fabs(err) > thresh:
                    curr -= err/(1 - e*math.cos(curr))
                    err = curr - e*math.sin(curr) - m
                    if count > g.N:
                        msg = "Too many iterations ({0}) in SolveKeplerCCode for e < 1 case"
                        raise ValueError(msg.format(count))
                    count += 1
            else:
                err = e*math.sinh(curr) - curr - m
                while math.fabs(err) > thresh:
                    curr -= err/(e*math.cosh(curr) - 1)
                    err = e*math.sinh(curr) - curr - m
                    if count > g.N:
                        msg = "Too many iterations ({0}) in SolveKeplerCCode for e >= 1 case"
                        raise ValueError(msg.format(count))
                    count += 1
            curr = -curr if neg else curr
            return (curr, count)
        def SolveKepler4(m, e, abstol=abstol):
            '''Use RootFinder, which is Jack Crenshaw's enhancements to an older IBM
            FORTRAN routine that uses inverse parabolic interpolation.
            '''
            def f(E):
                return m + e*math.sin(E) - E
            # Need to find a reliable way to bracket the root
            root, count = RootFinder(m/2, m, f, eps=abstol)
            return root
        if algorithm == Alg.iteration:
            return SolveKeplerIteration(m, e, abstol=abstol)
        elif algorithm == Alg.newton:
            return SolveKeplerNewton(m, e, abstol=abstol)
        elif algorithm == Alg.binary_search:
            return SolveKeplerBinarySearch(m, e, abstol=abstol)
        elif algorithm == Alg.c_code:
            return SolveKeplerCCode(m, e, abstol=abstol)
        # elif algorithm == Alg.root_finder:
        #    return SolveKepler4(m, e, abstol=abstol)
        else:
            raise ValueError("Bad algorithm number")
    def Show(m, e, p):
        def P(N, E, n, p, s):
            digits = int(math.log10(1/p)) + 1
            msg = "  Algorithm {N} = {E:.{digits}f} n = {n:2}  ({s})"
            print(msg.format(**locals()))
        E, n = Kepler(math.radians(m), e, p, algorithm=Alg.iteration)
        P(0, E, n, p, "Simple iteration")
        E, n = Kepler(math.radians(m), e, p, algorithm=Alg.newton)
        P(1, E, n, p, "Newton's method")
        E, n = Kepler(math.radians(m), e, algorithm=Alg.binary_search)
        P(2, E, n, p, "Sinnott's binary search")
        E, n = Kepler(math.radians(m), e, p, algorithm=Alg.c_code)
        P(3, E, n, p, "Projectpluto algorithm")
        # E, n = Kepler(math.radians(m), e, p, algorithm=Alg.root_finder)
        # P(4, E, n, p, "Inverse parabolic interpolation")
        print()

if __name__ == "__main__":
    from lwtest import run
    from frange import frange
    def TestCases():
        '''Run a variety of test cases on the different algorithms and show
        they all produce answers essentially equal to each other.
        '''
        tol = 1e-12
        for theta in range(5, 91):
            radians = math.radians(theta)
            for ecc in frange("0.1", "1.0", "0.1"):
                E = []
                for alg in (Alg.iteration, Alg.newton, Alg.binary_search, Alg.c_code):
                    try:
                        e, n = Kepler(radians, ecc, tol, algorithm=alg)
                    except ValueError:
                        print("Too many iterations {0}".format(g.N))
                        print("theta = {theta}, ecc = {ecc:.1f}".format(**locals()))
                        print("algorithm =", alg)
                        exit(1)
                    E.append(e)
                actual, n = Kepler(radians, ecc, tol/100, algorithm=Alg.c_code)
                for i, e in enumerate(E):
                    if abs(e - actual) > tol:
                        print("theta = {theta}, ecc = {ecc:.1f}".format(**locals()))
                        print("E =")
                        for j, k in enumerate(E):
                            print(" ", j, "    ", k)
                        print("actual =", actual)
                        print("Error for i =", i)
                        print("  E[i] - actual =", E[i] - actual)
                        exit(1)
    exit(run(globals(), halt=1)[0])
