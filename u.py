'''
Unit conversion utilities
    Please see the u.pdf documentation file that came in the package this
    script came in.  Here, we'll give an overview of the module's use.
    
    The main functions you'll use are u() and to().  You can either use
    the built-in set of SI and non-SI units or supply definitions of your
    own.
    
    You endow a variable with a physical unit by a line such as
    
        velocity = 3.7*u("miles/hour")
    
    The function u() returns a conversion factor that, when multiplied by
    the indicated unit, results in a number that is equivalent to the same
    dimensional quantity in base SI units.  Thus, the function call
    u("miles/hour") returns the number 0.44704.  If you print the variable
    velocity, it will have the value 1.654048; this is 3.7 miles per hour
    expressed in meters per second.  Note that the velocity variable is a
    python floating point number with no "knowledge" of the dimensions of its
    "attached" units, so it's up to you, the programmer, to keep things
    dimensionally consistent.
    
    When you want the variable velocity to contain the numerical value in
    ft/minute, you can use the following equivalent methods:
    
        velocity /= u("ft/minute")              # Divide by a u() call
        velocity = to(velocity, "ft/minute")    # Use a convenience function
    
    Numerous aliases are defined in the built-in set of SI units (and it's
    trivial to define others).  Thus, you can use
    
        feet, foot, ft
        min, minute, minutes
    
    If you use the following process when developing code:
    
        * Define all physical variables' numerical values using the u()
        function, even the dimensionless ones.
    
        * Perform all intermediate calculations knowing that all your
        variables are in base SI units (or derived units in terms of
        them).
    
        * For output, use the to() or u() functions to convert the
        variables' numerical values to the units of choice.
    
    you'll reduce the likelihood of making dimensional mistakes in your
    code.
    
        However, an important warning is that this is strictly a units
        conversion module.  Except for the dimensional checking feature
        mentioned below, the module is only useful for converting between
        units with identical dimensional structure.
    
    The ParseUnit() function is provided to help pick apart into the
    number and unit an input string a user might type in at a prompt in a
    program.

    The ParseFraction() function is used to get a number and a unit when
    the number can be an int, float, or proper or improper fraction.
    
    The unit 'm/s/s' is ambiguous in normal scientific usage and thus not
    allowed by SI rules.  Since this module uses python's expression parser
    to evaluate expressions, it means (m/s)/s to the parser, so is
    acceptable to this module.
    
    Dimensional checking
    --------------------
    
    A randomization feature is used to help discover dimensional errors in
    calculations; the idea of using random numbers to "orthogonalize" unit
    conversion factors to help find dimensional errors is is apparently
    due to Steve Byrnes and is given in his numericalunits package at
    http://pypi.python.org/pypi/numericalunits.  You can study the function
    GetConvenienceUInstance() to see how to instantiate a set of units using
    this functionality.
    
        Check out the Analon slide rule from Keuffel & Esser from the
        mid-1960's, as it used the idea of assigning real numbers to
        dimensions in a consistent way for dimensional analysis.  An
        emulator is at
        http://www.marksmath.com/slide-rules/virtual/ke-analon/ke-analon.html
    
        Also take a look at P. Bridgman's classic 1922 text on dimensional
        analysis.
    
    You can use the dim() function to determine the physical dimensions of a
    unit expression.  This returns a Dim object that encapsulates the
    dimensions.
'''
 
# Copyright (C) 2014, 2015 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
if 1:   # Standard imports
    import functools
    import io
    import random
    import re
    import sys
    import tokenize
    from collections import defaultdict
    from fractions import Fraction
    from decimal import Decimal
    from random import Random
    from math import pi
    from pdb import set_trace as xx
if 1:   # Custom imports
    if 0:
        import debug
        debug.SetDebugger()
    try:
        import uncertainties
        _have_uncertainties = True
    except ImportError:
        _have_uncertainties = False

if 1:   # Global variables
    class G:    # Global variable container
        # Utility stuff
        ii = isinstance
        have_uncertainties = _have_uncertainties
        # Regular expression that will match an integer or floating point
        # number in its string representation.
        _num_unit = re.compile(r'''
                (?x)                            # Allow verbosity
                ^                               # Must match at beginning
                (                               # Group
                    [+-]?                       # Optional sign
                    \.\d+                       # Number like .345
                    ([eE][+-]?\d+)?|            # Optional exponent
                # or
                    [+-]?                       # Optional sign
                    \d+\.?\d*                   # Number:  2.345
                    ([eE][+-]?\d+)?             # Optional exponent
                )                               # End group
        '''.strip())
        # This global variable holds the number of significant digits to
        # round to.  While the typical floating point implementation
        # uses around 16 digits, the default value is set to 12.  Very
        # few problems in the practical world need to deal with
        # measurements to more than 12 significant figures, so this
        # default should be suitable for most practical problems.  This
        # lower number is used to help avoid string interpolations like
        # '34.199999999999', which should be '34.2'.
        number_of_digits = 12
    del _have_uncertainties

    # Public symbols when "from u import *" is used.
    __all__ = [
        "CT",
        "dim",
        "Dim",
        "fromto",
        "ParseUnit",
        "RoundOff",
        "SI_prefixes",
        "to",
        "u",
        "U",
    ]
    # The SI_prefixes dictionary contains the SI prefixes as keys; the
    # values are the conversion factors as strings.
    SI_prefixes = {
        "y"  : "1e-24",
        "z"  : "1e-21",
        "a"  : "1e-18",
        "f"  : "1e-15",
        "p"  : "1e-12",
        "n"  : "1e-9",
        "u"  : "1e-6",
        "μ"  : "1e-6",
        "m"  : "1e-3",
        "c"  : "1e-2",
        "d"  : "1e-1",
        "da" : "1e1",
        "h"  : "1e2",
        "k"  : "1e3",
        "M"  : "1e6",
        "G"  : "1e9",
        "T"  : "1e12",
        "P"  : "1e15",
        "E"  : "1e18",
        "Z"  : "1e21",
        "Y"  : "1e24",
    }
    if 0:   # Set to 1 if you also want the following
        SI_additional = {
            "yocto"  : "1e-24",
            "zepto"  : "1e-21",
            "atto"   : "1e-18",
            "femto"  : "1e-15",
            "pico"   : "1e-12",
            "nano"   : "1e-9",
            "micro"  : "1e-6",
            "milli"  : "1e-3",
            "centi"  : "1e-2",
            "deci"   : "1e-1",
            "deca"   : "1e1",
            "deka"   : "1e1",
            "hecto"  : "1e2",
            "kilo"   : "1e3",
            "mega"   : "1e6",
            "giga"   : "1e9",
            "tera"   : "1e12",
            "peta"   : "1e15",
            "eta"    : "1e18",
            "zetta"  : "1e21",
            "yotta"  : "1e24",
        }
        SI_prefixes.update(SI_additional)

def RoundOff(number, digits=G.number_of_digits):
    '''Round the significand of number to the indicated number of digits
    and return the number suitably rounded (integers are returned
    untransformed).  The desire is to round things to get rid of
    trailing 0's and 9's:
 
        745.6998719999999  --> 745.699872
        4046.8726100000003 --> 4046.87261
        0.0254*12 = 0.30479999999999996 --> 0.3048
 
    so that printing a floating point representation is a bit easier
    to read.
    '''
    # Format the number to a string using scientific notation and pick off
    # the significand, which will be a string representing a number between
    # 1 and 10.  This is converted to a Decimal, which is then passed to
    # python's round() function.  The number is reconstituted with its
    # exponent using Decimal arithmetic, then returned as a float.
    if G.ii(number, int):
        return number
    if not G.ii(number, float):
        raise TypeError("number must be a float")
    if digits < 1:
        raise ValueError("digits must be an integer > 0")
    x, sign = abs(number), -1 if number < 0 else 1
    significand_str, exponent_str = "{:.16e}".format(x).split("e")
    significand_dec = Decimal(significand_str)
    significand = Decimal(str(round(significand_dec, digits - 1)))
    e = int(exponent_str)
    factor = sign*Decimal(10)**abs(e)
    if e < 0:
        return float(significand/factor)
    return float(significand*factor)

def to(x, s):
    '''Convenience function to convert a numerical value x to the unit
    expressed in the string s.
 
    Example:
        x = 22*u("m")       # x is 22 meters
        xmm = to(x, "km")   # xmm is 0.022 kilometers
    '''
    return x/u(s)

