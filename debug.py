'''
Debugging tools

    Turning on debugging
        - Set debug.show to True   OR
        - Set the environment variable Debug to a nonempty string
    Turning on Tracing
        - Set debug.Trace.show to True   OR
        - Set the environment variable Trace to a nonempty string
    
    The following functions/class work regardless of debug.show
        fln()
            File & line number string
        filelinenum()
            (file, line_number)
        DumpStack()
            Print a colorized version of the stack to a stream
        AutoIndent object
            Printed messages to a stream are indented according to stack level
        SetDebugger
            Execute to go to debugger on unhandled exception
        DumpException
            Gives more exception information than a normal backtrace

    Function decorators
        class Trace
            Function decorator to print entry/exit of function calls.  Turn on and off
            with Trace.show.
        ShowFunctionCall
            Function decorator to show call & return (logs to the file debug.log by
            default, but you can make it stdout).  You need to set
            debug.g.enable_tracing to True for this to work.
        DumpArgs1
            Prints a function's arguments when it is called
        DumpArgs2
            Similar to DumpArgs1 but you can control which functions are decorated
            at runtime
        Memoize
            Caches function calls in a dictionary
        TraceExecution  
            Show execution of each line of a function
        Passify         
            Disables a function and makes it return None
        IgnoreDeprecationWarnings
            Ignore deprecation warnings in a function
        
    The following only work when debug.show is True
        watch(variable)
            Print file:linenum with value/type of a variable
        trace(message)
            Print file:linenum with the message.
    To turn these off, run python with the -O option or set debug.show to False.
    
    References:
        A. Martelli and D. Ascher, ed., "Python Cookbook", O'Reilly, 2002.
        D. Beazley, "Python Essential Reference", 4th ed. (Kindle version)
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2009, 2014 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞ 
        
            - ∞∞3 Can stack levels be numbered?  Not a big priority, as dot example
              doesn't pretty well
  
        oo>
    '''
    if 1:   # Standard imports
        from collections import deque
        from inspect import stack
        from pathlib import Path
        import bdb
        import functools
        import linecache
        import os
        import pdb
        import re
        import sys
        import traceback as TB
        import warnings
    if 1:   # Custom imports
        from color import Color, Trm, t
        from constant import Constant
        from wrap import dedent
        import dpdb
    if 1:   # Global variables
        g = Constant()      # Class instance to hold global variables
        g.strict = False    # Note these aren't readonly variables
        # dash_O_on = True  ==> Use python -O to turn debugging on
        # dash_O_on = False ==> Use python -O to turn debugging off
        g.dash_O_on = False
        # Set this to the name of a file to log function calls to a file with the help
        # of the ShowFunctionCall decorator
        g.enable_tracing = ""
        if g.enable_tracing:
            g.debug_log = open(g.enable_tracing, "wb")
        g.noexit = False    # Switch for TraceExecution
if 1:   # Set key global variables based on environment variables
    g.W = int(os.environ.get("COLUMNS", "80")) - 1
    # Global variables to control debugging and tracing
    if 1:   # show causes debugging output if True
        show = 0
        if "Debug" in os.environ:   # True if nonzero integer
            s = os.environ.get("Debug", "0")
            try:
                value = int(s)
            except Exception:
                value = 0
            show = value
            del s
    if 1:   # Trace causes the class variable Trace.on set to True
        g.trace_on = 0
        if "Trace" in os.environ:   # True if nonzero integer
            s = os.environ.get("Trace", "0")
            try:
                value = int(s)
            except Exception:
                value = 0
            g.trace_on = value
            del s
