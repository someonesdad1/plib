'''
    wl2rgb(wl_nm)
        Converts a light wavelength in nm into an approximate RGB color
    rgb2wl(rgb)
        Approximate inverse function to wl2rgb()
    wl2cie_xy(wl_nm)
        Convert from wavelenth in nm to CIE x, y coordinates
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Wavelength of light to color oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2022 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ sci oo>
        <oo test ∞ --test oo>
        <oo todo ∞ oo>
    '''
    if 1:  # Standard imports
        pass
    if 1:  # Custom imports
        from color import Color, t
        from lwtest import Assert
    if 1:  # Global variables
        pass
if 1:  # Utility
    def GetCIETable():
        '''Returns a tuple of (nm, (xbar, ybar, zbar)) values to give the CIE's
        standard method to convert from a power spectral density (PSD) function
        to X, Y, Z tristimulus coordinates.  A PSD is integrated with these
        numerical functions over the wavelengths of 380 to 780 nm.  These are
        for the 2° field of view.  These numbers were derived around 1930 from
        two experimental samples from 17 people.  The experiments were careful
        and have been repeated, so though the samples were biased, it seems
        they represent a large portion of humanity.
        
        From 204.xls downloaded from
        https://web.archive.org/web/20170131100357/http://files.cie.co.at/204.xls
        Thu 24 Mar 2022.
        '''
        # CIE 1931 standard colorimetric observer
        # Columns:
        #     wavelength, nm
        #     xbar(wl_nm)
        #     ybar(wl_nm)
        #     zbar(wl_nm)
        data = [
            [380, [0.001368, 0.000039, 0.006450]],
            [385, [0.002236, 0.000064, 0.010550]],
            [390, [0.004243, 0.000120, 0.020050]],
            [395, [0.007650, 0.000217, 0.036210]],
            [400, [0.014310, 0.000396, 0.067850]],
            [405, [0.023190, 0.000640, 0.110200]],
            [410, [0.043510, 0.001210, 0.207400]],
            [415, [0.077630, 0.002180, 0.371300]],
            [420, [0.134380, 0.004000, 0.645600]],
            [425, [0.214770, 0.007300, 1.039050]],
            [430, [0.283900, 0.011600, 1.385600]],
            [435, [0.328500, 0.016840, 1.622960]],
            [440, [0.348280, 0.023000, 1.747060]],
            [445, [0.348060, 0.029800, 1.782600]],
            [450, [0.336200, 0.038000, 1.772110]],
            [455, [0.318700, 0.048000, 1.744100]],
            [460, [0.290800, 0.060000, 1.669200]],
            [465, [0.251100, 0.073900, 1.528100]],
            [470, [0.195360, 0.090980, 1.287640]],
            [475, [0.142100, 0.112600, 1.041900]],
            [480, [0.095640, 0.139020, 0.812950]],
            [485, [0.057950, 0.169300, 0.616200]],
            [490, [0.032010, 0.208020, 0.465180]],
            [495, [0.014700, 0.258600, 0.353300]],
            [500, [0.004900, 0.323000, 0.272000]],
            [505, [0.002400, 0.407300, 0.212300]],
            [510, [0.009300, 0.503000, 0.158200]],
            [515, [0.029100, 0.608200, 0.111700]],
            [520, [0.063270, 0.710000, 0.078250]],
            [525, [0.109600, 0.793200, 0.057250]],
            [530, [0.165500, 0.862000, 0.042160]],
            [535, [0.225750, 0.914850, 0.029840]],
            [540, [0.290400, 0.954000, 0.020300]],
            [545, [0.359700, 0.980300, 0.013400]],
            [550, [0.433450, 0.994950, 0.008750]],
            [555, [0.512050, 1.000000, 0.005750]],
            [560, [0.594500, 0.995000, 0.003900]],
            [565, [0.678400, 0.978600, 0.002750]],
            [570, [0.762100, 0.952000, 0.002100]],
            [575, [0.842500, 0.915400, 0.001800]],
            [580, [0.916300, 0.870000, 0.001650]],
            [585, [0.978600, 0.816300, 0.001400]],
            [590, [1.026300, 0.757000, 0.001100]],
            [595, [1.056700, 0.694900, 0.001000]],
            [600, [1.062200, 0.631000, 0.000800]],
            [605, [1.045600, 0.566800, 0.000600]],
            [610, [1.002600, 0.503000, 0.000340]],
            [615, [0.938400, 0.441200, 0.000240]],
            [620, [0.854450, 0.381000, 0.000190]],
            [625, [0.751400, 0.321000, 0.000100]],
            [630, [0.642400, 0.265000, 0.000050]],
            [635, [0.541900, 0.217000, 0.000030]],
            [640, [0.447900, 0.175000, 0.000020]],
            [645, [0.360800, 0.138200, 0.000010]],
            [650, [0.283500, 0.107000, 0.000000]],
            [655, [0.218700, 0.081600, 0.000000]],
            [660, [0.164900, 0.061000, 0.000000]],
            [665, [0.121200, 0.044580, 0.000000]],
            [670, [0.087400, 0.032000, 0.000000]],
            [675, [0.063600, 0.023200, 0.000000]],
            [680, [0.046770, 0.017000, 0.000000]],
            [685, [0.032900, 0.011920, 0.000000]],
            [690, [0.022700, 0.008210, 0.000000]],
            [695, [0.015840, 0.005723, 0.000000]],
            [700, [0.011359, 0.004102, 0.000000]],
            [705, [0.008111, 0.002929, 0.000000]],
            [710, [0.005790, 0.002091, 0.000000]],
            [715, [0.004109, 0.001484, 0.000000]],
            [720, [0.002899, 0.001047, 0.000000]],
            [725, [0.002049, 0.000740, 0.000000]],
            [730, [0.001440, 0.000520, 0.000000]],
            [735, [0.001000, 0.000361, 0.000000]],
            [740, [0.000690, 0.000249, 0.000000]],
            [745, [0.000476, 0.000172, 0.000000]],
            [750, [0.000332, 0.000120, 0.000000]],
            [755, [0.000235, 0.000085, 0.000000]],
            [760, [0.000166, 0.000060, 0.000000]],
            [765, [0.000117, 0.000042, 0.000000]],
            [770, [0.000083, 0.000030, 0.000000]],
            [775, [0.000059, 0.000021, 0.000000]],
            [780, [0.000042, 0.000015, 0.000000]],
            # Sums:  (21.371524, 21.371327, 21.371540)
        ]
        if not GetCIETable.checked:
            # Tasks:
            #   - Check the sums of each column
            #   - Round each float to 6 decimal places
            #   - Cache in GetCIETable.data
            checked = []
            sumx = sumy = sumz = 0
            def f(x):
                return round(x, 6)
            for wl, d in data:
                sumx += d[0]
                sumy += d[1]
                sumz += d[2]
                checked.append((wl, tuple([f(i) for i in d])))
            if f(sumx) != f(21.371524):
                raise ValueError("Bad x checksum")
            if f(sumy) != f(21.371327):
                raise ValueError("Bad y checksum")
            if f(sumz) != f(21.371540):
                raise ValueError("Bad z checksum")
            GetCIETable.data = checked
        return GetCIETable.data
    GetCIETable.checked = False
    GetCIETable()
    def GetCIEDict():
        '''Returns a dict keyed by integer wavelength in nm to return the CIE
        1931 Color Matching Functions to convert a spectral power density to
        tristimulus XYZ values by integration.  The keys are integers on the
        interval [380, 780] in steps of 1.
        '''
        if GetCIEDict.dict is None:
            # Linearly interpolate the GetCIETable()'s data to get 1 nm steps
            di = {}
            for wl, cmf in GetCIETable():
                di[wl] = cmf
            def f(x, n): return round(x, n)
            for wl in range(380, 779, 5):
                start, end = di[wl], di[wl + 5]
                slope = [f((j - i)/5, 10) for i, j in zip(start, end)]
                for i in (1, 2, 3, 4):
                    a = [f(j + k*i, 6) for j, k in zip(start, slope)]
                    di[wl + i] = a
            GetCIEDict.dict = di
        return GetCIEDict.dict
    GetCIEDict.dict = None