def fromto(x, s1, s2):
    '''Convenience function to convert a numerical value x in units s1
    to the unit expressed in the string s2.
 
    Example:
        x = fromto(1, "ft", "m")   # x will be 0.3048
    '''
    return x*u(s1)/u(s2)

def ParseUnit(s, allow_expr=False, allow_unc=False, allow_quit=True):
    '''Return (t, u) where t is a number string and u is a unit string.
    None will be returned if allow_expr is False and no number and unit
    could be found.  If allow_unc is true, then the number portion of the
    string can be an uncertainty expression usable by the uncertainties
    library and a unit, if present, must be separated from the uncertainty
    expression by one or more spaces.  allow_expr and allow_unc cannot both
    be True.
 
    The string s must be an integer or floating point number, followed by
    an optional string representing a unit.  The leading number is removed,
    leaving the unit.  These are returned as (number, unit), where both are
    strings (whitespace is stripped).  If there's no number, then None is
    returned instead of a tuple.  There doesn't need to be whitespace
    between the number and the unit.
 
    If s is "q" or "Q" and allow_quit is True, then the script will exit
    with status 0.
 
    The allow_expr keyword is used to facilitate a slightly different use
    case.  Here, the string s must be of the form "s u" where s is a python
    expression and u is a string designating a unit; the two are separated
    by one or more spaces.  The string u can be empty and the one or more
    space characters omitted, in which case the returned tuple will be
    (s, "").  Note this function doesn't evaluate the expression.
 
    If allow_unc is True, then the string s must be of the form "s u" where
    s is a string that can be evaluated by uncertainties.ufloat_fromstr()
    to produce a UFloat object and u is the optional unit string.  If no
    unit is present, then no space is necessary.  The returned form is
    (n, unit) where n is a UFloat type object and unit is a unit string or
    the empty string.  Note the use of allow_unc and the uncertainties
    library are optional (i.e., it's not a problem if the uncertainties
    library is not present unless you set allow_unc to True).
 
    Examples:
        ParseUnit("47.3e-88m/s") and ParseUnit("47.3e-88 m/s") both
        return ("47.3e-88", "m/s").
 
        ParseUnit("47.3e-88*1.23 m/s", allow_expr=True) returns 
        ("47.3e-88*1.23", "m/s").
 
        ParseUnit("4") returns ("4", "").
 
        Using the uncertainties library, the following all return the
        tuple (ufloat(4, 1), "m"):
            ParseUnit("4+-1 m", allow_unc=True)
            ParseUnit("4+/-1 m", allow_unc=True)
            ParseUnit("4(1) m", allow_unc=True)
            ParseUnit("4 m", allow_unc=True)
        ParseUnit("4+/-0 m", allow_unc=True) returns (ufloat(4, 0), "m").
    '''
    if s.lower() == "q" and allow_quit:
        exit(0)
    if allow_unc and not G.have_uncertainties:
        raise ValueError("uncertainties library not available")
    if allow_expr and allow_unc:
        raise ValueError("allow_expr and allow_unc cannot both be True")
    s = s.strip()
    if allow_expr:
        f = s.split(" ")
        if len(f) not in (1, 2):
            raise ValueError("s is not a proper string")
        if len(f) == 1:
            return (f[0], "")
        return tuple(f)
    else:
        # We allow the string "+-" to represent "+/-" (this is an
        # enhancement to the uncertainties package's syntax).
        s = s.replace("+-", "+/-")
        #is_unc = "+/-" in s or ("(" in s and ")" in s)
        f = s.split()
        if allow_unc:
            if len(f) not in (1, 2):
                raise ValueError("s is not a proper string")
            try:
                x = uncertainties.ufloat_fromstr(f[0])
            except Exception:
                raise ValueError("Cannot parse '{}'".format(f[0]))
            u = f[1] if len(f) == 2 else ""
            return (x, u)
        else:
            mo = G._num_unit.search(s)
            if mo:
                x, unit = s[:mo.end()].rstrip(), s[mo.end():].lstrip()
                return (x, unit)
            return None

def ParseFraction(s):
    '''Parse the number s and return it as (significand, unit, s) where
        significand = an int, float, or Fraction
        unit        = an optional unit string
        s           = the original string

    This function is intended to be used in programs where users might
    enter responses for a length such as '1/4 inches' or '0.25 inches'.

    Example: The fraction '9/8 mm' can be given as:
        9/8 mm
        18/16 mm
        1 1/8 mm
        1-1/8 mm
        1+1/8 mm
        1.1/8 mm
        str(9/8) + "mm"))
        str(9/8) + "    mm"))
    and after processing, (1.125, "mm", s) will be returned.
    '''
    Digits = set("1234567890")
    # Remove any unit
    unit = []
    for i in reversed(s):
        if i not in Digits:
            unit.append(i)
        else:
            break
    unit = ''.join(reversed(unit))
    num = s[:-len(unit)].strip() if unit else s.strip()
    unit = unit.strip()
    # Process number
    if "/" in num:
        try:
            num = num.replace(".", " ").replace("+", " ").replace("-", " ")
            if " " in num:
                i, f = num.split()
                significand = int(i) + Fraction(f)
            else:
                significand = Fraction(num)
        except Exception:
            raise ValueError(f"'{s}' is an invalid fraction")
    else:
        if "." in num or "e" in num.lower():
            try:
                significand = float(num)
            except Exception:
                raise ValueError(f"'{s}' is an invalid float")
        else:
            try:
                significand = int(num)
            except Exception:
                raise ValueError(f"'{s}' is an invalid integer")
    return (significand, unit, s)

def CT(T, T_from, T_to="K"):
    '''Convert temperature T in the unit indicated by the string
    T_from to the unit indicated by the string T_to.  The allowed
    strings for temperature are:
 
        K, k    Absolute temperature in kelvin
        C, c    Degrees Celsius
        F, f    Degrees Fahrenheit
        R, r    Degrees Rankine
    '''
    allowed, T0 = "kcfr", 273.15
    t_from, t_to, Tr = T_from.lower(), T_to.lower(), 9/5.*T0 - 32
    if len(t_from) != 1 or t_from not in allowed:
        raise ValueError("'%s' is a bad temperature unit" % T_from)
    if len(t_to) != 1 or t_to not in allowed:
        raise ValueError("'%s' is a bad temperature unit" % T_to)
    if t_from in "kr" and T < 0:
        raise ValueError("Absolute temperature must be >= 0")
    if t_from == "c" and T < -T0:
        raise ValueError("Temperature in deg C must be >= 273.15")
    if t_from == "r" and T < -Tr:
        raise ValueError("Temperature in deg F must be >= 491.67")
    f = {
        "kk" : lambda T: T,
        "kc" : lambda T: T - T0,
        "kf" : lambda T: 9./5*T - Tr,
        "kr" : lambda T: 9./5*T,
        "ck" : lambda T: T + T0,
        "cc" : lambda T: T,
        "cf" : lambda T: 9./5*T + 32,
        "cr" : lambda T: (T + T0)*9/5.,
        "fk" : lambda T: (T + Tr)*5/9.,
        "fc" : lambda T: (T - 32)*5/9.,
        "ff" : lambda T: T,
        "fr" : lambda T: T + Tr,
        "rk" : lambda T: 5/9*T,
        "rc" : lambda T: (T - Tr - 32)*5/9,
        "rf" : lambda T: T - Tr,
        "rr" : lambda T: T,
    }
    return f[t_from + t_to](T)

if 1:   # Utilities
    def NeedUncertainties():
        '''Print an error message the the uncertainties module is not
        present.
        '''
        if not G.have_uncertainties:
            print('''Error:  the uncertainties module is not available
            (see http://pythonhosted.org/uncertainties)''', file=sys.stderr)
            exit(1)

    def RemoveQuotes(s):
        '''For the string s, remove a leading and trailing quote pair if
        present.
        '''
        e = ValueError("Bad quoted string")
        if not s:
            return s
        elif s[0] == "'":
            if len(s) < 3 or s[-1] != "'":
                raise e
            return s[1:-1]
        elif s[0] == '"':
            if len(s) < 3 or s[-1] != '"':
                raise e
            return s[1:-1]
        else:
            return s

    def StrToNumber(s, allow_unc=False):
        '''Convert the string s to a number.  The number types allowed are:
        UFloat (if allow_unc is True), float, Fraction, and integer.
        '''
        if not s:
            raise ValueError("Argument cannot be empty string")
        if allow_unc and "+/-" in s:
            NeedUncertainties()
            return ufloat_fromstr(s)
        elif not allow_unc and "+/-" in s:
            raise ValueError("Uncertainties not allowed in s")
        elif "/" in s:
            return Fraction(s)
        elif "." in s or "e" in s.lower():
            return float(s)
        else:
            return int(s)

    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)

    def R(randomize=False):
        '''If randomize is False, return 1.  Otherwise, return a unique
        random float.
        '''
        if "numbers_used" not in dir(R):
            R.numbers_used = set()  # Keep track of random numbers used so far
        if randomize:
            udrn = lambda: 10**random.uniform(-1, 1)
            num = udrn()
            while not num or num in R.numbers_used:  # Not zero not allowed
                num = udrn()
            R.numbers_used.add(num)
            return num 
        else:
            return 1

