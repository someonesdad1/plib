'''
Lightweight testrunner framework

from lwtest import run, raises, assert_equal, Assert, Debugger

def TestExample():
    f = lambda x: set(x)
    # Two ways to check for expected exceptions
    raises(TypeError, f, 1)
    with raises(ZeroDivisionError) as x:
        1/0
    Assert(x.value = "<class 'ZeroDivisionError'>")
    if 1:   # How to compare floating point numbers
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
    Finds test functions and execute them.  Its single argument must be a dictionary
    containing the names and their associated function objects.  Set verbose=True to see
    which functions will be executed and their execution order.

Assert() 
    Works like python's assert statement, but can drop you into the debugger if so
    instructed.  Type 'up' to go to the failed Assert() line.  Since dropping into the
    debugger is a common need, there are multiple ways:

        - Set the debug keyword to True
        - Include a command line argument
        - Set Assert.debug to True
        - Set the environment variable 'Assert' to the nonempty string

    Note Assert() and assert_equal() do not pay attention to __debug__, unlike
    python's assert statement.

ToDoMessage()
    Causes a colored message to be printed to stdout to remind you of something that
    needs to be done.

My motivation for generating this lightweight testrunner framework was my frustration
with the unittest module in conjunction with the way I develop code.  I write my unit
tests before or during code development and often need to drop into the debugger or add
a print statement to see what's going wrong.  The unittest module traps stdout and makes
this painful to do.  I liked some of the available testrunners like nose or pytest, but
I decided that if I was going to add a new dependency, it might as well be a dependency
I could tune to my own preferences.  The other major desire was to allow fairly
comprehensive coverage of comparing numerical results.

This tool was derived from some nice code by Raymond Hettinger 8 May 2008:
http://code.activestate.com/recipes/572194/.  I'm grateful Raymond put it out there for
other folks.
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Lightweight test runner oo>
        <oo desc ∞ This was derived from some nice code by Raymond Hettinger at
            http://code.activestate.com/recipes/572194/.  Downloaded 27 Jul 2014.
        oo>
        <oo copy ∞ Copyright © 2014 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ testdir oo>
        <oo todo ∞
        
            - ∞∞1 Assert, assert_equal, and the check_* functions can use debug.fln() to get
              the file and line number of the failed call
                - ∞∞2 Also look at including debug.py to print the details during an
                  unhandled exception (see 'Demonstrate an unhandled exception' in
                  debug.py's demo).  This would let you see the local variables on the
                  stack, which is what usually needs to be done (tediously) with the
                  debugger.
            
            - This file could have a function that would find all the functions and
              classes in a module, then compare the list to all the Test_* functions
              found.  If they don't match 1-to-1, then the module may be missing a test
              case.

            - https://pycodestyle.pycqa.org/en/latest/advanced.html#automated-tests
              tells how to add automated code style testing for conformance.  Add it to
              the self tests as an option to run.
            
            - If an argument passed on the command line is a directory, search it
              recursively for all files that appear to be test scripts and run them.
            
                - If a file is passed on the command line, search it for suitable test
                  functions and run them, even if there's no run() call in the script.
                  Options to provide run()'s features:  -h to halt at first failure, -r
                  for regexp to identify a test function, -R for regexp's options, -v
                  for verbose
                
            - Add a verbose keyword to run() which prints the file name and the
              function/class to be executed, like 'nosetests -v' does.  Another thing to
              consider would be to let run look at sys.argv and process options there in
              lieu of keywords (this would be handy for command line work, as the
              command line options would overrule the keywords).
        
        oo>
    '''
    if 1:  # Standard imports
        import collections
        import decimal
        import math
        import os
        import re
        import sys
        import time
        import traceback
    if 1:  # Custom imports
        import color
        import f
        import trm
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
    if 1:  # Global variables
        u = trm.Trm()
        u.got = u.grn1
        u.exp = u.orn
        u.msg = u.mag
        _modname = "<lwtest.py>"
        __all__ = '''
            Assert
            ToDoMessage
            assert_equal
            raises
            run
            id_test_function_regexp
        '''.split()
        ii = isinstance
        python_version = ".".join([str(i) for i in sys.version_info[:3]])
        # Regular expression to identify test functions
        id_test_function_regexp = "^Test_|_test$"
