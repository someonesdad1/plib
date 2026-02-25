'''
        
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
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Python debugger extensions oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2023 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞ 
        
            - When debugging, the return value string gets truncated with '...'.  This
              can be a pain when e.g. the return value is a ufloat, as you can't see the
              value.  Make it use up the available width or see if a debugger option can
              be used to let you see the whole string.
            - Add a command to change the number of lines displayed
            - po command:
                - Columnize dir() output.  First arg is object to dir, remaining args
                  are regexps to search for.
            - See if r vs s behavior can be changed or toggled
            - inspect has a number of functions that could be useful for a command
              that's used to inspect an object:  it's source, docs, etc.  Call the
              built-in pager to do this.
            - Use a traceback to print the call stack on an exception.
        
        oo>
    '''
    if 1:  # Standard imports
        import decimal
        import fractions
        import pathlib
        import pdb
        import code
        import inspect
        import linecache
        import re
        import sys
    if 1:   # Custom modules
        import dpstr
        import columnize
        import f
        import trm
    if 1:   # Import symbols
        Decimal = decimal.Decimal
        Fraction = fractions.Fraction
        Path = pathlib.Path
        Pdb = pdb.Pdb
        # 
        RegexpDecorate = dpstr.RegexpDecorate
        Columnize = columnize.Columnize
        flt = f.flt
        cpx = f.cpx
        u = trm.Trm(default=2)
    if 1:  # Functions to set up colorizing strings
        def All():
            "Fancier set of colors"
            u.current_line  = u.cyn
            u.directory     = u.gry
            u.filename      = u.trq
            u.linenum       = u.orn
            u.function      = u.lav
            u.error         = u.red
            u.ret           = u.vio
            u.interactive   = u("blk", "yel")
        def LineNumOnly():
            "Minimal set of colors"
            u.current_line  = u.cyn
            u.directory     = u.gry
            u.filename      = u.wht
            u.linenum       = u.orn
            u.function      = u.wht
            u.error         = u.red
            u.ret           = u.vio
            u.interactive   = u("blk", "yel")
        def NoColors():
            u.current_line  = ""
            u.directory     = ""
            u.filename      = ""
            u.linenum       = ""
            u.function      = ""
            u.error         = ""
            u.ret           = ""
            u.interactive   = ""
    if 1:  # Global variables
        color_choice = All
        color_choice()
        # Set to True to see each line's repr() string
        dbg = 0
        ii = isinstance
if 1:  # Regular expressions
    # Identify current line in list command.  'B' can be in the string if the line is a
    # breakpoint.  Pdb.do_list() indicates '>>' can be used to indicate a line where an
    # exception was raised if it differs from the current line.
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
    rd.register(rret, u.vio)
