import wl2rgb
import color
from color import Color, t
from wrap import dedent
from bidict import bidict
from dpprint import PP
import termtables as tt
pp = PP()   # Get pprint with current screen width

def Introduction(quiet=False):
    if not quiet:
        print(dedent('''
        
        This script shows the Feb 2026 development of the short color names I use.  In
        May 2022 I developed a set of color names motivated by the resistor color code
        names.  I've come to like the brevity of the names and the set of names I use
        covers my needs adequately.
        
        A rule is that the name used should tend to make me think of the color.  This
        works fine for red, orn, yel, grn, blu, vio.  cyn and mag are easy too because
        they've been used in numerous color name sets.  ord, yon, and ygr are discussed
        below.  lwn was for "lawn", sea for "sea green", trq for turquoise, sky for
        approximately the color of a blue sky, den for denim, roy for royal blue, lav
        for lavender, pnk for pink, and lip for lipstick.
        
        The 2022 method used e.g. yel for yellow, yell for "light yellow", yeld for
        "dark yellow", and yelb for "bright yellow".  I virtually never used the d and b
        forms and most usage was probably with the l form.  I felt it was time to update
        the set of names.
        
        I'm concurrently working on a new class Trm which will be how my python scripts
        produce color output to the terminal and the new Trm class will be a subclass of
        dict, making it easy to keep sets of names around as needed and switching
        between them.
        
        My first step was to print out the various colors using HLS coordinates with
        0xff for hue, 0x7f for lightness, and 0xff for saturation.  I used steps of 5 in
        the hue parameter (wl is wavelength in nm).  I then assigned the names based on
        the appearance of the colors on my monitor's black background.  New names are
        'ord' for orange-red, 'yon' for yellow-orange, and 'ygr' for yellow-green.
        https://hypertextbook.com/facts/2007/SusanZhao.shtml states that the maximum
        sensitivity of the human eye is around 560 nm; I picked 555 nm for ygr and it is
        the color I now use for the cursor in my terminal, as it's the easiest to find
        on the screen.  I mentally think of it as Igor in the Discworld series.
        
        '''))
        print()
    di = bidict({
        "red": 0,
        "ord": 10,
        "orn": 20,
        "yon": 30,
        "yel": 40,
        "ygr": 55,
        "lwn": 70,
        "grn": 85,
        "sea": 105,
        "trq": 115,
        "cyn": 125,
        "sky": 135,
        "den": 145,
        "roy": 155,
        "blu": 170,
        "vio": 190,
        "lav": 200,
        "mag": 215,
        "pnk": 225,
        "lip": 235,
    })
    if not quiet:
        # Print by hex hue in steps of 5, giving 52 colors
        t.print(f'''{t(attr='ul')}Hue        HLS     RGV     HSV   wl   Name''')
        idi = di.invert()
        for h in range(0, 256, 5):
            c = Color(h, 0x7f, 0xff, hls=True)
            s = idi[h] if h in idi else ""
            t.print(f"{h:3d} "
                    f"0x{h:02x} "
                    f"{t(c)}{c.xhls} {c.xrgb} {c.xhsv} "
                    f"{wl2rgb.rgb2wl(c)}{t.n}   "
                    f"{s} "
                )
        print()
        print(dedent('''
        
        This is the first pass at naming; these names refer to a specific hue at a lightness
        of 0x7f and full saturation at 0xff.  The next step was to use integer modifiers of
        1, 2, 3 to designate colors with the same hue but darker:  0x60, 0x40, and 0x20
        because 0x7f is about 0x80, so the steps are 0x20.  Adding an l would lighten the
        hue to 0xc0.
            
        '''))
        print()
        # di:  "blu": 170, idi:  0: "red"
        print("Hue  Clr")
    s = " "*2
    # We'll put the names into the dict D:  "name": Color instance
    D = {}
    for name in di:
        h = di[name]
        a, b, c, d, e = name, name + "1", name + "2", name + "3", name + "l"
        D[a] = Color(h, 0x7f, 0xff, hls=True)
        D[b] = Color(h, 0x60, 0xff, hls=True)
        D[c] = Color(h, 0x40, 0xff, hls=True)
        D[d] = Color(h, 0x20, 0xff, hls=True)
        D[e] = Color(h, 0xc0, 0xff, hls=True)
        t.a = t(D[a])
        t.b = t(D[b])
        t.c = t(D[c])
        t.d = t(D[d])
        t.e = t(D[e])
        if not quiet:
            t.print(f"{t.a}{h:3d}{s}"
                    f"{a:3s}{s}"
                    f"{t.b}{b:4s}{s}"
                    f"{t.c}{c:4s}{s}"
                    f"{t.d}{d:4s}{s}"
                    f"{t.e}{e:4s}{s}"
                )
    if not quiet:
        print("      7f   60    40    20    c0")
        print("where the last number is the hex lightness in the HLS")
        print()
        print(dedent('''
        
        Assessment:  These are pretty good for a first pass; the 3-letter names look fairly
        close to my first set of choices in 2023 on my monitor with a black background.
        Some names from the 2022 set that are lacking are blk (black), brn (brown), gry
        (gray), wht (white), lil (lilac), pur (purple), and olv (olive).
        
        '''))
    # Add in some missing names.  Rename D to d.
    def A(name, hex, h=False):
        if h:
            D[name] = Color(hex, hls=True)
        else:
            D[name] = Color(hex)
    if 1:   # Black
        # Black is special, as all lightnesses are black
        A("blk", "#000000")
        A("blk1", "#000000")
        A("blk2", "#000000")
        A("blk3", "#000000")
        A("blkl", "#000000")
    if 1:   # Brown
        A("brnl", "$17a065")
        A("brn",  "$158065")
        A("brn1", "$156065")
        A("brn2", "$154065")
        A("brn3", "$152065")
    if 1:   # Gray
        A("gry",  "$004800")
        A("gry1", "$003800")
        A("gry2", "$003000")
        A("gry3", "$002000")
        A("gryl", "$005800")
    if 1:   # White
        A("wht",  "$00b500")
        A("wht1", "$009500")
        A("wht2", "$007500")
        A("wht3", "$006500")
        A("whtl", "$00ff00")
    if 1:   # Lilac
        A("lil",  "$baa030")
        A("lil1", "$ba8030")
        A("lil2", "$ba6030")
        A("lil3", "$ba4030")
        A("lill", "$bac060")
    if 1:   # Purple
        A("pur",  "$c580a0")
        A("pur1", "$c565a0")
        A("pur2", "$c550a0")
        A("pur3", "$c535a0")
        A("purl", "$c5b0d0")
    if 1:   # Olive
        A("olv",  "$38609a")
        A("olv1", "$38489a")
        A("olv2", "$38369a")
        A("olv3", "$38209a")
        A("olvl", "$38b09a")
    if 0:
        # Use this section to tune a base color
        #c = Color("#759a26")
        #print(c.xhls)
        s = "olv"
        a=s+"l";print(a, D[a], D[a].xhls)
        a=s;print(a + " ", D[a], D[a].xhls)
        a=s+"1";print(a, D[a], D[a].xhls)
        a=s+"2";print(a, D[a], D[a].xhls)
        a=s+"3";print(a, D[a], D[a].xhls)
        exit()
    if 1:   # Print out the colors
        for i in '''
                blu roy den sky cyn 
                trq sea grn lwn olv 
                yel ygr yon orn ord brn
                mag pnk lil lav pur lip red
                '''.split():
            s = i + "l"; c = D[s]; t.print(f"{t(c)}{s:4s}: {c}")
            s = i + "";  c = D[s]; t.print(f"{t(c)}{s:4s}: {c}")
            s = i + "1"; c = D[s]; t.print(f"{t(c)}{s:4s}: {c}")
            s = i + "2"; c = D[s]; t.print(f"{t(c)}{s:4s}: {c}")
            s = i + "3"; c = D[s]; t.print(f"{t(c)}{s:4s}: {c}")
    return D
