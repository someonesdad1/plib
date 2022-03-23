'''
Construct the rgbdata.py file.  This file is a list of color names
and Color objects encapsulating the RGB color.  Write the constructed data
to stdout.
'''
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
    from collections import deque
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    from rgb import Color
    if 0:
        import debug
        debug.SetDebugger()
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
            c = Color(color)
            out.append((attrnum, name, c))
            #print(f"{name:20s} [{attrnum}]", color, c)
        return out, attr
    def Report(data, attrdict):
        'Write output in form of python list and dict'
        # List of colors
        if 1:
            print(dedent(f'''
            from rgb import Color
                # Fields are:
                #   Attribution number (indexes into attrdict)
                #   Text name of color
                #   Color object holding the color data (the .rgb attribute
                #      gives the decimal values of the RGB numbers)
            '''))
            print("color_data = [")
            last = (1, 0, 0)
            for i in data:
                if i[0] != last[0]:     # Space after attribution number change
                    print()
                    last = i
                print(f"    {i},")
            print("]")
        # Attribution data
        print(dedent(f'''

        # Attribution dictionary:  the integer key is the color name
        # attribution in the above list, the value is the attribution
        # string.  These python scripts are in the /plib/rgb directory.
        '''))
        print("attr_data = {")
        for i in attrdict:
            print(f"    {i}: {attrdict[i]},")
        print("}")
        exit()

if __name__ == "__main__":
    d = {}      # Options dictionary
    file = ParseCommandLine(d)
    data, attrdict = GetData(file)
    Report(data, attrdict)
