'''
Prints a list of XWindows color names for a dictionary lookup
    The raw data for these names came from an X-Windows rgb.txt file.  The
    conversion was done by the /pylib/g/mkrgb.py script.  This script will
    print out python code that can be inserted into a script to provide a
    dictionary to convert a color name to an RGB tuple.
 
    Lines output are of the form:
        "aliceblue": (239, 247, 255),
        "antiquewhite": (249, 234, 214),
        etc.
'''
#∞test∞# ignore #∞test∞#
data = '''
    aliceblue            = (0.94, 0.97, 1.00)
    antiquewhite         = (0.98, 0.92, 0.84)
    aquamarine           = (0.20, 0.75, 0.76)
    aquamarine1          = (0.50, 1.00, 0.83)
    aquamarine2          = (0.46, 0.93, 0.78)
    aquamarine3          = (0.40, 0.80, 0.67)
    aquamarine4          = (0.27, 0.55, 0.45)
    azure                = (0.94, 1.00, 1.00)
    azure1               = (0.94, 1.00, 1.00)
    azure2               = (0.88, 0.93, 0.93)
    azure3               = (0.76, 0.80, 0.80)
    azure4               = (0.51, 0.55, 0.55)
    beige                = (0.96, 0.96, 0.86)
    bisque               = (1.00, 0.89, 0.77)
    bisque1              = (1.00, 0.89, 0.77)
    bisque2              = (0.93, 0.84, 0.72)
    bisque3              = (0.80, 0.72, 0.62)
    bisque4              = (0.55, 0.49, 0.42)
    black                = (0.00, 0.00, 0.00)
    blanchedalmond       = (1.00, 0.92, 0.80)
    blue                 = (0.00, 0.00, 1.00)
    blue1                = (0.00, 0.00, 1.00)
    blue2                = (0.00, 0.00, 0.93)
    blue3                = (0.00, 0.00, 0.80)
    blue4                = (0.00, 0.00, 0.55)
    blueviolet           = (0.54, 0.17, 0.89)
    brown                = (0.65, 0.16, 0.16)
    brown1               = (1.00, 0.25, 0.25)
    brown2               = (0.93, 0.23, 0.23)
    brown3               = (0.80, 0.20, 0.20)
    brown4               = (0.55, 0.14, 0.14)
    burlywood            = (0.87, 0.72, 0.53)
    burlywood1           = (1.00, 0.83, 0.61)
    burlywood2           = (0.93, 0.77, 0.57)
    burlywood3           = (0.80, 0.67, 0.49)
    burlywood4           = (0.55, 0.45, 0.33)
    cadetblue            = (0.37, 0.57, 0.62)
    chartreuse           = (0.50, 1.00, 0.00)
    chartreuse1          = (0.50, 1.00, 0.00)
    chartreuse2          = (0.46, 0.93, 0.00)
    chartreuse3          = (0.40, 0.80, 0.00)
    chartreuse4          = (0.27, 0.55, 0.00)
    chocolate            = (0.82, 0.41, 0.12)
    chocolate1           = (1.00, 0.50, 0.14)
    chocolate2           = (0.93, 0.46, 0.13)
    chocolate3           = (0.80, 0.40, 0.11)
    chocolate4           = (0.55, 0.27, 0.07)
    coral                = (1.00, 0.45, 0.34)
    coral1               = (1.00, 0.45, 0.34)
    coral2               = (0.93, 0.42, 0.31)
    coral3               = (0.80, 0.36, 0.27)
    coral4               = (0.55, 0.24, 0.18)
    cornflowerblue       = (0.13, 0.13, 0.60)
    cornsilk             = (1.00, 0.97, 0.86)
    cornsilk1            = (1.00, 0.97, 0.86)
    cornsilk2            = (0.93, 0.91, 0.80)
    cornsilk3            = (0.80, 0.78, 0.69)
    cornsilk4            = (0.55, 0.53, 0.47)
    cyan                 = (0.00, 1.00, 1.00)
    cyan1                = (0.00, 1.00, 1.00)
    cyan2                = (0.00, 0.93, 0.93)
    cyan3                = (0.00, 0.80, 0.80)
    cyan4                = (0.00, 0.55, 0.55)
    darkgoldenrod        = (0.72, 0.53, 0.04)
    darkgreen            = (0.00, 0.34, 0.18)
    darkkhaki            = (0.74, 0.72, 0.42)
    darkolivegreen       = (0.33, 0.34, 0.18)
    darkorange           = (1.00, 0.55, 0.00)
    darkorchid           = (0.55, 0.13, 0.55)
    darksalmon           = (0.91, 0.59, 0.48)
    darkseagreen         = (0.56, 0.74, 0.56)
    darkslateblue        = (0.22, 0.29, 0.40)
    darkslategray        = (0.18, 0.31, 0.31)
    darkslategrey        = (0.18, 0.31, 0.31)
    darkturquoise        = (0.00, 0.65, 0.65)
    darkviolet           = (0.58, 0.00, 0.83)
    deeppink             = (1.00, 0.08, 0.58)
    deepskyblue          = (0.00, 0.75, 1.00)
    dimgray              = (0.33, 0.33, 0.33)
    dimgrey              = (0.33, 0.33, 0.33)
    dodgerblue           = (0.12, 0.56, 1.00)
    firebrick            = (0.56, 0.14, 0.14)
    firebrick1           = (1.00, 0.19, 0.19)
    firebrick2           = (0.93, 0.17, 0.17)
    firebrick3           = (0.80, 0.15, 0.15)
    firebrick4           = (0.55, 0.10, 0.10)
    floralwhite          = (1.00, 0.98, 0.94)
    forestgreen          = (0.31, 0.62, 0.41)
    gainsboro            = (0.86, 0.86, 0.86)
    ghostwhite           = (0.97, 0.97, 1.00)
    gold                 = (0.85, 0.67, 0.00)
    gold1                = (1.00, 0.84, 0.00)
    gold2                = (0.93, 0.79, 0.00)
    gold3                = (0.80, 0.68, 0.00)
    gold4                = (0.55, 0.46, 0.00)
    goldenrod            = (0.94, 0.87, 0.52)
    goldenrod1           = (1.00, 0.76, 0.15)
    goldenrod2           = (0.93, 0.71, 0.13)
    goldenrod3           = (0.80, 0.61, 0.11)
    goldenrod4           = (0.55, 0.41, 0.08)
    green                = (0.00, 1.00, 0.00)
    green1               = (0.00, 1.00, 0.00)
    green2               = (0.00, 0.93, 0.00)
    green3               = (0.00, 0.80, 0.00)
    green4               = (0.00, 0.55, 0.00)
    greenyellow          = (0.68, 1.00, 0.18)
    honeydew             = (0.94, 1.00, 0.94)
    honeydew1            = (0.94, 1.00, 0.94)
    honeydew2            = (0.88, 0.93, 0.88)
    honeydew3            = (0.76, 0.80, 0.76)
    honeydew4            = (0.51, 0.55, 0.51)
    hotpink              = (1.00, 0.41, 0.71)
    indianred            = (0.42, 0.22, 0.22)
    ivory                = (1.00, 1.00, 0.94)
    ivory1               = (1.00, 1.00, 0.94)
    ivory2               = (0.93, 0.93, 0.88)
    ivory3               = (0.80, 0.80, 0.76)
    ivory4               = (0.55, 0.55, 0.51)
    khaki                = (0.70, 0.70, 0.49)
    khaki1               = (1.00, 0.96, 0.56)
    khaki2               = (0.93, 0.90, 0.52)
    khaki3               = (0.80, 0.78, 0.45)
    khaki4               = (0.55, 0.53, 0.31)
    lavender             = (0.90, 0.90, 0.98)
    lavenderblush        = (1.00, 0.94, 0.96)
    lawngreen            = (0.49, 0.99, 0.00)
    lemonchiffon         = (1.00, 0.98, 0.80)
    lightblue            = (0.69, 0.89, 1.00)
    lightcoral           = (0.94, 0.50, 0.50)
    lightcyan            = (0.88, 1.00, 1.00)
    lightgoldenrod       = (0.93, 0.87, 0.51)
    lightgoldenrodyellow = (0.98, 0.98, 0.82)
    lightgray            = (0.66, 0.66, 0.66)
    lightgrey            = (0.66, 0.66, 0.66)
    lightpink            = (1.00, 0.71, 0.76)
    lightsalmon          = (1.00, 0.63, 0.48)
    lightseagreen        = (0.13, 0.70, 0.67)
    lightskyblue         = (0.53, 0.81, 0.98)
    lightslateblue       = (0.52, 0.44, 1.00)
    lightslategray       = (0.47, 0.53, 0.60)
    lightslategrey       = (0.47, 0.53, 0.60)
    lightsteelblue       = (0.49, 0.60, 0.83)
    lightyellow          = (1.00, 1.00, 0.88)
    limegreen            = (0.00, 0.69, 0.08)
    linen                = (0.98, 0.94, 0.90)
    magenta              = (1.00, 0.00, 1.00)
    magenta1             = (1.00, 0.00, 1.00)
    magenta2             = (0.93, 0.00, 0.93)
    magenta3             = (0.80, 0.00, 0.80)
    magenta4             = (0.55, 0.00, 0.55)
    maroon               = (0.56, 0.00, 0.32)
    maroon1              = (1.00, 0.20, 0.70)
    maroon2              = (0.93, 0.19, 0.65)
    maroon3              = (0.80, 0.16, 0.56)
    maroon4              = (0.55, 0.11, 0.38)
    mediumaquamarine     = (0.00, 0.58, 0.56)
    mediumblue           = (0.20, 0.20, 0.80)
    mediumforestgreen    = (0.20, 0.51, 0.29)
    mediumgoldenrod      = (0.82, 0.76, 0.40)
    mediumorchid         = (0.74, 0.32, 0.74)
    mediumpurple         = (0.58, 0.44, 0.86)
    mediumseagreen       = (0.20, 0.47, 0.40)
    mediumslateblue      = (0.42, 0.42, 0.55)
    mediumspringgreen    = (0.14, 0.56, 0.14)
    mediumturquoise      = (0.00, 0.82, 0.82)
    mediumvioletred      = (0.84, 0.13, 0.47)
    midnightblue         = (0.18, 0.18, 0.39)
    mintcream            = (0.96, 1.00, 0.98)
    mistyrose            = (1.00, 0.89, 0.88)
    moccasin             = (1.00, 0.89, 0.71)
    navajowhite          = (1.00, 0.87, 0.68)
    navy                 = (0.14, 0.14, 0.46)
    navyblue             = (0.14, 0.14, 0.46)
    oldlace              = (0.99, 0.96, 0.90)
    olivedrab            = (0.42, 0.56, 0.14)
    orange               = (1.00, 0.53, 0.00)
    orange1              = (1.00, 0.65, 0.00)
    orange2              = (0.93, 0.60, 0.00)
    orange3              = (0.80, 0.52, 0.00)
    orange4              = (0.55, 0.35, 0.00)
    orangered            = (1.00, 0.27, 0.00)
    orchid               = (0.94, 0.52, 0.94)
    orchid1              = (1.00, 0.51, 0.98)
    orchid2              = (0.93, 0.48, 0.91)
    orchid3              = (0.80, 0.41, 0.79)
    orchid4              = (0.55, 0.28, 0.54)
    palegoldenrod        = (0.93, 0.91, 0.67)
    palegreen            = (0.45, 0.87, 0.47)
    paleturquoise        = (0.69, 0.93, 0.93)
    palevioletred        = (0.86, 0.44, 0.58)
    papayawhip           = (1.00, 0.94, 0.84)
    peachpuff            = (1.00, 0.85, 0.73)
    peru                 = (0.80, 0.52, 0.25)
    pink                 = (1.00, 0.71, 0.77)
    pink1                = (1.00, 0.71, 0.77)
    pink2                = (0.93, 0.66, 0.72)
    pink3                = (0.80, 0.57, 0.62)
    pink4                = (0.55, 0.39, 0.42)
    plum                 = (0.77, 0.28, 0.61)
    plum1                = (1.00, 0.73, 1.00)
    plum2                = (0.93, 0.68, 0.93)
    plum3                = (0.80, 0.59, 0.80)
    plum4                = (0.55, 0.40, 0.55)
    powderblue           = (0.69, 0.88, 0.90)
    purple               = (0.63, 0.13, 0.94)
    purple1              = (0.61, 0.19, 1.00)
    purple2              = (0.57, 0.17, 0.93)
    purple3              = (0.49, 0.15, 0.80)
    purple4              = (0.33, 0.10, 0.55)
    red                  = (1.00, 0.00, 0.00)
    red1                 = (1.00, 0.00, 0.00)
    red2                 = (0.93, 0.00, 0.00)
    red3                 = (0.80, 0.00, 0.00)
    red4                 = (0.55, 0.00, 0.00)
    rosybrown            = (0.74, 0.56, 0.56)
    royalblue            = (0.25, 0.41, 0.88)
    saddlebrown          = (0.55, 0.27, 0.07)
    salmon               = (0.91, 0.59, 0.48)
    salmon1              = (1.00, 0.55, 0.41)
    salmon2              = (0.93, 0.51, 0.38)
    salmon3              = (0.80, 0.44, 0.33)
    salmon4              = (0.55, 0.30, 0.22)
    sandybrown           = (0.96, 0.64, 0.38)
    seagreen             = (0.32, 0.58, 0.52)
    seashell             = (1.00, 0.96, 0.93)
    seashell1            = (1.00, 0.96, 0.93)
    seashell2            = (0.93, 0.90, 0.87)
    seashell3            = (0.80, 0.77, 0.75)
    seashell4            = (0.55, 0.53, 0.51)
    sienna               = (0.59, 0.32, 0.18)
    sienna1              = (1.00, 0.51, 0.28)
    sienna2              = (0.93, 0.47, 0.26)
    sienna3              = (0.80, 0.41, 0.22)
    sienna4              = (0.55, 0.28, 0.15)
    skyblue              = (0.45, 0.62, 1.00)
    slateblue            = (0.49, 0.53, 0.67)
    slategray            = (0.44, 0.50, 0.56)
    slategrey            = (0.44, 0.50, 0.56)
    snow                 = (1.00, 0.98, 0.98)
    snow1                = (1.00, 0.98, 0.98)
    snow2                = (0.93, 0.91, 0.91)
    snow3                = (0.80, 0.79, 0.79)
    snow4                = (0.55, 0.54, 0.54)
    springgreen          = (0.25, 0.67, 0.25)
    steelblue            = (0.33, 0.44, 0.67)
    tan                  = (0.87, 0.72, 0.53)
    tan1                 = (1.00, 0.65, 0.31)
    tan2                 = (0.93, 0.60, 0.29)
    tan3                 = (0.80, 0.52, 0.25)
    tan4                 = (0.55, 0.35, 0.17)
    thistle              = (0.85, 0.75, 0.85)
    thistle1             = (1.00, 0.88, 1.00)
    thistle2             = (0.93, 0.82, 0.93)
    thistle3             = (0.80, 0.71, 0.80)
    thistle4             = (0.55, 0.48, 0.55)
    tomato               = (1.00, 0.39, 0.28)
    tomato1              = (1.00, 0.39, 0.28)
    tomato2              = (0.93, 0.36, 0.26)
    tomato3              = (0.80, 0.31, 0.22)
    tomato4              = (0.55, 0.21, 0.15)
    transparent          = (0.00, 0.00, 0.00)
    turquoise            = (0.10, 0.80, 0.87)
    turquoise1           = (0.00, 0.96, 1.00)
    turquoise2           = (0.00, 0.90, 0.93)
    turquoise3           = (0.00, 0.77, 0.80)
    turquoise4           = (0.00, 0.53, 0.55)
    violet               = (0.61, 0.24, 0.81)
    violetred            = (0.95, 0.24, 0.59)
    wheat                = (0.96, 0.87, 0.70)
    wheat1               = (1.00, 0.91, 0.73)
    wheat2               = (0.93, 0.85, 0.68)
    wheat3               = (0.80, 0.73, 0.59)
    wheat4               = (0.55, 0.49, 0.40)
    white                = (1.00, 1.00, 1.00)
    whitesmoke           = (0.96, 0.96, 0.96)
    yellow               = (1.00, 1.00, 0.00)
    yellow1              = (1.00, 1.00, 0.00)
    yellow2              = (0.93, 0.93, 0.00)
    yellow3              = (0.80, 0.80, 0.00)
    yellow4              = (0.55, 0.55, 0.00)
    yellowgreen          = (0.20, 0.85, 0.22)
'''[1:-1]
for line in data.split("\n"):
    name, t = [i.strip() for i in line.split("=")]
    r, g, b = [int(255*i) for i in eval(t)]
    # Provide output for a python dictionary initialization
    print(f'{" "*12}"{name}": ({r}, {g}, {b}),')
