'''
Print out wood properties for "2 by" materials

Add -b option to select size, then print out beam properties including
critical load for buckling and tension/compression stress
'''
 
# Copyright (C) 2020 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Academic Free License version 3.0.
# See http://opensource.org/licenses/AFL-3.0.
#
 
if 1:   # Imports & globals
    import getopt
    import os
    import sys
    from math import sqrt, pi
    import textwrap as tw
    # Custom libraries
    from sig import sig
    import u

    # Try to import the color.py module; if not available, the script
    # should still work (you'll just get uncolored output).
    try:
        import color as C
        _have_color = True
    except ImportError:
        # Make a dummy color object to swallow function calls
        class Dummy:
            def fg(self, *p, **kw): pass
            def normal(self, *p, **kw): pass
            def __getattr__(self, name): pass
        C = Dummy()
        _have_color = False


    # Debugging stuff
    from pdb import set_trace as xx
    if 0:
        import debug
        debug.SetDebugger()  # Start debugger on unhandled exception

sizes = {
    #      width, height
    "2x2": [1.5, 1.5],
    "2x4": [1.5, 3.75],
    "2x6": [1.5, 5.5],
    "2x8": [1.5, 7.25],
    "2x10": [1.5, 9.25],
    "2x12": [1.5, 11.25],
}
more_sizes = {
    "4x4": [3.5, 3.5],
    "4x6": [3.5, 5.5],
    "4x8": [3.5, 7.25],
    "4x10": [3.5, 9.25],
    "4x12": [3.5, 11.25],
}

# The source for this modulus of rupture is page 4-12 of Chapter 4,
# "Mechanical Properties of Wood" by D. Green, J. Winandy, and D.
# Kretschmann (found on the web).
modulus_of_rupture_psi = 12e3
# Used to flag where color printing is needed
max_bending_stress_exceeded = False

def GetSize(s):
    'Return linear dimensions of beam'
    b, d = sizes[s]
    if opt["-l"]:
        b, d = d, b
    return b, d

def A(s):
    'Area in square inches'
    b, d = GetSize(s)
    return b*d

def I(s):
    'Moment of inertia in in4'
    b, d = GetSize(s)
    return b*d**3/12

def y(s):
    'Distance to neutral axis in inches'
    b, d = GetSize(s)
    return d/2

def Z(s):
    'Section modulus = I/y in in3'
    b, d = GetSize(s)
    return I(s)/y(s)

def k(s):
    'Radius of gyration in inches'
    b, d = GetSize(s)
    return d/sqrt(12)

def m(s):
    'Linear mass density in lbm/in'
    b, d = GetSize(s)
    return b*d*d["rho"]

def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)

def Usage(d, status=1):
    name = sys.argv[0]
    P(f'''
    Usage:  {name} [options] [length load]
      Print deflection and stress properties for beams from common Douglas
      fir wood commonly used in the US of the given length and uniform load.
      You can include common unit abbreviations with the numbers with no
      separating space (example: 12ft).  If no arguments are given, a table
      of properties is printed (use -f to include formulas).  
 
      The results are printed to {opt["-d"]} significant figures.  Formulas are from
      the 19th edition of Machinery's Handbook.

      The wide side of the beam is vertical with the load normal to
      the short side's surface.  To make the load normal to the wide
      side, use the -l option.
 
    Options:
      -c      Beam load is concentrated at one point
      -d n    Number of significant figures
      -e      Show some design examples
      -f      Include beam formulas when printing table
      -l      Load applied to wide side
      -m      Include more board sizes
      -s S    Specify the rupture stress in psi (S can be an expression)
      -t      Print table of beam properties
    '''[1:].rstrip())
    exit(status)

