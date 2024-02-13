'''
Fit the YSI thermistor data to a suitable function.

The equation is similar to the Steinhart-Hart equation:
    1/T = A[0] + A[1]*ln(R) + A[2]*ln(R)**2 + A[3]*ln(R)**3
were T is temperature in K and R is resistance in ohms.

Results:  
    A[0] = 9.503704e-04
    A[1] = 2.163135e-04
    A[2] = 4.939487e-07
    A[3] = 1.105645e-07
Max relative residual = 0.078%

A plot of the relative residuals shows that the predictions for
temperatures less than 30 degC have relative residuals less than 0.02%.
The largest relative residuals are for temperatures above 30 degC.

Here are the results of the regression for temperatures in degC (worst
prediction is at 149 degC with a residual of 0.33 K).

    Actual T vs. Predicted T, residual (all in degC)
    -40.0 -40.0  0.02
    -39.0 -39.0  0.01
    -38.0 -38.0  0.01
    -37.0 -37.0  0.01
    -36.0 -36.0  0.01
    -35.0 -35.0  0.00
    -34.0 -34.0  0.00
    -33.0 -33.0  0.00
    -32.0 -32.0  0.00
    -31.0 -31.0 -0.00
    -30.0 -30.0 -0.00
    -29.0 -29.0 -0.00
    -28.0 -28.0 -0.00
    -27.0 -27.0 -0.00
    -26.0 -26.0 -0.01
    -25.0 -25.0 -0.01
    -24.0 -24.0 -0.01
    -23.0 -23.0 -0.01
    -22.0 -22.0 -0.01
    -21.0 -21.0 -0.01
    -20.0 -20.0 -0.01
    -19.0 -19.0 -0.01
    -18.0 -18.0 -0.01
    -17.0 -17.0 -0.01
    -16.0 -16.0 -0.00
    -15.0 -15.0 -0.01
    -14.0 -14.0 -0.01
    -13.0 -13.0 -0.01
    -12.0 -12.0 -0.01
    -11.0 -11.0 -0.01
    -10.0 -10.0 -0.00
    -9.0  -9.0 -0.01
    -8.0  -8.0 -0.01
    -7.0  -7.0 -0.00
    -6.0  -6.0 -0.01
    -5.0  -5.0 -0.01
    -4.0  -4.0  0.00
    -3.0  -3.0  0.00
    -2.0  -2.0  0.00
    -1.0  -1.0  0.00
    0.0   0.0  0.00
    1.0   1.0  0.00
    2.0   2.0  0.00
    3.0   3.0  0.00
    4.0   4.0  0.00
    5.0   5.0  0.00
    6.0   6.0  0.00
    7.0   7.0  0.00
    8.0   8.0  0.00
    9.0   9.0  0.00
    10.0  10.0  0.00
    11.0  11.0  0.00
    12.0  12.0  0.00
    13.0  13.0  0.00
    14.0  14.0  0.00
    15.0  15.0  0.00
    16.0  16.0  0.00
    17.0  17.0  0.00
    18.0  18.0  0.00
    19.0  19.0  0.01
    20.0  20.0  0.01
    21.0  21.0  0.00
    22.0  22.0  0.00
    23.0  23.0  0.00
    24.0  24.0  0.01
    25.0  25.0  0.00
    26.0  26.0  0.01
    27.0  27.0  0.01
    28.0  28.0  0.00
    29.0  29.0  0.00
    30.0  30.0  0.00
    31.0  31.0  0.00
    32.0  32.0  0.01
    33.0  33.0  0.00
    34.0  34.0 -0.00
    35.0  35.0  0.01
    36.0  36.0  0.00
    37.0  37.0 -0.00
    38.0  38.0  0.00
    39.0  39.0  0.01
    40.0  40.0  0.00
    41.0  41.0  0.01
    42.0  42.0  0.01
    43.0  43.0  0.00
    44.0  44.0  0.01
    45.0  45.0 -0.00
    46.0  46.0  0.01
    47.0  47.0  0.01
    48.0  48.0  0.01
    49.0  49.0  0.01
    50.0  50.0  0.01
    51.0  51.0 -0.01
    52.0  52.0  0.00
    53.0  53.0 -0.00
    54.0  54.0  0.01
    55.0  55.0  0.00
    56.0  56.0  0.01
    57.0  57.0 -0.01
    58.0  58.0 -0.01
    59.0  59.0 -0.01
    60.0  60.0 -0.00
    61.0  61.0  0.01
    62.0  62.0 -0.01
    63.0  63.0  0.00
    64.0  64.0  0.02
    65.0  65.0 -0.01
    66.0  66.0  0.00
    67.0  67.0  0.00
    68.0  68.0 -0.00
    69.0  69.0 -0.02
    70.0  70.0 -0.00
    71.0  71.0  0.00
    72.0  72.0 -0.01
    73.0  73.0  0.01
    74.0  74.0  0.02
    75.0  75.0 -0.01
    76.0  76.0  0.01
    77.0  77.0 -0.01
    78.0  78.0  0.02
    79.0  79.0  0.00
    80.0  80.0  0.03
    81.0  81.0  0.01
    82.0  82.0  0.02
    83.0  83.0 -0.01
    84.0  84.0 -0.01
    85.0  85.0  0.04
    86.0  86.0  0.02
    87.0  87.0  0.04
    88.0  88.0 -0.01
    89.0  89.0 -0.03
    90.0  90.0 -0.01
    91.0  91.1  0.05
    92.0  92.0  0.03
    93.0  93.0  0.04
    94.0  94.0 -0.05
    95.0  95.0  0.03
    96.0  96.0  0.01
    97.0  97.0  0.03
    98.0  97.9 -0.07
    99.0  99.0  0.02
    100.0 100.0 -0.02
    101.0 101.0 -0.02
    102.0 102.0  0.02
    103.0 103.1  0.09
    104.0 104.0  0.01
    105.0 105.0 -0.04
    106.0 105.9 -0.05
    107.0 107.0 -0.04
    108.0 108.0  0.02
    109.0 109.1  0.11
    110.0 110.0  0.01
    111.0 110.9 -0.06
    112.0 111.9 -0.11
    113.0 112.9 -0.12
    114.0 113.9 -0.10
    115.0 115.0 -0.04
    116.0 116.1  0.05
    117.0 116.9 -0.10
    118.0 118.1  0.06
    119.0 119.0 -0.04
    120.0 119.9 -0.11
    121.0 120.8 -0.15
    122.0 122.2  0.17
    123.0 122.9 -0.15
    124.0 123.9 -0.10
    125.0 125.0 -0.01
    126.0 126.1  0.11
    127.0 126.9 -0.12
    128.0 128.1  0.07
    129.0 128.9 -0.11
    130.0 130.2  0.16
    131.0 131.0  0.03
    132.0 131.9 -0.07
    133.0 132.9 -0.15
    134.0 133.8 -0.20
    135.0 135.3  0.27
    136.0 136.3  0.29
    137.0 136.8 -0.19
    138.0 137.9 -0.12
    139.0 139.0 -0.02
    140.0 140.1  0.12
    141.0 141.3  0.29
    142.0 141.9 -0.10
    143.0 143.1  0.14
    144.0 143.8 -0.23
    145.0 145.1  0.08
    146.0 145.8 -0.24
    147.0 147.1  0.14
    148.0 147.9 -0.14
    149.0 149.3  0.33
    150.0 150.1  0.09

----------------------------------------------------------------------

https://www.mathscinotes.com/2011/07/thermistor-mathematics/ shows an
approximate method of linearizing a thermistor by putting a resistor in
series with it to make a voltage divider.
'''

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
from pylab import *
import scipy
import scipy.optimize
from scipy.optimize.minpack import leastsq
import sys

