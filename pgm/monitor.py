'''
Print out energy consumption of monitor
'''
 
if 1:  # Copyright, license
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
    pass
if 1:   # Standard imports
    import getopt
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    from f import flt
    from interpolate import LinearInterpFunction
    from color import C
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    class g:
        pass
    g.dollar_per_kWhr = 0.104
    g.cents = "¢"
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [monitor]
          Print energy usage and cost of monitor.
          Dell24 is the default.
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 3         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
if 1:   # Core functionality
    def Dell24():
        '''
        Brightness   Energy, W    ¢/week
           Off          10          17
             0          14          24
            10  *       16          28
            20  *       19          33
            30          21          37
            40          24          42
            50          26          45
            60          29          51
            70          32          56
            80          34          59
            90          36          63
           100          37          65

        Note when Windows blacks the screen in the screensaver, the power
        doesn't change.  When Windows turns the monitor off ("Off" in above
        table), the power goes to 10 W.  * marks where I run the monitor
        (it's used at 100 contrast):  10 brightness is good on a cloudy day
        and at night; 20 is good when the sun is shining on the curtains.
        '''
        model = "P2413Q"
        off = 10
        Br = list(range(0, 101, 10))
        P = [14, 16, 19, 21, 24, 26, 29, 32, 34, 36, 37]
        print("Dell P2413Q monitor energy cost as")
        print("function of brightness setting")
        print(f"                                       Corr")
        print(f"             Energy,   {g.cents} per   $ per   $ per")
        print(f"Brightness     W       week    year    year")
        print(f"----------   ------    ----    ----    ----")
        f = LinearInterpFunction(Br, P)
        flt(0).rtz = flt(0).rtdp = True
        for br in range(0, 101, 10):
            p_W = flt(f(br))
            kW = p_W/1000
            cost_week = 7*24*kW*g.dollar_per_kWhr
            cost_year = 52*cost_week
            # The monitor is at 10 W of power for at least 8 hours per day,
            # so the yearly cost will be 2/3 of the calculated value plus
            # 9.1.
            corr = 2/3*cost_year + 1/3*9.1
            lte30 = br <= 30
            if lte30:
                print(f"{C.lgrn}", end="")
            s = (f"{br:6d}{' '*7}{p_W!s:^6s}{100*cost_week:7.0f}"
                 f"{cost_year:9.1f}{corr:9.1f}")
            print(s, end="")
            print(f"{C.norm}") if 20 <= br <= 30 else print()
        print(dedent(f'''
 
        The colored rows are where I run the monitor brightness.  At night,
        I use a brightness of 10 and when the sun is on the south window, I
        use 25.  Thus, the power cost per year is about $13.

        $ per year is the energy cost to leave the monitor on continuously.
        The Corr column is for the real cost.  Windows powers the monitor
        down after 30 minutes of non-use; this means the monitor won't be
        used for 8 to 10 hours per day or more.  The Corr column estimates
        the real yearly cost when the monitor is powered down to 10 W for 8
        hours per day.

        The monitor's screen is 527x295 mm, giving a diagonal of 604 mm or
        23.8 inches.  Hence, it's called a 24 inch monitor.  I run both of
        them at 3840x2160 pixel resolution.
        '''))

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if not args:
        Dell24()
    else:
        raise Exception("not implemented")
