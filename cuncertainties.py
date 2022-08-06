'''
This module defines a cufloat object that can be used as a complex
number that has uncertainties associated with the real and imaginary
parts.

The use case which caused me to create this module is that of
wanting the uncertainty of an experimentally-measured electrical
impedance by using an oscilloscope.
'''
if 1:   # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2013 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <math> This module defines a cufloat object that can be used as a
    # complex number that has uncertainties associated with the real and
    # imaginary parts.
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
if 1:   # Imports
    import math
    import cmath
    import os
    import sys
    import uncertainties.umath as um
    from uncertainties import ufloat, UFloat
    from pdb import set_trace as xx
    # The uncertainties correlated_values_norm function requires numpy
    # to be present.
    _have_correlated_values_norm = False
    try:
        from uncertainties import correlated_values_norm
        _have_correlated_values_norm = True
    except Exception:
        pass
if 1:   # Custom imports
    from sig import sig
class cufloat(object):
    '''Models a complex number that has uncertainty in the real and
    imaginary parts.  r is the correlation coefficient between the
    real and imaginary parts.
    '''
    def __init__(self, re_nom=0, re_std=0, im_nom=0, im_std=0, r=0):
        e = TypeError("Arguments must be int or float")
        Number = (int, float)
        for i in (re_nom, re_std, im_nom, im_std, r):
            if not isinstance(i, Number):
                raise e
        if r and _have_correlated_values_norm:
            cm = ((1, r), (r, 1))     # Correlation matrix
            self._re, self._im = correlated_values_norm(
                ((re_nom, re_std), (im_nom, im_std)), cm)
        else:
            self._re = ufloat(re_nom, re_std)
            self._im = ufloat(im_nom, im_std)
    def __add__(self, other):
        o = self.coerce(other)
        r = self.copy()
        r._re += o._re
        r._im += o._im
        return r
    def __radd__(self, other):
        return self + other
    def __sub__(self, other):
        o = self.coerce(other)
        r = self.copy()
        r._re -= o._re
        r._im -= o._im
        return r
    def __rsub__(self, other):
        return -(self - other)
    def __mul__(self, other):
        o = self.coerce(other)
        r = self.copy()
        r._re, r._im = r._re*o._re - r._im*o._im, r._re*o._im + r._im*o._re
        return r
    def __rmul__(self, other):
        return self*other
    def __div__(self, other):
        return self.__truediv__(other)
    def __rdiv__(self, other):
        return (self*other)**(-1)
    def __truediv__(self, other):
        o = self.coerce(other)
        r = self.copy()
        m = o._re**2 + o._im**2
        x, y = r._re, r._im
        u, v = o._re, o._im
        r._re = (x*u + y*v)/m
        r._im = (u*y - x*v)/m
        return r
    def __rtruediv__(self, other):
        return (self*other)**(-1)
    def __pow__(self, other):
        o = self.coerce(other)
        return exp(o*log(self))
    def __rpow__(self, other):
        o = self.coerce(other)
        return exp(self*log(o))
    def __iadd__(self, other):
        o = self.coerce(other)
        self._re += o._re
        self._im += o._im
        return self
    def __isub__(self, other):
        o = self.coerce(other)
        self._re -= o._re
        self._im -= o._im
        return self
    def __imul__(self, other):
        o = self.coerce(other)
        self._re *= o._re
        self._im *= o._im
        return self
    def __idiv__(self, other):
        o = self.coerce(other)
        self._re /= o._re
        self._im /= o._im
        return self
    def __itruediv__(self, other):
        o = self.coerce(other)
        self._re /= o._re
        self._im /= o._im
        return self
    def __ipow__(self, other):
        raise Exception("Not implemented yet")
    def __neg__(self):
        o = self.copy()
        o._re = -o._re
        o._im = -o._im
        return o
    def __pos__(self):
        return self.copy()
    def __abs__(self):
        return um.sqrt(self._re**2 + self._im**2)
    def __invert__(self):
        '''Normally, invert (~) is used for bitwise inversion.  However,
        we'll use it for complex conjugation.
        '''
        o = self.copy()
        o._im = -o._im
        return o
    def __eq__(self, other):
        z = Convert(other)
        return (
            (self._re.nominal_value == z._re.nominal_value) and
            (self._im.nominal_value == z._im.nominal_value) and
            (self._re.std_dev == z._re.std_dev) and
            (self._im.std_dev == z._im.std_dev)
        )
    def __ne__(self, other):
        z = Convert(other)
        return not (self == other)
    def copy(self):
        r = cufloat(0, 0, 0, 0)
        r._re = self._re
        r._im = self._im
        return r
    def coerce(self, other):
        '''Coerce other types to a cufloat object.
        '''
        if isinstance(other, complex):
            return cufloat(other.real, 0, other.imag, 0)
        elif isinstance(other, (float, int)):
            return cufloat(other, 0, 0, 0)
        elif isinstance(other, UFloat):
            return cufloat(other.nominal_value, other.std_dev)
        elif isinstance(other, cufloat):
            return other.copy()
        else:
            raise TypeError("'%s' is an unsupported type" % str(other))
    def _re_get(self):
        return self._re
    def _re_set(self, other):
        if isinstance(other, (int, float)):
            self._re = ufloat(other, 0)
        elif isinstance(other, UFloat):
            self._re = other
        else:
            raise TypeError("Must use an integer, float, or ufloat")
    real = property(_re_get, _re_set, doc="Set the real part")
    def _im_get(self):
        return self._im
    def _im_set(self, other):
        if isinstance(other, (int, float)):
            self._im = ufloat(other, 0)
        elif isinstance(other, UFloat):
            self._im = other
        else:
            raise TypeError("Must use an integer, float, or ufloat")
    imag = property(_im_get, _im_set, doc="Set the imaginary part")
    def __str__(self):
        return "<" + str(self._re) + ", " + str(self._im) + ">"
    def __repr__(self):
        return "<" + repr(self._re) + ", " + repr(self._im) + ">"

