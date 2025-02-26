# plib

Last updated 26 Feb 2025 

# Introduction

This repository is a collection of python stuff I've written since 1998.  Feel free to
browse and use what suits your needs.  There are quite a few files, use the tools (see
below) to help understand what these files are for.  Most of the stuff is licensed under
the Open Software License version 3.0.

* The `plib` directory holds modules that are intended to be used by other scripts.
* The `plib/pgm` directory holds scripts that are separate programs.
* The `plib/test` directory holds scripts that test the modules in `plib` (many modules
  have their test code built-in).
* The `plib/g` directory holds a python graphics library that is a thin layer over
  PostScript.

## Roadmap

I made this repository public in 2022.  My goals for 2025 are 

* /plib
    * Use [ruff](https://docs.astral.sh/ruff/) to lint & format the files
    * Self-tests are up-to-date and all pass
    * Remove specialized modules that are better stored elsewhere
    * Move stuff in from Dev as appropriate & clean up Dev
    * Standardize on style and structure (see below)
        * 
    * 0what.py returns useful output for all modules
* /plib/pgm:  All scripts working with updated style and structure.  Remove any dependencies on
  old color.py module (kolor.py).
* All material tested with python 3.11.
* Create HTML pages to make it easier to find content.

## Caution

The set of files in this directory are a core set of python modules and scripts I've written over
the years for my own use.  There's some useful functionality in here, but it's fairly tightly
coupled.  This means if you find a script you like and want to move it somewhere else, you may find
that it's dependent on a number of other modules.  This will be annoying and possibly a lot of work
to fix.  This repository on my system is `/plib` and my `PYTHONPATH` variable is `"/plib:/plib/g"`,
so this repository is the only code I use outside of what's in the python distribution. 

# Code formatting

I prefer to work on all source code with no blank lines at all because 1) it lets me see
the most information on my screen via folding and 2) I can navigate to where I'm working
faster than any other way (I won't explain it, as it's specific to the editor I use).

Tools like black and ruff will format code with blank lines (e.g., between functions and
classes) and change lines with spaces only into empty lines.  Because I use both of
these methods to speed navigation through python files, I wrote a python tool
/plib/pgm/dbl.py that will delete blank lines from a file that the formatter has
inserted and fix the docstring blank lines.  This gives me the best of both worlds, as I
also value a standardized format that let people focus on the content, not argue over
formatting.

Because I use dbl to format a python file to work on it, I may check something in that's
not formatted like ruff would do it.  If this bugs you, run it through your formatter.

# Tools

## PostScript drawing tool

The g.py and other files in the g directory are a python wrapper over PostScript for making
drawings.  I wrote it in 2001 because there wasn't anything available at the time to do such tasks.
It has been used for thousands of tasks over that time with essentially no changes except for when
a python change or external library changed, requiring a fix in the g.py script.

## 0what.py

The 0what.py script can be run with the argument `.` and you'll get a short description of each
python file in the current directory.  These will be organized by categories.

## 0test.py

This script will run the self tests of the files.  The tests are either in the module's file or are
located in the /plib/test directory.  Each module file has a special trigger string (see
`trigger.py`) that tells `0test.py` how to run its tests.  If you run `python 0test.py`, you'll get
a summary report of passes and failures.  Only failed tests will print out messages.  Use the -v
option to see each test's output.  The default output tells you the files that fail self-tests and
need to be worked on.


## Assert()

I use this function in lwtest.py a lot while writing code because I set the Assert environment
variable to a nonempty string, causing this function to drop into the debugger when its argument is
False.  I use it to evaluate incoming parameters or invariants in a function.  When the debugger is
called, you enter "up" to go to the line that had the problem, letting you figure out what went
wrong.

# Most useful

Here are a few of the modules/scripts I use a lot or provide useful techniques.

* get.py
    - Get text, lines, tokens, words, binary content, etc. from files.  I use GetLines and
      GetTextLines the most.

* util.py
    - Numerous utility functions.

* pgm/prun.py
    - I use this to develop python scripts in a terminal window.  When the script's modification
      time changes by saving the script in the editor window (a different terminal window), the
      script is run, allowing you to see the results without leaving your editor window.  This is
      handy when using short output messages when debugging functionality, as you can see
      everything on the screen.  It also has an option to launch a browser showing you a diff of
      the previous and latest outputs so you can see what changed.

* color.py
    - Contains three key classes (Color, Trm, and ColorName) to deal with color definitions and
      generating escape codes for using color in text in output to a terminal.  This file went
      through a large revision in March/April 2022, as I changed the design from something I had
      been using for a couple of decades (it was renamed `kolor.py` and will eventually be
      removed).  I included support for the old design, as it was used in about 80 files in this
      directory tree.  I'll slowly convert things over to the new file and delete the legacy stuff.  
    - A handy utility that uses `color.py` is `cdec.py`, which will decorate lines of a file with
      color specifiers, so you see the line in its specified color.  Try 'python cdec.py
      colornames0' and you'll see a demo.  The colornames0 is my default set of colors with naming
      based on the 3 letter names of the resistor color code.  Run `color.py` as a script to see
      the colors and add the `a` argument to see the styles.  I use the mintty terminal under
      cygwin, which uses 24-bit color and provides Unicode support.

* lwtest.py
    - Lightweight test runner adapted from a nice tool by Raymond Hettinger.  I use this for
      testing of my python modules.  I don't like python's unittest module because it intercepts
      the standard streams, so you can't introduce breakpoints to see what is happening (or I'm
      ignorant of a suitable method).  I liked nose and pytest, but I wanted to minimize
      dependencies, so I rolled my own. 

* f.py
    - Provides flt and cpx types, derived from float and complex, respectively.  Their advantage is
      that they only show 3 significant figures by default, stopping digit diarrhea with the usual
      float or complex calculations.  This file is still under development -- but I use the flt()
      objects a lot for routine calculations because they are so convenient for calculating things
      based on measurements.  

* prob.py
    - Provides cumulative distribution functions and their inverses for common statistical tests.
      This module calls into a DLL made from S. Moshier's cephes library functions in C for the
      mathematical functions using python's ctypes module. 

* matrix.py
    - While numpy provides matrices, it's occasionally nice to have a pure-python module to deal
      with matrices.  The `matrix.py` module is derived from a public domain lightweight matrix
      module (version 3.0.0 of pymatrix gotten on 15 Jul 2019).  The module lets you put into a
      matrix anything that can be put into a list (the implementation uses nested lists).  mpmath
      supplies matrices based on dictionaries (great for sparse matrices), so that's an
      alternative.  mpmath.iv includes matrices that use mpmath.mpi interval numbers, which are
      handy for quantifying roundoff issues in matrix calculations.

* pgm/uni.py
    - This is a script that allows you to look up Unicode characters, either by codepoint string or
      looking for a particular string in the character's description.  I use this script a lot when
      writing scripts and working in a terminal.

* pgm/goto.py
    - This script keeps track of strings and lets you find them by either typing in their number
      from a list or using a short alias.  I use this to keep track of directories, project files,
      videos, and a bunch of other stuff.  One of the hidden benefits is that the datafile used for
      the projects, directories, etc. can have a line commented out, meaning you'll be able to
      remember where the directory/project is years later.  My computer has around 2 million files
      and it's impossible to remember where everything is.  I wrote this before I retired a couple
      of decades ago and a number of friends at work told me they couldn't live without the script.
      I use it constantly at the command line.

# Lessons

Two core lessons I have to learn over and over again are 

* Document your data structures in detail
* Find someway to index that large list of documents you'll write over time: what they do and where
  they are.
