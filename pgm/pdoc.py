"""
Display python files without header information

    The default behavior is to search for lines with "#∞x∞#" were x is one of the keywords
    copyright, contact, category, license, what, and test.

"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Display python files without header information
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import subprocess
        import sys
    if 1:  # Custom imports
        from color import t
        from dpprint import PP

        pp = PP()  # Screen width aware form of pprint.pprint
        from get import GetLines
        from wrap import dedent
        from wsl import wsl  # wsl is True when running under WSL Linux
        from lwtest import Assert

        if 1:
            import debug

            debug.SetDebugger()
    if 1:  # Global variables

        class G:  # Storage for global variables as attributes
            pass

        g = G()
        g.dbg = False
        # Collect file/directory data from command line
        g.ok = []  # Have the #∞...∞# lines and are complete
        g.have = []  # Have the #∞...∞# lines, but incomplete
        g.have_not = []  # Do not have any #∞...∞# lines
        ii = isinstance
if 1:  # Utility

    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )

    def GetColors():
        t.dbg = t("cyn") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("ornl")
        t.ok = t("grnl")

    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)

    Dbg.file = sys.stdout

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=0):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] [arg1 [arg2...]]
          Examine the arguments (assumed to be python files) and print out those that need 
          work.  The goal is to 
        Options:
            -h      Print a manpage
            -v      Print the files that are in good shape
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-r"] = False  # Recursively search for python scripts
        d["-v"] = False  # Print files in good shape
        if 0 and len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hrv")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("rv"):
                d[o] = not d[o]
            elif o == "-h":
                Usage(status=0)
        GetColors()
        g.W, g.L = GetScreen()
        return args


if 1:  # Classes

    class File:
        def __init__(self, file, lines):
            self.file = file
            self.lines = lines
            # Attributes
            self.copyright = 0
            self.contact = 0
            self.license = 0
            self.what = 0
            self.test = 0
            self.category = 0
            # Get the keywords
            for line in lines:
                line = line.strip()
                if line.startswith("#∞copyright∞#"):
                    self.copyright += 1
                    Assert(line.endswith("#∞copyright∞#"))
                elif line.startswith("#∞contact∞#"):
                    self.contact += 1
                    Assert(line.endswith("#∞contact∞#"))
                elif line.startswith("#∞license∞#"):
                    self.license += 1
                elif line.startswith("#∞what∞#"):
                    self.what += 1
                elif line.startswith("#∞test∞#"):
                    self.test += 1
                    Assert(line.endswith("#∞test∞#"))
                elif line.startswith("#∞category∞#"):
                    self.category += 1
                else:
                    Error(f"{line!r} not recognized")

        def get_errors(self):
            "Return string of attributes that are incorrect"

            def Strip(s):
                return s.replace("#∞", "").replace("∞#", "")

            errors = []
            if not self.copyright:
                errors.append(Strip("#∞copyright∞#"))
            elif not self.contact:
                errors.append(Strip("#∞contact∞#"))
            elif self.license != 2:
                errors.append("two license")
            elif self.what != 2:
                errors.append("two what")
            elif not self.test:
                errors.append(Strip("#∞test∞#"))
            elif not self.category:
                errors.append(Strip("#∞category∞#"))
            return ",".join(errors)

        def ok(self):
            errors = self.get_errors()
            return not bool(errors)

        def dump_no_errors(self):
            "Print filename if the #∞...∞# attributes are ok"
            errors = self.get_errors()
            if not errors:
                t.print(f"{t.ok}{self.file}")

        def dump_errors(self, width):
            "Print the errors"
            errors = self.get_errors()
            if errors:
                print(f"{t.err}{self.file:{width}s}{t.n} {errors}")


if 1:  # Core functionality

    def Process(file):
        p = P(file)
        if p.is_dir():
            if d["-r"]:
                files = p.glob("**/*.py")
            else:
                files = p.glob("*.py")
        elif p.is_file():
            files = [p]
        else:
            Error(f"{file!r} is not a file or directory")
        # Process each file
        r1 = re.compile(r"^[^#]*$")  # Ignore lines with no '#'
        s = "|".join("copyright contact license what test category".split())
        r2 = re.compile(f"^ *#∞({s})∞#")  # Find #∞...∞# lines
        have = []  # List of files that have #∞...∞# lines
        have_not = []  # List of files that don't have #∞...∞# lines
        for file in files:
            lines = GetLines(file, ignore=[r1], ignore_empty=True, nonl=True)
            file_keep_lines = [i.strip() for i in lines if r2.search(i)]
            if file_keep_lines:
                # File had some #∞...∞# lines
                f = File(file, file_keep_lines)
                if f.ok():
                    g.ok.append(f)
                else:
                    g.have.append(f)
            else:
                # File had no #∞...∞# lines
                g.have_not.append(file)

    def Report():
        if d["-v"]:
            # Print files that are OK
            for i in sorted(g.ok):
                print(f"{i.file}")
        else:
            # Print files missing #∞...∞# lines.
            # Get maximum width.
            o = []

            have = [i for i in have if i]  # Remove empty
            w = max(len(str(i.file)) for i in have)
            for f in have:
                errors = f.get_errors()
                print(f"{t.err}{str(f.file):{w}s}{t.n} {errors}")


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if not args:
        breakpoint()  # xx
    else:
        for i in args:
            Process(i)
    Report()
