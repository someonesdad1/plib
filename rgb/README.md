# rgb directory
Wed 16 Mar 2022 02:41:55 PM

These python files are used to build the ../rgbdata.py module, which is
used to correlate color names with RGB values.  These scripts have the data
from the indicated website that I collected in 2014 and, where the URLs
weren't defunct, were verified and updated in March of 2022 (except for the
wikipedia data).

Color naming is a subjective mess.  I put this list together more out of
curiosity than anything else.  There are 10637 colors in the list in
rgbdata.py.

The view.py script sorts the colors by RGB value and prints the six hex
digits out to the screen, wrapping so that you get orderly columns of
output.  On my computer (mintty under cygwin on Windows 10 with a 4k
monitor), I can view all of the colors on the screen at once.
