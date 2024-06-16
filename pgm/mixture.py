'''

TODO
    - Change to a datafile format
        - Get rid of prompting stuff
        - You then define variables c1, c2, c, v1, v2, v 
        - concentrations can be plain or have % appended
        - conc_unit = "%" or "" (used in output report)
        - vol_unit = "xxxx" 
        - Input data are printed, then report of results is given
    - 
    - Allow calculations via either mass or volume basis
        - -v is volume basis (default)
        - -m is mass basis
        - Or use 'basis = "mass"' in datafile
    - Allow specification of volume units and use of common ones
    - Use the u library so various units can be used
        - The -u option lets you specify the output volume unit
    - Allow command line to be e.g.  " 'c1 = 11.2%' 'c2 = 0' 'v  = 15 gal'
      'c = 0.25%' " and the other variables would be solved for.  You can
      give concentration in % or as a number which must be on [0, 1].
    - With no command line arguments, you're prompted for the quantities
 
- The basic problem variables are
    - a and b are the two solutions, m is the mixture
    - c1, c2, c = concentrations (fractions on [0, 1])
    - v1, v2, v  = volumes
    - Equations
        - v = v1 + v2
        - c = (c1*v1 + c2*v2)/v 
    - There are 6 variables with 2 equations, so there will be 4 variables
      that will need to be given for a solution.
    - The fundamental assumption is that the volumes don't change when you
      mix the solutions.  This can be a reasonable approximation for dilute
      solutions.


    Typical problems

        - Have 0.41 mixture of glyphosate.  Want to mix with water to get 0.02 solution and get v 
          of this amount.  Variables are
            - v = 15 gallons for our sprayer
            - c = 0.02     Desired mixture concentration
            - c1 = 0.41     Bottled glyphosate solution
            - c2 = 0        Concentration of water

              Here, v  = 15 gallons for our sprayer.  The solution b is water, so its
              concentration is c2 = 0.  Therefore v*c = v1*c1 or 15(0.02) = v1(0.42), giving
              that v1 = 15(0.02)/0.42 = 0.7143 gallons.  v2 = v  - v1 = 15 - 0.7143 = 14.3
              gallons.

            - *** WRONG ***   The solution to this problem given in the manual is 2-2/3 floz of
              solution to make 1 gallon of water.  This is 2.667/(128 - 2.667) = 2.13% since 1
              gallon is 128 floz..
            - Do for 1 gallon:  
                - v = 128 floz
                - c = 0.02     Desired mixture concentration
                - c1 = 0.41     Bottled glyphosate solution
                - c2 = 0        Concentration of water

                    v*c = v1*c1 + v2*c2 = 128*0.02 = v1*0.41
                    So 0.41*v1 = 2.56 giving v1 = 6.24 floz
                    v2 = 128 - 6.24 = 121.8 floz


---------------------------------------------------------------------------
 
Program to calculate mixtures
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
        # Calculate mixture concentrations
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Imports
        import sys
        import getopt
        from pathlib import Path as P
        import time
        from functools import partial
        from pprint import pprint as pp
    if 1:   # Custom imports
        from wrap import dedent
        from get import GetNumber, GetLines
        from f import flt
        from u import u
        from color import t
        from lwtest import Assert
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        Get = partial(GetNumber, num_type=flt, low=0)
        class g:
            pass
        g.Vol1 = flt(0)
        g.Vol2 = flt(0)
        g.VolMixture = flt(0)
        g.Conc1 = flt(0)
        g.Conc2 = flt(0)
        g.ConcMixture = flt(0)
        t.unk = t("ornl")
        t.c1, t.c2, t.c, t.v1, t.v2, t.v  = [""]*6
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(d):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [dilution_file]
          Solve a dilution problem whose definition is in dilution_file.  Use '-' to read the
          contents from stdin.  The variables are
            c1      Solution 1 concentration in %
            c2      Solution 2 concentration in %
            c       Mixture concentration in %
            v1      Solution 1 volume
            v2      Solution 2 volume
            v       Mixture volume
          The equations solved are
            v = v1 + v2
            c*v = c1*v1 + c2*v2
        Options
            -c      Print a sample datafile
            -d n    Number of figures to display
            -H      Show manpage
            -h      Show this help
            -i      Interactively solve the problem
        '''))
        exit(0)
    def ParseCommandLine(d):
        d["-c"] = False     # Print sample datafile
        d["-d"] = 3         # Number of significant digits
        d["-g"] = False     # Debug printing
        d["-i"] = False     # Interactive solution
        try:
            opts, args = getopt.getopt(sys.argv[1:], "cd:gHhi")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cgi"):
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
            elif o == "-h":
                Usage(d)
            elif o == "-H":
                Manpage(d)
        flt(0).N = d["-d"]
        if d["-c"]:
            PrintSampleDatafile()
            exit()
        elif d["-i"]:
            # Interactive solution
            GetData()
            PrintResults()
            exit(0)
        if not args:
            Usage(d)
        return args
    def Manpage(d):
        print(dedent('''
        
        This script calculates the concentration of a solution gotten by mixing two volumes of
        solutions of differing concentrations.  The solute is the solution that is diluted by
        adding solvent.  Examples:
        
            - A concentrated weed killer solution is the solute and the solvent is water.
            - The most general problem is mixing two different solutions of the same solvent and
              solute.  If you had a 30% solution of antifreeze in you car's radiator and wanted a
              50% solution and you have an 80% solution on-hand, then this script will tell you
              how much 80% solution to add to get the desired 50% solution.
        
        Symbols:
            c = concentration volume fraction in percent
            v = volume of solute + solvent
        
        The six variables in the problem are thus:
            Solution 1:  c1, v1
            Solution 2:  c2, v2
            Mixture:     c, v
        
        Solution A has a solute volume of c1*v1.
        Solution B has a solute volume of c2*v2.
        
        After mixing, the resulting mixture has a solute volume faction of
        
            c = (c1*v1 + c2*v2)/v 
        
        where the volume is
        
            v  = v1 + v2
        
        Assumptions:
            - The solute in both solutions 1 and 2 are the same
            - One or both solutions can be pure solvent
            - The solute and solvent are miscible and are mixed well
            - No volume or temperature changes occur when the solutions are mixed
            - Works best for dilute solutions
            - The concentration fractions are volume fractions.  This means both the solvent and
              solute are liquids.
        
        Note that this formulation is an approximation; real solutions sometimes don't satisfy the
        above assumptions.  Example:  ethanol and water mixed together will have a lower volume
        than their component sum because the water and ethanol molecules "interlock" somewhat
        because of close-range polar electrical forces.

        If you use the datafile approach to solve the problem, the calculation is a little more
        convenient because you can specify the unit used for the volumes used in the report.  Use
        the -c option to print a sample datafile and supply the known variables.  The u() function
        accepts commonly-used volume units.
        
        You can check the following cases for reasonableness:
            - Mix two unit-volume solutions of 0% concentration to get 2 units of volume of 0%
              concentration.
            - Mix two unit-volume solutions of 100% concentration to get a 100% volume of 2 units.
            - Mix one unit volume of p% concentration and one unit volume of 0% concentration to
              get 2 units of (p/2)% concentration.
        
        Weed killer example
        -------------------
            I have a weed killer with a concentration of 11.3%.  I want to mix it with water to
            get 15 gallons, the volume of my sprayer's tank.  The target mixture concentration for
            application is 0.25%.  What volume of the 11.3% solution should I mix with water to
            get the desired 15 gallons of 0.25% solution?
            
            Here are the entered values and results:
            
                Concentration of solution 1 in %? [0] 11.3
                Concentration of solution 2 in %? [0] 0
            
            Enter two of:  volume 1, volume 2, mixture volume, mixture concentration.  Press return
            if not known.  Expressions are allowed and the math module is in scope.
            
                Volume of solution 1? [0]
                Volume of solution 2? [0]
                Volume of mixture? 15
                Concentration of mixture in %? [0] 0.25
            
            Results:
                Solution            Volume            Concentration %
                --------        --------------        ---------------
                    1                0.332                  11.3
                    2                 14.7                   0
                Mixture              15                   0.25
            
            Note I assumed gallons for volumes.  The bottle of concentrate is 1 quart or 32 fl oz,
            which is 1/4 gallon.  Thus, I need to add 0.332/0.25 or 4(0.332) = 1.33 bottles to the
            tank and fill it up to the 15 gallon level.
        
        Antifreeze example
        -------------------
        
            I have an 80% solution of antifreeze solution on hand (it's diluted with water).  I
            estimate my car's radiator holds 15 liters of solution.  I used a refractometer to
            measure the antifreeze solution in the car at 30%.  I want it to be a 50% solution for
            the proper winter protection where I live.  How much should I drain from the radiator
            of the 30% solution and refill with the 80% solution to get the desired 50% solution?

            This is an example of a problem that can be solved iteratively and demonstrates why
            the datafile approach is convenient.

        References
        ----------
        At site https://www.physiologyweb.com/calculators (add this prefix to urls)
            [1] Percent solutions:  percent_solutions_calculator.html
            [2] Mass per unit volume calculator:  mass_per_volume_solution_concentration_calculator.html
            [3] Dilution calculator: dilution_calculator_mass_per_volume.html
        '''))
        exit(0)