pi = cufloat(math.pi)
e = cufloat(math.e)
j = cufloat(0, 0, 1)
one, two = cufloat(1), cufloat(2)

def _IsProperType(x, need_complex=False):
    '''Raise a type exception if x isn't an integer, float, complex,
    uncertainty, or cufloat.
    '''
    if need_complex:
        allowed = (complex, cufloat)
    else:
        allowed = (int, float, complex, UFloat, cufloat)
    if not isinstance(x, allowed):
        raise TypeError("'%s' is an improper type" % str(x))

if 1:   # Math functions to mirror those in cmath
    # All except # phase(), polar(), and rect() return a cufloat object.
    def phase(x):
        _IsProperType(x, need_complex=True)
        return um.atan2(x.imag, x.real)
    def polar(x):
        _IsProperType(x, need_complex=True)
        return (abs(x), phase(x))
    def rect(r, theta):
        allowed = (int, float, UFloat)
        if not isinstance(r, allowed):
            raise TypeError("'%s' is an improper type" % str(r))
        if not isinstance(theta, allowed):
            raise TypeError("'%s' is an improper type" % str(theta))
        return r*um.cos(theta), r*um.sin(theta)
    def exp(x):
        _IsProperType(x)
        z = Convert(x)
        m = um.exp(z.real)
        re = m*um.cos(z.imag)
        im = m*um.sin(z.imag)
        return cufloat(re.nominal_value, re.std_dev, im.nominal_value, im.std_dev)
    def log(x, base=math.e):
        _IsProperType(x)
        r, t = polar(x)
        L = um.log(r)/um.log(base)
        return cufloat(L.nominal_value, L.std_dev, t.nominal_value, t.std_dev)
    def log10(x):
        _IsProperType(x)
        return log(x, 10)
    def sqrt(x):
        _IsProperType(x)
        r, t = polar(x)
        x, y = rect(um.sqrt(r), t/2)
        return cufloat(x.nominal_value, x.std_dev, y.nominal_value, y.std_dev)
    def acos(x):
        _IsProperType(x)
        z = Convert(x)
        return -j*log(z + j*sqrt(one - z*z))
    def asin(x):
        _IsProperType(x)
        z = Convert(x)
        return -j*log(j*z + sqrt(one - z*z))
    def atan(x):
        _IsProperType(x)
        z = Convert(x)
        return j/two*log((j + z)/(j - z))
    def cos(x):
        _IsProperType(x)
        z = Convert(x)
        return (exp(j*z) + exp(-j*z))/two
    def sin(x):
        _IsProperType(x)
        z = Convert(x)
        return (exp(j*z) - exp(-j*z))/(two*j)
    def tan(x):
        _IsProperType(x)
        z = Convert(x)
        return sin(z)/cos(z)
    def acosh(x):
        _IsProperType(x)
        z = Convert(x)
        return log(z + sqrt(z*z - 1))
    def asinh(x):
        _IsProperType(x)
        z = Convert(x)
        return log(z + sqrt(z*z + 1))
    def atanh(x):
        _IsProperType(x)
        z = Convert(x)
        return log((one + z)/(one - z))/two
    def cosh(x):
        _IsProperType(x)
        z = Convert(x)
        return (exp(z) + exp(-z))/two
    def sinh(x):
        _IsProperType(x)
        z = Convert(x)
        return (exp(z) - exp(-z))/two
    def tanh(x):
        _IsProperType(x)
        z = Convert(x)
        return sinh(z)/cosh(z)
    def isinf(x):
        _IsProperType(x)
        z = Convert(x)
        return (math.isinf(z._re.nominal_value) or math.isinf(z._re.std_dev) or
                math.isinf(z._im.nominal_value) or math.isinf(z._im.std_dev))
    def isnan(x):
        _IsProperType(x)
        z = Convert(x)
        return (math.isnan(z._re.nominal_value) or math.isnan(z._re.std_dev) or
                math.isnan(z._im.nominal_value) or math.isnan(z._im.std_dev))
