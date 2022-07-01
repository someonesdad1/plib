'''
TODO:
 
    - Utilize flt to get rid of SigFig
    - Fully integrate matrix.py and change CTM etc. to real matrices.
    - What about movement?  An object could be given a constant velocity
      and its position at a later time would be calculated.  Even
      better, allow the initial velocity and constant acceleration to be
      defined.  This logically extends to letting the acceleration or
      force for an object with mass be defined by a function of time;
      the script would have to integrate the equations of motion to
      get the position at later times.
    - Update properties to more modern syntax

----------------------------------------------------------------------
 
Models points, lines, and planes and their transformations.  See the
documentation xyz.pdf for details.

'''
if 1:  # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2013 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # <math> Models points, lines, and planes and their transformations
        #∞what∞#
        #∞test∞# run #∞test∞#
    # Standard imports
        import sys
        import traceback
        from math import pi, e
        from pdb import set_trace as xx
    # Custom imports
        use_sig = True
        if use_sig:
            from sig import SigFig
        from f import flt
        import matrix
        Numbers = [int, float, flt]
        # Uncertainties library
        try:
            # Note these will replace all of math's symbols except pi and e
            from uncertainties.umath import (
                acos, acosh, asin, asinh, atan, atan2, atanh, ceil, copysign, cos,
                cosh, degrees, exp, fabs, factorial, floor, fmod, frexp, fsum,
                hypot, isinf, isnan, ldexp, log, log10, log1p, modf, pow,
                radians, sin, sinh, sqrt, tan, tanh, trunc)
            from uncertainties import ufloat, UFloat
            have_unc = True
            Numbers += [UFloat]
        except ImportError:
            have_unc = False
        # Numpy support must be enabled manually
        use_numpy = False
        if use_numpy:
            import numpy as np
            from numpy.linalg import det as npdet
    # Global variables
        __all__ = [
            "Ctm",
            "V",
            "Point",
            "Line",
            "Plane",
            "UseUnicode",
            "Det3",
            "Det4",
        ]
        ii = isinstance
        Numbers = tuple(Numbers)
        # If True, use Unicode symbols in string representations
        _use_unicode = False
def UseUnicode(s=True):
    global _use_unicode
    _use_unicode = True if s else False
class Ctm(object):
    '''Encapsulates the coordinate transformation matrix, combines
    transformations, and transforms points.  The transformation matrix
    elements are
        [ a  b  c  t ]
        [ d  e  f  u ]
        [ g  h  i  v ]
        [ 0  0  0  1 ]
    Thus, there are only 12 independent parameters.  This matrix is
    used with (x, y, z) homogeneous coordinates; thus, the coordinate
    elements these matrices left-multiply on are the transpose of the
    row vector [x, y, z, w] where w is 1.
     
    The CTM always transforms the default coordinates into the current
    coordinate system.  The ICTM, the inverse CTM, transforms from
    current coordinates to default coordinates.
    '''
    _CTM = [1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1]
    _ICTM = [1, 0, 0, 0,
             0, 1, 0, 0,
             0, 0, 1, 0,
             0, 0, 0, 1]
  
        # The following variable is used to detect when the absolute value
        # of a number is close to zero.
    eps = 5e-15
        # The following Boolean is used to flag when only rotation
        # transformations have been used.  This then allows us to find the
        # rotation axis if desired.
    _rotations_only = True
        # The following object is used to convert numbers to strings.
    _sig = SigFig()
        # Only initialize ourself once
    _initialized = False
        # The _coord_sys string identifies the coordinate system to use to
        # display a geometric object in the __str__ method.  The value can
        # be "rect", "cyl", or "sph" for rectangular, cylindrical, and
        # spherical, respectively.
    _coord_sys = "rect"
        # _compass indicates that the polar angle theta should be measured
        # clockwise from the +y axis instead of the usual polar angle
        # measured counterclockwise from the +x axis.
    _compass = False
        # _elev indicates that the spherical angle phi should instead be
        # presented as the elevation above the xy plane.  Thus, this means
        # the complement of phi is given.  It will range from -pi/2 to
        # pi/2.
    _elev = False
        # _neg indicates that the angle should increase in the opposite
        # direction than is customary.  Thus, if True, for polar angles,
        # the azimuth angle should increase when moving clockwise.  For
        # compass angles, the azimuth should increase when moving
        # counterclockwise.  The variable has no effect on the spherical
        # phi angle.
    _neg = False
        # _suppress_z, if True, causes the z component of an object to be
        # suppressed in the __str__ method if the z component is zero.
        # Thus, the third coordinate (z in rect/cyl or phi in sph) will be
        # suppressed if the point lies in the xy plane.  The intent is to
        # let geometry problems in the plane look like two-dimensional
        # problems.
    _suppress_z = True
        # Multiply angles in radians by _angle to convert angles from
        # radians to the desired angular unit.  For example, to make
        # degrees the default angular measure, set this to 180/pi.
    _angle = 1
        # _angle_name is a string used to identify the angular unit.
    _angle_name = "rad"
        # If _eye is not None, then it must be a Point object and
        # projection is done using this point as the eye point, resulting
        # in projective transformations.  If None, then the projections
        # are done from infinity, resulting in orthogonal projections.
    _eye = None
        # The _stack variable holds a copy of the CTM for push and pop
        # operations.
    _stack = []
    def __init__(self):
        if not Ctm._initialized:
            # Note:  do not set sig.rtz to True, as you'll get
            # incorrect uncertainty number displays in short form.
            Ctm._sig.integer = 1
            Ctm._sig.digits = 4
            Ctm._sig.unc_short = True
            self.reset()
            Ctm._initialized = True
    def push(self, ctm=None):
        '''Push the current CTM onto the stack.  If ctm is not None,
        then use it as the new CTM.
        '''
        Ctm._stack.append(self.GetCTM())
        if ctm:
            assert(len(ctm) == 16)
            self.SetCTM(ctm)
    def pop(self):
        '''Pop the last-pushed CTM from the stack and set it as the
        current CTM.  Also return it.
        '''
        if not Ctm._stack:
            raise ValueError("Stack is empty")
        ctm = Ctm._stack.pop()
        self.SetCTM(ctm)
        return ctm
    def GetICTM(self):
        '''Returns the inverse of the CTM as an array of 16 numbers.
        '''
        # The equations were gotten from running Mathematica 4.1 on
        # the following file:
        #
        # A = {
        #     {a, b, c, d},
        #     {e, f, g, h},
        #     {i, j, k, l},
        #     {m, n, o, p}
        # };
        # FortranForm[Inverse[A]]
        #
        # Then D was substituted for the determinant expression in
        # each term.
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = self.GetCTM()
        D = (d*g*j*m - c*h*j*m - d*f*k*m + b*h*k*m + c*f*l*m - b*g*l*m -
             d*g*i*n + c*h*i*n + d*e*k*n - a*h*k*n - c*e*l*n + a*g*l*n +
             d*f*i*o - b*h*i*o - d*e*j*o + a*h*j*o + b*e*l*o - a*f*l*o -
             c*f*i*p + b*g*i*p + c*e*j*p - a*g*j*p - b*e*k*p + a*f*k*p)
        if not D:
            raise ValueError("Singular CTM")
        m = [
            # Row 0
            (-(h*k*n) + g*l*n + h*j*o - f*l*o - g*j*p + f*k*p)/D,
            (d*k*n - c*l*n - d*j*o + b*l*o + c*j*p - b*k*p)/D,
            (-(d*g*n) + c*h*n + d*f*o - b*h*o - c*f*p + b*g*p)/D,
            (d*g*j - c*h*j - d*f*k + b*h*k + c*f*l - b*g*l)/D,
            # Row 1
            (h*k*m - g*l*m - h*i*o + e*l*o + g*i*p - e*k*p)/D,
            (-(d*k*m) + c*l*m + d*i*o - a*l*o - c*i*p + a*k*p)/D,
            (d*g*m - c*h*m - d*e*o + a*h*o + c*e*p - a*g*p)/D,
            (-(d*g*i) + c*h*i + d*e*k - a*h*k - c*e*l + a*g*l)/D,
            # Row 2
            (-(h*j*m) + f*l*m + h*i*n - e*l*n - f*i*p + e*j*p)/D,
            (d*j*m - b*l*m - d*i*n + a*l*n + b*i*p - a*j*p)/D,
            (-(d*f*m) + b*h*m + d*e*n - a*h*n - b*e*p + a*f*p)/D,
            (d*f*i - b*h*i - d*e*j + a*h*j + b*e*l - a*f*l)/D,
            # Row 3
            (g*j*m - f*k*m - g*i*n + e*k*n + f*i*o - e*j*o)/D,
            (-(c*j*m) + b*k*m + c*i*n - a*k*n - b*i*o + a*j*o)/D,
            (c*f*m - b*g*m - c*e*n + a*g*n + b*e*o - a*f*o)/D,
            (-(c*f*i) + b*g*i + c*e*j - a*g*j - b*e*k + a*f*k)/D,
        ]
        Ctm._ICTM = m
        return m
    def GetCTM(self):
        '''Returns the CTM as an array of 16 numbers.
        '''
        return Ctm._CTM[:]  # Note it's a copy
    def SetCTM(self, ctm):
        '''This method is intended to be used to set the CTM from a
        a previous value.  ctm must be a sequence of 16 values.  One
        use might be e.g. for a push/pop functionality like that in
        PostScript.
        '''
        if len(ctm) != 16:
            raise ValueError("Need sequence of 16 numbers for CTM")
        Ctm._CTM = list(ctm[:])
        # Verify all the matrix elements are numbers
        allowed = [int, float, flt]
        if have_unc:
            allowed += [UFloat]
        allowed = tuple(allowed)
        for i, elem in enumerate(Ctm._CTM):
            if not ii(elem, allowed):
                raise ValueError("Unallowed type for CTM[%d]" % i)
        self._check_det()
    def __str__(self):
        s = "Ctm("
        f = "%s, %s, %s, %s"
        g = "    " + f
        s += (f % tuple([Ctm.sig(i) for i in Ctm._CTM[0:4]])) + ",\n"
        s += (g % tuple([Ctm.sig(i) for i in Ctm._CTM[4:8]])) + ",\n"
        s += (g % tuple([Ctm.sig(i) for i in Ctm._CTM[8:12]])) + ",\n"
        s += (g % tuple([Ctm.sig(i) for i in Ctm._CTM[12:]])) + ")"
        return s
    def rotate(self, theta, u):
        '''Rotate the current coordinate system about an axis defined
        by the vector u (a 3-tuple or a Line object) and the angle
        theta in radians.  A positive rotation angle is
        counterclockwise when the vector u is pointing into your eye.
        '''
        e = ValueError("u must be a 3-tuple or Line")
        if ii(u, Line):
            if u.is_zero:
                raise ValueError("Axis cannot be the zero line")
            ux, uy, uz = u.dc
        elif ii(u, (tuple, list)):
            if len(u) != 3:
                raise e
            U = hypot(u[0], hypot(u[1], u[2]))
            # Make u a unit vector
            ux, uy, uz = [i/U for i in u]
        else:
            raise e
        r = self.Rnd
        if r(ux) == 0 and r(uy) == 0 and r(uz) == 0:
            raise ValueError("u can't be zero vector")
        # Note:  as originally written, this transformation went from
        # the CCS to the DCS.  Since I've decided I want the
        # transformation to go the other way, the easiest way to
        # invert it is to change the sign of the rotation angle.
        theta = -theta
        c, s = cos(theta), sin(theta)
        h = 1 - c
        # Calculate the rotation matrix elements.  Formula from
        # http://en.wikipedia.org/wiki/Rotation_matrix.
        r00, r01, r02 = c + ux*ux*h, ux*uy*h - uz*s, ux*uz*h + uy*s
        r10, r11, r12 = ux*uy*h + uz*s, c + uy*uy*h, uy*uz*h - ux*s
        r20, r21, r22 = ux*uz*h - uy*s, uy*uz*h + ux*s, c + uz*uz*h
        # Multiply rotation matrix and CTM
        a, b, c, t, d, e, f, u, g, h, i, v, J, K, L, M = self.GetCTM()
        # Row 0
        Ctm._CTM[0] = self.Rnd(a*r00 + d*r01 + g*r02)
        Ctm._CTM[1] = self.Rnd(b*r00 + e*r01 + h*r02)
        Ctm._CTM[2] = self.Rnd(c*r00 + f*r01 + i*r02)
        Ctm._CTM[3] = self.Rnd(t*r00 + u*r01 + v*r02)
        # Row 1
        Ctm._CTM[4] = self.Rnd(a*r10 + d*r11 + g*r12)
        Ctm._CTM[5] = self.Rnd(b*r10 + e*r11 + h*r12)
        Ctm._CTM[6] = self.Rnd(c*r10 + f*r11 + i*r12)
        Ctm._CTM[7] = self.Rnd(t*r10 + u*r11 + v*r12)
        # Row 2
        Ctm._CTM[8] = self.Rnd(a*r20 + d*r21 + g*r22)
        Ctm._CTM[9] = self.Rnd(b*r20 + e*r21 + h*r22)
        Ctm._CTM[10] = self.Rnd(c*r20 + f*r21 + i*r22)
        Ctm._CTM[11] = self.Rnd(t*r20 + u*r21 + v*r22)
        # Row 3
        Ctm._CTM[12] = 0
        Ctm._CTM[13] = 0
        Ctm._CTM[14] = 0
        Ctm._CTM[15] = 1
        self.GetICTM()
        self.ToCCS()
        self._check_det()
    def translate(self, x, y, z):
        '''Translate the origin to (x, y, z).
        '''
        Ctm._CTM[3] -= x
        Ctm._CTM[7] -= y
        Ctm._CTM[11] -= z
        Ctm._rotations_only = False
        self.GetICTM()
        self.ToCCS()
        self._check_det()
    def scale(self, sx, sy, sz):
        '''A dilatation transformation.  You must ensure the three
        scale factors are numbers greater than zero.  If the scale
        factors are numbers with uncertainty, this takes a bit more
        care, as you can't simply use the comparison operators like
        ">" (i.e., random variables aren't ordered).
        '''
        # Row 0
        Ctm._CTM[0] *= sx
        Ctm._CTM[1] *= sx
        Ctm._CTM[2] *= sx
        Ctm._CTM[3] *= sx
        # Row 1
        Ctm._CTM[4] *= sy
        Ctm._CTM[5] *= sy
        Ctm._CTM[6] *= sy
        Ctm._CTM[7] *= sy
        # Row 2
        Ctm._CTM[8] *= sz
        Ctm._CTM[9] *= sz
        Ctm._CTM[10] *= sz
        Ctm._CTM[11] *= sz
        # Row 3
        Ctm._CTM[12] = 0
        Ctm._CTM[13] = 0
        Ctm._CTM[14] = 0
        Ctm._CTM[15] = 1
        Ctm._rotations_only = False
        self.GetICTM()
        self.ToCCS()
        self._check_det()
    def reset(self):
        '''Set the CTM and ICTM equal to the identity matrix.
        '''
        Ctm._CTM = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        Ctm._ICTM = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        Ctm._rotations_only = True
        Ctm._stack = []
    def ToCCS(self):
        '''Transform the default coordinates of this object into
        current coordinates.  This is an abstract method, as each
        geometrical object will supply its own code.  Uses the CTM.
        '''
        raise RuntimeError("Abstract method")
    def ToDCS(self):
        '''Transform the current coordinates of this object into
        default coordinates.  This is an abstract method, as each
        geometrical object will supply its own code.  Uses the CTM.
        '''
        raise RuntimeError("Abstract method")
    def _check_det(self):
        # Check the CTM's determinant; if it is near zero, print a
        # warning message.  We also save the value for when we need to
        # invert the matrix.
        msg = "%s:  CTM determinant is %s\n"
        self.det, eps = Det4(Ctm._CTM), 1e-15
        if not self.det:
            sys.stderr.write(msg % ("Error", " zero"))
        elif eps:
            if abs(self.det) < eps:
                sys.stderr.write(msg % ("Warning", " nearly singular"))
            if abs(self.det) < 100*eps:
                sys.stderr.write(msg % ("Warning", " small"))
    def sig(self, x):
        # This lets x values near an integer be converted to integers.
        C = ii(x, UFloat)
        if not C and abs(self.Rnd(x - int(x))) == 0:
            return str(int(x))
        else:
            return Ctm._sig(x)
    def Rnd(self, x):
        '''Check to see whether the absolute value of x is less than
        Ctm.eps; if it is, change x to zero.  Note this method handles
        numbers with uncertainties too:  if the standard deviation is
        greater than Ctm.eps and the mean is less, then the mean is
        set to zero (the standard deviation will not be changed).
        '''
        if not Ctm.eps:
            return x
        if have_unc and ii(x, UFloat):
            #if x.std_dev > Ctm.eps and abs(x.nominal_value) < Ctm.eps:
            mean, s = x.nominal_value, x.std_dev
            if mean and abs(s/mean) < Ctm.eps:
                x = ufloat(mean, 0)
            elif not mean and s < Ctm.eps:
                x = ufloat(mean, 0)
            elif abs(mean) < Ctm.eps:
                x = ufloat(0, s)
        elif ii(x, (float, flt, int)):
            if abs(x) < Ctm.eps:
                x = 0
            # Convert to integer if appropriate
            if abs(int(x) - x) < Ctm.eps:
                x = int(x)
        else:
            raise TypeError("Unsupported type")
        return x
    def xfm(self, matrix, point):
        '''Left-multiply the point (a length-3 sequence) by the 4x4
        matrix (a 16-element array) and return the resulting 3-tuple.
        Note this is really using homogenous coordinates (x, y, z, w)
        where w is 1, but we're ignoring the w term because the last
        row of the matrices we see will be [0, 0, 0, 1].
        '''
        if len(point) != 3:
            raise ValueError("point argument must be a length-3 sequence")
        if len(matrix) != 16:
            raise ValueError("matrix argument must be a length-16 sequence")
        x, y, z = point
        a, b, c, t, d, e, f, u, g, h, i, v, J, K, L, M = matrix
        x0 = a*x + b*y + c*z + t
        y0 = d*x + e*y + f*z + u
        z0 = g*x + h*y + i*z + v
        return (x0, y0, z0)
    def GetRotationAxis(self):
        '''Return a tuple of the angle of rotation in radians and a
        3-tuple vector that is the rotation axis.  The rotation is
        counterclockwise when the vector is pointing towards your eye.
        '''
        if not Ctm._rotations_only:
            raise ValueError("Transformations have not been pure rotations")
        # From pg 93 of AnalyticGeometry.pdf at
        # http://code.google.com/p/hobbyutil/, section "Direction
        # cosine matrix to Euler axis and angle" under Rotations
        # in the Miscellaneous chapter.
        (R11, R12, R13, t,
         R21, R22, R23, u,
         R31, R32, R33, v,
         J,   K,   L,   M) = self.GetCTM()
        # The angle of rotation is related to the trace of the
        # rotation matrix.
        theta = acos((R11 + R22 + R33 - 1)/2)
        a = 2*sin(theta)
        if not a:
            return (0, (0, 0, 0))
        # I added the leading - sign to each term because of
        # changing the sign of the angle in the Rotation method.
        x = -(R32 - R23)/a
        y = -(R13 - R31)/a
        z = -(R21 - R12)/a
        return (theta, (self.Rnd(x), self.Rnd(y), self.Rnd(z)))
