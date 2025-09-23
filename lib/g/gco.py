'''
Constants for the g.py module
    Copyright (c) 2011 Don Peterson
    Contact:  gmail.com@someonesdad1

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
        - Redistributions of source code must retain the above copyright
          notice, this list of conditions and the following disclaimer.
        - Redistributions in binary form must reproduce the above copyright
          notice, this list of conditions and the following disclaimer in
          the documentation and/or other materials provided with the
          distribution.
        - Don Peterson's name may not be used to endorse or promote
          products derived from this software without specific prior
          written permission.
    This software is provided by Don Peterson "as is" and any express or
    implied warranties, including, but not limited to, the implied warranties
    of merchantability and fitness for a particular purpose are disclaimed.  In
    no event shall Don Peterson be liable for any direct, indirect, incidental,
    special, exemplary, or consequential damages (including, but not limited
    to, procurement of substitute goods or services; loss of use, data, or
    profits; or business interruption) however caused and on any theory of
    liability, whether in contract, strict liability, or tort (including
    negligence or otherwise) arising in any way out of the use of this
    software, even if advised of the possibility of such damage.
'''
from textwrap import dedent as Dedent
if 1:  # Exceptions
    class gException(Exception):
        pass
    class NotImplemented(gException):
        pass
if 1:  # Constants
    # We'll use a dictionary to keep track of the relationship between the
    # integer and variable name (this can help with debugging).
    varnames = {}
    # Temporary variables and functions to make constants like enums
    index = 100
    def Inc(name):  # Helper function
        global index, varnames
        index = index + 1
        varnames[index] = name
        return index
    inf = 1e38  # Roughly +infinity for Postscript
    no = Inc("no")
    yes = Inc("yes")
    #
    landscape = Inc("landscape")
    portrait = Inc("portrait")
    seascape = Inc("seascape")
    inversePortrait = Inc("inversePortrait")
    inverse_portrait = inversePortrait
    #
    no_fill = Inc("no_fill")
    solid_fill = Inc("solid_fill")
    line_fill = Inc("line_fill")
    gradient_fill = Inc("gradient_fill")
    #
    solid_line = Inc("solid_line")
    dashed = Inc("dashed")
    dash_little_gap = Inc("dash_little_gap")
    dash_big_gap = Inc("dash_big_gap")
    little_dash = Inc("little_dash")
    dash_dot = Inc("dash_dot")
    dash_dot_dot = Inc("dash_dot_dot")
    scale_factor = Inc("scale_factor")
    #
    points = Inc("points")
    inches = Inc("inches")
    mm = Inc("mm")
    cm = Inc("cm")
    ft = Inc("ft")
    #
    cap_butt = Inc("cap_butt")
    cap_round = Inc("cap_round")
    cap_projecting = Inc("cap_projecting")
    #
    join_miter = Inc("join_miter")
    join_round = Inc("join_round")
    join_bevel = Inc("join_bevel")
    #
    # The following fonts should be in every implementation
    Sans = Inc("Sans")  # e.g., Helvetica, Arial
    SansBold = Inc("SansBold")
    SansItalic = Inc("SansItalic")
    SansBoldItalic = Inc("SansBoldItalic")
    Serif = Inc("Serif")  # e.g., Times Roman
    SerifBold = Inc("SerifBold")
    SerifItalic = Inc("SerifItalic")
    SerifBoldItalic = Inc("SerifBoldItalic")
    Courier = Inc("Courier")
    CourierBold = Inc("CourierBold")
    CourierBoldItalic = Inc("CourierBoldItalic")
    CourierItalic = Inc("CourierItalic")
    Symbol = Inc("Symbol")
    #
    # The following fonts are implementation dependent.  These are Postscript
    # fonts for the HP 4050 LaserJet printer.
    AlbertusExtraBold = Inc("AlbertusExtraBold")
    AlbertusMedium = Inc("AlbertusMedium")
    AntiqueOlive = Inc("AntiqueOlive")
    AntiqueOliveBold = Inc("AntiqueOliveBold")
    AntiqueOliveItalic = Inc("AntiqueOliveItalic")
    Arial = Inc("Arial")
    ArialBold = Inc("ArialBold")
    ArialItalic = Inc("ArialItalic")
    ArialBoldItalic = Inc("ArialBoldItalic")
    AvantGarde = Inc("AvantGarde")
    AvantGardeBold = Inc("AvantGardeBold")
    AvantGardeItalic = Inc("AvantGardeItalic")
    AvantGardeBoldItalic = Inc("AvantGardeBoldItalic")
    Bookman = Inc("Bookman")
    BookmanBold = Inc("BookmanBold")
    BookmanItalic = Inc("BookmanItalic")
    BookmanBoldItalic = Inc("BookmanBoldItalic")
    Omega = Inc("Omega")
    OmegaBold = Inc("OmegaBold")
    OmegaItalic = Inc("OmegaItalic")
    OmegaBoldItalic = Inc("OmegaBoldItalic")
    CGTimes = Inc("CGTimes")
    CGTimesBold = Inc("CGTimesBold")
    CGTimesItalic = Inc("CGTimesItalic")
    CGTimesBoldItalic = Inc("CGTimesBoldItalic")
    ClarendonCondensedBold = Inc("ClarendonCondensedBold")
    Coronet = Inc("Coronet")
    GaramondAntiqua = Inc("GaramondAntiqua")
    GaramondHalbfett = Inc("GaramondHalbfett")
    GaramondKursiv = Inc("GaramondKursiv")
    GaramondKursivHalbfett = Inc("GaramondKursivHalbfett")
    Helvetica = Inc("Helvetica")
    HelveticaBold = Inc("HelveticaBold")
    HelveticaBoldOblique = Inc("HelveticaBoldOblique")
    HelveticaOblique = Inc("HelveticaOblique")
    HelveticaNarrow = Inc("HelveticaNarrow")
    HelveticaNarrowBold = Inc("HelveticaNarrowBold")
    HelveticaNarrowBoldOblique = Inc("HelveticaNarrowBoldOblique")
    HelveticaNarrowOblique = Inc("HelveticaNarrowOblique")
    Marigold = Inc("Marigold")
    Times = Inc("Times")
    TimesBold = Inc("TimesBold")
    TimesBoldItalic = Inc("TimesBoldItalic")
    TimesItalic = Inc("TimesItalic")
    UniversMedium = Inc("UniversMedium")
    UniversMediumItalic = Inc("UniversMediumItalic")
    UniversBold = Inc("UniversBold")
    UniversBoldItalic = Inc("UniversBoldItalic")
    UniversCondensedMedium = Inc("UniversCondensedMedium")
    UniversCondensedMediumItalic = Inc("UniversCondensedMediumItalic")
    UniversCondensedBold = Inc("UniversCondensedBold")
    UniversCondensedBoldItalic = Inc("UniversCondensedBoldItalic")
    Dingbats = Inc("Dingbats")
