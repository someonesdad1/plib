'''
Script to generate the colornames0 file

    - Short names candidates
        - Green
            - trq       turquoise
            - for       forest green
            - sea       sea green
            - olv       olive
            - spg       spring green
            - aqu       aqua
            - frn       fern
            - asp       asparagus
            - emr       emerald
            - lim       lime, lima
            - pea       pea green
            - alg       algae
            - mnt       mint
            - kiw       kiwi
            - lea       leaf
            - pin       pine
            - tea
        - Violet
            - lav       lavender
            - lil       lilac
            - plm       plum
        - Blue
            - pow       powder blue
            - roy       royal blue
            - sky       sky blue
            - den       denim
            - ind       indigo
            - pur       purple
            - tpz       topaz
            - ice
        - Yellow
            - mus       mustard
            - crn       corn
            - och       ochre
            - gld       gold
            - sun
            - mud
            - ash
        - Red
            - pnk       pink
            - prt       port
            - rub       ruby
            - rus       rust
            - bld       blood
            - win       wine
            - lav       lava
            - lip       lipstick
            - cop       copper
            - rou       rouge
            - san       sand
            - pea       peanut
            - tob       tobacco
            - orc       orchid
            - pch       peach
            - khk       khaki
            - slm       salmon
            - brz       bronze
            - brk       brick
            - dst       dust
            - fsh       flesh
            - wod       wood
            - jav       java (coffee)
            - cly       clay
            - fir       fire

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
    main = {
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
        "roy":  Color( 80,  80, 255),
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
                main["d" + i] = main[i].adjust(-30, comp="v")
        def BuildAdditional():
            for i in S:
                additional["d" + i] = additional[i].adjust(-30, comp="v")
                additional["l" + i] = additional[i].adjust(+20, comp="L")
                additional["b" + i] = additional[i].adjust(+50, comp="L")
        BuildAdditional()
        BuildDark()
        main.update(additional)
    Build()
if 1:   # Color definitions:  alternate method
    # Use HSV values in hex
    main1 = []
    if 1:  # Primary
        if 1:  # Grays
            if 1:  # blk
                main1.extend([
                    "blk  #000000",
                    "blkd #202020",
                    "blkl #404040",
                    "blkb #b4b4b4",
                ])
            if 1:  # gry
                main1.extend([
                    "gry  #646464",
                    "gryd #464646",
                    "gryl #969696",
                    "gryb #d2d2d2",
                ])
            if 1:  # wht
                main1.extend([
                    "wht  #b4b4b4",
                    "whtd #7e7e7e",
                    "whtl #ffffff",
                    "whtb #e6e6e6",
                ])
        if 1:  # blu
            main1.extend([
                "blu  #0000ff",
                "blud #0000b2",
                "blul #4064ff",
                "blub #b4b4ff",
            ])
        if 1:  # brn
            main1.extend([
                "brn  #964b00",
                "brnd #693400",
                "brnl #e2af80",
                "brnb #ffd296",
            ])
        if 1:  # cyn
            main1.extend([
                "cyn  #009696",
                "cynd #006968",
                "cynl #00ffff",
                "cynb #b4ffff",
            ])
        if 1:  # grn
            main1.extend([
                "grn  #00b400",
                "grnd #007f00",
                "grnl #00ff00",
                "grnb #b4ffb4",
            ])
        if 1:  # mag
            main1.extend([
                "mag  #b400b4",
                "magd #7d007d",
                "magl #ff00ff",
                "magb #ffb4ff",
            ])
        if 1:  # orn
            main1.extend([
                "orn  #d25000",
                "ornd #933700",
                "ornl #ff8000",
                "ornb #ff9664",
            ])
        if 1:  # red
            main1.extend([
                "red  #960000",
                "redd #690000",
                "redl #ff0000",
                "redb #ffb4b4",
            ])
        if 1:  # vio
            main1.extend([
                "vio  #8c00ff",
                "viod #6000b2",
                "viol #b400ff",
                "viob #dc80ff",
            ])
        if 1:  # yel
            main1.extend([
                "yel  #b4b400",
                "yeld #7e7e00",
                "yell #ffff00",
                "yelb #ffff96",
            ])
    if 1:  # Secondary
        a = bool(len(sys.argv) > 1)
        a = 1
        if a:  # pnk
            main1.extend([
                "pnk  $f79986",
                "pnkd $f76070",
                "pnkl $f7d0ff",
                "pnkb $f7db63",
            ])
        if a:  # lip
            main1.extend([
                "lip  $ef6bf3",
                "lipd $ef40ff",
                "lipl $efc0ff",
                "lipb $efe0ff",
            ])
        if a:  # lav
            main1.extend([
                "lav  $c2a092",
                "lavd $c24892",
                "lavl $c2c892",
                "lavb $c2e092",
            ])
        if a:  # lil
            main1.extend([
                "lil  $bac0b0",
                "lild $ba60b0",
                "lill $bad0b0",
                "lilb $bae0b0",
            ])
        if a:  # pur
            main1.extend([
                "pur  $c660c0",
                "purd $c640c0",
                "purl $c6b0c0",
                "purb $c6e0c0",
            ])
        if a:  # roy
            main1.extend([
                "roy  $9fa0c0",
                "royd $9f50c0",
                "royl $9fb1c0",
                "royb $9fe0c0",
            ])
        if a:  # den
            main1.extend([
                "den  $9770c0",
                "dend $9740c0",
                "denl $97b1c0",
                "denb $97e0c0",
            ])
        if a:  # sky
            main1.extend([
                "sky  $90c3ff",
                "skyd $9040ff",
                "skyl $90d7ff",
                "skyb $90e0ff",
            ])
        if a:  # trq
            main1.extend([
                "trq  $7370ff",
                "trqd $7340ff",
                "trql $73b0ff",
                "trqb $73e0ff",
            ])
        if a:  # sea
            main1.extend([
                "sea  $67807f",
                "sead $67407f",
                "seal $67b07f",
                "seab $67e07f",
            ])
        if a:  # lwn
            main1.extend([
                "lwn  $4260e4",
                "lwnd $4240e4",
                "lwnl $42a1e4",
                "lwnb $42e0e4",
            ])
        if a:  # olv
            main1.extend([
                "olv  $38609a",
                "olvd $38409a",
                "olvl $38b09a",
                "olvb $38e09a",
            ])

    R = "blk blu brn cyn grn gry mag orn red vio wht yel".split()
    S = "pnk lip lav lil pur roy den sky trq sea lwn lim olv".split()
    from columnize import Columnize
    out = []
    for i in main1:
        if "(" in i:
            name, cn = i.split("(")
            s = eval("(" + cn)
            c = Color(*s)
        else:
            name, cn = i.split()
            if cn.startswith("#"):
                c = Color(cn)
            elif cn.startswith("@"):
                c = Color(cn, hsv=True)
            else:
                c = Color(cn, hls=True)
        #if len(name) > 3: continue #xx
        print(f"{t(c)}{name:4s} {c.xhsv} {c.xrgb} {c.xhls} {c}{t.n}")
    exit()

    for i in Columnize(main1):
        print(i)

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
            -w      Include whites and grays
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-w"] = True      # Remove grays
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hw", ["help"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("w"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args[0] if args else ""
if 1:   # Core functionality
    def MakeOutputFile():
        raise ValueError("Need impl")
    def FT(s):
        'Format a tuple of integers'
        out = []
        for i in s:
            out.append(f"{i:3d}")
        s = "(" + ', '.join(out) + ")"
        return s
    def Decorate(srt="HL"):
        '''Print to stdout each color definition with rgb, hsv, and hls
        components.
        '''
        def GetNum(clr):
            assert(ii(srt, str))
            m = {"r":0, "g":1, "b":2,
                 "h":0, "s":1, "v":2,
                 "H":0, "L":1, "S":2}
            out = []
            for char in srt:
                if char in "rgb":
                        out.append(clr.irgb[m[char]])
                elif char in "hsv":
                        out.append(clr.ihsv[m[char]])
                elif char in "HLS":
                        out.append(clr.ihls[m[char]])
                else:
                    raise Exception("Bad clr")
            return tuple(out)
        # Remove grays and whites if needed
        ignore = []
        if d["-w"]:
            for i in main:
                c = main[i]
                r, g, b = c.irgb
                if r == g and r == b and g == b:
                    ignore.append(i)
        ignore = set(ignore)
        t.always = True
        print("Name       Color(RGB)              HSV                HLS")
        s = " "*4
        # Build a list tuples (srt, string) where srt is the parameter
        # being sorted by and string is the output string.
        out = []
        for k in main:
            if k in ignore:
                continue
            c = main[k]
            if 0:   # Regular tuples
                u = f"{t(c)}{k:4s}{s}{c!s}{s}{FT(c.ihsv)}{s}{FT(c.ihls)}{s}{c.xhls}{t.n}"
            else:   # Hex
                u = f"{t(c)}{k:4s}{s}{c.xrgb}{s}{c.xhsv}{s}{c.xhls}{t.n}"
            out.append((GetNum(c), u))
        print()
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
