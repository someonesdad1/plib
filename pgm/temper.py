'''
Adapted from
http://www.myvirtualnetwork.com/mklotz/fckeditor/UserFiles/File/data.zip
'''
from wrap import dedent
from f import flt
def Tempering():
    tempering_colors = (
        # Color, degF, uses
        ("Faint yellow",      420, "Knives, hammers"),
        ("Very pale yellow",  430, "Reamers"),
        ("Light yellow",      440, "Lathe tools, scrapers, milling cutters, reamers"),
        ("Pale straw yellow", 450, "Twist drills for hard use"),
        ("Straw yellow",      460, "Dies, punches, bits, reamers"),
        ("Deep straw yellow", 470, ""),
        ("Dark yellow",       480, "Twist drills, large taps"),
        ("Yellow brown",      490, ""),
        ("Brown yellow",      500, "Axes, wood chisels, drifts, taps >= 1/2\", dies"),
        ("Spotted red brown", 510, ""),
        ("Brown purple",      520, "Taps <= 1/4\""),
        ("Light purple",      530, ""),
        ("Full purple",       540, "Cold chisels, center punches"),
        ("Dark purple",       550, ""),
        ("Full blue",         560, "Screwdrivers, springs, gears"),
        ("Dark blue",         570, ""),
        ("Medium blue",       600, "Scrapers, spokeshaves"),
        ("Light blue",        640, "")
    )
    s = " "*10
    print(dedent('''
            Tempering Colors
            ----------------
         Color         °F     °C            Uses
    ----------------  -----  ------  --------------------'''))
    for name, degf, use in tempering_colors:
        degc = int((degf - 32)/1.8 + 0.5)
        print(f"{name:18s} {degf}{' '*5}{degc}   {use}")
def HeatColors():
    heat_colors = (
        # Name, degF
        ("Red - visible at night",    750),
        ("Red - visible at twilight", 885),
        ("Red - visible in daylight", 975),
        ("Red - visible in sunlight", 1075),
        ("Dark red",                  1290),
        ("Dull cherry red",           1475),
        ("Cherry red",                1650),
        ("Bright cherry red",         1830),
        ("Orange red",                2010),
        ("Orange yellow",             2190),
        ("Yellow white",              2370),
        ("White",                     2550),
        ("Brilliant white",           2730),
        ("Blue white",                2900),
        ("Acetylene flame",           4080),
        ("Induction furnace",         5450),
        ("Electric arc light",        7200)
    )
    print(dedent('''
            Incandescent Colors
            -------------------
                 Color               °F     °C
        -------------------------   -----  -----'''))
    for color, degf in heat_colors:
        c = flt((degf - 32)/1.8 + 0.5)
        with c:
            if c < 1000:
                c.N = 2
            else:
                c.N = 3
            print(f"{color:28s} {degf!s:4s}   {c!s:4s}")
if __name__ == "__main__":  
    x = flt(0)
    x.N = 3
    x.rtdp = x.rtz = True
    Tempering()
    print()
    HeatColors()
