'''
Given a reading from a DMM, calculates the uncertainty statement for the
reading.

Desired features

    - Each meter gets a class to define its capabilities.
        - Count, ranges, etc.
        - Functions
            - DC voltage
            - AC voltage
            - DC current
            - AC current
            - Resistance
            - Capacitance
            - Frequency
    - Figures out from the number you type in what range you are on.  This
      is important because if you're measuring a 9999 significand on an
      Aneng meter and the signal is a bit noisy, it almost always upranges
      and you'll lose a digit of resolution.
    - The -k option gives the number to divide the manufacturer's halfwidth
      to get the estimated uncertainty.  Defaults to 1, which is likely
      conservative, but manufacturers tell you nothing statistically about
      their meters.

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
        import os
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from f import flt
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # Colors
        t.unc = t("purl")   # Uncertainty, no coverage factor
        t.unck = t("ornl")  # Uncertainty, has a coverage factor
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] rdg1 [rdg2...]
          Convert the indicated reading to a number with its estimated
          uncertainty.  Units can be
            v   Volts, DC
            v~  Volts, AC
            a   Amperes, DC
            a~  Amperes, AC
            o   Ohms
            Ω   Ohms
            f   Farad
            hz  Hertz
          Case of the units is unimportant, but any SI prefix is
          case-sensitive.  One or more spaces between the number and the
          unit are allowed.
        Output:
            The output is given as an "accuracy" interval in various forms.
            It's up to you to interpret this properly.  You can use the -u
            option to interpret the halfwidth as a standard uncertainty
            with no coverage factor.  If you use the -k option to specify a
            coverage factor >= 1, then the halfwidth of the interval is
            divided by the coverage factor to "convert" it to a standard
            uncertainty.  Color in the printout will be used to denote that
            this should be interpreted as a standard uncertainty.
        Examples:
            '4.2'       4.2 V DC
            '4.2 V~'    4.2 V AC
            '4.2V~'     Same
            '4.2 mV~'   4.2 mV AC
            '4.2mV~'    Same
        Options:
            -h      Print a manpage
            -k n    Define a coverage factor
            -l      List meters supported
            -m n    Choose meter to use (default Aneng 870)
            -u      Halfwidth is standard uncertainty, no coverage factor
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h", 
                    ["help", "debug"])
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
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        return args
if 1:   # Meter classes
    class Aneng870:
        def __init__(self, sn=""):
            self.sn = sn
            self.count = 20000
            # Ranges and accuracy (% of reading, counts)
            a = (0.05, 3)
            self.dcv = {    
                0.02: a,
                0.2: a,
                2: a,
                20: a,
                200: a,
                1000: a,
            }
            a = (0.3, 3)
            self.acv = {
                0.02: a,
                0.2: a,
                2: a,
                20: a,
                200: a,
                750: a,
            }
            a = (0.5, 3)
            self.dci = {
                100e-6: a,
                2e-3: a,
                20e-3: a,
                0.2: a,
                2: a,
                20: a,
            }
            a = (0.8, 3)
            self.aci = {
                100e-6: a,
                2e-3: a,
                20e-3: a,
                0.2: a,
                2: a,
                20: a,
            }
            a = (0.2, 3)
            self.ohm = {
                200: (0.5, 3),
                2e3: a,
                20e3: a,
                200e3: a,
                2e6: (1, 3),
                20e6: (1, 3),
                200e6: (5, 5)
            }
            a = (2, 5)
            self.F = {
                10e-9: (5, 20),
                100e-9: a,
                1000e-9: a,
                10e-6: a,
                100e-6: a,
                1000e-6: a,
                10e-3: (5, 5),
            }
            a = (0.1, 2)
            self.Hz = {
                100: a,
                1e3: a,
                10e3: a,
                100e3: a,
                1e6: a,
                10e6: a,
            }
        def __call__(self, arg):
            '''arg is a string that is a number followed by an optional
            unit string.  If there is no unit string, DC voltage is
            assumed.  The case of the unit string is ignored; there can be
            an SI prefix on the unit.  The allowed unit strings are
                v   Volts, DC
                v~  Volts, AC
                a   Amperes, DC
                a~  Amperes, AC
                o   Ohms
                Ω   Ohms
                f   Farad
                hz  Hertz
            '''

if 1:   # Core functionality
    pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
