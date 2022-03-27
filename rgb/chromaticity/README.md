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

http://hyperphysics.phy-astr.gsu.edu/hbase/vision/colper.html
gives an overview and shows why the chromaticity diagram is such a useful
tool.

http://ultra.sdk.free.fr/docs/Image-Processing/Colors/Format/Chromaticity%20Diagrams%20Lab%20Report.htm
provides some computed chromaticity diagrams.  Also see
https://en.wikipedia.org/wiki/Chromaticity.

In school in the 1960's, one morning I played around with a Fabry-Perot
interferometer being illuminated by a sodium light in a dark room (I was
setting the equipment up for a lab period later that afternoon).  I
remember being surprised that my eye could see a color difference between
the two lines of the sodium doublet at 589 nm; they differ by 0.6 nm.
Since that was a long time ago, I can't remember whether my perception was
that the colors were different or whether I interpreted them as different
because one line is less intense than the other.  An article
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2570376/ discusses wavelength
discrimination.  From examining figure 3 in the article, particlarly the
black squares or dots and their error bars, I conclude I probably could not
see the color difference -- rather, I saw an intensity difference that led
my brain to concluding that the colors were different.  Because of the
small sample size (4 "younger" people (mean 31 years) and 4 "older" (mean
72 years)) of this well-written paper, it's not clear to me that the
experiment detected a real difference, regardless of what the regressions
say (look at the size of within-group standard deviations); it was a
difficult and time consuming experiment to run.

# Color matching functions (CMF)

https://en.wikipedia.org/wiki/CIE_1931_color_space#Color_matching_functions
These are three functions of light wavelength wl:  xbar(wl), ybar(wl), and
zbar(wl).  These weighting functions produce the CIE tristimulus values X,
Y, Z when integrated with the spectral radiance over the typical visible
range of 380 to 780 nm.

# Chromaticity diagrams

A chromaticity diagram plots colors in their "x, y" values or equivalents
in the various CIE coordinates.  If you see coordinates x, y, then it is a
1931 plot.  If you see u, v, it is a 1960 plot.  If you see u', v', it is a
1976 plot.  See https://en.wikipedia.org/wiki/Chromaticity.

These plots all contain the same information, but they are scaled
differently.  I prefer the 1976 plot because the Euclidean distance between
the points approximately measure the humanly-perceived "distance" between
two colors.  The 1976 plot is the 1931 plot changed by a projective
transformation with the intent of making the Euclidean distances
approximately the same as how much human's perceive the colors to be
different.  Much of the mess of all these color spaces and transformations
is due to the subjective nature of color interpretation.

1931Chromaticity.jpg and 1960Chromaticity.jpg are from
http://ultra.sdk.free.fr/docs/Image-Processing/Colors/Format/Chromaticity%20Diagrams%20Lab%20Report_files/CIE1931.jpg

1976Chromaticity.jpg is from
http://hyperphysics.phy-astr.gsu.edu/hbase/vision/vispic/cie1976b.jpg
