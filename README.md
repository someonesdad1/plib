# plib

# /plib vision

- Strategic
    - Move to a clean "import math" and "math.pi" usage in my python files.  Avoid "from
      x import y", which has higher risk of circular imports.  Minimize my definitions
      of import symbols.
    - /plib/tests will hold module tests
    - Makefile to help with testing/checking
        - 'make' prints key targets to use:
            - 'make check':  lints & type checks
            - 'make lint':  lints
            - 'make type':  type checking
            - 'make test':  run selftests
            - 'make fix':  run ruff to safely fix imports and syntax
            - 'make clean':  remove cache files & other leftover stuff
        - Move "test" to "tests"
            - All self tests then run by 'make test' at top level, which simply cd's to
              tests and runs make or a testing script
        - Need to support 'make z'; this would cause the test of the current file in .z
          to be run
    - Move /plib/pgm to /pgm
        - Makes /plib a core set of python library files
    - Core library stuff is type annotated
        - Use TypeAlias to make things more readable
        - Type hints provide a "user manual" baked into the code
        - Document "why" via Annotated:
            - from typing import Annotated
            - Radians = Annotated[float, "Phase angle in radians"]
            - Uncertainty = Annotated[float, "Standard deviation"]
        - The strategic benefits of the typing are
            - A good name for the class/method tell you what it does
            - The types tell you what it takes and what it returns
            - You don't have to read the code to get the prior two things
    - Use __all__ to signal public/private
    - DEVELOPER.md file to indicate epochs of code development, where the legacy stuff
      is, and what's the core up-to-date stuff.

- Tactical
    - All my stuff moved to MIT license
    - gist in every file
    - As much as possible has tests
        - Speed up testing with multiple processes
        - OK to e.g. use dptest.py to manage all testing
    - Coalesce similar functionality into fewer files
        - dp*.py is useful naming pattern to avoid conflicts with other namespaces
    - Move numeric/textual data to ./data modules
    - HTML doc produced automatically; allows a new visitor to browse contents at a
      reasonably high level
        - docstrings for functions & classes can have a marker in them that can be used
          to produce the HTML documentation.  This should be a brief description of the
          symbol and what problem it solves.
    - pydoc works well on all symbols

- color
    - Coalesce everything into color.py

# 2026 /plib vision

- Consolidate into fewer files
- Module documentation
    - Better documentation of design decisions used in the module
    - Must have adequate docstrings for use with pydoc
    - Each module can have a --demo option that lets you get an overview of the features
      and see an example of each component.  The demo code could be put in /plib/data
      and the module would just launch it.
- Update self-tests and ensure they pass
- Remove specialized modules that are better stored elsewhere
- 0what.py returns useful output for all modules

# 2026 /plib work done

- 14 Mar
    - dp\*.py files linted
    - Policies
        - Never use 'from x import y'
        - All imports will be 'import x'
        - Occasional abbreviations:  'import numpy as np'
        - Rarely define symbols:  no 'import math' and 'pi = math.pi'.  The primary
          reason is the person reading the code doesn't have to figure out where the
          symbol came from.  I'll occasionally let lines become long to support this.
        - /plib has a makefile that will run lint & type checking
        - /plib/tests will receive all the tests for the modules
            - Cleaner
            - Easy to name
            - Reduces module size
            - Lets module's main code be run for a demo
-  3 Mar
    - New dp\*.py files constructed
        - Now can test these with 'for i in dp*.py; do p $i ; done'
    - Started large refactoring
        - Moved a lot of util.py's stuff moved to dpseq.py, dpstr.py, etc.
        - Then moved util.py to dputil.py
    - Moved pgm/lib.py to data/dp_lib_data.py, which now runs as a script and holds
      snippets; supports interactive browsing
    - Created data/CIE_xyz_1931_2deg.py, which prototypes having accessible data in the
      /plib/data directory.  It also shows why this delivery method is preferable, as
      the data source can be attributed and checked as necessary, particularly if it's
      from a website with the URL given like this CIE data.
    - Terminal color stuff moved out of color.py into trm.py.  This broke nearly
      everything, but it's a lot cleaner now -- and it works properly and supports the
      context manager protocol, allowing the concept of style containers that I've
      wanted for years.
- 21 Feb 
    - data/dpcolornames.py constructed, giving many colornames collected from the web
    - I standardized on a new set of short color names (see key 0 in
      data/dpcolornames.py)
    - color.py
        - Color constructor was documented and the self-tests were improved
        - The Color class now has ColorNameNormalize as a class method

