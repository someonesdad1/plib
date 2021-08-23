'''
Script to calculate feeds for step boring in the lathe.  An example is to
make a Morse taper by step-boring, followed by reaming.
'''
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
    import math
    import getopt
    import time
    from pprint import pprint as pp
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from u import u, ParseUnit
    from get import GetNumber
    from bidict import bidict
    from frange import frange
    from sig import sig
if 1:   # Global variables
    nl = "\n"
    ii = isinstance
    # indicator_size defines the range in inches of the longitudinal
    # measurement with a dial indicator on the lathe.
    indicator_size = 2
    # Set dbg to True to get input data automatically for debugging
    dbg = 1
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
        '''Returns the tuple (tpf, small_diameter, length) in inches for a
        taper number size of this particular taper.
        '''
        raise ValueError("Abstract base class")
class Morse(Taper):
    def __init__(self):
        self.name = "Morse"
        self.super = super(Morse, self)
        self.super.__init__(set(range(8)))
        # Dimensions in inches; see MH, 19th ed., pg 1679.  The symbols
        # are:  tpf is the taper in inches per foot, D is the small
        # diameter of the plug, H is the depth of the hole, and X is the
        # additional length of the socket such that P = H - X = plug depth.
        self.data = {
            #      tpf       D      H       X
            0  : [0.62460, 0.252, 2+1/32,  1/32],
            1  : [0.59858, 0.369, 2+5/32,  1/16],
            2  : [0.59941, 0.572, 2+39/64, 1/16],
            3  : [0.60235, 0.778, 3+1/4,   1/16],
            4  : [0.62326, 1.020, 4+1/8,   1/16],
            5  : [0.63151, 1.475, 5+1/4,   1/16],
            6  : [0.62565, 2.116, 7+21/64, 1/16],
            7  : [0.62400, 2.750, 10+5/64, 1/16],
        }
        self.data = {
            # tpf = taper in inches per foot
            # A = large diameter
            # H = hole depth
            #      tpf       A      H
            0  : [0.62460, 0.3561, 2+1/32],
            1  : [0.59858, 0.475 , 2+5/32],
            2  : [0.59941, 0.700 , 2+39/64],
            3  : [0.60235, 0.938 , 3+1/4],
            4  : [0.62326, 1.231 , 4+1/8],
            5  : [0.63151, 1.748 , 5+1/4],
            6  : [0.62565, 2.494 , 7+21/64],
            7  : [0.62400, 3.270 , 10+5/64],
        }
    def __call__(self, n):
        '''Return the tuple (D, d, L) where the dimensions are in inches.
        D is the large diameter, d is the small diameter, and L is the
        length of the Morse taper socket.  n is the taper number.
        '''
        if n not in self.sizes:
            raise ValueError(self.errmsg(n))
        X = 1/16 if n else 1/32
        tpf, D, L = self.data[n]
        tpi = tpf/12    # Taper per inch in inch/inch
        d = D - (L - X)*tpi
        n = 4
        return (round(D, n), round(d, n), round(L, n))
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
        return (round(n/8, 3), round(n/10, 3), round(n/2, 3))
