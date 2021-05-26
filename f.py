# TODO
'''
    * Focus

        * Get arithmetic with units working
        * Get add/sub promotions working
        * Get comprehensive unit tests for arithmetic written

    * Comparisons:  should there be an attribute such that comparisons
      are made only to the number of significant figures?  This would
      make a lot of sense because it would avoid the annoyance of things
      like 0.44704 and 0.44704000000000005 being compared as different,
      particularly for things with units.  The attribute could be
      sigcomp or somesuch; the longer name means it has to be a bit more
      deliberate.

    * Unicode

        * x = flt("2 mi/hr"), so x*x gives 4 mi**2/hr**2.  I'd like to
          see the short form mi2/hr2 used, so there should be an
          attribute for this.  Maybe flt.short or flt.strict.

        * Add an attribute named uni that if True causes units to be
          printed using Unicode characters?  This would be nice, but
          then the constructors for flt/cpx will also need to translate
          such expressions into proper syntax for the parser.

    * If x.eng is True, return engineering form to present number
      of digits.  Otherwise, if x.eng is an integer, use that as the
      number of digits to return.  Note Decimal's engineering formatting
      is poorly designed and not suitable.

    * Add low and high attributes to flt to determine when string
      interpolation switches to scientific.

    * Add a color attribute to flt/cpx let you change the color of the
      number.  Its value should be the escape code to turn the color on.

    * It would be nice if the uncertainties library could be supported,
      as these are needed for physical calculations too.  A distinct
      disadvantage of the uncertainties ufloat is that it's not a class
      instance.  See if:

        * A suitable class can be defined.
        * The umath functions can also be in scope for such objects.
        * Can the flt object take a ufloat in the constructor and also
          use it otherwise as normal?  It should support the
          construction strings of 'a+-b', 'a+/-b', 'a±b', and 'a(b)'.

    * x = flt("1 mi/hr").  Different operations return different things:
        
        float(x) returns 0.44704.  It's the SI equivalent in m/s to 1
        mi/hr.
        x.val returns 1, the value in the original units.
        x.s returns '1\xa0mi/hr'.
        x.r returns '1.000...\xa0mi/hr' to full significand resolution

    * x.eng, x.sci, etc. are broken

    * lax attribute (flt/cpx wide)
        
        * False (default)

            * A flt/cpx in a math/cmath function must have no unit
              string; otherwise, you get a TypeError exception.

            * Unit strings are formatted per proper SI syntax.  Thus,
              "m2 s-2 K-1" is returned as "m²/(s²·K)".

        * True:  You can call math/cmath functions with a flt/cpx with a
          unit string.  The value returned will be calculated on the val
          attribute and will be a flt/cpx with no unit.

    * solidus attribute (flt/cpx wide):  Determines the formatting of
      unit strings.  The example is for the unit "m2 s-2 K-1".

        * Decision:  put this code in but don't enable it.  I don't like
          it because it may cause someone to make an error.  A user can
          change the code to enable it if they want to.

        * None:  returns "m²·s⁻²·K⁻¹" where the separation character is
          flt.sep.

        * False (default):  returns "m²/(s²·K)".

        * True:  returns "m²/s²·K", always with a single solidus.  
            
            * This is convenient for reading by humans, but you have to
              know that the solidus attribute is True because to the
              python parser, this means "m2 s-2 K-1" is returned as
              "m²/s²*K", which is a different unit.  

            * A special color or style (e.g. underline) could be used
              for such unit strings to flag that a special notation is
              being used.  Or maybe it could be "m²//s²·K".

    * Unit formatting

        * Maybe have a fmt attribute that has different attributes to get
          a variety of formats:

            3.45 kg·m·s⁻²·K⁻¹       # Canonical SI with nobreak space
            3.45·kg·m·s⁻²·K⁻¹       # Canonical SI with middle dot sep
            3.45 kg m s⁻² K⁻¹       # Canonical SI with sep = space
            3.45·kg·m/(s²·K)        # Correct SI with single solidus
            3.45·kg·m/s²·K          # Informal single solidus form

            fmt.sep = separates number and unit
            fmt.usep = separates units
            fmt.formal = "(", ")"
                       = "", "" for informal form
            fmt.ucolor = None   (None means same as number)

        * The current implementation returns the interpolated string
          with the unit in the same color as the number.  Having the
          unit in a different color or style could help set things off
          better to the eye.  But leave this for later.

    * cpx attributes
        * ss:  (sign space) Defaults to ("", "").  If they are both
          space characters, then you get '(1 + 2j)' instead of '(1+2j)'
          or '1 + 2i' instead of '1+2i' if the i attribute is True.

'''
__doc__ = '''

    This module is for routine calculations with real and complex
    numbers.  The reals are of type flt (derived from float) and the
    complex numbers are of type cpx (derived from complex).

    These types will be handy for folks who do physical calculations with
    numbers derived from measurements.  The features that help with this
    are:
        
    * Significant figures

      The str() form of the numbers only shows three significant figures
      by default (the n attribute lets you choose how many figures you
      want to see).  This is handy to avoid seeing meaningless digits in
      calculations with numbers gotten from measurements.  Use repr() if
      you want to see all the digits.

        * The interactive python interpreter and debugger use repr() for
          the default string interpolation of values.  For these
          conditions, set the flt or cpx instance's f attribute to True.
          This switches the output of the repr() and str() functions,
          letting you see the limited figures form in the interpreter
          and debugger.

    * Physical units

        * These number types can be initialized with strings
          representing common physical units.  The number's actual value
          is converted to an SI representation, but the str()
          interpolation will return the value in the original units and
          the unit string will be part of the str() value.

            Example:

            x = flt(1, "mi/hr")     # Separate units
            x = flt("1 mi/hr")      # String form
            float(x) returns 0.44704
            print(x) shows "1 mi/hr"
            x.s returns str(x) regardless of the f attribute
            x.r returns repr(x) regardless of the f attribute

        * Floating point and fractional exponents are supported.  This
          allows you to have units like 1/sqrt(Hz):  flt("1 1/Hz^(0.5)").

        * Unicode

            * Since this code is intended to be used with python 3 only,
              string interpolations use Unicode symbols to make it
              easier to read units with exponents.  

            * Example:  if x = flt("1 mi/hr**2"), its interpolated
              string is '1 mi/hr²'.  Note there is a nobreak space
              character after the 1.  

            * A weakness is Unicode's current design (as of version 13),
              as there are no superscript characters for floating point
              radix characters ('.' or ',') nor the solidus character
              for rational numbers.  Thus, you'll get ugly mixed
              displays for e.g. floating point exponents.  Examples:
                
                * If x = flt("1 mi2/hr**2.2"), its interpolated form is
                  '1 mi²/hr**2.2'.  
                * If x = flt("1 mi²/hr**(2/3)"), its interpolated form is
                  '1 mi²/hr**(2/3)'.

        * Comparisons

            Let x = flt(3)
                y = flt("4 mi/hr")
                w = cpx(3+3j)
                z = cpx("3+3j mi/hr")

            * x < y not supported unless promote attribute is True, in
              which case x is converted to a flt with the same units 
              as y.
            * flt and cpx cannot be compared.  Compare abs() values.
            * abs(y) returns flt(abs(4), "mi/hr").
            * abs(z) returns cpx(abs(3+3j), "mi/hr").

        * Division with units

            * Suppose x = flt("2 mi/hr") and y = flt("1 km/hr").  If we
              look at x/y, the answer should be 1 mi/km.  And that's
              what we get.

            * What should x//y be?  Here are some possibilities:

                * Use SI values.  2 mi/hr is 0.894 m/s and 1 km/hr is
                  0.278 m/s.  Therefore the answer should be the
                  dimensionless number 0.894//0.278, which is 3.0.

                * One mi/hr is 1.609 km/hr.  Therefore the expression is
                  [2(1.609) km/hr]//[1 km/hr], which is the
                  dimensionless number 3.218.

                * Instead, convert the divisor to mi/hr:  then the
                  expression is [2 mi/hr]//[0.621 mi/hr] and that
                  results in the dimensionless number 3.

            * Now, let y = flt("1 N/m**2").  Now we're asking how many
              integer number of pressure values are in a velocity.  This
              doesn't make physical sense, so x//y should raise an
              exception unless x and y are dimensionally the same.

    * Attributes

      Common to both flt and cpx

        - c:    Turn colorizing on if True
        - eng:  Return engineering string form
        - f:    Swap str() and repr() behavior if True
        - h:    Return a help string
        - n:    Set to number of significant figures desired in str()
        - r:    Return repr() string regardless of f attribute
        - s:    Return str() string regardless of f attribute
        - sci:  Return scientific notation string form
        - si:   Return eng with SI prefix on unit
        - t:    Return date/time string
        - u:    Return unit string or None if there isn't one
        - val:  Return value in original units
        - z:    Remove traiing zeros in str() if True

      cpx
        - real:  Real part
        - imag:  Imaginary part
        - i:     Use a+bi str() form if True
        - p:     Polar form:  None or 0 is rectangular, 1 is polar with
                 degrees, 2 is polar with radians
        - nz:    Don't show zero components if True

    * Colorizing

      Set the c attribute to True and ANSI escape codes will be used to
      color the output to the terminal when str() or repr() are called,
      letting you use color to identify flt and cpx values.

        * Default colors
            - flt:  lgreen
            - cpx:  yellow
            - cpx (polar degrees):  black with yellow background
            - cpx (polar radians):  black with white background
            - units with solidus True:  units in lred italics

    * Infection

      The flt and cpx types "infect" calculations with their types.
      Thus, a binary operation op(flt, numbers.Real) or op(numbers.Real,
      flt) will always return a flt (similarly for cpx).  This lets you
      perform physical calculations whose results only show the number
      of significant figures you wish to see.

    * Attributes and context management

      The flt and cpx attributes are class-wide, meaning a change on any
      instance affects all instances of that class.  A cpx is made up of
      two flt instances, so any flt attribute change may also affect the
      attributes of a cpx (for example, setting a flt.c attribute to
      True also causes colored output for cpx instances).

        * This class-wide feature can be an annoyance when you want to
          temporarily change an attribute because you may forget to
          change things back, leading to a bug or unexpected behavior
          later.  To get around this, flt and cpx instances are context
          managers:  you can use them in a 'with' statement to
          temporarily change the class attributes and have them reset to
          what they were before the 'with' statement after the 'with'
          block exits.  Example:

            >>> x = flt(1.23456)
            >>> x
            1.23456
            >>> x.f = True
            >>> x
            1.23            # Show 3 significant figures, the default
            >>> with x:
            ...  x.n = 4    # Show 4 significant figures
            ...  x
            ...
            1.235
            >>> x           # Reverts back to 3 figures
            1.23

        * When you want to do such things with both flt and cpx
          instances, use the following pattern:

            x, z = flt(something), cpx(something_else)
            with x:
                with z:
                    <do some stuff>

    * Factory behavior

        The flt and cpx instances are factories to create similar number
        instances with the same units.  This lets you use them in loops
        over a physical value without having to use the promote
        facility, which I'm not a fan of because of the potential for
        mistakes.  Here's an example:

            x = flt("1 mi/hr")
            # Print out a table of 1 to 10 mi/hr values
            for i in range(1, 11):
                print(x(i))

        The __call__ method of flt creates another flt object with the
        called value and the same units as the factory object.

        This is also a useful pattern for a physical calculation in a
        single set of units.  For example, if we wanted to do ideal gas
        law calculations with the units of yd3 for volume, lbf/furlong2
        for pressure, kelvin for temperature, and mol for amount of
        material, you'd set up the factories

            Pf = flt("1 lbf/furlong**2")
            vf = flt("1 yd**3")
            Tf = flt("1 K")
            Nf = flt("1 mol")
            R = gas constant

        Then for a pressure of 2, a volume of 3, and a temperature of 4,
        the amount of material is

            N = Nf(Pf(2)*vf(3)/(R*Tf(4)))

        and N will be in the units of mol.

    * math/cmath symbols

      As a convenience, the math/cmath symbols are in scope.

        * A Delegator object ensures the cmath version is called for
          cpx/complex objects and the math version is called for
          flt/float objects.  As an example, you can call sin(0.1) and
          sin(0.1j) and not get an exception and analogously with
          sqrt(2) and sqrt(-2).

    * promote attribute

        * Let x = flt("1 mi/hr").  An expression such as 'x + 3' is an
          error because the scalar 3 does not have physical dimensions
          compatible with x's speed units.  This expression will raise
          an exception.

        * For some use cases, you might want the '3' to be "promoted" to
          have the same units as x.  This can be done by setting
          x.promote to True.  Then the '3' will be changed to flt("3
          mi/hr") and the addition will succeed.

          An example lets you print out a table of speeds:
            
            x = flt("1 mi/hr")
            with x:
                x.promote = True
                while x < 5:
                    print(x)    # Shows '1 mi/hr' for first time through
                    x += 1      # Increment in 1 mi/hr units

          Note the use in a 'with' statement.  This is recommended so
          that you don't accidentally have the promote attribute True in
          later code where it might cause a bug.

    * lax attribute

        * Internally, unit expressions are handled by python's parser
          and thus follow python's expression grammar.  

        * By default, you'll need to enter unit expressions that are
          grammatically correct.  For example, 

            x = flt("1 lbm*m/s^2")

          lets x have the dimensions of a force, but with the pound mass
          unit.  A convenience is that '^' is replaced by '**' before
          evaluation, letting use either notation for exponentiation.

        * For lots of work with units, it's more convenient to use the
          shortcuts provided by the GNU units program.  To do this, set
          the flt.lax attribute to True.  This lets you 

            * Use cuddled numbers for exponents.  

            * Use space characters for implied multiplication.

            * Thus, the above value for x could be written 
              flt("1 lbm m/s2").

            * You cannot write exponents with a minus sign.  Thus,
              flt("1 lbm m s-2") would result in an exception.

            * You can use bare SI prefixes as convenience multipliers.
              Thus, flt("10 k") will have the value of 10000.0.

        * The units stuff is supported by the u.py module.  This module
          is worth looking at for general lightweight units support in
          other python scripts because it is simple to add units you
          wish to support.  The default behavior of the f.py module is 
          to use the convenience u.u() function to convert flt and cpx
          units to SI equivalents and store these equivalents as the
          actual float or complex number.  Then all calculations are
          done with SI units.  The original units are used only when
          doing string interpolation with e.g. str() or repr().

    * solidus attribute

        * This attribute can be None, False, or True.  The default is
          False.

        * Let x = flt("1 lbm*m/(s**2*K)").

        * For the default value of the attribute solidus, the string
          interpolation of x returns '1 bm·m/(s²·K)'.  Note that there
          is a nobreak space after the '1'.

        * If solidus is None, the string interpolation is 
          '1 lbm·m·s⁻²·K⁻¹'.

        * If solidus is True, the string interpolation is
          '1 lbm·m//s²·K'.  The '//' is used as a flag to warn you that
          a syntactically-illegal unit syntax is being used.  Though
          this notation is not allowed by SI syntax, it's still
          convenient for informal calculations because we can quickly
          mentally parse the numerator and denominator.

    * cpx objects can also be initialized with a unit string.  The unit
      will apply equally to both the real and imaginary parts.

    Example:

        >>> import f
        >>> from math import pi
        >>> pi
        3.141592653589793
        >>> type(pi)
        <class 'float'>
        >>> p = flt(pi)
        >>> type(p)
        <class 'f.flt'>
        >>> x, z = flt(p), cpx(p, 1/p)
        >>> x, z    # python uses repr() here, giving all the digits
        (3.141592653589793, (3.141592653589793+0.3183098861837907j))
        >>> x.f = True      # Interchange str() and repr() behavior
        >>> x, z
        (3.14, (3.14+0.318j))
        >>> sqrt(-1)        # A Delegator wrapper class calls cmath.sqrt
        (0.00+1.00j)

    The primary intent of this module is that you won't see all those
    pesky extra digits in the interpolated strings.

    The h attribute for either a flt or cpx will return a help string to
    give the class' attributes.

    Implementation
    --------------

    flt and cpx are derived from float and complex, so they can be used
    wherever float and complex can be used.  The Base class collects
    some common behavior.  A cpx object's real and imaginary parts are
    flt objects.

    The Formatter class in in the module helps with different string
    interpolation forms (fixed point, scientific notation, engineering
    notation, and SI notation with prefixes).  You can also set the
    points where the fixed display changes to scientific notation.

    The basic formatting strategy (with and without the Formatter class)
    is to use the scientific format of string interpolation f"{x:e}" with
    the proper number of decimal places to get the desired rounded string.
    The formatting is always done with Decimal objects to avoid float
    overflows or underflows.  I've testing the interpolation up to numbers
    with a million digits and things seem to work OK, so it should be
    robust.
'''

