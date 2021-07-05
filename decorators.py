'''
Various function decorators
    DumpArgs        Prints a function's arguments when it is called
    Memoize         Caches function calls in a dictionary
    TraceExecution  Show execution of lines of a function
    Passify         Disables a function and makes it return None
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Various function decorators
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import functools
    import linecache
    import pathlib
    import os
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    P = pathlib.Path
    # Set to a stream-like object to dump arguments
    dump_stream = sys.stdout
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
if 1:   # Global variables
    trace = functools.partial(StreamOut, sys.stdout)
    tracen = functools.partial(StreamOut, sys.stdout, auto_nl=False)
def DumpArgs(func):
    "Decorator to dump a function's arguments"
    # From http://wiki.python.org/moin/PythonDecoratorLibrary
    # Note the global variable dump_stream must be a stream-like object
    # for this to work.
    argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
    fname = func.func_name
    def EchoFunc(*args, **kwargs):
        if dump_stream:
            dump_stream("+ " + fname + "(" + ', '.join('%s=%r' % entry
                 for entry in zip(argnames, args) + kwargs.items())
                 + ")\n")
        return func(*args, **kwargs)
    return EchoFunc
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
def TraceExecution(f, ignore_exit=True, noname=True):
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
            if DoNotIgnore(P(filename)):
                tracen("%s[%s:%d] %s" % (h, bname, lineno, lc(filename, lineno)))
        elif why == "return":
            if DoNotIgnore(P(filename)):
                retval = "==> returning %s <==\n" % repr(arg)
                trace("%s[%s:%d] %s" % (h, bname, lineno, retval))
        elif why == "exception":
            if DoNotIgnore(P(filename)):
                trace("%s[%s:%d] %s" % (h, bname, lineno, "*** Got exception ***"))
        return localtrace
    def _f(*args, **kwds):
        sys.settrace(globaltrace)
        result = f(*args, **kwds)
        sys.settrace(None)
        return result
    return _f
def Passify(f):
    '''Decorator that disables a function.  The function will return None,
    which may break some code.
    '''
    def do_nothing(*args, **kw):
        pass
    return do_nothing
