'''
General-purpose math-related functions.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <math> General-purpose math-related functions:  AlmostEqual, polar
    # and rectangular coordinate conversions, bitlength of an integer,
    # integer square root, length of an Archimedean spiral,
    # approximation of inverse normal CDF.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    import math
    import sys
if 1:   # Custom imports
    from frange import frange
def AlmostEqual(a, b, rel_err=2e-15, abs_err=5e-323):
    '''Determine whether floating-point values a and b are equal to
    within a (small) rounding error; return True if almost equal and
    False otherwise.  The default values for rel_err and abs_err are
    chosen to be suitable for platforms where a float is represented
    by an IEEE 754 double.  They allow an error of between 9 and 19
    ulps.
 
    This routine comes from the Lib/test/test_cmath.py in the python
    distribution; the function was called almostEqualF.
    '''
    # Special values testing
    if math.isnan(a):
        return math.isnan(b)
    if math.isinf(a):
        return a == b
    # If both a and b are zero, check whether they have the same sign
    # (in theory there are examples where it would be legitimate for a
    # and b to have opposite signs; in practice these hardly ever
    # occur).
    if not a and not b:
        return math.copysign(float(1), a) == math.copysign(float(1), b)
    # If a - b overflows, or b is infinite, return False.  Again, in
    # theory there are examples where a is within a few ulps of the
    # max representable float, and then b could legitimately be
    # infinite.  In practice these examples are rare.
    try:
        absolute_error = abs(b - a)
    except OverflowError:
        return False
    else:
        return absolute_error <= max(abs_err, rel_err*abs(a))
def polar(x, y, deg=False):
    '''Return the polar coordinates for the given rectangular
    coordinates.  If deg is True, angle measure is in degrees;
    otherwise, angles are in radians.
    '''
    r2d = 180/math.pi if deg else 1
    return (math.hypot(x, y), math.atan2(y, x)*r2d)
def rect(r, theta, deg=False):
    '''Return the rectangular coordinates for the given polar
    coordinates.  If deg is True, angle measure is in degrees;
    otherwise, angles are in radians.
    '''
    d2r = math.pi/180 if deg else 1
    return (r*math.cos(theta*d2r), r*math.sin(theta*d2r))
if 1:   # Polynomial utilities
    # These routines were originally from 
    # http://www.physics.rutgers.edu/~masud/computing/
    # in the file WPark_recipes_in_python.html.  This URL is now defunct.

    # coef is a sequence of the polynomial's coefficients; coef[0] is the
    # constant term and coef[-1] is the highest term; x is a number.
    def polyeval(coef, x):
        '''Evaluate a polynomial with the stated coefficients.  Returns 
        coef[0] + x(coef[1] + x(coef[2] +...+ x(coef[n-1] + coef[n]x)...)
        This is Horner's method.
     
        Example: polyeval((3, 2, 1), 6) = 3 + 2(6) + 1(6)**2 = 51
        '''
        p = 0
        for i in reversed(coef):
            p = p*x + i
        return p
    def polyderiv(coef):
        '''Returns the coefficients of the derivative of a polynomial with
        coefficients in coef.
 
        Example: polyderiv((3, 2, 1)) = [2, 2]
        '''
        b = []
        for i in range(1, len(coef)):
            b.append(i*coef[i])
        return b
    def polyreduce(coef, root):
        '''Given a root of a polynomial, factor out the (x - root) term, then
        return the coefficients of the factored polynomial.
 
        Example: polyreduce((-12, -1, 1), -3) = [-4, 1]
        '''
        c, p = [], 0
        for i in reversed(coef):
            p = p*root + i
            c.append(p)
        c.reverse()
        return c[1:]
def bitlength(n):
    '''This emulates the n.bit_count() function of integers in python 2.7
    and 3.  This returns the number of bits needed to represent the
    integer n; n can be any integer.
 
    A naive implementation is to take the base two logarithm of the
    integer, but this will fail if abs(n) is larger than the largest
    floating point number.
    '''
    try:
        return n.bit_count()
    except Exception:
        return len(bin(abs(n))) - 2
def isqrt(x):
    '''Integer square root.  This calculation is done with integers, so it
    can calculate square roots for large numbers that would overflow the
    normal square root function.
    
    From
    http://code.activestate.com/recipes/577821-integer-square-root-function/
    '''
    if x < 0:
        raise ValueError("Square root not defined for negative numbers")
    n = int(x)
    if n == 0:
        return 0
    a, b = divmod(bitlength(n), 2)
    x = 2**(a+b)
    while True:
        y = (x + n//x)//2
        if y >= x:
            return x
        x = y
def inverse_normal_cdf(p):
    '''Compute the inverse CDF for the normal distribution.  Absolute
    value of the relative error is less than 1.15e-9.
 
    Retrieved 28 Feb 2012 from
    http://home.online.no/~pjacklam/notes/invnorm/impl/field/ltqnorm.txt.
    This link was provided by the algorithm's developer:
    http://home.online.no/~pjacklam/notes/invnorm/.
 
    DP:  I've made minor changes to formatting, etc.
 
    ---------------------------------------------------------------------------
    Original docstring:
 
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
if 1:   # Archimedean spirals
    ''' Length of an Archimedian spiral
    
    Motivation:  How much toilet paper is on a roll?  One way to measure it
    would be to roll it out.  This is perhaps the most accurate method.  But
    it would be nice to be able to estimate it from the roll's dimensions.
    The function ArchimedianSpiralArcLength below will help you do this.
    
    The polar equation of this spiral is
    
        r = a*theta
    
    where theta is the angle and a is a constant.  For a spiral with
    multiple revolutions, the distance between the revolutions (i.e., the
    pitch) is 
            
        pitch = 2*pi*a = math.tau*a.
    
    The arc length s is gotten from the integral from theta1 to theta2
    of
    
        sqrt(r*r + (dr/dtheta)^2) dtheta
    
    Substituting the equation for a spiral, we get
    
        A = sqrt(theta*theta + 1)
        s = a/2*[theta*A + ln(theta + A)]
    
    This is the formula for the total arc length from an angle of 0 to an angle
    of theta (remember theta is in radians).
    
    To convert this to more practical formulas, let
    
        D = outside diameter of roll
        d = inside diameter of roll
        t = thickness of material on roll
        n = number of turns of material on roll = n1 - n0
        n0 = number of turns to make up ID
        n1 = number of turns to make up OD
    
    Now, if t is reasonably thin, we have
    
        D = d + 2*n*t
    
    because one wrap adds a thickness of 2*t on the diameter.  For thin t,
    we can approximate the length by a finite sum:
    
        1st wrap:  circumference = pi*d
        2nd wrap:  circumference = pi*(d + 1*(2*t))
        3rd wrap:  circumference = pi*(d + 2*(2*t))
        4th wrap:  circumference = pi*(d + 3*(2*t))
        ...
        nth wrap:  circumference = pi*(d + (n-1)*(2*t))
    
    Thus, the sum is
    
        S = pi*[d + (d + 1*(2*t)) + (d + 2*(2*t)) + ... + (d + (n-1)*(2*t))]
    
    This is
    
        S = pi[n*d + 2*t*A(n - 1)]
    
    where A(n - 1) is the sum of the integers 1 to (n - 1).  This is
    0.5*(n - 1)*(n - 1 + 1) or n*(n - 1)/2.  Hence
    
        S/pi = n*d + 2*t*n*(n-1)/2 = n*d + t*n(n-1)
    
    or, finally,
    
    +------------------------+
    |                        |
    | S = pi*n*[t*(n-1) + d] |
    |                        |
    +------------------------+
    
    In terms of the constant in the polar equation for the spiral, we have
    
        t = 2*pi*a
        a = t/(2*pi)
    '''
def SpiralArcLength(a, theta, degrees=False):
    '''Calculate the arc length of an Archimedian spiral from angle
    0 to theta.  theta is in radians unless degrees is True.  The number a
    is the constant in the polar equation for the spiral
 
        r = a*theta
 
    The formula is exact.
    '''
    if a <= 0:
        raise ValueError("a must be > 0")
    theta = radians(flt(theta)) if degrees else flt(theta)
    A = sqrt(theta*theta + 1)
    return flt(a)/2*(theta*A + log(theta + A))
def ApproximateSpiralArcLength(ID, OD, thickness):
    '''Given the inside and outside diameters of a spiral roll of
    material with uniform thickness, estimate the length of material on
    the roll.  The three parameters must be measured in the same units
    and the returned number will be in the same units.
 
    The smaller thickness(OD - ID) is, the better the approximation.
    '''
    # Approximation:  for a large diameter circle, one revolution of a
    # fine-pitch spiral should be nearly equal to the circumference.
    if ID < 0 or ID >= OD:
        raise ValueError("ID must be >= 0 and < OD")
    if OD <= 0:
        raise ValueError("OD must be > 0")
    if thickness <= 0:
        raise ValueError("thickness must be > 0")
    n = (OD - ID)/thickness
    if n < 1:
        raise ValueError("Number of turns is < 1")
    pitch = (OD - ID)/n
    length = 0
    for dia in frange(ID, OD, 2*pitch):
        dia += pitch    # Use in-between diameter
        length += 2*math.pi*(dia + pitch)
    return length
if __name__ == "__main__": 
    from lwtest import run, raises, assert_equal, Assert
    from f import flt, tau, radians, log, sqrt
    eps = 1e-15
    def Test_polyeval():
        Assert(polyeval((3, 2, 1), 6) == 51)
    def Test_polyderiv():
        Assert(polyderiv((3, 2, 1)) == [2, 2])
    def Test_polyreduce():
        # Use (x - 1)*(x - 2) = 2 - 3*x + x**2
        p = (2, -3, 1)
        Assert(polyreduce(p, 1) == [-2, 1])
    def Test_rect():
        Assert(rect(0, 0) == (0, 0))
        Assert(rect(0, 180, deg=True) == (0, 0))
        x, y = rect(1, 45, deg=True)
        s = math.sin(math.pi/4)
        assert_equal(x, s, abstol=eps)
        assert_equal(y, s, abstol=eps)
    def Test_polar():
        Assert(polar(0, 0) == (0, 0))
        Assert(polar(0, 1) == (1, math.pi/2))
        Assert(polar(0, -1) == (1, -math.pi/2))
        Assert(polar(-1, 0) == (1, math.pi))
        s = math.sin(math.pi/4)
        r, theta = polar(s, s, deg=True)
        assert_equal(r, 1, abstol=eps)
        assert_equal(theta, 45, abstol=eps)
    def Test_isqrt():
        n0 = 123456789
        n = n0
        while n < n0**8:
            Assert(isqrt(n*n) == n)
            n = 3*n//2
    def Test_invnorm():
        '''I used scipy from a winpython36 installation to generate
        100 test points.
        '''
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
    def Test_Archimedean_exact():
        # a = 1, one revolution
        a, theta = 1, 2*math.pi
        A = math.sqrt(theta**2 + 1)
        exact = a/2*(theta*A + math.log(theta + A))
        formula = SpiralArcLength(a, theta)
        assert_equal(exact, formula)
        # Get ValueError for a < 0
        raises(ValueError, SpiralArcLength, -1, 1)
    def Test_Archimedean_approximation():
        # Approximation:  for a large diameter circle, one revolution of a
        # fine-pitch spiral should be nearly equal to the circumference.
        a, n_revolutions = 1, 10000
        theta = n_revolutions*math.tau
        arc_len = (SpiralArcLength(a, theta) -
                   SpiralArcLength(a, theta - math.tau))
        L_D = SpiralArcLength(a, n_revolutions*math.tau)
        L_d = SpiralArcLength(a, (n_revolutions - 1)*math.tau)
        arc_length = L_D - L_d
        pitch = a*math.tau
        D = (2*n_revolutions - 1)*pitch
        circumference = D*math.pi
        assert_equal(circumference, arc_len, reltol=1e-8)
    def Test_Archimedean_approximate_formula():
        ID, OD = 1, 2
        thickness = 0.001
        pitch = 2*thickness
        diameters = list(frange("1", "2", "0.001"))
        # Sum the circumferences
        estL1 = sum([dia*math.pi for dia in diameters])
        estL2 = ApproximateSpiralArcLength(ID, OD, thickness)
        assert_equal(estL1, estL2, reltol=0.002)
        # Now compare to exact formula
        a = pitch/math.tau
        # There are approximately ID/pitch circles from the spiral center
        # to the ID.  Since each is a revolution, multiplying by 2*pi
        # gives the total angle from 0 to the ID.  Similarly for OD.
        theta1 = math.tau*(ID/pitch)
        theta2 = math.tau*(OD/pitch)
        length1 = SpiralArcLength(a, theta1)
        length2 = SpiralArcLength(a, theta2)
        exact_length = length2 - length1
        tol = 0.001
        assert_equal(estL1, exact_length, reltol=tol)
        assert_equal(estL2, exact_length, reltol=tol)
        # In the above, L = 4710.8, estL = 4715.5, and the exact length
        # is 4712.4.  Note the exact length is between the two
        # estimates.
    def Test_Archimedean_toilet_paper_roll():
        '''A roll of toilet paper has an ID of 42 mm, an OD of 130 mm,
        and a thickness of about 0.125 mm.  Each sheet is 101x96 mm with
        the 101 mm dimension perpendicular to the perforations.  The
        manufacturer states there are 18 rolls in the package and the
        total area is 815.1 square feet.  Each roll is stated to have
        425 sheets on it, so that means the length of paper is 425(101
        mm) or 
        Check if this is approximately
        correct.  Use flt for calculations.
        '''
        num_rolls = 18
        mm = flt("1 mm")
        mm.n = 4
        ID, OD = mm(60), mm(130)
        fudge = 3.942
        width, thickness = mm(96), mm(0.125)*fudge
        pitch = 2*thickness
        length_actual = 425*mm(101)
        a = pitch/tau
        # Have to use ID.val because frange barfs on a flt
        f = lambda x:  float(x.val)
        # Since we know the stated length, use the approximate formula
        # to calculate what the thickness must be.
        length = mm(ApproximateSpiralArcLength(f(ID), f(OD),
                        f(thickness)))
        length_ft = length.to("ft")
        # The area per roll is the exact_length times the 101 mm
        # dimension
        area_per_roll = length*width
        area_per_roll_ft2 = area_per_roll.to("ft2")
        total_area = num_rolls*area_per_roll
        A_calc_ft2 = total_area.to('ft2')
        A_exact_ft2 = flt("815 ft2")
        assert_equal(A_calc_ft2, A_exact_ft2, reltol=0.01)
        if 0:   # Dump the variables
            d = locals()
            for i in sorted(d.keys()):
                if i in "flt tau mm f".split():
                    continue
                print(f"{i}: {d[i]}")
    exit(run(globals(), halt=1)[0])
