'''
Script to generate the colornames0 file
'''
'''
# 23 Apr 2022: This is my default color name file.  The three letter names
    # come from the resistor color code and make a basic set of 10 colors: blk,
    # brn, red, orn, yel, grn, blu, vio, gry, and wht.  cyan 'cyn' and magenta
    # 'mag' are added because these are common in terminal colors.  This gives
    # 12 basic colors.
 
    # I then added a few more three-letter color names.
 
    # Additional sets use single-letter prefixes:
    #   'l' for 'light'
    #   'd' for 'dark' 
    #   'b' for background (typically used as background colors with dark text)
 
    # Basic names
    "blk":  Color(  0,   0,   0) 
    "blu":  Color(  0,   0, 255) 
    "brn":  Color(150,  75,   0) 
    "cyn":  Color(  0, 150, 150) 
    "grn":  Color(  0, 180,   0) 
    "gry":  Color(100, 100, 100) 
    "mag":  Color(180,   0, 180) 
    "orn":  Color(210,  80,   0) 
    "red":  Color(150,   0,   0) 
    "vio":  Color(140,   0, 255) 
    "wht":  Color(180, 180, 180) 
    "yel":  Color(180, 180,   0) 
 
    # Light forms
    "lblk": Color( 64,  64,  64) 
    "lblu": Color( 64, 100, 255) 
    "lbrn": Color(226, 175, 128) 
    "lcyn": Color(  0, 255, 255) 
    "lgrn": Color(  0, 255,   0) 
    "lgry": Color(150, 150, 150) 
    "lmag": Color(255,   0, 255) 
    "lorn": Color(255, 128,   0) 
    "lred": Color(255,   0,   0) 
    "lvio": Color(180,   0, 255) 
    "lwht": Color(255, 255, 255) 
    "lyel": Color(255, 255,   0) 
 
    # Darker versions of these colors are occasionally useful.  Note the term
    # "self" is in scope (ColorName instance), so we can adjust the previous
    # set values.
    "dblk": self["lblk"].adjust(-30, comp="v")
    "dblu": self["blu"].adjust(-30, comp="v")
    "dbrn": self["brn"].adjust(-30, comp="v")
    "dcyn": self["cyn"].adjust(-30, comp="v")
    "dgrn": self["grn"].adjust(-30, comp="v")
    "dgry": self["gry"].adjust(-30, comp="v")
    "dmag": self["mag"].adjust(-30, comp="v")
    "dorn": self["orn"].adjust(-30, comp="v")
    "dred": self["red"].adjust(-30, comp="v")
    "dvio": self["vio"].adjust(-30, comp="v")
    "dwht": self["wht"].adjust(-30, comp="v")
    "dyel": self["yel"].adjust(-30, comp="v")
 
    # Even lighter versions are useful for background colors
    "bblk": Color(180, 180, 180) 
    "bblu": Color(180, 180, 255) 
    "bbrn": Color(230, 210, 150) 
    "bcyn": Color(180, 255, 255) 
    "bgrn": Color(180, 255, 180) 
    "bgry": Color(210, 210, 210) 
    "bmag": Color(255, 180, 255) 
    "born": Color(255, 150, 100) 
    "bred": Color(255, 180, 180) 
    "bvio": Color(220, 128, 255) 
    "bwht": Color(230, 230, 230) 
    "byel": Color(255, 255, 150) 
 
    #--------------------------------------------------------------------------------
    # Additional names
    "pnk":  Color(200,  90, 128) 
    "lip":  Color(200,  30,  90)
    "lav":  Color(140, 100, 180)
    "lil":  Color(190, 160, 255)
    "pur":  Color(110,  10, 170)
    "roy":  Color( 70,  60, 255)
    "den":  Color( 20, 100, 190)
    "sky":  Color(130, 200, 255)
    "trq":  Color(  0, 180, 150) 
    "sea":  Color(130, 180, 130) 
    "lwn":  Color(120, 190,   0)
    "lim":  Color( 50, 150,  40)
    "mus":  Color(170, 140,  10)
    '''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright © 2022 Don Peterson #∞copyright∞#
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
    # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
    # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
    # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:   # Color definition dictionaries
    R = "blk blu brn cyn grn gry mag orn red vio wht yel".split()
    basic = {
        "blk":  Color(  0,   0,   0),
        "blu":  Color(  0,   0, 255),
        "brn":  Color(150,  75,   0),
        "cyn":  Color(  0, 150, 150),
        "grn":  Color(  0, 180,   0),
        "gry":  Color(100, 100, 100),
        "mag":  Color(180,   0, 180),
        "orn":  Color(210,  80,   0),
        "red":  Color(150,   0,   0),
        "vio":  Color(140,   0, 255),
        "wht":  Color(180, 180, 180),
        "yel":  Color(180, 180,   0),
        #
        "lblk": Color( 64,  64,  64),
        "lblu": Color( 64, 100, 255),
        "lbrn": Color(226, 175, 128),
        "lcyn": Color(  0, 255, 255),
        "lgrn": Color(  0, 255,   0),
        "lgry": Color(150, 150, 150),
        "lmag": Color(255,   0, 255),
        "lorn": Color(255, 128,   0),
        "lred": Color(255,   0,   0),
        "lvio": Color(180,   0, 255),
        "lwht": Color(255, 255, 255),
        "lyel": Color(255, 255,   0),
        #
        "bblk": Color(180, 180, 180),
        "bblu": Color(180, 180, 255),
        "bbrn": Color(230, 210, 150),
        "bcyn": Color(180, 255, 255),
        "bgrn": Color(180, 255, 180),
        "bgry": Color(210, 210, 210),
        "bmag": Color(255, 180, 255),
        "born": Color(255, 150, 100),
        "bred": Color(255, 180, 180),
        "bvio": Color(220, 128, 255),
        "bwht": Color(230, 230, 230),
        "byel": Color(255, 255, 150),
    }
    additional = {
        "pnk":  Color(200,  90, 128),
        "lip":  Color(200,  30,  90),
        "lav":  Color(140, 100, 180),
        "lil":  Color(190, 160, 255),
        "pur":  Color(110,  10, 170),
        "roy":  Color( 70,  60, 255),
        "den":  Color( 20, 100, 190),
        "sky":  Color(130, 200, 255),
        "trq":  Color(  0, 180, 150),
        "sea":  Color(130, 180, 130),
        "lwn":  Color(120, 190,   0),
        "lim":  Color( 50, 150,  40),
        "olv":  Color(170, 140,  10),
    }
    S = tuple(additional.keys())
    def Build():
        def BuildDark():
            for i in R:
                k = "lblk" if i == "blk" else i
                basic["d" + i] = basic[k].adjust(-30, comp="v")
        def BuildAdditional():
            for i in S:
                k = "lblk" if i == "blk" else i
                additional["d" + i] = basic[k].adjust(-30, comp="v")
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [arg]
          If arg is 'mk', create the colornames0 file.  Otherwise, print a
          colorized version of what the file's contents would be, decorated
          with rgb/hsv/hls tuples.
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args[0] if args else ""
if 1:   # Core functionality
    def MakeFile():
        raise ValueError("Need impl")
    def FT(s):
        'Format a tuple of integers'
        out = []
        for i in s:
            out.append(f"{i:3d}")
        s = "(" + ', '.join(out) + ")"
        return s
    def Decorate(srt="h"):
        '''Print to stdout each color definition with rgb, hsv, and hls
        components.
        '''
        def GetNum(clr):
            assert(ii(srt, str) and len(srt) == 1)
            m = {"r":0, "g":1, "b":2,
                 "h":0, "s":1, "v":2,
                 "H":0, "L":1, "S":2}
            if srt in "rgb":
                    return clr.irgb[m[srt]]
            elif srt in "hsv":
                    return clr.ihsv[m[srt]]
            elif srt in "HLS":
                    return clr.ihls[m[srt]]
            else:
                raise Exception("Bad clr")

        t.always = True
        print("Name       Color(RGB)              HSV                HLS")
        s = " "*4
        # Build a list tuples (srt, string) where srt is the parameter
        # being sorted by and string is the output string.
        out = []
        di = basic
        for k in di:
            c = di[k]
            u = f"{t(c)}{k:4s}{s}{c!s}{s}{FT(c.ihsv)}{s}{FT(c.ihls)}{t.n}"
            out.append((GetNum(c), u))
        print()
        di = additional
        for k in di:
            c = di[k]
            u = f"{t(c)}{k:4s}{s}{c!s}{s}{FT(c.ihsv)}{s}{FT(c.ihls)}{t.n}"
            out.append((GetNum(c), u))
        # Print the sorted strings
        for dummy, string in sorted(out):
            print(string)

if __name__ == "__main__":
    d = {}      # Options dictionary
    arg = ParseCommandLine(d)
    if arg == "mk":
        MakeFile()
    else:
        Decorate()
