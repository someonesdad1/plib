_pgminfo = '''
<oo desc
    Print dimensional information for various folios made from common paper sizes
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo license
    Licensed under the Open Software License version 3.0.
    See http://opensource.org/licenses/OSL-3.0.
oo>
<oo cat Put_category_here oo>
<oo test none oo>
<oo todo

    - List of todo items here

oo>
'''
 
if 1:  # Header
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
        import termtables as tt
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        # Paper sizes in mm
        g.in2mm = flt(25.4)
        g.sz = {
            # Size is portrait width versus height
            "a3": (flt(297), flt(420), "A3"),
            "a4": (flt(210), flt(297), "A4"),
            "a5": (flt(148), flt(210), "A5"),
            "a6": (flt(105), flt(148), "A6"),
            "a7": (flt( 74), flt(105), "A7"),
            "a8": (flt( 52), flt( 74), "A8"),
            "b4": (flt(250), flt(353), "B4"),
            "b5": (flt(176), flt(250), "B5"),
            "b6": (flt(125), flt(176), "B6"),
            "b7": (flt( 88), flt(125), "B7"),
            "b8": (flt( 62), flt( 88), "B8"),
            #
            "a":  (flt(8.5)*g.in2mm, flt(11)*g.in2mm, "ANSI A"),
            "b":  (flt(11)*g.in2mm, flt(17)*g.in2mm, "ANSI B"),
            "l":  (flt(8.5)*g.in2mm, flt(14)*g.in2mm, "Legal"),
            "x":  (flt(7.25)*g.in2mm, flt(10.5)*g.in2mm, "Executive"),
            "pc": (flt(3.5)*g.in2mm, flt(5.5)*g.in2mm, "Post card"),
            "3": (flt(3)*g.in2mm, flt(5)*g.in2mm, "3x5 card"),
            "4": (flt(4)*g.in2mm, flt(6)*g.in2mm, "4x6 card"),
            "5": (flt(5)*g.in2mm, flt(8)*g.in2mm, "5x8 card"),
            "6": (flt(6)*g.in2mm, flt(9)*g.in2mm, "6x9 card"),
        }
        ii = isinstance
if 1:   # Utility
    def GetColors():
        t.mm = t.denl
        t.inch = t.wht
        t.ar = t.lav
        t.area = t.grn
        t.iso = t.sky
        t.us = t.trql
        t.err = t.redl
        t.dbg = t.lill if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Warn(*msg, status=1):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] size1 [size2...]
          Print dimensional information for folios made from various sizes:
            US:  a b l x pc
            ISO: a3-a8, b4-b8
          Use a size of 'all' to see the supported paper size dimensions.
        Options:
            -d n    Number of digits [{d["-d"]}]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
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
                    Error(f"-d option's argument must be an integer between 1 and 15")
            elif o == "-h":
                Usage()
        x = flt(0)
        x.N = d["-d"]
        x.rtz = True
        x.rtdp = True
        GetColors()
        return args
if 1:   # Core functionality
    def PrintAll():
        o = [("", 
             "", 
             f"{t.mm}Width,{t.n}",
             f"{t.mm}Height,{t.n}",
             f"{t.mm}Area,{t.n}",
             f"{t.inch}Width,{t.n}",
             f"{t.inch}Height,{t.n}",
             f"{t.inch}Area,{t.n}",
             f"{t.ar}Aspect{t.n}")]
        o.append(("Size", 
             "Name", 
             f"{t.mm}mm{t.n}",
             f"{t.mm}mm{t.n}",
             f"{t.mm}mm²{t.n}",
             f"{t.inch}in{t.n}",
             f"{t.inch}in{t.n}",
             f"{t.inch}in²{t.n}",
             f"{t.ar}ratio{t.n}"))
        iso = set("a3 a4 a5 a6 a7 a8 b4 b5 b6 b7 b8".split())
        for size in g.sz:
            w, h, name = g.sz[size]
            line = []
            line.append(size)
            # name
            line.append(f"{t.iso}{name}{t.n}" if size in iso else f"{t.us}{name}{t.n}")
            # width & height in mm
            line.append(f"{t.mm}{w}{t.n}")
            line.append(f"{t.mm}{h}{t.n}")
            line.append(f"{t.mm}{w*h}{t.n}")
            # width & height in inches
            line.append(f"{t.inch}{w/g.in2mm}{t.n}")
            line.append(f"{t.inch}{h/g.in2mm}{t.n}")
            line.append(f"{t.mm}{w*h/g.in2mm**2}{t.n}")
            # aspect ratio
            line.append(f"{t.ar}{h/w}{t.n}")
            o.append(line)
        pad = 1
        tt.print(o, header=None, padding=(pad, pad), style=" "*15, alignment="c"*9)
    def Area(w, h, inch=False):
        if inch:
            return f"{t.inch}[{w*h/g.in2mm**2} inch²]{t.n}"
        else:
            return f"{t.mm}[{w*h/100} cm²]{t.n}"
    def PrintLine(msg, w, h, width=15):
        print(f"  {msg:{width}s} {t.mm}{w}x{h} mm {Area(w, h)} "
              f"{t.inch}{w/g.in2mm}x{h/g.in2mm} inches {Area(w, h, True)} "
              f"{t.ar}({h/w}){t.n}")
    def PrintSize(size):
        try:
            w, h, name = g.sz[size.lower()]
        except KeyError:
            Error(f"{size!r} not recognized as a valid paper size")
        t.print(f"{t.ornl}{size} {name} folio characteristics {t.ar}(asp. ratio)")
        A = w*h
        PrintLine("Full sheet", w, h)
        PrintLine("  1/2 folio", h/2, w)
        # 1 cut
        w1, h1 = h/2, w
        PrintLine("1 cut", w1, h1)
        w2, h2 = h1/2, w1
        PrintLine("  1/4 folio", w2, h2)
        # 2 cuts
        w, h = [i/2 for i in (w, h)]
        PrintLine("2 cuts", w, h)
        w1, h1 = h/2, w
        PrintLine("  1/16 folio", w1, h1)

if __name__ == "__main__":
    d = {}      # Options dictionary
    sizes = ParseCommandLine(d)
    for size in sizes:
        if size.lower() == "all":
            PrintAll()
        else:
            PrintSize(size)
