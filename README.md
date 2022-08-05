# plib

Last updated 4 Aug 2022 

# Introduction
This repository is a collection of python stuff I've written since 1998.
Feel free to browse and use what suits your needs.  There are quite a few
files, use the tools (see below) to help understand what these files are
for.  Most of the stuff is licensed under the Open Software License version
3.0.

* The `plib` directory holds modules that are intended to be used by other
  scripts.
* The `plib/pgm` directory holds scripts that are separate programs.
* The `plib/test` directory holds scripts that test the modules in `plib` (many
  of the modules have their test code built-in).
* The `plib/g` directory holds a python graphics library that is a
  thin layer over PostScript.

This is a work-in-progress.  Currently, a few tests fail in /plib.  Most of
the scripts in `plib/pgm` don't have suitable 'what' strings (see 0what.py
below), so you'll have to look at their code to see what they do.
Eventually, all the 'what' strings will be filled out, as I can't remember
what all this stuff does myself.

Some repository tags are:
    * Creation_7Mar2022:  date the repository was created
    * Python_3.9_testing_26Jul2022:  I started using python 3.9 (I had been
      using 3.7 for a number of years).  The command 'python 0test.py .'
      passes for all the tested python modules except for geom_prim.py.

As of this writing (Jul 2022), this stuff has been tested with python
3.9.10 in a cygwin environment on Windows 10.  

## Coding style

My coding style is vertically compressed which most folks won't like.  You
can use a style formatter (e.g., black) to to recover more normal vertical
formatting.  I use pgm/rbl.py to remove blank lines so I can see as much as
possible on my screen.  

I use a folding editor, which folds on indentation and explains the
frequent use of 'if 1:' element, which I use to divide the code up into
viewable chunks.  A completely folded file should be viewable in 20-30 
lines.  I also use a second 4k monitor in portrait mode to view 100 to
150 lines of text at once; this is very convenient for coding.

My editor has commands to go to the next paragraph, which is defined by a
bare newline.  With no blank lines in a file, this lets me set up
"bookmarks" by inserting an empty line.  I can then jump between two areas
in a file with one key press, which is fast and efficient.  It's much
faster than using stored bookmarks or multiple tab pages.

You'll find 'git log' pretty useless in this repository, as my development
model is similar to how I used RCS at home for a few decades.  I'm the only
developer and I make check-ins when I've gotten far enough where I don't
want to lose something, so I check it in with no comment (when I worked in
industry, such behavior would have gotten one put on the 'atomiser', if
you've read "Broken Angels") and push it to github.  I also rarely make
branches.  I'll occasionally mark a notable event with a tag. 

I use pycodestyle (a python PEP8 style checker) to check my code's style,
but dislike the verbose output, so I pipe it to pgm/pycodestyle_filter.py,
which 1) condenses the output, 2) color codes the error/warning number and
description, and 3) only outputs the more important stuff unless the -a
option is used.  While I don't follow all the recommendations, I try to
correct the egregious problems.

## Status

I made this repository public on 7 Mar 2022.  I'll slowly add to it over
time and fix/maintain some of the stuff.  My intent is that this stuff will
remain here for a few years after I've died or when I turn its maintenance
over to a friend who said he'd be the caretaker for it after I'm no longer
able to maintain things.  By then any content of interest to others will probably
have made its way out into the world; he can remove the repository when he
sees fit.

## Caution

The set of files in this directory are a core set of python modules and
scripts I've written over the years for my own use.  There's some useful
functionality in here, but I must warn you it's fairly tightly coupled.  By
this, I mean if you find a script you like and want to move it somewhere
else, you'll probably find that it's dependent on a number of other
modules.  This will be annoying and possibly a lot of work to fix.  This
repository on my system is /plib and my PYTHONPATH variable is
"/plib:/plib/g", so this repository is the only code I use outside of
what's in the python distribution. 

# Software lesson

Recently I needed to execute some code buried in a function inside of a
function in /plib/color.py because running some code showed an exception in
this code.  I rashly stuck in three lines in the middle of the file like

