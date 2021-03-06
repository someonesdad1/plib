'''
TODO:

    - If an argument passed on the command line is a directory,
        search it recursively for all files that appear to be test
        scripts and run them.

        - If a file is passed on the command line, search it for
            suitable test functions and run them, even if there's no
            run() call in the script.  Options to provide run()'s
            features:  -h to halt at first failure, -r for regexp to
            identify a test function, -R for regexp's options, -v for
            verbose

    - Add a verbose keyword to run() which prints the file name and
        the function/class to be executed, like 'nosetests -v' does.
        Another thing to consider would be to let run look at sys.argv
        and process options there in lieu of keywords (this would be
        handy for command line work, as the command line options would
        overrule the keywords).
'''
if 1:  # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # <programming> Lightweight test runner.  I use this tool to run all
        # my python module's regression tests, as I was dissatisfied with
        # python's unittest and I've never liked doctest.
        #∞what∞#
        #∞test∞# ["test/lwtest_test.py"] #∞test∞#
    # Origin
        # Derived from some nice code by Raymond Hettinger 8 May 2008:
        # http://code.activestate.com/recipes/572194/.  Downloaded 27 Jul
        # 2014.  The ActiveState web page appears to state Hettinger's code
        # was released under the PSF (Python Software Foundation) License.
        # Hettinger's code includes a search for test functions that are
        # generators; if such functionality is important to you, you might
        # want to add it to this file.
        #
        # The raises context() manager functionality was inspired by pytest's
        # implementation (see https://docs.pytest.org/en/latest/).
    # Standard imports
        from collections.abc import Iterable
        from decimal import Decimal
        from math import isnan, isinf, copysign
        from time import time
        import os
        import re
        import sys
        import traceback
        from pdb import set_trace as xx 
    # Custom imports
        from f import flt, cpx
        from wrap import dedent
        from color import Color, TRM as t
    # Optional imports
        try:
            import numpy
            have_numpy = True
        except ImportError:
            have_numpy = False
        try:
            import mpmath
            have_mpmath = True
        except ImportError:
            have_mpmath = False
    # Global variables
        __doc__ = dedent('''
        Lightweight testrunner framework
            from lwtest import run, raises, assert_equal, Assert, Debugger
        
            def TestExample():
                f = lambda x: set(x)
                # Two ways to check for expected exceptions
                raises(TypeError, f, 1)
                with raises(ZeroDivisionError) as x:
                    1/0
                Assert(x.value = "<class 'ZeroDivisionError'>")
                # How to compare floating point numbers
                eps = 1e-6
                a, b = 1, 1 + eps

                # In following, debug=True starts debugger if a != b
                assert_equal(a, b, abstol=eps, debug=True)
                # Set Assert.debug to True to always drop into debugger
        
            if __name__ == "__main__":
                failed, messages = run(globals())
            or 
                exit(run(globals(), halt=True)[0])
        
            run()
                Finds test functions and execute them.  Its single argument
                must be a dictionary containing the names and their
                associated function objects.  Set verbose=True to see which
                functions will be executed and their execution order.
        
            Assert() 
                Works like python's assert statement, but can drop you into
                the debugger if so instructed.  Type 'up' to go to the
                failed Assert() line.  Since dropping into the debugger is
                a common need, there are multiple ways:

                    - Set the debug keyword to True
                    - Include a command line argument
                    - Set Assert.debug to True
                    - Set the environment variable 'Assert' to the nonempty
                      string

                Note Assert() and assert_equal() do not pay attention to
                __debug__, unlike python's assert statement.
        
            ToDoMessage()
                Causes a colored message to be printed to stdout to remind
                you of something that needs to be done.
        
            My motivation for generating this lightweight testrunner framework
            was my frustration with the unittest module in conjunction with the
            way I develop code.  I write my unit tests before or during code
            development and often need to drop into the debugger or add a print
            statement to see what's going wrong.  The unittest module traps
            stdout and makes this painful to do.  I liked some of the available
            testrunners like nose or pytest, but I decided that if I was going
            to add a new dependency, it might as well be a dependency I could
            tune to my own preferences.  The other major desire was to allow
            fairly comprehensive coverage of comparing numerical results.
        
            This tool was derived from some nice code by Raymond Hettinger 8
            May 2008: http://code.activestate.com/recipes/572194/.  I'm
            grateful Raymond put it out there for other folks.
        ''')
        __all__ = [
            "Assert",
            "ToDoMessage",
            "assert_equal",
            "raises",
            "run",
            "test_function_regexp",
        ]
        ii = isinstance
        python_version = '.'.join([str(i) for i in sys.version_info[:3]])
        # Regular expression to identify test functions
        test_function_regexp = "^_*test|test$"