if 1:   # Classes
    class Trace:
        '''Function decorator to print the entry and exit of function calls
        to a stream.  Each nested call results in indentation to help you
        visually see where in the call stack you are.  If Trace.show is
        False, there should be little extra overhead from this decorator,
        so you may want to leave it in production code.
        
        You may want to set your calling code up so that Trace.show is set to
        True if e.g. a particular environment variable is set or your
        program receives a software signal.
        
        Example of use:
        
            @Trace
            def MyFunction():
        '''
        increment = 2  # Increment for indenting
        # How many spaces to indent.  It's the negative of the increment so it
        # starts at 0.
        indent = -increment
        stream = sys.stdout  # Stream that receives the printed output
        show = g.trace_on  # Set to True to get tracing output
        prefix = "+ "
        def __init__(self, func):
            self.func = func
            try:
                self.name = func.func_name
            except AttributeError:
                self.name = func.__name__
        def __call__(self, *p, **kw):
            if Trace.show:
                Trace.indent += Trace.increment
                ind, f, prefix = " " * Trace.indent, self.name, Trace.prefix
                s = ["{prefix}{ind}Entering {f}(".format(**locals())]
                c = ", " if kw else ""
                if p:
                    s.append("args={p}{c}".format(**locals()))
                if kw:
                    s.append("kw={kw}".format(**locals()))
                s.append(")")
                print("".join(s), file=Trace.stream)
                retval = self.func(*p, **kw)
                print(
                    "{prefix}{ind}Exiting {f}:  returned {retval}".format(**locals()),
                    file=Trace.stream,
                )
                Trace.indent -= Trace.increment
                return retval
            else:
                return self.func(*p, **kw)
    class AutoIndent(object):
        '''Indent debug output based on function call depth.  Adapted from code by
        Lonnie Princehouse (submitted 26 Apr 2005) at
        http://code.activestate.com/recipes/411791
        
        Usage example:
            with AutoIndent():
                Execute code you want to watch
        
        which sends the printed messages through the AutoIndent object to
        be indented based on the stack depth.  Run this file as a script to see
        the example.
        '''
        def __init__(self, stream=sys.stdout, indent=4, ansi=False):
            '''stream is where you want the information to be sent.
            indent is either the number of spaces or a string to use for
            each indent level.  If ansi is True, then handle incoming
            strings with ANSI escape sequences for color specially.
            
            A handy value for indent is e.g. '|   ', as the vertical bar
            symbols will help you line up the indent levels.  This can be
            helpful for deeply-nested programs.
            '''
            self.stream = stream
            self.depth = len(stack())
            self.indent = " " * indent if isinstance(indent, int) else indent
            self.ansi = False
            if ansi:
                # Regular expression to recognize ANSI escape sequences
                # used for changing colors.
                self.ansi = re.compile(r"\x1b\[\d+(;\d+)*m")
        def _indent_level(self):
            return max(0, len(stack()) - self.depth - 2)
        def print(self, *args, **kw):
            'Send to plain stdout for debugging'
            t.print(*args, **kw, file=sys.__stdout__)
        def write(self, data):
            # Note we intercept ANSI escape codes when data is a string
            # and send them on unindented.
            if isinstance(data, str) and self.ansi:
                mo = self.ansi.search(data)
                if mo:
                    self.stream.write(data)
                    return
            indentation = self.indent * self._indent_level()
            def f(x):
                return indentation + x if x else x
            s = "\n".join([f(line) for line in data.split("\n")])
            self.stream.write(s)
        def flush(self):
            self.stream.flush()
        def __enter__(self):
            # Hook up the plumbing to make our instance the substitute for stdout
            self.stdout = sys.stdout
            sys.stdout = self
        def __exit__(self, exc_type, exc_val, exc_tb):
            # Reconnect the old plumbing
            sys.stdout = self.stdout
            return False if exc_type is None else True
