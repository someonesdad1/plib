'''
Self-tests for number.py
'''
import contextlib
import decimal
import fractions
import io
import sys
import mpmath
from number import Num, NumType, StringParser, unit_arbiter, Dbg, Bug
from lwtest import Assert, raises, run
import dptypes
assert mpmath.mp.dps == 15
if 1:   # Type abbreviations
    Int, Rat, Flt, Cpx = NumType.Int, NumType.Rat, NumType.Flt, NumType.Cpx
    Unc, UncCpx = NumType.Unc, NumType.UncCpx
    Fr = fractions.Fraction
    mpf = mpmath.mpf
    mpc = mpmath.mpc
# CHUNK: NumTestNumeric
if 1:   # Numeric tests
    def Test_Arithmetic():
        if 1:   # Test addition
            digits = 10     # Compare things with units to this number of digits
            if 1:   # Integer & real
                x = Num("1.0", "ft")
                y = Num("1", "m")
                result = x + y
                expected = "4.28083989501312"   # 15 digit GNU units answer
                Assert(result.is_equal(Num(expected, "ft"), digits))
            if 1:   # Rational
                x = Num("3/8", "in")
                y = Num("24/16", "in")
                result = x + y
                if 0:   # This is old test when the result was a rational
                    # Mike and I agreed it doesn't really make sense to spend effort
                    # fixing this now.  Maybe later it will feel more important if a
                    # special use case needs it.
                    expected = Num("15/8", "in")
                else:
                    expected = Num("1.875", "inch")
                Assert(result.is_equal(expected, digits))
                # See if an integer and fraction remain a fraction
                x = Num("3/8")
                y = Num("1")
                result = x + y
                expected = Num("11/8")
                Assert(result == expected)
                # Fraction and float should give a float
                x = Num("3/8")
                y = Num("1.0")
                result = x + y
                expected = Num("1.375") # Fractions that are powers of 2 are exact floats
                Assert(result == expected)
        if 1:   # Test subtraction
            if 1:   # Integer & real
                x = Num("1", "ft")
                y = Num("1", "m")
                result = x - y
                expected = Num('-2.28083989501312 ft')
                Assert(result == expected)
            if 1:   # Rational
                x = Num("3/8", "in")
                y = Num("24/16", "in")
                result = x - y
                #expected = Num("-1.125 inch")
                expected = Num("-9/8", "in")   # 3/8 - 12/8 = -9/8
                Assert(result == expected)
        if 1:   # Test multiplication
            if 1:   # Integer & real
                x = Num("1.5", "V")
                y = Num("2.0", "A")
                result = x*y
                expected = "3.0"
                Assert(result._real == mpmath.mpf(expected))
                #Assert(result == Num("3.0 kg*m^2/s^3"))  Old parse; new keeps V*A
                Assert(result == Num("3.0 (V)*(A)"))
            if 1:   # Rational
                x = Num("3/8", "in")
                y = Num("24/16", "in")
                result = x*y
                expected = Num("9/16", "(in)*(in)")   # 3/8*12/8 = 36/64 = 9/16
                #expected = Num("0.00036290249999999997 m^2")
                Assert(result == expected)
        if 1:   # Test division
            if 1:   # Integer & real
                x = Num("1.0", "ft")
                y = Num("1", "m")
                result = x/y
                #expected = Num("0.30480000000000002") Older conversion to float
                expected = Num("1.0 (ft)/(m)")
                Assert(result == expected)
            if 1:   # Rational
                x = Num("3/8", "in")
                y = Num("24/16", "in")
                result = x/y
                #expected = Num("0.25") Older conversion to float
                expected = Num("1/4 (in)/(in)")
                Assert(result == expected)
    def Test_ArithmeticWithTypes():
        '''The purpose of this test is to verify that the binary operations produce the type
        results expected.
        '''
        if 1:   # Shows downcasting
            # Downcasting to a Rat happens if the denominator is <= 1e5 and
            # mpf(numerator/denominator) == original mpf
            I = Num("2")
            R = Num("3/2")
            F = Num("2.5")
            C = Num("1+i")
            for case in (I*I, 2*I, 2.0*I, Fr(1, 2)*I, I*R, I*F):
                Assert(case.mytype == Int)
            Assert((R*F).mytype == Rat)
            # This gets a Rat
            x = Num("3.45")
            y = Num("4")
            Assert((x*y).mytype == Rat)
    def Test_Comparisons():
        if 1:   # Show we get exception when trying to compare nonconformable units
            x = Num("1 m")
            y = Num("1.0 J")
            z = Num("3.28083989501312 ft")
            with raises(ValueError):
                x < y
            with raises(ValueError):
                x <= y
            with raises(ValueError):
                x > y
            with raises(ValueError):
                x >= y
        if 1:   # Check equality testing
            Assert(x != y)
            Assert(x == z)
    def Test_Functions():
        x = Num(0)
        from number import radians, sin
        if 1:   # Prove radians() and sin() are in the global namespace
            x = Num(radians(30))
            Assert(sin(x).approx(0.5, 10))
    def Test_Infection():
        '''The Num class follows the infection model in that a Num instance with
        another instance in a binary operation will return the Num type, "infecting"
        the calculation.
        '''
        ptypes = (
            (1, NumType.Int), 
            (1.0, NumType.Int),
            (1+0j, NumType.Int),    # Gets downcast
            (1+1j, NumType.Cpx),
            (fractions.Fraction(1, 1), NumType.Int),    # Gets downcast
            (fractions.Fraction(1, 2), NumType.Rat),
            (decimal.Decimal("1"), NumType.Int)
        )
        y = Num("1")
        Assert(y.mytype == NumType.Int)
        def _Check(cond, op, types, got="", expected="", stop=False):
            if cond:
                return
            print(f"Failure:     {op}")
            print(f"  types:     {types}")
            print(f"  got:       {got}")
            print(f"  expected:  {expected}")
            if stop:
                exit()
        d = {1:"Int", 2:"Rat", 3:"Flt", 4:"Cpx", 5:"Unc"}
        for x, mytype in ptypes:
            '''
            No-stop Assert[number.py:4384]:
            op       = "Fraction(1, 1) + Num('1.0')"
            types    = "Rat + Flt"  # <--- Added this
            got      = <NumType.Flt: 3>
            expected = <NumType.Int: 1>
            '''
            if 1:
                z = x + y
                op = f"{x!r} + {y!r}"
                types = f"{d[Num(x).mytype]} + {d[y.mytype]}"
                _Check(z.mytype == mytype, op, types, got=d[z.mytype], expected=d[mytype])
                #
                z = y + x
                op = f"{y!r} + {x!r}"
                types = f"{d[y.mytype]} + {d[Num(x).mytype]}"
                _Check(z.mytype == mytype, op, types, got=d[z.mytype], expected=d[mytype])
            if 1:
                z = x - y
                op = f"{x!r} - {y!r}"
                types = f"{d[Num(x).mytype]} - {d[y.mytype]}"
                _Check(z.mytype == mytype, op, types, got=d[z.mytype], expected=d[mytype])
                #
                z = y - x
                op = f"{y!r} - {x!r}"
                types = f"{d[y.mytype]} - {d[Num(x).mytype]}"
                _Check(z.mytype == mytype, op, types, got=d[z.mytype], expected=d[mytype])
            if 1:
                z = x * y
                op = f"{x!r} * {y!r}"
                types = f"{d[Num(x).mytype]} * {d[y.mytype]}"
                _Check(z.mytype == mytype, op, types, got=d[z.mytype], expected=d[mytype])
                #
                z = y * x
                op = f"{y!r} * {x!r}"
                types = f"{d[y.mytype]} * {d[Num(x).mytype]}"
                _Check(z.mytype == mytype, op, types, got=d[z.mytype], expected=d[mytype])
            if 1:
                z = x / y
                op = f"{x!r} / {y!r}"
                types = f"{d[Num(x).mytype]} / {d[y.mytype]}"
                _Check(z.mytype == mytype, op, types, got=d[z.mytype], expected=d[mytype])
                #
                z = y / x
                op = f"{y!r} / {x!r}"
                types = f"{d[y.mytype]} / {d[Num(x).mytype]}"
                if x == fractions.Fraction(1, 2):
                    mytype = NumType.Int
                _Check(z.mytype == mytype, op, types, got=d[z.mytype], expected=d[mytype])
            y += x
            Assert(isinstance(y, Num))
            y -= x
            Assert(isinstance(y, Num))
            y *= x
            Assert(isinstance(y, Num))
            y /= x
            Assert(isinstance(y, Num))
