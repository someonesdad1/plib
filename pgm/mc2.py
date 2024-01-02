'''
Calculations relating mass and energy
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Relate mass and energy
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from math import *
        from pdb import set_trace as xx
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from u import u, ParseUnit
        from f import flt 
        from lwtest import Assert, check_flt
        from pprint import pprint as pp
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # Set to True for debug messages
        dbg = False
        t.dbg = t("lil")
        # Global variable holder
        class g:
            pass
        g.m = None          # Mass
        g.E = None          # Energy
        g.V = None          # Volume
        g.s = None          # Length of side of cube = Volume**3
        g.c = 299792458     # Speed of light in m/s
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        n = sys.argv[0]
        print(dedent(f'''
        This script is used to convert between mass and energy.  A simple
        example is the conversion of 1 kg of mass to energy:
            
            {n} m 1

        gives
            Input       'm 1'
            Mass        1 g = 1e0 g = 2.2e0 lb
            Energy      90 PJ = 9e16 J = 21000 kilotons TNT = 1400 Hiroshimas
            Volume      130 μm³ = 1.3e-4 m³
            Length      50 mm = 5e-2 m = 2e0 in
            Density     7900 kg/m³ = 7.9 g/cm³
            Material    Steel, rolled

        From the equation E = m*c**2, you can do this problem in your head:
        m is 1 kg and the speed of light c in SI is 3e8 m/s, so the result 
        is 1(3e8)**2 or 9e16 J, as expected.  

        The Volume is calculated from the mass, assuming the density of
        steel.  You can select different materials with the -m option (see
        a list of materials with -M) or give the -m option a numerical
        argument, assumed to be a density in g/mL.

        The Length is the side of a cube of this material, which is the
        cube root of the volume.

        If you use the -m option with the built-in materials, you'll find
        the size of the cube varies from 210 mm for aerogel to 35 mm for
        osmium.

        Here are some other examples to show the utility of the script.
        While there's nothing you can't do with a calculator, the script
        makes it a little easier to see the numbers.

        - What size of a cube of steel will convert to 1 J of energy?  Use
          the command '{n} L 1' and you get the length of 0.11 μm.  This is
          on the order of the size of a typical virus.

        - A car has a gas tank that contains 20 gallons of gasoline.  The
          combustion heat of this gasoline is 44 MJ/kg and the density of
          gasoline is about 0.75 g/m³, giving 2.5 GJ of heat energy.  The
          size of a cube of steel for this energy is 150 μm, or a cube with
          a side roughly the diameter of a human hair.

        - What mass has the energy equivalent of the bomb dropped on
          Hiroshima?  Noting the above example for 1 kg of mass yielded
          1400 Hiroshimas, use the command 

            {n} m 1/1400*tan(pi/4)

          to get a mass of 0.7 μg.  This demonstrates that the numerical
          term can be a python expression and that the math library is in
          scope.  Note you'll may have to escape the math symbols from the
          shell.

        - An estimate for the mass of the observable universe is 1e53 kg.
          Assuming the big bang started with the equivalent energy, how
          much energy does this represent?  'm 1e53' gives 9e69 J.  Since
          the mass of the hydrogen atom is about 1 Dalton = 1.7e-27 kg,
          this means there would be about 1e53/1.7e-27 hydrogen atoms in
          the universe, or 5e79.  This is pretty close to the typical
          calculation of 1e80 atoms gotten from assuming around 1e9
          stars in a galaxy, 1e12 galaxies, and each star being around the
          mass of the sun of 2e30 kg.  1e9*1e12*2e30 is 1e51, a factor of
          100 below the above mass of the observable universe.

        - The US consumed in 2021 about 1e20 J of energy.  If this could be
          produced by total annihilation of mass with 10% efficiency, how
          much mass would be required?  Use '{n} e 1e20/0.1' to get a
          mass of about 1e6 kg.  That's a cube of steel about 1 m on a
          side, maybe about half the size of a regular desk.
        '''))
        exit(0)
    def Usage(status=1):
        n = sys.argv[0]
        print(dedent(f'''
        Usage:  {n} [options] op arg
          Calculations involving m = mass, E = energy, s = side of cube.
          The op choices denoting the calculation to be done are:
            op    arg
            --    -------
            m     mass      
            E     energy    
            V     volume    
            L     length    
          You can include common units with the arg number, cuddled or
          separated by whitespace.  If you give a volume, the corresponding
          mass is calculated assuming the indicated material.  The letter
          for op is case-independent.  The default units are kg, m, J.
  
          A kiloton of TNT is equivalent to 4.184 TJ.  This unit is denoted
          kttnt in the script.  The Hiroshima bomb was 15.5 kttnt.
        Example:
            {n} -m water v 1 ml
          will calculate the energy created by the conversion of 1
          milliliter of water to energy.  Since this is 1 g of water,
          the resulting energy is 9e13 J.
        Options:
            -d n    Number of significant digits [{d['-d']}]
            -h      Print manpage
            -M      List material choices
            -m mat  Choose material (default is steel).  The mat string
                    must start the name in the list of materials.  Can also
                    be a number in g/mL.
            -t      Run self tests
        '''))
        exit(status)
    def ParseCommandLine(d):
        GetDensityDict()
        d["-d"] = 2         # Number of significant figures
        d["-m"] = "steel"   # Material
        d["-t"] = False     # Run self tests
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:hMm:t") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("t"):
                d[o] = not d[o]
            elif o == "-M":
                ListMaterials()
            elif o in ("-h", "--help"):
                Manpage()
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o == "-m":
                d["-m"] = a
        if d["-t"]:
            Test()
        if len(args) < 2:
            Usage()
        x = flt(1.23456)
        x.N = d["-d"]
        x.low = 1e-3
        x.high = 1e5
        GetDensity()
        if d["-t"]:
            Test()
        return args
if 1:   # Core functionality
    def ListMaterials():
        # Get max width
        w = 0
        for i in g.density:
            w = max(w, len(i))
        w += 2
        x = flt(0)
        x.N = 3
        print("Materials with density in kg/m3")
        print("-------------------------------")
        for i in g.density:
            print(f"{i:{w}s} {int(g.density[i]):6d}")
        exit(0)
    def GetDensityDict():
        'Put density dict in g.density in kg/m3'
        # Density in g/cc 
        data = '''
        Stryofoam                         ; 0.04     
        Aerogel, silica                   ; 0.11     
        Corkboard                         ; 0.2      
        Coffee (instant)                  ; 0.304     
        Flour, loose                      ; 0.45    
        Pine, Oregon                      ; 0.51     
        Ice, crushed                      ; 0.59     
        Gasoline                          ; 0.74
        Alcohol, wood (methanol)          ; 0.79     
        Diesel                            ; 0.8      
        Polypropylene                     ; 0.9      
        Vaseline                          ; 0.9      
        Water, (0 °C & 1 atm)             ;  1       
        Epoxy                             ; 1.11     
        PVC, polyvinyl chloride           ; 1.25     
        Earth (dirt), dry                 ; 1.4      
        Earth (dirt), wet, excavated      ; 1.6      
        Polyester w/65% by wt glass cloth ; 1.8      
        Brick, hard                       ;  2       
        Glass, window                     ; 2.5      
        Aluminum                          ; 2.7      
        Basalt, solid (igneous rock)      ; 3.01     
        Alumina Al₂O₃                     ; 3.68     
        Titanium                          ; 4.5      
        Pyrite (fool's gold, FeS₂)        ; 5
        Earth, planet, mean density       ; 5.51     
        Vanadium                          ; 6.1      
        Iron, cast gray                   ; 7.1
        Manganese                         ; 7.43     
        Steel, rolled                     ; 7.93     
        Brass, leaded free-machining      ; 8.5      
        Copper, pure                      ; 8.96     
        Bismuth                           ; 9.75     
        Molybdenum                        ; 10.2     
        Lead 99.9%                        ; 11.3     
        Palladium                         ;  12      
        Mercury (25 °C)                   ; 13.5     
        Tungsten carbide (WC)             ; 15.2     
        Uranium                           ; 19.1     
        Gold                              ; 19.3     
        Tungsten                          ; 19.3     
        Platinum                          ; 21.4     
        Osmium                            ; 22.6'''[1:]
        g.density = {}
        for line in data.split("\n"):
            f = line.split(";")
            Assert(len(f) == 2)
            name = f[0].strip()
            density = flt(f[1].strip())
            g.density[name] = density*u("g/cc")  # Convert to kg/m3
        if 0:
            print("Density dictionary:")
            pp(g.density)
    def FindMaterialDensity(material):
        'Return (name, density) of indicated material in kg/m3'
        found, names = [], []
        for matl in g.density:
            if matl.lower().startswith(material.lower()):
                found.append(g.density[matl])
                names.append(matl)
        if len(found) == 1:
            return names[0], found[0]
        elif len(found) == 0:
            Error("No material found for '{material}'")
        else:
            print("Found multiple material matches:")
            for i in names:
                print(f"    {i}")
            exit(1)
    def GetDensity():
        'Set g.rho to chosen material density in kg/m3'
        material = d["-m"]
        try:
            # Can be a flt in g/cc
            g.name = "{material} g/cc"
            g.rho = flt(material)*u("g/cc")
        except ValueError:
            g.name, g.rho = FindMaterialDensity(material)
    def Mass(op, arg):
        if dbg:
            t.print(f"{t.dbg}Mass({op}, {arg})")
        mass, unit = ParseUnit(arg, allow_expr=True)
        if not unit:
            unit = "kg"
        g.m = flt(eval(mass))*u(unit)
        g.V = g.m/g.rho
        g.s = g.V**(1/3)    # Edge of cube with this volume
        g.E = g.m*g.c**2
        Report(op, arg)
    def Energy(op, arg):
        if dbg:
            t.print(f"{t.dbg}Energy({op}, {arg})")
        energy, unit = ParseUnit(arg, allow_expr=True)
        if not unit:
            unit = "J"
        g.E = flt(eval(energy))*u(unit)
        g.m = g.E/g.c**2
        g.V = g.m/g.rho
        g.s = g.V**(1/3)
        Report(op, arg)
    def Volume(op, arg):
        if dbg:
            t.print(f"{t.dbg}Volume({op}, {arg})")
        volume, unit = ParseUnit(arg, allow_expr=True)
        if not unit:
            unit = "m3"
        g.V = flt(eval(volume))*u(unit)
        g.s = g.V**(1/3)    # Edge of cube with this volume
        g.m = g.rho*g.V
        g.E = g.m*g.c**2
        Report(op, arg)
    def Length(op, arg):
        if dbg:
            t.print(f"{t.dbg}Length({op}, {arg})")
        length, unit = ParseUnit(arg, allow_expr=True)
        if not unit:
            unit = "m"
        g.s = flt(eval(length))*u(unit)
        g.V = g.s**3
        g.m = g.rho*g.V
        g.E = g.m*g.c**2
        Report(op, arg)
    def Test():
        '''Test each function Mass, Energy, Volume, Length to show that
        they produce the correct values.
 
        The basic calculation is done for 1 kg of mass:
            m = 1 kg
            E = 8.98755178736818e16 J
            V = 1.26103404791929e-4 m3 for steel
            s = V**(1/3) = 0.0501466898597635 m
        '''
        def Check():
            eps = 1e-15
            f = check_flt(g.m, m, reltol=eps)
            Assert(not f)
            f = check_flt(g.E, E, reltol=eps)
            Assert(not f)
            f = check_flt(g.V, V, reltol=eps)
            Assert(not f)
            f = check_flt(g.s, s, reltol=eps)
            Assert(not f)
        GetDensity()
        # Expected values for a 1 kg mass of steel
        m = 1                       # kg
        E = 8.98755178736818e16     # J
        V = 1.26103404791929e-4     # m3
        s = 0.0501466898597635      # m
        # Mass
        Mass("m", str(m))
        Check()
        # Energy
        Energy("e", str(E))
        Check()
        # Volume
        Volume("V", str(V))
        Check()
        # Length
        Length("L", str(s))
        Check()
        print("Tests passed")
        exit(0)
    def Report(op, arg):
        if d["-t"]:
            return
        w, t = 12, " "*0
        print(f"{'Input':{w}s}{t}'{op} {arg}'")
        print(f"{'Mass':{w}s}{t}{g.m.engsi}g = {g.m.sci} g = {(g.m/u('lb')).sci} lb")
        kt = g.E/flt(4.184e12)
        hiroshima = kt/15.5
        print(f"{'Energy':{w}s}{t}{g.E.engsi}J = {g.E.sci} J = {kt} kilotons TNT = {hiroshima} Hiroshimas")
        print(f"{'Volume':{w}s}{t}{g.V.engsi}m³ = {g.V.sci} m³")
        print(f"{'Length':{w}s}{t}{g.s.engsi}m = {g.s.sci} m = {(g.s/u('in')).sci} in")
        print(f"{'Density':{w}s}{t}{g.rho} kg/m³ = {g.rho/1000} g/cm³")
        print(f"{'Material':{w}s}{t}{g.name}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    op = args.pop(0)
    arg = ' '.join(args)
    if op.lower() == "m":
        Mass(op, arg)
    elif op.lower() == "e":
        Energy(op, arg)
    elif op.lower() == "v":
        Volume(op, arg)
    elif op.lower() == "l":
        Length(op, arg)
    else:
        Error(f"'{op}' is an unrecognized op")
