'''
Todo
    - Need tests for all the functions

Color coordinates and transformations 
    - Your thumb at the end of your arm is 2°; your fist is 10°. 
    - Chances are, if you get some RGB color data, it's probably in the sRGB color space.  For
      example, the Dell monitor I'm using is stated as covering 99% of the sRGB space.  Because of
      this, the primary tools that should be used to go from a device RGB space to a perceptual
      space such as CIEXYZ should be the functions sRGB_to_XYZ and XYZ_to_sRGB below.
    - Here, LAB means CIE's L*a*b*, not Hunter's LAB
    - XYZ
        - CIE 1930 tristimulus values representing the amount of blue, green, and red gotten from
          an integration of the physical PSD with the three human response functions for blue,
          green, and red
    - xyY
        - Transformed XYZ by x = X/s, y = Y/s, s = sum(X, Y, Z)
        - Y represents the intensity of the light, regardless of color
        - x, y represent the chromaticity (hue)
    - References
        - [cie1931] https://en.wikipedia.org/wiki/CIE_1931_color_space
            - Results from experiments in late 1920's (D. Wright, 10 observers; J. Guild, 7
              observers).
            - Relate wavelength of light to human-perceived color
            - Though the samples sizes are small and they were undoubtedly biased, Guild's Phil
              Trans paper stated "The trichromatic coefficients for [Wright's] ten observers
              agreed so closely with those of the seven observers examined at the National
              Physical Laboratory as to indicate that both groups must give results approximating
              more closely to 'normal' than might have been expected from the size of either
              group."
        - [schils] http://www.color-theory-phenomena.nl/index.html.  Paul Schils died in 2011, so
          these pages won't be updated.  http://www.color-theory-phenomena.nl/07.00.html is good
          with a number of general thoughts/observations.
        - [hyperp1] http://hyperphysics.phy-astr.gsu.edu/hbase/vision/colper.html
            - Overview of color perception
        - [hyperp2] http://hyperphysics.phy-astr.gsu.edu/hbase/vision/cieprim.html
            - An overview of the 1931 CIE primary XYZ tristimulus values.  Properties
                - X, Y, and Z are alays positive
                - Any color can be represented by these three numbers
                - Equal values of X, Y, Z produce white
                - Y determines the luminance of the color
                - Related to sensitivity of human eye
                - The color matching functions (CMF) let you derive X, Y, Z by multiplying the CMF
                  at each wavelength by the spectral power distribution (SPD, derived e.g. from a
                  spectrophotometer), summing, and normalizing.  Note z = 1
                  - x - y, so x and y are the relevant color coordinates.
                - Result is x, y, and Y for the luminance.
                - Y is luminance, which is radiant flux power weighted by the sensitivity of the
                  human eye, giving luminous flux in lumens.
        - [cmf1] https://www.sciencedirect.com/topics/engineering/color-matching-function
        - [cmf2] http://cvrl.ioo.ucl.ac.uk/cmfs.htm  Site for downloading CIE color matching
          functions
        - [poyn] Poynton's ColorFAQ.pdf
        - [kon] https://sensing.konicaminolta.us/us/learning-center/color-measurement/color-spaces/
        - [wplab] https://en.wikipedia.org/wiki/CIELAB_color_space
        - [efg] http://ultra.sdk.free.fr/docs/Image-Processing/Colors/Format/Chromaticity%20Diagrams%20Lab%20Report.htm
        - [jw] https://www.fourmilab.ch/documents/specrend/  Explains about getting XYZ
          coordinates and converting from xy to RGB (device) color.  His table 1 shows
          chromaticities of primary colors for various system.  Note his article is from 1996, the
          same year that sRGB came out, so his material doesn't cover it.
        - The Dell manual for my P2415 manual pg 10 state the color gamut of the monitor is
          102.28% of CIE1976 test standards and includes 99% of sRBG.
        - https://getreuer.info/posts/colorspace/index.html gives some C++ code for color space
          transformation functions
        - https://easyrgb.com/en/math.php shows the math functions for their RGB calculator.  A
          refreshing find in the crappy world of calculator boxes with no explanations.
        - https://medium.com/hipster-color-science/a-beginners-guide-to-colorimetry-401f1830b65a
          has some good discussions.
        - http://www.cvrl.org/ Color & Vision Research Lab, Institute of Ophthalmology, part of
          Univ. College London.
        - https://rgbcmyk.com.ar/en/emulating-the-wright-guild-experiment/ Web page with an
          "emulator" of the Wright and Guild experiments, asking you to match colors like was done
          in the late 1920s.
        - http://jamie-wong.com/post/color/ Pretty good discussion.  I like the comment near the
          end "even if you're a person who understands that most things are deeper than they look,
          color is way deeper than you would reasonably expect".
        - Grassman's Law:  if two colors are indistinguishable (metamers), you can add another
          color equally to both of them and they will still appear to be the same color.  This
          with the Wright and Guild experiments showed that we are dealing with a linear system.
          Grassman was an 1800's polymath who is also known for Grassman algebra.
        - https://michaelbach.de/ot/col-lilacChaser/index.html Interesting applet to play around
          with.  If I put it in my browser on the right half of my first monitor and edit this
          text on my other monitor, my peripheral vision sees the moving green dots and mostly
          ignores the lilac colored ones.
        - https://scholar.harvard.edu/files/schwartz/files/lecture17-color.pdf Good discussion.
          Makes the point on pg 7 that the point of inventing XYZ is it lets us embed all
          perceivable colors in a triangle on the chromaticity diagram.
        - https://www.w3.org/TR/css-color-4 is a good document on color in CSS and the specs

'''
if 1:   # Imports
    from util import IsIterable
    from lwtest import run, raises, assert_equal, Assert