ln = log
k = 273.15

# Temp in deg C, R in kohm
data = '''
    -40 884.6
    -39 830.9
    -38 780.8
    -37 733.9
    -36 690.2
    -35 649.3
    -34 611
    -33 575.2
    -32 541.7
    -31 510.4
    -30 481
    -29 453.5
    -28 427.7
    -27 403.5
    -26 380.9
    -25 359.6
    -24 339.6
    -23 320.9
    -22 303.3
    -21 286.7
    -20 271.2
    -19 256.5
    -18 242.8
    -17 229.8
    -16 217.6
    -15 206.2
    -14 195.4
    -13 185.2
    -12 175.6
    -11 166.6
    -10 158
    -9 150
    -8 142.4
    -7 135.2
    -6 128.5
    -5 122.1
    -4 116
    -3 110.3
    -2 104.9
    -1 99.8
    0 94.98
    1 90.41
    2 86.09
    3 81.99
    4 78.11
    5 74.44
    6 70.96
    7 67.66
    8 64.53
    9 61.56
    10 58.75
    11 56.07
    12 53.54
    13 51.13
    14 48.84
    15 46.67
    16 44.6
    17 42.64
    18 40.77
    19 38.99
    20 37.3
    21 35.7
    22 34.17
    23 32.71
    24 31.32
    25 30
    26 28.74
    27 27.54
    28 26.4
    29 25.31
    30 24.27
    31 23.28
    32 22.33
    33 21.43
    34 20.57
    35 19.74
    36 18.96
    37 18.21
    38 17.49
    39 16.8
    40 16.15
    41 15.52
    42 14.92
    43 14.35
    44 13.8
    45 13.28
    46 12.77
    47 12.29
    48 11.83
    49 11.39
    50 10.97
    51 10.57
    52 10.18
    53 9.81
    54 9.45
    55 9.11
    56 8.78
    57 8.47
    58 8.17
    59 7.88
    60 7.6
    61 7.33
    62 7.08
    63 6.83
    64 6.59
    65 6.37
    66 6.15
    67 5.94
    68 5.74
    69 5.55
    70 5.36
    71 5.18
    72 5.01
    73 4.84
    74 4.68
    75 4.53
    76 4.38
    77 4.24
    78 4.1
    79 3.97
    80 3.84
    81 3.72
    82 3.6
    83 3.49
    84 3.38
    85 3.27
    86 3.17
    87 3.07
    88 2.98
    89 2.89
    90 2.8
    91 2.71
    92 2.63
    93 2.55
    94 2.48
    95 2.4
    96 2.33
    97 2.26
    98 2.2
    99 2.13
    100 2.07
    101 2.01
    102 1.95
    103 1.89
    104 1.84
    105 1.79
    106 1.74
    107 1.69
    108 1.64
    109 1.59
    110 1.55
    111 1.51
    112 1.47
    113 1.43
    114 1.39
    115 1.35
    116 1.31
    117 1.28
    118 1.24
    119 1.21
    120 1.18
    121 1.15
    122 1.11
    123 1.09
    124 1.06
    125 1.03
    126 1
    127 0.98
    128 0.95
    129 0.93
    130 0.9
    131 0.88
    132 0.86
    133 0.84
    134 0.82
    135 0.79
    136 0.77
    137 0.76
    138 0.74
    139 0.72
    140 0.7
    141 0.68
    142 0.67
    143 0.65
    144 0.64
    145 0.62
    146 0.61
    147 0.59
    148 0.58
    149 0.56
    150 0.55
'''

