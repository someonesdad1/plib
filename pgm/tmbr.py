'''
Index to Lautard's TMBR

    The index was taken from
    http://machinistindex.com/Metalworking_index_2000.txt, a defunct
    website.  The text included the name "Joe Landau's Metalworking Index
    2000 Edition", so maybe someone else has archived it on the web.
    
    Todo:
        - Collapse entries like 'Dial' and 'dial' into one.  Give the
          capitalized word precedence.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2008 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Index to Lautard's books
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        import sys
        import getopt
        import re
        import string
    if 1:  # Custom imports
        from wrap import dedent
        #from tmbr_data import data
        from columnize import Columnize
        from trm import TrmDP
        if 1:
            import debug
            debug.SetDebugger()
        t = TrmDP()
        t.v1 = t.pnkl
        t.v2 = t.yell
        t.v3 = t.cynl
        t.ht = t.grn
if 1:  # Data
    raw_data = '''
        "As I remember" (S. P. Timoshenko 's autobiography)	Lautard, Guy	TMBR#3:51
        "Cratex" abrasive-in-rubber	Lautard, Guy	TMBR#2:131
        "Hubers" cutting oil	Lautard, Guy	TMBR#3:102
        "Jet" propane torch head	Lautard, Guy	TMBR#1:51
        "Mouse Milk" penetrating and lubricating oil	Lautard, Guy	TMBR#3:237
        "Pull dowels" used to machine an angle plate	Lautard, Guy	TMBR#2:101
        "Quick" knurls	Lautard, Guy	TMBR#1:63-64
        "Royal" machine mount/leveling pads	Lautard, Guy	TMBR#3:71
        "Royal" vise jaw liners	Lautard, Guy	TMBR#3:70
        1/4 degree vernier	Lautard, Guy	TMBR#2:8
        15/16 hole vernier	Lautard, Guy	TMBR#1:42
        3 tapping hints	Lautard, Guy	TMBR#2:125
        75% depth of thread rule	Lautard, Guy	TMBR#1:18
        900 point slot drills	Lautard, Guy	TMBR#1:169
        A "Geometric solid" from sheet copper, for a lamp	Lautard, Guy	TMBR#3:206
        A "thin piece" collet	Lautard, Guy	TMBR#2:129
        A Luxo lamp base with rotating electrical pick-up	Lautard, Guy	TMBR#3:26
        A Toolmaker's Block	Lautard, Guy	TMBR#2:19
        A background shading punch	Lautard, Guy	TMBR#3:247
        A backplate fitting idea for 3-jaw chucks	Lautard, Guy	TMBR#3:65
        A block to produce 3 common angles from a sine bar	Lautard, Guy	TMBR#3:98
        A boring bar for reboring large cylinders	Lautard, Guy	TMBR#2:96
        A centerfinder	Lautard, Guy	TMBR#2:104
        A cheap master gage to test taper shanks against	Lautard, Guy	TMBR#2:92
        A collet chuck system for your lathe	Lautard, Guy	TMBR#3:11, TMBR#2:39
        A copper pipe soldering trick	Lautard, Guy	TMBR#2:150
        A deluxe overhaul for keyless chucks	Lautard, Guy	TMBR#3:119
        A dowel puller	Lautard, Guy	TMBR#1:67
        A fixture for accurate taper turning with the topslide	Lautard, Guy	TMBR#3:16
        A fixture for rounding the ends of small parts	Lautard, Guy	TMBR#2:107
        A fixture to guide the piercing saw	Lautard, Guy	TMBR#3:240
        A flexible pusher for the milling vise	Lautard, Guy	TMBR#3:70
        A foot powered piercing saw	Lautard, Guy	TMBR#3:240
        A gagemaker's square	Lautard, Guy	TMBR#2:64
        A handy deburring tool made from a file	Lautard, Guy	TMBR#3:72
        A handy decimal equivalent chart	Lautard, Guy	TMBR#2:162
        A handy lathe tool tray	Lautard, Guy	TMBR#2:132
        A hanger for shop drawings	Lautard, Guy	TMBR#2:145
        A hanging wire version	Lautard, Guy	HTIM:5
        A hole location device for clockmakers	Lautard, Guy	TMBR#2:22
        A jar opener	Lautard, Guy	TMBR#2:143
        A knocking block	Lautard, Guy	TMBR#2:112
        A lamp made from brass fittings	Lautard, Guy	TMBR#3:206
        A lathe center turned in place	Lautard, Guy	TMBR#3:108
        A lathe mandrel hand crank	Lautard, Guy	TMBR#2:112
        A lathe tracing attachment	Lautard, Guy	TMBR#2:108
        A low cost surface plate	Lautard, Guy	TMBR#1:8
        A low cost table saw	Lautard, Guy	TMBR#3:190
        A master gage for Morse taper shanks	Lautard, Guy	TMBR#1:17
        A means of holding flat work in the vise	Lautard, Guy	TMBR#2:15
        A mini 4-jaw chuck	Lautard, Guy	TMBR#3:60
        A model vise	Lautard, Guy	TMBR#3:206-207
        A multi-diameter edge finder adaptor	Lautard, Guy	TMBR#2:128
        A napkin holder	Lautard, Guy	HTIM:49
        A nice clean-looking clean drawer pull	Lautard, Guy	HTIM:32
        A quick detach sine fixture for your milling vise	Lautard, Guy	TMBR#2:80
        A reference straightedge from plate glass	Lautard, Guy	TMBR#2:12
        A replica Lunkenheimer whistle	Lautard, Guy	TMBR#2:134
        A rust preventative from Stockholm tar etc.	Lautard, Guy	TMBR#3:77
        A set-over tailstock center for taper turning	Lautard, Guy	TMBR#2:89-92; TMBR#3:13
        A severe first test for squareness	Lautard, Guy	TMBR#2:14-15
        A shop made centerpunch	Lautard, Guy	TMBR#3:105
        A shop made surface grinder	Lautard, Guy	TMBR#2:59, 60
        A shop-made bender	Lautard, Guy	TMBR#3:56
        A shop-made cylindrical square	Lautard, Guy	TMBR#2:18
        A shop-made hacksaw	Lautard, Guy	TMBR#2:100
        A simple stamping fixture	Lautard, Guy	TMBR#2:109
        A slitting saw arbor	Lautard, Guy	TMBR#1:62; TMBR#2:128
        A spillproof cutting oil bottle	Lautard, Guy	TMBR#3:227
        A tailstock die holder	Lautard, Guy	TMBR#2:103
        A tap starting block	Lautard, Guy	TMBR#3:74
        A tip on using calipers	Lautard, Guy	TMBR#3:106
        A tool for co-ordinate layout work in the mill	Lautard, Guy	TMBR#2:127
        A true square	Lautard, Guy	TMBR#2:18
        A tube flaring tool	Lautard, Guy	TMBR#2:126
        A use for worn or broken hacksaw blades	Lautard, Guy	TMBR#2:131
        A vise accessory for holding flat work	Lautard, Guy	TMBR#2:97
        A wax wire extruder	Lautard, Guy	TMBR#3:76
        A wire hoop bender	Lautard, Guy	TMBR#3:56
        A wood lathe	Lautard, Guy	TMBR#1:196
        Advice on getting ahead	Lautard, Guy	TMBR#1:181
        Alternator test bench	Lautard, Guy	TMBR#3:109
        Aluminum made 3000 years ago in China	Lautard, Guy	TMBR#3:210
        Aluminum soldering	Lautard, Guy	TMBR#1:103; HTIM:48
        Aluminum welding rod	Lautard, Guy	TMBR#2:122
        An adjustable workstop for the lathe spindle hole	Lautard, Guy	TMBR#3:75
        An aid to setting up work on a faceplate	Lautard, Guy	TMBR#3:20
        An attractive etched finish for aluminum	Lautard, Guy	TMBR#2:115
        An easy way to make a hex socket screw	Lautard, Guy	TMBR#2:95
        An old timer remembers flat belts & firm joint calipers	Lautard, Guy	TMBR#3:21
        An oversize paper clip	Lautard, Guy	TMBR#3:54-55
        An ultra sensitive dial indicator base	Lautard, Guy	TMBR#2:83
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
        Anodizing aluminum	Lautard, Guy	TMBR#1:197
        Anti-fatigue mats	Lautard, Guy	TMBR#1:176
        Anti-seize compound used in a milling job	Lautard, Guy	HTIM:21
        ApplePly	Lautard, Guy	TMBR#3:192
        Approximations of pi	Lautard, Guy	TMBR#3:10
        Art and design sense	Lautard, Guy	TMBR#3:242
        Aushalser - a German made pipe-T pulling tool	Lautard, Guy	TMBR#3:81
        Avoiding tap breakage	Lautard, Guy	TMBR#3:151
        BB introduced	Lautard, Guy	TMBR#3:4
        Back scratcher - the world's best	Lautard, Guy	TMBR#3:225
        Balancing grinding wheel flanges	Lautard, Guy	TMBR#2:114
        Ball ended centers from Ford pushrods	Lautard, Guy	TMBR#3:13
        Ball turning techniques	Lautard, Guy	TMBR#1:72-79; TMBR#3:24, 174
        Ballizing holes for high finish & high precision	Lautard, Guy	TMBR#2:132
        Baltic Birch plywood	Lautard, Guy	TMBR#3:192
        Bandsaw blade speeds	Lautard, Guy	HTIM:42; TMBR#3:184
        Basketball inflator needle for tap cutting removal	Lautard, Guy	TMBR#3:71
        Bead blasting & other ways of finishing aluminum	Lautard, Guy	HTIM:23
        Beam compass: Grinding the flat on the beam	Lautard, Guy	TMBR#3:122-126
        Behavior of slitting saws, etc.	Lautard, Guy	TMBR#1:55-61
        Benelex	Lautard, Guy	TMBR#3:191
        Benelex - a harder version of Medite	Lautard, Guy	TMBR#3:175
        Bengalis' (Tony) writings in Sport Aviation	Lautard, Guy	TMBR#3:56
        Bernzomatic torches etc.	Lautard, Guy	TMBR#1:51
        Between-centers boring bars	Lautard, Guy	TMBR#2:94
        Bevel protractor used to set up a reamer for stoning	Lautard, Guy	TMBR#3:159
        Bill's big firm joint calipers	Lautard, Guy	TMBR#3:20
        Bill's donkey engine & spar tree logging blocks	Lautard, Guy	TMBR#3:36-47
        Black or pink granite?	Lautard, Guy	TMBR#3:106
        Blade guides for bandsaw blades	Lautard, Guy	HTIM:42
        Blank end taper shank arbors	Lautard, Guy	TMBR#2:89
        Blueing cutters while hand filing the reliefs	Lautard, Guy	TMBR#3:110
        Blueing of steel with muriatic acid	Lautard, Guy	TMBR#3:175
        Blueing steel	Lautard, Guy	TMBR#1:34, 171,
        Blueing steel: Black velvet blue job for gun parts	Lautard, Guy	TMBR#3:137
        Blueing steel:Electroless nickel plating	Lautard, Guy	TMBR#3:139
        Blueing steel:Etching off a too high polish with nitric acid	Lautard, Guy	TMBR#3:138
        Blueing steel:How to do a durable black "Parkerized" finish	Lautard, Guy	TMBR#3:139
        Blueing steel:Numrich 44-40 gun blue	Lautard, Guy	TMBR#3:138
        Blueing steel:Swedish recipe	Lautard, Guy	TMBR#3:103
        Blueing steel:with Chem-Tech cutting fluid	Lautard, Guy	TMBR#3:175
        Blueing steel:with muriatic acid	Lautard, Guy	TMBR#3:175
        Boat repairs	Lautard, Guy	TMBR#3:208
        Bob Eaton's Civil War cannon	Lautard, Guy	TMBR#3:116
        Book citation: Accurate Tool Work	Lautard, Guy	TMBR#3:99
        Book citation: Cache Lake Country	Lautard, Guy	TMBR#3:2
        Book citation: Engineer to Win	Lautard, Guy	TMBR#3:218
        Book citation: Foundations of Mechanical Accuracy	Lautard, Guy	TMBR#2:67
        Book citation: Fundamentals of Dimensional Metrology	Lautard, Guy	TMBR#3:2 18
        Book citation: Gunsmithing Tips & Projects	Lautard, Guy	TMBR#3:153
        Book citation: Ron Fournier's book on sheet metal work	Lautard, Guy	TMBR#2:111
        Book citation: The Illustrated Reference of Cartridge Dimensions	Lautard, Guy	TMBR#3:166
        Book citation: The Masochist's Bedside Reader	Lautard, Guy	TMBR#3:227
        Book citation: The Muzzle Loading Caplock Rifle	Lautard, Guy	TMBR#3:166
        Book citation: Zen and the Art of Motorcycle Maintenance	Lautard, Guy	TMBR#3:230
        Book citation: several other shooting oriented books cited	Lautard, Guy	TMBR#3:217
        Box making - some ideas	Lautard, Guy	TMBR#1:123
        Boxes for small precision tools	Lautard, Guy	TMBR#3:91; TMBR#2:10, 15
        Boxes: Corner caps	Lautard, Guy	TMBR#3:197
        Boxes: Decorative finishing for boxes	Lautard, Guy	TMBR#3:199
        Boxes: Handles	Lautard, Guy	TMBR#3:197
        Boxes: Hinges	Lautard, Guy	TMBR#3:196, 199, 200
        Boxes: Knotted rope &/or deadeyes as handles	Lautard, Guy	TMBR#3:197
        Boxes: Latches	Lautard, Guy	TMBR#3:196
        Boxes: Plywood splinters	Lautard, Guy	TMBR#3:197
        Boxes: Solid wood boxes	Lautard, Guy	TMBR#3:198
        Boxes: Storage trays for parallels and similar	Lautard, Guy	TMBR#3:198
        Boxes: cast bronze chest handles	Lautard, Guy	TMBR#3:195
        Brass Kaleidoscope	Lautard, Guy	TMBR#2:140
        Brass compression nuts for file handle ferrules	Lautard, Guy	TMBR#3:107
        Brass filled characters in steel	Lautard, Guy	TMBR#1:137
        Brass napkin rings	Lautard, Guy	TMBR#1:143; HTIM:49
        Breaking out a new coil of music wire	Lautard, Guy	TMBR#1:137
        Brief business advice	Lautard, Guy	TMBR#3:2 16
        Brightening work before tempering	Lautard, Guy	TMBR#1:60
        Broken tap removal from aluminum	Lautard, Guy	TMBR#3:78
        Brownells. Inc., Gunsmiths "Kinks" books	Lautard, Guy	TMBR#1:6
        Brunzeals plywood	Lautard, Guy	TMBR#3:192
        Bullet mold making	Lautard, Guy	TMBR#1:118
        Business cards as advertising	Lautard, Guy	TMBR#3:209
        Button head socket cap screws	Lautard, Guy	HTIM:2
        Buying a used Gravermeister	Lautard, Guy	TMBR#3:243
        CRS - what is it?	Lautard, Guy	TMBR#1:23
        Calculating an angle	Lautard, Guy	TMBR#2:72
        Calculating bandsaw blade speeds	Lautard, Guy	TMBR#3:185
        Calculating numbers for cutting a ball	Lautard, Guy	TMBR#1:77; TMBR#3:24
        Calculating top slide infeed for screwcutting	Lautard, Guy	TMBR#2:112; TMBR#3:112
        Caliper or floating arm knurling tool	Lautard, Guy	TMBR#1:54
        Candle wax, blade breakage, sawing to a layout line	Lautard, Guy	TMBR#3:241
        Canjar triggers	Lautard, Guy	TMBR#3:153
        Capping piece of solid wood + plywood top	Lautard, Guy	TMBR#3: 194, 197-198
        Car badges, belt buckles, broochs	Lautard, Guy	TMBR#3:239
        Casehardening :Depth and distribution of parts in the pack box	Lautard, Guy	TMBR#2:183
        Casehardening methods, as continued	Lautard, Guy	TMBR#3:6-10
        Casehardening methods, as detailed in The Bullseye Mixture,	Lautard, Guy	TMBR#2:163-197
        Casehardening: - charring bone meal	Lautard, Guy	TMBR#3:8
        Casehardening: - washing bone meal	Lautard, Guy	TMBR#3:8
        Casehardening: A charcoal furnace	Lautard, Guy	TMBR#2:185-187
        Casehardening: Activators	Lautard, Guy	TMBR#2:194
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
        Casehardening: The secret powders: Barium carbonate	Lautard, Guy	TMBR#3:7
        Casehardening: The secret powders: Sodium carbonate (washing soda)	Lautard, Guy	TMBR#3:7
        Casehardening: Time at casehardening temp.	Lautard, Guy	TMBR#2:190-192
        Casehardening: Use of paper to consume excess oxygen	Lautard, Guy	TMBR#3:8
        Casehardening: Using lower temperatures	Lautard, Guy	TMBR#3:7
        Casehardening: Various quenching/heat treating scenarios	Lautard, Guy	TMBR#2:191
        Casehardening: Washing the charcoal	Lautard, Guy	TMBR#3:8
        Casehardening: What wrecked the stove	Lautard, Guy	TMBR#3:7
        Casehardening: Why/where used	Lautard, Guy	TMBR#2: 172-173
        Casehardening: air bubbles in the quench	Lautard, Guy	TMBR#2:191-192
        Casehardening: color casehardening	Lautard, Guy	TMBR#2:173
        Casehardening: quenching liquid	Lautard, Guy	TMBR#2:191-192
        Casehardening: the pack box	Lautard, Guy	TMBR#2:182
        Cast iron section for workholding	Lautard, Guy	TMBR#1:39
        Cast iron, source of high quality, for various	Lautard, Guy	TMBR#1:91; TMBR#3:79, 174
        Cast lead hammers for your shop	Lautard, Guy	TMBR#2:112
        Casting machine handles in epoxy	Lautard, Guy	TMBR#3:75
        Cautions re use of unapproved electrical devices	Lautard, Guy	TMBR#3:27
        Center punches, how to sharpen	Lautard, Guy	TMBR#1:21
        Centering a cutter over a shaft by eye	Lautard, Guy	TMBR#1:83
        Centering square/rectangular stock in the 4-jaw chuck	Lautard, Guy	TMBR#1:81
        Centrifuge type oil filter	Lautard, Guy	TMBR#1:197
        Chain drilling aided by accurate hole spacing	Lautard, Guy	TMBR#3:102
        Chain drilling to make a blind opening	Lautard, Guy	TMBR#2:125
        Chain making - some ideas	Lautard, Guy	TMBR#3:54
        Chalk on files	Lautard, Guy	TMBR#1:7
        Charcoal iron	Lautard, Guy	TMBR#2:11
        Checking a #2MT against standard specs	Lautard, Guy	TMBR#3:15
        Chinese tool steel	Lautard, Guy	TMBR#1:181
        Choice of files	Lautard, Guy	TMBR#1:7-8
        Choice of reamers	Lautard, Guy	TMBR#1:16
        Choosing & using a sensitive dial indicator	Lautard, Guy	TMBR#2:83
        Chuck backplate fitting procedures	Lautard, Guy	TMBR#3:63
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
        Citation: Mounting a DTI to a mill's vertical spindle	Lautard, Guy	HTIM:15
        Citation: SIC, a tiny steam engine	Lautard, Guy	TMBR#3:214
        Citation: Several articles re rifles/action building Citationd	Lautard, Guy	TMBR#3:167
        Citation: Slow speed attachment for a bandsaw	Lautard, Guy	HTIM:42
        Citation: making straightedges	Lautard, Guy	HTIM:48
        Clamping down a cylinder for machining	Lautard, Guy	TMBR#1:138
        Cleaning a granite surface plate	Lautard, Guy	HTIM:46; TMBR#3:204 & 224
        Cleaning clogged files	Lautard, Guy	TMBR#2:123
        Cleaning up a burred #2MT lathe tailstock	Lautard, Guy	TMBR#1:17
        Clearing tap cuttings	Lautard, Guy	TMBR#1:19
        Climb milling aluminum	Lautard, Guy	HTIM:14
        Coil springs for triggers	Lautard, Guy	TMBR#3:148
        Cold working of steel	Lautard, Guy	TMBR#1:180
        Cole Drill	Lautard, Guy	TMBR#3:18 (also inside back cover, in 2nd printing) 
        Collet chuck arrangement	Lautard, Guy	TMBR#2:39
        Compound Dividing	Lautard, Guy	TMBR#1:41
        Concrete & pipe work islands	Lautard, Guy	TMBR#3:27
        Copper coins as work protectors	Lautard, Guy	TMBR#3:236
        Copper fluid tanks for cars	Lautard, Guy	TMBR#3:80-81
        Copper setscrew pads	Lautard, Guy	TMBR#2:112
        Copper tube expander mandrel	Lautard, Guy	TMBR#2:129
        Copper vise jaw liners	Lautard, Guy	TMBR#2:122
        Copper wire setscrew pads	Lautard, Guy	TMBR#3:173
        Cork - where to buy sheets	Lautard, Guy	TMBR#2:119
        Correct depth to drill center holes	Lautard, Guy	TMBR#2:92
        Critical relationships between trigger & action parts	Lautard, Guy	TMBR#3:145
        Curing slipping of flat belt drives	Lautard, Guy	TMBR#3:59-60
        Cutter blocks & shop made cutters	Lautard, Guy	TMBR#1:101; TMBR#3:110
        Cutting a coin slot	Lautard, Guy	TMBR#2:131
        Cutting a large radius fillet	Lautard, Guy	HTIM:14-15
        Cutting metric threads on an "English" lathe	Lautard, Guy	TMBR#3:114
        Cutting multiple start threads	Lautard, Guy	TMBR#2:87
        Cutting oil - SC40	Lautard, Guy	TMBR#1:7
        Cutting plate cams to a layout line freehand	Lautard, Guy	TMBR#2:108
        Cutting plywood panels down to size safely	Lautard, Guy	TMBR#3:189,190
        Cutting speeds (a useful chart)	Lautard, Guy	TMBR#1:9
        Cutting the pieces	Lautard, Guy	TMBR#3:192
        Cutting threads in the lathe	Lautard, Guy	TMBR#3:102
        Cutting threads up to a shoulder	Lautard, Guy	TMBR#3:114
        D-bit	Lautard, Guy	TMBR#1:52
        D-bit Toolmaker's type	Lautard, Guy	TMBR#1:53
        D-bit from dowel pins etc.	Lautard, Guy	TMBR#3:66
        DC motor and speed controller for bandsaw speed	Lautard, Guy	TMBR#3:184
        DC motor/speed controller for bandsaw speed	Lautard, Guy	TMBR#3:184; HTIM:42
        De-horning a Myford driving dog	Lautard, Guy	TMBR#3:14
        Deciding upon box size	Lautard, Guy	TMBR#3:191
        Deepening a pattern layout with an electric engraver	Lautard, Guy	TMBR#3:240
        Dental abrasive strips and miniature tooth brushes	Lautard, Guy	TMBR#3:177
        Dental tools for removal of t'paper from tapped holes	Lautard, Guy	TMBR#3:177
        Depth gages	Lautard, Guy	TMBR#1:33; TMBR#3:173
        Designing & deciphering verniers	Lautard, Guy	TMBR#1:121
        Designing & fitting (split cotters)	Lautard, Guy	TMBR#1:92-96
        Dial indicator for measuring lathe saddle movement	Lautard, Guy	HTIM:8
        Diamantine powder	Lautard, Guy	TMBR#2:120 & 122
        Differential Dividing	Lautard, Guy	TMBR#1:41
        Dimensional tolerance of aluminum bar stock	Lautard, Guy	HTIM:12
        Direct Dividing	Lautard, Guy	TMBR#1:40
        Dismantling an edge finder (not in 1st printing)	Lautard, Guy	TMBR#3:139
        Dividing 1/4 degree vernier	Lautard, Guy	TMBR#2:8
        Dividing On a geared Rotary Table	Lautard, Guy	TMBR#1:41
        Dividing decent	Lautard, Guy	TMBR#2:8
        Dividing from Bandsaw blades	Lautard, Guy	TMBR#1:43-44; TMBR#2:198
        Dividing head a beefed up version	Lautard, Guy	TMBR#2:3
        Dividing with 15/16 hole vernier	Lautard, Guy	TMBR#1:42
        Division plates from bandsaw blades	Lautard, Guy	TMBR#2:3
        Doing work for university profs	Lautard, Guy	TMBR#3:209
        Don't drill into your lathe spindle taper	Lautard, Guy	TMBR#3:109
        Don't run a chuck up to speed without a workpiece in it	Lautard, Guy	TMBR#3:62
        Double pulley for dual motor drive	Lautard, Guy	TMBR#3:58
        Double-ball clamping levers	Lautard, Guy	TMBR#1:85
        Dovetail jigs, marking-out	Lautard, Guy	TMBR#3:194
        Dovetail, splines	Lautard, Guy	TMBR#3:193
        Dowel pins	Lautard, Guy	TMBR#2:103;
        Drafting, drawing: What does "2 off" mean?	Lautard, Guy	HTIM:47
        Drawer handles from bottle caps	Lautard, Guy	TMBR#3:237
        Drawfiling	Lautard, Guy	TMBR#1:5, 8,
        Drawfiling reliefs on shop-made taps	Lautard, Guy	TMBR#3:23-24
        Drawings for a graduated lathe leadscrew handwheel	Lautard, Guy	TMBR#1:71
        Drawings for a machinist's wooden tool chest	Lautard, Guy	TMBR#1:131
        Drawings for simple shop made pantograph	Lautard, Guy	TMBR#3:250
        Dressing abrasive stones flat	Lautard, Guy	TMBR#2:119
        Dressing an abrasive wheel	Lautard, Guy	TMBR#2:65
        Drill depth stop collar for a center drill	Lautard, Guy	TMBR#3:13, 14
        Drill modified for drilling plastic	Lautard, Guy	TMBR#3:66
        Drill press as a tapping machine	Lautard, Guy	TMBR#3:173
        Drill reamer	Lautard, Guy	TMBR#3:66
        Drill rod - is it "round"?	Lautard, Guy	TMBR#2:70
        Drill sharpening jigs	Lautard, Guy	TMBR#1:26, 205; TMBR#2:147; TMBR#3:257-8
        Drilling a 0.018" dia. hole	Lautard, Guy	TMBR#2:54
        Drilling a division plate	Lautard, Guy	TMBR#2:7
        Drilling a shaft from both ends	Lautard, Guy	TMBR#2:96
        Drilling a shaft in the mill	Lautard, Guy	TMBR#2:96
        Drilling a truck frame	Lautard, Guy	TMBR#3:19
        Drilling oversize holes	Lautard, Guy	TMBR#1:155
        Drilling plywood without splintering	Lautard, Guy	TMBR#3:188
        Drilling to an exact depth	Lautard, Guy	TMBR#1:20, 70,
        Drilling to size for reaming	Lautard, Guy	TMBR#1:16
        Drilling well centered holes in the ends of a bar	Lautard, Guy	TMBR#2:95
        Dual drive belt advice	Lautard, Guy	TMBR#3:58
        Dual set screws for V-belt pulleys, etc.	Lautard, Guy	TMBR#1:44; TMBR#3:175
        Dust control	Lautard, Guy	HTIM:44; TMBR#3:203
        Dust control from Medite	Lautard, Guy	HTIM:1
        Dust control, as a health hazard	Lautard, Guy	TMBR#3:203-204
        Ear cleaning syringe is handy	Lautard, Guy	TMBR#3:237
        Easy rolling shop trolleys	Lautard, Guy	HTIM:46
        Edge finding: How to make a wiggler	Lautard, Guy	TMBR#3:92
        Edge finding: Purpose of the bent shaft in a wiggler outfit	Lautard, Guy	TMBR#3:93
        Edge finding: Spud + boring head	Lautard, Guy	TMBR#3:96
        Edge finding: Spuds, bugs and wigglers	Lautard, Guy	TMBR#3:92-96
        Edge finding: The "Sticky Pin"	Lautard, Guy	TMBR#3:96
        Edge finding: What makes a wiggler work?	Lautard, Guy	TMBR#3:92-93
        Effects of errors in squareness	Lautard, Guy	TMBR#2:19
        Electrical extension cord caddy, WARNING: may be dangerous	Lautard, Guy	TMBR#3:33-34
        Emery sticks	Lautard, Guy	TMBR#2:14
        Engraving a feedscrew dial	Lautard, Guy	TMBR#1:43, 48-49
        Engraving cutters	Lautard, Guy	TMBR#2:36
        Equation defining the points on a circle	Lautard, Guy	TMBR#1:73
        Errata note re 30/40 Krag chamber in 30/06 chamber	Lautard, Guy	TMBR#2:126
        Errors in measuring, effect of	Lautard, Guy	TMBR#1:11
        Etching	Lautard, Guy	TMBR#1:136
        Etching off a too-high polish with nitric acid	Lautard, Guy	TMBR#3:138
        Etching on metal	Lautard, Guy	TMBR#3:244 & 254
        Exact-T-Guide cutting aid for sheet goods	Lautard, Guy	TMBR#3:190
        Extension for a small drill chuck	Lautard, Guy	TMBR#2:104
        Extruding lead wire	Lautard, Guy	TMBR#3:77
        FWW article on dovetailing cited	Lautard, Guy	TMBR#3:193-194
        FWW article on plywood referenced	Lautard, Guy	TMBR#3:191
        Farm Show Magazine	Lautard, Guy	TMBR#3:109
        Farm tractor carb repairs	Lautard, Guy	TMBR#3:217
        Fast removal of tap cuttings	Lautard, Guy	TMBR#2:125
        Fast way to dial in the head of a vertical mill	Lautard, Guy	HTIM:33; TMBR#3:84
        Federal File Co.	Lautard, Guy	TMBR#3:256
        Fenton, Bill	Lautard, Guy	TMBR#1:4, 182, 191; TMBR#2:22
        Figuring the tapping size hole for any thread	Lautard, Guy	TMBR#1:19
        File brushes	Lautard, Guy	TMBR#1:6
        File cleaning on wire wheel brush	Lautard, Guy	TMBR#3:108
        File handle ferrules made from compression nuts	Lautard, Guy	TMBR#3:107
        File handles that fit your hand	Lautard, Guy	TMBR#3:107
        File selection	Lautard, Guy	TMBR#3:71
        Filing buttons	Lautard, Guy	TMBR#2:106
        Filing for 'flat" and "finish"	Lautard, Guy	TMBR#3:15 1
        Filing in the lathe	Lautard, Guy	TMBR#1:7
        Filing off that last half thou	Lautard, Guy	TMBR#3:139
        Filing technique	Lautard, Guy	TMBR#1:7-8
        Filling voids in plywood	Lautard, Guy	TMBR#3:188
        Finding lost tools	Lautard, Guy	TMBR#3:73
        Fine toothed hacksaw blades	Lautard, Guy	TMBR#3:256
        Finger joints	Lautard, Guy	TMBR#3:194
        Finger plate	Lautard, Guy	TMBR#1:88-89, TMBR#3:79
        Finishing aluminum with a flap wheel	Lautard, Guy	TMBR#2:115
        Firewall grommet-making for aircraft	Lautard, Guy	TMBR#3:56
        Fitting washers - which side up?	Lautard, Guy	HTIM:31
        Flower arranging rod as a welding rod	Lautard, Guy	TMBR#2:124
        Flute spacing: uniform or non-uniform	Lautard, Guy	TMBR#1:101
        Flycutter made from a 2-flute end mill	Lautard, Guy	TMBR#3:12
        Fruit acid - effect on tools	Lautard, Guy	TMBR#1:62
        Fused glass car badges	Lautard, Guy	TMBR#3:246
        Galvanized sheet metal	Lautard, Guy	TMBR#3:103
        Gear oil, what is it?	Lautard, Guy	TMBR#2:115
        Gearcutting	Lautard, Guy	TMBR#2:199
        General Model 490 Bandsaw	Lautard, Guy	TMBR#3:184
        Geometry of a radius tangent to a line and a circle	Lautard, Guy	HTIM:16
        Getting a drill chuck off and on its arbor	Lautard, Guy	TMBR#3:117
        Getting a fair return for your work	Lautard, Guy	TMBR#1:179
        Getting a nice finish on screw threads	Lautard, Guy	TMBR#2:112
        Gib key - triangular	Lautard, Guy	TMBR#2:68
        Gibraltar toolpost	Lautard, Guy	TMBR#3:14
        Glendo Accu-finisher	Lautard, Guy	TMBR#3:111
        Gloves for use with a sandblast cabinet	Lautard, Guy	TMBR#3:131,134
        Glue turning black in contact with iron	Lautard, Guy	TMBR#3:195
        Glue, excess - dealing with	Lautard, Guy	TMBR#3:195
        Glued vs. dry vs. rabbeted joints etc.	Lautard, Guy	TMBR#3:192
        Good counter sinks	Lautard, Guy	TMBR#2:104
        Good old unsalted pork lard	Lautard, Guy	TMBR#2:116
        Good steel for making punches, etc.	Lautard, Guy	TMBR#3:104, 237
        Goodies at rock bottom prices from the right sources	Lautard, Guy	TMBR#3:104
        Grasping groove cutter	Lautard, Guy	TMBR#1:86
        Gravity operated shut-off button for mill-drill	Lautard, Guy	TMBR#3:25
        Habilus files	Lautard, Guy	TMBR#3:241
        Hacksaw	Lautard, Guy	TMBR#2:101-102
        Hanchett knife grinder; plywood lathe knives	Lautard, Guy	TMBR#1:117
        Hand chasing a thread	Lautard, Guy	TMBR#1:191
        Hand stamps don't "shoot straight"	Lautard, Guy	TMBR#2:110
        Hand stamps for uniform marking	Lautard, Guy	TMBR#2:24
        Handling a fine square	Lautard, Guy	TMBR#2:64
        Hanging plate shelf for your lathe or milling machine	Lautard, Guy	HTIM:6
        Hardened vs. cast iron heads for combination sets	Lautard, Guy	TMBR#3:106
        Hardened vs. cast iron heads for combination squares	Lautard, Guy	TMBR#3:106
        Harken yacht fittings	Lautard, Guy	TMBR#3:52
        Harmonographs	Lautard, Guy	TMBR#1:142
        Heat required to break a Loctite bond	Lautard, Guy	TMBR#1:115
        Heat treating & hardening trigger & sear parts	Lautard, Guy	TMBR#3:149
        Heat treating & hardening trigger/sear parts	Lautard, Guy	TMBR#3:149
        Heat treating a small drill rod cutter	Lautard, Guy	TMBR#1:45
        Heavy aluminum vise jaws	Lautard, Guy	TMBR#3:76
        Heavy duty scraper	Lautard, Guy	TMBR#3:237
        Heavy web dive belting as vise jaw liners	Lautard, Guy	TMBR#3:69
        Height gage from an engine valve	Lautard, Guy	TMBR#3:237
        Henteleffs #9, a gun cleaning solvent recipe	Lautard, Guy	TMBR#3:168
        Holding some odd shaped parts in the mill vise	Lautard, Guy	TMBR#3:71
        Holding thin workpieces in the lathe chuck	Lautard, Guy	TMBR#1:69
        Holding threaded items in a coil of wire	Lautard, Guy	TMBR#3:218
        Honing lathe tools	Lautard, Guy	TMBR#2:122
        Honing lubes	Lautard, Guy	TMBR#2:118-119; TMBR#3:165
        How calipers were made, & details of the hinge joint	Lautard, Guy	TMBR#3:22
        How not to lose springs	Lautard, Guy	TMBR#3:141
        How not to remove a milling machine arbor	Lautard, Guy	TMBR#3:226
        How to bolt down a bench lathe	Lautard, Guy	HTIM:34
        How to dress up hand stamped markings	Lautard, Guy	TMBR#1:86; TMBR#2:110
        How to machine a gib strip	Lautard, Guy	TMBR#3:67
        How to make a dovetail grip dial indicator clamp	Lautard, Guy	TMBR#2:84
        How to make a master reference square	Lautard, Guy	TMBR#2:10
        How to make a protective case	Lautard, Guy	TMBR#2:10, 15
        How to make a square hole sleeve	Lautard, Guy	TMBR#2:88
        How to quench a circular die	Lautard, Guy	TMBR#1:120
        How to restore age-hardened pencil erasers	Lautard, Guy	HTIM:37
        How to set up grinding wheels	Lautard, Guy	TMBR#2:114
        How to super-level your lathe	Lautard, Guy	HTIM:34
        How to tap a drawbar hole in a taper shank	Lautard, Guy	TMBR#2:92
        How to use an edgefinder	Lautard, Guy	TMBR#3:93-94
        Hydraulic & rubberdraulic locking of a ring on a dial	Lautard, Guy	TMBR#1:7TMBR#1: TMBR#2:123
        Ideas for master vernier protractor wanted	Lautard, Guy	TMBR#2:85
        Imitation ivory	Lautard, Guy	TMBR#1:132
        In Ireland - making architectural stuff	Lautard, Guy	TMBR#3:209
        In my shop	Lautard, Guy	HTIM:51
        Incra-Jigs	Lautard, Guy	TMBR#3:194
        Indexing holes in the rim of a chuck backplate	Lautard, Guy	TMBR#3:65
        Indicators and edge finders	Lautard, Guy	TMBR#3:83-97
        Info for camera buffs	Lautard, Guy	TMBR#1:141-142
        Is a Dial indicator an accurate measuring device?	Lautard, Guy	HTIM:47
        Jacobs spindle nose chuck	Lautard, Guy	TMBR#3:12
        Jaw protectors	Lautard, Guy	TMBR#3:68-69
        Keeping taps square	Lautard, Guy	TMBR#1:19
        Kerosene burning blowlamp	Lautard, Guy	TMBR#2:47; TMBR#3:102
        Killing chatter-	Lautard, Guy	TMBR#1:16
        Knorrostol rust remover/metal polish	Lautard, Guy	TMBR#3:72
        Knurling	Lautard, Guy	TMBR#1:5
        Knurling flat surfaces	Lautard, Guy	TMBR#3:74
        Knurling technique	Lautard, Guy	TMBR#1:60-61; TMBR#2:100
        Lacquered brass	Lautard, Guy	TMBR#1:143
        Lamp in the form of a clamp-on ball handle	Lautard, Guy	TMBR#3:205
        Lamp made from brass fittings	Lautard, Guy	TMBR#3:206
        Lapping an edgefinder , correct	Lautard, Guy	TMBR#3 2nd printing:94, 139. & 251
        Lapping an edgefinder, incorrect	Lautard, Guy	TMBR#3 1st printing:94, 139. & 251
        Lapping with Tripoli	Lautard, Guy	HTIM:47
        Lathe cleaning	Lautard, Guy	TMBR#1:175
        Lathe made in a Japanese POW camp	Lautard, Guy	TMBR#1:156
        Lautard's Octopus	Lautard, Guy	TMBR#2:v
        Lautard's manoeuvre	Lautard, Guy	TMBR#2:160
        Laying out a tilted circumferential notch	Lautard, Guy	HTIM:10
        Lazy susan bearings	Lautard, Guy	HTIM:2
        Lid/box match-up	Lautard, Guy	TMBR#3:192
        Lie-Nielsen Toolworks Scraping planes	Lautard, Guy	TMBR#3:195
        Lie-Nielsen Toolworks edge trimming block plane	Lautard, Guy	TMBR#3:194-195
        Light duty dividing head from BHJ, by Eliot Isaacs	Lautard, Guy	TMBR#2:1
        Light duty height-adjustable stands for...?	Lautard, Guy	TMBR#3:211
        Linoleum - a superior vise jaw lining material	Lautard, Guy	HTIM:38
        Locating buttons for master division plate	Lautard, Guy	TMBR#2:3
        Loctite	Lautard, Guy	TMBR#1:96
        Long transfer punches	Lautard, Guy	TMBR#3:175
        Lost wax casting for multiple parts	Lautard, Guy	TMBR#3:116
        Low cost master type for an engraving machine	Lautard, Guy	TMBR#3:252
        Lube for tube expanding etc.	Lautard, Guy	TMBR#2:129
        Lubes for tapping various materials	Lautard, Guy	TMBR#1:18
        Lubricating milling machine spindles	Lautard, Guy	TMBR#3:101
        Lubrication and grinding machines	Lautard, Guy	TMBR#2:161
        Lumiweld	Lautard, Guy	TMBR#2:123
        MIG and TIG welding	Lautard, Guy	TMBR#3:255-256
        Machine stands	Lautard, Guy	TMBR#3:186-190
        Machine tool heights for comfort	Lautard, Guy	TMBR#1:133; TMBR#3:187
        Machining a rubber roll	Lautard, Guy	TMBR#2:152
        Machining a spindle from its I.D.	Lautard, Guy	TMBR#2:39
        Made by soldering tubing to plate material	Lautard, Guy	TMBR#3:200
        Made flat by scraping	Lautard, Guy	TMBR#2:67
        Magnet as milling vise stop	Lautard, Guy	TMBR#3:58
        Magnetic goodies	Lautard, Guy	TMBR#3:68
        Magnetic indicator on dial indicator back	Lautard, Guy	TMBR#3:79
        Magnetic vise jaw liners	Lautard, Guy	TMBR#3:68
        Magnetic welding positioners	Lautard, Guy	TMBR#3:255
        Making & checking a flat master square	Lautard, Guy	TMBR#2:16, 17
        Making a Co-Axial indicator	Lautard, Guy	TMBR#3:83
        Making a M22 Springfield magazine clip (story)	Lautard, Guy	TMBR#2:110
        Making a good center, & drilling a hole there	Lautard, Guy	TMBR#3:104/105
        Making a set of angle blocks	Lautard, Guy	TMBR#2:81
        Making a sheet metal box	Lautard, Guy	HTIM:31
        Making a small pantograph engraving machine	Lautard, Guy	TMBR#2:24
        Making a solenoid core	Lautard, Guy	TMBR#2:129
        Making a special countersink	Lautard, Guy	TMBR#2:53
        Making a strop	Lautard, Guy	TMBR#2:120
        Making a wooden drive pulley	Lautard, Guy	TMBR#3:58
        Making an antique aircraft	Lautard, Guy	TMBR#3:208
        Making an engraving cutter	Lautard, Guy	TMBR#1:45-46; TMBR#2:36
        Making fishing reels	Lautard, Guy	TMBR#2:138-139
        Making gold refining equipment	Lautard, Guy	TMBR#3:208
        Making screwed fittings come up tight where wanted	Lautard, Guy	TMBR#3:82
        Making small, fine-quality aluminum castings	Lautard, Guy	TMBR#2:149, (202 after 1st printing); TMBR#3:129
        Making underwater housings for video cameras	Lautard, Guy	TMBR#3:215
        Making weatherproof work lights	Lautard, Guy	TMBR#3:210
        Making welded steel boxes	Lautard, Guy	TMBR#1:187
        Making your own chambering reamers	Lautard, Guy	TMBR#2:198
        Making/using a spindle nose duplicate	Lautard, Guy	TMBR#3:63
        Master type from Green Instrument Co.	Lautard, Guy	TMBR#2:25
        Master type racks	Lautard, Guy	TMBR#2:34
        Match drilling holes for pillars	Lautard, Guy	HTIM:4
        Material choice	Lautard, Guy	TMBR#3:19 1
        Materials/Scrounging	Lautard, Guy	TMBR#1:3
        McDuffie Drive	Lautard, Guy	TMBR#2:41
        Measuring an angle with a sine bar	Lautard, Guy	TMBR#3:98
        Measuring hole size with a rod	Lautard, Guy	TMBR#1:10
        Measuring hole size with taper leaf gages	Lautard, Guy	TMBR#1:10
        Measuring lathe saddle movement with	Lautard, Guy	HTIM:8
        Medite	Lautard, Guy	HTIM:1-3
        Medite, finishing	Lautard, Guy	HTIM:1-2; TMBR#3:190
        Metal polish	Lautard, Guy	TMBR#1:171
        Method for accurate setting of taper turning attachment	Lautard, Guy	TMBR#3:15
        Military triggers	Lautard, Guy	TMBR#3:143
        Milling a radius with a ball end mill	Lautard, Guy	HTIM:7-8
        Milling machine safety	Lautard, Guy	TMBR#3:91,84 & HTIM:33
        Milling spindles & overhead gear	Lautard, Guy	TMBR#2:37, 62-63
        Milling spindles, Lautard's manoeuvre	Lautard, Guy	TMBR#2:160
        Milling spindles, Osborne's manoeuvre	Lautard, Guy	TMBR#2:159
        Milling spindles, Overhead gear	Lautard, Guy	TMBR#2:40-46
        Milling spindles, Quill-Mate	Lautard, Guy	HTIM:33
        Milling spindles, bearings for	Lautard, Guy	TMBR#2:37; 59
        Milling spindles, for clockmaking	Lautard, Guy	TMBR#2:37
        Milling spindles, mounting one	Lautard, Guy	TMBR#2:37
        Milling spindles, other refinements	Lautard, Guy	TMBR#2:37
        Milling spindles, speeds for	Lautard, Guy	TMBR#2:37
        Milling tapers tangent to 2 circles	Lautard, Guy	TMBR#2:73
        Mitered and splined	Lautard, Guy	TMBR#3:193
        Mixing up replacement parts for drill chucks	Lautard, Guy	TMBR#3:118
        Model i.c. engines	Lautard, Guy	TMBR#1:144
        Modified for drilling plastic	Lautard, Guy	TMBR#3:66
        Modifying files for special uses	Lautard, Guy	TMBR#1:116
        Mods to a dial indicator base	Lautard, Guy	TMBR#3:79
        Moly grease	Lautard, Guy	TMBR#3:73
        Money from a kinetic sculpture	Lautard, Guy	TMBR#3:211
        Money from cast al. grave markers, juke box parts, toy cars	Lautard, Guy	TMBR#3:209
        Money from model steam engines	Lautard, Guy	TMBR#3:214, 216
        Money from sandblasting	Lautard, Guy	TMBR#3:134
        Money from wind chimes	Lautard, Guy	TMBR#2:136
        More motorcycle repairs	Lautard, Guy	TMBR#3:2 17
        More on EDM machine drwgs	Lautard, Guy	TMBR#3:78
        More tricks for the odd-leg artist	Lautard, Guy	TMBR#2:104
        Morse Taper sockets	Lautard, Guy	TMBR#1:16
        Motorcycle wheel repairs	Lautard, Guy	TMBR#3:213
        Mounting a bench stone	Lautard, Guy	TMBR#2:119
        Multi-facet milling of radii, & filing to finish	Lautard, Guy	HTIM:22, TMBR#2:105
        Multi-sheave blocks	Lautard, Guy	TMBR#3:44
        Multiple identical castings in epoxy	Lautard, Guy	TMBR#3:115
        Muzzle brake, shop made	Lautard, Guy	TMBR#3:152
        My shop	Lautard, Guy	TMBR#2:vi; HTIM:51
        Myford lathes	Lautard, Guy	TMBR#1:67
        Natural and artificial stones	Lautard, Guy	TMBR#2:117
        Nice finish from files	Lautard, Guy	TMBR#1:7
        Not breaking small taps	Lautard, Guy	TMBR#1:17
        Notes re drawings	Lautard, Guy	TMBR#2:v; vi HTIM:iii
        Odd-leg artistry (setting up by eye)	Lautard, Guy	TMBR#1:81
        Offshore bandsaw blades vs. good ones	Lautard, Guy	HTIM:42
        Oil & steel wool for a nice finish	Lautard, Guy	TMBR#2:124
        Oil can spout modification	Lautard, Guy	TMBR#2:126
        Oil for your lathe centers	Lautard, Guy	TMBR#2:115
        Oil on files	Lautard, Guy	TMBR#1:7; TMBR#3:66
        Oil squirters from shampoo bottles	Lautard, Guy	TMBR#2:104
        Oil used to stick cigarette paper to work	Lautard, Guy	TMBR#1:84
        On making safe wooden lamps	Lautard, Guy	TMBR#3:206
        Optical centerpunch	Lautard, Guy	TMBR#3:105
        Optivisor	Lautard, Guy	TMBR#3:241
        Orbital sander finish on stainless steel	Lautard, Guy	TMBR#2:111
        Originating a master division plate	Lautard, Guy	TMBR#2:3
        Ornamental turning	Lautard, Guy	TMBR#3:215
        Osborne's Manoeuvre	Lautard, Guy	TMBR#2:159; TMBR#3:83, 96
        Osborne's manoeuvre	Lautard, Guy	TMBR#2:159
        Other ideas for dial numbering	Lautard, Guy	TMBR#3:247
        Other interests - how to track down people with	Lautard, Guy	TMBR#1:5-6
        Other steam engine designs	Lautard, Guy	TMBR#2:150
        Other-than-Myford #2 MT collets	Lautard, Guy	TMBR#3:11
        PVC or copper pipe for compressed air piping	Lautard, Guy	TMBR#3:12
        Paint sticks and sandpaper	Lautard, Guy	TMBR#2:124
        Pantographs and other ideas	Lautard, Guy	TMBR#3:248-251
        Parting off, essentials of	Lautard, Guy	TMBR#3:111
        Patch box hinge	Lautard, Guy	TMBR#3:200
        Patience	Lautard, Guy	TMBR#3:2
        Pedestals for shop tools	Lautard, Guy	TMBR#1:140
        Pencil lead holder for beam compass	Lautard, Guy	TMBR#3:127
        Perma-grit files	Lautard, Guy	TMBR#3:108
        Photo resist for Etching	Lautard, Guy	TMBR#1:136
        Picking up an edge with an indicator (jig borer style)	Lautard, Guy	TMBR#3:94
        Pierced work	Lautard, Guy	HTIM:49; TMBR#3:238-239
        Pin vise made from a Dremel chuck	Lautard, Guy	TMBR#3:172
        Pipe flanges	Lautard, Guy	TMBR#3:29
        Planing knots & twisted grain	Lautard, Guy	TMBR#3:195
        Plans and info for a power hacksaw	Lautard, Guy	TMBR#1:197
        Plate vs. sheet	Lautard, Guy	TMBR#2:11
        Plate vs. sheet steel (terminology)	Lautard, Guy	TMBR#2:11
        Plywood	Lautard, Guy	TMBR#3:191
        Plywood bandsaw	Lautard, Guy	HTIM:38-43; TMBR#3:184
        Pocket microscope for examining reamer flutes	Lautard, Guy	TMBR#3:158
        Polymer resin "castings" from CAD drawings	Lautard, Guy	TMBR#3:97
        Polyurethane casting resin	Lautard, Guy	TMBR#3:115
        Pot hooks for the kitchen	Lautard, Guy	TMBR#3:55
        Practical joke - hacksaw blade set on toolbox	Lautard, Guy	TMBR#1:130
        Pre-load spring for Solid cotters	Lautard, Guy	TMBR#1:100
        Precision tilting V-block	Lautard, Guy	TMBR#2:80
        Preparing steel for painting	Lautard, Guy	TMBR#2:115
        Prick punches and center punches	Lautard, Guy	TMBR#3:104
        Primary and secondary relief angles on reamers	Lautard, Guy	TMBR#3:157
        Prime number division	Lautard, Guy	TMBR#2:8
        Propane torch, made at home	Lautard, Guy	TMBR#1:52
        Protective mats for the milling machine table	Lautard, Guy	TMBR#3:76
        Pulling a "T" in copper pipe	Lautard, Guy	TMBR#3:80
        Pulling pins from truck springs	Lautard, Guy	TMBR#3:108
        Punching shapes in thin sheet metal on a Bridgeport	Lautard, Guy	TMBR#2:129
        Purpose of the ball on a surface gage spindle	Lautard, Guy	TMBR#2:131
        Putting on fine cuts by angling the topslide	Lautard, Guy	TMBR#1:12, 15
        Puzzles: Conway's	Lautard, Guy	HTIM:50-51
        Puzzles: Slothouber-Graatsma	Lautard, Guy	HTIM:50
        Quick change inserts for your mill's depth stop	Lautard, Guy	HTIM:36
        Quick change vise jaw liners	Lautard, Guy	TMBR#3:69
        Quick detach sine fixture for your milling vise	Lautard, Guy	TMBR#2:80
        Quickie bandsaw blade welding jig	Lautard, Guy	TMBR#2:126
        Radio Shack parts required	Lautard, Guy	TMBR#3:31
        Radiusing the ends of a part	Lautard, Guy	TMBR#2:105
        Re-babbetting machinery bearings	Lautard, Guy	TMBR#1:135
        Realigning the tailstock center	Lautard, Guy	TMBR#2:92
        Reamer Stoning technique	Lautard, Guy	TMBR#3:165
        Reamer sharpening	Lautard, Guy	TMBR#3:157-161
        Reamer sharpening, Choice of stones	Lautard, Guy	TMBR#3:162-164
        Reaming	Lautard, Guy	TMBR#1:16
        Reaming, Made from a dowel pin	Lautard, Guy	TMBR#3:66
        Reaming, On not ruining	Lautard, Guy	TMBR#1:16
        Rebuilding "scrapped" equipment	Lautard, Guy	TMBR#3:228
        Rebuilding alternators	Lautard, Guy	TMBR#3:109
        Recipe for a good cutting lube	Lautard, Guy	TMBR#1:177; TMBR#3:77
        Recipe for artists etching ground	Lautard, Guy	TMBR#3:245
        Recommended SFM for lathe filing	Lautard, Guy	HTIM:46
        Reducing errors in copying a master division plate	Lautard, Guy	TMBR#2:6
        Ref. to an article on making straightedges	Lautard, Guy	HTIM:48
        Ref. to an article on restoring a bandsaw	Lautard, Guy	TMBR#3:186
        Removal of broken taps from aluminum	Lautard, Guy	TMBR#3:78
        Removal of stuck bullets from rifle/pistol barrels	Lautard, Guy	TMBR#3:156
        Removing broken taps	Lautard, Guy	TMBR#1:18
        Removing burrs from new taps	Lautard, Guy	TMBR#1:17
        Removing that last half thou	Lautard, Guy	TMBR#1:12-15; TMBR#3:29 & 139
        Research methods	Lautard, Guy	TMBR#3:4-5
        Resetting stone in diamond dresser	Lautard, Guy	TMBR#2:66
        Retaining ring ("circlip"), shop made	Lautard, Guy	HTIM:11-12
        Reversible 2-speed appliance motors for shop drives	Lautard, Guy	TMBR#3:57
        Rifle cleaning rod	Lautard, Guy	TMBR#3:169-171
        Rifling machine, Bill Webb's	Lautard, Guy	TMBR#3:167; TMBR#2:198
        Roll over triggers	Lautard, Guy	TMBR#3:143
        Rotary Table - choice of horizontal or hor/vert.	Lautard, Guy	TMBR#1:41
        Rothenberger tube expander and T-extractor	Lautard, Guy	TMBR#3:82
        Rough dividing via marks on the lathe chuck	Lautard, Guy	TMBR#2:9
        Rough down, then finish tapers by grinding	Lautard, Guy	TMBR#2:92
        Rubberdraulic (& see Obscure)	Lautard, Guy	TMBR#1:71; TMBR#2:123
        Rubberflex collets	Lautard, Guy	TMBR#3:11
        Ruger handguns, modified/rebuilt by Hamilton Bowen	Lautard, Guy	TMBR#3:154
        Rule #1 on shop safety	Lautard, Guy	TMBR#2:152
        Rule #2 on shop safety	Lautard, Guy	TMBR#2:153
        Rust Preventive #2 on files	Lautard, Guy	TMBR#1:8
        Rust preventative made from Stockholm tar	Lautard, Guy	TMBR#3:77
        Rust removal with oil & steel wool	Lautard, Guy	TMBR#2:124
        Rust, Caused by glue	Lautard, Guy	TMBR#1:122
        Rust, Caused by plastic foam	Lautard, Guy	TMBR#1:122
        SIC magazine	Lautard, Guy	TMBR#2:150; TMBR#3:78
        STP as way lube	Lautard, Guy	TMBR#3:172
        Safe speeds for lathe chucks	Lautard, Guy	TMBR#3:62
        Safer filing in the lathe	Lautard, Guy	TMBR#2:132
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
        Sandblasting equipment	Lautard, Guy	TMBR#3:130-138
        Sandblasting gun details	Lautard, Guy	TMBR#3:121,136
        Sawing a 1 thou slot	Lautard, Guy	TMBR#3:176
        Sawing a box open after glue-up	Lautard, Guy	TMBR#3:195-196
        Saws for marking work	Lautard, Guy	TMBR#3:240
        Schieglel vise lift	Lautard, Guy	TMBR#3:68
        ScotchBrite	Lautard, Guy	TMBR#2:108
        Scraping 2 surfaces true to each other	Lautard, Guy	TMBR#2:14
        Screw thread data	Lautard, Guy	TMBR#1:201
        Screwcutting without a threading dial	Lautard, Guy	TMBR#3:112
        Screwcutting: Higby End	Lautard, Guy	TMBR#1:5, 20
        Scribing block	Lautard, Guy	TMBR#1:97; TMBR#2:198
        Scroll saws - Hegner, 5161, and shop made	Lautard, Guy	TMBR#3:241
        Sears speed converter	Lautard, Guy	TMBR#3:184
        Seasonal wood shrinkage and swelling	Lautard, Guy	TMBR#3:195
        Seasoning with ice & hot water	Lautard, Guy	TMBR#2:17
        Self-centering faceplate	Lautard, Guy	TMBR#1:163
        Self-cleaning spindle nose thread modification	Lautard, Guy	TMBR#3:59
        Self-holding & self-releasing tapers	Lautard, Guy	TMBR#2:92-93; HTIM:48
        Sensitivity of a tenths indicator	Lautard, Guy	TMBR#3:14
        Service flange, defined	Lautard, Guy	TMBR#1:33
        Servicing drill chucks	Lautard, Guy	TMBR#3:117
        Setting a lathe job to run eccentric: (6th point)	Lautard, Guy	TMBR#1:128
        Setting work flush with the top of your vise jaws	Lautard, Guy	TMBR#2:124
        Shackles & swivels	Lautard, Guy	TMBR#3:46-47
        Sharpening center punches	Lautard, Guy	TMBR#1:21
        Sharpening razors with magnetism	Lautard, Guy	TMBR#1:186
        Sharpening tungsten carbide tools	Lautard, Guy	TMBR#1:147
        Sharpening"razors & other fined edged tools	Lautard, Guy	TMBR#2:117-122; TMBR#3:237
        ShearLoc finger knobs	Lautard, Guy	TMBR#1:198
        Ships' wheels & oboes	Lautard, Guy	TMBR#3:214-21
        Shipyards and HSM 's	Lautard, Guy	TMBR#1:178
        Shop lamps	Lautard, Guy	TMBR#3:26
        Shop made angle plates - how to machine	Lautard, Guy	TMBR#2:101
        Shop made electric dial indicators	Lautard, Guy	TMBR#3:79
        Shop made metal hinges	Lautard, Guy	TMBR#3:199
        Shop made nibbling cutters	Lautard, Guy	HTIM:37
        Shop made specialty hammers	Lautard, Guy	TMBR#2:149
        Shop-made gage blocks	Lautard, Guy	TMBR#2:69
        Shrinking a pressed-in bush to remove it	Lautard, Guy	TMBR#2:129
        Silver solder, soldering, etc. How to do it	Lautard, Guy	TMBR#1:59
        Silver soldering	Lautard, Guy	TMBR#1:103
        Silver steel = drill rod	Lautard, Guy	TMBR#2:116
        Simple Dividing	Lautard, Guy	TMBR#1:40
        Simple lathe carriage index	Lautard, Guy	TMBR#1:68
        Simple sheet metal bending devices	Lautard, Guy	HTIM:27; TMBR#2:110
        Single lip cutters in place of commercial end mills	Lautard, Guy	HTIM:19
        Single row deep groove ball bearings	Lautard, Guy	TMBR#2:32
        Sling swivel base for tubular magazine rifles	Lautard, Guy	TMBR#1:113
        Slitting thin wall tubing	Lautard, Guy	TMBR#3:129
        Slot drills, What are they?	Lautard, Guy	TMBR#1:169; HTIM:4
        Small commercial machine from Green Instrument Co.	Lautard, Guy	TMBR#2:25
        Small sheet aluminum packing pieces	Lautard, Guy	TMBR#1:167
        Small shop-made hacksaw	Lautard, Guy	TMBR#2:101-102
        Small stock storage scheme	Lautard, Guy	TMBR#3:73
        Small tap wrench	Lautard, Guy	TMBR#1:35
        Smaller (watchmakers) collets	Lautard, Guy	TMBR#3:12
        Socket head cap screw dimensions	Lautard, Guy	TMBR#1:204
        Solder reveals temperature for a shrink fit	Lautard, Guy	TMBR#3:211
        Solder reveals temperature for removing bearings	Lautard, Guy	TMBR#3:211
        Soldering a steel ball for ball handles	Lautard, Guy	TMBR#3:173
        Soldering a steel ball onto a tapered shank	Lautard, Guy	TMBR#3:89
        Solid cotters	Lautard, Guy	TMBR#1:96
        Solid wood edging in plywood	Lautard, Guy	TMBR#3:197-198
        Some flux removal tips	Lautard, Guy	TMBR#2:124
        Some handy small tools	Lautard, Guy	TMBR#2:101
        Some ideas on gun making	Lautard, Guy	TMBR#1:116; TMBR#3:167
        Some milling vise accessory ideas	Lautard, Guy	TMBR#2:80
        Some more welding ideas	Lautard, Guy	TMBR#3:253
        Some notes on screwcutting	Lautard, Guy	TMBR#2:111-112; TMBR#3:112-113
        Some notes on taper turning	Lautard, Guy	TMBR#3:13-17
        Some notions on sharpening steel	Lautard, Guy	TMBR#1:117
        Source for a light oil and a way oil recipe	Lautard, Guy	TMBR#2:115
        Source of high quality cast iron for bullet molds	Lautard, Guy	TMBR#3:174
        Source of high quality cast iron for this project	Lautard, Guy	TMBR#1:91; TMBR#3:79
        Source of nitric acid	Lautard, Guy	TMBR#3:78
        Source of some project plans	Lautard, Guy	TMBR#1:197
        Sources of lapping supplies	Lautard, Guy	TMBR#3:65
        Space blocks	Lautard, Guy	TMBR#2:69
        Spade drills	Lautard, Guy	TMBR#1:155
        Speeding up work by not wasting time on needless precision	Lautard, Guy	TMBR#1:23
        Speeding up work by planning the job	Lautard, Guy	TMBR#1:23
        Spoked handwheels	Lautard, Guy	TMBR#3:58
        Spot grinding & lapping - a visit with a retired gage maker	Lautard, Guy	TMBR#2:58
        Spring loaded C-clamp	Lautard, Guy	HTIM:6
        Spring making	Lautard, Guy	TMBR#1:29, 154; HTIM:23-26, 30; TMBR#3:90,
        Spring tool for screwcutting	Lautard, Guy	TMBR#2:111-112
        Square drill rod	Lautard, Guy	TMBR#3:105
        Starrett #118 spacing center punch	Lautard, Guy	TMBR#3:102
        Starrett #160 & #240 pin chucks	Lautard, Guy	TMBR#3:12
        Starrett hold-downs	Lautard, Guy	TMBR#2:80
        Starrett layout hammer	Lautard, Guy	TMBR#3:104
        Starrett lock joint calipers	Lautard, Guy	TMBR#3:106
        Starrett's big combination square	Lautard, Guy	TMBR#3:106
        Starting a local hsm club	Lautard, Guy	TMBR#1:6
        Starting a reamer into the work	Lautard, Guy	TMBR#1:16
        Starting taps square	Lautard, Guy	TMBR#3:172
        Steel boxes	Lautard, Guy	TMBR#3:191
        Sticking the pattern on with Spray-Mount	Lautard, Guy	TMBR#3:240
        Stockholm tar smells right in the shop	Lautard, Guy	HTIM:48
        Stoning down a mill file for use in the lathe	Lautard, Guy	HTIM:45; TMBR#3:12
        Stoning reamers in the lathe	Lautard, Guy	TMBR#3:159
        Strength of nails	Lautard, Guy	TMBR#3:48-51
        Stress relieving CRS	Lautard, Guy	TMBR#1:25
        Strike While the Iron is Hot (excerpt)	Lautard, Guy	TMBR#1:45
        Stropping abrasive - making from grass charcoal	Lautard, Guy	TMBR#2:121
        Sub-faceplate	Lautard, Guy	TMBR#1:166
        Subreckys gadgets - tools you cant buy	Lautard, Guy	TMBR#2:127
        Substitute for dowel pins	Lautard, Guy	TMBR#2:103
        Support pad location for granite surface plates	Lautard, Guy	TMBR#3:224
        Surface gage desk lamp	Lautard, Guy	TMBR#3:205
        Surface tension in silver soldering centers bolt head	Lautard, Guy	TMBR#3:116
        Swaging hex sockets	Lautard, Guy	TMBR#2:95
        Swashplate steam engine	Lautard, Guy	TMBR#1:198
        Swivel base for small vise	Lautard, Guy	TMBR#1:37
        Symbols &Terms defined	Lautard, Guy	TMBR#1:1-2; TMBR#2:v; HTIM:ii; TMBR#3:2
        T-slotted plate for workholding	Lautard, Guy	TMBR#1:39
        Table saw, Ryobi BT3000	Lautard, Guy	TMBR#3:186
        Tailstock barrel handwheel (idea only)	Lautard, Guy	TMBR#1:72
        Take a camera along	Lautard, Guy	TMBR#3:109
        Tap breakage	Lautard, Guy	TMBR#3:172
        Tap starting dodge	Lautard, Guy	TMBR#1:167; HTIM:28
        Taper turning	Lautard, Guy	TMBR#2:90
        Tapping lube for stainless steel	Lautard, Guy	TMBR#2:116
        Tapping of blind holes	Lautard, Guy	TMBR#3:76
        Tapping oversize when wanted	Lautard, Guy	TMBR#1:17
        Tapping plastic - coarse vs. fine threads	Lautard, Guy	TMBR#3:175
        Teflon on electrical cord plugs	Lautard, Guy	TMBR#1:25
        Temperature benchmarks	Lautard, Guy	TMBR#1:200
        Temperature by appearance	Lautard, Guy	TMBR#1:200
        Testing a square against a surface plate or straightedge	Lautard, Guy	TMBR#2:15
        Testing lifting and slinging gear	Lautard, Guy	TMBR#3:39
        The Bullseye Mixture	Lautard, Guy	TMBR#2:163
        The Cole Drill	Lautard, Guy	TMBR#3:18
        The Disappearing Drilling & Tapping Tool	Lautard, Guy	TMBR#3:172
        The Duo-Mite bender	Lautard, Guy	TMBR#3:54
        The General Model 490 bandsaw	Lautard, Guy	TMBR#3:184
        The Haralson hose end	Lautard, Guy	TMBR#2:148
        The Jimmy Jig ( a table saw fence and more)	Lautard, Guy	TMBR#3:190
        The Little Torch	Lautard, Guy	TMBR#3:254
        The Metalmaster lathe	Lautard, Guy	TMBR#2:68
        The Poor Man's Jig Borer, a combination angle plate and hole locator	Lautard, Guy	TMBR#2:21
        The Potts and Arrand milling spindles	Lautard, Guy	TMBR#2:39-40
        The Secret of the Old Master (fiction, by Lucian Cary)	Lautard, Guy	TMBR#1:104
        The Simple-Fyer	Lautard, Guy	TMBR#2:73
        The Strokagenius File Rack	Lautard, Guy	HTIM:TMBR#1: TMBR#3:202
        The TINKER - an easy-to-build T&C Grinding Jig	Lautard, Guy	TMBR#1:103
        The Tesla turbine	Lautard, Guy	TMBR#2:150
        The Weaver launch engine	Lautard, Guy	TMBR#3:2 16
        The Woodpile	Lautard, Guy	TMBR#3:178-199
        The checking set square	Lautard, Guy	TMBR#2:11-14
        The clamp-on ball handle	Lautard, Guy	TMBR#1:80-85
        The clamp-on ball handle, as a lamp	Lautard, Guy	TMBR#3:205
        The cross filing technique	Lautard, Guy	TMBR#2:123
        The need for the Keeper	Lautard, Guy	TMBR#3:31
        The sine bar explained	Lautard, Guy	TMBR#2:75-78
        The ultimate box latch	Lautard, Guy	TMBR#1:125-129
        There's a Bridgeport in my basement	Lautard, Guy	TMBR#2:155
        Thoughts on tool storage & toolboxes	Lautard, Guy	TMBR#1:122-124
        Tightening a Jacobs chuck	Lautard, Guy	TMBR#2:38
        Tip for machining copper	Lautard, Guy	TMBR#3:114
        Tip for making nice soldered joints in copper pipe	Lautard, Guy	TMBR#3:82
        Tip re using a ball end mill	Lautard, Guy	TMBR#1:76
        Tool extension shank	Lautard, Guy	TMBR#2:103
        Tool for hand beading on sheet metal	Lautard, Guy	TMBR#1:148
        Tool for straight knurling	Lautard, Guy	TMBR#1:62-66
        Tool stands	Lautard, Guy	TMBR#1:155
        Tool storage boxes	Lautard, Guy	TMBR#1:124
        Toolholder to tilt toolbits to any desired helix angle	Lautard, Guy	TMBR#2:88
        Toolmaker's buttons, making & using	Lautard, Guy	TMBR#2:70
        Toolmaker's clamps	Lautard, Guy	TMBR#1:149
        Toolmaker, Fay and Yankee calipers - which to buy?	Lautard, Guy	TMBR#3:106
        Toolmaking	Lautard, Guy	TMBR#3:3
        Tools for cutting multi-start Acme threads	Lautard, Guy	TMBR#2:88
        Toothbrush makes a narrow brush	Lautard, Guy	TMBR#3:237
        Torsion springs - aversion to	Lautard, Guy	TMBR#3:145
        Toughness of steel used in ball bearings	Lautard, Guy	TMBR#3:174
        Toxic dusts	Lautard, Guy	TMBR#3:204
        Transfer centerpunch (a good one vs. a cheap one)	Lautard, Guy	TMBR#3:105
        Trefolex paste cutting compound	Lautard, Guy	TMBR#2:116
        Trig - in high school vs. from Lautard	Lautard, Guy	TMBR#3:100
        Trigger pull weight	Lautard, Guy	TMBR#3:142
        Trigger tuning and shop made triggers	Lautard, Guy	TMBR#3:140-151
        Triggers, critical dimensions	Lautard, Guy	TMBR#3:143
        Triggers, torsion springs - aversion to	Lautard, Guy	TMBR#3:145
        Trigonometry	Lautard, Guy	TMBR#1:12-13; TMBR#2:72-78
        Tripoli - washed/levigated tripoli, tripoli polish	Lautard, Guy	TMBR#2:121
        Truing up a straightedge	Lautard, Guy	TMBR#2:12
        Truing up an out-of-truth machinist's square	Lautard, Guy	TMBR#2:10
        Turkshead handles for a box	Lautard, Guy	HTIM:31
        Turner's cube	Lautard, Guy	TMBR#3:219
        Turning a long, slender screw	Lautard, Guy	TMBR#1:140
        Turning a straight taper on a wood lathe	Lautard, Guy	TMBR#3:205
        Turning small electric motor armatures	Lautard, Guy	TMBR#3:208
        Turning the OD of thin sheet material on a lathe	Lautard, Guy	TMBR#2:130
        Two muzzle loaders	Lautard, Guy	TMBR#3:6
        Two nice die filing machines	Lautard, Guy	TMBR#3:259
        Type of grinding wheels to use for spot grinding	Lautard, Guy	TMBR#2:65
        Uneven spacing of reamer flutes	Lautard, Guy	TMBR#3:158
        Use of a "roller' in chucking a rough cube	Lautard, Guy	TMBR#3:219
        Use of a chucking stub	Lautard, Guy	TMBR#2:6
        Use of ultra-fine wet/dry paper for sharpening	Lautard, Guy	TMBR#2:124; TMBR#3:201
        Used as a fixturing aid	Lautard, Guy	TMBR#1:33
        Useful aid to holding slippery shapes in mill vise	Lautard, Guy	HTIM:38
        Useful modifications to hermaphrodite calipers	Lautard, Guy	TMBR#1:83
        Uses for fiberglass typewriter erasers	Lautard, Guy	TMBR#3:211
        Using "thin set" concrete to level a lathe stand	Lautard, Guy	TMBR#3:216
        Using a busted HSS tap as a scriber tip	Lautard, Guy	TMBR#2:104
        Using a combination square to lay out an angle	Lautard, Guy	TMBR#3:99
        Using a master square	Lautard, Guy	TMBR#2:16
        Using a phonograph needle as a scriber	Lautard, Guy	TMBR#1:100
        Using a surface gage to test for squareness	Lautard, Guy	HTIM:35
        Using a washer to true up a rough turned ball	Lautard, Guy	TMBR#2:109
        Using an automatic c/p as a small impact hammer	Lautard, Guy	TMBR#3:20
        Using triangular scrapers	Lautard, Guy	TMBR#1:196
        V-belt length calculations	Lautard, Guy	TMBR#1:199
        V-belt speeds/pulley sizes	Lautard, Guy	TMBR#1:199
        V-grooved faceplate	Lautard, Guy	TMBR#1:169
        VW engine conversion to aircraft use	Lautard, Guy	TMBR#3:56
        Vanishing oil for machining plexiglas	Lautard, Guy	TMBR#3:66
        Varathane finish	Lautard, Guy	TMBR#3:190
        Various tapping kinks	Lautard, Guy	TMBR#1:18
        Varsol - what is it?	Lautard, Guy	TMBR#3:168
        Varsol as a cutting fluid for aluminum	Lautard, Guy	HTIM:14
        Vernier Division	Lautard, Guy	TMBR#2:7
        Very fine wet-dry paper	Lautard, Guy	TMBR#2:124;
        Very fine wet-dry paper for sharpening things	Lautard, Guy	TMBR#3:201
        Vise - simple, small	Lautard, Guy	TMBR#2:86
        Vise alignment on milling machine	Lautard, Guy	TMBR#1:138
        Wafer head screws	Lautard, Guy	HTIM:32
        Wanting lots of #2 MT shanks	Lautard, Guy	TMBR#3:13
        Warnings re cadmium	Lautard, Guy	TMBR#2:116
        Warnings re cyanoacrylate glue	Lautard, Guy	TMBR#2:116
        Warpage in heat treating	Lautard, Guy	TMBR#1:53
        Water of Ayr stone	Lautard, Guy	TMBR#2:118; TMBR#3:237
        Wax/Stockholm tar resist	Lautard, Guy	TMBR#3:247
        Webber gage blocks	Lautard, Guy	TMBR#2:81-82
        Welded steel corner caps	Lautard, Guy	TMBR#3:256
        Welding rod	Lautard, Guy	TMBR#1:6
        Welding rod for aluminum	Lautard, Guy	TMBR#2:122
        What to do if you get a steel chip in your eye	Lautard, Guy	TMBR#1:132
        Where not to use a sine plate	Lautard, Guy	TMBR#2:79
        Where to buy Silver solder, solder	Lautard, Guy	TMBR#1:59
        Where you might get a drafting machine cheap	Lautard, Guy	TMBR#2:133
        Why Bubbles in levels get long or short	Lautard, Guy	TMBR#3:106
        Why an uneven number of spokes?	Lautard, Guy	TMBR#3:39
        Why is your lathe tailstock high?	Lautard, Guy	TMBR#3:217
        Why own several hacksaws?	Lautard, Guy	TMBR#2:100
        Why the ball on a surface gage spindle?	Lautard, Guy	TMBR#2:131
        Why the mirror in a Gerstner toolbox?	Lautard, Guy	TMBR#1:130-132
        Wire bending jigs	Lautard, Guy	TMBR#3:53
        Wire edge on cutting edges removed w/ a copper coin	Lautard, Guy	TMBR#3:157
        Wiring for correct polarity	Lautard, Guy	TMBR#3:57
        Wiring the lamp	Lautard, Guy	TMBR#3:31-32
        With Unimat lathes - repairing valves & spray nozzles	Lautard, Guy	TMBR#3:208
        With homebuilt aircraft people	Lautard, Guy	TMBR#3:56
        Wobbler for making centerpunch marks run true	Lautard, Guy	TMBR#1:22
        Wood finishing	Lautard, Guy	TMBR#3:198
        Wooden tool storage boxes	Lautard, Guy	TMBR#3:191-199, 215
        Woodturning on a metal lathe	Lautard, Guy	TMBR#1:174
        Workbenches etc.	Lautard, Guy	TMBR#1:133-135; TMBR#3:178-183
        Workmanship	Lautard, Guy	TMBR#1:4-5
        Worlds smallest lathe, and notes re some other miniatures	Lautard, Guy	TMBR#2:145
    '''
    # Construct data
    data = []
    for line in raw_data.split("\n"):
        line = line.strip()
        if not line:
            continue
        f = line.split("\t")
        assert len(f) == 3, repr(line)
        assert f[1] == "Lautard, Guy"
        data.append((f[0], f[2]))
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] regexp
            Look up topics in Guy Lautard's (1947-2025) "The Machinist Bedside Reader" books:
            vol. 1 (1986), vol. 2 (1988), vol. 3 (1993).  Matches are printed to stdout.  Use
            the command '{sys.argv[0]} .' to list all the entries.  TMBR#3:72 means volume 3,
            page 72.  HTIM:45 means "Hey, Tim...", a small 1990 51 page book.
        Options:
            -1    Only print out items from volume 1
            -2    Only print out items from volume 2
            -3    Only print out items from volume 3
            -i    Make the search case-sensitive
            -x    Print a concordance to stdout
        '''))
        exit(status)
    def ParseCommandLine():
        d["-1"] = False     # Vol 1 only
        d["-2"] = False     # Vol 2 only
        d["-3"] = False     # Vol 3 only
        d["-i"] = True      # Ignore case
        d["-x"] = False     # Generate concordance
        try:
            opts, args = getopt.getopt(sys.argv[1:], "123ix")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in "123ix":
                d[o] = not d[o]
        if d["-x"]:
            GenerateConcordance(d)
            exit(0)
        if not args:
            Usage()
        if d["-1"] or d["-2"] or d["-3"]:
            # Filter data
            def Keep(loc):
                if d["-1"] and "#1" in loc:
                    return True
                if d["-2"] and "#2" in loc:
                    return True
                if d["-3"] and "#3" in loc:
                    return True
                return False
            newdata = []
            global data
            for item, loc in data:
                if Keep(loc):
                    newdata.append((item, loc))
            data = newdata
        return args