# END_CHUNK: NumTestNumeric

# CHUNK: NumTestConstructor
if 1:   # Constructor, new unit, uncertainty tests
    def Test_Constructor_Strings():
        zero = 0
        ndigits = min(max(1, 7*mpmath.mp.dps//8), mpmath.mp.dps)
        test_cases = [("1", NumType.Int),
                        ("1/2", NumType.Rat),
                        ("1.2", NumType.Flt),
                        ("1.2e3", NumType.Flt),
                        ("1+2j", NumType.Cpx)]
        for s, typ in test_cases:
            x = Num(s)
            Assert(x.mytype == typ, expected=typ, got=x.mytype)
            # Check numerical value
            if s == "1":
                Assert(x._val.numerator == 1 and x._val.denominator == 1)
            elif s == "1/2":
                Assert(x._val.numerator == 1 and x._val.denominator == 2)
            elif s == "1.2":
                Assert(x._real == mpmath.mpf(s))
                Assert(x._imag == zero)
            elif s == "1.2e3":
                Assert(x.approx(Num("1200/1"), ndigits))
                Assert(x._imag == zero)
            elif s == "1+2j":
                Assert(x._real == mpmath.mpf("1") and x._imag == mpmath.mpf("2"))
        # Test using a long string to show we aren't dropping back to standard 64
        # bit float precision
        with mpmath.extradps(20):
            sx = "1.123456789012345678901234567890"
            sy = "11.23456789012345678901234567890"
            x = mpmath.mpf(sx)
            y = mpmath.mpf(sy)
            result = x*y
            expected = mpmath.mpf("12.621551567779301945529644873425361979")
            Assert(result == expected)
            x = Num(sx + " m")
            y = Num(sy + " kg")
            result = x*y
            expected = Num("12.621551567779301945529644873425361979 (m)*(kg)")
            Assert(result == expected)
    def Test_Constructor_With_Numbers():
        zero = 0
        if 1:   # No input
            num = Num()
            Assert(num._real == 0 and num._imag == 0)
            Assert(num.mytype == NumType.Int)
        if 1:   # int
            if 1:   # Positive
                x, T = 30957357, NumType.Int
                num = Num(x)
                Assert(num._val.numerator == x and num._val.denominator == 1)
                Assert(num.mytype == T)
                # As string
                num = Num(str(x))
                Assert(num._val.numerator == x and num._val.denominator == 1)
                Assert(num.mytype == T)
            if 1:   # Negative
                x, T = -30957357, NumType.Int
                num = Num(x)
                Assert(num._val.numerator == x and num._val.denominator == 1)
                Assert(num.mytype == T)
                # As string
                num = Num(str(x))
                Assert(num._val.numerator == x and num._val.denominator == 1)
                Assert(num.mytype == T)
        if 1:   # Rational
            x, T = "-3/8", NumType.Rat
            num = Num(x)
            Assert(num._val.numerator == -3 and num._val.denominator == 8)
            Assert(num.mytype == T)
            Assert(num == Num("-0.375"))
        if 1:   # float
            x, T = 3095.7357, NumType.Flt
            num = Num(x)
            Assert(num._real == x and num._imag == 0)
            Assert(num.mytype == T)
            num = Num(-x)
            Assert(num._real == -x and num._imag == 0)
            Assert(num.mytype == T)
        if 1:   # Decimal
            s = "3095.7357"
            x, T = decimal.Decimal(s), NumType.Flt
            num = Num(x)
            Assert(num._real == mpmath.mpf(s) and num._imag == zero)
            Assert(num.mytype == T)
            num = Num(-x)
            Assert(num._real == -x and num._imag == zero)
            Assert(num.mytype == T)
        if 1:   # mpmath.mpf
            s, T = "3095.7357", NumType.Flt
            x = mpmath.mpf(s)
            num = Num(x)
            Assert(num._real == x and num._imag == zero)
            Assert(num.mytype == T)
            num = Num(-x)
            Assert(num._real == -x and num._imag == zero)
            Assert(num.mytype == T)
        if 1:   # Complex
            x, T = -1+3j, NumType.Cpx
            num = Num(x)
            Assert(num._real == mpmath.mpf(-1) and num._imag == mpmath.mpf(3))
            Assert(num.mytype == T)
            num = Num(-x)
            Assert(num._real == mpmath.mpf(1) and num._imag == mpmath.mpf(-3))
            Assert(num.mytype == T)
        if 1:   # mpmath.mpc
            x, T = mpmath.mpc(-1, 3), NumType.Cpx
            num = Num(x)
            Assert(num._real == mpmath.mpf(-1) and num._imag == mpmath.mpf(3))
            Assert(num.mytype == T)
            num = Num(-x)
            Assert(num._real == mpmath.mpf(1) and num._imag == mpmath.mpf(-3))
            Assert(num.mytype == T)
        if 1:   # Rational
            pass
        if 1:   # Unc
            pass
    def Test_New_Unit():
        return
        # I've shut this off, as it has been tested and works
        if 0:
            basename = "delete_me_"
            for i in range(8):
                c = random.randint(97, 122)
                basename += chr(c)
            x = Num("1 m")
            print(f"basename = {basename!r}")
            x.base(basename) # The Arbiter will turn this into "name\t!"
    def Test_Uncertainty():
        '''This output came from the _unc.py script, which uses the python
        uncertainties library to calculate the results.  I feel the Num class
        must reproduce its results.
        
        Introduction
            This simulates a measurement made in the yard with a Starrett fiberglass
            200 foot tape measure.  The tape measure is graduated in units of 0.01 ft.
            I have no standard or calibration to know the uncertainty, so I'm forced
            to estimate a type B uncertainty.  Much of the measurement uncertainty
            won't come from the uncertainty in the tape measure itself; it will come
            from going over the bumpy lawn and having to be pulled on to get things
            straighter (tape stretch and small cumulative cosine errors).  I'll
            estimate the uncertainty at 0.1 ft, which means the standard deviation is
            about 1.2 inches.  If you regard a measurement as "nearly certain" if it's
            within 3 standard deviations, then that means we regard each measurement
            as "known" within about ±3.5 inches as a near certainty.  For a 50 to 100
            ft typical measurement in the yard, that sounds reasonable.
        
        Basic arithmetic:
            x1 = 100.00(10)
            x2 = 150.00(10)
            x1 + x2 = 250.00(14)
            x1 - x2 = -50.00(14)
            x1*x2 = 15000(18)
            x1/x2 = 0.66667(80)
        Problematic:
            sqrt(ufloat(0, 1)) = 0.0+/-nan
            ufloat(0, 1)/ufloat(0.0001, 1) = (0.0+/-1.0)e+04
        Trig:
            Using the cosine law and lengths x1 = 100.00+/-0.10 and x2 = 150.00+/-0.10,
            calculate the third edge of a triangle if the angle between the two lengths is 
            60(2) degrees, measured with a small compass.  The formula is
                y² = x1² + x2² - 2*x1*x2*cos(angle)
            where angle = 60.0+/-2.0°.  The task is to convert the angle to radians, then
            peform the calculation.  The terms are
                x1² = 10000+/-20
                x2² = 22500+/-30
                2*x1*x2 = (3.000+/-0.004)e+04
                cos(radians(angle)) = 0.500+/-0.030
            Putting the pieces together, the result is
                y = 132.3+/-3.4
            Note:  a calculator gives 132.388.
        
        Num constructor guts:
            self._val: fractions.Fraction = fractions.Fraction(0, 1)
            self._real: mpmath.mpf = mpmath.mpf("0")
            self._imag: mpmath.mpf = mpmath.mpf("0")
            self.re_unc: mpmath.mpf = mpmath.mpf("0")
            self.im_unc: mpmath.mpf = mpmath.mpf("0")
            self.correl: mpmath.mpf = mpmath.mpf("0")
            self._unit = ""
            self.mytype: NumType = NumType.Int
        '''
        from number import sqrt
        mpf, mpc = mpmath.mpf, mpmath.mpc
        indent = " "*4
        x1 = Num("100 ft")
        x2 = Num("150 ft")
        # Manually convert to Unc instances
        x1.re_unc = mpf("0.1")
        x2.re_unc = x1.re_unc
        x1.mytype = NumType.Unc
        x2.mytype = NumType.Unc
        if 1:   # Addition
            result = x1 + x2
            if 0:   # Dump values for debugging
                print("x1 dump")
                x1.dump(indent)
                print("\nx2 dump")
                x2.dump(indent)
                print("\nresult dump")
                result.dump(indent)
            Assert(result == Num("250 ft"))
            myresult = Num(str(result.re_unc))
            expected = mpf("0.1")*mpmath.sqrt(2)
            Assert(myresult.approx(expected, 14))
        if 1:   # Multiplication
            result = x1 * x2
            if 0:   # Dump values for debugging
                print("x1 dump")
                x1.dump(indent)
                print("\nx2 dump")
                x2.dump(indent)
                print("\nresult dump")
                result.dump(indent)
            Assert(result == Num("15000 (ft)*(ft)"))
            myresult = Num(str(result.re_unc))
            expected = mpf("18")
            Assert(myresult.approx(expected, 2))
        if 1:   # Division
            result = x1 / x2
            if 0:   # Dump values for debugging
                print("x1 dump")
                x1.dump(indent)
                print("\nx2 dump")
                x2.dump(indent)
                print("\nresult dump")
                result.dump(indent)
            Assert(result.approx(2/3, 14))
            myresult = Num(str(result.re_unc))
            expected = mpf("0.00080")
            Assert(myresult.approx(expected, 2))
        if 0:   # Cosine law example
            theta = Num(radians(60))    # 60°±2° 
            theta.re_unc = radians(mpf(2))
            theta.mytype = NumType.Unc
            result = sqrt(x1*x1 + x2*x2 - 2*x1*x2*cos(theta))
            if 0:   # Dump
                print("theta dump")
                theta.dump(indent)  # 1.0472 radians
                print("result dump")
                result.dump(indent)
        if 1:   # Large derivative
            x = Num("0")
            x.re_unc = mpf(1)
            x.mytype = NumType.Unc
            f = io.StringIO()
            with contextlib.redirect_stderr(f):
                result = sqrt(x)
            s = f.getvalue()
            if 1:
                Assert("Warning" in s)
            else:
                Bug(f'Test case ignored for now:  Warning missing about large derivative')
            # Note:  the numerical differentiation gives a large number (1.9e11 for
            # the default diff, but we're using a heuristic to select the step size
            # h) sensitivity sens in inject_math.wrapped().  However, it of course
            # doesn't result in a NaN like the python uncertainties library gets.
            Assert(result == Num(0))
            y = Num(result.re_unc)
            Assert(y.approx(22360, 4))
        if 1:   # Zero uncertainty
            x = Num("1.23(0)")
            Assert(x._real == mpmath.mpf("1.23"))
            Assert(x._imag == mpmath.mpf("0"))
            Assert(x.re_unc == mpmath.mpf("0"))
            Assert(x.im_unc == mpmath.mpf("0"))
            Assert(x.correl == mpmath.mpf("0"))
            Assert(x.mytype == NumType.Unc)
# END_CHUNK: NumTestConstructor

# CHUNK: NumTestCorner
if 1:   # Corner cases, Noether invariant
    def Test_Corners():
        N = Num
        if 1:   # 0 and 1
            # Addition
            Assert(N(0) + N(0) == N("0+0i") == N("0/1") == N("0.-0.i"))
            Assert(N(1) + N(1) == N("2+0i") == N("4/2"))
            x = N(-1) + N(-1)
            Assert(N(-1) + N(-1) == N("-2+0i") == N("-4/2"))
            # Subtraction
            Assert(N(0) - N(0) == N("0+0i") == N("0/1") == N("0.-0.i"))
            Assert(N(1) - N(1) == N("0+0i") == N("0/1") == N("0.-0.i"))
            Assert(N(-1) - N(-1) == N("0+0i") == N("0/1") == N("0.-0.i"))
            # Multiplication
            Assert(N(0)*N(0) == N("0+0i") == N("0/1") == N("0.-0.i"))
            Assert(N(1)*N(1) == N("1+0i") == N("2/2"))
            # Division
            Assert(N(0)/N(1) == N("0+0i") == N("0/1") == N("0.-0.i"))
            Assert(N(1)/N(1) == N("1+0i") == N("2/2"))
        if 1:   # With units
            # Real
            Assert(N("0 m") + N("0 m") == N("0 m"))
            Assert(N("0 m")*N("1 m") == Num('0 (m)*(m)'))
            Assert(N("0 m")/N("1 m") == N("0.0 (m)/(m)"))
            # Complex
            Assert(N("0+0j m") + N("0+0j m") == N("0+0j m"))
            Assert(N("0+0j m")*N("1+0j m") == N("0+0j m2"))
            Assert(N("0+0j m")/N("1+0j m") == N("0.0 (m)/(m)"))
            # Complex units corner case
            Assert(N("1+0i m") + N("1 m") == N("2+0j m"))
            Assert(N("1+0i m")*N("1 m") == N("1+0j m2"))
        if 1:   # Test core properties: as_mpf, etc.
            x = Num("10")
            Assert(x.mytype == NumType.Int)
            Assert(isinstance(x.as_mpf, mpmath.mpf) and x.as_mpf == mpmath.mpf("10"))
            Assert(isinstance(x.as_mpc, mpmath.mpc) and x.as_mpc == mpmath.mpc("10", 0))
            x = Num("10/20")
            Assert(isinstance(x.as_mpf, mpmath.mpf) and x.as_mpf == mpmath.mpf("1/2"))
            Assert(isinstance(x.as_mpc, mpmath.mpc) and x.as_mpc == mpmath.mpc("1/2", 0))
            x = Num("10+20j")
            Assert(isinstance(x.as_mpf, mpmath.mpf) and x.as_mpf == mpmath.mpf("10"))
            Assert(isinstance(x.as_mpc, mpmath.mpc) and x.as_mpc == mpmath.mpc("10", "20"))
        if 1:   # "1+2i m" * "3/4 A":  hope we don't get mA
            a = N("1+2i m")
            b = N("3/4 A")
            Assert(a*b == N("0.75+1.5i (m)*(A)"))
        if 1:   # Division by zero
            with raises(ZeroDivisionError):
                N("0")/N("0")
            with raises(ZeroDivisionError):
                N("0/0")
            with raises(ZeroDivisionError):
                N("0.")/N("0.")
            with raises(ZeroDivisionError):
                N("0+0i")/N("0+0i")
        if 1:   # Complex powers
            # First try no units; should maintain complex type
            x = N("1+1i")
            y = x**x
            Assert(y == N(mpmath.mpc(1, 1)**mpmath.mpc(1, 1)))
            # See that complex exponent gets exception on base with units
            a = N("1.2 m")
            with raises(TypeError):
                y = a**x
        if 0:   # Unit with rational power (base unit must be a root)
            x = N("2 gallons")
            a = N("2/3")
            result = x**a
            expected = Num("0.0385563058736576 m^2")
            if 0:
                result.dump()
                expected.dump()
                print("Are they equal?  ", result == expected)
                print(f"result.raw_value   = {result.raw_value} {type(result.raw_value)}")
                print(f"expected.raw_value = {expected.raw_value} {type(expected.raw_value)}")
            Assert(result == expected)
        else:
            Bug(f'Test case ignored for now:  N("2 gallons")**N("2/3")')
        if 1:   # In-place scaling    
            a = Num("1 m")
            a += Num("50 cm")
            Assert(a == Num("1.5 m"))
        if 1:   # Type closure
            x = Num(5)*Num(2)
            Assert(x == Num(10))
            x = Num("3/8")*Num("1/2")
            Assert(x == Num("3/16"))
            x = Num("0.375")*Num("0.5")
            Assert(x == Num("3/16") == Num("0.1875"))
        if 1:   # Downcasting
            x = Num("1+i")*Num("1-i")
            Assert(x == Num("2") and x.mytype == NumType.Int)
            x = Num("3/2")*Num("2/3")
            Assert(x == Num("1") and x.mytype == NumType.Int)
        if 1:   # inf and nan
            x = Num("inf m")
            Assert(x._real == mpmath.mpf("inf") and x.unit == "m")
            x = Num("-inf m")
            Assert(x._real == mpmath.mpf("-inf") and x.unit == "m")
            x = Num("nan m")
            Assert(mpmath.isnan(x._real) and x.unit == "m")
            x = Num("0+nanj m")
            Assert(x._real == mpmath.mpf(0) and x.unit == "m")
            Assert(mpmath.isnan(x._imag))
            x = Num("nan+nanj m")
            Assert(mpmath.isnan(x._real))
            Assert(mpmath.isnan(x._imag))
            Assert(x.unit == "m")
        if 1:   # Detect unit mistakes
            x, y = Num("0 m"), Num("0 J")
            with raises(ValueError):
                x + y
            x, y = Num("1 m"), Num("1.0 J")
            with raises(ValueError):
                x + y
            z = x*y
            Assert(z == Num('1.0 (m)*(J)'))
    def Test_Noether_Invariant():
        '''The .num component is used to normalize to a "unit vector" in the
        particular "unit" vector's direction.  This means that x/x.num returns a Num
        with unit numerical magnitude and the same units of x.  This is analogous to
        how you normalize in linear vector spaces:  a unit vector in the direction
        of v is v/|v|.
        
        I think it would be fitting to call this x/x.num the "Noether invariant";
        it's really the "unit vector" in the dimensional space described by the
        units.
        '''
        x = Num("1.23 A")
        Assert(x._real == mpmath.mpf("1.23"))
        Assert(x.unit == "A")
        y = x/x.num
        # Now y is in some sense a unit vector in the units space
        Assert(y == Num("1 A"))
        Assert(y.unit == x.unit)    # Make sure units didn't change
        Assert(x.num*y == x)        # Prove the Noether invariance
        # It has to work for complex too
        z = Num("1+2i m")
        y = z/z.num
        Assert(y.unit == z.unit)    # Make sure units didn't change
        Assert(z.num*y == z)        # Prove the Noether invariance
# END_CHUNK: NumTestCorner

# CHUNK: NumTestStringParser
if 1:   # StringParser tests
    def Test_StringParser():
        '''These are some test cases Mike and I developed together, as getting the
        string parsing to work is such a fundamental need.  Much of the work was at
        corner cases like '.0', 'inf', 'nan', and complex numbers.
        
        class ParsedPayload:
            type: NumType
            real: mpmath.mpf
            imag: mpmath.mpf = dataclasses.field(default_factory=lambda: mpmath.mpf("0"))
            numer: int = 0
            denom: int = 1
            re_unc: mpmath.mpf = dataclasses.field(default_factory=lambda: mpmath.mpf("0"))
            im_unc: mpmath.mpf = dataclasses.field(default_factory=lambda: mpmath.mpf("0"))
            unit: str = ""
        '''
        mpf, mpc = mpmath.mpf, mpmath.mpc
        p = StringParser().parse
        if 1:   # Integer
            tests = (
                ("0", 0),
                ("-0", 0),
                ("0000", 0),
                ("1", 1),
                ("-1", -1),
                ("398579387349375937593749379385740684095840", 398579387349375937593749379385740684095840),
                ("-398579387349375937593749379385740684095840", -398579387349375937593749379385740684095840),
            )
            for s, expected in tests:
                pl = p(s)
                Assert(pl.numer == expected)
                Assert(pl.type == NumType.Int)
        if 1:   # Rational
            raises(ZeroDivisionError, Num, "0/0")
            raises(ZeroDivisionError, Num, "-0/0")
            raises(ValueError, Num, "0/0.0")
            raises(ValueError, Num, "-0/0.0")
            raises(ValueError, Num, "2.0/2")
            tests = (
                ("0/1", 0, 1),
                ("0000/1", 0, 1),
                ("0000/0001", 0, 1),
                ("2/2", 1, 1),
                ("-2/2", -1, 1),
                ("2_2_2_2_2_2_2_2_2_2_2_2/2_2_2_2_2_2_2_2_2_2", 10101010101, 101010101),
                ("-2_2_2_2_2_2_2_2_2_2_2_2/2_2_2_2_2_2_2_2_2_2", -10101010101, 101010101),
            )
            for s, numer, denom in tests:
                pl = p(s)
                Assert(pl.numer == numer)
                Assert(pl.denom == denom)
                Assert(pl.type == NumType.Rat)
        if 1:   # Real
            s = "398579387349375937593749379385740684095840."
            u = "398579387_3493759375937493793857_40684095840."
            v = mpf("3.9857938734937592e+41")
            tests = (
                ("0.", mpf("0.0")),
                ("0.0", mpf("0.0")),
                (".0", mpf("0.0")),
                ("-.0", mpf("0.0")),
                ("-0.0", mpf("0.0")),
                ("1.", mpf("1.0")),
                ("1.0", mpf("1.0")),
                ("-1.", mpf("-1.0")),
                ("-.1", mpf("-0.1")),
                ("-1.0", mpf("-1.0")),
                ("inf", mpf("inf")),
                ("-inf", mpf("-inf")),
                (s, v),
                ("0000" + s, v),
                ("-" + s, -v),
                ("-0000" + s, -v),
                (u, v),
                ("-" + u, -v),
            )
            for s, expected in tests:
                pl = p(s)
                Assert(pl.real == expected)
                Assert(pl.type == NumType.Flt)
            pl = p("nan")
            Assert(mpmath.isnan(pl.real))
            Assert(pl.type == NumType.Flt)
            if 0:   # It's not important to support this test case even though python does
                pl = p("-nan")
                Assert(mpmath.isnan(pl.real))
                Assert(pl.type == NumType.Flt)
        if 1:   # Complex
            tests = (
                ("0j", 0, 0),
                ("1j", 0, 1),
                ("1/2j", 0, mpf("0.5")),
                ("0+0j", 0, 0),
                ("0+1j", 0, 1),
                ("1+0j", 1, 0),
                ("1+1j", 1, 1),
                ("1-0j", 1, 0),
                ("1-1j", 1, -1),
                ("1/3+1/2j", mpf("0.33333333333333331"), mpf("0.5")),
            )
            for s, re, im in tests:
                pl = p(s)
                Assert(pl.real == re)
                Assert(pl.imag == im)
                Assert(pl.type == NumType.Cpx)
        if 1:   # Uncertainty
            # Forms that cause exceptions
            exc = (
                "1(500)/2",
                "1.234(-0)",
                "1.234(12345678e88)",
                "1.234(inf)",
                "1.234(-inf)",
                "1.234(nan)",
            )
            for s in exc:
                with raises(ValueError):
                    p(s)
            '''
                    
            The following will be accepted as a valid number with unit because of
            our mandate that the last space delimits the unit string.  The
            parentheses and digits are allowed in unit strings.  Note that the GNU
            units command accepts this also:
                    
                You have: (123)
                You want:
                    Definition: 123
                    
            This means the Num constructor will accept it too, so it's a valid
            number with units.
                    
            '''
            s = "1.234 (12345678)"
            x = p(s)
            Assert(x.real == mpf('1.234'))
            Assert(x.unit == '(12345678)')
            Assert(x.type == NumType.Flt)
            x = Num(s)
            y = Num("3 (12345678)")
            x + y
            x - y
            x*y
            x/y
            tests = (
                ("0(0)", 0, 0),
                ("1(0)", 1, 0),
                ("-1(0)", -1, 0),
                ("0(100)", 0, 100),
                ("1(100)", 1, 100),
                ("-1(100)", -1, 100),
                ("1.234(0)e44", mpf("1.234e44"), mpf("0")),
                ("1.234(56)e44", mpf("1.234e44"), mpf("5.6000000000000011e+42")),
                ("1(10000000000000000000000000)e100", mpf("1.0e100"), mpf("1.0000000000000001e+125")),
                ("-1(10000000000000000000000000)e100", mpf("-1.0e100"), mpf("1.0000000000000001e+125")),
            )
            for s, nom, stdev in tests:
                pp = p(s)
                Assert(pp.real == nom)
                Assert(pp.re_unc == stdev)
                Assert(pp.type == NumType.Unc)
        if 1:   # Complex uncertainty
            # Forms that cause exceptions
            exc = (
                "1(500)/2-3j",
                "1.234(12345678e88)-3j",
                "1.234(inf)-3j",
                "1.234(-inf)-3j",
                "1.234(nan)-3j",
                "1+1(500)/2j",
                "1+1.234(12345678e88)j",
                "1+1.234(inf)j",
                "1+1.234(-inf)j",
                "1+1.234(nan)j",
            )
            for s in exc:
                with raises(ValueError):
                    p(s)
            # Valid forms
            tests = (
                ("0.0(2)-0.0(2)j", 0, 0, mpf("0.2"), mpf("0.2"), 0),
                ("1.0(2)-1.0(2)j", 1, -1, mpf("0.2"), mpf("0.2"), 0),
                ("-1.0(2)-1.0(2)j", -1, -1, mpf("0.2"), mpf("0.2"), 0),
                ("1.0(2)j", 0, 1, mpf("0.0"), mpf("0.2"), 0),
                ("-1.0(2)j", 0, -1, mpf("0.0"), mpf("0.2"), 0),
                # Correlation coefficient
                ("-1.0(2)-1.0(2)j<R=1>", -1, -1, mpf("0.2"), mpf("0.2"), 1),
                ("-1.0(2)-1.0(2)j<R=-1>", -1, -1, mpf("0.2"), mpf("0.2"), -1),
                ("-1.0(2)-1.0(2)j<R=2>", -1, -1, mpf("0.2"), mpf("0.2"), 2),
                ("-1.0(2)-1.0(2)j<R=-0.327>", -1, -1, mpf("0.2"), mpf("0.2"), mpf("-0.327")),
                # Hairy
                ("-147.883(22)e-12+89.112(3)e-8j", mpf("-147.883e-12"), mpf("89.112e-8"),
                    mpf('2.1999999999999998e-14'), mpf("0.003e-8"), 0),
                ("-147.883(22)e-12+89.112(3)e-8j<R=0.283>", mpf("-147.883e-12"), mpf("89.112e-8"),
                    mpf('2.1999999999999998e-14'), mpf("0.003e-8"), mpf("0.283")),
            )
            for s, re, im, re_unc, im_unc, correl in tests:
                #print(f"Test case:  {s!r}")
                pp = p(s)
                Assert(pp.real == re)
                Assert(pp.imag == im)
                Assert(pp.re_unc == re_unc)
                Assert(pp.im_unc == im_unc)
                Assert(pp.correl == correl)
                Assert(pp.type == NumType.UncCpx)
            # Correlation coefficient outside of [-1, 1] is error
            raises(ValueError, Num, "-1.0(2)-1.0(2)j<R=2>")
# END_CHUNK: NumTestStringParser
if __name__ == "__main__":  
    from number import g
    g.dbg = len(sys.argv) > 1
    exit(run(globals(), regexp=r"^Test_", halt=1, verbose=0)[0])
