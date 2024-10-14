'''
Provides convenience functions for CIE color data

ToDo
    - Write an access function that uses the data to linearly interpolate
      to the user's wavelength.
    - Compare the approximation to the interpolated table values.  Print
      out % deviations.
    - In the cie_cmf_analytical_code.zip file,
      xyzViewer/data/intraObserverVariance_20nm.h gives data on the
      variance at various wavelengths.  Use interpolation for these numbers
      to estimate the standard deviation of the diffs and display them as
      nominal normal deviates.


'''
from pdb import set_trace as xx 
import sys
import colorcoord
import wl2rgb
from color import Color, t

if 0:
    import debug
    debug.SetDebugger()

def GetCIETable():
    '''Returns a tuple of (nm, (xbar, ybar, zbar)) values to give the CIE's
    standard method to convert from a power spectral density (PSD) function
    to X, Y, Z tristimulus coordinates.  A PSD is integrated with these
    numerical functions over the wavelengths of 380 to 780 nm.  These are
    for the 2° field of view.  These numbers were derived around 1930 from
    two experimental samples from 17 people.  The experiments were careful
    and have been repeated, so though the samples were biased, it seems 
    they represent a large portion of humanity.
 
    From 204.xls downloaded from
    https://web.archive.org/web/20170131100357/http://files.cie.co.at/204.xls
    Thu 24 Mar 2022.
    '''
    # CIE 1931 standard colorimetric observer			
    # Columns: 
    #     wavelength, nm
    #     xbar(wl_nm)
    #     ybar(wl_nm)
    #     zbar(wl_nm)
    data = [
        [380, [0.001368, 0.000039, 0.006450]],
        [385, [0.002236, 0.000064, 0.010550]],
        [390, [0.004243, 0.000120, 0.020050]],
        [395, [0.007650, 0.000217, 0.036210]],
        [400, [0.014310, 0.000396, 0.067850]],
        [405, [0.023190, 0.000640, 0.110200]],
        [410, [0.043510, 0.001210, 0.207400]],
        [415, [0.077630, 0.002180, 0.371300]],
        [420, [0.134380, 0.004000, 0.645600]],
        [425, [0.214770, 0.007300, 1.039050]],
        [430, [0.283900, 0.011600, 1.385600]],
        [435, [0.328500, 0.016840, 1.622960]],
        [440, [0.348280, 0.023000, 1.747060]],
        [445, [0.348060, 0.029800, 1.782600]],
        [450, [0.336200, 0.038000, 1.772110]],
        [455, [0.318700, 0.048000, 1.744100]],
        [460, [0.290800, 0.060000, 1.669200]],
        [465, [0.251100, 0.073900, 1.528100]],
        [470, [0.195360, 0.090980, 1.287640]],
        [475, [0.142100, 0.112600, 1.041900]],
        [480, [0.095640, 0.139020, 0.812950]],
        [485, [0.057950, 0.169300, 0.616200]],
        [490, [0.032010, 0.208020, 0.465180]],
        [495, [0.014700, 0.258600, 0.353300]],
        [500, [0.004900, 0.323000, 0.272000]],
        [505, [0.002400, 0.407300, 0.212300]],
        [510, [0.009300, 0.503000, 0.158200]],
        [515, [0.029100, 0.608200, 0.111700]],
        [520, [0.063270, 0.710000, 0.078250]],
        [525, [0.109600, 0.793200, 0.057250]],
        [530, [0.165500, 0.862000, 0.042160]],
        [535, [0.225750, 0.914850, 0.029840]],
        [540, [0.290400, 0.954000, 0.020300]],
        [545, [0.359700, 0.980300, 0.013400]],
        [550, [0.433450, 0.994950, 0.008750]],
        [555, [0.512050, 1.000000, 0.005750]],
        [560, [0.594500, 0.995000, 0.003900]],
        [565, [0.678400, 0.978600, 0.002750]],
        [570, [0.762100, 0.952000, 0.002100]],
        [575, [0.842500, 0.915400, 0.001800]],
        [580, [0.916300, 0.870000, 0.001650]],
        [585, [0.978600, 0.816300, 0.001400]],
        [590, [1.026300, 0.757000, 0.001100]],
        [595, [1.056700, 0.694900, 0.001000]],
        [600, [1.062200, 0.631000, 0.000800]],
        [605, [1.045600, 0.566800, 0.000600]],
        [610, [1.002600, 0.503000, 0.000340]],
        [615, [0.938400, 0.441200, 0.000240]],
        [620, [0.854450, 0.381000, 0.000190]],
        [625, [0.751400, 0.321000, 0.000100]],
        [630, [0.642400, 0.265000, 0.000050]],
        [635, [0.541900, 0.217000, 0.000030]],
        [640, [0.447900, 0.175000, 0.000020]],
        [645, [0.360800, 0.138200, 0.000010]],
        [650, [0.283500, 0.107000, 0.000000]],
        [655, [0.218700, 0.081600, 0.000000]],
        [660, [0.164900, 0.061000, 0.000000]],
        [665, [0.121200, 0.044580, 0.000000]],
        [670, [0.087400, 0.032000, 0.000000]],
        [675, [0.063600, 0.023200, 0.000000]],
        [680, [0.046770, 0.017000, 0.000000]],
        [685, [0.032900, 0.011920, 0.000000]],
        [690, [0.022700, 0.008210, 0.000000]],
        [695, [0.015840, 0.005723, 0.000000]],
        [700, [0.011359, 0.004102, 0.000000]],
        [705, [0.008111, 0.002929, 0.000000]],
        [710, [0.005790, 0.002091, 0.000000]],
        [715, [0.004109, 0.001484, 0.000000]],
        [720, [0.002899, 0.001047, 0.000000]],
        [725, [0.002049, 0.000740, 0.000000]],
        [730, [0.001440, 0.000520, 0.000000]],
        [735, [0.001000, 0.000361, 0.000000]],
        [740, [0.000690, 0.000249, 0.000000]],
        [745, [0.000476, 0.000172, 0.000000]],
        [750, [0.000332, 0.000120, 0.000000]],
        [755, [0.000235, 0.000085, 0.000000]],
        [760, [0.000166, 0.000060, 0.000000]],
        [765, [0.000117, 0.000042, 0.000000]],
        [770, [0.000083, 0.000030, 0.000000]],
        [775, [0.000059, 0.000021, 0.000000]],
        [780, [0.000042, 0.000015, 0.000000]],
        # Sums:  (21.371524, 21.371327, 21.371540)
    ]
    if not GetCIETable.checked:
        # Tasks:
        #   - Check the sums of each column
        #   - Round each float to 6 decimal places
        #   - Cache in GetCIETable.data
        checked = []
        Σx = Σy = Σz = 0
        f = lambda x: round(x, 6)
        for wl, d in data:
            Σx += d[0]
            Σy += d[1]
            Σz += d[2]
            checked.append((wl, tuple([f(i) for i in d])))
        if f(Σx) != f(21.371524):
            raise ValueError("Bad x checksum")
        if f(Σy) != f(21.371327):
            raise ValueError("Bad y checksum")
        if f(Σz) != f(21.371540):
            raise ValueError("Bad z checksum")
        GetCIETable.data = checked
    return GetCIETable.data