if 1:   # Core functionality
    def watch(variables, color=None, stream=sys.stdout):
        '''Watch a variable; variables must be a sequence of variable names.
        Example:
            def test1():
                x = 17
                watch(x)
            test1()
        will print e.g.
            debug.py[384] in test1:  x <int> = 17
        Keywords:
            color  = None, a string that either names a color or is an ANSI escape
                     string, or a Color instance.
            stream = stream to print the information to
            
        See http://code.activestate.com/recipes/52314; also
        pg 427 of Python Cookbook.
        '''
        assert color is None or isinstance(color, str) or isinstance(color, Color)
        assert hasattr(stream, "write")
        def GetVariableNames(s):
            '''s is a string of the form 'watch([x, y], color=c)'.
            Extract the names of the nonkeyword parameters and return as a
            list of strings.
            
            Some possible forms of s are
                'watch((x,))'
                'watch((x,), color="abc")'
                'watch([x,])'
                'watch([x,], color="abc")'
                'watch((x, y))'
                'watch((x, y), color="abc")'
                'watch([x, y])'
                'watch([x, y], color="abc")'
            The first four forms need to return ("x",) or ["x"]; the second
            four need to return ("x", "y") or ["x", "y"].
            '''
            # Remove 'watch(' and trailing ')'
            u = s[6:-1]
            # Get rid of 'color' part
            if "=" in u:
                u = u.split("=")[0].rstrip()
                assert u.endswith("color")
                u = u[:-5].rstrip()
                assert u[-1] == ","
                u = u[:-1]
            u = u.strip()
            # Now u is the string of a tuple or list.  Remove the first and
            # last characters and we have a comma-separated list of variable
            # names.
            u = u[1:-1]
            v = [i.strip() for i in u.split(",") if i.strip()]
            return v
        if show and ((__debug__ and not g.dash_O_on) or (not __debug__ and g.dash_O_on)):
            fn, ln, method, call = TB.extract_stack()[-2:][0]
            names = GetVariableNames(call)
            if stream == sys.stdout and color is not None:
                if isinstance(color, str):
                    # It's a color name or hex string or an ANSI escape sequence
                    if "\x1b" in color:
                        print(color, end="")
                    else:
                        print(t(color), end="")
                elif isinstance(color, Color):
                    print(f"{t(color)}", end="")
                else:
                    raise TypeError(f"'{color}' is not a string or Color instance")
            for name, value in zip(names, variables):
                vartype = str(type(value))[8:-2]
                value = repr(value)
                s = f"{fn}[{ln}] in {method}:  {name} <{vartype}> = {value}\n"
                stream.write(s)
            if stream == sys.stdout and color is not None:
                print(f"{t.n}", end="")
    def trace(msg, color=None, stream=sys.stdout):
        '''Print a trace message.  You can set the color if the color.py
        module has been loaded.  Example:
            def test1():
                trace("Trace message")
            test1()
        will print e.g.
            debug.py[383] in test1:  Trace message
        '''
        # See http://code.activestate.com/recipes/52314; also
        # pg 427 of Python Cookbook.
        if show and ((__debug__ and not g.dash_O_on) or (not __debug__ and g.dash_O_on)):
            stack = TB.extract_stack()[-2:][0]
            fn, ln, method, call = stack
            fmt = "{fn}[{ln}] in {method}:  {msg}\n"
            if stream == sys.stdout and color is not None:
                print(t(color), end="")
            stream.write(fmt.format(**locals()))
            if stream == sys.stdout and color is not None:
                print(t.n, end="")
    def DumpException(fr_include=None, fr_ignore=None, var_include=None, var_ignore=None,
                      num_levels=0, hl={}, stream=sys.stdout):
        '''Print the traceback information followed by a listing of the
        local variables in each frame.  This function is intended to be
        used in a try/except block to print the details of an unhandled
        exception.  The keyword parameters give control over what is
        printed and how it's displayed.
        
        num_levels
            Controls the number of stack frames to display.  The default
            of 0 means to show all.  1 means to only show the top frame; 2
            means the top frame and second frame, etc.
        fr_include      (list of integers)
            If not None, it must be a sequence of integers; only those
            stack frames will be shown (the innermost frame is 0).
        fr_ignore       (list of integers)
            If not None, any frame number that is a member of that
            sequence will not be shown.
        var_include and var_ignore     (lists of variable names)
            These do similar things for variable names.  If var_include is
            not None, only those variable names are shown.  If var_ignore
            is not None, don't print any names in the container.
        hl
            A dictionary of variable names to highlight; the value is the
            byte representing the foreground and background colors to use
            (see color.py).  It can also be a tuple of the color integers.
            Here are some examples of use  that utilize the same colors
            (see color.py for details):
                import color as c
                hl = {
                    "a" : c.yellow,
                    "b" : (c.yellow, c.black),
                    "c" : 0x0e,
                }
        Examples:
            - To see everything except the first (module-level) frame, use
              e.g. 'include=range(1, 1000)' or 'ignore=[0]'.
            - To see levels 1, 2, and 3 only, use 'include=range(1, 4)'.
            - To see levels 1 and 3 only, use 'include=(1, 3)'.
            - To see any variables named 'alpha' in yellow on black, set
              hl={"alpha" : (Color("yel"), Color("blk"))}.
        '''
        # Derived from Bryn Keller's 7 Mar 2001 post at
        # http://code.activestate.com/recipes/52215.  Also see pg 431 of
        # Python Cookbook.
        #
        # Dump the exception
        if stream == sys.stdout:
            print(f"{t('redl', 'blk')}", end="")
        print("Unhandled exception:", file=stream)
        if stream == sys.stdout:
            print(f"{t.n}", end="")
        for line in TB.format_exc().split("\n"):
            print(" ", line, file=stream)  # Indent the stack trace
        # Get the needed traceback info
        tb = sys.exc_info()[2]
        while True:
            if not tb.tb_next:
                break
            tb = tb.tb_next
        # Dump local variables by getting the stack frames
        frames = []
        f = tb.tb_frame
        while f:
            frames.append(f)
            f = f.f_back
        frames.reverse()
        if fr_include is not None:
            s = str(fr_include).replace("[", "").replace("]", "")
            print("Locals in frames %s, innermost frame = 0" % s, file=stream)
        else:
            print("Locals by frame, innermost last", file=stream)
        # Print a note if not all stack frames are shown
        m1, m2 = "Note:", "  only selected %s are shown"
        if ((  fr_include is not None and len(fr_include))
               or (fr_ignore is not None and len(fr_ignore))
               or num_levels):
            if stream == sys.stdout:
                print(f"{t.redl}", end="")
            print(m1, end="", file=stream)
            if stream == sys.stdout:
                print(f"{t.n}", end="")
            print(m2 % "stack frames", file=stream)
        # Print a note if not all locals are shown
        if ((  var_include is not None and len(var_include))
               or (var_ignore is not None and len(var_ignore))
               or num_levels):
            if stream == sys.stdout:
                print(f"{t.redl}", end="")
            print(m1, end="", file=stream)
            if stream == sys.stdout:
                print(f"{t.n}", end="")
            print(m2 % "local variables", file=stream)
        levels_printed = 0
        for i, frame in enumerate(frames):
            if (  (fr_include is not None and i not in fr_include) or 
                  (fr_ignore is not None and i in fr_ignore)):
                continue
            print("-" * 70, file=stream)
            print("Frame %d %s() in %s at line %s"
                % (i, frame.f_code.co_name, frame.f_code.co_filename, frame.f_lineno),
                file=stream)
            Locals = list(frame.f_locals.items())
            Locals.sort()
            for key, value in Locals:
                if ((  var_include is not None and key not in var_include) or 
                      (var_ignore is not None and key in var_ignore)):
                    continue
                try:  # Catch any new errors
                    print("  ", end="", file=stream)
                    if key in hl:
                        # hl is dict like {'thing': 'yell', 'data': 'blul'}.
                        # Values can also be Color instances.
                        if stream == sys.stdout:
                            c = hl[key]
                            print(f"{t(c)}", end="")
                    # We handle a variable named 'buffer' specially, as it
                    # could contain binary data that hangs a shell window.
                    if key.lower() in ("buf", "buff", "buffer"):
                        s = "<%d bytes (binary?)>" % len(str(value))
                        print("%s = %s" % (key, s), file=stream)
                    elif key == "__doc__":
                        # Print just the first line
                        d = value.strip().split("\n")[0]
                        print("%s = %s ..." % (key, d), file=stream)
                    else:
                        print("%s = %s" % (key, str(value)), file=stream)
                    if stream == sys.stdout:
                        print(f"{t.n}", end="")
                except Exception as e:
                    print("<Error '%s' while printing value for '%s'>" % (str(e), key),
                        file=stream)
            levels_printed += 1
            if num_levels and levels_printed >= num_levels:
                break
    def TraceInfo(type, value, traceback):
        '''Start the debugger after an uncaught exception.  From Thomas
        Heller's post on 22 Jun 2001 http://code.activestate.com/recipes/65287
        Also see page 435 of "Python Cookbook".
        '''
        # Updated first test logic from https://gist.github.com/rctay/3169104
        if (  hasattr(sys, "ps1")
              or not sys.stderr.isatty()
              or not sys.stdout.isatty()
              or not sys.stdin.isatty()
              or issubclass(type, bdb.BdbQuit)
              or issubclass(type, SyntaxError)):
            # You are in interactive mode or don't have a tty-like device,
            # so call the default hook.
            sys.__excepthook__(type, value, traceback)
        else:
            # You are not in interactive mode; print the exception.
            TB.print_exception(type, value, traceback)
            print()
            # Now start the debugger
            try:
                dpdb.pm()
            except Exception:
                pdb.pm()
    def SetDebugger():
        '''If you execute this function, TraceInfo() will be called when
        you get an unhandled exception and you'll be dumped into the
        debugger.
        '''
        sys.excepthook = TraceInfo
    def DumpArgs(func):
        '''Decorator to dump a function's arguments to show how the function
        was called.  From
        http://wiki.python.org/moin/PythonDecoratorLibrary.
        
        Note the global variable must not be None and contain a stream
        for this to work.
        '''
        def echo_func(*p, **kw):
            fc = func.__code__
            fn = func.__name__
            argnames = fc.co_varnames[: fc.co_argcount]
            args = ", ".join(
                "%s=%r" % entry for entry in list(zip(argnames, p)) + list(kw.items())
            )
            print(f"{fn}({args})")
            return func(*p, **kw)
        return echo_func if show else func
    def ShowFunctionCall(func):
        '''This function is a decorator to log function calls to g.debug_log.  You must
        set debug.g.enable_tracing to True for it to work; otherwise there's no overhead.
        '''
        # This decorator is for showing how a function was called and its return value.
        # It comes from Beazley, 4th ed., Ch. 6, section on decorators.  callf is a
        # closure that replaces the original function.
        if g.enable_tracing:
            def callf(*args, **kwargs):
                g.debug_log.write("Calling %s: params=%s, kw=%s\n" % (func.__name__, args, kwargs))
                r = func(*args, **kwargs)
                g.debug_log.write("        %s returned %s\n" % (func.__name__, r))
                return r
            return callf
        else:
            return func
    def fln(brackets=False):
        'Return "file:linenum" from where this function was called'
        f, ln = filelinenum()
        return f"[{f}:{ln}]" if brackets else f"{f}:{ln}"
    def filelinenum():
        'Return (file, linenum) from where this function was called'
        s = TB.extract_stack()[-2:][0]
        return (s[0], s[1]) if __debug__ else tuple()
    def DumpStack(stream=sys.stdout, colorized=False):
        "Print a colorized version of the stack to a stream"
        def DumpFrameInfo(framenum, fi, t):
            parens = "" if fi.function.startswith("<") else "()"
            print(
                f"{t.frame}Frame {framenum}{t.n} "
                f"{t.filename}{fi.filename}{t.n}:"
                f"{t.lineno}{fi.lineno}{t.n} "
                f"{t.function}{fi.function}{parens}{t.n}"
            )
            print(f"  Code:  {t.code}{fi.code_context[0].strip()!r}{t.n}")
        t = Trm()
        t.always = True
        t.title = t("purl") if colorized else ""
        t.frame = t("whtl") if colorized else ""
        t.filename = t("yell") if colorized else ""
        t.lineno = t("magl") if colorized else ""
        t.function = t("cynl") if colorized else ""
        t.code = t("sky") if colorized else ""
        t.N = t.n if colorized else ""
        stk = deque(stack())
        n = len(stk) - 1
        print(f"{t.title}Stack dump{t.N}")
        # Get rid of this function's frame
        stk.popleft()
        count = 1
        while stk:
            fi = stk.popleft()
            DumpFrameInfo(n - count, fi, t)
            count += 1
