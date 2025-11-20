_pgminfo = '''
<oo desc
    Explore the different functionality in the textwrap module.
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo license
    Licensed under the Open Software License version 3.0.
    See http://opensource.org/licenses/OSL-3.0.
oo>
<oo cat util oo>
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
        import textwrap as tw
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
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
        t.title = t.purl
        t.none = t.wht
        t.fmt = t.skyl
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
        Usage:  {sys.argv[0]} [options] choice1 [choice2...]
          Prints demos of functionality in the textwrap module.  Choices are:
          1     Simple wrapping demo
        Options:
            -h      Print a manpage
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
        GetColors()
        return args
if 1:   # Core functionality
    def SimpleWrappingDemo():
        s = ('"What can be the meaning of that emphatic exclamation?" cried he.  "Do '
            'you consider the forms of introduction, and the stress that is laid on '
            'them, as nonsense?  I cannot quite agree with you _there_.  What say '
            'you, Mary?  For you are a young lady of deep reflection, I know, and '
            'read great books and make extracts."')
        t.print(f"{t.title}Unwrapped paragraph")
        print(s)
        t.print(f"{t.title}wrap(s, width=40)")
        u = '\n'.join(tw.wrap(s, width=40))
        t.print(f"{t.fmt}{u}")
        t.print(f"{t.title}wrap(s, width=40, initial_indent=v, subsequent_indent=v) v = \" \"*12")
        v = " "*12
        u = '\n'.join(tw.wrap(s, width=40, initial_indent=v, subsequent_indent=v))
        t.print(f"{t.fmt}{u}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    for arg in args:
        if int(arg) == 1:
            SimpleWrappingDemo()
        else:
            Error(f"{arg!r} not recognized")