class BrownAndSharpe(Taper):
    def __init__(self):
        self.name = "Brown & Sharpe"
        self.super = super(BrownAndSharpe, self)
        self.super.__init__(set(range(1, 19)))
        self.data = {
            # Reference MH, 19th ed., pg 1682.
            #   [ tpf(inch), minor_dia, length]
            1  : [0.50200, 0.20000, 15/16],
            2  : [0.50200, 0.25000, 1+3/16],
            3  : [0.50200, 0.31250, 1+1/2],
            4  : [0.50240, 0.35000, 1+11/16],
            5  : [0.50160, 0.45000, 2+1/8],
            6  : [0.50329, 0.50000, 2+3/8],
            7  : [0.50147, 0.60000, 2+7/8],
            8  : [0.50100, 0.75000, 3+9/16],
            9  : [0.50085, 0.90010, 4+1/4],
            10 : [0.51612, 1.04465, 5],
            11 : [0.50100, 1.24995, 5+15/16],
            12 : [0.49973, 1.50010, 7+1/8],
            13 : [0.50020, 1.75005, 7+3/4],
            14 : [0.50000, 2.00000, 8+1/4],
            15 : [0.50000, 2.25000, 8+3/4],
            16 : [0.50000, 2.50000, 9+1/4],
            17 : [0.50000, 2.75000, 9+3/4],
            18 : [0.50000, 3.00000, 10+1/4],
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
        tpf, d, P = self.data[n]
        tpi = tpf/12
        D = d + P*tpi
        return (round(D, 4), round(d, 5), round(P, 4))
class Jacobs(Taper):
    def __init__(self):
        self.name = "Jacobs"
        self.super = super(Jacobs, self)
        sizes = set(range(7))
        sizes.add(33)
        self.super.__init__(sizes)
        self.data = {
            # Reference MH, 19th ed., pg 1690.
            0  : [0.2500, 0.22844, 0.43750],
            1  : [0.3840, 0.33341, 0.65625],
            2  : [0.5590, 0.48764, 0.87500],
            3  : [0.8110, 0.74610, 1.21875],
            4  : [1.1240, 1.03720, 1.65630],
            5  : [1.4130, 1.31610, 1.87500],
            6  : [0.6760, 0.62410, 1.00000],
            33 : [0.6240, 0.56050, 1.00000],
        }
    def __call__(self, n):
        '''Return the tuple (D, d, L) where the dimensions are in inches.
        D is the large diameter, d is the small diameter, and L is the
        length of the socket.  n is the taper number.
        '''
        if n not in self.sizes:
            raise ValueError(self.errmsg(n))
        return self.data[n]
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
        self.tpf = 1 + 3/4
        self.Bprime = {   # Length from gauge line
            200  : 5+1/8,
            250  : 5+7/8,
            300  : 6+5/8,
            350  : 7+7/16,
            400  : 8+3/16,
            450  : 9,
            500  : 9+3/4,
            600  : 11+5/16,
            800  : 14+3/8,
            1000 : 17+7/16,
            1200 : 20+1/2,
        }
    def __call__(self, n):
        '''Return the tuple (D, d, L) where the dimensions are in inches.
        D is the large diameter, d is the small diameter, and L is the
        length of the socket.  n is the taper number.
        '''
        if n not in self.sizes:
            raise ValueError(self.errmsg(n))
        D = n/100
        L = self.Bprime[n]
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
        self.tpi = 3.5/12
        self.data = {
            # A = large diameter of taper
            # C = small diameter of taper
            #        A      C
            30  : (1+1/4, 0.6885),
            40  : (1+3/4, 1.001),
            50  : (2+3/4, 1.5635),
            60  : (4+1/4, 2.376),
        }
    def __call__(self, n):
        '''Return the tuple (D, d, L) where the dimensions are in inches.
        D is the large diameter, d is the small diameter, and L is the
        length of the socket.  n is the taper number.
        '''
        if n not in self.sizes:
            raise ValueError(self.errmsg(n))
        D, d = self.data[n]
        L = (D - d)/self.tpi
        return (D, d, L)
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Introduction():
    if dbg:
        return
    names = ["  " + i for i in taper_names]
    print(dedent(f'''
    This script will print a table of step-boring dimensions for a tapered
    hole.  You'll be prompted for the following information:
        - Standard taper name and size number
            or
        - Taper large and small diameters and length
        - Clearance between the step corners and the taper (this determines the
          amount of material that would need to be reamed out after step boring
          was finished).
        - Longitudinal step size
        - Units to display the output report in
    
    The default units are inches; you can use other common length units and
    metric prefixes as desired.
    
    The allowed standard taper names are:
    {nl.join(names)}
    '''))
def RTZ(s):
    '''Replace trailing 0 characters in s with spaces but don't change the
    length of s.
    '''
    t, i, n = list(reversed(list(s))), 1, len(s)
    if t[0] == "0":
        t[0] = " "
        while t[i - 1] == " " and t[i] == "0" and i < len(t):
            t[i] = " "
            i += 1
    t = ''.join(reversed(t))
    # Remove "." if it's the last non-space character
    u = t.rstrip()
    if u[-1] == ".":
        u = u[:-1] + " "
    u += " "*(n - len(u))
    return u
def Report(opts):
    print(f"{time.asctime():^78s}")
    if opts["taper_type"] != "dimensioned":
        print(opts["taper_type"], "#" + str(opts["taper_number"]),
              "standard taper")
    print()
    D = opts["D"]   # inches
    d = opts["d"]   # inches
    L = opts["L"]   # inches
    diff = sig(D - d)
    tpi = (D - d)/L
    tpi_ = sig(tpi)
    tpf_ = sig(tpi*12)
    tps = tpi*opts["step_size"]
    tps_ = sig(tps)
    # Fill locals with desired strings to be printed
    D_ = RTZ(sig(opts["D"]))
    d_ = RTZ(sig(opts["d"]))
    L_ = RTZ(sig(opts["L"]))
    clearance = RTZ(sig(opts["clearance"]))
    step_size = RTZ(sig(opts["step_size"]))
    print(dedent(f'''
    Taper dimensions in inches:
        D = large diameter = {D_}
        d = small diameter = {d_}
        Diameter difference = {diff}
        L = length = {L_}
        Clearance = {clearance}
        Step size = {step_size}
        Taper = {tpi_} inch/inch = {tpf_} inch/foot
        Taper per step = {tps_} inch
    '''))
    # Generate report
    print(dedent(f'''
 
    The following cutting schedule starts at the deepest part of the tapered
    bore (x = 0).  First bore a hole to the small diameter above less the
    clearance (the entry under Diameter for x = 0), then move the cutting tool
    right one step and then move the cross slide out by the indicated step dy.
    Repeat until the large diameter has been cut.
                                            Total
           x         dy        Diameter       x
        -------    ------      --------    -------'''))
    ss = opts["step_size"]
    m = 0  # Number of dial indicator ranges in x so far
    clr = opts["clearance"]
    for i, x in enumerate(frange(0, L + 0.9*ss, ss)):
        m_new, remainder = divmod(x, indicator_size)
        if m_new > m and remainder:
            print("Reset dial indicator")
            m = m_new
        X = x - m*indicator_size
        a = RTZ("{:10.3f}".format(X))
        b = RTZ("{:10.4f}".format(tps)) if i else " "*10
        c = RTZ("{:12.3f}".format(d - clr + i*tps))
        e = RTZ("{:10.3f}".format(x))
        print("{} {} {} {}".format(a, b, c, e))
def GetInfo(opts):
    '''Information needed:
    Standard taper or specify by dimensions?
        Standard:  Morse, Jarno, B&S
        Dimensions:  large dia, small dia, length
    Clearance from step to actual taper
    Radial step
    Longitudinal step
    Output dimensions [inch]
    '''
    if dbg:
        opts["taper_type"] = "Morse"
        opts["taper_number"] = 3
        opts["clearance"] = 0.002
        opts["clearance_input"] = ""
        opts["step_size"] = 0.1
        opts["step_size_input"] = ""
        T = Morse()
        D, d, L = T(opts["taper_number"])
        opts["D"] = D
        opts["D_input"] = str(D) + " in"
        opts["d"] = d
        opts["d_input"] = str(d) + " in"
        opts["L"] = L
        opts["L_input"] = str(L) + " in"
        return
    p = "Standard taper (1) or specified by dimensions (2)? "
    taper = GetNumber(p, numtype=int, default=1, low=1, high=2)
    opts["taper_type"] = "standard" if taper == 1 else "dimensioned"
    if 1:
        # Get taper type or dimensions
        if opts["taper_type"] == "standard":
            # Morse, Jarno, etc.
            print("Choose a taper type:")
            bd = bidict()
            for i, name in enumerate(taper_names):
                print("  {}) {}".format(i + 1, name))
                bd[i] = name
            morse = bd("Morse") + 1
            ok = False
            while not ok:
                try:
                    choice = GetNumber("?", default=morse, numtype=int,
                                       low=1, high=len(taper_names))
                    choice -= 1
                    ok = True
                except ValueError:
                    print("You must select one of the numbers.")
            opts["taper_type"] = taper_name = taper_names[choice]
            # Instantiate a taper object
            T = taper_objects[choice]()
            # Get taper number
            tapers = sorted(T.sizes)
            t = ' '.join([str(i) for i in tapers])
            ok, number = False, -1
            while number not in tapers:
                print('''Select a {} taper number from the following list:
      {}'''.format(taper_name, t))
                choice = input("? ")
                if choice.lower() == "q":
                    exit(0)
                try:
                    number = int(choice)
                except ValueError:
                    print("'{}' is not a valid number".format(choice))
            opts["taper_number"] = number
            # Convert to dimensions D, d, and L in inches
            D, d, L = T(number)
        else:
            # Dimensioned
            # Get D in inches
            p = "What is large diameter? "
            value, unit = GetNumber(p, low=0, low_open=True, use_unit=True)
            unit = unit if unit else "in"
            D = value*u(unit)/u("inch")
            opts["D_input"] = (sig(value) + " " + unit).strip()
            # Get d in inches
            p = "What is small diameter? "
            while True:
                print(p, end="")
                answer = input()
                if answer.strip().lower() == "q":
                    exit(0)
                value, unit = ParseUnit(answer)
                # Note value is a string
                opts["d_input"] = (value + " " + unit).strip()
                d = float(value)*u(unit)/u("inch")
                if d <= 0:
                    print("Diameter must be > 0")
                elif d >= D:
                    print("Diameter must be < {}".format(opts["D input"]))
                else:
                    break
            # Get L in inches
            p = "What is length? "
            value, unit = GetNumber(p, low=0, low_open=True, use_unit=True)
            unit = unit if unit else "in"
            L = value*u(unit)/u("inch")
            opts["L_input"] = (sig(value) + " " + unit).strip()
    opts["D"] = D
    opts["d"] = d
    opts["L"] = L
    # Get clearance from step corner to taper
    p = "What is clearance from step corner to taper? "
    value, unit = GetNumber(p, low=0, use_unit=True, default=0.005)
    unit = unit if unit else "in"
    opts["clearance"] = value*u(unit)/u("inch")
    opts["clearance_input"] = (sig(value) + " " + unit).strip()
    # Get (longitudinal) step size
    p = "What is longitudinal step size? "
    value, unit = GetNumber(p, low=0, low_open=True, use_unit=True,
                            default=0.1)
    unit = unit if unit else "in"
    opts["step_size"] = value*u(unit)/u("inch")
    opts["step_size_input"] = (sig(value) + " " + unit).strip()
    print()
if __name__ == "__main__":
    taper_names = ("Brown & Sharpe", "Jacobs", "Jarno", "Morse", "Sellers")
    taper_objects = (BrownAndSharpe, Jacobs, Jarno, Morse, Sellers)
    opts = {}   # Options & data
    sig.digits = 4
    sig.rtz = True
    Introduction()
    GetInfo(opts)
    Report(opts)