if 1:   # Utility
    def Dot(a, b, n=None):
        'Dot product of two sequences (n is number of decimal places to round to)'
        Assert(len(a) == len(b))
        if n:
            return sum([round(i*j, n) for i, j in zip(a, b)])
        return sum([i*j for i, j in zip(a, b)])
    def Clamp(a):
        'Clamp all values onto [0, 1]'
        f = lambda x: min(max(0.0, x), 1.0)
        if IsIterable(a):
            return tuple([f(i) for i in a])
        else:
            return f(a)
if 1:   # Core functionality
    def xy_to_sRGB(xy, Y=1):
        def f(x):
            return tuple([round(float(i), 4) for i in x])
        XYZ = xy_to_XYZ(xy, Y)
        return f(XYZ_to_sRGB(XYZ))
    def sRGB_to_XYZ(srgb, hires=False):
        '''Returns a tuple of XYZ values for an sRGB tuple.  All values in srgb must be on [0, 1].
        sRGB to CIE XYZ from https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ 
        
        - srgb components must be on [0, 1].  If 8-bit numbers, divide by 255 to put on this
          range.
        - Use "gamma-expanded" values if the component is > 0.04; otherwise divide the component
          by 12.92.
        - Transform to XYZ space with a matrix transformation.
 
        Test values:  Let sRGB = (0.2, 0.5, 0.8).  Transform each component x to be ((x +
        0.055)/1.055)**2.4, giving (0.033104766570885055, 0.21404114048223255, 0.6038273388553378)
        = (a, b, c).  The matrix multiplication is 
 
        X = 0.4124*a + 0.3576*b + 0.1805*c
        Y = 0.2126*a + 0.7152*b + 0.0722*c
        Z = 0.0193*a + 0.1192*b + 0.9505*c
 
        giving (0.19918435223366782, 0.20371663091121825, 0.6000905115222988).  The routine rounds
        this to 4 figures.
        '''
        def GammaExpand(x):
            return x/12.92 if x <= 0.04045 else ((x + 0.055)/1.055)**2.4
        # Make sure all values are between 0 and 1
        Assert(all([0 <= i <= 1 for i in srgb]))
        # Transformation matrix to produce XYZ values with respect to the D65 illumination (6500 K
        # blackbody radiation).
        if hires:
            # More significant figures from
            # https://www.image-engineering.de/library/technotes/958-how-to-convert-between-srgb-and-ciexyz
            n = 7
            r1 = (0.4124564, 0.3575761, 0.1804375)
            r2 = (0.2126729, 0.7151522, 0.0721750)
            r3 = (0.0193339, 0.1191920, 0.9503041)
        else:
            n = 4
            r1 = (0.4124, 0.3576, 0.1805)
            r2 = (0.2126, 0.7152, 0.0722)
            r3 = (0.0193, 0.1192, 0.9505)
        # "Gamma-expand" the values (the web page calls these the "linear" components).
        rgb = [GammaExpand(i) for i in srgb]
        # Perform the matrix transformation
        XYZ = Dot(r1, rgb), Dot(r2, rgb), Dot(r3, rgb)
        # Round the results
        XYZ = tuple(round(i, n) for i in XYZ)
        return XYZ
    def XYZ_to_sRGB(XYZ, hires=False):
        '''CIE XYZ to sRGB
        https://en.wikipedia.org/wiki/SRGB#From_CIE_XYZ_to_sRGB
        
        The test case for sRGB_to_XYZ will result in the original sRGB values when operated on
        with XYZ_to_sRGB().
        '''
        def GammaCompressed(x):
            return 12.92*x if x <= 0.0031308 else 1.055*x**(1/2.4) - 0.055
        if hires:
            # More significant figures from
            # https://www.image-engineering.de/library/technotes/958-how-to-convert-between-srgb-and-ciexyz
            n = 7
            r1 = (+3.2404542, -1.5371385, -0.4985314)
            r2 = (-0.9692660, +1.8760108, +0.0415560)
            r3 = (+0.0556434, -0.2040259, +1.0572252)
        else:
            n = 4
            r1 = (+3.2406, -1.5372, -0.4986)
            r2 = (-0.9689, +1.8758, +0.0415)
            r3 = (+0.0557, -0.2040, +1.0570)
        rgb = Dot(r1, XYZ), Dot(r2, XYZ), Dot(r3, XYZ)
        # Round the results and gamma compress
        sRGB = [round(GammaCompressed(i), n) for i in rgb]
        # Clip to [0, 1]
        clip = lambda x:  min(1, max(x, 0))
        sRGB = [clip(i) for i in sRGB]
        return tuple(sRGB)
    def XYZ_to_xy(XYZ):
        t = sum(XYZ)
        return (XYZ[0]/t, XYZ[1]/t)
    def xy_to_XYZ(xy, Y=1):
        x, y = xy
        return ((Y/y)*x, Y, (1 - x - y)*(Y/y))
    def D65(tristimulus=True):
        '''D65 standard illuminant tristimulus values Ref:
        https://en.wikipedia.org/wiki/Illuminant_D65#Definition This is
        nominally a blackbody at 6500 K For a standard 2° observer.  If
        tristimulus is True, returns standard X, Y, Z tristimulus values
        with luminance (Y); otherwise, standard chromaticity coordinates x,
        y, z are returned.
        '''
        if tristimulus:
            return 95.0489, 100, 108.8840
        else:
            return 0.31271, 0.32902, 0.35827