if 1:  # Interactive solution
    def GetData():
        # Set all numbers to 0
        g.Conc1 = g.Conc2 = flt(0)
        g.Vol1 = g.Vol2 = g.VolMixture = g.ConcMixture = flt(0)
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
        g.Conc1 = Get("  Concentration of solution 1 in %? ", high=100, default=0)
        g.Conc2 = Get("  Concentration of solution 2 in %? ", high=100, default=0)
        print(dedent('''
    
        Enter two of:  volume 1, volume 2, mixture volume, mixture
        concentration.  Press return if not known.  Expressions are allowed and
        the math module is in scope.
    
        '''))
        data_items_entered = 0
        while True:
            g.Vol1 = Get("  Volume of solution 1? ", default=g.Vol1)
            if g.Vol1:
                data_items_entered += 1
            g.Vol2 = Get("  Volume of solution 2? ", default=g.Vol2)
            if g.Vol2:
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
            # Show how we interpreted the input data
            print(dedent(f'''
    
            {t('cynl')}Entered data:
                Vol1            {g.Vol1!r}
                Vol2            {g.Vol2!r}
                VolMixture      {g.VolMixture!r}
                Conc1           {g.Conc1!r}
                Conc2           {g.Conc2!r}
                ConcMixture     {g.ConcMixture!r}{C.norm}'''))
    def PrintResults():
        pa, pb, pm = g.Conc1/flt(100), g.Conc2/flt(100), g.ConcMixture/flt(100)
        if g.Vol1 and g.Vol2:
            g.VolMixture = flt(g.Vol1 + g.Vol2)
            g.ConcMixture = flt(100*(g.Vol1*pa + g.Vol2*pb)/(g.Vol1 + g.Vol2))
        elif g.Vol1 and g.ConcMixture:
            g.VolMixture = flt(g.Vol1*(pa - pb)/(pm - pb))
            g.Vol2 = flt(g.VolMixture - g.Vol1)
        elif g.Vol1 and g.VolMixture:
            g.Vol2 = flt(g.VolMixture - g.Vol1)
            g.ConcMixture = flt(100*(g.Vol1*pa + g.Vol2*pb)/(g.Vol1 + g.Vol2))
        elif g.Vol2 and g.ConcMixture:
            g.VolMixture = flt(g.Vol2*(pb - pa)/(pm - pa))
            g.Vol1 = flt(g.VolMixture - g.Vol2)
        elif g.Vol2 and g.VolMixture:
            g.Vol1 = flt(g.VolMixture - g.Vol2)
            g.ConcMixture = flt(100*(g.Vol1*pa + g.Vol2*pb)/g.VolMixture)
        elif g.VolMixture and g.ConcMixture:
            g.Vol1 = flt(g.VolMixture*(pm - pb)/(pa - pb))
            g.Vol2 = flt(g.VolMixture - g.Vol1)
        else:
            print("Not enough information")
            exit(1)
        # Print results
        n, k, s = 8, 14, " "*8
        print(dedent(f'''
        
        Results:
            Solution            Volume            Concentration %
            --------        --------------        ---------------
            {"1":^{n}s}{s}{g.Vol1!s:^{k}s}{s}{g.Conc1!s:^{k}s}
            {"2":^{n}s}{s}{g.Vol2!s:^{k}s}{s}{g.Conc2!s:^{k}s}
            {"Mixture":^{n}s}{s}{g.VolMixture!s:^{k}s}{s}{g.ConcMixture!s:^{k}s}
        '''))