if 1:  # Core functionality
    def FilterWords(words):
        '''Remove words we don't want to keep.  words is a sequence of
        words.
        '''
        remove = set('''
            'flat 's - /or 0 018 1 1/4 118 15/16 160 1st 2 240 3 3/4 3000
            490 5161 6th 7/8 75 9 900 a after against ago ahead aid aided al
            along an and any are as at back be before big by c c/p can co
            come d dark de do does don't down el etc for from get half have
            her how i if in inc into is it its m22 may might more my not of
            on one ones only onto or other out over own p per pre re ref s
            see self so some t takes than that the then there there's they
            things this thou to too two up upon use used useful uses using v
            very vs w/ was we what what when where which while why why/where
            with without you your
        '''.split())
        words = set(words)
        keep = set()
        for word in words:
            if word.lower() in remove:
                continue
            keep.add(word)
        return keep
    def Split(line):
        '''Return a sequence of words from the line after replacing
        punctuation, etc. with spaces.  Also weed out lines that aren't to
        be used, so the returned sequence could be empty.
        '''
        p = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        p = string.punctuation
        for i in "/-'":
            p = p.replace(i, "")
        for i in p:
            line = line.replace(i, " ")
        words = line.split()
        return FilterWords(words)
    def NormalizeRefs(refs):
        "Split on ';', then sort"
        out = []
        for i in refs:
            for j in i.split(";"):
                out.append(j.strip())
        return list(sorted(set(out)))
    def GenerateConcordance(d):
        "Print a concordance to stdout"
        # Get all the words in the descriptions
        words = set()
        for text, vol in data:
            words.update(Split(text))
        words = list(sorted(words))
        for word in words:
            refs = []
            for text, ref in data:
                if word.lower() in text.lower():
                    refs.append(ref)
            if refs:
                print(word)
                sep = " " * 2
                refs = NormalizeRefs(refs)
                for line in Columnize(refs, indent=sep, sep=sep):
                    print(line)
        exit(0)
    def ColorizeLoc(loc):
        if "," in loc:
            o = []
            for loc1 in loc.split(","):
                o.append(ColorizeLoc(loc1.strip()))
            return ", ".join(o)
        else:
            if "#1" in loc:
                return f"{t.v1}{loc}{t.n}"
            elif "#2" in loc:
                return f"{t.v2}{loc}{t.n}"
            elif "#3" in loc:
                return f"{t.v3}{loc}{t.n}"
            elif "HTIM" in loc:
                return f"{t.ht}{loc}{t.n}"
            else:
                t.print(f"{t.orn}Unknown string in loc: {loc!r}")
                return f"{loc}"
    def PrintMatches(regexp):
        f = re.I if d["-i"] else 0
        r = re.compile(regexp, f)
        for i in data:
            title, loc = i
            mo = r.search(title)
            if mo:
                t.print(f"{title} {ColorizeLoc(loc)}")
if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine()
    for regexp in args:
        PrintMatches(regexp)
