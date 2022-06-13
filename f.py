''' 

    BUGS and key things to do
        - Remove units; it just makes a big mess
            - The fundamental benefits of the flt class are 1) string
              interpolation is pleasant and 2) math stuff is in scope.
            - The addition of units made the class too clumsy and bloated.
            - My overwhelming use case is to just see things to 3 figures.  
        - flt('inf') and flt('nan') need to work
            - _sci() and other stuff need to handle inf
        - Needs a rlz attribute to remove leading zero
        - Needs __all__, as there's lots of crap in the global namespace
        - flt and cpx need to be hashable
        - cpx needs to be initialized from a polar form too, so maybe add
          pol as a keyword to the constructor. 
            - Make sure angles are measured in radians by default, as this
              is too confusing if it's not True.  It's ok to have a cpx
              class variable that makes the string display in degrees.

        - Number of significant figures
            - The .n attribute when changed changes the class variable of
              Base.
            - After using this class for a while, I'm not so sure this is
              the proper use.  Sometimes you might want a number to display
              with 5 figures when the others in your problem display with
              3.  The original use case was that it lets you uniformly work
              to a given number of figures, but not all data are created
              equal.  Maybe the instance can be changed by setting n, then
              a reset() method would set the instance back to the class'
              value.
            - The context manager behavior is useful for special situations
            - What should happen with arithmetic?  Probably the result
              should have min(x1.n, x2.n).
 
    TODO
    
    - xyzzy to see documentation

    - Fundamental features
        - Immutable 
        - Real/complex numbers that display only practical digits
        - Infection model
        - String interpolation
            - Number of significant figures
                - .N is class variable for default
                - .n is instance variable
                - .n takes precedence and is used by context manager
                - Set .n to 0 to revert to .N behavior
            - .f to swap str() and repr()
            - Color coding in string interpolations to indicate type
            - Aimed at calculations with numbers from measurements, so the
              result of func(x, y) will be z with n digits of min(x.n, y.n).
            - fix, eng, sci, low/high adjustable
            - i or j notations
        - math/cmath functions in scope
        - Equality
            - Fundamental interpretation is numbers from measured
              quantities
            - Class variable physical?
                - If True, compare to min sig figures
                - If False, compare per usual float rules
            - Method needs to be thought out
                - Normal float model
                - Use equal() method where num digits can be given?
        - Attach any needed attributes
            - You can't do this with floats (probably for memory efficiency
              reasons)
            - One use case is to use x.u for the instance's physical units
                - Should this be formalized to appear in the str() value?
                  Might be OK if .u could be made immutable after setting
                  or you do it in the constructor.  Need for cpx too?

    - Focus
        - fmt.py works and has tests.  Use it as the formatter.
        - Test that all needed constructors are written
        - Get arithmetic with units working
        - Get comprehensive unit tests for arithmetic written
    - Add .rdp attribute to allow removal of decimal point if it is
      trailing. 
    - Add attribute to remove leading zero like sig.lead_zero.  Convenient
      to minimize length in tables.
    - Try to duplicate fpformat's engsi and engsic formatting for flt
      objects.
        - A common use case is in vmdivider.py.  A calculated resistance is
          e.g. 9k, but it gets displayed as '9.000k'.  It would be nice to
          see it as '9k', as that's easiest to read.  Attributes are needed
          to suppress the unit string but leave the SI prefix as a suffix.
    - one = flt(1); one("1 mi/hr") does not work.  Should it?
    - Add si method or attribute to Base?  This would return the number in
      base SI units.  A use case is the gas law calculation:  the number of
      moles results in units of 0.274 ft³·mol·psi/J.  Since p*V is energy,
      the resulting unit is mol, but you don't see that unless you know it.
      si would fix this.
        - There's no easy way to use SI prefixes with the unit string
          unless you put the prefix in a numerator object with unity power.
        - Thus, the output should be in scientific notation if it's beyond
          the fixed point limits.
    - Need to remove Base.sci, etc.  Add these attributes to flt and cpx.
    - Need to fix cpx radd, etc. (search for xx)
    - Tests need to cover all formatting options.
        - An invariant for divmod is that 'divmod(x,y)[0]*y + x % y' be
          very close to x (in REPL, type help() and * and look at footnote
          2 to the precedence table).
    - Uncertainties:  It would be nice if the uncertainties library could
      be supported, as these are needed for physical calculations too.  A
      distinct disadvantage of the uncertainties ufloat is that it's not a
      class instance.  See if:
        - A suitable class can be defined.
        - The umath functions can also be in scope for such objects.
        - Can the flt object take a ufloat in the constructor and also use
          it otherwise as normal?  It should support the construction
          strings of 'a+-b', 'a+/-b', 'a±b', and 'a(b)'.

'''
__doc__ = '''
    This module is for routine calculations with real and complex
    numbers.  The reals are of type flt (derived from float) and the
    complex numbers are of type cpx (derived from complex).
 
    The main characteristics are:
 
        - You won't see all those annoying extra digits in the numbers'
          interpolated strings.
        - You can use physical units with the numbers.
        - You can do reasonable calculations with numbers derived from
          measurements.
        - You'll have the math/cmath functions available and can use
          them with either flt or cpx arguments where appropriate.
 
    The module's features are:
        
    - Significant figures
 
      The str() form of the numbers only shows three significant figures
      by default (the n attribute lets you choose how many figures you
      want to see).  This is handy to avoid seeing meaningless digits in
      calculations with numbers gotten from measurements.  Use repr() if
      you want to see all the digits.
 
        - The interactive python interpreter and debugger use repr() for
          the default string interpolation of values.  For these
          conditions, set the flt or cpx instance's f attribute to True.
          This flips the output of the repr() and str() functions,
          letting you see the limited figures form in the interpreter
          and debugger.
 
        - Class variables:  if x = flt(1) and you set x.n = 6, this changes
          the Base._digits class variable.  Thus, all flt and cpx objects
          are then shown with 6 figures.
 
          Multiple threads:  all threads in a process see the same class
          variables.  Suppose you want two threads to use different
          number of significant figures to print out a number.  The way
          to do this is use the context manager facilities of flt:
 
            Thread1:
                with x:
                    x.n = 6
                    print(x)
            Thread2:
                with x:
                    x.n = 2
                    print(x)
 
          The context manager uses a lock to ensure that the attribute
          can't be changed during the context's scope.  To keep delays
          to a minimum, only put necessary code in the with statement.
 
          Multiple processes:  changes to the class variables in Base
          are not seen by different processes.
 
    - Colorizing
 
        - Set the c attribute to True and ANSI escape codes will be used
          to color the output to the terminal when str() or repr() are
          called, letting you use color to identify flt and cpx values.
          This is handy during interactive python interpreter sessions
          because the colors alert you to the flt and cpx number types.
          This works in typical UNIX terminals, but you'll need to
          modify the color.py module to get it to work in Windows.
 
    - Physical units
 
        - These number types can be initialized with strings
          representing common physical units.  The number's actual value
          is converted to an SI representation, but the str()
          interpolation will return the value in the original units and
          the unit string will be part of the str() value.
 
            Example:
 
            x = flt(1, "mi/hr")     # Separate units
            x = flt("1 mi/hr")      # String form
            float(x) returns 0.44704    # 1 mi/hr in m/s
            print(x) shows "1 mi/hr"
            x.s returns str(x) regardless of the f attribute
            x.r returns repr(x) regardless of the f attribute
 
        - Floating point and fractional exponents are supported.  This
          allows you to have units like 1/sqrt(Hz):  flt("1 1/Hz^(1/2)").
 
        - Some short notations are allowed in unit expressions.  A space
          character denotes multiplication, '^' means '**', and a number
          cuddled next to a unit is an exponent.  Note not every
          expression will be correct, as I used the tokenize module and
          there were a few problems that I didn't deem worth the effort
          to fix.  For example, 'm3.3' won't parse correctly, so write
          it with parentheses as 'm(3.3)'.
 
            - Remember this is a syntax for units.  Addition and
              subtraction are not allowed.  Thus, valid but
              perhaps confusing syntax like 'x = flt("2.2 s-2 m/kg-1")'
              is allowed and gives the units 'm·kg/s²'.
          
            - The unit expressions are actually evaluated by python's
              parser, so an exponent expression like m**(2.3*0.7) is
              allowed (but you can't use '+' or '-' in such
              expressions).
 
            - An exponent like m**(3/4) has the '3/4' evaluated by
              python's parser, which returns the float 0.75.  Thus,
              fractions aren't directly supported.  If Unicode would fix
              their design (see below), fractions would be easy to
              support.
 
        - Complex numbers
 
            - The cpx type is composed of two flt types and a cpx can have
              a physical unit, which is given to both real and imaginary
              parts (otherwise, what units should abs(z) have?).  
 
            - Z = cpx(274-22j, "ohms") constructs an impedance.  I like to
              change to polar form (Z.p = True) to see it displayed as
              275.∠-4.59°. 
 
        - Unicode
 
            - Since this code is intended to be used with python 3 only,
              string interpolations use Unicode symbols to make it
              easier to read units with exponents.  
 
            - Example:  if x = flt("1 mi/hr**2"), its interpolated
              string is '1 mi/hr²'.  There is a nobreak space character
              after the 1.  
              
            - Two flt/cpx attributes affect unit formatting.  Suppose the
              unit to be formatted is "kg*m/(s**2*K)".  The standard
              formatted form is 'kg·m/(s²·K)'.
 
                - flat is a Boolean when True that results in a "flat"
                  Unicode form:  'kg·m·s⁻²·K⁻¹'.
 
                - solidus is a Boolean when True results in the form
                  'kg·m//s²·K'.  This form is convenient for informal
                  work, but it is not algebraically correct with a
                  left-associative parser.  The '//' is intended to flag
                  to your eye that it's a special format.  Though this
                  notation is not allowed by SI syntax, it's still
                  convenient for informal calculations because we can
                  quickly mentally parse the numerator and denominator.
 
            - An ongoing weakness in Unicode's design (as of version 13)
              is there are no superscript characters for floating point
              radix characters ('.' or ',') nor the solidus character
              for rational numbers.  Thus, you may get ugly mixed
              displays when working with units.  Examples:
                
                - If x = flt("1 mi2/hr**2.2"), its interpolated form is
                  '1 mi²/hr**2.2'.  
                - If x = flt("1 mi2/hr**(2/3)"), its interpolated form is
                  'mi²/hr**0.6666666666666666'.  Fractions are evaluated
                  as floating point numbers.
 
        - Comparisons
 
            Let x = flt(3)
                y = flt("4 mi/hr")
                w = cpx(3+3j)
                z = cpx("3+3j mi/hr")
 
            - x < y not supported unless promote attribute is True, in
              which case x is converted to a flt with the same units 
              as y.
            - x == y has an exception unless x and y are dimensionally
              the same.
            - abs(y) returns flt(abs(4), "mi/hr").
            - abs(z) returns cpx(abs(3+3j), "mi/hr").
            - The sigcomp attribute of flt and cpx determine how many
              significant figures are used for the comparison is the
              attribute is not None and not zero.  This is handy when
              comparing numbers derived from measurements.
 
        - Division with units
 
            - Suppose x = flt("2 mi/hr") and y = flt("1 km/hr").  If we
              look at x/y, the answer by inspection is 1 mi/km.  And that's
              what we get.
 
            - However, floor division isn't as obvious.  What should
              x//y be?  Here are some possibilities:
 
                - Use SI values.  2 mi/hr is 0.894 m/s and 1 km/hr is
                  0.278 m/s.  Therefore the answer should be the
                  dimensionless number 0.894//0.278, which is 3.0.
 
                - One mi/hr is 1.609 km/hr.  Therefore the expression is
                  [2(1.609) km/hr]//[1 km/hr], which is the
                  dimensionless number 3.218.
 
                - Alternatively, convert the divisor to mi/hr:  then the
                  expression is [2 mi/hr]//[0.621 mi/hr] and that
                  results in the dimensionless number 3.
 
                - Because the first and third cases are congruent,
                  that's how floor division will work with flt objects
                  with units.  It's not supported for cpx objects.
 
                - Let y = flt("1 N/m**2").  Now x//y means we're asking
                  how many integer number of pressure values are in a
                  velocity.  This doesn't make physical sense, so x//y
                  raises an exception unless x and y are dimensionally
                  the same so that the returned value is dimensionless.
 
    - Attributes
 
      Common to both flt and cpx
 
        - c:    Turn colorizing on if True
        - eng:  Return engineering string form
        - f:    Swap str() and repr() behavior if True
        - flat: Show units in a flat SI form
        - h:    Return a help string
        - n:    Set to number of significant figures desired in str()
        - r:    Return repr() string regardless of f attribute
        - s:    Return str() string regardless of f attribute
        - sci:  Return scientific notation string form
        - si:   Return eng with SI prefix on unit
        - sigcomp:   Number of sig figures to compare for equality
        - solidus:   Show units in an informal form num//denom
        - t:    Return date/time string
        - u:    Return unit string or None if there isn't one
        - val:  Return value in original units
        - z:    Remove trailing zeros in str() if True
 
      cpx
        - rad:   Use radians for angle in polar form
        - real:  Real part
        - imag:  Imaginary part
        - i:     Use a+bi str() form if True
        - p:     Polar form (defaults to degrees for angle measure)
        - nz:    Don't show zero components if True
 
    - Type infection model
 
        - The flt and cpx types "infect" calculations with their types.
          Thus, a binary operation op(flt, numbers.Real) or
          op(numbers.Real, flt) will always return a flt (similarly for
          cpx).  This lets you perform physical calculations whose
          results only show the number of significant figures you wish
          to see.
 
    - Attributes and context management
 
        - The flt and cpx attributes are class-wide, meaning a change on
          any instance affects all instances of that class.  A cpx is
          made up of two flt instances, so any flt attribute change may
          also affect the attributes of a cpx (for example, setting a
          flt.c attribute to True also causes colored output for cpx
          instances).
 
        - This class-wide feature can be an annoyance when you want to
          temporarily change an attribute because you may forget to
          change things back, leading to a bug or unexpected behavior
          later.  To get around this, flt and cpx instances are context
          managers:  you can use them in a 'with' statement to
          temporarily change the class attributes and have them reset to
          what they were before the 'with' statement after the 'with'
          block exits.  Example:
 
            >>> x = flt(1.23456)
            >>> x
            1.23456         # This is the repr() string
            >>> x.f = True  # Swap str() and repr() behavior
            >>> x
            1.23            # Show 3 significant figures, the default
            >>> with x:
            ...  x.n = 4    # Show 4 significant figures
            ...  x
            ...
            1.235
            >>> x           # Reverts back to 3 figures after with block
            1.23
 
        - To provide thread-safe behavior, this context manager behavior
          is protected with a lock so that only one thread may change
          the class attributes at a time.  If your code uses multiple
          threads and you get a blocked thread, it's because of this
          locking mechanism to avoid race conditions.
 
            - When you want to do such things with both flt and cpx
              instances, the following won't work because the first with
              statements causes the second statement to block while
              trying to acquire the lock:
 
                  x, z = flt(something), cpx(something_else)
                  with x:
                      with z:
                          <do stuff>
 
              To handle this use case, you can manually set the
              Base._lock class variable to False.  However, you have to
              remember to manually reset it after the with block exits:
 
                  x, z = flt(something), cpx(something_else)
                  Base._lock = False
                  with x:
                      with z:
                          <do stuff>
                  Base._lock = True
 
             If you forget this, you may have a race condition in
             subsequent code.
 
    - Factory behavior
 
        - flt and cpx instances are factories to create similar number
          instances with the same units.  This lets you use them in
          loops over a physical value without having to use the promote
          facility, which I'm not a fan of because of the potential for
          bugs in code.  Here's an example:
 
              x = flt("1 mi/hr")
              # Print out a table of 1 to 10 mi/hr values
              for i in range(1, 11):
                  print(x(i))
 
        - The __call__ method of flt creates another flt object with the
          called value and the same units as the factory object.
 
        * This is also a useful pattern for a physical calculation in a
          particular set of units.  For example, if we wanted to do ideal
          gas law calculations with the units of yd3 for volume,
          lbf/furlong2 for pressure, kelvin for temperature, and mol for
          amount of material, you'd set up the factories
 
              Pf = flt("1 lbf/furlong**2")
              vf = flt("1 yd**3")
              Tf = flt("1 K")
              Nf = flt("1 mol")
              R = gas constant
 
          Then for a pressure of 2, a volume of 3, and a temperature of
          4, the amount of material is
 
              N = Nf(Pf(2)*vf(3)/(R*Tf(4)))
 
          and N will be in the units of mol.
 
    - math/cmath symbols
 
        - As a convenience, the math/cmath symbols are in scope.
 
        - A Delegator object ensures the cmath version is called for
          cpx/complex objects and the math version is called for
          flt/float objects.  For example, you can call sin(0.1) and
          sin(0.1j) and not get an exception.  Analogously, sqrt(2) and
          sqrt(-2) both work.
 
        - This use is distinct from standard python which divides things
          into math and cmath libraries and comments that users may not
          even know or care what complex numbers are.  The reason I did
          things this way is because of the HP-42s calculators I've been
          using since 1988 when they were introduced.  I have them set up
          so that complex results are allowed.  I feel this is most
          convenient for typical scientific/engineering use.
 
        - I use the flt/cpx types in my repl.py script, which is my version
          of a python-based console calculator.  It simulates an
          interactive python session, but allows customization to provide
          the classes and features you want (this is done using python's
          code module).  
 
    - promote attribute
 
        - Let x = flt("1 mi/hr").  An expression such as 'x + 3' is an
          error because the scalar 3 does not have physical dimensions
          compatible with x's speed units.  This expression will raise
          a TypeError exception.
 
        - For some use cases, you might want the '3' to be "promoted" to
          have the same units as x.  This can be done by setting
          x.promote to True.  Then the '3' will be changed to
          flt("3 mi/hr") and the addition will succeed.
 
          An example lets you print out a table of speeds:
 
              x = flt("1 mi/hr")
              with x:
                  x.promote = True
                  while x < 5:
                      print(x)    # Shows '1 mi/hr' for first time through
                      x += 1      # Increment in 1 mi/hr units
 
          Note the use in a 'with' statement.  This is recommended so
          that you don't accidentally leave the promote attribute True
          in later code where it might cause a bug.
 
    - sigcomp attribute
 
        - This attribute is an integer between 0 and 15 or None and is
          used to determine how to compare flt or cpx numbers for
          equality.  If not None or zero, then the numbers' values are
          rounded to the indicated number of significant figures before
          the comparison.
 
        - This attribute is handy for when dealing with numbers derived
          from physical measurements because such numbers virtually
          never have more than perhaps 12 significant figures.  This
          helps avoid annoyances like 0.44704 not being the same as
          0.44704000000000005, which is mi/hr in m/s -- these small
          differences often appear in floating point calculations.  Yet
          you would rarely have more than 4 or 5 significant figures in
          such numbers.
 
    - cpx objects can also be initialized with a unit string.  The unit
      will apply equally to both the real and imaginary parts.
 
        - Example:  An LCR meter reads an impedance of a component to be
          473 ohms with a phase angle of 34 degrees.  What are the
          impedance components?
 
              w = rect(473, 34*pi/180)      # Returns a cpx()
              Z = cpx(x, "ohm")             # Add the unit
              print(Z)
                  --> '(392.+264.j) ohm'
 
    Implementation
    --------------
 
        The flt and cpx objects are derived from flt(Base, float) and
        cpx(Base, complex), so they can be used wherever float and complex
        numbers can be used.  The Base class collects some common behavior.
        A cpx object's real and imaginary parts are flt objects.
    
        The physical units feature is aided with the help of the u.py
        module.  Over 800 common units are defined in it, but it's easy to
        add new units or changed to a different set.  It includes a
        randomization feature that helps determine when a calculation isn't
        dimensionally correct (read the docstring).
    
        The basic fixed-point formatting method is in Base.FixedFormat().
        It uses the scientific format of string interpolation f"{x:e}"
        with the proper number of decimal places to get the desired rounded
        string.  The formatting is done with Decimal objects to avoid float
        overflows or underflows.  I've testing the interpolation up to
        numbers with a million digits and things seem to work OK.
    
        There are perhaps 4000 lines of code in this module and the u.py
        module for units, so this is not a lightweight implementation of
        float and complex objects.  If you need computational speed, stick
        with float, complex, or numpy stuff.  You can use flt/cpx objects at
        the end of calculations for the presentation of results.
 
    Example
    -------
 
        from f import flt
        from u import u
 
        # Ideal gas law example calculation:  the oxygen cylinder on my
        # torch is about 7 inches in diameter and 33 inches long.  The
        # nominal internal volume is about 0.55 cubic feet per a table for
        # a "BL" type cylinder.  The gauge pressure of the tank is 1200
        # psi.  
 
        # Questions:
        #   1.  What is the mass of the remaining oxygen?
        #   2.  How many liters (at 1 atm) of oxygen remain in the tank?
 
        R = flt("8.314 J/(K*mol)")
        R.n = 3         # Show results to 3 figures
        R.f = False     # Don't interchange str() and repr()
        R.c = True      # Use ANSI escape sequences to color flt/cpx
        print(f"R = gas constant = {R}")
 
        # Gas cylinder internal volume
        V = flt("0.55 ft3")
        print(f"V = volume = {V} = {V.to('m3')} = {V.to('L')}")
 
        # This is the pressure reading from the regulator in psig
        # (i.e., gauge pressure with respect to atmospheric pressure),
        # which is corrected to an absolute pressure by adding 1 atm.  
        p = flt("1200 psi") + flt("1 atm")
        print(f"p = pressure = {p} = {p.to('MPa')}")
 
        T = flt("293 K")
        print(f"T = temperature = {T}")
 
        # Number of moles of oxygen
        n = p*V/(R*T)
        print(f"n = {n} = {n.toSI()} = {n.to('mol')}")
        print(f"Dimensions of n = {u.dim(n.u)}")
 
        # Molecular mass (standard atomic mass of oxygen is 16 and it's
        # a diatomic gas)
        molarmass = flt("32 g/mol")
        m = n*molarmass
        print(f"Mass of O₂ = {m} = {m.to('kg')}")
 
        # Since the tank volume is V, the volume Va at 1 atm is calculated
        # from p*V = pa*Va.  Thus, Va = V*p/pa.
        pa = flt("1 atm")
        Va = V*p/pa
        print(f"Volume of O₂ at 1 atm = {Va.to('liters')}")
 
    will print out
 
        R = gas constant = 8.31 J/(K·mol)
        V = volume = 0.550 ft³ = 0.0156 m³ = 15.6 L
        p = pressure = 1210. psi = 8.38 MPa
        T = temperature = 293. K
        n = 0.274 ft³·mol·psi/J = 53.5 mol = 53.5 mol
        Dimensions of n = Dim("N")
        R = gas constant = 8.31 J/(K·mol)
        V = volume = 0.550 ft³ = 0.0156 m³ = 15.6 L
        p = pressure = 1210. psi = 8.38 MPa
        T = temperature = 293. K
        n = 0.274 ft³·mol·psi/J = 53.5 mol = 53.5 mol
        Dimensions of n = Dim("N")
        Mass of O₂ = 8.78 ft³·g·psi/J = 1.71 kg
        Volume of O₂ at 1 atm = 1290. liters
 
'''
'''

    xyzzy Documentation

    Python's int, float, and complex number types are useful calculational
    tools, along with the math and cmath libraries.

    However, those of us who do calculations with measured quantities run
    into the an annoying feature of floating point computations: we often see
    far too many digits that don't contain real information.  Because of
    this, I designed the flt object to be a python float with the feature
    of showing only a few digits when it is converted to a string.  Since
    the same annoying plethora of digits happens with complex numbers, the
    cpx object is a python complex composed of two flt objects. 

    Example:  

        Using an old printer's rule, I measured the diameter of a piece of
        cylindrical metal as 7/12 inches and its length is 4 and 11/12
        inches.  I measured its mass as 312 g on my old Ohaus triple-beam
        scale.  What is the density of this material and what material is
        it likely made of?

        Using regular python floating point numbers, we get

            from math import pi
            diameter = 7/12             # inches
            length = 4 + 11/12          # inches
            area = pi*diameter**2/4     # inches**2
            volume = area*length        # inches**3
            mass = 312                  # grams
            density = mass/volume       # g/inches**3
            density = density/(2.54**3) # g/cm**3
            # Report
            print(f"""
                diameter = {diameter} in
                length = {length} in
                area = {area} in2
                volume = {volume} in3
                mass = {mass} g
                density = {density} g/cm3
            """)

        which prints

            diameter = 0.5833333333333334 in
            length = 4.916666666666667 in
            area = 0.26725354171163174 in2
            volume = 1.3139965800821896 in3
            mass = 312 g
            density = 14.489693844078017 g/cm3

        As is usual with floating point calculations, there are lots of
        digits shown.  Here's the same calculation with flt objects:

            from f import flt, pi
            diameter = flt(7/12)        # inches
            length = flt(4 + 11/12)     # inches
            area = pi*diameter**2/4     # inches**2
            volume = area*length        # inches**3
            mass = 312                  # grams
            density = mass/volume       # g/inches**3
            density = density/(2.54**3) # g/cm**3
            # Report
            print(f"""
                diameter = {diameter} in
                length = {length} in
                area = {area} in2
                volume = {volume} in3
                mass = {mass} g
                density = {density} g/cm3
            """)

        Note the only changes were 1) to use the f.py module's flt type and pi
        constant and 2) change diameter and length to flt types.  The area,
        volume, and density variables were "infected" with the flt type, as
        an arithmetic calculation with a flt type returns a flt type.  The
        default number of figures displayed for a flt is 3, so now you see
        only 3 figures in the results:

            diameter = 0.583 in
            length = 4.92 in
            area = 0.267 in2
            volume = 1.31 in3
            mass = 312 g
            density = 14.5 g/cm3

        Neither calculation is "correct" over the other, but the latter is
        what I prefer to see for output, as it's easier to parse mentally
        and judge the results.  I know from a lifetime of doing physical
        calculations that it's rare to have more than 3 or 4 significant
        figures for measured data.  The flt class supports this by using
        3 figures as the default and only displaying the instance's string
        value to 3 figures.   If you prefer to see all the digits, after
        diameter is defined, insert 'diameter.f = True' and you'll see the
        same results as the first example.  Behind the scenes, a flt object
        is a python float.  The difference is the __str__() method causes
        fewer significant figures to appear in the string interpolation.

    I often use the math and cmath libraries and I wanted them in scope by
    default.  Further, I wanted to emulate a valued feature of my HP-42s
    calculators, which can be configured to calculate elementary functions
    over the complex domain when presented with a complex number (most
    calculators will generate an error).  Thus, sin(x) will use math.sin(x)
    if x is a float type and will use cmath.sin(x) if x is a complex type.  

    Example:  

        My LCR meter measured a nominal 3 H coil's impedance at 1 kHz with
        a 0.6 V RMS sine wave as 15.820 kΩ @ 83.27°.  What is the ESR?

        The ESR is the real part of the complex impedance which we would
        just calculate as 15.82*cos(radians(83.27)).  However, let's look
        at the full calculation to see that things are consistent.

            from f import *
            mag, phase = 15820, 83.27  # mag in ohms, phase in degrees
            print(f"phase = {phase}°")
            phase = radians(phase)
            print(f"phase = {phase} radians")
            print(f"sin(phase) = {sin(phase)}")
            print(f"cos(phase) = {cos(phase)}")

            Z = cpx(mag*cos(phase), mag*sin(phase))
            Z.i = True                  # Use 'i' in display
            Z.rtz = Z.rtdp = True       # Remove excess zeros and decimal point
            print(f"Complex form of impedance = {Z}")
            print(f"Absolute value = {abs(Z)}")
            print(f"ESR = real part = {Z.real} Ω")

        This prints the results

            phase = 83.27°
            phase = 1.45 radians
            sin(phase) = 0.993
            cos(phase) = 0.117
            Complex form of impedance = 1850+15700i
            Absolute value = 15800
            ESR = real part = 1850 Ω
    
    A warning I must give is to be wary of the "significant figure"
    calculations given in basic science classes.  The intent of this method
    is an **approximate** method of calculating the uncertainty of a number
    derived from other numbers by arithmetic and functions.  Ultimately,
    the method is flawed because its output is not a group in the technical
    sense, but this is never communicated by the teachers of the elementary
    classes -- perhaps because they don't understand it themselves.  An
    experienced scientist will use it for approximate estimates, but will
    result to modern uncertainty calculations per the GUM for proper work,
    particularly if linear uncertainty theory is inadequate or complicated
    correlations are present.

    There's more to a calculation than just getting the right number of
    significant figures.  For example, suppose I measured a rectangular
    room with a tape measure as 23.4 by 16.7 feet.  The room's area is
    390.78 square feet, which would get rounded to 3 figures to give 391
    square feet.  How much material should I buy from a 12 foot wide roll
    to cover this room?  You'd calculate a length of 391/12 which would
    give 32.6 feet.  This gives two 16.3 foot long chunks, which are short
    by 0.4 ft.  Oops.  

        A better construction method would be to use two 12 foot wide
        strips 16.7 feet long and join them along the factory edges (it's
        easier to glue and tape).  You'd then trim them at the wall
        borders.  Experience will teach you that walls aren't straight, so
        you'll have an extra 0.3 feet (3.6 inches) on each side to trim.
        Thus, you need to cut 2(16.7) = 33.4 feet off the roll.  A cautious
        person would e.g. add another foot or two to allow for things like
        cutting mistakes.  A little bit too short is a worse error than a
        little bit too long.

'''
if 1:  # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright © 2021 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # <programming> This module provides the flt/cpx types for calculations
        # with numbers derived from measurements.  flt is derived from float
        # and cpx from complex.  These objects can be given physical units
        # (utilizing the u.py module).  They also display 3 significant figures
        # by default when str() is called on them, making floating point
        # calculations less cluttered with useless digits.  I use these a lot
        # with the repl.py script for my command line python-based calculator.
        #∞what∞#
        #∞test∞# run #∞test∞#
    # Standard library modules
        from collections import deque
        from collections.abc import Iterable
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
        import threading
        import time
    # Custom imports
        from wrap import dedent
        import u

        # Color stuff is commented out until circular import problems get fixed
        #from color import TRM as T
        # Debugging
        if 0:
            import debug
            debug.SetDebugger()