GetCIETable.checked = False
GetCIETable()

def GetCIEDict():
    '''Returns a dict keyed by integer wavelength in nm to return the CIE
    1931 Color Matching Functions to convert a spectral power density to
    tristimulus XYZ values by integration.  The keys are integers on the
    interval [380, 780] in steps of 1.
    '''
    if GetCIEDict.dict is None:
        # Linearly interpolate the GetCIETable()'s data to get 1 nm steps
        di = {}
        for wl, cmf in GetCIETable():
            di[wl] = cmf
        f = lambda x, n: round(x, n)
        for wl in range(380, 779, 5):
            start, end = di[wl], di[wl + 5]
            slope = [f((j - i)/5, 10) for i, j in zip(start, end)]
            for i in (1, 2, 3, 4):
                a = [f(j + k*i, 6) for j, k in zip(start, slope)]
                di[wl + i] = a
        GetCIEDict.dict = di
    return GetCIEDict.dict
GetCIEDict.dict = None

def wl2cie_xy(wl_nm):
    '''Returns CIE xy for a given integer wavelength in nm.  These are the
    1931 xy coordinates of the outside edges of the chromaticity diagram
    that correspond to a wavelength.  Spot checks against a few 1931
    chromaticity diagrams indicate the correct values have been gotten.
    '''
    di = GetCIEDict()
    wl = int(wl_nm)
    if wl not in di:
        msg = f"'{wl_nm}' isn't an integer wavelength in [380, 780]"
        raise ValueError(msg)
    XYZ = di[wl]
    f = lambda x, n: round(x, n)
    t = sum(XYZ)
    n = 4
    return (f(XYZ[0]/t, n), f(XYZ[1]/t, n))

def Round(x, n):
    'Round a sequence of floats to n places'
    return tuple([round(i, n) for i in x])


if 0:
    # See what we get for XYZ with a (1, 1, 1) sRGB.
    # https://en.wikipedia.org/wiki/SRGB#sRGB_definition states we should get
    # (X = 0.9505, Y = 1.0000, Z = 1.0890) and we actually get [0.9505, 1.0,
    # 1.0888], so this is a good start.  This is a Y of 1 for a D65 source.
    XYZ = Round(colorcoord.sRGB_to_XYZ((1, 1, 1)), 4)
    print(XYZ)
    # Note we should get (1, 1, 1) back and we do within 1 part in 1e4.
    print(colorcoord.XYZ_to_sRGB(XYZ))
    exit()

if 1:
    # Print the wavelengths out in their sRGB colors
    print("wl in nm vs CIExy")
    To_sRGB =  colorcoord.xy_to_sRGB
    step = 5
    for nm in range(380, 781, step):
        x, y = wl2cie_xy(nm)
        rgb = To_sRGB((x, y), Y=1)
        cn = Color(*rgb)
        bruton_rgb = wl2rgb.wl2rgb(nm)
        print(f"{t(cn)}{nm:3d} ({x:5.3f}, {y:5.3f}){t.n}     ", end="")
        print(f"{t(bruton_rgb)}Bruton wavelength{t.n}")
    exit()
