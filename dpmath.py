'''
Math-related functions
'''
if 1:  # Header
    if 1:  # Standard imports
        import collections
        import decimal
        import fractions
        import math
        import os
        import random
        import re
        import string
        import typing as ty
    if 1:  # Custom imports
        import dptypes
        import f
        import u
        try:
            import uncertainties as unc
            _have_unc = True
        except ImportError:
            _have_unc = False
        try:
            import mpmath
            _have_mpmath = True
        except ImportError:
            _have_mpmath = False
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        g = dptypes.Constant()
    if 1:  # Types
        @ty.runtime_checkable
        class SupportsArithmetic(ty.Protocol):
            def __add__(self, other: ty.Any) -> ty.Self: ...
            def __mul__(self, other: ty.Any) -> ty.Self: ...
            def __lt__(self, other: ty.Any) -> bool: ...
            def __gt__(self, other: ty.Any) -> bool: ...
        # Tnumber is now a type that acts like most numbers
        Tnumber = ty.TypeVar("Tnumber", bound=SupportsArithmetic)
        if 1:   # Basic number types
            Treal = int | float | decimal.Decimal | fractions.Fraction
            Tnum = Treal | complex
            T_Round = ty.TypeVar("T_Round", int, float, complex, decimal.Decimal,
                                  fractions.Fraction, ty.Any)
if 1:  # Polynomial utilities
    def PolynomialEvaluate(x: Tnumber, coefficients: ty.Sequence[Tnumber]) -> Tnumber:
        '''Evaluate a polynomial with the given coefficients
        
        If coefficients = [c0, c1, c2], then the evaluated polynomial is 
                c0 + c1*x + c2*x**2
        Using Horner's method, this is ((c2*x + c1)*x + c0).
        
        Arguments
            x           Value to evaluate the polynomial at
            coefficients
                Coefficients of the polynomial.  The 0th element is the coefficient of
                x**0.
        
        Algorithm
            Uses Horner's method.  Let coefficients = c, an array from 0 to n.  Then
            the polynomial's value is ((⋯(c[n]*x + c[n-1])*x + c[n-2])*x + ⋯ + c0).
                    
        Example
            >>> PolynomialEvaluate((1, 2, 3), 4) 
                = 3 + 2*(6**1) + 4*(6**2) = 3 + 12 + 4*36 = 159
            polyeval((3, 2, 4), 6, lowest_first=False) 
                = 4 + 2*(6**1) + 3*(6**2) = 4 + 12 + 3*36 = 124
        '''
        if not coefficients:
            raise ValueError("Coefficients cannot be empty.")
        # Start with the highest-degree coefficient to avoid '0' initialization
        coeffs_rev = reversed(coefficients)
        value: Tnumber = next(coeffs_rev)
        for c in coeffs_rev:
            value = value*x + c
        return value
    def PolynomialDerivative(coefficients: ty.Sequence[Tnumber]) -> ty.Sequence[Tnumber]:
        '''Return a list of the coefficients of the derivative of a polynomial
        
        Example
            >>> PolynomialDerivative([3, 4, 5])
            [4, 10]
        '''
        result: list[Tnumber] = []
        for i in range(1, len(coefficients)):
            result.append(coefficients[i]*i)
        return result
    def PolynomialReduce(root: Tnumber, coefficients: ty.Sequence[Tnumber]) -> ty.Sequence[Tnumber]:
        '''Given a root of a polynomial, return the factored coefficients
        
        The coefficients are (c0, c1, ⋯, cn) and the polynomial is the sum c0 + c1*x +
        c2*x**2 + ⋯ + cn*x**n.  The term (x - root) exactly factors this polynomial;
        this function returns the coefficients of this factored polynomial.
        
        Example:  (x - 1)*(x - 2) is 2 - 3*x + x**2.  The two roots are 1 and 2.  The
        coefficients are (2, -3, 1).  PolynomialReduce(1, (2, -3, 1)) returns [-2, 1],
        which is -2 + x or (x - 2).
        '''
        results: list[Tnumber] = []
        # Initialize using first element (last in the original list)
        it = reversed(coefficients)
        try:
            first = next(it)
        except StopIteration:
            return []
        cumulsum: Tnumber = first
        results.append(cumulsum)
        for i in it:
            cumulsum = cumulsum*root + i
            results.append(cumulsum)
        results.reverse()
        return results[1:]
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
    def SpiralArcLength(a: float, theta: float, degrees: bool=False) -> float:
        '''Given an angle, return the arc length of an Archimedian spiral
        
        The angle varies from 0 to theta.  The formula is exact because it is from an
        integration:  a/2*[θ*A + ln(θ + A)] where A = sqrt(θ² + 1) and θ = theta.
        
        Arguments
            a       The constant in the polar equation r = a*theta
            theta   The total angle of revolution of the spiral
            degrees If True, theta is in degrees
        
        Example
            >>> SpiralArcLength(1, 360, degrees=True)
            21.256294148209097
        '''
        if a <= 0:
            raise ValueError("a must be > 0")
        if theta < 0:
            raise ValueError("theta must be >= 0")
        theta = math.radians(theta) if degrees else theta
        A = math.sqrt(theta*theta + 1)
        return a/2*(theta*A + math.log(theta + A))
    def RollArcLength(D: float, d: float, thickness: float) -> float:
        '''Return the length of a roll of material of the given thickness with inside
        diameter d and outside diameter D.  It is assumed the roll forms a spiral.
        '''
        a = 2*thickness/math.tau  # Parameter of an Archimedean spiral
        # Since the polar equation of a spiral is r = a*θ, we can calculate the
        # corresponding angle from θ = D/(2*a) using the diameter D.
        θd, θD = d/(2*a), D/(2*a)
        Ld, LD = SpiralArcLength(a, θd), SpiralArcLength(a, θD)
        return LD - Ld
