'''
Call PaperSizes() to get a dictionary of common paper sizes in mm.  Call
PaperSizes(scale=x) to convert the sizes in mm to another length unit by multiplying
by x.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2025 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Library to get common paper sizes.
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        pass
    if 1:  # Custom imports
        from f import flt
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        class G:
            pass
        g = G()
        g.dbg = False  # Turns on debug printing
if 1:  # Core functionality
    def PaperSizes(scale=1):
        '''Return a dictionary keyed by a paper size string; the values are the width
        and the height of the paper size in portrait mode.  Dimensional units are mm.
        Change the scale keyword to multiply each dimension by the constant to return 
        the sizes in a different unit.
        '''
        in2mm = 25.4
        sizes = {
            # ISO sizes, checked against https://en.wikipedia.org/wiki/ISO_216 on 3 Nov 2025
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
            "3x5": (3*in2mm, 5*in2mm),
            "4x6": (4*in2mm, 6*in2mm),
            "5x8": (5*in2mm, 8*in2mm),
        }
        # Check the ISO sizes
        for i, size in enumerate('''
            4A0 2A0 A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 2B0 B0 B1 B2 B3 B4 B5 B6 B7 B8 B9
            B10 2C0 C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 C10'''.split()):
            w, h = sizes[size]
            ar = h/w
            print(ar)
            if i:
                pass
            else:
                pass

PaperSizes()
