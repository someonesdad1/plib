'''
        
This module extends the python debugger pdb.py Features:

    - Added commands
        - o, O      Dump local variables
        - dr obj    Prints dir() output in columns
        - cls       Clears the screen
        - clr       Set the colorizing state
        - aliases (in ~/.pdbrc)
            - tb = tbreak
            - pi = print instance variables
            - ps = print instance variables of self

    - Changed the 'list' command to output more lines.
    - Colorize certain strings to make them easier to spot:
        - The current line in a list command
        - The file and line number in the current line
        - Error messages
        - Entering the REPL
    - LocateSymbol() finds symbols in import libraries
        
    To use this module to debug my code, I set the environment variable PYTHONBREAKPOINT
    to 'dpdb.set_trace' and insert 'breakpoint()' where I want to drop into the debugger
    (this is available in python 3.7 and later).
    
    To avoid having to go too deep in the pdb/bdb code, I chose to use regular
    expressions to find the lines I wanted to colorize in the Pdb.message() method, so I
    overrode it with the definition here.  There may be some corner cases where it
    doesn't work right yet.
    
    Tips on the python debugger (pdb.py)
        - You can provide command aliases in a ~/.pdbrc or ./.pdbrc file.  For example,
          I alias 'interactive' to 'i'.  Use 'alias' command to see your defined
          aliases.
        - You can edit the pdb.py file to add commands.
            - Example:  I use tbreak a lot so I added 'do_tb = do_tbreak'.
            - Caution:  it's easy to go hog-wild adding new stuff.  You're then creating
              a mental dependency and you'll suffer if you have to debug on another
              system that doesn't have your added stuff.  You then have an update
              problem when you go to a new python version.  That's why I try to make my
              changes in this file.

'''
if 1:  # Header
    if 1:  # Standard imports
        import code
        import decimal
        import fractions
        import inspect
        import linecache
        import os
        import pathlib
        import pdb
        import re
        import sys
    if 1:   # Custom modules
        import columnize
        import dpstr
        import dptypes
        import f
        import trm
        import wrap
    if 1:   # Global variables
        yy = pdb.set_trace  # Handy when this file is broken
        u = trm.TrmDP()
    if 1:   # Core file gist information
        __gist__      = "DP's debugger additions"
        __copyright__ = "Copyright © 2023 Don Peterson"
        __license__   = "MIT License (see /plib/_lic.mit)"
        __test__      = "notest"
        __history__   = '''Important dates of changes'''
        __category__  = "util"
        __todo__      = r'''

        - If a debugger command starts with '^\s*#', it should be considered a comment
          and ignored.  This is helpful to type notes when using the script command to
          capture all the output.
        - When debugging, the return value string gets truncated with '...'.  This can
          be a pain when e.g. the return value is a ufloat, as you can't see the value.
          Make it use up the available screen width or see if a debugger option can be used to
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

        '''
    if 1:  # Functions to set up colorizing strings
        def All():
            "Fancier set of colors"
            u.current_line  = u.sky
            u.directory     = u.gryl
            u.filename      = u.orn
            u.linenum       = u.ygr
            u.function      = u.pnkl
            u.error         = u.red
            u.ret           = u.yel
            u.interactive   = u.ygr
        def LineNumOnly():
            "Minimal set of colors"
            u.current_line  = u.sky
            u.directory     = u.gryl
            u.filename      = u.wht
            u.linenum       = u.ygr
            u.function      = u.wht
            u.error         = u.red
            u.ret           = u.yel
            u.interactive   = u.ygr
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
        g = dptypes.Constant()
        # Set to True to see each line's repr() string
        g.dbg = 0
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
    rd = dpstr.RegexpDecorate()
    rd.register(rret, u.vio)
