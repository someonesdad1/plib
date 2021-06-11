'''
Give sequence values that are the IEC 60063 numbers.  
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2012 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <utility> IEC 60063 numbers (E-series:  E6, E12, etc.)
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
def E(series, normalize=False):
    '''Specify the series you want by an integer:  6, 12, 24, 48, 96,
    or 192.  If normalize is True, each value in the returned array
    will be in the interval [1, 10).
 
    Reference: http://en.wikipedia.org/wiki/Preferred_value#E_series
    '''
    def Convert(s):
        s = s.replace("\n", "")
        s = [int(i) for i in s.split()]
        s.sort()
        if normalize:
            s = [round(i/100, 3) for i in s]
        return s
    d = {
        6  : '''100 150 220 330 470 680''',
        12 : '''100 120 150 180 220 270 330 390 470 560 680 820''',
        24 : '''100 110 120 130 150 160 180 200 220 240 270 300 330 360
                390 430 470 510 560 620 680 750 820 910''',
        48 : '''100 105 110 115 121 127 133 140 147 154 162 169 178 187
                196 205 215 226 237 249 261 274 287 301 316 332 348 365
                383 402 422 442 464 487 511 536 562 590 619 649 681 715
                750 787 825 866 909 953''',
        96 : '''100 102 105 107 110 113 115 118 121 124 127 130 133 137
                140 143 147 150 154 158 162 165 169 174 178 182 187 191
                196 200 205 210 215 221 226 232 237 243 249 255 261 267
                274 280 287 294 301 309 316 324 332 340 348 357 365 374
                383 392 402 412 422 432 442 453 464 475 487 499 511 523
                536 549 562 576 590 604 619 634 649 665 681 698 715 732
                750 768 787 806 825 845 866 887 909 931 953 976''',
        192 : '''100 101 102 104 105 106 107 109 110 111 113 114 115 117
                 118 120 121 123 124 126 127 129 130 132 133 135 137 138
                 140 142 143 145 147 149 150 152 154 156 158 160 162 164
                 165 167 169 172 174 176 178 180 182 184 187 189 191 193
                 196 198 200 203 205 208 210 213 215 218 221 223 226 229
                 232 234 237 240 243 246 249 252 255 258 261 264 267 271
                 274 277 280 284 287 291 294 298 301 305 309 312 316 320
                 324 328 332 336 340 344 348 352 357 361 365 370 374 379
                 383 388 392 397 402 407 412 417 422 427 432 437 442 448
                 453 459 464 470 475 481 487 493 499 505 511 517 523 530
                 536 542 549 556 562 569 576 583 590 597 604 612 619 626
                 634 642 649 657 665 673 681 690 698 706 715 723 732 741
                 750 759 768 777 787 796 806 816 825 835 845 856 866 876
                 887 898 909 920 931 942 953 965 976 988''',
    }
    if series not in d:
        raise ValueError("Series number must be 6, 12, 24, 48, 96, or 192")
    return Convert(d[series])
if __name__ == "__main__": 
    if 1:   # Imports
        # Standard library modules
        import getopt
        import os
        import pathlib
        import sys
        from pdb import set_trace as xx
    if 1:   # Custom modules
        from wrap import wrap, dedent, indent, Wrap
        from lwtest import run, raises, assert_equal
        from columnize import Columnize
    if 1:   # Global variables
        P = pathlib.Path
        d = {}  # Options dictionary
        # Data copy and pasted from
        # http://en.wikipedia.org/wiki/Preferred_value#E_series
        raw_data = {
        6 : "10      15      22      33      47      68",
        12 : "10  12  15  18  22  27  33  39  47  56  68  82",
        24 : '''10  12  15  18  22  27  33  39  47  56  68  82
                11  13  16  20  24  30  36  43  51  62  75  91''',
        48 : '''100  121  147  178  215  261  316  383  464  562  681  825
                105  127  154  187  226  274  332  402  487  590  715  866
                110  133  162  196  237  287  348  422  511  619  750  909
                115  140  169  205  249  301  365  442  536  649  787 953
        ''',
        96 : '''100  121  147  178  215  261  316  383  464  562  681  825
                102  124  150  182  221  267  324  392  475  576  698  845
                105  127  154  187  226  274  332  402  487  590  715  866
                107  130  158  191  232  280  340  412  499  604  732  887
                110  133  162  196  237  287  348  422  511  619  750  909
                113  137  165  200  243  294  357  432  523  634  768  931
                115  140  169  205  249  301  365  442  536  649  787  953
                118  143  174  210  255  309  374  453  549  665  806  976
        ''',
        192 : '''100  121  147  178  215  261  316  383  464  562  681  825
                101  123  149  180  218  264  320  388  470  569  690  835
                102  124  150  182  221  267  324  392  475  576  698  845
                104  126  152  184  223  271  328  397  481  583  706  856
                105  127  154  187  226  274  332  402  487  590  715  866
                106  129  156  189  229  277  336  407  493  597  723  876
                107  130  158  191  232  280  340  412  499  604  732  887
                109  132  160  193  234  284  344  417  505  612  741  898
                110  133  162  196  237  287  348  422  511  619  750  909
                111  135  164  198  240  291  352  427  517  626  759  920
                113  137  165  200  243  294  357  432  523  634  768  931
                114  138  167  203  246  298  361  437  530  642  777  942
                115  140  169  205  249  301  365  442  536  649  787  953
                117  142  172  208  252  305  370  448  542  657  796  965
                118  143  174  210  255  309  374  453  549  665  806  976
                120  145  176  213  258  312  379  459  556  673  816  988
        '''}
    if 1:   # Unit test code
        def Convert(s):
            '''Convert the string to a list of integers.  The integers
            returned will all be >= 100 and < 1000.
            '''
            s = s.replace("\n", "")
            s = [int(i) for i in s.split()]
            s.sort()
            if s[0] < 100:
                s = [i*10 for i in s]
            return s
        def Test_E_series():
            # Convert strings to arrays in data dictionary
            data = {}
            for i in raw_data:
                data[i] = Convert(raw_data[i])
            for i in data:
                assert(E(i) == data[i])
    if 1:   # Module's base code
        def Error(msg, status=1):
            print(msg, file=sys.stderr)
            exit(status)
        def Usage(d, status=1):
            name = sys.argv[0]
            print(dedent(f'''
            Usage:  {name} 
              Prints the E series.
             
            Options:
              -p        Plot the data
              --test    Run internal self tests
            '''))
            exit(status)
        def ParseCommandLine(d):
            d["-p"] = False             # Plot the data
            d["--test"] = False         # Run self tests
            try:
                opts, args = getopt.getopt(sys.argv[1:], "hp", 
                    "test help".split())
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o in ("-h", "--help"):
                    Usage(d, status=0)
                elif o == "-p":
                    d["-p"] = True
                elif o == "--test":
                    d["--test"] = True
            return args
    if 1:   # Print and plot
        def PrintSeries():
            for series in (6, 12, 24, 48, 96, 192):
                print(f"E{series}")
                s = [str(i) for i in E(series)]
                for i in Columnize(s, indent=2*" ", horiz=True):
                    print(i)
        def PlotSeries():
            from pylab import plot, grid, xlabel, ylabel, legend, title, show
            from functools import partial
            s = "."
            S = partial(E, normalize=True)
            for i, lbl in ((S(6), "E6"),
                        (S(12), "E12"),
                        (S(24), "E24"),
                        (S(48), "E48"),
                        (S(96), "E96"),
                        (S(192), "E192")):
                plot(log10(i), s, label=lbl)
            grid()
            xlabel("Number of elements in series")
            ylabel("Base 10 logarithm of significand")
            legend(loc="lower right")
            title("Logarithms of E series values")
            show()
    ParseCommandLine(d)
    if d["--test"]:
        exit(run(globals())[0])
    elif d["-p"]:
        PlotSeries()
    else:
        PrintSeries()