def ParseCommandLine(opt):
    global modulus_of_rupture_psi, sizes
    opt["-c"] = False     # Concentrated load
    opt["-d"] = 2         # Number of significant digits
    opt["-e"] = False     # Show design examples
    opt["-f"] = False     # Include beam formulas
    opt["-l"] = False     # Neutral axis parallel to long axis
    opt["-m"] = False     # Include more board sizes
    opt["-t"] = False     # Print table
    opt["-s"] = modulus_of_rupture_psi   # Allowed stress
    try:
        opts, args = getopt.getopt(sys.argv[1:], "cd:efhlms:t")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("ceflt"):
            opt[o] = not opt[o]
        elif o in ("-d",):
            try:
                opt["-d"] = int(a)
                if not (1 <= opt["-d"] <= 15):
                    raise ValueError()
            except ValueError:
                msg = ("-d option's argument must be an integer between "
                       "1 and 15")
                Error(msg)
        elif o in ("-m",):
            for key, item in more_sizes.items():
                sizes[key] = item
        elif o in ("-s",):
            opt["-s"] = eval(a)
            if opt["-s"] <= 0:
                Error("Maximum stress must be > 0")
            modulus_of_rupture_psi = opt["-s"]
        elif o in ("-h", "--help"):
            Usage(opt, status=0)
    sig.digits = opt["-d"]
    if opt["-e"]:
        DesignExamples()
    if opt["-t"]:
        PrintTable()
    if not args or len(args) != 2:
        Usage(opt)
    return args

def DesignExamples():
    'Show examples of different designs'
    P(f'''
    Design examples

    * Standing on a 2x4

      This is intended to give a feel for the reasonableness of the
      program's predictions.  If I support an 8 foot long 2x4 on two
      ladders (e.g., a scaffold) and I weigh 180 lbf, what will be the
      deflection and stress if I stand on the long edge in the middle
      of the board?

      Method of solution:  Look for the data under the "Supported"
      column.  The arguments are "-c -l 8ft 180lbf".

      Answer:  The beam deflects 1.2 inches under where I stand and the
      stress is about half of the rupture value.  You can increase the
      load to find that rupture will occur at about 350 pounds with 3.2
      inches of deflection.  I might be able to break the board by
      jumping up and down on it.

      A 2x12 is roughly 3 times wider and both the deflection and stress
      are about 3 times less.

    * Sawhorse

      A 4 foot long 2x6 is used to make a sawhorse beam.  What is the
      maximum load for this beam if the ends are fixed?

      Method of solution:  find the load that results in the rupture
      stress allowed under the "Fixed" results.  Invoke with the
      arguments "4ft X" where X is the load value until the 2x6 entry
      for s under "Fixed" is > {modulus_of_rupture_psi} psi.  Compare
      the uniformly loaded value to the concentrated value by using the
      -c option. 

      Answers:  About 45 klbf for a uniform load and a third of this for
      the concentrated load.

    * Scaffold beam

      I need to stand on a scaffold beam that is 16 feet between supports.
      If my equipment and I weigh 250 lbf and I stand in the center of the
      beam, what wood width should I use to not exceed the maximum allowed
      wood bending stress of {modulus_of_rupture_psi/2} psi?

      Method of solution:  The load is concentrated at the center, so use
      the -c option.  Here, you also need to use the -l option because
      you'll be standing on the long side of the beam.  We need to
      specify the modulus of rupture to be 6500 psi, so the -s option is
      used.  The arguments are "-c -l -s 6500 16ft 250lbf".

      Answer:  A 2x12 is needed to get a factor of safety of about 2.  A
      2x10 could probably be used too because its stress is about 5%
      over the desired stress.  The beam could be made safer by screwing
      e.g. a 2x6 to the bottom of the 2x10 or 2x12 to make a beam with a
      T shape because this increases the moment of inertia.

      A factor of safety of 2 is fine if you know what you're doing,
      know the scaffold board is in good shape, and you know the load on
      the scaffold.  Because these assumptions usually aren't true for
      laborers, a factor of safety for scaffold design might be 4 or
      higher.

    * Cantilever

      I want to support load F on a beam A parallel to a wall and with
      two identical cantilever beams B and C fixed to the wall
      supporting the ends of beam A; the ends of beam A are screwed to
      then ends of beams B and C, so beam A's ends are fixed.  The load
      is concentrated in the center of beam A.  What beam sizes should I
      use?  Suppose 

          F = 500 lbf
          Beam A length = 10 ft
          Beam B and C lengths = 6 ft

      Method of solution:  There are two separate problems.  First, you
      need to determine the size of beam A.  This is done as in the
      scaffold problem above with the arguments "-l -c 10ft 500".
      Under the "Fixed" column, we'd pick the 2x4.

      Second, the load on each cantilevered beam will be half the force
      F or 250 lbf plus the weight of the 2x4 which is 12 lbf.  Use the
      arguments "-c 6ft 262" and the "Cantilevered" stress value will be
      acceptable if you use a 2x4.  The load must be on the short side
      of the beam.

      Note:  If this were a permanent structure, you might want to use
      the 10-year design stress levels which are on the order of
      one-tenth the rupture stress.  Aiming for around 1200 psi stress,
      you'd choose a 2x12 for beam A and a 2x8 for beams B and C.
    '''[1:].rstrip())
    exit(0)

