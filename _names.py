import wl2rgb
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
    d = D
    def D(name, hex):
        d[name] = Color(hex)
        d[name + "1"] = Color(hex)
        d[name + "2"] = Color(hex)
        d[name + "3"] = Color(hex)
        d[name + "l"] = Color(hex)
    D("brn", "#964a00")
    D("gry", "#646464")
    D("blk", "#000000")
    D("wht", "#b4b4b4")
    D("lil", "#b493ea")
    D("pur", "#7517a6")
    D("olv", "#759a26")
    return d
def Tweak(d):
    'Print a table showing the new and old'
    output = []  # List for output strings
    # Get the 3 letter names
    for s in sorted(i for i in d if len(i) == 3):
        o = []
        o.append(s)                     # Name in plain text white
        o.append(f"{t(d[s])}{s}{t.n}")       
        for i in "123l":
            u = d[s + i]
            o.append(f"{t(u)}{s + i}{t.n}")
        o.append("|")   # Separator
        # Old color names
        try:
            c = eval(f"t.{s}")
            o.append(f"{c}{s}{t.n}")
            for i in "ldb":
                u = eval(f"t.{s + i}")
                c = eval(f"t.{s}")
                o.append(f"{u}{s + i}{t.n}")
        except AttributeError:
            o.extend([""]*4)
        output.append(o)
    n = len(output[0])
    header = "Clr Nom 1 2 3 l | Old l d b".split()
    tt.print(output, header=header, padding=(1, 1), style=" "*15, alignment="c"*n)
    #tt.print(output)

if __name__ == "__main__":  
    d = Introduction(quiet=1)
    Tweak(d)