if 1:   # L*a*b*
    def XYZ_to_LAB(XYZ):
        # https://en.wikipedia.org/wiki/CIELAB_color_space#From_CIEXYZ_to_CIELAB
        def f(t):
            d = 6/29
            return t**(1/3) if t > d**3 else t/(3*d*d) + 4/29
        Xn, Yn, Zn = D65()
        X, Y, Z = XYZ
        L = 116*f(Y/Yn) - 16
        a = 500*(f(X/Xn) - f(Y/Yn))
        b = 200*(f(Y/Yn) - f(Z/Zn))
        return L, a, b
    def LAB_to_XYZ(LAB):
        def g(t):
            d = 6/29
            return t**3 if t > d else 3*d*d*(t - 4/29)
        Xn, Yn, Zn = D65()
        L, a, b = LAB
        X = Xn*g((L + 16)/116 + a/500)
        c = (L + 16)/116
        Y = Yn*g(c)
        Z = Zn*g(c - b/200)
if 1:   # L*u*v*
    # CIE's 1976 space that aims at representing perceptual differences
    # better
    def XYZ_to_CIELUV(XYZ, u1n=0.2009, v1n=0.4610, Yn=None):
        '''CIEL*u*v* 1976 color space which attempts perceptual uniformity.
        https://en.wikipedia.org/wiki/CIELUV.  You must define Yn. 
        '''
        if Yn is None:
            raise ValueError("Yn must be defined")
        X, Y, Z = XYZ
        s = X + 15*Y + 3*Z
        u1, v1 = 4*X/s, 9*Y/s
        t = (6/29)**3
        a = Y/Yn
        Lstar = t*a if a <= t else 116*a**(1/3) - 16
        ustar = 13*Lstar*(u1 - u1n)
        vstar = 13*Lstar*(v1 - v1n)
        return (Lstar, ustar, vstar)
    def CIELUV_to_XYZ(CIELUV, u1n=0.2009, v1n=0.4610, Yn=None):
        '''Reverse transformation of XYZ_to_CIELUV.
        https://en.wikipedia.org/wiki/CIELUV
        '''
        Lstar, ustar, vstar = CIELUV
        u1 = ustar/(13*Lstar) + u1n
        v1 = vstar/(13*Lstar) + v1n
        Y = Yn*Lstar*(3/29)**3 if Lstar <= 8 else Yn*((Lstar + 16)/116)**3
        X = Y*9*u1/(4*v1)
        Z = Y*(12 - 3*u1 - 20*v1)/(4*v1)
        return (X, Y, Z)
