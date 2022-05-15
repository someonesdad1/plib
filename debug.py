'''
Debugging tools
    Set debug.on to True to debug.

    Trace
        Function decorator to show function calls with their parameters.
    
    AutoIndent object
        Use this object to cause printed messages to a stream to be
        indented according to the stack level.  The output then gives you a
        visual image of the call stack.
    
    SetDebugger
        Execute and you'll be dumped into the debugger if your code has an
        unhandled exception.
    
    Put in your code:
        watch(variable)
            Prints out the file and line number along with the
            value and type of a variable.
        trace(message)
            Prints file and line number along with the message.
    To turn off, run python with the -O option or set debug.on to False.
    
    DumpException
        Gives more exception information than a normal backtrace.
    
    Identify location:
            ThisFunctionName()
            ThisLineNumber()
            ThisFilename()
    
    fln()
        File & line number if debug.on is True.
    
    ShowFunctionCall decorator [Beazley]
    
    References:
        A. Martelli and D. Ascher, ed., "Python Cookbook", O'Reilly, 2002.
        D. Beazley, "Python Essential Reference", 4th ed. (Kindle version)
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2009, 2014 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # <programming> Debugging aids (taken from the "Python Cookbook" and
        # Beazley's "Python Essential Reference", 4th edition).
        #∞what∞#
        #∞test∞# ignore #∞test∞#
    # Standard imports 
        import types
        import sys
        import traceback as TB
        import os
        import re
        import bdb
        import pdb
        from inspect import stack
        from pdb import set_trace as xx 
    # Custom imports 
        from util import IsIterable
        try:
            import dpdb
            have_dpdb = True
            xx = dpdb.set_trace
        except ImportError:
            have_dpdb = False
            xx = pdb.set_trace
        if 1:
            from color import Color, TRM as t
        else:
            try:
                import kolor as c
            except ImportError:
                # Make c a class that will swallow all color calls/references
                class C:
                    def __getattr__(self, x):
                        pass
                    def fg(self, *p, **kw):
                        pass
                    def normal(self):
                        pass
                c = C()
    # Global variables
        # dash_O_on = True  ==> Use python -O to turn debugging on.
        # dash_O_on = False ==> Use python -O to turn debugging off.
        dash_O_on = False
        on = True   # Setting on to True causes debugging output.
        enable_tracing = False
        if enable_tracing:
            debug_log = open("debug.log", "wb")
        ii = isinstance
        w = int(os.environ.get("COLUMNS", "80")) - 1
class Trace:
    '''Function decorator to print the entry and exit of function calls
    to a stream.  Each nested call results in indentation to help you
    visually see where in the call stack you are.  If Trace.on is
    False, there should be little extra overhead from this decorator,
    so you may want to leave it in production code.
 
    You may want to set your calling code up so that Trace.on is set to
    True if e.g. a particular environment variable is set or your
    program receives a software signal.
 
    Example of use:
 
        @Trace
        def MyFunction():
    '''
    increment = 2           # Increment for indenting
    indent = -increment     # How many spaces to indent.  It's negative
                            # the increment so it starts at 0.
    stream = sys.stdout     # Stream that receives the printed output
    on = False              # Set to True to get tracing output
    prefix = "+ "
    def __init__(self, func):
        self.func = func
        try:
            self.name = func.func_name
        except AttributeError:
            self.name = func.__name__
    def __call__(self, *p, **kw):
        if Trace.on:
            Trace.indent += Trace.increment
            ind, f, prefix = " "*Trace.indent, self.name, Trace.prefix
            s = ["{prefix}{ind}Entering {f}(".format(**locals())]
            c = ", " if kw else ""
            if p:
                s.append("args={p}{c}".format(**locals()))
            if kw:
                s.append("kw={kw}".format(**locals()))
            s.append(")")
            print(''.join(s), file=Trace.stream)
            retval = self.func(*p, **kw)
            print("{prefix}{ind}Exiting {f}:  returned {retval}".format(
                **locals()), file=Trace.stream)
            Trace.indent -= Trace.increment
            return retval
        else:
            return self.func(*p, **kw)
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
    assert(IsIterable(variables)) 
    assert(color is None or ii(color, str) or ii(color, Color))
    assert(hasattr(stream, "write"))
    def GetVariableNames(s):
        '''s is a string of the form 'watch([x, y], color=c)'.
        Extract the names of the nonkeyword parameters and return as a
        list of strings.
 
        Some possible forms of s are
            'watch((x,))'
            'watch((x,), color="xxx")'
            'watch([x,])'
            'watch([x,], color="xxx")'
            'watch((x, y))'
            'watch((x, y), color="xxx")'
            'watch([x, y])'
            'watch([x, y], color="xxx")'
        The first four forms need to return ("x",) or ["x"]; the second
        four need to return ("x", "y") or ["x", "y"].
        '''
        # Remove 'watch(' and trailing ')'
        u = s[6:-1]
        # Get rid of 'color' part
        if '=' in u:
            u = u.split("=")[0].rstrip()
            assert(u.endswith("color"))
            u = u[:-5].rstrip()
            assert(u[-1] == ",")
            u = u[:-1]
        u = u.strip()
        # Now u is the string of a tuple or list.  Remove the first and
        # last characters and we have a comma-separated list of variable
        # names.
        u = u[1:-1]
        v = [i.strip() for i in u.split(",") if i.strip()]
        return v
    if (((__debug__ and not dash_O_on) or
            (not __debug__ and dash_O_on)) and on):
        fn, ln, method, call = TB.extract_stack()[-2:][0]
        names = GetVariableNames(call)
        if stream == sys.stdout and color is not None:
            if ii(color, str):
                # It's a color name or hex string or an ANSI escape sequence
                if "\x1b" in color:
                    print(color, end="")
                else:
                    print(t(color), end="")
            elif ii(color, Color):
                print(f"t(color)", end="")
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
    if (((__debug__ and not dash_O_on) or
            (not __debug__ and dash_O_on)) and on):
        stack = TB.extract_stack()[-2:][0]
        fn, ln, method, call = stack
        fmt = "{fn}[{ln}] in {method}:  {msg}\n"
        if stream == sys.stdout and color is not None:
            c.fg(color)
        stream.write(fmt.format(**locals()))
        if stream == sys.stdout and color is not None:
            c.normal()
def DumpException(fr_include=None, fr_ignore=None,
                  var_include=None, var_ignore=None,
                  num_levels=0, hl={}, stream=sys.stdout):
    '''Print the traceback information followed by a listing of the
    local variables in each frame.  This function is intended to be
    used in a try/except block to print the details of an unhandled
    exception.  The keyword parameters give control over what is
    printed and how it's displayed.
 
    Note it always works, regardless of debug.on's value.
 
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
        print("Locals in frames %s, innermost frame = 0" % s,
              file=stream)
    else:
        print("Locals by frame, innermost last", file=stream)
    # Print a note if not all stack frames are shown
    m1, m2 = "Note:", "  only selected %s are shown"
    if ((fr_include is not None and len(fr_include)) or
            (fr_ignore is not None and len(fr_ignore)) or num_levels):
        if stream == sys.stdout:
            print(f"{t('redl', 'blk')}", end="")
        print(m1, end="", file=stream)
        if stream == sys.stdout:
            print(f"{t.n}", end="")
        print(m2 % "stack frames", file=stream)
    # Print a note if not all locals are shown
    if ((var_include is not None and len(var_include)) or
            (var_ignore is not None and len(var_ignore)) or num_levels):
        if stream == sys.stdout:
            print(f"{t('redl', 'blk')}", end="")
        print(m1, end="", file=stream)
        if stream == sys.stdout:
            print(f"{t.n}", end="")
        print(m2 % "local variables", file=stream)
    levels_printed = 0
    for i, frame in enumerate(frames):
        if ((fr_include is not None and i not in fr_include) or
                (fr_ignore is not None and i in fr_ignore)):
            continue
        print("-"*70, file=stream)
        print("Frame %d %s() in %s at line %s" % (
            i,
            frame.f_code.co_name,
            frame.f_code.co_filename,
            frame.f_lineno),
            file=stream
        )
        Locals = list(frame.f_locals.items())
        Locals.sort()
        for key, value in Locals:
            if ((var_include is not None and key not in var_include) or
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
                print("<Error '%s' while printing value for '%s'>" %
                      (str(e), key), file=stream)
        levels_printed += 1
        if num_levels and levels_printed >= num_levels:
            break
def TraceInfo(type, value, traceback):
    '''Start the debugger after an uncaught exception.  From Thomas
    Heller's post on 22 Jun 2001 http://code.activestate.com/recipes/65287
    Also see page 435 of "Python Cookbook".
    '''
    # Updated first test logic from https://gist.github.com/rctay/3169104
    if  (
            hasattr(sys, 'ps1')           or
            not sys.stderr.isatty()       or
            not sys.stdout.isatty()       or
            not sys.stdin.isatty()        or
            issubclass(type, bdb.BdbQuit) or
            issubclass(type, SyntaxError)
        ):
        # You are in interactive mode or don't have a tty-like device,
        # so call the default hook.
        sys.__excepthook__(type, value, traceback)
    else:
        # You are not in interactive mode; print the exception.
        TB.print_exception(type, value, traceback)
        print()
        # Now start the debugger
        if have_dpdb:
            dpdb.pm()
        else:
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
        argnames = fc.co_varnames[:fc.co_argcount]
        args = ", ".join("%s=%r" % entry for entry in
                         list(zip(argnames, p)) + list(kw.items()))
        print(f"{fn}({args})")
        return func(*p, **kw)
    return echo_func if on else func
def ShowFunctionCall(func):
    '''This is a wrapper function that decorates another function for
    tracing what happens.  The nice thing is that there is no overhead if
    enable_tracing is false.  callf is a closure that replaces the original
    function.
    '''
    # This decorator is for showing how a function was called
    # and its return value comes from Beazley, 4th ed., Ch. 6, section
    # on decorators.
    if enable_tracing and on:
        def callf(*args, **kwargs):
            debug_log.write("Calling %s: params=%s, kw=%s\n" %
                            (func.__name__, args, kwargs))
            r = func(*args, **kwargs)
            debug_log.write("        %s returned %s\n" % (func.__name__, r))
            return r
        return callf
    else:
        return func
def fln(brackets=True):
    'Return a string showing the file and line number if debug is on.'
    s = TB.extract_stack()[-2:][0]
    t = "{}:{}".format(s[0], s[1]) if __debug__ else ""
    if brackets:
        t = "[{}]".format(t)
    return t
class AutoIndent(object):
    '''Indent debug output based on function call depth.  Adapted from
    code by Lonnie Princehouse (submitted 26 Apr 2005) at
    http://code.activestate.com/recipes/411791
 
    Usage example:
        sys.stdout = AutoIndent()
        print(msg)
    which sends the printed messages through the AutoIndent object to
    be indented based on the stack depth.
 
    The code:
        def i():
            print("Entered i()")
            print("Do some things...")
            print("Leaving i()")
        def h():
            print("Entered h()")
            i()
            print("Leaving h()")
        def g():
            print("Entered g()")
            h()
            print("Leaving g()")
        sys.stdout = AutoIndent()
        print("Beginning level")
        g()
    will result in the following output
        Beginning level
        Entered g()
            Entered h()
                Entered i()
                Do some things...
                Leaving i()
            Leaving h()
        Leaving g()
    '''
    def __init__(self, stream=sys.stdout, indent=4, ansi=False):
        '''stream is where you want the information to be sent.
        indent is either the number of spaces or a string to use for
        each indent level.  If ansi is True, then handle incoming
        strings with ANSI escape sequences for color specially.
        '''
        self.stream = stream
        self.depth = len(stack())
        self.indent = " "*indent if isinstance(indent, int) else indent
        self.ansi = False
        if ansi:
            # Regular expression to recognize ANSI escape sequences
            # used for changing colors.
            self.ansi = re.compile(r"\x1b\[\d+(;\d+)*m")
    def _indent_level(self):
        return max(0, len(stack()) - self.depth - 2)
    def write(self, data):
        # Note we intercept ANSI escape codes when data is a string
        # and send them on unindented.
        if 0 and isinstance(data, str) and self.ansi:
            mo = self.ansi.search(data)
            if mo:
                self.stream.write(data)
                return
        indentation = self.indent*self._indent_level()
        f = lambda x: indentation + x if x else x
        data = '\n'.join([f(line) for line in data.split('\n')])
        self.stream.write(data)
    def flush(self):
        self.stream.flush()

if __name__ == "__main__":
    from wrap import dedent
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
            DumpException(fr_ignore=[0], hl=hl)

    # Print samples to stdout.  After seeing the behavior, set the global
    # variable on to False (uncomment the next line) to see the debug
    # printing turned off.
    #on = False
    def Sep():
        t.print(f"{t('purl')}{'='*(w - 10)}")
    t.ti = t("brnl")
    Sep()
    if 1:   # watch and trace
        print(dedent(f'''
        {t.ti}watch() and trace(){t.n}

        These function calls can be put inside functions to allow you to
        watch how objects change their values.  Note the convenience of
        colorizing the output (you could add logic that changed the color
        if a certain condition was true).
        
        '''))
        def test1():
            x, y = 17, -44.3
            watch((x, y), color="grnl")
            trace("Trace message")
        class A:
            def f(self):
                s = "a string"
                watch((s,), color="magl")
        test1()
        a = A()
        a.f()
        Sep()
    if 1:   # Demonstrate an unhandled exception
        print(dedent(f'''
        {t.ti}Demonstrate an unhandled exception{t.n}

        This example shows how DumpException() prints a backtrace followed by
        printing the local variables for each of the stack frames.  If you have
        the color.py module, you'll see the variables 'data' and 'thing'
        highlighted in color.

        '''))
        TestDump()
        Sep()
    if 1:   # Demonstrate tracing to a stream
        print(dedent(f'''
        {t.ti}Demonstrate tracing to a stream{t.n}

        This example shows how @ShowFunctionCall decorates a function to allow
        function calls and their return values to be documented.  If the global
        variable enable_tracing is False, there's no output and little overhead
        is added.

        '''))
        enable_tracing = True
        debug_log = sys.stdout
        if enable_tracing:
            @ShowFunctionCall
            def Square_x_and_add_y(x, y=0):
                return x*x + y
            Square_x_and_add_y(3)
            Square_x_and_add_y(4, 5)
            Square_x_and_add_y(4, y=5)
        enable_tracing = False
        Sep()
    if 1:   # Demonstrate auto indenting
        print(dedent(f'''
        {t.ti}Autoindent example{t.n}
        
        This example demonstrates the use of the AutoIndent object.  The
        object is used to replace sys.stdout and, thus, intercepts calls
        going to that stream.  Then strings sent to stdout are indented
        based on the current stack frame depth.  If you're able to see
        color, note one of the messages is in color; this is helpul to
        focus your attention on a particular function.
        
        An advantage of using Autoindent is that you only need to make the
        call shown in the first line; thereafter, all text going to stdout
        is indented by the stack frame's depth.  Make sure to un-redirect
        stdout when you're finished or the subsequent code will be messed
        up.
        
        Autoindent isn't affected by debug.on.

        '''))
        old_stdout = sys.stdout
        sys.stdout = AutoIndent(indent="|   ")
        def A():
            print("Entered A()")
            print("Do something...")
            B()
            print("Leaving A()")
        def B():
            print("Entered B()")
            print("Do something...")
            C()
            print("Leaving B()")
        def C():
            print("Entered C()")
            print(f"{t('grnl')}Do something...{t.n}")
            print("Leaving C()")
        A()
        # Remember to reconnect old stream
        sys.stdout = old_stdout
        Sep()
    if 1:   # DumpArgs function
        print(dedent(f'''
        {t.ti}DumpArgs function demo{t.n}

        The following code demonstrates the DumpArgs function, a
        decorator that will dump a function's arguments.

        '''))
        @DumpArgs
        def func(a, b):
            print("  Inside func:  a =", a)
            print("  Inside func:  b =", b)
        func(2, 3)