if 1:   # Core functionality
    def run(names_dict, **kw):
        '''Discover and run the test functions in the names_dict
        dictionary (name : function pairs).  Return (failed, s) where
        failed is an integer giving the number of failures that occurred
        and s is the information string that was sent (or would have been
        sent) to the stream.  A failure is an unhandled exception.
    
        Keyword options [default]:
            broken:     If True, testing code is acknowledged to be broken;
                        a warning message is printed and tests are not run.
                        [False]
            dbg:        If True, don't handle exceptions (allows you to trap
                        them in a debugger).  Also can set the environment
                        variable 'dbg' to do this. [False]
            verbose:    Print the function names as they are executed. [False]
            halt:       Stop at the first failure.  [False]
            quiet:      If True, no output.  [False]
            regexp:     Regular expression that identifies a test function.
                        Default is in global variable test_function_regexp.
            reopts:     Regular expression's options. [re.I]
            stream:     Where to send output [stdout].  None = no output.
            nomsg       If True, return only the integer 'failed'.
        '''
        # Keyword arguments
        broken = bool(kw.get("broken", False))
        dbg = bool(kw.get("dbg", False)) or "dbg" in os.environ
        verbose = bool(kw.get("verbose", False))
        halt = bool(kw.get("halt", False))
        quiet = kw.get("quiet", False)
        reopts = kw.get("reopts", re.I)
        regexp = kw.get("regexp", test_function_regexp)
        stream = kw.get("stream", sys.stdout)
        nomsg = kw.get("nomsg", False)
        # If broken, print error message and return
        if broken:
            # Get the name of the file that called us
            file = traceback.extract_stack()[0][0]
            print(f"{t('ornl')}! {file}:  Error:  tests are broken{t.n}")
            return (1, "Tests are broken")
        # Find test functions in names_dict to run.  Note we don't allow
        # "_lwtest" to end the name; this lets you use a variable like 
        # _have_lwtest in a script.
        istest = re.compile(regexp, reopts)
        tests = [(name, func) for name, func in names_dict.items()
                if istest.search(name) and not name.endswith("_lwtest")]
        # Reverse the list so they can be popped in alphabetical order
        tests = sorted(tests, reverse=True)
        try:
            filename = names_dict["__file__"]
        except KeyError:
            # Use the current file's name; put angle brackets around it to
            # indicate it might not be the correct file (e.g., the user
            # manually invoked run() with a hand-crafted dictionary and
            # forgot to add a "__file__" key).
            filename = f"<__file__ ?>"
        pass_count = fail_count = 0
        fail_messages = []
        if verbose:
            print("Test functions in {}:".format(filename), file=stream)
        nl = "\n"
        start_time = time()
        # Run the test functions
        while tests:
            name, func = tests.pop()
            try:
                if verbose:
                    print(" ", name, file=stream)
                func()
            except TypeError as e:
                # Probably trying to run the module.
                if str(e) == '''TypeError("'module' object is not callable",)''':
                    print("xx lwtest.py:  need to test TypeError catch")
                else:
                    raise
            except Exception as e:
                if dbg:
                    raise
                fail_count += 1
                lines = [f"{name} failed:  {e!r}"]
                # Append an indented stack trace
                for line in traceback.format_exc().split(nl):
                    lines.append("  " + line)
                fail_messages += lines
                if halt:
                    break
            else:
                pass_count += 1
        stop_time = time()
        output = (nl.join(fail_messages) if fail_messages else
                "{}:  {} {} passed in {} [python {}]".
                format(filename, 
                        pass_count, 
                        "test" if pass_count == 1 else "tests", 
                        GetTime(stop_time - start_time), 
                        python_version))
        if stream and not quiet:
            print(output, file=stream)
        if nomsg:
            return fail_count
        else:
            return (fail_count, output)
    def raises(ExpectedExceptions, *args, **kw):
        '''Asserts that a function call raises one of a sequence of expected
        exceptions.  ExpectedExceptions can either be a single exception
        type or a sequence of such types.  If args is empty, then a context
        manager instance is returned for use in a 'with' statement.  Examples:
            Function call:
                raises((Exception1, Exception2), func, 0, akw=True)
            Context manager:
                with raises(ZeroDivisionError):
                    1/0
        '''
        if args:
            try:
                args[0](*args[1:], **kw)
            except ExpectedExceptions:
                return
            else:
                raise AssertionError("Did not raise expected exception")
        return RaisesContextManager(ExpectedExceptions)
    class RaisesContextManager(object):
        def __init__(self, ExpectedExceptions):
            '''Initialize with one one exception object or a sequence of
            exception objects
            '''
            if issubclass(ExpectedExceptions, BaseException):
                self.expected = set([ExpectedExceptions])
                return
            elif not issubclass(ExpectedExceptions, Iterable):
                m = f"ExpectedExceptions must be a container of Exceptions"
                raise ValueError(m)
            self.expected = set(ExpectedExceptions)
            for exc in self.expected:
                if not issubclass(exc, BaseException):
                    m = f"'{exc}' is not a subclass of BaseException"
                    raise ValueError(m)
            self.value = None
        def __enter__(self):
            return self
        def __exit__(self, exception, exception_value, traceback):
            if exception in self.expected:
                self.value = str(exception)
                return True
            raise AssertionError("Did not raise expected exception")