if 1:  # Color definitions
    # These came from an X Windows rgb.txt file
    aliceblue = (0.94, 0.97, 1.00)
    antiquewhite = (0.98, 0.92, 0.84)
    aquamarine = (0.20, 0.75, 0.76)
    aquamarine1 = (0.50, 1.00, 0.83)
    aquamarine2 = (0.46, 0.93, 0.78)
    aquamarine3 = (0.40, 0.80, 0.67)
    aquamarine4 = (0.27, 0.55, 0.45)
    azure = (0.94, 1.00, 1.00)
    azure1 = (0.94, 1.00, 1.00)
    azure2 = (0.88, 0.93, 0.93)
    azure3 = (0.76, 0.80, 0.80)
    azure4 = (0.51, 0.55, 0.55)
    beige = (0.96, 0.96, 0.86)
    bisque = (1.00, 0.89, 0.77)
    bisque1 = (1.00, 0.89, 0.77)
    bisque2 = (0.93, 0.84, 0.72)
    bisque3 = (0.80, 0.72, 0.62)
    bisque4 = (0.55, 0.49, 0.42)
    black = (0.00, 0.00, 0.00)
    blanchedalmond = (1.00, 0.92, 0.80)
    blue = (0.00, 0.00, 1.00)
    blue1 = (0.00, 0.00, 1.00)
    blue2 = (0.00, 0.00, 0.93)
    blue3 = (0.00, 0.00, 0.80)
    blue4 = (0.00, 0.00, 0.55)
    blueviolet = (0.54, 0.17, 0.89)
    brown = (0.65, 0.16, 0.16)
    brown1 = (1.00, 0.25, 0.25)
    brown2 = (0.93, 0.23, 0.23)
    brown3 = (0.80, 0.20, 0.20)
    brown4 = (0.55, 0.14, 0.14)
    burlywood = (0.87, 0.72, 0.53)
    burlywood1 = (1.00, 0.83, 0.61)
    burlywood2 = (0.93, 0.77, 0.57)
    burlywood3 = (0.80, 0.67, 0.49)
    burlywood4 = (0.55, 0.45, 0.33)
    cadetblue = (0.37, 0.57, 0.62)
    chartreuse = (0.50, 1.00, 0.00)
    chartreuse1 = (0.50, 1.00, 0.00)
    chartreuse2 = (0.46, 0.93, 0.00)
    chartreuse3 = (0.40, 0.80, 0.00)
    chartreuse4 = (0.27, 0.55, 0.00)
    chocolate = (0.82, 0.41, 0.12)
    chocolate1 = (1.00, 0.50, 0.14)
    chocolate2 = (0.93, 0.46, 0.13)
    chocolate3 = (0.80, 0.40, 0.11)
    chocolate4 = (0.55, 0.27, 0.07)
    coral = (1.00, 0.45, 0.34)
    coral1 = (1.00, 0.45, 0.34)
    coral2 = (0.93, 0.42, 0.31)
    coral3 = (0.80, 0.36, 0.27)
    coral4 = (0.55, 0.24, 0.18)
    cornflowerblue = (0.13, 0.13, 0.60)
    cornsilk = (1.00, 0.97, 0.86)
    cornsilk1 = (1.00, 0.97, 0.86)
    cornsilk2 = (0.93, 0.91, 0.80)
    cornsilk3 = (0.80, 0.78, 0.69)
    cornsilk4 = (0.55, 0.53, 0.47)
    cyan = (0.00, 1.00, 1.00)
    cyan1 = (0.00, 1.00, 1.00)
    cyan2 = (0.00, 0.93, 0.93)
    cyan3 = (0.00, 0.80, 0.80)
    cyan4 = (0.00, 0.55, 0.55)
    darkgoldenrod = (0.72, 0.53, 0.04)
    darkgreen = (0.00, 0.34, 0.18)
    darkkhaki = (0.74, 0.72, 0.42)
    darkolivegreen = (0.33, 0.34, 0.18)
    darkorange = (1.00, 0.55, 0.00)
    darkorchid = (0.55, 0.13, 0.55)
    darksalmon = (0.91, 0.59, 0.48)
    darkseagreen = (0.56, 0.74, 0.56)
    darkslateblue = (0.22, 0.29, 0.40)
    darkslategray = (0.18, 0.31, 0.31)
    darkslategrey = (0.18, 0.31, 0.31)
    darkturquoise = (0.00, 0.65, 0.65)
    darkviolet = (0.58, 0.00, 0.83)
    deeppink = (1.00, 0.08, 0.58)
    deepskyblue = (0.00, 0.75, 1.00)
    dimgray = (0.33, 0.33, 0.33)
    dimgrey = (0.33, 0.33, 0.33)
    dodgerblue = (0.12, 0.56, 1.00)
    firebrick = (0.56, 0.14, 0.14)
    firebrick1 = (1.00, 0.19, 0.19)
    firebrick2 = (0.93, 0.17, 0.17)
    firebrick3 = (0.80, 0.15, 0.15)
    firebrick4 = (0.55, 0.10, 0.10)
    floralwhite = (1.00, 0.98, 0.94)
    forestgreen = (0.31, 0.62, 0.41)
    gainsboro = (0.86, 0.86, 0.86)
    ghostwhite = (0.97, 0.97, 1.00)
    gold = (0.85, 0.67, 0.00)
    gold1 = (1.00, 0.84, 0.00)
    gold2 = (0.93, 0.79, 0.00)
    gold3 = (0.80, 0.68, 0.00)
    gold4 = (0.55, 0.46, 0.00)
    goldenrod = (0.94, 0.87, 0.52)
    goldenrod1 = (1.00, 0.76, 0.15)
    goldenrod2 = (0.93, 0.71, 0.13)
    goldenrod3 = (0.80, 0.61, 0.11)
    goldenrod4 = (0.55, 0.41, 0.08)
    green = (0.00, 1.00, 0.00)
    green1 = (0.00, 1.00, 0.00)
    green2 = (0.00, 0.93, 0.00)
    green3 = (0.00, 0.80, 0.00)
    green4 = (0.00, 0.55, 0.00)
    greenyellow = (0.68, 1.00, 0.18)
    honeydew = (0.94, 1.00, 0.94)
    honeydew1 = (0.94, 1.00, 0.94)
    honeydew2 = (0.88, 0.93, 0.88)
    honeydew3 = (0.76, 0.80, 0.76)
    honeydew4 = (0.51, 0.55, 0.51)
    hotpink = (1.00, 0.41, 0.71)
    indianred = (0.42, 0.22, 0.22)
    ivory = (1.00, 1.00, 0.94)
    ivory1 = (1.00, 1.00, 0.94)
    ivory2 = (0.93, 0.93, 0.88)
    ivory3 = (0.80, 0.80, 0.76)
    ivory4 = (0.55, 0.55, 0.51)
    khaki = (0.70, 0.70, 0.49)
    khaki1 = (1.00, 0.96, 0.56)
    khaki2 = (0.93, 0.90, 0.52)
    khaki3 = (0.80, 0.78, 0.45)
    khaki4 = (0.55, 0.53, 0.31)
    lavender = (0.90, 0.90, 0.98)
    lavenderblush = (1.00, 0.94, 0.96)
    lawngreen = (0.49, 0.99, 0.00)
    lemonchiffon = (1.00, 0.98, 0.80)
    lightblue = (0.69, 0.89, 1.00)
    lightcoral = (0.94, 0.50, 0.50)
    lightcyan = (0.88, 1.00, 1.00)
    lightgoldenrod = (0.93, 0.87, 0.51)
    lightgoldenrodyellow = (0.98, 0.98, 0.82)
    lightgray = (0.66, 0.66, 0.66)
    lightgrey = (0.66, 0.66, 0.66)
    lightpink = (1.00, 0.71, 0.76)
    lightsalmon = (1.00, 0.63, 0.48)
    lightseagreen = (0.13, 0.70, 0.67)
    lightskyblue = (0.53, 0.81, 0.98)
    lightslateblue = (0.52, 0.44, 1.00)
    lightslategray = (0.47, 0.53, 0.60)
    lightslategrey = (0.47, 0.53, 0.60)
    lightsteelblue = (0.49, 0.60, 0.83)
    lightyellow = (1.00, 1.00, 0.88)
    limegreen = (0.00, 0.69, 0.08)
    linen = (0.98, 0.94, 0.90)
    magenta = (1.00, 0.00, 1.00)
    magenta1 = (1.00, 0.00, 1.00)
    magenta2 = (0.93, 0.00, 0.93)
    magenta3 = (0.80, 0.00, 0.80)
    magenta4 = (0.55, 0.00, 0.55)
    maroon = (0.56, 0.00, 0.32)
    maroon1 = (1.00, 0.20, 0.70)
    maroon2 = (0.93, 0.19, 0.65)
    maroon3 = (0.80, 0.16, 0.56)
    maroon4 = (0.55, 0.11, 0.38)
    mediumaquamarine = (0.00, 0.58, 0.56)
    mediumblue = (0.20, 0.20, 0.80)
    mediumforestgreen = (0.20, 0.51, 0.29)
    mediumgoldenrod = (0.82, 0.76, 0.40)
    mediumorchid = (0.74, 0.32, 0.74)
    mediumpurple = (0.58, 0.44, 0.86)
    mediumseagreen = (0.20, 0.47, 0.40)
    mediumslateblue = (0.42, 0.42, 0.55)
    mediumspringgreen = (0.14, 0.56, 0.14)
    mediumturquoise = (0.00, 0.82, 0.82)
    mediumvioletred = (0.84, 0.13, 0.47)
    midnightblue = (0.18, 0.18, 0.39)
    mintcream = (0.96, 1.00, 0.98)
    mistyrose = (1.00, 0.89, 0.88)
    moccasin = (1.00, 0.89, 0.71)
    navajowhite = (1.00, 0.87, 0.68)
    navy = (0.14, 0.14, 0.46)
    navyblue = (0.14, 0.14, 0.46)
    oldlace = (0.99, 0.96, 0.90)
    olivedrab = (0.42, 0.56, 0.14)
    orange = (1.00, 0.53, 0.00)
    orange1 = (1.00, 0.65, 0.00)
    orange2 = (0.93, 0.60, 0.00)
    orange3 = (0.80, 0.52, 0.00)
    orange4 = (0.55, 0.35, 0.00)
    orangered = (1.00, 0.27, 0.00)
    orchid = (0.94, 0.52, 0.94)
    orchid1 = (1.00, 0.51, 0.98)
    orchid2 = (0.93, 0.48, 0.91)
    orchid3 = (0.80, 0.41, 0.79)
    orchid4 = (0.55, 0.28, 0.54)
    palegoldenrod = (0.93, 0.91, 0.67)
    palegreen = (0.45, 0.87, 0.47)
    paleturquoise = (0.69, 0.93, 0.93)
    palevioletred = (0.86, 0.44, 0.58)
    papayawhip = (1.00, 0.94, 0.84)
    peachpuff = (1.00, 0.85, 0.73)
    peru = (0.80, 0.52, 0.25)
    pink = (1.00, 0.71, 0.77)
    pink1 = (1.00, 0.71, 0.77)
    pink2 = (0.93, 0.66, 0.72)
    pink3 = (0.80, 0.57, 0.62)
    pink4 = (0.55, 0.39, 0.42)
    plum = (0.77, 0.28, 0.61)
    plum1 = (1.00, 0.73, 1.00)
    plum2 = (0.93, 0.68, 0.93)
    plum3 = (0.80, 0.59, 0.80)
    plum4 = (0.55, 0.40, 0.55)
    powderblue = (0.69, 0.88, 0.90)
    purple = (0.63, 0.13, 0.94)
    purple1 = (0.61, 0.19, 1.00)
    purple2 = (0.57, 0.17, 0.93)
    purple3 = (0.49, 0.15, 0.80)
    purple4 = (0.33, 0.10, 0.55)
    red = (1.00, 0.00, 0.00)
    red1 = (1.00, 0.00, 0.00)
    red2 = (0.93, 0.00, 0.00)
    red3 = (0.80, 0.00, 0.00)
    red4 = (0.55, 0.00, 0.00)
    rosybrown = (0.74, 0.56, 0.56)
    royalblue = (0.25, 0.41, 0.88)
    saddlebrown = (0.55, 0.27, 0.07)
    salmon = (0.91, 0.59, 0.48)
    salmon1 = (1.00, 0.55, 0.41)
    salmon2 = (0.93, 0.51, 0.38)
    salmon3 = (0.80, 0.44, 0.33)
    salmon4 = (0.55, 0.30, 0.22)
    sandybrown = (0.96, 0.64, 0.38)
    seagreen = (0.32, 0.58, 0.52)
    seashell = (1.00, 0.96, 0.93)
    seashell1 = (1.00, 0.96, 0.93)
    seashell2 = (0.93, 0.90, 0.87)
    seashell3 = (0.80, 0.77, 0.75)
    seashell4 = (0.55, 0.53, 0.51)
    sienna = (0.59, 0.32, 0.18)
    sienna1 = (1.00, 0.51, 0.28)
    sienna2 = (0.93, 0.47, 0.26)
    sienna3 = (0.80, 0.41, 0.22)
    sienna4 = (0.55, 0.28, 0.15)
    skyblue = (0.45, 0.62, 1.00)
    slateblue = (0.49, 0.53, 0.67)
    slategray = (0.44, 0.50, 0.56)
    slategrey = (0.44, 0.50, 0.56)
    snow = (1.00, 0.98, 0.98)
    snow1 = (1.00, 0.98, 0.98)
    snow2 = (0.93, 0.91, 0.91)
    snow3 = (0.80, 0.79, 0.79)
    snow4 = (0.55, 0.54, 0.54)
    springgreen = (0.25, 0.67, 0.25)
    steelblue = (0.33, 0.44, 0.67)
    tan = (0.87, 0.72, 0.53)
    tan1 = (1.00, 0.65, 0.31)
    tan2 = (0.93, 0.60, 0.29)
    tan3 = (0.80, 0.52, 0.25)
    tan4 = (0.55, 0.35, 0.17)
    thistle = (0.85, 0.75, 0.85)
    thistle1 = (1.00, 0.88, 1.00)
    thistle2 = (0.93, 0.82, 0.93)
    thistle3 = (0.80, 0.71, 0.80)
    thistle4 = (0.55, 0.48, 0.55)
    tomato = (1.00, 0.39, 0.28)
    tomato1 = (1.00, 0.39, 0.28)
    tomato2 = (0.93, 0.36, 0.26)
    tomato3 = (0.80, 0.31, 0.22)
    tomato4 = (0.55, 0.21, 0.15)
    transparent = (0.00, 0.00, 0.00)
    turquoise = (0.10, 0.80, 0.87)
    turquoise1 = (0.00, 0.96, 1.00)
    turquoise2 = (0.00, 0.90, 0.93)
    turquoise3 = (0.00, 0.77, 0.80)
    turquoise4 = (0.00, 0.53, 0.55)
    violet = (0.61, 0.24, 0.81)
    violetred = (0.95, 0.24, 0.59)
    wheat = (0.96, 0.87, 0.70)
    wheat1 = (1.00, 0.91, 0.73)
    wheat2 = (0.93, 0.85, 0.68)
    wheat3 = (0.80, 0.73, 0.59)
    wheat4 = (0.55, 0.49, 0.40)
    white = (1.00, 1.00, 1.00)
    whitesmoke = (0.96, 0.96, 0.96)
    yellow = (1.00, 1.00, 0.00)
    yellow1 = (1.00, 1.00, 0.00)
    yellow2 = (0.93, 0.93, 0.00)
    yellow3 = (0.80, 0.80, 0.00)
    yellow4 = (0.55, 0.55, 0.00)
    yellowgreen = (0.20, 0.85, 0.22)