if 1:  # Datafile approach
    def PrintSampleDatafile():
        print(dedent(f"""
        '''
        This is a sample data file for the mixture.py script.  This data file needs to be valid
        python syntax.

        The problem being solved is the mixing of two solutions, solution 1 and solution 2.  Both
        solutions contain the same solvent and solute.  The key assumptions are that the solute
        and solvent are miscible, mixed well, and there are no volume or temperature changes when
        the solutions are mixed.  If the assumptions are not satisfied, you still may be able to
        get reasonably good approximate answers, particularly for dilute solutions.

        You need to define four of the following six variables:
          c1      Concentration of solution 1 in %
          c2      Concentration of solution 2 in %
          c       Concentration of resulting mixture in %
          v1      Volume of solution 1
          v2      Volume of solution 2
          v       Volume of mixture

        These variables satisfy the equations

            v = v1 + v2
            c*v = c1*v1 + c2*v2

        You cannot have unknowns of (c1, c2), (c1, c), or (c2, c) because these conditions
        effectively give one equation with two unknowns.

        You may also define 'v_unit' as the desired volume unit for output.  It defaults to 'm3'
        as if you used

            v_unit = "m3"

        The u() function is used to let you use the input volume units of your choice (it's in
        /plib/u.py).  The following example line lets you define the v1 variable in terms of ml:

          v1 = 321*u("ml")

        Run 'python /plib/u.py' to see allowed volume units (you can also use any valid length
        unit with an appended 3 for a power of 3).

        Your definitions must use valid python syntax.
        '''

        # The following example data solve the following problem.  I have a
        # weed killer (solution 1) with a concentration of 11.3%.  I want
        # to know how much of it I must mix with a volume of water
        # (solution 2) to get a 15 gallon solution with a concentration of
        # 0.25%.

        c1 = 11.3           # Concentration of solution 1
        c2 = 0              # Concentration of solution 2
        c  = 0.25           # Concentration of mixture
        v  = 15*u("gal")    # Volume of mixture
        v_unit = "gal"      # Report should use gallons for volumes

        # This optional variable holds a description of the problem and
        # is printed with the report if present.
        description = ""

        # This data file should give the results
        #   volume of solution 1 = 0.332 gal
        #   volume of solution 2 = 14.7 gal
        """))
    def TestSolutions():
        '''This function tests the GetUnknowns() function to see that it
        uses the correct formulas.  The equations are
            v = v1 + v2
            c*v = c1*v1 + c2*v2
        The problem is 
            c1, c2, c = 8, 10, 9
            v1, v2, v = 1, 1, 2
        '''
        init = 8, 10, 9, 1, 1, 2
        # Unknowns v2 and v 
        c1, c2, c, v1, v2, v  = init
        v2, v  = None, None
        v, _ = GetUnknowns(c1, c2, c, v1, v2, v )
        c1, c2, c, v1, v2, v  = v
        Assert(v2 == 1 and v  == 2)
        # Unknowns v1 and v 
        c1, c2, c, v1, v2, v  = init
        v1, v  = None, None
        v, _ = GetUnknowns(c1, c2, c, v1, v2, v )
        c1, c2, c, v1, v2, v  = v
        Assert(v1 == 1 and v  == 2)
        # Unknowns v1 and v2
        c1, c2, c, v1, v2, v  = init
        v1, v2 = None, None
        v, _ = GetUnknowns(c1, c2, c, v1, v2, v )
        c1, c2, c, v1, v2, v  = v
        Assert(v1 == 1 and v2 == 1)
        # Unknowns c  and v 
        c1, c2, c, v1, v2, v  = init
        c, v  = None, None
        v, _ = GetUnknowns(c1, c2, c, v1, v2, v )
        c1, c2, c, v1, v2, v  = v
        Assert(c  == 9 and v  == 2)
        # Unknowns c  and v2
        c1, c2, c, v1, v2, v  = init
        c, v2 = None, None
        v, _ = GetUnknowns(c1, c2, c, v1, v2, v )
        c1, c2, c, v1, v2, v  = v
        Assert(c  == 9 and v2 == 1)
        # Unknowns c  and v1
        c1, c2, c, v1, v2, v  = init
        c, v1 = None, None
        v, _ = GetUnknowns(c1, c2, c, v1, v2, v )
        c1, c2, c, v1, v2, v  = v
        Assert(c  == 9 and v1 == 1)
        # Unknowns c2 and v 
        c1, c2, c, v1, v2, v  = init
        c2, v  = None, None
        v, _ = GetUnknowns(c1, c2, c, v1, v2, v )
        c1, c2, c, v1, v2, v  = v
        Assert(c2 == 10 and v  == 2)
        # Unknowns c2 and v2
        c1, c2, c, v1, v2, v  = init
        c2, v2 = None, None
        v, _ = GetUnknowns(c1, c2, c, v1, v2, v )
        c1, c2, c, v1, v2, v  = v
        Assert(c2 == 10 and v2 == 1)
        # Unknowns c2 and v1
        c1, c2, c, v1, v2, v  = init
        c2, v1 = None, None
        v, _ = GetUnknowns(c1, c2, c, v1, v2, v )
        c1, c2, c, v1, v2, v  = v
        Assert(c2 == 10 and v1 == 1)
        # Unknowns c1 and v 
        c1, c2, c, v1, v2, v  = init
        c1, v  = None, None
        v, _ = GetUnknowns(c1, c2, c, v1, v2, v )
        c1, c2, c, v1, v2, v  = v
        Assert(c1 == 8 and v  == 2)
        # Unknowns c1 and v2
        c1, c2, c, v1, v2, v  = init
        c1, v2 = None, None
        v, _ = GetUnknowns(c1, c2, c, v1, v2, v )
        c1, c2, c, v1, v2, v  = v
        Assert(c1 == 8 and v2 == 1)
        # Unknowns c1 and v1
        c1, c2, c, v1, v2, v  = init
        c1, v1 = None, None
        v, _ = GetUnknowns(c1, c2, c, v1, v2, v )
        c1, c2, c, v1, v2, v  = v
        Assert(c1 == 8 and v1 == 1)
    def GetSolutions():
        '''Use sympy to solve for the needed volume mixture functions.
        The two core equations are:
            v  = v1 + v2
            c *v  = c1*v1 + c2*v2
        There are six variables, so the user must supply four of them.
        The problems are:
        
                Known      Solve for
            c1 c2 c  v1     v2 v 
            c1 c2 c  v2     v1 v 
            c1 c2 c  v      v1 v2
            c1 c2 v1 v2     c  v 
            c1 c2 v1 v      c  v2
            c1 c2 v2 v      c  v1
            c1 c  v1 v2     c2 v 
            c1 c  v1 v      c2 v2
            c1 c  v2 v      c2 v1
            c1 v1 v2 v      c2 c  *
            c2 c  v1 v2     c1 v 
            c2 c  v1 v      c1 v2
            c2 c  v2 v      c1 v1
            c2 v1 v2 v      c1 c  *
            c  v1 v2 v      c1 c2 *
        The problems marked * are those that cannot be solved because there
        is only one equation with two unknowns.
         
        This code produces the following output:
            (v2, v ) {((-c1*v1 + c *v1)/(c2 - c ), (-c1*v1 + c2*v1)/(c2 - c ))}
            (v1, v ) {((-c2*v2 + c *v2)/(c1 - c ), (c1*v2 - c2*v2)/(c1 - c ))}
            (v1, v2) {((-c2*v  + c *v )/(c1 - c2), (c1*v  - c *v )/(c1 - c2))}
            (c, v ) {((c1*v1 + c2*v2)/(v1 + v2), v1 + v2)}
            (c, v2) {((c1*v1 - c2*v1 + c2*v )/v , -v1 + v )}
            (c, v1) {((-c1*v2 + c1*v  + c2*v2)/v , -v2 + v )}
            (c2, v ) {((-c1*v1 + c *v1 + c *v2)/v2, v1 + v2)}
            (c2, v2) {((c1*v1 - c *v )/(v1 - v ), -v1 + v )}
            (c2, v1) {((c1*v2 - c1*v  + c *v )/v2, -v2 + v )}
            (c2, c ) EmptySet
            (c1, v ) {((-c2*v2 + c *v1 + c *v2)/v1, v1 + v2)}
            (c1, v2) {((c2*v1 - c2*v  + c *v )/v1, -v1 + v )}
            (c1, v1) {((c2*v2 - c *v )/(v2 - v ), -v2 + v )}
            (c1, c ) EmptySet
            (c1, c2) EmptySet
        The solutions marked as empty sets are not allowed.  You can see
        that the three volumes are given and the first equation may or may
        not be an equality.  Thus, the allowed solutions must contain at
        least one unknown volume.
        ----------------------------------------------------------------
        '''
        import sympy as S
        c1, c2, c, v1, v2, v  = S.symbols("c1 c2 c  v1 v2 v ")
        # Basic equations
        equations = [S.Eq(v , v1 + v2), S.Eq(c *v , c1*v1 + c2*v2)]
        # Get solutions
        for i in (
            (v2, v ),
            (v1, v ),
            (v1, v2),
            (c, v ),
            (c, v2),
            (c, v1),
            (c2, v ),
            (c2, v2),
            (c2, v1),
            (c2, c ),
            (c1, v ),
            (c1, v2),
            (c1, v1),
            (c1, c ),
            (c1, c2),
            ):
            try:
                print(i, S.linsolve(equations, i))
            except Exception:
                print(i, S.nonlinsolve(equations, i))
    def GetVars(file):
        'Return a dict of variables from file'
        vars = {}
        if file == "-":
            code = compile(sys.stdin.read(), "sys.stdin", 'exec')
            exec(code, globals(), vars)
        else:
            try:
                with open(file) as f:
                    code = compile(f.read(), file, 'exec')
                    exec(code, globals(), vars)
            except Exception:
                Error(f"Couldn't open file {file!r}")
        return vars
    def GetUnknowns(c1, c2, c, v1, v2, v ):
        '''Two of the unknowns should be None.  Solve for these two.
        Return (vars, colors) where both are 6-tuples.  vars contains the
        solved variables and colors contains the colorizing strings for the
        variables (the two unknowns will be colored).
        
        The solution's equations came from GetSolutions().
        '''
        if v2 is None and v  is None:
            v2 = (-c1*v1 + c *v1)/(c2 - c )
            v  = (-c1*v1 + c2*v1)/(c2 - c )
            t.v2 = t.v  = t.unk
        elif v1 is None and v  is None:
            v1 = (-c2*v2 + c *v2)/(c1 - c )
            v  = (c1*v2 - c2*v2)/(c1 - c )
            t.v1 = t.v  = t.unk
        elif v1 is None and v2 is None:
            v1 = (-c2*v  + c *v )/(c1 - c2)
            v2 = (c1*v  - c *v )/(c1 - c2)
            t.v1 = t.v2 = t.unk
        elif c  is None and v  is None:
            c  = (c1*v1 + c2*v2)/(v1 + v2)
            v  = v1 + v2
            t.c  = t.v  = t.unk
        elif c  is None and v2 is None:
            c  = (c1*v1 - c2*v1 + c2*v )/v 
            v2 = -v1 + v 
            t.c  = t.v2 = t.unk
        elif c  is None and v1 is None:
            c  = (-c1*v2 + c1*v  + c2*v2)/v 
            v1 = -v2 + v 
            t.c  = t.v1 = t.unk
        elif c2 is None and v  is None:
            c2 = (-c1*v1 + c *v1 + c *v2)/v2
            v  = v1 + v2
            t.c2 = t.v  = t.unk
        elif c2 is None and v2 is None:
            c2 = (c1*v1 - c *v )/(v1 - v )
            v2 = -v1 + v 
            t.c2 = t.v2 = t.unk
        elif c2 is None and v1 is None:
            c2 = (c1*v2 - c1*v  + c *v )/v2
            v1 = -v2 + v 
            t.c2 = t.v1 = t.unk
        elif c1 is None and v  is None:
            c1 = (-c2*v2 + c *v1 + c *v2)/v1
            v  = v1 + v2
            t.c1 = t.v  = t.unk
        elif c1 is None and v2 is None:
            c1 = (c2*v1 - c2*v  + c *v )/v1
            v2 = -v1 + v 
            t.c1 = t.v2 = t.unk
        elif c1 is None and v1 is None:
            c1 = (c2*v2 - c *v )/(v2 - v )
            v1 = -v2 + v 
            t.c1 = t.v1 = t.unk
        elif ((c2 is None and c  is None) or (c1 is None and c  is None) or 
              (c1 is None and c2 is None)):
            Error(dedent(f'''
            The following unknown pairs are not allowed:
                c1 and c2
                c1 and c 
                c2 and c 
            This is because this effectively gives one equation in two unknowns.
            '''))
        else:
            print("Bad problem:  variables are:")
            print(f"  c1 = {c1}%")
            print(f"  c2 = {c2}%")
            print(f"  c  = {c }%")
            print(f"  v1 = {v1}")
            print(f"  v2 = {v2}")
            print(f"  v  = {v }")
            exit(1)
        return (
            (c1, c2, c, v1, v2, v ),
            (t.c1, t.c2, t.c, t.v1, t.v2, t.v )
        )
    def SolveDatafile(file):
        '''Read the variables in from a text file and solve for the
        unknowns.  The core equations are
            v  = v1 + v2
            c *v  = c1*v1 + c2*v2
        There are six variables, so the user must supply four of them.
        There are Comb(6, 4) = 15 combinations, but 3 of them are not
        allowed because they have no solution.  The problems are:
               Known      Solve for
            c1 c2 c  v1     v2 v 
            c1 c2 c  v2     v1 v 
            c1 c2 c  v      v1 v2
            c1 c2 v1 v2     c  v 
            c1 c2 v1 v      c  v2
            c1 c2 v2 v      c  v1
            c1 c  v1 v2     c2 v 
            c1 c  v1 v      c2 v2
            c1 c  v2 v      c2 v1
            c1 v1 v2 v      c2 c  *
            c2 c  v1 v2     c1 v 
            c2 c  v1 v      c1 v2
            c2 c  v2 v      c1 v1
            c2 v1 v2 v      c1 c  *
            c  v1 v2 v      c1 c2 *
        The ones marked with * are not allowed because there is then
        effectively only one equation, the second, with two unknowns.
        '''
        if file != "-":
            f = P(file).resolve()
        vars = GetVars(f)
        # Get the problem's variables
        c1 = vars.get("c1", None)
        c2 = vars.get("c2", None)
        c  = vars.get("c ", None)
        v1 = vars.get("v1", None)
        v2 = vars.get("v2", None)
        v  = vars.get("v ", None)
        v_unit = vars.get("v_unit", "m3")
        # Set up output colors
        t.c1 = t.n
        t.c2 = t.n
        t.c  = t.n
        t.v1 = t.n
        t.v2 = t.n
        t.v  = t.n
        # Solve for the unknowns
        myvars, colors = GetUnknowns(c1, c2, c, v1, v2, v )
        c1, c2, c, v1, v2, v  = myvars
        t.c1, t.c2, t.c, t.v1, t.v2, t.v  = colors
        # Get width of printed variables
        c1, c2, c  = [flt(i) for i in (c1, c2, c )]
        v1, v2, v  = [flt(i)/u(v_unit) for i in (v1, v2, v )]
        results = c1, c2, c, v1, v2, v 
        w = max(len(str(i)) for i in results)
        # Print report
        t.print(dedent(f'''
        Concentration calculation (volume basis, unknowns in {t.unk}this color{t.n})
          Use '{sys.argv[0]} -H' to see the problem's assumptions.
          {time.asctime()}
          Input file = {t('grnl')}{"sys.stdin" if file == "-" else f} 
 
        '''))
        if "description" in vars and vars["description"].strip():
            print(vars["description"].strip())
            print()
        t.print(f"{t.c1}c1 = Solution 1 concentration   {c1!s:>{w}s} %")
        t.print(f"{t.c2}c2 = Solution 2 concentration   {c2!s:>{w}s} %")
        t.print(f"{t.c}c = Mixture concentration      {c!s:>{w}s} %")
        t.print(f"{t.v1}v1 = Volume of solution 1       {v1!s:>{w}s} {v_unit}")
        t.print(f"{t.v2}v2 = Volume of solution 2       {v2!s:>{w}s} {v_unit}")
        t.print(f"{t.v }v  = Volume of mixture          {v !s:>{w}s} {v_unit}")
        if len(args) > 1:
            print()

if __name__ == "__main__":
    d = {}      # Options dictionary
    TestSolutions()
    args = ParseCommandLine(d)
    for file in args:
        SolveDatafile(file)
