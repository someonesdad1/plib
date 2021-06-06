# Note RoundOff isn't tested because it was copied in from another
# tested module.

from u import U, u, to, fromto, CT, ParseUnit, G, GetUnits, Dim, R
from u import SI_prefixes, ParseFraction, GetDim
import contextlib
import sys
from math import pi
from random import seed
from lwtest import run, raises, assert_equal
from uncertainties import ufloat, ufloat_fromstr, UFloat
from decimal import Decimal
from fractions import Fraction
from io import StringIO

from pdb import set_trace as xx
if 0:
    import debug
    debug.SetDebugger()

eps = 1e-15     # For testing float equality
seed(0)         # So results are repeatable

def Initialize(randomize=False):
    global u
    units, dims = GetUnits(randomize=randomize)
    u = U(units, dims, SI_prefixes, {"in":"inches"})

def TestEmptyString():
    Initialize()
    assert(u("") == 1)
    assert(u(" \t\n\r") == 1)

def TestNoPrefixWith_kg():
    Initialize()
    raises(ValueError, u, "zkg")

def TestBaseUnitsDefined():
    Initialize()
    for i in "m kg s A cd mol K rad sr".split():
        assert(u(i) == 1)

def TestParentheses():
    Initialize()
    assert(u("m/(s/m)") == u("m2/s") == 1)

def TestEmptyStringReturnsUnity():
    Initialize()
    assert(u("") == 1)

def TestConstantMultiplesAllowed():
    Initialize()
    assert(u("8.9*m") == 8.9*u("m"))
    assert(u("8.9*m") == u("8900*mm"))
    assert(u("8.9*lb") == u("8900*mlb"))

def TestPrefixesWork():
    Initialize()
    assert(u("Mm") == u("km")*u("km") == 1e6)
    assert(u("Ym")/u("ym") == 1e48)
    # Can spell out
    if 0:  # For this to pass, you need to enable the word prefixes
        assert(u("ym*s") == u("yoctom*s"))
        # Hyphenation not allowed
        raises(ValueError, u, "yocto-m*s")

def TestExponentiation():
    Initialize()
    assert(u("mm2") == u("mm**2") == u("mm^2") == 1e-6)
    if 0:   # This works as of 28 May 2021
        # Negative exponents not allowed
        raises(ValueError, u, "m-1")
    else:
        assert(u("inch-1") == 1/0.0254)
    # Check more complicated expressions
    assert_equal(u("(ft/min)^2"), u("ft/min")**2, abstol=eps)
    assert_equal(u("(ft/min)**2"), u("ft/min")**2, abstol=eps)
    if 0:   # This works as of 28 May 2021
        # Implied exponentiation won't work on non-trivial expressions.
        assert_equal(u("(m/s)2"), None)
    else:
        assert_equal(u("(m/s)2"), 1)
    # But the following work
    assert_equal(u("(m/s)**2"), 1)
    assert_equal(u("(m/s)^2"), 1)

def TestMultiplicationUsingSpace():
    Initialize()
    assert(u("m*s") == u("m s") == 1)

def TestNonassociativity():
    Initialize()
    assert_equal(u("mm*g/zs/mm/g*zs"), 1, abstol=eps)

def TestTypicalExpressions():
    Initialize()
    assert_equal(u("88 ft/s"), u("60 mi/hr"), reltol=eps)
    assert_equal(u("mile"), u("5280     feet"), reltol=eps)
    assert_equal(u("rightangle"), u("100*grad"), reltol=eps)
    assert_equal(u("0.0254*m"), u("inch"), reltol=eps)
    assert_equal(u("furlong"), u("660*feet"), reltol=eps)
    assert_equal(u("4*cups"), u("quart"), reltol=eps)
    assert_equal(u("4*quarts"), u("gallon"), reltol=eps)
    # The following is a special case that has loss of significance; I'm
    # not sure of the reason for this loss.
    assert_equal(u("180*degrees"), pi, reltol=4e-12)

def TestDigits():
    Initialize()
    assert_equal(u("degrees"), 0.0174532925199433, abstol=eps)
    assert_equal(u("degrees", digits=5), 0.017453)
    u.digits = 5
    assert_equal(u("degrees"), 0.017453)