def Convert(x):
    'Takes a number x and converts it to a cufloat'
    _IsProperType(x)
    if isinstance(x, (int, float)):
        return cufloat(x, 0, 0, 0)
    elif isinstance(x, complex):
        return cufloat(x.real, 0, x.imag, 0)
    elif isinstance(x, UFloat):
        return cufloat(x.nominal_value, x.std_dev, 0, 0)
    elif isinstance(x, cufloat):
        return x.copy()
    else:
        raise TypeError("'%s' is an improper type" % str(x))

if __name__ == "__main__":
    def Examples():
        # Print some examples
        print("Examples of the use of cuncertainties module\n")
        # Plain arithmetic
        print("Real number arithmetic (unc = 0):")
        a, b = 17.2, 8.8
        for op in "+-*/":
            e = "cufloat(%s) %s cufloat(%s)" % (a, op, b)
            print(" ", e, "=", eval(e))
        # Complex arithmetic
        print("\nComplex number arithmetic (unc = 0):")
        n1, n2 = cufloat(1, 0, 1, 0), cufloat(2, 0, 1, 0)
        n1s, n2s = "cufloat(1, 0, 1, 0)", "cufloat(2, 0, 1, 0)"
        for op in "+-*/":
            e = "%s %s %s" % (n1, op, n2)
            es = "%s %s %s" % (n1s, op, n2s)
            print(" ", e, "=", eval(es))
        # Complex impedance.  These numbers came from actual
        # measurements of a 100 nF capacitor in series with a 1 kohm
        # resistor (978+/-1), with 51.6+/-3.5 mV across the resistor
        # (to get the current).  The uncertainties used are calculated
        # from the DC accuracy specifications in the scope's manual.
        Vr = ufloat(51.6e-3, 3.5e-3)    # Voltage across resistor, V
        Vc = ufloat(0.904, 0.0481)      # Voltage across capacitor, V
        R = ufloat(978, 1)              # Resistance in ohms
        iR = Vr/R                       # Current in A
        i_deg = ufloat(-89.3, 0.2)      # Current phase angle in degrees
        ir = sig(1e6*iR)
        id = sig(-i_deg)
        r = sig(R)
        vc = sig(Vc)
        theta = -i_deg*math.pi/180
        theta_ = sig(theta)
        vx, vy = Vc*um.cos(theta), Vc*um.sin(theta)
        vx_, vy_ = sig(vx), sig(vy)
        V = cufloat(vx.nominal_value, vx.std_dev,
                    vy.nominal_value, vy.std_dev)
        i = cufloat(iR.nominal_value, iR.std_dev, 0, 0)
        Z = V/i
        zx, zy = sig(Z.real), sig(Z.imag/1000)
        zm = abs(Z/1000)
        ztheta_deg = sig(um.atan(Z.imag/Z.real)*180/math.pi)
        print(dedent(f'''
        Complex electrical impedance
        ----------------------------
            Suppose a voltage across a capacitor was Vc = {vc} V with a
            polar angle of theta = {id}°.  Further suppose the current
            through the capacitor is ic = {ir} uA with a polar angle of
            0.  What is the capacitor's impedance Z?
        
            We need to convert these to cufloats:
        
                vx, vy = Vc*cos(theta), Vc*sin(theta)
                    = {vx_}, {vy_}
                V = cufloat(vx.nominal_value, vx.std_dev,
                            vy.nominal_value, vy.std_dev)
                i = cufloat(ic.nominal_value, ic.std_dev, 0, 0)
        
            The impedance is then
            Z = V/i = {Z} ohms
            Zx = {zx} ohms
            Zy = {zy} kohms
            Z magnitude = {zm} kohms
            Z phase angle = {ztheta_deg}°'''))
