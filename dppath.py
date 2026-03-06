'''
Path utilities
    RemoveDirs      Remove directories from a sequence that match a pattern
    RemoveFiles     Remove filenames from a sequence that match a pattern
    RemoveVCDir     Remove version control directories
    Get             Get all files and directories
    GetFiles        Return a recursive list of files
    GetDirs         Return a recursive list of directories
    KeepOnlyDirs    Keep only the directories in a list
    KeepOnlyFiles   Keep only the files in a list
    IsVCDir         Return True if dir is a version control directory
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Path utilities (all paths are pathlib.Path objects) oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2021 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ run oo>
        <oo todo - Move dirfiles.py stuff here oo>
    '''
    if 1:  # Imports
        from collections import deque
        import pathlib
        import re
    if 1:  # Custom imports
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        P = pathlib.Path
if 1:  # Core functionality 
    def Remove(pathseq, match=[], search=[], ic=False, dir=False):
        '''Return the items in the sequence pathseq of pathlib.Path objects
        with the patterns in the lists match and search removed.  Those in
        match must match fully and those in search can match anywhere in the
        path's components.  The patterns are strings and are compiled with
        re.compile().  If ic is True, then they are compiled with re.I to
        ignore case.  A path is removed in pathseq if any match or search
        pattern is a match.  Do not include '^' or '$' anchors in the match
        strings because they will be added.  The matching/searching is only
        done on the directory components of the items in pathseq if dir is
        True; otherwise, the matching is on the file name component only.
        
        '''
        if not match and not search:
            return pathseq
        # Build our regular expressions
        M, S = "", ""
        if match:
            a = []
            for i in match:
                a.append(f"^{i}$")
            M = re.compile("|".join(a), re.I if ic else 0)
        if search:
            a = []
            S = re.compile("|".join(search), re.I if ic else 0)
        input, output = deque(pathseq), deque()
        # Process the sequence
        while input:
            p = input.popleft()
            if not isinstance(p, P):
                raise ValueError(f"'{p}' is not a pathlib.Path object")
            p = p.resolve()
            if dir:
                parts = p.parts[:-1] if p.is_file() else p.parts
            else:
                if p.is_dir():
                    continue
                parts = [p.parts[-1]]  # File name portion
            if M:
                found = False
                for part in parts:
                    if M.match(part):
                        found = True
                        break
                if found:
                    continue
            if S:
                found = False
                for part in parts:
                    if S.search(part):
                        found = True
                        break
                if found:
                    continue
            output.append(p)
        return list(output)
    def RemoveDirs(pathseq, match=[], search=[], ic=False):
        "Remove directories using Remove()"
        return Remove(pathseq, match=match, search=search, ic=ic, dir=True)
    def RemoveVCDir(pathseq):
        "Remove git, Mercurial, Bazaar, and RCS directories"
        m = ["\\.git", "\\.hg", "\\.bzr", "RCS"]
        return Remove(pathseq, match=m, dir=True)
    def RemoveFiles(pathseq, match=[], search=[], ic=False):
        "Remove files using Remove()"
        return Remove(pathseq, match=match, search=search, ic=ic, dir=False)
    def Get(*dirs, recursive=False):
        '''Return a list of files and directories from the indicated
        directories.  If recursive is True, do so recursively.  All objects
        returned in the list are pathlib.Path objects.
        '''
        seq = []
        for dir in dirs:
            p = P(dir)
            if not p.is_dir():
                continue
            seq += p.rglob("*") if recursive else p.glob("*")
        return list(sorted(set(seq)))
    def GetFiles(*dirs, include_vc=False, recursive=False):
        '''Return a sorted sequence of file objects for the indicated
        directories.  If include_vc is True, include version control
        directories.  If recursive is True, do so recursively.
        '''
        f, g = lambda x: P(x).is_file(), lambda x: list(sorted(set(x)))
        seq = g(filter(f, Get(*dirs, recursive=recursive)))
        return seq if include_vc else RemoveVCDir(seq)
    def GetDirs(*dirs, include_vc=False, recursive=False):
        '''Return a sorted sequence of directory objects for the indicated
        directories.  If include_vc is True, include version control
        directories.  If recursive is True, do so recursively.
        '''
        f, g = lambda x: P(x).is_dir(), lambda x: list(sorted(set(x)))
        seq = g(filter(f, Get(*dirs, recursive=recursive)))
        return seq if include_vc else RemoveVCDir(seq)
    def KeepOnlyDirs(pathseq):
        return list(filter(lambda x: P(x).is_dir(), pathseq))
    def KeepOnlyFiles(pathseq):
        return list(filter(lambda x: P(x).is_file(), pathseq))
    def IsVCDir(dir):
        "Return True if dir is in a version control directory tree"
        if not hasattr(IsVCDir, "vc"):
            IsVCDir.vc = set((".bzr", ".git", ".hg", ".svn", "RCS"))
        for i in dir.parts:
            if i in IsVCDir.vc:
                return True
        return False
