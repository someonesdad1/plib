'''
Provides the function wl2rgb() to convert a light wavelength in nm into an
approximate RGB color.
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
        # Convert between RGB and light wavelength in nm
        #∞what∞#
        #∞test∞# ignore #∞test∞#
        pass
    if 1:   # Standard imports
        from pprint import pprint as pp
    if 1:   # Custom imports
        from color import Color, t
        from lwtest import Assert
    if 1:   # Global variables
        ii = isinstance
def wl2rgb(nm, gamma=0.8):
    '''Convert nm (light wavelength in nm on [380, 780]) into a Color
    object using a linear approximation.  The Color object represents an
    RGB color.  gamma is used for a gamma adjustment.
    '''
    # Translation of Dan Bruton's FORTRAN code from (defunct URL)
    # http://www.physics.sfasu.edu/astro/color/spectra.html into python.
    # See http://www.midnightkite.com/color.html.
    if 380 <= nm <= 440:
        a = (440 - nm)/(440 - 380), 0, 1
    elif 440 <= nm <= 490:
        a = 0, (nm - 440)/(490 - 440), 1
    elif 490 <= nm <= 510:
        a = 0, 1, (510 - nm)/(510 - 490)
    elif 510 <= nm <= 580:
        a = (nm - 510)/(580 - 510), 1, 0
    elif 580 <= nm <= 645:
        a = 1, (645 - nm)/(645 - 580), 0
    elif 645 <= nm <= 780:
        a = 1, 0, 0
    else:
        raise ValueError(f"Wavelength {nm} is not in [380, 780] nm")
    if gamma < 0:
        raise ValueError(f"gamma must be >= 0")
    # Intensity i falls off near vision limits
    i, u, v = 1, 0.3, 0.7
    if nm > 700:
        i = u + v*(780 - nm)/(780 - 700)
    elif nm < 420:
        i = u + v*(nm - 380)/(420 - 380)
    # Scale the RGB components by i and raise to the gamma power if gamma
    # is nonzero.
    if gamma:
        b = [float((i*j)**gamma) for j in a]
    else:
        b = [float(i) for i in a]
    # Make sure the numbers are on [0, 1]
    assert(all([0 <= i <=1 for i in b]))
    return Color(*b)
if 1:   # Inverse to wl2rgb()
    def rgb2wl(color):
        '''Convert the indicated color (a Color instance) to a wavelength in nm
        
        The algorithm is
            - Get the integer value of the hue on [0, 255]
            - If hue > 212 return 645 nm
            - Otherwise hue is in [0, 212] and use a dictionary lookup
        The dictionary was gotten by printing wl2rgb()'s output and filling in any missing key
        values by hand.  The "inversion" isn't perfect, but it matches mostly within ±1 nm.
        '''
        if not ii(color, Color):
            raise TypeError("color must be a Color (/plib/color.py) instance")
        if not hasattr(rgb2wl, "dict"):
            rgb2wl.dict = {
                0: 645, 1: 644, 2: 643, 3: 642, 4: 641, 5: 640, 6: 639, 7: 638, 8: 636, 9: 635,
                10: 634, 11: 633, 12: 631, 13: 630, 14: 628, 15: 627, 16: 625, 17: 624, 18: 622,
                19: 621, 20: 619, 21: 618, 22: 616, 23: 614, 24: 613, 25: 611, 26: 609, 27: 608,
                28: 606, 29: 604, 30: 602, 31: 601, 32: 599, 33: 597, 34: 595, 35: 594, 36: 592,
                37: 590, 38: 588, 39: 586, 40: 584, 41: 582, 42: 580, 43: 579, 44: 577, 45: 575,
                46: 573, 47: 571, 48: 569, 49: 567, 50: 565, 51: 563, 52: 561, 53: 559, 54: 557,
                55: 555, 56: 553, 57: 551, 58: 549, 59: 548, 60: 546, 61: 544, 62: 542, 63: 541,
                64: 539, 65: 537, 66: 535, 67: 534, 68: 532, 69: 530, 70: 529, 71: 527, 72: 526,
                73: 524, 74: 523, 75: 521, 76: 520, 77: 518, 78: 517, 79: 516, 80: 515, 81: 513,
                82: 512, 83: 511, 84: 511, 85: 510, 86: 510, 87: 509, 88: 509, 89: 509, 90: 508,
                91: 508, 92: 508, 93: 507, 94: 507, 95: 507, 96: 506, 97: 506, 98: 505, 99: 505,
                100: 504, 101: 504, 102: 503, 103: 503, 104: 502, 105: 502, 106: 501, 107: 501,
                108: 500, 109: 500, 110: 499, 111: 499, 112: 498, 113: 498, 114: 497, 115: 497,
                116: 496, 117: 496, 118: 495, 119: 495, 120: 494, 121: 494, 122: 493, 123: 493,
                124: 492, 125: 491, 126: 491, 127: 490, 128: 489, 129: 488, 130: 486, 131: 485,
                132: 483, 133: 482, 134: 480, 135: 479, 136: 478, 137: 476, 138: 475, 139: 473,
                140: 472, 141: 471, 142: 469, 143: 468, 144: 467, 145: 465, 146: 464, 147: 463,
                148: 462, 149: 460, 150: 459, 151: 458, 152: 457, 153: 456, 154: 454, 155: 453,
                156: 452, 157: 451, 158: 450, 159: 449, 160: 448, 161: 447, 162: 446, 163: 445,
                164: 444, 165: 443, 166: 442, 167: 442, 168: 441, 169: 441, 170: 440, 171: 439,
                172: 438, 173: 437, 174: 436, 175: 435, 176: 434, 177: 433, 178: 432, 179: 431,
                180: 430, 181: 428, 182: 427, 183: 426, 184: 425, 185: 423, 186: 422, 187: 420,
                188: 419, 189: 418, 190: 416, 191: 415, 192: 413, 193: 411, 194: 410, 195: 409,
                196: 407, 197: 406, 198: 404, 199: 402, 200: 401, 201: 399, 202: 397, 203: 396,
                204: 394, 205: 393, 206: 391, 207: 389, 208: 387, 209: 386, 210: 384, 211: 382,
                212: 380
            }
        hue = color.ihls[0]
        Assert(ii(hue, int) and 0 <= hue <= 255)
        if hue > 212:
            return 645
        return rgb2wl.dict[hue]

if __name__ == "__main__": 
    from lwtest import run
    from rgbdata import color_data
    from util import VisualCount
    def Test():
        'Show that wl2rgb() and rgb2wl() are (nearly) inverses'
        diffs = set()
        for wl_nm in range(380, 645):
            rgb = wl2rgb(wl_nm)
            wl = rgb2wl(rgb)
            diffs.add(wl_nm - wl)
        Assert(min(diffs) == -2 and max(diffs) == 1)
    def Decorate():
        '''Print each color in rgbdata.py with its name in its color, followed by the wavelength
        gotten from using rgb2wl() in its color.  Perusing this output gives a feel for the
        practicality of the wavelength inverse function.
         
        At the end, a histogram of the wavelengths used is printed, showing an overwhelming use of
        reds.
        '''
        o = []
        for _, name, c in color_data:
            wl = rgb2wl(c)
            rgb = wl2rgb(wl)
            o.append(wl)
            print(f"{t(rgb)}{wl}{t.n} {t(c)}{name:40s}{t.n}")
        for i in VisualCount(o, indent=4):
            print(i)
    #t.on = True
    Test()
    Decorate()
    if 0:
        rgb2wl(Color(0,0,0))
        diffs = set()
        for nm in range(380, 645, 1):
            rgb = wl2rgb(nm)
            nm1 = rgb2wl(rgb)
            diff = nm1 - nm
            diffs.add(diff)
            print(f"{t(rgb)}{nm:3d}{t.n} {rgb.ihsv[0]} {nm1} {diff}")
        print(diffs)
