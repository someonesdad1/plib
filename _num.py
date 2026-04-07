from __future__ import annotations
'''
Tue 7 Apr 2026 Tasks

- Get multiplication to work:  
    - Test case:
            x = Num("1", "ft")  # Is 0.3048 m
            y = Num("1", "m")   # Is 1 m
            x - y
            Should get Num("mpf('-0.69520000000000004')", "ft")
            but we're getting the negative of the correct answer, so there's a flip
            somewhere.
    - Num("2", "V")*Num("3.5", "A") -> Num("7", "(V)*(A)")
- Add nbs to string between number and unit
- Consider updating RoundOff to use mpf
- Need infection model for REPL
    - You can start off using int, float, complex, but as soon as one of these encounter
      a Num, a Num is always returned.  But the user has to type Num(x) to start the
      ball rolling.  The clue in the REPL is that the Num objects will always be
      colorized, but the python built-in types won't.  Thus, the REPL will behave like
      you're used to unless you deliberately use Num.
- Should Num have a .on attribute for colorizing?

'''
if 1:  # Header
    if 1:   # Standard imports
        import collections
        import decimal
        import enum
        import fcntl
        import fractions
        import getopt
        import operator
        import os
        import pathlib
        import re
        import string
        import subprocess
        import sys
        import threading
        import time
        import typing as ty
    if 1:   # Custom imports
        import columnize
        import dpstr
        import dpmath
        import dptypes
        import fmt
        import lwtest
        import mpmath
        import trm
        import uncertainties
        import wrap
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Core file gist information
        __gist__      = "Class to contain a general number"
        __copyright__ = "Copyright © 2026 Don Peterson"
        __license__   = "MIT License (see /plib/_lic.mit)"
        __test__      = "notest"
        __category__  = "math"
        __todo__      = '''These are ToDo items not to forget
            
            - Num.strict:  if on, uncertainties never compare equal.  If off, then if
              the mean and stdev match, they're equal with a warning to stderr:
              "Warning:  comparing distributions".
            - If Num.hashable is True, you might want the hash to be a tuple of the core
              values: hash((self.mytype, self.real, self.imag, self.unit)).  
            - Num.on?  Turns colorizing on/off
        
        '''
    if 1:   # Import symbols
        Path = pathlib.Path
        defaultdict = collections.defaultdict
        deque = collections.deque
        namedtuple = collections.namedtuple
        #
        Columnize = columnize.Columnize
        dedent = wrap.dedent
    if 1:   # Global variables
        t = trm.TrmDP()
        t.dbg = "#bdf6fe"
        g = dptypes.Constant()
        g.dbg = True if 0 else False
if 1:   # Types and enums
    class NumType(enum.IntEnum):
        Int = 1
        Rat = 2
        Flt = 3
        Cpx = 4
        Unc = 5
    NumericalTypes = ty.Union[
        int , float , complex , decimal.Decimal ,
        fractions.Fraction , mpmath.mpf , mpmath.mpc ,
        uncertainties.UFloat , "Num" , str , None]