if 1:  # Constants to identify graphics state (GS) elements
    g_paper_size = Inc("g_paper_size")
    g_orientation = Inc("g_orientation")
    g_units = Inc("g_units")
    g_line = Inc("g_line")
    g_fill = Inc("g_fill")
    g_font = Inc("g_font")
    g_ctm = Inc("g_ctm")
    g_current_path = Inc("g_current_path")
    g_current_clip_path = Inc("g_current_clip_path")
    g_current_point = Inc("g_current_point")
    g_current_color = Inc("g_current_color")
    g_scale_line_width = Inc("g_scale_line_width")
    g_scale_font_size = Inc("g_scale_font_size")
if 1:  # Indexes into class changed flag & value
    g_changed = 0
    g_value = 1
if 1:  # Constants used to identify paper sizes
    paper_letter = Inc("paper_letter")
    paper_legal = Inc("paper_legal")
    paper_ledger = Inc("paper_ledger")  # 11x17
    paper_A4 = Inc("paper_A4")
if 1:  # Constants used to identify a subpath element
    path_point = Inc("path_point")
    path_arc_ccw = Inc("path_arc_ccw")
    path_arc_cw = Inc("path_arc_cw")
    path_bezier = Inc("path_bezier")
if 1:  # Constant for PJL
    UEL = "\033%-12345X"  # Used in PJL
