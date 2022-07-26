'''
Math-related functions
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
    # <math> Math-related functions
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    import math
    import string
    import sys
    from fractions import Fraction
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from frange import frange
    from f import flt
if 1:   # Global variables
    ii = isinstance
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
    ## constant term and coef[-1] is the highest term; x is a number.
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
 
    The smaller thickness*(OD - ID) is, the better the approximation.
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
def CountBits(num):
    '''Return (n_on, n_off), the number of 'on' and 'off' bits in the 
    integer num.
    '''
    if not isinstance(num, int):
        raise ValueError("num must be an integer")
    s = list(bin(num)[2:])
    on  = sum([i == "1" for i in s])
    off = sum([i == "0" for i in s])
    return (on, off)
def DecimalToBase(num, base, check_result=False):
    '''Convert a decimal integer num to a string in base base.  Tested with
    random integers from 10 to 10,000 digits in bases 2 to 36 inclusive.
    Set check_result to True to assure that the integer was converted
    properly.
    '''
    if not 2 <= base <= 36:
        raise ValueError('Base must be between 2 and 36.')
    if num == 0:
        return "0"
    s, sign, n = "0123456789abcdefghijklmnopqrstuvwxyz", "", abs(num)
    if num < 0:
        sign, num = "-", abs(num)
    d, in_base = dict(zip(range(len(s)), list(s))), ""
    while num:
        num, rem = divmod(num, base)
        in_base = d[rem] + in_base
    if check_result and int(in_base, base) != n:
        raise ArithmeticError("Base conversion failed for %d to base %d" %
                              (num, base))
    return sign + in_base
def Int(s):
    '''Convert the string x to an integer.  Allowed forms are:
    Plain base 10 string
    0b binary
    0o octal
    0x hex
    '''
    neg = 1
    if s[0] == "-":
        neg = -1
        s = s[1:]
    if s.startswith("0b"):
        return neg*int(s, 2)
    elif s.startswith("0o"):
        return neg*int(s, 8)
    elif s.startswith("0x"):
        return neg*int(s, 16)
    else:
        return neg*int(s, 10)
def int2base(x, base):
    '''Converts the integer x to a string representation in a given
    base.  base may be from 2 to 94.
 
    Method by Alex Martelli
    http://stackoverflow.com/questions/2267362/convert-integer-to-a-string-in-a-given-numeric-base-in-python
    Modified slightly by DP.
    '''
    if not hasattr(int2base, "digits"):
        int2base.digits = (string.digits + string.ascii_letters +
                           string.punctuation)
    if not ii(base, int):
        raise TypeError(f"base must be an integer")
    if not (2 <= base <= len(int2base.digits)):
        n = len(int2base.digits)
        raise ValueError(f"base must be between 2 and {n} inclusive")
    if not isinstance(x, (int, str)):
        raise ValueError("Argument x must be an integer or string")
    y = int(x) if isinstance(x, str) else x
    sgn = -1 if y < 0 else 1
    if not y:
        return '0'
    y, answer = abs(y), []
    while y:
        answer.append(int2base.digits[y % base])
        y //= base
    if sgn < 0:
        answer.append('-')
    return ''.join(reversed(answer))
def base2int(x, base):
    '''Inverse of int2base.  Converts a string x in the indicated base
    to a base 10 integer.  base may be from 2 to 94.
    '''
    if not hasattr(base2int, "digits"):
        base2int.digits = (string.digits + string.ascii_letters +
                           string.punctuation)
    if not ii(base, int):
        raise TypeError(f"base must be an integer")
    if not (2 <= base <= len(base2int.digits)):
        n = len(int2base.digits)
        raise ValueError(f"base must be between 2 and {n} inclusive")
    if not isinstance(x, str):
        raise ValueError("Argument x must be a string")
    n, y = 0, reversed(x)
    n = 0
    for i, c in enumerate(y):
        try:
            val = base2int.digits.index(c)
        except Exception:
            raise ValueError(f"'{c}' not a valid character for base {base}")
        n += val*(base**i)
    return n
def int2bin(n, numbits=32):
    '''Returns the binary of integer n, using numbits number of
    digits.  Note this is a two's-complement representation.
    From http://www.daniweb.com/software-development/python/code/216539
    '''
    return "".join([str((n >> y) & 1) for y in range(numbits - 1, -1, -1)])
def Binary(n):
    '''convert an integer n to a binary string.  Example:  Binary(11549)
    gives '10110100011101'.
    '''
    if 0:
        # from http://www.daniweb.com/software-development/python/code/216539
        s, m = "", abs(n)
        if not n:
            return "0"
        while m > 0:
            s = str(m % 2) + s
            m >>= 1
        return "-" + s if n < 0 else s
    else:
        # Use built-in bin()
        return "-" + bin(n)[3:] if n < 0 else bin(n)[2:]
class bitvector(int):
    '''This convenience class is an integer that lets you get its bit
    values using indexing or slices.
 
    Examples:
        x = bitvector(9)
        x[3] returns 1
        x[2] returns 0
        x[2:3] returns 2
        x[123] returns 0    # Arbitrary bits can be addressed
        x[-1] raises an IndexError
 
    Suggested from python 2 code given by Ross Rogers at
    (http://stackoverflow.com/questions/147713/how-do-i-manipulate-bits-in-python)
    dated 29 Sep 2008.
    '''
    def __repr__(self):
        return "bitvector({})".format(self)
    def _validate_slice(self, slice):
        '''Check the slice object for valid values; raises an IndexError if
        it's improper.  Return (start, stop) where the values are valid
        indices into the binary value.  Note that start and stop values can
        be any integers >= 0 as long as start is less than or equal to
        stop.
        '''
        start, stop, step = slice.start, slice.stop, slice.step
        # Check start
        if start is None:
            start = 0
        elif start < 0:
            raise IndexError("Slice start cannot be < 0")
        # Check stop
        if stop is None:
            stop = int(math.log(self)/math.log(2))
        elif stop < 0:
            raise IndexError("Slice stop cannot be < 0")
        if step is not None:
            raise IndexError("Slice step must be None")
        if start > stop:
            raise IndexError("Slice start must be <= stop")
        return start, stop
    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop = self._validate_slice(key)
            return bitvector((self >> start) & (2**(stop - start + 1) - 1))
        else:
            try:
                index = int(key)
            except Exception:
                raise IndexError("'{}' is an invalid index".format(key))
            if index < 0:
                raise ValueError("Negative bit index not allowed")
            return bitvector((self & 2**index) >> index)
def bin2gray(bits):
    '''bits will be a string representing a binary number with the most
    significant bit at index 0; for example, the integer 13 would be
    represented by the string '1101'.  Return a string representing a Gray
    code of this number.
 
    Example:  If bits = '1011' (binary of the integer 13), this function
    returns '1011'.
    '''
    # Algorithm from http://rosettacode.org/wiki/Gray_code#Python
    b = [int(i) for i in bits]
    g = b[:1] + [i ^ ishift for i, ishift in zip(b[:-1], b[1:])]
    return ''.join([str(i) for i in g])
def gray2bin(bits):
    '''bits will be a string representing a Gray-encoded binary number.
    Return a string representing a binary number with the most significant
    bit at index 0.
 
    Example:  If bits = '1101', this function returns '1101', the binary
    form of the integer 13.
    '''
    # Algorithm from http://rosettacode.org/wiki/Gray_code#Python
    Bits = [int(i) for i in bits]
    b = [Bits[0]]
    for nextb in Bits[1:]:
        b.append(b[-1] ^ nextb)
    return ''.join([str(i) for i in b])
def InterpretFraction(s):
    '''Interprets the string s as a fraction.  The following are
    equivalent forms:  '5/4', '1 1/4', '1-1/4', or '1+1/4'.  The
    fractional part in a proper fraction can be improper:  thus,
    '1 5/4' is returned as Fraction(9, 4).
    '''
    if "/" not in s:
        raise ValueError("'%s' must contain '/'" % s)
    t = s.strip()
    # First, try to convert the string to a Fraction object
    try:
        return Fraction(t)
    except ValueError:
        pass
    # Assume it's of the form 'm[ +-]n/d' where m, n, d are
    # integers.
    msg = "'%s' is not of the correct form" % s
    neg = True if t[0] == "-" else False
    fields = t.replace("+", " ").replace("-", " ").strip().split()
    if len(fields) != 2:
        raise ValueError(msg)
    try:
        ip = abs(int(fields[0]))
        fp = abs(Fraction(fields[1]))
        return -(ip + fp) if neg else ip + fp
    except ValueError:
        raise ValueError(msg)
def ProperFraction(fraction, separator=" "):
    '''Return the Fraction object fraction in a proper fraction string
    form.
 
    Example:  Fraction(-5, 4) returns '-1 1/4'.
    '''
    if not isinstance(fraction, Fraction):
        raise ValueError("frac must be a Fraction object")
    sgn = "-" if fraction < 0 else ""
    n, d = abs(fraction.numerator), abs(fraction.denominator)
    ip, numerator = divmod(n, d)
    return "{}{}{}{}/{}".format(sgn, ip, separator, numerator, d)
def mantissa(x, digits=6):
    '''Return the mantissa of the base 10 logarithm of x rounded to the
    indicated number of digits.
    '''
    return round(math.log10(significand(x, digits=digits)), digits)
def significand(x, digits=6):
    '''Return the significand of x rounded to the indicated number of
    digits.
    '''
    s = SignSignificandExponent(x)[1]
    return round(s, digits - 1)
def SignSignificandExponent(x, digits=15):
    '''Returns a tuple (sign, significand, exponent) of a floating point
    number x.
    '''
    s = ("%%.%de" % digits) % abs(float(x))
    return (1 - 2*(x < 0), float(s[0:digits + 2]), int(s[digits + 3:]))
def signum(x, ret_type=int):
    '''Return a number -1, 0, or 1 representing the sign of x.
    '''
    if x < 0:
        return ret_type(-1)
    elif x > 0:
        return ret_type(1)
    return ret_type(0)
def Percentile(seq, fraction):
    '''Return the indicated fraction of a sequence seq of sorted
    values.  fraction will be converted to be in [0, 1].
 
    The method is recommended by NIST at
    https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm.  
    
    The algorithm is:
 
        Suppose you have N numbers Y_[1] to Y_[N].  For the pth percentile,
        let x = p*(N + 1) and
      
          k = int(x)      [Integer part of x], d >= 0
          d = x - k       [Fractional part of x], d in [0, 1)
      
        Then calculate
      
          1.  For 0 < k < N, Y_(p) = Y_[k] + d*(Y_[k+1] - Y_[k]).
          2.  For k = 0, Y_[p] = Y[1].  Note that any p <= 1/(N+1) will be
              set to the minimum value.
          3.  For k >= N, Y_(p) = = Y_[N].  Note that any p > N/(N+1) will
              be set to the maximum value.
      
          Note the array indexing is 1-based, so python code will need to
          take this into account.
  
    Example:  A gauge study resulted in 12 measurements:
  
         i  Measurements   Sorted       Ranks
        --- ------------   -------      -----
         1     95.1772     95.0610        9
         2     95.1567     95.0925        6
         3     95.1937     95.1065       10
         4     95.1959     95.1195       11
         5     95.1442     95.1442        5
         6     95.0610     95.1567        1
         7     95.1591     95.1591        7
         8     95.1195     95.1682        4
         9     95.1065     95.1772        3
        10     95.0925     95.1937        2
        11     95.1990     95.1959       12
        12     95.1682     95.1990        8
  
    To find the 90th percentile, we have p*(N+1) = 0.9*13 = 11.7.  Then 
    k = 11 and d = 0.7.  From step 1 above, we estimate Y_(90) as
  
        Y_(90) = Y[11] + 0.7*(95.1990 - 95.1959) = 95.1981
  
    Note this algorithm will work for N > 1.
 
    http://code.activestate.com/recipes/511478-finding-the-percentile-of-the-values/
    gives another algorithm, but it doesn't give the same results as the
    NIST algorithm.
    '''
    if not seq:
        return None
    N = len(seq)
    if N == 1:
        raise ValueError("Sequence must have at least 2 elements")
    fraction = max(min(fraction, 1), 0)
    x = fraction*(N + 1)
    k = int(x)      # Integer part of x
    d = x - k       # Fractional part of x
    if 0 < k < N:
        yk = seq[k - 1]
        y = yk + d*(seq[k] - yk)
    elif k >= N:
        y = seq[-1]
    else:
        y = seq[0]
    return y
def LengthOfRopeOnDrum(dia, width, flange_dia, barrel_dia):
    '''Return the length of rope of diameter dia that will fit on a
    winch drum of diameter barrel_dia.  The width of winding area is
    width and the maximum diameter of the drum's flange is flange_dia.
    These variables are in inches and the output length is in ft.
    '''
    # Formula from Sampson Rope Users Manual pg. 28.  Note the formula
    # is for all input variables in inches and output length in feet.
    A = width
    B = flange_dia
    C = barrel_dia
    rope_dia = dia
    L = flt(A*(B**2 - C**2)/(15.3*rope_dia**2))
    return L
    '''Here's a post on math.stackexchange that discusses this problem
    https://math.stackexchange.com/questions/3853557/how-to-calculate-the-length-of-cable-on-a-winch-given-the-rotations-of-the-drum
 
    Let's let n be the number of complete layers already laid down, and t be
    the number of turns in the current (partial) layer, and s be the length
    of cable currently wound on the spool. Given the other constants (drum
    diameter, drum width, cable diameter), you'd like
 
    A formula that converts n,t into s
 
    A formula that converts s into n,t
 
    each of them without loops if possible, and with the property that
 
    if you start with some n,t, convert to s, and convert back, you get back
    the same n,t you started with, and if you start with s, convert to
    (n,t), and then back to s, you get the same s you started with.  Before
    I jump into this, I want to observe that property 3 is almost impossible
    on a computer. If you start with a number x, compute its square root,
    and square that, you'll get back something very close to x, but not, in
    general, actually equal to x -- they'll differ in the 10th or 12th or
    20th digit somewhere. So testing for perfect equality of floating-point
    numbers is always a bad idea. The most you can hope for is approximate
    equality. Notice, however, that an error in the 20th digit in the
    reconstructed value for s is hugely smaller than the variation in the
    length of s due to differing loads on the winch, different temperature
    (because everything has a temperature coefficient, even your drum!), and
    probably amounts to something less than a wavelength of light in the
    cable-length --- a far tinier error than you have in your measurement of
    your (physical) drum or cable. In short: don't expect equality.
 
    I also want to note that I think your model of cable winding on a spool
    is probably a bit broken --- unless the diameter of the cable is small
    compared to the diameter of the drum, you probably want to worry about
    the fact that individual wraps are not circles, but are helixes. And at
    the end of a layer, the "climb up" to the next layer isn't really
    accounted for. Perhaps none of these matters for you, but they are
    caveats: my answer assumes that your model is a good one, and solves the
    problems you posed within that context only.
 
    As I said, I'm going to answer the question you asked. Your "side note"
    at the bottom makes me worry that this will all be of no use. It's
    incredibly easy to change a problem from one that's easy to solve into
    one that's impossible. Find an elementary antiderivative for x↦exp(−x)?
    Easy. Find one for x↦exp(−x2)? Impossible. I just say this so that
    you're warned.
 
    Letting w be the constant number of turns per full layer, d the drum
    diameter, and h the rope diameter...here goes.
 
    To convert (n,t) into s (only valid when t≤w, of course):
 
    Let's start with a largish value of n, to detect a pattern:
 
    Total length on layer 1: w(π(d+h))
 
    Total length on layer 2: w(π(d+2h))
 
    Total length on layer 3: w(π(d+3h))
 
    ...
 
    Total length on layer (n−1): w(π(d+(n−1)h))
 
    Total length on layer n: w(π(d+nh))
 
    Total length on layer n: t(π(d+(n+1)h))
 
    So the total length on the first n−1 layers is
 
    T1=πw[(d+h)+(d+2h)+…+(d+nh)]
 
    Within the brackets, there are n copies of d,which I'll gather together:
 
    T1=πw[nd+(h+2h+…+nh)]
 
    and then I factor out an h to get
 
    T1=πw[nd+h(1+2+…+n)]
 
    Now I have to pull out a formula, due to Gauss, for the sum of the first
    n positive integers, namely,
 
    1+2+…+n=(n(n+1))/2.
 
    So we can write
 
    T1=πw[nd+h(n(n+1)/2)]
 
    and then simplify to get
 
    T1=πwn[d+h(n+1)2].
 
    We add to this the total length on the (n+1)th layer, which is
    t(π(d+(n+1)h)), and we get
 
    s=T1+t(π(d+(n+1)h))=πwn[d+h(n+1)/2]+t(π(d+(n+1)h))
 
    At this point, it's nice to divide through by π just to make things
    prettier, and to multiply by 2 to get rid of fractions; we'll get back
    to s in a while. So we have
 
    2sπ=2wn[d+h(n+1)/2]+2t(d+(n+1)h)
 
    and now I'm going to just do algebra to expand all of this to be a
    nicely expressed function of n.
 
    2s/π=2wnd+2wnh(n+1)/2+2td+2th(n+1)
        =2wdn+wnhn+wnh+2td+2thn+2th
        =(wh)n2+(2wd+wh+2th)n+2td+2th
        =(wh)n2+(2wd+wh+2th)n+2t(h+d)
 
    so that
 
    s=π/2((wh)n^2+(2wd+wh+2th)n+2t(h+d)).
 
    So that's part 1: you can compute the total length s wrapped up in n−1
    layers with t more turns on the nth layer using that formula.
 
    I'm going to rewrite that as a sum of two terms:
 
    s=π/2(whn^2+(2wd+wh)n)+π/2((2th)n+t(2d+2h))
 
    Let's call those S1 and S2, respectively. S1 is the stuff in the first n
    (complete) layers; S2 is the length due to the additional t turns on the
    (n+1)st layer.
 
    Now suppose we have s and want to find n and t. Let's start out by
    finding n. We need the total length of the completed layers to be no
    more than s, i.e., we need to find the largest integer n with S1≤s. So
    we're looking for the largest integer n with
 
    π/2(whn^2+(2wd+wh)n) ≤ s (1)
 
    Because the length of the wrapped-up rope is an increasing function of n
    (at least for n>0, which is all we care about), we can find the real
    number n0 that makes equation 1 into an equality --- maybe we find that
    6.3 layers would produce our chosen value s. Well, you can't have 6.3
    layers, but the largest whole number of layers you can have that'll fit
    is 6 layers, and then you have to compute how many more wraps there will
    in the 7th layer to get all the way to s. So let's change to equality in
    equation 1, and solve:
 
    s = π/2(whn^2+(2wd+wh)n)
    2s/π = whn^2+(2wd+wh)n
    0=whn^2+(2wd+wh)n−2s/π
    0 =An^2+Bn+C, where
    A = wh
    B = (2wd+wh)
    C =−2s/π
 
    We can solve this with the quadratic formula, choosing the "plus" part
    of the plus-or-minus to avoid negative values of n, and get
 
    2wh(n_0) = -(2wd + wh) + sqrt((2wd+wh)^2 + 8whs/π)
 
    That'll be some typically non-integer number, but we can compute n to be
    the "floor" of n0, i.e., the result of rounding down to the nearest
    whole number. (The floor of 3.8 is 3; the floor of 7 is 7.)
 
    Now knowing n, the number of complete layers, we know the length of the
    cable in those layers is given by S1, i.e., it's
 
    s1=π/2(whn^2+(2wd+wh)n)
 
    Now the remaining part, s2, must be s−s1, so to find t, we need to solve
 
    π/2((2th)n+t(2d+2h))=s−s1
 
    for t. Let's do it!
 
    π/2((2th)n+t(2d+2h)) = s -s1
    (2th)n+t(2d+2h) = 2/π(s-s1)
    t(2nh)+t(2d+2h) = 2/π(s-s1)
    t(2nh+2d+2h)
    t = (2/π)(s−s1)/(2nh+2d+2h)
 
    and we're done.
 
    The only remaining question is whether this all works.
 
    It does: here's Matlab code that runs the operations both ways. THe
    result, when this is run, is to print out 200 zeroes (i.e., the input
    length and output lengths agree).
 
    ---------------------------------------------------------------------
    function test()
    for s = 1:200
        [n, t] = layersAndTurns(s); 
        sp = cableLength(n, t); 
        s - sp  % print out the difference between the two values.
    end
 
    function s = cableLength(n, t)
    % Express total length of cable as a function of the number of complete
    % layers, n, and the number, t, of turns on the (n+1)-st layer. Depends on 
    % constants d = drum diameter, w = number of turns in a full layer, and 
    % h = cable diameter. 
    w = 10;
    d = 20; 
    h = 1; 
 
    s = (pi/2)*( w*h*n^2 + (2*w*d + w*h + 2*t*h)*n + 2*t*(h + d));
    %s = (pi/2) * ( w*h * n^2 + (2*w*d - w*h + 2*t*h)*n + 2*(t-w)*d);
 
    function [n, t] = layersAndTurns(s)
    % Given the total length of cable, determine the number, n, of full layers 
    % on the cable drum, and the number, t, of turns on the next (unfilled)
    % layer.  Depends on 
    % constants d = drum diameter, w = number of turns in a full layer, and 
    % h = cable diameter. 
    w = 10;
    d = 20; 
    h = 1; 
 
    n0 = (-(2*w*d + w*h) + sqrt((2*w*d + w*h)^2 + 8*w*h*s/pi))/(2*w*h);
    n = floor(n0); % The whole number of layers that fit. 
 
    s_1 = (pi/2) * (w * h * n^2 + (2*w*d + w*h)* n);
    t   = (2/pi) * (s - s_1)/(2*n*h + 2*d + 2*h);
    ---------------------------------------------------------------------
    answered Oct 6 '20 at 16:22
 
    John Hughes
    '''

if __name__ == "__main__": 
    from lwtest import run, raises, assert_equal, Assert
    from f import flt, tau, radians, log, sqrt
    from random import randint
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
        ## estimates.
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
        mm = flt("1") # mm
        mm.n = 4
        ID, OD = mm(60), mm(130)
        fudge = 3.942
        width, thickness = mm(96), mm(0.125)*fudge
        pitch = 2*thickness
        length_actual = 425*mm(101)
        a = pitch/tau
        # Have to use float because frange barfs on a flt
        f = lambda x:  float(x)
        # Since we know the stated length, use the approximate formula
        # to calculate what the thickness must be.
        length = mm(ApproximateSpiralArcLength(f(ID), f(OD), f(thickness)))
        length_ft = length*0.00328084
        # The area per roll is the exact_length times the 101 mm
        # dimension
        area_per_roll = length*width
        area_per_roll_ft2 = area_per_roll*1.07639e-05
        total_area = num_rolls*area_per_roll
        A_calc_ft2 = total_area*1.07639e-05
        A_exact_ft2 = flt("815")
        assert_equal(A_calc_ft2, A_exact_ft2, reltol=0.01)
        if 0:   # Dump the variables
            d = locals()
            for i in sorted(d.keys()):
                if i in "flt tau mm f".split():
                    continue
                print(f"{i}: {d[i]}")
    def Test_CountBits():
        bits = "0112122312"
        for i in range(10):
            Assert(CountBits(i)[0] == int(bits[i]))
    def Test_bitlength():
        Assert(bitlength(0) == 1)
        Assert(bitlength(1) == 1)
        Assert(bitlength(2) == 2)
        Assert(bitlength(255) == 8)
        Assert(bitlength(256) == 9)
    def TestDecimalToBase():
        # Generate a few random integers and check the results with
        # python's int() built-in.
        for base in range(2, 37):
            for i in range(100):
                x = randint(0, int(1e6))
                # Note the following call also checks the result
                s = DecimalToBase(x, base, check_result=True)
    def TestInt():
        data = (
            ("0b11", 3),
            ("0o10", 8),
            ("0x10", 16),
            ("10", 10),
            ("-0b11", -3),
            ("-0o10", -8),
            ("-0x10", -16),
            ("-10", -10),
        )
        for s, n in data:
            Assert(Int(s) == n)
    def Test_int2base():
        raises(ValueError, int2base, "", 2)
        raises(ValueError, int2base, 0, 370)
        x = 12345
        Assert(int2base(x, 2) == bin(x)[2:])
        Assert(int2base(x, 8) == oct(x)[2:])
        Assert(int2base(x, 16) == hex(x)[2:])
        Assert(int2base(36**2, 36) == "100")
        s = "53,kkns^~laU"
        Assert(int2base("255" + str(2**64), 94) == s)
    def Test_base2int():
        s = "53,kkns^~laU"
        Assert(base2int(s, 94) == int("255" + str(2**64)))
    def Test_int2bin():
        Assert(int2bin(-33, 8) == "11011111")
        Assert(int2bin( 33, 8) == "00100001")
    def TestBinary():
        d = '''
        -1000 -1111101000
        -501 -111110101
        -500 -111110100
        -499 -111110011
        -16 -10000
        -15 -1111
        -14 -1110
        -13 -1101
        -12 -1100
        -11 -1011
        -10 -1010
        -9 -1001
        -8 -1000
        -7 -111
        -6 -110
        -5 -101
        -4 -100
        -3 -11
        -2 -10
        -1 -1
        0 0
        1 1
        2 10
        3 11
        4 100
        5 101
        6 110
        7 111
        8 1000
        9 1001
        10 1010
        11 1011
        12 1100
        13 1101
        14 1110
        15 1111
        16 10000
        499 111110011
        500 111110100
        501 111110101
        999 1111100111
        1000 1111101000
        '''.strip()
        for line in d.split("\n"):
            n, b = line.strip().split()
            n = int(n)
            Assert(Binary(n) == b)
    def Test_bitvector():
        if 1:
            # This test probably worked under python 2, but not under 3.
            # The failure is a maximum recursion depth exceeded, so it's a
            # repr() or str() calling str() a bunch of times
            return
        s = "9"
        bv = bitvector(s)
        Assert(str(bv) == s)
        Assert(repr(bv) == "bitvector({})".format(s))
        binary = bin(int(s))[2:] + "0"*8
        for i, value in enumerate(binary):
            Assert(bv[i] == int(value))
        Assert(bv[1000] == 0)   # Check a high bit number
    def Test_GrayConversions():
        # Test integers from 0 to 15
        gray = "0 1 11 10 110 111 101 100 1100 1101 1111 1110 1010 1011 1001 1000"
        for i, g in enumerate(gray.split()):
            b = gray2bin(g)
            Assert(b == bin(i)[2:])
            g1 = bin2gray(b)
            Assert(g1 == g)
    def TestInterpretFraction():
        expected = Fraction(5, 4)
        Assert(InterpretFraction("5/4") == expected)
        Assert(InterpretFraction("1 1/4") == expected)
        Assert(InterpretFraction("1+1/4") == expected)
        Assert(InterpretFraction("1-1/4") == expected)
        #
        Assert(InterpretFraction("+5/4") == expected)
        Assert(InterpretFraction("+1 1/4") == expected)
        Assert(InterpretFraction("+1+1/4") == expected)
        Assert(InterpretFraction("+1-1/4") == expected)
        #
        Assert(InterpretFraction("-5/4") == -expected)
        Assert(InterpretFraction("-1 1/4") == -expected)
        Assert(InterpretFraction("-1+1/4") == -expected)
        Assert(InterpretFraction("-1-1/4") == -expected)
        #
        Assert(InterpretFraction("1 1/1") == Fraction(2, 1))
        Assert(InterpretFraction("+1 1/1") == Fraction(2, 1))
        Assert(InterpretFraction("-1 1/1") == Fraction(-2, 1))
        #
        Assert(InterpretFraction("1 2/1") == Fraction(3, 1))
        Assert(InterpretFraction("+1 2/1") == Fraction(3, 1))
        Assert(InterpretFraction("-1 2/1") == Fraction(-3, 1))
        # Argument must contain "/" and be parseable
        raises(ValueError, InterpretFraction, "1")
        raises(ValueError, InterpretFraction, "1/")
        raises(ValueError, InterpretFraction, "/1")
    def TestProperFraction():
        Assert(ProperFraction(Fraction("-1")) == "-1 0/1")
        Assert(ProperFraction(Fraction("1")) == "1 0/1")
        Assert(ProperFraction(Fraction(-1, 1)) == "-1 0/1")
        Assert(ProperFraction(Fraction(1, 1)) == "1 0/1")
        Assert(ProperFraction(Fraction(-3, 1)) == "-3 0/1")
        Assert(ProperFraction(Fraction(3, 1)) == "3 0/1")
        Assert(ProperFraction(Fraction(5, 4)) == "1 1/4")
        Assert(ProperFraction(Fraction(-5, 4)) == "-1 1/4")
    def Test_mantissa():
        x = 1.234 
        mant = mantissa(x)
        Assert(mant == 0.091315)
    def Test_significand():
        x = math.pi*1e-10
        Assert(significand(x, digits=6) == 3.14159)
        Assert(significand(x, digits=2) == 3.1)
    def Test_SignSignificandExponent():
        s, m, e = SignSignificandExponent(-1.23e-4)
        Assert(s == -1 and m == 1.23 and e == -4)
    def Test_signum():
        Assert(signum(-5) == -1)
        Assert(signum(5) == 1)
        Assert(signum(0) == 0)
        t = float
        Assert(isinstance(signum(5, ret_type=t), t))
    def TestPercentile():
        s = sorted([  # NIST gauge study data from
            # https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm
            95.0610, 95.0925, 95.1065, 95.1195, 95.1442, 95.1567, 95.1591,
            95.1682, 95.1772, 95.1937, 95.1959, 95.1990])
        Assert(round(Percentile(s, -1), 4) == 95.0610)
        Assert(round(Percentile(s, 0), 4) == 95.0610)
        Assert(round(Percentile(s, 0.5), 4) == 95.1579)
        Assert(round(Percentile(s, 0.9), 4) == 95.1981)
        Assert(round(Percentile(s, 1), 4) == 95.1990)
        Assert(round(Percentile(s, 1.1), 4) == 95.1990)
        raises(ValueError, Percentile, [1], 0.5)
    def TestLengthOfRopeOnDrum():
        # All dimensions in inches
        A, B, C, dia = 72, 48, 12, 1
        expected = (A*(B**2 - C**2)/(15.3*dia**2))
        got = LengthOfRopeOnDrum(dia, A, B, C)
        assert_equal(got, expected, reltol=1e-10)
    exit(run(globals(), halt=1)[0])