if 1:   # Global variables
    Lock = threading.Lock()
    D = decimal.Decimal
    P = pathlib.Path
    ii = isinstance
    #__all__ = ["flt", "cpx"]
    _no_color = True
    # This can be True when a formatter class is written
    _have_Formatter = False
class Base(object):
    '''This class will contain the common things between the flt and cpx
    classes.
    '''
    _digits = 3         # Number of significant digits for str()
    _sigcomp = None     # Number of sig digits for comparisons
    _dp = locale.localeconv()["decimal_point"]
    _flip = False       # If True, interchange str() and repr()
    _fmt = None         # Formatter for flt
    _color = False      # Allow ANSI color codes in str() & repr()
    #_flt_color = T("cyn")
    #_cpx_color = T("brn")
    _rtz = False        # Remove trailing zeros if True
    _rtdp = False       # Remove trailing decimal point
    _sep = chr(0xa0)    # Separate num from unit in str()
    _promote = False    # Allow e.g. flt("1 mi/hr") + 1 if True
    _flat = False       # Flat form of Unicode units string interpolation
    _solidus = False    # Solidus form of Unicode units string interpolation
    _lock = True        # Use lock for context management
    _low = 1e-5         # When to switch to scientific notation
    _high = 1e16        # When to switch to scientific notation
    def __enter__(self):
        if Base._lock:
            Lock.acquire()
        du = "__"
        def Keep(s, A):
            'Return True if this attribute should be kept'
            if i.startswith(du) and i.endswith(du):
                return False
            if "function" in str(A[i]) or "property" in str(A[i]):
                return False
            if "staticmethod" in str(A[i]):
                return False
            return True
        base, cls = {}, {}
        B = Base.__dict__
        for i in B:
            if Keep(i, B):
                base[i] = B[i]
        S = flt.__dict__ if ii(self, flt) else cpx.__dict__
        for i in S:
            if Keep(i, S):
                cls[i] = S[i]
        self.base = base
        self.cls = cls
    def __exit__(self, exc_type, exc_val, exc_tb):
        B = Base.__dict__
        for i in self.base:
            exec(f"Base.{i} = self.base[i]")
        S = flt.__dict__ if ii(self, flt) else cpx.__dict__
        name = "flt" if ii(self, flt) else "cpx"
        for i in self.cls:
            exec(f"{name}.{i} = self.cls[i]")
        if Base._lock:
            Lock.release()
        return False
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
    def toSI(self):
        'Return the value of this flt/cpx in the base SI units'
        if self.u is None:
            return None
        mytyp = flt if ii(self, flt) else cpx
        typ = float if ii(self, flt) else complex
        value = typ(self)   # This is numerically in SI units
        units = u.dim(self.u).toSI()
        return mytyp(value, units=units)
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
    def eq_dim(self, other):
        'Return True if dimensions of self and other are equal'
        if self.u is None and other.u is None:
            return True
        elif self.u is None and other.u is not None:
            return False
        elif self.u is not None and other.u is None:
            return False
        # Both have unit strings
        return u.dim(self.u) == u.dim(other.u)
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
        t = f"{abs(x):.{n - 1}e}"
        s, e = t.split("e")
        exponent = int(e)
        if not x:
            return s
        if not exponent:
            return sign + s.replace(".", dp)
        significand = s.replace(dp, "")
        # Generate the fixed-point representation
        sig, out, zero_digit = deque(significand), deque(), "0"
        out.append(sign + zero_digit + dp if exponent < 0 else sign)
        if exponent < 0:
            while exponent + 1:
                out.append(zero_digit)
                exponent += 1
            while sig:
                out.append(sig.popleft())
        else:
            while exponent + 1:
                out.append(sig.popleft()) if sig else out.append(zero_digit)
                exponent -= 1
            out.append(dp)
            while sig:
                out.append(sig.popleft())
        return f"{''.join(out)}"
    def rnd(self, n=None):
        '''Return a flt that is rounded to the current number of digits 
        or n digits if n is not None.
        '''
        with self:
            if n is not None:
                if not ii(n, int) and not (1 <= n <= 15):
                    raise ValueError("n must be an integer between 1 and 15")
                self.n = n
            if self.u is None:
                return flt(self.s)
            else:
                return flt(self.s, units=self.u)
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
            return self(-float(self.val))
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
    def dim(self):
        "Return the Dim object of the instance's units"
        if self.u is not None:
            return u.dim(self.u)
        return None
    @property
    def f(self):
        'Flip the behavior of str() and repr() if value is True'
        return Base._flip
    @f.setter
    def f(self, value):
        Base._flip = bool(value)
    @property
    def flat(self):
        '''Unit string is given in Unicode flat form.  Example:  for
        'kg*m/(s2*K)', flat form is 'kg·m·s⁻²·K⁻¹'.
        '''
        return Base._flat
    @flat.setter
    def flat(self, value):
        Base._flat = bool(value)
        Base._solidus = False
    @property
    def h(self):
        'Return help string'
        return self.help()
    @property
    def high(self):
        'Switch to scientific notation when x > Base.high'
        return Base._high
    @high.setter
    def high(self, value):
        Base._high = D(abs(value)) if value is not None else D(0)
    @property
    def low(self):
        'Switch to scientific notation when x < Base.low'
        return Base._low
    @low.setter
    def low(self, value):
        Base._low = D(abs(value)) if value is not None else D(0)
    @property
    def n(self):
        'How many digits to round to'
        return Base._digits
    @n.setter
    def n(self, value):
        'The value is clamped to be between 1 and 15 digits'
        min_value, max_value = 1, 15
        if value is None:
            value = max_value
        elif not ii(value, int):
            raise ValueError("value must be an integer")
        if value < min_value:
            value = min_value
        elif value > max_value:
            value = max_value
        Base._digits = value
        assert(min_value <= Base._digits <= max_value)
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
    def rtdp(self):
        'Remove trailing zeros if True'
        return Base._rtdp
    @rtdp.setter
    def rtdp(self, value):
        Base._rtdp = bool(value)
    @property
    def rtz(self):
        'Remove trailing zeros if True'
        return Base._rtz
    @rtz.setter
    def rtz(self, value):
        Base._rtz = bool(value)
    @property
    def s(self):
        'Return the str() string, regardless of self.f'
        return self._s()
    @property
    def sigcomp(self):
        '''Significant digits for '==' and '<' comparisons.  If it is
        None, then comparisons are made to full precision.  Otherwise,
        it must be an integer between 1 and 15.
        '''
        return Base._sigcomp
    @sigcomp.setter
    def sigcomp(self, value):
        if value is None:
            self._sigcomp = None
            return
        val = int(value)
        if not (1 <= val <= 15):
            raise ValueError("sigcomp must be between 1 and 15")
        Base._sigcomp = val
    @property
    def solidus(self):
        '''Unit string is given in Unicode solidus form.  Example:  for
        'kg*m/(s2*K)', solidus form is 'kg·m//s²·K'.  This is a
        convenient short form, but it is NOT algebraically correct with
        a left-associative multiplication.  The two solidus characters
        are used to flag this visually.
        '''
        return Base._solidus
    @solidus.setter
    def solidus(self, value):
        Base._solidus = bool(value)
        Base._flat = False
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
            #o.append(Base._flt_color)
            o.append(string)
            #o.append(T.n)
            return ''.join(o)
        elif use_cpx or ii(number, cpx):
            #o.append(Base._cpx_color)
            o.append(string)
            #o.append(T.n)
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
    @staticmethod
    def sig_equal(a, b, n=None):
        '''Return True if objects a and b are equal to the indicated
        number of significant figures.  a must be a flt or cpx.  If a is
        a flt, b must be a flt or a number that can be converted to a
        flt (and a must not have units).  If a is cpx, then b must be a
        cpx or a number that can be converted to complex (and a must not
        have units).  If a and b are both flt or cpx, is assumed that
        they have dimensionally-equal units.
        '''
        # Make sure both a and b are flt or cpx types
        if ii(a, flt):
            if ii(b, flt):
                if not Base.eq_dim(a, b):
                    raise TypeError("a and b don't have same dimensions")
            elif ii(b, cpx):
                raise TypeError("b must be a flt since a is")
            else:
                if a.u is not None:
                    raise TypeError("a must not have units")
                b = flt(b)
        elif ii(a, cpx):
            if ii(b, cpx):
                if not Base.eq_dim(a, b):
                    raise TypeError("a and b don't have same dimensions")
            elif ii(b, flt):
                raise TypeError("b must be a cpx since a is")
            else:
                if a.u is not None:
                    raise TypeError("a must not have units")
                b = cpx(b)
        assert((ii(a, flt) and ii(b, flt)) or (ii(a, cpx) and ii(b, cpx)))
        def Round(x):
            y = D(repr(float(x)))
            with decimal.localcontext() as ctx:
                # Round to n significant figures
                ctx.prec = n
                y = +y
            return y
        if n is None:
            n = a.n
        n = max(1, min(n, 15))  # Clamp n to [1, 15]
        # Note we compare Decimal objects
        if ii(a, flt) and ii(b, flt):
            if not Base.eq_dim(a, b):
                return False
            return Round(a.val) == Round(b.val)
        elif ii(a, cpx) and ii(b, cpx):
            if not Base.eq_dim(a, b):
                return False
            a_re, a_im = Round(a.val.real), Round(a.val.imag)
            b_re, b_im = Round(b.val.real), Round(b.val.imag)
            return (a_re == b_re) and (a_im == b_im)
        else:
            raise TypeError("a and b must both be flt or cpx")
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
        toi = lambda x: "inch" if x.strip() == "in" else x
        if units is not None:
            units = toi(units)
            to_SI = u.u(units)
            if to_SI is None:
                raise ValueError(f"Unit '{units}' is not recognized")
        if ii(value, str):
            if Base._sep in value:
                # It's either a flt or cpx str() value
                val, units = [i.strip() for i in value.split(Base._sep)]
                units = toi(units)
                val = float(val)
            elif units is not None:
                val = float(value)
            else:
                # Use u.ParseUnit to see if there's a unit in value
                rv = u.ParseUnit(value.replace("_", ""))
                if rv is None:
                    raise ValueError(f"'{value}' is not recognized as a number")
                val, un = rv
                un = toi(un)
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
                    units = un if un else None
        instance = super().__new__(cls, float(val)*to_SI)
        instance._units = units if units else None
        instance._to_SI = D(to_SI)
        instance._check()
        if _have_Formatter and Base._fmt is None:
            Base._fmt = Formatter(Base._digits)
        return instance
    def _eng(self, n=None):    # flt
        'Return self in engineering notation (n overrides self.n)'
        if n is None:
            n = Base._digits
        x = D(self)
        dp = locale.localeconv()["decimal_point"]
        s = f"{abs(x):.{n - 1}e}"
        # Get significand and exponent
        significand, exponent = s.split("e")
        significand = significand.replace(dp, "")
        e = int(exponent) if x else 0
        sig = deque(significand)
        while len(sig) < 3:
            sig.append("0")
        # Get exponent divmod with 3
        div, rem = divmod(abs(e), 3)
        if abs(x) >= 1:
            nexp = abs(e) - rem
            # Position decimal point
            sig.insert(rem + 1, dp)
        else:
            nexp = 3*(div + bool(rem))
            # Position decimal point
            if rem == 2:
                sig.insert(2, dp)
            elif rem == 1:
                sig.insert(3, dp)
            else:
                sig.insert(1, dp)
        # Build output string
        sig.append("e")
        sig.append("-" if e < 0 else "")
        sig.append(str(nexp))
        return ''.join(sig)
    def _sci(self, n=None):    # flt
        'Return self in scientific notation (n overrides self.n)'
        if n is None:
            n = Base._digits
        x = D(self)
        s = f"{x:.{n - 1}e}"
        sig, exp = s.split("e")
        # Note e.g. f"{Decimal(0):.2e}" returns '0.00e+2', so 
        # get rid of leading 0's and fix the '0.00e+2' annoyance.
        exp = str(int(exp) if x else 0)
        s = f"{sig}e{str(exp)}"
        return s
    def _s(self, fmt="fix", no_color=False, no_units=False):    # flt
        '''Return the rounded string representation.  The fmt keyword only
        works if the Formatter class is present.  The no_units feature
        is needed for repr().
        '''
        self._check()
        if not Base._digits:
            return str(float(self))
        decorate = lambda x: x if no_color else Base.wrap(x, self)
        x = D(self)
        if _have_Formatter:
            raise Exception("Need to rewrite")
        else:
            n = Base._digits
            if n is None:
                n = 15
            if self.u is not None:
                x = x/D(u.u(self.u))   # Convert to value of units
            if x and (abs(x) < self.low or abs(x) > self.high):
                # Switch to scientific notation
                s = self._sci()
            else:
                # Basic fixed-point string interpolation
                s = self.FixedFormat(x, n)
                if Base._rtz:   # Remove trailing zeros
                    while "e" not in s and "E" not in s and s[-1] == "0":
                        s = s[:-1]
                if Base._rtdp and s[-1] == Base._dp: 
                    # Remove trailing decimal point
                    s = s[:-1]
            if self.u is not None and not no_units:
                un = u.FormatUnit(self.u, flat=self.flat, solidus=self.solidus)
                s = f"{s}{Base._sep}{un}"
            return decorate(s)
    def _r(self, no_color=False):  # flt
        'Return the repr string representation'
        self._check()
        f = lambda x: x if no_color else Base.wrap(x, self, force=flt)
        s = f"{repr(float(self.val))}"
        if self._units is not None:
            s = f"{repr(float(self.val))}{Base._sep}{self._units}"
        if no_color:
            return s
        return f(s)
    def __str__(self):  # flt
        return self._r() if Base._flip else self._s()
    def __repr__(self): # flt
        return self._s() if Base._flip else self._r()
    def __hash__(self): # flt
        return hash(float(self._r()))
    def copy(self): # flt
        'Returns a copy of self'
        if self._units:
            cp = flt(float(self.val), units=self._units)
        else:
            cp = flt(float(self))
        return cp
    def help(self): # flt
        print(dedent('''
        The flt class is derived from float and has the following attributes:
          c       * ANSI color escape codes in str() and repr()
          dim       Returns the Dim object for the instance's units
          eng       Format in engineering notation
          f       * Flip behavior of str() and repr()
          flat    * Print units in flat form e.g. W·m⁻²·K⁻¹
          h         Print this help
          high    * Switch to scientific notation if x > high
          low     * Switch to scientific notation if x < low 
          n       * Set/read the number of significant figures
          promote   Allows flt("1 mi/hr") + 1 (the 1 is given "mi/hr" units)
          r         The repr() string, regardless of f attribute state
          rtz     * Don't print trailing zeros
          s         The str() string, regardless of f attribute state
          sci       Format in scientific notation
          sigcomp * Only compare this number of sig figures for == if not None
          solidus * Print units in solidus form e.g. W//m²·K
          t       * Date and time
          val       Value in given units
             * means the attribute affects all flt and cps instances'''[1:]))
    # ----------------------------------------------------------------------
    ## Arithmetic functions
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
            if not(ii(other, float) and self.u is None):
                raise TypeError("Second operand must be a flt")
            other = flt(other)
        if self.u is not None:
            if u.dim(other.u) != u.dim(self.u):
                raise TypeError("Arguments must have the same unit dimensions")
        elif self.u is None and other.u is not None:
            raise TypeError("Arguments must both have no units")
        rem = abs(float(self.val) % float(other.val))
        assert(0 <= rem <= abs(other))
        rem *= -1 if other < 0 else 1
        return rem
    def __divmod__(self, other):    # flt
        '''Return (q, rem) where q is how many integer units of other are in
        self and rem is a float giving the remainder.
        '''
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
        q = math.floor(float(self.val)/float(other.val))
        rem = self % other
        # Note self could be mi/hr and other could be km/hour, so we
        # need to correct for the non-unity conversion factor
        units = Base.get_units(self, other, operator.truediv)
        conv = float(u.u(units))
        return q, float(rem)*conv
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
        return flt(abs(float(self.val)), units=self.u)
    def __ne__(self, other):    # flt
        return not (self == other)
    def __eq__(self, other):    # flt
        '''To be equal, two flt objects must have the same unit
        dimensions and the same SI values.  With no units, they must be
        numerically equal.
 
        If the sigcomp attribute is defined, it defines the number of
        significant figures involved in the comparison.
        '''
        self_has_units = self._units is not None
        other_has_units = ii(other, flt) and other._units is not None
        if self_has_units and other_has_units:
            # They are both flt instances
            if not Base.eq_dim(self, other):
                return False
            # Comparison will be below
        elif self_has_units and not other_has_units:
            if Base._promote:
                other = flt(other, units=self._units)
                return float(self) == float(other)
            return False
        elif not self_has_units and other_has_units:
            if Base._promote:
                me = flt(float(self), units=self._units)
                return float(me) == float(other)
            return False
        else:
            if ii(other, complex):
                if other.imag:
                    return False
                # Convert other to flt for comparison
                if ii(other, cpx):
                    other = flt(other.real, units=other.u)
                else:
                    other = flt(other.real)
            elif ii(other, float) and not ii(other, flt):
                if not self_has_units:
                    return float(self) == float(other)
                else:
                    # If we can promote other, do so
                    if Base._promote:
                        other = flt(float(other), units=self._units)
                        return float(self) == float(other)
                    return False
            else:
                if Base._promote:
                    other = flt(float(other), units=self._units)
                elif self._units == None:
                    other = flt(other)
                else:
                    m = ("other must be a flt with matching units or "
                        "promote must be on")
                    raise TypeError(m)
        # Get number of significant figures to make comparison to
        n = self.sigcomp if self.sigcomp is not None else 15
        other_units = hasattr(other, "u") and bool(other.u)
        if self_has_units and other_has_units:
            if not Base.eq_dim(self, other):
                return False
            # Use their SI values
            a, b = flt(float(self)), flt(float(other))
            return Base.sig_equal(a, b, n=n)
        elif ((self_has_units and not other_has_units) or 
            (not self_has_units and other_has_units)):
            return False
        else:
            b = flt(float(other))
            return Base.sig_equal(self, b, n=n)
    def __lt__(self, other):    # flt
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
        '''Return the value as a flt in the given units (not in SI).  
        Note that the returned value will have no units.
        '''
        if 1:
            # Warning:  Using self.val is convenient because user code will
            # only see the necessary significant figures, but it should be
            # first converted to a float for internal calculations to avoid
            # exceeding the maximum recursion depth.
            if self._units is not None:
                # Convert to a float with a value of self in its given units
                x = float(self)/u.u(self._units)
                return flt(x)
            return flt(float(self))
        else:
            # Test how things work returning a float
            if self._units is not None:
                # Convert to a float with a value of self in its given units
                return float(self)/u.u(self._units)
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
            if ii(imag, str):
                if units is not None:
                    s = "Ambiguous units (imag or units parameter?)"
                    raise ValueError(s)
                instance._units = imag
                to_SI = u.u(imag)
            else:
                instance._units = units
        elif ii(real, numbers.Real):
            re = float(real)*to_SI
            if ii(imag, numbers.Real):
                if ii(real, flt):
                    if units is not None and real.u is not None:
                        raise ValueError("real can't have units")
                if ii(imag, flt):
                    if units is not None and imag.u is not None:
                        raise ValueError("imag can't have units")
                re, im = float(real)*to_SI, float(imag)*to_SI
            elif ii(imag, str):
                re, im = float(real)*to_SI, float(imag)*to_SI
            elif imag is None:
                im = float(0)
            else:
                raise TypeError("imag not of proper type")
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
                    if ii(imag, str):
                        # It must be a unit
                        un = imag
                        to_SI = u.u(un)
                        if units is not None:
                            m = "Cannot have units in string and units keyword"
                            raise ValueError(m)
                    elif imag:
                        raise ValueError("Can't use 'i' or 'j' and give imag number")
                    z = complex(num)
                    re, im = z.real*to_SI, z.imag*to_SI
                else:
                    re = float(num)*to_SI
                    im = float(imag)*to_SI
                instance = super().__new__(cls, re, im)
                instance._real = flt(f(re))
                instance._imag = flt(f(im))
                instance._units = un
            else:
                raise TypeError("Unexpected type for real")
        instance._to_SI = to_SI
        return instance
    def _pol(self, repr=False): # cpx
        'Return polar form'
        f = lambda x:  Base.wrap(x, self)
        if self.u is None:
            r, theta = [flt(i) for i in polar(self)]
        else:
            # Have to remove the units to call cmath.polar()
            conv = 1/u.u(self.u)
            z = complex(self.real*conv, self.imag*conv)
            r, theta = [flt(i) for i in polar(z)]
        theta *= 1 if self.rad else 180/pi
        deg = "" if self.rad else "°"
        if repr:
            s = f"{r._r(no_color=True)}∠{theta._r(no_color=True)}{deg}"
        else:
            s = f"{r._s(no_color=True)}∠{theta._s(no_color=True)}{deg}"
        if self.u is not None:
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
        else:        # Rectangular coordinates
            conv = 1/u.u(self.u) if self.u else 1
            r, i = self._real*conv, self._imag*conv
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
        conv = 1/u.u(self.u) if self.u else 1   # SI to original units
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
                if self.u:  # Include units
                    s = f"({r}{sgn}{i}{I}){Base._sep}{self.u}"
        return f(s)
    def __str__(self):  # cpx
        return self._r() if Base._flip else self._s()
    def __repr__(self): # cpx
        return self._s() if Base._flip else self._r()
    def __hash__(self): # cpx
        return hash(complex(self))
    def copy(self): # cpx
        'Return a copy of self'
        if self.u:
            cp = cpx(complex(self.val), units=self.u)
        else:
            cp = cpx(complex(self))
        return cp
    def help(self): # cpx
        return print(dedent('''
        The cpx class is derived from complex and has the following attributes:
          c       * ANSI color escape codes in str() and repr()
          dim       Returns the Dim object for the instance's units
          eng       Format in engineering notation
          f       * Flip behavior of str() and repr()
          flat    * Print units in flat form e.g. W·m⁻²·K⁻¹
          h         Print this help
          high    * Switch to scientific notation if x > high
          i       * Use 'i' instead of 'j' as the imaginary unit
          imag      Return the imaginary component
          low     * Switch to scientific notation if x < low 
          n       * Set/read the number of significant figures
          nz      * Don't print zero components if True
          p       * Display in polar coordinates
          promote   Allows cpx("1 mi/hr") + 1 (the 1 is given "mi/hr" units)
          r         The repr() string, regardless of f attribute state
          rad       Display polar angle in radians
          real      Return the real component
          rtz     * Don't print trailing zeros
          s         The str() string, regardless of f attribute state
          sci       Format in scientific notation
          sigcomp * Only compare this number of sig figures for == if not None
          solidus * Print units in solidus form e.g. W//m²·K
          t       * Date and time
          val       Value in given units
             * means these attributes affect all cpx instances'''[1:]))
    ## Arithmetic functions
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
        return flt(abs(complex(self.val)), units=self.u)
    def __eq__(self, other):    # cpx
        '''To be equal, two cpx objects must have the same unit
        dimensions and the same SI values.  With no units, they must be
        numerically equal.
 
        If the sigcomp attribute is defined, it defines the number of
        significant figures involved in the comparison.
        '''
        # Get number of significant figures to make comparison to
        n = self.sigcomp if self.sigcomp is not None else 15
        other_units = hasattr(other, "u") and bool(other.u)
        self_units = bool(self.u)
        if self_units and other_units:
            if not Base.eq_dim(self, other):
                return False
            # Use their SI values
            a, b = cpx(complex(self)), cpx(complex(other))
            return Base.sig_equal(a, b, n=n)
        elif ((self_units and not other_units) or 
            (not self_units and other_units)):
            if Base._promote:
                # Use their SI values
                a, b = cpx(complex(self)), cpx(complex(other))
                return Base.sig_equal(a, b, n=n)
            else:
                return False
        else:
            b = cpx(complex(other))
            return Base.sig_equal(self, b, n=n)
    def __ne__(self, other):    # cpx
        return not (self == other)
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
        'Return the value as a cpx in the given units (not in SI)'
        if self._units is not None:
            return cpx(complex(self)/u.u(self._units))
        return self
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
        # The following strings can be used to decorate the names with
        # e.g. ANSI escape codes for color
        _left = "«"
        _right = "»"
        def __init__(self, name):
            self.name = name
        def __str__(self):
            return f"{Delegator._left}{self.name}{Delegator._right}"
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
            result = None
            try:
                result = eval(s)
            except AttributeError as err:
                raise TypeError(err) from None
            except ValueError as err:
                if str(err) == "math domain error":
                    # This can happen with e.g. asin(2) where you need
                    # to use the cmath version to get a complex result.
                    # The argument is a float, but the result is a
                    # complex and this case won't be detected by the
                    # above tests.
                    if self.name in "asin acos".split():
                        # Try using cmath
                        result = eval("c" + s)
                else:
                    raise
            except OverflowError as err:
                raise
            except Exception as err:
                print(f"Unhandled exception in f.py's Delegator:\n  '{err!r}'")
                print("Dropping into debugger")
                breakpoint() #xx
                pass
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
def GetSigFig(s, inttzsig=False):
    '''Return the number of significant figures in the string s which
    represents either a base 10 integer or a floating point number.  If
    tzsig is True, then trailing zeros of are not removed, meaning they
    are significant.
 
    Trailing 0 characters on integers are ambiguous in terms of
    significance and all, some, or none may be significant.  To avoid
    this ambiguity, use scientific notation.
    '''
    e = ValueError("'{}' is an illegal number form".format(s))
    dp = locale.localeconv()["decimal_point"]
    def RemoveSign(str):
        if str and str[0] in "+-":
            return str[1:]
        return str
    def rtz(s):     # Remove trailing zeros from string s
        dq = deque(s)
        while len(dq) > 1 and dq[-1] == "0":
            dq.pop()
        return ''.join(dq)
    def rlz(s):   # Remove leading zeros
        dq = deque(s)
        while len(dq) > 1 and dq[0] == "0" and not dq[-1] == dp:
            dq.popleft()
        return ''.join(dq)
    def Canonicalize(s):
        '''Remove any uncertainty, spaces, sign, and exponent and return
        the significand.
        '''
        t = s.replace(" ", "")
        # Remove any exponent portion
        if "e" in t:
            try:
                left, right = s.split("e")
            except ValueError:
                raise e
            t = left
        if not t:
            raise e
        t = RemoveSign(t)
        if t.count(dp) > 1:
            raise e
        return t
    #--------------------
    if not isinstance(s, str):
        raise ValueError("Argument must be a string")
    t = Canonicalize(s.lower().strip())
    if dp not in t:
        # It's an integer
        t = str(int(t))
        if inttzsig:
            return len(t)
        return len(rtz(t))
    # It's a float
    try:
        # It's valid if it can be converted to a Decimal
        D(t)
    except Exception:
        raise e
    t = rlz(t)  # Remove leading zeros up to the first nonzero digit or "."
    t = t.replace(dp, "")  # Remove decimal point
    # Remove any leading zeros but only if the string is not all zeros
    if set(t) != set("0"):
        t = rlz(t)
    return len(t)
