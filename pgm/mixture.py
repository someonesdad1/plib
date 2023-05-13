'''
Program to calculate mixtures
    Modeled after a C program by Marv Klotz.

13 May 2023:  Turn into a more general tool

- Problem variables
    - C = concentration []
    - V = volume [L³]
    - S = solute [L³]
    - T = solvent [L³]
- Equations
    - V = S + T
    - C = S/V
- Relations from equations
    - C = S/V = 1 - T/V
    - V = S + T = T/(1 - C)
    - S = C*V = V - T
    - T = V - S = V*(1 - C)
- Relations in terms of variables
    - C(S, V) = C(T, V)
    - V(S, T) = V(C, T)
    - S(C, V) = S(T, V)
    - T(S, V) = T(C, V)

- Numerical check:  S = 1, T = 3, V = 4, C = 1/4
- Problem statements
    - Problem 1a
        - Single solvent and solute.  Solutions A and B with different
          concentrations are mixed.  What are the characteristics of the
          mixture?
    - Problem 1b
        - Same as 1b, but multiple solutions A, B, C, ...
    - Problem 2
        - Single solvent, multiple solutes.  Solutions A, B, etc. with
          different concentrations are mixed.  What are the characteristics
          of the mixture?

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
    # Calculate mixture concentrations
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    import pathlib
    from functools import partial
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from get import GetNumber
    from f import flt
    from color import C
if 1:   # Global variables
    Get = partial(GetNumber, num_type=flt, low=0)
    class g:
        pass
    g.VolA = flt(0)
    g.VolB = flt(0)
    g.VolMixture = flt(0)
    g.ConcA = flt(0)
    g.ConcB = flt(0)
    g.ConcMixture = flt(0)
def ParseCommandLine(d):
    d["-d"] = 3         # Number of significant digits
    d["-g"] = False     # Turn on debug printing
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:h")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list(""):
            d[o] = not d[o]
        elif o in ("-d",):
            try:
                d["-d"] = int(a)
                if not (1 <= d["-d"] <= 15):
                    raise ValueError()
            except ValueError:
                msg = ("-d option's argument must be an integer between "
                    "1 and 15")
                print(msg, file=sys.stderr)
                exit(1)
        elif o in ("-h", "--help"):
            ShowFormulas()
    flt(0).N = d["-d"]
    return args
def ShowFormulas():
    print(dedent('''
    This script calculates the concentration of a solution gotten by mixing
    two volumes of solutions of differing concentrations.

    Assumptions:
        - The solute in both solutions A and B are the same.
        - One or both solutions can be pure solvent.
        - The solute and solvent are miscible and are mixed well.
        - There are no volume or temperature changes when the solutions are
          mixed.
        - Works best for dilute solutions.
        - The concentration fractions are volume fractions.  This means
          both the solvent and solute are liquids (example:  water and
          antifreeze for your car).
    
    Symbols:
        C = concentration fraction
        V = volume
    
    The six variables in the problem are thus:
        Solution A:  Ca, Va
        Solution B:  Cb, Vb
        Mixture:     C, V
    
    Solution A has a solute volume of Ca*Va.
    Solution B has a solute volume of Cb*Vb.
    
    After mixing, the resulting solution has a solute volume faction of
    
        C = (Ca*Va + Cb*Vb)/V
    
    where the volume is
    
        V = Va + Vb
    
    Note that this formulation is an approximation; real solutions sometimes
    don't satisfy the above assumptions.  Example:  ethanol and water mixed
    together will have a lower volume than their component sum because the
    water and ethanol molecules "interlock" somewhat because of close-range
    polar electrical forces.
    
    You can check the following cases for reasonableness:
        - Mix two unit-volume solutions of 0% concentration to get 2 units
          of volume of 0% concentration.
        - Mix two unit-volume solutions of 100% concentration to get a 100%
          volume of 2 units.
        - Mix one unit volume of p% concentration and one unit volume of 0%
          concentration to get 2 units of (p/2)% concentration.

    Here's a numerical example that can be used as a check case.  I have a
    weed killer with a concentration of 11.3%.  I want to mix it
    with water to get 15 gallons, the volume of my sprayer's tank.  The 
    target mixture concentration for application is 0.25%.  What volume of
    the 11.3% solution should I mix with water to get the desired 15
    gallons of 0.25% solution?

    This needs to be solved by iteration, but since it's a dilute solution,
    we'll probably get close enough on the first pass.  I'll suppose that
    the water volume I use is 14.75 gallons, as the typical bottled
    concentrate comes in 1/4th gallon (1 quart) containers.  Here are the 
    entered values and results:

        Concentration of solution A in %? [0] 11.3
        Concentration of solution B in %? [0] 0

      Enter two of:  volume A, volume B, mixture volume, mixture
      concentration.  Press return if not known.  Expressions are allowed and
      the math module is in scope.

        Volume of solution A? [0]
        Volume of solution B? [0] 14.75
        Volume of mixture? [0]
        Concentration of mixture in %? [0] 0.25

      Results:
          Solution            Volume            Concentration %
          --------        --------------        ---------------
             A                0.3337                 11.3
             B                14.75                   0
          Mixture             15.08                  0.25

    0.3337 gallons is 0.3337/0.25 = 1.33 bottles of concentrate.  No
    further iteration is necessary, as this is more than adequate for yard
    weed spraying.

    '''))
    exit(0)
def GetData():
    # Set all numbers to 0
    g.ConcA = g.ConcB = flt(0)
    g.VolA = g.VolB = g.VolMixture = g.ConcMixture = flt(0)
    #
    if 0:
        print(dedent(f'''
        Script is {pathlib.Path(sys.argv[0]).resolve()}

        Calculate the resulting concentration of a solution gotten by mixing
        two solutions of differing concentrations.  Use -h on the command line
        to see the formulas used.  Use -d to set the number of significant
        digits (defaults to {d["-d"]}).

        '''))
    print(dedent('''
    Specify concentrations of both solutions.  If one solution is a
    dilutant (e.g., pure water), enter its concentration as 0%.

    '''))
    g.ConcA = Get("  Concentration of solution A in %? ", high=100, default=0)
    g.ConcB = Get("  Concentration of solution B in %? ", high=100, default=0)
    print(dedent('''

    Enter two of:  volume A, volume B, mixture volume, mixture
    concentration.  Press return if not known.  Expressions are allowed and
    the math module is in scope.

    '''))
    data_items_entered = 0
    while True:
        g.VolA = Get("  Volume of solution A? ", default=g.VolA)
        if g.VolA:
            data_items_entered += 1
        g.VolB = Get("  Volume of solution B? ", default=g.VolB)
        if g.VolB:
            data_items_entered += 1
        if data_items_entered != 2:
            g.VolMixture = Get("  Volume of mixture? ", default=g.VolMixture)
            if g.VolMixture:
                data_items_entered += 1
            if data_items_entered != 2:
                g.ConcMixture = Get("  Concentration of mixture in %? ",
                                    high=100, default=g.ConcMixture)
                if g.ConcMixture:
                    data_items_entered += 1
                if data_items_entered != 2:
                    print("Insufficient data.  Try again.")
                break
            else:
                break
        else:
            break
    if d["-g"]:
        print(dedent(f'''

        {C.lcyn}Entered data:
            VolA            {g.VolA!r}
            VolB            {g.VolB!r}
            VolMixture      {g.VolMixture!r}
            ConcA           {g.ConcA!r}
            ConcB           {g.ConcB!r}
            ConcMixture     {g.ConcMixture!r}{C.norm}'''))
def PrintResults():
    pa, pb, pm = g.ConcA/flt(100), g.ConcB/flt(100), g.ConcMixture/flt(100)
    if g.VolA and g.VolB:
        g.VolMixture = flt(g.VolA + g.VolB)
        g.ConcMixture = flt(100*(g.VolA*pa + g.VolB*pb)/(g.VolA + g.VolB))
    elif g.VolA and g.ConcMixture:
        g.VolMixture = flt(g.VolA*(pa - pb)/(pm - pb))
        g.VolB = flt(g.VolMixture - g.VolA)
    elif g.VolA and g.VolMixture:
        g.VolB = flt(g.VolMixture - g.VolA)
        g.ConcMixture = flt(100*(g.VolA*pa + g.VolB*pb)/(g.VolA + g.VolB))
    elif g.VolB and g.ConcMixture:
        g.VolMixture = flt(g.VolB*(pb - pa)/(pm - pa))
        g.VolA = flt(g.VolMixture - g.VolB)
    elif g.VolB and g.VolMixture:
        g.VolA = flt(g.VolMixture - g.VolB)
        g.ConcMixture = flt(100*(g.VolA*pa + g.VolB*pb)/g.VolMixture)
    elif g.VolMixture and g.ConcMixture:
        g.VolA = flt(g.VolMixture*(pm - pb)/(pa - pb))
        g.VolB = flt(g.VolMixture - g.VolA)
    else:
        print("Not enough information")
        exit(1)
    # Print results
    n, k, s = 8, 14, " "*8
    print(dedent(f'''
    
    Results:
        Solution            Volume            Concentration %
        --------        --------------        ---------------
        {"A":^{n}s}{s}{g.VolA!s:^{k}s}{s}{g.ConcA!s:^{k}s}
        {"B":^{n}s}{s}{g.VolB!s:^{k}s}{s}{g.ConcB!s:^{k}s}
        {"Mixture":^{n}s}{s}{g.VolMixture!s:^{k}s}{s}{g.ConcMixture!s:^{k}s}
    '''))

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if 0:
        # Custom data for a test case:  0.188% concentration
        g.ConcA = flt(0.113)
        g.ConcB = flt(0)
        g.VolA = 0.25
        g.VolB = 14.75
    else:
        GetData()
    PrintResults()
