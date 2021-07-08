'''
Provide commonly-used sizes.
'''

from columnize import Columnize
from frange import frange
from sig import sig
from pdb import set_trace as xx 

__all__ = (
    "negative_gauges number_drills letter_drills clausing_lathe_tpi "
    "US_Standard steel galvanized_steel stainless_steel aluminum zinc "
    "AWG hypodermic_needles stubs_iron_wire Birmingham_iron_wire "
    "Washburn_and_Moen_steel_wire music_wire stubs_steel_wire nylon_twine"
    "TranslateGauge".split())

def TranslateGauge(g):
    '''If g is a negative integer, use negative_gauges to change it to a
    suitable string (e.g., -1 --> "2/0").  Otherwise, convert it to a
    string.
    '''
    if isinstance(g, int):
        if g < 0:
            return negative_gauges[g]
        return str(g)
    elif isinstance(g, str):
        return g
    else:
        return str(g)

negative_gauges = {
    -1: "2/0", -2: "3/0", -3: "4/0", -4: "5/0", -5: "6/0", -6: "7/0"
}

# Number drills (HCP59:F-162)
number_drills = {   # Key = number [1, 80], value = diameter in inches
     1: 0.228 ,    17: 0.173 ,    33: 0.113 ,    49: 0.073 ,    65: 0.035 ,
     2: 0.221 ,    18: 0.1695,    34: 0.111 ,    50: 0.070 ,    66: 0.033 ,
     3: 0.213 ,    19: 0.166 ,    35: 0.110 ,    51: 0.067 ,    67: 0.032 ,
     4: 0.209 ,    20: 0.161 ,    36: 0.1065,    52: 0.0635,    68: 0.031 ,
     5: 0.2055,    21: 0.159 ,    37: 0.104 ,    53: 0.0595,    69: 0.0293,
     6: 0.204 ,    22: 0.157 ,    38: 0.1015,    54: 0.055 ,    70: 0.0280,
     7: 0.201 ,    23: 0.154 ,    39: 0.0995,    55: 0.052 ,    71: 0.026 ,
     8: 0.199 ,    24: 0.152 ,    40: 0.098 ,    56: 0.0465,    72: 0.025 ,
     9: 0.196 ,    25: 0.1495,    41: 0.096 ,    57: 0.043 ,    73: 0.024 ,
    10: 0.1935,    26: 0.147 ,    42: 0.0935,    58: 0.042 ,    74: 0.0225,
    11: 0.191 ,    27: 0.144 ,    43: 0.089 ,    59: 0.041 ,    75: 0.021 ,
    12: 0.189 ,    28: 0.1405,    44: 0.086 ,    60: 0.040 ,    76: 0.020 ,
    13: 0.185 ,    29: 0.136 ,    45: 0.082 ,    61: 0.039 ,    77: 0.018 ,
    14: 0.182 ,    30: 0.1285,    46: 0.081 ,    62: 0.038 ,    78: 0.016 ,
    15: 0.180 ,    31: 0.120 ,    47: 0.0785,    63: 0.037 ,    79: 0.0145,
    16: 0.177 ,    32: 0.116 ,    48: 0.076 ,    64: 0.036 ,    80: 0.0135,
}

# Generate numbered thread sizes in inches by the formula 
# dia = 0.060 + n*0.013 where n is the number size.
numbered_threads = {}
for n in list(range(0, 11)) + [12, 14]:
    numbered_threads[n] = round(0.060 + n*0.013, 3)

letter_drills = { 
    # From:  TAD Universal Reference Calculator, TAD Products Corp., (C) 1964
    "A": 0.234, "B": 0.238, "C": 0.242, "D": 0.246, "E": 0.250, "F": 0.257,
    "G": 0.261, "H": 0.266, "I": 0.272, "J": 0.277, "K": 0.281, "L": 0.290,
    "M": 0.295, "N": 0.302, "O": 0.316, "P": 0.323, "Q": 0.332, "R": 0.339,
    "S": 0.348, "T": 0.358, "U": 0.368, "V": 0.377, "W": 0.386, "X": 0.397,
    "Y": 0.404, "Z": 0.413
}

