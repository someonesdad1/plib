'''
Provides probability functions used in basic statistics

    Use the convenience instances normal, chisq, F, binomial, student_t,
    and poisson.  Call the cdf() method for the CDF and icdf() method for
    the inverse CDF.  When needed, degree of freedom arguments come first.

    Examples

        1) What is the probability of a standard normal deviate being -1.8
           and 1.8 standard deviations from the mean?
            
                print(normal.cdf(-1.8)) --> 0.0359
                print(normal.cdf(1.8))  --> 0.964

           As expected, they sum to unit probability.  For more digits, set
           the N attribute of a flt instance to a higher number:

                flt(0).N = 8
                print(normal.cdf(-1.8)) --> 0.035930319
                print(normal.cdf(1.8))  --> 0.96406968

        2) A linear regression ANOVA had an F statistic ratio of 31.2 with
           df1 = 12 and df2 = 4.  What is the significance level?

                print(F.cdf(12, 4, 31.2)) --> 0.998

           You'd thus expect no effect to have an F value this large only
           once in 500 times, so the regression is likely significant.

    Implementation

        The implementation uses S. Moshier's cephes library functions from
        https://netlib.org/cephes (the double precision library). 

        Other distributions and special functions can be added by editing
        the construction of the cephes.dll DLL in cephes/makefile, then
        adding calling support in this module.  The DLL build is specific
        to cygwin and cygwin's python 3.7; other environments will need
        different tools.

        Method overview:  ctypes.cdll.LoadLibrary() is used to get a handle
        to the DLL.  This is used in each of the classes derived from the
        Prob class to access the needed compiled C functions in cephes.dll.
        It's important to specify the C types of the C function's input
        parameters (the .argtypes attribute) and the C function's return
        type (the .restype attribute), otherwise things will seem to work
        but the numbers will be wrong.  

        Testing:  run this module with the --test option to run the
        self-tests.  These tests include a TestUsing_mpmath() function that
        will compare Moshier's functions' output to those of mpmath.
        mpmath's ncdf, incomplete gamma, and incomplete beta functions
        provide arbitrary-precision checks of Moshier's functions and
        results agree to around 2e-16, which is typical IEEE floating point
        precision levels.

        Precision:  Moshier's documentation indicates worst-case conditions
        from his domain tests should give around 9 digits of precision in
        terms of relative error and usually 14 or more.  Even 9 digits is
        well beyond what is needed for practical work, which most of the
        time only needs two or three digits.  

        For making important decisions where the cost of a mistake is
        significant, I'd recommend backing up this module's results with a
        calculation by mpmath AND looking up things in a trusted printed
        reference.  Then get a coworker to check your results.  Mistakes
        are often caused by lack of standardization and documentation
        (stuff found on the web is often particularly crappy).  For
        example, that table you're using might be for one-sided tests, but
        the authors decided to make it a double-sided test -- and they
        don't label their assumptions or give you a picture of the
        integrand's graph being evaluated.  Another example is the
        significance level is in % but you assumed it wasn't or vice versa.
        In the 70's and 80's when I did a fair bit of experimental work, my
        favorite statistics reference was Crow, "Statistics Manual"
        (republished by Dover) because it was both terse and carefully
        labeled.  Biometrika Tables by Pearson and Hartley is also good,
        but you'll want to make sketches of the functions being integrated
        on the tables you're using.

'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Provides core probability functions used in basic statistics
        #∞what∞#
        #∞test∞# --test #∞test∞#
    # Standard imports
        from ctypes import cdll, c_double, c_int, c_short
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
    # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from f import flt
        from lwtest import run, raises, assert_equal, Assert
        from frange import frange
        try:
            import mpmath
            have_mpmath = True
        except ImportError:
            have_mpmath = False
        if 0:
            import debug
            debug.SetDebugger()
    # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        __all__ = '''normal chisq F binomial student_t poisson
            Prob Normal Chisq Fdist Binomial StudentT Poisson'''.split()
        # Colors
        t.ti = t("grnl")
        t.hdr = t("purl")
        t.first = t("sky")
        t.warn = t("ornl")
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] dist
          Print basic statistics tables.  dist should be:  normal,
          chisq, or t.
        Options:
            -h      Print a manpage
            -i      Print inverse CDF.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-i"] = False     # Print inverse CDF
        d["-d"] = 4         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:ih", ["help", "test"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("i"):
                d[o] = not d[o]
            elif o == "--test":
                exit(run(globals(), halt=True)[0])
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
if 1:   # Classes
    # Distributions:  normal, chisq, F, binomial, t, Poisson
    class Prob:
        def __init__(self, dll):
            self.dll = dll
        def cdf(self):
            'Return the cumulative distribution function'
            raise TypeError("Abstract method")
        def icdf(self):
            'Return the inverse cumulative distribution function'
            raise TypeError("Abstract method")
        def check_p(self, p, full=False):
            '''Verify that a probability p has acceptable values.  p must
            be on (0, 1) if full is False and on [0, 1] if full is True.
            '''
            if full:
                if not (0 <= p <= 1):
                    raise ValueError("p must be on [0, 1]")
            else:
                if not (0 < p < 1):
                    raise ValueError("p must be on (0, 1)")
        def check_df(self, df, allow_zero=False):
            '''Verify a degrees of freedom variable, which must be an
            integer > 0 if allow_zero is False and >= 0 if allow_zero is
            True.
            '''
            if not ii(df, int):
                raise TypeError("Argument must be an integer")
            if allow_zero:
                if df < 0:
                    raise ValueError("Argument must be >= 0")
            else:
                if df <= 0:
                    raise ValueError("Argument must be > 0")
    class Normal(Prob):
        def __init__(self, dll):
            super().__init__(dll)
            self._cdf = self.dll.ndtr
            self._cdf.argtypes = [c_double]
            self._cdf.restype = c_double
            self._icdf = self.dll.ndtri
            self._icdf.argtypes = [c_double]
            self._icdf.restype = c_double
        def cdf(self, x):
            return flt(self._cdf(x))
        def icdf(self, p):
            if not (0 < p < 1):
                raise ValueError("p must be on (0, 1)")
            return flt(self._icdf(p))
    class Chisq(Prob):
        def __init__(self, dll):
            super().__init__(dll)
            self._cdf = self.dll.chdtr
            self._cdf.argtypes = [c_double, c_double]
            self._cdf.restype = c_double
            self._icdf = self.dll.chdtri
            self._icdf.argtypes = [c_double, c_double]
            self._icdf.restype = c_double
        def cdf(self, df, x):
            self.check_df(df)
            return flt(self._cdf(df, x))
        def icdf(self, df, p):
            # Note the cephes inverse is of the complemented CDF (i.e.,
            # area under the right-hand tail), so we call with 1 - p.
            self.check_df(df)
            self.check_p(p)
            return flt(self._icdf(df, 1 - p))
    class Fdist(Prob):
        def __init__(self, dll):
            super().__init__(dll)
            self._cdf = self.dll.fdtr
            self._cdf.argtypes = [c_int, c_int, c_double]
            self._cdf.restype = c_double
            self._icdf = self.dll.fdtri
            self._icdf.argtypes = [c_int, c_int, c_double]
            self._icdf.restype = c_double
        def cdf(self, df1, df2, x):
            if x <= 0:
                raise ValueError("x must be > 0")
            self.check_df(df1)
            self.check_df(df2)
            return flt(self._cdf(df1, df2, x))
        def icdf(self, df1, df2, p):
            # Note the cephes inverse is of the complemented CDF (i.e.,
            # area under the right-hand tail), so we call with 1 - p.
            self.check_df(df1)
            self.check_df(df2)
            self.check_p(p)
            return flt(self._icdf(df1, df2, 1 - p))
    class Binomial(Prob):
        def __init__(self, dll):
            super().__init__(dll)
            self._cdf = self.dll.bdtr
            self._cdf.argtypes = [c_int, c_int, c_double]
            self._cdf.restype = c_double
            self._icdf = self.dll.bdtri
            self._icdf.argtypes = [c_int, c_int, c_double]
            self._icdf.restype = c_double
        def cdf(self, k, n, p):
            self.check_df(k, allow_zero=True)
            self.check_df(n)
            self.check_p(p, full=True)
            return flt(self._cdf(k, n, p))
        def icdf(self, k, n, p):
            '''Returns the binomial event probability such that the sum of
            the terms of 0 to k for size n is equal to the cumulative
            probability p.
            '''
            self.check_df(k, allow_zero=True)
            self.check_df(n)
            self.check_p(p, full=True)
            return flt(self._icdf(k, n, p))
    class StudentT(Prob):
        def __init__(self, dll):
            super().__init__(dll)
            self._cdf = self.dll.stdtr
            self._cdf.argtypes = [c_short, c_double]
            self._cdf.restype = c_double
            self._icdf = self.dll.stdtri
            self._icdf.argtypes = [c_int, c_double]
            self._icdf.restype = c_double
        def cdf(self, df, x):
            self.check_df(df)
            return flt(self._cdf(df, x))
        def icdf(self, df, p):
            self.check_df(df)
            self.check_p(p)
            return flt(self._icdf(df, p))
    class Poisson(Prob):
        def __init__(self, dll):
            super().__init__(dll)
            self._cdf = self.dll.pdtr
            self._cdf.argtypes = [c_int, c_double]
            self._cdf.restype = c_double
            self._icdf = self.dll.pdtri
            self._icdf.argtypes = [c_int, c_double]
            self._icdf.restype = c_double
        def cdf(self, k, λ):
            self.check_df(k, allow_zero=True)
            if λ < 0:
                raise ValueError("λ must be >= 0")
            return flt(self._cdf(k, λ))
        def icdf(self, k, p):
            self.check_df(k, allow_zero=True)
            self.check_p(p)
            return flt(self._icdf(k, p))
if 1:   # Convenience class instances
    _dll = cdll.LoadLibrary("cephes.dll")
    normal = Normal(_dll)
    chisq = Chisq(_dll)
    F = Fdist(_dll)
    binomial = Binomial(_dll)
    student_t = StudentT(_dll)
    poisson = Poisson(_dll)
if 1:   # Test functions
    def TestNormal():
        x = flt(0.51)
        a = normal.cdf(x)
        Assert(a == 0.6949742691024806)
        Assert(type(a) == type(x))
        # Show the inverse gives x
        i = normal.icdf(a)
        Assert(type(i) == type(x))
        Assert(i == x)
        # Illegal stuff
        raises(ValueError, normal.icdf, 0)
        raises(ValueError, normal.icdf, 1)
    def TestChisq():
        x, df = flt(0.554), 5
        # Should get CDF around 0.01
        a = chisq.cdf(df, x)
        Assert(str(a) == "0.00999")
        b = chisq.icdf(df, a)
        Assert(b == x)
        # Illegal stuff
        raises(TypeError, chisq.cdf, 5.0, 0)
        raises(ValueError, chisq.icdf, 5, 0)
        raises(ValueError, chisq.icdf, 5, 1)
    def TestF():
        x, df1, df2 = flt(8.75), 5, 6
        # Should get CDF around 0.99
        a = F.cdf(df1, df2, x)
        Assert(str(a) == "0.99")
        b = F.icdf(df1, df2, a)
        assert_equal(b, x, abstol=9e-15)
        # Illegal stuff
        raises(TypeError, F.cdf, 5.0, 0, 1)
        raises(TypeError, F.cdf, 5, 0.0, 1)
        raises(ValueError, F.icdf, 5, 6, 0)
        raises(ValueError, F.icdf, 5, 6, 1)
    def TestBinomial():
        p, k, n = flt(0.75), 2, 4
        # We can calculate the probability from 
        # C(4, 0)*p**0*(1-p)**4 + C(4, 1)*p**1*(1-p)**3 +
        # C(4, 2)*p**2*(1-p)**2 where C are the binomial coefficients and
        # C(n, m) = n!/(n - m)!*m!).
        a, q = binomial.cdf(k, n, p), 1 - p
        expected = q**4 + 4*p*q**3 + 6*p**2*q**2
        assert_equal(a, expected)
        # Inverse function
        x = binomial.icdf(k, n, a)
        assert_equal(x, p)
        # Illegal stuff
        raises(TypeError, binomial.cdf, 5.0, 0, 1)
        raises(TypeError, binomial.cdf, 5, 0.0, 1)
        raises(ValueError, binomial.cdf, 2, 3, -0.1)
        raises(ValueError, binomial.cdf, 2, 3, 1.1)
        raises(TypeError, binomial.icdf, 5.0, 0, 1)
        raises(TypeError, binomial.icdf, 5, 0.0, 1)
        raises(ValueError, binomial.icdf, 2, 3, -0.1)
        raises(ValueError, binomial.icdf, 2, 3, 1.1)
    def TestStudentT():
        x, df = flt(4.032), 5
        p = student_t.cdf(df, x)
        Assert(str(p) == "0.995")
        y = student_t.icdf(df, 0.995)
        Assert(str(y) == str(x))
        # Large negative value should produce small cumulative probability
        y = student_t.cdf(df, -120)
        p = flt(3.81e-10)
        Assert(str(y) == str(p))
        # Should be symmetrical
        z = student_t.cdf(df, 120)
        Assert(str(z) == str(1 - p))
        # Illegal stuff
        raises(TypeError, student_t.cdf, 5.0, 0.5)
        raises(TypeError, student_t.icdf, 5.0, 0.5)
        raises(ValueError, student_t.icdf, 5, 0)
        raises(ValueError, student_t.icdf, 5, 1)
    def TestPoisson():
        λ, k = 0.5, 1
        # CDF is exp(-λ)*(1 + λ)
        from f import exp
        expected = exp(-λ)*(1 + λ)
        got = poisson.cdf(k, λ)
        Assert(expected == got)
        # Inverse
        y = poisson.icdf(k, got)
        Assert(y == λ)
        # Illegal stuff
        raises(TypeError, poisson.cdf, 5.0, 0.5)
        raises(TypeError, poisson.icdf, 5.0, 0.5)
        raises(ValueError, poisson.icdf, 5, 0)
        raises(ValueError, poisson.icdf, 5, 1)
    def TestUsing_mpmath():
        if not have_mpmath:
            t.print(f"{t.warn}{sys.argv[0]}:  mpmath not available for testing")
            return
        eps = 2e-16
        # mpmath.ncdf() is the normal distribution CDF.  The argument is
        # limited to 27.4 because the cephes' function returns 0 for larger
        # arguments.
        for x1 in frange("0", "27.4", "0.05", return_type=flt):
            x2 = mpmath.mpf(x1)
            cdf1 = normal.cdf(x1)
            cdf2 = flt(mpmath.ncdf(x2))
            assert_equal(cdf1, cdf2, abstol=eps)
            cdf1 = normal.cdf(-x1)
            cdf2 = flt(mpmath.ncdf(-x2))
            assert_equal(cdf1, cdf2, abstol=eps)
        # mpmath.gammainc() is the incomplete gamma function which can be
        # used to calculate the Poisson and chi-square CDFs.
        for λ in frange("0", "10", "1", return_type=flt):
            if not λ:
                continue
            for k in range(1, 20):
                cdf1 = poisson.cdf(k, λ)
                cdf2 = flt(mpmath.gammainc(k + 1, λ, regularized=True))
                assert_equal(cdf1, cdf2, abstol=eps)
                cdf1 = chisq.cdf(k, λ)
                cdf2 = flt(mpmath.gammainc(k/2, λ/2, regularized=True))
                assert_equal(cdf1, cdf2, abstol=eps)
        # mpmath.betainc() is the incomplete beta function which can be
        # used to calculate the binomial and Student's t CDFs.
        beta = mpmath.betainc
        # Binomial
        for p in frange("0", "1", "0.05", return_type=flt):
            if not p:
                continue
            for n in range(2, 20):
                for k in range(0, n):
                    cdf1 = binomial.cdf(k, n, p)
                    cdf2 = flt(beta(n - k, k + 1, x2=1 - p, regularized=True))
                    assert_equal(cdf1, cdf2, abstol=eps)
        # Student's t
        K = list(range(1, 31)) + [40, 60, 120]
        for T in frange("0", "50", "1", return_type=flt):
            for k in K:
                cdf1 = student_t.cdf(k, T)
                z = k/(k + T**2)
                cdf2 = 1 - flt(beta(k/2, 1/2, x2=z, regularized=True))/2
                assert_equal(cdf1, cdf2, abstol=eps)
        # F
        K = list(range(1, 30, 5))
        for df1 in K:
            for df2 in K:
                for x in frange("0", "50", "1", return_type=flt):
                    if not x:
                        continue
                    cdf1 = F.cdf(df1, df2, x)
                    cdf2 = flt(beta(df1/2, df2/2, x2=df1*x/(df2 + df1*x), regularized=True))
                    assert_equal(cdf1, cdf2, abstol=eps)
if 1:   # Table functions
    X = flt(0)
    def Table(name):
        X.N = d["-d"]
        X.rtz = X.rtdp = False
        X.rlz = True
        if "norm" in name.lower():
            if d["-i"]:
                InvNormalTable()
            else:
                NormalTable()
        elif name.lower() == "t":
            TTable()
        elif "chi" in name.lower():
            ChiSquareTable()
        else:
            Error(f"{name!r} not recognized")
    def NormalTable():
        c0 = 4              # Width of first column
        w = (W - c0)//10    # Width of numerical columns
        def Hdr():
            t.print(f"{t.ti}{'Normal CDF':^{W}s}")
            print(" "*c0, end=f"{t.hdr}")
            for i in range(10):
                print(f"{i/100!s:^{w}s}", end="")
            t.print()
        Hdr()
        done = False
        for i in frange("0.0", "4.1", "0.1", return_type=flt):
            for j in frange("0", "0.1", "0.01"):
                z = i + j
                if not j:
                    with X:
                        X.rtz = X.rtdp = X.rlz = False
                        X.N = 1 if i < 1 else 2
                        print(f"{t.first}{i!s:{c0}s}{t.n}", end="")
                cdf = normal.cdf(z)
                s = set(str(cdf)[1:])
                if s == {"9"}:
                    done = True
                print(f"{cdf!s:^{w}s}", end="")
            print()
            if done:
                break
    def InvNormalTable():
        c0 = 6              # Width of first column
        w = (W - c0)//10    # Width of numerical columns
        # Percentage point table
        def NormHdr():
            t.print(f"{t.ti}{'Inverse Normal CDF':^{W}s}")
            print(" "*c0, end=f"{t.hdr}")
            for i in range(10):
                print(f"{i/100!s:^{w}s}", end="")
            t.print()
        NormHdr()
        for i in frange("0.0", "1.0", "0.1", return_type=flt):
            for j in frange("0", "0.1", "0.01"):
                p = i + j
                if not j:
                    # Print first column
                    with X:
                        X.rtz = X.rtdp = X.rlz = False
                        X.N = 1 if i < 1 else 2
                        print(f"{t.first}{i!s:{c0}s}{t.n}", end="")
                if 0.47 <= p <= 0.49:
                    X.N = d["-d"] - 2
                elif p < 0.54:
                    X.N = d["-d"] - 1
                else:
                    X.N = d["-d"]
                z = normal.icdf(p) if p else "-∞"
                print(f"{z!s:^{w}s}", end="")
            print()
        i = flt(0.99)
        for j in frange("0", "0.01", "0.001"):
            p = i + j
            if not j:
                with X:
                    X.rtz = X.rtdp = X.rlz = False
                    X.N = 2
                    # Header with more digits
                    print(" "*c0, end=f"{t.hdr}")
                    for k in range(10):
                        print(f"{k/1000!s:^{w}s}", end="")
                    t.print()
                    print(f"{t.first}{i!s:{c0}s}{t.n}", end="")
            z = normal.icdf(p)
            print(f"{z!s:^{w}s}", end="")
        print()
    def TTable():
        c0 = 4              # Width of first column
        sigpct = (20, 15, 10, 5, 2.5, 1, 0.5, 0.1)
        DF = list(range(1, 21)) + list(range(22, 41, 2))
        DF += list(range(50, 101, 10))
        pct = [flt(i) for i in sigpct]
        w = (W - c0)//len(sigpct)    # Width of numerical columns
        title = "Critical Values for Student's t"
        t.print(f"{t.ti}{title:^{W}s}")
        print(f"{t.hdr}{'df':^{c0}s}", end="")
        for p in sigpct:
            print(f"{str(p) + '%':^{w}s}", end="")
        t.print()
        for df in DF:
            print(f"{str(df):^{c0}s}", end="")
            for p in pct:
                cv = student_t.icdf(df, 1 - p/100)
                print(f"{cv!s:^{w}s}", end="")
            print()
    def ChiSquareTable():
        c0 = 4              # Width of first column
        sigpct = (50, 30, 20, 10, 5, 2, 1, 0.1)
        DF = list(range(1, 31)) + list(range(40, 101, 10))
        pct = [flt(i) for i in sigpct]
        w = (W - c0)//len(sigpct)    # Width of numerical columns
        title = "Critical Values for Chi-square"
        t.print(f"{t.ti}{title:^{W}s}")
        print(f"{t.hdr}{'df':^{c0}s}", end="")
        for p in sigpct:
            print(f"{str(p) + '%':^{w}s}", end="")
        t.print()
        for df in DF:
            print(f"{str(df):^{c0}s}", end="")
            for p in pct:
                cv = chisq.icdf(df, 1 - p/100)
                print(f"{cv!s:^{w}s}", end="")
            print()

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    for name in args:
        Table(name)
