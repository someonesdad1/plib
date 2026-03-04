'''
    
Miscellaneous utility routines in python: @start
    BraceExpansion        Brace expansion like modern shells
    Cfg                   Execute a sequence of text lines for config use
    Debug                 A class that helps with debugging
    EditData              Edit a str or bytes object with vim
    eng                   Convenience function for engineering format
    Engineering           Represent a number in engineering notation
    execfile              Python 3 replacement for python 2 function
    fsig                  Return string of float to specified number of digits
    getch                 Block until a key is pressed
    hyphen_range          Returns list of integers specified as ranges
    IsBinaryFile          Heuristic to see if a file is a binary file
    IsCygwinSymlink       Returns True if a file is a cygwin symlink
    IsTextFile            Heuristic to see if a file is a text file
    IterateOverSubclasses Generator to return subclasses
    Now                   Time or datetime as now
    NumBitsInByte         Returns a dict to count bits
    ProgressBar           Prints a progress bar to stdout
    ReadVariables         Read variables from a file
    ShowFile              Open indicated file(s) with registered app
    Singleton             Mix-in class for singleton pattern
    SizeOf                Estimate memory usage of an object in bytes
    Spinner               Console spinner to show activity
    TranslateSymlink      Returns what a cygwin symlink is pointing to
    US_states             Return a dict of US_states keyed by two-letter names
    Winnow                Winnow a sequence of strings with regular expressions
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Numerous utility functions oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2014 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ run oo>
        <oo todo ∞
                    
            - Missing tests for: Ignore Debug, GetString
        
        oo>
    '''
    if 1:  # Standard imports
        from collections import deque, defaultdict, OrderedDict
        from collections.abc import Iterable
        from decimal import Decimal
        from fractions import Fraction
        from itertools import chain, groupby, count
        from itertools import cycle, zip_longest, product
        from operator import itemgetter
        from pathlib import Path as P
        from random import seed
        from reprlib import repr as Repr
        import hashlib
        import inspect
        import math
        import os
        import platform
        import random
        import re
        import subprocess
        import sys
        import tempfile
        import threading
        import time
        if platform.system() == "Windows":
            import msvcrt
    if 1:  # Custom imports
        import dpmath
        from wsl import wsl
        _have_mpmath = False
        try:
            import mpmath
            _have_mpmath = True
        except ImportError:
            pass
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Import symbols
        SignSignificandExponent = dpmath.SignSignificandExponent
        AlmostEqual = dpmath.AlmostEqual
    if 1:  # Global variables
        pass
        ii = isinstance
        nl = "\n"
        fsig_lock = threading.Lock()
