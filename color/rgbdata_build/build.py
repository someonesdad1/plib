'''
Construct the rgbdata.py file.  This file is a list of color names
and Color objects encapsulating the RGB color.  Write the constructed data
to stdout.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Build the rgbdata.py file's information
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        import time
        from collections import deque
        from pdb import set_trace as xx
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color as C
    if 1:   # Global variables
        ii = isinstance
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] data_file
          Builds the data file from the data file.  Write the information
          to stdout.
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h", "help")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        if len(args) != 1:
            Usage()
        return args[0]
if 1:   # Core functionality
    class Color:
        def __init__(self, r, g, b):
            self.rgb = (r, g, b)
        def __str__(self):
            f = lambda x: f"{x:3d}"
            r, g, b = self.rgb
            return f"Color({f(r)}, {f(g)}, {f(b)})"
        def __repr__(self):
            return str(self)
    def GetData(file):
        datafile = P(file)
        if not datafile.exists():
            Error(f"Can't read {datafile}")
        lines = deque(open(datafile).read().split("\n"))
        # Output format will be a list of lines.  Each element in out will
        # be a tuple of (attrnum, color_name, color_spec) where attrnum is
        # a number that indexes the color's location in a datafile; this
        # number and the attribution string are in the dict attr.
        # color_name is a string and color_spec is an RGB spec of the form
        # '#xxyyzz'.
        out, attr, attrnum, linenum, trigger = [], {}, 0, 0, "'''"
        while lines:
            line = lines.popleft()
            linenum += 1
            got_attr = False
            if line.startswith(trigger):
                # First line of an attribution
                got_attr = True
                a = [line]
                attrnum += 1
                while lines:
                    line = lines.popleft()
                    a.append(line)
                    if line.endswith(trigger):
                        attr[attrnum] = '\n'.join(a)
                        break
            if got_attr or not line:
                continue
            name, color = line.split(",")
            color = color.strip()
            a = hex_to_int(color)
            c = Color(*a)
            out.append((attrnum, name, c))
            #print(f"{name:20s} [{attrnum}]", color, c)
        return out, attr
    def hex_to_int(s):
        's is of the form #000000'
        assert(len(s) == 7)
        s = s[1:]
        rgb = s[0:2], s[2:4], s[4:6]
        return tuple(int(i, 16) for i in rgb)
    def GetHueCategory(color_instance):
        'Return a hue category string for the color instance'
        h = color_instance.ihsv[0]
        if 5 <= h <= 15:
            return "redorn"
        elif 16 <= h <= 26:
            return "orn"
        elif 27 <= h <= 36:
            return "ornyel"
        elif 37 <= h <= 48:
            return "yel"
        elif 49 <= h <= 69:
            return "yelgrn"
        elif 70 <= h <= 97:
            return "grn"
        elif 98 <= h <= 118:
            return "grncyn"
        elif 119 <= h <= 136:
            return "cyn"
        elif 137 <= h <= 154:
            return "cynblu"
        elif 155 <= h <= 177:
            return "blu"
        elif 178 <= h <= 187:
            return "vio"
        elif 188 <= h <= 201:
            return "viomag"
        elif 202 <= h <= 222:
            return "mag"
        elif 223 <= h <= 243:
            return "magred"
        elif (0 <= h <= 4) or (244 <= h <= 255):
            return "red"
        else:
            raise ValueError(f"{h} is a bad hue number")
    def Report(data, attrdict):
        'Write output in form of python list and dict'
        myname = P(sys.argv[0]).resolve()
        # List of colors
        if 1:
            print(dedent(f'''
            # This file was constructed by {myname}
            # {time.asctime()}
            #
            # It is a list of color names compiled from a number of web
            # sources.  There are over 10,000 color names with a number of
            # duplicates, demonstrating a lot of copying over the years.  The
            # progenitor of much of this information was the rgb.txt file on 
            # early XWindows systems.

            from color import Color

            # Fields are:
            #   Attribution number (indexes into attribution_dict)
            #   Text name of color
            #   Color object holding the color data 
            #   Hue category string (there are 15 hue categories:  red, redorn, orn, ornyel, yel,
            #   yelgrn, grn, grncyn, cyn, cynblu, blu, vio, viomag, mag, magred))

            '''))
            print("color_data = [")
            last = (1, 0, 0)
            for i in data:
                if i[0] != last[0]:     # Space after attribution number change
                    print()
                    last = i
                attr, name, c = i
                # Make c a 'real' color.py:Color instance
                clr = C(*c.rgb)
                n = f'"{name}"'
                print(f"    ({attr:2d}, {n:44s}, {c}, {GetHueCategory(clr)!r}),")
            print("]")
        # Attribution data
        print(dedent(f'''

        # Attribution dictionary:  the integer key is the color name
        # attribution in the above list, the value is the attribution
        # string.  These python scripts are in the 
        # {myname.parent} directory.
        '''))
        print("attribution_dict = {")
        for i in attrdict:
            print(f"    {i}: {attrdict[i]},")
        print("}")
        exit()

if __name__ == "__main__":
    d = {}      # Options dictionary
    file = ParseCommandLine(d)
    data, attrdict = GetData(file)
    Report(data, attrdict)
