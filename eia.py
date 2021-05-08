'''
Module to provide EIA resistor values along with a custom set of
on-hand resistances.

'''

import sys
import u
from roundoff import RoundOff
from columnize import Columnize

# The following iterable defines the common powers of 10 to use to get 
# commonly-available resistors.
powers_of_10 = (-1, 0, 1, 2, 3, 4, 5, 6, 7)

# EIA recommended resistor significand values.  From
# https://en.wikipedia.org/wiki/E_series_of_preferred_numbers
EIA_series = {
    # >20%
    3 : (1.0, 2.2, 4.7),
    # 20%
    6 : (1.0, 1.5, 2.2, 3.3, 4.7, 6.8),
    # 10%
    12 : (1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2),
    # 5%
    24 : (1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 
          3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1),
    # 2%
    48 : (1.00, 1.05, 1.10, 1.15, 1.21, 1.27, 1.33, 1.40, 1.47, 1.54,
          1.62, 1.69, 1.78, 1.87, 1.96, 2.05, 2.15, 2.26, 2.37, 2.49, 2.61,
          2.74, 2.87, 3.01, 3.16, 3.32, 3.48, 3.65, 3.83, 4.02, 4.22, 4.42,
          4.64, 4.87, 5.11, 5.36, 5.62, 5.90, 6.19, 6.49, 6.81, 7.15, 7.50,
          7.87, 8.25, 8.66, 9.09, 9.53),
    # 1%
    96 : (1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27,
         1.30, 1.33, 1.37, 1.40, 1.43, 1.47, 1.50, 1.54, 1.58, 1.62, 1.65,
         1.69, 1.74, 1.78, 1.82, 1.87, 1.91, 1.96, 2.00, 2.05, 2.10, 2.15,
         2.21, 2.26, 2.32, 2.37, 2.43, 2.49, 2.55, 2.61, 2.67, 2.74, 2.80,
         2.87, 2.94, 3.01, 3.09, 3.16, 3.24, 3.32, 3.40, 3.48, 3.57, 3.65,
         3.74, 3.83, 3.92, 4.02, 4.12, 4.22, 4.32, 4.42, 4.53, 4.64, 4.75,
         4.87, 4.99, 5.11, 5.23, 5.36, 5.49, 5.62, 5.76, 5.90, 6.04, 6.19,
         6.34, 6.49, 6.65, 6.81, 6.98, 7.15, 7.32, 7.50, 7.68, 7.87, 8.06,
         8.25, 8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76),
    # 0.5%
    192 : (1.00, 1.01, 1.02, 1.04, 1.05, 1.06, 1.07, 1.09, 1.10, 1.11,
          1.13, 1.14, 1.15, 1.17, 1.18, 1.20, 1.21, 1.23, 1.24, 1.26, 1.27,
          1.29, 1.30, 1.32, 1.33, 1.35, 1.37, 1.38, 1.40, 1.42, 1.43, 1.45,
          1.47, 1.49, 1.50, 1.52, 1.54, 1.56, 1.58, 1.60, 1.62, 1.64, 1.65,
          1.67, 1.69, 1.72, 1.74, 1.76, 1.78, 1.80, 1.82, 1.84, 1.87, 1.89,
          1.91, 1.93, 1.96, 1.98, 2.00, 2.03, 2.05, 2.08, 2.10, 2.13, 2.15,
          2.18, 2.21, 2.23, 2.26, 2.29, 2.32, 2.34, 2.37, 2.40, 2.43, 2.46,
          2.49, 2.52, 2.55, 2.58, 2.61, 2.64, 2.67, 2.71, 2.74, 2.77, 2.80,
          2.84, 2.87, 2.91, 2.94, 2.98, 3.01, 3.05, 3.09, 3.12, 3.16, 3.20,
          3.24, 3.28, 3.32, 3.36, 3.40, 3.44, 3.48, 3.52, 3.57, 3.61, 3.65,
          3.70, 3.74, 3.79, 3.83, 3.88, 3.92, 3.97, 4.02, 4.07, 4.12, 4.17,
          4.22, 4.27, 4.32, 4.37, 4.42, 4.48, 4.53, 4.59, 4.64, 4.70, 4.75,
          4.81, 4.87, 4.93, 4.99, 5.05, 5.11, 5.17, 5.23, 5.30, 5.36, 5.42,
          5.49, 5.56, 5.62, 5.69, 5.76, 5.83, 5.90, 5.97, 6.04, 6.12, 6.19,
          6.26, 6.34, 6.42, 6.49, 6.57, 6.65, 6.73, 6.81, 6.90, 6.98, 7.06,
          7.15, 7.23, 7.32, 7.41, 7.50, 7.59, 7.68, 7.77, 7.87, 7.96, 8.06,
          8.16, 8.25, 8.35, 8.45, 8.56, 8.66, 8.76, 8.87, 8.98, 9.09, 9.20,
          9.31, 9.42, 9.53, 9.65, 9.76, 9.88),
}

