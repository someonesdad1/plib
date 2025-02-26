"""
Show HP scope storage registers
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Show HP scope's setup registers
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:  # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert

        if 0:
            import debug

            debug.SetDebugger()
    if 1:  # Global variables

        class G:
            pass

        g = G()
        g.dbg = False
        g.registers = {}  # Indexes register number to Scope object
        ii = isinstance
        # Printing widths
        g.w_reg = 3
        g.w_name = 50
        g.w_trig = 20
        # Colors
        t.reg = t.orn
        t.name = t.wht
        t.trig = t.royl
        t.title = t.purl
if 1:  # Classes

    class Scope:
        def __init__(self, register, name, trigger):
            self.register = register
            self.name = name
            self.trigger = trigger
            self.details = ""

        def __str__(self):
            s = f"Def " if not self.register else f"{self.register:<3d} "
            s += f"{self.name:{g.w_name}s} {self.trigger:{g.w_trig}s}"
            return s

        def __repr__(self):
            if self.details:
                return f"{t.purl}{str(self)}{t.n}\n{self.details}"
            else:
                return f"{str(self)}"

        def get_details(self):
            s = (
                f"{t.reg}Def{t.n} "
                if not self.register
                else f"{t.reg}{self.register:<3d}{t.n} "
            )
            s += f"{t.name}{self.name:{g.w_name}s} {t.trig}{self.trigger:{g.w_trig}s}{t.n}"
            return s


if 1:  # Utility

    def GetColors():
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""

    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )

    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=0):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] [reg] [reg...]
          Show HP scope setup register details.  Print summary for no arguments.
        Options:
            -h      Print a manpage
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False  # Need description
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ah")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        return args


if 1:  # Core functionality

    def BuildScopeData():
        s = g.registers
        s[0] = Scope(0, "Default setup 100 mV/div", "CH1 auto lvl")
        s[1] = Scope(1, "General CH 1", "CH1 auto lvl")
        s[2] = Scope(2, "General CH 2", "CH2 auto lvl")
        s[3] = Scope(3, "General CH 1 & CH 2", "CH3 auto lvl")
        s[3].details = dedent(f"""
            This mode is intended for general exploration of a circuit.  Connect a scope probe to
            CH 3 and use it for the clocking signal of the circuit.  Then CH 1 and CH 2 can be
            used for normal measurements.
        """)
        s[5] = Scope(5, "General work with function generator", "CH4 auto lvl")
        s[5].details = dedent(f"""
            This mode is when the B&K 4052 function generator is being used to provide a signal.
            The sync output of the generator is put in CH 4 to act as the trigger source.  Then
            the other three channels can be used as needed on the circuitry.  You'll have to set
            up the generator's sync output, as it's off by default.
        """)
        s[6] = Scope(6, "Probing 120 V AC with 10X probe", "Line")
        s[12] = Scope(12, "1 V roll mode (cursors are 1/3 V & 2/3 V)", "NA")
        s[5].details = dedent(f"""
            Roll mode at 0.5 s/div.  CH 1 is 200 mV/div and the cursor lines are at 1/3 V and
            2/3 V.  CH 2 is 1 V/div.  You can set timebase from 200 ms/div to 5 s/div.
        """)
        s[14] = Scope(14, "Octopus (XY mode)", "NA")
        s[14].details = dedent(f"""
            Horizontal is CH 1:  960 mV/div, DC coupled, 1X
            Vertical   is CH 2:  1.20 mV/div, DC coupled, inverted, 1X
        """)
        s[15] = Scope(15, "TTL testing", "CH1 normal")
        s[15].details = dedent(f"""
            Cursor lines show LOW threshold (0.8 V) and HIGH threshold (2.0 V).  CH 1 and CH 2
            are 1 V/div and set up for 10X probes.
        """)

    def Summary():
        print(f"{t.title}Reg {'Name':^{g.w_name}s} {'Trigger':^{g.w_trig}s}")
        print(f"--- {'-' * g.w_name} {'-' * g.w_trig}{t.n}")
        for i in g.registers:
            print(g.registers[i].get_details())

    def Details(args):
        for i, arg in enumerate(args):
            try:
                o = g.registers[int(arg)]
                print(f"{o!r}")
                if len(args) > 1 and arg != args[-1]:
                    print()
            except Exception as e:
                print(f"{e}")
                print(f"Register {arg!r} not found")


if __name__ == "__main__":
    d = {}  # Options dictionary
    BuildScopeData()
    args = ParseCommandLine(d)
    if not args:
        Summary()
    else:
        Details(args)