if 1:   # Imports
    # Standard library modules
    from collections import deque
    from collections.abc import Iterable
    from textwrap import dedent
    from fractions import Fraction
    import cmath
    import decimal
    import locale
    import math
    import numbers
    import operator
    import pathlib
    import re
    import sys
    import time
if 1:   # Custom imports
    import u
    # Decimal formatter
    try:
        # This library, if present, is used to get the string form of flt
        # objects to a desired number of significant figures.  It also can
        # format in scientific and engineering forms.
        #from format_numbers import Formatter

        # Unfortunately, I apparently had a file containing a Formatter
        # class, but this seems to have been deleted.  I need to make a
        # wrapper class to call FormatNumber() or use fpformat.py.
        from xformat_numbers import FormatNumber
        _have_Formatter = True
        class Formatter:
            def __init__(self, digits):
                self.digits = digits
    except ImportError:
        _have_Formatter = False
    # Debugging
    from pdb import set_trace as xx
    if len(sys.argv) > 1:
        import debug
        debug.SetDebugger()
    # Try to import the color.py module; if not available, the script
    # should still work (you'll just get uncolored output).
    try:
        import color as C
        _have_color = True
    except ImportError:
        # Make a dummy color object to swallow function calls
        class Dummy:
            def fg(self, *p, **kw): pass
            def normal(self, *p, **kw): pass
            def __getattr__(self, name): pass
        C = Dummy()
        _have_color = False