if 1:  # Light wavelength to & from RGB colors
    '''

        The goal of this stuff is to turn the wavelength of light into a suitable color
        for your computer monitor.  This is a complicated problem involving the human
        perception of color and the vagaries of software and hardware.

        https://stackoverflow.com/questions/3407942/rgb-values-of-visible-spectrum has a
        number of responses:

        The response by Ian Boyd seems to be the most detailed and explains a number of
        the assumptions that have to be made.  (Accessed 14 Feb 2026) He references a
        "CIE 1964 Supplementary Standard Colorimetric Observer" link that is broken, but
        the archive link next to it takes you to a document named tc148.pdf.  On page 48
        of this PDF is Table T.5, from 380 to 780 nm in 5 nm steps, giving the CIE 1964
        standard colorimetric observer function (I saved it in
        /ebooks/phys/misc/tc148_1964_standard_colorimetric_observer.pdf).  This table
        can be screen-scraped (commas converted to periods) and the data were put into
        the variable cie_1964_colorimetric below):

        wl   xbar      ybar      zbar   x       y
        455 0.342957 0.106256 1.900700 0.14594 0.04522
        
        The section after the table gives the sums Σxbar = 23.329353, Σybar = 23.332036,
        Σzbar = 23.334152676, which let you check your data entry.

        His example is for 455 nm.  He calls the xbar, etc. variables X, Y, Z and he
        uses X = 0.342957, Y = 0.106256, Z = 1.90070 which agree with the above table
        entry.  Note that x = X/(X + Y + Z) = 0.14594; the y value is calculated
        similarly.

        Then a whitepoint has to be picked.  He picked D65, the one that sRGB uses.
        sRGB is the standard RGB system defined in the 1990's

        

        --------------------------------------------------------------------------- 
        https://www.baeldung.com/cs/rgb-color-light-frequency
            - References the wl2rgb algorithm to Earl F. Glynn.  I got it from Dan Bruton's
                FORTRAN code from https://www.physics.sfasu.edu/astro/color/spectra.html,
                last modified 20 Feb 1996.
            - Gives a CIE color-matching using the 1931 CIE color model that models how
              the human eye perceives color.


    '''
    # In the following, wl is in nm and X, Y, Z are the usual CIE coordinates
    cie_1964_colorimetric = '''
        wl      X        Y        Z   
        380 0.000160 0.000017 0.000705
        385 0.000662 0.000072 0.002928
        390 0.002362 0.000253 0.010482
        395 0.007242 0.000769 0.032344
        400 0.019110 0.002004 0.086011
        405 0.043400 0.004509 0.197120
        410 0.084736 0.008756 0.389366
        415 0.140638 0.014456 0.656760
        420 0.204492 0.021391 0.972542
        425 0.264737 0.029497 1.282500
        430 0.314679 0.038676 1.553480
        435 0.357719 0.049602 1.798500
        440 0.383734 0.062077 1.967280
        445 0.386726 0.074704 2.027300
        450 0.370702 0.089456 1.994800
        455 0.342957 0.106256 1.900700
        460 0.302273 0.128201 1.745370
        465 0.254085 0.152761 1.554900
        470 0.195618 0.185190 1.317560
        475 0.132349 0.219940 1.030200
        480 0.080507 0.253589 0.772125
        485 0.041072 0.297665 0.570060
        490 0.016172 0.339133 0.415254
        495 0.005132 0.395379 0.302356
        500 0.003816 0.460777 0.218502
        505 0.015444 0.531360 0.159249
        510 0.037465 0.606741 0.112044
        515 0.071358 0.685660 0.082248
        520 0.117749 0.761757 0.060709
        525 0.172953 0.823330 0.043050
        530 0.236491 0.875211 0.030451
        535 0.304213 0.923810 0.020584
        540 0.376772 0.961988 0.013676
        545 0.451584 0.982200 0.007918
        550 0.529826 0.991761 0.003988
        555 0.616053 0.999110 0.001091
        560 0.705224 0.997340 0.000000
        565 0.793832 0.982380 0.000000
        570 0.878655 0.955552 0.000000
        575 0.951162 0.915175 0.000000
        580 1.014160 0.868934 0.000000
        585 1.074300 0.825623 0.000000
        590 1.118520 0.777405 0.000000
        595 1.134300 0.720353 0.000000
        600 1.123990 0.658341 0.000000
        605 1.089100 0.593878 0.000000
        610 1.030480 0.527963 0.000000
        615 0.950740 0.461834 0.000000
        620 0.856297 0.398057 0.000000
        625 0.754930 0.339554 0.000000
        630 0.647467 0.283493 0.000000
        635 0.535110 0.228254 0.000000
        640 0.431567 0.179828 0.000000
        645 0.343690 0.140211 0.000000
        650 0.268329 0.107633 0.000000
        655 0.204300 0.081187 0.000000
        660 0.152568 0.060281 0.000000
        665 0.112210 0.044096 0.000000
        670 0.081261 0.031800 0.000000
        675 0.057930 0.022602 0.000000
        680 0.040851 0.015905 0.000000
        685 0.028623 0.011130 0.000000
        690 0.019941 0.007749 0.000000
        695 0.013842 0.005375 0.000000
        700 0.009577 0.003718 0.000000
        705 0.006605 0.002565 0.000000
        710 0.004553 0.001768 0.000000
        715 0.003145 0.001222 0.000000
        720 0.002175 0.000846 0.000000
        725 0.001506 0.000586 0.000000
        730 0.001045 0.000407 0.000000
        735 0.000727 0.000284 0.000000
        740 0.000508 0.000199 0.000000
        745 0.000356 0.000140 0.000000
        750 0.000251 0.000098 0.000000
        755 0.000178 0.000070 0.000000
        760 0.000126 0.000050 0.000000
        765 0.000090 0.000036 0.000000
        770 0.000065 0.000025 0.000000
        775 0.000046 0.000018 0.000000
        780 0.000033 0.000013 0.000000
    '''
    def CIE1964Colorimetric(wl_nm):
        'Return (X, Y, Z) for wavelength in nm'
        if not (380 <= wl_nm <= 780):
            raise ValueError(f"Wavelength {wl_nm!r} is outside [380, 780] nm")

    def wl2rgb(wl_nm, gamma=0.8):
        '''Convert wl_nm (light wavelength in nm on [380, 780]) into a Color object
        using a linear approximation.  The Color object represents an RGB color.  gamma
        is used for a gamma adjustment.  This algorithm is apparently due to Earl F.
        Glynn.
        '''
        # Translation of Dan Bruton's FORTRAN code from 
        # https://www.physics.sfasu.edu/astro/color/spectra.html, which was last
        # modified 20 Feb 1996.
        if 380 <= wl_nm <= 440:
            a = (440 - wl_nm)/(440 - 380), 0, 1
        elif 440 <= wl_nm <= 490:
            a = 0, (wl_nm - 440)/(490 - 440), 1
        elif 490 <= wl_nm <= 510:
            a = 0, 1, (510 - wl_nm)/(510 - 490)
        elif 510 <= wl_nm <= 580:
            a = (wl_nm - 510)/(580 - 510), 1, 0
        elif 580 <= wl_nm <= 645:
            a = 1, (645 - wl_nm)/(645 - 580), 0
        elif 645 <= wl_nm <= 780:
            a = 1, 0, 0
        else:
            raise ValueError(f"Wavelength {wl_nm} is not in [380, 780] wl_nm")
        if gamma < 0:
            raise ValueError("gamma must be >= 0")
        # Intensity i falls off near vision limits
        i, u, v = 1, 0.3, 0.7
        if wl_nm > 700:
            i = u + v*(780 - wl_nm)/(780 - 700)
        elif wl_nm < 420:
            i = u + v*(wl_nm - 380)/(420 - 380)
        # Scale the RGB components by i and raise to the gamma power if gamma
        # is nonzero.
        if gamma:
            b = [float((i*j)**gamma) for j in a]
        else:
            b = [float(i) for i in a]
        # Make sure the numbers are on [0, 1]
        assert all([0 <= i <= 1 for i in b])
        return Color(*b)
    def rgb2wl(color):
        '''Convert the indicated color (a Color instance) to a wavelength in nm
        
        The algorithm is
            - Get the integer value of the hue on [0, 255]
            - If hue > 212 return 645 nm
            - Otherwise hue is in [0, 212] and use a dictionary lookup
        The dictionary was gotten by printing wl2rgb()'s output and filling in any missing key
        values by hand.  The "inversion" isn't perfect, but it matches mostly within ±1 nm.
        '''
        # 16 Jan 2025 14:34:34 pm Thu
        if not str(color)[:3] == "C⁸(":
            # This is a hack, as I'm getting strange behavior:  just before
            # wl2rgb.rgb2wl(c) where c is the Color instance 'C⁸(0, 0, 0)' and
            # isinstance(c, Color) returns true, the isinstance(color, Color) in this
            # function returns false.  Further, both id(instance) show the identical
            # location in memory.  To make this work, I've added the string form
            # detection.
            if not isinstance(color, Color):
                raise TypeError("color must be a Color (/plib/color.py) instance")
        if not hasattr(rgb2wl, "dict"):
            rgb2wl.dict = {
                0: 645, 1: 644, 2: 643, 3: 642, 4: 641, 5: 640, 6: 639, 7: 638, 8: 636,
                9: 635, 10: 634, 11: 633, 12: 631, 13: 630, 14: 628, 15: 627, 16: 625,
                17: 624, 18: 622, 19: 621, 20: 619, 21: 618, 22: 616, 23: 614, 24: 613,
                25: 611, 26: 609, 27: 608, 28: 606, 29: 604, 30: 602, 31: 601, 32: 599,
                33: 597, 34: 595, 35: 594, 36: 592, 37: 590, 38: 588, 39: 586, 40: 584,
                41: 582, 42: 580, 43: 579, 44: 577, 45: 575, 46: 573, 47: 571, 48: 569,
                49: 567, 50: 565, 51: 563, 52: 561, 53: 559, 54: 557, 55: 555, 56: 553,
                57: 551, 58: 549, 59: 548, 60: 546, 61: 544, 62: 542, 63: 541, 64: 539,
                65: 537, 66: 535, 67: 534, 68: 532, 69: 530, 70: 529, 71: 527, 72: 526,
                73: 524, 74: 523, 75: 521, 76: 520, 77: 518, 78: 517, 79: 516, 80: 515,
                81: 513, 82: 512, 83: 511, 84: 511, 85: 510, 86: 510, 87: 509, 88: 509,
                89: 509, 90: 508, 91: 508, 92: 508, 93: 507, 94: 507, 95: 507, 96: 506,
                97: 506, 98: 505, 99: 505, 100: 504, 101: 504, 102: 503, 103: 503, 104:
                502, 105: 502, 106: 501, 107: 501, 108: 500, 109: 500, 110: 499, 111:
                499, 112: 498, 113: 498, 114: 497, 115: 497, 116: 496, 117: 496, 118:
                495, 119: 495, 120: 494, 121: 494, 122: 493, 123: 493, 124: 492, 125:
                491, 126: 491, 127: 490, 128: 489, 129: 488, 130: 486, 131: 485, 132:
                483, 133: 482, 134: 480, 135: 479, 136: 478, 137: 476, 138: 475, 139:
                473, 140: 472, 141: 471, 142: 469, 143: 468, 144: 467, 145: 465, 146:
                464, 147: 463, 148: 462, 149: 460, 150: 459, 151: 458, 152: 457, 153:
                456, 154: 454, 155: 453, 156: 452, 157: 451, 158: 450, 159: 449, 160:
                448, 161: 447, 162: 446, 163: 445, 164: 444, 165: 443, 166: 442, 167:
                442, 168: 441, 169: 441, 170: 440, 171: 439, 172: 438, 173: 437, 174:
                436, 175: 435, 176: 434, 177: 433, 178: 432, 179: 431, 180: 430, 181:
                428, 182: 427, 183: 426, 184: 425, 185: 423, 186: 422, 187: 420, 188:
                419, 189: 418, 190: 416, 191: 415, 192: 413, 193: 411, 194: 410, 195:
                409, 196: 407, 197: 406, 198: 404, 199: 402, 200: 401, 201: 399, 202:
                397, 203: 396, 204: 394, 205: 393, 206: 391, 207: 389, 208: 387, 209:
                386, 210: 384, 211: 382, 212: 380,
            }
        hue = color.ihls[0]
        Assert(isinstance(hue, int) and 0 <= hue <= 255)
        if hue > 212:
            return 645
        return rgb2wl.dict[hue]
    def wl2cie_xy(wl_nm):
        '''Returns CIE xy for a given integer wavelength in nm.  These are the
        1931 xy coordinates of the outside edges of the chromaticity diagram
        that correspond to a wavelength.  Spot checks against a few 1931
        chromaticity diagrams indicate the correct values have been gotten.
        '''
        di = GetCIEDict()
        wl = int(wl_nm)
        if wl not in di:
            msg = f"'{wl_nm}' isn't an integer wavelength in [380, 780]"
            raise ValueError(msg)
        XYZ = di[wl]
        def f(x, n): round(x, n)
        t = sum(XYZ)
        n = 4
        return (f(XYZ[0]/t, n), f(XYZ[1]/t, n))

