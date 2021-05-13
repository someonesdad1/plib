'''
Give sequence values that are the IEC 60063 numbers.  Reference:
http://en.wikipedia.org/wiki/Preferred_value#E_series
'''

# Copyright (C) 2012 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

def E(series, normalize=False):
    '''Specify the series you want by an integer:  6, 12, 24, 48, 96,
    or 192.  If normalize is True, each value in the returned array
    will be in the interval [1, 10).
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
        24 : '''100 120 150 180 220 270 330 390 470 560 680 820
                110 130 160 200 240 300 360 430 510 620 750 910''',
        48 : '''
            100 121 147 178 215 261 316 383 464 562 681 825 105 127 154 187
            226 274 332 402 487 590 715 866 110 133 162 196 237 287 348 422
            511 619 750 909 115 140 169 205 249 301 365 442 536 649 787 953''',

        96 : '''
            100 121 147 178 215 261 316 383 464 562 681 825 102 124 150 182
            221 267 324 392 475 576 698 845 105 127 154 187 226 274 332 402
            487 590 715 866 107 130 158 191 232 280 340 412 499 604 732 887
            110 133 162 196 237 287 348 422 511 619 750 909 113 137 165 200
            243 294 357 432 523 634 768 931 115 140 169 205 249 301 365 442
            536 649 787 953 118 143 174 210 255 309 374 453 549 665 806 976''',
        192 : '''

            100 121 147 178 215 261 316 383 464 562 681 825 101 123 149 180
            218 264 320 388 470 569 690 835 102 124 150 182 221 267 324 392
            475 576 698 845 104 126 152 184 223 271 328 397 481 583 706 856
            105 127 154 187 226 274 332 402 487 590 715 866 106 129 156 189
            229 277 336 407 493 597 723 876 107 130 158 191 232 280 340 412
            499 604 732 887 109 132 160 193 234 284 344 417 505 612 741 898
            110 133 162 196 237 287 348 422 511 619 750 909 111 135 164 198
            240 291 352 427 517 626 759 920 113 137 165 200 243 294 357 432
            523 634 768 931 114 138 167 203 246 298 361 437 530 642 777 942
            115 140 169 205 249 301 365 442 536 649 787 953 117 142 172 208
            252 305 370 448 542 657 796 965 118 143 174 210 255 309 374 453
            549 665 806 976 120 145 176 213 258 312 379 459 556 673 816 988''',
    }
    if series not in d:
        raise ValueError("Series number must be 6, 12, 24, 48, 96, or 192")
    return Convert(d[series])

if __name__ == "__main__":
    import sys
    from columnize import Columnize
    if len(sys.argv) == 1:
        # Print the series
        for normalize in (True, False):
            for series in (6, 12, 24, 48, 96, 192):
                print("E{}".format(series))
                s = [str(i) for i in E(series, normalize=normalize)]
                for i in Columnize(s, indent=2*" "):
                    print(i)
    else:
        # Plot
        from pylab import *
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