if 1:   # TraceExecution
    # I'm not sure where I found this
    def StreamOut(stream, *s, **kw):
        # Process keyword arguments
        sep = kw.setdefault("sep", "")
        auto_nl = kw.setdefault("auto_nl", True)
        prefix = kw.setdefault("prefix", "")
        convert = kw.setdefault("convert", str)
        # Convert position arguments to strings
        strings = map(convert, s)
        # Dump them to the stream
        stream.write(prefix + sep.join(strings))
        # Add a newline if desired
        if auto_nl:
            stream.write("\n")
    g.trace = functools.partial(StreamOut, sys.stdout)
    g.tracen = functools.partial(StreamOut, sys.stdout, auto_nl=False)
    def TraceExecution(f, ignore_exit=True, noname=True, identity=False):
        '''Trace execution of lines inside a function.  If ignore_exit is
        True, typical files like _sitebuiltins.py and threading.py are
        ignored.  If noname is True, don't preface printed line with
        'TraceExecution()'.
        '''
        def DoNotIgnore(filename):
            if not ignore_exit:
                return True
            if filename.name in set("_sitebuiltins.py threading.py".split()):
                return False
            return True
        def globaltrace(frame, why, arg):
            if why == "call":
                return localtrace
            return None
        def localtrace(frame, why, arg):
            h = "" if noname else "TraceExecution() "
            lc = linecache.getline
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            bname = os.path.basename(filename)
            if why == "line":
                # Print the file name and line number of every trace
                if DoNotIgnore(Path(filename)):
                    g.tracen(f"{t.sky}%s[%s:%d] %s{t.n}" % (h, bname, lineno, lc(filename, lineno)))
            elif why == "return":
                if DoNotIgnore(Path(filename)):
                    retval = "==> returning %s <==\n" % repr(arg)
                    g.trace(f"{t.purl}%s[%s:%d] %s{t.n}" % (h, bname, lineno, retval))
            elif why == "exception":
                if DoNotIgnore(Path(filename)):
                    g.trace(f"{t.redl}%s[%s:%d] %s{t.n}" % (h, bname, lineno, "*** Got exception ***"))
                    # In Demo_TraceExecution() below, the traceback produces hundreds of
                    # lines of junk, so the easiest thing is to just exit -- but you
                    # then don't get a traceback -- and inserting a breakpoint doesn't
                    # work. 
                    if not g.noexit:
                        exit(1)
            return localtrace
        def _f(*args, **kwds):
            sys.settrace(globaltrace)
            result = f(*args, **kwds)
            sys.settrace(None)
            return result
        def _f1(*args, **kwds):
            result = f(*args, **kwds)
            return result
        if identity:
            return _f1
        else:
            return _f
