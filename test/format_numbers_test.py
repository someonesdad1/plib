from decimal import Decimal
from format_numbers import FormatUnits, FormatNumber
from fractions import Fraction
from lwtest import raises, run
from math import pi
from uncertainties import ufloat

def TestUnitFormatting():
    # Basics
    s = "m"
    assert(FormatUnits(s, solidus=True) == "m")
    assert(FormatUnits(s, solidus=False) == "m")
    s = "m2"
    assert(FormatUnits(s, solidus=True)  == "m²")
    assert(FormatUnits(s, solidus=False) == "m²")
    s = "m-1"
    assert(FormatUnits(s, solidus=True)  == "1/m")
    assert(FormatUnits(s, solidus=False) == "m⁻¹")
    s = "m-2"
    assert(FormatUnits(s, solidus=True)  == "1/m²")
    assert(FormatUnits(s, solidus=False) == "m⁻²")
    # Lots of digits
    s = "m22222"
    assert(FormatUnits(s, solidus=True)  == "m²²²²²")
    assert(FormatUnits(s, solidus=False) == "m²²²²²")
    s = "m-22222"
    assert(FormatUnits(s, solidus=True)  == "1/m²²²²²")
    assert(FormatUnits(s, solidus=False) == "m⁻²²²²²")
    # + and -
    s = "m s⁻¹"
    assert(FormatUnits(s, solidus=True) == "m/s")
    assert(FormatUnits(s, solidus=False) == "m·s⁻¹")
    s = "m s⁻²"
    assert(FormatUnits(s, solidus=True) == "m/s²")
    assert(FormatUnits(s, solidus=False) == "m·s⁻²")
    # All digits handled
    s = "m1234567890"
    assert(FormatUnits(s, solidus=True)  == "m¹²³⁴⁵⁶⁷⁸⁹⁰")
    assert(FormatUnits(s, solidus=False) == "m¹²³⁴⁵⁶⁷⁸⁹⁰")
    s = "m-1234567890"
    assert(FormatUnits(s, solidus=True)  == "1/m¹²³⁴⁵⁶⁷⁸⁹⁰")
    assert(FormatUnits(s, solidus=False) == "m⁻¹²³⁴⁵⁶⁷⁸⁹⁰")
    # + ignored
    s = "m+2"
    assert(FormatUnits(s, solidus=True)  == "m²")
    assert(FormatUnits(s, solidus=False) == "m²")
    s = "m+2 m-2"
    assert(FormatUnits(s, solidus=True)  == "m²/m²")
    assert(FormatUnits(s, solidus=False) == "m²·m⁻²")
    # Just a digit
    s = "2"
    raises(ValueError, FormatUnits, s)

def TestFormatFraction():
    # Regular fraction
    f = Fraction(2, 3)
    s = FormatNumber(f, units="m s-1", solidus=True)
    assert(s == "²/₃ m/s")
    s = FormatNumber(f, units="m s-1", solidus=False)
    assert(s == "²/₃ m·s⁻¹")
    # Mixed/improper fraction
    f = Fraction(3, 2)
    s = FormatNumber(f, units="m s-1", solidus=True, improper=False)
    assert(s == "1¹/₂ m/s")
    s = FormatNumber(f, units="m s-1", solidus=True, improper=True)
    assert(s == "³/₂ m/s")
    # Fixed length
    f = Fraction(2, 3)
    s = FormatNumber(f, solidus=True, length=7, position="<")
    assert(s == "²/₃    ")
    s = FormatNumber(f, solidus=True, length=7, position="^")
    assert(s == "  ²/₃  ")
    s = FormatNumber(f, solidus=True, length=7, position=">")
    assert(s == "    ²/₃")
    raises(ValueError, FormatNumber, f, solidus=True, length=2, position=">")

def TestFormatNumber():
    x = pi
    s = FormatNumber(x, units="m s-1")
    assert(s == "3.14 m·s⁻¹")
    s = FormatNumber(x, units="m s-1", digits=8)
    assert(s == "3.1415927 m·s⁻¹")
    x = pi*1e-34
    s = FormatNumber(x, units="m s-1")
    assert(s == "3.14×10⁻³⁴ m·s⁻¹")
    # Ufloat
    x = ufloat(pi*1e8, 0.0123e8)
    s = FormatNumber(x, units="m s-1")
    assert(s == "3.14(1)×10⁸ m·s⁻¹")
    # Decimal
    x = Decimal("3.14159e8")
    s = FormatNumber(x, units="m s-1")
    assert(s == "3.14×10⁸ m·s⁻¹")
    s = FormatNumber(x, units="m s-1", digits=6)
    assert(s == "3.14159×10⁸ m·s⁻¹")
    # Integer
    x = 314159
    s = FormatNumber(x, units="m s-1")
    assert(s == "314159 m·s⁻¹")
    # String
    x = "314159"
    s = FormatNumber(x, units="m s-1")
    assert(s == "314159 m·s⁻¹")

if __name__ == "__main__":
    exit(run(globals())[0])