if 1:   # Utility
    def GetTime(duration_s):
        if duration_s > 3600:
            return f"{duration_s/3600:.3f} hr"
        elif duration_s > 60:
            return f"{duration_s/60:.2f} min"
        else:
            return f"{duration_s:.2f} s"
    def ToDoMessage(message, prefix="+ ", color=None):
        '''This function results in a message to stdout; its purpose is to
        allow you to see something that needs to be done, but won't cause
        the test to fail.  The message is decorated with a leading prefix
        string and the file and line number.  If color is not None, then it
        must either be a string naming a color (see color.py) or a Color
        class instance.  The message is printed in this color.
        '''
        fn, ln, method, call = traceback.extract_stack()[-2]
        c = t(color) if color is not None else ""
        vars = {"fn": fn, "ln": ln, "method": method, "msg": message,
            "prefix": prefix, "c": c, "n": t.n }
        if vars["method"] == "<module>":
            if color is None:
                print("{prefix}{fn}[{ln}]:  {msg}".format(**vars))
            else:
                print("{c}{prefix}{fn}[{ln}]:  {msg}{n}".format(**vars))
        else:
            if color is None:
                print("{prefix}{fn}[{ln}] in {method}:  {msg}".format(**vars))
            else:
                print("{c}{prefix}{fn}[{ln}] in {method}:  {msg}{n}".format(**vars))
