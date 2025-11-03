_pgminfo = '''
<oo desc
    Call PaperSizes() to get a dictionary of common paper sizes in mm.  The floating 
    point sizes are returned as type f.flt, which shows you 3 figures of the value by
    default (the flt class is derived from float).
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo license
    Licensed under the Open Software License version 3.0.
    See http://opensource.org/licenses/OSL-3.0.
oo>
<oo cat Put_category_here oo>
<oo test none oo>
<oo todo
    - 
oo>
'''
if 1:  # Header
    from f import flt
    from lwtest import Assert
    from roundoff import RoundOff
    from dpprint import PP
    pp = PP()   # Get pprint with current screen width
    if 0:
        import debug
        debug.SetDebugger()
if 1:  # Core functionality
    def PaperSizes(scale=1, exact=False, digits=12):
        '''Return a dictionary keyed by a paper size string; the values are the width
        and the height of the paper size in portrait mode.  Dimensional units are mm.
        Keywords:
            scale   Multiply each dimension by this number (e.g., convert from mm to
                    inches by multiplying by 1/25.4)
            exact   If exact is False, the ISO size dimensions are returned rounded
                    to the nearest mm, given in the table at
                    https://en.wikipedia.org/wiki/ISO_216.  Otherwise, the dimensions
                    are calculated by the formulas given at that site.
            digits  The values returned are rounded to this number of digits if the
                    returned value is not an integer.

        https://en.wikipedia.org/wiki/ISO_216#Properties gives the exact formulas:
            a, b = 1/sqrt(2), 1/2
            A[n]:  w = a**(n + b),   h = a**(n - b)
            B[n]:  w = a**n,         h = a**(n - 1)
            C[n]:  w = a**(n + b/2), h = a**(n - 3*b/2)
        '''
        def Round(x):
            'Return x rounded to the indicated digits if it is not an integer'
            return x if isinstance(x, int) else RoundOff(x, digits=digits)
        in2mm = 25.4
        sizes = {
            # US sizes
            "A": (8.5*in2mm, 11*in2mm),
            "B": (11*in2mm, 17*in2mm),
            "C": (17*in2mm, 22*in2mm),
            "D": (22*in2mm, 34*in2mm),
            "E": (34*in2mm, 44*in2mm),
            "letter": (8.5*in2mm, 11*in2mm),
            "tabloid": (11*in2mm, 17*in2mm),
            "ledger": (11*in2mm, 17*in2mm),
            "legal": (8.5*in2mm, 14*in2mm),
            "executive": (7.25*in2mm, 10.5*in2mm),
            "US_post_card": (3.5*in2mm, 5.5*in2mm),
            # Common index card sizes
            "3x5": (3*in2mm, 5*in2mm),
            "4x6": (4*in2mm, 6*in2mm),
            "5x8": (5*in2mm, 8*in2mm),
            "6x9": (6*in2mm, 9*in2mm),
            "US_business_card": (2*in2mm, 3.5*in2mm),
            # Other sizes
            "ISO_business_card": (55, 85),  # ISO 7810
            "credit_card": (53.98, 85.60),  # ISO/IEC 7810 ID-1
        }
        ISO = {
            # ISO sizes, checked against https://en.wikipedia.org/wiki/ISO_216 on 3 Nov 2025
            # width, height in portrait mode
            "4A0": (1682, 2378),
            "2A0": (1189, 1682),
            "A0": (841, 1189),
            "A1": (594, 841),
            "A2": (420, 594),
            "A3": (297, 420),
            "A4": (210, 297),
            "A5": (148, 210),
            "A6": (105, 148),
            "A7": (74, 105),
            "A8": (52, 74),
            "A9": (37, 52),
            "A10": (26, 37),
            "2B0": (1414, 2000),
            "B0": (1000, 1414),
            "B1": (707, 1000),
            "B2": (500, 707),
            "B3": (353, 500),
            "B4": (250, 353),
            "B5": (176, 250),
            "B6": (125, 176),
            "B7": (88, 125),
            "B8": (62, 88),
            "B9": (44, 62),
            "B10": (31, 44),
            "2C0": (1297, 1834),
            "C0": (917, 1297),
            "C1": (648, 917),
            "C2": (458, 648),
            "C3": (324, 458),
            "C4": (229, 324),
            "C5": (162, 229),
            "C6": (114, 162),
            "C7": (81, 114),
            "C8": (57, 81),
            "C9": (40, 57),
            "C10": (28, 40),
        }
        if exact:
            # Compute the ISO sizes from formulas
            a, b, c = 1/2**(1/2), 1/2, 1000
            A = lambda n: (c*a**(n + b), c*a**(n - b))
            B = lambda n: (c*a**n, c*a**(n - 1))
            C = lambda n: (c*a**(n + b/2), c*a**(n - 3*b/2))
            ISO = {}
            for n in range(11):
                ISO[f"A{n}"] = A(n)
                ISO[f"B{n}"] = B(n)
                ISO[f"C{n}"] = C(n)
            # Manually handle the other sizes
            ISO[f"4A0"] = A(-2)
            ISO[f"2A0"] = A(-1)
            ISO[f"2B0"] = B(-1)
            ISO[f"2C0"] = C(-1)
        sizes.update(ISO)
        # Check the ISO sizes in the table:  This is a gross check to catch things like
        # unintended edits.
        iso_sizes = '''4A0 2A0 A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 2B0 B0 B1 B2 B3 B4 B5
                       B6 B7 B8 B9 B10 2C0 C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 C10'''.split()
        for i, size in enumerate(iso_sizes):
            w, h = sizes[size]
            Assert(1.405 < h/w < 1.429)     # Check aspect ratio
        # Round the values
        for i in sizes:
            sizes[i] = tuple(Round(j) for j in sizes[i])
        return sizes

if __name__ == "__main__":  
    # Print a table of paper sizes
    from color import t
    import termtables as tt
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
            from lwtest import Assert
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
            ii = isinstance
    if 1:   # Utility
        def GetColors():
            t.stuff = t.lill
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
            Usage:  {sys.argv[0]} [options] 
              Print dimensions of common paper sizes.
            Options:
                -d n    Change number of figures [{d["-d"]}]
            '''))
            exit(status)
        def ParseCommandLine(d):
            d["-a"] = False     # Need description
            d["-d"] = 3         # Number of significant digits
            if 0 and len(sys.argv) < 2:
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
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    sizes = PaperSizes()
    a = "─"*6
    hdr = [
        ("", "Width", "Height", "Area", "Width", "Height", "Area", "Aspect"),
        ("Size", "mm", "mm", "cm²", "inch", "inch", "inch²", "Ratio")
    ]
    o = []
    for i in hdr:
        o.append(i)
    o.append(("─"*17, a, a, a, a, a, a, a))
    for i, size in enumerate(sizes):
        w, h = [flt(j) for j in sizes[size]]
        w1, h1 = [flt(j/25.4) for j in sizes[size]]
        o.append((size, w, h, w*h/100, w1, h1, w1*h1, h/w))
    for i in hdr:
        o.append(i)
    pad = 1
    a = "l" + ("c"*(len(o[0]) - 1))
    tt.print(o, header=None, padding=(pad, pad), style=" "*15, alignment=a)