clausing_lathe_tpi = set((
    4, 4.5, 5, 5.5, 5.75, 6, 6.5, 6.75, 7, 8, 9, 10, 11, 11.5, 12, 13, 13.5, 14, 16,
    18, 20, 22, 23, 24, 26, 27, 28, 32, 36, 40, 44, 46, 48, 52, 54, 56, 64, 72, 80,
    88, 92, 96, 104, 108, 112, 128, 144, 160, 176, 184, 192, 208, 216, 224)
)

# The following were constructed by Dump()

US_Standard = {
    -6: 0.5000, -5: 0.4688, -4: 0.4375, -3: 0.4063, -2: 0.3750, -1: 0.3438,
    0: 0.3125, 1: 0.2813, 2: 0.2656, 3: 0.2500, 4: 0.2344, 5: 0.2188,
    6: 0.2031, 7: 0.1875, 8: 0.1719, 9: 0.1563, 10: 0.1406, 11: 0.1250,
    12: 0.1094, 13: 0.0938, 14: 0.0781, 15: 0.0703, 16: 0.0625, 17: 0.0563,
    18: 0.0500, 19: 0.0438, 20: 0.0375, 21: 0.0344, 22: 0.0313, 23: 0.0281,
    24: 0.0250, 25: 0.0219, 26: 0.0188, 27: 0.0172, 28: 0.0156, 29: 0.0141,
    30: 0.0125, 31: 0.0109, 32: 0.0102, 33: 0.0094, 34: 0.0086, 35: 0.0078,
    36: 0.0070, 37: 0.0066, 38: 0.0063
}

steel = {
    3: 0.2391, 4: 0.2242, 5: 0.2092, 6: 0.1943, 7: 0.1793, 8: 0.1644,
    9: 0.1495, 10: 0.1345, 11: 0.1196, 12: 0.1046, 13: 0.0897, 14: 0.0747,
    15: 0.0673, 16: 0.0598, 17: 0.0538, 18: 0.0478, 19: 0.0418, 20: 0.0359,
    21: 0.0329, 22: 0.0299, 23: 0.0269, 24: 0.0239, 25: 0.0209, 26: 0.0179,
    27: 0.0164, 28: 0.0149, 29: 0.0135, 30: 0.0120, 31: 0.0105, 32: 0.0097,
    33: 0.0090, 34: 0.0082, 35: 0.0075, 36: 0.0067, 37: 0.0064, 38: 0.0060
}

galvanized_steel = {
    8: 0.1681, 9: 0.1532, 10: 0.1382, 11: 0.1233, 12: 0.1084, 13: 0.0934,
    14: 0.0785, 15: 0.0710, 16: 0.0635, 17: 0.0575, 18: 0.0516, 19: 0.0456,
    20: 0.0396, 21: 0.0366, 22: 0.0336, 23: 0.0306, 24: 0.0276, 25: 0.0247,
    26: 0.0217, 27: 0.0202, 28: 0.0187, 29: 0.0172, 30: 0.0157, 31: 0.0142
}

stainless_steel = {
    7: 0.1875, 8: 0.1719, 9: 0.1563, 10: 0.1406, 11: 0.1250, 12: 0.1094,
    13: 0.0940, 14: 0.0781, 15: 0.0700, 16: 0.0625, 17: 0.0560, 18: 0.0500,
    19: 0.0440, 20: 0.0375, 21: 0.0340, 22: 0.0310, 23: 0.0280, 24: 0.0250,
    25: 0.0220, 26: 0.0190, 27: 0.0170, 28: 0.0160, 29: 0.0140, 30: 0.0130,
    31: 0.0110
}

aluminum = {
    6: 0.1620, 7: 0.1443, 8: 0.1285, 9: 0.1144, 10: 0.1019, 11: 0.0907,
    12: 0.0808, 13: 0.0720, 14: 0.0641, 15: 0.0570, 16: 0.0508, 17: 0.0450,
    18: 0.0403, 19: 0.0360, 20: 0.0320, 21: 0.0280, 22: 0.0250, 23: 0.0230,
    24: 0.0200, 25: 0.0180, 26: 0.0170, 27: 0.0140, 28: 0.0126, 29: 0.0113,
    30: 0.0100, 31: 0.0089
}

