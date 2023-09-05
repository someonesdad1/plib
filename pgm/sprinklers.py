'''
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
        # Print out sprinkler timing.
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
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # Circuit timing in minutes at budget == 100%
        timing = (
            ("1, 3", 100),
            ("2", 100),
            ("4", 115),
            ("5", 115),
            ("6", 115),
            ("7, 8", 130),
            ("9", 115),
        )
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [budget]
          Print out the times the sprinklers will come on.  Normal timing
          is such that budget == 70%.  This is done to get the longer times
          needed for July and August.
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
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
        '''t is time in minutes from midnight.  Return in HH:MM format.
        '''
        h, m = divmod(t, 60)
        h %= 24
        m %= 60
        return f"{h:02d}:{m:02d}"
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
            for ckt, minutes in timing:
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
            for ckt, minutes in timing:
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
    args = ParseCommandLine(d)
    if not args:
        budget = 70
    else:
        budget = int(TemplateRound(float(args[0]), 10))
    PrintSchedule(budget)