def TestTypicalExpressionsAfterRandomization():
    Initialize(randomize=True)
    assert_equal(u("180*degrees"), pi*u("radian"), reltol=eps)
    assert_equal(u("88*ft/s"), u("60*mi/hr"), reltol=eps)
    assert_equal(u("mile"), u("5280*feet"), reltol=eps)
    assert_equal(u("rightangle"), u("100*grad"), reltol=eps)
    assert_equal(u("0.0254*m"), u("inch"), reltol=eps)
    assert_equal(u("furlong"), u("660*feet"), reltol=eps)
    assert_equal(u("4*cups"), u("quart"), reltol=eps)
    assert_equal(u("4*quarts"), u("gallon"), reltol=eps)

def TestStrict():
    Initialize()
    for expr, val in (("mm kg", 1e-3), ("mm2", 1e-6)):
        # No strictness means implied multiplication and exponentiation
        assert(u(expr, strict=False) == val)
        # Strictness means no implied multiplication or exponentiation
        assert_equal(u(expr, strict=True), None)

def TestWithUncertainties():
    '''This routine demonstrates that the u module can work
    together with the python uncertainties library.  This
    allows you to perform calculations with both numbers that
    have uncertainty and a unit encoded in them.
    '''
    ua, ub = "inch/lbm/Ahr", "ft/tonne/(7.3*C)"
    s = 1.7, 1
    Initialize(randomize=True)
    width = ufloat(*s)*u("m")
    other = ufloat(1, 1)*u(ua)
    r1 = width*to("kg")  # Express a length as a mass
    # More algebraically complicated conversion
    o1 = other*to(ub)
    Initialize(randomize=True)    # Repeat the calculation
    width = ufloat(*s)*u("m")
    other = ufloat(1, 1)*u(ua)
    r2 = width*to("kg")
    o2 = other*to(ub)
    # Compare the results and show they're different
    assert(r1 != r2)
    assert(o1 != o2)

def TestTemperatureConversion():
    T0, a = 273.15, 9/5.
    Tr = a*T0
    assert_equal(CT(T0, "k", "k"), T0)
    assert_equal(CT(T0, "k", "c"), 0)
    assert_equal(CT(T0, "k", "f"), 32)
    assert_equal(CT(T0, "k", "r"), Tr)
    T = 0
    assert_equal(CT(T, "c", "k"), T0)
    assert_equal(CT(T, "c", "c"), T)
    assert_equal(CT(T, "c", "f"), 32)
    assert_equal(CT(T, "c", "r"), Tr)
    T = 32
    assert_equal(CT(T, "f", "k"), T0)
    assert_equal(CT(T, "f", "c"), 0)
    assert_equal(CT(T, "f", "f"), T)
    assert_equal(CT(T, "f", "r"), Tr)
    T = Tr
    assert_equal(CT(T, "r", "k"), T0)
    assert_equal(CT(T, "r", "c"), 0)
    assert_equal(CT(T, "r", "f"), 32)
    assert_equal(CT(T, "r", "r"), T)

def Test_fromto():
    # We'll have slight roundoff issues 12 vs 12.000000000000002, so we
    # don't use the default eps.
    tol = 2e-15
    assert_equal(fromto(1, "ft", "in"), 12, abstol=tol)
    assert_equal(fromto(1, "in", "ft"), 1/12, abstol=tol)

