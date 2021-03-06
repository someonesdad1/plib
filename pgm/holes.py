'''
Given a textfile of circle diameters (separated by whitespace), space
these circles equally around a circle whose diameter is given on the
command line.
'''
if 1:  # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2013 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Space holes equally around a circle
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        import sys
        import os
        import getopt
        import math
        #from math import *
        from pdb import set_trace as xx
    # Custom imports
        from wrap import dedent
        from sig import sig
        from f import flt
        have_g = False
        try:
            # This option library can generate a PostScript plot of the layout
            from g import *  
            have_g = True
        except ImportError:
            pass
    # Global variables
        ii = isinstance
        r2d = 180/math.pi
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] datafile diameter
        Will print a table of positions (Cartesian, angles, and chords) of
        the centers of the circles whose diameters are given in the datafile
        (one number per line) so that the angle between each of the circles
        is a constant.  There are no implied units for the dimensions; use 
        a consistent unit for your problem.
        
        The datafile may contain lines of the form 'a = b' which causes a
        variable named a to be defined.  This variable can then be used in
        subsequent lines.  b is a valid python expression.  All the symbols
        from the math module are in scope.  These assignment lines must be one
        per line.  The diameter of the main circle (or the line length for the
        linear problem) is defined to be the symbol D.  Then a single
        circle diameter must be on each line (expressions allowed).
        
        If you have the optional graphics library from
        https://github.com/someonesdad1/plib, the script can generate a
        scaled drawing of the layout.
        
        The -l option causes the layout of the circles to be on a straight
        line.  The diameter on the command line then becomes the distance
        between the circle's edges.  An example of use is to lay out the holes
        to drill in a block of wood to hold a set of sockets.
        
        Options:
          -d n  Number of significant figures in results [{d['-d']}]
          -g f  Generate a Postscript drawing to file f
          -l    Lay out the circles on a line.  The diameter on the command line 
                is the distance between the edges of the circles.
          -r    Lay out the circles in a clockwise direction (the default
                direction is counterclockwise).
        Example:  suppose the datafile contains
            1/4
            5/16
            3/8
            7/16
            1/2
        Running the script with the diameter 2 gives the output
        
        Main circle diameter = 2.000
                                                Polar ang.,                Ang. width,
            Dia           x             y        degrees       Chord        degrees
        -----------------------------------------------------------------------------
            0.2500       1.000        0.           0.           1.097       14.36
            0.3125       0.3982       0.9173      66.53         1.149       17.98
            0.3750      -0.7277       0.6859     136.7          1.201       21.61
            0.4375      -0.8616      -0.5075     210.5          1.252       25.27
            0.5000       0.3086      -0.9512     288.0          1.176       28.96
        
        Angle subtended by all circles = 108.2 deg = 1.888 rad
        Gap angle between each circle  = 50.36 deg = 0.8790 rad
        
        Running the script with the same command line arguments '-l datafile 0.2'
        gives the output
        
            Linear hole placement problem for line 
            L = distance between circle edges = 0.2
                                                            Hole
                    i            x         Dividers        Diameter
                --------      --------     --------        --------
                    0           0.000        0.000            0.25  
                    1           0.4813       0.4813          0.3125 
                    2           1.025        0.5437          0.375  
                    3           1.631        0.6062          0.4375 
                    4           2.300        0.6687           0.5   
            Sum of diameters = 1.875
            Number of lengths L between holes = 4
            Overall length = 2.675
        
        The number under the Dividers column is the distance to set your
        dividers to in order to scribe the hole location from the previous hole
        location (Dividers[i] = x[i] - x[i-1]).
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 4         # Number of significant figures in results
        d["-g"] = None      # Construct a Postscript drawing of output
        d["-l"] = False     # Linear layout instead of circular
        d["-r"] = False     # Go in clockwise direction
        d["warn_ratio"] = 0.9   # When to warn about a circle's diameter
        if len(sys.argv) < 2:
            Usage(d)
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "d:g:lr")
        except getopt.GetoptError as e:
            msg, option = e
            print(msg)
            exit(1)
        for o, a in optlist:
            if o == "-a":
                d["-a"] = not d["-a"]
            elif o == "-b":
                d["-b"] = a
            elif o == "-d":
                d["-d"] = int(a)
                if d["-d"] < 1:
                    Error("-d option must be integer > 0")
            elif o == "-g":
                d["-g"] = a
            elif o == "-l":
                d["-l"] = not d["-l"]
            elif o == "-h":
                Usage(d, status=0)
            elif o == "-r":
                d["-r"] = not d["-r"]
        if len(args) == 1:
            Error("Need a diameter/length as a second argument")
        if len(args) != 2:
            Usage(d)
        flt(0).n = d["-d"]
        return args
