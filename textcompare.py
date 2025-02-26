"""
Compare the whitespace-separated tokens in two text strings.  The use
case for this tool is comparing open source licenses, which are
typically 7-bit ASCII text but with differing whitespace.  Run as a
script to compare two files.
"""

import difflib
import hashlib
import io


class TextCompare:
    """Compares two text strings.  Useful attributes:
        diff    Returns a string describing how to change old to new
        equal   Returns True if the normalized strings are equal
        i       Ignore case in comparison if True
        ratio   Returns a number that tells you how close the strings are
                (if 1, they are equal).
        t       Number of tokens in file if they are equal
        x       Print diff offsets in hex if True
    Normalization is done by tokenizing on whitespace, then separating
    tokens by space characters.
    """

    def __init__(self, old: str, new: str):
        self.old = old
        self.new = new
        if not isinstance(old, str):
            raise TypeError(f"old must be a text string")
        if not isinstance(new, str):
            raise TypeError(f"new must be a text string")
        self._hex_offsets = False
        self._ignore_case = False

    def normalize(self, text):
        "Tokenize on whitespace and separate with one space character"
        s = " ".join(text.split())
        return s.lower() if self.i else s

    @property
    def diff(self):
        "Return a string showing how to convert old to new"
        F, O = ("x", "0x") if self.x else ("d", "")  # Format for offsets
        f = io.StringIO()
        print("To convert old to new:", file=f)
        old = self.normalize(self.old)
        new = self.normalize(self.new)
        s = difflib.SequenceMatcher(lambda x: x == " ", old, new)
        for o in s.get_opcodes():
            tag, o1, o2, n1, n2 = o
            if tag == "replace":
                print(
                    f"{tag} {O}{o1:{F}}:{O}{o2:{F}} {old[o1:o2]!r} "
                    f"with {O}{n1:{F}}:{O}{n2:{F}} {new[n1:n2]!r}",
                    file=f,
                )
            elif tag == "delete":
                print(f"{tag} {O}{o1:{F}}:{O}{o2:{F}} = {old[o1:o2]!r}", file=f)
            elif tag == "insert":
                print(f"{tag} at {O}{o1:{F}}:  {new[n1:n2]!r}", file=f)
        return f.getvalue().rstrip()

    @property
    def equal(self):
        "Return True if the normalized hashes are equal"
        f = hashlib.sha256
        old = self.normalize(self.old).encode()
        new = self.normalize(self.new).encode()
        o, n = f(), f()
        o.update(old)
        n.update(new)
        return o.digest() == n.digest()

    @property
    def i(self):
        "If True, ignore case in comparison"
        return bool(self._ignore_case)

    @i.setter
    def i(self, value):
        self._ignore_case = bool(value)

    @property
    def ratio(self):
        "Returns a ratio on [0, 1] that measures equality (equal is 1)"
        old = self.normalize(self.old)
        new = self.normalize(self.new)
        s = difflib.SequenceMatcher(lambda x: x == " ", old, new)
        ratio = s.ratio()
        # Make sure the returned ratio has enough decimal places
        r = f"{round(ratio, 2)}"
        if ratio != 1:
            n = 2
            r = f"{round(ratio, n)}"
            while int(float(r)) == 1:
                n += 1
                r = f"{round(ratio, n)}"
        return float(r)

    @property
    def t(self):
        "Number of tokens in file if they are equal; 0 otherwise"
        return len(self.old.split()) if self.equal else 0

    @property
    def x(self):
        "If True, use hex for offsets in diff string"
        return bool(self._hex_offsets)

    @x.setter
    def x(self, value):
        self._hex_offsets = bool(value)