def TestParseUnit():
    Initialize()
    # Empty string returns None (remember leading/trailing
    # whitespace is stripped off first)
    assert(ParseUnit("   ") == None)
    # A missing number also returns None
    assert(ParseUnit("a") == None)
    # But include a number and you'll get it and the unit
    assert(ParseUnit("1a") == ("1", "a"))
    # You can also have it evaluated as an expression
    assert(ParseUnit("a", allow_expr=True) == ("a", ""))
    # Common forms
    s = ("47.3e-88", "m/s")
    assert(ParseUnit("47.3e-88m/s")   == s)
    assert(ParseUnit("47.3e-88 m/s")  == s)
    assert(ParseUnit("47.3e-88  m/s") == s)
    # Pure numbers can be used
    assert(ParseUnit("4")          == ("4", ""))
    assert(ParseUnit("4 ")         == ("4", ""))
    assert(ParseUnit("4.1")        == ("4.1", ""))
    assert(ParseUnit("4.1 ")       == ("4.1", ""))
    assert(ParseUnit("47.3e-88")   == ("47.3e-88", ""))
    assert(ParseUnit("47.3e-88 ")  == ("47.3e-88", ""))
    assert(ParseUnit(" 4")         == ("4", ""))
    assert(ParseUnit(" 4 ")        == ("4", ""))
    assert(ParseUnit(" 4.1")       == ("4.1", ""))
    assert(ParseUnit(" 4.1 ")      == ("4.1", ""))
    assert(ParseUnit(" 47.3e-88")  == ("47.3e-88", ""))
    assert(ParseUnit(" 47.3e-88 ") == ("47.3e-88", ""))
    # An example of an ill-formed number that results in still
    # being interpreted as a number and a unit.
    assert(ParseUnit("1/2 m/s") == ("1", "/2 m/s"))
    # But it can be interpreted as an expression
    s = ParseUnit("1/2 m/s", allow_expr=True)
    assert(s == ("1/2", "m/s"))
    # Ability to use expressions (no spaces allowed because they're used to
    # separate the unit string from the expression)
    s = ParseUnit("47.3e-88*1.23 m/s", allow_expr=True)
    assert(s == ("47.3e-88*1.23", "m/s"))
    s = ParseUnit("47.3e-88*1.23", allow_expr=True)
    assert(s == ("47.3e-88*1.23", ""))
    s = ParseUnit("47.3e-88*1.23 ", allow_expr=True)
    assert(s == ("47.3e-88*1.23", ""))
    # Ill-formed expressions result in an exception
    raises(ValueError, ParseUnit, "a b c", allow_expr=True)
 
    # Test usage with uncertainties.  Note that because ufloats represent
    # random variables, ufloat(a, b) != ufloat(a, b) for two different
    # instances with the same constructor; you have to compare the nominal
    # value and standard deviation to determine the equality of
    # their distributions.
    if G.have_uncertainties:
        ueq = lambda a, b: (a.nominal_value == b.nominal_value and
            a.std_dev == b.std_dev)
        y = ufloat(4, 1)
        for s in ("4+/-1", "4+-1", "4(1)"):
            x, un = ParseUnit(s, allow_unc=True)
            assert(ueq(x, y))
            assert(not un)
        for s in ("4+/-1 m", "4+-1 m", "4(1) m"):
            x, un = ParseUnit(s, allow_unc=True)
            assert(ueq(x, y))
            assert(un == "m")
        # When uncertainty is zero, still should get a ufloat returned
        for s in ("4+/-0", "4+-0", "4(0)", "4"):
            x, un = ParseUnit(s, allow_unc=True)
            assert(x.nominal_value == 4)
            if s != "4":  # Has 1.0 default uncertainty
                assert(x.std_dev == 0)
            assert(not un)
        for s in ("4+/-0 m", "4+-0 m", "4(0) m", "4 m"):
            x, un = ParseUnit(s, allow_unc=True)
            assert(x.nominal_value == 4)
            if s != "4 m":  # Has 1.0 default uncertainty
                assert(x.std_dev == 0)
            assert(un == "m")
        # Here are some forms that are allowed, but semantically incorrect;
        # they can be discovered when the unit is attempted to be
        # interpreted.
        x, un = ParseUnit("4 +/-1", allow_unc=True)
        assert(x.nominal_value == 4 and x.std_dev == 1)
        assert(un == "+/-1")
        x, un = ParseUnit("4 1", allow_unc=True)
        assert(x.nominal_value == 4 and x.std_dev == 1)
        assert(un == "1")
        x, un = ParseUnit("4 1.0", allow_unc=True)
        assert(x.nominal_value == 4 and x.std_dev == 1)
        assert(un == "1.0")
        # Illegal forms should raise an exception
        raises(ValueError, ParseUnit, "4+/-1m", allow_unc=True)
        raises(ValueError, ParseUnit, "m", allow_unc=True)
    else:
        print("Warning:  uncertainties in u.py not tested")

def TestParseFraction():
    pf = ParseFraction
    expected_f = (Fraction(9, 8), "mm")
    assert(pf("   9/8 mm") == expected_f)
    assert(pf("18/16 mm") == expected_f)
    assert(pf(" 1 1/8 mm") == expected_f)
    assert(pf(" 1-1/8 mm") == expected_f)
    assert(pf(" 1+1/8 mm") == expected_f)
    assert(pf(" 1.1/8 mm") == expected_f)
    expected_r = (1.125, "mm")
    assert(pf(str(9/8) + " mm") == expected_r)
    assert(pf(str(9/8) + "    mm") == expected_r)