zinc = {
    3: 0.0060, 4: 0.0080, 5: 0.0100, 6: 0.0120, 7: 0.0140, 8: 0.0160,
    9: 0.0180, 10: 0.0200, 11: 0.0240, 12: 0.0280, 13: 0.0320, 14: 0.0360,
    15: 0.0400, 16: 0.0450, 17: 0.0500, 18: 0.0550, 19: 0.0600, 20: 0.0700,
    21: 0.0800, 22: 0.0900, 23: 0.1000, 24: 0.1250
}

AWG = {  # American Wire Gauge, also known as the Brown and Sharpe gauge
    -3: 0.46, -2: 0.4096, -1: 0.3648, 0: 0.3249, 1: 0.2893, 2: 0.2576,
    3: 0.2294, 4: 0.2043, 5: 0.1819, 6: 0.162, 7: 0.1443, 8: 0.1285, 9:
    0.1144, 10: 0.1019, 11: 0.0907, 12: 0.0808, 13: 0.072, 14: 0.0641,
    15: 0.0571, 16: 0.0508, 17: 0.0453, 18: 0.0403, 19: 0.0359, 20:
    0.032, 21: 0.0285, 22: 0.0253, 23: 0.0226, 24: 0.0201, 25: 0.0179,
    26: 0.0159, 27: 0.0142, 28: 0.0126, 29: 0.0113, 30: 0.01, 31:
    0.0089, 32: 0.008, 33: 0.0071, 34: 0.0063, 35: 0.0056, 36: 0.005,
    37: 0.0045, 38: 0.004, 39: 0.0035, 40: 0.0031, 41: 0.0028, 42:
    0.0025, 43: 0.0022, 44: 0.002, 45: 0.00176, 46: 0.00157, 47: 0.0014,
    48: 0.00124
}

hypodermic_needles = {  # OD in inches
    6: 0.2030, 7: 0.1800, 8: 0.1650, 9: 0.1480, 10: 0.1340, 11: 0.1200,
    12: 0.1090, 13: 0.0950, 14: 0.0830, 15: 0.0720, 16: 0.0650, 17:
    0.0580, 18: 0.0500, 19: 0.0420, 20: 0.0358, 21: 0.0323, 22: 0.0283,
    23: 0.0253, 24: 0.0223, 25: 0.0203, 26: 0.0183, 27: 0.0163, 28:
    0.0143, 29: 0.0133, 30: 0.0123, 31: 0.0103
}

stubs_iron_wire = {
    # From https://www.engineeringtoolbox.com/standard-gauges-d_1345.html
    -3: 0.454, -2: 0.425, -1: 0.38, 0: 0.34, 1: 0.3, 2: 0.284, 3: 0.259,
    4: 0.238, 5: 0.22, 6: 0.203, 7: 0.18, 8: 0.165, 9: 0.148, 10: 0.134,
    11: 0.12, 12: 0.109, 13: 0.095, 14: 0.083, 15: 0.072, 16: 0.065,
    17: 0.058, 18: 0.049, 19: 0.042, 20: 0.035, 21: 0.032, 22: 0.028,
    23: 0.025, 24: 0.022, 25: 0.02, 26: 0.018, 27: 0.016, 28: 0.014,
    29: 0.013, 30: 0.012, 31: 0.01, 32: 0.009, 33: 0.008, 34: 0.007,
    35: 0.005, 36: 0.004
}

Birmingham_iron_wire = {
    # From https://www.engineeringtoolbox.com/standard-gauges-d_1345.html
    -3: 0.454, -2: 0.425, -1: 0.38, 0: 0.34, 1: 0.3, 2: 0.284, 3: 0.259,
    4: 0.238, 5: 0.22, 6: 0.203, 7: 0.18, 8: 0.165, 9: 0.148, 10: 0.134,
    11: 0.12, 12: 0.109, 13: 0.095, 14: 0.083, 15: 0.072, 16: 0.065,
    17: 0.058, 18: 0.049, 19: 0.042, 20: 0.035, 21: 0.032, 22: 0.028,
    23: 0.025, 24: 0.022, 25: 0.02, 26: 0.018, 27: 0.016, 28: 0.014,
    29: 0.013, 30: 0.012, 31: 0.01, 32: 0.009, 33: 0.008, 34: 0.007,
    35: 0.005, 36: 0.004,
}