def BeamFormulas():
    P(f'''
    The approximate static bending stress at which Douglas fir will break
    ("modulus of rupture") is {sig(modulus_of_rupture_psi/1000, 2)} kpsi.  The 10 year maximum design stress is
    typically about an order of magnitude less.
 
    Beam formulas (from Machinery's Handbook, 19th ed., 1971)
       F = load in lbf
       d = beam height, inches
       b = beam width, inches
       L = beam length, inches
       y = maximum deflection of beam, inches
       s = maximum beam stress in psi (psi = lbf/inches**2)
       E = modulus of elasticity = {opt["E"]:.1e} psi for Douglas fir
       I = moment of inertia = b*d**3/12 inches**4
       Z = section modulus = I/Y = b*d**2/6 inches**3
       Y = distance to neutral axis = d/2 inches

       Note:   y is proportional to α and s is proportional to β
       α = F*L**3/(E*I)
       β = F*L/Z
                       b
                   +-------+
                   |       |
                   |       |
                   |       |
                 d |-------| -----
                   |       |   ^
                   |       |   Y
                   |       |   v
                   +-------+ -----

    Uniform load
      Fixed at both ends
          y = α/384
          s = β/24
      Supported at both ends
          y = α*5/384
          s = β/8
      Cantilevered (fixed at one end)
          y = α/8
          s = β/2
    Load concentrated at one point
      Fixed at both ends, load at center
          y = α/192
          s = β/8
      Supported at both ends, load at center
          y = α*5/384
          s = β/2
      Cantilevered (fixed at one end), load at unsupported end
          y = α/3
          s = β
    '''[:-1].rstrip())

def PrintTable():
    we = "long" if opt["-l"] else "short"
    na = f"Neutral axis parallel to {we} edge\n"
    P(f'''
    Table of Douglas fir lumber 
    Specific gravity = {opt["spgr"]}, density = {opt["density"]:.3g} lbm/cubic inch
    {na}
          Width,  Height,  Mass,    A,       I,      Y,      Z,      k,
    Size    in      in    lbm/in   in2      in4      in     in3      in
    ----  ------  ------  ------  ------  -------  -----  -------  -----'''[1:])
    for sz in sizes:
        b, d = w, h = GetSize(sz)
        A = b*d
        Y = d/2
        lmd = A*opt["density"]
        I = b*d**3/12
        Z = b*d**2/6
        k = d/sqrt(12)
        # Nominal size, inches
        print(f"{sz:4s}", end="")
        # Width, inches
        print(f"{str(w):>7s}", end="")
        # Height, inches
        print(f"{str(h):>9s}", end="")
        # Linear mass density lbm/inch
        print(f"{sig(lmd):>8s}", end="")
        # Area in inch**2
        print(f"{sig(A):>8s}", end="")
        # Moment of inertia in inch**4
        print(f"{sig(I):>9s}", end="")
        # Neutral axis in inches
        print(f"{sig(Y):>7s}", end="")
        # Section modulus in inch**3
        print(f"{sig(Z):>9s}", end="")
        # Radius of gyration in inches
        print(f"{sig(k):>7s}")
    print()
    P(f'''
      A = cross-sectional area
      I = moment of inertia
      Y = location of neutral axis from {we} edge
      Z = section modulus
      k = radius of gyration
    '''[1:].rstrip())
    if opt["-f"]:
        BeamFormulas()
    exit(0)

def P(s):
    'Print s but first remove leading 4 spaces'
    for line in s.split("\n"):
        print(line[4:])