> c = Color(args)
> Call the offending method
> exit()

I then got distracted by something else and I didn't get back to using my
system the next day, as I used another computer in the living room in the
evening.  Next morning I went to use my Windows system and something had
happened to the system (maybe an update), as all the files in my /plib had
the execute bit on, which I hate because an ls listing shows everything
green.  I ran my script /plib/pgm/x.py which fixes this quickly, but it
didn't work.  Then I tried to use my command I use to go to another
directory (the /plib/pgm/goto.py script) and it didn't work.  I couldn't
get **any** python stuff to work and it started to make me panic.  I ran
cygwin's setup again to reinstall python and rebooted the computer.  No
change.  Then I finally stuck a debugger breakpoint at the beginning of the
x.py script and stepped through the initial imports at the beginning of the
file and saw an exception when color.py was imported.  Calling that file up
in vim positioned me on the rashly inserted code and I knew what the
problem was:  idiot in the pilot's seat.  There are 85 files that import
color.py, so it's used quite a bit.  The key lesson is that such lines
should always be in a block that begins with 'if __name__ == "__main__":'
to help avoid such problems.

# Tools

## PostScript drawing tool

The g.py and other files in the g directory are a python wrapper over
PostScript for making drawings.  I wrote it in 2001 because there wasn't
anything available at the time to do such tasks.  Surprisingly, it has been
used for thousands of tasks over that time with few changes.

## 0what.py

The 0what.py script can be run with the argument `.` and you'll get a short
description of each python file in the current directory.  These will be
organized by categories.

## 0test.py

This script will run the self tests of the files.  The tests are either in
the module's file or are located in the test directory.  Each module file has
a special trigger string (see trigger.py) that tells 0test.py how to run
its tests.  If you run 'python 0test.py', you'll get a summary report of
passes and failures.  Only failed tests will print out messages.  Use the
-v option to see each test's output.  The default output tells you the
files that fail self-tests and need to be worked on.

# Most useful

Here are a few of the modules/scripts I use a lot or provide useful
techniques.

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

* lwtest.py
    - Lightweight test runner adapted from a nice tool by Raymond
      Hettinger.  I use this for testing of my python modules.

* f.py
    - Provides flt and cpx types, derived from float and complex,
      respectively.  Their advantage is that they only show 3 significant
      figures by default, stopping digit diarrhea with the usual float or
      complex calculations.  This file is still under development -- but I
      use the flt() objects a lot for routine calculations because they are
      so convenient for calculating things based on measurements.  

* prob.py
    - Provides cumulative distribution functions and their inverses for
      common statistical tests.  This module calls into a DLL made from S.
      Moshier's cephes library functions in C for the mathematical
      functions using the ctypes module. 

* matrix.py
    - While numpy provides matrices, it's occasionally nice to have a
      pure-python module to deal with matrices.  The matrix.py module is
      derived from a public domain lightweight matrix module (version 3.0.0
      of pymatrix gotten on 15 Jul 2019).  The module lets you put into a
      matrix anything that can be put into a list (the implementation uses
      nested lists).  mpmath supplies matrices based on dictionaries (great
      for sparse matrices), so that's an alternative.  mpmath.iv includes
      matrices that use mpmath.mpi interval numbers, which are handy for
      quantifying roundoff issues in matrix calculations.

* pgm/uni.py
    - This is a script that allows you to look up Unicode characters,
      either by codepoint string or looking for a particular string in the
      character's description.  I use this script a lot when writing
      scripts and working in a terminal.

* pgm/goto.py
    - This is a script that keeps track of strings and lets you find them
      by either typing in their number from a list or using a short alias.
      I use this to keep track of directories, project files, videos, and a
      bunch of other stuff.  One of the hidden benefits is that the
      datafile used for the projects, directories, etc. can be commented
      out, meaning you'll be able to remember where they are.  My computer
      has many hundreds of thousands of files and it's nearly impossible to
      remember where everything is.
