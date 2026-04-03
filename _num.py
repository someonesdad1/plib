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
                numer: int = 0
                denom: int = 0
                # The imaginary parts of real and image are used to represent uncertainty as a
                # standard deviation
                real: mpmath.mpc = mpmath.mpc("0")
                imag: mpmath.mpc = mpmath.mpc("0")
                mytype: NumType = NumType.tInt
                if value is None:
                    return
            if 1:   # Convert value to our internal representation
                if isinstance(value, int):
                    numer = int(value)
                    mytype = NumType.tInt
                elif isinstance(value, float):
                    real = mpmath.mpc(repr(value), 0)
                    mytype = NumType.tFloat
                elif isinstance(value, f.flt):
                    real = mpmath.mpc(repr(float(value)), 0)
                    mytype = NumType.tFloat
                elif isinstance(value, complex):
                    real = mpmath.mpc(repr(value.real), 0)
                    imag = mpmath.mpc(repr(value.imag), 0)
                    mytype = NumType.tComplex
                elif isinstance(value, f.cpx):
                    real = mpmath.mpc(repr(float(value.real)), 0)
                    imag = mpmath.mpc(repr(float(value.imag)), 0)
                    mytype = NumType.tComplex
                elif isinstance(value, decimal.Decimal):
                    real = mpmath.mpc(str(value), 0)
                    mytype = NumType.tFloat
                elif isinstance(value, fractions.Fraction):
                    numer = value.numerator
                    denom = value.denominator
                    mytype = NumType.tRational
                elif isinstance(value, mpmath.mpf):
                    real = mpmath.mpc(value, 0)
                    mytype = NumType.tMpf
                elif isinstance(value, mpmath.mpc):
                    real = mpmath.mpc(value.real, 0)
                    imag = mpmath.mpc(value.imag, 0)
                    mytype = NumType.tMpc
                elif isinstance(value, uncertainties.UFloat):
                    real = mpmath.mpc(value.nominal_value, value.std_dev)
                    mytype = NumType.tUnc
                elif isinstance(value, str):
                    raise NotImplementedError("str form not implemented yet")
                else:
                    raise TypeError(f"Type of {value!r} is not supported")
        def __str__(self) -> str:
            'Returns a base 62 representation of the memory location'
            me = dpstr.Int2Base(id(self), 62)
            return f"Num({me!r})"
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
        def Test_Basics():
            num = Num()
            #print(num)
        if len(sys.argv) > 1:
            Demo()
        else:
            exit(run(globals(), regexp=r"^Test_", halt=1, verbose=0)[0])