if 1:   # Other functionality
    def rgb_to_XYZ(rgb):
        'rgb is a 3-tuple of floats on [0, 1]'
        # [poyn] pg 10
        Assert(all([0 <= i <= 1 for i in rgb]))
        r1 = (0.412453, 0.357580, 0.180423)
        r2 = (0.212671, 0.715160, 0.072169)
        r3 = (0.019334, 0.119193, 0.950227)
        Assert(sum(r2) == 1)
        n = 6
        XYZ = Dot(r1, rgb, n), Dot(r2, rgb, n), Dot(r3, rgb, n)
        return XYZ
    def XYZ_to_rgb(XYZ):
        'XYZ is a 3-tuple of numbers'
        # [poyn] pg 10
        # Note:  this is the inverse of the matrix in rgb_to_XYZ()
        r1 = (3.240479, -1.537150, -0.498535)
        r2 = (-0.969256, 1.875992, 0.041556)
        r3 = (0.055648, -0.204043, 1.057311)
        rgb = Dot(r1, XYZ), Dot(r2, XYZ), Dot(r3, XYZ)
        # Clamp to [0, 1].  I'm also rounding to 6 places because that's
        # the resolution of the transformation matrix's values.
        rgb = [float(round(Clamp(i), 5)) for i in rgb]
        return tuple(rgb)
    def XYZ_to_xyz(XYZ):
        # CIE 1931 xyz values
        # [efg] under first chromaticity diagram
        s = sum(XYZ)
        xyz = [float(i/s) for i in XYZ]
        Assert(sum(xyz) == 1)
        return xyz
    def xyz_to_uv(xyz):
        # [efg] under 1960 CIE chromaticity diagram
        x, y, z = xyz
        s = -2*x + 12*y + 3
        u = 4*x/s
        v = 6*y/s
        return u, v
    def XYZ_to_uv(XYZ):
        # [efg] under 1960 CIE chromaticity diagram
        X, Y, Z = XYZ
        s = X + 15*Y + 3*Z
        u = 4*X/s
        v = 6*Y/s
        return u, v
    def uv_to_xy(uv):
        # u, v are 1960 CIE chromaticity coordinates
        # [efg] under 1960 CIE chromaticity diagram
        s = 2*u - 8*v + 4
        x = 3*u/s
        y = 2*v/s
        return x, y
    def u1v1_to_xy(u1v1):
        # http://www.color-theory-phenomena.nl/10.03.htm
        # 1976 CIE u', v' to 1931 x, y
        # The advantage of the 1976 chromaticity diagram is that the
        # distance between the points is approximately proportional to a
        # human's perceived color difference.
        s = 9*u1/2 - 12*v1 + 9
        x = (27*u1/4)/s
        y = 3*v1/s
    def u1v1_to_xyz(u1v1):
        # [efg] under 1976 CIE u'v' chromaticity diagram
        u1, v1 = u1v1
        s = 6*u1 - 16*v1 + 12
        x = 9*u1/s
        y = 4*v1/s
        z = (-3*u1 - 20*v1 + 12)/s
        return x, y, z
    def XYZ_to_u1v1(XYZ):
        # [efg] under 1976 CIE u'v' chromaticity diagram
        X, Y, Z = XYZ
        s = X + 15*Y + 3*Z
        u1 = 4*X/s
        v1 = 9*Y/s
        return u1, v1