def Int(x):
    '''If the string form of the float x ends in ".0", return it as an
    integer; otherwise, return it unchanged.
    '''
    x = RoundOff(x)
    return int(x) if str(x).endswith(".0") else x

def OnHand():
    '''Returns a set of on-hand resistors.
    '''
    prefixes = {"k": 3, "M": 6}
    onhand = []
    for i in OnHand.values.replace("\n", " ").split():
        val, prefix = u.ParseUnit(i)
        R = float(val)
        if prefix:
            R *= 10**prefixes[prefix]
        onhand.append(Int(R))
    return set(onhand)

OnHand.values = '''
0.025 0.2 0.27 0.33

1 2.2 4.6 8.3

10.1 12 14.7 15 17.8 22 27 28.4 30 31.6 33 35 38.4 46.3 50 55.5 61.8 67
75 78 81

100 110 115 121 150 162 170 178 196 215 220 237 268 270 287 316 330 349
388 465 500 513 546 563 617 680 750 808 822 980

1k 1.1k 1.18k 1.21k 1.33k 1.47k 1.5k 1.62k 1.78k 1.96k 2.16k 2.2k 2.37k
2.61k 2.72k 3k 3.16k 3.3k 3.47k 3.82k 4.64k 5k 5.53k 6.8k 6.84k 8k 8.3k
9.09k

10k 11.8k 12.1k 13.3k 15k 16.2k 17.8k 18k 19.5k 20k 22k 26.2k 33k 39k 42.4k
46k 51k 55k 67k 75k 82k

100k 120k 147k 162k 170k 180k 220k 263k 330k 390k 422k 460k 464k 560k 674k
820k

1M 1.2M 1.5M 1.7M 1.9M 2.2M 2.4M 2.6M 2.8M 3.2M 4M 4.8M 5.6M 6M 8.7M 10M
16M 23.5M
'''[1:-1]

def EIA(series, powers=(0, 1, 2, 3, 4, 5, 6)):
    '''Return a set of EIA resistors.  powers must be an iterable of
    integers giving the desired powers of 10 to use.
    '''
    R = []
    for eia in EIA_series[series]:
        for power in powers:
            R.append(Int(eia*10**power))
    return set(R)

if __name__ == "__main__": 
    if len(sys.argv) < 2:
        print('''Give an EIA series number from
  0, 3, 6, 12, 24, 48, 96, or 192
If you give 0, the on-hand resistor set will be printed.''')
        exit(1)
    allowed = (0, 3, 6, 12, 24, 48, 96, 192)
    n = int(sys.argv[1])
    if n not in allowed:
        print("Your choice must be in", allowed)
        exit(1)
    if n:
        print("EIA {} series:".format(n))
        for i in Columnize(EIA(n, (0,)), indent="  "):
            print(i)
    else:
        print("On-hand resistances in ohms:")
        for i in OnHand.values.split("\n"):
            print(" ", i)
