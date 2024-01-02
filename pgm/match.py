'''
Print out matching characteristics of two resistors.  They are measured in
series with a voltage across them.
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
        # Print out matching characteristics of two resistors
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        from si import GetSignificantFigures, ConvertSI
        from f import flt
    if 1:   # Global variables
        ii = isinstance
        t.pct = t("ornl")
        t.ppm = t("yell")
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''
        This script calculates how close two resistors' resistances are by
        measurement:  the two resistances in series are put across a known
        voltage and the voltage drop across each resistor is measured. 

        Example:  I have two matched resistors that came from a
        differential voltmeter.  I put 21.9 V across the two resistors and
        measured their voltage drops as  10.957 V and 10.955 V using an
        Aneng 870 DMM.  Giving the arguments '10.957 10.955' to the script,
        we get

            Resistor matching:
                V1   = 10.957
                V2   = 10.955
                Mean = 10.9560 ±0.0091% (±91 ppm)
        
        showing the resistors are matched to within about 90 ppm.  Note the
        mean has one more digit than the argument with the most digits.

        If you use -1 or -2 to define the resistance of one of the
        resistors, the report changes, as it assumes the given resistance
        is a known resistance standard.  The report then states how much
        the other resistor deviates from the given resistor.  The output is
        given in Ω because the current can be calculated.

        The above Fluke resistors are stamped with the value 98.582 kΩ.
        Giving the script the arguments '-1 98.582k 10.957 10.955'
        results in

            Resistor matching:
                R1   ≝ 98582
                R2   = 98582 - 0.018% = R1 - 180 ppm

        Note you can use cuddled SI prefixes with the -1 or -2 options.
        If the arguments were '-1 98.5820k 10.957 10.955', the results are

            Resistor matching (ppm = parts per 10⁶):
                R1   ≝ 98582.0 Ω
                R2   = 98582.0 Ω - 0.02% = R1 - 200 ppm

        In this case, the results are printed to six significant figures,
        as the argument to -1 had that many figures.  The argument with the
        maximum number of significant figures is used to print out the
        results.  Thus, '-1 98.582000k 1 1.1' results in 

            Resistor matching (ppm = parts per 10⁶):
                R1   ≝ 98582.000 Ω
                R2   = 98582.000 Ω + 10% = R1 + 100000 ppm

        because the -1 argument had 7 significant figures.  Of course, the
        measured voltages don't have that many figures, so you have to
        interpret the results with that in mind.  The results represent
        arithmetical significance, not necessarily physical significance.

        When the -1 or -2 options aren't used, the V1 and V2 values are the
        strings that were given on the command line.  The number of figures
        for the mean will be the maximum number of figures in V1 and V2
        plus one.

        '''))
        exit(0)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] V1 V2
          Print matching % for two resistors in series with a voltage
          across them.  V1 and V2 are the voltages in volts across the
          resistors.
 
          If either -1 or -2 are used, the resistance value of the other
          resistor will be calculated in terms of the given resistance.
          Voltages and resistances can have cuddled SI prefixes (e.g.,
          '1.234k').
        Example:
          Arguments of '1 1.01' produce
            Resistor matching:
                V1   = 1
                V2   = 1.01
                Mean = 1.005 ±0.5% (±5000 ppm)
        Options:
            -1 R    Define resistance of first resistor
            -2 R    Define resistance of second resistor
            -d n    Number of significant figures in % and ppm [{d['-d']}]
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["n"] = 0          # Number of digits for -1 or -2
        d["-1"] = None      # First resistor
        d["-2"] = None      # Second resistor
        d["-d"] = 2         # Number of significant digits in % or ppm
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "1:2:d:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-1":
                d[o] = ConvertSI(a)
                d["n"] = GetSignificantFigures(a)
                if d[o] <= 0:
                    Error(f"-1's value must be > 0")
                if d["-2"] is not None:
                    Error(f"-2 cannot be used if -1 is")
            elif o == "-2":
                d[o] = ConvertSI(a)
                d["n"] = GetSignificantFigures(a)
                if d[o] <= 0:
                    Error(f"-2's value must be > 0")
                if d["-1"] is not None:
                    Error(f"-1 cannot be used if -2 is")
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o == "-h":
                Manpage()
        if len(args) != 2:
            Usage()
        return args
if 1:   # Core functionality
    def Strip(s):
        'Remove letters/signs to make a float an integer significand'
        for i in ".,eE+-":
            s = s.replace(i, "")
        return s
    def Report(s1, s2):
        's1 and s2 are the strings the user entered for the voltages'
        # Get number of digits to use in numbers
        n = max(GetSignificantFigures(s1), GetSignificantFigures(s2))
        flt(0).N = n
        flt(0).rtz = False
        flt(0).high = 1e6
        V1, V2 = ConvertSI(s1), ConvertSI(s2)
        mean = (V1 + V2)/2
        halfwidth = abs(V1 - V2)/2
        if not mean:
            Error("One of the values is zero")
        cov = halfwidth/mean
        pct = 100*cov
        ppm = 1e6*cov
        # Print data
        print(f"Resistor matching (ppm = parts per 10⁶):")
        if d["-1"] or d["-2"]:
            # One of the resistors was defined
            V1.N = max(d["n"], n)
            if d["-1"]:
                i = flt(V1/d["-1"])
                R1, R2 = V1/i, V2/i
                diff = R2 - R1
                sgn = "-" if diff < 0 else "+"
                pct = 100*abs(diff)/R1
                ppm = 1e4*pct
                pct.n, ppm.n = d["-d"], d["-d"]
                print(f"  R1   ≝ {R1} Ω")
                print(f"  R2   = {R1} Ω {t.pct}{sgn} {pct}%{t.n} = R1 {t.ppm}{sgn} {ppm} ppm{t.n}")
            else:
                i = V2/d["-2"]
                R1, R2 = V1/i, V2/i
                diff = R1 - R2
                sgn = "-" if diff < 0 else "+"
                pct = 100*abs(diff)/R2
                ppm = 1e4*pct
                pct.n, ppm.n = d["-d"], d["-d"]
                print(f"  R1   = {R2} Ω {t.pct}{sgn} {pct}%{t.n} = R2 {t.ppm}{sgn} {ppm} ppm{t.n}")
                print(f"  R2   ≝ {R2} Ω")
        else:
            mean.N = n + 1  # One more digit than components
            print(f"  V1   = {s1}")
            print(f"  V2   = {s2}")
            print(f"  Mean = {mean} ", end="")
            pct.n, ppm.n = d["-d"], d["-d"]
            print(f"{t.pct}± {pct}%{t.n} = {mean} {t.ppm}± {ppm} ppm{t.n}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    Report(*args)