def DefaultUnitData(level=-1, randomize=False, angles_have_dim=False):
    '''Returns a tuple of two sequences (DefaultUnits, BaseUnits) that
    define the default set of units and dimensions used by the module.
 
    DefaultUnits has the structure
    [
        ["dimension letters",
            [
               [level_number, string],
               ...,
            ]
        ],
    ]
    The typical string is of the form "unit_name = conversion_factor",
    which can be evaluated to define a conversion factor number with a
    unit_name symbol which is a valid python variable name.
 
    BaseUnits has the structure
    [
        unit_name_string : [conversion_factor, Dim_object],
        ...,
    ]
    Note the conversion factor may be a unique random number when
    randomization is True to aid in dimensional checking.  For normal use,
    the conversion factor is set to the integer 1.  The Dim_object
    encapsulates the physical dimensions of the base unit.
 
    Though this function produces the default set of units for the module,
    it is intended that you adapt or edit it to your personal needs.

    level
        Integer used to define the set of units to use.  0 is the lowest level; -1
        means include all units.  The higher the number, the more units that are
        included.
    '''
    DefaultUnits = [
        ["R" if angles_have_dim else "", [      # Angles
            # Form is [lvl, expression_string]; lvl is an integer used to
            # determine the level of that particular unit; if level <= lvl,
            # then the unit is included in the resulting set of units.
            # Setting level=0 in the call is intended to return a
            # bare-bones set of SI units.
            [0, "rad = 1.0"],
            [0, "deg = pi/180"],
            [1, "radian = rad"],
            [1, "rev = 2*pi*rad"],
            [1, "degree = deg"],
            [1, "arcmin = deg/60"],
            [1, "arcsec = deg/3600"],
            [2, "radians = rad"],
            [2, "revs = rev"],
            [2, "revolution = rev"],
            [2, "revolutions = rev"],
            [2, "circle = rev"],
            [2, "circles = rev"],
            [2, "turn = rev"],
            [2, "turns = rev"],
            [2, "degrees = deg"],
            [2, "arcminute = arcmin"],
            [2, "arcminutes = arcmin"],
            [2, "arcsecond = arcsec"],
            [2, "arcseconds = arcsec"],
            [2, "rightangle = pi/2*rad"],
            [2, "grad = rightangle/100"],
            [2, "gradian = grad"],
            [2, "gradians = grad"],
        ]],
        ["S" if angles_have_dim else "", [  # Solid angles
            [1, "sr = 1.0"],
            [1, "steradian = sr"],
            [2, "steradians = sr"],
            [2, "sphere = 4*pi*sr"],
            [2, "sd = deg**2"],
            [2, "squaredegree = sd"],
        ]],
        ["L", [     # Lengths
            [0, "inch = 0.0254*m"],
            [0, "ft = 12*inch"],
            [0, "mi = 5280*ft"],
            [1, "meter = m"],
            [1, "foot = 12*inch"],
            [1, "feet = 12*inch"],
            [1, "yd = 3*ft"],
            [1, "yard = yd"],
            [1, "mile = mi"],
            [1, "ly = 365.25*24*3600*c*m"],
            [1, "au = 149597870700*m"],
            [1, "earthradius = 6.37101e6*m"],
            [1, "moonradius  = 1.73710e6*m"],
            [1, "sunradius   = 6.96342e8*m"],
            [2, "metre = m"],
            [2, "meters = m"],
            [2, "metres = m"],
            [2, "inches = inch"],
            [2, "micron = 1e-6*m"],
            [2, "mil = inch/1000"],
            [2, "thou = mil"],
            [2, "yds = 3*ft"],
            [2, "yards = 3*ft"],
            [2, "miles = mi"],
            [2, "lightyear = ly"],
            [2, "astronomicalunit = au"],
            # Less frequently-used length units
            [2, "Angstrom = 1e-10*m"],
            [2, "ang = Angstrom"],
            [2, "angstrom = Angstrom"],
            [2, "nmi = 1852*m"],
            [2, "nmile = nmi"],
            [2, "nauticalmile = nmi"],
            [2, "nauticalmiles = nmi"],
            [2, "cable = nmi/10"],
            [2, "caliber = inch/100"],
            [2, "chain = 20.11684*m"],
            [2, "click = 1000*m"],
            [2, "clicks = click"],
            [2, "klick = click"],
            [2, "klicks = click"],
            [2, "fathom = 6*feet"],
            [2, "rod = 5.5*yard"],
            [2, "furlong = 40*rod"],
            [2, "furlongs = furlong"],
            [2, "hand = 4*inches"],
            [2, "hands = hand"],
            [2, "league = 3*miles"],   # About 1 hour's walk
            [2, "link = chain/100"],
            [2, "ls = c*m"],
            [2, "lightsecond = ls"],
            [2, "pace = 2.5*feet"],
            [2, "pc = 3.08567758149e+16*m"],
            [2, "parsec = 3.08567758149e+16*m"],
            [2, "pt = inch/72.27"],  # Other definition is inch/72
            [2, "point = pt"],
            # Railroad track width (4 ft 8.5 inches)
            [2, "standardgauge = 56.5*inches"],
            # US coin dimensions from
            # http://www.usmint.gov/about_the_mint/?action=coin_specifications
            [2, "dpenny = 0.75*inches"],
            [2, "dnickel = 0.835*inches"],
            [2, "ddime = 0.705*inches"],
            [2, "dquarter = 0.955*inches"],
            [2, "dhalf = 1.205*inches"],
        ]],
        ["L2", [    # Area
            [0, "acre = 4046.87260987425*m**2"],
            [1, "hectare = 1e4*m**2"],
            [1, "barn = 1e-28*m**2"],
            [2, "are = 100*m**2"],
            [2, "letter = 8.5*11*inch**2"],   # US paper size
            [2, "legal = 8.5*14*inch**2"],    # US paper size
            [2, "ledger = 11*17*inch**2"],    # US paper size
            [2, "A4paper = 0.21*0.297*m**2"],
            [2, "dollarbill = 2.61*6.14*inch**2"],
            [2, "circmil = pi*(1e-3*inch)**2/4"],
            [2, "mcm = 1000*circmil"],
            [2, "eartharea = 4*pi*earthradius**2"],
            [2, "moonarea = 4*pi*moonradius**2"],
            [2, "sunarea = 4*pi*sunradius**2"],
        ]],
        ["L3", [    # Volume
            [0, "l = 1e-3*m**3"],  # Note liter is not an SI unit
            [0, "gal = 231*inch**3"],
            [0, "cc = 1e-6*m**3"],
            [1, "L = l"],
            [1, "liter = l"],
            [1, "gallon = gal"],
            [1, "acrefoot = acre*foot"],
            [1, "qt = gal/4"],
            [1, "pt = qt/2"],
            [1, "floz = pt/16"],
            [1, "cup = 8*floz"],
            [2, "liters = L"],
            [2, "litre = L"],
            [2, "litres = L"],
            [2, "gallons = gal"],
            [2, "cuft = ft**3"],
            [2, "cubicfoot = cuft"],
            [2, "cubicfeet = cuft"],
            [2, "cuin = inch**3"],
            [2, "cubicinch = cuin"],
            [2, "cubicinches = cuin"],
            [2, "bbl = 42*gal"],
            [2, "barrel = bbl"],
            [2, "barrels = bbl"],
            [2, "bdft = 12*12*1*inch**3"],
            [2, "boardfoot = bdft"],
            [2, "boardfeet = bdft"],
            [2, "bushel = 35.2391*L"],
            [2, "bushels = bushel"],
            [2, "cord = 4*4*8*ft**3"],
            [2, "qts = qt"],
            [2, "quart = qt"],
            [2, "quarts = qt"],
            [2, "pts = pt"],
            [2, "pint = pt"],
            [2, "pints = pt"],
            [2, "fluidounce = floz"],
            [2, "cups = cup"],
            [2, "dixiecup = cup"],
            [2, "fldram = floz/8"],
            [2, "fifth = gal/5"],
            [2, "gill = pt/4"],
            [2, "hogshead = 63*gal"],
            [2, "jigger = 1.5*floz"],
            [2, "shot = jigger"],
            [2, "magnum = 1.5*L"],
            [2, "minim = fldram/60"],
            [2, "drop = (L/1000)/20"],  # 20 drops per ml
            [2, "bloodunit = 0.45*L"],
            [2, "number1can = 10*floz"],
            [2, "number2can = 19*floz"],
            [2, "number2point5can = 28*floz"],
            [2, "number3can = 32*cups"],
            [2, "number5can = 56*cups"],
            [2, "peck = bushel/4"],
            [2, "popcan = 12*floz"],
            [2, "beercan = popcan"],
            [2, "bigbeercan = 16*floz"],
            [2, "shippington = 40*ft**3"],
            [2, "tbs = cup/16"],
            [2, "tbl = tbs"],
            [2, "tbls = tbs"],
            [2, "tablespoon = tbs"],
            [2, "tsp = tbs/3"],
            [2, "teaspoon = tsp"],
            [2, "saltspoon = tsp/4"],
            [2, "winebottle = 3/4*L"],
            [2, "wineglass = 4*floz"],
        ]],
        ["T", [     # Time
            [0, "sec = s"],
            [0, "min = 60*s"],
            [0, "hr = 3600*s"],
            [0, "yr = 365.242198781*24*hr"],
            [1, "day = 24*hr"],
            [1, "mo = yr/12"],
            [1, "week = 7*day"],
            [2, "second = s"],
            [2, "seconds = s"],
            [2, "minute = min"],
            [2, "minutes = min"],
            [2, "hour = hr"],
            [2, "hours = hr"],
            [2, "days = day"],
            [2, "weeks = week"],
            [2, "wk = week"],
            [2, "year = yr"],
            [2, "years = yr"],
            [2, "julianyear = 365.25*days"],
            [2, "month = mo"],
            [2, "months = mo"],
            [2, "decade = 10*yr"],
            [2, "decades = 10*yr"],
            [2, "century = 100*yr"],
            [2, "centuries = 100*yr"],
            [2, "millenium = 1000*yr"],
            [2, "millenia = 1000*yr"],
            [2, "fortnight = 2*weeks"],
            [2, "lustrum = 5*yr"],
            [2, "jiffy = 0.01*s"],
            [2, "leapyear = 366*day"],
            # Astronomy (from GNU units 1.80 units.dat file; note the 2.02
            # version [current as of this writing] has more up-to-date
            # values).
            [2, "siderealday = 23.934469444*hour"],
            [2, "siderealyear = 365.256360417*day"],
            [2, "lunarmonth = 29.*day + 12.*hr + 44.*minutes + 2.8*s"],
            [2, "mercuryday = 58.6462*day"],
            [2, "venusday   = 243.01*day"],
            [2, "earthday   = siderealday"],
            [2, "marsday    = 1.02595675*day"],
            [2, "jupiterday = 0.41354*day"],
            [2, "saturnday  = 0.4375*day"],
            [2, "uranusday  = 0.65*day"],
            [2, "neptuneday = 0.768*day"],
            [2, "plutoday   = 6.3867*day"],
            [2, "mercuryyear = 0.2408467*julianyear"],
            [2, "venusyear   = 0.61519726*julianyear"],
            [2, "earthyear   = siderealyear"],
            [2, "marsyear    = 1.8808476*julianyear"],
            [2, "jupiteryear = 11.862615*julianyear"],
            [2, "saturnyear  = 29.447498*julianyear"],
            [2, "uranusyear  = 84.016846*julianyear"],
            [2, "neptuneyear = 164.79132*julianyear"],
            [2, "plutoyear   = 247.92065*julianyear"],
        ]],
        ["L1 T-1", [    # Velocity
            [0, "mph = mi/hr"],
            [1, "kph = 1000*m/hr"],
            [1, "fps = ft/s"],
            [1, "fpm = ft/min"],
            [1, "knot = 1852*m/hr"],
            [2, "light = c*m/s"],
        ]],
        ["T-1", [   # Frequency
            [0, "Hz = 1/s"],
            [1, "rpm = 1/min"],
            [2, "hertz = Hz"],
            [2, "rps = Hz"],
        ]],
        ["M", [     # Mass
            [0, "g = kg/1000"],
            [0, "lb = 0.45359237*kg"],
            [1, "electron_m = 9.109384e-31*kg"],
            [1, "gram = g"],
            [1, "grams = g"],
            [1, "pound = lb"],
            [1, "lbs = lb"],
            [1, "lbm = lb"],
            [1, "amu = 1.660538921e-27*kg"],
            [1, "oz = lb/16"],
            [1, "ton = 2000*lb"],
            [1, "tonne = 1000*kg"],
            [2, "gm = g"],
            [2, "gramme = g"],
            [2, "grammes = g"],
            [2, "pounds = lb"],
            [2, "slug = 14.593903*kg"],
            [2, "Da = amu"],
            [2, "ounce = oz"],
            [2, "ounces = oz"],
            [2, "grain = lb/7000"],
            [2, "grains = lb/7000"],
            [2, "gr = lb/7000"],
            [2, "cwt = 100*lb"],
            [2, "hundredweight = cwt"],
            [2, "nailkeg = cwt"],
            [2, "troypound = 5760.*grain"],
            [2, "troyounce = troypound/12"],
            [2, "dwt = troyounce/20"],
            [2, "pennyweight = dwt"],
            [2, "egg = 50*g"],
            [2, "ft3h2o = 28.2661*kg"],
            [2, "galH2O = 3.7855178*kg"],
            [2, "galh2o = galH2O"],
            [2, "galwater = galH2O"],
            [2, "gallonwater = galH2O"],
            [2, "carat = g/5"],
            [2, "ct = carat"],
            [2, "dram = ounce/16"],
            [2, "stone = 14*lb"],
            [2, "lbm = lb"],
            # US coin masses from
            # http://www.usmint.gov/about_the_mint/?action=coin_specifications
            [2, "mpenny = 2.5*g"],
            [2, "mnickel = 5*g"],
            [2, "mdime = 2.268*g"],
            [2, "mquarter = 5.670*g"],
            [2, "mhalf = 11.340*g"],
            # Astronomy (from GNU units 1.80 units.dat file; the 2.02 version
            # has more up-to-date values).
            [2, "sunmass = 1.9891e30*kg"],
            [2, "moonmass = 7.3483e22*kg"],
            [2, "mercurymass = 0.33022e24*kg"],
            [2, "venusmass = 4.8690e24*kg"],
            [2, "earthmass = 5.9742e24*kg"],
            [2, "marsmass = 0.64191e24*kg"],
            [2, "jupitermass = 1898.8e24*kg"],
            [2, "saturnmass = 568.5e24*kg"],
            [2, "uranusmass = 86.625e24*kg"],
            [2, "neptunemass = 102.78e24*kg"],
            [2, "plutomass = 0.015e24*kg"],
        ]],
        ["M L2 T-2", [  # Energy
            [0, "J = kg*m**2/s**2"],
            [0, "btu = 1055.056*J"],
            [1, "eV = 1.602176565e-19*J"],
            [1, "cal = 4.1868*J"],
            [1, "kcal = 1000*cal"],
            [1, "Whr = 3600*J"],
            [1, "Wh = Whr"],
            [2, "erg = 1e-7*J"],
            [2, "CAL = kcal"],
            [2, "Calorie = kcal"],
            [2, "calorie = cal"],
            [2, "therm = 1.054804e8*J"],  # Unit of natural gas energy
            [2, "BTU = btu"],
        ]],
        ["N", [     # Quantity
            [1, "mole = mol"],
            [1, "molar = mol/L"],
        ]],
        ["N-1", [    # Avogadro's number
            [0, "NA = 6.02214129e23/mol"],
        ]],
        ["M L T-2", [   # Force
            [0, "N = kg*m/s**2"],
            [0, "lbf = 4.4482216152605*N"],
            [1, "kgf = kg*gravity"],
            [1, "gf = g*gravity"],
            [1, "dyne = 1e-5*N"],
            [2, "poundf = lbf"],
            [2, "poundforce = lbf"],
            [2, "kip = 1000*lbf"],
            [2, "slugf = slug*gravity"],
            [2, "tonf = ton*gravity"],
        ]],
        ["M L-1 T-2", [     # Pressure
            [0, "Pa = N/m**2"],
            [0, "psi = lbf/inch**2"],
            [1, "atm = 101325*Pa"],
            [1, "bar = 1e5*Pa"],
            [1, "psf = lbf/ft**2"],
            [2, "torr = atm/760"],
            [2, "ksi = kip/inch**2"],
            [2, "water = g*gravity/(m/100)**3"],
            [2, "fth2o = ft*water"],
            [2, "inh2o = inch*water"],
            [2, "mh2o = m*water"],
            [2, "mmh2o = m*water/1000"],
            [2, "Hg = 13.5951*g*gravity/(m/100)**3"],
            [2, "ftHg = ft*Hg"],
            [2, "fthg = ft*Hg"],
            [2, "inHg = inch*Hg"],
            [2, "inhg = inch*Hg"],
            [2, "mHg = m*Hg"],
            [2, "mhg = m*Hg"],
            [2, "mmHg = m*Hg/1000"],
            [2, "mmhg = m*Hg/1000"],
        ]],
        ["M L-1 T-1", [     # Dynamic viscosity
            [1, "P = 0.1*Pa*s"],        # The poise is the cgs unit
            [1, "poise = 0.1*Pa*s"],
        ]],
        ["L2 T-1", [        # Kinematic viscosity = (dynamic viscosity)/density
            [1, "stoke = 1e-4*m**2/s"],
            [1, "stokes = 1e-4*m**2/s"],
        ]],
        ["L3 T-1", [    # Flow
            [1, "gph = gallon/hr"],
            [1, "gpm = gallon/min"],
            [1, "gps = gallon/s"],
            [1, "cfh = ft**3/hr"],
            [1, "cfm = ft**3/min"],
            [1, "cfs = ft**3/s"],
            [1, "lpm = liter/min"],
            [1, "lph = liter/hr"],
            [1, "lps = liter/s"],
            # Note the definition of a miner's inch is location-dependent
            [2, "minersinch = 0.566*lps"],  # For northwest US
        ]],
        ["M L2 T-3", [  # Power
            [0, "W = J/s"],
            [0, "hp = 550.*ft*lb*gravity/s"],
            [0, "HP = 550.*ft*lb*gravity/s"],
            [1, "metrichp = 735.49875*W"],
            [2, "tonref = ton*144.*btu/(lbm*day)"],
            [2, "tonrefrigeration = ton*144.*btu/(lbm*day)"],
            [2, "sccs = atm*cc/s"],         # Gas flow
            [2, "sccm = atm*cc/minute"],    # Gas flow
            [2, "scfh = atm*cfh"],          # Gas flow
            [2, "scfm = atm*cfm"],          # Gas flow
            [2, "slpm = atm*lpm"],          # Gas flow
            [2, "slph = atm*lph"],          # Gas flow
        ]],
        ["K", [     # Temperature
            [1, "degC = K"],
            [1, "degF = 5/9*K"],
        ]],
        ["A", [     # Current
            [1, "amp = A"],
            [1, "ampere = A"],
            [2, "abamp = 10*A"],
            [2, "abampere = abamp"],
            [2, "biot = abamp"],
        ]],
        ["A T", [   # Charge
            [0, "coul = A/s"],
            [0, "electron_q = 1.602176634e-19*coul"],
            [1, "Ahr = 3600*coul"],
            [2, "amphour = 3600*coul"],
            [2, "coulomb = coul"],
            [2, "C = coul"],
            [2, "abcoul = abamp/s"],
        ]],
        ["M L2 A-1 T-3", [  # Voltage
            [0, "V = J/coul"],
            [1, "volt = V"],
            [2, "abvolt = dyne*(m/100)/(abamp*s)"],
        ]],
        ["M L2 A-2 T-3", [  # Resistance
            # The capital omega symbol is added below if we're using python 3
            [0, "ohm = V/A"],
            [2, "abohm = abvolt/abamp"],
        ]],
        ["M-1 L-2 A2 T3", [     # Conductivity
            [1, "S = A/V"],
            [1, "siemens = S"],
            [2, "mho = A/V"],
            [2, "abmho = abamp/abvolt"],
        ]],
        ["M L2 A-1 T-2", [  # Magnetic flux
            [1, "Wb  = J/A"],
            [1, "Oe  = 1000/(4*pi)*A/m"],
            [1, "oersted  = 1000/(4*pi)*A/m"],
            [2, "Maxwell  = abvolt*s"],
            [2, "unitpole  = 4*pi*Maxwell"],
        ]],
        ["M A-1 T-2", [     # Magnetic flux density (magnetic induction)
            [1, "T = Wb/m**2"],
            [1, "Tesla = T"],
            [1, "tesla = T"],
            [1, "gauss = T/10000"],
        ]],
        ["M-1 L-2 A2 T4", [     # Capacitance
            [0, "F  = coul/V"],
            [2, "abfarad  = abamp*s/abvolt"],
        ]],
        ["M L2 A-2 T-2", [  # Inductance
            [0, "H  = m**2*kg/coul**2"],
            [2, "abhenry  = abvolt*s/abamp"],
        ]],
        ["C", [     # Luminous intensity
            [1, "candela = cd"],
            [2, "candle = 1.02*cd"],
        ]],
        # Luminous flux (note that since the steradian is dimensionless,
        # the lumen has the same dimensions as luminous intensity).
        ["C", [
            [1, "lm = cd*sr"],
            [2, "lumen = lm"],
        ]],
        ["L-2 C", [     # Illuminance (luminous flux per unit area)
            [1, "lux = lm/m**2"],
            [1, "footcandle = lm/ft**2"],
            [2, "phot = 1e4*lux"],
        ]],
        ["L-1", [   # Reciprocal focal length
            [2, "diopter = 1/m"],
        ]],
    ]
    # BaseUnits contains the base units with conversion factors of unity
    # unless randomization is on for dimensional checking.  Note they will
    # be an integer 1; derived units with conversion factors of unity will
    # have floating point 1.0.
    BaseUnits = [
        ["m",   [R(randomize=randomize), Dim("L")]],
        ["kg",  [R(randomize=randomize), Dim("M")]],
        ["s",   [R(randomize=randomize), Dim("T")]],
        ["A",   [R(randomize=randomize), Dim("A")]],
        ["cd",  [R(randomize=randomize), Dim("C")]],
        ["mol", [R(randomize=randomize), Dim("N")]],
        ["K",   [R(randomize=randomize), Dim("K")]],
    ]
    # Add the capital omega for resistance
    for i in DefaultUnits:
        if i[0] == "M L2 A-2 T-3":
            i[1].append([0, "\u03A9 = V/A"])
    return (DefaultUnits, BaseUnits)