if 1:   # Global variables
    D = decimal.Decimal
    P = pathlib.Path
    ii = isinstance

all = ["flt", "cpx"]
_no_color = (not sys.stdout.isatty()) or (not _have_color)

class Base(object):
    '''This class will contain the common things between the flt and cpx
    classes.
    '''
    _digits = 3         # Number of significant digits
    _dp = locale.localeconv()["decimal_point"]
    _flip = False       # If True, interchange str() and repr()
    _fmt = None         # Formatter for flt
    _color = False      # Allow ANSI color codes in str() & repr()
    _flt_color = C.lgreen
    _cpx_color = C.yellow
    _rtz = False        # Remove trailing zeros if True
    _sep = chr(0xa0)    # Separate num from unit in str()
    _promote = False    # Allow e.g. flt("1 mi/hr") + 1 if True
    def __enter__(self):
        if ii(self, flt):
            self.saved = {
                "c": self.c,
                "f": self.f,
                "n": self.n,
                "rtz": self.rtz,
            }
        elif ii(self, cpx):
            self.saved = {
                "c": self.c,
                "f": self.f,
                "i": self.i,
                "n": self.n,
                "p": self.p,
                "rtz": self.rtz,
                "nz": self.nz,
            }
        else:
            raise TypeError("Unexpected type")
    def __exit__(self, exc_type, exc_val, exc_tb):
        if ii(self, flt):
            self.c = self.saved['c']
            self.f = self.saved['f']
            self.n = self.saved['n']
            self.rtz = self.saved['rtz']
            return False
        elif ii(self, cpx):
            self.c = self.saved['c']
            self.f = self.saved['f']
            self.i = self.saved['i']
            self.n = self.saved['n']
            self.p = self.saved['p']
            self.rtz = self.saved['rtz']
            self.nz = self.saved['nz']
            return False
        else:
            raise TypeError("Unexpected type")
    def to(self, units):
        '''Return a flt/cpx in the indicated units.  The new units must
        be dimensionally consistent with the current units.
        '''
        assert(ii(self, (flt, cpx)))
        if not units:
            return self(self)
        if not self.u:
            raise TypeError("self has no units")
        if u.dim(self.u) != u.dim(units):
            raise TypeError("self and units aren't dimensionally the same")
        value = float(self)/u.u(units)
        return flt(value, units=units)
    def _check(self):
        'Make sure Base._digits is an integer >= 0 or None'
        if not ii(Base._digits, int):
            raise TypeError("Base._digits is not an integer")
        if Base._digits is not None:
            if Base._digits < 0:
                raise TypeError("Base._digits must be None or an int >= 0")
    def __call__(self, value):
        'Return value as a flt/cpx with same units as self'
        if ii(self, flt):
            try:
                if value == self:
                    return self.copy()
            except TypeError:
                pass
            if self.u:
                return flt(str(float(value)) + " " + self.u)
            return flt(float(value))
        elif ii(self, cpx):
            if value == self:
                return self.copy()
            elif self.u:
                return cpx(str(complex(value)) + " " + self.u)
            return cpx(complex(value))
        else:
            raise TypeError(f"'{value}' is unrecognized type")
    def _r(self):
        raise RuntimeError("Base class method should be overridden")
    def _s(self):
        raise RuntimeError("Base class method should be overridden")
    def FixedFormat(self, x, n):
        '''Return a string interpolation for fixed-point form of a
        Decimal number with n significant figures.
        '''
        if not isinstance(x, D):
            raise TypeError("x must be a decimal.Decimal object")
        if not isinstance(n, int) or n <= 0:
            raise ValueError("n must be an integer > 0")
        dp = locale.localeconv()["decimal_point"]
        sign = "-" if x < 0 else ""
        # Get significand and exponent
        t = f"{abs(x):.{int(n) - 1}e}"
        s, e = t.split("e")
        exponent = int(e)
        if not x:
            return s
        if not exponent:
            return sign + s.replace(".", dp)
        significand = s.replace(dp, "")
        # Generate the fixed-point representation
        i, o, dz = deque(significand), deque(), "0"
        o.append(sign + dz + dp if exponent < 0 else sign)
        if exponent < 0:
            while exponent + 1:
                o.append(dz)
                exponent += 1
            while i:
                o.append(i.popleft())
        else:
            while exponent + 1:
                o.append(i.popleft()) if i else o.append(dz)
                exponent -= 1
            o.append(dp)
            while i:
                o.append(i.popleft())
        return f"{''.join(o)}"
    def __add__(self, other):
        return self._do_op(other, operator.add)
    def __sub__(self, other):
        return self._do_op(other, operator.sub)
    def __mul__(self, other):
        return self._do_op(other, operator.mul)
    def __truediv__(self, other):
        return self._do_op(other, operator.truediv)
    def __neg__(self):
        if ii(self, (flt, cpx)):
            return self(-self.val)
        else:
            raise RuntimeError("Bug in logic")
    # Properties
    @property
    def c(self):
        'If True, allow ANSI escape codes to color the output'
        return Base._color
    @c.setter
    def c(self, value):
        Base._color = bool(value)
    @property
    def f(self):
        'Flip the behavior of str() and repr() if value is True'
        return Base._flip
    @f.setter
    def f(self, value):
        Base._flip = bool(value)
    @property
    def h(self):
        'Return help string'
        return self.help()
    @property
    def n(self):
        'Return/set how many digits to round to'
        if not ii(Base._digits, int):
            raise TypeError("Base._digits is not an integer")
        return Base._digits
    @n.setter
    def n(self, value):
        if value is None:
            value = 0
        if not ii(value, int) or value < 0:
            raise ValueError("value must be an integer >= 0 or None")
        Base._digits = value
        if _have_Formatter:
            # Note Formatter won't allow 0 digits, so we let it be the
            # maximum number of digits in a float.
            from sys import float_info
            Base._fmt.n = value if value else float_info.dig
            Base._digits = Base._fmt.n
    @property
    def promote(self):
        '''If True, allow flt/cpx with units + number with no units.
        The number is assumed to have the same units as the flt/cpx.
        '''
        return Base._promote
    @promote.setter
    def promote(self, value):
        Base._promote = bool(value)
    @property
    def r(self):
        'Return the repr() string, regardless of self.f'
        return self._r()
    @property
    def s(self):
        'Return the str() string, regardless of self.f'
        return self._s()
    @property
    def t(self):
        'Return date/time string'
        f = time.strftime
        d = int(f("%d"))
        dt = f"{d}{f('%b%Y')}"
        h = f("%H")
        if h[0] == "0":
            h = h[1:]
        t = f"{h}:{f('%M:%S')} {f('%p').lower()}"
        return f"{dt} {t}"
    @property
    def u(self):
        'Return the units string (it will be None for no units)'
        return self._units
    @property
    def val(self):
        raise Exception("Abstract base class method")
    @property
    def rtz(self):
        'Remove trailing zeros if True'
        return Base._rtz
    @rtz.setter
    def rtz(self, value):
        Base._rtz = bool(value)
    # ----------------------------------------------------------------------
    # These properties will work if the Formatter object is present
    @property
    def eng(self):
        'Return a string formatted in engineering notation'
        return Base._fmt(self, fmt="eng") if _have_Formatter else ""
    @property
    def si(self):
        '''Return a string formatted in engineering notation with SI
        prefix appended with a space character.
        '''
        return self._s(fmt="engsi")
    @property
    def sic(self):
        '''Return a string formatted in engineering notation with SI
        prefix appended with no space character.
        '''
        return self._s(fmt="engsic")
    @property
    def sci(self):
        'Return a string formatted in scientific notation'
        return self._s(fmt="sci")
    # ----------------------------------------------------------------------
    # Static methods
    @staticmethod
    def wrap(string, number, force=None):
        'Provide ANSI escape codes around the string'
        if _no_color or not number.c:
            return string
        o = []
        use_flt = force is not None and force == flt
        use_cpx = force is not None and force == cpx
        if use_flt or ii(number, flt):
            o.append(C.fg(Base._flt_color, s=True))
            o.append(string)
            o.append(C.normal(s=True))
            return ''.join(o)
        elif use_cpx or ii(number, cpx):
            o.append(C.fg(Base._cpx_color, s=True))
            o.append(string)
            o.append(C.normal(s=True))
            return ''.join(o)
        else:
            return string
    @staticmethod
    def opname(op):
        "Return the short name of the operator module's function op"
        if not hasattr(Base.opname, "r"):
            Base.opname.r = re.compile(r"^<built-in function (.+)>$")
        mo = Base.opname.r.match(str(op))
        name = mo.groups()[0] if mo else str(op)
        return name
    @staticmethod
    def unit_error(a, b, op):
        'Raise a TypeError for units with helpful message'
        name = Base.opname(op)
        au, bu = a._units, b._units
        da, db = u.dim(au), u.dim(bu)
        msg = dedent(f'''
        Binary operation '{name}' error:
            First operand is {a}:
                Its dimensions are {da}
            Second operand {b}:
                Its dimensions are {db}
             Their dimensions must be equal.'''[1:])
        raise TypeError(msg)
    @staticmethod
    def get_units(a, b, op) -> str:
        '''This function returns the units string for the results of
        the binary operation 'a op b'.  Situations:
 
            * a has units, b doesn't:  return a's units
            * b has units, a doesn't:  return b's units
            * Neither have units:  return None
            * a and b have units:
                Raise a TypeError if they are not consistent for add/sub
                or pow.  Then use u.GetDim() and Dim.s to get the units
                of the result.
        '''
        # Get operation's symbol
        opname = Base.opname(op)
        # Get units string of variables
        f = lambda x:  x.u if hasattr(x, "u") else None
        ua, ub = f(a), f(b)
        if ua is None and ub is None:
            return None
        elif ua is not None and ub is None:
            # Only a has units
            if opname in "add sub".split():
                # a.promote must be True to allow this operation
                if not a.promote:
                    m = f"Second argument needs units like first"
                    raise TypeError(m)
            elif opname == "pow":
                da = u.GetDim(ua)
                d = op(da, b)
                return d.s
            elif opname == "floordiv":
                m = "Operands must have same dimensions for floor division"
                raise TypeError(m)
            return ua
        elif ua is None and ub is not None:
            # Only b has units
            if opname == "pow":
                raise TypeError("Exponent can't have units")
            elif opname in "add sub".split():
                # b.promote must be True to allow this operation
                if not b.promote:
                    m = f"First argument needs units like second"
                    raise TypeError(m)
            elif opname == "truediv":
                da = u.dim("m/m")
                db = u.GetDim(ub)
                d = op(da, db)
                return d.s
            elif opname == "floordiv":
                m = "Operands must have same dimensions for floor division"
                raise TypeError(m)
            return ub
        # Both a and b have unit strings
        if opname == "pow":
            raise TypeError("Exponent can't have units")
        if opname in "add sub".split():
            da, db = u.u(ua, dim=1)[1], u.u(ub, dim=1)[1]
            if da != db:
                m = ("Units are not dimensionally consistent for add/sub\n"
                  f"  First units  = '{ua}'\n"
                  f"  Second units = '{ub}'")
                raise TypeError(m)
            return ua
        else:
            assert opname in "mul floordiv truediv mod".split()
            da, db = u.GetDim(ua), u.GetDim(ub)
            if opname == "mul":
                d = da*db
                return d.s
            elif opname == "mod":
                da, db = u.u(ua, dim=1)[1], u.u(ub, dim=1)[1]
                if da != db:
                    m = ("Units are not dimensionally consistent for mod\n"
                    f"  First units  = '{ua}'\n"
                    f"  Second units = '{ub}'")
                    raise TypeError(m)
                return ub
            elif opname == "floordiv":
                # The two units must be dimensionally consistent
                f = lambda x: u.u(x, dim=1)[1]
                if f(ua) != f(ub):
                    m = "Operands must have same dimensions for floor division"
                    raise TypeError(m)
                units = u.GetDim(f"({ua})/({ub})")
                return units.s
            else:
                # Division
                d = da/db
                return d.s
    @staticmethod
    def binary_op(a, b, op):
        '''Handle the binary operation op(a, b), dealing with the
        resulting units.  a and b can be any numerical type that
        operate with flt and cpx; one of them must be a flt or cpx.
 
        Return either a flt or cpx.
        '''
        # Get the units the result must have for the given operation
        units = Base.get_units(a, b, op)
        if units is None:
            raise TypeError("Neither a nor b have units")
        # Check if we need promotion, which only happens for + or - and
        # when one of the operands has no units
        needs_promotion = False
        if op in (operator.add, operator.sub):
            f = lambda x:  hasattr(x, "u") and x.u
            # A True means b needs the promotion
            A = f(a) and not hasattr(b, "u")
            # B True means a needs the promotion
            B = f(b) and not hasattr(a, "u")
            if A^B:
                needs_promotion = True
        # If units is "", change to None so flt/cpx are dimensionless
        units = units if units else None
        def GetResult(type_a, type_b, type_result, promote=False):
            if promote:
                if A:
                    # b has no units, so promote it
                    bp = a(b)   # Gives b with a's units
                    result = op(a, bp)
                    assert(ii(result, type_a))
                elif B:
                    # a has no units, so promote it
                    ap = b(a)   # Gives a with b's units
                    result = op(ap, b)
                    assert(ii(result, type_b))
                else:
                    raise RuntimeError("Bug in logic")
                return result
            else:
                si_value = op(type_a(a), type_b(b))
                if 0:
                    print("  arg a =", a, type_a(a))
                    print("  arg b =", b, type_b(b))
                    print("  si_value =", si_value)
                # Scale to desired units 
                val = si_value/u.u(units) if units else si_value
                r = type_result(val, units=units)
                return r
        if ii(a, flt):
            if ii(b, flt):
                return GetResult(float, float, flt)
            elif ii(b, (complex, cpx)):
                return GetResult(float, complex, cpx)
            else:
                return GetResult(float, float, flt, promote=needs_promotion)
        elif ii(a, cpx):
            if ii(b, flt):
                return GetResult(complex, float, cpx)
            elif ii(b, (complex, cpx)):
                return GetResult(complex, complex, cpx)
            else:
                return GetResult(complex, float, cpx, promote=needs_promotion)
        else:
            type_a = complex if ii(a, complex) else float
            if ii(b, flt):
                if type_a == complex:
                    return GetResult(type_a, float, cpx)
                else:
                    return GetResult(type_a, float, flt)
            elif ii(b, cpx):
                return GetResult(type_a, complex, cpx)
            else:
                raise RuntimeError("At least one of a or b must be flt or cpx")