if 1:  # Clean up
    del index
    del Inc
if 1:  # Convenience function to calculate ISO paper sizes
    def ISO_paper(n, format):
        '''Return a tuple of (width, height) for ISO paper sizes.  The
        dimensions are in points.  The format parameter must be "A", "B", or
        "C" and n must be an integer between 0 and 10.  The width and height
        are given in points.  The formulas are taken from
        http://www.cl.cam.ac.uk/~mgk25/iso-paper.html.
        '''
        import math
        if n < 0 or n > 10 or int(n) != n:
            raise Exception("n must be an integer >=  and <= 10")
        # The following formulas give the paper dimensions in m
        if format == "A":
            width = math.pow(2, -1 / 4.0 - n / 2.0)
            height = math.pow(2, 1 / 4.0 - n / 2.0)
        elif format == "B":
            width = math.pow(2, -n / 2.0)
            height = math.pow(2, 1 / 2.0 - n / 2.0)
        elif format == "C":
            width = math.pow(2, -1 / 8.0 - n / 2.0)
            height = math.pow(2, 3 / 8.0 - n / 2.0)
        else:
            raise Exception("Unrecognized ISO paper format")
        m_to_points = 2845.2756  # Conversion factor
        return (int(width * m_to_points), int(height * m_to_points))
