'''

Color transformations 
    - References
        - [poyn] Poynton's ColorFAQ.pdf.
        - [kon]
          https://sensing.konicaminolta.us/us/learning-center/color-measurement/color-spaces/
        - [wplab] https://en.wikipedia.org/wiki/CIELAB_color_space

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
        return XYZ
    def XYZ_to_rgb(XYZ):
        'XYZ is a 3-tuple of numbers'
        # [poyn] pg 10
        f = lambda a, b: sum([i*j for i, j in zip(a, b)])
        r1 = (3.240479, -1.537150, -0.498535)
        r2 = (-0.969256, 1.875992, 0.041556)
        r3 = (0.055648, -0.204043, 1.057311)
        rgb = Dot(r1, XYZ), Dot(r2, XYZ), Dot(r3, XYZ)
        # Clamp to [0, 1]
        rgb = [float(round(Clamp(i), 6)) for i in rgb]
        return tuple(rgb)
    def XYZ_to_xy(XYZ):
        t = sum(XYZ)
        return (XYZ[0]/t, XYZ[1]/t)
    def xy_to_XYZ(xy, Y):
        return (x*Yy, Y, (1 - x - y)/y*Y)
    def D65():
        # D65 standard illuminant
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

if 1:   # Test functions
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

if 0:
    Check();exit()
    rgb = 1.0, 1.0, 1.0
    XYZ = rgb2XYZ(rgb)
    RGB = XYZ2rgb(XYZ)
    Assert(rgb == RGB)
    exit()

if __name__ == "__main__": 
    exit(run(globals(), halt=True)[0])
