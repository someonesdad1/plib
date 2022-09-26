'''
Information on Clausing 5914 lathe
'''
if 1:   # Header
    if 1:   # Copyright, license
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
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
    if 1:   # Custom imports
        from columnize import Columnize
        from color import t
        from f import flt
        from wrap import dedent
    if 1:   # Global variables
        ii = isinstance
        w = int(os.environ.get("COLUMNS", "80")) - 1
        tpi = [
            4, 4.5, 5, 5.5, 5.75, 6, 6.5, 6.75, 7, 8, 9, 10, 11, 11.5, 12,
            13, 13.5, 14, 16, 18, 20, 22, 23, 24, 26, 27, 28, 32, 36, 40,
            44, 46, 48, 52, 54, 56, 64, 72, 80, 88, 92, 96, 104, 108, 112,
            128, 144, 160, 176, 184, 192, 208, 216, 224,
        ]
        x = flt(0)
        x.N = 4
        t.mm = t('sky')
        t.inch = t('lwnl')
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] 
          Show Clausing lathe information.
        Options:
            -h      Print a manpage
            -m      Print in metric dimensions
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-m"] = False
        d["-d"] = 4         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:hm", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("m"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                    flt(0).N = d[o]
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
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
    def Threading_tpi():
        def f(x):
            'Return suitable string for tpi value'
            i = int(x)
            if i == x:
                return str(x)
            elif x - i == 1/4:
                return str(i) + "¼"
            elif x - i == 1/2:
                return str(i) + "½"
            elif x - i == 3/4:
                return str(i) + "¾"
        print(f"{t.inch}Threading tpi:")
        for line in Columnize([f(i) for i in tpi], col_width=8, indent=" "*4):
            print(line)
    def Threading_pitch_mils():
        print("Pitch in mils:")
        p = list(flt(1/i) for i in tpi)
        for line in Columnize([f"{i}" for i in p], col_width=8, indent=" "*4):
            print(line)
    def Threading_mm():
        print(f"{t.mm}Pitch in mm:")
        p = list(flt(25.4/i) for i in tpi)
        for line in Columnize([f"{i}" for i in p], col_width=8, indent=" "*4):
            print(line)
        t.print(end="")
    def Print_feeds():
        def Print(data, in_or_out):
            feed = []
            for i in data.strip().split("\n"):
                for j in i.split():
                    feed.append(flt(j))
            feed = list(sorted(feed))
            if d["-m"]:
                print(f"{t.mm}Feeds with slide gear {in_or_out} (μm/rev):")
                for line in Columnize([f"{i*1000}" for i in feed], col_width=8, indent=" "*4):
                    print(line)
            else:
                print(f"{t.inch}Feeds with slide gear {in_or_out} (mils/rev):")
                for line in Columnize([f"{i*1000}" for i in feed], col_width=8, indent=" "*4):
                    print(line)
            t.print(end="")
        data_slide_gear_in = '''
            0.03670 0.01830 0.00920
            0.03260 0.01630 0.00810
            0.02930 0.01470 0.00730
            0.02670 0.01340 0.00660
            0.02550 0.01270 0.00630
            0.02090 0.01050 0.00520
            0.02180 0.01090 0.00540
            0.02260 0.01130 0.00560
            0.02440 0.01220 0.00610
        '''.strip()
        data_slide_gear_out = '''
            0.00460 0.00220 0.00110
            0.00410 0.00200 0.00094
            0.00360 0.00180 0.00092
            0.00330 0.00170 0.00083
            0.00310 0.00160 0.00079
            0.00260 0.00130 0.00065
            0.00270 0.00136 0.00068
            0.00280 0.00140 0.00070
            0.00300 0.00150 0.00076
        '''.strip()
        Print(data_slide_gear_in, "in")
        Print(data_slide_gear_out, "out")
    def Metric_threads():
        'Show common coarse metric threads'
        metric = '''
            2-0.4 3-0.5 4-0.7 5-0.8 6-1 8-1.25 10-1.5 12-1.75 16-2 20-2.5
            24-3
        '''
        print(f"{t.mm}Common coarse metric threads")
        for i in Columnize(metric.split(), columns=4, col_width=12, indent=" "*4):
            print(i)
if __name__ == "__main__": 
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    print(dedent(f'''
    {t('ornl')}Clausing 5914 12x36 lathe{t.n}

    Swing over bed = {t.inch}6.08 inches{t.n} = {t.mm}154 mm{t.n}
    Swing over cross slide = {t.inch}3.72 inches{t.n} = {t.mm}94 mm{t.n}
    '''[1:]))
    if d["-m"]:
        Threading_tpi()
        Threading_mm()
        Metric_threads()
    else:
        Threading_tpi()
        Print_feeds()
        print("Use -m option to see metric equivalents")
