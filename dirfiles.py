'''
 
Module to get a set of files from a set of disjoint directory trees.
 
'''
 
# Copyright (C) 2020 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Academic Free License version 3.0.
# See http://opensource.org/licenses/AFL-3.0.
#
 
import pathlib
import re

class Dirfiles(object):
    '''Construct a set with file names or directory names from one or
    more directory trees.  The methods add(), keep(), keepext(), rm(),
    and rmr() are used to modify the set of files local to the instance.
    When the instance is finished processing, use the update() method to
    add the local files to the class variable Dirfiles.files set.  
 
    You can use multiple instances to process different trees or one
    instance.  To use one instance, use update() as needed, then set a
    new directory with the dir attribute.
 
    To start with an empty Dirfiles.files set, use the clear() method on
    an instance or set the clear keyword in the constructor set to True.
 
    Note that different threads from the same process have access to the
    same Dirfiles.files class variable.
 
    An example use case for this object is to generate a set of PDF files
    in various locations.  Suppose you wanted to collect the PDF files
    from the directory trees /tree1, /tree2/branch3, and /tree3.  The
    following code would do it:
        d = Dirfiles(".", clear=True)
        for dir in "/tree1 /tree2/branch3 /tree3".split():
            d.dir = dir
            d.add("**/*.pdf")
            d.update()
        # Now Dirfiles.files contains all the PDF files of interest.
 
    Example usage to find files
        d = Dirfiles("/ebooks", clear=True)
        d.add("chemistry", "math")      # Add files from two directories
        # Remove a particular file
        d.rm("chemistry/The_standard_formulary.pdf")
        # Remove a directory and its files
        d.rm("math/slide_rule/")
        # Remove all jpg files
        d.rm("jpg$")
        # Remove all jpg, JPG, Jpg, ... files by ignoring case.  Note
        # the need for using a regular expression and anchoring it at
        # the end of the file name.
        d.rmr(r"\.jpg$", ic=True)
 
        # At any time, you can get a copy of the set of files in the
        # instance by using the get property.
        file_set = d.get
 
        # To use the Dirfile.files set along with the current instance's
        # files, use the property get_all, which returns a copy of the
        # two sets.
        files = d.get_all
        # After using either .get or .get_all, you can continued to add
        # more files to the instance.
 
        # To start over with a new set of files, call clear().  This
        # sets Dirfiles.file and the instance's set of files to empty.
            *** CAUTION:  it does NOT set the files attribute of other
                instances to empty. ***
        d.clear()
 
        # To finish with the current directory, move the instance files
        # to Dirfiles.files and use the dir property to set a new
        # directory.
        d.update()
        d.dir = "/manuals"
 
    Getting directories (use getdirs in constructor)
        d = Dirfiles("/ebooks", clear=True, getdirs=True)
       ==> Now all entries in Dirfiles.files will be directory names
 
    Suppose we want to have a list of all the files at and below the
    directory dir with extensions png, jpg, and bmp directory.
        d = Dirfiles(dir)
        d.add("**/*")              # Add all files
        # Only keep the files of interest
        d.keep(r"\.png$", r"\.jpg$", r"\.bmp$", ic=True)
    Since this is a common pattern, it can also be done with 
        d.keepext(*"png jpg bmp".split(), ic=True)
    Here's how to do it just for the files in the dir directory:
        d = Dirfiles(dir)
        d.add("*")
        d.keepext(*"png jpg bmp".split(), ic=True)
 
    However, the above methods with keep() are inefficient because all
    files needs to be read in first.  Do it more efficiently with
    globbing:
        d = Dirfiles(dir)
        ext = "png jpg bmp".split()
        d.add(*[f"**/*.{i}" for i in ext])
 
    The containers for files are:
 
        Dirfiles.files(set) (class variable)
               |
               |- instance0.files(set)
               |- instance1.files(set)
               |- instance2.files(set)
               etc.
    When update() is called on an instanceX, the files in instanceX.files
    are transferred to the Dirfiles.files set and the instanceX's files
    set is emptied.
    '''
    files = set()   # Container for all files 
    def __init__(self, dir, clear=False, getdirs=False, ignore_repo=True):
        '''If getdirs is True, then we get directory names, not files.
        If ignore_repo is True, ignore directories like .git and .hg.
        '''
        if clear:
            Dirfiles.files.clear()
        self.ignore_repo = ignore_repo
        self.repo_re = re.compile(r"\.hg/|\.hg$|\.git/|.git$")
        self.getdirs = getdirs
        self.dir = dir
    def __str__(self):
        return f"Dirfiles({self.size} local, {len(Dirfiles.files)} total)"
    def __repr__(self):
        return str(self)
    @property
    def size(self):
        return len(self.files)
    @property
    def dir(self):
        return self._dir
    @dir.setter
    def dir(self, newdir):
        '''Set a new directory.  This clears the local file set.
        '''
        self._dir = newdir
        self.p = pathlib.Path(newdir)
        self.files = set()
    @property
    def get(self):
        '''Returns a copy of the instance's set of files.
        '''
        return self.files.copy()
    @property
    def get_all(self):
        '''Returns a copy of the set containing Dirfiles.files and the
        current local set of files.  Changes neither Dirfiles.files nor
        self.files.
        '''
        f = self.get
        f.update(Dirfiles.files)
        return f
    def clear(self):
        'Remove all files from the set.'
        self.files.clear()
        Dirfiles.files.clear()
    def update(self):
        '''Add instance's files to Dirfiles.files.  This operation is
        not reversible, so if you need to remove certain local files, do
        it before calling update().
        '''
        Dirfiles.files.update(self.files)
        self.files = set()
    def keepext(self, *extensions, **kw):
        '''Keep only those files with the indicated extensions.
        '''
        ic = kw.get("ic", False)
        ext = [rf"\.{i}$" for i in extensions]
        self.keep(*ext, ic=ic)
    def keep(self, *regexps, **kw):
        '''Keep only the items that match the regular expressions.  Set
        the ic keyword to True to ignore case.
        '''
        ic = kw.get("ic", False)
        keep = []
        for regex in regexps:
            r = re.compile(regex, re.I) if ic else re.compile(regex)
            for elem in self.files:
                mo = r.search(str(elem))
                if mo:
                    keep.append(elem)
        self.files = set(keep)
    def rmr(self, *regexps, **kw):
        '''Remove local items that contain the indicated regular
        expressions.  Set the ic keyword to True to ignore case.
        Returns the number of files removed.
        '''
        ic = kw.get("ic", False)
        remove, count = [], 0
        for regex in regexps:
            r = re.compile(regex, re.I) if ic else re.compile(regex)
            for elem in self.files:
                mo = r.search(str(elem))
                if mo:
                    remove.append(elem)
        for elem in remove:
            self.files.discard(elem)
        return len(remove)
    def rm(self, *items, **kw):
        '''Remove local items that contain the indicated strings.  Be
        careful with this tool, as it can remove more than you intended
        if you give it short strings.  You can be more specific with rmr().
 
        To remove exactly what you want, set the keyword exact to True;
        then an item is removed only if the string matches exactly.
 
        Returns the number of files removed.
        '''
        exact = kw.get("exact", False)
        remove = []
        for item in items:
            for elem in self.files:
                if item in str(elem):
                    if exact:
                        if item == str(elem):
                            remove.append(elem)
                    else:
                        remove.append(elem)
        for elem in remove:
            self.files.discard(elem)
        return len(remove)
    def add(self, *items, **kw):
        '''Add directories and files.  All files under a directory
        are added unless the item contains a globbing character.  A
        ValueError exception will be raised if an item doesn't exist; 
        to ignore when it doesn't exist, set the keyword ignore to True.
 
        The various items are:
            directory
                Adds all files recursively under the directory unless the 
                string contains a globbing character.
            **/*
                Adds all files at and below the current directory.
            *.odt
                Add all files ending in '.odt' in the current directory.
            **/*.odt
                Add all files ending in '.odt' at and below the current
                directory.
            examples/**/*.odt
                Add all files ending in '.odt' in the examples directory
                and below.
            examples/example.odt
                Add just this file.
        '''
        def is_not_repo(x):
            '''x is a pathlib.Path object.  Return True if x is not a
            revision control repository like .git or .hg and
            self.ignore_repo is True.  If self.ignore_repo is False,
            return False so that all files/directories are included.
            '''
            is_repo = bool(self.repo_re.search(str(x)))
            if self.ignore_repo:
                return not is_repo
            else:
                return True
        ignore = kw.get("ignore", False)
        for item in items:
            if "*" in item or "?" in item or "[" in item:
                if self.getdirs:
                    s = [i for i in self.p.glob(item) if i.is_dir()]
                else:
                    s = [i for i in self.p.glob(item) if i.is_file()]
                self.files.update(set(filter(is_not_repo, s)))
            else:
                f = self.p/item
                if f.exists():
                    if self.getdirs and f.is_dir():
                        self.files.add(f)
                    else:
                        if f.is_dir():
                            # Get all files under this directory
                            self.files.update(filter(is_not_repo, f.glob("**/*")))
                        elif f.is_file():
                            if is_not_repo(f):
                                self.files.add(f)
                        elif not ignore:
                            raise ValueError(f"'{item}' not a file or directory")
                else:
                    raise ValueError(f"'{item}' unrecognized")

