'''
Print the resistor color code or interpret it
'''
 
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Print or interpret resistor color code
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        ii = isinstance
        g.clr = {}
        g.code = {
            "blk": 0,
            "brn": 1,
            "red": 2,
            "orn": 3,
            "yel": 4,
            "grn": 5,
            "blu": 6,
            "vio": 7,
            "gry": 8,
            "wht": 9,
            "gld": 0.1,
            "sil": 0.01,
        }
if 1:   # Utility
    def GetColors():
        # Put into g.clr dict
        g.clr[""] = ""
        g.clr["blk"] = t("blk", "wht")
        g.clr["brn"] = t("brn")
        g.clr["red"] = t("redl")
        g.clr["orn"] = t("ornl")
        g.clr["yel"] = t("yell")
        g.clr["grn"] = t("grnl")
        g.clr["blu"] = t("blul")
        g.clr["vio"] = t("viol")
        g.clr["gry"] = t("gry")
        g.clr["wht"] = t("whtl")
        g.clr["gld"] = t("#dbb40c")
        g.clr["sil"] = t("wht")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        d["-d"] = 3         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h", "--debug") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o == "-h":
                Usage()
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an unhandled exception
                import debug
                debug.SetDebugger()
        GetColors()
        return args
if 1:   # Core functionality
    def PrintLine(name, abbr, digit, multiplier, tolerance):
        w = {
            "name": 8,
            "abbr": 12,
            "digit": 5,
            "multiplier": 10,
            "tolerance": 12,
        }
        spc = " "*4
        if name:
            if name == "Black":
                print(f"{g.clr[abbr]}{name}{t.n}", end=spc)
                remaining = w["name"] - 5
                print(f"{' '*(w['name'] - 5)}", end="")
            else:
                print(f"{g.clr[abbr]}{name:{w['name']}s}{t.n}", end=spc)
        else:
            print(f"{'':{w['name']}s}", end=spc)
        print(f"{abbr:^{w['abbr']}s}", end=spc)
        print(f"{digit:^{w['digit']}s}", end=spc)
        print(f"{multiplier:^{w['multiplier']}s}", end=spc)
        print(f"{tolerance:^{w['tolerance']}s}")
    def PrintTable():
        PrintLine("", "Abbreviation", "Digit", "Multiplier", "Tolerance, %")
        PrintLine("Black", "blk", "0", "1", "--")
        PrintLine("Brown", "brn", "1", "10", "±1")
        PrintLine("Red", "red", "2", "100", "±2")
        PrintLine("Orange", "orn", "3", "1 k", "±0.05")
        PrintLine("Yellow", "yel", "4", "10 k", "±0.02")
        PrintLine("Green", "grn", "5", "100 k", "±0.5")
        PrintLine("Blue", "blu", "6", "1 M", "±0.25")
        PrintLine("Violet", "vio", "7", "10 M", "±0.1")
        PrintLine("Gray", "gry", "8", "100 M", "±0.01")
        PrintLine("White", "wht", "9", "1 G", "--")
        PrintLine("Gold", "gld", "--", "0.1", "±5")
        PrintLine("Silver", "sil", "--", "0.01", "±10")
        PrintLine("None", "", "", "", "±20")
    def GetClr(name, bar_width, width):
        if name == "blk":
            return f"{'⎕'*bar_width:^{width}s}"
        else:
            return f"{g.clr[name]}{'█'*bar_width:^{width}s}{t.n}"
    def Interpret(args):
        b, blk = "██", "⎕⎕"
        excess_width, bar_width, o = 1, 3, []
        width = excess_width + bar_width
        for i in args:
            o.append(GetClr(i, bar_width, width))
        print(''.join(o))
        # Show the digits
        for i in args:
            print(f"{g.code[i]!s:^{width}s}", end="")
        print()
        # Interpret the digits
        if len(args) == 1:
            print("Value = {g.code[args[0]]!} Ω")
        elif len(args) == 2:
            a, b = args
            value = g.code[a]*10**g.code[b]
            print(f"Value = {value} Ω")
        elif len(args) == 3:
            a, b, c = args
            value = (10*g.code[a] + g.code[b])*10**g.code[c]
            print(f"Value = {value} Ω")
        elif len(args) == 4:
            a, b, c, d = args
            value = g.code[int(a + b + c)]*10**g.code[d]

if __name__ == "__main__":
    d = {}      # Options dictionary
    GetColors()
    args = ParseCommandLine(d)
    if args:
        Interpret(args)
    else:
        PrintTable()
