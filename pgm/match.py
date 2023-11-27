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
        # Program description string
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
        from si import GetSignificantFigures
        from f import flt
    if 1:   # Global variables
        ii = isinstance
        t.pct = t("ornl")
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''
        This script is used to assess how close two resistors' resistances
        are.  The primary use case is putting two resistances in series
        across a known voltage, then measuring the voltage drop across each
        resistor.  

        Example:  I have two precision Fluke resistors that came from an
        893A differential voltmeter.  I put the maximum output of my HP
        E3615A power supply across these two resistors in series, which is
        about 21.9 V.  The measured voltages across the two resistors were 
        10.957 V and 10.955 V, measured with an Aneng 870 DMM.  Using the
        arguments '10.957 10.955' to the script, we get

            Resistor matching:
                v1   = 10.957
                v2   = 10.955
                Mean = 10.956 ±0.0091% (±91 ppm)
        
        This shows the resistors are matched to within about 90 ppm.

        If you use -1 or -2 to define the resistance of one of the
        resistors, the report changes, as it assumes the given resistance
        is a known resistance standard.  The report then states how much
        the other resistor deviates from the first.  Note the output is
        given in Ω because the current can be calculated.

        The above Fluke resistors are stamped with the value 98.582 kΩ.
        Giving the script the arguments '-1 98.582k 10.957 10.955'
        results in

        '''))
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] V1 V2
          Print matching % for two resistors in series with a voltage
          across them.  The strings must be the voltages in volts.
          If the -w option is used, the input parameters are Vin and Vout.
          If either -1 or -2 are used, the resistance value of the other
          resistor will be calculated in terms of the given resistance.
        Example:
          Arguments of '1 1.01' produce
            Resistor matching:
                v1   = 1
                v2   = 1.01
                Mean = 1.005 ±0.5% (±5000 ppm)
        Options:
            -1 R    Define resistance of first resistor
            -2 R    Define resistance of second resistor
            -d n    Number of significant figures [{d['-d']}]
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-1"] = None      # First resistor
        d["-2"] = None      # Second resistor
        d["-d"] = 2         # Number of significant digits
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
                d[o] = flt(a)
                if d[o] <= 0:
                    Error(f"-1's value must be > 0")
                if d["-2"] is not None:
                    Error(f"-2 cannot be used if -1 is")
            elif o == "-2":
                d[o] = flt(a)
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
        # Get number of digits used in numbers
        n = max(GetSignificantFigures(s1), GetSignificantFigures(s2))
        V1, V2 = flt(s1), flt(s2)
        mean = (V1 + V2)/2
        halfwidth = abs(V1 - V2)/2
        cov = halfwidth/mean
        pct = 100*cov
        ppm = 1e6*cov
        # Print data
        print(f"Resistor matching:")
        mean.n = mean.N = max(d["-d"], n + 1)
        if d["-1"] or d["-2"]:
            # One of the resistors was defined
            if d["-1"]:
                i = V1/d["-1"]
                R1, R2 = V1/i, V2/i
                diff = R2 - R1
                sgn = "-" if diff < 0 else "+"
                pct = 100*abs(diff)/R1
                ppm = 1e4*pct
                print(f"  R1   ≝ {R1}")
                print(f"  R2   = {R1} {t.pct}{sgn} {pct}%{t.n} = R1 {sgn} {ppm} ppm")
            else:
                i = V2/d["-2"]
                R1, R2 = V1/i, V2/i
                diff = R1 - R2
                sgn = "-" if diff < 0 else "+"
                pct = 100*abs(diff)/R2
                ppm = 1e4*pct
                print(f"  R1   = {R2} {t.pct}{sgn} {pct}%{t.n} = R2 {sgn} {ppm} ppm")
                print(f"  R2   ≝ {R2}")
        else:
            print(f"  V1   = {s1}")
            print(f"  V2   = {s2}")
            print(f"  Mean = {mean} ", end="")
            print(f"{t.pct}±{pct}%{t.n} (±{ppm} ppm)")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    Report(*args)
