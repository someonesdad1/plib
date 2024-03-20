'''
TODO

    * Sizes are not sorted
    * "meters" in parentheses are not being converted to m.  Example:  do a
      search on '1mm'.

Show lengths close to command line argument
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2020 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Show lengths close to command line argument
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Imports
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        import u
        from f import flt
        from color import t
        import color as C
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        ii = isinstance
        SI_prefix = {
            -24: "y", -21: "z", -18: "a", -15: "f", -12: "p", -9: "n", -6: "μ",
            -3: "m", 0: "", 3: "k", 6: "M", 9: "G", 12: "T", 15: "P", 18: "E",
            21: "Z", 24: "Y"
        }
if 1:   # Raw data from https://en.wikipedia.org/wiki/Orders_of_magnitude_(length)
    # Changes I've made:
    #   - I have removed inconsistencies and annoyances in the original web page data.
    #
    # References to cm have been changed to mm, as I consider the use of CGS units to be
    # antiquated.  The entries were sorted by size.
    data = dedent('''

    1.6e-11 ym 		The Planck length (measures of distance shorter than this are considered nonsensical and do not make any physical sense, according to current theories of physics)
    1 ym 		 1 yoctometer, the smallest named subdivision of the meter in the SI base unit of length, 1e-24 meter
    1 ym 		 Length of a neutrino
    2 ym 		 Effective cross-section radius of 1 MeV neutrinos
    100 ym 		 Length of a top quark, one of the smallest known quarks
    2 zm 		 Length of a preon, hypothetical particles proposed as subcomponents of quarks and leptons
    2 zm 		 Radius of effective cross section for a 20 GeV neutrino scattering off a nucleon
    7 zm 		 Radius of effective cross section for a 250 GeV neutrino scattering off a nucleon
    15 zm 		 Length of a high energy neutrino
    30 zm 		 Length of a bottom quark
    177 zm 		 de Broglie wavelength of protons at the Large Hadron Collider (7 TeV as of 2010)
    1 am 		 Length of a down quark
    1 am 		 Length of an electron
    1 am 		 Length of an up quark
    1 am 		 Sensitivity of the LIGO detector for gravitational waves
    1 am 		 Upper bound of the typical size range for "fundamental strings"
    1 am 		 Upper limit for the size of quarks and electrons
    10 am 		 Range of the weak force
    100 am 		 All lengths shorter than this distance are not confirmed in terms of size
    850 am 		 Approximate proton radius
    1 fm 		 Diameter of a neutron, approximate range-limit of the color force carried between quarks by gluons
    1.5 fm 		 Diameter of the scattering cross section of an 11 MeV proton with a target proton
    1.75 fm 		 The effective charge diameter of a proton
    2.81794 fm 		 Classical electron radius
    3 fm 		 Approximate range-limit of the nuclear binding force mediated by mesons
    7 fm 		 The radius of the effective scattering cross section for a gold nucleus scattering a 6 MeV alpha particle over 140 degrees
    1.75 to 15 fm 		 Diameter range of the atomic nucleus
    570 fm 		 Typical distance from the atomic nucleus of the two innermost electrons (electrons in the 1s shell) in the uranium atom, the heaviest naturally-occurring atom
    1 pm 		 Distance between atomic nuclei in a white dwarf
    2.4 pm 		 The Compton wavelength of the electron
    5 pm 		 Shorter X-ray wavelengths
    25 pm 		 Approximate radius of a helium atom, the smallest neutral atom
    50 pm 		 Bohr radius: approximate radius of a hydrogen atom
    50 pm 		 Radius of a hydrogen atom
    ~50 pm 		 Best resolution of a high-resolution transmission electron microscope
    60 pm 		 Radius of a carbon atom
    93 pm 		 Length of a diatomic carbon molecule
    100 pm 		 1 Ångström
    100 pm 		 Covalent radius of sulfur atom
    120 pm 		 Radius of a gold atom
    120 pm 		 Van der Waals radius of a neutral hydrogen atom
    126 pm 		 Covalent radius of ruthenium atom
    135 pm 		 Covalent radius of technetium atom
    150 pm 		 Length of a typical covalent bond (C-C)
    153 pm 		 Covalent radius of silver atom
    155 pm 		 Covalent radius of zirconium atom
    175 pm 		 Covalent radius of thulium atom
    200 pm 		 Highest resolution of a typical electron microscope
    225 pm 		 Covalent radius of cesium atom
    280 pm 		 Average size of the water molecule
    298 pm 		 Radius of a cesium atom, calculated to be the largest atomic radius (except possibly francium)
    340 pm 		 Thickness of single layer graphene
    356.68 pm 		 Width of diamond unit cell
    403 pm 		 Width of lithium fluoride unit cell
    500 pm 		 Width of protein α helix
    543 pm 		 Silicon lattice spacing
    560 pm 		 Width of sodium chloride unit cell
    700 pm 		 Width of glucose molecule
    780 pm 		 Mean width of quartz unit cell
    820 pm 		 Mean width of ice unit cell
    900 pm 		 Mean width of coesite unit cell
    1 nm 		 Diameter of a carbon nanotube
    1 nm 		 Length of a buckyball
    1 nm 		 Roughly the length of a sucrose molecule, calculated by Albert Einstein
    2.3 nm 		 Length of a phospholipid
    2.3 nm 		 Smallest gate oxide thickness in microprocessors
    3 nm 		 As of 2019, the average half-pitch of a memory cell expected to be manufactured circa 2022
    3 nm 		 Width of a DNA helix
    3.4 nm 		 Length of a DNA turn (10 bp)
    3.8 nm 		 Size of an albumin molecule
    5 nm 		 As of October 2018, the average half-pitch of a memory cell expected to be manufactured circa 2019-2020
    5 nm 		 Size of the gate length of a 16 nm processor
    5 nm 		 Flying height of the head of a hard disk in 2011
    6 nm 		 Length of a phospholipid bilayer
    6.8 nm 		 Width of a hemoglobin molecule
    7 nm 		 Average half-pitch of a memory cell manufactured circa 2018
    6 to 10 nm 		 Thickness of cell membrane
    10 nm 		 Average half-pitch of a memory cell manufactured circa 2016-2017
    10 nm 		 Lower size of tobacco smoke
    10 nm 		 The average length of a nanowire
    10 nm 		 Thickness of cell wall in Gram negative bacteria
    13 nm 		 The length of the wavelength that is used for EUV lithography
    14 nm 		 Average half-pitch of a memory cell manufactured circa 2013
    14 nm 		 Length of a porcine circovirus
    15 nm 		 Length of an antibody
    18 nm 		 Diameter of tobacco mosaic virus
    20 nm 		 Length of a nanobe, could be one of the smallest forms of life
    20 nm 		 Thickness of bacterial flagellum
    22 nm 		 Average half-pitch of a memory cell manufactured circa 2011-2012
    22 nm 		 Smallest feature size of production microprocessors in September 2009
    30 nm 		 Lower size of cooking oil smoke
    32 nm 		 Average half-pitch of a memory cell manufactured circa 2009-2010
    40 nm 		 Extreme ultraviolet wavelength
    45 nm 		 Average half-pitch of a memory cell manufactured circa 2007-2008
    20 to 80 nm 		 Thickness of cell wall in Gram-positive bacteria
    50 nm 		 Flying height of the head of a hard disk
    50 nm 		 Upper size for airborne virus particles
    58 nm 		 Height of a T7 bacteriophage
    65 nm 		 Average half-pitch of a memory cell manufactured circa 2005-2006
    90 nm 		 Average half-pitch of a memory cell manufactured circa 2002-2003
    90 nm 		 Human immunodeficiency virus (HIV) (generally, viruses range in size from 20 nm to 450 nm)
    100 nm 		 90% of particles in wood smoke are smaller than this
    100 nm 		 Greatest particle size that can fit through a surgical mask
    100 nm 		 Length of a mesoporous silica nanoparticle
    120 nm 		 Diameter of a human immunodeficiency virus (HIV)
    120 nm 		 Greatest particle size that can fit through a ULPA filter
    125 nm 		 Standard depth of pits on compact disks (width: 500 nm, length: 850 nm to 3.5 μm)
    180 nm 		 Typical length of the rabies virus
    200 nm 		 Typical size of a Mycoplasma bacterium, among the smallest bacteria
    300 nm 		 Greatest particle size that can fit through a HEPA (High Efficiency Particulate Air) filter (N100 removes up to 99.97% at 0.3 micrometers, N95 removes up to 95% at 0.3 micrometers)
    300 to 400 nm 		 Near ultraviolet wavelength
    400 to 420 nm 		 Wavelength of violet light
    420 to 440 nm 		 Wavelength of indigo light
    440 to 500 nm 		 Wavelength of blue light
    500 to 520 nm 		 Wavelength of cyan light
    520 to 565 nm 		 Wavelength of green light
    589 nm 		 Wavelength of sodium light
    565 to 590 nm 		 Wavelength of yellow light
    590 to 625 nm 		 Wavelength of orange light
    625 to 700 nm 		 Wavelength of red light
    1 μm 		 Edge of cube of volume 10⁻¹⁸ m³ (1 fL)
    1 μm 		 Length of a lysosome
    1 μm 		 The side of square of area 10⁻¹² m²
    1 to 2 μm 		 Anthrax spore
    2 μm 		 Length of an average E. coli bacteria
    3 to 4 μm 		 Size of a typical yeast cell
    5 μm 		 Length of a typical human spermatozoon's head
    1 to 10 μm 		 Diameter of a typical bacterium
    3 to 8 μm 		 Width of strand of spider web silk
    6 μm 		 Thickness of the tape in a 120-minute (C120) compact cassette
    7 μm 		 Diameter of the nucleus of a typical eukaryotic cell
    ~ 7 μm 		 Diameter of human red blood cells
    5 to 10 μm 		 Width of a chloroplast
    8 to 11 μm 		 Size of a ground-level fog or mist droplet
    10 μm 		 Mean longest dimension of a human red blood cell
    10 μm 		 Transistor width of the Intel 4004, the world's first commercial microprocessor
    10 μm 		 Width of cotton fiber
    10.6 μm 		 Wavelength of light emitted by a carbon dioxide laser
    5 to 20 μm 		 Dust mite excreta
    15 μm 		 Width of silk fiber
    17 μm 		 Minimum width of a strand of human hair
    17.6 μm 		 One twip, a unit of length in typography
    25.4 μm 		 1/1000 inch, commonly referred to as 1 mil in the U.S. and 1 thou in the UK
    30 μm 		 Length of a human skin cell
    10 to 55 μm 		 Width of wool fiber
    50 μm 		 Length of a silt particle
    50 μm 		 Typical length of Euglena gracilis, a flagellate protist
    50 μm 		 Typical length of a human liver cell, an average-sized body cell
    60 μm 		 Length of a sperm cell
    100 μm 		 0.00394 inches
    100 μm 		 1/10 of a millimeter
    100 μm 		 Average diameter of a strand of human hair
    100 μm 		 Length of a dust particle
    100 μm 		 Smallest distance that can be seen with the naked eye
    100 μm 		 Thickness of a coat of paint
    120 μm 		 Diameter of a human ovum
    120 μm 		 The geometric mean of the Planck length and the diameter of the observable universe
    70 to 180 μm 		 Thickness of paper
    ~0.7 to 300 μm 		 Wavelength of infrared radiation
    170 μm 		 Length of the largest sperm cell in nature, belonging to the Drosophila bifurca fruit fly
    181 μm 		 Maximum width of a strand of human hair
    200 μm 		 Nominal width of the smallest commonly available mechanical pencil lead (0.2 mm)
    200 μm 		 Typical length of Paramecium caudatum, a ciliate protist
    100 to 400 μm 		 Length of Demodex mites living in human hair follicles
    250 to 300 μm 		 Length of a dust mite
    340 μm 		 Length of a single pixel on a 17-inch monitor with a resolution of 1024×768
    700 to 1.4 μm 		 Wavelength of near-infrared radiation
    500 μm 		 Average length of a grain of salt
    500 μm 		 Average length of a grain of sand
    500 μm 		 Average length of a grain of sugar
    500 μm 		 MEMS micro-engine
    500 μm 		 Typical length of Amoeba proteus, an amoeboid protist
    560 μm 		 Thickness of the central area of a human cornea
    750 μm 		 Diameter of a Thiomargarita namibiensis, the largest bacteria known
    760 μm 		 Thickness of an identification card
    1.0 mm 		 0.03937 inches or 5/127 (exactly)
    1.0 mm 		 1/1000 of a meter
    1.0 mm 		 Diameter of a pinhead
    1.0 mm 		 Side of square of area 1 mm²
    1.5 mm 		 Length of average flea
    1.52 mm 		 Thickness of US penny
    2.54 mm 		 Distance between pins on dual in-line package (DIP) electronic components (0.1 inch)
    5 mm 		 Diameter of an average grain of rice
    5 mm 		 Length of an average red ant
    6 mm 		 Approximate width of a pencil
    7 mm 		 Length of a Paedophryne amauensis, the smallest known vertebrate
    7.1 mm 		 Length of a sunflower seed
    8 mm 		 Length of a Paedocypris progenetica, the smallest known fish
    8 mm 		 Popular movie film width used from about 1930 to 1990
    10 mm 		 Approximate width of average fingernail
    10 mm 		 Edge of cube of volume 1 ml
    10 mm 		 Length of a coffee bean
    12 mm 		 Diameter of a dice
    12 mm 		 Length of a bee
    15 mm 		 Length of a very large mosquito
    16 mm 		 Popular movie film width used from about 1930 to 1970
    16 mm 		 Length of a Jaragua Sphaero, a very small reptile
    17 mm 		 Length of a Thorius arboreus, the smallest salamander
    19.05 mm 		 Diameter of US penny
    20 mm 		 Approximate width of an adult human finger
    24.26 mm 		 Diameter of US quarter
    25.4 mm 		 1 inch
    34 mm 		 Length of a quail egg
    35 mm 		 Width of film commonly used in motion pictures and still photography
    43 mm 		 Minimum diameter of a golf ball
    50 mm 		 Height of a hummingbird, the smallest known bird
    50 mm 		 Usual diameter of a chicken egg
    54 mm 		 Width of a standard credit card
    61 mm 		 Average height of an apple
    66.3 mm		 Height of a US dollar bill
    73 to 75 mm 		 Diameter of a baseball
    86 mm 		 Length of a standard credit card
    90 mm 		 Length of a Speckled Padloper, the smallest known turtle
    100 mm		 Diameter of the human cervix upon entering the second stage of labor
    100 mm		 Wavelength of the highest UHF radio frequency, 3 GHz
    101.6 mm		 1 hand used in measuring height of horses (4 inches)
    110 mm		 Diameter of an average potato in the US
    120 mm		 Diameter of a compact disk (CD)
    120 mm		 Wavelength of the 2.45 GHz ISM radio band
    150 mm		 Approximate size of largest beetle species
    150 mm		 Length of a Bic pen with cap on
    156 mm		 Width of a US dollar bill
    190 mm		 Length of a banana
    210 mm		 Wavelength of the 1.4 GHz hydrogen emission line, a hyperfine transition of the hydrogen atom
    220 mm		 Diameter of a typical soccer ball
    263 mm		 Length of average male human foot
    299.8 mm		 Distance light travels in one nanosecond
    300 mm		 Typical school-use ruler length (= 300 mm)
    304.8 mm		 1 foot (measure)
    310 mm		 Wingspan of largest butterfly species Ornithoptera alexandrae
    460 mm		 Length of an average domestic cat
    500 to 650 mm		 A coati's tail
    600 mm		 Standard depth (front to back) of a domestic kitchen worktop in Europe
    660 mm		 Length of the longest pine cones (produced by the sugar pine)
    840 mm		 Approximate diameter of 2008 TS26, a meteoroid
    900 mm		 Average length of a rapier, a fencing sword
    914.4 mm		 One yard (measure)
    1 m 		 Approximate height of the top part of a doorknob on a door
    1 m 		 Diameter of a very large beach ball
    1 m 		 Height of Homo floresiensis (the "Hobbit")
    1 m		 Wavelength of the lowest UHF radio frequency, 300 MHz
    1.15 m 		 A pizote (mammal)
    1.37 m 		 Average height of an Andamanese person
    1.435 m 		 Standard gauge of railway track used by about 60% of railways in the world = 4' 8½"
    1.63 m 		 (5 feet 4 inches) (or 64 inches) - height of average US female human as of 2002 (source: US Centers for Disease Control and Prevention (CDC))
    1.75 m 		 (5 feet 8 inches) - height of average US male human as of 2002 (source: US CDC as per female above)
    2.44 m 		 Height of an association soccer goal
    2.45 m 		 Highest high jump by a human being (Javier Sotomayor)
    2.5 m 		 Distance from the floor to the ceiling in an average residential house
    2.5 m 		 Height of a sunflower
    2.7 m 		 Length of the Starr Bumble Bee II, the smallest plane
    2.72 m 		 (8 feet 11 inches) - tallest known human being (Robert Wadlow)
    3.05 m 		 (10 feet) height of the basket in basketball
    3.05 m 		 The length of an old Mini
    2.77 to 3.44 m 		 Wavelength of the broadcast radio FM band 87-108 MHz
    3.63 m 		 The record wingspan for living birds (a wandering albatross)
    4.1 m 		 Diameter of 2008 TC3, a small asteroid that flew into the Earth's atmosphere on October 7, 2008
    3 to 6 m 		 Approximate diameter of 2003 SQ222, a meteoroid
    5 m 		 Length of an elephant
    5.2 m 		 Height of a giraffe
    5.5 m 		 Height of a Baluchitherium, the largest land mammal ever lived
    7 m 		 Wingspan of Argentavis, the largest flying bird known
    7.5 m 		 Approximate length of the human gastrointestinal tract
    8.38 m 		 The length of a London Bus (AEC Routemaster)
    8.95 m 		 Longest long jump by a human being (Mike Powell)
    10 meters 		 Average length of human digestive tract
    10 meters 		 Wavelength of the highest shortwave radio frequency, 30 MHz
    11 meters 		 Approximate width of a doubles tennis court
    12 meters 		 Length of a whale shark, largest living fish
    12 meters 		 Wingspan of a Quetzalcoatlus, a pterosaur
    13 meters 		 Length of a giant squid and colossal squid, the largest living invertebrates
    15 meters 		 Approximate distance the tropical circles of latitude are moving towards the equator and the polar circles are moving towards the poles each year due to a natural, gradual decrease in the Earth's axial tilt
    15 meters 		 Width of a standard FIBA basketball court
    15.24 meters 		 Width of an NBA basketball court (50 feet)
    18 meters 		 Height of a Sauroposeidon, the tallest known dinosaur
    18.44 meters 		 Distance between the front of the pitcher's rubber and the rear point of home plate on a baseball field (60 feet, 6 inches)
    20 meters 		 Length of a Leedsichthys, the largest known fish ever lived
    20 meters 		 Length of cricket pitch (22 yards)
    21 meters 		 Height of High Force waterfall in England
    23 meters 		 Height of the obelisk of the Place de la Concorde, Paris, France
    25 meters 		 Wavelength of the broadcast radio shortwave band at 12 MHz
    27.43 meters 		 Distance between bases on a baseball field (90 feet)
    28 meters 		 Length of a standard FIBA basketball court
    28.65 meters 		 Length of an NBA basketball court (94 feet)
    29 meters 		 Height of the lighthouse at Savudrija, Slovenia
    30 meters 		 Diameter of 1998 KY26, a rapidly spinning meteoroid
    31 meters 		 Wavelength of the broadcast radio shortwave band at 9.7 MHz
    32 meters 		 Approximate diameter of 2008 HJ, a small meteoroid
    33 meters 		 Length of a blue whale, the largest animal on earth, living or extinct, in terms of mass
    34 meters 		 Height of the Split Point Lighthouse in Aireys Inlet, Victoria, Australia
    35 meters 		 Length of a Supersaurus, the longest known dinosaur and longest vertebrate
    40 meters 		 Average depth beneath the seabed of the Channel tunnel
    49 meters 		 Wavelength of the broadcast radio shortwave band at 6.1 MHz
    49 meters 		 Width of an American football field (53.33 yards)
    50 meters 		 Length of a road train
    52 meters 		 Height of Niagara Falls
    55 meters 		 Height of the Leaning Tower of Pisa
    55 meters 		 Length of a bootlace worm, the longest known animal
    59.436 meters 		 Width of a Canadian football field (65 yards)
    62.5 meters 		 Height of Pyramid of Djoser
    64 meters 		 Wingspan of a Boeing 747-400
    69 meters 		 Wingspan of an Antonov An-124 Ruslan
    70 meters 		 Length of the Bayeux Tapestry
    70 meters 		 Typical width of soccer field
    70 meters 		 Width of a typical association soccer field
    77 meters 		 Wingspan of a Boeing 747-8
    83 meters 		 Height of a Western hemlock
    88.4 meters 		 Wingspan of the Antonov An-225 Mriya transport aircraft
    91 meters 		 Length of American football field (100 yards, measured between the goal lines)
    91.5 meters 		 137 meters - length of a soccer field
    93 meters 		 Height of the Statue of Liberty
    96 meters 		 Height of Big Ben
    100 meters 		 Spacing of location marker posts on British motorways
    100 meters 		 The distance a very fast human being can run in about 10 seconds
    100 meters 		 Wavelength of the highest medium wave radio frequency, 3 MHz
    100 meters 		 Wavelength of the lowest shortwave radio frequency, 3 MHz
    100.584 meters 		 Length of a Canadian football field between the goal lines (110 yards)
    105 meters 		 Length of a typical soccer field
    105 meters 		 Length of soccer pitch (UEFA Stadium Category 3 and 4)
    109.73 meters 		 Total length of an American football field (120 yards, including the end zones)
    115.5 meters 		 Height of the world's tallest tree in 2007, the Hyperion sequoia
    110 to 150 meters 		 The width of an Australian football field
    137.16 meters 		 Total length of a Canadian football field, including the end zones (150 yards)
    138.8 meters 		 Height of the Great Pyramid of Giza (Pyramid of Cheops)
    139 meters 		 Height of the world's tallest roller coaster, Kingda Ka
    187 meters 		 Shortest wavelength of the broadcast radio AM band, 1600 kHz
    202 meters 		 Length of the Széchenyi Chain Bridge connecting Buda and Pest
    270 meters 		 Length of 99942 Apophis
    310 meters 		 Maximum depth of Lake Geneva
    318 meters 		 Height of The New York Times Building
    318.9 meters 		 Height of the Chrysler Building
    320.75 meters 		 Height of the Eiffel Tower(including antenna)
    328 meters 		 Height of Auckland's Sky Tower, the tallest free-standing structure in the Southern Hemisphere
    340 meters 		 Distance sound travels in air at sea level in one second; see Speed of sound
    341 meters 		 Height of the world's tallest bridge, the Millau Viaduct
    390 meters 		 Height of the Empire State Building
    458 meters 		 Length of the Knock Nevis, the world's largest supertanker
    535 meters 		 Length of 25143 Itokawa, a small asteroid visited by a spacecraft
    553.33 meters 		 Height of the CN Tower
    555 meters 		 Longest wavelength of the broadcast radio AM band, 540 kHz
    400 to 800 meters 		 Approximate heights of the world's tallest skyscrapers of the past 80 years
    630 meters 		 Height of the KVLY-TV mast, second tallest structure in the world
    646 meters 		 Height of the Warsaw radio mast, the world's tallest structure until its collapse in 1991
    828 meters 		 Height of Burj Khalifa, world's tallest structure on 17 January 2009
    979 meters 		 Height of the Salto Angel, the world's highest free-falling waterfall (Venezuela)
    1 km 		 Diameter of 1620 Geographos
    1 km 		 Very approximate size of the smallest known moons of Jupiter
    1 km 		 Wavelength of the highest long wave radio frequency, 300 kHz
    1000 meters 		 Wavelength of the lowest mediumwave radio frequency, 300 kHz
    1.280 km 		 Span of the Golden Gate Bridge (distance between towers)
    1.4 km 		 Diameter of Dactyl, the first confirmed asteroid moon
    1.609 km 		 1 mile
    1.637 km 		 Deepest dive of Lake Baikal in Russia, the world's largest fresh water lake
    1.852 km 		 1 nautical mile, equal to 1 arc minute of latitude at the surface of the Earth
    1.991 km 		 Span of the Akashi Kaikyō Bridge
    2.228 km 		 Height of Mount Kosciuszko, highest point on mainland Australia
    2.309 km 		 Axial length of the Three Gorges Dam, the largest dam in the world
    3.991 km 		 Length of the Akashi Kaikyō Bridge, longest suspension bridge in the world as of December 2008
    4.8 km 		 Diameter of 5535 Annefrank, an inner belt asteroid
    4.810 km 		 Height of Mont Blanc, highest peak in the Alps
    4.884 km 		 Height of Carstensz Pyramid, highest peak in Oceania
    4.892 km 		 Height of Mount Vinson, highest peak in Antarctica
    5 km 		 Diameter of 3753 Cruithne
    5 km 		 Length of PSR B1257+12
    5.072 km 		 Height of Tanggula Mountain Pass, below highest peak in the Tanggula Mountains, highest railway pass in the world as of August 2005
    5.610 km 		 Height of Mount Damavand, highest peak in Iran
    5.642 km 		 Height of Mount Elbrus, highest peak in Europe
    5.727 km 		 Height of Cerro Aucanquilcha, highest road in the world, located in Chile
    5.895 km 		 Height of Mount Kilimanjaro, highest peak in Africa
    6.081 km 		 Height of Mount Logan, highest peak in Canada
    6.194 km 		 Height of Denali, highest peak in North America
    6.959 km 		 Height of Aconcagua, highest peak in South America
    7.5 km 		 Depth of Cayman Trench, deepest point in the Caribbean Sea
    8 km 		 Diameter of Themisto, one of Jupiter's moons
    8 km 		 Diameter of the Vela Pulsar
    8 km 		 Length of Palm Jebel Ali, an artificial island built off the coast of Dubai
    8.6 km 		 Diameter of Callirrhoe, also known as Jupiter XVII
    8.848 km 		 Height of Mount Everest, highest peak on Earth, on the border between Nepal and China
    9.737 km 		 Length of PSR B1919+21
    9.8 km 		 Length of The World, an artificial archipelago that is also built off the coast of Dubai, whose islands resemble a world map
    10 km 		 Diameter of the most massive neutron stars (3-5 solar masses)
    10 km 		 Height of Mauna Kea in Hawaii, measured from its base on the ocean floor
    11 km 		 Average height of the troposphere
    11 km 		 Deepest known point of the ocean, Challenger Deep in the Mariana Trench
    13 km 		 Mean diameter of Deimos, the smaller moon of Mars
    14 km 		 Width of the Gibraltar strait
    18 km 		 Cruising altitude of Concorde
    20 km 		 Diameter of Leda, one of Jupiter's moons
    20 km 		 Diameter of Pan, one of Saturn's moons
    20 km 		 Diameter of the least massive neutron stars (1.44 solar masses)
    21 km 		 Length of Manhattan
    22 km 		 Diameter of Phobos, the larger moon of Mars
    23 km 		 Depth of the largest earthquake ever recorded in the United Kingdom, in 1931 at the Dogger Bank of the North Sea
    27 km 		 Circumference of the Large Hadron Collider, as of May 2010 the largest and highest energy particle accelerator
    27 km 		 Height of Olympus Mons above the Mars reference level, the highest known mountain of the Solar System
    34 km 		 Narrowest width of the English Channel at the Strait of Dover
    34.668 km 		 Highest manned balloon flight (Malcolm D. Ross and Victor E. Prather on 4 May 1961)
    38.422 km 		 Length of the Second Lake Pontchartrain Causeway in Louisiana, US
    39 km 		 Undersea portion of the Channel tunnel
    42.195 km 		 Length of the marathon
    43 km 		 Diameter difference of Earth's equatorial bulge
    50 km 		 Approximate height of the stratosphere
    53.9 km 		 Length of the Seikan Tunnel, as of October 2009, the longest rail tunnel in the world
    66 km 		 Diameter of Naiad, the innermost of Neptune's moons
    77 km 		 Rough total length of the Panama Canal
    90 km 		 Width of the Bering Strait
    100 km 		 The Karman line: the official boundary of outer space
    100 km 		 The altitude at which the FAI defines spaceflight to begin
    105 km 		 Distance from Giridih to Bokaro
    109 km 		 Length of High Speed 1 between London and the Channel Tunnel
    111 km 		 Distance covered by one degree of latitude on Earth's surface
    130 km 		 Range of a Scud-A missile
    163 km 		 Length of the Suez Canal
    164 km 		 Length of the Danyang-Kunshan Grand Bridge
    167 km 		 Diameter of Amalthea, one of Jupiter's inner moons
    180 km 		 Distance between Mumbai and Nashik
    200 km 		 Width of Valles Marineris
    203 km 		 Length of Sognefjorden, the third largest fjord in the world
    213 km 		 Length of Paris Métro
    217 km 		 Length of the Grand Union Canal
    220 km 		 Diameter of Phoebe, the largest of Saturn's outer moons
    220 km 		 Distance between Pune and Nashik
    223 km 		 Length of the Madrid Metro
    240 km 		 Widest width of the English Channel
    300 km 		 Range of a Scud-B missile
    300 km 		 The approximate distance traveled by light in one millisecond
    340 km 		 Diameter of Nereid, the third largest moon of Neptune
    350 km 		 Lower bound of Low Earth orbit
    386 km 		 Altitude of the International Space Station
    408 km 		 Length of the London Underground (active track)
    420 km 		 Diameter of Proteus, the second largest moon of Neptune
    430 km 		 Length of the Pyrenees
    460 km 		 Distance from London to Paris
    468 km 		 Diameter of the asteroid 4 Vesta
    470 km 		 Distance from Dublin to London as the crow flies
    472 km 		 Diameter of Miranda, one of Uranus' major moons
    500 km 		 Widest width of Sweden from east to west
    550 km 		 Distance from San Francisco to Los Angeles as the crow flies
    560 km 		 Distance of Bordeaux-Paris, formerly
    590 km 		 Length of land boundary between Finland and Sweden
    600 km 		 Height above ground of the Hubble Space Telescope
    600 km 		 Range of a Scud-C missile
    724 km 		 Length of the Om River
    804.67 km 		 (500 miles) distance of the Indy 500 automobile race
    871 km 		 Distance from Sydney to Melbourne (along the Hume Highway)
    897 km 		 Length of the River Douro
    900 km 		 Distance from Berlin to Stockholm
    956 km 		 Distance from Washington, DC to Chicago, Illinois as the crow flies
    974.6 km 		 Greatest diameter of 1 Ceres,
    1.000 Mm 		 Estimated shortest axis of triaxial dwarf planet Haumea
    1.010 Mm 		 Distance from San Diego to El Paso as the crow flies
    1.186 Mm 		 Diameter of Charon, the largest moon of Pluto
    1.200 Mm 		 The length of the Paris-Brest-Paris bicycling event
    1.280 Mm 		 Diameter of the trans-Neptunian object 50000 Quaoar
    1.436 Mm 		 Diameter of Iapetus, one of Saturn's major moons
    1.578 Mm 		 Diameter of Titania, the largest of Uranus' moons
    1.960 Mm 		 Estimated longest axis of Haumea
    2.000 Mm 		 Distance from Beijing to Hong Kong as the crow flies
    2.100 Mm 		 Distance from Casablanca to Rome
    2.100 Mm 		 Length of proposed gas pipeline from Iran to India via Pakistan
    2.205 Mm 		 Length of Sweden's total land boundaries
    2.288 Mm 		 Length of the official Alaska Highway when it was built in the 1940s
    2.326 Mm 		 Diameter of the dwarf planet Eris, the largest trans-Neptunian object found to date
    2.376 Mm 		 Diameter of Pluto
    2.515 Mm 		 Length of Norway's total land boundaries
    2.707 Mm 		 Diameter of Triton, largest moon of Neptune
    2.800 Mm 		 Narrowest width of Atlantic Ocean (Brazil-West Africa)
    2.850 Mm 		 Length of the Danube river
    3.069 Mm 		 Length of Interstate 95 (from Houlton, Maine to Miami, Florida)
    3.122 Mm 		 Diameter of Europa, the smallest Galilean satellite of Jupiter
    3.476 Mm 		 Diameter of Earth's Moon
    3.643 Mm 		 Diameter of Io, a moon of Jupiter
    3.690 Mm 		 Length of the Volga river, longest in Europe
    3.846 Mm 		 Length of U.S. Route 1 (from Fort Kent, Maine to Key West, Florida)
    4.350 Mm 		 Length of the Yellow River
    4.800 Mm 		 Widest width of Atlantic Ocean (U.S.-Northern Africa)
    4.821 Mm 		 Diameter of Callisto, a moon of Jupiter
    4.879 Mm 		 Diameter of Mercury
    5.000 Mm 		 Width of the United States
    5.007 Mm 		 Estimated length of Interstate 90 (Seattle, Washington to Boston, Massachusetts)
    5.100 Mm 		 Distance from Dublin to New York as the crow flies
    5.150 Mm 		 Diameter of Titan, the largest moon of Saturn
    5.262 Mm 		 Diameter of Jupiter's moon Ganymede, the largest moon in the solar system
    5.614 Mm 		 Length of the Australian Dingo Fence
    6.270 Mm 		 Length of the Mississippi-Missouri River system
    6.371 Mm 		 Radius of Earth
    6.380 Mm 		 Length of the Yangtze River
    6.4 Mm 		 Length of the Great Wall of China
    6.400 Mm 		 Length of the Amazon River
    6.758 Mm 		 Length of the Nile system, longest on Earth
    6.792 Mm 		 Diameter of Mars
    7.821 Mm 		 Length of the Trans-Canada Highway, the world's longest national highway (from Victoria, British Columbia to St. John's, Newfoundland)
    8.200 Mm 		 Distance from Dublin to San Francisco as the crow flies
    8.836 Mm 		 Road distance between Prudhoe Bay, Alaska, and Key West, Florida, the endpoints of the U.S. road network
    8.852 Mm 		 Aggregate length of the Great Wall of China, including trenches, hills and rivers
    9.259 Mm 		 Length of the Trans-Siberian railway
    10 Mm 		 Approximate altitude of the outer boundary of the exosphere
    10.001 Mm 		 Length of the meridian arc from the North Pole to the Equator (the original definition of the meter was based on this length)
    11.085 Mm 		 Length of the Kiev-Vladivostok railway, a longer variant of the Trans-Siberian railway
    12.000 Mm 		 Diameter of Sirius B, a white dwarf
    12.104 Mm 		 Diameter of Venus
    12.742 Mm 		 Diameter of Earth
    12.900 Mm 		 Minimum distance of the meteoroid 2004 FU162 from the center of Earth on 31 March 2004, closest on record
    13.300 Mm 		 Length of roads being rehabilitated and widened under the National Highway Development Project (launched in 1998) in India
    14.000 Mm 		 Smallest diameter of Jupiter's Great Red Spot
    19.000 Mm 		 Separation between Pluto and Charon
    34.770 Mm 		 Minimum distance of the asteroid 99942 Apophis on 13 April 2029 from the center of Earth
    35.786 Mm 		 Altitude of geostationary orbit
    39.000 Mm 		 Length of the SEA-ME-WE 3 optical submarine telecommunications cable, joining 39 points between Norden, Germany and Okinawa, Japan
    40.005 Mm 		 Polar circumference of the Earth
    40.077 Mm 		 Equatorial circumference of the Earth
    49.528 Mm 		 Diameter of Neptune
    51.118 Mm 		 Diameter of Uranus
    60.000 Mm 		 Total length of the mid-ocean ridges
    67.000 Mm 		 Total length of National Highways in India
    102 Mm 		 Diameter of HD 149026 b, an unusually dense Jovian planet
    111.191 Mm 		 20,000 (nautical, British) leagues (see Jules Verne, Twenty Thousand Leagues Under the Sea)
    115 Mm 		 Width of Saturn's Rings
    120 Mm 		 Diameter of EBLM J0555-57Ab, the smallest known star
    120 Mm 		 Diameter of Saturn
    142 Mm 		 Diameter of Jupiter, the largest planet in the solar system
    170 Mm 		 Diameter of TRAPPIST-1, a star recently discovered to have 7 planets around it
    174 Mm 		 Diameter of OGLE-TR-122b
    180 Mm 		 Average distance covered during life
    196 Mm 		 Diameter of Proxima Centauri, a typical red dwarf
    257 Mm 		 Diameter of TrES-4
    272 Mm 		 Diameter of WASP-12b
    299.792 Mm 		 One light second; the distance light travels in vacuum in one second (see speed of light)
    300 Mm 		 Diameter of WASP-79b
    314 Mm 		 Diameter of CT Cha b
    384.4 Mm 		 Average Earth-Moon distance
    428 Mm 		 Diameter of GQ Lupi b, one of the largest known planets
    671 Mm 		 Separation between Jupiter and Europa
    986 Mm 		 Diameter of HD 100546 b's surrounding disk
    1.2 Gm 		 Separation between Saturn and Titan
    1.39 Gm 		 Diameter of Sun
    1.5 Gm 		 (proposed) Expected orbit from Earth of the James Webb Space Telescope
    2.19 Gm 		 Closest approach of Comet Lexell to Earth, happened on 1 July 1770; closest comet approach on record
    3 Gm 		 Total length of "wiring" in the human brain
    4.2 Gm 		 Diameter of Algol B
    5.0 Gm 		 (proposed) Size of the arms of the giant triangle shaped Michelson interferometer of the Laser Interferometer Space Antenna (LISA) planned to start observations sometime in the 2030s
    5.0 Gm 		 Closest approach of Comet Halley to Earth, happened on 10 April 837
    7.9 Gm 		 Diameter of Gamma Orionis
    9.0 Gm 		 Estimated diameter of the event horizon of Sagittarius A*, the supermassive black hole in the center of the Milky Way galaxy
    15 Gm 		 Closest distance of Comet Hyakutake from Earth
    18 Gm 		 One light-minute (see yellow sphere in right-hand diagram)
    24 Gm 		 Radius of a heliostationary orbit
    46 Gm 		 Perihelion distance of Mercury (yellow ellipse on the right)
    55 Gm 		 60,000-year perigee of Mars (last achieved on 27 August 2003)
    55 Gm 		 Radius of Rigel, a blue supergiant star (largest star on right)
    58 Gm 		 Average passing distance between Earth and Mars at the moment they overtake each other in their orbits
    61 Gm 		 Diameter of Aldebaran, an orange giant star (large star on right)
    70 Gm 		 Aphelion distance of Mercury
    76 Gm 		 Neso's apocentric distance; greatest distance of a natural satellite from its parent planet (Neptune)
    109 Gm 		 Distance between Venus and the Sun
    149.6 Gm 		 Distance between the Earth and the Sun - the definition of the astronomical unit
    180 Gm 		 Maximum diameter of Sagittarius A*, the supermassive black hole in the center of Milky Way galaxy
    228 Gm 		 Distance between Mars and the Sun
    570 Gm 		 Length of the tail of Comet Hyakutake measured by Ulysses; the actual value could be much higher
    591 Gm 		 Minimum distance between the Earth and Jupiter
    780 Gm 		 Distance between Jupiter and the Sun
    947 Gm 		 Diameter of Antares A
    965 Gm 		 Maximum distance between the Earth and Jupiter
    1.079 Tm 		 One light-hour
    1.4 Tm 		 Distance between Saturn and the Sun
    1.5 Tm 		 Estimated diameter of VV Cephei A, a red supergiant
    1.83 Tm 		 Diameter of HR 5171 A, the largest known yellow hypergiant star although the latest research suggests it is a red hypergiant with a diameter about 2.1 Tm (14 AU)
    2 Tm 		 Estimated diameter of VY Canis Majoris, one of the largest known stars
    2.9 Tm 		 Distance between Uranus and the Sun
    4 Tm 		 Previous estimated diameter of VY Canis Majoris based on direct measurements of the radius at infrared wavelengths
    4.4 Tm 		 Perihelion distance of Pluto
    4.5 Tm 		 Distance between Neptune and the Sun
    4.5 Tm 		 Inner radius of the Kuiper belt
    5.7 Tm 		 Perihelion distance of Eris
    7.3 Tm 		 Aphelion distance of Pluto
    7.5 Tm 		 Outer radius of the Kuiper Belt, inner boundary of the Oort Cloud
    10 Tm 		 Diameter of a hypothetical Quasi-star
    11.1 Tm 		 Distance that Voyager 1 began detecting returning particles from termination shock
    11.4 Tm 		 Perihelion distance of 90377 Sedna
    12.1 Tm 		 Distance to termination shock (Voyager 1 crossed at 94 AU)
    12.9 Tm 		 Distance to 90377 Sedna in March 2014
    13.2 Tm 		 Distance to Pioneer 11 in March 2014
    14.1 Tm 		 Estimated radius of the solar system
    14.4 Tm 		 Distance to Eris in March 2014 (now near its aphelion)
    15.1 Tm 		 Distance to heliosheath
    16.5 Tm 		 Distance to Pioneer 10 as of March 2014
    16.6 Tm 		 Distance to Voyager 2 as of May 2016
    20.0 Tm 		 Distance to Voyager 1 as of May 2016
    20.6 Tm 		 Distance to Voyager 1 as of late February 2017
    21.1 Tm 		 Distance to Voyager 1 as of November 2017
    25.9 Tm 		 One light-day
    55.7 Tm 		 Aphelion distance of the comet Hale-Bopp
    146 Tm 		 Aphelion distance of 90377 Sedna
    172 Tm 		 Schwarzschild diameter of H1821+643, one of the most massive black holes known
    181 Tm 		 One light-week
    653 Tm 		 Aphelion distance of comet Hyakutake (current orbit)
    757 Tm 		 Radius of the Stingray Nebula
    777 Tm 		 One light-month
    7.5 Pm 		 Possible outer boundary of Oort cloud (other estimates are 75,000 to 125,000 or even 189,000 AU (1.18, 2, and 3 light years, respectively))
    7.7 Pm 		 Aphelion distance of the Great Daylight Comet of 1910
    9.5 Pm 		 One light year, the distance traveled by light in one year
    15 Pm 		 Possible outer radius of Oort cloud
    20 Pm 		 Maximum extent of influence of the Sun's gravitational field
    30.9 Pm 		 1 parsec
    39.9 Pm 		 Distance to Proxima Centauri (nearest star to Sun)
    81.3 Pm 		 Distance to Sirius
    110 Pm 		 Distance to Tau Ceti
    230 Pm 		 Diameter of the Orion Nebula
    240 Pm 		 Distance to Vega
    260 Pm 		 Distance to Chara, a star approximately as bright as our Sun. Its faintness gives us an idea how our Sun would appear when viewed from even so close a distance as this
    350 Pm 		 Distance to Arcturus
    373.1 Pm 		 Distance to TRAPPIST-1, a star recently discovered to have 7 planets around it
    400 Pm 		 Distance to Capella
    620 Pm 		 Distance to Aldebaran
    750 Pm 		 Distance to Regulus
    900 Pm 		 Distance to Algol
    1.2 Em 		 Diameter of Messier 13 (a typical globular cluster)
    1.6 Em 		 Diameter of Omega Centauri (one of the largest known globular clusters, perhaps containing over a million stars)
    3.1 Em 		 Distance to Canopus according to Hipparcos
    5.7 Em 		 Diameter of the Tarantula Nebula
    6.1 Em 		 Distance to Betelgeuse according to Hipparcos
    6.2 Em 		 Distance to the Helix Nebula, located in the constellation Aquarius
    7.3 Em 		 Distance to Rigel according to Hipparcos
    13 Em 		 Distance to the Orion Nebula
    14 Em 		 Approximate thickness of the plane of the Milky Way galaxy at the Sun's location
    14.2 Em 		 Diameter of the NGC 604
    30.8568 Em 		 1 kiloparsec
    31 Em 		 Distance to Deneb according to Hipparcos
    46 Em 		 Distance to OGLE-TR-56, the first extrasolar planet discovered using the transit method
    47 Em 		 Distance to the Boomerang nebula, coldest place known (1 K)
    53 Em 		 Distance to the globular cluster M4 and the extrasolar planet PSR B1620-26 b within it
    61 Em 		 Distance to Perseus Spiral Arm (next spiral arm out in the Milky Way galaxy)
    71 Em 		 Distance to Eta Carinae
    150 Em 		 Diameter of the Small Magellanic Cloud, a dwarf galaxy orbiting the Milky Way
    200 Em 		 Distance to OGLE-2005-BLG-390Lb, the most distant and the most Earth-like planet known
    240 Em 		 Distance to the Canis Major Dwarf Galaxy
    260 Em 		 Distance to the center of the Galaxy
    830 Em 		 Distance to the Sagittarius Dwarf Elliptical Galaxy
    1.4 to 1.9 Zm 		 Estimated diameter of the disk of the Milky Way Galaxy. The size was previously thought to be half of this
    1.7 Zm 		 Distance to the Large Magellanic Cloud, largest satellite galaxy of the Milky Way
    2.0 Zm 		 Distance to the Small Magellanic Cloud
    2.8 Zm 		 Distance to the Intergalactic Wanderer, one of the most distant globular clusters of Milky Way
    8.5 Zm 		 Distance to the Leo I Dwarf Galaxy, farthest known Milky Way satellite galaxy
    24 Zm 		 Distance to the Andromeda Galaxy
    30.8568 Zm 		 1 megaparsec
    40 Zm 		 Distance to the IC 10, a distant member of the Local Group of galaxies
    49.2 Zm 		 Width of the Local Group of galaxies
    57 Zm 		 Diameter of the supergiant elliptical galaxy IC 1101
    95 Zm 		 Distance to the Maffei 1, the nearest giant elliptical galaxy in the Maffei 1 Group
    95 Zm 		 Distance to the Sculptor Galaxy in the Sculptor Group of galaxies
    140 Zm 		 Distance to Centaurus A galaxy
    250 Zm 		 Distance to the Pinwheel Galaxy
    280 Zm 		 Distance to the Sombrero Galaxy
    570 Zm 		 Approximate distance to the Virgo cluster, nearest galaxy cluster
    620 Zm 		 Approximate distance to the Fornax cluster
    800 Zm 		 Approximate distance to the Eridanus cluster
    1.2 Ym 		 Distance to the closest observed gamma ray burst GRB 980425
    1.3 Ym 		 Distance to the Centaurus Cluster of galaxies, the nearest large supercluster
    1.9 Ym 		 Diameter of the Local Supercluster
    2.3 Ym 		 Distance light travels in vacuum in one galactic year
    2.8 Ym 		 Distance to the Coma Cluster
    3.2 Ym 		 Distance to the Stephan's Quintet
    4.7 Ym 		 Length of the CfA2 Great Wall, one of the largest observed superstructures in the Universe
    6.1 Ym 		 Distance to the Shapley Supercluster
    9.5 Ym 		 Diameter of the Eridanus Supervoid
    13.7 Ym 		 Length of the Sloan Great Wall
    18 Ym 		 Redshift 0.16 - Distance to the quasar 3C 273 (light travel distance)
    33 Ym 		 Maximum distance of the 2dF Galaxy Redshift Survey (light travel distance)
    37.8 Ym 		 Length of the Huge-LQG
    75 Ym 		 Redshift 0.95 - Approximate distance to the supernova SN 2002dd in the Hubble Deep Field North (light travel distance)
    85 Ym 		 Redshift 1.6 - Approximate distance to the gamma ray burst GRB 990123 (light travel distance)
    94.6 Ym 		 Approximate distance to quasar OQ172
    94.6 Ym 		 Length of the Hercules-Corona Borealis Great Wall, one of the largest and most massive known cosmic structure
    130 Ym 		 Redshift 1000 - Distance (LTD) to the source of the cosmic microwave background radiation; radius of the observable universe measured as a LTD
    130 Ym 		 Redshift 6.41 - Light travel distance (LTD) to the quasar SDSS J1148+5251
    260 Ym 		 Diameter of the observable universe (double LTD)
    440 Ym 		 Radius of the universe measured as a comoving distance
    590 Ym 		 Cosmological event horizon: the largest comoving distance from which light will ever reach us (the observer) at any time in the future
    886.48 Ym 		 The diameter of the observable universe (twice the particle horizon); however, there might be unobserved distances that are even greater

    ''')
if 1:  # Classes
    class Num(flt):
        '''Encapsulate a number so "closeness" can be determined by the ==
        operator.  A list of Num objects will sort numerically by size.
        
        Note:  since I changed this to derive from flt, I had to change the
        low and high attributes of Num to Low and High to avoid the collision
        with flt's attributes.
        '''
        def __new__(cls, s, descr):
            '''descr is a string describing this number.
     
            s is a string representing the number.  It will be of one of
            the forms
                'a to b'
                '~a to b'
                'a'
                '<a'
                '~a'
            The '~' is ignored.  The 'a to b' form has the self.Low and
            self.High values set from a and b.  Otherwise, the value is set
            from a.  Note a will be of the form e.g. '1 nm', i.e., a number and
            a length unit.
     
            The value of a Num is the length in m.  When a range is given, the
            mean of the endpoints is the value.
            '''
            t = s
            if s[0] == "~":
                t = t[1:]
            if "to" in t:
                f = t.split()
                assert(len(f) == 4)
                assert(f[1] == "to") 
                unit = f[3]
                toSI = u.u(unit)
                Low, High = [float(i) for i in (f[0], f[2])]
                val = (Low + High)*toSI/2
                instance = flt.__new__(cls, val)
                instance.units = unit
                instance.Low = Low*toSI
                instance.High = High*toSI
            else:
                val, unit = u.ParseUnit(t)
                toSI = u.u(unit)
                instance = flt.__new__(cls, float(val)*toSI)
                instance.units = unit
                instance.Low = None
                instance.High = None
            instance.str = s.strip()
            instance.descr = descr.strip()
            return instance
        def __str__(self):
            return self.str + " " + self.descr
        def __repr__(self):
            return self.str + " " + self.descr
        def __eq__(self, other):
            '''Return True if we're equal to other.  If self is a single
            number, then it's True if other is within d["-t"] percent of it.
            Otherwise, it's equal if self.Low <= other <= self.High.
            '''
            if other is None:
                return False
            assert(ii(other, Num))
            if self.Low is None:
                p = flt(d["-t"])/100
                return (1 - p)*self <= other <= (1 + p)*self
            else:
                return self.Low <= other <= self.High
        def __lt__(self, other):
            'Return True if self < other'
            assert(ii(other, Num))
            # This depends on the floating point value being in m
            return float(self) < float(other)
if 1:  # Utility
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] dist1 [dist2 ...]
          Print the order of magnitude distance data for distances close to dist1, dist2, etc.  Default
          units are meters, but you can include another unit with no space between it and the number.
          If a dist argument can't be converted to a dimensioned number, it's a string that is
          searched for in the descriptions.  Unless -n is used, a 1-figure number in meters in
          scientific notation is in parentheses to help interpret SI prefixes used.
        Options:
          -d n    Number of significant figures to display
          -n      Do not display number in meters
          -m      Dump the raw data to stdout and exit
          -t n    Set % tolerance to be "equal" [{d["-t"]}]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 3         # Number of significant digits
        d["-m"] = False     # Dump data to stdout
        d["-n"] = True      # Display in meters numerically too
        d["-t"] = 50        # Tolerance to be "equal"
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:mnt")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("nm"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                           "1 and 15")
                    Error(msg)
            elif o in ("-t",):
                try:
                    d["-t"] = flt(a)
                    if d["-t"] <= 0:
                        raise ValueError()
                except ValueError:
                    msg = ("-t option must be > 0")
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(d, status=0)
        flt(0).n = d["-d"]
        flt(0).rtz = True
        if d["-m"]:
            GetData(show_sorted=True)
            exit(0)
        if not args:
            Usage(d)
        return args
if 1:  # Core functionality
    def ParseDistance(s):
        'Return distance string in s in m'
        f = s.split()
        if "to" in s:
            print(s)
        elif s[0] == "<":
            print(s)
        elif s[0] == "~":
            print(s)
        else:
            pass
        return 1
    def GetData(show_sorted=False):
        '''Put data into d["data"].  If show_sorted is True, then the input
        lines are sorted by size, printed to stdout, and the script exits.
        '''
        # d["data"] is a list of Num objects
        for line in data.split("\n"):
            line = line.strip()
            if not line:
                continue
            a, b = line.split("\t\t")
            x = Num(a, b)
            if show_sorted:
                d["data"].append((flt(float(x)), line))
            else:
                d["data"].append(x)
        if show_sorted:
            d["data"] = list(sorted(d["data"]))
            for i in d["data"]:
                print(i[1])
            exit()
    def Print(x, r=None):
        '''x is a Num object; print it.  If r is not None, then it will be
        the regex that matched x.descr.
        '''
        def sci(x):
            y = float(x)  # This is in m
            a, b = f"{y:.0e}".split("e")
            return ''.join([a, "e", str(int(b))])
        if r is None:
            # The number matched
            print(" ", x.str, end=" ")
            if d["-n"]:
                print(f"({sci(x)})", end=" ")
            print(x.descr)
        else:
            # The regex matched
            print(" ", x.str, end=" ")
            if d["-n"]:
                print(f"({sci(x)})", end=" ")
            print(x.descr)
            #C.PrintMatch(x.descr, r)
    def PrintClose(dist):
        '''dist is a command line argument.  Convert it to meters and print out
        those elements in d["data"] that are close to it.
        '''
        class DoTextSearch(Exception): pass
        try:
            val, unit = u.ParseUnit(dist)
            if not unit:
                m =Num(val + " m", "")
            elif u.dim(unit) != u.dim("m"):
                raise DoTextSearch()  # Just do a text search
            else:
                # It has a unit, so use as-is
                m = Num(dist, "")
            search = False
        except (DoTextSearch, TypeError):
            search, m = True, None
            r = re.compile(dist, re.I)
        print(dist)
        for x in d["data"]:
            if x == m:
                Print(x)
            elif search and r.search(x.descr):
                Print(x, r=r)

if __name__ == "__main__":
    d = {  # Options dictionary
        "data": [],
    }
    distances = ParseCommandLine(d)
    GetData()
    for dist in distances:
        PrintClose(dist)
