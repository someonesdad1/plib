'''
Experiment to convert wavelength in nm to RGB colors.  The raw data are the
1931 CIE PSD to XYZ tristimulus coordinates, which are then converted to
xyY values.

ToDo
    - Write a function which interpolates to 1 nm intervals.  Linear
      interpolation for this should be fine.

The raw data are in the cid204.xls file downloaded from
https://web.archive.org/web/20170131100357/http://files.cie.co.at/204.xls
on 24 Mar 2022.
'''
from pdb import set_trace as xx 
from f import flt
from wrap import dedent
import sys
if len(sys.argv) > 1:
    import debug
    debug.SetDebugger()
if 1:   # CIE data
    # This table is the standard method to convert from a power spectral
    # density (PSD) function to X, Y, Z tristimulus coordinates.  The PSD is
    # integrated with these numerical functions over the wavelengths of 380 to
    # 780 nm.  These are for the 2° field of view.  
    data = '''
        # CIE 1931 standard colorimetric observer			
        # Columns: 
        #     wavelength, nm
        #     xbar(wl_nm)
        #     ybar(wl_nm)
        #     zbar(wl_nm)
        380	0.001368	0.000039	0.006450
        385	0.002236	0.000064	0.010550
        390	0.004243	0.000120	0.020050
        395	0.007650	0.000217	0.036210
        400	0.014310	0.000396	0.067850
        405	0.023190	0.000640	0.110200
        410	0.043510	0.001210	0.207400
        415	0.077630	0.002180	0.371300
        420	0.134380	0.004000	0.645600
        425	0.214770	0.007300	1.039050
        430	0.283900	0.011600	1.385600
        435	0.328500	0.016840	1.622960
        440	0.348280	0.023000	1.747060
        445	0.348060	0.029800	1.782600
        450	0.336200	0.038000	1.772110
        455	0.318700	0.048000	1.744100
        460	0.290800	0.060000	1.669200
        465	0.251100	0.073900	1.528100
        470	0.195360	0.090980	1.287640
        475	0.142100	0.112600	1.041900
        480	0.095640	0.139020	0.812950
        485	0.057950	0.169300	0.616200
        490	0.032010	0.208020	0.465180
        495	0.014700	0.258600	0.353300
        500	0.004900	0.323000	0.272000
        505	0.002400	0.407300	0.212300
        510	0.009300	0.503000	0.158200
        515	0.029100	0.608200	0.111700
        520	0.063270	0.710000	0.078250
        525	0.109600	0.793200	0.057250
        530	0.165500	0.862000	0.042160
        535	0.225750	0.914850	0.029840
        540	0.290400	0.954000	0.020300
        545	0.359700	0.980300	0.013400
        550	0.433450	0.994950	0.008750
        555	0.512050	1.000000	0.005750
        560	0.594500	0.995000	0.003900
        565	0.678400	0.978600	0.002750
        570	0.762100	0.952000	0.002100
        575	0.842500	0.915400	0.001800
        580	0.916300	0.870000	0.001650
        585	0.978600	0.816300	0.001400
        590	1.026300	0.757000	0.001100
        595	1.056700	0.694900	0.001000
        600	1.062200	0.631000	0.000800
        605	1.045600	0.566800	0.000600
        610	1.002600	0.503000	0.000340
        615	0.938400	0.441200	0.000240
        620	0.854450	0.381000	0.000190
        625	0.751400	0.321000	0.000100
        630	0.642400	0.265000	0.000050
        635	0.541900	0.217000	0.000030
        640	0.447900	0.175000	0.000020
        645	0.360800	0.138200	0.000010
        650	0.283500	0.107000	0.000000
        655	0.218700	0.081600	0.000000
        660	0.164900	0.061000	0.000000
        665	0.121200	0.044580	0.000000
        670	0.087400	0.032000	0.000000
        675	0.063600	0.023200	0.000000
        680	0.046770	0.017000	0.000000
        685	0.032900	0.011920	0.000000
        690	0.022700	0.008210	0.000000
        695	0.015840	0.005723	0.000000
        700	0.011359	0.004102	0.000000
        705	0.008111	0.002929	0.000000
        710	0.005790	0.002091	0.000000
        715	0.004109	0.001484	0.000000
        720	0.002899	0.001047	0.000000
        725	0.002049	0.000740	0.000000
        730	0.001440	0.000520	0.000000
        735	0.001000	0.000361	0.000000
        740	0.000690	0.000249	0.000000
        745	0.000476	0.000172	0.000000
        750	0.000332	0.000120	0.000000
        755	0.000235	0.000085	0.000000
        760	0.000166	0.000060	0.000000
        765	0.000117	0.000042	0.000000
        770	0.000083	0.000030	0.000000
        775	0.000059	0.000021	0.000000
        780	0.000042	0.000015	0.000000
    '''[1:-1]
    # Check:  the sum of the columns should be these numbers
    Sum = (21.371524, 21.371327, 21.371540)

# Read in the data; the columns are tab-separated
cie = []
x = flt(0)
x.n = 3
x.rtz = x.rtdp = x.f = True
for line in data.split("\n"):
    line = line.strip()
    if not line or line.strip()[0] == "#":
        continue
    nm, *d = line.strip().split("\t")
    nm = int(nm)
    d = [flt(i) for i in d]
    cie.append((nm, d))
# Check sums
sx = sy = sz = 0
for nm, d in cie:
    sx += d[0]
    sy += d[1]
    sz += d[2]
f = lambda x: round(x, 6)
assert(f(sx) == Sum[0])
assert(f(sy) == Sum[1])
assert(f(sz) == Sum[2])
# Convert to integer values
cieint = []
for nm, d in cie:
    e = [int(round(i*1e6, 0)) for i in d]
    cieint.append((nm, e))
# Check sums again
sx = sy = sz = 0
for nm, d in cieint:
    sx += d[0]
    sy += d[1]
    sz += d[2]
f = lambda x: round(x, 6)
assert(sx == f(1e6*Sum[0]))
assert(sy == f(1e6*Sum[1]))
assert(sz == f(1e6*Sum[2]))
# Write out as integer structure

print(f'''# cieint1931
# This structure contains the 1931 CIE numerical functions for converting
# an optical power spectral density to the tristimulus XYZ functions.  This
# is nominally done by integrating the PSD over wavelength, weighted by
# these xbar, ybar, zbar functions.  Linear interpolation to the nearest nm
# works well and integration by summing over 1 nm intervals works
# acceptably.  Divide the integers in the (xbar, ybar, zbar) tuples by 1e6
# to get the CIE's floating point numbers and around to 6 decimal places.
''')
print("cieint1931 = (")
w = 7
for nm, d in cieint:
    x, y, z = d
    print(f"    ({nm:3d}, ({x:{w}d}, {y:{w}d}, {y:{w}d})),")
print(")")
print(f"# (xbar, ybar, zbar) tuple values should sum to ({sx}, {sy}, {sz})")
