"""
This module finds all the python files in /plib, then searches all
other directories for python files and finds those that import /plib
modules.

This script will fail on lines like the following:

    from modulename import (x,
        y, z)

because it uses a regexp on each line.  Because of this, a function will
detect lines like 'from modulename import (x,' and stop with an error.
The suggested fix is to rewrite things as:

    from modulename import x
    from modulename import y, z

I feel it's better to just use 'import modulename', but sometimes the
above style is useful to reduce the length of symbol names.

Other policies enforced by this script are:

    * The python files and modules must either be plain ASCII text or
      UTF-8 encoded.
"""

# ∞test∞# ignore #∞test∞#
if 1:  # Standard imports
    import getopt
    import io
    import os
    import pathlib
    import re
    import sys
    from collections import defaultdict
    from pprint import pprint as pp
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import wrap, dedent, indent, Wrap
    from columnize import Columnize
if 1:  # Global variables
    P = pathlib.Path
    # This will collect bad import lines that need fixing
    bad = set()
if 1:  # Utility

    def eprint(*p, **kw):
        "Print to stderr"
        print(*p, **kw, file=sys.stderr)

    def Error(msg, status=1):
        eprint(msg)
        exit(status)

    def Usage(d, status=1):
        name = sys.argv[0]
        print(
            dedent(f"""
        Usage:  {name} [options] etc.
        Explanations...
        
        Options:
          -h
            Print a manpage.
        """)
        )
        print(s.format(**locals()))
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3  # Number of significant digits
        if len(sys.argv) < 2:
            Usage(d)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o in ("-a",):
                d["-a"] = not d["-a"]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(d, status=0)
        if len(args) < 2:
            Usage(d)
        return args


if 1:  # Core functionality

    def GetModuleNames() -> set:
        "Return set of module names"
        # Assumes we're in the correct directory
        return set(P(".").glob("*.py"))

    def GetSourceFiles(modules: set) -> set:
        "Get all source files that are not modules"
        ignore = set(
            [
                P(i)
                for i in """
            pgm/words.py 
            pgm/words_syllables.py
            interval/interval_orig.py
            pgm/words.make.py
            pgm/words_syllables_old.py
            pgm/words_voa_make.py
            regress/kupper/kupper.py
            regress/wesley_phoa/1D_nonlinear_regress.py
            regress/wesley_phoa/mathutil.py
        """.split()
            ]
        )

        # Ignore files in these directories
        def f(x):
            return P(x).rglob("*.py")

        ignore.update(f("crenshaw"))
        ignore.update(f("g/demo"))
        ignore.update(f("g/gnew/demo"))
        ignore.update(f("inst"))
        ignore.update(f("matrix/old"))
        ignore.update(f("other"))
        ignore.update(f("pgm/wordlists"))
        ignore.update(f("yapf"))
        ignore.update(f("types_of_words"))
        # Find all *.py files in this tree and remove the modules and
        # ignored stuff
        p = P(".")
        source = set(p.rglob("*.py"))
        return source - ignore - modules

    def ProcessFile(file):
        """Read the file's lines and only keep those lines that have 'import'
        in them.
        """
        keep = []
        for line in open(file):
            if line.find("import") != -1:
                # Ignore comments
                if line.lstrip()[0] == "#":
                    continue
                # Ignore __future__
                if "__future__" in line:
                    continue
                # Ignore all but 'import', 'from', and 'if'
                if (
                    line.startswith("import ")
                    or line.startswith("from ")
                    or line.startswith("if ")
                ):
                    keep.append(line)
        return keep

    def Used(line, modules):
        found = []
        for m in modules:
            if m in line:
                found.append(m)
        return found

    def NotAComment(line):
        s = line.lstrip()
        return s and s[0] != "#"

    def GetFilesImportLines(file: P) -> list:
        "Return lines that aren't comments that contain 'import'"
        lines = []
        for line in file.read_text(encoding="UTF-8").split("\n"):
            if GetFilesImportLines.r.match(line):
                lines.append(line)
            if NotAComment(line):
                # Check for other regexps; if get a match, put in bad
                # container.
                for r in GetFilesImportLines.regexps:
                    if r.search(line):
                        msg = f"{file}:  '{line}'"
                        bad.add(msg)
        return lines

    GetFilesImportLines.r = re.compile(r"^\s*import |^\s*from\s+.*\s+import\s+")
    GetFilesImportLines.regexps = (
        re.compile(r"\bprint\s+[^(]"),
        re.compile(r"\blong\b"),
        re.compile(r"\bexecfile\b"),
        re.compile(r"\bxrange\b"),
        re.compile(r"\bexcept\s*\w+,\b"),
        re.compile(r"\bunicode\b"),
    )

    def BadImportLine(line, file):
        """Stop on a bad import line like
            'from x import (y, z, '
        that doesn't contain ')'.
        """
        assert "import" in line
        if "(" in line and ")" not in line:
            bad.add(str(file))

    def FileUsesModule(import_lines: list, module: P, file: P) -> bool:
        def ScrubLine(line):
            'Replace "(", ")", and "," with space characters'
            s = " "
            return line.replace("(", s).replace(")", s).replace(",", s)

        name_token = module.name[:-3]
        for line in import_lines:
            BadImportLine(line, file)
            tokens = ScrubLine(line).split()
            if name_token in tokens:
                return True
        return False

    def GetUsed(modules: set, sources: set) -> dict:
        """Return a dict of module names with the list of the file(s)
        in sources that import that name.  An example entry would be:
            P("sig.py"): [P("pgm/file1.py"), P("pgm/file2.py"), ...],
        where P is a pathlib.Path instance.
        """
        assert all([str(i).endswith(".py") for i in modules])
        module_names = [i.name[:-3] for i in modules]
        out = defaultdict(list)
        for file in sources:
            try:
                import_lines = GetFilesImportLines(file)
            except UnicodeDecodeError:
                print(f"Unicode error for '{file}'")
                exit()
            if not import_lines:
                continue
            for module in modules:
                if FileUsesModule(import_lines, module, file):
                    out[module].append(file)
        return out


if __name__ == "__main__":
    d = {}  # Options dictionary
    os.chdir("/plib")
    modules = GetModuleNames()
    source = GetSourceFiles(modules)
    used_dict = GetUsed(modules, source)
    if bad:
        print("These files need import lines fixed that are missing ')':")
        for line in sorted(bad):
            print(f"  {line}")
        exit(1)