if 1:   # Num class
        '''Represent a general number useful for routine calculations
        
            Warning:  The internal representation uses mpmath, so it's your responsibility
            as the user to ensure the mpmath context has sufficient resolution for your
            problems.
            
            The vision for this number class is for a "simple" view of the numerical
            universe in a python REPL (read-eval-print loop).  If you studied math as 
            e.g. an engineer/scientist in college, then you learned about some different
            number fields:  integers, rationals, reals, and complex numbers, the bedrock of
            practical math.  When doing calculations, we smoothly move between these fields
            as needed, converting things almost subconsciously, but it's harder for the
            computer stuff because these things (numbers) are usually types that often can't 
            unconsciously interact.  My vision for this Num class was to see if the
            following number types could be put into a logical single container:
                
                These "blackboard" symbols are used to denote the mathematical sets:
                    ℕ   Natural numbers:  the integers 1, 2, ...
                    ℤ   Positive and negative integers and zero
                    ℝ   Real numbers
                    ℂ   Complex numbers:  a pair of real numbers
            
                python's int, a representation of ℤ
                python's fractions.Fraction, a representation of ℚ
                python's float ℝ
                python's decimal.Decimal, another representation of ℝ
                python's complex ℂ
                mpmath's mpf, another representation of ℝ
                mpmath's mpc, another representation of ℂ
            
            Two other "types" needed to be addressed:
            
                - Because real-world practical problems include uncertainty, we need
                  some way to capture the notion of physical uncertainty in the numbers.
                  Python's uncertainties package is a good tool, but it lacks the
                  machinery to handle uncertainty in complex numbers, something I wanted
                  this Num class to handle.  If your first reaction is "that's not
                  needed", consider the output of an LCR meter: in general, you're given
                  back a complex impedance Z = ESR + X*i and the two real numbers can
                  have different (though perhaps correlated) uncertainty.  Though there
                  are other "number" types (vectors, matrices, quaternions, etc.) that
                  pop up in routine calculations, the Num type handles most of the
                  practical work.
            
                - Numbers based on physical measurement include units, which form their
                  own dimensional algebra and complicate things, as two real numbers x =
                  "3.4 m/s" and y = "6.7 A" are different types and have more
                  complicated arithmetic properties than "bare" numbers.  For example,
                  you cannot add x and y, but you're allowed to multiply them.
            
            Here's a very important practical notion of "logical" units.  We usually
            think of units as e.g. the familiar SI units.  However, almost all practical
            calculations involve some types of units.  For example, if you're measuring
            out pet food mass to feed some dogs and cats, you'd probably want the
            calculation to use the "units" kg_cat_food and kg_dog_food, assuming the
            dogs and cats get fed different foods.  This "unit orthogonality" helps
            keeps the animals fed properly, avoiding a mistake of mixing the foods,
            which might show up in a calculation as having units of
            kg_cat_food*kg_dog_food or a sum of 'kg_cat_food + kg_dog_food'.  The
            example isn't trivial -- if you're not convinced, look up the
            non-chump-change units mistake of the Mars Climate Orbiter, a loss of about
            half a billion 2026 dollars.  It's a shame the programming tools we have
            don't natively support both physical and logical units.  One of my goals in
            this Num class was providing a tool to do just this, because when the units
            in some arithmetical calculation aren't consistent, it's likely an error has
            been made.  Every scientist or engineer has learned to use such errors as
            red flags.
        
            Note for constructor
                # Note the user can supply a new unit string, changing the dimension
                # of value.  This is a deliberately allowed pattern:  the user needs
                # the number, but wants to change the unit "vector".
        '''