if __name__ == "__main__":
    # Standard library modules
    import getopt
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx

    # Custom modules
    from lwtest import run, raises, assert_equal
    from wrap import dedent

    # Try to import the color.py module; if not available, the script
    # should still work (you'll just get uncolored output).
    try:
        import xcolor as C

        _have_color = True
    except ImportError:
        # Make a dummy color object to swallow function calls
        class Dummy:
            def fg(self, *p, **kw):
                pass

            def normal(self, *p, **kw):
                pass

            def __getattr__(self, name):
                pass

        C = Dummy()
        _have_color = False
    if 1:  # Script base code

        def Error(msg, status=1):
            print(msg, file=sys.stderr)
            exit(status)

        def Usage(d, status=1):
            name = sys.argv[0]
            s = dedent(f"""
        Usage:  {name} [options] file1 file2
          Compare the two files by tokens to see if they are equal.  An example
          is comparing the text of two open source licenses.  A message is
          printed to stdout telling you whether they are equal or not.  If a 
          file is binary, it is decoded with UTF-8.
        
          The comparison method is to tokenize the files on whitespace and turn
          them into a string of tokens separated by space characters.  If the
          two strings are equal, the files are equal.
        
          If the files are not equal, a decimal number is printed telling you
          how close they are.  The closer this number is to 1, the more alike
          the files are.
        
          Return value is 0 if files are equal and 1 if they are not.
        
          Warning:  the difflib module's tools can take a long time for
          files with more than on the order of 1e4 tokens.
        
        Options:
            -D          Dump tokens to stdout
            -d          Print a diff showing how to convert file1 to file2
            -H          Print to stdout an HTML difference of the tokens
            -h          Print a manpage
            -i          Ignore case
            -x          Use hex offsets in diff
            --self      Run self tests
            --test      Run regression test file named test/X_test.py 
                        where X is the name of this script
            --Test f    Run regression test file f
            """)
            print(s)
            exit(status)

        def ParseCommandLine(d):
            d["-D"] = False  # Dump tokens to stdout
            d["-d"] = False  # Show diff
            d["-H"] = False  # Show HTML diff of tokens
            d["-i"] = False  # Ignore case
            d["-x"] = False  # Use hex for offsets in diff
            d["--example"] = False  # Run examples
            d["--self"] = False  # Run self tests
            d["--test"] = False  # Run tests in test/
            d["--Test"] = None  # Run tests in another file
            d["special"] = False  # If True, one of --example,
            # --self, or --test was given
            try:
                opts, args = getopt.getopt(
                    sys.argv[1:], "Ddhix", "example help self test Test=".split()
                )
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o[1] in list("Ddix"):
                    d[o] = not d[o]
                elif o in ("-h", "--help"):
                    Usage(d, status=0)
                elif o == "--example":
                    d["--example"] = True
                elif o == "--test":
                    d["--test"] = True
                elif o == "--Test":
                    d["--Test"] = a
                elif o == "--self":
                    d["--self"] = True
            d["special"] = d["--example"] or d["--self"] or d["--test"] or d["--Test"]
            if not args and not d["special"]:
                Usage(d)
            if len(args) != 2:
                Usage(d)
            return args

        def GetFile(file):
            s = open(file, "rb").read()
            return s.decode()

    if 1:  # Test code

        def Assert(cond):
            """Same as assert, but you'll be dropped into the debugger on an
            exception if you include a command line argument.
            """
            if not cond:
                if args:
                    print("Type 'up' to go to line that failed")
                    xx()
                else:
                    raise AssertionError

        def Test_1():
            pass

    if 1:  # Example code for module

        def Example_1():
            print("example 1")
            pass

    # ----------------------------------------------------------------------
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if d["special"]:
        if d["--self"]:
            r = r"^Test_"
            failed, messages = run(globals(), regexp=r)
        elif d["--example"]:
            r = r"^Example_"
            failed, messages = run(globals(), regexp=r, quiet=True)
        elif d["--Test"]:
            # Execute external test file
            e = sys.executable
            st = os.system(f"{e} {d['--Test']}")
            exit(st)
        elif d["--test"]:
            # Execute test file in test/
            e = sys.executable
            p = pathlib.Path(sys.argv[0])
            name = p.stem
            testfile = f"test/{name}_test.py"
            st = os.system(f"{e} {testfile}")
            exit(st)
    else:
        # Normal execution
        file1, file2 = args
        old = GetFile(file1)
        new = GetFile(file2)
        tc = TextCompare(old, new)
        tc.i = d["-i"]
        tc.x = d["-x"]
        if d["-D"]:
            # Dump tokens
            t = tc.normalize(tc.old)
            print(f"file1 ('{file1}', {len(t)} tokens)")
            print(t)
            print()
            t = tc.normalize(tc.new)
            print(f"file2 ('{file2}', {len(t)} tokens)")
            print(t)
            print()
        if tc.equal:
            C.fg(C.lgreen)
            print(f"Files are equal ({tc.t} tokens)")
            C.normal()
            exit(0)
        else:
            C.fg(C.lred)
            print(f"Files are not equal (ratio = {tc.ratio})")
            C.normal()
            if d["-d"]:
                print(tc.diff)
            exit(1)
