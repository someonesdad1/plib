'''
Provides the function wl2rgb() to convert a light wavelength in nm into an
approximate RGB color.
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Convert between RGB and light wavelength in nm
        #∞what∞#
        #∞test∞# ignore #∞test∞#
    # Standard imports
    # Custom imports
        from color import Color
    # Global variables
        ii = isinstance
def wl2rgb(nm, gamma=0.8):
    '''Convert nm (light wavelength in nm) into a Color object using a
    linear approximation.  The Color object represents an RGB color.
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
        b = [float((i*j)**gamma) for j in a]
    else:
        b = [float(i) for i in a]
    # Make sure the numbers are on [0, 1]
    assert(all([0 <= i <=1 for i in b]))
    return Color(*b)
if 0:
    # This was an approximate inverse function before color.py was
    # rewritten.
    def rgb2wl(colornum):
        'Convert the indicated color to a wavelength in nm'  
        '''
        The algorithm is
            - Get the integer value of the hue on [0, 255]
            - If hue > 212 return 645 nm
            - Otherwise hue is in [0, 211] and use a dictionary lookup
        '''
        if not ii(colornum, Color):
            raise TypeError("colornum must be a Colorinstance")
        if not hasattr(rgb2wl, "dict"):
            # Cache a dictionary to convert integer hue on [0, 211] to integer
            # wavelength in nm.
            dict = {}
            if 0:
                for nm in range(380, 645):
                    cn = wl2rgb(nm, gamma=0)
                    hue = cn.dhls[0]
                    dict[hue] = nm
                rgb2wl.dict = dict
                # Fix missing values
                for i in set(range(0, 212)) - set(dict):
                    dict[i] = dict[i - 1]
            else:
                for nm in range(380, 781):
                    cn = wl2rgb(nm, gamma=0)
                    hue = cn.dhls[0]
                    if hue > 212:
                        dict[hue] = 645
                    else:
                        dict[hue] = nm
                # Fill in missing values
                for hue in range(256):
                    i = hue
                    while hue not in dict:
                        i -= 1
                        try:
                            dict[hue] = dict[i]
                        except KeyError:
                            if i < 0:
                                raise Exception("Bad algorithm")
                rgb2wl.dict = dict
        hue = colornum.ihls[0]
        assert(ii(hue, int) and 0 <= hue <= 255)
        if hue > 212:
            return 645
        return rgb2wl.dict[hue]
if 0 and __name__ == "__main__": 
    from lwtest import run, Assert
    def Test():
        diffs = []
        for nm in range(380, 645):
            rgb = wl2rgb(nm)
            nm1 = rgb2wl(rgb)
            diffs.append(nm - nm1)
        diffs = set(diffs)
        Assert(min(diffs) == -7)
        Assert(max(diffs) == 6)
    exit(run(globals(), halt=True, broken=True)[0])
