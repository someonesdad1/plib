'''
Thoughts on refactoring f.py
    - /plib/f.py is a core module that includes flt(float) and cpx(complex).  These
      derived classes carry some extra state and the intention of the initial design was
      that these numbers would interpolate to strings with a user-specified number of
      significant figures.  A cpx inherits from complex; internally its implementation
      uses two flt instances.
    - Another core feature of these two number types is their infection model, meaning
      all typical calculations with them should ultimately wind up being flt or cpx
      instances.  This is useful e.g. for general calculations in a REPL.  
    - One of the reasons for refactoring and streamlining /plib/fmt.py is to be able to
      separate the string interpolation from the mathematical model (in the sense of the
      model-view-controller software pattern).  This will remove a goodly amount of code
      from the f.py file.
    - A primary use case of the f.py module is the N attribute of flt (it's actually in
      a Base class that both flt and cpx derive from too).  This controls the number of
      digits show in string interpolation for all flt and cpx instances.  This is useful
      because usually the user (e.g., me) has a pretty good idea of the needs of the
      problem and can set this value to a suitable number, avoiding numerical noise.
      The small n attribute is used for individual flt and cpx instances and is local to
      each, covering the use case for a specific number that's different than the rest.
      For example, the main set of numbers might have come from distance measurements
      with a tape measure, so N == 3 is suitable.  An associated voltage measurement
      from a 5 digit voltmeter would have its n set to 5.  Of course, there is no
      implied uncertainties in any of these settings.

General number implementation
    - An annoyance with numbers for calculations is that there are so many of them: int,
      float, complex, Fraction, Decimal, ufloat, mpf, mpc, etc.
    - Is it possible to define one type of number: Num?  Of course, this Num object will
      have to know about these different implementations internally, but its objective
      is to present a unified view to the user.
        - It would have different shorthand methods to convert it to a specific type:
            - i for int                     sky
            - f for float                   whtl
            - r for rational (fraction)     purl
            - c for complex                 pnkl
            - u for ufloat                  lip
        - But behind the scenes it could e.g. be an mpc, utilizing the components as
          needed.  For example, if it was a ufloat, then the real part can hold the
          nominal value and the imaginary part can hold the uncertaint.
    - In the terminal or a REPL, realtime calculations with these numbers would display
      their type by their color
    - Since most numbers come from strings in programs, the following algorithm would be
      used to "promote" a string to the proper type:
        - int:  "0x 0b 0o 0d" as prefix, leading + or -, digits or int(a, b)
            - Could support other bases later as needed
        - float:  contains "." or "e" or both or 'float(a)'
        - rational:  contains "/" or 'Fraction(a, b)'
        - complex:  contains i or j or 'complex(a, b)'
        - ufloat:  contains ± or "(" and ")"
    - Would need to support infection model
        - int -> rational -> float -> complex
    - Another view of uncertainty:
        - All uncertain numbers are either float or complex
    - The general number would need two integers and two mpmath.mpc numbers 
    - A demo of the capabilities would be to construct a REPL that uses fmt.py for
      formatting and trm.py for colorizing.  This would be a tool that would remember
      its history and state, letting you pick up the calculation later.
    - The overall use case would be manual calculation in a REPL, not high speed
      computations for scientific computing.  In essence, it would be the modern
      terminal replacement of a typical scientific calculator.
        
'''
if 1:  # Header
    if 1:   # Standard imports
        import collections
        import decimal
        import enum
        import fractions
        import getopt
        import os
        import pathlib
        import re
        import string
        import sys
    if 1:   # Custom imports
        import columnize
        import dpstr
        import dpmath
        import dptypes
        import f
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
        __todo__      = '''
            
            -

        '''
    if 1:   # Import symbols
        Path = pathlib.Path
        defaultdict = collections.defaultdict
        deque = collections.deque
        namedtuple = collections.namedtuple
        #
        Columnize = columnize.Columnize
        dedent = wrap.dedent
        flt = f.flt
    if 1:   # Global variables
        t = trm.Trm()
        g = dptypes.Constant()
        g.dbg = False
