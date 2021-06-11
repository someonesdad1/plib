'''
Dictionary of various gauge sizes for sheet and wire
    A gauge size of -1 means 00, -2 means 000, etc.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2013 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <shop> Dictionary of various gauge sizes for sheet and wire
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from pdb import set_trace as xx 
if 1:   # Custom imports
    try:
        from f import flt
        have_flt = True
    except ImportError:
        have_flt = False
if 1:   # Global variables
    __all__ = ["gauges", "GetGauge"]
    gauges, urls = {}, {}
def Convert(text):
    ''' Given the string text, put the indicated data into the global dict
    gauges under the key on the first comment line.  The value is a
    dictionary relating gauge size to diameter or thickness in inches.

    If the f.py module is available, the dimension in inches is stored
    as a f.flt object with units of inches.  Otherwise, it's a plain
    float.
    '''
    global gauges
    d, s = {}, []
    for i, line in enumerate(text.strip().split("\n")):
        if i == 0:
            # First line gives the key
            key = line[2:]
        elif i == 1:
            # Second line is the URL for the data
            url = line.strip()
            if url.startswith("#"):
                url = url[1:].strip()
        else:
            line = line.strip()
            if not line or line[0] == "#":
                continue
            s.append(line)
    s = ' '.join(s)
    for item in s.split(","):
        item = item.strip()
        if not item:
            continue
        n, dia = item.split()
        try:
            if have_flt:
                d[int(n)] = flt(dia, units="inches")
            else:
                d[int(n)] = float(dia)
        except Exception:
            if have_flt:
                d[n] = flt(dia, units="inches")
            else:
                d[n] = float(dia)
    gauges[key] = d
    urls[key] = url
def GetGauge(gauge):
    try:
        return gauges[gauge]
    except KeyError:
        try:
            return gauges[synonyms[gauge]]
        except KeyError:
            print("Gauge '{}' not found".format(gauge))
            exit(1)
if 1:   # Data
    _temp = '''
    # US Standard steel sheet
    # From https://www.unc.edu/~rowlett/units/scales/sheetmetal.html
    # Gauge number, diameter in inches

        3 0.2391, 4 0.2242, 5 0.2092, 6 0.1943, 7 0.1793, 8 0.1644, 9
        0.1495, 10 0.1345, 11 0.1196, 12 0.1046, 13 0.0897, 14 0.0747, 15
        0.0673, 16 0.0598, 17 0.0538, 18 0.0478, 19 0.0418, 20 0.0359, 21
        0.0329, 22 0.0299, 23 0.0269, 24 0.0239, 25 0.0209, 26 0.0179, 27
        0.0164, 28 0.0149, 29 0.0135, 30 0.012, 31 0.0105, 32 0.0097, 33
        0.009, 34 0.0082, 35 0.0075, 36 0.0067

    '''
    Convert(_temp)
    _temp = '''
    # Galvanized steel sheet
    # From https://www.unc.edu/~rowlett/units/scales/sheetmetal.html
    # Gauge number, diameter in inches

        9 0.1532, 10 0.1382, 11 0.1233, 12 0.1084, 13 0.0934, 14 0.0785, 15
        0.071, 16 0.0635, 17 0.0575, 18 0.0516, 19 0.0456, 20 0.0396, 21
        0.0366, 22 0.0336, 23 0.0306, 24 0.0276, 25 0.0247, 26 0.0217, 27
        0.0202, 28 0.0187, 29 0.0172, 30 0.0157, 31 0.0142, 32 0.0134

    '''
    Convert(_temp)
    _temp = '''
    # Aluminum sheet
    # From https://www.unc.edu/~rowlett/units/scales/sheetmetal.html
    # Gauge number, diameter in inches

        3 0.2294, 4 0.2043, 5 0.1819, 6 0.162, 7 0.1443, 8 0.1285, 9 0.1144,
        10 0.1019, 11 0.0907, 12 0.0808, 13 0.072, 14 0.0641, 15 0.0571, 16
        0.0508, 17 0.0453, 18 0.0403, 19 0.0359, 20 0.032, 21 0.0285, 22
        0.0253, 23 0.0226, 24 0.0201, 25 0.0179, 26 0.0159, 27 0.0142, 28
        0.0126, 29 0.0113, 30 0.01, 31 0.0089, 32 0.008, 33 0.0071, 34
        0.0063, 35 0.0056

    '''
    Convert(_temp)
    _temp = '''
    # AWG
    # From https://sizes.com/materials/wire.htm
    # Gauge number, diameter in inches
    # -1 == 00, -2 == 000, -3 == 0000

        -5  0.58, -4  0.5165, -3  0.46, -2  0.4096, -1  0.3648, 0  0.3249, 1
        0.2893, 2 0.2576, 3  0.2294, 4  0.2043, 5  0.1819, 6  0.162, 7
        0.1443, 8  0.1285, 9 0.1144, 10  0.1019, 11  0.0907, 12  0.0808, 13
        0.072, 14  0.0641, 15  0.0571, 16  0.0508, 17  0.0453, 18  0.0403,
        19  0.0359, 20  0.032, 21  0.0285, 22 0.0253, 23  0.0226, 24
        0.0201, 25  0.0179, 26  0.0159, 27  0.0142, 28  0.0126, 29  0.0113,
        30  0.01, 31  0.0089, 32  0.008, 33  0.0071, 34  0.0063, 35 0.0056,
        36  0.005, 37  0.0045, 38  0.004, 39  0.0035, 40  0.0031, 41
        0.0028, 42  0.0025, 43  0.0022, 44  0.00198, 45  0.00176, 46
        0.00157, 47  0.0014, 48 0.00124, 49  0.001108, 50  0.00099

    '''
    Convert(_temp)
    _temp = '''
    # US Number drill sizes
    # From /pylib/pgm/drill.py
    # Drill number, diameter in inches

        80 0.0135, 79 0.0145, 78 0.016, 77 0.018, 76 0.020, 75 0.021, 74
        0.0225, 73 0.024, 72 0.025, 71 0.026, 70 0.028, 69 0.0293, 68 0.031,
        67 0.032, 66 0.033, 65 0.035, 64 0.036, 63 0.037, 62 0.038, 61
        0.039, 60 0.040, 59 0.041, 58 0.042, 57 0.043, 56 0.0465, 55 0.052,
        54 0.055, 53 0.0595, 52 0.0635, 51 0.067, 50 0.070, 49 0.073, 48
        0.076, 47 0.0785, 46 0.081, 45 0.082, 44 0.086, 43 0.089, 42 0.0935,
        41 0.096, 40 0.098, 39 0.0995, 38 0.1015, 37 0.104, 36 0.1065, 35
        0.110, 34 0.111, 33 0.113, 32 0.116, 31 0.120, 30 0.1285, 29 0.136,
        28 0.1405, 27 0.144, 26 0.147, 25 0.1495, 24 0.152, 23 0.154, 22
        0.157, 21 0.159, 20 0.161, 19 0.166, 18 0.1695, 17 0.173, 16 0.177,
        15 0.180, 14 0.182, 13 0.185, 12 0.189, 11 0.191, 10 0.1935, 9
        0.196, 8 0.199, 7 0.201, 6 0.204, 5 0.2055, 4 0.209, 3 0.213, 2
        0.221, 1 0.228

    '''
    Convert(_temp)
    _temp = '''
    # US Letter drill sizes
    # From /pylib/pgm/drill.py
    # Drill number, diameter in inches

        A 0.234, B 0.238, C 0.242, D 0.246, E 0.250, F 0.257, G 0.261, H
        0.266, I 0.272, J 0.277, K 0.281, L 0.290, M 0.295, N 0.302, O
        0.316, P 0.323, Q 0.332, R 0.339, S 0.348, T 0.358, U 0.368, V
        0.377, W 0.386, X 0.397, Y 0.404, Z 0.413

    '''
    Convert(_temp)
    _temp = '''
    # Birmingham wire gauge
    # From https://sizes.com/materials/wire.htm
    # Gauge number, diameter in inches

        -4 0.5, -3 0.454, -2 0.425, -1 0.38, 0 0.34, 1 0.3, 2 0.284, 3
        0.259, 4 0.238, 5 0.22, 6 0.203, 7 0.18, 8 0.165, 9 0.148, 10 0.134,
        11 0.12, 12 0.109, 13 0.095, 14 0.083, 15 0.072, 16 0.065, 17 0.058,
        18 0.049, 19 0.042, 20 0.035, 21 0.032, 22 0.028, 23 0.025, 24
        0.022, 25 0.02, 26 0.018, 27 0.016, 28 0.014, 29 0.013, 30 0.012, 31
        0.01, 32 0.009, 33 0.008, 34 0.007, 35 0.005, 36 0.004,

    '''
    Convert(_temp)
    _temp = '''
    # Stubs' steel wire gauge
    # From https://sizes.com/materials/wire.htm
    # Gauge number, diameter in inches

        1 0.227, 2 0.219, 3 0.212, 4 0.207, 5 0.204, 6 0.201, 7 0.199, 8
        0.197, 9 0.194, 10 0.191, 11 0.188, 12 0.185, 13 0.182, 14 0.18, 15
        0.178, 16 0.175, 17 0.172, 18 0.168, 19 0.164, 20 0.161, 21 0.157,
        22 0.155, 23 0.153, 24 0.151, 25 0.148, 26 0.146, 27 0.143, 28
        0.139, 29 0.134, 30 0.127, 31 0.12, 32 0.115, 33 0.112, 34 0.11, 35
        0.108, 36 0.106, 37 0.103, 38 0.101, 39 0.099, 40 0.097, 41 0.095,
        42 0.092, 43 0.088, 44 0.085, 45 0.081, 46 0.079, 47 0.077, 48
        0.075, 49 0.072, 50 0.069, 51 0.066, 52 0.063, 53 0.058, 54 0.055,
        55 0.05, 56 0.045, 57 0.042, 58 0.041, 59 0.04, 60 0.039, 61 0.038,
        62 0.037, 63 0.036, 64 0.035, 65 0.033, 66 0.032, 67 0.031, 68 0.03,
        69 0.029, 70 0.027, 71 0.026, 72 0.024, 73 0.023, 74 0.022, 75 0.02,
        76 0.018, 77 0.016, 78 0.015, 79 0.014, 80 0.013

    '''
    Convert(_temp)
    _temp = '''
    # Washburn & Moen wire gauge
    # From https://sizes.com/materials/wire.htm
    # Gauge number, diameter in inches

        -6  0.4900, -5  0.4615, -4  0.4305, -3 0.3938, -2 0.3625, -1 0.331,
        0 0.3065, 1 0.283, 2 0.2625, 3 0.2437, 4 0.2253, 5 0.207, 6 0.192, 7
        0.177, 8 0.162, 9 0.1483, 10 0.135, 11 0.1205, 12 0.1055, 13 0.0915,
        14 0.08, 15 0.072, 16 0.0625, 17 0.054, 18 0.0475, 19 0.041, 20
        0.0348, 21 0.03175, 22 0.0286, 23 0.0258, 24 0.023, 25 0.0204, 26
        0.0181, 27 0.0173, 28 0.0162, 29 0.015, 30 0.014, 31 0.0132, 32
        0.0128, 33 0.0118, 34 0.0104, 35 0.0095, 36 0.009

    '''
    Convert(_temp)
    _temp = '''
    # Imperial wire gauge
    # From https://sizes.com/materials/wire.htm
    # Gauge number, diameter in inches

        -6 0.5, -5 0.464, -4 0.432, -3 0.4, -2 0.372, -1 0.348, 0 0.324, 1
        0.3, 2 0.276, 3 0.252, 4 0.232, 5 0.212, 6 0.192, 7 0.176, 8 0.16, 9
        0.144, 10 0.128, 11 0.116, 12 0.104, 13 0.092, 14 0.08, 15 0.072, 16
        0.064, 17 0.056, 18 0.048, 19 0.04, 20 0.036, 21 0.032, 22 0.028, 23
        0.024, 24 0.022, 25 0.02, 26 0.018, 27 0.0164, 28 0.0149, 29 0.0136,
        30 0.0124, 31 0.0116, 32 0.0108, 33 0.01, 34 0.0092, 35 0.0084, 36
        0.0076, 37 0.0068, 38 0.006, 39 0.0052, 40 0.0048, 41 0.0044, 42
        0.004, 43 0.0036, 44 0.0032, 45 0.0028, 46 0.0024, 47 0.002, 48
        0.0016, 49 0.0012, 50 0.001

    '''
    Convert(_temp)
    _temp = '''
    # Whitworth's wire gauge
    # From https://sizes.com/materials/wire.htm
    # Gauge number, diameter in inches

        1 0.001, 2 0.002, 3 0.003, 4 0.004, 5 0.005, 6 0.006, 7 0.007, 8
        0.008, 9 0.009, 10 0.01, 11 0.011, 12 0.012, 13 0.013, 14 0.014, 15
        0.015, 16 0.016, 17 0.017, 18 0.018, 19 0.019, 20 0.02, 21 0.021, 22
        0.022, 23 0.023, 24 0.024, 25 0.025, 26 0.026, 27 0.027, 28 0.028,
        29 0.029, 30 0.03, 31 0.031, 32 0.032, 33 0.033, 34 0.034, 35 0.035,
        36 0.036, 37 0.037, 38 0.038, 39 0.039, 40 0.04, 41 0.041, 42 0.042,
        43 0.043, 44 0.044, 45 0.045, 46 0.046, 47 0.047, 48 0.048, 49
        0.049, 50 0.05, 51 0.051, 52  0.052, 53  0.053, 54  0.054, 55 0.055,
        56 0.056, 57 0.057, 58 0.058, 59 0.059, 60 0.06, 61 0.061, 62 0.062,
        63 0.063, 64 0.064, 65 0.065, 66 0.066, 67 0.067, 68 0.068, 69
        0.069, 70 0.07, 71 0.071, 72 0.072, 73 0.073, 74 0.074, 75 0.075, 76
        0.076, 77 0.077, 78 0.078, 79 0.079, 80 0.08

    '''
    Convert(_temp)
    _temp = '''
    # Waterbury steel wire gauge (1917)
    # From https://sizes.com/materials/wire.htm
    # Gauge number, diameter in inches

        -8 0.005, -7 0.0055, -6 0.006, -5 0.0065, -4 0.007, -3 0.0075, -2
        0.008, -1 0.0085, 0 0.009, 1 0.01, 2 0.011, 3 0.012, 4 0.013, 5
        0.014, 6 0.016, 7 0.018, 8 0.02, 9 0.022, 10 0.024, 11 0.026, 12
        0.028, 13 0.03, 14 0.032, 15 0.034, 16 0.036, 17 0.038, 18 0.04, 19
        0.042, 20 0.044, 21 0.046, 22 0.048, 23 0.051, 24 0.055, 25 0.059,
        26 0.063, 27 0.067, 28 0.071, 29 0.074, 30 0.078, 31 0.082, 32
        0.086, 33 0.09, 34 0.094, 35 0.098, 36 0.102, 37 0.106, 38 0.112, 39
        0.118, 40 0.125, 41 0.132, 42 0.139, 43 0.146, 44 0.153, 45 0.16

    '''
    Convert(_temp)
    _temp = '''
    # American Steel & Wire Co. music wire gauge
    # From https://sizes.com/materials/wire.htm
    # Gauge number, diameter in inches

        -5 0.004, -4 0.005, -3 0.006, -2 0.007, -1 0.008, 0 0.009, 1 0.01, 2
        0.011, 3 0.012, 4 0.013, 5 0.014, 6 0.016, 7 0.018, 8 0.02, 9 0.022,
        10 0.024, 11 0.026, 12 0.029, 13 0.031, 14 0.033, 15 0.035, 16
        0.037, 17 0.039, 18 0.041, 19 0.043, 20 0.045, 21 0.047, 22 0.049,
        23 0.051, 24 0.055, 25 0.059, 26 0.063, 27 0.067, 28 0.071, 29
        0.075, 30 0.08, 31 0.085, 32 0.09, 33 0.095, 34 0.1, 35 0.106, 36
        0.112, 37 0.118, 38 0.124, 39 0.13, 40 0.138, 41 0.146, 42 0.154, 43
        0.162, 44 0.17, 45 0.18

    '''
    Convert(_temp)
    _temp = '''
    # American Screw & Wire Co. music wire gauge
    # From https://sizes.com/materials/wire.htm
    # Gauge number, diameter in inches

        -5 0.0095, -4 0.01, -3 0.011, -2 0.012, -1 0.0133, 0 0.0144, 1
        0.0156, 2 0.0166, 3 0.0178, 4 0.0188, 5 0.0202, 6 0.0215, 7 0.023, 8
        0.0243, 9 0.0256, 10 0.027, 11 0.0284, 12 0.0296, 13 0.0314, 14
        0.0326, 15 0.0345, 16 0.036, 17 0.0377, 18 0.0395, 19 0.0414, 20
        0.0434, 21 0.046, 22 0.0483, 23 0.051, 24 0.055, 25 0.0586, 26
        0.0626, 27 0.0675, 28 0.072, 29 0.076, 30 0.08, 31 0.085 

    '''
    Convert(_temp)
    _temp = '''
    # Wright Wire Co. music wire gauge
    # From https://sizes.com/materials/wire.htm
    # Gauge number, diameter in inches

        -1 0.0085, 0 0.009, 1 0.01, 2 0.011, 3 0.012, 4 0.013, 5 0.014, 6
        0.016, 7 0.018, 8 0.02, 9 0.022, 10 0.024, 11 0.026, 12 0.028, 13
        0.0305, 14 0.0325, 15 0.034, 16 0.036, 17 0.038, 18 0.0405, 19
        0.042, 20 0.044, 21 0.046, 22 0.0485, 23 0.0505, 24 0.0545, 25
        0.0583, 26 0.063, 27 0.067, 28 0.071, 29 0.0745, 30 0.078, 31 0.082,
        32 0.086, 33 0.09, 34 0.096

    '''
    Convert(_temp)
    _temp = '''
    # Washburn & Moen music wire gauge
    # From https://sizes.com/materials/wire.htm
    # Gauge number, diameter in inches

        -7 0.0083, -6 0.0087, -5 0.0095, -4 0.01, -3 0.011, -2 0.012, -1
        0.0133, 0 0.0144, 1 0.0156, 2 0.0166, 3 0.0178, 4 0.0188, 5 0.0202,
        6 0.0215, 7 0.023, 8 0.0243, 9 0.0256, 10 0.027, 11 0.0284, 12
        0.0296, 13 0.0314, 14 0.0326, 15 0.0345, 16 0.036, 17 0.0377, 18
        0.0395, 19 0.0414, 20 0.0434, 21 0.046, 22 0.0483, 23 0.051, 24
        0.055, 25 0.0586, 26 0.0626, 27 0.0658, 28 0.072, 29 0.076, 30 0.08

    '''
    Convert(_temp)
    _temp = '''
    # Roebling music wire gauge
    # From https://sizes.com/materials/wire.htm
    # Gauge number, diameter in inches

        -3 0.007, -2 0.0075, -1 0.0085, 0 0.009, 1 0.01, 2 0.011, 3 0.012, 4
        0.013, 5 0.014, 6 0.016, 7 0.018, 8 0.02, 9 0.022, 10 0.024, 11
        0.026, 12 0.028, 13 0.03, 14 0.032, 15 0.034, 16 0.036, 17 0.038, 18
        0.04, 19 0.042, 20 0.044, 21 0.046, 22 0.048, 23 0.051, 24 0.055, 25
        0.059, 26 0.063, 27 0.067, 28 0.071, 29 0.074, 30 0.078, 31 0.082,
        32 0.086, 33 0.09, 34 0.095, 35 0.1, 36 0.105, 37 0.11, 38 0.115, 39
        0.12, 40 0.125, 41 0.13

    '''
    Convert(_temp)
    _temp = '''
    # Felten & Guilleaume music wire gauge
    # From https://sizes.com/materials/wire.htm
    # Gauge number, diameter in inches

        -3 0.0068, -2 0.0075, -1 0.0087, 0 0.0093, 1 0.0098, 2 0.0106, 3
        0.0114, 4 0.0122, 5 0.0138, 6 0.0157, 7 0.0177, 8 0.0197, 9 0.0216,
        10 0.0236, 11 0.026, 12 0.0283, 13 0.0303, 14 0.0323, 15 0.0342, 16
        0.0362, 17 0.0382, 18 0.04, 19 0.042, 20 0.044, 21 0.046, 22 0.048,
        23 0.051, 24 0.055, 25 0.059, 26 0.063, 27 0.067, 28 0.071, 29
        0.074, 30 0.078, 31 0.082, 32 0.086

    '''
    Convert(_temp)
    _temp = '''
    # English music wire gauge
    # From https://sizes.com/materials/wire.htm
    # Gauge number, diameter in inches

        2 0.0105, 3 0.0115, 4 0.0125, 5 0.0145, 6 0.015, 7 0.0175, 8 0.019,
        9 0.022, 10 0.0245, 11 0.027, 12 0.028, 13 0.0305, 14 0.032, 15
        0.035, 16 0.036, 17 0.038, 18 0.04, 19 0.042, 20 0.043, 21 0.0445,
        22 0.047, 23 0.049, 24 0.053, 25 0.056, 26 0.0605, 27 0.064, 28
        0.0685, 29 0.0715, 30 0.075

    '''
    Convert(_temp)
    _temp = '''
    # Poehlmann music wire gauge
    # From https://sizes.com/materials/wire.htm
    # Gauge number, diameter in inches

        -3 0.006, -2 0.007, -1 0.008, 0 0.009, 1 0.01, 2 0.011, 3 0.012, 4
        0.013, 5 0.014, 6 0.016, 7 0.018, 8 0.02, 9 0.022, 10 0.024, 11
        0.026, 12 0.029, 13 0.031, 14 0.033, 15 0.035, 16 0.037, 17 0.039,
        18 0.041, 19 0.043, 20 0.045, 21 0.047, 22 0.049, 23 0.051, 24
        0.055, 25 0.059, 26 0.063, 27 0.067, 28 0.071, 29 0.075, 30 0.08

    '''
    Convert(_temp)
    _temp = '''
    # Alhoff & Muller music wire gauge
    # From https://sizes.com/materials/wire.htm
    # Gauge number, diameter in inches

        -1 0.008, 0 0.009, 1 0.01, 2 0.011, 3 0.012, 4 0.013, 5 0.014, 6
        0.016, 7 0.018, 8 0.02, 9 0.022, 10 0.024, 11 0.026, 12 0.028, 13
        0.03, 14 0.032, 15 0.034, 16 0.036, 17 0.038, 18 0.04, 19 0.042, 20
        0.044, 21 0.046, 22 0.048, 23 0.051, 24 0.055, 25 0.059, 26 0.063,
        27 0.067, 28 0.071, 29 0.074, 30 0.078, 31 0.082, 32 0.086, 33 0.09,
        34 0.094, 35 0.098, 36 0.102

    '''
    Convert(_temp)
    _temp = '''
    # W. N. Brunton music wire gauge
    # From https://sizes.com/materials/wire.htm
    # Gauge number, diameter in inches

        -1 0.0085, 0 0.009, 1 0.011, 2 0.01, 3 0.012, 4 0.013, 5 0.014, 6
        0.016, 7 0.017, 8 0.019, 9 0.022, 10 0.024, 11 0.027, 12 0.029, 13
        0.031, 14 0.032, 15 0.034, 16 0.036, 17 0.038, 18 0.04, 19 0.042, 20
        0.044, 21 0.046, 22 0.048, 23 0.05, 24 0.054, 25 0.058, 26 0.062, 27
        0.066, 28 0.069, 29 0.072, 30 0.076, 31 0.08, 32 0.086, 33 0.092, 34
        0.098, 35 0.104, 36 0.11, 37 0.117, 38 0.121, 39 0.13, 40 0.14

    '''
    Convert(_temp)
    synonyms = {
        "Brown & Sharpe Gauge": "AWG",
        "American Wire Gauge": "AWG",
        "Brown & Sharpe Gauge": "AWG",
        "Stubs' Iron Wire Gauge": "Birmingham wire gauge",
        "Cocker's Wire Gauge": "Whitworth's wire gauge",
        "Roebling": "Washburn & Moen wire gauge",
        "American Steel and Wire Co.": "Washburn & Moen wire gauge",
        "Trenton Iron Works music wire gauge": "Washburn & Moen music wire gauge",
    }
    for i in synonyms:
        if not i:
            continue
        if synonyms[i] not in gauges:
            print(synonyms[i], "missing in gauges")
if __name__ == "__main__": 
    import sys
    import os
    from wrap import dedent
    from columnize import Columnize
    name = sys.argv[0]
    w = int(os.environ.get("COLUMNS", 80)) - 5
    sep = "-"*w
    print(f"{name}:  List of different gauges (sizes in inches)")
    print(dedent(f'''
     Number   
    of sizes    Gauge name
    --------    {'-'*40}'''))
    for i in gauges:
        print(f"{len(gauges[i]):4d}        {i}")
    print(dedent('''
    Notes:
    - The Precision Brand music wire I have in the shop uses the US Standard
        wire gauge (e.g., 20 gauge is 0.045" diameter).'''))
    # Print out data
    print(sep)
    print("-1 means 00 or 1/0, -2 means 000 or 2/0, etc.")
    print("Trailing 0 digits are removed from the dimensions in inches")
    if have_flt:
        x = flt(0)
        x.n = 4         # Print numbers to 4 significant figures
        x.rtz = True    # Remove trailing 0 digits
    for gauge in gauges:
        data = gauges[gauge]
        print(sep)
        print(gauge)
        print(urls[gauge])
        o = []
        for key, value in data.items():
            o.append(f"{str(key):4s} {value.val}")
        for line in Columnize(o, col_width=16):
            print(line)
