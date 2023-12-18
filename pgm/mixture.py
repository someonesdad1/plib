'''

TODO
    - Change to a datafile format
        - Get rid of prompting stuff
        - You then define variables ca, cb, cm, va, vb, vm
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
    - Allow command line to be e.g.  " 'ca = 11.2%' 'cb = 0' 'vm = 15 gal'
      'cm = 0.25%' " and the other variables would be solved for.  You can
      give concentration in % or as a number which must be on [0, 1].
    - With no command line arguments, you're prompted for the quantities
 
- The basic problem variables are
    - a and b are the two solutions, m is the mixture
    - ca, cb, cm = concentrations
    - va, vb, vm = volumes
    - Equations
        - vm = va + vb
        - cm = (ca*va + cb*vb)/vm
    - There are 6 variables with 2 equations, so there will be 4 variables
      that will need to be given for a solution.
    - The fundamental assumption is that the volumes don't change when you
      mix the solutions.  This can be a reasonable approximation for dilute
      solutions.
 
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
        g.VolA = flt(0)
        g.VolB = flt(0)
        g.VolMixture = flt(0)
        g.ConcA = flt(0)
        g.ConcB = flt(0)
        g.ConcMixture = flt(0)
        t.unk = t("ornl")
        t.ca, t.cb, t.cm, t.va, t.vb, t.vm = [""]*6
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(d):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [file]
          Interactively calculate dilution problems.  If a file is given, the
          variables are taken from the file's contents (use '-' to read the
          file from stdin).
        Using a datafile:
          The variables are
            ca      Solution A concentration in %
            cb      Solution B concentration in %
            cm      Mixture concentration in %
            va      Solution A volume
            vb      Solution B volume
            vm      Mixture volume
          The equations solved are
            vm = va + vb
            cm*vm = ca*va + cb*vb
        Options
            -c      Print a sample datafile
            -d n    Number of figures to display
            -H      Show manpage
            -h      Show this help
        '''))
        exit(0)
    def ParseCommandLine(d):
        d["-c"] = False     # Print sample datafile
        d["-d"] = 3         # Number of significant digits
        d["-g"] = False     # Debug printing
        try:
            opts, args = getopt.getopt(sys.argv[1:], "cd:gHh")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cg"):
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
        return args
    def Manpage(d):
        print(dedent('''

Use [1] to provide a gentler introduction and to help design
further additions to the code.  Get rid of the interactive solution
code.


        This script calculates the concentration of a solution gotten by mixing
        two volumes of solutions of differing concentrations.  The solute
        is the solution that is diluted by adding solvent.  Example:  a
        concentrated weed killer solution is the solute and the solvent is
        water.  

        Symbols:
            c = concentration volume fraction in percent
            v = volume of solute + solvent
        
        The six variables in the problem are thus:
            Solution A:  ca, va
            Solution B:  cb, vb
            Mixture:     cm, vm
        
        Solution A has a solute volume of ca*va.
        Solution B has a solute volume of cb*vb.
        
        After mixing, the resulting mixture has a solute volume faction of
        
            cm = (ca*va + cb*vb)/vm
        
        where the volume is
        
            vm = va + vb
    
        Assumptions:
            - The solute in both solutions A and B are the same
            - One or both solutions can be pure solvent
            - The solute and solvent are miscible and are mixed well
            - No volume or temperature changes when the solutions are mixed
            - Works best for dilute solutions
            - The concentration fractions are volume fractions.  This means
              both the solvent and solute are liquids (example:  water and
              antifreeze for your car).
        
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
    
        Here are the entered values and results:
    
            Concentration of solution A in %? [0] 11.3
            Concentration of solution B in %? [0] 0
    
          Enter two of:  volume A, volume B, mixture volume, mixture concentration.
          Press return if not known.  Expressions are allowed and the math module
          is in scope.
    
            Volume of solution A? [0]
            Volume of solution B? [0]
            Volume of mixture? 15
            Concentration of mixture in %? [0] 0.25
    
          Results:
              Solution            Volume            Concentration %
              --------        --------------        ---------------
                 A                0.332                  11.3
                 B                 14.7                   0
               Mixture              15                   0.25
    
        Note I assumed gallons for volumes.  The bottle of concentrate is 1
        quart or 32 fl oz, which is 1/4 gallon.  Thus, I need to add 0.332/0.25
        or 4(0.332) = 1.33 bottles to the tank and fill it up to the 15 gallon
        level.
 
        If you use the datafile approach to solve the problem, the
        calculation is a little more convenient because you can specify the
        unit used for the volumes used in the report.  Use the -c option to
        print a sample datafile and supply the known variables.  The u()
        function accepts commonly-used volume units.

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
            # Show how we interpreted the input data
            print(dedent(f'''
    
            {t('cynl')}Entered data:
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
if 1:  # Datafile approach
    def PrintSampleDatafile():
        print(dedent(f"""
        '''
        This is a sample data file for the mixture.py script.  This data
        file needs to be valid python syntax.

        You need
        to define four of the following six variables:
          ca      Concentration of solution A in %
          cb      Concentration of solution B in %
          cm      Concentration of resulting mixture in %
          va      Volume of solution A
          vb      Volume of solution B
          vm      Volume of mixture

        These variables satisfy the equations

            vm = va + vb
            cm*vm = ca*va + cb*vb
        
        You cannot have unknowns of (ca, cb), (ca, cm), or (cb, cm) because
        these conditions effectively give one equation with two unknowns.

        You may also define 'v_unit' as the desired volume unit for
        output.  It defaults to 'm3' as if you used

            v_unit = "m3"
        
        The u() function is used to let you use the input volume units of
        your choice (it's in /plib/u.py).  The following example line lets
        you define the va variable in terms of ml:
        
          va = 321*u("ml")
        
        Run 'python /plib/u.py' to see allowed volume units (you can also
        use any valid length unit with an appended 3 for a power of 3).

        Your definitions must use valid python syntax.
        '''
 
        # The following example data solve the following problem.  I have a
        # weed killer (solution A) with a concentration of 11.3%.  I want
        # to know how much of it I must mix with a volume of water
        # (solution B) to get a 15 gallon solution with a concentration of
        # 0.25%.
    
        ca = 11.3           # Concentration of solution a
        cb = 0              # Concentration of solution b
        cm = 0.25           # Concentration of mixture
        vm = 15*u("gal")    # Volume of mixture
        v_unit = "gal"      # Report should use gallons for volumes

        description = '''
            This optional variable holds a description of the problem and
            is printed with the report if present.
        '''
    
        # This data file should give the results
        #   volume of solution A = 0.332 gal
        #   volume of solution B = 14.7 gal
        """))
    def TestSolutions():
        '''This function tests the GetUnknowns() function to see that it
        uses the correct formulas.  The equations are
            vm = va + vb
            cm*vm = ca*va + cb*vb
        The problem is 
            ca, cb, cm = 8, 10, 9
            va, vb, vm = 1, 1, 2
        '''
        init = 8, 10, 9, 1, 1, 2
        # Unknowns vb and vm
        ca, cb, cm, va, vb, vm = init
        vb, vm = None, None
        v, _ = GetUnknowns(ca, cb, cm, va, vb, vm)
        ca, cb, cm, va, vb, vm = v
        Assert(vb == 1 and vm == 2)
        # Unknowns va and vm
        ca, cb, cm, va, vb, vm = init
        va, vm = None, None
        v, _ = GetUnknowns(ca, cb, cm, va, vb, vm)
        ca, cb, cm, va, vb, vm = v
        Assert(va == 1 and vm == 2)
        # Unknowns va and vb
        ca, cb, cm, va, vb, vm = init
        va, vb = None, None
        v, _ = GetUnknowns(ca, cb, cm, va, vb, vm)
        ca, cb, cm, va, vb, vm = v
        Assert(va == 1 and vb == 1)
        # Unknowns cm and vm
        ca, cb, cm, va, vb, vm = init
        cm, vm = None, None
        v, _ = GetUnknowns(ca, cb, cm, va, vb, vm)
        ca, cb, cm, va, vb, vm = v
        Assert(cm == 9 and vm == 2)
        # Unknowns cm and vb
        ca, cb, cm, va, vb, vm = init
        cm, vb = None, None
        v, _ = GetUnknowns(ca, cb, cm, va, vb, vm)
        ca, cb, cm, va, vb, vm = v
        Assert(cm == 9 and vb == 1)
        # Unknowns cm and va
        ca, cb, cm, va, vb, vm = init
        cm, va = None, None
        v, _ = GetUnknowns(ca, cb, cm, va, vb, vm)
        ca, cb, cm, va, vb, vm = v
        Assert(cm == 9 and va == 1)
        # Unknowns cb and vm
        ca, cb, cm, va, vb, vm = init
        cb, vm = None, None
        v, _ = GetUnknowns(ca, cb, cm, va, vb, vm)
        ca, cb, cm, va, vb, vm = v
        Assert(cb == 10 and vm == 2)
        # Unknowns cb and vb
        ca, cb, cm, va, vb, vm = init
        cb, vb = None, None
        v, _ = GetUnknowns(ca, cb, cm, va, vb, vm)
        ca, cb, cm, va, vb, vm = v
        Assert(cb == 10 and vb == 1)
        # Unknowns cb and va
        ca, cb, cm, va, vb, vm = init
        cb, va = None, None
        v, _ = GetUnknowns(ca, cb, cm, va, vb, vm)
        ca, cb, cm, va, vb, vm = v
        Assert(cb == 10 and va == 1)
        # Unknowns ca and vm
        ca, cb, cm, va, vb, vm = init
        ca, vm = None, None
        v, _ = GetUnknowns(ca, cb, cm, va, vb, vm)
        ca, cb, cm, va, vb, vm = v
        Assert(ca == 8 and vm == 2)
        # Unknowns ca and vb
        ca, cb, cm, va, vb, vm = init
        ca, vb = None, None
        v, _ = GetUnknowns(ca, cb, cm, va, vb, vm)
        ca, cb, cm, va, vb, vm = v
        Assert(ca == 8 and vb == 1)
        # Unknowns ca and va
        ca, cb, cm, va, vb, vm = init
        ca, va = None, None
        v, _ = GetUnknowns(ca, cb, cm, va, vb, vm)
        ca, cb, cm, va, vb, vm = v
        Assert(ca == 8 and va == 1)
    def GetSolutions():
        '''Use sympy to solve for the needed volume mixture functions.
        The two core equations are:
            vm = va + vb
            cm*vm = ca*va + cb*vb
        There are six variables, so the user must supply four of them.
        The problems are:
        
                Known      Solve for
            ca cb cm va     vb vm
            ca cb cm vb     va vm
            ca cb cm vm     va vb
            ca cb va vb     cm vm
            ca cb va vm     cm vb
            ca cb vb vm     cm va
            ca cm va vb     cb vm
            ca cm va vm     cb vb
            ca cm vb vm     cb va
            ca va vb vm     cb cm *
            cb cm va vb     ca vm
            cb cm va vm     ca vb
            cb cm vb vm     ca va
            cb va vb vm     ca cm *
            cm va vb vm     ca cb *
        The problems marked * are those that cannot be solved because there
        is only one equation with two unknowns.
         
        This code produces the following output:
            (vb, vm) {((-ca*va + cm*va)/(cb - cm), (-ca*va + cb*va)/(cb - cm))}
            (va, vm) {((-cb*vb + cm*vb)/(ca - cm), (ca*vb - cb*vb)/(ca - cm))}
            (va, vb) {((-cb*vm + cm*vm)/(ca - cb), (ca*vm - cm*vm)/(ca - cb))}
            (cm, vm) {((ca*va + cb*vb)/(va + vb), va + vb)}
            (cm, vb) {((ca*va - cb*va + cb*vm)/vm, -va + vm)}
            (cm, va) {((-ca*vb + ca*vm + cb*vb)/vm, -vb + vm)}
            (cb, vm) {((-ca*va + cm*va + cm*vb)/vb, va + vb)}
            (cb, vb) {((ca*va - cm*vm)/(va - vm), -va + vm)}
            (cb, va) {((ca*vb - ca*vm + cm*vm)/vb, -vb + vm)}
            (cb, cm) EmptySet
            (ca, vm) {((-cb*vb + cm*va + cm*vb)/va, va + vb)}
            (ca, vb) {((cb*va - cb*vm + cm*vm)/va, -va + vm)}
            (ca, va) {((cb*vb - cm*vm)/(vb - vm), -vb + vm)}
            (ca, cm) EmptySet
            (ca, cb) EmptySet
        The solutions marked as empty sets are not allowed.  You can see
        that the three volumes are given and the first equation may or may
        not be an equality.  Thus, the allowed solutions must contain at
        least one unknown volume.
        ----------------------------------------------------------------
        '''
        import sympy as S
        ca, cb, cm, va, vb, vm = S.symbols("ca cb cm va vb vm")
        # Basic equations
        equations = [S.Eq(vm, va + vb), S.Eq(cm*vm, ca*va + cb*vb)]
        # Get solutions
        for i in (
            (vb, vm),
            (va, vm),
            (va, vb),
            (cm, vm),
            (cm, vb),
            (cm, va),
            (cb, vm),
            (cb, vb),
            (cb, va),
            (cb, cm),
            (ca, vm),
            (ca, vb),
            (ca, va),
            (ca, cm),
            (ca, cb),
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
    def GetUnknowns(ca, cb, cm, va, vb, vm):
        '''Two of the unknowns should be None.  Solve for these two.
        Return (vars, colors) where both are 6-tuples.  vars contains the
        solved variables and colors contains the colorizing strings for the
        variables (the two unknowns will be colored).
        
        The solution's equations came from GetSolutions().
        '''
        if vb is None and vm is None:
            vb = (-ca*va + cm*va)/(cb - cm)
            vm = (-ca*va + cb*va)/(cb - cm)
            t.vb = t.vm = t.unk
        elif va is None and vm is None:
            va = (-cb*vb + cm*vb)/(ca - cm)
            vm = (ca*vb - cb*vb)/(ca - cm)
            t.va = t.vm = t.unk
        elif va is None and vb is None:
            va = (-cb*vm + cm*vm)/(ca - cb)
            vb = (ca*vm - cm*vm)/(ca - cb)
            t.va = t.vb = t.unk
        elif cm is None and vm is None:
            cm = (ca*va + cb*vb)/(va + vb)
            vm = va + vb
            t.cm = t.vm = t.unk
        elif cm is None and vb is None:
            cm = (ca*va - cb*va + cb*vm)/vm
            vb = -va + vm
            t.cm = t.vb = t.unk
        elif cm is None and va is None:
            cm = (-ca*vb + ca*vm + cb*vb)/vm
            va = -vb + vm
            t.cm = t.va = t.unk
        elif cb is None and vm is None:
            cb = (-ca*va + cm*va + cm*vb)/vb
            vm = va + vb
            t.cb = t.vm = t.unk
        elif cb is None and vb is None:
            cb = (ca*va - cm*vm)/(va - vm)
            vb = -va + vm
            t.cb = t.vb = t.unk
        elif cb is None and va is None:
            cb = (ca*vb - ca*vm + cm*vm)/vb
            va = -vb + vm
            t.cb = t.va = t.unk
        elif ca is None and vm is None:
            ca = (-cb*vb + cm*va + cm*vb)/va
            vm = va + vb
            t.ca = t.vm = t.unk
        elif ca is None and vb is None:
            ca = (cb*va - cb*vm + cm*vm)/va
            vb = -va + vm
            t.ca = t.vb = t.unk
        elif ca is None and va is None:
            ca = (cb*vb - cm*vm)/(vb - vm)
            va = -vb + vm
            t.ca = t.va = t.unk
        elif ((cb is None and cm is None) or (ca is None and cm is None) or 
              (ca is None and cb is None)):
            Error(dedent(f'''
            The following unknown pairs are not allowed:
                ca and cb
                ca and cm
                cb and cm
            This is because this effectively gives one equation in two unknowns.
            '''))
        else:
            print("Bad problem:  variables are:")
            print("  ca = Solution {ca}")
            print("  cb = {cb}")
            print("  cm = {cm}")
            print("  va = {va}")
            print("  vb = {vb}")
            print("  vm = {vm}")
            exit(1)
        return (
            (ca, cb, cm, va, vb, vm),
            (t.ca, t.cb, t.cm, t.va, t.vb, t.vm)
        )
    def SolveDatafile(file):
        '''Read the variables in from a text file and solve for the
        unknowns.  The core equations are
            vm = va + vb
            cm*vm = ca*va + cb*vb
        There are six variables, so the user must supply four of them.
        There are Comb(6, 4) = 15 combinations, but 3 of them are not
        allowed because they have no solution.  The problems are:
               Known      Solve for
            ca cb cm va     vb vm
            ca cb cm vb     va vm
            ca cb cm vm     va vb
            ca cb va vb     cm vm
            ca cb va vm     cm vb
            ca cb vb vm     cm va
            ca cm va vb     cb vm
            ca cm va vm     cb vb
            ca cm vb vm     cb va
            ca va vb vm     cb cm *
            cb cm va vb     ca vm
            cb cm va vm     ca vb
            cb cm vb vm     ca va
            cb va vb vm     ca cm *
            cm va vb vm     ca cb *
        The ones marked with * are not allowed because there is then
        effectively only one equation, the second, with two unknowns.
        '''
        if file != "-":
            f = P(file).resolve()
        vars = GetVars(f)
        # Get the problem's variables
        ca = vars.get("ca", None)
        cb = vars.get("cb", None)
        cm = vars.get("cm", None)
        va = vars.get("va", None)
        vb = vars.get("vb", None)
        vm = vars.get("vm", None)
        v_unit = vars.get("v_unit", "m3")
        # Set up output colors
        t.ca = t.n
        t.cb = t.n
        t.cm = t.n
        t.va = t.n
        t.vb = t.n
        t.vm = t.n
        # Solve for the unknowns
        myvars, colors = GetUnknowns(ca, cb, cm, va, vb, vm)
        ca, cb, cm, va, vb, vm = myvars
        t.ca, t.cb, t.cm, t.va, t.vb, t.vm = colors
        # Get width of printed variables
        ca, cb, cm = [flt(i) for i in (ca, cb, cm)]
        va, vb, vm = [flt(i)/u(v_unit) for i in (va, vb, vm)]
        results = ca, cb, cm, va, vb, vm
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
        t.print(f"{t.ca}ca = Solution A concentration   {ca!s:>{w}s} %")
        t.print(f"{t.cb}cb = Solution B concentration   {cb!s:>{w}s} %")
        t.print(f"{t.cm}cm = Mixture concentration      {cm!s:>{w}s} %")
        t.print(f"{t.va}va = Volume of solution A       {va!s:>{w}s} {v_unit}")
        t.print(f"{t.vb}vb = Volume of solution B       {vb!s:>{w}s} {v_unit}")
        t.print(f"{t.vm}vm = Volume of mixture          {vm!s:>{w}s} {v_unit}")
        if len(args) > 1:
            print()

if __name__ == "__main__":
    d = {}      # Options dictionary
    TestSolutions()
    args = ParseCommandLine(d)
    if args:
        for file in args:
            SolveDatafile(file)
    else:
        GetData()
        PrintResults()