if 1:  # Classes
    class DPdb(Pdb):
        if 1:  # Overridden Pdb methods
            def message(self, msg):
                if dbg:  # Print line for debugging
                    u.print(f"{u('brnl')}{msg!r}")
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
                        u.print(f"{u.ret}{msg}")
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
                print(f"{u.error}", end="")
                u.print("***", msg, file=self.stdout)
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
                    code.interact("*Interactive*", local=ns)
                else:
                    # Leave interactive code in the brnl foreground color,
                    # which alerts you that you're in the REPL
                    code.interact(f"{u.interactive}*Interactive*{u.n}{u('lill')}", local=ns)
                # Go back to standard screen colors
                print(f"{u.n}", end="")
        if 1:  # New helper methods
            def current_stopped_line(self, file, linenum, func, remainder):
                print("> ", end="")
                # Only colorize the file name portion
                p = Path(file)
                print(f"{u.directory}{p.parent}/", end="")
                print(f"{u.filename}{p.name}{u.n} ", end="")
                print(f"{u.linenum}{linenum}{u.n} ", end="")
                print(f"{u.function}{func}{u.n}", end="")
                print(f"{remainder}")
            def current_listing_line(self, linenum, remainder):
                print(f"{u.linenum}{linenum}", end="")
                u.print(f"{u.current_line}{remainder}")
            def Decorate(self, name, val, u, w):
                "Print name and value in indicated color"
                c = ""
                is_str = False
                if ii(val, bool):
                    c = u.bool
                elif ii(val, int):
                    c = u.int
                elif ii(val, flt):
                    c = u.flt
                elif ii(val, cpx):
                    c = u.cpx
                elif ii(val, float):
                    c = u.float
                elif ii(val, Decimal):
                    c = u.Decimal
                elif ii(val, Fraction):
                    c = u.Fraction
                elif ii(val, str):
                    c = u.string
                    is_str = True
                elif ii(val, bytes):
                    c = u.bytes
                elif ii(val, bytearray):
                    c = u.bytearray
                elif ii(val, list):
                    c = u.list
                elif ii(val, tuple):
                    c = u.tuple
                elif val is None:
                    c = u.none
                # Print the color coding
                show_all = False    # If True, color the whole line
                if is_str: # Strings get shown by repr()
                    if show_all:
                        print(f"  {c}{name:{w}s} = {val!r}{u.N}")
                    else:
                        print(f"  {name:{w}s} = {c}{val!r}{u.N}")
                else:
                    if show_all:
                        print(f"  {c}{name:{w}s} = {val}{u.N}")
                    else:
                        print(f"  {name:{w}s} = {c}{val}{u.N}")
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
            def do_cls(self, arg):  # Clear the screen
                "Clear the screen"
                print("\x1b[H\x1b[2J\x1b[3J")
            def do_o(self, arg):  # Dump local variables
                'Dump local variables with color key (arg ignored)'
                if 1:  # Define our own colors
                    c = color_choice != NoColors
                    u.title = u.wht if c else ""
                    u.bool = u.pnk if c else ""
                    u.float = u.grn if c else ""
                    u.flt = u.red if c else ""
                    u.cpx = u.vio if c else ""
                    u.int = u.mag if c else ""
                    u.Decimal = u.trq if c else ""
                    u.Fraction = u.brn if c else ""
                    u.string = u.cyn if c else ""
                    u.bytes = u.orn if c else ""
                    u.bytearray = u.lwn if c else ""
                    u.list = u.roy if c else ""
                    u.tuple = u.lav if c else ""
                    u.none = u.gry if c else ""
                    u.N = u.n if c else ""
                if 1:  # Get local variables
                    fr = self.get_frame_of_interest()
                    di = fr.f_locals  # Local variable dictionary
                    if not di:
                        print("No local variables in this frame")
                        return
                if 1:  # Print the local variable dictionary
                    print(f"{u.title}Local variables:{u.N}")
                    # Get length of longest name
                    w = max(len(i) for i in di)
                    # Print the variables
                    for name in sorted(di):
                        self.Decorate(name, di[name], u, w)
                    breakpoint()
                    # Print a key
                    if c:
                        print(
                            f"{u.int}int{u.N} "
                            f"{u.float}float{u.N} "
                            f"{u.flt}flt{u.N} "
                            f"{u.cpx}cpx{u.N} "
                            f"{u.Decimal}Decimal{u.N} "
                            f"{u.Fraction}Fraction{u.N} "
                            "    "
                            f"{u.list}list{u.N} "
                            f"{u.tuple}tuple{u.N} "
                            f"{u.none}None{u.N} "
                            f"{u.string}str{u.N} "
                            f"{u.bool}bool{u.N} "
                            f"{u.bytes}bytes{u.N} "
                            f"{u.bytearray}bytearray{u.N} "
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
if 1:  # Core functionality
    def set_trace(*, header=None):
        pdb = DPdb()
        if header is not None:
            pdb.message(header)
        pdb.set_trace(sys._getframe().f_back)
    # The following two functions are needed by debug.py to let DPdb be used
    # by debug.TraceInfo().
    def post_mortem(tb=None):
        'Handle the traceback tb'
        # Handling the default
        if tb is None:
            # sys.exc_info() returns (type, value, traceback) if an exception is
            # being handled, otherwise it returns None
            tb = sys.exc_info()[2]
        if tb is None:
            raise ValueError("A valid traceback must be passed if no exception is being handled")
        p = DPdb()
        p.reset()
        p.interaction(None, tb)
    def pm():
        post_mortem(sys.last_traceback)
