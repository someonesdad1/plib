'''
Module to encapsulate circle packing information

    To use this module, call the function circle_packing.GetData().  This will return a
    dictionary with keys of integers > 0 that represent the number of circles inside a
    unit circle.  The values of this dictionary are namedtuples containing circle
    packing information.

    The following keyword parameters can control the nature of the dictionary you get
    returned

    N           An integer representing the maximum number of elements in the dictionary
                to be returned.  If N is 0, all elements will be returned.

    numtype     The floating point number type used to contain the information.  
                Set numtype to None and the raw information will be returned (all
                elements will be strings).  Since the raw data have 30 decimal digits,
                you'll need to use an extended floating point representation like
                python's Decimal or mpmath's mpf types if you wish to keep the
                precision.  Because most people probably won't be interested in seeing
                all the digits, the default type is flt (in /plib/f.py), as this type is
                a python float but defaults to showing only 3 figures in its string
                interpolation.  You can use any suitable numerical type that can convert
                the raw strings.

    The nametuple returned in the dictionary has the following elements (nt means the
    numtype given above)

    N           int     The number of circles
    radius      nt      The radius of the circles in the unit circle
    distance    nt      The largest distance between the circles
    ratio       nt      The reciprocal of the radius
    density     nt      Ratio of circles' area to area of unit circle
    contacts    int     Number of tangent points between all the circles
    loose       int     Number of circles whose center can move before contacting another circle
    boundary    int     Number of circles that are tangent to the unit circle
    symmetry    str     Symmetry group of packing
    reference   str     To the best-known packing so far

    Example:  
        d = GetData()
        print(d[4])
    will output:
        Entry(N=4, radius=0.41421356237309503, distance=1.4142135623730951,
              ratio=2.414213562373095, density=0.6862915010152396, contacts=8,
              loose=0, boundary=4, symmetry='D4', reference='Udo Pirl')

    The numbers mean that four circles of radius 0.414 can fit into a unit circle.
    Since the number loose is zero, this means that none of the circles' centers have any
    freedom of movement; if you look at
    http://hydra.nat.uni-magdeburg.de/packing/cci/d1.html, you'll see how the circles
    are constrained so that they can't move.  The term contacts tells you how many
    points of tangential contact these circles have with another circle, including the
    unit circle.  The boundary term tells you that four of those contact points are on
    the unit circle.  The density number tells you that the circles' area is about 69%
    of the unit circle's area.
    
    This module can also be run as a script; run it with no parameters to get a usage
    statement.

    The raw data came from http://hydra.nat.uni-magdeburg.de/packing/cci.  On 11 Jan
    2026, Eckard Specht told me in an email "you have all permissions to store, transform
    and handle the data presented at packomania.com. The website can be considered as an
    open source."  Thanks to Dr. Specht and the many researchers who have worked on the
    acquistion of these data.  Note the main web page is at http://packomania.com and
    the others are parts of it, though they use different base URLs.

    ---------------------------------------------------------------------------

    I don't need this type of information very often, but occasionally it's useful.  One
    example of use is figuring out how many wires can be put through a hole.  If you
    have a selection of different wire diameters, then you're probably on your own to
    solve it experimentally.  However, in my case, I was interested in seeing how many
    turns I could get through the center hole of a small toroidal current transformer.
    The hole diameter was 5.1 mm and the outside diameter of the silicone rubber
    insulation of the 22 AWG wire was 1.9 mm.  With the script arguments "-w 5.1 1.9",
    you'll find that 5 wires can be put through the hole.  This was correct, as I was
    just barely able to do this:  I had to put silicone grease on the tip of the wire
    for the last turn as well as in the remaining space through the hole for this wire.
    It was a tight fit, but I was able to make it work.  This demonstrates that the
    script can give practical results.

    The little current transformer in the previous paragraph sells on Amazon for around
    $2 each, with 5 in a bag.  These are nominally rated at 5 A and they come on a PC
    board with an LM358 op amp and a 10-turn pot to control the gain.  The bandwidth is
    around 3 kHz.  These make inexpensive monitors for AC line current at up to about 5
    A and you can get resolution down to around 10 mA.  Thus, this is a good tool for
    monitoring lower AC currents in appliances.

'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2014, 2026 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Circle packing information
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        from collections import namedtuple
        import csv
    if 1:  # Custom imports
        from f import flt
    if 1:  # Types
        Entry = namedtuple("Entry", '''N radius distance ratio density contacts
                           loose boundary symmetry reference'''.split())
if 1:  # Core functionality
    def GetData(maxsize=0, numtype=flt):
        '''Return a dictionary with keys of the integer number of circles in a unit
        circle; the values are the Entry named tuples containing the relevant packing
        information.
        
        If maxsize is 0, return all the on-hand data in the dictionary.  Otherwise,
        limit the size to the absolute value of maxsize).
        
        The numbers that contain decimal points will be converted to the numtype type
        keyword.  If numtype is None, they will remain as the original strings.
        '''
        if numtype is None:
            numtype = lambda x: x
        file = "circle_packing.csv"
        data = {}
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            count = 0
            for row in reader:
                N = int(row[0])
                radius = numtype(row[1])
                distance = numtype(row[2])
                ratio = numtype(row[3])
                density = numtype(row[4])
                contacts = int(row[5])
                loose = int(row[6])
                boundary = int(row[7])
                symmetry = row[8]
                reference = row[9]
                data[N] = Entry(N, radius, distance, ratio, density, contacts, loose,
                                boundary, symmetry, reference)
                count += 1
                if maxsize and count >= maxsize:
                    break
        return data

if __name__ == "__main__":
    if 1:  # Imports
        from collections import namedtuple, defaultdict
        from decimal import Decimal, getcontext
        import sys
        import os
        import getopt
    if 1:  # Custom imports
        import requests
        from f import flt
        from wrap import dedent
        from sig import sig
        from lwtest import Assert
        from color import t
        import termtables as tt
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Utility
        def GetColors():
            t.N = t.magl
            t.R = t.yell
            t.Dist = t.wht
            t.ρ = t.sky
            t.Contacts = t.pnkl
            t.Loose = t.ornl
            t.Boundary = t.brnl
        def Error(msg, status=1):
            print(msg, file=sys.stderr)
            exit(status)
        def Manpage():
            print(dedent(f'''
            Here's a practical example of the use of this script.
    
            I have a toroidal current transformer with a hole of diameter 16 mm through it.
            How many turns of 1.9 mm outside diameter wire can I get through this hole?
    
            This script prints out the maximum known number of equal-diameter circles that
            can be fit inside a unit circle.  Here, we'll assume our unit circle is the 16
            mm diameter hole.  We need to find the number of circles N that have a radius of
            1.9/16 = 0.119.  Note the ratio of the diameters is the same as the ratio of the
            corresponding radii.
    
            If you print out a table using the arguments of "-T 60", you'll see the value of
            R for N = 56 being 0.119.  This tells me I should be able to get about 56 turns
            through the coil.  R is the radius of the N equal-diameter circles that can fit
            in a unit circle.
    
            If you instead call the script with the arguments "-w 16 1.9", you'll get the
            report
    
                Hole diameter   = 16
                Wire diameter   = 1.9
                Diameter ratio  = 0.119
                Number of wires = 57
                Theoretical ratio = 0.1184
    
            which tells me that 57 wires is the number where the "theoretical ratio" is less
            than the diameter ratio.  Here, this "theoretical ratio" is the radius R in the
            -t report.
    
            With the same 1.9 mm diameter wire, how many wires can be passed through a small
            current transformer with a hole diameter of 5.1 mm?  Using the arguments "-w 5.1
            1.9", you'll get that 5 wires can be put through the hole.  This in fact is
            correct, as I was just barely able to do this, needing to put silicone grease on
            the tip of the wire for the last turn as well as in the remaining space for this
            wire.  It was a tight fit, but I was able to make it work.  This is an
            experimental demonstration that the script's data can give practical results.
            '''))
            exit(0)
        def Usage(status=1):
            name = sys.argv[0]
            digits = d["-d"]
            print(dedent(f'''
            Usage:  {name} [options] n1 [n2 ...]
              Give data on packing n1, n2, ... circles into a unit circle.  If there are no
              "loose" circles (rattlers), the loose line will be printed in color to alert
              you.  Important:  remember the diameter of a unit circle is 2; in most
              practical problems, we're interested in the diameters of the circles, so be
              careful of not making an error of factor 2.  For the -w wire problem, the two
              arguments are D and d, the hole diameter and wire diameter, respectively.
            Options:
              -a        Print all records
              -d n      Print results to the indicated number of digits. [{digits}]
              -h        Show a manpage with a practical example
              -n n      Print records from 1 to n
              -r        Print key and references
              -s        Show the raw data table; floating point numbers are shown to the number of digits
                        specified by the -d option.
              -T n      Same as -t but no key
              -t n      Print out in table form up to element n (include a key)
              -w        Wire problem:  how many wires of diameter d can fit through a circle
                        of diameter D.  The two command line arguments are D and d, in that
                        order.
            '''))
            exit(status)
        def ParseCommandLine():
            d["-a"] = False     # Print all records
            d["-d"] = 3         # Number of significant digits
            d["-n"] = None      # Show records 1 to n
            d["-s"] = False     # Show raw data
            d["-T"] = None      # Table form up to d["-T"] items
            d["-t"] = None      # Table form up to d["-t"] items
            d["-w"] = False     # Wire problem
            try:
                optlist, args = getopt.getopt(sys.argv[1:], "ad:hn:rsT:t:w")
            except getopt.GetoptError as e:
                msg, option = e
                print(msg)
                exit(1)
            for o, a in optlist:
                if o[1] in "asw":
                    d[o] = not d[o]
                elif o == "-d":
                    d[o] = int(a)
                    if d[o] < 1 or d[o] > 15:
                        Error("Number of digits must be between 1 and 15.")
                elif o == "-h":
                    Manpage()
                elif o == "-n":
                    d[o] = int(a)
                    if d[o] < 1 or d[o] > 1500:
                        Error("n must be between 1 and 1500.")
                elif o == "-r":
                    print(man)
                    exit(0)
                elif o == "-t" or o == "-T":
                    d[o] = int(a)
                    if d[o] < 0 or d[o] > 1500:
                        Error("Argument must be between 0 and 1500.")
            x = flt(0)
            x.N = d["-d"]
            x.rtz = x.rtdp = False
            ok = d["-a"] or d["-n"] or d["-s"] or d["-t"] is not None or d["-T"] is not None
            if not ok and len(args) < 1:
                Usage()
            GetColors()
            return args
    if 1:  # Core functionality
        def GetData(use_flt=True, limit_size=None, check=True):
            '''Return a dictionary of the data with the integer N as the key and a
            namedtuple as the value.  If use_flt is True, then the floating point strings
            
            use_flt     If True, strings will be returned as flt; otherwise, they will be a
                        Decimal instance that maintain the full significance.
            
            limit_size  If not None, then it must be an integer that limits the number of
                        entries in the returned dictionary.
            
            check       If True, check types and appropriateness of each entry as
                        appropriate.
            '''
            getcontext().prec = 30  # Decimal context to preserve number of digits
            results = defaultdict(namedtuple)
            Entry = namedtuple("Entry", '''
                radius
                distance
                ratio
                density
                contacts
                loose
                boundary
                symmetry
                reference''')
            numtype = flt if use_flt else Decimal
            limit_size = None if limit_size is None else abs(int(limit_size))
            Assert(limit_size is None or limit_size > 0)
            for i, line in enumerate(data.split("\n")):
                if not i:   # Ignore the first line
                    continue
                f = line.split("\t")
                Assert(len(f) == 10)    # Must have 10 fields
                N = int(f[0])
                radius = numtype(f[1])
                distance = numtype(f[2])
                ratio = numtype(f[3])
                density = numtype(f[4])
                contacts = int(f[5])
                try:
                    loose = int(f[6])
                except ValueError:
                    loose = 0
                boundary = int(f[7])
                symmetry = f[8].strip()
                try:
                    reference = int(f[9].strip().replace("[", "").replace("]", ""))
                except Exception:
                    reference = 0
                e = Entry(radius, distance, ratio, density, contacts, loose, boundary,
                          symmetry, reference)
                results[N] = e
                if check:
                    Assert(isinstance(N, int))
                    Assert(isinstance(e.radius, numtype))
                    Assert(isinstance(e.distance, numtype) or e.distance is None)
                    Assert(isinstance(e.ratio, numtype))
                    Assert(isinstance(e.density, numtype))
                    Assert(isinstance(e.contacts, int))
                    Assert(isinstance(e.loose, int))
                    Assert(isinstance(e.boundary, int))
                    Assert(isinstance(e.symmetry, str))
                    Assert(isinstance(e.reference, int) or e.reference is None)
            return results
        def Report(n, R):
            try:
                r, dist, ratio, density = [sig(i) for i in R[:4]]
            except ValueError as e:
                # This should only happen for n == 1:  dist is None
                r, dist, ratio, density = [sig(R[0]), "--", sig(R[2]), sig(R[3])]
                special = True
            contacts, loose, boundary, group, ref = R[4:]
            if not group:
                group = "C1"
            f = (r, dist, ratio, density, contacts, loose, boundary, group, ref)
            w, sp, h = max([len(str(i)) for i in f]), "  ", "  "
            if ref is None:
                ref = "--"
            t.l = t.wht if loose else t.purl
            print(dedent(f'''
                {t.ornl}Packing {t.grnl}{n}{t.ornl} circles into a unit circle:{t.n}
                {h}{r:{w}}{sp}Circle radius
                {h}{dist:{w}}{sp}Largest distance between centers
                {h}{ratio:{w}}{sp}Ratio (= 1/radius)
                {h}{density:{w}}{sp}Density (circle area to container area)
                {h}{contacts:<{w}}{sp}Contacts (number of contacts between circles & container)
                {h}{t.l}{loose:<{w}}{sp}Loose (number of circles within unit circle that can move = rattlers){t.n}
                {h}{boundary:<{w}}{sp}Boundary (number of circles with container contact)
                {h}{group:{w}}{sp}Symmetry group (Schönfliess)
                {h}{ref:<{w}}{sp}Reference
            '''))
        def ShowRecord(n, result):
            print(n, end=" ")
            for i in range(4):
                result[i] = "--" if not result[i] else sig(result[i])
                print(result[i], end=" ")
            result[7] = "--" if not result[7] else result[7]
            result[8] = "--" if not result[8] else result[8]
            print(" ".join([str(i).strip() for i in result[4:9]]))
        def WireProblem(hole_diameter, wire_diameter):
            '''Given a hole and wire diameter, how many wires can be fit through the hole?
            The two arguments must be in the same length units and wire_diameter must be
            less than hole_diameter.
            '''
            if hole_diameter <= 0:
                Error("hole_diameter must be > 0")
            if wire_diameter <= 0:
                Error("wire_diameter must be > 0")
            ratio = wire_diameter/hole_diameter
            if ratio > 1:
                Error("wire_diameter must be <= hole_diameter")
            # Solution method:  Search for the smallest N such that ratio <= R.
            found = None
            for N in results:
                entry = results[N]
                if entry.radius <= ratio:
                    found = N, entry
                    break
            if found:
                N, entry = found
                w, s = 25, " "*1
                print(f"{'Hole diameter':{w}s}{s}{hole_diameter}")
                print(f"{'Wire diameter':{w}s}{s}{wire_diameter}")
                print(f"{'Diameter ratio':{w}s}{s}{ratio}")
                t.print(f"{t.ornl}{'Number of wires':{w}s}{s}{t.grnl}{N}")
                with entry.radius:
                    entry.radius.N = d["-d"] + 1
                    print(f"{'Theoretical ratio':{w}s}{s}{entry.radius}")
        def TableKey():
            print()
            print(dedent(f'''
            {t(attr="ul")}Table key{t.n}:
              {t.N}N         Number of contained circles{t.n}
              {t.R}R         Radius of contained circles{t.n}
              {t.Dist}Dist      Greatest distance between contained circles' centers{t.n}
              {t.ρ}ρ         Ratio of contained circles' area to container area{t.n}
              {t.Contacts}Contacts  Number of contacts between circles and container{t.n}
              {t.Loose}Loose     Number of circles inside that can move (rattlers){t.n}
              {t.Boundary}∂         Number of circles touching containing circle's boundary{t.n}
            '''))
        def Table(n):
            if not n:
                n = len(results)
            header = [
                f"{t.N}N",
                f"{t.R}R",
                f"{t.Dist}Dist",
                f"{t.ρ}ρ",
                f"{t.Contacts}Contacts",
                f"{t.Loose}Loose",
                f"{t.Boundary}∂{t.n}",
            ]
            out = []
            for i in range(1, n + 1):
                nt = results[i]
                s = nt.loose if nt.loose else ""
                o = [f"{t.N}{i}", 
                     f"{t.R}{nt.radius}",
                     f"{t.Dist}{nt.distance}",
                     f"{t.ρ}{nt.density}",
                     f"{t.Contacts}{nt.contacts}",
                     f"{t.Loose}{s}",
                     f"{t.Boundary}{nt.boundary}{t.n}"
                ]
                out.append(o)
            tt.print(out, header, padding=(1, 1), style=" "*15, alignment="c"*len(header))
    # Main program code
    d = {}
    args = ParseCommandLine()
    results = GetData()
    sig.digits = d["-d"]
    if d["-a"] or d["-n"]:
        n = len(results) if d["-a"] else d["-n"]
        for i in range(1, n + 1):
            Report(i, results[i])
    elif d["-s"]:
        # Show the records in crude table form
        print("N radius distance ratio density contacts loose boundary symmetry ref")
        n = len(results) + 1
        for i in range(1, n):
            ShowRecord(i, list(results[i]))
    elif d["-t"] is not None or d["-T"] is not None:
        # Show the records in more readable table form
        if d["-T"]:
            Table(d["-T"])
        else:
            Table(d["-t"])
            TableKey()
    elif d["-w"]:
        hole_diameter = flt(args[0])
        wire_diameter = flt(args[1])
        WireProblem(hole_diameter, wire_diameter)
    else:
        for arg in args:
            try:
                n = int(arg)
            except Exception:
                Error("'%s' is not an integer." % arg)
            if n < 1 or n > len(results) - 1:
                Error("n must be > 0 and <= %d" % len(results))
            Report(n, results[n])
