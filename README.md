# plib

This repository is a collection of python stuff I've written from 1998 on.
Feel free to browse and use what suits your needs.  There are quite a few
files, use the tools (see below) to help understand what these files are
for.  Most of the stuff is licensed under the Open Software License version
3.0.

* The `plib` directory holds modules that are intended to be used by other
  scripts.
* The `pgm` directory holds scripts that are separate programs.
* The `test` directory holds scripts that test the modules.

# Conventions

## Python version

The python files are intended to be used with python 3.  I started working
on building this repository in May of 2021 and my current python version is
3.7.10, so that's what things were tested with.

## Coding style

You will probably not like my coding style because I vertically compress
things as much as possible by removing all blank lines.  This is because
screen vertical real estate is the most precious resource.  Because of the
editor I use, I can use this compressed form comfortably (it's a folding
editor and I fold on indentation).  I can usually see the whole file's
contents when it's folded in a few tens of lines, which makes navigation
easy (the 'if 1:' lines cause the folding and the comments give the section
a name).  Since this will probably bug most people, you can use a code
formatter to put things back to a more conventional form.  Except for this
vertical compression, I mostly follow the formatting guidelines of PEP-8
(see https://www.python.org/dev/peps/pep-0008/).

An advantage of this vertically compressed form is that I can insert a
single blank line where I'm working in the file.  The editor I use has
commands to move to the next or previous paragraph, which is an empty line.
Thus, I can fold the text, go to another section and look at the code, then
get back to my working spot with one key press without having to e.g.
remember a position or assign a location.  It's very efficient.  To jump
between the two sections, I insert another blank line.  This is faster than
switching to another tab page (in my editor, the former takes one keystroke
and switching tab pages takes two).

In Feb 2022, I added a second 24 inch monitor, so now I use two 4k
monitors.  One of these is in portrait mode, giving me a long editor window
that has 80 to 160 lines, depending on the magnification.  This allows for
comfortable editing sessions.  This portrait monitor is also nice for web
browsing catalog pages.

# Environment

I work in a cygwin environment on a Windows computer, so most of this stuff
is organized around a POSIX environment.  In particular, I spend most of my
day in bash shell windows, using an editor and running python scripts.
Many of the scripts use the ANSI escape sequences provided by the color.py
module.  I originally developed this on a Linux box, then adapted it to
work under cygwin.  In March 2022, I wrote the clr.py module, a replacement
for the aging color module.  The clr.py module works with mintty under
cygwin (an excellent 24-bit color terminal emulator) and on the Mac's
Terminal.app, an 8-bit color emulator.

The scripts are also heavily biased towards POSIX-style paths.

# Tools

## 0what.py

The 0what.py script can be run with the arguments `*.py` and you'll get
a short description of each python file.  These will be organized by 
topical categories, such as 'programming', 'utility', 'science', 
'math', 'shop', etc.  This will help you understand the purpose of each of
the files.

## 0test.py

This script will run the self tests of the files.  The tests are either
in the module file or are located in the test directory.  Each module
file has a special string that tells 0test.py how to run its tests.
If you run 'python 0test.py', you'll get a summary report of passes and
failures.  Only failed tests will print out messages.  Use the -v option
to see each test's output.  Use -V to also see the files that weren't
run because they don't have an associated test.

# History

Many of the copyright strings in these files are 2014.  That was the year I
translated many hundreds (actually, over a thousand) of my python scripts
written from 1998 on to python 3; many of the scripts didn't have dates in
them, so they got copyrighted in 2014.

# Feedback

If you find a bug or want to suggest an improvement, my email address is in
each file.  Send me an email with the subject `Github plib repository` in
the subject.