def CompareNewOld():
    'Print a table showing the new and old'
    output = []  # List for output strings
    # Get the 3 letter names
    for num, s in enumerate(sorted(i for i in d if len(i) == 3)):
        row = []
        row.append(str(num))
        row.append(s)   # Name in plain text white
        row.append(f"{t(d[s])}{s}{t.n}")       
        for i in "123l":
            u = d[s + i]
            row.append(f"{t(u)}{s + i}{t.n}")
        row.append("|")   # Separator
        # Old color names
        try:
            c = eval(f"t.{s}")
            row.append(f"{c}{s}{t.n}")
            for i in "ldb":
                u = eval(f"t.{s + i}")
                c = eval(f"t.{s}")
                row.append(f"{u}{s + i}{t.n}")
        except AttributeError:
            row.extend([""]*4)
        output.append(row)
    n = len(output[0])
    header = "Num Clr Nom 1 2 3 l | Old l d b".split()
    tt.print(output, header=header, padding=(1, 1), style=" "*15, alignment="c"*n)
def Assessment():
    print()
    print(dedent('''

    There are 5*26 + 1 or 131 colors.  This is roughly half of the 8-bit colors, so I'm
    assuming that there will be a pretty good matching (see below), meaning these names
    will work with either 8-bit or 24-bit colors.  Three new color names have been added
    over the old and the gradations by adding 1, 2, 3, and l to the name are more
    convenient and nicely spaced.  

    A handy addition to either Trm or Color would be methods that allow adjusting hue,
    lightness, and saturation up and down.  I could see the argument being a float on 
    [-10, 10], representing a percentage adjustment down or up.  1 represents 10%,
    probably a typical choice for an adjustment, as finer adjustments could be hard to
    see unless the colors are compared in two blocks next to each other.

    '''))
def CompareTo8bit():
    print()
    print("Comparison with closest 8-bit colors ('name closest_8-bit_color):")
    output = []  # List for output strings
    for name in sorted(i for i in d if len(i) == 3):
        if name == "blk":
            continue
        row = ["  "]
        c = d[name]
        row.append(f"{t(c)}{name}{t.n}")       
        n = color.RGBtoANSI8bit(*c.irgb)
        c1 = color.Translate8bit(n)
        row.append(f" {t(c1)}8bit{t.n}")       
        for ltr in "123l":
            row.append(" "*4)
            newname = name + ltr
            c = d[newname]
            row.append(f"{t(c)}{newname}{t.n}")       
            n = color.RGBtoANSI8bit(*c.irgb)
            c1 = color.Translate8bit(n)
            row.append(f" {t(c1)}8bit{t.n}")       
        print(''.join(row))
    exit()

    n = len(output[0])
    header = "Num Clr Nom 1 2 3 l | Old l d b".split()
    print()
    tt.print(output, header=header, padding=(1, 1), style=" "*15, alignment="c"*n)
    

if __name__ == "__main__":  
    d = Introduction(quiet=1)
    CompareNewOld()
    Assessment()
    CompareTo8bit()