if __name__ == "__main__": 
    from color import t
    def Test_RGB():
        # Not working yet
        t.print(f"{t.ornl}Test_RGB() not working yet")
        return #xx
        def Test_XYZ_to_rgb():
            # [poyn] pg 9
            r = XYZ_to_rgb((0.64, 0.33, 0.03))
            Assert(r == (1, 0, 0))
            g = XYZ_to_rgb((0.3, 0.6, 0.1))
            Assert(g == (0, 0.838974, 0))
            b = XYZ_to_rgb((0.15, 0.06, 0.79))
            Assert(b == (0, 0, 0.83138))
            w = XYZ_to_rgb((0.3127, 0.3290, 0.3582))
            a = 0.329
            Assert(w == (a, a, a))
        def Test_rgb_to_XYZ():
            r = (1, 0, 0)
            XYZ = rgb_to_XYZ(r)
            print(XYZ)
            print(XYZ_to_rgb((0.64, 0.33, 0.03)))
        Test_XYZ_to_rgb()
        Test_rgb_to_XYZ()
    def Test_sRGB_to_XYZ():
        if 1:
            # This is the example given in the docstring of sRGB_to_XYZ and was
            # manually calculated in a python REPL.
            sRGB = (0.2, 0.5, 0.8)
            XYZ = sRGB_to_XYZ(sRGB, hires=False)
            Assert(XYZ == (0.1992, 0.2037, 0.6001))
            srgb = XYZ_to_sRGB(XYZ, hires=False)
            #
            XYZ = sRGB_to_XYZ(sRGB, hires=True)
            Assert(XYZ == (0.1991434, 0.2036937, 0.5999716))
            # Test inverse
            srgb = XYZ_to_sRGB(XYZ, hires=True)
            Assert(srgb == (0.2000006, 0.4999999, 0.8))
        # The following are easily calculated results, as they just pick
        # out the matrix columns
        if 1:
            hr = False
            sRGB = (1, 0, 0)
            XYZ = sRGB_to_XYZ(sRGB, hires=hr)
            expected = (0.4124, 0.2126, 0.0193)
            Assert(XYZ == expected)
            srgb = XYZ_to_sRGB(XYZ, hires=hr)
            Assert(srgb == (1, 0.0003, 0.0))
            #
            sRGB = (0, 1, 0)
            XYZ = sRGB_to_XYZ(sRGB, hires=hr)
            expected = (0.3576, 0.7152, 0.1192)
            Assert(XYZ == expected)
            srgb = XYZ_to_sRGB(XYZ, hires=hr)
            Assert(srgb == (0, 1, 0.0002))
            #
            sRGB = (0, 0, 1)
            XYZ = sRGB_to_XYZ(sRGB, hires=hr)
            expected = (0.1805, 0.0722, 0.9505)
            Assert(XYZ == expected)
            srgb = XYZ_to_sRGB(XYZ, hires=hr)
            Assert(srgb == (0.0003, 0, 1))
        if 1:
            hr = True
            sRGB = (1, 0, 0)
            XYZ = sRGB_to_XYZ(sRGB, hires=hr)
            expected = (0.4124564, 0.2126729, 0.0193339)
            Assert(XYZ == expected)
            srgb = XYZ_to_sRGB(XYZ, hires=hr)
            Assert(srgb == (0.9999999, 1.7e-06, 0))
            #
            sRGB = (0, 1, 0)
            XYZ = sRGB_to_XYZ(sRGB, hires=hr)
            expected = (0.3575761, 0.7151522, 0.119192)
            Assert(XYZ == expected)
            srgb = XYZ_to_sRGB(XYZ, hires=hr)
            Assert(srgb == (5e-07, 1, 0))
            #
            sRGB = (0, 0, 1)
            XYZ = sRGB_to_XYZ(sRGB, hires=hr)
            expected = (0.1804375, 0.072175, 0.9503041)
            Assert(XYZ == expected)
            srgb = XYZ_to_sRGB(XYZ, hires=hr)
            Assert(srgb == (6e-07, 0, 1))
    exit(run(globals(), halt=True)[0])
