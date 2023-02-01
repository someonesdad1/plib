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
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
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
        This script is used to convert between mass and energy.

        Check the output
        ------------

            '{n} -d 4 m 1' should show the energy in 1 kg of matter, which
            will be (1 kg)(299792458 m/s)**2 or 8.988e16 J.  This is a
            volume of 1/7930 or 1.261e-4 m3.  Taking the cube root of this
            gives a length of 0.005015 m.

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
        g.m = flt(mass)*u(unit)
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
        g.E = flt(energy)*u(unit)
        g.V = 1/g.rho
        g.s = g.V**(1/3)
        g.m = g.E/g.c**2
    def Volume(op, arg):
        if dbg:
            t.print(f"{t.dbg}Volume({op}, {arg})")
        volume, unit = ParseUnit(arg, allow_expr=True)
        if not unit:
            unit = "m3"
        g.V = flt(volume)*u(unit)
        g.s = g.V**(1/3)    # Edge of cube with this volume
        g.m = g.rho*g.V
        g.E = g.m*g.c**2
    def Length(op, arg):
        if dbg:
            t.print(f"{t.dbg}Length({op}, {arg})")
        length, unit = ParseUnit(arg, allow_expr=True)
        if not unit:
            unit = "m"
        g.s = flt(length)*u(unit)
        g.V = g.s**3
        g.m = g.rho*g.V
        g.E = g.m*g.c**2
    def Report(op, arg):
        if d["-t"]:
            return
        w, t = 12, " "*0
        print(f"{'Input':{w}s}{t}'{op} {arg}'")
        print(f"{'Mass':{w}s}{t}{g.m} kg")
        kt = g.E/flt(4.184e12)
        hiroshima = kt/15.5
        print(f"{'Energy':{w}s}{t}{g.E} J = {kt} kilotons TNT = {hiroshima} Hiroshimas")
        print(f"{'Volume':{w}s}{t}{g.V} m3")
        print(f"{'Length':{w}s}{t}{g.s} m")
        print(f"{'Density':{w}s}{t}{g.rho} kg/m3")
        print(f"{'Material':{w}s}{t}{g.name}")
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
        # Expected answers
        m = 1
        E = 8.98755178736818e16
        V = 1.26103404791929e-4
        s = 0.0501466898597635
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
