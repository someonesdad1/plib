'''
TODO

    - Get rid of sig and use flt
        - Note:  putting sides of 1, 1, 1e-8 results in a division by zero
          exception because the area evaluates to zero.  Thus, it would be
          better to perform the calculations with Decimal or mpmath numbers,
          rounding to the needed figures at the end.
    - Uncertainies:  Enable explicitly with -u option
        - Allow a+-b, a+/-b, a(b) for uncertainties
        
Solve a triangle
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2013 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Solve a triangle
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        import sys
        import os
        import getopt
        from decimal import Decimal, localcontext
        from pdb import set_trace as xx
        from pprint import pprint as pp
    if 1:  # Custom imports
        import decimalmath as DM
        from f import flt
        from wrap import dedent
        from color import t
        if 1:  # xx
            try:
                # If you wish to add uncertainties to numbers, you'll need to install
                # the uncertainties library from
                # http://pypi.python.org/pypi/uncertainties/.
                from uncertainties import ufloat, AffineScalarFunc
                from uncertainties.umath import asin, acos, sqrt, sin, cos
                have_unc = True
            except ImportError:
                from math import acos, sqrt, sin, cos
                have_unc = False
        if 0:  # xx
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        ii = isinstance
        class g:
            pass
        t.i = t.cynl
        t.norm = t.wht
    class CannotBeZero(Exception):  # Flags a bad numerical condition
        pass
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] datafile
          Solve a triangle given the requisite sides and angles.  Here, "solving"
          means that the three angles and three sides of the triangle will be
          printed in the report.
        Options:
          -d n  Set the number of significant digits for the report [{d["-d"]}]
          -e    Show input parameters from datafile
          -i    Solve problem interactively by prompting for needed information
          -h    Print more detailed instructions
          -s    Print a sample datafile
          -t    Run self-tests
        '''))
        exit(status)
    def Manpage():
        print(dedent(f'''
        The datafile's lines must be of the following types:
        
            Specify angle measure:      deg (default) or rad
            Specify problem:            sss, ssa, sas, saa, asa
            Variable assignment:        var = value 
            Sides:                      S1 = value, S2 = value, S3 = value
            Angles:                     A1 = value, A2 = value, A3 = value
         
        Angle A1 is opposite side S1, etc.  Blank lines and lines that begin with a '#'
        after leading whitespace is removed are ignored.  Expressions are allowed and
        the math module's symbols are in scope.  Don't use variable names that start
        with double underscores.
        
        You must give the following quantities for the problem:
        
            sss:        S1, S2, S3
            ssa:        S1, S2, A1
            sas:        S1, S2, A3
            saa:        S1, A2, A3
            asa:        A1, S2, A3
            
        Example:  The following data file will show the solution of an
        equilateral triangle:
            sss
            S1 = 1
            S2 = 1
            S3 = 1
         
        For uncertainty calculations to work, you'll have to install the python
        uncertainties module from http://pypi.python.org/pypi/uncertainties/.  If it's
        not installed, any provided uncertainties will be ignored.
        
        ''')
        )
        exit(0)
    def ParseCommandLine():
        d["-d"] = 3
        d["-e"] = False  # Echo input values
        d["-h"] = False  # Show manpage
        d["-i"] = False  # Use interactive prompts to get data
        d["-s"] = False  # Print sample datafile
        d["-t"] = False  # Run self tests
        # Use degrees as the default angle measure.  If you want to use
        # radians as the default, change this to False.
        d["deg"] = True
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "d:ehist")
        except getopt.GetoptError as e:
            msg, option = e
            print(msg)
            exit(1)
        for o, a in optlist:
            if o[1] in "ehist":
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d["-d"] = int(a)
                    if d["-d"] < 1:
                        raise Exception()
                except Exception:
                    Error("-d option must be integer > 0")
        if d["-h"]:
            Manpage()
        elif d["-t"]:
            Test()
        elif d["-s"]:
            Datafile()
        if not args and not d["-i"]:
            Usage()
        return args