def GetUnits(GetUnitData=DefaultUnitData, level=-1, show=False,
             randomize=False, angles_have_dim=False, check=False):
    '''Returns a tuple of two dictionaries (units, dimensions) defining
    different sets of SI and non-SI units.  GetUnitData is a function that
    returns a tuple of two sequences (unit_seq, base_units); unit_seq
    defines the derived units and base_units defines the base units.  See
    the defaults for their data structure.
 
    units is used to provide conversion factors to base SI units.  Note the
    base SI units will have integer values of 1; derived SI units like J
    (joules) will have floating point values of 1.0.  An example:
        units = {
            "unit_string" : x,
            # x is a floating point conversion factor to base SI units.
            # Example:  "mm" : 0.001 is the entry for millimeters.
        }
 
    dimensions is used to determine the physical dimensions associated with
    a defined unit.  An example:
        dimensions = {
            "unit_string" : D,
            # D is a Dim object defining the unit's physical dimensions.
            # Example:  "mm" : Dim("L").
        }
 
    level determines which unit definitions will be included (the integer
    with each dimension must be <= level.  Level 0 is intended to be a
    minimal set of dimensions that are commonly used.  Higher levels define
    less commonly-used units.  Set to -1 to include all unit definitions.
 
    If show is True, the resulting defined units are printed to stdout.
 
    If randomize is True, the base SI numbers are randomized; this is used
    in a numerical technique for finding dimensional errors in calculations.
 
    If angles_have_dim is True, then angles and solid angles are considered
    to be dimensional objects.  Normal SI usage is to consider them to be
    dimensionless because the radian is defined as the ratio of an arc
    length to a radius and the steradian is defined as the ratio of the
    area of a solid angle's projection on a sphere to the area of the whole
    sphere.  And remember that though a quantity may be dimensionless, it
    can still have a dimensionless unit associated with it, such as radians
    or degrees.
 
    If check is True, then consistency and syntactical checks are made on
    the resulting set of units.  It is recommended you set check to True
    until you've debugged a particular set of units; then set Check to
    False to remove some processing overhead.
    '''
    units_seq, base_units_seq = DefaultUnitData(
        level=level, randomize=randomize, angles_have_dim=angles_have_dim)
    # units will contain the unit name strings as keys; the value is
    # the conversion factor to the quantity in base SI units.
    units = {
        "c" : 299792458,        # Speed of light in m/s
        "gravity" : 9.80665,    # Standard acceleration of gravity in m/s**2
    }
    # Construct the dimensions dictionary, which relates the unit name
    # string to its Dim object.  Also store the base units' conversion
    # factors into the units dictionary.
    dimensions = {}
    for i in base_units_seq:
        un = i[0]
        value, dims = i[1]
        dimensions[un] = dims
        units[un] = value
    # Construct the dictionaries
    for dim, U in units_seq:
        for lvl, line in U:
            if level != -1 and lvl > level:
                continue
            D = Dim(dim)
            s = line.strip()
            # The line must be of the form "a = b"
            un, val = [i.strip() for i in s.split("=")]
            # Note the RoundOff() call will ensure the resulting conversion
            # factor is a float except for base units .
            t = un + " = RoundOff(float(" + val + "))"
            try:
                exec(t, globals(), units)
            except SyntaxError:
                Error("'{}' is not a valid unit symbol".format(un))
            dimensions[un] = D
    # Delete constants
    for i in ("c", "gravity", "water", "Hg"):
        if i in units:
            del units[i]
        if i in dimensions:
            del dimensions[i]
    if check:
        CheckUnitDict(units)
        # Verify the keys of units and dimensions are the same
        assert(set(units.keys()) == set(dimensions.keys()))
    # Print a units summary to stdout if show is True
    if show:
        print("Units level {}".format(level))
        print("Base units:")
        for name, dim in base_units_seq:
            print("  {} [{}]".format(name, dim[1]))
        keys = sorted(units.keys(), key=str.lower)
        print("Derived units:")
        for k in keys:
            print("  {} = {} [{}]".format(k, units[k], dimensions[k]))
    return (units, dimensions)

