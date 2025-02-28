"""

This script worked when I used the clr.py stuff, but that script has disappeared (replaced by
color.py) and this script is no longer worth spending the time to translate between the
implementations.

---------------------------------------------------------------------------

Shows some thoughts about color naming
"""

import sys
import colorsys
from pdb import set_trace as xx

from util import iDistribute
from interpolate import LinearInterpFunction
from f import flt

# from rgb import ColorNum
from color import t, Color as ColorNum
from wrap import dedent
from columnize import Columnize
from frange import frange
from wl2rgb import wl2rgb, rgb2wl

if 0:
    import debug

    debug.SetDebugger()

ii = isinstance
fi = lambda x: f"({x[0]:3d}, {x[1]:3d}, {x[2]:3d})"
square = "■"


def Introduction():
    print(
        dedent(f"""

    This script details my thinking on coming up with a set of color names
    for my own use.  My impression from collecting samples of color names
    over the years (see rgbdata.py) is that there are way too many names.
    Part of this comes from commercial paint companies defining many colors
    for their products.  This is understandable, considering the fickleness
    of many consumers.  However, for use on a color monitor (which is my
    only interest), having on the order of ten thousand names is overkill.

    Take a look at the following printout, which shows 256 different 
    colors with nominal 1 nm steps in wavelength.

    """)
    )
    SteppedWavelengths(1, compact=True)
    print(
        dedent(f"""

    That's too fine a resolution.  How about 5 nm steps?

    """)
    )
    SteppedWavelengths(5, compact=True)
    print(
        dedent(f"""

    10 nm steps are better:

    """)
    )
    SteppedWavelengths(10, compact=True)
    print(
        dedent(f"""

    It's interesting to print the Unicode character U+25A0 out in the
    colors used in the above text table, as they then butt up nearly next
    to each other.  Here are these characters printed out in 5 nm
    wavelength steps:

    """)
    )
    PrintedLine(5)
    print(
        dedent(f"""

    Here are 10 nm steps:

    """)
    )
    PrintedLine(10)


def PrintedLine(step):
    for nm in range(380, 781, step):
        a = wl2rgb(nm)
        print(f"{t(a.xrgb)}{square}{t.n}", end="")
    print()


def SteppedWavelengths(step, compact=False, hdr=False):
    gamma = 0.8
    if hdr:
        print(
            dedent(f"""
        Wavelength in steps of {step} nm to RGB colors (gamma = {gamma})
        Uses Bruton's linear approximation to convert light wavelength in
        nm to an approximating RGB 3-tuple:
        """)
        )
    out, count = [], 0
    if not compact:
        print(f"  wl in nm, RGB hex, RGB integer, HSV integer")
    for nm in range(380, 781, step):
        colornum = wl2rgb(nm, gamma=gamma)
        s = colornum.xrgb
        T = colornum.irgb
        u = colornum.ihsv
        if compact:
            out.append(f"{t(s)}{nm}{t.n}")
        else:
            out.append(f"{t(s)}{nm} {s!s:7s}   {fi(T)}   {fi(u)}{t.n}")
        count += 1
    if compact:
        o = Columnize(out, indent=" " * 2, horiz=True)
    else:
        o = out
    for line in o:
        print(line)
    if hdr:
        print(f"{count} wavelengths printed")


def BasicColorNames():
    print(
        dedent(f"""

    This led to me subjectively defining some basic color names in terms
    of wavelength.  The corresponding RGB values are converted to HSV
    and the color is printed as (hue, 1, 1) where the numbers are on
    [0, 1].  We'll use EIA color abbreviations used in the color code
    for resistors.

    """)
    )
    defs = (  # Map name to wavelength (in nm) and hue (on [0, 255])
        ("vio", 400, 200),
        ("blu", 440, 170),
        ("cyn", 490, 127),
        ("grn", 510, 85),
        ("yel", 580, 42),
        ("orn", 618, 21),
        ("red", 646, 0),
    )
    print("    Name  nm  Hue  RGBhex        RGBint            HSVint")
    for name, nm, hue in defs:
        hsv = [i / 255 for i in (hue, 255, 255)]
        rgb = colorsys.hsv_to_rgb(*hsv)
        colornum = ColorNum(*rgb)
        s = colornum.xrgb
        T = colornum.irgb
        u = colornum.ihsv
        print(
            f"    {t(s)}{name:4s} {nm:3d}  {hue:3d} {s!s:7s}   {fi(T)}   {fi(u)}{t.n}"
        )
    print(
        dedent(
            f"""

    These look like a good basis, although they don't appear to be the same
    brightness to my eyes (this is a well-known phenomenon).  On my
    monitor, cyan, green and yellow are perceived as the brightest.
    Violet, orange, and red are a bit dimmer but about the same brightness
    amongst themselves.  Blue appears to be the dimmest of the colors.

    """.rstrip()
        )
    )


