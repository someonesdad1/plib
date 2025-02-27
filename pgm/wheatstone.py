"""
Calculation of Wheatstone bridge problems
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Wheatstone bridge problems
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
    if 1:  # Custom imports
        from wrap import wrap, dedent
        from f import flt
        from color import t

        try:
            from uncertainties import ufloat, ufloat_fromstr, UFloat

            have_unc = True
        except ImportError:
            have_unc = False
        if 1:
            import debug

            debug.SetDebugger()
    if 1:  # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        t.x = t("grnl")
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Manpage():
        print(
            dedent(f"""
        Use of the Wheatstone bridge script
        """)
        )
        exit(0)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] R1 R2 R3 Vin [Vout]
          Calculate the unknown resistance Rx of a Wheatstone bridge.  Left
          arm of bridge is R1 and R3.  Right arm is R2 and Rx.  +Vin is
          applied to the common connection of R1 and R2 and -Vin is applied
          to the common connection of R3 and Rx.  If Vout is not given, it
          is assumed the bridge is balanced (i.e., Vout = 0).  With the -u
          option, you can use the short-form notation for uncertainty as
          e.g. 1.00(3) to mean 1.00 ± 0.03 where 0.03 is the standard
          uncertainty.

          Voltages are in volts and resistances are in ohms.
        Options:
            -h      Print a manpage
            -u      Allow uncertainties
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-d"] = 3  # Number of significant digits
        d["-u"] = False  # Allow uncertainties
        d["-v"] = False  # Debugging output
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:huv")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("uv"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o in ("-h", "--help"):
                Manpage()
        if not d["-u"]:
            global have_unc
            have_unc = False
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
            print(f"{s!r} is not a valid number")
            exit(1)

    def Calculate(R1, R2, R3, Vin, Vout):
        a = (R1 + R2) * Vout / Vin
        Rx = (R2 * R3 + a) / (R1 - a)
        if Rx <= 0:
            Error("Unphysical input resulted in Rx <= 0")
        return Rx

    def P(x):
        """Return a string for the float or ufloat x.  The first string is the short
        form and the second is the % level of the uncertainty.  Otherwise
        just return the number to the desired number of decimal places.
        """
        if ii(x, UFloat):
            s1 = f"{x:fS}"
            m, s = flt(x.n), flt(x.s)
            p = flt(100 * s / m)
            loc = s1.find("(")
            if s:
                return f"{s1} = {s1[:loc]} ± {p}%"
            else:
                return f"{s1} = {s1[:loc]} ± {p}%"
        else:
            # return f"{x:.{d['-d']}e}"
            return f"{x}"

    def Report(R1, R2, R3, Rx, Vin, Vout):
        print(f"Vin  = {P(Vin)}")
        print(f"Vout = {P(Vout)}")
        print(f"R1   = {P(R1)}")
        print(f"R2   = {P(R2)}")
        print(f"R3   = {P(R3)}")
        t.print(f"{t.x}Rx   = {P(Rx)}")


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    R1 = GetNum(args[0])
    R2 = GetNum(args[1])
    R3 = GetNum(args[2])
    Vin = GetNum(args[3])
    Vout = GetNum(args[4]) if len(args) == 5 else GetNum("0")
    assert R1 > 0
    assert R2 > 0
    assert R3 > 0
    assert Vin > 0
    assert Vout >= 0
    assert Vout < Vin
    Rx = Calculate(R1, R2, R3, Vin, Vout)
    Report(R1, R2, R3, Rx, Vin, Vout)
