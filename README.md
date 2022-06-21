# plib

Last updated 18 May 2022 

# Introduction
This repository is a collection of python stuff I've written since 1998.
Feel free to browse and use what suits your needs.  There are quite a few
files, use the tools (see below) to help understand what these files are
for.  Most of the stuff is licensed under the Open Software License version
3.0.

* The `plib` directory holds modules that are intended to be used by other
  scripts.
* The `pgm` directory holds scripts that are separate programs.
* The `test` directory holds scripts that test the modules in `plib` (many
  of the modules have their test code built-in).
* The `g` directory holds a python graphics library I wrote about 20 years
  ago; it's a thin layer over PostScript.  It has made thousands of images
  for me over that time.  I would have preferred SVG, but it was too
  immature at the time.  An item on my to-do list is to write a backend for
  it that outputs SVG.

This is a work-in-progress.  Currently, a few tests fail in /plib.  Most of
the scripts in /plib/pgm don't have suitable 'what' strings (see 0what.py
below), so you'll have to look at the code to see what they do.
Eventually, all the 'what' strings will be filled out, as I can't remember
what all this stuff does myself.

As of this writing (March 2022), this stuff has been tested with python
3.7.12 in a cygwin environment on Windows 10.

## Coding style

My coding style is vertically compressed which most folks won't like.  You
can use a style formatter (e.g., black) to to recover more normal vertical
formatting.  I use pgm/rbl.py to remove blank lines so I can see as much as
possible on my screen.  

I use a folding editor, which folds on indentation and explains the
frequent use of 'if 1:' element, which I use to divide the code up into
viewable chunks.  A completely folded file should be viewable in a few tens
of lines.  I also use a second 4k monitor in portrait mode to view 100 to
150 lines of text at once; this is quite convenient for coding.

My editor has commands to go to the next paragraph, which is defined by a
bare newline.  With no blank lines in a file, this lets me set up
"bookmarks" by inserting an empty line.  I can then jump between two areas
in a file with one key press, which is fast and efficient.  It's much
faster than using stored bookmarks or multiple tab pages.

You'll find 'git log' pretty useless, as my development model is similar to
how I used RCS at home for a few decades.  I'm the only developer and I
make check-ins when I've gotten far enough where I don't want to lose
something, so I check it in with no comment (when I worked in industry,
such behavior would have gotten me put on the 'atomiser', if you've read
"Broken Angels") and push it to github.  I also rarely make branches.  I'll
occasionally mark a notable event with a tag. 

## Status

I made this repository public on 7 Mar 2022.  I'll slowly add to it over
time and fix/maintain some of the stuff.  My intent is that this stuff will
remain here for a few years after I've died or when I turn its maintenance
over to a friend who said he'd be the caretaker for it after I'm no longer
able to do this.  By then any content of interest to others will probably
have made its way out into the world; he can remove the repository when he
sees fit.

## Caution

The set of files in this directory are a core set of python modules and
scripts I've written over the years for my own use.  There's some useful
functionality in here, but I must warn you it's fairly tightly coupled.  By
this, I mean if you find a script you like and want to move it somewhere
else, you'll probably find that it's dependent on a number of other
modules.  This will be annoying and possibly a lot of work to fix.

# Tools

## PostScript drawing tool

The g.py and other files in the g directory are a python wrapper over
PostScript for making drawings.  I wrote it in 2001 because there wasn't
anything available at the time to do such tasks.  Surprisingly, it has been
used for thousands of tasks over that time with very few changes.  When I
find time, I'd like to rearchitect it to have a back-end rendering plugin
setup to allow different types of graphical files to be generated.  I'd
also like to change to a more object-oriented implementation to allow
easier subclassing for specialized tasks.

## 0what.py

The 0what.py script can be run with the argument `.` and you'll get a short
description of each python file in the current directory.  These will be
organized by categories.

## 0test.py

This script will run the self tests of the files.  The tests are either in
the module file or are located in the test directory.  Each module file has
a special trigger string (see trigger.py) that tells 0test.py how to run
its tests.  If you run 'python 0test.py', you'll get a summary report of
passes and failures.  Only failed tests will print out messages.  Use the
-v option to see each test's output.  The default output tells you the
files that fail self-tests and need to be worked on.

As of this writing (7 Mar 2022), there's one test that fails and some
warning messages from a few other tests.  I'll eventually get around to
fixing things, but such things aren't a priority.

# Most useful

Here are a few of the modules/scripts I use a lot.

* get.py
    - Get text, lines, tokens, words, binary content, etc. from files.  I
      use GetLines and GetTextLines the most.

* util.py
    - Numerous utility functions.

* pgm/prun.py
    - I use this to develop python scripts in a terminal window.  When the
      script's modification time changes by saving the script in the editor
      window (a different terminal window), the script is run, allowing you
      to see the results without leaving your editor window.  This is handy
      when using short output messages when debugging functionality, as you
      can see everything on the screen.  It also has an option to launch a
      browser showing you a diff of the previous and latest outputs so you
      can see what changed.

* color.py
    - Contains three key classes (Color, Trm, and ColorName) to deal with
      color definitions and generating escape codes for using color in text
      in output to a terminal.  This file went through a large revision in
      March/April 2022, as I changed the design from something I had been
      using for a couple of decades (it was renamed kolor.py and will
      eventually be removed).  I included support for the old design, as it
      was used in about 80 files in this directory tree.  I'll slowly
      convert things over to the new file and delete the legacy stuff.  
    - A handy utility that uses color.py is pgm/cdec.py, which will
      decorate lines of a file with color specifiers, so you see the line
      in its specified color.  Try 'cdec colornames0' and you'll see a
      demo.  The colornames0 is my default set of colors with naming based
      on the 3 letter names of the resistor color code.  Run color.py as a
      script to see the colors and add the 'a' argument to see the styles.
      I use this in a mintty terminal under cygwin and it's a powerful
      terminal program with 24-bit color support and numerous styles,
      including subscripts and superscripts.

* lwtest.py
    - Lightweight test runner adapted from a nice tool by Raymond
      Hettinger.  I use this testing of my python modules.

* f.py
    - Provides flt and cpx types, derived from float and complex,
      respectively.  Their advantage is that they only show 3 significant
      figures by default, stopping the typical digit diarrhea with the
      usual float or complex calculations.  This file is still under
      development -- but I use the flt() objects a lot for routine
      calculations because they are so convenient for calculating things
      based on measurements.  
    - flt and cpx currently support physical units too (kind of, but there
      are testing and corner case errors), but this is a lot of extra code
      and I have a to-do item to remove unit support, as I don't feel it's
      worth the coding and testing effort.