if 1:   # Utility
    def ReadDatafile(__datafile, __d):
        '''Return the variables the user defined along with the diameters
        of the circles.
        '''
        # Note:  the double underscores for variable names are used so
        # that those names can be removed from the locals() dictionary to
        # return a dictionary of the variables the user defined.
        __lines = [__i.strip() for __i in open(__datafile).readlines()]
        __diameters = []
        __msg = "Error in line %d:\n"
        __msg += "  Line:  '%s'"
        __msg += "  Error:  %s"
        D = __d["diameter"]
        for __num, __line in enumerate(__lines):
            __linenum = __num + 1
            __line = __line.strip()
            if not __line or __line[0] == "#":
                continue
            try:
                if "=" in __line:
                    # An assignment statement -- put into the local namespace
                    exec(__line)
                else:
                    # It's an expression for a diameter
                    __x = eval(__line)
                    __diameters.append(__x)
            except Exception as __e:
                Error(__msg % (__linenum, __line, str(__e)))
        # Get the locals dictionary, delete the items that begin with two
        # underscores, and return it.
        vars, rm = locals(), []
        for i in vars:
            if len(i) > 2 and i[:2] == "__":
                rm.append(i)
        for i in rm:
            del vars[i]
        __d["vars"] = vars
        __d["diameters"] = [flt(i) for i in __diameters]
        return __diameters
    def Fmt(x, d):
        '''Return string representation of the number x.  If it's an
        integer, just return its string.  Otherwise, assume it's a flt.
        '''
        if ii(x, int):
            return str(x)
        elif ii(x, flt):
            return str(x)
        else:
            return str(flt(x))
    def SolveProblem(diameters, d):
        '''diameters is a list of the circle diameters desired to be
        placed evenly spaced on a circle of diameter d["diameter"].
        Compute the gap angle in radians, then return a list of tuples of
        the form
            (diameter, x, y, polar_angle, chord_to_next, angle_subtended)
        where diameter is the circle diameter, (x, y) are the Cartesian
        coordinates of the center of the circle (will be on the main
        circle), angle is the polar angle of the circle's center (the
        first circle is defined to have zero polar angle), and
        chord_to_next is the distance to the center of the next circle.
        '''
        R = flt(d["vars"]["D"]/2)
        n = len(diameters)
        theta_total = flt(0)
        results = []
        neg = -1 if d["-r"] else 1
        # Calculate angular widths
        for dia in diameters:
            r = flt(dia)/2
            a = (R/r)**2
            if a < 1:
                msg = f"Circle with diameter {dia} too large"
                Error(msg)
            # Angular width of this circle
            thetai = flt(neg*2*math.atan(1/math.sqrt(a - 1)))
            theta_total += flt(abs(thetai))
            results.append([flt(dia), 0, 0, 0, 0, thetai])
        if theta_total > 2*math.pi:
            Error("No solution possible")
        # Number of gaps is equal to the number of circles
        gap = flt((2*math.pi - theta_total)/n)
        d["gap"] = gap
        d["theta_total"] = theta_total
        # Calculate polar angle of each circle center.  The first circle
        # will always be on the x axis.
        results[0][3] = 0
        for i in range(1, len(diameters)):
            theta = flt(abs(results[i - 1][5]/2) + abs(gap) + abs(results[i][5]/2))
            results[i][3] = flt(neg*(theta + abs(results[i - 1][3])))
        # Calculate the Cartesian coordinates of the circles' centers
        for i in range(len(results)):
            theta = flt(results[i][3])
            results[i][1] = flt(R*math.cos(theta))
            results[i][2] = flt(R*math.sin(theta))
        # Calculate chords
        for i in range(len(results)):
            # j is index of next circle (note it has to wrap around if i
            # is the last circle in the list).
            j = i + 1 if i != len(results) - 1 else 0
            x1, y1 = flt(results[i][1]), flt(results[i][2])
            x2, y2 = flt(results[j][1]), flt(results[j][2])
            chord = flt(math.hypot(x1 - x2, y1 - y2))
            results[i][4] = chord
        return results
    def Plot(results, diameters, d):
        def SetUp(file, orientation=landscape, units=inches):
            '''Convenience function to set up the drawing environment and
            return a file object to the output stream.
            '''
            ofp = open(file, "w")
            ginitialize(ofp, wrap_in_PJL=0)
            setOrientation(orientation, units)
            return ofp
        # We'll assume US letter-size paper.  Change the width W and the
        # height H if you wish to plot to another paper size.
        SetUp(d["-g"], orientation=landscape, units=inches)
        W, H, n = 11, 8.5, len(diameters)
        margin = 0.5
        # Put origin at center of page
        translate(W/2, H/2)
        # Draw coordinate axes
        r = 0.45*H
        LineType(little_dash)
        LineColor(gray(0.5))
        line(-r, 0, r, 0)
        line(0, -r, 0, r)
        LineType(solid_line)
        LineColor(black)
        # Text characteristics
        T = 0.15
        t = T/3
        TextSize(T)
        TextName(SansBold)
        # Dimensions of plotting viewport
        w, h = W - 2*margin, H - 2*margin
        r = max(diameters)/2
        R = d["vars"]["D"]/2
        # Scale things so that all circles will fit on page
        S = h/(2*(r + R))
        scale(S, S)
        move(0, 0)
        # Draw main circle
        circle(2*R)
        x, y = -w/2, h/2 - margin
        move(x/S, y/S)
        TextLines((
            "Main circle dia = " + sig(2*R),
            "Chords in red",
            "Gap angle = " + sig(d["gap"]*r2d) + " deg",
        ))
        # Plot small circles
        for i in range(len(results)):
            dia, x, y, theta, chord, thetai = results[i]
            move(x, y)
            line(0, 0, x, y)
            circle(dia)
            # Label with diameter
            push()
            rotate(theta*r2d)
            x = R + dia/2 + t/S
            move(x, -t/S)
            text(sig(dia))
            move(R/2, t/(2*S))
            ctext(sig(theta*r2d))
            if 0:
                TextName(Symbol)
                text(chr(176))
            else:
                text(" deg")
            pop()
            # Label with chord
            push()
            next = results[(i + 1) % n][3] + 2*math.pi*(not ((i + 1) % n))
            current = results[i][3]
            dtheta = (next - current)/2
            rotate((theta + dtheta)*r2d)
            x = R*0.75
            TextColor(red)
            move(x, -t/S)
            text(sig(chord))
            pop()
    def LinearProblem(diameters, d):
        '''Solve the problem of the diameters along a straight line.  
        Given r = [r_0, r_1, ..., r_(n-1)] and L, then the abscissa of the
        point i for i > 0 is
            
            x_i = x_(i-1) + r_(i-1) + L + r_i
     
        and x_0 = 0.
        '''
        L = d["vars"]["D"]
        x = flt(0)
        print(dedent(f'''
        Linear hole placement problem for line 
          L = distance between circle edges = {L}
          x = distance from origin (x = 0) of hole centers
          Results to {x.n} significant figures
        '''))
        r = [i/2 for i in diameters]
        print('''
                                                     Hole
            i            x         Dividers        Diameter
        --------      --------     --------        --------'''[1:])
        f = "     {:^8d}      {:^8s}     {:^8s}        {:^8s}"
        g = lambda x, n: "{:^8.{}f}".format(x, n)
        g = lambda x: f"{x!s:^8}"
        lastx = x
        for i, dia in enumerate(diameters):
            if i:
                x +=  r[i-1] + L + r[i]
            div = x - lastx
            if 0:
                if n is not None:
                    print(f.format(i, g(x, n), g(div, n), g(dia, n)))
                else:
                    print(f.format(i, sig(x), sig(div), sig(dia)))
            else:
                print(f.format(i, g(x), g(div), g(dia)))
            lastx = x
        S = flt(sum(diameters))
        N = len(diameters) - 1
        oal = S + N*L
        with oal:
            oal.n = 3
            need = str(oal + 4*L)
        print(dedent(f'''
            S = sum of diameters = {sum(diameters)}
            L = distance between hole edges = {L}
            N = Number of lengths L between holes = {len(diameters) - 1}
            OAL = Overall length = S + N*L = {S} + {N}*{L} = {S + N*L}
                           = outside distance of outermost holes
            With a border of 2*L on either end, you'll need a chunk of material
            that's OAL + 4*L = {need}.
        '''))
        exit(0)
    def PrintReport(results, diameters, d):
        R = flt(d["vars"]["D"]/2)
        print(f"Main circle diameter = {2*R}")
        for dia in diameters:
            r = dia/2
            if r/R > d["warn_ratio"]:
                print("  Warning:  large diameter circle: ", Fmt(dia, d))
        w = 12
        #sig.fit = w = 12
        #sig.dp_position = sig.fit//2
        print(" "*37, "Polar angle,", " "*12, "Angular width,")
        s = "Dia x y degrees Chord degrees"
        print(" "*4, end="")
        print("{0:14}{1:14}{2:9}{3:14}{4:13}{5}".format(*s.split()))
        print("-"*78)
        for item in results:
            dia, x, y, theta, chord, thetai = item
            if 0:
                sdia = sig(dia)
                sx = sig(x)
                sy = sig(y)
                stheta = sig(theta*r2d)
                schord = sig(chord)
                sangle = sig(abs(thetai*r2d))
                s = ("{sdia:{w}} {sx:{w}} {sy:{w}} {stheta:{w}} "
                    "{schord:{w}} {sangle:{w}}")
                print(s.format(**locals()))
            else:
                theta = flt(math.degrees(theta))
                chord = flt(chord)
                angle = flt(abs(math.degrees(thetai)))
                print(f"{dia!s:^{w}} {x!s:^{w}} {y!s:^{w}} {theta!s:^{w}} "
                      f"{chord!s:^{w}} {angle!s:^{w}}")
        #sig.fit, n = 0, len(diameters)
        n = len(diameters)
        print()
        print("Number of circles              =", n)
        gap = abs(d["gap"])
        print("Gap angle between each circle  =", Fmt(math.degrees(gap), d), "deg",
              "=", Fmt(gap, d), "rad")
        tga = gap*n
        print("Total gap angle                =", Fmt(math.degrees(tga), d), "deg", "=",
              Fmt(tga, d), "rad")
        ac = d["theta_total"]
        print("Angle subtended by all circles =", Fmt(math.degrees(ac), d), "deg", "=",
              Fmt(ac, d), "rad")
        ta = tga + ac
        print("Total angle", " "*20, Fmt(math.degrees(ta), d), "deg", "=", Fmt(ta, d), "rad")

if __name__ == "__main__":
    d = {}      # Options dictionary
    datafile, diameter = ParseCommandLine(d)
    try:
        d["diameter"] = float(eval(diameter))
    except Exception as e:
        msg = "Command line diameter '%s' couldn't be evaluated:\n"
        msg += "  Error:  %s"
        Error(msg % (diameter, str(e)))
    diameters = ReadDatafile(datafile, d)
    if d["-l"]:
        LinearProblem(diameters, d)
    results = SolveProblem(diameters, d)
    PrintReport(results, diameters, d)
    if d["-g"]:
        Plot(results, diameters, d)
