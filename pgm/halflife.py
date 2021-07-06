'''
Half-lives for various radionuclides
    A module to provide half-lives for various radionuclides.  halflife
    is a dictionary keyed by the element's symbol.  The values are
    dictionaries whose keys are the isotope numbers (note some of them
    have an appended 'm' for metastable states).  The half-life value is
    a string in seconds rounded to _ndigits significant figures.
 
    Data taken from the web page http://www.iem-inc.com/toolhalf.html.
    The web page's data were copied to a file; the file was sorted and
    only the relevant lines containing half-lives were retained.  Update
    17 Feb 2016:  the web page's data are no longer copyable to a file.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Program description string
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from f import flt
    from sig import sig
    if 1:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    # Dictionary to convert element symbols to names.  Note these are only
    # those elements that are in the halflife dictionary.
    elements = {
        "Ac" : "Actinium",
        "Ag" : "Silver",
        "Am" : "Americium",
        "Ar" : "Argon",
        "At" : "Astatine",
        "Au" : "Gold",
        "Ba" : "Barium",
        "Be" : "Beryllium",
        "Bi" : "Bismuth",
        "Bk" : "Berkelium",
        "Br" : "Bromine",
        "C"  : "Carbon",
        "Ca" : "Calcium",
        "Cd" : "Cadmium",
        "Ce" : "Cerium",
        "Cf" : "Californium",
        "Cl" : "Chlorine",
        "Cm" : "Curium",
        "Co" : "Cobalt",
        "Cr" : "Chromium",
        "Cs" : "Cesium",
        "Cu" : "Copper",
        "Eu" : "Europium",
        "F"  : "Fluorine",
        "Fe" : "Iron",
        "Fr" : "Francium",
        "Ga" : "Gallium",
        "Gd" : "Gadolinium",
        "H"  : "Hydrogen",
        "Hg" : "Mercury",
        "Ho" : "Holmium",
        "I"  : "Iodine",
        "In" : "Indium",
        "Ir" : "Iridium",
        "K"  : "Potassium",
        "Kr" : "Krypton",
        "La" : "Lanthanum",
        "Mn" : "Manganese",
        "Mo" : "Molybdenum",
        "N"  : "Nitrogen",
        "Na" : "Sodium",
        "Nb" : "Niobium",
        "Nd" : "Neodymium",
        "Ni" : "Nickel",
        "Np" : "Neptunium",
        "O"  : "Oxygen",
        "P"  : "Phosphorus",
        "Pa" : "Protactinium",
        "Pb" : "Lead",
        "Pd" : "Palladium",
        "Pm" : "Promethium",
        "Po" : "Polonium",
        "Pr" : "Praseodymium",
        "Pu" : "Plutonium",
        "Ra" : "Radium",
        "Rb" : "Rubidium",
        "Re" : "Rhenium",
        "Rh" : "Rhodium",
        "Rn" : "Radon",
        "Ru" : "Ruthenium",
        "S"  : "Sulfur",
        "Sb" : "Antimony",
        "Sc" : "Scandium",
        "Se" : "Selenium",
        "Sm" : "Samarium",
        "Sn" : "Tin",
        "Sr" : "Strontium",
        "Tb" : "Terbium",
        "Tc" : "Technetium",
        "Te" : "Tellurium",
        "Th" : "Thorium",
        "Tl" : "Thallium",
        "U"  : "Uranium",
        "V"  : "Vanadium",
        "W"  : "Tungsten",
        "Xe" : "Xenon",
        "Y"  : "Yttrium",
        "Yb" : "Ytterbium",
        "Zn" : "Zinc",
        "Zr" : "Zirconium"
    }
    # Dictionary to convert element names to symbols.
    Elements = {
        "Actinium"     : "Ac",
        "Americium"    : "Am",
        "Antimony"     : "Sb",
        "Argon"        : "Ar",
        "Astatine"     : "At",
        "Barium"       : "Ba",
        "Berkelium"    : "Bk",
        "Beryllium"    : "Be",
        "Bismuth"      : "Bi",
        "Bromine"      : "Br",
        "Cadmium"      : "Cd",
        "Calcium"      : "Ca",
        "Californium"  : "Cf",
        "Carbon"       : "C",
        "Cerium"       : "Ce",
        "Cesium"       : "Cs",
        "Chromium"     : "Cr",
        "Chlorine"     : "Cl",
        "Cobalt"       : "Co",
        "Copper"       : "Cu",
        "Curium"       : "Cm",
        "Europium"     : "Eu",
        "Fluorine"     : "F",
        "Francium"     : "Fr",
        "Gadolinium"   : "Gd",
        "Gallium"      : "Ga",
        "Gold"         : "Au",
        "Holmium"      : "Ho",
        "Hydrogen"     : "H",
        "Indium"       : "In",
        "Iodine"       : "I",
        "Iridium"      : "Ir",
        "Iron"         : "Fe",
        "Krypton"      : "Kr",
        "Lanthanum"    : "La",
        "Lead"         : "Pb",
        "Manganese"    : "Mn",
        "Mercury"      : "Hg",
        "Molybdenum"   : "Mo",
        "Neodymium"    : "Nd",
        "Neptunium"    : "Np",
        "Nickel"       : "Ni",
        "Niobium"      : "Nb",
        "Nitrogen"     : "N",
        "Oxygen"       : "O",
        "Palladium"    : "Pd",
        "Phosphorus"   : "P",
        "Plutonium"    : "Pu",
        "Polonium"     : "Po",
        "Potassium"    : "K",
        "Praseodymium" : "Pr",
        "Promethium"   : "Pm",
        "Protactinium" : "Pa",
        "Radium"       : "Ra",
        "Radon"        : "Rn",
        "Rhenium"      : "Re",
        "Rhodium"      : "Rh",
        "Rubidium"     : "Rb",
        "Ruthenium"    : "Ru",
        "Samarium"     : "Sm",
        "Scandium"     : "Sc",
        "Selenium"     : "Se",
        "Silver"       : "Ag",
        "Sodium"       : "Na",
        "Strontium"    : "Sr",
        "Sulfur"       : "S",
        "Technetium"   : "Tc",
        "Tellurium"    : "Te",
        "Terbium"      : "Tb",
        "Thallium"     : "Tl",
        "Thorium"      : "Th",
        "Tin"          : "Sn",
        "Tungsten"     : "W",
        "Uranium"      : "U",
        "Vanadium"     : "V",
        "Xenon"        : "Xe",
        "Ytterbium"    : "Yb",
        "Yttrium"      : "Y",
        "Zinc"         : "Zn",
        "Zirconium"    : "Zr",
        "Aluminum"     : "Al",
        "Dysprosium"   : "Dy",
        "Hafnium"      : "Hf",
        "Lutetium"     : "Lu",
        "Platinum"     : "Pt",
        "Osmium"       : "Os",
        "Tantalum"     : "Ta",
    }
    data1 = '''
        Ac-225, 10.0 days
        Ac-227, 21.773 years
        Ac-228, 6.13 hours
        Ag-110, 24.6 seconds
        Ag-110m, 249.9 days
        Ag-111, 7.45 days
        Am-241, 432.2 years
        Am-242, 16.02 hours
        Am-242m, 152 years
        Am-243, 7380 years
        Ar-41, 1.827 hours
        At-217, 0.0323 seconds
        At-218, 2 seconds
        Au-198, 2.696 days
        Ba-137m, 2.552 minutes
        Ba-139, 82.7 minutes
        Ba-140, 12.74 days
        Ba-141, 18.27 minutes
        Ba-142, 10.6 minutes
        Be-10, 1.6E6 years
        Be-7, 53.44 days
        Bi-210, 5.012 days
        Bi-211, 2.14 minutes
        Bi-212, 60.55 minutes
        Bi-213, 45.65 minutes
        Bi-214, 19.9 minutes
        Br-82, 35.30 hours
        Br-83, 2.39 hours
        Br-84, 31.80 minutes
        C-11, 20.38 minutes
        C-14, 5730 years
        Ca-41, 1.3E5 years
        Ca-47, 4.53 days
        Cd-113m, 13.6 years
        Cd-115m, 44.6 days
        Ce-141, 32.50 days
        Ce-143, 33.0 hours
        Ce-144, 284.3 days
        Cf-252, 2.638 years
        Cm-242, 162.8 days
        Cm-243, 28.5 years
        Cm-244, 18.11 years
        Cm-245, 8500 years
        Cm-246, 4730 years
        Cm-247, 1.56E7 years
        Cm-248, 3.39E5 years
        Co-56, 78.76 days
        Co-57, 270.9 days
        Co-58, 70.8 days
        Co-60, 5.27 years
        Cr-51, 27.704 days
        Cs-134, 2.062 years
        Cs-134m, 2.90 hours
        Cs-135, 2.3E6 years
        Cs-136, 13.1 days
        Cs-137, 30.0 years
        Cs-138, 32.2 minutes
        Cu-61, 3.408 hours
        Cu-64, 12.701 hours
        Eu-152, 13.33 years
        Eu-154, 8.8 years
        Eu-155, 4.96 years
        Eu-156, 15.19 days
        F-18, 109.74 minutes
        Fe-55, 2.7 years
        Fe-59, 44.53 days
        Fr-221, 4.8 minutes
        Fr-223, 21.8 minutes
        Ga-67, 3.261 days
        Gd-152, 1.08E14 years
        H-3, 12.35 years
        Hg-197, 64.1 hours
        Hg-203, 46.60 days
        Ho-166m, 1.20E3 years
        I-123, 13.2 hours
        I-125, 60.14 days
        I-129, 1.57E7 years
        I-130, 12.36 hours
        I-131, 8.04 days
        I-132, 2.30 hours
        I-133, 20.8 hours
        I-134, 52.6 minutes
        I-135, 6.61 hours
        In-111, 2.83 days
        In-113, 1.658 hours
        In-115, 5.1E15 years
        Ir-192, 74.02 days
        K-40, 1.27E9 years
        K-42, 12.36 hours
        K-43, 22.6 hours
        Kr-83m, 1.83 hours
        Kr-85, 10.72 years
        Kr-85m, 4.48 hours
        Kr-87, 76.3 minutes
        Kr-88, 2.84 minutes
        La-140, 40.272 hours
        La-141, 3.93 hours
        La-142, 92.5 minutes
        Mn-52, 5.591 days
        Mn-52m, 21.1 minutes
        Mn-54, 312.5 days
        Mn-56, 2.579 hours
        Mn-57, 36.08 hours
        Mo-93, 3.5E3 years
        Mo-99, 66.0 hours
        N-13, 9.97 minutes
        N-16, 7.13 seconds
        Na-22, 2.602 years
        Na-24, 15.00 hours
        Nb-93m, 13.6 years
        Nb-95, 35.15 days
        Nb-95m, 86.6 hours
        Nb-97, 72.1 minutes
        Nb-97m, 60 seconds
        Nd-147, 10.98 days
        Ni-59, 7.5E4 years
        Ni-63, 96 years
        Ni-65, 2.520 hours
        Np-237, 2.14E6 years
        Np-238, 2.117 days
        Np-239, 2.355 days
        Np-240, 65 minutes
        Np-240m, 7.4 minutes
        O-15, 122.24 seconds
        P-32, 14.29 days
        Pa-231, 3.28E4 years
        Pa-233, 27.0 days
        Pa-234, 6.70 hours
        Pa-234m, 1.17 minutes
        Pb-209, 3.253 hours
        Pb-210, 22.3 years
        Pb-211, 36.1 minutes
        Pb-212, 10.64 hours
        Pb-214, 26.8 minutes
        Pb-214, 26.8 minutes
        Pd-107, 6.5E6 years
        Pd-109, 13.427 hours
        Pm-147, 2.6234 years
        Pm-148, 41.3 days
        Pm-148, 5.37 days
        Pm-149, 53.08 hours
        Pm-151, 28.40 hours
        Po-210, 138.38 days
        Po-211, 0.516 seconds
        Po-212, 0.305 microseconds
        Po-213, 4.2 microseconds
        Po-214, 164.3 microseconds
        Po-215, 0.00178 seconds
        Po-216, 0.15 seconds
        Po-218, 3.05 minutes
        Pr-143, 13.56 days
        Pr-144, 17.28 minutes
        Pr-144m, 7.2 minutes
        Pu-238, 87.74 years
        Pu-239, 24065 years
        Pu-240, 6537 years
        Pu-241, 14.4 years
        Pu-242, 3.76E5 years
        Pu-243, 4.956 hours
        Pu-244, 8.26E7 years
        Ra-223, 11.434 days
        Ra-224, 3.66 days
        Ra-225, 14.8 days
        Ra-226, 1600 years
        Ra-228, 5.75 years
        Rb-86, 18.66 days
        Rb-87, 4.7E10 years
        Rb-88, 17.8 minutes
        Rb-89, 15.2 minutes
        Re-187, 5E10 years
        Rh-103m, 56.12 minutes
        Rh-105, 35.36 hours
        Rh-106, 29.9 seconds
        Rn-219, 3.96 seconds
        Rn-220, 55.6 seconds
        Rn-222, 3.824 days
        Ru-103, 39.28 days
        Ru-105, 4.44 hours
        Ru-106, 368.2 days
        Ru-97, 2.9 days
        S-35, 87.44 days
        Sb-124, 60.20 days
        Sb-125, 2.77 years
        Sb-126, 12.4 days
        Sb-126m, 19.0 minutes
        Sb-127, 3.85 days
        Sc-44, 3.927 hours
        Sc-46, 83.83 days
        Sc-47, 3.351 days
        Sc-48, 43.7 hours
        Se-75, 119.78 days
        Se-79, 65000 years
        Sm-147, 1.06E11 years
        Sm-151, 90 years
        Sm-153, 46.7 hours
        Sn-119m, 293.1 days
        Sn-123, 129.2 days
        Sn-125, 9.64 days
        Sn-126, 1.0E5 years
        Sr-85, 64.84 days
        Sr-87m, 2.81 hours
        Sr-89, 50.5 days
        Sr-90, 29.12 years
        Sr-91, 9.5 hours
        Sr-92, 2.71 hours
        Tb-160, 72.3 days
        Tc-101, 14.2 minutes
        Tc-99, 2.13E5 years
        Tc-99m, 6.02 hours
        Te-125m, 58 days
        Te-127, 9.35 hours
        Te-127m, 109 days
        Te-129, 69.6 minutes
        Te-129m, 33.6 days
        Te-131, 25.0 minutes
        Te-131m, 30 hours
        Te-132, 78.2 hours
        Te-133, 12.45 minutes
        Te-133m, 55.4 minutes
        Te-134, 41.8 minutes
        Th-227, 18.718 days
        Th-228, 1.913 years
        Th-229, 7340 years
        Th-230, 7.7E4 years
        Th-231, 25.52 hours
        Th-232, 1.41E10 years
        Th-234, 24.10 days
        Tl-201, 73.06 hours
        Tl-207, 4.77 minutes
        Tl-208, 3.07 minutes
        Tl-209, 2.20 minutes
        U-232, 72 years
        U-233, 1.59E5 years
        U-234, 2.445E5 years
        U-235, 7.03E8 years
        U-236, 2.34E7 years
        U-237, 6.75 days
        U-238, 4.47E9 years
        U-240, 14.1 hours
        V-48, 16.238 days
        W-181, 121.2 days
        W-185, 75.1 days
        W-187, 23.9 hours
        Xe-131m, 11.9 days
        Xe-133, 5.245 days
        Xe-133m, 2.188 days
        Xe-135, 9.09 hours
        Xe-135m, 15.29 minutes
        Xe-138, 14.17 minutes
        Y-90, 64.0 hours
        Y-91, 58.51 days
        Y-91m, 49.71 minutes
        Y-92, 3.54 hours
        Y-93, 10.1 hours
        Yb-169, 32.01 days
        Zn-65, 243.9 days
        Zn-69, 57 minutes
        Zr-93, 1.53E6 years
        Zr-95, 63.98 days
        Zr-97, 16.90 hours
    '''[1:-1]

    atomic_data = {
        # Symbol, atomic number, atomic mass
        "H": (1, "1.00797"),
        "He": (2, "4.00260"),
        "Li": (3, "6.941"),
        "Be": (4, "9.01218"),
        "B": (5, "10.81"),
        "C": (6, "12.011"),
        "N": (7, "14.0067"),
        "O": (8, "15.9994"),
        "F": (9, "18.998403"),
        "Ne": (10, "20.179"),
        "Na": (11, "22.98977"),
        "Mg": (12, "24.305"),
        "Al": (13, "26.98154"),
        "Si": (14, "28.0855"),
        "P": (15, "30.97376"),
        "S": (16, "32.06"),
        "Cl": (17, "35.453"),
        "Ar": (18, "39.948"),
        "K": (19, "39.0983"),
        "Ca": (20, "40.08"),
        "Sc": (21, "44.9559"),
        "Ti": (22, "47.90"),
        "V": (23, "50.9415"),
        "Cr": (24, "51.996"),
        "Mn": (25, "54.9380"),
        "Fe": (26, "55.847"),
        "Co": (27, "58.9332"),
        "Ni": (28, "58.70"),
        "Cu": (29, "63.546"),
        "Zn": (30, "65.38"),
        "Ga": (31, "69.72"),
        "Ge": (32, "72.59"),
        "As": (33, "74.9216"),
        "Se": (34, "78.96"),
        "Br": (35, "79.904"),
        "Kr": (36, "83.80"),
        "Rb": (37, "85.4678"),
        "Sr": (38, "87.62"),
        "Y": (39, "88.9059"),
        "Zr": (40, "91.22"),
        "Nb": (41, "92.9064"),
        "Mo": (42, "95.94"),
        "Tc": (43, "(98)"),
        "Ru": (44, "101.07"),
        "Rh": (45, "102.9055"),
        "Pd": (46, "106.4"),
        "Ag": (47, "107.868"),
        "Cd": (48, "112.41"),
        "In": (49, "114.82"),
        "Sn": (50, "118.69"),
        "Sb": (51, "121.75"),
        "Te": (52, "127.60"),
        "I": (53, "126.9045"),
        "Xe": (54, "131.30"),
        "Cs": (55, "132.9054"),
        "Ba": (56, "137.33"),
        "La": (57, "138.9055"),
        "Ce": (58, "140.12"),
        "Pr": (59, "140.9077"),
        "Nd": (60, "144.24"),
        "Pm": (61, "(145)"),
        "Sm": (62, "150.4"),
        "Eu": (63, "151.96"),
        "Gd": (64, "157.25"),
        "Tb": (65, "158.9254"),
        "Dy": (66, "162.50"),
        "Ho": (67, "164.9304"),
        "Er": (68, "167.26"),
        "Tm": (69, "168.9342"),
        "Yb": (70, "173.04"),
        "Lu": (71, "174.967"),
        "Hf": (72, "178.49"),
        "Ta": (73, "180.9479"),
        "W": (74, "183.85"),
        "Re": (75, "186.207"),
        "Os": (76, "190.2"),
        "Ir": (77, "192.22"),
        "Pt": (78, "195.09"),
        "Au": (79, "196.9665"),
        "Hg": (80, "200.59"),
        "Tl": (81, "204.37"),
        "Pb": (82, "207.2"),
        "Bi": (83, "208.9804"),
        "Po": (84, "(209)"),
        "At": (85, "(210)"),
        "Rn": (86, "(222)"),
        "Fr": (87, "(223)"),
        "Ra": (88, "226.0254"),
        "Ac": (89, "227.0278"),
        "Th": (90, "232.0381"),
        "Pa": (91, "231.0359"),
        "U": (92, "238.029"),
        "Np": (93, "237.0482"),
        "Pu": (94, "(242)"),
        "Am": (95, "(243)"),
        "Cm": (96, "(247)"),
        "Bk": (97, "(247)"),
        "Cf": (98, "(251)"),
        "Es": (99, "(252)"),
        "Fm": (100, "(257)"),
        "Md": (101, "(258)"),
        "No": (102, "(250)"),
        "Lr": (103, "(260)"),
        "Rf": (104, "(261)"),
        "Db": (105, "(262)"),
        "Sg": (106, "(263)"),
        "Bh": (107, "(262)"),
        "Hs": (108, "(255)"),
        "Mt": (109, "(256)"),
        "Ds": (110, "(269)"),
        "Rg": (111, "(272)"),
    }
def ProcessData():
    '''Return a dictionary indexed by the atomic symbol of the
    element.  Each value will be a dictionary of the half-life in
    seconds indexed by the isotope number.
    '''
    t = {
        "seconds"  : 1,
        "days"  : 24*3600,
        "years"  : 31556925.97,
        "hours"  : 3600,
        "microseconds"  : 1e6,
        "minutes"  : 60,
    }
    d, x = {}, flt(0)
    x.n = 4         # Assume half-life's to 4 figures
    x.rtz = True    # Remove trailing zeros
    for line in data1.split("\n") :
        if not line.strip():
            continue
        name, halflife = line.strip().split(",")
        element, isotope = [i.strip() for i in name.split("-")]
        num, unit = halflife.split()
        if unit == "microseconds":
            unit = "us"
        if element not in d :
            d[element] = {}
        d[element][isotope] = flt(num, units=unit)
    return d
def Another1():
    '''From
    http://www.astro.caltech.edu/~dperley/public/isotopetable.html
    Isotope \t half-life in years
    '''
    data = '''
    # From http://www.astro.caltech.edu/~dperley/public/isotopetable.html
    # Isotope 	Half-life (yr)
    Holmium-166m 	1,200
    Berkelium-247 	1,380
    Radium-226 	1,600
    Molybdenum-93 	4,000
    Holmium-153 	4,570
    Curium-246 	4,730
    Carbon-14 	5,730
    Plutonium-240 	6,563
    Thorium-229 	7,340
    Americium-243 	7,370
    Curium-245 	8,500
    Curium-250 	9,000
    Tin-126 	10,000
    Niobium-94 	20,300
    Plutonium-239 	24,110
    Protactinium-231	32,760
    Lead-202 	52,500
    Lanthanum-137 	60,000
    Thorium-230 	75,380
    Nickel-59 	76,000
    Thorium-230 	77,000
    Calcium-41 	103,000
    Neptunium-236 	154,000
    Uranium-233 	159,200
    Rhenium-186m 	200,000
    Technetium-99 	211,000
    Krypton-81 	229,000
    Uranium-234 	245,500
    Chlorine-36 	301,000
    Curium-248 	340,000
    Bismuth-208 	368,000
    Plutonium-242 	373,300
    Aluminum-26 	717,000
    Selenium-79 	1,130,000
    Iron-60 	1,500,000
    Beryllium-10 	1,510,000
    Zirconium-93 	1,530,000
    Curium-247 	1,560,000
    Gadolinium-150 	1,790,000
    Neptunium-237 	2,144,000
    Cesium-135 	2,300,000
    Technetium-97 	2,600,000
    Dysprosium-154 	3,000,000
    Bismuth-210m 	3,040,000
    Manganese-53 	3,740,000
    Technetium-98 	4,200,000
    Palladium-107 	6,500,000
    Hafnium-182 	9,000,000
    Lead-205 	15,300,000
    Curium-247 	15,600,000
    Iodine-129 	17,000,000
    Uranium-236 	23,420,000
    Niobium-92 	34,700,000
    Plutonium-244 	80,800,000
    Samarium-146 	103,000,000
    Uranium-236 	234,200,000
    Uranium-235 	703,800,000
    Potassium-40 	1,280,000,000
    Uranium-238 	4,468,000,000
    Rubidium-87 	4,750,000,000
    Thorium-232 	14,100,000,000
    Lutetium-176 	37,800,000,000
    Rhenium-187 	43,500,000,000
    Lanthanum-138 	105,000,000,000
    Samarium-147 	106,000,000,000
    Platinum-190 	650,000,000,000
    Tellurium-123 	>1 x 10^13
    Osmium-184 	>5.6 x 10^13
    Gadolinium-152 	1.08 x 10^14
    Tantalum-180m 	>1.2 x 10^15
    Xenon-124 	>1.6 x 10^14
    Indium-115 	4.41 x 10^14
    Zinc-70 	>5 x 10^14
    Hafnium-174 	2.0 x 10^15
    Osmium-186 	2.0 x 10^15
    Samarium-149 	>2 x 10^15
    Neodymium-144 	2.29 x 10^15
    Samarium-148 	7 x 10^15
    Cadmium-113 	7.7 x 10^15
    Cerium-142 	>5 x 10^16
    Tungsten-183 	>1.1 x 10^17
    Vanadium-50 	1.4 x 10^17
    Lead-204 	1.4 x 10^17
    Chromium-50 	>1.8 x 10^17
    Tungsten-184 	>3 x 10^17
    Calcium-48 	>6.3 x 10^18
    Molybdenum-100 	1.0 x 10^19
    Neodymium-150 	>1.1 x 10^19
    Zirconium-96 	>3.8 x 10^19
    Selenium-82 	1.1 x 10^20
    Tellurium-130 	7.9 x 10^20
    Xenon-136 	>2.4 x 10^21
    Tellurium-128 	2.2 x 10^24
    '''
    def convert(s):
        '''Return (greater, halflife) where greater is if a '>' sign was
        present and halflife is the floating point number in years.
        '''
        greater = False
        s = s.strip()
        if s[0] == ">":
            greater = True
            s = s[1:]
        if "x" in s:
            s = s.replace(" ", "")
            s = s.replace("x10^", "e")
        elif "," in s:
            s = s.replace(",", "")
        return (greater, float(s))
    def GetName(s):
        '''Split on '-' and convert to (abbreviation, isotope).
        '''
        name, isotope = s.split("-")
        abbr = Elements[name]
        return (abbr, isotope)
    d = {}
    for line in data.split("\n"):
        line = line.strip()
        if not line or line[0] == "#":
            continue
        name, halflife = line.split("\t")
        abbr, isotope = GetName(name)
        greater, hl = convert(halflife)
        gt = ">" if greater else ""
        print(abbr, isotope, greater, "{}{:.2g}".format(gt, hl))
def Another2():
    '''
    From http://www.nist.gov/pml/data/halflife-html.cfm, Wed 17 Feb 2016
 
    Columns:
        Radionuclide
        Number of sources
        Number of half lives followed
        Half-life *
        Statistical standard uncertainty
        Other standard uncertainty
        References
 
    * The stated uncertainties are the sum, in quadrature, of the
      statistical uncertainty (the "external standard deviation" in the
      weighted mean) and other uncertainties which include those from
      the Stevenson equation (NBS Special Publication 626) and from the
      correction for the 210Bi ingrowth in the radium reference sources.
 
    (a)     Measured by internal gas proportional counting.
    (b)     Normal saline solution.
    (c)     Acid solution.
 
    3H 	18 	3 	  4500 ± 8 d  	8 	0 	1 (a)
    18F 	3 	13.1 	  1.82951 ± 0.00034 h  	0.00024 	0.00024 	§
    22Na 	5 	1.9 - 4.7 	  950.97 ± 0.15 d  	0.09 	0.12 	§
    24Na 	14 	1.1 - 7.6 	  14.9512 ± 0.0032 h  	0.0009 	0.0031 	§
    32P 	2 	2.8 	  14.263 ± 0.003 d  	0.003 	0.0 	6
    44Ti 	1 	0.35 	  22154 ± 456 d  	180 	419 	2
    46Sc 	4 	3.6 - 10.3 	  83.831 ± 0.066 d  	0.030 	0.059 	§
    51Cr 	11 	2.3 - 8.9 	  27.7010 ± 0.0012 d  	0.0007 	0.0009 	§
    54Mn 	2 	3.3 - 7.4 	  312.028 ± 0.034 d  	0.034 	0.0 	§
    57Co 	7 	4.7 - 10.4 	  272.11 ± 0.26 d  	0.09 	0.25 	§
    58Co 	1 	9.1 	  70.77  ± 0.11 d  	0.11 	0.0 	§
    59Fe 	6 	4.0 - 9.3 	  44.5074 ± 0.0072 d  	0.0048 	0.0053 	§
    60Co 	8 	3.7 - 5.3 	  1925.20 ± 0.25 d  	0.10 	0.23 	§,6
    62Cu 	3 	2.7 - 3.9 	  9.6725 ± 0.0080 min  	0.0080 	0.0 	3,6
    65Zn 	1 	3.2 	  244.164 ± 0.099 d  	0.099 	0.0 	§
    67Ga 	13 	1.8 - 8.3 	  3.26154 ± 0.00054 d  	0.00015 	0.00052 	§
    75Se 	19 	2.4 - 8.7 	  119.809 ± 0.066 d  	0.014 	0.065 	§
    85Kr 	1 	1.9 	  3935.7 ± 1.2 d  	1.2 	0.0 	§,6
    85Sr 	8 	1.1 - 4.8 	  64.8530 ± 0.0081 d  	0.0039 	0.0071 	§
    88Y 	8 	1.3 - 8.1 	  106.626 ± 0.044 d  	0.017 	0.041 	§
    99Mo 	14 	3.6 - 9.5 	  65.9239 ± 0.0058 h  	0.0031 	0.0049 	§
    99mTc 	33 	2.1 - 12.0 	  6.00718 ± 0.00087 h  	0.00015 	0.00086 	§ (b)
    99mTc 	17 	1.9 - 8.0 	  6.0123 ± 0.0032 h  	0.0007 	0.0031 	6 (c)
    103Ru 	7 	0.4 	  39.310 ± 0.044 d  	0.044 	0.0 	6
    109Cd 	2 	3.4 - 5.3 	  463.26 ± 0.63 d  	0.36 	0.51 	§
    110mAg 	1 	9.3 	  249.950 ± 0.024 d  	0.024 	0.0 	§
    111In 	11 	1.4 - 9.3 	  2.80477 ± 0.00053 d  	0.00017 	0.00051 	§
    113Sn 	11 	2.3 - 11.0 	  115.079 ± 0.080 d  	0.025 	0.076 	§
    117mSn 	10 	1.5 - 4.0 	  14.00 ± 0.05 d  	0.05 	0.0 	4
    123I 	3 	5.4 - 12.7 	  13.2235 ± 0.0019 h  	0.0019 	0.0 	§
    125I 	18 	1.4 - 6.2 	  59.49  ± 0.13 d  	0.03 	0.12 	§
    125Sb 	1 	5.4 	  1007.56 ± 0.10 d  	0.10 	0.0 	§,6
    127Xe 	5 	1.1 - 11.5 	  36.3446 ± 0.0028 d  	0.0028 	0.0 	§
    131I 	21 	1.0 - 10.9 	  8.0197 ± 0.0022 d  	0.0005 	0.0021 	§
    131mXe 	2 	1.8 	  11.934 ± 0.021 d  	0.014 	0.016 	§
    133Ba 	4 	2.0 	  3854.7 ± 2.8 d  	1.3 	2.5 	§,6
    133Xe 	3 	4.8 - 11.2 	  5.24747 ± 0.00045 d  	0.00045 	0.0 	§
    134Cs 	5 	1.7 - 3.0 	  753.88 ± 0.15 d  	0.11 	0.11 	§
    137Cs 	6 	0.7 - 0.9 	  11018.3 ± 9.5 d  	3.5 	8.8 	§,6
    139Ce 	9 	1.5 - 6.4 	  137.734 ± 0.091 d  	0.029 	0.086 	§
    140Ba 	10 	1.8 - 4.4 	  12.7527 ± 0.0023 d  	0.0009 	0.0022 	§
    140La 	2 	4.2 	  40.293 ± 0.012 h  	0.008 	0.009 	§
    141Ce 	1 	6.1 	  32.510 ± 0.024 d  	0.024 	0.0 	§
    144Ce 	1 	3.9 	  284.534 ± 0.032 d  	0.032 	0.0 	§,6
    152Eu 	4 	1.6 - 1.8 	  4947.2 ± 1.1 d  	0.7 	0.8 	§,6
    153Gd 	2 	7.3 	  239.472 ± 0.069 d  	0.041 	0.055 	§
    153Sm 	1 	7.3 	  46.2853 ± 0.0014 h  	0.0014 	0.0 	§
    154Eu 	3 	2.4 	  3145.2 ± 1.1 d  	1.1 	0.0 	§,6
    155Eu 	2 	3.1 - 4.3 	  1739.06 ± 0.45 d  	0.45 	0.0 	§,6
    166Ho 	2 	5.4 - 7.2 	  26.794 ± 0.023 h  	0.013 	0.019 	§,6
    169Yb 	14 	3.4 - 9.5 	  32.0147 ± 0.0093 d  	0.0026 	0.0089 	§
    177Lu 	4 	2 - 5 	  6.64 ± 0.01 d  	0.01 	0.0 	5
    181W 	3 	5.9 - 6.6 	  121.095 ± 0.064 d  	0.042 	0.048 	§
    186Re 	2 	5.7 - 6.5 	  89.248 ± 0.069 h  	0.018 	0.067 	§
    188Re 	3 	4.2 - 7.1 	  17.001 ± 0.022 h  	0.09 	0.021 	§,6
    188W 	1 	4.0 	  69.783 ± 0.048 d  	0.048 	0.0 	6
    192Ir 	1 	2.4 	  73.810 ± 0.019 d  	0.019 	0.0 	§
    195Au 	5 	0.6 - 6.0 	  186.098 ± 0.047 d  	0.021 	0.042 	§
    198Au 	4 	4.5 - 7.4 	  2.69517 ± 0.00021 d  	0.00021 	0.0 	§
    201Tl 	12 	2.6 - 11.5 	  3.0456 ± 0.0015 d  	0.0004 	0.0014 	§
    202Tl 	1 	1.4 	  12.466 ± 0.081 d  	0.081 	0.0 	§
    203Hg 	14 	1.7 - 6.6 	  46.619 ± 0.027 d  	0.007 	0.026 	§
    203Pb 	7 	1.8 - 2.8 	  51.923 ± 0.037 h  	0.013 	0.034 	§
    207Bi 	2 	0.9 	  11523. ± 15. d  	9 	12 	§,6
    228Th 	6 	1.7 - 8.3 	  698.60 ± 0.36 d  	0.14 	0.33 	§
    '''
def Time(tm):
    '''Return a string where the time tm in seconds is given in
    customary time units.
    '''
    t, spd, spy = float(tm), 24*3600, 31556925.97
    if t < 1:
        if t < 1e-3:
            s = sig(t*1e6, _ndigits) + " us"
        else:
            s = sig(t*1e3, _ndigits) + " ms"
    else:
        if t < 60:
            s = sig(t, _ndigits) + " s"
        elif t < 60*60:
            s = sig(t/60, _ndigits) + " min"
        elif t < spd:
            s = sig(t/3600, _ndigits) + " hr"
        elif t < spy:
            s = sig(t/spd, _ndigits) + " day"
        else:
            s = sig(t/spy, _ndigits) + " yr"
    return s
if __name__ == "__main__":
    halflife = ProcessData()
    # Print out a table of half-lives
    usesci = flt(10000, units="year")
    for symbol in sorted(halflife):
        atno, atwt = atomic_data[symbol]
        name = elements[symbol]
        print(f"{symbol} ({name}, {atno} protons, {atwt} g/mol)")
        for isotope in sorted(halflife[symbol]):
            t = halflife[symbol][isotope]
            if t.val > usesci.val:
                x = flt(t.val)
                print(f"  {isotope:4s}    {x._sci(n=3)} years")
            else:
                print(f"  {isotope:4s}    {t}")