if 1:  # Ellipse circumference
    def EllipseCircumference(A: float, B: float, debug: bool = False) -> float:
        '''Return ellipse circumference A = maj dia, B = min dia
        
        Calculate the circumference of an ellipse with major diameter A and minor
        diameter B.  Relative accuracy is about 0.5^53 (about 1e-16).  Downloaded Mon 26
        May 2014 from http://paulbourke.net/geometry/ellipsecirc/python.code; also see
        the page http://paulbourke.net/geometry/ellipsecirc/.  This series converges
        quadratically and was first proposed by J. Ivory in 1798 (see
        https://en.wikipedia.org/wiki/James_Ivory_(mathematician)).
        
        The formula for the circumference of an ellipse is 2*a*E(e) where a is the major
        semidiameter, e is the eccentricity, and E is the complete elliptic integral of
        the second kind.  Thus, this function can also be used to calculate E.
        
        A quick check showed that Ivory's formula iterates about half as much as
        Weaver's EllipticE.  Since they agree in the tests to floating point precision,
        this method is preferred.
        
        Example
            >>> EllipseCircumference(1, 1)
            3.141592653589793
            >>> EllipseCircumference(1, 0)
            2.0
        '''
        if A < 0 or B < 0:
            raise ValueError("A and B must be >= 0")
        # Note the original formula is in terms of the 'semi-axes';
        # hence the division by 2.
        a, b = A/2, B/2
        x, y = max(a, b), min(a, b)
        digits = 53
        tol = math.sqrt(math.pow(0.5, digits))
        if digits*y < tol*x:
            return 4*x
        s, m = 0.0, 1.0
        while x - y > tol*y:
            x, y = 0.5*(x + y), math.sqrt(x*y)
            m *= 2.0
            s += m*math.pow(x - y, 2)
            if debug:
                val = math.pi*(math.pow(a + b, 2) - s)/(x + y)
                print(f"EllipseCircumference({A}, {B}, {val}")
        return math.pi*(math.pow(a + b, 2) - s)/(x + y)
if 1:  # RoundOff, SigFig, TemplateRound, Pound
    def RoundOff(number: T_Round, digits: int = 12, convert: bool = False) -> T_Round:
        '''Round the significand of number to the indicated number of digits and return
        the rounded number (integers and Fractions are returned untransformed).  number
        can be an int, float, Decimal, Fraction or complex number.
        
        If you have the mpmath library, mpf and mpc types can be rounded.  If you have
        the uncertainties library, UFloats can be passed in, but they will be returned
        unchanged.
        
        Rounding can get rid of trailing 0's and 9's:
                745.6998719999999               --> 745.699872
                4046.8726100000003              --> 4046.87261
                0.0254*12 = 0.30479999999999996 --> 0.3048
        so that printing the floating point representation is easier to read.
        
        If convert is True, then use float() to convert number to a floating point form.
        
        The digits keyword can be any integer greater than zero.  Arbitrary precisions
        with Decimal and mpmath mpf and mpc numbers are supported.
        
        The digits keyword defaults to 12 digits.  This is deliberate because
        virtually no practical problems need more digits if they're based on physical
        measurements (mathematical calculations are the exception where numerical
        accuracy may need to be assessed).  12 was chosen because it gives proper
        rounding in a number of practical test cases where 13 doesn't.  For example,
        
            x = math.pi/6
            math.sin(x) = 0.49999999999999994
            RoundOff(math.sin(x)) = 0.5
        '''
        if isinstance(number, (int, fractions.Fraction)):
            return number
        if _have_unc and isinstance(number, unc.UFloat):
            return number   # type: ignore
        if isinstance(number, complex):
            re = RoundOff(number.real, digits=digits)
            im = RoundOff(number.imag, digits=digits)
            # The following handles classes derived from complex
            return type(number)(re, im)     # type: ignore
        can_convert = False
        if convert and not isinstance(number, decimal.Decimal):
            try:
                float(number)
                can_convert = True
            except ValueError:
                pass
        if isinstance(number, float) or (convert and can_convert):
            # Convert to a decimal, then back to a float
            x = decimal.Decimal(number)
            with decimal.localcontext() as ctx:
                ctx.prec = digits
                x = +x
            return type(number)(x)  # Handles classes derived from floats
        elif isinstance(number, complex):
            return type(number)(
                RoundOff(number.real, digits=digits, convert=True),
                RoundOff(number.imag, digits=digits, convert=True),
            )
        elif isinstance(number, decimal.Decimal):
            with decimal.localcontext() as ctx:
                ctx.prec = digits
                number = +number
                return number
        elif _have_mpmath and isinstance(number, mpmath.mpf):
            x = decimal.Decimal(mpmath.nstr(number, mpmath.mp.dps))
            with decimal.localcontext() as ctx:
                ctx.prec = digits
                x = +x
                s = str(x)
                return mpmath.mpf(s)
        elif _have_mpmath and isinstance(number, mpmath.mpc):
            re = decimal.Decimal(mpmath.nstr(number.real, mpmath.mp.dps))
            im = decimal.Decimal(mpmath.nstr(number.imag, mpmath.mp.dps))
            with decimal.localcontext() as ctx:
                ctx.prec = digits
                re = +re
                im = +im
                sre, sim = str(re), str(im)
                with mpmath.workdps(digits):
                    z = mpmath.mpc(sre, sim)
                    return z
        else:
            raise TypeError("Unrecognized floating point type")
    def SigFig(x, clamp=True):
        '''Return the number of significant figures in the float x (x must be anything that can be
        converted to a float).  This is done by rounding to 12 figures, the default for RoundOff().
        Note you won't get more than 12 figures, even if the number has them.  The reason for this is
        that virtually no practical measured data ever has 12 figures (outside of physical
        laboratories like NIST or folks who work to their precisions).  If you do want more than 12,
        set clamp to False.
        
        Note that trailing '0' digits are removed, so a number like 30000 will have 1 significant
        figure, as will 30000.00.  If you're chronologically-gifted, you may have been taught that
        '30000.00' has seven significant figures.  Today, I recommend you use the notation
        '3.000000e4' instead to denote this.
        '''
        if x == 0:
            return 1
        radix = ".,"
        def RemoveTrailingZeroes(s):
            while s[-1] == "0":
                s = s[:-1]
            return s
        def RemoveRadix(s):
            for i in radix:
                s = s.replace(i, "")
            return s
        # Algorithm is to convert to scientific notation, parse out the
        # significand, remove the radix, and counts its digits.
        if clamp:
            y = RoundOff(float(x))
            s = f"{y:.12e}"
        else:
            s = f"{float(x):.16e}"
        m, e = s.split("e")
        t = str(float(m))
        t = RemoveRadix(t)
        t = RemoveTrailingZeroes(t)
        return len(t)
    def TemplateRound(x, template, up=None, roundoff=False):
        '''Round a number to a template number.
            - The returned value's type will be the same as template's type
            - template must be a number greater than zero
            - x/template must be a meaningful expression (x will be converted to
              template's type)
            - If up is None, then rounding is "simple", meaning the number is rounded up
              if the left-over fraction is 0.5 or larger
            - If up is True, then the fractional part is always rounded away from zero
            - If up is False, then the fractional part is always rounded towards zero
            - Supported types for template are int, float, flt, decimal.Decimal,
              fraction.Fraction, and mpmath.mpf
            - If roundoff is True, then the result x returned is filtered through 
              RoundOff(x), which rounds to 12 digits maximum.
            
        The algorithm determines how many template values are in x.  It is descended from the BASIC
        algorithm on pg 435 of the 31 Oct 1988 issue of "PC Magazine":
        
            DEF FNRound(Amount, Template) = SGN(Amount)*INT(0.5 + ABS(Amount)/Template)*Template
            
        Examples:
            TemplateRound(12, 10) = 10
            TemplateRound(12, 10, up=True) = 20
            TemplateRound(15, 10) = 20
            TemplateRound(15, 10, up=False) = 10
            
            The following example shows that this "rounding" can lead to numbers that don't look
            rounded.
            
                TemplateRound(1.6535, 0.1) = 1.7000000000000002
                TemplateRound(1.6535, flt(0.1)) = 1.7
                repr(TemplateRound(1.6535, flt(0.1))) = '1.7000000000000002'
                
            The root cause of the problem is that there's no floating point binary number equal to
            1.7.  Use Decimal or mpmath numbers for such a case:
            
                TemplateRound(Decimal("1.6535"), Decimal("0.1")) = 1.7
                TemplateRound(mpmath.mpf("1.6535"), mpmath.mpf("0.1")) = 1.7
                
            You can use fractions.Fraction too:
            
                TemplateRound(1.6535, Fraction(1, 8)) = 13/8
                
            which is correct, as 12/8 is 1.5 and 0.1535 is about 0.03 larger than 1/8.
        
            But the easiest fix is to set the roundoff keyword to True, which will work
            well for most cases, particularly if the number x is derived from some
            physical measurement, which will very rarely have more than perhaps 6 digits
            of significance.
        '''
        # Check inputs
        if template <= 0:
            raise ValueError("template must be > 0")
        tt = type(template)
        if not x:
            return tt(x)
        sign = tt(1) if x >= 0 else tt(-1)
        y = tt(int(abs(tt(x) / template) + tt(1) / tt(2)) * template)
        if up is not None:
            # Round toward or away from zero
            if sign < 0:
                up = not up
            if up and y < abs(tt(x)):  # Round away from zero
                y += template
            elif not up and y > abs(tt(x)):  # Round towards zero
                y -= template
        return sign * y
