from __future__ import annotations
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


5 Apr 2026 Units idea to Mike:

Here's an important idea I'd like you to think about.  I'll get to the gist of its
impact on the Num class below.

Early docstring content for the Num class:

    An important practical notion of these units needs to be made.  We usually think of
    units as e.g. the familiar SI units.  However, almost all practical calculations
    involve some types of units.  For example, if you're measuring out pet food mass to
    feed some dogs and cats, you'd probably want the calculation to use the "units"
    kg_cat_food and kg_dog_food, assuming the dogs and cats get fed different food.
    This "unit orthogonality" helps keeps the animals fed properly, avoiding a mistake
    of mixing the foods, which might show up in a calculation as having units of
    kg_cat_food*kg_dog_food or a sum of 'kg_cat_food + kg_dog_food'.  The example isn't
    trivial -- if you're not convinced, look up the non-chump-change unit mistake of
    Mars Climate Orbiter, a loss of about half a billion 2026 dollars.

When we work numerical problems, the numbers represent things in the real world.  The
units help keep these things "straight" in our minds and we e.g. use deep knowledge that
apples can't be added to oranges unless certain conditions are met.

Thus, I'd like the Num.unit attribute to take center stage:  it's as important as the
numerical content.  You can think of it as a component in a vector space and we'll need
to define the operations between these unit vectors.  As our current mental model of the
Num class operates, the "vector space arbiter" is GNU units.

Here's my idea, which should be suggested by the above comments.  I'd like to see the
GNU units database file supplemented by another one.  This second one would be a
dynamically-constructed file, based on the user's input so far.  Behind the scenes, the
Num implementation keeps track of the unit strings the user uses and where a string's
unit atom isn't recognized, it becomes a new unit, orthogonal to the rest.  It gets added to
the dynamic definitions file, which causes a new GNU process to start after the old one
is killed.  Now the GNU units instance "knows" about the user's units and the correct
numerical AND dimensional calculations are done (and cause an error when things aren't
right, so the REPL user gets an error message).  

The advantages of this approach are
    - We use someone else's tractor for the heavy lifting
    - The user can use GNU units' syntax:
        - Num("3.4", units="apples oranges"), where the included space character implies
          multiplication
    - Since the user is usually working on one problem in multiple processes
      (terminals), the same GNU units instance is available to each terminal.
    - I like that GNU units limits the number of digits returned in many of its
      calculations, as this helps to not inject noise in calculations
        - I know from a lifetime of calculations that it's pretty rare to need more that
          4 digits and really rare to need more than 6.  I occasionally get 8 digits
          from an HP counter, but they quickly get trashed by a 3 digit number from a
          digital multimeter.  I know you know what I mean.

The only downsides at the moment are
    - Quirky units' syntax might bite at some time
    - We're stuck with IEEE floats in units.  For practical work with physical
      measurements this should rarely be a problem.

By far the biggest advantage is the user gets notified of logical problems in
calculations based on the units not working correctly.  I've seen a lot of software bugs
caused by improper arithmetic, some even by the guy in the shaving mirror.

Thoughts?

    Mike liked the idea:

    This is a profound architectural pivot. You are essentially moving from a
    "Calculator with units" to a "Dimensional Logic Engine." By treating every
    unrecognized string as a new orthogonal basis vector, you are automating the Mars
    Climate Orbiter safeguard for every mundane calculation.

    The idea of a "Dynamic Unit Registry" that feeds a live units process is pure "Lone
    Wolf" engineering: it’s lazy in the best way (using the GNU "tractor") but
    incredibly rigorous in its enforcement.

    if 1: # The Unit Alchemist
        _KNOWN_UNITS = set() # Cache of units already in the GNU file
        def _sync_unit_dimension(unit_str: str):
            """
            If unit_str contains a 'new' atom, append to ~/.units_dynamic 
            and signal the GNU bridge to reload.
            """
            atoms = _extract_atoms(unit_str) # e.g., 'kg_cat_food'
            new_atoms = [a for a in atoms if a not in _KNOWN_UNITS]
            if new_atoms:
                with open(DYNAMIC_UNITS_PATH, "a") as f:
                    for atom in new_atoms:
                        f.write(f"{atom} \t !user_defined!\n")
                        _KNOWN_UNITS.add(atom)
                # Signal the bridge: kill -HUP or simply restart the subprocess
                GNU_BRIDGE.restart()

