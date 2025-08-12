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
        from color import t
        from wrap import dedent
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.results = []
if 1:   # Utility
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] arg1 [arg2...]
          Convert arguments to base 8, 10, 16 forms.  For negative integers, use '--' to
          indicate there are no more options.  A leading "0x", "h", or "H" indicate a
          hex number.  A leading "0" or "0o" indicate an octal integer.  An appended
          ":n" indicates a base n number.
        Examples:  
          1.  '10 10.0 10.273 012 0o12 0xa ha Ha' are all forms of the number 10
          2.  '10 10.0 10.273 012 0o12 0xa ha Ha' are all forms of the number 10
        Options
          -S    Sort the output by largest to smallest
          -s    Sort the output by smallest to largest
          -x    Don't include "0x" in hex form
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-S"] = False     # Sort the output by largest to smallest
        d["-S"] = False     # Sort the output by smallest to largest
        d["-x"] = False
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hx") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("x"):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        return args
if 1:   # Core functionality
    def GetInteger(arg):
        'Return arg as an integer'
    def Convert(arg):
        s = arg.strip()
        sign = "-" if s[0] == "-" else ""
        if s[0] == "-":
            s = s[1:]
        # Get hex form
        a = f"{arg.strip()}"
        try:
            if "e" in s or "E" in s:
                h = f"{sign + hex(int(float(s)))}"
            else:
                h = f"{sign + hex(int(s))}"
        except Exception:
            t.print(f"{t.ornl}Couldn't convert {arg.strip()!r}")
        else:
            g.results.append((a, h))

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    for arg in args:
        Convert(arg)
    # Report
    if g.results:
        # Get width of largest input string
        w = max(len(s) for s, _ in g.results)
        for i, o in g.results:
            t.print(f"{t.yel}{i:{w}s} {t.sky}{o}")
