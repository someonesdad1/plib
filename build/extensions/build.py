"""
Construct a dictionary of file name extensions to a tuple of their
descriptions to stdout.  This is used to make /plib/extension.py.
"""

if 1:  # Header
    if 1:  # Standard imports
        from collections import defaultdict
        from pathlib import Path as P
        import sys
        import time
    if 1:  # Custom imports
        from wrap import dedent
        from color import t
    if 1:  # Global variables
        t.err = t("ornl")

        class G:
            pass

        g = G()  # Storage for global variables as attributes
        g.di = defaultdict(list)  # Output dict
if 1:  # Utility

    def Webopedia():
        "Generator to return (ext, descr) tuples"
        # From https://www.webopedia.com/reference/data-formats-and-file-extensions/
        # 2 Dec 2023 09:08:10 AM
        data = """
            .!bt	BitTorrent Incomplete Download file
            .!qb	qBittorrent Partial Download file
            .!ut	uTorrent Incomplete Download file
            .#24	Printer data file for 24 pin matrix printer (LocoScript)
            .#ib	Printer data file (LocoScript)
            .#sc	Printer data file (LocoScript)
            .#st	Standard mode printer definitions (LocoScript)
            .$#!	Cryptext
            .$$$	Temporary file
            .$00	Pipe file (DOS)
            .$01	Pipe file (DOS)
            .$db	Temporary file (dBASE IV)
            .$ed	Editor temporary file (MS C)
            .$er	GroupWise Database
            .$o1	Pipe file (DOS)
            .$vm	Virtual manager temporary file (Windows 3.x)
            .^^^	Pervasive.SQL Database file
            .__a	File Splitter & Joiner Encrypted file
            .__b	File Splitter & Joiner Encrypted Archive file
            ._dd	Norton Disk Doctor Recovered file
            ._eml	Windows Live Mail Email file
            ._nws	Windows Live Mail Newsgroup Copy file
            ._p	Malicious Software Removal Tool Temporary file
            .~$~	Temporary file (1st Reader)
            .~ap	Old AppExpert project database (Borland C++ 4.5)
            .~de	Project backup (Borland C++ 4.5)
            .~hm	HostMonitor TestList Backup file
            .~mn	Menu backup (Norton Commander)
            .{pb	Corel WordPerfect Document Index file
            .201$201	Temporary file (1st Reader)
            .000	Image Data Recovery file
            Compressed harddisk data (DoubleSpace)
            .001	Norton Ghost Span file
            Multiple Volume Compressed file
            Fax (many)
            .075	75×75 dpi display font (Ventura Publisher)
            .085	85×85 dpi display font (Ventura Publisher)
            .091	91×91 dpi display font (Ventura Publisher)
            .096	96×96 dpi display font (Ventura Publisher)
            .0b	Printer font with lineDraw extended character set (PageMaker)
            .0xe	F-Secure Renamed Virus file
            .1	Inno Setup Binary file
            Roff/nroff/troff/groff source for manual page (cawf2.zip)
            .10	IBM Voice Type Script file
            .113	Iomega Backup file
            .123	Lotus 1-2-3 Spreadsheet file
            .15u	Printer font with PI font set (PageMaker)
            .1pe	TurboTax Form file
            .1ph	TurboTax file
            .1st	Usually README.1ST text
            .2	Setup Factory 6.0 setup launcher
            .264	Ripped Video Data file
            .2d	2d Drawings (VersaCad)
            .2da	2 Dimensional Data Array file
            .2dl	2d Libraries (VersaCad)
            .3d	3d Drawings (VersaCad)
            .3dl	3d Libraries (VersaCad)
            .3dv	3D VRML World
            .301	Fax (Super FAX 2000 – Fax-Mail 96)
            .386	Intel 80386 processor driver (Windows 3.x)
            .3da	3D Assembly file
            .3dd	ArcGlobe Document file
            .3dr	3DMark Benchmark file
            .3ds	Graphics (3D Studio)
            .3dt	Database for 3D mind map / concept map (3D Topicscape)
            .3fx	Effect (CorelChart)
            .3g2	3GPP2 file format
            .3gp	3GPP Multimedia file
            .3gr	Data file (Windows Video Grabber)
            .3ko	NGRAIN Mobilizer
            .3me	TurboTax Form file
            .3mm	3D Movie Maker Movie Project
            .3pe	TurboTax 2008 Form file
            .3t4	Binary file converter to ASCII (Util3)
            .411	Sony Mavica Data file
            .4c$	Datafile (4Cast/2)
            .4dv	4D View Ultrasound file
            .4mp	4-MP3 Database file
            .4sw	4dos Swap File
            .4th	Forth source code file (ForthCMP – LMI Forth)
            .5cr	Preconfigured drivers for System 5cr and System 5cr Plus
            .669	Music (8 channels) (The 669 Composer)
            .6cm	Music (6 Channel Module) (Triton FastTracker)
            .777	7-Zip compressed file archive
            .7z	7-Zip archiving format
            .8	A86 assembler source code file
            .8b?	Adobe Photoshop Plugin file
            .8ba	Adobe Photoshop Plugin file
            .8bf	Adobe Photoshop Plugin file
            .8bi	Adobe Photoshop Plugin file
            .8cm	Music (8 Channel Module) (Triton FastTracker)
            .8li	Photoshop Scripting Plug-in
            .8m	Printer font with Math 8 extended character set (PageMaker)
            .8pbs	Adobe Photoshop Macintosh file
            .8u	Printer font with Roman 8 extended character set (PageMaker)
            .a	Ada source code file
            Library (unix)
            .a0?	ALZip Split Archive file
            .a11	Graphics AIIM image file
            .a2b	A2B Player Playlist
            .a3d	Amapi 3D Modeling file
            .a3m	Unpackaged Authorware MacIntosh file
            .a3w	Unpackaged Authorware Windows file
            .a4a	Authorware 4.x Library
            .a4m	Unpackaged Authorware MacIntosh file
            .a4p	Authorware file packaged without runtime
            .a4w	Unpackaged Authorware Windows file
            .a5w	Unpackaged Authorware Windows file
            .aa	Audible Audio file
            .aab	Macromedia Authorware Binary
            .aac	Advanced Audio Coding MPEG-2, MPEG-4
            .aam	Authorware shocked file
            .aax	Audible Audiobook file
            .ab2	Parson’s Address Book
            .ab6	Datafile (ABStat)
            .ab8	Datafile (ABStat)
            .aba	Palm Address Book file
            .abc	ActionScript Byte Code File
            ABC FLOWCHARTER 1.x flowchart
            ABC2K Audio/Video Controller Software
            .abd	AmBiz Bonus Calculator data file
            Adventure Builder database
            .abf	Adobe Binary Font
            .abi	ABI CODER Encryption software
            AOL extension: AOL 6 Organizer
            .abk	Automatic backup file (CorelDRAW)
            .abm	ImagePals Photo Album Document
            Montage Photo Album file
            PhotoPlus Album file
            .abr	Adobe Photoshop brush file
            .abs	Abstracts (info file)
            Data file (Abscissa)
            MPEG audio sound file
            .abw	AbiWord document
            .abx	WordPerfect Address Book file
            .aby	AOL file (located in AOL program directory)
            .ac3	AC3 Audio File Format
            .aca	Microsoft Agent Character file
            Project (Project Manager Workbench)
            .acb	Graphics (ACMB)
            .acc	Program (DR-DOS – ViewMax) (GEM / resident)
            .acd	Sonic Foundry Acid music file
            .ace	Ace Archiver / WinAce compressed file
            .acf	Microsoft Agent Character file
            Adobe Photoshop Custom Filter
            .aci	ACI Development Appraisal
            .acl	Microsoft Office Auto Correction file
            Document file (Audit Command Language)
            ArborText Command Language
            .acm	Audio Compression Manager Driver
            Photoshop command button
            Windows system file
            ACBM image file
            Interplay compressed Sound file
            .acorn	ACORN Graphics format
            .acs	MS Agent Character file
            .acs2	AIMP2 Media Player Skin file
            .acsm	Adobe Content Server Message file
            .act	Actor source code file
            Foxdoc Action Diagrams (FoxPro)
            Presentation (Action!)
            .acv	OS/2 Audio Drivers
            Photoshop Saved Curve
            .ad	Screen saver data (AfterDark)
            .ada	Ada source code file
            .adb	Ada Package Body
            .adc	Bitmap graphics (16 colors) (Scanstudio)
            .ade	Microsoft Access Project
            .adf	Adapter Description file
            Admin Config file
            Amiga Disk File
            Dog Creek QC Mask file
            .adi	Graphics (AutoCAD)
            .adl	Mca adapter description library (QEMM)
            .adm	After Dark Screen Saver Module
            Windows Policy Template
            Addict Compiled Dictionary
            Administrative template files for protected mode in Internet Explorer 7.0
            Advantage Data Server Database Memo file
            .adn	Add-in (Lotus 1-2-3)
            .ado	Photoshop Duotone Options
            Stata Program
            .adp	FaxWorks Modem setup file
            Astound Dynamite file
            MS Access Project
            AOLserver Dynamic Page file
            .adr	Address Book
            Address Plus Database
            After Dark Random Screen Saver Module
            Opera Web Browser Bookmark file
            Smart Address Address Book
            .ads	Ada Package Specification
            .adt	Datafile for cardfile application (HP NewWave)
            Fax (AdTech)
            .adx	Document (Archetype Designer)
            .adz	GZ-Packed Amiga Disk file
            .aeh	iPer Advanced Embedded Hypertext
            .aep	Adobe After Effects Project file
            .aex	PGP Armored Extracted Public Encryption Key
            After Effects Plugin file
            .af2	Flowchart (ABC FlowCharter 2.0)
            .aff	AnyForm Form file
            .afi	Truevision bitmap graphics
            .afl	Font file (for Allways) (Lotus 1-2-3)
            .afm	Type 1 font metric ASCII data for font installer (ATM – many)
            Datafile for cardfile application (HP NewWave)
            .afs	Adobe Type Manager font set
            .aft	AnyForm template file
            .ag	Applixware graphics file
            .agp	Aspen Graphics Pages
            .agw	Aspen Graphics Windows
            .ai	Vector graphics (Adobe Illustrator)
            .aiff	Audio interchange file format
            .ain	Compressed file archive created by AIN
            .aio	APL file transfer format file
            .air	Adobe AIR Installation Package file
            Automatic Image Registration
            .ais	Array of Intensity Samples graphics (Xerox)
            .aix	Datafile for cardfile application (HP NewWave)
            .ajp	JPEG2000 Digital closed-circuit television (CCTV) security camera video format
            .alb	JASC Image Commander Album
            Photo Soap2 file
            Steinberg Cubase or VST Backup Song file
            .albm	webAlbum Photo Album
            HP Photosmart Photo Printing Album
            .all	Format file for working pages (Always)
            General printer information (WordPerfect for Win)
            Symbol and font files (Arts & Letters)
            .als	Alias Image
            Calmira Shortcut file
            .alt	Menu file (WordPerfect Library)
            .alx	ActiveX Layout file
            .alz	ALZip Compressed file
            .amf	Music (Advanced Module Format)
            .amff	Amiga Metafile
            .amg	Compressed file archive created by AMGC
            System image file (Actor)
            .amp	Photoshop Arbitrary Map Settings
            .amr	Adaptive Multi-Rate ACELP Codec
            Above audio file extension
            .amv	AMV Video file
            .amx	After Effects Motion Exchange file
            .anc	Animation file format (MorphInk)
            .ani	Animation (Presidio – many)
            .anm	Animation (Deluxe Paint Animator)
            .ann	Help Annotations (Windows 3.x)
            .ans	Ansi graphics (character animation)
            Ascii text ANSI character set (NewWave Write)
            .aos	Add-On Software (Nokia 9000)
            ARCHOS 504 media
            .ap	Compressed Amiga file archive created by WHAP
            Datafile (Datalex EntryPoint 90)
            Artwork Systems Program (ArtPro)
            .apc	Printer driver (Lotus 1-2-3)
            .apd	Printer driver (Lotus 1-2-3)
            .ape	Music format (different players)
            .apf	Printer driver (Lotus 1-2-3)
            .api	Adobe Acrobat Plugin file
            Passed parameter file (1st Reader)
            Printer driver (Lotus 1-2-3)
            .apk	Android Package file
            .apl	APL work space format file
            .apm	ArcPad 6 file
            .app	Add-in application file (Symphony)
            Application object file (dBASE Application Generator)
            Executable application file (DR-DOS – NeXTstep – Atari)
            Generated application (FoxPro)
            .apr	Employee performance review (Employee Appraiser)
            .aps	MS Visual C++ file
            ArcPad 5 Symbology file
            .apx	Appexpert database file (Borland C++ 4.5)
            .arc	Compressed file archive created by ARC (arc602.exe/pk361.exe)
            Compressed file archive created by SQUASH (squash.arc)
            .arf	Automatic Response file
            .arg	AutoCAD Profile Export file
            .ari	Compressed file archive created by ARI
            .arj	Compressed file archive created by ARJ (arj241.exe)
            .arl	AOL Organizer File
            .ark	Arc file archive created by CP/M port of ARC file archiver
            Compressed file archive created by QUARK
            .arr	Arrangement (Atari Cubase)
            .ars	Adobe After Effects Render
            .art	Graphics (scrapbook) (Art Import)
            Raster graphics (First Publisher)
            .arv	Arsiv File
            AutoRoute User Information
            .arx	Compressed file archive created by ARX
            .asa	MS Visual InterDev file
            Active Server Document
            .asc	Ascii text file
            Adobe ActionScript Communication file
            Transport armor file (PGP)
            .ascx	Microsoft ASP.NET user control file
            .asd	Autosave file (Word for Windows)
            Presentation (Astound)
            Screen driver (Lotus 1-2-3)
            .asf	Datafile (STATGRAPHICS)
            Screen font (Lotus 1-2-3)
            .ash	Assembly language header file (TASM 3.0)
            .asi	Assembler include file (Turbo C – Borland C++)
            .asl	Adobe Photoshop Layer file
            .asm	Assembly source code file
            Pro/Engineer Assembly file
            .asmx	Microsoft .NET Web Service file
            .aso	Assembler object (object orientated) file (Turbo Assembler)
            .asp	Microsoft Active Server Page
            Aspect source code file (Procomm Plus)
            Association of Shareware Professionals OMBUDSMN.ASP notice
            .aspx	Microsoft ASP.NET file
            .asr	Ms Automap Route
            Photoshop Scratch Area
            .asx	Microsoft Windows Media Active Stream Redirector file
            .asx	Microsoft Advanced Streaming Format
            .at2	Auto template (Aldus Persuasion 2.0)
            .atm	Adobe Type Manager data/info
            .atn	Adobe Photoshop Action file
            .atr	Lightscape Material Library
            .att	AT&T Group 4 Bitmap
            .aty	3D Topicscape (Exported association type)
            .au	Sound (audio) file (SUN Microsystems)
            .au3	Autoit3 script file
            .aud	Audio file
            .aut	AutoIt Script
            PocketWear Car Lease Kit vehicle data file
            TLG Workplace CD search file
            Xitami Webserver Admin Password file
            GPSMan-autoMapic file
            Signwave Auto-Illustrator file
            Descent Manager Mission file
            Authentication file (various)
            Interactive Pictures iPIX Format
            .aux	Auxillary references (TeX/LaTeX)
            Auxiliary dictionary (ChiWriter)
            .ava	Publication (Avagio)
            .avb	Inoculan Anti-Virus virus infected file
            Microsoft Chat character file
            .avd	Avery Label Pro Data file
            .avi	Audio Video Interleaved animation file (Video for Windows)
            .avr	Audio Visual Research file
            .avs	Animation file
            Application Visualization System Format
            Stardent AVS-X image
            Winamp Advanced Visualization Studio file
            .avx	ArcView file
            .aw	Text file (HP AdvanceWrite)
            Answer Wizard for Microsoft Help
            .awb	Lavasoft Ad-aware backup file
            .awd	AWD MS Fax
            Award BIOS file
            AWK Language Source Code file
            .awe	Adobe Acrobat Bookmark XML file
            .awk	Awk script/program
            .awm	Movie (Animation Works)
            .awp	Microsoft Fax key viewer
            .awr	Telsis Digital Audio file
            .aws	Data (STATGRAPHICS)
            .ax	DirectShow Filter
            .axd	Avery Label Pro Re-Index file
            Actrix Technical file
            .axe	Paradigm C++ Integrated Debugger file
            ChordMaster
            MS Autoroute export file
            .axg	MS Autoroute Trip file
            .axl	ArcIMS XML Project file
            .axs	AMX Axcess control system file format
            HTML Active X script
            .axt	ZenWorks snAPPshot ASCII Application Object template
            Photoshop Replace Color/Color Range
            .axx	axxess files used as backups of Inter-Tel databases
            .azw	Amazon Kindle eBook File
            .azz	AZZ Cardfile
            .b	Batch list (APPLAUSE)
            .b&w	Black and white graphics (atari – mac)
            .b~k	backup file
            Mono binary screen image (1st Reader)
            .b00	CD Image Segment file
            .b16	PCO Graphic file
            .b1n	Both mono and color binary screen image (1st Reader)
            .b1s	Booksmith
            .b30	Printer font (JLaser – Cordata) (Ventura Publisher)
            .b3d	3D Builder file
            .b5i	Blindwrite 5 Disk Image file
            .b5t	Blindwrite 5 Image Information file
            .b6i	Blindwrite 6 Disk Image file
            .b6t	Blindwrite 6 Image Information file
            .b8	Raw graphics (one byte per pixel) plane two (PicLab)
            .b_w	Black and white graphics (atari – mac)
            .bad	Bad file (Oracle)
            .bag	PMMail Mail Index file
            OS/2 Netfinity Manager Sysinfo file
            AOL Instant Messenger file
            .backup	Ad-Aware Reference file
            .bak	Backup file
            .bal	Music score (Ballade)
            .ban	Sierra Print Artist Banner
            .bar	Horizontal bar menu object file (dBASE Application Generator)
            .bas	Basic source code file
            Microsoft Visual Basic class module
            .bat	Batch file (DOS)
            .bb	Database backup (Papyrus)
            .bba	Settler IV Archive file
            .bbl	Bibliographic reference (TeX/BibTeX)
            .bbm	Brush (Deluxe Paint)
            .bbs	Bulletin Board System announce or text info file
            .bc!	Bitcomet Incompleted Download file
            .bcf	ConfigSafe Snapshot index
            Belarc Advisor Content File
            The Sims (Maxis) File
            .bch	Batch process object file (dBASE Application Generator)
            Datafile (Datalex EntryPoint 90)
            .bck	Backup
            .bcm	MS Works Communications file
            .bcn	Business Card Pro Design
            .bco	Outline font description (Bitstream)
            .bcp	Borland C++ makefile
            .bct	Business Card Designer template
            .bcw	Environment settings (Borland C++ 4.5)
            .bde	Borland Database Engine
            .bdf	Bitmap Distribution Format font file (X11)
            Datafile (Egret)
            .bdm	AVCHD Index file
            .bdmv	Blu-ray information file
            .bdr	Border (MS Publisher)
            .bez	Outline font description (Bitstream)
            .bf2	Bradford 2 font
            .bff	Binary file format
            .bfm	Font metrics (unix/Frame)
            .bfs	Tivoli Storage Manager file
            .bfx	Fax (BitFax)
            .bga	Bitmap graphics
            .bgt	Quicken 2002 Internet Common File
            .bgi	Borland Graphics Interface device driver
            .bgl	Flight Simulator scenery file
            .bgt	Quicken 2002 Internet Common File
            .bib	Bibliography (ASCII)
            Database – not compatible with TeX format (Papyrus)
            Literature database (TeX/BibTeX)
            .bic	Civilization III Scenario
            .bid	BidMaker 2002 file
            .bif	Binary Image Format b&w graphics (Image Capture board)
            .bik	BioCharter Profile backup file
            Bink Game video file
            .bin	Binary file
            .bio	OS/2 BIOS
            .bip	Free-motion capture files for character studio biped
            .bit	Bitmap Image
            Worms Armageddon Imported Map
            Worms World Party Imported Map
            .bk	Faxbook (JetFax)
            .bk!	Document backup (WordPerfect for Win)
            .bk1	Timed backup file for document window 1 (WordPerfect for Win)
            .bk2	Timed backup file for document window 2 (WordPerfect for Win)
            .bk3	Timed backup file for document window 3 (WordPerfect for Win)
            .bk4	Timed backup file for document window 4 (WordPerfect for Win)
            .bk5	Timed backup file for document window 5 (WordPerfect for Win)
            .bk6	Timed backup file for document window 6 (WordPerfect for Win)
            .bk7	Timed backup file for document window 7 (WordPerfect for Win)
            .bk8	Timed backup file for document window 8 (WordPerfect for Win)
            .bk9	Timed backup file for document window 9 (WordPerfect for Win)
            .bkf	Microsoft Backup file
            .bkg	Background file
            UWXAFS Binary Format Data file
            .bkp	Backup file (Write – TurboVidion DialogDesigner)
            .bkw	Mirror image of font set (FontEdit)
            .blb	DreamWorks Resource Archive
            .bld	Bloadable picture (BASIC)
            .blend	Blender 3D file
            .blf	Windows Registry Recovery file
            Bantec Scanner Driver file
            .blg	Binary Performance Log File
            .blk	Temporary file (WordPerfect for Win)
            Lightscape Block Library
            Alias Wavefront Image
            VersaPro Block
            .blob	Steam Archive file
            .blt	Saved AIM Buddy List file
            Wordperfect for DOS file
            .bm	Bitmap graphics
            .bmf	Corel Image file
            .bmi	3ds max Executable
            .bmk	Help Bookmarks (Windows 3.x)
            .bmp	Bitmap graphics (PC Paintbrush – many)
            .bmx	Buzz music file
            .bnd	Typequick file
            .bndl	Bundle file
            .bnk	Adlib instrument bank file
            .bob	BobDown Downloading Program
            Bob Raytracer
            .bom	MicroSim PCBoard Bill of Materials
            Orcad Schematic Capture Bill of Materials file
            Softshare Delta Business Object Model
            .boo	Compressed file ASCII archive created by BOO (msbooasm.arc)
            .book	Adobe FrameMaker Book
            HTMLDOC document
            .bot	Linkbot file
            .box	Myriad Jukebox file
            Notes Mailbox
            .bpc	Chart (Business Plan Toolkit)
            .bpl	Delphi Library
            .bpt	Bitmap fills file (CorelDRAW)
            .bqy	BrioQuery file
            .br	Script (Bridge)
            .brd	Eagle Layout file
            .brf	Braille ASCII file
            .brk	Fax (Brooktrout Fax-Mail)
            .brn	BornoSoft Bangla2000 (a Bengali word processor) File extension
            .bro	Tree Professional Broadleaf Creator file
            .brp	Tree Professional Broadleaf Creator image
            .brt	Micrografx Picture Publisher file
            .brx	Multimedia browsing index
            .bsa	Compressed file archive created by BSARC
            .bsb	MapInfo Sea Chart
            SWAT Sub-basin Output file
            .bsc	Compressed Apple II file archive created by BINSCII
            Database (Source Browser)
            Pwbrmake object file (MS Fortran)
            .bsdl	Boundary Scan Description Language
            .bsl	BSPlayer Configuration file
            .bsp	Half-life/TFC/CS Map
            Quake Map
            .bst	BibTeX Style file
            .bsv	Bluespec System Verilog file
            .bt!	BitTorrent Partial Download file
            .btm	Batch To Memory batch file (4DOS)
            .btn	Buttonware file
            .bto	Baytex Organix! 2001 Language Kit
            .btr	Btrieve Database file
            MS Frontpage-related file
            .btx	DB/TextWorks Database Term & Indexes
            .bud	Quicken Backup
            .bug	Bugs and Problems
            .bun	Bundled Audio files
            .bup	DVD Backup file
            .but	Button definitions (Buttons!)
            .buy	Datafile format (movie)
            .bv1	Overflow file below insert point in Doc 1 (WordPerfect for Win)
            .bv2	Overflow file below insert point in Doc 2 (WordPerfect for Win)
            .bv3	Overflow file below insert point in Doc 3 (WordPerfect for Win)
            .bv4	Overflow file below insert point in Doc 4 (WordPerfect for Win)
            .bv5	Overflow file below insert point in Doc 5 (WordPerfect for Win)
            .bv6	Overflow file below insert point in Doc 6 (WordPerfect for Win)
            .bv7	Overflow file below insert point in Doc 7 (WordPerfect for Win)
            .bv8	Overflow file below insert point in Doc 8 (WordPerfect for Win)
            .bv9	Overflow file below insert point in Doc 9 (WordPerfect for Win)
            .bwa	BlindWrite Disk Image Information file
            .bwb	Spreadsheet application (Visual Baler)
            .bwi	Blindread/Blindwrite
            .bwr	Beware (buglist) (Kermit)
            .bws	Blindwrite Sub Channel Data File
            .bwt	Blindread/Blindwrite
            .bxx	blaxxun Contact
            .bz2	Bzip 2 UNIX Compressed file
            .c	C source code file
            Compressed unix file archive created by COMPACT
            .c++	C++ source code file
            .c–	Source code (Sphinx C–)
            .c00	Print file (Ventura Publisher)
            WinAce Split Archive file
            .c01	Genesis 2000
            .c2d	WinOnCD CD Image
            .c4d	MAXON Cinema 4D File (Graphics)
            .c60	Midtronics Battery Management Software
            .c86	C source code file (Computer Innovation C86)
            .ca	Initial cache data for root domain servers (Telnet)
            .cab	Cabinet File (Microsoft installation archive)
            .cache	Cache file (typically Web cache)
            .cad	Softdesk Drafix CAD File
            .cac	dBASE IV executable when caching on/off (see cachedb.bat)
            .cad	Document (Drafix Windows CAD)
            .cag	MS Clip Gallery Catalog file
            .cal	Calendar file (Windows 3.x)
            Calendar Maker Pro
            .calb	Coolect Album file (Coolect Album Player)
            Spreatsheet (SuperCalc)
            .cam	Casio Camera Graphic
            .can	Fax (Navigator Fax)
            .cap	Caption (Ventura Publisher)
            Session capture file (Telix)
            .car	AtHome Assistant file
            Carrara Environment
            NeoBook Cartoon
            .cas	Comma-delimited ASCII File
            .cat	Catalog (dBASE IV)
            .cb	Clean Boot File (Microsoft)
            Brief Macro Source Code
            .cbc	Fuzzy logic system (CubiCalc)
            .cbf	Calendar Builder file
            .cbl	Cobol source code file
            .cbm	Compiled bitmap graphics (XLib)
            .cbp	CentralBuilder Project
            .cbr	ComicBook Reader File archive (CDisplay image viewer)
            .cbt	Computer Based Training (many)
            .cbz	ComicBook Reader File archive (CDisplay image viewer)
            .cc	C++ source code file
            .cca	CC:Mail archive file
            .ccb	Visual Basic Animated Button Configuration
            .ccc	Bitmap graphics (native format) (Curtain Call)
            .ccd	CloneCD Related file
            Vector CAD Program file
            .cce	Calendar Creator 2 Event file
            .ccf	Communications configuration file (Symphony)
            .cch	Chart (CorelChart)
            .ccl	Communication Command Language file (Intalk)
            .cco	Btx Graphics file (XBTX)
            .cct	Macromedia Director Shockwave file
            .ccx	Corel PrintHouse file
            .cda	CD Audio Track
            .cdb	Card database (CardScan)
            Main database (TCU Turbo C Utilities)
            .cdd	ConceptDraw Document file
            .cde	Honeywell Hybrid Control Designer
            .cdf	Component Definition file
            Graphics (netcdf)
            .cdg	Compact Disc Plus Graphics file
            .cdi	Phillips Compact Disk Interactive format
            DiscJuggler Image file
            .cdk	Document (Atari Calamus)
            .cdl	CaseWare Working Papers Document Link
            SignLab Vector Graphic
            .cdm	Media Maker Disk Image file
            Visual dBASE Custom Data Module
            .cdp	Visual Objects Developer file
            CD/Spectrum Pro
            .cdr	Vector graphics (CorelDRAW native format)
            .cdt	Data (CorelDraw 4.0)
            .cdx	CorelDraw Compressed Image file
            Compound index (FoxPro)
            .ce	Main.ce (The FarSide Computer Calendar)
            .ceb	Apabi eBook file
            .ceg	Bitmap graphics (Tempra Show – Edsun Continuous Edge Graphics)
            .cel	Graphics (Autodesk Animator – Lumena)
            .cf	Sendmail Configuration file
            Configuration file (imake)
            .cfb	Comptons multimedia file
            .cfc	Macromedia Coldfusion component extension
            .cfg	Configuration
            .cfl	Chart (CorelFLOW)
            .cfm	ColdFusion Markup Language (Allaire)
            .cfn	Font data (Atari Calamus)
            .cfo	C Form Object internal format object file (TCU Turbo C Utilities)
            .cfp	Quicken Cash Flow Projection file
            Fax (The Complete Fax Portable)
            .cfr	Crossfire Replay file
            .cga	CGA display font (Ventura Publisher)
            .cgd	Cricket Graph Data file
            .cge	CCD Astrocamera
            .cgi	Common Gateway Interface script
            .cgm	Computer Graphics Metafile vector graphics (A&L – HG – many)
            .ch	Header file (Clipper 5)
            .ch3	Chart (Harvard Graphics 3.0)
            .ch4	Presentation (Charisma 4.0)
            .chd	Font descriptor (FontChameleon)
            .chi	Document (ChiWriter)
            .chk	Recovered data (ChkDsk)
            Temporary file (WordPerfect for Win)
            .chl	Configuration History Log
            .chm	Compiled HTML
            .chn	Data (Ethnograph 3)
            .cho	ChordPro file
            .chp	Chapter file (Ventura Publisher)
            .chr	Character set (Turbo C – Turbo Pascal)
            .cht	Chart (Harvard Graphics 2.0 – SoftCraft Presenter)
            Interface file for ChartMaster (dBASE)
            .chw	Compiled Help Index file
            .cid	AnalogX Caller ID file
            .cif	Caltech Intermediate Format graphics
            Chapter information (Ventura Publisher)
            .ciff	Canon CIFF
            .cil	Clip Gallery Download Package
            .cit	Intergraph Raster File Reference
            .cix	Database index (TCU Turbo C Utilities)
            .ckb	Keyboard mapping (Borland C++ 4.5)
            .cl	Common LISP source code file
            .cl3	Easy CD Creator Layout file
            .cl4	Easy CD Creator Layout file
            .cl5	Easy CD Creator Layout file
            .class	Java class file
            .clb	ICQ Contact List
            MS Office XP Developer Code Librarian
            cdrLabel Compact Disc Label
            .clg	Windows Catalog file
            .cli	Client Management System Customer file
            .clm	COLIMO file
            .clp	Clip art graphics (Quattro Pro)
            Clipboard file (Windows 3.x)
            Compiler script file (clip list) (Clipper 5)
            .clpi	Blue-ray Disc Clip Information file
            .clr	Color binary screen image (1st Reader)
            Color definitions (Photostyler)
            .cls	C++ class definition file
            .cm	Data file (CraftMan)
            .cmd	Batch file (OS/2)
            Command (dBASE – Waffle)
            External command menu (1st Reader)
            .cmf	FM-music file (Creative Music File)
            .cmg	CMG file
            .cmk	Card (Card Shop Plus)
            .cml	COMAL programming language
            .cmm	Cmm script (batch) file (CEnvi)
            .cmo	Virtools Composition file
            .cmp	Header file for PostScript printer files (CorelDRAW)
            User dictionary (MS Word for DOS)
            Bitmap graphics (Lead CMP compression)
            .cmq	Culturemetrics file
            .cmt	Culturemetrics file
            .cms	TrialDirector media storage
            .cmv	Animation (CorelMove CorelDraw 4.0)
            .cmx	Corel PhotoPaint Image
            Corel Presentation Exchange Image
            The Sims (Maxis) 3D Body Mesh Data
            Apple Viewer file
            .cnc	CNC general program data
            .cnd	ControlDraw file
            Embroidery Design file
            .cnf	Configuration (program – printer setup)
            .cnt	Helpfile contents
            .cnv	Data conversion support file (Word for Windows)
            Temporary file (WordPerfect for Win)
            .cob	Cobol source code file
            .cod	Datafile (Forecast Plus – MS Multiplan – StatPac Gold)
            Program compiled code (FORTRAN)
            Template source file (dBASE Application Generator)
            Videotext file
            .col	Color palette (Autodesk Animator – many)
            Spreadsheet (MS Multiplan)
            .com	Command (memory image of executable program) (DOS)
            .con	Configuration file (Simdir)
            .conf	Configuration file
            .config	Configuration file
            .cor	Protein Structure file
            Web GPS Correction Server Export file
            WMOVIEC Input file
            .cpd	Script (Complaints Desk)
            .cpe	MS Fax Cover Sheet
            .cpf	Fax (The Complete Fax)
            Clever Cache Profile file
            .cph	Corel Print House image
            .cpi	Code Page Information file (DOS)
            AVCHD Clip Information
            Colorlab Processed Image bitmap graphics
            .cpl	Control panel file (Windows 3.x)
            Presentation (Compel)
            .cpo	Corel Print House file
            .cpp	C++ source code file
            Presentation (CA-Cricket Presents)
            .cpr	Cubase Project file
            .cps	Backup of startup files by Central Point PC Tools autoexec.cps
            coloured postscript files
            .cpt	Compressed Mac file archive created by COMPACT PRO (ext-pc.zip)
            Corel Photo-Paint Image
            Encrypted memo file (dBASE)
            Template (CA-Cricket Presents)
            .cpx	Control Panel Applet
            Corel Presentation Exchange Compressed Drawing
            .cpy	Copy Books Data file
            .cpz	Music text file (COMPOZ)
            .cr2	Canon Raw Image file
            .crc	Total Commander CRC file
            .crd	Cardfile (Windows 3.x – YourWay)
            ColdRED Script file
            Guitar Chord file
            .crf	Cross-reference (MS MASM – Zortech C++)
            .crh	Links Games Course file
            MS Golf Image file
            .crp	Encrypted database (dBASE IV)
            .crs	File Conversion Resource (WordPerfect 5.1)
            .crt	Terminal settings information (Oracle)
            Security certificate (Windows Sharepoint)
            .crtr	Multi-Ad Creator 7 document
            .crtx	Microsoft Chart Template file
            .cru	Compressed file archive created by CRUSH
            .crw	Canon RAW Image file
            .crx	Chrome Extension file
            Links Games Course file
            .crz	Links Games Course file
            .cs	Visual C# Source file
            .csa	Comma Deliminated Text
            Ultimate Ride Roller Coaster
            .csf	Adobe Colour Settings file
            Van Dyke’s CRT/SecureCRT Script file
            .csg	Graph (Statistica/w)
            .csh	Hamilton Labs C Shell Script file
            .csk	Claris Works
            .csm	Precompiled headers (Borland C++ 4.5)
            .cso	Compressed ISO Image file
            .csp	PC Emcee Screen Image file (Computer Support Corporation)
            .css	Cascading Sheet Style file
            Datafile (CSS – Stats+)
            Datasheet (Statistica/w)
            .cst	Macromedia Director Cast file
            Panasonic music file (keyboard)
            .csv	Comma Separated Values text file format (ASCII)
            Adjusted EGA/VGA palette (CompuShow)
            .ct	Continous Tone file
            .ctc	Control file (PC Installer)
            .ctd	Cobra Track Dump
            Cardtable file
            Marine Data file
            Simpsons Cartoon Studio Export file
            .ctf	Character code translation file (Symphony)
            .ctg	Canon Catalog file
            Cartridge Definition file
            ChessBase Opening Book
            Canon Powershot Pro 70 Info file
            .ctl	Microsoft Visual Basic Control file
            Control file (dBASE IV – Aldus Setup)
            Setup information
            .ctn	CADTERNS file
            .ctt	Messenger contacts file
            Labview file
            .ctu	CZTU, a gamma-ray analysis program. Need the CTZU.exe file to work
            .ctx	Course TeXt file (Microsoft online guides)
            Ciphertext file (Pretty Good Privacy RSA System)
            .cty	SimCity City file
            .cue	MS Cue Cards data
            .cuf	C Utilities Form definition (TCU Turbo C Utilities)
            .cul	Windows cursor library (IconForge, ImageForge, ImageForge PRO)
            .cur	Cursor image file (Windows 3.x)
            .cut	Bitmap graphics (Dr. Halo)
            Dr Halo CUT files
            .cv4	Color file (CodeView)
            .cv5	Canvas version 5
            .cva	ACD Canvas Sequence Set file
            Compaq Diagnostics
            .cvb	Borland BDE File
            .cvd	Bitdefender
            .cvp	Cover page (WinFax)
            .cvr	WinFax Cover Sheet
            ElectraSoft Fax Cover Sheet
            .cvs	Graphics (Canvas)
            .cvt	Backup file for CONVERTed database file (dBASE IV)
            .cvw	Color file (CodeView)
            .cwk	Claris Works data
            .cwz	CropWalker file
            .cxf	Google Picasa Collage file
            .cxp	Core Media Player XML-based Playlist File
            .cxt	Macromedia Director Protected Cast file
            .cxx	C++ source code file (Zortech C++)
            .d	D programming language source code
            GBG DraftMaker Drawing File
            .d00	Blaster Master Pro File
            AdLib Format File
            .d10	H&R Block Deduction Pro file
            Drake Software Dat file
            .d2s	Character file (Diablo 2)
            .d3d	File Extension for Desktop-3D Notes
            Compressed Draw 3D file
            .d64	Commodore 64 Emulator Disk Image
            .dat	Data file in special format or ASCII
            Gunlok Archive
            Mitsubishi DJ-1000 and Photorun Native Format
            Nascar Racing Archive
            SPOT Graphic
            WordPerfect Merge Data
            .data	Sid Tune audio file
            .day	Journal file
            .db	Configuration (dBASE IV – dBFast)
            Database (Paradox – Smartware)
            .db$	Temperature debug info (Clarion Modula-2)
            Temporary file (dBASE)
            .db2	Database (dBASE II)
            .db3	Database (dBASE III)
            .dba	Datafile (DataEase)
            Palm Desktop Date Book Archive
            .dbb	ANSYS Database Backup
            Mopheus music file
            .dbd	Business data (Business Insight)
            Debug info (Clarion Modula-2)
            .dbf	Database file (dBASE III/IV – FoxPro – dBFast – DataBoss)
            Oracle 8.x Tablespace File
            .dbg	Symbolic debugging information (MS C/C++)
            .dbk	Database backup (dBASE IV)
            .dbl	Windows XP Activation file
            .dbm	Datafile (DataEase)
            Cold Fusion Template
            Menu template (DataBoss)
            .dbo	Compiled program (dBASE IV)
            .dbs	Database in SQL Windows format
            Datafile (PRODAS)
            Printer description file (Word – Works)
            .dbt	Data Base Text (Clipper)
            Foxbase+ style memo (FoxPro)
            Memo file for database w/same name (dBASE IV – dBFast)
            .dbw	Windows file (DataBoss)
            .dbx	Database
            DataBeam Image
            MS Visual Foxpro Table
            Outlook Express e-mail folder file
            .dca	Document Content Architecture text file (IBM DisplayWrite)
            .dcf	Disk image file
            .dcm	DCM Module Format
            Dicom
            .dcp	Data CodePage (OS/2)
            .dcr	Kodak Proprietary Image Format
            Shockwave file
            .dcs	Bitmap graphics (CYMK format) (QuarkXPress)
            Datafile (ACT! Activity Files)
            .dct	Database dictionary (Clarion Database Developer)
            Spell checking dictionary (Harvard Graphics 3.0 – Symphony)
            .dcx	FAX Image
            ElectraSoft Fax
            PC-Paintbrush file
            Bitmap Graphics (Multipage PCX)
            Macros
            MS Visual Foxpro Database Container
            .dd	Compressed Macintosh file archive created by DISKDOUBLER
            .ddat	DivX Temporary file
            .ddb	Bitmap graphics
            .ddc	DivX Descriptor Description File
            .ddf	MS Data Definition Language file
            .ddi	Diskdupe Image file (ddupe322.zip)
            .ddp	Device Driver Profile file (OS/2)
            .de	MetaProducts Download Express incompletely downloaded file
            .de7	Dance E jay 7 File
            .deb	Debug script (DOS Debug)
            .dec	VersaPro Declaration file
            .def	Assembly header file (Geoworks)
            DATAIR data entry format file
            Defaults – definitions
            .dem	Demonstration
            Graphics (VistaPro)
            .des	Description Text
            Tribes 2 Game file
            Quickbooks Template
            Pro/DESKTOP file
            Interscope BlackBox file
            .dev	Device driver
            .dfd	Data Flow Diagram graphic (Prosa)
            .dff	Criterion RenderWare 3.x 3D object format
            .dfi	Outline font description (Digifont)
            .dfl	Default program settings (Signature)
            FreshDownloads (FreshDownload List temp file)
            File Extension for Desktop-3D Notes
            .dfm	Data Flow Diagram model file (Prosa)
            .dfs	Delight Sound file
            .dft	Fakt2000 file
            SolidEdge CAD file
            Workshare Synergy file
            PC Draft file
            .dfv	Printing form (Word)
            .dfx	Drafix file
            .dgn	Graphics (MicroStation)
            .dgr	Fax Page (MS Outlook Express)
            DART Pro 98 File Group Details
            .dgs	Diagnostics
            .dh	Dependency information for .ph (Geoworks)
            .dhp	Dr. Halo PIC Format graphics (Dr. Halo II – III)
            .dht	Datafile (Gauss)
            .dhy	Adobe Bridge file
            .dia	Diagraph graphics (Computer Support Corporation)
            .dib	Bitmap graphics (Device-Independent Bitmap)
            .dic	Lotus Notes / Domino dictonary file
            .dif	Database (VisiCalc)
            Output from Diff command – script for Patch command
            Text file (Data Interchange Format)
            .dig	Digilink Format
            Sound Designer Audio File
            Text Document
            .dip	Graphics
            .dir	Adobe Director Movie File
            Dialing directory file (Procomm Plus)
            Directory file (VAX)
            Movie (MacroMind Director 4.x)
            .dis	DATAIR data import specification file
            Distribution file (VAX Mail)
            Thesaurus (CorelDraw)
            >	
            .divx	DivX Encoded Movie file
            .diz	Description file (Description In Zip)
            .dje	MattBatt iAM-player
            .djv	DJVu Scanned file
            .djvu	DJVu file
            .dkb	Raytraced graphics (DKBTrace)
            .dl	Animation (Italian origin)
            .dl_	Compressed .dll file in an Install Archive
            .dld	Data (Lotus 1-2-3)
            .dlg	Dialog resource script file (MS Windows SDK)
            .dll	Dynamic Link Library (Windows 3.x – OS/2)
            Export/import filter (CorelDRAW)
            .dls	Setup (Norton Disklock)
            .dmf	Delusion/XTracker digital music file
            Packed Amiga Disk Image
            .dmg	Macintosh OS X Disk Image file
            .dml	Medical Manager DML System Script
            .dmo	Demo (Derive)
            .dmp	Dump file (eg. screen or memory)
            .dms	Compressed Amiga file archive created by DISKMASHER
            .dmsk	DivX Web Player Temporary file
            .dna	Desktop DNA data storage file
            .dnasym	Desktop DNA compiled application script
            .dnax	Desktop DNA exclusion list (text)
            .dne	Netica Bayes net file (Norsys Software Corp.)
            .dng	Adobe Digital Negative fFile
            Dungeon file
            .dnl	DigitalWebBook Electronic Book
            netMod Modem Firmware Upgrade file
            .do	ModelSim Filter Design HDL Coder
            .doc	Document text file
            .docm	Open XML Macro-enabled Document file (Microsoft Word 2007 / Word 2010)
            .docx	Open XML Document text file (Microsoft Office 2007 / Office 2010)
            .dog	Screen file (Laughing Dog Screen Maker)
            .doh	Dependency information for .poh (Geoworks)
            .dol	Nintendo Executable file
            .dos	External command file (1st Reader)
            Network driver (eg. pkt_dis.dos)
            Text file containing DOS specific info
            .dot	Line-type definition file (CorelDRAW)
            Template (Word for Windows)
            .dotx	Microsoft Word 2007 / Word 2010 Template file
            .dox	Text file (MultiMate 4.0)
            .doz	Description Out of Zip (VENDINFO)
            .dp	Calendar file (Daily Planner)
            Data file (DataPhile)
            .dpg	Nintendo DS MPEG Video File
            .dpk	Delphi Package file
            .dpp	Serif DrawPlus Drawing
            .dpr	Default project- and state-related information (Borland C++)
            .dps	DivX Player Skin file
            .dpt	Desktop DNA template
            .dpx	Digital moving picture exchange format
            .dra	Map Maker Pro GIS vector layer
            .drs	Display Resource (WordPerfect for Win)
            .drv	Device driver eg. for printer
            .drw	Drawing (various)
            Vector graphics (Micrografx Designer)
            .ds	Twain Data Source file
            .ds4	Vector graphics (Micrografx Designer 4.0)
            .dsa	DasyTec DASYLab file
            .dsb	DasyTec DASYLab file
            .dsc	Discard file (Oracle)
            .dsd	Database (DataShaper)
            .dsf	Micrografx Designer
            PC-TRUST Document Signer
            Delusion/XTracker Digital Sample
            .dsk	Project desktop file (Borland C++ – Turbo Pascal)
            Simple IDs (database)
            .dsm	Digital sound module (DSI)
            .dsn	ODBC Data Source file
            Design (Object System Designer)
            .dsp	Display parameters (Signature)
            Graphics display driver (Dr.Halo)
            MS Developer Studio Project
            ReaderX and DragonStar Pro Ltd file extensions
            .dsp2	ReaderX and DragonStar Pro Ltd file extensions
            .dsr	Driver Resource (WordPerfect for Win)
            .dss	Screensaver file (DCC)
            Sound (Digital Soup)
            .dst	PC-RDist Distribution file
            Embroidery Machine Stitch file (VeePro)
            .dsw	Desktop settings (Borland C++ 4.5)
            .dsy	PC Draft Symbol Library
            .dt_	Data fork of a Macintosh file (Mac-ette)
            .dta	Data file (Turbo Pascal – PC-File – Stata)
            .dtd	SGML Document Definition file
            .dtf	Database file (PFS – Q&A)
            .dtp	Document (Timeworks Publisher3)
            Publication (Publish-It!)
            .dup	Duplicate Backup
            .dus	Readiris font dictionary
            .dvc	Data (Lotus 1-2-3)
            .dvf	DV Studio Camcorder Graphics file
            .dvi	Device Independent document (TeX)
            .dvp	Desqview Program Information file (DESQview)
            Device parameter file (AutoCAD)
            .dvr	Windows Media Center Recorded file
            DR-92 Manager file
            .dvr-ms	files created by Stream Buffer Engine(SBE)
            .dw2	Drawing (DesignCAD for windows)
            .dwc	Compressed file archive created by DWC (dwc-a501.exe)
            .dwd	Davka Writer file
            DiamondWare Digitized file
            .dwf	Autodesk WHIP! Drawing Web file
            MS WHIP autoCAD REader Drawing Web file
            .dwg	Drawing (Drafix)
            Drawing database (AutoCAD)
            .dwk	DADiSP Worksheet File
            .dwl	Drawing Lock file
            .dwt	AutoCAD Template/Prototype file
            Macromedia Dreamweaver Template file
            Demon’s World Game Texture file
            .dwz	DVD movieFactory 3
            .dx	Text file (DEC WPS/DX format – DEC WPS Plus)
            .dxf	Drawing Interchange File Format vector graphics (AutoCAD)
            .dxn	Fax (Fujitsu dexNET)
            .dxr	Adobe Director Movie File
            Dependable Strengths Administrator Resources
            Green Building Advisor file
            Macromedia Director Protected Movie file
            .dyc	ICUII Videochat file
            .dylib	Apple osx extension for lib
            .dyn	Data (Lotus 1-2-3)
            .dz	Dzip Compressed file
            .e3p	CIM-Team E3.series parts file
            .e3s	CIM-Team E3.series project file format
            .e3t	CIM-Team E3.series template file
            .e3v	CIM-Team E3.series viewer project file format
            .eap	Enterprise Architect Project file
            .ear	Java Enterprise Application Packaging Unit
            .eas	Elite Visual Basic API Spy
            .ebj	Error-checking object file (Geoworks)
            .ebo	MS Reader Ebook Format
            .ebp	Pocket PC WindowsCE Project file
            .ecf	Microsoft Outlook Add-on file
            Microsoft Exchange Extended Configuration file
            WinFax Office Add-in file
            .eco	NetManage ECCO file
            .ecw	Ensoniq Waveset Format
            EclipseCrossword Crossword Puzzle
            .edb	MS Exchange Database
            ROOTS3 geneological data
            .edl	Edit Decision List (management for video/film post production)
            .edr	Portable energy file – GROMACS 3.3
            .eds	Ensoniq SQ80 disk image
            .edt	Default settings (VAX Edt editor)
            .eeb	Button bar for Equation Editor (WordPerfect for Win)
            .efe	Ensoniq EPS file
            .eft	High resolution screen font (ChiWriter)
            .efx	Fax (Everex EFax)
            .ega	EGA display font (Ventura Publisher)
            .ek5	SonarData Echoview file
            .ek6	SonarData Echoview file
            .ekm	EXP: The Scientific Word Processor Macro
            .el	Elisp source code file (Emacs lisp)
            .elc	Compiled ELISP code (Emacs lisp)
            .elm	MS FrontPage Theme-Pack file
            .elt	Event list text file (Prosa)
            .email	Outlook Express Mail Message
            .emb	Everest Embedded Bank File
            .emd	ABT Extended Module
            .emf	Enchanced Metafile graphics
            .eml	Electronic Mail (Email) Message file
            .emp	E-Music File Format
            .ems	PC Tools Enhanced Menu System Config
            .emu	Terminal emulation data (BITCOM)
            .emx	Ensuredmail encrypted file/e-mail message
            IBM Rational modeller software
            .emz	Windows Compressed Enhanced Metafile
            .enc	Encoded file – UUENCODEd file (Lotus 1-2-3 – uuexe515.exe)
            Music (Encore)
            .end	Arrow-head definition file (CorelDRAW)
            .eng	Dictionary engine (Sprint)
            Graphics (charting) (EnerGraphics)
            .ens	EndNote Styles file
            .env	Enveloper macro (WOPR)
            Environment file (WordPerfect for Win)
            .eot	MS WEFT Embedded OpenType file
            .epd	Publication (Express Publisher)
            .epf	Encryption Protection (encrypted file format)
            The extension of the Entrust Profile files.
            .epi	Document (Express Publisher)
            .epp	EditPad Pro Project
            .eps	Encapsulated PostScript vector graphics (Adobe Illustrator)
            Printer font (Epson – Xerox…) (Ventura Publisher)
            .epub	Open Electronic Book file
            .eqn	Equation (WordPerfect for Win)
            .erd	Entity Relationship Diagram graphic file (Prosa)
            .erm	Entity Relationship Diagram model file (Prosa)
            .err	Error log
            Error messages for command line compilers
            .esp	Ventura file
            .esh	Extended Shell batch file
            .esl	MS Visual FoxPro Distributable Support Library
            .ess	EXP: The Scientific Word Processor Style Sheet
            .est	MS Streets & Trips 2001 Trip file
            .etf	Enriched Text file
            PolyEdit file
            .eth	Document (Ethnograph 3)
            .ets	eSignal Time and Sales file
            .etx	Structure Enhanced (setext) text
            .ev	SonarData Echoview file
            .evi	SonarData Echoview file
            .evl	SonarData Echoview file
            .evr	SonarData Echoview file
            .evt	Event log
            .evy	Document (WordPerfect Envoy)
            .ewd	Document (Express Publisher for Windows)
            .ewl	EclipseCrossword Word List
            Microsoft Encarta Document
            .ex	Norton Ghost Template File
            .ex_	Compressed .EXE File in an Install Archive
            .ex3	Device driver (Harvard Graphics 3.0)
            .exc	Rexx source code file (VM/CMS)
            Exclude file for Optimize (do not process) (QEMM)
            .exd	Control Information Cache
            .exe	Directly executable program (DOS)
            .exm	Msdos executable, system-manager compliant (HP calculator)
            .exp	ICQ Saved Chat file
            QuickBooks file
            .ext	Extension file (Norton Commander)
            .ext2fs	filesystem driver in the Linux kernel
            .exx	Intermediate file by MsgPut (IBM LinkWay)
            .ezf	Fax (Calculus EZ-Fax)
            .ezm	Text file
            .ezp	Edify Electronic Workforce Backup Utility
            .ezz	eZBackup backup file
            .f	Fortran source code file
            Compressed file archive created by FREEZE
            .f_i	Print IPS file
            .f01	Fax (perfectfax)
            .f06	Dos screen text font – height 6 pixels (fntcol13.zip)
            .f07	Dos screen text font – height 7 pixels (fntcol13.zip)
            .f08	Dos screen text font – height 8 pixels (fntcol13.zip)
            .f09	Dos screen text font – height 9 pixels (fntcol13.zip)
            .f10	Dos screen text font – height 10 pixels (fntcol13.zip)
            .f11	Dos screen text font – height 11 pixels (fntcol13.zip)
            .f12	Dos screen text font – height 12 pixels (fntcol13.zip)
            .f13	Dos screen text font – height 13 pixels (fntcol13.zip)
            .f14	Dos screen text font – height 14 pixels (fntcol13.zip)
            .f16	Dos screen text font – height 16 pixels (fntcol13.zip)
            .f2	FLASH BIOS file
            .f2r	Linear module (music) (Farandole)
            .f3r	Blocked module (music) (Farandole)
            .f4v	MP4 Video file
            .f77	Fortran 77 source code file
            .f90	Fortran file
            .f96	Fax (Frecom FAX96)
            .fac	Face graphics
            .faq	Frequently Asked Questions text file
            .far	Farandoyle Tracker Music Module
            The Sims (Maxis) Archive file
            .fav	MS Outlook Bar Shortcuts
            .fax	Fax (raster graphics) (most Fax programs)
            .fbc	FamilyTree Compressed backup file
            .fbk	Navison Financials Backup
            FamilyTree Backup file
            .fc	Spell checking dictionary (Harvard Graphics 2.0)
            .fcd	Virtual CD-ROM
            FastCAD/EasyCAD Output
            Patton & Patton Flow Charting 3 file
            IsoBuster file
            .fcm	Binary file patch file (forward compression)(jlpak10.zip)
            .fcp	FLAMES Checkpoint Restart file (Ternion)
            .fcs	Flow Cytometry Standard Format
            Fantasy Football League Organizer file
            RealProducer Pro Settings
            c-tree Server/Plus Data file
            Canon Zoom Browser EX file
            CD Trustee file
            Spectrum Server Log file
            .fcw	Campaign Cartographer 2 file
            .fd	Declaration file (MS Fortran)
            Field offsets for compiler (DataFlex)
            .fdb	Art Explosion Portfolio Catalog file
            Legacy Family Tree Database
            Navison Financials Database
            .fde	FLAMES Dataset Export file (Ternion)
            .fdf	Adobe Acrobat Forms document
            .fdr	Final Draft Document file
            Embroidery Design file
            .fdw	Form (F3 Design and Mapping)
            .feb	Button bar for Figure Editor (WordPerfect for Win)
            .fef	Steuer2001 file
            .fes	Fabio Editing Software
            3D Topicscape – exported fileless occurrence
            .fev	FLAMES Environment Variable file (Ternion)
            .ff	Outline font description (Agfa Compugraphics)
            .ffa	MS Fast Find file
            .fff	Fax (defFax)
            .ffl	MS Fast Find file
            .ffo	MS Fast Find file
            .fft	Dca/FFT Final Form Text text file (DisplayWrite)
            .ffx	Microsoft Fast Find file
            .fgd	Folder Guard Data
            Half-life Modification Map Configuration file
            Digital Raster Graphic Metadata file
            .fh3	Vector graphics (Aldus FreeHand 3.x)
            .fh4	Vector graphics (Aldus FreeHand 4.x)
            .fh5	Freehand 5
            .fh6	Freehand 6
            .fh7	Freehand 7
            .fh8	Macromedia Freehand 8
            .fh9	Macromedia Freehand 9
            .fh10	Macromedia Freehand 10
            .fi	Interface file (MS Fortran)
            .fif	Fractal Image Format file
            .fig	REND386/AVRIL Graphic
            Super Nintendo Game-console ROM Image
            .fil	File template (Application Generator)
            Files list object file (dBASE Application Generator)
            Overlay (WordPerfect)
            .fin	Print-formatted text file (Perfect Writer – Scribble – MINCE)
            .fio	PhotoStyler graphics (filter)
            ULead Viewer (support file)
            .fit	Fits graphics
            File Index Table (WindowsNT)
            .fix	Patch file
            .fky	Macro file (FoxPro)
            .fla	Adobe Flash file
            .flac	Free Lossless Audio Codec
            .flb	Format library (Papyrus)
            .flc	Animation (Autodesk Animator)
            .fld	Folder (Charisma)
            .fle	Flea program: outbound file and attachment required by the given mailer environment
            .flf	Corel Paradox Form
            Firehand Lightning Graphic Collection
            Navison Financials License file
            OS/2 Driver file
            FLAMES License file, Enterprise Edition (Ternion)
            .fli	Tex font library (EmTeX)
            Animation (Autodesk Animator)
            .flk	File Locker Encrypted file
            .flm	Film Roll (AutoCAD/AutoShade)
            .flo	Micrografx FlowCharter
            .flp	Adobe Flash Project file
            FlipAlbum file
            Fruityloops Saved file
            .flt	Asymetrix Graphics Filter Support file
            CoolEdit Pro Filter
            Corel Graphic Filter
            FileMaker Filter
            FLIC Animation (DTA)
            Micrografx Picture Publisher Filter
            MS Graphics Filter
            MulitGen Open Flight file
            OS/2 Warp Filter Device Driver
            StarTrekker Music Module
            WinFlash Educator Flashcard Compiled Test file
            .flv	Adobe Flash Video file
            .flx	Compiled binary (DataFlex)
            .fm	Spreatsheet (FileMaker Pro)
            FrameMaker file
            .fm1	Spreadsheet (Lotus 1-2-3 release 2.x)
            .fm3	Device driver (Harvard Graphics 3.0)
            Spreadsheet (Lotus 1-2-3 release 3.x)
            .fmb	File Manager Button bar (WordPerfect for Win)
            .fmf	Font or icon file (IBM LinkWay)
            .fmg	FreeMarkets Graphics Browser
            .fmk	Makefile (Fortran PowerStation)
            .fmo	Compiled format file (dBASE IV)
            .fmp	FileMaker Pro Document
            FLAMES Model Prototype file for components written in C (Ternion)
            .fmpp	FLAMES Model Prototype file for components written in C++ (Ternion)
            .fmt	Format file (dBASE IV – FoxPro – Clipper 5 – dBFast)
            Style sheet (Sprint)
            .fmv	Frame Vector Metafile
            .fmz	Form Z Program files (drawing program)
            .fn3	Font file (Harvard Graphics 3.0)
            .fnt	Font file (many)
            .fnx	Inactive font (Exact)
            .fo1	Font file (Borland Turbo C)
            .fo2	Font file (Borland Turbo C)
            .fol	Folder of saved messages (1st Reader)
            .fon	Dialing directory file (Telix)
            Font file (many – Windows 3.x font library)
            Log of all calls (Procomm Plus)
            .for	Fortran source code file
            Form (WindowBase)
            .fot	Installed Truetype font (Windows Font Installer)
            .fp	Configuration file (FoxPro)
            .fp3	FileMaker Pro 3.0 and earlier files
            Floor Plan 3D Drawing file
            .fp4	FileMaker Pro 4.0
            .fp5	FileMaker Pro 5.0 and later files
            .fpb	FLAMES Playback Recorder file (Ternion)
            .fpc	Catalog (FoxPro)
            .fpk	JetForm FormFlow file
            .fpr	FLAMES Prototype file (Ternion)
            .fpt	Memo (FoxPro)
            .fpw	Floorplan drawing (FloorPLAN plus for Windows)
            .fpx	FlashPix Bitmap
            .fqy	FLAMES FLARE Command file (Ternion)
            .fr3	Renamed dBASE III+ form file (dBASE IV)
            .frc	FLAMES Recorder Output file; FLARE Input file (Ternion)
            .frd	Files which contain loudspeaker frequency response data
            .fre	Creative Digital Blaster Digital VCR file
            Male Normal CT
            .frf	Font (FontMonger)
            .frg	Uncompiled report file (dBASE IV)
            .frl	FormFlow file
            .frm	MySQL Database Format file
            Form (Visual Basic)
            Report file (dBASE IV – Clipper 5 – dBFast)
            Text (order form)
            .fro	Compiled report file (dBASE IV)
            .frp	Form (PerForm PRO Plus – FormFlow)
            .frs	Screen Font Resource (WordPerfect for Win)
            .frt	Report memo (FoxPro)
            .frx	Report (FoxPro)
            .fs	F# Source Code file
            .fsc	FLAMES Scenario file (Ternion)
            .fsh	EA Sports Game Graphic Editor file
            .fsl	Form (Paradox for Windows)
            .fsm	Farandoyle Sample format music
            .fst	Linkable program (dBFast)
            .fsproj	Store Firestarter projects used to generate class mapping definitions for Habanero Firestarter
            .fsx	Data (Lotus 1-2-3)
            .fsy	Fileware’s Filesync
            .ftm	Font file (Micrografx)
            .fts	Windows Help Full-Text Search Index file
            .ftw	Family file
            FontTwister
            .ftp	Configuration (FTP Software PC/TCP)
            .fus	Files that store user settings for various FLAMES applications (Ternion)
            .fvt	Interlock Public Computer Utility
            .fw	Database (FrameWork)
            .fw2	Database (Framework II)
            .fw3	Database (Framework III)
            .fwp	FLAMES Window Viewer project file (Ternion).
            .fx	DirectX Effects file
            On-line guide (FastLynx)
            .fxd	Phonebook (FAXit)
            .fxm	WinFax/WinFax MiniViewer Fax
            .fxo	Fax Image Document
            .fxp	Compiled format (FoxPro)
            .fxr	WinFax Received Document
            .fxs	Fax Transmit Format graphics (WinFax)
            .g	Data chart (APPLAUSE)
            .g3	Group 3 Fax document; Group 3 Fax
            .g3f	Zetafax TIFF file (fine resolution)
            .g3n	Zetafax TIFF file (normal resolution)
            .g8	Raw graphics (one byte per pixel) plane three (PicLab)
            .gab	Global Address Book file
            .gal	Corel Multimedia Manager Album
            .gam	Saved Game file
            Fax (GammaFax)
            TADS 2.x Game file
            Baldur’s Gate Game file
            Animated E-mail
            .gat	Gator file
            .gb	Pagefox Bitmap Image file
            GameBoy ROM
            .gba	Game Boy Advanced ROM
            GrabIt Batch files
            .gbc	Game Boy COlor ROM
            .gbd	Gator Banner file
            .gbl	Global definitions (VAXTPU editor)
            .gbr	GIMP Brush file
            Gerber Format file
            .gbx	Gerber file
            .gc1	Lisp source code (Golden Common Lisp 1.1)
            .gc3	Lisp source code (Golden Common Lisp 3.1)
            .gcd	Graphics
            .gcf	Steam GCF File
            .gdb	Interbase Database
            Group Mail file
            .gdf	Dictionary file (GEOS)
            .gdr	Bitmap Font file (SymbianOS)
            .ged	Editor’s native file format (Arts & Letters)
            GEDCOM Family History file
            Graphic Environment Document
            Graphics editor file (EnerGraphics)
            Game Editor Project File
            .gem	Vector graphics (GEM – Ventura Publisher)
            .gen	Compiled template (dBASE Application Generator)
            Generated text (Ventura Publisher)
            Genius Family Tree
            .geo	Geode (Geoworks)
            .gfb	Compressed GIF image created by GIFBLAST (gifblast.exe)
            .gft	Font (NeoPaint)
            .gfx	Genigraphics Graphics Link Presentation
            Graphic format used by Allen Bradley SCADA Software (RSView Works)
            .gg	Google Desktop Gadget file
            .gho	Symantec Ghost Disk image file
            .ghs	Lasertank High Scores
            Symantec Ghost Disk Image Span file
            .gib	Chart (Graph-in-the-Box)
            .gid	Windows Help index file
            .gif	Graphics Interchange Format bitmap graphics (CompuShow)
            .gig	Sound file
            .giw	Presentation (Graph-in-the-Box for Windows)
            .gl	Animation (GRASP GRAphical System for Presentation)
            .glm	Datafile (Glim)
            .gls	Datafile (Across)
            .gly	Glossary (MS Word)
            .gmd	Game Maker file format
            .gmf	CGM graphics (APPLAUSE)
            .gml	Geography Markup Language file
            .gmp	Geomorph tile map (SPX)
            .gno	Genopro Genealogy Document file
            .gnt	In MF COBOL a compiled .cbl file
            .goc	Goc source code file (Geoworks)
            .goh	Goc header file (Geoworks)
            .gp	Geode parameter file (Geoworks Glue)
            .gp3	CCITT Group 3 file
            GuitarPro 3
            .gp4	Guitar Pro version 4.06
            .gpd	VISUAL EPR Input Data for PARAMS.EXE
            .gph	Graph (Lotus 1-2-3/G)
            .gpk	Omnigo program package
            .gpx	GPS eXchange Format
            .gr2	Screen driver (Windows 3.x)
            .gra	Datafile (SigmaPlot)
            .grb	Ms-DOS Shell Monitor file (MS-DOS 5)
            .grd	Gradebook Power file
            Map Projection Grid file
            .grf	Micrografix Image file
            Graph file (Graph Plus – Charisma)
            .grl	Matlab Graphic Format
            .grp	Group file (Windows 3.x – Papyrus)
            Pictures group (PixBase)
            .grx	File list (GetRight)
            .gry	Raw GREY graphics
            .gs1	Presentation (GraphShow)
            .gsd	Vector graphics (Professional Draw)
            GSplit file splitting utility (GDGsoft.com)
            .gsm	Raw GSM 6.10 Audio Stream
            Sound file
            US Robotics modem file
            .gsp	Geometer’s Sketchpad Material file
            .gsw	Worksheet (GraphShow)
            .gtp	Gnome Desktop Theme file
            GuitarPro file
            .gts	Genome Software Tempo Alarm Clock
            .gup	Data (PopMail)
            .gwi	Groupwise File
            .gwp	Greetings WorkShop file
            .gxd	General CADD Pro file
            GX-Reports file
            Jeol EX Spectrometer Data file
            .gxl	Graphics library (Genus)
            .gxt	GTA2 Game file
            .gym	Sega Genesis Music Logged Format
            .gz	Compressed file archive created by GZIP (GNU zip)
            .gzip	Compressed file archive created by GZIP (GNU zip)
            .h	Header file
            .h!	On-line help file (Flambeaux Help! Display Engine)
            .h++	Header file (C++)
            .h–	Header file (Sphinx C–)
            .ha	Compressed file archive created by HA (ha098.zip)
            .ham	Image file
            .hap	Compressed file archive created by HAP (hap303re.zip)
            .hbk	Handbook (Mathcad)
            .hbs	eBerry Transparent Animation – compressed bitmap files
            .hcr	IBM HCD/HCM Production Configuration
            .hdf	Hierarchical Data File graphics (SDSC Image Tools)
            Help file (Help Development Kit)
            .hdl	Alternate download file listing (Procomm Plus)
            .hdp	HD Photo File
            Magix Music/Video
            .hdr	InstallShield Setup header
            Pc-File+ Database header
            Datafile (Egret)
            Message header text (Procomm Plus – 1st Reader)
            .hds	Windows Digital Right Management file
            .hdw	Vector graphics (Harvard Draw)
            .hdx	Help index (AutoCAD – Zortech C++)
            .hed	HighEdit document
            .hex	Hex dump
            .hfi	Hp Font Info file (GEM)
            .hfx	HotFax file
            US Robotics Rapid Comm Voice Data file
            .hgl	Hp Graphics Language graphics
            .hh	C++ header file
            .hhc	Table of Contents file
            TurboTax Contents file
            .hhh	Precompiled header file (Power C)
            .hhk	Help Workshop Index file
            .hhp	Help information for remote users (Procomm Plus)
            .hht	MS Messenger file
            .hin	Molecule (HyperChem)
            .his	Insight II Dynamics Trajectory History file
            Spy-CD CD Search Database file
            .hlb	Help library (VAX)
            .hlp	Help information
            .hlz	Multi-Edit Packed Help file
            .hm3	Help & Manual 3 project Format
            .hmm	Alternate Mail Read option menu (Procomm Plus)
            .hnc	CNC program files Heidenhain (?) dialog
            .hof	Hall Of Fame (game scores)
            .hp8	Ascii text HP Roman8 character set (NewWave Write)
            .hpf	Hp LaserJet fonts (PageMaker)
            .hpg	HPGL plotter file vector graphics (AutoCad – Harvard Graphics)
            .hpi	Font information file (GEM)
            .hpj	Help project (MS Help Compiler)
            .hpk	Compressed file archive created by HPACK (hpack75.zip)
            .hpm	Emm text (HP NewWave)
            Alternate Main menu for privileged users (Procomm Plus)
            .hpp	C++ header file (Zortech C++)
            .hqx	Compressed Macintosh ASCII archive created by BINHEX (xbin23.zip)
            .hrf	Graphics (Hitachi Raster Format)
            .hrm	Alternate Main menu for limited/normal users (Procomm Plus)
            .hs2	Monochrome image (Postering)
            .hsi	Handmade Software Inc. graphics – almost JPEG (Image Alchemy)
            .hst	Yahoo Messenger History file
            History file (Procomm Plus)
            .hta	Hypertext application
            .htc	HTML Component (mechanism for implementing Dynamic HTML in script)
            .htf	WebBase File
            .hti	WebBase File
            .htm	HyperText Markup Language document
            .html	HyperText Markup Language document
            .htr	Motion Analysis Software Skeletal file
            .htt	Hypertext template
            .htx	Hypertext file
            .hus	Husqvarna Designer I Embroidery Machine Format
            .hwd	Presentation (Hollywood)
            .hxm	Alternate Protocol Selection menu for all users (Procomm Plus)
            .hxx	C++ header file
            .hy1	Hyphenation algorithms (Ventura Publisher)
            .hy2	Hyphenation algorithms (Ventura Publisher)
            .hyc	Data (WordPerfect)
            .hyd	Hyphenation dictionary (WordPerfect for Win)
            .hyp	Compressed file archive created by HYPER (hyper25.zip)
            .hyt	VFSMOD Project output file
            .i	Intermediate file (Borland C++ 4.5)
            .iaf	MS Outlook 97 and 2000 e-mail account settings
            .iax	Bitmap graphics (IBM Image Access eXecutive)
            .ibm	Compressed file archive created by ARCHDOS (Internal IBM only)
            .ibd	Installer Dialog Resource file
            .ibp	Isobuster Image file
            .ibq	Isobuster Managed Image file
            .ica	Bitmap graphics (Image Object Content Architecture)
            .icb	Bitmap graphics
            .icc	Kodak Printer Image
            IronCAD Catalog
            .icd	IronCAD 2D CAD file
            .icl	Icon library (ActivIcons, IconForge, ImageForge, ImageForge PRO)
            .icm	Image Color Matching Profile file
            ICC Profile, Acer Monotor Drive
            .icn	Icon source code file
            .ico	Icon (Windows 3.x)
            .ics	iCalendar Calendar file
            .id	Disk identification file
            Lotus Notes User ID file
            .id2	Windows Live Messenger Emoticon file
            .idb	Database Used by Disassembler
            MS Developer Intermediate file
            .ide	Project (Borland C++ 4.5)
            .idf	ARTiSAN Real-time Studio ID file
            MIDI Instruments Drivers file
            .idl	MS Visual C++ Interface Definition file
            OMG CORBA Interface Definition Language
            .idw	Vector graphics (IntelliDraw)
            .idx	Index (many – FoxPro)
            .ies	Photometric file data
            .ifd	Form (JetForm Design)
            .iff	Interchange File Format bitmap graphics/sound (Amiga)
            Maxis The Sims Object file
            Philips CDI File
            Sun TAAC Image File Format (SDSC Image Tool)
            .ifo	Saved graphic objects (ImageForge PRO)
            .ifp	Script (KnowledgeMan)
            .ifs	Fractal image compressed file (Yuvpak)
            System file (OS/2) hpfs.ifs
            .igr	Intergraph SmartSketch Drawing
            .igs	IGES-Format
            .igx	iGrafx Process
            .iif	QuickBooks for Windows Interchange file
            .ilb	Data (Scream Tracker)
            .ilk	Outline of program’s format (MS ILink incremental linker)
            .im30	Sun Raster image file
            .im8	Sun raster graphics
            .ima	Mirage vector graphics (EGO, Chart, Autumn)
            .imb	IncrediMail file
            .imc	IncrediMail file
            .imd	Caseware IDEA (GIS data file)
            .imf	ImageForge/IconForge saved filtered brushes(IconForge, ImageForge, ImageForge PRO)
            .img	Bitmap graphics (Ventura Publisher – GEM Paint)
            .imm	IncrediMail Trash
            .imn	IncrediMail Notifier
            .imp	Spreadsheet (Lotus Improv)
            Impaticized PowerPoint file
            .imq	Image presentation (ImageQ)
            .ims	Incredimail Graphic
            .imv	Yahoo Instant Messenger IMVironment
            Impaticized Video format
            .imw	Imageware Surfacer 3D CAD Surface Geometry
            IncrediMail Sound
            .imz	Compressed floppy image
            .in$	Installation file (HP NewWave)
            .in3	Input device driver (Harvard Graphics 3.0)
            .inb	Test script (Vermont HighTest)
            .inc	Include file (several programming languages)
            .ind	Index (dBASE IV)
            Adobe InDesign document file
            .indd	Adobe InDesign file format
            .inf	Type 1 LaserJet font information file (soft font installers)
            Information text file (ASCII)
            Install script
            .ini	Initialization file
            .ink	Pantone reference fills file (CorelDRAW)
            .inl	MS Visual C++ Inline Function file
            .inp	GIS Software Text Input file
            Oracle Source Code
            Self-Extracting Archive Utility Project
            .ins	Data (WordPerfect)
            Installation script (1st Reader)
            Instrument music file (Adlib)
            .int	Borland Interface Units
            Program saved in Internal (semi-compiled) format (Signature)
            .inv	Rogue Spear Inventory file
            .inx	Foxpro Index (Foxbase)
            .io	Compressed file archive created by CPIO
            .iob	3d graphics database in TDDD format
            .ioc	Organizational chart (Instant ORGcharting!)
            .ion	4dos descript.ion file (file descriptions)
            .ipa	iPod/iPhone Application file
            .ipd	BlackBerry Backup file
            InstallPROG 6 EDBS Install Database
            .ipg	Mindjongg Format
            .ipj	Impatica OnCue Project file
            .ipl	Pantone Spot reference palette file (CorelDRAW)
            .ipp	Help & Manual Proprietary Image
            .ips	Game Patch file
            MENSI 3Dipsos
            .ipsw	IPod/IPad/IPhone Software file
            .ipx	IPIX AV file
            .ipz	ICQ Skin Plus
            .iri	IR Image file
            .irs	Resource (WordPerfect)
            .isd	Spelling Checker dictionary (RapidFile)
            .ish	Compressed file archive created by ISH
            .isk	Command file
            .iso	Easy CD Creator Disc Image
            File List for CD-ROM
            InstallShield Uninstall file
            ISO Buster file
            ISO-9660 Table
            RichWin
            Vector Graphics (IsoDraw Illustration)
            .isr	MS Streets & Trips Route file
            .iss	InstallShield Response file
            ISS Graphic
            .ist	Digitrakker Instrument File (n-FaCToR)
            .isu	InstallShield Uninstall Script
            Easy CD Creator 4 Uninstall file
            Netscape file
            .isz	An extension on .ISO that allows compression and splitting of an archive
            .it	Settings (intalk)
            .itc2	iTunes Album Data file
            .itdb	iTunes Database file
            .itf	Interface file (JPI TopSpeed Pascal)
            .ith	InTether technology secured file
            .itl	Music Library file
            .iv	OpenInventor files (the successor to Inventor)
            .iva	security video data file
            .ivt	MS Infoviewer Title
            .iw	Presentation flowchart (IconAuthor – HSC InterActive)
            .iwa	Text file (IBM Writing Assistant)
            .iwd	Call of Duty Game Data file
            .iwp	Text file (Wang)
            .izt	Izl binary token file (IZL)
            .j01	File Extension from ADP Payroll Company
            .jad	Java Application Descriptor extension (for installing MIDlets)
            .jar	Java archive file
            .jas	Graphics
            .jav	Java source code file
            .java	Java source code file
            .jbc	Jam Byte-Code Hex file
            BestCrypt File
            .jbd	Datafile (SigmaScan)
            .jbf	Paint Shop Pro browser file
            .jbk	Juno Backup file
            .jbr	Jasc Paint Shop Pro Brush
            .jbx	Project file (Project Scheduler 4)
            .jdt	Accelio Capture Classic Filler
            .jef	Janome NH10000 Sewing Machine file
            .jet	Fax (Hybrid JetFax)
            .jff	Bitmap graphics (JPEG File Interchange Format)
            .jfif	JPEG image
            .jfx	J2 Fax File
            .jhtml	Dynamo Server Page
            .jif	JPEG/JIFF Image
            Jeff’s Image Format
            .jmx	JMeter file
            .jnb	Sigma Plot Workbook file
            .jnl	Ingres Journal file
            .jnlp	Java Web Start file
            .jnt	Windows Journal Note file
            .job	Job file
            Task Scheduler Task Object
            AI Research file
            QuestVision Vector Graphics file
            .jor	Journal file SQL
            .jou	Journal backup (VAX Edt editor)
            .jp2	JPEG 2000 file
            .jpc	Graphics (Japan PIC)
            .jpeg	JPEG image
            .jpf	JPEG 2000 file
            .jpg	Bitmap graphics (Joint Photography Experts Group)
            .jps	Stereo Image
            .jpx	JBuilder Project file
            .js	Microsoft Scripting Language “JScript” file extension
            .jsd	eFAX Jet Suite Document
            .jse	JScript Encoded Script file
            .jsf	Fireworks Batch Script file
            .jsh	Henter-Joyce, Inc. Jaws Script Header file
            .json	JavaScript Object Notation file
            .jsp	Java Server page
            .jtf	Fax (Hayes JT Fax)
            Bitmap graphics (JPEG Tagged Interchange Format)
            .jtp	Jetform file
            .jup	(New Planet Software) Code Crusader user’s project preferences file
            .jw	Text document (JustWrite)
            .jwl	Library (JustWrite)
            .jwp	Easy CD Creator Label file
            JWP Document
            .jxr	JPEG XR file
            .jzz	Spreadsheet (Jazz)
            .kar	Midi file with karaoke word track
            .kau	Sassafras KeyAudit Audit file
            .kb	Keyboard script (Borland C++ 4.5)
            Program source (Knowledge Pro)
            .kbd	Keyboard mapping (LocoScript – Signature – Procomm Plus)
            .kbm	Keyboard mapping (Reflection 4.0)
            .kcl	Lisp source code (Kyoto Common Lisp)
            .kcp	Keychamp file
            .kdc	Kaspersky Virus Database file
            Kodak Photo-Enhancer/Photogen file
            .keo	Older, outdated Print Shop extension
            .ket	Older, outdated Print Shop extension
            .kex	Macro (KEDIT)
            .kext	Mac OS X Kernel Extension
            .key	Datafile (Forecast Pro)
            Keyboard macros
            WinRAR License file
            Security file eg. Shareware Registration info
            .kgb	KGB Archive file
            .kit	Raven Toolkit file
            .kix	KixTart Script
            .kma	Kodak Memory Book file
            Correlate K-Map
            .kml	Keyhole Markup Language file
            .kmp	Korg Trinity KeyMaP file
            .kmx	Kaufman Mmail Warrior Mail Folder
            .kmz	Google Earth Map Location file
            .kos	MicroType Pro Document
            .kp2	Kruptos Encrypted file
            .kpl	Kazaa Playlist
            KPL Source Code
            .kpp	Toolpad (SmartPad)
            .kps	Ibm KIPS bitmap graphics
            .kqb	Knowledge Question Base file
            .kqe	W32/Spybot.KQE Worm virus
            .kqp	Konica Quality Picture
            .krz	Kurzweil 2000 Sample
            .ksd	Native Instruments Audio Patch file
            .ktk	Kutoka’s Mia
            .kwi	Navigation Data file
            .kwm	WebMoney Private Key file
            .kyb	Keyboard mapping (FTP Software PC/TCP)
            .l	Lex source code file
            Lisp source code file
            Linker directive file (WATCOM wlink)
            .l01	ARC Digitized Raster Graphics
            .lab	Datafile (NCSS – SOLO)
            Mailing labels (Q+E for MS Excel)
            .lang	Skype Language file
            .lat	Crossword Express Lattice file
            .latex	LaTeX typesetting system
            .lay	Word chart layout (APPLAUSE)
            .lbg	Label generator data (dBASE IV)
            .lbl	Label (dBASE IV – Clipper 5 – dBFast)
            .lbm	Bitmap graphics (DeluxePaint)
            Linear bitmap graphics (XLib)
            .lbo	Compiled label (dBASE IV)
            .lbr	Compressed file archive created by LU (lue220.arc)
            Display driver (Lotus 1-2-3)
            .lbt	Label memo (FoxPro)
            .lbx	Label (FoxPro)
            .lcf	Linker Control File (Norton Guides compiler)
            .lck	Lockfile (Paradox)
            .lcl	Data (FTP Software PC/TCP)
            .lcn	Lection (WordPerfect)
            .lcs	Datafile (ACT! History Files)
            L0phtCrack Audit file
            .lcw	Spreadsheet (Lucid 3-D)
            .ld	Long Distance codes file (Telix)
            .ld1	Overlay file (dBASE)
            .ldb	Data (MS Access)
            .ldf	Library definition file (Geoworks Glue)
            locking data file or (locking security file)
            IBM Works for OS/2 Filer Form
            Microsoft SQL Server Transaction Log File
            .ldif	LDAP Data Interchange Format
            .leg	Legacy Graphic Format
            .les	Lesson (check *.cbt)
            .let	Letter
            .lev	Level file (NetHack 3.x)
            .lex	Lexicon (dictionary) (many)
            .lfa	LifeForm file
            .lft	Laser printer font (ChiWriter)
            .lg	Logo procedure definitions (LSRHS Logo)
            .lgc	Program Use Log file
            .lgo	Logo for header and footer (SuperFax)
            Startup logo code (Windows 3.x)
            .lgx	Gerber file
            .lha	Compressed file archive created by LHA/LHARC (lha255b.exe)
            .lhw	Compressed Amiga file archive created by LHWARP
            .lib	Library file (several programming languages)
            .lic	License file (Shareware)
            FLAMES License File Professional Edition (Ternion)
            .lid	Kodak Gallery Album file
            WinDVD file
            Light Field Description file
            Dylan Library Interchange Description
            LabelVision Auto Incrementing Value file
            Maple V Setup file
            Scholar’s Aid Backup file
            .lif	Logical Interchange Format data file (Hewlett-Packard)
            Compressed file archive
            .lim	Compressed file archive created by LIMIT (limit12.zip)
            .lin	Line types (AutoCAD)
            .lis	Listing (VAX)
            .lit	MS Reader eBook file
            .lix	Extend Simulation Library file
            Libronix DLS Resource (LLS 2.x Index)
            .lj	Text file for HP LJ II printer
            .lko	MS Outlook Express Linked Object
            .ll3	Laplink III related file (document) (LapLink III)
            .lmp	Lump File
            .lmt	Nokia PC Suite Log file
            RPG Maker map tree file
            .lnd	3D Landscape Data
            .lng	Adobe Acrobat Language Plugin file
            Diablo II file
            NRG SDR Language file
            .lnk	Windows Shortcut file
            Linker response file (.RTLink)
            .loc	MicroSim PCBoard Component Locations Report
            Suppose Locations file
            Download format for search results on Geocaching.com
            .lod	Load file
            .log	Log file
            .lok	Encrypted and compressed archive format (FileWrangler, SecurDesk!, ZipWrangler)
            .lpc	Printer driver (TEKO)
            .lpd	Helix Nuts and Bolts File
            Avery Label Pro
            .lpf	Lytec’s Direct Electronic Medical Claims ClaimsDirect
            .lpi	Live Pictures
            .lpk	Licensed ActiveX Control for Internet Explorer.
            .lrf	Linker response file (MS C/C++)
            .lrs	Language Resource File (WordPerfect for Win)
            .lse	Nokia Audio Manager
            .lsf	Streaming Audio/Video file
            Libronix DLS Resource
            .lsl	Lotus Script Library
            .lsp	Lisp source code file (Xlisp)
            .lss	Spreadsheet (Legato)
            .lst	Keyboard macro (1st Reader)
            List file (archive index – compiler listfile)
            Spool file (Oracle)
            SAS Program file
            .lt2	e frontier Poser file
            .ltm	Form (Lotus Forms)
            .ltr	Letter
            .lua	Lua Source Code file
            .lvl	Game Level file
            .lvp	Lucent Voice Player
            LView Pro
            .lwa	LightWorks Archive Material/Scene file
            .lwd	Text document (LotusWorks)
            .lwo	NewTek Lightwave Object
            .lwp	IBM Word Pro / Lotus Word Pro 96/97 document file
            .lwz	MS Linguistically Enhanced Sound file
            .lx	Lexico – files with source code
            .lyr	DataCAD Layer file
            .lzd	Difference file for binaries (Ldiff 1.20)
            .lzh	Compressed file archive created by LHA/LHARC (lha255b.exe)
            .lzs	Compressed file archive created by LARC (larc333.zip)
            .lzw	Compressed Amiga file archive created by LHWARP
            .lzx	Compressed file
            .m	Function (program) (Matlab)
            Macro module (Brief)
            Standard package (Mathematica)
            .m11	Text file (MASS11)
            .m1v	MPEG-1 Video file
            .m2p	MPEG-2 Program Stream Format file
            .m2ts	BDAV MPEG-2 file
            .m2v	MPEG-2 Video Only file
            .m3	Modula 3 source code file
            .m3d	3D animation macro
            .m3u	Music Playlist (Winamp)
            .m4	M4 preprocessor file (unix)
            .m4a	MPEG-4 Audio Layer
            .m4b	MPEG-4 Audio Book file
            .m4p	MPEG-4 Encoded Audio file
            .m4r	iPhone Ringtone file
            .m4v	Apple Video file
            .m_u	Backup of boot sector, FAT and boot dir (MazeGold)
            .ma3	Macro (Harvard Graphics 3.0)
            .mac	Bitmap graphics (Macintosh MacPaint)
            Macro
            .mad	MS Access Module Shortcut
            .maff	Mozilla Archive Format file
            .mag	Woody Lynn’s MAG graphics format (MPS Magro Paint System)
            .mai	Mail (VAX)
            .mak	Makefile
            Project file (Visual Basic)
            .man	Command manual
            .map	Color palette
            Format data (Micrografx Picture Publisher)
            Linker map file
            Map (Atlas MapMaker)
            Network map (AccView)
            .mar	Mozilla Archive
            Microsoft Access Report file
            Assembly program (VAX Macro)
            .mas	Smartmaster set (Freelance Graphics)
            .mat	Data file (Matlab)
            Microsoft Access Shortcut file
            .max	Max source code file
            Microsoft Data Analyser View
            .mb	Memo field values for database (Paradox)
            .mbf	MS Money Backup file
            .mbk	Multiple index file backup (dBASE IV)
            Medisoft for Windows Backup
            .mbx	Mailbox (Eudora/Zerberus)
            .mcc	Configuration file (Mathcad)
            .mcd	Document (Mathcad)
            .mcf	Mathcad font
            Meta Content Format file
            Master Command file
            TMPGEnc template
            .mci	Mci command script (Media Control Interface)
            .mcp	Application script (Capsule)
            Printer driver (Mathcad)
            .mcr	DataCAD Keyboard macro file
            .mcw	Text file (MacWrite II)
            .mcx	Graphic file
            .md	Compressed file archive created by MDCD (mdcd10.arc)
            .md5	MD5 Checksum file
            Message Digest 5 (Easy MD5 Creator)
            .mda	Data (MS Access)
            .mdb	Database (MS Access)
            .mde	Microsoft Access MDE database
            .mdf	Accelio Capture Classic (JetForm) Filler
            I-deas Master Drafting Machine Data file
            Menu Definition file
            MS-SQL Master Database file
            Alcohol 120% CD Image File
            .mdi	Microsoft Office 2003 imaging format
            Borland multiple document interface
            .mdk	Keyboard Map file
            .mdl	Model (3D Design Plus)
            Spreadsheet (CA-Compete!)
            .mdm	Modem definition (TELIX)
            .mdmp	Microsoft Windows XP Trouble Report
            .mdr	FaxTalk Modem Doctor Modem Report file
            .mdt	Data table (MS ILink incremental linker)
            .mdx	Multiple index file (dBASE IV)
            .mdz	MS Access Wizard Template
            .me	Usually ASCII text file READ.ME
            .meb	Macro Editor bottom overflow file (WordPerfect Library)
            .med	Macro Editor delete save (WordPerfect Library)
            Music (OctaMED)
            .mem	Macro Editor macro (WordPerfect Library)
            Memory variable save file (Clipper – dBASE IV – FoxPro)
            .meq	Macro Editor print queue file (WordPerfect Library)
            .mer	Macro Editor resident area (WordPerfect Library) (vakioalue)
            .mes	Macro Editor work space file (WordPerfect Library)
            Message
            .met	Document (Omnipage Pro)
            eDonkey2000 file
            Macro Editor top overflow file (WordPerfect Library)
            Presentation Manager Meta file
            .meu	Menu group (DOS Shell)
            .mex	Mex file (executable command) (Matlab)
            Macro Editor expound file (WordPerfect Library)
            Mioplanet mex reader interactive file
            .mf	Metafont text file
            .mfx	ImageMAKER Fax Viewer folder file
            .mgf	Font (Micrografx)
            .mgi	Modular Gateway Interface
            .mgp	MagicPoint Presentation file
            .mhp	MS Home Publishing Project
            .mht	MS MHTML Document
            .mia	MusicIndiaOnline player music file
            .mib	Snmp MIB file
            .mic	Microsoft Image Composer file
            .mid	Standard MIDI file (music synthetizers)
            .mif	Maker Interchange Format (FrameMaker)
            .mii	Datafile (MicroStat-II)
            .mim	MIME file
            .mio	Multimedia Interactive Object
            .mip	Paint Shop Pro Multiple Image Print file
            .mis	Delta Force Land Warrior Mission
            MagicInstall Installation Script
            Tribes 2 Game file
            .mix	Object file (Power C)
            .mk	Makefile
            .mkd	Pervasive Btrieve files
            .mke	Makefile (MS Windows SDK)
            .mki	Japanese graphics MAKIchan format (MagView 0.5)
            .mks	Data (TACT)
            .ml3	Project (Milestones 3.x)
            .mlb	Macro library file (Symphony)
            .mlm	Novel Groupwise e-mail file
            .mm	Text file (MultiMate Advantage II)
            .mmc	Media Catalog
            MSoffice Media Content
            .mmd	Peristudio/PeriProducer file
            .mmf	Mail message file (MS Mail)
            .mml	Mail Meta Language
            .mmm	Movie (RIFF RMMP format) (MacroMind Director 3.x)
            .mmo	Memo writer file (RapidFile)
            .mmp	Output video format from Bravado board
            .mmx	Command & Conquer Red Alert 2 Map file
            Oracle Forms Compiled Menu
            .mmz	MusicMatch Theme file
            .mnd	Menu source (AutoCAD Menu Compiler)
            .mng	Map (DeLorme Map’n’Go)
            .mnt	Menu memo (FoxPro)
            .mnu	Advanced macro (HP NewWave)
            Menu (AutoCAD Menu Compiler – Norton Commander – Signature)
            .mnx	Compiled menu (AutoCAD)
            Menu (FoxPro)
            .mny	Account book (MS Money)
            .mob	Device definition (PEN Windows)
            .mod	Modula-2 source code file (Clarion Modula-2)
            Windows kernel module
            Music (FastTracker – many)
            .mol	MDL Molfile
            .mon	Monitor description (ReadMail)
            .mov	QuickTime Video Clip
            Apple QuickTime Audio
            AutoCAD AutoFlix Movie
            .mp2	Mpeg audio file (xing)
            .mp3	mp3PRO Audio file
            MPEG Audio Stream, Layer III
            SHARP MZ-series Emulator file
            Wrapster Wrapped file
            .mp4	MPEG-4 Video File
            .mpa	MPEG Audio Stream, Layer I, II or III
            .mpc	Calender file (MS Project)
            .mpd	MS Project database file
            .mpe	MPEG Movie Clip
            .mpeg	MPEG Movie Clip
            .mpf	MS Design Gallery
            MosASCII Project Workspace file
            .mpg	MPEG-1 animation
            .mpl	Playlist Data file
            .mpls	Blu-ray Information file
            .mpm	Mathplan macro (WordPerfect Library)
            .mpp	Project file (MS Project)
            CAD Drawing File
            .mpq	Blizzard Game Data file
            .mpr	Generated program (FoxPro)
            .mps	Multimedia File
            Casio PDL Pocket Streets Map
            .mpt	Bitmap graphics (Multipage TIFF)
            Template File (MS Project)
            .mpv	View file (MS Project)
            .mpw	MosASCII Project Workspace file
            .mpx	Compiled menu program (FoxPro)
            .mrb	Multiple Resolution Bitmap graphics (MS C/C++)
            .mrc	MIRC Script file
            Bibliographic Data Format
            .mrk	Informative Graphics markup file
            .mrs	Macro Resource file (WordPerfect for Win)
            .msc	MS C makefile
            .msd	MS Diagnostic Utility Report
            .msf	Multiple Sequence file
            .msg	Message
            .msi	Windows Installer file
            .msm	MultiSIM Circuit Diagram
            .msn	MSN Content Plus file
            .mso	Math Script Object file
            MS FrontPage file
            MS Word OLE Web Page Storage Stream
            .msp	Bitmap graphics (Microsoft Paint)
            .mspx	XML based Web Page
            .mss	Manuscript text file (Perfect Writer – Scribble – MINCE – Jove)
            .mst	ChemFinder Chemical Structure Index
            DATAIR Pension System Master file
            Minispecification file (Prosa)
            Setup script (MS Windows SDK)
            Visual Test Source file
            .msu	Windows Update file
            .msv	Sony Memory Stick Format
            .msw	Text file (MS Word)
            .mswmm	Windows Movie Maker Project
            .msx	Compressed CP/M file archive created by MSX
            .mtd	Digital Sheet Music
            .mth	Math file (Derive)
            .mtm	Multitracker Module music
            .mts	AVCHD Video file
            Viewpoint iPix file
            .mtv	MTV Music Generator
            .mtw	Datafile (Minitab)
            .mtx	Temporary File often used by a browser or TWAIN device
            Viewpoint iPix file
            Max Magic Microtuner tuning text file
            .mu	Menu (Quattro Pro)
            .mu3	Myriad Music file (packed sounds & digital tracks)
            .muf	ProtoMuck Multi User Forth Program
            .mul	Ultima Online Game
            .mus	MusicTime Sound file
            Myriad Music file
            .mvb	Database
            MS Multimedia viewer file
            MvPCbase www.mvsoft-comp.com
            .mvc	Music Collector Collection Manager file
            .mvd	MicroDVD (DVD movie file)
            .mvf	Stop frame file (AutoCAD AutoFlix)
            .mvi	Movie command file (AutoCAD AutoFlix)
            .mvw	Log file (Saber LAN)
            .mwf	Animation (ProMotion)
            .mwp	Lotus Wordpro 97 Smartmaster file
            MegaWorks Pack file
            .mws	Maple Worksheet File
            .mwv	MovieWorks file
            .mxd	GIS Project file
            .mxe	Macro Express
            Mindex Effect Album
            .mxf	Material eXchange Format for the interchange of audio-visual
            Material with associated data and metadata.
            .mxl	Moxcel Spreadsheet File
            .mxm	MS Project/Outlook Team Assign Task
            .mxp	Macromedia Extension Manager
            ArcReader Published Map
            .mxt	Data (MS C)
            .myp	Presentation (MM Make Your Point)
            .myr	Myriad Music file
            .mys	Myst Saved Game
            .myt	Myriad Tutorial file
            .mzp	Maxscript Compressed File
            .na2	Netscape Mail file
            .nam	MS Office Name file
            .nap	Naplps file (VideoShow) (EnerGraphics)
            .nav	MSN Application Extension
            .nb	Text file (Nota Bene)
            .nbf	Backup Now Backup file
            .nbu	Nokia PC Suite Backup file
            .nc	Graphics (netcdf)
            Instructions for NC (Numerical Control) machine (CAMS)
            .ncb	MS Developer Studio file
            .ncc	Cnc (Computer Numeric Control) control file (CamView 3D)
            .ncd	Nero CoverDesigner Document file
            Norton Change Directory support file (Norton Commander)
            NTI CD-Maker file
            .ncf	Lotus Notes Internal Clipboard
            Steam Configuration file
            Netware Command file
            .nch	Outlook Express folder file
            On Hold message/music file
            .nd5	NDS Renamed file
            .ndb	Network database (Intellicom – Compex)
            .nde	Video format – various manufactures of surveillance camera systems
            .ndf	NeoPlanet Browser File
            .ndk	Lotus Notes(containing the files related to workspace)
            .ndx	Index file (dBASE II – III – IV – dBFast)
            .neb	Nortec H.E.L.P.
            .ned	MSN Application Extension
            .nef	Nikon’s RAW format for digital cameras (Nikon Electronic Format)
            .neo	Raster graphics (Atari Neochrome)
            .nes	Nintendo Entertainment System ROM Image
            .net	Network configuration/info file
            .new	New info
            .nfo	Info file
            .ng	Online documentation database (Norton Guide)
            .ngf	Enterasys Networks NetSight generated format file
            .ngg	Nokia Group Graphics
            .nh	NetHack file
            .nib	Adobe AIR file
            .nif	NetImmerse File Format
            .njb	Photo Index file
            .nlm	Netware Loadable Module
            .nls	Code Page National Language Support
            .nlx	Form (FormWorx 3.0)
            .nmd	SwordSearcher file
            .nmi	SwordSearcher file
            .nmo	Virtools Behavioral Objects
            .nms	Numega Softice’s Loader file
            Virtools Graphical Scripts
            .nnb	newnovelist Story Outline
            .nob	VersaPro Word Exchange file
            .nol	Nokia Operator Logo
            .not	Acrobat Spelling file
            ActiveNote Post-It-Notes
            .now	Text file
            .np	Project schedule (Nokia Planner) (Visual Planner 3.x)
            .npa	ReliaSoft Weibull++ 6
            .npf	Backup Now Image file
            .npi	Source for DGEN.EXE intepreter (dBASE Application Generator)
            .nra	Nero Audio-CD Compilation
            .nrb	Nero CD-ROM Boot Compilation
            .nrg	Norton Registration Entries
            Nero CD-Image
            IsoBuster file
            NRG File Format
            .nri	Nero ISO CD-ROM compilation
            .nrl	iManage file
            .nrw	Nero WMA Compilation file
            Nikon RAW file
            .nsc	Noder file (Polish)
            Windows Media Station file
            .nsf	Lotus Notes / Domino database
            .nsi	Nullsoft Install System Script
            .nst	Music (NoiseTracker)
            .nt	Startup files (Windows NT)
            .ntf	Lotus Notes / Domino template file
            .nth	Nokia Theme file
            .ntp	Neato CD Labels
            .ntr	Executable ASCII text file (strip header and rename) (netrun31.zip)
            .nts	Tutorial (Norton)
            Executable ASCII text file (strip header and rename) (netsend1.zip)
            .ntx	Index (Clipper 5)
            .ntz	InVircible Directory Integrity Information
            .nu4	Norton Utilities Root File (DLL) Symantec Corporation
            .nuf	Message for new users on their 1st call (Procomm Plus)
            .numbers	iWork Numbers Spreadsheet file
            .nup	Program Component Update files
            .nvc	Nero Vision Project file
            .nvm	AOLpress Help file
            .nwc	Noteworthy Composer song file
            .nws	Info text file (latest news) (ASCII)
            .nwr	New World Report Aegis/MSP Law Enforcement Records (New World Systems)
            .nwt	New World Text Aegis/MSP Law Enforcement Records (New World Systems)
            .nxt	Sound (NeXT format)
            .nzb	NewsBin Index file
            .o	Object file (unix – Atari – GCC)
            .o$$	Outfile (Sprint)
            .oaz	Fax (NetFax Manager)
            .ob	Object cut/paste file (IBM LinkWay)
            .obd	MS Office Binder
            .obj	Object code (Intel Recolatable Object Module)
            .obr	Object browser data file (Borland C++)
            .obs	Script (ObjectScript)
            .obv	Visual interface (ObjectScript)
            .oca	Control Typelib Cache
            .ocf	Object Craft File (Object Craft)
            .ocm	AOL Advertising Control files
            Internet Odyssey 2 Update
            .ocp	Advanced Art Studio
            Offline Commander Project file
            .ocr	Incoming fax transcribed to text (FAXGrapper)
            .oct	Radiance Octree Format
            .ocx	OLE ActiveX custom control
            .odf	Open Document Interchange
            BattleZone Cartographers Guild file
            Star Trek Armada Ship/Structure Infomation
            .odg	OpenDocument Graphic file
            .odl	Type library source (Visual C++)
            .odp	OpenOffice Presentation file
            .ods	OpenOffice Spreadsheet file
            .odt	OpenOffice OpenDocument text document
            .oeb	Outlook Express Backup Wizard
            .oem	TextSetup OEM file
            .ofc	Open Financial Connectivity file
            .ofd	Form definition (ObjectView)
            .off	Object File Format vector graphics
            .ofm	Adobe font
            .oft	MS Outlook Item Template
            .ofx	Olicom Fax
            Open Financial Exchange file
            .ogg	Ogg Vorbis Codec Compressed WAV file
            .ogm	Ogg Vorbis Compressed Video file
            .ogv	Video Container file
            .okt	Music (Oktalizer)
            .olb	Object library (VAX)
            .old	Backup file
            .ole	Object Linking and Embedding Object
            .oli	Text file (Olivetti)
            .oma	OpenMG Music file
            .omf	Open Media file
            .omg	OpenMG Jukebox
            .oms	Briggs Softworks Order Maven
            Macintosh MP3 Music Format
            Omega Downloader Configuration file
            .ond	Lotus Notes-related file
            .one	OneNote Document File
            .ont	Bible file
            .oom	Swap file (Shroom)
            .opd	Omnipage file
            .opf	Flip Album file
            Open Packaging Format file
            .opl	Psion Organiser Programming Language Source file
            .opn	Active options (Exact)
            .ops	Microsoft Office profile settings file
            .opt	Optimize support file (QEMM)
            .opw	Organization chart (Org Plus for Windows)
            .opx	Inactive options (Exact)
            .or2	Lotus Organizer 2 file
            .or3	Lotus Organizer 97 file
            .or4	Lotus Organizer file
            .or5	Lotus Organizer file
            .ora	Parameter file (Oracle)
            .org	Calendar file (Lotus Organizer)
            .osd	Open Software Description file
            .oss	MS Office Saved Search
            .ost	Microsoft Outlook Offline file
            .otf	Open Type Format
            .otl	Outline font description (Z-Soft Type Foundry)
            .otx	Text file (Olivetti Olitext Plus)
            .out	Output file
            .ov1	Overlay file (part of program to be loaded when needed)
            .ov2	Overlay file (part of program to be loaded when needed)
            .ovd	Datafile (ObjectVision)
            .ovl	Overlay file (part of program to be loaded when needed)
            .ovr	Overlay file (part of program to be loaded when needed)
            .ovw	Cool Edit Pro Overviewfile
            Cubase .WAV File Image
            DIANA Overview file
            .ows	Web Studio 2 Project file
            .oxt	Open Office Extension file
            .p	Pascal source code file
            Rea-C-Time application parameter file (ReaGeniX code generator)
            Picture file (APPLAUSE)
            .p16	Music (16 channels) (ProTracker Studio 16)
            .p22	Patch file (Patch22)
            .p65	Adobe Pagemaker v6.5
            .p7m	PKCS #7 MIME Message
            .pa	Print Artist
            .pa1	Worktable (PageAhead)
            .pab	Microsoft Outlook personal address book
            .pac	Stad Image (graphics ?)
            Package (SBStudio II)
            .pack	Pack 2000 Compressed file
            .pad	Keypad definition (Telemate)
            .paf	PARIS audio format
            Personal Ancestral file
            .pages	Pages document
            .pak	Compressed file archive created by PAK (pak251.exe)
            .pal	Adobe Pagemaker Library Palette
            Color Palette
            Compressed File
            Tree Professional Palm Creator file
            .pan	Printer-specific file (copy to coreldrw.ink) (CorelDRAW)
            .par	Parts application (Digitalk PARTS)
            Parameter file (Fractint)
            Permanent output file (Windows 3.x)
            .pas	Pascal source code file
            .pat	Hatch patterns (AutoCAD – Photostyler)
            Vector fill files (CorelDRAW)
            .pax	Pax Archive file
            .pb	Fax (FAXability Plus)
            Phonebook (WinFax Pro)
            Setup file (PixBase)
            .pb1	Document (First Publisher for Windows)
            .pba	Powerbasic BASIC source code (Genus)
            .pbd	Phone book (FaxNOW! – Faxit)
            .pbf	Turtle Beach Pinnacle Bank file
            Grand Prix Legends BMAP file
            PBook E-book Format (renamed ZIP file)
            Portable Bitmap Format file
            .pbi	Powerbasic include file (Genus)
            Profiler Binary Input (MS Source Profiler)
            .pbk	Microsoft XP Remote Access Phonebook file
            .pbl	Powerbasic library (Genus)
            .pbm	Pbm Portable Bit Map graphics
            Planar bitmap graphics (XLib)
            .pbo	Profiler Binary Output (MS Source Profiler)
            .pbr	Microsoft Publisher backup file
            .pbt	Profiler Binary Table (MS Source Profiler)
            .pc	Text file containing IBM PC specific info
            .pc3	Custom palette (Harvard Graphics 3.0)
            .pc8	Ascii text IBM8 character set (NewWave Write)
            .pca	Cash Register Express program
            .pcb	Broderbund Print Shop Business Card
            Ivex Winboard Design file
            MS PowerPoint Application Data file
            Protel Technology Advanced PCB Design
            .pcc	Cutout picture vector graphics (PC Paintbrush)
            .pcd	Graphics (Kodak PhotoCD)
            Microsoft Visual Test compiled script
            .pcf	Profile Configuration file
            Profiler Command File (MS Source Profiler)
            .pch	Patch file
            Precompiled header (MS C/C++)
            .pcj	Multimedia authoring tool graphics (IBM’s Linkaway-Live)
            .pck	Received Package file
            Pickfile (Turbo Pascal)
            .pcl	HP-PCL graphics data (HP Printer Control Language)
            .pcm	Plasmacam CAD/CAM system file
            .pcs	PICS Animation
            .pct	Bitmap Graphic
            Honeywell GUS Display Builder
            Macintosh Quickdraw/PICT Drawing
            NIST IHDR
            .pcw	Text file (PC Write)
            .pcx	Bitmap graphics (PC Paintbrush)
            .pd	SynerGEE Stoner software files (compressible pipe flow program)
            .pda	Bitmap graphics
            .pdb	Data (TACT)
            .pdc	Personal Database Creator file
            .pdd	Adobe PhotoDeluxe Image
            .pde	Principalm Data Extract files
            Processing Environment text files
            .pdf	Adobe Portable Document Format
            Package Definition File
            Graphics file (ED-SCAN 24bit format)
            .pdg	Printshop Deluxe files
            .pdl	Project Description Language file (Borland C++ 4.5)
            .pdr	Port or printer driver
            .pds	Incredimail
            Source Code File
            Telsis HiCall Program File
            Pds graphics
            Planetary Data System
            Pldasm source code file (hardware assembly)
            Print Shop Graphic
            .pdt	ProCite Primary Database
            VersaPro Compiled Block
            .pdv	Printer driver (Paintbrush)
            .pdw	Document (Professional Draw)
            .pdx	Adobe Acrobat Index file
            .pe4	Photo Explorer Thumbnail
            .pea	PeaZip Compressed FileArchived files
            .peb	Program Editor bottom overflow file (WordPerfect Library)
            .ped	Program Editor delete save (WordPerfect Library)
            .pem	Program Editor macro (WordPerfect Library)
            Privacy Enhanced Mail Certificate file
            .peq	Program Editor print queue file (WordPerfect Library)
            .per	Program Editor resident area (WordPerfect Library) (vakioalue)
            .pes	Program Editor work space file (WordPerfect Library)
            .pet	Program Editor top overflow file (WordPerfect Library)
            .pf	Windows Prefetch file
            Monitor/printer profile file
            .pfa	Type 3 font file (unhinted PostScript font)
            .pfb	Type 1 PostScript font file
            .pfc	Text file (First Choice)
            .pfg	jEEPers file
            .pfk	Programmable function keys (XTreePro)
            .pfl	Family Lawyer Data file
            .pfm	Windows Type 1 font metric file
            .pfs	Database (PFS:FILE) – text file (PFS:Write)
            .pft	Printer font (ChiWriter)
            .pg	Pagefox File
            Page cut/paste file (IBM LinkWay)
            .pgi	Printer Graphics File device driver (PGRAPH library)
            .pgm	Portable Grayscale bitMap graphics
            Program (Signature)
            .pgp	Support file (Pretty Good Privacy RSA System)
            .pgs	Manual page (man4dos)
            .ph	Optimized .goh file (Geoworks)
            Perl header file
            Phrase-table (MS C/C++)
            .phb	NewLeaf PhraseBook
            ClustaW Tree file
            TreeView file
            PhoneB Phonebook file
            .phn	Phone list (UltraFax – QmodemPro)
            .php	PHP Script
            MS Picture It! Publishing Project File
            PhotoParade
            .pho	Phone database (Metz Phone for Windows)
            .phr	Phrases (LocoScript)
            .phtml	PHP Script
            .pic	Pixar picture file (SDSC Image Tool)
            Bitmap graphics (Macintosh b&w PICT1 – color PICT2)
            Bitmap graphics (many eg. Lotus 1-2-3 – PC Paint)
            .pif	Program Information File (Windows 3.x)
            Vector graphics GDF format (IBM mainframe computers)
            Shortcut to MS-DOS program
            .pim	PIM Archive file
            .pip	Personalized menu and toolbar (MS Office)
            .pit	Compressed Mac file archive created by PACKIT (unpackit.zoo)
            .pix	Alias image file (SDSC Image Tool)
            .pj64	Project 64 game files.mswmm Windows Movie Maker Project file
            .pj	Project (CA-SuperProject)
            .pjt	Project memo (FoxPro)
            .pjx	Project (FoxPro)
            .pk	Packed bitmap font bitmap file (TeX DVI drivers)
            .pk3	American McGee Alice Archive
            Return to Castle Wolfenstein file
            Heavy Metal: F.A.K.K.2 Archive
            Quake 3 Arena Archive (renamed zip file)
            .pka	Compressed file archive created by PKARC
            .pkd	Top Secret Crypto Gold file
            .pkg	Installer script (Next)
            .pkk	Private Key file
            .pkt	Packet Tracer Network Simulation file
            .pl	Perl source code file
            Prolog source code file
            Property List font metric file (TeX)
            Palette (Harvard Graphics)
            .pl1	Room plan (3D Home Architect)
            .pl3	Chart palette (Harvard Graphics 3.0)
            .plb	Library (FoxPro)
            .plc	Add-in file (functions – macros – applications) (Lotus 1-2-3)
            .pll	Pre-linked library (Clipper 5)
            .pln	Spreadsheet (WordPerfect for Win)
            .plr	Descent Pilot file
            Player file
            .pls	DisorderTracker2 Sample
            WinAmp MPEG PlayList file
            Shoutcast file
            MYOB Data file
            .plt	AutoCAD HPGL Vector Graphic Plotter file
            Bentley’s CAD MicroStation Driver Configuration for Plotting
            Clipper 5 Pre-linked Transfer file
            Gerber Sign-making Software file
            HP Graphics Language
            .pmv	Pegasus Mail Filter Rule file
            .pmx	Pegasus Mail file
            .pn3	Printer device driver (Harvard Graphics 3.0)
            .pnf	Precompiled Setup Information (Temporary file seen during installs)
            .png	Bitmap graphics (Portable Network Graphics)
            .pnm	Pbm Portable aNy Map (PNM) graphics
            .pnt	Macintosh painting
            Qwk reader pointer file (MarkMail 2.x)
            .pod	OPENPROJ Project file
            .poh	Optimized .goh file (Geoworks)
            .poi	Point of interest file
            .pop	Messages index (PopMail)
            Pop-up menu object (dBASE Application Generator)
            .pos	ProCite Output Styles
            QuickPOS IIF file
            .pot	PowerPoint template
            .potx	PowerPoint Open XML Template file
            .pov	Raytraced scene description file (Persistence Of Vision)
            .pow	Chord chart (PowerChords)
            .pp	Free Pascal Source Code file
            Compressed Amiga file archive created by POWERPACKER
            .ppa	PowerPoint Add-in
            .ppb	Button bar for Print Preview (WordPerfect for Win)
            .ppd	PostScript Printer Description (Acrobat)
            .ppf	Turtle Beach Pinnacle Program file
            Jasc Paint Shop Pro 7 Preset file
            Micrografx Picture Publisher file
            PlayStation Patch file
            .ppg	MS PowerPoint Ppresentation
            Professor Franklin’s Photo Print Gold
            .ppl	Polaroidpaletteplus ColorKey device driver (Harvard Graphics 3.0)
            .ppm	Portable Pixel Map graphics
            .ppo	Pre-processor output (Clipper 5)
            .ppp	Publication (PagePlus)
            Image files used in PagePlus SE
            .pps	PowerPoint Slideshow
            Storyboard (Personal Producer)
            .ppsx	MS Office PowerPoint Slide Show file
            .ppt	General file extension (PowerPoint)
            .ppz	PowerPoint Packaged Presentation
            .pqa	Palm Query Application File (database for wireless access)
            .pqi	Power Quest Drive imaging
            .pr2	Presentation (Aldus Persuasion 2.x)
            .pr2	Printer driver (dBASE IV)
            .pr3	Postscript printer driver (dBASE IV)
            Presentation (Aldus Persuasion 3.x)
            .prc	Corel Presentation file
            Palmpilot resource file
            Picture Gear Pocket
            .prd	Printer driver (many)
            .pre	Presentation (Freelance Graphics)
            Settings (Programmer’s WorkBench – MS C/C++)
            .prf	Pixel Run Format graphics (Improces – Fastgraph)
            Printer driver (dBASE IV)
            Profiler output
            .prg	Program (Atari)
            Program source (dBASE IV – FoxPro – Clipper 5 – dBFast)
            .pri	Printer definitions (LocoScript)
            .prj	Project
            .prm	Parameters
            MYOB Premier file extension
            .prn	DataCAD Windows Printer file
            HP Printer Control Language
            PostScript file
            Printer Text file
            XYWrite Printer Driver
            .pro	Prolog source code file
            Graphics profile file (DOS)
            .prs	Printer Resource eg. fonts (WordPerfect for Win)
            Presentation (Harvard Graphics Win)
            Procedure (dBASE IV)
            .prt	CADKEY Part file
            Printer Configuration
            Printer driver (Dr.Halo)
            Printer-formatted file
            Pro/ENGINEER Model file
            Process Revolution Template file
            SCEdit Part file
            Unigraphics Part file
            .prx	Windows Media Settings file
            Compiled program (FoxPro)
            .prz	Freelance Graphics 97 file
            .ps	PostScript file (text/graphics) (ASCII)
            .ps2	PostScript Level 2 file
            .psb	Pinnacle Sound Bank
            Project Scheduler Configuration file
            .psd	Adobe Photoshop file
            Design II for Windows
            .pse	Bitmap graphics (IBM printer Page SEgment)
            .psf	Photoshop Proof Settings file
            Outline PostScript printer font (ChiWriter)
            PrintShop Mail Favorites
            .psi	PSION A-law Audio
            File extenstion for Pierresoft Adesign Image
            .psm	Music (MASI – ProTracker)
            PrintShop Mail
            Symbol table of IDE (Turbo Pascal)
            .psmdoc	PrintShop Mail
            .psp	PaintShop Pro Image
            Procedure (Prodea Synergy)
            Project Scheduler Planning file
            .psr	Project Scheduler Resource file
            .pst	MS Outlook personal folder
            .psw	WinXP Backup Password File
            .pt3	Device driver (Harvard Graphics 3.0)
            Template (PageMaker 3)
            .pt4	Template (PageMaker 4)
            .ptb	Script (PubTech BatchWorks)
            .ptm	Macro (PubTech BatchWorks)
            An extension used in PUNCH! home design software
            Polynomial Texture Map
            .ptn	PaperPort Thumbnail Images
            .ptp	Act! Modem Sync file
            .ptr	Qwk reader pointer file (QMail)
            .pts	Infinity Engine Game Tileset
            Halflife Map Creation Debug file
            .ptx	Real Legal E-Transcript
            .pub	Page template (MS Publisher)
            Public key ring file (Pretty Good Privacy RSA System)
            Publication (Ventura Publisher – 1st Publisher)
            .put	Compressed file archive created by PUT (put334.zip)
            .puz	Across Lite Crossword Puzzle
            Packed MS Publisher file
            .pva	Hauppauge DVB-Software
            .pvd	Script (Instalit)
            .pvm	Parallel Virtual Machine software library
            .pvl	Library (Instalit)
            .pvt	Local Fidonet pointlist
            .pw	Text file (Professional Write)
            .pwd	Pocket Word document
            AutoCAD Password file
            .pwf	ProCite Workforms
            .pwi	Pocket Word document
            .pwl	Password List
            .pwm	WebMoney Purse file
            .pwp	Text document (Professional WritePlus)
            .pwz	MS Powerpoint Wizard
            .px	Primary database index (Paradox)
            .pxl	Pocket Excel Spreadsheet
            .pxv	Modelworks Project File used in JPad Pro and SitePad Pro
            .py	Python script file
            .pyc	Compiled PYTHON script file
            .pyd	Binary Python Extension on Windows
            .pyw	Python GUI Script on Windows
            .pz2	Curious Labs Poser Pose file
            .pz3	Curious Labs Poser Document
            .pza	MGI PhotoSuite II/III/4 Album file
            .pzd	Default settings (Pizazz Plus)
            .pzl	Jigs@w Puzzle
            Lode Runner Game Puzzle
            Puzzle
            .pzo	Overlay file (Pizazz Plus)
            .pzp	MGI PhotoSuite II/III/4 Project file
            Palette (Pizazz Plus)
            .pzs	Settings (Pizazz Plus)
            .pzt	Transfer file (Pizazz Plus)
            .pzx	Swap file (Pizazz Plus)
            .q05	Intuit Canada Quick tax file, tax return file
            .q9q	BladePro Graphic Plugin file
            .qad	QuickArt database
            .qag	Quick Access Group (Norton Desktop)
            .qap	Application (Omnis Quartz)
            .qbb	QuickBooks for Windows Backup file
            .qbe	Saved query (Query By Example) (dBASE IV – Quattro Pro)
            .qbk	Intuit Canada Quick tax file, backup copy of tax return file
            .qbl	Business Lawyer Document
            .qbo	Compiled query (dBASE IV)
            .qbr	QuickBooks Report
            .qbw	Spreadsheet (QuickBooks for Windows)
            .qcn	Qualcomm Phonebook file
            .qcp	Qualcomm PureVoice File
            Contains data frames generated by QCELP 13K vocoder
            .qd0	Data file – segment 10 (Omnis Quartz)
            .qd1	Data file – segment 1 (Omnis Quartz)
            .qd2	Data file – segment 2 (Omnis Quartz)
            .qd3	Data file – segment 3 (Omnis Quartz)
            .qd4	Data file – segment 4 (Omnis Quartz)
            .qd5	Data file – segment 5 (Omnis Quartz)
            .qd6	Data file – segment 6 (Omnis Quartz)
            .qd7	Data file – segment 7 (Omnis Quartz)
            .qd8	Data file – segment 8 (Omnis Quartz)
            .qd9	Data file – segment 9 (Omnis Quartz)
            .qdat	Quicktime Installer Cache
            .qdb	Quicken data file
            .qdf	Quicken for Windows data file
            .qdt	Quark Xpress Dictionary file
            Question Mark Designer Test file
            QuickBooks UK Accountancy Data file
            Quicken Data file
            .qdv	Graphics (Steve Blackstock Giffer)
            .qe4	Kingpin Project file
            .qef	Query file (Q+E for MS Excel)
            .qel	Quicken Electronic Library file
            .qfl	Quicken Family Lawyer file
            .qfx	Quicken Financial Exchange file
            Fax (QuickLink)
            .qhf	QIP PDA History file
            .qic	Backup set for Microsoft Backup
            .qif	Quicken Interchange Format
            Quicktime Image
            .qix	NovaStar Backup file
            Quicken for DOS v.2 data file
            .qlb	Quick library (MS C/C++)
            .qlc	Data (PostScript help file) atmfonts.qlc
            .qlf	Family Tree Maker Genealogy file
            .qlp	Printer driver (QuickLink)
            .qm4	Options or services file (QMail 4.x Mail Door)
            .qm	Virtual Box Language file
            .qml	Quick Markup Language file
            .qph	Intuit Quicken Price History file
            .qpr	Generated query program (FoxPro)
            Print queue device driver (OS/2)
            .qpw	Quattro Pro Project file
            .qpx	Compiled query program (FoxPro)
            .qrp	QuickReport Report files
            Centura Report Builder file
            Liberty for Windows report file
            .qrs	Equation Editor support file (WordPerfect for Win)
            .qrt	Qrt ray tracing graphics
            .qru	SQL Query file
            .qry	Query (dBASE IV)
            .qsd	Quicken for Windows data file
            .qsi	Quintessential Stereotaxic Injector Commander log files
            .qst	Quake Spy Tab file
            .qt	Quicktime movie (animation)
            .qtc	Incite Media Assistant file
            .qtk	Apple QuickTake file format for Windows
            .qtl	Quick Time Media Link file
            .qtp	QuickTime Preferences
            Astra Quicktest Report
            .qts	Macintosh PICT image
            QuickTime image
            .qtx	QuickTime image
            .que	CuteFTP Queue file
            Task Scheduler Queue Object
            .qvm	Quake file
            .qvs	Casio Digital Camera file
            .qw	Symantec Q&A Write file
            .qwk	QWK reader message file
            .qxd	QuarkXPress document file format
            .qxl	Element library (QuarkXPress)
            .qxp	QuarkXPress project file
            .qxt	Template file (QuarkXpress)
            .r	Ratfor (FORTRAN preprosessor) file
            .r33	Train Simulator Game file
            .r8	Raw graphics (one byte per pixel) plane one (PicLab)
            .r8p	Pcl 4 bitmap font file (Intellifont)
            .ra	Music (RealAudio)
            .ram	Ramfile (RealAudio)
            .rar	Compressed file archive created by RAR (rar1_402.exe)
            .ras	Sun Rasterfile graphics
            .rat	Datafile (RATS)
            .raw	Raw RGB 24-bit graphics
            .rb	Ruby on Rails class file
            .rbf	Windows Installer Rollback file
            Datafile (Rbase)
            .rbn	Richard’s Bridge Notation
            Real Sound file
            .rbs	Windows Installer Rollback Script file
            .rbx	Format for playing RapidPlayer v3.0 ActiveX Control in Explorer
            .rc	Resource script (Visual C/C++ – Borland C++)
            Configuration (emacs)
            .rcf	Rhapsody Storage file
            .rcg	Netscape newsgroup file (netsc.rcg)
            .rcp	Recomposer’s MIDI Sequencer Music file
            .rcx	Lego Mindstorms Robotics Invention System
            .rdb	TrueVector Rules database
            ZoneAlarm Rules database
            .rdf	Compiled UIC source code (Geoworks UI Compiler)
            .rdi	Device-independent bitmap file (RIFF RDIB format)
            .rds	Ray Dream Studio file
            .rdx	Datafile (Reflex)
            .rec	Datafile (EpiInfo)
            Record file (Sprint)
            Recorded macro file (Windows 3.x)
            .red	Path info (Clarion Modula-2)
            .ref	Cross-reference
            .reg	OLE Registration (Windows 3.x)
            Registration (Corel programs)
            .rels	Microsoft Office 2007 Relationships
            .rem	Encrypted Data file
            Remarks
            .rep	QWK reader reply file
            Report (Report Designer – CodeReporter – DataBoss)
            .req	Request
            .res	Compiled resource (MS C/C++ – Borland C++)
            Dbase resources (dBASE IV)
            .rev	Revision file (Geoworks)
            .rex	Rexx source code file
            .rex	Report definition (Oracle)
            .rez	Resource file
            .rf	Sun raster graphics
            .rfl	Roll Forward Log file
            .rft	Dca/RFT Revisable Format Text file (IBM DisplayWrite 4.0-5.1)
            .rgb	Sgi RGB image file (SDSC Image Tool)
            .rgi	RealArcade Game Installer
            .rgp	RealArcade Game Package
            .rgs	RealArcade Game Installer
            .rgx	Symbol tables etc. info (ReaGeniX code generator)
            .rh	Resource header file (Borland C++ 4.5)
            .rhp	Rhapsody Notation Program File Format
            .ri	Data (Lotus 1-2-3)
            .rib	Graphics in Renderman format (3DReality)
            .ric	Fax (Ricoh)
            .rif	Riff bitmap graphics (Fractal Design Painter)
            .rip	Graphics (Remote Access)
            .rix	Bitmap graphics (ColorRIX VGA Paint)
            .rl4	Bitmap graphics
            .rl8	Bitmap graphics
            .rla	Wavefront raster image file (SDSC Image Tool)
            .rlb	Data (Harvard Graphics Win) hgw.rlb
            .rlc	Graphics 1bit/pixel scanner output
            .rle	Utah Run Length Encoded raster graphic (SDSC Image Tool)
            .rlz	Realizer source code file (CA-Realizer)
            .rm	RealMedia file
            .rmf	Rich Map Format
            Rich Music format
            .rmi	Midi file (RIFF RMID format)
            .rmj	Real Jukebox file
            .rmk	Makefile (Clipper RMake)
            .rmm	RealPlayer file
            .rmr	Resume Maker file
            .rms	Secure Real Media file
            .rmvb	Video file for Realplayer
            .rm	RealMedia
            .rmvb	Real Media video file
            .rmx	RealJukeBox MP3 file
            .rn	Xpl program for Nota Bene users
            .rnd	Rendering Slide (AutoCAD AutoShade)
            .roi	Actuate ReportBlast file
            .rno	Runoff file (VAX)
            .rol	Fm music Adlib Music File (Roland)
            .rpd	Database (RapidFile)
            RosaPro file
            RPV Printing System file
            .rpl	Text document (Replica)
            .rpm	RedHat Package Manager
            RealMedia Player file
            RunPaint Multicolor Graphic
            .rps	Propellerhead Software Reason Song
            .rpt	Report
            .rrd	ERDAS Imagine file
            .rs	Data file (Amiga Resource – Reassembler)
            .rs_	Resource fork of a Macintosh file (Mac-ette)
            .rsb	Red Storm Image Format
            .rsc	Resource file
            .rsm	ReliaSoft MPC 3
            RuneSword II Game
            WinWay Deluxe Resume file
            .rsp	Response file
            .rss	Rockwell Logix PLC file
            .rst	ANSYS Results
            ReliaSoft BlockSim
            .rsw	ReliaSoft BlockSim
            .rtc	Live Meeting Connection file
            .rtf	Rich Text Format text file (many – Windows Word)
            Windows Help file script
            .rtl	Run Time Library (NU 7.0)
            Text file
            .rtp	Turbo Tax Update file
            RTPatch software update package data file
            .rts	Runtime library file (CA-Realizer)
            .rtx	Reliacast Audience Manager Turnstile
            Mobile Phone Ringtone
            .ru	JavaSoft Library file
            .rul	InstallShield
            .run	RunScanner Saved file
            .rv	RealVideo Video file
            .rvb	Rhinoscript file
            .rvp	MS Scan Configuration file
            .rvw	Review
            .rwg	Random Word Generator List file
            .rws	Resource Workshop data file (Borland C++)
            .rwx	Script (RenderWare)
            .rwz	MS Outlook Rules Wizard file
            .rzk	Red Zion File Crypt (password file)
            .rzr	in-sync Speed Razor Project file
            .rzx	in-sync Speed Razor Project file
            Red Zion File Crypt (encrypted file)
            .s	Assembly source code file (Unix)
            Scheme source code file
            .s$$	Temporary sort file (Sprint)
            .s3m	Music (16 channels) (Scream Tracker 3.0)
            .sac	Shared Asset Catalog (Adobe)
            .saf	MusicMatch Jukebox Secure Audio file
            Safe File Encryption (Helix Software)
            Twelve Ghosts file
            .sah	SETI@Home data file
            .sal	Datafile (SORITEC)
            .sam	Text file (Samna – Lotus Ami/Ami Pro)
            .sar	Compressed file archive created by SAR (sar1.zip)
            .sas	SAS System program
            .sas7bcat	SAS System file catalog
            .sas7bdat	SAS System data set
            .sas7bndx	SAS System index
            .sas7bpgm	SAS System Stored Program
            .sas7bvew	SAS Data Set View
            .sas7mdb	SAS System multidimensional database
            .sat	Standard ACIS Text file
            .sav	Backup file (saved file)
            Configuration
            Saved game situation (eg. NetHack)
            .sb	Audio file (signed byte)
            .sbc	Sagebrush Corporation Spectrum CIRC/CAT Report
            .sbd	Storyboard (Storyboard Editor)
            .sbi	Sound Blaster Instrument file (Creative Labs)
            .sbj	Micrografx Clipart or Palette file
            .sbn	ArcView file (GIS)
            .sbp	Dml program (Superbase 4)
            .sbr	Support file (Source Browser)
            .sbs	SWAT HRU Output file
            .sbt	Notes related to record (Suberbase 4 Windows)
            .sbx	ArcView file (GIS)
            .sc	Pal script (Paradox)
            Display driver (Framework II)
            .sc3	Renamed dBASE III screen mask file (dBASE IV)
            Screen device driver (Harvard Graphics 3.0)
            .sca	Datafile (SCA)
            .scc	Text file
            .scd	Scodl Scan Conversion Object Description Language graphics
            .scf	Multimedia show (ScoreMaker)
            Spelling checker configuration (Symphony)
            Windows Explorer command file
            .sch	Project schedule (Schedule Publisher)
            Schematics file (ORCAD)
            .sci	System Configuration Information
            Fax (SciFax)
            .scm	Scheme source code file
            ScreenCam Movie file
            SchematicMaker file
            .scn	Screen file (Kermit)
            Pinnacle Studio Scene file
            .sco	High score
            .scp	Script (BITCOM)
            .scr	Debug source code file (DOS Debug)
            Screen – screen snapshot (dBASE IV – Procomm Plus)
            Screen font (LocoScript)
            Screen saver (Windows 3.x)
            Script (Kermit – 1st Reader)
            .sct	Screen memo (FoxPro)
            Windows Script Component
            .scx	Bitmap graphics (ColorRIX)
            Chart (Stanford Chart)
            Screen (FoxPro)
            .scy	Security file (ReaGeniX)
            .sda	Fidonet’s Software Distribution Network file archive description
            .sdc	StarOffice Spreadsheet
            .sdd	StarOffice Presentation
            .sdf	System Data Format file (fixed lenght ASCII text)
            .sdi	Software Distribution Network Info file
            Single Document Interface file
            .sdn	Software Distribution Network compressd file archive (pak251.exe)
            .sdr	SmartDraw file
            .sds	Chart Application Document file
            .sdt	SmartDraw Template
            Dungeon Keeper 2 Archive
            Theme Park World Archive
            .sdu	Edwards Systems Technology file
            .sdw	StarOffice Text
            Raw Signed DWord Data
            Lotus WordPro Graphic
            .sea	Self-Extracting compressed Macintosh file Archive
            .sec	CyberPaint animation file (sequence)
            Secret key ring file (Pretty Good Privacy RSA System)
            Secured animation file (Disney Animation Studio)
            .sed	Self Extraction Directive file
            .sep	Printer separator page
            .seq	Atari animation file
            Sequential Instruction File (Bubble Chamber)
            .ses	Session info (Clarion Modula-2)
            .set	Configuration (1st Reader)
            Driver sets created by Install (Symphony)
            Setup options file
            .sf	Ircam Sound File (CSound package – MixView sound sample editor)
            Wps attribute storage (OS/2 WorkPlace Shell) wp_root.sf
            .sf2	Creative Labs Soundfont file
            .sfb	HP Soft Font file
            .sfc	System File Checker file
            .sff	Fritz Fax-Print file
            Stage Scene file
            Structured Fax Format
            .sfi	Graphics (SIS Framegrabber)
            Printer font (HP LaserJet landscape) (Ventura Publisher)
            .sfl	Pcl 4 bitmap font (landscape) (Intellifont) (Ventura Publisher)
            .sfn	Font (SPX)
            .sfo	CuteFTP Search file
            .sfp	Pcl 4 bitmap font (portrait) (Intellifont) (Ventura Publisher)
            .sfs	Pcl 5 scalable font file (Intellifont)
            .sft	Screen font (ChiWriter)
            .sfv	QuickSFV/WinSFV Checksum file
            Simple File Verification (Easy SFV Creator)
            .sfw	Seattle Film Works file
            .sfx	Self Extracting Archive file
            .sg1	Graphics (Stanford Graphics)
            .sgf	Document with graphics (Starwriter)
            Smart Game Format
            Sonique Skin
            .sgi	Graphics (IRIS – Silicon Graphics)
            .sgm	Standard Generalized Markup Language file
            Run-Time Help Files
            SoftQuad XMetaL File
            .sgn	Sierra Print Artist Sign
            .sgp	Statistics (STATGRAPHICS Plus)
            .sgt	Save/get keyboard macro (Signature)
            .sh	Unix shell script
            Unix ASCII file archive created by SHAR (unshar.zip)
            .sh3	Presentation (Harvard Graphics 3.0)
            .sha	Shell Archive file
            .shb	Background (CorelShow)
            .shd	Microsoft Windows Shadow file
            Print Spooler Shadow file
            .shg	Segmented-graphics bitmap
            .shk	Compressed Apple II file archive created by SHRINKIT
            .shm	Shell macro (WordPerfect Library)
            .shn	Shorten audio compression file
            .shp	Shape file and source file for text fonts (AutoCAD)
            .shr	Unix ASCII file archive created by SHAR (unshar.zip)
            .shs	Microsoft Word or Excel scrap file which is created when you drag and drop selected text
            .shtml	HTML File with Server Side
            .shw	Presentation (Harvard Graphics 2.0 – CorelShow)
            Slide show (WordPerfect Presentations)
            .shx	Shape entities (AutoCAD)
            .sid	Commodore64 Music file
            LizardTech MrSID Photo
            .sif	Setup Installation Files info (Windows NT Setup)
            .sig	Current program settings (Signature)
            PrintShop Sign file
            Signature file (PopMail)
            .sik	Backup file (Sicherungskopie) (MS Word)
            .sim	Aurora
            PC Finder 2002C
            PowerDVD file
            Simulation (various)
            .sis	SymbianOS Installer file
            .sit	Compressed Macintosh archive created by STUFFIT (unsit30.zip)
            .sitx	Stuffit SITX Compressed File
            .skb	SketchUp software file (3D Design Tool)
            .skf	Autosketch file
            .skin	Skin file
            .skm	Google Sketchup Texture file
            .skn	Interface skins images (FileWrangler, SecurDesk!, SecurDesk! LV, ZipWrangler)
            Symbian OS Skin File
            .skp	Sketchup software component (3D Design Tool)
            .sl	S-Lang source code file
            .slb	Slide library (AutoCAD)
            .slc	Compiled SALT script (Telix)
            .sld	Slide (AutoCAD)
            .slf	BitDefender file
            Symantec Licence file
            .sli	Slide (MAGICorp Slide Service)
            .slk	Sylk Symbolic Link format data file (MultiPlan)
            .sll	Sound data file
            .sln	Microsoft Visual Studio Solution file
            .slt	Salt Script Application Language for Telix script source (Telix)
            .sm	Smalltalk source code file
            Maillist (SoftSpoken Mailer)
            Script (ScriptMaker)
            Text file (Samna Word)
            .smc	Super Nintendo Game-console ROM Image
            .smd	StarOffice Mail
            .smf	Fax (SMARTFAX)
            .smi	RealPlay SMIL file
            Self Mounting Image file
            .smil	Synchronized Multimedia Integration Language file
            .smk	Compressed File (Smacker)
            .smm	Macro (Ami Pro)
            .smp	Sample (sound file)
            .sms	Microsoft Package Definition file
            Sega Master System Emulator
            .smt	Text file (Smart Ware II)
            .smtmp	SMTMP Virus
            .snd	Digitized sound file (Macintosh/ATARI/PC)
            .sng	Song (midi sound) (Midisoft Studio – Prism)
            .snm	Netscape mail
            .sno	Snobol4 source code file
            .snp	CoffeeCup HTML Editor Snippet
            Computer Eyes Video Output
            Microsoft Access Report Snapshop file
            Snapview Shapshot
            .snx	Mirage Microdrive Snapshot Extended Version
            Second Nature Software Graphic
            StarCraft Saved file
            .so	Apache Module file
            .sol	Flash shared object file
            Solution eg. game walkthroughs
            .som	Network serial numbers (Quattro Pro)
            Sort information (Paradox)
            .son	Song (SBStudio II)
            .sou	Sound data (sound tool)
            .sp	Compressed file archive created by SPLINT (unix)
            .spa	Macromedia FutureSplash file
            Smart Protocol Analyzer Real Time Communication Data
            SmartPA Saved Capture file
            Thermo Nicolet OMNIC file
            .spc	Program (MS Multiplan)
            Temporary file (WordPerfect for Win)
            Super Nintendo SPC700 sound file
            .spd	Scalable font (Speedo) (Harvard Graphics 3.0)
            .spf	Slide presentation file (EnerGraphics)
            .spg	Glossary (Sprint)
            .spi	Graphics (Siemens and Philips scanner)
            .spi	InConSoft Ltd. Sim-Path system files
            .spl	Compressed file archive created by SPLINT (splint.arc)
            Customized printer driver (Sprint)
            Personal spell dictionary (Signature)
            Microsoft Windows Print Spool file
            Sample
            .spm	Data (WordPerfect) wp{wp}.spm
            .spo	Statistical Program (SPSS)
            .spp	Printer file (Sprint)
            .spr	Document letter (Sprint)
            Genarated screen program (FoxPro)
            Sprite
            .sps	Spssx source code file (VAX/VMS)
            Screen driver (Sprint)
            .spt	Spitbol source code file
            Support file (MITAC disk/system management utility pack)
            .spv	InConSoft Ltd Sim-Path vehicle file
            .spw	Worksheet (SigmaPlot)
            .spx	Compiled screen program (FoxPro)
            .sql	SQL report or query
            .sqlite	SQLite Database file
            .sqm	Service Quality Monitoring file
            Logfile for Windows Live Messenger
            .sqz	Compressed file archive created by SQUEEZE (sqz1083e.exe)
            .src	Source (DataFlex)
            .srf	Sun Raster File graphics
            Sony RAW Image file
            .srp	Script (QuickLink)
            .srt	BSplayer Subtitle file
            Omron CX-Supervisor
            SDR99 Speech Recognition Task Speech Recogniser Transcript
            .ss	Bitmap graphics (Splash)
            .ssa	Subtitles
            .ssb	SmartSync Pro
            .ssd	Datafile (SAS/PC)
            .ssf	Snagit file
            Enable Spreadsheet file
            .ssm	RealPlayer Standard Streaming Metafile
            .ssp	Datafile (SAS Transport)
            .st	Smalltalk source code file (Little Smalltalk)
            Instrument library (Scream Tracker)
            Stamp (NeoPaint)
            .st3	MIDI Karaoke file
            .sta	Adobe Photoshop Match Colour Image Statistics file
            Saved state (Reflection 4.0)
            Stack (Spinmaker Plus)
            .stb	Stub library (Genus GX Kernel)
            .std	State Transition Diagram graphic file (Prosa)
            Standard (something..) (LocoScript)
            .stf	Compressed file archive created by SHRINKTOFIT
            .stg	ActiveSync (Microsoft) Backup file
            Statistica Graphics File
            .stl	C++ Standard Template Library
            .stm	State Transition Diagram model file (Prosa)
            Music (Scream Tracker)
            .stn	ArcView Geocoding Standardization file
            STiNG file
            .sto	Pascal stub OBJ file (Genus GX Kernel)
            .stp	Sharepoint Web Site Template File
            PageKeeper Packed Storage file
            DART Pro 98 system settings
            AP203 Step file
            .str	Structure list object file (dBASE Application Generator)
            .sts	Project status info (MS C/C++)
            Song format (Scream Tracker)
            .stt	Automap Template
            SureThing CD Labeler Template file
            .stu	Tarantella Enterprise 3 3270 Emulator Style file
            xyALGEBRA file
            .stw	Data file (SmartTerm for Windows)
            .stx	Electronic book (SmarText)
            Tax form (CA-Simply Tax)
            .sty	Style library or sheet (many text and graphics programs)
            .sub	CloneCd related file
            .sui	Suit library (Simple User Interface Toolkit)
            .sum	Summary
            .sun	Sun rasterfile graphics
            .sup	Supplementary dictionary (WordPerfect for Win)
            .sv4	RollerCoaster Tycoon Saved Game
            .svd	Autosave file for document (MS Word)
            .svg	Autosave file for glossary (MS Word)
            Scalable Vector Graphics File format
            .svgz	Compressed Scaleable Graphic file
            .svp	WISCO Survey Power
            Sonique Visual Plugin file
            SwiftView Command file
            .svs	Autosave file for style sheet (MS Word)
            .sw	Audio file (signed word)
            .swd	Storybook file
            Sabiston Textbook
            .swf	ShockWave Flash object
            .swg	Swag packet (SWAG Reader)
            .swi	Swish Data file
            .swk	Swapkeys Keyboard File
            .swp	Document backup (Sprint)
            Swap file (DOS)
            .sxc	StarOffice / OpenOffice Spreadsheet file
            .sxw	OpenOffice.org Writer 6.0 text file
            StarOffice Word Document file
            .sy1	Smartpix symbol library (Ami Pro)
            .sy3	Symbol file (Harvard Graphics 3.0)
            .syd	Backup of startup files created by QEMM (?) autoexec.syd
            .sym	Precompiled headers (Borland C++)
            Program symbol table (many compilers and linkers)
            Symbol file (Harvard Graphics 2.0)
            .syn	Sdsc Synu image file (SDSC Image Tool)
            Synonym file (MS Word 5)
            .sys	Datafile (SYGRAPH – SYSTAT – SPSS/PC)
            System file – device driver or hardware configuration info (DOS)
            .syw	Graphics symbols (Harvard Graphics Win)
            .szc	Windows Mobile 5 (Pocket PC)
            .t	Tads source
            Tape Archive (tar) without compression
            Tester symbol table (ReaGeniX code generator)
            File extension for a Turing open source file
            .t$m	AVG Internet Security Temporary file
            .t04	TaxCut 2004 file
            .t05	TaxCut 2005 Tax Return
            .t06	TaxCut 2006 Tax Return
            .t07	TaxCut 2007 Tax Return
            .t08	TaxCut 2008 Tax Return
            .t09	H&R Block At Home 2009 Tax Return
            .t10	H&R Block At Home 2010 Tax Return
            .t11	H&R Block At Home 2011 Tax Return
            .t12	H&R Block At Home 2012 Tax Return
            .t2	Textease 2000 file
            .t44	Temporary file for Sort or Index (dBASE IV)
            .t64	Program (C64S emulator)
            .ta0	TaxAct file
            .tab	Guitar Tablature file
            MapInfo Table
            Diabetes Mentor file
            .tag	Query tag name (DataFlex)
            .tah	Turbo Assembler Help file (Borland C++)
            .tal	Text illustration (TypeAlign)
            .tao	IsoBuster file
            .tar	Compressed file archive created by TAR (pax2exe.zoo)
            .tax	TurboTax file
            .taz	Compressed ASCII file archive created by TAR and COMPRESS (.tar.Z)
            .tb1	Font file (Borland Turbo C)
            .tb2	Font file (Borland Turbo C)
            .tbf	Fax (Imavox TurboFax)
            .tbh	Mah Jongg for Windows Tile Set
            .tbk	Memo backup (dBASE IV – FoxPro)
            Toolbook (Asymetrix ToolBook)
            .tbl	Graphics (native format) (Adobe PageMaker TableEditor)
            Table of values (OS/2)
            .tbs	Text elements ?? (Textbausteine) (MS Word)
            .tbx	Table (Project Scheduler 4)
            .tc	Configuration (Turbo C – Borland C++)
            .tch	Turbo C Help file (Borland C++)
            .tcl	Tool Command Language source code (Swat)
            .tcp	3D Topicscape (exported inter-Topicscape topic link)
            .tcw	Drawing (TurboCAD for Windows)
            .td	Configuration file (Turbo Debugger for DOS)
            .td0	Disk image file (Teledisk)
            .td2	Configuration file (Turbo Debugger for Win32)
            .tdb	Database (TACT)
            eBay Turbo Lister file
            .tdf	Font (TheDraw)
            Typeface definition file (Speedo)
            .tdh	Help file (Turbo Debugger)
            .tdk	Keystroke recording file (Turbo Debugger)
            .tds	Symbol table (Turbo Debugger)
            .tdt	ASCII Data File in CSV Format
            Daylight Fingerprint Data file
            Thor Datatree file
            .tdw	Configuration file (Turbo Debugger for Windows)
            .tee	TeeChart Office graphic
            .tef	Fax (Relisys TEFAX)
            .tel	Host file (Telnet)
            .tem	Turbo Editor Macro Language script (Borland C++)
            Input template (IconAuthor)
            .temp	Temporary file
            .test	Test File Extension
            .tex	LaTeX Source Document file
            Tex text file (Scientific Word)
            Datasheet (Idealist)
            .text	ASCII Text file
            .tf	Configuration (Turbo Profiler)
            Configuration (TinyFugue)
            .tfa	Area file (Turbo Profiler)
            .tfc	Catalogue file (Tobi’s Floppy Cataloguer)
            .tfh	Help file (Turbo Profiler)
            .tfm	Tex Font Metric file (TeX)
            Tagged font metric file (Intellifont)
            .tfs	Statistics (Turbo Profiler)
            .tfw	ArcView World File For TIF Image
            Digital Raster Graphic World
            .tg1	Project file (On Target)
            .tga	Truevision Targa bitmap graphics
            .tgz	Compressed file archive created by TAR and GNUzip (.tar.gz)
            .thb	KinuPix Skin
            .thd	Thread
            .thm	Thumbnail Image file
            Microsoft Clipart Gallery database
            Serif DrawPlus Theme
            .thn	Graphics Workshop for Windows Thumbnail
            .ths	Thesaurus dictionary (WordPerfect for Win)
            .tib	Acronis True Image file
            .tif	Tagged Image File Format bitmap graphics (PageMaker – CorelDRAW)
            .tiff	Tagged Image File Format
            .til	Fuzzy logic knowledge base (Togai InfraLogic Fuzzy-C Compiler)
            .tim	Playstation Game Texture Image
            The Incredible Machine Level File
            .tis	Tile set (MahJongg 3.0)
            .tix	ASA for UNIX Terminfo Extension file
            DivX file
            Hybrid Graphics file
            Tix Widgets
            .tjl	Backup file (VAXTPU editor)
            .tlb	OLE Type Library
            Reference table (Bubble Chamber)
            Text library (VAX)
            Type library (Visual C++)
            .tlc	Compiled Tool Command Language source code (Swat)
            .tlp	Project (TimeLine)
            .tlt	Trellix Web Design file
            .tmb	Timbuktu Pro Connection Document
            .tmd	Document (TextMaker)
            .tmf	Tagged Font Metric file (WordPerfect for Win)
            .tmo	Ztg global optimizer default output file (Zortech C++)
            .tmp	Temporary file
            .tmpl	eMule Web Interface Template file
            .tmq	TestMaster file
            .tms	Script (Telemate)
            .tmv	Template (TextMaker)
            .toc	Table Of Contents
            PSP Audio file
            .tol	Kodak Photoenhancer
            .TOPC	TopicCrunch project file for saving and resubmitting SEO searches
            .tos	Self-extracting file archive (Atari ST)
            .tp	Configuration (Turbo Pascal)
            Session-state file (Turbo Profiler)
            GUI template file for components written in C (Ternion)
            .tp3	Template (Harvard Graphics 3.0)
            .tpb	Downloadable PCL Soft font file backup (HiJaak)
            .tpf	Downloadable PCL Soft font file (HiJaak)
            .tph	Help file (Turbo Pascal)
            .tpi	Microsoft Test file
            .tpl	Document Template file
            Resident units library (Turbo Pascal)
            Template (Harvard Graphics 2.0)
            .tpp	Protected Mode Units (Borland Pascal 7.0)
            Teleport Pro Project file
            GUI template file for components written in C++ (Ternion)
            .tps	Clarion for Windows data file
            .tpu	Turbo Pascal Unit (BGI) (Turbo Pascal)
            Command file (VAXTPU editor)
            .tpw	Session-state file (Turbo Profiler for Windows)
            Turbo Pascal Unit (BGI) (Turbo Pascal for Windows)
            .tpz	Compressed file archive created by TAR and GNUzip (.tar.gz)
            .tr	Session-state settings (Turbo Debugger for DOS)
            Man page input suitable for troff -man (cawf2.zip)
            .tr2	Session-state settings (Turbo Debugger for Win32)
            .trace	ECXpert Debugging file
            TcpDump Output file
            Telcordia Software Visualization and Analysis Toolsuite
            WebSTAR Mail Server Error file
            Zope 3 Strace Log
            .trc	Debug support file (Power CTrace)
            .tre	Directory tree file (PC-Tools)
            .trg	Symantec LiveUpdate file
            .tri	Trigram file
            .trk	Kermit Script file
            Mixman Studio Track
            Train Dispatcher Railroad Centgralized Traffic Control Simulation
            Magellan “MapSend”- series GPS ‘track’ data file
            .trm	Terminal settings (Windows 3.x)
            .trn	Translation support file (Quattro)
            .trp	Tripmaker file
            High Definition Video Transport Stream file
            .trs	Executable file (Micrografx)
            .trw	Session-state settings (Turbo Debugger for Windows)
            .trx	Router Firmware file
            Emerald PC Authorize Batch Transaction file
            .ts	Transport Stream file
            .tsk	Skins for Pocket PC PDAs
            PhotoImpact Quick Command
            .tsp	Windows Telephony Service Provider
            .tst	Printer test file (WordPerfect for Win)
            .tsv	Tab Separated Value file
            .tt10	Turbotax 2010 Return file
            .tta	The True Audio Codec file
            .ttc	OpenType font file
            .ttf	Truetype Font file
            .tub	PaintShop Pro Tube file
            .tut	Tutorial
            .tv	Table view settings (Paradox)
            .tv1	Overflow file above insert point in Doc 1 (WordPerfect for Win)
            .tv2	Overflow file above insert point in Doc 2 (WordPerfect for Win)
            .tv3	Overflow file above insert point in Doc 3 (WordPerfect for Win)
            .tv4	Overflow file above insert point in Doc 4 (WordPerfect for Win)
            .tv5	Overflow file above insert point in Doc 5 (WordPerfect for Win)
            .tv6	Overflow file above insert point in Doc 6 (WordPerfect for Win)
            .tv7	Overflow file above insert point in Doc 7 (WordPerfect for Win)
            .tv8	Overflow file above insert point in Doc 8 (WordPerfect for Win)
            .tv9	Overflow file above insert point in Doc 9 (WordPerfect for Win)
            .tvf	Table view settings (dBASE)
            .tvo	TeveoLive
            .tvp	NVIDIA Graphic Card Update file
            .tvr	Navicat for MySQL file
            .tvt	RealPlayer
            .txd	Grand Theft Auto 3 Texture file
            Letters Direct
            .txf	Compressed file archive created by TAR and FREEZE (.tar.f)
            .txi	Support file (TeX)
            .txl	Genesis3D Texture file
            .txt	Text file
            .tym	Time Stamp (PageMaker 4)
            .tz	Compressed file archive created by TAR and COMPRESS (.tar.Z)
            .tzb	Compressed file archive created by TAR – COMPRESS – BTOA (.tar.Z.btoa)
            .uax	Unreal Audio file
            .ub	Audio file (unsigned byte)
            .uc2	Compressed file archive created by UltraCompressor II (uc2.zip)
            .ucn	New compressed file archive created by UltraCompressor II
            .ucs	Universal Classification Standard Database file
            .udc	Acrobat Spelling file
            .udf	Filter (Photostyler)
            .udl	MS Data Link
            .uds	Sierra Generations Family file
            .ue2	Encrypted file archive created by UltraCompressor II
            .ufo	Ulead PhotoImpact Graphic file
            .uha	UHARC Compressed Archive file
            .uhs	Universal Hint System (binary file)
            .ui	Espire source code file (Geoworks UI Compiler)
            User interface (Sprint)
            .uif	MagicISO Disc Image file
            Long prompts for windows (WordPerfect for Win)
            .uih	Espire header file (Geoworks UI Compiler)
            .uis	WindowBlinds (Copyright Neil Banfield & Stardock.net, Inc.)
            .ul	Ulaw audio file
            .uld	Information about uploaded files (Procomm Plus)
            .ult	Music (UltraTracker)
            .umb	Backup file (MemMaker)
            .umd	Universal Media Disc file
            .umf	Stockmoves, MOTEK BV
            .umx	Unreal music file
            .uni	Unimod music module (MIKMOD)
            Datafile (Forecast Pro)
            .unl	Garmin Unlock file
            .unq	Fax View file
            .uns2	Ultra Notes Backup file
            .unx	Text file containing UNIX specific info
            .upd	Program update info
            Update data (dBASE)
            .upg	Firmware Upgrade file
            .upo	Compiled update data (dBASE)
            .upx	ULead Photo Express Saved Image file
            .url	Uniform Resource Locator (Internet shortcut)
            .urls	GetRight URL List file
            .usb	D-Link FM Radio Update
            USB Protocol Analyzer Trace
            .user	Visual Studio User Options file
            .usp	Printer font with USASCII extended character set (PageMaker)
            .usr	User database file (Procomm Plus – Turbo C++ tour)
            .utf	AOL Updating Files
            .utl	Sound file
            .utx	Unreal Engine Texture file
            Unicode file
            .uu	Compressed ASCII file archive created by UUDE/ENCODE
            .uue	Compressed ASCII file archive created by UUENCODE (uuexe515.exe)
            .uvf	CSV (comma separated value) format. Used by Netica
            .uvr	Ulead Cool 360 Viewer file
            .uw	Audio file (unsigned word)
            .uwl	WordPerfect User Word List file
            .v	Consistency check support file (ReaGeniX code generator)
            Main input file for an image (Vivid 2.0)
            .v2	Microsoft Live Messenger data file
            .v64	Nintento 64 Emulation ROM Image
            .val	Validity checks and referential integrity (Paradox for Windows)
            Values list object file (dBASE Application Generator)
            .van	Animation (VistaPro)
            .var	Variable file (IconAuthor)
            .vbc	Visual Business Cards
            .vbd	ActiveX file
            .vbe	VBScript Encoded Script file
            .vbn	Norton Corporate anti-virus quarantined file
            .vbp	Visual Basic Project file
            .vbs	Visual Basic Script file (Visual Basic)
            .vbw	Visual Basic Project Workplace (Visual Basic)
            .vbx	Visual Basic eXtension (Visual Basic)
            .vc	Include file with color definitions (Vivid 2.0)
            Spreatsheet (VisiCalc)
            .vc4	Virtual CD/DVD Image file
            .vcd	VisualCADD Drawing file
            Video CD format
            .vce	Visual CE Class Type file
            .vcf	VCard file
            .vch	Interlock Public Computer Utility
            .vcmf	VAIO Content Metadata file
            .vcs	vCalender file
            .vcw	Visual workbench information (MS Visual C++)
            .vcx	Spreatsheet (VisiCalc Advanced)
            .vda	Bitmap graphics
            .vdb	Norton AntiVirus Corporate Edition Update file
            PC-cillin Quarantined file
            .vdf	Avira AntiVir virus definition file
            Vexira Anti-virus virus definition file
            .vdi	Virtual Disk Images files
            .vdj	Virtual DJ Sample file
            .vdm	VDM Play
            .vdr	Drawing (ComputerEasy Draw)
            .vdx	XML for Visio Drawing file
            Vector Graphic file
            Virtual Device Driver
            .vem	VeePro Embroidery Software Format
            Voice E-mail file
            .ver	Version Description file
            .vew	View file (Clipper 5, Lotus Approach)
            .vfm	Voting Form (Voter)
            .vfn	Voting Form for Customers (Voter)
            .vfp	TMPGEnc VFAPI Plug-in
            .vfs	Virtual File System Index
            .vfx	Ulead Video Studio Sample file
            .vga	Vga display driver
            Vga display font
            .vgd	Vga display driver (Generic CADD)
            .vgr	Graphics (Ventura Publisher)
            .vhd	Virtual Hard Disk file
            .vi	Graphics (Jovian Logic VI)
            .vic	Vicar graphics
            .vid	Video file
            Ms-DOS Shell Monitor file (MS-DOS 5)
            Bitmap graphics (YUV12C M-Motion Frame Buffer)
            Screen device driver (Word)
            .vif	Khoros Visualization image file (SDSC Image Tool)
            .vik	Viking graphics
            .vir	Virus Infected file
            .vis	Vis graphics
            .viv	VivoActive Player Video file
            .vlm	Ashlar-Vellum file
            Novell Virtual Loadable Module
            Vellum CAD Drawing
            .vlt	WinVault Container file
            .vm	Virtual Memory file (Geoworks)
            .vm1	Panasonic SD Voice Editor file
            .vmc	Virtual memory configuration (Acrobat reader)
            .vmdk	VMware Image file
            .vmf	Font characteristics (Ventura Publisher)
            Voice mail file (VocalTec Voice)
            .vmg	Text Message files
            .vml	Vector Markup Language
            .vmo	Mobile Phone voice file (Siemens Sl45)
            Virtools Behavioral Server Composition (Web-based Protected Format)
            Cosmopolitan Virtual Makeover File
            .vmp	Logos Library System 2.x Verse Map
            .vms	Text file containing VMS specific info
            .vmt	Valve Material file. Details how a material is to be rendered
            .vmx	VMware Configuration file
            .vnt	vNote file
            .vo	Include file with object definition (Vivid 2.0)
            .vob	DVD video movie file
            .voc	Digitized samples (Creative Voice file)
            .vof	Object folder (VZ Programmer)
            .vol	VOL Archive file
            Tribes 2 game file
            Earth Siege 2 Archive
            Giants: Citizen Kabuto Archive
            Tribes Archive
            Tribes Extreme Archive
            .vor	OpenOffice.org Template
            .vox	Vox Audio
            Dialogic ADPCM
            Talking Technology Inc. file
            Natural MicroSystmes Voice file
            .vp6	TrueMotion VP6 Video file
            .vpa	Excite Chat Gestures file
            .vpd	Virpet Performance Descriptor
            VitaGraph file
            .vpg	Graphics (VPGraphics)
            .vpk	Steam Package Archive file
            .vpl	Karaoke Player Playlist file
            Virtual Property List file
            .vpp	Virtual Pool Game
            Red Faction/Summoner Package file
            .vqe	Yamaha Sound-VQ Locator File
            .vqf	Yamaha Sound-VQ File
            .vql	Yamaha Sound-VQ Locator File
            .vrd	VRScape data file
            .vrm	Overlay file (QuattroPro)
            .vro	Panasonic DVD Recorder file
            .vrp	Project (WATCOM VX?Rexx)
            .vrs	Video Resource eg. video device driver (WordPerfect)
            .vs	Include file with surface definition (Vivid 2.0)
            .vsd	Diagram (Shapeware Visio)
            .vsl	GetRight Download List file
            Visio Library
            .vsm	Simulation model (VisSim)
            .vsp	Visual Studio file
            Sprite (SPX)
            Backup Exec 9.1 and higher
            .vss	Smartshapes file (Shapeware Visio)
            .vst	Truevision Vista bitmap graphics
            .vtf	Valve Texture file. Used to store texture data
            .vts	DVD File format
            .vtx	XML for Visio template file
            .vue	Animation (3D Studio)
            View (dBASE IV – FoxPro)
            .vw	Text file (Volkswriter)
            .vw3	Text file (Volkswriter 3)
            .vwl	VideoWave Video Wave Library
            .vwr	File viewer file (PC Tools)
            .vwt	VideoWave Thumbnail
            .vxd	Virtual device driver (MS Windows)
            .vyd	VyperHelp
            .w	Database AppBuilder Source Code file
            Word chart file (APPLAUSE)
            .w02	Multiple Archive file
            .w30	Printer font (AST TurboLaser) (Ventura Publisher)
            .w31	Startup file (Windows 3.1)
            .w3g	Warcraft III file
            .w3m	Warcraft III Map file
            .w44	Temporary file for Sort or Index (dBASE)
            .w5v	Winamp file
            .wab	Outlook File
            .wac	Infinity Game Engine WAVC Sound
            .wad	Doom Game file
            Gunman Chronicle Archive
            Half Life Archive
            Heretic Archive
            Hexen Archive
            Quake Archive
            Theme Park World Archive
            .waf	Mayim’s WAF Compiler file
            .wal	Winamp Skin file
            WalMaster Showlist file
            .war	Java Web Archive (used by Servlets)
            Konqeror HTML page archive
            .wav	Waveform audio file (RIFF WAVE format)
            .wax	Windows Media Player Redirect file
            .wb1	Notebook (Quattro Pro)
            .wb2	Spreadsheet (Quattro Pro)
            .wb3	Quattro Pro for Windows
            .wba	WindowBlinds Compressed Skin
            Winace Zip file
            .wbc	Webshots Picture Collection
            .wbf	Ms Windows Batch File (Catch)
            .wbk	Document/workbook (WordPerfect for Win)
            .wbmp	Wireless Application Protocol Bitmap file
            .wbt	Batch file (WinBatch)
            .wbx	Webigger file
            .wbz	WebShots file
            .wcd	Macro token list (WordPerfect for Win)
            .wcm	Data transmission file (MS Works)
            Macro (WordPerfect for Win)
            .wcp	Product information description (WordPerfect for Win)
            .wd2	Info Select for Palm Organizer file
            WordExpress Document
            .wdb	Database (MS Works)
            .wdf	ReliaSoft Weibull 5.0
            Workshare DeltaView DeltaFile
            .wdl	Windows XP Watchdog Log file
            .web	Web source code file
            .wer	Microsoft Windows Error Report file
            .wfc	Windows Connect Now file
            .wfm	Form object (dBASE Form Designer)
            .wfn	Font (CorelDRAW)
            .wfx	Data file (Winfax)
            .wg1	Worksheet (Lotus 1-2-3/G)
            .wg2	Worksheet (Lotus 1-2-3 for OS/2)
            .wgt	Opera Widget file
            .wid	Width table (Ventura Publisher)
            .wim	Image Format file
            .win	Opera Saved Window file
            Window file (FoxPro – dBASE)
            Wonderware InTouch window file
            .wiz	Page wizard (MS Publisher)
            .wjp	WildTangent Branded .jpg file
            .wk1	Spreadsheet (Lotus 1-2-3 version 2.x – Symphony 1.1+)
            .wk3	Spreadsheet (Lotus 1-2-3 version 3.x)
            .wk4	Spreadsheet (Lotus 1-2-3 version 3.4)
            .wkb	Document (WordPerfect for Win)
            Workbook file
            .wke	Spreatsheet (Lotus 1-2-3 educational version)
            .wkq	Spreatsheet (Quattro)
            .wks	Spreadsheet (Lotus 1-2-3 version 1A – Symphony 1.0 – MS Works)
            Workspace (Xlisp)
            .wll	Word Add-in
            .wlk	Graphics (Virtus Walkthrough)
            .wlt	eWallet file
            WaveL Wavelet Compressed Graphic
            Words of Worship Liturgy
            .wma	Microsoft Active Streaming file
            .wmc	Backup of startup files by Windows MathCad autoexec.wmc
            Macro file (WordPerfect for Win)
            Text file (WordMARC)
            .wmf	Windows MetaFile vector graphics
            .wml	Wireless Markup Language
            .wmv	MS Active Streaming file
            .wmz	Windows Media Compressed skin file
            .wn	Text (NeXT WriteNow)
            .wnf	Outline font description (CorelDRAW native format)
            .wo4	STABCAL file
            .wo7	STABCAL file
            .woa	Swap file (Windows 3.x)
            .woc	Microsoft Office 2007 Organization file
            Organization (Windows OrgChart)
            .wor	MapInfo Workspace
            .wot	WebEx Saved Meeting Movie
            .wow	Music (8 channels) (Grave Mod Player)
            .wp	Text file (WordPerfect 4.2)
            .wp3	Microsoft Photo Story Project file
            .wp5	Document (WordPerfect 5.x)
            .wpd	Document (WordPerfect 6.0 – PFS:WindowWorks)
            .wpf	Fax (WorldPort)
            Form (WordPerfect)
            .wpg	WildTangent Branded .PNG file
            Wordperfect Graphics vector graphics (DrawPerfect)
            .wpj	MS Works Projects
            .wpk	Macros (WordPerfect for Win)
            .wpl	Windows Media Player Playlist file/td>
            Draxy Software Wallpaper Sequencer
            Online WebPanel file
            PFS WinWorks Spreadsheet
            WHAT IF MOL-object
            Words of Worship Playlist
            .wpm	Macros (WordPerfect)
            .wps	Text document (MS Works)
            .wpt	WordPerfect template
            602 pro PC SUITE template document file
            .wpw	PerfectWorks document
            .wq!	Compressed spreadsheet (Quattro Pro)
            .wq1	Spreadsheet (Quattro Pro)
            .wr1	Spreadsheet (Symphony 1.1 – 1.2 – 2)
            .wrd	Template (Charisma)
            .wrf	used for WebEx recording. Microsoft office add-in for meeting
            .wri	Text file (Windows Write)
            .wrk	Spreadsheet (Symphony 1.0, 1.2, 2.0, 3.0)
            .wrl	Plain text VRML file
            .wrml	Plain text VRML file
            .wrp	Compressed Amiga file archive created by WARP
            .wrs	Windows Resource eg. printer driver (WordPerfect for Win)
            .ws	Text file (WordStar 5.0-6.0)
            .wsf	Windows Script file
            .wss	Web Screen Saver file (Web Screen Saver 2008)
            .ws2	Text file (WordStar 2000)
            .wsc	Windows scripting component file
            .wsd	Document (WordStar)
            .wsf	Windows Script file
            .wsh	Windows Script Host Settings file
            .wsp	Workspace (Fortran PowerStation)
            .wsr	FirstStop WebSearch file
            .wss	Web Screen Saver file (Web Screen Saver 2008)
            .wst	Text file (WordStar)
            .wsx	WinMX Filesharing Program
            .wsz	Skin Zip file (WinAmp)
            .wtd	WinTune Document file
            .wtr	MS Encarta file
            .wv	WavPack compressed Audio file
            .wve	Component of a DIVX Movie Conversion
            Psion Series 3a/3c/3mx Waveform sound file
            .wvx	Metafile
            .wvw	Backup Wonderware InTouch window file
            .wwb	Button bar for document window (WordPerfect for Win)
            .wwk	Keyboard layout (WordPerfect for Win)
            .wwp	Worms World Party Teams file
            .wws	AutoRoute User Information
            .wwv	WildTangent Branded .WAV file
            .wxp	Document (EXP for Windows)
            .wxs	Easy Cross crosstitch file
            .wzg	WZebra file
            .wzs	Microsoft Word wizard
            .x	DirectX Object file
            AVS X image file (SDSC Image Tool)
            Lex source code file
            .x01	Secondary index (Paradox)
            .x02	Secondary index (Paradox)
            .x03	Secondary index (Paradox)
            .x04	Secondary index (Paradox)
            .x05	Secondary index (Paradox)
            .x06	Secondary index (Paradox)
            .x07	Secondary index (Paradox)
            .x08	Secondary index (Paradox)
            .x09	Secondary index (Paradox)
            .x16	Macromedia Program Extension (16-bit)
            .x32	Macromedia Program Extension (32-bit)
            .xap	Silveright Application Package
            .xbel	XML Bookmark Exchange Language file
            .xbm	X11 Bitmap graphics
            .xcf	Gimp Image file
            .xdf	Milnta APL Transfer Function
            Workshare Synergy file
            .xdw	X Windows Screen Dump file
            .xef	X-Genics eManager – XML form and data for eManager
            .xem	X-Genics eManager – Metered units / credit definition for forms/file usage in eManager
            .xep	X-Genics eManager – File packaging / unpacking information for eManager components
            .xes	X-Genics eManager – XML definition for UI skins
            .xet	X-Genics eManager – XML definition for eManager process
            .xev	X-Genics eManager – File download definition for auto-update and delivery of new procedures
            .xez	X-Genics eManager – Template package for eManager
            .xfd	XML Form in XFDL Format
            .xfdl	Extensible Forms Description Language file
            .xfn	Printer font (Xerox 4045) (Ventura Publisher)
            .xft	24 pin printer font (ChiWriter)
            .xfx	Fax File (various)
            .xhtml	Extensible HyperText Markup Language file
            .xi	Fast Tracker 2 Instrument or ScreamTracker Instrument file
            .xif	Wang image file
            Often a Fax image (TIFF) file
            ScanSoft Pagis XIF Extended Image Format
            Xerox image file
            .xla	Xlib Archive (xlibpas2.zip)
            .xla	Add-in macro sheet (MS Excel)
            .xlb	Data (MS Excel)
            .xlc	Chart document (MS Excel)
            .xlk	Excel Backup
            .xll	Excel Dynamic Link Library (MS Excel)
            .xlm	Macro sheet (MS Excel)
            .xlr	MS Works file
            .xls	Spreadsheet(MS Works)
            DATAIR Data Import Specification Translation file
            Worksheet (MS Excel)
            .xlsm	Microsoft Excel Macro-Enabled Workbook file
            .xlsx	Microsoft Excel XML file
            .xlt	Template (MS Excel)
            Translation table (Lotus 1-2-3 – Symphony – Procomm Plus)
            .xlw	Workbook (MS Excel)
            .xlx	XoloX Incomplete Download file
            .xm	Music (Fast Tracker)
            .xmi	Compressed eXtended MIdi music
            .xml	Extensible Markup Language file
            .xmp	Extensible Metadata Platform
            .xnf	Standard Network File form
            .xpi	XPInstall File
            Digital surveillance system
            .xnk	Microsoft Exchange Shortcut
            .xpl	Music file
            .xpm	X11 Pixel Map graphics
            .xpr	Memorex CD-ROM label file
            .xps	XML Paper Specification file
            .xpt	Mozilla Firefox Component file
            XPCOM Type Library
            .xpw	Leading Market Technologies EXPO
            Screen-Fillable Surfer Version of a Form
            .xqt	Executable file (Waffle)
            Macro sheet (SuperCalc)
            .xpv	digital surveillance system
            .xrf	Cross-reference file
            .xsd	XML Schema file
            .xsf	Milnta APL Transfer Function
            .xsl	Extensible Stylesheet Language file
            .xspf	XML Shareable Playlist file
            .xss	Ability Office Spreadsheet
            .xtb	External translation table (LocoScript)
            .xtm	Xtremsplit Data file
            .xtr	MapTool file (an add-on for UI-View)
            Xtreme Tuning files
            .xul	XML User Interface Language file
            .xvb	WinExplorer VB Script
            .xvid	Xvid Video file
            .xvl	Compact 3D file format for web apps.(Lattice 3D)
            .xwd	X Window System window dump image graphics (SDSC Image Tool)
            .xwk	Keyboard mapping (Crosstalk)
            .xwp	Session (Crosstalk)
            Text file (Xerox Writer)
            .xx	Compressed file ASCII archive created by XXENCODE (uuexe515.exe)
            .xxe	Compressed file ASCII archive created by XXENCODE (uuexe515.exe)
            .xxx	Singer Sewing Machine Professional SewWare file
            Embroidery Design file
            .xy	Text file (XY Write)
            .xy3	Text file (XYWrite III)
            .xyw	Text file (XyWrite III)
            .xyz	ASCII RPG Maker Graphic Format
            .xz	XZ Compressed Archive file
            .y	Yacc grammar file
            Compressed Amiga file archive created by YABBA
            .y01	Secondary index (Paradox)
            .y02	Secondary index (Paradox)
            .y03	Secondary index (Paradox)
            .y04	Secondary index (Paradox)
            .y05	Secondary index (Paradox)
            .y06	Secondary index (Paradox)
            .y07	Secondary index (Paradox)
            .y08	Secondary index (Paradox)
            .y09	Secondary index (Paradox)
            .yab	Yabasic Source Code file
            .yal	Data (Arts & Letters)
            .ybk	Microsoft Encarta Yearbook file
            .ychat	Yahoo! Messenger chat log
            .yenc	yEnc file
            .ymg	Yahoo! Messenger file
            .yml	YAML file
            .ync	yEnc Encoded file
            .yps	Yahoo! Messenger Data file
            .yuv	YUV Encoded Image or Video file
            .yz	Compressed file archive created by YAC
            .yz1	Yamazaki ZIPPER file
            .z	Compressed file ASCII archive created by COMPRESS (comp430d.zip)
            Unix Compressed file archive created by PACK (Unix SysV pack)
            .z01	Winzip Split Archive file
            .z02	Split Archive file
            .z1	ZoneAlarm Renamed VB file
            .z3	Infocom game module
            .zap	Zero Administration Package file
            FileWrangler Compressed file
            MS Windows Software Installation Settings
            .zbd	Canon ZoomBrowser Database file
            MechWarrior 3 Snow Fields file
            Zebedee Encrypted file
            .zdb	Zimbra Database File
            .zdb	
            .zdct	After Effects Language file
            .zdg	Compressed ZiffNet text document (Zview)
            .zdl	Design Pro Label file
            .zdp	ZDNet Password Pro 32
            .zer	Data file (Zerberus)
            .zfx	ZFX – CC3 File Packer Tool
            .zgm	Graphics (Zenographics)
            .zhtml	Secure IE Zipped HTML file
            .zi	Renamed Zip file
            .zif	Zooming Image Format file
            .zip	ZIP Compressed file archive
            .zipx	WinZip Compressed file
            .zix	Quicken Data file
            WinZix Compressed file
            .zl?	Zone Alarm Mailsafe Renamed File.
            ZoneAlarm quarantines attachments and changes their file names.
            ZoneAlarm Quarantined EXE File (Ex. .EXE to .zl9)
            .zl	Zlib Compressed file
            .zls	Atlantis Ocean Mind Word Processing file
            .zmc	ZoneAlarm Mailsafe
            .zom	Compressed Amiga file archive created by ZOOM
            .zon	Grand Theft Auto 3 Zone file
            .zoo	Compressed file archive created by ZOO (zoo210.exe)
            .zpk	Z Firm Package file
            .zpl	Creative Zen Micro playlist
            .zst	ZSNES Slot 0 Savestate
            .ztd	Ziff Davis Media text database
            .zvd	Zyxel Voicefile (Z-Fax)
            .zvz	Possible Virus file
            .zxp	Extension Manager Package
            .zz	Zzip Compressed Archive file
            .zzt	ZZT Game Creation System
        """[1:-1]
        for line in data.split("\n"):
            if "\t" in line:
                e, s = line.split("\t")
                if s.strip():
                    yield e.strip(), s.strip()

    def Wikipedia():
        "Generator to return (ext, descr) tuples"
        # From https://en.wikipedia.org/wiki/List_of_file_formats
        # 2 Dec 2023 09:25:35 AM

        data = """
            .?Q? – files that are compressed, often by the SQ program.
            7z – 7z: 7-Zip compressed file
            A – An external file extension for C/C++
            AAC – Advanced Audio Coding
            ACE – ace: ACE compressed file
            ALZ – ALZip compressed file
            APK – Android package: Applications installable on Android; package format of the Alpine Linux distribution
            APPX – Microsoft Application Package (.appx)
            APP – HarmonyOS APP Packs file format for HarmonyOS apps installable from AppGallery and third party OpenHarmony based app distribution stores.
            AT3 – Sony's UMD data compression
            ARC – ARC: pre-Zip data compression
            ARC – Nintendo U8 Archive (mostly Yaz0 compressed)
            ARJ – ARJ compressed file
            ASS, SSA – ASS (also SSA): a subtitles file created by Aegisub, a video typesetting application (also a Halo game engine file)
            B – (B file) Similar to .a, but less compressed.
            BA – BA: Scifer Archive (.ba), Scifer External Archive Type
            BIN – compressed archive, can be read and used by CD-ROMs and Java, extractable by 7-zip and WINRAR
            BKF – Microsoft backup created by NTBackup.c
            BLEND – An external 3D file format used by the animation software, Blender.
            BZ2 – bzip2
            BMP – Bitmap Image – You can create one by right-clicking the home screen, next, click new, then, click Bitmap Image
            CAB – A cabinet (.cab) file is a library of compressed files stored as one file. Cabinet files are used to organize installation files that are copied to the user's system.[2]
            C4 – JEDMICS image files, a DOD system
            CALS – JEDMICS image files, a DOD system
            XAML – Used in programs like Visual Studio to create exe files.
            CPT, SEA – Compact Pro (Macintosh)
            DAA – DAA: Closed-format, Windows-only compressed disk image
            DEB – deb: Debian install package
            DMG – an Apple compressed/encrypted format
            DDZ – a file which can only be used by the "daydreamer engine" created by "fever-dreamer", a program similar to RAGS, it's mainly used to make somewhat short games.
            DN – Adobe Dimension CC file format
            DNG – "Digital Negative" a type of raw image file format used in digital photography.
            DPE – Package of AVE documents made with Aquafadas digital publishing tools.
            EGG – Alzip Egg Edition compressed file
            EGT – EGT Universal Document also used to create compressed cabinet files replaces .ecab
            ECAB, EZIP – EGT Compressed Folder used in advanced systems to compress entire system folders, replaced by EGT Universal Document
            ESD – ESD: Electronic Software Distribution, a compressed and encrypted WIM File
            ESS – EGT SmartSense File, detects files compressed using the EGT compression system.
            EXE – Windows application
            FLIPCHART – Used in Promethean ActivInspire Flipchart Software.
            FUN – A FUN file is a file that has been encrypted by Jigsaw ransomware, which is malware distributed by cybercriminals. It contains a file, such as a .JPG, .DOCX, .XLSX, .MP4, or .CSV file, that has been renamed and encrypted by the virus.
            FLM – FL Studio Mobile, can also be used as a project file.
            FLP – FL Studio Project File
            GBS, GGP, GSC – GBS OtterUI binary scene file
            GHO, GHS – GHO Norton Ghost
            GIF – GIF Graphics Interchange Format
            GZ – gzip Compressed file
            IPG – Format in which Apple Inc. packages their iPod games. can be extracted through Winrar
            JAR – jar ZIP file with manifest for use with Java applications.
            JPG – Joint Photographic Experts Group – Image File
            JPEG – Joint Photographic Experts Group – Image File
            LAWRENCE – LBR Lawrence Compiler Type file
            LBR – LBR Library file
            LLSP3 – Lego Spike program file
            LQR – LQR LBR Library file compressed by the SQ program.
            LZH – LHA Lempel, Ziv, Huffman
            LZ – lzip Compressed file
            IZO – lzo
            IZMA – lzma Lempel–Ziv–Markov chain algorithm compressed file
            LZX – LZX
            LUA – Lua
            MBW – MBRWizard archive
            MHTML – Mime HTML (Hyper-Text Markup Language) code file
            MIDI, MID – Musical Instrument Digital Interface
            MPQ – MPQ Archives Used by Blizzard Entertainment
            BIN – BIN MacBinary
            NL2PKG – NoLimits 2 Package
            NTH – NTH: Nokia Theme Used by Nokia Series 40 Cellphones
            OAR – OAR: OAR archive
            OGG – Ogg Vorbis Compressed Audio File
            OSG – Compressed osu! live gameplay archive (optimized for spectating)
            OSK – Compressed osu! skin archive
            OSR – Compressed osu! replay archive
            OSZ – Compressed osu! beatmap archive
            PAK – Enhanced type of .ARC archive
            PAR, PAR 2 – PAR Parchive
            PART – A file used with Stud.Io
            PAF – PAF Portable Application File
            PEA – PEA PeaZip archive file
            PNG – Portable Network Graphic Image File
            WEBP – Raster image format developed by Google for web graphics
            PHP – PHP code file
            PYK – PYK Compressed file
            PK3 – PK3 Quake 3 archive (See note on Doom³)
            PK4 – PK4 Doom³ archive (Opens similarly to a zip archive.)
            PNJ – sub-format of the MNG file format, used for encapsulating JPEG files[3]
            PXZ – PXZ A compressed layered image file used for the image editing website, pixlr.com .
            PY, PYW – Python code file
            PMP – Penguinmod Project
            RAR – RAR Rar Archive, for multiple file archive (rar to .r01-.r99 to s01 and so on)
            RAG, RAGS – Game file, a game playable in the RAGS game-engine, a free program which both allows people to create games, and play games, games created have the format "RAG game file"
            RaX – Archive file created by RaX
            RBXL – Roblox Studio place file (XML, binary)
            RBXLX – Roblox Studio place file (exclusively XML)
            RBXM – Roblox Studio model file (XML, binary)
            RBXMX – Roblox Studio model file (exclusively XML)
            RPM – Red Hat package/installer for Fedora, RHEL, and similar systems.
            SB – Scratch 1.X file
            SB2 – Scratch 2.0 file
            SB3 – Scratch 3.0 file
            SEN – Scifer Archive (.sen) – Scifer Internal Archive Type
            SF2 – Polyphone Soundfont 2
            SF3 – Polyphone Soundfont 3
            SF4 – Polyphone Soundfont 4
            SITX – SIT StuffIt (Macintosh)
            SIS, SISX – SIS/SISX: Symbian Application Package
            SKB – Google SketchUp backup File
            SQ – SQ: Squish Compressed Archive
            SRT – SubRip Subtitle – file format for closed captioning or subtitles.
            SWM – Splitted WIM File, usually found on OEM Recovery Partition to store preinstalled Windows image, and to make Recovery backup (to USB Drive) easier (due to FAT32 limitations)
            SZS – Nintendo Yaz0 Compressed Archive
            TAR – TAR: group of files, packaged as one file
            GZIP, TAR.GZ – (Gzip, .tar.gz): TGZ gzipped tar file
            TB – TB Tabbery Virtual Desktop Tab file
            TIB – TIB Acronis True Image backup
            UHA – Ultra High Archive Compression
            UUE – UUE unified utility engine – the generic and default format for all things UUe-related.
            UF2 – Microsoft makecode arcade game.
            VIV – Archive format used to compress data for several video games, including Need For Speed: High Stakes.
            VOL – video game data package.
            VSA – Altiris Virtual Software Archive
            WAX – Wavexpress – A ZIP alternative optimized for packages containing video, allowing multiple packaged files to be all-or-none delivered with near-instantaneous unpacking via NTFS file system manipulation.
            WAV, WAVE – a format for storing uncompressed audio files.
            WFP – a Wondershare Flimora project file
            WIM – WIM A compressed disk image for installing Windows Vista or higher, Windows Fundamentals for Legacy PC, or restoring a system image made from Backup and Restore (Windows Vista/7)
            XAP – Windows Phone Application Package
            XZ – xz compressed files, based on LZMA/LZMA2 algorithm
            Z – Unix compress file
            ZOO – zoo: based on LZW
            ZIP – zip: popular compression format
            ZIM – ZIM: an open file format that stores wiki content for offline usage
            Physical recordable media archiving
            ISO – Generic format for most optical media, including CD-ROM, DVD-ROM, Blu-ray, HD DVD and UMD.
            NRG – Proprietary optical media archive format used by Nero applications.
            IMG – Raw disk image, for archiving DOS formatted floppy disks, hard drives, and larger optical media.
            ADF – for archiving Amiga floppy disks
            ADZ – The GZip-compressed version of ADF.
            DMS – a disk-archiving system native to the Amiga.
            DSK – For archiving floppy disks from a number of other platforms, including the ZX Spectrum and Amstrad CPC.
            D64 – An archive of a Commodore 64 floppy disk.
            SDI – used for archiving and providing "virtual disk" functionality.
            MDS – Daemon Tools native disc image format used for making images from optical CD-ROM, DVD-ROM, HD DVD or Blu-ray. It comes together with MDF file and can be mounted with DAEMON Tools.
            MDX – Daemon Tools format that allows getting one MDX disc image file instead of two (MDF and MDS).
            DMG – Macintosh disk image files
            CDI – DiscJuggler image file
            CUE – CDRWrite CUE image file
            CIF – Easy CD Creator .cif format
            C2D – Roxio-WinOnCD .c2d format
            DAA – PowerISO .daa format
            B6T – BlindWrite 6 image file
            B5T – BlindWrite 5 image file
            BWT – BlindWrite 4 image file
            FFPPKG – FreeFire Profile Export Package
            LemonOS/LemonTabOS/LemonRoid
            LEMONAPP – LemonOS/LemonTabOS/LemonRoid App (.lem_app)
            Other extensions
            Msi – Windows installation file
            Vdhx – Virtual disk created by Hyper-V (Hyper-V runs on windows operating system)
            Computer-aided design
            Computer-aided is a prefix for several categories of tools (e.g., design, manufacture, engineering) which assist professionals in their respective fields (e.g., machining, architecture, schematics).
            
            Computer-aided design (CAD)
            Computer-aided design (CAD) software assists engineers, architects and other design professionals in project design.
            
            3DXML – Dassault Systemes graphic representation
            3MF – Microsoft 3D Manufacturing Format[4]
            ACP – VA Software VA – Virtual Architecture CAD file
            AMF – Additive Manufacturing File Format
            AEC – DataCAD drawing format[5]
            AR – Ashlar-Vellum Argon – 3D Modeling
            ART – ArtCAM model
            ASC – BRL-CAD Geometry File (old ASCII format)
            ASM – Solidedge Assembly, Pro/ENGINEER Assembly
            BIN, BIM – Data Design System DDS-CAD
            BREP – Open CASCADE 3D model (shape)
            C3D – C3D Toolkit File Format
            C3P – Construct3 Files
            CCC – CopyCAD Curves
            CCM – CopyCAD Model
            CCS – CopyCAD Session
            CAD – CadStd
            CATDrawing – CATIA V5 Drawing document
            CATPart – CATIA V5 Part document
            CATProduct – CATIA V5 Assembly document
            CATProcess – CATIA V5 Manufacturing document
            cgr – CATIA V5 graphic representation file
            CKD – KeyCreator CAD parts, assemblies, and drawings
            CKT – KeyCreator template file
            CO – Ashlar-Vellum Cobalt – parametric drafting and 3D modeling
            DRW – Caddie Early version of Caddie drawing – Prior to Caddie changing to DWG
            DFT – Solidedge Draft
            DGN – MicroStation design file
            DGK – Delcam Geometry
            DMT – Delcam Machining Triangles
            DXF – ASCII Drawing Interchange file format, AutoCAD
            DWB – VariCAD drawing file
            DWF – Autodesk's Web Design Format; AutoCAD & Revit can publish to this format; similar in concept to PDF files; Autodesk Design Review is the reader
            DWG – Popular file format for Computer Aided Drafting applications, notably AutoCAD, Open Design Alliance applications, and Autodesk Inventor Drawing files
            EASM – SolidWorks eDrawings assembly file
            EDRW – eDrawings drawing file
            EMB – Wilcom ES Designer Embroidery CAD file
            EPRT – eDrawings part file
            EscPcb – "esCAD pcb" data file by Electro-System (Japan)
            EscSch – "esCAD sch" data file by Electro-System (Japan)
            ESW – AGTEK format
            EXCELLON – Excellon file
            EXP – Drawing Express format
            F3D – Autodesk Fusion 360 archive file[6]
            FCStd – Native file format of FreeCAD CAD/CAM package
            FM – FeatureCAM Part File
            FMZ – FormZ Project file
            G – BRL-CAD Geometry File
            GBR – Gerber file
            GLM – KernelCAD model
            GRB – T-FLEX CAD File
            GRI – AppliCad GRIM-In file in readable text form for importing roof and wall cladding job data generated by business management and accounting systems into the modelling/estimating program
            GRO – AppliCad GRIM-Out file in readable text form for exporting roof and wall cladding data job material and labour costing data, material lists generated by the modelling/estimating program to business management and accounting systems
            IAM – Autodesk Inventor Assembly file
            ICD – IronCAD 2D CAD file
            IDW – Autodesk Inventor Drawing file
            IFC – buildingSMART for sharing AEC and FM data
            IGES – Initial Graphics Exchange Specification
            .dgn, .cel – Intergraph Standard File Formats Intergraph
            IO – Stud.io 3d model
            IPN – Autodesk Inventor Presentation file
            IPT – Autodesk Inventor Part file
            JT – Jupiter Tesselation
            MCD – Monu-CAD (Monument/Headstone Drawing file)
            MDG – Model of Digital Geometric Kernel
            model – CATIA V4 part document
            OCD – Orienteering Computer Aided Design (OCAD) file
            PAR – Solidedge Part
            PIPE – PIPE-FLO Professional Piping system design file
            PLN – ArchiCad project
            PRT – NX (recently known as Unigraphics), Pro/ENGINEER Part, CADKEY Part
            PSM – Solidedge Sheet
            PSMODEL – PowerSHAPE Model
            PWI – PowerINSPECT File
            PYT – Pythagoras File
            SKP – SketchUp Model
            RLF – ArtCAM Relief
            RVM – AVEVA PDMS 3D Review model
            RVT – Autodesk Revit project files
            RFA – Autodesk Revit family files
            RXF – AppliCad annotated 3D roof and wall geometry data in readable text form used to exchange 3D model geometry with other systems such as truss design software
            S12 – Spirit file, by Softtech
            SCAD – OpenSCAD 3D part model
            SCDOC – SpaceClaim 3D Part/Assembly
            SLDASM – SolidWorks Assembly drawing
            SLDDRW – SolidWorks 2D drawing
            SLDPRT – SolidWorks 3D part model
            dotXSI – For Softimage
            STEP – Standard for the Exchange of Product model data
            STL – Stereo Lithographic data format used by various CAD systems and stereo lithographic printing machines.
            STD – Power Vision Plus – Electricity Meter Data (Circuitor)
            TCT – TurboCAD drawing template
            TCW – TurboCAD for Windows 2D and 3D drawing
            UNV – I-DEAS I-DEAS (Integrated Design and Engineering Analysis Software)
            VC6 – Ashlar-Vellum Graphite – 2D and 3D drafting
            VLM – Ashlar-Vellum Vellum, Vellum 2D, Vellum Draft, Vellum 3D, DrawingBoard
            VS – Ashlar-Vellum Vellum Solids
            WRL – Similar to STL, but includes color. Used by various CAD systems and 3D printing rapid prototyping machines. Also used for VRML models on the web.
            X_B – Parasolids binary format
            X_T – Parasolids
            XE – Ashlar-Vellum Xenon – for associative 3D modeling
            ZOFZPROJ – ZofzPCB 3D PCB model, containing mesh, netlist and BOM
            Electronic design automation (EDA)
            Electronic design automation (EDA), or electronic computer-aided design (ECAD), is specific to the field of electrical engineering.
            
            BRD – Board file for EAGLE Layout Editor, a commercial PCB design tool
            BSDL – Description language for testing through JTAG
            CDL – Transistor-level netlist format for IC design
            CPF – Power-domain specification in system-on-a-chip (SoC) implementation (see also UPF)
            DEF – Gate-level layout
            Detailed Standard Parasitic Format – Detailed Standard Parasitic Format, Analog-level Parastic component of interconnections in IC design
            EDIF – Vendor neutral gate-level netlist format
            FSDB – Analog waveform format (see also Waveform viewer)
            GDSII – Format for PCB and layout of integrated circuits
            HEX – ASCII-coded binary format for memory dumps
            LEF – Library Exchange Format, physical abstract of cells for IC design
            Liberty (EDA) – Library modeling (function, timing) format
            MS12 – NI Multisim file
            OASIS – Open Artwork System Interchange Standard
            OpenAccess – Design database format with APIs
            PSF – Cadence proprietary format to store simulation results/waveforms (2GB limit)
            PSFXL – Cadence proprietary format to store simulation results/waveforms
            SDC – Synopsys Design Constraints, format for synthesis constraints
            SDF – Standard for gate-level timings
            SPEF – Standard format for Parasitic component of interconnections in IC design
            SPI, CIR – SPICE Netlist, device-level netlist and commands for simulation
            SREC, S19 – S-record, ASCII-coded format for memory dumps
            SST2 – Cadence proprietary format to store mixed-signal simulation results/waveforms
            STIL – Standard Test Interface Language, IEEE1450-1999 standard for Test Patterns for IC
            SV – SystemVerilog source file
            S*P – Touchstone/EEsof Scattering parameter data file – multi-port blackbox performance, measurement or simulated
            TLF – Contains timing and logical information about a collection of cells (circuit elements)
            UPF – Standard for Power-domain specification in SoC implementation
            V – Verilog source file
            VCD – Standard format for digital simulation waveform
            VHD, VHDL – VHDL source file
            WGL – Waveform Generation Language, format for Test Patterns for IC
            Test technology
            Files output from Automatic Test Equipment or post-processed from such.
            
            Standard Test Data Format
            Database
            4DB – 4D database Structure file
            4DC – 4D database Structure file (compiled in legacy mode)
            4DD – 4D database Data file
            4DIndy – 4D database Structure Index file
            4DIndx – 4D database Data Index file
            4DR – 4D database Data resource file (in old 4D versions)
            4DZ – 4D database Structure file (compiled in 4D Project mode)
            ACCDB – Microsoft Database (Microsoft Office Access 2007 and later)
            ACCDE – Compiled Microsoft Database (Microsoft Office Access 2007 and later)
            ADT – Sybase Advantage Database Server (ADS)
            APR – Lotus Approach data entry & reports
            BOX – Lotus Notes Post Office mail routing database
            CHML – Krasbit Technologies Encrypted database file for 1 click integration between contact management software and the Chameleon Software
            DAF – Digital Anchor data file
            DAT – DOS Basic
            DAT – Intersystems Caché database file
            DB – Paradox
            DB – SQLite
            DBF – db/dbase II,III,IV and V, Clipper, Harbour/xHarbour, Fox/FoxPro, Oracle
            DTA – Sage Sterling database file
            EGT – EGT Universal Document, used to compress sql databases to smaller files, may contain original EGT database style.
            ESS – EGT SmartSense is a database of files and its compression style. Specific to EGT SmartSense
            EAP – Enterprise Architect Project
            FDB – Firebird Databases
            FDB – Navision database file
            FP, FP3, FP5, FP7 – FileMaker Pro
            FRM – MySQL table definition
            GDB – Borland InterBase Databases
            GTABLE – Google Drive Fusion Table
            KEXI – Kexi database file (SQLite-based)
            KEXIC – shortcut to a database connection for a Kexi databases on a server
            KEXIS – shortcut to a Kexi database
            LDB – Temporary database file, only existing when database is open
            LIRS – Layered Intager Storage. Stores intageres with characters such as semicolons to create lists of data.
            MDA – Add-in file for Microsoft Access
            MDB – Microsoft Access database
            ADP – Microsoft Access project (used for accessing databases on a server)
            MDE – Compiled Microsoft Database (Access)
            MDF – Microsoft SQL Server Database
            MYD – MySQL MyISAM table data
            MYI – MySQL MyISAM table index
            NCF – Lotus Notes configuration file
            NSF – Lotus Notes database
            NTF – Lotus Notes database design template
            NV2 – QW Page NewViews object oriented accounting database
            ODB – LibreOffice Base or OpenOffice Base database
            ORA – Oracle tablespace files sometimes get this extension (also used for configuration files)
            PCONTACT – WinIM Contact file
            PDB – Palm OS Database
            PDI – Portable Database Image
            PDX – Corel Paradox database management
            PRC – Palm OS resource database
            SQL – bundled SQL queries
            REC – GNU recutils database
            REL – Sage Retrieve 4GL data file
            RIN – Sage Retrieve 4GL index file
            SDB – StarOffice's StarBase
            SDF – SQL Compact Database file
            sqlite – SQLite
            UDL – Universal Data Link
            waData – Wakanda (software) database Data file
            waIndx – Wakanda (software) database Index file
            waModel – Wakanda (software) database Model file
            waJournal – Wakanda (software) database Journal file
            WDB – Microsoft Works Database
            WMDB – Windows Media Database file – The CurrentDatabase_360.wmdb file can contain file name, file properties, music, video, photo and playlist information.
            Big Data (Distributed)
            Avro – Data format appropriate for ingestion of record based attributes. Distinguishing characteristic is schema is stored on each row enabling schema evolution.
            Parquet – Columnar data storage. It is typically used within the Hadoop ecosystem.
            ORC – Similar to Parquet, but has better data compression and schema evolution handling.
            Desktop publishing
            AI – Adobe Illustrator
            AVE, ZAVE – Aquafadas
            CDR – CorelDRAW
            CHP, pub, STY, CAP, CIF, VGR, FRM – Ventura Publisher – Xerox (DOS / GEM)
            CPT – Corel Photo-Paint
            DTP – Greenstreet Publisher, GST PressWorks
            FM – Adobe FrameMaker
            GDRAW – Google Drive Drawing
            ILDOC – Broadvision Quicksilver document
            INDD – Adobe InDesign
            MCF – FotoInsight Designer
            PDF – Adobe Acrobat or Adobe Reader
            PMD – Adobe PageMaker
            PPP – Serif PagePlus
            PSD – Adobe Photoshop
            PUB – Microsoft Publisher
            QXD – QuarkXPress
            SLA, SCD – Scribus
            XCF – XCF: File format used by the GIMP, as well as other programs
            Document
            These files store formatted text and plain text.
            
            0 – Plain Text Document, normally used for licensing
            1ST – Plain Text Document, normally preceded by the words "README" (README.1ST)
            600 – Plain Text Document, used in UNZIP history log
            602 – Text602 (T602) document
            ABW – AbiWord document
            ACL – MS Word AutoCorrect List
            AFP – Advanced Function Presentation
            AMI – Lotus Ami Pro Amigaguide
            ANS – American National Standards Institute (ANSI) text
            ASC – ASCII text
            AWW – Ability Write
            CCF – Color Chat 1.0
            CSV – ASCII text as comma-separated values, used in spreadsheets and database management systems
            CWK – ClarisWorks-AppleWorks document
            DBK – DocBook XML sub-format
            DITA – Darwin Information Typing Architecture document
            DOC – Microsoft Word document
            DOCM – Microsoft Word macro-enabled document
            DOCX – Office Open XML document
            DOT – Microsoft Word document template
            DOTX – Office Open XML text document template
            DWD – DavkaWriter Heb/Eng word processor file
            EGT – EGT Universal Document
            EPUB – EPUB open standard for e-books
            EZW – Reagency Systems easyOFFER document[7]
            FDX – Final Draft
            FTM – Fielded Text Meta
            FTX – Fielded Text (Declared)
            GDOC – Google Drive Document
            HTML, HTM – HyperText Markup Language
            HWP – Haansoft (Hancom) Hangul Word Processor document
            HWPML – Haansoft (Hancom) Hangul Word Processor Markup Language document
            LOG – Text log file
            LWP – Lotus Word Pro
            MBP – metadata for Mobipocket documents
            MD – Markdown text document
            ME – Plain text document normally preceded by the word "READ" (READ.ME)
            MCW – Microsoft Word for Macintosh (versions 4.0–5.1)
            Mobi – Mobipocket documents
            NB – Mathematica Notebook
            nb – Nota Bene Document (Academic Writing Software)
            NBP – Mathematica Player Notebook
            NEIS – 학교생활기록부 작성 프로그램 (Student Record Writing Program) Document
            NT – N-Triples RDF container (.nt)
            NQ – N-Quads RDF container (.nq)
            ODM – OpenDocument master document
            ODOC – Synology Drive Office Document
            ODT – OpenDocument text document
            OSHEET – Synology Drive Office Spreadsheet
            OTT – OpenDocument text document template
            OMM – OmmWriter text document
            PAGES – Apple Pages document
            PAP – Papyrus word processor document
            PER – Canadian Forces Personnel Appraisal System (CFPAS) Personnel Evaluation Report (PER)
            PDR – Canadian Forces Personnel Appraisal System (CFPAS) Personnel Development Report (PDR)
            PDAX – Portable Document Archive (PDA) document index file
            PDF – Portable Document Format
            QUOX – Question Object File Format for Quobject Designer or Quobject Explorer
            Radix-64 – Need helps!!!
            RTF – Rich Text document
            RPT – Crystal Reports
            SDW – StarWriter text document, used in earlier versions of StarOffice
            SE – Shuttle Document
            STW – OpenOffice.org XML (obsolete) text document template
            Sxw – OpenOffice.org XML (obsolete) text document
            TeX – TeX
            INFO – Texinfo
            Troff – Unix OS document processing system
            TXT – ASCII or Unicode plain text file
            UOF – Uniform Office Format
            UOML – Unique Object Markup Language
            VIA – Revoware VIA Document Project File
            WPD – WordPerfect document
            WPS – Microsoft Works document
            WPT – Microsoft Works document template
            WRD – WordIt! document
            WRF – ThinkFree Write
            WRI – Microsoft Write document
            xhtml, xht – XHTML eXtensible HyperText Markup Language
            XML – eXtensible Markup Language
            XPS – XPS: Open XML Paper Specification
            Financial records
            MYO – MYOB Limited (Windows) File
            MYOB – MYOB Limited (Mac) File
            TAX – TurboTax File
            YNAB – You Need a Budget (YNAB) File
            Financial data transfer formats
            IFX – Interactive Financial Exchange XML-based specification for various forms of financial transactions
            .ofx – Open Financial Exchange， open standard supported by CheckFree and Microsoft and partly by Intuit; SGML and later XML based
            QFX – proprietary pay-only format used only by Intuit
            .qif – Quicken Interchange Format open standard formerly supported by Intuit
            Font file
            ABF – Adobe Binary Screen Font
            AFM – Adobe Font Metrics
            BDF – Bitmap Distribution Format
            BMF – ByteMap Font Format
            BRFNT – Binary Revolution Font Format
            FNT – Bitmapped Font – Graphics Environment Manager (GEM)
            FON – Bitmapped Font – Microsoft Windows
            MGF – MicroGrafx Font
            OTF – OpenType Font
            PCF – Portable Compiled Format
            PFA – Printer Font ASCII
            PFB – Printer Font Binary – Adobe
            PFM – Printer Font Metrics – Adobe
            AFM – Adobe Font Metrics
            FOND – Font Description resource – Mac OS
            SFD – FontForge spline font database Font
            SNF – Server Normal Format
            TDF – TheDraw Font
            TFM – TeX font metric
            .ttf, .ttc – TrueType Font
            UFO – Unified Font Object is a cross-platform, cross-application, human readable, future proof format for storing font data.
            WOFF – Web Open Font Format
            General purpose
            These file formats allow for the rapid creation of new binary file formats.
            
            IFDS – Incredibly Flexible Data Storage file format. File extension and the magic number does not have to be IFDS.[8]
            Geographic information system
            Main article: GIS file formats
            ASC – ASCII point of interest (POI) text file
            APR – ESRI ArcView 3.3 and earlier project file
            DEM – USGS DEM file format
            E00 – ARC/INFO interchange file format
            GeoJSON – Geographically located data in object notation
            TopoJSON – Extension of GeoJSON with topology encoded in arcs for web development
            GeoTIFF – Geographically located raster data
            GML – Geography Markup Language file[9]
            GPX – XML-based interchange format
            ITN – TomTom Itinerary format
            MXD – ESRI ArcGIS project file, 8.0 and higher
            NTF – National Transfer Format file
            OV2 – TomTom POI overlay file
            SHP – ESRI shapefile
            TAB – MapInfo TAB format
            GeoTIFF – Geographically located raster data: text file giving corner coordinate, raster cells per unit, and rotation
            DTED – Digital Terrain Elevation Data
            KML – Keyhole Markup Language, XML-based
            Graphical information organizers
            3DT – 3D Topicscape, the database in which the meta-data of a 3D Topicscape is held, it is a form of 3D concept map (like a 3D mind-map) used to organize ideas, information, and computer files
            ATY – 3D Topicscape file, produced when an association type is exported; used to permit round-trip (export Topicscape, change files and folders as desired, re-import to 3D Topicscape)
            CAG (file format) – Linear Reference System
            FES (file format) – 3D Topicscape file, produced when a fileless occurrence in 3D Topicscape is exported to Windows. Used to permit round-trip (export Topicscape, change files and folders as desired, re-import them to 3D Topicscape)
            MGMF – MindGenius Mind Mapping Software file format
            MM – FreeMind mind map file (XML)
            MMP (file format) – Mind Manager mind map file
            TPC (file format) – 3D Topicscape file, produced when an inter-Topicscape topic link file is exported to Windows; used to permit round-trip (export Topicscape, change files and folders as desired, re-import to 3D Topicscape)
            Graphics
            Main articles: Image file formats and Comparison of graphics file formats
            Color palettes
            ACT – Adobe Color Table. Contains a raw color palette and consists of 256 24-bit RGB colour values.
            ASE – Adobe Swatch Exchange. Used by Adobe Substance, Photoshop, Illustrator, and InDesign.[10]
            GPL – GIMP palette file. Uses a text representation of color names and RGB values. Various open source graphical editors can read this format,[11] including GIMP, Inkscape, Krita,[12] KolourPaint, Scribus, CinePaint, and MyPaint.[13]
            PAL – Microsoft RIFF palette file
            Color management
            ICC, ICM – Color profile conforming the specification of the ICC.
            Raster graphics
            Raster or bitmap files store images as a group of pixels.
            
            ART – America Online proprietary format
            BLP – Blizzard Entertainment proprietary texture format
            BMP – Microsoft Windows Bitmap formatted image
            BTI – Nintendo proprietary texture format
            CD5 – Chasys Draw IES image
            CIT – Intergraph is a monochrome bitmap format
            CPT – Corel PHOTO-PAINT image
            CR2 – Canon camera raw format; photos have this on some Canon cameras if the quality RAW is selected in camera settings
            CLIP – CLIP STUDIO PAINT format
            CPL – Windows control panel file
            DDS – DirectX texture file
            DIB – Device-Independent Bitmap graphic
            DjVu – DjVu for scanned documents
            EGT – EGT Universal Document, used in EGT SmartSense to compress PNG files to yet a smaller file
            Exif – Exchangeable image file format (Exif) is a specification for the image format used by digital cameras
            GIF – CompuServe's Graphics Interchange Format
            GRF – Zebra Technologies proprietary format
            ICNS – format for icons in macOS. Contains bitmap images at multiple resolutions and bitdepths with alpha channel.
            ICO – a format used for icons in Microsoft Windows. Contains small bitmap images at multiple resolutions and bitdepths with 1-bit transparency or alpha channel.
            .iff, .ilbm, .lbm – IFF ILBM
            JNG – a single-frame MNG using JPEG compression and possibly an alpha channel
            JPEG, JFIF, .jpg, .jpeg – Joint Photographic Experts Group; a lossy image format widely used to display photographic images
            JP2 – JPEG2000
            JPS – JPEG Stereo
            KRA – Krita image file
            LBM – Deluxe Paint image file
            MAX – ScanSoft PaperPort document
            MIFF – ImageMagick's native file format
            MNG – Multiple-image Network Graphics, the animated version of PNG
            MSP – a format used by old versions of Microsoft Paint; replaced by BMP in Microsoft Windows 3.0
            NITF – A U.S. Government standard commonly used in Intelligence systems
            OTB – Over The Air bitmap, a specification designed by Nokia for black and white images for mobile phones
            PBM – Portable bitmap
            PC1 – Low resolution, compressed Degas picture file
            PC2 – Medium resolution, compressed Degas picture file
            PC3 – High resolution, compressed Degas picture file
            PCF – Pixel Coordination Format
            PCX – a lossless format used by ZSoft's PC Paint, popular for a time on DOS systems.
            PDN – Paint.NET image file
            PGF – Progressive Graphics File
            PGM – Portable graymap
            PI1 – Low resolution, uncompressed Degas picture file
            PI2 – Medium resolution, uncompressed Degas picture file; also Portrait Innovations encrypted image format
            PI3 – High resolution, uncompressed Degas picture file
            PICT, PCT – Apple Macintosh PICT image
            PNG – Portable Network Graphic (lossless, recommended for display and edition of graphic images)
            PNM – Portable anymap graphic bitmap image
            PNS – PNG Stereo
            PPM – Portable Pixmap (Pixel Map) image
            .procreate – Procreate (software)’s drawing file
            PSB – Adobe Photoshop Big image file (for large files)
            PSD, PDD – Adobe Photoshop Drawing
            PSP – Paint Shop Pro image
            PX – Pixel image editor image file
            PXM – Pixelmator image file
            PXR – Pixar Image Computer image file
            QFX – QuickLink Fax image
            RAW – General term for minimally processed image data (acquired by a digital camera)
            RLE – a run-length encoding image
            SCT – Scitex Continuous Tone image file
            SGI, RGB, INT, BW – Silicon Graphics Image
            TGA, .tga, .targa, .icb, .vda, .vst, .pix – Truevision TGA (Targa) image
            TIFF, .tif, .tiff – Tag(ged) Image File Format; usually lossless, but many variants exist, including lossy ones.
            TIFF/EP, .tif, .tiff – Tag Image File Format / Electronic Photography, ISO 12234-2; tends to be used as a basis for other formats rather than in its own right.
            VTF – Valve Texture Format
            XBM – X Window System Bitmap
            XCF – GIMP image (from Gimp's origin at the eXperimental Computing Facility of the University of California)
            XPM – X Window System Pixmap
            ZIF – Zoomable/Zoomify Image Format (a web-friendly, TIFF-based, zoomable image format)
            
            Vector graphics
            Vector graphics use geometric primitives such as points, lines, curves, and polygons to represent images.
            
            3DV file – 3-D wireframe graphics by Oscar Garcia
            AMF – Additive Manufacturing File Format
            AWG – Ability Draw
            AI – Adobe Illustrator Document
            CGM – Computer Graphics Metafile, an ISO Standard
            CDR – CorelDRAW Document
            CMX – CorelDRAW vector image
            DP – Drawing Program file for PERQ[14]
            DRAWIO – Diagrams.net offline diagram
            DXF – ASCII Drawing Interchange file Format, used in AutoCAD and other CAD-programs
            E2D – 2-dimensional vector graphics used by the editor which is included in JFire
            EGT – EGT Universal Document, EGT Vector Draw images are used to draw vector to a website
            EPS – Encapsulated Postscript
            FS – FlexiPro file
            GBR – Gerber file
            ODG – OpenDocument Drawing
            MOVIE.BYU – 3D Vector file for polygons, coordinates and more complex shapes
            RenderMan – Displays Shading in both 2D and 3D scapes
            SVG – Scalable Vector Graphics, employs XML
            3DMLW – Scene description languages (3D vector image formats)
            STL – STL: Stereo Lithographic data format (see STL (file format)) used by various CAD systems and stereo lithographic printing machines. See above.
            .wrl – Virtual Reality Modeling Language, VRML Uses this extension for the creation of 3D viewable web images.
            X3D – XML based file for communicating 3D graphics
            SXD – OpenOffice.org XML (obsolete) Drawing
            TGAX – Texture format used by Zwift
            V2D – voucher design used by the voucher management included in JFire
            VDOC – Vector format used in AnyCut, CutStorm, DrawCut, DragonCut, FutureDRAW, MasterCut, SignMaster, VinylMaster software by Future Corporation
            VSD – Vector format used by Microsoft Visio
            VSDX – Vector format used by MS Visio and opened by VSDX Annotator
            VND – Vision numeric Drawing file used in TypeEdit, Gravostyle.
            WMF – WMF: Windows Meta File
            EMF – EMF: Enhanced (Windows) MetaFile, an extension to WMF
            ART – Xara–Drawing (superseded by XAR)
            XAR – Xara–Drawing
            3D graphics
            See also: 3D file format at EduTech Wiki
            3D graphics are 3D models that allow building models in real-time or non-real-time 3D rendering.
            
            3DMF – QuickDraw 3D Metafile (.3dmf)
            3DM – OpenNURBS Initiative 3D Model (used by Rhinoceros 3D) (.3dm)
            3MF – Microsoft 3D Manufacturing Format (.3mf)[4]
            3DS – legacy 3D Studio Model (.3ds)
            ABC – Alembic (computer graphics)
            AC – AC3D Model (.ac)
            AMF – Additive Manufacturing File Format
            AN8 – Anim8or Model (.an8)
            AOI – Art of Illusion Model (.aoi)
            ASM – PTC Creo assembly (.asm)
            B3D – Blitz3D Model (.b3d)
            BLEND – Blender (.blend)
            BLOCK – Blender encrypted blend files (.block)
            BMD3 – Nintendo GameCube first-party J3D proprietary model format (.bmd)
            BDL4 – Nintendo GameCube and Wii first-party J3D proprietary model format (2002, 2006–2010) (.bdl)
            BRRES – Nintendo Wii first-party proprietary model format 2010+ (.brres)
            BFRES – Nintendo Wii U and later Switch first-party proprietary model format
            C4D – Cinema 4D (.c4d)
            Cal3D – Cal3D (.cal3d)
            CCP4 – X-ray crystallography voxels (electron density)
            CFL – Compressed File Library (.cfl)
            COB – Caligari Object (.cob)
            CORE3D – Coreona 3D Coreona 3D Virtual File(.core3d)
            CTM – OpenCTM (.ctm)
            DAE – COLLADA (.dae)
            DFF – RenderWare binary stream, commonly used by Grand Theft Auto III-era games as well as other RenderWare titles
            DPM – DeepMesh (.dpm)
            DTS – Torque Game Engine (DTS (file format))
            EGG – Panda3D Engine
            FACT – Electric Image (.fac)
            FBX – Autodesk FBX (.fbx)
            G – BRL-CAD geometry (.g)
            GLB – a binary form of glTF required to be loaded in Facebook 3D Posts. (.glb)
            GLM – Ghoul Mesh (.glm)
            glTF – the JSON-based standard developed by Khronos Group (.gltf)
            .hec – Hector Game Engine – Flatspace model format
            IO – Bricklink Stud.io 2.0 Model File (.io)
            IOB – Imagine (3D modeling software) (.iob)
            JAS – Cheetah 3D file (.jas)
            JMESH – Universal mesh data exchange file based on JMesh specification (.jmsh for text/JSON based, .bmsh for binary/UBJSON based)
            LDR – LDraw Model File (.ldr)
            LWO – Lightwave Object (.lwo)
            LWS – Lightwave Scene (.lws)
            LXF – LEGO Digital Designer Model file (.lxf)
            LXO – Luxology Modo (software) file (.lxo)
            M3D – Model3D, universal, engine-neutral format (.m3d)
            MA – Autodesk Maya ASCII File (.ma)
            MAX – Autodesk 3D Studio Max file (.max)
            MB – Autodesk Maya Binary File (.mb)
            MPD – LDraw Multi-Part Document Model File (.mpd)
            MD2 – MD2: Quake 2 model format (.md2)
            MD3 – MD3: Quake 3 model format (.md3)
            MD5 – MD5: Doom 3 model format (.md5)
            MDX – Blizzard Entertainment's own model format (.mdx)
            MESH – New York University(.m)
            MESH – Meshwork Model (.mesh)
            MIOBJECT – Mine-Imator object file (.miobject)
            MIPARTICLE – Mine-Imator particle file (.miparticle)
            MIMODEL – Mine-Imator model file (.mimodel)
            MM3D – Misfit Model 3d (.mm3d)
            MPO – Multi-Picture Object – This JPEG standard is used for 3d images, as with the Nintendo 3DS
            MRC – MRC: voxels in cryo-electron microscopy
            NIF – Gamebryo NetImmerse File (.nif)
            OBJ – Wavefront .obj file (.obj)
            OFF – OFF Object file format (.off)
            OGEX – Open Game Engine Exchange (OpenGEX) format (.ogex)
            PLY – PLY: Polygon File Format / Stanford Triangle Format (.ply)
            PRC – Adobe PRC (embedded in PDF files)
            PRT – PTC Creo part (.prt)
            POV – POV-Ray document (.pov)
            R3D – Realsoft 3D (Real-3D) (.r3d)
            RWX – RenderWare Object (.rwx)
            SIA – Nevercenter Silo Object (.sia)
            SIB – Nevercenter Silo Object (.sib)
            SKP – Google Sketchup file (.skp)
            SLDASM – SolidWorks Assembly Document (.sldasm)
            SLDPRT – SolidWorks Part Document (.sldprt)
            SMD – Valve Studiomdl Data format (.smd)
            U3D – Universal 3D format (.u3d)
            USD – Universal Scene Description (.usd)
            USDA – Universal Scene Description, human-readable text format (.usda)
            USDC – Universal Scene Description, binary format (.usdc)
            USDZ – Universal Scene Description, a zip-compressed container (.usdz)
            VIM – Revizto visual information model format (.vimproj)
            VRML97 – VRML Virtual reality modeling language (.wrl)
            VUE – Vue scene file (.vue)
            VWX – Vectorworks (.vwx)
            WINGS – Wings3D (.wings)
            W3D – Westwood 3D Model (.w3d)
            X – DirectX 3D Model (.x)
            X3D – Extensible 3D (.x3d)
            Z3D – Zmodeler (.z3d)
            ZBMX – Mecabricks Blender Add-On (.zbmx)
            Links and shortcuts
            Alias – Alias (Mac OS)
            JNLP – Java Network Launching Protocol, an XML file used by Java Web Start for starting Java applets over the Internet
            LNK – binary-format file shortcut in Microsoft Windows 95 and later
            APPREF-MS – File shortcut format used by ClickOnce
            NAL – ZENworks Instant shortcut (opens a .EXE not on the C:/ )
            URL – INI file pointing to a URL bookmarks/Internet shortcut in Microsoft Windows
            WEBLOC – Property list file pointing to a URL bookmarks/Internet shortcut in macOS
            SYM – Symbolic link
            .desktop – Desktop entry on Linux Desktop environments
            Mathematical
            Harwell-Boeing – a file format designed to store sparse matrices
            MML – MathML – Mathematical Markup Language
            ODF – OpenDocument Math Formula
            SXM – OpenOffice.org XML (obsolete) Math Formula
            Object code, executable files, shared and dynamically linked libraries
            8BF – files plugins for some photo editing programs including Adobe Photoshop, Paint Shop Pro, GIMP and Helicon Filter.
            .a – a static library on Unix-like systems
            .a – Objective C native static library
            a.out – (no suffix for executable image, .o for object files, .so for shared object files) classic UNIX object format, now often superseded by ELF
            APK – Android Application Package
            APP – A folder found on macOS systems containing program code and resources, appearing as one file.
            .app, APP – file extension are executable application packages for running apps on HarmonyOS, OpenHarmony and HarmonyOS NEXT devices.
            BAC – an executable image for the RSTS/E system, created using the BASIC-PLUS COMPILE command[15]
            BPL – a Win32 PE file created with Borland Delphi or C++Builder containing a package.
            Bundle – a Macintosh plugin created with Xcode or make which holds executable code, data files, and folders for that code.
            .class – Compiled Java bytecode
            COFF – (no suffix for executable image, .o for object files) UNIX Common Object File Format, now often superseded by ELF
            COM – Simple executable format used by CP/M and DOS.
            DCU – Delphi compiled unit
            DLL – Dynamic library used in Windows and OS/2 to store data, resources and code.
            DOL – the format used by the GameCube and Wii, short for Dolphin, which was the codename of the GameCube.
            .EAR – archives of Java enterprise applications
            ELF – (no suffix for executable image, .o for object files, .so for shared object files) used in many modern Unix and Unix-like systems, including Solaris, other System V Release 4 derivatives, Linux, and BSD)
            .exe – DOS executable (.exe: used in DOS)
            .EXE – New Executable (used in multitasking ("European") MS-DOS 4.0, 16-bit Microsoft Windows, and OS/2)
            .EXE – Portable Executable used in Microsoft Windows and some other systems
            .ipa, .IPA – file extension for apple IOS application executable file. Another form of zip file.
            .JAR – archives of Java class files
            JEFF – a file format allowing execution directly from static memory[16]
            .ko – Loadable kernel module
            LIB – a static library on Microsoft platforms
            LIST – variable list
            Mach-O – (no suffix for executable image, .o for object files, .dylib and .bundle for shared object files) Mach-based systems, notably native format of macOS, iOS, watchOS, and tvOS
            .NLM – NetWare Loadable Module the native 32-bit binaries compiled for Novell's NetWare Operating System (versions 3 and newer)
            .o – un-linked object files directly from the compiler
            OBJ – object file on Windows
            RLL – used in Microsoft operating systems together with a DLL file to store program resources
            .s1es – Executable used for S1ES learning system.
            .so – shared library, typically ELF
            .VAP – Value Added Process the native 16-bit binaries compiled for Novell's NetWare Operating System (version 2, NetWare 286, Advanced NetWare, etc.)
            WAR, .WAR – .WAR are archives of Java Web applications
            .XAP – Windows Phone package
            XBE – XBE is Xbox executable
            XCOFF – (no suffix for executable image, .o for object files, .a for shared object files) extended COFF, used in AIX
            XEX – XEX is Xbox 360 executable
            .XPI – PKZIP archive that can be run by Mozilla web browsers to install software.
            Object extensions:
            
            .OCX – .OCX are Object Control extensions
            .TLB – .TLB are Windows Type Library
            .VBX – .VBX are Visual Basic extensions
            Page description language
            For a more comprehensive list, see List of page description languages.
            DVI – DVI are Device independent format
            .egt – Universal Document can be used to store CSS type styles
            PLD – PLD (Need to be added!!!)
            PCL – PCL (Need to be added!!!)
            PDF – PDF are Portable Document Format
            .ps, .ps, .gz – PostScript (Need to be added!!!)
            SNP – SNP are Microsoft Access Report Snapshot
            XPS – XPS
            XSL-FO – XSL-FO (Formatting Objects)
            Configurations, Metadata
            CSS – CSS are Cascading Style Sheets
            .xslt, .xsl – XML Style Sheet
            .tpl – Web template
            Personal information manager
            Main article: Personal information manager
            MNB – MyInfo notebook
            MSG – Microsoft Outlook task manager
            ORG – Lotus Organizer PIM package
            ORG – Emacs Org-Mode Mindmanager, contacts, calendar, email-integration
            PST, OST – Microsoft Outlook email communication
            SC2 – Microsoft Schedule+ calendar
            Presentation
            GSLIDES – Google Drive Presentation
            KEY, KEYNOTE – Apple Keynote Presentation
            NB – Mathematica Slideshow
            NBP – Mathematica Player slideshow
            ODP – OpenDocument Presentation
            OTP – OpenDocument Presentation template
            PEZ – Prezi Desktop Presentation
            POT – Microsoft PowerPoint template
            PPS – Microsoft PowerPoint Show
            PPT – Microsoft PowerPoint Presentation
            PPTX – Office Open XML Presentation
            PRZ – Lotus Freelance Graphics
            SDD – StarOffice's StarImpress
            SHF – ThinkFree Show
            SHOW – Haansoft(Hancom) Presentation software document
            SHW – Corel Presentations slide show creation
            SLP – Logix-4D Manager Show Control Project
            SSPSS – SongShow Plus Slide Show
            STI – OpenOffice.org XML (obsolete) Presentation template
            SXI – OpenOffice.org XML (obsolete) Presentation
            THMX – Microsoft PowerPoint theme template
            WATCH – Dataton Watchout Presentation
            Project management software
            Main article: Project management software
            MPP – Microsoft Project
            Reference management software
            Main article: Reference management software
            Formats of files used for bibliographic information (citation) management.
            
            bib – BibTeX
            enl – EndNote
            ris – Research Information Systems RIS (file format)
            Scientific data (data exchange)
            .fits – FITS (Flexible Image Transport System) standard data format for astronomy
            Silo – Silo, a storage format for visualization developed at Lawrence Livermore National Laboratory
            SPC – SPC, spectroscopic data
            EAS3 – binary format for structured data
            EOSSA – Electro-Optic Space Situational Awareness format
            OST – (Open Spatio-Temporal) extensible, mainly images with related data, or just pure data; meant as an open alternative for microscope images
            CCP4 – CCP4, X-ray crystallography voxels (electron density)
            MRC – MRC, voxels in cryo-electron microscopy
            HITRAN – spectroscopic data with one optical/infrared transition per line in the ASCII file (.hit)
            .root – hierarchical platform-independent compressed binary format used by ROOT
            SDF – Simple Data Format (SDF), a platform-independent, precision-preserving binary data I/O format capable of handling large, multi-dimensional arrays.
            MYD – Everfine LEDSpec software file for LED measurements
            CSDM – (Core Scientific Dataset Model) model for multi-dimensional and correlated datasets from various spectroscopies, diffraction, microscopy, and imaging techniques (.csdf, .csdfe).[17]
            Multi-domain
            NetCDF – Network common data format
            HDR, HDF, h4, h5 – Hierarchical Data Format
            SDXF – SDXF, (Structured Data Exchange Format)
            CDF – Common Data Format
            CGNS – CGNS, CFD General Notation System
            FMF – Full-Metadata Format
            Meteorology
            GRIB – Grid in Binary, WMO format for weather model data
            BUFR – WMO format for weather observation data
            PP – UK Met Office format for weather model data
            NASA-Ames – Simple text format for observation data. First used in aircraft studies of the atmosphere.
            Chemistry
            Main article: chemical file format
            CML – Chemical Markup Language (CML) (.cml)
            .mol, .sd, .sdf – Chemical table file (CTab)
            .dx, .jdx – Joint Committee on Atomic and Molecular Physical Data (JCAMP)
            .smi – Simplified molecular input line entry specification (SMILES)
            Mathematics
            .g6, .s6 – graph6, sparse6, ASCII encoding of Adjacency matrices
            Biology
            Molecular biology and bioinformatics:
            
            AB1 – In DNA sequencing, chromatogram files used by instruments from Applied Biosystems
            ACE – A sequence assembly format
            ASN.1 – Abstract Syntax Notation One, is an International Standards Organization (ISO) data representation format used to achieve interoperability between platforms. NCBI uses ASN.1 for the storage and retrieval of data such as nucleotide and protein sequences, structures, genomes, and PubMed records.
            BAM – Binary Alignment/Map format (compressed SAM format)
            BCF – Binary compressed VCF format
            BED – The browser extensible display format is used for describing genes and other features of DNA sequences
            CAF – Common Assembly Format for sequence assembly
            CRAM – compressed file format for storing biological sequences aligned to a reference sequence
            DDBJ – The flatfile format used by the DDBJ to represent database records for nucleotide and peptide sequences from DDBJ databases.
            EMBL – The flatfile format used by the EMBL to represent database records for nucleotide and peptide sequences from EMBL databases.
            FASTA – The FASTA format, for sequence data. Sometimes also given as FNA or FAA (Fasta Nucleic Acid or Fasta Amino Acid).
            FASTQ – The FASTQ format, for sequence data with quality. Sometimes also given as QUAL.
            GCPROJ – The Genome Compiler project. Advanced format for genetic data to be designed, shared and visualized.
            GenBank – The flatfile format used by the NCBI to represent database records for nucleotide and peptide sequences from the GenBank and RefSeq databases
            GFF – The General feature format is used to describe genes and other features of DNA, RNA, and protein sequences
            GTF – The Gene transfer format is used to hold information about gene structure
            MAF – The Multiple Alignment Format stores multiple alignments for whole-genome to whole-genome comparisons [1]
            NCBI – Structured ASN.1 format used at National Center for Biotechnology Information for DNA and protein data
            NEXUS – The Nexus file encodes mixed information about genetic sequence data in a block structured format
            NeXML – XML format for phylogenetic trees
            NWK – The Newick tree format is a way of representing graph-theoretical trees with edge lengths using parentheses and commas and useful to hold phylogenetic trees.
            PDB – structures of biomolecules deposited in Protein Data Bank, also used to exchange protein and nucleic acid structures
            PHD – Phred output, from the base-calling software Phred
            PLN – Protein Line Notation used in proteax software specification
            SAM – SAM, Sequence Alignment Map format, in which the results of the 1000 Genomes Project will be released
            SBML – The Systems Biology Markup Language is used to store biochemical network computational models
            SCF – Staden chromatogram files used to store data from DNA sequencing
            SFF – Standard Flowgram Format
            SRA – format used by the National Center for Biotechnology Information Short Read Archive to store high-throughput DNA sequence data
            Stockholm – The Stockholm format for representing multiple sequence alignments
            Swiss-Prot – The flatfile format used to represent database records for protein sequences from the Swiss-Prot database
            VCF – Variant Call Format, a standard created by the 1000 Genomes Project that lists and annotates the entire collection of human variants (with the exception of approximately 1.6 million variants).
            Biomedical imaging
            .dcm – Digital Imaging and Communications in Medicine (DICOM)
            NIfTI – Neuroimaging Informatics Technology Initiative
            .nii – single-file (combined data and meta-data) style
            .nii.gz – gzip-compressed, used transparently by some software, notably the FMRIB Software Library (FSL)
            .gii – single-file (combined data and meta-data) style; NIfTI offspring for brain surface data
            .img, .hdr – dual-file (separate data and meta-data, respectively) style
            .BRIK, .HEAD – AFNI data, meta-data
            .MGH – uncompressed, Massachusetts General Hospital imaging format, used by the FreeSurfer brain analysis package
            .MGZ – zip-compressed, Massachusetts General Hospital imaging format, used by the FreeSurfer brain analysis package
            .img, .hdr – Analyze data, meta-data
            MINC – Medical Imaging NetCDF format
            .mnc – previously based on NetCDF; since version 2.0, based on HDF5
            Biomedical signals (time series)
            ACQ – AcqKnowledge format for Windows/PC from Biopac Systems Inc., Goleta, CA, USA
            ADICHT – LabChart format from ADInstruments Pty Ltd, Bella Vista NSW, Australia
            BCI2000 – The BCI2000 project, Albany, NY, USA
            BDF – BioSemi data format from BioSemi B.V. Amsterdam, Netherlands
            BKR – The EEG data format developed at the University of Technology Graz, Austria
            CFWB – Chart Data Format from ADInstruments Pty Ltd, Bella Vista NSW, Australia
            DICOM – Waveform An extension of Dicom for storing waveform data
            ecgML – A markup language for electrocardiogram data acquisition and analysis
            EDF, EDF+ – European Data Format
            FEF – File Exchange Format for Vital signs, CEN TS 14271
            GDF – The General Data Format for biomedical signals
            HL7aECG – Health Level 7 v3 annotated ECG
            MFER – Medical waveform Format Encoding Rules
            OpenXDF – Open Exchange Data Format from Neurotronics, Inc., Gainesville, FL, USA
            SCP-ECG – Standard Communication Protocol for Computer assisted electrocardiography EN1064:2007
            SIGIF – A digital SIGnal Interchange Format with application in neurophysiology
            WFDB – Format of Physiobank
            XDF – eXtensible Data Format
            Other biomedical formats
            HL7 – Health Level 7, a framework for exchange, integration, sharing, and retrieval of health information electronically
            xDT – a family of data exchange formats for medical records
            Biometric formats
            CBF – Common Biometric Format, based on CBEFF 2.0 (Common Biometric ExFramework).
            EBF – Extended Biometric Format, based on CBF but with S/MIME encryption support and semantic extensions
            CBFX – XML Common Biometric Format, based upon XCBF 1.1 (OASIS XML Common Biometric Format)
            EBFX – XML Extended Biometric Format, based on CBFX but with W3C XML Encryption support and semantic extensions
            Programming languages and scripts
            ADB – Ada body
            ADS – Ada specification
            AHK – AutoHotkey script file
            APPLESCRIPT – applescript: see SCPT
            AS – Adobe Flash ActionScript File
            AU3 – AutoIt version 3
            AWK – AWK
            BAT – Batch file
            BAS – QBasic & QuickBASIC
            BTM – Batch file
            CLASS – Compiled Java binary
            CLJS – ClojureScript
            CMD – Batch file
            Coffee – CoffeeScript
            C – C
            CIA – Nintendo 3DS Software Installation File, short for "CTR Importable Archive"
            CPP – C++
            CS – C#
            FS – F#
            EGG – Chicken
            EGT – EGT Asterisk Application Source File, EGT Universal Document
            ERB – Embedded Ruby, Ruby on Rails Script File
            GO – Go
            HTA – HTML Application
            IBI – Icarus script
            ICI – ICI
            IJS – J script
            INO – Arduino sketch (program)
            .ipynb – IPython Notebook
            ITCL – Itcl
            JS – JavaScript and JScript
            JSFL – Adobe JavaScript language
            .kt – Kotlin
            LUA – Lua
            M – Mathematica package file
            MRC – mIRC Script
            NCF – NetWare Command File[18][19] (scripting for Novell's NetWare OS)
            NUC – compiled script
            NUD – C++ External module written in C++
            NUT – Squirrel
            nqp – Raku language Not Quite Perl, or Raku bootstrapping language[20]
            O – Compiled and optimized C/C++ binary
            pde – Processing (programming language), Processing script
            PHP – PHP
            PHP? – PHP (? = version number)
            PL – Perl
            PM – Perl module
            PS1 – Windows PowerShell shell script
            PS1XML – Windows PowerShell format and type definitions
            PSC1 – Windows PowerShell console file
            PSD1 – Windows PowerShell data file
            PSM1 – Windows PowerShell module file
            PY – Python
            PYC – Python byte code files
            PYO – Python
            R – R scripts
            r – REBOL scripts
            raku – Raku language Raku script (compiled into memory)[20]
            rakumod – Raku language Raku module (precompiled)
            rakudoc – Raku language Raku documentation file (a slang or sublanguage of Raku)
            rakutest – Raku language Unit test files in Raku
            RB – Ruby
            RDP – RDP connection
            red – Red scripts
            RS – Rust (programming language)
            SB2, SB3 – Scratch
            SCPT – Applescript
            SCPTD – See SCPT.
            SDL – State Description Language
            SH – Shell script
            SPRITE3 – Scratch 3.0 exported sprite file
            SPWN – SPWN source file
            SYJS – SyMAT JavaScript
            SYPY – SyMAT Python
            TCL – Tcl
            TNS – Ti-Nspire Code/File
            TS – TypeScript
            VBS – Visual Basic Script
            XPL – XProc script/pipeline
            ebuild – Gentoo Linux's portage package.
            Security
            Authentication and general encryption formats are listed here.
            
            OMF – OpenPGP Message Format used by Pretty Good Privacy, GNU Privacy Guard, and other OpenPGP software; can contain keys, signed data, or encrypted data; can be binary or text ("ASCII armored")
            Certificates and keys
            GXK – Galaxkey, an encryption platform for authorized, private and confidential email communication[citation needed]
            .ssh – OpenSSH private key, Secure Shell private key; format generated by ssh-keygen or converted from PPK with PuTTYgen[21][22][23]
            .pub – OpenSSH public key, Secure Shell public key; format generated by ssh-keygen or PuTTYgen[21][22][23]
            .ppk – PuTTY private key, Secure Shell private key, in the format generated by PuTTYgen instead of the format used by OpenSSH[21][22][23]
            .nSign – nSign public key nSign public key in a custom format[24]
            X.509
            .cer, .crt, .der – Distinguished Encoding Rules stores certificates
            .p7b, .p7c – PKCS#7 SignedData commonly appears without main data, just certificates or certificate revocation lists (CRLs)
            .p12, .pfx – PKCS#12 can store public certificates and private keys
            PEM – Privacy-enhanced Electronic Mail: full format not widely used, but often used to store Distinguished Encoding Rules in Base64 format
            PFX – Microsoft predecessor of PKCS#12
            Encrypted files
            This section shows file formats for encrypted general data, rather than a specific program's data.
            
            AXX – Encrypted file, created with AxCrypt
            EEA – An encrypted CAB, ostensibly for protecting email attachments
            TC – Virtual encrypted disk container, created by TrueCrypt
            KODE – Encrypted file, created with KodeFile
            nSignE – An encrypted private key, created by nSign[24]
            Password files
            Password files (sometimes called keychain files) contain lists of other passwords, usually encrypted.
            
            BPW – Encrypted password file created by Bitser password manager
            KDB – KeePass 1 database
            KDBX – KeePass 2 database
            Signal data (non-audio)
            ACQ – AcqKnowledge format for Windows/PC from Biopac
            ADICHT – LabChart format from ADInstruments
            BKR – The EEG data format developed at the University of Technology Graz
            BDF, CFG – Configuration file for Comtrade data
            CFWB – Chart Data format from ADInstruments
            DAT – Raw data file for Comtrade data
            EDF – European data format
            FEF – File Exchange Format for Vital signs
            GDF – General data formats for biomedical signals
            GMS – Gesture And Motion Signal format
            IROCK – intelliRock Sensor Data File Format
            MFER – Medical waveform Format Encoding Rules
            SAC – Seismic Analysis Code, earthquake seismology data format[25]
            SCP-ECG – Standard Communication Protocol for Computer assisted electrocardiography
            SEED, MSEED – Standard for the Exchange of Earthquake Data, seismological data and sensor metadata[26]
            SEGY – Reflection seismology data format
            SIGIF – SIGnal Interchange Format
            WIN, WIN32 – NIED/ERI seismic data format (.cnt)[27]
            Sound and music
            See also: List of audio file formats
            Lossless audio
            Uncompressed
            8SVX – Commodore-Amiga 8-bit sound (usually in an IFF container)
            16SVX – Commodore-Amiga 16-bit sound (usually in an IFF container)
            AIFF, AIF, AIFC – Audio Interchange File Format
            AU – Simple audio file format introduced by Sun Microsystems
            AUP3 – Audacity’s file for when you save a song
            BWF – Broadcast Wave Format, an extension of WAVE
            CDDA – Compact Disc Digital Audio
            DSF, DFF – Direct Stream Digital audio file, also used in Super Audio CD
            RAW – Raw samples without any header or sync
            WAV – Microsoft Wave
            CWAV – file read by the Nintendo 3DS for Home-screen sound effects
            Compressed
            RA, RM – RealAudio format
            FLAC – Free lossless codec of the Ogg project
            LA – Lossless audio
            PAC – LPAC
            APE – Monkey's Audio
            OFR, OFS, OFF – OptimFROG
            RKA – RKAU
            SHN – Shorten
            TAK – Tom's Lossless Audio Kompressor[28]
            THD – Dolby TrueHD
            TTA – Free lossless audio codec (True Audio)
            WV – WavPack
            WMA – Windows Media Audio 9 Lossless
            BCWAV – Nintendo 3DS Home-screen BGM file
            BRSTM – Binary Revolution Stream[29]
            DTS, DTSHD, DTSMA – DTS (sound system)
            AST – Nintendo Audio Stream
            AW – Nintendo Audio Sample used in first-party games
            PSF – Portable Sound Format, PlayStation variant (originally PlayStation Sound Format)
            Lossy audio
            AC3 – Usually used for Dolby Digital tracks
            AMR – For GSM and UMTS based mobile phones
            MP1 – MPEG Layer 1
            MP2 – MPEG Layer 2
            MP3 – MPEG Layer 3
            SPX – Speex (Ogg project, specialized for voice, low bitrates)
            GSM – GSM Full Rate, originally developed for use in mobile phones
            WMA – Windows Media Audio
            AAC – Advanced Audio Coding (usually in an MPEG-4 container)
            MPC – Musepack
            VQF – Yamaha TwinVQ
            OTS – Audio File (similar to MP3, with more data stored in the file and slightly better compression; designed for use with OtsLabs' OtsAV)
            SWA – Adobe Shockwave Audio (Same compression as MP3 with additional header information specific to Adobe Director)
            VOX – Dialogic ADPCM Low Sample Rate Digitized Voice
            VOC – Creative Labs Soundblaster Creative Voice 8-bit & 16-bit Also output format of RCA Audio Recorders
            DWD – DiamondWare Digitized
            SMP – Turtlebeach SampleVision
            OGG – Ogg Vorbis
            Tracker modules and related
            MOD – Soundtracker and Protracker sample and melody modules
            MT2 – MadTracker 2 module
            S3M – Scream Tracker 3 module
            XM – Fast Tracker module
            IT – Impulse Tracker module
            NSF – NES Sound Format
            MID, MIDI – Standard MIDI file; most often just notes and controls but occasionally also sample dumps (.mid, .rmi)
            FTM – FamiTracker Project file
            BTM – BambooTracker Project file
            Sheet music files
            ABC – ABC Notation sheet music file
            DARMS – DARMS File Format also known as the Ford-Columbia Format
            ETF – Enigma Transportation Format abandoned sheet music exchange format
            GP – Guitar Pro sheet music and tablature file
            KERN – Kern File Format sheet music file
            LY – LilyPond sheet music file
            MEI – Music Encoding Initiative file format that attempts to encode all musical notations
            MIDI – MIDI file format that is a music sheet for instruments
            MUS, MUSX – Finale sheet music file
            MXL, XML – MusicXML standard sheet music exchange format
            MSCX, MSCZ – MuseScore sheet music file
            SMDL – Standard Music Description Language sheet music file
            SIB – Sibelius sheet music file
            Other file formats pertaining to audio
            NIFF – Notation Interchange File Format
            PTB – Power Tab Editor tab
            ASF – Advanced Systems Format
            CUST – DeliPlayer custom sound format
            GYM – Genesis YM2612 log
            JAM – Jam music format
            MNG – Background music for the Creatures game series, starting from Creatures 2
            RMJ – RealJukebox Media used for RealPlayer
            SID – Sound Interface Device – Commodore 64 instructions to play SID music and sound effects
            SPC – Super NES sound format
            TXM – Track ax media
            VGM – Stands for "Video Game Music", log for several different chips
            YM – Atari ST/Amstrad CPC YM2149 sound chip format
            PVD – Portable Voice Document used for Oaisys & Mitel call recordings
            Playlist formats
            AIMPPL – AIMP Playlist format
            ASX – Advanced Stream Redirector
            RAM – Real Audio Metafile For RealAudio files only.
            XPL – HDi playlist
            XSPF – XML Shareable Playlist Format
            ZPL – Xbox Music (Formerly Zune) Playlist format from Microsoft
            M3U – Multimedia playlist file
            PLS – Multimedia playlist, originally developed for use with the museArc
            Audio editing and music production
            ALS – Ableton Live set
            ALC – Ableton Live clip
            ALP – Ableton Live pack
            ATMOS, AUDIO, METADATA – Dolby Atmos Rendering and Mastering related file
            AUP – Audacity project file
            AUP3 – Audacity 3.0 project file
            BAND – GarageBand project file
            CEL – Adobe Audition loop file (Cool Edit Loop)
            CAU – Caustic project file
            CPR – Steinberg Cubase project file
            CWP – Cakewalk Sonar project file
            DRM – Steinberg Cubase drum file
            DWP – DirectWave Sampler Instrument file (mainly used for FL Studio Mobile)
            DMKIT – Image-Line's Drumaxx drum kit file
            ENS – Native Instruments Reaktor Ensemble
            FLM – Image Line FL Studio Mobile project file
            FLP – Image Line FL Studio project file
            GRIR – Native Instruments Komplete Guitar Rig Impulse Response
            LOGIC – Logic Pro X project file
            MMP – LMMS project file (alternatively MMPZ for compressed formats)
            MMR – MAGIX Music Maker project file
            MX6HS – Mixcraft 6 Home Studio project file
            NPR – Steinberg Nuendo project file
            OMF, OMFI – Open Media Framework Interchange OMFI succeeds OMF (Open Media Framework)
            PTX – Pro Tools 10 or later project file
            PTF – Pro Tools 7 up to Pro Tools 9 project file
            PTS – Legacy Pro Tools project file
            RIN – Soundways RIN-M file containing sound recording participant credits and song information
            RPP, RPP-BAK – REAPER project file
            REAPEAKS – REAPER peak (waveform cache) file
            SES – Adobe Audition multitrack session file
            SFK – Sound Forge waveform cache file
            SFL – Sound Forge sound file
            SNG – MIDI sequence file (MidiSoft, Korg, etc.) or n-Track Studio project file
            STF – StudioFactory project file. It contains all necessary patches, samples, tracks and settings to play the file
            SND – Akai MPC sound file
            SYN – SynFactory project file. It contains all necessary patches, samples, tracks and settings to play the file
            UST – Utau Editor sequence excluding wave-file
            VCLS – VocaListener project file
            VPR – Vocaloid 5 Editor sequence excluding wave-file
            VSQ – Vocaloid 2 Editor sequence excluding wave-file
            VSQX – Vocaloid 3 & 4 Editor sequence excluding wave-file
            Recorded television formats
            DVR-MS – Windows XP Media Center Edition's Windows Media Center recorded television format
            WTV – Windows Vista's and up Windows Media Center recorded television format
            Source code for computer programs
            ADA, ADB, 2.ADA – Ada (body) source
            ADS, 1.ADA – Ada (specification) source
            ASM, S – Assembly language source
            BAS – BASIC, FreeBASIC, Visual Basic, BASIC-PLUS source,[15] PICAXE basic
            BB – Blitz Basic Blitz3D
            BMX – Blitz Basic BlitzMax
            C – C source
            CLJ – Clojure source code
            CLS – Visual Basic class
            COB, CBL – COBOL source
            CPP, CC, CXX, C, CBP – C++ source
            CS – C# source
            CSPROJ – C# project (Visual Studio .NET)
            D – D source
            DBA – DarkBASIC source
            DBPro123 – DarkBASIC Professional project
            E – Eiffel source
            EFS – EGT Forever Source File
            EGT – EGT Asterisk Source File, could be J, C#, VB.net, EF 2.0 (EGT Forever)
            EL – Emacs Lisp source
            FOR, FTN, F, F77, F90 – Fortran source
            FRM – Visual Basic form
            FRX – Visual Basic form stash file (binary form file)
            FTH – Forth source
            GED – Game Maker Extension Editable file as of version 7.0
            GM6 – Game Maker Editable file as of version 6.x
            GMD – Game Maker Editable file up to version 5.x
            GMK – Game Maker Editable file as of version 7.0
            GML – Game Maker Language script file
            GO – Go source
            H – C/C++ header file
            HPP, HXX – C++ header file
            HS – Haskell source
            HX – Haxe source
            I – SWIG interface file
            INC – Turbo Pascal included source
            JAVA – Java source
            L – lex source
            LGT – Logtalk source
            LISP – Common Lisp source
            M – Objective-C source
            M – MATLAB
            M – Mathematica
            M4 – m4 source
            ML – Standard ML and OCaml source
            MSQR – M² source file, created by Mattia Marziali
            N – Nemerle source
            NB – Nuclear Basic source
            P – Parser source
            PAS, PP, P – Pascal source (DPR for projects)
            PHP, PHP3, PHP4, PHP5, PHPS, Phtml – PHP source
            PIV – Pivot stickfigure animator
            PL, PM – Perl
            PLI, PL1 – PL/I
            PRG – Ashton-Tate; dbII, dbIII and dbIV, db, db7, clipper, Microsoft Fox and FoxPro, harbour, xharbour, and Xbase
            PRO – IDL
            POL – Apcera Policy Language doclet
            PY – Python source
            R – R source
            raku, rakumod, rakudoc, rakutest, nqp – Raku Language
            RED – Red source
            REDS – Red/System source
            RB – Ruby source
            RESX – Resource file for .NET applications
            RC, RC2 – Resource script files to generate resources for .NET applications
            RKT, RKTL – Racket source
            SCALA – Scala source
            SCI, SCE – Scilab
            SCM – Scheme source
            SD7 – Seed7 source
            SKB, SKC – Sage Retrieve 4GL Common Area (Main and Amended backup)
            SKD – Sage Retrieve 4GL Database
            SKF, SKG – Sage Retrieve 4GL File Layouts (Main and Amended backup)
            SKI – Sage Retrieve 4GL Instructions
            SKK – Sage Retrieve 4GL Report Generator
            SKM – Sage Retrieve 4GL Menu
            SKO – Sage Retrieve 4GL Program
            SKP, SKQ – Sage Retrieve 4GL Print Layouts (Main and Amended backup)
            SKS, SKT – Sage Retrieve 4GL Screen Layouts (Main and Amended backup)
            SKZ – Sage Retrieve 4GL Security File
            SLN – Visual Studio solution
            SPIN – Spin source (for Parallax Propeller microcontrollers)
            STK – Stickfigure file for Pivot stickfigure animator
            SWG – SWIG source code
            TCL – Tcl source code
            VAP – Visual Studio Analyzer project
            VB – Visual Basic.NET source
            VBG – Visual Studio compatible project group
            VBP, VIP – Visual Basic project
            VBPROJ – Visual Basic .NET project
            VCPROJ – Visual C++ project
            VDPROJ – Visual Studio deployment project
            XPL – XProc script/pipeline
            XQ – XQuery file
            XSL – XSLT stylesheet
            Y – yacc source
            Spreadsheet
            123 – Lotus 1-2-3
            AB2 – Abykus worksheet
            AB3 – Abykus workbook
            AWS – Ability Spreadsheet
            BCSV – Nintendo proprietary table format
            CLF – ThinkFree Calc
            CELL – Haansoft(Hancom) SpreadSheet software document
            CSV – Comma-Separated Values
            GSHEET – Google Drive Spreadsheet
            numbers – An Apple Numbers Spreadsheet file
            gnumeric – Gnumeric spreadsheet, a gziped XML file
            LCW – Lucid 3-D
            ODS – OpenDocument spreadsheet
            OTS – OpenDocument spreadsheet template
            QPW – Quattro Pro spreadsheet
            SDC – StarOffice StarCalc Spreadsheet
            SLK – SYLK (SYmbolic LinK)
            STC – OpenOffice.org XML (obsolete) Spreadsheet template
            SXC – OpenOffice.org XML (obsolete) Spreadsheet
            TAB – tab delimited columns; also TSV (Tab-Separated Values)
            TXT – text file
            VC – Visicalc
            WK1 – Lotus 1-2-3 up to version 2.01
            WK3 – Lotus 1-2-3 version 3.0
            WK4 – Lotus 1-2-3 version 4.0
            WKS – Lotus 1-2-3
            WKS – Microsoft Works
            WQ1 – Quattro Pro DOS version
            XLK – Microsoft Excel worksheet backup
            XLS – Microsoft Excel worksheet sheet (97–2003)
            XLSB – Microsoft Excel binary workbook
            XLSM – Microsoft Excel Macro-enabled workbook
            XLSX – Office Open XML worksheet sheet
            XLR – Microsoft Works version 6.0
            XLT – Microsoft Excel worksheet template
            XLTM – Microsoft Excel Macro-enabled worksheet template
            XLW – Microsoft Excel worksheet workspace (version 4.0)
            Tabulated data
            TSV – Tab-separated values
            CSV – Comma-separated values
            db – databank format; accessible by many econometric applications
            dif – accessible by many spreadsheet applications
            Video
            Main article: video file format
            AAF – mostly intended to hold edit decisions and rendering information, but can also contain compressed media essence
            3GP – the most common video format for cell phones
            GIF – Animated GIF (simple animation; until recently often avoided because of patent problems)
            ASF – container (enables any form of compression to be used; MPEG-4 is common; video in ASF-containers is also called Windows Media Video (WMV))
            AVCHD – Advanced Video Codec High Definition
            AVI – container (a shell, which enables any form of compression to be used)
            .bik – BIK Bink Video file. A video compression system developed by RAD Game Tools
            BRAW – a video format used by Blackmagic's Ursa Mini Pro 12K cameras.
            CAM – aMSN webcam log file
            COLLAB – Blackboard Collaborate session recording
            DAT – video standard data file (automatically created when we attempted to burn as video file on the CD)
            DVR-MS – Windows XP Media Center Edition's Windows Media Center recorded television format
            FLV – Flash video (encoded to run in a flash animation)
            MPEG-1 – M1V Video
            MPEG-2 – M2V Video
            NOA – rare movie format use in some Japanese eroges around 2002
            FLA – Adobe Flash (for producing)
            FLR – (text file which contains scripts extracted from SWF by a free ActionScript decompiler named FLARE)
            SOL – Adobe Flash shared object ("Flash cookie")
            STR – Sony PlayStation video stream
            M4V – video container file format developed by Apple
            .mkv – Matroska Matroska is a container format, which enables any video format such as MPEG-4 ASP or AVC to be used along with other content such as subtitles and detailed meta information
            WRAP – MediaForge (*.wrap)
            MNG – mainly simple animation containing PNG and JPEG objects, often somewhat more complex than animated GIF
            .mov – QuickTime container which enables any form of compression to be used; Sorenson codec is the most common; QTCH is the filetype for cached video and audio streams
            .mpeg, .mpg, .mpe – MPEG
            THP – Nintendo proprietary movie/video format
            MPEG-4 – MPEG-4 Part 14, shortened "MP4" multimedia container (most often used for Sony's PlayStation Portable and Apple's iPod)
            MXF – Material Exchange Format (standardized wrapper format for audio/visual material developed by SMPTE)
            ROQ – used by Quake III Arena
            NSV – NSV Nullsoft Streaming Video (media container designed for streaming video content over the Internet)
            Ogg – container, multimedia
            RM – RealMedia
            SVI – SVI Samsung video format for portable players
            SMI – SMI SAMI Caption file (HTML like subtitle for movie files)
            .smk – SMK Smacker video file. A video compression system developed by RAD Game Tools
            SWF – Adobe Flash (for viewing)
            WMV – Windows Media Video (See ASF)
            WTV – Windows Vista's and up Windows Media Center recorded television format
            YUV – raw video format; resolution (horizontal x vertical) and sample structure 4:2:2 or 4:2:0 must be known explicitly
            WebM – video file format for web video using HTML5
            Video editing, production
            BRAW – Blackmagic Design RAW video file name
            DRP – Davinci Resolve 17 project file
            FCP – Final Cut Pro project file
            MSWMM – Windows Movie Maker project file
            PPJ, PRPROJ – Adobe Premiere Pro video editing file
            IMOVIEPROJ – iMovie project file
            VEG, VEG-BAK – Sony Vegas project file
            SUF – Sony camera configuration file (setup.suf) produced by XDCAM-EX camcorders
            WLMP – Windows Live Movie Maker project file
            KDENLIVE – Kdenlive project file
            VPJ – VideoPad project file
            MOTN – Apple Motion project file
            IMOVIEMOBILE – iMovie project file for iOS users
            WFP, WVE – Wondershare Filmora Project
            PDS – Cyberlink PowerDirector project
            VPROJ – VSDC Free Video Editor project file
            Video game data
            List of common file formats of data for video games on systems that support filesystems, most commonly PC games.
            
            Minecraft
            files used by Mojang to develop Minecraft
            
            MCADDON – format used by the Bedrock Edition of Minecraft for add-ons; Resource packs for the game
            MCFUNCTION – format used by Minecraft for storing functions/scripts
            MCMETA – format used by Minecraft for storing data for customizable texture packs for the game
            MCPACK – format used by the Bedrock Edition of Minecraft for in-game texture packs; full addons for the game
            MCR – format used by Minecraft for storing data for in-game worlds before version 1.2
            MCTEMPLATE – format used by the Bedrock Edition of Minecraft for world templates
            MCWORLD – format used by the Bedrock Edition of Minecraft for in-game worlds
            NBS – format used by Note Block Studio, a tool that can be used to make note block songs for Minecraft.
            TrackMania/Maniaplanet Engine
            Formats used by games based on the TrackMania engine.
            
            GBX – All user-created content is stored in this file type.
            REPLAY.GBX – Stores the replay of a race.
            CHALLENGE.GBX, MAP.GBX – Stores tracks/maps.
            SYSTEMCONFIG.GBX – Launcher info.
            TRACKMANIAVEHICLE.GBX – Info about a certain car type.
            VEHICLETUNINGS.GBX – Vehicle physics.
            SOLID.GBX – A block's model.
            ITEM.GBX – Custom Maniaplanet item.
            BLOCK.GBX – Custom Maniaplanet block.
            TEXTURE.GBX – Info about a texture that are used in materials.
            MATERIAL.GBX – Info about a material such as surface type that are used in Solids.
            TMEDCLASSIC.GBX – Block info.
            GHOST.GBX – Player ghosts in Trackmania and TrackMania Turbo.
            CONTROLSTYLE.GBX – Menu files.
            SCORES.GBX – Stores info about the player's best times.
            PROFILE.GBX – Stores a player's info such as their login.
            DDS – Almost every texture in the game uses this format.
            PAK – Stores environment data such as valid blocks.
            LOC – A locator. Locators allow the game to download content such as car skins from an external server.
            SCRIPT.TXT – Scripts for Maniaplanet such as menus and game modes.
            XML – ManiaLinks.
            Doom engine
            Formats used by games based on the Doom engine.
            
            DEH – DeHackEd files to mutate the game executable (not officially part of the DOOM engine)
            DSG – Saved game
            LMP – A lump is an entry in a DOOM wad.
            LMP – Saved demo recording
            MUS – Music file (usually contained within a WAD file)
            WAD – Data storage (contains music, maps, and textures)
            Quake engine
            Formats used by games based on the Quake engine.
            
            BSP – BSP: (For Binary space partitioning) compiled map format
            MAP – MAP: Raw map format used by editors like GtkRadiant or QuArK
            MDL, MD2, MD3, MD5 – MDL/MD2/MD3/MD5: Model for an item used in the game
            PAK, PK2 – PAK/PK2: Data storage
            PK3, PK4 – PK3/PK4: used by the Quake II, Quake III Arena and Quake 4 game engines, respectively, to store game data, textures etc. They are actually .zip files.
            .dat – not specific file type, often generic extension for "data" files for a variety of applications, sometimes used for general data contained within the .PK3/PK4 files
            .fontdat – a .dat file used for formatting game fonts
            .roq – Video format
            .sav – Savegame/Savefile format
            Unreal Engine
            Formats used by games based on the Unreal engine.
            
            U – Unreal script format
            UAX – Animations format for Unreal Engine 2
            UMX – Map format for Unreal Tournament
            UMX – Music format for Unreal Engine 1
            UNR – Map format for Unreal
            UPK – Package format for cooked content in Unreal Engine 3
            USX – Sound format for Unreal Engine 1 and Unreal Engine 2
            UT2 – Map format for Unreal Tournament 2003 and Unreal Tournament 2004
            UT3 – Map format for Unreal Tournament 3
            UTX – Texture format for Unreal Engine 1 and Unreal Engine 2
            UXX – Cache format; these are files a client downloaded from server (which can be converted to regular formats)
            Duke Nukem 3D Engine
            Formats used by games based on this engine
            
            DMO – Save game
            GRP – Data storage
            MAP – Map (usually constructed with BUILD.EXE)
            Diablo Engine
            Formats used by Diablo by Blizzard Entertainment.
            
            SV – Save Game
            ITM – Item File
            Real Virtuality Engine
            Formats used by Bohemia Interactive. Operation:Flashpoint, ARMA 2, VBS2
            
            SQF – Format used for general editing
            SQM – Format used for mission files
            PBO – Binarized file used for compiled models
            LIP – Format that is created from WAV files to create in-game accurate lip-sync for character animations.
            Roblox studio engine
            RBXL – Roblox Studio place file (XML, binary) RBXM – Roblox Studio model file (XML, binary) RBXLX – Roblox Studio place file (exclusively XML) RBXMX – Roblox Studio model file (exclusively XML)
            
            Source engine
            Formats used by Valve. Half-Life 2, Counter-Strike: Source, Day of Defeat: Source, Half-Life 2: Episode One, Team Fortress 2, Half-Life 2: Episode Two, Portal, Left 4 Dead, Left 4 Dead 2, Alien Swarm, Portal 2, Counter-Strike: Global Offensive, Titanfall, Insurgency, Titanfall 2, Day of Infamy
            
            VMF – Valve Hammer Map editor raw map file
            VMX – Valve Hammer Map editor backup map file
            BSP – Source Engine compiled map file
            MDL – Source Engine model format
            SMD – Source Engine uncompiled model format
            PCF – Source Engine particle effect file
            HL2 – Half-Life 2 save format
            DEM – Source Engine demo format
            VPK – Source Engine pack format
            VTF – Source Engine texture format
            VMT – Source Engine material format.
            Pokemon generation V
            CGB – Pokemon Black and White/Pokemon Black 2 and White 2 C-Gear skins.
            Other formats
            ARC – used to store New Super Mario Bros. Wii level data
            B – used for Grand Theft Auto saved game files
            BOL – used for levels on Poing!PC
            DBPF – The Sims 2, DBPF, Package
            DIVA – Project DIVA timings, element coördinates, MP3 references, notes, animation poses and scores.
            ESM, ESP – Master and Plugin data archives for the Creation Engine
            HAMBU – format used by the Aidan's Funhouse game RGTW for storing map data[30]
            HE0, HE2, HE4 – HE games File
            GCF – format used by the Steam content management system for file archives
            IMG – format used by Renderware-based Grand Theft Auto games for data storage
            LOVE – format used by the LOVE2D Engine[31]
            MAP – format used by Halo: Combat Evolved for archive compression, Doom³, and various other games
            MCA – format used by Minecraft for storing data for in-game worlds[32]
            NBT – format used by Minecraft for storing program variables along with their (Java) type identifiers
            OEC – format used by OE-Cake for scene data storage
            OSB – osu! storyboard data
            OSC – osu!stream combined stream data
            OSF2 – free osu!stream song file
            OSR – osu! replay data
            OSU – osu! beatmap data
            OSZ2 – paid osu!stream song file
            P3D – format for panda3d by Disney
            PLAGUEINC – format used by Plague Inc. for storing custom scenario information[33]
            POD – format used by Terminal Reality
            RCT – Used for templates and save files in RollerCoaster Tycoon games
            REP – used by Blizzard Entertainment for scenario replays in StarCraft.
            Simcity, DBPF, .dat, .SC4Lot, .SC4Model – All game plugins use this format, commonly with different file extensions(Simcity 4)
            SMZIP – ZIP-based package for StepMania songs, themes and announcer packs.
            SOLITAIRETHEME8 – A solitaire theme for Windows solitaire
            USLD – format used by Unison Shift to store level layouts.
            VVVVVV – format used by VVVVVV
            CPS – format used by The Powder Toy, Powder Toy save
            STM – format used by The Powder Toy, Powder Toy stamp
            PKG – format used by Bungie for the PC Beta of Destiny 2, for nearly all the game's assets.
            CHR – format used by Team Salvato, for the character files of Doki Doki Literature Club!
            Z5 – format used by Z-machine for story files in interactive fiction.
            scworld – format used by Survivalcraft to store sandbox worlds.
            scskin – format used by Survivalcraft to store player skins.
            scbtex – format used by Survivalcraft to store block textures.
            prison – format used by Prison Architect to save prisons
            escape – format used by Prison Architect to save escape attempts
            WBFS – (Wii Backup File System)
            .GBA – Game Boy Advance ROM File
            .pss – Sony PlayStation 2 Game Video file and is used to store audio and video data by games for the PlayStation 2 console.
            Video game storage media
            List of the most common filename extensions used when a game's ROM image or storage medium is copied from an original read-only memory (ROM) device to an external memory such as hard disk for back up purposes or for making the game playable with an emulator. In the case of cartridge-based software, if the platform specific extension is not used then filename extensions ".rom" or ".bin" are usually used to clarify that the file contains a copy of a content of a ROM. ROM, disk or tape images usually do not consist of one file or ROM, rather an entire file or ROM structure contained within one file on the backup medium.[34]
            
            .a26 – Atari 2600
            .a52 – Atari 5200
            .a78 – Atari 7800
            .lnx – Atari Lynx
            .jag, .j64 – an Atari Jaguar game from a Rom Cartridge
            .iso, .wbfs, .wad, .wdf – a Wii and WiiU disk/game
            .gcm, .iso – a GameCube disk/game
            .min – a Pokemon mini rom/game
            .nds – a Nintendo DS game from a Rom Cartridge
            .dsi – Nintendo DSiWare
            .3ds – Nintendo 3DS
            .cia – Nintendo 3DS Installation File (for installing games with the use of the FBI homebrew application)
            .gb – Game Boy (this applies to the original Game Boy and the Game Boy Color)
            .gbc – Game Boy Color
            .gba – a Game Boy Advance Game from a Rom Cartridge
            .sav – Game Boy Advance Saved Data Files
            .sgm – Visual Boy Advance Save States
            .n64, .v64, .z64, .u64, .usa, .jap, .pal, .eur, .bin – Nintendo 64
            .pj – Project 64 Save States
            .nes – Nintendo Entertainment System[35]
            .fds – Famicom Disk System
            .jst – Jnes Save States
            .fc# – FCEUX Save States (.fc#, where # is any character, usually a number)
            .gg – Game Gear
            .sms – Master System
            .sg – SG-1000
            .smd, .bin – Mega Drive/Genesis
            .32x – Sega 32X
            .smc, .078, .sfc – Super NES (.078 is for split ROMs, which are rare)
            .fig – Super Famicom (Japanese releases are rarely .fig, above extensions are more common)
            .srm – Super NES Saved Data Files
            .zst, .zs1-.zs9, .z10-.z99 – ZSNES Save States (.zst, .zs1-.zs9, .z10-.z99)
            .frz, .000-.008 – Snes9X Save States
            .pce – TurboGrafx-16/PC Engine
            .npc, .ngp – Neo Geo Pocket
            .ngc – Neo Geo Pocket Color
            .vb – Virtual Boy
            .int – Intellivision
            .min – Pokémon Mini
            .vec – Vectrex
            .bin – Odyssey²
            .ws – WonderSwan
            .wsc – WonderSwan Color
            .tzx – ZX Spectrum (for exact copies of ZX Spectrum games)
            TAP – for tape images without copy protection
            Z80, SNA – (for snapshots of the emulator RAM)
            DSK – (for disk images)
            .tap – Commodore 64 (.tap) (for tape images including copy protection)
            T64 – (for tape images without copy protection, considerably smaller than .tap files)
            D64 – (for disk images)
            CRT – (for cartridge images)
            .adf – Amiga (.adf) (for 880K diskette images)
            ADZ – GZip-compressed version of the above.
            DMS – Disk Masher System, previously used as a disk-archiving system native to the Amiga, also supported by emulators.
            .pss – A Sony PlayStation 2 Game Video file and is used to store audio and video data by games for the PlayStation 2 console.
            Virtual machines
            Microsoft Virtual PC, Virtual Server
            .vfd – Virtual Floppy Disk
            .vhd – Virtual Hard Disk
            .vud – Virtual Undo Disk
            .vmc – Virtual Machine Configuration
            .vsv – Virtual Machine Saved State
            VMware ESX, GSX, Workstation, Player
            .log – Virtual Machine Logfile
            .vmdk, .dsk – Virtual Machine Disk
            .nvram – Virtual Machine BIOS
            .vmem – Virtual Machine paging file
            .vmsd – Virtual Machine snapshot metadata
            .vmsn – Virtual Machine snapshot
            .vmss, .std – Virtual Machine suspended state
            .vmtm – Virtual Machine team data
            .vmx, .cfg – Virtual Machine configuration
            .vmxf – Virtual Machine team configuration
            VirtualBox
            .vbox – VirtualBox machine
            .vdi – VirtualBox virtual disk image
            .vbox-extpack – VirtualBox extension pack
            Parallels Workstation
            .hdd – Virtual Machine hard disk
            .pvs – Virtual Machine preferences/configuration
            .sav – Virtual Machine saved state
            QEMU
            .cow – Copy-on-write
            .qcow – QEMU copy-on-write
            .qcow2 – QEMU copy-on-write – version 2
            .qed – QEMU enhanced disk format
            Web page
            Static
            
            DTD – Document Type Definition (standard), MUST be public and free
            .html, .htm – HTML HyperText Markup Language
            .xhtml, .xht – XHTML eXtensible HyperText Markup Language
            .mht, .mhtml – MHTML Archived HTML, store all data on one web page (text, images, etc.) in one big file
            .maff – MAF web archive based on ZIP
            Dynamically generated
            
            .asp – ASP Microsoft Active Server Page
            .aspx – ASPX Microsoft Active Server Page. NET
            .adp – ADP AOLserver Dynamic Page
            .bml – BML Better Markup Language (templating)
            .cfm – CFM ColdFusion
            .cgi – CGI
            .ihtml – iHTML Inline HTML
            .jsp – JSP JavaServer Pages
            .las, .lasso, .lassoapp – Lasso, A file created or served with the Lasso Programming Language
            .pl – Perl
            .php, .php?, .phtml – PHP ? is version number (previously abbreviated Personal Home Page, later changed to PHP: Hypertext Preprocessor)
            .shtml – SSI HTML with Server Side Includes (Apache)
            .stm – SSI HTML with Server Side Includes (Apache)
            Markup languages and other web standards-based formats
            .atom, .xml – Atom Another syndication format.
            .eml – EML Format used by several desktop email clients.
            .jsonld – JSON-LD A JSON-based serialization for linked data.
            .kprx – KPRX A XML-based serialization for workflow definition generated by K2.
            .ps – PS A XML-based serialization for test automation scripts called PowerScripts for K2 based applications.
            .metalink, .met – Metalink A format to list metadata about downloads, such as mirrors, checksums, and other information.
            .rss, .xml – RSS Syndication format.
            .markdown, .md – Markdown Plain text formatting syntax, which is popularly used to format "readme" files.
            .se – Shuttle Another lightweight markup language.
            Other
            AXD – cookie extensions found in temporary internet folder
            APK – Android Package Kit
            BDF – Binary Data Format – raw data from recovered blocks of unallocated space on a hard drive
            CBP – CD Box Labeler Pro, CentraBuilder, Code::Blocks Project File, Conlab Project
            CEX – SolidWorks Enterprise PDM Vault File
            COL – Nintendo GameCube proprietary collision file (.col)
            CREDX – CredX Dat File
            DDB – Generating code for Vocaloid singers voice (see .DDI)
            DDI – Vocaloid phoneme library (Japanese, English, Korean, Spanish, Chinese, Catalan)
            DUPX – DuupeCheck database management tool project file
            FTM – Family Tree Maker data file
            FTMB – Family Tree Maker backup file
            GA3 – Graphical Analysis 3
            .ged – GEDCOM (GEnealogical Data COMmunication) format to exchange genealogy data between different genealogy software
            HLP – Windows help file
            IGC – flight tracks downloaded from GPS devices in the FAI's prescribed format
            INF – similar format to INI file; used to install device drivers under Windows, inter alia.
            JAM – JAM Message Base Format for BBSes
            KMC – tests made with KatzReview's MegaCrammer
            KCL – Nintendo GameCube/Wii proprietary collision file (.kcl)
            KTR – Hitachi Vantara Pentaho Data Integration/Kettle Transformation Project file
            LNK – Microsoft Windows format for Hyperlinks to Executables
            LSM – LSMaker script file (program using layered .jpg to create special effects; specifically designed to render lightsabers from the Star Wars universe) (.lsm)
            MELSAVE – Melon Playground build save file
            MELMOD – Melon Playground mod file
            NARC – Archive format used in Nintendo DS games.
            OER – AU OER Tool, Open Educational Resource editor
            PA – Used to assign sound effects to materials in KCL files (.pa)
            PIF – Used to run MS-DOS programs under Windows
            POR – So called "portable" SPSS files, readable by PSPP
            PXZ – Compressed file to exchange media elements with PSALMO
            RISE – File containing RISE generated information model evolution
            SCR – Windows Screen Saver file
            TOPC – TopicCrunch SEO Project file holding keywords, domain, and search engine settings (ASCII)
            XLF – Utah State University Extensible LADAR Format
            XMC – Assisted contact lists format, based on XML and used in kindergartens and schools
            ZED – My Heritage Family Tree
            zone – Zone file a text file containing a DNS zone
            FX – Microsoft DirectX plain text effects and properties for the associated file and are used to specify the textures, shading, rendering, lighting and other 3D effects (.fx)
            MIFRAMES – Mine-imator keyframes file (.miframes)
            MILANGUAGE – Mine-Imator language data file (.milanguage)
            MIDATA – Mine-Imator data file (.midata)
            BCA – Short for Burst Cutting Area Holds the information of the circular area near the center of a DVD, HD DVD or Blu-ray Disc, it is usually 64 bytes in size. (.bca)
            Cursors
            ANI – Animated cursor
            CUR – Cursor file
            Smes – Hawk's Dock configuration file
            Generalized files
            General data formats
            These file formats are fairly well defined by long-term use or a general standard, but the content of each file is often highly specific to particular software or has been extended by further standards for specific uses.
            
            Text-based
            CSV – comma-separated values
            HTML – hyper text markup language
            CSS – cascading style sheets
            INI – a configuration text file whose format is substantially similar between applications
            JSON – JavaScript Object Notation is an openly used data format now used by many languages, not just JavaScript
            TSV – tab-separated values
            XML – an open data format
            YAML – an open data format
            ReStructuredText – an open text format for technical documents used mainly in the Python programming language
            .md – Markdown an open lightweight markup language to create simple but rich text, often used to format README files
            AsciiDoc – an open human-readable markup document format semantically equivalent to DocBook
            .yni – a configuration file similar to YAML
            Generic file extensions
            These are filename extensions and broad types reused frequently with differing formats or no specific format by different programs.
            
            Binary files
            .bak, .bk – Bak file various backup formats: some just copies of data files, some in application-specific data backup formats, some formats for general file backup programs
            BIN – binary data, often memory dumps of executable code or data to be re-used by the same software that originated it
            DAT – data file, usually binary data proprietary to the program that created it, or an MPEG-1 stream of Video CD
            DSK – file representations of various disk storage images
            RAW – raw (unprocessed) data
            SZH – files that are associated with zero unique file types (the most prevalent being the Binary Data format)
            Text files
            .cnf, .conf, .cfg – configuration file substantially software-specific
            .log – logfiles usually text, but sometimes binary
            .asc, .text, .txt,– human-readable plain text, usually no more specific
            Partial files
            Differences and patches
            diff – text file differences created by the program diff and applied as updates by patch
            Incomplete transfers
            .!ut – !UT partly complete uTorrent download
            .crdownload – CRDOWNLOAD partly complete or incomplete Google Chrome or Microsoft Edge download
            .opdownload – OPDOWNLOAD partly complete or incomplete Opera download
            .part – PART partly complete Mozilla Firefox or Transmission download
            .partial – PARTIAL partly complete Internet Explorer or Edge Legacy download
            Temporary files
            .temp, .tmp – Temporary file sometimes in a specific format, but often just raw data in the middle of processing
        """[1:-1]

        def P(s):
            'Make extension is s lowercase and prepend a "." if needed'
            s = s.strip().lower()
            assert s
            if not s.startswith("."):
                s = "." + s
            return s

        dsh = "–"  # U+2013 en dash
        out = defaultdict(list)
        for line in data.split("\n"):
            if not line.strip():
                continue
            if dsh in line:
                e, descr = [i.strip() for i in line.split(dsh, 1)]
                e = e.lower().strip()
                if e == "a.out":
                    continue
                if "," in e:
                    for e1 in e.split(","):
                        e1 = e1.strip()
                        if not e1:
                            continue
                        if not e1.startswith("."):
                            e1 = "." + e1
                        yield e1, descr
                else:
                    if not e.startswith("."):
                        e = "." + e
                    yield e, descr

    def Header():
        script = P(sys.argv[0]).absolute()
        dt = time.asctime(time.localtime())
        print(
            dedent(f"""
        '''
        This module provides the extensions dictionary, which provides a
        number of lowercase extensions casually used for various datafiles.

        Constructed by {script} {dt}
        '''

        extensions = {{
        """)
        )

    def Trailer():
        print("}")

    def Vet():
        "Check the dict"
        bad = 0
        for i in g.di:
            if not i.startswith("."):
                t.print(f"{t.err}{i!r}: missing '.'")
                bad += 1
        if bad:
            exit(1)

    def Fix():
        """Find keys with '-' in them and generate suitable ranges of them."""
        Vet()
        for i in g.di.copy():
            if i == ".zs1-.zs9":
                for j in range(1, 10):
                    g.di[f".zs{j}"] = g.di[i]
                del g.di[i]
            elif i == ".z10-.z99":
                for j in range(10, 100):
                    g.di[f".z{j}"] = g.di[i]
                del g.di[i]
            elif i == ".000-.008":
                for j in range(9):
                    g.di[f".00{j}"] = g.di[i]
                del g.di[i]

    def DumpDict():
        Fix()
        for i in sorted(g.di):
            lst = g.di[i]
            if len(lst) == 1:
                print(f"    {i!r}: ({lst[0]!r},),")
            else:
                print(f"    {i!r}: (")
                for j in sorted(set(g.di[i]), key=str.lower):
                    print(f"        {j!r},")
                print(f"    ),")


if __name__ == "__main__":
    # Construct a suitable dictionary (key is extension, value is list of
    # descriptions)
    for e, s in Webopedia():
        g.di[e].append(s)
    for e, s in Wikipedia():
        g.di[e].append(s)
    # Dump this dict to stdout
    Header()
    DumpDict()
    Trailer()