class Num:
    '''Represent a general number useful for routine calculations'''
    # Pick color based on number type
    type_color = {  # Match number types in dpdb.py for debugger
        NumType.Int: t("mag", "gry1"),
        NumType.Rat: t("brn", "gry1"),
        NumType.Flt: t("ygr", "gry1"),
        NumType.Cpx: t("sky", "gry1"),
        NumType.Unc: t("pur", "gry1"),
    }
    def __init__(self, value: ty.Optional[NumericalTypes] = None, unit: str = "") -> None:
        if 1:  # Default internal state representation
            self.numer: int = 0
            self.denom: int = 1
            self.real: mpmath.mpf = mpmath.mpf("0")
            self.imag: mpmath.mpf = mpmath.mpf("0")
            self.re_unc: mpmath.mpf = mpmath.mpf("0")
            self.im_unc: mpmath.mpf = mpmath.mpf("0")
            self.correl: mpmath.mpf = mpmath.mpf("0")
            self._unit = ""
            self.unit = unit  # Uses setter for stripping
            self.mytype: NumType = NumType.Int
            if value is None:
                return
        if 1:  # High-Precision Conversion Logic
            if isinstance(value, Num):  # Copy constructor
                self.numer = value.numer
                self.denom = value.denom
                self.real = value.real
                self.imag = value.imag
                self.re_unc = value.re_unc
                self.im_unc = value.im_unc
                self.unit = unit if unit else value.unit
                self.mytype = value.mytype
            elif isinstance(value, int):
                self.numer = int(value)
                self.mytype = NumType.Int
            elif isinstance(value, float):
                self.real = mpmath.mpf(repr(value))
                self.mytype = NumType.Flt
            elif isinstance(value, complex):
                self.real = mpmath.mpf(repr(value.real))
                self.imag = mpmath.mpf(repr(value.imag))
                self.mytype = NumType.Cpx
            elif isinstance(value, decimal.Decimal):
                self.real = mpmath.mpf(str(value))
                self.mytype = NumType.Flt
            elif isinstance(value, fractions.Fraction):
                self.numer = value.numerator
                self.denom = value.denominator
                self.mytype = NumType.Rat
            elif isinstance(value, mpmath.mpf):
                self.real = value
                self.mytype = NumType.Flt
            elif isinstance(value, mpmath.mpc):
                self.real = value.real
                self.imag = value.imag
                self.mytype = NumType.Cpx
            elif isinstance(value, uncertainties.UFloat):
                self.real = mpmath.mpf(str(value.nominal_value))
                self.re_unc = mpmath.mpf(str(value.std_dev))
                self.mytype = NumType.Unc
            elif isinstance(value, str):
                msg = f"{value!r} not recognized as a number"
                normalized = set(value.lower().replace("i", "j").strip())
                if "/" in normalized:
                    try:
                        self.numer, self.denom = [int(i) for i in value.split("/")]
                        self.mytype = NumType.Rat
                    except Exception as e: raise ValueError(msg) from e
                elif "j" in normalized:
                    re, im = dpmath.ParseComplex(value)
                    self.real = mpmath.mpf(re)
                    self.imag = mpmath.mpf(im)
                    self.mytype = NumType.Cpx
                elif "." in normalized or "e" in normalized:
                    try:
                        self.real = mpmath.mpf(value)
                        self.mytype = NumType.Flt
                    except Exception as e: raise ValueError(msg) from e
                else:
                    try:
                        self.numer = int(value)
                        self.mytype = NumType.Int
                    except Exception as e: raise ValueError(msg) from e
            else:
                raise TypeError(f"Type of {value!r} is not supported")
    def _binary_op(self, other: "Num", op_func: ty.Callable) -> "Num":
        target_type = max(self.mytype.value, other.mytype.value)
        if target_type <= NumType.Rat.value:
            return Num(op_func(self.as_int_or_rat, other.as_int_or_rat))
        if target_type == NumType.Unc.value:
            return self._do_uncertainty_math(other, op_func) # type: ignore
        # Real/Complex Promotion
        a = self.real if self.mytype >= NumType.Flt else self.as_mpf
        b = other.real if other.mytype >= NumType.Flt else other.as_mpf
        # If either is complex, use mpc to ensure mpmath handles it correctly
        if self.mytype == NumType.Cpx or other.mytype == NumType.Cpx:
            ac = mpmath.mpc(self.real, self.imag)
            bc = mpmath.mpc(other.real, other.imag)
            return Num(op_func(ac, bc))
        return Num(op_func(a, b))
    def _check_units(self, other: "Num") -> mpmath.mpf:
        '''Returns the multiplier to convert other.unit -> self.unit.'''
        if (not self.unit and not other.unit) or (self.unit == other.unit):
            return mpmath.mpf("1")
        arbiter = UnitArbiter()
        # We need: magnitude in other.unit * factor = magnitude in self.unit
        is_ok, factor_str = arbiter.check_conformable(other.unit, self.unit)
        if not is_ok:
            raise ValueError(f"Unit Mismatch: {self.unit} vs {other.unit}")
        return mpmath.mpf(factor_str)
    def _normalize(self, other: "Num") -> "Num":
        '''Returns a copy of other scaled to self.unit.'''
        factor = self._check_units(other)
        if factor == 1:
            return Num(other)
        adjusted = Num(other)
        if adjusted.mytype <= NumType.Rat:
            adjusted.real = adjusted.as_mpf * factor
            adjusted.mytype = NumType.Flt
        else:
            adjusted.real = adjusted.real * factor
            adjusted.imag = adjusted.imag * factor
        adjusted.unit = self.unit
        return adjusted
    # Arithmetic Methods
    def __add__(self, other: ty.Any) -> "Num":
        other_num = Num(other)
        adj = self._normalize(other_num)
        res = self._binary_op(adj, operator.add)
        res.unit = self.unit
        return res
    def __sub__(self, other: ty.Any) -> "Num":
        other_num = Num(other)
        adj = self._normalize(other_num)
        res = self._binary_op(adj, operator.sub)
        res.unit = self.unit
        return res
    def __mul__(self, other: ty.Any) -> "Num":
        other_num = Num(other)
        res = self._binary_op(other_num, operator.mul)
        if not self.unit and not other_num.unit: res.unit = ""
        elif self.unit and not other_num.unit: res.unit = self.unit
        elif not self.unit and other_num.unit: res.unit = other_num.unit
        else: res.unit = f"({self.unit})*({other_num.unit})"
        return res
    def __rmul__(self, other: ty.Any) -> "Num":
        return self.__mul__(other)
    def __truediv__(self, other: ty.Any) -> "Num":
        other_num = Num(other)
        if other_num.as_mpf == 0: raise ZeroDivisionError("Tractor at 0 divisor.")
        res = self._binary_op(other_num, operator.truediv)
        if not self.unit and not other_num.unit: res.unit = ""
        elif self.unit and not other_num.unit: res.unit = self.unit
        elif not self.unit and other_num.unit: res.unit = f"1/({other_num.unit})"
        else: res.unit = f"({self.unit})/({other_num.unit})"
        return res
    def __rtruediv__(self, other: ty.Any) -> "Num":
        return Num(other) / self
    def __eq__(self, other: ty.Any) -> bool:
        other_num = Num(other)
        if self.unit != other_num.unit: return False
        target_type = max(self.mytype.value, other_num.mytype.value)
        if target_type <= NumType.Rat.value:
            return self.as_int_or_rat == other_num.as_int_or_rat
        return bool(self.as_mpf == other_num.as_mpf)
    if 1:   # String interpolation
        def __str__(self) -> str:
            if self.mytype == NumType.Int: s = fmt.fmt(self.numer)
            elif self.mytype == NumType.Rat: s = fmt.fmt(fractions.Fraction(self.numer, self.denom))
            elif self.mytype == NumType.Cpx: s = fmt.fmt(mpmath.mpc(self.real, self.imag))
            elif self.mytype == NumType.Unc: s = f"{self.real} ± {self.re_unc}"
            else: s = fmt.fmt(self.real)
            unit_str = f" {t.whtl}{self.unit}{t.n}" if self.unit else ""
            color = Num.type_color.get(self.mytype, t.wht)
            return f"{color}{s}{t.n}{unit_str}"
        def __repr__(self) -> str:
            if self.mytype == NumType.Int: s = str(self.numer)
            elif self.mytype == NumType.Rat: s = f"{self.numer}/{self.denom}"
            elif self.mytype == NumType.Cpx: s = f"{self.real!r}+{self.imag!r}j"
            elif self.mytype == NumType.Unc: s = f"{self.real} ± {self.re_unc}"
            else: s = f"{self.real!r}"
            return f'Num("{s}", "{self.unit}")'
    if 1:   # Properties
        @property
        def unit(self) -> str:
            return self._unit.strip()
        @unit.setter
        def unit(self, value: str) -> None:
            self._unit = value.strip() if value else ""
        @property
        def as_mpf(self) -> mpmath.mpf:
            if self.mytype == NumType.Int: return mpmath.mpf(str(self.numer))
            if self.mytype == NumType.Rat: return mpmath.mpf(self.numer)/mpmath.mpf(self.denom)
            return self.real
        @property
        def as_int_or_rat(self) -> ty.Union[int, fractions.Fraction]:
            if self.mytype == NumType.Int: return self.numer
            return fractions.Fraction(self.numer, self.denom)