class Dim(object):
    '''This class captures the dimensions of a unit in terms of a set of
    allowed symbols.
    '''
    def __init__(self, s="", ignore_case=True,
                 allowed_symbols=tuple("M L T A K N C".split())):
        '''Initialize with a string s of e.g. the form 'L1 T-2', which
        means L/T**2, an acceleration.  Case of the symbols isn't important
        if ignore_case is True.  The allowed_symbols container has the
        symbols that are allowed to be used for dimensions.  The number 1
        is implied if there is no number after the symbol.
 
        The default symbol set is:
            L = length
            M = mass
            T = time
            A = current
            K = temperature
            N = amount of substance
            C = luminous intensity
        The order of the symbols determines the print order in __str__.
 
        Using the convenience U object later in this module, you can
        define Dim objects with fractional and floating point exponents.
        For example, u.dim("m^(3/2)/s")) returns Dim("L1.5 T-1").
        '''
        msg = "'{}' is an improper initializer".format(s)
        self._dims = {}
        self.number_types = (int, float, Fraction, Decimal)
        self.ignore_case = ignore_case
        self.allowed_symbols = allowed_symbols
        if ignore_case:
            self.allowed_symbols = tuple([i.upper() for i in allowed_symbols])
        for i in s.split():
            symbol, number = self._split(i)
            if number is None:
                msg = "'{}' is an improper dimension term".format(i)
                raise ValueError(msg)
            value = StrToNumber(number) if number else 1
            if symbol in self._dims:
                self._dims[symbol] += value
            else:
                self._dims[symbol] = value
    def _split(self, item):
        '''item is a string that contains a symbol and an optional trailing
        cuddled number with an optional sign.  Return the symbol and the
        number string.  Example:  "M4.0" returns ("M", "4.0").  The symbol
        must be in self.allowed_symbols.
        '''
        symbols = self.allowed_symbols[:]
        if self.ignore_case:
            symbols = [i.upper() for i in symbols]
            item = item.upper()
        for symbol in symbols:
            if item.startswith(symbol):
                return (symbol, item[len(symbol):])
        return (None, None)
    def _normalize(self):
        'Remove any dimensions with exponents of zero.'
        to_be_deleted = []
        for key in self._dims:
            if not self._dims[key]:
                to_be_deleted.append(key)
        for key in to_be_deleted:
            del self._dims[key]
    def __str__(self):
        '''Returns a string form of this instance.
        '''
        self._normalize()
        s = []
        for symbol in self.allowed_symbols:
            if symbol not in self._dims:
                continue
            if self._dims[symbol] != 1:
                s.append(symbol + str(self._dims[symbol]))
            else:
                s.append(symbol)
        return 'Dim("{}")'.format(' '.join(s))
    def __repr__(self):
        '''Same string representation as __str__.
        '''
        return str(self)
    def __hash__(self):
        '''Allows a Dim object to be used as a dictionary key (a Dim
        object is immutable).
        '''
        return hash(str(self))
    def __ne__(self, other):
        return not (self == other)
    def __eq__(self, other):
        '''Return True if this Dim object has the same dimensions as the
        other Dim object.
        '''
        if other is None:
            return False
        if not G.ii(other, Dim):
            raise TypeError("other must be a Dim object")
        if set(self._dims.keys()) != set(other._dims.keys()):
            return False
        # Check each dimensional component.  Compare as floats if one of
        # them is a float.
        s, o = self._dims, other._dims
        for key in self._dims:
            if G.ii(s[key], float) or G.ii(o[key], float):
                # Note we have to round things off or you'll get
                # unequal comparisons when things are nearly equal.
                a = RoundOff(float(s[key]))
                b = RoundOff(float(o[key]))
                if a != b:
                    return False
            else:
                if s[key] != o[key]:
                    return False
        return True
    def __pow__(self, other):
        '''Raise this Dim object to a power.  other must be an integer,
        float, Fraction, or string that can be converted to one of these
        number types.
        '''
        if not G.ii(other, (int, float, Fraction, str)):
            msg = "exponent must be a number or string"
            raise TypeError(msg)
        if G.ii(other, str):
            if "/" in other:
                exponent = Fraction(other)
            elif "." in other or "e" in other.lower():
                exponent = float(other)
            else:
                exponent = int(other)
        else:
            exponent = other
        if not other:
            return Dim("")
        d = self.dims
        for i in self._dims:
            d[i] *= exponent
        result = Dim("")
        result._dims = d
        result._normalize()
        return result
    @property
    def dims(self):
        '''Returns a copy of the object's dictionary relating the physical
        dimensions to their exponents.
        '''
        return self._dims.copy()
    def __add__(self, other):
        '''Addition of two Dim objects will result in a returned Dim
        object with the same dimensions.  If other is a number,
        then self must be Dim("") and a Dim("") instance is returned.
        '''
        if G.ii(other, self.number_types):
            if str(self) != 'Dim("")':
                m = "Must be dimensionless to add/subtrac a number"
                raise TypeError(m)
            return Dim("")
        else:
            if not G.ii(other, Dim):
                raise TypeError("other must be a Dim instance")
            if self._dims != other._dims:
                raise TypeError("Arguments must have identical dimensions")
            return self
    def __radd__(self, other):
        return self.__add__(other)
    def __sub__(self, other):
        return self.__add__(other)
    def __rsub__(self, other):
        return self.__add__(other)
    def __mul__(self, other):
        '''Multiplication of two Dim objects will result in a returned Dim
        object representing the combined dimensions.  If other is a number,
        then just return self.
        '''
        if G.ii(other, self.number_types):
            return self
        if not G.ii(other, Dim):
            raise TypeError("other must be a Dim instance")
        other._normalize()
        product_dims = self.dims
        for letter in other._dims:
            if letter in self._dims:
                product_dims[letter] += other._dims[letter]
            else:
                product_dims[letter] = other._dims[letter]
        result = Dim("")
        result._dims = product_dims
        result._normalize()
        return result
    def __rmul__(self, other):
        '''This method is needed to handle expressions like 1e-6*Dim("L").
        '''
        if G.ii(other, self.number_types):
            return self
        return self*other
    def __truediv__(self, other):
        '''Division of two Dim objects will result in a returned Dim object
        representing the combined dimensions.
        '''
        if G.ii(other, self.number_types):
            return self
        if not G.ii(other, Dim):
            raise TypeError("other must be a Dim instance")
        other._normalize()
        d = self._dims.copy()
        for letter in other.dims:
            if letter in self._dims:
                d[letter] -= other._dims[letter]
            else:
                d[letter] = -other._dims[letter]
        result = Dim("")
        result._dims = d
        result._normalize()
        return result
    def __rtruediv__(self, other):
        '''This method can handle the case of a number divided by a Dim
        object.  Note that other must be an integer or float.
        '''
        if not G.ii(other, self.number_types):
            raise TypeError("other must be an integer or float")
        return Dim("")/self
    def approx_equal(self, other, reltol=0.01):
        '''Compare the dimensions of two Dim objects like __eq__, but
        convert the exponents to floats and declare them equal if the
        relative tolerance is within reltol.  This can be useful when
        dimensionally comparing empirical equations.
        '''
        if other is None:
            return False
        if not G.ii(other, Dim):
            raise TypeError("other must be a Dim object")
        if set(self._dims.keys()) != set(other._dims.keys()):
            return False
        self._normalize()
        other._normalize()
        d1, d2 = self._dims, other._dims
        for key in self._dims:
            exp1, exp2 = float(d1[key]), float(d2[key])
            diff = abs(exp1 - exp2)
            reldiff = min(diff/exp1, diff/exp2)
            if reldiff > reltol:
                return False
        return True

