'''
Show sprinkler timings
    Looks at the current day/time and if the sprinklers are on, shows the
    current circuit that's on.  If the sprinklers are not on, shows the
    schedule.
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        import datetime
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
        from pprint import pprint as pp
    # Custom imports
        from wrap import wrap, dedent
        from f import flt
        from color import Color, TRM as t
    # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        from color import t
        t.timing = t("lavl")
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [time] [day]
          With no arguments, show the sprinkler circuit that is currently
          on.  If the sprinklers are not on, show the schedule.  If time is
          given, it's in the form hh:mm.  If day is given, it's a
          case-insensitive first three letters of the day.
        Options:
            -b b    Set the budget % setting (allowed values are
                    {', '.join(str(i) for i in bset)})
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-b"] = 100       # Budget setting in % (10% units)
        d["-v"] = False     # Verbose
        try:
            opts, args = getopt.getopt(sys.argv[1:], "b:hv", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("v"):
                d[o] = not d[o]
            elif o in ("-b",):
                try:
                    d["-b"] = b = int(a)
                    if b not in bset:
                        raise ValueError()
                except ValueError:
                    msg = f"-b option argument must be in {bset}"
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        return args
if 1:   # Core functionality
    class Sprinklers:
        def __init__(self, budget=100):
            self.budget = budget
            self.cumulative_timing = self.GetTiming()
            self.schedule = self.GetSchedule()
            now = datetime.datetime.now()
            now_tt = now.timetuple()
            self.current_time = now_tt.tm_hour + now_tt.tm_min/60 + now_tt.tm_sec/3600
            self.day = now_tt.tm_wday        # Monday == 1
            try:
                self.on_hour = self.schedule[self.day]
            except KeyError:
                self.on_hour = None
            self.circuit_on_index = self.CircuitOn()
            self.Report()
        def GetTiming(self):
            '''Return tuple of sprinkler timing
                (ckt_name, time_min, adj_time_hr, cumul_time_hr)
            '''
            b, adj = 70, self.budget/100
            a = [
                # (ckt_name, time_min, adj_time_hr, cumul_time_hr)
                ["1 & 3", adj*b       , 0, 0],
                ["2",     adj*b       , 0, 0],
                ["4",     adj*(b + 10), 0, 0],
                ["5",     adj*(b + 10), 0, 0],
                ["6",     adj*(b + 10), 0, 0],
                ["7 & 8", adj*(b + 20), 0, 0],
                ["9",     adj*(b + 10), 0, 0],
            ]
            # Fill in last two columns
            for i in range(len(a)):
                ckt_name, time_min, adj_time_hr, cumul_time_hr = a[i]
                adj_time_hr = flt(time_min/60)
                a[i] = [ckt_name, time_min, adj_time_hr, cumul_time_hr]
                csum = 0
                for j in range(i):
                    csum += a[j][2]
                a[i][3] = csum
            for i in range(len(a)):
                a[i] = tuple(a[i])
            a = tuple(a)
            if d["-v"]:
                print(f"{t.timing}Sprinkler timing data:")
                ind, w = " "*4, 12
                # Print header
                print(f"{ind}", end="")
                print(f"{'Circuit':^{w}s}", end="")
                print(f"{'Minutes':^{w}s}", end="")
                print(f"{'Hr':^{w}s}", end="")
                print(f"{'CumulHr':^{w}s}")
                # Print data
                for i in range(len(a)):
                    print(f"{ind}", end="")
                    for j in range(len(a[i])):
                        print(f"{a[i][j]!s:^{w}s}", end="")
                    print()
                t.out("")
            return a
        def CircuitOn(self):
            '''Return the circuit index that's on.  on_hour and current_time are
            decimal hours.  If no circuit is on, return -1.
            '''
            not_on = -1
            # Get the total running time
            total_time_hr = self.cumulative_timing[-1][-1]
            if self.on_hour + total_time_hr < self.current_time:
                return not_on
            # Get cumulative sum to identify circuit that's on
            a = self.cumulative_timing.copy()
            i = 0
            while a:
                ckt, tcumulative = a.pop(0)
                if self.current_time <= tcumulative:
                    return i
            return not_on
        def GetSchedule(self):
            return {
                # Time in 24 hour units for sprinklers to come on.  The dict
                # key is the day number, starting with Monday being 0.
                1: 7,   # Tuesday at 7 am
                3: 7,   # Thursday at 7 am
                5: 16,  # Saturday at 4 pm
            }
        def Report(self):
            'Print schedule.  If a sprinkler is on, color highlight it.'
            on_index = self.CircuitOn()
            if on_index != -1:
                print("on_index =", on_index)
            exit() #xx
            
if __name__ == "__main__":
    bset = list(range(10, 101, 10))  # Allowed budget settings
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    s = Sprinklers(budget=d["-b"])
