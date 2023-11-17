# From https://en.wikipedia.org/wiki/List_of_file_formats
# Downloaded Thu 16 Nov 2023 01:13:25 PM
from collections import defaultdict
data = '''
    .?Q? – files that are compressed, often by the SQ program.
    7z – 7z: 7-Zip compressed file
    A – An external file extension for C/C++
    AAC – Advanced Audio Coding
    ace – ace: ACE compressed file
    ALZ – ALZip compressed file
    APK – Android package: Applications installable on Android; package format of the Alpine Linux distribution
    APPX – Microsoft Application Package (.appx)
    APP – HarmonyOS APP Packs file format for HarmonyOS apps installable from AppGallery and third party OpenHarmony based app distribution stores.
    AT3 – Sony's UMD data compression
    ARC – ARC: pre-Zip data compression
    ARC – Nintendo U8 Archive (mostly Yaz0 compressed)
    ARJ – ARJ compressed file
    ASS – a subtitles file created by Aegisub, a video typesetting application (also a Halo game engine file)
    SSA – a subtitles file created by Aegisub, a video typesetting application (also a Halo game engine file)
    B – (B file) Similar to .a, but less compressed.
    BA – BA: Scifer Archive (.ba), Scifer External Archive Type
    BIN – compressed archive, can be read and used by CD-ROMs and Java, extractable by 7-zip and WINRAR
    .bkf – Microsoft backup created by NTBackup.c
    Blend – An external 3D file format used by the animation software, Blender.
    .bz2 – bzip2
    BMP – Bitmap Image – You can create one by right-clicking the home screen, next, click new, then, click Bitmap Image
    cab – A cabinet (.cab) file is a library of compressed files stored as one file. Cabinet files are used to organize installation files that are copied to the user's system.[2]
    c4 – JEDMICS image files, a DOD system
    cals – JEDMICS image files, a DOD system
    xaml – Used in programs like Visual Studio to create exe files.
    CPT, SEA – Compact Pro (Macintosh)
    DAA – DAA: Closed-format, Windows-only compressed disk image
    deb – deb: Debian install package
    DMG – an Apple compressed/encrypted format
    DDZ – a file which can only be used by the "daydreamer engine" created by "fever-dreamer", a program similar to RAGS, it's mainly used to make somewhat short games.
    DN – Adobe Dimension CC file format
    DNG – "Digital Negative" a type of raw image file format used in digital photography.
    DPE – Package of AVE documents made with Aquafadas digital publishing tools.
    .egg – Alzip Egg Edition compressed file
    .egt – EGT Universal Document also used to create compressed cabinet files replaces .ecab
    .ECAB, .ezip – EGT Compressed Folder used in advanced systems to compress entire system folders, replaced by EGT Universal Document
    ESD – ESD: Electronic Software Distribution, a compressed and encrypted WIM File
    .ess – EGT SmartSense File, detects files compressed using the EGT compression system.
    .exe – Windows application
    .flipchart – Used in Promethean ActivInspire Flipchart Software.
    .fun – A FUN file is a file that has been encrypted by Jigsaw ransomware, which is malware distributed by cybercriminals. It contains a file, such as a .JPG, .DOCX, .XLSX, .MP4, or .CSV file, that has been renamed and encrypted by the virus.
    flm – FL Studio Mobile, can also be used as a project file.
    flp – FL Studio Project File
    .gbs, .ggp, .gsc – GBS OtterUI binary scene file
    .gho, .ghs – GHO Norton Ghost
    .gif – GIF Graphics Interchange Format
    .gz – gzip Compressed file
    .html – HTML code file
    .ipg – Format in which Apple Inc. packages their iPod games. can be extracted through Winrar
    jar – jar ZIP file with manifest for use with Java applications.
    JPG – Joint Photographic Experts Group – Image File
    JPEG – Joint Photographic Experts Group – Image File
    .Lawrence – LBR Lawrence Compiler Type file
    LBR – LBR Library file
    .llsp3 – Lego Spike program file
    LQR – LQR LBR Library file compressed by the SQ program.
    .lzh – LHA Lempel, Ziv, Huffman
    .lz – lzip Compressed file
    .lzo – lzo
    lzma – lzma Lempel–Ziv–Markov chain algorithm compressed file
    LZX – LZX
    .lua – Lua
    .mbw – MBRWizard archive
    MHTML – Mime HTML (Hyper-Text Markup Language) code file
    .midi – Musical Instrument Digital Interface
    .mpq – MPQ Archives Used by Blizzard Entertainment
    .bin – BIN MacBinary
    .nl2pkg – NoLimits 2 Package
    .nth – NTH: Nokia Theme Used by Nokia Series 40 Cellphones
    .oar – OAR: OAR archive
    OGG – Ogg Vorbis Compressed Audio File
    OSG – Compressed osu! live gameplay archive (optimized for spectating)
    OSK – Compressed osu! skin archive
    OSR – Compressed osu! replay archive
    OSZ – Compressed osu! beatmap archive
    PAK – Enhanced type of .ARC archive
    .par, .par2 – PAR Parchive
    .paf – PAF Portable Application File
    .pea – PEA PeaZip archive file
    PNG – Portable Network Graphic Image File
    Webp – Raster image format developed by Google for web graphics
    .php – PHP code file
    .pyk – PYK Compressed file
    .pk3 – PK3 Quake 3 archive (See note on Doom³)
    .pk4 – PK4 Doom³ archive (Opens similarly to a zip archive.)
    .pnj – sub-format of the MNG file format, used for encapsulating JPEG files[3]
    .pxz – PXZ A compressed layered image file used for the image editing website, pixlr.com .
    py, pyw – Python code file
    .pmp – Penguinmod Project
    .rar – RAR Rar Archive, for multiple file archive (rar to .r01-.r99 to s01 and so on)
    RAG, RAGS – Game file, a game playable in the RAGS game-engine, a free program which both allows people to create games, and play games, games created have the format "RAG game file"
    RaX – Archive file created by RaX
    RBXL – Roblox Studio place file (XML, binary)
    RBXLX – Roblox Studio place file (exclusively XML)
    RBXM – Roblox Studio model file (XML, binary)
    RBXMX – Roblox Studio model file (exclusively XML)
    RPM – Red Hat package/installer for Fedora, RHEL, and similar systems.
    sb – Scratch 1.X file
    sb2 – Scratch 2.0 file
    sb3 – Scratch 3.0 file
    SEN – Scifer Archive (.sen) – Scifer Internal Archive Type
    .sf2 – Polyphone Soundfont 2
    .sf3 – Polyphone Soundfont 3
    .sf4 – Polyphone Soundfont 4
    .sitx – SIT StuffIt (Macintosh)
    SIS, SISX – SIS/SISX: Symbian Application Package
    SKB – Google SketchUp backup File
    .sq – SQ: Squish Compressed Archive
    .srt – SubRip Subtitle – file format for closed captioning or subtitles.
    SWM – Splitted WIM File, usually found on OEM Recovery Partition to store preinstalled Windows image, and to make Recovery backup (to USB Drive) easier (due to FAT32 limitations)
    SZS – Nintendo Yaz0 Compressed Archive
    TAR – TAR: group of files, packaged as one file
    Gzip, .tar.gz – (Gzip, .tar.gz): TGZ gzipped tar file
    .tb – TB Tabbery Virtual Desktop Tab file
    .tib – TIB Acronis True Image backup
    UHA – Ultra High Archive Compression
    .uue – UUE unified utility engine – the generic and default format for all things UUe-related.
    uf2 – Microsoft makecode arcade game.
    VIV – Archive format used to compress data for several video games, including Need For Speed: High Stakes.
    VOL – video game data package.
    VSA – Altiris Virtual Software Archive
    WAX – Wavexpress – A ZIP alternative optimized for packages containing video, allowing multiple packaged files to be all-or-none delivered with near-instantaneous unpacking via NTFS file system manipulation.
    .wav – a format for storing uncompressed audio files.
    .wfp – a Wondershare Flimora project file
    WIM – WIM A compressed disk image for installing Windows Vista or higher, Windows Fundamentals for Legacy PC, or restoring a system image made from Backup and Restore (Windows Vista/7)
    XAP – Windows Phone Application Package
    xz – xz compressed files, based on LZMA/LZMA2 algorithm
    Z – Unix compress file
    zoo – zoo: based on LZW
    zip – zip: popular compression format
    ZIM – ZIM: an open file format that stores wiki content for offline usage
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
    LEMONAPP – LemonOS/LemonTabOS/LemonRoid App (.lem_app)
    HTML – Hypertext Markup Language
    Msi – Windows installation file
    Vdhx – Virtual disk created by Hyper-V (Hyper-V runs on windows operating system)
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
    Avro – Data format appropriate for ingestion of record based attributes. Distinguishing characteristic is schema is stored on each row enabling schema evolution.
    Parquet – Columnar data storage. It is typically used within the Hadoop ecosystem.
    ORC – Similar to Parquet, but has better data compression and schema evolution handling.
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
    HTML – HyperText Markup Language (.html, .htm)
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
    MYO – MYOB Limited (Windows) File
    MYOB – MYOB Limited (Mac) File
    TAX – TurboTax File
    YNAB – You Need a Budget (YNAB) File
    IFX – Interactive Financial Exchange XML-based specification for various forms of financial transactions
    .ofx – Open Financial Exchange， open standard supported by CheckFree and Microsoft and partly by Intuit; SGML and later XML based
    QFX – proprietary pay-only format used only by Intuit
    .qif – Quicken Interchange Format open standard formerly supported by Intuit
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
    IFDS – Incredibly Flexible Data Storage file format. File extension and the magic number does not have to be IFDS.[8]
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
    3DT – 3D Topicscape, the database in which the meta-data of a 3D Topicscape is held, it is a form of 3D concept map (like a 3D mind-map) used to organize ideas, information, and computer files
    ATY – 3D Topicscape file, produced when an association type is exported; used to permit round-trip (export Topicscape, change files and folders as desired, re-import to 3D Topicscape)
    CAG (file format) – Linear Reference System
    FES (file format) – 3D Topicscape file, produced when a fileless occurrence in 3D Topicscape is exported to Windows. Used to permit round-trip (export Topicscape, change files and folders as desired, re-import them to 3D Topicscape)
    MGMF – MindGenius Mind Mapping Software file format
    MM – FreeMind mind map file (XML)
    MMP (file format) – Mind Manager mind map file
    TPC (file format) – 3D Topicscape file, produced when an inter-Topicscape topic link file is exported to Windows; used to permit round-trip (export Topicscape, change files and folders as desired, re-import to 3D Topicscape)
    ACT – Adobe Color Table. Contains a raw color palette and consists of 256 24-bit RGB colour values.
    ASE – Adobe Swatch Exchange. Used by Adobe Substance, Photoshop, Illustrator, and InDesign.[10]
    GPL – GIMP palette file. Uses a text representation of color names and RGB values. Various open source graphical editors can read this format,[11] including GIMP, Inkscape, Krita,[12] KolourPaint, Scribus, CinePaint, and MyPaint.[13]
    PAL – Microsoft RIFF palette file
    ICC, ICM – Color profile conforming the specification of the ICC.
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
    Alias – Alias (Mac OS)
    JNLP – Java Network Launching Protocol, an XML file used by Java Web Start for starting Java applets over the Internet
    LNK – binary-format file shortcut in Microsoft Windows 95 and later
    APPREF-MS – File shortcut format used by ClickOnce
    NAL – ZENworks Instant shortcut (opens a .EXE not on the C:/ )
    URL – INI file pointing to a URL bookmarks/Internet shortcut in Microsoft Windows
    WEBLOC – Property list file pointing to a URL bookmarks/Internet shortcut in macOS
    SYM – Symbolic link
    .desktop – Desktop entry on Linux Desktop environments
    Harwell-Boeing – a file format designed to store sparse matrices
    MML – MathML – Mathematical Markup Language
    ODF – OpenDocument Math Formula
    SXM – OpenOffice.org XML (obsolete) Math Formula
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
    .OCX – .OCX are Object Control extensions
    .TLB – .TLB are Windows Type Library
    .VBX – .VBX are Visual Basic extensions
    DVI – DVI are Device independent format
    .egt – Universal Document can be used to store CSS type styles
    PLD – PLD (Need to be added!!!)
    PCL – PCL (Need to be added!!!)
    PDF – PDF are Portable Document Format
    .ps, .ps, .gz – PostScript (Need to be added!!!)
    SNP – SNP are Microsoft Access Report Snapshot
    XSL-FO – XSL-FO (Formatting Objects)
    CSS – CSS are Cascading Style Sheets
    .xslt, .xsl – XML Style Sheet
    .tpl – Web template
    MNB – MyInfo notebook
    MSG – Microsoft Outlook task manager
    ORG – Lotus Organizer PIM package
    ORG – Emacs Org-Mode Mindmanager, contacts, calendar, email-integration
    PST, OST – Microsoft Outlook email communication
    SC2 – Microsoft Schedule+ calendar
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
    MPP – Microsoft Project
    bib – BibTeX
    enl – EndNote
    ris – Research Information Systems RIS (file format)
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
    NetCDF – Network common data format
    HDR, HDF, h4, h5 – Hierarchical Data Format
    SDXF – SDXF, (Structured Data Exchange Format)
    CDF – Common Data Format
    CGNS – CGNS, CFD General Notation System
    FMF – Full-Metadata Format
    GRIB – Grid in Binary, WMO format for weather model data
    BUFR – WMO format for weather observation data
    PP – UK Met Office format for weather model data
    NASA-Ames – Simple text format for observation data. First used in aircraft studies of the atmosphere.
    CML – Chemical Markup Language (CML) (.cml)
    .mol, .sd, .sdf – Chemical table file (CTab)
    .dx, .jdx – Joint Committee on Atomic and Molecular Physical Data (JCAMP)
    .smi – Simplified molecular input line entry specification (SMILES)
    .g6, .s6 – graph6, sparse6, ASCII encoding of Adjacency matrices
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
    HL7 – Health Level 7, a framework for exchange, integration, sharing, and retrieval of health information electronically
    xDT – a family of data exchange formats for medical records
    CBF – Common Biometric Format, based on CBEFF 2.0 (Common Biometric ExFramework).
    EBF – Extended Biometric Format, based on CBF but with S/MIME encryption support and semantic extensions
    CBFX – XML Common Biometric Format, based upon XCBF 1.1 (OASIS XML Common Biometric Format)
    EBFX – XML Extended Biometric Format, based on CBFX but with W3C XML Encryption support and semantic extensions
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
    OMF – OpenPGP Message Format used by Pretty Good Privacy, GNU Privacy Guard, and other OpenPGP software; can contain keys, signed data, or encrypted data; can be binary or text ("ASCII armored")
    GXK – Galaxkey, an encryption platform for authorized, private and confidential email communication[citation needed]
    .ssh – OpenSSH private key, Secure Shell private key; format generated by ssh-keygen or converted from PPK with PuTTYgen[21][22][23]
    .pub – OpenSSH public key, Secure Shell public key; format generated by ssh-keygen or PuTTYgen[21][22][23]
    .ppk – PuTTY private key, Secure Shell private key, in the format generated by PuTTYgen instead of the format used by OpenSSH[21][22][23]
    .nSign – nSign public key nSign public key in a custom format[24]
    .cer, .crt, .der – Distinguished Encoding Rules stores certificates
    .p7b, .p7c – PKCS#7 SignedData commonly appears without main data, just certificates or certificate revocation lists (CRLs)
    .p12, .pfx – PKCS#12 can store public certificates and private keys
    PEM – Privacy-enhanced Electronic Mail: full format not widely used, but often used to store Distinguished Encoding Rules in Base64 format
    PFX – Microsoft predecessor of PKCS#12
    AXX – Encrypted file, created with AxCrypt
    EEA – An encrypted CAB, ostensibly for protecting email attachments
    TC – Virtual encrypted disk container, created by TrueCrypt
    KODE – Encrypted file, created with KodeFile
    nSignE – An encrypted private key, created by nSign[24]
    BPW – Encrypted password file created by Bitser password manager
    KDB – KeePass 1 database
    KDBX – KeePass 2 database
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
    MOD – Soundtracker and Protracker sample and melody modules
    MT2 – MadTracker 2 module
    S3M – Scream Tracker 3 module
    XM – Fast Tracker module
    IT – Impulse Tracker module
    NSF – NES Sound Format
    MID, MIDI – Standard MIDI file; most often just notes and controls but occasionally also sample dumps (.mid, .rmi)
    FTM – FamiTracker Project file
    BTM – BambooTracker Project file
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
    AIMPPL – AIMP Playlist format
    ASX – Advanced Stream Redirector
    RAM – Real Audio Metafile For RealAudio files only.
    XPL – HDi playlist
    XSPF – XML Shareable Playlist Format
    ZPL – Xbox Music (Formerly Zune) Playlist format from Microsoft
    M3U – Multimedia playlist file
    PLS – Multimedia playlist, originally developed for use with the museArc
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
    🗿 – ThirtyDollar Project file
    DVR-MS – Windows XP Media Center Edition's Windows Media Center recorded television format
    WTV – Windows Vista's and up Windows Media Center recorded television format
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
    TSV – Tab-separated values
    CSV – Comma-separated values
    db – databank format; accessible by many econometric applications
    dif – accessible by many spreadsheet applications
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
    MCADDON – format used by the Bedrock Edition of Minecraft for add-ons; Resource packs for the game
    MCFUNCTION – format used by Minecraft for storing functions/scripts
    MCMETA – format used by Minecraft for storing data for customizable texture packs for the game
    MCPACK – format used by the Bedrock Edition of Minecraft for in-game texture packs; full addons for the game
    MCR – format used by Minecraft for storing data for in-game worlds before version 1.2
    MCTEMPLATE – format used by the Bedrock Edition of Minecraft for world templates
    MCWORLD – format used by the Bedrock Edition of Minecraft for in-game worlds
    NBS – format used by Note Block Studio, a tool that can be used to make note block songs for Minecraft.
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
    DEH – DeHackEd files to mutate the game executable (not officially part of the DOOM engine)
    DSG – Saved game
    LMP – A lump is an entry in a DOOM wad.
    LMP – Saved demo recording
    MUS – Music file (usually contained within a WAD file)
    WAD – Data storage (contains music, maps, and textures)
    BSP – BSP: (For Binary space partitioning) compiled map format
    MAP – MAP: Raw map format used by editors like GtkRadiant or QuArK
    MDL, MD2, MD3, MD5 – MDL/MD2/MD3/MD5: Model for an item used in the game
    PAK, PK2 – PAK/PK2: Data storage
    PK3, PK4 – PK3/PK4: used by the Quake II, Quake III Arena and Quake 4 game engines, respectively, to store game data, textures etc. They are actually .zip files.
    .dat – not specific file type, often generic extension for "data" files for a variety of applications, sometimes used for general data contained within the .PK3/PK4 files
    .fontdat – a .dat file used for formatting game fonts
    .roq – Video format
    .sav – Savegame/Savefile format
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
    DMO – Save game
    GRP – Data storage
    MAP – Map (usually constructed with BUILD.EXE)
    SV – Save Game
    ITM – Item File
    SQF – Format used for general editing
    SQM – Format used for mission files
    PBO – Binarized file used for compiled models
    LIP – Format that is created from WAV files to create in-game accurate lip-sync for character animations.
    RBXL – Roblox Studio place file (XML, binary) RBXM – Roblox Studio model file (XML, binary) RBXLX – Roblox Studio place file (exclusively XML) RBXMX – Roblox Studio model file (exclusively XML)
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
    CGB – Pokemon Black and White/Pokemon Black 2 and White 2 C-Gear skins.
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
    .vfd – Virtual Floppy Disk
    .vhd – Virtual Hard Disk
    .vud – Virtual Undo Disk
    .vmc – Virtual Machine Configuration
    .vsv – Virtual Machine Saved State
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
    .vbox – VirtualBox machine
    .vdi – VirtualBox virtual disk image
    .vbox-extpack – VirtualBox extension pack
    .hdd – Virtual Machine hard disk
    .pvs – Virtual Machine preferences/configuration
    .sav – Virtual Machine saved state
    .cow – Copy-on-write
    .qcow – QEMU copy-on-write
    .qcow2 – QEMU copy-on-write – version 2
    .qed – QEMU enhanced disk format
    DTD – Document Type Definition (standard), MUST be public and free
    .html, .htm – HTML HyperText Markup Language
    .xhtml, .xht – XHTML eXtensible HyperText Markup Language
    .mht, .mhtml – MHTML Archived HTML, store all data on one web page (text, images, etc.) in one big file
    .maff – MAF web archive based on ZIP
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
    .atom, .xml – Atom Another syndication format.
    .eml – EML Format used by several desktop email clients.
    .jsonld – JSON-LD A JSON-based serialization for linked data.
    .kprx – KPRX A XML-based serialization for workflow definition generated by K2.
    .ps – PS A XML-based serialization for test automation scripts called PowerScripts for K2 based applications.
    .metalink, .met – Metalink A format to list metadata about downloads, such as mirrors, checksums, and other information.
    .rss, .xml – RSS Syndication format.
    .markdown, .md – Markdown Plain text formatting syntax, which is popularly used to format "readme" files.
    .se – Shuttle Another lightweight markup language.
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
    ANI – Animated cursor
    CUR – Cursor file
    Smes – Hawk's Dock configuration file
    CSV – comma-separated values
    HTML – hyper text markup language
    CSS – cascading style sheets
    INI – a configuration text file whose format is substantially similar between applications
    JSON – JavaScript Object Notation is an openly used data format now used by many languages, not just JavaScript
    TSV – tab-separated values
    XML – an open data format
    YAML – an open data format
    .md – Markdown an open lightweight markup language to create simple but rich text, often used to format README files
    AsciiDoc – an open human-readable markup document format semantically equivalent to DocBook
    .yni – a configuration file similar to YAML
    .bak, .bk – Bak file various backup formats: some just copies of data files, some in application-specific data backup formats, some formats for general file backup programs
    BIN – binary data, often memory dumps of executable code or data to be re-used by the same software that originated it
    DAT – data file, usually binary data proprietary to the program that created it, or an MPEG-1 stream of Video CD
    DSK – file representations of various disk storage images
    RAW – raw (unprocessed) data
    SZH – files that are associated with zero unique file types (the most prevalent being the Binary Data format)
    .cnf, .conf, .cfg – configuration file substantially software-specific
    .log – logfiles usually text, but sometimes binary
    .asc, .text, .txt,– human-readable plain text, usually no more specific
    diff – text file differences created by the program diff and applied as updates by patch
    .!ut – !UT partly complete uTorrent download
    .crdownload – CRDOWNLOAD partly complete or incomplete Google Chrome or Microsoft Edge download
    .opdownload – OPDOWNLOAD partly complete or incomplete Opera download
    .part – PART partly complete Mozilla Firefox or Transmission download
    .partial – PARTIAL partly complete Internet Explorer or Edge Legacy download
    .temp, .tmp – Temporary file sometimes in a specific format, but often just raw data in the middle of processing
'''
dash = "–"
o = []
out = defaultdict(list)
for i, line in enumerate(data.split("\n")):
    line = line.strip()
    if not line:
        continue
    if dash not in line:
        print(f"Line {i + 3} missing en dash '{dash}'")
        exit(1)
    ext, descr = line.split(dash, 1)
    if "," in ext:
        for j in ext.split(","):
            o.append((j.strip(), descr.strip()))
# Get widest extension
if 1:
    import debug
    debug.SetDebugger()
# Put in dict
for i in o:
    ext, descr = i
    ext = ext.lower()
    if ext.strip():
        if not ext.startswith("."):
            ext = "." + ext
        out[ext].append(descr)
# Ensure no duplicates
for i in out:
    out[i] = list(sorted(set(out[i])))
# Print to stdout
keys = sorted(list(out))
w = max(len(i) for i in keys)
for i in keys:
    for j in out[i]:
        print(f'"{i}": "{j}",')