if 1:   # Decorators
    class Memoized(object):
        '''Decorator that caches a function's return value each time it is called.
        If called later with the same arguments, the cached value is returned, and
        not re-evaluated.
        '''
        def __init__(self, func):
            self.func = func
            self.cache = {}
        def __call__(self, *args):
            try:
                return self.cache[args]
            except KeyError:
                self.cache[args] = value = self.func(*args)
                return value
            except TypeError:
                # uncachable -- for instance, passing a list as an argument.
                # Better to not cache than to blow up entirely.
                return self.func(*args)
        def __repr__(self):
            '''Return the function's docstring.'''
            return self.func.__doc__
    def Passify(f):
        '''Decorator that disables a function.  The function will return None,
        which may break some code.
        '''
        def do_nothing(*args, **kw):
            pass
        return do_nothing
    def IgnoreDeprecationWarnings(func):
        'Decorator to ignore deprecation warnings occurring in a function'
        def new_func(*args, **kwargs):
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                return func(*args, **kwargs)
        new_func.__name__ = func.__name__
        new_func.__doc__ = func.__doc__
        new_func.__dict__.update(func.__dict__)
        return new_func
if 1:   # Decorators for dumping function arguments
    def DumpArgs1(func):
        'Decorator for dumping arguments passed to a function before calling it'
        # From https://wiki.python.org/moin/PythonDecoratorLibrary (note the code there
        # is for python 2)
        argnames = func.__code__.co_varnames[:func.__code__.co_argcount]
        fname = func.__name__
        def echo_func(*args,**kwargs):
            s = ', '.join('%s=%r' % entry for entry in list(zip(argnames, args))
                          + list(kwargs.items()))
            t.print(t.sky + fname + t.n, ":", s)    # Print the function name & arguments
            return func(*args, **kwargs)    # Call the real function
        return echo_func
    if 1:  # g.names_to_debug for using DumpArgs2()
        # The following global variable controls which names in the following set are
        # allowed to have their arguments shown in class DumpArgs2
        g.names_to_debug = set("a b".split())  # Names that will show arguments
    class DumpArgs2:
        '''Decorator which helps to control which functions have their arguments shown.
        on per-function basis. Names are provided as list of arguments and control which
        functions actually get decorated.  It doesn't slow down functions which aren't
        supposed to be debugged.
        '''
        # From https://wiki.python.org/moin/PythonDecoratorLibrary.
        def __init__(self, names=None):
            'names should be a sequence of strings'
            self.names = set(names)
        def __call__(self, f):
            if self.names & g.names_to_debug:
                def newf(*args, **kwds):
                    t.print(f"{t.sky}{f.__name__} {t.ornl}{args} {t.yel}{kwds}")
                    result = f(*args, **kwds)
                    t.print(f"  {t.sky}{f.__name__} returned {t.purl}{result}")
                    return result
                newf.__doc__ = f.__doc__
                return newf
            else:
                return f

