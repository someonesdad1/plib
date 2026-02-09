'''
Various function decorators
    DumpArgs1
        Prints a function's arguments when it is called
    DumpArgs2
        Similar to DumpArgs1 but you can control which functions are decorated
        at runtime
    Memoize
        Caches function calls in a dictionary
    TraceExecution  
        Show execution of lines of a function
    Passify         
        Disables a function and makes it return None
    IgnoreDeprecationWarnings
        Ignore deprecation warnings in a function

    These decorators came from https://wiki.python.org/moin/PythonDecoratorLibrary.

    https://realpython.com/primer-on-python-decorators/ has some information on
    decorators

'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Various function decorators oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2014 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞ 
        
            - This functionality has been moved to debug.py; this file can go to old.
            - https://wiki.python.org/moin/PythonDecoratorLibrary#Function_Timeout looks
              useful
        
        oo>
    '''
    if 1:  # Standard imports
        import functools
        import linecache
        import os
        from pathlib import Path
        import sys
        import warnings
    if 1:  # Custom imports
        from constant import Constant
        from color import t
    if 1:  # Global variables
        g = Constant()
        g.strict = False
        g.noexit = False    # Switch for TraceExecution
        # Set to a stream-like object to dump arguments
        dump_stream = sys.stdout
if 1:  # TraceExecution
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
                    g.trace("{t.purl}%s[%s:%d] %s{t.n}" % (h, bname, lineno, retval))
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
if 1:  # Core functionality
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
if 1:  # Dumping function arguments
    def DumpArgs1(func):
        'Dumps arguments passed to a function before calling it'
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
        on per-function basis. Aspects are provided as list of arguments.
        It DOESN'T slowdown functions which aren't supposed to be debugged.
        '''
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
    from lwtest import run
    from wrap import dedent
    def Sep():
        t.print(f"{t.purl}{'-'*80}")
    def Demo_DumpArgs1():
        print(f"DumpArgs1 dumps a function's arguments:")
        @DumpArgs1
        def Example1(a, b, hi="OK"):
            pass
        Example1(42, 3.14, hi="NotOK")
        Sep()
    def Demo_DumpArgs2():
        print(dedent('''
        DumpArgs2 uses a string to determine if the the function should be decorated
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
    def Demo_TraceExecution():
        print(dedent('''
        TraceExecution prints the line number and line's string for each line in the
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
            raise ValueError()
            return 42
        Example2()
    #Demo_DumpArgs1()
    #Demo_DumpArgs2()
    Demo_TraceExecution()
    #exit(run(globals(), regexp=r"^[Demo_]", halt=1, verbose=0)[0])
