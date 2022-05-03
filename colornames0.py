'''
Script to generate the colornames0.py module
    3 May 2022

    - Primary names
        - blk   Black
        - gry   Gray
        - wht   White
        - blu   Blue
        - brn   Brown
        - cyn   Cyan
        - grn   Green
        - mag   Magenta
        - orn   Orange
        - red   Red
        - vio   Violet
        - yel   Yellow
    - Secondary names
        - pnk   Pink
        - lip   Lipstick
        - lav   Lavender
        - lil   Lilac
        - pur   Purple
        - roy   Royal blue
        - den   Denim
        - sky   Sky blue
        - trq   Turquoise
        - sea   Sea green
        - lwn   Lawn
        - olv   Olive

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
        if len(sys.argv) > 1:
            import debug
            debug.SetDebugger()
    # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:   # Colors
    # Use HLS values in hex
    main = []
    if 1:  # Primary
        if 1:  # Grays
            if 1:  # blk
                main.extend([
                    "blk  $000000",
                    "blkd $001e00",
                    "blkl $003c00",
                    "blkb $00b400",
                ])
            if 1:  # gry
                main.extend([
                    "gry  $006400",
                    "gryd $005000",
                    "gryl $009600",
                    "gryb $00d200",
                ])
            if 1:  # wht
                main.extend([
                    "wht  $00b400",
                    "whtd $008200",
                    "whtl $00ff00",
                    "whtb $00e600",
                ])
        if 1:  # blu
            main.extend([
                "blu  $aa80ff",
                "blud $aa40ff",
                "blul $aaa0ff",
                "blub $aae0ff",
            ])
        if 1:  # brn
            main.extend([
                "brn  $154bff",
                "brnd $1534ff",
                "brnl $15b0ff",
                "brnb $15e0ff",
            ])
        if 1:  # cyn
            main.extend([
                "cyn  $7f4cff",
                "cynd $7f35ff",
                "cynl $7f80ff",
                "cynb $7fd9ff",
            ])
        if 1:  # grn
            main.extend([
                "grn  $555aff",
                "grnd $5540ff",
                "grnl $5580ff",
                "grnb $55e0ff",
            ])
        if 1:  # mag
            main.extend([
                "mag  $d450ff",
                "magd $d43eff",
                "magl $d480ff",
                "magb $d4e0ff",
            ])
        if 1:  # orn
            main.extend([
                "orn  $1060ff",
                "ornd $1040ff",
                "ornl $1090ff",
                "ornb $10e0ff",
            ])
        if 1:  # red
            main.extend([
                "red  $0050ff",
                "redd $0034ff",
                "redl $0080ff",
                "redb $00e0ff",
            ])
        if 1:  # vio
            main.extend([
                "vio  $c180ff",
                "viod $c140ff",
                "viol $c1a0ff",
                "viob $c1e0ff",
            ])
        if 1:  # yel
            main.extend([
                "yel  $2a60ff",
                "yeld $2a40ff",
                "yell $2a80ff",
                "yelb $2ae0ff",
            ])
    if 1:  # Secondary
        if 1:  # pnk
            main.extend([
                "pnk  $f79986",
                "pnkd $f76070",
                "pnkl $f7d0ff",
                "pnkb $f7db63",
            ])
        if 1:  # lip
            main.extend([
                "lip  $ef6bf3",
                "lipd $ef40ff",
                "lipl $efc0ff",
                "lipb $efe0ff",
            ])
        if 1:  # lav
            main.extend([
                "lav  $c2a092",
                "lavd $c24892",
                "lavl $c2c892",
                "lavb $c2e092",
            ])
        if 1:  # lil
            main.extend([
                "lil  $bac0b0",
                "lild $ba60b0",
                "lill $bad0b0",
                "lilb $bae0b0",
            ])
        if 1:  # pur
            main.extend([
                "pur  $c660c0",
                "purd $c640c0",
                "purl $c6b0c0",
                "purb $c6e0c0",
            ])
        if 1:  # roy
            main.extend([
                "roy  $9fa0c0",
                "royd $9f50c0",
                "royl $9fb1c0",
                "royb $9fe0c0",
            ])
        if 1:  # den
            main.extend([
                "den  $9770c0",
                "dend $9740c0",
                "denl $97b1c0",
                "denb $97e0c0",
            ])
        if 1:  # sky
            main.extend([
                "sky  $90c3ff",
                "skyd $9040ff",
                "skyl $90d7ff",
                "skyb $90e0ff",
            ])
        if 1:  # trq
            main.extend([
                "trq  $7370ff",
                "trqd $7340ff",
                "trql $73b0ff",
                "trqb $73e0ff",
            ])
        if 1:  # sea
            main.extend([
                "sea  $67807f",
                "sead $67407f",
                "seal $67b07f",
                "seab $67e07f",
            ])
        if 1:  # lwn
            main.extend([
                "lwn  $4260e4",
                "lwnd $4240e4",
                "lwnl $42a1e4",
                "lwnb $42e0e4",
            ])
        if 1:  # olv
            main.extend([
                "olv  $38609a",
                "olvd $38409a",
                "olvl $38b09a",
                "olvb $38e09a",
            ])
    if 0:
        R = "blk blu brn cyn grn gry mag orn red vio wht yel".split()
        S = "pnk lip lav lil pur roy den sky trq sea lwn olv".split()
        from columnize import Columnize
        out = []
        dump = 0
        for i in main:
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
            if dump:
                print(f"{t(c)}{name:4s} {c.xhsv} {c.xrgb} {c.xhls} {c}{t.n}")
            else:
                out.append((name, c))
        if dump:
            exit()
        # Print the colors out by row
        for name, c in out:
            if len(name) == 3:
                print()
            print(f"{t(c)}{name:>4s}{t.n} ", end="")
        exit()
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
    def GetColorSeq():
        out = []
        dump = 0
        for i in main:
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
            if dump:
                print(f"{t(c)}{name:4s} {c.xhsv} {c.xrgb} {c.xhls} {c}{t.n}")
            else:
                out.append((name, c))
        if dump:
            exit()
        return out    
    def DumpDict(seq):
        print(dedent("""
        '''
        Name strings to Color instance mapping

            This file is my basic set of colors for use in terminal programs with the
            color.py module.

            The first set of 12 colors were motivated by the resistor color code: blk
            brn red orn yel grn blu vio gry wht.  I added cyn and mag because these
            two colors are used a lot.  Suffixes of "d" for "dark", "l" for "light",
            and "b" for "background" were added.  Most of these are gotten by
            changing the L parameter in the hue, lightness, saturation coordinates.
            Note that small inconsistencies exist in the hex strings for these HLS
            definitions because of float rounding characteristics of the python
            colorsys module's functions.

            The second set of color names added the following names, trying to stick
            with a 3-letter naming scheme:

                - pnk   Pink
                - lip   Lipstick
                - lav   Lavender
                - lil   Lilac
                - pur   Purple
                - roy   Royal blue
                - den   Denim
                - sky   Sky blue
                - trq   Turquoise
                - sea   Sea green
                - lwn   Lawn
                - olv   Olive
            
            A basic naming goal was that the name should evoke that color in my mind.
            This, of course, is subjective, so feel free to define things to your
            needs.

            Note these definitions rely on an 8-bit color environment.

            For a preview of the colors, run the script /plib/pgm/cdec.py with this
            filename as its argument.
        '''
        """))
        print(dedent('''
        # Copyright, license
            # These "trigger strings" can be managed with trigger.py
            #∞copyright∞# Copyright © 2022 Don Peterson #∞copyright∞#
            #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
            #∞license∞#
            #   Licensed under the Open Software License version 3.0.
            #   See http://opensource.org/licenses/OSL-3.0.
            #∞license∞#
            #∞what∞#
            # colornames0 module to define basic Color instances
            #∞what∞#
            #∞test∞# #∞test∞#

        from color import Color

        colornames = {
        '''))
        for name, c in seq:
            print(f"    {name!r:6s}:  Color({c.xhls!r}, bpc=8),")
        print("}")
    def Decorate():
        'Print the color names in their colors'
        out = GetColorSeq()

if __name__ == "__main__":
    d = {}      # Options dictionary
    arg = ParseCommandLine(d)
    seq = GetColorSeq()
    DumpDict(seq)
#vim: tw=85