def TestCustomUnits():
    '''This example is from the documentation and verifies both the
    ability to define custom units and test the randomization feature
    for detecting dimensionality problems.
    '''
    '''
    This example demonstrates defining a unit system and using it to uncover
    a dimensionally-inconsistent calculation.
 
    Problem:  given a certain number of cats and dogs, calculate the amount
    of food needed to feed them, given the mass per animal needed:
 
        food per dog = 0.2 kg/dog
        food per cat = 0.1 kg/cat
        number of dogs = 7
        number of cats = 12
 
    Clearly, the answer is (7 dog)*(0.2 kg/dog) + (12 cat)*(0.1 kg/cat) or
    2.6 kg.  
 
    However, if we accidentally switched the mass per animal numbers, we'd
    blithely calculate 
 
        (7 dog)*(0.1 kg/cat) + (12 cat)*(0.2 kg/dog)
 
    and get the numerical result 3.1 kg.  If we expand the above, keeping
    the units, we get
 
        0.7*kg*(dog/cat) + 2.4*kg*(cat/dog)
 
    and it would be obvious that the terms are dimensionally inconsistent.
    '''
    seed(0)  # force repeatability
    # Make kg, dogs, and cats independent base units
    allowed = set("DCM")    # D = dog, C = cat, M = mass
    base_units = {
        "dog": Dim("D", allowed_symbols=allowed),
        "cat": Dim("C", allowed_symbols=allowed),
        "kg": Dim("M", allowed_symbols=allowed),
    }
    def GetUnits(randomize=False):
        digits = 6
        # Define the conversion factor dictionary.  If randomize is True,
        # note that the conversion factors will have random nonzero values.
        # If randomize is False, they'll all have values of 1.
        return {
            "dog": R(randomize=randomize),
            "cat": R(randomize=randomize),
            "kg": R(randomize=randomize),
        }
    def CorrectCalculation():
        units = GetUnits(randomize=False)
        print('''
Dimensionally-correct calculation
---------------------------------'''[1:])
        print("  units =", units)
        # Make our U instance for conversion factors
        u = U(units, base_units)
        # Do the correct calculations
        food_per_dog = 0.2*u("kg/dog")
        food_per_cat = 0.1*u("kg/cat")
        print('''
  food_per_dog = {food_per_dog}
  food_per_cat = {food_per_cat}'''[1:].format(**locals()))
        # Number of animals
        n_dogs =  7*u("dog")
        n_cats = 12*u("cat")
        print('''
  number of dogs = {n_dogs}
  number of cats = {n_cats}'''[1:].format(**locals()))
        # Total food amount needed in kg
        total_food_kg = n_dogs*food_per_dog + n_cats*food_per_cat
        m = ("  calculation performed = {n_dogs}*{food_per_dog} + "
             "{n_cats}*{food_per_cat} = {total_food_kg:.1f}")
        print(m.format(**locals()))
        # Report results
        print("  Total food needed in kg = {:.1f}".format(total_food_kg))
        return round(total_food_kg, 1)
    def IncorrectCalculation(randomize=False):
        # Make the deliberate mistake of swapping the cat and dog
        # numbers.
        units = GetUnits(randomize=randomize)
        randomized = "Randomized" if randomize else "Not randomized"
        print('''
Dimensionally-incorrect calculation
-----------------------------------
  ** {randomized} **'''.format(**locals()))
        print("  units =", units)
        # Make our U instance for conversion factors
        u = U(units, base_units)
        # Do the correct calculations
        food_per_dog = 0.2*u("kg/dog")
        food_per_cat = 0.1*u("kg/cat")
        print('''
  food_per_dog = {food_per_dog}
  food_per_cat = {food_per_cat}'''[1:].format(**locals()))
        # Number of animals
        n_dogs =  7*u("dog")
        n_cats = 12*u("cat")
        print('''
  number of dogs = {n_dogs}
  number of cats = {n_cats}'''[1:].format(**locals()))
        # Total food amount needed in kg.  Note the error is that we swapped
        # the n_dogs and n_cats terms.
        total_food_kg = n_cats*food_per_dog + n_dogs*food_per_cat
        m = ("  calculation performed = {n_cats}*{food_per_dog} + "
             "{n_dogs}*{food_per_cat} = {total_food_kg:.1f}")
        print(m.format(**locals()))
        # Report results
        print("  Total food needed in kg = {:.1f}".format(total_food_kg))
        return round(total_food_kg, 1)
    out = StringIO()
    with contextlib.redirect_stdout(out):
        sys.stdout = out
        total_food_kg_std = CorrectCalculation()
        assert(total_food_kg_std == 2.6)
        total_food_kg = IncorrectCalculation(randomize=False)
        assert(total_food_kg == 3.1)
        total_food_kg = IncorrectCalculation(randomize=True)
        print("u_test:  total_food_kg =", total_food_kg)
        assert(total_food_kg == 1.8)
        total_food_kg = IncorrectCalculation(randomize=True)
        print("u_test:  total_food_kg =", total_food_kg)
        assert(total_food_kg == 5.1)