if 1:  # Core functionality
    def Datafile():
        print(
            dedent(f'''
        # Sample datafile
        # Specify angle measure:  deg (default) or rad
        # Specify problem:  sss, ssa, sas, saa, asa
        # Variable assignment:  var = value
        # Sides:    S1, S2, S3
        # Angles:   A1, A2, A3
        
        # This example is nearly an equilateral triangle
        sss
        S1 = 1
        S2 = 1
        S3 = 1.2
        
        # Results:
        # Triangle solution (to 3 figures):
        # Sides                     1               1               1.2            
        # Angles                    53.2°           53.2°           73.2°          
        # Area                      0.479
        # Perimeter                 3.2
        # Inscribed circle¹         r = 0.299, d = 0.598
        # Circumscribed circle²     r = 0.625, d = 1.25
        # ¹ Center located by angle bisectors.
        # ² Center located by perpendicular bisectors of the sides.
        ''')
        )
        exit(0)
    def CleanDict(vars):
        '''vars is a dictionary of local variables.  Remove all variable
        names that begin with an underscore and also remove __d and return the
        remaining dictionary.
        '''
        v = vars.copy()
        try:
            del v["__d"]
        except KeyError:
            pass
        keys = list(v.keys())
        rm = []
        for k in keys:
            if len(k) > 1 and k.startswith("_"):
                rm.append(k)
        for i in rm:
            del v[i]
        return v
    def InterpretNum(s, vars):
        '''s is a number string or expression.  Evaluate the string and
        return a Decimal number.  Raise an exception if the number is 0 or
        less.
        '''
        # Get vars into our local namespace
        for k in vars:
            exec("%s = vars['%s']" % (k, k))
        try:
            # See if it can be interpreted as a number directly
            x = Decimal(s)
            if x <= 0:
                raise CannotBeZero("Value must be greater than zero")
            return x
        except CannotBeZero:
            Error(f"'{s}' must be > 0")
        except Exception:
            pass
        try:
            # It's not a number, so see if it's an expression
            x = Decimal(eval(s))
            if x <= 0:
                raise CannotBeZero("Value must be greater than zero")
            return x
        except Exception as e:
            Error("Can't evaluate '%s'\n  Error:  %s" % (s, str(e)))
    def GetDataInteractively():
        '''Note:  local variables are named with two leading underscores to allow them 
        to not be confused with the variables the user types in.
        '''
        t.print(f"{t.sky}Triangle solving utility\n")
        __d = d
        if 1:   # Set to 0 for debugging interactive input
            while True:
                __v = input(f"Number of significant digits to display [{flt(0).N}]: ")
                __v = __v.strip()
                if __v in ("q", "Q"):
                    exit(0)
                if not __v:
                    break
                else:
                    try:
                        __x = int(__v)
                        if not (1 <= __x <= 15):
                            raise Exception()
                        sig.digits = __x
                        break
                    except Exception as e:
                        print("Must be an integer between 1 and 15")
            while True:
                __v = input("Degrees [d] or radians (r) for angle measure: ")
                __v = __v.strip()
                if __v in ("q", "Q"):
                    exit(0)
                elif __v in ("d", "D", ""):
                    __d["deg"] = True
                    print("  --> Using degrees")
                    break
                elif __v in ("r", "R"):
                    __d["deg"] = False
                    print("  --> Using radians")
                    break
                else:
                    print("Improper response -- must be 'd' or 'r'")
            print(
                dedent('''
            Enter the type of problem you want solved [sss]:
            sss:  Given three sides
            ssa:  Given two sides and an angle not between the two sides
            sas:  Given two sides and angle between the two sides
            saa:  Given one side, one angle opposite, and one angle adjacent
            asa:  Given one side and the two angles on either side of it''')
            )
            while True:
                __prob = input("Problem?  ")
                __prob = __prob.strip().lower()
                if __prob in ("q", "Q"):
                    exit(0)
                if not __prob:
                    __d["problem_type"] = "sss"
                    __prob = "sss"
                    print("  --> Solving sss problem")
                    break
                if __prob not in ("sss", "ssa", "sas", "saa", "asa"):
                    print("Improper problem abbreviation")
                    continue
                else:
                    __d["problem_type"] = __prob
                    break
            __need = {
                # Encodes the number of sides and number of angles to prompt for
                "sss": (3, 0),
                "ssa": (2, 1),
                "sas": (2, 1),
                "saa": (1, 2),
                "asa": (1, 2),
            }
            # Get sides
            for __i in range(1, __need[__prob][0] + 1):
                while True:
                    __v = input("Enter length of side %d:  " % __i)
                    __v = __v.strip()
                    if __v in ("q", "Q"):
                        exit(0)
                    elif "=" in __v:
                        try:
                            exec(__v)
                            print("Assignment OK")
                        except Exception as e:
                            print("Assignment failed:  %s" % str(e))
                    else:
                        try:
                            __x = InterpretNum(__v, CleanDict(locals()))
                            exec("S%d = __x" % __i)
                            break
                        except Exception as e:
                            print("Number not correct:  %s" % str(e))
            # Get angles.  Note we'll return the numbers the user typed in.
            for __i in range(1, __need[__prob][1] + 1):
                while True:
                    __v = input("Enter angle %d:  " % __i)
                    __v = __v.strip()
                    if __v in ("q", "Q"):
                        exit(0)
                    elif "=" in __v:
                        try:
                            exec(__v)
                            print("Assignment OK")
                        except Exception as e:
                            print("Assignment failed:  %s" % str(e))
                    else:
                        try:
                            __x = InterpretNum(__v, CleanDict(locals()))
                            exec("A%d = __x" % __i)
                            break
                        except Exception as e:
                            print("Number not correct:  %s" % str(e))
            __d["vars"] = CleanDict(locals())
        else:
            # For debugging:  sss problem with sides 3, 4, 5
            __d["problem_type"] = "sss"
            __d["vars"] = {'S1': Decimal('3'), 'S2': Decimal('4'), 'S3': Decimal('5')}
        print()
    def ReadDatafile(datafile):
        if d["-e"]:
            t.print(f"{t.i}Problem's lines from datafile:")
        def PrintLine():
            if d["-e"]:
                t.print(f"    {t.i}{_line}")
        _lines = [i.strip() for i in open(datafile).readlines()]
        try:
            for _i, _line in enumerate(_lines):
                _linenum = _i + 1
                if not _line or _line[0] == "#":
                    continue
                if "=" not in _line:
                    if _line == "deg":
                        d["deg"] = True
                    elif _line == "rad":
                        d["deg"] = False
                    elif _line in ("sss", "ssa", "sas", "asa", "saa"):
                        d["problem_type"] = _line
                    else:
                        raise Exception("Line not an assignment or keyword")
                    PrintLine()
                    continue
                _f = [j.strip() for j in _line.split("=")]
                if len(_f) > 2:
                    raise Exception("Too many '=' signs")
                _name, _value = _f
                # Get the variable into our local namespace
                _x = InterpretNum(_value, locals())
                exec(f"{_name} = _x")
                if _name in "S1 S2 S3 A1 A2 A3".split():
                    PrintLine()
        except Exception as e:
            msg = "Line %d is bad in datafile '%s'\n" % (_linenum, datafile)
            msg += "  Line:  '%s'\n" % _line
            msg += "  Error:  %s" % str(e)
            Error(msg)
        # Set d["vars"] to the defined variables
        d["vars"] = CleanDict(locals())
        del d["vars"]["datafile"]
    def SolveProblem():
        "Note the solution is done with Decimal arithmetic"
        # Get our needed variables
        v = d["vars"].get
        S1 = v("S1", 0)
        S2 = v("S2", 0)
        S3 = v("S3", 0)
        A1 = v("A1", 0)
        A2 = v("A2", 0)
        A3 = v("A3", 0)
        # Function to convert angle measure to radians if needed
        f = lambda x: DM.pi() * x / 180 if d["deg"] else x
        prob = d["problem_type"]
        pi = DM.pi()
        try:
            if prob == "sss":
                # Law of cosines to find two angles, angle law to find third.
                A1 = DM.acos((S2**2 + S3**2 - S1**2) / (2 * S2 * S3))
                A2 = DM.acos((S1**2 + S3**2 - S2**2) / (2 * S1 * S3))
                A3 = pi - A1 - A2
            elif prob == "ssa":
                # Law of sines to find the other two angles and remaining
                # side.  Note it can have two solutions (the second solution's
                # data will be in the variables S1_2, S2_2, etc.).
                A1 = f(A1)  # Make sure angle is in radians
                arg = S2 / S1 * DM.sin(A1)
                if abs(arg) > 1:
                    print("No solution:  sine law gives asin argument > 1")
                    print(f"  S1 = {S1}")
                    print(f"  S2 = {S2}")
                    print(f"  A1 = {A1} radians = {A1 * 180 / pi}°")
                    exit(1)
                A2 = DM.asin(arg)
                A3 = pi - A1 - A2
                S3 = S2 * DM.sin(A3) / DM.sin(A2)
                # Check for other solution
                A1_2 = A1
                A2_2 = pi - A2
                A3_2 = pi - A1_2 - A2_2
                if A1_2 + A2_2 + A3_2 > pi:
                    # Second solution not possible
                    del A1_2
                    del A2_2
                    del A3_2
                else:
                    # Second solution is possible
                    S1_2 = S1
                    S2_2 = S2
                    S3_2 = S2_2 * DM.sin(A3_2) / DM.sin(A2_2)
            elif prob == "sas":
                # Law of cosines to find third side; law of sines to find
                # another angle; angle law for other angle.  Note we rename
                # the incoming angle to be consistent with a solution diagram.
                A3 = f(A1)  # Make sure angle is in radians
                S3 = DM.sqrt(S1**2 + S2**2 - 2 * S1 * S2 * DM.cos(A3))
                A2 = DM.asin(S2 * DM.sin(A3) / S3)
                A1 = pi - A2 - A3
            elif prob == "asa":
                # Third angle from angle law; law of sines for other two
                # sides.  Note we rename the sides for consistency with a
                # diagram.
                A1 = f(A1)  # Make sure angle is in radians
                A2 = f(A2)  # Make sure angle is in radians
                A3 = pi - A1 - A2
                S3 = S1
                S2 = S3 * DM.sin(A2) / DM.sin(A3)
                S1 = S3 * DM.sin(A1) / DM.sin(A3)
            elif prob == "saa":
                # Third angle from angle law; law of sines for other two
                # sides.
                A1 = f(A1)  # Make sure angle is in radians
                A2 = f(A2)  # Make sure angle is in radians
                A3 = pi - A1 - A2
                S2 = S1 * DM.sin(A2) / DM.sin(A1)
                S3 = S1 * DM.sin(A3) / DM.sin(A1)
            else:
                raise ValueError("Bug:  unrecognized problem")
        except UnboundLocalError as e:
            s = str(e)
            loc = s.find("'")
            s = s[loc + 1 :]
            loc = s.find("'")
            s = s[:loc]
            Error("Variable '%s' not defined" % s)
        except ValueError as e:
            msg = "Can't solve the problem:\n"
            msg += "  Error:  %s" % str(e)
            Error(msg)
        # Collect solution information
        solution = {}
        vars = set(
            (
                "S1",
                "S2",
                "S3",
                "A1",
                "A2",
                "A3",
                "S1_2",
                "S2_2",
                "S3_2",
                "A1_2",
                "A2_2",
                "A3_2",
            )
        )
        for k in vars:
            try:
                exec(f"solution['{k}'] = {k}", None, locals())
            except NameError:
                # Second solution variables not present unless ssa problem
                if prob == "ssa":
                    pass
        d["solution"] = solution
        CheckSolution()
    def CheckSolution():
        '''Check solution for reasonableness.  If one angle is zero, then the
        problem is degenerate (like sss with sides of 1, 2, 3).  If any side
        or angle is negative, the problem doesn't have a solution.
        '''
        S = d["solution"]
        no_solution = "Problem has no solution"
        S1, S2, S3, A1, A2, A3 = [S[i] for i in "S1 S2 S3 A1 A2 A3".split()]
        # Check for a side or angle being zero
        s = sum([S1 == 0, S2 == 0, S3 == 0])
        a = sum([A1 == 0, A2 == 0, A3 == 0])
        if s == 1:
            print("Problem is degenerate (one side is zero)")
            exit(1)
        elif s > 1:
            print(no_solution)
            exit(1)
        if a == 1:
            print("Problem is degenerate (one angle is zero)")
            exit(1)
        elif a > 1:
            print(no_solution)
            exit(1)
        # Check for a side or angle being negative
        s = sum([S1 < 0, S2 < 0, S3 < 0])
        a = sum([A1 < 0, A2 < 0, A3 < 0])
        if s:
            print("Problem has no solution:  a side is negative")
            exit(1)
        if a:
            print("Problem has no solution:  an angle is negative")
            exit(1)
    def Test():
        '''The following test cases came from the sample problems at
        http://www.mathsisfun.com/algebra/trig-solving-triangles.html
        '''
        eps = 1e-14
        pi = DM.pi()
        radians = lambda x: x * pi / 180
        d["angle_measure"] = radians(1)
        # sss
        d["vars"] = {
            "S1": 6,
            "S2": 7,
            "S3": 8,
        }
        d["problem_type"] = "sss"
        SolveProblem()
        k = d["solution"]
        assert abs(k["A1"] - DM.acos(77 / 112)) < eps
        assert abs(k["A2"] - (pi - k["A3"] - k["A1"])) < eps
        assert abs(k["A3"] - DM.acos(1 / 4)) < eps
        # ssa
        d["vars"] = {
            "S1": 8,
            "S2": 13,
            "A1": 31,  # Angle in degrees
        }
        d["problem_type"] = "ssa"
        SolveProblem()
        k = d["solution"]
        a2 = DM.asin(13 * sin(radians(31)) / 8)
        assert abs(k["A2"] - a2) < eps
        a3 = pi - k["A2"] - k["A1"]
        assert abs(k["A3"] - a3) < eps
        assert abs(k["S3"] - DM.sin(a3) * 8 / DM.sin(radians(31))) < eps
        # Check other solution
        a2_2 = pi - DM.asin(13 * DM.sin(radians(31)) / 8)
        assert abs(k["A2_2"] - a2_2) < eps
        a3_2 = pi - k["A2_2"] - k["A1_2"]
        assert abs(k["A3_2"] - a3_2) < eps
        assert abs(k["S3_2"] - DM.sin(a3_2) * 8 / DM.sin(radians(31))) < eps
        # sas
        d["vars"] = {
            "S1": 5,
            "S2": 7,
            "A1": 49,  # Angle in degrees
        }
        d["problem_type"] = "sas"
        SolveProblem()
        k = d["solution"]
        # asa
        d["vars"] = {
            "S1": 9,
            "A1": 76,  # Angle in degrees
            "A2": 34,  # Angle in degrees
        }
        d["problem_type"] = "asa"
        SolveProblem()
        k = d["solution"]
        assert abs(k["S2"] - 9 * DM.sin(radians(34)) / DM.sin(radians(70))) < eps
        assert abs(k["S1"] - 9 * DM.sin(radians(76)) / DM.sin(radians(70))) < eps
        assert abs(k["A3"] - radians(70)) < eps
        # saa
        d["vars"] = {
            "S1": 7,
            "A1": 62,  # Angle in degrees
            "A2": 35,  # Angle in degrees
        }
        d["problem_type"] = "saa"
        SolveProblem()
        k = d["solution"]
        assert abs(k["A3"] - radians(83)) < eps
        assert abs(k["S2"] - 7 * DM.sin(radians(35)) / DM.sin(radians(62))) < eps
        assert abs(k["S3"] - 7 * DM.sin(radians(83)) / DM.sin(radians(62))) < eps
        print("Tests passed")
        exit(0)
    def GetOtherFacts(s1, s2, s3, a1, a2, a3, d):
        '''Calculate the other relevant measures of the triangle.'''
        A = s1 * s2 * DM.sin(a3) / 2
        s = (s1 + s2 + s3) / 2
        r = A / s
        R = s1 * s2 * s3 / (4 * A)
        d["area"] = A
        d["perimeter"] = 2 * s
        d["r_inscribed"] = r
        d["R_circumscribed"] = R
    def F(x):
        "Format Decimal x by removing trailing zeros and decimal point"
        s = str(+x)
        while s and s[0] != 0 and s[-1] == "0":
            s = s[:-1]
        if s[-1] == ".":
            s = s[:-1]
        return s
    def Report():
        S, w = d["solution"], 15
        dm = "°" if d["deg"] else " "
        S1, S2, S3, A1, A2, A3 = [S[i] for i in "S1 S2 S3 A1 A2 A3".split()]
        GetOtherFacts(S1, S2, S3, A1, A2, A3, d)
        dm, rad, pi = " ", "(radians)", DM.pi()
        if d["deg"]:
            dm = "°"
            rad = " " * len("(radians)")
            A1, A2, A3 = [180 * i / pi for i in (A1, A2, A3)]
        n = d["-d"]
        area = d["area"]
        r = d["r_inscribed"]
        R = d["R_circumscribed"]
        di = d["r_inscribed"] * 2
        D = d["R_circumscribed"] * 2
        p = d["perimeter"]
        # Check that needed types are Decimal
        for i in "S1 S2 S3 A1 A2 A3 r R di D p".split():
            assert ii(eval(i), Decimal), f"{i} is not Decimal"
        title = f"Triangle solution (to {n} figure{'s' if n > 1 else ''})"
        def ShowSolution():
            print(
                dedent(f'''
            {title}:
            Sides                     {F(S1):{w}s} {F(S2):{w}s} {F(S3):{w}s}
            Angles {rad}          {F(A1) + dm:{w}s} {F(A2) + dm:{w}s} {F(A3) + dm:{w}s}
            Area                      {area}
            Perimeter                 {p}
            Inscribed circle¹         r = {r}, d = {di}
            Circumscribed circle²     r = {R}, d = {D}
            ''')
            )
        ShowSolution()
        # Check for second solution (only for ssa problem)
        if "S1_2" in S:
            S1, S2, S3, A1, A2, A3 = [S[i] for i in "S1_2 S2_2 S3_2 A1_2 A2_2 A3_2".split()]
            GetOtherFacts(S1, S2, S3, A1, A2, A3, d)
            if d["deg"]:
                A1, A2, A3 = [180 * i / pi for i in (A1, A2, A3)]
            title = "Second solution"
            area = d["area"]
            r = d["r_inscribed"]
            R = d["R_circumscribed"]
            di = d["r_inscribed"] * 2
            D = d["R_circumscribed"] * 2
            p = d["perimeter"]
            # Check that needed types are Decimal
            for i in "S1 S2 S3 A1 A2 A3 r R di D p".split():
                assert ii(eval(i), Decimal), f"{i} is not Decimal"
            ShowSolution()
        print(dedent('''
        ¹ Center located by angle bisectors.
        ² Center located by perpendicular bisectors of the sides.
        '''))
        # Check for reasonableness
        if A1 == 0 or A2 == 0 or A3 == 0:
            print("\nThis is a degenerate triangle since one or more angles are zero")

if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine()
    datafile = args[0] if args else None
    if datafile is None:
        GetDataInteractively()
    else:
        ReadDatafile(datafile)
    with localcontext() as ctx:
        ctx.prec = d["-d"]
        SolveProblem()
        Report()