if 1:   # Checking functions
    def check_flt(a, b, reltol=None, abstol=None, use_min=False):
        '''a must be a flt.  If b is not a flt, then convert it if
        possible.
        '''
        assert(ii(a, flt))
        check_float(float(a), float(b), reltol=reltol,
                    abstol=abstol, use_min=use_min)
    def check_cpx(a, b, reltol=None, abstol=None, use_min=False):
        '''a must be a cpx.  If b is not a cpx, then convert it if
        possible.
        '''
        assert(ii(a, cpx))
        check_complex(complex(a), complex(b), reltol=reltol,
                      abstol=abstol, use_min=use_min)
    def check_float(a, b, reltol=None, abstol=None, use_min=False):
        '''Some of these checks were patterned after the checks in
        Lib/test/test_cmath.py in the python distribution (probably
        version 2.6.5).
        '''
        if not ii(a, (int, float)):
            raise ValueError("a needs to be a float")
        if not ii(b, float):
            # Convert b to float
            try:
                b = float(str(b))
            except Exception:
                raise ValueError("b must be convertible to a float")
        fail = None
        # Handle NaN and infinite values
        if ((isnan(a) and not isnan(b)) or (not isnan(a) and isnan(b))):
            fail = []
        if ((isinf(a) and not isinf(b)) or (not isinf(a) and isinf(b))):
            fail = []
        sign_a, sign_b = copysign(1., a), copysign(1., b)
        if isinf(a) and isinf(b):
            # a and b can be infinite, but they must have the same sign
            if sign_a != sign_b:
                fail = ["a and b are infinity with opposite signs"]
        elif not a and not b:  # Zeros must have the same sign
            if sign_a != sign_b:
                fail = ["a and b are zero with opposite signs"]
        else:
            try:
                # Check for overflow (mentioned as a rare corner case in
                # Lib/test/test_cmath.py).
                absdiff = abs(b - a)
            except OverflowError:
                fail = ["Arguments not equal (overflow occurred)"]
            else:
                abstol = 0 if abstol is None else abstol
                reltol = 0 if reltol is None else reltol
                minmax = min if use_min else max
                tolerance = minmax(abstol, reltol*abs(a))
                if not a and b:  # Relative to b if a is zero
                    tolerance = minmax(abstol, reltol*abs(b))
                if absdiff > tolerance:
                    fail = [
                         "Unacceptable numerical difference:",
                        f"  abstol     = {abstol}",
                        f"  reltol     = {reltol}",
                        f"  tolerance  = {tolerance}",
                        f"  difference = {absdiff}",
                        f"  difference - tolerance = {absdiff - tolerance}",
                    ]
        return fail
    def check_decimal(a, b, reltol=None, abstol=None, use_min=False):
        fail = None
        if not ii(a, Decimal):
            raise ValueError("a needs to be a Decimal")
        if not ii(b, Decimal):
            # Convert b to Decimal
            try:
                b = Decimal(str(b))
            except Exception:
                raise ValueError("b must be convertible to a Decimal")
        # Handle NaN and infinite values
        if ((a.is_nan() and not b.is_nan(b)) or (not a.is_nan() and b.is_nan())):
            fail = []
        if ((a.is_infinite() and not b.is_infinite()) or
                (not a.is_infinite() and b.is_infinite())):
            fail = []
        sign_a, sign_b = a.copy_sign(Decimal(1)), b.copy_sign(Decimal(1))
        if a.is_infinite() and b.is_infinite():
            # a and b can be infinite, but they must have the same sign
            if sign_a != sign_b:
                fail = ["a and b are infinity with opposite signs"]
        elif not a and not b:  # Zeros must have the same sign
            if sign_a != sign_b:
                fail = ["a and b are zero with opposite signs"]
        else:
            try:
                # Check for overflow
                absdiff = abs(b - a)
            except OverflowError:
                fail = ["Arguments not equal (overflow occurred)"]
            else:
                D, zero = Decimal, Decimal(0)
                abstol = zero if abstol is None else D(str(abstol))
                reltol = zero if reltol is None else D(str(reltol))
                minmax = min if use_min else max
                tolerance = minmax(abstol, reltol*abs(a))
                if not a and b:  # Relative to b if a is zero
                    tolerance = minmax(abstol, reltol*abs(b))
                if absdiff > tolerance:
                    fail = [
                         "Numerical difference",
                        f"  abstol     = {abstol}",
                        f"  reltol     = {reltol}",
                        f"  tolerance  = {tolerance}",
                        f"  difference = {absdiff}",
                        f"  difference - tolerance = {absdiff - tolerance}",
                    ]
        return fail
    def check_complex(a, b, reltol=None, abstol=None, use_min=False):
        if not ii(a, complex) or not ii(b, complex):
            raise ValueError("Both a and be need to be complex")
        # The real and imaginary parts must satisfy the requirements
        # separately.
        fail = check_float(a.real, b.real, reltol=reltol, abstol=abstol,
                        use_min=use_min)
        f = check_float(a.imag, b.imag, reltol=reltol, abstol=abstol,
                        use_min=use_min)
        if f is not None:
            if fail is not None:
                fail += f
            else:
                fail = f
        return fail
    def check_equal(a, b, reltol=None, abstol=None, use_min=False):
        '''a and b are not sequences, so they can be compared directly.
        The comparison semantics are determined by reltol and abstol; if
        either is nonzero, then a and b are compared as floating point
        types; which type comparison is used is determined by the type
        of a.  Otherwise, a and b are compared directly.
        '''
        fail = None
        R, A, U = reltol, abstol, use_min
        if reltol is not None or abstol is not None:
            # Floating point comparisons
            if ii(a, flt):
                fail = check_flt(a, b, reltol=R, abstol=A, use_min=U)
            elif ii(a, (int, float)):
                fail = check_float(a, b, reltol=R, abstol=A, use_min=U)
            elif ii(a, complex):
                fail = check_complex(a, b, reltol=R, abstol=A, use_min=U)
            elif ii(a, Decimal):
                fail = check_decimal(a, b, reltol=R, abstol=A, use_min=U)
            elif have_mpmath and ii(a, mpmath.mpf):
                fail = check_float(a, b, reltol=R, abstol=A, use_min=U)
            elif have_mpmath and ii(a, mpmath.mpc):
                fail = check_complex(a, b, reltol=R, abstol=A, use_min=U)
            else:
                raise RuntimeError(f"a is unrecognized type '{type(a)}'")
        else:
            # Object comparison
            if ii(a, str):
                if a != b:
                    fail = ["Unequal strings"]
            else:
                if a != b:
                    fail = ["{} != {}".format(repr(a), repr(b))]
        return fail
    def assert_equal(a, b, reltol=None, abstol=None, use_min=False, 
                    msg="", halt=True, debug=False):
        '''Raise an AssertionError if a != b.  a and b can be objects,
        numbers, or sequences of numbers (sequence elements are compared
        pairwise), or dictionaries.  reltol and abstol are the relative and
        absolute tolerances.  No exception will be raised if for each
        number element (if a is zero, reltol*b is used instead)
                abs(a - b) <= reltol*a
        or
                abs(a - b) <= abstol
        If both abstol and reltol are defined, the one with the larger
        tolerance range will be used unless use_min is True, in which case
        the smaller tolerance will be used.
    
        If msg is present, include it in the printout as a message.
    
        If halt is True, a failed assertion causes an exception to be
        raised; if halt is False, the error message is printed to stderr and
        the function returns (this allows you to e.g. start a debugger).
 
        If debug is True, a failed assertion will drop you into the
        debugger.
        '''
        # fail will be None if all things compared are equal.  Otherwise,
        # it will be a list of error message strings detailing where the
        # comparison(s) failed.
        fail = None
        if not ii(a, str) and ii(a, Iterable):
            if reltol is None and abstol is None:
                # Compare them as objects.  Note they could be numpy
                # arrays.
                if have_numpy and type(a) == numpy.ndarray:
                    if any(a != b):
                        fail = []
                else:
                    if a != b:
                        fail = []
            else:
                # Sequences:  compare each corresponding element.  Note
                # dictionaries are sequences too and will be equal iff
                # they have the same key and value pairs.
                try:
                    for i, j in zip(a, b):
                        f = check_equal(i, j, reltol=reltol, abstol=abstol,
                                        use_min=use_min)
                        if f is not None:
                            if fail is not None:
                                fail += f
                            else:
                                fail = f
                except Exception:
                    m = "Could not pairwise compare a and b"
                    raise AssertionError(m)
        else:
            fail = check_equal(a, b, reltol=reltol, abstol=abstol, use_min=use_min)
        if fail is None:
            return      # a and b were equal
        else:
            arg_not_eq = "Arguments are not equal [pyver {}]:".format(python_version)
            try:
                # Assume they're sequences
                diff = [a[i] - b[i] for i in range(len(a))]
            except Exception:
                try:
                    # Assume they're numbers
                    diff = a - b
                except Exception:
                    # Should work for any other objects
                    fail += [
                        arg_not_eq,
                        f"  1st  = {a!r}",
                        f"  2nd  = {b!r}",
                    ]
                else:
                    try:
                        rel_diff_arg1 = diff/a
                    except Exception:
                        rel_diff_arg1 = None
                    try:
                        rel_diff_arg2 = diff/b
                    except Exception:
                        rel_diff_arg2 = None
                    fail += [
                        arg_not_eq,
                        f"  arg1 = {a!r}",
                        f"  arg2 = {b!r}",
                        f"  diff = {diff!r}",
                    ]
                    if rel_diff_arg1 is not None:
                        fail += [f"  diff/arg1 = {rel_diff_arg1!r}"]
                    if rel_diff_arg2 is not None:
                        fail += [f"  diff/arg2 = {rel_diff_arg2!r}"]
            else:
                fail += [
                    arg_not_eq,
                    f"  arg1 = {a!r}",
                    f"  arg2 = {b!r}",
                    f"  diff = {diff!r}",
                ]
        if msg:
            fail.append(msg)
        if halt:
            raise AssertionError("\n".join(fail))
        elif debug:
            breakpoint()
        else:
            print(fail, file=sys.stderr)
    def Assert(cond, debug=False):
        '''Similar to assert, but you'll be dropped into the debugger on an
        exception if debug is True, Assert.debug is True, or 'Assert' is
        a nonempty environment string.
        '''
        if not cond:
            if debug or Assert.debug or os.environ.get("Assert", ""):
                print("Type 'up' to go to line that failed", file=sys.stderr)
                breakpoint()
            else:
                raise AssertionError
    Assert.debug = False