if 1:   # UnitArbiter class
    class UnitArbiter:  # A singleton with a lock
        _instance: ty.Optional['UnitArbiter'] = None
        _lock = threading.Lock()
        def __new__(cls):
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(UnitArbiter, cls).__new__(cls)
                    cls._instance._init_arbiter()
            return cls._instance
        def _init_arbiter(self):
            self.path = os.path.expanduser("~/.units_dynamic")
            if not os.path.exists(self.path):
                open(self.path, 'a').close()
            self.proc = None
            self._start_process()
        def _start_process(self):
            if self.proc:
                self.proc.terminate()
            # -q: quiet
            # -f: load our dynamic file
            cmd = ['units', '-q', '-f', '/home/don/.0rc/bin/definitions.units', '-f', self.path]
            Dbg(f"Starting 'units' process with command\n  {cmd}")
            self.proc = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1 # Line buffered
            )
        def add_primitive(self, unit_name: str) -> None:
            '''Inject a new primitive into the dynamic units file.'''
            if not unit_name:
                return
            with self._lock:
                # Open for appending and reading
                with open(self.path, "a+") as f:
                    try:
                        # Exclusive lock (blocks until available)
                        fcntl.flock(f, fcntl.LOCK_EX)
                        f.seek(0)
                        content = f.read()
                        # Only add if it's truly new
                        if unit_name not in content:
                            # GNU Units syntax for a primitive
                            f.write(f"{unit_name}\tprimitive\n")
                            f.flush()
                            # We must restart the process to pick up the new file state
                            self._start_process()
                    finally:
                        # Always release the lock
                        fcntl.flock(f, fcntl.LOCK_UN)
        def check_conformable(self, have: str, want: str) -> ty.Tuple[bool, str]:
            '''Returns (is_match, multiplier_string)'''
            with self._lock:
                try:
                    Dbg(f"check_conformable:  have = {have}, want = {want}")
                    if not have or not want:
                        return False, "0"
                    query = f"{have}\n{want}\n"
                    Dbg(f"  query = {query!r}")
                    self.proc.stdin.write(query)
                    self.proc.stdin.flush()
                    # GNU Units output: line 1 is reciprocal, line 2 is the factor
                    line_1 = self.proc.stdout.readline().strip()
                    if not line_1 or "conformable" in line_1 or "error" in line_1:
                        Dbg("  error in units call")
                        return False, "0"
                    line_2 = self.proc.stdout.readline().strip()
                    Dbg(f"  line_1 = {line_1!r}")
                    Dbg(f"  line_2 = {line_2!r}")
                    # Extract just the numeric part of the factor
                    # e.g., "* 0.3048" -> "0.3048"
                    factor_str = line_1.split()[-1]
                    Dbg(f"  returning True, factor_str = {factor_str!r}")
                    return True, factor_str
                except Exception as e:
                    Dbg(f"Restarting 'units' process: {e!r}", color="yel")
                    self._start_process()
                    return False, "0"