if 1:  # Core functionality
    def run(names_dict, **kw):
        '''Discover and run the test functions in the names_dict dictionary (name :
        function pairs).  Return (failed, s) where failed is an integer giving the
        number of failures that occurred and s is the information string that was sent
        (or would have been sent) to the stream.  A failure is an unhandled exception.
        
        Keyword options [default]:
            broken:     If True, testing code is acknowledged to be broken; a warning 
                        message is printed and tests are not run.  [False]
            dbg:        If True, don't handle exceptions (allows you to trap them in a
                        debugger).  Also can set the environment variable 'dbg' to do
                        this. [False]
            verbose:    Print the function names as they are executed. [False]
            halt:       Stop at the first failure.  [False]
            quiet:      If True, no output.  [False]
            regexp:     Regular expression that identifies a test function.
                        Default is in global variable id_test_function_regexp.
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
        regexp = kw.get("regexp", id_test_function_regexp)
        stream = kw.get("stream", sys.stdout)
        nomsg = kw.get("nomsg", False)
        # If broken, print error message and return
        if broken:
            # Get the name of the file that called us
            file = traceback.extract_stack()[0][0]
            u.print(f"{u.orn}{_modname}! {file}:  Error:  tests are broken")
            return (1, "Tests are broken")
        # Find test functions in names_dict to run.  Note we don't allow
        # "_lwtest" to end the name; this lets you use a variable like
        # _have_lwtest in a script.
        istest = re.compile(regexp, reopts)
        tests = [
            (name, func)
            for name, func in names_dict.items()
            if istest.search(name) and not name.endswith("_lwtest")
        ]
        # Reverse the list so they can be popped in alphabetical order
        tests = sorted(tests, reverse=True)
        try:
            filename = names_dict["__file__"]
        except KeyError:
            # Use the current file's name; put angle brackets around it to
            # indicate it might not be the correct file (e.g., the user
            # manually invoked run() with a hand-crafted dictionary and
            # forgot to add a "__file__" key).
            filename = "<__file__ ?>"
        pass_count = fail_count = 0
        fail_messages = []
        if verbose:
            print("{} Test functions in {}:".format(_modname, filename), file=stream)
        nl = "\n"
        start_time = time.time()
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
                    print(f"∞∞2 {_modname}:  need to test TypeError catch")
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
        stop_time = time.time()
        output = (
            nl.join(fail_messages)
            if fail_messages
            else "{}:  {} {} passed in {} [python {}]".format(
                filename,
                pass_count,
                "test" if pass_count == 1 else "tests",
                GetTime(stop_time - start_time),
                python_version,
            )
        )
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
            '''Initialize with one exception object or a sequence of
            exception objects
            '''
            if issubclass(ExpectedExceptions, BaseException):
                self.expected = set([ExpectedExceptions])
                return
            elif not issubclass(ExpectedExceptions, collections.abc.Iterable):
                m = "ExpectedExceptions must be a container of Exceptions"
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
if 1:  # Utility
    def GetTime(duration_s):
        if duration_s > 3600:
            return f"{duration_s/3600:.3f} hr"
        elif duration_s > 60:
            return f"{duration_s/60:.2f} min"
        else:
            return f"{duration_s:.2f} s"
    def ToDoMessage(message, prefix="+ ", color=u.orn):
        '''This function results in a message to stdout; its purpose is to
        allow you to see something that needs to be done, but won't cause
        the test to fail.  The message is decorated with a leading prefix
        string and the file and line number.  If color is not None, then it
        must either be a string naming a color (see color.py) or a Color
        class instance.  The message is printed in this color.
        '''
        fn, ln, method, call = traceback.extract_stack()[-2]
        c = u(color) if color is not None else ""
        vars = {
            "fn": fn,
            "ln": ln,
            "method": method,
            "msg": message,
            "prefix": prefix,
            "c": c,
            "n": u.n,
        }
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
if 1:  # Checking functions
    def check_flt(a, b, reltol=None, abstol=None, use_min=False):
        '''a must be a flt.  If b is not a flt, then convert it if
        possible.
        '''
        assert ii(a, f.flt)
        return check_float(
            float(a), float(b), reltol=reltol, abstol=abstol, use_min=use_min
        )
    def check_cpx(a, b, reltol=None, abstol=None, use_min=False):
        '''a must be a cpx.  If b is not a cpx, then convert it if
        possible.
        '''
        assert ii(a, f.cpx)
        return check_complex(
            complex(a), complex(b), reltol=reltol, abstol=abstol, use_min=use_min
        )
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
        if (math.isnan(a) and not math.isnan(b)) or (not math.isnan(a) and math.isnan(b)):
            fail = []
        if (math.isinf(a) and not math.isinf(b)) or (not math.isinf(a) and math.isinf(b)):
            fail = []
        sign_a, sign_b = math.copysign(1.0, a), math.copysign(1.0, b)
        if math.isinf(a) and math.isinf(b):
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
        if not ii(a, decimal.Decimal):
            raise ValueError("a needs to be a Decimal")
        if not ii(b, decimal.Decimal):
            # Convert b to Decimal
            try:
                b = decimal.Decimal(str(b))
            except Exception:
                raise ValueError("b must be convertible to a Decimal")
        # Handle NaN and infinite values
        if (a.is_nan() and not b.is_nan(b)) or (not a.is_nan() and b.is_nan()):
            fail = []
        if (a.is_infinite() and not b.is_infinite()) or (
            not a.is_infinite() and b.is_infinite()
        ):
            fail = []
        sign_a, sign_b = a.copy_sign(decimal.Decimal(1)), b.copy_sign(decimal.Decimal(1))
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
                D, zero = decimal.Decimal, decimal.Decimal(0)
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
        fail = check_float(
            a.real, b.real, reltol=reltol, abstol=abstol, use_min=use_min
        )
        f = check_float(a.imag, b.imag, reltol=reltol, abstol=abstol, use_min=use_min)
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
            if ii(a, f.flt):
                fail = check_flt(a, b, reltol=R, abstol=A, use_min=U)
            elif ii(a, (int, float)):
                fail = check_float(a, b, reltol=R, abstol=A, use_min=U)
            elif ii(a, complex):
                fail = check_complex(a, b, reltol=R, abstol=A, use_min=U)
            elif ii(a, decimal.Decimal):
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
    def assert_equal(a, b, reltol=None, abstol=None, use_min=False, msg="", halt=True, debug=False):
        '''Raise an AssertionError if a != b.  a and b can be objects, numbers, or
        sequences of numbers (sequence elements are compared pairwise), or dictionaries.
        reltol and abstol are the relative and absolute tolerances.  No exception will
        be raised if for each number element (if a is zero, reltol*b is used instead)
                abs(a - b) <= reltol*a
        or
                abs(a - b) <= abstol
        If both abstol and reltol are defined, the one with the larger tolerance range
        will be used unless use_min is True, in which case the smaller tolerance will be
        used.
        
        If msg is present, include it in the printout as a message.
        
        If halt is True, a failed assertion causes an exception to be raised; if halt is
        False, the error message is printed to stderr and the function returns (this
        allows you to e.g. start a debugger).
        
        If debug is True, a failed assertion will drop you into the debugger.
        '''
        # fail will be None if all things compared are equal.  Otherwise,
        # it will be a list of error message strings detailing where the
        # comparison(s) failed.
        fail = None
        if not ii(a, str) and ii(a, collections.abc.Iterable):
            if reltol is None and abstol is None:
                # Compare them as objects.  Note they could be numpy
                # arrays.
                if have_numpy and type(a) is numpy.ndarray:
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
                        f = check_equal(
                            i, j, reltol=reltol, abstol=abstol, use_min=use_min
                        )
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
            return  # a and b were equal
        else:
            arg_not_eq = f"{u.msg}Arguments are not equal [pyver {python_version}]{u.n}:"
            try:
                # Assume they're sequences
                diff = [a[i] - b[i] for i in range(len(a))]
            except Exception:
                try:
                    # Assume they're numbers
                    diff = a - b
                except Exception:
                    # Should work for any other objects
                    fail += [arg_not_eq, f"  1st  = {a!r}", f"  2nd  = {b!r}", ]
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
                        f"{u.got}  got      = {a!r}{u.n}",
                        f"{u.exp}  expected = {b!r}{u.n}",
                        f"  diff = {diff!r}",
                    ]
                    if rel_diff_arg1 is not None:
                        fail += [f"  diff/got      = {rel_diff_arg1!r}"]
                    if rel_diff_arg2 is not None:
                        fail += [f"  diff/expected = {rel_diff_arg2!r}"]
            else:
                fail += [
                    arg_not_eq,
                    f"{u.got}  got      = {a!r}{u.n}",
                    f"{u.exp}  expected = {b!r}{u.n}",
                    f"  diff = {diff!r}",
                ]
        if msg:
            fail.append(msg)
        if halt:
            raise AssertionError("\n".join(fail))
        elif debug:
            breakpoint()
        else:
            print(_modname, fail, file=sys.stderr)
    def Assert(condition, msg="", debug=False):
        '''Replacement for assert but it can't be optimized out.  If debug is True, Assert.debug is
        True, or 'Assert' is a nonempty environment string, you'll be dropped into a debugger.  If
        msg is not empty, it's printed out.
        '''
        if not hasattr(Assert, "debug"):
            Assert.debug = False
        if not condition:
            if debug or Assert.debug or os.environ.get("Assert", ""):
                # Print colorized message to stdout and start debugger
                if msg:
                    u.print(f"{u.mag}{_modname} {msg}", file=sys.stderr)
                print("Type 'up' to go to line that failed", file=sys.stderr)
                breakpoint()
            else:
                raise AssertionError(msg)
if 1:  # Testing functions
    def Test_Raises():
        f = lambda x: 1/x
        # Function call & object instantiation semantics
        raises(ZeroDivisionError, f, 0)
        try:
            raises(RuntimeError, f, 1)
        except AssertionError:
            pass
        else:
            raise Exception("Bug!")
        class A:
            def __init__(self):
                raise RuntimeError
        raises(RuntimeError, A)
    def Test_RaisesContextManager():
        f = lambda x: 1/x
        with raises(ZeroDivisionError):
            f(0)
        with raises(ZeroDivisionError) as x:
            assert x is not None
            f(0)
        Assert(x.value == "<class 'ZeroDivisionError'>")
        try:
            with raises(ZeroDivisionError):
                f(1)
        except AssertionError:
            pass
        else:
            raise Exception("Bug!")
    def Test_AssertEqual():
        """Demonstrate that the assert_equal function can detect equal and
        non-equal objects for the following types:
            Numbers
                integers
                floats
                Decimals
                complex
            Sequences of numbers
            Arbitrary objects that can be compared
        """
        E = AssertionError
        # Numbers
        x = 0.0
        assert_equal(int(x), int(x))
        raises(E, assert_equal, int(x), int(x) + 1)
        assert_equal(x, x)
        raises(E, assert_equal, x, x + 1.0)
        x, y = "0.0", "1.0"
        assert_equal(decimal.Decimal(x), decimal.Decimal(x))
        raises(E, assert_equal, decimal.Decimal(x), decimal.Decimal(y))
        x, y = 1 + 1j, 1 + 2j
        assert_equal(x, x)
        raises(E, assert_equal, x, x + 1.0)
        if have_mpmath:
            x = mpmath.mpf("1.0")
            assert_equal(x, x)
            raises(E, assert_equal, x, x + 1.0)
        # Sequences of numbers
        x = [1.0, 2.0]
        y = [int(i) for i in x]
        assert_equal(y, y)
        raises(E, assert_equal, y, [i + 1 for i in y])
        assert_equal(x, x)
        raises(E, assert_equal, x, [i + 1 for i in x])
        x = [decimal.Decimal("1.0"), decimal.Decimal("2.0")]
        assert_equal(x, x)
        raises(E, assert_equal, x, [i + 1 for i in x])
        x = [1 + 1j, 1 + 2j]
        assert_equal(x, x)
        raises(E, assert_equal, x, [i + 1 for i in x])
        if have_mpmath:
            x = [mpmath.mpf("1.0"), mpmath.mpf("1.0")]
            assert_equal(x, x)
            raises(E, assert_equal, x, [i + 1 for i in x])
        if have_numpy:
            x = numpy.array([1.0, 1.0])
            assert_equal(x, x)
            raises(E, assert_equal, x, x + 1)
        # -----------------
        # abstol
        x, eps = 1, 1e-15
        assert_equal(x, x + eps, abstol=2*eps)
        raises(E, assert_equal, x, x + eps, abstol=eps)
        # Check things work if one argument is zero
        x, eps = 0, 1e-15
        assert_equal(0, eps, abstol=2*eps)
        assert_equal(eps, 0, abstol=2*eps)
        # -----------------
        # reltol
        x, tol, eps = 1, 0.01, 1e-15
        assert_equal(x, x*(1 + tol - eps), reltol=tol)
        raises(E, assert_equal, x, x*(1 + tol), reltol=tol)
        # reltol & abstol both defined, use_min=True
        assert_equal(x, x*(1 + tol - eps), reltol=tol, abstol=0)  # Passes
        raises(
            E, assert_equal, x, x*(1 + tol - eps), reltol=tol, abstol=0, use_min=True
        )  # Catches failure
        # Check things work if one argument is zero
        assert_equal(0, 1, reltol=1)
        assert_equal(1, 0, reltol=1)
        # ----- Other objects -----
        # Strings
        x = "a string"
        assert_equal(x, x)
        raises(E, assert_equal, x, x[:-1])
        # Classes and instances
        class A:
            pass
        class B:
            pass
        a, b = A(), B()
        assert_equal(a, a)
        assert_equal(A, A)
        raises(E, assert_equal, a, b)
        raises(E, assert_equal, A, B)
        # Functions
        assert_equal(Test_Raises, Test_Raises)
        raises(E, assert_equal, Test_Raises, assert_equal)
    def Test_flt_cpx():
        x, z = f.flt(0), f.cpx(0)
        with x:
            a, b = f.flt(1), f.flt(1)
            assert_equal(a, b)
            b = 1.0
            assert_equal(a, b)
        with z:
            a, b = f.cpx(1 + 1j), f.cpx(1 + 1j)
            assert_equal(a, b)
            b = 1 + 1j
            assert_equal(a, b)
    def Test_Run():
        def TestA():
            raise ValueError()
        def TestB():
            raise ValueError()
        def testA():
            raise ValueError()
        st, d = StringIO(), {"TestA": TestA, "TestB": TestB, "testA": testA}
        # Test halt keyword
        failed, messages = run(d, stream=None, halt=True)
        assert messages.split("\n")[0] == "TestA failed:  ValueError()"
        # Test that run has two failures
        failed, messages = run(d, stream=None)
        m1, m2 = "TestA failed:", "TestB failed:"
        assert m1 in messages and m2 in messages
        # Show regexp change results in only one function being run
        failed, messages = run(d, stream=None, regexp="^TestA$")
        assert m1 in messages and m2 not in messages
        # Change to a case sensitive search
        st = StringIO()
        failed, messages = run(d, stream=st, regexp="^testA$", reopts=0)
        s = st.getvalue().strip().split("\n")
        assert s[0] == "testA failed:  ValueError()"
        assert m1 not in messages and m2 not in messages
    def Test_ToDoMessage():
        ToDoMessage("Simulated to-do message")
        ToDoMessage("Simulated to-do message in color", color="yel")

if __name__ == "__main__":
    if 1:  # Standard imports
        import sys
        from io import StringIO
    if 1:  # Custom imports
        from lwtest import run, raises, assert_equal, Assert, ToDoMessage
        import wrap
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
    def ShowUsage():
        u.k = u.sky
        u.d = u.grn1
        u.u = u.lavl
        print(wrap.dedent(f'''
        {u.yel}lwtest:  Lightweight test framework -- typical usage:{u.n}
            from lwtest import run, assert_equal, raises, Assert
            # Name your test functions e.g. "def Test_*()"
            if __name__ == "__main__":
                {u.orn}num_failed, messages = run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0){u.n}
                  or
                {u.mag}exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0]){u.n}
            
                {u.k}broken{u.n}      If True, testing code is acknowledged to be broken; a warning
                            message is printed and tests are not run.  [{u.d}False{u.n}]
                {u.k}dbg{u.n}         If True, don't handle exceptions (allows you to trap them in a
                            debugger).  Also can set the environment variable 'dbg' to do
                            this. [{u.d}False{u.n}]
                {u.k}verbose{u.n}     Print the function names as they are executed.  [{u.d}False{u.n}]
                {u.k}halt{u.n}        Stop at the first failure.  [{u.d}False{u.n}]
                {u.k}quiet{u.n}       If True, no output.  [{u.d}False{u.n}]
                {u.k}regexp{u.n}      Regular expression that identifies a test function.  Default
                            is [{u.d}{id_test_function_regexp}{u.n}]
                {u.k}reopts{u.n}      Regular expression's options. [{u.d}re.I{u.n}]
                {u.k}stream{u.n}      Where to send output [{u.d}stdout{u.n}].  None = no output.
                {u.k}nomsg{u.n}       If True, return only the integer 'num_failed'.
            
                exit(num_failed)      # Nonzero status if 1 or more unhandled exceptions
        
        Utility functions:
            Check that two numbers are close:
                {u.u}assert_equal{u.n}(a, b, reltol=None, abstol=None, use_min=False)
            Check that something raises an exception:
                {u.u}raises{u.n}(exception_object, func, *p, **kw)
                {u.u}raises{u.n}(sequence_of_exception_objects, func, *p, **kw)
                with {u.u}raises{u.n}(exception_object):
                    <code that must raise an exception>
            Send a colored reminder message to stdout:
                {u.u}ToDoMessage{u.n}(message, prefix="+", color="yel")
                
            {u.u}Assert{u.n}(condition, msg="", debug=False)
                Is like assert but can't be optimized out.  The debug keyword argument if True drops
                you into the debugger if condition is False (type 'u' to go to the line that failed)
                and msg is printed in color to stderr.  You can also get this behavior if the
                environment variable Assert is not empty.
        '''[1:].rstrip()))
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        exit(run(globals(), halt=1)[0])
    else:
        ShowUsage()
