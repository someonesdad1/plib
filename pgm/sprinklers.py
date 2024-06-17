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
        import datetime as dt
        import getopt
        import sys
        import time
    if 1:   # Custom imports
        from get import GetClosest
        from color import t
        from wrap import dedent
    if 1:   # Global variables
        class G:
            pass
        g = G()
        ii = isinstance
        # Circuit timing in minutes at budget == 100%, as of 6 Jun 2024
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
        # The Orbit controller only allows the following % values for the budget setting
        g.allowed_budget = (0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100)
if 1:   # Utility
    def GetColors():
        t.budget = t("ornl")
        t.err = t("redl")
    def SetBudget(budget):
        try:
            b = GetClosest(budget, g.allowed_budget)
            with open(g.budget_file, "w") as fp:
                fp.write(str(b))
            print(f"Budget set to {b}%")
        except Exception:
            Error(f"Could not write budget file {g.budget_file}.")
    def GetBudget():
        try:
            with open(g.budget_file) as fp:
                s = fp.read()
                budget = int(s)
                return GetClosest(budget, g.allowed_budget)
        except Exception:
            t.print(f"{t.err}Could not read budget file {g.budget_file!r}.  Using 50%.")
            return 50
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
        try:
            opts, args = getopt.getopt(sys.argv[1:], "B:b:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-B":
                try:
                    SetBudget(int(a))
                    exit(0)
                except Exception:
                    Error(f"{a!r} is not a valid integer")
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
    def PrintSchedule():
        budget = d["-b"]
        assert(ii(budget, int) and 0 <= budget <= 100)
        p = budget/100
        t.print(f"{t.budget}Budget = {budget}%")
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
            T = 16*60    # Start at 4 pm
            total_minutes = 0
            for ckt, minutes in g.timing:
                minutes = int(minutes*budget/100 + 0.5)
                total_minutes += minutes
                print(f"{indent}{ckt:^{w[0]}s}"
                    f"{sep}{minutes!s:^{w[1]}s}"
                    f"{sep}{HM(T):^{w[2]}s}"
                    f"{sep}{HM(T + minutes):^{w[3]}s}")
                T += minutes
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
            T = 7*60    # Start at 7 am
            total_minutes = 0
            for ckt, minutes in g.timing:
                minutes = int(minutes*budget/100 + 0.5)
                total_minutes += minutes
                print(f"{indent}{ckt:^{w[0]}s}"
                    f"{sep}{minutes!s:^{w[1]}s}"
                    f"{sep}{HM(T):^{w[2]}s}"
                    f"{sep}{HM(T + minutes):^{w[3]}s}")
                T += minutes
            print(f"{indent}Total minutes = {total_minutes} = {total_minutes/60:.3f} hours")
    def H(tm):
        '''tm is a datetime.  Extract the time and return it in the form 'hh:mm am' or 'hh:mm pm'.
        '''
        hr, min, sec = [int(i) for i in str(tm).split()[1].split(":")]
        a = "am"
        if hr >= 12:
            a = "pm"
            hr -= 12
        if not hr:
            hr = 12
        return f"{hr:2d}:{min:02d} {a}"
    def GetStartTime(start_time):
        '''start_time can be of the following forms:
            13:34       24 hour hh:mm form
            1:34 p      12 hour hh:mm am/pm form
            1:34 pm     12 hour hh:mm am/pm form
            13.4        24 hour h.h decimal form
            1.6 p       12 hour h.h decimal form
        Return it as (h, m) where h and m are integers with h on [0, 23) and m on [0, 60).
        '''
        h, m = 0, 0
        try:
            if "a" in start_time:
                # 12 hour hh:mm form
                a, b = start_time.split(":")
                h = int(a)
            elif "p" in start_time:
                # 12 hour hh:mm form
                a, b = start_time.split(":")
            elif "." in start_time:
                # Decimal form
                if "a" in start_time:
                    pass
                elif "p" in start_time:
                    pass
            else:
                # 24 hour hh:mm form
                    pass
        except Exception:
            Error(f"{start_time!r} is a bad start time")
        if not (0 <= h < 24):
            Error(f"Hour must be on [0, 24)")
        if not (0 <= m < 60):
            Error(f"Minutes must be on [0, 60)")
        return h, m
    def PrintOffsetSchedule(h, m):
        '''Print out the actual times for programs A and B, as they both run unless you select only one.
        h is integer on [0, 24) and m is integer on [0, 60).
        '''
        budget = d["-b"]
        assert(ii(budget, int) and 0 <= budget <= 100)
        p = budget/100
        t.print(f"{t.budget}Budget = {budget}%")
        now = dt.datetime.now()
        starttime = dt.datetime(now.year, now.month, now.day, h, m)
        indent = " "*4
        total_minutes = 0
        def Print():
            w = (7, 7, 12, 12)
            nonlocal total_minutes
            print(f"{indent} "
                f"{'Circuit':^{w[0]}s}{indent}"
                f"{'Minutes':^{w[1]}s}{indent}"
                f"{'Start':^{w[2]}s}{indent}"
                f"{'End':^{w[3]}s}")
            s = "-"
            print(f"{indent} "
                f"{s*w[0]:^{w[0]}s}{indent}"
                f"{s*w[1]:^{w[1]}s}{indent}"
                f"{s*w[2]:^{w[2]}s}{indent}"
                f"{s*w[3]:^{w[3]}s}")
            for ckt, minutes in g.timing:
                minutes = int(minutes*budget/100 + 0.5)
                start = starttime + dt.timedelta(minutes=total_minutes)
                total_minutes += minutes
                finish = starttime + dt.timedelta(minutes=total_minutes)
                print(f"{indent} "
                    f"{ckt:^{w[0]}s}{indent}"
                    f"{minutes!s:^{w[1]}s}{indent}"
                    f"{H(start):^{w[2]}s}{indent}"
                    f"{H(finish):^{w[3]}s}")
            print(f"{indent}Watering time = {total_minutes} minutes = {total_minutes/60:.2f} hours")
        # Program A
        print("Program A")
        Print()
        # Program B
        print("\nProgram B")
        Print()

if 1: #xx
    print(GetStartTime("7:34"))

    exit()

if __name__ == "__main__":
    d = {}      # Options dictionary
    GetColors()
    g.default_budget = GetBudget()
    args = ParseCommandLine(d)
    if args:
        for arg in args:
            h, m = GetStartTime(arg)
            PrintOffsetSchedule(h, m)
    else:
        PrintSchedule()