def PlotModel(a, b, c, d, T, R):
    plot(ln(R), 1/T)
    plot(ln(R), Model(a, b, c, d, R))
    grid()
    show()
    #savefig("a.png", dpi=200)

def Model(A, R):
    t = ln(R)
    return A[0] + A[1]*t + A[2]*t*t + A[3]*t*t*t

def objective(A, t, y0, func):
    # Residual of model and data
    return y0 - func(A, t)

if __name__ == "__main__": 
    # Convert data into an array of number pairs
    d = []
    for i in data.split("\n"):
        i = i.strip()
        if not i or i[0] == "#":
            continue
        d.append([float(j) for j in i.split()])

    # Get the data into numpy arrays
    a = array(d)
    T = a[:, 0] + k          # Temperature in K
    R = a[:, 1]*1000         # Resistance in ohms

    A0 = (2.508e-3, 2.425e-4, 1e-7, 4.415e-7)
    param = (R, 1/T, Model)     # x, y, function
    # Perform the regression
    A, cov_x, infodict, mesg, ier = leastsq(objective, A0, args=param,
                                            full_output=True)
    if ier != 1:
        print("No fit!")
        print(mesg)
        exit(1)
    y_final = Model(A, R)
    chi2 = sum((1/T - y_final)**2/y_final)

    # Print parameters
    print("Model:  1/T = A[0] + A[1]*x + A[2]*x*x + A[3]*x**3 where x = ln(R)")
    print("Regression parameters:")
    for i in range(len(A)):
        print("A[%d] = %e" % (i, A[i]))
    print("Covariance matrix:")
    print(cov_x)

    # Plot the fitted curve
    if len(sys.argv) > 1:
        a, b, c, d = A
        oot = a + b*ln(R) + c*ln(R)**2 + d*ln(R)**3
        semilogy(T, R, ".", label="data")
        semilogy(1/oot, R, label="fitted")
        title("Fitted Function")
        xlabel("Temperature, K")
        ylabel("Resistance, ohms")
        grid()
        legend(loc="upper right")
        show()

    # Plot the relative residuals
    residuals = 100*(Model(A, R) - 1/T)/(1/T)
    if len(sys.argv) > 1:
        if 0:
            # Print the relative residuals
            print("\nRelative residuals in %:")
            print(residuals)
        semilogx(R, residuals)
        title("Relative Residuals")
        xlabel("Resistance, ohms")
        ylabel("Relative Residual, %")
        grid()
        show()
    print(f"Max relative residual = {max(abs(residuals)):.3f}%")

    if 1:
        # Print the actual vs. predicted temperatures
        print("\nActual T vs. Predicted T, residual (all in degC)")
        M = Model(A, R)
        r = lambda x: round(x, 1)
        for i in range(len(T)):
            T_actual = T[i] - k
            T_pred = 1/M[i] - k
            diff = round(T_pred - T_actual, 2)
            print(f"{r(T_actual):5.1f} {r(T_pred):5.1f} {diff: .2f}")
