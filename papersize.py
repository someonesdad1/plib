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
    def PaperSizes(scale=1, exact=None):
        '''Return a dictionary keyed by a paper size string; the values are the width
        and the height of the paper size in portrait mode.  Dimensional units are mm.
        Keywords:
            scale   Multiply each dimension by this number (e.g., convert from mm to
                    inches by multiplying by 1/25.4)
            exact   If exact is not None, it must be an integer greater than 0.  It is
                    the number of digits to round the size to, computed from the exact
                    formula.  Otherwise, the returned dimensions are rounded to the
                    nearest mm.

        https://en.wikipedia.org/wiki/ISO_216#Properties gives the exact formulas:
            a, b = 1/sqrt(2), 1/2
            A[n]:  w = a**(n + b),   h = a**(n - b)
            B[n]:  w = a**n,         h = a**(n - 1)
            C[n]:  w = a**(n + b/2), h = a**(n - b/2)
        '''
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
            "6x0": (6*in2mm, 9*in2mm),
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
            # Compute the ISO sizes from formulas and 
            a, b, c = 1/2**(1/2), 1/2, 1000
            f = lambda x: flt(RoundOff(x, digits=6))
            A = lambda n: (f(c*a**(n + b)), f(c*a**(n - b)))
            B = lambda n: (f(c*a**n), f(c*a**(n - 1)))
            C = lambda n: (f(c*a**(n + b/2)), f(c*a**(n - b/2)))
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
            pp(ISO);exit()#xx
        sizes.extend(ISO)
        # Check formulas
        a, b, c = 1/2**(1/2), 1/2, 1000
        I = lambda n: (c*a**(n + b), c*a**(n - b))
        R = lambda x: int(round(x, 0))
        for i in range(-2, 11):
            breakpoint() #xx

            if i == -1:
                w0, h0 = sizes[f"2A0"]
            else:
                w0, h0 = sizes[f"A{i}"]
            w, h = I(i)
            Assert(abs(w0 - R(w)) <= 1)
            Assert(abs(h0 - R(h)) <= 1)
        exit() #xx 
        # Check the ISO sizes in the table
        iso_sizes = '''4A0 2A0 A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 2B0 B0 B1 B2 B3 B4 B5
                       B6 B7 B8 B9 B10 2C0 C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 C10'''.split()
        for i, size in enumerate(iso_sizes):
            w, h = sizes[size]
            Assert(1.405 < h/w < 1.429)     # Check aspect ratio
            if i:
                # Check that width is height of previous value
                w1, h1 = sizes[iso_sizes[i - 1]]
                Assert(h == w1)
            else:
                pass
        print(f"max = {max(a)}")
        print(f"min = {min(a)}")

PaperSizes(exact=1)
