'''

Color coordinates and transformations 
    - Here, LAB means CIE's L*a*b*, not Hunter's LAB
    - XYZ
        - CIE 1930 tristimulus values representing the amount of blue,
          green, and red gotten from an integration of the physical PSD
          with the three human response functions for blue, green, and red
    - xyY
        - Transformed XYZ by x = X/s, y = Y/s, s = sum(X, Y, Z)
        - Y represents the intensity of the light, regardless of color
        - x, y represent the chromaticity (hue)
    - References
        - [cie1931] https://en.wikipedia.org/wiki/CIE_1931_color_space
            - Results from experiments in late 1920's (D. Wright, 10
              observers; J. Guild, 7 observers).
            - Relate wavelength of light to human-perceived color
            - Though the samples sizes are small and they were undoubtedly
              biased, Guild's Phil Trans paper stated "The trichromatic
              coefficients for [Wright's] ten observers agreed so closely
              with those of the seven observers examined at the National
              Physical Laboratory as to indicate that both groups must give
              results approximating more closely to 'normal' than might
              have been expected from the size of either group."

        - [hyperp1] http://hyperphysics.phy-astr.gsu.edu/hbase/vision/colper.html
            - Overview of color perception
        - [hyperp2] http://hyperphysics.phy-astr.gsu.edu/hbase/vision/cieprim.html
            - An overview of the 1931 CIE primary XYZ tristimulus values.
              Properties
                - X, Y, and Z are alays positive
                - Any color can be represented by these three numbers
                - Equal values of X, Y, Z produce white
                - Y determines the luminance of the color
                - Related to sensitivity of human eye
                - The color matching functions (CMF) let you derive X, Y, Z by
                  multiplying the CMF at each wavelength by the 
                  spectral power distribution (SPD, derived
                  e.g. from a spectrophotometer), summing, and normalizing.
                  Note z = 1 - x - y, so x and y are the relevant color
                  coordinates.
                - Result is x, y, and Y for the luminance.
                - Y is luminance, which is radiant flux power weighted by
                  the sensitivity of the human eye, giving luminous flux in
                  lumens.
        - [cmf1] https://www.sciencedirect.com/topics/engineering/color-matching-function
        - [cmf2] http://cvrl.ioo.ucl.ac.uk/cmfs.htm  Site for
          downloading CIE color matching functions
        - [poyn] Poynton's ColorFAQ.pdf
        - [kon]
          https://sensing.konicaminolta.us/us/learning-center/color-measurement/color-spaces/
        - [wplab] https://en.wikipedia.org/wiki/CIELAB_color_space
        - [efg] http://ultra.sdk.free.fr/docs/Image-Processing/Colors/Format/Chromaticity%20Diagrams%20Lab%20Report.htm

'''
from pdb import set_trace as xx 
from util import IsIterable
from lwtest import run, raises, assert_equal, Assert

if 1:   # Utility
    def Dot(a, b):
        'Dot product of two sequences'
        Assert(len(a) == len(b))
        return sum([i*j for i, j in zip(a, b)])
    def Clamp(a):
        'Clamp all values onto [0, 1]'
        f = lambda x: min(max(0.0, x), 1.0)
        if IsIterable(a):
            return tuple([f(i) for i in seq])
        else:
            return f(a)
if 1:   # Core functionality
    def rgb_to_XYZ(rgb):
        'rgb is a 3-tuple of floats on [0, 1]'
        # [poyn] pg 10
        Assert(all([0 <= i <= 1 for i in rgb]))
        r1 = (0.412453, 0.357580, 0.180423)
        r2 = (0.212671, 0.715160, 0.072169)
        r3 = (0.019334, 0.119193, 0.950227)
        Assert(sum(r2) == 1)
        XYZ = Dot(r1, rgb), Dot(r2, rgb), Dot(r3, rgb)
        return tuple([round(i, 6) for i in XYZ])
    def XYZ_to_rgb(XYZ):
        'XYZ is a 3-tuple of numbers'
        # [poyn] pg 10
        f = lambda a, b: sum([i*j for i, j in zip(a, b)])
        r1 = (3.240479, -1.537150, -0.498535)
        r2 = (-0.969256, 1.875992, 0.041556)
        r3 = (0.055648, -0.204043, 1.057311)
        rgb = Dot(r1, XYZ), Dot(r2, XYZ), Dot(r3, XYZ)
        # Clamp to [0, 1].  I'm also rounding to 6 places because that's
        # the resolution of the transformation matrix's values.
        rgb = [float(round(Clamp(i), 6)) for i in rgb]
        return tuple(rgb)
    def XYZ_to_xyz(XYZ):
        # CIE 1931 xyz values
        # [efg] under first chromaticity diagram
        s = sum(XYZ)
        xyz = [float(i/s) for i in XYZ]
        Assert(sum(xyz) == 1)
        return xyz
    def XYZ_to_xy(XYZ):
        t = sum(XYZ)
        return (XYZ[0]/t, XYZ[1]/t)
    def xy_to_XYZ(xy, Y):
        return (x*Yy, Y, (1 - x - y)/y*Y)
    def D65():
        # D65 standard illuminant tristimulus values
        # == blackbody at 6500 K
        return 95.0489, 100, 108.8840
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
        # [efg] under 1960 CIE chromaticity diagram
        s = 2*u - 8*v + 4
        x = 3*u/s
        y = 2*v/s
        return x, y
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
        

if 0:
    Check();exit()
    rgb = 1.0, 1.0, 1.0
    XYZ = rgb2XYZ(rgb)
    RGB = XYZ2rgb(XYZ)
    Assert(rgb == RGB)
    exit()

if __name__ == "__main__": 
    def Test_XYZ_to_rgb():
        # [poyn] pg 9
        r = XYZ_to_rgb((0.64, 0.33, 0.03))
        g = XYZ_to_rgb((0.3, 0.6, 0.1))
        b = XYZ_to_rgb((0.15, 0.06, 0.79))
        w = XYZ_to_rgb((0.3127, 0.3290, 0.3582))
        Assert(r == (1, 0, 0))
        Assert(g == (0, 0.838974, 0))
        Assert(b == (0, 0, 0.83138))
        a = 0.329
        Assert(w == (a, a, a))
    exit(run(globals(), halt=True)[0])
