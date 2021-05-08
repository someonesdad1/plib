# plib

This repository is a collection of python stuff I've written.  Feel free
to browse and use what suits your needs.  There are quite a few files,
peruse the tools (see below) to help understand what these files are
for.

The general organization is that the root directory holds modules that
are mostly intended to be imported into other scripts.

The `pgm` directory holds scripts that are separate programs.  The
`test` directory holds files that test the modules.

# Conventions

## Python version

The python files are intended to be used with python 3.  If a particular
python 3 version has been used to test everything and all the tests
passed, then a git tag is used to indicate a repository state where
those tests passed.  It will be an annotated tag with a name something
like 'Tested_python3.7.7_21May2021'.

I started working on building this repository in May of 2021 and my
current python version is 3.7.7, so that's what things will be tested
with.

## Encoding

If you run the UNIX command 'file' on the python files, it should tell
you it's either ASCII text or UTF-8 encoded text.  A file will only be
UTF-8 if it includes non-7-bit Unicode characters.

# Tools

## what.py

The what.py script can be run with the argument 'all' and you'll get
a short description of each python file.  These will be organized by 
topical categories, such as 'programming', 'utility', 'science', 
'math', 'shop', etc.  You can also see this description by providing the
file name to the command line of `what.py`.

## 0test.py

This script will run the self tests of the files.  The tests are either
in the module file or are located in the test directory.  Each module
file has a special string that tells 0test.py how to run its tests.  You
can run all the tests by using the -a option or just pass the files you
want to test on the command line.

## Module features

Some of the modules use the `template.py` file, which provides a user
interface, example output, and self-test facilities.  These scripts
should have the options

>  --example   Show examples of module's output
>  --test      Run internal self tests
>  --Test f    Run external regression test file f
>  --what      Brief descript of module's purpose

This is true even for the files that are intended to be modules that you
import.

# Python 2

A number of these modules and files once supported python 2.7.  However, I
have changed these files to work only on python 3.  If the file doesn't
use many f-strings and "looks" like older code, you might be able to get
things running under python 2.7 by adding a line like:

    from __future__ import print_function, division 

and hacking on the syntax errors.  If you really need python 2.7
functionality and can't get things working, take a look at
https://pypi.org/project/six/, which might provide some help.

# Feedback

If you find a bug or want to suggest an improvement, my email
address is in each file.  Send me an email with the subject `Github
plib repository` in the subject.
