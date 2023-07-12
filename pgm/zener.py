'''
Given a voltage on the command line, determine the best set of diodes
(zener, Si, Ge, Schottky, LED) to get the desired voltage.

On-hand zeners 1/2 W:
3.3 4.7 5.1 6.2 7.5 8.2 9.1 10 12 15 18 24 27 30

Note:  Ideally, the output needs to be based on experimental measurements of real
diodes, reflecting the current levels and the normal stochastic variation in a set of
"the same" diodes.

It would be nice to have a tester that would have specific current levels
for testing.  Useful values would be 0.1, 0.5, 1, 2, 5, 10, 20 mA. 

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
        # Given a desired voltage, print out a string of diodes to
        # get this value.
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        vlow = 3.3
        vhigh = 100
        zeners = (3.3, 4.7, 5.1, 6.2, 7.5, 8.2, 9.1, 10, 12, 15, 18, 24, 27, 30)
        current_mA = (0.5, 1, 2, 5, 10, 15, 20, 25, 30)
        leds = {
            "yel3": (1.85, 1.88, 1.92, 1.98, 2.05, 2.09, 2.12, 2.15, 2.16),
            "yel5": (1.85, 1.88, 1.92, 1.98, 2.05, 2.09, 2.12, 2.15, 2.16),
            "grn3": (1.87, 1.91, 1.94, 1.98, 2.02, 2.04, 2.06, 2.07, 2.08),
            "grn5": (2.28, 2.33, 2.40, 2.54, 2.68, 2.78, 2.86, 2.92, 2.98),
            "red3": (1.81, 1.84, 1.87, 1.93, 1.97, 2.01, 2.03, 2.05, 2.07),
            "red5": (1.76, 1.79, 1.83, 1.90, 1.98, 2.03, 2.07, 2.10, 2.13),
            "blu3": (2.62, 2.67, 2.74, 2.86, 3.00, 3.10, 3.16, 3.21, 3.25),
            "blu5": (2.62, 2.67, 2.74, 2.86, 3.00, 3.10, 3.16, 3.21, 3.25),
            "wht3": (2.60, 2.64, 2.70, 2.80, 2.90, 2.98, 3.05, 3.11, 3.17),
            "wht5": (2.61, 2.65, 2.70, 2.82, 2.96, 3.07, 3.14, 3.21, 3.26),

        }
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] voltage_V current_mA
          Print a diode string to use to get a desired voltage drop at
          a specified current.
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "a") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
if 1:   # Core functionality
    def ProcessVoltage(voltage):
        if not (vlow <= voltage <= vhigh):
            print(f"Voltage must be between {vlow} and {vhigh} V")
            exit(1)
        

if __name__ == "__main__":
    d = {}      # Options dictionary
    voltages = ParseCommandLine(d)