if 1:  # Dictionaries used to translate and validate values
    paper_sizes = {  # (width, height) in portrait mode in points
        paper_letter: (8.5 * 72, 11.0 * 72),
        paper_legal: (8.5 * 72, 14.0 * 72),
        paper_ledger: (11.0 * 72, 17.0 * 72),
        paper_A4: ISO_paper(4, "A"),
    }
    allowed_orientations = {  # Gives rotation angle
        portrait: 0,
        seascape: 90,
        inverse_portrait: 180,
        landscape: 270,
    }
    allowed_units = {  # Convenience array of scaling factors.  These factors
        # convert back to the default Postscript units, which
        # are points.
        points: 1.0,
        inches: 72.0,
        mm: 72.0 / 25.4,
        cm: 72.0 / 2.54,
        ft: 72.0 * 12,
    }
    allowed_fill_types = {
        no_fill: no_fill,
        solid_fill: solid_fill,
        line_fill: line_fill,
        gradient_fill: gradient_fill,
    }
    dashes = {  # Maps dash types to their Postscript setdash values.  These
        # sizes are in the Postscript default units, which are points.
        # The first number is the length of the first dash, the second
        # number is the width of the space, etc.
        solid_line: [],
        dashed: [10, 10],
        dash_little_gap: [20, 4],
        dash_big_gap: [1, 10],
        little_dash: [4, 4],
        dash_dot: [10, 2, 2, 2],
        dash_dot_dot: [10, 2, 2, 2, 2, 2],
        scale_factor: 1.0,  # Used to scale the dash sizes
    }
    line_caps = {
        cap_butt: 0,
        cap_round: 1,
        cap_projecting: 2,
    }
    line_joins = {
        join_miter: 0,
        join_round: 1,
        join_bevel: 2,
    }
    allowed_font_names = {
        Sans: "Helvetica",
        SansBold: "Helvetica-Bold",
        SansItalic: "Helvetica-Italic",
        SansBoldItalic: "Helvetica-BoldItalic",
        Serif: "Times-Roman",
        SerifBold: "Times-Bold",
        SerifItalic: "Times-Oblique",
        SerifBoldItalic: "Times-BoldOblique",
        AlbertusExtraBold: "Albertus-ExtraBold",
        AlbertusMedium: "Albertus-Medium",
        AntiqueOlive: "AntiqueOlive",
        AntiqueOliveBold: "AntiqueOlive-Bold",
        AntiqueOliveItalic: "AntiqueOlive-Italic",
        Arial: "Arial",
        ArialBold: "Arial-Bold",
        ArialItalic: "Arial-Italic",
        ArialBoldItalic: "Arial-BoldItalic",
        AvantGarde: "AvantGarde-Book",
        AvantGardeBold: "AvantGarde-Demi",
        AvantGardeItalic: "AvantGarde-BookOblique",
        AvantGardeBoldItalic: "AvantGarde-DemiOblique",
        Bookman: "Bookman-Light",
        BookmanBold: "Bookman-Demi",
        BookmanItalic: "Bookman-LightItalic",
        BookmanBoldItalic: "Bookman-DemiItalic",
        Omega: "CGOmega",
        OmegaBold: "CGOmega-Bold",
        OmegaItalic: "CGOmega-Italic",
        OmegaBoldItalic: "CGOmega-BoldItalic",
        CGTimes: "CGTimes",
        CGTimesBold: "CGTimes-Bold",
        CGTimesItalic: "CGTimes-Italic",
        CGTimesBoldItalic: "CGTimes-BoldItalic",
        ClarendonCondensedBold: "Clarendon-Condensed-Bold",
        Coronet: "Coronet",
        Courier: "Courier",
        CourierBold: "Courier-Bold",
        CourierBoldItalic: "Courier-BoldItalic",
        CourierItalic: "Courier-Italic",
        GaramondAntiqua: "Garamond-Antiqua",
        GaramondHalbfett: "Garamond-Halbfett",
        GaramondKursiv: "Garamond-Kursiv",
        GaramondKursivHalbfett: "Garamond-KursivHalbfett",
        Helvetica: "Helvetica",
        HelveticaBold: "Helvetica-Bold",
        HelveticaBoldOblique: "Helvetica-BoldOblique",
        HelveticaOblique: "Helvetica-Oblique",
        HelveticaNarrow: "Helvetica-Narrow",
        HelveticaNarrowBold: "Helvetica-Narrow-Bold",
        HelveticaNarrowBoldOblique: "Helvetica-Narrow-BoldOblique",
        HelveticaNarrowOblique: "Helvetica-Narrow-Oblique",
        Marigold: "Marigold",
        Symbol: "Symbol",
        Times: "Times-Roman",
        TimesBold: "Times-Bold",
        TimesBoldItalic: "Times-BoldItalic",
        TimesItalic: "Times-Italic",
        UniversMedium: "Univers-Medium",
        UniversMediumItalic: "Univers-MediumItalic",
        UniversBold: "Univers-Bold",
        UniversBoldItalic: "Univers-BoldItalic",
        UniversCondensedMedium: "Univers-Condensed-Medium",
        UniversCondensedMediumItalic: "Univers-Condensed-MediumItalic",
        UniversCondensedBold: "Univers-Condensed-Bold",
        UniversCondensedBoldItalic: "Univers-Condensed-BoldItalic",
        Dingbats: "ZapfDingbats",
    }
    # The ps dictionary is used to save a little space in the output Postscript
    # file by aliasing the Postscript commands with single characters.  Of
    # course, this makes the output file impossible to read easily, so you'll
    # want to set translate_PS to no for debugging the Postscript output.
    translate_PS = yes
    ps = {
        "arc": "",
        "begin": "",
        "bind": "",
        "closepath": "",
        "colorimage": "",
        "currentmatrix": "",
        "curveto": "",
        "dict": "",
        "div": "",
        "ellipse": "",
        "ellipsedict": "",
        "eofill": "",
        "exch": "",
        "fill": "",
        "findfont": "",
        "flattenpath": "",
        "grestore": "",
        "gsave": "",
        "initmatrix": "",
        "lineto": "",
        "matrix": "",
        "moveto": "",
        "newpath": "",
        "readhexstring": "",
        "rlineto": "",
        "rmoveto": "",
        "rotate": "",
        "savematrix": "",
        "scale": "",
        "scalefont": "",
        "setdash": "",
        "setfont": "",
        "setlinecap": "",
        "setlinejoin": "",
        "setlinewidth": "",
        "setmatrix": "",
        "setmiterlimit": "",
        "setrgbcolor": "",
        "show": "",
        "showpage": "",
        "stroke": "",
        "translate": "",
    }
    if translate_PS == yes:
        # Set the values to single letters
        value = ord("A")
        for key in ps.keys():
            ps[key] = chr(value)
            value = value + 1
            if value == ord("Z"):
                value = ord("a")
    else:
        # Use the full Postscript names
        for key in ps.keys():
            ps[key] = key
    # The INV dictionary will contain a mapping from integer value to the
    # constant's name.  This will help with debugging output by giving
    # symbolic names, rather than integers.
    INV = {}
    g = globals()
    for key in g.keys():
        if type(g[key]) == type(0):
            INV[g[key]] = key
        elif type(g[key]) == type((0,)) and len(g[key]) == 3:  # A color tuple
            INV[g[key]] = key
    del g
