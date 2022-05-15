'''
    - Bugs
        - 

    - Todo
        - o command:  dump local variables
        - Make sure a deep backtrace is readable
        - See if r vs s behavior can be changed or toggled


This module colorizes parts of the python debugger output using the
color.py module.  Features:
    - Added the 'cls' command to clear the screen
    - The three colorizations I wanted were:
        - The current line in a list command
        - Colorize the line number in the current line
        - Error messages 
        - The 'clr' command can be used to choose the colorizing colors or turn
        them off.
 
    To use this to debug my code, I insert the line
 
        from dpdb import set_trace as xx 
 
    in the code, then put 'xx()' where I want to debug (later python
    versions use 'breakpoint' for this).
 
    To avoid having to go too deep in the pdb/bdb code, I chose to use
    regular expressions to find the lines I wanted to colorize in the 
    Pdb.message() method, so I overrode it with the definition here.
    There may be some corner cases where it doesn't work right yet.

    Tips on the python debugger (pdb.py)
        - You can provide command aliases in a ~/.pdbrc or ./.pdbrc file to
          help with custom commands.  Example:  'alias i interact' lets you
          type 'i' to jump into the python REPL.
        - Aliases won't get explained when you use help.  Thus, 'h i' for
          the previous alias shows nothing (type 'alias' to see a list).  
        - You can edit the pdb.py file to add commands.  For example, I use
          tbreak a lot and like to use tb for this like gdb works.  Go to
          the pdb source code and find 'def do_tbreak()'.  After the method
          ends, add 'do_tb = do_tbreak' and now tb works and will be part
          of the built-in commands.
            - Caution:  it's easy to go hog-wild adding new stuff.  You're
              then creating a mental dependency and you'll suffer if you
              have to debug on another system that doesn't have your added
              stuff.
        - Learn what all the debugger commands do by typing 'help cmd'.  To
          get a more readable listing, start the python REPL, type 'import
          pdb', and type 'help(pdb)'.
        - I use terminal windows with lots of lines (50-100) and the 11
          lines displayed by the pdb debugger are not enough.  See the code
          below for how to change do_list() to show more lines.
'''
from pdb import Pdb
import linecache
import re
import os
import sys
import inspect
from wrap import dedent
from color import Color, Trm, TRM as t, RegexpDecorate
from pathlib import Path
from collections import deque
from f import flt, cpx
from decimal import Decimal
if 1:   # Functions to set up colorizing strings
    def All():
        'Fancier set of colors'
        t.current_line = t("cynl")
        t.directory = t("brnl")
        t.filename = t("trq")
        t.linenum = t("yell")
        t.function = t("lavl")
        t.error = t("redl")
        t.ret = t("viol")
    def LineNumOnly():
        'Minimal set of colors'
        t.current_line = t("cynl")
        t.directory = t("wht")
        t.filename = t("wht")
        t.linenum = t("grnl")
        t.function = t("wht")
        t.error = t("redl")
        t.ret = t("viol")
    def NoColors():
        t.current_line = ""
        t.directory = ""
        t.filename = ""
        t.linenum = ""
        t.function = ""
        t.error = ""
        t.ret = ""
if 1:   # Global variables
    color_choice = LineNumOnly
    color_choice()
    # Set to True to see each line's repr() string
    dbg = len(sys.argv) > 1
    dbg = 0
    ii = isinstance
if 1:   # Regular expressions
    # Identify current line in list command.  'B' can be in the string
    # if the line is a breakpoint.  Pdb.do_list() indicates '>>' can be
    # used to indicate a line where an exception was raised if it differs
    # from the current line.
    rlist = re.compile(r"^\s*(\d+)(\s+[B]?[->]>\s*.*)$")
    # Identify current line when stepping
    rcurr = re.compile(r'''
        ^>\s        # Beginning of line is '> '
        ([^(]*?)    # Match up to parentheses for dir/filename
        \((.*?)\)   # Get text in parentheses for line number
        ([^\n]*)    # Get text up to newline for function name
        (\n.*)$     # String to end of line for current line
        ''', re.M|re.X)
    # Identify a (simple) return
    rret = re.compile(r"--Return--")
    # Regular expression decorator
    rd = RegexpDecorate()
    rd.register(rret, Color("viol"))