if 0:
    exit()
if __name__ == "__main__": 
    from lwtest import run, raises, assert_equal, Assert
    eps = 1e-15
    def Equal(a, b, reltol=eps):
        'Return True if a == b within the indicated tolerance'
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
            raise TypeError("Both a and b must be flt or cpx")
    def Test_sig_equal():
        '''Base.sig_equal compares two numbers to a specified number of
        significant figures and returns True if they are equal.
        
        The choice of this number for p means there will be no spurious
        rounding of the last digit.  If you choose p == pi, you'll see
        the following tests fail for n = 2, 6, and 9.  For example, for 
        n == 2, you'll see x = 3.14... and y = 3.17...  In the 
        Base.sig_equal function, the two numbers compared will be 
        Decimal('3.1') and Decimal('3.2'), leading to an inequality.
        '''
        p = 1.111111111111111
        for n in range(1, 15):
            eps = 10**-n
            a = 1 + eps
            x = flt(p)
            y = flt(p*a)
            Assert(Base.sig_equal(x, y, n=n))
            Assert(not Base.sig_equal(x, y, n=n + 1))
            x = cpx(p, p)
            y = cpx(p*a, p*a)
            Assert(Base.sig_equal(x, y, n=n))
            Assert(not Base.sig_equal(x, y, n=n + 1))
    def Test_flt_constructor():
        # No units
        with flt(0):
            # flt(X) 
            for i in (1, 1.0, flt(1), Fraction(1, 1), D("1")):
                Assert(flt(i) == float(i))
                Assert(flt(i, units=None) == float(i))
                Assert(flt(i, None) == float(i))
                x = flt(i)
                # Factory works
                Assert(x(i) == x)
            with raises(TypeError):
                flt(cpx(1))
        # With units
        with flt(0):
            one = flt(1)
            x = flt(1, units="mi/hr")
            Assert(flt(1) == one)
            Assert(flt(1, units="") == one)
            Assert(flt(1, units=None) == one)
            # With strings
            Assert(flt("1") == one)
            Assert(flt("1", units="") == one)
            Assert(flt("1", units=None) == one)
            Assert(flt(1, units="mi/hr") == x)
            Assert(flt("1", units="mi/hr") == x)
            Assert(flt("1 mi/hr") == x)
            # Factory with units works
            Assert(x(1) == x)
    def Test_cpx_constructor():
        # No units
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
            Assert(z == cpx(1, "2"))
            Assert(z == cpx("1", "2"))
            # String
            Assert(z == cpx("1+2j"))
            Assert(z == cpx("1+2i"))
        # With units
        with cpx(0):
            z = cpx(1, 2, units="mi/hr")
            Assert(z == cpx(1, 2, units="mi/hr"))
            Assert(z == cpx("1", 2, units="mi/hr"))
            Assert(z == cpx(1, "2", units="mi/hr"))
            Assert(z == cpx("1", "2", units="mi/hr"))
            # String
            Assert(z == cpx("1+2i mi/hr"))
            Assert(z == cpx("1+2i", "mi/hr"))
            Assert(z == cpx("1+2i", units="mi/hr"))
            Assert(z == cpx("1+2i", 0, units="mi/hr"))
            # Factory with units works
            Assert(z(z) == z)
            # Unallowed forms
            with raises(ValueError):
                # Which imag part should be used?
                cpx("1+2i", 1, units="mi/hr")
            with raises(ValueError):
                # Which units should be used?
                cpx("1+2i", "m/s", units="mi/hr")
    def Test_copy():
        # flt
        with flt(0):
            x = flt(1)
            Assert(x == x.copy())
            Assert(x(x) == x.copy())
            Assert(x(1) == x.copy())
            x = flt("1 mi/hr")
            xcopy = x.copy()
            Assert(x == xcopy)
            Assert(x(x) == xcopy)
            Assert(x(1) == xcopy)
        # cpx
        with cpx(0):
            z = cpx(1)
            zcopy = z.copy()
            Assert(z == zcopy)
            Assert(z(z) == zcopy)
            Assert(z(1) == zcopy)
            z = flt("1 mi/hr")
            zcopy = z.copy()
            Assert(z == zcopy)
            Assert(z(z) == zcopy)
            Assert(z(1) == zcopy)
    def Test_FixedFormat():
        x = flt(0)
        with x:
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
            s = x.FixedFormat(D(0), 3)
            Assert(s == "0.00")
    def Test_flt_arithmetic_with_units():
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
            Assert(ii(rem, float))
        # Test string interpolation behavior
        with flt(1):
            x = flt("1 mi/hr")
            assert_equal(float(x), 0.44704, reltol=eps)
            Assert(x.val == 1 and ii(x.val, float))
            Assert(x.s == "1.00\xa0mi/hr")
            Assert(x.r == "1.0\xa0mi/hr")
            x.f = 1
            Assert(x.s == "1.00\xa0mi/hr")
            Assert(x.r == "1.0\xa0mi/hr")
    def Test_reverse_flt_arithmetic_with_units():
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
            Assert(ii(rem, float))
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
    def Test_promote_flt():
        '''The promote attribute when True allows expressions like
        'flt("1 mi/hr") + 1' to be evaluated by giving the '1' the same
        units as the flt.
        '''
        x, y, expected = 2, flt("1 mi/hr"), flt("3 mi/hr")
        with y:
            # Arithmetic fails if promote False
            y.promote = 0
            with raises(TypeError):
                x + y
            with raises(TypeError):
                y + x
            with raises(TypeError):
                x - y
            with raises(TypeError):
                y - x
            # Arithmetic succeeds if promote True
            y.promote = 1
            Assert(x + y == expected)
            Assert(y + x == expected)
            Assert(x - y == y)
            Assert(y - x == -y)
        x, y =flt(1), flt("1 A")
        with y:
            for p in (False, True):
                x.promote = p
                if p:
                    Assert(x == y)
                    Assert(1 == y)
                    Assert(1.0 == y)
                    Assert(y == x)
                    Assert(y == 1)
                    Assert(y == 1.0)
                else:
                    Assert(not (x == y))
                    Assert(not (1 == y))
                    Assert(not (1.0 == y))
                    Assert(not (y == x))
                    Assert(not (y == 1))
                    Assert(not (y == 1.0))
        # Make sure == and != are opposites
        with y:
            x.promote = 0
            Assert(bool(x != y) == (not bool(x == y)))
            x.promote = 0
            Assert(bool(x != y) == (not bool(x == y)))
    def Test_promote_cpx():
        a = cpx(0)
        with a:
            a.promote = 0
            z = cpx(1+1j, "m")
            w = cpx(1+1j)
            print(f"xx Promotion for cpx doesn't work") #xx
            print(f"  NOTE:  Assert is commented out") #xx
            #Assert(z != w)
            ##xx promotion for cpx doesn't work
    def Test_sigcomp_flt():
        '''The flt/cpx sigcomp attribute is an integer that forces
        comparisons to be made to the indicated number of significant
        figures.
        '''
        # Note:  if you use a number like pi, some digits will round up,
        # some won't and the test won't pass for some values of i.
        o = 1.1111111111111111
        for i in range(2, 14):
            x = flt(o)
            y = flt(o*(1 + 10**-i))
            with x:
                x.sigcomp = i 
                Assert(x == y)
                x.sigcomp = i + 1
                Assert(x != y)
        # Check sigcomp = None
        with x:
            x.sigcomp = None
            x = flt(pi)
            y = flt(pi*(1 + 10**-16))
            Assert(x == y)
    def Test_sigcomp_cpx():
        # Note:  if you use a number like pi, some digits will round up,
        # some won't and the test won't pass for some values of i.
        o = 1.1111111111111111
        for i in range(2, 14):
            x = cpx(o, o)
            t = o*(1 + 10**-i)
            y = cpx(t, o)
            with x:
                x.sigcomp = i
                Assert(x == y)
                x.sigcomp = i + 1
                Assert(x != y)
            y = cpx(o, t)
            with x:
                x.sigcomp = i
                Assert(x == y)
                x.sigcomp = i + 1
                Assert(x != y)
        # Check sigcomp = None
        with x:
            x.sigcomp = None
            x = cpx(pi, pi)
            t = pi*(1 + 10**-16)
            y = cpx(t, pi)
            Assert(x == y)
            y = cpx(pi, t)
            Assert(x == y)
    def Test_polar():
        # No units
        z = cpx(1, 1)
        with z:
            z.n = 3
            z.p = 1
            Assert(z.s == "(1.41∠45.0°)")
            z.i = 1
            Assert(z.s == "1.41∠45.0°")
            z.rad = 1
            Assert(z.s == "1.41∠0.785")
        # Units
        z = cpx(1, 1, "mi/hr")
        nbs = Base._sep
        with z:
            z.n = 3
            z.p = 1
            Assert(z.s == f"(1.41∠45.0°){nbs}mi/hr")
            z.i = 1
            # Still have parentheses because units require them
            Assert(z.s == f"(1.41∠45.0°){nbs}mi/hr")
            z.rad = 1
            Assert(z.s == f"(1.41∠0.785){nbs}mi/hr")
    def Test_unit_formatting():
        x = flt("2.23456 W/(m2*K)")
        with x:
            Assert(x.s == "2.23 W/(m²·K)")
            x.solidus = 1
            Assert(x.s == "2.23 W//m²·K")
            x.flat = 1
            Assert(x.s == "2.23 W·m⁻²·K⁻¹")
    def Test_low_and_high():
        'Also tests flt._sci()'
        x = flt(1)
        with x:
            x.n = 2
            x.low = 0.01
            x.high = 100
            Assert(x(1).s == "1.0")
            Assert(x(10).s == "10.")
            Assert(x(100).s == "100.")
            Assert(x(99.9).s == "100.")
            Assert(x(100.9).s == "1.0e2")
            Assert(x(101).s == "1.0e2")
            Assert(x(0.1).s == "0.10")
            Assert(x(0.01).s == "0.010")
            Assert(x(0.00999).s == "1.0e-2")
            Assert(x(0.0099).s == "9.9e-3")
            Assert(x(0.001).s == "1.0e-3")
        z = cpx(1, 1)
        with z:
            z.n = 2
            z.low = 0.01
            Assert(z(1).s == "(1.0+0.0j)")
            Assert(z(0.1).s == "(0.10+0.0j)")
            Assert(z(0.01).s == "(0.010+0.0j)")
            Assert(z(0.001).s == "(1.0e-3+0.0j)")
            Assert(z(1j).s == "(0.0+1.0j)")
            Assert(z(0.1j).s == "(0.0+0.10j)")
            Assert(z(0.01j).s == "(0.0+0.010j)")
            Assert(z(0.001j).s == "(0.0+1.0e-3j)")
            Assert(z(1+1j).s == "(1.0+1.0j)")
            Assert(z(0.1+0.1j).s == "(0.10+0.10j)")
            Assert(z(0.01+0.01j).s == "(0.010+0.010j)")
            Assert(z(0.001+0.001j).s == "(1.0e-3+1.0e-3j)")
    def Test_eng():
        Expected = '''
            3.14e-9 31.4e-9 314.e-9 3.14e-6 31.4e-6 314.e-6 3.14e-3
            31.4e-3 314.e-3 3.14e0 31.4e0 314.e0 3.14e3 31.4e3 314.e3
            3.14e6 31.4e6 314.e6 3.14e9'''.split()
        with flt(0):
            for i in range(-9, 10):
                expected = Expected[i + 9]
                x = flt(pi*10**i)
                s = x._eng()
                Assert(s == expected)
            Assert(x(0)._eng() == "0.00e0")
    def TestGetSigFig():
        data = '''
            # Various forms of 0
            0 1
            +0 1
            -0 1
            0. 1
            0.0 1
            00 1
            000000 1
            .0 1
            .00 2
            0.00 2
            00.00 2
            .000000 6
            0.000000 6
            00.000000 6
        #
            1 1
            +1 1
            -1 1
            1. 1
            .000001 1
            0.1 1
            .1 1
            +.1 1
            -.1 1
            1.0 2
            10 1
            100000 1
            12300 3
            123.456 6
            +123.456 6
            -123.456 6
            123.45600 8
            012300 3
            0123.456 6
            0123.45600 8
            0.00000000000000000000000000001 1
            0.000000000000000000000000000010 2
            1e4 1
            1E4 1
            01e4 1
            01E4 1
            1.e4 1
            1.E4 1
            01.e4 1
            01.E4 1
            1.0e4 2
            1.0E4 2
            01.0e4 2
            01.0E4 2
            123.456e444444 6
            123.45600e444444 8
            000000123.456e444444 6
            000000123.45600e444444 8
        '''
        for i in data.strip().split("\n"):
            i = i.strip()
            if not i or i.startswith("#"):
                continue
            if 1:
                print("Testing", i.strip())
            try:
                s, n = i.split()
            except Exception as e:
                print(f"Unhandled exception:  '{e}'")
                print(f"Dropping into debugger")
                breakpoint() #xx
            a = GetSigFig(s)
            n = int(n)
            assert_equal(a, n)
        # Test with inttzsig
        assert_equal(GetSigFig("12300", inttzsig=False), 3)
        assert_equal(GetSigFig("12300", inttzsig=True), 5)
        # Forms that raise exceptions
        raises(ValueError, GetSigFig, 1)
        raises(ValueError, GetSigFig, 1.0)
        raises(ValueError, GetSigFig, "a")
        raises(ValueError, GetSigFig, "e2")
        raises(ValueError, GetSigFig, "1..e2")
        # Show that GetSigFig works with strings from Decimal objects
        from decimal import Decimal
        n = 50
        x = Decimal("1." + "1"*n)
        assert_equal(GetSigFig(str(x)), n + 1)
    failed, messages = run(globals(), regexp=r"^[Tt]est_", halt=1)