class V(Ctm):
    '''Model a free vector in three-dimensional space using Cartesian
    coordinates and provide typical vector operations.  You can
    also get the cylindrical and spherical coordinates.  The
    definitions of these values are:
 
    Cylindrical:  rho is sqrt(x*x + y*y), theta is the usual
    polar angle in the xy plane from the +x axis measured
    counterclockwise, and z is the distance above the xy plane.
    Note that theta is on the interval [0, 2*pi).
 
    Spherical:  r is sqrt(x*x + y*y + z*z), theta is the same as the
    cylindrical theta, and phi is the angle off the +z axis.  Note
    that theta is on the half-open interval [0, 2*pi) and phi is on
    the closed interval [0, pi].
    '''
    def __init__(self, x, y=0, z=0):
        '''A vector can be initialized by:
            * Three numbers
            * A Point object
            * A 3-tuple
            * A Line object
            * Another vector
        '''
        Ctm.__init__(self)
        if ii(x, Numbers) and ii(y, Numbers) and ii(z, Numbers):
            self._p = Point(x, y, z)
        elif ii(x, Point):
            self._p = x
        elif ii(x, (tuple, list)):
            if len(x) != 3:
                raise ValueError("List or tuple must have 3 elements")
            self._p = Point(*x)
        elif ii(x, Line):
            x1, y1, z1 = x.p.rect
            x2, y2, z2 = x.q.rect
            self._p = Point(x2 - x1, y2 - y1, z2 - z1)
        elif ii(x, V):
            self._p = x._p.copy
        else:
            msg = "Init with 3 numbers, point, 3-tuple, line, or vector"
            raise ValueError(msg)
    def ToCCS(self):
        '''Calculate and return the vector's coordinates in the current
        coordinate system.
        '''
        return self._p.ToCCS()
    def ToDCS(self):
        '''Calculate and return the point's coordinates in the default
        coordinate system.
        '''
        return self._p.ToDCS()
    def __str__(self):
        s = "V(%s, %s, %s)" % tuple([self.sig(i) for i in self._p.rect])
        return s
    def dist(self, other):
        '''Calculate the distance between this vector's point and
        another vector's point.
        '''
        if not ii(other, V):
            raise TypeError("other must be a vector")
        x1, y1, z1 = self._p.ToCCS()
        x2, y2, z2 = other._p.ToCCS()
        return hypot(x1 - x2, hypot(y1 - y2, z1 - z2))
    def __neg__(self):
        x, y, z = self.ToCCS()
        return V(-x, -y, -z)
    def __ne__(self, other):
        return not (self == other)
    def __eq__(self, other):
        if not ii(other, V):
            raise TypeError("other needs to be a vector")
        return self._p == other._p
    def __add__(self, other):
        if not ii(other, V):
            raise TypeError("other needs to be a vector")
        x1, y1, z1 = self._p.ToCCS()
        x2, y2, z2 = other._p.ToCCS()
        return V(x1 + x2, y1 + y2, z1 + z2)
    def __radd__(self, other):
        if not ii(other, V):
            raise TypeError("other needs to be a vector")
        return self.__add__(other)
    def __sub__(self, other):
        if not ii(other, V):
            raise TypeError("other needs to be a vector")
        x1, y1, z1 = self._p.ToCCS()
        x2, y2, z2 = other._p.ToCCS()
        return V(x1 - x2, y1 - y2, z1 - z2)
    def __rsub__(self, other):
        if not ii(other, V):
            raise TypeError("other needs to be a vector")
        return other.__sub__(self)
    def __mul__(self, a):
        '''Multiplication by a scalar a.
        '''
        if not ii(a, Numbers):
            raise TypeError("a needs to be a scalar")
        x, y, z = self._p.ToCCS()
        return V(a*x, a*y, a*z)
    def __rmul__(self, a):
        if not ii(a, Numbers):
            raise TypeError("a needs to be a scalar")
        return self.__mul__(a)
    def dot(self, other):
        '''Dot product.
        '''
        if not ii(other, V):
            raise TypeError("other needs to be a vector")
        x1, y1, z1 = self._p.ToCCS()
        x2, y2, z2 = other._p.ToCCS()
        return x1*x2 + y1*y2 + z1*z2
    def cross(self, other):
        '''Return cross product of self X other.
        '''
        if not ii(other, V):
            raise TypeError("other needs to be a vector")
        ax, ay, az = self._p.ToCCS()
        bx, by, bz = other._p.ToCCS()
        return V(ay*bz - az*by, az*bx - ax*bz, ax*by - ay*bx)
    def normalize(self):
        '''Normalize this vector's magnitude to unity.
        '''
        self._p = Point(*self.dc)
        return self
    def STP(self, other1, other2):
        '''Scalar triple product.
        '''
        if not ii(other1, V):
            raise TypeError("other1 needs to be a vector")
        if not ii(other2, V):
            raise TypeError("other2 needs to be a vector")
        return self.dot(other1.cross(other2))
    def VTP(self, other1, other2):
        '''Vector triple product.
        '''
        if not ii(other1, V):
            raise TypeError("other1 needs to be a vector")
        if not ii(other2, V):
            raise TypeError("other2 needs to be a vector")
        return self.cross(other1.cross(other2))
    @property
    def copy(self):
        return V(*self.ToCCS())
    @property
    def mag(self):
        '''Return the vector's magnitude.
        '''
        return sqrt(self.dot(self))
    @property
    def rect(self):
        '''Return a 3-tuple of the vector's rectangular coordinates
        in the current coordinate system.
        '''
        return self.ToCCS()
    @property
    def cyl(self):
        '''Return a 3-tuple of the vector's cylindrical coordinates
        in the current coordinate system.
        '''
        return self._p.cyl
    @property
    def sph(self):
        '''Return a 3-tuple of the vector's spherical coordinates in
        the current coordinate system.
        '''
        return self._p.sph
    @property
    def dc(self):
        '''Return a 3-tuple of the direction cosines of the vector in
        the current coordinate system.
        '''
        x, y, z = self._p.ToCCS()
        if self.Rnd(x) == 0 and self.Rnd(y) == 0 and self.Rnd(z) == 0:
            raise ValueError("No direction cosines for zero vector")
        L = hypot(x, hypot(y, z))
        return (x/L, y/L, z/L)
    @property
    def u(self):
        '''Return a unit vector object in the same direction as this
        vector.
        '''
        return V(*self.dc)
    @property
    def x(self):
        '''Return the x coordinate in current coordinates.
        '''
        return self.rect[0]
    @property
    def y(self):
        '''Return the y coordinate in current coordinates.
        '''
        return self.rect[1]
    @property
    def z(self):
        '''Return the z coordinate in current coordinates.
        '''
        return self.rect[2]
    @property
    def rho(self):
        '''Return the rho cylindrical coordinate in current coordinates.
        '''
        return self.cyl[0]
    @property
    def theta(self):
        '''Return the theta cylindrical coordinate in current coordinates.
        '''
        return self.cyl[1]
    @property
    def r(self):
        '''Return the r spherical coordinate in current coordinates.
        '''
        return self.sph[0]
    @property
    def phi(self):
        '''Return the phi spherical coordinate in current coordinates.
        '''
        return self.sph[2]
