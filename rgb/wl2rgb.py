'''
Provides the function wl2rgb to convert a light wavelength in nm into an
approximate RGB color.
 
In units of nm, here are the approximate color divisions:
    violet      380-450
    blue        450-495
    green       495-570
    yellow      570-590
    orange      590-620
    red         620-780
 
Observations
    - Monitors can't reproduce what our eyes are capable of seeing.  In the
      1960's, I remember adjusting a Fabry-Perot interferometer that was
      looking at a sodium lamp in a dark room.  I remember being surprised
      by seeing the orange sodium doublet concentric rings and realizing I
      could see that they were different shades of orange.  
 
'''
import sys
from rgb import ColorNum
from util import Distribute
from pdb import set_trace as xx 
if 1:
    import debug
    debug.SetDebugger()
 
def wl2rgb(nm, gamma=0.8):
    '''Convert nm (light wavelength in nm) into a ColorNum object using a
    linear approximation.  The ColorNum object represents an RGB color.
    gamma is used for a gamma adjustment.  nm must be on [380, 780].
    '''
    # Translation of Dan Bruton's FORTRAN code from
    # http://www.physics.sfasu.edu/astro/color/spectra.html into python.
    # Also see http://www.midnightkite.com/color.html.
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
        b = [(i*j)**gamma for j in a]
    # Make sure the numbers are on [0, 1]
    assert(all([0 <= i <=1 for i in b]))
    return ColorNum(b)

