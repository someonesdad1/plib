# plib

This repository is a collection of python stuff I've written.  Feel free
to browse and use what suits your needs.  There are quite a few files,
use the tools (see below) to help understand what these files are
for.

The general organization is that the root directory holds modules that
are mostly intended to be imported into other scripts.

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
file has a special string that tells 0test.py how to run its tests.
If you run 'python 0test.py', you'll get a summary report of passes and
failures.  Only failed tests will print out messages.  Use the -v option
to see each test's output.  Use -V to also see the files that weren't
run because they don't have an associated test.

# Feedback

If you find a bug or want to suggest an improvement, my email
address is in each file.  Send me an email with the subject `Github
plib repository` in the subject.