if 1:  # PostScript chunks
    # The following chunks of Postscript are used as needed by the program.
    # Note they aren't output unless functions that use them are called.

    # Code to draw an ellipse.  From the Blue Book, pg. 137.
    ellipse_ps = '''
        /edct 8 dict def edct /mtrx matrix put /ellipse { edct begin /ea
        exch def /sa exch def /md exch def /Md exch def /y exch def /x exch
        def /sm mtrx currentmatrix def newpath x y translate Md 2 div md 2
        div scale 0 0 1 sa ea arc sm setmatrix end } def
    '''

    # This is code to put text in a circle, from the Adobe Blue Book, pg 167
    # (names were shortened).
    circ_text_ps = '''
        % Text on a circular path
        /outsidecircletext
        { circtextdict
        begin
            /radius exch def
            /centerangle exch def
            /ptsize exch def
            /str exch def
            /xradius radius ptsize 4 div add def
            gsave
            centerangle str findhalfangle add rotate
            str
                { /charcode exch def
                ( ) dup 0 charcode put outsideplacechar
                } forall
            grestore
        end
        } def
        /insidecircletext
        { circtextdict
        begin
            /radius exch def
            /centerangle exch def
            /ptsize exch def
            /str exch def
            /xradius radius ptsize 3 div add def
            gsave
            centerangle str findhalfangle sub rotate
            str
                { /charcode exch def
                ( ) dup 0 charcode put insideplacechar
                } forall
            grestore
        end
        } def
        /circtextdict 16 dict def
        circtextdict
        begin
            /findhalfangle  {
            stringwidth pop 2 div
            2 xradius mul pi mul div 360 mul
            } def
            /outsideplacechar {
            /char exch def
            /halfangle char findhalfangle def
            gsave
                halfangle neg rotate
                radius 0 translate
                -90 rotate
                char stringwidth pop 2 div neg 0 moveto
                char show
            grestore
            halfangle 2 mul neg rotate
            } def
            /insideplacechar {
            /char exch def
            /halfangle char findhalfangle def
            gsave
                halfangle rotate
                radius 0 translate
                90 rotate
                char stringwidth pop 2 div neg 0 moveto
                char show
            grestore
            halfangle 2 mul rotate
            } def
            /pi 3.1415926 def
        end
    '''

    # From Adobe Blue Book pg 171:  Postscript code to print text along a path
    path_text_ps = '''
        /pathtextdict 26 dict def
        /pathtext
        { pathtextdict begin
            /offset exch def
            /str exch def
            /pathdist 0 def
            /setdist offset def
            /charcount 0 def
            gsave
            flattenpath
            {movetoproc} {linetoproc}
            {curvetoproc} {closepathproc}
            pathforall
            grestore
            newpath
        end
        } def
        pathtextdict begin
        /movetoproc {
        /newy exch def /newx exch def
        /firstx newx def /firsty newy def
        /ovr 0 def
        newx newy transform
        /cpy exch def /cpx exch def
        } def
        /linetoproc {
        /oldx newx def /oldy newy def
        /newy exch def /newx exch def
        /dx newx oldx sub def
        /dy newy oldy sub def
        /dist dx dup mul dy dup mul add sqrt def
        dist 0 ne {
            /dsx dx dist div ovr mul def
            /dsy dy dist div ovr mul def
            oldx dsx add oldy dsy add transform
            /cpy exch def /cpx exch def
            /pathdist pathdist dist add def
            { setdist pathdist le
            { charcount str length lt {setchar} {exit} ifelse }
            { /ovr setdist pathdist sub def exit } ifelse
            } loop
        } if
        } def
        /curvetoproc {
        (ERROR:  no curveto's after a flattenpath!) print
        } def
        /closepathproc {
        firstx firsty linetoproc
        firstx firsty movetoproc
        } def
        /setchar {
        /char str charcount 1 getinterval def
        /charcount charcount 1 add def
        /charwidth char stringwidth pop def
        gsave
            cpx cpy itransform translate
            dy dx atan rotate
            0 0 moveto char show
            currentpoint transform
            /cpy exch def /cpx exch def
        grestore
        /setdist setdist charwidth add def
        } def
        end
    '''

    # From Adobe Blue Book pg 161:  Postscript code to print fractions
    fraction_text_ps = '''
        /fractiondict 5 dict def
        /fractionshow {
        fractiondict begin
            /denominator exch def
            /numerator exch def
            /regularfont currentfont def
            /fractionfont currentfont [.65 0 0 .6 0 0] makefont def
            gsave
            newpath
                0 0 moveto
                (1) true charpath
            flattenpath pathbbox
            /height exch def pop pop pop
            grestore
            0 .4 height mul rmoveto
            fractionfont setfont numerator show
            0 .4 height mul neg rmoveto
            regularfont setfont (\244) show
            fractionfont setfont denominator show
            regularfont setfont
        end
        } def
    '''
