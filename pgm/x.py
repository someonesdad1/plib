"""
For non-Windows machines, this needs to be modified to not change binary
executables that are compiled.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2020 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Change execute bits to off
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Standard imports
    import getopt
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from columnize import Columnize
    from wrap import dedent
    from color import t  # C
if 1:  # Global variables
    P = pathlib.Path
    ii = isinstance
    # These are the extensions to turn off the execute bits for -e
    ext = """
        asciidoc asm atom au aux avi bak bas bmp bz2 c cc cfg chm
        commonmark conf config cpp css csv dat db dbf dbg dlock doc docx
        dvi elf eps epub f f90 faq fmt gif gitignore gvim gz h hgignore hld
        hlp hpp htm html ico idx ini ino jar java jpeg jpg json lib log lst
        lyx man markdown markdown_github markdown_mmd markdown_phpextra
        markdown_strict mass md5 mediawiki mid midi mobi mov mp3 mp4 mpg
        msi o obj odb odf odg odm odp ods odt ogg otf out oxt pcx pdf php
        pickle png ppg ppt prd profile ps psp pspimage pub py pyc rar raw
        readme rec rot13 rtf s sgml sha256 src stackdump stderr stdout sty
        sub svg tags tar tbl template tex textile tgz tif tiff tmp todo ttf
        txt vim vimrc wav wmf wmv xls xlsx xml yaml zimwiki zip
    """
    extensions = set("*." + i for i in (ext + ext.upper()).split())
    ii = isinstance
    P = pathlib.Path
if 1:  # Utility

    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)

    def Dbg(*p, **kw):
        if d["-d"]:
            if "cc" in kw:
                if kw["cc"]:
                    print(f"{kw['cc']}", end="")
                else:
                    # print(f"{C.cyn}", end="")
                    print(f"{t('cynl')}", end="")
                del kw["cc"]
            kw["end"] = ""
            print(*p, **kw)
            # print(f"{C.norm}")
            print(f"{t.n}")

    def Usage(d, status=1):
        name = sys.argv[0]
        print(
            dedent(f"""
        Usage:  {name} [options] [item1 [item2 ...]]
          Turn execute permission off on files (never directories).  If item is a
          directory, do it for the files in that directory; otherwise, it's a
          single file.  Defaults to current directory.

          If -f is not used, only turn execute permission off on files that aren't
          executables like compiled binaries or scripts that begin with "#!".
        Options:
            -d      Show debug output
            -E      Show supported extensions
            -e      Only change files with supported extensions
            -f      Force permission changes on all files
            -H      Include hidden files
            -h      Print a manpage
            -n      Dry run:  show what will happen but don't make changes
            -r      Recurse into the indicated directories
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-d"] = False  # Debug output
        d["-E"] = False  # List extensions
        d["-e"] = False  # Only files with supported extensions
        d["-f"] = False  # Force changes on all files
        d["-H"] = False  # Include hidden files
        d["-n"] = False  # Dry run
        d["-r"] = False  # Operate recursively
        try:
            opts, dirs = getopt.getopt(sys.argv[1:], "dEefHhnr")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dEefHnr"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(d, status=0)
        if d["-E"]:
            ShowExtensions()
        if not dirs:
            dirs = ["."]
        return dirs


if 1:  # Core functions

    def ShowExtensions():
        print("Extensions that will have execute bits turned off:")
        e = sorted(set([i.lower().replace("*.", "") for i in extensions]))
        for i in Columnize(e, indent=" " * 4):
            print(i)
        exit(0)

    def IgnoreHidden(file):
        if file.name[0] == "." and not d["-H"]:
            return True
        return False

    def IgnoreExecutable(file):
        """Return True if this file should be ignored since it is an
        executable.
        """
        if d["-f"]:
            return False
        extension = file.suffix.lower()
        common = set(
            [
                "." + i
                for i in """
                exe sh bash ksh csh tcsh zsh dll
                """.split()
            ]
        )
        if extension in common:
            return True
        else:
            if ("*" + extension) in extensions:
                return False  # Always process known extensions
            # See if first line starts with '#!'
            try:
                line = open(file).readline().strip()
            except UnicodeDecodeError:
                # It's not a UTF-8 file
                if d["-d"]:
                    t.print(
                        f"{t('magl')}Unicode decode error for '{file}'", file=sys.stderr
                    )
                return False
            except Exception as e:
                if d["-d"]:
                    t.print(f"{t('magl')}Exception for '{file}':  {e}", file=sys.stderr)
                return False
            if len(line) > 2:
                return True if line[:2] == "#!" else False

    def ExecuteBitOff(file):
        assert isinstance(file, pathlib.Path)

        def execute_is_on(value):
            return get_bit(value, 0) or get_bit(value, 3) or get_bit(value, 6)

        def get_bit(value, n):
            return (value >> n & 1) != 0

        def clear_bit(value, n):
            return value & ~(1 << n)

        if file.is_dir():  # Do not change directory permissions
            Dbg(f"Ignored directory:  '{file}'", cc=t("redl"))
            return
        elif file.is_symlink():  # Do not change directory permissions
            Dbg(f"Ignored symlink:  '{file}'", cc=t("redl"))
            return
        p = file.stat().st_mode
        if execute_is_on(p):
            if IgnoreExecutable(file):
                Dbg(f"Ignored executable:  '{file}'", cc=t("redl"))
                return
            if IgnoreHidden(file):
                Dbg(f"Ignored hidden:  '{file}'", cc=t("redl"))
                return
            if d["-n"]:  # Dry run
                print(file)
            else:
                p = clear_bit(p, 0)
                p = clear_bit(p, 3)
                p = clear_bit(p, 6)
                file.chmod(p)
                Dbg(f"'{file}' processed")

    def ProcessDirectory(p):
        s = "**/*" if d["-r"] else "*"
        for file in p.glob(s):
            ExecuteBitOff(file)


if __name__ == "__main__":
    d = {}  # Options dictionary
    dirs = ParseCommandLine(d)
    for dir in dirs:
        p = P(dir)
        ExecuteBitOff(p) if p.is_file() else ProcessDirectory(p)
