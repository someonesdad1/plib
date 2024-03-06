'''

ToDo:
    - Color-highlight the matched strings in each line
    - The data need to be regularized
        - A single field for each entry
        - Use a character like "|" to separate fields (note this character
          isn't in the current data)
        - Output in e.g. CSV form.
        - Datafile should be pure ASCII if possible
        - There are 8268 records currently, a lot of work
        - Eliminate titles in authors' names (like Dr.)

    - Eliminate duplicates (e.g. Lautard's "Wax/Stockholm tar resist")
    - "A Rocking', ' Swinging Grinder Table" in vp1 has a comma in
        it, so it needs to be parsed by e.g. a CSV routine.  Joe
        Landau's index has it in it, so the vp1 index needs to be
        filtered and written so it can be simply split with a simple
        field separator.

    - Add feature that highlights HSM issues I have.

---------------------------------------------------------------------------
Search various indexes of metalworking publications
    The script contains its own data, so this is the only file you
    should need.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2020 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Search metalworking publications for titles
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from collections import namedtuple
    from io import StringIO
    import csv
    import getopt
    import re
    import sys
if 1:   # Custom imports
    from wrap import dedent
    import color as C
    from pdb import set_trace as xx 
    if 1:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    # Raw data for the script
    #
    # Note:  None of these files contain any information about how they are
    # licensed, so I am assuming they are available for public use.  I have
    # attributed their sources, given their download dates, and the MD5
    # hashes of the files I downloaded.  If this use is improper, please
    # notify me at the above email address.
    #
    # Encoding:  these files were converted to plain UTF-8 files.  The CSV
    # files had the BOM and carriage returns deleted and the
    # Metalworking_index_2000.txt file was converted from ISO-8859 using
    # 'iconv -f iso-8859-1 -t utf-8'.  After the encoding changes, I
    # replaced the following codepoints with their 7-bit ASCII equivalents:
    # U+00c4, U+2013, U+2018, U+2019, U+201c, U+201d, U+2026.  This ensures
    # that this file is 7-bit clean.
    #
    # File:  Metalworking_index_2000.txt, Downloaded from the link at
    # http://machinistindex.com/html/metalworking_index.html on Wed 19 Feb
    # 2020 12:33:16 PM.  The actual link used is
    # http://machinistindex.com/Metalworking_index_2000.txt.  MD5 hash is
    # 5e4ac70ff2eb81007e3c32b7b6fb7d57.
    # NOTE:  these links are defunct as of 6 Jul 2021.
    mi = dedent('''

    ! Joe Landau's Metalworking Index 2000 Edition, covering 
    ! "Home Shop Machinist" through 1999
    ! "Projects in Metal" magazines through-1998
    ! "Machinist's Workshop" magazine, beginning 1999
    ! Issues numbered 9-32 of Model Engineers' Workshop magazine
    ! The Machinist's Bedside Reader (TMBR) #1, 2, and 3, by Guy Lautard 
    ! "Hey Tim, I gotta tell ya..." (HTIM), by Guy Lautard 
    ! Index entries for the magazine articles are the article titles. 
    ! The text of the articles was not indexed.
    ! Index entries for HTIM and TMBR are derived from 
    ! Guy Lautard's Comprehensive Index, with permission.
    ! 
    ! This is an index only, and does not contain the articles themselves.
    ! Please contact the publishers for copies of the magazines and books:
    ! For HSM and PiM:
    ! Village Press, 2779 Aero Park Drive, Traverse City, MI 49686 USA
    ! For HTIM and TMBR:
    ! Guy Lautard, 2570 Rosebery Avenue, West Vancouver, B,.C. Canada V7V2Z9
    ! For MEW
    ! Nexus Special Interests, Nexus House, Azalea Drive,
    !Ciconv  Swanley, Kent BR8 8HY, England
    ! 
    ! Many of the articles from HSM and PiM have been reprinted by Village Press 
    ! in book form. An index to these volumes has been compiled by Peter Brooks. 
    ! This and much other valuable information is available at the Metalworking FAQ, 
    ! at http://w3.uwyo.edu/~metal/
    !
    ! Many thanks to Jim Kirkpatrick for suggestions and proofreading, and for the FAQ.
    
    ! Compiled by Joe Landau
    ! jrl@versaform.com
    ! Even Jove Nods
    !
    ! Key:
    ! HSM-Home Shop Machinist
    ! M&M -PiM Metals & More
    ! MEW-Model Engineers' Workshop
    ! MN-PiM Margin Notes
    ! MW-Machinist's Workshop
    ! PiM-Projects in Metal
    ! HTIM-"Hey Tim, I gotta tell ya..."
    ! TMBR#n-The Machinist's Bedside Reader #1, 2, or 3
    !************************************************************************************************

    "Floating" End Mill Sharpener Part 1, 2	DUCLOS, PHILIP	HSM'87:S/O20,N/D38
    "Quickie" Reamer, A	HOFF, MIKE 	MW Jun. 99, 41
    "Slow Poke" Small Keyway Broach	DUCLOS, PHILIP	HSM'85:S/O22
    "Truing Your Action and Installing a New Barrel";Video Reviews	LAUTARD, GUY	HSM'96:M/J 20
    "Very Much Improved" Qttorn Tool and Cutter Grinder, A Part 1	MUELLER, WALTER B.	HSM'99:N/D 30
    "Whatzit" Engine, Parts 1-2	DUCLOS, PHILIP	HSM'88:J/A20,S/O18
    "White Glove" Solvent Change		HSM'91:M/A15
    "Zappo" the Swarf Lifter	SEXTON, TERRY	PiM-Dec.'96, 12
    $100 Digital Readout	HANLEY, DICK	HSM'89:J/F39
    $20 Drip Coolant System, The	NOLAN, PETER	PiM Apr. '98 24
    $50 Power Table Feed, A	HALLIGAN, H.	PiM-Jun.'96, 20
    ...And Again		HSM'88:M/J11
    ...Or Stand On Your Head		HSM'84:J/F16
    "As I remember" (S. P. Timoshenko 's autobiography)	Lautard, Guy	TMBR#3:51
    "Cratex" abrasive-in-rubber	Lautard, Guy	TMBR#2:131
    "Helix" Gear Hobbing Machine,The	SEXTON, TERRY	PiM Dec. '98 20 
    "Hubers" cutting oil	Lautard, Guy	TMBR#3:102
    "Jet" propane torch head	Lautard, Guy	TMBR#1:51
    "Mouse Milk" penetrating and lubricating oil	Lautard, Guy	TMBR#3:237
    "Pull dowels" used to machine an angle plate	Lautard, Guy	TMBR#2:101
    "Quick" knurls	Lautard, Guy	TMBR#1:63-64
    "Royal" machine mount/leveling pads	Lautard, Guy	TMBR#3:71
    "Royal" vise jaw liners	Lautard, Guy	TMBR#3:70
    "Victorian" Engine, A, Part 5	DUCLOS, PHILIP	HSM'98:J/F 48
    1" Reverse Arbor, A	HAUSER, JAMES W.	MW Dec. 99, 37
    1/4 degree vernier	Lautard, Guy	TMBR#2:8
    10" "Super Colossal" Fly Cutter	DUCLOS PHILIP	HSM'86:M/A32
    15/16 hole vernier	Lautard, Guy	TMBR#1:42
    3 Phase In The Workshop	BOUCHER	MEW#9,46
    3 tapping hints	Lautard, Guy	TMBR#2:125
    3" Parrott Field Rifle Parts I-III	GREEN, WILLIAM F	HSM'82:J/F28,M/A29,M/J36
    36" Brake, A	McKNIGHT, JAMES	PiM Jun. '98 24
    40-Ton Hydraulic Arbor Press Parts 1, 2	JONES, BRUCE	HSM'86:M/J28,J/A38
    4-way Toolpost -- Peatol lathe	GRAY	MEW#26,14
    5C Collet Adapter for the Lathe, A	JOHNSON, D. E.	HSM'97:J/F 26 
    5C Collet Closer, A	VANDUYN, LARRY	PiM-Apr.'90,12
    64th Int. Model Engineer Exhibition	SHEPPARD	MEW#29,49
    75% depth of thread rule	Lautard, Guy	TMBR#1:18
    900 point slot drills	Lautard, Guy	TMBR#1:169
    A "Showpiece" Challenge	DUCLOS, PHILIP	HSM'85:J/F44
    A "Skypod,"	WILSON, GLENN L.	PiM-Feb.'91,4
    A "Geometric solid" from sheet copper, for a lamp	Lautard, Guy	TMBR#3:206
    A "thin piece" collet	Lautard, Guy	TMBR#2:129
    A 20-Ton Hydraulic Press You Can Build	JONES, RODNEY D	HSM'83:M/A39,M/J39
    A 32-Pounder Seacoast Cannon	GREEN, WILLIAM F.	PiM-Dec.'88,4
    A 5C Collet Fixture Tailstock	ACKER, STEVE	PiM-Oct.'91,13
    A background shading punch	Lautard, Guy	TMBR#3:247
    A background shading punch	Lautard, Guy	TMBR#3:247
    A backplate fitting idea for 3-jaw chucks	Lautard, Guy	TMBR#3:65
    A Bit of A Tip		HSM'84:M/A16
    A Bit of Inspiration	LAUTARD, GUY	HSM'84:N/D34
    A Bit of Inspiration: David Kucer, Miniaturist	RICE, JOE	HSM'92:M/A36
    A Bit of Inspiration: Miniature Machine Shop		HSM'88:M/J14
    A Bit of Inspiration: Sculpting with Plastics		HSM'88:J/F16
    A Bit of Inspiration: The Work of John Crunkleton	CRUNKLETON, JOHN	HSM'96:J/A24
    A block to produce 3 common angles from a sine bar	Lautard, Guy	TMBR#3:98
    A boring bar for reboring large cylinders	Lautard, Guy	TMBR#2:96
    A Built-in Drill Guide	DEAN, JOHN	HSM'83:S/O39
    A Camera-Tripod Attachment	MARX, ALBERTO	HSM'88:M/A20 
    A centerfinder	Lautard, Guy	TMBR#2:104
    A Center-mounted Drill	McHENRY, ROGER	HSM'88:S/O30 
    A cheap master gage to test taper shanks against	Lautard, Guy	TMBR#2:92
    A collet chuck system for your lathe	Lautard, Guy	TMBR#3:11, TMBR#2:39
    A Compound and Ram Tailstock	CLARKE, THEODORE M.	HSM'83:S/O30
    A copper pipe soldering trick	Lautard, Guy	TMBR#2:150
    A deluxe overhaul for keyless chucks	Lautard, Guy	TMBR#3:119
    A Digital Readout For Your Vertical Milling Machine	LAUTARD, GUY	HSM'83:J/A44
    A dowel puller	Lautard, Guy	TMBR#1:67
    A Drafting Table You Can Build For Less Than $20		HSM'83:J/F32
    A Drill Press Improvement	ESTY, F BURROWS	HSM'82:J/A48
    A Feed Lever for a 10-K	BENNETT, NORMAN	HSM'88:M/J?4
    A Few Thoughts on Drill Presses and Tool Grinders	McLEAN, FRANK A	HSM'82:M/J39
    A Few Tips on Drilling on a Drill Press or a Vertical Milling Machine	McLEAN, FRANK	HSM'83:J/A60
    A Fireside Chat About Lathe Chucks	McLEAN, FRANK	HSM'83:N/D54
    A Fireside Chat About Lathe Tools	McLEAN, FRANK	HSM'83:J/F46
    A Fireside Chat About Lathes	McLEAN, FRANK A	HSM'82:S/O48
    A Firing Model Napoleon Field Gun Part 1-4	GREEN, WILLIAM F.	HSM'85:J/A26,S/O38,N/D44; HSM'86:J/F31
    A fixture for accurate taper turning with the topslide	Lautard, Guy	TMBR#3:16
    A fixture for rounding the ends of small parts	Lautard, Guy	TMBR#2:107
    A fixture to guide the piercing saw	Lautard, Guy	TMBR#3:240
    A flexible pusher for the milling vise	Lautard, Guy	TMBR#3:70
    A Fly Cutter Arbor That Is Different		HSM'88:J/A14
    A foot powered piercing saw	Lautard, Guy	TMBR#3:240
    A gagemaker's square	Lautard, Guy	TMBR#2:64
    A Gas Welding Tip	METZE, R.W.	HSM'82:S/O35
    A Grinding Rest for Precise Tools, Parts 1, 2	KOUHOUPT, RUDY	HSM'90:M/J40,J/A48
    A Handy Combo-Mallet and Knockout		HSM'84:M/J18
    A handy deburring tool made from a file	Lautard, Guy	TMBR#3:72
    A handy decimal equivalent chart	Lautard, Guy	TMBR#2:162
    A handy lathe tool tray	Lautard, Guy	TMBR#2:132
    A hanger for shop drawings	Lautard, Guy	TMBR#2:145
    A hanging wire version	Lautard, Guy	HTIM:5
    A hole location device for clockmakers	Lautard, Guy	TMBR#2:22
    A Home Foundry Parts I-III	TIMM HAROLD	HSM'82:M/A18,M/J23,J/A34
    A Homemade Disk Sander	SAPORITO, TOM	HSM'82:S/O36
    A Homemade Rack for your Files	WALKER, RALPH T.	HSM'83:J/A47
    A jar opener	Lautard, Guy	TMBR#2:143
    A knocking block	Lautard, Guy	TMBR#2:112
    A lamp made from brass fittings	Lautard, Guy	TMBR#3:206
    A Large Steady Rest from the Scrap Pile	BARBOUR, J. O., Jr.	HSM'84:M/J35
    A lathe center turned in place	Lautard, Guy	TMBR#3:108
    A lathe mandrel hand crank	Lautard, Guy	TMBR#2:112
    A Lathe Milling Adaptation, Part 1, 2, 3	KOUHOUPT, RUDY	HSM'89:M/J47,J/A56,S/O52
    A lathe tracing attachment	Lautard, Guy	TMBR#2:108
    A Little Bit of Everything	WOLLENBERG, GALE	HSM'82:M/A42
    A Little More Leverage		HSM'83:J/A12
    A low cost surface plate	Lautard, Guy	TMBR#1:8
    A low cost table saw	Lautard, Guy	TMBR#3:190
    A Luxo lamp base with rotating electrical pick-up	Lautard, Guy	TMBR#3:26
    A Make-Do Surface Grinder Parts I, II	WALKER, RICHARD B.	HSM'84:S/O24,N/D24
    A Makeshift Vise Stop		HSM'88:J/A15
    A master gage for Morse taper shanks	Lautard, Guy	TMBR#1:17
    A means of holding flat work in the vise	Lautard, Guy	TMBR#2:15
    A Micrometer Faceplate Attachment, Parts 1-2	KOUHOUPT, RUDY	HSM'88:M/A50,M/J39
    A Micrometer Stop Nut	McLEAN, FRANK A	HSM'88:J/A46 
    A Mill-drill Lubrication Upgrade     	ARMSTRONG DENNIS 	MW Oct. 99, 8
    A Mill-Drill Stand	DULLUM, LAWRENCE J.	HSM'88:M/A28
    A Milling Machine for Your Lathe Parts I-III	SNYDER, JOHN	HSM'84:M/J36,J/A44,S/O36
    A mini 4-jaw chuck	Lautard, Guy	TMBR#3:60
    A Mini-course in Orthographic Drawing Techniques, Parts 1-4	WASHBURN, ROBERT A.	HSM'87:J/F50,M/A47,J/A54,M/J42
    A model vise	Lautard, Guy	TMBR#3:206-207
    A Modified "Wedge" Oscillating Engine Parts I-III	CUTLER, RICHARD F	HSM'82:J/F18,M/A24,M/J26
    A multi-diameter edge finder adaptor	Lautard, Guy	TMBR#2:128
    A napkin holder	Lautard, Guy	HTIM:49
    A New Cutoff Tool	ESTY, F. BURROWS	HSM'88:M/J23
    A New Rotary Table	McLEAN, FRANK A	HSM'88:M/J43 
    A New Year Message		HSM'84:N/D12
    A nice clean-looking clean drawer pull	Lautard, Guy	HTIM:32
    A Plastic Dip Pot	DONDRO, CHARLIE	HSM'88:J/F40
    A Pocket Size Camera Tripod	LAUTARD, GUY	HSM'83:S/O45
    A Practical Ball-Turning Tool for Atlas 12" & Similar Lathes	LANDWEHR, JOHN G	HSM'82:J/F33
    A Practical Suds Pump	PASSINO, KEITH E.	HSM'84:M/A28
    A Puzzle	REICHART, BILL	HSM'87:M/A32
    A quick detach sine fixture for your milling vise	Lautard, Guy	TMBR#2:80
    A Quick Tumbler Gear Reversal Mechanism	MYERS, TED	HSM'94:M/A44
    A Quick-change Tool Post System Parts 1-4	TORGERSON, RICHARD	HSM'93:J/A36,S/O39,N/D39;HSM'94:J/F24
    A Quick-index Drill Stand		HSM'88:M/J12
    A reference straightedge from plate glass	Lautard, Guy	TMBR#2:12
    A replica Lunkenheimer whistle	Lautard, Guy	TMBR#2:134
    A rust preventative from Stockholm tar etc.	Lautard, Guy	TMBR#3:77
    A Sensitive Level		HSM'84:N/D16
    A Sensitive Level	KELLY, HOWARD	HSM'88:J/F20
    A set-over tailstock center for taper turning	Lautard, Guy	TMBR#2:89-92; TMBR#3:13
    A severe first test for squareness	Lautard, Guy	TMBR#2:14-15
    A Shield Against Corrosion		HSM'88:J/A13
    A shop made centerpunch	Lautard, Guy	TMBR#3:105
    A shop made surface grinder	Lautard, Guy	TMBR#2:59, 60
    A shop-made bender	Lautard, Guy	TMBR#3:56
    A shop-made cylindrical square	Lautard, Guy	TMBR#2:18
    A shop-made hacksaw	Lautard, Guy	TMBR#2:100
    A Simple Die Filer	HOLEN, D W	HSM'83:J/A48
    A Simple Holddown Device	METZE, R.W.	HSM'83:S/O53
    A Simple Lathe Dog	SCHARPLAZ, JAMES D., P. E.	HSM'83:N/D46
    A simple stamping fixture	Lautard, Guy	TMBR#2:109
    A slitting saw arbor	Lautard, Guy	TMBR#1:62; TMBR#2:128
    A Small Demagnetizer/Magnetizer	LONGLEY, FRANKLIN A.	HSM'87:M/A25
    A Small Melt Furnace,	ROY, BILL	HSM'88:M/A22 
    A Special Breed	BARBOUR, J. O.	HSM'88:S/O40
    A spillproof cutting oil bottle	Lautard, Guy	TMBR#3:227
    A Stirling-powered Tractor, Parts 1-7	KOUHOUPT, RUDY	HSM'97:J/F 44, M/A 28, M/J 44, J/A 54, S/O 47 N/D 46, HSM'96:N/D24
    A Sturdy Workbench	McLEAN, FRANK A	HSM'82:M/A36
    A tailstock die holder	Lautard, Guy	TMBR#2:103
    A tap starting block	Lautard, Guy	TMBR#3:74
    A Taper Attachment for Your Machines 5 Lathe	JONES ROD	HSM'82:J/A44
    A Temporary Aluminum Furnace	DUCLOS, PHILIP	HSM'84:S/O44
    A Thin Slice of V-Block	DEAN, JOHN	HSM'84:J/A63
    A Thought About Turning		HSM'88:S/O13
    A Thread Tooling System and Wiggler for the Lathe	JOHNSON, D. E.	HSM'92:N/D18
    A tip on using calipers	Lautard, Guy	TMBR#3:106
    A Tool Bit Index		HSM'88:M/A15
    A tool for co-ordinate layout work in the mill	Lautard, Guy	TMBR#2:127
    A Toolmaker's Block	Lautard, Guy	TMBR#2:19
    A Toolpost Grinder For Your Machinex 5 or Unimat Lathe	JONES ROD	HSM'82:M/J10
    A Toolpost Grinder	DEAN, JOHN	HSM'84:J/A18
    A Toolpost Problem Solver	DEAN, JOHN	HSM'84:J/A55
    A true square	Lautard, Guy	TMBR#2:18
    A tube flaring tool	Lautard, Guy	TMBR#2:126
    A use for worn or broken hacksaw blades	Lautard, Guy	TMBR#2:131
    A V-Block Drill Guide	METZE, R.W.	HSM'83:M/A38
    A Versatile, Quick Change Bench Grinder	DEAN, JOHN	HSM'82:N/D33
    A vise accessory for holding flat work	Lautard, Guy	TMBR#2:97
    A wax wire extruder	Lautard, Guy	TMBR#3:76
    A wire hoop bender	Lautard, Guy	TMBR#3:56
    A wood lathe	Lautard, Guy	TMBR#1:196
    About Dimensions	HAMILL, JAMES	HSM'83:J/A24
    Abrasive Belt Slitter, An	SMELTZER, PAUL	PiM-Aug.'95 28
    Accessories for a Rotary Table Parts 1-3	STRAIGHT, J. W.	HSM'90:J/A28,S/O26,N/D33
    Accessories for a Unimat	HAUSER, JAMES W.	PiM Dec. '97 24
    Accurate "U" Bolts		HSM'87:M/J14
    Accurate angles	LAMMAS	MEW#25,20
    Accurate Chucking		HSM'91:J/A13
    Accurate division -- simple tools	HARVEY	MEW#28,21
    Accurate Drilling Through Bolts		PiM-Apr.'89,24
    Accurate Location to Holes or Edges	EVANS, JIM	PiM-Feb.'94,3
    Accurate Quill Depth Control for Mill/Drills	BODMER, JOHN A.	HSM'89:N/D24
    Accurate Vise Alignment	McLEAN, FRANK	PiM-Jun.'94,MN
    Adapter for a Boring Head	VREELAND, DON H.	HSM'92:J/F39
    Adapting a Palmgren Drill Press Vise for Use on Sherline Machines	ATKINSON, CHARLES T.	PiM-Oct.'95 31
    Adapting the Myford for Hand Turning and 10mm Collets	SMITH, W. R.	HSM'92:M/J26
    Adapting the Sherline for Wheel Cutting and Pinion Making, Parts 1-2	SMITH, W. R.	HSM'96:M/A 24 M/J 36
    Adding A Flywheel To Milldrill	AMOS	MEW#19,28
    Adding fine feed -- dig. Vernier	LOADER	MEW#27,48
    Adding flywheel to mill/drill	WILTON	MEW#23,33
    Adding Muscle to Your 9 x 20" Bench Lathe	CHLAPECKA, RICHARD	PiM Jun. '98. 36
    Additions to the Quorn tool and Cutter Grinder Parts 1, 2	MUELLER, WALTER B.	HSM'98:M/J 46, J/A 46
    Adjustable Angle Plate	GEISLER, FRED	PiM-Dec.'95 34
    Adjustable Angle Plate	SISSON, LANE	PiM-Feb.'90,10
    Adjustable Cross-slide Nut, An	PETERSEN, EUGENE E.	PiM Apr. '98 27
    Adjustable Lathe Stop for Under $15	TITUS, DON	HSM'97:J/A 37
    Adjustable Parallels	DUCLOS, PHILIP	HSM'85:M/A24
    Adjustable Pop-stop for the Myford Lathe	YOUNG, MARSHALL R.	PiM-Jun.'91,22
    Adjustable Pop-stop	YOUNG, MARSHALL	PiM-Aug.'89,15
    Adjustable stop bar -- milling mc	COCKSEDGE	MEW#32,12
    Adjustable Traveling Dial Indicator Rod	GASCOYNE, JOHN	HSM'86:J/F25
    Adjustable Try Squares	WRIGHT, TED	PiM-Jun.'88,8
    Adjustable Vise Spacer		HSM'83:S/O20
    Advantage of Three-phase	FRENCH, DICK	HSM'96:M/A 19
    Advice on getting ahead	Lautard, Guy	TMBR#1:181
    Aligning A Lathe	MORRIS	MEW#9,60
    Aligning a Lathe	WELLCOME, STEVE	PiM-Aug.'95 34
    All That Glitters	TAYLOR	MEW#18,25
    All-around Access	GASCOYNE, JOHN	HSM'98:M/A 22 
    Almost a Product Review	NOLAN, PETE	HSM'96:S/O 23
    Alternate Clamping Devices Parts 1-2	HOFFMAN, EDWARD G.	HSM'92:S/O40,N/D34
    Alternative to Layout Dye	THOMPSON, LARRY R.	PiM-Feb.'96, 43
    Alternator test bench	Lautard, Guy	TMBR#3:109
    Aluminum Fundamentals, Part 1	GENEVRO, GEORGE	HSM'93:J/F 26
    Aluminum Fundamentals, Part 2 Temper Designation	GENEVRO, GEORGE	HSM'93:M/A30
    Aluminum made 3000 years ago in China	Lautard, Guy	TMBR#3:210
    Aluminum Raw Stock Source	BROWN, KENNETH G	HSM'92:M/A15
    Aluminum soldering	Lautard, Guy	TMBR#1:103; HTIM:48
    Aluminum welding rod	Lautard, Guy	TMBR#2:122
    Always Remove or Secure Jewelry When Operating Any Shop Equipment	HOFFMAN EDWARD G	HSM'82:J/A17
    Always Wears Protective Glasses When Operating Any Shop Equipment	HOFFMAN EDWARD G	HSM'82:M/J12
    Amateur's Lathe, The		HSM'86:N/D44
    An Accessory Table for Your Lathe	METZE, R.W.	HSM'82:S/O52
    An Accurate Taper Attachment for Under $5.00	BARBOUR, J. O., Jr.	HSM'86:M/A20
    An Accurate Vise for the Milling Machine	KOUHOUPT, RUDY	HSM'91:N/D18
    An Adjustable Bushing	KOLAR, GEORGE	PiM-Apr.'94,MN
    An adjustable workstop for the lathe spindle hole	Lautard, Guy	TMBR#3:75
    An Affordable Mill-drill Power Drive, Part 1-5	COX, ED 	MW Apr. 99, 24, MW Jun. 99, 28, Aug. 99, 32, Oct. 99, 30, Dec. 99, 48
    An aid to setting up work on a faceplate	Lautard, Guy	TMBR#3:20
    An Ancient Indexing Method		HSM'85:M/J15
    An Assist from the Forge	HANCOCK, CLIFFORD	HSM'88:J/A50
    An attractive etched finish for aluminum	Lautard, Guy	TMBR#2:115
    An Automatic Parallel	KOUHOUPT, RUDY	HSM'84:M/A36
    An Automatic Punch	DUBOSKY, EDWARD	PiM-Feb.'93,10
    An easy way to make a hex socket screw	Lautard, Guy	TMBR#2:95
    An Elevated or Auxiliary Lathe Spindle Part 1-2	McLEAN, FRANK A.	HSM'96:S/O34 N/D32
    An Expanding Mandrel	PETERKA, W. PETE	HSM'83:J/A30
    An old timer remembers flat belts & firm joint calipers	Lautard, Guy	TMBR#3:21
    An oversize paper clip	Lautard, Guy	TMBR#3:54-55
    An ultra sensitive dial indicator base	Lautard, Guy	TMBR#2:83
    Anaerobic Adhesives for Machinery	KRAEMER, TIM	PiM-Jun.'96, 32
    Ancient Chinese Hoist		HSM'87:M/J15
    And Now For Something Completely Different	FRIESTAD, R. W.	HSM'93:M/A44
    Anecdotes: A 7/8" hole in a 3/4" shaft	Lautard, Guy	TMBR#3:97
    Anecdotes: A mechanical El Dorado	Lautard, Guy	TMBR#2:156
    Anecdotes: Al Zueff makes a prop shaft	Lautard, Guy	TMBR#2:154
    Anecdotes: Alice loses her shirt	Lautard, Guy	TMBR#2:153
    Anecdotes: An in situ shaft repair	Lautard, Guy	TMBR#1:192
    Anecdotes: Coal miner s cure for headaches	Lautard, Guy	TMBR#1:195
    Anecdotes: Coincidence Maximus	Lautard, Guy	TMBR#3:234
    Anecdotes: Delphon and the Adding Machine	Lautard, Guy	TMBR#1:189
    Anecdotes: Helping the war effort	Lautard, Guy	TMBR#1:185
    Anecdotes: How not to get a welding ticket	Lautard, Guy	TMBR#1:186
    Anecdotes: How to impress your mother-in-law	Lautard, Guy	TMBR#1:193
    Anecdotes: How to remove a chuck that is jammed on tight	Lautard, Guy	TMBR#1:194
    Anecdotes: I was so happy I could have cried	Lautard, Guy	TMBR#2:161
    Anecdotes: Lebow's shop mishaps	Lautard, Guy	TMBR#3:228
    Anecdotes: One way to ruin a lathe	Lautard, Guy	TMBR#1:194
    Anecdotes: Quitting time	Lautard, Guy	TMBR#3:231
    Anecdotes: Rocky takes a holiday	Lautard, Guy	TMBR#2:151
    Anecdotes: Sharpening razor blades	Lautard, Guy	TMBR#1:186
    Anecdotes: Sleepy apprentice boy	Lautard, Guy	TMBR#1:190
    Anecdotes: Snow, fire and speedometer cables	Lautard, Guy	TMBR#3:102
    Anecdotes: Stealing the trade	Lautard, Guy	TMBR#1:184
    Anecdotes: We lost that one sheave completely	Lautard, Guy	TMBR#2:152
    Anecdotes: Where gears come from	Lautard, Guy	TMBR#1:195
    Angle plates for workholding	Lautard, Guy	TMBR#1:39
    Angles, division of circles, etc	Lautard, Guy	TMBR#2:1
    Angular Measurement	HOFFMAN, EDWARD G.	HSM'85:M/A20,M/J16 
    Anodizing aluminum	Lautard, Guy	TMBR#1:197
    Another Fly Cutter	FELLER, ERNEST T.	HSM'92:J/A57
    Another Index System for the Lathe	THOMPSON, JACK	PiM-Aug.'94,16
    Another Mill-drill Adventure	HOKE, GEORGE F.	HSM'97:S/O 58
    Another Power Feed Drive for a Mill	METZE, BOB	PiM-Aug.'96, 19
    Another Quorn	GOODEN	MEW#32,17
    Another Use	VANICE, L. L.	PiM-Aug.'94,3
    Another Viewpoint	LAMANCE, THOMAS 	MW Oct. 99, 55
    Another Vise Jaw Idea	BRUCE, FRED	HSM'94:J/F16
    Another Way to Turn Offset Diameters	BRUCE, FRED	PiM Oct. '98 47
    Anti-fatigue mats	Lautard, Guy	TMBR#1:176
    Antique Machine Tool Museum		HSM'88:J/A12
    Antirotation Drill Holder for the Lathe Tailstock	JOHNSON, D. E.	PiM-Dec.'93,30
    Anti-seize compound used in a milling job	Lautard, Guy	HTIM:21
    Anvil Chorus		HSM'86:N/D12
    ApplePly	Lautard, Guy	TMBR#3:192
    Approximations of pi	Lautard, Guy	TMBR#3:10
    Arbor Day		HSM'83:S/O18
    Arbor Press		HSM'89:N/D14
    Arbor Press	IRVIN, H.	PiM Aug.'97 12
    Arc Stabilizer		HSM'87:N/D17
    Art and design sense	Lautard, Guy	TMBR#3:242
    Art of Soldering, The	HUNT, DONALD	HSM'87:S/O56
    Asian Connection, The	SEXTON, TERRY	PiM-Dec.'93,24
    Assembly		HSM'84:J/F46
    Assembly	STRASSER, FREDERICO	HSM'83:N/D48
    Atkinson Cycle Engine	TEAGUE, ARNOLD L	PiM-Feb.'96, 4
    Atlas Tailstock Modification	JONES, BRUCE	HSM'96:N/D 55
    Attaching the Chuck	PEASE, F D.	HSM'99:M/J 24
    Attachments For The Hobbymat	FORD	MEW#12,28
    Aushalser - a German made pipe-T pulling tool	Lautard, Guy	TMBR#3:81
    Automated Coolant Applicator, An  	WILSON, GLENN L.	MW Dec. 99, 8
    Automatic Carriage Stop for a 6' Atlas Lathe	BADGER, EDWARD	PiM Apr. '98 20
    Automatic Carriage Stop	LEBARON, R. P.	PiM-Apr.'88,15
    Automatic Feed Adapter for a Mill/drill	REICHART, BILL	PiM-Dec.'95 33
    Automatic Oiler	LAMANCE, THOMAS	PiM-Apr.'94,3
    Auxiliary Outboard Motor Bracket	GREEN, WILLIAM F.	HSM'89:S/O41
    Auxiliary Tailstock Center		PiM-Apr.'89,3
    Avoid Injury		PiM-Apr.'90,3
    Avoiding Broken Gear Belts	LANGFORD, FRANCIS	HSM'94:S/O19
    Avoiding Hazards		PiM-Apr.'89,3
    Avoiding Lathe Dog Slips		HSM'90:S/O15
    Avoiding Rust In The Toolbox		PiM-Apr.'88,24
    Avoiding tap breakage	Lautard, Guy	TMBR#3:151
    Babbitt Bearings, Q&A		HSM'82:N/D11
    Back scratcher - the world's best	Lautard, Guy	TMBR#3:225
    Back To College	HALL	MEW#12,34
    Back Tool Post, A	YOUNG, BARRY	MW Dec. 99, 44
    Backlash (Re Added Flywheel)	READERS	MEW#19,31
    Backlash	READERS	MEW#11,72
    Backlash	READERS	MEW#18,59
    Backwards look at gear cutting	UNWIN	MEW#31,65
    Balanced Ball Handles	SEXTON, TERRY	HSM'97:N/D 50
    Balancing a Grinding Wheel	CHRISTOPHERSON, A. M.	HSM'94:J/F36
    Balancing grinding wheel flanges	Lautard, Guy	TMBR#2:114
    Ball ended centers from Ford pushrods	Lautard, Guy	TMBR#3:13
    Ball Turning in the Mill	BENNETT, NORMAN H	HSM'92:M/J44
    Ball turning techniques	Lautard, Guy	TMBR#1:72-79; TMBR#3:24, 174
    Ball turning tool	THOMAS	MEW#26,52
    Ballizing holes for high finish & high precision	Lautard, Guy	TMBR#2:132
    Balls & Bull Noses	LAUTARD, GUY	HSM'83:S/O40,N/D42
    Baltic Birch plywood	Lautard, Guy	TMBR#3:192
    Band Saw Alignment Tool	PIAZZA, JAMES D.	MW Dec. 99, 38
    Band Saw Base, A	MASSICOTTE, PIERRE	MW Dec. 99, 18
    Band Saw Blade Fixture	ASHCRAFT, RAY	HSM'98:S/O 24
    Band Saw Blade Grinder	LINCOLN, W. A. "LINK"	PiM-Feb.'95 4
    Band Saw Blades		HSM'88:M/A13
    Band Saw Conversion		HSM'89:J/F12
    Band Saw Fixture	DRAYSON, D. A.	HSM'97:S/O 46
    Band Saw Improvement	TALBOT, BRYAN E.	HSM'97:J/F 23 
    Band Saw Repair	HESSE, JAMES	PiM-Jun.'94,MN
    Band Saw Slow Speed Attachment, A Parts 1, 2	McLEAN, FRANK A.	HSM'90:M/A40,M/J43
    Band Saw Speed Reducer, A	NELSON, BOB	PiM-Feb.'88,22
    Band Saw Transmission	TORGERSON, RICHARD	HSM'90:J/A18
    Bandsaw blade speeds	Lautard, Guy	HTIM:42; TMBR#3:184
    Bandsaw Vice Improvement	HALL	MEW#18,38
    Base for a Band Saw	KOUHOUPT, RUDY	HSM'94:J/F46
    Basement Rust	AMBROSINO, MICHAEL M.	HSM'92:N/D40
    Baseplate for a Dividing Head, A	McLEAN, FRANK	HSM'86:J/A50
    Basic Home Shop Tool: The Lathe	WASHBURN, ROBERT A.	HSM'83:S/O60
    Basic Industrial Electrical Control	COHON, HAROLD G.	HSM'97:J/A 40
    Basic Metal Finishes	HARRILL, JAMES B.	PiM-Jun.'88,3
    Basics of Locating, Part 1, 2		HSM'89:S/O50,N/D52
    Basketball inflator needle for tap cutting removal	Lautard, Guy	TMBR#3:71
    Bastion of the Belts	JONES, DAVID	HSM'85:M/J26
    BB introduced	Lautard, Guy	TMBR#3:4
    Bead blasting & other ways of finishing aluminum	Lautard, Guy	HTIM:23
    Beam compass: Grinding the flat on the beam	Lautard, Guy	TMBR#3:122-126
    Bearing Remetalling	FETTLER	MEW#13,38
    Bed Extension for Atlas and Craftsman Lathes	METZE, ROBERT W	PiM-Aug.'91,18
    Behavior of slitting saws, etc.	Lautard, Guy	TMBR#1:55-61
    Bell Chuck for Your Lathe, A	MCLEAN, FRANK A.	HSM'92:J/A54
    Belt Replacement (Tips & Tricks)	STAHLER, EARL	PiM-Jun.'95 42
    Belt Replacement		PiM-Aug.'93,3
    Belt Replacement	STAHLER, EARL	PiM-Aug.'93,3
    Belt Sander Conversion		PiM-Feb.'91,3
    Belt Sander	HEDIN, R. S.	PiM-Apr.'88,20
    Belt Sander	McKNIGHT, JAMES	PiM Oct. '98 17
    Bench Block	ACKER, STEVE	HSM'89:N/D29
    Bench Grinder Safety	HOFFMAN, EDWARD G.	HSM'83:M/A27,M/J26,J/A16
    Bench mounted support -- lathe	WALTERS	MEW#22,20
    Bend Allowances	HOFFMAN, EDWARD G.	HSM'83:J/A26
    Bending Strip Material	HARRIES	MEW#19,18
    Benelex - a harder version of Medite	Lautard, Guy	TMBR#3:175
    Benelex	Lautard, Guy	TMBR#3:191
    Bengalis' (Tony) writings in Sport Aviation	Lautard, Guy	TMBR#3:56
    Bernzomatic torches etc.	Lautard, Guy	TMBR#1:51
    Better Boring Bars	LAMANCE, THOMAS 	MW Aug. 99, 58
    Better File Handles	PATRICK, BOB	PiM-Dec.'89,8
    Better Protractor, A		HSM'90:S/O14
    Better Visibility		PiM-Oct.'91,3
    Between-centers boring bars	Lautard, Guy	TMBR#2:94
    Bevel protractor used to set up a reamer for stoning	Lautard, Guy	TMBR#3:159
    Big collets for the S7 lathe	CANNER	MEW#31,58
    Bill's big firm joint calipers	Lautard, Guy	TMBR#3:20
    Bill's donkey engine & spar tree logging blocks	Lautard, Guy	TMBR#3:36-47
    Birth of the large machine tool	UNWIN	MEW#25,55
    Bit of Inspiration, A Machining Skills Pay Off	GANOE, WILLIAM H.	HSM'97:M/A 52 
    Bit of Inspiration, A	HOLEN, D. W.	HSM'87:N/D22
    Bits & bobs -- universal bandsaw	CLARKE	MEW#24,22
    Black or pink granite?	Lautard, Guy	TMBR#3:106
    Black-it review update	HALL	MEW#28,33
    Black-it	HALL	MEW#22,57
    Blacksmith Extraordinaire, A	BARBOUR, J. O. JR	HSM'91:M/A48
    Blacksmithing in the Twenty-first Century	SMITH, DAVID	PiM-Apr.'94,26
    Blade guides for bandsaw blades	Lautard, Guy	HTIM:42
    Blank end taper shank arbors	Lautard, Guy	TMBR#2:89
    Blueing cutters while hand filing the reliefs	Lautard, Guy	TMBR#3:110
    Blueing of steel with muriatic acid	Lautard, Guy	TMBR#3:175
    Blueing Steel	LAUTARD, GUY	HSM'87:S/O41
    Blueing steel	Lautard, Guy	TMBR#1:34, 171,
    Blueing steel: Black velvet blue job for gun parts	Lautard, Guy	TMBR#3:137
    Blueing steel:Electroless nickel plating	Lautard, Guy	TMBR#3:139
    Blueing steel:Etching off a too high polish with nitric acid	Lautard, Guy	TMBR#3:138
    Blueing steel:How to do a durable black "Parkerized" finish	Lautard, Guy	TMBR#3:139
    Blueing steel:Numrich 44-40 gun blue	Lautard, Guy	TMBR#3:138
    Blueing steel:Swedish recipe	Lautard, Guy	TMBR#3:103
    Blueing steel:with Chem-Tech cutting fluid	Lautard, Guy	TMBR#3:175
    Blueing steel:with muriatic acid	Lautard, Guy	TMBR#3:175
    Blueprint Holders		HSM'86:M/J14
    Boat repairs	Lautard, Guy	TMBR#3:208
    Bob Eaton's Civil War cannon	Lautard, Guy	TMBR#3:116
    Book citation: Accurate Tool Work	Lautard, Guy	TMBR#3:99
    Book citation: Cache Lake Country	Lautard, Guy	TMBR#3:2
    Book citation: Engineer to Win	Lautard, Guy	TMBR#3:218
    Book citation: Foundations of Mechanical Accuracy	Lautard, Guy	TMBR#2:67
    Book citation: Fundamentals of Dimensional Metrology	Lautard, Guy	TMBR#3:2 18
    Book citation: Gunsmithing Tips & Projects	Lautard, Guy	TMBR#3:153
    Book citation: Ron Fournier's book on sheet metal work	Lautard, Guy	TMBR#2:111
    Book citation: several other shooting oriented books cited	Lautard, Guy	TMBR#3:217
    Book citation: The Illustrated Reference of Cartridge Dimensions	Lautard, Guy	TMBR#3:166
    Book citation: The Masochist's Bedside Reader	Lautard, Guy	TMBR#3:227
    Book citation: The Muzzle Loading Caplock Rifle	Lautard, Guy	TMBR#3:166
    Book citation: Zen and the Art of Motorcycle Maintenance	Lautard, Guy	TMBR#3:230
    Book Review Tabletop Machining	RICE, JOE	HSM'99:J/F 27
    Book Review Three Elegant Oscillators	McKINLEY, CLOVER	HSM'99:N/D 26
    Book Review, Advanced Telescope Making Techniques	LAUTARD, GUY	HSM'90:M/J13
    Book Review, Designing Cost-Efficient Mechanisms	JOLY, DAVID	HSM'96:J/A 23
    Book Review, Model Engineers Workshop Manual, The	WIDIN, GREGORY P.	HSM'95:J/F18
    Book Review, Practical Ideas .for Metalworking Operations, Tooling, and Maintenance	RICE, JOE	HSM'95:N/D25
    Book Review, Shop Savvy	LAUTARD, GUY	HSM'90:S/O17
    Book Review: Build your Own Metal Working Shop From Scrap-Gingery	HOFFMAN EDWARD	HSM'82:N/D12
    Book Review: Clockmaking & Modelmaking Tools and Techniques	LAUTARD, GUY	HSM'92:J/F14
    Book Review: Drilling Technology, Grinding Technology and Turning Technology-Krar/Oswald	NIERGARTH, RAYMOND D.	HSM'83:S/O11
    Book Review: Gunsmith Kinks	LAUTARD, GUY w	HSM'86:J/A13
    Book Review: How to Build a Radial Arm Flame-Cutter	RICE, JOE	HSM'86:S/O48
    Book Review: How to Build Your Own Flintlock Rifle or Pistol	COFFIELD, REID	HSM'86:M/J20
    Book Review: How to Build Your Own Percussion Rifle or Pistol	COFFIELD, REID	HSM'86:M/J20
    Book Review: How to Build Your Own Wheellock Rifle or Pistol	COFFIELD, REID	HSM'86:M/J20
    Book Review: How to Make a Grasshopper Skeleton Clock	LAUTARD, GUY	HSM'91:J/A12
    Book Review: How to Make a Skeleton Wall Clock	LAUTARD, GUY	HSM'97:M/J 24
    Book Review: Jig and Fixture Design-Hoffman	NIERGARTH, RAYMOND D.	HSM'82:N/D13
    Book Review: Machinist's Bedside Reader, The	McKINLEY, CLOVER	HSM'86:N/D44
    Book Review: Machinist's Third Bedside Reader, The	McKINLEY, CLOVER	HSM'94:J/F23
    Book Review: Making An Eight Day Longcase Clock-Timmins	McKINLEY, CLOVER	HSM'83:J/A13
    Book Review: Making the Most of Your Lathe	RICE, JOE	HSM'93:S/O16
    Book Review: Manufacture of the Springfield Model 1903 Service Rifle	LAUTARD, GUY	HSM'85:N/D17
    Book Review: Master Mechanics' Manual, Volume One	McKINLEY, CLOVER	HSM'94:S/O18
    Book Review: My Own Right Time	JOLY DAVID	HSM'97:S/O 55 
    Book Review: Offenhauser	RICE, JOE	HSM'98:J/A 23
    Book Review: Practical Problems in Mathematics for Machinists-Hoffman	NIERGARTH, RAYMOND D.	HSM'83:J/F21
    Book Review: Strike While The Iron Is Hot-Lautard	McKINLEY, CLOVER	HSM'83:N/D18
    Book Review: Student's Shop Reference Handbook	RICE, JOE	HSM'86:S/O48
    Book Review: The Art of Engraving	LAUTARD, GUY	HSM'85:J/A15
    Book Review: The Basics of Firearms Engraving	COFFIELD, REID	HSM'87:J/F22
    Book Review: The Springfield M1903 Rifles	LAUTARD, GUY	HSM'87:M/A13
    Books: Art of Welding, W. A. Vause		HSM'88:N/D14 
    Books: Inspection and Gaging, Clifford W. Kennedy, Edward G. Hoffman, Steven D. Bond		HSM'88:N/D14 
    Books: Making Knives and Tools, Percy W. Blandford		HSM'88:N/D14 
    Books: Metal Turner's Handybook, The Paul N. Hasluck		HSM'88:N/D14 
    Books: Metallurgy Fundamentals, Daniel A. Brandt		HSM'88:N/D14 
    Books: Modular Fixturing, Edward G. Hoffman		HSM'88:N/D14 
    Books: Sheet Metal Work, R. E. Wakeford		HSM'88:N/D14 
    Books: Soldering and Brazing, Tubal Cain		HSM'88:N/D14 
    Books: The Antique Tool Collector's Guide to Value, Ronald S. Barlow		HSM'88:N/D14 
    Books: The Construction of a Weight Driven Brass Alarm Clock, John Wilding		HSM'88:N/D14 
    Books: The Machinist's Second Bedside Reader Guy Lautard		HSM'88:N/D14 
    Books: Using the Small Lathe, John Wilding		HSM'88:N/D14 
    Boring & Lathe Measuring Tools	WASHBURN, ROBERT A.	HSM'84:M/A60
    Boring and Threading Bars		HSM'89:J/A12
    Boring Bar and Tool Holder for Compact 5	RASNICK, JACK W.	HSM'89:S/O46
    Boring Bar Block	CLARKE	MEW#16,74
    Boring Bar Cutters and Turning Tools Part 2	KOUHOUPT, RUDY	HSM'90:J/F57
    Boring Bar from Worn-out Bits		PiM-Aug.'89,28
    Boring bar setting device	REBBECK	MEW#23,13
    Boring Bars Part I-II	KOUHOUPT, RUDY	HSM'84:J/A58,S/O56
    Boring head for Hobbymat BFE65,	HALL	MEW#27,43
    Boring Head	GROSJEAN, W.C	HSM'82:N/D26
    Boring head	MACEKE	MEW#27,27
    Boring Internal Threads	McLEAN, FRANK	HSM'85:J/F56
    Boring Thin-wall Tubing	TURNER, JOHN E.	PiM-Jun.'93,32
    Boring, Flycutting a Spot Facing with Rotating Cutters	ROUBAL, WM. T., Ph.D.	HSM'82:J/F24
    Bottles for the Home Shop	ZANROSSO, EDDIE	HSM'99:J/A 24
    Box making - some ideas	Lautard, Guy	TMBR#1:123
    Boxes for small precision tools	Lautard, Guy	TMBR#3:91; TMBR#2:10, 15
    Boxes: cast bronze chest handles	Lautard, Guy	TMBR#3:195
    Boxes: Corner caps	Lautard, Guy	TMBR#3:197
    Boxes: Decorative finishing for boxes	Lautard, Guy	TMBR#3:199
    Boxes: Handles	Lautard, Guy	TMBR#3:197
    Boxes: Hinges	Lautard, Guy	TMBR#3:196, 199, 200
    Boxes: Knotted rope &/or deadeyes as handles	Lautard, Guy	TMBR#3:197
    Boxes: Latches	Lautard, Guy	TMBR#3:196
    Boxes: Plywood splinters	Lautard, Guy	TMBR#3:197
    Boxes: Solid wood boxes	Lautard, Guy	TMBR#3:198
    Boxes: Storage trays for parallels and similar	Lautard, Guy	TMBR#3:198
    Brass compression nuts for file handle ferrules	Lautard, Guy	TMBR#3:107
    Brass filled characters in steel	Lautard, Guy	TMBR#1:137
    Brass Hammer	DAVIDSON, BILL	PiM-Jun.'88,12
    Brass is Beautiful	MARX, ALBERTO	HSM'86:S/O31
    Brass Kaleidoscope	Lautard, Guy	TMBR#2:140
    Brass Kaleidoscope, A		HSM'89:S/O24
    Brass napkin rings	Lautard, Guy	TMBR#1:143; HTIM:49
    Brass oil dribbler	JEEVES	MEW#25,26
    Brass Pad, The	GASCOYNE, JOHN	HSM'99:J/A 45
    Brazing Band Saw Blades	McLEAN, FRANK A.	HSM'93:S/O44
    Brazing The Misunderstood Joining Process	HUNT, CHARLES K	HSM'83:M/A24
    Breaking out a new coil of music wire	Lautard, Guy	TMBR#1:137
    Bridgeport Adapter Plate	SCHULTZ, ERIC A.	PiM-Dec.'96, 40
    Bridgeport Mill Tricks	KOUTSOURES, JIM	HSM'94:M/J14
    Brief business advice	Lautard, Guy	TMBR#3:2 16
    Brightening work before tempering	Lautard, Guy	TMBR#1:60
    British Standards for amateur engineers	JEEVES	MEW#21,18
    Broaching With Your Lathe	JENKINS, DAN	HSM'86:S/O42
    Broken tap removal from aluminum	Lautard, Guy	TMBR#3:78
    Broken Taps		PiM-Apr.'89,24
    Brown & Sharpe Digital Electronic Caliper		HSM'83:J/A8
    Brownells. Inc., Gunsmiths "Kinks" books	Lautard, Guy	TMBR#1:6
    Brunzeals plywood	Lautard, Guy	TMBR#3:192
    Build & Use an Adjustable Angle Plate Parts 1-3	KOUHOUPT, RUDY	HSM'98:M/A 48, M/J 42, J/A 60
    Build a Circle-cutting Attachment	WARING, LEONARD	PiM Aug. '98 34
    Build a Gimbaled Ship's Lamp	GREEN, WILLIAM F.	HSM'85:J/F34
    Build a Metal Slicer	DEAN, JOHN	PiM-Apr.'95. 18
    Build a Precise Tapper	BOLANTE, JAY	HSM'83:J/F51
    Build a Working Cannon	HOLM, PAUL J.	MW Feb. 99, 30
    Build an Electric Gun	METZE, ROBERT W.	HSM'85:M/A46
    Build and Use a Tool Post Grinder Parts 1-3	KOUHOUPT, RUDY	HSM'94:M/A20,M/J52,J/A46
    Build Your Own CNC Controller Parts 1-3	FRIESTAD, R. W.	HSM'92:S/O52,N/D51;HSM'93:J/F54
    Build Your Own Dividing Attachment	KOUHOUFT, RUDY	HSM'83:N/D32
    Build Your Own Face Plate	HADLEY, MARLYN	HSM'85:M/A28
    Build Your Own Geared Rotary Table Part 1	COLLINS, MARSH	PiM Aug. '98 6
    Build Your Own Geared Rotary Table Part 2	COLLINS, MARSH	PiM Oct. '98 28
    Build Your Own Shaper   Parts 3,4	COLLINS, MARSH	HSM'99:J/F 46 M/A 35
    Build Your Own Shaper Parts 1, 2	COLLINS, MARSH	HSM'98:J/A 30, S/O 40
    Building "Zippy" MK1	SEXTON, TERRY	PiM-Aug.'95 4
    Building a Band Saw	STRAUSS, MAX B.	PiM-Jun.'93,13
    Building a Belt Sander	GENEVRO, GEORGE	HSM'85:J/A32 
    Building a Cabinet for Your Sandblaster	WASHBURN, ROBERT A.	HSM'87:S/O50
    Building A Garden Workshop	HUDSON	MEW#15,48
    Building a Hydraulic Press Twice Parts 1, 2	ACKER, STEVE	HSM'93:M/J31,J/A43
    Building a Metal-bodied Hand Plane Parts 1-3	THOMAS, STEPHEN M.	HSM'99:J/A 28 S/O 62 N/D 44
    Building a Multi Cutter Face Mill	KOUHOUPT, RUDY	HSM'91:J/F50
    Building a Portable Vise Bench	HUNT, CHARLES K.	HSM'84:M/J24
    Building a Rack Cutting Attachment	SEXTON, TERRY	PiM Feb. '98 4
    Building a Rotary Table Parts 1-3	KOUHOUPT, RUDY	HSM'87:J/A57,S/O58,N/D62
    Building A Small Compressor	HOWELL	MEW#20,46
    Building a Target Rifle Parts 1-4	ACKER, STEVE	HSM'99:M/J 32 J/A36 S/O 46 N/D 48
    Building Phil Duclos' Model Maker's Dividing Head	COLLINS, MARSH	HSM'96:M/J 46
    Building The Edge Master Lawn Edging Machine Parts 1-	JOHNSON, D. F.	HSM'98:J/F 28, M/A 30, M/J 54, J/A 53, S/O 46
    Building the Panther Pup, Parts 1-9	REICHART, JOHN W. "BILL"	HSM'89:M/A30,M/J32,J/A8,S/O34,N/D34;HSM'90:J/F38,M/A28,M/J31,J/A42
    Building the Shop	ACKER, STEVE	HSM'95:S/O28
    Building the Titan .60 Parts 1-5	GENEVRO, GEORGE	HSM'94:M/A34,M/J32,J/A39,S/O44,N/D32
    Building the Universal Pillartool Parts 1-5	MASON, HAROLD	HSM'91:J/F16,M/A32,M/J28,J/A21,S/O32
    Building Your Own Collet Chuck	DOCHTERMAN, WILLIAM B.	PiM Apr. '98 10
    Bullet mold making	Lautard, Guy	TMBR#1:118
    Bumping Out	BLANDFORD, PERCY	PiM-Apr.'95 33
    Business cards as advertising	Lautard, Guy	TMBR#3:209
    Butler Multiple Boring Machines, The	MASON, HAROLD	HSM'93:M/A14
    Button head socket cap screws	Lautard, Guy	HTIM:2
    Button V-Block	DUBOSKY, ED	PiM-Oct.'88,12
    Buying a used Gravermeister	Lautard, Guy	TMBR#3:243
    Buying and renovating -- lathe	MACHIN	MEW#32,30
    Buying Used Machine Tools	GRADY, ROBERT L.	HSM'88:S/O32
    Buying Used Welding Equipment	HUNT, CHARLES K.	HSM'84:J/A24
    C&D Grinder Stand	PLOTKlN, CHUCK	MW Oct. 99, 38
    Cabin Fever 1998	RICE, JOE	HSM'98:S/O 52
    CAD Capabilities, Parts 1,2	HALL	MEW#20,12;#21,34
    CAD for the Common Man	HINSHAW, ANNETTE	HSM'85:N/D28
    CAD for the Small Shop	HOFFMAN, EDWARD G.	HSM'91:J/F12
    Calculating an angle	Lautard, Guy	TMBR#2:72
    Calculating bandsaw blade speeds	Lautard, Guy	TMBR#3:185
    Calculating numbers for cutting a ball	Lautard, Guy	TMBR#1:77; TMBR#3:24
    Calculating top slide infeed for screwcutting	Lautard, Guy	TMBR#2:112; TMBR#3:112
    Caliper or floating arm knurling tool	Lautard, Guy	TMBR#1:54
    Cam Clamps	HOFFMAN, EDWARD G.	HSM'91:N/D54
    Can You Handle It?	MASON, HAROLD	PiM-Jun.'89,10
    Candle wax, blade breakage, sawing to a layout line	Lautard, Guy	TMBR#3:241
    Canjar triggers	Lautard, Guy	TMBR#3:153
    Capping piece of solid wood + plywood top	Lautard, Guy	TMBR#3: 194, 197-198
    Car badges, belt buckles, broochs	Lautard, Guy	TMBR#3:239
    Carbide Cutting Tools for the Lathe	BRATVOLD, BRIAN	PiM Jun.'97 21 
    Carbide End Mill, A	McLEAN, FRANK A.	HSM'89:J/A54
    Carbide Inserts	WITHEROW, JEFF	HSM'96:J/A 58
    Carriage Multi-stop	DUBOSKY, ED	HSM'89:J/F46
    Carriage Stop for the Mill, A	RICE, ROY	PiM-Aug.'94,27
    Carriage Stop Indicator		HSM'90:J/F14
    Casehardening :Depth and distribution of parts in the pack box	Lautard, Guy	TMBR#2:183
    Casehardening methods, as continued	Lautard, Guy	TMBR#3:6-10
    Casehardening methods, as detailed in The Bullseye Mixture,	Lautard, Guy	TMBR#2:163-197
    Casehardening: - charring bone meal	Lautard, Guy	TMBR#3:8
    Casehardening: - washing bone meal	Lautard, Guy	TMBR#3:8
    Casehardening: A charcoal furnace	Lautard, Guy	TMBR#2:185-187
    Casehardening: Activators	Lautard, Guy	TMBR#2:194
    Casehardening: air bubbles in the quench	Lautard, Guy	TMBR#2:191-192
    Casehardening: Applicability of pack casehardening	Lautard, Guy	TMBR#2:18 1
    Casehardening: Bean charcoal	Lautard, Guy	TMBR#3:7
    Casehardening: Bone dust	Lautard, Guy	TMBR#2:176
    Casehardening: Bone meal	Lautard, Guy	TMBR#3:7
    Casehardening: Carbon content	Lautard, Guy	TMBR#2:172-173
    Casehardening: Carburizing	Lautard, Guy	TMBR#2:173
    Casehardening: Casehardening temperatures	Lautard, Guy	TMBR#2:190
    Casehardening: Charcoal	Lautard, Guy	TMBR#2:176
    Casehardening: Cheap source of potassium nitrate	Lautard, Guy	TMBR#3:9
    Casehardening: Clay containers	Lautard, Guy	TMBR#3:7
    Casehardening: color casehardening	Lautard, Guy	TMBR#2:173
    Casehardening: Depths of carbon penetrations	Lautard, Guy	TMBR#2:174
    Casehardening: Don't re-use charcoal from the quench tank	Lautard, Guy	TMBR#3:9
    Casehardening: Dried beans	Lautard, Guy	TMBR#3:7
    Casehardening: Early results, per Bullseye Mixture methods	Lautard, Guy	TMBR#3:7
    Casehardening: Ebonex & ready-made bone charcoal	Lautard, Guy	TMBR#3:9
    Casehardening: Effect of time at high temperature	Lautard, Guy	TMBR#2:174
    Casehardening: Electric furnace	Lautard, Guy	TMBR#2:185
    Casehardening: Fire clay or partially hardened ceramic slip	Lautard, Guy	TMBR#3:8
    Casehardening: Flower pot as a pack box	Lautard, Guy	TMBR#2:182
    Casehardening: Handling the pack box	Lautard, Guy	TMBR#2:183
    Casehardening: Hardenability of some steels	Lautard, Guy	TMBR#2:172
    Casehardening: Hardening of mild steel by carbon migration	Lautard, Guy	TMBR#2:172
    Casehardening: Hatcher's Notebook (a book)	Lautard, Guy	TMBR#2:191
    Casehardening: How to do it	Lautard, Guy	TMBR#2:182
    Casehardening: Incorporating the washing soda	Lautard, Guy	TMBR#3:8
    Casehardening: Industrial practice	Lautard, Guy	TMBR#2: 175-176
    Casehardening: Judging furnace temp by eye	Lautard, Guy	TMBR#2:189
    Casehardening: Kasenite	Lautard, Guy	TMBR#2:176
    Casehardening: Masking off parts of a job against casehardening	Lautard, Guy	TMBR#2:183
    Casehardening: Metals Handbook	Lautard, Guy	TMBR#2:192
    Casehardening: Neycraft furnace	Lautard, Guy	TMBR#3:6
    Casehardening: Old time methods	Lautard, Guy	TMBR#2:176
    Casehardening: Oxidation & dark coloration	Lautard, Guy	TMBR#3:7
    Casehardening: Packing the job in a flower pot with bone charcoal	Lautard, Guy	TMBR#3:8
    Casehardening: Pre-heat and carburizing heat	Lautard, Guy	TMBR#3:9
    Casehardening: Quench tank - making one	Lautard, Guy	TMBR#2:190-191
    Casehardening: quenching liquid	Lautard, Guy	TMBR#2:191-192
    Casehardening: Quenching	Lautard, Guy	TMBR#2: 172-173
    Casehardening: Quenching	Lautard, Guy	TMBR#3:9
    Casehardening: Refining the grain structure	Lautard, Guy	TMBR#2:173, 191
    Casehardening: Sealing the pack box	Lautard, Guy	TMBR#2:183
    Casehardening: Sealing the pot	Lautard, Guy	TMBR#3:9
    Casehardening: Some sources of carbon	Lautard, Guy	TMBR#2:173
    Casehardening: Sourcing the activators	Lautard, Guy	TMBR#2:194
    Casehardening: Temperature indicating pellets	Lautard, Guy	TMBR#2:190
    Casehardening: Tempering	Lautard, Guy	TMBR#2:173
    Casehardening: The charcoal recipe	Lautard, Guy	TMBR#2:192-194
    Casehardening: the pack box	Lautard, Guy	TMBR#2:182
    Casehardening: The secret powders: Barium carbonate	Lautard, Guy	TMBR#3:7
    Casehardening: The secret powders: Sodium carbonate (washing soda)	Lautard, Guy	TMBR#3:7
    Casehardening: Time at casehardening temp.	Lautard, Guy	TMBR#2:190-192
    Casehardening: Use of paper to consume excess oxygen	Lautard, Guy	TMBR#3:8
    Casehardening: Using lower temperatures	Lautard, Guy	TMBR#3:7
    Casehardening: Various quenching/heat treating scenarios	Lautard, Guy	TMBR#2:191
    Casehardening: Washing the charcoal	Lautard, Guy	TMBR#3:8
    Casehardening: What wrecked the stove	Lautard, Guy	TMBR#3:7
    Casehardening: Why/where used	Lautard, Guy	TMBR#2: 172-173
    Cast Iron Repair	WALKER, RICHARD B.	HSM'91:J/F30
    Cast iron section for workholding	Lautard, Guy	TMBR#1:39
    Cast iron, source of high quality, for various	Lautard, Guy	TMBR#1:91; TMBR#3:79, 174
    Cast lead hammers for your shop	Lautard, Guy	TMBR#2:112
    Casting machine handles in epoxy	Lautard, Guy	TMBR#3:75
    Castle Nuts	SCHULZINGER, JACOB	PiM-Apr.'95 14
    Cat Head Chucks		HSM'88:J/F13
    Cautions re use of unapproved electrical devices	Lautard, Guy	TMBR#3:27
    Cellulose Tape-Silent Magic	BECK, B.	HSM'86:J/F30
    Center Alignment		HSM'90:S/O15
    Center Knocker Refinements	YOUNG, BARRY	MW Aug. 99, 47
    Center punches, how to sharpen	Lautard, Guy	TMBR#1:21
    Center Test Indicator	BROCKARDT, FRANK G.	HSM'84:M/A19
    Centering a cutter over a shaft by eye	Lautard, Guy	TMBR#1:83
    Centering a cutter over a shaft by eye	Lautard, Guy	TMBR#1:83
    Centering a Gear Cutter		PiM-Aug.'89,24
    Centering Cap	McCORMAC, DON	HSM'82:M/A7
    Centering Guide	OPFER, JOHN, JR.	HSM'87:S/O32
    Centering Holes		HSM'86:N/D12
    Centering in the Lathe		HSM'86:N/D12
    Centering Lathe Tools	DRAYSON, D. A.	PiM-Apr.'96, 40
    Centering square/rectangular stock in the 4-jaw chuck	Lautard, Guy	TMBR#1:81
    Centering the Tailstock		HSM'89:S/O16
    Centering the Tailstock		HSM'90:M/A16
    Centering Work (Tips & Tricks)	LAMANCE, THOMAS	PiM-Apr.'95 39
    Centre punch guide	LOADER	MEW#29,12
    Centre Square	HALL	MEW#11,47
    Centrifuge type oil filter	Lautard, Guy	TMBR#1:197
    Century-Old Lathe Back at Work	HOLKEBOER, CARL	HSM'88:N/D56
    Ceramic Cutting Tools		HSM'87:N/D17
    Ceramic Cutting Tools		HSM'89:J/F12
    Cerro Alloys Aid in Machining Irregular Parts	McBRIDE, RONALD E.	HSM'93:N/D36
    Chain drilling aided by accurate hole spacing	Lautard, Guy	TMBR#3:102
    Chain drilling to make a blind opening	Lautard, Guy	TMBR#2:125
    Chain drilling	TWIST	MEW#25,40
    Chain making - some ideas	Lautard, Guy	TMBR#3:54
    Chalk on files	Lautard, Guy	TMBR#1:7
    Chambering a Rifle Barrel for Accuracy	CONSTANTINE, RANDOI.PH	MW Dec. 99, 13
    Change Gears	ISAAC, P.	HSM'96:S/O 63
    Change wheels and screwcutting	HALL	MEW#28,24
    Change-Gear Bracket, A	HARMAN, STEVE	PiM-Feb.'89,17
    Changing the Feed		HSM'86:M/J15
    Charcoal iron	Lautard, Guy	TMBR#2:11
    Chatter and the Cutoff Blade	DAVIS, LAURENCE	PiM-Apr.'93,29
    Chatter-free Radius Turning		HSM'87:M/A15
    Chatterless Countersinks	HEDIN, R. S.	HSM'94:N/D48
    Cheap and Effective Belt Dressing	PETERKA, W. PETE	HSM'83:M/J15
    Cheap Cup Washers	LAMANCE, THOMAS	PiM-Dec.'92,3
    Cheap Cutoff Tool, A	LAMANCE, THOMAS	PiM-Aug.'92,3
    Cheap Rotary File, A	ARNOLD, GREGRICH	PiM-Apr.'94,MN
    Checkering in the Mill	ACKER, STEVE	HSM'92:S/O30
    Checking a #2MT against standard specs	Lautard, Guy	TMBR#3:15
    Checking Lathe Alignment	KOUHOUPT, RUDY	HSM'92:S/O48
    Child's Lock, A	TATA, ROBERT 	MW Oct. 99, 46
    Chinese tool steel	Lautard, Guy	TMBR#1:181
    Chip Breaker, A	MUELLER, WALTER	PiM-Dec.'93,23
    Chip Catcher		HSM'90:S/O15
    Chip Shield		PiM-Apr.'90,3
    Chip Vac	KOLAR, GEORGE	HSM'92:N/D14
    Chisel Protection		PiM-Oct.'91,3
    Choice of files	Lautard, Guy	TMBR#1:7-8
    Choice of reamers	Lautard, Guy	TMBR#1:16
    Choosing & using a sensitive dial indicator	Lautard, Guy	TMBR#2:83
    Chuck backplate fitting procedures	Lautard, Guy	TMBR#3:63
    Chuck Key Retainer	VAUGHN, W.B.	HSM'82:J/A41
    Chuck Key Storage	JOHNS, JACK	HSM'92:N/D15
    Chuck Lifter, A	STAIGER, JOHN L., JR.	PiM Jun. '98 16
    Chuck Support	PAQUAY, ART	PiM-Aug.'94,MN
    Chuck Tool		PiM-Aug.'90,24
    Chuck Wrench Storage		PiM-Oct.'91,3
    Chuckboard, A	COLEMAN, ROBERT	HSM'86:J/F55
    Chucking a Disk Square		HSM'83:J/A12
    Cigarette paper test of squareness, etc.	Lautard, Guy	TMBR#2:72
    Circumventing "minimum orders"	Lautard, Guy	TMBR#1:3
    Citation: FWW, good bandsaw articles in	Lautard, Guy	HTIM:42
    Citation: FWW, making a table saw fence	Lautard, Guy	HTIM:44; TMBR#3:183
    Citation: FWW, making dovetail joints	Lautard, Guy	TMBR#3:193-194
    Citation: FWW, making safe wooden lamps	Lautard, Guy	TMBR#3:206
    Citation: FWW, re-babbetting machinery bearings	Lautard, Guy	TMBR#1:135
    Citation: FWW, restoring a bandsaw	Lautard, Guy	TMBR#3:186
    Citation: FWW, working with plywood	Lautard, Guy	TMBR#3:191
    Citation: GBL's 3-legged lathe stand	Lautard, Guy	TMBR#3:2 15
    Citation: GBL's surface gage desk lamp	Lautard, Guy	TMBR#3:205
    Citation: How to make an EDM machine	Lautard, Guy	TMBR#2:150; TMBR#3:78
    Citation: How to make your own decals	Lautard, Guy	TMBR#2:149
    Citation: Making a machinist's screw jack	Lautard, Guy	HTIM:20
    Citation: Making small, fine-quality al. castings	Lautard, Guy	TMBR#2:149
    Citation: making straightedges	Lautard, Guy	HTIM:48
    Citation: Mounting a DTI to a mill's vertical spindle	Lautard, Guy	HTIM:15
    Citation: Several articles re rifles/action building Citationd	Lautard, Guy	TMBR#3:167
    Citation: SIC, a tiny steam engine	Lautard, Guy	TMBR#3:214
    Citation: Slow speed attachment for a bandsaw	Lautard, Guy	HTIM:42
    Clamp for Cross-drilling, A		PiM-Aug.'91,3
    Clamping down a cylinder for machining	Lautard, Guy	TMBR#1:138
    Clamping Tapered Material in a Vise-No Problem!	HARMON, JOE	HSM'94:N/D54
    Clamping the Tailstock		PiM-Oct.'89,3
    Clamping Work to the Mill Table	TIMM, HAROLD	HSM'84:S/O10
    Clamp-type Lathe Dog	McCORMAC, DON	HSM'83:M/J50
    Classic Boring Bar Holder, A	JOHNSON, D. E.	PiM-Dec.'92,4
    Clayton's Change Wheel, A	SEXTON, TERRY	PiM Dec. '98 29
    Clean Tapers		HSM'91:M/A15
    Cleaning a granite surface plate	Lautard, Guy	HTIM:46; TMBR#3:204 & 224
    Cleaning a Universal Chuck	McLEAN, FRANK A.	HSM'96:J/F 57
    Cleaning Chucks		HSM'85:M/J14
    Cleaning clogged files	Lautard, Guy	TMBR#2:123
    Cleaning Files		PiM-Aug.'89,24
    Cleaning Magnets		HSM'87:M/A15
    Cleaning out Your Dies		PiM-Jun.'90,24
    Cleaning Silicone Sealer Nozzles		HSM'88:N/D16
    Cleaning up a burred #2MT lathe tailstock	Lautard, Guy	TMBR#1:17
    Cleaning Up Magnetic Chucks	SEVIGNY, DICK	HSM'92:M/A15
    Clearing tap cuttings	Lautard, Guy	TMBR#1:19
    Climb milling aluminum	Lautard, Guy	HTIM:14
    Cloche Hoops	MCLEAN, FRANK A.	HSM'95:N/D62
    Clutch for Your Lathe, A	VAN DUYN, LARRY	PiM-Aug.'96,20
    Clutch Guard for a Bridgeport Model J Head	HAUSER, JAMES W.	MW Apr. 99, 45
    Clutch-motor Starter for Three-phase Converters	HESSE, JAMES	PiM Oct.. 94,22
    Coaxial Indicator	METZE, ROBERT W	PiM-Oct.'91,18
    Coil springs for triggers	Lautard, Guy	TMBR#3:148
    Coil springs for triggers	Lautard, Guy	TMBR#3:148
    Coils for a novel application	HASS	MEW#30,24
    Cold working of steel	Lautard, Guy	TMBR#1:180
    Cole Drill	Lautard, Guy	TMBR#3:18 (also inside back cover, in 2nd printing) 
    Collar Substitute		PiM-Feb.'89,24
    Collar Substitute	LAMANCE, THOMAS	PiM-Apr.'93,3
    Collar-like Nut		PiM-Jun.'91,3
    Collet Adapter	PAQUAY, ART	PiM-Feb.'94,30
    Collet chuck arrangement	Lautard, Guy	TMBR#2:39
    Collets for Your Lathe	REISDORF, GARY F.	HSM'87:M/A28
    Collets Galore		HSM'83:J/F16
    Color of Steel, The	MASSEY, G. ROBERT	HSM'89:M/J43
    Column Storage Box for a Drill Press	VAUGHN, W. B.	HSM'84:J/F44
    Combination Chuck Wrench		PiM-Aug.'91,3
    Combination Regular and Bull Nose Live Center, A	BARBOUR, JOE, JR	PiM-Jun.'95 28
    Comments on My Shop	McLEAN, FRANK A	HSM'88:M/A46 
    Commercial Components	HOFFMAN, EDWARD G	HSM'92:J/F56
    Compact Boring Head, A Part 1-3(Micro Machinist, The)	KOUHOUPT, RUDY	HSM'95:J/A55 S/O51 N/D56
    Compact Carousel Tool Rack, A	WILSON, GLENN L.	PiM-Jun.'94,4
    Compact Five Conversion	JENNINGS	MEW#10,26
    Compound Dividing	Lautard, Guy	TMBR#1:41
    Compound Rest Lock	MARX, ALBERTO	HSM'88:M/J35 
    Compressed Air Motor Parts I-III	KOUHOUPT, RUDY	HSM'84:J/F48,M/A58,M/J58
    Compressed Air Safety	HOFFMAN, EDWARD G.	HSM'83:J/F24
    Compressed Air	EVERETT, LYNN	HSM'82:S/O20,N/D8
    Computer controlled x-y table	STUART	MEW#27,18
    Computer Simulation	LENGE	MEW#9,16
    Computer-aided Dividing Plates	FOSTER, CHARLES R	HSM'98:J/F 24 
    Computerizing Machine Shop Calculations		HSM'84:S/O14
    Computers in the Shop, Basic Principles	FRIESTAD, ROLAND	HSM'89:N/D43
    Computers in the Shop, Introduction	FRIESTAD, ROLAND	HSM'89:S/O56
    Concave and Convex Radius Cutter	JONES, BRUCE	HSM'84:N/D40
    Concentric Morse taper spindle	DEW	MEW#30,26
    Concrete & pipe work islands	Lautard, Guy	TMBR#3:27
    Cone Mandrel	LAMANCE, THOMAS	PiM-Jun.'92,3
    Confessions of a Junkyard Motor Junkie	MYERS, TED	HSM'91:J/F45
    Conservative Coolant Applicator	WILSON, GLENN L.	PiM-Aug.'91,4
    Conserving Cutting Oils	VAUGHAN, W.B.	HSM'83:N/D47
    Construction & Use of the Lathe Carriage Stop	JOHNSON. D. E., P. E.	HSM'84:S/O39
    Construction of Pottery Kilns (Heat-treat Furnaces)	HESSE, JIM	PiM Apr.'97 16
    Construction, and Inspection		HSM'85:M/J32 
    Convenient Addition to a Palmgren Angle Vise, A	ATKINSON, CHARLES T.	PiM-Jun.'95 38
    Conversion of a Gear-driven Shaper to Hydraulic Drive	CLARKE, THEODORE M.	HSM'84:J/F36
    Conversion to Three-phase Power	ROBERTSON, J. C.	PiM-Dec.'92,28
    Convert a Milling Machine to CNC Control Parts 1-6	FRIESTAD, R. W.	HSM'91:M/J51,J/A44,N/D44,S/O52;HSM'92:J/F45,M/A45
    Convert Your Mill-drill to CNC Parts 1-4	FRIESTAD, ROLAND	HSM'90:M/A46,M/J50,J/A54,S/O46
    Converting a Lathe to Cut Metric Threads	LINCOLN, W.A.	HSM'88:N/D30 
    Convex and Concave Lathe Work		HSM'88:S/O13
    Coolant Delivery On The Cheap	BROOKS	MEW#11,23
    Coolant Pump (Tips & Tricks)	KOLAR, GEORGE	PiM-Aug.'95 44
    Coolant Tank and Pump, A	TORGERSON, RICHARD S.	PiM-Feb.'90,15
    Co-ordinate measuring	FREED	MEW#30,68
    Copper and Its Alloys	GENEVRO, GEORGE	HSM'98:M/A 51 
    Copper coins as work protectors	Lautard, Guy	TMBR#3:236
    Copper fluid tanks for cars	Lautard, Guy	TMBR#3:80-81
    Copper setscrew pads	Lautard, Guy	TMBR#2:112
    Copper tube expander mandrel	Lautard, Guy	TMBR#2:129
    Copper Tubing Depth Gage		PiM-Feb.'88,24
    Copper vise jaw liners	Lautard, Guy	TMBR#2:122
    Copper wire setscrew pads	Lautard, Guy	TMBR#3:173
    Cork - where to buy sheets	Lautard, Guy	TMBR#2:119
    Corner Locator	MADISON, JAMES	PiM-Apr.'94,21
    Correct depth to drill center holes	Lautard, Guy	TMBR#2:92
    Correcting a Milling Machine Vise	McLEAN, FRANK A.	HSM'94:J/A50
    Correcting Watch Case Bow/Pendant Wear	SMITH, W. R.	PiM-Feb.'95 28
    Corrections to Concave and Convex Radius Cutter	JONES, BRUCE	HSM'85:J/A19
    Crank Handles		HSM'91:N/D14
    Crankcases, Crankshafts, and Connecting Rods for Model Engines Parts 1,2	GENEVRO, GEORGE	HSM'99:S/O 28 N/D 55
    Crankshaft reconditioning tech	HARTWELL	MEW#30,17
    Creativity	WILSON, GLENN L.	PiM-Jun.'95 26
    Critical relationships between trigger & action parts	Lautard, Guy	TMBR#3:145
    Cross Drilling Jig	HARRIES	MEW#9,24
    Cross Drilling		PiM-Dec.'89,24
    Cross slide brkt -- pistol drill	BROOKS	MEW#28,45
    Cross Slide Mounted Drilling Machine		HSM'84:N/D17
    Cross-feed Cover for a 10-K	BENNETT, N. H.	HSM'85:N/D57
    Cross-feed Lever	TORGERSON, RICHARD	PiM-Apr.'89,18
    Crossvice To Vertical Slide	HARTWELL	MEW#15,23
    CRS - what is it?	Lautard, Guy	TMBR#1:23
    Cure for Head-banging, A	SPARBER, R. G.	MW Aug. 99, 46
    Curing slipping of flat belt drives	Lautard, Guy	TMBR#3:59-60
    Curved Spoke Flywheel	DUCLOS, PHILIP	PiM-Apr.'88,4
    Customizing an Imported Drill Press 	WILSON, GLENN L.	MW Feb. 99, 15
    Cut Convex or Concave Sections		HSM'91:M/A16
    Cut Threads With a Tap	HESTER, DON	HSM'94:M/A17
    Cut-rate Machinist's Level, A	THOMPSON, JACK R.	PiM Dec. '98 33
    Cutter Bit Grinding Block	JOHNSON, D. E.	HSM'87:M/A44
    Cutter Bit Grinding Block, A	PETERKA, W. PETE	HSM'86:M/J54
    Cutter blocks & shop made cutters	Lautard, Guy	TMBR#1:101; TMBR#3:110
    Cutter frame	GRAY	MEW#28,16
    Cutting a coin slot	Lautard, Guy	TMBR#2:131
    Cutting a Keyway		PiM-Dec.'89,24
    Cutting a large radius fillet	Lautard, Guy	HTIM:14-15
    Cutting a Non-standard Radius on a Milling Machine	WOLCOTT; ED	HSM'99:S/O 33
    Cutting a Radius		HSM'91:M/J10
    Cutting a Rifle Crown	ACKER, STEVE	PiM-Jun.'96, 36
    Cutting a Thin Gear	DEWBERRY, O. J.	HSM'87:N/D58
    Cutting Bastard Threads on a Quick Change Lathe	FELLER, E. T.	HSM'86:J/F54
    Cutting Coarse Internal Threads	KOLAR, GEORGE	HSM'93:S/O14
    Cutting Duplicate Short Lengths		PiM-Aug.'89,24
    Cutting Fluids and Compounds	MARCUS, JOHN, Ph.D.	HSM'84:J/F40
    Cutting Heavy Sheet Metal	LAMANCE, THOMAS	PiM-Jun.'92,3
    Cutting Irregularly Shaped Holes	ROSCOE, LOWIE	HSM'92:N/D39
    Cutting Keyways Inside Holes		PiM-Apr.'89,3
    Cutting Left Hand Threads	BRIFFA	MEW#20,54
    Cutting Left-hand Threads	McLEAN, FRANK A.	HSM'91:J/A56 
    Cutting metric threads on an "English" lathe	Lautard, Guy	TMBR#3:114
    Cutting Metric Threads		HSM'91:S/O12
    Cutting multiple start threads	Lautard, Guy	TMBR#2:87
    Cutting Odd-Count Threads	JAMES, CLINTON	PiM-Jun.'94,3
    Cutting Off Threads		HSM'86:J/A12
    Cutting oil - SC40	Lautard, Guy	TMBR#1:7
    Cutting Oil (Tips & Tricks)	KORMAN, JOHN G.	PiM-Dec.'95 42
    Cutting plate cams to a layout line freehand	Lautard, Guy	TMBR#2:108
    Cutting plywood panels down to size safely	Lautard, Guy	TMBR#3:189,190
    Cutting Racks	UNWIN	MEW#9,70
    Cutting speeds (a useful chart)	Lautard, Guy	TMBR#1:9
    Cutting Steel with a Circular Saw Blade	ACKER, STEVE	HSM'96:S/O 33
    Cutting the Chatter	BAUMGARDNER, PAUL	HSM'93:J/F14
    Cutting the pieces	Lautard, Guy	TMBR#3:192
    Cutting the Rust		HSM'87:J/A16
    Cutting threads in the lathe	Lautard, Guy	TMBR#3:102
    Cutting threads up to a shoulder	Lautard, Guy	TMBR#3:114
    Cutting Threads		HSM'90:N/D14
    Cutting Tool for Machining Aluminum, A	LEWIS, JAMES A	HSM'85:N/D48
    Cutting Torch Contour Guide	LYNCH, CARLYLE	HSM'88:J/A55 
    Cutting Vee Notches	COOPER, JOHN A.	HSM'93:J/A48
    Cutting Wood or Steel		HSM'88:M/A14
    Cuttlebone Casting	LEWIS, JAMES R.	HSM'87:M/J48
    Cyclone Dust Collector, A	HESSE, JIM 	MW Dec. 99, 32
    Cylinder or Master Square, A	MCLEAN, FRANK A.	HSM'92:N/D42
    Cylinders and Pistons for Two-stroke Cycle Model Engines	GENEVRO, GEORGE	HSM'96:N/D38
    Dating Old Metalworking Machinery	BATORY, DANA MARTIN	PiM Apr.'97 33
    D-bit from dowel pins etc.	Lautard, Guy	TMBR#3:66
    D-bit Toolmaker's type	Lautard, Guy	TMBR#1:53
    D-bit	Lautard, Guy	TMBR#1:52
    DC motor and speed controller for bandsaw speed	Lautard, Guy	TMBR#3:184
    DC motor/speed controller for bandsaw speed	Lautard, Guy	TMBR#3:184; HTIM:42
    DC Motors Speed Control, Part 4	HALL	MEW#18,68
    Dead On, Dead Center + .000"	EVERS, HOWARD W. 	MW Oct. 99, 51
    Dealing With Wear		HSM'91:J/A15
    Deburring Scraper	McCORMAC, DON	HSM'83:J/F52
    Deciding upon box size	Lautard, Guy	TMBR#3:191
    Dedicated Tapper, The	MASON, HAROLD	PiM-Oct.'93,6
    Deepening a pattern layout with an electric engraver	Lautard, Guy	TMBR#3:240
    Degassing Molten Aluminum		HSM'89:S/O44
    Degreaser		HSM'89:J/F12
    De-horning a Myford driving dog	Lautard, Guy	TMBR#3:14
    Deluxe Radius Turning Attachment, A Parts 1-2	WILSON, GLENN L.	HSM'92:J/A2,0,S/O18
    Demagnetize Large Pieces		HSM'88:J/A13
    Demagnetizing Tools		HSM'87:J/A16
    Density, Volume, Dimensions = Weight	MELTON, L. C.	HSM'90:M/J38
    Dental abrasive strips and miniature tooth brushes	Lautard, Guy	TMBR#3:177
    Dental Burrs in the Metal Shop	BROWNE, DONOVAN V.	HSM'94:M/A16
    Dental tools for removal of t'paper from tapped holes	Lautard, Guy	TMBR#3:177
    Depth Gage Attachment, A		HSM'89:M/J50
    Depth Gage Attachment, A	McLEAN, FRANK A.	HSM'89:M/J50
    Depth Gage, A (drill press)		PiM-Jun.'89,20
    Depth Gage, A	YOUNG, MARSHALL	PiM-Jun.'89,20
    Depth gages	Lautard, Guy	TMBR#1:33; TMBR#3:173
    Depth Stop for a Unimat		HSM'90:M/J15
    Designing & deciphering verniers	Lautard, Guy	TMBR#1:121
    Designing & fitting (split cotters)	Lautard, Guy	TMBR#1:92-96
    dial indicator for measuring lathe saddle movement	Lautard, Guy	HTIM:8
    Dial Indicators-Dial Test Indicators		HSM'91:N/D37
    Dial Test Indicator Acc, Parts 1-3	HALL	MEW#14,34;#15,10;#16,32
    Dial Test Indicator Base	HALL	MEW#17,50
    Diamantine powder	Lautard, Guy	TMBR#2:120 & 122
    Diamond Dresser, A	HUARD, CONRAD	PiM-Feb.'92,14
    Diamond Tool Efficiency	OGINZ, FREDERICK	HSM'88:J/A37 
    Die Cutting Threads		HSM'86:J/F13
    Die Filer		HSM'89:J/F12
    Die Maker Buttons		PiM Apr. '98 16
    Die Stock Plus, A	WRIGHT, TED	PiM-Feb.'90,4
    Differential Dividing	Lautard, Guy	TMBR#1:41
    Differential Micrometer Head	MORRIS	MEW#20,40
    Digital Readout, Part 2	HALL	MEW#9,51
    Dimensional tolerance of aluminum bar stock	Lautard, Guy	HTIM:12
    Dimensions & Tolerances, Parts 13 - 16		HSM'89:J/F16,M/A18,M/J7,J/A14
    Direct Dividing	Lautard, Guy	TMBR#1:40
    Direct Reading SFPM Adapter for the Common Speed Indicator, A	HEMMELGARN, KEN	PiM Jun. '98 38
    Disk Sander Safety	LAMANCE, THOMAS	PiM-Oct.'92,3
    Dismantling an edge finder (not in 1st printing)	Lautard, Guy	TMBR#3:139
    Dismantling Jacobs type chuck	COOPER	MEW#22,26
    Dividing 1/4 degree vernier	Lautard, Guy	TMBR#2:8
    Dividing att for Boxford lathe	SHIRRAS	MEW#28,34
    Dividing att For The Unimat 3	SCOGGINS	MEW#13,69
    Dividing Attachment	HESSE, ROBERT	PiM-Jun.'94,M&M
    Dividing Computer Program	TURNBULL	MEW#19,45
    Dividing decent	Lautard, Guy	TMBR#2:8
    Dividing from Bandsaw blades	Lautard, Guy	TMBR#1:43-44; TMBR#2:198
    Dividing funny numbers	GRAY	MEW#22,47
    Dividing head a beefed up version	Lautard, Guy	TMBR#2:3
    Dividing head for Peatol lathe Part l	JEFFREE	MEW#21,57; #22,27
    Dividing Head for the Milling Table	WASHBURN, ROBERT A.	HSM'85:J/A58 
    Dividing Head for the Taig (Taig/Peatol)Lathe, A	JEFFREE TONY	PiM Oct.'97 4
    Dividing Head Index Plates	JOHNSON, D. E.	PiM-Dec.'89,4
    Dividing Head Revisited, The	WASHBURN, ROBERT A	HSM'86:S/O52
    Dividing Head, The	McLEAN, FRANK	PiM Oct.'94,16
    Dividing On a geared Rotary Table	Lautard, Guy	TMBR#1:41
    Dividing on the Lathe	SCHMIDT, JAMES	HSM'95:M/J45
    Dividing with 15/16 hole vernier	Lautard, Guy	TMBR#1:42
    Division plates from bandsaw blades	Lautard, Guy	TMBR#2:3
    Dog Work	LAMANCE, THOMAS 	MW Jun. 99, 10
    Doggone Good		HSM'83:J/F16
    Doing work for university profs	Lautard, Guy	TMBR#3:209
    Don't drill into your lathe spindle taper	Lautard, Guy	TMBR#3:109
    Don't run a chuck up to speed without a workpiece in it	Lautard, Guy	TMBR#3:62
    Don't Fake A Casting-Make A Casting Parts I-III		HSM'84:M/A50,M/J52,J/A52
    Double Design Drill	NEAVE	MEW#19,20
    Double pulley for dual motor drive	Lautard, Guy	TMBR#3:58
    Double the Capacity of Your Lathe	BARBOUR, J. O., Jr.	HSM'84:S/O18
    Double-ball clamping levers	Lautard, Guy	TMBR#1:85
    Double-ended Dial Indicator Adapter, A	LAUTARD, GUY	PiM-Apr.'88,12
    Double-sided Tape for Machining	MADISON, JAMES	PiM-Dec.'92,21
    Double-Stick Rug Tape Makes Tough Easy		HSM'84:S/O16
    Dovetail jigs, marking-out	Lautard, Guy	TMBR#3:194
    Dovetail Slides	WOLLENBERG, GALE	HSM'82:J/F14
    Dovetail, splines	Lautard, Guy	TMBR#3:193
    Dowel pins	Lautard, Guy	TMBR#2:103;
    Downfeed Scale	WILSON, GLENN L.	PiM-Feb.'94,22
    Downfeed Scale	WILSON, GLENN	PiM-Feb.'89,22
    Drafting, drawing: What does "2 off" mean?	Lautard, Guy	HTIM:47
    Draw bars	CANNER	MEW#29,24
    Drawbar Knocker	WELLS, NORMAN	HSM'98:J/F 47 
    Drawer for a lathe cabinet	REID	MEW#28,22
    Drawer handles from bottle caps	Lautard, Guy	TMBR#3:237
    Drawfiling reliefs on shop-made taps	Lautard, Guy	TMBR#3:23-24
    Drawfiling	Lautard, Guy	TMBR#1:5, 8,
    Drawing Up A Bargain	LAUTARD, GUY	HSM'84:M/J45
    Drawings for a graduated lathe leadscrew handwheel	Lautard, Guy	TMBR#1:71
    Drawings for a machinist's wooden tool chest	Lautard, Guy	TMBR#1:131
    Drawings for simple shop made pantograph	Lautard, Guy	TMBR#3:250
    Dressing abrasive stones flat	Lautard, Guy	TMBR#2:119
    Dressing an abrasive wheel	Lautard, Guy	TMBR#2:65
    Drill Bushings Parts 1-4	HOFFMAN, EDWARD G.	HSM'93:J/A54,S/O54,N/D56;HSM'94:J/F44
    Drill Chuck Adapter		HSM'90:J/A14
    Drill Chuck Adapter	WOOD, GRANT W	HSM'82:S/O52
    Drill depth stop collar for a center drill	Lautard, Guy	TMBR#3:13, 14
    Drill Grinder Attachment Mount	TORGERSON, RICHARD	PiM-Aug.'89,18
    Drill grinding geometry	FALLOWS	MEW#23,16
    Drill Guide Device for the Atlas/Craftsman 6" Lathe, A	REYNOLDS, JIM	MW Jun. 99, 38
    Drill Guide		PiM-Aug.'89,26
    Drill Holder For Lathes		HSM'88:M/A15
    Drill Holder for Your Lathe, h	PEAVEY, GEORGE A.	HSM'85:N/D18 
    Drill modified for drilling plastic	Lautard, Guy	TMBR#3:66
    Drill press as a tapping machine	Lautard, Guy	TMBR#3:173
    Drill Press Chuck Handles	KOUHOUPT, RUDY	HSM'93:M/A39
    Drill Press Modification, A	BIDDLE, H. T.	PiM-Feb.'96, 42
    Drill Press Quill Lock	YOUNG, MARSHALL R.	HSM'92:J/F40
    Drill Press Router Adapter	McLEAN, FRANK A.	HSM'93:M/J38
    Drill Press Safety		HSM'86:M/J14
    Drill Press Speed Reducer	MAUDE, WARD	HSM'93:S/Oi4
    Drill Press Speed Reducer, A	JOHNSON, D. E.	PiM-Feb.'92,16
    Drill Press Table Holding Devices 	HAUSER, JAMES W.	MW Oct. 99, 50
    Drill Press Table	HEDIN, R S	HSM'82:J/F5
    Drill Press Tapping Tool	MASON, HAROLD	HSM'85:N/D24
    Drill Press Vise Restraints	BERGER, JAMES	HSM'92:J/A45
    Drill reamer	Lautard, Guy	TMBR#3:66
    Drill rod - is it "round"?	Lautard, Guy	TMBR#2:70
    Drill Shank Welding fig	CROW, ART	HSM'85:M/J63
    Drill Sharpening Fixture and Point Splitter	HEDIN, R. S.	PiM-Jun.'92,22
    Drill Sharpening Jig	MACEKE	MEW#17,41
    Drill sharpening jigs	Lautard, Guy	TMBR#1:26, 205; TMBR#2:147; TMBR#3:257-8
    Drill Stand For Small Drills	HALL	MEW#13,28
    Drill/mill down feed stop	HALL	MEW#23,55
    Drilling a 0.018" dia. hole	Lautard, Guy	TMBR#2:54
    Drilling a division plate	Lautard, Guy	TMBR#2:7
    Drilling a Hole On Center		HSM'90:J/A14
    Drilling a shaft from both ends	Lautard, Guy	TMBR#2:96
    Drilling a shaft in the mill	Lautard, Guy	TMBR#2:96
    Drilling a truck frame	Lautard, Guy	TMBR#3:19
    Drilling Accurate Holes	BENNETT, NORMAN H.	HSM'86:M/A37
    Drilling Accurately Centered Cross-holes in Round Stock	KOVAL, ROBERT	PiM-Jun.'93,26
    Drilling and Tapping Hints	McLEAN, FRANK	HSM'84:N/D56
    Drilling and Tapping in the Drill Press		HSM'85:J/F16
    Drilling Center Holes Accurately	McLEAN, FRANK A.	HSM'89:J/F56
    Drilling Challenge, A		PiM-Dec.'91,24
    Drilling Holes in Hard Material	METZE, BOB	PiM Aug.'97 29
    Drilling Machine Dividing Unit	YOUNG	MEW#16,12
    Drilling machine safety	HALL	MEW#24,39
    Drilling method from the past	LOADER	MEW#27,30
    Drilling Multiple Holes in Line	WAGNER, BILL	HSM'91:J/A18
    Drilling oversize holes	Lautard, Guy	TMBR#1:155
    Drilling plywood without splintering	Lautard, Guy	TMBR#3:188
    Drilling Square Holes	WINKS	MEW#14,14
    Drilling Steam Passages and Tangents	HASLAM, KENNETH R.	HSM'88:N/D40
    Drilling Tip		HSM'90:M/J15
    Drilling to an exact depth	Lautard, Guy	TMBR#1:20, 70,
    Drilling to size for reaming	Lautard, Guy	TMBR#1:16
    Drilling True		HSM'85:S/O16
    Drilling well centered holes in the ends of a bar	Lautard, Guy	TMBR#2:95
    Drilling With Accuracy		HSM'90:N/D15
    Drilling With Accuracy	McLEAN, FRANK A	HSM'88:S/O54
    Drills And Drilling	LOADER	MEW#11,14
    Drills for Mill Cutters		PiM-Jun.'90,3
    Drills From Flat Stock	JONES	MEW#12,70
    Drip Oiler	VREELAND, DON H.	PiM-Aug.'92,32
    Drop Cord Caddy	CROW, ART	HSM'86:M/A31
    Drop-by-drop Cutting Fluid	YAMAMOTO, MICHAEL	PiM-Feb.'93,28
    Dual drive belt advice	Lautard, Guy	TMBR#3:58
    Dual set screws for V-belt pulleys, etc.	Lautard, Guy	TMBR#1:44; TMBR#3:175
    Duplicating Radii	ROSCOE, LOWIE L., JR	PiM-Apr.'95 24
    Dust control from Medite	Lautard, Guy	HTIM:1
    Dust control	Lautard, Guy	HTIM:44; TMBR#3:203
    Dust control, as a health hazard	Lautard, Guy	TMBR#3:203-204
    Dye Applicator	NOBLE, BURT	PiM-Jun.'93,3
    Ear cleaning syringe is handy	Lautard, Guy	TMBR#3:237
    Easy Indicator, An	LAMANCE, THOMAS	PiM-Aug.'92,3
    Easy rolling shop trolleys	Lautard, Guy	HTIM:46
    Easy Way to Cut Metric Threads	LIND, JACK R.	HSM'95:M/A21 N/D24
    Easy Way to Make a Multi-position Tool Post, An	BARBOUR, J. O., JR.	PiM-Jun.'93,30
    Easyset tailstock die holder	WASHINGTON	MEW#27,55
    Easy-to-build C-clamps	CROW, ART	PiM-Feb.'94,22
    Economical Large-Hole Drilling	WALKER, RICHARD B.	HSM'88:M/J18 
    Economical X-axis Readout, An	MUELLER, FRAN	PiM-Dec.'90,18
    Economy Substitute for a Bridgeport	ERNEST, JOHN F.	PiM-Oct.'92,24
    Edge Finder, An	SPARBER, R. G.	PiM Aug.'97 30
    Edge Finders	CUTTRELL, JIMMY C.	HSM'93:M/J13
    Edge finding: How to make a wiggler	Lautard, Guy	TMBR#3:92
    Edge finding: Purpose of the bent shaft in a wiggler outfit	Lautard, Guy	TMBR#3:93
    Edge finding: Spud + boring head	Lautard, Guy	TMBR#3:96
    Edge finding: Spuds, bugs and wigglers	Lautard, Guy	TMBR#3:92-96
    Edge finding: The "Sticky Pin"	Lautard, Guy	TMBR#3:96
    Edge finding: What makes a wiggler work?	Lautard, Guy	TMBR#3:92-93
    Edge Gage	MADISON, JAMES	PiM Jun.'97 33
    EDM Safety (Chips & Sparks)	WELLS, NORM	HSM'95:M/J19 S/O20
    Effects of errors in squareness	Lautard, Guy	TMBR#2:19
    Eight-tube Wind Chimes	HOWARD THOMAS F.	PiM-Dec.'91,14
    Electic Motors-AC	HALL	MEW#15,17
    Electric Arc Welding	BRAY	MEW#12,62
    Electric Discharge Machining (EDM)	MEADOR, HANK	HSM'91:J/F42
    Electric Edge Finder		HSM'87:M/J14
    Electric Motors DC	HALL	MEW#16,66
    Electric Motors for Stationary Power Tools	DOUGLAS, ALAN	HSM'95:N/D52
    Electric Motors	LAMPARTER, ROBERT W.	HSM'87:J/A47
    Electrical Discharge Machining Part 5 Head and EDM Operation, The	LANGLOIS, ROBERT P.	HSM'96:J/F34
    Electrical Discharge Machining Part 6 Other Odds and Ends	LANGLOIS, ROBERT P.	HSM'96:M/A37
    Electrical Discharge Machining --Removing Metal By Spark Erosion Parts 1-4	LANGLOIS, ROBERT P.	HSM'95:M/J22 J/A40 S/O34 N/D34
    Electrical extension cord caddy, WARNING: may be dangerous	Lautard, Guy	TMBR#3:33-34
    Electrical Phase Converter for Shop Motors	EVANS, R. W.	PiM-Feb.'96, 28
    Electrode Selection	HUNT, CHARLES K	HSM'83:J/F22
    Electronics engineer -- mech drive	SHEPPARD	MEW#30,38
    Elegant Ball Turning Tool	SWALLOW	MEW#11,44
    Elegant Long Reach Thickness Caliper	CROW, ART	PiM-Feb.'95 12
    Elevating a Vertical Mill	KOUHOUPT, RUDY	HSM'91:M/A54
    Eliminate Headache Potential	HOWARD, JOSEPH P.	HSM'86:N/D14
    Eliminating Chips		HSM'88:N/D17
    Elliptical Rotary Engine	HEDIN, R. S.	PiM-Apr.'90,4
    Emco Maier Dl-4" Cam Lock Fixture Plate; Product Review	LINDQUIST, DAVID	HSM'96:J/F 22
    Emergency Drill Press Jig		PiM-Oct.'90,3
    Emergency Source		HSM'91:J/F11
    Emery Cloth Substitute	BENDER, BRIAN	HSM'92:S/O14
    Emery sticks	Lautard, Guy	TMBR#2:14
    Enco 12 x 26" Geared Head Engine Lathe: A Review	LAWSON, CLIFTON E. R.	HSM'93:N/D44
    End Mill Sharpening Fixture	HEDIN, R. S.	HSM'85:J/A22
    End Mill Sharpening Holding Fixture	CROW, ART	PiM-Aug.'92,26
    End Mill Sharpening Jig	COOPER, JOHN A.	PiM-Oct.'95 23
    Engine Turning	BIGANEISS, DONALD	HSM'93:N/D14
    Engine Turning	ELLIOTT, GENE	PiM-Aug.'89,22
    Engine Turning	MARCHESE, BOB	PiM-Aug.'89,22
    Engineering Plastics	DOWLING, THOMAS W. III	HSM'96:J/F 33
    Engineers Level	HALL	MEW#10,38
    Engraving a feedscrew dial	Lautard, Guy	TMBR#1:43, 48-49
    Engraving Attachment	UNWIN	MEW#10,11
    Engraving cutters	Lautard, Guy	TMBR#2:36
    Engraving Pantograph	KOUHOUPT, RUDY	HSM'90:N/D24
    Enlarging the Ejection Port	ACKER, STEVE	PiM-Aug.'96, 32
    Equation defining the points on a circle	Lautard, Guy	TMBR#1:73
    Equipment Lights	HOLM, PAUL	PiM Aug.'97 26
    Errata note re 30/40 Krag chamber in 30/06 chamber	Lautard, Guy	TMBR#2:126
    Errata	SEXTON, TERRY	MW Aug. 99, 49
    Errors in measuring, effect of	Lautard, Guy	TMBR#1:11
    Erten Machining Center, The	BEN-AARON, MAX	HSM'98:S/O 33
    Etching off a too-high polish with nitric acid	Lautard, Guy	TMBR#3:138
    Etching on metal	Lautard, Guy	TMBR#3:244 & 254
    Etching	Lautard, Guy	TMBR#1:136
    Every Pot Finds Its Own Lid	LAUTARD, GUY	HSM'84:M/A24
    Everything in Its Place		HSM'87:J/A16
    Evolution of drilling Ik drills	UNWIN	MEW#29,52
    Evolution Of The Lathe, Parts l-2	UNWIN	MEW#15,58;#16,46
    Exact Lengths Easily		PiM-Apr.'88,24
    Exact-T-Guide cutting aid for sheet goods	Lautard, Guy	TMBR#3:190
    Excerpts from The Federal Firearms Regulations Guide	DOCKERY, KEVIN	HSM'94:S/O42
    Expanding Lathe Capability		HSM'85:M/A17
    Expanding Mandrels	DELONG, JAMES	PiM Aug. '98 31
    Expanding Your Arbor Press Capability	TURNER, JOHN E.	PiM-Oct.'92,30
    Experimental Helical Milling Attachment	SEXTON, TERRY	MW Jun. 99, 12
    Extend the Capacity of Your Milling Machine	REISDORF, GARY F	HSM'86:S/O28
    Extending Blade Life	KNITTLE, MARK Q.	HSM'92:M/J13
    Extending Drills and Center Drills	McALLISTER, DENNIS E	PiM-Aug.'94,MN
    Extension for a small drill chuck	Lautard, Guy	TMBR#2:104
    External Threads Part 1	McLEAN, FRANK	HSM'84:S/O50
    Extra Hand, An	LAMANCE, THOMAS	PiM-Oct.'92,3
    Extra Length Combined Drill and Countersinks	YAMAMOTO, MICHAEL T.	HSM'84:M/A18
    Extra Probes for the Lincoln Center Finder	GOLDING, MARK	PiM-Aug.'94,32
    Extra Set of Jaws		HSM'86:N/D13
    Extruding lead wire	Lautard, Guy	TMBR#3:77
    Eyebolt Chuck		PiM-Aug.'89,28
    E-Z Bore	ERICKSON, DONALD	HSM'98:S/O 37
    Fabricated Drawing Board	VAGG	MEW#14,31
    Fabricated faceplate -- Unimat	LOADER	MEW#25,43
    Fabricated vice	LOADER	MEW#26,18
    Fabricating the Tumbler Link	HOLDEN, D. W.	HSM'84:N/D32
    Faceplate Removal	BLANDFORD, PERCY	PiM-Apr '95 32
    Faceplate Toolholder, A	THOMSON, D. M.	HSM'97:M/A 45
    Faceplate/Angleplate Clamps	HALL	MEW#20,24
    Faceplates and Such Parts I, II	LAMARCHE, ROBERT E	HSM'82:M/J18,J/A29
    Faceplates for Gap Bed Lathes	MAYKOSKI, TOM	PiM-Apr.'93,12
    Facing Thin Pieces	MARX, ALBERTO	HSM'86:J/A30
    Facing to Accurate Length	MELTON, L. C.	HSM'94:J/F40
    Farm Show Magazine	Lautard, Guy	TMBR#3:109
    Farm tractor carb repairs	Lautard, Guy	TMBR#3:217
    Farrier's Forge	HUARD, CONRAD	PiM-Aug.'95 17
    Fast Dressing of Band Saw Welds, A	DOOLIN, THOMAS J.	HSM'97:J/A 25 
    Fast removal of tap cuttings	Lautard, Guy	TMBR#2:125
    Fast way to dial in the head of a vertical mill	Lautard, Guy	HTIM:33; TMBR#3:84
    Fastener Gauge	KELLER, PHIL	PiM-Oct.'90,8
    Fear Neither Sphere Nor Hemisphere	DEAN, JOHN	HSM'84:N/D50
    Federal File Co.	Lautard, Guy	TMBR#3:256
    Feed and Speed Calculator	ROSENTHAL, BRIAN	MW Oct. 99, 43
    Feed Lever Tapping Aid	HAYNES	MEW#9,10
    Fenton, Bill	Lautard, Guy	TMBR#1:4, 182, 191; TMBR#2:22
    Few Good Hints, A	HAINES, C. LAWRENCE	HSM'98:J/A 24 
    Few Thoughts on Shapers, A	McLEAN, FRANK A.	HSM'97:M/J 51
    Fifteen Minute Expanding Mandrel	WOOD, GRANT W	HSM'82:N/D37
    Figuring Arc Radius		HSM'90:M/J15
    Figuring the tapping size hole for any thread	Lautard, Guy	TMBR#1:19
    File brushes	Lautard, Guy	TMBR#1:6
    File cleaning on wire wheel brush	Lautard, Guy	TMBR#3:108
    File handle ferrules made from compression nuts	Lautard, Guy	TMBR#3:107
    File handles that fit your hand	Lautard, Guy	TMBR#3:107
    File selection	Lautard, Guy	TMBR#3:71
    File storage	HALL	MEW#25,29
    File Them Away	GREGRICH, ARNOLD	HSM'92:N/D14
    Files and Filing Parts 1-3	HOFFMAN, EDWARD G.	HSM'94:S/O47,N/D50, HSM'95:J/F48
    Files And Filing	LOADER	MEW#16,50
    Filing buttons	Lautard, Guy	TMBR#2:106
    Filing Flat		PiM-Apr.'89,24
    Filing for 'flat" and "finish"	Lautard, Guy	TMBR#3:15 1
    Filing in the lathe	Lautard, Guy	TMBR#1:7
    Filing off that last half thou	Lautard, Guy	TMBR#3:139
    Filing Rest For The Sherline Lathe, A	SMITH, W. R.	HSM'98:M/J 26
    Filing Rest	BRAY	MEW#9,20
    Filing technique	Lautard, Guy	TMBR#1:7-8
    Filling a Boring Bar	HUGHES, ED	HSM'97:J F J/F
    Filling voids in plywood	Lautard, Guy	TMBR#3:188
    Finding and Making Gun Parts	ACKER, STEVE	MW Oct. 99, 48
    Finding lost tools	Lautard, Guy	TMBR#3:73
    Finding Material		HSM'87:J/A17
    Finding the Center		HSM'86:M/J14
    Finding the Diameter		HSM'86:S/O19
    Finding the Diameter		HSM'90:S/O14
    Finding the Drill	McEVOY, TIM	PiM Oct.. 94, MN
    Finding the Hole		PiM-Dec.'91,24
    Finding the Socket		PiM-Oct.'89,3
    Finding the Wrench Hole		PiM-Aug.'88,24
    Fine Cuts	LaMANCE, 'I'HOMAS	PiM-Jun.'96, 41
    Fine Downfeed for the Jet Mill/drill, A	TUMELSON, JAMES G.	PiM-Feb.'96, 26
    Fine Feed Attachment for a Vertical Mill, A Parts 1, 2	WADHAM, G.	HSM'97:S/O 24, N/D 32
    Fine toothed hacksaw blades	Lautard, Guy	TMBR#3:256
    Finger joints	Lautard, Guy	TMBR#3:194
    Finger plate	Lautard, Guy	TMBR#1:88-89, TMBR#3:79
    Finger Treadle	PETERSEN, BIRK	PiM-Jun.'91,4
    Finishing aluminum with a flap wheel	Lautard, Guy	TMBR#2:115
    Finishing Contoured Metal Castings	ROUBAL, WM. T., Ph.D.	HSM'82:S/O41
    Fire Safety Parts 3-5	HOFFMAN, EDWARD G.	HSM'84:J/F56,M/A64,M/J63
    Fire Safety	HOFFMAN, EDWARD G.	HSM'83:S/O64,N/D64
    Firewall grommet-making for aircraft	Lautard, Guy	TMBR#3:56
    First Look		HSM'88:J/F57,M/A58,M/J57,J/A58,S/O58,N/D59
    First Project: A Knockout Bar	YOUNG, BARRY	MW Jun. 99, 46
    First steps -- useful tools	SCON	MEW#30,23
    Fitting Small Drill Chucks	McLEAN, FRANK A.	HSM'92:J/F52
    Fitting washers - which side up?	Lautard, Guy	HTIM:31
    Five Quickies	LANGAM	MEW#13,32
    Five-Layer "Lazy Susan" Drill Index	GASCOYNE, JOHN	HSM'84:N/D36
    Fixed Steady Rest Parts 1, 2	KOUHOUPT, RUDY	HSM'86:M/A56,M/J56
    Fixture for Milling End Curves, A	KOUHOUPT, RUDY	HSM'94:S/O50
    Fixture for Milling the Recoil Lug, A	ACKER, STEVE	PiM-Feb.'96, 34
    Fixture Keys	HOFFMAN, EDWARD G	HSM'92:J/A58
    Fixture Plate for a Lathe or Mill, A	STARNES, RAY E.	HSM'91:M/A30
    Fixture to Hold Small Pieces	HASBROUCK, RAY	PiM Apr. '98 30
    Fixturing With Collets Parts 1-3	HOFFMAN, EDWARD G.	HSM'96:M/J 60 J/A60 N/D 62
    Flame Cutter	VERITY, THOMAS M.	HSM'90:S/O50
    Flare Nut Adapter Tool	HOFF, MIKE	PiM-Aug.'92,19
    FLASH-Making a Good Weld	HUNT, CHARLES K	HSM'82:J/A16
    Flat Steel Springs		HSM'91:M/A15
    FlexArm System; Product Review	HOFFMAN, EDWARD G.	HSM'96:J/F 23
    Floating Chucks	JACOT, MICHEL	HSM'99:J/A 24
    Floating Drill Press Vise		HSM'89:J/A12
    Floating Drive, A	LEMANCE, THOMAS	HSM'98:J/A 24
    Floating reamer chuck	JEEVES	MEW#24,35
    Flower arranging rod as a welding rod	Lautard, Guy	TMBR#2:124
    Flute spacing: uniform or non-uniform	Lautard, Guy	TMBR#1:101
    Flute Your Own Rifle Barrel	JOHNSON, NORMAN E.	MW Aug. 99, 26
    Fly Cutter and Angle Plate	KOUHOUPT, RUDY	HSM'88:J/F54
    Fly Cutter	GENEVRO, GEORGE	PiM-Dec.'89,18
    Flycutter made from a 2-flute end mill	Lautard, Guy	TMBR#3:12
    Flycutters	McLEAN, FRANK	HSM'84:M/J56
    Flying Dog Protection	LAMANCE, THOMAS	PiM-Apr.'92,3
    Follower Rest	HOLM, PAUL	PiM Aug.'97 26
    Foot operated saw table	BROOMFIELD	MEW#23,38
    Foot Switch For A Drilling M	COE	MEW#15,30
    For A Good Look		HSM'84:J/F16
    For Unobstructed Milling, Keep a Low Profile	COOPER, JOHN A.	PiM-Dec.'96, 20
    Fore Word	RICE, JOE	PiM Feb. Aug. Dec. '98 3
    ForeWord	McKINLEY, CLOVER	PiM Apr., Jun. '98 3
    ForeWord	MCKINLEY, CLOVER	PiM-Oct.'95 3
    Foreword	RICE, JOE	MW Feb. 99, 3, Apr. 99, Aug. 99, 5, Dec. 99, 5 
    ForeWord	RICE, JOE	PiM Apr-Aug Dec '97 3
    ForeWord	RICE, JOE	PiM-Feb. Apr. Jun.-Aug. Dec '95 3
    ForeWord	RICE, JOE	PiM-Feb.-Jun, Oct-Dec '96, 3
    Foreword	WILSON, GLENN L.	MW Oct. 99, 5
    Forming Scale Bolts and Nuts on the Lathe	HOFF, MICHAEL	PiM Jun.'97 4
    Found Materials	SWITZER, GENE	HSM'98:J/A 24
    Foundry-Don't Fake a Casting,  Make a Casting	LEWIS, JAMES R.	HSM'87:M/J48
    Foundry-Don't Fake a Casting, Make A Casting The Pattern Part 1-6	LEWIS, JAMES A	HSM'85:J/F52,M/A52,M/J42,J/A52,S/O48,N/D50
    Foundry-Metals for Casting Parts 1-6	LEWIS, JAMES R.	HSM'86:J/F47,M/A47,M/J46,J/A48,S/O50,N/D48
    Four Jaw Independent Lathe Chuck	JOHNSON, PAUL K	HSM'82:J/A26
    Four way carriage stop	MORRIS	MEW#25,41
    Four-Station Grinder, A	SCHARPLAZ, JAMES	PiM-Oct.'88,4
    Free Machining Steel	KEET, A.	HSM'93:J/A18
    Free Pendulum Clock Part 1 Introduction and overview	BOUCHERON, PIERRE H.	HSM'91:M/A20
    Free Pendulum Clock Part 2 The bob and air losses	BOUCHERON, PIERRE H.	HSM'91:M/J34
    Free Pendulum Clock Part 3 Electronics	BOUCHERON, PIERRE H.	HSM'91:J/A40
    Free Pendulum Clock Part 4 Setup and general considerations	BOUCHERON, PIERRE H.	HSM'91:S/O40
    Free Rotary Burrs		HSM'89:J/A12
    Freedom Tripod Head, A	WILSON, GLENN L.	PiM-Apr.'96, 4
    Freehand Twist Drill Sharpening	DREWNIAK, JOSEPH A.	HSM'87:J/F34
    Free-standing Lathe Toolholder, A	SCHWEINFURTH, LUDWIG	MW Feb. 99, 28
    Fret Saw/Filing Machine	GRAY	MEW#12,12
    Fretsaw att for the lathe	GAULD	MEW#28,48
    From drilling to milling vice	HALL	MEW#23,50
    From My Shop to Yours Parts 1, 2	HOLM, PAUL J.	HSM'86:M/A34,M/J38
    From Pain to Pleasure	PLOTKIN, CHUCK	PiM Oct. '98 25
    From Shears to Brake: A Boxing Story	MASON, HAROLD	PiM-Feb.'92,4
    From Steam Arm to Elgamill	MASON,HAROLD	HSM'89:M/A22
    From the Editor	McKINLEY, CLOVER	HSM'96:S/O 4
    From the Editor	McKINLEY, CLOVER	HSM'97:J/A 2
    From the Editor	McKINLEY, CLOVER	HSM'98:J/A 4 
    From the Editor	RICE, JOE	HSM'83:J/F2,M/A2,M/J2,J/A2,S/O2,N/D2
    From the Editor	RICE, JOE	HSM'84:J/F2,M/A2,N/D2
    From the Editor	RICE, JOE	HSM'85:M/A2,M/J2,J/A2,S/O2,N/D2 
    From the Editor	RICE, JOE	HSM'88:Jan through Dec
    From the Editor	RICE, JOE	HSM'94:J/F,M/J-N/D2
    From the Editor	RICE, JOE	HSM'95:M/A-N/D2
    From the Editor	RICE, JOE	HSM'96:J/F 2, M/A 4, J/A 4,S/O 4, N/D 4
    From the Editor	RICE, JOE	HSM'97:J/F-M/A 4, M/J 2, S/O-N/D 4 
    From the Editor	RICE, JOE	HSM'98:J/F 4, M/A 4 M/J 4, S/O 6, N/D 4
    From the Editor	RICE, JOE	HSM'99:J/F N/D 4
    From the Files of the Primitive Machine Shop	WOLLENBERG, GALE	HSM'82:S/O50
    Fruit acid - effect on tools	Lautard, Guy	TMBR#1:62
    Furnaces For the Home Foundry		HSM'82:J/A34
    Further Comments--Belt Sander	TAYLOR	MEW#10,74
    Fused glass car badges	Lautard, Guy	TMBR#3:246
    FWW article on dovetailing cited	Lautard, Guy	TMBR#3:193-194
    FWW article on plywood referenced	Lautard, Guy	TMBR#3:191
    Galvanized sheet metal	Lautard, Guy	TMBR#3:103
    Garden Gate	REID	MEW#12,43
    Gas Tungsten Arc Welding Parts I, II	HUNT CHARLES K.	HSM'84:J/F22,M/A26
    Gasket Cutter	CLAUDE, ROGER	PiM-Aug.'94,3
    Gasket in a Hurry, A	BAEHRE, HERB	PiM Aug.'97 31
    Gear Ctttting on the Sherline Lathe Parts 2,3    	SMITH, W. R.	HSM'99:J/F 35  M/A 42
    Gear Cutting Adventures Part 1 Spur Gears and Pinions 	COOPER, JOHN	MW Apr. 99, 8 
    Gear Cutting Adventures Part 2 Helical Gears 	COOPER, JOHN	MW Jun. 99, 23
    Gear Cutting on the Sherline Lathe Part 1 Configuring the Sherline	SMITH, W. R.	HSM'98:N/D 34 
    Gear Cutting With The Shaper		HSM'88:S/O12
    Gear Driven Shapers	REISDORF, GARY F.	HSM'88:S/O48
    Gear Lubrication: Lathe, Mill and Drill		HSM'91:J/F10
    Gear oil, what is it?	Lautard, Guy	TMBR#2:115
    Gear Repair	REISDORF, GARY F.	HSM'89:M/J38
    Gear-cutting Device, A	REYNOLDS, JIM	MW Aug. 99, 8
    Gearcutting	Lautard, Guy	TMBR#2:199
    Geared Rotary Table	FIGES	MEW#30,43
    Gearless Hit 'n Miss Engine Parts 1-4	DUCLOS, PHILIP	HSM'93:M/J16,J/A20,S/O18,N/D29
    Gears -- without complex cutters	HOLT	MEW#28,61
    Gears and gearing	UNWIN	MEW#28,28
    Gears	HOFFMAN, EDWARD G.	HSM'85:S/O19,N/D20 
    General Model 490 Bandsaw	Lautard, Guy	TMBR#3:184
    Generic Crane, A	WENCE, DENNIS K.	HSM'89:J/A40
    Geometric Construction Parts 3-5	HOFFMAN, EDWARD G	HSM'92:J/F15,M/A17,M/J15
    Geometric Construction	LOESCHER, RICHARD J.	HSM'82:M/A38
    Geometric Forms	HOFFMAN EDWARD G	HSM'82:N/D20
    Geometric Forms	HOFFMAN, EDWARD G.	HSM'83:J/F18
    Geometry of a radius tangent to a line and a circle	Lautard, Guy	HTIM:16
    Get a Handle On Your Lathe	GASCOYNE, JOHN B.	HSM'96:N/D 46
    Get a True-running Center Spot		HSM'90:J/F14
    Getting a Better View		PiM-Apr.'89,3
    Getting A Cleaner Cut		PiM-Feb.'88,24
    Getting a drill chuck off and on its arbor	Lautard, Guy	TMBR#3:117
    Getting a fair return for your work	Lautard, Guy	TMBR#1:179
    Getting a New Vise in Shape	NOLAN, PETER	PiM Jun. '98 28 
    Getting a nice finish on screw threads	Lautard, Guy	TMBR#2:112
    Getting a Smooth Finish		HSM'89:N/D15
    Getting more out of rotary tbl	AMOS	MEW#29,60
    Getting Rid of Chips on Your Band Saw	CHRISTOPHERSON, A. M.	PiM-Apr.'93,28
    Getting the Angle		HSM'87:M/J14
    Getting the Most from Your Center Gage and Other Threading Gages	GENEVRO, GEORGE, HOFFMAN, EDWARD G.	HSM'85:M/A38
    Getting the Radius, Again		HSM'88:M/J10
    Getting With the Program	HOWARD, THOMAS F.	HSM'88:J/A16
    Gib key - triangular	Lautard, Guy	TMBR#2:68
    Gibraltar toolpost	Lautard, Guy	TMBR#3:14
    Give Metal Spinning a Whirl	DUCLOS, PHILIP	PiM-Aug.'90,4
    Glass Cutting Helper for your Drill Press, A	NEWCOMB, ROBERT	PiM-Apr.'91,15
    Glendo Accu-finisher	Lautard, Guy	TMBR#3:111
    Gloves for use with a sandblast cabinet	Lautard, Guy	TMBR#3:131,134
    Glue turning black in contact with iron	Lautard, Guy	TMBR#3:195
    Glue, excess - dealing with	Lautard, Guy	TMBR#3:195
    Glued vs. dry vs. rabbeted joints etc.	Lautard, Guy	TMBR#3:192
    Go Further	WEISNER, CARL G.	PiM-Oct.94, MN
    Good counter sinks	Lautard, Guy	TMBR#2:104
    Good Housekeeping Parts 1, 2	HOFFMAN, EDWARD G.	HSM'84:J/A64,S/O60
    Good Lubricant, A		HSM'86:S/O19
    Good old unsalted pork lard	Lautard, Guy	TMBR#2:116
    Good Sources		HSM'89:J/A12
    Good steel for making punches, etc.	Lautard, Guy	TMBR#3:104, 237
    Goodies at rock bottom prices from the right sources	Lautard, Guy	TMBR#3:104
    Graduated saddle stop	MCQUEEN	MEW#24,26
    Grain Growth		HSM'83:M/J14
    Grasping groove cutter	Lautard, Guy	TMBR#1:86
    Gravity operated shut-off button for mill-drill	Lautard, Guy	TMBR#3:25
    Grease Adapter for the South Bend, A	THOMPSON, JACK	HSM'98:M/J 63
    Great Little Clamp, A	PATRICK, BOB	PiM-Aug.'93,12
    Greater Precision for Scroll Chucks	TORGERSON, RICHARD	PiM-Aug.'88,21
    Grinder Cleaning		HSM'91:J/A15
    Grinding and Lapping With Diamond	HESSE, JIM	HSM'88:J/F36
    Grinding Bench, A	McLEAN, FRANK A.	HSM'89:M/A51
    Grinding Tool Bits for a Smooth Cut	BURNS, FRANK E.	HSM'97:J/A 58
    Grinding Wheel Arbor	BERTRAND,JEFF	HSM'85:J/A25
    Grinding Wheel Arbors		HSM'87:M/A14
    Grinding Wheel Dresser		HSM'86:S/O19
    Grinding Wheels	HOFFMAN, EDWARD G.	HSM'85:J/F20
    Grinding Wheels, Safety Tips	HOFFMAN EDWARD G	HSM'82:N/D25
    GripsAll Indicator Base	TORGERSON, RICHARD	PiM-Aug.'89,4
    Griptru chuck	JEEVES	MEW#27,17
    Grizzly 8 Table Indexing Plates Summary	LAWSON, CLIFTON E. R.	HSM'98:N/D 58
    Grooving Small Shafts		HSM'90:J/F14
    Grow That "Third Hand"		HSM'88:J/F12
    Guest Editorial	BOOTH, KATHY	HSM'96:M/J 4
    Guest Editorial	ITNYRE, BOB	HSM'90:S/O2
    Guest Editorial	JENKINS, DAN	HSM'95:J/F4
    Guest Editorial	KOUHOUPT, RUDY	HSM'90:N/D2
    Guest Editorial	STRUBEL, GILBERT	HSM'90:S/O2
    Guest Editorial	SWINNEY, ROBERT D.	HSM'94:M/A2
    Gunsmith's Workbench, A German Silver Escutcheons	MORROW, LAURIE	HSM'96:J/A 52
    Habilus files	Lautard, Guy	TMBR#3:241
    Hacksaw Cuts Simplified	WILDER, FRED E.	HSM'96:M/A 19
    Hacksaw Cuts	GRASS, JOHN	HSM'98:M/A 22
    Hacksaw	Lautard, Guy	TMBR#2:101-102
    Half Center, A	WELLS, NORM	HSM'93:N/D15
    Hammer Work	ACKER, STEVE	PiM-Apr.'96, 38
    Hanchett knife grinder; plywood lathe knives	Lautard, Guy	TMBR#1:117
    Hand chasing a thread	Lautard, Guy	TMBR#1:191
    Hand Mill Restoration	SCHARPLAZ, JIM	PiM-Apr.'96, 14
    Hand punches explained	LOADER	MEW#28,18
    Hand shapers and vee blocks	HALL	MEW#32,40
    Hand stamps don't "shoot straight"	Lautard, Guy	TMBR#2:110
    Hand stamps for uniform marking	Lautard, Guy	TMBR#2:24
    Hand Turning on the Lathe	MCLEAN, FRANK A.	HSM'95:J/F56
    Hand turning	READ	MEW#30,12
    Handling a fine square	Lautard, Guy	TMBR#2:64
    Handling Large Bore Tubing	DURLING, H.R., Jr.	HSM'83:M/J47
    Handwheel Modification on a Sherline Mill	SEWELL, W. L.	PiM-Apr.'95 43
    Handy Deburring Tool	JONES, BRUCE	HSM'88:M/A34
    Handy File Cleaner, A	ACKER, STEVE	HSM'93:M/A42
    Handy Graduating Tool, A	SEXTON, TERRY	PiM Apr.'97 4
    Handy Holdit Brothers		HSM'86:M/A14
    Handy screw jacks	JEEVES	MEW#23,12
    Handy Shop Odds and Ends	COLLINS, MARSH	PiM Jun. '98 11
    Hanging plate shelf for your lathe or milling machine	Lautard, Guy	HTIM:5, 6
    Hard Face Welding of a Cutting Edge Lip		HSM'87:J/F19
    Hardened vs. cast iron heads for combination sets	Lautard, Guy	TMBR#3:106
    Hardened vs. cast iron heads for combination squares	Lautard, Guy	TMBR#3:106
    Hardness Tester	HINSHAW, LOU	PiM-Apr.'89,21
    Harken yacht fittings	Lautard, Guy	TMBR#3:52
    Harmonographs	Lautard, Guy	TMBR#1:142
    Hart multi purp grind rest, Parts 1,2	HALL	MEW#21,46;#22,22
    Head Spindle	HIBBARD, WILLIAM D.	PiM-Aug.'94,32
    Headstock Angle Adjuster for the Sherline 4000 Lathe	DENNING, JOHN H.	HSM'98:J/F 66
    Headstock Belt the Easy Way	MYERS, BOB	HSM'93:S/O14
    Heat required to break a Loctite bond	Lautard, Guy	TMBR#1:115
    Heat treating & hardening trigger & sear parts	Lautard, Guy	TMBR#3:149
    Heat treating & hardening trigger/sear parts	Lautard, Guy	TMBR#3:149
    Heat treating a small drill rod cutter	Lautard, Guy	TMBR#1:45
    Heat Treating Basics	ACKER, STEVE	HSM'91:S/O28
    Heat-treatment Processes for Engine Components	GENEVRO, GEORGE	HSM'95:M/A46
    Heavy aluminum vise jaws	Lautard, Guy	TMBR#3:76
    Heavy Duty Belt Grinder, A	CROW, ART	PiM-Dec.'93,9
    Heavy duty scraper	Lautard, Guy	TMBR#3:237
    Heavy web dive belting as vise jaw liners	Lautard, Guy	TMBR#3:69
    Heavy-Duty Centers	PARSHALL, CHET	HSM'84:M/A63
    Height Gage Conversion and Attachments	TORGERSON, DICK	PiM-Dec.'91,4
    Height gage from an engine valve	Lautard, Guy	TMBR#3:237
    Height Gage	JENKINS, LEWIS J.	HSM'84:M/J10
    Height Gauge Using Inside Mic	SMITH	MEW#18,29
    Helical Springs Part 1-2	HIRAOKA, KOZO	HSM'87:M/J20,J/A30
    Henteleffs #9, a gun cleaning solvent recipe	Lautard, Guy	TMBR#3:168
    Hex Screw Stock	DRAYSON, D. A.	PiM-Jun.'96, 41
    Hex Wrench Extension	MCDOWELL, THEODORE R.	PiM-Apr.'93,20
    High-efficiency Screw Press, A	JOHNSON, D. E.	PiM-Aug.'91,9
    Hinge Centering Punch	McLEAN, FRANK A.	HSM'93:N/D54
    History of the milling machine	UNWIN	MEW#23,60
    Hobbing concave knurling wheels	DERMOTT	MEW#23,37
    Hobby Businesses	BATTERSBY, MARK E.	HSM'86:S/O44
    Hobbymat to Myford adaptor	WALTERS	MEW#24,64
    Holder for 13/16" Dies, A	KOUHOUPT, RUDY	HSM'92:J/F42
    Holding Adjustable Centers (Tips & Tricks)	LAMANCE, THOMAS	PiM-Apr.'95 39
    Holding Adjustable Centers	LAMANCE, THOMAS	PiM Dec. '97 4
    Holding Countersunk Screws	UNWIN	MEW#19,54
    Holding Difficult and Odd-shaped Parts for Machining		PiM-Oct.'95 43
    Holding Larger Shafts		HSM'86:N/D13
    Holding Material in Place		PiM-Feb.'89,24
    Holding Material in Place	LAMANCE, THOMAS	PiM-Apr.'93,3
    Holding Small Objects	TAFT, GEORGE L.	HSM'84:N/D17
    Holding Small Threading Dies	BROWN, CHARLES	HSM'96:N/D 20
    Holding some odd shaped parts in the mill vise	Lautard, Guy	TMBR#3:71
    Holding The Chuck		HSM'88:J/F12
    Holding the Drill Chuck Arbor		HSM'89:J/F12
    Holding Thin Material for Machining	COOPER, JOHN A.	PiM-Feb.'92,12
    Holding thin workpieces in the lathe chuck	Lautard, Guy	TMBR#1:69
    Holding threaded items in a coil of wire	Lautard, Guy	TMBR#3:218
    Holding Work		HSM'88:N/D17
    Hole Aligning Clamps	CLEGG	MEW#18,44
    Hole Enlargement		PiM-Dec.'91,24
    Hole Gauges	HALL	MEW#15,56
    Hole Locating	ROSCOE, LOWIE L., JR	PiM-Apr.'96, 10
    Hole Punch for Thin Material, A	BRUCE, FRED	PiM -Apr.'95.30
    Home Designed & Built Power Table Drive for a Mill-drill Machine, A	COOPER, JOHN A.	PiM Feb.'97 4 
    Home Sandblasting Cabinet	LAVENUTA, FRED	PiM-Dec.'94,30
    Home Shop Metal Melter, Part 1-5	PILZNIENSKI, JOHN F.	HSM'89:J/F24,M/A46,M/J27,J/A36,S/O27
    Home-built Gearbox For Your Atlas 6" Lathe	PETTIT, GLENN	PiM-Dec.'92,6
    Home-Built Motor Reversing Switch		HSM'86:J/F39
    Homemade Air Compressor	KOLAR, GEORGE	HSM'93:N/D14
    Homemade Arbors	McLEAN, FRANK A	HSM'88:J/F48 
    Homemade Bench Mill, A	McKNIGHT, JAMES S.	HSM'91:J/A42
    Homemade Center Punch		HSM'87:J/A17
    Homemade Counterbores	MCLEAN, FRANK A.	HSM'95:S/O54
    Homemade Die Filer, A	KALB, MELVIN L.	HSM'95:M/A48
    Homemade Disk Sander A		HSM'82:S/O36
    Homemade Electric Motor Mount, A	WALKER, RALPH T.	HSM'92:M/J42
    Homemade Hydraulic Press		HSM'85:J/F14
    Homemade Wheel Balancer, A	PETERSEN, BIRK	PiM-Oct.'96, 22
    Honing lathe tools	Lautard, Guy	TMBR#2:122
    Honing lubes	Lautard, Guy	TMBR#2:118-119; TMBR#3:165
    Horizontal Band Saw Parts 1-3	McKNIGHT, JAMES	HSM'99:M/J 46
    Horizontal Milling Attachment Part 1-2	MCLEAN, FRANK A.	HSM'95:M/A40 M/J48
    Horizontal Toggle Clamps	HALL	MEW#10,54
    Hot Bluing Steel	ACKER, STEVE	HSM'96:S/O 28
    Hot Dip Tool Protection	TORGERSON, DICK	PiM-Apr.'92,14
    Hot to Get to the Center of Things		HSM'82:S/O46
    How and Why of Tangential Cutting, The	BURKE, DESMOND	HSM'96:M/J 28
    How calipers were made, & details of the hinge joint	Lautard, Guy	TMBR#3:22
    How Healthy is Your Shop?	HANSON, WAYNE	PiM Dec. '97 18
    How I Almost Became a Millionaire	LIVINGSTON, JESSE	HSM'97:J/F 62
    How not to lose springs	Lautard, Guy	TMBR#3:141
    How not to remove a milling machine arbor	Lautard, Guy	TMBR#3:226
    How to bolt down a bench lathe	Lautard, Guy	HTIM:34
    How to Broach Small Holes	McLEAN, FRANK	HSM'85:M/A56
    How to Deal with Cranks and Eccentrics	JENKINS, DAN	HSM'87:N/D24
    How to Dial a Taper		HSM'90:J/F14
    How to dress up hand stamped markings	Lautard, Guy	TMBR#1:86; TMBR#2:110
    How to Equally Divide A Pie	DEAN, JOHN	HSM'82:M/A14
    How to Get Things in Line Again	DEAN, JOHN	HSM'82:J/A11
    How to Get to the Center of Things	DEAN, JOHN	HSM'82:S/O46
    How to machine a gib strip	Lautard, Guy	TMBR#3:67
    How To Machine a Vee Block on a Vertical Milling Machine	McLEAN, FRANK	HSM'83:S/O52
    How to Machine an Angle Plate	McLEAN, FRANK	HSM'84:M/A56
    How to Make a Chuck Backplate	McLEAN, FRANK A.	HSM'96:S/O 52
    How to make a dovetail grip dial indicator clamp	Lautard, Guy	TMBR#2:84
    How to make a master reference square	Lautard, Guy	TMBR#2:10
    How to make a protective case	Lautard, Guy	TMBR#2:10, 15
    How to Make a Skeleton Wall Clock Parts 8-12	SMITH, W. R.	HSM'95:J/F37 M/A22 M/J39 J/A32 S/O44
    How to Make a Skeleton Wall Clock Parts l-7	SMITH, W. R.	HSM'93:N/D22;HSM'94:J/F29,M/A24,M/J36,J/A20,S/O28,N/D25
    How to Make a Special Tap	McLEAN, FRANK	HSM'86:J/F44
    How to make a square hole sleeve	Lautard, Guy	TMBR#2:88
    How to Make a Tapered End Mill	McLEAN, FRANK A.	HSM'97:M/A 56
    How to Make Quality Photos of Machined Projects at Home	IVY, DENNIS	HSM'85:J/F38
    How to quench a circular die	Lautard, Guy	TMBR#1:120
    How to Replace the Damaged Thread on a Drawbar	McLEAN, FRANK	HSM'86:S/O56
    How to restore age-hardened pencil erasers	Lautard, Guy	HTIM:37
    How to Set Up and Use a Drill Grinding Attachment	McLEAN, FRANK A.	HSM'96:M/A57
    How to set up grinding wheels	Lautard, Guy	TMBR#2:114
    How to super-level your lathe	Lautard, Guy	HTIM:34
    How to tap a drawbar hole in a taper shank	Lautard, Guy	TMBR#2:92
    How to Taper Off	DEAN, JOHN	HSM'83:M/A50
    How to use an edgefinder	Lautard, Guy	TMBR#3:93-94
    How to Use the Vertical Milling Machine	McLEAN, FRANK	HSM'84:J/A56
    How Would You Make This Part?	HOLDEN, D. W.	HSM'84:N/D31
    Huff 'n Puff Engine, A	DUCLOS, PHILIP	PiM-Oct.'89,14
    Humble Angle Plate, The	McLEAN, FRANK A	HSM'90:N/D46
    Hydraulic & rubberdraulic locking of a ring on a dial	Lautard, Guy	TMBR#1:7TMBR#1: TMBR#2:123
    Hydraulic Press Substitute		HSM'90:M/A16
    Ideas for master vernier protractor wanted	Lautard, Guy	TMBR#2:85
    Imitation ivory	Lautard, Guy	TMBR#1:132
    Improve on an Idea		PiM-Oct.'90,3
    Improve Your Lathe Drawbar	NYMAN, PHIL	HSM'99:S/O 34
    Improve Your Mill/Drill Machine	DAVIDSON, BILL	PiM-Oct.'89,4
    Improved Atlas 6" Lathe Gear Cover	LUCHESSA, C. M.	HSM'87:J/A52
    Improved Chuck Boards	HALL	MEW#11,50
    Improved Lathe Drive, An	WADHAM, G.	HSM'92:S/O24
    Improved Tooling for Threading and Boring with the Unimat DB200 Lathe	CLARKE, THEODORE M.	PiM Aug. '98 22
    Improvement for the Atlas 6" Lathe	MILSTER, CONRAD	HSM'83:M/A44
    Improvement to the Kraemer Power Feed, An	TELLESON, NORMAN	PiM-Dec.'94,MN
    Improvements to the Vertical/ horizontal Cutoff Saw	WELLS, NORM	PiM Dec. '98 40
    Improving a Milling Machine Vise	McLEAN, FRANK A.	HSM'91:J/F56
    Improving A Milling Vice	HALL	MEW#12,49
    Improving the Collet Draw Tube	MCLEAN, FRANK A.	HSM'92:M/A49
    Improving the Horizontal/Vertical Band Saw	McLEAN, FRANK A.	HSM'94:N/D58
    Improving the Lathe Steady Rest	JOHNSON, NORMAN E.	PiM Dec. '98 34
    Improving the Quick-change on a Small Lathe	FETTER, E. T.	PiM-Apr.'91,20
    Improving your Lathe With A Dial Indicator	KWASNIEWSKI, GEORGE A	HSM'82:J/A39
    Improving Your Vertical Mill	McLEAN, FRANK	HSM'86:M/J48
    Improvised Small End Mills		PiM-Apr.'91,24
    In Ireland - making architectural stuff	Lautard, Guy	TMBR#3:209
    In Lieu of a Thread Cutting Dial	SNOW, HARRY U.	HSM'94:J/A16
    In my shop	Lautard, Guy	HTIM:51
    Incra-Jigs	Lautard, Guy	TMBR#3:194
    Index the Indexing Ring		PiM-Feb.'90,3
    Index with R8 Collets, An	COOPER, JOHN	PiM Oct. '98 4
    Indexing and Dividing	JOHNSON, D. F.	HSM'98:N/D 28
    Indexing Centers, Parts 1, 2	KOUHOUPT, RUDY	HSM'98:S/O 59, N/D 42
    Indexing Chuck	EVENISS	MEW#14,18
    Indexing Device, An	DUBOSKY, ED	HSM'90:S/O20
    Indexing holes in the rim of a chuck backplate	Lautard, Guy	TMBR#3:65
    Indexing on Small Lathes	ROUBAL, WILLIAM T (TED)	HSM'86:J/A46
    Indexing Parts in a Set	DARNER, RONALD G.	HSM'98:J/F 63
    Indexing Pin		HSM'91:M/A15
    Indexing Template for Easier Layout	HOFFMAN, EDWARD G	HSM'92:J/F29
    Indexing	HOFFMAN, EDWARD G.	HSM'83:S/O22
    Indicating & "Picking Up" Parts 1-4	MADISON, JAMES	PiM-'95 Jun. 31 Aug 36 Oct 34 Dec 38
    Indicating a Bridgeport Head	HOWARD, JOSEPH P.	PiM Dec. '98 35
    Indicating Your Setting		PiM-Apr.'90,3
    Indicator Clamps for Lathe Beds	TORGERSON, RICHARD S.	PiM-Apr.'90,16
    Indicator Stand, An	BOWER, EARL L.	HSM'96:J/A 48
    Indicators and edge finders	Lautard, Guy	TMBR#3:83-97
    Inertia Welding	HESSE, JIM	PiM Jun.'97 28
    Inexpensive Air Compressor, An	HESSE, JAMES	PiM Oct.. 94, 24
    Inexpensive Fitted Instrument Case	VAUGHN, W.B.	HSM'82:M/J14
    Inexpensive Milling/drilling Spindle	SMITH, W. R.	PiM Oct.. 94, 4
    Inexpensive Power Feed, An	KALB, MELVIN L.	HSM'92:M/A53
    Inexpensive Power Feed, An	KRAEMER, JOHN E	PiM-Aug.'94,4
    Inexpensive Suds Pump	PLUMMER	MEW#20,23
    Inexpensive Tool Mounts(Chips & Sparks)	VERITY, TOM	HSM'95:M/A20
    Info for camera buffs	Lautard, Guy	TMBR#1:141-142
    Installing a Locking Base Pin	ACKER, STEVE	MW Aug. 99, 38
    Installing a Power Feed Unit on a Vertical Mill	McLEAN, FRANK	HSM'86:N/D52
    Instant Soft Jaws for the Vise	JOHNSON, D. E.	PiM-Aug.'93,29
    Instantaneously Reversible Motor Control	STROH, RAY	PiM-Apr.'94,32
    Instrument Makers Vice	HALL	MEW#18,32
    Internal chasers on the cheap	JEEVES	MEW#28,32
    Internal Keyway Slotting	KOLAR, GEORGE	HSM'94:M/J15
    Internal Keyways		HSM'89:N/D40
    Internal Spindle Stop	BLACKMON, BILLY J.	HSM'96:J/A 46
    Internal-external Center Finder	LINCOLN, W. A.	PiM-Oct.'93,3
    Intro. to broaching	JEEVES	MEW#26,49
    Intro. to enamelling metals	JEEVES	MEW#30,32
    Introduction to Jigs and Fixtures	HOFFMAN, EDWARD G.	HSM'89:J/A52
    Investment Casting, Parts 1-2	LEWIS, JAMES R.	HSM'87:S/O44,N/D53, HSM'88:J/F44,M/A42,M/J46
    Iron & Steel The Bare Bones--	UNWIN	MEW#14,54
    Is a Dial indicator an accurate measuring device?	Lautard, Guy	HTIM:47
    Jack The Ribber	TAYLOR	MEW#12,17
    Jacobs spindle nose chuck	Lautard, Guy	TMBR#3:12
    Jaw Boxes	HAUSER, JAMES W.	MW Aug. 99, 45
    Jaw protectors	Lautard, Guy	TMBR#3:68-69
    Jaws	GILL, L.	PiM-Feb.'96, 42
    Jaws	TOGERSON, RICHARD	HSM'86:J/F17
    Jeclanide Handwheel	TAYLOR	MEW#13,48
    Jig for Cross Drilling		PiM-Dec.'89,24
    Jigs & Fixtures Reducing Wotkholder Weight Parts 1-3	HOFFMAN, EDWARD C.	HSM'99:J/F 62 M/A 60 M/J 56
    Jigs & Fixtures: Basics of Clamping Parts 1-2	HOFFMAN, EDWARD G.	HSM'91:J/F58,M/A52
    Jigs & Fixtures: Basics of Locating Parts 3-8	HOFFMAN, EDWARD G.	HSM'90:J/F54,M/A52,M/J57,J/A56,S/O55,N/D56
    Jigs & Fixtures: Cam Clamps	HOFFMAN, EDWARD G.	HSM'91:N/D54
    Jigs & Fixtures: Fixturing With Collets, Parts 4-8	HOFFMAN, EDWARD C	HSM'97:J/F 63, M/A 58, M/J 62, J/A 63, S/O 62
    Jigs & Fixtures: Locating Pins Part 1	HOFFMAN, EDWARD G	HSM'95:N/D60
    Jigs & Fixtures: Screw Clamps	HOFFMAN, EDWARD G.	HSM'91:M/J56
    Jigs & Fixtures: Specialty Clamping Devices Part 1-4	HOFFMAN, EDWARD G	HSM'95:M/A54 M/J54 J/A58 S/O56
    Jigs & Fixtures: Specialty Locating Devices Part 2	HOFFMAN, EDWARD G	HSM'95:J/F58
    Jigs & Fixtures: Toggle Clamps	HOFFMAN, EDWARD G.	HSM'91:S/O55
    Jigs & Fixtures: Wedge Clamps	HOFFMAN, EDWARD G.	HSM'91:J/A54
    Jigs and Fixtures		HSM'87:S/O15
    John Steele's new workshop	HALL	MEW#24,48
    Jot it Down	WELLS, NORM	PiM-Apr.'96, 44
    Just Like Magic		HSM'83:J/F16
    Keep It Simple, Guys		HSM'92:M/J14
    Keep that Universal Chuck Accurate	PETERKA, PETE	HSM'85:M/A22 
    Keeper of the Key	RICHARDS, DAVID	HSM'91:M/A38
    Keeping a Jacobs JT 33 Chuck on the Spindle		HSM'87:J/F20
    Keeping taps square	Lautard, Guy	TMBR#1:19
    Keeping the Dust Down		HSM'87:J/F19
    Keeping the Noise Down		PiM-Jun.'91,3
    Keeping Track of the Chuck Wrench		PiM-Feb.'89,24
    Keeping Track of the Chuck Wrench	LAMANCE, THOMAS	PiM Oct.'97 44 
    Kerosene burning blowlamp	Lautard, Guy	TMBR#2:47; TMBR#3:102
    Key Seat Attachment		HSM'89:M/J16
    Keyed Assemblies	HOFFMAN EDWARD G	HSM'82:S/O17
    Keys and keyways	JEEVES	MEW#29,14
    Keyseat Cutter for the Lathe, A	HESTER, DON	PiM-Aug.'96, 28
    Keyway Broach Bushings	McLEAN, FRANK A.	HSM'94:S/O56
    Keyway Shaping -- A Lathe Attachment	LEAFE, MAL.COLM K.	PiM-Apr.'96, 25
    Keyways-Internal and External	WASHBURN, ROBERT A	HSM'86:M/A50
    Killing chatter-	Lautard, Guy	TMBR#1:16
    Knife Blade from Scrap, A	ACKER, STEVE	PiM-Jun.'90,12
    Knockout Bar	THOMPSON, JACK R.	HSM'93:M/J37
    Knorrostol rust remover/metal polish	Lautard, Guy	TMBR#3:72
    Knurling flat surfaces	Lautard, Guy	TMBR#3:74
    Knurling technique	Lautard, Guy	TMBR#1:60-61; TMBR#2:100
    Knurling Tip	LUCHESSA, C. M.	HSM'92:S/O15
    Knurling	Lautard, Guy	TMBR#1:5
    Knurls and Knurling	CARVER, ERIC	HSM'92:M/A38
    Kroy Light Table		HSM'83:J/A8
    L. S. Starrett Company	HAUSER, JAMES W.	MW Aug. 99, 45
    Lacquered brass	Lautard, Guy	TMBR#1:143
    Lamp Base for the Shadowgraph, A	BUTTERICK, RICHARD	PiM Jun.'97 32
    Lamp in the form of a clamp-on ball handle	Lautard, Guy	TMBR#3:205
    Lamp made from brass fittings	Lautard, Guy	TMBR#3:206
    Lapping an edgefinder , correct	Lautard, Guy	TMBR#3 2nd printing:94, 139. & 251
    Lapping an edgefinder, incorrect	Lautard, Guy	TMBR#3 1st printing:94, 139. & 251
    Lapping with Tripoli	Lautard, Guy	HTIM:47
    Laps and lapping	JEEVES	MEW#23,43
    Large capacity two part vice	JEEVES	MEW#24,20
    Large Radii Cutting (Tips & Tricks)	SCHROEDER, ARDEN A.	PiM-Apr.'95 33
    Large Radius Cylindrical Cuts on a Shaper	HOIJER, PETER J	HSM'94:J/A44
    Large tap holder	POWELL	MEW#23,18
    Larger Steady Rest,	WILSON, GLENN A	HSM'90:J/F24
    Laser Alignment for the Home Shop	BLACK, JOE	HSM'99:J/A 62
    Last Pass Indicator	WILSON, GLENN L.	PiM-Dec.'94,4
    Lathe Accessories	McLEAN, FRANK	HSM'83:M/A52,M/J51
    Lathe Accessories	WASHBURN, ROBERT A.	HSM'83:N/D60
    Lathe Adapter Blocks	PIPER, PHIL	PiM-Dec.'94,29
    Lathe Adapters	JONES, BRUCE	PiM-Apr.'95 2l
    Lathe Alignment	FANGOHR, JOE	HSM'97:ND 58
    Lathe Alignment	HUFFAKER, ROBERT	PiM-Apr.'96, 31
    Lathe Back Stop	HALL	MEW#10,22
    Lathe Bench, A	YOUNG, BARRY	MW Feb. 99, 42
    Lathe Bit Grinding Jig	KEELY, ARTHUR W.	PiM-Apr.'96, 19
    Lathe Boring Bar Set, A	HEDIN, R. S.	PiM-Aug.'94,13
    Lathe Cabinet/Stand, A	WALKER, RALPH T.	HSM'89:J/A18
    Lathe Carriage Dial Indicator	GREGG, ALLEN	HSM'88:S/O28
    Lathe Carriage Oiler	BENNETT, N. H.	HSM'85:M/A41
    Lathe Carriage Stop Modification		HSM'83:N/D24
    Lathe Carriage Stop	McCORMAC, DON	HSM'83:J/F52
    Lathe Carriage Stop	NEILL, IRA J.	HSM'91:J/F36
    Lathe Carriage Way Covers	VREELAND, DON H.	PiM-Aug.'91,22
    Lathe Chip Shield	BERGER, JIM	HSM'84:M/A44
    Lathe Chuck Adaptations	BRAXTON, LOWELL P.	MW Feb. 99, 20
    Lathe Chuck Adapter		HSM'85:M/A17
    Lathe Chuck and the 1930s Revisited		HSM'85:M/J14
    Lathe Chuck Backstop	McDOWELL, THEODORE	HSM'86:M/J33
    Lathe cleaning	Lautard, Guy	TMBR#1:175
    Lathe Collet Stand, A	WALKER, RALPH T.	PiM-Jun.'90,22
    Lathe Cutting Internal Keyways	WALKER, RICHARD B.	HSM'89:N/D40
    Lathe Dog	DRAYSON, D. A.	PiM Oct.. 94, 3
    Lathe Form Tools	HALL	MEW#13,54
    Lathe Four-way Tool Turret, A	HANNUM, ROBERT C.	PiM-Feb.'89,11
    Lathe Handles	RAUBACH, PIERCE	HSM'96:J/A 21
    Lathe Index and Crank	LETZRING, NORMAN	PiM Oct.'97 16
    Lathe inspection	MORRIS	MEW#32,45
    Lathe made in a Japanese POW camp	Lautard, Guy	TMBR#1:156
    Lathe Measuring Instruments	WASHBURN, ROBERT A.	HSM'84:M/J60
    Lathe Milling Attachment	HEDIN, R S	HSM'83:J/F26
    Lathe milling attachment	NEAVE	MEW#21,40
    Lathe Milling Attachment, A	BOROWICZ, TOM	PiM-Jun.'94,8
    Lathe Modification		HSM'86:S/O18
    Lathe Mounted Band Saw	GRAY	MEW#9,37
    Lathe Mounted Fret Saw	FLETCHER	MEW#18,18
    Lathe Operations on a Vertical Mill Parts 1, 2	THOMAS, STEPHEN M.	HSM'90:J/F29,M/A33
    Lathe Rack Repair, A	WRIGHT, TED	PiM-Aug.'91,14
    Lathe Shear Pin Modification	TORGERSON, RICHARD	PiM-Dec.'89,20
    Lathe Spur Mandrel	REED, KEN	PiM-Aug.'94,MN
    Lathe Spur Mandrel	REED, KEN	PiM-Oct.'96, 44
    Lathe Stands	McLEAN, FRANK A	HSM'82:N/D48
    Lathe Table, A	KOUHOUPT, RUDY	HSM'93:M/J43
    Lathe Thread Cutting Stop, A	WALKER, RICHARD B	HSM'86:M/A16
    Lathe Threading Stop	HEDIN, R. S.	PiM-Feb.'89,14
    Lathe Tips	HOFFMAN, EDWARD G, STONE, EDWARD P..	HSM'96:J/F 50
    Lathe Tips	TORGERSON, RICHARD	PiM-Apr.'89,12
    Lathe Tool Grinding Holder		PiM-Jun.'90,24
    Lathe Tool Post Grinder for Serious Grinding, A Parts 1,2	JOHNSON, D. E.	HSM'99:J/F 28 M/A 28
    Lathe Tool Setup Gage, A	McDERMOTT, IOHN P. Jr.	HSM'86:M/A23
    Lathe Turning Tools	WASHBURN, ROBERT A.	HSM'84:J/F52
    Lathe Work Out of Round		HSM'85:M/J14
    Lathe Work	HAMILL, JAMES	HSM'82:S/O22
    Lathe-center Step-up Cone, A	JOHNSON, NORMAN E	MW Feb. 99, 26
    Lautard's manoeuvre	Lautard, Guy	TMBR#2:160
    Lautard's Octopus	Lautard, Guy	TMBR#2:v
    Lava Handsoap		HSM'88:M/A13
    Laying out a tilted circumferential notch	Lautard, Guy	HTIM:10
    Lazy susan bearings	Lautard, Guy	HTIM:2
    Lead Shot Filled Boring Bar	STRAIGHT, J. W.	HSM'93:J/F38
    Learner's Notes	LAUTARD, GUY	PiM Aug. '98 39
    Lemon Squeezer	METZE, BOB	PiM Aug.'97 27
    Lettering On Line		HSM'85:N/D12
    Level Check		PiM-Apr.'88,24
    Lever Arm Adapter		HSM'91:M/A16
    Lever Operated Tailstock	DUBOSKY, ED	PiM-Apr.'92,20
    Lever Operated Tailstock, Parts 1-2	KOUHOUPT, RUDY	HSM'88:J/A34,S/O42
    Lever Tailstock Feed for the Center Lathe, A	WRIGHT, TED	PiM-Feb.'93,12
    Lever-operated Tailstock Clamp for Atlas/Sears 12" Lathes, A	FRANCISCO, HARRY B.	PiM-Aug.'93,4
    Lid/box match-up	Lautard, Guy	TMBR#3:192
    Lie-Nielsen Toolworks edge trimming block plane	Lautard, Guy	TMBR#3:194-195
    Lie-Nielsen Toolworks Scraping planes	Lautard, Guy	TMBR#3:195
    Life With a Mill-drill	COLLINS, MARSH	PiM-Aug.'96, 14
    Lifting Gadget		HSM'90:J/A15
    Light duty dividing head from BHJ, by Eliot Isaacs	Lautard, Guy	TMBR#2:1
    Light duty height-adjustable stands for...?	Lautard, Guy	TMBR#3:211
    Light duty mill/drill spindle	GRAY	MEW#27,32
    Light Reflector		PiM-Dec.'88,24
    Lighting Your Vertical Mill	McLEAN, FRANK A.	HSM'87:S/O49
    Linoleum - a superior vise jaw lining material	Lautard, Guy	HTIM:38
    Little "Blazer" Engine	DUCLOS, PHILIP	PiM-Jun.'92,4
    Little Job Cement Mixer Parts 1-4	KOUHOUPT, RUDY	HSM'96:J/F 54, M/A 50, M/J 55, J/A 51
    Live Center, A		PiM-Jun.'95 28
    Load Cell (Hydraulic Scale)	METZE, ROBERT W	PiM-Dec.'91,12
    Locating buttons for master division plate	Lautard, Guy	TMBR#2:3
    Locating Pins Parts 2-3	HOFFMAN, EDWARD G.	HSM'96:J/F 62 M/A 54
    Locating Work on a Mill		HSM'91:J/A13
    Locating	GASCOYNE, JOHN	PiM-Dec.'88,14
    Locking Pliers Jerk Puller	CROW, ARTHUR	PiM-Feb.'96, 23
    Loctite	Lautard, Guy	TMBR#1:96
    Long Story Shortened (extra-long taps)	WHIPPLE, STEVEN G.	HSM'96:J/A 20
    Long transfer punches	Lautard, Guy	TMBR#3:175
    Long, Useful Life		HSM'87:J/A17
    Long-Lasting Heat Dam, A		HSM'86:M/J14
    Look at Derek Brooks Workshop	HALL	MEW#16,35
    Look in Books		HSM'86:M/A14
    Looking at stainless steels	JEEVES	MEW#25,48
    Lost wax casting for multiple parts	Lautard, Guy	TMBR#3:116
    Low Cost Adjustable Counterbore, A	WORZALA, J.	PiM-Dec.'92,31
    Low Cost Ball Bearings		HSM'91:J/A15
    Low cost master type for an engraving machine	Lautard, Guy	TMBR#3:252
    Low Cost Stepper Motor Drive, A	DAHLIN, TOM	PiM-Dec.'94,8
    Low cost vertical slide	PENGELLY	MEW#27,36
    Low Range Ohmmeters for Electric Motors	MYERS, TED	HSM'91:M/A24
    Low range torque wrench	OAKES	MEW#27,59
    Low Speed Countershaft	WINKS	MEW#9,43
    Low voltage lighting	SERVICE	MEW#22,30
    Low-cost Bead Blaster, A	ACKER STEVE	HSM'97:J/F 36
    Low-cost Quick-change Tool Post, A	PILESKI, MIKE	PiM-Oct.'96, 4
    Low-cost Reversing Switch for Electric Motors	HALBERT, R. L	HSM'94:N/D53
    Low-tech Edge Finder, A	DRAYSON, D. A.	PiM Aug. '98 40
    Lube for tube expanding etc.	Lautard, Guy	TMBR#2:129
    Lubes for tapping various materials	Lautard, Guy	TMBR#1:18
    Lubricating Long Lathe Cuts		HSM'91:J/A14
    Lubricating milling machine spindles	Lautard, Guy	TMBR#3:101
    Lubrication and grinding machines	Lautard, Guy	TMBR#2:161
    Lumiweld	Lautard, Guy	TMBR#2:123
    M.I.G. Welding	MCCLEAN	MEW#12,58
    Mach 92	HALL	MEW#12,30
    Machinable Angles	MADISON, JAMES	PiM-Feb.'94,28
    Machine Cutting Speeds	STOKES, FRANK	HSM'89:M/A50
    Machine Guards	HOFFMAN, EDWARD G.	HSM'87:M/J64
    Machine Mobility	VORDAHL, NORMAN A.	HSM'96:S/O 20
    Machine Shop Calculations Right Triangles Part 3	HOFFMAN, EDWARD G	HSM'90:J/F20
    Machine Shop Calculations Shop Measurement Parts 1-5	HOFFMAN, EDWARD G.	HSM'90:M/A17,M/J20,J/A16,S/O18,N/D18
    Machine Shop Calculations, Dimensions and Tolerances Parts 1-6	HOFFMAN, EDWARD G.	HSM'87:J/F26,M/A17,M/J16,J/A18,S/O17,N/D19
    Machine Shop Calculations: Dimensions & Tolerances, Parts 7-12	HOFFMAN, EDWARD G.	HSM'88:J/F17,M/A16,M/J16,J/A17,S/O15,N/D18
    Machine Shop Calculations: Geometric Construction Parts 1, 2	HOFFMAN, EDWARD G.	HSM'91:S/O17,N/D15
    Machine Shop Calculations: Shop Measurement Part 6	HOFFMAN, EDWARD G.	HSM'91:J/F13
    Machine Shop Calculations: Surface Finish Designations Parts 1-3	HOFFMAN, EDWARD G.	HSM'91:M/A17,M/J13,J/A16
    Machine Shop Calculations-Gears Parts 3-8	HOFFMAN, EDWARD G.	HSM'86:J/F56,M/A58,M/J17,J/A14,S/O46,N/D18
    Machine Shop Crossword Puzzle	INSTONE, JAMES R.	HSM'97:ND 20
    Machine Shop Crossword Puzzle	INSTONE, JAMES R.	HSM'98:J/F 25, M/J 59, J/A 25, S/O 24
    Machine Shop Crossword Puzzle	INSTONE, JAMES R.	HSM'99:M/A 26, M/J 26, J/A 26
    Machine Shop in a Cabinet	KOUHOUFT, RUDY	HSM'83:J/A62
    Machine stands	Lautard, Guy	TMBR#3:186-190
    Machine Tool Covers	MYERS, TED	HSM'92:M/J39
    Machine tool heights for comfort	Lautard, Guy	TMBR#1:133; TMBR#3:187
    Machine Tools for Woodworking	ROUBAL, TED	PiM-Aug.'88,12
    Machinery Covers ((Tips & Tricks))	JOHNS, MICHAEL	PiM-Dec.'95 42
    Machinery Oil Gun, A	SOKOL, JERRY L.	PiM-Aug.'95 22
    Machining a rubber roll	Lautard, Guy	TMBR#2:152
    Machining a spindle from its I.D.	Lautard, Guy	TMBR#2:39
    Machining Aids for a Machine Lathe	LEWIS, JAMES R.	HSM'87:M/A22
    Machining an Angle Plate	ACKER, STEVE	PiM-Jun.'92,20
    Machining Internal Threads - A Different Approach	GRADY, ROBERT L.	PiM-Aug.'93,30
    Machining on the Internet	MENDUM, J. H.	HSM'96:S/O 62
    Machining Paraffin		HSM'86:N/D12
    Machining Small Diameter Work		HSM'89:M/J16
    Machining Small Diameter Work	McELVAIN, EVERETJ.	PiM-Jun.'94,M&M
    Machining Thin Disks and Rings	JOHNSON. D. E., P. E.	HSM'84:M/J50
    Machining Thin Plates on a Vertical Mill	McLEAN, FRANK A.	HSM'87:M/A56
    Machining white metal bearings	HARTWELL	MEW#28,53
    Machining Your Own Spur Gears	KOUHOUFT, RUDY	HSM'83:M/J28
    Machining	STRASSER, FREDERICO	HSM'83:J/A50,S/O48
    Machinist Uses for Seemingly Unrelated Products	DOOLIN, THOMAS J.	HSM'97:S/O 22
    Machinist's Clock, A	REICHART, BILL	HSM'95:M/A37
    Machinist's Desk Lamp, A Parts 1-2	LAUTARD, GUY	HSM'87:J/A22,S/O34
    Made by soldering tubing to plate material	Lautard, Guy	TMBR#3:200
    Made flat by scraping	Lautard, Guy	TMBR#2:67
    Made in the Shade (lathe way cover)	STANAITIS, PETE	HSM'96:S/O 21
    Magnet as milling vise stop	Lautard, Guy	TMBR#3:58
    Magnetic Back for a Dial Indicator, A	BROWNE, DONOVAN V.	PiM Aug.'97 31
    Magnetic Base Indicator Mount	DAVIS, M. O.	HSM'96:S/O 22
    Magnetic Base, A	THOMPSON, JACK R.	PiM Jun.'97 14
    Magnetic goodies	Lautard, Guy	TMBR#3:68
    Magnetic indicator on dial indicator back	Lautard, Guy	TMBR#3:79
    Magnetic Mandrel	PUNSHON, CLAYTON	HSM'98:S/O 58
    Magnetic post	FROST	MEW#21,22
    Magnetic Template	KINZER, DWIGHT	PiM-Oct.'96, 42
    Magnetic vise jaw liners	Lautard, Guy	TMBR#3:68
    Magnetic welding positioners	Lautard, Guy	TMBR#3:255
    Magnifying Glass Holder		PiM-Feb.'88,24
    Mail Order Customer Rights		HSM'86:N/D51
    Maintaining Files	MAZARR, CHARLES ("MUZZIE")	PiM-Oct.'96, 4Z
    Make a Center Finder	KOUHOUPT, RUDY	HSM'93:N/D51
    Make a Tap Center	HALLWARD, PETER M.	PiM Apr. '98 36
    Make a Thread Dial for Your Lathe	BARBOUR, J. O.	PiM Oct.. 94, 30
    Make A Wiggler	BLACKMON, BILLY	MW Apr. 99, 22
    Make a Work Saver From Scrap Iron	DEAN, JOHN	HSM'82:J/F17
    Make an Open-sided Tool Post	KOUHOUPT, RUDY	HSM'94:N/D62
    Make It Bright		HSM'85:M/J14
    Make Your Own Collet Chuck	LOOP, PAT	PiM-Jun.'88,4
    Make Your Own Edge Finder	ROSCOE, LOWIE L., JR	PiM-Feb.'95 24
    Make Your Own Lathe Collets, Parts 1-2	KOUHOUPT, RUDY	HSM'96:S/O 58, N/D 56
    Make-Do Spotlight		PiM-Apr.'88,24
    Making & checking a flat master square	Lautard, Guy	TMBR#2:16, 17
    Making A Box Angle Plate	BERNHARDT	MEW#15,44
    Making a Catch Plate	KOUHOUPT, RUDY	HSM'92:J/A51
    Making a Clapper	KOUHOUPT, RUDY	HSM'98:J/F 60
    Making a Co-Axial indicator	Lautard, Guy	TMBR#3:83
    Making a Cutoff Toolholder	KOUHOUPT, RUDY	HSM'93:J/A49
    Making a Cylindrical Square	WRIGHT, TED	PiM-Aug.'88,18
    Making a Dovetail Front Sight	ACKER, STEVE	PiM-Oct.'96, 40
    Making A Four Jaw Chuck	MORRIS	MEW#12,64
    Making a good center, & drilling a hole there	Lautard, Guy	TMBR#3:104/105
    Making a hand shear	GOULD	MEW#28,37
    Making a Hardened Steel Washer	ACKER, STEVE	PiM-Feb.'94,24
    Making a Height Gage		HSM'85:S/O16
    Making a Knurled Head Thumbscrew	MCLEAN, FRANK A.	HSM'92:S/O45
    Making A Lathe Filing Rest	FLETCHER	MEW#19,42
    Making a M22 Springfield magazine clip (story)	Lautard, Guy	TMBR#2:110
    Making a Milling Saw Arbor	GENEVRO, GEORGE W.	PiM-Dec.'88,22
    Making a Mold Using a Matchplate	LEWIS, JAMES R.	HSM'87:J/F56
    Making a Pair of Milling Clamps Part 1	KOUHOUPT, RUDY	HSM'91:N/D48
    Making a precision angle plate	HALL	MEW#26,38
    Making a set of angle blocks	Lautard, Guy	TMBR#2:81
    Making a Set of Boring Bars	LOFQUIST, A. J.	PiM-Apr.'93,22
    Making a sheet metal box	Lautard, Guy	HTIM:31
    Making A Small Four Jaw Chuck	LOADER	MEW#11,32
    Making a small pantograph engraving machine	Lautard, Guy	TMBR#2:24
    Making a Small Split Collar	HOLM, PAUL J.	PiM Oct. '98 20
    Making a solenoid core	Lautard, Guy	TMBR#2:129
    Making a special countersink	Lautard, Guy	TMBR#2:53
    Making a Spring-loaded Center	GENEVRO, GEORGE	PiM-Aug.'91,20
    Making a strop	Lautard, Guy	TMBR#2:120
    Making a wooden drive pulley	Lautard, Guy	TMBR#3:58
    Making an Angle Plate in the Lathe	HANCOCK, C. H.	HSM'87:M/J45
    Making an Angle Plate	KOUHOUPT, RUDY	HSM'97:N/D 63
    Making an antique aircraft	Lautard, Guy	TMBR#3:208
    Making an Automatic Feed for a Milling Machine	REICHART, JOHN	HSM'84:S/O31
    Making an engraving cutter	Lautard, Guy	TMBR#1:45-46; TMBR#2:36
    Making an Index Plate for a 4x4" Center Height Dividing Head	WRIGHT, TED	PiM-Aug.'92,16
    Making Ball Handles -- A New Approach	LINCOLN, W. A. ("LINK")	PiM-Dec.'96, 4
    Making Chatterless Countersinks	JOHNSON, D. E.	PiM-Apr.'93,26
    Making division plates	SWALLOW	MEW#24,16
    Making fishing reels	Lautard, Guy	TMBR#2:138-139
    Making Gears Using a Hob	DOBIAS, DON	PiM Dec. '98 13
    Making gold refining equipment	Lautard, Guy	TMBR#3:208
    Making Heavy Work Light(Tips & Tricks)	RANSIL, R. JOSEPH	PiM-Feb.'95 48
    Making Identical Patterns for Multiple Lost Wax Castings, Parts 1-3	LEWIS, JAMES R	HSM'88:J/A27,S/O49,N/D52
    Making most of the workshop	AMOS	MEW#31,44
    Making Pin Punches	ACKER, STEVE	HSM'93:J/F32
    Making screwed fittings come up tight where wanted	Lautard, Guy	TMBR#3:82
    Making Simple Graduated Collars with Your Computer	MCCREARY, TERRY	PiM-Apr.'93,30
    Making small, fine-quality aluminum castings	Lautard, Guy	TMBR#2:149, (202 after 1st printing); TMBR#3:129
    Making Tap and Reamer Handles	KOUHOUPT, RUDY	HSM'91:J/A49
    Making the Home Shop Pay	ODER, JOHN W.	HSM'84:N/D45
    Making the Lathe Safer	JEDLICKA, JIM	HSM'89:N/D20
    Making the most of the four jaw chuck	HARTWELL	MEW#26,27
    Making underwater housings for video cameras	Lautard, Guy	TMBR#3:215
    Making Up Band Saw Blades	HEDIN, R. S.	PiM-Jun.'91,9
    Making weatherproof work lights	Lautard, Guy	TMBR#3:210
    Making welded steel boxes	Lautard, Guy	TMBR#1:187
    Making your own chambering reamers	Lautard, Guy	TMBR#2:198
    Making/using a spindle nose duplicate	Lautard, Guy	TMBR#3:63
    Marking Gauge	LANGHAM	MEW#14,46
    Marking out angles	HALL	MEW#31,31
    Master type from Green Instrument Co.	Lautard, Guy	TMBR#2:25
    Master type racks	Lautard, Guy	TMBR#2:34
    Match drilling holes for pillars	Lautard, Guy	HTIM:4
    Material choice	Lautard, Guy	TMBR#3:19 1
    Materials/Scrounging	Lautard, Guy	TMBR#1:3
    Mathematical Approach to Knurling, A	KOVAL, ROBERT	PiM Aug.'97 22
    Mathematics of a Dividing Head, The	WELLCOME, STEVE	PiM-Feb.'91,17
    Mathematics of taper turning	HALL	MEW#22,53
    Maverick Engine Parts 1-2	DUCLOS, PHILIP	HSM'95:S/O22 N/D40
    Maverick Engine Parts 3-4	DUCLOS, PHILIP	HSM'96:J/F 44,M/A 42
    Maximising workshop space	MACHIN	MEW#31,33
    McDuffie Drive	Lautard, Guy	TMBR#2:41
    Md65 Modifications	SHEPHERD	MEW#13,16
    Measurement for Taper Turning	FELLER, E. T.	HSM'87:N/D50
    Measuring & marking out angles	HALL	MEW#24,42
    Measuring an angle with a sine bar	Lautard, Guy	TMBR#3:98
    Measuring Angles	MEISTER, HORST	PiM-Dec.'96, ZZ
    Measuring hole size with a rod	Lautard, Guy	TMBR#1:10
    Measuring hole size with taper leaf gages	Lautard, Guy	TMBR#1:10
    Measuring lathe saddle movement with	Lautard, Guy	HTIM:8
    Measuring Long Fits		HSM'86:S/O18
    Measuring Long Pieces		PiM-Aug.'88,24
    Measuring Pitch Diameter	DONDRO, CHARLIE	HSM'85:M/J20
    Measuring Small Work	LaMANCE, 'I'HOMAS	PiM-Jun.'96, 40
    Measuring With Pins Parts 1-3	HOFFMAN, EDWARD G	HSM'92:J/A18,S/O16,N/D16, HSM'93:J/F16
    Mechanical Fasteners Parts 1, 2	HOFFMAN, EDWARD G	HSM'92:M/A50,M/J53
    Mechanical Lift for a Drill Press Table, A	CORTNER, ROBERT	HSM'98:S/O 38
    Mechanical Revolutions Counter, A Parts 1-3	KOUHOUPT RUDY	HSM'99:M/A 56
    Mechanical Stroboscope, A Parts 1,2	KOUHOUPT RUDY	HSM'99:S/O 38 N/D 60
    Mechanical Variable speed Drive	LONGWORTH	MEW#11,57
    Medite	Lautard, Guy	HTIM:1-3
    Medite, finishing	Lautard, Guy	HTIM:1-2; TMBR#3:190
    Medium Duty Fret Saw	HALL	MEW#11,24
    Metal bench planes	JONES	MEW#23,26
    Metal Bender	GOULD	MEW#18,41
    Metal Forming Brake Attachment	BARBOUR, J. O., Jr.	HSM'85:N/D35
    Metal Lathe Mount for a Laminate Trimmer, A	BATORY, DANA MARTIN	PiM Oct. '98 36
    Metal polish	Lautard, Guy	TMBR#1:171
    Metal Polishing	JEEVES	MEW#16,24
    Metal Spinning Lubricant	LAMANCE, THOMAS 	MW Aug. 99, 58
    Metal Spinning	JEEVES	MEW#15,38
    Metal Turning and Glassblowing with the Metal Lathe	ROUBAL, WILLIAM T., Ph.D.	HSM'83:J/F44,M/A34,M/J34
    Metal Turning and Glassblowing with the Metal Lathe	ROUBAL, WM. T., Ph.D.	HSM'82:N/D38
    Metals for Casting		HSM'86:J/F47,M/A47,M/J46, VA 48,S/O50,N/D48
    Method for accurate setting of taper turning attachment	Lautard, Guy	TMBR#3:15
    Methods for Success: Turning Tools for Tough Materials	MADISON, JAMES	PiM Feb. '98 32
    Methods of a professional	GOULD	MEW#23,23
    Metric Equivalents		HSM'91:M/A16
    Metric Thread Conversion	CRAIG, LAWRENCE	PiM-Aug.'96, 3
    Metric Thread Cutting With an Eight TPI Lead Screw	GIBSON, ARCH	PiM-Apr.'96, 37
    Metric Threads From Your English Lathe	CRAIG, LAWRENCE	HSM'99:S/O  26
    Metric Threads	CULVER, JOHN S.	HSM'99:J/A 46
    Metric-Decimal Equivalents and Tap Drill Sizes	ALLES, WILLIAM J., JR	HSM'88:J/F19 
    Micro Adjust Boring Adaptor	LONGWORTH	MEW#19,14
    Micro Adjustable Bow Sight	TITUS, DON	MW Apr. 99, 16
    Micro Aids for a Full Size Machinist	JOHNSON, D. E.	PiM-Oct.'92,4
    Micro Drill Press, A	LOOP, PAT	PiM Dec. '97 4
    Micro Drilling/milling Spindle, A	SMITH, W. R.	PiM-Apr.'93,4
    Micro Machinist, The Indexing Centers Part 3	KOUHOUPT RUDY	HSM'99:J/F 42
    Micro Machinist, The: Making Accurate Squares	KOUHOUPT, RUDY	HSM'97:S/O 56
    Micrometer Adapter		HSM'86:J/A12
    Micrometer Attachment for Lathe Lead Screws	McDERMOTT, JOHN P., JR.	HSM'85:M/J22
    Micrometer Boring Adaptor	LONGWORTH	MEW#18,27
    Micrometer Dial for the Tailstock	GROSJEAN, W C	HSM'83:J/A40
    Micrometer Mount		HSM'87:M/A15
    Micrometer Stand	McCORMAC, DON	HSM'83:J/A64
    Micrometers With A Difference	HALL	MEW#19,32
    MIG and TIG welding	Lautard, Guy	TMBR#3:255-256
    Mig Welding	MCCLEAN	MEW#13,13
    Military triggers	Lautard, Guy	TMBR#3:143
    Mill Drill Repair, A	ACKER, STEVE	PiM-Oct.'90,24
    Mill Spindle Indicator Holder, A	RICE, ROY	HSM'94:J/A35
    Mill Vise: Rework for Precision	TORGERSON, DICK	PiM-Jun.'92,6
    Mill/Drill Attachments	HOLM, PAUL	PiM-Apr.'89,11
    Mill/drill modification	HALL	MEW#30,29
    Mill/drill modification	LINFORD	MEW#30,31
    Mill/drill Power Feed	PATTERSON, FRED V.	PiM Feb. '98 13
    Mill/Drill Speed Reduction	TORGERSON, DICK	PiM-Aug.'92,4
    Mill/Drill Stand,	MULHOLLAND, GERARD A	HSM'90:M/A51
    Mill/drill Support, A	HOLM, PAUL	HSM'94:M/J29
    Mill/drill Tips	EISLER, DAVID	HSM'96:J/F 21
    Mill-drill Adventures Part 7 Keeping Track of the Cutting Tool and Table Positions	JOHNSON, D. E.	HSM'96:J/A 30
    Mill-Drill Adventures Parts 1-4	JOHNSON, D. E.	HSM'95:M/A34 M/J32 J/A22 N/D28
    Mill-drill Adventures Parts 5-6 A Power Feed for the Main Table and a Rotary Table	JOHNSON, D. E.	HSM'96:J/F 26, M/A 32
    Mill-drill Adventures: New Handwheels and Leadscrew Bearings Fix Backlash and Rattles Part 8, 9	JOHNSON, D. E.	HSM'97:J/A 32, S/O 40
    Mill-drill Improvements	RIDENOUR, V. L.	PiM Apr. '98 9
    Mill-drill Installation 	DRAYSON, D. A.	MW Feb. 99, 24
    Mill-drill Modification, A	SCHAEFFER, WILLIAM K.	HSM'98:M/J 62 
    Mill-drill Repair, A		PiM-Oct.'90,24
    Mill-drill Spindle Lock	LEGNAME, RUDY	HSM'97:MA 39
    Milling a Flat	BLOCKER, DAVID C.	HSM'96:S/O 21
    Milling a Keyseat in a Shaft	McLEAN, FRANK A.	HSM'94:M/J58
    Milling a radius with a ball end mill	Lautard, Guy	HTIM:7-8
    Milling Accessories Part I	KOUHOUPT, RUDY	HSM'84:N/D58
    Milling Accessories	KOUHOUPT, RUDY	HSM'85:J/F62,M/A62
    Milling Advice (Chips and Sparks)		HSM'84:M/A16
    Milling Attachment for a Small Lathe, A	REYNOLDS, JIM	PiM Aug.'97 4
    Milling Attachment for the Lathe	PETERKA, W. PETE	HSM'83:M/A28
    Milling Column, A	TAYLOR, HOUSTON	PiM-Jun.'89,4
    Milling Cutter Arbor	STRAIGHT, J. W.	PiM-Dec.'91,11
    Milling For Beginners, Parts 1-3	HALL	MEW#10,63;#11,20;#12,38
    Milling Grasping Grooves		PiM Dec. '97 29
    Milling Head Alignment Wheel	JOHNSON, NORMAN E.	PiM Aug.'97 28
    Milling Machine Chip Shield	BERGER, JAMES	HSM'85:N/D30
    Milling Machine Conversion, A	SHULL, LARRY	HSM'93:M/A24
    Milling Machine Down Feed Mod	CORPS	MEW#11,67
    Milling Machine Power Feed	LINCOLN, W. A. "LINK"	PiM-Jun.'95 4
    Milling machine safety	Lautard, Guy	TMBR#3:91,84 & HTIM:33
    Milling Machine Stand	CARTWRIGHT	MEW#12,33
    Milling Machine Table Stop	HALL	MEW#16,45
    Milling Machine Vertical Power Feed, A	LINCOLN, W. A. "LINK"	PiM-Dec.'95 26
    Milling Machine		HSM'94:J/F49
    Milling on a Drill Press	KOUHOUPT, RUDY	HSM'82:S/O26
    Milling on the Lathe	McLEAN, FRANK A	HSM'90:J/A51
    Milling Pockets	MADISON, JAMES	PiM-Oct.'90,15
    Milling spindles & overhead gear	Lautard, Guy	TMBR#2:37, 62-63
    Milling spindles, bearings for	Lautard, Guy	TMBR#2:37; 59
    Milling spindles, for clockmaking	Lautard, Guy	TMBR#2:37
    Milling spindles, Lautard's manoeuvre	Lautard, Guy	TMBR#2:160
    Milling spindles, mounting one	Lautard, Guy	TMBR#2:37
    Milling spindles, Osborne's manoeuvre	Lautard, Guy	TMBR#2:159
    Milling spindles, other refinements	Lautard, Guy	TMBR#2:37
    Milling spindles, Overhead gear	Lautard, Guy	TMBR#2:40-46
    Milling spindles, Quill-Mate	Lautard, Guy	HTIM:33
    Milling spindles, speeds for	Lautard, Guy	TMBR#2:37
    Milling Table, A	FAIREY, BRIAN	PiM-Jun.'94,32
    Milling tapers tangent to 2 circles	Lautard, Guy	TMBR#2:73
    Milling Tips		HSM'83:J/A13
    Milling/Drilling Spindle -- Lathe	SKINNER	MEW#17,14
    Mini Mill Attachment, A	WILSON, GLENN L.	PiM-Dec.'95 6
    Mini Square Hole Punch	DUBOSKY, ED	PiM-Aug.'92,24
    Miniature Machine Shop	PROCKNOW, SID	HSM'88:M/J14 
    Mirror-faced Hammer, The		HSM'89:J/F44
    Miscellaneous Tooling		HSM'88:J/F12
    Mitered and splined	Lautard, Guy	TMBR#3:193
    Mitutoyo Tool Kit	HOFFMAN, EDWARD G.	HSM'87:M/A12
    Mixing up replacement parts for drill chucks	Lautard, Guy	TMBR#3:118
    ML7 Tailstock Lever Feed	COE	MEW#16,30
    Mobile Lathe Stand, A	KOUHOUPT RUDY	HSM'99:N/H 38
    Mobilize Your Heavy Shop Tools	CARSON, SAMUEL W.	HSM'93:M/J24
    Model Builder's Hand Vise	GREEN, WILLIAM F.	PiM-Oct.'88,22
    Model Engineer Exhibition 1992	HALL	MEW#10,48
    Model Engineer I Modelling Ex	HALL	MEW#22,50
    Model i.c. engines	Lautard, Guy	TMBR#1:144
    Model Maker's Dividing Head, Parts 1-3	DUCLOS, PHILIP	HSM'88:N/D20;HSM'89:J/F30,M/A41
    Model Maker's Pipe Tap and Die	COOPER, JOHN A.	PiM-Feb.'96, 41
    Model Piston Rings	DUCLOS, PHILIP	HSM'88:M/J20
    Modelmaker's Vise	HAUSER, JAMES W.	MW Feb. 99, 40
    Modern paint finishes	SHEPPARD	MEW#29,34
    Modification for an Inexpensive Power Feed for the Rf-30 Mill/Drill	KRAEMER, JOHN F.	PiM-Apr.'95 34
    Modifications to a Maximat V-8 Lathe	MARSHALL, DAVE	HSM'84:J/A36
    Modifications to a mc vice	BRITTAIN	MEW#32,21
    Modifications to the Atlas 6" Lathe	BROWN, MICHAEL	PiM-Jun.'95 20
    Modifications to the Machinex 5 Lathe	WELLING, RICHARD	HSM'83:J/F38
    Modifications to the Sherline Mill	UPSHUR, H. B.	PiM-Dec.'94,28
    Modified Arbor Press Ram, A	ANDREWS, ALAN	HSM'94:M/A54
    Modified for drilling plastic	Lautard, Guy	TMBR#3:66
    Modified grinding att -- Unimat3	LOADER	MEW#31,12
    Modified Live Centre	BARTLETT	MEW#13,14
    Modify Your Bead Blast Gun	HOLM, PAUL, J.	HSM'98:M/A 60
    Modifying files for special uses	Lautard, Guy	TMBR#1:116
    Modifying the Carriage Stop		HSM'85:J/A17
    Mods to a dial indicator base	Lautard, Guy	TMBR#3:79
    Moly grease	Lautard, Guy	TMBR#3:73
    Money from a kinetic sculpture	Lautard, Guy	TMBR#3:211
    Money from cast al. grave markers, juke box parts, toy cars	Lautard, Guy	TMBR#3:209
    Money from model steam engines	Lautard, Guy	TMBR#3:214, 216
    Money from sandblasting	Lautard, Guy	TMBR#3:134
    Money from wind chimes	Lautard, Guy	TMBR#2:136
    More Accuracy for your Three-jaw		HSM'89:S/O16
    More Accuracy for Your Three-jaw		HSM'90:M/J15
    More angles on the sine bar	MORRIS	MEW#30,53
    More Belt Power		HSM'89:N/D15
    More Inspiration	ODER, JOHN	HSM'86:J/F14
    More Inspiration, Part 2-5	ODER, JOHN	HSM'88:M/J31,J/A30,S/O35,N/D38
    More Inspiration, Part 6	ODER, JOHN	HSM'89:J/F42
    More motorcycle repairs	Lautard, Guy	TMBR#3:2 17
    More Museums Of Interest	HALL	MEW#12,15
    More on a Gear-Driven Shaper Conversion	CLARKE, THEODORE M	HSM'84:M/J16
    More on Alignment		HSM'84:J/A17
    More on EDM machine drwgs	Lautard, Guy	TMBR#3:78
    More on EDM	LEWIS, JACK	HSM'94:M/J44
    More on Instantaneously Reversible Motor Control	STROH, RAY	PiM-Aug.'94,30
    More on Milling With a Drill Press	CLARKE, THEODORE M	HSM'84:J/A10
    More on Programming Principles	FRIESTAD, ROLAND	HSM'90:J/F44
    More on Three-phase Converters	MATTHYS, ROBERT J.	HSM'94:J/F41
    More On Way Lube		HSM'87:S/O15
    More Reconditioning a Lathe	BLOOM, HARRY	HSM'87:J/F30
    More tricks for the odd-leg artist	Lautard, Guy	TMBR#2:104
    More Versatile Tool, A	WELLS, NORM	PiM-Apr.'93,3
    More Versatile Toot A		PiM-Feb.'89,24
    Morse Taper sockets	Lautard, Guy	TMBR#1:16
    Motor Drive Modification, A	HABERMAN, WILLIAM	PiM Oct.. 94, 28
    Motorcycle wheel repairs	Lautard, Guy	TMBR#3:213
    Moulded Tool Storage Units	ELLIS, ART	HSM'83:M/J48
    Mounting a bench stone	Lautard, Guy	TMBR#2:119
    Mounting a Dial Caliper on the Lathe	LINCOLN, W. A. "LINK"	PiM-Oct.'95 28
    Mounting Small Chucks and Faceplates	KOUHOUPT, RUDY	HSM'97:J/F 53
    Move Was Right, Why Isn't It There?, The	MADISON, JAMES	PiM Oct.'97 30
    Movement Indicator		HSM'89:S/O16
    Moving on a Budget	TITUS, DON	PiM-Apr.'95 27
    Multi-boring Block for a 9" Enco Lathe, A	SOHL, AL, JR	PiM-Aug.'96, '34
    Multifacet Drills		PiM-Oct.'92,16
    Multi-facet milling of radii, & filing to finish	Lautard, Guy	HTIM:22, TMBR#2:105
    Multi-patterns -- Economy in Numbers	DRAYSON, D. A.	PiM-Dec.'96, 18
    Multiple identical castings in epoxy	Lautard, Guy	TMBR#3:115
    Multiple Tool Post for 6" Lathes, A	TRAUB, CARL A	HSM'86:M/A38
    Multi-Purpose Block	JOHNSON, D. E.	HSM'86:S/O21
    Multi-purpose Gadget, A	ALLERS, CHARLES H.	HSM'92:M/A14
    Multi-Purpose Machine, The	BROWNE, DONOVAN V.	PiM Jun. '98 33
    Multi-sheave blocks	Lautard, Guy	TMBR#3:44
    Multi-Stand	BERTRAND, JEFF	HSM'88:M/A25
    Museums Of Interest	HALL	MEW#11,53
    Muzzle brake, shop made	Lautard, Guy	TMBR#3:152
    My shop	Lautard, Guy	TMBR#2:vi; HTIM:51
    My way to a workshop	ROCKEY	MEW#31,62
    Myford lathes	Lautard, Guy	TMBR#1:67
    Natural and artificial stones	Lautard, Guy	TMBR#2:117
    Naval Jelly Uses		HSM'85:M/J14
    Need a Lift?	WAGNER, RAY F.	HSM'95:N/D33
    Networking		HSM'88:J/F63,M/A63,M/J62,J/A62,S/O60,N/D60 
    New Belts	WELLS, NORM	PiM-Dec.'94,MN
    New Centering Gage, A	McLEAN, FRANK A.	HSM'91:M/A50
    New Use for an Old Tool	AUSTILL, BOB	HSM'93:J/P 14
    New Uses for Old Tools	ERNEST, JOHN E	PiM Oct.. 94, 26
    New Vertical Milling Machine, A	McLEAN, FRANK	HSM'85:S/O42
    Nice finish from files	Lautard, Guy	TMBR#1:7
    Nice Priced Handwheel		PiM-Aug.'89,26
    No holds barred	CANNER	MEW#30,40
    No More Hunting		PiM-Apr.'91,24
    No More Shocks	BLOCKER, DAVID C.	HSM'96:M/A 19
    No Need For a Third Hand		PiM-Feb.'88,24
    No-Bounce Soft Hammers	HEDIN, R S	HSM'82:M/A16
    Noisy Spindles		HSM'86:S/O19
    North American Model Engineering Exposition	RICE, JOE	HSM'94:M/A30
    Not breaking small taps	Lautard, Guy	TMBR#1:17
    Notes on Dividing		HSM'87:M/A14
    Notes re drawings	Lautard, Guy	TMBR#2:v; vi HTIM:iii
    Novel Tripod Ball Head, A	WILSON, GLENN L.	PiM-Feb.'93,4
    Novice Adds Some Stops to His Sherline Mill, The	ATKINSON, CHARLES TRACY	PiM Dec. '97 15
    Novice Reports on His Experience with Sherline Tools, A	ATKINSON, CHARLES T.	PiM-Apr.'95 35
    Now how do you get it home?	TITUS	MEW#32,38
    Nozzle Keeper		HSM'91:J/F11
    Number Wheels	KINNAMAN, CARL C.	HSM'92:J/A12
    Odd Thickness Spacers	BIRMINGHAM, CHARLES	PiM-Feb.'93,3
    Odd-leg artistry (setting up by eye)	Lautard, Guy	TMBR#1:81
    Odds and Ends	EVANS, R. W.	HSM'92:S/O14
    Odds and Ends	EVANS, ROBERT W.	HSM'93:S/O15
    Odds n Ends Hit 'n Miss Engine Parts 1-5	DUCLOS PHILIP	HSM'86:N/D22;HSM'87:J/F43,M/A36,M/J26,J/A33
    Of Auctions and Industrial Sales	WALKER, RICHARD B.	HSM'87:J/A36
    Off Hand Grinding Att Unimat3	LOADER	MEW#19,58
    Offshore bandsaw blades vs. good ones	Lautard, Guy	HTIM:42
    Oil & steel wool for a nice finish	Lautard, Guy	TMBR#2:124
    Oil can spout modification	Lautard, Guy	TMBR#2:126
    Oil Container Caps	ZANROSSO, EDDIE M.	PiM-Aug.'94,MN
    Oil Dispenser	FREEMAN, HARVEY	HSM'94:J/F16
    Oil for your lathe centers	Lautard, Guy	TMBR#2:115
    Oil on files	Lautard, Guy	TMBR#1:7; TMBR#3:66
    Oil Sink Cutter	JENNINGS	MEW#9,28
    Oil squirters from shampoo bottles	Lautard, Guy	TMBR#2:104
    Oil used to stick cigarette paper to work	Lautard, Guy	TMBR#1:84
    Old Compound Indexing Table Reworked, The	KUZMACK, RICH	HSM'98:J/F 54
    Old Iron Part 1-3	KOUHOUPT, RUDY	HSM'95:J/F52 M/A50 M/J56
    Old Lathe Collet Adapters	DUCLOS, PHILIP	PiM-Feb.'88,12
    On Improving the Image	MARX, ALBERTO	HSM'92:S/O33
    On making safe wooden lamps	Lautard, Guy	TMBR#3:206
    On Preventing Bloodshed	MARX, ALBERTO	HSM'90:N/D21
    On Pumps and Pumping	MARX, ALBERTO	HSM'98:N/D 50 
    On Safety		HSM'87:S/O16
    On The Cutting Edge	MARX, ALBERTO	PiM-Aug.'90,16
    On the Mark		HSM'83:J/F16
    On the Subject of Stiffness and Overhang	KEET, AUBREY	PiM-Feb.'93,20
    On the Use of Threading Dials for Cutting Metric Threads	PETERSEN, EUGENE E.	HSM'93:N/D49
    One Thing Leads to Another (telescope parts)	EDWARDS, WILLIAM ROLLIN	PiM-Dec.'96, 29
    One Way to "Fix" a Stud	SCHONHER, SPENCER	PiM-Apr.'93,18
    One-evening Projects	RUNGE, WALTER C.	HSM'88:M/A54 
    One-handed Depth Gage, A	DUBOSKY, EDWARD	PiM-Aug.'90,12
    One-inch Height Gage, A	MUELLER, WALTER	PiM-Apr.'94,4
    Oops!		HSM'88:J/A15
    Open-sided Toolholder, An	IIAMES, JAMES	PiM-Feb.'95 17
    Open-sided Toolholder, An	TURNER, RICK	PiM-Feb.'95 17
    Optical centerpunch	Lautard, Guy	TMBR#3:105
    Optimizing Revolver Throats	ACKER, STEVE	MW Jun. 99, 48
    Optivisor	Lautard, Guy	TMBR#3:241
    Orbital sander finish on stainless steel	Lautard, Guy	TMBR#2:111
    Organizing Small Items		HSM'86:M/A15
    Originating a master division plate	Lautard, Guy	TMBR#2:3
    Ornamental Turning Lathe; Product Review	LAUTARD, GUY	HSM'96:M/A 20
    Ornamental turning	Lautard, Guy	TMBR#3:215
    Osborne's manoeuvre	Lautard, Guy	TMBR#2:159
    Osborne's Manoeuvre	Lautard, Guy	TMBR#2:159; TMBR#3:83, 96
    Osborne's Four Steps to Center	MELTON, L.C.	HSM'88:J/A42 
    Other ideas for dial numbering	Lautard, Guy	TMBR#3:247
    Other interests - how to track down people with	Lautard, Guy	TMBR#1:5-6
    Other steam engine designs	Lautard, Guy	TMBR#2:150
    Other-than-Myford #2 MT collets	Lautard, Guy	TMBR#3:11
    Otis Makes an Accurate Final Cut	MELTON, L. C	HSM'89:N/D57
    Otis Measures Across Backlash	MELTON, L. C.	HSM'91:J/F41
    Otis Stops the Chatter	MELTON, L. C.	HSM'91:M/A45
    Out-of-the-Way Storage Where You Need It	VREELAND, DON H.	HSM'91:N/D40
    Oxy-fuel Cutting Guide Jig	PHILLIPS, ORLEY	HSM'84:J/A42
    Paint sticks and sandpaper	Lautard, Guy	TMBR#2:124
    Pair of fly cutters	HALL	MEW#29,44
    Pantograph Label Maker, A	WILSON, GLENN L.	PiM-Apr.'95 4
    Pantographs and other ideas	Lautard, Guy	TMBR#3:248-251
    Parallel Arm Scroll Saw, A	HEDIN, R. S.	PiM-Aug.'88,4
    Parallels	HALL	MEW#13,34
    Parting Off	GRASS, JOHN	HSM'98:M/J 22
    Parting off, essentials of	Lautard, Guy	TMBR#3:111
    Parting Remarks	JOHNS, JACK	HSM'93:M/A13
    Parting Through Large Diameters		PiM-Oct.'88,3
    Parting Tool Modification.	LAMANCE, THOMAS	PiM-Apr.'94,3
    Parts Cleaner	STARNES, RAY E	HSM'86:J/F28
    patch box hinge	Lautard, Guy	TMBR#3:200
    Patience	Lautard, Guy	TMBR#3:2
    Patterns and Molding Procedure Parts 1-6	GINGERY, DAVE	HSM'87:N/D30, HSM'88:J/F30,M/A40,M/J36,J/A38,S/O37
    PC Board Vise	RAUSCHER, ALAN D.	HSM'98:N/D 54
    Peace and Quiet	SULKIN, BARRY	HSM'98:N/D 27 
    Pedestals for shop tools	Lautard, Guy	TMBR#1:140
    Pencil Attachment, A	GASCOYNE, JOHN	PiM-Feb.'94,26
    Pencil lead holder for beam compass	Lautard, Guy	TMBR#3:127
    Perma-grit files	Lautard, Guy	TMBR#3:108
    Personal Safety and Machine Grounding	ACKER, STEVE	PiM-Aug.'94,24
    Personal Safety Equipment	HOFFMAN, EDWARD G.	HSM'87:J/F64
    Personal Safety Habits	HOFFMAN, EDWARD G.	HSM'87:M/A64
    Photo resist for Etching	Lautard, Guy	TMBR#1:136
    Picking up an edge with an indicator (jig borer style)	Lautard, Guy	TMBR#3:94
    Pierced work	Lautard, Guy	HTIM:49; TMBR#3:238-239
    Piloted Tap Guide Wrench, A	LINCOLN, W. A. 'LINK"	HSM'97:M/A 34
    Pin vise made from a Dremel chuck	Lautard, Guy	TMBR#3:172
    Pin Vise	ZANROSSO, EDDIE M.	HSM'94:J/A16
    Pipe Center for your Lathe, A	SCHARPLAZ, JAMES D.	PiM-Oct.'89,8
    pipe flanges	Lautard, Guy	TMBR#3:29
    Pipeline to Prosperity	BROWN, MIKE	HSM'87:M/J32
    Plain Mans Guide To Matls, Parts l-3	LOADER	MEW#20,32;#21,53;#22,59
    Plain Talk About Stick Electrode Arc Welding	HUNT, CHARLES K	HSM'83:M/J22,J/A28
    Planer, Slotter And Shaper, Parts l-2	UNWIN	MEW#19,38;#20,59
    Planing knots & twisted grain	Lautard, Guy	TMBR#3:195
    Planning a Small Shop	McLEAN, FRANK A	HSM'82:J/F42
    Plans and info for a power hacksaw	Lautard, Guy	TMBR#1:197
    Plastic Injection Molding Machine Parts 1-4	HANSON, RODNEY W.	HSM'91:M/J16,J/A32,S/O44,N/D32
    Plastics Forum, The Parts 1-5	SELTER, PAUL E, Sr.	HSM'86:M/A44,J/A42,N/D36;HSM'87:J/F48,M/A34
    Plastigage in the Shop	GRABHORN, MERLE	PiM-Dec.'93,20
    Plate vs. sheet steel (terminology)	Lautard, Guy	TMBR#2:11
    Plate vs. sheet	Lautard, Guy	TMBR#2:11
    Platform for the Hart	HALL	MEW#23,56
    Plus or Minus?	MADISON, JAMES	PiM-Feb.'95 32
    Plywood bandsaw	Lautard, Guy	HTIM:38-43; TMBR#3:184
    Plywood	Lautard, Guy	TMBR#3:191
    Pocket microscope for examining reamer flutes	Lautard, Guy	TMBR#3:158
    Pocket-sized, Gift Quality Blow Gun, A		PiM-Oct.'95 4
    Point of Safety		PiM-Oct.'91,3
    Polishing and Utility Lathe, A	HOFF, MIKE 	MW Oct. 99, 18
    Polishing		HSM'88:N/D16
    Polymer resin "castings" from CAD drawings	Lautard, Guy	TMBR#3:97
    Polyurethane casting resin	Lautard, Guy	TMBR#3:115
    Poor Man's "T" Handle		HSM'90:J/F14
    Poor Man's Electronic Edge Finder, A	PELLIZZARI, F. A.	PiM-Aug.'95 26
    Pop Can Crusher, A	PETERSEN, BIRK	MW Aug. 99, 13
    Poshin' Up a Taiwanese Lathe	LAUTARD, GUY	HSM'91:M/J23
    Poshin' Up a Taiwanese Lathe	WARREN, WALT	HSM'91:M/J23
    Pot Chuck		PiM-Feb.'91,3
    Pot hooks for the kitchen	Lautard, Guy	TMBR#3:55
    Potpourri, A	WASHBURN, ROBERT A.	HSM'85:S/O54 
    Power Drive for Lathe Chucks	SOUTHWICK, F. D.	PiM Apr. '98 37
    Power Feed Ball Turning Fixture	VREELAND, DON H.	PiM-Dec.'90,20
    Power Quill Feed Attachment, A	DWORZAN, P.	HSM'87:S/O25
    Power Saw Blades		HSM'89:M/J16
    Power Traverse-Milling MC, Parts 1-3	MACHIN	MEW#14,61;#15,64;#16,43
    Practical Design Hints Part IV Assembly	STRASSER, FREDERICO	HSM'84:J/F46
    Practical joke - hacksaw blade set on toolbox	Lautard, Guy	TMBR#1:130
    Precise Tailstock Setover		HSM'90:M/A16
    Precision Metal Stamper, A	WILSON, GLENN L.	PiM-Dec.'93,4
    Precision tilting V-block	Lautard, Guy	TMBR#2:80
    pre-load spring for Solid cotters	Lautard, Guy	TMBR#1:100
    Preparing steel for painting	Lautard, Guy	TMBR#2:115
    Presentation Swarf Collector, The	JONES, BRUCE	PiM-Dec.'88,12
    Prevent Scale Adhesion		PiM-Apr.'88,24
    Prevent Slipping		PiM-Feb.'90,3
    Preventing Blade Binding		PiM-Apr.'91,23
    Preventing Scoring		PiM-Apr.'91,23
    Prick punches and center punches	Lautard, Guy	TMBR#3:104
    Primary and secondary relief angles on reamers	Lautard, Guy	TMBR#3:157
    Prime number division	Lautard, Guy	TMBR#2:8
    PRIME	RICE, JOE	HSM'98:J/F 56
    Product Opinion	HOFFMAN, EDWARD G.	PiM-Oct.'95 37
    Product Review 5C Callet Chuck, A	LAUTARD, GUY	HSM'99:S/O 24
    Product Review Brass Clock Kit	McKINLEY, MARK	HSM'99:N/D 24
    Product Review Machinery's Handbook, 25th Edition CD ROM Version	HOFFMAN, EDWARD C.	HSM'99:M/J 28
    Product Review The Sakai ML-360	LIOUFIS, MARIOS M	MW Apr. 99, 38
    Product Review: "In Line" Vise Positioner	RICE, JOE	HSM'91:M/J12
    Product Review: 950 Bead Blaster from Skat Blast	ACKER STEVE	HSM'97:J/A 26
    Product Review: Accu-Finish 11 Precision Tool Sharpener		HSM'89:S/O20
    Product Review: Adjustable Packing Blocks	KOUHOUPT, RUDY	HSM'94:M/A18
    Product Review: AMT Radial Drill Press	HOFFMAN, EDWARD G.	HSM'94:M/J16
    Product Review: An Owner's Review of the Jet JVM-840	WELLCOME, STEVE	HSM'86:S/O12
    Product Review: Anton Angular Gage Blocks	HOFFMAN, EDWARD G.	HSM'85:M/A10
    Product Review: Anton Toolmaker's Dream Kit	HOFFMAN, EDWARD G.	HSM'85:J/A11
    Product Review: ATCO Combo-Cube	HOFFMAN, EDWARD G.	HSM'85:S/O12
    Product Review: Athens Centering Thimbles	HOFFMAN, EDWARD G.	HSM'85:M/J10
    Product Review: Band Saw Splicer	RICE, JOE	HSM'92:M/A12
    Product Review: Barker Horizontal Milling Machine	HOFFMAN, EDWARD G.	HSM'85:J/F8
    Product Review: Brown & Sharpe Digital Electronic Caliper	HOFFMAN, EDWARD G.	HSM'83:J/A8
    Product Review: BTI - Super "T" Drivers	HOFFMAN, EDWARD G.	HSM'86:J/F10
    Product Review: CAD for the Small Shop	HOFFMAN, EDWARD G	HSM'92:J/A14
    Product Review: Cameron Series 164 Micro Drill Press	GASCOYNE, JOHN	HSM'92:J/A15
    Product Review: Carr Lane Spring Locating Pins	HOFFMAN, EDWARD G.	HSM'90:S/O16
    Product Review: CBX System DRO by Shooting Star Technology	TOLLENAAR, DIRK 	MW Aug. 99, 28
    Product Review: Challenger Gage Block Set	HOFFMAN, EDWARD G.	HSM'86:M/A10
    Product Review: Chinese- and American-made Vernier Calipers	LAUTARD, GUY	HSM'93:J/A12
    Product Review: Convert It	HOFFMAN, EDWARD G.	HSM'93:M/J14
    Product Review: Craftmark Zero/Zero Center Finder	HOFFMAN, EDWARD G.	HSM'85:J/A10
    Product Review: Criterion Boring Head	HOFFMAN, EDWARD G.	HSM'84:J/A8
    Product Review: Darex Corporation's Drill Doctor	JOLY DAVID	HSM'97:J/A 28 
    Product Review: Darex M3 Drill Sharpener	HOFFMAN, EDWARD G.	HSM'84:S/O8
    Product Review: Dillon Mk III Welding & Cutting Torch	HOFFMAN, EDWARD G.	HSM'84:N/D8
    Product Review: Dupli-Carver Band Saw	HOFFMAN, EDWARD G.	HSM'84:M/A8
    Product Review: Emco Compact 10 Lathe	HOFFMAN, EDWARD G.	HSM'83:N/D15
    Product Review: Emco Compact 5	HOFFMAN, EDWARD G.	HSM'83:J/F9
    Product Review: Emco Maier FB-2 Milling Machine	HOFFMAN, EDWARD G.	HSM'84:J/A6
    Product Review: Emco Maier Maximat Super II	HOFFMAN, EDWARD G.	HSM'84:J/F9
    Product Review: Fisher "Pee Dee" Thread Measuring Wires	HOFFMAN, EDWARD G.	HSM'84:M/A11
    Product Review: Fisher 5" Sine Bar	HOFFMAN, EDWARD G.	HSM'84:J/F8
    Product Review: Fisher Edge and Center Finders and Tap Guide	HOFFMAN, EDWARD G.	HSM'83:N/D12
    Product Review: Fisher Universal Indicator Holder	HOFFMAN, EDWARD G.	HSM'83:S/O8
    Product Review: Fowler Heavy Duty Dial Caliper	HOFFMAN, EDWARD G.	HSM'83:M/J10
    Product Review: Fu San 8" Metal Lathe	SCOTT, EDWARD H.	HSM'88:J/F14
    Product Review: Glendo Accu-Finish Tool Sharpener	HOFFMAN, EDWARD G.	HSM'83:N/D12
    Product Review: Greenfield Tap Wrenches	LAUTARD, GUY	HSM'90:N/D16
    Product Review: Grizzly G4000 Lathe	PERKINS, DON	HSM'97:N/D 17 
    Product Review: Huron Workholding System		HSM'89:N/D16
    Product Review: Infinity Precision Boring Head	HOFFMAN, EDWARD G.	HSM'85:S/O8
    Product Review: John Deere Model E	RICE, JOE	HSM'98:M/A 24
    Product Review: Kalamazoo 4.00" Belt Sander	HOFFMAN, EDWARD G.	HSM'85:S/O10
    Product Review: Knorrostol	LAUTARD, GUY	HSM'93:S/O17
    Product Review: Kroy Light Table	HOFFMAN, EDWARD G.	HSM'83:J/A8
    Product Review: Lawrence Drill Press Table	HOFFMAN, EDWARD G.	HSM'83:M/J10
    Product Review: Learn CAD Now and Easy CAD 2	RICE, JOE	HSM'94:J/F18
    Product Review: Loc-Line Modular Hose System		HSM'89:M/J14
    Product Review: Maier Lathe Chucks	HOFFMAN, EDWARD G	HSM'84:N/D9
    Product Review: Manhattan 3-in-1 Drill Set	HOFFMAN, EDWARD G.	HSM'83:S/O8
    Product Review: Math Solutions At Your Fingertips		HSM'92:N/D56
    Product Review: Math Solutions At Your Fingertips	HOFFMAN, EDWARD G	HSM'92:N/D56
    Product Review: Math Solutions for Your Computer	HOFFMAN, EDWARD G.	HSM'98:M/A 25
    Product Review: Math Solutions: Any Angle	HOFFMAN, EDWARD G.	HSM'93:N/D16
    Product Review: Math Solutions: Craft-E	HOFFMAN, EDWARD G.	HSM'93:N/D16
    Product Review: Math Solutions: Mr. Machinist	HOFFMAN, EDWARD G.	HSM'93:N/D17
    Product Review: Math Solutions: NBS Trig and NBS Toolpath	HOFFMAN, EDWARD G.	HSM'93:N/D18
    Product Review: Math Solutions: Shopmathster II	HOFFMAN, EDWARD G.	HSM'93:N/D19
    Product Review: Mecanix L-150 Universal Machine Tool	NIERGARTH, RAYMOND D.	HSM'86:M/J12
    Product Review: Micrografx Designer 3.1	RICE, JOE	HSM'94:J/F19
    Product Review: Mitchell Abrasive Cords and Tapes	HOFFMAN, EDWARD G.	HSM'84:M/J9
    Product Review: Mitee-Bite Clamping System		HSM'89:M/A16
    Product Review: Mr. Cushion Step	LAUTARD, GUY	HSM'93:S/O57
    Product Review: Nonmetallic Tooling Alternative	HOFFMAN, EDWARD G	HSM'95:N/D26
    Product Review: Northwestern Clamping Kit	HOFFMAN, EDWARD G	HSM'84:J/A8
    Product Review: Omni-Post Quick Change Toolpost	HOFFMAN, EDWARD G.	HSM'87:J/F14
    Product Review: Optical Locator	RICE, JOE	HSM'87:J/A11
    Product Review: Quorn Mark II Grinder	HOFFMAN, EDWARD G.	HSM'85:M/A12
    Product Review: Rank Scherr-Tumico Micrometer Set	HOFFMAN, EDWARD G.	HSM'83:M/A9
    Product Review: Richlite Fibre Laminate	HOFFMAN, EDWARD G	HSM'98:N/D 26 
    Product Review: Rockwell Sander/Grinder	HOFFMAN, EDWARD G.	HSM'83:M/A8
    Product Review: Rovi Expanding Mini Collets	HOFFMAN, EDWARD G.	HSM'90:M/J16
    Product Review: Royal Clamping System		HSM'89:J/F14
    Product Review: S- T Industries Universal Dial Indictor Test Set	HOFFMAN, EDWARD G.	HSM'85:N/D8
    Product Review: Scherr-Tumico Machinist Tool Set	HOFFMAN, EDWARD G.	HSM'85:M/J8
    Product Review: Sears 15 l/2'' Drill Press	HOFFMAN, EDWARD G.	HSM'84:M/A10
    Product Review: Sears Bench Grinder	HOFFMAN, EDWARD G.	HSM'84:M/J8
    Product Review: Sears Hardwood Machinist's Tool Chest	HOFFMAN, EDWARD G.	HSM'85:M/A10
    Product Review: Sears Tap and Die Sets	HOFFMAN, EDWARD G.	HSM'83:S/O9
    Product Review: Shooting Star Technology CBX Digital Readout	GRAFF, JOHN	HSM'98:J/A 26
    Product Review: Shop Math Computer	HOFFMAN, EDWARD G.	HSM'90:J/F18
    Product Review: ShopTronics Digital Readout	HOFFMAN, EDWARD G.	HSM'85:M/J11
    Product Review: Small Magnetic V-block, A	LAUTARD, GUY	HSM'91:N/D43
    Product Review: Smithy CB 1 220 XL	HANEY LON	HSM'97:M/A 49
    Product Review: Snap Jaws	LAUTARD, GUY	HSM'90:M/J18
    Product Review: SPI Space Block Set	HOFFMAN, EDWARD G.	HSM'84:J/F8
    Product Review: S-T Industries 12" Height Gage	HOFFMAN, EDWARD G.	HSM'84:S/O8
    Product Review: S-T Industries Electronic Digital Caliper	HOFFMAN, EDWARD G.	HSM'85:J/A8
    Product Review: Starrett Trammel Set	HOFFMAN, EDWARD G.	HSM'84:M/J9
    Product Review: Starrett's No. 164 Series "A" Clamp	LAUTARD, GUY	HSM'94:N/D55
    Product Review: Taig Micro Mill	ROSS, HERMAN	MW Oct. 99, 27
    Product Review: The Diamond Toolholder	KOUHOUPT, RUDY	HSM'93:J/A16
    Product Review: The Manupress,	LAUTARD,GUY	HSM'89:S/O17
    Product Review: The Paragon Q-11A Heat-treating Furnace	ACKER, STEVE	HSM'94:J/F20
    Product Review: The Sherline #5000 Vertical Milling Machine	HOFFMAN EDWARD G	HSM'82:N/D16
    Product Review: Thermal Dynamics Air Plasma Cutting System	HESSE, JIM	HSM'98:S/O 25
    Product Review: Thompson T/C Mill-Drill Table	HOFFMAN, EDWARD G.	HSM'85:J/F10
    Product Review: TRIM Computer	HOFFMAN, EDWARD G.	HSM'88:S/O11
    Product Review: Tru Punch Shim Punch and Die Set	LAUTARD, GUY	HSM'93:M/A14
    Product Review: TWF Industries "Machinist Assortment"	HOFFMAN, EDWARD G.	HSM'85:N/D6
    Product Review: Two New Twist Drills	JEDLICKA, JIM	HSM'90:J/F15
    Product Review: Ultra-Thin Parallels	LAUTARD, GUY	HSM'91:S/O15
    Product Review: Vee-Grooved Snap Jaws		HSM'92:M/A11
    Product Review: Vernier Protractor		HSM'92:S/O12
    Product Review: Waldmann Spotlight	HOFFMAN, EDWARD G.	HSM'86:J/A10
    Product Review: Westhoff Mighty Mag		HSM'89:J/A64
    Product Review: Westhoff Mighty Mag	HOFFMAN, EDWARD G.	HSM'85:N/D6
    Product Review: Westhotf Magna-Base	HOFFMAN, EDWARD G.	HSM'86:M/A10
    Product Review: Whistler Metaligner Dowel Pins	HOFFMAN, EDWARD G.	HSM'90:N/D16
    Product Review: Workshop Tool 8, Accessory Plans	RICE, JOE	HSM'94:M/A18
    Product Review: Workshop Tools & Accessory Plans		HSM'94:M/A18
    Product Review: Zero-It Indicator Adapter	HOFFMAN, EDWARD G.	HSM'86:J/F10
    Projects at Home		HSM'85:J/F38 
    Propane torch, made at home	Lautard, Guy	TMBR#1:52
    Proper Grounding of Power Tools	WIREMAN, TERRY	HSM'84:N/D52
    Proper Use of Diamond Dressers, The	BOCHERT, JOHN	HSM'96:J/A 56
    Protect That Slide	HALL	MEW#9,29
    Protect Threads		PiM-Dec.'88,24
    Protect Your Mill from Shavings	McLEAN, FRANK A.	HSM'87:J/A56
    Protect Your Shop from Voltage Spikes	HINSHAW, LOU	HSM'88:J/F28
    Protecting Cutting Edges		HSM'87:J/F20
    Protecting Taps		PiM-Jun.'89,26
    Protecting Threads	LAMANCE, THOMAS	PiM Oct.'97 3
    Protecting Your Chisels		PiM-Apr.'89,24
    Protective mats for the milling machine table	Lautard, Guy	TMBR#3:76
    Protective Vise Jaws	OTT, JACK	HSM'91:J/F43
    Pseudo Drawbar for the Tailstock, A	NYMAN, PHIL	HSM'96:N/D52
    P-style Upside-down Partoff Blade Holder	YAMAMOTO, MICHAEL	PiM-Jun.'94,28
    Pulley Arrangement vs. Spindle Speed	REYNOLDS, JIM	HSM'98:J/A 44
    Pulley Puller,	A WORZALA, J.	HSM'90:N/D35
    Pulling a "T" in copper pipe	Lautard, Guy	TMBR#3:80
    Pulling pins from truck springs	Lautard, Guy	TMBR#3:108
    Punching shapes in thin sheet metal on a Bridgeport	Lautard, Guy	TMBR#2:129
    Purchasing a computer for CAD	OPPENHEIM	MEW#21,26
    Purchasing Aluminum	HAUSER, JAMES W.	MW Aug. 99, 45
    Purpose of the ball on a surface gage spindle	Lautard, Guy	TMBR#2:131
    Putting on fine cuts by angling the topslide	Lautard, Guy	TMBR#1:12, 15
    Puzzles: Conway's	Lautard, Guy	HTIM:50-51
    Puzzles: Slothouber-Graatsma	Lautard, Guy	HTIM:50
    PVC or copper pipe for compressed air piping	Lautard, Guy	TMBR#3:12
    Q & A		HSM'83:M/A10
    Q & A	BLOOM, HARRY	HSM'83:N/D21
    Q & A	EVERETT, LYNN	HSM'83:M/A11,J/A10
    Q & A	HOFFMAN, EDWARD G.	HSM'84:M/J12,J/A12,N/D22
    Q & A	KOUHOUFT, RUDY	HSM'83:J/A10
    Q & A	McLEAN, FRANK	HSM'83:J/F13,J/A10,S/O12
    Q & A	NIERGARTH, RAY	HSM'84:J/F12,M/A12,M/J12,J/A12
    Q & A	NIERGARTH, RAYMOND D.	HSM'83:M/J12,S/O12,N/D20
    Q&A		HSM'87:J/F23
    Q&A	BLOOM, HARRY	HSM'87:J/F24,S/O14
    Q&A	BLOOM, HARRY	HSM'90:M/J19
    Q&A	DEWBERRY, O. J	HSM'88:M/J13
    Q&A	EVANS, RICHARD E.	HSM'85:N/D22 
    Q&A	GASCOYNE, JOHN B.	HSM'85:M/J18 
    Q&A	KOUHOUPT, RUDY	HSM'85:S/O18
    Q&A	LAUTARD, GUY	HSM'88:N/D12
    Q&A	LEWIS, JAMES A	HSM'85:M/J18
    Q&A	LEWIS, JAMES R.	HSM'87:J/F23,M/A20
    Q&A	McLEAN, FRANK	HSM'85:M/J19,J/A14,S/O18
    Q&A	NIERGARTH, RAYMOND D.	HSM'85:M/J19 
    Q&A	ROUBAL, TED	HSM'88:M/A12
    Q&A	SELTER, PAUL E., SR.	HSM'87:M/J19
    Q&A	SMITH, TIM	HSM'87:N/D17
    Quenching Techniques	SCHARABOK, KEN	PiM-Apr.'96, 44
    Quest for Mr Morse	LOADER	MEW#26,58
    Quick and Accurate Center Punching		HSM'91:J/F10
    Quick and Easy Electric Furnace	CORTNER, ROBERT	PiM-Jun.'91,18
    Quick change gearbox for Myford.	PRATT	MEW#22,64
    Quick change inserts for your mill's depth stop	Lautard, Guy	HTIM:36
    Quick change toolholder	BOWNESS	MEW#26,15
    Quick change vise jaw liners	Lautard, Guy	TMBR#3:69
    Quick detach sine fixture for your milling vise	Lautard, Guy	TMBR#2:80
    Quick Gear Selection		PiM-Dec.'89,24
    Quick Graduated Collars	VERDIANI, DON	HSM'98:N/D 46
    Quick Quill Stop	CLAUDE, ROGER	PiM Oct.'97 26
    Quick Rust Inhibiting Finish for Ferrous Parts, A	JOHNS, MICHAEL	PiM-Dec.'95 42
    Quick Setup Gage, A		PiM-Aug.'89,28
    Quick Threading and Tapping in the Lathe	HOFF, MICHAEL F., Jr.	HSM'86:N/D38
    Quick-acting Tailstock Lock, A	CALDER, JOHN	PiM-Oct.'92,20
    Quick-acting Universal Lathe Mandrel	JOHNSON, D. E.	PiM-Apr.'94,31
    Quick-Adjust Depth Stop	WOOD, GRANT W.	HSM'83:J/A56
    Quick-change Gearbox, A	TOSCANO, EUGENE	PiM Aug.'89 10, Oct.'89 11
    Quick-change Indicator Holder	EVERS, HOWARD W.	PiM Feb. '98 31
    Quick-change Tool Post, A	DOBIAS, DONALD	PiM Aug.'97 24
    Quickie bandsaw blade welding jig	Lautard, Guy	TMBR#2:126
    Quick-release Tailstock Lock for Small Lathes, A	GOVUS, STEVE	PiM Jun.'97 20
    Quick-release T-rest for the Sherline Lathe, A	SMITH, W. R	HSM'96:J/A 36
    R8 Lathe Collet Holder, An	BIDDLE, H. T.	PiM-Apr.'96, 30
    Radio Shack parts required	Lautard, Guy	TMBR#3:31
    Radius Turning Attachment	CLARKE, THEODORE M.	HSM'83:J/A32
    Radius Turning on The Metal-Working Lathe		HSM'83:N/D24
    Radius Turning Tool	MARTLN, WILL	HSM'86:J/A16
    Radiusing the ends of a part	Lautard, Guy	TMBR#2:105
    Raising block for the Unimat3	LOADER	MEW#32,52
    Raising Work	NOBLE, BURT	PiM Feb.'97 44
    Ram Tailstock, A	CLARKE, THEODORE M.	PiM-Dec.'88,11
    Ramming the Mold for a Metal Casting	LEWIS, JAMES R.	HSM'84:S/O46
    Random Orbital Sander	CROW, ARTHUR	PiM Dec. '97 26
    Rapid Machine Tapping Drillpress	ROUBAL, WM. T. (TED), Ph.D.	HSM'84:M/J20
    Reaching the Unreachable		PiM-Dec.'91,24
    Reader Survey Report	HALL	MEW#20,62
    Reader Survey Report	HALL	MEW#9,18
    Reader Survey Report	SHEPPARD	MEW#29,48
    Ready Ink Applicator	LAMANCE, THOMAS	PiM Feb. '98 40 
    Readying the Lathe for Work	YOUNG, BARRY	MW Apr. 99, 42
    Real Do-it-yourself Threading Dial, A	WINIECKI, TED	MW Feb. 99, 10
    Realigning the tailstock center	Lautard, Guy	TMBR#2:92
    Reamer sharpening	Lautard, Guy	TMBR#3:157-161
    Reamer sharpening, Choice of stones	Lautard, Guy	TMBR#3:162-164
    Reamer Stoning technique	Lautard, Guy	TMBR#3:165
    Reamer Tips	MADISON, JAMES	PiM-Jun.'96, 38
    Reamers And Reaming	LOADER	MEW#13,66
    Reamers for Odd Sized Holes	ROSCOE, LOWIE L., JR.	PiM-Apr.'92,12
    Reaming	Lautard, Guy	TMBR#1:16
    Reaming, Made from a dowel pin	Lautard, Guy	TMBR#3:66
    Reaming, On not ruining	Lautard, Guy	TMBR#1:16
    Rear Sight Shifter, A	ACKER, STEVE	MW Feb. 99, 38
    Rear Tool Post (Reversible) for Atlas or Craftsman 6" Swing Lathes	GASCOYNE, JOHN B.	PiM Feb. '98 14
    Re-babbetting machinery bearings	Lautard, Guy	TMBR#1:135
    Rebirth of a Model C South Bend Lathe, The	GRAHAM, DOUGLAS	HSM'96:N/D49
    Rebuilding "scrapped" equipment	Lautard, Guy	TMBR#3:228
    Rebuilding alternators	Lautard, Guy	TMBR#3:109
    Recipe for a good cutting lube	Lautard, Guy	TMBR#1:177; TMBR#3:77
    Recipe for artists etching ground	Lautard, Guy	TMBR#3:245
    Recommended SFM for lathe filing	Lautard, Guy	HTIM:46
    Reconditioning a Lathe Parts I-VI	BLOOM, HARRY	HSM'84:J/F24,M/A40,M/J48,J/A49,S/O42,N/D48
    Reconditioning an Atlas Milling Machine, Parts 1-3	KOUHOUPT, RUDY	HSM'97:M/A 46, M/J 58, J/A 60
    Reconditioning Your Chuck	LAMANCE, THOMAS	PiM-Dec.'93,3
    Recycling a Mirror	SEXTON, TERRY	PiM-Apr.'93,21
    Recycling Broken Center Drills		HSM'90:M/A16
    Reducing Chip Gathering		PiM-Feb.'91,3
    Reducing errors in copying a master division plate	Lautard, Guy	TMBR#2:6
    Reducing Expense		HSM'87:S/O16
    Reducing Tap Breakage	JOHNSON, D.E.	HSM'88:M/A37
    Ref. to an article on making straightedges	Lautard, Guy	HTIM:48
    Ref. to an article on restoring a bandsaw	Lautard, Guy	TMBR#3:186
    Releasable mandrel handle	BRAY	MEW#29,68
    Reliable Drill Guide, A		PiM-Jun.'90,24
    Relocating Work	MANCE, THOMAS 	MW Jun. 99, 10
    Reminder	LAMANCE, THOMAS	PiM-Dec.'94,3
    Remote Switch for the Mill	VOSS, C. O.	HSM'96:M/J 49
    Remounting a Four-jaw Chuck	WADHAM, G.	HSM'91:J/F25
    Removable High Performance Disks for Your Computer System	HOFFMAN, EDWARD G.	HSM'91:M/A12
    Removable Tie-down	KINZER, DWIGHT	PiM Dec. '98 41 
    Removal of broken taps from aluminum	Lautard, Guy	TMBR#3:78
    Removal of stuck bullets from rifle/pistol barrels	Lautard, Guy	TMBR#3:156
    Removing A Wire Brush		HSM'88:l/A 14
    Removing Bearings and Bushings		PiM-Dec.'88,24
    Removing Broken Screws and Studs	HOFFMAN, EDWARD G	HSM'92:M/J37
    Removing Broken Screws		HSM'86:J/A12
    Removing broken taps	Lautard, Guy	TMBR#1:18
    Removing burrs from new taps	Lautard, Guy	TMBR#1:17
    Removing Bushings from Blind Holes		PiM-Apr.'89,24
    Removing Labels		HSM'88:J/F12
    Removing Saw Burrs on Tubing		HSM'87:J/A17
    Removing that last half thou	Lautard, Guy	TMBR#1:12-15; TMBR#3:29 & 139
    Removing Threaded Chucks	HESTER, DON	PiM Oct.. 94, MN
    Renewing Half Nuts		HSM'89:J/A25
    Renovating A Compressor	LAMMAS	MEW#13,18
    Repairing an Old Lathe	McLEAN, FRANK A.	HSM'87:N/D59
    Repeat Threading (Tips & Tricks)	WILSON, J. R., JR	PiM-Feb.'95 48
    Repeatable Quick-Change Tool Holder	SCHROEDER, ARDEN	HSM'89:M/J40
    Replacing an Integral Front Sight	ACKER, STEVE	MW Apr. 99, 35
    Replacing the Lathe Spindle Belt	BUCCA, JOSEPH, JR.	HSM'93:M/J12
    Reproducing a Taper		HSM'89:S/O14
    Research methods	Lautard, Guy	TMBR#3:4-5
    Resetting Lathe Tool Height		PiM-Aug.'90,24
    Resetting stone in diamond dresser	Lautard, Guy	TMBR#2:66
    Restoring a Transit	DOW, G. S.	HSM'89:J/A49
    Restoring Battered Threads		HSM'89:N/D14
    Retaining ring ("circlip"), shop made	Lautard, Guy	HTIM:l1-12
    Retrofitting Atlas/Craftsman and Other Lathes to CNC Control Parts 4, 5	FRIESTAD, R. W.	HSM'94:J/F52,M/J48
    Retrofitting Atlas/Craftsman and Other Lathes to CNC Control, Parts 1, 2	FRIESTAD, R. W	HSM'93:M/J48,S/O49
    Returning The Tailstock On-Center		HSM'84:J/A16
    Reuse Broken Drills	VAN VEGHEL, L. A.	HSM'94:M/A55
    Reverse for a Small Lathe, A	FELLER, E.T.	PiM-Apr.'88,16
    Reverse is Handy		HSM'86:N/D12
    Reversible 2-speed appliance motors for shop drives	Lautard, Guy	TMBR#3:57
    Reversible Lathe Carriage Stop	BOROWICZ, TOM	PiM-Feb.'93,24
    Reversible Lathe Die Holder	BLANDFORD, PERCY	PiM-Jun.'89,19
    Reversible Power Feed		HSM'91:M/J10
    Reversing Rotation on a Single Split-phase Motor	ZUMWALT, ROBERT B.	PiM Dec. '98 38
    Reversing the Power Feed	GEESE, ROLF A.	PiM-Dec.'94,MN
    Reviewing CAD Systems Part 1	FRIESTAD, ROLAND	HSM'90:N/D49
    Reviving a Lunch Break Shaper	SEXTON, TERRY	HSM'94:N/D22
    Rifle cleaning rod	Lautard, Guy	TMBR#3:169-171
    Rifling machine, Bill Webb's	Lautard, Guy	TMBR#3:167; TMBR#2:198
    Right Triangles, Part 1	HOFFMAN, EDWARD G	HSM'89:S/O22,N/D18
    Rigid Tool Bit Clamp, A	GENEVRO, GEORGE	HSM'97:S/O 54
    Ring Furnace, A		PiM-Oct.'92,28
    Rise and Fall of the Taiwanese Band Saw, The	STRAMPE, SCOTT D.	PiM-Jun.'93,28
    Risers for a 6" Atlas or Craftsman Lathe	METZE, ROBERT W.	PiM-Apr.'90,22
    Riveting Press, A	PETERSEN, BIRK	PiM Jun. '98 6
    Robbins and Lawrence legacy, 'The -Proven Interchangeability      	McCARTHY, BII.L	MW Dec. 99, 53
    Rocker Retainer	WOOD, GRANT W.	HSM'83:J/F43
    Rocking, Swinging Grinder Table, A	MASON, HAROLD	PiM-Feb.'88,4
    Rockwell Sander/Grinder		HSM'83:M/A8
    Roll over triggers	Lautard, Guy	TMBR#3:143
    Rolling Tailstock Arbor, A	JOHNSON, D. E.	PiM-Jun.'90,8
    Rong Fu Headlock		PiM Apr. '98 28
    Ross Box, The	COSS, TERRY	MW Jun. 99, 18
    Rotary Indexing Fixture 	GEISLER, FRED	MW Feb. 99, 4
    Rotary Milling Table Parts I, II	KADRON S. F.	HSM'84:M/J28,J/A30
    Rotary Table - choice of horizontal or hor/vert.	Lautard, Guy	TMBR#1:41
    Rotary Welding Table, A	FLEMING, JIM	HSM'86:M/J45
    Rotary, Dual Cross-slide Drill Press and Milling Machine Table Parts 1-4	GASCOYNE, JOHN	HSM'91:M/A40,M/J38,J/A36
    Rotating Centre	WATKINS	MEW#20,21
    Rothenberger tube expander and T-extractor	Lautard, Guy	TMBR#3:82
    Rough dividing via marks on the lathe chuck	Lautard, Guy	TMBR#2:9
    Rough down, then finish tapers by grinding	Lautard, Guy	TMBR#2:92
    Round File Handles		HSM'85:M/A16
    Round Keys Reduce Fatigue Failures 	STRAIGHT, J. W.	MW Jun. 99, 37 
    Round Stock Welding Jig, A	DeLONG, JAMES	MW Feb. 99, 35
    Rounding the Ends	McLEAN, FRANK A.	HSM'93:J/A52
    Rubber Tires		HSM'86:N/D12
    Rubberdraulic (& see Obscure)	Lautard, Guy	TMBR#1:71; TMBR#2:123
    Rubberflex collets	Lautard, Guy	TMBR#3:11
    Ruger handguns, modified/rebuilt by Hamilton Bowen	Lautard, Guy	TMBR#3:154
    Rugged Tap Wrench, A	BLYSTONE, DAVID	PiM-Dec.'93,31
    Rule #1 on shop safety	Lautard, Guy	TMBR#2:152
    Rule #2 on shop safety	Lautard, Guy	TMBR#2:153
    Rule Guide for Easier Layout	HOFFMAN, EDWARD G.	HSM'91:J/A39
    Rule Holder		PiM-Aug.'90,24
    Rule of Thumb		PiM-Feb.'88,24
    Rules - Differential and Difference	DUBOSKY, ED	PiM-Feb.'92,19
    Rumbling tumbler	GOULD	MEW#26,34
    Rust preventative made from Stockholm tar	Lautard, Guy	TMBR#3:77
    Rust Preventive #2 on files	Lautard, Guy	TMBR#1:8
    Rust removal with oil & steel wool	Lautard, Guy	TMBR#2:124
    Rust, Caused by glue	Lautard, Guy	TMBR#1:122
    Rust, Caused by plastic foam	Lautard, Guy	TMBR#1:122
    Saddle stop and index arm	GRAY	MEW#26,60
    Saddle V-Block	DUBOSKY, ED	PiM-Feb.'89,4
    Safe Outlets (Chips & Sparks)	LOCATI, GREG	HSM'95:M/J18, S/O20
    Safe speeds for lathe chucks	Lautard, Guy	TMBR#3:62
    Safe thinking	GINN	MEW#24,32
    Safer filing in the lathe	Lautard, Guy	TMBR#2:132
    Safety Chain		HSM'88:M/A13
    Safety Tips Common Hardware	HOFFMAN, EDWARD G.	HSM'88:M/J64
    Safety Tips Using Hand Files and Scrapers	HOFFMAN, EDWARD G.	HSM'88:J/F64
    Safety Tips Using Layout Tools	HOFFMAN, EDWARD G.	HSM'88:M/A64
    Safety Tips Using Taps and Dies, Parts 1-2	HOFFMAN, EDWARD G.	HSM'88:J/A64,S/O64
    Safety Tips: Common Hardware, Part 2-4		HSM'89:J/F64,M/A64,M/J64
    Safety Tips: Shop Layout Part 2-5	HOFFMAN, EDWARD G.	HSM'85:J/F20,M/A51,J/A64,S/O64
    Safety Tips: Shop Storage Parts 2-4	HOFFMAN, EDWARD G.	HSM'86:J/F64,M/A64,M/J64
    Safety Tips: Storage of Flammable Liquids Parts 1, 2	HOFFMAN, EDWARD G.	HSM'86:J/A64,S/O64
    Safety Tips: Using Toxic Materials	HOFFMAN, EDWARD G.	HSM'86:N/D64
    Safety When Polishing Ball Handles		HSM'85:M/A18
    Safety when using a table saw	Lautard, Guy	TMBR#3:189
    Safety with a shop made surface grinder	Lautard, Guy	TMBR#2:59-60; TMBR#3:233
    Salability of models of various	Lautard, Guy	TMBR#3:206-207
    Salability of models: Helicopter rotor hub	Lautard, Guy	TMBR#3:207
    Salability of models: Miniature firearms	Lautard, Guy	TMBR#3:207
    Salability of models: Model Bridgeport	Lautard, Guy	TMBR#3:206
    Salability of models: Model stagecoach	Lautard, Guy	TMBR#3:207
    Salability of models: Model vise	Lautard, Guy	TMBR#3:206
    Salt and vinegar for oxide removal	Lautard, Guy	TMBR#1:46
    Salvaging a drill chuck	Lautard, Guy	TMBR#3:121
    Salvaging Drill Bits		HSM'86:M/A14
    Salvaging Thin Aluminum		HSM'85:J/F15
    Sand blasting Cabinet, A	JOHNS, MICHAEL	PiM-Apr.'96, 44
    Sandblasting equipment	Lautard, Guy	TMBR#3:130-138
    Sandblasting gun details	Lautard, Guy	TMBR#3:121,136
    Saving Some Pinched Fingers	WULFF, JAY E.	PiM-Apr.'96, 35
    Saw Blade Cutoff Tool, A	HUARD, CONRAD	HSM'93:J/F31
    Saw Table for the Sherline Lathe, A	SMITH, W. R.	HSM'98:S/O 28 
    Sawfeed	REYNOLDS, JIM	PiM Apr. '98 4
    Sawing a 1 thou slot	Lautard, Guy	TMBR#3:176
    Sawing a box open after glue-up	Lautard, Guy	TMBR#3:195-196
    Saws for marking work	Lautard, Guy	TMBR#3:240
    Schieglel vise lift	Lautard, Guy	TMBR#3:68
    ScotchBrite	Lautard, Guy	TMBR#2:108
    Scrap Iron Tapping Guide Prevents Making Screwy Threads	DEAN, JOHN	HSM'82:M/J12
    Scrape & Shape Parts 1-5	THOMAS, STEPHEN M.	HSM'97:N/D 26, HSM'98:J/F 35, M/A 41, M/J 35, J/A38
    Scraping 2 surfaces true to each other	Lautard, Guy	TMBR#2:14
    Screw Blueing Tools	JENNINGS	MEW#13,52
    Screw Clamps		HSM'91:M/J56
    Screw Cutting On The Toyo	WINKS	MEW#10,58
    Screw Heads and Screwdrivers	SCHULZINGER, JACOB	HSM'97: J/A 52
    Screw Thread Calculations Parts 2-4	HOFFMAN, EDWARD G.	HSM'84:J/F18,M/A20,M/J20
    Screw Thread Calculations	HOFFMAN, EDWARD G.	HSM'83:N/D26
    Screw thread data	Lautard, Guy	TMBR#1:201
    Screw Trouble (Chips & Sparks)	DUNCAN, DONALD	HSM'95:M/J18
    Screwcutting Threads		HSM'86:J/F20
    Screwcutting without a threading dial	Lautard, Guy	TMBR#3:112
    Screwcutting: Higby End	Lautard, Guy	TMBR#1:5, 20
    Screwdriver Blade Grinding Jig	PLANK, KIM E.	HSM'84:J/A35
    Screwy History	UNWIN	MEW#17,46
    Scribing block	Lautard, Guy	TMBR#1:97; TMBR#2:198
    Scroll Saw	HEDIN, R. S.	HSM'86:J/A23
    Scroll saws - Hegner, 5161, and shop made	Lautard, Guy	TMBR#3:241
    Sculpting with Plastics	MERCER, NORMAN J.	HSM'88:J/F16 
    Sealing a Bargain (Tips & Tricks)	KOLAR, GEORGE	PiM-Jun.'95 44
    Sears speed converter	Lautard, Guy	TMBR#3:184
    Sears speed converter	Lautard, Guy	TMBR#3:184
    Sears Tap and Die Sets		HSM'83:S/O9
    Seasonal wood shrinkage and swelling	Lautard, Guy	TMBR#3:195
    Seasoning with ice & hot water	Lautard, Guy	TMBR#2:17
    Second Lease on Life, A	LEUCK, ROBERT	PiM Apr.'97 27
    Second Life For Boot Liners	WHITE, GREG	HSM'92:N/D15
    Secret of Taper Pins, The	HAUSER, JAMES W.	MW Apr. 99, 45
    Seen At The Exhibition	HALL	MEW#16,40
    Selecting a Milling Machine	WASHBURN, ROBERT A.	HSM'84:S/O60
    Self holding taper sockets	JEEVES	MEW#26,23
    Self-centering faceplate	Lautard, Guy	TMBR#1:163
    Self-cleaning spindle nose thread modification	Lautard, Guy	TMBR#3:59
    Self-Contained Cutter Grinder, A		HSM'89:M/J44
    Self-holding & self-releasing tapers	Lautard, Guy	TMBR#2:92-93; HTIM:48
    Self-holding & self-releasing tapers	Lautard, Guy	TMBR#2:92-93; HTIM:48
    Sensitive Drilling Attachment	HEDIN, R S	HSM'82:J/A42
    Sensitivity of a tenths indicator	Lautard, Guy	TMBR#3:14
    Sentinel	DEHNICKE, DUANE	HSM'89:M/A20
    Serious Milling With the Lathe Parts 1-3	JOHNSON, D. E.	HSM'94:S/O20,N/D38, HSM'95:J/F 30
    Service flange, defined	Lautard, Guy	TMBR#1:33
    Servicing drill chucks	Lautard, Guy	TMBR#3:117
    Set Blocks	HOFFMAN, EDWARD G.	HSM'94:M/A48
    Set of Precision Balancing Ways, A	BARBOUR, J. O.	PiM-Jun.'96, 30
    Setting a lathe job to run eccentric: (6th point)	Lautard, Guy	TMBR#1:128
    Setting the Depth		HSM'86:N/D13
    Setting Tool Height		HSM'89:S/O15
    Setting Up a Home Foundry	GINGERY, DAVE	HSM'85:J/A46
    Setting Up a Machine Shop in a Walkdown Basement	MACFARLANE, BOB	PiM Aug. '98 26
    Setting Up in the Four-jaw	BUQUOI, MICHEL	HSM'92:M/J13
    Setting Up Shop	KOUHOUPT, RUDY	HSM'92:M/J47
    Setting Up Work in the Lathe	WILLOX, PETER J.	HSM'96:S/O 33
    Setting work flush with the top of your vise jaws	Lautard, Guy	TMBR#2:124
    Shackles & swivels	Lautard, Guy	TMBR#3:46-47
    Shadowgraph, A	BUTTERICK, RICHARD	PiM-Oct.'96, 9
    Shapes And Types Of Lathe Tool	LOADER	MEW#18,53
    Sharp Return Bends		PiM-Aug.'89,24
    Sharpen for Brass Cutting	BLACKBURN, CHARLIE	HSM'97:J/A 25
    Sharpen Your End Mills Parts 1, 2	KOUHOUPT, RUDY	HSM'90:S/O42
    Sharpening center punches	Lautard, Guy	TMBR#1:21
    Sharpening endmills -- slotdrills	SKINNER	MEW#25,30
    Sharpening Jig-Slot/End Mills	LONGWORTH	MEW#14,41
    Sharpening Lathe Tools	LOER, CHARLES H.	HSM'98:J/A 24
    Sharpening Milling Cutters	JOHNSON, WILLIAM A	HSM'83:M/A36
    Sharpening razors with magnetism	Lautard, Guy	TMBR#1:186
    Sharpening Small Drills	ROBINSON, TREVOR	HSM'87:N/D51
    Sharpening Tungsten Carbide Drills	NETZEL, WALT	HSM'96:J/A 50
    Sharpening tungsten carbide tools	Lautard, Guy	TMBR#1:147
    Sharpening Two-Lip End Mills	McLEAN, FRANK	HSM'84:J/F50
    Sharpening Wood Planer Blades	GRAY	MEW#17,45
    Sharpening		PiM-Aug.'88,24
    Sharpening"razors & other fined edged tools	Lautard, Guy	TMBR#2:117-122; TMBR#3:237
    ShearLoc finger knobs	Lautard, Guy	TMBR#1:198
    Sheet Metal Applications	WESTON, WARREN	HSM'82:J/F38
    Sheet metal forming rollers	JEEVES	MEW#31,24
    Sheetmetal Fabrication, Edges	LOESCHER, RICHARD J.	HSM'82:J/A15
    Sheetmetal Fabrication, Notches	LOESCHER, RICHARD J.	HSM'82:N/D19
    Sheetmetal Fabrication, Seams	LOESCHER, RICHARD J.	HSM'82:S/O14
    Sheetmetal Layout	LOESCHER, RICHARD J	HSM'83:J/F14,M/A18,M/J24,J/A20,S/O56,N/D58
    Shelf Brackets		HSM'83:S/O19
    Shell End Mill Arbor, A	McLEAN, FRANK A.	HSM'91:N/D51
    Shims for the Faceplate		HSM'87:J/F19
    Shims	SPARBER, R. G.	PiM-Oct.'96, 44
    Ships' wheels & oboes	Lautard, Guy	TMBR#3:214-21
    Shipyards and HSM 's	Lautard, Guy	TMBR#1:178
    Shoot a "Best" for the Least	EGBERT; ROBERT I..	MW Jun. 99, 34
    Shop Bench (Chips & Sparks)	JOLY, DAVID	HSM'95:S/O18
    Shop Bench	JOLY, DAVID	PiM-Jun.'95 22
    Shop Equipment for Fixture Building	MADISON, JAMES	PiM Aug.'97 34
    Shop Gadget Clears the Air	CROW, ART	HSM'88:S/O57
    Shop Hot-tank, A	HUTTINGER, RICHARD L.	PiM-Oct.'90,22
    Shop lamps	Lautard, Guy	TMBR#3:26
    Shop Layout Part 1	HOFFMAN, EDWARD G.	HSM'84:N/D64
    Shop made angle plates - how to machine	Lautard, Guy	TMBR#2:101
    Shop made electric dial indicators	Lautard, Guy	TMBR#3:79
    Shop made metal hinges	Lautard, Guy	TMBR#3:199
    Shop made nibbling cutters	Lautard, Guy	HTIM:37
    Shop made specialty hammers	Lautard, Guy	TMBR#2:149
    Shop Notes on Metals and Metal Identification	HUNT, CHARLES K	HSM'83:N/D29
    Shop of The Month	FUNK, J.C.	HSM'84:J/F20
    Shop of the Month	GODDARD, LARRY	HSM'87:M/J41
    Shop of the Month	HASKINS, D E	HSM'83:M/J16
    Shop of the Month	SHERWOOD, GORDON	HSM'82:S/O12
    Shop Rags		HSM'85:J/A17
    Shop-built Taper Attachment, A	PETTIT, GLENN	PiM-Apr.'94,16
    Shop-made Expanding Mandrel A	WASHBURN, ROBERT A.	PiM-Jun.'88,20
    Shop-made gage blocks	Lautard, Guy	TMBR#2:69
    Shoptask Modifications	SCHWEINFURTH, LUDWIG	PiM-Aug.'94,21
    Shortcuts to Making an Arbor	McLEAN, FRANK A	HSM'88:N/D46 
    Short-tailed Dog, A	LAMANCE, THOMAS	PiM-Oct.'92,3
    Shower Power		PiM-Feb.'90,18
    Shrink and Expansion Fits	DEVOR, DANIEL	HSM'86:M/A43
    Shrink the Bore	JOHNS, JACK	HSM'92:M/A14
    Shrinking a pressed-in bush to remove it	Lautard, Guy	TMBR#2:129
    SIC magazine	Lautard, Guy	TMBR#2:150; TMBR#3:78
    Sight Holding Fixtures	ACKER, STEVE	PiM-Dec.'96, 32
    Silver solder, soldering, etc. How to do it	Lautard, Guy	TMBR#1:59
    Silver Soldering Fundamentals		HSM'95:N/D48
    Silver soldering	Lautard, Guy	TMBR#1:103
    Silver steel = drill rod	Lautard, Guy	TMBR#2:116
    Simple Broach, A	RULE, J. F.	HSM'93:S/O15
    Simple Centering Gage	NORMAN, ROBERT	HSM'87:N/D52
    Simple Chucks to Protect Finished Pieces	PETERKA, W. PETE	HSM'83:J/A57
    Simple Dividing	Lautard, Guy	TMBR#1:40
    Simple Driver, A		PiM-Dec.'91,24
    Simple Estimating of Variable Motor Speeds	PLOTKlN, CHUCK	MW Jun. 99, 42
    Simple Formula		HSM'83:M/A12
    Simple graduating tool	BUCK	MEW#24,54
    Simple Grinder Water Pot, A	FELLER, ERNEST T.	HSM'92:J/A50
    Simple Indexing Attachment for Your Lathe, A	TITUS, DON	PiM Jun.'97 11
    Simple Indexing Rotary Table, A	HOFF, MICHAEL F., JR.	HSM'92:J/F32
    Simple Indicator Mount for a Lathe, A	ROBERTSON, JIM	MW Oct. 99, 15
    Simple lathe carriage index	Lautard, Guy	TMBR#1:68
    Simple Lathe Mill, A	FOSTER, CHARLIE	PiM-Apr.'96, 22
    Simple Oil Can	HALL	MEW#18,26
    Simple optical centre punch	HARTWELL	MEW#25,24
    Simple Phase Converter, A	ACKER, STEVE	HSM'91:J/F38
    Simple press tool	AMOS	MEW#28,64
    Simple Punch Guide, A	JOHNSON, WILLIAM R.	PiM Oct.'97 29
    Simple Rotary Table, A	WELLCOME, STEPHEN G.	PiM-Jun.'88,22
    Simple sheet metal bending devices	Lautard, Guy	HTIM:27; TMBR#2:110
    Simple steady	JEEVES	MEW#24,18
    Simple Stepper-motor Driver, A	HOOVER, C. A.	PiM Apr.'97 12
    Simple Surface Plate		HSM'85:S/O16
    Simple Tapping Guide, A	HUFFMAN, PHIL	HSM'95:N/D47
    Simple Timer, A	REICHART, BILL	HSM'94:M/A52
    Simple Tooling for Model Size Shoulder Bolts	GINGERY, DAVE	PiM-Feb.'90,21
    Simple Tooling for Model Size Shoulder Bolts	SILVA, FERD	PiM-Feb.'90,21
    Simple Truing Jig, A (Tips & Tricks)	LAMANCE, THOMAS	PiM-Jun.'95 42
    Simple Truing Jig, A	LAMANCE, THOMAS	PiM-Jun.'94,3
    Simple Way to Measure Inside Diameters, A	SPARBER, R. G.	PiM Apr.'97 32
    Simplest Phase Converter	GRIMES, THOMAS	HSM'97:M/J 25
    Sine of the Times	KLOTZ, MARVIN W. 	MW Feb. 99, 45
    Sine Plate	McKNIGIT, JAMES	MW Aug. 99, 40
    Single Beam Trammel, A	TORGERSON, DICK	PiM-Jun.'91,12
    Single lip cutters in place of commercial end mills	Lautard, Guy	HTIM:19
    Single Point Cutting	CLARKE, THEODORE M.	HSM'89:J/F53
    Single Point Threading		HSM'84:J/F16
    Single row deep groove ball bearings	Lautard, Guy	TMBR#2:32
    Single Thread Worm Drives	OLSON, JOHN	PiM-Aug.'90,21
    Single Thread Worm Drives	SINGER, NORMAN H.	PiM-Aug.'90,21
    Single Wheel Knurling Tool	TORGERSON, DICK	PiM-Apr.'91,10
    Single-phase to Three-phase Plus Speed Control	EYER, CHARLES	PiM Dec. '98 6
    Single-shot Pneumatic Hammer, A	CALVERT, ROBERT L.	PiM-Dec.'95 22
    Single-shot, Lever-action, Falling-block Rifle Action Parts 1-4	MUELLER, WALTER B.	HSM'94:M/J20,J/A26,S/O36,N/D45
    Single-shot, Lever-action, Falling-block Rifle Action Parts 5-8	MUELLER, WALTER B.	HSM'95:J/F44 M/A28 M/J46 J/A27
    Six Station Saddle Stop	VICKERY	MEW#10,31
    Six-cycle "Oddball" Engine Parts 1-5	DUCLOS, PHILIP	HSM'90:M/A20,M/J26,J/A36,S/O30,N/D38
    Skipping	SEXTON, TERRY	HSM'92:S/O46
    Sky Charger Part 1-6	WASHBURN, ROBERT A.	HSM'85:J/F24,M/A32,M/J36,J/A42,S/O27,N/D38
    Sky Charger Parts 7-11	WASHBURN, ROBERT A	HSM'86:J/F34,M/A28,M/J34,J/A33,S/O36
    Slide Duplicating & Macro Photographic Apparatus, A	PARK, RICHARD M.	HSM'89:J/F20
    Sliding Bandsaw Vise	MERRIFIELD, ED	HSM'84:M/A35
    Sliding Bevel Gage with Protractor, A	WRIGHT, TED	HSM'96:M/J31
    Sling swivel base for tubular magazine rifles	Lautard, Guy	TMBR#1:113
    Slitting Saw Carrier	HALL	MEW#11,64
    Slitting Saws	KOUHOUPT, RUDY	HSM'85:J/A56
    Slitting thin wall tubing	Lautard, Guy	TMBR#3:129
    Slot Anvil Depth Gage Mike	DUBOSKY, ED	PiM-Oct.'91,22
    Slot drills, What are they?	Lautard, Guy	TMBR#1:169; HTIM:4
    Slotting att for a mill/drill	JEEVES	MEW#29,26
    Slotting device for Myford S7	TWIST	MEW#30,62
    Slow Speed Drill Press Attachment, A	COLEMAN, ROBERT	HSM'86:M/J42
    Small Boring Head, A	HEDIN, R. S.	PiM-Jun.'90,4
    Small Chip Guard	LOADER	MEW#9,30
    Small commercial machine from Green Instrument Co.	Lautard, Guy	TMBR#2:25
    Small dividing head	TAYLOR	MEW#29,38
    Small Drill Sharpening Guides	MCLEAN, FRANK A.	HSM'95:J/A52
    Small Drill Sharpening Jig	UNWIN	MEW#9,14
    Small height gauge	JEEVES	MEW#24,31
    Small Hole Saws	HEDIN, R.S.	HSM'88:N/D36
    Small Item Organizer	BECK, B.	HSM'92:M/J13
    Small Keyways and Keyseats Parts 1, 2	KOUHOUPT, RUDY	HSM'86:J/A52,S/O57
    Small Machine Vise, A	McLEAN, FRANK	HSM'85:J/A49
    Small Quick-change Tool Post, A	FELLER, E T.	PiM-Dec.'89,15
    Small sheet aluminum packing pieces	Lautard, Guy	TMBR#1:167
    Small Sheet Metal Brake, A	WILSON, GLENN L.	PiM-Jun.'90,16
    Small Shop Butt Welder, A	HABICHER, WOLFGANG F.	HSM'96:M/A48
    Small shop-made hacksaw	Lautard, Guy	TMBR#2:101-102
    Small staking tool	JENNINGS	MEW#23,20
    Small stock storage scheme	Lautard, Guy	TMBR#3:73
    Small tap wrench	Lautard, Guy	TMBR#1:35
    Small tool & materials storage	POOLER	MEW#21,21
    Small Tool and Cutter Grinder, A	WILSON, GLENN L.	PiM-Apr.'91,4
    Small Tool and Cutter Grinder, A(Plans)	WILSON, GLENN L.	PiM-Oct.'91,4
    Small Tool Caddy		PiM-Oct.'88,3
    Small T-slot Nuts	WILLIAMS, JOHN D.	HSM'90:J/F59
    Small Vari-Speed Controller	MACHIN	MEW#14,26
    Smaller (watchmakers) collets	Lautard, Guy	TMBR#3:12
    Smallest "Hit R. Miss" Gas Engine?		HSM'90:J/F34
    Smooth Handles	EVERS, HOWARD	PiM-Apr.'96, 34
    Smooth Surfaces		HSM'84:M/J19
    Smoother Castings		HSM'86:J/F13
    Socket head cap screw dimensions	Lautard, Guy	TMBR#1:204
    Socket to 'em		HSM'83:J/A12
    Soft Aluminum Inserts	BARRETT, TOM	PiM-Apr.'94,MN
    Soft Bed, A		PiM-Feb.'88,24
    Soft Faced Hammer	BOWSER, BRUCE	PiM-Oct.'90,10
    Soft Jaws Hold Small Cylinders 	LEE, ARTHUR	MW Dec. 99, 47
    Soft Vise Jaws	MADISON, JAMES	HSM'90:J/A32
    Solder reveals temperature for a shrink fit	Lautard, Guy	TMBR#3:211
    Solder reveals temperature for removing bearings	Lautard, Guy	TMBR#3:211
    Soldering a steel ball for ball handles	Lautard, Guy	TMBR#3:173
    Soldering a steel ball onto a tapered shank	Lautard, Guy	TMBR#3:89
    Soldering aluminium	READ	MEW#29,66
    Solid cotters	Lautard, Guy	TMBR#1:96
    Solid wood edging in plywood	Lautard, Guy	TMBR#3:197-198
    Solving a Weighty Problem	DAVIDSON, BILL	HSM'85:S/O32
    Some Electric Motor Troubles	TURNER, G ALAN	HSM'86:N/D29
    Some Facts on Dial Indicators	SPOKOVICH, RON	HSM'86:M/A40
    Some flux removal tips	Lautard, Guy	TMBR#2:124
    Some handy small tools	Lautard, Guy	TMBR#2:101
    Some ideas on gun making	Lautard, Guy	TMBR#1:116; TMBR#3:167
    Some Light on the Subject	CROW, ART	HSM'85:M/J31
    Some milling vise accessory ideas	Lautard, Guy	TMBR#2:80
    Some more welding ideas	Lautard, Guy	TMBR#3:253
    Some notes on screwcutting	Lautard, Guy	TMBR#2:111-112; TMBR#3:112-113
    Some notes on taper turning	Lautard, Guy	TMBR#3:13-17
    Some notions on sharpening steel	Lautard, Guy	TMBR#1:117
    Some Parts Sources	HONEYWELL, DONALD G.	HSM'94:J/A56
    Some Pointers on Rotary Table Work	LAUTARD, GUY	HSM'85:J/A40
    Some Pointers on Scroll Sawing	LAUTARD, GUY	HSM'94:J/A34
    Sometimes Slower is Better	BARBOUR, J. O.	PiM-Jun.'94,24
    Source for a light oil and a way oil recipe	Lautard, Guy	TMBR#2:115
    Source of high quality cast iron for bullet molds	Lautard, Guy	TMBR#3:174
    Source of high quality cast iron for this project	Lautard, Guy	TMBR#1:91; TMBR#3:79
    Source of Machinery		HSM'87:J/F20
    Source of nitric acid	Lautard, Guy	TMBR#3:78
    Source of some project plans	Lautard, Guy	TMBR#1:197
    Sources of Cerrosafe		HSM'85:S/O16
    Sources of lapping supplies	Lautard, Guy	TMBR#3:65
    Space blocks	Lautard, Guy	TMBR#2:69
    Spacing Drill Guide Makes It Easy	DEAN, JOHN	HSM'84:M/A39
    Spacing Holes	HOFFMAN, EDWARD G.	HSM'83:M/A14,M/J18
    Spade drills	Lautard, Guy	TMBR#1:155
    Spanner Making The Easy Way	LANE	MEW#10,72
    Spare Parts		HSM'88:J/A13
    Spark Eroding a Broken Stud	LANGLOIS, ROBERT P.	HSM'95:M/J30
    Spark Testing		HSM'85:J/A18
    Special Driver		HSM'91:J/A13
    Special Milling Jig (Tips & Tricks)	HAAS, EDWARD T., JR.	PiM-Feb.'95 41
    Special Scoop, A	LAMANCE, THOMAS  	MW Aug. 99, 58
    Specialty Brush		PiM-Apr.'91,23
    Specialty Locating Devices Part 1	HOFFMAN, EDWARD G.	HSM'94:N/D60
    Speed Control Of AC Motors	HALL	MEW#17,68
    Speed Reducer		HSM'91:S/O14
    Speeding up work by not wasting time on needless precision	Lautard, Guy	TMBR#1:23
    Speeding up work by planning the job	Lautard, Guy	TMBR#1:23
    Speeds And Feeds Parts 1-3	HOFFMAN, EDWARD G.	HSM'84:J/A20,S/O20,N/D18
    Speeds and Feeds	YOUNG, BARRY	MW Oct. 99, 52
    Sphere Machining	JENKINS, LEWIS	PiM-Feb.'95 20
    Spindle Clamps for a Mill/drill	LIFSON, WILLIAM	PiM-Dec.'94,19
    Spindle Clamps for Imported Mill-drills	WATERS, RALPH T.	PiM-Aug.'96, 37
    Spindle Cleaner	LAMANCE, THOMAS	PiM-Jun.'93,3
    Spindle Driving Handle for Emco Super11 Lathe	PAULE, BOB	PiM-Jun.'90,15
    Spindle Lock for Your Milll/drill, A	LOWERY, BILL	HSM'93:M/A28 
    Spindle Lock	TORGERSON, DICK	PiM-Feb.'91,20
    Spindle Motor Reverse	RAYHEL, JAMES	PiM Feb. '98 31
    Spindle Nose Collet Chuck	PARK, WILLLEM B.	HSM'86:J/A20
    Spindle Oscillator for Sanding and Honing	MUELLER, FRAN O.	PiM Feb.'97 12
    Spindle Power for the Unimat	GALLAGHER, MARK	HSM'97:M/J 25 
    Spindle Stop for a 10-K	BENNETT, N. H.	HSM'85:M/A31
    Spindle Thread Protection		PiM-Jun.'92,3
    Spindle Thread Protection	LAMANCE, THOMAS	PiM-Jun.'92,3
    Spindle Work Stop, A	MARX, ALBERTO	HSM'87:M/A26
    Spindle-mounted Collet Attachment for 12" Atlas-type Lathes	JONES, BRUCE	PiM-Jun.'93,4
    Spindle-nose Collet		PiM-Apr.'91,24
    Spinning Your Own Oil Can	DUCLOS, PHILIP	PiM-Dec.'90,5
    Split Bronze Bearings		HSM'91:M/A14
    Split Bushings		HSM'86:S/O18
    Spoked handwheels	Lautard, Guy	TMBR#3:58
    Spot grinding & lapping - a visit with a retired gage maker	Lautard, Guy	TMBR#2:58
    Spring and Coil Winder, A	WILSON, GLENN L.	MW Oct. 99, 40
    Spring loaded C-clamp	Lautard, Guy	HTIM:6
    Spring making	Lautard, Guy	TMBR#1:29, 154; HTIM:23-26, 30; TMBR#3:90,
    Spring tool for screwcutting	Lautard, Guy	TMBR#2:111-112
    Spur Center for Turning Wood, A	McLEAN, FRANK A.	HSM'96:N/D59
    Square Collets	HEDIN, R. S.	PiM-Oct.'90,20
    Square drill rod	Lautard, Guy	TMBR#3:105
    Square Pegs and Round Holes	LUKENS, LUKE	HSM'85:M/J46
    Square References, their Design, Construction, and Inspection	REISDORF, GARY F.	HSM'85:M/J32
    Square Stock in the Universal Chuck		PiM-Apr.'89,3
    Square Stock		PiM-Dec.'91,24
    Square Tapping		HSM'91:J/A14
    Squaring the Circle	MARX, ALBERTO	PiM-Apr.'89,15
    Squaring the Circle	SMITH, TIM	PiM-Apr.'89,15
    Stable Propane Torch, A	WELLS NORM	HSM'94:J/F17
    Stainless Steel Fundamentals	GENEVRO, GEORGE	HSM'91:J/A28
    Stalking the Wily Chuck Key and Related Matters	LAUTARD, GUY	HSM'82:M/A34
    Starrett #118 spacing center punch	Lautard, Guy	TMBR#3:102
    Starrett #160 & #240 pin chucks	Lautard, Guy	TMBR#3:12
    Starrett hold-downs	Lautard, Guy	TMBR#2:80
    Starrett layout hammer	Lautard, Guy	TMBR#3:104
    Starrett lock joint calipers	Lautard, Guy	TMBR#3:106
    Starrett's big combination square	Lautard, Guy	TMBR#3:106
    Starters & Motors For MC Tools	BOUCHER	MEW#10,34
    Starting a local hsm club	Lautard, Guy	TMBR#1:6
    Starting a reamer into the work	Lautard, Guy	TMBR#1:16
    Starting taps square	Lautard, Guy	TMBR#3:172
    Starting the Die Squarely		HSM'87:J/A17
    Starting Turning Part 1 A Paperweight	MASON, AUDREY	HSM'92:M/A20
    Starting Turning Part 2 Decorative Boxes	MASON, AUDREY	HSM'92:M/J19
    Starting Turning Part 3 Lace Bobbins	MASON, AUDREY	HSM'92:J/A27
    Starting Turning Part 4 Two Candlesticks	MASON, AUDREY	HSM'92:N/D24
    Starting Turning Part 5	MASON, AUDREY	HSM'93:S/O30
    Starting Turning Part 6 Mini Screw Clamps	MASON, AUDREY	HSM'95:J/F22
    Stay-put Lathe Carriage Lock Wrench	GASCOYNE, JOHN B.	PiM-Aug.'91,24
    Steady Improvement	VAUGHAN, W.B.	PiM-Dec.'88,20
    Steady Rest, A		HSM'91:J/A14
    Steam Engine Parts 1-3	KOUHOUPT, RUDY	HSM'85:S/O58,N/D58, HSM'86:J/F58
    Steam/Air Engine for Fun, A	KEREKGYARTO, GEORGE	HSM'96:S/O48
    Steel Beam Trammel, A Parts 1, 2	LAUTARD, GUY	HSM'85:J/F46,M/A35
    Steel boxes	Lautard, Guy	TMBR#3:191
    Steel Heat And Crystals	MORRIS	MEW#14,22
    Step Collets	ROUBAL, WM. T., Ph.D.	HSM'82:M/A40
    Stepper motors	STUART	MEW#26,61
    Steve Makes a Mistake	ACKER, STEVE	HSM'92:J/F38
    Sticking the pattern on with Spray-Mount	Lautard, Guy	TMBR#3:240
    Sticktoitiveness		HSM'83:J/A13
    Stockholm tar smells right in the shop	Lautard, Guy	HTIM:48
    Stocking Stuffers	KOUHOUPT, RUDY	HSM'86:N/D45
    Stoning down a mill file for use in the lathe	Lautard, Guy	HTIM:45; TMBR#3:12
    Stoning reamers in the lathe	Lautard, Guy	TMBR#3:159
    Stopping Vibration		HSM'88:J/F12
    STP as way lube	Lautard, Guy	TMBR#3:172
    Strength of nails	Lautard, Guy	TMBR#3:48-51
    Stress relieving CRS	Lautard, Guy	TMBR#1:25
    Strike Three Against Home Offices?	BATTERSBY, MARK E.	HSM'93:J/A34
    Strike While the Iron is Hot (excerpt)	Lautard, Guy	TMBR#1:45
    Strokes with a shaper Parts 1-3	MORRIS	MEW#22,40;#24,58;#25,27
    Stronger Legs	WINKLER, ROBERT D.	PiM-Dec.'94,MN
    Stronger Scope Installation	ACKER, STEVE	MW Dec. 99, 40
    Stropping abrasive - making from grass charcoal	Lautard, Guy	TMBR#2:121
    Stuck Chucks, One-more-time, Didactic #17	KRATT, HENRY J.	HSM'96:J/A 49
    Studs and dowels	BURGESS	MEW#24,14
    Study Reference for Novice Machinists	EVANS, R. W.	HSM'86:J/A56
    Sub-faceplate	Lautard, Guy	TMBR#1:166
    Subreckys gadgets - tools you cant buy	Lautard, Guy	TMBR#2:127
    Substitute for dowel pins	Lautard, Guy	TMBR#2:103
    Substitute Tailstock Center	LaMANCE, THOMAS	HSM'96:M/A19
    Suggested mod to Myf Slotter	TWIST	MEW#32,25
    Supplement to the Home Shop Motor Controller	EYER, CHARLES	HSM'97:J/F 60
    Supplementary Tilting Milling Table, A	YAMAMOTO, MICHAEL T.	PiM-Aug.'88,17
    Support pad location for granite surface plates	Lautard, Guy	TMBR#3:224
    Surface Finishes	MADISON, JAMES	PiM-Apr.'93,14
    Surface gage desk lamp	Lautard, Guy	TMBR#3:205
    Surface Grinding On a Vertical Mill	KEET, AUBREY	PiM-Feb.'88,19
    Surface Grinding on the Drill Press	STARNES, RAY E.	HSM'90:M/A54
    Surface Plate Care	WELLS NORM	HSM'94:M/A16
    Surface tension in silver soldering centers bolt head	Lautard, Guy	TMBR#3:116
    Sustaining Tailstock Lubrication		PiM-Apr.'91,24
    Swaging Down a Copper Pipe Elbow	LAUTARD, GUY	HSM'84:N/D54
    Swaging hex sockets	Lautard, Guy	TMBR#2:95
    Swan necked turning toolholder	WATKINS	MEW#29,47
    Swarf Picker	NOBLE, BURT	PiM-Apr.'96, 44
    Swarf Protection		HSM'88:S/O12
    Swarf Trays for the Myford Series 7 Lathes	LAUTARD, GUY	HSM'82:S/O38
    Swashplate steam engine	Lautard, Guy	TMBR#1:198
    Swivel base for small vise	Lautard, Guy	TMBR#1:37
    Swivel Base	GOULD	MEW#18,46
    Symbols &Terms defined	Lautard, Guy	TMBR#1:1-2; TMBR#2:v; HTIM:ii; TMBR#3:2
    Table Covers and Tool Trays	KINDERMAN, ED	HSM'86:S/O41
    Table Fixtures and Applications	MADISON, JAMES	PiM-Dec.'93,14
    Table saw, Ryobi BT3000	Lautard, Guy	TMBR#3:186
    Table Square	MADISON, JAMES	HSM'91:M/J58
    Table Stop		PiM-Apr.'92,18
    Table Stop	MADISON, JAMES	HSM'96:J/A44
    Taig Lathe Tool Rest, A	McLEAN, FRANK A.	HSM'96:J/A54
    Tailstock Attachment	McLEAN, FRANK A.	HSM'93:M/A36
    Tailstock Attachments for the Lathe	McLEAN, FRANK A.	HSM'93:J/F46
    Tailstock barrel handwheel (idea only)	Lautard, Guy	TMBR#1:72
    Tailstock Die Holder	GENEVRO, GEORGE	PiM-Oct.'92,11
    Tailstock Die Holder	TIMM, HAROLD	HSM'85:M/J40 
    Tailstock Die Holder	WATKINS	MEW#9,26
    Tailstock for a small lathe	BOURNE	MEW#31,52
    Tailstock Tap and Die Holder, A	McHENRY, ROGER R.	PiM-Oct.'91,20
    Tailstock taper turning att	MAJOR	MEW#26,12
    Tailstock tapping device	MCKENZIE	MEW#21,16
    Tailstock Tip		PiM-Oct.'91,3
    Tailstock Troubles		PiM-Apr.'89,24
    Tailstock turret	JACKSON	MEW#28,59
    Taiwan Lathe Problems	HESSE, JIM	PiM Dec. '98 30
    Takang Model 1760G Lathe; Product Review	BENJAMIN, JOHN	HSM'96:J/A22
    Take a camera along	Lautard, Guy	TMBR#3:109
    Tale of a Jet GHB Gap Bed Lathe	TOOKE, PATRICK	HSM'99:M/A 54
    Tangential skiving tool	BENTLEY	MEW#27,51
    Tap and Clearance Drills	FORSLIND, STEPHEN R.	HSM'93:J/A18
    Tap breakage	Lautard, Guy	TMBR#3:172
    Tap Dogs	PETTIT, GLENN A.	HSM'94:S/O43
    Tap Drill Sizes		HSM'88:M/A39 
    Tap starting dodge	Lautard, Guy	TMBR#1:167; HTIM:28
    Tap Wrench Guide with Depth Gage	SPARBER, R. G.	PiM-Apr.'94,30
    Tap Wrenches from Scrap		HSM'89:J/A44
    Tape Tricks		HSM'86:J/A12
    Taper Cutting Checks and Setup		HSM'89:M/A13
    Taper Shank Turning Made Easy	JOHNSON, D. E.	PiM-Oct.'90,4
    Taper turning att -- Myford 254	CURSON	MEW#25,12
    Taper Turning Attachment	HALL	MEW#9,64
    Taper turning using gears	JEEVES	MEW#32,26
    Taper turning	Lautard, Guy	TMBR#2:90
    Taper Turning	VREELAND, DON H.	HSM'92:S/O47
    Tapered Arbor	JOHNS, JACK	HSM'92:S/O14
    Tapering Off		HSM'83:J/F16
    Tapers on Oblong Pieces	HAMILL, JAMES	PiM-Jun.'89,22
    Tapers Parts I, II	HOFFMAN EDWARD G	HSM'82:M/J15,J/A13
    Taplicator	LAMANCE, THOMAS	PiM-Feb.'92,3
    Tapper, A	BOLANTE, JAY	PiM-Dec.'96, 16
    Tapping a Channel-shaped Part	BAYLISS, LEROY C	HSM'97:J/F 22
    Tapping Aid		HSM'90:M/J14
    Tapping Block	SISSON, LANE	PiM-Feb.'91,10
    Tapping Fixture	MCQUEEN	MEW#10,70
    Tapping Guide for a Unimat,	A NESSEN, LEROY J.	HSM'90:J/A27
    Tapping lube for stainless steel	Lautard, Guy	TMBR#2:116
    Tapping of blind holes	Lautard, Guy	TMBR#3:76
    Tapping oversize when wanted	Lautard, Guy	TMBR#1:17
    Tapping Oversize	JOHNS, JACK	HSM'92:J/P 13
    Tapping plastic - coarse vs. fine threads	Lautard, Guy	TMBR#3:175
    Tapping Square	GRAY	MEW#13,26
    Tapping Station	PILESKI, MIKE	PiM Oct.'97 22
    Tapping Straight Holes		HSM'83:S/O18
    Tax-deductible Home Shop	BATTERSBY, MARK E.	HSM'90:M/A38
    Tee Slot Cutter	HALL	MEW#17,36
    Teeth for Rotary Cutting Tools	HEDIN, R. S.	HSM'91:M/A39
    Teflon on electrical cord plugs	Lautard, Guy	TMBR#1:25
    Telegraph Key Parts 1, 2	RIPKA, DOUG	HSM'98:J/F 42, M/A 36
    Telescoping Taper Attachment		HSM'89:M/A15
    Temperature benchmarks	Lautard, Guy	TMBR#1:200
    Temperature by appearance	Lautard, Guy	TMBR#1:200
    Temporary Self-locking Stub Mandrel	DUCLOS, PHILIP	HSM'84:J/A28
    Tenon Turning		PiM-Dec.'88,24
    Test Indicator	KOUHOUFT, RUDY	HSM'83:S/O54,N/D52
    Testing a square against a surface plate or straightedge	Lautard, Guy	TMBR#2:15
    Testing lifting and slinging gear	Lautard, Guy	TMBR#3:39
    Testing squares against a surface plate or straightedge	Lautard, Guy	TMBR#2:15
    Test-tube Stirling Engine, A	O'NEIL, DAVE	HSM'97:S/O 61
    Thar She Blows!		HSM'84:J/F16
    The $5.00 Taper Jig Revisited	OLSON, JOHN W.	HSM'88:M/J42 
    The Apprentice	WASHBURN, ROBERT A.	HSM'87:S/O50
    The Basic Approach to Using the Milling Machine	WASHBURN, ROBERT A.	HSM'84:N/D60
    The Bullseye Mixture	Lautard, Guy	TMBR#2:163
    The checking set square	Lautard, Guy	TMBR#2:11-14
    The clamp-on ball handle	Lautard, Guy	TMBR#1:80-85
    The clamp-on ball handle, as a lamp	Lautard, Guy	TMBR#3:205
    The Cole Drill	Lautard, Guy	TMBR#3:18
    The cross filing technique	Lautard, Guy	TMBR#2:123
    The Disappearing Drilling & Tapping Tool	Lautard, Guy	TMBR#3:172
    The Duo-Mite bender	Lautard, Guy	TMBR#3:54
    The Duo-Mite bender	Lautard, Guy	TMBR#3:54
    The Extremes of Space, Parts 1-2	DAVIDSON, BILL	HSM'87:S/O28,N/D46
    The Gear Head Engine Lathe, Part 1-3		HSM'89:M/A52,M/J52,J/A47
    The General Model 490 bandsaw	Lautard, Guy	TMBR#3:184
    The Grizzly 8 x 18" Lathe	SCHULTZ, GLENN M.	HSM'93:J/F39
    The Gunsmith Machinist: Aligning Scope Mounts	ACKER, STEVE	PiM-Apr.'95 40
    The Gunsmith Machinist: Barrel Bushing Jig, A	ACKER, STEVE	PiM-Aug.'95 32
    The Gunsmith Machinist: Barrel Vise, A	ACKER, STEVE	PiM Dec. '98 36
    The Gunsmith Machinist: Centering a Barrel Bore	ACKER, STEVE	PiM Apr. '98 34
    The Gunsmith Machinist: Chambering a Rifle Barrel	ACKER, STEVE	PiM Oct. '98 41
    The Gunsmith Machinist: Custom Bolt Handle	ACKER, STEVE	PiM-Dec.'95 36
    The Gunsmith Machinist: Cutting Rifle Barrel Threads	ACKER, STEVE	PiM Aug. '98 37
    The Gunsmith Machinist: Drilling and Tapping for Scope Mounts	ACKER, STEVE	PiM Feb. '98 28
    The Gunsmith Machinist: Gunsmith's Lathe Helper, A	ACKER, STEVE	PiM Oct.'97 34
    The Gunsmith Machinist: Installing a Front Sight	ACKER, STEVE	PiM Feb.'97 34
    The Gunsmith Machinist: Installing Sight Beads	ACKER, STEVE	PiM-Oct.'95 32
    The Gunsmith Machinist: Making Rifle Bedding Pillars	ACKER, STEVE	PiM Aug.'97 32
    The Gunsmith Machinist: Milling Grasping Grooves	ACKER, STEVE	PiM Dec. '97 29
    The Gunsmith Machinist: Moving a Firing Pin Hole	ACKER, STEVE	PiM Apr.'97 34
    The Gunsmith Machinist: Travel Measurement Plate, A	ACKER, STEVE	PiM-Jun.'95 36
    The Gunsmith Machinist: Trigger Job Pins	ACKER, STEVE	PiM Jun.'97 36
    The Haralson hose end	Lautard, Guy	TMBR#2:148
    The Installation of a ShopTronics Milling Machine DRO	WASHBURN, ROBERT A	HSM'86:M/J24
    the Jimmy Jig ( a table saw fence and more)	Lautard, Guy	TMBR#3:190
    The Little Torch	Lautard, Guy	TMBR#3:254
    The Machinex 5	WELLING, RICHARD	HSM'82:M/J33
    The Metalmaster lathe	Lautard, Guy	TMBR#2:68
    The Minton Milling Machine	FELLER, E.T.	HSM'88:M/A32
    the need for the Keeper	Lautard, Guy	TMBR#3:31
    The other guy's shop	MCQUEEN	MEW#31,40
    The other guy's w'shop	KRAN	MEW#31,41
    The Poor Man's Jig Borer, a combination angle plate and hole locator	Lautard, Guy	TMBR#2:21
    The Potts and Arrand milling spindles	Lautard, Guy	TMBR#2:39-40
    The Secret of the Old Master (fiction, by Lucian Cary)	Lautard, Guy	TMBR#1:104
    The Simple-Fyer	Lautard, Guy	TMBR#2:73
    The sine bar explained	Lautard, Guy	TMBR#2:75-78
    The Stirling Hot Air Engine	MAYES, THORN L	HSM'83:S/O33
    The Strokagenius File Rack	Lautard, Guy	HTIM:TMBR#1: TMBR#3:202
    The Surface Grinder, Parts 1-4	WASHBURN, ROBERT A.	HSM'87:N/D56, HSM'88:J/F51,M/A48,M/J52
    The Sweeper lathe tool grinder	SCOGGINS	MEW#28,12
    The Tesla turbine	Lautard, Guy	TMBR#2:150
    The Third Hand		HSM'88:N/D61
    The TINKER - an easy-to-build T&C Grinding Jig	Lautard, Guy	TMBR#1:103
    The ultimate box latch	Lautard, Guy	TMBR#1:125-129
    The Universal Plain Dividing Head, Parts 1-4	KUZMACK, RICH	HSM'97:M/A 41, M/J 37, J/A 48, S/O 50
    The Watchmaker's and Model Engineer's Lathe, Donald DeCarle		HSM'88:N/D14
    The Weaver launch engine	Lautard, Guy	TMBR#3:2 16
    The Woodpile	Lautard, Guy	TMBR#3:178-199
    There's a Bridgeport in my basement	Lautard, Guy	TMBR#2:155
    Thin piece vice accessory	CAMBRIDGE	MEW#24,70
    Thin Sheet Filing Fixture	WRIGHT, TED	HSM'99:M/A 48
    Thoughts on Selecting Vertical Mills Parts1, 2	HOWARD, THOMAS F.	HSM'93:J/A30,S/O26
    Thoughts on tool storage & toolboxes	Lautard, Guy	TMBR#1:122-124
    Thread and Screw Making	KWASNIEWSKI, GEORGE	HSM'83:J/A54
    Thread Chasing		HSM'88:M/J12
    Thread cutting att for Unimat3	FROST	MEW#22,13
    Thread Cutting on the Lathe	KOUHOUPT, RUDY	HSM'93:J/F18
    Thread Locking Products		HSM'91:J/F11
    Thread-cutting Aid, A	BROWN, KARL R.	HSM'92:N/D57
    Threaded Bushing	THOMPSON, JACK R.	HSM'93:S/O56
    Threaded Chucks	BENNETT, NORMAN	PiM-Apr.'96, 44
    Threading Calculations		PiM-Dec.'88,24
    Threading Copper Tubing	DIETEL, JAMES B	HSM'82:M/J17
    Threading Dial Indicator for the Lathe	PETERKA, W. PETE	HSM'86:M/J22
    Threading Oil Cup	McCORMAC, DON	HSM'82:M/J48
    Threading On a Lathe	STELLHORN, ROBERT	HSM'97:J/F 23 
    Threading on the Lathe	WASHBURN, ROBERT A.	HSM'84:J/A60
    Threading Set-up Chart		HSM'86:J/F39
    Threading the End of a Shaft	ARNOLD, GEORGE	PiM-Apr.'94,MN
    Three Ideas for a More Efficient Shop	VREELAND, DON	PiM-Aug.'94,26
    Three Modifications		HSM'89:M/A12
    Three Types of Unique Mill Table Clamps	WASHBURN, ROBERT A.	HSM'85:M/J55 
    Three way tailstock turret	HALL	MEW#22,33
    Three way tool post	LAMMAS	MEW#27,56
    Three-jaw Chuck Can Be Accurate, A	DOOLIN, THOMAS J.	HSM'97:J/F F 22
    Three-jaw Chuck Center, A	GRADY, ROBERT I,.	PiM-Apr.'96, 36
    Three-phase Idler Flywheel	HOUSEMAN, ROBIN	HSM'96:J/A 20
    Three-phase Motors from Single-phase Supplies	COX, V. J.	HSM'92:J/F12
    Throw away cutter holder	WALTERS	MEW#24,29
    Tidy Lathe Chuck Storage		PiM Oct.'97 3
    Tighten the Spindle Pulley	RACHUNAS, ART	HSM'96:S/O22
    Tightening a Jacobs chuck	Lautard, Guy	TMBR#2:38
    Tightening Metal Pins or Studs		HSM'87:J/A21
    Tilting table	FIGES	MEW#31,19
    Time and Labor Saver		PiM-Dec.'91,24
    Time for an Overhaul Parts 1-3	KOUHOUPT, RUDY	HSM'87:J/F54,M/A53,M/J46
    Time for Reflection, A	McLEAN, FRANK A.	HSM'96:S/O56
    Time Saver	LAMANCE, THOMAS	PiM-Jun.'92,3
    Timesaver Clampset	MADISON, JAMES	PiM-Dec.'94,26
    Time-saving Measure		PiM-Jun.'91,3
    Tiny Engines	KOUHOUPT, RUDY	HSM'92:N/D46
    Tip for machining copper	Lautard, Guy	TMBR#3:114
    Tip for making nice soldered joints in copper pipe	Lautard, Guy	TMBR#3:82
    Tip re using a ball end mill	Lautard, Guy	TMBR#1:76
    Tips & Tricks	BIDDLE, H. J.	PiM-Aug.'89,26
    Tips & Tricks	BIDDLE, H.	PiM-Jun.'90,3
    Tips & Tricks	BIRMINGHAM, CHARLES	PiM-Feb.'89,24
    Tips & Tricks	GARDING, R.	PiM-Jun.'90,24
    Tips & Tricks	GIBSON, ARCH	PiM-Aug.'90,24
    Tips & Tricks	LAMANCE, THOMAS	PiM-Apr.'90,3
    Tips & Tricks	LAMANCE, THOMAS	PiM-Feb.'90,3
    Tips & Tricks	LAMANCE, THOMAS	PiM-Jun.'90,24
    Tips & Tricks	LAMANCE, THOMAS	PiM-Oct.'90,3
    Tips & Tricks	LANDRY, VOLNEY	PiM-Jun.'90,3
    Tips & Tricks	SCHALLHORN, DAVID	PiM-Feb.'91,3
    Tips & Tricks	SCHUBERT, JAMES	PiM-Feb.'91,3
    Tips & Tricks	WELLS, NORM	PiM-Feb.'89,24
    Tips & Tricks	WELLS, NORM	PiM-Feb.'91,3
    To Magnify Without Glass		HSM'91:M/A14
    To the Point		HSM'86:N/D12
    Toggle Clamps		HSM'91:S/O55
    Toggle-link Operated Can Crusher	MARUSCHAK, JOHN	HSM'91:N/D41
    Tom Senior and the "Atlas" Special Parts 1, 2	MASON, HAROLD	HSM'86:N/D32, HSM'87:J/F40
    Tool and Cutter Grinder, A	BROOKS, DEREK	PiM-Jun.'96, 4
    Tool And Cutter Grinder, Parts l-2	BROOKS	MEW#16,60;#17,22
    Tool Bit Shims		HSM'89:J/F12
    Tool Bit Support	LAMANCE, THOMAS	PiM-Apr.'94,3
    Tool Block Carousel, A	PILESKI, MIKE	PiM Feb.'97 27
    Tool Block		HSM'87:N/D17
    Tool Bodies Parts 1,2	HOFFMAN, EDWARD G.	HSM'93:M/A48,M/J46
    Tool extension shank	Lautard, Guy	TMBR#2:103
    Tool for hand beading on sheet metal	Lautard, Guy	TMBR#1:148
    Tool for straight knurling	Lautard, Guy	TMBR#1:62-66
    Tool Height Indicator for the Lathe	NYMAN, PHIL	PiM-Jun.'96, 22
    Tool Holder Retainer	BIDDLE, H.T.	HSM'84:M/A55
    Tool Plate	VITKOVITS, STEPHEN, JR	HSM'88:M/J25 
    Tool Post Boring Bars, Part 1		HSM'89:N/D48
    Tool Post Grinder Parts 1-2	CORNELL	MEW#18,63;#19,64
    Tool Post Grinder, A	HANSON, WAYNE	PiM Apr. '98 32
    Tool Rests for Turning Wood	McLEAN, FRANK A.	HSM'97:J/F 48
    Tool stands	Lautard, Guy	TMBR#1:155
    Tool storage boxes	Lautard, Guy	TMBR#1:124
    Tool Tower	DUBOSKY, ED	PiM-Oct.'92,14
    Tool Tray		PiM-Dec.'89,24
    Tool Tray	KOLAR, GEORGE	HSM'93:M/J12
    Tool Tray	KOLAR, GEORGE	HSM'94:J/F17
    Toolholder for a Lathe        	SWITZER, GENE	HSM'99:M/A 27
    Toolholder to tilt toolbits to any desired helix angle	Lautard, Guy	TMBR#2:88
    Toolholder, A	CREWS, E. W.	PiM-Jun.'95 24
    Tooling for a Vertical Mill, Parts 1-3	KOUHOUPT, RUDY	HSM'88:N/D48;HSM'89:J/F50,M/A54
    Tooling for the Micro Machinist	SPROTT, JAMES	HSM'89:N/D54
    Tooling for Unimat-type Drilling/Milling Machines	CLARKE, THEODORE M.	HSM'86:N/D43
    Tool-Less Holddown Bolt	VAUGHN, W.B.	HSM'82:N/D52
    Toolmaker clamps & milling ops	HALL	MEW#25,67
    Toolmaker, Fay and Yankee calipers - which to buy?	Lautard, Guy	TMBR#3:106
    Toolmaker's buttons, making & using	Lautard, Guy	TMBR#2:70
    Toolmaker's clamps	Lautard, Guy	TMBR#1:149
    Toolmaker's Button	THOMSON, D. M.	HSM'93:S/O56
    Toolmakers' Buttons	JOHNSON, D. F..	PiM-Aug.'96, 13
    Toolmakers clamps	HALL	MEW#25,37
    Toolmaker's Clamps	LAUTARD, GUY	HSM'85:N/D40
    Toolmaker's Flat Vise, A	McLEAN, FRANK A	HSM'90:J/F52
    Toolmakers vice	HALL	MEW#28,42
    Toolmaking	Lautard, Guy	TMBR#3:3
    Toolpost Grinder, A	McLEAN, FRANK A.	HSM'91:M/J44
    Tools for cutting multi-start Acme threads	Lautard, Guy	TMBR#2:88
    Toothbrush makes a narrow brush	Lautard, Guy	TMBR#3:237
    Top Slide Improvements		HSM'87:N/D16
    Topics in Micromachining Parts 1-3	ROUBAL, TED	HSM'90:M/J22,J/A23,S/O38
    Topsy-turvy Engine Parts 1-5	DUCLOS, PHILIP	HSM'91:S/O20,N/D27, HSM'92:J/F24,M/A29,M/J32
    Torsion springs - aversion to	Lautard, Guy	TMBR#3:145
    Touch-up Brush		HSM'86:J/A12
    Tough Nut to Crack, A		PiM-Jun.'90,3
    Tough Tools for Tough Machining Operations Part 1	MADISON, JAMES	PiM Dec. '97 32
    Toughness of steel used in ball bearings	Lautard, Guy	TMBR#3:174
    Tourist Bar	HAUSER, JAMES	PiM Dec. '98 48
    Toxic dusts	Lautard, Guy	TMBR#3:204
    Transfer centerpunch (a good one vs. a cheap one)	Lautard, Guy	TMBR#3:105
    Transfer Screws		HSM'85:M/J14
    Transferring Hole Locations		PiM-Aug.'89,24
    Travel Measurement Plate, A		PiM-Jun.'95 36
    Tray for the Lathe		HSM'91:M/J10
    Treat Chips Carefully, Safety Tips	HOFFMAN EDWARD G	HSM'82:S/O21
    Trefolex paste cutting compound	Lautard, Guy	TMBR#2:116
    Trepanning Tool, A	McLEAN, FRANK A.	HSM'96:M/J58
    Triangular Tool Holder		PiM-Apr.'88,24
    Triangulation Layout		HSM'83:J/F14
    Trig - in high school vs. from Lautard	Lautard, Guy	TMBR#3:100
    Trigger pull weight	Lautard, Guy	TMBR#3:142
    Trigger tuning and shop made triggers	Lautard, Guy	TMBR#3:140-151
    Triggers, critical dimensions	Lautard, Guy	TMBR#3:143
    Triggers, torsion springs - aversion to	Lautard, Guy	TMBR#3:145
    Trigonometry	Lautard, Guy	TMBR#1:12-13; TMBR#2:72-78
    Triplex	SCHEFER, E. I.	HSM'84:S/O34
    Tripod Eliminator, The	MASON, HAROLD	PiM-Feb.'94,4
    Tripoli - washed/levigated tripoli, tripoli polish	Lautard, Guy	TMBR#2:121
    Triscamp .059 Parts 1-6	WASHBURN, ROBERT A	HSM'82:J/A18,S/O31,N/D43, HSM'83:J/F41,M/A47,M/J44
    Troubleshooting Primary Reasons for Scrap	GRADY, ROBERT	HSM'98:N/D 60
    Trueing Trick		HSM'84:M/J18
    Truing a Grinding Wheel	LAMANCE, THOMAS	PiM-Apr.'92,3
    Truing drill chucks	RAYSSIGIUR	MEW#27,41
    Truing the Column of a Mill-drill Machine	COOPER, JOHN A.	PiM-Aug.'93,26
    Truing up a straightedge	Lautard, Guy	TMBR#2:12
    Truing up an out-of-truth machinist's square	Lautard, Guy	TMBR#2:10
    T-slotted plate for workholding	Lautard, Guy	TMBR#1:39
    Tune in for a Touchdown (electric zeroing)	SPARBER, R. G.	PiM-Apr.'96, 42
    Turkshead handles for a box	Lautard, Guy	HTIM:31
    Turn a Shaft Without a Center Hole		PiM-Feb.'89,24
    Turn a Shaft Without a Center Hole		PiM-Feb.'93,3
    Turn Scrap Into Workstands	CROSBY, DAVID F.	PiM-Feb.'96, 32
    Turner's cube	Lautard, Guy	TMBR#3:219
    Turning A Ball Handle	HALL	MEW#12,24
    Turning a long, slender screw	Lautard, Guy	TMBR#1:140
    Turning a Morse Taper	KOUHOUPT, RUDY	HSM'92:M/A42
    Turning a straight taper on a wood lathe	Lautard, Guy	TMBR#3:205
    Turning Hardened Steels	RAYSSIGIUR	MEW#13,12
    Turning Long Tapers Using a Boring Head	JOHNSON, D. F..	PiM-Apr.'96, 16
    Turning Ornamental Shapes	MILSTER, CONRAD	HSM'85:M/A42 
    Turning Short Tapers on a Mill	THOMAS, STEPHEN	HSM'92:J/F18 
    Turning Short Tapers on a Mill/drill	THOMAS, STEPHEN M.	HSM'94:M/A41
    Turning Small Beads and Coves	LAMANCE, THOMAS	PiM-Aug.'92,3
    Turning small electric motor armatures	Lautard, Guy	TMBR#3:208
    Turning Square Stock Round	REICHART, J. W. "BILL"	PiM-Oct.'93,31
    Turning Tapers in the Lathe	REYNOLDS, JIM	PiM-Oct.'96, 28
    Turning the OD of thin sheet material on a lathe	Lautard, Guy	TMBR#2:130
    Turning Tip, A		PiM-Apr.'91,24
    Turning Your Vise Into a Universal Workholding System, Parts 1-7	HOFFMAN, EDWARD C	HSM'97:N/D 60, HSM'98:J/F 64, M/A 62, M/J 60, J/A 63, S/O 62, N/D 62
    Turn-O-Mill	MILLER, RALPH B.	PiM-Oct.'95 16
    Twiddle Stick	JENNINGS	MEW#15,55
    Twin Lock Workholding System	HOFFMAN, EDWARD G.	HSM'91:M/J10
    Twin-beam Trammel, A	MARX, ALBERTO	HSM'86:M/A27
    Two Accessories for the Atlas 12" Lathe	ERNEST, JOHN F.	HSM'88:M/J28
    Two approaches to "C' spanners	NOAKES	MEW#28,41
    Two approaches to 'C" spanners	WALTERS	MEW#28,41
    Two Designs for Welding Tables	WALKER, RICHARD B.	PiM-Dec.'88,17
    Two DROs Under $125 Per Axis	MARTIN, GENE	PiM-Aug.'93,17
    Two Handy Jigs	DUBOSKY, ED	PiM-Apr.'89,4
    Two jaw chuck	FIGES	MEW#32,60
    Two Machine Tool Stands	LAUTARD, GUY	HSM'83:J/F35
    Two Machining Aids	CAMPBELL, JOHN I.	HSM'83:J/A22
    Two muzzle loaders	Lautard, Guy	TMBR#3:6
    Two nice die filing machines	Lautard, Guy	TMBR#3:259
    Two Small Presses	METZE, ROBERT	PiM-Dec.'94,12
    Two Steps to Center	HOLTHAM, JON H.	HSM'89:M/A38
    Two Tools for Shop Angle Measurements	PETERSON, DON	PiM Oct. '98 38
    Two Useful Charts	BROWN, KARL R.	MW Feb. 99, 36
    Two Useful Lathe Dogs	KOUHOUPT, RUDY	HSM'91:S/O48
    Two Useful Milling Accessories	KOUHOUPT, RUDY	HSM'91:M/J48
    Two ways to pull a fast one	TAYLOR	MEW#27,40
    Two Workshop Hints		HSM'87:S/O15
    Two-bit Tool, A	LAMANCE, THOMAS	PiM-Feb.'92,3
    Two-cylinder Oscillating Steam Engine	HEDIN, R. S.	PiM-Dec.'90,6
    Two-headed Bolt with Nut	FEAR, JERRY J.	PiM-Dec.'91,21
    Two-jaw Lathe Chuck, A	SCHULZINGER, JACOB	PiM-Feb.'94,15
    Two-Speed Belt Transmission	BUTZ, JACK	HSM'98:N/D 48
    Two-Sphere Gage	CLARKE, THEODORE M.	HSM'88:M/J26
    Type of grinding wheels to use for spot grinding	Lautard, Guy	TMBR#2:65
    Ultra Precision Parallel Set	HAUSER, JAMES W.	HSM'98:J/F 24 
    Understanding Abrasives Parts 1,2	GENEVRO, GEORGE	HSM'99:M/A 50 M/J 52
    Uneven spacing of reamer flutes	Lautard, Guy	TMBR#3:158
    Uniform Conical Chamfer		PiM-Dec.'88,24
    Unimat 3 Top Slide	SCOGGINS	MEW#16,15
    Unimat Headstock Adapter	HUARD, CONRAD A	HSM'94:J/F38
    Universal and Reusable Table Fixtures		PiM-Jun.'92,29
    Universal Belt Tensioner, A	JOHNSON, D. E.	PiM-Apr.'91,18
    Universal Cross Drilling Fixture, A	JOHNSON, D. E.	PiM-Apr.'92,4
    Universal Drill Press Hold-down	STRAIGHT, J. W.	PiM-Apr.'94,24
    Universal Jig/Machine Vice	JENNINGS	MEW#16,20
    Universal Lamp, The	REICHART, J. R. "BILL"	PiM Aug. '98 16
    Universal Milling Attachment	LONGWORTH	MEW#13,56
    Universal milling dividing att	CORNELL	MEW#26,41
    Universal Surface Gage	McLEAN, FRANK	HSM'85:M/J48
    Unorthodox Mill/Lathe Grinder	DUCLOS, PHILIP	PiM-Jun.'88,15
    Unorthodox Spur Gear, An	HOFF, MICHAEL	PiM Apr.'97 24
    Untapped Source for Cast Iron Stock, An	KOPF, JOHN	PiM-Aug.'88,3
    Unusual Lathe Dog, An	MCLEAN, FRANK A.	HSM'92:M/J50
    Unusual Lathe Work		HSM'83:N/D40
    Unusual Power Drive, An (Tips & Tricks)	METZE, ROBERT W.	PiM-Dec.'95 40
    Unusual tee nuts	HALL	MEW#23,49
    Unusual Turning Operation, An	McLEAN, FRANK A.	HSM'94:M/A46
    Update and Improvements for the Craftsman 109 Series Lathe	WEIGHTMAN, LIONEL	PiM Feb. '98 18
    Updating Flat Belt Driven Equipment	OSLISLO, JAMES E.	HSM'86:J/F40
    Upgrading to Variable Speed DC	ACKER, STEVE	HSM'99:J/A 43
    Usage for Gearing	WASHBURN, ROBERT A	HSM'86:N/D55
    Use of a "roller' in chucking a rough cube	Lautard, Guy	TMBR#3:219
    Use of a chucking stub	Lautard, Guy	TMBR#2:6
    Use of Dimensions	KOUHOUPT, RUDY	HSM'85:M/J58
    Use of ultra-fine wet/dry paper for sharpening	Lautard, Guy	TMBR#2:124; TMBR#3:201
    Use Your Hands		HSM'84:S/O15
    Used as a fixturing aid	Lautard, Guy	TMBR#1:33
    Useful aid to holding slippery shapes in mill vise	Lautard, Guy	HTIM:38
    Useful Follower Rest, A	HOLM, PAUL	HSM'91:M/A28
    Useful modifications to hermaphrodite calipers	Lautard, Guy	TMBR#1:83
    Useful, High-quality Magnifying Glass, A	LAUTARD, GUY	HSM'97:N/D 55
    Uses for Emco3 mill/drill head	WALTERS	MEW#27,62
    Uses for fiberglass typewriter erasers	Lautard, Guy	TMBR#3:211
    Using "thin set" concrete to level a lathe stand	Lautard, Guy	TMBR#3:216
    Using A Bench Press, Parts 1-3	HALL	MEW#19,46;#20,37;#21,63
    Using a busted HSS tap as a scriber tip	Lautard, Guy	TMBR#2:104
    Using a combination square to lay out an angle	Lautard, Guy	TMBR#3:99
    Using a Computer to Draw Scales	INSTONE, JAMES R.	HSM'98:S/O 56
    Using a Cutoff Tool	KOUHOUPT, RUDY	HSM'93:S/O46
    Using a master square	Lautard, Guy	TMBR#2:16
    Using a phonograph needle as a scriber	Lautard, Guy	TMBR#1:100
    Using a Router on the Vertical Milling Machine	McLEAN, FRANK A.	HSM'94:J/F49
    Using a surface gage to test for squareness	Lautard, Guy	HTIM:35
    Using A Surplus Motor	RIX	MEW#20,64
    Using a Vertical Bandsaw, Parts 1-3	WASHBURN, ROBERT A	HSM'88:J/A44,S/O46,N/D43
    Using a washer to true up a rough turned ball	Lautard, Guy	TMBR#2:109
    Using Aluminum Foil		HSM'86:N/D13
    Using an automatic c/p as a small impact hammer	Lautard, Guy	TMBR#3:20
    Using Brass Shim Stock		PiM-Aug.'89,26
    Using Carbide Turning Tools	ESTY, F. B.	HSM'89:M/J57
    Using Chisels and Punches	HOFFMAN, EDWARD G.	HSM'87:J/A64
    Using Hand Hacksaws	HOFFMAN, EDWARD G.	HSM'87:N/D68
    Using Stub Mandrels	HALL	MEW#14,48
    Using the Diamond Toolholder	KOUHOUPT, RUDY	HSM'96:M/J24
    Using the Four-jaw Chuck	LINCOLN, W. A. ("LINK")	PiM-Jun.'96, 26
    Using the Milling Machine as a Copy Stand	BAKER, FOREST N.	PiM Dec. '98 24
    Using the Needle Point Shaft in a Wiggler Set	BAYLISS, LEROY C.	HSM'98:M/J 22
    Using the Wiggler and Edge Finder	WASHBURN, ROBERT A.	HSM'85:M/A58 
    Using triangular scrapers	Lautard, Guy	TMBR#1:196
    Using Unimat SL Chucks and Collets	ROUBAL, WILLIAM T (TED)	HSM'86:S/O34
    Using Wrenches and Screwdrivers	HOFFMAN, EDWARD G.	HSM'87:S/O64
    V Stage for the Home Constructor, An	BUTTERICK, RICHARD	PiM Aug.'97 14
    Vacuum Up Those Chips!	DOUGHERTY, WALT	HSM'93:M/J36
    Value of Wood in the Metal Shop, The		HSM'86:M/A15
    Valve Stem Remover	GOLEMBIEWSKI, LOUIS	HSM'93:J/A18
    Vanishing oil for machining plexiglas	Lautard, Guy	TMBR#3:66
    Varathane finish	Lautard, Guy	TMBR#3:190
    Variable Frequency Drive Applications	O'BRIAN, R. W.	PiM Dec. '98 26
    Variable Speed DC Motor for the Home Shop	EYER, CHARLES	HSM'96:M/J50
    Variations on a "Whatzit" engine	HOLLENBECK, KEN	HSM'96:N/D48
    Variations on a Button V-block	WAGNER, WILLL&M S.	PiM-Apr.'90,24
    Various tapping kinks	Lautard, Guy	TMBR#1:18
    Varsol - what is it?	Lautard, Guy	TMBR#3:168
    Varsol as a cutting fluid for aluminum	Lautard, Guy	HTIM:14
    V-belt length calculations	Lautard, Guy	TMBR#1:199
    V-belt speeds/pulley sizes	Lautard, Guy	TMBR#1:199
    V-Blocks in a Vise	MADISON, JAMES	PiM-Aug.'94,28
    V-Blocks Quickly Made	DEAN, JOHN	HSM'84:M/A43
    Vee-Grooved Snap Jaws		HSM'92:M/A11
    Vernier conversion	LOADER	MEW#25,32
    Vernier Dividing Head, A	MARX, ALBERTO	PiM-Feb.'88,16
    Vernier Division	Lautard, Guy	TMBR#2:7
    Vernier Division	Lautard, Guy	TMBR#2:7
    Vernier Height Gage	JENKINS, LEWIS J.	HSM'86:S/O25
    Vernier Protractor		HSM'92:S/O12
    Versatile Bubble Protractor, A	WILSON, GLENN L.	PiM-Feb.'94,18
    Versatile Coolant/Lubricant		HSM'91:J/A13
    Versatile Fastener	WOOD, GRANT W.	HSM'83:S/O26
    Vertical belt grinder	LEAFE	MEW#25,61
    Vertical Discharge: Everybody Needs VD	HESSE, JAMES	HSM'99:M/J 59
    Vertical Drive Dog		PiM-Feb.'88,24
    Vertical Shaping Facility	MOOR	MEW#14,51
    Vertical Toggle Clamps	HALL	MEW#9,33
    Very fine wet-dry paper for sharpening things	Lautard, Guy	TMBR#3:201
    Very fine wet-dry paper	Lautard, Guy	TMBR#2:124;
    Very Handy One-inch Height Gage, A	KUBOWSKY, HERMAN	PiM-Dec.'93,16
    V-grooved faceplate	Lautard, Guy	TMBR#1:169
    Vibrating Tap-buster Head, A	HESSE, JIM	PiM-Oct.'96, 30
    Vice Positioning Device	HALL	MEW#10,24
    Victorian" Engine, A, Part 1-4	DUCLOS, PHILIP	HSM'97:M/J 28, J/A 42, S/O 31, N/D 40
    Video Review Examining a Used Lathe and Mill	McKINLEY, CLOVER	HSM'99:J/F 27
    Video Review Fender Arches Videotape	LAUTARD, GUY	HSM'99:N/D 24
    Video Review: "Graver Making & Hand Turning for Clockmakers & Modelmakers"	LAUTARD, GUY	HSM'97:N/D 22
    Video Review: "Wheel Cutting, Pinion Making Depthing"	LAUTARD, GUY	HSM'97:M/J 22
    Video Review: 1998 NAMES. Exhibition	RICE, JOE	HSM'98:N/D 65 
    Video Review: A Video Visit with Guy Lautard & Bill Fenton	McKINLEY, CLOVER	HSM'94:M/J13
    Video Review: American's View of the English Wheel, An	LAUTARD, GUY	HSM'96:M/J 20
    Video Review: Basic Metal Lathe Operation, Part II	LAUTARD, GUY	HSM'93:S/O 16
    Video Review: Bedding, Scoping, and Crowning the Remington 700	LAUTARD, GUY	HSM'96:M/J 20
    Video Review: Correcting Bolt Lug Engagement and Excess Headspace	LAUTARD, GUY	HSM'96:M/J 20
    Video Review: Edge those Panels	LAUTARD, GUY	HSM'96:M/J 20
    Video Review: Fourth Annual NAMES Exposition	McKINLEY, CLOVER	HSM'94:S/O18
    Video Review: Greensand Casting Techniques	RICE, JOE	HSM'91:S/O47
    Video Review: Greensand Casting Techniques-Volume 2	RICE, JOE	HSM'93:S/O17
    Video Review: The 1893 Springfield Duryea	RICE, JOE	HSM'94:J/A56
    View Camera, A	HOLEN, D. W.	HSM'87:N/D22
    Vise - simple, small	Lautard, Guy	TMBR#2:86
    Vise alignment on milling machine	Lautard, Guy	TMBR#1:138
    Vise for Small Parts, A	DUBOSKY, ED	HSM'87:J/A42
    Vise Jaw Fixtures Parts 1-3	HOFFMAN, EDWARD G	HSM'92:S/O56,N/D54, HSM'93:J/F52
    Vise Sine Bar, A	GEIB, RANDALL R.	HSM'92:J/A13
    Vise-Clamp		PiM-Aug.'88,24
    Visible Chuck Wrench		PiM-Feb.'91,3
    VW engine conversion to aircraft use	Lautard, Guy	TMBR#3:56
    Wafer head screws	Lautard, Guy	HTIM:32
    Walking Staff, The	TITUS, DON	HSM'96:S/O43
    Wanting lots of #2 MT shanks	Lautard, Guy	TMBR#3:13
    Warnings re cadmium	Lautard, Guy	TMBR#2:116
    Warnings re cyanoacrylate glue	Lautard, Guy	TMBR#2:116
    Warpage in heat treating	Lautard, Guy	TMBR#1:53
    Washers		HSM'90:N/D15
    Watch Repair in the Home Machine Shop	ROUBAL, TED	HSM'87:M/J37
    Water of Ayr stone	Lautard, Guy	TMBR#2:118; TMBR#3:237
    Water-cooling Torches	JULIAN, BILL	HSM'97:S/O 22
    Wax/Stockholm tar resist	Lautard, Guy	TMBR#3:247
    Wax/Stockholm tar resist	Lautard, Guy	TMBR#3:247
    Way Lube		HSM'86:M/J14
    Ways and Means With Old Milling Machines	SEXTON, TERRY	PiM-Aug.'96, 4
    We visit -- Alan Cambridge	HALL	MEW#20,28
    We visit -- Chester UK Ltd	SHEPPARD	MEW#29,59
    We visit -- Don Hedger	HALL	MEW#23,34
    We visit -- Geoff Walker's W-Shop	HALL	MEW#17,56
    We visit -- Gordon Barber	HALL	MEW#21,31
    We visit -- Guy Keen's Workshop	HALL	MEW#25,35
    We visit -- Simon Trendall	HALL	MEW#27,34
    Webber gage blocks	Lautard, Guy	TMBR#2:81-82
    Wedge Clamps		HSM'91:J/A54
    Welded steel corner caps	Lautard, Guy	TMBR#3:256
    Welding Alternatives for the Machinist	HUNT, CHARLES K	HSM'82:M/J46
    Welding Cast Iron Parts I, II	HUNT, CHARLES K	HSM'82:S/O24,N/D22
    Welding Experience Afloat		HSM'83:M/A12
    Welding Light Sheet Metal		PiM-Feb.'89,24
    Welding Light Sheet Metal	LAMANCE, THOMAS	PiM-Apr.'93,3
    Welding of Tool and Die Steels	HUNT, CHARLES K	HSM'83:S/O28
    Welding rod for aluminum	Lautard, Guy	TMBR#2:122
    Welding Rod Organizer		HSM'85:N/D12
    Welding rod	Lautard, Guy	TMBR#1:6
    Welding Table, A		HSM'90:N/D13
    Welding Tip, A	ACKER, STEVE	PiM-Aug.'93,31
    Welding Up a Meat Smoker	ACKER, STEVE	HSM'99:J/F 54
    Weldments Can Replace Castings		HSM'84:J/F31
    Well Covered	HAMILTON, BONI	PiM-Aug.'94,MN
    What to do if you get a steel chip in your eye	Lautard, Guy	TMBR#1:132
    Wheel dressing jig	CURTIS	MEW#27,12
    Wheel Engine From Scrap	LEMARCHANT	MEW#12,23
    Wheel You Can't Live Without, The	MUELLER, WALTER B.	HSM'97:J/F 58
    When You Are Without a Tool Post Grinder (Chips & Sparks)	GODEKE, CHAD	HSM'95:M/A21 S/O20
    Where not to use a sine plate	Lautard, Guy	TMBR#2:79
    Where to buy Silver solder, solder	Lautard, Guy	TMBR#1:59
    Where you might get a drafting machine cheap	Lautard, Guy	TMBR#2:133
    Why a Layout? Part 3	MADISON, JAMES	PiM Feb.'97 30
    Why a Layout? Parts 1-2	MADISON, JAMES	PiM-Oct.,'96, 35, Dec.'96, 34
    Why an uneven number of spokes?	Lautard, Guy	TMBR#3:39
    Why Bubbles in levels get long or short	Lautard, Guy	TMBR#3:106
    Why is your lathe tailstock high?	Lautard, Guy	TMBR#3:217
    Why own several hacksaws?	Lautard, Guy	TMBR#2:100
    Why the ball on a surface gage spindle?	Lautard, Guy	TMBR#2:131
    Why the mirror in a Gerstner toolbox?	Lautard, Guy	TMBR#1:130-132
    Wiggler Bar and Test Bar	HOFFMAN, EDWARD G.	HSM'86:S/O26
    Winding a Coil For a Magnetic Chuck	HESSE, JAMES	PiM-Dec.'94,22
    Winding small springs	HARRIES	MEW#27,14
    Wing Divider	GINGERY, DAVE	PiM-Dec.'89,12
    Wire bending jigs	Lautard, Guy	TMBR#3:53
    Wire Clamps	JOHNSON, WILLLAM A.	PiM-Dec.'90,3
    Wire Clamps	WILSON, GLENN L.	PiM-Dec.'90,3
    Wire edge on cutting edges removed w/ a copper coin	Lautard, Guy	TMBR#3:157
    Wiring for correct polarity	Lautard, Guy	TMBR#3:57
    Wiring the lamp	Lautard, Guy	TMBR#3:31-32
    Wisdom in Technique Saves Time and Money	MADISON, JAMES	PiM-Feb.'96, 36
    With homebuilt aircraft people	Lautard, Guy	TMBR#3:56
    with Unimat lathes - repairing valves & spray nozzles	Lautard, Guy	TMBR#3:208
    Wobbler for making centerpunch marks run true	Lautard, Guy	TMBR#1:22
    Wood Carving Machine, A	SNYDER, JOHN W.	HSM'92:J/A34
    Wood finishing	Lautard, Guy	TMBR#3:198
    Wood Planer	GOULD	MEW#17,27
    Wooden Chuck		PiM-Apr.'91,23
    Wooden Mats	HAUSER, JAMES W.	MW Feb. 99,41
    Wooden tool storage boxes	Lautard, Guy	TMBR#3:191-199, 215
    Wooden Work Support in the Mill, A	ACKER, STEVE	HSM'98:J/A 58
    Woodturning on a metal lathe	Lautard, Guy	TMBR#1:174
    Woodworking in the Machine Shop	ERNEST, JOHN F.	HSM'97:M/A 54 
    Word for LPiM Oct. '98ite, A	KLASNA, JON	PiM Oct. '98 44
    Work Holding in the Band Saw	CRAIK, G. V.	PiM-Jun.'94,MN
    Work Holding	MULHOLLAND, GERARD	PiM-Jun.'94,MN
    Work on Your Faceplate	LAMANCE, THOMAS	PiM-Apr.'92,3
    Work With Morse Tapers	ROSEN, BERNARD L.	PiM Apr. '98 37
    Workbenches etc.	Lautard, Guy	TMBR#1:133-135; TMBR#3:178-183
    Workholder Alternatives Parts 1-3	HOFFMAN, EDWARD C.	HSM'99:J/A 58 S/O 41N/D  63
    Workholder Design Tips Part 1	HOFFMAN, EDWARD G.	HSM'94:M/J56,J/A51,S/O54
    Workholding in an Asian Mill-drill	WRIGHT, RICHARD	PiM-Dec.'96, 11
    Working in the Dark	DOLLNIG, WERNER W.	HSM'96:J/A 67
    Workings of a Sine Bar, The Parts 1, 2	WASHBURN, ROBERT A.	HSM'85:N/D54;HSM'86:J/F49
    Workmanship	Lautard, Guy	TMBR#1:4-5
    Workshop Basics For Beginners	PARKE	MEW#18,14
    Workshop Equipment On A Budget	DAVIS	MEW#14,58
    Workshop Geometry	HALL	MEW#11,13
    Workshop Mathematics	HALL	MEW#10,44
    Workshop security	SHEPPARD	MEW#31,42
    Workshop Visit	HALL	MEW#11,41
    Workshop Visit-Albert Wallis	HALL	MEW#15,32
    Workshop Visit-Harold Newman	HALL	MEW#18,49
    Worlds smallest lathe, and notes re some other miniatures	Lautard, Guy	TMBR#2:145
    Worm Drives Revisited	MATHESON, VIRGIL	PiM-Apr.'91,3
    Worshipful Co Of Turners Award	HALL	MEW#17,21
    X and Y Scales for the Mill	WILSON, GLENN L.	PiM-Apr.'92,10
    X and Y Stops for the Mill	KOUHOUPT, RUDY	HSM'93:J/F 49
    X, Y Stage for the Home Constructor, An		PiM Aug.'97 14
    Yortek Award	EDITORIAL	MEW#20,56
    You Can Do It	SCHONHER, SPENCER	HSM'97:M/A 40
    You Can Find It	BATORY, DANA MARTIN	HSM'97:J/F 56
    You Need A Rest!	DEAN, JOHN	HSM'83:J/A58
    Zap an Import-Build It Yourself	BARBOUR, J. O., JR.	PiM Apr.'97 30 
    Z-axis Downfeed for a Mill-drill Machine	MUELLER, FRAN O.	PiM-Feb.'91,12
    Zero Set Micrometer Dial	GROSJEAN, W. C.	PiM-Jun.'90,7
    Zinc Aluminum Alloy Sleeve Bearings for a Dividing head Upgrade	CLARKE, THEODORE M	HSM'99:S/O  60
    ''')
    mi_key = (
        "HSM    Home Shop Machinist",
        "HTIM   Hey Tim, I gotta tell ya...",
        "M&M    PiM Metals & More",
        "MEW    Model Engineers' Workshop",
        "MN     PiM Margin Notes",
        "MW     Machinist's Workshop",
        "PiM    Projects in Metal",
        "TMBR   The Machinist's Bedside Reader #1, #2, or #3",
    )

    # File:  Machinists_Workshop_Article_Index.csv Downloaded Mon 17 Feb
    # 2020 07:49:09 PM from
    # http://www.machinistsworkshop.net/resources/article-index/.  MD5 hash
    # is 7c4c9b4941327bbdc90ba6cb8bc4483a19ef8630.  BOM & carriage returns
    # removed.
    vp1 = dedent('''
    "Article Title","Author Name","Subject","Issue","Page"
    "A Rocking, Swinging Grinder Table","Harold Mason","Shop Machinery","MW Vol. 01 No. 1 Feb-Mar 1988","4"
    "Old Lathe Collet Adapters","Philip Duclos","Lathes","MW Vol. 01 No. 1 Feb-Mar 1988","12"
    "A Vernier Dividing Head","Alberto Marx","Shop Machinery","MW Vol. 01 No. 1 Feb-Mar 1988","16"
    "Surface Grinding On a Vertical Mill","Aubrey Keet","Mills","MW Vol. 01 No. 1 Feb-Mar 1988","19"
    "A Band Saw Speed Reducer","Bob Nelson","Shop Machinery","MW Vol. 01 No. 1 Feb-Mar 1988","22"
    "Curved Spoke Flywheel","Philip Duclos","Projects","MW Vol. 01 No. 2 Apr-May 1988","4"
    "A Double-ended Dial Indicator Adapter","Guy Lautard","Shop Machinery","MW Vol. 01 No. 2 Apr-May 1988","12"
    "Automatic Carriage Stop","R. P. Lebaron","Lathes","MW Vol. 01 No. 2 Apr-May 1988","15"
    "A Reverse for a Small Lathe","E. T. Feller","Lathes","MW Vol. 01 No. 2 Apr-May 1988","16"
    "Belt Sander","Robert S. Hedin","Shop Machinery","MW Vol. 01 No. 2 Apr-May 1988","20"
    "Basic Metal Finishes","James B. Harrill","General Machining Knowledge","MW Vol. 01 No. 3 Jun-Jul 1988","3"
    "Make Your Own Collet Chuck","Pat Loop","Lathes","MW Vol. 01 No. 3 Jun-Jul 1988","4"
    "Adjustable Try Squares","Ted Wright","Shop Accessories","MW Vol. 01 No. 3 Jun-Jul 1988","8"
    "Brass Hammer","Bill Davidson","Shop Accessories","MW Vol. 01 No. 3 Jun-Jul 1988","12"
    "Unorthodox Mill/Lathe Grinder","Philip Duclos","Shop Machinery","MW Vol. 01 No. 3 Jun-Jul 1988","15"
    "A Simple Rotary Table","Stephen G. Wellcome","Shop Machinery","MW Vol. 01 No. 3 Jun-Jul 1988","22"
    "An Untapped Source for Cast Iron Stock","John Kopf","Techniques","MW Vol. 01 No. 4 Aug-Sep 1988","3"
    "A Parallel Arm Scroll Saw","Robert S. Hedin","Shop Machinery","MW Vol. 01 No. 4 Aug-Sep 1988","4"
    "Machine Tools for Woodworking","Ted Roubal","Machine Tools","MW Vol. 01 No. 4 Aug-Sep 1988","12"
    "A Supplementary Tilting Milling Table","Michael T. Yamamoto","Mills","MW Vol. 01 No. 4 Aug-Sep 1988","17"
    "Making a Cylindrical Square","Ted Wright","Machining Accessories","MW Vol. 01 No. 4 Aug-Sep 1988","18"
    "Greater Precision for Scroll Chucks","Richard S. Torgerson","Techniques","MW Vol. 01 No. 4 Aug-Sep 1988","21"
    "A Four-Station Grinder","James D. Scharplaz, P.E.","Machine Tools","MW Vol. 01 No. 5 Oct-Nov 1988","4"
    "Button V-Block","Ed Dubosky","Workholding","MW Vol. 01 No. 5 Oct-Nov 1988","12"
    "Model Builder's Hand Vise","William F. Green","Hand Tools","MW Vol. 01 No. 5 Oct-Nov 1988","22"
    "A 32-Pounder Seacoast Cannon","William F. Green","Hobby Items","MW Vol. 01 No. 6 Dec 1988-Jan 1989","4"
    "A Ram Tailstock","Theodore M. Clarke","Machining Accessories","MW Vol. 01 No. 6 Dec 1988-Jan 1989","11"
    "The Presentation Swarf Collector","Bruce Jones","Machining Accessories","MW Vol. 01 No. 6 Dec 1988-Jan 1989","12"
    "Locating","John B. Gascoyne","General Machining Knowledge","MW Vol. 01 No. 6 Dec 1988-Jan 1989","14"
    "Two Designs for Welding Tables","Richard B. Walker","Welding/Foundry/Forging","MW Vol. 01 No. 6 Dec 1988-Jan 1989","17"
    "Steady Improvement","W.B Vaughan","Techniques","MW Vol. 01 No. 6 Dec 1988-Jan 1989","20"
    "Making a Milling Saw Arbor","George W. Genevro","Machining Accessories","MW Vol. 01 No. 6 Dec 1988-Jan 1989","22"
    "Saddle V-Block","Ed Dubosky","Machining Accessories","MW Vol. 02 No. 1 Feb-Mar 1989","4"
    "A Lathe Four-way Tool Turret","Robert C. Hannum","Machining Accessories","MW Vol. 02 No. 1 Feb-Mar 1989","11"
    "Lathe Threading Stop","Robert S. Hedin","Machining Accessories","MW Vol. 02 No. 1 Feb-Mar 1989","14"
    "A Change-Gear Bracket","Steve Harman","Machining Accessories","MW Vol. 02 No. 1 Feb-Mar 1989","17"
    "Downfeed Scale","Glenn L. Wilson","Machining Accessories","MW Vol. 02 No. 1 Feb-Mar 1989","22"
    "Collar Substitute","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 1 Feb-Mar 1989","24"
    "Holding Material in Place","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 1 Feb-Mar 1989","24"
    "Keeping Track of the Chuck Wrench","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 1 Feb-Mar 1989","24"
    "A More Versatile Tool","Norm Wells","Tips & Tricks","MW Vol. 02 No. 1 Feb-Mar 1989","24"
    "Odd Thickness Spacers","Charles Birmingham","Tips & Tricks","MW Vol. 02 No. 1 Feb-Mar 1989","24"
    "Turn a Shaft Without a Center Hole","Norm Wells","Techniques","MW Vol. 02 No. 1 Feb-Mar 1989","24"
    "Welding Light Steel Metal","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 1 Feb-Mar 1989","24"
    "Auxiliary Tailstock Center","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 2 Apr-May 1989","3"
    "Avoiding Hazards","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 2 Apr-May 1989","3"
    "Cutting Keyways Inside Holes","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 2 Apr-May 1989","3"
    "Getting a Better View","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 2 Apr-May 1989","3"
    "Square Stock in the Universal Chuck","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 2 Apr-May 1989","3"
    "Two Handy Jigs","Ed Dubosky","Shop Accessories","MW Vol. 02 No. 2 Apr-May 1989","4"
    "Mill/Drill Attachments","Paul J. Holm","Machining Accessories","MW Vol. 02 No. 2 Apr-May 1989","11"
    "Lathe Tips","Richard S. Torgerson","Techniques","MW Vol. 02 No. 2 Apr-May 1989","12"
    "Squaring the Circle","Alberto Marx","Techniques","MW Vol. 02 No. 2 Apr-May 1989","15"
    "Cross-feed Lever","Richard S. Torgerson","Machining Accessories","MW Vol. 02 No. 2 Apr-May 1989","18"
    "Hardness Tester","Lou Hinshaw","General Machining Knowledge","MW Vol. 02 No. 2 Apr-May 1989","21"
    "Accurate Drilling Through Bolts","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 2 Apr-May 1989","24"
    "Broken Taps","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 2 Apr-May 1989","24"
    "Filing Flat","Tim Smith","Tips & Tricks","MW Vol. 02 No. 2 Apr-May 1989","24"
    "Protecting Your Chisels","Thomas LaMance","Techniques","MW Vol. 02 No. 2 Apr-May 1989","24"
    "Removing Bushings From Blind Holes","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 2 Apr-May 1989","24"
    "Tailstock Troubles","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 2 Apr-May 1989","24"
    "A Milling Column","Houston Taylor","Machining Accessories","MW Vol. 02 No. 3 Jun-Jul 1989","4"
    "Can You Handle It?","Harold Mason","Machining Accessories","MW Vol. 02 No. 3 Jun-Jul 1989","10"
    "Reversible Lathe Die Holder","Percy Blandford","Machining Accessories","MW Vol. 02 No. 3 Jun-Jul 1989","19"
    "A Depth Gage","Marshall R. Young","Hand Tools","MW Vol. 02 No. 3 Jun-Jul 1989","20"
    "Tapers on Oblong Pieces","James Hamill","Techniques","MW Vol. 02 No. 3 Jun-Jul 1989","22"
    "Protecting Taps","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 3 Jun-Jul 1989","26"
    "GripsAll Indicator Base","Richard S. Torgerson","Shop Accessories","MW Vol. 02 No. 4 Aug-Sep 1989","4"
    "A Quick-change Gearbox","Eugene Toscano","Machining Accessories","MW Vol. 02 No. 4 Aug-Sep 1989","10"
    "Adjustable Pop-stop","Marshall R. Young","Machining Accessories","MW Vol. 02 No. 4 Aug-Sep 1989","15"
    "Drill Grinder Attachment Mount","Richard S. Torgerson","Machining Accessories","MW Vol. 02 No. 4 Aug-Sep 1989","18"
    "Engine Turning","Bob Marchese","Techniques","MW Vol. 02 No. 4 Aug-Sep 1989","22"
    "Centering a Gear Cutter","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 4 Aug-Sep 1989","24"
    "Cleaning Files","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 4 Aug-Sep 1989","24"
    "Cutting Duplicate Short Lengths","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 4 Aug-Sep 1989","24"
    "Sharp Return Bends","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 4 Aug-Sep 1989","24"
    "Transferring Hole Locations","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 4 Aug-Sep 1989","24"
    "Drill Guide","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 4 Aug-Sep 1989","26"
    "Nice Priced Handwheel","Ray Beals","Tips & Tricks","MW Vol. 02 No. 4 Aug-Sep 1989","26"
    "Using Brass Shim Stock","H. T. Biddle","Tips & Tricks","MW Vol. 02 No. 4 Aug-Sep 1989","26"
    "Boring Bar from Worn-out Bits","Gene Elliott","Tips & Tricks","MW Vol. 02 No. 4 Aug-Sep 1989","28"
    "Eyebolt Chuck","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 4 Aug-Sep 1989","28"
    "A Quick Setup Gage","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 4 Aug-Sep 1989","28"
    "Clamping the Tailstock","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 5 Oct-Nov 1989","3"
    "Finding the Socket","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 5 Oct-Nov 1989","3"
    "Protecting Your Chisels","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 5 Oct-Nov 1989","3"
    "A Quick Setup Gage","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 5 Oct-Nov 1989","3"
    "Improve Your Mill/Drill Machine","Bill Davidson","Techniques","MW Vol. 02 No. 5 Oct-Nov 1989","4"
    "A Pipe Center for your Lathe","James D. Scharplaz, P.E.","Machining Accessories","MW Vol. 02 No. 5 Oct-Nov 1989","8"
    "A Quick-change Gearbox","Eugene Toscano","Machining Accessories","MW Vol. 02 No. 5 Oct-Nov 1989","11"
    "A Huff 'n Puff Engine","Philip Duclos","Engines","MW Vol. 02 No. 5 Oct-Nov 1989","14"
    "Dividing Head Index Plates","D. E. Johnson","Machining Accessories","MW Vol. 02 No. 6 Dec 1989-Jan 1990","4"
    "Better File Handles","Bob Patrick","Hand Tools","MW Vol. 02 No. 6 Dec 1989-Jan 1990","8"
    "Wing Divider","Dave Gingery","Machining Accessories","MW Vol. 02 No. 6 Dec 1989-Jan 1990","12"
    "A Small Quick-change Tool Post","E. T. Feller","Machining Accessories","MW Vol. 02 No. 6 Dec 1989-Jan 1990","15"
    "Fly Cutter","George W. Genevro","Machining Accessories","MW Vol. 02 No. 6 Dec 1989-Jan 1990","18"
    "Lathe Shear Pin Modifications","Richard S. Torgerson","Machining Accessories","MW Vol. 02 No. 6 Dec 1989-Jan 1990","20"
    "Cross Drilling","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 6 Dec 1989-Jan 1990","24"
    "Cutting a Keyway","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 6 Dec 1989-Jan 1990","24"
    "Jig for Cross Drilling","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 6 Dec 1989-Jan 1990","24"
    "Quick Gear Selection","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 6 Dec 1989-Jan 1990","24"
    "Tool Tray","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 6 Dec 1989-Jan 1990","24"
    "Transferring Hole Locations","Thomas LaMance","Tips & Tricks","MW Vol. 02 No. 6 Dec 1989-Jan 1990","24"
    "Index the Indexing Ring","Thomas LaMance","Tips & Tricks","MW Vol. 03 No. 1 Feb-Mar 1990","3"
    "Prevent Slipping","Thomas LaMance","Tips & Tricks","MW Vol. 03 No. 1 Feb-Mar 1990","3"
    "A Die Stock Plus","Ted Wright","Hand Tools","MW Vol. 03 No. 1 Feb-Mar 1990","4"
    "Adjustable Angle Plate","Lane Sisson","Measuring & Layout","MW Vol. 03 No. 1 Feb-Mar 1990","10"
    "A Coolant Tank and Pump","Richard S. Torgerson","Machining Accessories","MW Vol. 03 No. 1 Feb-Mar 1990","15"
    "Shower Power","Alberto Marx","Techniques","MW Vol. 03 No. 1 Feb-Mar 1990","18"
    "Simple Tooling for Model Size Shoulder Bolts","Dave Gingery","Miscellaneous","MW Vol. 03 No. 1 Feb-Mar 1990","21"
    "Avoid Injury","Thomas LaMance","Tips & Tricks","MW Vol. 03 No. 2 Apr-May 1990","3"
    "Chip Shield","Thomas LaMance","Tips & Tricks","MW Vol. 03 No. 2 Apr-May 1990","3"
    "Indicating Your Setting","Thomas LaMance","Tips & Tricks","MW Vol. 03 No. 2 Apr-May 1990","3"
    "Elliptical Rotary Engine","Robert S. Hedin","Engines","MW Vol. 03 No. 2 Apr-May 1990","4"
    "A 5C Collet Closer","Larry Vanduyn","Machining Accessories","MW Vol. 03 No. 2 Apr-May 1990","12"
    "Indicator Clamps for Lathe Beds","Richard S. Torgerson","Machining Accessories","MW Vol. 03 No. 2 Apr-May 1990","16"
    "Risers for a 6 Atlas or Craftsman Lathe","Robert W. Metze","Machining Accessories","MW Vol. 03 No. 2 Apr-May 1990","22"
    "Variations on a Button V-block","William S. Wagner","Machining Accessories","MW Vol. 03 No. 2 Apr-May 1990","24"
    "Drills for Mill Cutters","H. T. Biddle","Tips & Tricks","MW Vol. 03 No. 3 Jun-Jul 1990","3"
    "A Tough Nut to Crack","Volney Landry","Tips & Tricks","MW Vol. 03 No. 3 Jun-Jul 1990","3"
    "A Small Boring Head","Robert S. Hedin","Machining Accessories","MW Vol. 03 No. 3 Jun-Jul 1990","4"
    "Zero Set Micrometer Dial","W.C. Grosjean","Machining Accessories","MW Vol. 03 No. 3 Jun-Jul 1990","7"
    "A Rolling Tailstock Arbor","D. E. Johnson","Machining Accessories","MW Vol. 03 No. 3 Jun-Jul 1990","8"
    "A Knife Blade from Scrap","Steve Acker","Hobby Items","MW Vol. 03 No. 3 Jun-Jul 1990","12"
    "Spindle Driving Handle for Emco Super 11 Lathe","Bob Paule","Machining Accessories","MW Vol. 03 No. 3 Jun-Jul 1990","15"
    "A Small Sheet Metal Brake","Glenn L. Wilson","Shop Machinery","MW Vol. 03 No. 3 Jun-Jul 1990","16"
    "Quick and Easy Electric Furnace","Robert Cortner","Welding/Foundry/Forging","MW Vol. 03 No. 3 Jun-Jul 1990","18"
    "A Lathe Collet Stand","Ralph T. Walker","Shop Accessories","MW Vol. 03 No. 3 Jun-Jul 1990","22"
    "Cleaning Out Your Dies","Norman H. Singer","Tips & Tricks","MW Vol. 03 No. 3 Jun-Jul 1990","24"
    "Lathe Tool Grinding Holder","Thomas LaMance","Tips & Tricks","MW Vol. 03 No. 3 Jun-Jul 1990","24"
    "A Reliable Drill Guide","R. Garding","Tips & Tricks","MW Vol. 03 No. 3 Jun-Jul 1990","24"
    "Give Metal Spinning a Whirl","Philip Duclos","Techniques","MW Vol. 03 No. 4 Aug-Sep 1990","4"
    "A One-handed Depth Gage","Ed Dubosky","Measuring & Layout","MW Vol. 03 No. 4 Aug-Sep 1990","12"
    "On The Cutting Edge","Alberto Marx","Techniques","MW Vol. 03 No. 4 Aug-Sep 1990","16"
    "Single Thread Worm Drives","John Olson","Lathes","MW Vol. 03 No. 4 Aug-Sep 1990","21"
    "Chuck Tool","Fred Silva","Tips & Tricks","MW Vol. 03 No. 4 Aug-Sep 1990","24"
    "Resetting Lathe Tool Height","Arch Gibson","Tips & Tricks","MW Vol. 03 No. 4 Aug-Sep 1990","24"
    "Rule Holder","Arch Gibson","Tips & Tricks","MW Vol. 03 No. 4 Aug-Sep 1990","24"
    "Emergency Drill Press Jig","Thomas LaMance","Tips & Tricks","MW Vol. 03 No. 5 Oct-Nov 1990","3"
    "Improve on an Idea","Glenn L. Wilson","Tips & Tricks","MW Vol. 03 No. 5 Oct-Nov 1990","3"
    "Taper Shank Turning Made Easy","D. E. Johnson","Techniques","MW Vol. 03 No. 5 Oct-Nov 1990","4"
    "Fastener Gauge","Phil Keller","Machining Accessories","MW Vol. 03 No. 5 Oct-Nov 1990","8"
    "Soft Faced Hammer","Bruce Bowser","Hand Tools","MW Vol. 03 No. 5 Oct-Nov 1990","10"
    "Milling Pockets","James Madison","Techniques","MW Vol. 03 No. 5 Oct-Nov 1990","15"
    "Square Collets","Robert S. Hedin","Machining Accessories","MW Vol. 03 No. 5 Oct-Nov 1990","20"
    "A Shop Hot-tank","Richard L. Huttinger","Welding/Foundry/Forging","MW Vol. 03 No. 5 Oct-Nov 1990","22"
    "A Mill-drill Repair","Steve Acker","Techniques","MW Vol. 03 No. 5 Oct-Nov 1990","24"
    "Wire Clamps","William A. Johnson","Machining Accessories","MW Vol. 03 No. 6 Dec 1990-Jan 1991","3"
    "Spinning Your Own Oil Can","Philip Duclos","Techniques","MW Vol. 03 No. 6 Dec 1990-Jan 1991","5"
    "Two-cylinder Oscillating Steam Engine","Robert S. Hedin","Engines","MW Vol. 03 No. 6 Dec 1990-Jan 1991","6"
    "An Economical X-axis Readout","Fran O. Mueller","Computers","MW Vol. 03 No. 6 Dec 1990-Jan 1991","18"
    "Power Feed Ball Turning Fixture","Don H. Vreeland","Machining Accessories","MW Vol. 03 No. 6 Dec 1990-Jan 1991","20"
    "Belt Sander Conversion","Norm Wells","Tips & Tricks","MW Vol. 04 No. 1 Feb-Mar 1991","3"
    "Pot Chuck","James Schubert","Tips & Tricks","MW Vol. 04 No. 1 Feb-Mar 1991","3"
    "Reducing Chip Gathering","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 1 Feb-Mar 1991","3"
    "Visible Chuck Wrench","David Schallhorn","Tips & Tricks","MW Vol. 04 No. 1 Feb-Mar 1991","3"
    "A Skypod","Glenn L. Wilson","Hobby Items","MW Vol. 04 No. 1 Feb-Mar 1991","4"
    "Tapping Block","Lane Sisson","Machining Accessories","MW Vol. 04 No. 1 Feb-Mar 1991","10"
    "Z-axis Downfeed for a Mill-drill Machine","Fran O. Mueller","Machining Accessories","MW Vol. 04 No. 1 Feb-Mar 1991","12"
    "The Mathematics of a Dividing Head","Stephen G. Wellcome","General Machining Knowledge","MW Vol. 04 No. 1 Feb-Mar 1991","17"
    "Spindle Lock","Richard S. Torgerson","Machining Accessories","MW Vol. 04 No. 1 Feb-Mar 1991","20"
    "Worm Drives Revisited","Virgil Matheson","Techniques","MW Vol. 04 No. 2 Apr-May 1991","3"
    "A Small Tool and Cutter Grinder","Glenn L. Wilson","Machine Tools","MW Vol. 04 No. 2 Apr-May 1991","4"
    "Single Wheel Knurling Tool","Richard S. Torgerson","Shop Accessories","MW Vol. 04 No. 2 Apr-May 1991","10"
    "A Glass Cutting Helper for your Drill Press","Robert Newcomb","Machining Accessories","MW Vol. 04 No. 2 Apr-May 1991","15"
    "A Universal Belt Tensioner","D. E. Johnson","Machining Accessories","MW Vol. 04 No. 2 Apr-May 1991","18"
    "Improving the Quick-change on a Small Lathe","E. T. Feller","Techniques","MW Vol. 04 No. 2 Apr-May 1991","20"
    "Preventing Blade Binding","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 2 Apr-May 1991","23"
    "Preventing Scoring","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 2 Apr-May 1991","23"
    "Specialty Brush","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 2 Apr-May 1991","23"
    "Wooden Chuck","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 2 Apr-May 1991","23"
    "Improvised Small End Mills","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 2 Apr-May 1991","24"
    "No More Hunting","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 2 Apr-May 1991","24"
    "Spindle-nose Collet","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 2 Apr-May 1991","24"
    "Sustaining Tailstock Lubrication","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 2 Apr-May 1991","24"
    "A Turning Tip","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 2 Apr-May 1991","24"
    "Collar-like Nut","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 3 Jun-Jul 1991","3"
    "Keeping the Noise Down","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 3 Jun-Jul 1991","3"
    "Time-saving Measure","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 3 Jun-Jul 1991","3"
    "Finger Treadle","Birk Petersen","Hobby Items","MW Vol. 04 No. 3 Jun-Jul 1991","4"
    "Making Up Band Saw Blades","Robert S. Hedin","Techniques","MW Vol. 04 No. 3 Jun-Jul 1991","9"
    "A Single Beam Trammel","Richard S. Torgerson","Machining Accessories","MW Vol. 04 No. 3 Jun-Jul 1991","12"
    "Adjustable Pop-stop for the Myford Lathe","Marshall R. Young","Machining Accessories","MW Vol. 04 No. 3 Jun-Jul 1991","22"
    "A Clamp for Cross-drilling","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 4 Aug-Sep 1991","3"
    "Combination Chuck Wrench","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 4 Aug-Sep 1991","3"
    "Conservative Coolant Applicator","Glenn L. Wilson","Shop Accessories","MW Vol. 04 No. 4 Aug-Sep 1991","4"
    "A High-efficiency Screw Press","D. E. Johnson","Machine Tools","MW Vol. 04 No. 4 Aug-Sep 1991","9"
    "A Lathe Rack Repair","Ted Wright","Techniques","MW Vol. 04 No. 4 Aug-Sep 1991","14"
    "Bed Extension for Atlas and Craftsman Lathes","Robert W. Metze","Machining Accessories","MW Vol. 04 No. 4 Aug-Sep 1991","18"
    "Making a Spring-loaded Center","George W. Genevro","Machining Accessories","MW Vol. 04 No. 4 Aug-Sep 1991","20"
    "Lathe Carriage Way Covers","Don H. Vreeland","Machining Accessories","MW Vol. 04 No. 4 Aug-Sep 1991","22"
    "Stay-put Lathe Carriage Lock Wrench","John B. Gascoyne","Machining Accessories","MW Vol. 04 No. 4 Aug-Sep 1991","24"
    "Better Visibility","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 5 Oct-Nov 1991","3"
    "Chisel Protection","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 5 Oct-Nov 1991","3"
    "Chuck Wrench Storage","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 5 Oct-Nov 1991","3"
    "Point of Safety","Thomas LaMance","General Machining Knowledge","MW Vol. 04 No. 5 Oct-Nov 1991","3"
    "Tailstock Tip","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 5 Oct-Nov 1991","3"
    "A Small Tool and Cutter Grinder (Plans)","Glenn L. Wilson","Machine Tools","MW Vol. 04 No. 5 Oct-Nov 1991","4"
    "Coaxial Indicator","Robert W. Metze","Techniques","MW Vol. 04 No. 5 Oct-Nov 1991","18"
    "A Tailstock Tap and Die Holder","Roger R. McHenry","Machining Accessories","MW Vol. 04 No. 5 Oct-Nov 1991","20"
    "Slot Anvil Depth Gage Mike","Ed Dubosky","Machining Accessories","MW Vol. 04 No. 5 Oct-Nov 1991","22"
    "Height Gage Conversion and Attachments","Richard S. Torgerson","Measuring & Layout","MW Vol. 04 No. 6 Dec 1991-Jan 1992","4"
    "Milling Cutter Arbor","J. W. Straight","Machining Accessories","MW Vol. 04 No. 6 Dec 1991-Jan 1992","11"
    "Load Cell (Hydraulic Scale)","Robert W. Metze","Techniques","MW Vol. 04 No. 6 Dec 1991-Jan 1992","12"
    "Eight-tube Wind Chimes","Thomas F. Howard","Hobby Items","MW Vol. 04 No. 6 Dec 1991-Jan 1992","14"
    "Two-headed Bolt with Nut","Jerry J. Fear","Hobby Items","MW Vol. 04 No. 6 Dec 1991-Jan 1992","21"
    "A Drilling Challenge","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 6 Dec 1991-Jan 1992","24"
    "Finding the Hole","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 6 Dec 1991-Jan 1992","24"
    "Hole Enlargement","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 6 Dec 1991-Jan 1992","24"
    "Reaching the Unreachable","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 6 Dec 1991-Jan 1992","24"
    "A Simple Driver","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 6 Dec 1991-Jan 1992","24"
    "Square Stock","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 6 Dec 1991-Jan 1992","24"
    "Time and Labor Saver","Thomas LaMance","Tips & Tricks","MW Vol. 04 No. 6 Dec 1991-Jan 1992","24"
    "Spindle Thread Protection","Thomas LaMance","Tips & Tricks","MW Vol. 05 No. 1 Feb-Mar 1992","3"
    "Taplicator","Thomas LaMance","Tips & Tricks","MW Vol. 05 No. 1 Feb-Mar 1992","3"
    "A Two-bit Tool","Thomas LaMance","Tips & Tricks","MW Vol. 05 No. 1 Feb-Mar 1992","3"
    "From Shears to Brake: A Boxing Story","Harold Mason","Miscellaneous","MW Vol. 05 No. 1 Feb-Mar 1992","4"
    "Holding Thin Material for Machining","John A. Cooper","Workholding","MW Vol. 05 No. 1 Feb-Mar 1992","12"
    "A Diamond Dresser","Conrad A. Huard","Shop Accessories","MW Vol. 05 No. 1 Feb-Mar 1992","14"
    "A Drill Press Speed Reducer","D. E. Johnson","Machining Accessories","MW Vol. 05 No. 1 Feb-Mar 1992","16"
    "Rules - Differential and Difference","Ed Dubosky","Hand Tools","MW Vol. 05 No. 1 Feb-Mar 1992","19"
    "Flying Dog Protection","Thomas LaMance","Tips & Tricks","MW Vol. 05 No. 2 Apr-May 1992","3"
    "Truing a Grinding Wheel","Thomas LaMance","Tips & Tricks","MW Vol. 05 No. 2 Apr-May 1992","3"
    "Work on Your Faceplate","Thomas LaMance","Tips & Tricks","MW Vol. 05 No. 2 Apr-May 1992","3"
    "A Universal Cross Drilling Fixture","D. E. Johnson","Lathes","MW Vol. 05 No. 2 Apr-May 1992","4"
    "X and Y Scales for the Mill","Glenn L. Wilson","Machining Accessories","MW Vol. 05 No. 2 Apr-May 1992","10"
    "Reamers for Odd Sized Holes","Lowie L. Roscoe, Jr.","Machining Accessories","MW Vol. 05 No. 2 Apr-May 1992","12"
    "Hot Dip Tool Protection","Richard S. Torgerson","Techniques","MW Vol. 05 No. 2 Apr-May 1992","14"
    "Table Stop","James Madison","Machining Accessories","MW Vol. 05 No. 2 Apr-May 1992","18"
    "Lever Operated Tailstock","Ed Dubosky","Machining Accessories","MW Vol. 05 No. 2 Apr-May 1992","20"
    "Cone Mandrel","Thomas LaMance","Tips & Tricks","MW Vol. 05 No. 3 Jun-Jul 1992","3"
    "Cutting Heavy Sheet Metal","Thomas LaMance","Tips & Tricks","MW Vol. 05 No. 3 Jun-Jul 1992","3"
    "Time Saver","Thomas LaMance","Tips & Tricks","MW Vol. 05 No. 3 Jun-Jul 1992","3"
    "Little Blazer Engine","Philip Duclos","Engines","MW Vol. 05 No. 3 Jun-Jul 1992","4"
    "Mill Vise: Rework for Precision","Richard S. Torgerson","Techniques","MW Vol. 05 No. 3 Jun-Jul 1992","6"
    "Machining an Angle Plate","Steve Acker","Gunsmithing","MW Vol. 05 No. 3 Jun-Jul 1992","20"
    "Drill Sharpening Fixture and Point Splitter","Robert S. Hedin","Shop Accessories","MW Vol. 05 No. 3 Jun-Jul 1992","22"
    "Universal and Reusable Table Fixtures","James Madison","Machining Accessories","MW Vol. 05 No. 3 Jun-Jul 1992","29"
    "A Cheap Cutoff Tool","Thomas LaMance","Tips & Tricks","MW Vol. 05 No. 4 Aug-Sep 1992","3"
    "An Easy Indicator","Thomas LaMance","Tips & Tricks","MW Vol. 05 No. 4 Aug-Sep 1992","3"
    "Turning Small Beads and Coves","Thomas LaMance","Tips & Tricks","MW Vol. 05 No. 4 Aug-Sep 1992","3"
    "Mill/Drill Speed Reduction","Richard S. Torgerson","Machining Accessories","MW Vol. 05 No. 4 Aug-Sep 1992","4"
    "Making an Index Plate for a 4-3/4 Center Height Dividing Head","Ted Wright","Machining Accessories","MW Vol. 05 No. 4 Aug-Sep 1992","16"
    "Flare Nut Adapter Tool","Mike Hoff","Machining Accessories","MW Vol. 05 No. 4 Aug-Sep 1992","19"
    "Mini Square Hole Punch","Ed Dubosky","Machining Accessories","MW Vol. 05 No. 4 Aug-Sep 1992","24"
    "End Mill Sharpening Holding Fixture","Arthur Crow","Machining Accessories","MW Vol. 05 No. 4 Aug-Sep 1992","26"
    "Drip Oiler","Don H. Vreeland","Machine Modifications","MW Vol. 05 No. 4 Aug-Sep 1992","32"
    "Disk Sander Safety","Thomas LaMance","Tips & Tricks","MW Vol. 05 No. 5 Oct-Nov 1992","3"
    "An Extra Hand","Thomas LaMance","Tips & Tricks","MW Vol. 05 No. 5 Oct-Nov 1992","3"
    "A Short-tailed Dog","Thomas LaMance","Tips & Tricks","MW Vol. 05 No. 5 Oct-Nov 1992","3"
    "Micro Aids for a Full Size Machinist","D. E. Johnson","Techniques","MW Vol. 05 No. 5 Oct-Nov 1992","4"
    "Tailstock Die Holder","George W. Genevro","Machining Accessories","MW Vol. 05 No. 5 Oct-Nov 1992","11"
    "Tool Tower","Ed Dubosky","Shop Accessories","MW Vol. 05 No. 5 Oct-Nov 1992","14"
    "Multifacet Drills","James Madison","Machining Accessories","MW Vol. 05 No. 5 Oct-Nov 1992","16"
    "A Quick-acting Tailstock Lock","John Calder","Machining Accessories","MW Vol. 05 No. 5 Oct-Nov 1992","20"
    "Economy Substitute for a Bridgeport","John F. Ernest","Machining Accessories","MW Vol. 05 No. 5 Oct-Nov 1992","24"
    "A Ring Furnace","Conrad A. Huard","Welding/Foundry/Forging","MW Vol. 05 No. 5 Oct-Nov 1992","28"
    "Expanding Your Arbor Press Capability","John E. Turner","Shop Machinery","MW Vol. 05 No. 5 Oct-Nov 1992","30"
    "Cheap Cup Washers","Thomas LaMance","Tips & Tricks","MW Vol. 05 No. 6 Dec 1992-Jan 1993","3"
    "A Classic Boring Bar Holder","D. E. Johnson","Machining Accessories","MW Vol. 05 No. 6 Dec 1992-Jan 1993","4"
    "Home-built Gearbox For Your Atlas 6 Lathe","Glenn A. Pettit","Machining Accessories","MW Vol. 05 No. 6 Dec 1992-Jan 1993","6"
    "Double-sided Tape for Machining","James Madison","Techniques","MW Vol. 05 No. 6 Dec 1992-Jan 1993","21"
    "Conversion to Three-phase Power","James C. Robertson","Motors","MW Vol. 05 No. 6 Dec 1992-Jan 1993","28"
    "A Low Cost Adjustable Counterbore","J. Worzala","Machining Accessories","MW Vol. 05 No. 6 Dec 1992-Jan 1993","31"
    "Odd Thickness Spacers","Charles Birmingham","Tips & Tricks","MW Vol. 06 No. 1 Feb-Mar 1993","3"
    "Turn a Shaft Without a Center Hole","Norm Wells","Tips & Tricks","MW Vol. 06 No. 1 Feb-Mar 1993","3"
    "A Novel Tripod Ball Head","Glenn L. Wilson","Hobby Items","MW Vol. 06 No. 1 Feb-Mar 1993","4"
    "An Automatic Punch","Ed Dubosky","Hand Tools","MW Vol. 06 No. 1 Feb-Mar 1993","10"
    "A Lever Tailstock Feed for the Center Lathe","Ted Wright","Machining Accessories","MW Vol. 06 No. 1 Feb-Mar 1993","12"
    "On the Subject of Stiffness and Overhang","Aubrey Keet","Techniques","MW Vol. 06 No. 1 Feb-Mar 1993","20"
    "Reversible Lathe Carriage Stop","Tom Borowicz","Machining Accessories","MW Vol. 06 No. 1 Feb-Mar 1993","24"
    "Drop-by-drop Cutting Fluid","Michael T. Yamamoto","Miscellaneous","MW Vol. 06 No. 1 Feb-Mar 1993","28"
    "Collar Substitute","Thomas LaMance","Tips & Tricks","MW Vol. 06 No. 2 Apr-May 1993","3"
    "Holding Material in Place","Thomas LaMance","Tips & Tricks","MW Vol. 06 No. 2 Apr-May 1993","3"
    "A More Versatile Tool","Norm Wells","Tips & Tricks","MW Vol. 06 No. 2 Apr-May 1993","3"
    "Welding Light Sheet Metal","Thomas LaMance","Tips & Tricks","MW Vol. 06 No. 2 Apr-May 1993","3"
    "A Micro Drilling/milling Spindle","W. R. Smith","Lathes","MW Vol. 06 No. 2 Apr-May 1993","4"
    "Faceplates for Gap Bed Lathes","Tom Maykoski","Lathes","MW Vol. 06 No. 2 Apr-May 1993","12"
    "Surface Finishes","James Madison","General Machining Knowledge","MW Vol. 06 No. 2 Apr-May 1993","14"
    "One Way to Fix a Stud","Spencer Schonher","Techniques","MW Vol. 06 No. 2 Apr-May 1993","18"
    "Hex Wrench Extension","Theodore R. McDowell","General Machining Knowledge","MW Vol. 06 No. 2 Apr-May 1993","20"
    "Recycling a Mirror","Terry Sexton","Techniques","MW Vol. 06 No. 2 Apr-May 1993","21"
    "Making a Set of Boring Bars","A. J. Lofquist","Lathes","MW Vol. 06 No. 2 Apr-May 1993","22"
    "Making Chatterless Countersinks","D. E. Johnson","General Machining Knowledge","MW Vol. 06 No. 2 Apr-May 1993","26"
    "Getting Rid of Chips on Your Band Saw","A. M. Christopherson","Techniques","MW Vol. 06 No. 2 Apr-May 1993","28"
    "Chatter and the Cutoff Blade","Laurence Davis","Techniques","MW Vol. 06 No. 2 Apr-May 1993","29"
    "Making Simple Graduated Collars with Your Computer","Terry McCreary","Techniques","MW Vol. 06 No. 2 Apr-May 1993","30"
    "Dye Applicator","Burt Noble","Tips & Tricks","MW Vol. 06 No. 3 Jun-Jul 1993","3"
    "Spindle Cleaner","Thomas LaMance","Tips & Tricks","MW Vol. 06 No. 3 Jun-Jul 1993","3"
    "Spindle-mounted Collet Attachment for 12 Atlas-type Lathes","Bruce Jones","Machining Accessories","MW Vol. 06 No. 3 Jun-Jul 1993","4"
    "Building a Band Saw","Max B. Strauss","Machine Tools","MW Vol. 06 No. 3 Jun-Jul 1993","13"
    "Drilling Accurately Centered Cross-holes in Round Stock","Robert Koval","Techniques","MW Vol. 06 No. 3 Jun-Jul 1993","26"
    "The Rise and Fall of the Taiwanese Band Saw","Scott D. Strampe","Machine Tools","MW Vol. 06 No. 3 Jun-Jul 1993","28"
    "An Easy Way to Make a Multi-position Tool Post","J. O. Barbour, Jr.","Machining Accessories","MW Vol. 06 No. 3 Jun-Jul 1993","30"
    "Boring Thin-wall Tubing","John E. Turner","Techniques","MW Vol. 06 No. 3 Jun-Jul 1993","32"
    "Belt Replacement","Earl Stahler","Tips & Tricks","MW Vol. 06 No. 4 Aug-Sep 1993","3"
    "A Lever-operated Tailstock Clamp for Atlas/Sears 12\"" Lathes","Harry B. Francisco","Lathes","MW Vol. 06 No. 4 Aug-Sep 1993","4"
    "A Great Little Clamp","Bob Patrick","General Machining Knowledge","MW Vol. 06 No. 4 Aug-Sep 1993","12"
    "Two DROs Under $125 Per Axis","Gene Martin","Computers","MW Vol. 06 No. 4 Aug-Sep 1993","17"
    "Truing the Column of a Mill-drill Machine","John A. Cooper","Mills","MW Vol. 06 No. 4 Aug-Sep 1993","26"
    "Instant Soft Jaws for the Vise","D. E. Johnson","Shop Accessories","MW Vol. 06 No. 4 Aug-Sep 1993","29"
    "Machining Internal Threads - A Different Approach","Robert L. Grady","Techniques","MW Vol. 06 No. 4 Aug-Sep 1993","30"
    "A Welding Tip","Steve Acker","Welding/Foundry/Forging","MW Vol. 06 No. 4 Aug-Sep 1993","31"
    "Internal-external Center Finder","W. A. Lincoln","Machining Accessories","MW Vol. 06 No. 5 Oct-Nov 1993","3"
    "The Dedicated Tapper","Harold Mason","Shop Accessories","MW Vol. 06 No. 5 Oct-Nov 1993","6"
    "Turning Square Stock Round","J. W. (Bill) Reichart","Techniques","MW Vol. 06 No. 5 Oct-Nov 1993","31"
    "Reconditioning Your Chuck","Thomas LaMance","Tips & Tricks","MW Vol. 06 No. 6 Dec 1993-Jan 1994","3"
    "A Precision Metal Stamper","Glenn L. Wilson","Shop Accessories","MW Vol. 06 No. 6 Dec 1993-Jan 1994","4"
    "A Heavy Duty Belt Grinder","Arthur Crow","Shop Machinery","MW Vol. 06 No. 6 Dec 1993-Jan 1994","9"
    "Table Fixtures and Applications","James Madison","Shop Accessories","MW Vol. 06 No. 6 Dec 1993-Jan 1994","14"
    "A Very Handy One-inch Height Gage","Herman Kubowsky","Miscellaneous","MW Vol. 06 No. 6 Dec 1993-Jan 1994","16"
    "Plastigage in the Shop - A Handy Measuring Tool","Merle Grabhorn","Miscellaneous","MW Vol. 06 No. 6 Dec 1993-Jan 1994","20"
    "A Chip Breaker","Walter B. Mueller","Lathes","MW Vol. 06 No. 6 Dec 1993-Jan 1994","23"
    "The Asian Connection","Terry Sexton","General Machining Knowledge","MW Vol. 06 No. 6 Dec 1993-Jan 1994","24"
    "Antirotation Drill Holder for the Lathe Tailstock","D. E. Johnson","Lathes","MW Vol. 06 No. 6 Dec 1993-Jan 1994","30"
    "A Rugged Tap Wrench","David Blystone","Miscellaneous","MW Vol. 06 No. 6 Dec 1993-Jan 1994","31"
    "Accurate Location to Holes or Edges","Jim Evans","Tips & Tricks","MW Vol. 07 No. 1 Feb-Mar 1994","3"
    "The Tripod Eliminator","Harold Mason","Miscellaneous","MW Vol. 07 No. 1 Feb-Mar 1994","4"
    "A Two-jaw Lathe Chuck","Jacob Schulzinger","Lathes","MW Vol. 07 No. 1 Feb-Mar 1994","15"
    "A Versatile Bubble Protractor","Glenn L. Wilson","Miscellaneous","MW Vol. 07 No. 1 Feb-Mar 1994","18"
    "Easy-to-build C-clamps","Arthur Crow","General Machining Knowledge","MW Vol. 07 No. 1 Feb-Mar 1994","22"
    "Making a Hardened Steel Washer","Steve Acker","Gunsmithing","MW Vol. 07 No. 1 Feb-Mar 1994","24"
    "A Pencil Attachment for the Universal Surface Gage","John B. Gascoyne","Miscellaneous","MW Vol. 07 No. 1 Feb-Mar 1994","26"
    "Machinable Angles","James Madison","Mills","MW Vol. 07 No. 1 Feb-Mar 1994","28"
    "Collet Adapter","Art Paquay","Lathes","MW Vol. 07 No. 1 Feb-Mar 1994","30"
    "Automatic Oiler","Thomas LaMance","Tips & Tricks","MW Vol. 07 No. 2 Apr-May 1994","3"
    "Parting Tool Modification","Thomas LaMance","Tips & Tricks","MW Vol. 07 No. 2 Apr-May 1994","3"
    "Tool Bit Support","Thomas LaMance","Tips & Tricks","MW Vol. 07 No. 2 Apr-May 1994","3"
    "A One-inch Height Gage","Walter B. Mueller","Miscellaneous","MW Vol. 07 No. 2 Apr-May 1994","4"
    "A Shop-built Taper Attachment for Your Atlas 6\"" Lathe","Glenn A. Pettit","Lathes","MW Vol. 07 No. 2 Apr-May 1994","16"
    "Corner Locator","James Madison","Mills","MW Vol. 07 No. 2 Apr-May 1994","21"
    "Universal Drill Press Hold-down","J. W. Straight","Shop Machinery","MW Vol. 07 No. 2 Apr-May 1994","24"
    "Blacksmithing in the Twenty-first Century","David Smith","Welding/Foundry/Forging","MW Vol. 07 No. 2 Apr-May 1994","26"
    "Tap Wrench Guide with Depth Gage","R.G. Sparber","General Machining Knowledge","MW Vol. 07 No. 2 Apr-May 1994","30"
    "Quick-acting Universal Lathe Mandrel","D. E. Johnson","Lathes","MW Vol. 07 No. 2 Apr-May 1994","31"
    "Instantaneously Reversible Motor Control","Ray Stroh","Miscellaneous","MW Vol. 07 No. 2 Apr-May 1994","32"
    "Cutting Odd-Count Threads","Clinton James","Tips & Tricks","MW Vol. 07 No. 3 Jun-Jul 1994","3"
    "A Simple Truing Jig","Thomas LaMance","Tips & Tricks","MW Vol. 07 No. 3 Jun-Jul 1994","3"
    "A Compact Carousel Tool Rack","Glenn L. Wilson","Miscellaneous","MW Vol. 07 No. 3 Jun-Jul 1994","4"
    "A Lathe Milling Attachment","Tom Borowicz","Lathes","MW Vol. 07 No. 3 Jun-Jul 1994","8"
    "Sometimes Slower is Better","J. O. Barbour, Jr.","General Machining Knowledge","MW Vol. 07 No. 3 Jun-Jul 1994","24"
    "P-style Upside-down Partoff Blade Holder","Michael T. Yamamoto","Lathes","MW Vol. 07 No. 3 Jun-Jul 1994","28"
    "A Milling Table","Brian Fairey","Mills","MW Vol. 07 No. 3 Jun-Jul 1994","32"
    "Another Use","L. L. Vanice","Tips & Tricks","MW Vol. 07 No. 4 Aug-Sep 1994","3"
    "Gasket Cutter","Roger Claude","Tips & Tricks","MW Vol. 07 No. 4 Aug-Sep 1994","3"
    "An Inexpensive Power Feed for the RF-30 Mill/Drill","John F. Kraemer","Mills","MW Vol. 07 No. 4 Aug-Sep 1994","4"
    "A Lathe Boring Bar Set","Robert S. Hedin","Lathes","MW Vol. 07 No. 4 Aug-Sep 1994","13"
    "Another Index System for the Lathe","Jack R. Thompson","Lathes","MW Vol. 07 No. 4 Aug-Sep 1994","16"
    "Shoptask Modifications","Ludwig Schweinfurth","Shop Machinery","MW Vol. 07 No. 4 Aug-Sep 1994","21"
    "Personal Safety and Machine Grounding","Steve Acker","Gunsmithing","MW Vol. 07 No. 4 Aug-Sep 1994","24"
    "Three Ideas for a More Efficient Shop","Don H. Vreeland","General Machining Knowledge","MW Vol. 07 No. 4 Aug-Sep 1994","26"
    "A Carriage Stop for the Mill","Roy Rice","Mills","MW Vol. 07 No. 4 Aug-Sep 1994","27"
    "V-Blocks in a Vise","James Madison","Mills","MW Vol. 07 No. 4 Aug-Sep 1994","28"
    "More on Instantaneously Reversible Motor Control","Ray Stroh","Miscellaneous","MW Vol. 07 No. 4 Aug-Sep 1994","30"
    "Extra Probes for the Lincoln Center Finder","Mark Golding","Miscellaneous","MW Vol. 07 No. 4 Aug-Sep 1994","32"
    "Atlas 10-31T Head Spindle","William D. Hibbard","Lathes","MW Vol. 07 No. 4 Aug-Sep 1994","32"
    "Lathe Dog","D. A. Drayson","Tips & Tricks","MW Vol. 07 No. 5 Oct-Nov 1994","3"
    "An Inexpensive Milling/Drilling Spindle","W. R. Smith","Lathes","MW Vol. 07 No. 5 Oct-Nov 1994","4"
    "The Dividing Head (Index Head)","Frank A. McLean","General Machining Knowledge","MW Vol. 07 No. 5 Oct-Nov 1994","16"
    "Clutch-motor Starter for Three-phase Converters","James Hesse","Projects","MW Vol. 07 No. 5 Oct-Nov 1994","22"
    "An Inexpensive Air Compressor","James Hesse","Miscellaneous","MW Vol. 07 No. 5 Oct-Nov 1994","24"
    "New Uses for Old Tools","John F. Ernest","Techniques","MW Vol. 07 No. 5 Oct-Nov 1994","26"
    "A Motor Drive Modification for the Sherline Mill and Lathe","William Haberman","Shop Machinery","MW Vol. 07 No. 5 Oct-Nov 1994","28"
    "Make a Thread Dial for Your Lathe","J. O. Barbour, Jr.","Lathes","MW Vol. 07 No. 5 Oct-Nov 1994","30"
    "Lathe Adapter Blocks","Phil Piper","Machining Accessories","MW Vol. 07 No. 6 Dec 1994-Jan 1995","2"
    "Reminder","Thomas LaMance","Tips & Tricks","MW Vol. 07 No. 6 Dec 1994-Jan 1995","3"
    "Last Pass Indicator","Glenn L. Wilson","Machining Accessories","MW Vol. 07 No. 6 Dec 1994-Jan 1995","4"
    "A Low Cost Stepper Motor Drive","Tom Dahlin","Motors","MW Vol. 07 No. 6 Dec 1994-Jan 1995","8"
    "Two Small Presses","Robert W. Metze","Machine Tools","MW Vol. 07 No. 6 Dec 1994-Jan 1995","12"
    "Spindle Clamps for a Mill/drill","William Lifson","Machining Accessories","MW Vol. 07 No. 6 Dec 1994-Jan 1995","19"
    "Winding a Coil For a Magnetic Chuck","Glenn L. Wilson","Techniques","MW Vol. 07 No. 6 Dec 1994-Jan 1995","22"
    "Winding a Coil For a Magnetic Chuck","James Hesse","Techniques","MW Vol. 07 No. 6 Dec 1994-Jan 1995","22"
    "Timesaver Clampset","James Madison","Workholding","MW Vol. 07 No. 6 Dec 1994-Jan 1995","26"
    "Modifications to the Sherline Mill","H. B. Upshur","Machining Accessories","MW Vol. 07 No. 6 Dec 1994-Jan 1995","28"
    "Home Sandblasting Cabinet","Fred Lavenuta","Shop Accessories","MW Vol. 07 No. 6 Dec 1994-Jan 1995","30"
    "Band Saw Blade Grinder","W. A. Lincoln","Machining Accessories","MW Vol. 08 No. 1 Feb-Mar 1995","4"
    "Elegant Long Reach Thickness Caliper","Arthur Crow","Measuring & Layout","MW Vol. 08 No. 1 Feb-Mar 1995","12"
    "An Open-sided Toolholder","James Iiames","Machining Accessories","MW Vol. 08 No. 1 Feb-Mar 1995","17"
    "Sphere Machining","Lewis Jenkins","Techniques","MW Vol. 08 No. 1 Feb-Mar 1995","20"
    "Make Your Own Edge Finder","Lowie L. Roscoe, Jr.","Shop Accessories","MW Vol. 08 No. 1 Feb-Mar 1995","24"
    "Correcting Watch Case Bow/Pendant Wear","W. R. Smith","Miscellaneous","MW Vol. 08 No. 1 Feb-Mar 1995","28"
    "Methods for Success: Plus or Minus?","James Madison","Techniques","MW Vol. 08 No. 1 Feb-Mar 1995","32"
    "Special Milling Jig","Edward T. Haas, Jr.","Tips & Tricks","MW Vol. 08 No. 1 Feb-Mar 1995","41"
    "Making Heavy Work Light","R. Joseph Ransil","Tips & Tricks","MW Vol. 08 No. 1 Feb-Mar 1995","48"
    "Repeat Threading","J. R. Wilson, Jr.","Tips & Tricks","MW Vol. 08 No. 1 Feb-Mar 1995","48"
    "A Pantograph Label Maker","Glenn L. Wilson","Shop Accessories","MW Vol. 08 No. 2 Apr-May 1995","4"
    "Castle Nuts","Jacob Schulzinger","Miscellaneous","MW Vol. 08 No. 2 Apr-May 1995","14"
    "Build a Metal Slicer","John Dean","Shop Machinery","MW Vol. 08 No. 2 Apr-May 1995","18"
    "Lathe Adapters","Bruce Jones","Machining Accessories","MW Vol. 08 No. 2 Apr-May 1995","21"
    "Duplicating Radii","Lowie L. Roscoe, Jr.","Techniques","MW Vol. 08 No. 2 Apr-May 1995","24"
    "Moving on a Budget","Don Titus","Techniques","MW Vol. 08 No. 2 Apr-May 1995","27"
    "A Hole Punch for Thin Material","Fred Bruce","Machining Accessories","MW Vol. 08 No. 2 Apr-May 1995","30"
    "Faceplate Removal","Percy Blandford","Techniques","MW Vol. 08 No. 2 Apr-May 1995","32"
    "Bumping Out","Percy Blandford","Techniques","MW Vol. 08 No. 2 Apr-May 1995","33"
    "Large Radii Cutting","Arden A. Schroeder","Tips & Tricks","MW Vol. 08 No. 2 Apr-May 1995","33"
    "Modifications for an Inexpensive Power Feed for the RF-30 Mill/drill","John F. Kraemer","Machining Accessories","MW Vol. 08 No. 2 Apr-May 1995","34"
    "A Novice Reports on His Experience with Sherline Tools","Charles T. Atkinson","Techniques","MW Vol. 08 No. 2 Apr-May 1995","35"
    "Centering Work","Thomas LaMance","Tips & Tricks","MW Vol. 08 No. 2 Apr-May 1995","39"
    "Holding Adjustable Centers","Thomas LaMance","Tips & Tricks","MW Vol. 08 No. 2 Apr-May 1995","39"
    "The Gunsmith Machinist: Aligning Scope Mounts","Steve Acker","Gunsmithing","MW Vol. 08 No. 2 Apr-May 1995","40"
    "Handwheel Modification on a Sherline Mill","W. L. Sewell","Machining Accessories","MW Vol. 08 No. 2 Apr-May 1995","43"
    "A Weird Thread that Works","Clinton James","Techniques","MW Vol. 08 No. 2 Apr-May 1995","45"
    "Product Opinion","Joe Rice","Hobby Community","MW Vol. 08 No. 2 Apr-May 1995","48"
    "Milling Machine Power Feed","W. A. Lincoln","Machining Accessories","MW Vol. 08 No. 3 Jun-Jul 1995","4"
    "Modifications to the Atlas 6 Lathe","Michael Brown","Machining Accessories","MW Vol. 08 No. 3 Jun-Jul 1995","20"
    "Shop Bench","David Joly","Shop Accessories","MW Vol. 08 No. 3 Jun-Jul 1995","22"
    "A Toolholder","E. W. Crews","Machining Accessories","MW Vol. 08 No. 3 Jun-Jul 1995","24"
    "Creativity","Glenn L. Wilson","Techniques","MW Vol. 08 No. 3 Jun-Jul 1995","26"
    "A Combination Regular and Bull Nose Live Center","J. O. Barbour, Jr.","Machining Accessories","MW Vol. 08 No. 3 Jun-Jul 1995","28"
    "Methods for Success: Indicating & Picking Up - Part I","James Madison","Miscellaneous","MW Vol. 08 No. 3 Jun-Jul 1995","31"
    "The Gunsmith Machinist: A Travel Measurement Plate","Steve Acker","Gunsmithing","MW Vol. 08 No. 3 Jun-Jul 1995","36"
    "A Convenient Addition to a Palmgren Angle Vise","Charles T. Atkinson","Workholding","MW Vol. 08 No. 3 Jun-Jul 1995","38"
    "Belt Replacement","Earl Stahler","Tips & Tricks","MW Vol. 08 No. 3 Jun-Jul 1995","42"
    "A Simple Truing Jig","Thomas LaMance","Tips & Tricks","MW Vol. 08 No. 3 Jun-Jul 1995","42"
    "Sealing a Bargain","George Kolar","Tips & Tricks","MW Vol. 08 No. 3 Jun-Jul 1995","44"
    "Building Zippy MK1","Terry Sexton","Shop Machinery","MW Vol. 08 No. 4 Aug-Sep 1995","4"
    "Farrier's Forge","Conrad A. Huard","Hand Tools","MW Vol. 08 No. 4 Aug-Sep 1995","17"
    "A Machinery Oil Gun","Jerry L. Sokol","Machine Modifications","MW Vol. 08 No. 4 Aug-Sep 1995","22"
    "A Poor Man's Electronic Edge Finder","F. A. Pellizzari","Shop Accessories","MW Vol. 08 No. 4 Aug-Sep 1995","26"
    "An Abrasive Belt Slitter","Paul Smeltzer","Shop Machinery","MW Vol. 08 No. 4 Aug-Sep 1995","28"
    "The Gunsmith Machinist: A Barrel Bushing Jig Aligning Scope Mounts","Steve Acker","Gunsmithing","MW Vol. 08 No. 4 Aug-Sep 1995","32"
    "Aligning a Lathe","Stephen G. Wellcome","Techniques","MW Vol. 08 No. 4 Aug-Sep 1995","34"
    "Methods for Success: Indicating & Picking Up - Part II","James Madison","Miscellaneous","MW Vol. 08 No. 4 Aug-Sep 1995","36"
    "Lights Out","Clinton James","Welding/Foundry/Forging","MW Vol. 08 No. 4 Aug-Sep 1995","41"
    "Coolant Pump","George Kolar","Tips & Tricks","MW Vol. 08 No. 4 Aug-Sep 1995","44"
    "A Pocket-sized, Gift Quality Blow Gun","Bruce Jones","Hobby Items","MW Vol. 08 No. 5 Oct-Nov 1995","4"
    "Turn-O-Mill","Ralph B. Miller","Machine Tools","MW Vol. 08 No. 5 Oct-Nov 1995","16"
    "End Mill Sharpening Jig","John A. Cooper","Machining Accessories","MW Vol. 08 No. 5 Oct-Nov 1995","23"
    "Mounting a Dial Caliper on the Lathe","W. A. Lincoln","Machining Accessories","MW Vol. 08 No. 5 Oct-Nov 1995","28"
    "Adapting a Palmgren Drill Press Vise for Use on Sherline Machines","Charles T. Atkinson","Machining Accessories","MW Vol. 08 No. 5 Oct-Nov 1995","31"
    "The Gunsmith Machinist: Installing Sight Beads","Steve Acker","Gunsmithing","MW Vol. 08 No. 5 Oct-Nov 1995","32"
    "Methods for Success: Indicating & Picking Up - Part III","James Madison","Miscellaneous","MW Vol. 08 No. 5 Oct-Nov 1995","34"
    "Product Opinion","Edward G. Hoffman","Hobby Community","MW Vol. 08 No. 5 Oct-Nov 1995","37"
    "A Mini Mill Attachment","Glenn L. Wilson","Machining Accessories","MW Vol. 08 No. 6 Dec 1995-Jan 1996","6"
    "A Single-shot Pneumatic Hammer","Robert L. Calvert","Shop Machinery","MW Vol. 08 No. 6 Dec 1995-Jan 1996","22"
    "A Milling Machine Vertical Power Feed","W. A. Lincoln","Machining Accessories","MW Vol. 08 No. 6 Dec 1995-Jan 1996","26"
    "Adjustable Angle Plate","Fred Geisler","Measuring & Layout","MW Vol. 08 No. 6 Dec 1995-Jan 1996","34"
    "The Gunsmith Machinist: Custom Bolt Handle","Steve Acker","Gunsmithing","MW Vol. 08 No. 6 Dec 1995-Jan 1996","36"
    "Methods for Success: Indicating & Picking Up - Part IV","James Madison","Miscellaneous","MW Vol. 08 No. 6 Dec 1995-Jan 1996","38"
    "An Unusual Power Drive","Robert W. Metze","Tips & Tricks","MW Vol. 08 No. 6 Dec 1995-Jan 1996","40"
    "Cutting Oil","John G. Korman","Tips & Tricks","MW Vol. 08 No. 6 Dec 1995-Jan 1996","42"
    "Machinery Covers","Michael Johns","Tips & Tricks","MW Vol. 08 No. 6 Dec 1995-Jan 1996","42"
    "A Quick Rust Inhibiting Finish for Ferrous Parts","Michael Johns","Techniques","MW Vol. 08 No. 6 Dec 1995-Jan 1996","42"
    "Atkinson Cycle Engine","Arnold L. Teague","Engines","MW Vol. 09 No. 1 Feb-Mar 1996","4"
    "Locking Pliers Jerk Puller","Arthur Crow","Hand Tools","MW Vol. 09 No. 1 Feb-Mar 1996","23"
    "A Fine Downfeed for the Jet Mill/drill","James G. Tumelson","Machining Accessories","MW Vol. 09 No. 1 Feb-Mar 1996","26"
    "Electrical Phase Converter for Shop Motors","Robert W. Evans","Motors","MW Vol. 09 No. 1 Feb-Mar 1996","28"
    "Turn Scrap Into Workstands","David F. Crosby","Shop Accessories","MW Vol. 09 No. 1 Feb-Mar 1996","32"
    "The Gunsmith Machinist: A Fixture for Milling the Recoil Lug","Steve Acker","Gunsmithing","MW Vol. 09 No. 1 Feb-Mar 1996","34"
    "Wisdom in Technique Saves Time and Money","James Madison","Techniques","MW Vol. 09 No. 1 Feb-Mar 1996","36"
    "Model Maker's Pipe Tap and Die","John A. Cooper","Tips & Tricks","MW Vol. 09 No. 1 Feb-Mar 1996","41"
    "A Drill Press Modification","H. T. Biddle","Tips & Tricks","MW Vol. 09 No. 1 Feb-Mar 1996","42"
    "Jaws","L. Gill","Tips & Tricks","MW Vol. 09 No. 1 Feb-Mar 1996","42"
    "Alternative to Layout Dye","Larry R. Thompson","Tips & Tricks","MW Vol. 09 No. 1 Feb-Mar 1996","43"
    "A Freedom Tripod Head","Glenn L. Wilson","Hobby Items","MW Vol. 09 No. 2 Apr-May 1996","4"
    "Hole Locating","Lowie L. Roscoe, Jr.","Measuring & Layout","MW Vol. 09 No. 2 Apr-May 1996","10"
    "Hand Mill Restoration","James D. Scharplaz, P.E.","Machining Accessories","MW Vol. 09 No. 2 Apr-May 1996","14"
    "Turning Long Tapers Using a Boring Head","D. E. Johnson","Techniques","MW Vol. 09 No. 2 Apr-May 1996","16"
    "Lathe Bit Grinding Jig","Arthur W. Keely","Machining Accessories","MW Vol. 09 No. 2 Apr-May 1996","19"
    "A Simple Lathe Mill","Charlie R. Foster","Machining Accessories","MW Vol. 09 No. 2 Apr-May 1996","22"
    "Keyway Shaping - A Lathe Attachment","Malcom K. Leafe","Machining Accessories","MW Vol. 09 No. 2 Apr-May 1996","25"
    "An R8 Lathe Collet Holder","H. T. Biddle","Machining Accessories","MW Vol. 09 No. 2 Apr-May 1996","30"
    "Lathe Alignment","Robert Huffaker","Techniques","MW Vol. 09 No. 2 Apr-May 1996","31"
    "Smooth Handles","Howard W. Evers","Techniques","MW Vol. 09 No. 2 Apr-May 1996","34"
    "Saving Some Pinched Fingers","Jay E. Wulff","Techniques","MW Vol. 09 No. 2 Apr-May 1996","35"
    "A Three-jaw Chuck Center","Robert L. Grady","Machining Accessories","MW Vol. 09 No. 2 Apr-May 1996","36"
    "Metric Thread Cutting With an Eight TPI Lead Screw","Arch Gibson","Techniques","MW Vol. 09 No. 2 Apr-May 1996","37"
    "The Gunsmith Machinist: Hammer Work","Steve Acker","Gunsmithing","MW Vol. 09 No. 2 Apr-May 1996","38"
    "Centering Lathe Tools","D. A. Drayson","Tips & Tricks","MW Vol. 09 No. 2 Apr-May 1996","40"
    "Tune in for a Touchdown","R.G. Sparber","Tips & Tricks","MW Vol. 09 No. 2 Apr-May 1996","42"
    "Jot it Down","Norm Wells","Tips & Tricks","MW Vol. 09 No. 2 Apr-May 1996","44"
    "Quenching Techniques","Ken Scharabok","Tips & Tricks","MW Vol. 09 No. 2 Apr-May 1996","44"
    "A Sand Blasting Cabinet","Michael Johns","Tips & Tricks","MW Vol. 09 No. 2 Apr-May 1996","44"
    "Swarf Picker","Burt Noble","Tips & Tricks","MW Vol. 09 No. 2 Apr-May 1996","44"
    "Threaded Chucks","Norman H. Bennett","Tips & Tricks","MW Vol. 09 No. 2 Apr-May 1996","44"
    "A Tool and Cutter Grinder","Derek Brooks","Machine Tools","MW Vol. 09 No. 3 Jun-Jul 1996","4"
    "A $50 Power Table Feed","H. Halligan","Machining Accessories","MW Vol. 09 No. 3 Jun-Jul 1996","20"
    "Tool Height Indicator for the Lathe","Phil Nyman","Measuring & Layout","MW Vol. 09 No. 3 Jun-Jul 1996","22"
    "A Set of Precision Balancing Ways","J. O. Barbour, Jr.","Shop Accessories","MW Vol. 09 No. 3 Jun-Jul 1996","30"
    "Anaerobic Adhesives for Machinery","John F. Kraemer","General Machining Knowledge","MW Vol. 09 No. 3 Jun-Jul 1996","32"
    "The Gunsmith Machinist: Cutting a Rifle Crown","Steve Acker","Gunsmithing","MW Vol. 09 No. 3 Jun-Jul 1996","36"
    "The Gunsmith Machinist: Cutting a Rifle Crown","Steve Acker","Gunsmithing","MW Vol. 09 No. 3 Jun-Jul 1996","36"
    "Methods for Success: Reamer Tips","James Madison","Techniques","MW Vol. 09 No. 3 Jun-Jul 1996","38"
    "Measuring Small Work","Thomas LaMance","Tips & Tricks","MW Vol. 09 No. 3 Jun-Jul 1996","40"
    "Fine Cuts","Thomas LaMance","Tips & Tricks","MW Vol. 09 No. 3 Jun-Jul 1996","41"
    "Hex Screw Stock","D. A. Drayson","Tips & Tricks","MW Vol. 09 No. 3 Jun-Jul 1996","41"
    "Using the Four-jaw Chuck","W. A. Lincoln","Techniques","MW Vol. 09 No. 3 Jun-Jul 1996","185"
    "Metric Thread Conversion","Lawrence Craig","Tips & Tricks","MW Vol. 09 No. 4 Aug-Sep 1996","3"
    "Ways and Means With Old Milling Machines","Terry Sexton","Techniques","MW Vol. 09 No. 4 Aug-Sep 1996","4"
    "Toolmakers' Buttons","D. E. Johnson","Workholding","MW Vol. 09 No. 4 Aug-Sep 1996","13"
    "Life With a Mill-drill","Marsh Collins","Techniques","MW Vol. 09 No. 4 Aug-Sep 1996","14"
    "Another Power Feed Drive for a Mill","Robert W. Metze","Mills","MW Vol. 09 No. 4 Aug-Sep 1996","19"
    "A Clutch for Your Lathe","Larry Vanduyn","Machining Accessories","MW Vol. 09 No. 4 Aug-Sep 1996","20"
    "A Keyseat Cutter for the Lathe","Don Hester","Machining Accessories","MW Vol. 09 No. 4 Aug-Sep 1996","28"
    "The Gunsmith Machinist: Enlarging the Ejection Port","Steve Acker","Gunsmithing","MW Vol. 09 No. 4 Aug-Sep 1996","32"
    "A Multi-boring Block for a 9 Enco Lathe","Al Sohl, Jr.","Machining Accessories","MW Vol. 09 No. 4 Aug-Sep 1996","34"
    "Spindle Clamps for Imported Mill-drills","Ralph T. Waters","Machining Accessories","MW Vol. 09 No. 4 Aug-Sep 1996","37"
    "A Low-cost Quick-change Tool Post","Mike Pileski","Machining Accessories","MW Vol. 09 No. 5 Oct-Nov 1996","4"
    "A Shadowgraph","Richard Butterick","Machining Accessories","MW Vol. 09 No. 5 Oct-Nov 1996","9"
    "A Homemade Wheel Balancer","Birk Petersen","Shop Machinery","MW Vol. 09 No. 5 Oct-Nov 1996","22"
    "Turning Tapers in the Lathe","Jim Reynolds","Techniques","MW Vol. 09 No. 5 Oct-Nov 1996","28"
    "A Vibrating Tap-buster Head","James Hesse","Machining Accessories","MW Vol. 09 No. 5 Oct-Nov 1996","30"
    "Methods for Success: Why a Layout? - Part I","James Madison","Measuring & Layout","MW Vol. 09 No. 5 Oct-Nov 1996","35"
    "The Gunsmith Machinist: Making a Dovetail Front Sight","Steve Acker","Gunsmithing","MW Vol. 09 No. 5 Oct-Nov 1996","40"
    "Magnetic Template","Dwight Kinzer","Tips & Tricks","MW Vol. 09 No. 5 Oct-Nov 1996","42"
    "Maintaining Files","Charles "Muzzy" Mazarr","Tips & Tricks","MW Vol. 09 No. 5 Oct-Nov 1996","42"
    "Lathe Spur Mandrel","Ken Reed","Tips & Tricks","MW Vol. 09 No. 5 Oct-Nov 1996","44"
    "Shims","R.G. Sparber","Tips & Tricks","MW Vol. 09 No. 5 Oct-Nov 1996","44"
    "Making Ball Handles - A New Approach","W. A. Lincoln","Machining Accessories","MW Vol. 09 No. 6 Dec 1996-Jan 1997","4"
    "Workholding in an Asian Mill-drill","Richard Wright","Workholding","MW Vol. 09 No. 6 Dec 1996-Jan 1997","11"
    "Zappo the Swarf Lifter","Terry Sexton","Machining Accessories","MW Vol. 09 No. 6 Dec 1996-Jan 1997","12"
    "A Tapper","Jay Bolante","Hand Tools","MW Vol. 09 No. 6 Dec 1996-Jan 1997","16"
    "Multi-patterns - Economy in Numbers","D. A. Drayson","Measuring & Layout","MW Vol. 09 No. 6 Dec 1996-Jan 1997","18"
    "For Unobstructed Milling, Keep a Low Profile","John A. Cooper","Machining Accessories","MW Vol. 09 No. 6 Dec 1996-Jan 1997","20"
    "Measuring Angles","Horst Meister","Measuring & Layout","MW Vol. 09 No. 6 Dec 1996-Jan 1997","22"
    "One Thing Leads to Another","William Rollin Edwards","Techniques","MW Vol. 09 No. 6 Dec 1996-Jan 1997","29"
    "The Gunsmith Machinist: Sight Holding Fixtures","Steve Acker","Gunsmithing","MW Vol. 09 No. 6 Dec 1996-Jan 1997","32"
    "Methods for Success: Why a Layout? - Part II","James Madison","Measuring & Layout","MW Vol. 09 No. 6 Dec 1996-Jan 1997","34"
    "Bridgeport Adapter Plate","Eric A. Schultz","Tips & Tricks","MW Vol. 09 No. 6 Dec 1996-Jan 1997","40"
    "A Home Designed & Built Power Table Drive for a Mill-drill Machine","John A. Cooper","Machining Accessories","MW Vol. 10 No. 1 Feb-Mar 1997","4"
    "Spindle Oscillator for Sanding and Honing","Fran O. Mueller","Machining Accessories","MW Vol. 10 No. 1 Feb-Mar 1997","12"
    "A Tool Block Carousel","Mike Pileski","Machining Accessories","MW Vol. 10 No. 1 Feb-Mar 1997","27"
    "Methods for Success: Why a Layout? - Part III","James Madison","Measuring & Layout","MW Vol. 10 No. 1 Feb-Mar 1997","30"
    "The Gunsmith Machinist: Installing a Front Sight","Steve Acker","Gunsmithing","MW Vol. 10 No. 1 Feb-Mar 1997","34"
    "Raising Work","Burt Noble","Tips & Tricks","MW Vol. 10 No. 1 Feb-Mar 1997","44"
    "A Handy Graduating Tool","Terry Sexton","Shop Accessories","MW Vol. 10 No. 2 Apr-May 1997","4"
    "A Simple Stepper-motor Driver","C. A. Hoover","Motors","MW Vol. 10 No. 2 Apr-May 1997","12"
    "Construction of Pottery Kilns (Heat-treat Furnaces)","James Hesse","Welding/Foundry/Forging","MW Vol. 10 No. 2 Apr-May 1997","16"
    "An Unorthodox Spur Gear","Mike Hoff","Machining Accessories","MW Vol. 10 No. 2 Apr-May 1997","24"
    "A Second Lease on Life","Robert Leuck","Shop Accessories","MW Vol. 10 No. 2 Apr-May 1997","27"
    "Zap an Import - Build It Yourself","J. O. Barbour, Jr.","Techniques","MW Vol. 10 No. 2 Apr-May 1997","30"
    "A Simple Way to Measure Inside Diameters","R.G. Sparber","Measuring & Layout","MW Vol. 10 No. 2 Apr-May 1997","32"
    "Dating Old Metalworking Machinery","Dana Martin Batory","Techniques","MW Vol. 10 No. 2 Apr-May 1997","33"
    "The Gunsmith Machinist: Moving a Firing Pin Hole","Steve Acker","Gunsmithing","MW Vol. 10 No. 2 Apr-May 1997","34"
    "Forming Scale Bolts and Nuts on the Lathe","Mike Hoff","Techniques","MW Vol. 10 No. 3 Jun-Jul 1997","4"
    "A Simple Indexing Attachment for Your Lathe","Don Titus","Machining Accessories","MW Vol. 10 No. 3 Jun-Jul 1997","11"
    "A Magnetic Base","Jack R. Thompson","Machining Accessories","MW Vol. 10 No. 3 Jun-Jul 1997","14"
    "A Quick-release Tailstock Lock for Small Lathes","Steve Govus","Machining Accessories","MW Vol. 10 No. 3 Jun-Jul 1997","20"
    "Carbide Cutting Tools for the Lathe","Brian Bratvold","Machining Accessories","MW Vol. 10 No. 3 Jun-Jul 1997","21"
    "Inertia Welding","James Hesse","Welding/Foundry/Forging","MW Vol. 10 No. 3 Jun-Jul 1997","28"
    "A Lamp Base for the Shadowgraph","Richard Butterick","Machining Accessories","MW Vol. 10 No. 3 Jun-Jul 1997","32"
    "Methods for Success: Edge Gage","James Madison","Techniques","MW Vol. 10 No. 3 Jun-Jul 1997","33"
    "The Gunsmith Machinist: Trigger Job Pins","Steve Acker","Gunsmithing","MW Vol. 10 No. 3 Jun-Jul 1997","36"
    "A Milling Attachment for a Small Lathe","Jim Reynolds","Machining Accessories","MW Vol. 10 No. 4 Aug-Sep 1997","4"
    "Arbor Press","H. Irvin","Shop Machinery","MW Vol. 10 No. 4 Aug-Sep 1997","12"
    "An X, Y Stage for the Home Constructor","Richard Butterick","Machining Accessories","MW Vol. 10 No. 4 Aug-Sep 1997","14"
    "A Mathematical Approach to Knurling","Robert Koval","Techniques","MW Vol. 10 No. 4 Aug-Sep 1997","22"
    "A Quick-change Tool Post","Donald Dobias","Machining Accessories","MW Vol. 10 No. 4 Aug-Sep 1997","24"
    "Equipment Lights","Paul J. Holm","Machining Accessories","MW Vol. 10 No. 4 Aug-Sep 1997","26"
    "Follower Rest","Paul J. Holm","Machining Accessories","MW Vol. 10 No. 4 Aug-Sep 1997","26"
    "Lemon Squeezer","Robert W. Metze","Machining Accessories","MW Vol. 10 No. 4 Aug-Sep 1997","27"
    "Milling Head Alignment Wheel","Norman E. Johnson","Machining Accessories","MW Vol. 10 No. 4 Aug-Sep 1997","28"
    "Drilling Holes in Hard Material","Robert W. Metze","Techniques","MW Vol. 10 No. 4 Aug-Sep 1997","29"
    "An Edge Finder","R.G. Sparber","Shop Accessories","MW Vol. 10 No. 4 Aug-Sep 1997","30"
    "A Gasket in a Hurry","Herb Baehre","Tips & Tricks","MW Vol. 10 No. 4 Aug-Sep 1997","31"
    "A Magnetic Back for a Dial Indicator","Donovan V. Browne","Machining Accessories","MW Vol. 10 No. 4 Aug-Sep 1997","31"
    "The Gunsmith Machinist: Making Rifle Bedding Pillars","Steve Acker","Gunsmithing","MW Vol. 10 No. 4 Aug-Sep 1997","32"
    "Methods for Success: Shop Equipment for Fixture Building","James Madison","Shop Accessories","MW Vol. 10 No. 4 Aug-Sep 1997","34"
    "Protecting Threads","Thomas LaMance","Techniques","MW Vol. 10 No. 5 Oct-Nov 1997","3"
    "Tidy Lathe Chuck Storage","Donovan V. Browne","Tips & Tricks","MW Vol. 10 No. 5 Oct-Nov 1997","3"
    "A Dividing Head for the Taig (Taig/Peatol) Lathe","Tony Jeffree","Machining Accessories","MW Vol. 10 No. 5 Oct-Nov 1997","4"
    "Lathe Index and Crank","Norman Letzring","Machining Accessories","MW Vol. 10 No. 5 Oct-Nov 1997","16"
    "Tapping Station","Mike Pileski","Shop Accessories","MW Vol. 10 No. 5 Oct-Nov 1997","22"
    "Quick Quill Stop","Roger Claude","Machining Accessories","MW Vol. 10 No. 5 Oct-Nov 1997","26"
    "A Simple Punch Guide","William R. Johnson","Hand Tools","MW Vol. 10 No. 5 Oct-Nov 1997","29"
    "Methods for Success: The Move Was Right, Why Isn't It There?","James Madison","Techniques","MW Vol. 10 No. 5 Oct-Nov 1997","30"
    "The Gunsmith Machinist: A Gunsmith's Lathe Helper","Steve Acker","Gunsmithing","MW Vol. 10 No. 5 Oct-Nov 1997","34"
    "Keeping Track of the Chuck Wrench","Thomas LaMance","Tips & Tricks","MW Vol. 10 No. 5 Oct-Nov 1997","44"
    "A Micro Drill Press","Pat Loop","Machine Tools","MW Vol. 10 No. 6 Dec 1997-Jan 1998","4"
    "The Novice Adds Some Stops to His Sherline Mill","Charles T. Atkinson","Techniques","MW Vol. 10 No. 6 Dec 1997-Jan 1998","15"
    "How Healthy is Your Shop?","Wayne Hanson","General Machining Knowledge","MW Vol. 10 No. 6 Dec 1997-Jan 1998","18"
    "Accessories for a Unimat","James W. Hauser","Machining Accessories","MW Vol. 10 No. 6 Dec 1997-Jan 1998","24"
    "Random Orbital Sander","Arthur Crow","Shop Accessories","MW Vol. 10 No. 6 Dec 1997-Jan 1998","26"
    "The Gunsmith Machinist: Milling Grasping Grooves","Steve Acker","Gunsmithing","MW Vol. 10 No. 6 Dec 1997-Jan 1998","29"
    "Methods for Success: Tough Tools for Tough Machining Operations - Part I","James Madison","Machining Accessories","MW Vol. 10 No. 6 Dec 1997-Jan 1998","32"
    "Holding Adjustable Centers","Thomas LaMance","Tips & Tricks","MW Vol. 10 No. 6 Dec 1997-Jan 1998","44"
    "Building a Rack Cutting Attachment","Terry Sexton","Machining Accessories","MW Vol. 11 No. 1 Feb-Mar 1998","4"
    "Mill/drill Power Feed","Fred V. Patterson","Machining Accessories","MW Vol. 11 No. 1 Feb-Mar 1998","13"
    "Rear Tool Post (Reversible) for Atlas or Craftsman 6 Swing Lathes","John B. Gascoyne","Machining Accessories","MW Vol. 11 No. 1 Feb-Mar 1998","14"
    "Update and Improvements for the Craftsman 109 Series Lathe","Lionel Weightman","Techniques","MW Vol. 11 No. 1 Feb-Mar 1998","18"
    "The Gunsmith Machinist: Drilling and Tapping for Scope Mounts","Steve Acker","Gunsmithing","MW Vol. 11 No. 1 Feb-Mar 1998","28"
    "Quick-change Indicator Holder","Howard W. Evers","Machining Accessories","MW Vol. 11 No. 1 Feb-Mar 1998","31"
    "Spindle Motor Reverse","James Rayhel","Tips & Tricks","MW Vol. 11 No. 1 Feb-Mar 1998","31"
    "Methods for Success: Turning Tools for Tough Materials","James Madison","Machining Accessories","MW Vol. 11 No. 1 Feb-Mar 1998","32"
    "Ready Ink Applicator","Thomas LaMance","Tips & Tricks","MW Vol. 11 No. 1 Feb-Mar 1998","40"
    "Sawfeed","Jim Reynolds","Machining Accessories","MW Vol. 11 No. 2 Apr-May 1998","4"
    "Mill-drill Improvements","V. L. Ridenour","Tips & Tricks","MW Vol. 11 No. 2 Apr-May 1998","9"
    "Building Your Own Collet Chuck","William B. Dochterman","Machining Accessories","MW Vol. 11 No. 2 Apr-May 1998","10"
    "Die Maker Buttons","Jack R. Thompson","Machining Accessories","MW Vol. 11 No. 2 Apr-May 1998","16"
    "Automatic Carriage Stop for a 6 Atlas Lathe","Edward Badger","Machining Accessories","MW Vol. 11 No. 2 Apr-May 1998","20"
    "The $20 Drip Coolant System","Peter Nolan","Machining Accessories","MW Vol. 11 No. 2 Apr-May 1998","24"
    "An Adjustable Cross-slide Nut","Eugene E. Petersen","Machining Accessories","MW Vol. 11 No. 2 Apr-May 1998","27"
    "Rong Fu Headlock","Howard W. Evers","Machining Accessories","MW Vol. 11 No. 2 Apr-May 1998","28"
    "Fixture to Hold Small Pieces","Ray Hasbrouck","Workholding","MW Vol. 11 No. 2 Apr-May 1998","30"
    "A Tool Post Grinder","Wayne Hanson","Machining Accessories","MW Vol. 11 No. 2 Apr-May 1998","32"
    "The Gunsmith Machinist: Centering a Barrel Bore","Steve Acker","Gunsmithing","MW Vol. 11 No. 2 Apr-May 1998","34"
    "Make a Tap Center","Peter M. Hallward","Machining Accessories","MW Vol. 11 No. 2 Apr-May 1998","36"
    "Power Drive for Lathe Chucks","F. D. Southwick","Machining Accessories","MW Vol. 11 No. 2 Apr-May 1998","37"
    "Work With Morse Tapers","Bernard L. Rosen","Tips & Tricks","MW Vol. 11 No. 2 Apr-May 1998","37"
    "A Riveting Press","Birk Petersen","Shop Machinery","MW Vol. 11 No. 3 Jun-Jul 1998","6"
    "Handy Shop Odds and Ends","Marsh Collins","Techniques","MW Vol. 11 No. 3 Jun-Jul 1998","11"
    "A Chuck Lifter","John L. Staiger, Jr.","Machining Accessories","MW Vol. 11 No. 3 Jun-Jul 1998","16"
    "A 36" Brake","James S. McKnight","Shop Machinery","MW Vol. 11 No. 3 Jun-Jul 1998","24"
    "Getting a New Vise in Shape","Peter Nolan","Techniques","MW Vol. 11 No. 3 Jun-Jul 1998","28"
    "The Multi-Purpose Machine","Donovan V. Browne","Hobby Community","MW Vol. 11 No. 3 Jun-Jul 1998","33"
    "Adding Muscle to Your 9 x 20 Bench Lathe","Richard Chlapecka","Machining Accessories","MW Vol. 11 No. 3 Jun-Jul 1998","36"
    "A Direct Reading SFPM Adapter for the Common Speed Indicator","Ken Hemmelgarn","Shop Accessories","MW Vol. 11 No. 3 Jun-Jul 1998","38"
    "Build Your Own Geared Rotary Table - Part I","Marsh Collins","Machining Accessories","MW Vol. 11 No. 4 Aug-Sep 1998","6"
    "The Universal Lamp","J. W. (Bill) Reichart","Machining Accessories","MW Vol. 11 No. 4 Aug-Sep 1998","16"
    "Improved Tooling for Threading and Boring with the Unimat DB200 Lathe","Theodore M. Clarke","Techniques","MW Vol. 11 No. 4 Aug-Sep 1998","22"
    "Setting Up a Machine Shop in a Walkdown Basement","Bob MacFarlane","General Machining Knowledge","MW Vol. 11 No. 4 Aug-Sep 1998","26"
    "Expanding Mandrels","James DeLong","Machining Accessories","MW Vol. 11 No. 4 Aug-Sep 1998","31"
    "Build a Circle-cutting Attachment","Leonard Waring","Machining Accessories","MW Vol. 11 No. 4 Aug-Sep 1998","34"
    "The Gunsmith Machinist: Cutting Rifle Barrel Threads","Steve Acker","Gunsmithing","MW Vol. 11 No. 4 Aug-Sep 1998","37"
    "Leaner's Notes","Guy Lautard","Tips & Tricks","MW Vol. 11 No. 4 Aug-Sep 1998","39"
    "A Low-tech Edge Finder","D. A. Drayson","Tips & Tricks","MW Vol. 11 No. 4 Aug-Sep 1998","40"
    "An Index with R8 Collets","John A. Cooper","Machining Accessories","MW Vol. 11 No. 5 Oct-Nov 1998","4"
    "Belt Sander","James S. McKnight","Shop Machinery","MW Vol. 11 No. 5 Oct-Nov 1998","17"
    "Making a Small Split Collar","Paul J. Holm","Machining Accessories","MW Vol. 11 No. 5 Oct-Nov 1998","20"
    "From Pain to Pleasure","Chuck Plotkin","Techniques","MW Vol. 11 No. 5 Oct-Nov 1998","25"
    "Build Your Own Geared Rotary Table - Part II","Marsh Collins","Machining Accessories","MW Vol. 11 No. 5 Oct-Nov 1998","28"
    "A Metal Lathe Mount for a Laminate Trimmer","Dana Martin Batory","Machining Accessories","MW Vol. 11 No. 5 Oct-Nov 1998","36"
    "Two Tools for Shop Angle Measurements","Don Peterson","Measuring & Layout","MW Vol. 11 No. 5 Oct-Nov 1998","38"
    "The Gunsmith Machinist: Chambering a Rifle Barrel","Steve Acker","Gunsmithing","MW Vol. 11 No. 5 Oct-Nov 1998","41"
    "A Word for Loctite","Jon Klasna","General Machining Knowledge","MW Vol. 11 No. 5 Oct-Nov 1998","44"
    "Another Way to Turn Offset Diameters","Fred Bruce","Techniques","MW Vol. 11 No. 5 Oct-Nov 1998","47"
    "Single-phase to Three-phase Plus Speed Control","Charles Eyer","Miscellaneous","MW Vol. 11 No. 6 Dec 1998-Jan 1999","6"
    "Making Gears Using a Hob","Donald Dobias","Techniques","MW Vol. 11 No. 6 Dec 1998-Jan 1999","13"
    "The Helix Gear Hobbing Machine","Terry Sexton","Shop Machinery","MW Vol. 11 No. 6 Dec 1998-Jan 1999","20"
    "Using the Milling Machine as a Copy Stand","Forest N. Baker","Techniques","MW Vol. 11 No. 6 Dec 1998-Jan 1999","24"
    "Variable Frequency Drive Applications","R. W. O'Brian","Motors","MW Vol. 11 No. 6 Dec 1998-Jan 1999","26"
    "A Claytons Change Wheel","Terry Sexton","Machining Accessories","MW Vol. 11 No. 6 Dec 1998-Jan 1999","29"
    "Taiwan Lathe Problems","James Hesse","Techniques","MW Vol. 11 No. 6 Dec 1998-Jan 1999","30"
    "A Cut-rate Machinist's Level","Jack R. Thompson","Machining Accessories","MW Vol. 11 No. 6 Dec 1998-Jan 1999","33"
    "Improving the Lathe Steady Rest","Norman E. Johnson","Techniques","MW Vol. 11 No. 6 Dec 1998-Jan 1999","34"
    "Indicating a Bridgeport Head","Joseph P. Howard","Techniques","MW Vol. 11 No. 6 Dec 1998-Jan 1999","35"
    "The Gunsmith Machinist: A Barrel Vise","Steve Acker","Gunsmithing","MW Vol. 11 No. 6 Dec 1998-Jan 1999","36"
    "Reversing Rotation on a Single Split-phase Motor","Joseph Zumwaldt","Motors","MW Vol. 11 No. 6 Dec 1998-Jan 1999","38"
    "Improvements to the Vertical/horizontal Cutoff Saw","Norm Wells","Techniques","MW Vol. 11 No. 6 Dec 1998-Jan 1999","40"
    "Removable Tie-down","Dwight Kinzer","Tips & Tricks","MW Vol. 11 No. 6 Dec 1998-Jan 1999","41"
    "Tourist Bar","James W. Hauser","Tips & Tricks","MW Vol. 11 No. 6 Dec 1998-Jan 1999","48"
    "Rotary Indexing Fixture","Fred Geisler","Machining Accessories","MW Vol. 12 No. 1 Feb-Mar 1999","4"
    "A Real Do-it-yourself Threading Dial","Ted Winiecki","Machining Accessories","MW Vol. 12 No. 1 Feb-Mar 1999","10"
    "Customizing an Imported Drill Press","Glenn L. Wilson","Techniques","MW Vol. 12 No. 1 Feb-Mar 1999","15"
    "Lathe Chuck Adaptations","Lowell P. Braxton","Machining Accessories","MW Vol. 12 No. 1 Feb-Mar 1999","20"
    "Mill-drill Installation","D. A. Drayson","Techniques","MW Vol. 12 No. 1 Feb-Mar 1999","24"
    "A Lathe-center Step-up Cone","Norman E. Johnson","Machining Accessories","MW Vol. 12 No. 1 Feb-Mar 1999","26"
    "A Free-standing Lathe Toolholder","Ludwig Schweinfurth","Machining Accessories","MW Vol. 12 No. 1 Feb-Mar 1999","28"
    "Build a Working Cannon","Paul J. Holm","Hobby Items","MW Vol. 12 No. 1 Feb-Mar 1999","30"
    "A Round Stock Welding Jig","James DeLong","Welding/Foundry/Forging","MW Vol. 12 No. 1 Feb-Mar 1999","35"
    "Two Useful Charts","Karl R. Brown","General Machining Knowledge","MW Vol. 12 No. 1 Feb-Mar 1999","36"
    "The Gunsmith Machinist: A Rear Sight Shifter","Steve Acker","Gunsmithing","MW Vol. 12 No. 1 Feb-Mar 1999","38"
    "The Tool Room: Modelmaker's Vise","James W. Hauser","Shop Accessories","MW Vol. 12 No. 1 Feb-Mar 1999","40"
    "Wooden Mats","James W. Hauser","Shop Accessories","MW Vol. 12 No. 1 Feb-Mar 1999","41"
    "The Amateur Machinist: A Lathe Bench","Barry Young","Shop Accessories","MW Vol. 12 No. 1 Feb-Mar 1999","42"
    "Sine of the Times","Marvin W. Klotz","Tips & Tricks","MW Vol. 12 No. 1 Feb-Mar 1999","45"
    "Gear Cutting Adventures - Part I: Spur Gears and Pinions","John A. Cooper","Techniques","MW Vol. 12 No. 2 Apr-May 1999","8"
    "Micro Adjustable Bow Sight","Don Titus","Hobby Items","MW Vol. 12 No. 2 Apr-May 1999","16"
    "Make A Wiggler","Billy J. Blackmon","Machining Accessories","MW Vol. 12 No. 2 Apr-May 1999","22"
    "An Affordable Mill-drill Power Drive - Part I","Edwin Cox","Machining Accessories","MW Vol. 12 No. 2 Apr-May 1999","24"
    "The Gunsmith Machinist: Replacing an Integral Front Sight","Steve Acker","Gunsmithing","MW Vol. 12 No. 2 Apr-May 1999","35"
    "The Sakai ML-360","Marios M. Lioufis","Hobby Community","MW Vol. 12 No. 2 Apr-May 1999","38"
    "The Amateur Machinist: Readying the Lathe for Work","Barry Young","Techniques","MW Vol. 12 No. 2 Apr-May 1999","42"
    "The Tool Room: Clutch Guard for a Bridgeport Model J Head","James W. Hauser","Machining Accessories","MW Vol. 12 No. 2 Apr-May 1999","45"
    "Dog Work","Thomas LaMance","Tips & Tricks","MW Vol. 12 No. 3 Jun-Jul 1999","10"
    "Relocating Work","Thomas LaMance","Tips & Tricks","MW Vol. 12 No. 3 Jun-Jul 1999","10"
    "Experimental Helical Milling Attachment","Terry Sexton","Machining Accessories","MW Vol. 12 No. 3 Jun-Jul 1999","12"
    "The Ross Box","Terry Coss","Hobby Items","MW Vol. 12 No. 3 Jun-Jul 1999","18"
    "Gear Cutting Adventures - Part II: Helical Gears","John A. Cooper","Techniques","MW Vol. 12 No. 3 Jun-Jul 1999","23"
    "An Affordable Mill-drill Power Drive - Part II","Edwin Cox","Machining Accessories","MW Vol. 12 No. 3 Jun-Jul 1999","28"
    "Shoot a Best for the Least","Robert L. Egbert","Gunsmithing","MW Vol. 12 No. 3 Jun-Jul 1999","34"
    "Round Keys Reduce Fatigue Failures","J. W. Straight","Machining Accessories","MW Vol. 12 No. 3 Jun-Jul 1999","37"
    "A Drill Guide Device for the Atlas/Craftsman 6 Lathe","Jim Reynolds","Machining Accessories","MW Vol. 12 No. 3 Jun-Jul 1999","38"
    "A Quickie Reamer","Mike Hoff","Hand Tools","MW Vol. 12 No. 3 Jun-Jul 1999","41"
    "Simple Estimating of Variable Motor Speeds","Chuck Plotkin","Motors","MW Vol. 12 No. 3 Jun-Jul 1999","42"
    "The Amateur Machinist: First Project - A Knockout Bar","Barry Young","Machining Accessories","MW Vol. 12 No. 3 Jun-Jul 1999","46"
    "The Gunsmith Machinist: Optimizing Revolver Throats","Steve Acker","Gunsmithing","MW Vol. 12 No. 3 Jun-Jul 1999","48"
    "A Gear-cutting Device","Jim Reynolds","Machining Accessories","MW Vol. 12 No. 4 Aug-Sep 1999","8"
    "A Pop Can Crusher","Birk Petersen","Hobby Items","MW Vol. 12 No. 4 Aug-Sep 1999","13"
    "Flute Your Own Rifle Barrel","Norman E. Johnson","Gunsmithing","MW Vol. 12 No. 4 Aug-Sep 1999","26"
    "CBX System DRO by Shooting Star Technology","Dirk Tollenaar","Hobby Community","MW Vol. 12 No. 4 Aug-Sep 1999","28"
    "An Affordable Mill-drill Power Drive - Part III","Edwin Cox","Machining Accessories","MW Vol. 12 No. 4 Aug-Sep 1999","32"
    "The Gunsmith Machinist: Installing a Locking Base Pin","Steve Acker","Gunsmithing","MW Vol. 12 No. 4 Aug-Sep 1999","38"
    "Sine Plate","James S. McKnight","Machining Accessories","MW Vol. 12 No. 4 Aug-Sep 1999","40"
    "The Tool Room: Jaw Boxes","James W. Hauser","Shop Accessories","MW Vol. 12 No. 4 Aug-Sep 1999","45"
    "A Cure for Head-banging","","Miscellaneous","MW Vol. 12 No. 4 Aug-Sep 1999","46"
    "The Amateur Machinist: Center Knocker Refinements","Barry Young","Techniques","MW Vol. 12 No. 4 Aug-Sep 1999","47"
    "Better Boring Bars","Thomas LaMance","Tips & Tricks","MW Vol. 12 No. 4 Aug-Sep 1999","58"
    "Metal Spinning Lubricant","Thomas LaMance","Tips & Tricks","MW Vol. 12 No. 4 Aug-Sep 1999","58"
    "A Special Scoop","Thomas LaMance","Tips & Tricks","MW Vol. 12 No. 4 Aug-Sep 1999","58"
    "Mill-drill Lubrication Upgrade","Dennis A. Armstrong","Machine Modifications","MW Vol. 12 No. 5 Oct-Nov 1999","8"
    "A Simple Indicator Mount for a Lathe","James C. Robertson","Machining Accessories","MW Vol. 12 No. 5 Oct-Nov 1999","15"
    "A Polishing and Utility Lathe","Mike Hoff","Machine Tools","MW Vol. 12 No. 5 Oct-Nov 1999","18"
    "Taig Micro Mill","Herman Ross","Hobby Community","MW Vol. 12 No. 5 Oct-Nov 1999","27"
    "An Affordable Mill-drill Power Drive - Part IV","Edwin Cox","Machining Accessories","MW Vol. 12 No. 5 Oct-Nov 1999","30"
    "C&D Grinder Stand","Chuck Plotkin","Machining Accessories","MW Vol. 12 No. 5 Oct-Nov 1999","38"
    "A Spring and Coil Winder","Glenn L. Wilson","Shop Accessories","MW Vol. 12 No. 5 Oct-Nov 1999","40"
    "Feed and Speed Calculator","Brian Rosenthal","General Machining Knowledge","MW Vol. 12 No. 5 Oct-Nov 1999","43"
    "A Child's Lock","Robert Tata","Hobby Items","MW Vol. 12 No. 5 Oct-Nov 1999","46"
    "The Gunsmith Machinist: Finding and Making Gun Parts","Steve Acker","Gunsmithing","MW Vol. 12 No. 5 Oct-Nov 1999","48"
    "The Tool Room: Drill Press Table Holding Devices","James W. Hauser","Machining Accessories","MW Vol. 12 No. 5 Oct-Nov 1999","50"
    "Dead On, Dead Center +/- .001","Howard W. Evers","Techniques","MW Vol. 12 No. 5 Oct-Nov 1999","51"
    "The Amateur Machinist: Speeds and Feeds","Barry Young","General Machining Knowledge","MW Vol. 12 No. 5 Oct-Nov 1999","52"
    "Another Viewpoint","Thomas LaMance","Tips & Tricks","MW Vol. 12 No. 5 Oct-Nov 1999","55"
    "An Automated Coolant Applicator","Glenn L. Wilson","Machining Accessories","MW Vol. 12 No. 6 Dec 1999-Jan 2000","8"
    "Chambering a Rifle Barrel for Accuracy","Randolph Constantine","Gunsmithing","MW Vol. 12 No. 6 Dec 1999-Jan 2000","13"
    "A Band Saw Base","Pierre Massicotte","Machine Tools","MW Vol. 12 No. 6 Dec 1999-Jan 2000","18"
    "The Tool Room: A 1 Reverse Arbor","James W. Hauser","Miscellaneous","MW Vol. 12 No. 6 Dec 1999-Jan 2000","18"
    "A Cyclone Dust Collector","James Hesse","Machining Accessories","MW Vol. 12 No. 6 Dec 1999-Jan 2000","32"
    "Band Saw Alignment Tool","James D. Piazza","Machining Accessories","MW Vol. 12 No. 6 Dec 1999-Jan 2000","38"
    "The Gunsmith Machinist: Stronger Scope Installation","Steve Acker","Gunsmithing","MW Vol. 12 No. 6 Dec 1999-Jan 2000","40"
    "The Amateur Machinist: A Back Tool Post","Barry Young","Machining Accessories","MW Vol. 12 No. 6 Dec 1999-Jan 2000","44"
    "Soft Jaws Hold Small Cylinders","Arthur Lee","Techniques","MW Vol. 12 No. 6 Dec 1999-Jan 2000","47"
    "An Affordable Mill-drill Power Drive - Part V","Edwin Cox","Machining Accessories","MW Vol. 12 No. 6 Dec 1999-Jan 2000","48"
    "The Robbins and Lawrence Legacy - Proven Interchangeability","Bill McCarthy","Techniques","MW Vol. 12 No. 6 Dec 1999-Jan 2000","53"
    "Shuffle-Easy Card Shuffler","Donald R. Oswald","Hobby Items","MW Vol. 13 No. 1 Feb-Mar 2000","8"
    "Lathe Cross Slide Attachments","Peter F. Lott","Machining Accessories","MW Vol. 13 No. 1 Feb-Mar 2000","15"
    "Bringing the Craftsman Model 80 Metal-turning Lathe Into the 21st Century","Frank Beafore","Techniques","MW Vol. 13 No. 1 Feb-Mar 2000","20"
    "A Cast Gunmetal Pump Rod","Terry Sexton","Machining Accessories","MW Vol. 13 No. 1 Feb-Mar 2000","26"
    "Measure Gear Teeth With a Caliper","W. A. Lincoln","Techniques","MW Vol. 13 No. 1 Feb-Mar 2000","32"
    "An Affordable Mill-drill Power Drive - Part VI","Edwin Cox","Machining Accessories","MW Vol. 13 No. 1 Feb-Mar 2000","34"
    "Making Case - Forming Tools and Forming Cases for a 7.62 mm Russian Nagant Revolver","Lowell P. Braxton","Gunsmithing","MW Vol. 13 No. 1 Feb-Mar 2000","37"
    "The Tool Room: A Collet Stop Extension","James W. Hauser","Machining Accessories","MW Vol. 13 No. 1 Feb-Mar 2000","42"
    "The Gunsmith Machinist: An Unusual Scope Mount","Steve Acker","Gunsmithing","MW Vol. 13 No. 1 Feb-Mar 2000","43"
    "An Auxiliary Toolholder for the Sherline Boring Head","Dann E. Rinsma","Machining Accessories","MW Vol. 13 No. 1 Feb-Mar 2000","46"
    "Tyro's First Lathe - Part I","Jim Swartz","Techniques","MW Vol. 13 No. 1 Feb-Mar 2000","47"
    "The Amateur Machinist: Self-feed Equipment","Barry Young","Machining Accessories","MW Vol. 13 No. 1 Feb-Mar 2000","49"
    "A Simple Shortcut","Thomas LaMance","Tips & Tricks","MW Vol. 13 No. 1 Feb-Mar 2000","56"
    "An Index Head For the Sherline Lathe/Mill - Part I","Milo W. Bresley","Machining Accessories","MW Vol. 13 No. 2 Apr-May 2000","8"
    "Building a Stirling Cycle Hot Air Engine","Terry Coss","Engines","MW Vol. 13 No. 2 Apr-May 2000","18"
    "Build a Center-finding Center Punch","J. W. Straight","Machining Accessories","MW Vol. 13 No. 2 Apr-May 2000","25"
    "Cross-feed Nut","Thomas Morrison","Machining Accessories","MW Vol. 13 No. 2 Apr-May 2000","26"
    "Game Boards","Rodney W. Hanson","Hobby Items","MW Vol. 13 No. 2 Apr-May 2000","28"
    "A Gearless Transmission","Roger Claude","Shop Machinery","MW Vol. 13 No. 2 Apr-May 2000","33"
    "Baby Sampson and the Weld Wagon","Terry Sexton","Welding/Foundry/Forging","MW Vol. 13 No. 2 Apr-May 2000","34"
    "Build Your Own Anvil","Barry Dosdall","Machining Accessories","MW Vol. 13 No. 2 Apr-May 2000","40"
    "Dancing Master Calipers","Allen Weiss","Hand Tools","MW Vol. 13 No. 2 Apr-May 2000","42"
    "The Gunsmith Machinist: Installing a Screw-in Choke Adapter","Steve Acker","Gunsmithing","MW Vol. 13 No. 2 Apr-May 2000","44"
    "The Tool Room: Milling Machine Vise Stop","James W. Hauser","Mills","MW Vol. 13 No. 2 Apr-May 2000","49"
    "The Amateur Machinist: Cutting Screw Threads","Barry Young","Techniques","MW Vol. 13 No. 2 Apr-May 2000","50"
    "Re-sharpening Small Drills","Glenn L. Wilson","Techniques","MW Vol. 13 No. 2 Apr-May 2000","54"
    "The Unstuck Chuck","Walter Wiebe","Tips & Tricks","MW Vol. 13 No. 3 Jun-Jul 2000","6"
    "Toothless - Another Way to Turn a Wheel","Arnold L. Teague","Hobby Items","MW Vol. 13 No. 3 Jun-Jul 2000","8"
    "An Affordable Mill-drill Power Drive - Part VII","Edwin Cox","Machining Accessories","MW Vol. 13 No. 3 Jun-Jul 2000","19"
    "An Index Head For the Sherline Lathe/Mill - Part II","Milo W. Bresley","Machining Accessories","MW Vol. 13 No. 3 Jun-Jul 2000","24"
    "An Elliptical Turning Attachment","Michel Jacot","Machining Accessories","MW Vol. 13 No. 3 Jun-Jul 2000","36"
    "The Gunsmith Machinist: Manson Rifle Receiver Blueprinting Tools","Steve Acker","Hobby Community","MW Vol. 13 No. 3 Jun-Jul 2000","38"
    "A Primer On Welding","James C. Robertson","Welding/Foundry/Forging","MW Vol. 13 No. 3 Jun-Jul 2000","40"
    "Manual Numerical Control","R.G. Sparber","Computers","MW Vol. 13 No. 3 Jun-Jul 2000","43"
    "The Gunsmith Machinist: Removing a Broken Screw","Steve Acker","Gunsmithing","MW Vol. 13 No. 3 Jun-Jul 2000","47"
    "The Amateur Machinist: Cover Your Machine","Barry Young","Techniques","MW Vol. 13 No. 3 Jun-Jul 2000","50"
    "Making Parallels Work","Marshall Damerell","Tips & Tricks","MW Vol. 13 No. 3 Jun-Jul 2000","51"
    "The Tool Room: Railroad Lock Keys","James W. Hauser","Miscellaneous","MW Vol. 13 No. 3 Jun-Jul 2000","52"
    "Go Ahead, Make My Angle","William A. Johnson","Machining Accessories","MW Vol. 13 No. 4 Aug-Sep 2000","8"
    "Tyro's First Lathe - Part II","Jim Swartz","Techniques","MW Vol. 13 No. 4 Aug-Sep 2000","12"
    "Salvage Operations on a Mill-Drill Quill","Terry Sexton","Techniques","MW Vol. 13 No. 4 Aug-Sep 2000","16"
    "An Affordable Mill-drill Power Drive - Part VIII","Edwin Cox","Machining Accessories","MW Vol. 13 No. 4 Aug-Sep 2000","19"
    "An Index Head For the Sherline Lathe/Mill - Part III","Milo W. Bresley","Machining Accessories","MW Vol. 13 No. 4 Aug-Sep 2000","30"
    "The Gunsmith Machinist: Installing a Pre-threaded Short Chambered Rifle Barrel","Steve Acker","Gunsmithing","MW Vol. 13 No. 4 Aug-Sep 2000","44"
    "The Tool Room: Spring-loaded Tap Guide","James W. Hauser","Hand Tools","MW Vol. 13 No. 4 Aug-Sep 2000","51"
    "How to Make a Small Rubber Wheel (2 to 3 dia.) from a Hockey Puck","James R. Instone","Machining Accessories","MW Vol. 13 No. 4 Aug-Sep 2000","52"
    "Machining Suggestions for a Power Cross-feed Attachment","Fred Geisler","Techniques","MW Vol. 13 No. 5 Oct-Nov 2000","8"
    "Parallel Clamps","H. D. Candland","Workholding","MW Vol. 13 No. 5 Oct-Nov 2000","15"
    "Small Index Fixture","James S. McKnight","Measuring & Layout","MW Vol. 13 No. 5 Oct-Nov 2000","16"
    "An Index Head For the Sherline Lathe/Mill - Part IV","Milo W. Bresley","Machining Accessories","MW Vol. 13 No. 5 Oct-Nov 2000","22"
    "Building the Gingery Dividing Head","J. F. Ladd","Machining Accessories","MW Vol. 13 No. 5 Oct-Nov 2000","28"
    "Making a Spinning Target","Lowell P. Braxton","Hobby Items","MW Vol. 13 No. 5 Oct-Nov 2000","30"
    "Laying Out: Putting Your Desktop Printer to Work in Your Shop","Steven A. Scampini","Computers","MW Vol. 13 No. 5 Oct-Nov 2000","32"
    "An Adjustable Angle Plate - An Alternate Design","David Popelka","Machining Accessories","MW Vol. 13 No. 5 Oct-Nov 2000","34"
    "Laser Guidance System for a Mill-drill","Terry Sexton","Techniques","MW Vol. 13 No. 5 Oct-Nov 2000","35"
    "A Hand Drill Tool Post Fixture for Grinding and Indexing","Eugene Pischel","Shop Accessories","MW Vol. 13 No. 5 Oct-Nov 2000","39"
    "Determining the Size of a Metric Thread from Inch Measurements","Robert Koval","Techniques","MW Vol. 13 No. 5 Oct-Nov 2000","40"
    "The Gunsmith Machinist: A Post-ban AR-15 Muzzle Brake","Steve Acker","Gunsmithing","MW Vol. 13 No. 5 Oct-Nov 2000","42"
    "The Amateur Machinist: Gage Blocks - Who, Where and Why","Barry Young","Measuring & Layout","MW Vol. 13 No. 5 Oct-Nov 2000","44"
    "The Tool Room: Lathe Die Holder","James W. Hauser","Lathes","MW Vol. 13 No. 5 Oct-Nov 2000","46"
    "Addenda to the Automatic Coolant Applicator","Glenn L. Wilson","Machining Accessories","MW Vol. 13 No. 5 Oct-Nov 2000","47"
    "Tyro's First Lathe - Part III","Jim Swartz","Techniques","MW Vol. 13 No. 5 Oct-Nov 2000","49"
    "A New Look at the Bell Chuck","Michel Jacot","Techniques","MW Vol. 13 No. 5 Oct-Nov 2000","52"
    "Hand Vise","William R. Johnson","Hand Tools","MW Vol. 13 No. 5 Oct-Nov 2000","53"
    "Tool Post Grinder","Thomas Morrison","Shop Accessories","MW Vol. 13 No. 6 Dec 2000-Jan 2001","8"
    "V-Belt Drive for a 9 South Bend Lathe - NOTE: Author is incorrectly named A.N. Harwood","A. N. Eastwood","Machining Accessories","MW Vol. 13 No. 6 Dec 2000-Jan 2001","14"
    "V-belt Drive for a 9 South Bend Lathe - NOTE: Author is really A.N. Eastwood","A. N. Harwood","Machine Tools","MW Vol. 13 No. 6 Dec 2000-Jan 2001","14"
    "A Carousel Toolholder","William A. Johnson","Machining Accessories","MW Vol. 13 No. 6 Dec 2000-Jan 2001","20"
    "An End Mill Holder for the Lathe","Alan McFarlane","Machining Accessories","MW Vol. 13 No. 6 Dec 2000-Jan 2001","25"
    "Chuck Point","James DeLong","Machining Accessories","MW Vol. 13 No. 6 Dec 2000-Jan 2001","26"
    "Balanced Lathe Dog","James DeLong","Machining Accessories","MW Vol. 13 No. 6 Dec 2000-Jan 2001","27"
    "A Flexible Belt Sander","Jesse Livingston","Shop Accessories","MW Vol. 13 No. 6 Dec 2000-Jan 2001","28"
    "Candleholders","John W. Foster","Hobby Items","MW Vol. 13 No. 6 Dec 2000-Jan 2001","33"
    "Making an Adjustable Headspace Gage for Rimmed Cartridges","Lowell P. Braxton","Gunsmithing","MW Vol. 13 No. 6 Dec 2000-Jan 2001","38"
    "No Castings Required","Michael Dunham","Welding/Foundry/Forging","MW Vol. 13 No. 6 Dec 2000-Jan 2001","42"
    "The Gunsmith Machinist: Making a Chamber Casting","Steve Acker","Gunsmithing","MW Vol. 13 No. 6 Dec 2000-Jan 2001","46"
    "The Tool Room: Belt or Brake Replacement on a Model J Bridgeport Head","James W. Hauser","Machining Accessories","MW Vol. 13 No. 6 Dec 2000-Jan 2001","48"
    "A New Electronic Circuit for Glenn Wilson's Coolant Pump","Norman Telleson","Machining Accessories","MW Vol. 13 No. 6 Dec 2000-Jan 2001","50"
    "Mill and Factory: Buried Treasure","Wayne Woods","Tips & Tricks","MW Vol. 13 No. 6 Dec 2000-Jan 2001","53"
    "Mill and Factory: Holder Straightens Out Stamping Job","Wayne Woods","Tips & Tricks","MW Vol. 13 No. 6 Dec 2000-Jan 2001","53"
    "Mill and Factory: Protects Delicate Parts From Heat Damage","Wayne Woods","Tips & Tricks","MW Vol. 13 No. 6 Dec 2000-Jan 2001","54"
    "Mill and Factory: Punching Holes in Thin Metal","Wayne Woods","Tips & Tricks","MW Vol. 13 No. 6 Dec 2000-Jan 2001","54"
    "Mill and Factory: Simple Holder Makes Hand Reaming Easy","Wayne Woods","Tips & Tricks","MW Vol. 13 No. 6 Dec 2000-Jan 2001","54"
    "Mill and Factory: Helps When Inserting Cotter Pins","Wayne Woods","Tips & Tricks","MW Vol. 13 No. 6 Dec 2000-Jan 2001","55"
    "Mill and Factory: Holder for Broken Needle Files","Wayne Woods","Tips & Tricks","MW Vol. 13 No. 6 Dec 2000-Jan 2001","55"
    "A Spindle Lock for the Sherline Lathe/Mill Index Head","Milo W. Bresley","Machining Accessories","MW Vol. 14 No. 1 Feb-Mar 2001","4"
    "Sand Casting Simple Artwork","John A. Cooper","Welding/Foundry/Forging","MW Vol. 14 No. 1 Feb-Mar 2001","12"
    "Scrap Pile Turntable","D. A. Drayson","Machining Accessories","MW Vol. 14 No. 1 Feb-Mar 2001","15"
    "Circular Saw Sharpener","James S. McKnight","Shop Accessories","MW Vol. 14 No. 1 Feb-Mar 2001","18"
    "An Inexpensive Collet Closer for a Morse 5 Taper","Peter Stenabaugh","Machining Accessories","MW Vol. 14 No. 1 Feb-Mar 2001","26"
    "Primer on Welding II","James C. Robertson","Welding/Foundry/Forging","MW Vol. 14 No. 1 Feb-Mar 2001","29"
    "Cutting Metal With a Hole Saw","Patrick Tooke","Machining Accessories","MW Vol. 14 No. 1 Feb-Mar 2001","33"
    "Spring Winder","Glenn L. Wilson","Machining Accessories","MW Vol. 14 No. 1 Feb-Mar 2001","34"
    "A Relic from the Re-bore in the Chassis Era","Terry Sexton","Miscellaneous","MW Vol. 14 No. 1 Feb-Mar 2001","38"
    "Tripod","Steve Damon","Miscellaneous","MW Vol. 14 No. 1 Feb-Mar 2001","40"
    "Drill Press Tapping Jig","Gordon Rusbatch","Machining Accessories","MW Vol. 14 No. 1 Feb-Mar 2001","42"
    "Knurled Knobs","Wayne Hanson","Machining Accessories","MW Vol. 14 No. 1 Feb-Mar 2001","43"
    "Time-saving Formulas","Richard L. Idler","General Machining Knowledge","MW Vol. 14 No. 1 Feb-Mar 2001","44"
    "The Gunsmith Machinist: Using a Receiver Contouring Fixture","Steve Acker","Gunsmithing","MW Vol. 14 No. 1 Feb-Mar 2001","45"
    "The Tool Room: Cutting 27 Threads Per Inch on a Logan Lathe","James W. Hauser","General Machining Knowledge","MW Vol. 14 No. 1 Feb-Mar 2001","48"
    "Radial Traverse Indicator","Glenn L. Wilson","Measuring & Layout","MW Vol. 14 No. 2 Apr-May 2001","4"
    "An Easy-to-Use 2-Belt Sander","Thomas M. Verity","Shop Machinery","MW Vol. 14 No. 2 Apr-May 2001","8"
    "A Polishing and Utility Lathe Update","Mike Hoff","Machine Tools","MW Vol. 14 No. 2 Apr-May 2001","18"
    "Shop Lights","W. A. Lincoln","Machining Accessories","MW Vol. 14 No. 2 Apr-May 2001","20"
    "Suggestions for Thread Cutting - The Center Gage and Taps as Thread Chasers","Peter F. Lott","Techniques","MW Vol. 14 No. 2 Apr-May 2001","24"
    "Toolmaker's Vise","James S. McKnight","Workholding","MW Vol. 14 No. 2 Apr-May 2001","28"
    "Plaster Casting","James Hesse","Miscellaneous","MW Vol. 14 No. 2 Apr-May 2001","32"
    "Fabricating a Gavel","Terry Coss","Hobby Items","MW Vol. 14 No. 2 Apr-May 2001","40"
    "Mechanical Climbing Monkey","Birk Petersen","Hobby Items","MW Vol. 14 No. 2 Apr-May 2001","43"
    "Barrel Bedding Fixture","Jim Swartz","Gunsmithing","MW Vol. 14 No. 2 Apr-May 2001","47"
    "A Small Forge","Jack R. Thompson","Welding/Foundry/Forging","MW Vol. 14 No. 2 Apr-May 2001","50"
    "The Tool Room: Screw Cutter","James W. Hauser","Miscellaneous","MW Vol. 14 No. 2 Apr-May 2001","51"
    "The Gunsmith Machinist: Making an AR-15 Front Sight","Steve Acker","Gunsmithing","MW Vol. 14 No. 2 Apr-May 2001","52"
    "A Lathe Accessory Post","Glenn L. Wilson","Machining Accessories","MW Vol. 14 No. 3 Jun-Jul 2001","4"
    "Build a Lathe Milling Attachment","Marsh Collins","Machining Accessories","MW Vol. 14 No. 3 Jun-Jul 2001","8"
    "Power Feed","Jerry Vinarcik","Machining Accessories","MW Vol. 14 No. 3 Jun-Jul 2001","14"
    "Chasing Metric Threads on Lathes With Inch Thread Lead Screws","Peter F. Lott","Techniques","MW Vol. 14 No. 3 Jun-Jul 2001","18"
    "Making a Tubing Notcher","Lowell P. Braxton","Shop Accessories","MW Vol. 14 No. 3 Jun-Jul 2001","22"
    "Metal-cutting Band Saw Modifications","Paul Smeltzer","Shop Machinery","MW Vol. 14 No. 3 Jun-Jul 2001","28"
    "Making a Myford Form a Grizzly","Steve Roberts","Machine Modifications","MW Vol. 14 No. 3 Jun-Jul 2001","32"
    "A Cylinder Revolves With the Wheel It Drives","Arnold L. Teague","Engines","MW Vol. 14 No. 3 Jun-Jul 2001","36"
    "Centering","J. B. Shipstead","Techniques","MW Vol. 14 No. 3 Jun-Jul 2001","40"
    "The Mover - A Little Engine Project","Roger Claude","Engines","MW Vol. 14 No. 3 Jun-Jul 2001","41"
    "Accessories for Your Arbor Press","Eddie M. Zanrosso","Shop Accessories","MW Vol. 14 No. 3 Jun-Jul 2001","44"
    "Allen Wrench Holder","William Tannahill","Hand Tools","MW Vol. 14 No. 3 Jun-Jul 2001","46"
    "Cross-feed Fix - Lathe","Rudy Legname","Machine Modifications","MW Vol. 14 No. 3 Jun-Jul 2001","47"
    "The Tool Room: Magnetic Base","James W. Hauser","Shop Accessories","MW Vol. 14 No. 3 Jun-Jul 2001","48"
    "Machining a Frame for a Ramped Barrel","Corrine Hummel","Gunsmithing","MW Vol. 14 No. 3 Jun-Jul 2001","49"
    "Grinding Wheel Balance","Glenn L. Wilson","Miscellaneous","MW Vol. 14 No. 3 Jun-Jul 2001","51"
    "Quick Change Radii Attachment","Mike Hoff","Machining Accessories","MW Vol. 14 No. 4 Aug-Sep 2001","4"
    "Babbitt Bearings - Still a Viable Solution","James P. Riser","Techniques","MW Vol. 14 No. 4 Aug-Sep 2001","18"
    "Cutoff Toolholder","Marsh Collins","Machining Accessories","MW Vol. 14 No. 4 Aug-Sep 2001","26"
    "Automatic Vent Door","James S. McKnight","Shop Accessories","MW Vol. 14 No. 4 Aug-Sep 2001","32"
    "Right-angle Accessory for a Dial Indicator","George A. Ewen","Measuring & Layout","MW Vol. 14 No. 4 Aug-Sep 2001","38"
    "Round V-blocks","Arden A. Schroeder","Machining Accessories","MW Vol. 14 No. 4 Aug-Sep 2001","42"
    "Arc Welding Tips","Robert Ford","Welding/Foundry/Forging","MW Vol. 14 No. 4 Aug-Sep 2001","44"
    "The Gunsmith Machinist: Headspace and Headspace Gages","Steve Acker","Gunsmithing","MW Vol. 14 No. 4 Aug-Sep 2001","45"
    "The Tool Room: Barrel Bolt","James W. Hauser","Shop Accessories","MW Vol. 14 No. 4 Aug-Sep 2001","48"
    "Save Your Gears - A Simple Modification for the Taig Micro Lathe","J P. Weiser","Machine Tools","MW Vol. 14 No. 5 Oct-Nov 2001","4"
    "Power Cross-feed for a Milling Machine","F. J. Lennox","Machining Accessories","MW Vol. 14 No. 5 Oct-Nov 2001","8"
    "Bench Size Combination Press and Brake","Lawrence Craig","Shop Machinery","MW Vol. 14 No. 5 Oct-Nov 2001","18"
    "The Trigger Treatise","Marsh Collins","Gunsmithing","MW Vol. 14 No. 5 Oct-Nov 2001","25"
    "Propane-fired Furnace","Wayne Hanson","Welding/Foundry/Forging","MW Vol. 14 No. 5 Oct-Nov 2001","31"
    "Jet Lathe Modifications","Jim Snowdon","Machine Tools","MW Vol. 14 No. 5 Oct-Nov 2001","34"
    "Using Surplus Circuit-board Tooling in the Home Shop","Bob Neidorff","Machining Accessories","MW Vol. 14 No. 5 Oct-Nov 2001","36"
    "Some Shaper Tips","Sam Doughty","Machine Tools","MW Vol. 14 No. 5 Oct-Nov 2001","40"
    "Indicating Mill Vises","Joseph P. Howard","Workholding","MW Vol. 14 No. 5 Oct-Nov 2001","42"
    "Concentric Turning","John Hayslip","Techniques","MW Vol. 14 No. 5 Oct-Nov 2001","43"
    "Horizontal Saw Accessories","Gary Vriezen","Machining Accessories","MW Vol. 14 No. 5 Oct-Nov 2001","44"
    "Outfit Your Shoptask Lathe With a 5-C Collet Chuck","James R. Instone","Machining Accessories","MW Vol. 14 No. 5 Oct-Nov 2001","46"
    "The Gunsmith Machinist","Reid Coffield","Hobby Community","MW Vol. 14 No. 5 Oct-Nov 2001","49"
    "The Gunsmith Machinist: An M-14 Front Sight for the Mauser","Steve Acker","Gunsmithing","MW Vol. 14 No. 5 Oct-Nov 2001","50"
    "The Tool Room: Rough and Tumble Press Block","James W. Hauser","Shop Accessories","MW Vol. 14 No. 5 Oct-Nov 2001","53"
    "A Gage for Setting the Cutter on a Diamond Tool Holder","R.G. Sparber","Machining Accessories","MW Vol. 14 No. 5 Oct-Nov 2001","54"
    "The Tie-clasp Wobbler","Jerry Pontius","Engines","MW Vol. 14 No. 6 Dec 2001-Jan 2002","4"
    "Tooling Plates for a Small Mill/Drill","Marsh Collins","Machining Accessories","MW Vol. 14 No. 6 Dec 2001-Jan 2002","22"
    "Fastening Thin Sheet Metal","James DeLong","Miscellaneous","MW Vol. 14 No. 6 Dec 2001-Jan 2002","26"
    "Rebuilding Lathe Half-nuts","Jim Swartz","Lathes","MW Vol. 14 No. 6 Dec 2001-Jan 2002","27"
    "Starting a Blacksmith Shop at Home","Leland Stone","Welding/Foundry/Forging","MW Vol. 14 No. 6 Dec 2001-Jan 2002","30"
    "Eliminate Grinder Vibration","Thomas Morrison","Shop Machinery","MW Vol. 14 No. 6 Dec 2001-Jan 2002","34"
    "Morse Taper Tooling for the Lathe","Peter J. Willox","Machining Accessories","MW Vol. 14 No. 6 Dec 2001-Jan 2002","38"
    "The Gunsmith Machinist: Repairing a Scope Base Mounting Hole","Steve Acker","Gunsmithing","MW Vol. 14 No. 6 Dec 2001-Jan 2002","41"
    "Ultra-micro Torch Adaptation","Brian Hammond","Miscellaneous","MW Vol. 14 No. 6 Dec 2001-Jan 2002","44"
    "The Tool Room: A Cheap Trammel","James W. Hauser","Miscellaneous","MW Vol. 14 No. 6 Dec 2001-Jan 2002","45"
    "Micro Index Head Attachment for the Sherline Lathe/Mill Index Head - Part One","Milo W. Bresley","Machining Accessories","MW Vol. 15 No. 1 Feb-Mar 2002","4"
    "A Cart for Your Stirling-powered Tractor","Karl T. Schwab","Hobby Items","MW Vol. 15 No. 1 Feb-Mar 2002","16"
    "The Four-bats Project","Terry Coss","Hobby Items","MW Vol. 15 No. 1 Feb-Mar 2002","22"
    "An Easy Lathe Tool-height Gage","Alan McFarlane","Machining Accessories","MW Vol. 15 No. 1 Feb-Mar 2002","26"
    "Silver Solder Techniques","Brian Hammond","Miscellaneous","MW Vol. 15 No. 1 Feb-Mar 2002","27"
    "Build the Engine Mill","George A. Ewen","Machine Tools","MW Vol. 15 No. 1 Feb-Mar 2002","28"
    "The Ubiquitous Morse Taper","Marsh Collins","Machining Accessories","MW Vol. 15 No. 1 Feb-Mar 2002","34"
    "The Tool Room: A Cartridge Remover for Moen Faucets","James W. Hauser","Miscellaneous","MW Vol. 15 No. 1 Feb-Mar 2002","38"
    "The Gunsmith Machinist: Using a Grip Safety Feature","Steve Acker","Gunsmithing","MW Vol. 15 No. 1 Feb-Mar 2002","40"
    "Something's Out of Round!","Matthew J. Russel","Machining Accessories","MW Vol. 15 No. 2 Apr-May 2002","4"
    "A Pillar Bedding Tool","Fred Prestridge","Gunsmithing","MW Vol. 15 No. 2 Apr-May 2002","15"
    "Micro Index Head Attachment for the Sherline Lathe/Mill Index Head - Part Two","Milo W. Bresley","Machining Accessories","MW Vol. 15 No. 2 Apr-May 2002","18"
    "Clymer Gearless Differential","Jim Reynolds","Miscellaneous","MW Vol. 15 No. 2 Apr-May 2002","28"
    "Power Hacksaws in the Home Shop","Terry Sexton","Shop Machinery","MW Vol. 15 No. 2 Apr-May 2002","33"
    "Adding Dial RO's to Your Shoptask- A Mill-Drill Adventure","Ron Carvalho","Machining Accessories","MW Vol. 15 No. 2 Apr-May 2002","36"
    "Care and Feeding of Indicators","James DeLong","Measuring & Layout","MW Vol. 15 No. 2 Apr-May 2002","40"
    "Making a Ruger Scope Ring Base","Corrine Hummel","Gunsmithing","MW Vol. 15 No. 2 Apr-May 2002","42"
    "The Tool Room: Threading Dial Captive Wrench","James W. Hauser","Lathes","MW Vol. 15 No. 2 Apr-May 2002","45"
    "An R-8 Fly Cutter","Rick Turner","Machining Accessories","MW Vol. 15 No. 3 Jun-Jul 2002","6"
    "Outboard Motor Lifter","Donald R. Oswald","Projects","MW Vol. 15 No. 3 Jun-Jul 2002","10"
    "Micro Index Head Attachment for the Sherline Lathe/Mill Index Head - Part Three","Milo W. Bresley","Machining Accessories","MW Vol. 15 No. 3 Jun-Jul 2002","18"
    "Holding Small Workpieces","Martin Gingrich","Machining Accessories","MW Vol. 15 No. 3 Jun-Jul 2002","27"
    "Converting a Grizzly G8689 Mini-Mill to Belt Drive","Ken Coburn","Machine Modifications","MW Vol. 15 No. 3 Jun-Jul 2002","30"
    "Sheet Metal Roller","Alan R. Swank","Shop Accessories","MW Vol. 15 No. 3 Jun-Jul 2002","36"
    "The Gunsmith Machinist: Rebarreling an M-1 Garand - Part One","Steve Acker","Gunsmithing","MW Vol. 15 No. 3 Jun-Jul 2002","40"
    "The Tool Room: Hand Knurler","James W. Hauser","Hand Tools","MW Vol. 15 No. 3 Jun-Jul 2002","45"
    "Let's Tie One On! - Make a Fly-tying Vise","Peter Stenabaugh","Hobby Items","MW Vol. 15 No. 4 Aug-Sep 2002","6"
    "Simple Fixes for Four-by-sixes","R. W. O'Brien","Miscellaneous","MW Vol. 15 No. 4 Aug-Sep 2002","16"
    "Micro Index Head Attachment for the Sherline Lathe/Mill Index Head - Part Four","Milo W. Bresley","Machining Accessories","MW Vol. 15 No. 4 Aug-Sep 2002","18"
    "Sharpening Drills by Hand","Glenn L. Wilson","Miscellaneous","MW Vol. 15 No. 4 Aug-Sep 2002","26"
    "Index/Angle Plate","James S. McKnight","Machining Accessories","MW Vol. 15 No. 4 Aug-Sep 2002","29"
    "Small Gear and Bearing Puller","John A. Cooper","Miscellaneous","MW Vol. 15 No. 4 Aug-Sep 2002","33"
    "A Sanding Disk for the Lathe","Thomas Morrison","Machining Accessories","MW Vol. 15 No. 4 Aug-Sep 2002","36"
    "Surfacing an Exhaust Manifold","Tim Clarke","Miscellaneous","MW Vol. 15 No. 4 Aug-Sep 2002","39"
    "Easy Tapper","John Davis","Hand Tools","MW Vol. 15 No. 4 Aug-Sep 2002","41"
    "The Gunsmith Machinist: Rebarreling an M-1 Garand - Part Two","Steve Acker","Gunsmithing","MW Vol. 15 No. 4 Aug-Sep 2002","43"
    "The Tool Room: Machinist's Jacks","James W. Hauser","Shop Accessories","MW Vol. 15 No. 4 Aug-Sep 2002","46"
    "Two-liter Bottle Launcher","Paul Smeltzer","Projects","MW Vol. 15 No. 5 Oct-Nov 2002","6"
    "A New Tool Post for the 9 South Bend Lathe","Terrill E. Koken","Machining Accessories","MW Vol. 15 No. 5 Oct-Nov 2002","14"
    "Metal Lathe Cone Center","William Alles","Machining Accessories","MW Vol. 15 No. 5 Oct-Nov 2002","20"
    "An Inexpensive EDM","Arnold Gregrich","EDM","MW Vol. 15 No. 5 Oct-Nov 2002","24"
    "Round Corners in Angle Iron - The Hammond Methodology","Brian Hammond","Projects","MW Vol. 15 No. 5 Oct-Nov 2002","27"
    "Chestnut Slitter","Donald R. Oswald","Projects","MW Vol. 15 No. 5 Oct-Nov 2002","33"
    "Electric Metal Stamper","Glenn L. Wilson","Shop Machinery","MW Vol. 15 No. 5 Oct-Nov 2002","36"
    "Improving a Pistol Grip - The Gunsmith Machinist","Corrine Hummel","Gunsmithing","MW Vol. 15 No. 5 Oct-Nov 2002","41"
    "The Tool Room: Faucet Angle Extension","James W. Hauser","Projects","MW Vol. 15 No. 5 Oct-Nov 2002","45"
    "Boring Bars - Problems and Solutions","Daniel Devor","Machining Accessories","MW Vol. 15 No. 5 Oct-Nov 2002","46"
    "Power File","Ronald G. Casteel","Shop Machinery","MW Vol. 15 No. 6 Dec 2002-Jan 2003","6"
    "A Set of Hold-down Clamps","John A. Cooper","Machining Accessories","MW Vol. 15 No. 6 Dec 2002-Jan 2003","16"
    "Improving the Performance of the 9 and 10 South Bend Lathes","John W. Foster","Machine Tools","MW Vol. 15 No. 6 Dec 2002-Jan 2003","18"
    "Old Vise","Marsh Collins","Machining Accessories","MW Vol. 15 No. 6 Dec 2002-Jan 2003","24"
    "Inside-out Metal Turning - A Christmas Ornament","Dean C. Andrus","Techniques","MW Vol. 15 No. 6 Dec 2002-Jan 2003","27"
    "Tool Bit Broach","Marvin Stamp","Machining Accessories","MW Vol. 15 No. 6 Dec 2002-Jan 2003","30"
    "Another Collet Closer","Fred Prestridge","Machining Accessories","MW Vol. 15 No. 6 Dec 2002-Jan 2003","32"
    "A Sequel to the Inexpensive EDM","Arnold Gregrich","EDM","MW Vol. 15 No. 6 Dec 2002-Jan 2003","35"
    "A Router Base for Dremel Tools","Leroy C. Bayliss","Machining Accessories","MW Vol. 15 No. 6 Dec 2002-Jan 2003","37"
    "A Different Tool Post Milling Spindle","Patrick Tooke","Machining Accessories","MW Vol. 15 No. 6 Dec 2002-Jan 2003","42"
    "Making a Cleaning Rod Muzzle Guide - The Gunsmith Machinist","Corrine Hummel","Gunsmithing","MW Vol. 15 No. 6 Dec 2002-Jan 2003","44"
    "The Tool Room: Spring-loaded Drill Chuck","James W. Hauser","Shop Accessories","MW Vol. 15 No. 6 Dec 2002-Jan 2003","47"
    "Project Lost - Project Recovered - Tuning the Mill-Drill","Myles Milner","Machine Tools","MW Vol. 16 No. 1 Feb-Mar 2003","6"
    "A Spindle Lock for Your Mill-Drill","Marsh Collins","Machining Accessories","MW Vol. 16 No. 1 Feb-Mar 2003","12"
    "Make a Dividing Head from a Lathe Headstock","Stephen G. Wellcome","Machine Tools","MW Vol. 16 No. 1 Feb-Mar 2003","20"
    "Portable Shop Light With Outlet","Ronald Geppert","Shop Accessories","MW Vol. 16 No. 1 Feb-Mar 2003","24"
    "A Low-profile Chuck Mounting for a Rotary Table","John Opfer, Jr.","Machining Accessories","MW Vol. 16 No. 1 Feb-Mar 2003","26"
    "Adding DC to Your AC Welder","James C. Robertson","Welding/Foundry/Forging","MW Vol. 16 No. 1 Feb-Mar 2003","30"
    "Gear Repair","John W. Foster","Lathes","MW Vol. 16 No. 1 Feb-Mar 2003","34"
    "Improve Your Down-feed Accuracy","Don Titus","Machining Accessories","MW Vol. 16 No. 1 Feb-Mar 2003","37"
    "Make a Carbide-insert Boring Bar","Alan McFarlane","Machining Accessories","MW Vol. 16 No. 1 Feb-Mar 2003","40"
    "The Tool Room: V-Block Clamp","James W. Hauser","Shop Accessories","MW Vol. 16 No. 1 Feb-Mar 2003","41"
    "Tapping a Shallow Hole - The Gunsmith Machinist","Corrine Hummel","Gunsmithing","MW Vol. 16 No. 1 Feb-Mar 2003","42"
    "Ball Handles Made on the Lathe","W. A. Lincoln","Machining Accessories","MW Vol. 16 No. 2 Apr-May 2003","6"
    "Router Machine","James S. McKnight","Shop Machinery","MW Vol. 16 No. 2 Apr-May 2003","10"
    "Magnetizer - Demagnetizer","Birk Petersen","Shop Accessories","MW Vol. 16 No. 2 Apr-May 2003","27"
    "Slitting Small Screw Heads","Conrad A. Huard","Machining Accessories","MW Vol. 16 No. 2 Apr-May 2003","30"
    "Improving Mill-Drill Belt Tensioning","Tim Clarke","Machine Tools","MW Vol. 16 No. 2 Apr-May 2003","32"
    "New Life for a Warped Lathe","Stephen G. Wellcome","Lathes","MW Vol. 16 No. 2 Apr-May 2003","36"
    "More Uses for Cerrosafe","Corrine Hummel","Gunsmithing","MW Vol. 16 No. 2 Apr-May 2003","38"
    "The Tool Room: Hairpin Thread Cleaner","James W. Hauser","Shop Accessories","MW Vol. 16 No. 2 Apr-May 2003","42"
    "A Hand Pump for the Kitchen","Tim Johnson","Projects","MW Vol. 16 No. 3 Jun-Jul 2003","6"
    "Bubba Backhoe","David O'Neil","Projects","MW Vol. 16 No. 3 Jun-Jul 2003","14"
    "Convert a Fixed Dial to a Zero-set Dial","Don Garlow","Machining Accessories","MW Vol. 16 No. 3 Jun-Jul 2003","16"
    "Solving Tapered Tool Spin","Jim Swartz","Techniques","MW Vol. 16 No. 3 Jun-Jul 2003","20"
    "Die Files for the Power File","Ronald G. Casteel","Machining Accessories","MW Vol. 16 No. 3 Jun-Jul 2003","22"
    "Build an Auxiliary Mill Vise","Mike Hoff","Machining Accessories","MW Vol. 16 No. 3 Jun-Jul 2003","26"
    "Little Easy Sander","A. C. Frohnapfel","Shop Machinery","MW Vol. 16 No. 3 Jun-Jul 2003","36"
    "Reworking the New Multi-Vise","Corrine Hummel","Gunsmithing","MW Vol. 16 No. 3 Jun-Jul 2003","40"
    "The Tool Room: Strange Wrench for a Stub Arbor","James W. Hauser","Miscellaneous","MW Vol. 16 No. 3 Jun-Jul 2003","45"
    "Lathe Turning FUNdementals","Walter Yetman","Projects","MW Vol. 16 No. 4 Aug-Sep 2003","6"
    "Oscillating Edge Belt/Spindle Sander","James S. McKnight","Shop Machinery","MW Vol. 16 No. 4 Aug-Sep 2003","10"
    "Build a Budget Speed Handle","Jim Swartz","Machining Accessories","MW Vol. 16 No. 4 Aug-Sep 2003","28"
    "Barrel Vise and Action Wrench","Fred Prestridge","Gunsmithing","MW Vol. 16 No. 4 Aug-Sep 2003","30"
    "Fabricate a Diving Board Pedestal","Marsh Collins","Projects","MW Vol. 16 No. 4 Aug-Sep 2003","34"
    "Installing a Low Mount BO-MAR Sight","Corrine Hummel","Gunsmithing","MW Vol. 16 No. 4 Aug-Sep 2003","38"
    "The Tool Room: A Different Type of Boring Bar","James W. Hauser","Shop Accessories","MW Vol. 16 No. 4 Aug-Sep 2003","44"
    "My Replica of a Bugatti","Fred Storer","Projects","MW Vol. 16 No. 5 Oct-Nov 2003","6"
    "Simple Simon Stirling Engine","David O'Neil","Engines","MW Vol. 16 No. 5 Oct-Nov 2003","14"
    "Make a 35-Millimeter Stereo Hand Viewer","Glenn L. Wilson","Miscellaneous","MW Vol. 16 No. 5 Oct-Nov 2003","18"
    "An Easy Taper Attachment","Thomas Morrison","Machining Accessories","MW Vol. 16 No. 5 Oct-Nov 2003","26"
    "Slow Your Mill-Drill to 30 RPM","David Robinson","Machine Modifications","MW Vol. 16 No. 5 Oct-Nov 2003","32"
    "Handy Little Tap Guide","Dewey Dirrim","Machining Accessories","MW Vol. 16 No. 5 Oct-Nov 2003","33"
    "Make a Mini Lathe Carrier","Charles Baker","Projects","MW Vol. 16 No. 5 Oct-Nov 2003","34"
    "The Gunsmith Machinist: Installing a Muzzle Brake","Steve Acker","Gunsmithing","MW Vol. 16 No. 5 Oct-Nov 2003","36"
    "The Tool Room: British Association (B.A.) Standard Thread Substitution","James W. Hauser","General Machining Knowledge","MW Vol. 16 No. 5 Oct-Nov 2003","39"
    "Small Compound Angle Vise","James S. McKnight","Shop Accessories","MW Vol. 16 No. 6 Dec 2003-Jan 2004","6"
    "Build a Threading Dial","D. A. Drayson","Lathes","MW Vol. 16 No. 6 Dec 2003-Jan 2004","14"
    "Roller Stand for a Small Metal-Cutting Band Saw","Ronald G. Casteel","Shop Accessories","MW Vol. 16 No. 6 Dec 2003-Jan 2004","18"
    "Power Tapping","Jim Swartz","Lathes","MW Vol. 16 No. 6 Dec 2003-Jan 2004","21"
    "Measuring the Radius of Circular Arcs","Bob Mansfield","General Machining Knowledge","MW Vol. 16 No. 6 Dec 2003-Jan 2004","22"
    "Make An Auxiliary Boring Table for the 12 Craftsman Lathe","Lowell P. Braxton","Lathes","MW Vol. 16 No. 6 Dec 2003-Jan 2004","26"
    "Making 3D Photographic Slides","Glenn L. Wilson","Projects","MW Vol. 16 No. 6 Dec 2003-Jan 2004","30"
    "The Gunsmith Machinist: A Side Safety for the Mauser Rifle","Steve Acker","Gunsmithing","MW Vol. 16 No. 6 Dec 2003-Jan 2004","36"
    "The Tool Room: Water Softener Point","James W. Hauser","Projects","MW Vol. 16 No. 6 Dec 2003-Jan 2004","43"
    "Finish with a Shaving Tool Bit","Clinton James","Tips & Tricks","MW Vol. 16 No. 6 Dec 2003-Jan 2004","47"
    "The Enterprise - A 3-inch-Plus Radius-turning Tool","Peter Stenabaugh","Lathes","MW Vol. 17 No. 1 Feb-Mar 2004","8"
    "An Unusual Collet Chuck System","George A. Ewen","Lathes","MW Vol. 17 No. 1 Feb-Mar 2004","18"
    "Handy Chuck Holder","Chet McClellan","Shop Accessories","MW Vol. 17 No. 1 Feb-Mar 2004","22"
    "Tightening a Horizontal Mill Arbor","Bob Neidorff","Mills","MW Vol. 17 No. 1 Feb-Mar 2004","24"
    "Machined Cartridge Cases","Tim Clarke","Gunsmithing","MW Vol. 17 No. 1 Feb-Mar 2004","26"
    "Cutting Threads on a Lathe by the Numbers","Rene Lajoinie","Lathes","MW Vol. 17 No. 1 Feb-Mar 2004","28"
    "Turning a Left-hand Acme Thread","Marsh Collins","Lathes","MW Vol. 17 No. 1 Feb-Mar 2004","29"
    "The Gunsmith Machinist: Welding up a Barrel Hood","Steve Acker","Gunsmithing","MW Vol. 17 No. 1 Feb-Mar 2004","31"
    "Large Concave Radius Milling","Mike Hoff","Mills","MW Vol. 17 No. 1 Feb-Mar 2004","37"
    "The Tool Room: Indicator Holder for the Milling Machine","James W. Hauser","Mills","MW Vol. 17 No. 1 Feb-Mar 2004","38"
    "Make Your Own Square and Hex Collet Adapters","W. A. Lincoln","Shop Accessories","MW Vol. 17 No. 2 Apr-May 2004","6"
    "Build a Coolant Applicator Pen","Glenn L. Wilson","Shop Accessories","MW Vol. 17 No. 2 Apr-May 2004","10"
    "How to Cut Multiple Internal Blind Keyways","Alan R. Swank","Lathes","MW Vol. 17 No. 2 Apr-May 2004","12"
    "A Tool Tree for your Lathe Accessories","Don Titus","Shop Accessories","MW Vol. 17 No. 2 Apr-May 2004","15"
    "Bench Blocks","Jim Swartz","Shop Accessories","MW Vol. 17 No. 2 Apr-May 2004","18"
    "A Unique Mill Vise","Fred Prestridge","Mills","MW Vol. 17 No. 2 Apr-May 2004","20"
    "The Art of Making Darts","Steve Kinsey","Projects","MW Vol. 17 No. 2 Apr-May 2004","26"
    "Buying Used Measuring Tools","Thomas M. Buckley","General Machining Knowledge","MW Vol. 17 No. 2 Apr-May 2004","36"
    "The Gunsmith Machinist: Repairing a Feed Ramp","Steve Acker","Gunsmithing","MW Vol. 17 No. 2 Apr-May 2004","38"
    "The Tool Room: Make a Chuck Key Holder for Your Lathe","James W. Hauser","Lathes","MW Vol. 17 No. 2 Apr-May 2004","42"
    "A Micro Adjustable Boring Head Attachment","Peter Stenabaugh","Shop Machinery","MW Vol. 17 No. 3 Jun-Jul 2004","6"
    "A Dial Indicator Holder for your Lathe","Stephen G. Wellcome","Lathes","MW Vol. 17 No. 3 Jun-Jul 2004","12"
    "No-Lift Milling Machine Accessory Table","W. A. Lincoln","Mills","MW Vol. 17 No. 3 Jun-Jul 2004","16"
    "Make An Auto-Locking Hitch Pin","Brian Kuncelman","Projects","MW Vol. 17 No. 3 Jun-Jul 2004","18"
    "Building a Rifle Rest","J. Randolph Bulgin","Gunsmithing","MW Vol. 17 No. 3 Jun-Jul 2004","20"
    "Making a Mill Vise Alignment System","Lowell P. Braxton","Mills","MW Vol. 17 No. 3 Jun-Jul 2004","28"
    "Balancing Grinding Wheels","Allen Blaney","Shop Machinery","MW Vol. 17 No. 3 Jun-Jul 2004","30"
    "Various 3C Collets","John W. Way","Lathes","MW Vol. 17 No. 3 Jun-Jul 2004","36"
    "The Gunsmith Machinist: Cutting a Gun Screw to Length","Steve Acker","Gunsmithing","MW Vol. 17 No. 3 Jun-Jul 2004","40"
    "The Tool Room: Ladder Tightening Device","James W. Hauser","Projects","MW Vol. 17 No. 3 Jun-Jul 2004","43"
    "Table Saw for the Dremel Motor Tool - Part One","Jerry Pontius","Shop Machinery","MW Vol. 17 No. 4 Aug-Sep 2004","6"
    "Foundryman's Molding Bench","Stephen Vitkovits","Welding/Foundry/Forging","MW Vol. 17 No. 4 Aug-Sep 2004","18"
    "Saving Face...Plate, that is!","Myles Milner","Lathes","MW Vol. 17 No. 4 Aug-Sep 2004","22"
    "Positioning the Tailstock Ram...Exactly","Burt Noble","Lathes","MW Vol. 17 No. 4 Aug-Sep 2004","26"
    "A Universal Workstop for Angle Lock Style Vises","Jim Swartz","Shop Accessories","MW Vol. 17 No. 4 Aug-Sep 2004","28"
    "Making a Trim Die for Rimmed Cartridges","Lowell P. Braxton","Gunsmithing","MW Vol. 17 No. 4 Aug-Sep 2004","30"
    "Old Brute - Bench Vise","LeRoy Anderson","Shop Accessories","MW Vol. 17 No. 4 Aug-Sep 2004","32"
    "Bolt Hole Chart","Tom Taylor","General Machining Knowledge","MW Vol. 17 No. 4 Aug-Sep 2004","34"
    "Salvaging an Old Thickness Planer","Spencer Schonher","Shop Machinery","MW Vol. 17 No. 4 Aug-Sep 2004","35"
    "The Gunsmith Machinist: A Lanyard Loop for the 1911 Pistol","Steve Acker","Gunsmithing","MW Vol. 17 No. 4 Aug-Sep 2004","38"
    "Gauge for Setting Tool Bit Height","Wayne Woods","Shop Accessories","MW Vol. 17 No. 4 Aug-Sep 2004","41"
    "The Tool Room: Making a Fly Cutter","James W. Hauser","Shop Accessories","MW Vol. 17 No. 4 Aug-Sep 2004","42"
    "Repairing Worn or Damaged Shafts","J. Randolph Bulgin","Miscellaneous","MW Vol. 17 No. 5 Oct-Nov 2004","6"
    "Handy Mill-Drill Dial Modification","Ed Payne","Mills","MW Vol. 17 No. 5 Oct-Nov 2004","12"
    "Set Up a Power Feed Limit Switch","Peter Nolan","Mills","MW Vol. 17 No. 5 Oct-Nov 2004","14"
    "Golf Ball Holder/Dispenser/Pick-Up","Donald R. Oswald","Projects","MW Vol. 17 No. 5 Oct-Nov 2004","16"
    "Tips on the Grizzly 1031 Lathe","W.B Vaughan","Lathes","MW Vol. 17 No. 5 Oct-Nov 2004","22"
    "Table Saw for the Dremel Motor Tool - Part Two","Jerry Pontius","Shop Machinery","MW Vol. 17 No. 5 Oct-Nov 2004","24"
    "A Gas Cylinder Screw for the M1 Rifle","Jim Swartz","Gunsmithing","MW Vol. 17 No. 5 Oct-Nov 2004","33"
    "Poor (Thinking) Man's Worm Gear","Don E. Jones","Miscellaneous","MW Vol. 17 No. 5 Oct-Nov 2004","36"
    "The Gunsmith Machinist: Repairing a Tokarev Safety","Steve Acker","Gunsmithing","MW Vol. 17 No. 5 Oct-Nov 2004","38"
    "The Tool Room: Extended Unimat Toolpost","James W. Hauser","Lathes","MW Vol. 17 No. 5 Oct-Nov 2004","43"
    "Buoy - An Engine From an Engine","Karl T. Schwab","Engines","MW Vol. 17 No. 6 Dec 2004-Jan 2005","6"
    "Effects of Tool Bit Height While Turning Tapers","Fred Prestridge","General Machining Knowledge","MW Vol. 17 No. 6 Dec 2004-Jan 2005","16"
    "Grinding a Morse No. 0 Taper the Amateur Way","L. McKinley","Lathes","MW Vol. 17 No. 6 Dec 2004-Jan 2005","18"
    "Dampen Pipe Noise - Make a Special Clamp","Robert Shosh","Projects","MW Vol. 17 No. 6 Dec 2004-Jan 2005","20"
    "Make a Mill-Drill Chip Pan","Frank Goeringer","Mills","MW Vol. 17 No. 6 Dec 2004-Jan 2005","24"
    "A Unique Mill Vise - "Junior Edition"","Donald L. Feinberg","Shop Accessories","MW Vol. 17 No. 6 Dec 2004-Jan 2005","26"
    "Rebuild That M1 Gas Cylinder Lock Screw","Jim Swartz","Gunsmithing","MW Vol. 17 No. 6 Dec 2004-Jan 2005","28"
    "Shop Compressed Air for In-house Tire Service","William Johnson","Projects","MW Vol. 17 No. 6 Dec 2004-Jan 2005","31"
    "Repairing a Flat Belt on a Floor-type South Bend Lathe","Keith Mizell","Lathes","MW Vol. 17 No. 6 Dec 2004-Jan 2005","34"
    "Drilling Holes in Glass","Tom Bartlett","Projects","MW Vol. 17 No. 6 Dec 2004-Jan 2005","36"
    "Adjusting Firing Pin Protrusion","Corrine Hummel","Gunsmithing","MW Vol. 17 No. 6 Dec 2004-Jan 2005","38"
    "The Tool Room: Make a Lathe Test Bar","James W. Hauser","Lathes","MW Vol. 17 No. 6 Dec 2004-Jan 2005","41"
    "An Offside Lathe Chuck","Lowell P. Braxton","Machining Accessories","MW Vol. 18 No. 1 Feb-Mar 2005","6"
    "Mobile Flip Top Tool Stand","Ronald G. Casteel","Shop Accessories","MW Vol. 18 No. 1 Feb-Mar 2005","12"
    "Handy Mill Work Fixture","Chet McClellan","Machining Accessories","MW Vol. 18 No. 1 Feb-Mar 2005","18"
    "Waterproof Match Container","Walter Yetman","Projects","MW Vol. 18 No. 1 Feb-Mar 2005","22"
    "Install a 3-1/2 Axis Digital Readout","Steve Roberts","Measuring & Layout","MW Vol. 18 No. 1 Feb-Mar 2005","26"
    "Install a 3-1/2 Axis Digital Readout on Your Mill-Drill","Steve Roberts","Mills","MW Vol. 18 No. 1 Feb-Mar 2005","26"
    "Positioning the Tailstock Ram Exactly","Burt Noble","Lathes","MW Vol. 18 No. 1 Feb-Mar 2005","30"
    "Positioning the Tailstock Ram... Exactly","Burt Noble","Lathes","MW Vol. 18 No. 1 Feb-Mar 2005","30"
    "Making a Scope Mount for a Krag Rifle","Theodore M. Clarke","Gunsmithing","MW Vol. 18 No. 1 Feb-Mar 2005","32"
    "Making a Small Screwdriver Bit","Corrine Hummel","Gunsmithing","MW Vol. 18 No. 1 Feb-Mar 2005","38"
    "The Tool Room: Dedicated Mill Vise Hold-down Bolts","James W. Hauser","Shop Accessories","MW Vol. 18 No. 1 Feb-Mar 2005","42"
    "A Mechanical Toy","David Fiscus","Projects","MW Vol. 18 No. 2 Apr-May 2005","6"
    "Build a Fretwork Saw","James S. McKnight","Machine Tools","MW Vol. 18 No. 2 Apr-May 2005","10"
    "Making Handles","Bob Neidorff","Miscellaneous","MW Vol. 18 No. 2 Apr-May 2005","21"
    "Hand Tappers","William Johnson","Machining Accessories","MW Vol. 18 No. 2 Apr-May 2005","26"
    "Innovating and Adapting Toolholders","Myles Milner","Lathes","MW Vol. 18 No. 2 Apr-May 2005","29"
    "Repairing a Stripped Grip Screw Hole","Corrine Hummel","Gunsmithing","MW Vol. 18 No. 2 Apr-May 2005","32"
    "Centering Spin Indexes and Rotary Tables","John W. Way","General Machining Knowledge","MW Vol. 18 No. 2 Apr-May 2005","36"
    "Vise Abuse - A Pressing Problem","Lowell P. Braxton","Workholding","MW Vol. 18 No. 2 Apr-May 2005","38"
    "The Tool Room: Down and Dirty Tap Rack","James W. Hauser","Shop Accessories","MW Vol. 18 No. 2 Apr-May 2005","46"
    "High Speed Steel Toolholder","James Hannum","Lathes","MW Vol. 18 No. 3 Jun-Jul 2005","6"
    "Chamfer Set Gauge","Glenn L. Wilson","Miscellaneous","MW Vol. 18 No. 3 Jun-Jul 2005","9"
    "Re-Knob Your Way Lock","Myles Milner","Mills","MW Vol. 18 No. 3 Jun-Jul 2005","10"
    "Handy Little Hacksaw","Chet McClellan","Hand Tools","MW Vol. 18 No. 3 Jun-Jul 2005","12"
    "Precision Grinding Fixture for Tool Bits","James S. McKnight","Miscellaneous","MW Vol. 18 No. 3 Jun-Jul 2005","16"
    "A Lathe Tailstock Die Holder","Herbert Yohe","Lathes","MW Vol. 18 No. 3 Jun-Jul 2005","22"
    "Shaping Up a Delta Drill Press","Don Woit","Shop Machinery","MW Vol. 18 No. 3 Jun-Jul 2005","24"
    "Workshop Transport System","LeRoy Anderson","Shop Accessories","MW Vol. 18 No. 3 Jun-Jul 2005","26"
    "Adventures with the 9 X 20 Lathe","James A. Hornicek","Lathes","MW Vol. 18 No. 3 Jun-Jul 2005","29"
    "Cheap Power Feed for your Mill-Drill","Frank Goeringer","Mills","MW Vol. 18 No. 3 Jun-Jul 2005","32"
    "The Home Shop Machinist's Library","William Johnson","Hobby Community","MW Vol. 18 No. 3 Jun-Jul 2005","34"
    "Threaded Brass Inserts for Aluminum Bodies","Robert Shosh","Miscellaneous","MW Vol. 18 No. 3 Jun-Jul 2005","36"
    "The Gunsmith Machinist: Reling a Ruger Pistol - Part One","Steve Acker","Gunsmithing","MW Vol. 18 No. 3 Jun-Jul 2005","38"
    "The Tool Room: Make a Jab Saw From Conduit","James W. Hauser","Shop Machinery","MW Vol. 18 No. 3 Jun-Jul 2005","43"
    "Spindle Mount Your Motor Tool","Jerry Pontius","Machining Accessories","MW Vol. 18 No. 4 Aug-Sep 2005","6"
    "Slow Down a Small Mill","Chet McClellan","Mills","MW Vol. 18 No. 4 Aug-Sep 2005","10"
    "My Mini Shaper","Fred Prestridge","Machine Tools","MW Vol. 18 No. 4 Aug-Sep 2005","18"
    "Touch Chuck","Robert Beaupre","Shop Accessories","MW Vol. 18 No. 4 Aug-Sep 2005","23"
    "Facelift for an Old Favorite","Peter C. Esselburne","Gunsmithing","MW Vol. 18 No. 4 Aug-Sep 2005","30"
    "The Gunsmith Machinist: Relining a Ruger Pistol - Part Two","Steve Acker","Gunsmithing","MW Vol. 18 No. 4 Aug-Sep 2005","40"
    "The Tool Room: Collet Chuck Extension","James W. Hauser","Lathes","MW Vol. 18 No. 4 Aug-Sep 2005","44"
    "Boring Head Without a Tail","Charles St. Louis","Shop Accessories","MW Vol. 18 No. 5 Oct-Nov 2005","6"
    "An Air Compressor Reel","Thomas Morrison","Shop Accessories","MW Vol. 18 No. 5 Oct-Nov 2005","16"
    "Portable Power Band Saw","James S. McKnight","Shop Machinery","MW Vol. 18 No. 5 Oct-Nov 2005","26"
    "Vise Island","David Crement","Workholding","MW Vol. 18 No. 5 Oct-Nov 2005","32"
    "Cut a 4mm Pitch Thread on Your 9 X 20 Lathe","James A. Hornicek","Lathes","MW Vol. 18 No. 5 Oct-Nov 2005","33"
    "Moto Guzzi Screws and Triumph Exhaust Nipples","Patrick Tooke","Engines","MW Vol. 18 No. 5 Oct-Nov 2005","36"
    "The Gunsmith Machinist: Tightening a Ruger Mark 1 Frame","Steve Acker","Gunsmithing","MW Vol. 18 No. 5 Oct-Nov 2005","40"
    "The Tool Room: An Adapter for Your Faceplate","James W. Hauser","Lathes","MW Vol. 18 No. 5 Oct-Nov 2005","46"
    "Grizzly G4000 Tailstock Clamp Mechanism","Steve Roberts","Lathes","MW Vol. 18 No. 6 Dec 2005-Jan 2006","6"
    "Portable Power Band Saw: Part Two","James S. McKnight","Shop Machinery","MW Vol. 18 No. 6 Dec 2005-Jan 2006","12"
    "A Hand Vise for Small Parts","Roy Rice","Workholding","MW Vol. 18 No. 6 Dec 2005-Jan 2006","18"
    "Notes on an Old Shepherd Lathe","Clay Hale","Lathes","MW Vol. 18 No. 6 Dec 2005-Jan 2006","21"
    "Miniature Punches and Chisels: Fast and Inexpensive","Ronald G. Casteel","Hand Tools","MW Vol. 18 No. 6 Dec 2005-Jan 2006","23"
    "Building Cartridge Loading Dies Without Reamers","Lowell P. Braxton","Gunsmithing","MW Vol. 18 No. 6 Dec 2005-Jan 2006","26"
    "The Gunsmith Machinist: Lengthening a Winchester 97 Chamber - Part One","Steve Acker","Gunsmithing","MW Vol. 18 No. 6 Dec 2005-Jan 2006","36"
    "The Tool Room: A Starrett Indicator Adapter","James W. Hauser","Lathes","MW Vol. 18 No. 6 Dec 2005-Jan 2006","42"
    "Make an R8 Collet Holder for a 12 Craftsman Lathe","Lowell P. Braxton","Lathes","MW Vol. 19 No. 1 Feb-Mar 2006","6"
    "A Multi-Purpose Live Center","Jerry L. Sokol","Lathes","MW Vol. 19 No. 1 Feb-Mar 2006","12"
    "Compact V-Belt Speed Reducers","Theodore M. Clarke","Motors","MW Vol. 19 No. 1 Feb-Mar 2006","14"
    "A Handy Machine Dolly","D. Churchwell","Hand Tools","MW Vol. 19 No. 1 Feb-Mar 2006","17"
    "A Pulley Removal Tool for the 9 X 20 Lathe","James A. Hornicek","Lathes","MW Vol. 19 No. 1 Feb-Mar 2006","18"
    "Review of the Harbor Freight 115-volt Spot Welder","James Hesse","Welding/Foundry/Forging","MW Vol. 19 No. 1 Feb-Mar 2006","22"
    "Put a Guard on Your Mandrel-type Grinder","William Alles","Shop Machinery","MW Vol. 19 No. 1 Feb-Mar 2006","26"
    "The Gunsmith Machinist: Lengthening a Winchester 97 Chamber","Steve Acker","Gunsmithing","MW Vol. 19 No. 1 Feb-Mar 2006","32"
    "The Tool Room: My Dream Angle Plate Shim","James W. Hauser","Shop Accessories","MW Vol. 19 No. 1 Feb-Mar 2006","39"
    "Bolt Puzzle","Roger Wiley","Projects","MW Vol. 19 No. 1 Feb-Mar 2006","40"
    "Making Perfect Graduated Dials","Allen Blaney","Machine Modifications","MW Vol. 19 No. 2 Apr-May 2006","6"
    "Band Saw Improvements","Chet McClellan","Shop Machinery","MW Vol. 19 No. 2 Apr-May 2006","12"
    "Frank McLean's Sheet Metal Drills","Charles St. Louis","Shop Accessories","MW Vol. 19 No. 2 Apr-May 2006","20"
    "Another Quick-Change Tool Post - Part One","Mike Hoff","Lathes","MW Vol. 19 No. 2 Apr-May 2006","26"
    "Measure Bolt Hole Centers the Easy Way","Wayne Woods","Measuring & Layout","MW Vol. 19 No. 2 Apr-May 2006","34"
    "A Powered Door","Ronald G. Casteel","Projects","MW Vol. 19 No. 2 Apr-May 2006","36"
    "The Gunsmith Machinist: A Gunsmith's Grinder Bit Handles","Steve Acker","Gunsmithing","MW Vol. 19 No. 2 Apr-May 2006","36"
    "The Gunsmith Machinist: A Gunsmith's Grinder Bit Handles","Steve Acker","Gunsmithing","MW Vol. 19 No. 2 Apr-May 2006","41"
    "The Tool Room: Chuck Key Holder for a Logan Lathe","James W. Hauser","Lathes","MW Vol. 19 No. 2 Apr-May 2006","45"
    "A Better Powder Measure","J. Randolph Bulgin","Projects","MW Vol. 19 No. 3 Jun-Jul 2006","6"
    "Another Quick-Change Tool Pos - Part Two","Mike Hoff","Lathes","MW Vol. 19 No. 3 Jun-Jul 2006","14"
    "Spring Loaded Key Ring","Walter Yetman","Projects","MW Vol. 19 No. 3 Jun-Jul 2006","26"
    "Dealing with Stuck Machine Screws and Broken Springs","Lowell P. Braxton","Techniques","MW Vol. 19 No. 3 Jun-Jul 2006","30"
    "Make an Optical Center Punch","Dick Saunders","Shop Accessories","MW Vol. 19 No. 3 Jun-Jul 2006","33"
    "An Inexpensive Quill DRO for your Mill","Gregory Whitney","Mills","MW Vol. 19 No. 3 Jun-Jul 2006","34"
    "My Mini-Lathe","Jim Reynolds","Lathes","MW Vol. 19 No. 3 Jun-Jul 2006","38"
    "The Gunsmith Machinist: Jewelling a Rifle Bolt","Steve Acker","Gunsmithing","MW Vol. 19 No. 3 Jun-Jul 2006","40"
    "The Tool Room: Scrap Box Puzzle","James W. Hauser","Projects","MW Vol. 19 No. 3 Jun-Jul 2006","45"
    "Compact Boring Head for a Unimat SL","Theodore M. Clarke","Lathes","MW Vol. 19 No. 4 Aug-Sep 2006","6"
    "The South Bend Lathe Rebuild Program","Bill Johnston","Lathes","MW Vol. 19 No. 4 Aug-Sep 2006","20"
    "Radial Center Finders for the Drill Press","John W. Way","Machine Tools","MW Vol. 19 No. 4 Aug-Sep 2006","26"
    "Air Support","George Christensen","Shop Accessories","MW Vol. 19 No. 4 Aug-Sep 2006","30"
    "1-2-3.Nuts! An Accessory for Joining 1-2-3 Blocks Together","Nick Carter","Shop Accessories","MW Vol. 19 No. 4 Aug-Sep 2006","34"
    "Anodizing Aluminum on a Shoestring","Dewey Dirrim","Techniques","MW Vol. 19 No. 4 Aug-Sep 2006","38"
    "The Gunsmith Machinist: Widening a Rear Sight Notch","Corrine Hummel","Gunsmithing","MW Vol. 19 No. 4 Aug-Sep 2006","40"
    "The Tool Room: The Lathe Shelf","James W. Hauser","Lathes","MW Vol. 19 No. 4 Aug-Sep 2006","44"
    "Photography Tripod Adapter","Chet McClellan","Hobby Items","MW Vol. 19 No. 5 Oct-Nov 2006","6"
    "Tooling up a Mill-Drill","Lowell P. Braxton","Machine Modifications","MW Vol. 19 No. 5 Oct-Nov 2006","6"
    "Building the Little Brassy Stirling Engine","Charles St. Louis","Engines","MW Vol. 19 No. 5 Oct-Nov 2006","16"
    "First Class Letter Opener","Walter Yetman","Hobby Items","MW Vol. 19 No. 5 Oct-Nov 2006","26"
    "Dial Indicator Holder-Holder","Karl Schulz","Lathes","MW Vol. 19 No. 5 Oct-Nov 2006","29"
    "Mounting Ball Handles on a Mini Mill","Bob Hadley","Machine Modifications","MW Vol. 19 No. 5 Oct-Nov 2006","30"
    "Using Bowed Shafting for Turned Parts","Randall R. Geib","Techniques","MW Vol. 19 No. 5 Oct-Nov 2006","32"
    "The Gunsmith Machinist: A Cartridge-Specific Powder Funnel Tunnel","Corrine Hummel","Gunsmithing","MW Vol. 19 No. 5 Oct-Nov 2006","34"
    "Enhanced Optical Center Punch","Arnold Gregrich","Measuring & Layout","MW Vol. 19 No. 5 Oct-Nov 2006","38"
    "A 5C Collet Stop","Ronald Geppert","Lathes","MW Vol. 19 No. 5 Oct-Nov 2006","40"
    "The Tool Room: Lathe Die Holders","James W. Hauser","Lathes","MW Vol. 19 No. 5 Oct-Nov 2006","43"
    "Build a Beam Compass that Doubles as a Marking Gage","Ray Shoberg","Measuring & Layout","MW Vol. 19 No. 6 Dec 2006-Jan 2007","12"
    "Build a Cutoff Attachment for Your Lathe","Bob Nelson","Lathes","MW Vol. 19 No. 6 Dec 2006-Jan 2007","18"
    "Lathe Tool Panel","Conrad A. Huard","Shop Accessories","MW Vol. 19 No. 6 Dec 2006-Jan 2007","22"
    "Flip-up Vise Stop","Jonathan Hogg","Hand Tools","MW Vol. 19 No. 6 Dec 2006-Jan 2007","26"
    "Using the Versa Mill in the Lathe","Gale Miles","Techniques","MW Vol. 19 No. 6 Dec 2006-Jan 2007","30"
    "Using the Versa Mill in the Lathe","Gale Miles","Techniques","MW Vol. 19 No. 6 Dec 2006-Jan 2007","30"
    "Mobile Anvil Stand","Dan Morell","Hobby Items","MW Vol. 19 No. 6 Dec 2006-Jan 2007","34"
    "The Gunsmith Machinist: Installing Colored Light Inserts","Corrine Hummel","Gunsmithing","MW Vol. 19 No. 6 Dec 2006-Jan 2007","36"
    "The Tool Room: South Bend Drill Press Stop","James W. Hauser","Shop Machinery","MW Vol. 19 No. 6 Dec 2006-Jan 2007","42"
    "Supplemental Index Plates for a Mini Rotary Table","Cristie Rethman","Measuring & Layout","MW Vol. 20 No. 1 Feb-Mar 2007","6"
    "Make a Set of Chuck Stops","James A. Hornicek","Lathes","MW Vol. 20 No. 1 Feb-Mar 2007","18"
    "Improved Threading Arm for the Unimat","Theodore M. Clarke","Machine Modifications","MW Vol. 20 No. 1 Feb-Mar 2007","24"
    "Vise Restoration","Mike Fendley","Shop Accessories","MW Vol. 20 No. 1 Feb-Mar 2007","28"
    "A MIG Torch Caddy","Karl Schulz","Welding/Foundry/Forging","MW Vol. 20 No. 1 Feb-Mar 2007","30"
    "Tipping Layout Tools with Tungsten Carbide","Jesse Livingston","Techniques","MW Vol. 20 No. 1 Feb-Mar 2007","32"
    "Book Review: The Backyard Blacksmith, by Lorelei Sims","Otto Bacon","Hobby Community","MW Vol. 20 No. 1 Feb-Mar 2007","34"
    "A Clean File Cuts True","Wayne Woods","Techniques","MW Vol. 20 No. 1 Feb-Mar 2007","35"
    "The Gunsmith Machinist: The Micrometer Adjustable Reamer Stop","Corrine Hummel","Gunsmithing","MW Vol. 20 No. 1 Feb-Mar 2007","36"
    "The Tool Room: An Indicator Holder","James W. Hauser","Shop Accessories","MW Vol. 20 No. 1 Feb-Mar 2007","40"
    "A Simple 5C Collet Attachment","Thomas Morrison","Lathes","MW Vol. 20 No. 2 Apr-May 2007","6"
    "Panel Saw","Ronald G. Casteel","Shop Machinery","MW Vol. 20 No. 2 Apr-May 2007","14"
    "Machining with a Coolant/Vacuum System","Wil Nise","Shop Accessories","MW Vol. 20 No. 2 Apr-May 2007","26"
    "Paint Trick for Raised Lettering","Otto Bacon","Hobby Items","MW Vol. 20 No. 2 Apr-May 2007","28"
    "Alternative Lathe Boring Table","Gary Vriezen","Lathes","MW Vol. 20 No. 2 Apr-May 2007","30"
    "Adding an Over-arm to a Barker Milling Machine","Gregg Goodwill","Machine Modifications","MW Vol. 20 No. 2 Apr-May 2007","32"
    "Six-Inch Calculator","Frank Ford","Measuring & Layout","MW Vol. 20 No. 2 Apr-May 2007","34"
    "Testing Different Types of Penetrating Oils","Lloyd Bender","General Machining Knowledge","MW Vol. 20 No. 2 Apr-May 2007","35"
    "Lathe Spindle Crank","Allan Moore","Machine Modifications","MW Vol. 20 No. 2 Apr-May 2007","36"
    "Centering an AR15 Front Sight","Corrine Hummel","Gunsmithing","MW Vol. 20 No. 2 Apr-May 2007","38"
    "The Tool Room: Milling Machine Manual Shaper Tool","James W. Hauser","Machine Modifications","MW Vol. 20 No. 2 Apr-May 2007","45"
    "Welded Quick-change Toolholders","Arnold Gregrich","Welding/Foundry/Forging","MW Vol. 20 No. 3 Jun-Jul 2007","6"
    "The Poor Man's DRO","Robert Beaupre","Measuring & Layout","MW Vol. 20 No. 3 Jun-Jul 2007","11"
    "Beating the Heat in the Shop","David Kumhyr","Shop Accessories","MW Vol. 20 No. 3 Jun-Jul 2007","22"
    "The Gunsmith Machinist: Protective Center for a Rifle Barrel","Corrine Hummel","Gunsmithing","MW Vol. 20 No. 3 Jun-Jul 2007","38"
    "The Tool Room: Straight Tap Wrench","James W. Hauser","Machine Modifications","MW Vol. 20 No. 3 Jun-Jul 2007","42"
    "End Mill Adapter for a Sherline Mill","Norm Wells","Machine Modifications","MW Vol. 20 No. 3 Jun-Jul 2007","44"
    "New Light for your Lantern Tool Post","Charles St. Louis","Lathes","MW Vol. 20 No. 4 Aug-Sep 2007","6"
    "Quick-change Gearbox for a Chinese Mini-lathe","Lex Liberato","Lathes","MW Vol. 20 No. 4 Aug-Sep 2007","18"
    "Improving Cut-off Saw Performance","Cristie Rethman","Miscellaneous","MW Vol. 20 No. 4 Aug-Sep 2007","24"
    "Bolt Vise for the AR-15/M-16","Jim Swartz","Gunsmithing","MW Vol. 20 No. 4 Aug-Sep 2007","29"
    "Adding Oiling Fittings to your Mill Table","John Felgenhauer","Machine Modifications","MW Vol. 20 No. 4 Aug-Sep 2007","34"
    "The Gunsmith Machinist: Lathe Cutting Threads on Blank Screws","Corrine Hummel","Gunsmithing","MW Vol. 20 No. 4 Aug-Sep 2007","36"
    "The Tool Room: Indicator Attachment","James W. Hauser","Measuring & Layout","MW Vol. 20 No. 4 Aug-Sep 2007","45"
    "Threading","J. Randolph Bulgin","Techniques","MW Vol. 20 No. 5 Oct-Nov 2007","6"
    "Cutting Screws and Other Short Pieces of Metal to Length","Chet McClellan","Shop Accessories","MW Vol. 20 No. 5 Oct-Nov 2007","18"
    "Quick and Easy Form Tool -- Recycling Your Old Files","Frank Ford","Hand Tools","MW Vol. 20 No. 5 Oct-Nov 2007","28"
    "Quick Change Saw Table","Myles Milner","Machine Modifications","MW Vol. 20 No. 5 Oct-Nov 2007","32"
    "Weld Aluminum with a Torch","Allan Moore","Welding/Foundry/Forging","MW Vol. 20 No. 5 Oct-Nov 2007","36"
    "The Gunsmith Machinist: Surface Grinding a Remington Recoil Lug","Corrine Hummel","Gunsmithing","MW Vol. 20 No. 5 Oct-Nov 2007","38"
    "The Tool Room: Adapting a CDCO 6 V-jaw to fit a Kurt Vise","James W. Hauser","Machine Modifications","MW Vol. 20 No. 5 Oct-Nov 2007","47"
    "Drill Press-to-Mill Modifications","James A. Hornicek","Machine Modifications","MW Vol. 20 No. 6 Dec 2007-Jan 2008","6"
    "Ring Roller","Otto Bacon","Shop Accessories","MW Vol. 20 No. 6 Dec 2007-Jan 2008","14"
    "Black Iron Days","Neil Knopf","Welding/Foundry/Forging","MW Vol. 20 No. 6 Dec 2007-Jan 2008","24"
    "Debunking the Myths of the Gap-bed Lathe","J. Randolph Bulgin","Lathes","MW Vol. 20 No. 6 Dec 2007-Jan 2008","26"
    "Adapting a Quick-change Tool Post to a 9 x 29 Lathe","James Johnston","Machine Modifications","MW Vol. 20 No. 6 Dec 2007-Jan 2008","32"
    "The Gunsmith Machinist: Line Boring a Ruger to .45 Colt - Part One","Corrine Hummel","Gunsmithing","MW Vol. 20 No. 6 Dec 2007-Jan 2008","36"
    "Telescoping Magnetic Pick-up Tool","Walter Yetman","Shop Accessories","MW Vol. 20 No. 6 Dec 2007-Jan 2008","42"
    "The Tool Room: The Bumper Jack Arbor Press","James W. Hauser","Shop Accessories","MW Vol. 20 No. 6 Dec 2007-Jan 2008","47"
    "Armillary Sphere","Otto Bacon","Hobby Items","MW Vol. 21 No. 1 Feb-Mar 2008","6"
    "Blade Sharpening Attachment for a Bench Grinder","William J. Alles, Jr.","Shop Accessories","MW Vol. 21 No. 1 Feb-Mar 2008","10"
    "Skin-off-the-Back Transmission","Charles St. Louis","Lathes","MW Vol. 21 No. 1 Feb-Mar 2008","18"
    "Simple Air Hose Reel","Ronald Schultz","Shop Accessories","MW Vol. 21 No. 1 Feb-Mar 2008","24"
    "Homebuilt Surface Gage","James S. McKnight","Shop Accessories","MW Vol. 21 No. 1 Feb-Mar 2008","26"
    "Small, Inexpensive Light Source for Your Machines","Dick Saunders","Shop Accessories","MW Vol. 21 No. 1 Feb-Mar 2008","30"
    "The Gunsmith Machinist: Line Boring a Ruger to .45 Colt - Part Two","Corrine Hummel","Gunsmithing","MW Vol. 21 No. 1 Feb-Mar 2008","32"
    "The Tool Room: Improved Optical Center Punch Base","James W. Hauser","Shop Accessories","MW Vol. 21 No. 1 Feb-Mar 2008","40"
    "Another Lathe Tailstock Die Holder - a Modular Approach","Herbert  Yohe","Lathes","MW Vol. 21 No. 2 Apr-May 2008","7"
    "Shop Notes for Building a Treadle-powered Wood Lathe","Lowell P. Braxton","Shop Machinery","MW Vol. 21 No. 2 Apr-May 2008","10"
    "Drill Press Modification","Mark  Whitmore","Machine Modifications","MW Vol. 21 No. 2 Apr-May 2008","24"
    "A Quick Swivel Base","Steve  Marshall","Shop Accessories","MW Vol. 21 No. 2 Apr-May 2008","27"
    "Bulgin, J. Randolph","J. Randolph Bulgin","Hobby Community","MW Vol. 21 No. 2 Apr-May 2008","28"
    "A Low-cost Way of Converting your Lathe to Variable Speed","Charlie Briggs","Lathes","MW Vol. 21 No. 2 Apr-May 2008","30"
    "Tricks for Centering on the Four-jaw Chuck","Earl Wilms","Techniques","MW Vol. 21 No. 2 Apr-May 2008","32"
    "Center-Drills","Lloyd Bender","Shop Accessories","MW Vol. 21 No. 2 Apr-May 2008","34"
    "Simplifying the Belt Changing/tightening Process on a Mill-drill","Gordon Tengen","Machine Modifications","MW Vol. 21 No. 2 Apr-May 2008","35"
    "The Gunsmith Machinist: Line Boring a Ruger to .45 Colt - Part Three","Corrine Hummel","Gunsmithing","MW Vol. 21 No. 2 Apr-May 2008","38"
    "The Tool Room: Improved 5C Collet Stop","James W. Hauser","Lathes","MW Vol. 21 No. 2 Apr-May 2008","46"
    "Build a Rotary Valve Engine","Walter  Yetman","Engines","MW Vol. 21 No. 3 Jun-Jul 2008","7"
    "An Easy Honing Fixture","James S. McKnight","Shop Accessories","MW Vol. 21 No. 3 Jun-Jul 2008","14"
    "Machine Feet on the Cheap","Jim  Sturmer","Machine Modifications","MW Vol. 21 No. 3 Jun-Jul 2008","20"
    "The Grizzly G3003G Gunsmith Lathe","Corrine  Hummel","Gunsmithing","MW Vol. 21 No. 3 Jun-Jul 2008","24"
    "Handy Angle Plate You May Already Have in Your Shop","Otto  Bacon","Shop Accessories","MW Vol. 21 No. 3 Jun-Jul 2008","35"
    "Improved Tailstock Clamp for Small Lathes","R  Mounier","Lathes","MW Vol. 21 No. 3 Jun-Jul 2008","36"
    "The Gunsmith Machinist: Line Boring a Ruger to .45 Colt - Part Four","Corrine  Hummel","Gunsmithing","MW Vol. 21 No. 3 Jun-Jul 2008","38"
    "The Tool Room: Tailstock Indicator Holder","James W. Hauser","Lathes","MW Vol. 21 No. 3 Jun-Jul 2008","46"
    "The Care and Feeding of the Common Twist Drill","J. Randolph  Bulgin","Shop Accessories","MW Vol. 21 No. 4 Aug-Sep 2008","7"
    "A Ball Turning Attachment from the Past","Paul J. Holm","Lathes","MW Vol. 21 No. 4 Aug-Sep 2008","15"
    "Making a Triplex Flycutter","Lowell P. Braxton","Machine Modifications","MW Vol. 21 No. 4 Aug-Sep 2008","20"
    "Circle Cutting Attachment for Plasma Cutters","Rich  Mancini","Welding/Foundry/Forging","MW Vol. 21 No. 4 Aug-Sep 2008","24"
    "Mill Lever Extension","F. A. Pellizzari","Machine Modifications","MW Vol. 21 No. 4 Aug-Sep 2008","28"
    "M1 Firing Pin and Barrel Gas Port Gages","Jim  Swartz","Gunsmithing","MW Vol. 21 No. 4 Aug-Sep 2008","30"
    "The Tool Room: Adjustable Lathe Dog","James W. Hauser","Lathes","MW Vol. 21 No. 4 Aug-Sep 2008","32"
    "Make a Pipe Vise","Stephen  Chastain","Projects","MW Vol. 21 No. 4 Aug-Sep 2008","35"
    "The Gunsmith Machinist: Line Boring a Ruger to .45 Colt - Part Five","Corrine  Hummel","Gunsmithing","MW Vol. 21 No. 4 Aug-Sep 2008","36"
    "Boring Head Extension","Wayne  Woods","Machine Modifications","MW Vol. 21 No. 4 Aug-Sep 2008","44"
    "The Tool Room: Angle Block Fixture","James W. Hauser","Measuring & Layout","MW Vol. 21 No. 4 Aug-Sep 2008","45"
    "Not So Poor Man's Transfer Punches","Charles  St. Louis","Hand Tools","MW Vol. 21 No. 5 Oct-Nov 2008","7"
    "Accessories for a Mill-Drill","Gary  Paine","Machine Modifications","MW Vol. 21 No. 5 Oct-Nov 2008","18"
    "A Two-in-One Gunsmithing","Paul  Smeltzer","Gunsmithing","MW Vol. 21 No. 5 Oct-Nov 2008","24"
    "A Machinist's Tent Stakes","Corrine  Hummel","Hobby Items","MW Vol. 21 No. 5 Oct-Nov 2008","26"
    "Poor Man's Collet Chuck","Bob  Mansfield","Lathes","MW Vol. 21 No. 5 Oct-Nov 2008","30"
    "Salt Cellar","Gary  Repesh","Hobby Items","MW Vol. 21 No. 5 Oct-Nov 2008","32"
    "Wrench/Hammer Combo","Phil  Lipoma","Engines","MW Vol. 21 No. 5 Oct-Nov 2008","35"
    "The Gunsmith Machinist: Line Boring a Ruger to .45 Colt - Part Six","Corrine  Hummel","Gunsmithing","MW Vol. 21 No. 5 Oct-Nov 2008","36"
    "The Tool Room: A No. 2 Morse Center Drill Adapter","James W. Hauser","Shop Accessories","MW Vol. 21 No. 5 Oct-Nov 2008","46"
    "Rolling Steady Rest for the Sherline Lathe","Vince  Pugliese","Lathes","MW Vol. 21 No. 6 Dec 2008-Jan 2009","7"
    "Forward Mounting a Reflex Sight on a Bolt Action Rifle","Mark  Blankenau","Gunsmithing","MW Vol. 21 No. 6 Dec 2008-Jan 2009","11"
    "Building a Motor Pedestal for a Lathe","Thomas  Morrison","Machine Modifications","MW Vol. 21 No. 6 Dec 2008-Jan 2009","18"
    "Hydraulic Tracer for the Home Shop","James  Hannum","Shop Accessories","MW Vol. 21 No. 6 Dec 2008-Jan 2009","22"
    "Modify a Swing-Back Trailer Jack","Joe  Harmon","Projects","MW Vol. 21 No. 6 Dec 2008-Jan 2009","27"
    "Low Profile Vise","Jerrold  Tiers","Shop Accessories","MW Vol. 21 No. 6 Dec 2008-Jan 2009","30"
    "Shim Punch","Don  Wiederhold","Shop Accessories","MW Vol. 21 No. 6 Dec 2008-Jan 2009","34"
    "Attaching a Vise to a Drill Press","Jack  Lundigran","Shop Accessories","MW Vol. 21 No. 6 Dec 2008-Jan 2009","35"
    "Attaching a Vise to a Drill Press","Jack  Lundigran","Shop Accessories","MW Vol. 21 No. 6 Dec 2008-Jan 2009","35"
    "The Gunsmith Machinist: Line Boring a Ruger to .45 Colt - Part Seven","Steve  Acker","Gunsmithing","MW Vol. 21 No. 6 Dec 2008-Jan 2009","36"
    "The Tool Room: Aerator Wrench","James W. Hauser","Projects","MW Vol. 21 No. 6 Dec 2008-Jan 2009","43"
    "Book Review: Machining Projects by David Avery","James W. Hauser","Hobby Community","MW Vol. 21 No. 6 Dec 2008-Jan 2009","45"
    "Candleholders Revisited","John W. Foster","Projects","MW Vol. 22 No. 1 Feb-Mar 2009","4"
    "Optimizing a Milling Attachment on a Lathe","Mogens  Kilde","Lathes","MW Vol. 22 No. 1 Feb-Mar 2009","10"
    "A Horizontal Milling Machine","J. Randolph  Bulgin","Mills","MW Vol. 22 No. 1 Feb-Mar 2009","15"
    "Dad's Old Tool Box","Otto  Bacon","Miscellaneous","MW Vol. 22 No. 1 Feb-Mar 2009","20"
    "Making a Boring Bar Toolholder","Gary  Paine","Projects","MW Vol. 22 No. 1 Feb-Mar 2009","24"
    "Sand Heater for the Home Shop Foundry","James A. Hornicek","Welding/Foundry/Forging","MW Vol. 22 No. 1 Feb-Mar 2009","27"
    "The Gunsmith Machinist: A Varmint Hunting Scope Mount for the AR-15","Steve  Acker","Gunsmithing","MW Vol. 22 No. 1 Feb-Mar 2009","37"
    "The Tool Room: Storage Box","James W. Hauser","Projects","MW Vol. 22 No. 1 Feb-Mar 2009","37"
    "A Brass Bouquet for Mother's Day","Walter  Yetman","Projects","MW Vol. 22 No. 2 Apr-May 2009","4"
    "Yet Another Treadmill Motor Powered Machine Tool","Jeff  Clark","Mills","MW Vol. 22 No. 2 Apr-May 2009","9"
    "A Tool Post Grinder","Jon  Nelson","Lathes","MW Vol. 22 No. 2 Apr-May 2009","13"
    "Reversible Vise Jaws","Dick  Saunders","Shop Accessories","MW Vol. 22 No. 2 Apr-May 2009","26"
    "Snap Caps","Tim  Clarke","Gunsmithing","MW Vol. 22 No. 2 Apr-May 2009","28"
    "A Way to Sharpen Lathe Tools","H. D. Candland","General Machining Knowledge","MW Vol. 22 No. 2 Apr-May 2009","30"
    "The Gunsmith Machinist: A Rifle Target Stand from Pipe","Steve  Acker","Gunsmithing","MW Vol. 22 No. 2 Apr-May 2009","33"
    "Book Review: Machine Shop Essentials -- Questions and Answers","Craig  Foster","Hobby Community","MW Vol. 22 No. 2 Apr-May 2009","40"
    "The Tool Room: Bridgeport Digital Readout","James W. Hauser","Mills","MW Vol. 22 No. 2 Apr-May 2009","41"
    "General Purpose Gear Cutter Attachment for the Sherline Mill","Jim  Hansen","Mills","MW Vol. 22 No. 3 Jun-Jul 2009","4"
    "Narrow Belt Sander - Part One","James S. McKnight","Shop Machinery","MW Vol. 22 No. 3 Jun-Jul 2009","10"
    "Motorized Playing Card Shuffler","Donald R. Oswald","Projects","MW Vol. 22 No. 3 Jun-Jul 2009","18"
    "Building the M1 Trigger Housing Assembly Fixture","Jim  Swartz","Gunsmithing","MW Vol. 22 No. 3 Jun-Jul 2009","24"
    "Power Feed for a Sherline Lathe","Dewey  Dirrim","Lathes","MW Vol. 22 No. 3 Jun-Jul 2009","27"
    "Homemade Welding Cart","Don  Wiederhold","Welding/Foundry/Forging","MW Vol. 22 No. 3 Jun-Jul 2009","33"
    "The Gunsmith Machinist: An Emergency Garand Op Rod Repair","Steve  Acker","Gunsmithing","MW Vol. 22 No. 3 Jun-Jul 2009","36"
    "The Tool Room: Fine Feed Bridgeport Handle","James W. Hauser","Projects","MW Vol. 22 No. 3 Jun-Jul 2009","40"
    "Old Man's Lever Dolly","Ronald  Geppert","Shop Accessories","MW Vol. 22 No. 3 Jun-Jul 2009","45"
    "Modifying a Plunger Indicator to Read Internal Threads","Ray  Katzmar","Shop Accessories","MW Vol. 22 No. 3 Jun-Jul 2009","47"
    "Building a Steady Rest","John  Bergmann","Lathes","MW Vol. 22 No. 4 Aug-Sep 2009","5"
    "G.A. Ewen's Engine Mill -- My version","Myles  Milner","Mills","MW Vol. 22 No. 4 Aug-Sep 2009","15"
    "An EpiPen Case","Alan  Anganes","Projects","MW Vol. 22 No. 4 Aug-Sep 2009","22"
    "M1 Clip Conversion for Single Shot Loading","Jim  Swartz","Gunsmithing","MW Vol. 22 No. 4 Aug-Sep 2009","26"
    "Band Saw Modifications","Norm  Whittaker","Shop Machinery","MW Vol. 22 No. 4 Aug-Sep 2009","28"
    "Oil Can on the Cheap","Henry J. Kratt","Shop Accessories","MW Vol. 22 No. 4 Aug-Sep 2009","30"
    "Safe and Easy Way to Change the Blade on a Band Saw","R.G.  Sparber","Shop Machinery","MW Vol. 22 No. 4 Aug-Sep 2009","33"
    "Narrow Belt Sander - Part Two","James S. McKnight","Shop Machinery","MW Vol. 22 No. 4 Aug-Sep 2009","34"
    "The Gunsmith Machinist: Making Thin Firearm Washers","Steve  Acker","Gunsmithing","MW Vol. 22 No. 4 Aug-Sep 2009","39"
    "The Tool Room: Answering Machine Table","James W. Hauser","Projects","MW Vol. 22 No. 4 Aug-Sep 2009","44"
    "A Quick Double - Part One","Fred  Prestridge","Gunsmithing","MW Vol. 22 No. 5 Oct-Nov 2009","5"
    "A Propane Torch for the Workshop","Edward  Hume","Welding/Foundry/Forging","MW Vol. 22 No. 5 Oct-Nov 2009","17"
    "Looking for a Project? Whistle!","Walter  Yetman","Projects","MW Vol. 22 No. 5 Oct-Nov 2009","24"
    "A Spindle Support for Your 8 Drill-to-Mill Conversion","James A. Hornicek","Mills","MW Vol. 22 No. 5 Oct-Nov 2009","28"
    "Make a Cathead","Leonard  Waring","Lathes","MW Vol. 22 No. 5 Oct-Nov 2009","34"
    "Mill-drill Improvement II","Gordon  Tengen","Mills","MW Vol. 22 No. 5 Oct-Nov 2009","35"
    "A Fast Vise Stop","Paul  Alciatore","Shop Accessories","MW Vol. 22 No. 5 Oct-Nov 2009","36"
    "A Carriage Indicator","Dennis  Sardi","Lathes","MW Vol. 22 No. 5 Oct-Nov 2009","37"
    "The Gunsmith Machinist: M1A Bolt Roller Grease Tool","Steve  Acker","Gunsmithing","MW Vol. 22 No. 5 Oct-Nov 2009","39"
    "The Tool Room: Wing!","James W. Hauser","Shop Accessories","MW Vol. 22 No. 5 Oct-Nov 2009","44"
    "Adapting the Taig Milling Attachment to the Sherline Lathe","Vince  Pugliese","Lathes","MW Vol. 22 No. 6 Dec 2009-Jan 2010","5"
    "Making a Mill-drill Y-axis Travel Stop","Lowell P. Braxton","Mills","MW Vol. 22 No. 6 Dec 2009-Jan 2010","11"
    "An Adapter for Mounting a Camera to a Microscope","Lloyd  Bender","Projects","MW Vol. 22 No. 6 Dec 2009-Jan 2010","15"
    "The Display Stand","Weston  Bye","Projects","MW Vol. 22 No. 6 Dec 2009-Jan 2010","18"
    "A Quick Double - Part Two","Fred  Prestridge","Gunsmithing","MW Vol. 22 No. 6 Dec 2009-Jan 2010","23"
    "Tool Post Grinder","William J. Alles, Jr.","Lathes","MW Vol. 22 No. 6 Dec 2009-Jan 2010","32"
    "The Gunsmith Machinist: Improving a Ruger 10/22 Chamber","Steve  Acker","Gunsmithing","MW Vol. 22 No. 6 Dec 2009-Jan 2010","38"
    "A Low-cost Induction Heater","Ernie  Henne","Welding/Foundry/Forging","MW Vol. 22 No. 6 Dec 2009-Jan 2010","44"
    "Drill Press Vise Holder","","Shop Machinery","MW Vol. 22 No. 6 Dec 2009-Jan 2010","45"
    "The Tool Room: Drill Press Vise Holder","James W. Hauser","Shop Machinery","MW Vol. 22 No. 6 Dec 2009-Jan 2010","45"
    "How to Build a Model -- My Scale 81mm Mortar","Walter  Yetman","Projects","MW Vol. 23 No. 1 Feb-Mar 2010","5"
    "Quick-change Tool Post","Paul  Alciatore","Lathes","MW Vol. 23 No. 1 Feb-Mar 2010","8"
    "Precision Lathe Tailstock Depth Calibration","Tom  McAllister","Lathes","MW Vol. 23 No. 1 Feb-Mar 2010","18"
    "Repairing a Crankshaft Keyseat","Alan  Anganes","Projects","MW Vol. 23 No. 1 Feb-Mar 2010","21"
    "One Man's Trash","Wayne  Hanson","Mills","MW Vol. 23 No. 1 Feb-Mar 2010","25"
    "Reconditioning an M1 Garand Op Rod","John  Viggers","Gunsmithing","MW Vol. 23 No. 1 Feb-Mar 2010","29"
    "Speed Handle for a Hex Shaft Mill Vise","John  Viggers","Mills","MW Vol. 23 No. 1 Feb-Mar 2010","32"
    "Parallel Retainer Clips","John  Mallak","Shop Accessories","MW Vol. 23 No. 1 Feb-Mar 2010","37"
    "The Gunsmithing Machinist: Reworking a Ruger 10/22 Bolt","Steve  Acker","Gunsmithing","MW Vol. 23 No. 1 Feb-Mar 2010","38"
    "The Tool Room: Milling Machine Step Blocks","James W. Hauser","Projects","MW Vol. 23 No. 1 Feb-Mar 2010","42"
    "A Portable Hammer Stand","Brad  Ocock","Shop Accessories","MW Vol. 23 No. 2 Apr-May 2010","5"
    "Building an Engraving Arrangement for a Dremel","Mogens  Kilde","Shop Machinery","MW Vol. 23 No. 2 Apr-May 2010","11"
    "A Combination Spindle Stiffener and Threading Aid","David J Graves","Lathes","MW Vol. 23 No. 2 Apr-May 2010","20"
    "Anvils","Otto  Bacon","Welding/Foundry/Forging","MW Vol. 23 No. 2 Apr-May 2010","24"
    "A Milling Table","Gary  Vriezen","Mills","MW Vol. 23 No. 2 Apr-May 2010","28"
    "Garden Tractor Brakes Upgrade","Howard  Hull","Projects","MW Vol. 23 No. 2 Apr-May 2010","30"
    "The Gunsmith Machinist: Modifying a Rifle Scope Mount","Steve  Acker","Gunsmithing","MW Vol. 23 No. 2 Apr-May 2010","33"
    "The Tool Room: Backward Arbor","James W. Hauser","Mills","MW Vol. 23 No. 2 Apr-May 2010","38"
    "The Modular Dividing Head","Ted  Hansen","Shop Machinery","MW Vol. 23 No. 3 Jun-Jul 2010","5"
    "A Machinist's Birthday Candle-cade","Peter  Sevier","Projects","MW Vol. 23 No. 3 Jun-Jul 2010","14"
    "A Swaging Die for Paper Patched Bullets","Peter C. Esselburne","Gunsmithing","MW Vol. 23 No. 3 Jun-Jul 2010","16"
    "A Tailstock Quill Scale","Don  Wiederhold","Lathes","MW Vol. 23 No. 3 Jun-Jul 2010","22"
    "A Universal Angle Block","James S. McKnight","Shop Accessories","MW Vol. 23 No. 3 Jun-Jul 2010","24"
    "Electric Tram","Robert  Huffaker","Miscellaneous","MW Vol. 23 No. 3 Jun-Jul 2010","28"
    "Using a Steel Rule","Chris  Wood","General Machining Knowledge","MW Vol. 23 No. 3 Jun-Jul 2010","29"
    "Alternative Layout Method","Andrew  Barrowman","Lathes","MW Vol. 23 No. 3 Jun-Jul 2010","32"
    "Repairing an Antique Radiator Cap","John W. Foster","Projects","MW Vol. 23 No. 3 Jun-Jul 2010","33"
    "The Gunsmith Machinist: A 98 Mauser Receive Shaper Fixture","Steve  Acker","Gunsmithing","MW Vol. 23 No. 3 Jun-Jul 2010","38"
    "The Tool Room: Small Universal Faceplate","","Lathes","MW Vol. 23 No. 3 Jun-Jul 2010","41"
    "The Tool Room: Small Universal Faceplate","James W. Hauser","Shop Accessories","MW Vol. 23 No. 3 Jun-Jul 2010","41"
    "Lathe Slotting Attachment - Part One","Jim  Sterner","Lathes","MW Vol. 23 No. 4 Aug-Sep 2010","5"
    "A New Bench for the Shop","Peter  McKelvey","Shop Accessories","MW Vol. 23 No. 4 Aug-Sep 2010","15"
    "Rotary Phase Converter from a Kit","Leo  Radovich","Mills","MW Vol. 23 No. 4 Aug-Sep 2010","22"
    "A Solution to the Problem of Magazine Storage","George  Gadomski","Projects","MW Vol. 23 No. 4 Aug-Sep 2010","26"
    "Problem Solving Plus Tool Collecting Equals Machining","Paul E Wofford","Lathes","MW Vol. 23 No. 4 Aug-Sep 2010","29"
    "What is a Heat Number?","Ralph  Waters","Welding/Foundry/Forging","MW Vol. 23 No. 4 Aug-Sep 2010","33"
    "The Gunsmith Machinist: A 9mm 1911 for a Lady","Steve  Acker","Gunsmithing","MW Vol. 23 No. 4 Aug-Sep 2010","34"
    "The Tool Room: Homemade Cabinet Latch","James W. Hauser","Projects","MW Vol. 23 No. 4 Aug-Sep 2010","43"
    "A Worm Indexing Module for the Modular Dividing Head","Ted  Hansen","General Machining Knowledge","MW Vol. 23 No. 5 Oct-Nov 2010","5"
    "A Scope Mount Screw Change","Fred  Prestridge","Gunsmithing","MW Vol. 23 No. 5 Oct-Nov 2010","21"
    "A Treadmill Drive for your Lathe","Stan  Stumbo","Lathes","MW Vol. 23 No. 5 Oct-Nov 2010","24"
    "Super Recycle Project - My Own Crucible","Spencer  Schonher","Welding/Foundry/Forging","MW Vol. 23 No. 5 Oct-Nov 2010","27"
    "Vise Stop","Ed  Warren","Shop Accessories","MW Vol. 23 No. 5 Oct-Nov 2010","31"
    "Quick and Easy Angle Cutting","Don  Wiederhold","Mills","MW Vol. 23 No. 5 Oct-Nov 2010","32"
    "Lathe Slotting Attachment - Part Two","Jim  Sterner","Lathes","MW Vol. 23 No. 5 Oct-Nov 2010","34"
    "The Gunsmith Machinist: A 1911 Plunger Tube Staking Tool","","Gunsmithing","MW Vol. 23 No. 5 Oct-Nov 2010","42"
    "The Tool Room: Nice Split Bushings","James W. Hauser","Shop Accessories","MW Vol. 23 No. 5 Oct-Nov 2010","47"
    "4-ton Hydraulic Press","Robert  Yost","Shop Machinery","MW Vol. 23 No. 5 Oct-Nov 2010","50"
    "Scrap Box Rifle Rest","Peter  Esselburne","Projects","MW Vol. 23 No. 6 Dec 2010-Jan 2011","5"
    "Lantern Tool Post Improvement","Paul J. Holm","Lathes","MW Vol. 23 No. 6 Dec 2010-Jan 2011","12"
    "Building a Miniature Lubricating Oil Can","Mogens  Kilde","Shop Accessories","MW Vol. 23 No. 6 Dec 2010-Jan 2011","14"
    "Measuring Screw Threads Over the Wire","James A. Hornicek","General Machining Knowledge","MW Vol. 23 No. 6 Dec 2010-Jan 2011","20"
    "A Handy Dowel Cutter","R Alan Mounier","Shop Accessories","MW Vol. 23 No. 6 Dec 2010-Jan 2011","25"
    "A 3/4" Bridgeport","Charles  St. Louis","Mills","MW Vol. 23 No. 6 Dec 2010-Jan 2011","28"
    "A Quick Fix for a Counterbore Cutter","William  Vander-Reyden","Shop Accessories","MW Vol. 23 No. 6 Dec 2010-Jan 2011","30"
    "Worn Out Brake Rotors Find New Uses","Bart  Buehler","Projects","MW Vol. 23 No. 6 Dec 2010-Jan 2011","33"
    "The Gunsmith Machinist: Modifying a Bullet Mold","Steve  Acker","Gunsmithing","MW Vol. 23 No. 6 Dec 2010-Jan 2011","34"
    "The Tool Room: Optical Center Punch Accessory","James W. Hauser","Shop Accessories","MW Vol. 23 No. 6 Dec 2010-Jan 2011","44"
    "Damascus Steel","Bill  Herndon","Projects","MW Vol. 24 No. 1 Feb-Mar 2011","5"
    "How to Make an Inexpensive "Exact Adjust" 5C Collet Chuck","Gregory  Whitney","Lathes","MW Vol. 24 No. 1 Feb-Mar 2011","11"
    "Turning Up a Rockwell Delta 21-100 Vertical Mill","William  Bentz","Mills","MW Vol. 24 No. 1 Feb-Mar 2011","16"
    "Planer and Shaper Gage","James S. McKnight","Shop Accessories","MW Vol. 24 No. 1 Feb-Mar 2011","20"
    "Door Lock Release Buttons","Thomas  Morrison","Projects","MW Vol. 24 No. 1 Feb-Mar 2011","24"
    "Scrap Hobby Motors","John  Buffum","General Machining Knowledge","MW Vol. 24 No. 1 Feb-Mar 2011","27"
    "Squaring Blocks","Chris  David","Shop Accessories","MW Vol. 24 No. 1 Feb-Mar 2011","30"
    "Spindle Nose Spider","Chris  David","Lathes","MW Vol. 24 No. 1 Feb-Mar 2011","34"
    "The Gunsmith Machinist: Making a Custom Bullet Seater","Steve  Acker","Gunsmithing","MW Vol. 24 No. 1 Feb-Mar 2011","35"
    "The Tool Room: Vertical Band Saw Vise","James W. Hauser","Shop Machinery","MW Vol. 24 No. 1 Feb-Mar 2011","40"
    "The Poor Man's Indexable Toolholder","Ralph  Waters","Lathes","MW Vol. 24 No. 2 Apr-May 2011","4"
    "Salvaging a Rifle Barrel","Lowell P. Braxton","Gunsmithing","MW Vol. 24 No. 2 Apr-May 2011","10"
    "A Home-built Metal Bender","Rich  Mancini","Shop Accessories","MW Vol. 24 No. 2 Apr-May 2011","17"
    "Build Your Own Skunk Trap","Doug  Greene","Projects","MW Vol. 24 No. 2 Apr-May 2011","25"
    "Adapting Taig Components to a Sherline","Marcelo  Jost","Shop Accessories","MW Vol. 24 No. 2 Apr-May 2011","32"
    "The Gunsmith Machinist: Gordy's Method of Rifle Chambering","Steve  Acker","Gunsmithing","MW Vol. 24 No. 2 Apr-May 2011","37"
    "The Tool Room: Building a Tap Guide","James W. Hauser","Shop Accessories","MW Vol. 24 No. 2 Apr-May 2011","41"
    "Bolt Bending Blocks","Fred  Prestridge","Gunsmithing","MW Vol. 24 No. 3 Jun-Jul 2011","5"
    "Build Your Own Oxy-acetylene Pattern-cutting Torch","Gregory  Whitney","Shop Machinery","MW Vol. 24 No. 3 Jun-Jul 2011","11"
    "A Replacement Lead Screw Bearing","Stu  Booher","Lathes","MW Vol. 24 No. 3 Jun-Jul 2011","18"
    "Deep Drilling on a Short Bed","Paul J. Holm","Projects","MW Vol. 24 No. 3 Jun-Jul 2011","20"
    "Building a Hand-held Cherry Pitter","Donald R. Oswald","Projects","MW Vol. 24 No. 3 Jun-Jul 2011","26"
    "Lifting Heavy Chucks onto the Lathe","Ronald  Schultz","Shop Accessories","MW Vol. 24 No. 3 Jun-Jul 2011","29"
    "A Squaring Jig for your Mill","Alan  Goertz","Mills","MW Vol. 24 No. 3 Jun-Jul 2011","30"
    "The Gunsmith Machinist: Turning Down a DPMS LR-308 Barrel","Steve  Acker","Gunsmithing","MW Vol. 24 No. 3 Jun-Jul 2011","33"
    "The Tool Room -- Kurt Vise Jaws","","Shop Accessories","MW Vol. 24 No. 3 Jun-Jul 2011","42"
    "The Tool Room: Kurt Vise Soft Jaws","James W. Hauser","Shop Accessories","MW Vol. 24 No. 3 Jun-Jul 2011","42"
    "A Bench-mounted Spotting Scope Stand","David  Gere","Projects","MW Vol. 24 No. 4 Aug-Sep 2011","4"
    "Carriage Lock for the Sherline Lathe","Vince  Pugliese","Lathes","MW Vol. 24 No. 4 Aug-Sep 2011","15"
    "Sliding Table Band Saw","Otto  Bacon","Shop Machinery","MW Vol. 24 No. 4 Aug-Sep 2011","20"
    "A Dropped Part Finder","Paul  Alciatore","Shop Accessories","MW Vol. 24 No. 4 Aug-Sep 2011","30"
    "A Centering Jig","Carl  Byrns","Shop Accessories","MW Vol. 24 No. 4 Aug-Sep 2011","33"
    "Dividing with a Rotary Table","James  Johnson","General Machining Knowledge","MW Vol. 24 No. 4 Aug-Sep 2011","34"
    "Bridgeport M-head Quill Power Feed","Harvey  Kratz","Mills","MW Vol. 24 No. 4 Aug-Sep 2011","36"
    "The Gunsmith Machinist: Correcting Reamer Chatter","Dave  Manson","Gunsmithing","MW Vol. 24 No. 4 Aug-Sep 2011","37"
    "The Tool Room: A Close-quarter Wrench Adaptor for a Kurt Vise","James W. Hauser","Shop Accessories","MW Vol. 24 No. 4 Aug-Sep 2011","42"
    "My 23-year Project - A 1/7 Scale Model of a German PAK 43/71 Anti-tank Cannon","Bob  Woods","Gunsmithing","MW Vol. 24 No. 5 Oct-Nov 2011","5"
    "Radius Turning Without Special Tooling","Donald  Brouse","General Machining Knowledge","MW Vol. 24 No. 5 Oct-Nov 2011","19"
    "Don't be Limited by a Limit Switch - Rear Mounted X-axis Control Conversion","William  Longyard","Shop Accessories","MW Vol. 24 No. 5 Oct-Nov 2011","22"
    "Making an Impossible Joint - A Dovetail Puzzle","Charles St. Louis","Projects","MW Vol. 24 No. 5 Oct-Nov 2011","26"
    "A Tailstock Fix for a Mini-lathe","Kevin  Castner","Lathes","MW Vol. 24 No. 5 Oct-Nov 2011","32"
    "The Gunsmith Machinist: Cutting Threads to the Right","Steve  Acker","Gunsmithing","MW Vol. 24 No. 5 Oct-Nov 2011","36"
    "The Tool Room: Compound Angle Fixture","James W. Hauser","Shop Accessories","MW Vol. 24 No. 5 Oct-Nov 2011","40"
    "Adapting a Welder to use Smaller Wire Spools","Alan  Anganes","Welding/Foundry/Forging","MW Vol. 24 No. 5 Oct-Nov 2011","44"
    "Snap Caps","Fred  Prestridge","Gunsmithing","MW Vol. 24 No. 6 Dec 2011-Jan 2012","4"
    "Laser Printing on Any Clean, Smooth Surface","R.G.  Sparber","Projects","MW Vol. 24 No. 6 Dec 2011-Jan 2012","8"
    "Making a Forming Die for Pull-handles","Thomas  Morrison","Projects","MW Vol. 24 No. 6 Dec 2011-Jan 2012","10"
    "Lubricating the Cross-slide Nut on a South Bend Lathe","Doug  Ripka","Lathes","MW Vol. 24 No. 6 Dec 2011-Jan 2012","16"
    "Recycling Steel","Ernie  Henne","General Machining Knowledge","MW Vol. 24 No. 6 Dec 2011-Jan 2012","18"
    "A Simple Parallel Holder for the Milling Vise","David J Graves","Shop Accessories","MW Vol. 24 No. 6 Dec 2011-Jan 2012","26"
    "Outboard Bearing","J. Randolph  Bulgin","Lathes","MW Vol. 24 No. 6 Dec 2011-Jan 2012","32"
    "The Gunsmith Machinist: Cutting a Gordy Crown on a Short Barrel","Steve  Acker","Gunsmithing","MW Vol. 24 No. 6 Dec 2011-Jan 2012","39"
    "The Tool Room: Angle Plate Nuts","James W. Hauser","Shop Accessories","MW Vol. 24 No. 6 Dec 2011-Jan 2012","44"
    "A Lot of Work for a Little Job: Making a Breech Plug Jig","Dr. Kurt  Hillig","Gunsmithing","MW Vol. 25 No. 1 Feb-Mar 2012","4"
    "Screw Threads of the World Unite (If All Goes to Plan!)","Martin  Gearing","General Machining Knowledge","MW Vol. 25 No. 1 Feb-Mar 2012","13"
    "Hand Knurler","David  Bradley","Shop Machinery","MW Vol. 25 No. 1 Feb-Mar 2012","18"
    "A Manually Operated Vertically Transposing Machine for the Extraction of Fermentation Seals","Peter C. Esselburne","Projects","MW Vol. 25 No. 1 Feb-Mar 2012","26"
    "Build Your Own Oxy-Acetylene Pattern-Cutting Torch: Drive System Upgrade","Gregory  Whitney","Shop Machinery","MW Vol. 25 No. 1 Feb-Mar 2012","34"
    "The Gunsmith Machinist: Opening Up a Bentz Chamber","Steve  Acker","Gunsmithing","MW Vol. 25 No. 1 Feb-Mar 2012","37"
    "The Tool Room: Cross Slide Indicator Holder","James W. Hauser","Lathes","MW Vol. 25 No. 1 Feb-Mar 2012","42"
    "The Gunsmith Machinist: A Bolt Carrier Weight","Steve  Acker","Gunsmithing","MW Vol. 25 No. 2 Apr-May 2012","0"
    "A Completely Adjustable Camera Mount","Don  Byrnes","Projects","MW Vol. 25 No. 2 Apr-May 2012","4"
    "Poor Man's Expandable Collet","Peter  Arnold","Shop Accessories","MW Vol. 25 No. 2 Apr-May 2012","12"
    "From the Scrap Box - A Support Stand","Tim  Clarke","Shop Accessories","MW Vol. 25 No. 2 Apr-May 2012","14"
    "An Engraving Machine","James S. McKnight","Shop Machinery","MW Vol. 25 No. 2 Apr-May 2012","16"
    "Using Sector Arms on the Dividing Head","Martin  Gearing","General Machining Knowledge","MW Vol. 25 No. 2 Apr-May 2012","27"
    "Cutter Storage","Jerrold  Tiers","Projects","MW Vol. 25 No. 2 Apr-May 2012","28"
    "Quill Lock Problem Solved","Richard  Sevigny","Mills","MW Vol. 25 No. 2 Apr-May 2012","39"
    "The Tool Room: Business Card Holder","James W. Hauser","Projects","MW Vol. 25 No. 2 Apr-May 2012","42"
    "5C Spin Indexer Modifications","Carl  Blum","Shop Accessories","MW Vol. 25 No. 3 Jun-Jul 2012","4"
    "A New Tool for the Shop: A Fixed Scriber Block","Charles  St. Louis","Shop Accessories","MW Vol. 25 No. 3 Jun-Jul 2012","10"
    "Get More from Your Digital Readouts","Norm  Whittaker","Computers","MW Vol. 25 No. 3 Jun-Jul 2012","14"
    "A Simple Steady Rest","Blaine  Geddes","Lathes","MW Vol. 25 No. 3 Jun-Jul 2012","16"
    "Book Review: Welding Know-How by Frank Marlow","Daron  Klooster","Hobby Community","MW Vol. 25 No. 3 Jun-Jul 2012","23"
    "A Simple Swan","Walter  Yetman","Projects","MW Vol. 25 No. 3 Jun-Jul 2012","26"
    "Making a Rotary Table Auxiliary Top","Lowell P. Braxton","Shop Accessories","MW Vol. 25 No. 3 Jun-Jul 2012","32"
    "The Gunsmith Machinist: Timing an FAL Barrel","Steve  Acker","Gunsmithing","MW Vol. 25 No. 3 Jun-Jul 2012","36"
    "The Tool Room: Material Storage Rack","James W. Hauser","Miscellaneous","MW Vol. 25 No. 3 Jun-Jul 2012","42"
    "A Carbide Insert Toolholder","Dion  Amato","Shop Accessories","MW Vol. 25 No. 4 Aug-Sep 2012","4"
    "Sand Casting: A Primer","Bill  Conway","Welding/Foundry/Forging","MW Vol. 25 No. 4 Aug-Sep 2012","10"
    "A Mill Rack to Save Your Back","Chet  McClellan","Shop Accessories","MW Vol. 25 No. 4 Aug-Sep 2012","14"
    "M1A/M14 Spring Guide Modification","Jim  Swartz","Gunsmithing","MW Vol. 25 No. 4 Aug-Sep 2012","18"
    "Making Thin Disks & Washers with a Three-jaw Chuck","Paul W Olsen","Miscellaneous","MW Vol. 25 No. 4 Aug-Sep 2012","21"
    "Speed Reducer for an Old Lathe","Jim  Venier","Lathes","MW Vol. 25 No. 4 Aug-Sep 2012","26"
    "A Simple Dial Gauge Hand Puller","Paul  Smeltzer","Miscellaneous","MW Vol. 25 No. 4 Aug-Sep 2012","30"
    "How to Save Tendons and Destory a Keyless Chuck","Charles  St. Louis","Miscellaneous","MW Vol. 25 No. 4 Aug-Sep 2012","32"
    "Book Review: The Four Jaw Chuck by Dick Boothroyd","Daron  Klooster","Hobby Community","MW Vol. 25 No. 4 Aug-Sep 2012","36"
    "The Gunsmith Machinist: Making a Spring Loaded Plunger","Steve  Acker","Gunsmithing","MW Vol. 25 No. 4 Aug-Sep 2012","37"
    "The Tool Room: Strange Lathe Dog","James W. Hauser","Lathes","MW Vol. 25 No. 4 Aug-Sep 2012","44"
    "Tips and Techniques for Machining Plastic","Jerry  Pontius","Miscellaneous","MW Vol. 25 No. 5 Oct-Nov 2012","4"
    "Epoxy-Bonded Sand Mold for an Aluminum Casting","David  Wimberley","Welding/Foundry/Forging","MW Vol. 25 No. 5 Oct-Nov 2012","15"
    "Christmas Tree Stand","Rodney W. Hanson","Projects","MW Vol. 25 No. 5 Oct-Nov 2012","27"
    "The Gunsmith Machinist: Making a Custom .308 AR Barrel - Part One","Steve  Acker","Gunsmithing","MW Vol. 25 No. 5 Oct-Nov 2012","33"
    "The Tool Room: Bevel Square","James W. Hauser","Miscellaneous","MW Vol. 25 No. 5 Oct-Nov 2012","42"
    "Reconditioning an Atlas Model 7B Shaper - Part One","Lowell P. Braxton","Shop Machinery","MW Vol. 25 No. 6 Dec 2012-Jan 2013","4"
    "Three Left Turns Equals...A Workstop","John  Dougherty","Shop Accessories","MW Vol. 25 No. 6 Dec 2012-Jan 2013","18"
    "Making a Tractor Part","John  Viggers","Miscellaneous","MW Vol. 25 No. 6 Dec 2012-Jan 2013","22"
    "Another Way","Ronald  Geppert","Miscellaneous","MW Vol. 25 No. 6 Dec 2012-Jan 2013","27"
    "Turning a File into a Chisel","Allan  Moore","Miscellaneous","MW Vol. 25 No. 6 Dec 2012-Jan 2013","29"
    "The Gunsmith Machinist: Making a Custom .308 AR Barrel - Part Two","Steve  Acker","Gunsmithing","MW Vol. 25 No. 6 Dec 2012-Jan 2013","34"
    "The Tool Room: Milling Machine Tap Guide","James W. Hauser","Mills","MW Vol. 25 No. 6 Dec 2012-Jan 2013","34"
    "Reconditioning an Atlas Model 7B Shaper","Lowell P. Braxton","Shop Machinery","MW Vol. 26 No. 1 Feb-Mar 2013","4"
    "Rock of Ages: Tips for Building a Solid, Extra-functional Welding Table","Brad  Ocock","Shop Accessories","MW Vol. 26 No. 1 Feb-Mar 2013","4"
    "An Easy-to-Make Time-Saver for Sherline Lathes","Peter  Torrione","Lathes","MW Vol. 26 No. 1 Feb-Mar 2013","23"
    "Lathe Tailstock Spindle Lock","J.A.  Long","Lathes","MW Vol. 26 No. 1 Feb-Mar 2013","26"
    "When 10/32 is not a Fraction","John W. Foster","General Machining Knowledge","MW Vol. 26 No. 1 Feb-Mar 2013","30"
    "The Gunsmith Machinist: Modifying Handheld Grinder Abrasive Bits","Steve  Acker","Gunsmithing","MW Vol. 26 No. 1 Feb-Mar 2013","36"
    "The Tool Room: Hardinge Diving Head Guard","James W. Hauser","Shop Accessories","MW Vol. 26 No. 1 Feb-Mar 2013","42"
    "Lathe Tapping Tool","Paul J. Holm","Lathes","MW Vol. 26 No. 1 Feb-Mar 2013","44"
    "Converting a Digital Caliper to a Height Gage","David J Graves","Shop Accessories","MW Vol. 26 No. 2 Apr-May 2013","4"
    "A Band Saw V-Block","Ronald  Burri","Shop Accessories","MW Vol. 26 No. 2 Apr-May 2013","11"
    "Reconditioning an Atlas Model 7B Shaper","Lowell P. Braxton","Shop Machinery","MW Vol. 26 No. 2 Apr-May 2013","12"
    "A Simple Ball Turner","George E. Overturf Jr.","Lathes","MW Vol. 26 No. 2 Apr-May 2013","27"
    "Make a Deck Washer for Your Lawn Mower","James A. Hornicek","Projects","MW Vol. 26 No. 2 Apr-May 2013","28"
    "An Easy Way to Set Tool Height","Bill  Conway","Lathes","MW Vol. 26 No. 2 Apr-May 2013","36"
    "The Gunsmith Machinist: Replacing a Ruger Mark I Ejector","Steve  Acker","Gunsmithing","MW Vol. 26 No. 2 Apr-May 2013","38"
    "The Tool Room: Stamp Holder","James W. Hauser","Projects","MW Vol. 26 No. 2 Apr-May 2013","42"
    "A Sharpening Attachment for a Bench Grinder","Ted  Hansen","Shop Accessories","MW Vol. 26 No. 3 Jun-Jul 2013","4"
    "Protecting Yourself in the Shop","Leonard  Waring","General Machining Knowledge","MW Vol. 26 No. 3 Jun-Jul 2013","18"
    "Modifications to a Dake Arbor Press","Chuck  Bommarito","Shop Machinery","MW Vol. 26 No. 3 Jun-Jul 2013","20"
    "A Hardware Store Handle","John  Dougherty","Miscellaneous","MW Vol. 26 No. 3 Jun-Jul 2013","22"
    "Machine Rebuilding: Heavy Duty Moving","John  Ehler","Miscellaneous","MW Vol. 26 No. 3 Jun-Jul 2013","26"
    "Burr Caddy","Karl H. Schultz","Shop Accessories","MW Vol. 26 No. 3 Jun-Jul 2013","36"
    "The Gunsmith Machinist: A Bolt Handle Fixture","Steve  Acker","Gunsmithing","MW Vol. 26 No. 3 Jun-Jul 2013","38"
    "The Tool Room: Angle Plate Clamp","James W. Hauser","Shop Accessories","MW Vol. 26 No. 3 Jun-Jul 2013","42"
    "A Temporary Fourth Axis on the Mill","Ed  Hollingsworth","Mills","MW Vol. 26 No. 4 Aug-Sep 2013","4"
    "Making Stubby Nut Drivers","Carl  Blum","Projects","MW Vol. 26 No. 4 Aug-Sep 2013","10"
    "Old Iron","Spencer  Schonher","Shop Accessories","MW Vol. 26 No. 4 Aug-Sep 2013","14"
    "Machine Rebuilding: Cleaning, Disassembly, Inspection, and Repair - Part One","John  Ehler","Miscellaneous","MW Vol. 26 No. 4 Aug-Sep 2013","16"
    "Trash to Treasure","Tom  Holderer","Shop Accessories","MW Vol. 26 No. 4 Aug-Sep 2013","22"
    "Threading Alerter","Andrew  Barrowman","Lathes","MW Vol. 26 No. 4 Aug-Sep 2013","26"
    "Compound Rest and Cross Slide Clamps for the Mini-Lathe","Tom  McAllister","Lathes","MW Vol. 26 No. 4 Aug-Sep 2013","28"
    "Book Review: Forging Damascus Steel Knives for Beginners","George  Bulliss","Hobby Community","MW Vol. 26 No. 4 Aug-Sep 2013","32"
    "The Gunsmith Machinist: Making a Custom Cast Bullet Expander Plug for the 9mm","Steve  Acker","Gunsmithing","MW Vol. 26 No. 4 Aug-Sep 2013","33"
    "The Tool Room: Machinist's Jacks","James W. Hauser","Shop Accessories","MW Vol. 26 No. 4 Aug-Sep 2013","40"
    "Nifty Belt Grinder - Part One","Peter  Merriam","Shop Machinery","MW Vol. 26 No. 5 Oct-Nov 2013","4"
    "Scrap Yard Buddy","Mike  Fendley","Shop Accessories","MW Vol. 26 No. 5 Oct-Nov 2013","14"
    "Machine Rebuilding: Cleaning, Disassembly, Inspection, and Repair - Part Two","John  Ehler","Miscellaneous","MW Vol. 26 No. 5 Oct-Nov 2013","18"
    "The Tool Room: Broaching and Broach Sleeves","James W. Hauser","Shop Accessories","MW Vol. 26 No. 5 Oct-Nov 2013","26"
    "Turning a Six-Start Thread on an Engine Lathe","Chuck  Lathe","Lathes","MW Vol. 26 No. 5 Oct-Nov 2013","31"
    "The Gunsmith Machinist: Using the LaBounty Bolt Fixture","Steve  Acker","Gunsmithing","MW Vol. 26 No. 5 Oct-Nov 2013","39"
    "Shop Adventures with a "Basket Case" Stevens Favorite Rifle - Part One","Lowell P. Braxton","Gunsmithing","MW Vol. 26 No. 5 Oct-Nov 2013","44"
    "An M1-A/M-14 Scope Mount","Eugene  Pizzoli","Gunsmithing","MW Vol. 26 No. 5 Oct-Nov 2013","48"
    "A Bore Reflector","Ronald  Geppert","Gunsmithing","MW Vol. 26 No. 5 Oct-Nov 2013","51"
    "Centering the Cheap Way","Lewis  Hein","Lathes","MW Vol. 26 No. 5 Oct-Nov 2013","53"
    "The Trammel Compass the Every Shop Has: Plus, a Welder's Height Gauge","Charles St. Louis","Shop Accessories","MW Vol. 26 No. 6 Dec 2013-Jan 2014","4"
    "Milling Cylindrical Grooves: A Cautionary Tale","Dr. Kurt  Hillig","General Machining Knowledge","MW Vol. 26 No. 6 Dec 2013-Jan 2014","12"
    "Full Monty of a Grizzly Lathe","Steve  Roberts","Miscellaneous","MW Vol. 26 No. 6 Dec 2013-Jan 2014","14"
    "Modifications to a Harbor Freight Lathe/Mill: Pre-school Stuff","Andrew  Brislen","Lathes","MW Vol. 26 No. 6 Dec 2013-Jan 2014","18"
    "Nifty Belt Grinder - Part Two","Peter  Merriam","Shop Machinery","MW Vol. 26 No. 6 Dec 2013-Jan 2014","22"
    "Put Friction to Work for You","Roger  Taylor","General Machining Knowledge","MW Vol. 26 No. 6 Dec 2013-Jan 2014","30"
    "Budget Parting Blades","Bob  Daley","Lathes","MW Vol. 26 No. 6 Dec 2013-Jan 2014","32"
    "Book Review: Steel Helix","George  Bulliss","Hobby Community","MW Vol. 26 No. 6 Dec 2013-Jan 2014","33"
    "The Tool Room: A Hammer Holder","James W. Hauser","Miscellaneous","MW Vol. 26 No. 6 Dec 2013-Jan 2014","34"
    "The Gunsmith Machinist: A Custom Flip Sight Aperture for an AR15","Steve  Acker","Gunsmithing","MW Vol. 26 No. 6 Dec 2013-Jan 2014","37"
    "Shop Adventures with a "Basket Case" Stevens Favorite Rifl - Part Two","Lowell P. Braxton","Gunsmithing","MW Vol. 26 No. 6 Dec 2013-Jan 2014","44"
    "Action Solution","Fred  Prestridge","Gunsmithing","MW Vol. 26 No. 6 Dec 2013-Jan 2014","48"
    "An Unusual Four-Jaw Chuck for the Clockmaker","William  Vander-Reyden","Lathes","MW Vol. 27 No. 1 Feb-Mar 2014","4"
    "A Studebaker Hydraulic Vise","Brad  Ocock","Shop Accessories","MW Vol. 27 No. 1 Feb-Mar 2014","14"
    "Cold Casting with RTV","Bernard  Cooper","Miscellaneous","MW Vol. 27 No. 1 Feb-Mar 2014","17"
    "Give Your Vise Swivel Jaws and Pads","Jerry L. Sokol","Shop Accessories","MW Vol. 27 No. 1 Feb-Mar 2014","18"
    "Improve the Lead Screw Reverse Latch on Your Mini-lathe","James A. Hornicek","Lathes","MW Vol. 27 No. 1 Feb-Mar 2014","20"
    "Book Review: The Art of Welding","George  Bulliss","Hobby Community","MW Vol. 27 No. 1 Feb-Mar 2014","22"
    "Machine Rebuilding: Bearing Surface Renewal - Part Three","John  Ehler","Miscellaneous","MW Vol. 27 No. 1 Feb-Mar 2014","26"
    "The Tool Room: Small Universal Faceplate","James W. Hauser","Shop Accessories","MW Vol. 27 No. 1 Feb-Mar 2014","34"
    "An Accuracy Experiment","Fred  Prestridge","Gunsmithing","MW Vol. 27 No. 1 Feb-Mar 2014","36"
    "A Vertical Shear Bit for the Lathe","Steve  Acker","Gunsmithing","MW Vol. 27 No. 1 Feb-Mar 2014","41"
    "Machine Rebuilding: Bearing Surface Renewal - Part Four","John  Ehler","Miscellaneous","MW Vol. 27 No. 2 Apr-May 2014","4"
    "Abrasive Control","Jim  Venier","Miscellaneous","MW Vol. 27 No. 2 Apr-May 2014","14"
    "Boost Your Lathe's Efficiency","Tom  McAllister","Lathes","MW Vol. 27 No. 2 Apr-May 2014","16"
    "A "Shift" in Thought","Paul  Anderson","Miscellaneous","MW Vol. 27 No. 2 Apr-May 2014","22"
    "Bringing My Hydraulic Press Back to Life","Al  Hanson","Shop Machinery","MW Vol. 27 No. 2 Apr-May 2014","26"
    "Belt and Pulley Primer","RJ  Marshall","Miscellaneous","MW Vol. 27 No. 2 Apr-May 2014","32"
    "The Gunsmith Machinist: Milling Scope Rings","Steve  Acker","Gunsmithing","MW Vol. 27 No. 2 Apr-May 2014","37"
    "The Tool Room: Boring Bar Holders","James W. Hauser","Shop Accessories","MW Vol. 27 No. 2 Apr-May 2014","43"
    "A Spotting Scope Mount - Part One","Fred  Prestridge","Gunsmithing","MW Vol. 27 No. 3 Jun-Jul 2014","4"
    "Working in a Parallel Universe","John  Dougherty","Shop Accessories","MW Vol. 27 No. 3 Jun-Jul 2014","12"
    "What, Another Ball Turning Device?","Jerry L. Sokol","Shop Accessories","MW Vol. 27 No. 3 Jun-Jul 2014","14"
    "Notes on a Home Aluminum Foundry","William  Alles","Welding/Foundry/Forging","MW Vol. 27 No. 3 Jun-Jul 2014","16"
    "Cutting a Radius","Ron  Fennell","General Machining Knowledge","MW Vol. 27 No. 3 Jun-Jul 2014","27"
    "Changing the Chuck Jaws - the Easy Way","James  Long","Lathes","MW Vol. 27 No. 3 Jun-Jul 2014","31"
    "Salvage that Reel","Paul J. Holm","Shop Accessories","MW Vol. 27 No. 3 Jun-Jul 2014","32"
    "The First Years with My Jet Lathe","Robert  Huffaker","Miscellaneous","MW Vol. 27 No. 3 Jun-Jul 2014","34"
    "The Gunsmith Machinist: Quickly Dialing-in a Four-Jaw Chuck","Steve  Acker","Gunsmithing","MW Vol. 27 No. 3 Jun-Jul 2014","36"
    "The Tool Room: Why a Shop?","James W. Hauser","Miscellaneous","MW Vol. 27 No. 3 Jun-Jul 2014","42"
    "A Square Cat","Chris  Howie","Miscellaneous","MW Vol. 27 No. 4 Aug-Sep 2014","4"
    "Making a Box from Extrusions","R.G.  Sparber","Projects","MW Vol. 27 No. 4 Aug-Sep 2014","10"
    "Forging Ahead","David  McCormick","Welding/Foundry/Forging","MW Vol. 27 No. 4 Aug-Sep 2014","17"
    "A Simple Sheet Metal Brake","Ronald  Geppert","Shop Accessories","MW Vol. 27 No. 4 Aug-Sep 2014","21"
    "A Spotting Scope Mount - Part Two","Fred  Prestridge","Gunsmithing","MW Vol. 27 No. 4 Aug-Sep 2014","26"
    "New Saddle Clamps for a Mini-Lathe","Carl  Byrns","Lathes","MW Vol. 27 No. 4 Aug-Sep 2014","32"
    "The Gunsmith Machinist: Brownells Career Fair","Steve  Acker","Gunsmithing","MW Vol. 27 No. 4 Aug-Sep 2014","35"
    "The Tool Room: Acetylene Torch Guide","James W. Hauser","Shop Accessories","MW Vol. 27 No. 4 Aug-Sep 2014","43"
    "Cross Feed Nuts for an Atlas Lathe","Alan  McFarlane","Lathes","MW Vol. 27 No. 4 Aug-Sep 2014","47"
    "A Hardware Store Steam Engine","David O'Neil","Engines","MW Vol. 27 No. 5 Oct-Nov 2014","0"
    "Build a Band Saw - Part One","James McKnight","Shop Machinery","MW Vol. 27 No. 5 Oct-Nov 2014","0"
    "Creating a U-Bender","Karl Schulz","Shop Accessories","MW Vol. 27 No. 5 Oct-Nov 2014","0"
    "Plastic Fantastic!","Cheyne Greek","Miscellaneous","MW Vol. 27 No. 5 Oct-Nov 2014","0"
    "Slap Happy - Make a Slap Hammer from Scrap","Brad Ocock","Shop Accessories","MW Vol. 27 No. 5 Oct-Nov 2014","0"
    "The Gunsmith Machinist: Correcting .308 AR Primer Cratering","Steve Acker","Gunsmithing","MW Vol. 27 No. 5 Oct-Nov 2014","0"
    "The Tool Room: Double Wide Angle Plate Clamp","James W. Hauser","Shop Accessories","MW Vol. 27 No. 5 Oct-Nov 2014","0"
    "A Lathe Toolholder","H. Candland","Lathes","MW Vol. 27 No. 6 Dec 2014-Jan 2015","0"
    "A Practical Repair: Removing a Broken Exhaust Manifold Stud","Lowell Braxton","Engines","MW Vol. 27 No. 6 Dec 2014-Jan 2015","0"
    "A Workshop in a Box","Ted Hansen","Shop Accessories","MW Vol. 27 No. 6 Dec 2014-Jan 2015","0"
    "Build a Band Saw - Part Two","James McKnight","Shop Machinery","MW Vol. 27 No. 6 Dec 2014-Jan 2015","0"
    "Cataloging and Storing Slitting Saws","Ken Roth","Miscellaneous","MW Vol. 27 No. 6 Dec 2014-Jan 2015","0"
    "Modified Motor Shaft Arbors for the Shopsmith","Peter Merriam","Shop Accessories","MW Vol. 27 No. 6 Dec 2014-Jan 2015","0"
    "The Gunsmith Machinist: Correcting a 1911 Disconnector Hole","Steve Acker","Gunsmithing","MW Vol. 27 No. 6 Dec 2014-Jan 2015","0"
    "The Mini Bench Shear","Ronald Ballantine","Shop Accessories","MW Vol. 27 No. 6 Dec 2014-Jan 2015","0"
    "The Tool Room: Male Thread Gauge","James W. Hauser","Shop Accessories","MW Vol. 27 No. 6 Dec 2014-Jan 2015","0"
    "Turning a Replacement Punch","Allan Moore","General Machining Knowledge","MW Vol. 27 No. 6 Dec 2014-Jan 2015","0"
    "An ER-40 Collet Chuck for a South Bend 9\"" Lathe","Dave Garrett","Lathes","MW Vol. 28 No. 1 Feb-Mar 2015","0"
    "A Tire Bead Breaker","William Alles","Miscellaneous","MW Vol. 28 No. 1 Feb-Mar 2015","0"
    "An Installation Tool for Threaded Inserts","John Dougherty","Shop Accessories","MW Vol. 28 No. 1 Feb-Mar 2015","0"
    "Sensitive Drill Press","Ken Coburn","Shop Machinery","MW Vol. 28 No. 1 Feb-Mar 2015","0"
    "Snug","John Buffum","Shop Accessories","MW Vol. 28 No. 1 Feb-Mar 2015","0"
    "The Gunsmith Machinist: A Gas Check Seater for the RCBS Sizer-Lubricator","Steve Acker","Gunsmithing","MW Vol. 28 No. 1 Feb-Mar 2015","0"
    "The Tool Room: Antenna Wrench","James W. Hauser","Miscellaneous","MW Vol. 28 No. 1 Feb-Mar 2015","0"
    "My Craftsman 6\"" Lathe Addition","Paul Holm","Lathes","MW Vol. 28 No. 2 Apr-May 2015","0"
    "A New Firing Pin for an Old Firearm","James Hornicek","Gunsmithing","MW Vol. 28 No. 2 Apr-May 2015","0"
    "A Woodworker's Marking Knife","Peter Esselburne","Miscellaneous","MW Vol. 28 No. 2 Apr-May 2015","0"
    "Lathe Milling Fixture","Jerry Sokol","Lathes","MW Vol. 28 No. 2 Apr-May 2015","0"
    "Sand Sifter","Karl Schulz","Miscellaneous","MW Vol. 28 No. 2 Apr-May 2015","0"
    "Scrounging 101: Cheap Steel for the Hobby Metalworker","Lane Bingham","Miscellaneous","MW Vol. 28 No. 2 Apr-May 2015","0"
    "The Gunsmith Machinist: HSS Chip Breaker for Turning Barrels","Steve Acker","Gunsmithing","MW Vol. 28 No. 2 Apr-May 2015","0"
    "The Tool Room: Small Broach Bushing Box","James W. Hauser","Shop Accessories","MW Vol. 28 No. 2 Apr-May 2015","0"
    "A Centerscribe","R.G. Sparber","Shop Accessories","MW Vol. 28 No. 3 Jun-Jul 2015","0"
    "A Practical Project","Bernard Cooper","Miscellaneous","MW Vol. 28 No. 3 Jun-Jul 2015","0"
    "A Treadmill Motor for a Drill Press","Ed Payne","Shop Machinery","MW Vol. 28 No. 3 Jun-Jul 2015","0"
    "Handy Modifications","Don Wiederhold","Lathes","MW Vol. 28 No. 3 Jun-Jul 2015","0"
    "Steady Rest for a LeBlond","D. Churchwell","Lathes","MW Vol. 28 No. 3 Jun-Jul 2015","0"
    "The Gunsmith Machinist: Correcting a 1911 Frame Feed Ramp","Steve Acker","Gunsmithing","MW Vol. 28 No. 3 Jun-Jul 2015","0"
    "The Tool Room: Captive Wrench","James W. Hauser","Shop Accessories","MW Vol. 28 No. 3 Jun-Jul 2015","0"
    "Blade Welding","Alan Anganes","Shop Machinery","MW Vol. 28 No. 4 Aug-Sep 2015","4"
    "Spring Loaded Tap Follower","Gregory Martin","Shop Accessories","MW Vol. 28 No. 4 Aug-Sep 2015","10"
    "Dovetail Fixture","James McKnight","Miscellaneous","MW Vol. 28 No. 4 Aug-Sep 2015","16"
    "Antique Lathe V-Belt Conversion and Drive","Blaine Geddes","Lathes","MW Vol. 28 No. 4 Aug-Sep 2015","20"
    "The Tool Room: Custom Clamps for a Toolmaker\'s Angle Plate","James W. Hauser","Shop Accessories","MW Vol. 28 No. 4 Aug-Sep 2015","28"
    "The Gunsmith Machinist: Fitting the Barrel Hood on a Gold Cup","Steve Acker","Gunsmithing","MW Vol. 28 No. 4 Aug-Sep 2015","35"
    "Hydraulic Feed Control","Richard Vanden Berg","Shop Machinery","MW Vol. 28 No. 5 Oct-Nov 2015","4"
    "Soft Jaws for the Lathe Chuck","David J. Graves","Lathe","MW Vol. 28 No. 5 Oct-Nov 2015","12"
    "Rockin\' the Rockers","Ed Hollingsworth","Projects","MW Vol. 28 No. 5 Oct-Nov 2015","20"
    "Fitting a Nut at a Distance","Martin Gearing","Lathe","MW Vol. 28 No. 5 Oct-Nov 2015","27"
    "Reloading the Coffee Cup","Ron Geppert","Miscellaneous","MW Vol. 28 No. 5 Oct-Nov 2015","28"
    "Sanding Belt Adapter","Peter Merriam","Shop Accessories","MW Vol. 28 No. 5 Oct-Nov 2015","30"
    "The Tool Room: Arbor Press Accessory Plate","James W. Hauser","Shop Accessories","MW Vol. 28 No. 5 Oct-Nov 2015","33"
    "The Gunsmith Machinist: Tuning the .45 Colt Redhawk for Heavy Cast Bullets","Steve Acker","Gunsmithing","MW Vol. 28 No. 5 Oct-Nov 2015","35"
    "The Cheap NiCad Rebuild","E. Paul Alciatore III","Miscellaneous","MW Vol. 28 No. 6 Dec 2015-Jan 2016","4"
    "Slotting on the Lathe","Saul Gabriel Ceballos Gomez","Lathes","MW Vol. 28 No. 6 Dec 2015-Jan 2016","11"
    "Adjustable Worktable for an overfilled Shop","Jerry L. Sokol","Shop Accessories","MW Vol. 28 No. 6 Dec 2015-Jan 2016","16"
    "Indicator Holder/Stop","Don Wiederhold","Shop Accessories","MW Vol. 28 No. 6 Dec 2015-Jan 2016","18"
    "The Tool Room: V-Block Project","James W. Hauser","Shop Accessories","MW Vol. 28 No. 6 Dec 2015-Jan 2016","26"
    "Neck Reaming","Fred Prestridge","Gunsmithing","MW Vol. 28 No. 6 Dec 2015-Jan 2016","28"
    "The Gunsmith Machinist: Making an AR15 Barrel Weight","Steve Acker","Gunsmithing","MW Vol. 28 No. 6 Dec 2015-Jan 2016","36"
    "Antique Toy Steam Engine","James W. Hauser","Miscellaneous","MW Vol. 29 No. 1 Feb-Mar 2016","4"
    "Over the Top Ball Turner","Lykle Schepers","Lathes","MW Vol. 29 No. 1 Feb-Mar 2016","8"
    "A Cargo Rack for the New Truck","Lowell Braxton","Miscellaneous","MW Vol. 29 No. 1 Feb-Mar 2016","14"
    "Don\'t Replace - Repair!","Paul Anderson","Miscellaneous","MW Vol. 29 No. 1 Feb-Mar 2016","20"
    "A Shop Made Collet","Ken Hemmelgarn","Mills","MW Vol. 29 No. 1 Feb-Mar 2016","22"
    "A Tool Holding Plate for the Lathe","Gary Paine","Lathes","MW Vol. 29 No. 1 Feb-Mar 2016","26"
    "Lyman T-mag Modifications","Al Hanson","Gunsmithing","MW Vol. 29 No. 1 Feb-Mar 2016","32"
    "The Gunsmith Machinist: Making a Revolver Forcing Cone Lap","Steve Acker","Gunsmithing","MW Vol. 29 No. 1 Feb-Mar 2016","37"
    "The Tool Room: Center Drill Storage Box","James W. Hauser","Shop Accessories","MW Vol. 29 No. 1 Feb-Mar 2016","42"
    "The Easy Stirling Engine","David O\'Neil","Engines","MW Vol. 29 No. 2 Apr-May 2016","4"
    "Pipe Fittings Drill Press","Mike Fendley","Shop Machinery","MW Vol. 29 No. 2 Apr-May 2016","8"
    "A PVC Dust Collection System","Paul Holm","Shop Accessories","MW Vol. 29 No. 2 Apr-May 2016","12"
    "Mini-Lathe Modifications","George Overturf","Lathes","MW Vol. 29 No. 2 Apr-May 2016","20"
    "Series Test Light","William Alles","Miscellaneous","MW Vol. 29 No. 2 Apr-May 2016","26"
    "Addendum to ""Hydraulic Feed Control""","Richard Vanden Berg","Shop Machinery","MW Vol. 29 No. 2 Apr-May 2016","28"
    "The Gunsmith Machinist: AR-15 to AR-180 Magazine Conversion","Steve Acker","Gunsmithing","MW Vol. 29 No. 2 Apr-May 2016","32"
    "The Tool Room: South Bend Drill Press Accessories","James W. Hauser","Shop Accessories","MW Vol. 29 No. 2 Apr-May 2016","40"
    "A Plasma Cutter for the Home Shop","James Hornicek","Shop Accessories","MW Vol. 29 No. 3 Jun-Jul 2016","4"
    "Lawn Mower Blade Sharpening Fixture","Jerry L. Sokol","Welding/Foundry/Forging","MW Vol. 29 No. 3 Jun-Jul 2016","18"
    "Half Step","Myles Milner","Miscellaneous","MW Vol. 29 No. 3 Jun-Jul 2016","26"
    "The Budget Tungsten Sharpener","Roger Taylor","Shop Accessories","MW Vol. 29 No. 3 Jun-Jul 2016","28"
    "Low Profile V-Block Clamp","John Dougherty","Shop Accessories","MW Vol. 29 No. 3 Jun-Jul 2016","31"
    "Making a Sight Base for a Remington Rolling Block","Lowell Braxton","Gunsmithing","MW Vol. 29 No. 3 Jun-Jul 2016","32"
    "The Tool Room: Bridgeport Edge Finder Holder","James W. Hauser","Mills","MW Vol. 29 No. 3 Jun-Jul 2016","42"
    "The Gunsmith Machinist: The AR-15 Receiver Facer Tool","Steve Acker","Gunsmithing","MW Vol. 29 No. 3 Jun-Jul 2016","37"
    "The Buffer - A Handy Addition","Paul Holm","Shop Machinery","MW Vol. 29 No. 4 Aug-Sep 2016","4"
    "Sounding Cannon","Thomas I. Stuart","Projects","MW Vol. 29 No. 4 Aug-Sep 2016","10"
    "TIG Welding","Jon Working","Welding/Foundry/Forging","MW Vol. 29 No. 4 Aug-Sep 2016","18"
    "Parting Tool","Ron Graham","Lathes","MW Vol. 29 No. 4 Aug-Sep 2016","21"
    "A Visit to the Past","Harold Scuterud","Mills","MW Vol. 29 No. 4 Aug-Sep 2016","22"
    "Shop Made Spanner Wrench","John Dougherty","Miscellaneous","MW Vol. 29 No. 4 Aug-Sep 2016","26"
    "Arbor Press Socket","Peter Merriam","Shop Machinery","MW Vol. 29 No. 4 Aug-Sep 2016","32"
    "Wildcat Rifle Chamber without a Wildcat Reamer","Jim Venier","Gunsmithing","MW Vol. 29 No. 4 Aug-Sep 2016","33"
    "The Gunsmith Machinist: Aligning the Lathe Tailstock","Steve Acker","Lathes","MW Vol. 29 No. 4 Aug-Sep 2016","36"
    "The Tool Room: Thread Cleaner","James W. Hauser","Miscellaneous","MW Vol. 29 No. 4 Aug-Sep 2016","43"
    "Getting the Most out of your Lantern Tool Post","Gary P. Paine","Lathes","MW Vol. 29 No. 5 Oct-Nov 2016","4"
    "Steady Rest","William Alles","Lathes","MW Vol. 29 No. 5 Oct-Nov 2016","10"
    "Two-Part Vise for a Small Mill","Richard Rex","Mills","MW Vol. 29 No. 5 Oct-Nov 2016","18"
    "Shear Delight","Don Wiederhold","Shop Machinery","MW Vol. 29 No. 5 Oct-Nov 2016","26"
    "A Belt Drive Conversion for the Mini-mill","Ed Jerome","Mills","MW Vol. 29 No. 5 Oct-Nov 2016","28"
    "A Cartridge Aligner","Fred Prestridge","Gunsmithing","MW Vol. 29 No. 5 Oct-Nov 2016","32"
    "Redneck Snap Gauge","Warren Radcliff","Miscellaneous","MW Vol. 29 No. 5 Oct-Nov 2016","39"
    "Plasma Tap Extraction","Roger Taylor","Miscellaneous","MW Vol. 29 No. 5 Oct-Nov 2016","40"
    "The Tool Room: The Job that Almost Happened","James W. Hauser","Miscellaneous","MW Vol. 29 No. 5 Oct-Nov 2016","42"
    "My Version of a Cam Lock Tailstock - The Fastest Tailstock in the Midwest","Dan Thomson","Lathes","MW Vol. 29 No. 6 Dec 2016-Jan 2017","4"
    "Resucue and Rebuild a Drill Press","Myles Milner","Shop Machinery","MW Vol. 29 No. 6 Dec 2016-Jan 2017","10"
    "Dial Indicator Holder - Another Angle","Herb Yohe","Shop Accessories","MW Vol. 29 No. 6 Dec 2016-Jan 2017","19"
    "The Vernier Scale","Richard Rex","General Machining Knowledge","MW Vol. 29 No. 6 Dec 2016-Jan 2017","22"
    "Camera Trigger","John Buffum","Projects","MW Vol. 29 No. 6 Dec 2016-Jan 2017","26"
    "Upgrading a Ruger No. 3 Rifle - Part One","Lowell Braxton","Gunsmithing","MW Vol. 29 No. 6 Dec 2016-Jan 2017","29"
    "A Ring Roller","John Viggers","Miscellaneous","MW Vol. 29 No. 6 Dec 2016-Jan 2017","36"
    "Milling a Hex or Square Head Bolt","Arthur A. Lacy","General Machining Knowledge","MW Vol. 29 No. 6 Dec 2016-Jan 2017","38"
    "The Tool Room: Boring Bar Sharpening Fixture","James W. Hauser","Grinders","MW Vol. 29 No. 6 Dec 2016-Jan 2017","42"
    "Cam Lock Nuts: Mounting an A2 Chuck on a D1 Spindle","David Bowling","Lathes","MW Vol. 30 No. 1 Feb-Mar 2017","4"
    "Another Slow Speed Band Saw Attachment","Roger Taylor","Shop Machinery","MW Vol. 30 No. 1 Feb-Mar 2017","8"
    "Machine Guards","William Alles","Shop Machinery","MW Vol. 30 No. 1 Feb-Mar 2017","14"
    "A Tip: Measuring O-Rings","E. Paul III Alciatore","General Machining Knowledge","MW Vol. 30 No. 1 Feb-Mar 2017","22"
    "Small Work on Big Lathes","Jim Hansen","Lathes","MW Vol. 30 No. 1 Feb-Mar 2017","26"
    "Thread Cutting Calculations and Techniques","Arthur A. Lacy","General Machining Knowledge","MW Vol. 30 No. 1 Feb-Mar 2017","28"
    "Using the Screw Saver Bench Block","Jim Janecek","Gunsmithing","MW Vol. 30 No. 1 Feb-Mar 2017","32"
    "Upgrading a Ruger No. 3 Rifle - Part Two","Lowell Braxton","Gunsmithing","MW Vol. 30 No. 1 Feb-Mar 2017","36"
    "A Valve Spring Compressor for a Small OHV Engine","Don Wiederhold","Engines","MW Vol. 30 No. 1 Feb-Mar 2017","41"
    "The Tool Room: Extension Cord Connection Cover","James W. Hauser","Miscellaneous","MW Vol. 30 No. 1 Feb-Mar 2017","42"
    "My Shop Made Rotary Table","William Alles","Shop Accessories","MW Vol. 30 No. 2 Apr-May 2017","4"
    "Welding Urethane Belts","Ted Hansen","Miscellaneous","MW Vol. 30 No. 2 Apr-May 2017","12"
    "Modifications for the Schumacher Flux Wire Welder","James Hornicek","Welding/Foundry/Forging","MW Vol. 30 No. 2 Apr-May 2017","14"
    "Fitting a Bridgeport Right Angle Adapter to a Millrite","Herb Yohe","Shop Machinery","MW Vol. 30 No. 2 Apr-May 2017","22"
    "Square Tubing Steady Rest","Don Wiederhold","Shop Accessories","MW Vol. 30 No. 2 Apr-May 2017","26"
    "An Experimental Rifle - Part One","Fred Prestridge","Gunsmithing","MW Vol. 30 No. 2 Apr-May 2017","26"
    "Pneumatic Can Crusher","Ron Geppert","Miscellaneous","MW Vol. 30 No. 2 Apr-May 2017","42"
    "The Tool Room: Compact Three-way Tap Wrench","James W. Hauser","Miscellaneous","MW Vol. 30 No. 2 Apr-May 2017","38"
    "Table Top Band Saw - Part One","William Alles","Shop Machinery","MW Vol. 30 No. 3 Jun-Jul 2017","8"
    "Magnetic Soft Jaws","E. Paul III Alciatore","Shop Accessories","MW Vol. 30 No. 3 Jun-Jul 2017","4"
    "Removable Downfeed Arm for an RF-30 Mill/Drill","John Herrmann","Mills","MW Vol. 30 No. 3 Jun-Jul 2017","18"
    "Repairing a Logan 9B Back Gear","Mike Fendley","Lathes","MW Vol. 30 No. 3 Jun-Jul 2017","20"
    "Nifty Belt Grinder Modifications","Peter Merriam","Shop Machinery","MW Vol. 30 No. 3 Jun-Jul 2017","26"
    "Metric Threading on the 9 x 20 Lathe","Harold Scuterud","Miscellaneous","MW Vol. 30 No. 3 Jun-Jul 2017","32"
    "An Experimental Rifle - Part Two","Fred Prestridge","Gunsmithing","MW Vol. 30 No. 3 Jun-Jul 2017","36"
    "The Tool Room: Dial Indicator Clamp","James W. Hauser","Miscellaneous","MW Vol. 30 No. 3 Jun-Jul 2017","34"
    "My Mega Plate","Tom McAllister","Shop Accessories","MW Vol. 30 No. 4 Aug-Sep 2017","4"
    "Isolation Mounts for Shop Machinery","Mike Fendley","Shop Accessories","MW Vol. 30 No. 4 Aug-Sep 2017","8"
    "Lower Speeds for the Drill Press","Gregory Whitney","Shop Machinery","MW Vol. 30 No. 4 Aug-Sep 2017","10"
    "A Simple Rotary Table Clamp Set","Greg Bucci","Shop Accessories","MW Vol. 30 No. 4 Aug-Sep 2017","14"
    "A Basic Tool Post Grinder","James McKnight","Shop Machinery","MW Vol. 30 No. 4 Aug-Sep 2017","16"
    "Diamond Toolholder Adapter","R.F. Pierce","Miscellaneous","MW Vol. 30 No. 4 Aug-Sep 2017","22"
    "Table Top Band Saw - Part Two","William Alles","Shop Machinery","MW Vol. 30 No. 4 Aug-Sep 2017","26"
    "Sliding Bolt Extension Handle","Roger Taylor","Miscellaneous","MW Vol. 30 No. 4 Aug-Sep 2017","32"
    "The Tool Room: Flip Over/Drop In T-Nut","James W. Hauser","Miscellaneous","MW Vol. 30 No. 4 Aug-Sep 2017","34"
    "An Experimental Rifle - Part Three","Fred Prestridge","Gunsmithing","MW Vol. 30 No. 4 Aug-Sep 2017","36"
    "Machining a Propeller Shaft","Peter McKelvey","Miscellaneous","MW Vol. 30 No. 5 Oct-Nov 2017","4"
    "Belt Sander Repairs","Jerry L. Sokol","Shop Machinery","MW Vol. 30 No. 5 Oct-Nov 2017","11"
    "A Bench Block and Accessories","Walter Yetman","Shop Accessories","MW Vol. 30 No. 5 Oct-Nov 2017","14"
    "Fighting Friction","Roger Taylor","General Machining Knowledge","MW Vol. 30 No. 5 Oct-Nov 2017","26"
    "Building the Handy Hacksaw","Michael Jenks","Projects","MW Vol. 30 No. 5 Oct-Nov 2017","20"
    "Rotary Tool Accessories","Charles St. Louis","Shop Accessories","MW Vol. 30 No. 5 Oct-Nov 2017","28"
    "Extending a Drill and Tap","Gale Miles","General Machining Knowledge","MW Vol. 30 No. 5 Oct-Nov 2017","32"
    "An Experimental Rifle - Part Four","Fred Prestridge","Gunsmithing","MW Vol. 30 No. 5 Oct-Nov 2017","37"
    "The Tool Room: Homemade Armstrong Boring Bar Holder","James W. Hauser","Lathes","MW Vol. 30 No. 5 Oct-Nov 2017","34"
    "Another Way to Part","Alan Goertz","Lathes","MW Vol. 30 No. 6 Dec 2017-Jan 2018","4"
    "The Wohlhaupter Universal Facing and Boring Head","John Lindo","Mills","MW Vol. 30 No. 6 Dec 2017-Jan 2018","12"
    "Taking on (Almost) More Than I Can Handle","RJ Marshall","Miscellaneous","MW Vol. 30 No. 6 Dec 2017-Jan 2018","16"
    "Chess Piece or Reducer Jack","Ron Geppert","Shop Accessories","MW Vol. 30 No. 6 Dec 2017-Jan 2018","22"
    "Rotary Table Extensions","Jim Nolen","Shop Accessories","MW Vol. 30 No. 6 Dec 2017-Jan 2018","26"
    "Top Notch Insert Toolholder","Don Wiederhold","Lathes","MW Vol. 30 No. 6 Dec 2017-Jan 2018","29"
    "How Much Chatter is Chatter?","Jim Venier","Gunsmithing","MW Vol. 30 No. 6 Dec 2017-Jan 2018","33"
    "Shop Notes of an Amateur Gunsmith: Loading Dies for a Wildcat","Lowell Braxton","Gunsmithing","MW Vol. 30 No. 6 Dec 2017-Jan 2018","38"
    "The Tool Room: Drill Press Vise Holder","James W. Hauser","Shop Machinery","MW Vol. 30 No. 6 Dec 2017-Jan 2018","36"
    "A First Class Log Splitter","Jerry L. Sokol","Projects","MW Vol. 31 No. 1 Feb-Mar 2018","4"
    "A D-Tool Countersink","Frank DiSanti","General Machining Knowledge","MW Vol. 31 No. 1 Feb-Mar 2018","10"
    "Updating the Shop","Fred Prestridge","Miscellaneous","MW Vol. 31 No. 1 Feb-Mar 2018","14"
    "No-Weld Steady Rests","Harold Scuterud","Lathes","MW Vol. 31 No. 1 Feb-Mar 2018","17"
    "A Handy Little Die Wrench","Michael Jenks","General Machining Knowledge","MW Vol. 31 No. 1 Feb-Mar 2018","18"
    "String Cutter","Don Wiederhold","Miscellaneous","MW Vol. 31 No. 1 Feb-Mar 2018","20"
    "Electrician's Torque Screw Driver","Dave Ford","Miscellaneous","MW Vol. 31 No. 1 Feb-Mar 2018","26"
    "A Front Sight for a Henry Rifle","RJ Marshall","Gunsmithing","MW Vol. 31 No. 1 Feb-Mar 2018","28"
    "Shop Notes of an Amateur Gunsmith: A Budget Scout Rifle","Lowell Braxton","Gunsmithing","MW Vol. 31 No. 1 Feb-Mar 2018","33"
    "The Tool Room: A Modified Cherry Picker","James W. Hauser","Shop Machinery","MW Vol. 31 No. 1 Feb-Mar 2018","38"
    "Adjustable Band Saw Stop","R. G. Sparber","Shop Machinery","MW Vol. 31 No. 2 Apr-May 2018","4"
    "Angle Table","Jim Nolen","Shop Accessories","MW Vol. 31 No. 2 Apr-May 2018","10"
    "Three-Jaw Live Center","Don Wiederhold","Lathes","MW Vol. 31 No. 2 Apr-May 2018","12"
    "A Laminate Trimmer as a Tool Post Grinder","John Viggers","Shop Machinery","MW Vol. 31 No. 2 Apr-May 2018","16"
    "Another Boring Bar Holder","Fred Prestridge","Lathes","MW Vol. 31 No. 2 Apr-May 2018","20"
    "A Really Short Handle Screwdriver","Jerry L. Sokol","Miscellaneous","MW Vol. 31 No. 2 Apr-May 2018","22"
    "A 13"" South Bend Toolroom Lathe Rebuild","Steve Epstein","Lathes","MW Vol. 31 No. 2 Apr-May 2018","26"
    "Relining the Barrel of a Barn Relic","Jim Venier","Gunsmithing","MW Vol. 31 No. 2 Apr-May 2018","32"
    "Shop Notes of an Amateur Gunsmith: Footsteps Along the Path: Projects Beget Projects","Lowell Braxton","Gunsmithing","MW Vol. 31 No. 2 Apr-May 2018","37"
    "The Tool Room: A New Door Knocker","James W. Hauser","Miscellaneous","MW Vol. 31 No. 2 Apr-May 2018","40"
    "Tenoning Jig","Paul J. Smeltzer","Shop Accessories","MW Vol. 31 No. 3 Jun-Jul 2018","4"
    "Sharpening Hole Saws","William Vander-Reyden","General Machining Knowledge","MW Vol. 31 No. 3 Jun-Jul 2018","12"
    "A Simple Lathe Accessory","Alan Goertz","Lathes","MW Vol. 31 No. 3 Jun-Jul 2018","16"
    "Little Ol' Knob Maker","Don Wiederhold","Lathes","MW Vol. 31 No. 3 Jun-Jul 2018","20"
    "A Powered Hacksaw Build","Saul Gabriel Ceballos Gomez","Shop Machinery","MW Vol. 31 No. 3 Jun-Jul 2018","28"
    "Build Your Own Toggle Clamp","Jerry L. Sokol","Shop Accessories","MW Vol. 31 No. 3 Jun-Jul 2018","32"
    "Dillon Press Powder Funnel (Expander Die) Modification","James Tucker","Gunsmithing","MW Vol. 31 No. 3 Jun-Jul 2018","34"
    "Shop Notes of an Amateur Gunsmith: Restoring a Bucket Rifle - Hopkins and Allen 922","Lowell Braxton","Gunsmithing","MW Vol. 31 No. 3 Jun-Jul 2018","38"
    "The Tool Room: Cedar City Treasures - A New Bridgeport Feed Handle","James W. Hauser","Mills","MW Vol. 31 No. 3 Jun-Jul 2018","42"
    "Patent Pending - Part One","Charles St. Louis","Hobby Community","MW Vol. 31 No. 4 Aug-Sep 2018","4"
    "A Quick-Change Drill Press Fence","R.G. Sparber","Shop Machinery","MW Vol. 31 No. 4 Aug-Sep 2018","13"
    "Flange Bearing Greaser","Don Wiederhold","General Machining Knowledge","MW Vol. 31 No. 4 Aug-Sep 2018","22"
    "Candy Dispenser","Kenneth Hemmelgarn","Miscellaneous","MW Vol. 31 No. 4 Aug-Sep 2018","26"
    "A Heavy Duty Workbench","Paul Holm","Shop Accessories","MW Vol. 31 No. 4 Aug-Sep 2018","28"
    "A Bullet Casting Fluxing Tool","Al Peterson","Gunsmithing","MW Vol. 31 No. 4 Aug-Sep 2018","32"
    "Shop Notes of an Amateur Gunsmith: Wildcat on the Cheap - Part One","Lowell Braxton","Gunsmithing","MW Vol. 31 No. 4 Aug-Sep 2018","36"
    "The Tool Room: A Dedicated Boring Head Wrench","James W. Hauser","Mills","MW Vol. 31 No. 4 Aug-Sep 2018","42"
    "Hydraulic Press - Part One","William Alles","Shop Machinery","MW Vol. 31 No. 5 Oct-Nov 2018","4"
    "New Life for an Old Grinder","Fred Prestridge","Shop Machinery","MW Vol. 31 No. 5 Oct-Nov 2018","10"
    "Magnetic Chuck for a Metal Lathe","Mike Fendley","Lathes","MW Vol. 31 No. 5 Oct-Nov 2018","12"
    "Patent Pending - Part Two","Charles St. Louis","Hobby Community","MW Vol. 31 No. 5 Oct-Nov 2018","18"
    "Candlestick Repair","Paul Anderson","Miscellaneous","MW Vol. 31 No. 5 Oct-Nov 2018","26"
    "Portable Spotting Scope Stand","Peter Esselburne","Gunsmithing","MW Vol. 31 No. 5 Oct-Nov 2018","30"
    "Shop Notes of an Amateur Gunsmith: Wildcat on the Cheap - Part Two","Lowell Braxton","Gunsmithing","MW Vol. 31 No. 5 Oct-Nov 2018","36"
    "The Tool Room: Hardinge Quick Action Tailstock","James W. Hauser","Lathes","MW Vol. 31 No. 5 Oct-Nov 2018","42"
    "Upgrade your Lathe with a 5C Collet Spin Index","Dennis Sandoz","Lathes","MW Vol. 31 No. 6 Dec 2018-Jan 2019","5"
    "Hydraulic Press - Part Two","William Alles","Shop Machinery","MW Vol. 31 No. 6 Dec 2018-Jan 2019","11"
    "Articulating Base for a Small Vise","Timothy J. Apps","Shop Accessories","MW Vol. 31 No. 6 Dec 2018-Jan 2019","18"
    "Easy Lantern Chuck","Peter Merriam","Shop Accessories","MW Vol. 31 No. 6 Dec 2018-Jan 2019","20"
    "A First Class Gun Vise","Jerry L. Sokol","Gunsmithing","MW Vol. 31 No. 6 Dec 2018-Jan 2019","26"
    "Shop Notes of an Amateur Gunsmith: Making Dies and Loading Dies","Lowell Braxton","Gunsmithing","MW Vol. 31 No. 6 Dec 2018-Jan 2019","34"
    "The Tool Room: Shaft Clamp","James W. Hauser","Mills","MW Vol. 31 No. 6 Dec 2018-Jan 2019","42"
    "Rod Bender","Don Wiederhold","Shop Accessories","MW Vol. 32 No. 1 Feb-Mar 2019","4"
    "The Saga of the Machine Shop Bus","Mike Fendley","Miscellaneous","MW Vol. 32 No. 1 Feb-Mar 2019","13"
    "A Shop Made Power Hacksaw","Harold Scuterud","Shop Machinery","MW Vol. 32 No. 1 Feb-Mar 2019","22"
    "Vise Squaring Tool","David Ford","Shop Accessories","MW Vol. 32 No. 1 Feb-Mar 2019","26"
    "Sine Bar Project","Noel Henderson","Projects","MW Vol. 32 No. 1 Feb-Mar 2019","28"
    "Specific Purpose Saw","James E. Simpson","Shop Machinery","MW Vol. 32 No. 1 Feb-Mar 2019","30"
    "My Coehorn Mortar Project","Bob Woods","Gunsmithing","MW Vol. 32 No. 1 Feb-Mar 2019","32"
    "Shop Notes of an Amateur Gunsmith: A Metamorphosing Peabody Martini Rifle","Lowell Braxton","Gunsmithing","MW Vol. 32 No. 1 Feb-Mar 2019","34"
    "The Tool Room: Bridgeport Switch Extension","James W. Hauser","Mills","MW Vol. 32 No. 1 Feb-Mar 2019","42"
    "Super Colossal Lantern","Chuck St. Louis","Lathes","MW Vol. 32 No. 2 Apr-May 2019","5"
    "A Vise Mounted Work Stop","Jerry L. Sokol","Shop Accessories","MW Vol. 32 No. 2 Apr-May 2019","18"
    "Muzzle Loader Ram Rod","Al Peterson","Gunsmithing","MW Vol. 32 No. 2 Apr-May 2019","26"
    "Hydraulic Press - Part Three","William Alles","Shop Machinery","MW Vol. 32 No. 2 Apr-May 2019","20"
    "Shop Notes of an Amateur Gunsmith: The Evolution of an ""H Mill""","Lowell Braxton","Mills","MW Vol. 32 No. 2 Apr-May 2019","34"
    "The Tool Room: Collet Drawbar Holder","James W. Hauser","Lathes","MW Vol. 32 No. 2 Apr-May 2019","32"
    "A Small Block and Tackle","Steve Wellcome","Shop Accessories","MW Vol. 32 No. 3 Jun-Jul 2019","4"
    "An Alternate Mini-Lathe Timing Belt","John Manhardt","Lathes","MW Vol. 32 No. 3 Jun-Jul 2019","12"
    "Hydraulic Broach","Don Wiederhold","Shop Machinery","MW Vol. 32 No. 3 Jun-Jul 2019","20"
    "A Three-ball Spherometer","Kurt, Dr. Hillig","Miscellaneous","MW Vol. 32 No. 3 Jun-Jul 2019","26"
    "Hydraulic Press - Part Four: Hole Punching Dies","William Alles","Shop Machinery","MW Vol. 32 No. 3 Jun-Jul 2019","30"
    "Tailstock Register Plate","Fred Prestridge","Lathes","MW Vol. 32 No. 3 Jun-Jul 2019","36"
    "Shop Notes of an Amateur Gunsmith: Assembling a Mauser 71-84 Rifle","Lowell Braxton","Gunsmithing","MW Vol. 32 No. 3 Jun-Jul 2019","37"
    "Shop-made Collets","Dave Strom","Gunsmithing","MW Vol. 32 No. 3 Jun-Jul 2019","40"
    "The Tool Room: H2 Hummer Shift Lock Button","James W. Hauser","Miscellaneous","MW Vol. 32 No. 3 Jun-Jul 2019","42"
    "Modifying a Blaster","Carl Byrns","Projects","MW Vol. 32 No. 4 Aug-Sep 2019","4"
    "A DIY Bore Illuminator","John M. Herrmann","Miscellaneous","MW Vol. 32 No. 4 Aug-Sep 2019","10"
    "Hydraulic Press - Part Five: Flat Stock Shear","William Alles","Shop Machinery","MW Vol. 32 No. 4 Aug-Sep 2019","30"
    "Tools, Tips, Toys & Tricks: Improving your Drill Index Stand","Chuck St. Louis","Shop Accessories","MW Vol. 32 No. 4 Aug-Sep 2019","26"
    "Demagnetizer","R. Brien","Miscellaneous","MW Vol. 32 No. 4 Aug-Sep 2019","28"
    "The Tool Room: Facing Tool","James W. Hauser","Miscellaneous","MW Vol. 32 No. 4 Aug-Sep 2019","30"
    "Shop Notes of an Amateur Gunsmith: Rebirth of a Wildcat - Part One","Lowell Braxton","Gunsmithing","MW Vol. 32 No. 4 Aug-Sep 2019","32"
    "A Wad Cutter Bullet Seating Plug","Al Peterson","Gunsmithing","MW Vol. 32 No. 4 Aug-Sep 2019","38"
    "Fitting and Stabilizing a Milling Attachment on Your Lathe","Dennis Sandoz","Lathes","MW Vol. 32 No. 5 Oct-Nov 2019","4"
    "A Shop PITA","Fred Prestridge","Shop Machinery","MW Vol. 32 No. 5 Oct-Nov 2019","8"
    "A Universal Bench Grinder Tool Rest","Jerry L. Sokol","Shop Machinery","MW Vol. 32 No. 5 Oct-Nov 2019","10"
    "Placing Punch Marks with Older Eyes","Timothy J. Apps","Miscellaneous","MW Vol. 32 No. 5 Oct-Nov 2019","15"
    "Making Threaded Rivets","R. G. Sparber","Miscellaneous","MW Vol. 32 No. 5 Oct-Nov 2019","18"
    "Tools, Tips, Toys & Tricks: Universal T-Nut Set","Chuck St. Louis","Miscellaneous","MW Vol. 32 No. 5 Oct-Nov 2019","22"
    "A Pivoting Mill Sub-table for a Dividing Head","Jerrold Tiers","Shop Accessories","MW Vol. 32 No. 5 Oct-Nov 2019","28"
    "Hydraulic Press - Part Six: Round Stock Shear","William Alles","Shop Machinery","MW Vol. 32 No. 5 Oct-Nov 2019","30"
    "The Tool Room: Threading Tool Grinding Fixture","James W. Hauser","Shop Accessories","MW Vol. 32 No. 5 Oct-Nov 2019","36"
    "Shop Notes of an Amateur Gunsmith: Rebirth of a Wildcat - Part Two","Lowell Braxton","Gunsmithing","MW Vol. 32 No. 5 Oct-Nov 2019","38"
    "Dragonfly Air Rifle - PART ONE","Leslie Proper","Gunsmithing","MW Vol. 32 No. 6 Dec 19/Jan 20","4"
    "A Spring Loaded Center","Walter Yetman","Projects","MW Vol. 32 No. 6 Dec 19/Jan 20","15"
    "5C Collet Attachment for a Heavy 10","Paul Holm","Lathes","MW Vol. 32 No. 6 Dec 19/Jan 20","30"
    "Tools, Tips, Toys & Tricks: Transfer Punch Set Revisited","Chuck St. Louis","Shop Accessories","MW Vol. 32 No. 6 Dec 19/Jan 20","18"
    "Hydraulic Press - Part Seven: The Arbor Press","William Alles","Shop Machinery","MW Vol. 32 No. 6 Dec 19/Jan 20","22"
    "Spindle Lock for a Bench-top Mill","Harvey Kratz","mills","MW Vol. 32 No. 6 Dec 19/Jan 20","28"
    "Tool Room: Tripod Project","James Hauser","Miscellaneous","MW Vol. 32 No. 6 Dec 19/Jan 20","37"
    "Shop Notes of an Amateur Gunsmith: Making a Front Sight","Lowell Braxton","Gunsmithing","MW Vol. 32 No. 6 Dec 19/Jan 20","40"
    "A Primer on Pickling","Al Peterson","Miscellaneous","MW Vol. 33 No. 1 Feb/Mar 20","4"
    "Strap Wrench","Ron Geppert","Shop Accessories","MW Vol. 33 No. 1 Feb/Mar 20","10"
    "My Shop","William Alles","Miscellaneous","MW Vol. 33 No. 1 Feb/Mar 20","12"
    "The Dragonfly Air Rifle - Part Two","Leslie Proper","Gunsmithing","MW Vol. 33 No. 1 Feb/Mar 20","18"
    "Tools, Tips, Toys & Tricks: Cross Hole Drill Bushings","Chuck St. Louis","Shop Accessories","MW Vol. 33 No. 1 Feb/Mar 20","32"
    "Tool Room: Drill Press Improvments","James Hauser","Shop Machinery","MW Vol. 33 No. 1 Feb/Mar 20","36"
    "Shop Notes of an Amateur Gunsmith: Making a Swivel Base for a Vise","Lowell Braxton","Gunsmithing","MW Vol. 33 No. 1 Feb/Mar 20","38"
    "Tips  & Tricks: Another Type of Threaded Rivet","Howie Grunert","Tips & Tricks","MW Vol. 33 No. 1 Feb/Mar 20","43"
    "Tips  & Tricks: Cutting a Radius","Aaron Kohler","Tips & Tricks","MW Vol. 33 No. 1 Feb/Mar 20","43"
    ''')
    # File:  The_Home_Shop_Machinist_Article_Index.csv Downloaded Mon 17 Feb
    # 2020 07:49:09 PM from
    # http://www.homeshopmachinist.net/resources/article-index/.  MD5 hash
    # is 0615a68f7866dd3e94238d595b1d5492.  BOM & carriage returns removed.
    vp2 = dedent('''
    "Article Title","Author Name","Article Subject","Issue","Page"
    "Drill Press Table","Robert S. Hedin","Shop Machinery","HSM Vol. 01 No. 1 Jan-Feb 1982","5"
    "A Lathe Tool Holder","John Campbell","Lathes","HSM Vol. 01 No. 1 Jan-Feb 1982","7"
    "Dovetail Slides","Gale Wollenberg","Shop Machinery","HSM Vol. 01 No. 1 Jan-Feb 1982","14"
    "Make a Work Saver From Scrap Iron","John Dean","Shop Accessories","HSM Vol. 01 No. 1 Jan-Feb 1982","17"
    "A Modified "Wedge" Oscillating Engine - Part I","Richard F. Cutler","Engines","HSM Vol. 01 No. 1 Jan-Feb 1982","18"
    "Boring, Flycutting & Spot Facing with Rotating Cutters","William T. Roubal, Ph.D.","Miscellaneous","HSM Vol. 01 No. 1 Jan-Feb 1982","24"
    "3"" Parrott Field Rifle - Part I","William F. Green","Gunsmithing","HSM Vol. 01 No. 1 Jan-Feb 1982","28"
    "A Practical Ball-Turning Tool for Atlas 12" & Similar Lathes","John G. Landwehr","Lathes","HSM Vol. 01 No. 1 Jan-Feb 1982","33"
    "Sheet Metal Applications","Warren Weston","Miscellaneous","HSM Vol. 01 No. 1 Jan-Feb 1982","38"
    "A Lathe Carriage Stop With Dial Indicator","W.C. Grosjean","Lathes","HSM Vol. 01 No. 1 Jan-Feb 1982","40"
    "From the Scrapbox: Planning a Small Shop","Frank A. McLean","Miscellaneous","HSM Vol. 01 No. 1 Jan-Feb 1982","42"
    "Centering Cap","Don McCormac","Shop Accessories","HSM Vol. 01 No. 2 Mar-Apr 1982","7"
    "How to Equally Divide A Pie!","John Dean","General Machining Knowledge","HSM Vol. 01 No. 2 Mar-Apr 1982","14"
    "No-Bounce Soft Hammers","Robert S. Hedin","Shop Accessories","HSM Vol. 01 No. 2 Mar-Apr 1982","16"
    "A Home Foundry - Part I","Harold Timm","Welding/Foundry/Forging","HSM Vol. 01 No. 2 Mar-Apr 1982","18"
    "A Modified "Wedge" Oscillating Engine - Part II","Richard F. Cutler","Engines","HSM Vol. 01 No. 2 Mar-Apr 1982","24"
    "3"" Parrott Field Rifle - Part II","William F. Green","Gunsmithing","HSM Vol. 01 No. 2 Mar-Apr 1982","29"
    "Stalking the Wily Chuck Key and Related Matters","Guy Lautard","Lathes","HSM Vol. 01 No. 2 Mar-Apr 1982","34"
    "From the Scrapbox: A Sturdy Workbench","Frank A. McLean","Shop Accessories","HSM Vol. 01 No. 2 Mar-Apr 1982","36"
    "Geometric Construction","Richard J. Loescher","General Machining Knowledge","HSM Vol. 01 No. 2 Mar-Apr 1982","38"
    "Step Collets","William T. Roubal, Ph.D.","Lathes","HSM Vol. 01 No. 2 Mar-Apr 1982","40"
    "A Little Bit of Everything","Gale Wollenberg","Miscellaneous","HSM Vol. 01 No. 2 Mar-Apr 1982","42"
    "A Toolpost Grinder for Your Machinex 5 or Unimat Lathe","Rodney Jones","Lathes","HSM Vol. 01 No. 3 May-Jun 1982","10"
    "Always Wear Protective Glasses When Operating Any Shop Equipment","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 01 No. 3 May-Jun 1982","12"
    "Scrap Iron Tapping Guide Prevents Making Screwy Threads","John Dean","Lathes","HSM Vol. 01 No. 3 May-Jun 1982","12"
    "Inexpensive Fitted Instrument Case","W.B Vaughan","Miscellaneous","HSM Vol. 01 No. 3 May-Jun 1982","14"
    "Machine Shop Calculations: Tapers - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 01 No. 3 May-Jun 1982","15"
    "Threading Copper Tubing","James B. Dietel","General Machining Knowledge","HSM Vol. 01 No. 3 May-Jun 1982","17"
    "Faceplates and Such - Part I","Robert E. LaMarche","Lathes","HSM Vol. 01 No. 3 May-Jun 1982","18"
    "A Home Foundry - Part II","Harold Timm","Welding/Foundry/Forging","HSM Vol. 01 No. 3 May-Jun 1982","23"
    "A Modified "Wedge" Oscillating Engine - Part III","Richard F. Cutler","Engines","HSM Vol. 01 No. 3 May-Jun 1982","26"
    "The Machinex 5","Richard Welling","Shop Machinery","HSM Vol. 01 No. 3 May-Jun 1982","33"
    "3"" Parrott Field Rifle - Part III","William F. Green","Gunsmithing","HSM Vol. 01 No. 3 May-Jun 1982","36"
    "From the Scrapbox: A Few Thoughts on Drill Presses and Tool Grinders","Frank A. McLean","Shop Machinery","HSM Vol. 01 No. 3 May-Jun 1982","39"
    "Welding Alternatives for the Machinist","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 01 No. 3 May-Jun 1982","46"
    "Threading Oil Cup","Don McCormac","Lathes","HSM Vol. 01 No. 3 May-Jun 1982","48"
    "How to Get Things in Line Again","John Dean","Lathes","HSM Vol. 01 No. 4 Jul-Aug 1982","11"
    "Machine Shop Calculations: Tapers - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 01 No. 4 Jul-Aug 1982","13"
    "Sheetmetal Fabrication: Edges","Richard J. Loescher","Miscellaneous","HSM Vol. 01 No. 4 Jul-Aug 1982","15"
    "FLASH - Making a Good Weld","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 01 No. 4 Jul-Aug 1982","16"
    "Always Remove or Secure Jewelry When Operating Any Shop Equipment","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 01 No. 4 Jul-Aug 1982","17"
    "Triscamp .059 - Part I","Robert A. Washburn","Engines","HSM Vol. 01 No. 4 Jul-Aug 1982","18"
    "Four-Jaw Independent Lathe Chuck","Paul K. Johnson","Lathes","HSM Vol. 01 No. 4 Jul-Aug 1982","26"
    "Faceplates and Such - Part II","Robert E. LaMarche","Lathes","HSM Vol. 01 No. 4 Jul-Aug 1982","29"
    "A Home Foundry - Part III","Harold Timm","Welding/Foundry/Forging","HSM Vol. 01 No. 4 Jul-Aug 1982","34"
    "Improving Your Lathe With A Dial Indicator","George A. Kwasniewski","Lathes","HSM Vol. 01 No. 4 Jul-Aug 1982","39"
    "Chuck Key Retainer","W.B Vaughan","Lathes","HSM Vol. 01 No. 4 Jul-Aug 1982","41"
    "Sensitive Drilling Attachment","Robert S. Hedin","Shop Machinery","HSM Vol. 01 No. 4 Jul-Aug 1982","42"
    "A Taper Attachment for Your Machinex 5 Lathe","Rodney Jones","Lathes","HSM Vol. 01 No. 4 Jul-Aug 1982","44"
    "A Drill Press Improvement","F. Burrows Esty","Shop Machinery","HSM Vol. 01 No. 4 Jul-Aug 1982","48"
    "Shop of the Month","Gordon L. Sherwood","Hobby Community","HSM Vol. 01 No. 5 Sep-Oct 1982","12"
    "Sheetmetal Fabrication: Seams","Richard J. Loescher","Miscellaneous","HSM Vol. 01 No. 5 Sep-Oct 1982","14"
    "Machine Shop Calculations: Keyed Assemblies","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 01 No. 5 Sep-Oct 1982","17"
    "Compressed Air - Part I","Lynn Everett","Shop Accessories","HSM Vol. 01 No. 5 Sep-Oct 1982","20"
    "Treat Chips Carefully","Edward G. Hoffman","Lathes","HSM Vol. 01 No. 5 Sep-Oct 1982","21"
    "Lathe Work","James Hamill","Lathes","HSM Vol. 01 No. 5 Sep-Oct 1982","22"
    "Welding Cast Iron - Part I","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 01 No. 5 Sep-Oct 1982","24"
    "Milling on a Drill Press","Rudy Kouhoupt","Shop Machinery","HSM Vol. 01 No. 5 Sep-Oct 1982","26"
    "Triscamp .059 - Part II","Robert A. Washburn","Engines","HSM Vol. 01 No. 5 Sep-Oct 1982","31"
    "A Gas Welding Tip","Robert W. Metze","General Machining Knowledge","HSM Vol. 01 No. 5 Sep-Oct 1982","35"
    "A Homemade Disk Sander","Tom Saporito","Shop Machinery","HSM Vol. 01 No. 5 Sep-Oct 1982","36"
    "Swarf Trays for the Myford Series 7 Lathes","Guy Lautard","Lathes","HSM Vol. 01 No. 5 Sep-Oct 1982","38"
    "Finishing Contoured Metal Castings","William T. Roubal, Ph.D.","Miscellaneous","HSM Vol. 01 No. 5 Sep-Oct 1982","41"
    "How to Get to the Center of Things","John Dean","General Machining Knowledge","HSM Vol. 01 No. 5 Sep-Oct 1982","46"
    "From the Scrapbox: A Fireside Chat About Lathes","Frank A. McLean","Lathes","HSM Vol. 01 No. 5 Sep-Oct 1982","48"
    "From the Files of the Primitive Machine Shop","Gale Wollenberg","Miscellaneous","HSM Vol. 01 No. 5 Sep-Oct 1982","50"
    "An Accessory Table for Your Lathe","Robert W. Metze","Lathes","HSM Vol. 01 No. 5 Sep-Oct 1982","52"
    "Drill Chuck Adapter","Grant W. Wood","Shop Accessories","HSM Vol. 01 No. 5 Sep-Oct 1982","52"
    "Compressed Air - Part 2","Lynn Everett","Shop Accessories","HSM Vol. 01 No. 6 Nov-Dec 1982","8"
    "Book Review: Build Your Own Metal Working Shop from Scrap","Dave Gingery","Hobby Community","HSM Vol. 01 No. 6 Nov-Dec 1982","12"
    "Build Your Own Metalworking Shop From Scrap - Ammen","Edward G. Hoffman","Hobby Community","HSM Vol. 01 No. 6 Nov-Dec 1982","12"
    "Book Review: Jig and Fixture Design","Edward G. Hoffman","Hobby Community","HSM Vol. 01 No. 6 Nov-Dec 1982","13"
    "Jig and Fixture Design - Hoffman","Raymond D. Niergarth","Hobby Community","HSM Vol. 01 No. 6 Nov-Dec 1982","13"
    "The Sherline #5000 Vertical Milling Machine","Edward G. Hoffman","Mills","HSM Vol. 01 No. 6 Nov-Dec 1982","16"
    "Sheetmetal Fabrication: Notches","Richard J. Loescher","Miscellaneous","HSM Vol. 01 No. 6 Nov-Dec 1982","19"
    "Machine Shop Calculations: Geometric Forms","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 01 No. 6 Nov-Dec 1982","20"
    "Welding Cast Iron - Part II","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 01 No. 6 Nov-Dec 1982","22"
    "Grinding Wheels","Edward G. Hoffman","Shop Machinery","HSM Vol. 01 No. 6 Nov-Dec 1982","25"
    "Boring Head","W.C. Grosjean","Mills","HSM Vol. 01 No. 6 Nov-Dec 1982","26"
    "A Versatile, Quick Change Bench Grinder Solves Many Problems","Glenn L. Wilson","Shop Machinery","HSM Vol. 01 No. 6 Nov-Dec 1982","33"
    "A Versatile, Quick Change Bench Grinder Solves Many Problems","John Dean","Shop Machinery","HSM Vol. 01 No. 6 Nov-Dec 1982","33"
    "Fifteen Minute Expanding Mandrel","Grant W. Wood","Lathes","HSM Vol. 01 No. 6 Nov-Dec 1982","37"
    "Metal Turning and Glassblowing with the Metal Lathe","William T. Roubal, Ph.D.","Lathes","HSM Vol. 01 No. 6 Nov-Dec 1982","38"
    "Triscamp .059 - Part III","Robert A. Washburn","Engines","HSM Vol. 01 No. 6 Nov-Dec 1982","43"
    "From the Scrapbox: Lathe Stands","Frank A. McLean","Shop Accessories","HSM Vol. 01 No. 6 Nov-Dec 1982","48"
    "Tool-Less Hold-down Bolt","W.B Vaughan","Shop Accessories","HSM Vol. 01 No. 6 Nov-Dec 1982","52"
    "Emco Compact 5","Edward G. Hoffman","Miscellaneous","HSM Vol. 02 No. 1 Jan-Feb 1983","9"
    "Q & A","Frank A. McLean","General Machining Knowledge","HSM Vol. 02 No. 1 Jan-Feb 1983","13"
    "Sheetmetal Fabrication: Sheetmetal Layout - Part I","Richard J. Loescher","Miscellaneous","HSM Vol. 02 No. 1 Jan-Feb 1983","14"
    "Machine Shop Calculations: Geometric Forms","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 02 No. 1 Jan-Feb 1983","18"
    "Practical Problems in Mathematics for Machinists - Hoffman","Raymond D. Niergarth","Hobby Community","HSM Vol. 02 No. 1 Jan-Feb 1983","21"
    "Electrode Selection","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 02 No. 1 Jan-Feb 1983","22"
    "Compressed Air Safety","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 02 No. 1 Jan-Feb 1983","24"
    "Lathe Milling Attachment","Robert S. Hedin","Lathes","HSM Vol. 02 No. 1 Jan-Feb 1983","26"
    "A Drafting Table You Can Build for Less than $20","Edward G. Hoffman","Shop Accessories","HSM Vol. 02 No. 1 Jan-Feb 1983","32"
    "Two Machine Tool Stands","Guy Lautard","Shop Accessories","HSM Vol. 02 No. 1 Jan-Feb 1983","35"
    "Modifications to the Machinex 5 Lathe","Richard Welling","Lathes","HSM Vol. 02 No. 1 Jan-Feb 1983","38"
    "Triscamp .059 - Part IV","Robert A. Washburn","Engines","HSM Vol. 02 No. 1 Jan-Feb 1983","41"
    "Rocker Retainer","Grant W. Wood","Lathes","HSM Vol. 02 No. 1 Jan-Feb 1983","43"
    "Metal Turning and Glassblowing with the Metal Lathe - Part I","William T. Roubal, Ph.D.","Projects","HSM Vol. 02 No. 1 Jan-Feb 1983","44"
    "From the Scrapbox: A Fireside Chat About Lathe Tools","Frank A. McLean","Lathes","HSM Vol. 02 No. 1 Jan-Feb 1983","46"
    "Build a Precise Tapper","Jay Bolante","Miscellaneous","HSM Vol. 02 No. 1 Jan-Feb 1983","51"
    "Deburring Scraper","Don McCormac","Shop Accessories","HSM Vol. 02 No. 1 Jan-Feb 1983","52"
    "Lathe Carriage Stop","Don McCormac","Lathes","HSM Vol. 02 No. 1 Jan-Feb 1983","52"
    "Rockwell Sander/Grinder","Edward G. Hoffman","Miscellaneous","HSM Vol. 02 No. 2 Mar-Apr 1983","8"
    "Rank Scherr-Tumico Micrometer Set","Edward G. Hoffman","Miscellaneous","HSM Vol. 02 No. 2 Mar-Apr 1983","9"
    "Q & A","William T. Roubal, Ph.D.","General Machining Knowledge","HSM Vol. 02 No. 2 Mar-Apr 1983","10"
    "Q & A","Lynn Everett","General Machining Knowledge","HSM Vol. 02 No. 2 Mar-Apr 1983","11"
    "Machine Shop Calculations: Spacing Holes - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 02 No. 2 Mar-Apr 1983","14"
    "Sheetmetal Fabrication: Sheetmetal Layout - Part II","Richard J. Loescher","Miscellaneous","HSM Vol. 02 No. 2 Mar-Apr 1983","18"
    "Brazing: The Misunderstood Joining Process","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 02 No. 2 Mar-Apr 1983","24"
    "Bench Grinder Safety - Part I","Edward G. Hoffman","Shop Machinery","HSM Vol. 02 No. 2 Mar-Apr 1983","27"
    "Milling Attachment for the Lathe","W. Pete Peterka","Lathes","HSM Vol. 02 No. 2 Mar-Apr 1983","28"
    "Metal Turning and Glassblowing with the Metal Lathe - Part II","William T. Roubal, Ph.D.","Projects","HSM Vol. 02 No. 2 Mar-Apr 1983","34"
    "Sharpening Milling Cutters","William A. Johnson","Shop Machinery","HSM Vol. 02 No. 2 Mar-Apr 1983","36"
    "A V-Block Drill Guide","Robert W. Metze","Shop Accessories","HSM Vol. 02 No. 2 Mar-Apr 1983","38"
    "A 20-Ton Hydraulic Press You Can Build - Part I","Rodney Jones","Shop Machinery","HSM Vol. 02 No. 2 Mar-Apr 1983","39"
    "Improvement for the Atlas 6" Lathe","Conrad Milster","Lathes","HSM Vol. 02 No. 2 Mar-Apr 1983","44"
    "Triscamp .059 - Part V","Robert A. Washburn","Engines","HSM Vol. 02 No. 2 Mar-Apr 1983","47"
    "How to Taper Off","John Dean","Lathes","HSM Vol. 02 No. 2 Mar-Apr 1983","50"
    "From the Scrapbox: Lathe Accessories - Part I","Frank A. McLean","Lathes","HSM Vol. 02 No. 2 Mar-Apr 1983","52"
    "Fowler Heavy Duty Dial Caliper","Edward G. Hoffman","Miscellaneous","HSM Vol. 02 No. 3 May-Jun 1983","10"
    "Lawrence Drill Press Table","Edward G. Hoffman","Miscellaneous","HSM Vol. 02 No. 3 May-Jun 1983","10"
    "Q & A","Raymond D. Niergarth","General Machining Knowledge","HSM Vol. 02 No. 3 May-Jun 1983","12"
    "Cheap and Effective Belt Dressing","W. Pete Peterka","Miscellaneous","HSM Vol. 02 No. 3 May-Jun 1983","15"
    "Shop of the Month","D. E. Haskins","Hobby Community","HSM Vol. 02 No. 3 May-Jun 1983","16"
    "Machine Shop Calculations: Spacing Holes - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 02 No. 3 May-Jun 1983","18"
    "Plain Talk About Stick Electrode Arc Welding - Part I","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 02 No. 3 May-Jun 1983","22"
    "Sheetmetal Fabrication: Sheetmetal Layout - Part III","Richard J. Loescher","Miscellaneous","HSM Vol. 02 No. 3 May-Jun 1983","24"
    "Bench Grinder Safety - Part II","Edward G. Hoffman","Shop Machinery","HSM Vol. 02 No. 3 May-Jun 1983","26"
    "Machining Your Own Spur Gears","Rudy Kouhoupt","Lathes","HSM Vol. 02 No. 3 May-Jun 1983","28"
    "A Fine Fed Attachment for a Vertical Mill - Part II","G. Wadham","Machining Accessories","HSM Vol. 02 No. 3 May-Jun 1983","32"
    "Metal Turning and Glassblowing with the Metal Lathe - Part III","William T. Roubal, Ph.D.","Projects","HSM Vol. 02 No. 3 May-Jun 1983","34"
    "A 20-Ton Hydraulic Press You Can Build - Part II","Rodney Jones","Shop Machinery","HSM Vol. 02 No. 3 May-Jun 1983","39"
    "Triscamp .059 - Part VI","Robert A. Washburn","Engines","HSM Vol. 02 No. 3 May-Jun 1983","44"
    "Handling Large Bore Tubing","H.R. Durling, Jr.","Miscellaneous","HSM Vol. 02 No. 3 May-Jun 1983","47"
    "Moulded Tool Storage Units","Art Ellis","Shop Accessories","HSM Vol. 02 No. 3 May-Jun 1983","48"
    "Clamp-type Lathe Dog","Don McCormac","Lathes","HSM Vol. 02 No. 3 May-Jun 1983","50"
    "From the Scrapbox: Lathe Accessories - Part II","Frank A. McLean","Lathes","HSM Vol. 02 No. 3 May-Jun 1983","51"
    "Lathe Alignment","Joe Fangohr","Techniques","HSM Vol. 02 No. 3 May-Jun 1983","58"
    "Q & A","Lynn Everett","General Machining Knowledge","HSM Vol. 02 No. 4 Jul-Aug 1983","10"
    "Q & A","Frank A. McLean","General Machining Knowledge","HSM Vol. 02 No. 4 Jul-Aug 1983","10"
    "Q & A","Rudy Kouhoupt","General Machining Knowledge","HSM Vol. 02 No. 4 Jul-Aug 1983","10"
    "Book Review: Making an Eight Day Longcase Clock - Timmins","Clover McKinley","Hobby Community","HSM Vol. 02 No. 4 Jul-Aug 1983","13"
    "Bench Grinder Safety - Part III","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 02 No. 4 Jul-Aug 1983","16"
    "Sheetmetal Layout","Richard J. Loescher","General Machining Knowledge","HSM Vol. 02 No. 4 Jul-Aug 1983","20"
    "Two Machining Aids","John Campbell","Shop Accessories","HSM Vol. 02 No. 4 Jul-Aug 1983","22"
    "About Dimensions","James Hamill","General Machining Knowledge","HSM Vol. 02 No. 4 Jul-Aug 1983","24"
    "Machine Shop Calculations: Bend Allowances","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 02 No. 4 Jul-Aug 1983","26"
    "Plain Talk About Stick Electrode Arc Welding - Welding Machines - Part II","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 02 No. 4 Jul-Aug 1983","28"
    "An Expanding Mandrel","W. Pete Peterka","Lathes","HSM Vol. 02 No. 4 Jul-Aug 1983","30"
    "Making a Worm Wheel Driven Yoke Type Radius Turning Attachment","Theodore M. Clarke","Lathes","HSM Vol. 02 No. 4 Jul-Aug 1983","32"
    "Micrometer Dial for the Tailstock","W.C. Grosjean","Lathes","HSM Vol. 02 No. 4 Jul-Aug 1983","40"
    "A Digital Readout for Your Vertical Milling Machine","Guy Lautard","Mills","HSM Vol. 02 No. 4 Jul-Aug 1983","44"
    "A Homemade Rack for Your Files","Ralph T. Walker","Projects","HSM Vol. 02 No. 4 Jul-Aug 1983","47"
    "A Simple Die Filer","D. W. Holen","Lathes","HSM Vol. 02 No. 4 Jul-Aug 1983","48"
    "Practical Design Hints - Machining","Frederico Strasser","General Machining Knowledge","HSM Vol. 02 No. 4 Jul-Aug 1983","50"
    "Some Remarks on Thread and Screw Making","George A. Kwasniewski","General Machining Knowledge","HSM Vol. 02 No. 4 Jul-Aug 1983","54"
    "Quick-Adjust Depth Stop","Grant W. Wood","Mills","HSM Vol. 02 No. 4 Jul-Aug 1983","56"
    "Simple Chucks to Protect Finished Pieces","W. Pete Peterka","Lathes","HSM Vol. 02 No. 4 Jul-Aug 1983","57"
    "You Need a Rest!","John Dean","Shop Machinery","HSM Vol. 02 No. 4 Jul-Aug 1983","58"
    "From the Scrapbox: A Few Tips on Drilling on a Drill Press or a Vertical Milling Machine","Frank A. McLean","General Machining Knowledge","HSM Vol. 02 No. 4 Jul-Aug 1983","60"
    "The Micro Machinist: Machine Shop in a Cabinet","Rudy Kouhoupt","Hobby Community","HSM Vol. 02 No. 4 Jul-Aug 1983","62"
    "Micrometer Stand","Don McCormac","Shop Accessories","HSM Vol. 02 No. 4 Jul-Aug 1983","64"
    "Fisher Universal Indicator Holder","Edward G. Hoffman","Miscellaneous","HSM Vol. 02 No. 5 Sep-Oct 1983","8"
    "Manhattan 3-in-1 Drill Set","Edward G. Hoffman","Miscellaneous","HSM Vol. 02 No. 5 Sep-Oct 1983","8"
    "Sears Tap and Die Sets","Edward G. Hoffman","Miscellaneous","HSM Vol. 02 No. 5 Sep-Oct 1983","9"
    "Drilling Technology, Grinding Technology and Turning Technology - Krar/Oswald","Raymond D. Niergarth","Hobby Community","HSM Vol. 02 No. 5 Sep-Oct 1983","11"
    "Q & A","Raymond D. Niergarth","General Machining Knowledge","HSM Vol. 02 No. 5 Sep-Oct 1983","12"
    "Q & A","Frank A. McLean","General Machining Knowledge","HSM Vol. 02 No. 5 Sep-Oct 1983","12"
    "Machine Shop Calculations: Indexing","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 02 No. 5 Sep-Oct 1983","22"
    "Versatile Fastener","Grant W. Wood","Miscellaneous","HSM Vol. 02 No. 5 Sep-Oct 1983","26"
    "Welding of Tool and Die Steels","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 02 No. 5 Sep-Oct 1983","28"
    "A Compound and Ram Tailstock","Theodore M. Clarke","Lathes","HSM Vol. 02 No. 5 Sep-Oct 1983","30"
    "The Stirling Hot Air Engine","Thorn L. Mayes","Engines","HSM Vol. 02 No. 5 Sep-Oct 1983","33"
    "A Built-in Drill Guide","John Dean","Shop Machinery","HSM Vol. 02 No. 5 Sep-Oct 1983","39"
    "Balls & Bull Noses - Part I","Guy Lautard","Miscellaneous","HSM Vol. 02 No. 5 Sep-Oct 1983","40"
    "A Pocket Size Camera Tripod","Guy Lautard","Projects","HSM Vol. 02 No. 5 Sep-Oct 1983","45"
    "Practical Design Hints: Machining - Part II","Frederico Strasser","General Machining Knowledge","HSM Vol. 02 No. 5 Sep-Oct 1983","48"
    "From the Scrapbox: How To Machine a Vee Block on a Vertical Milling Machine","Frank A. McLean","Mills","HSM Vol. 02 No. 5 Sep-Oct 1983","52"
    "A Simple Holddown Device","Robert W. Metze","Shop Accessories","HSM Vol. 02 No. 5 Sep-Oct 1983","53"
    "The Micro Machinist: Test Indicator - Part I","Rudy Kouhoupt","Shop Accessories","HSM Vol. 02 No. 5 Sep-Oct 1983","54"
    "Sheetmetal Fabrication: Sheetmetal Layout - Part V","Richard J. Loescher","Miscellaneous","HSM Vol. 02 No. 5 Sep-Oct 1983","56"
    "The Apprentice: Basic Home Shop Tool - The Lathe","Robert A. Washburn","Lathes","HSM Vol. 02 No. 5 Sep-Oct 1983","60"
    "Fire Safety - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 02 No. 5 Sep-Oct 1983","64"
    "Fisher Edge and Center Finders and Tap Guide","Edward G. Hoffman","Miscellaneous","HSM Vol. 02 No. 6 Nov-Dec 1983","12"
    "Glendo Accu-Finish Tool Sharpener","Edward G. Hoffman","Miscellaneous","HSM Vol. 02 No. 6 Nov-Dec 1983","12"
    "Emco Compact 10 Lathe","Edward G. Hoffman","Miscellaneous","HSM Vol. 02 No. 6 Nov-Dec 1983","15"
    "Strike While The Iron Is Hot - Lautard","Clover McKinley","Hobby Community","HSM Vol. 02 No. 6 Nov-Dec 1983","18"
    "Q & A","Raymond D. Niergarth","General Machining Knowledge","HSM Vol. 02 No. 6 Nov-Dec 1983","20"
    "Q & A","Harry Bloom","General Machining Knowledge","HSM Vol. 02 No. 6 Nov-Dec 1983","21"
    "Machine Shop Calculations: Screw Thread Calculations","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 02 No. 6 Nov-Dec 1983","26"
    "Shop Notes on Metals and Metal Identification","Charles K. Hunt","General Machining Knowledge","HSM Vol. 02 No. 6 Nov-Dec 1983","29"
    "Build Your Own Dividing Attachment","Rudy Kouhoupt","Shop Machinery","HSM Vol. 02 No. 6 Nov-Dec 1983","32"
    "Unusual Lathe Work","D. W. Holen","Lathes","HSM Vol. 02 No. 6 Nov-Dec 1983","40"
    "Balls & Bull Noses - Part II","Guy Lautard","Miscellaneous","HSM Vol. 02 No. 6 Nov-Dec 1983","42"
    "A Simple Lathe Dog","James D. Scharplaz, P.E.","Lathes","HSM Vol. 02 No. 6 Nov-Dec 1983","46"
    "Conserving Cutting Oils","W.B Vaughan","General Machining Knowledge","HSM Vol. 02 No. 6 Nov-Dec 1983","47"
    "Practical Design Hints: Assembly","Frederico Strasser","General Machining Knowledge","HSM Vol. 02 No. 6 Nov-Dec 1983","48"
    "The Micro Machinist: Test Indicator - Part II","Rudy Kouhoupt","Shop Accessories","HSM Vol. 02 No. 6 Nov-Dec 1983","52"
    "From the Scrapbox: A Fireside Chat About Lathe Chucks","Frank A. McLean","Lathes","HSM Vol. 02 No. 6 Nov-Dec 1983","54"
    "Sheetmetal Fabrication: Sheetmetal Layout - Part VI","Richard J. Loescher","Miscellaneous","HSM Vol. 02 No. 6 Nov-Dec 1983","58"
    "The Apprentice: Lathe Accessories","Robert A. Washburn","Lathes","HSM Vol. 02 No. 6 Nov-Dec 1983","60"
    "Fire Safety - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 02 No. 6 Nov-Dec 1983","64"
    "Fisher 5\"" Sine Bar","Edward G. Hoffman","Miscellaneous","HSM Vol. 03 No. 1 Jan-Feb 1984","8"
    "SPI Space Block Set","Edward G. Hoffman","Miscellaneous","HSM Vol. 03 No. 1 Jan-Feb 1984","8"
    "Emco Maier Maximat Super II","Edward G. Hoffman","Miscellaneous","HSM Vol. 03 No. 1 Jan-Feb 1984","9"
    "Q & A","Robert A. Washburn","General Machining Knowledge","HSM Vol. 03 No. 1 Jan-Feb 1984","12"
    "Q & A","Raymond D. Niergarth","General Machining Knowledge","HSM Vol. 03 No. 1 Jan-Feb 1984","12"
    "Machine Shop Calculations: Screw Thread Calculations - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 03 No. 1 Jan-Feb 1984","18"
    "Shop of the Month","J. C. Funk","Hobby Community","HSM Vol. 03 No. 1 Jan-Feb 1984","20"
    "Gas Tungsten Arc Welding - Part I","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 03 No. 1 Jan-Feb 1984","22"
    "Welding: Gas Tungsten Arc Welding - Part I","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 03 No. 1 Jan-Feb 1984","22"
    "Reconditioning a Lathe - Part I","Harry Bloom","Lathes","HSM Vol. 03 No. 1 Jan-Feb 1984","24"
    "Weldments Can Replace Castings","Richard B. Walker","Welding/Foundry/Forging","HSM Vol. 03 No. 1 Jan-Feb 1984","31"
    "Conversion of a Gear-driven Shaper to Hydraulic Drive","Theodore M. Clarke","Shop Machinery","HSM Vol. 03 No. 1 Jan-Feb 1984","36"
    "Cutting Fluids and Compounds","John Marcus, Ph.D.","General Machining Knowledge","HSM Vol. 03 No. 1 Jan-Feb 1984","40"
    "Column Storage Box for a Drill Press","W.B Vaughan","Shop Accessories","HSM Vol. 03 No. 1 Jan-Feb 1984","44"
    "Practical Design Hints: Assembly - Part IV","Frederico Strasser","General Machining Knowledge","HSM Vol. 03 No. 1 Jan-Feb 1984","46"
    "The Micro Machinist: Compressed Air Motor - Part I","Rudy Kouhoupt","Projects","HSM Vol. 03 No. 1 Jan-Feb 1984","48"
    "From the Scrapbox: Sharpening Two-lip End Mills","Frank A. McLean","General Machining Knowledge","HSM Vol. 03 No. 1 Jan-Feb 1984","50"
    "The Apprentice: Lathe Turning Tools","Robert A. Washburn","Lathes","HSM Vol. 03 No. 1 Jan-Feb 1984","52"
    "Fire Safety - Part III","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 03 No. 1 Jan-Feb 1984","56"
    "Dupli-Carver Band Saw","Edward G. Hoffman","Miscellaneous","HSM Vol. 03 No. 2 Mar-Apr 1984","8"
    "Sears 15-1/2" Drill Press","Edward G. Hoffman","Miscellaneous","HSM Vol. 03 No. 2 Mar-Apr 1984","10"
    "Fisher "Pee Dee" Thread Measuring Wires","Edward G. Hoffman","Miscellaneous","HSM Vol. 03 No. 2 Mar-Apr 1984","11"
    "Q & A","Raymond D. Niergarth","General Machining Knowledge","HSM Vol. 03 No. 2 Mar-Apr 1984","12"
    "Extra Length Combined Drill and Countersinks","Michael T. Yamamoto","Shop Accessories","HSM Vol. 03 No. 2 Mar-Apr 1984","18"
    "Center Test Indicator","Frank G. Brockardt","Mills","HSM Vol. 03 No. 2 Mar-Apr 1984","19"
    "Machine Shop Calculations: Screw Thread Calculations - Part III","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 03 No. 2 Mar-Apr 1984","20"
    "Every Pot Finds Its Own Lid","Guy Lautard","Miscellaneous","HSM Vol. 03 No. 2 Mar-Apr 1984","24"
    "Gas Tungsten Arc Welding - Part II","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 03 No. 2 Mar-Apr 1984","26"
    "Welding: Gas Tungsten Arc Welding - Part II","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 03 No. 2 Mar-Apr 1984","26"
    "A Practical Suds Pump","Keith E. Passino","Shop Accessories","HSM Vol. 03 No. 2 Mar-Apr 1984","28"
    "Sliding Band Saw Vise","Ed Merrifield","Shop Accessories","HSM Vol. 03 No. 2 Mar-Apr 1984","35"
    "An Automatic Parallel","Rudy Kouhoupt","Shop Accessories","HSM Vol. 03 No. 2 Mar-Apr 1984","36"
    "Spacing Drill Guide Makes It Easy","John Dean","Shop Machinery","HSM Vol. 03 No. 2 Mar-Apr 1984","39"
    "Reconditioning a Lathe - Part II","Harry Bloom","Lathes","HSM Vol. 03 No. 2 Mar-Apr 1984","40"
    "V-Blocks Quickly Made","John Dean","Shop Accessories","HSM Vol. 03 No. 2 Mar-Apr 1984","43"
    "Lathe Chip Shield","James Berger","Lathes","HSM Vol. 03 No. 2 Mar-Apr 1984","44"
    "Don't Fake a Casting - Make a Casting: Equipment & Supplies - Part I","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 03 No. 2 Mar-Apr 1984","50"
    "Tool Holder Retainer","H. T. Biddle","Lathes","HSM Vol. 03 No. 2 Mar-Apr 1984","55"
    "From the Scrapbox: How to Machine an Angle Plate","Frank A. McLean","General Machining Knowledge","HSM Vol. 03 No. 2 Mar-Apr 1984","56"
    "The Micro Machinist: Compressed Air Motor - Part II","Rudy Kouhoupt","Projects","HSM Vol. 03 No. 2 Mar-Apr 1984","58"
    "The Apprentice: Boring & Lathe Measuring Tools","Robert A. Washburn","Lathes","HSM Vol. 03 No. 2 Mar-Apr 1984","60"
    "Heavy-Duty Centers","Chet Parshall","Lathes","HSM Vol. 03 No. 2 Mar-Apr 1984","63"
    "Fire Safety - Part IV","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 03 No. 2 Mar-Apr 1984","64"
    "Sears Bench Grinder","Edward G. Hoffman","Miscellaneous","HSM Vol. 03 No. 3 May-Jun 1984","8"
    "Mitchell Abrasive Cords and Tapes","Edward G. Hoffman","Miscellaneous","HSM Vol. 03 No. 3 May-Jun 1984","9"
    "Starrett Trammel Set","Edward G. Hoffman","Miscellaneous","HSM Vol. 03 No. 3 May-Jun 1984","9"
    "Height Gage","Lewis Jenkins","Shop Accessories","HSM Vol. 03 No. 3 May-Jun 1984","10"
    "Q & A","Raymond D. Niergarth","General Machining Knowledge","HSM Vol. 03 No. 3 May-Jun 1984","12"
    "Q & A","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 03 No. 3 May-Jun 1984","12"
    "More on a Gear-driven Shaper Conversion","Theodore M. Clarke","Shop Machinery","HSM Vol. 03 No. 3 May-Jun 1984","16"
    "Machine Shop Calculations: Screw Thread Calculations - Part IV","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 03 No. 3 May-Jun 1984","20"
    "Rapid Machine Tapping Drill Press","William T. Roubal, Ph.D.","Shop Machinery","HSM Vol. 03 No. 3 May-Jun 1984","22"
    "Building a Portable Vise Bench","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 03 No. 3 May-Jun 1984","24"
    "Welding: Building a Portable Vise Bench","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 03 No. 3 May-Jun 1984","24"
    "Rotary Milling Table - Part I","S. F. Kadron","Shop Machinery","HSM Vol. 03 No. 3 May-Jun 1984","28"
    "A Large Steady Rest from the Scrap Pile","J. O. Barbour, Jr.","Lathes","HSM Vol. 03 No. 3 May-Jun 1984","35"
    "A Milling Machine for Your Lathe - Part I","John Snyder","Lathes","HSM Vol. 03 No. 3 May-Jun 1984","36"
    "Drawing Up a Bargain","Guy Lautard","Shop Accessories","HSM Vol. 03 No. 3 May-Jun 1984","45"
    "Reconditioning a Lathe - Part III","Harry Bloom","Lathes","HSM Vol. 03 No. 3 May-Jun 1984","48"
    "Machining Thin Disks and Rings","D. E. Johnson","Miscellaneous","HSM Vol. 03 No. 3 May-Jun 1984","50"
    "Don't Fake a Casting - Make a Casting: Equipment & Supplies - Part II","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 03 No. 3 May-Jun 1984","52"
    "From the Scrapbox: Flycutters","Frank A. McLean","General Machining Knowledge","HSM Vol. 03 No. 3 May-Jun 1984","56"
    "The Micro Machinist: Compressed Air Motor - Part III","Rudy Kouhoupt","Projects","HSM Vol. 03 No. 3 May-Jun 1984","58"
    "The Apprentice: Lathe Measuring Instruments","Robert A. Washburn","Lathes","HSM Vol. 03 No. 3 May-Jun 1984","60"
    "Fire Safety - Part V","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 03 No. 3 May-Jun 1984","63"
    "Emco Maier FB-2 Milling Machine","Edward G. Hoffman","Miscellaneous","HSM Vol. 03 No. 4 Jul-Aug 1984","6"
    "Criterion Boring Head","Edward G. Hoffman","Miscellaneous","HSM Vol. 03 No. 4 Jul-Aug 1984","8"
    "Northwestern Clamping Kit","Edward G. Hoffman","Miscellaneous","HSM Vol. 03 No. 4 Jul-Aug 1984","8"
    "More on Milling with a Drill Press","Theodore M. Clarke","Shop Machinery","HSM Vol. 03 No. 4 Jul-Aug 1984","10"
    "Q & A","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 03 No. 4 Jul-Aug 1984","12"
    "Q & A","Raymond D. Niergarth","General Machining Knowledge","HSM Vol. 03 No. 4 Jul-Aug 1984","12"
    "A Toolpost Grinder","John Dean","Lathes","HSM Vol. 03 No. 4 Jul-Aug 1984","18"
    "Machine Shop Calculations: Speeds And Feeds - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 03 No. 4 Jul-Aug 1984","20"
    "Buying Used Welding Equipment","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 03 No. 4 Jul-Aug 1984","24"
    "Welding: Buying Used Welding Equipment","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 03 No. 4 Jul-Aug 1984","24"
    "Temporary Self-locking Stub Mandrel","Philip Duclos","Lathes","HSM Vol. 03 No. 4 Jul-Aug 1984","28"
    "Rotary Milling Table - Part II","S. F. Kadron","Shop Machinery","HSM Vol. 03 No. 4 Jul-Aug 1984","30"
    "Screwdriver Blade Grinding Jig","Kim E. Plank","Miscellaneous","HSM Vol. 03 No. 4 Jul-Aug 1984","35"
    "Modifications to a Maximat V-8 Lathe","Dave Marshall","Lathes","HSM Vol. 03 No. 4 Jul-Aug 1984","36"
    "Oxy-fuel Cutting Guide Jig","Orley Phillips","Miscellaneous","HSM Vol. 03 No. 4 Jul-Aug 1984","42"
    "A Milling Machine for Your Lathe - Part II","John Snyder","Lathes","HSM Vol. 03 No. 4 Jul-Aug 1984","44"
    "Reconditioning a Lathe - Part IV","Harry Bloom","Lathes","HSM Vol. 03 No. 4 Jul-Aug 1984","49"
    "Don't Fake a Casting - Make a Casting: Equipment & Supplies - Part III","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 03 No. 4 Jul-Aug 1984","52"
    "A Toolpost Problem Solver","John Dean","Lathes","HSM Vol. 03 No. 4 Jul-Aug 1984","55"
    "From the Scrapbox: How to Use the Vertical Milling Machine","Frank A. McLean","Mills","HSM Vol. 03 No. 4 Jul-Aug 1984","56"
    "The Micro Machinist: Boring Bars - Part I","Rudy Kouhoupt","Lathes","HSM Vol. 03 No. 4 Jul-Aug 1984","58"
    "The Apprentice: Threading on the Lathe","Robert A. Washburn","Lathes","HSM Vol. 03 No. 4 Jul-Aug 1984","60"
    "A Thin Slice of V-Block","John Dean","Shop Accessories","HSM Vol. 03 No. 4 Jul-Aug 1984","63"
    "Good Housekeeping - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 03 No. 4 Jul-Aug 1984","64"
    "Darex M3 Drill Sharpener","Edward G. Hoffman","Miscellaneous","HSM Vol. 03 No. 5 Sep-Oct 1984","8"
    "S-T Industries 12\"" Height Gage","Edward G. Hoffman","Miscellaneous","HSM Vol. 03 No. 5 Sep-Oct 1984","8"
    "Clamping Work to the Mill Table","Harold Timm","Mills","HSM Vol. 03 No. 5 Sep-Oct 1984","10"
    "Double the Capacity of Your Lathe","J. O. Barbour, Jr.","Lathes","HSM Vol. 03 No. 5 Sep-Oct 1984","18"
    "Machine Shop Calculations: Speeds And Feeds - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 03 No. 5 Sep-Oct 1984","20"
    "A Make-Do Surface Grinder - Part I","Richard B. Walker","Shop Machinery","HSM Vol. 03 No. 5 Sep-Oct 1984","24"
    "Making an Automatic Feed for a Milling Machine","J. W. (Bill) Reichart","Mills","HSM Vol. 03 No. 5 Sep-Oct 1984","31"
    "Triplex","E. I. Schefer","Shop Machinery","HSM Vol. 03 No. 5 Sep-Oct 1984","34"
    "A Milling Machine for Your Lathe - Part III","John Snyder","Lathes","HSM Vol. 03 No. 5 Sep-Oct 1984","36"
    "Construction & Use of the Lathe Carriage Stop","D. E. Johnson","Lathes","HSM Vol. 03 No. 5 Sep-Oct 1984","39"
    "Reconditioning a Lathe - Part V","Harry Bloom","Lathes","HSM Vol. 03 No. 5 Sep-Oct 1984","42"
    "A Temporary Aluminum Furnace","Philip Duclos","Welding/Foundry/Forging","HSM Vol. 03 No. 5 Sep-Oct 1984","44"
    "Don't Fake a Casting - Make a Casting: Ramming the Mold for a Metal Casting","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 03 No. 5 Sep-Oct 1984","46"
    "From the Scrapbox: External Threads - Part I","Frank A. McLean","General Machining Knowledge","HSM Vol. 03 No. 5 Sep-Oct 1984","50"
    "The Micro Machinist: Boring Bars - Part II","Rudy Kouhoupt","Lathes","HSM Vol. 03 No. 5 Sep-Oct 1984","56"
    "Good Housekeeping - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 03 No. 5 Sep-Oct 1984","60"
    "The Apprentice: Selecting a Milling Machine","Robert A. Washburn","Mills","HSM Vol. 03 No. 5 Sep-Oct 1984","60"
    "Dillon Mk III Welding & Cutting Torch","Edward G. Hoffman","Miscellaneous","HSM Vol. 03 No. 6 Nov-Dec 1984","8"
    "A New Year Message","Rudy Kouhoupt","Miscellaneous","HSM Vol. 03 No. 6 Nov-Dec 1984","12"
    "Holding Small Objects","George L. Taft","General Machining Knowledge","HSM Vol. 03 No. 6 Nov-Dec 1984","17"
    "Machine Shop Calculations: Speeds And Feeds - Part III","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 03 No. 6 Nov-Dec 1984","18"
    "Q & A","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 03 No. 6 Nov-Dec 1984","22"
    "A Make-Do Surface Grinder - Part II","Richard B. Walker","Shop Machinery","HSM Vol. 03 No. 6 Nov-Dec 1984","24"
    "How Would You Make This Part?","D. W. Holen","Projects","HSM Vol. 03 No. 6 Nov-Dec 1984","31"
    "Fabricating the Tumbler Link","D. W. Holen","Projects","HSM Vol. 03 No. 6 Nov-Dec 1984","32"
    "A Bit of Inspiration","Guy Lautard","Miscellaneous","HSM Vol. 03 No. 6 Nov-Dec 1984","34"
    "Five-Layer Lazy Susan Drill Index","John B. Gascoyne","Shop Accessories","HSM Vol. 03 No. 6 Nov-Dec 1984","36"
    "Concave and Convex Radius Cutter","Bruce Jones","Lathes","HSM Vol. 03 No. 6 Nov-Dec 1984","40"
    "Making the Home Shop Pay","John W. Oder","Projects","HSM Vol. 03 No. 6 Nov-Dec 1984","45"
    "Reconditioning a Lathe - Part VI","Harry Bloom","Lathes","HSM Vol. 03 No. 6 Nov-Dec 1984","48"
    "Fear Neither Sphere Nor Hemisphere","John Dean","Techniques","HSM Vol. 03 No. 6 Nov-Dec 1984","50"
    "Proper Grounding of Power Tools","Terry Wireman","General Machining Knowledge","HSM Vol. 03 No. 6 Nov-Dec 1984","52"
    "Swaging Down a Copper Pipe Elbow","Guy Lautard","Miscellaneous","HSM Vol. 03 No. 6 Nov-Dec 1984","54"
    "From the Scrapbox: Drilling and Tapping Hints","Frank A. McLean","General Machining Knowledge","HSM Vol. 03 No. 6 Nov-Dec 1984","56"
    "The Micro Machinist: Milling Accessories - Part I","Rudy Kouhoupt","Mills","HSM Vol. 03 No. 6 Nov-Dec 1984","58"
    "The Apprentice: The Basic Approach to Using the Milling Machine","Robert A. Washburn","Mills","HSM Vol. 03 No. 6 Nov-Dec 1984","60"
    "Shop Layout - Part I","Edward G. Hoffman","Miscellaneous","HSM Vol. 03 No. 6 Nov-Dec 1984","64"
    "Machine Shop Calculations: Grinding Wheels","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 04 No. 1 Jan-Feb 1985","20"
    "Sky Charger - Part I","Robert A. Washburn","Engines","HSM Vol. 04 No. 1 Jan-Feb 1985","24"
    "Build a Gimbaled Ship's Lamp","William F. Green","Projects","HSM Vol. 04 No. 1 Jan-Feb 1985","35"
    "How to Make Quality Photos of Machined Metal Projects at Home","Dennis Ivy","Miscellaneous","HSM Vol. 04 No. 1 Jan-Feb 1985","38"
    "A "Showpiece" Challenge","Philip Duclos","Projects","HSM Vol. 04 No. 1 Jan-Feb 1985","44"
    "A Steel Beam Trammel - Part I","Guy Lautard","Shop Accessories","HSM Vol. 04 No. 1 Jan-Feb 1985","46"
    "Don't Fake a Casting, Make a Casting: The Pattern - Part I","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 04 No. 1 Jan-Feb 1985","52"
    "From the Scrapbox: Boring Internal Threads","Frank A. McLean","Lathes","HSM Vol. 04 No. 1 Jan-Feb 1985","56"
    "The Micro Machinist: Milling Accessories - Part II","Rudy Kouhoupt","Mills","HSM Vol. 04 No. 1 Jan-Feb 1985","62"
    "Shop Layout - Part II","Edward G. Hoffman","Miscellaneous","HSM Vol. 04 No. 1 Jan-Feb 1985","64"
    "Product Review: Anton Angular Gage Blocks","Edward G. Hoffman","Hobby Community","HSM Vol. 04 No. 2 Mar-Apr 1985","10"
    "Product Review: Sears Hardwood Machinist's Tool Chest","Edward G. Hoffman","Hobby Community","HSM Vol. 04 No. 2 Mar-Apr 1985","10"
    "Product Review: Quorn Mark II Grinder","Edward G. Hoffman","Hobby Community","HSM Vol. 04 No. 2 Mar-Apr 1985","12"
    "Machine Shop Calculations: Angular Measurement - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 04 No. 2 Mar-Apr 1985","20"
    "Keep that Universal Chuck Accurate","W. Pete Peterka","Lathes","HSM Vol. 04 No. 2 Mar-Apr 1985","22"
    "Adjustable Parallels","Philip Duclos","Shop Accessories","HSM Vol. 04 No. 2 Mar-Apr 1985","24"
    "Build Your Own Face Plate","Marlyn Hadley","Lathes","HSM Vol. 04 No. 2 Mar-Apr 1985","28"
    "Spindle Stop for a 10-K","Norman H. Bennett","Lathes","HSM Vol. 04 No. 2 Mar-Apr 1985","31"
    "Sky Charger - Part II","Robert A. Washburn","Engines","HSM Vol. 04 No. 2 Mar-Apr 1985","32"
    "A Steel Beam Trammel - Part II","Guy Lautard","Shop Accessories","HSM Vol. 04 No. 2 Mar-Apr 1985","35"
    "Getting the Most from Your Center Gage and Other Threading Gages","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 04 No. 2 Mar-Apr 1985","38"
    "Lathe Carriage Oiler","Norman H. Bennett","Lathes","HSM Vol. 04 No. 2 Mar-Apr 1985","41"
    "Turning Ornamental Shapes","Conrad Milster","Lathes","HSM Vol. 04 No. 2 Mar-Apr 1985","42"
    "Build an Electric Gun","Robert W. Metze","Gunsmithing","HSM Vol. 04 No. 2 Mar-Apr 1985","46"
    "Shop Layout - Part III","Edward G. Hoffman","Miscellaneous","HSM Vol. 04 No. 2 Mar-Apr 1985","51"
    "Don't Fake A Casting, Make A Casting: The Pattern - Part II","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 04 No. 2 Mar-Apr 1985","52"
    "From the Scrapbox: How to Broach Small Holes","Frank A. McLean","Lathes","HSM Vol. 04 No. 2 Mar-Apr 1985","56"
    "The Apprentice: Using the Wiggler and Edge Finder","Robert A. Washburn","Mills","HSM Vol. 04 No. 2 Mar-Apr 1985","58"
    "The Micro Machinist: Milling Accessories - Part III","Rudy Kouhoupt","Mills","HSM Vol. 04 No. 2 Mar-Apr 1985","62"
    "Product Review: Scherr-Tumico Machinist Tool Set","Edward G. Hoffman","Hobby Community","HSM Vol. 04 No. 3 May-Jun 1985","8"
    "Product Review: Athens Centering Thimbles","Edward G. Hoffman","Hobby Community","HSM Vol. 04 No. 3 May-Jun 1985","10"
    "Product Review: ShopTronics Digital Readout","Edward G. Hoffman","Hobby Community","HSM Vol. 04 No. 3 May-Jun 1985","11"
    "Machine Shop Calculations: Angular Measurement - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 04 No. 3 May-Jun 1985","16"
    "Q & A","John B. Gascoyne","General Machining Knowledge","HSM Vol. 04 No. 3 May-Jun 1985","18"
    "Q & A","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 04 No. 3 May-Jun 1985","18"
    "Q & A","Frank A. McLean","General Machining Knowledge","HSM Vol. 04 No. 3 May-Jun 1985","19"
    "Q & A","Raymond D. Niergarth","General Machining Knowledge","HSM Vol. 04 No. 3 May-Jun 1985","19"
    "Measuring Pitch Diameter","Charlie Dondro","General Machining Knowledge","HSM Vol. 04 No. 3 May-Jun 1985","20"
    "Micrometer Attachment for Lathe Lead Screws","John P. McDermott, Jr.","Lathes","HSM Vol. 04 No. 3 May-Jun 1985","22"
    "Bastion of the Belts","David Jones","Hobby Community","HSM Vol. 04 No. 3 May-Jun 1985","26"
    "Some Light on the Subject","Arthur Crow","Shop Accessories","HSM Vol. 04 No. 3 May-Jun 1985","31"
    "Square References, Their Design, Construction, and Inspection","Gary F. Reisdorf","Shop Accessories","HSM Vol. 04 No. 3 May-Jun 1985","32"
    "Sky Charger - Part III","Robert A. Washburn","Engines","HSM Vol. 04 No. 3 May-Jun 1985","36"
    "Tailstock Die Holder","Harold Timm","Lathes","HSM Vol. 04 No. 3 May-Jun 1985","40"
    "Don't Fake A Casting, Make A Casting: The Pattern - Part III","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 04 No. 3 May-Jun 1985","42"
    "Square Pegs and Round Holes","Luke Lukens","General Machining Knowledge","HSM Vol. 04 No. 3 May-Jun 1985","46"
    "From the Scrapbox: Universal Surface Gage","Frank A. McLean","Shop Accessories","HSM Vol. 04 No. 3 May-Jun 1985","48"
    "The Apprentice: Three Types of Unique Mill Table Clamps","Robert A. Washburn","Shop Accessories","HSM Vol. 04 No. 3 May-Jun 1985","55"
    "The Micro Machinist: Use of Dimensions","Rudy Kouhoupt","General Machining Knowledge","HSM Vol. 04 No. 3 May-Jun 1985","58"
    "Drill Shank Welding Jig","Arthur Crow","Welding/Foundry/Forging","HSM Vol. 04 No. 3 May-Jun 1985","63"
    "Product Review: S-T Industries Electronic Digital Caliper","Edward G. Hoffman","Hobby Community","HSM Vol. 04 No. 4 Jul-Aug 1985","8"
    "Product Review: Craftmark Zero/Zero Center Finder","Edward G. Hoffman","Hobby Community","HSM Vol. 04 No. 4 Jul-Aug 1985","10"
    "Product Review: Anton Toolmaker's Dream Kit","Edward G. Hoffman","Hobby Community","HSM Vol. 04 No. 4 Jul-Aug 1985","11"
    "Q & A","Frank A. McLean","General Machining Knowledge","HSM Vol. 04 No. 4 Jul-Aug 1985","14"
    "The Art of Engraving","Guy Lautard","General Machining Knowledge","HSM Vol. 04 No. 4 Jul-Aug 1985","15"
    "Corrections to Concave and Convex Radius Cutter","Bruce Jones","Lathes","HSM Vol. 04 No. 4 Jul-Aug 1985","19"
    "End Mill Sharpening Fixture","Robert S. Hedin","Shop Accessories","HSM Vol. 04 No. 4 Jul-Aug 1985","22"
    "Grinding Wheel Arbor","Jeff Bertrand","Shop Accessories","HSM Vol. 04 No. 4 Jul-Aug 1985","25"
    "Firing Model Napoleon Field Gun - Part I","William F. Green","Gunsmithing","HSM Vol. 04 No. 4 Jul-Aug 1985","26"
    "Building a Belt Sander","George W. Genevro","Shop Machinery","HSM Vol. 04 No. 4 Jul-Aug 1985","32"
    "Some Pointers on Rotary Table Work","Guy Lautard","Shop Machinery","HSM Vol. 04 No. 4 Jul-Aug 1985","40"
    "Sky Charger - Part IV","Robert A. Washburn","Engines","HSM Vol. 04 No. 4 Jul-Aug 1985","42"
    "Setting Up a Home Foundry","Dave Gingery","Welding/Foundry/Forging","HSM Vol. 04 No. 4 Jul-Aug 1985","46"
    "From the Scrapbox: A Small Machine Vise","Frank A. McLean","Shop Accessories","HSM Vol. 04 No. 4 Jul-Aug 1985","49"
    "Don't Fake A Casting, Make A Casting: The Pattern - Part IV","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 04 No. 4 Jul-Aug 1985","52"
    "The Micro Machinist: Slitting Saws","Rudy Kouhoupt","Mills","HSM Vol. 04 No. 4 Jul-Aug 1985","56"
    "The Apprentice: Dividing Head for the Milling Table","Robert A. Washburn","Shop Accessories","HSM Vol. 04 No. 4 Jul-Aug 1985","58"
    "Shop Layout - Part IV","Edward G. Hoffman","Miscellaneous","HSM Vol. 04 No. 4 Jul-Aug 1985","64"
    "Product Review: Infinity Precisions Boring Head","Edward G. Hoffman","Hobby Community","HSM Vol. 04 No. 5 Sep-Oct 1985","8"
    "Product Review: Kalamazoo 4.00 Belt Sander","Edward G. Hoffman","Hobby Community","HSM Vol. 04 No. 5 Sep-Oct 1985","10"
    "Product Review: ATCO Combo-Cube","Edward G. Hoffman","Hobby Community","HSM Vol. 04 No. 5 Sep-Oct 1985","12"
    "Q & A","Rudy Kouhoupt","General Machining Knowledge","HSM Vol. 04 No. 5 Sep-Oct 1985","18"
    "Q & A","Frank A. McLean","General Machining Knowledge","HSM Vol. 04 No. 5 Sep-Oct 1985","18"
    "Machine Shop Calculations: Gears - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 04 No. 5 Sep-Oct 1985","19"
    ""Slow Poke" Small Keyway Broach","Philip Duclos","Shop Accessories","HSM Vol. 04 No. 5 Sep-Oct 1985","22"
    "Sky Charger - Part V","Robert A. Washburn","Engines","HSM Vol. 04 No. 5 Sep-Oct 1985","27"
    "Solving a Weighty Problem","Bill Davidson","Miscellaneous","HSM Vol. 04 No. 5 Sep-Oct 1985","32"
    "Firing Model Napoleon Field Gun - Part II","William F. Green","Gunsmithing","HSM Vol. 04 No. 5 Sep-Oct 1985","38"
    "From the Scrapbox: A New Vertical Milling Machine","Frank A. McLean","Mills","HSM Vol. 04 No. 5 Sep-Oct 1985","42"
    "Don't Fake A Casting, Make A Casting: The Pattern - Part V","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 04 No. 5 Sep-Oct 1985","48"
    "The Apprentice: A Potpourri","Robert A. Washburn","General Machining Knowledge","HSM Vol. 04 No. 5 Sep-Oct 1985","54"
    "The Micro Machinist: Steam Engine - Part I","Rudy Kouhoupt","Engines","HSM Vol. 04 No. 5 Sep-Oct 1985","58"
    "Shop Layout - Part V","Edward G. Hoffman","Miscellaneous","HSM Vol. 04 No. 5 Sep-Oct 1985","64"
    "Product Review: TWF Industries Machinist Assortment","Edward G. Hoffman","Hobby Community","HSM Vol. 04 No. 6 Nov-Dec 1985","6"
    "Product Review: Westhoff Mighty Mag","Edward G. Hoffman","Hobby Community","HSM Vol. 04 No. 6 Nov-Dec 1985","6"
    "Product Review: S-T Industries Universal Dial Indicator Test Set","Edward G. Hoffman","Hobby Community","HSM Vol. 04 No. 6 Nov-Dec 1985","8"
    "Manufacture of the Springfield Model 1903 Service Rifle","Guy Lautard","Gunsmithing","HSM Vol. 04 No. 6 Nov-Dec 1985","17"
    "A Drill Holder for Your Lathe","George A. Peavey","Lathes","HSM Vol. 04 No. 6 Nov-Dec 1985","18"
    "Machine Shop Calculations: Gears - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 04 No. 6 Nov-Dec 1985","20"
    "Q & A","Richard E. Evans","General Machining Knowledge","HSM Vol. 04 No. 6 Nov-Dec 1985","22"
    "Drill Press Tapping Tool","Harold Mason","Shop Machinery","HSM Vol. 04 No. 6 Nov-Dec 1985","24"
    "CAD for the Common Man","Annette Hinshaw","Computers","HSM Vol. 04 No. 6 Nov-Dec 1985","28"
    "Milling Machine Chip Shield","James Berger","Mills","HSM Vol. 04 No. 6 Nov-Dec 1985","30"
    "Metal Forming Brake Attachment","J. O. Barbour, Jr.","Shop Accessories","HSM Vol. 04 No. 6 Nov-Dec 1985","35"
    "Sky Charger - Part VI","Robert A. Washburn","Engines","HSM Vol. 04 No. 6 Nov-Dec 1985","38"
    "Toolmaker's Clamps","Guy Lautard","Shop Accessories","HSM Vol. 04 No. 6 Nov-Dec 1985","40"
    "Firing Model Napoleon Field Gun - Part III","William F. Green","Gunsmithing","HSM Vol. 04 No. 6 Nov-Dec 1985","44"
    "A Cutting Tool for Machining Aluminum","James R. Lewis","Lathes","HSM Vol. 04 No. 6 Nov-Dec 1985","48"
    "Don't Fake A Casting, Make A Casting: The Pattern - Part VI","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 04 No. 6 Nov-Dec 1985","50"
    "The Apprentice: The Workings of a Sine Bar - Part I","Robert A. Washburn","Shop Accessories","HSM Vol. 04 No. 6 Nov-Dec 1985","54"
    "Cross-feed Cover for a 10-K","Norman H. Bennett","Lathes","HSM Vol. 04 No. 6 Nov-Dec 1985","57"
    "The Micro Machinist: Steam Engine - Part II","Rudy Kouhoupt","Engines","HSM Vol. 04 No. 6 Nov-Dec 1985","58"
    "Product Review: BTI - Super T Drivers","Edward G. Hoffman","Hobby Community","HSM Vol. 05 No. 1 Jan-Feb 1986","10"
    "Product Review: Zero-It Indicator Adapter","Edward G. Hoffman","Hobby Community","HSM Vol. 05 No. 1 Jan-Feb 1986","10"
    "Q & A","Frank A. McLean","General Machining Knowledge","HSM Vol. 05 No. 1 Jan-Feb 1986","13"
    "More Inspiration - Part I","John W. Oder","Engines","HSM Vol. 05 No. 1 Jan-Feb 1986","14"
    "Jaws","Richard S. Torgerson","Lathes","HSM Vol. 05 No. 1 Jan-Feb 1986","17"
    "Screwcutting Threads","Ted Wright","Lathes","HSM Vol. 05 No. 1 Jan-Feb 1986","20"
    "Adjustable, Traveling Dial Indicator Rod","John B. Gascoyne","Lathes","HSM Vol. 05 No. 1 Jan-Feb 1986","25"
    "Parts Cleaner","Ray E. Starnes","Shop Accessories","HSM Vol. 05 No. 1 Jan-Feb 1986","28"
    "Cellulose Tape - Silent Magic","B. Beck","Miscellaneous","HSM Vol. 05 No. 1 Jan-Feb 1986","30"
    "A Firing Model Napoleon Field Gun - Part IV","William F. Green","Gunsmithing","HSM Vol. 05 No. 1 Jan-Feb 1986","31"
    "Sky Charger - Part VII","Robert A. Washburn","Engines","HSM Vol. 05 No. 1 Jan-Feb 1986","34"
    "Home-Built Motor Reversing Switch","Bruce Jones","Miscellaneous","HSM Vol. 05 No. 1 Jan-Feb 1986","39"
    "Threading Set-up Chart","Bruce Jones","General Machining Knowledge","HSM Vol. 05 No. 1 Jan-Feb 1986","39"
    "Updating Flat Belt Driven Equipment","James E. Oslislo","Shop Machinery","HSM Vol. 05 No. 1 Jan-Feb 1986","40"
    "From the Scrapbox: How to Make a Special Tap","Frank A. McLean","Shop Accessories","HSM Vol. 05 No. 1 Jan-Feb 1986","44"
    "Don't Fake a Casting, Make a Casting: Metals for Casting - Part I","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 05 No. 1 Jan-Feb 1986","47"
    "The Apprentice: The Workings of a Sine Bar - Part II","Robert A. Washburn","Shop Accessories","HSM Vol. 05 No. 1 Jan-Feb 1986","49"
    "Cutting Bastard Threads on a Quick Change Lathe","E. T. Feller","Lathes","HSM Vol. 05 No. 1 Jan-Feb 1986","54"
    "A Chuckboard","Robert Coleman","Lathes","HSM Vol. 05 No. 1 Jan-Feb 1986","55"
    "Machine Shop Calculations: Gears - Part III","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 05 No. 1 Jan-Feb 1986","56"
    "The Micro Machinist: Steam Engine - Part III","Rudy Kouhoupt","Engines","HSM Vol. 05 No. 1 Jan-Feb 1986","58"
    "Shop Storage - Part II","Edward G. Hoffman","Miscellaneous","HSM Vol. 05 No. 1 Jan-Feb 1986","64"
    "Product Review: Challenger Gage Block Set","Edward G. Hoffman","Hobby Community","HSM Vol. 05 No. 2 Mar-Apr 1986","10"
    "Product Review: Westhoff Magna-Base","Edward G. Hoffman","Hobby Community","HSM Vol. 05 No. 2 Mar-Apr 1986","10"
    "A Lathe Thread Cutting Stop","Richard B. Walker","Lathes","HSM Vol. 05 No. 2 Mar-Apr 1986","16"
    "An Accurate Taper Attachment for Under $5.00","J. O. Barbour, Jr.","Lathes","HSM Vol. 05 No. 2 Mar-Apr 1986","20"
    "A Lathe Tool Setup Gage","John P. McDermott, Jr.","Lathes","HSM Vol. 05 No. 2 Mar-Apr 1986","23"
    "A Twin-beam Trammel","Alberto Marx","Shop Accessories","HSM Vol. 05 No. 2 Mar-Apr 1986","27"
    "Sky Charger - Part VIII","Robert A. Washburn","Engines","HSM Vol. 05 No. 2 Mar-Apr 1986","28"
    "Drop Cord Caddy","Arthur Crow","Shop Accessories","HSM Vol. 05 No. 2 Mar-Apr 1986","31"
    "10"" Super Colossal Fly Cutter","Philip Duclos","Mills","HSM Vol. 05 No. 2 Mar-Apr 1986","32"
    "From My Shop to Yours - Part I","Paul J. Holm","Lathes","HSM Vol. 05 No. 2 Mar-Apr 1986","34"
    "Drilling Accurate Holes","Norman H. Bennett","General Machining Knowledge","HSM Vol. 05 No. 2 Mar-Apr 1986","37"
    "A Multiple Tool Post for 6"" Lathes","Carl A. Traub","Lathes","HSM Vol. 05 No. 2 Mar-Apr 1986","38"
    "Some Facts on Dial Indicators","Ron Spokovich","Shop Accessories","HSM Vol. 05 No. 2 Mar-Apr 1986","40"
    "Shrink and Expansion Fits","Daniel Devor","General Machining Knowledge","HSM Vol. 05 No. 2 Mar-Apr 1986","43"
    "The Plastics Forum - Part I","Paul E. Selter, Sr.","Miscellaneous","HSM Vol. 05 No. 2 Mar-Apr 1986","44"
    "Don't Fake a Casting, Make a Casting: Metals for Casting - Part II","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 05 No. 2 Mar-Apr 1986","47"
    "The Apprentice: Keyways - Internal and External","Robert A. Washburn","General Machining Knowledge","HSM Vol. 05 No. 2 Mar-Apr 1986","50"
    "The Micro Machinist: Fixed Steady Rest - Part I","Rudy Kouhoupt","Lathes","HSM Vol. 05 No. 2 Mar-Apr 1986","56"
    "Machine Shop Calculations: Gears - Part IV","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 05 No. 2 Mar-Apr 1986","58"
    "Shop Storage - Part III","Edward G. Hoffman","Miscellaneous","HSM Vol. 05 No. 2 Mar-Apr 1986","64"
    "Product Review: Mecanix L-150 Universal Machine Tool","Raymond D. Niergarth","Shop Machinery","HSM Vol. 05 No. 3 May-Jun 1986","12"
    "Machine Shop Calculations: Gears - Part V","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 05 No. 3 May-Jun 1986","17"
    "Book Review: How to Build Your Own Percussion Rifle or Pistol by Georg Lauber","Reid Coffield","General Machining Knowledge","HSM Vol. 05 No. 3 May-Jun 1986","20"
    "Book Review: How to Build Your Own Wheellock Rifle or Pistol by Georg Lauber","Reid Coffield","General Machining Knowledge","HSM Vol. 05 No. 3 May-Jun 1986","20"
    "How to Build Your Own Flintlock Rifle or Pistol - Georg Lauber","Reid Coffield","General Machining Knowledge","HSM Vol. 05 No. 3 May-Jun 1986","20"
    "Q & A","Raymond D. Niergarth","General Machining Knowledge","HSM Vol. 05 No. 3 May-Jun 1986","20"
    "Q & A","Raymond D. Niergarth","General Machining Knowledge","HSM Vol. 05 No. 3 May-Jun 1986","20"
    "Threading Dial Indicator for the Lathe","W. Pete Peterka","Lathes","HSM Vol. 05 No. 3 May-Jun 1986","22"
    "The Installation of a ShopTronics Milling Machine DRO","Robert A. Washburn","Mills","HSM Vol. 05 No. 3 May-Jun 1986","24"
    "40-Ton Hydraulic Arbor Press - Part I","Bruce Jones","Shop Machinery","HSM Vol. 05 No. 3 May-Jun 1986","28"
    "Lathe Chuck Backstop","Theodore R. McDowell","Lathes","HSM Vol. 05 No. 3 May-Jun 1986","33"
    "Sky Charger - Part IX","Robert A. Washburn","Engines","HSM Vol. 05 No. 3 May-Jun 1986","34"
    "From My Shop to Yours - Part II","Paul J. Holm","Lathes","HSM Vol. 05 No. 3 May-Jun 1986","38"
    "A Slow Speed Drill Press Attachment","Robert Coleman","Shop Machinery","HSM Vol. 05 No. 3 May-Jun 1986","42"
    "A Rotary Welding Table","Jim Fleming","Welding/Foundry/Forging","HSM Vol. 05 No. 3 May-Jun 1986","45"
    "Don't Fake a Casting, Make a Casting: Metals for Casting - Part III","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 05 No. 3 May-Jun 1986","46"
    "From the Scrapbox: Improving Your Vertical Mill","Frank A. McLean","Mills","HSM Vol. 05 No. 3 May-Jun 1986","48"
    "A Cutter Bit Grinding Block","W. Pete Peterka","Shop Accessories","HSM Vol. 05 No. 3 May-Jun 1986","54"
    "The Micro Machinist: Fixed Steady Rest - Part II","Rudy Kouhoupt","Lathes","HSM Vol. 05 No. 3 May-Jun 1986","56"
    "Shop Storage - Part IV","Edward G. Hoffman","Miscellaneous","HSM Vol. 05 No. 3 May-Jun 1986","64"
    "Book Review: Gunsmith Kinks","Guy Lautard","Gunsmithing","HSM Vol. 05 No. 4 Jul-Aug 1986","13"
    "Radius Turning Tool","Will Martin","Lathes","HSM Vol. 05 No. 4 Jul-Aug 1986","16"
    "Spindle Nose Collet Chuck","William B. Park","Lathes","HSM Vol. 05 No. 4 Jul-Aug 1986","20"
    "Scroll Saw","R. S. Hedin","Shop Machinery","HSM Vol. 05 No. 4 Jul-Aug 1986","23"
    "Facing Thin Pieces","Alberto Marx","Lathes","HSM Vol. 05 No. 4 Jul-Aug 1986","30"
    "Sky Charger - Part X","Robert A. Washburn","Engines","HSM Vol. 05 No. 4 Jul-Aug 1986","33"
    "40-Ton Hydraulic Arbor Press - Part II","Bruce Jones","Shop Machinery","HSM Vol. 05 No. 4 Jul-Aug 1986","38"
    "The Plastics Forum - Part II","Paul E. Selter, Sr.","Miscellaneous","HSM Vol. 05 No. 4 Jul-Aug 1986","42"
    "Indexing on Small Lathes","William T. Roubal, Ph.D.","Lathes","HSM Vol. 05 No. 4 Jul-Aug 1986","46"
    "Don't Fake a Casting, Make a Casting: Metals for Casting - Part IV","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 05 No. 4 Jul-Aug 1986","48"
    "From the Scrapbox: A Baseplate for a Dividing Head","Frank A. McLean","Shop Machinery","HSM Vol. 05 No. 4 Jul-Aug 1986","50"
    "The Micro Machinist: Small Keyways and Keyseats - Part I","Rudy Kouhoupt","Mills","HSM Vol. 05 No. 4 Jul-Aug 1986","52"
    "Study References for Novice Machinists","R. W. Evans","Hobby Community","HSM Vol. 05 No. 4 Jul-Aug 1986","56"
    "Storage of Flammable Liquids - Part I","Edward G. Hoffman","Miscellaneous","HSM Vol. 05 No. 4 Jul-Aug 1986","64"
    "Product Review: An Owner's Review of the Jet JVM-840","Stephen G. Wellcome","Hobby Community","HSM Vol. 05 No. 5 Sep-Oct 1986","12"
    "Q & A","Frank A. McLean","General Machining Knowledge","HSM Vol. 05 No. 5 Sep-Oct 1986","15"
    "Multi-Purpose Block","D. E. Johnson","Shop Accessories","HSM Vol. 05 No. 5 Sep-Oct 1986","21"
    "Vernier Height Gage","Lewis Jenkins","Shop Accessories","HSM Vol. 05 No. 5 Sep-Oct 1986","25"
    "Wiggler Bar and Test Bar","Edward G. Hoffman","Shop Accessories","HSM Vol. 05 No. 5 Sep-Oct 1986","26"
    "Extend the Capacity of Your Milling Machine","Gary F. Reisdorf","Mills","HSM Vol. 05 No. 5 Sep-Oct 1986","28"
    "Brass is Beautiful","Alberto Marx","General Machining Knowledge","HSM Vol. 05 No. 5 Sep-Oct 1986","31"
    "Using Unimat SL Chucks and Collets","William T. Roubal, Ph.D.","Lathes","HSM Vol. 05 No. 5 Sep-Oct 1986","34"
    "Sky Charger - Part XI","Robert A. Washburn","Engines","HSM Vol. 05 No. 5 Sep-Oct 1986","36"
    "Table Covers and Tool Trays","Ed Kinderman","Lathes","HSM Vol. 05 No. 5 Sep-Oct 1986","41"
    "Broaching With Your Lathe","Dan Jenkins","Lathes","HSM Vol. 05 No. 5 Sep-Oct 1986","42"
    "Hobby Businesses","Mark E. Battersby","Hobby Community","HSM Vol. 05 No. 5 Sep-Oct 1986","44"
    "Machine Shop Calculations: Gears - Part VII","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 05 No. 5 Sep-Oct 1986","46"
    "Book Review: How to Build a Radial Arm Flame-cutter","Joe Rice","Hobby Community","HSM Vol. 05 No. 5 Sep-Oct 1986","48"
    "Book Review: Student's Shop Reference Handbook","Joe Rice","Hobby Community","HSM Vol. 05 No. 5 Sep-Oct 1986","48"
    "Don't Fake a Casting, Make a Casting: Metals for Casting - Part V","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 05 No. 5 Sep-Oct 1986","50"
    "The Apprentice: The Dividing Head Revisited","Robert A. Washburn","Shop Machinery","HSM Vol. 05 No. 5 Sep-Oct 1986","52"
    "From the Scrapbox: How to Replace the Damaged Thread on a Drawbar","Frank A. McLean","Lathes","HSM Vol. 05 No. 5 Sep-Oct 1986","56"
    "The Micro Machinist: Small Keyways and Keyseats - Part II","Rudy Kouhoupt","Mills","HSM Vol. 05 No. 5 Sep-Oct 1986","57"
    "Storage of Flammable Liquids - Part II","Edward G. Hoffman","Miscellaneous","HSM Vol. 05 No. 5 Sep-Oct 1986","64"
    "Eliminate Headache Potential","Joseph P. Howard","Lathes","HSM Vol. 05 No. 6 Nov-Dec 1986","14"
    "Q & A","Frank A. McLean","General Machining Knowledge","HSM Vol. 05 No. 6 Nov-Dec 1986","16"
    "Q & A","Frank A. McLean","General Machining Knowledge","HSM Vol. 05 No. 6 Nov-Dec 1986","17"
    "Machine Shop Calculations: Gears - Part VIII","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 05 No. 6 Nov-Dec 1986","18"
    "Odds 'n Ends Hit 'n Miss Engine - Part I","Philip Duclos","Engines","HSM Vol. 05 No. 6 Nov-Dec 1986","22"
    "Some Electric Motor Troubles","G. Alan Turner","Miscellaneous","HSM Vol. 05 No. 6 Nov-Dec 1986","29"
    "Tom Senior and the Atlas Special - Part I","Harold Mason","Shop Machinery","HSM Vol. 05 No. 6 Nov-Dec 1986","32"
    "The Plastics Forum - Part III","Paul E. Selter, Sr.","Miscellaneous","HSM Vol. 05 No. 6 Nov-Dec 1986","36"
    "Quick Threading and Tapping in the Lathe","Mike Hoff","Lathes","HSM Vol. 05 No. 6 Nov-Dec 1986","38"
    "Tooling for Unimat-type Drilling/Milling Machines","Theodore M. Clarke","Mills","HSM Vol. 05 No. 6 Nov-Dec 1986","43"
    "Book Review: The Amateur's Lathe by L. H. Sparey","Reid Coffield","General Machining Knowledge","HSM Vol. 05 No. 6 Nov-Dec 1986","44"
    "Book Review: The Machinist's Bedside Reader","Reid Coffield","Hobby Community","HSM Vol. 05 No. 6 Nov-Dec 1986","44"
    "The Micro Machinist: Stocking Stuffers","Rudy Kouhoupt","Projects","HSM Vol. 05 No. 6 Nov-Dec 1986","45"
    "Don't Fake a Casting, Make a Casting: Metals for Casting - Part VI","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 05 No. 6 Nov-Dec 1986","48"
    "Mail Order Customer Rights","Joe Rice","Hobby Community","HSM Vol. 05 No. 6 Nov-Dec 1986","51"
    "From the Scapbox: Installing a Power Feed Unit on a Vertical Mill","Frank A. McLean","Mills","HSM Vol. 05 No. 6 Nov-Dec 1986","52"
    "The Apprentice: Usage for Gearing","Robert A. Washburn","General Machining Knowledge","HSM Vol. 05 No. 6 Nov-Dec 1986","55"
    "Using Toxic Materials","Edward G. Hoffman","Miscellaneous","HSM Vol. 05 No. 6 Nov-Dec 1986","64"
    "Product Review: Omni-Post Quick Change Toolpost","Edward G. Hoffman","Hobby Community","HSM Vol. 06 No. 1 Jan-Feb 1987","14"
    "Book Review: The Basics of Firearms Engraving","Reid Coffield","Hobby Community","HSM Vol. 06 No. 1 Jan-Feb 1987","22"
    "Q & A","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 06 No. 1 Jan-Feb 1987","23"
    "Q & A","Rudy Kouhoupt","General Machining Knowledge","HSM Vol. 06 No. 1 Jan-Feb 1987","23"
    "Q & A","Harry Bloom","General Machining Knowledge","HSM Vol. 06 No. 1 Jan-Feb 1987","24"
    "Machine Shop Calculations: Dimensions & Tolerances - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 06 No. 1 Jan-Feb 1987","26"
    "More Reconditioning a Lathe","Harry Bloom","Lathes","HSM Vol. 06 No. 1 Jan-Feb 1987","30"
    "Freehand Twist Drill Sharpening","Joseph A. Drewniak","Miscellaneous","HSM Vol. 06 No. 1 Jan-Feb 1987","34"
    "Tom Senior and the Atlas Special - Part II","Harold Mason","Shop Machinery","HSM Vol. 06 No. 1 Jan-Feb 1987","40"
    "Odds 'n Ends Hit 'n Miss Engine - Part II","Philip Duclos","Engines","HSM Vol. 06 No. 1 Jan-Feb 1987","43"
    "The Plastics Forum - Part IV","Paul E. Selter, Sr.","Miscellaneous","HSM Vol. 06 No. 1 Jan-Feb 1987","48"
    "The Apprentice: A Mini-course in Orthographic Drawing Techniques - Part I","Robert A. Washburn","General Machining Knowledge","HSM Vol. 06 No. 1 Jan-Feb 1987","50"
    "The Micro Machinist: Time for an Overhaul - Part I","Rudy Kouhoupt","Lathes","HSM Vol. 06 No. 1 Jan-Feb 1987","54"
    "Don't Fake a Casting - Make a Casting: Making a Mold Using a Matchplate","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 06 No. 1 Jan-Feb 1987","56"
    "Personal Safety Equipment","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 06 No. 1 Jan-Feb 1987","64"
    "Product Review: Mitutoyo Tool Kit","Edward G. Hoffman","Hobby Community","HSM Vol. 06 No. 2 Mar-Apr 1987","12"
    "Book Review: The Springfield M1903 Rifles","Guy Lautard","Hobby Community","HSM Vol. 06 No. 2 Mar-Apr 1987","13"
    "Machine Shop Calculations: Dimensions & Tolerances - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 06 No. 2 Mar-Apr 1987","17"
    "Q & A","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 06 No. 2 Mar-Apr 1987","20"
    "Machining Aids for a Machine Lathe","James R. Lewis","Lathes","HSM Vol. 06 No. 2 Mar-Apr 1987","22"
    "A Small Demagnetizer/Magnetizer","Franklin A. Longley","Miscellaneous","HSM Vol. 06 No. 2 Mar-Apr 1987","25"
    "A Spindle Work Stop","Alberto Marx","Lathes","HSM Vol. 06 No. 2 Mar-Apr 1987","26"
    "Collets for Your Lathe","Gary F. Reisdorf","Lathes","HSM Vol. 06 No. 2 Mar-Apr 1987","28"
    "A Puzzle","Bill Reichart","Miscellaneous","HSM Vol. 06 No. 2 Mar-Apr 1987","32"
    "The Plastics Forum - Part V","Paul E. Selter, Sr.","Miscellaneous","HSM Vol. 06 No. 2 Mar-Apr 1987","34"
    "Odds 'n Ends Hit 'n Miss Engine - Part III","Philip Duclos","Engines","HSM Vol. 06 No. 2 Mar-Apr 1987","36"
    "Cutter Bit Grinding Block","D. E. Johnson","Shop Accessories","HSM Vol. 06 No. 2 Mar-Apr 1987","44"
    "The Apprentice: A Mini-course in Orthographic Drawing Techniques - Part II","Robert A. Washburn","General Machining Knowledge","HSM Vol. 06 No. 2 Mar-Apr 1987","47"
    "The Micro Machinist: Time for an Overhaul - Part II","Rudy Kouhoupt","Lathes","HSM Vol. 06 No. 2 Mar-Apr 1987","53"
    "From the Scrapbox: Machining Thin Plates on a Vertical Mill","Frank A. McLean","Mills","HSM Vol. 06 No. 2 Mar-Apr 1987","56"
    "Personal Safety Habits","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 06 No. 2 Mar-Apr 1987","64"
    "Machine Shop Calculations: Dimensions & Tolerances - Part III","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 06 No. 3 May-Jun 1987","16"
    "Q & A","Paul E. Selter, Sr.","General Machining Knowledge","HSM Vol. 06 No. 3 May-Jun 1987","19"
    "Helical Springs - Part I","Kozo Hiraoka","Projects","HSM Vol. 06 No. 3 May-Jun 1987","20"
    "Odds 'n Ends Hit 'n Miss Engine - Part IV","Philip Duclos","Engines","HSM Vol. 06 No. 3 May-Jun 1987","26"
    "Pipeline to Prosperity","Michael Brown","Miscellaneous","HSM Vol. 06 No. 3 May-Jun 1987","32"
    "Watch Repair in the Home Machine Shop","William T. Roubal, Ph.D.","Miscellaneous","HSM Vol. 06 No. 3 May-Jun 1987","37"
    "Shop of the Month","Larry Goddard","Hobby Community","HSM Vol. 06 No. 3 May-Jun 1987","41"
    "The Apprentice: A Mini-course in Orthographic Drawing Techniques - Part III","Robert A. Washburn","General Machining Knowledge","HSM Vol. 06 No. 3 May-Jun 1987","42"
    "Making an Angle Plate in the Lathe","Clifford H. Hancock","Lathes","HSM Vol. 06 No. 3 May-Jun 1987","45"
    "The Micro Machinist: Time for an Overhaul - Part III","Rudy Kouhoupt","Lathes","HSM Vol. 06 No. 3 May-Jun 1987","46"
    "Don't Fake a Casting - Make a Casting: Cuttlebone Casting","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 06 No. 3 May-Jun 1987","48"
    "Machine Guards","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 06 No. 3 May-Jun 1987","64"
    "Product Review: Optical Locator","Joe Rice","Hobby Community","HSM Vol. 06 No. 4 Jul-Aug 1987","11"
    "Machine Shop Calculations: Dimensions & Tolerances - Part IV","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 06 No. 4 Jul-Aug 1987","18"
    "A Machinist's Desk Lamp - Part I","Guy Lautard","Shop Accessories","HSM Vol. 06 No. 4 Jul-Aug 1987","22"
    "Helical Springs - Part II","Kozo Hiraoka","Projects","HSM Vol. 06 No. 4 Jul-Aug 1987","30"
    "Odds 'n Ends Hit 'n Miss Engine - Part V","Philip Duclos","Engines","HSM Vol. 06 No. 4 Jul-Aug 1987","33"
    "Of Auctions and Industrial Sales","Richard B. Walker","Hobby Community","HSM Vol. 06 No. 4 Jul-Aug 1987","36"
    "A Vise for Small Parts","Ed Dubosky","Shop Accessories","HSM Vol. 06 No. 4 Jul-Aug 1987","42"
    "Electric Motors","Robert W. Lamparter","Miscellaneous","HSM Vol. 06 No. 4 Jul-Aug 1987","47"
    "Improved Atlas 6"" Lathe Gear Cover","C. M. Luchessa","Lathes","HSM Vol. 06 No. 4 Jul-Aug 1987","52"
    "The Apprentice: A Mini-course in Orthographic Drawing Techniques - Part IV","Robert A. Washburn","General Machining Knowledge","HSM Vol. 06 No. 4 Jul-Aug 1987","54"
    "From the Scrapbox: Protect Your Mill from Shavings","Frank A. McLean","Mills","HSM Vol. 06 No. 4 Jul-Aug 1987","56"
    "The Micro Machinist: Building a Rotary Table - Part I","Rudy Kouhoupt","Shop Accessories","HSM Vol. 06 No. 4 Jul-Aug 1987","57"
    "Using Chisels and Punches","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 06 No. 4 Jul-Aug 1987","64"
    "Q & A","Harry Bloom","General Machining Knowledge","HSM Vol. 06 No. 5 Sep-Oct 1987","14"
    "Machine Shop Calculations: Dimensions & Tolerances - Part V","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 06 No. 5 Sep-Oct 1987","17"
    ""Floating" End Mill Sharpener - Part I","Philip Duclos","Shop Machinery","HSM Vol. 06 No. 5 Sep-Oct 1987","20"
    "A Power Quill Feed Attachment","P. Dworzan","Mills","HSM Vol. 06 No. 5 Sep-Oct 1987","25"
    "The Extremes of Space - Part I","Bill Davidson","Miscellaneous","HSM Vol. 06 No. 5 Sep-Oct 1987","28"
    "Centering Guide","John Opfer, Jr.","Lathes","HSM Vol. 06 No. 5 Sep-Oct 1987","32"
    "A Machinist's Desk Lamp - Part II","Guy Lautard","Shop Accessories","HSM Vol. 06 No. 5 Sep-Oct 1987","34"
    "Blueing Steel","Guy Lautard","General Machining Knowledge","HSM Vol. 06 No. 5 Sep-Oct 1987","41"
    "Don't Fake a Casting - Make a Casting: Investment Casting - Part I","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 06 No. 5 Sep-Oct 1987","44"
    "From the Scrapbox: Lighting Your Vertical Mill","Frank A. McLean","Shop Accessories","HSM Vol. 06 No. 5 Sep-Oct 1987","49"
    "The Apprentice: Building a Cabinet for Your Sandblaster","Robert A. Washburn","Projects","HSM Vol. 06 No. 5 Sep-Oct 1987","50"
    "The Art of Soldering","Donald Hunt","Welding/Foundry/Forging","HSM Vol. 06 No. 5 Sep-Oct 1987","56"
    "The Micro Machinist: Building a Rotary Table - Part II","Rudy Kouhoupt","Shop Accessories","HSM Vol. 06 No. 5 Sep-Oct 1987","58"
    "Using Wrenches and Screwdrivers","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 06 No. 5 Sep-Oct 1987","64"
    "Q & A","Tim Smith","General Machining Knowledge","HSM Vol. 06 No. 6 Nov-Dec 1987","17"
    "Machine Shop Calculations: Dimensions & Tolerances - Part VI","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 06 No. 6 Nov-Dec 1987","19"
    "A Bit of Inspiration - A View Camera","D. W. Holen","Projects","HSM Vol. 06 No. 6 Nov-Dec 1987","22"
    "How to Deal with Cranks and Eccentrics","Dan Jenkins","General Machining Knowledge","HSM Vol. 06 No. 6 Nov-Dec 1987","24"
    "Patterns and Molding Procedure - Part I","Dave Gingery","Welding/Foundry/Forging","HSM Vol. 06 No. 6 Nov-Dec 1987","30"
    ""Floating" End Mill Sharpener - Part II","Philip Duclos","Shop Machinery","HSM Vol. 06 No. 6 Nov-Dec 1987","38"
    "The Extremes of Space - Part II","Bill Davidson","Miscellaneous","HSM Vol. 06 No. 6 Nov-Dec 1987","46"
    "Measurement for Taper Turning","E. T. Feller","Lathes","HSM Vol. 06 No. 6 Nov-Dec 1987","50"
    "Sharpening Small Drills","Trevor Robinson","Miscellaneous","HSM Vol. 06 No. 6 Nov-Dec 1987","51"
    "Simple Centering Gage","Robert Norman","Shop Accessories","HSM Vol. 06 No. 6 Nov-Dec 1987","52"
    "Don't Fake a Casting - Make a Casting: Investment Casting - Part II","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 06 No. 6 Nov-Dec 1987","53"
    "The Apprentice: The Surface Grinder - Part I","Robert A. Washburn","Shop Machinery","HSM Vol. 06 No. 6 Nov-Dec 1987","56"
    "Cutting a Thin Gear","O. J. Dewberry","Miscellaneous","HSM Vol. 06 No. 6 Nov-Dec 1987","58"
    "From the Scrapbox: Repairing and Old Lathe","Frank A. McLean","Lathes","HSM Vol. 06 No. 6 Nov-Dec 1987","59"
    "The Micro Machinist: Building a Rotary Table - Part III","Rudy Kouhoupt","Machining Accessories","HSM Vol. 06 No. 6 Nov-Dec 1987","62"
    "Using Hand Hacksaws","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 06 No. 6 Nov-Dec 1987","68"
    "Product Review: Fu San 8"" Metal Lathe","Edward H. Scott","Hobby Community","HSM Vol. 07 No. 1 Jan-Feb 1988","14"
    "A Bit of Inspiration: Sculpting with Plastics","Norman J. Mercer","Miscellaneous","HSM Vol. 07 No. 1 Jan-Feb 1988","16"
    "Machine Shop Calculations: Dimensions & Tolerances - Part VII","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 07 No. 1 Jan-Feb 1988","17"
    "Metric-Decimal Equivalents and Tap Drill Sizes","William J. Alles, Jr.","General Machining Knowledge","HSM Vol. 07 No. 1 Jan-Feb 1988","19"
    "A Sensitive Level","Howard Kelly","Shop Accessories","HSM Vol. 07 No. 1 Jan-Feb 1988","20"
    "Protect Your Shop from Voltage Spikes","Lou Hinshaw","Miscellaneous","HSM Vol. 07 No. 1 Jan-Feb 1988","28"
    "Patterns and Molding Procedure - Part II","Dave Gingery","Welding/Foundry/Forging","HSM Vol. 07 No. 1 Jan-Feb 1988","30"
    "Grinding and Lapping With Diamond","James Hesse","Miscellaneous","HSM Vol. 07 No. 1 Jan-Feb 1988","36"
    "A Plastic Dip Pot","Charlie Dondro","Shop Accessories","HSM Vol. 07 No. 1 Jan-Feb 1988","40"
    "Don't Fake a Casting - Make a Casting: Investment Casting - Part III","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 07 No. 1 Jan-Feb 1988","44"
    "From the Scrapbox: Homemade Arbors","Frank A. McLean","Mills","HSM Vol. 07 No. 1 Jan-Feb 1988","48"
    "The Apprentice: The Surface Grinder - Part II","Robert A. Washburn","Shop Machinery","HSM Vol. 07 No. 1 Jan-Feb 1988","51"
    "The Micro Machinist: Fly Cutter and Angle Plate","Rudy Kouhoupt","Shop Accessories","HSM Vol. 07 No. 1 Jan-Feb 1988","54"
    "Using Hand Files and Squares","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 07 No. 1 Jan-Feb 1988","64"
    "Machine Shop Calculations: Dimensions & Tolerances - Part VIII","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 07 No. 2 Mar-Apr 1988","16"
    "A Camera-Tripod Attachment","Alberto Marx","Projects","HSM Vol. 07 No. 2 Mar-Apr 1988","20"
    "A Small Melt Furnace","Bill Roy","Welding/Foundry/Forging","HSM Vol. 07 No. 2 Mar-Apr 1988","22"
    "Multi-Stand","Jeff Bertrand","Shop Accessories","HSM Vol. 07 No. 2 Mar-Apr 1988","25"
    "A Mill-Drill Stand","Lawrence L. Dullum","Mills","HSM Vol. 07 No. 2 Mar-Apr 1988","28"
    "The Minton Milling Machine","E. T. Feller","Mills","HSM Vol. 07 No. 2 Mar-Apr 1988","32"
    "Handy Deburring Tool","Bruce Jones","Shop Accessories","HSM Vol. 07 No. 2 Mar-Apr 1988","34"
    "Reducing Tap Breakage","D. E. Johnson","General Machining Knowledge","HSM Vol. 07 No. 2 Mar-Apr 1988","37"
    "Patterns and Molding Procedure - Part III","Dave Gingery","Welding/Foundry/Forging","HSM Vol. 07 No. 2 Mar-Apr 1988","40"
    "Don't Fake a Casting - Make a Casting: Investment Casting - Part IV","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 07 No. 2 Mar-Apr 1988","42"
    "From the Scrapbox: Comments on My Shop","Frank A. McLean","Miscellaneous","HSM Vol. 07 No. 2 Mar-Apr 1988","46"
    "The Apprentice: The Surface Grinder - Part III","Robert A. Washburn","Shop Machinery","HSM Vol. 07 No. 2 Mar-Apr 1988","48"
    "The Micro Machinist: A Micrometer Faceplate Attachment - Part I","Rudy Kouhoupt","Lathes","HSM Vol. 07 No. 2 Mar-Apr 1988","50"
    "One-evening Projects","Walter C. Runge","Projects","HSM Vol. 07 No. 2 Mar-Apr 1988","54"
    "Using Layout Tools","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 07 No. 2 Mar-Apr 1988","64"
    "A Bit of Inspiration: Miniature Machine Shop","Sid Procknow","Miscellaneous","HSM Vol. 07 No. 3 May-Jun 1988","14"
    "Machine Shop Calculations: Dimensions & Tolerances - Part IX","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 07 No. 3 May-Jun 1988","16"
    "Economical Large-Hole Drilling","Richard B. Walker","Mills","HSM Vol. 07 No. 3 May-Jun 1988","18"
    "Model Piston Rings","Philip Duclos","Engines","HSM Vol. 07 No. 3 May-Jun 1988","20"
    "A New Cutoff Tool","F. Burrows Esty","Lathes","HSM Vol. 07 No. 3 May-Jun 1988","23"
    "Tool Plate","Stephen Vitkovits, Jr.","Shop Accessories","HSM Vol. 07 No. 3 May-Jun 1988","25"
    "Two-Sphere Gage","Theodore M. Clarke","Shop Accessories","HSM Vol. 07 No. 3 May-Jun 1988","26"
    "Two Accessories for the Atlas 12"" Lathe","John F. Ernest","Lathes","HSM Vol. 07 No. 3 May-Jun 1988","28"
    "More Inspiration - Part II","John W. Oder","Engines","HSM Vol. 07 No. 3 May-Jun 1988","31"
    "A Feed Lever for a 10-K","Norman H. Bennett","Lathes","HSM Vol. 07 No. 3 May-Jun 1988","34"
    "Compound Rest Lock","Alberto Marx","Lathes","HSM Vol. 07 No. 3 May-Jun 1988","35"
    "Patterns and Molding Procedure - Part IV","Dave Gingery","Welding/Foundry/Forging","HSM Vol. 07 No. 3 May-Jun 1988","36"
    "The Micro Machinist: A Micrometer Faceplate Attachment - Part II","Rudy Kouhoupt","Lathes","HSM Vol. 07 No. 3 May-Jun 1988","39"
    "The $5.00 Taper Jig Revisited","John Olson","General Machining Knowledge","HSM Vol. 07 No. 3 May-Jun 1988","42"
    "From the Scrapbox: A New Rotary Table","Frank A. McLean","Shop Machinery","HSM Vol. 07 No. 3 May-Jun 1988","43"
    "Don't Fake a Casting - Make a Casting: Investment Casting - Part V","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 07 No. 3 May-Jun 1988","46"
    "The Apprentice: The Surface Grinder - Part IV","Robert A. Washburn","Shop Machinery","HSM Vol. 07 No. 3 May-Jun 1988","52"
    "Using Hammers","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 07 No. 3 May-Jun 1988","64"
    "Getting With the Program","Thomas F. Howard","Computers","HSM Vol. 07 No. 4 Jul-Aug 1988","16"
    "Machine Shop Calculations: Dimensions & Tolerances - Part X","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 07 No. 4 Jul-Aug 1988","17"
    "Whatzit Engine - Part I","Philip Duclos","Engines","HSM Vol. 07 No. 4 Jul-Aug 1988","20"
    "Don't Fake a Casting - Make a Casting: Making Identical Patterns for Multiple Lost Wax Castings - Part I","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 07 No. 4 Jul-Aug 1988","27"
    "More Inspiration - Part III","John W. Oder","Engines","HSM Vol. 07 No. 4 Jul-Aug 1988","30"
    "The Micro Machinist: Lever Operated Tailstock - Part I","Rudy Kouhoupt","Lathes","HSM Vol. 07 No. 4 Jul-Aug 1988","34"
    "Diamond Tool Efficiency","Frederick Oginz","Miscellaneous","HSM Vol. 07 No. 4 Jul-Aug 1988","37"
    "Patterns and Molding Procedure - Part V","Dave Gingery","Welding/Foundry/Forging","HSM Vol. 07 No. 4 Jul-Aug 1988","38"
    "Osborne's Four Steps to Center","L. C. Melton","General Machining Knowledge","HSM Vol. 07 No. 4 Jul-Aug 1988","42"
    "The Apprentice: Using a Vertical Band Saw - Part I","Robert A. Washburn","Shop Machinery","HSM Vol. 07 No. 4 Jul-Aug 1988","44"
    "From the Scrapbox: A Micrometer Stop Nut","Frank A. McLean","Mills","HSM Vol. 07 No. 4 Jul-Aug 1988","46"
    "An Assist from the Forge","Clifford H. Hancock","Welding/Foundry/Forging","HSM Vol. 07 No. 4 Jul-Aug 1988","50"
    "Cutting Torch Contour Guide","Carlyle Lynch","Shop Accessories","HSM Vol. 07 No. 4 Jul-Aug 1988","55"
    "Using Taps and Dies - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 07 No. 4 Jul-Aug 1988","64"
    "Product Review: TRIM Computer","Edward G. Hoffman","Hobby Community","HSM Vol. 07 No. 5 Sep-Oct 1988","11"
    "Machine Shop Calculations: Dimensions & Tolerances - Part XI","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 07 No. 5 Sep-Oct 1988","15"
    "Whatzit Engine - Part II","Philip Duclos","Engines","HSM Vol. 07 No. 5 Sep-Oct 1988","18"
    "Lathe Carriage Dial Indicator","Allen Gregg","Lathes","HSM Vol. 07 No. 5 Sep-Oct 1988","28"
    "A Center-mounted Drill","Roger R. McHenry","Lathes","HSM Vol. 07 No. 5 Sep-Oct 1988","30"
    "Buying Used Machine Tools","Robert L. Grady","Miscellaneous","HSM Vol. 07 No. 5 Sep-Oct 1988","32"
    "More Inspiration - Part IV","John W. Oder","Engines","HSM Vol. 07 No. 5 Sep-Oct 1988","35"
    "Patterns and Molding Procedure - Part VI","Dave Gingery","Welding/Foundry/Forging","HSM Vol. 07 No. 5 Sep-Oct 1988","37"
    "A Special Breed","J. O. Barbour, Jr.","Hobby Community","HSM Vol. 07 No. 5 Sep-Oct 1988","40"
    "The Micro Machinist: Lever Operated Tailstock - Part II","Rudy Kouhoupt","Lathes","HSM Vol. 07 No. 5 Sep-Oct 1988","42"
    "The Apprentice: Using a Vertical Band Saw - Part II","Robert A. Washburn","Shop Machinery","HSM Vol. 07 No. 5 Sep-Oct 1988","46"
    "Gear Driven Shapers","Gary F. Reisdorf","Shop Machinery","HSM Vol. 07 No. 5 Sep-Oct 1988","48"
    "Don't Fake a Casting - Make a Casting: Making Identical Patterns for Multiple Lost Wax Castings - Part II","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 07 No. 5 Sep-Oct 1988","49"
    "From the Scrapbox: Drilling with Accuracy","Frank A. McLean","Shop Machinery","HSM Vol. 07 No. 5 Sep-Oct 1988","54"
    "Shop Gadget Clears the Air","Arthur Crow","Shop Accessories","HSM Vol. 07 No. 5 Sep-Oct 1988","57"
    "Using Taps and Dies - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 07 No. 5 Sep-Oct 1988","64"
    "Machine Shop Calculations: Dimensions & Tolerances - Part XII","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 07 No. 6 Nov-Dec 1988","18"
    "Model Maker's Dividing Head - Part I","Philip Duclos","Shop Accessories","HSM Vol. 07 No. 6 Nov-Dec 1988","20"
    "Converting a Lathe to Cut Metric Threads","W. A. Lincoln","Lathes","HSM Vol. 07 No. 6 Nov-Dec 1988","30"
    "Small Hole Saws","Robert S. Hedin","Shop Accessories","HSM Vol. 07 No. 6 Nov-Dec 1988","36"
    "More Inspiration - Part V","John W. Oder","Engines","HSM Vol. 07 No. 6 Nov-Dec 1988","38"
    "Drilling Steam Passages and Tangents","Kenneth R. Haslam","General Machining Knowledge","HSM Vol. 07 No. 6 Nov-Dec 1988","40"
    "The Apprentice - Using a Vertical Band Saw - Part III","Robert A. Washburn","Machine Tools","HSM Vol. 07 No. 6 Nov-Dec 1988","43"
    "The Apprentice: Using a Vertical Band Saw - Part III","Robert A. Washburn","Shop Machinery","HSM Vol. 07 No. 6 Nov-Dec 1988","43"
    "From the Scrapbox: Shortcuts to Making an Arbor","Frank A. McLean","Shop Accessories","HSM Vol. 07 No. 6 Nov-Dec 1988","46"
    "The Micro Machinist: Tooling for a Vertical Mill - Part I","Rudy Kouhoupt","Mills","HSM Vol. 07 No. 6 Nov-Dec 1988","48"
    "Don't Fake a Casting - Make a Casting: Making Identical Patterns for Multiple Lost Wax Castings - Part III","James R. Lewis","Welding/Foundry/Forging","HSM Vol. 07 No. 6 Nov-Dec 1988","52"
    "Century-Old Lathe Back at Work","Carl Holkeboer","Lathes","HSM Vol. 07 No. 6 Nov-Dec 1988","56"
    "Common Hardware - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 07 No. 6 Nov-Dec 1988","64"
    "Product Review: Royal Clamping System","Edward G. Hoffman","Hobby Community","HSM Vol. 08 No. 1 Jan-Feb 1989","14"
    "Machine Shop Calculations: Dimensions & Tolerances - Part XIII","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 08 No. 1 Jan-Feb 1989","16"
    "A Slide Duplicating & Macro Photographic Apparatus","Richard M. Park","Miscellaneous","HSM Vol. 08 No. 1 Jan-Feb 1989","20"
    "Home Shop Metal Melter - Part I","John F. Pilznienski","Welding/Foundry/Forging","HSM Vol. 08 No. 1 Jan-Feb 1989","24"
    "Model Maker's Dividing Head - Part II","Philip Duclos","Shop Accessories","HSM Vol. 08 No. 1 Jan-Feb 1989","30"
    "$100 Digital Readout","Dick Hanley","Shop Accessories","HSM Vol. 08 No. 1 Jan-Feb 1989","39"
    "More Inspiration - Part VI","John W. Oder","Engines","HSM Vol. 08 No. 1 Jan-Feb 1989","42"
    "The Mirror-faced Hammer","Steve Acker","Miscellaneous","HSM Vol. 08 No. 1 Jan-Feb 1989","44"
    "Carriage Multi-stop","Ed Dubosky","Lathes","HSM Vol. 08 No. 1 Jan-Feb 1989","46"
    "The Micro Machinist: Tooling for a Vertical Mill - Part II","Rudy Kouhoupt","Mills","HSM Vol. 08 No. 1 Jan-Feb 1989","50"
    "Single Point Cutting","Theodore M. Clarke","Lathes","HSM Vol. 08 No. 1 Jan-Feb 1989","53"
    "From the Scrapbox: Drilling Center Holes Accurately","Frank A. McLean","General Machining Knowledge","HSM Vol. 08 No. 1 Jan-Feb 1989","56"
    "Safety Tips: Common Hardware - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 08 No. 1 Jan-Feb 1989","64"
    "Product Review: Mitee-Bite Clamping System","Edward G. Hoffman","Hobby Community","HSM Vol. 08 No. 2 Mar-Apr 1989","16"
    "Machine Shop Calculations: Dimensions & Tolerances - Part XIV","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 08 No. 2 Mar-Apr 1989","18"
    "Sentinel","Duane Dehnicke","Projects","HSM Vol. 08 No. 2 Mar-Apr 1989","20"
    "From Steam Arm to Elgamill","Harold Mason","Miscellaneous","HSM Vol. 08 No. 2 Mar-Apr 1989","22"
    "Building the Panther Pup: Part I - Introduction and Materials","J. W. (Bill) Reichart","Engines","HSM Vol. 08 No. 2 Mar-Apr 1989","30"
    "Two Steps to Center","Jon H. Holtham","General Machining Knowledge","HSM Vol. 08 No. 2 Mar-Apr 1989","38"
    "Model Maker's Dividing Head - Part III","Philip Duclos","Shop Accessories","HSM Vol. 08 No. 2 Mar-Apr 1989","41"
    "Home Shop Metal Melter - Part II","John F. Pilznienski","Welding/Foundry/Forging","HSM Vol. 08 No. 2 Mar-Apr 1989","46"
    "Machine Cutting Speeds","Frank Stokes","General Machining Knowledge","HSM Vol. 08 No. 2 Mar-Apr 1989","50"
    "From the Scrapbox: A Grinding Bench","Frank A. McLean","Shop Accessories","HSM Vol. 08 No. 2 Mar-Apr 1989","51"
    "The Apprentice: The Gear Head Engine Lathe - Part I","Robert A. Washburn","Lathes","HSM Vol. 08 No. 2 Mar-Apr 1989","52"
    "The Micro Machinist: Tooling for a Vertical Mill - Part III","Rudy Kouhoupt","Mills","HSM Vol. 08 No. 2 Mar-Apr 1989","54"
    "Safety Tips: Common Hardware - Part III","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 08 No. 2 Mar-Apr 1989","64"
    "Product Review: Loc-Line Modular Hose System","Edward G. Hoffman","Hobby Community","HSM Vol. 08 No. 3 May-Jun 1989","14"
    "Machine Shop Calculations: Dimensions & Tolerances - Part XV","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 08 No. 3 May-Jun 1989","17"
    "Home Shop Metal Melter - Part III","John F. Pilznienski","Welding/Foundry/Forging","HSM Vol. 08 No. 3 May-Jun 1989","27"
    "Building the Panther Pup: Part II - Patterns and Connecting Rod","J. W. (Bill) Reichart","Engines","HSM Vol. 08 No. 3 May-Jun 1989","32"
    "Gear Repair","Gary F. Reisdorf","Miscellaneous","HSM Vol. 08 No. 3 May-Jun 1989","38"
    "Repeatable Quick-Change Tool Holder","Arden A. Schroeder","Lathes","HSM Vol. 08 No. 3 May-Jun 1989","40"
    "The Color of Steel","G. Robert Massey","General Machining Knowledge","HSM Vol. 08 No. 3 May-Jun 1989","43"
    "A Self-Contained Cutter Grinder","John Crunkleton","Shop Machinery","HSM Vol. 08 No. 3 May-Jun 1989","44"
    "The Micro Machinist: A Lathe Milling Adaptation - Part I","Rudy Kouhoupt","Lathes","HSM Vol. 08 No. 3 May-Jun 1989","47"
    "From the Scrapbox: A Depth Gage Attachment","Frank A. McLean","Shop Accessories","HSM Vol. 08 No. 3 May-Jun 1989","50"
    "The Apprentice: The Gear Head Engine Lathe - Part II","Robert A. Washburn","Lathes","HSM Vol. 08 No. 3 May-Jun 1989","52"
    "Using Carbide Turning Tools","F. Burrows Esty","Lathes","HSM Vol. 08 No. 3 May-Jun 1989","57"
    "Safety Tips: Common Hardware - Part IV","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 08 No. 3 May-Jun 1989","64"
    "Q & A","Harry Bloom","General Machining Knowledge","HSM Vol. 08 No. 4 Jul-Aug 1989","13"
    "Machine Shop Calculations: Dimensions & Tolerances - Part XVI","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 08 No. 4 Jul-Aug 1989","14"
    "A Lathe Cabinet/Stand","Ralph T. Walker","Lathes","HSM Vol. 08 No. 4 Jul-Aug 1989","18"
    "Renewing Half Nuts","Harry Bloom","Lathes","HSM Vol. 08 No. 4 Jul-Aug 1989","25"
    "Building the Panther Pup: Part III - Crankshaft, Piston, and Cylinder","J. W. (Bill) Reichart","Engines","HSM Vol. 08 No. 4 Jul-Aug 1989","28"
    "Home Shop Metal Melter - Part IV","John F. Pilznienski","Welding/Foundry/Forging","HSM Vol. 08 No. 4 Jul-Aug 1989","36"
    "A Generic Crane","Dennis K. Wence","Shop Accessories","HSM Vol. 08 No. 4 Jul-Aug 1989","40"
    "Tap Wrenches from Scrap","Steve Acker","Miscellaneous","HSM Vol. 08 No. 4 Jul-Aug 1989","44"
    "The Apprentice: The Gear Head Engine Lathe - Part III","Robert A. Washburn","Lathes","HSM Vol. 08 No. 4 Jul-Aug 1989","47"
    "Restoring a Transit","G. S. Dow","Projects","HSM Vol. 08 No. 4 Jul-Aug 1989","49"
    "Introduction to Jigs and Fixtures","Edward G. Hoffman","Shop Accessories","HSM Vol. 08 No. 4 Jul-Aug 1989","52"
    "From the Scrapbox: A Carbide End Mill","Frank A. McLean","Mills","HSM Vol. 08 No. 4 Jul-Aug 1989","54"
    "The Micro Machinist: A Lathe Milling Adaptation - Part II","Rudy Kouhoupt","Lathes","HSM Vol. 08 No. 4 Jul-Aug 1989","56"
    "Product Review: Westhoff Mighty Mag","Edward G. Hoffman","Hobby Community","HSM Vol. 08 No. 4 Jul-Aug 1989","64"
    "Product Review: The Manupress","Frank A. McLean","General Machining Knowledge","HSM Vol. 08 No. 5 Sep-Oct 1989","17"
    "Product Review: Accu-Finish II Precision Tool Sharpener","Edward G. Hoffman","Hobby Community","HSM Vol. 08 No. 5 Sep-Oct 1989","20"
    "Machine Shop Calculations: Right Triangles - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 08 No. 5 Sep-Oct 1989","22"
    "A Brass Kaleidoscope","Guy Lautard","Projects","HSM Vol. 08 No. 5 Sep-Oct 1989","24"
    "Home Shop Metal Melter - Part V","John F. Pilznienski","Welding/Foundry/Forging","HSM Vol. 08 No. 5 Sep-Oct 1989","27"
    "Building the Panther Pup: Part IV - Rocker Arms, Valves, and Flywheel","J. W. (Bill) Reichart","Engines","HSM Vol. 08 No. 5 Sep-Oct 1989","34"
    "Auxiliary Outboard Motor Bracket","William F. Green","Projects","HSM Vol. 08 No. 5 Sep-Oct 1989","41"
    "Degassing Molten Aluminum","Philip Duclos","Welding/Foundry/Forging","HSM Vol. 08 No. 5 Sep-Oct 1989","44"
    "Boring Bar and Tool Holder for Compact 5","Jack W. Rasnick","Lathes","HSM Vol. 08 No. 5 Sep-Oct 1989","46"
    "Basics of Locating - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 08 No. 5 Sep-Oct 1989","50"
    "The Micro Machinist: A Lathe Milling Adaptation - Part III","Rudy Kouhoupt","Lathes","HSM Vol. 08 No. 5 Sep-Oct 1989","52"
    "Computers in the Shop: Introduction","Roland W. Friestad","Computers","HSM Vol. 08 No. 5 Sep-Oct 1989","56"
    "Product Review: Huron Workholding System","Edward G. Hoffman","Hobby Community","HSM Vol. 08 No. 6 Nov-Dec 1989","16"
    "Machine Shop Calculations: Right Triangles - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 08 No. 6 Nov-Dec 1989","18"
    "Making the Lathe Safer","Jim Jedlicka","Lathes","HSM Vol. 08 No. 6 Nov-Dec 1989","20"
    "Accurate Quill Depth Control for Mill/Drills","John A. Bodmer","Mills","HSM Vol. 08 No. 6 Nov-Dec 1989","24"
    "Bench Block","Steve Acker","Shop Accessories","HSM Vol. 08 No. 6 Nov-Dec 1989","29"
    "Building the Panther Pup: Part V - Cams","J. W. (Bill) Reichart","Engines","HSM Vol. 08 No. 6 Nov-Dec 1989","34"
    "Lathe Cutting Internal Keyways","Richard B. Walker","Lathes","HSM Vol. 08 No. 6 Nov-Dec 1989","40"
    "Computers in the Shop: Basic Principles","Roland W. Friestad","Computers","HSM Vol. 08 No. 6 Nov-Dec 1989","43"
    "The Micro Machinist: Tool Post Boring Bars - Part I","Rudy Kouhoupt","Lathes","HSM Vol. 08 No. 6 Nov-Dec 1989","48"
    "Basics of Locating - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 08 No. 6 Nov-Dec 1989","52"
    "Tooling for the Micro Machinist","James Sprott","Shop Accessories","HSM Vol. 08 No. 6 Nov-Dec 1989","54"
    "Otis Makes an Accurate Final Cut","L. C. Melton","Lathes","HSM Vol. 08 No. 6 Nov-Dec 1989","57"
    "Product Review: Two New Twist Drills","Jim Jedlicka","Miscellaneous","HSM Vol. 09 No. 1 Jan-Feb 1990","15"
    "Product Review: Shop Math Computer","Edward G. Hoffman","Miscellaneous","HSM Vol. 09 No. 1 Jan-Feb 1990","18"
    "Machine Shop Calculations: Right Triangles - Part III","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 09 No. 1 Jan-Feb 1990","20"
    "A Larger Steady Rest","Glenn L. Wilson","Lathes","HSM Vol. 09 No. 1 Jan-Feb 1990","24"
    "Lathe Operations on a Vertical Mill - Part I","Stephen M. Thomas","Mills","HSM Vol. 09 No. 1 Jan-Feb 1990","29"
    "Smallest Hit & Miss Gas Engine?","Philip Duclos","Engines","HSM Vol. 09 No. 1 Jan-Feb 1990","34"
    "Building the Panther Pup: Part VI","J. W. (Bill) Reichart","Engines","HSM Vol. 09 No. 1 Jan-Feb 1990","38"
    "Computers in the Shop: More on Programming Principles","Roland W. Friestad","Computers","HSM Vol. 09 No. 1 Jan-Feb 1990","44"
    "From the Scrapbox: A Toolmaker's Flat Vise","Frank A. McLean","Shop Accessories","HSM Vol. 09 No. 1 Jan-Feb 1990","52"
    "Basics of Locating - Part III","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 09 No. 1 Jan-Feb 1990","54"
    "The Micro Machinist: Boring Bar Cutters and Turning Tools - Part II","Rudy Kouhoupt","Lathes","HSM Vol. 09 No. 1 Jan-Feb 1990","57"
    "Small T-slot Nuts","John D. Williams","Miscellaneous","HSM Vol. 09 No. 1 Jan-Feb 1990","59"
    "Machine Shop Calculations: Shop Measurements - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 09 No. 2 Mar-Apr 1990","17"
    "Six-cycle Oddball Engine - Part I","Philip Duclos","Engines","HSM Vol. 09 No. 2 Mar-Apr 1990","20"
    "Building the Panther Pup: Part VII","J. W. (Bill) Reichart","Engines","HSM Vol. 09 No. 2 Mar-Apr 1990","28"
    "Lathe Operations on a Vertical Mill - Part II","Stephen M. Thomas","Mills","HSM Vol. 09 No. 2 Mar-Apr 1990","33"
    "Tax-deductible Home Shop","Mark E. Battersby","Hobby Community","HSM Vol. 09 No. 2 Mar-Apr 1990","38"
    "From the Scrapbox: A Band Saw Slow Speed Attachment - Part I","Frank A. McLean","Shop Machinery","HSM Vol. 09 No. 2 Mar-Apr 1990","40"
    "Computers in the Shop: Convert Your Mill-drill to CNC - Part I","Roland W. Friestad","Computers","HSM Vol. 09 No. 2 Mar-Apr 1990","46"
    "A Mill/Drill Stand","Gerard Mulholland","Shop Accessories","HSM Vol. 09 No. 2 Mar-Apr 1990","51"
    "Basics of Locating - Part IV","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 09 No. 2 Mar-Apr 1990","52"
    "Surface Grinding on the Drill Press","Ray E. Starnes","Shop Machinery","HSM Vol. 09 No. 2 Mar-Apr 1990","54"
    "Book Review: Advanced Telescope Making Techniques","Guy Lautard","Hobby Community","HSM Vol. 09 No. 3 May-Jun 1990","13"
    "Product Review: Rovi Expanding Mini Collets","Edward G. Hoffman","Miscellaneous","HSM Vol. 09 No. 3 May-Jun 1990","16"
    "Product Review: Snap Jaws","Guy Lautard","Miscellaneous","HSM Vol. 09 No. 3 May-Jun 1990","18"
    "Q & A","Harry Bloom","General Machining Knowledge","HSM Vol. 09 No. 3 May-Jun 1990","19"
    "Machine Shop Calculations: Shop Measurements - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 09 No. 3 May-Jun 1990","20"
    "Topics in Micromachining - Part I","William T. Roubal, Ph.D.","General Machining Knowledge","HSM Vol. 09 No. 3 May-Jun 1990","22"
    "Six-cycle Oddball Engine - Part II","Philip Duclos","Engines","HSM Vol. 09 No. 3 May-Jun 1990","26"
    "Building the Panther Pup: Part VIII","J. W. (Bill) Reichart","Engines","HSM Vol. 09 No. 3 May-Jun 1990","31"
    "Density, Volume, Dimensions = Weight","L. C. Melton","General Machining Knowledge","HSM Vol. 09 No. 3 May-Jun 1990","38"
    "The Micro Machinist: A Grinding Rest for Precise Tools - Part I","Rudy Kouhoupt","Shop Accessories","HSM Vol. 09 No. 3 May-Jun 1990","40"
    "From the Scrapbox: A Band Saw Slow Speed Attachment - Part II","Frank A. McLean","Shop Machinery","HSM Vol. 09 No. 3 May-Jun 1990","43"
    "Computers in the Shop: Convert Your Mill-drill to CNC - Part II","Roland W. Friestad","Computers","HSM Vol. 09 No. 3 May-Jun 1990","50"
    "Basics of Locating - Part V","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 09 No. 3 May-Jun 1990","57"
    "Machine Shop Calculations: Shop Measurements - Part III","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 09 No. 4 Jul-Aug 1990","16"
    "Band Saw Transmission","Richard S. Torgerson","Shop Machinery","HSM Vol. 09 No. 4 Jul-Aug 1990","18"
    "Topics in Micromachining - Part II","William T. Roubal, Ph.D.","General Machining Knowledge","HSM Vol. 09 No. 4 Jul-Aug 1990","23"
    "A Tapping Guide for a Unimat","Leroy J. Nessen","Lathes","HSM Vol. 09 No. 4 Jul-Aug 1990","27"
    "Accessories for a Rotary Table - Part I","J. W. Straight","Shop Accessories","HSM Vol. 09 No. 4 Jul-Aug 1990","28"
    "Soft Vise Jaws","James Madison","Shop Accessories","HSM Vol. 09 No. 4 Jul-Aug 1990","32"
    "Six-cycle Oddball Engine - Part III","Philip Duclos","Engines","HSM Vol. 09 No. 4 Jul-Aug 1990","36"
    "Building the Panther Pup: Part IX","J. W. (Bill) Reichart","Engines","HSM Vol. 09 No. 4 Jul-Aug 1990","42"
    "The Micro Machinist: A Grinding Rest for Precise Tools - Part II","Rudy Kouhoupt","Shop Accessories","HSM Vol. 09 No. 4 Jul-Aug 1990","48"
    "From the Scrapbox: Milling on the Lathe","Frank A. McLean","Lathes","HSM Vol. 09 No. 4 Jul-Aug 1990","51"
    "Computers in the Shop: Convert Your Mill-drill to CNC - Part III","Roland W. Friestad","Computers","HSM Vol. 09 No. 4 Jul-Aug 1990","54"
    "Basics of Locating - Part VI","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 09 No. 4 Jul-Aug 1990","56"
    "Product Review: Carr Lane Spring Locating Pins","Edward G. Hoffman","Miscellaneous","HSM Vol. 09 No. 5 Sep-Oct 1990","16"
    "Book Review: Shop Savvy","Guy Lautard","Miscellaneous","HSM Vol. 09 No. 5 Sep-Oct 1990","17"
    "Machine Shop Calculations: Shop Measurements - Part IV","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 09 No. 5 Sep-Oct 1990","18"
    "An Indexing Device","Ed Dubosky","Shop Accessories","HSM Vol. 09 No. 5 Sep-Oct 1990","20"
    "Accessories for a Rotary Table - Part II","J. W. Straight","Shop Accessories","HSM Vol. 09 No. 5 Sep-Oct 1990","26"
    "Six-cycle Oddball Engine - Part IV","Philip Duclos","Engines","HSM Vol. 09 No. 5 Sep-Oct 1990","30"
    "Topics in Micromachining - Part III","William T. Roubal, Ph.D.","General Machining Knowledge","HSM Vol. 09 No. 5 Sep-Oct 1990","38"
    "The Micro Machinist: Sharpen Your End Mills - Part I","Rudy Kouhoupt","Shop Accessories","HSM Vol. 09 No. 5 Sep-Oct 1990","42"
    "Computers in the Shop: Convert Your Mill-drill to CNC - Part IV","Roland W. Friestad","Computers","HSM Vol. 09 No. 5 Sep-Oct 1990","46"
    "Flame Cutter","Thomas M. Verity","Shop Machinery","HSM Vol. 09 No. 5 Sep-Oct 1990","50"
    "Basics of Locating - Part VII","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 09 No. 5 Sep-Oct 1990","55"
    "Product Review: Greenfield Tap Wrenches","Guy Lautard","Miscellaneous","HSM Vol. 09 No. 6 Nov-Dec 1990","16"
    "Product Review: Whistler Metaligner Dowel Pins","Edward G. Hoffman","Miscellaneous","HSM Vol. 09 No. 6 Nov-Dec 1990","16"
    "Machine Shop Calculations: Shop Measurements - Part V","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 09 No. 6 Nov-Dec 1990","18"
    "On Preventing Bloodshed","Alberto Marx","Miscellaneous","HSM Vol. 09 No. 6 Nov-Dec 1990","21"
    "Engraving Pantograph","Rudy Kouhoupt","Shop Machinery","HSM Vol. 09 No. 6 Nov-Dec 1990","24"
    "Accessories for a Rotary Table - Part III","J. W. Straight","Shop Accessories","HSM Vol. 09 No. 6 Nov-Dec 1990","33"
    "A Pulley Puller","J. Worzala","Projects","HSM Vol. 09 No. 6 Nov-Dec 1990","35"
    "Six-cycle Oddball Engine - Part V","Philip Duclos","Engines","HSM Vol. 09 No. 6 Nov-Dec 1990","38"
    "From the Scrapbox: The Humble Angle Plate","Frank A. McLean","Mills","HSM Vol. 09 No. 6 Nov-Dec 1990","46"
    "Computers in the Shop: Reviewing CAD Systems - Part I","Roland W. Friestad","Computers","HSM Vol. 09 No. 6 Nov-Dec 1990","49"
    "The Micro Machinist: Sharpen Your End Mills - Part II","Rudy Kouhoupt","Shop Accessories","HSM Vol. 09 No. 6 Nov-Dec 1990","52"
    "Basics of Locating - Part VIII","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 09 No. 6 Nov-Dec 1990","56"
    "Product Review: CAD for the Small Shop","Edward G. Hoffman","Miscellaneous","HSM Vol. 10 No. 1 Jan-Feb 1991","12"
    "Machine Shop Calculations: Shop Measurement - Part VI","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 10 No. 1 Jan-Feb 1991","13"
    "Building the Universal Pillartool - Part I","Harold Mason","Projects","HSM Vol. 10 No. 1 Jan-Feb 1991","16"
    "Remounting a Four-jaw Chuck","G. Wadham","Lathes","HSM Vol. 10 No. 1 Jan-Feb 1991","25"
    "Cast Iron Repair","Richard B. Walker","Welding/Foundry/Forging","HSM Vol. 10 No. 1 Jan-Feb 1991","30"
    "Lathe Carriage Stop","Ira J. Neill","Lathes","HSM Vol. 10 No. 1 Jan-Feb 1991","36"
    "A Simple Phase Converter","Steve Acker","Miscellaneous","HSM Vol. 10 No. 1 Jan-Feb 1991","38"
    "Otis Measures Across Backlash","L. C. Melton","General Machining Knowledge","HSM Vol. 10 No. 1 Jan-Feb 1991","41"
    "Electric Discharge Machining (EDM)","Hank Meador","EDM","HSM Vol. 10 No. 1 Jan-Feb 1991","42"
    "Protective Vise Jaws","Jack Ott","Shop Accessories","HSM Vol. 10 No. 1 Jan-Feb 1991","43"
    "Confessions of a Junkyard Motor Junkie","Theodore (Ted) J. Myers","Miscellaneous","HSM Vol. 10 No. 1 Jan-Feb 1991","45"
    "The Micro Machinist: Building a Multi Cutter Face Mill","Rudy Kouhoupt","Shop Accessories","HSM Vol. 10 No. 1 Jan-Feb 1991","50"
    "Computers in the Shop: Reviewing CAD Systems - Part II","Roland W. Friestad","Computers","HSM Vol. 10 No. 1 Jan-Feb 1991","53"
    "From the Scrapbox: Improving a Milling Machine Vise","Frank A. McLean","Mills","HSM Vol. 10 No. 1 Jan-Feb 1991","56"
    "Basics of Clamping - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 10 No. 1 Jan-Feb 1991","58"
    "Product Review: Removable High Performance Disks for Your Computer System","Edward G. Hoffman","Miscellaneous","HSM Vol. 10 No. 2 Mar-Apr 1991","12"
    "Machine Shop Calculations: Surface Finish Designations - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 10 No. 2 Mar-Apr 1991","17"
    "Free Pendulum Clock: Part I - Introduction and Overview","Pierre H. Boucheron","Clocks","HSM Vol. 10 No. 2 Mar-Apr 1991","20"
    "Low Range Ohmmeters for Electric Motors","Theodore (Ted) J. Myers","Miscellaneous","HSM Vol. 10 No. 2 Mar-Apr 1991","24"
    "A Useful Follower Rest","Paul J. Holm","Lathes","HSM Vol. 10 No. 2 Mar-Apr 1991","28"
    "A Fixture Plate for a Lathe or Mill","Ray E. Starnes","Shop Accessories","HSM Vol. 10 No. 2 Mar-Apr 1991","30"
    "Building the Universal Pillartool - Part II","Harold Mason","Projects","HSM Vol. 10 No. 2 Mar-Apr 1991","32"
    "Keeper of the Key","David Richards","Miscellaneous","HSM Vol. 10 No. 2 Mar-Apr 1991","38"
    "Teeth for Rotary Cutting Tools","Robert S. Hedin","Shop Accessories","HSM Vol. 10 No. 2 Mar-Apr 1991","39"
    "Rotary, Dual Cross-slide Drill Press and Milling Machine Table - Part I","John B. Gascoyne","Shop Machinery","HSM Vol. 10 No. 2 Mar-Apr 1991","40"
    "Otis Stops the Chatter","L. C. Melton","General Machining Knowledge","HSM Vol. 10 No. 2 Mar-Apr 1991","45"
    "A Blacksmith Extraordinaire","J. O. Barbour, Jr.","Welding/Foundry/Forging","HSM Vol. 10 No. 2 Mar-Apr 1991","48"
    "From the Scrapbox: A New Centering Gage","Frank A. McLean","Shop Accessories","HSM Vol. 10 No. 2 Mar-Apr 1991","50"
    "Basics of Clamping - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 10 No. 2 Mar-Apr 1991","52"
    "The Micro Machinist: Elevating a Vertical Mill","Rudy Kouhoupt","Mills","HSM Vol. 10 No. 2 Mar-Apr 1991","54"
    "Product Review: Twin Lock Workholding System","Edward G. Hoffman","Miscellaneous","HSM Vol. 10 No. 3 May-Jun 1991","10"
    "Product Review: "In Line" Vise Positioner","Joe Rice","Miscellaneous","HSM Vol. 10 No. 3 May-Jun 1991","12"
    "Machine Shop Calculations: Surface Finish Designations - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 10 No. 3 May-Jun 1991","13"
    "Plastic Injection Molding Machine - Part I","Rodney W. Hanson","Shop Machinery","HSM Vol. 10 No. 3 May-Jun 1991","16"
    "Poshin' Up a Taiwanese Lathe","Guy Lautard","Lathes","HSM Vol. 10 No. 3 May-Jun 1991","23"
    "Poshin' Up a Taiwanese Lathe","Walt Warren","Lathes","HSM Vol. 10 No. 3 May-Jun 1991","23"
    "Building the Universal Pillartool - Part III","Harold Mason","Projects","HSM Vol. 10 No. 3 May-Jun 1991","28"
    "Free Pendulum Clock: Part II - The Bob and Air Losses","Pierre H. Boucheron","Clocks","HSM Vol. 10 No. 3 May-Jun 1991","34"
    "Rotary, Dual Cross-slide Drill Press and Milling Machine Table - Part II","John B. Gascoyne","Shop Machinery","HSM Vol. 10 No. 3 May-Jun 1991","38"
    "From the Scrapbox: A Toolpost Grinder","Frank A. McLean","Lathes","HSM Vol. 10 No. 3 May-Jun 1991","44"
    "The Micro Machinist: Two Useful Milling Accessories","Rudy Kouhoupt","Mills","HSM Vol. 10 No. 3 May-Jun 1991","48"
    "Computers in the Shop: Convert a Milling Machine to CNC Control - Part I","Roland W. Friestad","Computers","HSM Vol. 10 No. 3 May-Jun 1991","51"
    "Screw Clamps","Edward G. Hoffman","Shop Accessories","HSM Vol. 10 No. 3 May-Jun 1991","56"
    "Table Square","James Madison","Shop Accessories","HSM Vol. 10 No. 3 May-Jun 1991","58"
    "Book Review: How to Make a Grasshopper Skeleton Clock","Guy Lautard","Miscellaneous","HSM Vol. 10 No. 4 Jul-Aug 1991","12"
    "Machine Shop Calculations: Surface Finish Designations - Part III","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 10 No. 4 Jul-Aug 1991","16"
    "Drilling Multiple Holes in Line","William S. Wagner","Miscellaneous","HSM Vol. 10 No. 4 Jul-Aug 1991","18"
    "Building the Universal Pillartool - Part IV","Harold Mason","Projects","HSM Vol. 10 No. 4 Jul-Aug 1991","21"
    "Stainless Steel Fundamentals","George W. Genevro","General Machining Knowledge","HSM Vol. 10 No. 4 Jul-Aug 1991","28"
    "Plastic Injection Molding Machine - Part II","Rodney W. Hanson","Shop Machinery","HSM Vol. 10 No. 4 Jul-Aug 1991","32"
    "Rotary, Dual Cross-slide Drill Press and Milling Machine Table - Part III","John B. Gascoyne","Shop Machinery","HSM Vol. 10 No. 4 Jul-Aug 1991","36"
    "Rule Guide for Easier Layout","Edward G. Hoffman","Shop Accessories","HSM Vol. 10 No. 4 Jul-Aug 1991","39"
    "Free Pendulum Clock: Part III - Electronics","Pierre H. Boucheron","Clocks","HSM Vol. 10 No. 4 Jul-Aug 1991","40"
    "A Bit of Inspiration: A Homemade Bench Mill","James S. McKnight","Mills","HSM Vol. 10 No. 4 Jul-Aug 1991","42"
    "Computers in the Shop: Convert a Milling Machine to CNC Control - Part II","Roland W. Friestad","Computers","HSM Vol. 10 No. 4 Jul-Aug 1991","44"
    "The Micro Machinist: Making Tap and Reamer Handles","Rudy Kouhoupt","Projects","HSM Vol. 10 No. 4 Jul-Aug 1991","49"
    "Wedge Clamps","Edward G. Hoffman","Shop Accessories","HSM Vol. 10 No. 4 Jul-Aug 1991","54"
    "From the Scrapbox: Cutting Left-hand Threads","Frank A. McLean","General Machining Knowledge","HSM Vol. 10 No. 4 Jul-Aug 1991","56"
    "Machine Shop Calculations: Geometric Construction - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 10 No. 5 Sep-Oct 1991","17"
    "Topsy-turvy Engine - Part I","Philip Duclos","Engines","HSM Vol. 10 No. 5 Sep-Oct 1991","20"
    "Heat Treating Basics","Steve Acker","General Machining Knowledge","HSM Vol. 10 No. 5 Sep-Oct 1991","28"
    "Building the Universal Pillartool - Part V","Harold Mason","Projects","HSM Vol. 10 No. 5 Sep-Oct 1991","32"
    "Free Pendulum Clock: Part IV - Setup and General Considerations","Pierre H. Boucheron","Clocks","HSM Vol. 10 No. 5 Sep-Oct 1991","40"
    "Plastic Injection Molding Machine - Part III","Rodney W. Hanson","Shop Machinery","HSM Vol. 10 No. 5 Sep-Oct 1991","44"
    "Book/Video Review: Green Sand Casting Techniques","Joe Rice","Miscellaneous","HSM Vol. 10 No. 5 Sep-Oct 1991","47"
    "The Micro Machinist: Two Useful Lathe Dogs","Rudy Kouhoupt","Lathes","HSM Vol. 10 No. 5 Sep-Oct 1991","48"
    "Computers in the Shop: Convert a Milling Machine to CNC Control - Part III","Roland W. Friestad","Computers","HSM Vol. 10 No. 5 Sep-Oct 1991","52"
    "Toggle Clamps","Edward G. Hoffman","Shop Accessories","HSM Vol. 10 No. 5 Sep-Oct 1991","55"
    "Machine Shop Calculations: Geometric Construction - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 10 No. 6 Nov-Dec 1991","15"
    "Product Review: Ultra-Thin Parallels","Guy Lautard","Miscellaneous","HSM Vol. 10 No. 6 Nov-Dec 1991","15"
    "An Accurate Vise for the Milling Machine","Rudy Kouhoupt","Mills","HSM Vol. 10 No. 6 Nov-Dec 1991","18"
    "Topsy-turvy Engine - Part II","Philip Duclos","Engines","HSM Vol. 10 No. 6 Nov-Dec 1991","27"
    "Plastic Injection Molding Machine - Part IV","Rodney W. Hanson","Shop Machinery","HSM Vol. 10 No. 6 Nov-Dec 1991","32"
    "Dial Indicators - Dial Test Indicators","John B. Gascoyne","Shop Accessories","HSM Vol. 10 No. 6 Nov-Dec 1991","37"
    "Out-of-the-Way Storage Where You Need It","Don H. Vreeland","Lathes","HSM Vol. 10 No. 6 Nov-Dec 1991","40"
    "Toggle-link Operated Can Crusher","John Maruschak","Projects","HSM Vol. 10 No. 6 Nov-Dec 1991","41"
    "Product Review: A Small Magnetic V-block","Guy Lautard","Miscellaneous","HSM Vol. 10 No. 6 Nov-Dec 1991","43"
    "Computers in the Shop: Convert a Milling Machine to CNC Control - Part IV","Roland W. Friestad","Computers","HSM Vol. 10 No. 6 Nov-Dec 1991","44"
    "The Micro Machinist: Making a Pair of Milling Clamps - Part I","Rudy Kouhoupt","Mills","HSM Vol. 10 No. 6 Nov-Dec 1991","48"
    "From the Scrapbox: A Shell End Mill Arbor","Frank A. McLean","Shop Accessories","HSM Vol. 10 No. 6 Nov-Dec 1991","51"
    "Cam Clamps","Edward G. Hoffman","Shop Accessories","HSM Vol. 10 No. 6 Nov-Dec 1991","54"
    "Book Review: Clockmaking & Modelmaking Tools and Techniques","Guy Lautard","Miscellaneous","HSM Vol. 11 No. 1 Jan-Feb 1992","14"
    "Machine Shop Calculations: Geometric Construction - Part III","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 11 No. 1 Jan-Feb 1992","15"
    "Turning Short Tapers on a Mill","Stephen M. Thomas","Mills","HSM Vol. 11 No. 1 Jan-Feb 1992","18"
    "Topsy-turvy Engine - Part III","Philip Duclos","Engines","HSM Vol. 11 No. 1 Jan-Feb 1992","24"
    "Indexing Template for Easier Layout","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 11 No. 1 Jan-Feb 1992","29"
    "A Simple Indexing Rotary Table","Mike Hoff","Shop Accessories","HSM Vol. 11 No. 1 Jan-Feb 1992","32"
    "Steve Makes a Mistake","Steve Acker","General Machining Knowledge","HSM Vol. 11 No. 1 Jan-Feb 1992","38"
    "Adapter for a Boring Head","Don H. Vreeland","Mills","HSM Vol. 11 No. 1 Jan-Feb 1992","39"
    "Drill Press Quill Lock","Marshall R. Young","Shop Machinery","HSM Vol. 11 No. 1 Jan-Feb 1992","40"
    "The Micro Machinist: A Holder for 13/16"" Dies","Rudy Kouhoupt","Shop Accessories","HSM Vol. 11 No. 1 Jan-Feb 1992","42"
    "Computers in the Shop: Convert a Milling Machine to CNC Control - Part V","Roland W. Friestad","Computers","HSM Vol. 11 No. 1 Jan-Feb 1992","45"
    "From the Scrapbox: Fitting Small Drill Chucks","Frank A. McLean","Shop Machinery","HSM Vol. 11 No. 1 Jan-Feb 1992","52"
    "Commercial Components","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 11 No. 1 Jan-Feb 1992","56"
    "Product Review: Vee-Grooved Snap Jaws","Guy Lautard","Miscellaneous","HSM Vol. 11 No. 2 Mar-Apr 1992","11"
    "Product Review: Band Saw Splicer","Joe Rice","Miscellaneous","HSM Vol. 11 No. 2 Mar-Apr 1992","12"
    "Machine Shop Calculations: Geometric Construction - Part IV","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 11 No. 2 Mar-Apr 1992","17"
    "Starting Turning: Part I - A Paperweight","Audrey Mason","Lathes","HSM Vol. 11 No. 2 Mar-Apr 1992","20"
    "Topsy-turvy Engine - Part IV","Philip Duclos","Engines","HSM Vol. 11 No. 2 Mar-Apr 1992","29"
    "A Bit of Inspiration: A David Kucer, Miniaturist","Joe Rice","Hobby Community","HSM Vol. 11 No. 2 Mar-Apr 1992","36"
    "Knurls and Knurling","Eric Carver","Shop Accessories","HSM Vol. 11 No. 2 Mar-Apr 1992","38"
    "The Micro Machinist: Turning a Morse Taper","Rudy Kouhoupt","Shop Accessories","HSM Vol. 11 No. 2 Mar-Apr 1992","42"
    "Computers in the Shop: Convert a Milling Machine to CNC Control - Part VI","Roland W. Friestad","Computers","HSM Vol. 11 No. 2 Mar-Apr 1992","45"
    "From the Scrapbox: Improving the Collet Draw Tube","Frank A. McLean","Lathes","HSM Vol. 11 No. 2 Mar-Apr 1992","49"
    "Mechanical Fasteners - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 11 No. 2 Mar-Apr 1992","50"
    "An Inexpensive Power Feed","Melvin L. Kalb","Miscellaneous","HSM Vol. 11 No. 2 Mar-Apr 1992","53"
    "Machine Shop Calculations: Geometric Construction - Part V","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 11 No. 3 May-Jun 1992","15"
    "Starting Turning: Part II - Decorative Boxes","Audrey Mason","Lathes","HSM Vol. 11 No. 3 May-Jun 1992","19"
    "Adapting the Myford for Hand Turning and 10mm Collets","W. R. Smith","Lathes","HSM Vol. 11 No. 3 May-Jun 1992","26"
    "Topsy-turvy Engine - Part V","Philip Duclos","Engines","HSM Vol. 11 No. 3 May-Jun 1992","32"
    "Removing Broken Screws and Studs","Edward G. Hoffman","Miscellaneous","HSM Vol. 11 No. 3 May-Jun 1992","37"
    "Machine Tool Covers","Theodore (Ted) J. Myers","Miscellaneous","HSM Vol. 11 No. 3 May-Jun 1992","39"
    "A Homemade Electric Motor Mount","Ralph T. Walker","Miscellaneous","HSM Vol. 11 No. 3 May-Jun 1992","42"
    "Ball Turning in the Mill","Norman H. Bennett","Mills","HSM Vol. 11 No. 3 May-Jun 1992","44"
    "The Micro Machinist: Setting Up Shop","Rudy Kouhoupt","General Machining Knowledge","HSM Vol. 11 No. 3 May-Jun 1992","47"
    "From the Scrapbox: An Unusual Lathe Dog","Frank A. McLean","Lathes","HSM Vol. 11 No. 3 May-Jun 1992","50"
    "Mechanical Fasteners - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 11 No. 3 May-Jun 1992","53"
    "Product Review: CAD for the Small Shop","Edward G. Hoffman","Miscellaneous","HSM Vol. 11 No. 4 Jul-Aug 1992","14"
    "Product Review: Cameron Series 164 Micro Drill Press","John B. Gascoyne","Miscellaneous","HSM Vol. 11 No. 4 Jul-Aug 1992","15"
    "Machine Shop Calculations: Measuring With Pins - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 11 No. 4 Jul-Aug 1992","18"
    "A Deluxe Radius Turning Attachment - Part I","Glenn L. Wilson","Lathes","HSM Vol. 11 No. 4 Jul-Aug 1992","20"
    "Starting Turning: Part III - Lace Bobbins","Audrey Mason","Lathes","HSM Vol. 11 No. 4 Jul-Aug 1992","27"
    "A Wood Carving Machine","John Snyder","Shop Machinery","HSM Vol. 11 No. 4 Jul-Aug 1992","34"
    "Drill Press Vise Restraints","James Berger","Shop Machinery","HSM Vol. 11 No. 4 Jul-Aug 1992","45"
    "A Simple Grinder Water Pot","E. T. Feller","Miscellaneous","HSM Vol. 11 No. 4 Jul-Aug 1992","50"
    "The Micro Machinist: Making a Catch Plate","Rudy Kouhoupt","Lathes","HSM Vol. 11 No. 4 Jul-Aug 1992","51"
    "From the Scrapbox: A Bell Chuck for Your Lathe","Frank A. McLean","Lathes","HSM Vol. 11 No. 4 Jul-Aug 1992","54"
    "Another Fly Cutter","E. T. Feller","Miscellaneous","HSM Vol. 11 No. 4 Jul-Aug 1992","57"
    "Fixture Keys","Edward G. Hoffman","Shop Accessories","HSM Vol. 11 No. 4 Jul-Aug 1992","58"
    "Product Review: Vernier Protractor","Guy Lautard","Miscellaneous","HSM Vol. 11 No. 5 Sep-Oct 1992","12"
    "Machine Shop Calculations: Measuring With Pins - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 11 No. 5 Sep-Oct 1992","16"
    "A Deluxe Radius Turning Attachment - Part II","Glenn L. Wilson","Lathes","HSM Vol. 11 No. 5 Sep-Oct 1992","18"
    "An Improved Lathe Drive","G. Wadham","Lathes","HSM Vol. 11 No. 5 Sep-Oct 1992","24"
    "Checkering in the Mill","Steve Acker","Mills","HSM Vol. 11 No. 5 Sep-Oct 1992","30"
    "On Improving the Image","Alberto Marx","Miscellaneous","HSM Vol. 11 No. 5 Sep-Oct 1992","33"
    "Alternate Clamping Devices - Part I","Edward G. Hoffman","Shop Accessories","HSM Vol. 11 No. 5 Sep-Oct 1992","40"
    "From the Scrapbox: Making a Knurled Head Thumbscrew","Frank A. McLean","Miscellaneous","HSM Vol. 11 No. 5 Sep-Oct 1992","45"
    "Skipping","Terry Sexton","Miscellaneous","HSM Vol. 11 No. 5 Sep-Oct 1992","46"
    "Taper Turning","Don H. Vreeland","Lathes","HSM Vol. 11 No. 5 Sep-Oct 1992","47"
    "The Micro Machinist: Checking Lathe Alignment","Rudy Kouhoupt","Lathes","HSM Vol. 11 No. 5 Sep-Oct 1992","48"
    "Computers in the Shop: Build Your Own CNC Controller - Part I","Roland W. Friestad","Computers","HSM Vol. 11 No. 5 Sep-Oct 1992","52"
    "Vise Jaw Fixtures - Part I","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 11 No. 5 Sep-Oct 1992","56"
    "Machine Shop Calculations: Measuring With Pins - Part III","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 11 No. 6 Nov-Dec 1992","16"
    "A Thread Tooling System and Wiggler for the Lathe","D. E. Johnson","Lathes","HSM Vol. 11 No. 6 Nov-Dec 1992","18"
    "Starting Turning: Part IV - Two Candlesticks","Audrey Mason","Lathes","HSM Vol. 11 No. 6 Nov-Dec 1992","24"
    "Alternate Clamping Devices - Part II","Edward G. Hoffman","Shop Accessories","HSM Vol. 11 No. 6 Nov-Dec 1992","34"
    "Cutting Irregularly Shaped Holes","Lowie L. Roscoe, Jr.","Miscellaneous","HSM Vol. 11 No. 6 Nov-Dec 1992","39"
    "Basement Rust","Michael M. Ambrosino","General Machining Knowledge","HSM Vol. 11 No. 6 Nov-Dec 1992","40"
    "From the Scrapbox: A Cylinder or Master Square","Frank A. McLean","Lathes","HSM Vol. 11 No. 6 Nov-Dec 1992","42"
    "The Micro Machinist: Tiny Engines","Rudy Kouhoupt","Engines","HSM Vol. 11 No. 6 Nov-Dec 1992","46"
    "Computers in the Shop: Build Your Own CNC Controller - Part II","Roland W. Friestad","Computers","HSM Vol. 11 No. 6 Nov-Dec 1992","51"
    "Vise Jaw Fixtures - Part II","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 11 No. 6 Nov-Dec 1992","54"
    "Product Review: Math Solutions at Your Fingertips","Edward G. Hoffman","Miscellaneous","HSM Vol. 11 No. 6 Nov-Dec 1992","56"
    "A Thread-cutting Aid","Karl R. Brown","General Machining Knowledge","HSM Vol. 11 No. 6 Nov-Dec 1992","57"
    "Machine Shop Calculations: Measuring With Pins - Part IV","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 12 No. 1 Jan-Feb 1993","6"
    "Chips & Sparks: Cutting the Chatter","Paul Baumgardner","Techniques","HSM Vol. 12 No. 1 Jan-Feb 1993","14"
    "Chips & Sparks: New Use for an Old Tool","Bob Austill","Techniques","HSM Vol. 12 No. 1 Jan-Feb 1993","14"
    "Thread Cutting on the Lathe","Rudy Kouhoupt","Techniques","HSM Vol. 12 No. 1 Jan-Feb 1993","18"
    "Aluminum Fundamentals - Part I","George W. Genevro","General Machining Knowledge","HSM Vol. 12 No. 1 Jan-Feb 1993","26"
    "A Saw Blade Cutoff Tool","Conrad A. Huard","Machining Accessories","HSM Vol. 12 No. 1 Jan-Feb 1993","31"
    "Making Pin Punches","Steve Acker","Jigs & Fixtures","HSM Vol. 12 No. 1 Jan-Feb 1993","32"
    "Lead Shot Filled Boring Bar","J. W. Straight","Machining Accessories","HSM Vol. 12 No. 1 Jan-Feb 1993","38"
    "The Grizzly 8 x 18 Lathe","Glenn M. Schultz","Machine Tools","HSM Vol. 12 No. 1 Jan-Feb 1993","39"
    "From the Scrapbox: Tailstock Attachments for the Lathe","Frank A. McLean","Machining Accessories","HSM Vol. 12 No. 1 Jan-Feb 1993","46"
    "The Micro Machinist: X and Y Stops for the Mill","Rudy Kouhoupt","Machining Accessories","HSM Vol. 12 No. 1 Jan-Feb 1993","49"
    "Vise Jaw Fixtures - Part III","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 12 No. 1 Jan-Feb 1993","52"
    "Computers in the Shop: Build Your Own CNC Controller - Part III","Roland W. Friestad","Computers","HSM Vol. 12 No. 1 Jan-Feb 1993","54"
    "Chips & Sparks: Parting Remarks","Jack Johns","Techniques","HSM Vol. 12 No. 2 Mar-Apr 1993","13"
    "The Butler Multiple Boring Machines","Harold Mason","Miscellaneous","HSM Vol. 12 No. 2 Mar-Apr 1993","14"
    "Tru Punch Shim Punch and Die Set","Guy Lautard","Hobby Community","HSM Vol. 12 No. 2 Mar-Apr 1993","14"
    "A Milling Machine Conversion","Larry Shull","Techniques","HSM Vol. 12 No. 2 Mar-Apr 1993","24"
    "A Spindle Lock for Your Mill/drill","Bill Lowery","Machining Accessories","HSM Vol. 12 No. 2 Mar-Apr 1993","28"
    "Aluminum Fundamentals - Part II - Temper Designation","George W. Genevro","General Machining Knowledge","HSM Vol. 12 No. 2 Mar-Apr 1993","30"
    "From the Scrapbox: Tailstock Attachment","Frank A. McLean","Machining Accessories","HSM Vol. 12 No. 2 Mar-Apr 1993","36"
    "The Micro Machinist: Drill Press Chuck Handles","Rudy Kouhoupt","Machining Accessories","HSM Vol. 12 No. 2 Mar-Apr 1993","39"
    "A Handy File Cleaner","Steve Acker","Techniques","HSM Vol. 12 No. 2 Mar-Apr 1993","42"
    "Computers in the Shop: And Now For Something Completely Different","Roland W. Friestad","Computers","HSM Vol. 12 No. 2 Mar-Apr 1993","44"
    "Mechanical Fasteners - Part I","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 12 No. 2 Mar-Apr 1993","48"
    "Chips & Sparks: Replacing the Lathe Spindle Belt","Joseph Bucca, Jr.","Techniques","HSM Vol. 12 No. 3 May-Jun 1993","12"
    "Chips & Sparks: Tool Tray","George Kolar","Machining Accessories","HSM Vol. 12 No. 3 May-Jun 1993","12"
    "Chips & Sparks: Edge Finders","Jimmy C. Cuttrell","Machining Accessories","HSM Vol. 12 No. 3 May-Jun 1993","13"
    "Convert It","Edward G. Hoffman","Hobby Community","HSM Vol. 12 No. 3 May-Jun 1993","14"
    "Gearless Hit 'n Miss Engine - Part I","Philip Duclos","Engines","HSM Vol. 12 No. 3 May-Jun 1993","16"
    "Mobilize Your Heavy Shop Tools","Samuel W. Carson","Techniques","HSM Vol. 12 No. 3 May-Jun 1993","24"
    "Building a Hydraulic Press Twice - Part I","Steve Acker","Machine Tools","HSM Vol. 12 No. 3 May-Jun 1993","31"
    "Vacuum Up Those Chips!","Walt Dougherty","Techniques","HSM Vol. 12 No. 3 May-Jun 1993","36"
    "Knockout Bar","Jack R. Thompson","Machining Accessories","HSM Vol. 12 No. 3 May-Jun 1993","37"
    "From the Scrapbox: Drill Press Router Adapter","Frank A. McLean","Machining Accessories","HSM Vol. 12 No. 3 May-Jun 1993","38"
    "The Micro Machinist: A Lathe Table","Rudy Kouhoupt","Machining Accessories","HSM Vol. 12 No. 3 May-Jun 1993","43"
    "Mechanical Fasteners - Part II","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 12 No. 3 May-Jun 1993","46"
    "Computers in the Shop: Retrofitting Atlas/Craftsman and Other Lathes to CNC Control - Part I","Roland W. Friestad","Computers","HSM Vol. 12 No. 3 May-Jun 1993","48"
    "Chinese- and American-made Vernier Calipers","Guy Lautard","Hobby Community","HSM Vol. 12 No. 4 Jul-Aug 1993","12"
    "The Diamond Toolholder","Rudy Kouhoupt","Hobby Community","HSM Vol. 12 No. 4 Jul-Aug 1993","16"
    "Chips & Sparks: Free Machining Steel","Aubrey Keet","General Machining Knowledge","HSM Vol. 12 No. 4 Jul-Aug 1993","18"
    "Chips & Sparks: Tap and Clearance Drills","Stephen R. Forslind","Techniques","HSM Vol. 12 No. 4 Jul-Aug 1993","18"
    "Chips & Sparks: Valve Stem Remover","Louis Golembiewski","Jigs & Fixtures","HSM Vol. 12 No. 4 Jul-Aug 1993","18"
    "Gearless Hit 'n Miss Engine - Part II","Philip Duclos","Engines","HSM Vol. 12 No. 4 Jul-Aug 1993","20"
    "Thoughts on Selecting Vertical Mills - Part I","Thomas F. Howard","Techniques","HSM Vol. 12 No. 4 Jul-Aug 1993","30"
    "Strike Three Against Home Offices?","Mark E. Battersby","Hobby Community","HSM Vol. 12 No. 4 Jul-Aug 1993","34"
    "A Quick-change Tool Post System - Part I","Richard S. Torgerson","Machining Accessories","HSM Vol. 12 No. 4 Jul-Aug 1993","36"
    "Building a Hydraulic Press Twice - Part II","Steve Acker","Machine Tools","HSM Vol. 12 No. 4 Jul-Aug 1993","43"
    "Cutting Vee Notches","John A. Cooper","Techniques","HSM Vol. 12 No. 4 Jul-Aug 1993","48"
    "The Micro Machinist: Making a Cutoff Toolholder","Rudy Kouhoupt","Machining Accessories","HSM Vol. 12 No. 4 Jul-Aug 1993","49"
    "From the Scrapbox: Rounding the Ends","Frank A. McLean","Techniques","HSM Vol. 12 No. 4 Jul-Aug 1993","52"
    "Drill Bushings - Part I","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 12 No. 4 Jul-Aug 1993","54"
    "Chips & Sparks: Cutting Coarse Internal Threads","George Kolar","Techniques","HSM Vol. 12 No. 5 Sep-Oct 1993","14"
    "Chips & Sparks: Drill Press Speed Reducer","Ward Maude","Machining Accessories","HSM Vol. 12 No. 5 Sep-Oct 1993","14"
    "Chips & Sparks: Headstock Belt the Easy Way","Bob Myers","Techniques","HSM Vol. 12 No. 5 Sep-Oct 1993","14"
    "Chips & Sparks: A Simple Broach","J. F. Rule","Machining Accessories","HSM Vol. 12 No. 5 Sep-Oct 1993","15"
    "Chips & Sparks: Odds and Ends","Robert W. Evans","Techniques","HSM Vol. 12 No. 5 Sep-Oct 1993","15"
    "Basic Metal Lathe Operations - Part II","Guy Lautard","Hobby Community","HSM Vol. 12 No. 5 Sep-Oct 1993","16"
    "Making the Most of Your Lathe","Joe Rice","Hobby Community","HSM Vol. 12 No. 5 Sep-Oct 1993","16"
    "Greensand Casting Techniques - Volume 2","Joe Rice","Hobby Community","HSM Vol. 12 No. 5 Sep-Oct 1993","17"
    "Knorrostol","Guy Lautard","Hobby Community","HSM Vol. 12 No. 5 Sep-Oct 1993","17"
    "Gearless Hit 'n Miss Engine - Part III","Philip Duclos","Engines","HSM Vol. 12 No. 5 Sep-Oct 1993","18"
    "Thoughts on Selecting Vertical Mills - Part II","Thomas F. Howard","Techniques","HSM Vol. 12 No. 5 Sep-Oct 1993","26"
    "Starting Turning - Part V","Audrey Mason","Techniques","HSM Vol. 12 No. 5 Sep-Oct 1993","30"
    "A Quick-change Tool Post System - Part II","Richard S. Torgerson","Machining Accessories","HSM Vol. 12 No. 5 Sep-Oct 1993","39"
    "From the Scrapbox: Brazing Band Saw Blades","Frank A. McLean","Techniques","HSM Vol. 12 No. 5 Sep-Oct 1993","44"
    "The Micro Machinist: Using a Cutoff Tool","Rudy Kouhoupt","Techniques","HSM Vol. 12 No. 5 Sep-Oct 1993","46"
    "Computers in the Shop: Retrofitting Atlas/Craftsman and Other Lathes to CNC Control - Part II","Roland W. Friestad","Computers","HSM Vol. 12 No. 5 Sep-Oct 1993","49"
    "Drill Bushings - Part II","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 12 No. 5 Sep-Oct 1993","54"
    "Threaded Bushing","Jack R. Thompson","Techniques","HSM Vol. 12 No. 5 Sep-Oct 1993","56"
    "Toolmaker's Button","D. M. Thomson","Shop Accessories","HSM Vol. 12 No. 5 Sep-Oct 1993","56"
    "Mr. Cushion Step","Guy Lautard","Hobby Community","HSM Vol. 12 No. 5 Sep-Oct 1993","57"
    "Chips & Sparks: Engine Turning","Paul Biganeiss","Techniques","HSM Vol. 12 No. 6 Nov-Dec 1993","14"
    "Chips & Sparks: Homemade Air Compressor","George Kolar","Shop Machinery","HSM Vol. 12 No. 6 Nov-Dec 1993","14"
    "Math Solutions for Your Computer: Any Angle","Edward G. Hoffman","Hobby Community","HSM Vol. 12 No. 6 Nov-Dec 1993","16"
    "Math Solutions for Your Computer: Craft-E","Edward G. Hoffman","Hobby Community","HSM Vol. 12 No. 6 Nov-Dec 1993","16"
    "Math Solutions for Your Computer: Mr. Machinist","Edward G. Hoffman","Hobby Community","HSM Vol. 12 No. 6 Nov-Dec 1993","17"
    "Math Solutions for Your Computer: NBS Trig and NBS Toolpath","Edward G. Hoffman","Hobby Community","HSM Vol. 12 No. 6 Nov-Dec 1993","18"
    "Math Solutions for Your Computer: Shopmathster II","Edward G. Hoffman","Hobby Community","HSM Vol. 12 No. 6 Nov-Dec 1993","19"
    "How to Make a Skeleton Wall Clock - Part I","W. R. Smith","Clocks","HSM Vol. 12 No. 6 Nov-Dec 1993","22"
    "Gearless Hit 'n Miss Engine - Part IV","Philip Duclos","Engines","HSM Vol. 12 No. 6 Nov-Dec 1993","29"
    "Cerro Alloys Aid in Machining Irregular Parts","Ronald E. McBride","Miscellaneous","HSM Vol. 12 No. 6 Nov-Dec 1993","36"
    "A Quick-change Tool Post System - Part III","Richard S. Torgerson","Machining Accessories","HSM Vol. 12 No. 6 Nov-Dec 1993","39"
    "Enco 12 x 26 Geared Head Engine Lathe: A Review","Clifton E. R. Lawson","Hobby Community","HSM Vol. 12 No. 6 Nov-Dec 1993","44"
    "Chips & Sparks: A Half Center","Norm Wells","Techniques","HSM Vol. 12 No. 6 Nov-Dec 1993","49"
    "On the Use of Threading Dials for Cutting Metric Threads","Eugene E. Petersen","Techniques","HSM Vol. 12 No. 6 Nov-Dec 1993","49"
    "The Micro Machinist: Make a Center Finder","Rudy Kouhoupt","Shop Accessories","HSM Vol. 12 No. 6 Nov-Dec 1993","51"
    "From the Scrapbox: Hinge Centering Punch","Frank A. McLean","Machining Accessories","HSM Vol. 12 No. 6 Nov-Dec 1993","54"
    "Drill Bushings - Part III","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 12 No. 6 Nov-Dec 1993","56"
    "Chips & Sparks: Another Vise Jaw Idea","Fred Bruce","Machining Accessories","HSM Vol. 13 No. 1 Jan-Feb 1994","16"
    "Chips & Sparks: Oil Dispenser","Harvey Freeman","Machine Modifications","HSM Vol. 13 No. 1 Jan-Feb 1994","16"
    "Chips & Sparks: A Stable Propane Torch","Norm Wells","Welding/Foundry/Forging","HSM Vol. 13 No. 1 Jan-Feb 1994","17"
    "Chips & Sparks: Tool Tray","George Kolar","Machining Accessories","HSM Vol. 13 No. 1 Jan-Feb 1994","17"
    "Learn CAD Now and Easy CAD 2","Joe Rice","Hobby Community","HSM Vol. 13 No. 1 Jan-Feb 1994","18"
    "Micrografx Designer 3.1","Joe Rice","Hobby Community","HSM Vol. 13 No. 1 Jan-Feb 1994","19"
    "The Paragon Q-11A Heat-Treating Furnace","Corrine Hummel","Hobby Community","HSM Vol. 13 No. 1 Jan-Feb 1994","20"
    "The Machinist's Third Bedside Reader","Clover McKinley","Hobby Community","HSM Vol. 13 No. 1 Jan-Feb 1994","23"
    "A Quick-change Tool Post System - Part IV","Richard S. Torgerson","Machining Accessories","HSM Vol. 13 No. 1 Jan-Feb 1994","24"
    "How to Make a Skeleton Wall Clock - Part II","W. R. Smith","Clocks","HSM Vol. 13 No. 1 Jan-Feb 1994","29"
    "Some Pointers on Scroll Sawing","Guy Lautard","Techniques","HSM Vol. 13 No. 1 Jan-Feb 1994","34"
    "A Mill Spindle Indicator Holder","Roy Rice","Machining Accessories","HSM Vol. 13 No. 1 Jan-Feb 1994","35"
    "Balancing a Grinding Wheel","A. M. Christopherson","Miscellaneous","HSM Vol. 13 No. 1 Jan-Feb 1994","36"
    "Unimat Headstock Adapter","Conrad A. Huard","Machining Accessories","HSM Vol. 13 No. 1 Jan-Feb 1994","38"
    "Facing to Accurate Length","L. C. Melton","Techniques","HSM Vol. 13 No. 1 Jan-Feb 1994","40"
    "More on Three-phase Converters","Robert J. Matthys","Miscellaneous","HSM Vol. 13 No. 1 Jan-Feb 1994","41"
    "Drill Bushings - Part IV","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 13 No. 1 Jan-Feb 1994","44"
    "Jigs & Fixtures: Drill Brushings - Part IV","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 13 No. 1 Jan-Feb 1994","44"
    "The Micro Machinist: Base for a Band Saw","Rudy Kouhoupt","Shop Machinery","HSM Vol. 13 No. 1 Jan-Feb 1994","46"
    "From the Scrapbox: Using a Router on the Vertical Milling Machine","Frank A. McLean","Machining Accessories","HSM Vol. 13 No. 1 Jan-Feb 1994","49"
    "Computers in the Shop: Retrofitting Atlas/Craftsman and Other Lathes to CNC Control - Part III","Roland W. Friestad","Computers","HSM Vol. 13 No. 1 Jan-Feb 1994","52"
    "Chips & Sparks: Dental Burrs in the Metal Shop","Donovan V. Browne","Miscellaneous","HSM Vol. 13 No. 2 Mar-Apr 1994","16"
    "Chips & Sparks: Surface Plate Care","Norm Wells","Techniques","HSM Vol. 13 No. 2 Mar-Apr 1994","16"
    "Surface Plate Care","Norm Wells","Techniques","HSM Vol. 13 No. 2 Mar-Apr 1994","16"
    "Chips & Sparks: Cut Threads With a Tap","Don Hester","Techniques","HSM Vol. 13 No. 2 Mar-Apr 1994","17"
    "Adjustable Packing Blocks","Rudy Kouhoupt","Hobby Community","HSM Vol. 13 No. 2 Mar-Apr 1994","18"
    "Workshop Tool & Accessory Plans","Joe Rice","Hobby Community","HSM Vol. 13 No. 2 Mar-Apr 1994","18"
    "The Micro Machinist: Build and Use a Tool Post Grinder - Part I","Rudy Kouhoupt","Shop Accessories","HSM Vol. 13 No. 2 Mar-Apr 1994","20"
    "How to Make a Skeleton Wall Clock - Part III","W. R. Smith","Clocks","HSM Vol. 13 No. 2 Mar-Apr 1994","24"
    "North American Model Engineering Exposition","Joe Rice","Hobby Community","HSM Vol. 13 No. 2 Mar-Apr 1994","30"
    "Building the Titan .60 - Part I","George W. Genevro","Engines","HSM Vol. 13 No. 2 Mar-Apr 1994","34"
    "Turning Short Tapers on a Mill/drill","Stephen M. Thomas","Techniques","HSM Vol. 13 No. 2 Mar-Apr 1994","41"
    "A Quick Tumbler Gear Reversal Mechanism","Theodore (Ted) J. Myers","Machining Accessories","HSM Vol. 13 No. 2 Mar-Apr 1994","44"
    "From the Scrapbox: An Unusual Turning Operation","Frank A. McLean","Techniques","HSM Vol. 13 No. 2 Mar-Apr 1994","46"
    "Set Blocks","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 13 No. 2 Mar-Apr 1994","48"
    "A Simple Timer","J. W. (Bill) Reichart","Clocks","HSM Vol. 13 No. 2 Mar-Apr 1994","52"
    "A Modified Arbor Press Ram","Alan Andrews","Shop Machinery","HSM Vol. 13 No. 2 Mar-Apr 1994","54"
    "Reuse Broken Drills","L. A. Van Veghel","Techniques","HSM Vol. 13 No. 2 Mar-Apr 1994","55"
    "A Video Visit with Guy Lautard & Bill Fenton","Clover McKinley","Hobby Community","HSM Vol. 13 No. 3 May-Jun 1994","13"
    "The Video with Guy Lautard & Bill Fenton","L. A. Van Veghel","Hobby Community","HSM Vol. 13 No. 3 May-Jun 1994","13"
    "Chips & Sparks: Bridgeport Mill Tricks","Jim Koutsoures","Techniques","HSM Vol. 13 No. 3 May-Jun 1994","14"
    "Chips & Sparks: Internal Keyway Slotting","George Kolar","Techniques","HSM Vol. 13 No. 3 May-Jun 1994","15"
    "AMT Radial Drill Press","Edward G. Hoffman","Hobby Community","HSM Vol. 13 No. 3 May-Jun 1994","16"
    "Single-shot, Lever-action, Falling-block Rifle Action - Part I","Walter B. Mueller","Gunsmithing","HSM Vol. 13 No. 3 May-Jun 1994","20"
    "A Mill/Drill Support","Paul J. Holm","Machining Accessories","HSM Vol. 13 No. 3 May-Jun 1994","29"
    "Building the Titan .60 - Part II","George W. Genevro","Engines","HSM Vol. 13 No. 3 May-Jun 1994","32"
    "How to Make a Skeleton Wall Clock - Part IV","W. R. Smith","Clocks","HSM Vol. 13 No. 3 May-Jun 1994","36"
    "More on EDM","Jack Lewis","EDM","HSM Vol. 13 No. 3 May-Jun 1994","44"
    "Computers in the Shop: Retrofitting Atlas/Craftsman and Other Lathes to CNC Control - Part IV","Roland W. Friestad","Computers","HSM Vol. 13 No. 3 May-Jun 1994","48"
    "The Micro Machinist: Build and Use a Tool Post Grinder - Part II","Rudy Kouhoupt","Shop Accessories","HSM Vol. 13 No. 3 May-Jun 1994","52"
    "Workholder Design Tips - Part I","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 13 No. 3 May-Jun 1994","56"
    "From the Scrapbox: Milling a Keyseat in a Shaft","Frank A. McLean","Techniques","HSM Vol. 13 No. 3 May-Jun 1994","58"
    "Chips & Sparks: In Lieu of a Thread Cutting Dial","Harry U. Snow","Techniques","HSM Vol. 13 No. 4 Jul-Aug 1994","16"
    "Chips & Sparks: Pin Vise","Eddie M. Zanrosso","Shop Accessories","HSM Vol. 13 No. 4 Jul-Aug 1994","16"
    "How to Make a Skeleton Wall Clock - Part V","W. R. Smith","Clocks","HSM Vol. 13 No. 4 Jul-Aug 1994","20"
    "Single-shot, Lever-action, Falling-block Rifle Action - Part II","Walter B. Mueller","Gunsmithing","HSM Vol. 13 No. 4 Jul-Aug 1994","26"
    "Building the Titan .60 - Part III","George W. Genevro","Engines","HSM Vol. 13 No. 4 Jul-Aug 1994","39"
    "Large Radius Cylindrical Cuts on a Shaper","Peter J. Hoijer","Techniques","HSM Vol. 13 No. 4 Jul-Aug 1994","44"
    "The Micro Machinist: Build and Use a Tool Post Grinder - Part III","Rudy Kouhoupt","Shop Accessories","HSM Vol. 13 No. 4 Jul-Aug 1994","46"
    "From the Scrapbox: Correcting a Milling Machine Vise","Frank A. McLean","Techniques","HSM Vol. 13 No. 4 Jul-Aug 1994","50"
    "Workholder Design Tips - Part II","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 13 No. 4 Jul-Aug 1994","51"
    "Some Parts Source","Donald G. Honeywell","General Machining Knowledge","HSM Vol. 13 No. 4 Jul-Aug 1994","56"
    "The 1893 Springfield Duryea","Joe Rice","Hobby Community","HSM Vol. 13 No. 4 Jul-Aug 1994","56"
    "Fourth Annual NAMES Exposition","L. A. Van Veghel","Hobby Community","HSM Vol. 13 No. 5 Sep-Oct 1994","18"
    "Master Mechanics' Manual, Volume One","Clover McKinley","Hobby Community","HSM Vol. 13 No. 5 Sep-Oct 1994","18"
    "Avoiding Broken Gear Belts","Francis Langford","Techniques","HSM Vol. 13 No. 5 Sep-Oct 1994","19"
    "Serious Milling With the Lathe - Part I","D. E. Johnson","Machining Accessories","HSM Vol. 13 No. 5 Sep-Oct 1994","20"
    "How to Make a Skeleton Wall Clock - Part VI","W. R. Smith","Clocks","HSM Vol. 13 No. 5 Sep-Oct 1994","28"
    "Single-shot, Lever-action, Falling-block Rifle Action - Part III","Walter B. Mueller","Gunsmithing","HSM Vol. 13 No. 5 Sep-Oct 1994","36"
    "Excerpts from The Federal Firearms Regulations Guide","Kevin Dockery","Gunsmithing","HSM Vol. 13 No. 5 Sep-Oct 1994","42"
    "Tap Dogs","Glenn A. Pettit","Machining Accessories","HSM Vol. 13 No. 5 Sep-Oct 1994","43"
    "Building the Titan .60 - Part IV","George W. Genevro","Engines","HSM Vol. 13 No. 5 Sep-Oct 1994","44"
    "Files and Filing - Part I","Edward G. Hoffman","Hand Tools","HSM Vol. 13 No. 5 Sep-Oct 1994","47"
    "A Fixture for Milling End Curves","Rudy Kouhoupt","Machining Accessories","HSM Vol. 13 No. 5 Sep-Oct 1994","50"
    "Workholder Design Tips - Part III","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 13 No. 5 Sep-Oct 1994","54"
    "From the Scrapbox: Keyway Broach Bushings","Frank A. McLean","Machining Accessories","HSM Vol. 13 No. 5 Sep-Oct 1994","56"
    "Reviving a Lunch Break Shaper","Terry Sexton","Techniques","HSM Vol. 13 No. 6 Nov-Dec 1994","22"
    "How to Make a Skeleton Wall Clock - Part VII","W. R. Smith","Clocks","HSM Vol. 13 No. 6 Nov-Dec 1994","25"
    "Building the Titan .60 - Part V","George W. Genevro","Engines","HSM Vol. 13 No. 6 Nov-Dec 1994","32"
    "Serious Milling With the Lathe - Part II","D. E. Johnson","Machining Accessories","HSM Vol. 13 No. 6 Nov-Dec 1994","38"
    "Single-shot, Lever-action, Falling-block Rifle Action - Part IV","Walter B. Mueller","Gunsmithing","HSM Vol. 13 No. 6 Nov-Dec 1994","45"
    "Chatterless Countersinks","Robert S. Hedin","Machining Accessories","HSM Vol. 13 No. 6 Nov-Dec 1994","48"
    "Files and Filing - Part II","Edward G. Hoffman","Hand Tools","HSM Vol. 13 No. 6 Nov-Dec 1994","50"
    "Low-cost Reversing Switch for Electric Motors","R. L. Halbert","Motors","HSM Vol. 13 No. 6 Nov-Dec 1994","53"
    "Clamping Tapered Material in a Vise - No Problem!","Joe Harmon","Techniques","HSM Vol. 13 No. 6 Nov-Dec 1994","54"
    "Starrett's No.164 Series A Clamp","Guy Lautard","Hobby Community","HSM Vol. 13 No. 6 Nov-Dec 1994","55"
    "From the Scrapbox: Improving the Horizontal/Vertical Band Saw","Frank A. McLean","Techniques","HSM Vol. 13 No. 6 Nov-Dec 1994","58"
    "Specialty Locating Devices - Part I","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 13 No. 6 Nov-Dec 1994","60"
    "Make an Open-Sided Tool Post","Rudy Kouhoupt","Machining Accessories","HSM Vol. 13 No. 6 Nov-Dec 1994","62"
    "The Model Engineers Workshop Manual","Gregory P. Widin","Hobby Community","HSM Vol. 14 No. 1 Jan-Feb 1995","18"
    "Start Turning: Part VI - Mini Screw Clamps","Audrey Mason","Machining Accessories","HSM Vol. 14 No. 1 Jan-Feb 1995","22"
    "Serious Milling With the Lathe - Part III","D. E. Johnson","Machining Accessories","HSM Vol. 14 No. 1 Jan-Feb 1995","30"
    "How to Make a Skeleton Wall Clock - Part VIII","W. R. Smith","Clocks","HSM Vol. 14 No. 1 Jan-Feb 1995","37"
    "Single-shot, Lever-action, Falling-block Rifle Action - Part V","Walter B. Mueller","Gunsmithing","HSM Vol. 14 No. 1 Jan-Feb 1995","44"
    "Files and Filing - Part III","Edward G. Hoffman","Hand Tools","HSM Vol. 14 No. 1 Jan-Feb 1995","48"
    "The Micro Machinist: Old Iron - Part I","Rudy Kouhoupt","Machine Tools","HSM Vol. 14 No. 1 Jan-Feb 1995","52"
    "From the Scrapbox: Hand Turning on the Lathe","Frank A. McLean","Techniques","HSM Vol. 14 No. 1 Jan-Feb 1995","56"
    "Specialty Locating Devices - Part II","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 14 No. 1 Jan-Feb 1995","58"
    "Chips & Sparks: Inexpensive Tool Mounts","Thomas M. Verity","Machining Accessories","HSM Vol. 14 No. 2 Mar-Apr 1995","20"
    "Chips & Sparks: Easy Way to Cut Metric Threads","Jack R. Lind","Techniques","HSM Vol. 14 No. 2 Mar-Apr 1995","21"
    "Chips & Sparks: When You Are Without a Tool Post Grinder","Chad Godeke","Miscellaneous","HSM Vol. 14 No. 2 Mar-Apr 1995","21"
    "How to Make a Skeleton Wall Clock - Part IX","W. R. Smith","Clocks","HSM Vol. 14 No. 2 Mar-Apr 1995","22"
    "Single-shot, Lever-action, Falling-block Rifle Action - Part VI","Walter B. Mueller","Gunsmithing","HSM Vol. 14 No. 2 Mar-Apr 1995","28"
    "Mill-drill Adventures - Part I","D. E. Johnson","Machining Accessories","HSM Vol. 14 No. 2 Mar-Apr 1995","34"
    "A Machinist's Clock","J. W. (Bill) Reichart","Clocks","HSM Vol. 14 No. 2 Mar-Apr 1995","37"
    "From the Scrapbox: Horizontal Milling Attachment - Part I","Frank A. McLean","Machining Accessories","HSM Vol. 14 No. 2 Mar-Apr 1995","40"
    "Heat-Treatment Processes for Engine Components","George W. Genevro","Techniques","HSM Vol. 14 No. 2 Mar-Apr 1995","46"
    "A Homemade Die Filer","Melvin L. Kalb","Machine Tools","HSM Vol. 14 No. 2 Mar-Apr 1995","48"
    "The Micro Machinist: Old Iron - Part II","Rudy Kouhoupt","Machine Tools","HSM Vol. 14 No. 2 Mar-Apr 1995","50"
    "Specialty Clamping Devices - Part I","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 14 No. 2 Mar-Apr 1995","54"
    "Chips & Sparks: Safe Outlets","Greg Locati","General Machining Knowledge","HSM Vol. 14 No. 3 May-Jun 1995","18"
    "Chips & Sparks: Screw Trouble","Donald Duncan","Techniques","HSM Vol. 14 No. 3 May-Jun 1995","18"
    "Chips & Sparks: EDM Safety","Norm Wells","EDM","HSM Vol. 14 No. 3 May-Jun 1995","19"
    "Electrical Discharge Machining - Removing Metal By Spark Erosion: Part I - Introduction and Box Construction","Robert P. Langlois","Machining Accessories","HSM Vol. 14 No. 3 May-Jun 1995","22"
    "Spark Eroding a Broken Stud","Robert P. Langlois","EDM","HSM Vol. 14 No. 3 May-Jun 1995","30"
    "Mill-drill Adventures - Part II","D. E. Johnson","Machining Accessories","HSM Vol. 14 No. 3 May-Jun 1995","32"
    "How to Make a Skeleton Wall Clock - Part X","W. R. Smith","Clocks","HSM Vol. 14 No. 3 May-Jun 1995","39"
    "Dividing On The Lathe","James Schmidt","Techniques","HSM Vol. 14 No. 3 May-Jun 1995","45"
    "Single-shot, Lever-action, Falling-block Rifle Action - Part VII","Walter B. Mueller","Gunsmithing","HSM Vol. 14 No. 3 May-Jun 1995","46"
    "From the Scrapbox: Horizontal Milling Attachment - Part II","Frank A. McLean","Machining Accessories","HSM Vol. 14 No. 3 May-Jun 1995","48"
    "Specialty Clamping Devices - Part II","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 14 No. 3 May-Jun 1995","54"
    "The Micro Machinist: Old Iron - Part III","Rudy Kouhoupt","Machine Tools","HSM Vol. 14 No. 3 May-Jun 1995","56"
    "Mill-drill Adventures - Part III","D. E. Johnson","Machining Accessories","HSM Vol. 14 No. 4 Jul-Aug 1995","22"
    "Single-shot, Lever-action, Falling-block Rifle Action - Part VIII","Walter B. Mueller","Gunsmithing","HSM Vol. 14 No. 4 Jul-Aug 1995","27"
    "How to Make a Skeleton Wall Clock - Part XI","W. R. Smith","Clocks","HSM Vol. 14 No. 4 Jul-Aug 1995","32"
    "Electrical Discharge Machining - Removing Metal By Spark Erosion: Part II - The Spark Power Supply","Robert P. Langlois","Machining Accessories","HSM Vol. 14 No. 4 Jul-Aug 1995","40"
    "Drill Press Accessories: Small Drill Sharpening Guides","Alan Douglas","Machining Accessories","HSM Vol. 14 No. 4 Jul-Aug 1995","52"
    "From the Scrapbox: Small Drill Sharpening Guides","Frank A. McLean","Shop Accessories","HSM Vol. 14 No. 4 Jul-Aug 1995","52"
    "The Micro Machinist: A Compact Boring Head - Part I","Rudy Kouhoupt","Machining Accessories","HSM Vol. 14 No. 4 Jul-Aug 1995","55"
    "Specialty Clamping Devices - Part III","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 14 No. 4 Jul-Aug 1995","58"
    "Chips & Sparks: Shop Bench","David Joly","Shop Accessories","HSM Vol. 14 No. 5 Sep-Oct 1995","18"
    "Chips & Sparks: EDM Safety","Norm Wells","EDM","HSM Vol. 14 No. 5 Sep-Oct 1995","20"
    "Chips & Sparks: Safe Outlets","Greg Locati","General Machining Knowledge","HSM Vol. 14 No. 5 Sep-Oct 1995","20"
    "Chips & Sparks: When You Are Without a Tool Post Grinder","Chad Godeke","Miscellaneous","HSM Vol. 14 No. 5 Sep-Oct 1995","20"
    "Maverick Engine - Part I","Philip Duclos","Engines","HSM Vol. 14 No. 5 Sep-Oct 1995","22"
    "Building the Shop","Corrine Hummel","General Machining Knowledge","HSM Vol. 14 No. 5 Sep-Oct 1995","28"
    "Electrical Discharge Machining - Removing Metal By Spark Erosion: Part III - The Stepper Motor Logic and Driver Board","Robert P. Langlois","Machining Accessories","HSM Vol. 14 No. 5 Sep-Oct 1995","34"
    "How to Make a Skeleton Wall Clock - Part XII","W. R. Smith","Clocks","HSM Vol. 14 No. 5 Sep-Oct 1995","44"
    "The Micro Machinist: A Compact Boring Head - Part II","Rudy Kouhoupt","Machining Accessories","HSM Vol. 14 No. 5 Sep-Oct 1995","51"
    "Drill Press Accessories: Homemade Counterbores","Alan Douglas","Machining Accessories","HSM Vol. 14 No. 5 Sep-Oct 1995","54"
    "From the Scrapbox: Homemade Counterbores","Frank A. McLean","Machining Accessories","HSM Vol. 14 No. 5 Sep-Oct 1995","54"
    "Specialty Clamping Devices - Part IV","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 14 No. 5 Sep-Oct 1995","56"
    "Chips & Sparks: Easy Way to Cut Metric Threads","Jack R. Lind","Techniques","HSM Vol. 14 No. 6 Nov-Dec 1995","24"
    "Practical Ideas... for Metalworking Operations, Tooling, and Maintenance","Joe Rice","Hobby Community","HSM Vol. 14 No. 6 Nov-Dec 1995","25"
    "Nonmetallic Tooling Alternative","Edward G. Hoffman","Hobby Community","HSM Vol. 14 No. 6 Nov-Dec 1995","26"
    "Mill-drill Adventures - Part IV","D. E. Johnson","Machining Accessories","HSM Vol. 14 No. 6 Nov-Dec 1995","28"
    "Need A Lift?","Ray F. Wagner","Shop Accessories","HSM Vol. 14 No. 6 Nov-Dec 1995","33"
    "Electrical Discharge Machining - Removing Metal By Spark Erosion: Part IV Installing the Stepper Motor Board & Stepper Motor","Robert P. Langlois","Machining Accessories","HSM Vol. 14 No. 6 Nov-Dec 1995","34"
    "Maverick Engine - Part II","Philip Duclos","Engines","HSM Vol. 14 No. 6 Nov-Dec 1995","40"
    "Drill Press Accessories: A Simple Tapping Guide","Alan Douglas","Machining Accessories","HSM Vol. 14 No. 6 Nov-Dec 1995","47"
    "A Simple Tapping Guide","Phil Huffman","Machining Accessories","HSM Vol. 14 No. 6 Nov-Dec 1995","47"
    "Silver Soldering Fundamentals","George W. Genevro","Techniques","HSM Vol. 14 No. 6 Nov-Dec 1995","48"
    "Electric Motors for Stationary Power Tools","Alan Douglas","Motors","HSM Vol. 14 No. 6 Nov-Dec 1995","52"
    "The Micro Machinist: A Compact Boring Head - Part III","Rudy Kouhoupt","Machining Accessories","HSM Vol. 14 No. 6 Nov-Dec 1995","56"
    "Locating Pins - Part I","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 14 No. 6 Nov-Dec 1995","60"
    "From the Scrapbox: Cloche Hoops","Frank A. McLean","Techniques","HSM Vol. 14 No. 6 Nov-Dec 1995","62"
    "Chips & Sparks: Mill/drill Tips","David Eisler","Techniques","HSM Vol. 15 No. 1 Jan-Feb 1996","21"
    "Emco Maier D1-4 Cam Lock Fixture Plate","David Lindquist","Hobby Community","HSM Vol. 15 No. 1 Jan-Feb 1996","22"
    "FlexArm System","Edward G. Hoffman","Hobby Community","HSM Vol. 15 No. 1 Jan-Feb 1996","23"
    "Mill-drill Adventures - Part V - A Power Feed for the Main Table and a Rotary Table","D. E. Johnson","Machining Accessories","HSM Vol. 15 No. 1 Jan-Feb 1996","26"
    "Engineering Plastics","Thomas W. Dowling, III","Techniques","HSM Vol. 15 No. 1 Jan-Feb 1996","33"
    "Electrical Discharge Machining - Removing Metal By Spark Erosion - Part V - The Head and EDM Operation","Robert P. Langlois","Machining Accessories","HSM Vol. 15 No. 1 Jan-Feb 1996","34"
    "Maverick Engine - Part III","Philip Duclos","Engines","HSM Vol. 15 No. 1 Jan-Feb 1996","44"
    "Lathe Tips","Edward P. Stone","Techniques","HSM Vol. 15 No. 1 Jan-Feb 1996","50"
    "The Micro Machinist: Little Job Cement Mixer - Part I","Rudy Kouhoupt","Projects","HSM Vol. 15 No. 1 Jan-Feb 1996","54"
    "From the Scrapbox: Cleaning a Universal Chuck","Frank A. McLean","Techniques","HSM Vol. 15 No. 1 Jan-Feb 1996","57"
    "Locating Pins - Part II","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 15 No. 1 Jan-Feb 1996","62"
    "Chips & Sparks: Advantage of Three-phase","Dick French","Motors","HSM Vol. 15 No. 2 Mar-Apr 1996","19"
    "Chips & Sparks: Hacksaw Cuts Simplified","Fred E. Wilder","Techniques","HSM Vol. 15 No. 2 Mar-Apr 1996","19"
    "Chips & Sparks: No More Shocks","David C. Blocker","Techniques","HSM Vol. 15 No. 2 Mar-Apr 1996","19"
    "Chips & Sparks: Substitute Tailstock Center","Thomas LaMance","Machining Accessories","HSM Vol. 15 No. 2 Mar-Apr 1996","19"
    "Ornamental Turning Lathe","Guy Lautard","Hobby Community","HSM Vol. 15 No. 2 Mar-Apr 1996","20"
    "Adapting the Sherline for Wheel Cutting and Pinion Making - Part I","W. R. Smith","Techniques","HSM Vol. 15 No. 2 Mar-Apr 1996","24"
    "Mill-drill Adventures - Part VI - A Power Feed for the Main Table and a Rotary Table continued","D. E. Johnson","Machining Accessories","HSM Vol. 15 No. 2 Mar-Apr 1996","32"
    "Electrical Discharge Machining - Removing Metal By Spark Erosion - Part VI - Other Odds and Ends","Robert P. Langlois","Machining Accessories","HSM Vol. 15 No. 2 Mar-Apr 1996","37"
    "Maverick Engine - Part IV","Philip Duclos","Engines","HSM Vol. 15 No. 2 Mar-Apr 1996","42"
    "A Small Shop Butt Welder","Wolfgang F. Habicher","Welding/Foundry/Forging","HSM Vol. 15 No. 2 Mar-Apr 1996","48"
    "The Micro Machinist: Little Job Cement Mixer - Part II","Rudy Kouhoupt","Projects","HSM Vol. 15 No. 2 Mar-Apr 1996","50"
    "Locating Pins - Part III","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 15 No. 2 Mar-Apr 1996","54"
    "From the Scrapbox: How to Set Up and Use a Drill Grinding Attachment","Frank A. McLean","Shop Accessories","HSM Vol. 15 No. 2 Mar-Apr 1996","57"
    "Building Phil Duclos' Model Maker's Dividing Head","Marsh Collins","Machining Accessories","HSM Vol. 15 No. 3 May-Jun 1996","16"
    "An American's View of the English Wheel","Guy Lautard","Hobby Community","HSM Vol. 15 No. 3 May-Jun 1996","20"
    "Bedding, Scoping, and Crowning the Remington 700","Guy Lautard","Hobby Community","HSM Vol. 15 No. 3 May-Jun 1996","20"
    "Correcting bolt Lug Engagement and Excess Headspace","Guy Lautard","Hobby Community","HSM Vol. 15 No. 3 May-Jun 1996","20"
    "Edge those Panels","Guy Lautard","Hobby Community","HSM Vol. 15 No. 3 May-Jun 1996","20"
    "Truing Your Action and Installing a New Barrel","Guy Lautard","Hobby Community","HSM Vol. 15 No. 3 May-Jun 1996","20"
    "The Micro Machinist: Using the Diamond Toolholder","Rudy Kouhoupt","Techniques","HSM Vol. 15 No. 3 May-Jun 1996","24"
    "The How and Why of Tangential Cutting","Desmond Burke","Techniques","HSM Vol. 15 No. 3 May-Jun 1996","28"
    "A Sliding Bevel Gage with Protractor","Ted Wright","Measuring & Layout","HSM Vol. 15 No. 3 May-Jun 1996","31"
    "Adapting the Sherline for Wheel Cutting and Pinion Making - Part II","W. R. Smith","Techniques","HSM Vol. 15 No. 3 May-Jun 1996","36"
    "Remote Switch for the Mill","C. O. Voss","Machining Accessories","HSM Vol. 15 No. 3 May-Jun 1996","49"
    "Variable Speed DC Motor for the Home Shop","Charles Eyer","Motors","HSM Vol. 15 No. 3 May-Jun 1996","50"
    "The Micro Machinist: Little Job Cement Mixer - Part III","Rudy Kouhoupt","Projects","HSM Vol. 15 No. 3 May-Jun 1996","55"
    "From the Scrapbox: A Trepanning Tool","Frank A. McLean","Machining Accessories","HSM Vol. 15 No. 3 May-Jun 1996","58"
    "Fixturing With Collets - Part I","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 15 No. 3 May-Jun 1996","60"
    "Chips & Sparks: Long Story Shortened","Steven G. Whipple","Techniques","HSM Vol. 15 No. 4 Jul-Aug 1996","20"
    "Three-phase Idler Flywheel","Robin Houseman","Machining Accessories","HSM Vol. 15 No. 4 Jul-Aug 1996","20"
    "Lathe Handles","Pierce Raubach","Machining Accessories","HSM Vol. 15 No. 4 Jul-Aug 1996","21"
    "Takang Model 1760G Lathe","John Benjamin","Hobby Community","HSM Vol. 15 No. 4 Jul-Aug 1996","22"
    "Designing Cost-Efficient Mechanisms","David Joly","Techniques","HSM Vol. 15 No. 4 Jul-Aug 1996","23"
    "A Bit of Inspiration: The Work of John Crunkleton","John Crunkleton","Hobby Community","HSM Vol. 15 No. 4 Jul-Aug 1996","24"
    "Mill-drill Adventures - Part VII - Keeping Track of the Cutting Tool and Table Positions","D. E. Johnson","Machining Accessories","HSM Vol. 15 No. 4 Jul-Aug 1996","30"
    "A Quick-release T-rest for the Sherline Lathe","W. R. Smith","Machining Accessories","HSM Vol. 15 No. 4 Jul-Aug 1996","36"
    "Table Stop","James Madison","Machining Accessories","HSM Vol. 15 No. 4 Jul-Aug 1996","44"
    "Internal Spindle Stop","Billy J. Blackmon","Machining Accessories","HSM Vol. 15 No. 4 Jul-Aug 1996","46"
    "An Indicator Stand","Earl L. Bower","Machining Accessories","HSM Vol. 15 No. 4 Jul-Aug 1996","48"
    "Stuck Chucks, One-more-time, Didactic #17","Henry J. Kratt","Techniques","HSM Vol. 15 No. 4 Jul-Aug 1996","49"
    "Sharpening Tungsten Carbide Drills","Walt Netzel","Miscellaneous","HSM Vol. 15 No. 4 Jul-Aug 1996","50"
    "The Micro Machinist: Little Job Cement Mixer - Part IV","Rudy Kouhoupt","Projects","HSM Vol. 15 No. 4 Jul-Aug 1996","51"
    "A Gunsmith's Workbench, German Silver Escutcheons","Laurie Morrow","Gunsmithing","HSM Vol. 15 No. 4 Jul-Aug 1996","52"
    "From the Scrapbox: A Taig Lathe Tool Rest","Frank A. McLean","Machining Accessories","HSM Vol. 15 No. 4 Jul-Aug 1996","54"
    "The Proper Use of Diamond Dressers","John Bochert","Techniques","HSM Vol. 15 No. 4 Jul-Aug 1996","56"
    "Carbide Inserts","Jeff Witherow","Machining Accessories","HSM Vol. 15 No. 4 Jul-Aug 1996","58"
    "Fixturing With Collets - Part II","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 15 No. 4 Jul-Aug 1996","60"
    "Chips & Sparks: Working in the Dark","Werner W. Dolling","Techniques","HSM Vol. 15 No. 4 Jul-Aug 1996","67"
    "Chips & Sparks: Machine Mobility","Norman A. Vordahl","Techniques","HSM Vol. 15 No. 5 Sep-Oct 1996","20"
    "Chips & Sparks: Made in the Shade","Pete Stanaitis","Techniques","HSM Vol. 15 No. 5 Sep-Oct 1996","21"
    "Chips & Sparks: Milling a Flat","David C. Blocker","Techniques","HSM Vol. 15 No. 5 Sep-Oct 1996","21"
    "Chips & Sparks: Magnetic Base Indicator Mount","M. O. Davis","Machining Accessories","HSM Vol. 15 No. 5 Sep-Oct 1996","22"
    "Chips & Sparks: Tighten the Spindle Pulley","Art Rachunas","Techniques","HSM Vol. 15 No. 5 Sep-Oct 1996","22"
    "Almost a Product Review","Peter Nolan","Hobby Community","HSM Vol. 15 No. 5 Sep-Oct 1996","23"
    "Hot Bluing Steel","Steve Acker","Techniques","HSM Vol. 15 No. 5 Sep-Oct 1996","28"
    "Chips & Sparks: Setting Up Work in the Lathe","Peter J. Willox","Techniques","HSM Vol. 15 No. 5 Sep-Oct 1996","33"
    "Cutting Steel with a Circular Saw Blade","Steve Acker","Techniques","HSM Vol. 15 No. 5 Sep-Oct 1996","33"
    "An Elevated or Auxiliary Lathe Spindle - Part I","Frank A. McLean","Machining Accessories","HSM Vol. 15 No. 5 Sep-Oct 1996","34"
    "The Walking Staff","Don Titus","Projects","HSM Vol. 15 No. 5 Sep-Oct 1996","43"
    "A Steam/Air Engine for Fun","George Kerekgyarto","Engines","HSM Vol. 15 No. 5 Sep-Oct 1996","48"
    "From the Scrapbox: How to Make a Chuck Backplate","Frank A. McLean","Machining Accessories","HSM Vol. 15 No. 5 Sep-Oct 1996","52"
    "A Time for Reflection","Frank A. McLean","Techniques","HSM Vol. 15 No. 5 Sep-Oct 1996","56"
    "The Micro Machinist: Make Your Own Lathe Collets - Part I","Rudy Kouhoupt","Machining Accessories","HSM Vol. 15 No. 5 Sep-Oct 1996","58"
    "Machining on the Internet","J. H. Mendum","General Machining Knowledge","HSM Vol. 15 No. 5 Sep-Oct 1996","62"
    "Chips & Sparks: Change Gears","P. Isaac","Techniques","HSM Vol. 15 No. 5 Sep-Oct 1996","63"
    "Chips & Sparks: Holding Small Threading Dies","Charles Brown","Techniques","HSM Vol. 15 No. 6 Nov-Dec 1996","20"
    "The Micro Machinist: A Stirling-powered Tractor - Part I","Rudy Kouhoupt","Engines","HSM Vol. 15 No. 6 Nov-Dec 1996","24"
    "An Elevated or Auxiliary Lathe Spindle - Part II","Frank A. McLean","Machining Accessories","HSM Vol. 15 No. 6 Nov-Dec 1996","32"
    "Cylinders and Pistons for Two-stroke Cycle Model Engineers","George W. Genevro","Engines","HSM Vol. 15 No. 6 Nov-Dec 1996","38"
    "Get a Handle On Your Lathe","John B. Gascoyne","Machining Accessories","HSM Vol. 15 No. 6 Nov-Dec 1996","46"
    "Variations on a Whatzit","Ken Hollenbeck","Engines","HSM Vol. 15 No. 6 Nov-Dec 1996","48"
    "The Rebirth of a Model C South Bend Lathe","Douglas Graham","Machine Tools","HSM Vol. 15 No. 6 Nov-Dec 1996","49"
    "A Pseudo Drawbar for the Tailstock","Phil Nyman","Machining Accessories","HSM Vol. 15 No. 6 Nov-Dec 1996","52"
    "Atlas Tailstock Modification","Bruce Jones","Machining Accessories","HSM Vol. 15 No. 6 Nov-Dec 1996","55"
    "The Micro Machinist: make Your Own Lathe Collets - Part II","Rudy Kouhoupt","Machining Accessories","HSM Vol. 15 No. 6 Nov-Dec 1996","56"
    "From the Scrapbox: A Spur Center for Turning Wood","Frank A. McLean","Machining Accessories","HSM Vol. 15 No. 6 Nov-Dec 1996","59"
    "Fixturing With Collets - Part III","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 15 No. 6 Nov-Dec 1996","62"
    "Chips & Sparks: A Three-jaw Chuck Can Be Accurate","Thomas J. Doolin","Techniques","HSM Vol. 16 No. 1 Jan-Feb 1997","22"
    "Chips & Sparks: Tapping a Channel-shaped Part","Leroy C. Bayliss","Techniques","HSM Vol. 16 No. 1 Jan-Feb 1997","22"
    "Chips & Sparks: Band Saw Improvement","Bryan E. Talbot","Techniques","HSM Vol. 16 No. 1 Jan-Feb 1997","23"
    "Chips & Sparks: Filling a Boring Bar","Ed Hughes","Techniques","HSM Vol. 16 No. 1 Jan-Feb 1997","23"
    "Chips & Sparks: Threading On a Lathe","Robert Stellhorn","Techniques","HSM Vol. 16 No. 1 Jan-Feb 1997","23"
    "A 5C Collet Adapter for the Lathe","D. E. Johnson","Machining Accessories","HSM Vol. 16 No. 1 Jan-Feb 1997","26"
    "A Low-cost Bead Blaster","Steve Acker","Shop Accessories","HSM Vol. 16 No. 1 Jan-Feb 1997","36"
    "A Stirling-powered Tractor - Part II - Rear Wheel Assembly","Rudy Kouhoupt","Engines","HSM Vol. 16 No. 1 Jan-Feb 1997","44"
    "From the Scrapbox: Tool Rests for Turning Wood","Frank A. McLean","Machining Accessories","HSM Vol. 16 No. 1 Jan-Feb 1997","48"
    "The Micro Machinist: Mounting Small Chucks and Faceplates","Rudy Kouhoupt","Techniques","HSM Vol. 16 No. 1 Jan-Feb 1997","53"
    "You Can Find It","Dana Martin Batory","Hobby Community","HSM Vol. 16 No. 1 Jan-Feb 1997","56"
    "The Wheel You Can't Live Without","Walter B. Mueller","Machining Accessories","HSM Vol. 16 No. 1 Jan-Feb 1997","58"
    "Supplement to the Home Shop Motor Controller","Charles Eyer","Motors","HSM Vol. 16 No. 1 Jan-Feb 1997","60"
    "How I Almost Became a Millionaire","Jesse Livingston","Techniques","HSM Vol. 16 No. 1 Jan-Feb 1997","62"
    "Fixturing With Collets - Part IV","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 16 No. 1 Jan-Feb 1997","63"
    "A Stirling-powered Tractor - Part III - Gear Details and Displacer Cylinder","Rudy Kouhoupt","Engines","HSM Vol. 16 No. 2 Mar-Apr 1997","28"
    "A Piloted Tap Guide Wrench","W. A. Lincoln","Machining Accessories","HSM Vol. 16 No. 2 Mar-Apr 1997","34"
    "Mill-drill Spindle Lock","Rudi Legname","Machining Accessories","HSM Vol. 16 No. 2 Mar-Apr 1997","39"
    "You Can Do It","Spencer Schonher","Techniques","HSM Vol. 16 No. 2 Mar-Apr 1997","40"
    "The Universal Plain Dividing Head - Part I","Rich Kuzmack","Machining Accessories","HSM Vol. 16 No. 2 Mar-Apr 1997","41"
    "A Faceplate Toolholder","D. M. Thomson","Machining Accessories","HSM Vol. 16 No. 2 Mar-Apr 1997","45"
    "The Micro Machinist: Reconditioning an Atlas Milling Machine - Part I","Rudy Kouhoupt","Machine Tools","HSM Vol. 16 No. 2 Mar-Apr 1997","46"
    "Smithy CB 1220 XL","Lon Haney","Hobby Community","HSM Vol. 16 No. 2 Mar-Apr 1997","49"
    "A Bit of Inspiration: Machining Skills Pay Off","William H. Ganoe","Techniques","HSM Vol. 16 No. 2 Mar-Apr 1997","52"
    "Woodworking in the Machine shop","John F. Ernest","Techniques","HSM Vol. 16 No. 2 Mar-Apr 1997","54"
    "From the Scrapbox: How to Make a Tapered End Mill","Frank A. McLean","Machining Accessories","HSM Vol. 16 No. 2 Mar-Apr 1997","56"
    "Fixturing With Collets - Part V","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 16 No. 2 Mar-Apr 1997","58"
    "Wheel Cutting, Pinion Making & Depthing","Guy Lautard","Miscellaneous","HSM Vol. 16 No. 3 May-Jun 1997","22"
    "How to Make a Skeleton Wall Clock","Guy Lautard","Clocks","HSM Vol. 16 No. 3 May-Jun 1997","24"
    "Chips & Sparks: Simplest Phase Converter","Thomas Grimes","Miscellaneous","HSM Vol. 16 No. 3 May-Jun 1997","25"
    "Chips & Sparks: Spindle Power for the Unimat","Mark Gallagher","Motors","HSM Vol. 16 No. 3 May-Jun 1997","25"
    "A Victorian Engine - Part I","Philip Duclos","Engines","HSM Vol. 16 No. 3 May-Jun 1997","28"
    "The Universal Plain Dividing Head - Part II","Rich Kuzmack","Machining Accessories","HSM Vol. 16 No. 3 May-Jun 1997","37"
    "A Stirling-powered Tractor - Part IV - Engine","Rudy Kouhoupt","Engines","HSM Vol. 16 No. 3 May-Jun 1997","44"
    "From the Scrapbox: A Few Thoughts on Shapers","Frank A. McLean","Techniques","HSM Vol. 16 No. 3 May-Jun 1997","51"
    "The Micro Machinist: Reconditioning an Atlas Milling Machine - Part II","Rudy Kouhoupt","Machine Tools","HSM Vol. 16 No. 3 May-Jun 1997","58"
    "Fixturing With Collets - Part VI","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 16 No. 3 May-Jun 1997","62"
    "Chips & Sparks: A Fast Dressing of Band Saw Welds","Thomas J. Doolin","Techniques","HSM Vol. 16 No. 4 Jul-Aug 1997","25"
    "Chips & Sparks: Sharpen for Brass Cutting","Charlie Blackburn","Techniques","HSM Vol. 16 No. 4 Jul-Aug 1997","25"
    ""950 Bead Blaster from Skat Blast Manson Rifle Receiver Blueprinting Tools"","Steve Acker","Gunsmithing","HSM Vol. 16 No. 4 Jul-Aug 1997","26"
    "Darex Corporation's Drill Doctor","David Joly","Hobby Community","HSM Vol. 16 No. 4 Jul-Aug 1997","28"
    "Mill-drill Adventures: New Handwheels and Leadscrew Bearings Fix Backlash and Rattles - Part VIII","D. E. Johnson","Machining Accessories","HSM Vol. 16 No. 4 Jul-Aug 1997","32"
    "Adjustable Lathe Stop for Under $15","Don Titus","Machining Accessories","HSM Vol. 16 No. 4 Jul-Aug 1997","37"
    "Basic Industrial Electrical Control","Harold G. Cohon","Miscellaneous","HSM Vol. 16 No. 4 Jul-Aug 1997","40"
    "A Victorian Engine - Part II","Philip Duclos","Engines","HSM Vol. 16 No. 4 Jul-Aug 1997","42"
    "The Universal Plain Dividing Head - Part III","Rich Kuzmack","Machining Accessories","HSM Vol. 16 No. 4 Jul-Aug 1997","48"
    "Screw Heads and Screwdrivers","Jacob Schulzinger","Hand Tools","HSM Vol. 16 No. 4 Jul-Aug 1997","52"
    "A Stirling-powered Tractor - Part V - Gear Engagement and Footplate","Rudy Kouhoupt","Engines","HSM Vol. 16 No. 4 Jul-Aug 1997","54"
    "Grinding Tool Bits for a Smooth Cut","Frank E. Burns","Techniques","HSM Vol. 16 No. 4 Jul-Aug 1997","58"
    "The Micro Machinist: Reconditioning an Atlas Milling Machine - Part III","Rudy Kouhoupt","Machine Tools","HSM Vol. 16 No. 4 Jul-Aug 1997","60"
    "Fixturing With Collets - Part VII","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 16 No. 4 Jul-Aug 1997","63"
    "Chips & Sparks: Machinist Uses for Seemingly Unrelated Products","Thomas J. Doolin","Techniques","HSM Vol. 16 No. 5 Sep-Oct 1997","22"
    "Chips & Sparks: Water-cooling Torches","Bill Julian","Techniques","HSM Vol. 16 No. 5 Sep-Oct 1997","22"
    "A Fine Feed Attachment for a Vertical Mill - Part I","G. Wadham","Machining Accessories","HSM Vol. 16 No. 5 Sep-Oct 1997","24"
    "A Victorian Engine - Part III","Philip Duclos","Engines","HSM Vol. 16 No. 5 Sep-Oct 1997","31"
    "Mill-drill Adventures: New Handwheels and Leadscrew Bearings Fix Backlash and Rattles - Part IX","D. E. Johnson","Machining Accessories","HSM Vol. 16 No. 5 Sep-Oct 1997","40"
    "Band Saw Fixture","D. A. Drayson","Jigs & Fixtures","HSM Vol. 16 No. 5 Sep-Oct 1997","46"
    "A Stirling-powered Tractor - Part VI - Furnace","Rudy Kouhoupt","Engines","HSM Vol. 16 No. 5 Sep-Oct 1997","47"
    "The Universal Plain Dividing Head - Part IV","Rich Kuzmack","Machining Accessories","HSM Vol. 16 No. 5 Sep-Oct 1997","50"
    "A Rigid Tool Bit Clamp","George W. Genevro","Machining Accessories","HSM Vol. 16 No. 5 Sep-Oct 1997","54"
    "My Own Right Time","David Joly","Hobby Community","HSM Vol. 16 No. 5 Sep-Oct 1997","55"
    "The Micro Machinist: Making Accurate Squares","Rudy Kouhoupt","Machining Accessories","HSM Vol. 16 No. 5 Sep-Oct 1997","56"
    "Another Mill-drill Adventure","George E. Hoke","Techniques","HSM Vol. 16 No. 5 Sep-Oct 1997","58"
    "A Test-tube Stirling Engine","David O'Neil","Engines","HSM Vol. 16 No. 5 Sep-Oct 1997","61"
    "Fixturing With Collets - Part VIII","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 16 No. 5 Sep-Oct 1997","62"
    "Grizzly G4000 Lathe","Don Perkins","Hobby Community","HSM Vol. 16 No. 6 Nov-Dec 1997","17"
    "Machine Shop Crossword Puzzle","James R. Instone","Miscellaneous","HSM Vol. 16 No. 6 Nov-Dec 1997","20"
    "Graver Making & Hand Turning for Clockmakers & Modelmakers","Guy Lautard","Hobby Community","HSM Vol. 16 No. 6 Nov-Dec 1997","22"
    "Scrape & Shape - Part I","Stephen M. Thomas","Techniques","HSM Vol. 16 No. 6 Nov-Dec 1997","26"
    "A Victorian Engine - Part IV","Philip Duclos","Engines","HSM Vol. 16 No. 6 Nov-Dec 1997","40"
    "A Stirling-powered Tractor - Part VII - Cooling System and Fuel Tank","Rudy Kouhoupt","Engines","HSM Vol. 16 No. 6 Nov-Dec 1997","46"
    "Balanced Ball Handles","Terry Sexton","Techniques","HSM Vol. 16 No. 6 Nov-Dec 1997","50"
    "A Useful, High-quality Magnifying Glass","Guy Lautard","Hand Tools","HSM Vol. 16 No. 6 Nov-Dec 1997","55"
    "Turning Your Vise Into a Universal Workholding System - Part I","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 16 No. 6 Nov-Dec 1997","60"
    "The Micro Machinist: Making an Angle Plate","Rudy Kouhoupt","Machining Accessories","HSM Vol. 16 No. 6 Nov-Dec 1997","63"
    "Chips & Sparks: Computer-aided Dividing Plates","Charlie R. Foster","Machining Accessories","HSM Vol. 17 No. 1 Jan-Feb 1998","24"
    "Chips & Sparks: Ultra Precision Parallel Set","James W. Hauser","Measuring & Layout","HSM Vol. 17 No. 1 Jan-Feb 1998","24"
    "Machine Shop Crossword Puzzle","James R. Instone","Miscellaneous","HSM Vol. 17 No. 1 Jan-Feb 1998","25"
    "Building The Edge Master Lawn Edging Machine - Part I","D. E. Johnson","Projects","HSM Vol. 17 No. 1 Jan-Feb 1998","28"
    "Scrape & Shape - Part II","Stephen M. Thomas","Techniques","HSM Vol. 17 No. 1 Jan-Feb 1998","35"
    "Telegraph Key - Part I","Doug Ripka","Miscellaneous","HSM Vol. 17 No. 1 Jan-Feb 1998","42"
    "Drawbar Knocker","Norm Wells","Machining Accessories","HSM Vol. 17 No. 1 Jan-Feb 1998","47"
    "A Victorian Engine - Part V","Philip Duclos","Engines","HSM Vol. 17 No. 1 Jan-Feb 1998","48"
    "The Old Compound Indexing Table Reworked","Rich Kuzmack","General Machining Knowledge","HSM Vol. 17 No. 1 Jan-Feb 1998","54"
    "PRIME","Joe Rice","Hobby Community","HSM Vol. 17 No. 1 Jan-Feb 1998","56"
    "The Micro Machinist: Making a Clapper","Rudy Kouhoupt","Machining Accessories","HSM Vol. 17 No. 1 Jan-Feb 1998","60"
    "Indexing Parts in a Set","Ronald G. Darner","Techniques","HSM Vol. 17 No. 1 Jan-Feb 1998","63"
    "Turning Your Vise Into a Universal Workholding System - Part II","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 17 No. 1 Jan-Feb 1998","64"
    "Headstock angle Adjuster for the Sherline 4000 Lathe","John H. Denning","Machining Accessories","HSM Vol. 17 No. 1 Jan-Feb 1998","66"
    "Chips & Sparks: All-around Access","John B. Gascoyne","Techniques","HSM Vol. 17 No. 2 Mar-Apr 1998","22"
    "Chips & Sparks: Hacksaw Cuts","John Grass","Techniques","HSM Vol. 17 No. 2 Mar-Apr 1998","22"
    "John Deere Model E","Joe Rice","Hobby Community","HSM Vol. 17 No. 2 Mar-Apr 1998","24"
    "Math Solutions for Your Computer","Edward G. Hoffman","Hobby Community","HSM Vol. 17 No. 2 Mar-Apr 1998","25"
    "Building The Edge Master Lawn Edging Machine - Part II","D. E. Johnson","Projects","HSM Vol. 17 No. 2 Mar-Apr 1998","30"
    "Telegraph Key - Part II","Doug Ripka","Miscellaneous","HSM Vol. 17 No. 2 Mar-Apr 1998","36"
    "Scrape & Shape - Part III","Stephen M. Thomas","Techniques","HSM Vol. 17 No. 2 Mar-Apr 1998","41"
    "The Micro Machinist: Build & Use an Adjustable Angle Plate - Part I","Rudy Kouhoupt","Machining Accessories","HSM Vol. 17 No. 2 Mar-Apr 1998","48"
    "Copper and Its Alloys","George W. Genevro","General Machining Knowledge","HSM Vol. 17 No. 2 Mar-Apr 1998","51"
    "Modify Your Bead Blast Gun","Paul J. Holm","Techniques","HSM Vol. 17 No. 2 Mar-Apr 1998","60"
    "Turning Your Vise Into a Universal Workholding System - Part III","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 17 No. 2 Mar-Apr 1998","62"
    "Chips & Sparks: Parting Off","John Grass","Techniques","HSM Vol. 17 No. 3 May-Jun 1998","22"
    "Chips & Sparks: Using the Needle Point Shaft in a Wiggler Set","Leroy C. Bayliss","Techniques","HSM Vol. 17 No. 3 May-Jun 1998","22"
    "A Filing Rest For The Sherline Lathe","W. R. Smith","Machining Accessories","HSM Vol. 17 No. 3 May-Jun 1998","26"
    "Scrape & Shape - Part IV","Stephen M. Thomas","Techniques","HSM Vol. 17 No. 3 May-Jun 1998","35"
    "The Micro Machinist: Build & Use an Adjustable Angle Plate - Part II","Rudy Kouhoupt","Machining Accessories","HSM Vol. 17 No. 3 May-Jun 1998","42"
    "Additions to the Quorn tool and Cutter Grinder - Part I","Walter B. Mueller","Shop Machinery","HSM Vol. 17 No. 3 May-Jun 1998","46"
    "Building The Edge Master Lawn Edging Machine - Part III","D. E. Johnson","Projects","HSM Vol. 17 No. 3 May-Jun 1998","54"
    "Machine Shop Crossword Puzzle","James R. Instone","Miscellaneous","HSM Vol. 17 No. 3 May-Jun 1998","59"
    "Turning Your Vise Into a Universal Workholding System - Part IV","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 17 No. 3 May-Jun 1998","60"
    "A Mill-drill Modification","William K. Schaeffer","Machining Accessories","HSM Vol. 17 No. 3 May-Jun 1998","62"
    "A Grease Adapter for the South Bend","Jack R. Thompson","Machine Modifications","HSM Vol. 17 No. 3 May-Jun 1998","63"
    "Offenhauser, the Legendary American Racing Machine and The Men Who Built It","Joe Rice","Hobby Community","HSM Vol. 17 No. 4 Jul-Aug 1998","23"
    "Chips & Sparks: A Few Good Hints","C. Lawrence Haines","Techniques","HSM Vol. 17 No. 4 Jul-Aug 1998","24"
    "Chips & Sparks: A Floating Drive","Thomas LaMance","Machining Accessories","HSM Vol. 17 No. 4 Jul-Aug 1998","24"
    "Chips & Sparks: Found Materials","Gene Switzer","Techniques","HSM Vol. 17 No. 4 Jul-Aug 1998","24"
    "Chips & Sparks: Sharpening Lathe Tools","Charles H. Loer","Techniques","HSM Vol. 17 No. 4 Jul-Aug 1998","24"
    "Machine Shop Crossword Puzzle","James R. Instone","Miscellaneous","HSM Vol. 17 No. 4 Jul-Aug 1998","25"
    "Shooting Star Technology CBX Digital Readout","John Graff","Hobby Community","HSM Vol. 17 No. 4 Jul-Aug 1998","26"
    "Build Your Own Shaper - Part I","Marsh Collins","Machine Tools","HSM Vol. 17 No. 4 Jul-Aug 1998","30"
    "Scrape & Shape - Part V","Stephen M. Thomas","Techniques","HSM Vol. 17 No. 4 Jul-Aug 1998","38"
    "Pulley Arrangement vs. Spindle Speed","Jim Reynolds","Techniques","HSM Vol. 17 No. 4 Jul-Aug 1998","44"
    "Additions to the Quorn tool and Cutter Grinder - Part II","Walter B. Mueller","Shop Machinery","HSM Vol. 17 No. 4 Jul-Aug 1998","46"
    "Building The Edge Master Lawn Edging Machine - Part IV","D. E. Johnson","Projects","HSM Vol. 17 No. 4 Jul-Aug 1998","53"
    "A Wooden Work Support in the Mill","Corrine Hummel","Machining Accessories","HSM Vol. 17 No. 4 Jul-Aug 1998","58"
    "The Micro Machinist: Build & Use an Adjustable Angle Plate - Part III","Rudy Kouhoupt","Machining Accessories","HSM Vol. 17 No. 4 Jul-Aug 1998","60"
    "Turning Your Vise Into a Universal Workholding System - Part V","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 17 No. 4 Jul-Aug 1998","63"
    "Chips & Sparks: Band Saw Blade Fixture","Ray Ashcraft","Jigs & Fixtures","HSM Vol. 17 No. 5 Sep-Oct 1998","24"
    "Machine Shop Crossword Puzzle","James R. Instone","Miscellaneous","HSM Vol. 17 No. 5 Sep-Oct 1998","24"
    "Thermal Dynamics Air Plasma Cutting System","James Hesse","Hobby Community","HSM Vol. 17 No. 5 Sep-Oct 1998","25"
    "A Saw Table for the Sherline Lathe","W. R. Smith","Machining Accessories","HSM Vol. 17 No. 5 Sep-Oct 1998","28"
    "The Erten Machining Center","Max Ben-Aaron","Machine Tools","HSM Vol. 17 No. 5 Sep-Oct 1998","33"
    "E-Z Bore","Donald Erickson","Machining Accessories","HSM Vol. 17 No. 5 Sep-Oct 1998","37"
    "A Mechanical Lift for a Drill Press Table","Robert Cortner","Machining Accessories","HSM Vol. 17 No. 5 Sep-Oct 1998","38"
    "Build Your Own Shaper - Part II","Marsh Collins","Machine Tools","HSM Vol. 17 No. 5 Sep-Oct 1998","40"
    "Building The Edge Master Lawn Edging Machine - Part V","D. E. Johnson","Projects","HSM Vol. 17 No. 5 Sep-Oct 1998","46"
    "Cabin Fever 1998","Joe Rice","Hobby Community","HSM Vol. 17 No. 5 Sep-Oct 1998","52"
    "Using a Computer to Draw Scales","James R. Instone","Techniques","HSM Vol. 17 No. 5 Sep-Oct 1998","56"
    "Magnetic Mandrel","Clayton Punshon","Machining Accessories","HSM Vol. 17 No. 5 Sep-Oct 1998","58"
    "The Micro Machinist: Indexing Centers - Part I","Rudy Kouhoupt","Machining Accessories","HSM Vol. 17 No. 5 Sep-Oct 1998","59"
    "Turning Your Vise Into a Universal Workholding System - Part VI","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 17 No. 5 Sep-Oct 1998","62"
    "Richlite Fibre Laminate","Edward G. Hoffman","Hobby Community","HSM Vol. 17 No. 6 Nov-Dec 1998","26"
    "Chips & Sparks: Peace and Quiet","Barry Sulkin","Techniques","HSM Vol. 17 No. 6 Nov-Dec 1998","27"
    "Mill-drill Adventures Indexing and Dividing","D. E. Johnson","Machining Accessories","HSM Vol. 17 No. 6 Nov-Dec 1998","28"
    "Gear Cutting on the Sherline Lathe - Part I - Configuring the Sherline","W. R. Smith","Techniques","HSM Vol. 17 No. 6 Nov-Dec 1998","34"
    "The Micro Machinist: Indexing Centers - Part II","Rudy Kouhoupt","Machining Accessories","HSM Vol. 17 No. 6 Nov-Dec 1998","42"
    "Quick Graduated Collars","Don Verdiani","Machine Tools","HSM Vol. 17 No. 6 Nov-Dec 1998","46"
    "Two-Speed Belt Transmission","Jack Butz","Techniques","HSM Vol. 17 No. 6 Nov-Dec 1998","48"
    "On Pumps and Pumping","Alberto Marx","Techniques","HSM Vol. 17 No. 6 Nov-Dec 1998","50"
    "PC Board Vise","Alan D. Rauscher","Shop Accessories","HSM Vol. 17 No. 6 Nov-Dec 1998","54"
    "Grizzly 8 Table Indexing Plates Summary","Clifton E. R. Lawson","Machining Accessories","HSM Vol. 17 No. 6 Nov-Dec 1998","58"
    "Troubleshooting Primary Reasons for Scrap","Robert L. Grady","Techniques","HSM Vol. 17 No. 6 Nov-Dec 1998","60"
    "Turning Your Vise Into a Universal Workholding System - Part VII","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 17 No. 6 Nov-Dec 1998","62"
    "1998 N.A.M.E.S. Exhibition","Joe Rice","Hobby Community","HSM Vol. 17 No. 6 Nov-Dec 1998","65"
    "Examining a Used Lathe and Mill","Clover McKinley","Hobby Community","HSM Vol. 18 No. 1 Jan-Feb 1999","27"
    "Tabletop Machining","Joe Rice","Hobby Community","HSM Vol. 18 No. 1 Jan-Feb 1999","27"
    "A Lathe Tool Post Grinder for Serious Grinding - Part I","D. E. Johnson","Machining Accessories","HSM Vol. 18 No. 1 Jan-Feb 1999","28"
    "Gear Cutting on the Sherline Lathe - Part II","W. R. Smith","Techniques","HSM Vol. 18 No. 1 Jan-Feb 1999","35"
    "The Micro Machinist: Indexing Centers - Part III","Rudy Kouhoupt","Machining Accessories","HSM Vol. 18 No. 1 Jan-Feb 1999","42"
    "Build Your Own Shaper - Part III","Marsh Collins","Machine Tools","HSM Vol. 18 No. 1 Jan-Feb 1999","46"
    "Welding Up a Meat Smoker","Steve Acker","Welding/Foundry/Forging","HSM Vol. 18 No. 1 Jan-Feb 1999","54"
    "Reducing Workholder Weight - Part I","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 18 No. 1 Jan-Feb 1999","62"
    "Machine Shop Crossword Puzzle","James R. Instone","Miscellaneous","HSM Vol. 18 No. 2 Mar-Apr 1999","26"
    "Chips & Sparks: Toolholder for a Lathe","Gene Switzer","Machining Accessories","HSM Vol. 18 No. 2 Mar-Apr 1999","27"
    "A Lathe Tool Post Grinder for Serious Grinding - Part II","D. E. Johnson","Machining Accessories","HSM Vol. 18 No. 2 Mar-Apr 1999","28"
    "Build Your Own Shaper - Part IV","Marsh Collins","Machine Tools","HSM Vol. 18 No. 2 Mar-Apr 1999","35"
    "Gear Cutting on the Sherline Lathe - Part III","W. R. Smith","Techniques","HSM Vol. 18 No. 2 Mar-Apr 1999","42"
    "Thin Sheet Filing Fixture","Ted Wright","Jigs & Fixtures","HSM Vol. 18 No. 2 Mar-Apr 1999","48"
    "Understanding Abrasives - Part I","George W. Genevro","General Machining Knowledge","HSM Vol. 18 No. 2 Mar-Apr 1999","50"
    "Tale of a Jet GHB Gap Bed Lathe","Patrick Tooke","Techniques","HSM Vol. 18 No. 2 Mar-Apr 1999","54"
    "The Micro Machinist: A Mechanical Revolutions Counter - Part I","Rudy Kouhoupt","Machining Accessories","HSM Vol. 18 No. 2 Mar-Apr 1999","56"
    "Reducing Workholder Weight - Part II","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 18 No. 2 Mar-Apr 1999","60"
    "Brown & Sharpe Digital Electronic Caliper","Edward G. Hoffman","Hobby Community","HSM Vol. 18 No. 3 May-Jun 1999","8"
    "Kroy Light Table","Edward G. Hoffman","Miscellaneous","HSM Vol. 18 No. 3 May-Jun 1999","8"
    "Q & A","Lynn Everett","General Machining Knowledge","HSM Vol. 18 No. 3 May-Jun 1999","10"
    "Q & A","Rudy Kouhoupt","Techniques","HSM Vol. 18 No. 3 May-Jun 1999","10"
    "Making An Eight Day Longcase Clock - Timmins","Clover McKinley","Hobby Community","HSM Vol. 18 No. 3 May-Jun 1999","13"
    "Sheetmetal Fabrication: Sheetmetal Layout - Part IV","Richard J. Loescher","Miscellaneous","HSM Vol. 18 No. 3 May-Jun 1999","20"
    "Two Machining Aids","John Campbell","Lathes","HSM Vol. 18 No. 3 May-Jun 1999","22"
    "About Dimensions","James Hamill","General Machining Knowledge","HSM Vol. 18 No. 3 May-Jun 1999","24"
    "Machine Shop Calculations: Bend Allowances","Edward G. Hoffman","General Machining Knowledge","HSM Vol. 18 No. 3 May-Jun 1999","26"
    "Plain Talk About Stick Electrode Arc Welding - Part II","Charles K. Hunt","Welding/Foundry/Forging","HSM Vol. 18 No. 3 May-Jun 1999","28"
    "An Expanding Mandrel","W. Pete Peterka","Lathes","HSM Vol. 18 No. 3 May-Jun 1999","30"
    "Radius Turning Attachment","Theodore M. Clarke","Lathes","HSM Vol. 18 No. 3 May-Jun 1999","32"
    "Micrometer Dial for the Tailstock","W.C. Grosjean","Lathes","HSM Vol. 18 No. 3 May-Jun 1999","40"
    "Micrometer Dial for the Tailstock","W.C. Grosjean","Lathes","HSM Vol. 18 No. 3 May-Jun 1999","40"
    "A Digital Readout for Your Vertical Milling Machine","Guy Lautard","Mills","HSM Vol. 18 No. 3 May-Jun 1999","44"
    "A Simple Die Filer","D. W. Holen","Shop Machinery","HSM Vol. 18 No. 3 May-Jun 1999","48"
    "Practical Design Hints: Machining - Part I","Frederico Strasser","Lathes","HSM Vol. 18 No. 3 May-Jun 1999","50"
    "Thread and Screw Making","George A. Kwasniewski","General Machining Knowledge","HSM Vol. 18 No. 3 May-Jun 1999","54"
    "Simple Chucks to Protect Finished Pieces","W. Pete Peterka","Lathes","HSM Vol. 18 No. 3 May-Jun 1999","57"
    "You Need A Rest!","John Dean","Lathes","HSM Vol. 18 No. 3 May-Jun 1999","58"
    "From the Scrapbox: A Few Tips on Drilling on a Drill Press or a Vertical Milling Machine","Frank A. McLean","Shop Machinery","HSM Vol. 18 No. 3 May-Jun 1999","60"
    "The Micro Machinist: Machine Shop in a Cabinet","Rudy Kouhoupt","Miscellaneous","HSM Vol. 18 No. 3 May-Jun 1999","62"
    "Micrometer Stand","Don McCormac","Shop Accessories","HSM Vol. 18 No. 3 May-Jun 1999","64"
    "Q & A","Frank A. McLean","General Machining Knowledge","HSM Vol. 18 No. 4 Jul-Aug 1999","10"
    "Bench Grinder Safety - Part III","Edward G. Hoffman","Shop Machinery","HSM Vol. 18 No. 4 Jul-Aug 1999","16"
    "Chips & Sparks: Bottles for the Home Shop","Eddie M. Zanrosso","Miscellaneous","HSM Vol. 18 No. 4 Jul-Aug 1999","24"
    "Chips & Sparks: Floating Chucks","Michel Jacot","Machining Accessories","HSM Vol. 18 No. 4 Jul-Aug 1999","24"
    "Machine Shop Crossword Puzzle","James R. Instone","Miscellaneous","HSM Vol. 18 No. 4 Jul-Aug 1999","26"
    "Metric Threads From Your English Lathe","Lawrence Craig","Techniques","HSM Vol. 18 No. 4 Jul-Aug 1999","26"
    "Building a Metal-bodied Hand Plane - Part I","Stephen M. Thomas","Projects","HSM Vol. 18 No. 4 Jul-Aug 1999","28"
    "Crankcases, Crankshafts, and Connecting Rods for Model Engines - Part I","George W. Genevro","Engines","HSM Vol. 18 No. 5 Sep-Oct 1999","28"
    "Building a Target Rifle - Part II","Steve Acker","Gunsmithing","HSM Vol. 18 No. 4 Jul-Aug 1999","36"
    "Workholder Alternatives - Part II","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 18 No. 4 Jul-Aug 1999","41"
    "Upgrading to Variable Speed DC","Steve Acker","Techniques","HSM Vol. 18 No. 4 Jul-Aug 1999","43"
    "The Brass Pad","John B. Gascoyne","Jigs & Fixtures","HSM Vol. 18 No. 4 Jul-Aug 1999","45"
    "Metric Threads","John S. Culver","Techniques","HSM Vol. 18 No. 4 Jul-Aug 1999","46"
    "Horizontal Band Saw - Part II","James S. McKnight","Machine Tools","HSM Vol. 18 No. 4 Jul-Aug 1999","48"
    "The Micro Machinist: A Mechanical Revolutions Counter - Part III","Rudy Kouhoupt","Machining Accessories","HSM Vol. 18 No. 4 Jul-Aug 1999","55"
    "Workholder Alternatives - Part I","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 18 No. 4 Jul-Aug 1999","58"
    "Laser Alignment for the Home Shop","Joe Black","Techniques","HSM Vol. 18 No. 4 Jul-Aug 1999","62"
    "A 5C Collet Chuck","Guy Lautard","Hobby Community","HSM Vol. 18 No. 5 Sep-Oct 1999","24"
    "Cutting a Non-standard Radius on a Milling Machine","Ed Wolcott","Techniques","HSM Vol. 18 No. 5 Sep-Oct 1999","33"
    "Improve Your Lathe Drawbar","Phil Nyman","Techniques","HSM Vol. 18 No. 5 Sep-Oct 1999","34"
    "The Micro Machinist: A Mechanical Strobescope - Part I","Rudy Kouhoupt","Shop Accessories","HSM Vol. 18 No. 5 Sep-Oct 1999","38"
    "Building a Target Rifle - Part III","Steve Acker","Gunsmithing","HSM Vol. 18 No. 5 Sep-Oct 1999","46"
    "Horizontal Band Saw - Part III","James S. McKnight","Machine Tools","HSM Vol. 18 No. 5 Sep-Oct 1999","54"
    "Crankcases, Crankshafts, and Connecting Rods for Model Engines - Part II","George W. Genevro","Engines","HSM Vol. 18 No. 6 Nov-Dec 1999","55"
    "Zinc Aluminum Alloy Sleeve Bearings for a Dividing Head Upgrade","Theodore M. Clarke","Techniques","HSM Vol. 18 No. 5 Sep-Oct 1999","60"
    "Building a Metal-bodied Hand Plane - Part II","Stephen M. Thomas","Projects","HSM Vol. 18 No. 5 Sep-Oct 1999","62"
    "Brass Clock Kit","Mark McKinley","Hobby Community","HSM Vol. 18 No. 6 Nov-Dec 1999","24"
    "Fender Arches Videotape","Guy Lautard","Hobby Community","HSM Vol. 18 No. 6 Nov-Dec 1999","24"
    "Three Elegant Oscillators","Clover McKinley","Hobby Community","HSM Vol. 18 No. 6 Nov-Dec 1999","26"
    "A Very Much Improved Quorn Tool and Cutter Grinder - Part I","Walter B. Mueller","Shop Machinery","HSM Vol. 18 No. 6 Nov-Dec 1999","30"
    "A Mobile Lathe Stand","Rudy Kouhoupt","Machining Accessories","HSM Vol. 18 No. 6 Nov-Dec 1999","38"
    "Building a Metal-bodied Hand Plane - Part III","Stephen M. Thomas","Projects","HSM Vol. 18 No. 6 Nov-Dec 1999","44"
    "Building a Target Rifle - Part IV","Steve Acker","Gunsmithing","HSM Vol. 18 No. 6 Nov-Dec 1999","48"
    "The Micro Machinist: A Mechanical Strobescrope - Part II","Rudy Kouhoupt","Shop Accessories","HSM Vol. 18 No. 6 Nov-Dec 1999","60"
    "Workholder Alternatives - Part III","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 18 No. 6 Nov-Dec 1999","63"
    "Chips & Sparks: A Challenge","Richard Gideon","Techniques","HSM Vol. 19 No. 1 Jan-Feb 2000","24"
    "Chips & Sparks: Holding Short Stock","Roger Claude","Techniques","HSM Vol. 19 No. 1 Jan-Feb 2000","24"
    "Chips & Sparks: Indexing Stops","Robert M. Vaughn","Techniques","HSM Vol. 19 No. 1 Jan-Feb 2000","24"
    "Incra, A Holy Rule","Stan Searing","Hobby Community","HSM Vol. 19 No. 1 Jan-Feb 2000","26"
    "Prazi SD300 5 x 12 Masterturn Metal Lathe and BF 400 Vertical Milling and Drilling Head","Don E. Jones","Hobby Community","HSM Vol. 19 No. 1 Jan-Feb 2000","28"
    "Tooling the Workshop for Clockmakers and Model Makers","Guy Lautard","Hobby Community","HSM Vol. 19 No. 1 Jan-Feb 2000","31"
    "Applying a Quill DRO to a Small Vertical Mill - Part I","Jim Gavin","Mills","HSM Vol. 19 No. 1 Jan-Feb 2000","32"
    "A Very Much Improved Quorn Tool and Cutter Grinder - Part II","Walter B. Mueller","Shop Machinery","HSM Vol. 19 No. 1 Jan-Feb 2000","39"
    "A Multiple Project - Part I - Radius Attachment","Birk Petersen","Machining Accessories","HSM Vol. 19 No. 1 Jan-Feb 2000","44"
    "Ball Turning","Earl Anderson","Techniques","HSM Vol. 19 No. 1 Jan-Feb 2000","52"
    "Improving a Chinese-born Lathe","Paul T. Lindemann","Techniques","HSM Vol. 19 No. 1 Jan-Feb 2000","53"
    "The Micro Machinist: A Mechanical Stroboscope - Part III","Rudy Kouhoupt","Shop Accessories","HSM Vol. 19 No. 1 Jan-Feb 2000","56"
    "Taxes and Homework","Mark E. Battersby","Hobby Community","HSM Vol. 19 No. 1 Jan-Feb 2000","60"
    "Workholding Alternatives - Part IV","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 19 No. 1 Jan-Feb 2000","62"
    "Machine Shop Crossword Puzzle","James R. Instone","Miscellaneous","HSM Vol. 19 No. 1 Jan-Feb 2000","65"
    "Multitool Belt and Disk Grinding Attachment","Edward G. Hoffman","Hobby Community","HSM Vol. 19 No. 2 Mar-Apr 2000","28"
    "Applying a Quill DRO to a Small Vertical Mill - Part II","Jim Gavin","Mills","HSM Vol. 19 No. 2 Mar-Apr 2000","32"
    "A Very Much Improved Quorn Tool and Cutter Grinder - Part III","Walter B. Mueller","Shop Machinery","HSM Vol. 19 No. 2 Mar-Apr 2000","37"
    "A Multiple Project - Part II - Engraver's Block; Bench Block and Steel Rose","Birk Petersen","Jigs & Fixtures","HSM Vol. 19 No. 2 Mar-Apr 2000","42"
    "Morse Taper Work Arbors for an Oversized Project","Lowell P. Braxton","Machining Accessories","HSM Vol. 19 No. 2 Mar-Apr 2000","50"
    "V-Block/Center Drilling Fixture","James S. McKnight","Machining Accessories","HSM Vol. 19 No. 2 Mar-Apr 2000","55"
    "The Micro Machinist: Carriage Stops","Rudy Kouhoupt","Machining Accessories","HSM Vol. 19 No. 2 Mar-Apr 2000","58"
    "Workholding Alternatives - Part V","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 19 No. 2 Mar-Apr 2000","61"
    "Chips & Sparks: I.D.-ing the Oil","Harold G. Cohon","Techniques","HSM Vol. 19 No. 3 May-Jun 2000","24"
    "Chips & Sparks: Quick Table Mount","Alton A. Dubois, Jr.","Machining Accessories","HSM Vol. 19 No. 3 May-Jun 2000","24"
    "5c Collet Closer - Part I","Norman Telleson","Machining Accessories","HSM Vol. 19 No. 3 May-Jun 2000","28"
    "Rotary Tables","Edward G. Hoffman","Machining Accessories","HSM Vol. 19 No. 3 May-Jun 2000","35"
    "The Lathe Thread-chasing Dial - Lathes With Inch-thread Screws","Peter F. Lott","Machining Accessories","HSM Vol. 19 No. 3 May-Jun 2000","38"
    "A Very Much Improved Quorn Tool and Cutter Grinder - Part IV","Walter B. Mueller","Shop Machinery","HSM Vol. 19 No. 3 May-Jun 2000","42"
    "The Real Spindle Lock","Lou Schneider","Machining Accessories","HSM Vol. 19 No. 3 May-Jun 2000","50"
    "A Fixture for Thin Stuff","James DeLong","Jigs & Fixtures","HSM Vol. 19 No. 3 May-Jun 2000","52"
    "Taming the Recoil","Marsh Collins","Gunsmithing","HSM Vol. 19 No. 3 May-Jun 2000","53"
    "Turning a Thin Wall in Teflon","Theodore R. McDowell","Techniques","HSM Vol. 19 No. 3 May-Jun 2000","55"
    "The Micro Machinist: Cross Slide Stops","Rudy Kouhoupt","Machining Accessories","HSM Vol. 19 No. 3 May-Jun 2000","56"
    "Workholding Alternatives - Part VI","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 19 No. 3 May-Jun 2000","59"
    "The Art of Recycling","Robert L. Grady","Techniques","HSM Vol. 19 No. 3 May-Jun 2000","62"
    "Toolmakers' Buttons Generate Precision Holes","Eugene L. Gotz","Shop Accessories","HSM Vol. 19 No. 3 May-Jun 2000","64"
    "Machine Shop Crossword Puzzle","James R. Instone","Miscellaneous","HSM Vol. 19 No. 3 May-Jun 2000","65"
    "The Micro Machinist: Make a Magnetic Lathe Chuck - Part I","Rudy Kouhoupt","Machining Accessories","HSM Vol. 19 No. 4 Jul-Aug 2000","28"
    "Filing Parallel","James S. McKnight","Miscellaneous","HSM Vol. 19 No. 4 Jul-Aug 2000","30"
    "A Dremel Drill Attachment","Jerry Pontius","Hand Tools","HSM Vol. 19 No. 4 Jul-Aug 2000","33"
    "Atlas/Craftsman Slide Stop","James D. Piazza","Machining Accessories","HSM Vol. 19 No. 4 Jul-Aug 2000","42"
    "Sharpen Those Drill Bits - Part I","Paul J. Holm","Machining Accessories","HSM Vol. 19 No. 4 Jul-Aug 2000","45"
    "Electric Discharge Machine (EDM)","Ken Round","Machining Accessories","HSM Vol. 19 No. 4 Jul-Aug 2000","58"
    "Upgrading an Old Bridgeport","Randall Courts","Techniques","HSM Vol. 19 No. 4 Jul-Aug 2000","58"
    "Selecting Mechanical Fasteners - Part I","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 19 No. 4 Jul-Aug 2000","61"
    "Chips & Sparks: A Simpler Brass Pad","Gordon Bader","Machining Accessories","HSM Vol. 19 No. 5 Sep-Oct 2000","20"
    "Chips & Sparks: Good Oilers","Charles H. Loer","Machine Modifications","HSM Vol. 19 No. 5 Sep-Oct 2000","22"
    "Chips & Sparks: Pivoting Depth Gage","Al Sohl, Jr.","Measuring & Layout","HSM Vol. 19 No. 5 Sep-Oct 2000","24"
    "Chips & Sparks: Socket Wrench","Thomas D. Sharples","Hand Tools","HSM Vol. 19 No. 5 Sep-Oct 2000","26"
    "Chips & Sparks: Floating Chucks","Michel Jacot","Machining Accessories","HSM Vol. 19 No. 5 Sep-Oct 2000","27"
    "Free Pendulum Clock - Part I","Jeffrey C. Maier","Clocks","HSM Vol. 19 No. 5 Sep-Oct 2000","28"
    "A Homemade Magnetizer-Demagnetizer","Jim Wiley","Shop Accessories","HSM Vol. 19 No. 5 Sep-Oct 2000","35"
    "Sharpen Those Drill Bits - Part II","Paul J. Holm","Machining Accessories","HSM Vol. 19 No. 5 Sep-Oct 2000","42"
    "Self-centering Drill Jig","James S. McKnight","Machining Accessories","HSM Vol. 19 No. 5 Sep-Oct 2000","49"
    "A Poor Man's Level","Jack R. Thompson","Measuring & Layout","HSM Vol. 19 No. 5 Sep-Oct 2000","52"
    "Chips & Sparks: Band Saw Modifications","Harold G. Cohon","Techniques","HSM Vol. 19 No. 5 Sep-Oct 2000","53"
    "Small Precision Balls","John Bochert","Techniques","HSM Vol. 19 No. 5 Sep-Oct 2000","54"
    "The Micro Machinist: Make a Magnetic Lathe Chuck - Part II","Rudy Kouhoupt","Machining Accessories","HSM Vol. 19 No. 5 Sep-Oct 2000","56"
    "Mill Restoration","Martin Ford","Machine Tools","HSM Vol. 19 No. 5 Sep-Oct 2000","58"
    "Selecting Mechanical Fasteners - Part II","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 19 No. 5 Sep-Oct 2000","61"
    "Grizzly 13 x 40 Lathe","Jean Michel","Machine Tools","HSM Vol. 19 No. 5 Sep-Oct 2000","64"
    "Build an Air Compressor","Jim Reynolds","Shop Machinery","HSM Vol. 19 No. 6 Nov-Dec 2000","35"
    "Driving the Stirling-Powered Tractor","Norman Briskman","Engines","HSM Vol. 19 No. 6 Nov-Dec 2000","44"
    "Free Pendulum Clock - Part II","Jeffrey C. Maier","Clocks","HSM Vol. 19 No. 6 Nov-Dec 2000","50"
    "Miniature Height Gage","James S. McKnight","Measuring & Layout","HSM Vol. 19 No. 6 Nov-Dec 2000","56"
    "Parting Tool Holder","Wayne Gosnell","Machining Accessories","HSM Vol. 19 No. 6 Nov-Dec 2000","60"
    "The Micro Machinist: Make a Magnetic Lathe Chuck - Part III","Rudy Kouhoupt","Machining Accessories","HSM Vol. 19 No. 6 Nov-Dec 2000","62"
    "Selecting Mechanical Fasteners - Part III","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 19 No. 6 Nov-Dec 2000","64"
    "Secret Workshop Business","Terry Sexton","Miscellaneous","HSM Vol. 19 No. 6 Nov-Dec 2000","67"
    "Book Review: Iron Melting Cupola Furnaces by Steve Chastain","Steve Acker","Hobby Community","HSM Vol. 20 No. 1 Jan-Feb 2001","18"
    "The Phoenix Horizontal Milling and Boring Machine - Part 1","A. N. Eastwood","Machine Tools","HSM Vol. 20 No. 1 Jan-Feb 2001","20"
    "Additions and Modifications to the Sakai ML-360 Lathe","Roger Lang","Machine Tools","HSM Vol. 20 No. 1 Jan-Feb 2001","26"
    "The Poor Man's T-Slot Rotary Table - Part 1","Wayne Hanson","Machining Accessories","HSM Vol. 20 No. 1 Jan-Feb 2001","32"
    "Free Pendulum Clock - Part 3","Jeffrey C. Maier","Clocks","HSM Vol. 20 No. 1 Jan-Feb 2001","40"
    "Another Edge Finder","Richard Young","Machining Accessories","HSM Vol. 20 No. 1 Jan-Feb 2001","50"
    "Bench Blocks","Michael T. Yamamoto","Machining Accessories","HSM Vol. 20 No. 1 Jan-Feb 2001","52"
    "Projects Without Drawings","Michael T. Yamamoto","Machining Accessories","HSM Vol. 20 No. 1 Jan-Feb 2001","52"
    "Miniature Bender","Michael T. Yamamoto","Machining Accessories","HSM Vol. 20 No. 1 Jan-Feb 2001","54"
    "Small Blow Gun","Michael T. Yamamoto","Machining Accessories","HSM Vol. 20 No. 1 Jan-Feb 2001","54"
    "Fine Oil Dispenser","Michael T. Yamamoto","Machining Accessories","HSM Vol. 20 No. 1 Jan-Feb 2001","55"
    "How Many Turns? How Many Holes?","M V Stivison","Measuring & Layout","HSM Vol. 20 No. 1 Jan-Feb 2001","56"
    "The Micro Machinist: A Balanced Knurling Tool - Part 1","Rudy Kouhoupt","Machining Accessories","HSM Vol. 20 No. 1 Jan-Feb 2001","58"
    "Clamp Set for Your Mill","Jack R. Thompson","Machining Accessories","HSM Vol. 20 No. 1 Jan-Feb 2001","61"
    "Jigs & Fixtures: Selecting Mechanical Fasteners - Part 4","Edward G. Hoffman","Miscellaneous","HSM Vol. 20 No. 1 Jan-Feb 2001","62"
    "Tapping Machine","Richard Butterick","Machining Accessories","HSM Vol. 20 No. 2 Mar-Apr 2001","22"
    "The Phoenix Horizontal Milling and Boring Machine - Part 2","A. N. Eastwood","Machine Tools","HSM Vol. 20 No. 2 Mar-Apr 2001","32"
    "Free Pendulum Clock - Part 4","Jeffrey C. Maier","Clocks","HSM Vol. 20 No. 2 Mar-Apr 2001","42"
    "The Poor Man's T-Slot Rotary Table - Part 2","Wayne Hanson","Machining Accessories","HSM Vol. 20 No. 2 Mar-Apr 2001","50"
    "The Micro Machinist: A Balanced Knurling Tool - Part 2","Rudy Kouhoupt","Machining Accessories","HSM Vol. 20 No. 2 Mar-Apr 2001","56"
    "Jigs & Fixtures: Selecting Mechanical Fasteners - Part 5","Edward G. Hoffman","Miscellaneous","HSM Vol. 20 No. 2 Mar-Apr 2001","60"
    "Tilt Body Indexer - Part 1","Wayne Hanson","Machining Accessories","HSM Vol. 20 No. 3 May-Jun 2001","18"
    "Tapping Machine - Part 2","Richard Butterick","Machining Accessories","HSM Vol. 20 No. 3 May-Jun 2001","28"
    "The Phoenix Horizontal Milling and Boring Machine - Part 3","A. N. Eastwood","Machine Tools","HSM Vol. 20 No. 3 May-Jun 2001","36"
    "Free Pendulum Clock - Part 5","Jeffrey C. Maier","Clocks","HSM Vol. 20 No. 3 May-Jun 2001","46"
    "The Micro Machinist: A Balanced Knurling Tool - Part 3","Rudy Kouhoupt","Machining Accessories","HSM Vol. 20 No. 3 May-Jun 2001","56"
    "Jig & Fixtures - Selecting Mechanical Fasteners - Part 6","Edward G. Hoffman","Miscellaneous","HSM Vol. 20 No. 3 May-Jun 2001","60"
    "The Micro Machinist: An Atlas Mill Update - Part 1","Rudy Kouhoupt","Machine Modifications","HSM Vol. 20 No. 4 Jul-Aug 2001","16"
    "Casting Iron in the Home Foundry","Stephen Chastain","Welding/Foundry/Forging","HSM Vol. 20 No. 4 Jul-Aug 2001","22"
    "Tapping Machine - Part 3","Richard Butterick","Machining Accessories","HSM Vol. 20 No. 4 Jul-Aug 2001","32"
    "Tilt Body Indexer - Part 2","Wayne Hanson","Machining Accessories","HSM Vol. 20 No. 4 Jul-Aug 2001","38"
    "The Phoenix Horizontal Milling and Boring Machine - Part 4","A. N. Eastwood","Machine Tools","HSM Vol. 20 No. 4 Jul-Aug 2001","47"
    "Machining a Cast Iron Faceplate","Steve Acker","Machining Accessories","HSM Vol. 20 No. 4 Jul-Aug 2001","54"
    "Overhauling the Old Lady","Marsh Collins","Lathes","HSM Vol. 20 No. 4 Jul-Aug 2001","60"
    "Angle Measurement with an Adjustable Square","Robert D. Swinney","Measuring & Layout","HSM Vol. 20 No. 4 Jul-Aug 2001","61"
    "Larger Spherical Radii","John Bochert","Techniques","HSM Vol. 20 No. 4 Jul-Aug 2001","62"
    "A Modified Base for a Band Saw","Jim McKee","Machine Modifications","HSM Vol. 20 No. 4 Jul-Aug 2001","64"
    "Jigs & Fixtures: Lifting Devices - Part 1","Edward G. Hoffman","Techniques","HSM Vol. 20 No. 4 Jul-Aug 2001","66"
    "Tesla Turbine Part 1","Jeffrey C. Maier","Engines","HSM Vol. 20 No. 5 Sep-Oct 2001","18"
    "Tilt Body Indexer Part 3","Wayne Hanson","Machining Accessories","HSM Vol. 20 No. 5 Sep-Oct 2001","34"
    "The Phoenix Horizontal Milling and Boring Machine - Part 5","A. N. Eastwood","Machine Tools","HSM Vol. 20 No. 5 Sep-Oct 2001","42"
    "Digital Readout for the Grizzly G-1005 Mill-Drill Part 1","Roland W. Friestad","Mills","HSM Vol. 20 No. 5 Sep-Oct 2001","52"
    "Scroll Chucks - Their Care and Repair","Nathan Miller","Miscellaneous","HSM Vol. 20 No. 5 Sep-Oct 2001","58"
    "A Locating Stop for the Milling Vise","Glenn L. Wilson","Machining Accessories","HSM Vol. 20 No. 5 Sep-Oct 2001","62"
    "Setting Up Fly-cutter Bits","Gary Christiansen","Techniques","HSM Vol. 20 No. 5 Sep-Oct 2001","64"
    "An Atlas Mill Update Part 2","Rudy Kouhoupt","Machine Modifications","HSM Vol. 20 No. 5 Sep-Oct 2001","66"
    "Jigs & Fixtures: Lifting Devices - Part 2","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 20 No. 5 Sep-Oct 2001","70"
    "Angle Makes All the Difference!","Paul J. Holm","Shop Accessories","HSM Vol. 20 No. 6 Nov-Dec 2001","18"
    "Induction Motors and Rotary Phase Converters","Robert D. Swinney","Miscellaneous","HSM Vol. 20 No. 6 Nov-Dec 2001","26"
    "Tilt Body Indexer Part 4","Wayne Hanson","Machining Accessories","HSM Vol. 20 No. 6 Nov-Dec 2001","38"
    "Tesla Turbine - Part 2","Jeffrey C. Maier","Engines","HSM Vol. 20 No. 6 Nov-Dec 2001","43"
    "Replacing Quill Bearings","Marsh Collins","Mills","HSM Vol. 20 No. 6 Nov-Dec 2001","52"
    "Overhauling a Jacobs Chuck","Martin Gingrich","Lathes","HSM Vol. 20 No. 6 Nov-Dec 2001","55"
    "Tale of Three Smoke-poles","Birk Petersen","Gunsmithing","HSM Vol. 20 No. 6 Nov-Dec 2001","57"
    "Digital Readout for the Grizzly G-1005 Mill-Drill Part 2","Roland W. Friestad","Mills","HSM Vol. 20 No. 6 Nov-Dec 2001","58"
    "An Easy Lathe Collet Adapter","James S. McKnight","Machine Tools","HSM Vol. 20 No. 6 Nov-Dec 2001","61"
    "An Atlas Mill Update Part 3","Rudy Kouhoupt","Machine Modifications","HSM Vol. 20 No. 6 Nov-Dec 2001","64"
    "Jigs & Fixtures: Lifting Devices - Part 3","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 20 No. 6 Nov-Dec 2001","67"
    "Electric Engine","Don H. Vreeland","Engines","HSM Vol. 21 No. 1 Jan-Feb 2002","18"
    "Linux in the Home Workshop","Wayde Gutman","Computers","HSM Vol. 21 No. 1 Jan-Feb 2002","24"
    "Potter's Wheel - Part 1","Guy Ells","Projects","HSM Vol. 21 No. 1 Jan-Feb 2002","26"
    "Basic Machining Reference Handbook","Raymond D. Niergarth","Hobby Community","HSM Vol. 21 No. 1 Jan-Feb 2002","34"
    "Workshop Procedures for Clockmakers and Modelmakers","Guy Lautard","Hobby Community","HSM Vol. 21 No. 1 Jan-Feb 2002","39"
    "Tesla Turbine - Part 3","Jeffrey C. Maier","Engines","HSM Vol. 21 No. 1 Jan-Feb 2002","41"
    "Upgrading a Cintilathe Dial","Ed Ashby","Machine Modifications","HSM Vol. 21 No. 1 Jan-Feb 2002","49"
    "Like a Bridge Over Troublesome Shapes","Charles St. Louis","Measuring & Layout","HSM Vol. 21 No. 1 Jan-Feb 2002","52"
    "An Atlas Mill Update - Part 4","Rudy Kouhoupt","Machine Tools","HSM Vol. 21 No. 1 Jan-Feb 2002","54"
    "Retrofit a Grizzly G1005 Mill-Drill to CNC - Part 1","Roland W. Friestad","Computers","HSM Vol. 21 No. 1 Jan-Feb 2002","58"
    "Jigs & Fixtures: Setup Tips","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 21 No. 1 Jan-Feb 2002","62"
    "Build a Quick-Change Toolholder - Part 1","Rudy Kouhoupt","Machining Accessories","HSM Vol. 21 No. 2 Mar-Apr 2002","16"
    "Tesla Turbine - Part 4","Jeffrey C. Maier","Engines","HSM Vol. 21 No. 2 Mar-Apr 2002","20"
    "Potter's Wheel - Part 2","Guy Ells","Projects","HSM Vol. 21 No. 2 Mar-Apr 2002","26"
    "Vane Pump","Jim Reynolds","Shop Machinery","HSM Vol. 21 No. 2 Mar-Apr 2002","39"
    "Americanizing a Falcon Lathe","Ed Ashby","Machine Modifications","HSM Vol. 21 No. 2 Mar-Apr 2002","46"
    "Retrofit a Grizzly G1005 Mill-Drill to CNC - Part 2","Roland W. Friestad","Computers","HSM Vol. 21 No. 2 Mar-Apr 2002","50"
    "Jigs & Fixtures: Setup Tips - Part 2","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 21 No. 2 Mar-Apr 2002","56"
    "Hobbing Gears in a Mill","Terry Sexton","Mills","HSM Vol. 21 No. 3 May-Jun 2002","12"
    "Pick-off Gears - An Explanation","Terry Sexton","Machining Accessories","HSM Vol. 21 No. 3 May-Jun 2002","21"
    "Hand-held Dial Indicator Tester","Ferdinand Baar","Measuring & Layout","HSM Vol. 21 No. 3 May-Jun 2002","24"
    "Tesla Turbine - Part 5","Jeffrey C. Maier","Engines","HSM Vol. 21 No. 3 May-Jun 2002","30"
    "Buffers Etcetera","Wayne Hanson","Shop Machinery","HSM Vol. 21 No. 3 May-Jun 2002","39"
    "Potter's Wheel - Part 3","Guy Ells","Projects","HSM Vol. 21 No. 3 May-Jun 2002","44"
    "Retrofit a Grizzly G1005 Mill-Drill to CNC - Part 3","Roland W. Friestad","Computers","HSM Vol. 21 No. 3 May-Jun 2002","52"
    "Build a Quick-Change Toolholder - Part 2","Rudy Kouhoupt","Machining Accessories","HSM Vol. 21 No. 3 May-Jun 2002","58"
    "Jigs & Fixtures: Approximate Location Conical Locators - Part 1","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 21 No. 3 May-Jun 2002","62"
    "Enco 12 x 36 Lathe and Shooting Star Digital Readout","Stephen Chastain","Hobby Community","HSM Vol. 21 No. 3 May-Jun 2002","64"
    "Getting Started in Metal Spinning - Part 1","James P. Riser","General Machining Knowledge","HSM Vol. 21 No. 4 Jul-Aug 2002","12"
    "Dual-action Fly Cutter","Fred Prestridge","Machining Accessories","HSM Vol. 21 No. 4 Jul-Aug 2002","21"
    "A Collet Reference - From the 1942 Hardinge Bros Catalog","Ralph B. Miller","General Machining Knowledge","HSM Vol. 21 No. 4 Jul-Aug 2002","24"
    "Building a Spider Handle","Doug Ripka","Machining Accessories","HSM Vol. 21 No. 4 Jul-Aug 2002","27"
    "Chuck Mounting Plate","Paul Smeltzer","Machining Accessories","HSM Vol. 21 No. 4 Jul-Aug 2002","30"
    "Precision Boring","R.G. Sparber","Lathes","HSM Vol. 21 No. 4 Jul-Aug 2002","34"
    "Toolholder Extension","Theodore M. Clarke","Machining Accessories","HSM Vol. 21 No. 4 Jul-Aug 2002","38"
    "Welding Electrodes for the Home Shop Machinist","George A. Ewen","Welding/Foundry/Forging","HSM Vol. 21 No. 4 Jul-Aug 2002","39"
    "Notes on the 7 x 10 Mini-Lathe - Harbor Freight Model 33684","Joe Mroz","Hobby Community","HSM Vol. 21 No. 4 Jul-Aug 2002","41"
    "Make Your Own Small Toolholder","James R. Instone","Machining Accessories","HSM Vol. 21 No. 4 Jul-Aug 2002","43"
    "The Continental A-40 Aircraft Engine","George W. Genevro","Engines","HSM Vol. 21 No. 4 Jul-Aug 2002","46"
    "Build a Quick-Change Toolholder - Part 3","Rudy Kouhoupt","Machining Accessories","HSM Vol. 21 No. 4 Jul-Aug 2002","59"
    "Jigs & Fixtures: Approximate Location Conical Locators - Part 2","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 21 No. 4 Jul-Aug 2002","63"
    "Retrofit a Grizzly G1005 Mill-Drill to CNC - Part 4","Roland W. Friestad","Computers","HSM Vol. 21 No. 4 Jul-Aug 2002","66"
    "Gear Repair by Bronze Surfacing","Dennis Erdelac","Miscellaneous","HSM Vol. 21 No. 5 Sep-Oct 2002","11"
    "Getting Started in Metal Spinning - Part 2","James P. Riser","General Machining Knowledge","HSM Vol. 21 No. 5 Sep-Oct 2002","14"
    "Miniature Collet Driver, A - Learning Experiences in Concentricity","John W. Way","Machining Accessories","HSM Vol. 21 No. 5 Sep-Oct 2002","23"
    "Modified Chuck Key","Paul J. Holm","Machining Accessories","HSM Vol. 21 No. 5 Sep-Oct 2002","28"
    "Building a Miniature Church","Walter Yetman","Projects","HSM Vol. 21 No. 5 Sep-Oct 2002","30"
    "Make Your Own Socket Head Fasteners with the Brinkerhoff Rotary Broach","Joe Black","Machining Accessories","HSM Vol. 21 No. 5 Sep-Oct 2002","36"
    "Notes on Building a Nine-cylinder Radial Aircraft Engine","Douglas Kelley","Engines","HSM Vol. 21 No. 5 Sep-Oct 2002","39"
    "Way Too Fast!","Gordon Tengen","General Machining Knowledge","HSM Vol. 21 No. 5 Sep-Oct 2002","43"
    "Removing Backlash with a Left-hand Tap","Fred Prestridge","Lathes","HSM Vol. 21 No. 5 Sep-Oct 2002","47"
    "Make Your Own 3C and 6K Collets","John W. Foster","Machining Accessories","HSM Vol. 21 No. 5 Sep-Oct 2002","50"
    "Building an MLA Filing Machine","Jerry Tuwiner","Shop Machinery","HSM Vol. 21 No. 5 Sep-Oct 2002","54"
    "CNC Tooling Setups and Used CNC Equipment","Roland W. Friestad","Computers","HSM Vol. 21 No. 5 Sep-Oct 2002","57"
    "Build a Quick-change Toolholder - Part 4","Rudy Kouhoupt","Machining Accessories","HSM Vol. 21 No. 5 Sep-Oct 2002","63"
    "Jigs & Fixtures: Approximate Location Sight Locators","Edward G. Hoffman","Jigs & Fixtures","HSM Vol. 21 No. 5 Sep-Oct 2002","67"
    "Makers of American Machinist's Tools","Neil Knopf","Hobby Community","HSM Vol. 21 No. 5 Sep-Oct 2002","70"
    "The Vandy Electric Scooter - Part 1","Glenn Vandiver","Projects","HSM Vol. 21 No. 6 Nov-Dec 2002","14"
    "Getting Started in Metal Spinning - Part 3","James P. Riser","General Machining Knowledge","HSM Vol. 21 No. 6 Nov-Dec 2002","28"
    "Making Small Pistons and Rings","Bob Shores","Engines","HSM Vol. 21 No. 6 Nov-Dec 2002","39"
    "A Look at Tru-Punch from Precision Brand","Neil Knopf","Hobby Community","HSM Vol. 21 No. 6 Nov-Dec 2002","40"
    "Computers in the Shop: Quick Change Drawbar","Roland W. Friestad","Machining Accessories","HSM Vol. 21 No. 6 Nov-Dec 2002","43"
    "Metric Equivalent Drills","M V Stivison","General Machining Knowledge","HSM Vol. 21 No. 6 Nov-Dec 2002","47"
    "The Micro Machinist: A Compact Double-action Indicator - Part 1","Rudy Kouhoupt","Measuring & Layout","HSM Vol. 21 No. 6 Nov-Dec 2002","49"
    "Inexpensive Sand Blasting Cabinet","Todd Bredeson","Shop Accessories","HSM Vol. 21 No. 6 Nov-Dec 2002","54"
    "Solving the Three-phase Problem with a VFD","Stephen G. Wellcome","Motors","HSM Vol. 21 No. 6 Nov-Dec 2002","59"
    "The Ten-cent Solution","Hugh M. Sanborn","General Machining Knowledge","HSM Vol. 21 No. 6 Nov-Dec 2002","64"
    "Moving a Rong Fu Mill-Drill","Herb Helbig","Machine Tools","HSM Vol. 21 No. 6 Nov-Dec 2002","66"
    "Radial Electric Motor - Part 1","Jeffrey C. Maier","Engines","HSM Vol. 22 No. 1 Jan-Feb 2003","10"
    "Electrical Discharge Machining - Removing Metal by Spark Erosion - Part 7 - Mechanical Components of a Wire EDM","Robert P. Langlois","EDM","HSM Vol. 22 No. 1 Jan-Feb 2003","26"
    "The Geneva Mechanism","Weston Bye","Projects","HSM Vol. 22 No. 1 Jan-Feb 2003","31"
    "A Different Approach to Small Flywheel Machining","Fred Prestridge","Miscellaneous","HSM Vol. 22 No. 1 Jan-Feb 2003","36"
    "Machining in the 21st Century","Joe Martin","Hobby Community","HSM Vol. 22 No. 1 Jan-Feb 2003","39"
    "An Excellent, Affordable Drill Bit Sharpener","David O'Neil","Shop Accessories","HSM Vol. 22 No. 1 Jan-Feb 2003","41"
    "The Vandy Electric Scooter - Part 2","Glenn Vandiver","Projects","HSM Vol. 22 No. 1 Jan-Feb 2003","46"
    "Universal CNC Controller - Part 1","Roland W. Friestad","Computers","HSM Vol. 22 No. 1 Jan-Feb 2003","56"
    "A Compact, Double-action Indicator - Part 2","Rudy Kouhoupt","Measuring & Layout","HSM Vol. 22 No. 1 Jan-Feb 2003","64"
    "Temporary Marking on Metal - Chips & Sparks","Bob Neidorff","Techniques","HSM Vol. 22 No. 1 Jan-Feb 2003","71"
    "Outstanding Metalworking Craftsman for 2003 is Barry Jordan","Neil Knopf","Hobby Community","HSM Vol. 22 No. 2 Mar-Apr 2003","15"
    "Mill-Drill Vise with Real Capacity","Paul J. Holm","Machining Accessories","HSM Vol. 22 No. 2 Mar-Apr 2003","16"
    "Radial Electric Motor - Part 2","Jeffrey C. Maier","Engines","HSM Vol. 22 No. 2 Mar-Apr 2003","20"
    "The Vandy Electric Scooter - Part 3","Glenn Vandiver","Projects","HSM Vol. 22 No. 2 Mar-Apr 2003","32"
    "Electrical Discharge Machining - Removing Metal by Spark Erosion - Part 8","Robert P. Langlois","EDM","HSM Vol. 22 No. 2 Mar-Apr 2003","44"
    "Swivel Blocks","Walter Yetman","Machining Accessories","HSM Vol. 22 No. 2 Mar-Apr 2003","50"
    "Computers in the Shop: Universal CNC Controller - Part 2","Roland W. Friestad","Computers","HSM Vol. 22 No. 2 Mar-Apr 2003","56"
    "Book Review: Five Hundred and Seven Mechanical Movements","Neil Knopf","Hobby Community","HSM Vol. 22 No. 2 Mar-Apr 2003","66"
    "The Micro Machinist: A Compact, Double-action Indicator - Part 3","Rudy Kouhoupt","Measuring & Layout","HSM Vol. 22 No. 2 Mar-Apr 2003","67"
    "Build the Radial Five - Part 1","Rudy Kouhoupt","Engines","HSM Vol. 22 No. 3 May-Jun 2003","16"
    "The Vandy Electric Scooter - Part 4","Glenn Vandiver","Projects","HSM Vol. 22 No. 3 May-Jun 2003","20"
    "Spring Fever - Winding Your Own","George Ingraham","General Machining Knowledge","HSM Vol. 22 No. 3 May-Jun 2003","30"
    "Radial Electric Motor - Part 3 Conclusion","Jeffrey C. Maier","Engines","HSM Vol. 22 No. 3 May-Jun 2003","36"
    "Electrical Discharge Machining - Removing Metal by Spark Erosion - Part 9","Robert P. Langlois","EDM","HSM Vol. 22 No. 3 May-Jun 2003","50"
    "A Radius Cutting Tool for the Grizzly G4015Z Mill-Lathe","Jerry L. Sokol","Machining Accessories","HSM Vol. 22 No. 3 May-Jun 2003","60"
    "Indexable Carbide Insert End Mill","Michael Jenks","Machining Accessories","HSM Vol. 22 No. 3 May-Jun 2003","66"
    "Computers in the Shop: Universal CNC Controller - Part 3","Roland W. Friestad","Computers","HSM Vol. 22 No. 3 May-Jun 2003","70"
    "Rebuild a Cylinder Head","Stephen Chastain","Miscellaneous","HSM Vol. 22 No. 4 Jul-Aug 2003","10"
    "Repairing Old Iron","David R. MacManus","Miscellaneous","HSM Vol. 22 No. 4 Jul-Aug 2003","18"
    "A Handy Material Storage Rack","Stephen J. Roberts","Shop Accessories","HSM Vol. 22 No. 4 Jul-Aug 2003","25"
    "Sharpening HSS Lathe Tool Bits","Stephen G. Wellcome","Techniques","HSM Vol. 22 No. 4 Jul-Aug 2003","28"
    "Electrical Discharge Machining - Removing Metal by Spark Erosion - Part 10","Robert P. Langlois","EDM","HSM Vol. 22 No. 4 Jul-Aug 2003","34"
    "Build the Radial Five - Part 2","Rudy Kouhoupt","Engines","HSM Vol. 22 No. 4 Jul-Aug 2003","38"
    "The Vandy Electric Scooter - Part 5","Glenn Vandiver","Projects","HSM Vol. 22 No. 4 Jul-Aug 2003","41"
    "Get Straight to the Point with The Drill Doctor","George Ingraham","Shop Accessories","HSM Vol. 22 No. 4 Jul-Aug 2003","50"
    "Book Review: The Taig Lathe - DivisionMaster Press","Neil Knopf","Hobby Community","HSM Vol. 22 No. 4 Jul-Aug 2003","54"
    "Finish That Micrometer Box","William Johnson","Miscellaneous","HSM Vol. 22 No. 4 Jul-Aug 2003","56"
    "Two-stroke Cycle Model Engines - a look at basic concepts","George W. Genevro","Engines","HSM Vol. 22 No. 4 Jul-Aug 2003","60"
    "Make a Hub Wrench","Peter C. Esselburne","Miscellaneous","HSM Vol. 22 No. 4 Jul-Aug 2003","65"
    "The NAMES Show CNC Department","Roland W. Friestad","Hobby Community","HSM Vol. 22 No. 4 Jul-Aug 2003","68"
    "Functional Metal Enclosures from Sheet Brass and Aluminum","William T. Roubal, Ph.D.","Projects","HSM Vol. 22 No. 5 Sep-Oct 2003","10"
    "2003 Machinist's Challenge Results","Magazine Services","Hobby Community","HSM Vol. 22 No. 5 Sep-Oct 2003","20"
    "Lifetime Achievement Award Presented to Rudy Kouhoupt","Magazine Services","Hobby Community","HSM Vol. 22 No. 5 Sep-Oct 2003","21"
    "Transplant a Compound Gear Assembly","Herbert Yohe","Machine Modifications","HSM Vol. 22 No. 5 Sep-Oct 2003","22"
    "Disk-cutting Fixtures for the Lathe","Bernard Szwarc","Machining Accessories","HSM Vol. 22 No. 5 Sep-Oct 2003","24"
    "Hang That File","William Johnson","Miscellaneous","HSM Vol. 22 No. 5 Sep-Oct 2003","26"
    "Book Review: The Tinsmith's Helper and Pattern Book","Neil Knopf","Hobby Community","HSM Vol. 22 No. 5 Sep-Oct 2003","28"
    "Thread Substitutions","Theodore M. McDowell","General Machining Knowledge","HSM Vol. 22 No. 5 Sep-Oct 2003","30"
    "Small Parts Holder for Silver Soldering","Tom Bartlett","Jigs & Fixtures","HSM Vol. 22 No. 5 Sep-Oct 2003","35"
    "The Vandy Electric Scooter - Part 6","Glenn Vandiver","Projects","HSM Vol. 22 No. 5 Sep-Oct 2003","38"
    "Easy Threading Tool Sharpener","Glenn L. Wilson","Shop Accessories","HSM Vol. 22 No. 5 Sep-Oct 2003","42"
    "Using The Lincoln Electric Invertec V-160-S Welder","R.G. Sparber","Welding/Foundry/Forging","HSM Vol. 22 No. 5 Sep-Oct 2003","46"
    "Electric Discharge Machining - Removing Metal by Spark Erosion - Part 11","Robert P. Langlois","EDM","HSM Vol. 22 No. 5 Sep-Oct 2003","50"
    "The Micro Machinist: Build the Radial Five - Part 3","Rudy Kouhoupt","Engines","HSM Vol. 22 No. 5 Sep-Oct 2003","57"
    "Titanium - A Metal for the Space Age","George W. Genevro","General Machining Knowledge","HSM Vol. 22 No. 5 Sep-Oct 2003","62"
    "Computers in the Shop: Reclaiming a Bridgeport Series I CNC Milling Machine - Part 1","Roland W. Friestad","Computers","HSM Vol. 22 No. 5 Sep-Oct 2003","68"
    "Lathe Ball Making Accessory - Part One","Robert L. Bailey","Machining Accessories","HSM Vol. 22 No. 6 Nov-Dec 2003","10"
    "A Simple Turret for the Atlas/Craftsman 12 Lathe","Tim Clarke","Machining Accessories","HSM Vol. 22 No. 6 Nov-Dec 2003","18"
    "Experimenting With Fly Cutters","Chet McClellan","Machining Accessories","HSM Vol. 22 No. 6 Nov-Dec 2003","28"
    "Milling Vise Alignment","Donald Erickson","Machine Modifications","HSM Vol. 22 No. 6 Nov-Dec 2003","34"
    "A Look at the Grizzly G9950 Shear/Brake","Harold G. Cohon","Hobby Community","HSM Vol. 22 No. 6 Nov-Dec 2003","38"
    "Electric Discharge Machining - Removing Metal by Spark Erosion - Part 12","Robert P. Langlois","EDM","HSM Vol. 22 No. 6 Nov-Dec 2003","44"
    "Heat Treating Steel - An Amateur's View","Randolph Constantine","General Machining Knowledge","HSM Vol. 22 No. 6 Nov-Dec 2003","50"
    "Essential Reading for the Home Shop Machinist - Good Books That Won't Break Your Budget","Stephen Chastain","General Machining Knowledge","HSM Vol. 22 No. 6 Nov-Dec 2003","56"
    "Build the Radial Five - Part 4","Rudy Kouhoupt","Engines","HSM Vol. 22 No. 6 Nov-Dec 2003","60"
    "Computers in the Shop: Reclaiming a Bridgeport Series I CNC Milling Machine - Part 2","Roland W. Friestad","Computers","HSM Vol. 22 No. 6 Nov-Dec 2003","66"
    "Converting a Woodcutting Band Saw to Cut Metal","Jim Gavin","Shop Machinery","HSM Vol. 23 No. 1 Jan-Feb 2004","10"
    "Lathe Ball Making Accessory - Part 2","Robert L. Bailey","Lathes","HSM Vol. 23 No. 1 Jan-Feb 2004","20"
    "Repair Backlash with Moglice","Otto Bacon","Mills","HSM Vol. 23 No. 1 Jan-Feb 2004","26"
    "First Annual Men, Metal, and Machines Expo","Neil Knopf","Hobby Community","HSM Vol. 23 No. 1 Jan-Feb 2004","34"
    "How to Build an Excuse-Some Things You Just Can't Learn in School","Butch Holcombe","Hobby Community","HSM Vol. 23 No. 1 Jan-Feb 2004","45"
    "Telescopic Taper Attachment for South Bend 9 or 10 lathes","John W. Foster","Lathes","HSM Vol. 23 No. 1 Jan-Feb 2004","48"
    "The Micro Machinist: Build the Radial Five - Part 5","Rudy Kouhoupt","Engines","HSM Vol. 23 No. 1 Jan-Feb 2004","62"
    "Computers in the Shop: Reclaiming a Bridgeport Series 1 CNC Milling Machine - Part 3","Roland W. Friestad","Computers","HSM Vol. 23 No. 1 Jan-Feb 2004","68"
    "Removing Broken Taps and Studs by Welding","J. Randolph Bulgin","Welding/Foundry/Forging","HSM Vol. 23 No. 2 Mar-Apr 2004","12"
    "Lathe Ball Making Accessory Part Three","Robert L. Bailey","Lathes","HSM Vol. 23 No. 2 Mar-Apr 2004","16"
    "Make a Saddle/Carriage Clamp Lock","Steve Roberts","Lathes","HSM Vol. 23 No. 2 Mar-Apr 2004","26"
    "A Thread Cutting Stop for South Bend Lathes","A. N. Eastwood","Lathes","HSM Vol. 23 No. 2 Mar-Apr 2004","32"
    "High Quality Project Cases","Robert Nance Dee","Shop Accessories","HSM Vol. 23 No. 2 Mar-Apr 2004","36"
    "The New Hand: Using the Wiggler for Drilling Accurately Drilled Holes","Forrest Addy","Shop Machinery","HSM Vol. 23 No. 2 Mar-Apr 2004","44"
    "Moving an Enco RF-30 Mill Drill...Twice","R.G. Sparber","Miscellaneous","HSM Vol. 23 No. 2 Mar-Apr 2004","48"
    "Engine Configurations - Planning an Engine Layout","George W. Genevro","Engines","HSM Vol. 23 No. 2 Mar-Apr 2004","51"
    "The Micro Machinist: Build the Radial Five - Part 6","Rudy Kouhoupt","Engines","HSM Vol. 23 No. 2 Mar-Apr 2004","60"
    "Computers in the Shop: CAD Basics - Part 1","Roland W. Friestad","Computers","HSM Vol. 23 No. 2 Mar-Apr 2004","64"
    "The "Outstanding Metalworking Craftsman" for 2004 is Roger L. Ronnie","Craig Libuse","Hobby Community","HSM Vol. 23 No. 3 May-Jun 2004","11"
    "A Tandem, Double-Acting Engine","Douglas Kelley","Engines","HSM Vol. 23 No. 3 May-Jun 2004","12"
    "Lathe Ball Making Accessory - Part 4 - Conclusion","Robert L. Bailey","Lathes","HSM Vol. 23 No. 3 May-Jun 2004","16"
    "Build a 50/30 Ton H-Frame Hydraulic Floor Press","Reed Streifthau","Shop Machinery","HSM Vol. 23 No. 3 May-Jun 2004","20"
    "The New Hand - Using the Edge Finder","Forrest Addy","General Machining Knowledge","HSM Vol. 23 No. 3 May-Jun 2004","36"
    "Getting Started with Welding Plastic","Glenn Vandiver","Welding/Foundry/Forging","HSM Vol. 23 No. 3 May-Jun 2004","44"
    "Book Review: A Sand Casting Manua l -Volume 1","George W. Genevro","Hobby Community","HSM Vol. 23 No. 3 May-Jun 2004","54"
    "Lockable Gib Adjusting Screws for the Mill-Drill","Tim Clarke","Mills","HSM Vol. 23 No. 3 May-Jun 2004","58"
    "Sherline's CNC Mill System","Neil Knopf","Computers","HSM Vol. 23 No. 3 May-Jun 2004","62"
    "The Micro Machinist: Build the Radial Five - Part 7 - Conclusion","Rudy Kouhoupt","Engines","HSM Vol. 23 No. 3 May-Jun 2004","66"
    "Computers in the Shop: CAD Basics - Part Two","Roland W. Friestad","Computers","HSM Vol. 23 No. 3 May-Jun 2004","70"
    "A Rotating Lathe Tailstock Chuck","Peter Stenabaugh","Lathes","HSM Vol. 23 No. 4 Jul-Aug 2004","12"
    "My Delta-T Stirling Engine","Bert de Kat","Engines","HSM Vol. 23 No. 4 Jul-Aug 2004","18"
    "Build a Three-Axis Wood Mill - Part One","James S. McKnight","Shop Machinery","HSM Vol. 23 No. 4 Jul-Aug 2004","22"
    "A Universal Motor Controller","R.G. Sparber","Shop Machinery","HSM Vol. 23 No. 4 Jul-Aug 2004","34"
    "Harry Siebers' Miniature Workbench","Tom Siebers","Shop Accessories","HSM Vol. 23 No. 4 Jul-Aug 2004","42"
    "The New Hand - Discussing Dividers, Calipers, and Trammel Points","Forrest Addy","Shop Accessories","HSM Vol. 23 No. 4 Jul-Aug 2004","44"
    "Granite Surface Plates","David Combs","Shop Accessories","HSM Vol. 23 No. 4 Jul-Aug 2004","52"
    "Book Review: Engineering Formulas for Metalcutting","Neil Knopf","Hobby Community","HSM Vol. 23 No. 4 Jul-Aug 2004","54"
    "Model Ignition Systems - How Much Voltage is Required?","David Bowes","General Machining Knowledge","HSM Vol. 23 No. 4 Jul-Aug 2004","58"
    "It Never Fails! - Raising the Lathe Axis - Part One","Rudy Kouhoupt","Lathes","HSM Vol. 23 No. 4 Jul-Aug 2004","62"
    "Computers in the Shop: CAD Basics - Part Three","Roland W. Friestad","Computers","HSM Vol. 23 No. 4 Jul-Aug 2004","70"
    "Remembering Bob Shores","Neil Knopf","Hobby Community","HSM Vol. 23 No. 5 Sep-Oct 2004","4"
    "Reconditioning a Lathe - Revisited - Part One","Harry Bloom","Lathes","HSM Vol. 23 No. 5 Sep-Oct 2004","12"
    "The Thirteenth Annual Sherline Machinist's Challenge Contest Results","","Hobby Community","HSM Vol. 23 No. 5 Sep-Oct 2004","26"
    "Build a Three-Axis Wood Mill - Part Two","James S. McKnight","Shop Machinery","HSM Vol. 23 No. 5 Sep-Oct 2004","28"
    "Machining a Spiral Cam","Weston Bye","Miscellaneous","HSM Vol. 23 No. 5 Sep-Oct 2004","42"
    "Designing an Adjustable Fly Cutter","Michael Furtado","Mills","HSM Vol. 23 No. 5 Sep-Oct 2004","45"
    "Score in Your Shop With a Hockey Puck","Otto Bacon","Shop Accessories","HSM Vol. 23 No. 5 Sep-Oct 2004","50"
    "The New Hand - Things to Know About Three-jaw Chucks","Forrest Addy","Lathes","HSM Vol. 23 No. 5 Sep-Oct 2004","54"
    "Adding MACH2 CNC Software to the Universal CNC Controller","Roland W. Friestad","Computers","HSM Vol. 23 No. 5 Sep-Oct 2004","62"
    "The Micro Machinist: It Never Fails! - Raising the Lathe Axis - Part Two","Rudy Kouhoupt","Lathes","HSM Vol. 23 No. 5 Sep-Oct 2004","68"
    "Building a Model Engine Camshaft Grinder","Jerry Kieffer","Engines","HSM Vol. 23 No. 6 Nov-Dec 2004","12"
    "Reconditioning a Lathe - Revisited - Part Two","Harry Bloom","Lathes","HSM Vol. 23 No. 6 Nov-Dec 2004","20"
    "Make Mild Steel Behave Like High-carbon Steel","Otto Bacon","General Machining Knowledge","HSM Vol. 23 No. 6 Nov-Dec 2004","32"
    "All Wound Up About Springs","Don Byrnes","Projects","HSM Vol. 23 No. 6 Nov-Dec 2004","36"
    "The New Hand - Things to Know About Four-jaw Chucks","Forrest Addy","Lathes","HSM Vol. 23 No. 6 Nov-Dec 2004","44"
    "Machining the M.L.A. Collet Chuck Kit","Bill McCarthy","Lathes","HSM Vol. 23 No. 6 Nov-Dec 2004","56"
    "Computers in the Shop: Adding MACH2 CNC Software to the Universal CNC Controller - Part Two","Roland W. Friestad","Computers","HSM Vol. 23 No. 6 Nov-Dec 2004","62"
    "Book Review: Patents and Trademarks - Plain & Simple","Craig Foster","Hobby Community","HSM Vol. 23 No. 6 Nov-Dec 2004","68"
    "The Micro Machinist: Make a Holiday Nutcracker","Rudy Kouhoupt","Projects","HSM Vol. 23 No. 6 Nov-Dec 2004","69"
    "A Tribute to Rudy Kouhoupt","Neil Knopf","Hobby Community","HSM Vol. 24 No. 1 Jan-Feb 2005","10"
    "Make an Adjustable Collet Chuck - Part One","Peter Stenabaugh","Machining Accessories","HSM Vol. 24 No. 1 Jan-Feb 2005","14"
    "Abrasive Blasting 101","Gerald Hast","General Machining Knowledge","HSM Vol. 24 No. 1 Jan-Feb 2005","28"
    "Creating a 19th Century Shop","Hunter Davidson","Miscellaneous","HSM Vol. 24 No. 1 Jan-Feb 2005","36"
    "The New Hand: Using Dial Indicators","Forrest Addy","Measuring & Layout","HSM Vol. 24 No. 1 Jan-Feb 2005","44"
    "Router Base Plate for the Wood Mill","James S. McKnight","Shop Machinery","HSM Vol. 24 No. 1 Jan-Feb 2005","52"
    "Reconditioning a Lathe - Revisited - Part Three","Harry Bloom","Machine Tools","HSM Vol. 24 No. 1 Jan-Feb 2005","58"
    "Computers in the Shop: Adding Mach2 CNC Software to the Universal CNC Controller","Roland W. Friestad","Computers","HSM Vol. 24 No. 1 Jan-Feb 2005","70"
    "Build the EVIC-211 Mk1 - A Four-stroke Cycle Twin - Part One","David Bowes","Engines","HSM Vol. 24 No. 2 Mar-Apr 2005","10"
    "Make an Adjustable Collet Chuck - Part Two","Peter Stenabaugh","Machining Accessories","HSM Vol. 24 No. 2 Mar-Apr 2005","18"
    "A CNC Pocket Knife","Steve Archer","Projects","HSM Vol. 24 No. 2 Mar-Apr 2005","30"
    "Repairing and Mounting a Four-jaw Lathe Chuck","James Hannum","Machining Accessories","HSM Vol. 24 No. 2 Mar-Apr 2005","38"
    "Reconditioning a Lathe - Revisited - Part Four","Harry Bloom","Machine Tools","HSM Vol. 24 No. 2 Mar-Apr 2005","48"
    "Inch Precision for the Unimat Lathe","Raymond Hyman","Lathes","HSM Vol. 24 No. 2 Mar-Apr 2005","60"
    "Unimat Drive Belts for Under a Dollar","Raymond Hyman","Machining Accessories","HSM Vol. 24 No. 2 Mar-Apr 2005","62"
    "The New Hand: The Surface Plate and Basic Layout Tools","Forrest Addy","Measuring & Layout","HSM Vol. 24 No. 2 Mar-Apr 2005","66"
    "Computers in the Shop: Convert a Rotary Table to CNC","Roland W. Friestad","Computers","HSM Vol. 24 No. 2 Mar-Apr 2005","74"
    "Down-Feed Attachment for the Grizzly Mill-Drill","Roger Hallbach","Machining Accessories","HSM Vol. 24 No. 3 May-Jun 2005","12"
    "An Automatic Carriage Stop for Thread Cutting","Jim McKee","Machining Accessories","HSM Vol. 24 No. 3 May-Jun 2005","18"
    "Modifications to the Grizzly 13 x 40 Lathe","Lionel Gard","Machine Tools","HSM Vol. 24 No. 3 May-Jun 2005","26"
    "Fabricating a South Bend Cross-feed Screw","Walter Yetman","Machining Accessories","HSM Vol. 24 No. 3 May-Jun 2005","36"
    "Review of the Nano-Tram","Nick Carter","Hobby Community","HSM Vol. 24 No. 3 May-Jun 2005","42"
    "The New Hand - Twist Drill Lore","Forrest Addy","General Machining Knowledge","HSM Vol. 24 No. 3 May-Jun 2005","48"
    "Build the EVIC-211 Mk1 - A Four-stroke Cycle Twin - Part Two","David Bowes","Engines","HSM Vol. 24 No. 3 May-Jun 2005","58"
    "Improved Quill Stop for the Delta Bench Drill Press","E. I. Schefer","Machining Accessories","HSM Vol. 24 No. 3 May-Jun 2005","64"
    "Organizing Your Tool Box","J. Randolph Bulgin","Miscellaneous","HSM Vol. 24 No. 3 May-Jun 2005","67"
    "Computers in the Shop: A Flood Coolant Enclosure for your Bridgeport CNC Milling Machine","Roland W. Friestad","Computers","HSM Vol. 24 No. 3 May-Jun 2005","70"
    "Build a Cross-slide Rotary Table - Part One","Dennis Zefran","Machining Accessories","HSM Vol. 24 No. 4 Jul-Aug 2005","10"
    "Build the Crusader .60 - Part One","George W. Genevro","Engines","HSM Vol. 24 No. 4 Jul-Aug 2005","20"
    "Automated CNC Milling and Prototyping","Richard Sideritz","Computers","HSM Vol. 24 No. 4 Jul-Aug 2005","30"
    "Lathe Chuck Wrench Holder","Robert L. Bailey","Machining Accessories","HSM Vol. 24 No. 4 Jul-Aug 2005","34"
    "A Pneumatic Comparator","Bob Knapp","Measuring & Layout","HSM Vol. 24 No. 4 Jul-Aug 2005","36"
    "Build the EVIC-211 Mk1 - A Four-stroke Cycle Twin - Part Three","David Bowes","Engines","HSM Vol. 24 No. 4 Jul-Aug 2005","44"
    "Squaring or Tramming a Basic Vertical Mill","James Murnaghen","Machining Accessories","HSM Vol. 24 No. 4 Jul-Aug 2005","54"
    "Steve Pierce Wins 2005 Sherline Challenge","Craig Libuse","Hobby Community","HSM Vol. 24 No. 4 Jul-Aug 2005","59"
    "Book Review: Machine Shop Trade Secrets - Harvey, Industrial Press","Craig Foster","Hobby Community","HSM Vol. 24 No. 4 Jul-Aug 2005","60"
    "Book Review: Making Pistons for Experimental and Restoration Engines - Chastain","Steve Acker","Hobby Community","HSM Vol. 24 No. 4 Jul-Aug 2005","61"
    "Tool Blocks","William Johnson","Machining Accessories","HSM Vol. 24 No. 4 Jul-Aug 2005","62"
    "The New Hand: Getting Smart on Home Shop Compressors","Forrest Addy","General Machining Knowledge","HSM Vol. 24 No. 4 Jul-Aug 2005","66"
    "Computers in the Shop: The New and Improved Universal CNC Controller - Part One","Roland W. Friestad","Computers","HSM Vol. 24 No. 4 Jul-Aug 2005","72"
    "A Lead Screw Handwheel Design for a Grizzly Lathe","Cristie Rethman","Lathes","HSM Vol. 24 No. 5 Sep-Oct 2005","10"
    "Repairing a Dumore No. 5 Motor","Steve Acker","Motors","HSM Vol. 24 No. 5 Sep-Oct 2005","32"
    "Hook Up an SFM Meter","Jerry Pontius","Measuring & Layout","HSM Vol. 24 No. 5 Sep-Oct 2005","38"
    "Review of the A2Z CNC Quick-Change Tool Post","Nick Carter","Hobby Community","HSM Vol. 24 No. 5 Sep-Oct 2005","42"
    "A Sherline Headstock on an Atlas Bench Mill","Richard Zielike","Machine Modifications","HSM Vol. 24 No. 5 Sep-Oct 2005","58"
    "Build the Crusader .60","George W. Genevro","Engines","HSM Vol. 24 No. 5 Sep-Oct 2005","62"
    "Computers in the Shop: The New and Improved Universal CNC Controller - Part Two","Roland W. Friestad","Computers","HSM Vol. 24 No. 5 Sep-Oct 2005","76"
    "Build a Horizontal Stirling Engine","Terry Coss","Engines","HSM Vol. 24 No. 6 Nov-Dec 2005","10"
    "A Veteran's Tribute","Walter Yetman","Hobby Community","HSM Vol. 24 No. 6 Nov-Dec 2005","22"
    "Upgrading an Atlas 10F Lathe","Ken Hollenbeck","Lathes","HSM Vol. 24 No. 6 Nov-Dec 2005","30"
    "What Happens to the Masterpiece?","T Parkinson","Hobby Community","HSM Vol. 24 No. 6 Nov-Dec 2005","36"
    "What Happens to the Masterpiece?","T Parkinson","Hobby Community","HSM Vol. 24 No. 6 Nov-Dec 2005","36"
    "What Happens to The Masterpiece?","T Parkinson","Hobby Community","HSM Vol. 24 No. 6 Nov-Dec 2005","36"
    "Slim Down Your Four-Jaw Chuck","Allan Moore","Lathes","HSM Vol. 24 No. 6 Nov-Dec 2005","42"
    "Build the EVIC-211 Mk1 - A Four-stroke Cycle Twin - Part Five","David Bowes","Engines","HSM Vol. 24 No. 6 Nov-Dec 2005","48"
    "Review of the Thin Parallels Set from Travers Tool","Stephen G. Wellcome","Machine Tools","HSM Vol. 24 No. 6 Nov-Dec 2005","57"
    "Build the Crusader .60 - Part Three","George W. Genevro","Engines","HSM Vol. 24 No. 6 Nov-Dec 2005","58"
    "The New Hand: A Series for the Novice - ABC's of AC Induction Motors - Part One","Forrest Addy","Motors","HSM Vol. 24 No. 6 Nov-Dec 2005","68"
    "Computers in the Shop: The New and Improved Universal CNC Controller - Part Three","Roland W. Friestad","Computers","HSM Vol. 24 No. 6 Nov-Dec 2005","78"
    "Build an English Wheel - The Crowning Touch: Part One","Peter Stenabaugh","Shop Accessories","HSM Vol. 25 No. 1 Jan-Feb 2006","10"
    "A Simple Mill-Drill Spindle Lock","James A. Hornicek","Machine Tools","HSM Vol. 25 No. 1 Jan-Feb 2006","20"
    "Easy Grinder Adjustment","Joe Matter","Shop Machinery","HSM Vol. 25 No. 1 Jan-Feb 2006","22"
    "Optics for Micro Machining","Jerry Kieffer","Machining Accessories","HSM Vol. 25 No. 1 Jan-Feb 2006","26"
    "Build the EVIC-211 Mk1 - A Four-stroke Cycle Twin - Part Six","David Bowes","Engines","HSM Vol. 25 No. 1 Jan-Feb 2006","38"
    "Build the Crusader .60 - Part Four","George W. Genevro","Engines","HSM Vol. 25 No. 1 Jan-Feb 2006","50"
    "A Halogen Light for Your Inspection Table","Otto Bacon","Shop Accessories","HSM Vol. 25 No. 1 Jan-Feb 2006","56"
    "The New Hand: A Series for the Novice - ABC's of AC Induction motors - Part Two","Forrest Addy","Engines","HSM Vol. 25 No. 1 Jan-Feb 2006","58"
    "David Kucer wins 2006 Outstanding Metalworking Craftsman Award","","Hobby Community","HSM Vol. 25 No. 2 Mar-Apr 2006","12"
    "Rudy's Balanced Knurling Tool with a Twist","Steve Kinsey","Shop Accessories","HSM Vol. 25 No. 2 Mar-Apr 2006","14"
    "Shop Knives from Files","Steve Acker","Projects","HSM Vol. 25 No. 2 Mar-Apr 2006","24"
    "Build an English Wheel - The Crowning Touch: Part Two","Peter Stenabaugh","Shop Accessories","HSM Vol. 25 No. 2 Mar-Apr 2006","32"
    "An Accurate Measurement for your Vertical Milling Operations","Wil Nise","Measuring & Layout","HSM Vol. 25 No. 2 Mar-Apr 2006","38"
    "Build the Crusader .60","George W. Genevro","Engines","HSM Vol. 25 No. 2 Mar-Apr 2006","42"
    "Build the EVIC-211 Mk1 - A Four-stroke Cycle Twin - Part Seven","David Bowes","Engines","HSM Vol. 25 No. 2 Mar-Apr 2006","50"
    "Installing a Grizzly DRO on a Mill-Drill","Erick Peterson","Machine Modifications","HSM Vol. 25 No. 2 Mar-Apr 2006","56"
    "A Lathe Ben Dial Indicator","Robert L. Bailey","Lathes","HSM Vol. 25 No. 2 Mar-Apr 2006","60"
    "Computers in the Shop: Fundamentals of CNC Programming - Part One","Roland W. Friestad","Computers","HSM Vol. 25 No. 2 Mar-Apr 2006","64"
    "The Home Machinist's Surface Grinder - Part One","Robert Byler","Shop Machinery","HSM Vol. 25 No. 3 May-Jun 2006","10"
    "An MLA Tool Post","A. J. Lofquist","Lathes","HSM Vol. 25 No. 3 May-Jun 2006","24"
    "Cutting Threads on a Lathe - 101","Michael Gelcius","Lathes","HSM Vol. 25 No. 3 May-Jun 2006","34"
    "Build an English Wheel - The Crowning Touch: Part Three","Peter Stenabaugh","Shop Accessories","HSM Vol. 25 No. 3 May-Jun 2006","42"
    "Build the EVIC-211 Mk1 - A Four-stroke Cycle Twin - Part Eight","David Bowes","Engines","HSM Vol. 25 No. 3 May-Jun 2006","50"
    "The Finger Engine","T Parkinson","Engines","HSM Vol. 25 No. 3 May-Jun 2006","58"
    "Lathe Spindle Stop","Gary Vriezen","Lathes","HSM Vol. 25 No. 3 May-Jun 2006","62"
    "Daul Die Lathe Tool","Thomas M. Verity","Lathes","HSM Vol. 25 No. 3 May-Jun 2006","66"
    "Computers in the Shop: Fundamentals of CNC Programming - Part Two","Roland W. Friestad","Computers","HSM Vol. 25 No. 3 May-Jun 2006","72"
    "Tanks for Model Engines","George W. Genevro","Engines","HSM Vol. 25 No. 4 Jul-Aug 2006","10"
    "The Home Shop Machinist's Surface Grinder - Part Two","Robert Byler","Shop Machinery","HSM Vol. 25 No. 4 Jul-Aug 2006","20"
    "Build the EVIC-211 Mk1: A Four-stroke Cycle Twin - Part Nine","David Bowes","Engines","HSM Vol. 25 No. 4 Jul-Aug 2006","28"
    "Grand Opening of the Joe Martin Foundation Museum of Craftsmanship","Neil Knopf","Hobby Community","HSM Vol. 25 No. 4 Jul-Aug 2006","36"
    "Hot-Rodding a 9"" South Bend Lathe","Peter Verbree","Lathes","HSM Vol. 25 No. 4 Jul-Aug 2006","38"
    "Combined Tool for Finder Edges and Centers","Mogens Kilde","Shop Accessories","HSM Vol. 25 No. 4 Jul-Aug 2006","46"
    "Build an English Wheel - The Crowning Touch - Part Four","Peter Stenabaugh","Shop Accessories","HSM Vol. 25 No. 4 Jul-Aug 2006","52"
    "The New Hand: Setting Angles","Kilgore-Bauer Nona","Techniques","HSM Vol. 25 No. 4 Jul-Aug 2006","64"
    "Carriage Indicator","Fred Prestridge","Lathes","HSM Vol. 25 No. 4 Jul-Aug 2006","74"
    "Computers in the Shop: The Universal CNC Controller Revisited Again - Part One","Roland W. Friestad","Computers","HSM Vol. 25 No. 4 Jul-Aug 2006","78"
    "Installing a Power Feed on a Small Knee Mill","Richard L Kruger","Machine Modifications","HSM Vol. 25 No. 5 Sep-Oct 2006","8"
    "Building a Riser Block for a Burke Powermatic Millrite Mill","Chuck Materna","Machine Modifications","HSM Vol. 25 No. 5 Sep-Oct 2006","16"
    "Improved Grooving Tool for the Lathe","Edward Hume","Lathes","HSM Vol. 25 No. 5 Sep-Oct 2006","24"
    "A Tiny Sterling Engine","Bert de Kat","Engines","HSM Vol. 25 No. 5 Sep-Oct 2006","30"
    "The Home Machinist's Surface Grinder - Part Three","Robert Byler","Shop Machinery","HSM Vol. 25 No. 5 Sep-Oct 2006","42"
    "Build an English Wheel - The Crowning Touch - Part Five","Peter Stenabaugh","Shop Accessories","HSM Vol. 25 No. 5 Sep-Oct 2006","50"
    "The New Hand: Points to Consider - Tool Posts for Engine Lathes","Kilgore-Bauer Nona","Lathes","HSM Vol. 25 No. 5 Sep-Oct 2006","58"
    "Computers in the Shop: The Universal CNC Controller Revisited Again - Part Two","Roland W. Friestad","Computers","HSM Vol. 25 No. 5 Sep-Oct 2006","68"
    "Build the Snow - A Tandem, Double-Acting Engine - Part One","Douglas Kelley","Engines","HSM Vol. 25 No. 6 Nov-Dec 2006","10"
    "Quick-Adjusting Boring Head","James S. McKnight","Shop Accessories","HSM Vol. 25 No. 6 Nov-Dec 2006","18"
    "A Simple Clutch-Connector for the Mini-Mill Power Table Feed","John Krueger","Machine Modifications","HSM Vol. 25 No. 6 Nov-Dec 2006","24"
    "The NAMES Top","T Parkinson","Projects","HSM Vol. 25 No. 6 Nov-Dec 2006","30"
    "Make an Overarm Brace for a Clausing Horizontal Mill","Jim Swartz","Machine Modifications","HSM Vol. 25 No. 6 Nov-Dec 2006","36"
    "Cut-Off Tool","Theodore M. Clarke","Shop Accessories","HSM Vol. 25 No. 6 Nov-Dec 2006","42"
    "Bridgeport-type Quick-Release Quill Handle Adapted for a Small Mill","Reed Streifthau","Machine Modifications","HSM Vol. 25 No. 6 Nov-Dec 2006","46"
    "Build an English Wheel - The Crowning Touch - Part Six","Peter Stenabaugh","Shop Accessories","HSM Vol. 25 No. 6 Nov-Dec 2006","50"
    "Cast Name Plate","Otto Bacon","Miscellaneous","HSM Vol. 25 No. 6 Nov-Dec 2006","58"
    "Setting and Using the Taper Attachment on a South Bend Lathe","Paul J. Holm","Lathes","HSM Vol. 25 No. 6 Nov-Dec 2006","62"
    "A Quick and Cheap Surface Gauge","Don Byrnes","Shop Accessories","HSM Vol. 25 No. 6 Nov-Dec 2006","66"
    "Micrometers Revealed","Bob Hadley","Measuring & Layout","HSM Vol. 25 No. 6 Nov-Dec 2006","68"
    "Computers in the Shop: The Universal CNC Controller Revisited Again - Part Three","Roland W. Friestad","Computers","HSM Vol. 25 No. 6 Nov-Dec 2006","72"
    "The New Hand: Points to Consider - Tool Posts for Engine Lathes - Part Two","Kilgore-Bauer Nona","Lathes","HSM Vol. 25 No. 6 Nov-Dec 2006","80"
    "Easy Rotary Table - Part One","Fred Prestridge","Shop Machinery","HSM Vol. 26 No. 1 Jan-Feb 2007","16"
    "Upgrading a Drill Press Cradle-Style Vise for Precision Shaping and Milling","Theodore M. Clarke","Machine Modifications","HSM Vol. 26 No. 1 Jan-Feb 2007","26"
    "Line Boring a South Bend Lathe Headstock","Jack Butz","Lathes","HSM Vol. 26 No. 1 Jan-Feb 2007","32"
    "Steve Pierce Makes it Two in a Row","Craig Libuse","Hobby Community","HSM Vol. 26 No. 1 Jan-Feb 2007","38"
    "A Handy Tool for Cutting Screws to Length","Mogens Kilde","Hand Tools","HSM Vol. 26 No. 1 Jan-Feb 2007","42"
    "Remanufactured Impeller Housing","Robert Shosh","Shop Machinery","HSM Vol. 26 No. 1 Jan-Feb 2007","46"
    "Build the Snow - A Tandem, Double-Acting Engine - Part Two","Douglas Kelley","Engines","HSM Vol. 26 No. 1 Jan-Feb 2007","50"
    "Mounts for Model Engines","George W. Genevro","Engines","HSM Vol. 26 No. 1 Jan-Feb 2007","60"
    "SafeStop Switch","Bob Beecroft","General Machining Knowledge","HSM Vol. 26 No. 1 Jan-Feb 2007","66"
    "Computers in the Shop: The Universal CNC Controller Revisited Again - Part Four","Roland W. Friestad","Computers","HSM Vol. 26 No. 1 Jan-Feb 2007","68"
    "The Home Shop Machinist Celebrates its 25th Birthday","Craig Foster","Hobby Community","HSM Vol. 26 No. 1 Jan-Feb 2007","71"
    "Bench Top Band Saw","John Gjertsen","Shop Machinery","HSM Vol. 26 No. 2 Mar-Apr 2007","10"
    "Build the Snow - A Tandem, Double-acting Engine - Part Three","Douglas Kelley","Engines","HSM Vol. 26 No. 2 Mar-Apr 2007","24"
    "The Crankless Michell Engine","Clif Roemmich","Hobby Community","HSM Vol. 26 No. 2 Mar-Apr 2007","36"
    "East Rotary Table - Part Two","Fred Prestridge","Shop Machinery","HSM Vol. 26 No. 2 Mar-Apr 2007","42"
    "Stud Drive for Hurricane Plywood","Allan Moore","Miscellaneous","HSM Vol. 26 No. 2 Mar-Apr 2007","52"
    "Micrometer Stop for a Miter Saw","Jim Gavin","Shop Machinery","HSM Vol. 26 No. 2 Mar-Apr 2007","54"
    "Computers in the Shop: CNC Retrofit for the Grizzly G1006 Benchtop Mill - Part One","Roland W. Friestad","Computers","HSM Vol. 26 No. 2 Mar-Apr 2007","66"
    "Shopsmith Adventures - Converting a Shopsmith to Cut Metal - Part One","Robert L. Bailey","Shop Machinery","HSM Vol. 26 No. 3 May-Jun 2007","10"
    "Easy Rotary Table - Part Three, Conclusion","Fred Prestridge","Shop Machinery","HSM Vol. 26 No. 3 May-Jun 2007","22"
    "Pierre Scerri Wins Joe Martin Foundation's Outstanding Metalworking Craftsman Award for 2007","Craig Libuse","Hobby Community","HSM Vol. 26 No. 3 May-Jun 2007","33"
    "Expanding Thread Cutting Options on Lathes with Quick-Change Gears","Kim Steiner","Lathes","HSM Vol. 26 No. 3 May-Jun 2007","36"
    "Build the Snow - A Tandem, Double-acting Engine - Part Four, Conclusion","Douglas Kelley","Engines","HSM Vol. 26 No. 3 May-Jun 2007","44"
    "An Improved Drawbar for an RF 30 Mill-Drill","R.G. Sparber","Machine Modifications","HSM Vol. 26 No. 3 May-Jun 2007","56"
    "Computers in the Shop: CNC Retrofit for the Grizzly G1006 Benchtop Mill - Part Two","Roland W. Friestad","Computers","HSM Vol. 26 No. 3 May-Jun 2007","66"
    "Pneumatic Power Shapes Sheet Metal (2007 Bonus Issue)","Kent White","Miscellaneous","HSM Vol. 26 No. 4 Jul-Aug 2007","6"
    "The Four Inch Engine - Part One","Jerry Pontius","Engines","HSM Vol. 26 No. 4 Jul-Aug 2007","10"
    "New Dials for Older Machines","Jan Michaels","Machine Modifications","HSM Vol. 26 No. 4 Jul-Aug 2007","22"
    "Setting up a Lathe","John Robinson","Techniques","HSM Vol. 26 No. 4 Jul-Aug 2007","32"
    "Roller Blocks on a Steady Rest","Allan Moore","Machining Accessories","HSM Vol. 26 No. 4 Jul-Aug 2007","42"
    "Shopsmith Adventures - Converting a Shopsmith to Cut Metal - Part Two","Robert L. Bailey","Shop Machinery","HSM Vol. 26 No. 4 Jul-Aug 2007","46"
    "Retrofitting a Flat-belt Grinder with a V-belt Drive","Bob Neidorff","Shop Machinery","HSM Vol. 26 No. 4 Jul-Aug 2007","56"
    "Installing a Power Feed to a Burke Powermatic Millrite Mill","Chuck Materna","Machine Modifications","HSM Vol. 26 No. 4 Jul-Aug 2007","62"
    "Computers in the Shop: CNC Retrofit for the Grizzly G1006 Benchtop Mill - Part Three","Roland W. Friestad","Computers","HSM Vol. 26 No. 4 Jul-Aug 2007","70"
    "Cut-off Tool for the 6 Atlas Lathe","John Bergmann","Lathes","HSM Vol. 26 No. 5 Sep-Oct 2007","10"
    "On the Cutting Edge: Understanding Drill Sharpening","Matthew J. Russel","General Machining Knowledge","HSM Vol. 26 No. 5 Sep-Oct 2007","18"
    "Micrometer Stop for a Grizzly 4000 Lathe","David Bradley","Lathes","HSM Vol. 26 No. 5 Sep-Oct 2007","34"
    "The Four Inch Engine - Part Two","Jerry Pontius","Engines","HSM Vol. 26 No. 5 Sep-Oct 2007","42"
    "Shopsmith Adventures - Converting a Shopsmith to Cut Metal - Part Three, Drill Sharpener Improvement","Robert L. Bailey","Shop Machinery","HSM Vol. 26 No. 5 Sep-Oct 2007","54"
    "Computers in the Shop: Third Annual CNC Workshop","Roland W. Friestad","Hobby Community","HSM Vol. 26 No. 5 Sep-Oct 2007","66"
    "Iqbal Ahmed Claims First Place","Craig Libuse","Hobby Community","HSM Vol. 26 No. 5 Sep-Oct 2007","70"
    "My Universal Pillar Tool","Fred Prestridge","Shop Accessories","HSM Vol. 26 No. 6 Nov-Dec 2007","10"
    "Cutting Metric Threads","James Hubbell","Techniques","HSM Vol. 26 No. 6 Nov-Dec 2007","22"
    "Small Puller for Dismantling a Miniature Engine","Mogens Kilde","Engines","HSM Vol. 26 No. 6 Nov-Dec 2007","30"
    "Notes from Building a Nine-cylinder Radial Engine","gerald baxter","Hobby Community","HSM Vol. 26 No. 6 Nov-Dec 2007","36"
    "The Four Inch Engine - Part Three","Jerry Pontius","Engines","HSM Vol. 26 No. 6 Nov-Dec 2007","42"
    "Shopsmith Adventures - Converting a Shopsmith to Cut Metal - Part Four","Robert L. Bailey","Shop Machinery","HSM Vol. 26 No. 6 Nov-Dec 2007","48"
    "Computers in the Shop: Retrofitting a Benchtop Lathe with Ball Screws - Part One","Roland W. Friestad","Computers","HSM Vol. 26 No. 6 Nov-Dec 2007","66"
    "Making Miniature Taps and Dies","Jerry Kieffer","Techniques","HSM Vol. 27 No. 1 Jan-Feb 2008","8"
    "Modifying the Phoenix Miller Part One","Thomas Morrison","Machine Modifications","HSM Vol. 27 No. 1 Jan-Feb 2008","18"
    "An Easy Nutcracker","Bernard Cooper","Projects","HSM Vol. 27 No. 1 Jan-Feb 2008","32"
    "Vertical Storage - Extra Duty for the Mill","F Kaisler","Mills","HSM Vol. 27 No. 1 Jan-Feb 2008","38"
    "Added Feature to Andy's Quick-change Tool Post","Bob Hadley","Lathes","HSM Vol. 27 No. 1 Jan-Feb 2008","44"
    "A Six-sided Block for 3C Collets","Jerrold Tiers","Lathes","HSM Vol. 27 No. 1 Jan-Feb 2008","50"
    "Restoration of an Antique Pressure Gauge","Bill Lindsey","Miscellaneous","HSM Vol. 27 No. 1 Jan-Feb 2008","54"
    "The Four Inch Engine - Part Four","Jerry Pontius","Engines","HSM Vol. 27 No. 1 Jan-Feb 2008","58"
    "Retrofitting a Benchtop Lathe with Ball Screws - Part Two","Roland W. Friestad","Computers","HSM Vol. 27 No. 1 Jan-Feb 2008","68"
    "Caliper Helper","Don Peterson","Measuring & Layout","HSM Vol. 27 No. 1 Jan-Feb 2008","73"
    "The Finger Brake - Part One","Michael Ward","Machine Tools","HSM Vol. 27 No. 2 Mar-Apr 2008","12"
    "Jacot Drum - A Clockmaking/Repair Accessory for a Sherline Lathe","Ronald G. Casteel","Clocks","HSM Vol. 27 No. 2 Mar-Apr 2008","28"
    "Precision without Measurement - Indexing a Swivel Base Vise","Frank Ford","Techniques","HSM Vol. 27 No. 2 Mar-Apr 2008","34"
    "Lathe Carriage Stop","Allan Moore","Lathes","HSM Vol. 27 No. 2 Mar-Apr 2008","38"
    "Modifying the Phoenix Miller - Part Two","Thomas Morrison","Machine Modifications","HSM Vol. 27 No. 2 Mar-Apr 2008","42"
    "Couple of Hacks for the Ubiquitous 4 x 6 Metal-cutting Band Saw","Greg Saville","Shop Machinery","HSM Vol. 27 No. 2 Mar-Apr 2008","50"
    "The Four Inch Engine - Part Five","Jerry Pontius","Engines","HSM Vol. 27 No. 2 Mar-Apr 2008","52"
    "Computers in the Shop: Retrofitting a Benchtop Lathe with Ball Screws - Part Three","Roland W. Friestad","Computers","HSM Vol. 27 No. 2 Mar-Apr 2008","58"
    "A Problem in Restoring an Old Cadillac","John W. Foster","Miscellaneous","HSM Vol. 27 No. 2 Mar-Apr 2008","66"
    "Tapping Technique for Tilted Holes","Marcelo Jost","Techniques","HSM Vol. 27 No. 2 Mar-Apr 2008","70"
    "Taper Attachment for Atlas 10/12 Lathes","John Ehler","Lathes","HSM Vol. 27 No. 3 May-Jun 2008","10"
    "A Spindle Adapter","Fred Prestridge","Machine Modifications","HSM Vol. 27 No. 3 May-Jun 2008","24"
    "A Cane for Eva","Leo Radovich","Projects","HSM Vol. 27 No. 3 May-Jun 2008","32"
    "Ron Colonna - 2008 Metalworking Craftsman of the Year","Craig Libuse","Hobby Community","HSM Vol. 27 No. 3 May-Jun 2008","38"
    "Improvements for The Home Shop Machinist Phase Converter","Robert Byler","Miscellaneous","HSM Vol. 27 No. 3 May-Jun 2008","42"
    "The Finger Brake - Part Two","Michael Ward","Shop Accessories","HSM Vol. 27 No. 3 May-Jun 2008","46"
    "Modifying the Phoenix Miller - Part Three","Thomas Morrison","Machine Modifications","HSM Vol. 27 No. 3 May-Jun 2008","58"
    "Computers in the Shop: Retrofitting a Benchtop Lathe with Ball Screws - Part Four","Roland W. Friestad","Computers","HSM Vol. 27 No. 3 May-Jun 2008","68"
    "Build a Miniature Side Lever Steam Engine - Part One","Mogens Kilde","Engines","HSM Vol. 27 No. 4 Jul-Aug 2008","14"
    "Add a Leadscrew Reverse to your 9 x 20 Lathe","James A. Hornicek","Lathes","HSM Vol. 27 No. 4 Jul-Aug 2008","26"
    "Make Your Own Arbors","Jerrold Tiers","Machine Modifications","HSM Vol. 27 No. 4 Jul-Aug 2008","34"
    "Some Thoughts on Machining Titanium","Doug Ripka","Techniques","HSM Vol. 27 No. 4 Jul-Aug 2008","42"
    "The Finger Brake - Part Three","Michael Ward","Shop Accessories","HSM Vol. 27 No. 4 Jul-Aug 2008","48"
    "Taper Attachment for Atlas 10/12 Lathes - Part Two","John Ehler","Lathes","HSM Vol. 27 No. 4 Jul-Aug 2008","64"
    "Cutting Dovetails on the Fly","Andrew Wakefield","Techniques","HSM Vol. 27 No. 5 Sep-Oct 2008","14"
    "High-Speed Spindle - Part One","Jerry Pontius","Machine Modifications","HSM Vol. 27 No. 5 Sep-Oct 2008","26"
    "Precision Grinding Vise","James S. McKnight","Shop Accessories","HSM Vol. 27 No. 5 Sep-Oct 2008","36"
    "Rolling Along with the Wheel","Kent White","Techniques","HSM Vol. 27 No. 5 Sep-Oct 2008","42"
    "Permanent Indicator Mount for a Sherline Lathe","Marcelo Jost","Lathes","HSM Vol. 27 No. 5 Sep-Oct 2008","54"
    "Taper Attachment for Atlas 10/12 Lathes - Part Three","John Ehler","Lathes","HSM Vol. 27 No. 5 Sep-Oct 2008","58"
    "Build a Miniature Side Lever Steam Engine - Part Two","Mogens Kilde","Engines","HSM Vol. 27 No. 5 Sep-Oct 2008","70"
    "A Pneumatic Locking Lathe Turret","Jerry Pryor","Machine Modifications","HSM Vol. 27 No. 6 Nov-Dec 2008","12"
    "Rescuing Stock too Short to be Saved","Weston Bye","Techniques","HSM Vol. 27 No. 6 Nov-Dec 2008","26"
    "Producing an Internal Bore around Corners","Richard Carlstedt","Techniques","HSM Vol. 27 No. 6 Nov-Dec 2008","32"
    "Lathe Setup for Accurate Tapers","Reid Kowallis","Techniques","HSM Vol. 27 No. 6 Nov-Dec 2008","42"
    "Build a Miniature Side Lever Steam Engine - Part Three","Mogens Kilde","Engines","HSM Vol. 27 No. 6 Nov-Dec 2008","48"
    "A High-Speed Spindle - Part Two","Jerry Pontius","Machine Modifications","HSM Vol. 27 No. 6 Nov-Dec 2008","60"
    "Create a Hydraulic Lift Assembly - Cheap and Easy","Ken Sevene","Shop Accessories","HSM Vol. 27 No. 6 Nov-Dec 2008","74"
    "A Tangential Toolholder for a Sherline Lathe","Marcelo Jost","Lathes","HSM Vol. 28 No. 1 Jan-Feb 2009","12"
    "Setting Up Accurate Angles - Inexpensively","Paul Alciatore","General Machining Knowledge","HSM Vol. 28 No. 1 Jan-Feb 2009","30"
    "Randolph's Shop Class: Squaring, or Tramming, the Mill Head","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 28 No. 1 Jan-Feb 2009","36"
    "Installing a Power Feed to the Quill of a Burke Powermatic Millrite Mill","Chuck Materna","Mills","HSM Vol. 28 No. 1 Jan-Feb 2009","42"
    "Logan Lathes","Bob Neidorff","Lathes","HSM Vol. 28 No. 1 Jan-Feb 2009","52"
    "Chain Drive for a Mill-Drill X-axis","Peter Merriam","Shop Machinery","HSM Vol. 28 No. 1 Jan-Feb 2009","60"
    "Security in the Home Shop","","Hobby Community","HSM Vol. 28 No. 1 Jan-Feb 2009","66"
    "Retrofitting a Benchtop Lathe with Ball Screws - Conclusion","Roland W. Friestad","Lathes","HSM Vol. 28 No. 1 Jan-Feb 2009","68"
    "Precision Router Table - Part One","Jim Gavin","Shop Accessories","HSM Vol. 28 No. 2 Mar-Apr 2009","10"
    "Chaotic Double Pendulum","James Donnelly","Projects","HSM Vol. 28 No. 2 Mar-Apr 2009","24"
    "Making Headroom","Fred Prestridge","Mills","HSM Vol. 28 No. 2 Mar-Apr 2009","38"
    "Making Headroom","Fred Prestridge","Shop Accessories","HSM Vol. 28 No. 2 Mar-Apr 2009","38"
    "Building an Atlas Lathe Carriage Dial Indicator and Clamp Assembly","Gary Paine","Lathes","HSM Vol. 28 No. 2 Mar-Apr 2009","42"
    "Installing a Power Feed to the Quill of a Burke Powermatic Millrite Mill - Part 2","Chuck Materna","Mills","HSM Vol. 28 No. 2 Mar-Apr 2009","46"
    "Randolph's Shop Class: Soft Jaws","J. Randolph Bulgin","Shop Accessories","HSM Vol. 28 No. 2 Mar-Apr 2009","54"
    "An Internal Expanding Mandrel for the Lathe","James Hannum","Lathes","HSM Vol. 28 No. 2 Mar-Apr 2009","58"
    "Balance Your Wheel Once - Part One","Charles St. Louis","Shop Accessories","HSM Vol. 28 No. 3 May-Jun 2009","10"
    "Ball Turner","Jan Michaels","Lathes","HSM Vol. 28 No. 3 May-Jun 2009","20"
    "The Odd Screw","Paul J. Holm","Lathes","HSM Vol. 28 No. 3 May-Jun 2009","34"
    "Polarizing Filter for a Pocket Camera","Bob Hadley","Projects","HSM Vol. 28 No. 3 May-Jun 2009","38"
    "Richard Carlstedt - 2009 Metalworking Craftsman of the Year","Craig Libuse","Hobby Community","HSM Vol. 28 No. 3 May-Jun 2009","38"
    "A Side-by-Side Horizontal","Douglas Kelley","Engines","HSM Vol. 28 No. 3 May-Jun 2009","48"
    "Stamp Holder","Thomas M. Verity","Projects","HSM Vol. 28 No. 3 May-Jun 2009","52"
    "Precision Router Table - Part Two","Jim Gavin","Shop Machinery","HSM Vol. 28 No. 3 May-Jun 2009","54"
    "Randolph's Shop Class: Turning Between Centers","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 28 No. 3 May-Jun 2009","64"
    "Quick-change Jaw System for the Bench Vise - Part One","Michael Ward","Shop Accessories","HSM Vol. 28 No. 4 Jul-Aug 2009","14"
    "My Six Favorite Shop Made Tools","Ted Hansen","Shop Accessories","HSM Vol. 28 No. 4 Jul-Aug 2009","29"
    "Builder's Notes on Rudy Kouhoupt's Steam Tractor","Ronald G. Casteel","Engines","HSM Vol. 28 No. 4 Jul-Aug 2009","32"
    "Quick Clamp","Leo Radovich","Shop Machinery","HSM Vol. 28 No. 4 Jul-Aug 2009","38"
    "Randolph's Shop Class: The Rotary Table","J. Randolph Bulgin","Shop Machinery","HSM Vol. 28 No. 4 Jul-Aug 2009","40"
    "Balance Your Wheel Once - Part Two","Charles St. Louis","Shop Accessories","HSM Vol. 28 No. 4 Jul-Aug 2009","48"
    "Precision Router Table, Part Three","Jim Gavin","Shop Accessories","HSM Vol. 28 No. 4 Jul-Aug 2009","62"
    "17 Reasons to Love the Oxy-Acetylene Torch (or How to Use Pyrotechnics to your Best Advantage) Part One","Kent White","Welding/Foundry/Forging","HSM Vol. 28 No. 5 Sep-Oct 2009","12"
    "Building a Large, Beam-type Steam Engine - Part One","Brian Rupnow","Engines","HSM Vol. 28 No. 5 Sep-Oct 2009","22"
    "Scott LaBombard Wins 2009 Sherline Machinist's Challenge","Craig Libuse","Hobby Community","HSM Vol. 28 No. 5 Sep-Oct 2009","38"
    "Making a Larger Cross-feed Dial for a Logan Lathe","Bob Neidorff","Lathes","HSM Vol. 28 No. 5 Sep-Oct 2009","42"
    "Randolph's Shop Class: Speeds and Feeds","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 28 No. 5 Sep-Oct 2009","50"
    "Quick-change Jaw System for the Bench Vise - Part Two","Michael Ward","Shop Accessories","HSM Vol. 28 No. 5 Sep-Oct 2009","54"
    "Precision Router Table - Part Four","Jim Gavin","Shop Accessories","HSM Vol. 28 No. 5 Sep-Oct 2009","68"
    "New Life for Old Collets","Paul J. Holm","Lathes","HSM Vol. 28 No. 6 Nov-Dec 2009","10"
    "Variable Speed for Your Power Tools - A DC Motor and Controller","Jerry Pryor","Shop Machinery","HSM Vol. 28 No. 6 Nov-Dec 2009","22"
    "Duplicating on a Metal Lathe","Gary Paine","Lathes","HSM Vol. 28 No. 6 Nov-Dec 2009","30"
    "Making a Light Mount for the Mini-mill","Sandro Di Filippo","Shop Accessories","HSM Vol. 28 No. 6 Nov-Dec 2009","42"
    "17 Reasons to Love the Oxy-acetylene Torch (or How to Use Pyrotechnics to your Best Advantage) - Conclusion","Kent White","Welding/Foundry/Forging","HSM Vol. 28 No. 6 Nov-Dec 2009","48"
    "Building a Large, Beam-type Steam Engine - Part Two","Brian Rupnow","Engines","HSM Vol. 28 No. 6 Nov-Dec 2009","61"
    "Randolph's Shop Class: Machining and Measuring Tapers","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 28 No. 6 Nov-Dec 2009","68"
    "Upgrading the Atlas 10/12 Taper Attachment - Part One","John Ehler","Lathes","HSM Vol. 29 No. 1 Jan-Feb 2010","12"
    "A Cross-slide for a Rotary Table","Matthew J. Russel","Shop Machinery","HSM Vol. 29 No. 1 Jan-Feb 2010","30"
    "GEARS","Fred Prestridge","Hobby Community","HSM Vol. 29 No. 1 Jan-Feb 2010","36"
    "A Homemade Miller Vise","Thomas Morrison","Shop Accessories","HSM Vol. 29 No. 1 Jan-Feb 2010","42"
    "Anti-gravity Machine - Part One","Charles St. Louis","Projects","HSM Vol. 29 No. 1 Jan-Feb 2010","50"
    "Building a Modified Gingery Metal Shaper","R.G. Sparber","Shop Machinery","HSM Vol. 29 No. 1 Jan-Feb 2010","56"
    "Wood Lathe Follow Rest","Ronald G. Casteel","Lathes","HSM Vol. 29 No. 1 Jan-Feb 2010","64"
    "Randolph's Shop Class: Tool Posts","J. Randolph Bulgin","Lathes","HSM Vol. 29 No. 1 Jan-Feb 2010","70"
    "The Cut Knurling Tool - Part One","Michael Ward","Shop Machinery","HSM Vol. 29 No. 2 Mar-Apr 2010","12"
    "Anti-gravity Machine - Part Two","Charles St. Louis","Projects","HSM Vol. 29 No. 2 Mar-Apr 2010","28"
    "Tool and Cutter Grinder Modification","Guy Hanson","Shop Machinery","HSM Vol. 29 No. 2 Mar-Apr 2010","34"
    "A Method for Re-registering Threaded Work in the Lathe","Jerry Pontius","Lathes","HSM Vol. 29 No. 2 Mar-Apr 2010","36"
    "A User-friendly Bridgeport Mill M-head Spindle Lock","Harvey Kratz","Mills","HSM Vol. 29 No. 2 Mar-Apr 2010","38"
    "A New X-feed Nut System","Jerrold Tiers","Lathes","HSM Vol. 29 No. 2 Mar-Apr 2010","42"
    "Upgrading the Atlas 10/12 Taper Attachment - Part Two","John Ehler","Lathes","HSM Vol. 29 No. 2 Mar-Apr 2010","44"
    "Randolph's Shop Class - Spiders and Steady Rests and Such","J. Randolph Bulgin","Lathes","HSM Vol. 29 No. 2 Mar-Apr 2010","58"
    "How to Make Bearings for your Bike","Bob Rodgerson","Projects","HSM Vol. 29 No. 2 Mar-Apr 2010","64"
    "A Miniature Ball Turner","Jerry Kimble","Lathes","HSM Vol. 29 No. 3 May-Jun 2010","12"
    "How to Make a Cylinder for a Motorcycle","Bob Rodgerson","Engines","HSM Vol. 29 No. 3 May-Jun 2010","20"
    "A Radical Toolholder for High-speed Steel Tool Bits","David Wimberley","Lathes","HSM Vol. 29 No. 3 May-Jun 2010","30"
    "Positioning the Cross-slide on a Rotary Table","R.G. Sparber","Shop Machinery","HSM Vol. 29 No. 3 May-Jun 2010","36"
    "Michel Lefaivre - 2010 Metalworking Craftsman of the Year","Craig Libuse","Hobby Community","HSM Vol. 29 No. 3 May-Jun 2010","38"
    "Upgrading the Atlas 10/12 Taper Attachment, Part Three","John Ehler","Lathes","HSM Vol. 29 No. 3 May-Jun 2010","42"
    "The Cut Knurling Tool, Part Two","Michael Ward","Shop Machinery","HSM Vol. 29 No. 3 May-Jun 2010","54"
    "Randolph's Shop Class: Mandrels and Their Kin","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 29 No. 3 May-Jun 2010","64"
    "A Visit to the American Precision Museum","Peter Merriam","General Machining Knowledge","HSM Vol. 29 No. 3 May-Jun 2010","70"
    "Development of a Lathe Tool Post Grinder, Part One","Jim Gavin","Lathes","HSM Vol. 29 No. 4 Jul-Aug 2010","10"
    "Shop Made Bevel Gears","Edward Hume","Projects","HSM Vol. 29 No. 4 Jul-Aug 2010","20"
    "Beyond the Basics with a Variable Frequency Drive","Dennis Hardin","Lathes","HSM Vol. 29 No. 4 Jul-Aug 2010","28"
    "Phoenix Battery Drills","Martin Gearing","Miscellaneous","HSM Vol. 29 No. 4 Jul-Aug 2010","34"
    "The Cut Knurling Tool - Part Three","Michael Ward","Shop Machinery","HSM Vol. 29 No. 4 Jul-Aug 2010","40"
    "Milling Index Center - Cheap and Easy","Ken Sevene","Mills","HSM Vol. 29 No. 4 Jul-Aug 2010","57"
    "Randolph's Shop Class - Heat Treating","J. Randolph Bulgin","Welding/Foundry/Forging","HSM Vol. 29 No. 4 Jul-Aug 2010","58"
    "Power through Flat Belts","Joel Sanderson","Projects","HSM Vol. 29 No. 5 Sep-Oct 2010","12"
    "A Star Shines Again - Restoring an Old Lathe","Gary Paine","Lathes","HSM Vol. 29 No. 5 Sep-Oct 2010","30"
    "Low-tech Plastic Injection","Lloyd Bender","Miscellaneous","HSM Vol. 29 No. 5 Sep-Oct 2010","36"
    "Development of a Lathe Tool Post Grinder - Part Two","Jim Gavin","Lathes","HSM Vol. 29 No. 5 Sep-Oct 2010","42"
    "The Cut Knurling Tool - Part Four","Michael Ward","Shop Machinery","HSM Vol. 29 No. 5 Sep-Oct 2010","48"
    "Randolph's Shop Class: Coolants - Yes and No","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 29 No. 5 Sep-Oct 2010","62"
    ""Tanks" a Lot: Methods for Metal Fuel Tank Development and Fabrication","Kent White","Projects","HSM Vol. 29 No. 6 Nov-Dec 2010","12"
    "Stop Your Bridgeport","Charles St. Louis","Mills","HSM Vol. 29 No. 6 Nov-Dec 2010","26"
    "Development of a Lathe Tool Post Grinder - Part Three","Jim Gavin","Lathes","HSM Vol. 29 No. 6 Nov-Dec 2010","32"
    "Secure that Tailstock Spindle Chuck","Paul J. Holm","Lathes","HSM Vol. 29 No. 6 Nov-Dec 2010","44"
    "Bridgeport Vise Storage System","James W. Hauser","Shop Accessories","HSM Vol. 29 No. 6 Nov-Dec 2010","48"
    "Modifications to Philip Duclos' Engines","James Service","Engines","HSM Vol. 29 No. 6 Nov-Dec 2010","52"
    "The Cut Knurling Tool - Part Five","Michael Ward","Shop Machinery","HSM Vol. 29 No. 6 Nov-Dec 2010","56"
    "Randolph's Shop Class: Heat Treating II - The Sequel","J. Randolph Bulgin","Welding/Foundry/Forging","HSM Vol. 29 No. 6 Nov-Dec 2010","68"
    "Basic Fixtures and Techniques for Making Rings","Mark Smith","Projects","HSM Vol. 30 No. 1 Jan-Feb 2011","10"
    "Brian's Radial Engine - Part One","Brian Rupnow","Engines","HSM Vol. 30 No. 1 Jan-Feb 2011","20"
    "Sensitive Drill Press","Glenn A. Pettit","Shop Machinery","HSM Vol. 30 No. 1 Jan-Feb 2011","30"
    "Lathe Keyway Cutting Jig","Thomas M. Verity","Lathes","HSM Vol. 30 No. 1 Jan-Feb 2011","38"
    "NEMES Model Engineering Show","Max Ben-aaron","Hobby Community","HSM Vol. 30 No. 1 Jan-Feb 2011","44"
    "Snow Engine Distributor Update","Ray Sholl","Engines","HSM Vol. 30 No. 1 Jan-Feb 2011","50"
    "A Lowered Bridgeport Switch","David L Meyers","Mills","HSM Vol. 30 No. 1 Jan-Feb 2011","54"
    "Development of a Lathe Tool Post Grinder - Part Four","Jim Gavin","Lathes","HSM Vol. 30 No. 1 Jan-Feb 2011","58"
    "Randolph's Shop Class: Shop Safety","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 30 No. 1 Jan-Feb 2011","64"
    "Wood Lathe Chisel Sharpener","Peter Merriam","Shop Machinery","HSM Vol. 30 No. 1 Jan-Feb 2011","70"
    "Change Gear Dividing on the Mark II Atlas 6" Lathe","Reid Kowallis","Lathes","HSM Vol. 30 No. 2 Mar-Apr 2011","12"
    "A Low Cost Digital Readout for a Lathe","R.G. Sparber","Lathes","HSM Vol. 30 No. 2 Mar-Apr 2011","30"
    "A Simple Follower Rest for the Lathe","Paul B Russ","Lathes","HSM Vol. 30 No. 2 Mar-Apr 2011","42"
    "Reproducing an 18th Century Rolling Double Cone","James Donnelly","Projects","HSM Vol. 30 No. 2 Mar-Apr 2011","46"
    "Brian's Radial Engine, Part Two","Brian Rupnow","Engines","HSM Vol. 30 No. 2 Mar-Apr 2011","48"
    "Development of a Lathe Tool Post Grinder, Part Five","Jim Gavin","Lathes","HSM Vol. 30 No. 2 Mar-Apr 2011","54"
    "A Tale of Two Vises","Myles Milner","Shop Accessories","HSM Vol. 30 No. 2 Mar-Apr 2011","64"
    "Randolph's Shop Class: Indexing Basics","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 30 No. 2 Mar-Apr 2011","66"
    "Scraping in the Home Shop, Part One","Michael Ward","General Machining Knowledge","HSM Vol. 30 No. 3 May-Jun 2011","12"
    "My Myford ML2 - It's Rebuild and Conversion to a Turret Lathe","Alan Suttie","Lathes","HSM Vol. 30 No. 3 May-Jun 2011","35"
    "How to Make Valve Guides","Bob Rodgerson","Projects","HSM Vol. 30 No. 3 May-Jun 2011","42"
    "Tweaking a Using an Imported Spin Index","J.A. Long","Shop Accessories","HSM Vol. 30 No. 3 May-Jun 2011","48"
    "Making a Semi-quick-change Tool Post Holder","William Vander-Reyden","Lathes","HSM Vol. 30 No. 3 May-Jun 2011","54"
    "Stuck up Bridgeport Quill Locking Lever","Charles St. Louis","Mills","HSM Vol. 30 No. 3 May-Jun 2011","58"
    "Louis Chenot "Metalworking Craftsman of the Decade"","Craig Libuse","Hobby Community","HSM Vol. 30 No. 3 May-Jun 2011","62"
    "Machine Shop in a Closet","Arthur Lowenthal","Miscellaneous","HSM Vol. 30 No. 3 May-Jun 2011","64"
    "Boring and Facing Heads","J. Randolph Bulgin","Shop Accessories","HSM Vol. 30 No. 3 May-Jun 2011","66"
    "A T-slotted Faceplate for the Mini-lathe","Sandro Di Filippo","Lathes","HSM Vol. 30 No. 4 Jul-Aug 2011","10"
    "Making Use of Turret Tooling","William Abernathy","Lathes","HSM Vol. 30 No. 4 Jul-Aug 2011","22"
    "Floating Tailstock Die Holder","Jeff Lott","Lathes","HSM Vol. 30 No. 4 Jul-Aug 2011","28"
    "Milling Machine Vacuum Arm","Mike Pileski","Mills","HSM Vol. 30 No. 4 Jul-Aug 2011","34"
    "Atlas Lathe Tailstock Lock","Michael Neafus","Lathes","HSM Vol. 30 No. 4 Jul-Aug 2011","38"
    "Digital Camera to Microscope Adapter","Peter Merriam","Projects","HSM Vol. 30 No. 4 Jul-Aug 2011","42"
    "Guitar Fret Mill","Roger Taylor","Projects","HSM Vol. 30 No. 4 Jul-Aug 2011","46"
    "Scraping for the Home Shop, Part Two","Michael Ward","General Machining Knowledge","HSM Vol. 30 No. 4 Jul-Aug 2011","50"
    "Randolph's Shop Class: Welding in the Home Shop","J. Randolph Bulgin","Welding/Foundry/Forging","HSM Vol. 30 No. 4 Jul-Aug 2011","66"
    "Anti-rotational Shim for the Rotary Table","Tom McAllister","Mills","HSM Vol. 30 No. 4 Jul-Aug 2011","70"
    "The EZ - Air Engine","Christopher Vasconcelos","Engines","HSM Vol. 30 No. 5 Sep-Oct 2011","8"
    "Myford Series Seven Handwheel Dial","Graham Meek","Lathes","HSM Vol. 30 No. 5 Sep-Oct 2011","26"
    "A Million Dollars Worth of Machinery for the Price of Tuition","R. Lane Maxwell","Hobby Community","HSM Vol. 30 No. 5 Sep-Oct 2011","36"
    "Improvements to a Metal-cutting Band Saw","Robert Yost","Shop Machinery","HSM Vol. 30 No. 5 Sep-Oct 2011","42"
    "Workholding with a Wedge","Richard Sevigny","Shop Accessories","HSM Vol. 30 No. 5 Sep-Oct 2011","44"
    "Scraping for the Home Shop, Part Three","Michael Ward","General Machining Knowledge","HSM Vol. 30 No. 5 Sep-Oct 2011","46"
    "A Round Die Wrench Replacement","Paul J. Holm","Shop Accessories","HSM Vol. 30 No. 5 Sep-Oct 2011","60"
    "Randolph's Shop Class - Knurling","J. Randolph Bulgin","Shop Accessories","HSM Vol. 30 No. 5 Sep-Oct 2011","64"
    "Lever Paradox","James Donnelly","Projects","HSM Vol. 30 No. 6 Nov-Dec 2011","10"
    "An Automatic Feed for an Imported Boring Head","Ted Hansen","Lathes","HSM Vol. 30 No. 6 Nov-Dec 2011","36"
    "An Oiler for Ball-type Oil Ports","Art Plunkett","Projects","HSM Vol. 30 No. 6 Nov-Dec 2011","42"
    "Scraping for the Home Shop - Part Four","Michael Ward","General Machining Knowledge","HSM Vol. 30 No. 6 Nov-Dec 2011","46"
    "Beginners' Tips from the Toolmaker: Who I am and Why I Like to Think I Know What I'm Talking About","Sandro Di Filippo","Hobby Community","HSM Vol. 30 No. 6 Nov-Dec 2011","60"
    "Randolph's Shop Class - Chucks and Chucking - Part One","J. Randolph Bulgin","Lathes","HSM Vol. 30 No. 6 Nov-Dec 2011","62"
    "Repairing a Pulley Hub","Carl Byrns","Miscellaneous","HSM Vol. 30 No. 6 Nov-Dec 2011","66"
    "A User-friendly Follower Rest","Harry Bloom","Lathes","HSM Vol. 30 No. 6 Nov-Dec 2011","224"
    "Four-Facet Drill Sharpener with Optional Point Splitter","John Moran","Shop Machinery","HSM Vol. 31 No. 1 Jan-Feb 2012","10"
    "Weekend Project: A Woodworker's Marking Gauge","Andrew Wakefield","Shop Accessories","HSM Vol. 31 No. 1 Jan-Feb 2012","24"
    "An Upgrade You Must Make","Steve Kinsey","Lathes","HSM Vol. 31 No. 1 Jan-Feb 2012","38"
    "A Clamp-type Knurling Tool","John Viggers","Shop Machinery","HSM Vol. 31 No. 1 Jan-Feb 2012","42"
    "Tweaking and Using an Imported Right Angle Head","J.A. Long","Mills","HSM Vol. 31 No. 1 Jan-Feb 2012","47"
    "Scraping for the Home Shop - Part Five","Michael Ward","General Machining Knowledge","HSM Vol. 31 No. 1 Jan-Feb 2012","50"
    "Randolph's Shop Class - Chucks and Chucking: Part Two","J. Randolph Bulgin","Lathes","HSM Vol. 31 No. 1 Jan-Feb 2012","64"
    "Thread Designations and What They Mean","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 31 No. 1 Jan-Feb 2012","70"
    "A Slotting Attachment for the Mill","Graham Meek","Mills","HSM Vol. 31 No. 2 Mar-Apr 2012","12"
    "A "Sound" Repair","Walter Yetman","Projects","HSM Vol. 31 No. 2 Mar-Apr 2012","21"
    "Some Drill Press Mods","Peter Merriam","Shop Machinery","HSM Vol. 31 No. 2 Mar-Apr 2012","24"
    "Four-Facet Drill Sharpener with Optional Point Splitter - Part Two","John Moran","Shop Machinery","HSM Vol. 31 No. 2 Mar-Apr 2012","28"
    "I Cut Threads!","Paul E Wofford","Projects","HSM Vol. 31 No. 2 Mar-Apr 2012","42"
    "Tale of a Torii","Otto Bacon","Projects","HSM Vol. 31 No. 2 Mar-Apr 2012","45"
    "Scraping for the Home Shop - Part Six","Michael Ward","General Machining Knowledge","HSM Vol. 31 No. 2 Mar-Apr 2012","48"
    "Randolph's Shop Class: Poor Man's DRO","J. Randolph Bulgin","Shop Accessories","HSM Vol. 31 No. 2 Mar-Apr 2012","65"
    "Tool Steels Explained","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 31 No. 2 Mar-Apr 2012","69"
    "A Multispeed Attachment for a South Bend Drill Press","James A. Benjamin","Shop Machinery","HSM Vol. 31 No. 3 May-Jun 2012","8"
    "Bridgeport Mill Switch Relocation","Weston R. Loomer","Shop Machinery","HSM Vol. 31 No. 3 May-Jun 2012","22"
    "Modifying a Smithy Chuck","William Vander-Reyden","Lathes","HSM Vol. 31 No. 3 May-Jun 2012","28"
    "A Small Bender","Roger Taylor","Shop Accessories","HSM Vol. 31 No. 3 May-Jun 2012","38"
    "Scraping for the Home Shop - Part Seven","Michael Ward","General Machining Knowledge","HSM Vol. 31 No. 3 May-Jun 2012","40"
    "A Die Holder for the Tool Post","Ivan Yelusich","Lathes","HSM Vol. 31 No. 3 May-Jun 2012","56"
    "Beginners' Tips from the Toolmaker: Cutting Speed and Feed Rates","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 31 No. 3 May-Jun 2012","57"
    "Gary Conley - 2012 Metalworking Craftsman of the Year","Craig Libuse","Hobby Community","HSM Vol. 31 No. 3 May-Jun 2012","60"
    "Randolph's Shop Class: Mistakes","J. Randolph Bulgin","Projects","HSM Vol. 31 No. 3 May-Jun 2012","62"
    "A New Top Slide for the Atlas 6"" Lathe","James A. Hornicek","Lathes","HSM Vol. 31 No. 4 Jul-Aug 2012","8"
    "One Way to Make a Steam Ejector","Chet Roberts","Projects","HSM Vol. 31 No. 4 Jul-Aug 2012","20"
    "Mr. Murphy and I Order a Lathe","R. Lynnard Tessner","Lathes","HSM Vol. 31 No. 4 Jul-Aug 2012","26"
    "Running the "Boiler" Dry","Paul Anderson","Projects","HSM Vol. 31 No. 4 Jul-Aug 2012","31"
    "Beginners' Tips from the Toolmaker: Steel - How To Figure Out What It Is","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 31 No. 4 Jul-Aug 2012","34"
    "Sherline Lathe Power Feed","Ronald G. Casteel","Lathes","HSM Vol. 31 No. 4 Jul-Aug 2012","38"
    "Scraping for the Home Shop - Part Eight","Michael Ward","General Machining Knowledge","HSM Vol. 31 No. 4 Jul-Aug 2012","46"
    "Randolph's Shop Class: From the Corner of the Tool Box","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 31 No. 4 Jul-Aug 2012","60"
    "Deburr That Hole","Scott B. Lacey","Miscellaneous","HSM Vol. 31 No. 4 Jul-Aug 2012","65"
    "In the Workshop with Humbernut: Constructing an Antique Crankcase - Part One","Bob Rodgerson","Projects","HSM Vol. 31 No. 5 Sep-Oct 2012","10"
    "A Quick Adjust Quill Depth Stop","Gary Paine","Shop Machinery","HSM Vol. 31 No. 5 Sep-Oct 2012","22"
    "Additions and Modifications to a Mini-lathe","Ted Hansen","Shop Machinery","HSM Vol. 31 No. 5 Sep-Oct 2012","29"
    "Scraping for the Home Shop - Part Nine","Michael Ward","General Machining Knowledge","HSM Vol. 31 No. 5 Sep-Oct 2012","34"
    "Drag Link Repair","Carl Byrns","Miscellaneous","HSM Vol. 31 No. 5 Sep-Oct 2012","50"
    "Winging It: A Dual Purpose Handle","Charles St. Louis","Miscellaneous","HSM Vol. 31 No. 5 Sep-Oct 2012","53"
    "Beginners' Tips from the Toolmaker:- Basic Layout Skills","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 31 No. 5 Sep-Oct 2012","58"
    "Randolph's Shop Class - Threading","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 31 No. 5 Sep-Oct 2012","62"
    "My Version of a Drill Finder Chart","Joe Blumber","General Machining Knowledge","HSM Vol. 31 No. 5 Sep-Oct 2012","70"
    "The Bruce MacBeth Egine - Part One","Douglas Kelley","Engines","HSM Vol. 31 No. 6 Nov-Dec 2012","10"
    "Build a Gingery Dividing Head without Castings","Jerry L. Sokol","Shop Accessories","HSM Vol. 31 No. 6 Nov-Dec 2012","18"
    "In the Workshop with Humbernut: Constructing an Antique Crankcase - Part Two","Bob Rodgerson","Miscellaneous","HSM Vol. 31 No. 6 Nov-Dec 2012","24"
    "Threading Stop for a 9"" South Bend Lathe","Jim Connell","Lathes","HSM Vol. 31 No. 6 Nov-Dec 2012","24"
    "Additions and Modifications to a Mini-lathe: Making a Faceplate or Chuck Adapter","Ted Hansen","Lathes","HSM Vol. 31 No. 6 Nov-Dec 2012","42"
    "Beginners' Tips from the Toolmaker: Common Problems with Drilled Holes","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 31 No. 6 Nov-Dec 2012","45"
    "Scraping for the Home Shop - Part Ten","Michael Ward","General Machining Knowledge","HSM Vol. 31 No. 6 Nov-Dec 2012","48"
    "Randolph's Shop Class: Threading - Part Two","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 31 No. 6 Nov-Dec 2012","58"
    "A Poor Man's Multispeed Drill Press Attachment","Gary Vriezen","Shop Machinery","HSM Vol. 31 No. 6 Nov-Dec 2012","66"
    "Broken Tap Tip","Bob Mansfield","Miscellaneous","HSM Vol. 31 No. 6 Nov-Dec 2012","70"
    "Building a Tailstock Live Center with a 1-1/2-8 Spindle","Dave Garrett","Lathes","HSM Vol. 32 No. 1 Jan-Feb 2013","10"
    "The Bruce Macbeth Engine - Part Two","Douglas Kelley","Engines","HSM Vol. 32 No. 1 Jan-Feb 2013","10"
    "Making a Thick Walled Boring Bar Insert","R.G. Sparber","Projects","HSM Vol. 32 No. 1 Jan-Feb 2013","45"
    "Additions and Modifications to a Mini-lathe: Apron Upgrades","Ted Hansen","Lathes","HSM Vol. 32 No. 1 Jan-Feb 2013","49"
    "A Chisel Grinding Fixture","Jeff A. Finley","Shop Accessories","HSM Vol. 32 No. 1 Jan-Feb 2013","53"
    "In the Workshop with Humbernut: Constructing an Antique Crankcase - Part Three","Bob Rodgerson","Miscellaneous","HSM Vol. 32 No. 1 Jan-Feb 2013","56"
    "Randolph's Shop Class: Lifting Devices for the Small Shop","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 32 No. 1 Jan-Feb 2013","64"
    "Beginners' Tips From the Toolmaker: How to Achieve a More Accurate Layout","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 32 No. 1 Jan-Feb 2013","69"
    "Synergy","Charles Fox","Hobby Community","HSM Vol. 32 No. 1 Jan-Feb 2013","71"
    "Building a Modified Brooks Cutter Grinder - Part One","James Schroeder","Shop Machinery","HSM Vol. 32 No. 2 Mar-Apr 2013","10"
    "Rescue Poxy: How an Epoxy Disaster Drove the Search to Find a Good, Castable Epoxy","L.H. Cantwell","Miscellaneous","HSM Vol. 32 No. 2 Mar-Apr 2013","28"
    "A Portable Machine Oiler","Alan Anganes","Shop Accessories","HSM Vol. 32 No. 2 Mar-Apr 2013","44"
    "The Bruce Macbeth Engine - Part Three","Douglas Kelley","Engines","HSM Vol. 32 No. 2 Mar-Apr 2013","44"
    "Metric and Imperial Together - Without Pain","Martin Gearing","General Machining Knowledge","HSM Vol. 32 No. 2 Mar-Apr 2013","50"
    "Additions and Modifications to a Mini-Lathe: Bed Wipers & Carriage Ways","Ted Hansen","Lathes","HSM Vol. 32 No. 2 Mar-Apr 2013","52"
    "Bolt in a Bottle Puzzle","Otto Bacon","Miscellaneous","HSM Vol. 32 No. 2 Mar-Apr 2013","56"
    "Randolph's Shop Class: Collets","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 32 No. 2 Mar-Apr 2013","58"
    "Atlas Lathe Tool Holder","Michael Neafus","Lathes","HSM Vol. 32 No. 2 Mar-Apr 2013","63"
    "Beginners' Tips from the Toolmaker: Tapping a Hole by Hand","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 32 No. 2 Mar-Apr 2013","64"
    "Book Review: Turning Precision Tapers on Your Mini Lathe","George Bulliss","Hobby Community","HSM Vol. 32 No. 2 Mar-Apr 2013","72"
    "Modeling a 1950s Briggs & Stratton Model 6S in Half Scale - A Project Overview","Bill Lindsey","Engines","HSM Vol. 32 No. 3 May-Jun 2013","10"
    "The Bruce MacBeth Engine - Part Four","Douglas Kelley","Engines","HSM Vol. 32 No. 3 May-Jun 2013","20"
    "Additions and Modifications to a Mini-Lathe: Increasing Torque with a Small Motor Pulley","Ted Hansen","Lathes","HSM Vol. 32 No. 3 May-Jun 2013","28"
    "Emco Maier Dividing Attachment Modification","Gary Repesh","Shop Accessories","HSM Vol. 32 No. 3 May-Jun 2013","34"
    "Guillermo Rojas-Bazan - 2013 Metalworking Craftsman of the Year","","Hobby Community","HSM Vol. 32 No. 3 May-Jun 2013","38"
    "Buillding a Modified Brooks Cutter Grinder - Part Two","James Schroeder","Shop Machinery","HSM Vol. 32 No. 3 May-Jun 2013","42"
    "Storing End Mills","Art Plunkett","Miscellaneous","HSM Vol. 32 No. 3 May-Jun 2013","56"
    "Randolph's Shop Class: The Milling Machine: Home Shop Version - Part One","J. Randolph Bulgin","Mills","HSM Vol. 32 No. 3 May-Jun 2013","60"
    "Beginners' Tips from the Toolmaker: Using a Micrometer","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 32 No. 3 May-Jun 2013","70"
    "The Lathe: An Early Historical Overview","George W. Genevro","Miscellaneous","HSM Vol. 32 No. 4 Jul-Aug 2013","10"
    "Solving a Work Holding Problem","James Kilroy","Miscellaneous","HSM Vol. 32 No. 4 Jul-Aug 2013","24"
    "A Very Simple Ball Turning Attachment for a Lathe","Bob Neidorff","Lathes","HSM Vol. 32 No. 4 Jul-Aug 2013","28"
    "Additions and Modifications to the Mini-Lathe: Upgrading the Tailstock","Ted Hansen","Lathes","HSM Vol. 32 No. 4 Jul-Aug 2013","34"
    "Building a Modified Brooks Cutter Grinder - Part Three","James Schroeder","Shop Machinery","HSM Vol. 32 No. 4 Jul-Aug 2013","42"
    "2012 Lifetime Achievement Award","","Hobby Community","HSM Vol. 32 No. 4 Jul-Aug 2013","55"
    "Repairing and Improving My Old Mill Vise","George J. Baisz","Shop Accessories","HSM Vol. 32 No. 4 Jul-Aug 2013","58"
    "Randolph's Shop Class: The Milling Machine, Home Shop Version - Part One","J. Randolph Bulgin","Mills","HSM Vol. 32 No. 4 Jul-Aug 2013","60"
    "Using an EDM to Repair an Odometer","Dennis Debano","EDM","HSM Vol. 32 No. 4 Jul-Aug 2013","66"
    "A Machinist's Microscope","Alan Anganes","Shop Accessories","HSM Vol. 32 No. 4 Jul-Aug 2013","72"
    "The OPOC 246 Engine - Part One","James Donnelly","Engines","HSM Vol. 32 No. 5 Sep-Oct 2013","12"
    "Cutting Accurate External, Single-point Threads in a Lathe","Wes Brenner","Lathes","HSM Vol. 32 No. 5 Sep-Oct 2013","25"
    "Re-Machining a Low Cost XY Compound Vise","R.G. Sparber","Shop Accessories","HSM Vol. 32 No. 5 Sep-Oct 2013","31"
    "Additions and Modifications to a Mini-Lathe: Alignment Essentials","Ted Hansen","Lathes","HSM Vol. 32 No. 5 Sep-Oct 2013","46"
    "Building a Modified Brooks Cutter Grinder - Part Four","James Schroeder","Shop Machinery","HSM Vol. 32 No. 5 Sep-Oct 2013","50"
    "Not Another Rotary Table","Joe Black","Shop Accessories","HSM Vol. 32 No. 5 Sep-Oct 2013","55"
    "Randolph's Shop Class: Fly Cutters","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 32 No. 5 Sep-Oct 2013","57"
    "Clock Bushing Repair Using a Sherline Mill","Ronald G. Casteel","Mills","HSM Vol. 32 No. 5 Sep-Oct 2013","61"
    "Beginners' Tips from the Toolmaker: Hot-rolled vs. Cold-rolled Steel","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 32 No. 5 Sep-Oct 2013","66"
    "A Carriage Indicator Stop for the Atlas Lathe","James A. Hornicek","Lathes","HSM Vol. 32 No. 5 Sep-Oct 2013","68"
    "Hex Head Drivers","Michael Ward","Shop Accessories","HSM Vol. 32 No. 6 Nov-Dec 2013","12"
    "Quick and Easy Boring Table for the Lathe","Charles E. Joscelyn","Lathes","HSM Vol. 32 No. 6 Nov-Dec 2013","30"
    "Re-machining End Mill Holders for Lathe Collet Use","William Vander-Reyden","Lathes","HSM Vol. 32 No. 6 Nov-Dec 2013","35"
    "Building a Time Capsule","Kevin Smolkowski","Projects","HSM Vol. 32 No. 6 Nov-Dec 2013","38"
    "Additions and Modifications to the Mini-Lathe: A Carriage Travel Stop and Spindle Index","Ted Hansen","Lathes","HSM Vol. 32 No. 6 Nov-Dec 2013","42"
    "The OPOC 246 Engine - Part Two","James Donnelly","Engines","HSM Vol. 32 No. 6 Nov-Dec 2013","50"
    "Randolph's Shop Class: Work Holding - Part One","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 32 No. 6 Nov-Dec 2013","58"
    "Beginners\' Tips from the Toolmaker: Benchwork - Using a Hacksaw","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 32 No. 6 Nov-Dec 2013","64"
    "A Speed Key for Your Four-jaw Chuck","David Morrow","Miscellaneous","HSM Vol. 32 No. 6 Nov-Dec 2013","67"
    "Buillding a Coleman Boulevard Lamp - Part One","Jeffrey C. Maier","Projects","HSM Vol. 33 No. 1 Jan-Feb 2014","12"
    "Scratch Built: The Challenges and the Rewards","Bill Conway","Miscellaneous","HSM Vol. 33 No. 1 Jan-Feb 2014","21"
    "Cams Made Easy","Graham Meek","Engines","HSM Vol. 33 No. 1 Jan-Feb 2014","24"
    "Tailstock Parking Device and Bed Extension","Steve Roberts","Lathes","HSM Vol. 33 No. 1 Jan-Feb 2014","32"
    "Additions and Modifications to a Mini-Lathe: Using the Compound Rest as a Milling Slide","Ted Hansen","Lathes","HSM Vol. 33 No. 1 Jan-Feb 2014","37"
    "A Tool Post Dial Indicator Holder","Doug Ripka","Shop Accessories","HSM Vol. 33 No. 1 Jan-Feb 2014","44"
    "A Reversing Switch for a Mini-mill","Carl Byrns","Mills","HSM Vol. 33 No. 1 Jan-Feb 2014","50"
    "A Home Built Shop","John Buffum","Miscellaneous","HSM Vol. 33 No. 1 Jan-Feb 2014","56"
    "Randolph's Shop Class: Work Holding - Part Two","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 33 No. 1 Jan-Feb 2014","62"
    "Beginners\' Tips from the Toolmaker: Bench Work - Using Files","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 33 No. 1 Jan-Feb 2014","68"
    "Low Cost DROs for a Vertical Mill - Part One","Jim Gavin","Mills","HSM Vol. 33 No. 2 Mar-Apr 2014","12"
    "Designing Fabrications with Wood: The Poor Man's "SolidWorks"","Charles E. Joscelyn","General Machining Knowledge","HSM Vol. 33 No. 2 Mar-Apr 2014","26"
    "Stopping the Screwless Vise","Tom McAllister","Shop Accessories","HSM Vol. 33 No. 2 Mar-Apr 2014","30"
    "Additions and Modifications to a Mini-Lathe: Milling Setups","Ted Hansen","Lathes","HSM Vol. 33 No. 2 Mar-Apr 2014","34"
    "Building a Coleman Boulevard Lamp - Part Two","Jeffrey C. Maier","Projects","HSM Vol. 33 No. 2 Mar-Apr 2014","42"
    "Some Recent Acquisitions by the Joe Martin Foundation Craftmanship Museum","Craig Libuse","Hobby Community","HSM Vol. 33 No. 2 Mar-Apr 2014","54"
    "Randolph's Shop Class: When is a Lathe not a Lathe?","J. Randolph Bulgin","Lathes","HSM Vol. 33 No. 2 Mar-Apr 2014","56"
    "Beginners' Tips from the Toolmaker: Bench Work - Making a Drill Gage","Sandro Di Filippo","Shop Accessories","HSM Vol. 33 No. 2 Mar-Apr 2014","62"
    "Making a Steam Turbine","Walter Erspamer","Projects","HSM Vol. 33 No. 3 May-Jun 2014","12"
    "A Fix for the Mini-Lathe","Marco Crivellari","Lathes","HSM Vol. 33 No. 3 May-Jun 2014","22"
    "Setting Up a Bench Grinder for Shaping Lathe Tools","Donald Brouse","Shop Accessories","HSM Vol. 33 No. 3 May-Jun 2014","30"
    "Improving the Breed - Rebuilding a Homemade Rotary Table","Myles Milner","Shop Accessories","HSM Vol. 33 No. 3 May-Jun 2014","34"
    "Tailstock Drill Press","Richard Rex","Lathes","HSM Vol. 33 No. 3 May-Jun 2014","42"
    "Additions and Modifications to a Mini-Lathe: Compound Rest Improvements","Ted Hansen","Lathes","HSM Vol. 33 No. 3 May-Jun 2014","46"
    "Low Cost DROs for a Vertical Mill - Part Two","Jim Gavin","Mills","HSM Vol. 33 No. 3 May-Jun 2014","50"
    "Steve Lindsay - 2014 Metalworking Craftsman of the Year","Craig Libuse","Hobby Community","HSM Vol. 33 No. 3 May-Jun 2014","58"
    "Beginners' Tips from the Toolmaker: Sharpening a Drill by Hand","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 33 No. 3 May-Jun 2014","60"
    "Randolph's Shop Class: The Dial Indicator","J. Randolph Bulgin","Shop Accessories","HSM Vol. 33 No. 3 May-Jun 2014","64"
    "Book Review: The Engine Lathe","George Bulliss","Hobby Community","HSM Vol. 33 No. 3 May-Jun 2014","69"
    "Building Henry Ford's First Stationary Internal Combustion Engine - Part One","Christopher Vasconcelos","Engines","HSM Vol. 33 No. 4 Jul-Aug 2014","10"
    "Tempering (as in Heat Treatment) the Easy Way - Results Guaranteed","Martin Gearing","General Machining Knowledge","HSM Vol. 33 No. 4 Jul-Aug 2014","26"
    "Improvements to Inexpensive Squares","Paul Alciatore","Shop Accessories","HSM Vol. 33 No. 4 Jul-Aug 2014","32"
    "Installing a Machine Single-handedly","James A. Hornicek","Miscellaneous","HSM Vol. 33 No. 4 Jul-Aug 2014","46"
    "Additions and Modifications to the Mini-Lathe: A Quick-change Tool Post","Ted Hansen","Lathes","HSM Vol. 33 No. 4 Jul-Aug 2014","50"
    "Construction of a Fence for a Delta Band Saw","Paul Smeltzer","Miscellaneous","HSM Vol. 33 No. 4 Jul-Aug 2014","56"
    "Joe Martin - Model Engineer, Entrepreneur, and Sportsman","","Hobby Community","HSM Vol. 33 No. 4 Jul-Aug 2014","60"
    "Randolph's Shop Class: Uh-Oh!","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 33 No. 4 Jul-Aug 2014","62"
    "Beginners' Tips from the Toolmaker: Using a Bench Grinder","Sandro Di Filippo","Shop Machinery","HSM Vol. 33 No. 4 Jul-Aug 2014","68"
    "The Myford Super 7 Screw Cutting Clutch - Screw Cutting Simplified: Part One","Graham Meek","Lathes","HSM Vol. 33 No. 5 Sep-Oct 2014","10"
    "External Single Point Threading for Lathes","Dave Ford","General Machining Knowledge","HSM Vol. 33 No. 5 Sep-Oct 2014","24"
    "Another Poor Man's DRO Solution","William Vander-Reyden","Shop Accessories","HSM Vol. 33 No. 5 Sep-Oct 2014","26"
    "Building Henry Ford's First Stationary Internal Combustion Engine - Part Two","Christopher Vasconcelos","Engines","HSM Vol. 33 No. 5 Sep-Oct 2014","28"
    "How to Make Push Rod Ends for Vintage Motorcycles","Bob Rodgerson","Miscellaneous","HSM Vol. 33 No. 5 Sep-Oct 2014","42"
    "Additions and Modifications to the Mini-Lathe: Aligning the Cross Slide","Ted Hansen","Lathes","HSM Vol. 33 No. 5 Sep-Oct 2014","52"
    "Randolph's Shop Class: Keyways","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 33 No. 5 Sep-Oct 2014","60"
    "Beginners' Tips frtom the Toolmaker: Using a Depth Micrometer","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 33 No. 5 Sep-Oct 2014","66"
    "An Easy Rockwell Mill Arbor Support","Roger Taylor","Mills","HSM Vol. 33 No. 5 Sep-Oct 2014","70"
    "Additions and Modifications to the Mini-Lathe: Cross Slide Improvements","Ted Hansen","Lathes","HSM Vol. 33 No. 6 Nov-Dec 2014","53"
    "Beginners' Tips from the Toolmaker: Using Inside Micrometers","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 33 No. 6 Nov-Dec 2014","66"
    "Book Review: Tabletop Milling","George Bulliss","Miscellaneous","HSM Vol. 33 No. 6 Nov-Dec 2014","70"
    "Making a Tap Guide","Walter Erspamer","Shop Accessories","HSM Vol. 33 No. 6 Nov-Dec 2014","50"
    "Miters and More - 4x6 Band Saw and Welding Fixtures","Charles Joscelyn","Shop Accessories","HSM Vol. 33 No. 6 Nov-Dec 2014","26"
    "Modifying the 'Lil Brother Hit 'n Miss Engine - Part One","Donald Brouse","Engines","HSM Vol. 33 No. 6 Nov-Dec 2014","10"
    "Randolph's Shop Class: Abrasive Machining","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 33 No. 6 Nov-Dec 2014","58"
    "Rudy Kouhoupt: My Teacher, My Mentor","Bill Conway","Hobby Community","HSM Vol. 33 No. 6 Nov-Dec 2014","23"
    "The Myford Super 7 Screw Cutting Clutch - Screw Cutting Simplified: Part Two","Graham Meek","Lathes","HSM Vol. 33 No. 6 Nov-Dec 2014","36"
    "A Digital Readout for the Myford Super Series Lathe","G. Wadham","Lathes","HSM Vol. 34 No. 1 Jan-Feb 2015","30"
    "A Professional Grade Tortilla Press","Bernt Normanson","Projects","HSM Vol. 34 No. 1 Jan-Feb 2015","70"
    "Additions and Modifications to the Mini-Lathe: Carriage Locks and More","Ted Hansen","Lathes","HSM Vol. 34 No. 1 Jan-Feb 2015","58"
    "Modifying the 'Lil Brother Hit 'n Miss Engine - Part Two","Donald Brouse","Engines","HSM Vol. 34 No. 1 Jan-Feb 2015","38"
    "Randolph's Shop Class - Holes","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 34 No. 1 Jan-Feb 2015","64"
    "Spade Drill Holder","Don Wiederhold","Shop Accessories","HSM Vol. 34 No. 1 Jan-Feb 2015","24"
    "Threading Clutch for the Grizzly G0602 - Part One","James Schroeder","Lathes","HSM Vol. 34 No. 1 Jan-Feb 2015","12"
    "Tighter and Brighter","Charles St. Louis","Mills","HSM Vol. 34 No. 1 Jan-Feb 2015","46"
    "Workholding for Thin Materials","Frank DiSanti","General Machining Knowledge","HSM Vol. 34 No. 1 Jan-Feb 2015","56"
    "A Quickset Depth Stop","James Harp","Shop Machinery","HSM Vol. 34 No. 2 Mar-Apr 2015","32"
    "A Tailstock Tap and Die Holding Tool with Feel","Paul Holm","Lathes","HSM Vol. 34 No. 2 Mar-Apr 2015","52"
    "Additions and Modifications to the Mini-Lathe: The Modular Dividing Head for the Mini","Ted Hansen","Lathes","HSM Vol. 34 No. 2 Mar-Apr 2015","58"
    "Alignment Help for the Mill-Drill","Dave Sage","Mills","HSM Vol. 34 No. 2 Mar-Apr 2015","12"
    "Cutting Corners","R.G. Sparber","Miscellaneous","HSM Vol. 34 No. 2 Mar-Apr 2015","62"
    "Improvements to a Smithy 5C Collet Chuck","Carl Blum","Lathes","HSM Vol. 34 No. 2 Mar-Apr 2015","25"
    "Quick-change Tool Post Mount","Wayne Hill","Lathes","HSM Vol. 34 No. 2 Mar-Apr 2015","30"
    "Randolph's Shop Class: Who Said this is Impossible!?","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 34 No. 2 Mar-Apr 2015","64"
    "Threading Clutch for the Grizzly G0602 - Part Two","James Schroeder","Lathes","HSM Vol. 34 No. 2 Mar-Apr 2015","42"
    "William R. Robertson - 2015 Metalworking Craftsman of the Year","Craig Libuse","Hobby Community","HSM Vol. 34 No. 3 May-Jun 2015","33"
    "Additions and Modifications to the Mini-Lathe: A Worm Drive for the Indexing Head","Ted Hansen","Lathes","HSM Vol. 34 No. 3 May-Jun 2015","46"
    "Beginners' Tips from the Toolmaker: Drills","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 34 No. 3 May-Jun 2015","62"
    "Boring Mill Seat Cutter","Michael Long","Shop Accessories","HSM Vol. 34 No. 3 May-Jun 2015","42"
    "Capturing the Tommy Bar","Martin Gearing","Shop Accessories","HSM Vol. 34 No. 3 May-Jun 2015","44"
    "Design and Construction of a Custom Golf Putter Head - Part One","Jim Gavin","Projects","HSM Vol. 34 No. 3 May-Jun 2015","10"
    "Grandpa's Toolbox","Jon Working","Miscellaneous","HSM Vol. 34 No. 3 May-Jun 2015","70"
    "Laser Tramming a Mill","Peter McKelvey","Mills","HSM Vol. 34 No. 3 May-Jun 2015","67"
    "Quick-Change Toolholders and a Filing rest","Richard Rex","Lathes","HSM Vol. 34 No. 3 May-Jun 2015","36"
    "Randolph's Shop Class: Gear Cutting","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 34 No. 3 May-Jun 2015","54"
    "Spunky - the Super Simple to Build and Understand Pony Hot Air Engine","Charles St. Louis","Engines","HSM Vol. 34 No. 3 May-Jun 2015","20"
    "A Device for Simplifying Thread Cutting","Jim McKee","Lathes","HSM Vol. 34 No. 4 Jul-Aug 2015","35"
    "Additions and Modifications to the Mini-Lathe: Using the Worm Attachment and Adding a Spindle Index","Ted Hansen","Lathes","HSM Vol. 34 No. 4 Jul-Aug 2015","54"
    "Beginners' Tips from the Toolmaker: Getting Started - What to Get First","Sandro Di Filippo","Shop Machinery","HSM Vol. 34 No. 4 Jul-Aug 2015","68"
    "Building the Shortstack Twin","Christopher Vasconcelos","Engines","HSM Vol. 34 No. 4 Jul-Aug 2015","8"
    "Design and Construction of a Custom Golf Putter Head - Part Two","Jim Gavin","Projects","HSM Vol. 34 No. 4 Jul-Aug 2015","42"
    "Lathe Chuck Safety Device","David Childers","Lathes","HSM Vol. 34 No. 4 Jul-Aug 2015","32"
    "Little Metal Monsters Made on Your Lathe","Thomas I. Stuart","Miscellaneous","HSM Vol. 34 No. 4 Jul-Aug 2015","26"
    "Randolph's Shop Class: Table Furniture","J. Randolph Bulgin","Shop Accessories","HSM Vol. 34 No. 4 Jul-Aug 2015","60"
    "Tailstock Chuck Arbor","Roger Taylor","Lathes","HSM Vol. 34 No. 4 Jul-Aug 2015","48"
    "Improvements on a Multipurpose Machine - Part One","James Hornicek","Shop Machinery","HSM Vol. 34 No. 5 Sep-Oct 2015","10"
    "A Wright Brothers Engine Projects","Ken Reed","Engines","HSM Vol. 34 No. 5 Sep-Oct 2015","24"
    "Design and Construction of a Custom Golf Putter Head - Part Three","Jim Gavin","Projects","HSM Vol. 34 No. 5 Sep-Oct 2015","32"
    "Four-Tool Turrets","Graham Meek","Lathes","HSM Vol. 34 No. 5 Sep-Oct 2015","42"
    "My EDM","Luis Ballin","EDM","HSM Vol. 34 No. 5 Sep-Oct 2015","54"
    "Additions and Modifications to the Mini-Lathe: Making Gear Cutters","Ted Hansen","Miscellaneous","HSM Vol. 34 No. 5 Sep-Oct 2015","56"
    "Randolph's Shop Class: Indexing In-Depth","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 34 No. 5 Sep-Oct 2015","60"
    "Beginners' Tips from the Toolmaker: Telescoping Gages","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 34 No. 5 Sep-Oct 2015","68"
    "Lathe Boring Bar Holder","Wilfred Nise","Lathes","HSM Vol. 34 No. 6 Nov-Dec 2015","8"
    "Miller, Offenhauser, Meyer-Drake: America's Unique Racing Engines and the Men Who Built Them","George Genevro","Engines","HSM Vol. 34 No. 6 Nov-Dec 2015","10"
    "Upgrading an Import Drill Press for some ""Real"" Work","John Felgenhauer","Shop Machinery","HSM Vol. 34 No. 6 Nov-Dec 2015","30"
    "Improvements on a Multipurpose Machine - Part Two","James Hornicek","Shop Machinery","HSM Vol. 34 No. 6 Nov-Dec 2015","32"
    "A Grinder with Guts","Andrew H. Wakefield","Shop Machinery","HSM Vol. 34 No. 6 Nov-Dec 2015","42"
    "Additions and Modifications to the Mini-Lathe: Steady Rests","Ted Hansen","Lathes","HSM Vol. 34 No. 6 Nov-Dec 2015","56"
    "Band Saw Tips","Paul Anderson","Shop Machinery","HSM Vol. 34 No. 6 Nov-Dec 2015","62"
    "Randolph's Shop Class: The Volstro System","J. Randolph Bulgin","Shop Accessories","HSM Vol. 34 No. 6 Nov-Dec 2015","64"
    "Beginners' Tips from the Toolmaker: Small Hole Gages","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 34 No. 6 Nov-Dec 2015","71"
    "Brain Snapper","Chuck St. Louis","Miscellaneous","HSM Vol. 35 No. 1 Jan-Feb 2016","12"
    "Adapting a Bridgeport-style Right Angle Drive to a Tree Mill","Harvey Kratz","Mills","HSM Vol. 35 No. 1 Jan-Feb 2016","18"
    "Docking a Smartphone","R. G. Sparber","Miscellaneous","HSM Vol. 35 No. 1 Jan-Feb 2016","20"
    "Cutter Grinder Improvements","William Vander-Reyden","Shop Machinery","HSM Vol. 35 No. 1 Jan-Feb 2016","26"
    "Funky Power Tapper","Carl Blum","Shop Machinery","HSM Vol. 35 No. 1 Jan-Feb 2016","34"
    "A Lathe Tool Height Gage","Jim Gavin","Lathes","HSM Vol. 35 No. 1 Jan-Feb 2016","42"
    "Max, My E-Z Boring Tool Holder","Donald Erickson","Shop Accessories","HSM Vol. 35 No. 1 Jan-Feb 2016","48"
    "Additions and Modifications to the Mini-Lathe: Vertical Milling Attachment","Ted Hansen","Lathes","HSM Vol. 35 No. 1 Jan-Feb 2016","50"
    "Randolph's Shop Class: The SINE","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 35 No. 1 Jan-Feb 2016","58"
    "Beginners' Tips from the Toolmaker: Calipers","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 35 No. 1 Jan-Feb 2016","64"
    "Shoes for Enco's 12x36 Gearhead Lathe","Joe Fox","Lathes","HSM Vol. 35 No. 1 Jan-Feb 2016","68"
    "The IHC Titan 50 HP - Part One","Doug Kelley","Engines","HSM Vol. 35 No. 2 Mar-Apr 2016","12"
    "The Fifteen Puzzle","J. Randolph Bulgin","Miscellaneous","HSM Vol. 35 No. 2 Mar-Apr 2016","24"
    "Vise Pads","Fred Prestridge","Shop Accessories","HSM Vol. 35 No. 2 Mar-Apr 2016","32"
    "Gain Pitch Thread","Richard Hanley","General Machining Knowledge","HSM Vol. 35 No. 2 Mar-Apr 2016","36"
    "Jaw Repair - Using a Cheap and Nasty Tool Post Grinder","John Viggers","Lathes","HSM Vol. 35 No. 2 Mar-Apr 2016","38"
    "SuperMax Mill Repair","David R.  MacManus","Mills","HSM Vol. 35 No. 2 Mar-Apr 2016","46"
    "Additions and Modifications to the Mini-Lathe: A Horizontal Milling Attachment","Ted Hansen","Lathes","HSM Vol. 35 No. 2 Mar-Apr 2016","52"
    "Randolph's Shop Class: Threads","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 35 No. 2 Mar-Apr 2016","60"
    "Beginners' Tips from the Toolmaker: Vernier Calipers","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 35 No. 2 Mar-Apr 2016","66"
    "Book Review: The Turret-Ram Milling Machine For the Beginner by J. Randolph Bulgin","George Bulliss","Hobby Community","HSM Vol. 35 No. 3 May-Jun 2016","56"
    "Book Review: STEEL - From Mine to Mill, the Metal that Made America by Brooke C. Stoddard","George Bulliss","Hobby Community","HSM Vol. 35 No. 3 May-Jun 2016","56"
    "A Swivel Yoke for the Mini-Mill","Chris Howie","Mills","HSM Vol. 35 No. 3 May-Jun 2016","14"
    "An Antique Machine Shop","Ronald Hoffman","Hobby Community","HSM Vol. 35 No. 3 May-Jun 2016","26"
    "Homemade Hand Tapper","Pete Sorenson","Shop Accessories","HSM Vol. 35 No. 3 May-Jun 2016","32"
    "The IHC Titan 50 HP - Part Two","Doug Kelley","Engines","HSM Vol. 35 No. 3 May-Jun 2016","42"
    "Protecting the Change Gears","Samuel Will","Lathes","HSM Vol. 35 No. 3 May-Jun 2016","48"
    "Making a Rocker","Don Wiederhold","Lathes","HSM Vol. 35 No. 3 May-Jun 2016","50"
    "Angle Half Nut","R. G. Sparber","Miscellaneous","HSM Vol. 35 No. 3 May-Jun 2016","58"
    "Additions and Modifications to the Mini-Lathe: Fine Feeds and Torque","Ted Hansen","Lathes","HSM Vol. 35 No. 3 May-Jun 2016","52"
    "Randolph's Shop Class: Material Storage","J. Randolph Bulgin","Miscellaneous","HSM Vol. 35 No. 3 May-Jun 2016","60"
    "Beginners' Tips from the Toolmaker: Basic Turning","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 35 No. 3 May-Jun 2016","66"
    "Book Review: 30th Edition Machinery's Handbook by Industrial Press","George Bulliss","Hobby Community","HSM Vol. 35 No. 4 Jul-Aug 2016","50"
    "A Boring and Facing Head - Part One","Graham Meek","Mills","HSM Vol. 35 No. 4 Jul-Aug 2016","10"
    "Quick and Easy Setups!","Maurice King","Shop Accessories","HSM Vol. 35 No. 4 Jul-Aug 2016","20"
    "Improving the Accuracy of a Vertical Mill","Jim Gavin","Mills","HSM Vol. 35 No. 4 Jul-Aug 2016","22"
    "Reversing Gear for a Grizzly G0602 Lathe","Richard Robertson","Lathes","HSM Vol. 35 No. 4 Jul-Aug 2016","34"
    "Quarter-Turn Thumbscrew","Larry Rudd","Miscellaneous","HSM Vol. 35 No. 4 Jul-Aug 2016","38"
    "The IHC Titan 50 HP - Part Three","Doug Kelley","Engines","HSM Vol. 35 No. 4 Jul-Aug 2016","42"
    "Edge Finder Zero Block","Mark Schell","Shop Accessories","HSM Vol. 35 No. 4 Jul-Aug 2016","67"
    "Microscope Illuminator","Terrell E. Koken","Miscellaneous","HSM Vol. 35 No. 4 Jul-Aug 2016","68"
    "Metric Threading","Marc Pohm","General Machining Knowledge","HSM Vol. 35 No. 4 Jul-Aug 2016","72"
    "Additions and Modifications to the Mini-Lathe: Ball Thrust Bearings and Working with Wood","Ted Hansen","Lathes","HSM Vol. 35 No. 4 Jul-Aug 2016","52"
    "Randolph's Shop Class: Moving Machinery","J. Randolph Bulgin","Miscellaneous","HSM Vol. 35 No. 4 Jul-Aug 2016","58"
    "Beginners' Tips from the Toolmaker: Fly Cutters","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 35 No. 4 Jul-Aug 2016","64"
    "Making a Pendulum Clock - Part One","Lowell Braxton","Mills","HSM Vol. 35 No. 5 Sep-Oct 2016","47"
    "Shop Saw","Duane Dehnicke","Shop Machinery","HSM Vol. 35 No. 5 Sep-Oct 2016","28"
    "Collet Adapter","Harvey Kratz","Shop Accessories","HSM Vol. 35 No. 5 Sep-Oct 2016","42"
    "Cold Saw Cart","Don Wiederhold","Shop Accessories","HSM Vol. 35 No. 5 Sep-Oct 2016","44"
    "The IHC Titan 50 HP - Part Four","Doug Kelley","Engines","HSM Vol. 35 No. 5 Sep-Oct 2016","54"
    "Additions and Modifications to the Mini-Lathe: Turning Tapers","Ted Hansen","Lathes","HSM Vol. 35 No. 5 Sep-Oct 2016","60"
    "Randolph's Shop Class: Reamers and Reaming","J. Randolph Bulgin","Miscellaneous","HSM Vol. 35 No. 5 Sep-Oct 2016","66"
    "The Rupnow Flathead Engine - Part One","Brian Rupnow","Engines","HSM Vol. 35 No. 6 Nov-Dec 2016","10"
    "Copying a Die Filer","Ken Roth","Shop Accessories","HSM Vol. 35 No. 6 Nov-Dec 2016","20"
    "Carriage Indicators for an Atlas Lathe","Dave Harnish","Lathes","HSM Vol. 35 No. 6 Nov-Dec 2016","26"
    "A Threaded Collet for a Three-Jaw Chuck","R. G. Sparber","Shop Accessories","HSM Vol. 35 No. 6 Nov-Dec 2016","28"
    "Impossible Sliding Blocks","J. Randolph Bulgin","Projects","HSM Vol. 35 No. 6 Nov-Dec 2016","32"
    "Making a Pendulum Clock - Part Two","Lowell Braxton","Clocks","HSM Vol. 35 No. 6 Nov-Dec 2016","42"
    "A Self-Centering Holder for Sharpening Drills","Robert E. Poupard","Shop Accessories","HSM Vol. 35 No. 6 Nov-Dec 2016","52"
    "Additions and Modifications to the Mini-Lathe: Upgrading Some Upgrades","Ted Hansen","Lathes","HSM Vol. 35 No. 6 Nov-Dec 2016","56"
    "Randolph's Shop Class: Horizontal Attachments","J. Randolph Bulgin","Shop Accessories","HSM Vol. 35 No. 6 Nov-Dec 2016","64"
    "The Rupnow Flathead Engine - Part Two","Brian Rupnow","Engines","HSM Vol. 36 No. 1 Jan-Feb 2017","28"
    "Evolution of a Carburetor","Graham Meek","Engines","HSM Vol. 36 No. 1 Jan-Feb 2017","10"
    "Restoration and Reconnection","Roger Taylor","Welding/Foundry/Forging","HSM Vol. 36 No. 1 Jan-Feb 2017","24"
    "What is a Blade Skate and why do I Need One?","R. G. Sparber","Shop Machinery","HSM Vol. 36 No. 1 Jan-Feb 2017","27"
    "Depth Stop Revision","Ronald Casteel","Shop Accessories","HSM Vol. 36 No. 1 Jan-Feb 2017","42"
    "Making a Pendulum Clock - Part Three","Lowell Braxton","Clocks","HSM Vol. 36 No. 1 Jan-Feb 2017","44"
    "Building the Beam Engine Mary","Ernie Noa","Engines","HSM Vol. 36 No. 1 Jan-Feb 2017","70"
    "Additions and Modifications to the Mini-Lathe: A Workshop Cabinet","Ted Hansen","Shop Accessories","HSM Vol. 36 No. 1 Jan-Feb 2017","50"
    "Randolph's Shop Class: Vertical Slotter","J. Randolph Bulgin","Shop Machinery","HSM Vol. 36 No. 1 Jan-Feb 2017","60"
    "Beginners' Tips from the Toolmaker: High Speed Steel","Sandro Di Filippo","Lathes","HSM Vol. 36 No. 1 Jan-Feb 2017","66"
    "Making Gear Cutters using a Button Formed Profile","Martin Gearing","Lathes","HSM Vol. 36 No. 2 Mar-Apr 2017","12"
    "Dedicated Spot and Center Drill Holders","Dave Garrett","Lathes","HSM Vol. 36 No. 2 Mar-Apr 2017","26"
    "A Trip Through Bernie's Shop","Bernie Kaczkowski","Miscellaneous","HSM Vol. 36 No. 2 Mar-Apr 2017","30"
    "A Small Wheel Adapter","David Myers","Shop Accessories","HSM Vol. 36 No. 2 Mar-Apr 2017","36"
    "Making a Pendulum Clock - Part Four","Lowell Braxton","Clocks","HSM Vol. 36 No. 2 Mar-Apr 2017","38"
    "The Rupnow Flathead Engine - Part Three","Brian Rupnow","Engines","HSM Vol. 36 No. 2 Mar-Apr 2017","48"
    "Randolph's Shop Class: Tool Caddys","J. Randolph Bulgin","Shop Accessories","HSM Vol. 36 No. 2 Mar-Apr 2017","56"
    "Beginners' Tips from the Toolmaker: Lathe Tooling: Carbide","Sandro Di Filippo","Lathes","HSM Vol. 36 No. 2 Mar-Apr 2017","64"
    "Pop Rivet Die","Ron Geppert","Miscellaneous","HSM Vol. 36 No. 2 Mar-Apr 2017","68"
    "Profiled Fly Cutters for Gear Cutting","Martin Gearing","Lathes","HSM Vol. 36 No. 3 May-Jun 2017","26"
    "A Handwheel Dial for the Mini-Lathe","Graham Meek","Lathes","HSM Vol. 36 No. 3 May-Jun 2017","12"
    "My Completed PM Research Engine","Ernie Noa","Engines","HSM Vol. 36 No. 3 May-Jun 2017","36"
    "Another DRO Finds a Mill","Tom McAllister","Mills","HSM Vol. 36 No. 3 May-Jun 2017","42"
    "A Poor Man's Worm Drive","Clarence Elias","Mills","HSM Vol. 36 No. 3 May-Jun 2017","56"
    "The Rupnow Flathead Engine - Part Four","Brian Rupnow","Engines","HSM Vol. 36 No. 3 May-Jun 2017","47"
    "Cherry Hill - 2017 Craftsman of the Year Award","Craig Libuse","Hobby Community","HSM Vol. 36 No. 3 May-Jun 2017","59"
    "Using Spacer Block","R. G. Sparber","General Machining Knowledge","HSM Vol. 36 No. 3 May-Jun 2017","70"
    "Randolph's Shop Class: Machine Shop Alloys","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 36 No. 3 May-Jun 2017","61"
    "Beginners' Tips from the Toolmaker: More About Threads","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 36 No. 3 May-Jun 2017","67"
    "Say Goodbye to the Compound - Part One","Richard Rex","Lathes","HSM Vol. 36 No. 4 Jul-Aug 2017","8"
    "Repairing a Broken Bolt","William Vander-Reyden","Miscellaneous","HSM Vol. 36 No. 4 Jul-Aug 2017","22"
    "Understanding Hand Reamers","Roger Taylor","General Machining Knowledge","HSM Vol. 36 No. 4 Jul-Aug 2017","26"
    "Review and Teardown of the South Bend SB-1002 - the ""New"" 10K Lathe","Doug Ripka","Lathes","HSM Vol. 36 No. 4 Jul-Aug 2017","34"
    "Fox .36X","John Buffum","Engines","HSM Vol. 36 No. 4 Jul-Aug 2017","50"
    "Converting a Vertical Mill to a Vertical Lathe","Thomas Allsup","Mills","HSM Vol. 36 No. 4 Jul-Aug 2017","54"
    "Knobs","Bernard Cooper","Miscellaneous","HSM Vol. 36 No. 4 Jul-Aug 2017","70"
    "Randolph's Shop Class: The Common Twist Drill","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 36 No. 4 Jul-Aug 2017","57"
    "Beginners' Tips from the Toolmaker: Measuring Threads","Sandro Di Filippo","General Machining Knowledge","HSM Vol. 36 No. 4 Jul-Aug 2017","65"
    "A Small Dividing Head for the Home Shop - Part One","John Manhardt","Mills","HSM Vol. 36 No. 5 Sep-Oct 2017","8"
    "Mini-Lathe Improvements","Michael Beresford","Lathes","HSM Vol. 36 No. 5 Sep-Oct 2017","19"
    "Yet Another Taper Attachment","Bob Woods","Lathes","HSM Vol. 36 No. 5 Sep-Oct 2017","24"
    "An Arbor-Mounted Universal Tap Holder (also Charles Levinski)","John Lindo","Shop Accessories","HSM Vol. 36 No. 5 Sep-Oct 2017","28"
    "A Centrifugal Seperator for the Shop Vacuum","Ron Geppert","Miscellaneous","HSM Vol. 36 No. 5 Sep-Oct 2017","38"
    "Mill/Drill Gib Lock","Michael Jenks","Mills","HSM Vol. 36 No. 5 Sep-Oct 2017","44"
    "Band-Aid for an Old Drill Press","Timothy J. Apps","Shop Machinery","HSM Vol. 36 No. 5 Sep-Oct 2017","50"
    "Say Goodbye to the Compound - Part Two","Richard Rex","Lathes","HSM Vol. 36 No. 5 Sep-Oct 2017","56"
    "Randolph's Shop Class: Toolholder for the Quick-Change Tool Post","J. Randolph Bulgin","Lathes","HSM Vol. 36 No. 5 Sep-Oct 2017","67"
    "Any Thread: A Parallel-linked, Adjustable Sine Bar Threading Attachment - Part One","Herb Yohe","Lathes","HSM Vol. 36 No. 6 Nov-Dec 2017","8"
    "Miniature Spark Plugs Made Easy","Graham Meek","Engines","HSM Vol. 36 No. 6 Nov-Dec 2017","24"
    "Nash Engine Build","Doug Kelley","Engines","HSM Vol. 36 No. 6 Nov-Dec 2017","34"
    "A Different Spacer for the Lathe Chuck","William Vander-Reyden","Lathes","HSM Vol. 36 No. 6 Nov-Dec 2017","37"
    "Improving the Pulley Serviceability on an RF-30 Mill/Drill","John M.  Herrmann","Mills","HSM Vol. 36 No. 6 Nov-Dec 2017","42"
    "A Small Dividing Head for the Home Shop - Part Two","John Manhardt","Mills","HSM Vol. 36 No. 6 Nov-Dec 2017","46"
    "An Electronic Edge Finder","R.G. Sparber","Miscellaneous","HSM Vol. 36 No. 6 Nov-Dec 2017","56"
    "The Nursery","Richard Henley","Miscellaneous","HSM Vol. 36 No. 6 Nov-Dec 2017","70"
    "Randolph's Shop Class: Shaft Repair","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 36 No. 6 Nov-Dec 2017","62"
    "Hold Onto that Boring Bar - Part One","Michael Ward","Lathes","HSM Vol. 37 No. 1 Jan-Feb 2018","10"
    "A Dremel Bracket","Jerry L. Sokol","Miscellaneous","HSM Vol. 37 No. 1 Jan-Feb 2018","18"
    "Making Piston Rings","Ted Hansen","Engines","HSM Vol. 37 No. 1 Jan-Feb 2018","20"
    "Any Thread: A Parallel-linked, Adjustable Sine Bar Threading Attachment - Part Two","Herb Yohe","Lathes","HSM Vol. 37 No. 1 Jan-Feb 2018","24"
    "Model Radiators","David Bradley","Engines","HSM Vol. 37 No. 1 Jan-Feb 2018","37"
    "A Small Dividing Head for the Home Shop - Part Three","John Manhardt","Mills","HSM Vol. 37 No. 1 Jan-Feb 2018","42"
    "The Old, Retired Shop Teacher: The Hamilton Sensitive Drill Press and Tapping Machine","Rogert Taylor","Shop Machinery","HSM Vol. 37 No. 1 Jan-Feb 2018","52"
    "A Depthing Tool (The Wrong Way to do a Machining Operation)","Ernie Noa","Miscellaneous","HSM Vol. 37 No. 1 Jan-Feb 2018","66"
    "Randolph's Shop Class: Differential Threads","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 37 No. 1 Jan-Feb 2018","60"
    "The Project","Graham Meek","Engines","HSM Vol. 37 No. 2 Mar-Apr 2018","12"
    "Fancy Knurling","Gary P.  Paine","General Machining Knowledge","HSM Vol. 37 No. 2 Mar-Apr 2018","22"
    "A Spindle Brake for the Jet 13"" Lathe","Paul Temple","Lathes","HSM Vol. 37 No. 2 Mar-Apr 2018","26"
    "Independent Rest","David Bradley","Lathes","HSM Vol. 37 No. 2 Mar-Apr 2018","36"
    "Building a Power Feed for a Milling Machine","Blaine Geddes","Mills","HSM Vol. 37 No. 2 Mar-Apr 2018","38"
    "Hold Onto that Boring Bar - Part Two","Michael Ward","Lathes","HSM Vol. 37 No. 2 Mar-Apr 2018","46"
    "Randolph's Shop Class: Rebuilding a (your machine here)","J. Randolph Bulgin","Miscellaneous","HSM Vol. 37 No. 2 Mar-Apr 2018","60"
    "The Old, Retired Shop Teacher: Building a Train Whistle","Rogert Taylor","Miscellaneous","HSM Vol. 37 No. 2 Mar-Apr 2018","66"
    "Henry Ford's Quadricycle Engine in Half-Scale - Part One","Christopher Vasconcelos","Engines","HSM Vol. 37 No. 3 May-Jun 2018","12"
    "The First Engine","Larry Shulda","Engines","HSM Vol. 37 No. 3 May-Jun 2018","23"
    "Tramming Made Easy","David Ford","Mills","HSM Vol. 37 No. 3 May-Jun 2018","24"
    "A Micrometer Height Gauge","Graham Meek","Miscellaneous","HSM Vol. 37 No. 3 May-Jun 2018","28"
    "A Two Piece Milling Vise","Jerry L. Sokol","Mills","HSM Vol. 37 No. 3 May-Jun 2018","42"
    "A Mini-Lathe Carriage Guide","Ted Hansen","Lathes","HSM Vol. 37 No. 3 May-Jun 2018","44"
    "Furl the Mainsail","Paul Anderson","Miscellaneous","HSM Vol. 37 No. 3 May-Jun 2018","46"
    "Chuck Balmer - 2018 Craftsman of the Year Award","Craig Libuse","Hobby Community","HSM Vol. 37 No. 3 May-Jun 2018","50"
    "My First Clock","Ernie Noa","Clocks","HSM Vol. 37 No. 3 May-Jun 2018","66"
    "Randolph's Shop Class: Building a Loom - Part One","J. Randolph Bulgin","Projects","HSM Vol. 37 No. 3 May-Jun 2018","54"
    "The Old, Retired Shop Teacher: The Anti-Compound Accessory","Rogert Taylor","Lathes","HSM Vol. 37 No. 3 May-Jun 2018","64"
    "A Lathe Belt-Drive Unit - Part One","Michael Ward","Lathes","HSM Vol. 37 No. 4 Jul-Aug 2018","10"
    "Machining the MLA Sine Plate","Fred Prestridge","Projects","HSM Vol. 37 No. 4 Jul-Aug 2018","22"
    "My Retractable Toolholder Design","Don Wiederhold","Lathes","HSM Vol. 37 No. 4 Jul-Aug 2018","26"
    "Custom Tooling for a Restoration Project","Frank DiSanti","Shop Machinery","HSM Vol. 37 No. 4 Jul-Aug 2018","32"
    "Turning a Tippe Top","Andrew Bernat","Projects","HSM Vol. 37 No. 4 Jul-Aug 2018","34"
    "Spiffing up the Saw","David Bradley","Shop Machinery","HSM Vol. 37 No. 4 Jul-Aug 2018","38"
    "My Version of the Meek Handwheel","Robert L. Franklin, Ph.D.","Lathes","HSM Vol. 37 No. 4 Jul-Aug 2018","42"
    "Henry Ford's Quadricycle Engine in Half-Scale - Part Two","Christopher Vasconcelos","Engines","HSM Vol. 37 No. 4 Jul-Aug 2018","44"
    "Randolph's Shop Class: Building a Loom - Part Two","J. Randolph Bulgin","Projects","HSM Vol. 37 No. 4 Jul-Aug 2018","56"
    "The Old, Retired Shop Teacher: Angle Grinder Adaptor","Rogert Taylor","Shop Machinery","HSM Vol. 37 No. 4 Jul-Aug 2018","66"
    "Soft Jaws Solve Many Issues","John Lindo","Lathes","HSM Vol. 37 No. 5 Sep-Oct 2018","10"
    "Building a Universal Pillar Tool","Jerry L. Sokol","Shop Machinery","HSM Vol. 37 No. 5 Sep-Oct 2018","22"
    "A Tapping Attachment for Small Taps","Graham Meek","Shop Accessories","HSM Vol. 37 No. 5 Sep-Oct 2018","26"
    "A Lathe Belt-Drive Unit - Part Two","Michael Ward","Lathes","HSM Vol. 37 No. 5 Sep-Oct 2018","30"
    "Henry Ford's Quadricycle Engine in Half-Scale - Part Three","Christopher Vasconcelos","Engines","HSM Vol. 37 No. 5 Sep-Oct 2018","42"
    "Portable Cut Off Saw Cart","Don Wiederhold","Shop Accessories","HSM Vol. 37 No. 5 Sep-Oct 2018","52"
    "Why Have CNC in Your Home Shop","R.G. Sparber","General Machining Knowledge","HSM Vol. 37 No. 5 Sep-Oct 2018","55"
    "Cooling With Steam: Old Iron in Souther Patagonia","Kurt, Dr. Hillig","Miscellaneous","HSM Vol. 37 No. 5 Sep-Oct 2018","57"
    "Randolph's Shop Class: Building a Loom - Part Three","J. Randolph Bulgin","Projects","HSM Vol. 37 No. 5 Sep-Oct 2018","64"
    "The Old, Retired Shop Teacher: My Steady Rest","Rogert Taylor","Shop Accessories","HSM Vol. 37 No. 5 Sep-Oct 2018","71"
    "Hydraulic Downfeed for the 4 x 6 Bandsaw - Part One","John M. Herrmann","Shop Machinery","HSM Vol. 37 No. 6 Nov-Dec 2018","8"
    "The Max-Aire Diffuser","Walter Yetman","Engines","HSM Vol. 37 No. 6 Nov-Dec 2018","24"
    "Using a Virtual Reference Point in the Mill","Edward P. Alciatore III","Mills","HSM Vol. 37 No. 6 Nov-Dec 2018","32"
    "Fun With Collets","William Vander-Reyden","Miscellaneous","HSM Vol. 37 No. 6 Nov-Dec 2018","38"
    "Henry Ford's Quadricycle Engine in Half-Scale - Part Four","Christopher Vasconcelos","Engines","HSM Vol. 37 No. 6 Nov-Dec 2018","44"
    "Randolph's Shop Class: Building a Loom - Part Four","J. Randolph Bulgin","Projects","HSM Vol. 37 No. 6 Nov-Dec 2018","52"
    "The Old, Retired Shop Teacher: A Neat Little Grinder","Rogert Taylor","Shop Machinery","HSM Vol. 37 No. 6 Nov-Dec 2018","64"
    "A Boring and Facing Head - Part Two","Graham Meek","Mills","HSM Vol. 35 No. 5 Sep-Oct 2016","47"
    "Scraping a 9 x 20 Lathe - a Beginner's Attempt","Larry Curts","Lathes","HSM Vol. 38 No. 1 Jan-Feb 2019","8"
    "A Different Kind of Jack","Richard Brien","Miscellaneous","HSM Vol. 38 No. 1 Jan-Feb 2019","26"
    "Drip Feed Coolant System","John Lindo","Miscellaneous","HSM Vol. 38 No. 1 Jan-Feb 2019","27"
    "Manual Numerical Control: Creating 2D Curves on Your Lathe","Ronald Pierik","Lathes","HSM Vol. 38 No. 1 Jan-Feb 2019","30"
    "Hydraulic Downfeed for the 4 x 6 Bandsaw - Part Two","John M. Herrmann","Shop Machinery","HSM Vol. 38 No. 1 Jan-Feb 2019","44"
    "T-Square Table Saw Fence","Paul Anderson","Shop Machinery","HSM Vol. 38 No. 1 Jan-Feb 2019","52"
    "Randolph's Shop Class: Outboard Bearing","J. Randolph Bulgin","Lathes","HSM Vol. 38 No. 1 Jan-Feb 2019","66"
    "The Old, Retired Shop Teacher: Broken Cast Iron with Missing Pieces","Roger Taylor","Welding/Foundry/Forging","HSM Vol. 38 No. 1 Jan-Feb 2019","60"
    "A Machine Way Alignment Tool - Part One","Michael Ward","Lathes","HSM Vol. 38 No. 2 Mar-Apr 2019","9"
    "Perfect Cylinders - The Easy Way","Clif Roemmich","Engines","HSM Vol. 38 No. 2 Mar-Apr 2019","26"
    "The Conning Tower Nut and Swiss Cheese - Mini-Lathe Cross Slide Mods","John Lindo","Lathes","HSM Vol. 38 No. 2 Mar-Apr 2019","28"
    "Adding a Fine/Power Feed to an Emco FB2 Mill Drill","Graham Meek","Mills","HSM Vol. 38 No. 2 Mar-Apr 2019","34"
    "A Hollow Screw Jack","Brian Weeks","Shop Accessories","HSM Vol. 38 No. 2 Mar-Apr 2019","52"
    "The Design and Building of a Ball Turner","Gary P.  Paine","Lathes","HSM Vol. 38 No. 2 Mar-Apr 2019","54"
    "Randolph's Shop Class: A Workbench to Suit Your Needs","J. Randolph Bulgin","Shop Accessories","HSM Vol. 38 No. 2 Mar-Apr 2019","69"
    "The Old, Retired Shop Teacher: An Unusual Little Machine Vise Find","Roger Taylor","Shop Accessories","HSM Vol. 38 No. 2 Mar-Apr 2019","67"
    "My 1/2 Scale Oliver Tractor","Rich Dosdall","Projects","HSM Vol. 38 No. 3 May-Jun 2019","9"
    "James T. Hastings - 2019 Craftsman of the Year Award","Craig Libuse","Hobby Community","HSM Vol. 38 No. 3 May-Jun 2019","22"
    "Floating Knurl Tool","Don Wiederhold","General Machining Knowledge","HSM Vol. 38 No. 3 May-Jun 2019","26"
    "Clock Bushing Repair","William Vander-Reyden","Clocks","HSM Vol. 38 No. 3 May-Jun 2019","26"
    "A Machine Way Alignment Tool - Part Two","Michael Ward","Lathes","HSM Vol. 38 No. 3 May-Jun 2019","36"
    "Rejuvenating My Steady Rest","Fred Prestridge","Lathes","HSM Vol. 38 No. 3 May-Jun 2019","52"
    "A Blast Media Separator and Classifier","Ronald Pierik","Miscellaneous","HSM Vol. 38 No. 3 May-Jun 2019","55"
    "A Small Knee Mill Riser Block","Gary Nichols","Mills","HSM Vol. 38 No. 3 May-Jun 2019","58"
    "Randolph's Shop Class: Loom Addendum","J. Randolph Bulgin","Projects","HSM Vol. 38 No. 3 May-Jun 2019","68"
    "The Old Retired Shop Teacher: Tips for Hole Saws in Metalworking","Roger Taylor","General Machining Knowledge","HSM Vol. 38 No. 3 May-Jun 2019","62"
    "Metric Threading on an Antique Lathe","Blaine Geddes","Lathes","HSM Vol. 38 No. 4 Jul-Aug 2019","9"
    "Simple Radius Tool for a South Bend Lathe","Ron Anders","Lathes","HSM Vol. 38 No. 4 Jul-Aug 2019","20"
    "Living with a Metal cutting Band Saw","Graham Meek","Shop Machinery","HSM Vol. 38 No. 4 Jul-Aug 2019","26"
    "A Machine Way Alignment Tool - Part Three","Michael Ward","Lathes","HSM Vol. 38 No. 4 Jul-Aug 2019","42"
    "Enhancing the Sherline Mill and Lathe: Workpiece Supports","Bill Schirado","General Machining Knowledge","HSM Vol. 38 No. 4 Jul-Aug 2019","54"
    "The Old Retired Shop Teacher: Get the Kids into the Shop","Roger Taylor","Miscellaneous","HSM Vol. 38 No. 4 Jul-Aug 2019","60"
    "Randolph's Shop Class: Steady Rest for a Wood Lathe","J. Randolph Bulgin","Lathes","HSM Vol. 38 No. 4 Jul-Aug 2019","66"
    "A Walking Beam Engine - Part One","Don Birkley","Engines","HSM Vol. 38 No. 5 Sep-Oct 2019","8"
    "Emergency Limit Stop for the Lathe","Brian Weeks","Lathes","HSM Vol. 38 No. 5 Sep-Oct 2019","26"
    "A 3D CAD Primer - Learn the Basics and Try it for Free","Alibre","Computers","HSM Vol. 38 No. 5 Sep-Oct 2019","28"
    "A Machine Way Alignment Tool - Part Four","Michael Ward","Lathes","HSM Vol. 38 No. 5 Sep-Oct 2019","38"
    "Adjust Your Feed With a Twist of a Knob","Harvey Kratz","Lathes","HSM Vol. 38 No. 5 Sep-Oct 2019","48"
    "A Spindle Lock for an X1 Mill","Graham Meek","Mills","HSM Vol. 38 No. 5 Sep-Oct 2019","50"
    "Enhancing the Sherline Mill and Lathe: Y-Axis Tooling Plate","Bill Schirado","General Machining Knowledge","HSM Vol. 38 No. 5 Sep-Oct 2019","56"
    "The Old Retired Shop Teacher: Multi-Purpose Shop Storage Idea","Roger Taylor","Shop Accessories","HSM Vol. 38 No. 5 Sep-Oct 2019","62"
    "Randolph's Shop Class: Second Generation Tool Caddy","J. Randolph Bulgin","Shop Accessories","HSM Vol. 38 No. 5 Sep-Oct 2019","64"
    "Fair and Square","Kurt, Dr. Hillig","General Machining Knowledge","HSM Vol. 38 No. 6 Nov-Dec 2019","8"
    "The Leon Ridenour No. 2 Ford Engine","Rolland Huff","Engines","HSM Vol. 38 No. 6 Nov-Dec 2019","24"
    "A Walking Beam Engine - Part Two","Don Birkley","Engines","HSM Vol. 38 No. 6 Nov-Dec 2019","34"
    "The Silver Bullet Spill Proof Cutting Oil Container","Ron Geppert","Miscellaneous","HSM Vol. 38 No. 6 Nov-Dec 2019","44"
    "Mini-Lathe Lead Screw Hand Crank","Gary Wagoner","Lathes","HSM Vol. 38 No. 6 Nov-Dec 2019","48"
    "Enhancing the Sherline Mill and Lathe: Adjustable Angle Tooling Plate","Bill Schirado","Shop Accessories","HSM Vol. 38 No. 6 Nov-Dec 2019","52"
    "The Old Retired Shop Teacher: Lathe Tubing Cutter","Roger Taylor","Lathes","HSM Vol. 38 No. 6 Nov-Dec 2019","58"
    "Randolph's Shop Class: Machining a Sine Bar","J. Randolph Bulgin","General Machining Knowledge","HSM Vol. 38 No. 6 Nov-Dec 2019","60"
    "An Introduction to Computer Aided Design (CAD)- Part One","Bob Guarnieri","Computers","HSM Vol. 39 No. 1 Jan-Feb 2020","8"
    "A Better Vise Stop","Ken Strauss","Shop Accessories","HSM Vol. 39 No. 1 Jan-Feb 2020","26"
    "Icosahedron Vertex Clamps","Kurt, Dr. Hillig","Projects","HSM Vol. 39 No. 1 Jan-Feb 2020","28"
    "Adjustable Tool Rest","Jerrold Tiers","Shop Accessories","HSM Vol. 39 No. 1 Jan-Feb 2020","38"
    "A Couple of Mill Upgrades","Graham Meek","Mills","HSM Vol. 39 No. 1 Jan-Feb 2020","45"
    "Hardinge Speed Lathe Brake","Don Wiederhold","Lathes","HSM Vol. 39 No. 1 Jan-Feb 2020","52"
    "A Walking Beam Engine - Part Three","Don Birkley","Engines","HSM Vol. 39 No. 1 Jan-Feb 2020","55"
    "The Old Retired Shop Teacher: Little 4 x 6 Band Saw Tune-Up","Roger Taylor","Shop Machinery","HSM Vol. 39 No. 1 Jan-Feb 2020","62"
    "A Tramming Device for a Benchmaster Mill","Jerrold Tiers","Mills","HSM Vol. 39 No. 2 Mar/Apr 2020","10"
    "Gear Teeth Dentistry","Ron Pierik","General Machining Knowledge","HSM Vol. 39 No. 2 Mar/Apr 2020","24"
    "Y-Axis Stops for the Emco FB 2","Graham Meek","Mills","HSM Vol. 39 No. 2 Mar/Apr 2020","30"
    "An Introducation to Computer Aided Design (CAD) Part Two","Bob Guarnieri","Computers","HSM Vol. 39 No. 2 Mar/Apr 2020","38"
    "A Simple Gravity Powered Band Saw Fence","Brian Weeks","Shop Machinery","HSM Vol. 39 No. 2 Mar/Apr 2020","51"
    "Making Custom Washers and Spacers","R.G. Sparber","General Machining Knowledge","HSM Vol. 39 No. 2 Mar/Apr 2020","56"
    "The Old Retired Shop Teacher: Take the Muscle Out of Lathe Chuck Handling","Roger Taylor","lathes","HSM Vol. 39 No. 2 Mar/Apr 2020","60"
    ''')
    '''
    Formats of different publication entries: [x] is line number in raw
    data.  This could stand some regularlizing, along with author names and
    titles.
    
    VP format:
        HSM Vol. 01 No. 1 Jan-Feb 1982,14 [5544]
    MI format:
        HSM'82:J/A18,S/O31,N/D43, HSM'83:J/F41,M/A47,M/J44 [3376]
        HTIM:1-2; TMBR#3:190 [1990]
        MEW#10,63;#11,20;#12,38 [2059]
        MW Apr. 99, 24, MW Jun. 99, 28, Aug. 99, 32, Oct. 99, 30, Dec. 99, 48 [240]
        PiM-Oct.,'96, 35, Dec.'96, 34 [3614]
        TMBR#1:1-2; TMBR#2:v; HTIM:ii; TMBR#3:2 [3103]
        TMBR#2:v; vi HTIM:iii [2196]
        TMBR#3 1st printing:94, 139. & 251 [1698]
        TMBR#3 2nd printing:94, 139. & 251 [1697]
    '''
def Regularlize(string):
    'Fix inconsistencies in the raw data strings'
    string = re.sub("  +", " ", string)
    return string
def GetData():
    'Return a sequence of named tuples of the form (title, author, pub)'
    NT = namedtuple("NT", "title author pub")
    seq = []
    # Metalworking index
    for line in Regularlize(mi).split("\n"):
        line = line.strip()
        if not line or line[0] == "!":
            continue
        seq.append(NT(*line.split("\t")))
    def ProcessVP(raw_data):
        # Process Village Press indexes
        VP = namedtuple("VP", "title author subject issue page")
        sio = StringIO(Regularlize(raw_data))
        c = csv.reader(sio)
        for i, line in enumerate(c):
            if not i:   # Ignore first line
                continue
            # This does not read the Harold Mason article on a "Rocking,
            # Swinging Grinder table" correctly.
            title, author, subject, issue, page = VP(*line)
            pub = issue.strip() + "," + page.strip()
            seq.append(NT(title, author, pub))
    # Machinist's Workshop index
    ProcessVP(vp1)
    # Home Shop Machinist index
    ProcessVP(vp2)
    return seq
def Usage(d, status=1):
    name = sys.argv[0]
    print(dedent(f'''
    Usage:  {name} [options] [regex1 [regex2 ...]]
      Search metalworking titles for regular expressions.  Note the datasets
      have overlap, so you'll see multiple references to the same article.
      The output will be sorted by the title, even if you only e.g. print
      out the author's names or the publication.
    Examples:
      python {name} rudy
          Show all titles with the string 'rudy'
      python {name} -a rudy
          Show all authors with the string 'rudy'
      python {name} -p HSM
          Show all HSM publications
      python {name} -d
          Show all records in the data
    Options:
      -1    Print the title
      -2    Print the author
      -3    Print the publication
      -a    Search author instead of title
      -d    Dump all records to stdout
      -i    Don't ignore case
      -k    Show publication abbreviations
      -p    Search publication instead of title
      -s x  Separate printed fields with the string x (default is "{d['-s']}")
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-1"] = False     # Print title
    d["-2"] = False     # Print author
    d["-3"] = False     # Print author
    d["-d"] = False     # Dump all records
    d["-a"] = False     # Search author
    d["-i"] = True      # Ignore case
    d["-p"] = False     # Search publication
    d["-s"] = " | "     # Printing separator
    try:
        opts, args = getopt.getopt(sys.argv[1:], "123adhikps:")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("123adip"):
            d[o] = not d[o]
        elif o in ("-h", "--help"):
            d["-h"] = True
            Usage(d, status=0)
        elif o == "-k":
            print("Publication abbreviations:")
            for i in mi_key:
                print("   ", i)
            exit(0)
        elif o in ("-s",):
            d["-s"] = a
    d["all"] = False if d["-1"] or d["-2"] or d["-3"] else True
    if not d["-d"] and not args:
        Usage(d)
    return args
def PrintItem(item):
    title, author, pub = item
    if d["all"]:
        print(title, author, pub, sep=d["-s"])
    else:
        n = d["-1"] + d["-2"] + d["-3"]
        s = []
        s += [title] if d["-1"] else []
        s += [author] if d["-2"] else []
        s += [pub] if d["-3"] else []
        print(*s, sep=d["-s"])
def Search(regexp):
    r = re.compile(regexp, re.I) if d["-i"] else re.compile(regexp)
    out = []
    for item in d["data"]:
        title, author, pub = item
        if d["-a"]:
            if r.search(author):
                out.append(item)
        elif d["-p"]:
            if r.search(pub):
                out.append(item)
        elif r.search(title):
                out.append(item)
    for item in sorted(out):
        PrintItem(item)
if __name__ == "__main__": 
    d = {}      # Options dictionary
    regexps = ParseCommandLine(d)
    d["data"] = GetData()
    if d["-d"]:
        for title, author, pub in d["data"]:
            print(title, author, pub)
        exit(0)
    else:
        for regexp in regexps:
            Search(regexp)