def Thoughts1():
    print(
        dedent(
            f"""

    Starting from these names, I'd like color names to have no spaces
    in them (separate word components with the underscore character)
    and be as short as practical.  If you look at the names in
    rgbdata.py, they range in length from 3 to 41 characters with
    statistics of:  mean of 9.4, median of 9.0, mode of 6.0, and
    standard deviation of 3.7 characters.  This leads me to want all
    names to be less than about the median plus two standard
    deviations, which I'd call about 16 characters.  Hence, I decided
    all names should be 15 characters or less.

    The next step is to look at sets of colors centered around each of
    these hues.  The goal is to decide on a suitable hue step for the
    interval.

    """.rstrip()
        )
    )


def HueIntervals():
    print(
        dedent("""

    Define color intervals in terms of wavelength in nm.  The step
    increment was picked by examining the screen output.  The goal was
    to get three colors of each "band" that grade into the colors next
    to them (I will call them bands instead of using the term
    "primary", as that usually means something else to folks in the
    context of color).  The strings are the primary's 3-letter name with
    the wavelength in nm.

    """)
    )
    n = 14
    colors = [
        ("vio", range(380, 425 + 1, n + 2)),
        ("blu", range(425, 465 + 1, n)),
        ("cyn", range(465, 495 + 1, n)),
        ("grn", range(495, 540 + 1, n + 2)),
        ("yel", range(540, 600 + 1, n + 11)),
        ("orn", range(600, 632 + 1, n)),
        ("red", range(632, 780 + 1, 3 * n + 8)),
    ]
    for color, wavelengths in colors:
        for nm in wavelengths:
            colornum = wl2rgb(nm)
            s = colornum.xrgb
            print(f"    {t(s)}{color}{nm}{t.n} ", end="")
        print()
    print(
        dedent("""

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

    """)
    )
    count, indent = 0, " " * 4
    print(indent, end="")
    for name in """v380 v396 v412
                    b425 b439 b453
                    c465 c479 c490
                    g500 g520 g540
                    y550 y565 y590
                    o600 o614 o628
                    r632 r682 r732""".split():
        colornum = GetBaseColornum(name)
        s = colornum.xrgb
        print(f"{t(s)}{name}{t.n} ", end="")
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
        R = list(iDistribute(k + 1, 0, 255))  # Count 0 as one we don't want
        if R[0] == 0:
            R = R[1:]  # Remove the first element of 0
        indent = " " * 4
        for base in "g500 g520 g540".split():
            cn = GetBaseColornum(base)
            s = cn.xrgb
            print(f"{t(s)}{base}{t.n}")
            hls = list(cn.ihls)
            for l in R:
                if l == 255:
                    continue
                print(indent, end="")
                hls[1] = l / 255
                rgb = colorsys.hls_to_rgb(*hls)
                n = ColorNum(*rgb)
                hls1 = list(n.ihls)
                for s in R:
                    li = R.index(l)
                    si = R.index(s)
                    hls1[2] = s / 255
                    rgb = colorsys.hls_to_rgb(*hls1)
                    m = ColorNum(*rgb)
                    if use_hex:
                        print(f"{t(m.xrgb)}{m.xrgb}{t.n} ", end="")
                    else:
                        name = f"{base}_{li}{si}"
                        print(f"{t(m.xrgb)}{name}{t.n} ", end="")
                print()
            print()

    def ShowHSV(k, use_hex=False):
        R = list(iDistribute(k + 1, 0, 255))  # Count 0 as one we don't want
        if R[0] == 0:
            R = R[1:]  # Remove the first element of 0
        indent = " " * 4
        for base in "g500 g520 g540".split():
            cn = GetBaseColornum(base)
            s = cn.xrgb
            print(f"{t(s)}{base}{t.n}")
            hsv = list(cn.ihsv)
            for s in R:
                if s == 255:
                    continue
                print(indent, end="")
                hsv[1] = s / 255
                rgb = colorsys.hsv_to_rgb(*hsv)
                n = ColorNum(*rgb)
                hsv1 = list(n.ihsv)
                for v in R:
                    si = R.index(s)
                    vi = R.index(v)
                    hsv1[2] = v / 255
                    rgb = colorsys.hsv_to_rgb(*hsv1)
                    m = ColorNum(*rgb)
                    if use_hex:
                        print(f"{t(m.xrgb)}{m.xrgb}{t.n} ", end="")
                    else:
                        name = f"{base}_{si}{vi}"
                        print(f"{t(m.xrgb)}{name}{t.n} ", end="")
                print()
            print()

    print(
        dedent("""

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

    """)
    )
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
    print(
        dedent(f"""

    {t.ornl}Bugs, so the previous stuff isn't printed.{t.n}

    The two methods give similar results.  Sorting the printed RGB
    values show that they use similar but not identical colors.  My
    preference is for the HLS set of colors, so that's the method I
    chose.

    """)
    )


