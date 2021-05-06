# plib

This repository is a collection of python stuff I've written.  Feel
free to browse and use what suits your needs.  There are numerous
files, so there are tools to help understand what these files are
for.

# Tools

## what.py

The what.py script can be run with the argument 'all' and you'll get
a short description of each python file.  These will be organized by 
topical categories, such as 'programming', 'utility', 'science', 
'math', 'shop', etc.  You can also see this description by providing the
file name to the command line of `what.py`.

## Script features

Each of the scripts should use the `template.py` file, which provides 
a user interface, example output, and self-test facilities.  These
scripts should have the options

>  --example   Show examples of module's output
>  --test      Run internal self tests
>  --Test f    Run external regression test file f
>  --what      Brief descript of module's purpose

This is true even for the files that are intended to be modules that you
impport.

# Feedback

If you find a bug or want to suggest an improvement, my email
address is in each file.  Send me an email with the submect "Github
plib repository" in the subject.
