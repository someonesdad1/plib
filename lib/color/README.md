# Color utilities
Wed 16 Mar 2022 02:41:55 PM

# rgbdata_build directory

The files in this directory are used to build the /plib/rgbdata.py module, which is used to
correlate color name strings with RGB values.  These scripts have the data from the indicated
websites that I collected in 2014 and, where the URLs weren't defunct, were verified and updated
in March of 2022 (except for the wikipedia data).

When you enter this directory, run the build.py script.  It will construct rgbdata.py.  You can
diff it with /plib/rgbdata.py and if it is updated, you can manually replace the latter if you
wish.

There are 10637 colors in the list in rgbdata.py, far too many names.  Over 3000 of them have
duplicates in the file.

# view.py

This script sorts the colors in rgbdata.py by RGB value and prints the six hex digits out to the
screen, wrapping so that you get orderly columns of output.  On my computer (mintty under cygwin
on Windows 10 with a 4k monitor), I can view all of the colors on the screen at once when I use a
terminal window with 548 columns and 157 lines.  Yes, things are tiny, but I can read them with a
magnifier.
