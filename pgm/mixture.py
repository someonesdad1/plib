'''

TODO
    - Consider changing to a datafile format.
        - You then define variables ca, cb, cm, va, vb, vm
        - concentrations can be plain or have % appended
        - conc_unit = "%" or "" (used in output report)
        - vol_unit = "xxxx" 
        - Input data are printed, then report of results is given
    - Change to allow calculations via either mass or volume basis
        - -v is volume basis (default)
        - -m is mass basis
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
        import pathlib
        from functools import partial
        from pprint import pprint as pp
    if 1:   # Custom imports
        from wrap import dedent
        from get import GetNumber, GetLines
        from f import flt
        from u import u
        from color import C
        if 1:
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
        Options
            -c      Print a sample datafile
            -d n    Number of figures to display
            -H      Show manpage
            -h      Show this help
        '''))
        exit(0)
    def ParseCommandLine(d):
        d["-d"] = 3         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "cd:Hh")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("c"):
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
            Mixture:     Cm, Vm
        
        Solution A has a solute volume of Ca*Va.
        Solution B has a solute volume of Cb*Vb.
        
        After mixing, the resulting mixture has a solute volume faction of
        
            Cm = (Ca*Va + Cb*Vb)/Vm
        
        where the volume is
        
            Vm = Va + Vb
        
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
    
          Enter two of:  volume A, volume B, mixture volume, mixture
          concentration.  Press return if not known.  Expressions are allowed and
          the math module is in scope.
    
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
if 1:  # Datafile approach
    def PrintSampleDatafile():
        print(dedent(f'''
        
        # This is a sample data file for the mixture.py script.  You need
        # to define four of the following six variables:
        #   ca      Concentration of solution A in %
        #   cb      Concentration of solution B in %
        #   cm      Concentration of resulting mixture in %
        #   va      Volume of solution A
        #   vb      Volume of solution B
        #   vm      Volume of mixture
        #
        # You should also define 'v_unit' as the desired volume unit for
        # output.  It defaults to 'm3'.
        #
        # The u() function is used to let you use the input volume units of
        # your problem.  The following example line lets you define the va
        # variable in terms of ml:
        # 
        #   va = 321*u("ml")
        # 
        # Your definitions must use valid python syntax.

        # The following example data solve the following problem.  I have a
        # weed killer (solution a) with a concentration of 11.3%.  I want
        # to know how much of it I must mix with a volume of water
        # (solution b) to get a 15 gallon solution with a concentration of
        # 0.25%.
    
        ca = 11.3           # Concentration of solution a
        cb = 0              # Concentration of solution b
        cm = 0.25           # Concentration of mixture
        vm = 15*u("gal")    # Volume of mixture
        u_out = "gal"       # Report should use gallons for volumes
    
        # This data file should give the results
        #   volume of solution A = 0.332 gal
        #   volume of solution B = 14.7 gal
        '''))
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
        '''This code produces the following output:
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
        '''
    def GetVars(file):
        'Return a dict of variables from file'
        vars = {}
        with open(file) as f:
            code = compile(f.read(), file, 'exec')
            exec(code, globals(), vars)
        return vars
    def SolveDatafile(file):
        '''Read the variables in from a text file and solve for the
        unknowns.  The core equations are
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
        The ones marked with * are not allowed because there is then
        effectively only one equation, the second, with two unknowns.
        '''
        vars = GetVars(file)
        # Get the problem's variables
        ca = vars.get("ca", None)
        cb = vars.get("cb", None)
        cm = vars.get("cm", None)
        va = vars.get("va", None)
        vb = vars.get("vb", None)
        vm = vars.get("vm", None)
        u_out = vars.get("u_out", "m3")
        # Solve for the unknowns
        if vb is None and vm is None:
            vb = (-ca*va + cm*va)/(cb - cm)
            vm = (-ca*va + cb*va)/(cb - cm)
        elif va is None and vm is None:
            va = (-cb*vb + cm*vb)/(ca - cm)
            vm = (ca*vb - cb*vb)/(ca - cm)
        elif va is None and vb is None:
            va = (-cb*vm + cm*vm)/(ca - cb)
            vb = (ca*vm - cm*vm)/(ca - cb)
        elif cm is None and vm is None:
            cm = (ca*va + cb*vb)/(va + vb)
            vm = va + vb
        elif cm is None and vb is None:
            cm = (ca*va - cb*va + cb*vm)/vm
            vb = -va + vm
        elif cm is None and va is None:
            cm = (-ca*vb + ca*vm + cb*vb)/vm
            va = -vb + vm
        elif cb is None and vm is None:
            cb = (-ca*va + cm*va + cm*vb)/vb
            vm = va + vb
        elif cb is None and vb is None:
            cb = (ca*va - cm*vm)/(va - vm)
            vb = -va + vm
        elif cb is None and va is None:
            cb = (ca*vb - ca*vm + cm*vm)/vb
            va = -vb + vm
        elif ca is None and vm is None:
            ca = (-cb*vb + cm*va + cm*vb)/va
            vm = va + vb
        elif ca is None and vb is None:
            ca = (cb*va - cb*vm + cm*vm)/va
            vb = -va + vm
        elif ca is None and va is None:
            ca = (cb*vb - cm*vm)/(vb - vm)
            va = -vb + vm
        elif ((cb is None and cm is None) or (ca is None and cm is None) or 
              (ca is None and cb is None)):
            Error("At least one volume must be unknown")
        else:
            print("Bad problem:  variables are:")
            print("  ca = {ca}")
            print("  cb = {cb}")
            print("  cm = {cm}")
            print("  va = {va}")
            print("  vb = {vb}")
            print("  vm = {vm}")
            exit(1)
        # Print report
        print(f"ca = {flt(ca)}%")
        print(f"cb = {flt(cb)}%")
        print(f"cm = {flt(cm)}%")
        print(f"va = {flt(va)/u(u_out)} {u_out}")
        print(f"vb = {flt(vb)/u(u_out)} {u_out}")
        print(f"vm = {flt(vm)/u(u_out)} {u_out}")

if 0:
    for i in '''
    ca cb cm va
    ca cb cm vb
    ca cb cm vm
    ca cb va vb
    ca cb va vm
    ca cb vb vm
    ca cm va vb
    ca cm va vm
    ca cm vb vm
    ca va vb vm
    cb cm va vb
    cb cm va vm
    cb cm vb vm
    cb va vb vm
    cm va vb vm
    '''.strip().split("\n"):
        missing = ' '.join(set("ca cb cm va vb vm".split()) - set(i.split()))
        print(i, "   ", ' '.join(sorted(missing.split())))
    exit()

#GetSolutions()
SolveDatafile("mixture.data")
exit()

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