Washburn_and_Moen_steel_wire = {
    # From https://www.engineeringtoolbox.com/standard-gauges-d_1345.html
    -6: 0.49, -5: 0.462, -4: 0.431, -3: 0.394, -2: 0.363, -1: 0.331,
    0: 0.307, 1: 0.283, 2: 0.263, 3: 0.244, 4: 0.225, 5: 0.207, 6: 0.192,
    7: 0.177, 8: 0.162, 9: 0.148, 10: 0.135, 11: 0.121, 12: 0.106, 13: 0.092,
    14: 0.08, 15: 0.072, 16: 0.063, 17: 0.054, 18: 0.048, 19: 0.041,
    20: 0.035, 21: 0.032, 22: 0.029, 23: 0.026, 24: 0.023, 25: 0.02,
    26: 0.018, 27: 0.017, 28: 0.016, 29: 0.015, 30: 0.014, 31: 0.013,
    32: 0.013, 33: 0.012, 34: 0.01, 35: 0.0095, 36: 0.009, 37: 0.0085,
    38: 0.008, 39: 0.0075, 40: 0.007
}

music_wire = {
    # From https://www.engineeringtoolbox.com/standard-gauges-d_1345.html
    -5: 0.004, -4: 0.005, -3: 0.006, -2: 0.007, -1: 0.008, 0: 0.009,
    1: 0.01, 2: 0.011, 3: 0.012, 4: 0.013, 5: 0.014, 6: 0.016, 7: 0.018,
    8: 0.02, 9: 0.022, 10: 0.024, 11: 0.026, 12: 0.029, 13: 0.031, 14: 0.033,
    15: 0.035, 16: 0.037, 17: 0.039, 18: 0.041, 19: 0.043, 20: 0.045,
    21: 0.047, 22: 0.049, 23: 0.051, 24: 0.055, 25: 0.059, 26: 0.063,
    27: 0.067, 28: 0.071, 29: 0.075, 30: 0.08, 31: 0.085, 32: 0.09,
    33: 0.095
}

stubs_steel_wire = {
    # From https://www.engineeringtoolbox.com/standard-gauges-d_1345.html
    1: 0.227, 2: 0.219, 3: 0.212, 4: 0.207, 5: 0.204, 6: 0.201, 7: 0.199,
    8: 0.197, 9: 0.194, 10: 0.191, 11: 0.188, 12: 0.185, 13: 0.182, 14: 0.18,
    15: 0.178, 16: 0.175, 17: 0.172, 18: 0.168, 19: 0.164, 20: 0.161, 21:
    0.157, 22: 0.155, 23: 0.153, 24: 0.151, 25: 0.148, 26: 0.146, 27: 0.143,
    28: 0.139, 29: 0.134, 30: 0.127, 31: 0.12, 32: 0.115, 33: 0.112, 34: 0.11,
    35: 0.108, 36: 0.106, 37: 0.103, 38: 0.101, 39: 0.099, 40: 0.097,
}

nylon_twine = {
    # From https://l-36.com/twine_size.php
    # I've read there are at least two size series in use and there are
    # no standards.
    4: 0.026, 5: 0.030, 6: 0.033, 7: 0.036, 9: 0.042, 12: 0.047, 15:
    0.052, 18: 0.060, 21: 0.067, 24: 0.073, 30: 0.078, 36: 0.085, 42:
    0.092, 60: 0.116, 72: 0.125
}

