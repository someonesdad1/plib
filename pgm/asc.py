"""

TODO

Prints out ASCII characters
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2009, 2014 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Prints out ASCII/Unicode characters
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        import getopt
        import sys
        from textwrap import dedent
    if 1:  # Custom imports
        from color import t
        from columnize import Columnize
        from dpprint import PP
        from wrap import dedent
        from wsl import wsl  # wsl is True when running under WSL Linux

        pp = PP()  # Screen width aware form of pprint.pprint
    if 1:  # Global variables

        class Global:
            pass

        g = Global()
        if 0:
            g.dbg = True
        else:
            g.dbg = False
        g.decimal = False
        g.octal = False
        g.binary = False
        g.Binary = False
        g.offset = 0
        g.column_width = 9
        g.number_of_columns = 8
        g.c = True  # Colorize
if 1:  # Utility

    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )

    def GetColors():
        t.dbg = t("cyn")
        t.err = t("redl")
        t.dec = t("sky")
        t.hex = t("wht")
        t.oct = t("olv")
        t.bin = t("yeld")
        t.chr = t("yell")

    def Dbg(*p, **kw):
        if g.dbg:
            if 0:
                print(f"{t.dbg}", end="", file=Dbg.file)
                k = kw.copy()
                k["file"] = Dbg.file
                print(*p, **k)
                print(f"{t.n}", end="", file=Dbg.file)
            else:
                print(f"{t.dbg}", end="")
                k = kw.copy()
                print(*p, **k)
                t.print(f"", end="")

    Dbg.file = sys.stdout

    def Error(msg, status=1):
        print(msg)
        exit(status)

    def Usage():
        name = sys.argv[0]
        print(
            dedent(
                f"""
        Usage: {name} [options] [offset [numchars]]
          Prints the ASCII/Unicode character set starting at the indicated offset 
          for the indicated number of characters (default 0x100).
           
          offset and numchars can be expressions.  Prefix hex numbers with
          '0x', octal numbers with '0o', and binary numbers with '0b'.
           
          The character 0x7f is printed as a red block, as it typically
          won't display as a single characters.
        Options
          -B    Print the 256 binary characters
          -b    Print a binary listing
          -c    Don't colorize
          -d    Print in decimal
          -h    Print this help
          -l    Print the lower 128 characters
          -o    Print octal characters
          -u    Print the upper 128 characters
          -x    Print in hex (default)
        Example
            {name} 0x10a8*2
          will print a table of Unicode characters starting at 0x2150.
          These are Unicode fractions symbols such as 1/7, 1/9, 1/10, etc.
          and a variety of arrows and math symbols."""[1:]
            )
        )
        exit(1)

    def ParseCommandLine():
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "Bbcdhloux")
        except getopt.GetoptError as st:
            msg, option = st
            print(msg)
            sys.exit(1)
        lower, upper = 0, 256
        for o, a in optlist:
            if o == "-B":
                g.Binary = True
            elif o == "-b":
                g.binary = True
            elif o == "-c":
                g.c = not g.c
            elif o == "-d":
                g.decimal = True
            elif o == "-h":
                Usage()
            elif o == "-l":
                lower, upper = 0, 128
            elif o == "-o":
                g.octal = True
            elif o == "-u":
                lower, upper = 128, 256
            elif o == "-x":
                g.Binary = g.binary = g.decimal = g.octal = False
        GetColors()
        Dbg("Debugging turned on")
        # Get Unicode start and number of characters if present
        if args:
            Dbg(f"args = {args}")
            offset = args[0]
            numchars = None
            if len(args) > 2:
                Usage(status=1)
            if len(args) == 2:
                numchars = args[1]
            try:
                i = eval(offset)  # This handles "0x3", "0o3", "0b11", "3"
                if i < 0:
                    raise ValueError()
                g.offset = min(max(0, i), 0x10FFFF)
            except Exception:
                Error(f"'{offset}' is not a valid integer for offset (must be >= 0)")
            try:
                if numchars is None:
                    g.numchars = 256
                else:
                    g.numchars = int(numchars)
                    if g.numchars < 1:
                        raise ValueError()
            except Exception:
                Error(f"'{numchars}' is not a valid integer for numchars (must be > 0)")
        else:
            g.offset = 0
            g.numchars = 256
        if 1:  # Debug print input stuff
            Dbg(f"g.offset   = {g.offset}")
            Dbg(f"g.numchars = {g.numchars}")
            Dbg(f"Settings:")
            for i in dir(g):
                if i.startswith("_"):
                    continue
                Dbg(f"  g.{i} = {eval(f'g.{i}')}")
        return g.offset, g.offset + g.numchars


if 1:  # Core functionality

    def Integer(s):
        """Convert the string s to an integer.  Allow prefixes such as 0x,
        0b, 0o.
        """
        s, base = s.lower(), 10
        if s.startswith("0b"):
            base = 2
        elif s.startswith("0o"):
            base = 8
        elif s.startswith("0x"):
            base = 16
        return int(s, base)

    def PrintBinary():
        for i in range(lower, upper):
            c = i + g.offset
            s = " " * 4  # Spacing to make things easier to read
            print(
                f"{t.dec}{c:3d}{t.n}{s}"
                f"{t.hex}0x{c:02x}{t.n}{s}"
                f"{t.oct}0o{c:03o}{t.n}{s}"
                f"{t.bin}0b{c:08b}{t.n}{s}"
                f"{t.chr}{chr(c)}{t.n}"
            )

    def PrintBinaryListing():
        for i in range(0x100):
            c = i + g.offset
            print(chr(c))
        print()

    def PrintTable(lower, upper):
        ctrl = """
                nul soh stx etx eot enq ack bel bs ht nl vt ff cr so si dle dc1
                dc2 dc3 dc4 nak syn etb can em sub esc fs gs rs us sp
        """.split()
        out = []
        for i in range(lower, upper):
            c = ctrl[i] if i <= ord(" ") else chr(i)
            # Handle the special case of char == 0xf7, which doesn't print correctly.  We
            # replace it with a space with a red background.
            c = f"{t('redl', 'redl')} {t.n}" if i == 0x7F else c
            if g.decimal:
                out.append(f"{t.dec}{i:3d}{t.n} {t.chr}{c:3s}{t.n}")
            elif g.octal:
                out.append(f"{t.oct}{i:03o}{t.n} {t.chr}{c:3s}{t.n}")
            else:
                out.append(f"{t.hex}{i:02x}{t.n} {t.chr}{c:3s}{t.n}")
        for i in Columnize(out, col_width=g.column_width, columns=g.number_of_columns):
            print(i)


if __name__ == "__main__":
    lower, upper = ParseCommandLine()
    if g.binary:
        PrintBinary()
    elif g.Binary:
        PrintBinaryListing()
    else:
        PrintTable(lower, upper)
