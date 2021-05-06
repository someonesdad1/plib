# plib

Last update: 4 May 2021 

Rationale & Organization

    This repository is a collection of python stuff I use.  I've had the
    directory /pylib on my system since before 2000 that contains many of
    the python scripts and modules I've written.  They starte out written 
    for python 2 versions, which looks quaint and ugly today, but was still
    providing useful functionality.  Around 2014 I spent weeks migrating
    virtually all of that code so that it would work on python 3.  After
    about 2016, I stopped bothering to make things work on python 2.  

    As of May 2021, there are more than 1200 python modules and scripts in
    /pylib.  I can't remember most of them.

    My reasons in moving this stuff to github were 1) to have a backup in the
    cloud and 2) let others access this stuff.  Some of my objectives are:

        * Move the core /pylib stuff to /plib.  Here, "core" means it gets
        used on my system often enough that I'd feel pain without it.

        * Create /plib/old to contain older or less-used stuff.

        * Create /plib/pgm to contain python scripts I find useful.

    For the last decade or two, I've populated /pylib/test with the test
    scripts that provide the tests for the modules in /pylib.  Recently
    I decided I didn't like this approach, primarily because the code and
    its test code were then separated.  Sometimes that makes sense, but most
    of the time it's more sensible to have everything in one place.

    I've written a python file called template.py which will let /plib be
    populated by both functioning scripts and modules.  This template
    allows:
        
        * Self test code to be included in the file.  It uses my lwtest.py 
        lightweight test runner to run the self tests.

        * The lwtest.py functionality also allows generation of output
        examples for people who want to use the module's functionality.

        * It lets the file act as a normal script rather than a module if
        desired.

        * In fact, it's a common pattern to write a module for other
        programs' use and also make a utility from the module.

    It will take time to move the self tests and examples to the modules, as
    it is also an opportunity to inspect the code and refactor it to use the
    more recent python 3 standard libraries.  I just did this today with a
    script that was a couple of decades old and it reduced the file's size
    by at least a factor of 2.

Code style

    My standard for python code is similar to PEP8, except I like to jam
    everything together vertically because I'd much rather be able to
    see hundreds of lines on the screen if could (some day I'll get a
    second monitor and turn it vertically for editing code files).  I
    also limit things to 80 columns because I've been using that
    convention for decades.  The vertical compression is easy for me to
    deal with because I use a folding editor and the syntax coloring
    makes it easier to sort things out.  

        Another reason for the vertical compression is that I'll put at
        least one space on every "blank" line.  This lets me use my
        editor's navigation tool that goes to the next block as
        indicated by a blank line.  Since everything is compressed or
        there are no truly blank lines, this editor operator lets me
        navigate to exactly what I'm working on in a file without having
        to insert any extraneous symbols/tags.

    If you my style annoying, run the code though a code formatting tool
    like yapf, black, autopep8, etc.

    You'll also see me put blocks of code surrounded by an 'if 1:'
    block.  I do this on code I look at a lot so that the whole file can
    be shown in about 25-30 lines when folded.  The comments on the 'if'
    statement hint at the organization.

Licensing

    This is all open source code and, in general, it will be under
    either the AFL3 or the OSL3.  Each file/module will have a short
    license statement in it.

Feedback

    If you find a bug or want to suggest an improvement, my email
    address is in the file.  Send me an email with the submect "Github
    plib repository" in the subject.