def Dump():
    '''Dump the sheet metal gauges to stdout.  This is used to prepare the
    tables for inclusion in this document.  The output will be a dictionary
    keyed by the integer gauge number (-1 for 2/0, -2 for 3/0, etc.) and
    the diameter in decimal inches.
    '''
    sheet_metal_gauges = '''
From https://en.wikipedia.org/wiki/Sheet_metal#Gauge

A = US Standard for sheet and plate
B = Steel MH27
C = Galvanized steel
D = Stainless steel
E = Aluminum
F = Zinc

Dimension in inches (mm)
       
       A               B              C              D               E               F
7/0, 0.5000 (12.70), ......       , ......       , ......       ,  ......       ,  ......
6/0, 0.4688 (11.91), ......       , ......       , ......       ,  ......       ,  ......
5/0, 0.4375 (11.11), ......       , ......       , ......       ,  ......       ,  ......
4/0, 0.4063 (10.32), ......       , ......       , ......       ,  ......       ,  ......
3/0, 0.3750 (9.53) , ......       , ......       , ......       ,  ......       ,  ......
2/0, 0.3438 (8.73) , ......       , ......       , ......       ,  ......       ,  ......
0  , 0.3125 (7.94) , ......       , ......       , ......       ,  ......       ,  ......
1  , 0.2813 (7.15) , ......       , ......       , ......       ,  ......       ,  ......
2  , 0.2656 (6.75) , ......       , ......       , ......       ,  ......       ,  ......
3  , 0.2500 (6.35) , 0.2391 (6.07), ......       , ......       ,  ......       ,  0.006 (0.15)
4  , 0.2344 (5.95) , 0.2242 (5.69), ......       , ......       ,  ......       ,  0.008 (0.20)
5  , 0.2188 (5.56) , 0.2092 (5.31), ......       , ......       ,  ......       ,  0.010 (0.25)
6  , 0.2031 (5.16) , 0.1943 (4.94), ......       , ......       ,  0.162 (4.1)  ,  0.012 (0.30)
7  , 0.1875 (4.76) , 0.1793 (4.55), ......       , 0.1875 (4.76),  0.1443 (3.67),  0.014 (0.36)
8  , 0.1719 (4.37) , 0.1644 (4.18), 0.1681 (4.27), 0.1719 (4.37),  0.1285 (3.26),  0.016 (0.41)
9  , 0.1563 (3.97) , 0.1495 (3.80), 0.1532 (3.89), 0.1563 (3.97),  0.1144 (2.91),  0.018 (0.46)
10 , 0.1406 (3.57) , 0.1345 (3.42), 0.1382 (3.51), 0.1406 (3.57),  0.1019 (2.59),  0.020 (0.51)
11 , 0.1250 (3.18) , 0.1196 (3.04), 0.1233 (3.13), 0.1250 (3.18),  0.0907 (2.30),  0.024 (0.61)
12 , 0.1094 (2.78) , 0.1046 (2.66), 0.1084 (2.75), 0.1094 (2.78),  0.0808 (2.05),  0.028 (0.71)
13 , 0.0938 (2.38) , 0.0897 (2.28), 0.0934 (2.37), 0.094 (2.4)  ,  0.072 (1.8)  ,  0.032 (0.81)
14 , 0.0781 (1.98) , 0.0747 (1.90), 0.0785 (1.99), 0.0781 (1.98),  0.0641 (1.63),  0.036 (0.91)
15 , 0.0703 (1.79) , 0.0673 (1.71), 0.0710 (1.80), 0.07 (1.8)   ,  0.057 (1.4)  ,  0.040 (1.0)
16 , 0.0625 (1.59) , 0.0598 (1.52), 0.0635 (1.61), 0.0625 (1.59),  0.0508 (1.29),  0.045 (1.1)
17 , 0.0563 (1.43) , 0.0538 (1.37), 0.0575 (1.46), 0.056 (1.4)  ,  0.045 (1.1)  ,  0.050 (1.3)
18 , 0.0500 (1.27) , 0.0478 (1.21), 0.0516 (1.31), 0.0500 (1.27),  0.0403 (1.02),  0.055 (1.4)
19 , 0.0438 (1.11) , 0.0418 (1.06), 0.0456 (1.16), 0.044 (1.1)  ,  0.036 (0.91) ,  0.060 (1.5)
20 , 0.0375 (0.95) , 0.0359 (0.91), 0.0396 (1.01), 0.0375 (0.95),  0.0320 (0.81),  0.070 (1.8)
21 , 0.0344 (0.87) , 0.0329 (0.84), 0.0366 (0.93), 0.034 (0.86) ,  0.028 (0.71) ,  0.080 (2.0)
22 , 0.0313 (0.80) , 0.0299 (0.76), 0.0336 (0.85), 0.031 (0.79) ,  0.025 (0.64) ,  0.090 (2.3)
23 , 0.0281 (0.71) , 0.0269 (0.68), 0.0306 (0.78), 0.028 (0.71) ,  0.023 (0.58) ,  0.100 (2.5)
24 , 0.0250 (0.64) , 0.0239 (0.61), 0.0276 (0.70), 0.025 (0.64) ,  0.02 (0.51)  ,  0.125 (3.2)
25 , 0.0219 (0.56) , 0.0209 (0.53), 0.0247 (0.63), 0.022 (0.56) ,  0.018 (0.46) ,  ......
26 , 0.0188 (0.48) , 0.0179 (0.45), 0.0217 (0.55), 0.019 (0.48) ,  0.017 (0.43) ,  ......
27 , 0.0172 (0.44) , 0.0164 (0.42), 0.0202 (0.51), 0.017 (0.43) ,  0.014 (0.36) ,  ......
28 , 0.0156 (0.40) , 0.0149 (0.38), 0.0187 (0.47), 0.016 (0.41) ,  0.0126 (0.32),  ......
29 , 0.0141 (0.36) , 0.0135 (0.34), 0.0172 (0.44), 0.014 (0.36) ,  0.0113 (0.29),  ......
30 , 0.0125 (0.32) , 0.0120 (0.30), 0.0157 (0.40), 0.013 (0.33) ,  0.0100 (0.25),  ......
31 , 0.0109 (0.28) , 0.0105 (0.27), 0.0142 (0.36), 0.011 (0.28) ,  0.0089 (0.23),  ......
32 , 0.0102 (0.26) , 0.0097 (0.25), ......       , ......       ,  ......       ,  ......
33 , 0.0094 (0.24) , 0.0090 (0.23), ......       , ......       ,  ......       ,  ......
34 , 0.0086 (0.22) , 0.0082 (0.21), ......       , ......       ,  ......       ,  ......
35 , 0.0078 (0.20) , 0.0075 (0.19), ......       , ......       ,  ......       ,  ......
36 , 0.0070 (0.18) , 0.0067 (0.17), ......       , ......       ,  ......       ,  ......
37 , 0.0066 (0.17) , 0.0064 (0.16), ......       , ......       ,  ......       ,  ......
38 , 0.0063 (0.16) , 0.0060 (0.15), ......       , ......       ,  ......       ,  ......
'''
    def Fix(fields):
        for i, f in enumerate(fields):
            loc = f.find("(")
            if loc != -1:
                fields[i] = f[:loc].strip()
            if f == "......":
                fields[i] = ""
        return fields
    s = []
    for line in sheet_metal_gauges.split("\n")[13:]:
        line = line.strip()
        if not line:
            continue
        f = [i.strip() for i in line.split(",")]
        s.append(Fix(f))
    # Now dump each gauge's dictionary
    tr = { '7/0':-6, '6/0':-5, '5/0':-4, '4/0':-3, '3/0':-2, '2/0':-1}
    indent = " "*3
    # US Standard (column A)
    print("US_Standard = {")
    for i in s:
        key, val = i[0], i[1]
        if key in tr:
            key = tr[key]
        gauge_number = int(key)
        print(indent, "{}: {:.4f},".format(gauge_number, float(val)))
    print("}")
    def Others(name, column):
        print("{} = {{".format(name))
        for i in s:
            key, val = i[0], i[column]
            if key in tr:
                key = tr[key]
            if not val:
                continue
            gauge_number = int(key)
            print(indent, "{}: {:.4f},".format(gauge_number, float(val)))
        print("}")
    Others("steel", 2)
    Others("galvanized_steel", 3)
    Others("stainless_steel", 4)
    Others("aluminum", 5)
    Others("zinc", 6)