def PrintBeamReport(L, F):
    'Length L in inches, load F in lbf'
    global max_bending_stress_exceeded
    max_bending_stress_exceeded = False
    def PI(y, s):
        # Deflection y
        print(f"{sig(y):^9s} ", end="")
        # Stress s
        if s > modulus_of_rupture_psi:
            global max_bending_stress_exceeded
            max_bending_stress_exceeded = True
            C.fg(C.lred)
        print(f"{sig(s):^9s}  ", end="")
        if s > modulus_of_rupture_psi:
            C.normal()
    s = "concentrated" if opt["-c"] else "uniform"
    P(f'''
    Loaded beam results for Douglas fir
      Specific gravity = {opt["spgr"]}, density = {opt["density"]:.3g} lbm/cubic inch
      Modulus of elasticity = {sig(opt["E"]/1e6)} Mpsi
      Length = {sig(L)} inches = {sig(L/12)} feet = {sig(L/39.37)} m
      Load   = {sig(F)} lbf ({s})
      y      = maximum deflection in inches
      s      = maximum stress in psi
    '''[1:].rstrip())
    if opt["-c"]:
        print("Beam configurations (load is concentrated at one point):")
        P(f'''
      Fixed           Fixed at both ends, load at center
      Supported       Supported at both ends, load at center
      Cantilevered    Fixed at one end, load at unsupported end'''[1:])
    else:
        print("Beam configurations (beam has a uniform load and is horizontal):")
        P(f'''
      Fixed           Fixed at both ends
      Supported       Supported at both ends
      Cantilevered    Fixed at one end'''[1:])
    # We'll explicitly indicate the Douglas fir rupture stress if it is equal
    # to 1.2e4 psi; otherwise, it's the "maximum allowed stress".
    sl = "Rupture stress" if opt["-s"] == 1.2e4 else "Maximum allowed stress"
    P(f'''    {sl} = {sig(opt["-s"]/1000)} kpsi, weight of board is ignored
    Colored output means stress is larger than maximum allowed. 

          Mass          Fixed              Supported          Cantilevered
           lb      y, in    s, psi      y, in    s, psi      y, in    s, psi
          -----  --------- ---------  --------- ---------  --------- ---------
    '''.rstrip())
    for i in sizes:
        print(f"{i:6s}", end="")
        b, d = w, h = GetSize(i)
        Y = d/2
        A = w*h
        m = A*L*opt["density"]
        I = b*d**3/12   # Moment of inertia in in**4
        Z = I/Y         # Section modulus in in**3
        # Mass in lb
        print(f"{sig(m):>5s}  ", end="")
        α = F*L**3/(opt["E"]*I)
        β = F*L/Z
        if opt["-c"]:   # Load is concentrated
            # Fixed
            y = α/192
            s = β/8                                                           
            PI(y, s)
            # Supported
            y = 5*α/384
            s = β/2
            PI(y, s)
            # Cantilevered
            y = α/3
            s = β
            PI(y, s)
        else:   # Uniform load
            # Fixed
            y = α/384
            s = β/24
            PI(y, s)
            # Supported
            y = 5*α/384
            s = β/8
            PI(y, s)
            # Cantilevered
            y = α/8
            s = β/2
            PI(y, s)
        print()
    # Print critical buckling load and tension/compressive stress
    P(f'''    
    Column characteristics
 
          Compression   Critical force
              psi       buckling, klbf
          -----------  ---------------
    '''.rstrip())
    for i in sizes:
        print(f"{i:6s}", end="")
        b, d = GetSize(i)
        I = b*d**3/12   # Moment of inertia in in**4
        Fcrit = 4*pi**2*opt["E"]*I/(L**2*1000)
        Comp = F/(b*d)
        print(f"{sig(Comp):^11s} ", end="")
        print(f"{sig(Fcrit):^17s} ")

if __name__ == "__main__":
    # Note:  all calculations are done in inches and lbm
    opt = { # Options dictionary
        "spgr": 0.48,           # Douglas fir specific gravity
        "E": 1.7e6,             # Modulus of elasticity in psi
        "-s": 12000,            # Rupture stress for Douglas fir
    }
    # Calculate Douglas fir density in lbm/in3
    opt["density"] = opt["spgr"]*0.0361
    args = ParseCommandLine(opt)
    value, unit = u.ParseUnit(args[0])
    x = float(value)
    L = x*u.u(unit)/u.u("inch") if unit else x
    value, unit = u.ParseUnit(args[1])
    x = float(value)
    F = x*u.u(unit)/u.u("lbf") if unit else x
    PrintBeamReport(L, F)