- 13 Feb 
    - Have \_trm_proto.py working to make a Trm object a context manager (adds the style
      feature I've wanted) and fixes the .on problem.
- 8 Feb
    - pgm/todo.py written:  lists priority tasks in python scripts
    - constant.py updated; works nicely and is now part of my python boilerplate.  I
      plan for all modules/scripts to use it eventually.
- 7 Feb
    - gist added to all /plib/\*.py files and all of these files have:
        - Single line gist to summarize their behavior
        - Marked with todo string (∞∞) to things that need to be done
        - Have a how to test field (notest, run, or --test)
    - All files switched to MIT license

# Description

[plib](https://github.com/someonesdad1/plib)

This repository is a collection of python modules and scripts.

- `plib` has modules that are intended to be used by other scripts
- `plib/pgm` has scripts that are separate programs
- `plib/tests` has test scripts for modules that don't have their tests built in
- `plib/g` has a python graphics library that outputs PostScript
- `plib/doc` has things related to documentation
- `plib/lib` has things that support a few of the modules in `plib`

Click on the following links to get more information (**note:  this structure is planned but
not implemented yet**):

- [plib](doc/modules.html) Information on plib's modules
- [pgm](doc/pgm.html) Information on plib/pgm's scripts
- [lib](doc/lib.html) Information on plib/lib's content
- [roadmap](doc/roadmap.html) How I plan to change things in this repository

### Formatting

I don't follow some recommendations of PEP-8:

- I use no empty lines in files (regex ^$).  Any "blank lines" will be sequences of one
  or more space characters.  This is done to see as many lines in my editor as I can.
    - It also lets me insert an empty line to mark places where I'm working, as I can
      jump to them with one keystroke in either direction.
    - I use a folding editor and the 'if 1:  # Comment' lines provide a natural folding
      of the files.
- A formatter like black or ruff can badly screw up carefully formatted mathematical
  expressions.  It can take hours to fix the mess it can cause in complicated code.  It
  can literally turn something complicated but readable into something essentially
  incomprehensible.  This is the "foolish consistency" that PEP-8 was talking about.
  Most programmers don't write such stuff, so they don't feel the pain.  I haven't found
  a decent python formatter.  
    - I like ruff, but until the developers feel the pain of this math mangling, they
      won't change anything.  In my opinion, the best fix would probably be a way in
      the code to delineate a block to say "don't mess with the formatting of this
      block, but lint it all you want".

## Caution

- The set of files in this directory are a core set of python modules and scripts I've
  written over the years for my own use.  There's some useful functionality in here, but
  it's fairly tightly coupled.  This means if you find a script you like and want to
  move it somewhere else, you may find that it's dependent on a number of other modules.
  This will be annoying and maybe a lot of work to fix.  This repository on my system is
  `/plib` and my `PYTHONPATH` variable is `"/plib:/plib/g"`.  This repository is the
  only code I use outside of what's in the python distribution. 
- I work in a bash terminal and use the /plib/color.py module to provide ANSI escape
  sequences to colorize text output.  I used to provide -c options to turn on
  colorization in scripts, but today everything I do is in a 24-bit color terminal and
  the days of monochrome terminals are probably over, so I just put escape codes in
  everything now.  I've got an item on my todo list to fix this and it should happen in
  my reorganization/refactoring efforts in the first half of 2026.
- I make lots of checkins to git, but virtually never include a commit message.  Yes,
  this is horrible practice in an industrial environment where you work with lots of
  other folks.  If/when one or more people ever start helping to maintain this stuff,
  the commit messages will instantly get better.

# Tools

## PostScript drawing tool

The g.py and other files in the g directory are a python wrapper over PostScript for
making drawings.  I wrote it over Thanksgiving vacation in 2001 because there wasn't
anything available at the time to do such tasks.  It has been used for thousands of
tasks over that time with essentially no changes except for when python changed or an
external library changed, requiring a fix in the g.py script.  I'd like to update it to
use SVG, but writing such library code is a lot of work and I'm not sure it would be
worth the effort for the return.

## 0what.py

The 0what.py script can be run with the argument `.` and you'll get a short description
of each python file in the current directory.  These will be organized by categories.

## 0test.py

This script will run the self tests of the files.  The tests are either in the module's
file or are located in the /plib/test directory.  Each module file has a special trigger
string (see `trigger.py`) that tells `0test.py` how to run its tests.  If you run
`python 0test.py`, you'll get a summary report of passes and failures.  Only failed
tests will print out messages.  Use the -v option to see each test's output.  The
default output tells you the files that fail self-tests and need to be worked on.

## Assert()

I use this function in lwtest.py (see below) a lot while writing code because I set the
Assert environment variable to a nonempty string, causing this function to drop into the
debugger when its argument is False.  I use it to evaluate incoming parameters or
invariants in a function.  When the debugger is called, you enter "up" to go to the line
that had the problem, letting you figure out what went wrong.  lwtest.py in turn was
written because the standard testing framework in python intercepts the standard
streams, meaning you can't use the debugger.

# Most useful

Here are a few of the modules/scripts I use a lot or provide useful techniques.

- get.py
    - Get text, lines, tokens, words, binary content, etc. from files.  I use GetLines
      and GetTextLines the most.
    - tokenizer.py has a useful tokenizer that, unlike get.Tokenize(), has the line and
      column number in the input file where the token came from (this is useful for e.g.
      a spell checker, as the user can be told where the word is in a large input file).

- util.py
    - Numerous utility functions.

- pgm/prun.py
    - I use this to develop python scripts in a terminal window.  When the script's
      modification time changes by saving the script in the editor window (a different
      terminal window), the script is run, allowing you to see the results without
      leaving your editor window.  This is handy when using short output messages when
      debugging functionality, as you can see everything on the screen.  It also has an
      option to launch a browser showing you a diff of the previous and latest outputs
      so you can see what changed.

- color.py
    - Contains three key classes (Color, Trm, and ColorName) to deal with color
      definitions and generating escape codes for using color in text in output to a
      terminal.  This file went through a large revision in March/April 2022, as I
      changed the design from something I had been using for a couple of decades (it was
      renamed `kolor.py` and will eventually be removed).  I included support for the
      old design, as it was used in about 80 files in this directory tree.  I'll slowly
      convert things over to the new file and delete the legacy stuff.  
    - A handy utility that uses `color.py` is `cdec.py`, which will decorate lines of a
      file with color specifiers, so you see the line in its specified color.  Try
      'python /plib/pgm/cdec.py colornames0' and you'll see a demo.  The colornames0 is
      my default set of colors with naming based on the 3 letter names of the resistor
      color code.  Run `color.py` as a script to see the colors and add the `a` argument
      to see the styles.  I use both the mintty terminal under cygwin, which uses 24-bit
      color and provides Unicode support, and the not-quite-as-good Windows Terminal
      running bash under WSL.

- lwtest.py
    - Lightweight test runner adapted from a nice tool by Raymond Hettinger.  I use this
      for testing my python modules.  I don't like python's unittest module because
      it intercepts the standard streams, so you can't introduce breakpoints to see what
      is happening (or I'm ignorant of a suitable method).  I liked nose and pytest, but
      I wanted to minimize dependencies, so I rolled my own. 

- f.py
    - Provides flt and cpx types, derived from float and complex, respectively.  Their
      advantage is that they only show 3 significant figures by default, stopping digit
      diarrhea with the usual float or complex calculations.  This file is still under
      development -- but I use the flt() objects a lot for routine calculations because
      they are convenient for calculating things based on measurements.  

- matrix.py
    - While numpy provides matrices, it's occasionally nice to have a pure-python module
      to deal with matrices.  The `matrix.py` module is derived from a public domain
      lightweight matrix module (version 3.0.0 of pymatrix gotten on 15 Jul 2019).  The
      module lets you put into a matrix anything that can be put into a list (the
      implementation uses nested lists).  mpmath supplies matrices based on dictionaries
      (great for sparse matrices), so that's an alternative.  mpmath.iv includes
      matrices that use mpmath.mpi interval numbers, which are handy for quantifying
      roundoff issues in matrix calculations.

- pgm/uni.py
    - This is a script that allows you to look up Unicode characters, either by
      codepoint string or looking for a particular string in the character's
      description.  I use this script a lot when writing scripts and working in a
      terminal.

- pgm/goto.py
    - This script keeps track of strings and lets you find them by either typing in
      their number from a list or using a short alias.  I use this to keep track of
      directories, project files, videos, and a bunch of other stuff.  One of the hidden
      benefits is that the datafile used for the projects, directories, etc. can have a
      line commented out, meaning you'll be able to remember where the directory/project
      is years later.  My computer has around 2 million files and it's impossible to
      remember where everything is (even if I wasn't chronologically gifted).

