# Chromaticity

Human color perception is more complicated than one expects.  First start
with the wavelengths of colored that are separated by a device like a prism
or diffraction grating.  See
http://hyperphysics.phy-astr.gsu.edu/hbase/vision/specol.html.

Once you know about these spectral colors, you then have to factor in how
humans perceive light, based on the physical mechanisms of the human eye
and brain.  Start at http://hyperphysics.phy-astr.gsu.edu/hbase/vision/ciecon.html#c1

http://hyperphysics.phy-astr.gsu.edu/hbase/vision/colper.html
gives an overview and shows why the chromaticity diagram is such a useful
tool.

http://ultra.sdk.free.fr/docs/Image-Processing/Colors/Format/Chromaticity%20Diagrams%20Lab%20Report.htm
provides some computed chromaticity diagrams

Color matching functions (CMF)
https://en.wikipedia.org/wiki/CIE_1931_color_space#Color_matching_functions
These are three functions of light wavelength wl:  xbar(wl), ybar(wl), and
zbar(wl).  These weighting functions that produce the CIE tristimulus
values X, Y, Z when integrated with the spectral radiance over the typical
visible range of 380 to 780 nm.
