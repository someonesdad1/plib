if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Identify file differences between /plib and /pylib oo>
        <oo desc ∞ Description oo>
        <oo copy ∞ Copyright © 2021 Don Peterson oo>
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
    if 1:  # Standard modules
        import getopt
        import pathlib
        import sys
    if 1:  # Custom modules
        from cmddecode import CommandDecode
        from wrap import dedent
        from columnize import Columnize
        if 0:
            import debug
            debug.SetDebugger()  # Start debugger on unhandled exception
    if 1:  # Global variables
        commands = "report details diff".split()
        P = pathlib.Path
if 1:  # Utility
    def eprint(*p, **kw):
        "Print to stderr"
        print(*p, **kw, file=sys.stderr)
    def Error(msg, status=1):
        eprint(msg)
        exit(status)
    def Usage(d, status=1):
        name = sys.argv[0]
        print(dedent( f'''
        Usage:  {name} [options] cmd [file1 ...]
          Analyze differences between /plib and /pylib.  cmd:
            diff               Show files in /plib that differ from /pylib
            report             Show summary report
            details files...   Explain how they differ
        Options:
          -a  Print a manpage.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False  # Show all
        try:
            opts, args = getopt.getopt(sys.argv[1:], "a")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
        if not args:
            Usage(d)
        return args
if 1:  # Core functionality
    def GetCommand(cmd):
        c = CommandDecode(commands)
        candidates = c(cmd)
        if len(candidates) == 1:
            return candidates[0]
        elif len(candidates) > 1:
            eprint(f"Ambiguous command:  {' '.join(candidates)}")
        else:
            eprint(f"Command '{cmd}' not recognized")
        exit(1)
    def GetFiles():
        "Return dictionaries keyed by file name (value is pathlib.Path)"
        pl = set(P("/plib").glob("*.py"))
        py = set(P("/pylib").glob("*.py"))
        plib, pylib = {}, {}
        for i in pl:
            plib[i.name] = i
        for i in py:
            pylib[i.name] = i
        return plib, pylib
if 1:  # Core functions
    def Details():
        pass
    def Missing():
        pass
    def Report():
        plib, pylib = GetFiles()
        common = set(plib) & set(pylib)
        if not common:
            m = f"No common files ({len(plib)} in plib, {len(pylib)} in pylib"
            print(m)
        print("Common: ", common)
    def Diff():
        plib, pylib = GetFiles()
        common = set(plib) & set(pylib)
        o = []
        for i in common:
            pl = plib[i].read_text()
            py = pylib[i].read_text()
            if pl != py:
                o.append(i)
        if o:
            print("Files that differ between /plib and /pylib:")
            for line in Columnize(o, indent="  "):
                print(line)

if __name__ == "__main__":
    d = {}  # Options dictionary
    dispatch = {
        "diff": Diff,
        "report": Report,
        "details": Details,
        "missing": Missing,
    }
    args = ParseCommandLine(d)
    cmd = GetCommand(args[0])
    dispatch[cmd]()
