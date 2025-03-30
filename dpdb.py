'''
    - Todo
        - When debugging, the return value string gets truncated with '...'.  This can
          be a pain when e.g. the return value is a ufloat, as you can't see the value.
          Make it use up the available width or see if a debugger option can be used to
          let you see the whole string.
        - Add a command to change the number of lines displayed
        - po command:
            - Columnize dir() output.  First arg is object to dir, remaining args are
              regexps to search for.
        - See if r vs s behavior can be changed or toggled
        - inspect has a number of functions that could be useful for a command that's
          used to inspect an object:  it's source, docs, etc.  Call the built-in pager
          to do this.
        - Use a traceback to print the call stack on an exception.
        
This module extends the python debugger pdb.py Features:
    - Added commands
        - o         Dump local variables
        - dr obj    Prints dir() output in columns
        - cls       Clears the screen
        - clr       Set the colorizing state
    - Changed the 'list' command to output more lines.
    - Colorize certain strings to make them easier to spot:
        - The current line in a list command
        - The file and line number in the current line
        - Error messages
        - Entering the REPL
        
    To use this module to debug my code, I set the environment variable
    PYTHONBREAKPOINT to 'dpdb.set_trace' and insert 'breakpoint()' where I
    want to drop into the debugger (this is available in python 3.7 and
    later).
    
    To avoid having to go too deep in the pdb/bdb code, I chose to use
    regular expressions to find the lines I wanted to colorize in the
    Pdb.message() method, so I overrode it with the definition here.
    There may be some corner cases where it doesn't work right yet.
    
    Tips on the python debugger (pdb.py)
        - You can provide command aliases in a ~/.pdbrc or ./.pdbrc file.
          For example, I alias 'interactive' to 'i'.  Use 'alias' command
          to see your defined aliases.
        - You can edit the pdb.py file to add commands.
            - Example:  I use tbreak a lot so I added 'do_tb = do_tbreak'.
            - Caution:  it's easy to go hog-wild adding new stuff.  You're
              then creating a mental dependency and you'll suffer if you
              have to debug on another system that doesn't have your added
              stuff.  You then have an update problem when you go to a new
              python version.  That's why I try to make my changes in this
              file.
'''
##∞test∞# none #∞test∞#
from pdb import Pdb
import code
import linecache
import re
import os
import sys
import inspect
from color import Color, Trm, TRM as t, RegexpDecorate
from pathlib import Path
from collections import deque
from f import flt, cpx
from decimal import Decimal
from pprint import pprint as pp
from columnize import Columnize
if 1:  # Functions to set up colorizing strings
    def All():
        "Fancier set of colors"
        t.current_line = t("cynl")
        t.directory = t("gry")
        t.filename = t("trq")
        t.linenum = t("ornl")
        t.function = t("lavl")
        t.error = t("redl")
        t.ret = t("viol")
        t.interactive = t("blk", "yell")
    def LineNumOnly():
        "Minimal set of colors"
        t.current_line = t("cynl")
        t.directory = t("gry")
        t.filename = t("wht")
        t.linenum = t("ornl")
        t.function = t("wht")
        t.error = t("redl")
        t.ret = t("viol")
        t.interactive = t("blk", "yell")
    def NoColors():
        t.current_line = ""
        t.directory = ""
        t.filename = ""
        t.linenum = ""
        t.function = ""
        t.error = ""
        t.ret = ""
        t.interactive = ""
if 1:  # Global variables
    color_choice = All
    color_choice()
    # Set to True to see each line's repr() string
    dbg = 0
    ii = isinstance
if 1:  # Regular expressions
    # Identify current line in list command.  'B' can be in the string
    # if the line is a breakpoint.  Pdb.do_list() indicates '>>' can be
    # used to indicate a line where an exception was raised if it differs
    # from the current line.
    rlist = re.compile(r"^\s*(\d+)(\s+[B]?[->]>\s*.*)$")
    # Identify current line when stepping
    rcurr = re.compile(
        r'''
        ^>\s        # Beginning of line is '> '
        ([^(]*?)    # Match up to parentheses for dir/filename
        \((.*?)\)   # Get text in parentheses for line number
        ([^\n]*)    # Get text up to newline for function name
        (\n.*)$     # String to end of line for current line
        ''',
        re.M | re.X,
    )
    # Identify a (simple) return
    rret = re.compile(r"--Return--")
    # Regular expression decorator
    rd = RegexpDecorate()
    rd.register(rret, Color("viol"))
