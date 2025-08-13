_pgminfo = '''
<oo 
    Convert numbers on command line to base 8, 10, 16
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat utility oo>
<oo test none oo>
<oo todo oo>
'''
if 1:  # Header
    if 1:   # Standard imports
        import getopt
        import sys
    if 1:   # Custom imports
        import termtables as tt
        from color import t
        from wrap import dedent
        from get import GetInt
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.results = []
        # Colors for output
        t.input, t.hex, t.oct, t.dec = t.brnl, t.ornl, t.sky, t.lavl
if 1:   # Utility
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] arg1 [arg2...]
          Convert arguments to base 8, 10, 16 forms.  For negative integers, use '--' to
          indicate there are no more options (or put argument in quotes).  A leading 0x,
          h, or H indicate a hex number.  A leading 0 or 0o indicate an octal integer.
          An appended ":n" indicates a base n number.
        Examples:  
          1.  '10 10.0 10.273 012 0o12 0xa ha Ha' are all forms of the number 10
          2.  '1000:32' is 32768 in base 32
        Options
          -S    Sort the output by largest to smallest
          -s    Sort the output by smallest to largest
          -x    Don't include "0x" or "0o" in output
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-S"] = False     # Sort the output by largest to smallest
        d["-s"] = False     # Sort the output by smallest to largest
        d["-x"] = False
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hSsx") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("Ssx"):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        return args
if 1:   # Core functionality
    def Convert(arg):
        try:
            n = GetInt(arg)
        except Exception:
            t.print(f"{t.ornl}Couldn't convert {arg.strip()!r}", file=sys.stderr)
            return
        if isinstance(arg, str):
            input = arg.strip()
        else:
            input = str(arg)
        hex = f"{n:x}" if d["-x"] else f"0x{n:x}"
        oct = f"{n:o}" if d["-x"] else f"0o{n:o}"
        dec = f"{n:d}"
        g.results.append((input, dec, hex, oct))
    def Report():
        header, o = (f"{t.input}Input", f"{t.dec}Decimal", f"{t.hex}Hex", f"{t.oct}Octal"), []
        # Sort g.results if necessary
        if d["-s"]:     # Sort smallest to largest
            g.results = sorted(g.results, key=lambda x: int(x[1]))
        elif d["-S"]:   # Sort largest to smallest
            g.results = sorted(g.results, key=lambda x: int(x[1]), reverse=True)
        # Colorize and append to o
        for input, dec, hex, oct in g.results:
            o.append((f"{t.input}{input}", f"{t.dec}{dec}",
                      f"{t.hex}{hex}", f"{t.oct}{oct}"))
        tt.print(o, header, style=" "*15, alignment="cccc")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    for arg in args:
        Convert(arg)
    if g.results:
        Report()