class U(object):
    '''The U object provides an interface that can be used to calculate a
    conversion factor for an expression of units.  You instantiate a U
    object with its needed dictionaries:
 
        u = U(units, dimensions, prefixes, special)
 
    The instance u can be used for supported tasks associated with units
    and dimensions.  A common use case is to convert to base SI units;
    e.g., to convert miles per hour to m/s:
 
        v_in_m_per_s = v_in_mph*u("mph")
 
    This is a purely numerical conversion and contains no dimensional
    information.  Use the u.dim(expr) to get the Dim object associated with
    the unit expression expr (the Dim object captures the dimensional
    information of the expression).  You can also use u(expr, dim=True),
    which returns a tuple of the conversion factor and Dim object.
 
    See the __call__ method for a discussion of what the strict
    attribute controls.
 
    Use the digits attribute to control how many significant digits are
    returned from the __call__ method.  For example, when working with
    experimental data measured to around 0.1% uncertainties, you might want
    to limit digits to 3 or 4.
    '''
    def __init__(self, units, dimensions, prefixes={},
                 special={}, check=True):
        '''units is a dictionary whose keys are unit strings and values are
        the units' conversion factors to base units.  SI example:
            units = {"inch": 0.0254}
        converts inches to m.
 
        dimensions is a dictionary whose keys are unit strings and the
        values are Dim objects representing the physical dimensions of the
        unit string.  SI example:
            dimensions = {"inch": Dim("L")}
 
             **********************************************************
             *  units and dimensions are different dictionaries       * 
             *  because they are used as local variables for eval()   * 
             *  at two different times.  Otherwise, they would have   * 
             *  been combined into one dictionary.                    * 
             **********************************************************
 
        prefixes is a dictionary of allowed prefixes; the values are the
        strings that represent the value of each prefix.  Example:
            {"m": "1e-3", "milli": "1e-3", "milli-": "1e-3"}
 
        special, if not None, is a dictionary that is used to translate
        units that are python reserved words to suitable units that can be
        evaluated in expressions.  Example:
            {"in": "inches"}
 
        If check is True, perform some consistency and sanity checks on
        the incoming dictionaries.
        '''
        # Our dictionary attributes
        self._units = units
        self._dimensions = dimensions
        self._prefixes = prefixes
        self._special = special
        self._inv_dimensions = self._invert_dimensions()
        # Perform checks
        if check:
            # They incoming data must be dictionaries
            assert(G.ii(units, dict))
            assert(G.ii(dimensions, dict))
            assert(G.ii(prefixes, dict))
            assert(G.ii(special, dict))
            # units and dimensions must have the same size and keys
            assert(len(units) == len(dimensions))
            assert(set(units) == set(dimensions))
            # Check the dicts
            CheckUnitDict(units)
            CheckPrefixDict(prefixes)
            CheckDimDict(dimensions)
            for key, value in special:
                assert(G.ii(key, str))
                assert(G.ii(value, str))
        # Syntax shortcuts are allowed if self._strict is False
        self._strict = False
        # If units is empty, then insert the base units.
        if not units:
            self._units = {}
            for un, (value, dim) in self._dimensions:
                self._units[un] = value
        # Regular expressions for processing unit expression short-cuts
        self._spaces = re.compile(" +")       # One or more spaces
        self._ending_digits = re.compile(r"(\d+$)")  # Ends in > 0 digits
        self._default_digits = 16
        self._digits = self._default_digits
    def _invert_dimensions(self):
        '''Invert the dimensions to provide a way of looking up the unit
        strings associated with a particular dimensions.
        '''
        d = defaultdict(list)
        for unit in self._dimensions:
            dim = self._dimensions[unit]
            d[dim].append(unit)
        return d
    def find_unit(self, dim_object):
        '''Given a Dim object, return a list of the unit strings that
        have those dimensions or None if not found.
        '''
        return self._inv_dimensions.get(dim_object, None)
    def _set_strict(self, strict):
        self._strict = bool(strict)
    def _get_strict(self):
        return self._strict
    strict = property(_get_strict, _set_strict,
                      "Get/set the strict attribute (true ==> no "
                      "syntax shortcuts)")
    def _set_digits(self, digits):
        '''The digits attribute controls the number of significant
        figures shown in the string representation returned by str().
        digits must be None or an integer >= 0.  If digits is None or 0,
        then self.digits is set to the default value.
        '''
        if digits is None:
            self._digits = self._default_digits
        else:
            m = "digits must be an integer >= 0"
            if not G.ii(digits, int):
                raise TypeError(m)
            if digits < 0:
                raise ValueError(m)
            if digits:
                self._digits = digits
            else:
                self._digits = self._default_digits
    def _get_digits(self):
        return self._digits
    digits = property(_get_digits, _set_digits,
                      "Get/set the number of significant figures for the"
                      "output of __call__.)")
    def dim(self, expr, use_exc=False):
        '''Return the Dim object associated with the unit expression expr.
        If there is no unit associated with the expression or a conversion
        exception occurs, return None.  This method allows calling code to
        determine if an expression is a valid unit and get its associated
        Dim object for e.g. dimensional checking.  Two Dim objects can
        be compared for dimensional equality using '=='.
 
        If you'd rather have an exception when an invalid unit is
        encountered, set use_exc to True.
        '''
        if not G.ii(expr, str):
            raise TypeError("expr must be a string")
        if not expr:
            return Dim("")
        try:
            _, dim = self(expr, dim=True)
            if dim is None and use_exc:
                raise ValueError("'{}' is invalid dimension".format(expr))
            return dim
        except Exception:
            if use_exc:
                raise
            return None
    def _expand_units(self, expr, strict=False):
        '''This function provides the core unit expression evaluation
        capability.
        '''
        # The basic idea is to only let the dictionaries defining the
        # units contain unit strings that are valid python identifiers.
        # Then use python's parser via eval() using the units dictionary
        # as the local variables to result in a numerical expression.
        # When used with the dimensions dictionary, the same evaluation
        # results in a Dim expression.
        #
        # There are a few syntactical shortcuts for expr syntax, such as
        # implied exponentiation ("m2" meaning "m**2", allowing '^' for
        # '**', and letting a sequence of space characters represent a
        # multiplication.  These shortcuts are processed by using the
        # tokenize module to break the string expr into its tokens;
        # substitute as needed for the syntactical shortcuts, then
        # reassembling the components into the actual string to be
        # evaluated.  If strict is True, these shortcuts aren't allowed.
        _strict = bool(strict) if strict is not None else self._strict
        if not _strict:
            s = self._spaces.sub("*", expr)     # Multiple spaces --> '*'
        else:
            s = expr
        t, r = io.BytesIO(s.encode("utf-8")).readline, []
        dbg = False
        # Token numbers:
        #   tokenize.NAME     1
        #   tokenize.NUMBER   2
        #   tokenize.STRING   3
        #   tokenize.OP       52
        for toknum, string, _, _, _ in tokenize.tokenize(t):
            if dbg:
                print("Token = [{}] {}".format(toknum, string))
            if toknum == tokenize.NAME and string not in self._units:
                found_bare = False
                # Process as a unit expression
                mo, exponent = self._ending_digits.search(string), ""
                if mo is not None and not _strict:
                    # Ending number is implied exponentiation
                    exponent = "**" + str(int(string[mo.start():mo.end()]))
                    string = string[:mo.start()]
                # Replace special strings
                if string in self._special:  # e.g. "in" --> "inch"
                    string = self._special[string]
                if (string in self._prefixes and string not in
                        self._units and not _strict):
                    # Expand bare SI prefixes
                    string = "({})".format(self._prefixes[string])
                    found_bare = True
                else:
                    # Find SI prefix and replace with its value.
                    # An SI prefix has higher precedence than
                    # exponentiation.  Thus, 'mm2' means '(mm)**2', not
                    # 'm(m**2)'.
                    for p in self._prefixes:
                        if string.startswith(p):  # Has a prefix
                            remaining = string[len(p):]
                            if remaining == "kg":
                                msg = "Prefix not allowed with 'kg'"
                                raise ValueError(msg)
                            # Precedence is gotten by leaving off
                            # the trailing ')'
                            if remaining in self._units:
                                string = ("((" + self._prefixes[p] +
                                          "*" + remaining + ")")
                                break
                            elif remaining in self._special:
                                t = self._special[remaining]
                                string = ("((" + self._prefixes[p] +
                                          "*" + t + ")")
                                break
                if exponent:
                    string += exponent
                if not found_bare and string[0] == "(":
                    string += ")"
                if dbg:
                    print("  Changed:  {}".format(string))
            elif toknum == tokenize.STRING:  # Must be a number
                if ((string[0] == "'" and string[-1] == "'") or
                        (string[0] == '"' and string[-1] == '"')):
                    string = RemoveQuotes(string)
                    if "/" in string:
                        string = "Fraction(" + string + ")"
                    else:
                        pass  # int and float will evaluate as-is
            elif toknum == tokenize.OP:     # Change '^' to '**'
                if string == "^" and not _strict:
                    string = "**"
            # We need to disallow negative exponents such as 'm-1'
            # because arithmetic will be done with them by the parser.
            # This also disallows forms such as 'yocto-m'.
            if string == "-":
                raise ValueError("Negative signs or hyphens are not allowed")
            r.append((toknum, string))
        return tokenize.untokenize(r).decode("utf-8")
    def __call__(self, expr, strict=None, dim=False, digits=None):
        '''Returns a conversion factor to base units for the string
        expr, an expression in terms of unit strings.  The value will be
        rounded off to the U instance's digits attribute's number of
        significant figures.  If the keyword digits is a suitable
        integer, it is used instead, so that you don't have to change
        the instance attribute (it must be an integer or None).
        
        The current global context is used for evaluating the
        expression; the local context is all the units that have been
        defined (they must be valid python variable names).  An
        exception is raised if the call can't complete.
 
        expr can be a string of whitespace or empty, in which case 1 will
        be returned.
 
        If dim is True, then a tuple (factor, Dim_instance) is returned.
        factor is the conversion factor (a float) and Dim_instance is a Dim
        object representing the physical dimensions of expr.
 
        If strict is True, then only valid python expressions in the
        unit strings are allowed; the unit strings are regarded as
        variable names.  If strict is not True, then the following
        syntactical conveniences are allowed:
 
            - Sequences of one or more space characters in expr are
              converted to '*' characters (alternate multiplication
              syntax).  Example:  'J s' means joule*seconds.
            - '^' is equivalent to '**'
            - A unit string can have an appended integer, which is an
              implied exponent.  Example:  'm2' means square meters.
              Warning:  this only works for positive integers.
            - Bare SI prefixes can be used as numerical constants
              (excluding 'm'); implicit exponentiation works with them.
              Example:  'k2' means 1000**2 == 1e6.
 
        If strict is None (the default), then the current setting of the
        object's strict attribute are used.
 
        Fractions in an expression are indicated by a pair of single or
        double quotes; This e.g. allows fractional exponents and lets you
        use fractions of an inch (assume u is a U instance for SI units):
            print(u("m^'1/2'", dim=True))
            print(u("'7/16' inch"))
        outputs
            (1.0, Dim("L1/2"))
            0.011112499999999999
        showing that the physical dimensions are the square root of a
        length.
        '''
        assert expr is not None, "Bug in U.__call__:  expr is None"
        expression = self._expand_units(expr.strip(), strict=strict)
        exception = None
        try:
            if not expression.strip():
                value = 1
            else:
                value = eval(expression, globals(), self._units)
                s, ex = str(value), expression.strip()
                # The following are checks to see that things
                # like 'abs', 'int', 'quit', etc. aren't
                # recognized as proper units.
                if s.startswith("<built-in"):
                    raise Exception("'{}' is a built-in".format(ex))
                elif s.startswith("<function "):
                    raise Exception("'{}' is a function".format(ex))
                elif s.startswith("<class "):
                    raise Exception("'{}' is a class".format(ex))
                elif ex in globals():
                    raise Exception("'{}' is a global symbol".format(ex))
                elif ex == "quit":
                    raise Exception("'{}' is a command".format(ex))
        except NameError:
            msg = "'{}' is not a recognized dimensional unit"
            exception = ValueError(msg.format(expression.strip()))
        except Exception as e:
            exception = e
        if exception is not None:
            return (None, None) if dim else None
        # Get the number of digits to round to
        if digits is not None:
            m = "digits must be an integer"
            if not G.ii(digits, int):
                raise TypeError(m)
            if digits < 1:
                raise ValueError(m)
            value = RoundOff(value, digits)
        else:
            value = RoundOff(value, self._digits)
        # Get the Dim object
        if dim:
            try:
                dims = eval(expression, globals(), self._dimensions)
            except Exception:
                return (None, None)
            if G.ii(dims, (float, int, Fraction)):
                # Ensure we always return a Dim object (this exceptional
                # case can happen with exponents of zero).
                return (value, Dim(""))
            return (value, dims)
        else:
            if exception is not None:
                raise exception
        return value