if 1:  # Core functions
    def Ceil(x, fp):
        'Ceiling function for type fp:  float, flt, mpf, Decimal'
        if fp is float or fp is f.flt:
            return int(math.ceil(x))
        elif _have_mpmath and fp is mpmath.mpf:
            return int(mpmath.ceil(x))
        elif fp is decimal.Decimal and x is decimal.Decimal:
            return int(x.to_integral_exact(rounding=decimal.ROUND_CEILING))
        else:
            raise TypeError(f"Type {fp} not supported")
    def Log2(x, fp):
        'Base 2 logarithm function for type fp:  float, flt, mpf, Decimal'
        if fp is float or fp is f.flt:
            return math.log2(x)
        elif _have_mpmath and fp is mpmath.mpf:
            return mpmath.log(x)/mpmath.log(2)
        elif fp is decimal.Decimal:
            assert x is decimal.Decimal
            return x.ln(x)/x.ln(2)
        else:
            raise TypeError(f"Type {fp} not supported")
    def IsBracketed(a, b, f, fp=float):
        '''Check that a and b bracket a root of f(x); raise ValueError if not.  Return
        the values (fp(f(a)), fp(f(b))) for convenience and to avoid recalculating them.
        '''
        fa, fb = fp(f(a)), fp(f(b))
        if fa*fb > 0:
            raise ValueError(f"a = {a} and b = {b} do not bracket a root of f")
        return (fa, fb)
    def Pound(z, adjust=True, ratio=2.5e-15):
        '''Turn z into a real if z.imag is small enough relative to the z.real and
        adjust is True.  Do the analogous thing for a nearly pure imaginary number.
        
        The name comes from imagining the complex number is a nail which a light tap
        from a hammer makes it lie parallel to either the real or imaginary axis.
        
        Set adjust to False so that only pure real or imaginary numbers are converted.
        
        Examples
            Pound(-6.9e-17+1j) --> 1j
            Pound(1-6.9e-17j) --> 1.0
            Pound(-6.9e-17+1j, ratio=1e-20) --> (-6.9e-17+1j)
            Pound(-6.9e-14+1j) --> (-6.9e-14+1j)
        '''
        if not isinstance(z, complex):
            if _have_mpmath and not isinstance(z, mpmath.mpc):
                return z
            else:
                return z
        if z.real and not z.imag:
            return z.real
        elif not z.real and z.imag:
            return 1j*z.imag
        # Adjust if the z.real/z.imag or z.imag/z.real ratio is small enough, otherwise
        # return z unchanged
        if adjust and z.real and abs(z.imag/z.real) <= ratio:
            return z.real
        elif adjust and z.imag and abs(z.real/z.imag) <= ratio:
            return 1j*z.imag
        else:
            return z
    def AlmostEqual(a, b, rel_err=2e-15, abs_err=5e-323):
        '''Determine whether floating-point values a and b are equal to
        within a (small) rounding error; return True if almost equal and
        False otherwise.  The default values for rel_err and abs_err are
        chosen to be suitable for platforms where a float is represented
        by an IEEE 754 double.  They allow an error of between 9 and 19
        ulps.
        
        This routine comes from the Lib/test/test_cmath.py in the python
        distribution; the function was called almostEqualF.
        
        ∞∞2 This should probably use math.isclose()
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
        d, in_base = dict(zip(range(len(s)), list(s), strict=True)), ""
        while num:
            num, rem = divmod(num, base)
            in_base = d[rem] + in_base
        if check_result and int(in_base, base) != n:
            raise ArithmeticError(f"Base conversion failed for {num} to base {base}")
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
        if not isinstance(base, int):
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
        if not isinstance(base, int):
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
            except Exception as e:
                raise ValueError(f"'{c}' not a valid character for base {base}") from e
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
        g = b[:1] + [i ^ ishift for i, ishift in zip(b[:-1], b[1:], strict=True)]
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
            raise ValueError(f"{s!r} must contain '/'")
        t = s.strip()
        # First, try to convert the string to a Fraction object
        try:
            return fractions.Fraction(t)
        except ValueError:
            pass
        # Assume it's of the form 'm[ +-]n/d' where m, n, d are
        # integers.
        msg = f"{s!r} is not of the correct form"
        neg = True if t[0] == "-" else False
        fields = t.replace("+", " ").replace("-", " ").strip().split()
        if len(fields) != 2:
            raise ValueError(msg)
        try:
            ip = abs(int(fields[0]))
            fp = abs(fractions.Fraction(fields[1]))
            return -(ip + fp) if neg else ip + fp
        except ValueError as e:
            raise ValueError(msg) from e
    def ProperFraction(fraction, separator=" "):
        '''Return the Fraction object fraction in a proper fraction string
        form.
        
        Example:  Fraction(-5, 4) returns '-1 1/4'.
        '''
        if not isinstance(fraction, fractions.Fraction):
            raise ValueError("frac must be a fractions.Fraction object")
        sgn = "-" if fraction < 0 else ""
        n, d = abs(fraction.numerator), abs(fraction.denominator)
        ip, numerator = divmod(n, d)
        return f"{sgn}{ip}{separator}{numerator}/{d}"
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
        s = f"{abs(float(x)):.{digits}e}"
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
        L_ft = f.flt(width*(flange**2 - drum**2)/(15.3*rope**2))
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
if 1:   # Stuff from util.py
    def AcceptableDiff(x, y, n=3, strict=False):
        '''Return True if abs((x - y)/x) <= 10ⁿ.  If x is 0, then calculate abs((y - x)/y).  If
        strict is True, then x and y must be the same numerical type.
        
        The use case for this is testing for numerical differences when the numbers come from physical
        measurements.  Most of the time such data have n = 2, 3, or 4 figures.
        '''
        if strict and (type(x) is not type(y)):
            raise TypeError("x and y must be the same numerical type")
        if x == y:
            return True
        if x:
            return abs((x - y)/x) <= 10**-n
        else:
            return abs((x - y)/y) <= 10**-n
    def Cumul(seq, check=False):
        '''Return the cumulative sum list of the given sequence seq.  If check is True, verify the last
        element of the returned array is equal to the sum of all the elements in seq.
        
        Example:  Cumul([1, 2, 3, 4, 7]) returns [1, 3, 6, 10, 17]
        '''
        cumul, dq = [], collections.deque(seq)
        while dq:
            item = dq.popleft()
            cumul.append(cumul[-1] + item) if cumul else cumul.append(item)
        if check and cumul and cumul[-1] != sum(seq):
            raise ValueError("Sum of sequence not same as last cumul element")
        return cumul
    def DoubleFactorial(n):
        '''Returns n!! which is defined to be the product from k = 0 to k = int(n/2) - 1 of (n - 2*k).
        Since we ensure that n is an integer, this function should never fail, but of course it will
        take a long time for big integers.
        
        Examples:
            If n is even, n!! = n(n - 1)(n - 4)···(4)(2)
                Or:  Product from k = 1 to n//2 of 2*k
            If n is odd,  n!! = n(n - 1)(n - 4)···(3)(1)
                Or:  Product from k = 1 to (n+1)//2 of 2*k - 1
        '''
        if not isinstance(n, int):
            raise TypeError("n must be an integer")
        if n < 0:
            raise ValueError("n must not be negative")
        product = 1
        for i in range(n, 0, -2):
            product *= i
        return product
    def IsConvexPolygon(*p):
        '''Return True if the sequence p of two-dimensional points constitutes a convex polygon.  Ref:
        http://stackoverflow.com/questions/471962/how-do-determine-if-a-polygon-is-complex-convex-nonconvex
        
        The assumption is that the sequence p of points traverses consecutive points of the polygon.
        
        The algorithm is to look at the triples of points and calculate the sign of the z component of
        their cross product.  The polygon is convex if the signs are either all negative or all
        positive.
        
        Examples:
            ((0, 0), (1, 0), (1, 1), (1, 0)) will return True.
            ((0, 0), (1, 0), (1, 1), (0.5,         0.5)) will return False.
            ((0, 0), (1, 0), (1, 1), (0.5 - 1e-10, 0.5)) will return True.
        '''
        n = len(p)
        if n < 3:
            raise ValueError("Need at least three points")
        cross_product_signs = []
        for index in range(n + 3):
            # Generate indices of the needed points
            i = index % n
            j = (index + 1) % n
            k = (index + 2) % n
            p1, p2, p3 = p[i], p[j], p[k]
            dx1 = p2[0] - p1[0]
            dy1 = p2[1] - p1[1]
            dx2 = p3[0] - p2[0]
            dy2 = p3[1] - p2[1]
            cross_product_signs.append(signum(dx1*dy2 - dy1*dx2))
        assert len(cross_product_signs) == n + 3
        if cross_product_signs[0] and len(set(cross_product_signs)) == 1:
            return True
    def ParseComplex(numstring):
        '''numstring contains a string representing a complex number that must be of the form 'x+yi';
        the complex unit can be i or j.  Return (real, imag) where real and imag are the real and
        imaginary strings of the complex number.  Space characters can be anywhere in the string, as
        they are removed.
        '''
        # The method uses a regular expression to recognize the string forms of integers or real
        # numbers.  Applied to the string twice, it picks out the real and imaginary parts.
        str = numstring.lower().strip().replace("i", "j").replace(",", ".").replace(" ", "")
        msg = f"{numstring!r} not a valid complex number string"
        # Check for illegal characters
        s = set(str)
        if not s.issubset(set("j+-e.0123456789")):
            raise ValueError(msg)
        # Regular expression to recognize an int or float
        regex = r'''
                (                               # Group
                    [+-]?                       # Optional sign
                    \.\d+                       # Number like .345
                    ([eE][+-]?\d+)?|            # Optional exponent
                # or
                    [+-]?                       # Optional sign
                    \d+\.?\d*                   # Number:  2.345
                    ([eE][+-]?\d+)?             # Optional exponent
                )                               # End group
                '''
        r = re.compile(regex, re.X)
        # If no 'j', it's real
        if str[-1] != "j":
            return (str, "")
        if 1:  # Extract real part
            first = ""
            mo = r.search(str)
            if mo:
                a, b = mo.span()
                first = str[a:b]
                str = str[b:]
            else:
                # It must have been only 'j' or '-j'
                if str[0] == "+" or str[0] == "j":
                    return ("", "1")
                elif str[0] == "-":
                    return ("", "-1")
                else:
                    raise ValueError(msg)
            if str == "j":
                # It was pure imaginary
                return ("", first)
        if 1:  # Extract imag part
            mo = r.search(str)
            if mo:
                a, b = mo.span()
                second = str[a:b]
                assert str[-1] == "j"
            else:
                # It can only be '+j' or '-j'
                if str == "+j":
                    second = "1"
                elif str == "-j":
                    second = "-1"
                else:
                    raise ValueError(msg)
        return (first, second)
    def RandomIntegers(n, maxint, seed=None, duplicates_OK=False):
        '''Return a random list of n integers between 0 and maxint - 1.  Set seed to be not None to
        generate a repeatable set of integers.  If duplicates_OK is False, the integers are distinct;
        otherwise, the list may contain duplicates.
        '''
        # Check parameters
        if not isinstance(n, int) or not isinstance(maxint, int):
            raise TypeError("n and maxint must be integers")
        if n <= 0:
            raise ValueError("n must be > 0")
        if not maxint and duplicates_OK:
            return [0]*n
        if not duplicates_OK and n > maxint:
            raise ValueError(
                f"maxint ({maxint}) is too small to generate {n} distinct integers"
            )
        s = [] if duplicates_OK else set()
        f = s.append if duplicates_OK else s.add
        numbytes = maxint.bit_length() // 8 + 1
        if seed is not None:
            random.seed(seed)
        while len(s) < n:
            if seed is None:
                f(int.from_bytes(os.urandom(numbytes), "big") % maxint)
            else:
                f(random.randint(0, maxint - 1))
        return list(s)
    def randq(seed=-1):
        '''The simple random number generator in the section "An Even Quicker Generator" from
        "Numerical Recipes in C", page 284, chapter 7, 2nd ed, 1997 reprinting (found on the web in PDF
        form).
        
        If seed is not -1, it is used to initialize the sequence; it can be any hashable value.
        '''
        if not hasattr(randq, "a"):
            # State variables for randq
            randq.a = 1664525  # Recommended by Knuth
            randq.c = 1013904223  # From Lewis
            randq.idum = 0
            randq.maxidum = 2**32
        if seed != -1:
            randq.idum = abs(hash(seed))
        randq.idum = (randq.a*randq.idum + randq.c) % randq.maxidum
        return randq.idum
    def randr(seed=-1):
        "Uses randq to return a floating point number on [0, 1)"
        n = randq(seed=seed) if seed != -1 else randq()
        return n/float(randq.maxidum)
    def SignificantFiguresS(value, digits=3, exp_compress=True):
        '''Returns a string representing the number value rounded to a specified number
        of significant figures.  The number is converted to a string, then rounded and
        returned as a string.  If you want it back as a number, use float() on the
        string.  If exp_compress is true, the exponent has leading zeros removed.
        
        The following types of printouts can be gotten using this function and native
        python formats:
        
            A              B               C               D
        3.14e-12       3.14e-012       3.14e-012       3.14e-012
        3.14e-11       3.14e-011       3.14e-011       3.14e-011
        3.14e-10       3.14e-010       3.14e-010       3.14e-010
        3.14e-9        3.14e-009       3.14e-009       3.14e-009
        3.14e-8        3.14e-008       3.14e-008       3.14e-008
        3.14e-7        3.14e-007       3.14e-007       3.14e-007
        3.14e-6        3.14e-006       3.14e-006       3.14e-006
        3.14e-5        3.14e-005       3.14e-005       3.14e-005
        3.14e-4        3.14e-004        0.000314        0.000314
        3.14e-3        3.14e-003         0.00314         0.00314
        3.14e-2        3.14e-002          0.0314          0.0314
        3.14e-1        3.14e-001           0.314           0.314
        3.14e+0        3.14e+000            3.14            3.14
        3.14e+1        3.14e+001            31.4            31.4
        3.14e+2        3.14e+002             314           314.0
        3.14e+3        3.14e+003       3.14e+003          3140.0
        3.14e+4        3.14e+004       3.14e+004         31400.0
        3.14e+5        3.14e+005       3.14e+005        314000.0
        3.14e+6        3.14e+006       3.14e+006       3140000.0
        3.14e+7        3.14e+007       3.14e+007      31400000.0
        3.14e+8        3.14e+008       3.14e+008     314000000.0
        3.14e+9        3.14e+009       3.14e+009    3140000000.0
        3.14e+10       3.14e+010       3.14e+010   31400000000.0
        3.14e+11       3.14e+011       3.14e+011  314000000000.0
        3.14e+12       3.14e+012       3.14e+012       3.14e+012
        
        A:  SignificantFiguresS(x, 3)
        B:  SignificantFiguresS(x, 3, 0)
        C:  "%.3g" % x
        D:  float(SignificantFiguresS(x, 3))
        '''
        if digits < 1 or digits > 15:
            msg = "Number of significant figures must be >= 1 and <= 15"
            raise ValueError(msg)
        sign, significand, exponent = SignSignificandExponent(float(value))
        fmt = f"%.{digits - 1:d}f"
        neg = "-" if sign < 0 else ""
        e = f"e{exponent:+d}" if exp_compress else f"e{exponent:+04d}"
        return neg + (fmt % significand) + e
    def SignificantFigures(value, figures=3):
        "Rounds a value to specified number of significant figures.  Returns a float."
        return float(SignificantFiguresS(value, figures))
if 1:  # Simple linear regression
    def LinearRegression(x, y):
        'Return (m, b, Rsquared) for a simple linear regression problem'
        if len(x) != len(y):
            raise ValueError("x and y are not same length")
        n, sx, sy = len(x), sum(x), sum(y)
        sXX = sum([i*i for i in x])
        sYY = sum([i*i for i in y])
        sXY = sum([i*j for i, j in zip(x, y, strict=True)])
        m = f.flt((n*sXY - sx*sy)/(n*sXX - sx**2))
        b = f.flt((sy - m*sx)/n)
        Rsquared = f.flt((n*sXY - sx*sy)**2/((n*sXX - sx**2)*(n*sYY - sy**2)))
        return (m, b, Rsquared)

if __name__ == "__main__":
    if 1:   # Standard imports
        import numbers
        import random
    if 1:   # Custom imports
        import lwtest
    if 1:   # Import symbols
        Assert = lwtest.Assert
        ToDoMessage = lwtest.ToDoMessage
        assert_equal = lwtest.assert_equal
        raises = lwtest.raises
        run = lwtest.run
    if 1:   # Global variables
        g.eps = 1e-15
    def Test_PythagoreanSum():
        assert_equal(PythagoreanSum(3, 4, epsilon=1e-16), 5, abstol=g.eps)
    def Test_PolynomialEvaluate():
        Assert(PolynomialEvaluate(6, (3, 2, 1)) == 51)
        Assert(PolynomialEvaluate(6, list(reversed((1, 2, 3)))) == 51)
        # Test with only constant
        Assert(PolynomialEvaluate(6, (3,)) == 3)
        Assert(PolynomialEvaluate(8, (3,)) == 3)
        # Test linear case
        Assert(PolynomialEvaluate(6, (3, 1)) == 9)
        Assert(PolynomialEvaluate(8, (3, 1)) == 11)
    def Test_PolynomialDerivative():
        Assert(PolynomialDerivative((3, 2, 1)) == [2, 2])
    def Test_polyreduce():
        # Use (x - 1)*(x - 2) = 2 - 3*x + x**2
        coefficients = (2, -3, 1)
        Assert(PolynomialReduce(1, coefficients) == [-2, 1])
    def Test_rect():
        Assert(rect(0, 0) == (0, 0))
        Assert(rect(0, 180, deg=True) == (0, 0))
        x, y = rect(1, 45, deg=True)
        s = math.sin(math.pi/4)
        assert_equal(x, s, abstol=g.eps)
        assert_equal(y, s, abstol=g.eps)
    def Test_polar():
        Assert(polar(0, 0) == (0, 0))
        Assert(polar(0, 1) == (1, math.pi/2))
        Assert(polar(0, -1) == (1, -math.pi/2))
        Assert(polar(-1, 0) == (1, math.pi))
        s = math.sin(math.pi/4)
        r, theta = polar(s, s, deg=True)
        assert_equal(r, 1, abstol=g.eps)
        assert_equal(theta, 45, abstol=g.eps)
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
    def Test_EllipseCircumference():
        assert_equal(EllipseCircumference(1, 1), math.pi, reltol=1e-14)
        assert_equal(EllipseCircumference(1, 1), math.pi, reltol=1e-14)
        # Gemini pulled this value from a table and originally set the reltol at 1e-9,
        # which was too tight
        assert_equal(EllipseCircumference(10, 8), 28.361652188, reltol=1e-6)
    def Test_CountBits():
        bits = "0112122312"
        for i in range(10):
            Assert(CountBits(i)[0] == int(bits[i]))
    def TestDecimalToBase():
        # Generate a few random integers and check the results with
        # python's int() built-in.
        for base in range(2, 37):
            for _ in range(100):
                x = random.randint(0, int(1e6))
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
        Assert(repr(bv) == f"bitvector({s})")
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
        expected = fractions.Fraction(5, 4)
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
        Assert(InterpretFraction("1 1/1") == fractions.Fraction(2, 1))
        Assert(InterpretFraction("+1 1/1") == fractions.Fraction(2, 1))
        Assert(InterpretFraction("-1 1/1") == fractions.Fraction(-2, 1))
        #
        Assert(InterpretFraction("1 2/1") == fractions.Fraction(3, 1))
        Assert(InterpretFraction("+1 2/1") == fractions.Fraction(3, 1))
        Assert(InterpretFraction("-1 2/1") == fractions.Fraction(-3, 1))
        # Argument must contain "/" and be parseable
        raises(ValueError, InterpretFraction, "1")
        raises(ValueError, InterpretFraction, "1/")
        raises(ValueError, InterpretFraction, "/1")
    def TestProperFraction():
        Assert(ProperFraction(fractions.Fraction("-1")) == "-1 0/1")
        Assert(ProperFraction(fractions.Fraction("1")) == "1 0/1")
        Assert(ProperFraction(fractions.Fraction(-1, 1)) == "-1 0/1")
        Assert(ProperFraction(fractions.Fraction(1, 1)) == "1 0/1")
        Assert(ProperFraction(fractions.Fraction(-3, 1)) == "-3 0/1")
        Assert(ProperFraction(fractions.Fraction(3, 1)) == "3 0/1")
        Assert(ProperFraction(fractions.Fraction(5, 4)) == "1 1/4")
        Assert(ProperFraction(fractions.Fraction(-5, 4)) == "-1 1/4")
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
        for i in (-1, -2, -2.2, fractions.Fraction(-1, 1), decimal.Decimal("-3.7")):
            assert_equal(signum(i), -1)
        for i in (0, 0.0, fractions.Fraction(0, 1), decimal.Decimal(0)):
            assert_equal(signum(i), 0)
        for i in (1, 2, 2.2, fractions.Fraction(1, 1), decimal.Decimal("3.7")):
            assert_equal(signum(i), 1)
        raises(TypeError, signum, "a")
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
    def Test_RoundOff():
        Assert(RoundOff(745.6998719999999) == 745.699872)
        Assert(RoundOff(745.6998719999999, 5) == 745.70)
        Assert(RoundOff(745.6998719999999, 4) == 745.7)
        Assert(RoundOff(745.6998719999999, 3) == 746)
        Assert(RoundOff(745.6998719999999, 2) == 750)
        Assert(RoundOff(745.6998719999999, 1) == 700)
        Assert(RoundOff(4046.8726100000003) == 4046.87261)
        Assert(RoundOff(-0.30479999999999996) == -0.3048)
    def Test_TemplateRound():
        # Routine floating point rounding
        a, t = 463.77, 0.1
        Assert(TemplateRound(-a, t, up=True) == -463.7)
        Assert(TemplateRound(-a, t, up=False) == -463.8)
        Assert(TemplateRound(a, t, up=True) == 463.8)
        Assert(TemplateRound(a, t, up=False) == 463.7)
        a, t = 463.77, 1.0
        Assert(TemplateRound(-a, t, up=True) == -463)
        Assert(TemplateRound(-a, t, up=False) == -464)
        Assert(TemplateRound(a, t, up=True) == 464)
        Assert(TemplateRound(a, t, up=False) == 463)
        a, t = 463.77, 10.0
        Assert(TemplateRound(-a, t, up=True) == -460)
        Assert(TemplateRound(-a, t, up=False) == -470)
        Assert(TemplateRound(a, t, up=True) == 470)
        Assert(TemplateRound(a, t, up=False) == 460)
        Assert(TemplateRound(123.48, 0.1, up=True) == 123.5)
        Assert(TemplateRound(123.48, 0.1, up=False) == 123.4)
        # Integer rounding
        a, t = 463, 1
        Assert(TemplateRound(-a, t, up=True) == -463)
        Assert(TemplateRound(-a, t, up=False) == -463)
        Assert(TemplateRound(a, t, up=True) == 463)
        Assert(TemplateRound(a, t, up=False) == 463)
        a, t = 463, 10
        Assert(TemplateRound(-a, t, up=True) == -460)
        Assert(TemplateRound(-a, t, up=False) == -470)
        Assert(TemplateRound(a, t, up=True) == 470)
        Assert(TemplateRound(a, t, up=False) == 460)
        # Decimal rounding
        a, t = decimal.Decimal("123.48"), decimal.Decimal("0.1")
        Assert(TemplateRound(a, t, up=True) == decimal.Decimal("123.5"))
        Assert(TemplateRound(a, t, up=False) == decimal.Decimal("123.4"))
        # Fraction rounding:  a will be 123+31/64, t will be 1/8
        a, t = 123 + fractions.Fraction(31, 64), fractions.Fraction(1, 8)
        Assert(TemplateRound(a, t, up=True) == fractions.Fraction(247, 2))
        Assert(TemplateRound(a, t, up=False) == fractions.Fraction(987, 8))
        # mpmath
        if _have_mpmath:
            mpf = mpmath.mpf
            a, t = mpf("123.48"), mpf("0.1")
            Assert(TemplateRound(a, t, up=True) == mpf("123.5"))
            Assert(TemplateRound(a, t, up=False) == mpf("123.4"))
    def Test_AlmostEqual():
        Assert(AlmostEqual(0, 0))
        Assert(AlmostEqual(0, 1e-353))
        Assert(AlmostEqual(1.0, 1.0))
        Assert(AlmostEqual(1, 1 + 2e-15))
        Assert(not AlmostEqual(1, 1 + 2.11e-15))
        Assert(AlmostEqual(1.0, 1.001, 1e-2))
        Assert(not AlmostEqual(1.0, 1.011, 1e-2))
    def Test_SigFig():
        from math import pi
        x = pi*1e8
        for n in range(1, 14):
            y = RoundOff(x, n)
            Assert(SigFig(y) == min(n, 12))
        x = 0.00081
        Assert(SigFig(x) == 2)
        x = 0.0001
        Assert(SigFig(x) == 1)
        x = 0.0000
        Assert(SigFig(x) == 1)
    def Test_LinearRegression():
        if 1:   # Identity function
            x = [1, 2]
            y = [1, 2]
            m, b, Rsq = LinearRegression(x, y)
            Assert((m, b, Rsq) == (1, 0, 1))
        if 1:   # Test case checked against HP-42s
            x = [1, 2, 3]
            y = [1, 2, 3.1]
            m, b, Rsq = LinearRegression(x, y)
            Assert(m == 1.0500000000000018)
            Assert(b == -0.06666666666667058)
            Assert(Rsq == 0.9992447129909383)
    def Test_Pound():
        '''Pound(z) returns a pure real or imaginary if z is close enough to
        the real or imaginary axis.
        '''
        def test1():
            Assert(Pound(0, True) == 0)
            Assert(Pound(1 + 1j, True) == 1 + 1j)
            for z, expected, t in (
                (1 + 0j, 1, numbers.Real),
                (1 - 0j, 1, numbers.Real),
                (-1 + 0j, -1, numbers.Real),
                (-1 - 0j, -1, numbers.Real),
                #
                (1 + 1e-16j, 1, numbers.Real),
                (1 - 1e-16j, 1, numbers.Real),
                (-1 + 1e-16j, -1, numbers.Real),
                (-1 - 1e-16j, -1, numbers.Real),
                #
                (1e-16 + 1e-32j, 1e-16, numbers.Real),
                (1e-16 - 1e-32j, 1e-16, numbers.Real),
                (-1e-16 + 1e-32j, -1e-16, numbers.Real),
                (-1e-16 - 1e-32j, -1e-16, numbers.Real),
                #
                (0 + 1j, 1j, numbers.Complex),
                (0 - 1j, -1j, numbers.Complex),
                (-0 + 1j, 1j, numbers.Complex),
                (-0 - 1j, -1j, numbers.Complex),
                #
                (1e-16 + 1j, 1j, numbers.Complex),
                (1e-16 - 1j, -1j, numbers.Complex),
                (-1e-16 + 1j, 1j, numbers.Complex),
                (-1e-16 - 1j, -1j, numbers.Complex),
            ):
                b = Pound(z)
                Assert(b == expected)
                Assert(isinstance(b, t))
        def test2():
            epsilon = 2.5e-15
            tol = 0.99*float(epsilon)
            # Zero
            Assert(Pound(0, 0) == 0)
            Assert(Pound(0j, 1) == 0)
            Assert(Pound(0 + 0j, 1) == 0)
            # Pure real
            Assert(Pound(1, 0) == 1)
            Assert(Pound(1, 1) == 1)
            Assert(Pound(1 + tol, 1) == 1 + tol)
            # Pure imaginary
            Assert(Pound(1j, 0) == 1j)
            Assert(Pound(1j, 1) == 1j)
            x = (1 + tol)*1j
            Assert(Pound(x, 1) == x)
            # Real with small imaginary part
            x = 1
            y = x + tol*1j
            Assert(Pound(y, 0) == y)
            Assert(Pound(y, 1) == x)
            # Imaginary with small real part
            y = tol + x*1j
            Assert(Pound(y, 0) == y)
            Assert(Pound(y, 1) == x*1j)
            # Number that shouldn't be changed
            x = 1 + 1j
            Assert(Pound(x, 0) == x)
            Assert(Pound(x, 1) == x)
        test1()
        test2()
    if 1:   # Test stuff from util.py
        def Test_AcceptableDiff():
            Assert(AcceptableDiff(0, 0))
            Assert(not AcceptableDiff(1, 1.01))
            Assert(AcceptableDiff(1, 1.001))
            raises(TypeError, AcceptableDiff, 1, 1.1, strict=True)
        def Test_Cumul():
            for a in ([], [0], [0, 1]):
                Assert(Cumul(a, check=True) == a)
            a = [0, 1, 2]
            Assert(Cumul(a, check=True) == [0, 1, 3])
            a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            Assert(Cumul(a, check=True) == [0, 1, 3, 6, 10, 15, 21, 28, 36, 45])
        def Test_DoubleFactorial():
            df = DoubleFactorial
            Assert(df(0) == 1)
            Assert(df(1) == 1)
            Assert(df(2) == 2)
            Assert(df(3) == 3)
            Assert(df(4) == 8)
            Assert(df(5) == 15)
            Assert(df(6) == 48)
            Assert(df(7) == 105)
            Assert(df(8) == 384)
            Assert(df(9) == 945)
            Assert(df(10) == 3840)
            Assert(df(11) == 10395)
            Assert(df(12) == 46080)
            Assert(df(13) == 135135)
            Assert(df(14) == 645120)
        def Test_IsConvexPolygon():
            p = ((0, 0), (1, 0), (1, 1), (0, 1))
            Assert(IsConvexPolygon(*p))
            p = ((0, 0), (1, 0), (1, 1), (0.5, 0.5))
            Assert(not IsConvexPolygon(*p))
            # Test with lines slightly above and below the above figure's
            # diagonal.
            d = 1e-10
            p = ((0, 0), (1, 0), (1, 1), (0.5 + d, 0.5))  # Concave
            Assert(not IsConvexPolygon(*p))
            p = ((0, 0), (1, 0), (1, 1), (0.5 - d, 0.5))  # Convex
            Assert(IsConvexPolygon(*p))
            p = ((0, 0), (1, 0), (1, 1), (0.5, 0.5 + d))  # Convex
            Assert(IsConvexPolygon(*p))
            p = ((0, 0), (1, 0), (1, 1), (0.5, 0.5 - d))  # Concave
            Assert(not IsConvexPolygon(*p))
        def Test_ParseComplex():
            # Note:  I don't test the regexp exhaustively, as it has been tested
            # numerous times before
            for input, expected in (
                # Real numbers
                ("0", ("0", "")),
                ("+0", ("+0", "")),
                ("-0", ("-0", "")),
                ("1", ("1", "")),
                ("-1", ("-1", "")),
                ("- 1", ("-1", "")),
                ("0.", ("0.", "")),
                ("1.", ("1.", "")),
                ("-1.", ("-1.", "")),
                (".0", (".0", "")),
                (".1", (".1", "")),
                ("-.1", ("-.1", "")),
                ("- . 1", ("-.1", "")),
                # Imaginary numbers
                ("0j", ("", "0")),
                ("+0j", ("", "+0")),
                ("-0j", ("", "-0")),
                ("j", ("", "1")),
                ("-j", ("", "-1")),
                ("2.2j", ("", "2.2")),
                ("+2.2j", ("", "+2.2")),
                ("-2.2j", ("", "-2.2")),
                ("- 2 . 2 j", ("", "-2.2")),
                # Complex numbers
                ("0+i", ("0", "1")),
                ("0-i", ("0", "-1")),
                ("0+1i", ("0", "+1")),
                ("0-1i", ("0", "-1")),
                ("1+0i", ("1", "+0")),
                ("1-0i", ("1", "-0")),
                ("-1-0i", ("-1", "-0")),
                #
                ("1.33+37i", ("1.33", "+37")),
                ("1.33-37i", ("1.33", "-37")),
                ("-1.33+37i", ("-1.33", "+37")),
                ("-1.33-37i", ("-1.33", "-37")),
                ("+1.33+37i", ("+1.33", "+37")),
                ("+1.33-37i", ("+1.33", "-37")),
                ("+ 1.33 - 37 i", ("+1.33", "-37")),
            ):
                got = ParseComplex(input)
                if got != expected:
                    print(f"Input    = {input!r}")
                    print(f"Expected = {expected!r}")
                    print(f"Got      = {got!r}")
                    exit(1)
            # Illegal forms
            raises(ValueError, ParseComplex, "x")
        def Test_RandomIntegers():
            # Random, no duplicates
            n = 10
            maxint = 10  # This means we must get all integers from 0 to 9
            s = RandomIntegers(n, maxint, seed=None, duplicates_OK=False)
            Assert(s == list(range(n)))
            # Random, no duplicates, larger set
            s = RandomIntegers(n, 1000, seed=None, duplicates_OK=False)
            t = RandomIntegers(n, 1000, seed=None, duplicates_OK=False)
            Assert(s != t)
            # maxint is too small --> generates exception
            with raises(ValueError):
                s = RandomIntegers(n, 9, seed=None, duplicates_OK=False)
            # maxint == 0 OK if duplicates allowed
            maxint = 0
            s = RandomIntegers(n, maxint, seed=None, duplicates_OK=True)
            Assert(s == [0]*n)
            # Repeatable sequence
            s = RandomIntegers(n, 1000, seed=0, duplicates_OK=False)
            t = RandomIntegers(n, 1000, seed=0, duplicates_OK=False)
            Assert(s == t)
            s = RandomIntegers(n, 1000, seed=0, duplicates_OK=True)
            t = RandomIntegers(n, 1000, seed=0, duplicates_OK=True)
            Assert(s == t)
        def Test_randq():
            s = [randq(seed=0)]
            for _ in range(10):
                s.append(randq())
            s = [f"{i:08X}" for i in s]
            # Hex strings from "Numerical Recipes in C", page 284
            t = [
                "3C6EF35F",
                "47502932",
                "D1CCF6E9",
                "AAF95334",
                "6252E503",
                "9F2EC686",
                "57FE6C2D",
                "A3D95FA8",
                "81FDBEE7",
                "94F0AF1A",
                "CBF633B1",
            ]
            Assert(s == t)
        def Test_randr():
            m = randq.maxidum
            Assert(randr(0) == (1013904223 % m)/float(m))
        def Test_SignificantFigures():
            Assert(AlmostEqual(float(SignificantFiguresS(1.2345e-6)), 1.23e-6))
            Assert(AlmostEqual(SignificantFigures(1.2345e-6), 1.23e-6))
    exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])

def GetGist():
    g = {}
    g["gist"] = "Math-related functions"
    g["copy"] = "Copyright © 2014 Don Peterson"
    g["lic"] = "MIT License (see /plib/_lic.mit)"
    g["test"] = "run"
    g["cat"] = "math"
    g["todo"] = ''' 

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
    '''
    return g
