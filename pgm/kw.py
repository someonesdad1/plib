"""
List keywords etc. of python
"""
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright © 2025 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # List keywords etc. of python
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        Globals = globals().copy()  # Before any imports
        from collections import deque, defaultdict
        from functools import partial
        from pathlib import Path as P
        import getopt
        import keyword
        import os
        import re
        import sys
    if 1:  # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from columnize import Columnize
        from dpprint import PP
        pp = PP()
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:  # Utility
    def GetColors():
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=0):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        """)
        )
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False  # Need description
        d["-d"] = 3  # Number of significant digits
        if 0 and len(sys.argv) < 2:
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
        return args
if 1:  # Core functionality
    COLUMNIZE5 = partial(Columnize, columns=5, sep=" " * 5, indent=" " * 4)
    COLUMNIZE3 = partial(Columnize, columns=3, indent=" " * 4)
    foldsort = partial(sorted, key=str.lower)
    def PythonVersion():
        t.print(f"{t.redl}Python {'.'.join(str(i) for i in sys.version_info[:3])}")
        t.print(f"{' ' * 4}{t.sky}{sys.version}")
    def Keywords():
        t.print(f"{t.ornl}Python keywords:")
        for i in COLUMNIZE5(keyword.kwlist):
            print(i)
    def GlobalsBeforeImport():
        t.print(f"{t.ornl}Globals before any imports:")
        for i in COLUMNIZE5(Globals.keys()):
            print(i)
    def GlobalsAfterImport():
        t.print(f"{t.ornl}Globals after imports:")
        for i in Columnize(globals().keys(), columns=4, indent=" " * 4):
            print(i)
    def ExceptionSet():
        'Taken from HTML manpage for "Built-in Exceptions"'
        exceptions_3_12_2 = """
            ArithmeticError AssertionError AttributeError BaseException BaseExceptionGroup
            BlockingIOError BrokenPipeError BufferError BytesWarning ChildProcessError
            ConnectionAbortedError ConnectionError ConnectionRefusedError ConnectionResetError
            DeprecationWarning EOFError EncodingWarning EnvironmentError Exception
            ExceptionGroup FileExistsError FileNotFoundError FloatingPointError FutureWarning
            GeneratorExit IOError ImportError ImportWarning IndentationError IndexError
            InterruptedError IsADirectoryError KeyError KeyboardInterrupt LookupError
            MemoryError ModuleNotFoundError NameError NotADirectoryError NotImplementedError
            OSError OverflowError PendingDeprecationWarning PermissionError ProcessLookupError
            RecursionError ReferenceError ResourceWarning RuntimeError RuntimeWarning
            StopAsyncIteration StopIteration SyntaxError SyntaxWarning SystemError SystemExit
            TabError TimeoutError TypeError UnboundLocalError UnicodeDecodeError
            UnicodeEncodeError UnicodeError UnicodeTranslateError UnicodeWarning UserWarning
            ValueError Warning WindowsError ZeroDivisionError""".split()
        return set(exceptions_3_12_2)
    def Builtins():
        t.print(f"{t.ornl}Builtins in __builtins__.__dict__:")
        # Categorize the builtins by type
        di = __builtins__.__dict__
        items = defaultdict(list)
        for i in foldsort(di):
            typ = str(type(di[i]))
            items[typ].append(i)
        for k in foldsort(items):
            i = k.replace("<class '", "").replace("'>", "")
            if i == "type":
                continue
            t.print(f"{t.purl}  {i}")
            for j in COLUMNIZE5(items[k]):
                print(j)
        # Handle 'type' key specially:  divide into classes & errors/warnings
        exceptions_3_12_2 = ExceptionSet()
        # Print types
        o = []
        for i in items["<class 'type'>"]:
            if i in exceptions_3_12_2:
                continue
            o.append(i)
        t.print(f"{t.purl}  types")
        for i in COLUMNIZE5(sorted(o)):
            print(i)
        # Print exceptions & warnings
        o = []
        for i in items["<class 'type'>"]:
            if i not in exceptions_3_12_2:
                continue
            o.append(i)
        t.print(f"{t.purl}  Exceptions/warnings")
        for i in COLUMNIZE3(sorted(o)):
            print(i)

if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    PythonVersion()
    Builtins()
    GlobalsBeforeImport()
    # GlobalsAfterImport()
    Keywords()
