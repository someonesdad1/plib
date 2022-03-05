# plib

This repository is a collection of python stuff I've written from 1998 on.
Feel free to browse and use what suits your needs.  There are quite a few
files, use the tools (see below) to help understand what these files are
for.  Most of the stuff is licensed under the Open Software License version
3.0.

* The `plib` directory holds modules that are intended to be used by other
  scripts.
* The `pgm` directory holds scripts that are separate programs.
* The `test` directory holds scripts that test the modules in `plib`.

# Python

As of this writing (March 2022), this stuff has been tested with python 3.7
in a cygwin environment on Windows 10.  I quit supporting and using python
2.7 about a decade ago, although many of the scripts in /plib/pgm were
first developed as python 2 applications.

In 2022, I'm tentatively planning to move to a different development
machine (a MacBook), then upgrade the old Windows box to a late version of
Windows 10 or 11 and load the Windows Subsystem for Linux.  Then I should
have the ability to develop and test these python scripts on
Mac/Windows/Linux boxes.

My coding style is vertically compressed; use a formatter like black
(https://github.com/psf/black) to recover more normal vertical formatting.
I use 'black -S -l 75' to format, followed by the script pgm/rbl.py to
remove the blank lines.

# Tools

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

# Most useful

This list contains the things I us a lot.

* pgm/prun.py
    - I use this to develop python scripts.  When the script's modification
      time changes by saving the script in the editor window, the script is
      run, allowing you to see the results without leaving your editor
      window.  
* clr.py
    - Generates ANSI escape codes to color text in terminal output.
      Contains two functions to highlight matches in regular expressions,
      which helps develop them more quickly.  Use prun.py to make it even
      faster.
* lwtest.py
    - Lightweight test runner adapted from a nice tool by Raymond
      Hettinger.  I use this for all testing of python scripts.
* f.py
    - Provides flt and cpx types, derived from float and complex,
      respectively.  Their advantage is that they only show 3 significant
      figures by default, stopping the typical digit diarrhea with usual
      float or complex calculations.  This file is still under development,
      but I use the flt() objects a lot for routine calculations because
      they are so convenient.  I'd like to get them fully functional with
      physical units too, but this is a more challenging task.
* repl.py
    - A REPL (read, evaluate, print, loop) that replaces the standard
      python REPL and is my interactive python calculator.  Uses f.py for
      floats and complex numbers and has math and cmath symbols in scope.
      I also import the python uncertainties library and the u.py module,
      so physical calculations using units and uncertainties can be done.
      In a UNIX-like environment, you have history and command line
      completion.  flt and cpx numbers are printed out in color to help
      identify the types.

# Feedback

If you find a bug or want to suggest an improvement, my email address is in
each file.  Send me an email with the subject `Github plib repository` in
the subject.