class DPdb(Pdb):
    if 1:  # Overridden Pdb methods
        def message(self, msg):
            if dbg:  # Print line for debugging
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
                    t.print(f"{t.ret}{msg}")
                    #   The following line is what has been giving the
                    #   'C⁸(163,  65, 255)--Return--' message in the
                    #   debugger, so I've just commented it out.
                    #rd(msg, insert_nl=True)
                    return
            except TypeError:
                # This exception will occur when the 'whatis' command
                # returns a type and re.match expects a string or bytes
                pass
            # Nothing special found, so print line as normal
            print(f"{msg}")
        def error(self, msg):
            print(f"{t.error}", end="")
            t.print("***", msg, file=self.stdout)
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
            numlines = 20  # DP
            half = numlines // 2  # DP
            self.lastcmd = "list"
            last = None
            if arg and arg != ".":
                try:
                    if "," in arg:
                        first, last = arg.split(",")
                        first = int(first.strip())
                        last = int(last.strip())
                        if last < first:
                            # assume it's a count
                            last = first + last
                    else:
                        first = int(arg.strip())
                        # first = max(1, first - 5)
                        first = max(1, first - half)  # DP
                except ValueError:
                    self.error("Error in argument: %r" % arg)
                    return
            elif self.lineno is None or arg == ".":
                # first = max(1, self.curframe.f_lineno - 5)
                first = max(1, self.curframe.f_lineno - half)  # DP
            else:
                first = self.lineno + 1
            if last is None:
                # last = first + 10
                last = first + numlines  # DP
            filename = self.curframe.f_code.co_filename
            breaklist = self.get_file_breaks(filename)
            try:
                lines = linecache.getlines(filename, self.curframe.f_globals)
                self._print_lines(
                    lines[first - 1 : last], first, breaklist, self.curframe
                )
                self.lineno = min(last, len(lines))
                if len(lines) < last:
                    self.message("[EOF]")
            except KeyboardInterrupt:
                pass
        do_l = do_list
        def do_interact(self, arg):
            ns = self.curframe.f_globals.copy()
            ns.update(self.curframe_locals)
            if color_choice == NoColors:
                code.interact(f"*Interactive*", local=ns)
            else:
                # Leave interactive code in the brnl foreground color,
                # which alerts you that you're in the REPL
                code.interact(f"{t.interactive}*Interactive*{t.n}{t('lill')}", local=ns)
            # Go back to standard screen colors
            print(f"{t.n}", end="")
    if 1:  # New helper methods
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
        def Decorate(self, name, val, t, w):
            "Print name and value in indicated color"
            c = ""
            is_str = False
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
                is_str = True
            elif ii(val, bytes):
                c = t.bytes
            elif ii(val, bytearray):
                c = t.bytearray
            if is_str:
                # Strings get shown by repr()
                print(f"  {c}{name:{w}s} = {val!r}{t.N}")
            else:
                print(f"  {c}{name:{w}s} = {val}{t.N}")
        def get_frame_of_interest(self):
            '''Return the stack frame that's current in the thing being
            debugged.
            '''
            # Get the stack.  Note that st will be a list of FrameInfo
            # objects.
            st = inspect.stack()
            if 0:
                # Print the stack to see what's going on.  This will show
                # that the first occurrence of a bdb.py frame near the
                # bottom of the stack is just above the frame of interest.
                print("Stack:")
                for i in st:
                    print(f"  {i.filename}:{i.lineno} {i.function}")
                exit()
            if 1:  # Get the stack frame of interest
                # Find the stack frame of interest.  Do this by popping items
                # until we see a frame from bdb.py with the function
                # 'trace_dispatch'.  Then the next frame is the one we're
                # interested in.
                #
                # The following loop positions the variable fi on the FrameInfo
                # object of interest
                fi, curr, nolocals = st.pop(), st.pop(), False
                while curr.function != "trace_dispatch":
                    fi = curr
                    if st:
                        curr = st.pop()
                    else:
                        nolocals = True
                        break
                if nolocals:
                    print("No locals (probably had an exception)")
                    return None
                fr = fi.frame  # Stack frame
                return fr
    if 1:  # New debugger commands
        def do_clr(self, var):  # Set colorizing state
            "Set colorizing:  0 = None, 1 = line number, 2 = all"
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
        def do_cls(self, arg):  # Clear the screen
            "Clear the screen"
            print("\x1b[H\x1b[2J\x1b[3J")
        def do_o(self, arg):  # Dump local variables
            "Dump local variables (extra arg shows color key)"
            if 1:  # Define our own colors
                t = Trm()
                c = color_choice != NoColors
                t.title = t("whtl") if c else ""
                t.bool = t("pnkl") if c else ""
                t.float = t("brnl") if c else ""
                t.flt = t("redl") if c else ""
                t.cpx = t("viol") if c else ""
                t.int = t("magl") if c else ""
                t.Decimal = t("trq") if c else ""
                t.string = t("sky") if c else ""
                t.bytes = t("ornl") if c else ""
                t.bytearray = t("lwnl") if c else ""
                t.N = t.n if c else ""
            if 1:  # Get local variables
                fr = self.get_frame_of_interest()
                di = fr.f_locals  # Local variable dictionary
                if not di:
                    print("No local variables in this frame")
                    return
            if 1:  # Print the local variable dictionary
                print(f"{t.title}Local variables (extra arg for color key):{t.N}")
                # Get length of longest name
                w = max(len(i) for i in di)
                # Print the variables
                for name in sorted(di):
                    self.Decorate(name, di[name], t, w)
                breakpoint()
                # Print a key
                if arg and c:
                    t.print(f"Color coding:  ", end="")
                    print(
                        f"{t.int}int{t.N} "
                        f"{t.float}float{t.N} "
                        f"{t.flt}flt{t.N} "
                        f"{t.cpx}cpx{t.N} "
                        f"{t.Decimal}Decimal{t.N} "
                        f"{t.string}str{t.N} "
                        f"{t.bool}bool{t.N} "
                        f"{t.bytes}bytes{t.N} "
                        f"{t.bytearray}bytearray{t.N} "
                    )
        def do_dr(self, arg):  # Nicely print dir(arg)
            "Print the results of dir(obj) for objects in argument"
            if not arg:
                print("Need an argument")
                return
            fr = self.get_frame_of_interest()
            # Get locals and globals
            di = fr.f_locals  # Local variable dictionary
            args = arg.split()
            def Pr(s):
                "Print item of interest s if in locals or globals"
                if s in di:
                    obj = di[s]
                elif s in globals():
                    obj = globals()[s]
                else:
                    print(f"'{s}' not found")
                    return
                print(f"{s} ({type(obj)})")  # Show object's name and type
                for i in Columnize(dir(obj), indent="  "):
                    print(i)
            for i in args:
                Pr(i)
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
        raise ValueError(
            "A valid traceback must be passed if no exception is being handled"
        )
    p = DPdb()
    p.reset()
    p.interaction(None, t)
def pm():
    post_mortem(sys.last_traceback)
