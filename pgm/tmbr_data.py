'''
This is from http://machinistindex.com/Metalworking_index_2000.txt
downloaded 28 Jan 2020 (site is defunct as of Aug 2021).  This information
is used to produce the 'data' variable for tmbr.py.  data is a tuple of
lines from raw_data that are from TMBR or "Hey Tim" by Lautard.  A typical
element of the tuple is

    ("A dowel puller", #1:67")

#1 means the first volume of TMBR.  67 is the page number this topic is
on.
'''

raw_data = '''
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
! Swanley, Kent BR8 8HY, England
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
Dial indicator for measuring lathe saddle movement	Lautard, Guy	HTIM:8
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
Foundry-Don't Fake a Casting Ä Make a Casting	LEWIS, JAMES R.	HSM'87:M/J48
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
Rapid Machine Tapping Drillpress	ROUBAL, WM. T. (TED}, Ph.D.	HSM'84:M/J20
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
Retaining ring ("circlip"), shop made	Lautard, Guy	HTIM:11-12
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
'''

# Get lines:  each field separated by tab characters
lines, l = [], raw_data.split("\n")
for line in l:
    line = line.strip()
    if not line or line[0] == "!":
        continue
    lines.append(line.split("\t"))
# Verify there are three fields in each line
assert(set(len(i) for i in lines) == {3})
# Keep TMBR and "Hey Tim" lines
keep = []
for line in lines:
    title, author, pub = line
    p = pub.lower()
    if "lautard" in author.lower():
        if "tmbr" in p or "htim" in p:
            keep.append((title, pub))
# Eliminate duplicates
keep = set(tuple(keep))
# Provide a tuple of the lines as the basic data structure
data = tuple(sorted(keep))
