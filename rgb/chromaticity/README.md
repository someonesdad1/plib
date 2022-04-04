# Chromaticity

Human color perception is more complicated than one expects.  First start
with the wavelengths of colored that are separated by a device like a prism
or diffraction grating.  See
http://hyperphysics.phy-astr.gsu.edu/hbase/vision/specol.html.

Once you know about these spectral colors, you then have to factor in how
humans perceive light, based on the physical mechanisms of the human eye
and brain.  Start at
http://hyperphysics.phy-astr.gsu.edu/hbase/vision/ciecon.html#c1.  You'll
be led to the fundamental work done by Wright and Guild in the late 1920's
using a sample of 17 people to characterize human vision as a function of
wavelength of light.  This led to the CIE 1931 color matching functions
(CMFs) that are still used today (see below and
https://en.wikipedia.org/wiki/CIE_1931_color_space).  

http://hyperphysics.phy-astr.gsu.edu/hbase/vision/colper.html gives an
overview and shows why the chromaticity diagram is a useful tool.

http://ultra.sdk.free.fr/docs/Image-Processing/Colors/Format/Chromaticity%20Diagrams%20Lab%20Report.htm
provides some computed chromaticity diagrams.  Also see
https://en.wikipedia.org/wiki/Chromaticity.

# Color matching functions (CMF)

https://en.wikipedia.org/wiki/CIE_1931_color_space#Color_matching_functions
These are three functions of light wavelength wl:  xbar(wl), ybar(wl), and
zbar(wl).  These weighting functions produce the CIE tristimulus values X,
Y, Z when integrated with the spectral radiance over the typical visible
range of 380 to 780 nm.

# Chromaticity diagrams

A chromaticity diagram plots colors in their 1931 CIE "x, y" values or
equivalents in the various CIE coordinate systems.  If you see coordinates
x, y, then it is a 1931 plot.  If you see u, v, it is a 1960 plot.  If you
see u', v', it is a 1976 plot.  See
https://en.wikipedia.org/wiki/Chromaticity.

Such plots contain the same information, but they are scaled differently.
The 1931 chromaticity diagram suffers from being perceived as giving too
much "weight" to greens, so the CIE has fiddled with it over the decades,
primarily in 1960 and then in 1976.

I prefer the 1976 plot because Euclidean distances between points
approximately measure the humanly-perceived "distance" between two colors.
The 1976 plot is the 1931 plot changed by a projective transformation with
the intent of making the Euclidean distances approximately the same as how
much human's perceive the colors to be different.  Much of the mess of all
these color spaces and transformations is due to the subjective nature of
color interpretation.

1931Chromaticity.jpg and 1960Chromaticity.jpg are from
http://ultra.sdk.free.fr/docs/Image-Processing/Colors/Format/Chromaticity%20Diagrams%20Lab%20Report_files/CIE1931.jpg

1976Chromaticity.jpg is taken from
http://hyperphysics.phy-astr.gsu.edu/hbase/vision/vispic/cie1976b.jpg,
although it may be due to http://www.color-theory-phenomena.nl/10.03.htm.

# nimeroff.py

This python script contains the data from the paper I. Nimeroff, J.
Rosenblatt, M. Dannemiller, "Variability of Spectral Tristimulus Values",
J. Research of the NBS A, 65A(6) 475-483, Nov-Dec 1961.  Table 3 of the
paper gives the proposed CIE 10° observer color matching functions in 10 nm
steps.  Most usefully, the estimated variances and covariances are included
which can give you a feeling for how well the observers were able to match
colors.  In a nutshell, the standard deviations are within about 0.1 to 0.2
of the mean and are mostly composed of between-observer variation.

# solarspectrum.jpg

This picture came from
https://solarsystem.nasa.gov/resources/390/the-solar-spectrum/, which in
turn came from Kitt Peak Observatory, published in Nov 2017.  It shows the
sun's spectrum from 400 to 700 nm with each of the 50 strips being 6 nm
wide.  The dark lines are absorption lines that identify elements in
various parts of the sun.  This provides a "fingerprint" of the elements in
the sun and is what astronomers used to e.g. classify the age and type of a
star.  Shortest wavelength is at bottom left and wavelength increases to
the right.  If you magnify the image, you'll see a number of strange color
quantification oddities in the bottom 6 or 7 lines where the violet portion
of the spectrum resides.  It's likely these colors are out of the typical
sRGB gamut for computer monitors.

# Wavelength discrimination

nihms72432_wavelength_discrimination.pdf and wavelength_discrimination.png
show that human wavelength discrimination is, at best, around 2 nm.  The
latter picture, though terse and useful, is disappointingly unattributed at 
https://www.wolframalpha.com/widgets/gallery/view.jsp?id=5072e9b72faacd73c9a4e4cb36ad08d#.