if 1:  # Core functionality
    def US_states():
        "Return dictionary of US state abbreviations"
        a = '''AK AL AR AZ CA CO CT DE FL GA HI IA ID IL IN KS KY LA MA MD ME MI MN MO MS MT NC ND NE
            NH NJ NM NV NY OH OK OR PA RI SC SD TN TX UT VA VT WA WI WV WY'''.split()
        b = [
            i.replace("·", " ")
            for i in '''Alaska Alabama Arkansas Arizona California Colorado
            Connecticut Delaware Florida Georgia Hawaii Iowa Idaho Illinois Indiana Kansas Kentucky
            Louisiana Massachusetts Maryland Maine Michigan Minnesota Missouri Mississippi Montana
            North·Carolina North·Dakota Nebraska New·Hampshire New·Jersey New·Mexico Nevada New·York
            Ohio Oklahoma Oregon Pennsylvania Rhode·Island South·Carolina South·Dakota Tennessee Texas
            Utah Virginia Vermont Washington Wisconsin West·Virginia Wyoming'''.split()
        ]
        return dict(zip(a, b))
    def getch():
        "Block until a key is pressed.  This function returns nothing."
        s = platform.system()
        if s == "Linux" or s.startswith("CYGWIN"):
            os.system('bash -c "read -n 1"')
        else:
            msvcrt.getch()
    def IterateOverSubclasses(cls, seen=None):
        '''Iterator over all subclasses of a given class, in depth first order.  If not
        None, seen should be a set that will contain the class names already seen.
        Downloaded Tue 12 Aug 2014 from http://code.activestate.com/recipes/576949; URL
        defunct as of 2 Feb 2026
        '''
        if not isinstance(cls, type):
            raise TypeError("IterateOverSubclasses must be called with new-style classes")
        if seen is None:
            seen = set()
        try:
            subs = cls.__subclasses__()
        except TypeError:  # Fails only when cls is type
            subs = cls.__subclasses__(cls)
        for sub in subs:
            if sub not in seen:
                seen.add(sub)
                yield sub
                for sub in IterateOverSubclasses(sub, seen):
                    yield sub
    class Singleton(object):
        "Mix-in class to make an object a singleton.  From 'Python in a Nutshell', p 84."
        _singletons = {}
        def __new__(cls, *args, **kw):
            if cls not in cls._singletons:
                cls._singletons[cls] = object.__new__(cls)
            return cls._singletons[cls]
    def Cfg(lines, lvars=OrderedDict(), gvars=OrderedDict()):
        '''Allow use of sequences of text strings to be used for general-purpose configuration
        information.  Each string must be valid python code.
        
        Each line in lines is executed with the local variables in lvars and global variables in gvars.
        The lvars dictionary is returned, which will contain each of the defined variables and
        functions.
        
        Any common leading indentation is removed before processing; this allows you to indent your
        configuration lines as desired.
        
        Example:
            lines = """
                    from math import sqrt
                    a = 44
                    b = "A string"
                    def X(a):
                        return a/2
                    c = a*sqrt(2)
                    d = X(a)
                """[1:-1].split("\n")
                
        The code
            d = Cfg(lines)
            for i in d.keys():
                print(i + " = " + str(d[i]))
                
        results in
            sqrt = <built-in function sqrt>
            a = 44
            b = A string
            X = <function X at 0x00B9C9B0>
            c = 62.2253967444
            d = 22.0
        ∞∞1 This uses exec() and could be abused.  No file in /plib is using this, so I
        think it should be obsoleted -- or at least commented out.
        '''
        # Remove any common indent
        indent = os.path.commonprefix(lines)
        if indent:
            lines = [i.replace(indent, "", 1) for i in lines]
        # Put lines into a temporary file so execfile can be used.  I
        # would have used NamedTemporaryFile(), but it doesn't work
        # correctly on Windows XP, so I used the deprecated mktemp.
        exec(nl.join(lines), gvars, lvars)
        # The things defined in the configuration lines are now in the
        # dictionary lvars.
        return lvars
    def ReadVariables(file, ignore_errors=False):
        '''Given a file of lines of python code, this function reads in each line and executes it.  If
        the lines of the file are assignments to variables, then this results in a defined variable in
        the local namespace.  Return the dictionary containing these variables.
        
        file can be a name of a file, a file-like object, a string, or a multiline string.
        
        Note that this function will not execute any line that doesn't contain an '=' character to cut
        down on the chance that some unforeseen error can occur (but, of course, this protection can
        rather easily be subverted).
        
        This function is intended to be used to allow you to have an easy-to-use configuration file for
        a program.  For example, a user could write the configuration file
        
            # This is a comment
            ProcessMean              = 37.2
            ProcessStandardDeviation = 12.1
            NumberOfParts            = 180
            
        When this function returned, you'd have a dictionary with four variables in it.
        
        If any line in the input file causes an exception, the offending line will be printed to stderr
        and the program will exit unless ignore_errors is True.
        
        ∞∞1 This uses exec() and could be abused.  No file in /plib is using this, so I
        think it should be obsoleted -- or at least commented out.
        '''
        try:
            lines = file.readlines()
        except AttributeError:
            try:
                lines = open(file).readlines()
            except FileNotFoundError:
                # Assume it's a multiline string
                lines = file.strip().split("\n")
        for i, line in enumerate(lines):
            if "=" not in line:
                continue
            try:
                exec(line)
            except Exception:
                sys.stderr.write(
                    "Line %d of file '%s' bad:\n  '%s'\n" % (i + 1, file, line.rstrip())
                )
                if not ignore_errors:
                    exit(1)
        d = locals()
        for i in "line lines i file ignore_errors".split():
            del d[i]
        return d
    def IsCygwinSymlink(file):
        "Return True if file is a cygwin symbolic link"
        s = open(file).read(20)
        if len(s) > 10:
            if s[2:9] == "symlink":
                return True
        return False
    def TranslateSymlink(file):
        "For a cygwin symlink, return a string of what it's pointing to"
        return open(file).read()[12:].replace("\x00", "")
    def IsTextFile(file, num_bytes=100):
        '''Heuristic to classify a file as text or binary.  The algorithm is to read num_bytes from the
        beginning of the file; if there are any characters other than the "typical" ones found in plain
        text files, the file is classified as binary.  This won't work on a file that contains Unicode
        characters but is otherwise plain text.  Here, "text" means plain ASCII.
        
        Note:  if file is a string, it is assumed to be a file name and opened.  Otherwise it is
        assumed to be an open stream.
        '''
        text_chars = set([ord(i) for i in "\n\r\b\t\v"] + list(range(32, 127)))
        if isinstance(file, str):
            s = open(file, "rb").read(num_bytes)
        else:
            s = file.read(num_bytes)
        for c in s:
            if ord(c) not in text_chars:
                return False
        return True
    def IsBinaryFile(file, num_bytes=100):
        "Heuristic that returns True if a file is a binary file"
        return not IsTextFile(file, num_bytes)
    class Debug:
        '''Implements a debug class that can be useful in printing debugging information.
        
        dbg = Debug()
        dbg.print("Message")
            Will print '+ Message' to stderr
        Turn off printing with 'dbg.on = False'.
        '''
        def __init__(self, stream=sys.stderr, add_nl=True, prefix="+ "):
            self.stream = stream
            self.on = True
            self.add_nl = add_nl
            self.prefix = prefix
        def print(self, s):
            if self.on:
                s = self.prefix + s
                if self.add_nl:
                    s += nl
                self.stream.write(s)
    def EditData(data, binary=False):
        "Edit a str or bytes object using vim"
        if not isinstance(data, (str, bytes)):
            raise TypeError("data must be a str or bytes object")
        if binary and isinstance(data, str):
            raise TypeError("data must be a bytes object")
        if not binary and isinstance(data, bytes):
            raise TypeError("data must be a str")
        vi = "vim"
        with tempfile.NamedTemporaryFile() as temp:
            file = P(temp.name)
            if binary:
                file.write_bytes(data)
                cmd = [vi, "-b", str(file)]
            else:
                file.write_text(data)
                cmd = [vi, str(file)]
            subprocess.call(cmd)
            if binary:
                data = file.read_bytes()
            else:
                data = file.read_text()
        return data
    def Engineering(value, digits=3):
        '''Return a tuple (m, e, s) representing a float in engineering notation.  m is the
        significand.  e is the exponent in the form of an integer; it is adjusted to be a multiple of
        3.  s is the SI symbol for the exponent; for "e+003" it would be "k".  s is empty if there is
        no SI symbol.
        
        Engineering(1.2345678901234567890e-88, 4) --> ('123.5', -90, '')
        Engineering(1.2345678901234567890e-8, 4)  --> ('12.35', -9, 'n')
        Engineering(1.2345678901234567890e8, 4)   --> ('123.5', 6, 'M')
        '''
        suffixes = {
            -10: "q", -9: "r", -8: "y", -7: "z", -6: "a", -5: "f", -4: "p", -3: "n",
            -2: "u", -1: "m", 0: "", 1: "k", 2: "M", 3: "G", 4: "T", 5: "P", 6: "E",
            7: "Z", 8: "Y", 9: "R", 10: "Q",
        }
        if digits < 1 or digits > 15:
            raise ValueError("Number of significant digits must be >= 1 and <= 15")
        sign, significand, exponent = SignSignificandExponent(float(value))
        s = suffixes[exponent // 3] if exponent // 3 in suffixes else ""
        m = sign*(("%%.%dg" % digits) % (significand*10**(exponent % 3)))
        if m.find("e") != -1:
            # digits = 1 or 2 can cause e.g. 3e+001, so the following
            # eliminates the exponential notation
            m = str(int(float(m)))
        return m, 3*(exponent // 3), s
    def eng(value, digits=3, unit=None, width=0):
        '''Convenience function for engineering representation.  If unit is given, then the number of
        digits is displayed in value with the prefix prepended to unit.  Otherwise, "xey" notation is
        used, except if y == 0, no exponent portion is given.  Returns a string for printing.  If width
        is nonzero, then returns a string right-justified to that width.
        '''
        m, e, p = Engineering(value, digits)
        if unit:
            s = m + " " + p + unit
        else:
            s = m if e == 0 else "%se%d" % (m, e)
        if width:
            if len(s) < width:
                p = " "*(width - len(s))
                s = p + s
        return s
    def BraceExpansion(s, glob=False):
        '''Generator to perform brace expansion on the string s.  If glob is True, then also glob each
        pattern in the current directory.  Examples:
        
        - BraceExpansion("a.{a,b}") returns
            ['a.a', 'a.b'].
        - BraceExpansion("pictures/*.{jpg,png}")) returns a list of
                all the JPG and PNG files in the pictures directory under the
            current directory.
        - BraceExpansion("{a,b}/*.{jpg,png}") returns
            ['a/*.jpg', 'a/*.png', ' b/*.jpg', ' b/*.png']
        - BraceExpansion("{,a}/{c,d}") returns
            ['/c', '/d', 'a/c', 'a/d']
        - BraceExpansion(r"{,,a}/{c,d}") returns
            ['/c', '/d', '/c', '/d', 'a/c', 'a/d']
        '''
        '''Algorithm from http://rosettacode.org/wiki/Brace_expansion#Python The web page's content is
        available under the GNU Free Documentation license 1.2.
        '''
        def getitem(s, depth=0):
            out = [""]
            while s:
                c = s[0]
                if depth and (c == "," or c == "}"):
                    return out, s
                if c == "{":
                    x = getgroup(s[1:], depth + 1)
                    if x:
                        out, s = [a + b for a in out for b in x[0]], x[1]
                        continue
                if c == "\\" and len(s) > 1:
                    s, c = s[1:], c + s[1]
                out, s = [a + c for a in out], s[1:]
            return out, s
        def getgroup(s, depth):
            out, comma = [], False
            while s:
                g, s = getitem(s, depth)
                if not s:
                    break
                out += g
                if s[0] == "}":
                    if comma:
                        return out, s[1:]
                    return ["{" + a + "}" for a in out], s[1:]
                if s[0] == ",":
                    comma, s = True, s[1:]
            return None
        if glob:
            for i in getitem(s)[0]:
                for j in glob.glob(i):
                    yield j
        else:
            for i in getitem(s)[0]:
                yield i
    def Spinner(chars=r"-\|/-\|/", delay=0.1):
        '''Show a spinner to indicate that processing is still taking place.  Set Spinner.stop to True
        to cause it to exit.  Note this is not thread-safe.
        
        Here's some example code that demonstrates how it could be used:
        
            from util import Spinner
            from threading import Thread
            import time
            def T():
                Spinner()
                if Spinner.stop:
                    return
            t = Thread(target=T)
            t.start()
            time.sleep(2)
            Spinner.stop = True
        '''
        # Idea from https://realpython.com/python-print/#living-it-up-with-cool-animations
        for frame in cycle(chars):
            print("\r", frame, sep="", end="", flush=True)
            time.sleep(delay)
            if Spinner.stop:
                print()
                return
    Spinner.stop = False
    def ProgressBar(frac=0, width=40, char="#"):
        '''Prints a progress bar to stdout.  frac must be a number on the closed interval [0, 1].
        
        Here's an example of use:
            n = 100
            for i in range(n + 1):
                ProgressBar(i/n)
                time.sleep(0.01)
            print()
        '''
        # Idea from https://realpython.com/python-print/#living-it-up-with-cool-animations
        assert len(char) == 1
        left = int(width*frac)
        right = width - left
        percent = int(100*frac)
        print(
            "\r[",
            char*left,
            " "*right,
            "]",
            " {}%".format(percent),
            sep="",
            end="",
            flush=True,
        )
    def execfile(filename, globals=None, locals=None, use_user_env=True):
        '''Python 3 substitute for python 2's execfile.  It gets the locals and globals from the
        caller's environment unless use_user_env is False.
        
        Caution:  you should be aware of the risks of using this function to execute arbitrary code,
        as a malicious file could e.g. wipe out your system or do other types of arbitrary damage.
        
        ∞∞1 I don't believe I've ever used this and I don't like the security
        vulnerabilities.  It could be put somewhere in commented-out form.
        '''
        # https://stackoverflow.com/questions/436198/what-is-an-alternative-to-execfile-in-python-3
        e = sys._getframe(1)
        if globals is None and use_user_env:
            globals = e.f_globals
        if locals is None and use_user_env:
            locals = e.f_locals
        with open(filename, "r") as fh:
            s = fh.read() + "\n"
            exec(s, globals, locals)
    def SizeOf(o, handlers={}, verbose=False, full=False, title=None):
        '''Returns a string containing the approximate memory in bytes used by
        an object.  Recursively uses sys.getsizeof().
        
        verbose     If True, show the details on each object.
        full        If True, use repr() instead of reprlib.repr()
        title       String for first line in verbose report
        handlers    dict(Class: Handler)
            Example handler for class:
                def Iter(s):
                    return s.attr1, s.attr2
                handler = {MyClass: Iter}
        '''
        # DP 11 Apr 2022
        # This is a modified version of
        # https://code.activestate.com/recipes/577504/.  Changes:
        #  - The ability to make verbose a stream
        #  - Indented the verbose output to see the recursion
        #  - Added the full and title keywords
        #  - Used deque to collect output
        def dict_handler(d):
            return chain.from_iterable(d.items())
        all_handlers = {
            tuple: iter,
            list: iter,
            deque: iter,
            dict: dict_handler,
            set: iter,
            frozenset: iter,
        }
        all_handlers.update(handlers)  # User handlers take precedence
        seen = set()  # Track objects seen
        default_size = sys.getsizeof(0)  # Estimate size without __sizeof__
        Repr_local = repr if full else Repr
        indent, output = 0, deque()
        if verbose:
            output.append(title) if title else output.append("Components:")
        def sizeof(o):
            nonlocal indent
            indent += 2
            if id(o) in seen:  # do not double count the same object
                return 0
            seen.add(id(o))
            sz = sys.getsizeof(o, default_size)
            if verbose:
                i = " "*(indent - 1)
                output.append(" ".join((i, str(sz), str(type(o)), Repr_local(o))))
            for typ, handler in all_handlers.items():
                if isinstance(o, typ):
                    sz += sum(map(sizeof, handler(o)))
                    break
            indent -= 2
            return sz
        total = sizeof(o)
        if verbose:
            s = output.popleft()
            s = f"{total} {s}"
            output.appendleft(s)
            return "\n".join(output)
        else:
            return total
    class Now:
        '''Example:
            s = Now()
            print(s.time())
            print(s.date())
            print(s.cdate())
        prints
            3:20pm
            11 Oct 2024
            11Oct2024
        '''
        def __init__(self):
            self._t = t = time.localtime()
            dy = self.remove_leading_zero(time.strftime("%d", t))
            mo = time.strftime("%b", t)
            yr = time.strftime("%Y", t)
            self._dt = dy, mo, yr
        def remove_leading_zero(self, s):
            if s[0] == "0":
                return s[1:]
            return s
        def time(self):
            t = self._t
            hr = self.remove_leading_zero(time.strftime("%I", t))
            min = time.strftime("%M", t)
            ampm = time.strftime("%p", t).lower()
            return f"{hr}:{min}{ampm}"
        def date(self):
            dy, mo, yr = self._dt
            return f"{dy} {mo} {yr}"
        def cdate(self):
            dy, mo, yr = self._dt
            return f"{dy}{mo}{yr}"
    def NumBitsInByte():
        'Returns a dict to count bits in a byte:  d = NumBitsInByte() and d[0xff] = 8'
        if not hasattr(NumBitsInByte, "dict"):
            NumBitsInByte.dict, bits_in_nibble = {}, tuple(bin(i).count('1') for i in range(16))
            for i in range(0x100):
                NumBitsInByte.dict[i] = bits_in_nibble[i & 0x0f] + bits_in_nibble[i >> 4]
        return NumBitsInByte.dict
    def ShowFile(*files):
        "Open indicated file(s) with registered app"
        for file in files:
            if wsl:
                # Use the ~/.0rc/bin/expl script to open a file with Explorer.  This script first
                # cd's to the file's directory, as otherwise Explorer doesn't work.
                subprocess.run(f"/home/don/.0rc/bin/expl {file}", shell=True)
            else:
                app = "d:/cygwin64/bin/cygstart.exe"  # cygwin
                subprocess.run([app, file])
    def Winnow(seq, regexps=[], OR=False, flags=re.I):
        '''Returns a set of strings contained in seq that match the regular expression strings in the
        sequence regexps.  The regexps are ANDed together unless OR is True.  flags are used in the
        re.compile() function (use 0 or re.NOFLAG to use no flags).
        '''
        if not seq:
            return set()
        if not regexps:
            return set(seq)
        # Don't modify seq or regexps
        items = set(seq)
        regexes = deque(regexps)
        if not all(ii(i, str) for i in items):
            raise TypeError("Items in seq must all be strings")
        if not all(ii(i, str) for i in regexps):
            raise TypeError("Items in *regexps must all be strings")
        results = set()
        while regexes:
            r = re.compile(regexes.popleft(), flags)
            for item in items:
                if r.search(item):
                    results.add(item)
            if not OR and regexes:
                items = results
                results = set()
        return results
    def fsig(x, digits=None):
        '''Returns a string representing the float x to a specified number of digits.  x can
        also be an integer, in which case it is converted to a float.  Similar to the 'g'
        string formatting spec, but you can control the points where fixed point
        interpolation switches to scientific notation.
        
        The fsig function attributes control other behaviors:
        
            fsig.low         Use scientific notation if x < low
            fsig.high        Use scientific notation if x >= high
            fsig.digits      Default number of significant digits
            fsig.dp          String to use for decimal point
            fsig.rdp         Remove ending decimal point if True
            fsig.rtz         Remove trailing zeroes if True
            fsig.rlz         Remove leading 0 before decimal point if True
        
        This function is not thread-safe.
        '''
        with fsig_lock:
            fsig.low = fsig.__dict__.get("low", 1e-5)
            fsig.high = fsig.__dict__.get("high", 1e6)
            fsig.digits = fsig.__dict__.get("digits", 3)
            fsig.dp = fsig.__dict__.get("dp", ".")
            fsig.rdp = fsig.__dict__.get("rdp", False)
            fsig.rtz = fsig.__dict__.get("rtz", False)
            fsig.rlz = fsig.__dict__.get("rlz", False)
            def rtz(s):
                if not fsig.rtz:
                    return s
                t = list(s)
                while t and t[-1] == "0":
                    del t[-1]
                return "".join(t)
            if fsig.low > fsig.high:
                raise ValueError("fsig.low > fsig.high")
            msg = "{}digits = {} is out of range"
            if not (1 <= fsig.digits <= 15):
                raise ValueError(msg.format("fsig.", fsig.digits))
            if digits is not None and not (1 <= digits <= 15):
                raise ValueError(msg.format("", digits))
            if not isinstance(x, (float, int)):
                raise TypeError("x must be a float or integer")
            if isinstance(x, int):
                x = float(x)
            ndig = fsig.digits - 1 if digits is None else digits - 1
            if x and (abs(x) < fsig.low or abs(x) > fsig.high):
                xs = "{:.{}e}".format(x, ndig)  # Use scientific notation
                st, e = xs.split("e")
                t = "{}e{}".format(rtz(st), int(e))
                return t.replace(".", fsig.dp)
            # xs = list of significant digits with decimal point removed
            # e = integer exponent
            xs, e = "{:.{}e}".format(abs(x), ndig).replace(".", "").split("e")
            xs, e = list(xs), int(e)
            sgn = "-" if x < 0 else ""
            if not e:
                t = "{:.{}e}".format(abs(x), ndig).split("e")[0]
                u = t.replace(".", fsig.dp)
                v = rtz(u)
                if fsig.rdp and v[-1] == fsig.dp:
                    v = v[:-1]
                return sgn + v
            elif e < 0:
                e = abs(e) - 1
                xs.reverse()
                while e:
                    xs.append("0")
                    e -= 1
                xs.append(fsig.dp)
                if not fsig.rlz:
                    xs.append("0")
                xs.reverse()
            else:
                n = len(xs)
                if e >= n:
                    e -= n - 1
                    while e:
                        xs.append("0")
                        e -= 1
                    xs.append(fsig.dp)
                else:
                    xs.insert(e + 1, fsig.dp)
            t = rtz("".join(xs))
            if fsig.rdp and t[-1] == fsig.dp:
                t = t[:-1]
            return sgn + t

if __name__ == "__main__":
    from io import StringIO
    from lwtest import run, assert_equal, raises, Assert
    from dpseq import fDistribute
    from random import seed
    from wrap import dedent
    import trm
    t = trm.Trm()
    import itertools
    import math
    import sys
    from itertools import zip_longest
    from collections import namedtuple
    seed(2**64)  # Make test sequences repeatable
    show_coverage = len(sys.argv) > 1
    # Need to have version, as SizeOf stuff changed between 3.7 and 3.9
    vi = sys.version_info
    ver = f"{vi[0]}.{vi[1]}"
    if 1:  # Debugging help
        class G:
            pass
        g = G()
        g.dbg = False
        def Dbg(*p, **kw):
            if g.dbg:
                print(f"{t.dbg}", end="")
                print(*p, **kw)
                print(f"{t.N}", end="")
    def Test_NumBitsInByte():
        d = NumBitsInByte()
        for i in d:
            assert d[i] == bin(i).count("1")  # Count 1's in binary represention
    def Test_fsig():
        fsig.digits = 2
        fsig.rtz = True
        fsig.rlz = True
        u = 1.23456789
        for x, s in (
            (u, "1.2"),
            (u*10, "12."),
            (u*100, "120."),
            (u*1e5, "120000."),
            (u*1e6, "1.2e6"),
            (u/10, ".12"),
            (u/100, ".012"),
            (u/1e5, ".000012"),
            (u/1e6, "1.2e-6"),
        ):
            Assert(fsig(x) == s, "fsig({}) != {}".format(x, s))
            Assert(fsig(-x) == "-" + s, "fsig({}) != {}".format(x, "-" + s))
    def Test_Winnow():
        s = set("ei eI Ei EI".split())
        regexps = ["e", "I"]
        # Don't ignore case
        u = Winnow(s, regexps=regexps, flags=0)
        Assert(u == {"eI"})
        # Ignore case
        u = Winnow(s, regexps=regexps, flags=re.I)
        Assert(u == s)
        # Empty item_sequence returns empty set
        Assert(Winnow([], regexps=regexps, flags=0) == set())
        # Empty regexps returns item_sequence set
        Assert(Winnow(s, regexps=[], flags=0) == set(s))
    def Test_SizeOf():
        if ver == "3.7":
            data = (
                # These numbers worked for python 3.7
                (tuple, 40),
                (list, 60),
                (deque, 328),
                (set, 124),
                (frozenset, 124),
            )
        if ver == "3.9":
            data = (
                # These numbers worked for python 3.9
                (tuple, 72),
                (list, 88),
                (deque, 648),
                (set, 240),
                (frozenset, 240),
            )
        if ver == "3.11":
            data = (
                # These numbers worked for python 3.11
                (tuple, 76),
                (list, 100),
                (deque, 788),
                (set, 244),
                (frozenset, 244),
            )
        for typ, sz in data:
            x = typ((0,))
            Assert(SizeOf(x) == sz)
        # Size of dict
        x = {1: 1}
        if ver == "3.7":
            Assert(SizeOf(x) == 146)  # For python 3.7
        elif ver == "3.9":
            Assert(SizeOf(x) == 260)  # For python 3.9
        elif ver == "3.11":
            Assert(SizeOf(x) == 252)  # For python 3.11
        else:
            Assert(SizeOf(x) == 140)  # It will fail
    def Test_Engineering():
        m, e, s = Engineering(1.2345e-6)
        Assert(float(m) == 1.23 and e == -6 and s == "u")
        m, e, s = Engineering(1.2345e-7)
        Assert(float(m) == 123 and e == -9 and s == "n")
        m, e, s = Engineering(1.2345e-8)
        Assert(float(m) == 12.3 and e == -9 and s == "n")
    def Test_eng():
        Assert(eng(3456.78) == "3.46e3")
        Assert(eng(3456.78, digits=4) == "3.457e3")
        # kkg is a illegal SI unit, but the code allows it
        Assert(eng(3456.78, unit="kg") == "3.46 kkg")
    def Test_IsTextFile():
        s = StringIO("Some text")
        Assert(IsTextFile(s))
        s = StringIO("Some text\xf8")
        Assert(not IsTextFile(s))
        # Also test IsBinaryFile()
        s = StringIO("Some text\xf8")
        Assert(IsBinaryFile(s))
    util_simlink = "c:/cygwin/pylib/test/util_simlink.py"
    translated_util_simlink = "../util.py"
    def Test_IsCygwinSymlink():
        if sys.platform == "win32":
            # For this to work, create a cygwin simlink named util_simlink.py
            # in /pylib/test that points to /pylib/util.py.
            Assert(IsCygwinSymlink(util_simlink))
            Assert(not IsCygwinSymlink("c:/cygwin/home/Don/bin/data/notes.txt"))
    def Test_TranslateSymlink():
        if sys.platform == "win32":
            # For this to work, create a cygwin simlink named util_simlink.py
            # in /pylib/test that points to /pylib/util.py.
            Assert(TranslateSymlink(util_simlink) == translated_util_simlink)
    def Test_Cfg():
        lines = dedent('''
            from math import sqrt
            a = 44
            b = "A string"
            def X(a):
                return a/2
            c = a*sqrt(2)
            d = X(a)
        ''').split("\n")
        d = Cfg(lines)
        Assert(d["a"] == 44)
        Assert(d["b"] == "A string")
        Assert(d["c"] == d["a"]*d["sqrt"](2))
        Assert(d["d"] == 22)
        Assert(str(d["X"])[:11] == "<function X")
    def Test_Singleton():
        class A(object):
            pass
        a, b = A(), A()
        Assert(hash(a) != hash(b))
        class A(Singleton):
            pass
        a, b = A(), A()
        Assert(hash(a) == hash(b))
    def Test_IterateOverSubclasses():
            class A: pass
            class B(A): pass
            class C(A): pass
            class D(C): pass
            class E(C): pass
            x = E()
            r = [str(i) for i in IterateOverSubclasses(A)]
            # Expected
            s = "<class '__main__.Test_IterateOverSubclasses.<locals>."
            expected = []
            for i in "BCDE":
                expected.append(s + i + "'>")
            Assert(r == expected)
    def Test_ReadVariables():
        code = dedent('''
        a = 3
        b = 4
        c = "5"''')
        s = StringIO(code)
        d = ReadVariables(s)
        Assert(d == {"a": 3, "b": 4, "c": "5"})
    def Test_BraceExpansion():
        # Simple
        s = " ".join(BraceExpansion("a{d,c,b}e"))
        assert s == "ade ace abe"
        #
        Assert(list(BraceExpansion("a.{a, b}")) == ["a.a", "a. b"])
        # Cartesian product
        s = list(BraceExpansion("{A,B,C,D}{A,B,C,D}"))
        t = [i + j for i, j in itertools.product("ABCD", repeat=2)]
        Assert(s == t)
        #
        s = " ".join(BraceExpansion("{a,b,c}{d,e,f}"))
        t = " ".join([i + j for i, j in product("abc", "def")])
        Assert(s == t)
        s = str(list(BraceExpansion("{a,b}/*.{jpg,png}")))
        t = "['a/*.jpg', 'a/*.png', 'b/*.jpg', 'b/*.png']"
        Assert(s == t)
        # Nested
        s = " ".join(BraceExpansion("{,a}{b,{c,d},e}"))
        t = "b c d e ab ac ad ae"
        assert s == t
    def TestParameterSequence():
        fd = fDistribute
        expected = [0.0, 1.0]
        got = list(fd(2))
        assert_equal(got, expected)
        #
        expected = [0.0, 0.5, 1.0]
        got = list(fd(3))
        assert_equal(got, expected)
        #
        expected = [Fraction(0, 1), Fraction(1, 2), Fraction(1, 1)]
        got = list(fd(3, impl=Fraction))
        assert_equal(got, expected)
        #
        expected = [1.0, 1.5, 2.0]
        got = list(fd(3, a=1, b=2))
        assert_equal(got, expected)
        # Check type/value violations
        with raises(TypeError):
            list(fd(1.0))
        with raises(ValueError):
            list(fd(1))
        with raises(TypeError):
            list(fd(2, a=""))
        with raises(TypeError):
            list(fd(2, b=""))
        with raises(ValueError):
            list(fd(1, a=2, b=1))
    def Test_check_names():
        "Make sure the docstring list of names is up-to-date"
        if not check_names:
            return
        names = set()
        dq = deque(__doc__.split("\n"))
        # Position at beginning of relevant items
        while dq:
            item = dq.popleft()
            if "@start" in item:
                break
        found = False
        while dq:
            line = dq.popleft()
            if not line.strip():
                continue
            name = line.split()[0]
            if not name or name in ignore:
                continue
            names.add(name)
            if name not in mnames:
                t.print(f"{t.ornl}{name} in docstring not in module")
                found = True
        if found:
            print("-"*70)
        for name in mnames:
            if name.startswith("Test"):
                continue
            if name not in names and name not in "wsl t".split():
                print(
                    f"{t.ornl}util:Test_check_names(){t.n}:  {name} in module not in docstring"
                )
    # Make sure the docstring list of names is up-to-date'
    check_names = False
    check_names = True
    if check_names:
        mnames, delete = set(dir()), []
        ignore = '''
            __
            AlmostEqual
            Assert
            DIGITS
            Dbg
            Decimal
            Fraction
            G
            Iterable
            Miscellaneous
            OrderedDict
            P
            Repr
            SignSignificandExponent
            StringIO
            Test
            ToDo
            __annotations__
            ascii_letters
            assert_equal
            __builtins__
            __cached__
            chain
            check_names
            cmath
            combinations
            count
            cycle
            debug
            dedent
            defaultdict
            deque
            digits
            __doc__
            fDistribute
            __file__
            flt
            frange
            fsig_lock
            g
            glob
            groupby
            hashlib
            _have_mpmath
            ii
            inspect
            islice
            itemgetter
            itertools
            __loader__
            math
            mpmath
            __name__
            namedtuple
            nl
            os
            __package__
            pathlib
            _pgminfo
            platform
            product
            punctuation
            raises
            randint
            random
            re
            run
            seed
            show_coverage
            signum
            __spec__
            struct
            subprocess
            sys
            tempfile
            threading
            time
            translated_util_simlink
            util_simlink
            ver
            vi
            zip_longest
        '''.split()
        for name in mnames:
            for s in ignore:
                if name == s:
                    delete.append(name)
                    break
        for name in delete:
            mnames.discard(name)
    exit(run(globals(), halt=0, verbose=0)[0])

def GetGist():
    g = {}
    g["gist"] = "Utility functions"
    g["copy"] = "Copyright © 2026 Don Peterson"
    g["lic"] = "MIT License (see /plib/_lic.mit)"
    g["test"] = "run"
    g["cat"] = "utility"
    g["todo"] = '''
    
        - Convert Spinner to a class so the instance is thread-safe
        - Debug class should use print()'s arguments.  Also address why it's not in
          debug.py.
        - Document Now class
    
    '''
    return g