if __name__ == "__main__":
    import sys
    from lwtest import run, assert_equal, raises, Assert
    eps = 1e-15
    ii = isinstance
    def cufloat_rel_eq(a, b, eps=eps):
        '''a and b are cufloats.  Return True if they are less than
        eps apart in the complex plane.
        '''
        assert(ii(a, cufloat))
        assert(ii(b, cufloat))
        if a:
            return True if abs(abs(b - a)/a) < eps else False
        elif b:
            return True if abs(abs(b - a)/b) < eps else False
        else:
            return True
    def float_rel_eq(a, b, eps=eps):
        assert(ii(a, (int, float)))
        assert(ii(b, (int, float)))
        if a:
            return True if abs(b - a)/a < eps else False
        elif b:
            return True if abs(b - a)/b < eps else False
        else:
            return True
    def non_rv_equal(a, b, eps=eps):
        '''a is a cufloat object and b is a regular python complex
        number.  Ensure that their real and imaginary parts are equal
        within a relative amount of eps.
        '''
        assert ii(a, cufloat) and ii(b, complex)
        a_re = a.real.nominal_value
        a_im = a.imag.nominal_value
        assert a.real.std_dev == 0
        assert a.imag.std_dev == 0
        return (float_rel_eq(a_re, b.real) and 
            float_rel_eq(a_im, b.imag))
    def Test_functions():
        '''Use the corresponding methods of cmath to check basic
        behavior on numbers that have no uncertainty.  We should have
        identical results.
        '''
        x, y = -1.3, 2.7
        z = complex(x, y)
        zu = cufloat(x, 0, y, 0)
        non_rv_equal(zu, z)
        float_rel_eq(phase(zu).nominal_value, cmath.phase(z))
        r1, t1 = polar(zu)
        r2, t2 = cmath.polar(z)
        float_rel_eq(r1.nominal_value, r2)
        float_rel_eq(t1.nominal_value, t2)
        x1, y1 = rect(r1, t1)
        z2 = cmath.rect(r2, t2)
        float_rel_eq(x1.nominal_value, z2.real)
        float_rel_eq(y1.nominal_value, z2.imag)
        for f in (
            (exp, cmath.exp),
            (log, cmath.log),
            (log10, cmath.log10),
            (sqrt, cmath.sqrt),
            (acos, cmath.acos),
            (asin, cmath.asin),
            (atan, cmath.atan),
            (cos, cmath.cos),
            (sin, cmath.sin),
            (tan, cmath.tan),
            (acosh, cmath.acosh),
            (asinh, cmath.asinh),
            (atanh, cmath.atanh),
            (cosh, cmath.cosh),
            (sinh, cmath.sinh),
            (tanh, cmath.tanh),
        ):
            non_rv_equal(f[0](zu), f[1](z))
    def Test_trig():
        '''Check with some real values via the math module.
        '''
        for x in (0.01, 0.1, 0.5, 0.99, 1, 1.01, math.pi/2):
            assert(abs(sin(x) - cufloat(math.sin(x))) < eps)
            assert(abs(cos(x) - cufloat(math.cos(x))) < eps)
            assert(abs(tan(x) - cufloat(math.tan(x))) < eps)
            assert(abs(sinh(x) - cufloat(math.sinh(x))) < eps)
            assert(abs(cosh(x) - cufloat(math.cosh(x))) < eps)
            assert(abs(tanh(x) - cufloat(math.tanh(x))) < eps)
        # Check with some complex values via the cmath module
        for y in (0.01, 0.1, 0.5, 0.99, 1, 1.01, math.pi/2):
            x = complex(y, 1)
            z = cmath.sin(x)
            v = cufloat(z.real, 0, z.imag)
            assert(abs(sin(x) - v) < eps)
            z = cmath.cos(x)
            v = cufloat(z.real, 0, z.imag)
            assert(abs(cos(x) - v) < eps)
            z = cmath.tan(x)
            v = cufloat(z.real, 0, z.imag)
            assert(abs(tan(x) - v) < eps)
            z = cmath.sinh(x)
            v = cufloat(z.real, 0, z.imag)
            assert(abs(sinh(x) - v) < eps)
            z = cmath.cosh(x)
            v = cufloat(z.real, 0, z.imag)
            assert(abs(cosh(x) - v) < eps)
            z = cmath.tanh(x)
            v = cufloat(z.real, 0, z.imag)
            assert(abs(tanh(x) - v) < eps)
    def Test_inv_trig():
        '''Check with some real values via the math/cmath modules.
        '''
        for x in (0.01, 0.1, 0.5, 0.99, 1):
            assert(abs(asin(x) - cufloat(math.asin(x))) < eps)
            assert(abs(acos(x) - cufloat(math.acos(x))) < eps)
            assert(abs(atan(x) - cufloat(math.atan(x))) < eps)
            assert(abs(asinh(x) - cufloat(math.asinh(x))) < eps)
            if x != 1:
                assert(abs(atanh(x) - cufloat(math.atanh(x))) < eps)
            z = cmath.acosh(x)
            assert(abs(acosh(x) - cufloat(z.real, 0, z.imag)) < eps)
    def Test_properties():
        '''Check that we can read the properties.
        '''
        r, i, f = 1, 2, 3.0
        x = cufloat(r, 0, i, 0)
        assert(x.real == r)
        assert(x.imag == i)
        # Show we can also set the property value
        # int
        x.imag = i*i
        assert(x.imag == i*i)
        # float
        x.imag = f
        assert(x.imag == f)
        # ufloat
        y = ufloat(3, 8)
        x.imag = y
        assert(x.imag == y)
    def Test_identities():
        '''Show that finv(f(x)) is x.
        '''
        # Note:  limit the maximum value, as the roundoff error for
        # the cosine increases as this maximum value increases.
        for z in (
            cufloat(0.1),
            cufloat(0.5),
            cufloat(1),
            cufloat(2),
        ):
            assert(abs(z - sin(asin(z))) <= eps)
            assert(abs(z - cos(acos(z))) <= eps)
            assert(abs(z - tan(atan(z))) <= eps)
            assert(abs(z - sinh(asinh(z))) <= eps)
            assert(abs(z - cosh(acosh(z))) <= eps)
            if z != one:
                assert(abs(z - tanh(atanh(z))) <= eps)
    def Test_equality():
        '''Integer and float initialization should result in the same
        numbers.
        '''
        x = cufloat(1, 2, 3, 4)
        y = cufloat(1.0, 2.0, 3.0, 4.0)
        z = cufloat(1.0, 2.0, 3.0, 4.0 + eps)
        assert(x == x.copy())
        assert(x == y)
        assert(x != z)
    def Test_arithmetic():
        x = cufloat(1, 0, 2, 0)
        y = cufloat(3, 0, 4, 0)
        assert_equal(x + y, cufloat(4, 0, 6, 0))
        assert_equal(y - x, cufloat(2, 0, 2, 0))
        assert_equal(x*y, cufloat(-5, 0, 10, 0))
        assert_equal(x/y, cufloat(0.44, 0, 0.08, 0))
        # Now with small but nonzero uncertainties
        a = 1000
        x = cufloat(1, 1/a, 2, 2/a)
        y = cufloat(3, 3/a, 4, 4/a)
        sx, sy = 0.0031622776601683794, 0.004472135954999579
        assert_equal(x + y, cufloat(4, sx, 6, sy))
        assert_equal(y - x, cufloat(2, sx, 2, sy))
        #
        sx = 0.012083045973594572
        sy = 0.01019803902718557 
        prod = x*y
        ans = cufloat(-5, sx, 10, sy)
        # This comparison is needed for python 2.7 (4th one fails if not
        # done this way).
        assert_equal(prod.real.nominal_value, ans.real.nominal_value)
        assert_equal(prod.real.std_dev, ans.real.std_dev)
        assert_equal(prod.imag.nominal_value, ans.imag.nominal_value)
        assert_equal(prod.imag.std_dev, ans.imag.std_dev, abstol=1e-15)
        #
        sx, sy = 0.0004633319328516005, 0.000430492183436587
        assert_equal(x/y, cufloat(0.44, sx, 0.08, sy))
    def Test_init():
        z = cufloat(0)
        z = cufloat(0.0)
        z = cufloat(1)
        z = cufloat(1.0)
        z = cufloat(1, 2)
        z = cufloat(1, 2, 3)
        z = cufloat(1, 2, 3, 4)
        raises(TypeError, cufloat, 1j)
        raises(TypeError, cufloat, ufloat(1, 1))
        raises(TypeError, cufloat, cufloat(1))
if __name__ == "__main__": 
    if 1:   # Imports
        # Standard library modules
        import getopt
        import os
        import pathlib
        import sys
        from pdb import set_trace as xx
    if 1:   # Custom modules
        from wrap import dedent
        from lwtest import run, raises, assert_equal
    if 1:   # Module's base code
        def Error(msg, status=1):
            print(msg, file=sys.stderr)
            exit(status)
        def Usage(d, status=1):
            name = sys.argv[0]
            print(dedent(f'''
            Usage:  {name} [options] etc.
              Run as script to show examples of module's functions.
             
            Options:
              --test      Run internal self tests
            '''))
            exit(status)
        def ParseCommandLine(d):
            d["--test"] = False         # Run self tests
            try:
                opts, args = getopt.getopt(sys.argv[1:], "h", 
                                           "test")
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o in ("-h", "--help"):
                    Usage(d, status=0)
                elif o == "--test":
                    d["--test"] = True
            return args
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["--test"]:
        exit(run(globals(), halt=True)[0])
    else:
        Examples()