class Colors:
    def __init__(self):
        self.colors = Dedent('''
        aliceblue           darkolivegreen      lightgray           plum
        antiquewhite        darkorange          lightgrey           plum1
        aquamarine          darkorchid          lightpink           plum2
        aquamarine1         darksalmon          lightsalmon         plum3
        aquamarine2         darkseagreen        lightseagreen       plum4
        aquamarine3         darkslateblue       lightskyblue        powderblue
        aquamarine4         darkslategray       lightslateblue      purple
        azure               darkslategrey       lightslategray      purple1
        azure1              darkturquoise       lightslategrey      purple2
        azure2              darkviolet          lightsteelblue      purple3
        azure3              deeppink            lightyellow         purple4
        azure4              deepskyblue         limegreen           red
        beige               dimgray             linen               red1
        bisque              dimgrey             magenta             red2
        bisque1             dodgerblue          magenta1            red3
        bisque2             firebrick           magenta2            red4
        bisque3             firebrick1          magenta3            rosybrown
        bisque4             firebrick2          magenta4            royalblue
        black               firebrick3          maroon              saddlebrown
        blanchedalmond      firebrick4          maroon1             salmon
        blue                floralwhite         maroon2             salmon1
        blue1               forestgreen         maroon3             salmon2
        blue2               gainsboro           maroon4             salmon3
        blue3               ghostwhite          mediumaquamarine    salmon4
        blue4               gold                mediumblue          sandybrown
        blueviolet          gold1               mediumforestgreen   seagreen
        brown               gold2               mediumgoldenrod     seashell
        brown1              gold3               mediumorchid        seashell1
        brown2              gold4               mediumpurple        seashell2
        brown3              goldenrod           mediumseagreen      seashell3
        brown4              goldenrod1          mediumslateblue     seashell4
        burlywood           goldenrod2          mediumspringgreen   sienna
        burlywood1          goldenrod3          mediumturquoise     sienna1
        burlywood2          goldenrod4          mediumvioletred     sienna2
        burlywood3          green               midnightblue        sienna3
        burlywood4          green1              mintcream           sienna4
        cadetblue           green2              mistyrose           skyblue
        chartreuse          green3              moccasin            slateblue
        chartreuse1         green4              navajowhite         slategray
        chartreuse2         greenyellow         navy                slategrey
        chartreuse3         honeydew            navyblue            snow
        chartreuse4         honeydew1           oldlace             snow1
        chocolate           honeydew2           olivedrab           snow2
        chocolate1          honeydew3           orange              snow3
        chocolate2          honeydew4           orange1             snow4
        chocolate3          hotpink             orange2             springgreen
        chocolate4          indianred           orange3             steelblue
        coral               ivory               orange4             tan
        coral1              ivory1              orangered           tan1
        coral2              ivory2              orchid              tan2
        coral3              ivory3              orchid1             tan3
        coral4              ivory4              orchid2             tan4
        cornflowerblue      khaki               orchid3             thistle
        cornsilk            khaki1              orchid4             thistle1
        cornsilk1           khaki2              palegoldenrod       thistle2
        cornsilk2           khaki3              palegreen           thistle3
        cornsilk3           khaki4              paleturquoise       thistle4
        cornsilk4           lavender            palevioletred       tomato
        cyan                lavenderblush       papayawhip          tomato1
        cyan1               lawngreen           peachpuff           tomato2
        cyan2               lemonchiffon        peru                tomato3
        cyan3               lightblue           pink                tomato4
        cyan4               lightcoral          pink1               transparent
        darkgoldenrod       lightcyan           pink2               turquoise
        darkgreen           lightgoldenrod      pink3               turquoise1
        darkkhaki           lightgoldenrodyello pink4               turquoise2
        turquoise3          wheat1              white               yellow2
        turquoise4          wheat2              whitesmoke          yellow3
        violet              wheat3              yellow              yellow4
        violetred           wheat4              yellow1             yellowgreen
        wheat
        '''.rstrip()[1:])
    def __str__(self):
        return self.colors
