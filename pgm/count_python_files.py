'''
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Count python files on my system oo>
        <oo desc ∞ Description oo>
        <oo copy ∞ Copyright © 2026 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ category oo>
        <oo test ∞ notest oo>
        <oo todo ∞ Todo items oo>
    '''
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
        import trm
        t = trm.TrmDP()
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
        # Default list of directories to search.  Most of my core files are on github,
        # so you won't see my normal /plib, etc. stuff here, as it's all under /gh.
        g.dirs = '''
            doc
            ebooks
            elec
            family_history
            gh
            manuals
            math
            pictures
            projects
            pylib
            science
            shop
            techref
            tips
            tools
            tools_cyg
        '''.split()
        # File to cache the search results
        g.cache = P("/plib/pgm/.python_file_cache")
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
    def Manpage():
        print(dedent(f'''
        This script is used to locate all the python files on my system, but it by
        default excludes .git and .hg directories.  The two primary use cases are
        1) to locate a particular python file and 2) to count the number of python files
        on my system.

        Speed is maintained by caching the directory trees in a hidden file.  Whenever
        the -u option is used, the cache is updated by the script traversing the whole
        relevant directory tree.  It is recommended that you use e.g. a daily cron job
        to keep this file updated.
        '''))
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] cmd [args]
            count   Count all files on the system if no args.  If args are given, they
                    are the regexes to count.
            locate  Locate a regex to help you find a named python file
          The script caches the count results and uses the cache for reporting.  To
          refresh the cache, use -u.
        Options:
          -h        Print a manpage
          -u        Update the cache.  If any directories are given on the command line,
                    only these directories (or their parents as appropriate) are updated.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Turn on debug
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "dh") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("d"):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        if d["-d"]:
            g.dbg = True
        GetColors()
        return args
if 1:   # Core functionality
    pass

if 0:   # Prototyping area
    p = P("/plib/pgm/count_python_files.py")
    x = p.stat()
    print(x)
    print("size", sys.getsizeof(x))
    exit()

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