if __name__ == "__main__":  
    if 1:   # Standard imports
        pass
    if 1:   # Custom imports
        pass
    if 1:   # Import symbols
        run = lwtest.run
        raises = lwtest.raises
        Assert = lwtest.Assert
    if 1:   # Utility stuff for a script
        def GetScreen():
            'Return (LINES, COLUMNS)'
            return (
                int(os.environ.get("LINES", "50")),
                int(os.environ.get("COLUMNS", "80")) - 1,
            )
        def GetColors():
            t.dbg = "lil"
            t.err = "redl"
        def Dbg(*p, **kw):
            if not hasattr(Dbg, "file"):
                Dbg.file = sys.stdout
            if g.dbg:
                if "color" in kw:
                    print(f"{t(kw['color'])}", end="", file=Dbg.file)
                    del kw["color"]
                else:
                    print(f"{t.dbg}", end="", file=Dbg.file)
                k = kw.copy()
                k["file"] = Dbg.file
                print(*p, **k)
                print(f"{t.n}", end="", file=Dbg.file)
        def Warn(*msg, **kw):
            print(*msg, file=sys.stderr)
        def Error(*msg, status=1):
            Warn(f"{t.err}", end="")
            Warn(*msg)
            Warn(f"{t.n}")
            exit(status)
        def Usage(status=1):
            print(dedent(f'''
            Usage:  {sys.argv[0]} [options] [arg1 [arg2...]]
            Describe behavior
            Options:
                -a      Describe
                -d n    Number of significant digits
                -h      Print help
            '''))
            exit(status)
        def ParseCommandLine(d):
            d["-a"] = False  # Description
            d["-d"] = 3      # Description
            try:
                opts, args = getopt.getopt(sys.argv[1:], "ad:h")
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o[1] in list("a"):
                    d[o] = not d[o]
                elif o == "-d":
                    try:
                        d[o] = int(a)
                        if not (1 <= d[o] <= 15):
                            raise ValueError()
                    except Exception:
                        Error(f"{o!r} option must be an int between 1 and 15")
                elif o == "-h":
                    Usage(status=0)
            GetColors()
            g.W, g.L = GetScreen()
            return args
    if 0:
        d = {}  # Options dictionary
        args = ParseCommandLine(d)
        if args:
            for arg in args:
                pass    # Do stuff
    else:   # Demo & tests for module
        zero = mpmath.mpf(0)
        def Demo():
            pass
        def Test_Constructor_With_Numbers():
            if 1:   # No input
                num = Num()
                Assert(num.real == 0 and num.imag == 0)
                Assert(num.mytype == NumType.Int)
            if 1:   # int
                if 1:   # Positive
                    x, T = 30957357, NumType.Int
                    num = Num(x)
                    Assert(num.numer == x and num.denom == 1)
                    Assert(num.mytype == T)
                    # As string
                    num = Num(str(x))
                    Assert(num.numer == x and num.denom == 1)
                    Assert(num.mytype == T)
                if 1:   # Negative
                    x, T = -30957357, NumType.Int
                    num = Num(x)
                    Assert(num.numer == x and num.denom == 1)
                    Assert(num.mytype == T)
                    # As string
                    num = Num(str(x))
                    Assert(num.numer == x and num.denom == 1)
                    Assert(num.mytype == T)
            if 1:   # float
                x, T = 3095.7357, NumType.Flt
                num = Num(x)
                Assert(num.real == x and num.imag == 0)
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num.real == -x and num.imag == 0)
                Assert(num.mytype == T)
            if 1:   # Decimal
                s = "3095.7357"
                x, T = decimal.Decimal(s), NumType.Flt
                num = Num(x)
                Assert(num.real == mpmath.mpf(s) and num.imag == zero)
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num.real == -x and num.imag == zero)
                Assert(num.mytype == T)
            if 1:   # mpmath.mpf
                s, T = "3095.7357", NumType.Flt
                x = mpmath.mpf(s)
                num = Num(x)
                Assert(num.real == x and num.imag == zero)
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num.real == -x and num.imag == zero)
                Assert(num.mytype == T)
            if 1:   # Complex
                x, T = -1+3j, NumType.Cpx
                num = Num(x)
                Assert(num.real == mpmath.mpf(-1) and num.imag == mpmath.mpf(3))
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num.real == mpmath.mpf(1) and num.imag == mpmath.mpf(-3))
                Assert(num.mytype == T)
            if 1:   # mpmath.mpc
                x, T = mpmath.mpc(-1, 3), NumType.Cpx
                num = Num(x)
                Assert(num.real == mpmath.mpf(-1) and num.imag == mpmath.mpf(3))
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num.real == mpmath.mpf(1) and num.imag == mpmath.mpf(-3))
                Assert(num.mytype == T)
            if 1:   # Rational
                pass
            if 1:   # Unc
                pass
        def Test_Constructor_Strings():
            test_cases = [("1", NumType.Int),
                          ("1/2", NumType.Rat),
                          ("1.2", NumType.Flt),
                          ("1.2e3", NumType.Flt),
                          ("1+2j", NumType.Cpx)]
            for s, typ in test_cases:
                x = Num(s)
                Assert(x.mytype == typ, got=typ, expected=x.mytype)
                # Check numerical value
                if s == "1":
                    Assert(x.numer == 1 and x.denom == 1)
                elif s == "1/2":
                    Assert(x.numer == 1 and x.denom == 2)
                elif s == "1.2":
                    Assert(x.real == mpmath.mpf("1.2") and x.imag == zero)
                elif s == "1.2e3":
                    Assert(x.real == mpmath.mpf("1.2e3") and x.imag == zero)
                elif s == "1+2j":
                    Assert(x.real == mpmath.mpf("1") and x.imag == mpmath.mpf("2"))
        def Test_Arithmetic():
            if 1:   # Test addition
                x = Num("1", "ft")
                y = Num("1", "m")
                result = x + y
                expected = "4.2808399000000001"
                Assert(result.real == mpmath.mpf(expected))
                Assert(result == Num(expected, "ft"))
            if 1:   # Test subtraction
                x = Num("1", "ft")
                y = Num("1", "m")
                result = x - y
                expected = "-2.2808399000000001"
                Assert(result.real == mpmath.mpf(expected))
                Assert(result == Num(expected, "ft"))
            if 1:   # Test multiplication
                x = Num("1.5", "V")
                y = Num("2.0", "A")
                result = x*y
                expected = "3.0"
                Assert(result.real == mpmath.mpf(expected))
                Assert(result == Num(expected, "(V)*(A)"))
            if 1:   # Test division
                x = Num("1.0", "ft")
                y = Num("1", "m")
                result = x/y
                expected = "1.0"
                Assert(result.real == mpmath.mpf(expected))
                Assert(result == Num(expected, "(ft)/(m)"))
        if 0:   # Special one-off test area
            # Problem with subtraction
            x = Num("1.0", "ft")  # Is 0.3048 m
            y = Num("1", "m")   # Is 1 m
            # So 0.3048 - 1 is -0.6952 m, which is -2.28083989501312 ft by GNU units
            result = x - y
            print(f"result = {result!s}")
            expected = "-2.28083989501312"
            exit()
            
        if len(sys.argv) > 1:
            Demo()
        else:
            exit(run(globals(), regexp=r"^Test_", halt=1, verbose=0)[0])