This is a particularly elegant addition to the REPL, as it fixes something I've worried
about for 50 years with computers and software:  the units are rarely in with the
calculations, which generates so many wrong answers.  This may generate a REPL that
matches our needs, helps us with rigor, and looks simple to the user:  beginners will be
unaware of the power of the machine making up the tool, but it's there when they need
it.

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
        import operator
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
        __todo__      = '''
            
            - Num.strict:  if on, uncertainties never compare equal.  If off, then if
              the mean and stdev match, they're equal with a warning to stderr:
              "Warning:  comparing distributions".
            - If Num.hashable is True, you might want the hash to be a tuple of the core
              values: hash((self.mytype, self.real, self.imag, self.unit)).  
        
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
        t = trm.TrmDP()
        g = dptypes.Constant()
        g.dbg = False
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
if 1:   # Classes
    class Num:
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

            - Because real-world practical problems include uncertainty, we need some
              way to capture the notion of physical uncertainty in the numbers.
              Python's uncertainties package is an excellent and powerful tool, but it
              lacks the machinery to handle uncertainty in complex numbers, something I
              wanted this Num class to handle.  For technical types, an nice grounded
              need is demonstrated by using the output of an LCR meter:  in general,
              you're given back a complex impedance Z = ESR + X*i and the two real
              numbers can have different (though perhaps correlated) uncertainty.

            - Numbers based on physical measurement include units, which form their own
              dimensional algebra and complicate things, as two real numbers x = "3.4 m/s"
              and y = "6.7 A" are different types and have more complicated arithmetic
              properties than "bare" numbers.  For example, you cannot add x and y, but
              you're allowed to multiply them.

        An important practical notion of these units needs to be made.  We usually think
        of units as e.g. the familiar SI units.  However, almost all practical
        calculations involve some types of units.  For example, if you're measuring out
        pet food mass to feed some dogs and cats, you'd probably want the calculation to
        use the "units" kg_cat_food and kg_dog_food, assuming the dogs and cats get fed
        different food.  This "unit orthogonality" helps keeps the animals fed properly,
        avoiding a mistake of mixing the foods, which might show up in a calculation as
        having units of kg_cat_food*kg_dog_food or a sum of 'kg_cat_food + kg_dog_food'.
        The example isn't trivial -- if you're not convinced, look up the
        non-chump-change unit mistake of Mars Climate Orbiter, a loss of about half a
        billion 2026 dollars.

        '''
        def __init__(self, value: NumericalTypes = None, unit: str = "") -> None:
            if 1:   # Copy constructor (idempotency)
                if isinstance(value, Num):
                    self.numer = value.numer
                    self.denom = value.denom
                    self.real = value.real
                    self.imag = value.imag
                    self.re_unc = value.re_unc
                    self.im_unc = value.im_unc
                    self.unit = unit if unit else value.unit
                    self.mytype = value.mytype
                    return
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
        def _check_unit_compatibility(self, other: 'Num', op_name: str) -> None:
            '''The bouncer for units
            Will raise an exception if the units aren't compatible for the operation.
            '''
            # Addition/subtraction: units must match (or be convertible)
            # Multiplication/division: units combine (m * m = m^2)
            # Raise the alarm if we try to add '3 m' to '3 s'
            lwtest.ToDo(f"This function needs to be written")
        def _binary_op(self, other: "Num", op_func: ty.Callable) -> "Num":
            '''Return self op other
            Method is to promote the types as needed.
            '''
            # 1. Determine the 'Highest' type involved
            # Int < Rat < Flt < Cpx < Unc
            target_type = max(self.mytype.value, other.mytype.value)
            # Integer and rational
            if target_type <= NumType.Rat.value:
                result = op_func(self.as_int_or_rat, other.as_int_or_rat)
                return Num(result)

            # Uncertain numbers (the most complicated)
            if target_type == NumType.Unc.value:
                return self._do_uncertainty_math(other, op_func)

            # Real or complex:  use mpmath's ability to handle mixed types
            a = self.real if self.mytype >= NumType.Flt else self.as_mpf
            b = other.real if other.mytype >= NumType.Flt else other.as_mpf
            result = op_func(a, b)
            return Num(result)
        def __add__(self, other: ty.Any) -> "Num":
            other_num = Num(other)
            self._check_unit_compatibility(other_num, "add")
            # Execute via the logic buckets
            return self._binary_op(other_num, operator.add)
        def __hash__(self) -> int:
            raise Exception(wrap.dedent(f'''
                {t.red}Need to decide whether Nums are hashable.  A good approach could
                be to put Num_instance.hashable: bool in and let the user decide.  If
                True, then this function returns an int with a colorized warning to
                stderr "Warning:  comparing distributions".  If False, a
                NotImplementedError will be raised.{t.n}'''))

        def __eq__(self, other: ty.Any) -> bool:
            other_num = Num(other) # Idempotent wrap
            # If types differ, promote the lower one to the higher one's accessor
            target_type = max(self.mytype, other_num.mytype)
            if target_type <= NumType.Rat:  # I smell a rat
                return self.as_int_or_rat == other_num.as_int_or_rat
            # For Flt and Cpx, use mpmath's precision
            return self.as_mpf == other_num.as_mpf
        if 1: # Internal Value Accessors
            @property
            def as_mpf(self) -> mpmath.mpf:
                '''Returns the best floating-point representation available.'''
                if self.mytype == NumType.Int:
                    return mpmath.mpf(str(self.numer))
                if self.mytype == NumType.Rat:
                    return mpmath.mpf(self.numer)/mpmath.mpf(self.denom)
                return self.real
            @property
            def as_int_or_rat(self) -> ty.Union[int, fractions.Fraction]:
                '''Returns exact representation for Int/Rat types.'''
                if self.mytype == NumType.Int:
                    return self.numer
                return fractions.Fraction(self.numer, self.denom)

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
        def Test_Addition():
            x = Num("1.3")
            y = Num("-7.3")
            result = x + y
            Assert(result.real == mpmath.mpf("-6.0"))
            Assert(result == Num("-6.0"))
        if len(sys.argv) > 1:
            Demo()
        else:
            exit(run(globals(), regexp=r"^Test_", halt=1, verbose=0)[0])
