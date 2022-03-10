# plib

## Status

I made this repository public on 7 Mar 2022.  I'll slowly add to it over
time and fix/maintain some of the stuff.  My intent is that this stuff will
remain here for a few years after I've died or when I turn its maintenance
over to a friend who said he'd be the caretaker.  By then any content of
interest to others will probably have made its way out into the world.

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

This is a work-in-progress.  Currently, a few tests fail in /plib.  Most of
the scripts in /plib/pgm don't have suitable 'what' strings (see 0what.py
below), so you'll have to look at the code to see what they do.
Eventually, all the 'what' strings will be filled out, as I can't remember
what all this stuff does myself.

As of this writing (March 2022), this stuff has been tested with python
3.7.12 in a cygwin environment on Windows 10.

My coding style is vertically compressed which most folks won't like.  Use
a style formatter to to recover more normal vertical formatting if you
wish.  I use pgm/rpl.py to remove blank lines so I can see as much as
possible on my screen.  I use a folding editor, which folds on indentation
and explains the use of 'if 1:  # Comment' "sections".  A completely folded
file should be viewable in a few tens of lines.

My editor has commands to go to the next paragraph, which is defined by a
bare newline.  With no blank lines in a file, this lets me set up
"bookmarks" by inserting an empty line.  I can then jump between two areas
in a file with one key press, which is fast and efficient.  It's faster
than using stored bookmarks or multiple tab pages.

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

This list a few of the modules/scripts I us a lot.

* pgm/prun.py
    - I use this to develop python scripts in a terminal window .  When the
      script's modification time changes by saving the script in the editor
      window (a diffent terminal window), the script is run, allowing you
      to see the results without leaving your editor window.  This is handy
      when using short output messages when debugging functionality, as you
      can see everything on the screen.  It also has an option to launch a
      browser showing you a diff of the previous and latest outputs so you
      can see what changed.

* clr.py
    - Generates ANSI escape codes to color text in terminal output.
      Contains two functions to highlight matches in regular expressions,
      which helps to develop regular expressions more quickly.  Use prun.py
      to make it even faster.  This is for POSIX machines like cygwin/bash,
      MacOS, and Linux.  If you're on Windows, there's already a library to
      help with getting colored output in DOS terminal windows (it works by
      making calls to the Windows DLL rather than emitting escape codes).

* lwtest.py
    - Lightweight test runner adapted from a nice tool by Raymond
      Hettinger.  I use this for all testing of python scripts.

* f.py
    - Provides flt and cpx types, derived from float and complex,
      respectively.  Their advantage is that they only show 3 significant
      figures by default, stopping the typical digit diarrhea with the
      usual float or complex calculations.  This file is still under
      development -- but I use the flt() objects a lot for routine
      calculations because they are so convenient.  I'd like to get them
      fully functional with physical units too, but this is a more
      challenging task.  See them used in pgm/repl.py, a REPL (read,
      evaluate, print, loop) that replaces the standard python REPL and is
      my interactive python calculator.  Uses f.py for floats and complex
      numbers and has math and cmath symbols in scope.  flt and cpx numbers
      are printed out in color to help identify the types.

# Feedback

If you find a bug or want to suggest an improvement, my email address is in
each file.  Send me an email with the subject `Github plib repository` in
the subject.
