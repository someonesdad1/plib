# Color utilities
Wed 16 Mar 2022 02:41:55 PM

# build directory

The files in this directory are used to build the /plib/rgbdata.py module,
which is used to correlate color name strings with RGB values.  These
scripts have the data from the indicated website that I collected in 2014
and, where the URLs weren't defunct, were verified and updated in March of
2022 (except for the wikipedia data).

When you enter this directory, run the build.py script.  It will construct
rgbdata.py, compare it to the current /plib/rgbdata.py file, and replace
the latter if they don't match.

There are 10637 colors in the list in rgbdata.py, far too many names.  Over
3000 of them have duplicates in the file.

# clrinterp.py

This script lets you supply arguments in the form 'c1 n c2 m c3 ...' where
the c's are color specifiers like '#121ef45' and n, m, etc. are integers.
The script then prints n hex specifiers that interpolate between c1 and c2
and analogously for the other colors.  You can use the options -@, -#, or
-$ to determine if the interpolation takes place in HSV, RGB, or HLS space,
respectively.

Example:  python clrinterp.py '#000000' 8 '#ffffff' shows eight grays
between black and white.  The values shown on the screen are:

\#000000 #242424 #484848 #6d6d6d #919191 #b6b6b6 #dadada #ffffff

# cnvclr.py

This script will convert and display color specifiers.  The default
behavior for 'python cnvclr.py \#7e4071' is to display the string input in
the color it represents.  Adding the -a option displays RGB, HSV, and HLS
values in hex, integer, and decimal fraction forms along with any color
names in the rgbdata.py file that match this color.  For example, the
indicated color is a dark magenta that xkcd's color data calls "bruise".

A handy use is to call 'python cnvclr.py -' and pipe a file's contents to
it.  It uses regular expressions to recognize color specifiers on each line
and, if found, prints out the line in the indicated color.  A variation on
this is if you use the '-f file' option to read the lines from a file.
Then you can include regular expressions on the command line to search for
(they are OR'd together).  Any matches found are printed out in the
indicated color.  Thus, 'python cnvclr.py -f rgbdata.py lilac' shows all
the colors with 'lilac' in their name and you can see how they display
differently on your screen.

# view.py

This script sorts the colors in rgbdata.py by RGB value and prints the six
hex digits out to the screen, wrapping so that you get orderly columns of
output.  On my computer (mintty under cygwin on Windows 10 with a 4k
monitor), I can view all of the colors on the screen at once when I use a
terminal window with 548 columns and 157 lines.  Yes, things are tiny, but
I can read them with a magnifier.
