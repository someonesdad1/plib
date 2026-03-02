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

if __name__ == "__main__":
    from lwtest import run, Assert
    h = "/gh"   # Header string for my files stored on github
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
                {h}/plib/dpprint.py
                {h}/plib/dpseq.py
                {h}/plib/dpshop.py
                {h}/plib/dpstr.py
                {h}/plib/dptags.py
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
    exit(run(globals(), regexp="^Test", halt=1)[0])
