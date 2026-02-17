import wl2rgb
from color import Color, t
from wrap import dedent
from bidict import bidict
from dpprint import PP
pp = PP()   # Get pprint with current screen width

def Introduction(dbg=False):
    if not dbg:
        print(dedent('''
        This script shows the Feb 2026 development of the short color names I use.  My old
        naming method used e.g. yel for yellow, yell for "light yellow", yeld for "dark yellow",
        and yelb for "bright yellow".  I virtually never used the d and b forms and most usage
        was probably with the l form.
        
        Thus, I wanted to rethink my naming scheme.  My first step was to print out the various
        colors in full lightness & saturation form in steps of 5 in the hue parameter.  This
        resulted in the assignment of new two and three letter names to the various hues.
        '''))
        print()
    di = bidict({
        "red": 0,
        "or": 10,
        "orn": 20,
        "yo": 30,
        "yel": 40,
        "yg": 55,
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
        t.print(f'''{t(attr='ul')}Hue        HLS{' '*25}Name''')
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
    This is the first pass at naming; these names refer to a specific hue.  The next
    step was to use integer modifiers of 1, 2, 3 to designate colors with the same hue
    but darker.  Adding an l would lighten the hue.
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

if __name__ == "__main__":  
    Introduction(1)