def WrenchSizes():
    print("\n{:^70s}".format("Wrench Sizes"))
    inch_sizes = (list(frange("3/16", "17/16", "1/16", include_end=True)) +
                  list(frange("18/16", "24/16", "1/16", include_end=True)) +
                  list(frange("13/8", "2", "1/8", include_end=True))
                  )
    mm_sizes = list(sorted((list(range(3, 25)) + 
                    [5.5, 26, 27, 28, 30, 32, 34, 36, 38, 41, 42, 
                     45, 46, 48, 50])))
    mm_sizes = [str(i) for i in mm_sizes]
    sizes, results = [], ["Decimal Frac    mm"]
    single_column = False
    for i in inch_sizes:
        sizes.append((float(i), str(i)))
    for i in mm_sizes:
        sizes.append((float(i)/25.4, i + " mm"))
    sizes = sorted(sizes)  # Sort by size in decimal inches
    #      Dec in   Frac   mm
    if single_column:
        fmt = "{:5.3f}\t{:^7s}\t{:^6s}"
    else:
        fmt = "{:5.3f}  {:^7s} {:^6s}"
    for inches, size in sizes:
        if "mm" in size:
            s = fmt.format(inches, "", size.replace("mm", ""))
        else:
            mm = str(round(inches*25.4, 2))
            s = fmt.format(inches, size, mm)
        results.append(s)
    if single_column:
        results[0] = "Decimal\tFrac\tmm"
        for i in results:
            print(i)
    else:
        for i in Columnize(results):
            print(i)