def TestAdditionSubtraction():
    '''Show that compatible Dim objects can be added and subtracted.
    '''
    vel, nodim, screwy = u.dim("m/s"), u.dim(""), u.dim("m**(3/2)/A8")
    assert_equal(str(vel), 'Dim("L T-1")')
    assert_equal(str(nodim), 'Dim("")')
    assert_equal(str(screwy), 'Dim("L1.5 A-8")')
    for i in (vel, nodim, screwy):
        i + i
        i - i
    with raises(TypeError):
        vel + nodim
    # Check with numbers
    for i in (1, 2.0, Fraction(1, 3), Decimal("4.567")):
        i + nodim
        nodim + i
        with raises(TypeError):
            vel + i
        with raises(TypeError):
            i + vel

def TestMultiplicationDivision():
    '''Show that any Dim objects can be multiplied or divided.
    '''
    vel = u.dim("m/s")
    recip_vel = u.dim("s/m")
    nodim = u.dim("")
    screwy = u.dim("m**(3/2)/A8")
    recip_screwy = u.dim("A8/m^(3/2)")
    assert_equal(vel*vel, u.dim("m2/s2"))
    assert_equal(vel/vel, nodim)
    assert_equal(vel*recip_vel, nodim)
    assert_equal(screwy*screwy, u.dim("m3/A16"))
    assert_equal(screwy/screwy, nodim)
    assert_equal(screwy*recip_screwy, nodim)

def Test_find_unit():
    L = set(u.find_unit(u.dim("m/s")))
    M = set(["knot", "mph", "light", "fpm", "fps", "kph"])
    assert_equal(L, M)
    L = set(u.find_unit(u.dim("therm")))
    M = set(["Wh", "erg", "cal", "Whr", "CAL", "calorie", "kcal", "btu",
             "eV", "J", "BTU", "Calorie", "therm"])
    assert_equal(L, M)
    assert_equal(u.find_unit(u.dim("m88/s2348")), None)

def Test_GetDim():
    s = "T*m/(kg*s2)"
    u = GetDim(s)
    assert(str(u) == 'Dim("T kg-1 m s-2")')

def Test_s_attribute():
    s = "lbm*gal*gal/psi"
    u = GetDim(s)
    assert(str(u) == 'Dim("gal2 lbm psi-1")')
    assert((u*u).s == "gal**4*lbm**2/psi**2")

def Test_new_stuff():
    # Added 28 May 2021 ability to use negative exponents
    k = 26
    for i in '''
        m-1                       Dim("L-1")
        (m/s)-1                   Dim("L-1 T")
        (m/s)1                    Dim("L T-1")
        (m-1/s-1)-1               Dim("L T-1")
        m**(-0.278)               Dim("L-0.278")
        m-0.278                   Dim("L-0.278")
        m^(-78.4/26.2*0.883)      Dim("L-2.642259541984733")
        m**(-78.4/26.2*0.883)     Dim("L-2.642259541984733")
        m(-78.4/26.2*0.883)       Dim("L-2.642259541984733")
        m^(-3/4)                  Dim("L-0.75")
        m**(-3/4)                 Dim("L-0.75")
        m(-3/4)                   Dim("L-0.75")
        ym                        Dim("L")'''.split("\n"):
        i = i.strip()
        if not i:
            continue
        s, e = i[:k].strip(), i[k:].strip()
        d = u(s, dim=1)[1]
        assert(e == str(d))
    # Should return None
    for i in "yocto-m m**x".split():
        assert(u(i) is None)
    for i in "m**(1j)".split():
        with raises(TypeError):
            u(i, dim=1)[1]

if __name__ == "__main__":
    exit(run(globals())[0])
