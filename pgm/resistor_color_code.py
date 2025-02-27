"""
Print resistor color code to screen
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Print resistor color code to screen
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:  # Custom imports
        from color import t
        from bidict import bidict
        from get import GetLines
        from wrap import dedent
        from dpprint import PP

        pp = PP()  # Screen width aware form of pprint.pprint
        from wsl import wsl  # wsl is True when running under WSL Linux
        # from columnize import Columnize
    if 1:  # Global variables

        class G:
            # Storage for global variables as attributes
            pass

        g = G()
        g.dbg = False
        ii = isinstance
        # Define the color coding
        g.cc = {
            #    Color    Abbrev Digit      Mult        Tolerance
            0: ("Black ", "blk", " 0", "  1  ", " --  "),
            1: ("Brown ", "brn", " 1", " 10  ", "±1   "),
            2: ("Red   ", "red", " 2", "100  ", "±2   "),
            3: ("Orange", "orn", " 3", "  1 k", "±0.05"),
            4: ("Yellow", "yel", " 4", "  1 k", "±0.02"),
            5: ("Green ", "grn", " 5", "  1 k", "±0.5 "),
            6: ("Blue  ", "blu", " 6", "  1 M", "±0.25"),
            7: ("Violet", "vio", " 7", "  1 M", "±0.1 "),
            8: ("Gray  ", "gry", " 8", "  1 M", "±0.01"),
            9: ("White ", "wht", " 9", "  1 G", " --  "),
            10: ("Gold  ", "gld", " -", " 0.1 ", "±5   "),
            11: ("Silver", "sil", " -", "0.01 ", "±10  "),
            None: ("      ", "   ", "  ", "     ", "±20  "),
        }
        g.colors = {
            0: t("blk", "gry"),
            1: t("brn"),
            2: t("red"),
            3: t("orn"),
            4: t("yel"),
            5: t("grn"),
            6: t("blu"),
            7: t("vio"),
            8: t("gry"),
            9: t("whtl"),
            10: t("#e6be8a"),
            11: t("#c9c0bb"),
            None: t("wht"),
        }
        g.letters = bidict()
        g.letters.update(
            {
                "k": 0,
                "b": 1,
                "r": 2,
                "o": 3,
                "y": 4,
                "g": 5,
                "u": 6,
                "v": 7,
                "a": 8,
                "t": 9,
                "d": 10,
                "l": 11,
            }
        )
if 1:  # Utility

    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )

    def GetColors():
        t.dbg = t("cyn") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("redl")

    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)

    Dbg.file = sys.stderr  # Debug printing to stderr by default

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] [args]
          With no arguments, print a resistor color code table.  Otherwise,
          the arguments are read and interpreted.  You can use arguments of
          blk brn red orn yel grn blu vio gry wht gld sil, the single
          letters given in the output table, or spell out the names.
        Example:
            '{sys.argv[0]} red vio grn gld' will print out This is a 2.7 MΩ
            5% resistor.
        Options:
            -h      Print a manpage
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False  # Describe this option
        d["-d"] = 3  # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o == "-h":
                Usage(status=0)
        GetColors()
        g.W, g.L = GetScreen()
        if not args:
            PrintTable()
            exit(0)
        return args


if 1:  # Core functionality

    def PrintTable():
        print(
            dedent(f"""
        IEC 60062:2016 standard resistor color codes.  The decimal point is
        implied after the last digit.  To orient left to right, there is a
        gap between the last two bands.

        """)
        )
        # Column widths
        w = (8, 14, 8, 8, 12, 14)
        # Print header
        t.print(
            f"{t('magl')}"
            f"{'':{w[0]}s}"
            f"{'Abbreviation':^{w[1]}s}"
            f"{'Letter':^{w[2]}s}"
            f"{'Digit':^{w[3]}s}"
            f"{'Multiplier':^{w[4]}s}"
            f"{'Tolerance, %':^{w[5]}s}"
        )
        # Print table
        for i in range(12):
            color, abbr, digit, mult, tol = g.cc[i]
            ltr = g.letters(i)
            t.print(
                f"{g.colors[i]}"
                f"{color:{w[0]}s}"
                f"{abbr:^{w[1]}s}"
                f"{ltr:^{w[2]}s}"
                f"{digit:^{w[3]}s}"
                f"{mult:^{w[4]}s}"
                f"{tol:^{w[5]}s}"
            )
        color, abbr, digit, mult, tol = g.cc[None]
        print(
            f"{'None':{w[0]}s}"
            f"{'':^{w[1]}s}"
            f"{'':^{w[2]}s}"
            f"{'':^{w[3]}s}"
            f"{'':^{w[4]}s}"
            f"{tol:^{w[5]}s}"
        )

    def Interpret(*args):
        """Print an interpretation of a set of colors."""


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    Interpret(*args)

"""
Note the decimal point is implied after the last digit.  The standard is
IEC 60062:2016.  To orient left to right, there is a gap between the last
two bands.
 
         Abbreviation       Digit     Multiplier    Tolerance, %
Black        blk              0           1             -
Brown        brn              1          10            ±1
Red          red              2         100            ±2
Orange       orn              3           1 k          ±0.05
Yellow       yel              4          10 k          ±0.02
Green        grn              5         100 k          ±0.5
Blue         blu              6           1 M          ±0.25
Violet       vio              7          10 M          ±0.1
Gray         gry              8         100 M          ±0.01
White        wht              9           1 G           --
Gold         gld              -          0.1           ±5
Silver       sil              -         0.01           ±10
None                                                   ±20
 
Example:  red, vio, grn, gold
    2, 7, 5, meaning 27e5 or 2.7 MΩ.  Tolerance is 5%.
"""