def Get(gauge):
    if isinstance(gauge, str):
        return gauge
    elif gauge < 0:
        return negative_gauges[gauge]
    else:
        return str(gauge)

def Print(dictionary, name, nl=True, custom=None):
    header, s = "Size  inches   mm", []
    print("{:^70s}".format(name))
    for gauge, inches in dictionary.items():
        if custom:
            inch = custom[0].format(inches)
            mm = custom[1].format(inches*25.4)
            s.append([gauge, "{:s} {:s}".format(inch, mm)])
        else:
            s.append([gauge, "{:7.4f} {:6.3f}".format(inches, inches*25.4)])
    s = sorted(s)
    for i, item in enumerate(s):
        gauge, sizes = item
        s[i] = "{:^5s}".format(Get(gauge)) + sizes
    s.insert(0, header)
    for i in Columnize(s):
        print(i)
    if nl:
        print()

if __name__ == "__main__": 
    # Dump these gauges to stdout
    print("In the following, -1 means 00, -2 means 000, etc.\n")
    Print(number_drills, "Number Drills")
    Print(letter_drills, "Letter Drills")
    print("{:^70s}".format("Clausing lathe threads in tpi"))
    s = [str(i) for i in sorted(list(clausing_lathe_tpi))]
    for i in Columnize(s, columns=8, col_width=9):
        print(i)
    print()
    Print(US_Standard, "US Standard sheet metal gauge")
    Print(steel, "Steel sheet metal gauge")
    Print(galvanized_steel, "Galvanized steel sheet metal gauge")
    Print(stainless_steel, "Stainless steel sheet metal gauge")
    Print(aluminum, "Aluminum sheet metal gauge")
    Print(zinc, "Zinc sheet metal gauge")
    Print(nylon_twine, "Nylon Twine", custom=["{:7.3f}", "{:6.2f}"])
    Print(hypodermic_needles, "Hypodermic Needles")
    #
    Print(stubs_iron_wire, "Stubs' iron wire gauge")
    Print(Birmingham_iron_wire, "Birmingham iron wire gauge (same as Stubs' iron wire gauge)")
    Print(Washburn_and_Moen_steel_wire, "Washburn and Moen steel wire")
    Print(music_wire, "Music wire")
    Print(stubs_steel_wire, "Stubs' steel wire")
    #
    Print(numbered_threads, "US numbered thread sizes")
    Print(AWG, "American Wire Gauge (AWG, Brown & Sharpe)", nl=False)
    print("    An increase of 6 gauge numbers about halves the diameter")
    #
    WrenchSizes()