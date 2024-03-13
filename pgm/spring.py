'''
TODO

    - Use uncertainties
    - Print results in both English and metric units -- or allow user
      to choose mm/N/Pa or in/lbf/psi (change to u module).

----------------------------------------------------------------------
Helical spring design with round music wire

    Symbols are from Machinery's Handbook, 19th ed., pg 494 (Springs section).

    d = wire diameter, inches
    D = Mean coil diameter of spring = inside diameter of spring + d, inches
    P = load, pounds
    delta = deflection, inches
    tau = allowable stress, psi
    N = number of active coils
    G = modulus of rigidity, psi
    Ka = Wahl stress factor for helical springs
    C = spring index = D/d
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2006 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Helical ppring design using music wire
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import math
        import os
        import re
        import subprocess
        import sys
    if 1:   # Custom imports
        import shop_util
        from color import t
        from f import flt
        from dpprint import PP
        pp = PP()   # Screen width aware form of pprint.pprint
        from get import GetLines
        from wrap import dedent
        from wsl import wsl     # wsl is True when running under WSL Linux
        from interpolation import LagrangeInterpolation
        #from columnize import Columnize
    if 1:   # Global variables
        pi = math.pi
        class G:
            # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = True
        g.dbg = False
        ii = isinstance
        # Modulus of rigidity (modulus of torsional elasticity) of music
        # wire, MH pg 533
        g.G = 12e6    # psi
        # Allowable working stresses for compression springs, MH pg 535
        g.diameters = tuple([0.005] + [x/100 for x in range(1, 17)])
        g.Light_stress = (190, 172, 158, 148, 141, 136, 132, 128, 126, 123, 121, 119, 117.5, 116, 113, 112, 111)
        g.Average_stress = (170, 155, 141, 132, 126, 122, 119, 115, 112.5, 110.5, 108, 106, 105, 104, 102, 101, 99.5)
        g.Severe_stress = (130, 117, 106, 99, 94, 91.5, 89, 87, 84.5, 82.5, 80.5, 79, 77.5, 76, 75, 74, 73)
        assert(len(g.Light_stress) == 17)
        assert(len(g.Average_stress) == 17)
        assert(len(g.Severe_stress) == 17)
        stress_message = dedent(f'''
        {t('lill')}Define the service environment:{t.n}
            {t('brnl')}Light service{t.n}:  static loads only, small deflections, low stress.  Less than 1,000
                deflections in spring's lifetime (and rarely more than 10,000).
            {t('brnl')}Average service{t.n}:  majority of springs in general use.  1e5 to 1e6 deflections over
                the life of the spring.
            {t('brnl')}Severe service{t.n}:  rapid deflections over long periods of time.  Should be adequate
                for 1e6 deflection life; lower stress by 10% to get 1e7 deflections.  However,
                consult handbooks for details on how to avoid fatigue failure.
        ''')
if 1:   # Utility
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def GetColors():
        t.dbg = t("cyn") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("redl")
        t.title = t("ornl")
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)
    Dbg.file = sys.stdout
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Describe this option
        d["-d"] = 3         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
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
        GetColors()
        g.W, g.L = GetScreen()
        return args
if 1:   # Core functionality
    def Ka(d, D):
        'Wahl helical spring stress factor'
        C = D/d
        return (4*C-1)/(4*C-4) + 0.615/C
    def root_find(x0, x2, f, eps, itmax):
        ''' A root finding routine.  See "All Problems Are Simple" by Jack Crenshaw, Embedded
        Systems Programming, May, 2002, pg 7-14, jcrens@earthlink.com.  Can be downloaded from
        www.embedded.com/code.htm.
    
        Translated from Crenshaw's C code modified by Don Peterson 20 May 2003.
    
        Crenshaw states this routine will converge rapidly on most functions, typically adding 4
        digits to the solution on each iteration.  The method is something called "inverse
        parabolic interpolation".  The routine works by starting with x0, x2, and finding a third
        x1 by bisection.  The ordinates are gotten, then a horizontally- opening parabola is fitted
        to the points.  The parabola's root's abcissa is gotten, and the iteration is repeated.
    
        The function root_find will find a root of the function f(x) in the interval [x0, x2].  We
        must have that f(x0)*f(x2) < 0.
    
        The root value is returned.
    
        Root lies between x0 and x2.  f is the function to evaluate; it takes one float argument
        and returns a float.  eps is the precision to find the root to and itmax is the maximum
        number of iterations allowed.
    
        Returns a tuple (x, numits) where
            x is the root.
            numits is the number of iterations taken.
        The routine will throw an exception if it receives bad input data or it doesn't converge.
        '''
        x1 = y0 = y1 = y2 = b = c = temp = y10 = y20 = y21 = xm = ym = 0.0
        xmlast = x0
        assert(x0 < x2)
        assert(eps > 0.0)
        assert(itmax > 0)
        y0 = f(x0)
        if y0 == 0.0:
            return x0, 0
        y2 = f(x2)
        if y2 == 0.0:
            return x2, 0
        if y2 * y0 > 0.0:
            raise ValueError("Bad data: y0 = %f, y2 = %f\n" % (y0, y2))
        for ix in range(itmax):
            x1 = 0.5 * (x2 + x0)
            y1 = f(x1)
            if (y1 == 0.0) or (math.fabs(x1 - x0) < eps):
                return x1, ix+1
            if y1 * y0 > 0.0:
                temp = x0
                x0 = x2
                x2 = temp
                temp = y0
                y0 = y2
                y2 = temp
            y10 = y1 - y0
            y21 = y2 - y1
            y20 = y2 - y0
            if y2 * y20 < 2.0 * y1 * y10:
                x2 = x1
                y2 = y1
            else:
                b = (x1 - x0) / y10
                c = (y10 - y21) / (y21 * y20)
                xm = x0 - b * y0 * (1.0 - c * y1)
                ym = f(xm)
                if ((ym == 0.0) or (math.fabs(xm - xmlast) < eps)):
                    return xm, ix+1
                xmlast = xm
                if ym * y0 < 0.0:
                    x2 = xm
                    y2 = ym
                else:
                    x0 = xm
                    y0 = ym
                    x2 = x1
                    y2 = y1
        raise "No convergence"
    def GetAllowableWorkingStressInPsi(d, service_type):
        stress = g.Severe_stress
        if service_type == "l":
            stress = g.Light_stress
        elif service_type == "a":
            stress = g.Average_stress
        working_stress = LagrangeInterpolation(d, g.diameters, stress)
        return working_stress*1e3
    def SpringMandrel(D, d, phosphor_bronze=False):
        '''Return the required diameter of a spring winding mandrel for a helical spring made from
        music wire, stainless steel, or phosphor bronze.  d is the wire diameter and D is the
        outside diameter of the spring.
        '''
        D_mean = D - d
        si = D_mean/d
        if not 5 <= si <= 15:
            s = round(si, 3)
            raise ValueError("Spring index D/d = {0} out of range".format(s))
        # Points on the line
        if phosphor_bronze:
            x0, y0, x1, y1 = 5, 0.933, 15, 0.823
        else:
            x0, y0, x1, y1 = 5, 0.922, 15, 0.797
        m = (y1 - y0)/(x1 - x0)
        b = y0 - m*x0
        Dm = (m*si + b)*D_mean - d
        return round(Dm, 4)
    def GetLoadAndDeflection():
        if g.dbg:
            d = flt(0.04)
            s = "a"
            tau = flt(GetAllowableWorkingStressInPsi(d, s))
            D = flt(0.3)
            N = 20
            H = flt(1.5)
        else:
            # The min and max wire dimensions are from the chart on page 535 of MH
            d = shop_util.GetDouble("Wire diameter in inches?", "0.040", 0.005, 0.160)
            print(stress_message)
            s = shop_util.GetChoice("Service type l=light, a=average, s=severe?", "a", ("l", "a", "s"))
            tau = GetAllowableWorkingStressInPsi(d, s)
            D = shop_util.GetDouble("Mean spring diameter in inches?", "0.3", 0.005, 1e6)
            N = shop_util.GetInt("Number of active coils?", 20, 1, int(1e9))
            H = shop_util.GetDouble("Free length of spring in inches?", "1.5", 2*d, int(1e9))
        h = N*d + d
        L = (H-d)/N
        P = pi*d**3*tau/(8*Ka(d, D)*D)
        delta = 8*N*D**3*P/(g.G*d**4)
        k = P/delta
        try:
            md = "%.3g inches" % SpringMandrel(D + d, d)
        except Exception:
            md = "D/d out of range"
        print()
        print("Spring index D/d                 %.3g" % (D/d))
        print("Wire diameter d                  %.4g inches" % d)
        print("Mean spring diameter D           %.2g inches" % D)
        print("Number of active coils N         %d inches" % N)
        print("Free length H                    %.3g inches" % H)
        print("Pitch at free length L           %.4g inches" % (L/N))
        print("Solid length h                   %.3g inches" % h)
        print("Allowable working shear stress   %.0f kpsi" % (tau/1e3))
        print("Wahl stress factor               %.3g" % Ka(d, D))
        print("Load                             %.3g pounds" % P)
        print("Deflection                       %.3g inches" % delta)
        print("Spring constant k                %.3g lb/inch" % k)
        print("Mandrel diameter                 %s" % md)
        print()
        print(dedent(f'''
            For ordinary practice, the spring index should be from 5 to 12, with values less than 3 or 4
            unusual.  A low index indicates a stiff spring; a high value a compliant spring.
                
            This spring design assumes plain ends that are not squared.
        '''.rstrip()))
    def GetWireDiameter():
        '''This is based on the algorithm in Marv Klotz's spring.zip package
        http://www.myvirtualnetwork.com/mklotz/fckeditor/UserFiles/File/spring.zip
        See http://www.myvirtualnetwork.com/mklotz/.
        '''
        P = shop_util.GetDouble("Load in pounds?", "5", 0.001, 2000)
        OD = shop_util.GetDouble("Spring outside diameter in inches?", "0.5",
                                 0.005, 1e6)
        delta = shop_util.GetDouble("Deflection in inches?", "1", 0.001, 2000)
        H = shop_util.GetDouble("Free length of spring in inches?", "2", 0.01,
                                int(1e9))
        d = (8*P*0.8*OD*1.5/(pi*69000))**(1/3)  # First guess
        newd = 1e-9
        while (abs(d - newd)/newd) > 0.0005:
            mdia = OD - d
            wahl = 2.120672*((mdia/d)**(-0.268606))  # Wahl's constant
            s = math.floor(43094-(11037*math.log(d)))  # Allowable stess, average service
            newd = (8*P*mdia*wahl/(pi*s))**(1/3)
            d = newd
        working_stress = s
        dmin = newd
        d2 = d
        maxcoil = ((H/dmin)-1)/2
        ncoil = math.ceil((maxcoil+4)/2)
        d3 = 1e9
        while abs(d3-d2) > 0.0005:
            mdia = OD - d2
            d3 = ((8*P*ncoil*mdia**3)/(delta*g.G))**(1/4)
            d2 = (d3 + d2)/2
            if d3*(2*ncoil - 1) > H:
                ncoil -= 1
        d = d3
        try:
            pitch = H/(ncoil - 1)
        except Exception:
            print("No solution")
            sys.exit(1)
        h = ncoil*d + d
        D = OD - d
        k = P/delta
        try:
            md = "%.3g inches" % SpringMandrel(D + d, d)
        except Exception:
            md = "D/d out of range"
        print()
        print("Spring index D/d                 %.2g" % (D/d))
        print("Wire diameter d                  %.3g inches" % d)
        if d < dmin:
            print("** To meet required deflection, the spring would "
                  "be overstressed **")
        print("Mean spring diameter D           %.3g inches" % D)
        print("Spring OD                        %.3g inches" % (D + d))
        print("Spring ID                        %.3g inches" % (D - d))
        print("Number of active coils N         %d" % ncoil)
        print("Free length H                    %.3g inches" % H)
        print("Pitch at free length L           %.3g inches" % pitch)
        print("Solid length h                   %.3g inches" % h)
        print("Allowable working shear stress   %.0f kpsi" % (working_stress/1e3))
        print("Wahl stress factor               %.3g" % Ka(d, D))
        print("Load                             %.3g pounds" % P)
        print("Deflection                       %.3g inches" % delta)
        print("Spring constant k                %.3g lb/inch" % k)
        print("Mandrel diameter                 %s" % md)
        print()
        print('''For ordinary practice, the spring index should be from 5 to 12, with
    values less than 3 or 4 unusual.  A low index indicates a stiff spring; a
    high value a compliant spring.
    
    This spring design assumes plain ends not squared.
    ''')

if __name__ == "__main__": 
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if g.dbg:
        GetLoadAndDeflection()
        exit(0)
    print(dedent(f'''
    {t.title}Helical Compression Spring Design Using Steel Music Wire{t.n}
        Dimensions in inches and stress in psi.
    Choose problem:
        1.  You know wire diameter, mean spring diameter, allowable stress, spring length and
            number of active coils.  Calculate load and deflection.
        2.  You know the load, deflection, mean spring diameter, spring length, and number of
            active coils.  Calculate the wire diameter to use.

    '''.rstrip()))
    problem = shop_util.GetChoice("Problem type?", "1", ("1", "2"))
    if problem == "1":
        GetLoadAndDeflection()
    else:
        GetWireDiameter()