if __name__ == "__main__":
    from rgbdata import color_data
    from util import VisualCount, TemplateRound
    from columnize import Columnize
    from lwtest import run
    from wrap import dedent
    from f import flt
    import sys
    from pprint import pprint as pp
    def Test_ColorFuncs():
        "Show that wl2rgb() and rgb2wl() are (nearly) inverses"
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
        o, p = [], []
        print("Wavelength in nm of each RGB color in rgbdata.py")
        maxlen = 0
        for attribution_number, name, Color_instance, hue_category in color_data:
            wl = rgb2wl(Color_instance)
            rgb = wl2rgb(wl)
            o.append(TemplateRound(wl, 10))
            s = f"{t(rgb)}{wl}{t.n} {t(Color_instance)}{name.strip()}{t.n}"
            p.append(s)
            maxlen = max(maxlen, len(s))
        for i in Columnize(p, esc=True):
            print(i)
        print(f"maxlen = {maxlen}")
        print("Histogram of wavelengths in above data")
        for i in VisualCount(o, indent=4):
            print(i)
        print(f"({len(o)} colors in file)")
    def Interactive():
        print(dedent(f'''
        
        Enter numbers to approximately relate light wavelength and RGB colors (enter q
        to quit).  Enter a single number that will be interpreted as a wavelength.
        Enter three numbers that will be converted to an RGB value and the wavelength
        returned (separate them by commas or spaces).  If you enter three numbers, they
        are converted to integers and should be in the range 0 to 255.  Enter the numbers:
        
        '''))
        done = False
        while not done:
            OK = False
            is_wavelength = False
            is_string = False
            while not OK:
                s = input("Number(s) [q to quit]?  ")
                s = s.strip()
                if s == "q":
                    done = True
                    break
                elif not s:
                    continue
                f= s.replace(",", " ").split()
                if len(f) == 1:      # Wavelength
                    if f[0][0] in "#$@":
                        rgb = f[0]
                        is_string = True
                        OK = True
                    else:
                        try:
                            wl = flt(f[0])
                        except Exception:
                            print("Couldn't convert to float")
                            continue
                        if not (400 <= wl <= 700):
                            print("Wavelength must be between 400 nm and 700 nm")
                        else:
                            OK = True
                            is_wavelength = True
                elif len(f) == 3:   # Tuple
                    rgb = [int(i) for i in f]
                    if not all(0 <= i <= 255 for i in rgb):
                        print("Integers must be between 0 and 255")
                    else:
                        OK = True
                else:
                    print("Didn't have 1 or 3 numbers")
            if not done:
                if is_wavelength:
                    rgb = wl2rgb(wl)
                    t.print(f"{wl} nm is {rgb} {t(rgb)} this color")
                else:
                    if is_string:
                        c = Color(rgb)
                        wl = rgb2wl(c)
                        t.print(f"{rgb} is {t(c)}this color{t.n}, "
                                f"about {wl} nm")
                    else:
                        c = Color(*rgb)
                        wl = rgb2wl(c)
                        t.print(f"{', '.join(str(i) for i in rgb)} is {t(c)}this color{t.n}, "
                                f"about {wl} nm")
    def SteppedWavelengths(step_nm, cols=True):
        gamma = 0.8
        print(f"Wavelength in steps of {step_nm} nm to RGB colors")
        out, count = [], 0
        for nm in range(380, 781, step_nm):
            colornum = wl2rgb(nm, gamma=gamma)
            s = colornum.xrgb
            out.append(f"{t(s)}{nm}{t.n}")
            count += 1
        if cols:
            o = Columnize(out, indent=" "*2, horiz=1)
            for line in o:
                print(line)
        else:
            for line in out:
                print(line)
        print(f"{count} wavelengths printed")
    def Names():
        'Show wavelengths with name candidates'
        gamma = 0.8
        for nm in range(380, 651, 10):
            c = wl2rgb(nm, gamma=gamma)
            s = c.xrgb
            h = c.xhsv
            v = c.xhls
            r, g, b = c.irgb
            t.print(f"{t(s)}{nm} {s} {h} {v} ({r:3d}, {g:3d}, {b:3d})")
        print("nm    #rgb    @hsv    $hls")

    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])
        elif sys.argv[1] == "names":
            Names()
        else:
            Interactive()
            exit()
    else:
        t.on = True
        #Decorate()
        #print()
        #SteppedWavelengths(2)
        #print()
        SteppedWavelengths(5)
        print()
        SteppedWavelengths(10)
        print()
        SteppedWavelengths(20)
