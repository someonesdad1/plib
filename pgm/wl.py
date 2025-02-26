"""
Print out a table of colors (using RGB) representing visible colors from
380 to 780 nm light wavelengths.
"""

from columnize import Columnize
from wrap import dedent
from color import Color, t


def wl2rgb(nm, gamma=0.8):
    """Convert nm (light wavelength in nm) into a Color instance using a linear approximation.
    The Color instance represents an RGB color.  gamma is used for a gamma adjustment.  nm must be
    on [380, 780].
    """
    # Translation of Dan Bruton's FORTRAN code from
    # http://www.physics.sfasu.edu/astro/color/spectra.html into python.  Also see
    # http://www.midnightkite.com/color.html.
    if 380 <= nm <= 440:
        a = (440 - nm) / (440 - 380), 0, 1
    elif 440 <= nm <= 490:
        a = 0, (nm - 440) / (490 - 440), 1
    elif 490 <= nm <= 510:
        a = 0, 1, (510 - nm) / (510 - 490)
    elif 510 <= nm <= 580:
        a = (nm - 510) / (580 - 510), 1, 0
    elif 580 <= nm <= 645:
        a = 1, (645 - nm) / (645 - 580), 0
    elif 645 <= nm <= 780:
        a = 1, 0, 0
    else:
        raise ValueError(f"Wavelength {nm} is not in [380, 780] nm")
    if gamma < 0:
        raise ValueError(f"gamma must be >= 0")
    # Intensity i falls off near vision limits
    i, u, v = 1, 0.3, 0.7
    if nm > 700:
        i = u + v * (780 - nm) / (780 - 700)
    elif nm < 420:
        i = u + v * (nm - 380) / (420 - 380)
    # Scale the RGB components by i and raise to the gamma power if gamma
    # is nonzero.
    if gamma:
        rgb = [float((i * j) ** gamma) for j in a]
    else:
        rgb = [float(i) for i in a]
    # Make sure the numbers are on [0, 1]
    assert all([0 <= i <= 1 for i in rgb])
    return Color(*rgb)


def SteppedWavelengths(nm_step):
    gamma = 0.8
    print(f"Wavelength in steps of {nm_step} nm to RGB colors")
    out, count = [], 0
    for nm in range(380, 781, nm_step):
        c = wl2rgb(nm, gamma=gamma)
        out.append(f"{t(c.xrgb)}{nm}{t.n}")
        count += 1
    o = Columnize(out, horiz=True)
    for line in o:
        print(line)
    print(f"{count} wavelengths printed")


SteppedWavelengths(5)