class Point(Ctm):
    '''Model a point in three-dimensional space using Cartesian
    coordinates.  The point can also have an object m associated with
    it; m is intended to be a mass to help with calculating a
    centroid, but syntactically it can be any object, as it is only
    assigned to the self.m attribute.
 
    DCS means default coordinate system, CCS means current
    coordinate system.
    '''
    def __init__(self, x=0, y=0, z=0, m=None):
        '''x, y, and z are Cartesian coordinates defining this point
        in the current coordinate system.  m is an object associated
        with the point; it was intended to be a mass, but m can be any
        object.
 
        Besides x being a number, it can be a 3-tuple containing the
        Cartesian coordinates, another Point object, or a vector V.
        '''
        Ctm.__init__(self)
        if ii(x, (list, tuple)):
            if len(x) != 3:
                raise ValueError("x sequence wrong length")
            self._r, self.m = x, m
        elif ii(x, Point):
            o = x.copy
            self._r = o._r
            try:
                self.m = o.m.copy
            except AttributeError:
                # Just use a reference
                self.m = o.m
        elif ii(x, V):
            self._r, self.m = x.rect, m
        else:
            self._r, self.m = (x, y, z), m
        # x, y, and z are in the current coordinate system.  Use the
        # inverse CTM to transform them back to default coordinates.
        self._r0 = self.xfm(self.GetICTM(), self._r)
    def ToCCS(self):
        '''Calculate and return the point's coordinates in the current
        coordinate system.
        '''
        r = tuple([self.Rnd(i) for i in self.xfm(self.GetCTM(), self._r0)])
        self._r = r
        return r
    def ToDCS(self):
        '''Calculate and return the point's coordinates in the default
        coordinate system.
        '''
        r = tuple([self.Rnd(i) for i in self.xfm(self.GetICTM(), self._r)])
        self._r0 = r
        return r
    def __str__(self, no2d=False):
        '''String representation of a Point object.  If no2d is True,
        always use three coordinates in the representation.
        '''
        def AdjustTheta(theta):
            # To calculate the compass mode angle, subtract the normal
            # polar angle from pi/2.  A sketch of angles in the four
            # quadrants and reducing the expressions will show that
            # this works for any quadrant.  If the angle is negative,
            # add 2*pi so that we always have theta on [0, 2*pi).
            if Ctm._compass:
                theta = pi/2 - theta
                if theta < 0:
                    theta = R(theta + 2*pi)
            if Ctm._neg:
                theta = R(2*pi - theta)
            if theta == 2*pi:
                theta = 0
            assert 0 <= theta < 2*pi
            return theta
        x, y, z = self.ToCCS()
        R, M = self.Rnd, ""
        if not R(x) and not R(y) and not R(z):
            return "Origin"
        if self.m is not None:
            # M will contain the string representation of the mass
            # object
            try:
                M = "m=%s" % self.sig(self.m)
            except Exception:
                M = "m=%s" % str(self.m)
        # Encode the settings into an ASCII string
        S = " "
        if Ctm._compass:
            S += "C"
        if Ctm._elev:
            S += "E"
        if Ctm._angle_name == "deg":
            S += "\xb0" if _use_unicode else "o"
        elif Ctm._angle_name == "rev":
            S += "V"
        elif Ctm._angle_name == "rad":
            pass
        else:
            S += " S"
        S += "-" if Ctm._neg else ""
        if not S.strip():
            S = ""
        if Ctm._coord_sys == "rect":
            s = "Pt(%s, %s" % (self.sig(x), self.sig(y))
            if no2d or not Ctm._suppress_z or (Ctm._suppress_z and R(z) != 0):
                s += ", %s" % self.sig(z)
            if M:
                s += ", %s" % M         # Add mass
            s += ")"
            return s
        elif Ctm._coord_sys == "cyl":
            rho, theta, z = self.cyl
            s = "Pt<%s, %s" % (self.sig(rho), self.sig(theta))
            # If not suppressing the third coordinate, add it to the
            # string s.
            is_xy = (R(z) == 0)
            if not is_xy or no2d or not Ctm._suppress_z:
                s += ", %s" % self.sig(z)
            if M:
                s += ", %s" % M         # Add mass
            s += "%s>" % S
            return s
        elif Ctm._coord_sys == "sph":
            r, theta, phi = self.sph
            s = "Pt<<%s, %s" % (self.sig(r), self.sig(theta))
            # If not suppressing the third coordinate, add it to the
            # string s.
            C1 = Ctm._elev and not R(phi)
            C2 = not Ctm._elev and R(phi - pi/2) == 0
            is_xy = (C1 or C2)
            if not is_xy or no2d or not Ctm._suppress_z:
                s += ", %s" % self.sig(R(phi))
            if M:
                s += ", %s" % M         # Add mass
            s += "%s>>" % S
            return s
        else:
            raise ValueError("Bad Ctm._coord_sys class variable")
    def dist(self, other):
        '''Calculate the distance between this point and another
        object.  To lines and planes, the distance is the
        perpendicular distance and it will always be positive.
        '''
        if ii(other, Point):
            # Need coordinates in current coordinate system
            x1, y1, z1 = self.ToCCS()
            x2, y2, z2 = other.ToCCS()
            return abs(self.Rnd(hypot(hypot(x1 - x2, y1 - y2), z1 - z2)))
        elif ii(other, Line):
            return other.dist(self)
        elif ii(other, Plane):
            return other.dist(self)
        else:
            raise TypeError("other must be a point, line, or plane")
    def locate(self, point):
        '''Set point self._r to point.p.
        '''
        if not ii(point, (Point, Line, Plane)):
            msg = "The other object needs to be a point, line, or plane"
            raise TypeError(msg)
        if ii(point, Point):
            self._r = point.rect
        else:
            self._r = point.p.rect
        self.ToDCS()
    def __neg__(self):
        '''The unary negation of a point means to negate its coordinates.
        This is equivalent to the scaling transformation where sx, sy,
        and sz are -1.
        '''
        x, y, z = self.ToCCS()
        return Point(-x, -y, -z)
    def __ne__(self, other):
        return not (self == other)
    def __eq__(self, other):
        if not ii(other, Point):
            raise TypeError("The other object needs to be a point")
        x1, y1, z1 = self.ToCCS()
        x2, y2, z2 = other.ToCCS()
        R = self.Rnd
        # The two corresponding points have to match
        if R(x1 - x2) == 0 and R(y1 - y2) == 0 and R(z1 - z2) == 0:
            return True
        return False
    def __abs__(self):
        '''Return the magnitude of the unit vector.
        '''
        return abs(Line(Point(0, 0, 0), Point(self.rect)))
    def __add__(self, other):
        if not ii(other, (Point, Line, Plane)):
            msg = "The other object needs to be a point, line, or plane"
            raise TypeError(msg)
        ln = Line(Point(0, 0, 0), Point(self.rect))
        if ii(other, Point):
            other = Line(Point(0, 0, 0), Point(other.rect))
        return ln + other
    def __sub__(self, other):
        return self + (-other)
    def __mul__(self, other):
        if not ii(other, Numbers):
            raise TypeError("The other object needs to be a number")
        return Point([i*other for i in self.rect])
    def __rmul__(self, other):
        return self*other
    def __div__(self, other):
        if not ii(other, Numbers):
            raise TypeError("The other object needs to be a number")
        return self*(1/other)
    def __truediv__(self, other):
        return self.__div__(other)
    def AreCollinear(self, other1, other2):
        '''Return True if the three points are collinear.
        '''
        # [an] p 77
        r1, r2, r3 = V(self.rect), V(other1.rect), V(other2.rect)
        x, y, z = (r2 - r1).cross(r2 - r3).rect
        return self.Rnd(x) == 0 and self.Rnd(y) == 0 and self.Rnd(z) == 0
    def intersect(self, other):
        '''Return the intersection if this point intersects the other
        object; otherwise, return None.
        '''
        if ii(other, Point):
            return self if self == other else None
        elif ii(other, Line):
            return self._intersects_line(other)
        elif ii(other, Plane):
            return other.intersect(self)
        else:
            raise TypeError("other must be a point, line, or plane")
    def dot(self, other):
        '''Consider ourselves a position vector.  Dot with the vector
        that the other object represents.
        '''
        if not ii(other, (Point, Line, Plane)):
            raise TypeError("other must be a Point, Line, or Plane object")
        v1 = V(self.rect)
        if ii(other, Point):
            v2 = V(other.rect)
        else:
            p, q = V(other.p), V(other.q)
            v2 = q - p
        return v1.dot(v2)
    def cross(self, other):
        '''Consider ourselves a position vector.  Cross with the vector
        that the other object represents.
        '''
        if not ii(other, (Point, Line, Plane)):
            raise TypeError("other must be a Point, Line, or Plane object")
        v1 = V(self.rect)
        if ii(other, Point):
            v2 = V(other.rect)
        else:
            p, q = V(other.p), V(other.q)
            v2 = q - p
        c = v1.cross(v2)
        return Line(Point(0, 0, 0), Point(c))
    def ConvertTheta(self, ang):
        '''ang is an angle.  Convert it using the state of the
        Ctm._neg and Ctm._compass flags.  Note that this function is
        an involution (i.e., it is its own inverse).  ang is in
        radians and the returned value is in radians.
        '''
        def pos(ang):
            return ang if ang >= 0 else ang + 2*pi
        if Ctm._compass:
            ang = pos(pi/2 - ang)
        if Ctm._neg:
            ang = pos(-ang)
        return ang
    def ConvertPhi(self, ang):
        '''ang is a canonical phi angle in radians.  Convert it using
        the state of the Ctm._elev flag and return it, leaving it in
        radians.
        '''
        def pos(ang):
            return ang if ang >= 0 else ang + 2*pi
        if Ctm._elev:
            ang = pi/2 - ang
        return ang
    def _intersects_line(self, line):
        '''Check to see if the point satisfies the parametric
        equation of the line.
        '''
        # The parametric equation of the line is r = r1 + t*(r2 - r1)
        # where r1 and r2 are the two position vectors of the
        # points on the line.
        x0, y0, z0 = self.rect
        x1, y1, z1 = line.p.rect
        x2, y2, z2 = line.q.rect
        r = self.Rnd
        # Solve for the parameter t
        if r(x2 - x1) == 0 and r(y2 - y1) == 0 and r(z2 - z1) == 0:
            # Swap x1 and x2
            x1, y1, z1 = x2, y2, z2
        if r(x2 - x1):
            t = (x0 - x1)/(x2 - x1)
        elif r(y2 - y1):
            t = (y0 - y1)/(y2 - y1)
        elif r(z2 - z1):
            t = (z0 - z1)/(z2 - z1)
        else:
            raise ValueError("Both p and q (nearly) at origin")
        # Check that t solves each equation
        C1 = r(t*(x2 - x1) + x1 - x0) == 0
        C2 = r(t*(y2 - y1) + y1 - y0) == 0
        C3 = r(t*(z2 - z1) + z1 - z0) == 0
        return self if C1 and C2 and C3 else None
    def _get_azimuth(self, x, y):
        '''The cylindrical theta coordinate is typically given as
        the result of an atan2() call; this results in the range
        being (-pi, pi].  I've decided instead that I'd prefer
        the polar azimuth range on [0, 2*pi) instead.  If you
        don't like this choice, you can fix it in this function.
         
        Note theta is returned in radians.
        '''
        theta = atan2(y, x)
        if theta < 0:
            theta += 2*pi
        if theta == 2*pi:
            # This can happen with e.g. atan2(1/a, a) where a = -1e8
            theta = 0
        assert 0 <= theta < 2*pi
        return self.Rnd(theta)
    def _cyl(self):
        '''Return canonical cylindrical coordinates in radians with no
        conversions of angle units.
        '''
        x, y, z = self.ToCCS()
        R = self.Rnd
        try:
            rho = R(hypot(x, y))
        except ZeroDivisionError:
            # This will occur if x and y are both zero and they're
            # uncertainty ufloats because umath tries to calculate the
            # derivative of hypot.
            s = 0
            if ii(x, UFloat):
                s = max(s, x.std_dev)
            if ii(y, UFloat):
                s = max(s, y.std_dev)
            if s:
                rho = ufloat(0, s)
            else:
                rho = 0
        if ii(rho, UFloat):
            threshold = rho.nominal_value
        else:
            threshold = rho
        theta = self._get_azimuth(x, y) if threshold else 0
        return (rho, theta, z)
    def _sph(self):
        '''Return canonical spherical coordinates in radians with no
        conversions of angle units.
        '''
        x, y, z = self.ToCCS()
        rho, theta, z = self._cyl()
        R = self.Rnd
        try:
            r = R(hypot(rho, z))
        except ZeroDivisionError:
            # This will occur if rho and z are both zero and they're
            # uncertainty ufloats because umath tries to calculate the
            # derivative of hypot.
            s = 0
            if ii(rho, UFloat):
                s = max(s, rho.std_dev)
            if ii(z, UFloat):
                s = max(s, z.std_dev)
            if s:
                r = ufloat(0, s)
            else:
                r = 0
        phi = atan2(rho, z)
        return (R(r), R(theta), R(phi))
    # Properties
    @property
    def copy(self):
        x, y, z = self.ToCCS()
        p = Point(x, y, z)
        # Since numbers are immutable, these won't hold references
        p._r = self._r
        p._r0 = self._r0
        try:
            p.m = self.m.copy()
        except AttributeError:
            # Just use a reference
            p.m = self.m
        return p
    @property
    def proj_ang(self):
        '''Return the two projection angles of the position vector of
        the point.  These are the projections of that vector onto the
        xz and yz planes and are the angles measured with respect to
        the +x and +y directions.
        '''
        x, y, z = self.rect
        A, B = atan2(z, x), atan2(z, y)
        return (self.Rnd(A), self.Rnd(B))
    @property
    def dc(self):
        '''Returns the direction cosines for the point considered as a
        position vector.
        '''
        R = self.Rnd
        x, y, z = self.rect
        if R(x) == 0 and R(y) == 0 and R(z) == 0:
            return (0, 0, 0)
        m = hypot(x, hypot(y, z))
        return (R(x/m), R(y/m), R(z/m))
    @property
    def rect(self):
        return self.ToCCS()
    @property
    def rec(self):
        return self.ToCCS()
    @property
    def xyz(self):
        return self.ToCCS()
    @property
    def cyl(self):
        '''Note that Ctm._compass, Ctm._neg, and Ctm._elev will be
        honored in the return values.  Also, the returned angles will
        be in the units indicated by Ctm._angle.
        '''
        rho, theta, z = self._cyl()
        R = self.Rnd
        # Convert theta to current angle measurement flavor in current
        # angular units.
        theta = R(Ctm._angle*self.ConvertTheta(theta))
        return (rho, theta, z)
    @property
    def sph(self):
        '''Note that Ctm._compass, Ctm._neg, and Ctm._elev will be
        honored in the return values.  Also, the returned angles will
        be in the units indicated by Ctm._angle.
        '''
        r, theta, phi = self._sph()
        R = self.Rnd
        # Convert angles to requisite values
        phi = (pi/2 - phi if Ctm._elev else phi)*Ctm._angle
        theta = Ctm._angle*self.ConvertTheta(theta)
        return (R(r), R(theta), R(phi))
    def _get_x(self):
        x, y, z = self.ToCCS()
        return x
    def _set_x(self, x):
        if not ii(x, Numbers):
            raise TypeError("Argument must be a number")
        self.ToCCS()
        dummy, y, z = self._r
        self._r = (self.Rnd(x), y, z)
        self.ToDCS()  # Propagates change back to self._r0
    def _get_y(self):
        x, y, z = self.ToCCS()
        return y
    def _set_y(self, y):
        if not ii(y, Numbers):
            raise TypeError("Argument must be a number")
        self.ToCCS()
        x, dummy, z = self._r
        self._r = (x, self.Rnd(y), z)
        self.ToDCS()  # Propagates change back to self._r0
    def _get_z(self):
        x, y, z = self.ToCCS()
        return z
    def _set_z(self, z):
        if not ii(z, Numbers):
            raise TypeError("Argument must be a number")
        self.ToCCS()
        x, y, dummy = self._r
        self._r = (x, y, self.Rnd(z))
        self.ToDCS()  # Propagates change back to self._r0
    def _get_rho(self):
        return self.cyl[0]
    def _set_rho(self, val):
        if not ii(val, Numbers):
            raise TypeError("Argument must be a number")
        rho, theta, z = self.cyl
        R = self.Rnd
        e = ValueError("Argument must >= 0")
        if ii(val, UFloat):
            if val.nominal_value < 0:
                raise e
        else:
            if val < 0:
                raise e
        x, y = R(val*cos(theta/Ctm._angle)), R(val*sin(theta/Ctm._angle))
        self._r = (x, y, z)
        self.ToDCS()  # Propagates change back to self._r0
    def _get_r(self):
        return self.sph[0]
    def _set_r(self, val):
        if not ii(val, Numbers):
            raise TypeError("Argument must be a number")
        r, theta, phi = self.sph
        # Convert angles to radians.  Also convert theta to the
        # customary polar angle.
        theta = self.ConvertTheta(theta/Ctm._angle)
        phi /= Ctm._angle
        # Convert phi if elevation mode is on
        if Ctm._elev:
            phi -= pi/2
        R = self.Rnd
        e = ValueError("Argument must >= 0")
        if ii(val, UFloat) and val.nominal_value < 0:
            raise e
        else:
            if val < 0:
                raise e
        rho = val*sin(phi)
        x, y, z = R(rho*cos(theta)), R(rho*sin(theta)), R(val*cos(phi))
        self._r = (x, y, z)
        self.ToDCS()  # Propagates change back to self._r0
    def _get_theta(self):
        return self.cyl[1]
    def _set_theta(self, val):
        if not ii(val, Numbers):
            raise TypeError("Argument must be a number")
        rho, theta, z = self.cyl
        # Convert theta to radians and have it be the customary polar
        # angle.
        theta = self.ConvertTheta(val/Ctm._angle)
        R = self.Rnd
        theta = fmod(theta, 2*pi)
        x, y = R(rho*cos(theta)), R(rho*sin(theta))
        self._r = (x, y, z)
        self.ToDCS()  # Propagates change back to self._r0
    def _get_phi(self):
        return self.sph[2]
    def _set_phi(self, val):
        if not ii(val, Numbers):
            raise TypeError("Argument must be a number")
        r, theta, phi = self.sph
        R = self.Rnd
        e = ValueError("Argument must >= 0")
        if ii(val, UFloat):
            if val.nominal_value < 0:
                raise e
        else:
            if val < 0:
                raise e
        # Convert val to radians
        val /= Ctm._angle
        if Ctm._elev:
            # It's psi; convert to complement phi
            val = pi/2 - val
        phi = fmod(val, pi)
        rho = r*sin(phi)
        x, y, z = R(rho*cos(theta)), R(rho*sin(theta)), R(r*cos(phi))
        self._r = (x, y, z)
        self.ToDCS()  # Propagates change back to self._r0
    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)
    z = property(_get_z, _set_z)
    rho = property(_get_rho, _set_rho)
    r = property(_get_r, _set_r)
    theta = property(_get_theta, _set_theta)
    phi = property(_get_phi, _set_phi)