class flt(Base, float):
    '''The flt class is a float except that its str() representation is
    limited to the number of significant figures set in the attribute n.
    Changing n for an instance changes all flt objects' behavior.  Set
    it to None or 0 to return to normal float behavior.  You can include
    an option string in the constructor to give the number a physical
    unit, either like flt("1 mi/hr") or flt(1, "mi/hr").
    '''
    def __new__(cls, value, units=None):    # flt
        # See if we have a valid unit string
        to_SI, val = 1, value
        if units is not None:
            to_SI = u.u(units)
            if to_SI is None:
                raise ValueError(f"Unit '{units}' is not recognized")
        if ii(value, str):
            if Base._sep in value:
                # It's either a flt or cpx str() value
                val, units = [i.strip() for i in value.split(Base._sep)]
                val = float(val)
            elif units is not None:
                val = float(value)
            else:
                # Use u.ParseUnit to see if there's a unit in value
                rv = u.ParseUnit(value)
                if rv is None:
                    raise ValueError(f"'{value}' is not recognized as a number")
                val, un = rv
                val = float(val)
                if u.dim(un) == u.dim("k"):
                    # The "units" were an SI prefix
                    val *= u.u(un)
                    to_SI = 1
                else:
                    if u.u(un) is None:
                        raise ValueError(f"The units in '{value}' are not recognized")
                    if units is not None:
                        m = "Can't have units in string and the units keyword"
                        raise ValueError(m)
                    to_SI = u.u(un)
                    units = un
        instance = super().__new__(cls, float(val)*to_SI)
        instance._units = units
        instance._to_SI = D(to_SI)
        instance._check()
        if _have_Formatter and Base._fmt is None:
            Base._fmt = Formatter(Base._digits)
        return instance
    def _s(self, fmt="fix", no_color=False, no_units=False):    # flt
        '''Return the rounded string representation.  The fmt keyword only
        works if the Formatter class is present.
        '''
        self._check()
        if not Base._digits:
            return str(float(self))
        decorate = lambda x: x if no_color else Base.wrap(x, self)
        x = D(self)
        if _have_Formatter:
            raise Exception("Need to rewrite")
            if x and self._to_SI is not None:
                # Convert to original units
                x /= self._to_SI
            s = decorate(Base._fmt(x, fmt=fmt))
            if self._to_SI is not None:
                s = f"{s}{Base._sep}{self._units}"
            return s
        else:
            n = Base._digits
            if n is None:
                n = 15
            if self.u is not None:
                x = x/D(u.u(self.u))   # Convert to value of units
            s = self.FixedFormat(x, n)
            if Base._rtz:   # Remove trailing zeros
                while "e" not in s and "E" not in s and s[-1] == "0":
                    s = s[:-1]
            if self.u is not None and not no_units:
                s = f"{s}{Base._sep}{self.u}"
            return decorate(s)
    def _r(self, no_color=False):  # flt
        'Return the repr string representation'
        self._check()
        f = lambda x: x if no_color else Base.wrap(x, self, force=flt)
        s = f"{repr(self.val)}"
        if self.u is not None:
            s = f"{repr(self.val)}{Base._sep}{self.u}"
        if no_color:
            return s
        return f(s)
    def __str__(self):  # flt
        return self._r() if Base._flip else self._s()
    def __repr__(self): # flt
        return self._s() if Base._flip else self._r()
    def copy(self): # flt
        'Returns a copy of self'
        if self.u:
            cp = flt(self.val, units=self.u)
        else:
            cp = flt(float(self))
        return cp
    def help(self): # flt
        return dedent('''
        The flt class is derived from float and has the following attributes:
          c       * ANSI color escape codes in str() and repr()
          eng       Format in engineering notation
          si        Format in engineering notation with SI prefix
          sic       Format in engineering notation with SI prefix cuddled
          f       * Flip behavior of str() and repr()
          h         Print this help
          n       * Set/read the number of significant figures
          promote   Allows flt("1 mi/hr") + 1 (the 1 is given "mi/hr" units)
          r         The repr() string, regardless of f attribute state
          s         The str() string, regardless of f attribute state
          t       * Date and time
          rtz     * Don't print trailing zeros
          sci       Format in scientific notation
          val       Value in given units
             * means the attribute affects all flt and cps instances'''[1:])
    def round(self, n=None):    # flt
        'Return flt rounded to n places or Base._digits if n is None'
        if n is None:
            n = Base._digits
        if not ii(n, int) or n < 0:
            raise ValueError("n must be an integer >= 0 or None")
        if n:
            x = D(self)
            with decimal.localcontext() as ctx:
                ctx.prec = abs(n)
                x = +x
                return flt(x)
        else:
            return self
    # ----------------------------------------------------------------------
    # Arithmetic functions
    def _do_op(self, other, op):  # flt
        other_units = hasattr(other, "u") and bool(other.u)
        self_units = bool(self.u)
        if not (self_units or other_units):
            # Doesn't involve units
            if ii(other, complex):
                return cpx(op(float(self), other))
            return flt(op(float(self), float(other)))
        # Involves units, so must be more careful
        r = Base.binary_op(self, other, op)
        return r
    def __floordiv__(self, other):  # flt
        if ii(other, complex):
            raise TypeError("can't take floor of complex number")
        other_units = hasattr(other, "u") and bool(other.u)
        self_units = bool(self.u)
        if not (self_units or other_units):
            return self._do_op(other, operator.floordiv)
        # For floordiv with units, we must have the units be
        # dimensionally consistent.  If they are, then we return the
        # floordiv of the SI values.
        f = lambda x: u.u(x, dim=1)[1]  # Return the Dim object
        ua, ub = f(self.u), f(other.u)
        if ua != ub:
            m = "Arguments must be dimensionally the same for floor division" 
            raise TypeError(m)
        return flt(float(self)//float(other))
    def __mod__(self, other):   # flt
        if not ii(other, flt):
            raise TypeError("Second operand must be a flt")
        if self.u is not None:
            if u.dim(other.u) != u.dim(self.u):
                raise TypeError("Arguments must have the same unit dimensions")
        elif self.u is None and other.u is not None:
            raise TypeError("Arguments must both have no units")
        rem = abs(self.val % other.val)
        assert(0 <= rem <= abs(other))
        rem *= -1 if other < 0 else 1
        return rem
    def __divmod__(self, other):    # flt
        # The two operands must have the same dimensions; this ensures
        # plain numbers are returned.
        if not ii(other, flt):
            raise TypeError("Second operand must be a flt")
        if self.u is not None:
            if u.dim(other.u) != u.dim(self.u):
                raise TypeError("Arguments must have the same unit dimensions")
        elif self.u is None and other.u is not None:
            raise TypeError("Arguments must both have no units")
        # See python-3.7.4-docs-html/library/functions.html#divmod
        q = math.floor(self.val/other.val)
        rem = self % other
        # Note self could be mi/hr and other could be km/hour, so we
        # need to correct for the non-unity conversion factor
        units = Base.get_units(self, other, operator.truediv)
        conv = u.u(units)
        return q, flt(rem*conv)
    def __pow__(self, other):   # flt
        'self**other'
        return self._do_op(other, operator.pow)
    def __radd__(self, other):  # flt
        'other + self'
        return self + other
    def __rsub__(self, other):  # flt
        'other - self'
        if ii(other, (flt, cpx)):
            return other.__add__(-self)
        return -self + other
    def __rmul__(self, other):  # flt
        'other*self'
        return self*other
    def __rtruediv__(self, other):  # flt
        'other/self'
        return operator.truediv(flt(1), self)*other
    def __rfloordiv__(self, other): # flt
        'other//self'
        return flt(floor((flt(1)/self)*other))
    def __rmod__(self, other):  # flt
        'other % self'
        return self.__mod__(other, self)
    def __rdivmod__(self, other):   # flt
        'divmod(other, self)'
        return self.__divmod__(other, self)
    def __rpow__(self, other):  # flt
        'Calculate other**self'
        if ii(other, flt):
            return pow(other, self)
        else:
            if self.u is not None:
                raise TypeError("Exponent cannot have a unit")
            return pow(float(other), self)
    def __abs__(self):  # flt
        return flt(abs(self.val), units=self.u)
    def __eq__(self, other):    # flt
        '''To be equal, two flt objects must have the same unit
        dimensions and the same SI values.  With no units, they must be
        numerically equal.
        '''
        if ii(other, complex):
            raise ValueError("Complex numbers are not ordered")
        other_units = hasattr(other, "u") and bool(other.u)
        self_units = bool(self.u)
        if self_units and other_units:
            dself = u.dim(self.u)
            dother = u.dim(other.u)
            if dself != dother:
                # Not dimensionally the same
                return False
            # Use their SI values
            return float(self) == float(other)
        elif ((self_units and not other_units) or 
            (not self_units and other_units)):
            return False
        else:
            return float(self) == float(other)
    def __le__(self, other):    # flt
        if ii(other, complex):
            raise ValueError("Complex numbers are not ordered")
        other_units = hasattr(other, "u") and bool(other.u)
        self_units = bool(self.u)
        if self_units and other_units:
            dself = u.dim(self.u)
            dother = u.dim(self.u)
            if dself != dother:
                return False
            # Use their SI values
            return float(self) < float(other)
        elif ((self_units and not other_units) or 
            (not self_units and other_units)):
            return False
        else:
            return float(self) < float(other)
    @property
    def val(self):  # flt
        'Return the value as a float in the given units (not in SI)'
        if self.u is not None:
            return float(self)/u.u(self.u)
        return float(self)

class cpx(Base, complex):
    '''The cpx class is a complex except that its components are flt
    numbers.
    '''
    _i = False      # If True, use "i" instead of "j" in str()
    _p = False      # If True, use polar representation in str()
    _rad = False    # If True, use radians for angle measurement
    _nz = False     # If True, don't print out zero components
    def __new__(cls, real, imag=0, units=None): # cpx
        'real can be a number type, a cpx, or a complex.'
        to_SI = u.u(units) if units else 1
        f = lambda x:  D(x) if x else D(0)
        if ii(real, cpx):
            if units is not None and real.u is not None:
                raise ValueError("real can't have units")
            re, im = real._real*to_SI, real._imag*to_SI
            instance = super().__new__(cls, re, im)
            instance._real = flt(f(real._real), units=units)
            instance._imag = flt(f(real._imag), units=units)
            instance._units = units
        elif ii(real, numbers.Real) and ii(imag, numbers.Real):
            if ii(real, flt):
                if units is not None and real.u is not None:
                    raise ValueError("real can't have units")
            if ii(imag, flt):
                if units is not None and imag.u is not None:
                    raise ValueError("imag can't have units")
            re, im = float(real)*to_SI, float(imag)*to_SI
            instance = super().__new__(cls, re, im)
            instance._real = flt(f(real), units=units)
            instance._imag = flt(f(imag), units=units)
            instance._units = units
        elif ii(real, numbers.Complex):
            re, im = real.real*to_SI, real.imag*to_SI
            assert(not hasattr(real, "_units"))
            instance = super().__new__(cls, re, im)
            instance._real = flt(f(real.real), units=units)
            instance._imag = flt(f(real.imag), units=units)
            instance._units = units
        else:
            if ii(real, str):
                real = real.replace("·", " ").replace("\xa0", " ")
                g = real.split()
                un = None
                if len(g) == 2:
                    num, un = g
                    to_SI = u.u(un)
                elif len(g) == 1:
                    num, un = real, None
                else:
                    raise ValueError(f"'{real}' is an illegal string")
                if "i" in num:
                    num = num.replace("i", "j")
                if units is not None and un is not None:
                    m = "Cannot have units in string and units keyword"
                    raise ValueError(m)
                un = units if units is not None else un
                if "j" in num:
                    if imag:
                        raise ValueError("Can't use 'j' and give imag number")
                    z = complex(num)
                    re, im = z.real*to_SI, z.imag*to_SI
                else:
                    re = float(num)*to_SI
                    im = float(imag)*to_SI
                instance = super().__new__(cls, re, im)
                instance._real = flt(f(re))
                instance._imag = flt(f(im))
                instance._to_SI = to_SI
                instance._units = un
            else:
                raise TypeError("Unexpected type for real")
        return instance
    def _pol(self, repr=False): # cpx
        'Return polar form'
        f = lambda x:  Base.wrap(x, self)
        r, theta = [flt(i) for i in polar(self)]
        theta *= 1 if self.rad else 180/pi
        deg = "" if self.rad else "°"
        if repr:
            s = f"{r._r(no_color=True)}∠{theta._r(no_color=True)}{deg}"
        else:
            s = f"{r._s(no_color=True)}∠{theta._s(no_color=True)}{deg}"
        if self._to_SI is not None:
            t = "(" + s + ")"
            t = f"{t}{Base._sep}{self._units}"
        else:
            t = f(s) if self.i else f("(" + s + ")")
        return f(t)
    def _s(self, fmt="fix"):    # cpx
        '''Return the rounded string representation.  If cpx.i is True,
        then "i" is used as the unit imaginary and no parentheses are
        placed around the string.  If cpx.p is False, use rectangular;
        if True, use polar coordinates.
        '''
        f = lambda x:  Base.wrap(x, self)
        if self.p:   # Polar coordinates
            return self._pol()
        else:       # Rectangular coordinates
            r, i = self._real, self._imag
            re = r._s(fmt=fmt, no_color=True, no_units=True)
            im = i._s(fmt=fmt, no_color=True, no_units=True)
            if self.nz and ((r and not i) or (not r and i)):
                if r:
                    s = f"{re}" if cpx._i else f"({re})"
                else:
                    s = f"{im}i" if cpx._i else f"({im}j)"
            else:
                im = "+" + im if im[0] != "-" else im
                s = f"{re}{im}i" if cpx._i else f"({re}{im}j)"
            if self.u:  # Include units
                s = f"{s}{Base._sep}{self._units}"
            return f(s)
    def _r(self):   # cpx
        'Return the full representation string'
        f = lambda x:  Base.wrap(x, self, force=cpx)
        conv = 1/u.u(self.u) if self.u else 1
        if self.p:
            s = self._pol(repr=True)
        else:
            re, im = float(self._real*conv), float(self._imag*conv)
            I = "i" if self.i else "j"
            if self.nz:
                s = []
                if re:
                    s.append(f"{re!r}")
                if im:
                    if s:
                        s.append("+" if im > 0 else "")
                    s.append(f"{im!r}")
                    s.append(I)
                if self.u:
                    t = f"({''.join(s)})"
                else:
                    t = f"{''.join(s)}"
                s = t
            else:
                r = f"{float(self._real*conv)!r}"
                i = f"{float(self._imag*conv)!r}"
                sgn = "+" if self._imag > 0 else ""
                s = f"{r}{sgn}{i}{I}"
                if self.u:
                    s = f"({r}{sgn}{i}{I}) {self.u}"
        return f(s)
    def __str__(self):  # cpx
        return self._r() if Base._flip else self._s()
    def __repr__(self): # cpx
        return self._s() if Base._flip else self._r()
    def copy(self): # cpx
        'Return a copy of self'
        if self.u:
            cp = cpx(self.val, units=self.u)
        else:
            cp = cpx(complex(self))
        return cp
    def help(self): # cpx
        return dedent('''
        The cpx class is derived from complex and has the following attributes:
          c       * ANSI color escape codes in str() and repr()
          eng       Format in engineering notation
          si        Format in engineering notation with SI prefix
          sic       Format in engineering notation with SI prefix cuddled
          f       * Flip behavior of str() and repr()
          h         Print this help
          i       * Use 'i' instead of 'j' as the imaginary unit
          imag      Return the imaginary component
          n       * Set/read the number of significant figures
          nz      * Don't print zero components if True
          p       * Display in polar coordinates
          promote   Allows cpx("1 mi/hr") + 1 (the 1 is given "mi/hr" units)
          r         The repr() string, regardless of f attribute state
          rad       Display polar angle in radians
          real      Return the real component
          s         The str() string, regardless of f attribute state
          t       * Date and time
          rtz     * Don't print trailing zeros
          sci       Format in scientific notation
          val       Value in given units
             * means these attributes affect all cpx instances'''[1:])
    def round(self, n=None):    # cpx
        'Return a cpx with components rounded to n decimal places'
        return cpx(self.real.round(n), self.imag.round(n))
    # Arithmetic functions
    def _do_op(self, other, op):    # cpx
        other_units = hasattr(other, "u") and bool(other.u)
        self_units = bool(self.u)
        if not (self_units or other_units):
            return cpx(op(complex(self), complex(other)))
        # Involves units, so must be more careful
        r = Base.binary_op(self, other, op)
        return r
    def __complex__(self):  # cpx
        return complex(self._real, self._imag)
    def __truediv__(self, other):   # cpx
        return self._do_op(other, operator.truediv)
    def __pow__(self, other):   # cpx
        return self._do_op(other, operator.pow)
    def __radd__(self, other):  # cpx
        #xx
        return cpx(complex(other) + complex(self))
    def __rsub__(self, other):  # cpx
        #xx
        return cpx(complex(other) - complex(self))
    def __rmul__(self, other):  # cpx
        #xx
        return cpx(complex(other)*complex(self))
    def __rtruediv__(self, other):  # cpx
        #xx
        return cpx(complex(other)/complex(self))
    def __rpow__(self, other):  # cpx
        #xx
        #return cpx(pow(complex(other), complex(self)))
        return cpx(complex(other)**complex(self))
    def __neg__(self):  # cpx
        #xx
        return cpx(-complex(self))
    def __pos__(self):  # cpx
        #xx
        return cpx(complex(self))
    def __abs__(self):  # cpx
        return flt(abs(self.val), units=self.u)
    def __eq__(self, other):    # cpx
        if not ii(other, (float, flt, complex, cpx)):
            if self._units is not None:
                return False
            if other != self:
                return False
            return True
        elif ii(other, cpx):
            if ((self._units and not other._units) or
                (not self._units and other._units)):
                return False
            return other.val == self.val
        elif ii(other, flt):
            if self.imag:
                return False
            if other._units != self._units:
                return False
            if other != self.val:
                return False
            return True
        elif ii(other, complex):
            if self._units is not None:
                return False
            if self.val != other:
                return False
            return True
    def __ne__(self, other):    # cpx
        return not self.__eq__(other)
    # ----------------------------------------------------------------------
    # Properties
    @property
    def real(self): # cpx
        return self._real
    @property
    def imag(self): # cpx
        return self._imag
    @property
    def i(self):    # cpx
        'Return boolean that indicates using "i" instead of "j"'
        return cpx._i
    @i.setter
    def i(self, value): # cpx
        'Set boolean that indicates using "i" instead of "j"'
        cpx._i = bool(value)
    @property
    def nz(self):   # cpx
        '''Return boolean that indicates don't print out zero components'''
        return cpx._nz
    @nz.setter
    def nz(self, value):    # cpx
        '''Set boolean that indicates don't print out zero components'''
        cpx._nz = bool(value)
    @property
    def p(self):    # cpx
        'If True, use polar coordinates; if False, use rectangular'
        return cpx._p
    @p.setter
    def p(self, value): # cpx
        cpx._p = bool(value)
    @property
    def rad(self):  # cpx
        'If True, use radians in polar form'
        return cpx._rad
    @rad.setter
    def rad(self, value):   # cpx
        cpx._rad = bool(value)
    @property
    def val(self):  # cpx
        'Return the value as a complex in the given units (not in SI)'
        if self._units is not None:
            return complex(self)/u.u(self._units)
        return complex(self)

if 1:   # Get math/cmath functions into our namespace
    '''Put all math symbols into this namespace.  We use an object with
    the same name as the function and let it have a __call__ method.
    When called, it calls the relevant math or cmath function and
    returns the result if it doesn't get an exception.  It also allows for
    special handling where needed (e.g., see how sqrt of a negative number
    is handled to give a cpx instead of an exception).
    '''
    class Delegator(object):
        '''A delegator object is used to encapsulate the math and cmath
        functions and allow them to be put in this module's namespace.  When
        the Delegator instance.__call__ is called, the cmath routine is
        called if any of the arguments are complex; otherwise, the math
        routine is called.
        '''
        def __init__(self, name):
            self.name = name
        def __call__(self, *args, **kw):
            C = (complex, cpx)
            if hasattr(math, name) and not hasattr(cmath, name):
                # Forces a math call
                s = f"math.{self.name}(*args, **kw)"
            elif not hasattr(math, name) and hasattr(cmath, name):
                # Forces a cmath call
                s = f"cmath.{self.name}(*args, **kw)"
            else:
                if self.iscomplex(*args, **kw):
                    s = f"cmath.{self.name}(*args, **kw)"
                else:
                    if self.name == "sqrt" and len(args) == 1 and args[0] < 0:
                        s = f"cmath.{self.name}(*args, **kw)"
                    elif self.name == "rect" and len(args) == 2:
                        s = f"cmath.{self.name}(*args, **kw)"
                    elif self.name == "pow" and len(args) == 2:
                        s = f"math.{self.name}(*args, **kw)"
                    else:
                        s = f"math.{self.name}(*args, **kw)"
            # Make sure function arguments don't have units.
            units = any([hasattr(i, "u") and i.u for i in args])
            if units:
                raise TypeError("One or more arguments have units")
            # Now execute the function.  You'll get a TypeError if you do
            # something like erf(1j), just what you'll get from
            # math.erf(1j).  However, the Delegator's exception message will
            # tell you that "module 'cmath' has no attribute 'erf'".  The
            # TypeError from math.erf will tell you "can't convert complex
            # to float".  The complex argument forced the Delegator to
            # search for a complex function, which doesn't exist.  This
            # could be fixed with more code (e.g., knowing erf is only in
            # math), but I don't think it's worth the extra effort.
            try:
                result = eval(s)
            except AttributeError as err:
                raise TypeError(err) from None
            if ii(result, int):
                return result
            elif ii(result, (float, flt)):
                return flt(result)
            elif ii(result, C):
                return cpx(result)
            else:
                if self.name == "polar":
                    result = tuple([flt(i) for i in result])
                return result
        @staticmethod
        def iscomplex(*args, **kw):
            '''Return True if any argument or keyword argument is
            complex.  If arg[0] is an iterator, also look for complex
            numbers in it.
            '''
            C = (complex, cpx)
            cc = lambda x: any([ii(i, C) for i in x])
            if cc(list(args) + list(kw.values())):
                return True
            if len(args) == 1:
                if not ii(args[0], str) and ii(args[0], Iterable):
                    return cc(args[0])
            return False
    # All math/cmath function names for Version 3.9.4
    functions = '''
    acos      comb      exp       gamma     lcm       nextafter remainder
    acosh     copysign  expm1     gcd       ldexp     perm      sin
    asin      cos       fabs      hypot     lgamma    phase     sinh
    asinh     cosh      factorial isclose   log       polar     sqrt
    atan      degrees   floor     isfinite  log10     pow       tan
    atan2     dist      fmod      isinf     log1p     prod      tanh
    atanh     erf       frexp     isnan     log2      radians   trunc
    ceil      erfc      fsum      isqrt     modf      rect      ulp
    '''
    for name in functions.split():
        if hasattr(math, name) or hasattr(cmath, name):
            s = f"{name} = Delegator('{name}')"
            exec(s)
    # Constants
    #   both:  e inf nan pi tau
    #   cmath: infj nanj 
    from math import e, inf, nan, pi, tau
    from cmath import infj, nanj
    # Change constants' type to flt
    constants = "e pi tau".split()
    for i in constants:
        exec(f"{i} = flt({i})")

if 0:
    x = flt("10 k")
    print(x)
    print(x.u)
    exit()

if __name__ == "__main__": 
    from lwtest import run, raises, assert_equal
    if 1:   # Test code 
        def Assert(cond):
            '''Same as assert, but you'll be dropped into the debugger on an
            exception if you include a command line argument.
            '''
            if not cond:
                if len(sys.argv) > 1:
                    print("Type 'up' to go to line that failed")
                    xx()
                else:
                    raise AssertionError
        def Equal(a, b, reltol=1e-15):
            'Return if a == b within the indicated tolerance'
            if not a and not b:
                return True
            if ii(a, flt) and ii(b, flt):
                if (a.u and not b.u) or (not a.u and b.u):
                    return False
                if a.u is not None and b.u is not None:
                    da, db = u.dim(a.u), u.dim(b.u)
                    if da != db:
                        return False
                diff = abs(float(a) - float(b))
                if float(a):
                    reldiff = abs(diff/float(a))
                elif float(b):
                    reldiff = abs(diff/float(b))
                return reldiff <= reltol
            elif ii(a, cpx) and ii(b, cpx):
                if (a.u and not b.u) or (not a.u and b.u):
                    return False
                if not a.u and not b.u:
                    da, db = u.dim(a.u), u.dim(b.u)
                    if da != db:
                        return False
                # Real part
                realdiff = abs(float(a.real) - float(b.real))
                if float(a.real):
                    reldiff = abs(realdiff/float(a.real))
                elif float(b):
                    reldiff = abs(realdiff/float(b.real))
                else:
                    reldiff = realdiff
                if reldiff > reltol:
                    return False
                # Imaginary part
                imagdiff = abs(float(a.imag) - float(b.imag))
                if float(a.imag):
                    reldiff = abs(imagdiff/float(a.imag))
                elif float(b.imag):
                    reldiff = abs(imagdiff/float(b.imag))
                else:
                    reldiff = imagdiff
                if reldiff > reltol:
                    return False
                return True
            else:
                raise TypeError("Must both be flt or cpx")
        def Test_constructors():
            # W is any type that float(W) works on
            # S is str
            # X is types:  int, float, flt, Fraction, Decimal, W
            # Z is types:  complex, cpx
            with flt(0):
                # flt(X) 
                for i in (1, 1.0, flt(1), Fraction(1, 1), D("1")):
                    Assert(flt(i) == float(i))
                    Assert(flt(i, units=None) == float(i))
                    Assert(flt(i, None) == float(i))
                    x = flt(i)
                    Assert(x(i) == x)
                with raises(TypeError):
                    flt(cpx(1))
            x = flt(1, units="mi/hr")
            with x:
                # With strings
                Assert(flt("1") == 1)
                Assert(flt("1", units="") == 1)
                Assert(flt("1", units=None) == 1)
                Assert(flt(1, units="mi/hr") == x)
                Assert(flt("1", units="mi/hr") == x)
                Assert(flt("1 mi/hr") == x)
                Assert(x(1) == x)
            with cpx(0):
                z = cpx(1)
                # Simple
                Assert(z == cpx(1))
                Assert(z == cpx(1, imag=None))
                Assert(z == cpx(1, imag=None, units=None))
                # Two components
                z = cpx(1, 2)
                Assert(z == cpx(1, 2))
                Assert(z == cpx("1", 2))
                Assert(z == cpx("1", "2"))
                # String
                Assert(z == cpx("1+2j"))
                Assert(z == cpx("1+2i"))
                # With units
                z = cpx(1, 2, units="mi/hr")
                # String
                Assert(z == cpx("1+2i mi/hr"))
                Assert(z == cpx("1+2i", units="mi/hr"))
                Assert(z == cpx("1+2i", 0, units="mi/hr"))
                with raises(ValueError):
                    cpx("1+2i", 1, units="mi/hr")
                Assert(z(z) == z)
        def Test_copy():
            x = flt(1)
            Assert(x == x.copy())
            x = flt("1 mi/hr")
            Assert(x == x.copy())
            z = cpx(1)
            Assert(z == z.copy())
            z = flt("1 mi/hr")
            Assert(z == z.copy())
        def Test_FixedFormat():
            x = flt(0)
            data = [i.strip() for i in '''
                -10 0.0000000003142
                -9 0.000000003142
                -8 0.00000003142
                -7 0.0000003142
                -6 0.000003142
                -5 0.00003142
                -4 0.0003142
                -3 0.003142
                -2 0.03142
                -1 0.3142
                0 3.142
                1 31.42
                2 314.2
                3 3142.
                4 31420.
                5 314200.
                6 3142000.
                7 31420000.
                8 314200000.
                9 3142000000.
                10 31420000000.
            '''.strip().split("\n")]
            for i in data:
                exp, expected = i.split()
                y = D(f"{str(math.pi)}e{exp}")
                got = x.FixedFormat(y, 4)
                Assert(got == expected)
        def Test_flt_with_units():
            with flt(1):
                # Same units
                x = flt("2 mi/hr")
                y = flt("1 mi/hr")
                Assert(x + y == flt("3 mi/hr"))
                Assert(x - y == flt("1 mi/hr"))
                Assert(x*y == flt("2 mi2/hr2"))
                Assert(x/y == flt(2))
                Assert(x//y == flt(2))
                # Different units
                x = flt("2 mi/hr")
                y = flt("1 km/hr")
                Equal(x + y, flt("2.6213711922373344 mi/hr"))
                Equal(x - y, flt("1.378628807762666 mi/hr"))
                Equal(x*y, flt("2 km*mi/hr2"))
                Equal(x/y, flt("2 mi/km"))
                Equal(x//y, flt(3))
                # pow
                with raises(TypeError):
                    x**y    # Exception because y has units
                Equal(x**3, flt("8 mi3/hr3"))
                Equal(x**3.3, flt(repr(2**3.3) + " mi^3.3/hr^3.3"))
                # divmod
                q, rem = divmod(x, y)
                Assert(q == 2)
                Assert(rem == 0)
                Assert(ii(rem, flt))
        def Test_reverse_flt_with_units():
            with flt(0):
                x = 2
                y = flt("1 mi/hr")
                y.f = y.c = 1
                # Exception with promote off
                y.promote = 0
                with raises(TypeError):
                    x + y
                # Works with promote on
                y.promote = 1
                Assert(x + y == flt("3 mi/hr"))
                Assert(x - y == flt("1 mi/hr"))
                Assert(x*y == flt("2 mi/hr"))
                Equal(x/y, flt("2 hr/mi"))
                # Different units
                x = flt("2 mi/hr")
                y = flt("1 km/hr")
                Equal(x + y, flt("2.6213711922373344 mi/hr"))
                Equal(x - y, flt("1.378628807762666 mi/hr"))
                Equal(x*y, flt("2 km*mi/hr2"))
                Equal(x/y, flt("2 mi/km"))
                # pow
                with raises(TypeError):
                    x**y
                Equal(x**3, flt("8 mi3/hr3"))
                Equal(x**3.3, flt(repr(2**3.3) + " mi^3.3/hr^3.3"))
                # divmod
                q, rem = divmod(x, y)
                Assert(q == 2)
                Assert(rem == 0)
                Assert(ii(rem, flt))
        def Test_cpx_with_units():
            with cpx(1):
                # Same units
                x = cpx("2+1j mi/hr")
                y = cpx("1+1j mi/hr")
                Assert(x + y == cpx("3+2j mi/hr"))
                Assert(x - y == cpx("1-0j mi/hr"))
                Equal(x*y, cpx("1+3j mi**2/hr**2"))
                Assert(x/y == cpx("1.5-0.5j"))
                with raises(TypeError):
                    x//y
                # Different units
                x = cpx("2+1j mi/hr")
                y = cpx("1+1j km/hr")
                w = cpx("2.6213711922373344+1.6213711922373342j mi/hr")
                Equal(x + y, w)
                w = cpx("1.378628807762666+0.378628807762666j mi/hr")
                Equal(x - y, w)
                w = cpx("0.9999999999999997+2.999999999999999j mi/hr")
                Equal(x*y, w)
                w = cpx("1.4999999999999998-0.49999999999999994j mi/km")
                Equal(x/y, w)
                with raises(TypeError):
                    x//y
                # pow
                with raises(TypeError):
                    x**y    # Exception because y has units
                Equal(x**3, cpx("1.9999999999999991+11.0j mi**3/hr**3"))
                w = "0.5799707405700941+14.221311772360444j mi^3.3/hr^3.3"
                Equal(x**3.3, cpx(w))
                # divmod
                with raises(TypeError):
                    q, rem = divmod(x, y)
        def Test_promote():
            x, y, expected = 2, flt("1 mi/hr"), flt("3 mi/hr")
            y.promote = 0
            with raises(TypeError):
                x + y
            with raises(TypeError):
                y + x
            y.promote = 1
            Assert(x + y == expected)
            Assert(y + x == expected)
    r = r"^[Tt]est_"
    failed, messages = run(globals(), regexp=r, quiet=0, halt=1)