if __name__ == "__main__":
    from wrap import dedent
    from lwtest import run
    t.ti = t("brnl")
    show = True
    Trace.show = True
    def TestDump():
        data = ["1", "2", 3, "4"]
        def pad4(seq):
            return_value = []
            for thing in seq:
                # Will get exception on third element
                return_value.append("0" * (4 - len(thing)) + thing)
            return return_value
        try:
            pad4(data)
        except Exception:
            # Highlight the variable 'thing' in yellow and the variable
            # 'data' in blue.
            hl = {"thing": "yell", "data": "roy"}
            print("\nWe're just about to call DumpException() and we're giving it the")
            print("argument fr_ignore=[0, 1] to ignore frames 0 and 1, which is useful")
            print("to avoid seeing lots of stuff from the global frame.\n")
            DumpException(fr_ignore=[0, 1], hl=hl)
    def Sep():
        t.print(f"{t('purl')}{'='*(g.W - 10)}")
    def Demo_1WatchAndTrace():
        print(dedent(f'''
        {t.ti}watch() and trace(){t.n}
         
        These function calls can be put inside functions to allow you to watch how
        objects change their values.  Note the convenience of colorizing the output (you
        could add logic that changed the color if a certain condition was true).
        '''))
        def test1():
            x, y = 17, -44.3
            watch((x, y), color="grn")
            trace("Trace message")
        class A:
            def f(self):
                s = "a string"
                watch((s,), color="mag")
        print()
        test1()
        a = A()
        a.f()
        # Now use the Trace decorator
        @Trace
        def test2():
            x, y = 88, -42.0
            return x, y
        print("\nThe following is an example of using class Trace, a decorator")
        test2()
        Sep()
    def Demo_2UnhandledException():
        print( dedent(f'''
        {t.ti}Demonstrate an unhandled exception{t.n}
         
        This example shows how DumpException() prints a backtrace followed by
        printing the local variables for each of the stack frames.  If you have
        the color.py module, you'll see the variables 'data' and 'thing'
        highlighted in color.
        '''))
        TestDump()
        print()
        print(dedent('''

        Inspecting Frame 4 and the backtrace, you see that 
            - The exception's problem occurred on line 562
            - Inspecting the return_value list and seq, you can see the problem occurred
              for the value 'thing = 3'.  The problem is that integers don't have a
              length.
        '''))
        Sep()
    def Demo_3TracingToAStream():
        print(dedent(f'''
        {t.ti}Demonstrate tracing to a stream{t.n}
        
        This example shows how @ShowFunctionCall decorates a function to allow
        function calls and their return values to be monitored.  If the global
        variable debug.g.enable_tracing is False, there's no output and little overhead
        is added.  Normally, output goes to a file 'debug.log', but here we set
        g.debug_log to sys.stdout so it went to the console.
        '''))
        g.enable_tracing = True
        g.debug_log = sys.stdout
        if g.enable_tracing:
            @ShowFunctionCall
            def Square_x_and_add_y(x, y=0):
                return x * x + y
            Square_x_and_add_y(3)
            Square_x_and_add_y(4, 5)
            Square_x_and_add_y(4, y=5)
        g.enable_tracing = False
        Sep()
    def Demo_4DumpArgs():
        print(dedent(f'''
        {t.ti}DumpArgs function demo{t.n}
         
        The following code demonstrates the DumpArgs function, a decorator that will
        dump a function's arguments.  We also used debug.fln() to print the file and
        line number where the function returned.
        '''))
        @DumpArgs
        def func(a, b):
            print("  Inside func:  a =", a)
            print("  Inside func:  b =", b)
            t.print(f"  Leaving func() at {t.purl}{fln()}")
        func(2, 3)
        Sep()
    def Demo_5AutoIndenting():
        print(dedent(f'''
        {t.ti}Autoindent example{t.n}
        
        This example demonstrates the use of the AutoIndent object.  The object is used
        to replace sys.stdout and, thus, intercepts calls going to that stream.  Then
        strings sent to stdout are indented based on the current stack frame depth.  If
        you're able to see color, note one of the messages is in color; this is helpul
        to focus your attention on a particular function.  Also note there's a call to
        StackDump() in the function C().

        The Autoindent class is a context manager which gives it a simple usage pattern:

            with Autoindent():
                Code you want to watch...

        The facilities of a context manager allow the Autoindent instance to replace
        sys.stdout with the Autoindent instance, which then has write() and flush()
        methods to behave like a stream.  When the context manager block is exited, the
        standard plumbing is reconnected.
        
        Thereafter, all text going to stdout is indented by the stack frame's depth.
        
        Autoindent isn't affected by debug.show.

        The example here that uses the blue dots is handy because you can see the stack
        depth and get it by counting the dots:
 
        '''))
        print()
        def A():
            print("Entered A()")
            print("Do something...")
            B(i=42, s="something")
            print("Leaving A()")
        def B(i=0, s=""):
            print("Entered B()")
            print(f"Do something in B() at {fln()}")
            C()
            print("Leaving B()")
        def C():
            print("Entered C()")
            print(f"    {t.grn}Indented do something in C() at {fln()}{t.n}")
            print("    This demonstrates that you could put debug code in the function and")
            print("    use its indentation to see what's going on in the function.")
            print("About to call DumpStack()")
            DumpStack()
            print("Leaving C()")
        with AutoIndent(indent=f"{t.sky}·{t.n} "):
            A()
        Sep()
    def Demo_6DumpArgs1():
        t.print(f"{t.ti}DumpArgs1 dumps a function's arguments:")
        @DumpArgs1
        def Example1(a, b, hi="OK"):
            pass
        Example1(42, 3.14, hi="NotOK")
        Sep()
    def Demo_7DumpArgs2():
        print(dedent(f'''
        {t.ti}DumpArgs2{t.n} uses a string to determine if the the function should be decorated
        and prints both the arguments and the return value.
        '''))
        @DumpArgs2(["a"])
        def prn(x):
            print(x)
        @DumpArgs2(["b"])
        def mult(x, y):
            return x * y
        prn(mult(2, 2))
        Sep()
    def Demo_8TraceExecution():
        print(dedent(f'''
        {t.ti}TraceExecution{t.n} prints the line number and line's string for each line in the
        function.  The program's output is mixed in with the debugging output.

        Unfortunately, I've had to insert an exit() call after an exception encountered
        while TraceExecution is running; otherwise, a lot of cruft is printed.  If you 
        want to deal with the exception, comment out the exit() call.
        you can't insert a breakpoint because I've put an exit() call in
        the TraceExecution function to avoid lots of cruft that gets printed out on an
        exception.  If you want to deal with the exception, set the global variable 
        g.noexit to True.
        '''))
        @TraceExecution
        def Example2():
            a = 3
            print()
            b = a*a**a
            #raise ValueError()
            return 42
        Example2()
    run(globals(), regexp=r"^Demo_", quiet=1, halt=1, verbose=0)