class Line(Ctm):
    '''Model a line in three-dimensional space using Cartesian
    coordinates.  Internally, the line is modeled by two points.  Each
    line can be regarded as a line segment composed of these two
    points.  This gives each Line object a magnitude, direction, and
    attached to a point in space, thus making it a bound vector.  The
    tail of the vector is the point p and the tip of the vector is the
    point q.
    '''
    def __init__(self, p, q):
        '''Two points p and q determine the line.  q can also be a
        3-tuple of direction numbers; the line goes through point p
        and will have unit length.  Similarly, q can be a Line
        object that supplies the direction; this also results in a
        line with unit length.
        '''
        Ctm.__init__(self)
        self.is_zero = False
        if not ii(p, Point):
            raise ValueError("p must be a point")
        if ii(q, Point):
            # Note we need to allow for the case of the zero vector.
            # This can happen e.g. when a vector is crossed into
            # itself.
            if p == q:
                self.is_zero = True
            self._p, self._q = p, q
        elif ii(q, (tuple, list)):
            if len(q) != 3:
                raise ValueError(msg)
            if tuple(q) == (0, 0, 0):
                raise ValueError("Not all direction numbers can be zero")
            a, b, c = q
            D = sqrt(a*a + b*b + c*c)
            # Convert to direction cosines
            if D:
                a, b, c = tuple([i/D for i in (a, b, c)])
                # Get second point
                x, y, z = p.rect
                pt2 = Point(x + a, y + b, z + c)
                self._p, self._q = p, pt2
                if self._p == self._q:
                    self.is_zero = True
            else:
                self._p, self._q = Point(0, 0, 0), Point(0, 0, 0)
                self.is_zero = True
        elif ii(q, Line):
            if q.is_zero:
                self._p, self._q = Point(0, 0, 0), Point(0, 0, 0)
            else:
                nx, ny, nz = q.dc
                x1, y1, z1 = p.rect
                x2, y2, z2 = x1 + nx, y1 + ny, z1 + nz
                self._p, self._q = p, Point(x2, y2, z2)
        else:
            raise ValueError("q must be a point, 3-tuple, or Line")
    def ToCCS(self):
        '''Calculate and return the point p's coordinates in the current
        coordinate system.
        '''
        self.q.ToCCS()
        return self.p.ToCCS()
    def ToDCS(self):
        '''Calculate and return the point p's coordinates in the default
        coordinate system.
        '''
        self.q.ToDCS()
        return self.p.ToDCS()
    def __str__(self, no2d=False):
        '''String representation of a Line object.
        '''
        self.ToCCS()
        no2d = True if self.p.z != 0 or self.q.z != 0 else False
        sp = self.p.__str__(no2d)
        sq = self.q.__str__(no2d)
        return "Ln(%s, %s)" % (sp, sq)
    def __neg__(self):
        '''The unary negation of a line means change its direction by
        180 degrees.  This is done by exchanging the two points
        defining the line.
        '''
        o = self.copy
        o._p, o._q = o._q, o._p
        return o
    def __ne__(self, other):
        return not (self == other)
    def __eq__(self, other):
        if not ii(other, Line):
            raise TypeError("The other object needs to be a line")
        sx1, sy1, sz1 = self.p.ToCCS()
        sx2, sy2, sz2 = self.q.ToCCS()
        if IsUncertainty((sx1, sy1, sz1, sx2, sy2, sz2)):
            msg = "One or more of the components is an uncertainty number"
            raise ValueError(msg)
        ox1, oy1, oz1 = other.p.ToCCS()
        ox2, oy2, oz2 = other.q.ToCCS()
        if IsUncertainty((ox1, oy1, oz1, ox2, oy2, oz2)):
            msg = "One or more of the components is an uncertainty number"
            raise ValueError(msg)
        r = self.Rnd
        # The two corresponding points have to match
        C1 = r(sx1 - ox1) == 0 and r(sy1 - oy1) == 0 and r(sz1 - oz1) == 0
        C2 = r(sx2 - ox2) == 0 and r(sy2 - oy2) == 0 and r(sz2 - oz2) == 0
        if C1 and C2:
            return True
        return False
    def __abs__(self):
        return self.p.dist(self.q)
    def __add__(self, other):
        '''Note that addition and subtraction can also be with a
        Plane, since it inherits from a line object.  Because we want
        to be able to create new planes from adding vectors in
        expressions like 'i + xz', we want the result of addition with
        a Plane to be another Plane, as this seems the most useful.
        '''
        if not ii(other, (Point, Line, Plane)):
            msg = "The other object needs to be a point, line, or plane"
            raise TypeError(msg)
        conv = True if ii(other, Plane) else False
        if ii(other, Point):
            other = Line(Point(0, 0, 0), other.p)
        # This is vector addition
        p1, q1 = V(self.p), V(self.q)
        p2, q2 = V(other.p), V(other.q)
        r1, r2 = q1 - p1, q2 - p2
        r = r1 + r2
        if conv:
            return Plane(Point(0, 0, 0), Point(r))
        else:
            return Line(Point(0, 0, 0), Point(r))
    def __sub__(self, other):
        if not ii(other, (Line, Plane)):
            raise TypeError("The other object needs to be a line")
        # This is vector subtraction
        p1, q1 = V(self.p), V(self.q)
        p2, q2 = V(other.p), V(other.q)
        r1, r2 = q1 - p1, q2 - p2
        r = r1 - r2
        return Line(Point(0, 0, 0), Point(r))
    def __mul__(self, other):
        if not ii(other, Numbers):
            raise TypeError("The other object needs to be a number")
        p, q = V(self.p)*other, V(self.q)*other
        return Line(Point(p), Point(q))
    def __rmul__(self, other):
        return self*other
    def __div__(self, other):
        if not ii(other, Numbers):
            raise TypeError("The other object needs to be a number")
        return self*(1/other)
    def __truediv__(self, other):
        return self.__div__(other)
    def locate(self, point):
        '''Set point self.p to the given point and adjust self.q so
        that the line still points in the same direction.  Note point
        can be a Point, Line, or Plane (the p point is taken if it's a
        line or plane).
        '''
        if not ii(point, (Point, Line, Plane)):
            msg = "The other object needs to be a point, line, or plane"
            raise TypeError(msg)
        a, b, c = self.dc   # Get our direction
        L = self.L          # Save our length
        if ii(point, Point):
            self._p = point
        else:
            self._p = point.p
        x, y, z = self.p.rect
        self._q = Point(x + L*a, y + L*b, z + L*c)
    def intersect(self, other):
        '''Return the intersection if this line intersects the other
        object; otherwise, return None.
        '''
        if self.is_zero:
            return None
        elif ii(other, Point):
            return other.intersect(self)
        elif ii(other, Plane):
            # Note we must check for a Plane first, as a Plane will
            # also be an instance of a line.
            return other.intersect(self)
        elif ii(other, Line):
            if self == other:
                return self
            # Find the intersection point.  The method is to solve for
            # the parameters in the parametric equations that yield
            # the desired intersection point.  See
            # http://mathforum.org/library/drmath/view/63719.html.
            n1x, n1y, n1z = self.dc
            n2x, n2y, n2z = other.dc
            x1, y1, z1 = self.p.rect
            x2, y2, z2 = other.p.rect
            # In the following, the solutions were gotten using
            # Mathematica:
            # f = x1 + t*n1x - x2 - s*n2x;
            # g = y1 + t*n1y - y2 - s*n2y;
            # h = z1 + t*n1z - z2 - s*n2z;
            # FortranForm[Solve[{f==0, g==0}, {s, t}]]
            Dxy = n1y*n2x - n1x*n2y
            Dxz = n1z*n2x - n1x*n2z
            Dyz = n1z*n2y - n1y*n2z
            if Dxy:
                s = -(-(n1y*x1) + n1y*x2 + n1x*y1 - n1x*y2)/Dxy
                t = -(-(n2y*x1) + n2y*x2 + n2x*y1 - n2x*y2)/Dxy
            elif Dxz:
                s = -(-(n1z*x1) + n1z*x2 + n1x*z1 - n1x*z2)/Dxz
                t = -(-(n2z*x1) + n2z*x2 + n2x*z1 - n2x*z2)/Dxz
            elif Dyz:
                s = -(-(n1z*y1) + n1z*y2 + n1y*z1 - n1y*z2)/Dyz
                t = -(-(n2z*y1) + n2z*y2 + n2y*z1 - n2y*z2)/Dyz
            else:
                # Lines don't intersect
                return None
            x = x1 + t*n1x
            y = y1 + t*n1y
            z = z1 + t*n1z
            return Point(x, y, z)
        else:
            raise TypeError("other must be a point, line, or plane")
    def dist(self, other):
        '''Calculate the distance between this line and another
        object.  To lines and planes, the distance is the
        perpendicular distance and it will always be positive.
        '''
        if self.is_zero:
            raise ValueError("Is the zero vector")
        elif ii(other, Point):
            # http://mathforum.org/dr.math/faq/formulas/faq.ag3.html
            # Also Corral, Vector Calculus, pg 33.
            x1, y1, z1 = self.p.rect   # Any point on the line
            x2, y2, z2 = other.rect
            a, b, c = self.dc
            mu = V(a, b, c)
            numer = ((c*(y2-y1)-b*(z2-z1))**2 +
                     (a*(z2-z1)-c*(x2-x1))**2 +
                     (b*(x2-x1)-a*(y2-y1))**2)
            denom = mu.dot(mu)
            return self.Rnd(sqrt(abs(numer/denom)))
        elif ii(other, Plane):
            # Note we must check for a Plane first, as a Plane will
            # also be an instance of a line.
            return other.dist(self)
        elif ii(other, Line):
            # These formulas are from
            # http://pages.pacificcoast.net/~cazelais/251/distance.pdf.
            r1 = V(self.p.rect)   # Point on the first line
            r2 = V(other.p.rect)  # Point on the second line
            r = r2 - r1
            # Direction cosine unit vectors (point along the lines)
            mu1, mu2 = V(self.dc), V(other.dc)
            n = mu1.cross(mu2)  # Unit vector perp to both lines
            if self.Rnd(mu1.cross(mu2).mag) == 0:
                dist = r.cross(mu1).mag   # Parallel lines
            else:
                dist = r.dot(n)  # Skew lines (may intersect)
            return self.Rnd(abs(dist))
        else:
            raise TypeError("other must be a point, line, or plane")
    def dot(self, other):
        '''Consider the line from p to q a vector.  Return the dot
        product of these two vectors.
        '''
        if self.is_zero:
            return 0
        if not ii(other, (Point, Line, Plane)):
            raise TypeError("other must be a Point, Line, or Plane object")
        r1 = V(self.q) - V(self.p)  # The vector self is
        if ii(other, Point):
            r2 = V(other.rect)      # The vector other is
        else:
            r2 = V(other.q) - V(other.p)  # The vector other is
        return r1.dot(r2)
    def cross(self, other):
        '''Consider the line from p to q a vector.  Return the cross
        product of these two vectors.
        '''
        if self.is_zero:
            return self.copy
        if not ii(other, (Point, Line, Plane)):
            raise TypeError("other must be a Point, Line, or Plane object")
        r1 = V(self.q) - V(self.p)  # The vector self is
        if ii(other, Point):
            r2 = V(other.rect)      # The vector other is
        else:
            r2 = V(other.q) - V(other.p)  # The vector other is
        r = r1.cross(r2)
        return Line(Point(0, 0, 0), Point(r))
    def normalize(self):
        '''Adjust q so that the vector from p to q is of unit length.
        '''
        if self.is_zero:
            return
        x, y, z = self.p.rect
        a, b, c = self.dc
        self._q = Point(x + a, y + b, z + c)
    @property
    def copy(self):
        return Line(self.p.copy, self.q.copy)
    @property
    def dc(self):
        '''Returns a 3-tuple of the direction cosines of the line in
        the current coordinate system.
        '''
        if self.is_zero:
            return (0, 0, 0)
        x1, y1, z1 = self.p.ToCCS()
        x2, y2, z2 = self.q.ToCCS()
        L = hypot(x1 - x2, hypot(y1 - y2, z1 - z2))
        if not L:
            raise RuntimeError("Bug in Line.dc:  zero length vector")
        return ((x2 - x1)/L, (y2 - y1)/L, (z2 - z1)/L)
    @property
    def L(self):
        '''Returns the length of the line segment.
        '''
        if self.is_zero:
            return 0
        x1, y1, z1 = self.p.ToCCS()
        x2, y2, z2 = self.q.ToCCS()
        return hypot(x1 - x2, hypot(y1 - y2, z1 - z2))
    @property
    def u(self):
        '''Returns the line's unit vector as a 3-tuple.
        '''
        if self.is_zero:
            return self.copy
        L = self.L
        x1, y1, z1 = self.p.ToCCS()
        x2, y2, z2 = self.q.ToCCS()
        if not L:
            raise ValueError("Zero vector")
        return ((x2 - x1)/L, (y2 - y1)/L, (z2 - z1)/L)
    def _get_p(self):
        return self._p
    def _set_p(self, p):
        if not ii(p, Point):
            raise ValueError("p must be set to a Point object")
        if self.q == p:
            raise ValueError("p must be distinct from q")
        self._p = p
    def _get_q(self):
        return self._q
    def _set_q(self, pt):
        if not ii(pt, Point):
            raise ValueError("q must be set to a point")
        if self.p == pt:
            raise ValueError("q must be distinct from p")
        self._q = pt
    p = property(_get_p, _set_p, doc="Get/set the first point")
    q = property(_get_q, _set_q, doc="Get/set the second point")
