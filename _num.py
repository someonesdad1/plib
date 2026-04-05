'''
 5 Apr 2026 Task

- Get constructor to initialize properly
- Perform an addition of Num(33) + Num(3.444448)
- Show inclusion of units, but don't hook up type plumbing yet

---------------------------------------------------------------------------'
General number implementation

Vision:  a single number object for a REPL environment that allows use with physical
units.  The GNU units program will be the arbiter for the units calculation and it must
be satisifed for the calculation to proceed to numerical evaluation (or overridden).  

- With the proper semantics and grease, numpy can be used to do the calculations behind
  the scene.  This isn't for high-speed huge matrices, it's for the 10 to 1000 data a
  person working at a practical problem might encounter.
- SQLite can be used as a repository for data, giving speed and, effectively, a single
  channel IPC method.  Another process in another terminal can have its data be shared
  by SQLite giving it a namespace that another process can use/list and borrow what's
  needed.  In general, we want our process' local variables to be locally private, but
  sometimes we want to share.
- The minitab environment I remember let data be accessible as column vectors and
  matrices.  I showed Mike the transformation, stats, and regression tools of xfmpy
  and explained I want these in the REPL too.
- Plotting is important for models, but I don't have a GUI handy like matplotlib in WSL.
  But Plotext can do such things well enough in another terminal window to let you see
  residual plots, histograms, and probability plots.  The user should be able to run a 
  command to say "send this data to be plotted in the other window".
- Persistence:  the db approach gives data persistence so when you start a new REPL in a
  window, you see the same data you saw when you last exited.  This provides problem
  continuity, as often you have to e.g. go to a prompt and do some other task.

Another vision is that this tool should be minimalistic, in the sense that the
components required should be easy for people to get.  So far, I know of the following
dependencies:
    - python 3.11
    - mpmath (pip)
    - plotext (pip)
    - numpy (pip)
    - GNU units (external package)
    - SQLite (built into python)

---------------------------------------------------------------------------

Experiment:  construct a python class that holds a number.  The vision is that this
number can be an int, float, complex, rational, or a float or complex with uncertainty
in each element.  Behind the scenes the implementation is done with mpmath.mpf floating
point numbers.  The plan is that a REPL will be made that provides these numbers for
general computing.  The fmt.py and trm.py files will be used for formatting and
colorizing (colorizing the type will be helpful to the user, not for identifying the
type, which can be done by the formatting, but to alert to perhaps an unexpected change
in type).

The formatting will be controlled by the allowed width for the number display.  This
will default to the width of the terminal, but the user can set it to smaller numbers.
When this width is exceeded, the U+22EF character ⋯ "midline horizontal ellipsis" is
used to indicate middle character removal to fit things to the current number of spaces.

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

Mentioned this Num idea to Mike and asked him to save the thread for future discussion.
Some core ideas
    - Num class that's a universal container for numbers
        - Int, Flt, Cpx, Rat, Unc are the enum types.  An Unc can be
          either a Flt or Cpx (for Cpx, need correlation coefficient between re and im
          parts)
    - Units:  units operations are handled by pipe to GNU units.  Can be used to get
      definitions of oddball units as well as do dimensional algebra.
        - Use -t option in pipe:  terse output, perfect for processing
        - Write a module function that does 15 digit conversion factors and dimensional
          algebra
    - Memory:  SQLite-backed state machine for atomic, multi-process safety across
      WSL/tmux use
        - Handles file locking.  You can query it via grep or an SQL query to e.g. "find
          "Every calculation where the result was a NumType.Unc with a standard
          deviation > 5%."
        - Logging:  The database is the log. Every input, output, and timestamped state
          change goes into a row.
    - Display:  trm.py and fmt.py providing real-time, context-aware, colorized feedback
    - Logging:  a recorder that logs every move to ensure you know what happened
    - Terminal power that fits in a tmux pane
    - It's a multi-process safe REPL, essentially a distributed state machine
    - Note uncertainty for complex numbers needs to know the covariance matrix between
      the two components (i.e., you just need the correlation coefficient)
    - Write-ahead log pattern
        - Before the Num calculation starts, log the input.
        - After the calculation:  log the result, the current mpmath.mp precision, and
          any Fmt state changes.
        - If it crashes:  the "input" is already on disk, so you know exactly which
          string caused the problem.
    - Variables:  if you have two terminals open, should they share variables?
        - Shared State: If you set a = Num(5) in Terminal A, does Terminal B see it?
          This requires a central "Variable Server" or a watched database.
        - Isolated State / Shared History: Usually, physicists prefer isolated
          namespaces but a shared "Knowledge Base." You can have a global_history table
          and a session_variables table.
    - Console architecture
        - Using code.InteractiveConsole is a great base, but we can wrap it to inject
          your Num logic and Fmt context manager automatically.  

            import code
            import sys
            class PhysicsREPL(code.InteractiveConsole):
                def __init__(self, locals=None):
                    # Inject our 'Num' and 'Fmt' into the REPL's namespace
                    names = locals or {}
                    names.update({
                        'Num': Num,
                        'fmt': Fmt(), # Your context-aware formatter
                        'mp': mpmath.mp
                    })
                    super().__init__(locals=names)
                def push(self, line):
                    'Intercept the command to log it before execution'
                    self.log_input(line)
                    return super().push(line)
                def write(self, data):
                    'Colorize and log the output via trm and fmt'
                    # Use your Trm/Fmt logic here to make the REPL 'pretty'
                    sys.stderr.write(f"{t.grn}{data}{t.no}")

    - Other
        - Serialization: How do we store a Num in the DB? (Pickle is easy but dangerous;
          a custom JSON-like string with Type/Value/Unit is "Siriusly" better).
        - Crash Recovery: If the REPL dies, do you want it to auto-reload the last 50
          variables?
        - The "Wizard's" Role: I can help you write the __repr__ for Num that uses your
          "Plucked Middle" and FmtColor logic so that just typing x in the REPL gives
          you a wealth of metadata.
        - I also want the ability to turn the db data into a text file that can be
          converted back; this lets me edit the contents in my editor to prune stuff
          that doesn't need to stick around.  A python tool acts as the gatekeeper in
          both directions.
    - Safety:  the "black box" traceback
        - Since your REPL will be talking to units via subprocess and mpmath for the
              heavy lifting, the "Why" of a failure can get buried. In your
              PhysicsREPL(code.InteractiveConsole) wrapper, we should override
              showtraceback() to specifically pull the last state from the SQLite
              "Flight Recorder."
            - That way, if the engine explodes, the terminal won't just give you a
              generic Python error; it will say:
                - "Dimensional Mismatch: Attempted to add Tesla to Bananas while mp.prec
                  was 128."

- Thoughts
    - I like the SQLite approach to persistence.  This should be structured so that the
      db file is versioned in git.  Then, most importantly, it needs to be dumped in a
      text form to a file in its whole that lets me edit the thing with an editor.  This
      lets me prune stuff that's not needed anymore.  It's the mental equivalent to
      having a binary file X, then doing 'xxd X >a; vi a; xxd -r a >X'.
    - Good questions and should result in a powerful tool.  I particularly like the idea
      of "injecting" the normal REPL's namespace, as it leaves you with the other tools.
    - I'd like some namespace reducing tools.  For example, the 'm' namespace might
      provide all the Num/mpmath symbols, the 'g' namespace could be my global
      "between-processes" namespace, and the 'd' namespace would be the REPL-local
      namespace.  However, each process could have its data saved at anytime in the db
      under a name and other processes could access this data if the namespace is known.  
    - The REPL needs some single letter commands, like 'q' to quit.  
    - The GNU units command is used for unit conversion & typing stuff
    - If I quit a REPL, then start it from the same shell, I should be exactly where I
      was before the quit.
    - The colorful Unicode prompt ▶▶▶ I used in /plib/repl.py is a core way for the the tool
      to communicate important status.  An ❌ can show the last command failed, just
      like I use in my WSL shell via starship.  Or, the ▶▶▶ can have a red background.
      I could live with a normal prompt of ▶; extra ones would indicate e.g. a pushed
      state.
    - Core needs
        - Vectors and 2D matrixes of Num objects
        - These need to be handled by numpy if possible by e.g. a type-narrowing
          transformation to floats
        - Provide core tools of xfmpy
            - xfm of vectors
            - stats on column vectors
            - Multiple linear regression
        - Use plotext to make "remote" plots in another terminal as its data window
        
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
        import typing as ty
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
    NumType = enum.Enum("NumType", ("Int", "Flt", "Cpx", "Rat", "Unc"))
    NumericalTypes = ty.Union[int | float | complex | decimal.Decimal |
                              fractions.Fraction | mpmath.mpf | mpmath.mpc |
                              uncertainties.UFloat | str | None]
    class Num:
        '''Represent a general number useful for routine calculations

        The internal representation uses mpmath, so it's your responsibility as the
        user to ensure the mpmath context has sufficient resolution for your problems.
        '''
        def __init__(self, value: NumericalTypes = None, unit: str = "") -> None:
            if 1:   # Default internal state representation
                # numer & denom are for Int and Rat
                self.numer: int = 0
                self.denom: int = 1
                # real & imag for Flt and Cpx
                self.real: mpmath.mpf = mpmath.mpf("0")
                self.imag: mpmath.mpf = mpmath.mpf("0")
                # re_unc & im_unc for Unc:  the _unc portion is the standard deviation
                self.re_unc: mpmath.mpf = mpmath.mpf("0")
                self.im_unc: mpmath.mpf = mpmath.mpf("0")
                self.correl: mpmath.mpf = mpmath.mpf("0")   # Correlation coefficient
                self.unit: str|None = unit
                self.mytype: NumType = NumType.Int
                if value is None:
                    return
            if 1:   # Convert value to our internal representation
                if isinstance(value, int):
                    self.numer = int(value)
                    self.mytype = NumType.Int
                elif isinstance(value, float):
                    self.real = mpmath.mpc(repr(value), 0)
                    self.mytype = NumType.Flt
                elif isinstance(value, complex):
                    self.real = mpmath.mpc(repr(value.real), 0)
                    self.imag = mpmath.mpc(repr(value.imag), 0)
                    self.mytype = NumType.Cpx
                elif isinstance(value, decimal.Decimal):
                    self.real = mpmath.mpc(str(value), 0)
                    self.mytype = NumType.Flt
                elif isinstance(value, fractions.Fraction):
                    self.numer = value.numerator
                    self.denom = value.denominator
                    self.mytype = NumType.Rat
                elif isinstance(value, mpmath.mpf):
                    self.real = mpmath.mpc(value, 0)
                    self.mytype = NumType.Flt
                elif isinstance(value, mpmath.mpc):
                    self.real = mpmath.mpc(value.real, 0)
                    self.imag = mpmath.mpc(value.imag, 0)
                    self.mytype = NumType.Cpx
                elif isinstance(value, uncertainties.UFloat):
                    self.real = mpmath.mpf(str(value.nominal_value))
                    self.re_unc = mpmath.mpf(str(value.std_dev))
                    self.mytype = NumType.Unc
                    print(f"{__file__}:  Need to handle re/im correlation", file=sys.stderr)
                elif isinstance(value, str):
                    msg = f"{value!r} not recognized as a number"
                    normalized = set(value.lower().replace("i", "j").strip())
                    if "/" in normalized:    # It's rational
                        try:
                            self.numer, self.denom = [int(i) for i in value.split("/")]
                            self.mytype = NumType.Rat
                        except Exception as e:
                            raise ValueError(msg) from e
                    elif "j" in normalized:  # It's complex
                        re, im = dpmath.ParseComplex(value)
                        self.real = mpmath.mpf(re)
                        self.imag = mpmath.mpf(im)
                        self.mytype = NumType.Cpx
                    elif "." in normalized or "e" in normalized:  # It's floating point
                        try:
                            self.real = mpmath.mpf(value)
                            self.mytype = NumType.Flt
                        except Exception as e:
                            raise ValueError(msg) from e
                    else:   # It's an integer
                        try:
                            self.numer = int(value)
                            self.mytype = NumType.Int
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
        if len(sys.argv) > 1:
            Demo()
        else:
            exit(run(globals(), regexp=r"^Test_", halt=1, verbose=0)[0])