if 1:  # Print colors to get a listing of colors
    colors = Colors()

if __name__ == "__main__":
    import sys
    import re
    from pdb import set_trace as xx
    from columnize import Columnize
    if 0:
        import debug
        debug.SetDebugger()
    if 1:
        def GetNamesOfConstants(sort_by_number=True):
            '''Return a string representing the name of the constants that are
            represented by integers.
            '''
            if 1:  # Check for missing numbers (could be bug)
                k = list(varnames.keys())
                assert k == sorted(k)
                for i in range(1, len(k)):
                    if k[i - 1] + 1 != k[i]:
                        msg = f"Discontinuity in varnames indexes at {i}"
                        raise ValueError(msg)
            if 1:  # Return the names & values
                s = []
                items = varnames.items()
                if sort_by_number:
                    items = list(sorted(items))
                    for num, name in items:
                        s.append(f"{num:3d} {name}")
                else:
                    items = list(sorted([[j, i] for i, j in items]))
                    for name, num in items:
                        s.append(f"{name}: {num}")
                return s
        def WriteNamesOfConstants(file):
            def P(x):
                print(x, file=f)
            f = open(file, "w")
            s = "Names & values of constants in gco.py"
            P(s)
            P("")
            for i in Columnize(GetNamesOfConstants(True)):
                P(i)
            P("")
            for i in Columnize(GetNamesOfConstants(False)):
                P(i)
        WriteNamesOfConstants("gco.constants")
    # If run as a script, search for the constants that contain the
    # regexp(s) on the command line.
    if 0:
        sym = []
        # Get Inc() symbols
        lines = open(sys.argv[0]).readlines()
        r = re.compile(r'= Inc\(".*"\)')
        for i in lines:
            mo = r.search(i)
            if mo:
                loc = i.find("=")
                sym.append(i[:loc].strip())
        # Get colors
        r = re.compile(r"= \(.*?,.*?,.*\)")
        for i in lines:
            mo = r.search(i)
            if mo:
                sym.append(i.strip())
        for i in sys.argv[1:]:
            r = re.compile(i, re.I)
            for i in sym:
                mo = r.search(i)
                if mo:
                    print(i)
    else:
        args = sys.argv[1:]
        if not args:
            exit(0)
        print("Number is variable value and text is the variable's name:")
        cl, indent = [], " " * 4
        for text in args:
            r = re.compile(text, re.I)
            for symbol in GetNamesOfConstants():
                mo = r.search(symbol)
                if mo:
                    print(indent, symbol)
            for name in str(colors).split():
                mo = r.search(name)
                if mo:
                    cl.append(name)
        # Color search
        if cl:
            print("\nSearch of colors:")
            for i in sorted(cl):
                print(indent, i)