colorbands = """v380 v396 v412 b425 b439 b453 c465 c479 c490 
                g500 g520 g540 y550 y565 y590 o600 o614 o628
                r632 r682 r732""".split()


def FirstChoice(n):
    print()
    print(
        dedent(f"""
    Here's a printout of a set of colors, selected as shown above by an
    algorithm.  I've chosen to use {n} levels of lightness and
    saturation.  The following will print out each color band color and
    its gradations.  This will make a candidate for a color set.  The
    hex number shown is HLS and the L value of 0xff is not used.

    """)
    )
    R = list(iDistribute(n + 1, 0, 255))  # The 1 is added to ignore zero
    if R[0] == 0:
        R = R[1:]  # Remove the first element of 0
    for name in colorbands:
        colornum = GetBaseColornum(name)
        hls = list(colornum.ihls)
        s = colornum.xrgb
        print(f"{t(s)}{name}{t.n} ", end="")
        for l in R:
            if l == 255:
                continue
            hls[1] = l / 255  # Convert to decimal
            rgb = colorsys.hls_to_rgb(*hls)
            n = ColorNum(*rgb)
            hls1 = list(n.ihls)
            for s in R:
                li = R.index(l)
                si = R.index(s)
                hls1[2] = s / 255
                rgb = colorsys.hls_to_rgb(*hls1)
                m = ColorNum(*rgb)
                print(f"{t(m.xrgb)}{m.xhls}{t.n} ", end="")
        print()
    print(
        dedent(f"""

    Missing from the set are the usual saturated colors of red, green,
    blue, yellow, cyan, magenta, bright white, and the shades of gray.
    Black also needs to be on the list.  Here are these:

    """)
    )
    d = {
        "blk": ColorNum(*(0, 0, 0)).xhls,
        "whtl": ColorNum(*(1, 1, 1)).xhls,
        "blul": ColorNum(*(0, 0, 1)).xhls,
        "yell": ColorNum(*(1, 1, 0)).xhls,
        "cynl": ColorNum(*(0, 1, 1)).xhls,
        "magl": ColorNum(*(1, 0, 1)).xhls,
    }
    print("  ", end="")
    for i in "blk whtl blul yell cynl magl".split():
        print(f"{t(i)}{i:7s}{t.n}", end=" ")
    print()
    for i in "blk whtl blul yell cynl magl".split():
        print(f"{t(i)}{d[i]}{t.n}", end=" ")
    print()
    ngray = 12
    print(
        dedent(f"""

    Remember '$' means an HLS value.  Here are {ngray} shades of gray
    in RGB hex notation:

    """)
    )
    count = 0
    for i in iDistribute(0, 255, ngray):
        n = ColorNum(*[i / 255 for i in (i, i, i)])
        count += 1
        if count == ngray // 2 + 1:
            print()
        print(f"{t(n.xrgb)}{n.xrgb}{t.n} ", end="")
    print()
    n = 12 * 21 + ngray
    print(
        dedent(f"""

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

    """)
    )


def SomeNames():
    print(
        dedent(f"""
    Invariably, someone will want to start giving names to colors.
    Here are some of my desires for such naming:

        - The color should be able to be computed from the name.
        - The name should be adequately close to the perceived color.
        - The names must be short.
        - Case should be irrelevant.
        - Spaces can be inserted if desired and they don't change the
          computed color since they are stripped out.
        - Adjectives as words or abbreviations can be moved around in the
          name and it's still the same name.

    The three groups of four columns each can be labeled "dark",
    "medium", and "light".  The "medium" colors are really the 0x80
    level of lightness and these are probably colors that would get
    used pretty heavily, so the "medium" could be left off.  Then 'lt'
    and 'dk' could be used for light and dark to keep things short.

    Here's an attempt to come up with a set of short names:

    """)
    )
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
    indent = " " * 4
    print(f"{indent}Band   Short  Longer     Named")
    for name in colorbands:
        colornum = GetBaseColornum(name)
        s = colornum.xrgb
        print(f"{indent}{t(s)}{name}  {d[name]}{t.n} ")
    print(
        dedent(f"""

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

    """)
    )