if 1:   # Utility
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
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.n}", end="", file=Dbg.file)
    def Warning(*msg, **kw):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warning(f"{t.err}", end="")
        Warning(*msg)
        Warning(f"{t.n}")
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
if 1:   # Classes

    NumType = enum.Enum("NumType", ("tUnknown", "tInt", "tFloat", "fFlt", "tComplex",
        "tCpx", "tDecimal", "tRational", "tMpf", "tMpc", "tUnc"))
    class Num:
        '''Represent a general number useful for routine calculations

        The internal representation uses mpmath, so it's your responsibility as the
        user to ensure the mpmath context has sufficient resolution for your problems.
        '''
        def __init__(self, value: str|None = None) -> None:
            if 1:   # Default internal state representation
                self.numer: int = 0
                self.denom: int = 0
                # The imaginary parts of real and image are used to represent uncertainty as a
                # standard deviation
                self.real: mpmath.mpc = mpmath.mpc("0")
                self.imag: mpmath.mpc = mpmath.mpc("0")
                self.mytype: NumType = NumType.tInt
                if value is None:
                    return
            if 1:   # Convert value to our internal representation
                if isinstance(value, int):
                    self.numer = int(value)
                    self.mytype = NumType.tInt
                elif isinstance(value, float):
                    self.real = mpmath.mpc(repr(value), 0)
                    self.mytype = NumType.tFloat
                elif isinstance(value, f.flt):
                    self.real = mpmath.mpc(repr(float(value)), 0)
                    self.mytype = NumType.tFloat
                elif isinstance(value, complex):
                    self.real = mpmath.mpc(repr(value.real), 0)
                    self.imag = mpmath.mpc(repr(value.imag), 0)
                    self.mytype = NumType.tComplex
                elif isinstance(value, f.cpx):
                    self.real = mpmath.mpc(repr(float(value.real)), 0)
                    self.imag = mpmath.mpc(repr(float(value.imag)), 0)
                    self.mytype = NumType.tComplex
                elif isinstance(value, decimal.Decimal):
                    self.real = mpmath.mpc(str(value), 0)
                    self.mytype = NumType.tFloat
                elif isinstance(value, fractions.Fraction):
                    self.numer = value.numerator
                    self.denom = value.denominator
                    self.mytype = NumType.tRational
                elif isinstance(value, mpmath.mpf):
                    self.real = mpmath.mpc(value, 0)
                    self.mytype = NumType.tMpf
                elif isinstance(value, mpmath.mpc):
                    self.real = mpmath.mpc(value.real, 0)
                    self.imag = mpmath.mpc(value.imag, 0)
                    self.mytype = NumType.tMpc
                elif isinstance(value, uncertainties.UFloat):
                    self.real = mpmath.mpc(value.nominal_value, value.std_dev)
                    self.mytype = NumType.tUnc
                elif isinstance(value, str):
                    msg = f"{value!r} not recognized as a number"
                    chars = set(value.lower().strip())
                    if "/" in chars:    # Assume it's a rational number
                        try:
                            self.numer, self.denom = [int(i) for i in value.split("/")]
                            self.mytype = NumType.tRational
                        except Exception as e:
                            raise ValueError(msg) from e
                    elif "j" in chars or "i" in chars:  # Assume it's complex
                        re, im = dpmath.ParseComplex(value)
                        self.real = mpmath.mpc(re, 0)
                        self.imag = mpmath.mpc(im, 0)
                        self.mytype = NumType.tComplex
                    elif "." in chars or "e" in chars:  # Assume it's floating point
                        try:
                            self.real = mpmath.mpc(mpmath.mpf(value), 0)
                            self.mytype = NumType.tFloat
                        except Exception as e:
                            raise ValueError(msg) from e
                    else:   # Assume it's an integer
                        try:
                            self.numer = int(value)
                            self.mytype = NumType.tInt
                        except Exception as e:
                            raise ValueError(msg) from e
                else:
                    raise TypeError(f"Type of {value!r} is not supported")
        def __str__(self) -> str:
            'For now, just use the id number'
            me = dpstr.Int2Base(id(self), 62)
            return f"Num(0x{id(self):x})"
        def __repr__(self) -> str:
            'This is detailed info for debugger view'
            typ = self.mytype
            s = (f"Num<type={typ}\n"
                 f"   real:  {self.real}\n"
                 f"   imag:  {self.imag}\n"
                 f"   numer: {self.numer}\n"
                 f"   denom: {self.denom}>")
            return s
if 1:   # Functions
    pass

if __name__ == "__main__":  
    if 1:   # Standard imports
        pass
    if 1:   # Custom imports
        import lwtest
    if 1:   # Import symbols
        run = lwtest.run
        raises = lwtest.raises
        Assert = lwtest.Assert
    if 0:   # For script
        d = {}  # Options dictionary
        args = ParseCommandLine(d)
        if args:
            for arg in args:
                pass    # Do stuff
    else:   # For module
        def Demo():
            pass
        def Test_Constructor():
            if 1:   # No input
                num = Num()
                Assert(num.real == 0 and num.imag == 0)
                Assert(num.mytype == NumType.tInt)
            if 1:   # int
                if 1:   # Positive
                    x, T = 30957357, NumType.tInt
                    num = Num(x)
                    Assert(num.numer == x and num.denom == 0)
                    Assert(num.mytype == T)
                    # As string
                    num = Num(str(x))
                    Assert(num.numer == x and num.denom == 0)
                    Assert(num.mytype == T)
                if 1:   # Negative
                    x, T = -30957357, NumType.tInt
                    num = Num(x)
                    Assert(num.numer == x and num.denom == 0)
                    Assert(num.mytype == T)
                    # As string
                    num = Num(str(x))
                    Assert(num.numer == x and num.denom == 0)
                    Assert(num.mytype == T)
            if 1:   # float
                if 1:   # Positive float
                    x, T = 3095.7357, NumType.tFloat
                    num = Num(x)
                    Assert(num.real.real == x and num.real.imag == 0)
                    Assert(num.mytype == T)
                    # As string
                    num = Num(str(x))
                    Assert(num.real.real == mpmath.mpf(str(x)) and num.real.imag == 0)
                    Assert(num.mytype == T)
                if 1:   # Negative float
                    x, T = -3095.7357, NumType.tFloat
                    num = Num(x)
                    Assert(num.real.real == mpmath.mpf(str(x)) and num.real.imag == 0)
                    Assert(num.mytype == T)
                    # As string
                    num = Num(str(x))
                    Assert(num.real.real == mpmath.mpf(str(x)) and num.real.imag == 0)
                    Assert(num.mytype == T)
            if 1:   # Complex
                pass
            if 1:   # Decimal
                pass
            if 1:   # Rational
                pass
            if 1:   # Unc
                pass
        if len(sys.argv) > 1:
            Demo()
        else:
            exit(run(globals(), regexp=r"^Test_", halt=1, verbose=0)[0])