if __name__ == "__main__": 
    from clr import Clr
    from wrap import dedent
    from columnize import Columnize
    from frange import frange
    import colorsys
    c = Clr(override=True)
    f = lambda x: f"({x[0]:3d}, {x[1]:3d}, {x[2]:3d})"
    def Introduction():
        print(dedent(f'''
 
        This script details my thinking on coming up with a set of color
        names for my own use.  My impression from collecting samples of
        color names over the years (see rgbdata.py) is that there are way
        too many names.  Part of this comes from commercial paint companies
        defining many colors for their products.  This is understandable,
        considering the fickleness of many consumers.  However, for use on
        a color monitor (which is my only interest), having on the order of
        ten thousand names is overkill.
 
        Take a look at the following printout, which shows 256 different 
        colors with nominal 1 nm steps in wavelength.
 
        '''))
        SteppedWavelengths(1, compact=True)
        print(dedent(f'''
 
        It's overkill on my monitor because I can't see color differences
        like I can with real light.  I know from using a Fabry-Perot
        interferometer on sodium light that you can see the color
        difference between the two lines in the sodium doublet, which
        differ by 0.6 nm in wavelength.  The wavelength to RGB function
        produces (255, 226, 0) for 589 mm and (255, 223, 0) for 590 mm.
        These colors are indistinguishable on my monitor from a normal
        viewing distance.  With a 10X loupe, I may or may not see
        differences in the small red, green, and blue elements making up
        each pixel.  Since there are over 7 pixels per mm, each pixel's
        red, green, or blue bar is on the order of 50 μm wide.  An
        interesting test is to print the Unicode character U+25A0 out in
        the the colors used in the above text table, as they then butt up
        nearly next to each other.  Here are these characters printed out
        (in 1 nm wavelength steps):
 
        '''))
        s = "■"
        for nm in range(380, 781):
            a = wl2rgb(nm)
            print(f"{c(a.rgbhex)}{s}{c.n}", end="")
        print()
    def SteppedWavelengths(step, compact=False):
        gamma = 0.8
        print(dedent(f'''
        Wavelength in steps of {step} nm to RGB colors (gamma = {gamma})
        Uses Bruton's linear approximation to convert light wavelength in
        nm to an approximating RGB 3-tuple:
        '''))
        out, count = [], 0
        if not compact:
            print(f"  wl in nm, RGB hex, RGB integer, HSV integer")
        for nm in range(380, 781, step):
            colornum = wl2rgb(nm, gamma=gamma)
            s = colornum.rgbhex
            t = colornum.RGB
            u = colornum.HSV
            if compact:
                out.append(f"{c(s)}{nm}{c.n}")
            else:
                out.append(f"{c(s)}{nm} {s!s:7s}   {f(t)}   {f(u)}{c.n}")
            count += 1
        if compact:
            o = Columnize(out, indent=" "*2)
        else:
            o = out
        for line in o:
            print(line)
        print(f"{count} wavelengths printed")
    def BasicColorNames():
        print(dedent(f'''
 
        This led to me subjectively defining some basic color names in terms
        of wavelength.  The corresponding RGB values are converted to HSV
        and the color is printed as (hue, 1, 1) where the numbers are on
        [0, 1].  We'll use EIA color abbreviations used in the color code
        for resistors.
 
        '''))
        defs = (    # Map name to wavelength (in nm) and hue (on [0, 255])
            ("vio", 400, 200),
            ("blu", 440, 170),
            ("cyn", 490, 127),
            ("grn", 510,  85),
            ("yel", 580,  42),
            ("orn", 618,  21),
            ("red", 646,   0),
        )
        print("    Name  nm  Hue  RGBhex        RGBint            HSVint")
        for name, nm, hue in defs:
            hsv = [i/255 for i in (hue, 255, 255)]
            rgb = colorsys.hsv_to_rgb(*hsv)
            colornum = ColorNum(rgb)
            s = colornum.rgbhex
            t = colornum.RGB
            u = colornum.HSV
            print(f"    {c(s)}{name:4s} {nm:3d}  {hue:3d} {s!s:7s}   {f(t)}   {f(u)}{c.n}")
        print(dedent(f'''
 
        These look like a good basis, although they don't appear to be the
        same brightness to my eyes.  On my monitor, cyan, green and yellow
        are perceived as the brightest.  Violet, orange, and red are a bit
        dimmer but about the same brightness amongst themselves.  Blue is
        the dimmest of the colors.
 
        '''.rstrip()))
    def Thoughts1():
        print(dedent(f'''
 
        Starting from these names, I'd like color names to have no spaces
        in them (separate word components with the underscore character)
        and be as short as practical.  If you look at the names in
        rgbdata.py, they range in length from 3 to 41 characters with
        statistics of:  mean of 9.4, median of 9.0, mode of 6.0, and
        standard deviation of 3.7 characters.  This leads me to want all
        names to be less than about the median plus two standard
        deviations, which I'd call about 16 characters.  Hence, my decision
        is that all names should be 15 characters or less.
 
        The next step is to look at sets of colors centered around each of
        these hues.  The goal is to decide on a suitable hue step for the
        interval.
 
        '''.rstrip()))
    def HueIntervals():
        print(dedent('''
 
        Define color intervals in terms of wavelength in nm.  The step
        increment was picked by examining the screen output.  The goal was
        to get three colors of each "band" that grade into the colors next
        to them (I will call them bands instead of using the term
        "primary", as that usually means something else to folks in the
        context of color).  The strings are the primary's 3-letter name with
        the wavelength in nm.
 
        '''))
        n = 14
        colors = [
            ("vio", range(380, 425 + 1, n + 2)),
            ("blu", range(425, 465 + 1, n)),
            ("cyn", range(465, 495 + 1, n)),
            ("grn", range(495, 540 + 1, n + 2)),
            ("yel", range(540, 600 + 1, n + 11)),
            ("orn", range(600, 632 + 1, n)),
            ("red", range(632, 780 + 1, 3*n + 8)),
        ]
        for color, wavelengths in colors:
            for nm in wavelengths:
                colornum = wl2rgb(nm)
                s = colornum.rgbhex
                print(f"    {c(s)}{color}{nm}{c.n} ", end="")
            print()
        print(dedent('''
 
        Comments:  I like the distribution.  The middle value of each color
        is the nominal center color; either side of that is one that is
        gradated towards the next band's color.  For example, the three
        yellow colors look like a greenish-yellow, normal yellow, and an
        orangish-yellow.  The orangish-yellow is visually distinct from the
        yellowish-orange.  This gives 21 hues to use.
 
        The beginning letter of each band color name uniquely identifies
        the color band.  Thus, we could let the color name be the leading
        letter and the wavelength in nm.  Here's what what such a list
        would look like after slight tuning after seeing what it looked
        like:
 
        '''))
        count, indent = 0, " "*4
        print(indent, end="")
        for name in '''v380 v396 v412
                       b425 b439 b453
                       c465 c479 c490
                       g500 g520 g540
                       y550 y565 y590
                       o600 o614 o628
                       r632 r682 r732'''.split():
            colornum = GetBaseColornum(name)
            s = colornum.rgbhex
            print(f"{c(s)}{name}{c.n} ", end="")
            count += 1
            if count and not (count % 9):
                print()
                print(indent, end="")
        print()
    def GetBaseColornum(name):
        nm = int(name[1:4])
        return wl2rgb(nm)
    def HueGradations():
        def ShowHLS(k, use_hex=False):
            R = Distribute(0, 255, k + 1)   # Count 0 as one we don't want
            if R[0] == 0:
                R = R[1:]   # Remove the first element of 0
            indent = " "*4
            for base in "g500 g520 g540".split():
                cn = GetBaseColornum(base)
                s = cn.rgbhex
                print(f"{c(s)}{base}{c.n}")
                hls = list(cn.hls)
                for l in R:
                    if l == 255:
                        continue
                    print(indent, end="")
                    hls[1] = l/255
                    rgb = colorsys.hls_to_rgb(*hls)
                    n = ColorNum(rgb)
                    hls1 = list(n.hls)
                    for s in R:
                        li = R.index(l)
                        si = R.index(s)
                        hls1[2] = s/255
                        rgb = colorsys.hls_to_rgb(*hls1)
                        m = ColorNum(rgb)
                        if use_hex:
                            print(f"{c(m.rgbhex)}{m.rgbhex}{c.n} ", end="")
                        else:
                            name = f"{base}_{li}{si}"
                            print(f"{c(m.rgbhex)}{name}{c.n} ", end="")
                    print()
                print()
        def ShowHSV(k, use_hex=False):
            R = Distribute(0, 255, k + 1)   # Count 0 as one we don't want
            if R[0] == 0:
                R = R[1:]   # Remove the first element of 0
            indent = " "*4
            for base in "g500 g520 g540".split():
                cn = GetBaseColornum(base)
                s = cn.rgbhex
                print(f"{c(s)}{base}{c.n}")
                hsv = list(cn.hsv)
                for s in R:
                    if s == 255:
                        continue
                    print(indent, end="")
                    hsv[1] = s/255
                    rgb = colorsys.hsv_to_rgb(*hsv)
                    n = ColorNum(rgb)
                    hsv1 = list(n.hsv)
                    for v in R:
                        si = R.index(s)
                        vi = R.index(v)
                        hsv1[2] = v/255
                        rgb = colorsys.hsv_to_rgb(*hsv1)
                        m = ColorNum(rgb)
                        if use_hex:
                            print(f"{c(m.rgbhex)}{m.rgbhex}{c.n} ", end="")
                        else:
                            name = f"{base}_{si}{vi}"
                            print(f"{c(m.rgbhex)}{name}{c.n} ", end="")
                    print()
                print()
        print(dedent('''
 
        The next task is to define the gradations of these 21 colors by
        e.g. varying lightness and saturation.  Let's experiment with the
        green colors first.  I lean towards a naming convention that allows
        each of these 21 colors to have 4 values of lightness and 4 values
        of saturation.  This would give us 21*4*4 or 336 colors.  Contrast
        this to the nearly 1000 colors in a typical XWindows rgb.txt file.
        The naming convention would be to use decimal numbers for the
        lightness and value step numbers starting with 1.  This would let
        you calculate the RGB components of the color from the name, which
        would be handy.
 
        '''))
        n = 4
        if 0:
            print("HLS by name")
            ShowHLS(n, use_hex=False)
        print("HLS by RGB hex value")
        ShowHLS(n, use_hex=True)
        if 0:
            print("HSV by name")
            ShowHSV(n, use_hex=False)
        print("HSV by RGB hex value")
        ShowHSV(n, use_hex=True)
        print(dedent('''
        The two methods give similar results.  Sorting the printed RGB
        values show that they use similar but not identical colors.  My
        preference is for the HLS set of colors, so that's the method I'd
        choose.

        '''))
    colorbands = '''v380 v396 v412 b425 b439 b453 c465 c479 c490 
                    g500 g520 g540 y550 y565 y590 o600 o614 o628
                    r632 r682 r732'''.split()
    def FirstChoice(n):
        print(dedent(f'''
        Here's a printout of a set of colors, selected as shown above by an
        algorithm.  I've chosen to use {n} levels of lightness and
        saturation.  The following will print out each color band color and
        its gradations.  This will make a candidate for a color set.  The
        hex number shown is HLS and the L value of 0xff is not used.

        '''))
        R = Distribute(0, 255, n + 1)   # The 1 is added to ignore zero
        if R[0] == 0:
            R = R[1:]   # Remove the first element of 0
        for name in colorbands:
            colornum = GetBaseColornum(name)
            hls = list(colornum.hls)
            s = colornum.rgbhex
            print(f"{c(s)}{name}{c.n} ", end="")
            for l in R:
                if l == 255:
                    continue
                hls[1] = l/255  # Convert to decimal
                rgb = colorsys.hls_to_rgb(*hls)
                n = ColorNum(rgb)
                hls1 = list(n.hls)
                for s in R:
                    li = R.index(l)
                    si = R.index(s)
                    hls1[2] = s/255
                    rgb = colorsys.hls_to_rgb(*hls1)
                    m = ColorNum(rgb)
                    print(f"{c(m.rgbhex)}{m.hlshex}{c.n} ", end="")
            print()
        print(dedent(f'''

        Missing from the set are the usual saturated colors of red, green,
        blue, yellow, cyan, magenta, bright white, and the shades of gray.
        Black also needs to be on the list.  Here are these:

        '''))
        d = {
            "blk": ColorNum((0, 0, 0)).hlshex,
            "lwht": ColorNum((1, 1, 1)).hlshex,
            "lblu": ColorNum((0, 0, 1)).hlshex,
            "lyel": ColorNum((1, 1, 0)).hlshex,
            "lcyn": ColorNum((0, 1, 1)).hlshex,
            "lmag": ColorNum((1, 0, 1)).hlshex,
        }
        print("  ", end="")
        for i in "blk lwht lblu lyel lcyn lmag".split():
            print(f"{c(i)}{i:7s}{c.n}", end=" ")
        print()
        for i in "blk lwht lblu lyel lcyn lmag".split():
            print(f"{c(i)}{d[i]}{c.n}", end=" ")
        print()
        ngray = 12
        print(dedent(f'''

        Remember '$' means an HLS value.  Here are {ngray} shades of gray
        in RGB hex notation:

        '''))
        count = 0
        for i in Distribute(0, 255, ngray):
            n = ColorNum([i/255 for i in (i, i, i)])
            count += 1
            if count == ngray//2 + 1:
                print()
            print(f"{c(n.rgbhex)}{n.rgbhex}{c.n} ", end="")
        print()
        n = 12*21 + ngray
        print(dedent(f'''

        These 12 grays could be added to a 'blk' color that's got the label
        of 'k000'.

        A fundamental feature of this naming scheme is that the names are
        all 7 characters long (the same as the #xxyyzz hex notation) and
        you can calculate the RGB values of the color from the name.

        Conclusions:  this isn't a bad set of colors.  The lblu, lyel,
        lcyn, and lmag colors aren't really needed, as there are ones in
        the table that are close enough.  The grays are needed and the
        brightest one can double as lwht.  There are {n} colors in this
        set.  

        '''))
    def SomeNames():
        print(dedent(f'''

        Invariably, someone will want to start giving names to colors.
        Here are some of my desires for such naming:

            - The color should be able to be computed from the name.
            - The name should be adequately close to the perceived color.
            - I'd want the names to be short.
            - Case should be irrelevant.
            - Spaces can be inserted if desired and they do.
            - Adjectives as words or abbreviations can be moved around in
              the name and it's still the same name.

        The three groups of four columns each can be labeled "dark",
        "medium", and "light".  The "medium" colors are really the 0x80
        level of lightness and these are probably colors that would get
        used pretty heavily, so the "medium" could be left off.  Then 'lt'
        and 'dk' could be used for light and dark to keep things short.

        Here's an attempt to come up with a set of short names:

        '''))
        d = {

            "v380": "  uv    ultvio     purple               ",
            "v396": "  vv    viovio     wine                 ",
            "v412": "  bv    bluvio     plum                 ",
            "b425": "  vb    vioblu     slate                ",
            "b439": "  bb    blublu     blue                 ",
            "b453": "  cb    cynblu     dodger               ",
            "c465": "  bc    blucyn     sky                  ",
            "c479": "  cc    cyncyn     cyan                 ",
            "c490": "  gc    grncyn     teal                 ",
            "g500": "  cg    cyngrn     aqua                 ",
            "g520": "  gg    grngrn     green                ",
            "g540": "  yg    yelgrn     lawn                 ",
            "y550": "  gy    grnyel     spring               ",
            "y565": "  yy    yelyel     yellow               ",
            "y590": "  oy    ornyel     wheat                ",
            "o600": "  yo    yelorn     gold                 ",
            "o614": "  oo    ornorn     orange               ",
            "o628": "  ro    redorn     brick                ",
            "r632": "  or    ornred     tomato               ",
            "r682": "  rr    redred     red                  ",
            "r732": "  ir    infred     cherry               ",

        }
        indent = " "*4
        print(f"{indent}Band   Short  Longer     Named")
        for name in colorbands:
            colornum = GetBaseColornum(name)
            s = colornum.rgbhex
            print(f"{indent}{c(s)}{name}  {d[name]}{c.n} ")
        print(dedent(f'''

        One of the features of these names is that they are all six or less
        characters, consistent with on of the goals.  Part of the
        motivation for this was the 6 character hex specifications, which
        include a '@', '#', or '$' leader character identifying what the
        numbers represent (HSV, RGB, or HLS).

        These names are also pretty easy to make matches with a few
        characters.  For r732 I first used 'blood', which worked well but
        confused searches with the 'blu' elements.  I then chose 'cherry'
        as an alternate.  For the vv color, I liked 'grape', but it
        clashed with the first two letters of green, so other names like
        wine, jam, jelly, orchid, indigo, mauve, iris, etc.  Wine won over
        lilac because it was shorter and a typical red wine is darker than
        our lilac plants' blooms.

        Because these names are both subjective and preloaded in many
        minds, many folks will argue with my picks.  Yet remember the goal
        was a six letter or less name that would describe the color
        'adequately'.  My primary goal for this project was to come up with
        on the order of 2**8 colors that could be used for my day-to-day
        work.  Having 2**9 would be OK, but just a little large.  Another
        primary goal was to have names that exhibited regularity and
        predictability.  Once working on this project I realized it would
        be possible to calculate the color's RGB values from the name once
        the naming scheme was regularlized.  This is nice because I am
        often using a variety of color specifiers, such as names, hex
        strings, RGB, HSV, and HLS.  

        '''))
    if len(sys.argv) > 1:
        Introduction()
        SteppedWavelengths(25)
        BasicColorNames()
        Thoughts1()
        HueIntervals()
        HueGradations()
        FirstChoice(4)
    SomeNames()
