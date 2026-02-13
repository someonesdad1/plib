if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Math-related functions oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2014 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ math oo>
        <oo test ∞ run oo>
        <oo todo ∞ 
        
            - ∞∞2 Write docstring so pydoc works on it
            - ∞∞2 Divide up into sections by function types
            - SpiralArcLength() and RollArcLength() are duplicated in pgm/spiral,
              although this module would be a good location for the spiral-related
              functions
            - SignSignificandExponent:  allow it to also process Decimal and mpmath
              numbers.  Also change the significand to be a string instead of a float;
              this allows it to be used with mpmath and Decimal numbers.  First check
              what python scripts under plib would be affected by this type change.
            - Polynomial stuff:  itertool's examples (e.g. polynomial_eval) may have
              more efficient/standard implementations that can replace this stuff.
              Could also be customized to return flt instead of float, although the
              general techniques are type-unaware.
        
        oo>
    '''
    if 1:  # Standard imports
        import math
        import string
        import sys
        from fractions import Fraction
    if 1:  # Custom imports
        from frange import frange
        from f import flt
        import u
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        ii = isinstance
if 1:  # Classes
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
                return bitvector((self >> start) & (2 ** (stop - start + 1) - 1))
            else:
                try:
                    index = int(key)
                except Exception:
                    raise IndexError("'{}' is an invalid index".format(key))
                if index < 0:
                    raise ValueError("Negative bit index not allowed")
                return bitvector((self & 2**index) >> index)
if 1:  # Polynomial utilities
    # These routines were originally from
    # http://www.physics.rutgers.edu/~masud/computing/ in the file
    # WPark_recipes_in_python.html; I probably downloaded them before 2000.  This
    # URL is defunct.
    #
    # coef is a sequence of the polynomial's coefficients; coef[0] is the
    # constant term and coef[-1] is the highest term; x is a number.
    def polyeval(coef, x, lowest_first=True):
        '''Evaluate a polynomial with the stated coefficients.  Returns
        coef[0] + x(coef[1] + x(coef[2] +...+ x(coef[n-1] + coef[n]x)...)
        This is Horner's method.  If lowest_first is False, then the
        coefficients are in the opposite order with the highest degree
        coefficient first.
                    
        Example: polyeval((3, 2, 1), 6) = 3 + 2(6) + 1(6)**2 = 51
        '''
        f = reversed if lowest_first else lambda x: x
        p = 0
        for i in f(coef):
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
if 1:  # Spirals
    ''' 
    Length of an Archimedian spiral
        ref page 317 of Bartsch, "Handbook of Mathematical Formulas", 1974
        
        Symbols
            a = constant in polar equation of spiral
            θ = polar coordinate angle
            r = polar coordinate radius
            pitch = 2*pi*a = distance between spiral's revolutions
            s = arc length of spiral
            t = thickness of a material on a roll
            n = number of turns of a material on a roll
        
        A point moving on a radius vector from the origin at constant speed while the
        radius vector rotates about a pole at constant angular speed describes an
        Archimedean spiral.
        
        Motivation:  How much toilet paper is on a roll?  One way to measure it would be
        to roll it out.  This is perhaps the most accurate method.  But it would be nice
        to be able to estimate it from the roll's dimensions.  The function
        ArchimedianSpiralArcLength below will help you do this.
        
        The polar equation of this spiral is
        
            r = a*θ
        
        where θ is the angle and a is a constant.  For a spiral with multiple
        revolutions, the distance between the revolutions (i.e., the pitch) is 
                
            pitch = 2*pi*a 
        
            Example:  let a = 0.1.  Then r at 2*pi is 0.63 and at 4*pi is 1.26.  The
            distance between the spiral at the intersections on the x axis is thus the
            pitch.  Thus, the thickness of a roll and the spiral's pitch are the same
            measure.
        
        The arc length s is gotten from the integral from θ1 to θ2 of
        
            sqrt(r² + (dr/dθ)²) dθ
        
        Substituting the equation for a spiral, we get
        
            A = sqrt(θ² + 1)
            s = arc length = a/2*[θ*A + ln(θ + A)]
                           = a/2*(θ*A + sinh⁻¹θ)       (Bartsch's equivalent form)
        
        This is the formula for the total arc length from an angle of 0 (i.e., the
        origin of the polar coordinate system) to an angle of θ (remember θ is in
        radians).  
        
        For large θ, the approximation is s = a*θ²/2 because A is about θ and θ² will be
        large compared to ln(2θ).
    '''
    def SpiralArcLength(a, theta, degrees=False):
        '''Calculate the arc length of an Archimedian spiral from angle 0 to theta.
        theta is in radians unless degrees is True.  The number a is the constant in the
        polar equation for the spiral r = a*theta.  The formula is exact because it is
        from an integration.
        '''
        if a <= 0:
            raise ValueError("a must be > 0")
        if theta < 0:
            raise ValueError("theta must be >= 0")
        theta = radians(flt(theta)) if degrees else flt(theta)
        A = sqrt(theta*theta + 1)
        return flt(a)/2*(theta*A + math.log(theta + A))
    def RollArcLength(D, d, thickness):
        '''Return the length of a roll of material of the given thickness with inside
        diameter d and outside diameter D.  It is assumed the roll forms a spiral.
        '''
        a = 2*thickness/math.tau  # Parameter of an Archimedean spiral
        # Since the polar equation of a spiral is r = a*θ, we can calculate the
        # corresponding angle from θ = D/(2*a) using the diameter D.
        θd, θD = d/(2*a), D/(2*a)
        Ld, LD = SpiralArcLength(a, θd), SpiralArcLength(a, θD)
        return LD - Ld
if 1:  # Core functionality
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
        a, b = divmod(n.bit_length(), 2)
        x = 2**(a + b)
        while True:
            y = (x + n//x)//2
            if y >= x:
                return x
            x = y
    def CountBits(num):
        'Return (n_on, n_off), the number of on and off bits in the integer |num|'
        if not isinstance(num, int):
            raise TypeError("num must be an integer")
        s = list(bin(abs(num))[2:])
        return (sum([i == "1" for i in s]), sum([i == "0" for i in s]))
    def DecimalToBase(num, base, check_result=False):
        '''Convert a decimal integer num to a string in base base.  Tested with
        random integers from 10 to 10,000 digits in bases 2 to 36 inclusive.
        Set check_result to True to assure that the integer was converted
        properly.
        '''
        if not 2 <= base <= 36:
            raise ValueError("Base must be between 2 and 36.")
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
            raise ArithmeticError(
                "Base conversion failed for %d to base %d" % (num, base)
            )
        return sign + in_base
    def Int(s):
        '''Convert the string (or bytes) s to an integer.  Allowed forms are:
            - Plain base 10 string
            - 0b, 0B:  binary
            - 0o, 0O:  octal
            - 0x, 0X:  hex
            - u+, U+:  hex style for Unicode codepoints
        '''
        if not isinstance(s, (str, bytes, bytearray)):
            raise TypeError("s must be str, bytes, or bytearray")
        isstr = True if isinstance(s, str) else False
        neg = 1
        if s[0] == "-" or s[0] == ord("-"):
            neg = -1
            s = s[1:]
        if s.lower().startswith("0b" if isstr else b"0b"):
            return neg*int(s, 2)
        elif s.lower().startswith("0o" if isstr else b"0o"):
            return neg*int(s, 8)
        elif s.lower().startswith("0x" if isstr else b"0x"):
            return neg*int(s, 16)
        elif s.lower().startswith("u+" if isstr else b"u+"):
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
            a = string.digits + string.ascii_letters
            int2base.digits = a + string.punctuation
        if not ii(base, int):
            raise TypeError("base must be an integer")
        if not (2 <= base <= len(int2base.digits)):
            n = len(int2base.digits)
            raise ValueError(f"base must be between 2 and {n} inclusive")
        if not isinstance(x, (int, str)):
            raise ValueError("Argument x must be an integer or string")
        y = int(x) if isinstance(x, str) else x
        sgn = -1 if y < 0 else 1
        if not y:
            return "0"
        y, answer = abs(y), []
        while y:
            answer.append(int2base.digits[y % base])
            y //= base
        if sgn < 0:
            answer.append("-")
        return "".join(reversed(answer))
    def base2int(x, base):
        '''Inverse of int2base.  Converts a string x in the indicated base
        to a base 10 integer.  base may be from 2 to 94.
        '''
        if not hasattr(base2int, "digits"):
            a = string.digits + string.ascii_letters
            base2int.digits = a + string.punctuation
        if not ii(base, int):
            raise TypeError("base must be an integer")
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
        return "".join([str(i) for i in g])
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
        return "".join([str(i) for i in b])
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
        number x.  sign is -1 or 1, significand is a float, and exponent is an
        integer.
        '''
        s = ("%%.%de" % digits) % abs(float(x))
        return (1 - 2*(x < 0), float(s[0 : digits + 2]), int(s[digits + 3 :]))
    def signum(x, return_type=int):
        'Return a number -1, 0, or 1 representing the sign of x'
        if not x:
            return return_type(0)
        elif x > 0:
            return return_type(1)
        else:
            return return_type(-1)
    def Percentile(seq, fraction):
        '''Return the indicated fraction of a sequence seq of sorted values.  fraction
        will be converted to be in [0, 1].
        
        The method is recommended by NIST at
        https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm.
        
        The algorithm is:
        
            Suppose you have N numbers Y_[1] to Y_[N].  For the pth percentile,
            let x = p*(N + 1) and
            
              k = int(x)      [Integer part of x], d >= 0
              d = x - k       [Fractional part of x], d in [0, 1)
              
            Then calculate
            
              1.  For 0 < k < N, Y_(p) = Y_[k] + d*(Y_[k+1] - Y_[k]).
              2.  For k = 0, Y_[p] = Y[1].  Any p <= 1/(N+1) will be set to the
                  minimum value.
              3.  For k >= N, Y_(p) = = Y_[N].  Any p > N/(N+1) will be set to
                  the maximum value.
                  
              The algorithm's array indexing is 1-based, so python code needs to take
              this into account.
              
        Example:  A gauge study resulted in 12 measurements (data from above NIST URL):
        
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
            
        To find the 90th percentile, we have p*(N+1) = 0.9*13 = 11.7.  Then k = 11 and d
        = 0.7.  From step 1 above, we estimate Y_(90) as
        
            Y_(90) = Y[11] + 0.7*(95.1990 - 95.1959) = 95.1981
            
        Note this algorithm will work for N > 1.
        
        http://code.activestate.com/recipes/511478-finding-the-percentile-of-the-values/
        gives another algorithm, but it doesn't give the same results as the NIST
        algorithm.
        
        King's book on probability plotting gave a number of such estimating functions
        with i/(n + 1) one of the most common and easist to use.  This works well if you
        have an approximately linearizing function for the ordinates.  It's also the
        best for when you are analyzing data and making probablility plots by hand.  
        '''
        if not seq:
            return None
        N = len(seq)
        if N == 1:
            raise ValueError("Sequence must have at least 2 elements")
        fraction = max(min(fraction, 1), 0)
        x = fraction*(N + 1)
        k = int(x)  # Integer part of x
        d = x - k  # Fractional part of x
        if 0 < k < N:
            yk = seq[k - 1]
            y = yk + d*(seq[k] - yk)
        elif k >= N:
            y = seq[-1]
        else:
            y = seq[0]
        return y
    def LengthOfRopeOnDrum(rope_dia, drum_width, flange_dia, drum_dia, units="mm"):
        '''Return the length of rope of diameter rope_dia_in that will fit on a winch
        drum of diameter drum_dia.  The width of the winding area is width and the maximum
        diameter of the drum's flange is flange_dia.  The units keyword defines the
        units being used (you can use any in u.py) and the output length is in the same
        units.  This is based on the formula from "Sampson Rope Users Manual" pg. 28.

        ||                       ||  ^
        ||<--------- A --------->||  |      A = drum_width
        ||                       ||  |      B = flange diameter
        ||-----------------------||  |      C = drum diameter
        ||           ^           ||         D = rope diameter
        ||           C           ||  B 
        ||                       ||         Sampson's formula:
        ||           v           ||  |  Length(feet) = A*(B² - C²)/(15.3*D²)
        ||-----------------------||  |
        ||                       ||  |      where D = rope diameter in inches
        ||                       ||  |      and A, B, C are in inches
        ||                       ||  V

        Here's a post on math.stackexchange that discusses this problem
        https://math.stackexchange.com/questions/3853557/how-to-calculate-the-length-of-cable-on-a-winch-given-the-rotations-of-the-drum
        '''
        # Check parameters are > 0
        param = (rope_dia, drum_width, flange_dia, drum_dia)
        for i in param:
            assert i > 0, f"{i!r} is less than 0"
        assert flange_dia > drum_dia
        # Convert parameters to inches
        factor = u.u(units)/u.u("inches")
        rope, width, flange, drum = [i*factor for i in param]
        # Sampson's formula takes parameters in inches and returns feet
        L_ft = flt(width*(flange**2 - drum**2)/(15.3*rope**2))
        # Convert feet to the user's units
        return L_ft*u.u("ft")/u.u(units)
    def PythagoreanSum(x, y, epsilon=1e-9, watch=False):
        '''Computes sqrt(x**2 + y**2) using a cubically-convergent algorithm from Moler and
        Morrison 1983 (IBM J. Res. Develop. vol 27, no. 6, Nov 1983.  The algorithm is
        terminated when abs((p[i] - p[i-1])/p[i]) is less than abs(epsilon).  With floats,
        it will never need more than three iterations.  Set watch to True to see
        convergence.
        
        The benefit of this algorithm is that it avoids pernicious overflows or underflows
        caused by using the naive formula sqrt(x**2 + y**2).  It's also robust.  It's
        particularly fast when the magnitude of x and y different significantly.
        '''
        if not x and not y:
            return 0
        p, q, n, plast = max(abs(x), abs(y)), min(abs(x), abs(y)), 0, None
        while q:
            r = (q/p)**2
            s = r/(4 + r)
            p = p + 2*s*p
            q = s*q
            n += 1
            if plast is not None:   # Check for convergence
                diff = abs((p - plast)/p)
                if diff < abs(epsilon):
                    break
                if watch:
                    print(f"{n}: p = {p} q = {q}   diff = {diff}")
            plast = p
        return p

if __name__ == "__main__":
    from lwtest import run, raises, assert_equal, Assert
    from f import flt, radians, sqrt
    from random import randint
    from color import t
    from pprint import pprint as pp
    eps = 1e-15
    def Test_PythagoreanSum():
        assert_equal(PythagoreanSum(3, 4, epsilon=1e-16), 5, abstol=eps)
    def Test_polyeval():
        Assert(polyeval((3, 2, 1), 6) == 51)
        Assert(polyeval((1, 2, 3), 6, lowest_first=False) == 51)
        # Test with only constant
        Assert(polyeval((3,), 6) == 3)
        Assert(polyeval((3,), 8) == 3)
        Assert(polyeval((3,), 6, lowest_first=False) == 3)
        Assert(polyeval((3,), 8, lowest_first=False) == 3)
        # Test linear case
        Assert(polyeval((3, 1), 6) == 9)
        Assert(polyeval((3, 1), 8) == 11)
        Assert(polyeval((3, 1), 6, lowest_first=False) == 19)
        Assert(polyeval((3, 1), 8, lowest_first=False) == 25)
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
            n = 3*n // 2
    def Test_SpiralArcLength():
        # a = 1, one revolution
        a, theta = 1, 2*math.pi
        A = math.sqrt(theta**2 + 1)
        exact = a/2*(theta*A + math.log(theta + A))
        formula = SpiralArcLength(a, theta)
        assert_equal(exact, formula)
        # Get ValueError for a <= 0
        raises(ValueError, SpiralArcLength, -1, 1)
        raises(ValueError, SpiralArcLength, 0, 1)
        # Get ValueError for theta < 0
        raises(ValueError, SpiralArcLength, 1, -1)
    def Test_Archimedean_toilet_paper_roll():
        '''A roll of toilet paper has an ID of 42 mm, an OD of 130 mm, and a thickness
        of about 0.125 mm.  Each sheet is 101x96 mm with the 101 mm dimension
        perpendicular to the perforations.  
        
        The manufacturer states there are 18 rolls in the package and the total area is
        815.1 ft².  Each roll is stated to have 425 sheets on it.  The area on a single
        roll should then be 815.1/18 ft² or 45.28 ft².  Let's see how well the actual
        measurements give the same area.
        '''
        # All lengths in mm
        ID, OD = 60, 130
        width, thickness = 96, 0.125
        mm_to_ft = 1/25.4/12
        # Calculate the area of a roll
        length_ft = RollArcLength(OD, ID, thickness)*mm_to_ft
        width_ft = width*mm_to_ft
        area_roll = length_ft*width_ft
        expected_area = 45.28
        # It's within about 5%
        assert_equal(area_roll, expected_area, reltol=0.05)
    def Test_CountBits():
        bits = "0112122312"
        for i in range(10):
            Assert(CountBits(i)[0] == int(bits[i]))
    def TestDecimalToBase():
        # Generate a few random integers and check the results with
        # python's int() built-in.
        for base in range(2, 37):
            for i in range(100):
                x = randint(0, int(1e6))
                # Note the following call also checks the result
                DecimalToBase(x, base, check_result=True)
    def TestInt():
        data = (
            # Positive integers
            ("0b11", 3),
            ("0o10", 8),
            ("0x10", 16),
            ("10", 10),
                # Bytes
                (b"0b11", 3),
                (b"0o10", 8),
                (b"0x10", 16),
                (b"10", 10),
            # Negative integers
            ("-0b11", -3),
            ("-0o10", -8),
            ("-0x10", -16),
            ("-10", -10),
                # Bytes
                (b"-0b11", -3),
                (b"-0o10", -8),
                (b"-0x10", -16),
                (b"-10", -10),
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
        Assert(int2bin(33, 8) == "00100001")
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
        Assert(bv[1000] == 0)  # Check a high bit number
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
        Assert(isinstance(signum(5, return_type=float), float))
    def TestPercentile():
        s = sorted(
            [  # NIST gauge study data from
                # https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm
                95.0610,
                95.0925,
                95.1065,
                95.1195,
                95.1442,
                95.1567,
                95.1591,
                95.1682,
                95.1772,
                95.1937,
                95.1959,
                95.1990,
            ]
        )
        Assert(round(Percentile(s, -1), 4) == 95.0610)
        Assert(round(Percentile(s, 0), 4) == 95.0610)
        Assert(round(Percentile(s, 0.5), 4) == 95.1579)
        Assert(round(Percentile(s, 0.9), 4) == 95.1981)
        Assert(round(Percentile(s, 1), 4) == 95.1990)
        Assert(round(Percentile(s, 1.1), 4) == 95.1990)
        raises(ValueError, Percentile, [1], 0.5)
    def TestLengthOfRopeOnDrum():
        if 0:   # Old test when units were inches
            # All dimensions in inches
            A, B, C, dia = 72, 48, 12, 1
            expected = A*(B**2 - C**2)/(15.3*dia**2)
            got = LengthOfRopeOnDrum(dia, A, B, C)
            assert_equal(got, expected, reltol=1e-10)
        
        L = LengthOfRopeOnDrum(1, 20, 40, 10, units="inches")
        Assert(L == 23529.41176470588)
        L = LengthOfRopeOnDrum(1, 1, 2, 1, units="inches")
        Assert(L == 12*3/15.3)
        c = 25.4
        L = LengthOfRopeOnDrum(c, c, 2*c, c, units="mm")
        Assert(L == c*12*3/15.3)
    exit(run(globals(), halt=1)[0])