class DPdb(Pdb):
    if 1:   # Overridden Pdb methods
        def message(self, msg):
            if dbg:   # Print line for debugging
                t.print(f"{t('brnl')}{msg!r}")
            try:
                # Current line being printed by list command
                mo = rlist.match(msg)
                if mo:
                    linenum, remainder = mo.groups()
                    self.current_listing_line(linenum, remainder)
                    return
                # Current stopped line
                mo = rcurr.match(msg)
                if mo:
                    file, linenum, func, remainder = mo.groups()
                    self.current_stopped_line(file, linenum, func, remainder)
                    return
                # A return
                mo = rret.match(msg)
                if mo:
                    #t.print(f"{t.ret}{msg}")
                    rd(msg, insert_nl=True)
                    return
            except TypeError:
                # This exception will occur when the 'whatis' command
                # returns a type and re.match expects a string or bytes
                pass
            # Nothing special found, so print line as normal
            print(f"{msg}")
        def error(self, msg):
            print(f"{t.error}", end="")
            t.print('***', msg, file=self.stdout)
        # This method is changed to allow more than 11 lines to be shown
        def do_list(self, arg):
            '''l(ist) [first [,last] | .]
 
            List source code for the current file.  Without arguments,
            list 11 lines around the current line or continue the previous
            listing.  With . as argument, list 11 lines around the current
            line.  With one argument, list 11 lines starting at that line.
            With two arguments, list the given range; if the second
            argument is less than the first, it is a count.
 
            The current line in the current frame is indicated by "->".
            If an exception is being debugged, the line where the
            exception was originally raised or propagated is indicated by
            ">>", if it differs from the current line.
            '''
            numlines = 50       # DP
            half = numlines//2  # DP
            self.lastcmd = 'list'
            last = None
            if arg and arg != '.':
                try:
                    if ',' in arg:
                        first, last = arg.split(',')
                        first = int(first.strip())
                        last = int(last.strip())
                        if last < first:
                            # assume it's a count
                            last = first + last
                    else:
                        first = int(arg.strip())
                        #first = max(1, first - 5)
                        first = max(1, first - half)   # DP
                except ValueError:
                    self.error('Error in argument: %r' % arg)
                    return
            elif self.lineno is None or arg == '.':
                #first = max(1, self.curframe.f_lineno - 5)
                first = max(1, self.curframe.f_lineno - half)  # DP
            else:
                first = self.lineno + 1
            if last is None:
                #last = first + 10
                last = first + numlines     # DP
            filename = self.curframe.f_code.co_filename
            breaklist = self.get_file_breaks(filename)
            try:
                lines = linecache.getlines(filename, self.curframe.f_globals)
                self._print_lines(lines[first-1:last], first, breaklist,
                                self.curframe)
                self.lineno = min(last, len(lines))
                if len(lines) < last:
                    self.message('[EOF]')
            except KeyboardInterrupt:
                pass
        do_l = do_list
    if 1:   # New methods
        def current_stopped_line(self, file, linenum, func, remainder):
            print("> ", end="")
            # Only colorize the file name portion
            p = Path(file)
            print(f"{t.directory}{p.parent}/", end="")
            print(f"{t.filename}{p.name}{t.n} ", end="")
            print(f"{t.linenum}{linenum}{t.n} ", end="")
            print(f"{t.function}{func}{t.n}", end="")
            print(f"{remainder}")
        def current_listing_line(self, linenum, remainder):
            print(f"{t.linenum}{linenum}", end="")
            t.print(f"{t.current_line}{remainder}")
        def do_clr(self, var):
            'Set colorizing:  0 = None, 1 = line number, 2 = all'
            global color_choice
            try:
                value = int(var)
            except Exception:
                value = 1
            if value == 0:
                NoColors()
                color_choice = NoColors
            elif value == 1:
                LineNumOnly()
                color_choice = LineNumOnly
            elif value == 2:
                All()
                color_choice = All
            else:
                print("value must be 0 (no color), 1 (line number), or 2 (all)")
        def do_cls(self, arg):
            'Clear the screen'
            print("\x1b[H\x1b[2J\x1b[3J")
        def do_o(self, arg):
            'Dump local variables'
            # Define our own colors
            t = Trm()
            c = color_choice != NoColors
            t.title = t("whtl") if c else ""
            t.bool = t("lipl") if c else ""
            t.float = t("ornl") if c else ""
            t.flt = t("yell") if c else ""
            t.cpx = t("royl") if c else ""
            t.int = t("grnl") if c else ""
            t.Decimal = t("magl") if c else ""
            t.string = t("sky") if c else ""
            t.bytes = t("trq") if c else ""
            t.bytearray = t("lwnl") if c else ""
            t.N = t.n if c else ""
            # Get list of FrameInfo objects
            st = inspect.stack()
            # Pop off items until we see a frame from bdb.py
            fi = st.pop()
            curr = st.pop()
            while curr.function != "trace_dispatch":
                fi = curr
                curr = st.pop()
            # Get stack frame into fr
            fr = fi.frame
            # Get the local variable dictionary
            di = fr.f_locals
            if not di:
                print("No local variables")
                return
            print(f"{t.title}Local variables:{t.N}")
            # Get length of longest name
            w = max(len(i) for i in di)
            # Print the variables
            for name in sorted(di):
                self.Decorate(name, di[name], t, w)
            breakpoint()
            # Print a key
            if c:
                t.print(f"Color coding:  ", end="")
                print(f"{t.int}int{t.N} "
                      f"{t.float}float{t.N} "
                      f"{t.flt}flt{t.N} "
                      f"{t.cpx}cpx{t.N} "
                      f"{t.Decimal}Decimal{t.N} "
                      f"{t.string}str{t.N} "
                      f"{t.bool}bool{t.N} "
                      f"{t.bytes}bytes{t.N} "
                      f"{t.bytearray}bytearray{t.N} "
                     )
        def Decorate(self, name, val, t, w):
                c = ""
                if ii(val, bool):
                    c = t.bool
                elif ii(val, int):
                    c = t.int
                elif ii(val, flt):
                    c = t.flt
                elif ii(val, cpx):
                    c = t.cpx
                elif ii(val, float):
                    c = t.float
                elif ii(val, Decimal):
                    c = t.Decimal
                elif ii(val, str):
                    c = t.string
                elif ii(val, bytes):
                    c = t.bytes
                elif ii(val, bytearray):
                    c = t.bytearray
                print(f"  {c}{name:{w}s} = {val}{t.N}")
def set_trace(*, header=None):
    pdb = DPdb()
    if header is not None:
        pdb.message(header)
    pdb.set_trace(sys._getframe().f_back)
# The following two functions are needed by debug.py to let DPdb be used
# by debug.TraceInfo(). 
def post_mortem(t=None):
    # handling the default
    if t is None:
        # sys.exc_info() returns (type, value, traceback) if an exception is
        # being handled, otherwise it returns None
        t = sys.exc_info()[2]
    if t is None:
        raise ValueError("A valid traceback must be passed if no "
                         "exception is being handled")
    p = DPdb()
    p.reset()
    p.interaction(None, t)
def pm():
    post_mortem(sys.last_traceback)
