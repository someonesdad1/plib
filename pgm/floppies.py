'''
Index of old floppy disks
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright © 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import re
        import sys
        from pdb import set_trace as xx
    # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t, RegexpDecorate
        from get import GetTextLines
    # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        data = '''
            # Disk_size StartNumber EndNumber Title
            5   1 12        MS BASIC 7.0
            5   13 28       MS Word 5.0
            5   29 30       MS Flight Simulator 3.0
            5   31          Super Morse
            5   32 35       dBase III
            5   36          QEdit 2.1
            5   37          Checkup program
            5   38          LIST program 7.3
            5   39          Kwiktree 2.14
            5   40 44       PCBoard 14.2 Demo
            5   45          Spitfire 2.8
            5   46          MS Entertainment Pack for Windows
            5   47 48       Jumbo 2.23 for tape backup
            5   49 52       MS EasyCAD 2.05
            5   53 54       MS MS-DOS 3.3
            5   55 58       MS Mouse & Paintbrush
            5   59 66       MS Word for Windows 1.0
            5   67          Telix 3.12
            5   67A         Copy of original Telix disk
            5   68          Rich Levin's virus detection system
            5   69          Patriquin's hard disk utilities
            5   70          HDM IV Hard Disk Manager
            5   71 73       Statgraphics from hard disk
            5   74 76       Drawing gallery B.03.00
            5   77 79       MS Flight Simulator 4.0
            5   80 85       PC Tools 6.0
            5   86 90       MS QuickBASIC 4.5
            5   91 93       Turbo Pascal
            5   94 95       Turbo BASIC
            5   96          HP PCLPak A.00.02
            5   97          Quicken 2.0
            5   98          Vectra high speed coprocessor diagnostic
            5   99          Glyphix font catalog
            5   100         PC Magazine Utilities disk
            5   101         PC Tools resident DOS utilities
            5   102 110     MS Word 4.0
            5   111 113     Lotus Magellan 1.0
            5   114 115     Quicken 3.0
            5   116 119     MS Word for Windows 1.1
            5   120         Numerical Recipes Pascal 2.0
            5   121         Lotus 123 (zipped)
            5   122 123     Quicken 5.0
            5   124 131     MS QuickC 2.5
            5   132         Catchem virus scan; sysmap
            5   133 134     MS Visual Basic
            5   135 141     MS Word for Windows 2.0
            5   142 143     Patriquin's hard disk utilities
            5   144 145     Demon's tomb
            5   146         MS Word for Windows Sample Macros
            5   147         Chuck Yeager's Advanced Flight Trainer
            5   148         Leather Goddesses of Phobos
            5   149         Transylvania
            5   150         Planetfall
            5   151         Silent Service
            5   152         Gato
            5   153         Helicopter
            5   154 156     King's Quest 3
            5   157 158     King's Quest 2
            5   159 160     Harrier
            5   161 163     Police Quest 1
            5   164 169     Leisure Suit Larry 2
            5   170         Font Load
            5   171 175     Letter Gothic font
            5   176 178     Prestige Elite font
            5   179         Headlines font
            5   180         Zapf Humanist font
            5   181         Century Schoolbook font
            5   182 183     TmsRmn & Helv fonts
            5   184         Headlines, Cent. Sch., Z. Humanist fonts arced
            5   185         Elite, Letter Gothic, FontLoad fonts
            5   186         Type Director pgm, fonts
            5   187         Premier Collection -- CG Times, Univers, Decor fonts
            5   188 197     The Colonel's Bequest
            5   198 203     Space Quest 3
            5   204 209     Police Quest 2
            5   210 218     King's Quest 4
            5   219 221     Space Quest 2
            5   222         Vendor's file backup
            5   223         Retire spreadsheet by Greg Hite
            5   224         Happy Games
            5   225 233     Codename -- Iceman
            3   234 237     Codename -- Iceman
            3   238 240     PC Tools deluxe
            3   241 244     King's Quest 4
            3   245 246     Microsoft EasyCAD ver. 1.10
            3   247 251     Harpoon
            3   252         King's Quest 2
            3   253         Helicopter
            3   254 260     MS Windows 3.0
            3   261         MS Flight Simulator Aircraft & Scenery Designer
            3   262 263     Flight Simulator ATP
            3   264 265     Lotus Magellan
            3   266 267     MS Mouse & Paintbrush
            3   268 269     MS Excel 3.0
            3   270         Calendar Creator Plus
            3   271         Willmaker
            3   272 274     Leisure Suit Larry 2
            3   275         Starflight
            3   276 278     Space Quest 3
            3   279 280     Police Quest 1
            3   281 283     Police Quest 2
            3   284 285     King's Quest 3
            3   286 287     Space Quest 2
            3   288         Quicken 5.0
            3   289         MS Sample macros for Using WordBasic (Word for Windows 2.0)
            3   290         MS Supplemental file conversions (Word for Windows 2.0)
            5   291         MS Supplemental file conversions (Word for Windows 2.0)
            3   292         Visual Basic Superbible
            3   293 295     Crescent QuickPak Professional SN062457 for BASIC
            5   296 297     Wasteland
            3   298 300     Mathcad 3.1
            5   301         Don Malin's XREF 2.10
            5   302         Peter Norton's book on assy language -- files
            5   303         A86/D86 Assembler/Disassembler by Eric Isaacson
            3   304 306     MKS RCS/MAKE utilities
            3   307 312     MS Windows 3.1
            5   313         DOS Power Tools (from the book)
            3   314 316     Typecase II (TrueType fonts for Windows)
            3   317 318     Norton pcAnywhere version 4.5
            3   319 321     Codewright 3.0c for Windows (319a-c are 1st set of disks that had two uncopyable files
            3   322         Dashboard 2.0
            3   323         Hearts for Windows version 2.0
            3   324 325     Codewright 2.0i for Windows SN CW020009-08868
            5   326 327     Codewright 2.0i for Windows SN CW020009-08868
            3   334         Commander Keen
            3   335         Kroz
            3   336 337     XTree version 2.0
            3   338 346     Turbo C++ for Windows + Protogen
            3   347         PKZIP 2.04g
            5   348         PKZIP 2.04g
            3   349 352     Doom version 1.2
            3   353 354     Jill of the Jungle, Xargon, Kiloblaster
            3   355 358     Sound Blaster software
            3   359         Lemmings (came w/Sound Blaster)
            3   360         Indianapolis 500 (came w/Sound Blaster)
            3   361         Numerical Recipes in C (2nd ed.) v2.02
            3   362 365     MKS Toolkit Version 4.2e for DOS, SN 3015391399
            3   366         MS Mouse Driver 9.0
            3   367 369     Quicken 4.0 for Windows
            3   370         Adaptec EZSCSI 2.02
            3   371         Adaptec Software Developer's Kit 2.2
            3   372         EasyCAD 2 version 2.72
            3   374         Commander Keen - Goodbye Galaxy
            3   375         Halloween Harry
            3   376 378     Microsoft Flight Simulator 5.0
            3   379 380     Applied Cryptography by Bruce Schneier
            3   400 402     MSDOS 6.22
            3   403 406     Microsoft Windows Printing System 1.0 (for Win 3.1)
            3   407 408     Diamond Stealth 64 Win 3.1 video drivers
            3   409 410     SimEarth
            3   411 418     Mathcad 6.0
            3   419         Xargon 2:  Secret Chamber
            3   420         Windows Coloring Book (Shareware version 1.0)
            3   421         Autofont Support - ProCollection
            3   422 426     MSDOS 6.0 plus Enhanced Tools
            3   427         Support disk for HP PC LAN adapter/16 Plus
            3   428 439     Borland C++ 3.1
            3   440         ProtoGen 2.2 for Borland C++ 3.1
            3   441         Photo duplication business idea Jul 1994
            3   442         DOS 5.0 boot disk
            3   443         Copy of DOS 5.0 boot disk (not bootable)
            3   444 446     MSDOS 6.21
            3   447         pgp 2.6.2 for DOS 8/13/95
            3   448         100LX connectivity pack
            3   449         pgp 2.6.2 + source
            3   450         form program archives 5/25/95
            3   451         Linux library from 7/8/95
            3   452         Old form backup from 12/6/93
            3   453         Windows NT emergency disk 10/31/96
            3   454         Micron CDROM Win 95 boot floppy rev 2.21
            3   455         Micron CDROM setup boot disk Win95 2/20/96
            3   456         FS4 & FS5 stuff from Jim
            3   457         Hard Disk Manager 4 (DOS program)
            3   458 459     Quick C zipped image from disk 1994
            3   460         16 bit MKS Toolkit utilities for DOS
            3   461         DOS 5.0 boot disk
            3   462         DOS 5.0 addendum, MKS man pages
            3   463         QuickBASIC 4.5
            3   464         Oct 1994 LIB archives (C, Pascal, NR)
            3   465         NSF matrix, Aetna Part B Medicare, Wordperfect format
            3   466 467     1994 election voter data
            3   468         Backup of Don's word processing documents from May 1995
            3   469         Backup of Glenda's word processing documents from May 1995
            3   470         Library files from old Linux machine
            3   471         Library files from old DOS machine
            3   472         1995 Quicken files
            3   473         nform:  rewrite of form program in C++
            3   474         GNU RCS 5.7 for DOS (used to use for form program)
            3   475         GNU RCS 5.7 for NT/Win95 (used for form program)
            3   476         MKS Toolkit 5.2 manpages
            3   477         NSF specifications (1.01 and 3.01)
            3   478         form (python) test files
            3   479         form (python) releases
            3   480 481     form (python) file backup
            3   482         BASIC programs, home & work
            3   483         Excel backup files (old ones)
            3   484         PC references:  helppc and dosref22
            3   485         IBM Assembler 2.0, Pascal programs, PSCSI, Turbo Assembler 1.0
            3   486         ProCollection for QuickBASIC 4.5
            3   487         knots.doc material.zip photo.zip
            3   488         Telix 3.12
            3   489 493     Microsoft QuickC (disk image)
            3   494 497     Borland C++ 3.1 (disk image)
            3   498         EasyCAD for Windows
            3   499 502     Python 1.5.1 (self-extracting executable)
            3   503         vim 4.6
            3   504 505     vim 5.3
            3   506         vim 5.3 source
            3   507 511     Turbo C++ 3.0 for DOS
        '''
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] regexp1 [regexp2...]
          Search for the indicated regular expressions in the names of old
          floppy disks.
        Options:
            -h      Print a manpage
            -i      Don't ignore case
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-i"] = True      # Ignore case
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hi", ["help"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("i"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
if 1:   # Core functionality
    def Search(regexp):
        r = re.compile(regexp, re.I) if d["-i"] else re.compile(regexp)
        rd.register(r, Color("yell"), None)
        for line in lines:
            rd(line)

if __name__ == "__main__":
    d = {}      # Options dictionary
    regexps = ParseCommandLine(d)
    rd = RegexpDecorate()
    lines = GetTextLines(data)
    for regexp in regexps:
        Search(regexp)
