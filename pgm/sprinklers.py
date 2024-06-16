'''

- Default behavior is to print out timing with current budget setting
    - Spring budget setting is 50%, letting hot summer temperatures use 80% or 90%
- Use -b option to display for a different budget setting
- Use -B option to change default budget setting
- As of May 2024, all circuit timing is 120 minutes
- A command line argument lets you define the starting time and the new table will reflect that
  starting time


Print out sprinkler timing
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Print out sprinkler timing
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
    if 1:   # Global variables
        class G:
            pass
        g = G()
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # Circuit timing in minutes at budget == 100%
        # As of 6 Jun 2024
        a = 120
        g.timing = (
            ("1,3", a),
            ("2", a),
            ("4", a),
            ("5", a),
            ("6", a),
            ("7,8", a),
            ("9", a),
        )
        del a
        # Where to store the default budget value
        g.budget_file = "/plib/pgm/sprinklers.budget"
        # This variable is the budget setting (resolution = 10%)
        g.default_budget = None
if 1:   # Utility
    def GetBudget():
        try:
            with open(g.budget_file) as fp:
                s = fp.read()
                return int(s)
        except Exception:
            Error(f"Could not read budget file {g.budget_file}")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [start]
          Print out the times the sprinklers will come on.  No argument prints the normal weekly
          schedule.  If you provide a start time hh:mm in 24 hour form, the sprinkler circuit
          timing will be printed.
        Options:
            -B n    Set n to the default budget value
            -b n    Use n as the budget value [50]
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-b"] = g.default_budget    # Default budget value
        breakpoint() #xx 
        try:
            opts, args = getopt.getopt(sys.argv[1:], "b:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-b":
                d[o] = b = int(a)
                allowed = (0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100)
                if b not in allowed:
                    print(f"{a!r} is not an acceptable budget number:")
                    print(f"    Must be one of {' '.join(str(i) for i in allowed)}")
                    exit(1)
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
if 1:   # Core functionality
    def TemplateRound(x, template, up=True):
        '''Round a float to a template number.  The basic algorithm is to
        determine how many template values are in x.  You can choose to
        round up (the default) or down.
        '''
        if not x:
            return x
        sign = 1 if x >= 0 else -1
        if sign < 0:
            up = not up
        y = int(abs(x/template) + 0.5)*abs(template)
        if up and y < abs(x):
            y += template
        elif not up and y > abs(x):
            y -= template
        return sign*y
    def HM(t):
        't is time in minutes from midnight.  Return in HH:MM format.'
        h, m = divmod(t, 60)
        H = h % 24
        h %= 12
        m %= 60
        ap = "pm" if H > 11 else "am"
        if not h:
            h = 12
        return f"{h:2d}:{m:02d} {ap}"
    def PrintSchedule(budget):
        def f(t):
            return t.strftime('%I:%M %p').lower()
        assert(ii(budget, int) and 0 <= budget <= 100)
        p = budget/100
        print(f"Budget = {budget}%")
        if 1:   # Saturday
            print(f"Saturday schedule")
            w, sep, indent = (7, 7, 7, 7), " "*5, " "*4
            print(f"{indent}{'Circuit':^{w[0]}s}"
                  f"{sep}{'Minutes':^{w[1]}s}"
                  f"{sep}{'Start':^{w[2]}s}"
                  f"{sep}{'End':^{w[3]}s}")
            print(f"{indent}{'-'*w[0]:^{w[0]}s}"
                  f"{sep}{'-'*w[1]:^{w[1]}s}"
                  f"{sep}{'-'*w[2]:^{w[2]}s}"
                  f"{sep}{'-'*w[3]:^{w[3]}s}")
            t = 16*60    # Start at 4 pm
            total_minutes = 0
            for ckt, minutes in g.timing:
                minutes = int(minutes*budget/100 + 0.5)
                total_minutes += minutes
                print(f"{indent}{ckt:^{w[0]}s}"
                    f"{sep}{minutes!s:^{w[1]}s}"
                    f"{sep}{HM(t):^{w[2]}s}"
                    f"{sep}{HM(t + minutes):^{w[3]}s}")
                t += minutes
            print(f"{indent}Total minutes = {total_minutes} = {total_minutes/60:.3f} hours")
        if 1:   # Tuesday and Thursday
            print(f"Tuesday, Thursday schedule")
            w, sep, indent = (7, 7, 7, 7), " "*5, " "*4
            print(f"{indent}{'Circuit':^{w[0]}s}"
                  f"{sep}{'Minutes':^{w[1]}s}"
                  f"{sep}{'Start':^{w[2]}s}"
                  f"{sep}{'End':^{w[3]}s}")
            print(f"{indent}{'-'*w[0]:^{w[0]}s}"
                  f"{sep}{'-'*w[1]:^{w[1]}s}"
                  f"{sep}{'-'*w[2]:^{w[2]}s}"
                  f"{sep}{'-'*w[3]:^{w[3]}s}")
            t = 7*60    # Start at 7 am
            total_minutes = 0
            for ckt, minutes in g.timing:
                minutes = int(minutes*budget/100 + 0.5)
                total_minutes += minutes
                print(f"{indent}{ckt:^{w[0]}s}"
                    f"{sep}{minutes!s:^{w[1]}s}"
                    f"{sep}{HM(t):^{w[2]}s}"
                    f"{sep}{HM(t + minutes):^{w[3]}s}")
                t += minutes
            print(f"{indent}Total minutes = {total_minutes} = {total_minutes/60:.3f} hours")

if __name__ == "__main__":
    d = {}      # Options dictionary
    g.default_budget = GetBudget()
    args = ParseCommandLine(d)
    budget = d["-b"]
    PrintSchedule(budget)