class Plane(Line):
    '''Model a plane in three-dimensional space using Cartesian
    coordinates.  The plane is characterized by a vector from point p
    to q that is normal to the plane; point p is in the plane.
    Because of this, it is derived from Line.
    '''
    def __init__(self, *par):
        '''There are a variety of ways to define a plane (pt = Point
        type, ln = Line type, pl = Plane type):
            * pl: copy of existing Plane object
            * ln: make the plane the same as the line, but normalized
            * pt1, pt2, pt3: three noncollinear points.
            * pt, ln1, ln2:  a point and two lines (the line's cross
              product determines the plane's normal).
            * pt, ln:  a point and a line; the plane will contain
              the line and the line is a normal to the plane.
            * pt, pl:  a point and a plane; the new plane will be
              parallel to the given plane and pass through the point.
 
        These aren't implemented yet:
            * ln1, ln2:  two lines that intersect; the plane's normal
              will be defined by the cross product and the plane will
              contain the lines.
            * ln1, ln2:  two lines that don't intersect; the plane
              will contain the first line and be parallel to the
              second line.
        '''
        Ctm.__init__(self)
        # Implementation:  the plane will be defined by two points p
        # and q.  The plane passes through p and the unit vector
        # from p to q determines the normal.  Since this is what is
        # encapsulated in a Line object, the plane is derived from
        # a Line object.
        if len(par) == 1:
            # Initialize by making a copy of a Plane object
            if not ii(par[0], (Line, Plane)):
                msg = ("Require a plane or line for one-parameter "
                       "initialization")
                raise ValueError(msg)
            super(Plane, self).__init__(par[0]._p.copy, par[0]._q.copy)
            self.normalize()
        elif len(par) == 2:
            C1a = ii(par[0], Point) and ii(par[1], Plane)
            C1b = ii(par[0], Plane) and ii(par[1], Point)
            C1 = C1a or C1b
            C2a = ii(par[0], Point) and ii(par[1], Line)
            C2b = ii(par[0], Line) and ii(par[1], Point)
            C2 = C2a or C2b
            C3 = ii(par[0], Line) and ii(par[1], Line)
            C4 = ii(par[0], Point) and ii(par[1], Point)
            if C1:
                # The new plane will pass through the point and be
                # parallel to the existing plane.
                pt, pl = par if C1a else (par[1], par[0])
                x, y, z = pt.rect
                a, b, c = pl.dc
                pt1 = Point(x + a, y + b, z + c)
                #self._p, self._q = pt, pt1
                super(Plane, self).__init__(pt, pt1)
            elif C2:
                # The plane will contain the point and the line is a
                # normal to the plane.
                p, ln = par if C2a else (par[1], par[0])
                x, y, z = p.rect
                a, b, c = ln.dc
                q = Point(x + a, y + b, z + c)
                #self._p, self._q = p, q
                super(Plane, self).__init__(p, q)
            elif C3:
                # If the lines intersect, then the plane contains both
                # lines and the normal is defined by p X q.  If the
                # lines do not intersect, the plane will contain line 1
                # and will be parallel to line 2.
                ln1, ln2 = par
                R = ln1.Rnd
                if ln1 == ln2:
                    raise ValueError("Two lines are the same")
                # [an:80] The lines intersect iff the following scalar
                # triple product is zero.
                r1, r2 = V(ln1.p.rect), V(ln1.q.rect)
                r3, r4 = V(ln2.p.rect), V(ln2.q.rect)
                if R((r1 - r2).STP(r2, r4)) == 0:
                    # Lines intersect
                    pt1 = ln1.intersect(ln2)
                    normal = (r2 - r1).cross(r4 - r3)
                    ln = Line(Point(0, 0, 0), Point(normal))
                    a, b, c = ln.dc
                    x, y, z = pt1.rect
                    super(Plane, self).__init__(pt1, Point(x + a, y + b,
                                                           z + c))
                else:
                    # Lines do not intersect.  Make plane contain line
                    # 1 and be parallel to line 2:  take the two
                    # points making up line 1 as the first 2 points.
                    # Then take the direction cosines of line 2 and
                    # use them to construct a third point in the same
                    # direction from point q.  Construct the plane
                    # from these three points.
                    p, q = ln1.p, ln1.q
                    x, y, z = q.rect
                    a, b, c = ln2.dc
                    r = Line(q, Point(x + a, y + b, z + c))
                    super(Plane, self).__init__(p, q, r)
            elif C4:
                # The two points are our normal after normalizing
                super(Plane, self).__init__(par[0], par[1])
            else:
                raise ValueError("Improper types of parameters")
        elif len(par) == 3:
            p, q, p3 = par
            C1 = ii(p, Point) and ii(q, Point) and ii(p3, Point)
            C2a = ii(par[0], Point) and ii(par[1], Line) and ii(par[2], Line)
            C2b = ii(par[0], Line) and ii(par[1], Point) and ii(par[2], Line)
            C2c = ii(par[0], Line) and ii(par[1], Line) and ii(par[2], Point)
            C2 = C2a or C2b or C2c
            if C1:
                # Plane from 3 points
                if p.AreCollinear(q, p3):
                    raise ValueError("Three points are collinear")
                r1, r2, r3 = V(p.rect), V(q.rect), V(p3.rect)
                # The following is the unit vector in the plane's
                # direction (see [an] p 77).  I've defined things so
                # that if you e.g. had the three points the origin,
                # hat i and hat j, in that order (i.e.,
                # counterclockwise), you'd have the unit vector
                # pointing in the hat k direction.  If the points are
                # taken clockwise, the unit vector points in the
                # negative hat k direction.
                u = (r1 - r2).cross(r1 - r3).normalize()
                # The second point of the line will be 1 unit of
                # distance away from p in the direction of the
                # normal; this uses the vector parametric equation of
                # the line with parameter = 1.
                p4 = Point(r1 + u)
                # This defines the normal to the plane and passes
                # through p.
                #self._p, self._q = p, p4
                super(Plane, self).__init__(p, p4)
            elif C2:
                # Plane from a point and two lines.  The cross product
                # of ln1 x ln2 determines the plane's normal
                # direction.
                p, ln1, ln2 = [V(i) for i in par]
                # Unit vector in direction of cross product
                u = V(ln1.dc).cross(V(ln2.dc)).normalize()
                r1, R = V(p.rect), p.Rnd
                a, b, c = u.rect
                if R(a) == 0 and R(b) == 0 and R(c) == 0:
                    raise ValueError("The lines are parallel")
                q = Point(r1 + u)
                #self._p, self._q = Point(p), q
                super(Plane, self).__init__(Point(p), q)
            else:
                raise ValueError("Improper types of parameters")
        else:
            raise ValueError("Improper number of parameters")
    def ToCCS(self):
        '''Calculate and return the point p's coordinates in the current
        coordinate system.
        '''
        self.q.ToCCS()
        return self.p.ToCCS()
    def ToDCS(self):
        '''Calculate and return the point p's coordinates in the default
        coordinate system.
        '''
        self.q.ToDCS()
        return self.p.ToDCS()
    def __str__(self):
        '''String representation of a Plane object.
        '''
        no2d = True
        sp = self.p.__str__(no2d)
        sq = self.q.__str__(no2d)
        return "Pl(%s, %s)" % (sp, sq)
    def __neg__(self):
        '''The unary negation of a plane means to make its normal
        point in the opposite direction.
        '''
        o = Plane(self)
        x, y, z = o.p.rect
        ln = -Line(o.p, o.q)
        a, b, c = ln.dc
        o._q = Point(x + a, y + b, z + c)
        return o
    def _pt_in_plane(self, other):
        # Return True if the point other is in the plane.
        # The point must satisfy the plane's equation to
        # intersect it.
        if not ii(other, Point):
            raise TypeError("other must be a point")
        if self.is_zero:
            return False
        r, mu = V(other.rect), V(self.dc)
        p0 = mu.dot(r)
        return True if self.Rnd(self.dnd - p0) == 0 else False
    def intersect(self, other):
        if self.is_zero:
            return None
        elif ii(other, Point):
            return other if self._pt_in_plane(other) else None
        elif ii(other, Plane):
            n, no = V(self.dc), V(other.dc)
            if self.Rnd(n.dot(no) - 1) == 0:
                # Planes are parallel
                return self if self == other else None
            # They intersect in a line.  Formulas from [an:81].
            A1, B1, C1 = self.dc
            A2, B2, C2 = other.dc
            D1, D2 = -self.dnd, -other.dnd
            a = Det2((B1, C1, B2, C2))
            b = Det2((C1, A1, C2, A2))
            c = Det2((A1, B1, A2, B2))
            mu = a*a + b*b + c*c
            assert mu, "Bug:  planes are parallel"
            # Intersection point (x, y, z)
            x = (b*Det2((D1, C1, D2, C2)) - c*Det2((D1, B1, D2, B2)))/mu
            y = (c*Det2((D1, A1, D2, A2)) - a*Det2((D1, C1, D2, C2)))/mu
            z = (a*Det2((D1, B1, D2, B2)) - b*Det2((D1, A1, D2, A2)))/mu
            p = Point(x, y, z)
            q = Point(x + a/mu, y + b/mu, z + c/mu)
            return Line(p, q)
        elif ii(other, Line):
            # The line will intersect the plane if it's not parallel
            # to it.  If it's a line segment, then the intersection
            # point must be between the Line's two points, inclusive.
            mu, o = V(self.n.dc), V(other.dc)
            if self.Rnd(mu.dot(o)) == 0:
                # The line is parallel to the plane.  If a point of
                # the line is in the plane, then return the line;
                # otherwise return None.
                p = other.p
                return other if self._pt_in_plane(p) else None
            # The line and plane definitely intersect at one point.
            # Method from [an:82].
            rl, nl = V(other.p.rect), V(other.dc)
            rp, np = V(self.p.rect), V(self.dc)
            G = np.dot(rp - rl)/nl.dot(np)
            ri = rl + G*nl
            pt = Point(ri)
            # xxz Need to handle case where it's a line segment
            return pt
        else:
            raise ValueError("other must be a point, line, or plane")
    def dist(self, other):
        '''Calculate the distance between this plane and another
        object.  To lines and planes, the distance is the
        perpendicular distance and it will always be positive.
        '''
        R = self.Rnd
        if self.is_zero:
            raise ValueError("Plane is the zero plane")
        elif ii(other, Point):
            # [an:85]
            n = self.n  # Unit normal vector to plane
            r = V(other.rect)
            return abs(self.Rnd(n.dot(r)))
        elif ii(other, Plane):
            return self.dist(other.p)
        elif ii(other, Line):
            # The distance will be zero unless the line is parallel to
            # the plane.  The line will be parallel to the plane if
            # the line is perpendicular to the plane's normal.
            u_line = V(other.dc)
            u_plane = self.n
            t = u_line.dot(u_plane)
            if R(t):
                # Line and plane not parallel
                return 0
            # Pick a point on the line, then calculate the distance
            # from the plane to the line
            return self.dist(other.p)
        else:
            raise TypeError("other must be a point, line, or plane")
    @property
    def copy(self):
        return Plane(self)
    @property
    def n(self):
        '''Returns the unit normal vector to the plane.
        '''
        if self.is_zero:
            raise ValueError("Plane is the zero plane")
        return V(self.dc)
    @property
    def dnd(self):
        '''Returns the directed normal distance from the origin to the
        plane; this is usually called p in the Hessian normal form
        equation):  n dot r = p where n is the unit normal vector to
        the plane and r is any point on the plane.
        '''
        if self.is_zero:
            raise ValueError("Plane is the zero plane")
        r0, mu = V(self.p), V(self.dc)
        return mu.dot(r0)
    def _set_p(self, p):
        '''Set the point self.p to a given point.
        '''
        if not ii(p, Point):
            raise ValueError("p must be a Point object")
        if self.q == p:
            self.is_zero = True
        else:
            self.p = p
            self.is_zero = False
    def _set_q(self, q):
        '''Set the point self.q to a given point.
        '''
        if not ii(q, Point):
            raise ValueError("q must be a Point object")
        if self.p == q:
            self.is_zero = True
        else:
            self.q = q
            self.is_zero = False
    def _get_p(self):
        return self._p
    def _get_q(self):
        return self._q
    p = property(_get_p, _set_p, doc="Get/set the first point")
    q = property(_get_q, _set_q, doc="Get/set the second point")
