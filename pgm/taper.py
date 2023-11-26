'''
Script to deal with tapers
 
Operators & their arguments
 
- t name size 
    - Print out table of taper sizes
    - If no name is given, it's assumed to be a Morse taper
    - If neither name or size are given, a help message is printed
    - name
        - m (Morse)
        - ms (Morse Stub)
        - b (B&S)
        - jar (Jarno)
        - jac (Jacobs)
        - a (Milling machine spindle)
    - size
        - Morse:  0-7
        - Morse stub:  1-5
        - B&S:  1-18
        - Jarno:  2-20 (note 11 is special, as it can have D as 1-3/8 or
          1-1/2; my lathe has 1.5)
        - Jacobs:  0-6, 33
- b
    - Print a table of steps to bore a tapered socket or a male taper
- i
    - Same as b except you are prompted for the data
- c
    - Calculate a taper from 2 diameters and a length.  If it matches any
      of the standard tapers, so indicate.
 
Script to calculate feeds for step boring in the lathe.  An example is to
make a Morse taper by step-boring, followed by reaming.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Calculate feeds for step-boring in lathe
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Imports
        import sys
        import getopt
    if 1:   # Custom imports
        from wrap import dedent
        from get import GetNumber
        from frange import frange
        from f import flt, tan, sin, atan, pi, degrees, ceil
        from color import t
    if 1:   # Global variables
        nl = "\n"
        ii = isinstance
        # indicator_size defines the range in inches of the longitudinal
        # measurement with a dial indicator on the lathe.
        indicator_size = 2
        # Set dbg to True to get input data automatically for debugging
        dbg = False
        dbg = True
        # Colors
        t.dbg = t("denl")
        t.title = t("ornl")
        t.impt = t("grnl")
        t.hdr = t("magl")
if 1:   # Classes
   class Taper(object):
       'Base class for tapers'
       def __init__(self, sizes):
           if not ii(sizes, set):
               raise ValueError("sizes must be a set")
           self.sizes = sizes
           self.data = {}
       def __str__(self):
           name = self.name
           sizes = tuple(self.sizes)
           return "{name}{sizes}".format(**locals())
       def errmsg(self, n):
           return "'{}' is a bad {} taper number".format(str(n), self.name)
       def __call__(self, size):
           '''Returns the tuple (tpi, large_diameter, length) in inches for a
           taper number size of this particular taper.
           '''
           raise ValueError("Abstract base class")
   class Morse(Taper):
       def __init__(self):
           self.name = "Morse"
           self.super = super(Morse, self)
           self.super.__init__(set(range(8)))
           # Dimensions in inches; see MH, 19th ed., pg 1679. 
           self.data = {
               # tpf = taper in inches per foot
               # A = large diameter
               # H = hole depth
               #      tpf       A      H
               0: [0.62460, 0.3561, 2+1/32],
               1: [0.59858, 0.475, 2+5/32],
               2: [0.59941, 0.700, 2+39/64],
               3: [0.60235, 0.938, 3+1/4],
               4: [0.62326, 1.231, 4+1/8],
               5: [0.63151, 1.748, 5+1/4],
               6: [0.62565, 2.494, 7+21/64],
               7: [0.62400, 3.270, 10+5/64],
           }
       def __call__(self, n):
           '''Return the tuple (D, d, L) where the dimensions are in inches.
           D is the large diameter, d is the small diameter, and L is the
           length of the Morse taper socket.  n is the taper number.
           '''
           if n not in self.sizes:
               raise ValueError(self.errmsg(n))
           X = 1/16 if n else 1/32
           tpf, D, L = [flt(i) for i in self.data[n]]
           tpi = tpf/12    # Taper per inch in inch/inch
           d = D - (L - X)*tpi
           return (D, d, L)
   class Jarno(Taper):
       def __init__(self):
           self.name = "Jarno"
           self.super = super(Jarno, self)
           self.super.__init__(set(range(2, 21)))
       def __call__(self, n):
           '''Return the tuple (D, d, L) where the dimensions are in inches.
           D is the large diameter, d is the small diameter, and L is the
           length of the socket.  n is the taper number.
    
           See MH, 19th ed., pg 1683.  If n is the taper number, then
           (dimensions in inches)
               D = n/8
               d = n/10
               L = n/2
           '''
           if n not in self.sizes:
               raise ValueError(self.errmsg(n))
           return (flt(n/8), flt(n/10), flt(n/2))
   class BrownAndSharpe(Taper):
       def __init__(self):
           self.name = "Brown & Sharpe"
           self.super = super(BrownAndSharpe, self)
           self.super.__init__(set(range(1, 19)))
           self.data = {
               # Reference MH, 19th ed., pg 1682.
               #   [ tpf(inch), minor_dia, length]
               1: [0.50200, 0.20000, 15/16],
               2: [0.50200, 0.25000, 1+3/16],
               3: [0.50200, 0.31250, 1+1/2],
               4: [0.50240, 0.35000, 1+11/16],
               5: [0.50160, 0.45000, 2+1/8],
               6: [0.50329, 0.50000, 2+3/8],
               7: [0.50147, 0.60000, 2+7/8],
               8: [0.50100, 0.75000, 3+9/16],
               9: [0.50085, 0.90010, 4+1/4],
               10: [0.51612, 1.04465, 5],
               11: [0.50100, 1.24995, 5+15/16],
               12: [0.49973, 1.50010, 7+1/8],
               13: [0.50020, 1.75005, 7+3/4],
               14: [0.50000, 2.00000, 8+1/4],
               15: [0.50000, 2.25000, 8+3/4],
               16: [0.50000, 2.50000, 9+1/4],
               17: [0.50000, 2.75000, 9+3/4],
               18: [0.50000, 3.00000, 10+1/4],
           }
       def __call__(self, n):
           '''Return the tuple (D, d, L) where the dimensions are in inches.
           D is the large diameter, d is the small diameter, and L is the
           length of the socket.  n is the taper number.
           '''
           if n not in self.sizes:
               raise ValueError(self.errmsg(n))
           # Symbols are from page 1682 of MH, 19th ed.  tpf = taper per foot,
           # d = diameter of small end of plug, P = plug depth.
           tpf, d, P = [flt(i) for i in self.data[n]]
           tpi = tpf/12
           D = d + P*tpi
           return (D, d, P)
   class Jacobs(Taper):
       def __init__(self):
           self.name = "Jacobs"
           self.super = super(Jacobs, self)
           sizes = set(range(7))
           sizes.add(33)
           self.super.__init__(sizes)
           self.data = {
               # Reference MH, 19th ed., pg 1690.
               0: [0.2500, 0.22844, 0.43750],
               1: [0.3840, 0.33341, 0.65625],
               2: [0.5590, 0.48764, 0.87500],
               3: [0.8110, 0.74610, 1.21875],
               4: [1.1240, 1.03720, 1.65630],
               5: [1.4130, 1.31610, 1.87500],
               6: [0.6760, 0.62410, 1.00000],
               33: [0.6240, 0.56050, 1.00000],
           }
       def __call__(self, n):
           '''Return the tuple (D, d, L) where the dimensions are in inches.
           D is the large diameter, d is the small diameter, and L is the
           length of the socket.  n is the taper number.
           '''
           if n not in self.sizes:
               raise ValueError(self.errmsg(n))
           return tuple(flt(i) for i in self.data[n])
   class Sellers(Taper):
       '''Defined on page 791 and 795 of Colvin & Stanley, "American
       Machinist's Handbook", 8th ed., 1945.  Also see page 1687 of MH, 19th
       ed.
       '''
       def __init__(self):
           self.name = "Sellers"
           self.super = super(Sellers, self)
           sizes = set((200, 250, 300, 350, 400, 450, 500, 600, 800, 1000, 1200))
           self.super.__init__(sizes)
           self.tpf = flt(1 + 3/4)
           self.Bprime = {   # Length from gauge line
               200: 5+1/8,
               250: 5+7/8,
               300: 6+5/8,
               350: 7+7/16,
               400: 8+3/16,
               450: 9,
               500: 9+3/4,
               600: 11+5/16,
               800: 14+3/8,
               1000: 17+7/16,
               1200: 20+1/2,
           }
       def __call__(self, n):
           '''Return the tuple (D, d, L) where the dimensions are in inches.
           D is the large diameter, d is the small diameter, and L is the
           length of the socket.  n is the taper number.
           '''
           if n not in self.sizes:
               raise ValueError(self.errmsg(n))
           D = flt(n/100)
           L = flt(self.Bprime[n])
           tpi = self.tpf/12
           d = D - L*tpi
           return (D, d, L)
   class NMTB(Taper):
       '''Defined on page 1691 of MH, 19th ed.
       '''
       def __init__(self):
           self.name = "NMTB"
           self.super = super(NMTB, self)
           sizes = set((30, 40, 50, 60))
           self.super.__init__(sizes)
           self.tpi = flt(3.5/12)
           self.data = {
               # A = large diameter of taper
               # C = small diameter of taper
               #        A      C
               30: (1+1/4, 0.6885),
               40: (1+3/4, 1.001),
               50: (2+3/4, 1.5635),
               60: (4+1/4, 2.376),
           }
       def __call__(self, n):
           '''Return the tuple (D, d, L) where the dimensions are in inches.
           D is the large diameter, d is the small diameter, and L is the
           length of the socket.  n is the taper number.
           '''
           if n not in self.sizes:
               raise ValueError(self.errmsg(n))
           D, d = [flt(i) for i in self.data[n]]
           L = (D - d)/self.tpi
           return (D, d, L)
if 1:   # Utility
    def Dbg(*p, **kw):
        if dbg:
            print(f"{t.dbg}", end="")
            t.print(*p, **kw)
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] op arguments
          t 
            Print table of taper sizes
          b
            Print step boring/turning information (you'll be prompted for
            the taper)
          m
            Calculate taper from measurements (you'll be prompted for
            the measurements)
        Options:
            -d n    Number of significant figures
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 4         # Number of significant digits
        d["-m"] = False     # Output in mm
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:hm") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("m"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o == "-h":
                Usage(status=0)
        x = flt(0)
        x.N = d["-d"]
        x.rtz = x.rtdp = False
        if not dbg and not args:
            Usage()
        return args
if 1:   # Core functionality
    def TaperSizes():
        print(dedent(f'''
        Taper sizes in mils
          Dimensions are for the socket
            D       Large end diameter
            d       Small end diameter
            L       Length
            θ       Half of taper's included angle in degrees
            tpi     Taper in mils per inch.  This is a dial indicator's
                    reading on the cross slide if you move the saddle 
                    1 inch towards the headstock.
            tpf     Taper per foot in mils
 
        '''))
        w = 8
        i = " "*3
        for id in tapers:
            T, name = tapers[id]
            t.print(f"{t.title}{name} tapers")
            t.print(f"{t.hdr}{i}Num{'D ':>{w}s} {'d ':>{w}s} {'L ':>{w}s} {'θ, °':>{w}s}  "
                  f"{'tpi/2':>{w}s}{'tpf':>{w}s}")
            f = lambda x: str(int(1000*x))
            for N in T.sizes:
                D, d, L = T(N)
                tpi = (D - d)/L
                tpf = 1000*12*tpi
                θ = degrees(atan(tpi/2))
                impt = (name == "Morse" and N == 3)
                if impt:
                    print(f"{t.impt}", end="")
                print(f"{i}{N:2d} {f(D):>{w}s} {f(d):>{w}s} {f(L):>{w}s} {θ:>{w}.4f}"
                      f"  {1000*tpi/2!s:>{w}s} {tpf!s:>{w}s}", end="")
                t.print() if impt else print()
            print()
    def Get(prompt, allowed=None):
        if allowed:
            print("Answers:  ", ' '.join(allowed))
        while True:
            s = input(prompt).lower()
            if s == "q":
                exit(0)
            elif allowed:
                if s in allowed:
                    return s
                print("Must be one of:")
                print("  ", ' '.join(allowed))
            else:
                return s
    def StepBoring():
        'Prompt user for details and print out a step boring table'
        # Get data by prompting:
        #   Taper name
        #   Taper size
        #   Longitudinal step
        t.print(f"{t.title}Step boring table for a taper\n")
        print("Default units are inches.  Include different unit if desired.")
        if 0 and dbg:
            taper = "m"
            T, name = tapers[taper]
            num = 3
            step = flt(0.1)
            allow = 0.003
        else:
            taper = Get("Which taper? ", list(tapers))
            T, name = tapers[taper]
            nums = [str(i) for i in T.sizes]
            num = int(Get("Which number? ", nums))
            ans = GetNumber("Enter longitudinal step size: ", low=0,
                low_open=True, allow_quit=True, use_unit=True, default="0.1")
            step = ans[0]
            if ans[1]:
                step = ans[0]*u(ans[1])/u("in")
            allow = GetNumber("Allowance for reaming", low=0, high=0.006,
                low_open=True, allow_quit=True, use_unit=False, default="0.003")
        Dbg(f"Taper = {name} {num}")
        Dbg(f"Step size = {step} inches")
        Dbg(f"Allowance = {allow} inches")
        D, d, L = T(num)
        # Report
        i, w = " "*4, 6
        f = lambda x: str(int(1000*x))
        print(f"\n{name} {num} taper (dimensions in mils)")
        print(f"{i}D{2*i}{f(D):>{w}s}")
        print(f"{i}d{2*i}{f(d):>{w}s}")
        print(f"{i}L{2*i}{f(L):>{w}s}")
        delta = flt(0.05)
        with delta:
            delta.rtz = True
            print(dedent(f'''
 
            Use stock length of at least {L + delta} inches.  This allows {delta} inches of
            the first cut to be used to set cross slide to zero.  You'll face this
            {delta} inch off at the end.
 
            '''))
        print(dedent(f'''
        Bore hole to d = {f(d - allow)} mils.  Set boring bar face to front edge of work.
        Set longitudinal dial indicator to zero.
 
        '''))
        with delta:
            delta.rtz = True
            print(dedent(f'''
            Bore {delta} deep to a diameter of {f(D - allow)} mils.  Set cross slide to zero.
            Set longitudinal dial indicator to zero.
 
            '''))
        N = ceil(L/step)
        print(f"{i}Cut     Depth, in    Cross feed, mils")
        xstep = (D - d)/N
        for j in range(N + 1):
            depth = j*step
            cross = max(j*xstep - allow, 0)
            cross = f(cross)
            with depth:
                depth.rtz = True
                print(f"{i}{j:2d}{' '*8}{depth!s:^6s}{' '*10}{cross:^6s}")
        with delta:
            delta.rtz = True
            print(dedent(f'''
 
            Face off {delta} inch from the front of the socket.
            '''))
    def Measured():
        'Prompt for D, d, L and try to identify taper'
        t.print(f"{t.title}Calculate taper values from measurements\n")
        if dbg:
            D = flt(0.938)
            d = flt(0.778)
            L = flt(3.25)
        else:
            print("Enter the measured values for the taper (default units inches):")
            while True:
                D, units = GetNumber("  Large diameter? ", low=0, low_open=True, allow_quit=True, use_unit=True)
                if units:
                    D *= u(units)/u("inch")
                d, units = GetNumber("  Small diameter? ", low=0, low_open=True, allow_quit=True, use_unit=True)
                if units:
                    d *= u(units)/u("inch")
                if d <= D:
                    break
                else:
                    print("Can't have d > D, try again")
            L, units = GetNumber("  Length? ", low=0, low_open=True, allow_quit=True, use_unit=True)
            if units:
                L *= u(units)/u("inch")
            print()
        print(dedent(f'''
        Input data
            D = large diameter = {D} inches
            d = small diameter = {d} inches
            L = length         = {L} inches
        '''))
        tpi = (D - d)/L
        θ = atan(tpi/2)
        print(dedent(f'''
 
        Calculated data
            θ = half angle          {degrees(θ)}°
            2θ = included angle     {degrees(2*θ)}°
            tpi                     {tpi}
            tpf                     {tpi*12}
            tan(θ)                  {tan(θ)}
            tan(2θ)                 {tan(2*θ)}

        In the lathe, a dial indicator traversed 1 inch along the taper
        will show a change of {tpi/2:.3f} inches.
        '''))

if __name__ == "__main__":
    opt = {}      # Options dictionary
    tapers = {
        #"s": (Sellers(), "Sellers"),
        "b": (BrownAndSharpe(), "Brown & Sharpe"),
        "n": (NMTB(), "NMTB"),
        "jar": (Jarno(), "Jarno"),
        "jac": (Jacobs(), "Jacobs"),
        "m": (Morse(), "Morse"),
    }
    args = ParseCommandLine(opt)
    if not dbg:
        op = args.pop(0)
    else:
        op = "m"
    if op == "t":
        TaperSizes()
    elif op == "b":
        StepBoring()
    elif op == "m":
        Measured()
    else:
        Error(f"{op!r} not recognized")
