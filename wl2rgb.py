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
        from f import flt
    # Global variables
        ii = isinstance
def wl2rgb(nm, gamma=0.8):
    '''Convert nm (light wavelength in nm on [380, 780]) into a Color
    object using a linear approximation.  The Color object represents an
    RGB color.  gamma is used for a gamma adjustment.
    '''
    # Translation of Dan Bruton's FORTRAN code from (defunct URL)
    # http://www.physics.sfasu.edu/astro/color/spectra.html into python.
    # See http://www.midnightkite.com/color.html.
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
if 0:   # Attempt at wl2rgb with a JavaScript function
    def wl2rgb1(nm):
        '''
        From https://stackoverflow.com/questions/3407942/rgb-values-of-visible-spectrum/22681410#22681410
        near bottom by user bobtato.
        '''
        orig_js_source = '''
            function wavelengthToRGB (λ) {
                const C=[
                    350,
                        3.08919e-5,-2.16243e-2, 3.78425e+0,
                        0.00000e+0, 0.00000e+0, 0.00000e+0,
                        4.33926e-5,-3.03748e-2, 5.31559e+0,
                    397,
                        -5.53952e-5, 4.68877e-2,-9.81537e+0,
                        6.13203e-5,-4.86883e-2, 9.66463e+0,
                        4.41410e-4,-3.46401e-1, 6.80468e+1,
                    423,
                        -3.09111e-5, 2.61741e-2,-5.43445e+0,
                        1.85633e-4,-1.53857e-1, 3.19077e+1,
                        -4.58520e-4, 4.14940e-1,-9.29768e+1,
                    464,
                        2.86786e-5,-2.91252e-2, 7.39499e+0,
                        -1.66581e-4, 1.72997e-1,-4.39224e+1,
                        4.37994e-7,-1.09728e-2, 5.83495e+0,
                    514,
                        2.06226e-4,-2.11644e-1, 5.43024e+1,
                        -6.65652e-5, 7.01815e-2,-1.74987e+1,
                        9.41471e-5,-1.07306e-1, 3.05925e+1,
                    565,
                        -2.78514e-4, 3.36113e-1,-1.00439e+2,
                        -1.79851e-4, 1.98194e-1,-5.36623e+1,
                        1.12142e-5,-1.35916e-2, 4.11826e+0,
                    606,
                        -1.44403e-4, 1.73570e-1,-5.11884e+1,
                        2.47312e-4,-3.19527e-1, 1.03207e+2,
                        0.00000e+0, 0.00000e+0, 0.00000e+0,
                    646,
                        6.24947e-5,-9.37420e-2, 3.51532e+1,
                        0.00000e+0, 0.00000e+0, 0.00000e+0,
                        0.00000e+0, 0.00000e+0, 0.00000e+0,
                    750
                ];
                let [r,g,b] = [0,0,0];
                if (λ >= C[0] && λ < C[C.length-1]) {
                    for (let i=0; i<C.length; i+=10) {
                        if (λ < C[i+10]) {
                            const λ2 = λ*λ;
                            r = C[i+1]*λ2 + C[i+2]*λ + C[i+3];
                            g = C[i+4]*λ2 + C[i+5]*λ + C[i+6];
                            b = C[i+7]*λ2 + C[i+8]*λ + C[i+9];
                        break;
                    }
                }
            }
            return [r,g,b];
        '''
        # NOTE:  this code translated to python doesn't appear to generate
        # reasonable output as compared to wl2rgb().
        # https://github.com/polydojo/jispy is a JavaScript interpreter written
        # in python.
        C = (
            350,        3.08919e-5,-2.16243e-2, 3.78425e+0,
                        0.00000e+0, 0.00000e+0, 0.00000e+0,
                        4.33926e-5,-3.03748e-2, 5.31559e+0,
            397,       -5.53952e-5, 4.68877e-2,-9.81537e+0,
                        6.13203e-5,-4.86883e-2, 9.66463e+0,
                        4.41410e-4,-3.46401e-1, 6.80468e+1,
            423,       -3.09111e-5, 2.61741e-2,-5.43445e+0,
                        1.85633e-4,-1.53857e-1, 3.19077e+1,
                       -4.58520e-4, 4.14940e-1,-9.29768e+1,
            464,        2.86786e-5,-2.91252e-2, 7.39499e+0,
                       -1.66581e-4, 1.72997e-1,-4.39224e+1,
                        4.37994e-7,-1.09728e-2, 5.83495e+0,
            514,        2.06226e-4,-2.11644e-1, 5.43024e+1,
                       -6.65652e-5, 7.01815e-2,-1.74987e+1,
                        9.41471e-5,-1.07306e-1, 3.05925e+1,
            565,       -2.78514e-4, 3.36113e-1,-1.00439e+2,
                       -1.79851e-4, 1.98194e-1,-5.36623e+1,
                        1.12142e-5,-1.35916e-2, 4.11826e+0,
            606,       -1.44403e-4, 1.73570e-1,-5.11884e+1,
                        2.47312e-4,-3.19527e-1, 1.03207e+2,
                        0.00000e+0, 0.00000e+0, 0.00000e+0,
            646,        6.24947e-5,-9.37420e-2, 3.51532e+1,
                        0.00000e+0, 0.00000e+0, 0.00000e+0,
                        0.00000e+0, 0.00000e+0, 0.00000e+0,
            750
        )
        rgb, λ = [0, 0, 0], flt(nm)
        λmin, λmax = 350, 750
        assert λ > 0
        if λmin <= λ <= λmax:
            for i in range(0, len(C), 10):
                if λ < C[i+10]:
                    λ2 = λ*λ
                    r = C[i+1]*λ2 + C[i+2]*λ + C[i+3];
                    g = C[i+4]*λ2 + C[i+5]*λ + C[i+6];
                    b = C[i+7]*λ2 + C[i+8]*λ + C[i+9];
                    if 1:
                        assert 0 <= r <= 1
                        assert 0 <= g <= 1
                        assert 0 <= b <= 1
                    rgb = [int(j)*255 for j in (r, g, b)]
                break
        return Color(*rgb)
if 1:   # Attempt at an inverse to wl2rgb()
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

if __name__ == "__main__": 
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
    #exit(run(globals(), halt=True, broken=True)[0])
    for nm in range(380, 645, 2):
        rgb = wl2rgb(nm)
        nm1 = rgb2wl(rgb)
        print(f"{nm:3d} {rgb} {nm1}")
