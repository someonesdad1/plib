# encoding: utf-8
'''
This module defines a cufloat object that can be used as a complex
number that has uncertainties associated with the real and imaginary
parts.

The use case which caused me to create this module is that of
wanting the uncertainty of an experimentally-measured electrical
impedance by using an oscilloscope.
'''

# Copyright (C) 2013 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

from __future__ import division, print_function
import math
import cmath
import os
import sys
import uncertainties.umath as um
from uncertainties import ufloat, UFloat
from sig import sig
from pdb import set_trace as xx

pyver = sys.version_info[0]
if pyver == 3:
    long = int

# The uncertainties correlated_values_norm function requires numpy to be
# present.
_have_correlated_values_norm = False
try:
    from uncertainties import correlated_values_norm
    _have_correlated_values_norm = True
except Exception:
    pass

class cufloat(object):
    '''Models a complex number that has uncertainty in the real and
    imaginary parts.  r is the correlation coefficient between the
    real and imaginary parts.
    '''
    def __init__(self, re_nom=0, re_std=0, im_nom=0, im_std=0, r=0):
        e = TypeError("Arguments must be int, long, or float")
        Number = (int, long, float)
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
        elif isinstance(other, (float, int, long)):
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
        if isinstance(other, (int, long, float)):
            self._re = ufloat(other, 0)
        elif isinstance(other, UFloat):
            self._re = other
        else:
            raise TypeError("Must use an integer, float, or ufloat")
    real = property(_re_get, _re_set, doc="Set the real part")
    def _im_get(self):
        return self._im
    def _im_set(self, other):
        if isinstance(other, (int, long, float)):
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
        allowed = (int, long, float, complex, UFloat, cufloat)
    if not isinstance(x, allowed):
        raise TypeError("'%s' is an improper type" % str(x))

# ----------------------------------------------------------------------
# Math functions to mirror those provided in cmath.  All except
# phase(), polar(), and rect() return a cufloat object.

def phase(x):
    _IsProperType(x, need_complex=True)
    return um.atan2(x.imag, x.real)

def polar(x):
    _IsProperType(x, need_complex=True)
    return (abs(x), phase(x))

def rect(r, theta):
    allowed = (int, long, float, UFloat)
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
    l = um.log(r)/um.log(base)
    return cufloat(l.nominal_value, l.std_dev, t.nominal_value, t.std_dev)

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

# ----------------------------------------------------------------------
# The Convert function takes a numerical argument and converts it to a
# cufloat type.
def Convert(x):
    _IsProperType(x)
    if isinstance(x, (int, long, float)):
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
    print('''
Complex electrical impedance
----------------------------
    Suppose a voltage across a capacitor was Vc = {vc} V with a polar
    angle of theta = {id} degrees.  Further suppose the current through
    the capacitor is ic = {ir} uA with a polar angle of 0.  What is the
    capacitor's impedance Z?
 
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
      Z phase angle = {ztheta_deg}\x0b
'''[:-1].format(**globals()))