if 1:  # class Dirfiles
    class Dirfiles:
        r'''Construct a set with file names or directory names from one or
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
        directory dir with extensions png, jpg, and bmp.
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
        files = set()  # Container for all files
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
            self.files = set()
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
            "Set a new directory; this clears the local file set"
            self._dir = newdir
            self.p = pathlib.Path(newdir)
            self.files = set()
        @property
        def get(self):
            "Returns a copy of the instance's set of files"
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
            "Remove all files from the set."
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
            '''Keep only those files with the indicated extensions.'''
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
            remove = []
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
                    f = self.p / item
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

if __name__ == "__main__":
    if 1:  # Standard imports
        import os
        import threading
    if 1:  # Custom imports
        import lwtest
        import wsl
    if 1:  # Import symbols
        Lock = threading.Lock
        Thread = threading.Thread
        # 
        run = lwtest.run
        raises = lwtest.raises
        Assert = lwtest.Assert
        wsl = wsl.wsl
    if 1:  # Global variables
        h = "/gh"   # Header string for my files stored on github
        P = pathlib.Path
        dirfiles_image_list = "img1.png img2.png".split()
        dirfiles_filea = "file.a"
        dirfiles_images = set([P(i) for i in dirfiles_image_list])
        dirfiles_dir = "dirfiles"
    def Test_GetDirs():
        dirs = GetDirs(f"{h}/plib")
        Assert(isinstance(dirs, list))
        # These two directories are present for sure.  Others may be
        # present, but they're aren't core at the moment.
        for i in f"{h}/plib/pgm {h}/plib/test".split():
            Assert(P(i) in dirs)
        Assert(list(sorted(set(dirs))) == dirs)  # No duplicates
    def Test_GetFiles():
        'Test that a sample of the files in /plib are there'
        files = GetFiles(f"{h}/plib")
        Assert(isinstance(files, list))
        # Use some of the dp*.py files
        for i in f'''
                {h}/plib/dparith.py
                {h}/plib/dpastro.py
                {h}/plib/dpbp.py
                {h}/plib/dpdata.py
                {h}/plib/dpdb.py
                {h}/plib/dpdecimal.py
                {h}/plib/dpelec.py
                {h}/plib/dpmath.py
                {h}/plib/dppath.py
                {h}/plib/dpphys.py
                {h}/plib/dpseq.py
                {h}/plib/dpshop.py
                {h}/plib/dpstr.py
                {h}/plib/dptime.py
                {h}/plib/dptypes.py
            '''.split():
            Assert(P(i) in files)
        Assert(list(sorted(set(files))) == files)  # No duplicates
    def Test_Remove():
        pathseq = [P(i) for i in f'''{h}/plib/e.py {h}/plib/sig.py {h}/plib/eia.py
                   {h}/plib/sigfig.py {h}/plib/elliptic.py {h}/plib/sizes.py
                   {h}/plib/enc.py {h}/plib/states.py
                   {h}/plib/enc_codecs.csv'''.split()
        ]
        # Remove all items that have a directory that starts with 'p'
        s = RemoveDirs(pathseq, match=["p.*"])
        Assert(not s)
        # Remove files that contain 'i' or 'l'
        s = RemoveFiles(pathseq, search=["i", "l"])
        t = [P(i) for i in f'''{h}/plib/e.py {h}/plib/enc.py {h}/plib/states.py
                               {h}/plib/enc_codecs.csv'''.split()]
        Assert(s == t)
    def Test_RemoveVCDir():
        dirs = KeepOnlyDirs(Get("/plib"))
        Assert(P("/plib/.git") in dirs)
        dirs = RemoveVCDir(dirs)
        Assert(P("/plib/.git") not in dirs)
    def dirfiles_init():
        "Return an instance with no files"
        os.chdir(DirfilesSetup.cwd)  # Go back to starting directory
        # Change to the test directory
        os.chdir(dirfiles_dir)
        return Dirfiles(".", clear=True)
    def Test_Dirfiles_globbing():
        a = dirfiles_init()
        a.add("*.png")
        for i in dirfiles_images:
            Assert(i in a.files)
        a.update()
        for i in dirfiles_images:
            Assert(i not in a.files)
            Assert(i in Dirfiles.files)
    def Test_Dirfiles_size():
        a = dirfiles_init()
        a.add("*.png")
        Assert(a.size >= len(dirfiles_images))
    def Test_Dirfiles_dir():
        "This assumes the parent directory has more files than the current directory"
        a = dirfiles_init()
        a.add("*")
        n = a.size
        a.update()
        Assert(not a.size)
        a.dir = ".."
        a.add("*")
        m = a.size
        Assert(m and m > n)
    def Test_Dirfiles_get():
        a = dirfiles_init()
        a.add("*.png")
        f = a.get
        Assert(f == dirfiles_images)
        a.update()
        f = a.get
        Assert(not f and f != dirfiles_images)
    def Test_Dirfiles_get_all():
        a = dirfiles_init()
        a.add("*.png")
        a.update()
        f = a.get_all
        Assert(f == dirfiles_images)
    def Test_Dirfiles_clear():
        a = dirfiles_init()
        a.add("*.png")
        Assert(a.size)
        Assert(not len(Dirfiles.files))
        a.update()
        a.add("*.png")
        Assert(a.size)
        Assert(len(Dirfiles.files))
        a.files.clear()
        Assert(not a.size)
        Assert(len(Dirfiles.files))
        a.clear()
        Assert(not a.size)
        Assert(not len(Dirfiles.files))
    def Test_Dirfiles_update():
        a = dirfiles_init()
        a.add("*.png")
        Assert(not Dirfiles.files)
        a.update()
        Assert(Dirfiles.files == dirfiles_images)
        Assert(not a.files)
    def Test_Dirfiles_keepext():
        a = dirfiles_init()
        a.add("*")
        Assert(a.size == 3)
        a.keepext("png")
        Assert(P(dirfiles_filea) not in a.files)
    def Test_Dirfiles_keep():
        a = dirfiles_init()
        a.add("*")
        a.keep("file")
        Assert(P(dirfiles_filea) in a.files)
    def Test_Dirfiles_rmr():
        a = dirfiles_init()
        a.add("*")
        n = a.size
        a.rmr(r"^img.?\.png$")
        Assert(a.size == n - 2)
    def Test_Dirfiles_rm():
        a = dirfiles_init()
        a.add("*")
        n = a.size
        a.rm("dkjfdkjfdkjfd")  # No exception, no change
        Assert(a.size == n)
        a.rm(dirfiles_filea)
        Assert(a.size == n - 1)
        a.add(dirfiles_filea)
        Assert(a.size == n)
        a.add(dirfiles_filea)
        Assert(a.size == n)
        # Verify multiple items are removed when a string is given
        Assert(P("img1.png") in a.files)
        Assert(P("img2.png") in a.files)
        Assert(P(dirfiles_filea) in a.files)
        Assert(a.rm("img") == 2)
        Assert(P("img1.png") not in a.files)
        Assert(P("img2.png") not in a.files)
        Assert(P(dirfiles_filea) in a.files)
        # Check that exact works
        a = dirfiles_init()
        a.add("*")
        n = a.size
        a.rm("img", exact=True)
        Assert(a.size == n)
        a.rm("img1.png", exact=True)
        Assert(a.size == n - 1)
    def Test_Dirfiles_add():
        a = dirfiles_init()
        nonexistent = ";;nonexistent;;"
        # Get exception for nonexistent file or directory
        raises(ValueError, a.add, nonexistent, ignore=False)
        a.add("*.png")
        Assert(a.size == 2)
        # Ignore exception if ignore set
        raises(ValueError, a.add, nonexistent, ignore=True)
    def Test_Dirfiles_threading():
        "Show that two threads with different instances have access to the same Dirfiles.files data"
        a = dirfiles_init()
        a.add("*.png")
        a.update()
        Assert(Dirfiles.files == dirfiles_images)
        lock = Lock()
        def Process(s):
            lock.acquire()
            Assert(Dirfiles.files == dirfiles_images)
            # Add the 'files.a' file
            b = Dirfiles(".")
            b.add(dirfiles_filea)
            b.update()
            lock.release()
        t = Thread(name="Thd", target=Process, args=(a.get,))
        t.start()
        # Block until the started thread returns
        lock.acquire()
        # Show that Dirfiles.files now has dirfiles_filea.
        s = dirfiles_images.copy()
        s.add(P(dirfiles_filea))
        Assert(s == Dirfiles.files)
    def DirfilesSetup():
        "Create a dirfiles directory that will contain the three empty files"
        DirfilesSetup.cwd = os.getcwd()
        if not P(dirfiles_dir).exists():
            os.mkdir(dirfiles_dir)
        os.chdir(dirfiles_dir)
        # Create three empty files
        for file in dirfiles_image_list:
            if not P(file).exists():
                open(file, "w")
        if not P(dirfiles_filea).exists():
            open(dirfiles_filea, "w")
    def DirfilesTeardown():
        os.chdir(DirfilesSetup.cwd)  # Go back to starting directory
        os.chdir(dirfiles_dir)
        for file in dirfiles_image_list:
            if P(file).exists():
                os.remove(file)
        if P(dirfiles_filea).exists():
            os.remove(dirfiles_filea)
        os.chdir(DirfilesSetup.cwd)  # Go back to starting directory
        os.rmdir(dirfiles_dir)
    def Test_Dirfiles_get_directories():
        os.chdir(DirfilesSetup.cwd)  # Go back to starting directory
        if wsl:
            # Needed because /plib on WSL is a softlink to /gh/plib
            Assert(DirfilesSetup.cwd == "/gh/plib")
        else:
            Assert(DirfilesSetup.cwd == "/plib")
        a = Dirfiles(".", clear=True, getdirs=True)
        a.add("*")
        if a.size == 1:
            Assert(a.files == set([P(dirfiles_dir)]))
        else:
            Assert(P(dirfiles_dir) in a.files)
        # Change the directory to /plib/Dev/0dirfiles_test, which is a test directory.
        # It will have a .git directory and a testdir directory.
        os.chdir("/plib/Dev/0dirfiles_test")
        if 1:   # Check we have recursion and that repos are seen
            a = Dirfiles(".", clear=True, getdirs=True, ignore_repo=False)
            a.add("**/*")
            Assert(P("testdir") in a.files)
            Assert(P(".git") in a.files)
        if 1:   # Check we have recursion and that repos are not seen
            a = Dirfiles(".", clear=True, getdirs=True, ignore_repo=True)
            a.add("**/*")
            Assert(P("testdir") in a.files)
            Assert(P(".git") not in a.files)
        # Go back to starting directory
        os.chdir(DirfilesSetup.cwd)
    DirfilesSetup()
    status = run(globals(), regexp="^Test_", halt=True, verbose=False)[0]
    DirfilesTeardown()
    exit(status)