if 1:  # Classes
    class DPdb(pdb.Pdb):
        if 1:  # Overridden Pdb methods
            def message(self, msg):
                if g.dbg:  # Print line for debugging
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
                
                List source code for the current file.  Without arguments, list 11 lines
                around the current line or continue the previous listing.  With . as
                argument, list 11 lines around the current line.  With one argument,
                list 11 lines starting at that line.  With two arguments, list the given
                range; if the second argument is less than the first, it is a count.
                
                The current line in the current frame is indicated by "->".  If an
                exception is being debugged, the line where the exception was originally
                raised or propagated is indicated by ">>", if it differs from the
                current line.

                '''
                numlines = 20           # DP
                half = numlines // 2    # DP
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
                            first = max(1, first - numlines)  # DP
                    except ValueError:
                        self.error(f"Error in argument: {arg!r}")
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
                    self._print_lines(lines[first - 1 : last], first, breaklist, self.curframe)
                    self.lineno = min(last, len(lines))
                    if len(lines) < last:
                        self.message("[EOF]")
                except KeyboardInterrupt:
                    pass
            do_l = do_list
            def do_repl(self, arg):
                'Enter a REPL; press ctrl-D to return to debugger'
                ns = self.curframe.f_globals.copy()
                ns.update(self.curframe_locals)
                i = "---- Interactive ---- (^D back to debugger)"
                if color_choice == NoColors:
                    code.interact(f"{i}", local=ns)
                else:
                    code.interact(f"{u.interactive}{i}{u.n}{u('whtl')}", local=ns)
                # Go back to standard screen colors
                print(f"{u.n}", end="")
            do_interact = do_repl
            def do_run(self, arg):
                '''Restart the program.  
                The default run/restart in pdb raises an exception and thus don't work.
                This command works, but your breakpoints and other information are not
                restored.
                '''
                if 1:
                    raise pdb.Restart
                else:
                    # The built-in command to the debugger usually has an exception; this
                    # method seems to work OK.
                    # From https://bobbyhadz.com/blog/how-to-restart-python-script-from-within-itself#how-to-restart-a-python-script
                    u.print(f"{u.pnk}Restarting session")
                    os.execv(sys.executable, ['python'] + sys.argv)
            do_restart = do_run
            def do_t(self, arg):
                'Quick tutorial'
                print(wrap.dedent(f'''
                Post-mortem debugging:  Use pdb.post_mortem() to view program state after an exception.

                display expression:  Show the expression if it changed each time execution stops
                    in the current frame.  The old and new values are shown.
                '''))
            def do_H(self, arg):
                self.do_h("all")
            def do_h(self, arg):
                '''Annotated help (use 'all' to see details)'''
                if not arg or arg == "h":
                    # Print my customized list of commands
                    self.my_help_listing(arg)
                elif arg == "all":
                    self.my_help_listing("all")
                elif arg == "!":
                    super().do_h("exec")
                else:
                    super().do_h(arg)
        if 1:  # New helper methods
            def my_help_listing(self, arg):
                'My help listing'
                if arg == "h":
                    super().do_h(arg)
                else:
                    u.bp = u.denl
                    u.up = u.lip
                    u.w = u.orn
                    u.s = u.sea
                    u.disp = u.pnkl
                    builtin_cmds = [
                        ["", "alias",  "Define an alias"],
                        ["", "a(rgs)",  "Args of current function"],
                        [u.bp, "b(reak)", "List/define breakpoints"],
                        [u.w, "bt",      "Backtrace"],
                        ["", "c(ontinue)",  "Continue execution"],
                        [u.bp, "cl(ear)", "Clear breakpoints"],
                        [u.bp, "commands",    "Specify commands for bp; end with 'end'"],
                        [u.bp, "condition",   "Set a condition for a bp"],
                        [u.up, "d(own)",  "Move down the stack"],
                        ["", "debug",   "Recursive debugger"],
                        [u.bp, "disable", "Disable bp"],
                        [u.disp, "display", "Display an expression at each stop"],
                        [u.bp, "enable",  "Enable a bp"],
                        ["", "q(uit)",  "Exit the debugger"],
                        [u.bp, "ignore",  "Ignore a bp"],
                        ["", "j(ump)",  "Set next line to be executed"],
                        ["", "l(ist)",  "Show code"],
                        ["", "ll",      "Longlist"],
                        [u.s, "n(ext)",  "Step over"],
                        ["", "r(eturn)",    "Continue until function return"],
                        ["", "repl",    "Start a REPL"],
                        ["", "run", "Restart program (also restart)"],
                        ["", "retval",  "Last return value of a function (also rv)"],
                        [u.s, "s(tep)",  "Step into"],
                        ["", "source",  "Show source code for expressions"],
                        [u.bp, "tbreak",  "Set temporary bp"],
                        [u.up, "u(p)",    "Move up stack frame"],
                        ["", "unalias", "Remove alias"],
                        [u.disp, "undisplay",   "Remove named expression or all"],
                        ["", "unt(il)", "Continue until line number > current reached"],
                        ["", "whatis",  "Print type of arg"],
                        [u.w, "w(here)", "Backtrace"],
                    ]
                    if arg == "all":
                        for clr, abbr, descr in builtin_cmds:
                            print(f"  {clr}{abbr:10s}{u.n} {descr}")
                    else:
                        built = []
                        for clr, abbr, descr in builtin_cmds:
                            built.append(clr + abbr + u.n)
                        for i in columnize.Columnize(built):
                            print(i)


            def current_stopped_line(self, file, linenum, func, remainder):
                print("> ", end="")
                # Only colorize the file name portion
                p = pathlib.Path(file)
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
                if isinstance(val, bool):
                    c = u.bool
                elif isinstance(val, int):
                    c = u.int
                elif isinstance(val, f.flt):
                    c = u.flt
                elif isinstance(val, f.cpx):
                    c = u.cpx
                elif isinstance(val, float):
                    c = u.float
                elif isinstance(val, decimal.Decimal):
                    c = u.Decimal
                elif isinstance(val, fractions.Fraction):
                    c = u.Fraction
                elif isinstance(val, str):
                    c = u.string
                    is_str = True
                elif isinstance(val, bytes):
                    c = u.bytes
                elif isinstance(val, bytearray):
                    c = u.bytearray
                elif isinstance(val, list):
                    c = u.list
                elif isinstance(val, tuple):
                    c = u.tuple
                elif val is None:
                    c = u.none
                # Print the color coding
                show_all = False    # If True, color the whole line
                try:
                    if is_str: # Strings get shown by repr()
                        if show_all:
                            print(f"  {c}{name:{w}s} = {val!r}{u.n}")
                        else:
                            print(f"  {name:{w}s} = {c}{val!r}{u.n}")
                    else:
                        if show_all:
                            print(f"  {c}{name:{w}s} = {val}{u.n}")
                        else:
                            print(f"  {name:{w}s} = {c}{val}{u.n}")
                except Exception as e:
                    print(f"  {name} had exception: {e}")
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
            def define_colors(self):
                bg = "gry1"
                c = color_choice != NoColors
                u.title = u.wht
                u.bool = u.lipl
                u.float = u("ygr", bg)
                u.flt = u("red", bg)
                u.cpx = u("cyn", bg)
                u.int = u("mag", bg)
                u.Decimal = u("yonl", bg)
                u.Fraction = u("brn", bg)
                u.string = u.lwn
                u.bytes = u.orn
                u.bytearray = u.olv
                u.lst = u.yel
                u.tuple = u.den
                u.none = u.gry
                u.n = u.n
                if color_choice == NoColors:
                    u.on = False
                return c
            def do_O(self, arg):  # Dump local variables with key
                'Dump local variables with color key'
                c = self.define_colors()
                if 1:  # Get local variables
                    fr = self.get_frame_of_interest()
                    di = fr.f_locals  # Local variable dictionary
                    if not di:
                        print("No local variables in this frame")
                        return
                if 1:  # Print the local variable dictionary
                    print(f"{u.title}Local variables:{u.n}")
                    # Get length of longest name
                    w = max(len(i) for i in di)
                    # Print the variables
                    for name in sorted(di):
                        self.Decorate(name, di[name], u, w)
                    # Print a key
                    if c:
                        print(
                            f"{u.int}int{u.n} "
                            f"{u.float}float{u.n} "
                            f"{u.flt}f.flt{u.n} "
                            f"{u.cpx}f.cpx{u.n} "
                            f"{u.Decimal}Decimal{u.n} "
                            f"{u.Fraction}Fraction{u.n} "
                            "    "
                            f"{u.lst}list{u.n} "
                            f"{u.tuple}tuple{u.n} "
                            f"{u.none}None{u.n} "
                            f"{u.string}str{u.n} "
                            f"{u.bool}bool{u.n} "
                            f"{u.bytes}bytes{u.n} "
                            f"{u.bytearray}bytearray{u.n} "
                        )
                        print("Use dpdb.LocateSymbol(symbol) to find a symbol in import libraries")
            def do_o(self, arg):  # Dump local variables
                'Dump local variables'
                c = self.define_colors()
                if 1:  # Get local variables
                    fr = self.get_frame_of_interest()
                    di = fr.f_locals  # Local variable dictionary
                    if not di:
                        print("No local variables in this frame")
                        return
                if 1:  # Print the local variable dictionary
                    print(f"{u.title}Local variables:{u.n}")
                    # Get length of longest name
                    w = max(len(i) for i in di)
                    # Print the variables
                    for name in sorted(di):
                        self.Decorate(name, di[name], u, w)
            if 0:
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
                        for i in columnize.Columnize(dir(obj), indent="  "):
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
if 1:  # Find symbols
    def LocateSymbol(symbol):
        'Return list of modules that contain symbol'
        for name, module in sys.modules.items():
            if hasattr(module, '__file__') and module.__file__:
                try:
                    with open(module.__file__, errors='ignore') as f:
                        if symbol in f.read():
                            print(f"Found {symbol!r} in: {name} ({module.__file__})")
                except Exception:
                    pass