def CheckPrefixDict(pdict):
    '''Perform checks on the udict dictionary with keys of unit names
    and values of strings that represent numbers.
    '''
    for i in pdict:
        try:
            # Value must be a string representing a number
            float(pdict[i])
        except ValueError:
            Error("'{}' is not a valid prefix value".format(pdict[i]))

def CheckUnitDict(udict, special=False):
    '''Perform checks on the udict dictionary with keys of unit names
    and values of numbers.  If special is True, don't check that the key
    is a valid variable name.
    '''
    for i in udict:
        # No unit name ends in a digit
        if i[-1] in set("0123456789"):
            msg = "Bug:  '{}' as a unit name may not end with a digit"
            raise SyntaxError(msg.format(i))
        if not special:
            # Unit names are valid python variable names (needed to be able
            # to use these dictionaries in eval() to evaluate arbitrary unit
            # expressions).
            try:
                eval(i, None, udict)
            except Exception:
                Error("'{}' is not a valid unit symbol".format(i))
    # udict's' values must be numbers
    assert(all([G.ii(i, (int, float)) for i in udict.values()]))

def CheckDimDict(ddict):
    '''Perform checks on the ddict dictionary with keys of unit names
    and values Dim objects.
    '''
    for i in ddict:
        # No unit name ends in a digit
        if i[-1] in set("0123456789"):
            msg = "Bug:  '{}' as a unit name may not end with a digit"
            raise SyntaxError(msg.format(i))
        # Unit names are valid python variable names (needed to be able
        # to use these dictionaries in eval() to evaluate arbitrary unit
        # expressions).
        try:
            eval(i, None, ddict)
        except Exception:
            Error("'{}' is not a valid unit symbol".format(i))
    # dimensions' values must be Dim instances
    assert(all([G.ii(i, Dim) for i in ddict.values()]))

def GetConvenienceUInstance():
    units, dims = GetUnits(check=False, show=False, level=2)
    return U(units, dims, SI_prefixes, {"in": "inches"}, check=True)

def dim(s):
    '''Returns a Dim object associated with a unit expression s.
    '''
    return u(s, dim=True)[1]

u = GetConvenienceUInstance()

def to(*p, **kw):
    '''Convenience function to let you use expressions like 
        x*to("ft/s")
    to convert the numerical variable x to have units of ft/s rather
    than
        x/u("ft/s")
    You can also use to(x, "ft/s").
    '''
    v = ValueError("Unrecognized unit string")
    try:
        if len(p) == 1:
            return 1/u(*p, **kw)
        elif len(p) == 2:
            return p[0]*1/u(p[1], **kw)
    except TypeError:
        raise v
    raise SyntaxError("'to' only takes 1 or 2 arguments")
        

if __name__ == "__main__":
    # Print out the supported units
    for i in range(3):
        GetUnits(level=i, check=True, show=True)
