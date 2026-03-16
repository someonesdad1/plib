if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2008 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ category oo>
        <oo test ∞ run oo>
        <oo todo ∞
            - ∞∞3 Move to dpmath
        oo>
    '''
    if 1:  # Standard imports
        import math
        import cmath
    if 1:  # Custom imports
        pass
    if 1:  # Global variables
        pass
if 1:  # Core functionality
    def lngamma(z):
        '''Routine to calculate the logarithm of the gamma function.  Translated from C.
        See page 160 of "Numerical Recipes".  This is Lanczos' remarkable formula.  |error|
        < 2e-10 everywhere Re x > 0.
        '''
        stp = 2.50662827465
        if isinstance(z, complex):
            if z.real <= 0:
                raise ValueError("Argument's real part must be > 0")
            x = z - 1
            tmp = x + 5.5
            tmp = (x + 0.5)*cmath.log(tmp) - tmp
            ser = (1 + 76.18009173/(x + 1) - 86.50532033/(x + 2) + 24.01409822/(x + 3)
                - 1.231739516/(x + 4) + 0.120858003e-2/(x + 5) - 0.536382e-5/(x + 6))
            return tmp + cmath.log(stp*ser)
        else:
            if z <= 0:
                raise ValueError("Argument must be > 0")
            x = z - 1
            tmp = x + 5.5
            tmp = (x + 0.5)*math.log(tmp) - tmp
            ser = (1 + 76.18009173/(x + 1) - 86.50532033/(x + 2) + 24.01409822/(x + 3)
                - 1.231739516/(x + 4) + 0.120858003e-2/(x + 5) - 0.536382e-5/(x + 6))
            return tmp + math.log(stp*ser)

if __name__ == "__main__":
    import dpseq
    import lwtest
    import trm
    t = trm.Trm()
    def TestReal():
        tol = 1e-10
        for x, value in ((1, 1), (1.1, 0.9513507699), (1.61, 0.8946806085)):
            assert math.fabs(math.exp(lngamma(x)) - value) < tol
        assert math.fabs(lngamma(100) - 359.13420537) < 1e-7
        # If we are running under python 3, then the math library has lgamma
        # which we can test against.
        tol = 2e-9
        for x in dpseq.frange("0.1", "10", "0.1"):
            y = lngamma(x)
            y0 = math.lgamma(x)
            if not y0:
                assert y < tol
            else:
                lwtest.assert_equal(lngamma(x), math.lgamma(x), reltol=tol)
    def TestComplex():
        # Use mpmath for complex value standards
        try:
            from mpmath import ln, gamma
        except ImportError:
            t.print(f"{t.yel}Warning:  TestComplex in lngamma_test.py not run")
            return
        start, stop, step = 0, 10, 1
        eps = 3e-10
        for r in dpseq.frange(start + step, stop, step):
            for i in dpseq.frange(start + step, stop, step):
                z = complex(r, i)
                got = lngamma(z)
                expected = ln(gamma(z))
                diff = abs(got - expected)
                if diff > 1:  # Correct for phase difference of n*pi
                    diff -= round(diff/math.pi, 6)*math.pi
                assert diff <= eps
    exit(lwtest.run(globals(), halt=1)[0])