def HueVersusFrequency():
    print(
        dedent(f"""
    It's also convenient to have an inverse to the wl2rgb function by
    Bruton.  Here's a printout of the "frequency" and hue of
    wavelengths in nm in 10 nm steps:

    """)
    )
    flt(0).rtdp = True
    i = " " * 4
    use_color = True
    print(f"{i}Hue  'Hz'    nm")
    for nm in range(380, 781, 10):
        cn = wl2rgb(nm, 0)
        h, l, s = cn.HLS
        f = int(1e5 / nm)
        if use_color:  # Print in color
            cl = t(cn.xrgb)
            print(f"{i}{cl}{h:3d}{t.n}   {f:3d}   {nm:3d}")
        else:
            print(f"{i}{h:3d}   {f:3d}   {nm:3d}")
    print(
        dedent(f"""

    Frequency is int(1e5/nm) for wavelength nm in nm.  Note the hue
    ranges over only 0-212 for return values of wl2rgb().  Higher
    numbered hues are problematic since hues wrap around to red as they
    approach 255 from below.  This is a discontinuity we need to deal
    with.  Here are these higher hue numbers converted to their
    equivalent RGB values with lightness = 128 and saturation of 255:

    """)
    )
    for hue in range(200, 256, 5):
        hls = [i / 255 for i in (hue, 128, 255)]
        rgb = colorsys.hls_to_rgb(*hls)
        cn = ColorNum(*rgb)
        cl = t(cn.xrgb)
        print(f"{i}{t(cn.xrgb)}{hue:3d}{t.n}")
    print(
        dedent(f"""

    A plot of "frequency" versus hue is nonlinear, so I decided the
    best way to get an inverse is to create a dictionary of hue versus
    wavelength and use that for lookups.  As soon as the equivalent
    hue is above 212, the color automatically becomes red.  Not ideal,
    but it's a limitation of the mapping in wl2rgb().  Ultimately, we
    should judge wl2rgb() by how well it seems to reproduce the visible
    spectrum to our eyes.  Here's a terminal-based approximation that
    fits on one line:

    """)
    )
    for wl in range(380, 781, 6):
        cn = wl2rgb(wl)
        print(f"{t(cn.xrgb)}{square}", end="")
    print(f"{t.n}")

    print(
        dedent(f"""

    This looks to be identical (not suprisingly) to the simulated
    spectrum in the file spectrum.png, which was constructed with
    Bruton's FORTRAN algorithm to make a PPM file.  When I was a
    student, we had access to a monochromator by Bausch & Lomb and I
    would like to use that to compare to what I see on my screen.  That
    monochromator used a diffraction grating to get its colors and they
    seemed to be very pure colors when you looked at the output (and
    the dial was calibrated in wavelength).  You might want to compare
    the colors to those at
    https://demonstrations.wolfram.com/ColorsOfTheVisibleSpectrum/.  I
    don't recall seeing the purple/magenta colors in the actual
    physical spectrum (at least not as simulated by the wl2rgb()
    function), but that was in the 1960's and my memory is a bit hazy.

    Here's the relationship between color and wavelength.  The first
    column is wavelength in nm.  The second column is the hue of the
    color calculated by the wl2rgb() function.  The third column is the
    hue of the wavelength in nm calculated by rgb2wl(); the hue is
    shown in the color from wl2rgb(), so the two shown colors should be
    identical if we did a good job of generating an inverse.  The Diff
    columns show the nonzero numerical differences in hue and
    wavelengths.  The hue differences should be zero, but the
    wavelengths will differ by 0 or 1 for a good fit (the differences
    of 1 come about because not all wavelengths map to an integer hue)
    over all except the reds.

    """)
    )
    print(f"{i}           Inv    Hue    nm")
    print(f"{i}nm     Hue Hue    Diff  Diff")
    for nm in range(380, 781, 10):
        print(f"{i}{nm:3d}    ", end="")
        cn = wl2rgb(nm, gamma=0)
        x = cn.xrgb
        hue = cn.HLS[0]
        print(f"{t(x)}{hue:03d}{t.n} ", end="")
        # Convert wl2rgb() color's hue back to wavelength
        nm_new = rgb2wl(cn)
        cn_new = wl2rgb(nm_new, gamma=0)
        hue_new = cn_new.HLS[0]
        print(f"{t(cn_new.xrgb)}{hue_new:03d}{t.n}   ", end="")
        hue_diff = hue_new - hue
        hue_diff = str(hue_diff) if hue_diff else ""
        nm_diff = nm_new - nm
        nm_diff = str(nm_diff) if nm_diff else ""
        print(f"{hue_diff:4s}   ", end="")
        print(f"{nm_diff:4s}")
    print(
        dedent(f"""

    Not suprisingly, the inverse for wavelength is poor for the reds
    approaching the infrared.  Note the lack of dimming because gamma
    was set to zero in wl2rgb().

    """)
    )


if 1:
    Introduction()
    BasicColorNames()
    Thoughts1()
    HueIntervals()
    HueGradations()
    FirstChoice(4)
    SomeNames()
    HueVersusFrequency()