if __name__ == "__main__":
    print(dedent(f'''
    lwtest:  Lightweight test framework -- typical usage:
        from lwtest import run, assert_equal, raises
        # Name your test functions e.g. "def Test_*()"
        if __name__ == "__main__":
            failed, messages = run(globals())
    
    run()'s keyword arguments (default value in square brackets):
        broken:   If True, testing is acknowledged to be broken and a warning
                  message to this effect is printed. [False]
        verbose:  Print the function names as they are executed. [False]
        halt:     Stop at the first failure.  [False]
        regexp:   Regular expression that identifies a test function.
                  ["{test_function_regexp}"]
        reopts:   Regular expression's options. [re.I]
        stream:   Where to send output [stdout].  None = no output.
    
    Utility functions:
        Check that two numbers are close:
            assert_equal(a, b, reltol=None, abstol=None, use_min=False)
        Check that something raises an exception:
            raises(exception_object, func, *p, **kw)
            raises(sequence_of_exception_objects, func, *p, **kw)
            with raises(exception_object):
                <code that must raise an exception>
        Send a colored reminder message to stdout:
            ToDoMessage(message, prefix="+", color="yel")
        Like assert, but puts you into the debugger with cmd line arg:
            Assert(condition)
        Both assert_equal and Assert also include a debug keyword argument
    '''[1:].rstrip()))
