'''
Help with planning road trips
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
        # Help with planning road trips.
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        from pprint import pprint as pp
        import sys
    if 1:   # Custom imports
        import get
        from util import Cumul
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from f import flt
        from lwtest import Assert
        from color import t
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        delimiter = "|"
        # Design:  use a datafile to control printout.  Here's for going
        # from Boise to Spokane via I84, Pendleton, Kennewick, up 394 to
        # I90, then to Spokane.  '|' is the field separator, giving the
        # fields as city, state, mileage.
        data = '''
            Boise         | ID | 0
            Ontario       | OR | 56.7
            Huntington    | OR | 29.3
            Durkee        | OR | 20.9
            Baker City    | OR | 23.8
            North Powder  | OR | 20.5
            La Grande     | OR | 25
            Pendleton     | OR | 50.6
            Umatilla      | OR | 42.1
            Kennewick     | WA | 27.6
            Connell       | WA | 39.4
            Ritzville     | WA | 41.7
            Sprague       | WA | 25
            Spokane       | WA | 36.6
            The Y         | WA | 6
        '''
        vehicles = {
            1: {
                "name": "2011 Suburban",
                "mpg": 13.5,
                "gallons": 26,
            },
            2: {
                "name": "2008 Subaru",
                "mpg": 20,
                "gallons": 16.9,
            },
        }
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] file
          Print mileage table for a trip given by the data in file.  The
          file's format is one city per line, followed by two character
          state and mileage from the previous city.
        Options:
            -c x    Cost of gasoline in $/gallon [{d["-c"]}]
            -D      Debug mode
            -h      Print a manpage
            -m x    Mileage of vehicle in miles/gallon [{d["-m"]}]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = 4         # Cost of gas in $/gallon
        d["-D"] = False     # Debug
        d["-l"] = False     # List vehicles
        d["-v"] = 1         # Which vehicle
        try:
            opts, args = getopt.getopt(sys.argv[1:], "c:Dhv:", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("Dl"):
                d[o] = not d[o]
            elif o == "-c":
                d[o] = flt(a)
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o == "-v":
                d[o] = int(a)
                if d[o] not in vehicles:
                    Error(f"{d[o]} is not a valid vehicle number")
        if d["-l"]:
            ListVehicles()
        if not args and not d["-D"]:
            Usage()
        return args
if 1:   # Core functionality
    def ListVehicles():
        for i in vehicles:
            di = vehicles[i]
            print(f"{i:2d} {di['name']}: {di['mpg']} mpg, {di['gallons']} gallons")
    def GetCol(n, lst):
        'Return column n (0-based) of lst'
        return [i[n] for i in lst]
    def GetPath(lines):
        '''Return a list of the path being traveled.  Each element will be
        [city_name, city_state, miles] where the first two items are
        strings and the last is an integer.
        '''
        o = []
        for line in lines:
            f = [i.strip() for i in line.split(delimiter)]
            if not f:
                continue
            if len(f) != 3:
                Error(f"{line!r} doesn't have 3 fields")
            miles = int(round(float(f.pop()), 0))
            f.append(miles)
            o.append(f)
        return o
    def PrintTable(path):
        cities = GetCol(0, path)
        w = max(len(i) for i in cities)
        states = GetCol(1, path)
        miles = GetCol(2, path)
        cumul = Cumul(miles, check=True)
        # Get reverse direction arrays
        rmiles = miles.copy()
        # Put initial mileage on end
        first = rmiles.pop(0)
        assert(not first)   # Make sure it's zero
        rmiles.append(first)
        rmiles = list(reversed(rmiles))
        rcumul = Cumul(rmiles, check=True)
        # Reverse them to get in correct order
        rmiles = list(reversed(rmiles))
        rcumul = list(reversed(rcumul))
        w = max(len(i) for i in cities)
        u = 10
        # Print report
        print(f"{'City':^{w}s} ST   {'To':^{u}s}  {'From':^{u}s}")
        print(f"{'-'*w:^{w}s} --   {'-'*u}  {'-'*u}")
        for i in range(len(cities)):
            print(f"{cities[i]:{w}s} {states[i]:2s}   "
                  f"{miles[i]:>4d}  "
                  f"{cumul[i]:>4d}  "
                  f"{rmiles[i]:>4d}  "
                  f"{rcumul[i]:>4d}")
        # Print gas cost and gallons used
        v = vehicles[d["-v"]]
        mi = flt(cumul[-1])
        capacity_gal = v['gallons']
        mpg = v['mpg']
        dpg = d["-c"]
        print(f"\n{v['name']} {mpg} mpg, {capacity_gal} gal tank")
        gal = flt(mi/mpg)
        cost = flt(dpg*gal)
        print(f"  Gallons used      {gal}")
        print(f"  Cost of gas       ${cost}")
        # Driving time
        print(f"Driving time, hours")
        print(f"{mi/75:>6.1f} @ 75 mph")
        print(f"{mi/70:>6.1f} @ 70 mph")
        print(f"{mi/65:>6.1f} @ 65 mph")
        print(f"{mi/60:>6.1f} @ 60 mph")

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        lines = get.GetLines(P(file), ignore=[], script=True, ignore_empty=True, strip=True)
        path = GetPath(lines)
        PrintTable(path)
