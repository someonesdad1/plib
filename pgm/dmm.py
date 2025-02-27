"""
Given a reading from a DMM, calculates the uncertainty statement for the
reading.

Desired features

    - Need a -r option to manually specify the range when it has been
      manually selected.
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
        # Calculate uncertainty of DMM reading
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
        from color import Color, TRM as t
        from lwtest import Assert
        from f import flt
        from si import SI
        from uncertainties import ufloat, ufloat_fromstr, UFloat
        from u import u, ParseUnit

        if 0:
            import debug

            debug.SetDebugger()
    if 1:  # Global variables

        class G:
            pass

        g = G()  # Storage for global variables as attributes
        g.dbg = True
        g.si = SI(pure=True)  # True means avoid 2 character prefixes like 'da'
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # Colors
        t.dbg = t("sky") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.unc = t("purl") if g.dbg else ""  # Uncertainty, no coverage factor
        t.unck = t("ornl") if g.dbg else ""  # Uncertainty, has a coverage factor
if 1:  # Utility

    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] rdg1 [rdg2...]
          Convert the indicated DMM reading to a number with its estimated
          uncertainty.  Each reading must include the SI unit for the
          measurement.  Attach '~' for an AC value.  Use 'ohm' or 'Ω' for
          resistance.  If no unit is given, DC volts are assumed.  A
          variety of output forms are given and color is used to
          distinguish them.
        Options:
            -h      Print a manpage
            -k n    Define a coverage factor
            -l      List meters supported
            -m n    Choose meter to use (default Aneng 870)
            -o n    Choose output format
                       n = 0    Short form uncertainty   [default]
                       n = 1    Regular form uncertainty
                       n = 2    Accuracy interval
            -r val  Manually define the instrument's range
            -t      Assume a triangular distribution to get uncertainty
            -u      Assume a uniform distribution to get uncertainty
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3  # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h", ["help", "debug"])
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
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug

                debug.SetDebugger()
        return args


if 1:  # Meter classes

    class Meter:
        "Base class for meters"

        def __init__(self, serial_number=""):
            self.serial_number = sn
            # Set up number of digits for flt type
            x = flt(0)
            x.N = 3
            x.rtz = x.rtdp = False
            # Dictionaries for range (key) and accuracy (value = tuple of %
            # accuracy and counts)
            self.dcv = {}
            self.acv = {}
            self.dci = {}
            self.aci = {}
            self.ohm = {}
            self.F = {}
            self.Hz = {}

        def get_unit(self, un):
            """Return (prefix, si_unit, is_ac) where prefix is a proper SI
            prefix, si_unit is a proper SI unit (may contain an SI prefix)
            and is_ac is True if it's an AC quantity.
            """
            myun = un.strip()
            is_ac = True if myun.endswith("~") else False
            if is_ac:
                myun = myun[:-1]
            Assert(myun)
            # Substitute "Ω" for "ohm"
            myun = myun.replace("ohm", "Ω")
            # The only allowed units in un are "V, A, Ω, F, or Hz".  There
            # can be a leading SI prefix.
            found = None
            for unit in "V A Ω F Hz".split():
                if myun.endswith(unit):
                    found = unit
                    break
            if not found:
                raise ValueError(f"{un!r} is an invalid unit")
            # Remove the unit
            prefix = myun.replace(found, "")
            # Anything left over must be the SI prefix
            if prefix and prefix not in g.si:
                raise ValueError(f"{un!r} has an invalid SI prefix")
            # Make sure it can be converted to an SI quantity
            if u(prefix + found) is None:
                raise ValueError(f"{un!r} is an unrecognized unit")
            return (prefix, found, is_ac)

        def __call__(self, arg):
            "arg = string = number followed by an optional unit"
            Dbg(f"arg = {arg!r}")
            value, unit = ParseUnit(arg, allow_unc=False)
            value = flt(value)
            Dbg(f"  value = {value!r}, unit = {unit!r}")
            # Get proper SI unit
            prefix, un, ac = self.get_unit(unit)
            # Convert to an SI quantity
            measured = value * u(un)
            Dbg(f"  SI value = '{measured} {un} {'AC' if ac else 'DC'}'")
            if ac and un != "V" and un != "A":
                raise ValueError(f"AC can only be used with V or A")
            self.report(arg, measured, un, ac)

        def get_range(self, measured, unit, ac):
            "Return (di, range) for the measured value"
            if unit == "V":
                di = self.acv if ac else self.dcv
            elif unit == "A":
                di = self.aca if ac else self.dca
            elif unit == "Ω":
                di = self.ohm
            elif unit == "F":
                di = self.F
            elif unit == "Hz":
                di = self.Hz
            else:
                raise ValueError(f"Bug:  {unit!r} is bad unit")
            # Find which range it is by getting the first range which is
            # larger than the absolute value of the measured value.
            Dbg("  get_range:")
            values = list(sorted(di))
            for i, value in enumerate(di):
                Dbg(f"    Checking {value}")
                if abs(measured) < value:
                    return (di, values[i])
            raise ValueError(f"{measured!r} {unit} is out of range")

        def report(self, arg, measured, unit, ac):
            """arg is the user's request.  measured is the measured value
            in SI units, unit is the unit string, and ac is a boolean
            indicating an AC measurement.
            """
            Dbg(f"Reporting: {arg!r} {measured} {unit} ac={ac}")
            di, range = self.get_range(measured, unit, ac)
            pct, digits = di[range]
            Dbg(f"    Found range = {range}:  {pct}% and {digits} digits")

    class Aneng870(Meter):
        def __init__(self, serial_number=""):
            self.count = 20000
            flt(0).N = 5
            # Ranges and accuracy (% of reading, counts)
            a = (0.05, 3)
            self.dcv = dict(zip((0.02, 0.2, 2, 20, 200, 1000), [a] * 6))
            a = (0.3, 3)
            self.acv = dict(zip((0.02, 0.2, 2, 20, 200, 700), [a] * 6))
            a = (0.5, 3)
            self.dci = dict(zip((100e-6, 2e-3, 0.02, 0.2, 2, 20), [a] * 6))
            a = (0.8, 3)
            self.aci = dict(zip((100e-6, 2e-3, 0.02, 0.2, 2, 20), [a] * 6))
            a = (0.2, 3)
            self.ohm = dict(
                zip(
                    (200, 2e3, 20e3, 200e3, 2e6, 20e6, 200e6),
                    [(0.5, 3), a, a, a, (1, 3), (1, 3), (5, 5)],
                )
            )
            a = (2, 5)
            self.F = dict(
                zip(
                    (10e-9, 100e-9, 1e-8, 10e-6, 100e-6, 1e-5, 10e-3),
                    [(5, 20), a, a, a, a, a, (5, 5)],
                )
            )
            a = (0.1, 2)
            self.Hz = dict(zip((100, 1e3, 10e3, 100e3, 1e6, 10e6), [a] * 6))


if 1:  # Prototyping area
    dmm = Aneng870()
    dmm("1.321 V")
    exit()

if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
