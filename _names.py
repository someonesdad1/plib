import wl2rgb
from color import Color, t
from wrap import dedent
from bidict import bidict
from dpprint import PP
pp = PP()   # Get pprint with current screen width

def Introduction(dbg=False):
    if not dbg:
        print(dedent('''

        This script shows the Feb 2026 development of the short color names I use.  My
        old naming method used e.g. yel for yellow, yell for "light yellow", yeld for
        "dark yellow", and yelb for "bright yellow".  I virtually never used the d and b
        forms and most usage was probably with the l form.
        
        Thus, I wanted to rethink my naming scheme.  My first step was to print out the
        various colors in full lightness & saturation form in steps of 5 in the hue
        parameter (wl is wavelength in nm).  I then assigned the names based on how this
        printed out on my monitor's black background.  New names are 'ord' for
        orange-red, 'yon' for yellow-orange, and 'ygr' for yellow-green.
        https://hypertextbook.com/facts/2007/SusanZhao.shtml states that the maximum
        sensitivity of the human eye is around 560 nm; I picked 555 nm for ygr and it is
        the color I now use for the cursor in my terminal, as it's the easiest to find
        on the screen.

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
        "lil": 200,
        "mag": 215,
        "pnk": 225,
        "lip": 235,
    })
    if not dbg:     # Print by hex hue in steps of 5, giving 52 colors
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
    for i in di:
        h = di[i]
        t.c  = t(Color(h, 0x7f, 0xff, hls=True))
        t.cl = t(Color(h, 0xc0, 0xff, hls=True))
        t.c1 = t(Color(h, 0x60, 0xff, hls=True))
        t.c2 = t(Color(h, 0x40, 0xff, hls=True))
        t.c3 = t(Color(h, 0x20, 0xff, hls=True))
        t.print(f"{t.c}{h:3d}{s}"
                f"{i:3s}{s}"
                f"{t.c1}{i + '1':4s}{s}"
                f"{t.c2}{i + '2':4s}{s}"
                f"{t.c3}{i + '3':4s}{s}"
                f"{t.cl}{i + 'l':4s}{s}"
               )
    print("      7f   60    40    20    c0")
    print("where the last number is the hex lightness in the HLS")
    print()
    print(dedent('''
    Assessment:  These are fair for a first pass, but it's clear they will need tuning,
    as on my monitor with a black background, seal, trql, cynl, skyl, and denl all look
    pretty similar (skyl and denl look slightly different in hue).  magl and pnkl look 
    the same.
    '''))

if __name__ == "__main__":  
    Introduction(0)
