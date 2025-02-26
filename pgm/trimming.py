"""
Calculate the resistance of resistor trimming circuits.
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Resistor trimming circuits
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
    if 1:  # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t

        try:
            from uncertainties import ufloat, ufloat_fromstr, UFloat

            have_unc = True
        except ImportError:
            have_unc = False
    if 1:  # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Manpage():
        print(
            dedent(f"""
        This script calculates the equivalent resistance of a trimming
        circuit and includes the adjustment range of this resistance given
        by the four resistances a, b, c, and d, where d is an adjustable
        resistance from 0 to d.  Note the equivalent resistance is
        calculated for d/2, the middle of the pot's range.

        The use case is to let you get a specific resistance value for
        resistors you have on-hand.  One use is for trimming standard
        resistors.  As an example, see the trimming circuit used in the
        ESI SR1010 transfer standard on page 4 of the manual at 
        https://www.ietlabs.com/esi-sr1010-resistance-transfer-standard.html,
        which is used to trim a 10 kΩ resistor by about ±50 ppm (parts per
        10⁶).

        Low resistor problem (default)
        ------------------------------
            Calculate R for a + (b || (c + d)) where d is a pot that ranges
            from 0 to d.  The nominal calculation will be done with d/2.

        High resistor problem
        ---------------------
            Calculate R for (a + b) || (c + d) where d is a pot that ranges
            from 0 to d.  The nominal calculation will be done with d/2.

        The parameters on the command line will be checked to see they satisfy
        these constraints:

            - All resistances must be > 0
            - a < R
            - d is a "standard" pot unless the -s option was used

        A standard pot is a value with a significand of 1, 2, or 5 and a
        multiplier of 1e1 through 1e6.  10 nor 5e5 are allowed.

        The -u option lets you use the short form uncertainty specification
        for a parameter, such as 11039.0(3), meaning the nominal value is
        11039.0 and the standard uncertainty is 0.3.  To use -u, you must
        have the python uncertainties library installed.  Note the
        calculation uses linear uncertainty propagation and assumes there
        is no correlation between the parameters.
        """)
        )
        exit(0)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] R a b c d
          Print the equivalent resistance of a resistor trimming circuit.
        Options:
            -d n    Number of significant figures [{d["-d"]}]
            -m      Print a manpage
            -h      High resistance problem
            -s      Don't require standard pot values
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-d"] = 3  # Number of significant digits
        d["-h"] = False  # High resistance problem
        d["-s"] = True  # Use standard pots
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:hms")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("hms"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o == "-m":
                Manpage()
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug

                debug.SetDebugger()
        return args


if 1:  # Core functionality

    def GetNum(s):
        """Return a float or ufloat from s, which can either be a regular float
        string like '1.23' or '1.23e9' or contain a short-form uncertainty
        as in '1.23(3)'.  Note these are the only two allowed forms.
        """
        try:
            if "(" in s and have_unc:
                return ufloat_fromstr(s)
            else:
                return float(s)
        except Exception:
            if "(" in s and not have_unc:
                print(f"Python uncertainties library not installed")
            else:
                print(f"{s!r} is not a valid number")
            exit(1)


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