def IsUncertainty(lst):
    '''If one of the numbers in the sequence lst is an uncertainty
    type, return True.
    '''
    if ii(lst, (tuple, list)):
        for i in lst:
            if ii(i, UFloat):
                return True
        return False
    else:
        return ii(lst, UFloat)
def Det2(matrix):
    '''Calculate a 2x2 determinant:
        | a b |
        | c d |
    '''
    a, b, c, d = matrix
    return a*d - b*c
def Det3(matrix):
    '''Calculate a 3x3 determinant:
        | a b c |
        | d e f |
        | g h i |
    '''
    a, b, c, d, e, f, g, h, i = matrix
    return a*Det2((e, f, h, i)) - b*Det2((d, f, g, i)) + c*Det2((d, e, g, h))
def Det4(matrix):
    '''Calculate a 4x4 determinant.
    '''
    a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p = matrix
    # Expand along first row
    return (a*Det3((f, g, h, j, k, l, n, o, p)) +
            -b*Det3((e, g, h, i, k, l, m, o, p)) +
            c*Det3((e, f, h, i, j, l, m, n, p)) +
            -d*Det3((e, f, g, i, j, k, m, n, o)))
if __name__ == "__main__": 
    if 1:   # Setup
        # Standard imports
            import math
        # Custom imports
            from f import flt
            from lwtest import *
        # Global variables
            # The following is a "random" matrix that I made up; it has no
            # other significance.
            rm = [  1,    -7,      3,   17, 
                -47.5,   0.002,  1,   -1, 
                -0.2, -10,     -3.3,  4, 
                    1,     0.1,   -0.2,  0.3]
            identity = [1, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1]
            # Make sure we test with Ctm angle measurements in radians
            Ctm._angle = 1
            Ctm._angle_name = "rad"
            # Tolerance for floating point stuff
            eps = 1e-15
    def Test_Ctm():
        # We'll test some of the basic capabilities of Ctm.  We can't
        # test the transformations, as that would use one of the methods
        # which is abstract; they'll be tested in e.g. the tests of the
        # Point object.
        # 
        # Things to test:
        #     - CTM is identity matrix at instantiation
        #     - Rnd()
        #     - Can get and set CTM
        #     - CTM inverse (note it's in separate test)
        #     - reset() sets CTM to identity matrix
        # Verify identity matrices at instantiation
        c = Ctm()
        got = c.GetCTM()
        assert_equal(got, identity[:])
        got = c.GetICTM()
        assert_equal(got, identity[:])
        # Check Rnd
        Ctm.eps = 0.01
        got = c.Rnd(-0.00999)
        expected = 0
        assert_equal(got, expected)
        # Check ability to set CTM
        expected = rm[:]
        c.SetCTM(expected[:])
        got = c.GetCTM()
        assert_equal(got, expected)
        # If reset() is not used here, later tests will fail
        c.reset()
        assert_equal(c.GetCTM(), identity[:])
    if use_numpy:
        def Test_MatrixInverse():
            # This test uses numpy's matrix inversion as a standard.
            def MakeMatrix(lst):
                A = np.array(lst)
                A.shape = (4, 4)
                return np.matrix(A)
            c, p = Ctm(), Point(0, 0, 0)
            c.SetCTM(rm[:])
            P, n = MakeMatrix(c.GetCTM())*MakeMatrix(c.GetICTM()), 4
            # P should be the identity matrix
            for i in range(n):
                for j in range(n):
                    if i == j:
                        assert_equal(p.Rnd(P[i, j] - 1), 0)
                    else:
                        assert_equal(p.Rnd(P[i, j]), 0)
            c.reset()
        def Test_Det():
            # Determinant.  Check Det4, as it depends on Det3 and Det2.
            # numpy provides the standard determinant.
            A = np.array(rm)
            A.shape = (4, 4)
            A = np.matrix(A)
            p = Point(0, 0, 0)
            assert_equal(p.Rnd(Det4(rm) - npdet(A)), 0)
    else:
        # This uses matrix.py's features
        def Test_MatrixInverse():
            def MakeMatrix(lst):
                # Make the list a 4x4 matrix
                A = matrix.matrix(lst, size=(4, 4))
                return A
            c, p = Ctm(), Point(0, 0, 0)
            c.SetCTM(rm[:])
            P, n = MakeMatrix(c.GetCTM())*MakeMatrix(c.GetICTM()), 4
            # P should be the identity matrix
            for i in range(n):
                for j in range(n):
                    if i == j:
                        assert_equal(p.Rnd(P[i, j] - 1), 0)
                    else:
                        assert_equal(p.Rnd(P[i, j]), 0)
            c.reset()
        def Test_Det():
            # Check Det4, as it depends on Det3 and Det2.
            A = matrix.matrix(rm, size=(4, 4))
            expected = A.det
            got = Det4(rm)
            p = Point(0, 0, 0)
            assert_equal(p.Rnd(got - expected), 0)
    def Test_Vector():
        Ctm._compass = False
        Ctm._neg = False
        Ctm._elev = False
        # Initialization
        if True:
            # Three numbers
            i = V(1, 0, 0)
            # A Point object
            j = V(Point(0, 1, 0))
            # A 3-tuple
            k = V((0, 0, 1))
            # A Line object
            v = V(Line(Point(0, 0, 0), Point(1, 1, 1)))
            # Another vector
            w = V(V(1, 2, 3))
        # copy
        a = v.copy
        assert_equal(v, a)
        # dist
        assert_equal(i.dist(j), math.sqrt(2))
        # Unary negate
        a = -i
        assert_equal(a._p, Point(-1, 0, 0))
        # Equality
        assert_equal(a == a, True)
        assert_equal(a != i, True)
        # Addition
        assert_equal(i + j + k, v)
        # Subtraction
        assert_equal(i - j, V(1, -1, 0))
        # Multiplication
        assert_equal(2*i, V(2, 0, 0))
        assert_equal(i*2, V(2, 0, 0))
        # Dot product
        assert_equal(i.dot(j), 0)
        assert_equal(i.dot(i), 1)
        assert_equal(v.dot(w), 6)
        # Cross product
        assert_equal(i.cross(j), k)
        assert_equal(j.cross(k), i)
        assert_equal(k.cross(i), j)
        # Magnitude
        assert_equal(v.mag, math.sqrt(3))
        # Normalize
        a = w.copy
        assert(a.mag != 1.0)
        a.normalize()
        assert_equal(a.Rnd(a.mag - 1), 0)
        # Scalar triple product
        assert_equal(i.STP(j, k), 1)
        # Vector triple product
        assert_equal(i.VTP(j, k), V(0, 0, 0))
        # rect property
        assert_equal(i.rect, (1, 0, 0))
        # dc property
        a = 1/math.sqrt(3)
        assert_equal(i.dc, (1, 0, 0))
        assert_equal(v.dc, (a, a, a), abstol=eps)
        # u property
        a = 1/math.sqrt(3)
        assert_equal(v.u, V(a, a, a))
        # cyl property
        assert_equal(v.cyl, (math.sqrt(2), math.pi/4, 1))
        rho, theta, z = v.cyl
        assert_equal(v.rho, rho)
        assert_equal(v.theta, theta)
        assert_equal(v.z, z)
        # sph property
        r = math.hypot(rho, v._p._r[2])
        x, y, z = v._p._r
        assert_equal(v.sph, (r, math.atan2(y, x), math.atan2(rho, z)))
        r, theta, phi = v.sph
        assert_equal(r, v.r)
        assert_equal(theta, v.theta)
        assert_equal(phi, v.phi)
    def Test_Point():
        Ctm._compass = False
        Ctm._neg = False
        Ctm._elev = False
        # Instantiation
        if 1:
            # 3 rectangular coordinates
            p = Point(1, 2, 3)
            assert_equal(p.rect, (1, 2, 3))
            # A 3-tuple
            p = Point((1, 2, 3))
            assert_equal(p.rect, (1, 2, 3))
            # Another point
            p1 = Point(p)
            assert_equal(p.rect, (1, 2, 3))
            # A vector V object
            p1 = Point(V(1, 2, 3))
            assert_equal(p1, p)
        # Copy
        p1 = p.copy
        assert_equal(p, p1)
        # String representations
        i = Point(0, 0, 0)
        assert_equal(str(i), "Origin")
        i = Point(1, 0, 0)
        Ctm._suppress_z = False
        assert_equal(str(i), "Pt(1, 0, 0)")
        Ctm._suppress_z = True
        assert_equal(str(i), "Pt(1, 0)")
        assert_equal(i.__str__(no2d=True), "Pt(1, 0, 0)")
        Ctm._suppress_z = False
        Ctm._coord_sys = "cyl"
        assert_equal(str(i), "Pt<1, 0, 0>")
        Ctm._coord_sys = "sph"
        assert_equal(str(i), "Pt<<1, 0, 1.571>>")
        Ctm._elev = True
        assert_equal(str(i), "Pt<<1, 0, 0 E>>")
        Ctm._angle = 180/math.pi
        Ctm._angle_name = "deg"
        assert_equal(str(i), "Pt<<1, 0, 0 Eo>>")
        # Conversions to cylindrical and spherical coordinates
        Ctm._coord_sys = "rect"
        Ctm._elev = False
        Ctm._suppress_z = False
        Ctm._angle = 1
        Ctm._angle_name = "rad"
        if 1:
            def TestConversions(deg=False):
                '''This will test in radians unless deg is True, in
                which case the angles will be converted to radians.
                '''
                Ctm._compass = False
                Ctm._neg = False
                Ctm._elev = False
                d2r = math.pi/180 if deg else 1
                # Basics
                p = Point(1, 2, 3)
                assert_equal(p.rect, (1, 2, 3))
                rho, theta, z = p.cyl
                assert_equal(p.Rnd(rho - math.sqrt(5)), 0)
                assert_equal(p.Rnd(d2r*theta - math.atan(2)), 0)
                assert_equal(p.Rnd(z - 3), 0)
                r, theta, phi = p.sph
                assert_equal(p.Rnd(r - math.sqrt(14)), 0)
                assert_equal(p.Rnd(d2r*theta - math.atan(2)), 0)
                assert_equal(p.Rnd(d2r*phi - math.atan(math.sqrt(5)/3)), 0)
                # Compass mode 
                o = Point(0, 0, 0)
                i, j = Line(o, Point(1, 0, 0)), Line(o, Point(0, 1, 0))
                k = Line(o, Point(0, 0, 1))
                Ctm._compass = True
                rho, theta, z = i.q.cyl
                assert_equal(i.Rnd(d2r*theta), math.pi/2)
                rho, theta, z = j.q.cyl
                assert_equal(i.Rnd(d2r*theta), 0)
                ij = i + j
                rho, theta, z = ij.q.cyl
                assert_equal(i.Rnd(d2r*theta - math.pi/4), 0)
                # Negative mode
                Ctm._compass = False
                Ctm._neg = True
                rho, theta, z = j.q.cyl
                assert_equal(i.Rnd(d2r*theta - 3*math.pi/2), 0)
                rho, theta, z = ij.q.cyl
                assert_equal(i.Rnd(d2r*theta - 7*math.pi/4), 0)
                Ctm._compass = True
                rho, theta, z = ij.q.cyl
                assert_equal(i.Rnd(d2r*theta - 7*math.pi/4), 0)
                # Elevation mode
                Ctm._compass = False
                Ctm._neg = False
                Ctm._elev = True
                r, theta, phi = ij.q.sph
                assert_equal(i.Rnd(d2r*phi), 0)
                ijk = i + j + k
                r, theta, phi = ijk.q.sph
                assert_equal(i.Rnd(r), math.sqrt(3), abstol=eps)
                assert_equal(i.Rnd(d2r*theta - math.pi/4), 0)
                assert_equal(i.Rnd(d2r*phi - math.atan(1/math.sqrt(2))), 0)
                ijmk = i + j - k
                r, theta, phi = ijmk.q.sph
                assert_equal(i.Rnd(d2r*phi + math.atan(1/math.sqrt(2))), 0)
            Ctm._angle = 1
            TestConversions(deg=False)
            # Check that things work in degrees too
            Ctm._angle = 180/math.pi
            TestConversions(deg=True)
        # Restore default state
        Ctm._angle = 1
        Ctm._compass = False
        Ctm._neg = False
        Ctm._elev = False
        # Rotate point on x axis about the z axis by 90 deg
        p = Point(1, 0, 0)
        p.rotate(math.pi/2, (0, 0, 1))
        x, y, z = p.ToCCS()
        assert_equal(p.Rnd(x), 0)
        assert_equal(p.Rnd(y + 1), 0)
        assert_equal(p.Rnd(z), 0)
        # Verify coordinates in default system unchanged
        x, y, z = p.ToDCS()
        assert_equal(p.Rnd(x - 1), 0)
        assert_equal(p.Rnd(y), 0)
        assert_equal(p.Rnd(z), 0)
        # Verify rotation axis and angle as expected
        theta, axis = p.GetRotationAxis()
        assert_equal(p.Rnd(theta - math.pi/2), 0)
        x, y, z = axis
        assert_equal(p.Rnd(x), 0)
        assert_equal(p.Rnd(y), 0)
        assert_equal(p.Rnd(z - 1), 0)
        # Check dist works
        p1, p2 = Point(0, 0, 0), Point(1, 1, 1)
        assert_equal(p.Rnd(p1.dist(p2) - math.sqrt(3)), 0)
        # Check equality 
        p1, p2 = Point(0, 0, 0), Point(0, 0, 0)
        assert_equal(p1 == p2, True)
        p1, p2 = Point(0, 0, 0), Point((0, 0, 1))
        assert_equal(p1 == p2, False)
        # Point.m can be set to an object (we'll use a function object
        # for this test)
        p = Point(1, 2, 3, Det4)
        assert_equal(p.m, Det4)
        # Collinearity
        p1, p2, p3 = Point(0, 0, 0), Point(1, 0, 0), Point(2, 0, 0)
        assert_equal(p1.AreCollinear(p2, p3), True)
        # Negation
        p1, p2, p3 = Point(0, 0, 0), Point(1, 1, 1), Point(-1, -1, -1)
        assert_equal(-p1, p1)
        assert_equal(-p2, p3)
        # Intersection
        assert_equal(p1.intersect(p1), p1)
        assert_equal(p1.intersect(p2), None)
        # Attributes
        if 1:
            # Rectangular
            p, a, b, c = Point(1, 0, 0), 2, 3, 4
            p.x = a
            assert_equal(p.x, a)
            assert_equal(p, Point(a, 0, 0))
            p.y = b
            assert_equal(p.y, b)
            assert_equal(p, Point(a, b, 0))
            p.z = c
            assert_equal(p.z, c)
            assert_equal(p, Point(a, b, c))
            # Cylindrical
            a, b, c = 1, 2, 3
            p = Point(a, b, c)
            assert_equal(p.rho, math.hypot(a, b))
            theta = p.theta
            r = 10
            p.rho = r
            x, y, z = p.rect
            assert_equal(x, r*math.cos(theta))
            assert_equal(y, r*math.sin(theta))
            p = Point(a, b, c)
            p.theta = math.pi/2
            x, y, z = p.rect
            assert_equal(x, 0)
            assert_equal(y, math.sqrt(5))
            # Spherical
            a, b, c = 1, 2, 3
            p = Point(a, b, c)
            assert_equal(p.Rnd(p.r - math.hypot(a, math.hypot(b, c))), 0)
            r, theta, phi = p.sph
            d = 1
            p.r = d
            r, theta, phi = p.sph
            assert_equal(p.Rnd(r - d), 0)
            p.theta = d
            r, theta, phi = p.sph
            assert_equal(p.Rnd(theta - d), 0)
            p.phi = d
            r, theta, phi = p.sph
            assert_equal(p.Rnd(phi - d), 0)
            # Direction cosines
            p = Point(1, 1, 1)
            dc, a = p.dc, 1/math.sqrt(3)
            assert_equal(dc, (a, a, a), abstol=eps)
            # proj_ang
            pa = p.proj_ang
            a = math.pi/4
            assert_equal(pa, (a, a))
    def Test_Line():
        Ctm._compass = False
        Ctm._neg = False
        Ctm._elev = False
        # Get and set attributes
        p0 = Point(0, 0, 0)
        px = Point(1, 0, 0)
        py = Point(0, 1, 0)
        pz = Point(0, 0, 1)
        p  = Point(1, 1, 1)
        # Initialization 
        if True:
            # Use 2 points
            L = Line(px, py)
            assert_equal(L.L, math.sqrt(2))
            assert_equal(L.p, px)
            assert_equal(L.q, py)
            L.p = p0   # Set attribute
            assert_equal(L.p, p0)
            L.q = px   # Set attribute
            assert_equal(L.L, 1)
            # Use 1 point and direction numbers
            npy = (0, -1, 0)
            L = Line(px, npy)  # Line goes in -y direction
            assert_equal(L.p, px)
            assert_equal(L.dc, (0, -1, 0))
            # Use 1 point and a line
            L = Line(px, Line(p0, Point(*npy)))
            assert_equal(L.p, px)
            assert_equal(L.dc, (0, -1, 0))
        # Check equality
        assert_equal(Line(p0, px), Line(p0, px))
        # Check direction cosines
        assert_equal(Line(p0, px).dc, (1, 0, 0))
        assert_equal(Line(p0, py).dc, (0, 1, 0))
        assert_equal(Line(p0, pz).dc, (0, 0, 1))
        # Check dist
        if True:
            # Line and point
            L = Line(p0, px)
            assert_equal(L.dist(py), 1)
            L = Line(p0, py)
            assert_equal(L.dist(pz), 1)
            L = Line(p0, pz)
            assert_equal(L.dist(px), 1)
            L = Line(px, p0)
            assert_equal(L.dist(p), math.sqrt(2))
            # Line and line
            L1 = Line(px, p0)   # Line along x axis
            a = math.sqrt(5)
            L2 = Line(Point(0, 0, a), Point(0, 1, a)) # Along y at z = a
            assert_equal(L1.dist(L2), a)
        # Negation
        L = Line(Point(0, 0, 0), Point(1, 1, 1))
        M = -L
        assert_equal(M.p, L.q)
        assert_equal(M.q, L.p)
        # Copy
        L = Line(Point(0, 0, 0), Point(1, 1, 1))
        M = L.copy
        assert_equal(L, M)
        # Intersections
        O, i, j = Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0)
        if True:
            # Line and point
            L = Line(O, i)
            assert_equal(L.intersect(O), O)
            assert_equal(L.intersect(j), None)
            L, p = Line(i, j), Point(1/2, 1/2, 0)
            assert_equal(L.intersect(O), None)
            assert_equal(L.intersect(p), p)
            # Line and line
            if True:
                # Coincident parallel lines
                L = Line(O, i)
                assert_equal(L.intersect(L), L)
                # Two intersecting lines in the xy plane
                L1 = Line(i, j)
                L2 = Line(O, Point(1, 1, 0))
                assert_equal(L1.intersect(L2), Point(1/2, 1/2, 0))
        # Check dot product
        Li, Lj, Lk, a = Line(O, i), Line(O, j), Line(O, Point(0, 0, 1)), 3
        L1, L2 = Line(O, Point(a, a, a)), Line(O, Point(-a, -a, -a))
        if True:
            # Simple orthogonal checks
            assert_equal(Li.dot(Lj), 0)
            assert_equal(Li.dot(Li), 1)
            assert_equal(Li.dot(L1), a)
            assert_equal(Lj.dot(L1), a)
            assert_equal(Lk.dot(L1), a)
            assert_equal(Li.dot(L2), -a)
            assert_equal(Lj.dot(L2), -a)
            assert_equal(Lk.dot(L2), -a)
            # Non-orthogonal check
            a, b = Point(1, 2, 3), Point(-4, -5, -6)
            c, d = Point(-7, -8, 9), Point(10, -11, 12)
            L1, L2 = Line(a, b), Line(c, d)
            assert_equal(L1.dot(L2), -91)
        # Check cross product
        assert_equal(Li.cross(Lj), Lk)
        assert_equal(Lj.cross(Lk), Li)
        assert_equal(Lk.cross(Li), Lj)
        # Check locate
        o, i, p = Point(0, 0), Point(1, 0), Point(0, 1)
        ln = Line(o, i)
        ln.locate(p)
        assert_equal(ln, Line(Point(0, 1), Point(1, 1)))
        o.locate(p)
        assert_equal(o, p)
    def Test_Plane():
        Ctm._compass = False
        Ctm._neg = False
        Ctm._elev = False
        # Plane from 3 points
        O, i, j, k = (Point(0, 0, 0), 
                    Point(1, 0, 0), 
                    Point(0, 1, 0),
                    Point(0, 0, 1))
        xy = Plane(O, i, j)  # Go around polygon ccw
        assert_equal(xy.dc, (0, 0, 1))
        pl = Plane(O, j, i)  # Go around polygon cw
        assert_equal(pl.dc, (0, 0, -1))
        # Plane from point and two lines
        ln1, ln2 = Line(O, i), Line(O, j)
        pl = Plane(k, ln1, ln2)
        assert_equal(pl.dc, (0, 0, 1))
        assert_equal(pl.p, k)
        assert_equal(pl.q, Point(0, 0, 2))
        # Plane from point and plane
        xy = Plane(O, i, j)  # Is xy plane
        pt = Point(0, 0, 1)
        pl = Plane(pt, xy)
        assert_equal(pl.dc, (0, 0, 1))
        assert_equal(pl.dc, (0, 0, 1))
        # Plane from another plane
        pl1 = Plane(pl)
        assert_equal(pl, pl1)
        # Plane from point and line
        pl = Plane(O, Line(O, k))
        assert_equal(pl.dc, (0, 0, 1))  # Is xy plane
        assert_equal(pl.p, O)
        assert_equal(pl.q, k)
        # Plane from two lines that intersect
        o, i, k = Point(0, 0, 0), Point(1, 0, 0), Point(0, 0, 1)
        pl = Plane(Line(o, k), Line(o, i))
        xz = Plane(o, k, i)
        assert_equal(pl, xz)
        # Plane from two lines that don't intersect.  Plane will
        # contain ln1 and will be parallel to ln2.  Since ln1 is the i
        # unit vector and ln2 runs parallel to j, the plane will
        # contain the x axis and have its normal parallel to k; thus,
        # it will be the xy plane.
        o = Point(0, 0, 0)
        xy = Plane(o, Line(o, Point(0, 0, 1)))
        ln1 = Line(o, Point(1, 0, 0))   # In i direction
        ln2 = Line(Point(0, 0, 1), Point(0, 1, 1)) # In j direction
        pl = Plane(ln1, ln2)
        assert_equal(pl, xy)
        # Copy
        pl = Plane(O, i, j)
        pl1 = pl.copy
        assert_equal(pl, pl1)
        # Properties
        if True:
            pl = Plane(O, i, j)
            # Direction cosines of unit normal
            assert_equal(pl.dc, (0, 0, 1))
            # Hessian normal form p value
            pl = Plane(O, i, j)
            assert_equal(pl.dnd, 0)
            pl = Plane(k, Point(1, 0, 1), Point(0, 1, 1))
            assert_equal(pl.dnd, 1)
        # Intersections
        if True:
            # Plane and point
            pl = Plane(O, i, j)
            assert_equal(pl.intersect(O), O)
            assert_equal(pl.intersect(k), None)
            # Plane and line
            if True:
                # No intersection
                p1 = Point(1, 0, 1)
                ln = Line(p1, k)
                assert_equal(pl.intersect(ln), None)
                # Intersects in a point
                ln = Line(O, Point(1, 0, 1))
                assert_equal(pl.intersect(ln), O)
                # Intersects in a line (the line is in the plane)
                ln = Line(i, O)
                assert_equal(pl.intersect(ln), ln)
            # Plane and plane
            if True:
                # xy plane and xz plane
                pl1, pl2 = Plane(O, i, j), Plane(O, i, Point(1, 0, 1))
                ln = Line(O, i)
                assert_equal(pl1.intersect(pl2), ln)
                # Vertical planes through origin at right angles
                pl1 = Plane(O, Point(1, -1, 0), Point(1, -1, 1))
                pl2 = Plane(O, Point(1, 1, 0), Point(1, 1, 1))
                ln = Line(O, k)
                assert_equal(pl1.intersect(pl2), ln)
                # Parallel planes, equal
                assert_equal(pl1.intersect(pl1), pl1)
                # Parallel planes, don't intersect
                pl1 = Plane(O, i, j) # xy plane
                pl2 = Plane(Point(0, 0, 1), Point(1, 0, 1), Point(0, 1, 1))
                assert_equal(pl1.intersect(pl2), None)
        # dist
        if True:
            # Point and plane
            assert_equal(xy.dist(k), 1)
            assert_equal(xy.dist(i), 0)
            # Line and plane
            ln = Line(i, j)
            assert_equal(xy.dist(ln), 0)
            ln = Line(Point(1, 0, 1), Point(0, 1, 1))
            assert_equal(xy.dist(ln), 1)
            # Two planes
            pl = Plane(Point(0, 0, 1), Point(1, 0, 1), Point(0, 1, 1))
            assert_equal(xy.dist(pl), 1)
            pl = Plane(O, i, j)
            assert_equal(xy.dist(pl), 0)
    Test_Ctm()
    Test_Vector()
    Test_Point()
    Test_Line()
    Test_Plane()
    exit(run(globals(), halt=True)[0])
