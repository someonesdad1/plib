# plib

This repository is a collection of python stuff I've written from 1998
on.  Feel free to browse and use what suits your needs.  There are quite
a few files, use the tools (see below) to help understand what these
files are for.  Most of the stuff is licensed under the Open Software
License version 3.0.

* The `plib` directory holds modules that are intended to be used by
  other scripts.
* The `pgm` directory holds scripts that are separate programs.
* The `test` directory holds scripts that test the modules.

# Conventions

## Python version

The python files are intended to be used with python 3.  If a particular
python 3 version has been used to test everything and all the tests
passed, then a git tag is used to indicate a repository state where
those tests passed.  It will be an annotated tag with a name something
like 'Tested_python3.7.10_16Jun2021'.

I started working on building this repository in May of 2021 and my
current python version is 3.7.10, so that's what things will be tested
with.

## Coding style

It is likely you will not like my coding style, as I vertically compress
things as much as possible.  This is because screen vertical real estate
is the most precious resource.  Because of the editor I use, I can use
this compressed form comfortably (it's a folding editor).  I can usually
see the whole file's contents when folded in 20 to 30 lines, which makes
navigation easy (the 'if 1:' lines cause the folding and the comments
give the section a name).  Since this will bug most people, it's not
hard to get a code formatter to put things back to a more conventional
form.  Otherwise, I mostly follow the formatting guidelines of PEP-8 (see
https://www.python.org/dev/peps/pep-0008/).

One great advantage of this vertically compressed form is that I can
insert a single blank line where I'm working in the file.  The editor I
use has commands to move to the next or previous paragraph, which is
usually a blank line.  Thus, I can fold the text, go to another section
and look at the code, then get back to my working spot with one key
press.  It's very efficient.  To jump between two different sections,
insert blank lines at each position.

# Tools

## 0what.py

The 0what.py script can be run with the argument 'all' and you'll get
a short description of each python file.  These will be organized by 
topical categories, such as 'programming', 'utility', 'science', 
'math', 'shop', etc.  You can also see this description by providing the
file name to the command line of `what.py`.

## 0test.py

This script will run the self tests of the files.  The tests are either
in the module file or are located in the test directory.  Each module
file has a special string that tells 0test.py how to run its tests.
If you run 'python 0test.py', you'll get a summary report of passes and
failures.  Only failed tests will print out messages.  Use the -v option
to see each test's output.  Use -V to also see the files that weren't
run because they don't have an associated test.

# History

I spent 25 years at HP as an R&D scientist at an HP site in the
northwest US.  The first half of my time at HP was in thin film stuff
and the second half I worked as a software engineer (I retired from HP
in 2002).  In 1998, our software team was disbanded and each of us
needed to find another position on site.  It took me two months to find
another group and most of that time was spent at my desk learning new
tools because interviews were infrequent (HP management was really good
about helping experienced senior folks find new positions).  I spent
some time learning perl because I liked its power, but came to dislike
its syntax.  I then tried python and immediately liked it because it was
so C-like and easy to use (I was writing useful scripts in an hour by
reading the excellent tutorial).  Python has been my favorite
programming language since then.

# Feedback

If you find a bug or want to suggest an improvement, my email
address is in each file.  Send me an email with the subject `Github
plib repository` in the subject.
