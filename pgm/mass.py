'''
TODO:

* Consider making an input datafile a chunk of executable python.  Each
  of the objects would then be instantiated with lines like 

    import mass 
    mass.material = "fir"
    mass.units = "inches"
    mass.angles = "degrees"
    mass.digits = 3
    mass.mass_unit = "kg"
    mass.volume_unit = "in3"
    mass.debug = True    # Causes verbose debugging output

    mass.components = [
        mass.w2by4(L="10 ft", material="fir", n=5, name="Main joist",
                   neg=False, rho=None),
        ...
    ]
    mass.components += [
        ...
    ]

  It would also make sense to use the f.py module for the flt objects.  

  One advantage of this approach is that a repl could be used to process
  things and maybe the syntax errors will be pointed out.

  Another benefit is that things could be set up to watch the execution
  of the config file with the debugger, letting you see where errors
  occur.

  * I'd be able to document a configuration file with triple-quoted
    strings.

  * Another syntax could be 

    mass.components = [
        mass.comp(mass.w2x4, L="10 ft", material=mass.fir, n=5, 
                  name="Main joist", neg=False, rho=None),
        ...
    ]

   The words like w2x4 and fir would be defined as global variables,
   reducing the typing of quotes.  oct would go to octbar and hex would
   go to hexbar to avoid clashing with python keywords.

* Add bolt, screw, washer, nut, lockwasher objects.  Have them default
  to being made from steel.

----------------------------------------------------------------------
Script to calculate the mass and volume of an object composed of basic
geometrical shapes.  You define a datafile that describes the
composite object; the script reads this datafile and prints out a
report giving the volume and mass of each component.

See the mass.pdf file for documentation.

The included densities are derived from the values I given in the
density.zip package (see
https://someonesdad1.github.io/hobbyutil/project_list.html).

'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2013 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Calculate mass of a structure made of geometrical primitives
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from math import *
    from uncertainties import UFloat, ufloat
    import getopt
    import hashlib
    import inspect
    import re
    import sys
    import time
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from asme import UnifiedThread
    from sig import sig, SigFig
    from u import u, to, ParseUnit
    from columnize import Columnize
    from get import GetNumber
    from cmddecode import CommandDecode
if 1:   # Global variables
    # The density of air in g/cc at 20 degrees C and 1 atmosphere.  The
    # density of other gases are defined in terms of air's density.
    _air_density = 0.0012041
    # The following dictionary defines the usable materials.  Level is an
    # integer that is used to determine which level in the -L option the
    # material is printed to stdout (note that all materials will be
    # defined in the program).  The ShortID should be a short string in
    # all lowercase letters.  Note the density must be in g/cc (grams per
    # cubic centimeter).
    _materials = {
        "Metals": (
            # Level, ShortID, name, density in g/cc
            (1, "al", "Aluminum", 2.7),
            (1, "brass", "Brass", 8.47),
            (1, "bronze", "Bronze", 8.8),
            (1, "ci", "Iron, cast", 7.2),
            (1, "cu", "Copper", 8.9),
            (1, "steel", "Steel 1018", 7.86),
            (1, "pb", "Lead", 11.35),
            (2, "ag", "Silver", 10.5),
            (2, "au", "Gold", 19.3),
            (2, "becu", "BeCu (beryllium copper)", 8.25),
            (2, "mg", "Magnesium", 1.74),
            (2, "sn", "Tin", 7.3),
            (2, "solder", "Solder, Pb-Sn eutectic", 8.32),
            (2, "sst", "Steel 304 stainless", 8.02),
            (2, "zn", "Zinc", 7.1),
            (3, "alnico", "Alnico", 7),
            (3, "babbit", "Babbit", 7.28),
            (3, "cd", "Cadmium", 8.65),
            (3, "co", "Cobalt", 8.9),
            (3, "constantan", "Constantan", 8.9),
            (3, "cr", "Chromium", 7.2),
            (3, "fe", "Iron (pure)", 7.87),
            (3, "hg", "Mercury (liquid)", 13.546),
            (3, "iron", "Iron (pure)", 7.87),
            (3, "k", "Potassium", 0.86),
            (3, "li", "Lithium", 0.534),
            (3, "mn", "Manganese", 7.4),
            (3, "mo", "Molybdenum", 10.2),
            (3, "monel", "Monel", 7),
            (3, "na", "Sodium", 0.97),
            (3, "neo", "Neodymium magnet", 7.45),
            (3, "ni", "Nickel", 8.9),
            (3, "pt", "Platinum", 21.4),
            (3, "pu", "Plutonium", 19.84),
            (3, "si", "Silicon", 2.33),
            (3, "ta", "Tantalum", 16.6),
            (3, "th", "Thorium", 11.7),
            (3, "ti", "Titanium", 4.5),
            (3, "u", "Uranium", 18.8),
            (3, "v", "Vanadium", 6.1),
            (3, "w", "Tungsten", 19.3),
            (3, "zr", "Zirconium", 6.5),
            (3, "gsilv", "German silver Cu, Ni, Zn", 8.45),
        ),
        "Woods": (
            # The value for fir from my references was 0.48.  I adjusted
            # it upwards a bit to make an 8' 2x4 have a mass of about 9.5
            # pounds.  Clearly, this is an approximation, as I have
            # purchased very dry 2x4's that weigh half or less of very wet
            # ones you occasionally find.
            (1, "fir", "Douglas fir", 0.52),
            (1, "maple", "Maple", 0.71),
            (1, "masonite", "Masonite", 0.9),
            (1, "mpartbd", "Particle board, med.", 0.6),
            (1, "oak", "Oak", 0.8),
            (1, "pine", "Pine", 0.4),
            # The number for plywood was found on the web as 3 lbm per square
            # foot per inch of thickness.
            (1, "ply", "Plywood", 0.58),
            (1, "plywood", "Plywood", 0.58),
            (2, "balsa", "Balsa", 0.13),
            (2, "bamboo", "Bamboo", 0.35),
            (2, "cedar", "Cedar, red", 0.38),
            (2, "cherry", "Cherry", 0.8),
            (2, "walnut", "Walnut", 0.68),
            (3, "apple", "Apple", 0.71),
            (3, "ash", "Ash", 0.75),
            (3, "ash, green", "Ash, green", 0.85),
            (3, "hickory", "Hickory", 0.85),
            (3, "beech", "Beech", 0.8),
            (3, "lv", "Lignum vitae", 1.28),
            (3, "mahog", "Mahogany", 0.6),
            (3, "oak, green", "Oak, green", 1.0),
            (3, "sugar maple, green", "Sugar maple, green", 1.0),
            (3, "willow, green", "Willow, green", 0.87),
        ),
        "Plastics": (
            (1, "acrylic", "Acrylic", 1.19),
            (1, "nylon", "Nylon", 1.14),
            (1, "poly", "Polyethylene", 0.93),
            (1, "pvc", "PVC", 1.2),
            (1, "styro", "Styrofoam", 0.04),
            (2, "abs", "ABS", 1.07),
            (2, "hdpe", "Polyethylene HDPE", 0.96),
            (2, "polycarb", "Polycarbonate", 1.2),
            (2, "polypro", "Polypropylene", 0.9),
            (2, "styrene", "Polystyrene", 1.06),
            (2, "teflon", "Teflon", 2.2),
            (3, "bak", "Bakelite", 1.36),
            (3, "epgc", "Epoxy w/65% by wt glass cloth", 2.0),
            (3, "epoxy", "Epoxy", 1.11),
            (3, "hrfoam", "High resilience foam", 0.048),
            (3, "kapton", "Kapton polyimide", 1.42),
            (3, "kelf", "Kel-F", 2.1),
            (3, "ldfoam", "Low-density polyurethane foam", 0.019),
            (3, "memfoam", "Memory foam (dev. for NASA)", 0.055),
            (3, "mylar", "Mylar", 1.395),
            (3, "phenolic", "Phenolic", 1.9),
        ),
        "Stone, ceramics, glass, etc.": (
            (1, "brick", "Brick", 1.8),
            (1, "rconcrete", "Concrete, reinforced", 2.2),
            (1, "concrete", "Concrete, gravel", 2.5),
            (1, "mdirt", "Earth, moist excavated", 1.44),
            (1, "mdirtp", "Earth, moist packed", 1.6),
            (1, "mud", "Mud, flowing", 1.7),
            (1, "ddirt", "Earth, dry", 1.4),
            (1, "glass", "Window glass", 2.58),
            (1, "gravel", "Gravel, dry", 1.5),
            (1, "sand", "Sand, dry", 1.6),
            (1, "wetsand", "Sand, wet packed", 2.0),
            (2, "wdirt", "Earth, wet excavated", 1.6),
            (2, "alumina", "Alumina", 3.68),
            (2, "basalt", "Basalt", 3.0),
            (2, "clay", "Clay", 1.9),
            (2, "fbrick", "Brick (fire clay)", 2.4),
            (2, "granite", "Granite", 2.7),
            (2, "marble", "Marble", 2.6),
            (2, "plaster", "Plaster", 0.85),
            (2, "sio2", "Silica glass SiO2", 2.55),
            (3, "bent", "Bentonite", 0.6),
            (3, "corundum", "Corundum", 3.2),
            (3, "dia", "Diamond", 3.1),
            (3, "graphite", "Graphite", 1.6),
            (3, "mgo", "Magnesium oxide", 2.8),
            (3, "sic", "Silicon carbide", 2.72),
        ),
        "Other": (
            (1, "card", "Cardboard", 0.7),
            (1, "paper", "Paper", 0.9),
            (1, "rubber", "Rubber, hard", 1.2),
            (2, "buna", "Rubber, Buna N", 1.0),
            (2, "chalk", "Chalk", 2),
            (2, "cork", "Cork", 0.24),
            (2, "drywall", "Gypsum board", 0.8),
            (2, "ice", "Ice 0 deg C", 0.9),
            (2, "leather", "Leather", 0.95),
            (2, "linoleum", "Linoleum", 1.18),
            (2, "perl", "Perlite", 0.09),
            (2, "wax", "Paraffin wax", 0.9),
            (3, "amber", "Amber", 1.08),
            (3, "beeswax", "Beeswax", 0.95),
            (3, "bicarb", "Bicarbonate of soda", 0.69),
            (3, "bullseye", "Bullseye gunpowder", 0.4),
            (3, "butter", "Butter", 0.87),
            (3, "cement", "Cement, Portland", 1.5),
            (3, "charcoal", "Charcoal", 0.2),
            (3, "coal", "Coal (solid)", 1.5),
            (3, "csalt", "Coarse salt", 0.8),
            (3, "felt", "Felt, wool", 0.3),
            (3, "flour", "Flour, wheat", 0.59),
            (3, "fsalt", "Fine salt", 1.2),
            (3, "garbage", "Garbage", 0.5),
            (3, "gelatine", "Gelatine", 1.27),
            (3, "mortar", "Mortar (wet)", 2.4),
            (3, "neoprene", "Rubber, Neoprene", 1.25),
            (3, "porcelain", "Porcelain", 2.4),
            (3, "potato", "Potatoes", 0.7),
            (3, "rsalt", "Rock salt", 2.2),
            (3, "sawdust", "Sawdust", 0.2),
            (3, "snow", "Snow, compacted", 0.48),
            (3, "sugar", "Sugar, granulated", 0.85),
            (3, "sulfur", "Sulfur, pulverized", 0.96),
            (3, "tar", "Tar", 1.1),
            (3, "verm", "Vermiculite", 0.13),
            (3, "viton", "Rubber, Viton", 1.85),
        ),
        "Liquids": (
            (1, "gas", "Gasoline", 0.7),
            (1, "oil", "Machine oil", 0.9),
            (1, "water", "Water", 1),
            (2, "acetone", "Acetone", 0.79),
            (2, "ethanol", "Alcohol, ethyl", 0.788),
            (2, "ipa", "Alcohol, isopropyl", 0.79),
            (2, "kerosene", "Kerosene", 0.823),
            (2, "methanol", "Alcohol, methyl", 0.79),
            (2, "spirits", "Mineral spirits", 0.66),
            (3, "acetic", "Acetic acid", 1.05),
            (3, "eglycol", "Ethylene glycol", 1.1),
            (3, "benzene", "Benzene", 0.876),
            (3, "carbtet", "Carbon tetrachloride", 1.59),
            (3, "chloro", "Chloroform", 1.5),
            (3, "crude", "Crude oil", 0.8),
            (3, "d2o", "Heavy water", 1.1086),
            (3, "ether", "Ether", 0.72),
            (3, "glycerine", "Glycerine", 0.63),
            (3, "hcl40", "Hydrochloric acid 40%", 1.2),
            (3, "linseed", "Linseed oil", 0.93),
            (3, "naphtha", "Naphtha", 0.85),
            (3, "nitric91", "Nitric acid 91%", 1.51),
            (3, "pglycol", "Propylene glycol", 0.968),
            (3, "lpropane", "Propane (liquid)", 0.5),
            (3, "sea", "Sea water", 1.03),
            (3, "sulfuric87", "Sulfuric acid 87%", 1.79),
            (3, "toluene", "Toluene", 0.87),
            (3, "trichlor", "1,1,1 Trichloroethane", 0.94),
            (3, "turp", "Turpentine", 0.87),
            (3, "xylene", "Xylene", 0.89),
        ),
        "Gases": (
            (1, "air", "Dry air 20 C, 1 atm", _air_density),
            (1, "h2", "Hydrogen (gas)", 0.070*_air_density),
            (1, "n2", "Nitrogen (gas)", 0.967*_air_density),
            (1, "o2", "Oxygen (gas)", 1.105*_air_density),
            (1, "co2", "Carbon dioxide (gas)", 1.52*_air_density),
            (2, "ar", "Argon (gas)", 0.59*_air_density),
            (2, "he", "Helium (gas)", 0.138*_air_density),
            (2, "ne", "Neon (gas)", 0.697*_air_density),
            (2, "propane", "Propane (gas)", 1.52*_air_density),
            (2, "xe", "Xenon (gas)", 4.53*_air_density),
            (3, "acetylene", "Acetylene (gas)", 0.9*_air_density),
            (3, "butane", "Butane (gas)", 0.9*_air_density),
            (3, "cl", "Chlorine (gas)", 2.45*_air_density),
            (3, "co1", "Carbon monoxide (gas)", 0.967*_air_density),
            (3, "f", "Fluorine (gas)", 1.31*_air_density),
            (3, "hcl", "Hydrogen chloride (gas)", 1.26*_air_density),
            (3, "methane", "Methane (gas)", 0.554*_air_density),
            (3, "nh3", "Ammonia (gas)", 0.9*_air_density),
            (3, "ozone", "Ozone (gas)", 1.66*_air_density),
            (3, "r11", "Refrigerant 11 (gas)", 4.74*_air_density),
            (3, "so2", "Sulfur dioxide (gas)", 2.21*_air_density),
            (3, "vacuum", "Vacuum", 0),
        ),
    }
    # The following keywords represent control commands that change the
    # current state of the script.
    _control_cmds = set((
        "del",          # Delete a variable
        "digits",       # How many significant figures in report
        "angles",       # Factor to convert angle measure to radians
        "material",     # Default material
        "munit",        # Mass unit for report
        "units",        # Default units to use
        "vunit",        # Volume unit for report
    ))
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
'''
Component classes
    We define classes that encapsulate properties of the components in
    the datafile.  The objects all internally convert their linear
    dimensions to meters and calculate their mass in grams.

    If you're not familiar with object-oriented programming, the
    following Primitive object encapsulates all the behavior common to
    the different geometrical components defined by the program.  Then
    the derived objects (for example, Rect, which is a subclass of
    Primitive) only have to define the chunks of code that change from
    object to object.  In this script, this is the volume calculation.
    In the case of 2x4, 2x6, etc., note how the 2x6, 2x8, etc. are
    subclasses of the 2x4 object; all they have to do differently is
    define their width in the constructor __init__().

    Because of this object design, it should be easy to add new
    geometrical components -- just emulate what's been done for the
    existing components.
'''
class Primitive(object):
    '''This class is a base object for all of the geometrical shapes.
    It can calculate its volume and mass.
    '''
    # If not None, these are variable names that should be removed from the
    # object's string representation.
    ignore = None
 
    # Used where steel is the default material (this value of 10*pi/4 was
    # well-known to slide rule makers).
    steel_sp_gr = 10*pi/4   # g/cc
 
    def __init__(self, linenum, line, opts, **kw):
        '''The dictionary kw will contain the numbers that were
        given in the datafile line.  Make sure we have a corresponding
        diameter if a radius was given.
 
        linenum     1-based line number in the datafile that created us.
        line        String from that line.
        opts        Dictionary of settings.
        kw          Keyword dictionary.
 
        kw must contain:
 
            rho     Defines the specific mass of the object's material.
            vars    Dictionary of the variable definitions in scope at
                    the moment of creation of the object.
            un      It is the unit that the linear dimensions are
                    defined in.
        '''
        self.kw = {}
        self.opts = opts
        self.linenum = linenum
        self.line = line
        self.kw.update(kw)
        # Make sure we have both diameters d and D and radii r and R.
        # Note we do NOT convert them to meters at this point; this is
        # to allow the original datafile strings to remain so that
        # they can be shown with the object's string representation is
        # printed.
        if "r" in self.kw and "d" not in self.kw:
            self.kw["d"] = 2*self.kw["r"]
        if "R" in self.kw and "D" not in self.kw:
            self.kw["D"] = 2*self.kw["R"]
        if "d" in self.kw and "r" not in self.kw:
            self.kw["r"] = self.kw["d"]/2
        if "D" in self.kw and "R" not in self.kw:
            self.kw["R"] = self.kw["D"]/2
        # Must have a density in g/cc
        if "rho" not in self.kw:
            msg = "Density missing in line {}\n  '{}'"
            Error(msg.format(linenum, line))
        assert isinstance(self.kw["rho"], (int, float))
        # Must have a count n
        if "n" not in self.kw:
            self.kw["n"] = 1
        else:
            if (not isinstance(self.kw["n"], (int, float)) or
                    self.kw["n"] < 0):
                msg = "n keyword must be a number >= 0 in line {}\n  '{}'"
                Error(msg.format(linenum, line))
        # Must have a unit specified with the "un" keyword
        if "un" not in self.kw:
            msg = "Units (un) missing in line {}\n  '{}'"
            Error(msg.format(linenum, line))
        # Verify we have the parameters we need
        self.msg = "Parameter '{}' missing from keywords\n"
        self.msg += "  Line {} in datafile '{}'".format(self.linenum,
                                                    opts["datafile"])
        self.check()
    def __str__(self):
        return self.cls() + "<" + DictToStr(self.kw, Primitive.ignore) + ">"
    def check(self):
        '''Check the keyword parameters to ensure we have those we
        need.  The derived class must create the set of self.varnames.
        '''
        for i in self.varnames:
            if i not in self.kw:
                Error(self.msg.format(i))
            if isinstance(self.kw[i], (int, float)):
                if self.kw[i] < 0:
                    msg = "Parameter '{}' is negative\n"
                    msg += "  Line {} in datafile '{}'"
                    Error(msg.format(i, self.linenum, self.opts["datafile"]))
    def volume(self):
        '''Return the volume in cubic meters.
        '''
        raise RuntimeError("Abstract method")
    def mass(self):
        '''Return the mass in g of the object.  The 1e6 is to
        convert g/cc to g/m^3 (needed because the volume is in cubic
        meters).
        '''
        return 1e6*self.kw["rho"]*self.volume()
    def neg(self):
        '''Return 1 if the neg keyword is False or doesn't exist; -1
        if it's True.
        '''
        return -1 if "neg" in self.kw and self.kw["neg"] else 1
    def cls(self):
        '''Return object name.
        '''
        s = str(self.__class__).split()[1].replace("'", "")
        return s.split(".")[1].replace(">", "")
    def id(self):
        '''If we have a "name" in the self.kw dictionary, return this
        as a name.  Otherwise, return our object name and append the
        line number we were defined in the datafile in square
        brackets.
        '''
        ln = " [{}]".format(self.linenum)
        if "name" in self.kw:
            s = self.kw["name"]
        else:
            s = self.cls() + ln
        return s
    def ToSI(self, s, is_area=False):
        '''Conver the string self.kw[s] to an SI unit.  There are two
        allowed forms.  First, self.kw[s] can simply be a string
        representing a number; this case is converted to meters using
        the unit given in self.kw["un"].  The second case is where a
        unit string comes after the number, separated by one or more
        spaces.
 
        Note these quantities are linear dimensions unless is_area is
        True, in which case it's an area.
        '''
        x = self.kw[s]
        e = 2 if is_area else 1
        if isinstance(x, (int, float)):
            # Uses the default unit
            return float(x)*(u(self.kw["un"])**e)
        elif isinstance(x, str):
            # Has an attached unit
            try:
                f = x.split()
                if len(f) != 2:
                    raise Exception("Must be number, space, unit")
                return float(eval(f[0]))*(u(f[1])**e)
            except Exception as e:
                msg = "'{}' is an improper unit string in line {} of datafile:"
                msg += "\n  '{}'\n  {}"
                Error(msg.format(self.kw[s], self.linenum, self.line, str(e)))
class Rect(Primitive):  # Rectangular bar stock
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("abL")
        self.doc = "rect:a=side, b=side, L=length"
        super(Rect, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        a = self.ToSI("a")
        b = self.ToSI("b")
        L = self.ToSI("L")
        V = self.kw["n"]*self.neg()*a*b*L
        return V
class Cyl(Primitive):   # Cylinder
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("dL")
        self.doc = "cyl:d=diam, r=radius, L=length"
        super(Cyl, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        d = self.ToSI("d")
        L = self.ToSI("L")
        return self.kw["n"]*self.neg()*pi*d**2*L/4
class Gcyl(Primitive):  # Generalized cylinder
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("AL")
        self.doc = "gcyl:A=area, L=length"
        super(Gcyl, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        A = self.ToSI("A", is_area=True)
        L = self.ToSI("L")
        return self.kw["n"]*self.neg()*A*L
class Pipe(Primitive):
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("tdL")
        self.doc = "pipe:d=diam, r=radius, t=wall, L=length"
        super(Pipe, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        t = self.ToSI("t")
        d = self.ToSI("d")
        L = self.ToSI("L")
        di = d - 2*t
        return self.kw["n"]*self.neg()*pi/4*L*(d**2 - di**2)
class TorxWoodScrew(Primitive):
    '''Models a bugle head steel Torx head wood screw.  You must measure
    the mass of the screw; the volume is calculated from this mass.
 
    I use Torx woodscrews a lot in shop and DIY projects.  I use the
    modern Hillman design and measured the mass of screws from 1.25" to
    4" long.  A plot showed these were pretty linear in mass with
    length, so I fitted a line to get a slope of 2.2 and an intercept of
    0.3.  Thus, mass in g is m = 2.2*L + 0.3 where L is length in
    inches.
    '''
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set()
        super(TorxWoodScrew, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        # Return the volume from the known mass
        cm3_to_m3 = 1e-6
        v = (self.mass_grams/Primitive.steel_sp_gr)*cm3_to_m3
        return self.kw["n"]*self.neg()*v
    def get_mass(self):
        allowed_lengths = set((1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.5, 4))
        if self.length not in allowed_lengths:
            raise ValueError("Length is out of range")
        if self.length == 4:
            # Note the 4 inch length is not predicted by the regression
            self.mass_grams = 8.1
        else:
            # Mass from length in inches gotten from a linear regression
            self.mass_grams = 2.2*self.length + 0.3
class T125(TorxWoodScrew):
    def __init__(self, linenum, line, opts, **kw):
        self.length = 1.25
        super(T125, self).__init__(linenum, line, opts, **kw)
        self.get_mass()
class T150(TorxWoodScrew):
    def __init__(self, linenum, line, opts, **kw):
        self.length = 1.5
        super(T150, self).__init__(linenum, line, opts, **kw)
        self.get_mass()
class T175(TorxWoodScrew):
    def __init__(self, linenum, line, opts, **kw):
        self.length = 1.75
        super(T175, self).__init__(linenum, line, opts, **kw)
        self.get_mass()
class T200(TorxWoodScrew):
    def __init__(self, linenum, line, opts, **kw):
        self.length = 2
        super(T200, self).__init__(linenum, line, opts, **kw)
        self.get_mass()
class T225(TorxWoodScrew):
    def __init__(self, linenum, line, opts, **kw):
        self.length = 2.25
        super(T225, self).__init__(linenum, line, opts, **kw)
        self.get_mass()
class T250(TorxWoodScrew):
    def __init__(self, linenum, line, opts, **kw):
        self.length = 2.5
        super(T250, self).__init__(linenum, line, opts, **kw)
        self.get_mass()
class T275(TorxWoodScrew):
    def __init__(self, linenum, line, opts, **kw):
        self.length = 2.75
        super(T275, self).__init__(linenum, line, opts, **kw)
        self.get_mass()
class T300(TorxWoodScrew):
    def __init__(self, linenum, line, opts, **kw):
        self.length = 3
        super(T300, self).__init__(linenum, line, opts, **kw)
        self.get_mass()
class T350(TorxWoodScrew):
    def __init__(self, linenum, line, opts, **kw):
        self.length = 3.5
        super(T350, self).__init__(linenum, line, opts, **kw)
        self.get_mass()
class T400(TorxWoodScrew):
    def __init__(self, linenum, line, opts, **kw):
        self.length = 4
        super(T400, self).__init__(linenum, line, opts, **kw)
        self.get_mass()
'''
Bolt, washer, nut
    The following classes are used to model bolts, machine screws,
    washers, and machine screw nuts.  The thread pitch diameters are
    taken from the asme.py module, which in turn gets its formulas from
    ASME B1.1-1989.
'''
class Bolt(Primitive):
    '''Models a steel bolt or machine screw.  The required parameters are:
        L = length of bolt
        d = major diameter
    The optional parameters are:
        T = head type, string [hex]
        P = percentage of length that is threaded [100%]
        p = pitch
        tpi = threads per inch
        number = Boolean [False].  If true, it's a numbered thread.  Sizes
            from 0 to 14 are allowed.
 
    Pitch is in default units; tpi is in inches.  If both are given, the
    tpi term takes priority.  If neither are given, a coarse thread is
    chosen per Seller's US Standard formula from the 1800's:
        pitch in inches = a*sqrt(d + 5/8) - 0.175
    where d is in inches, and a = 0.24 for d >= 1/4, a = 0.23 for smaller
    diameters.  This formula gives the following tpi's for various
    diameters:
          d     tpi     UNC
        0.138   38.6    32      (#6)
        0.164   34.1    32      (#8)
        0.19    30.6    24      (#10)
        0.25    20.2    20
        0.3125  17.4    18
        0.375   15.4    16
        0.5     12.6    13
    so you can see it's close to the UNC thread sizes.  The formula will be
    a bit too coarse for typical ISO metric threads, and thus underestimate
    the mass slightly.
 
    If number is True, the diameter d will be interpreted as a US numbered
    thread and the major diameter in inches will be calculated from the
    formula 0.060 + N*0.013 where N = d; it is an error if N < 0 or N > 14.
 
    Head types can be 'hex', 'flat', 'round', 'pan'.  Recesses for e.g. a
    screwdriver are not modeled.
 
    Other dimensions are gotten from regressing the dimensional information
    from the TAD calculator for nominal bolt sizes from about 1/4 inch to
    3/4 inch (dimensions all in inches).  Use outside this interval (covers
    the practical stuff I do) should be checked.
  
    In the following, the nominal bolt size is d in inches.  The number R
    in parentheses is the correlation coefficient (ranges from -1 to 1).
 
    Distance across the flats of a hex head:
        Bolt size       Distance across flats
        1/4             7/16
        5/16            1/2
        3/8             9/16
        1/2             3/4
        3/4             1-1/8
    wrench_size = 1.4000*d + 0.0625 (R = 0.9975)
 
    Thickness of a hex head:
        Bolt size       Thickness
        1/4             0.156
        3/8             0.295
        1/2             0.323
        3/4             0.483
    thickness = 0.6155*d + 0.0257 (R = 0.9797)
    '''
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("dL")
        super(Bolt, self).__init__(linenum, line, opts, **kw)
        self.in2m = 1/39.37   # Converts inches to meters
        if "number" in kw:
            try:
                n = int(kw["d"])
                if not (0 <= n <= 14):
                    raise Exception()
            except Exception:
                Error("'{}' is a bad number thread size".format(kw["d"]))
            self.d = (0.06 + n*0.013)*self.in2m  # In meters
        self.d = self.ToSI("d")
        self.L = self.ToSI("L")
        if "rho" not in kw:     # Default to a steel bolt
            kw["rho"] = Primitive.steel_sp_gr
        if "T" not in kw:
            self.T = "hex"
        else:
            self.T = kw["T"]
            self.allowed_types = ("hex", "flat", "round", "pan")
            if self.T not in self.allowed_types:
                msg = "'{}' bolt head type not recognized"
                Error(msg)
        if "P" not in kw:
            self.P = 100
        else:
            try:
                self.P = float(kw["P"])
                if not (0 <= self.P <= 100):
                    raise Exception()
            except Exception:
                Error("'{}' invalid threaded percentage".format(kw["P"]))
        if "tpi" in kw:
            try:
                self.tpi = float(kw["tpi"])
                if self.tpi <= 0:
                    raise Exception()
            except Exception:
                Error("'{}' invalid tpi".format(kw["tpi"]))
            self.p = (1/tpi)*self.in2m   # pitch in m
        if "p" in kw:
            self.p = self.ToSI("p")
        elif "tpi" not in kw:
            # Use Seller's formula
            d = round(self.d/self.in2m, 3)  # Need diameter in inches
            a = 0.24 if d >= 1/4 else 0.23
            self.p = (a*sqrt(d + 5/8) - 0.175)*self.in2m    # In meters
    def volume(self):
        d_inches = self.d/self.in2m
        tpi = 1/(self.p/self.in2m)
        ut = UnifiedThread(d_inches, tpi)
        # Get mean external pitch diameter in meters
        pd = (ut.Emax() + ut.Emin())/2*self.in2m
        L_threaded = self.L*self.P/100
        L_unthreaded = self.L - L_threaded
        # Unthreaded cylinder volume
        v = pi*self.d**2/4*L_unthreaded
        # Threaded cylinder volume
        v += pi*pd**2/4*L_threaded
        # Head volume
        if self.T == "hex":
            wrench_size = (1.4*(self.d/self.in2m) + 0.0626)*self.in2m
            area = wrench_size**2*sqrt(3)/2
            head_thickness = (0.6155*self.d/self.in2m + 0.0257)*self.in2m
            v += head_thickness*area
        elif self.T == "flat":
            raise Exception("not written yet")
        elif self.T == "round":
            raise Exception("not written yet")
        elif self.T == "pan":
            raise Exception("not written yet")
        else:
            raise Exception("Software bug:  bad head type")
        return self.kw["n"]*self.neg()*v
class Washer(Primitive):
    '''Models an annular steel washer.  The parameters are:
    D = outside diameter (optional)
    d = inside diameter (required)
    t = thickness (optional)
 
    The outside diameter and thickness default values are gotten via
    empirical formulas based on typical US inch-based sizes from the TAD
    calculator (the smaller washer size is used):
        Diameter        OD      Thickness
        #8 (0.164)      0.3     0.04
        #10 (0.190)     0.34    0.047
        1/4             0.493   0.062
        5/16            0.591   0.078
        3/8             0.688   0.094
        1/2             0.879   0.125
        3/4             1.279   0.188
    A plot shows these are pretty linear, so the empirical formula was
    gotten via linear regression:
        OD = 1.654*d + 0.0525 (R = 0.998)
        t = 0.2521*d - 0.0010 (R = 1.0000)
    where the dimensions are in inches.
    '''
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("d")
        self.doc = "washer:D=OD[optional], d=ID, t=thickness"
        super(Washer, self).__init__(linenum, line, opts, **kw)
        self.d = self.ToSI("d")
        C = 39.37   # Number of inches in 1 m
        d_inches = self.d*C
        if "D" not in kw:
            self.D = (1.654*d_inches + 0.0525)/C  # Is in m
        else:
            self.D = self.ToSI("D")
        if "t" not in kw:
            self.t = (0.2521*d_inches - 0.0010)/C  # Is in m
        else:
            self.t = self.ToSI("t")
        assert self.D > self.d
        assert self.t > 0
    def volume(self):
        return self.kw["n"]*self.neg()*pi/4*self.t*(self.D**2 - self.d**2)
class Nut(Primitive):
    '''Models a steel hex nut.  The parameters are:
    d = thread major diameter
    p = pitch
    tpi = threads per inch
    t = thickness
    Pitch is in default units; tpi is in inches.  If both are given, the
    pitch term takes priority.
    '''
    def __init__(self, linenum, line, opts, **kw):
        super(Nut, self).__init__(linenum, line, opts, **kw)
class Us2x4(Primitive):
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set(["L"])
        self.doc = "2x4:L=length"
        super(Us2x4, self).__init__(linenum, line, opts, **kw)
        self.b = (4 - 1/2)/39.37  # Standard width
    def volume(self):
        L = self.ToSI("L")
        a = (2 - 1/2)/39.37  # Standard thickness
        # We'll correct for the minor effect of a radius on four
        # edges.  The 2x4s I've measured have a 3/32 inch radius on
        # each edge.
        r = (3/32)/39.37
        # Subtract the volume of four spandrels
        A = a*self.b - (4 - pi)*r**2
        return self.kw["n"]*self.neg()*A*L
class Us2x6(Us2x4):
    def __init__(self, linenum, line, opts, **kw):
        self.doc = "2x6:L=length"
        super(Us2x6, self).__init__(linenum, line, opts, **kw)
        self.b = (6 - 1/2)/39.37  # Standard width
class Us2x8(Us2x4):
    def __init__(self, linenum, line, opts, **kw):
        self.doc = "2x8:L=length"
        super(Us2x8, self).__init__(linenum, line, opts, **kw)
        self.b = (8 - 3/4)/39.37  # Standard width
class Us2x10(Us2x4):
    def __init__(self, linenum, line, opts, **kw):
        self.doc = "2x10:L=length"
        super(Us2x10, self).__init__(linenum, line, opts, **kw)
        self.b = (10 - 3/4)/39.37  # Standard width
class Us2x12(Us2x4):
    def __init__(self, linenum, line, opts, **kw):
        self.doc = "2x12:L=length"
        super(Us2x12, self).__init__(linenum, line, opts, **kw)
        self.b = (12 - 3/4)/39.37  # Standard width
class Us4x4(Us2x4):
    def __init__(self, linenum, line, opts, **kw):
        super(Us4x4, self).__init__(linenum, line, opts, **kw)
        self.doc = "4x4:L=length"
        self.a = self.b = (4 - 1/2)/39.37  # Actual 3.5x3.5 inches
class Cap(Primitive):   # Spherical cap
    def __init__(self, linenum, line, opts, **kw):
        self.doc = "cap:r=radius, h=height"
        self.varnames = set("rh")
        super(Cap, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        r = self.ToSI("r")
        h = self.ToSI("h")
        return self.kw["n"]*self.neg()*pi*h**2*(r - h/3)
class Sph(Primitive):   # Sphere
    def __init__(self, linenum, line, opts, **kw):
        self.doc = "sphere:r=radius"
        self.varnames = set("r")
        super(Sph, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        r = self.ToSI("r")
        return self.kw["n"]*self.neg()*4/3*pi*r**3
class Hex(Primitive):   # Hexagonal bar stock
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("dL")
        self.doc = "hex:d=diam, L=length"
        super(Hex, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        d = self.ToSI("d")
        L = self.ToSI("L")
        A = sqrt(3)/2*d**2
        return self.kw["n"]*self.neg()*A*L
class Poly(Primitive):  # Polygonal bar stock
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set(("r", "L", "nsides"))
        self.doc = "poly:r=radius, L=length, nsides"
        super(Poly, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        r = self.ToSI("r")
        L = self.ToSI("L")
        nsides = self.kw["nsides"]
        if nsides < 3:
            msg = "Poly:  nsides must be >= 3\n"
            msg += "  Error in line {} of datafile".format(self.linenum)
            Error(msg)
        A = nsides*r**2*tan(pi/nsides)
        return self.kw["n"]*self.neg()*A*L
class Cone(Primitive):
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("rh")
        self.doc = "cone:r=radius, h=height"
        super(Cone, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        h = self.ToSI("h")
        r = self.ToSI("r")
        A = pi*r**2
        return self.kw["n"]*self.neg()*h*A/3
class Pyr(Primitive):   # Pyramid
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("Ah")
        self.doc = "pyr:A=area, h=height"
        super(Pyr, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        A = self.ToSI("A", is_area=True)
        h = self.ToSI("h")
        return self.kw["n"]*self.neg()*h*A/3
class Frust(Primitive):     # Generalized frustum
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set(("A1", "A2", "h"))
        self.doc = "frust:A1=area1, A2=area2, h=height"
        super(Frust, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        A1 = self.ToSI("A1", is_area=True)
        A2 = self.ToSI("A2", is_area=True)
        h = self.ToSI("h")
        return self.kw["n"]*self.neg()*h/3*(A1 + A2 + sqrt(A1*A2))
class Oct(Primitive):   # Octagonal bar stock
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("rL")
        self.doc = "oct:r=radius, L=length"
        super(Oct, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        L = self.ToSI("L")
        r = self.ToSI("r")
        A = 8*r**2*tan(pi/8)
        return self.kw["n"]*self.neg()*A*L
class Bbl(Primitive):   # Barrel
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("dDL")
        self.doc = "bbl:D=OD, d=end dia, L=length"
        super(Bbl, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        L = self.ToSI("L")
        d = self.ToSI("d")
        D = self.ToSI("D")
        return self.kw["n"]*self.neg()*pi*L*(2*D**2 + d**2)/12
class Cwedge(Primitive):
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set(("h1", "h2", "r"))
        self.doc = "cwedge:r=radius, h1=small height, h2=large height"
        super(Cwedge, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        h1 = self.ToSI("h1")
        h2 = self.ToSI("h2")
        r = self.ToSI("r")
        h = (h1 + h2)/2
        return self.kw["n"]*self.neg()*pi*r**2*h
class Ell(Primitive):   # Ellipsoid
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("abc")
        self.doc = "ell:a=semidia, b=semidia, c=semidia"
        super(Ell, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        # Note a, b, c are diameters, not semidiameters; the formula
        # is for semidiameters, which is why they are halved.
        a = self.ToSI("a")/2
        b = self.ToSI("b")/2
        c = self.ToSI("c")/2
        return self.kw["n"]*self.neg()*4/3*pi*a*b*c
class Lune(Primitive):
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set(("theta", "r"))
        self.doc = "lune:r=radius, theta=wedge angel"
        super(Lune, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        r = self.ToSI("r")
        theta = self.kw["theta"]*self.opts["angles"]
        return self.kw["n"]*self.neg()*2/3*theta*r**3
class Par(Primitive):  # Parallelopiped
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set(("a", "b", "c", "theta_ab", "theta_ac",
                             "theta_bc"))
        self.doc = "par:a,b,c=sides, theta_ac,theta_ab,theta_bc=angles"
        super(Par, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        a = self.ToSI("a")
        b = self.ToSI("b")
        c = self.ToSI("c")
        theta_ab = self.kw["theta_ab"]*self.opts["angles"]
        theta_ac = self.kw["theta_ac"]*self.opts["angles"]
        theta_bc = self.kw["theta_bc"]*self.opts["angles"]
        cab, cac, cbc = cos(theta_ab), cos(theta_ac), cos(theta_bc)
        V = a*b*c*sqrt(1 + 2*cab*cac*cbc - cab**2 - cac**2 - cbc**2)
        return self.kw["n"]*self.neg()*V
class Rev(Primitive):  # Solid of revolution
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("dA")
        self.doc = "rev:d=diameter, A=area"
        super(Rev, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        d = self.ToSI("d")
        A = self.ToSI("A", is_area=True)
        return self.kw["n"]*self.neg()*pi*d*A
class Sphs(Primitive):  # Spherical sector
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set(("r", "theta"))
        self.doc = "sphs:r=radius, theta=angle"
        super(Sphs, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        r = self.ToSI("r")
        theta = self.kw["theta"]*self.opts["angles"]
        return self.kw["n"]*self.neg()*2/3*theta*r**3
class Torus(Primitive):
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("rR")
        self.doc = "torus:r=cross-section radius, R=donut radius"
        super(Torus, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        r = self.ToSI("r")
        R = self.ToSI("R")
        return self.kw["n"]*self.neg()*2*pi**2*R*r**2
class User(Primitive):
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("V")
        self.doc = "user:V=volume"
        super(User, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        V = self.ToSI("V")*self.ToSI("V", is_area=True)
        return self.kw["n"]*self.neg()*V
class Wedge(Primitive):
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("abch")
        self.doc = "wedge:a=bottom, b=bottom, c=top, h=height"
        super(Wedge, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        a = self.ToSI("a")
        b = self.ToSI("b")
        c = self.ToSI("c")
        h = self.ToSI("h")
        return self.kw["n"]*self.neg()*b*h*(2*a + c)/6
class Ibeam(Primitive):
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("whtL")
        self.doc = "ibeam:w=width, h=height, t=edge thick., t1=web thick."
        super(Ibeam, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        w = self.ToSI("w")
        h = self.ToSI("h")
        t = self.ToSI("t")
        L = self.ToSI("L")
        t1 = t
        if "t1" in self.kw:
            t1 = self.ToSI("t1")
        return self.kw["n"]*self.neg()*(2*w*t + t1*(h - 2*t))*L
class Cbeam(Primitive):
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("whtL")
        self.doc = "cbeam:w=width, h=height, t=thickness"
        super(Cbeam, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        w = self.ToSI("w")
        h = self.ToSI("h")
        t = self.ToSI("t")
        L = self.ToSI("L")
        return self.kw["n"]*self.neg()*(2*t*h + (w - 2*t)*t)*L
class Tbeam(Primitive):
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("whtL")
        self.doc = "tbeam:w=width, h=height, t=thickness, t1=thickness"
        super(Tbeam, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        w = self.ToSI("w")
        h = self.ToSI("h")
        t = self.ToSI("t")
        L = self.ToSI("L")
        t1 = t
        if "t1" in self.kw:
            t1 = self.ToSI("t1")
        return self.kw["n"]*self.neg()*(w*t + (h - t)*t1)*L
class Angle(Primitive):
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("abtL")
        self.doc = "angle:a=leg1, b=leg2, t=a thick., t1=b thick."
        super(Angle, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        a = self.ToSI("a")
        b = self.ToSI("b")
        t = self.ToSI("t")
        L = self.ToSI("L")
        t1 = t
        if "t1" in self.kw:
            t1 = self.ToSI("t1")
        return self.kw["n"]*self.neg()*(a*t + t1*(b - t))*L
class Rectube(Primitive):
    def __init__(self, linenum, line, opts, **kw):
        self.varnames = set("abtL")
        self.doc = "rectube:a=width, b=height, t=thickness, L=length"
        super(Rectube, self).__init__(linenum, line, opts, **kw)
    def volume(self):
        a = self.ToSI("a")
        b = self.ToSI("b")
        t = self.ToSI("t")
        L = self.ToSI("L")
        return self.kw["n"]*self.neg()*(a*b - (a - 2*t)*(b - 2*t))*L
def Help():
    print(dedent('''
    Component keywords and their required parameters ({r, d} means a radius or
    diameter for a circular object):
        2x10        Standard US board with length L
        2x12        Standard US board with length L
        2x4         Standard US board with length L
        2x6         Standard US board with length L
        2x8         Standard US board with length L
        4x4         Standard US board with length L
        angle       Angle shape, w, h, t
        bbl         Barrel {R, D}, {r, d}, L
        cap         Spherical cap {r, d}, h
        cbeam       C-beam w, h, t
        cone        Cone {r, d}, h
        cwedge      Cylindrical wedge {r, d}, h1, h2
        cyl         Cylinder {r, d}, L
        ell         Ellipsoid a, b, c (diameters, not semidiameters)
        frust       Frustum A1, A2, h
        gcyl        Generalized cylinder A, L
        hex         Hexagonal bar stock {r, d}, L
        ibeam       I-beam w, h, t, t1
        lune        Wedge from a sphere {r, d}, theta
        oct         Octagonal bar stock {r, d}, L
        par         Parallelopiped a, b, c, theta_ac, theta_bc, theta_ab
        pipe        Round pipe {r, d}, t, L
        poly        Bar with regular polygon cross section {r, d}, nsides, L
        pyr         Pyramid A, h
        rect        Rectangular solid a, b, L
        rectube     Rectangular tubing a, b, t, L
        rev         Volume of an area rotated around an axis A, {r, d}
        sph         Sphere {r, d}
        sphs        Spherical sector {r, d}, theta
        T125        1.25 inch long Torx wood screw
        T150        1.5 inch long Torx wood screw
        T175        1.75 inch long Torx wood screw
        T200        2 inch long Torx wood screw
        T225        2.25 inch long Torx wood screw
        T250        2.5 inch long Torx wood screw
        T275        2.75 inch long Torx wood screw
        T300        3 inch long Torx wood screw
        T350        3.5 inch long Torx wood screw
        T400        4 inch long Torx wood screw
        tbeam       T-beam w, h, t, t1
        torus       Torus {R, D}, {r, d}
        user        User-defined V
        wedge       Ordinary wedge a, b, c, h
    
    Modifiers:
        n           Quantity of this part
        name        String describing component
        rho         Specify density in g/cc
        neg         A negative mass (i.e., a hole) if True
        material    A string to specify the material
    
    Control keywords:
        digits      How many significant figures in report
        angles      Factor to convert angle measure to radians
        material    Default material
        munit       Mass unit for report
        units       Default units to use for linear dimensions
        vunit       Volume unit for report
    '''))
def PrintDatafileExample(d):
    print(dedent(f'''
    # For a list of the keywords, modifiers, and control keywords, use the
    # -h command line option.  Also consult the mass.pdf instructions.
    
    # This is an example datafile for the mass.py script.  It can be used
    # as a template for a particular assembly by modifying and addng to
    # the included items.
    
    # Material:  Use the -l option for a listing of the available
    # materials.  Use the -L 3 option to see all materials supported by
    # the script.
    material concrete
    
    # Units:  define the default length units.  You can change units at
    # any time by using a new units statement.  Most common length units 
    # are supported; note SI prefixes can be used.
    units cm
    
    # Angles:  define the angle units.  This control keyword defines the
    # factor that converts angle measure to radians.  To have all angles
    # in degrees, use the following line.
    angles pi/180
    
    # Digits:  the number of significant figures in the printed report is
    # controlled by this number.
    digits 3
    
    # Mass unit:  this control keyword defines the mass unit to be used in
    # the report.
    munit kg
    
    # Volume unit:  specifies the volume unit to be used in the report.
    vunit cc
    
    #----------------------------------------------------------------------
    # Components:  each component of the composite assembly is defined by
    # a component line.  Each line requires certain keywords to specify
    # the dimension of the component.  Each keyword must be of the form
    # 'kw = value', followed by a comma.  Keywords can be:
    #
    # n         Number of components of this type.
    # name      String to identify the component.
    # rho       Density of the component in g/cc.
    # neg       Defines a negative component (i.e., a hole).
    # material  Uses a short string to identify the component's material.
    #
    # Here's an example that specifies a bar of steel with a cylindrical
    # cross section 3/4 length units in diameter and 15 length units long.
    # The component has the name "shaft 3".
    cyl d=3/4, L=15, material="steel", name="shaft 3"
    
    # Note:  when a diameter is needed, either the radius r can be given
    # or the diameter d can be given.  To understand all the keywords,
    # you'll need to look at the diagrams in the mass.pdf file.
    
    # Here are the component keywords:
    #
    # 2x10    4x4     cbeam   ell     ibeam           rect    sphs    tbeam
    # 2x12    angle   cone    frust   lune    pipe    rectube torus
    # 2x4     bbl     cwedge  gcyl    oct     poly    rev     user
    # 2x6     cap     cyl     hex     par     pyr     sph     wedge
    # 2x8
    # and the following Torx wood screw sizes (name is length in 1/100 inches):
    # T125    T150    T175    T200    T225    T250    T275    T300    T350
    # T400
    '''))
    exit(0)
def InterpretNumberSizeInInches(dia, linenum, line):
    '''dia begins with 'no' and must be followed by an integer.
    The number returned is in inches.
    '''
    msg = ("Bad 'dia' parameter in line {} for number-sized US"
           " screw\n".format(linenum))
    msg += "  Line :  '{}'".format(line)
    try:
        n = int(dia[2:])
        if n < 0:
            Error(msg)
        return (0.013*n + 0.06)
    except Exception as e:
        msg += "  Error:  '{}'".format(str(e))
        Error(msg)
def InterpretFraction(dia, linenum, line):
    '''dia is a string that contains '/'.  Pick it apart and return a
    float.  Note we'll allow forms like '1-1/4', '1+1/4' and '1 1/4' to
    mean the same thing.  Note:  this only interprets the fraction;
    the units are not necessarily inches.
    '''
    s = dia.replace("-", "+")
    s = dia.replace(" ", "+")
    # Now just evaluate it as an expression
    try:
        d = float(eval(s))
        return d
    except Exception as e:
        msg = "Bad 'dia' parameter in line {}\n".format(linenum)
        msg += "  Line :  '{}'\n".format(line)
        msg += "  Error:  '{}'".format(str(e))
        Error(msg)
def DictToStr(d, ignore=set()):
    '''Convert a dictionary of keywords to a compact string.  Note we
    don't include a title variable if it is defined.  Any strings in the
    container ignore are not returned.
    '''
    s = []
    keys = list(d.keys())
    keys.sort()
    sig = SigFig()
    sig.rtz = True
    for k in keys:
        if k == "title" or k in ignore:
            continue
        if isinstance(k, str):
            t = k + "="
            v = d[k]
            if isinstance(v, str):
                t += repr(v)
            elif isinstance(v, int):
                t += str(v)
            else:
                t += sig(v)
            s.append(t)
    s.sort(key=str.lower)
    return ' '.join(s)
def ParseCommandLine(d):
    sig.digits = 3
    GetMaterialDictionary(d)
    # Set the defaults
    d["sep_char"] = ","     # What keyword expressions are separated by
    d["digits"] = 3
    d["-d"] = None          # Command line number of significant figures
    d["default_material"] = "steel"
    # Factor to convert angles to radians.  Set it to pi/180
    # if you want the default to be degrees.
    d["angles"] = 1
    d["on"] = ".on"
    d["off"] = ".off"
    # Default units
    d["units"] = "cm"
    d["munit"] = "g"
    d["vunit"] = "cc"
    # Specific gravity of default material
    d["rho"] = d["materials"][d["default_material"]][1]
    d["-i"] = False         # Interactive mode
    d["-l"] = False         # Print material list
    d["-n"] = False         # Don't print header
    d["-L"] = 1             # Material levels to print
    d["-s"] = False         # Print summary of objects
    d["-v"] = False         # Verbosity in report
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "cDd:hiL:lnsv")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for opt in optlist:
        if opt[0] == "-c":
            PrintDatafileExample(d)
            exit(0)
        elif opt[0] == "-d":
            d["-d"] = max(int(opt[1]), 1)
            sig.digits = d["-d"]
        elif opt[0] == "-h":
            Help()
            exit(0)
        elif opt[0] == "-i":
            d["-i"] = not d["-i"]
        elif opt[0] == "-L":
            d["-L"] = max(int(opt[1]), 1)
        elif opt[0] == "-l":
            d["-l"] = not d["-l"]
        elif opt[0] == "-n":
            d["-n"] = not d["-n"]
        elif opt[0] == "-s":
            d["-s"] = not d["-s"]
        elif opt[0] == "-v":
            d["-v"] = not d["-v"]
    if len(args) != 1 and not d["-l"] and not d["-i"] and not d["-s"]:
        Usage(d)
    if d["-i"] or d["-s"]:
        return None
    if not d["-l"]:
        return args[0]
def ShowUnits():
    '''Print the various units allowed to stdout.
    '''
    def Strip(s):
        return str(s).replace("[", "").replace("]", "").replace("'", "")
    def Lst(lst):
        k = list(lst.keys())
        k.sort()
        return Strip(k)
    SI_prefixes_order = ("y", "z", "a", "f", "p", "n", "u", "m", "c", "d",
                         "da", "h", "k", "M", "G", "T", "P", "E", "Z", "Y")
    si = Strip(list(SI_prefixes_order))
    # Get their logs
    sil = ""
    for i in SI_prefixes_order:
        sil += "{:4d}".format(_SI_prefixes[i])
    linear = Lst(_allowed_linear_units)
    mass = Lst(_allowed_mass_units)
    vol = Lst(_allowed_volume_units)
    print(dedent(f'''
    SI prefixes and their base 10 logs:
       {si}
    {sil}
    
    Linear units
    ------------
    {linear}
    
    Mass units
    ----------
    {mass}
    
    Volume units (besides cubes of linear units)
    --------------------------------------------
    {vol}
    '''))
def GetShapes(d):
    '''Insert a dictionary into d keyed by 'shapes' that lists the
    component names in the datafile keyed to the class that will
    instantiate that object.
    '''
    ignore = '''CommandDecode SigFig StringIO UFloat UnifiedThread'''.split()
    shapes = {}
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if name in ignore:
            continue
        if inspect.isclass(obj):
            s = str(obj).split()[1].replace("'", "")
            cls = s.split(".")[1].replace(">", "")
            nm = cls.lower()
            # Handle the special case of 2x4, etc. by removing the
            # leading "us".
            if nm[:2] == "us" and nm != "user":
                nm = nm[2:]
            exec('shapes["{}"] = {}'.format(nm, cls))
    # Add some synonyms
    for i, j in (
        ("sphere", "sph"),
        ("polygon", "poly"),
        ("barrel", "bbl"),
        ("cylinder", "cyl"),
        ("ellipsoid", "ell"),
        ("frustum", "frust"),
        ("hexagon", "hex"),
        ("octagon", "oct"),
        ("parallelopiped", "par"),
        ("pyramid", "pyr"),
        ("rectangular", "rect"),
        ("rectangular_tubing", "rectube"),
        ("solid_of_revolution", "rev"),
        ("spherical_sector", "sphs"),
    ):
        shapes[i] = shapes[j]
    d["shapes"] = shapes
def GetUnitsFactor(unit_str, linenum, line):
    '''Interpret the given unit_str string and return a factor that
    converts these units to m.
    '''
    msg = "'{}' is an improper unit string in line {} of datafile".format(
        unit_str, linenum)
    msg += "\n  '{}'".format(line)
    if unit_str in _allowed_linear_units:
        # It's a base unit with no prefix
        return _allowed_linear_units[unit_str]
    else:
        # See if it has an SI prefix
        try:
            prefix, unit = unit_str[0], unit_str[1:]
            if prefix in _SI_prefixes and unit in _allowed_linear_units:
                factor = 10**_SI_prefixes[prefix]
                return _allowed_linear_units[unit]*factor
            else:
                Error(msg)
        except IndexError:
            Error(msg)
def PrintMaterials(d):
    print("Materials List (ShortID, name, and mass density in g/cc)")
    # Set up sig to line up decimal points
    sig.dp_position = 4
    sig.fit = maxrho = 12
    sig.lead_zero = False
    sig.low = 1e-6
    sig.rtz = True
    # Find max sizes of strings
    maxid, maxname = 0, 0
    for i in _materials:
        for include, id, name, rho in _materials[i]:
            if not include or (include and include > d["-L"]):
                continue
            maxid = max(len(id), maxid)
            maxname = max(len(name), maxname)
    # Print by sorted keys
    keys = list(_materials.keys())
    keys.sort()
    for key in keys:
        print(key)
        items = list(_materials[key])
        items.sort(key=lambda x: x[1])
        for include, id, name, _rho in items:
            if not include or (include and include > d["-L"]):
                continue
            if _rho:
                rho = sig(_rho)
            else:
                rho = "  zero"
            s = "    {id:{maxid}}  {name:{maxname}}  {rho:{maxrho}}"
            print(s.format(**locals()))
def GetVar(__line, __linenum, __vars):
    '''Return a dictionary containing the evaluated variable
    assignment.  __vars is a dictionary of already-defined variables.
    '''
    # Add the variables in __vars to our local namespace
    for __k in __vars:
        exec("{} = __vars['{}']".format(__k, __k))
    # Evaluate the new variable
    try:
        exec(__line)
    except Exception as __e:
        __msg = "Line {} in datafile is an incorrect assignment:\n '{}'"
        __msg = __msg.format(__linenum, __line)
        __msg += "\n  Error:  {}".format(str(__e))
        Error(__msg)
    # Remove the variables starting with double underscores and return
    # the locals dictionary.
    vars, rm = locals(), []
    for i in vars:
        if len(i) > 2 and i[:2] == "__":
            rm.append(i)
    for i in rm:
        del vars[i]
    return vars
def GetMaterialDictionary(d):
    '''Add the materials dictionary to d under the key "materials"
    that is indexed by the ShortID of the material name.  The values
    are tuples of the material name and specific gravity in g/cc.
    Ensure that the ShortIDs given are unique.
    '''
    D = {}
    for i in _materials:
        for include, id, name, rho in _materials[i]:
            if id in D:
                Error("'{}' is a duplicated ShortID in _materials dict".format(id))
            else:
                D[id] = (name, rho)
    d["materials"] = D
def GetKeywords(__linenum, __line, __list_of_expr, __vars):
    '''Given a list of expressions and a dictionary of variables __vars,
    evaluate the expressions and return a dictionary containing the
    numbers.
    '''
    # NOTE:  the double underscores in this function are used to keep the
    # function's local variables out of the returned dictionary.
    # Import the variables into our local namespace.
    for __k in __vars:
        exec("{} = __vars['{}']".format(__k, __k))
    # Evaluate each item
    for __item in __list_of_expr:
        try:
            exec(__item.strip())
        except SyntaxError:
            # This is probably caused by an attached unit.  We'll
            # surround the right-hand side by quotes and let a later
            # chunk of code process the number and unit.
            __s = __item.replace("=", '="') + '"'
            try:
                exec(__s.strip())
            except Exception as e:
                msg = "Line {} in datafile had an evaluation error:\n '{}'"
                msg += "\n  Error:  {}"
                Error(msg.format(__linenum, __line, str(e)))
    # Get the locals dictionary, delete the items that begin with two
    # underscores, and return it.
    vars, rm = locals(), []
    for i in vars:
        if i.startswith("__"):
            rm.append(i)
    for i in rm:
        del vars[i]
    return vars
def md5(file):
    '''Return MD5 hex hash of file.
    '''
    m = hashlib.md5()
    m.update(open(file).read().encode("utf-8"))
    return m.hexdigest()
def GetComponents(data, matl, d):
    '''Return a list of the components in the model; each item will be
    an object whose volume and mass can be calculated.  The order of
    the items in the list is the order they were encountered in the
    datafile.

    data is a dictionary with keys 'lines' and 'vars'.  The 'lines' is
    a sequence of each relevant line in the data file; each item is a
    tuple of the line number and the string making up the line.

    vars is a dictionary of variables that the user defined.

    matl is a dictionary that maps the ShortID to the mass density in
    g/cc.
    '''
    comp = []
    # Process each line
    for linenum, line in data['lines']:
        f = line.split()
        cmd = f[0]
        if f[0] not in cmds:
            msg = "Line {} in datafile is bad:\n  '{}'".format(linenum, line)
            Error(msg)
        if cmd not in ("matl", "units", "unit"):
            # Get keywords
            s = ' '.join(f[1:])
            list_of_expr = s.split(",")
            kw = GetKeywords(linenum, line, list_of_expr, data["vars"])
        if cmd == "matl":
            if f[1] not in matl:
                msg = "Material '{}' in line {} of datafile unrecognized"
                Error(msg.format(f[1], linenum))
            global default_material
            default_material = f[1]
        elif cmd == "rect":
            comp.append(Rect(linenum, line, **kw))
    return comp
def Eval(linenum, line, expr, vars):
    '''expr is an expression; evaluate it using the variables in vars.
    '''
    try:
        x = eval(expr, globals(), vars)
        return x
    except Exception as e:
        msg = "Bad expression in line {}:\n  '{}'\n  Error:  {}"
        Error(msg.format(linenum, line, str(e)))
def RemoveComment(line, nostrip=None):
    loc = line.find("#")
    if loc != -1:
        line = line[:loc]
    return line.strip() if nostrip is None else line
def GetSci(num, digits, fit):
    '''The number can't be displayed with sig, so change to scientific
    notation and center in fit spaces.
    '''
    if num:
        s = "{:.{}e}".format(digits - 1, num)
        return "{0:^{1}}".format(s, fit)
    else:
        return "{0:^{1}}".format(0, fit)
def GetVal(x, digits, fit):
    bad = "-.-"
    try:
        s = sig(x)
        if s.strip() == bad:
            s = GetSci(x, digits, fit)
            while len(s) < fit:
                s += " "
    except ValueError:
        s = GetSci(x, digits, fit)
        while len(s) < fit:
            s += " "
    return s
def Report(d):
    if d["-v"]:
        print("Components:")
        Primitive.ignore = d["vars"]
        for i in d["components"]:
            print(" ", str(i))
        print()
    nm = 20     # Width of component column
    fit = 16    # Width of mass & volume columns
    pfit = 10   # Width of "% of total" columns
    tm = time.asctime()
    datafile = d["datafile"]
    pgm = sys.argv[0]
    pgm_md5 = md5(pgm)
    df_md5 = md5(datafile)
    vunit = d["vunit"]
    if u.dim(vunit) != u.dim("m3"):
        Error("vunit doesn't have the dimensions of volume")
    munit = d["munit"]
    if u.dim(munit) != u.dim("kg"):
        Error("munit doesn't have the dimensions of mass")
    if d["-d"] is not None:
        sig.digits = d["-d"]  # Overrides digits keyword in datafile
    else:
        sig.digits = d["digits"]
    digits = sig.digits
    if not d["-n"]:
        print(dedent(f'''
        Mass/volume calculation
        -----------------------
          {tm}
        '''))
        if "title" in d["vars"]:
            title = d["vars"]["title"]
            print(f"  {title}")
        print(dedent(f'''
      Name of datafile     = {datafile}
      MD5 hash of datafile = {df_md5}
      ''', n=4))
        if d["material"] is not None:
            print("  Material is", d["material"])
            print("  Material specific gravity =", d["rho"])
        else:
            print("  Material specific gravity =", d["rho"])
        print()
    # Get positive and negative masses
    pM, pV, nM, nV = 0, 0, 0, 0
    for c in d["components"]:
        m = c.mass()
        if m < 0:
            nM += m
        else:
            pM += m
        v = c.volume()
        if v < 0:
            nV += v
        else:
            pV += v
    mass = "{0:^{1}}".format(munit, fit)
    volume = "{0:^{1}}".format(vunit, fit)
    hyph = "-"*fit
    phyph = "-"*pfit
    chyph = "-"*nm
    pof = "{0:^{1}}".format("% of", pfit)
    mss = "{0:^{1}}".format("Mass", fit)
    vol = "{0:^{1}}".format("Volume", fit)
    ttl = "{0:^{1}}".format("Total", pfit)
    nmst = "{0:^{1}}".format("Component", nm)
    nms = "{0:^{1}}".format("[x] is line no.", nm)
    # Print table header
    print(dedent(f'''
    {nms} {mss} {pof} {vol} {pof}
    {nmst} {mass} {ttl} {volume} {ttl}
    {chyph} {hyph} {phyph} {hyph} {phyph}
    '''))
    sig.high = 1e6
    sig.low = 1e-6
    sig.rtz = False
    mcf = to(1, munit)/1000
    vcf = to(1, vunit)
    fmt = "{name:{nm}} {ms} {mf} {vs} {vf}"
    bad = "-.-"
    for c in d["components"]:
        name = c.kw["name"] if "name" in c.kw else c.id()
        if "name" not in c.kw and name[:2] == "Us" and name[:4] != "User":
            name = name[2:]
        if len(name) > nm:
            name = name[:nm]
        v = c.volume()
        m = c.mass()        # mass is in g
        sig.fit = fit
        sig.dp_position = fit//2
        tl = "Too large"
        try:
            ms = sig(m*mcf)
            if ms.strip() == bad:
                ms = GetSci(m*mcf, digits, fit)
        except ValueError:
            ms = GetSci(m*mcf, digits, fit)
            while len(ms) < fit:
                ms += " "
        try:
            vs = sig(v*vcf)
            if vs.strip() == bad:
                vs = GetSci(v*vcf, digits, fit)
        except ValueError:
            vs = GetSci(m*mcf, digits, fit)
            while len(vs) < fit:
                vs += " "
        sig.fit = pfit
        sig.dp_position = pfit//2
        try:
            if m < 0:
                mf = sig(-100*m/nM)
            else:
                mf = sig(100*m/pM)
        except ZeroDivisionError:
            mf = sig(0)
        try:
            if v < 0:
                vf = sig(-100*v/nV)
            else:
                vf = sig(100*v/pV)
        except ZeroDivisionError:
            vf = sig(0)
        print(fmt.format(**locals()))
    # Print totals
    print("{chyph} {hyph} {phyph} {hyph} {phyph}".format(**locals()))
    sig.fit = fit
    sig.dp_position = fit//2
    TpM = GetVal(pM*mcf, digits, fit)
    TpV = GetVal(pV*vcf, digits, fit)
    TnM = GetVal(nM*mcf, digits, fit)
    TnV = GetVal(nV*vcf, digits, fit)
    TM = GetVal(mcf*(pM + nM), digits, fit)
    TV = GetVal(vcf*(pV + nV), digits, fit)
    # Positive total
    name = "Total positive"
    ms, mf = TpM, " "*pfit
    vs, vf = TpV, " "*pfit
    print(fmt.format(**locals()))
    # Negative total
    name = "Total negative"
    ms, mf = TnM, " "*pfit
    vs, vf = TnV, " "*pfit
    print(fmt.format(**locals()))
    # Totals
    print("{chyph} {hyph} {phyph} {hyph} {phyph}".format(**locals()))
    name = "Total net"
    ms, mf = TM, " "*pfit
    vs, vf = TV, " "*pfit
    print(fmt.format(**locals()))
def GetLeadingSpaceCount(line):
    count = 0
    while len(line[:count]) < len(line) and line[count] == " ":
        count += 1
    return count
def ReadDatafile(d):
    '''Add to the settings dictionary d a list of component objects as
    found in the datafile under the key "components" and a dictionary
    of the user's defined variables under the key "vars".
    '''
    names, code, indent, ignore = set(), None, None, False
    d["vars"], d["components"] = {}, []
    lines = open(d["datafile"]).readlines()
    for i, Line in enumerate(lines):
        if ignore:
            continue
        if Line.strip() == "{":
            code = []
            continue
        elif Line.strip() == d["off"]:
            ignore = True
            continue
        elif Line.strip() == d["on"]:
            ignore = False
            continue
        line = RemoveComment(Line, nostrip=code)
        if not line:
            continue
        linenum = i + 1
        if code is not None:
            if line.lstrip() == "}\n":
                # The chunk of code has ended, so execute it.  Use the
                # defined globals and vars as our local variables.
                co = compile(''.join(code), "User code block", "exec")
                exec(co, globals(), d["vars"])
                code, indent = None, None
                continue
            if indent is None:
                # This is the first line, so utilize its leading
                # space characters as the indent (and, thus, remove
                # this indent from all subsequent lines in this
                # block).
                indent = GetLeadingSpaceCount(Line)
            # Remove the indicated space characters.  First check
            # that there's no inconsistent indent.
            if line[:indent] != " "*indent:
                msg = ("Line {} of datafile has an inconsistent indent:\n"
                       "  (It needs to be {} space characters)\n"
                       "  Line = '{}'".format(linenum, indent, Line.rstrip()))
                if "\t" in line[:indent]:
                    msg += "\n  (Note it contains a tab character)"
                Error(msg)
            line = line[indent:]
            code.append(line)   # Accumulate the lines
            continue
        f = line.split()
        if len(f) > 2 and f[1] == "=":
            # It's a variable assignment.  Add the definition to
            # the vars dictionary.
            d["vars"] = GetVar(line, linenum, d["vars"])
        elif f[0] in d["shapes"]:
            shape = f[0]
            # Create the associated shape object.  Get a list of the
            # keywords by splitting on the sep character.
            list_of_expr = ' '.join(f[1:]).split(d["sep_char"])
            kw = GetKeywords(linenum, line, list_of_expr, d["vars"])
            if "rho" not in kw:
                if "material" in kw:
                    kw["rho"] = d["materials"][kw["material"]][1]
                else:
                    kw["rho"] = d["rho"]  # Use current default material
            elif isinstance(kw["rho"], (int, float)):
                pass
                # This means setting rho to a number overrides setting
                # the material.
            elif isinstance(kw["rho"], str):
                kw["rho"] = d["materials"][kw["rho"]][1]
            if "name" in kw:
                if kw["name"] in names:
                    msg = dedent(f'''
                    Error in line {linenum} of datafile:
                      '{kw["name"]}' is already used for a name.''')
                    Error(msg)
                else:
                    names.add(kw["name"])
            if "un" not in kw:
                try:
                    # Make sure it can be converted
                    u(d["units"])
                except Exception:
                    Error('Bad d["units"] setting')
                kw["un"] = d["units"]  # Use default units
            obj = d["shapes"][f[0]]
            d["components"].append(obj(linenum, line, d, **kw))
        elif f[0] in _control_cmds:
            # It's a control command.  Adjust the relevant variable in d.
            expr = " ".join(f[1:])
            if f[0] == "angles":
                d["angles"] = Eval(linenum, line, expr, d["vars"])
            elif f[0] == "del":
                try:
                    del d["vars"][f[1]]
                except KeyError:
                    msg = "Variable '{}' not defined in line {}\n"
                    msg += "  Line = '{}'"
                    Error(msg.format(f[1], linenum, line))
            elif f[0] == "digits":
                d["digits"] = Eval(linenum, line, expr, d["vars"])
            elif f[0] == "material":
                d["material"] = None
                if f[1] in d["materials"]:
                    matl = d["materials"][f[1]]
                    d["rho"] = matl[1]
                    d["material"] = "{} ({})".format(f[1], matl[0])
                else:
                    # Assume it's a numerical expression
                    try:
                        # Put it back together in case it contained
                        # spaces.
                        d["rho"] = float(eval(expr))
                    except Exception:
                        msg = "Bad density in line {}\n"
                        msg += "  Line = '{}'"
                        Error(msg.format(linenum, line))
            elif f[0] in ("units", "munit", "vunit"):
                # We have to handle a few cases.  The common case is
                # that f will have two elements; the second element
                # will be the unit to use.

                # The auxiliary case is where f has more than two
                # units because the line had more than one space
                # character.  An example would be 'vunit trailer in3'
                # where trailer is a defined variable (or it could be
                # an expression) and in3 is the unit identifier.  We
                # will make the assumption that if len(f) > 2, then
                # f[1:-1] is the expression to evaluate and f[-1] is
                # the physical unit string.
                if len(f) == 2:
                    # It's just a single unit string
                    try:
                        u(f[1])
                        value = f[1]
                    except Exception:
                        msg = ("'{}' in line {} is an unrecognized unit\n"
                               "  Line = '{}'".format(f[1], linenum, line))
                        Error(msg)
                elif len(f) >= 3:
                    expr = ''.join(f[1:-1])
                    # Make it a number
                    try:
                        value = str(eval(expr, None, d["vars"]))
                    except Exception as e:
                        msg = ("Error in line {}:\n"
                               "  Line  = '{}'\n"
                               "  Error = '{}'".format(linenum, line, str(e)))
                        Error(msg)
                    # Check the physical unit and append it
                    try:
                        u(f[-1])
                        value += " " + f[-1]
                    except Exception:
                        msg = ("'{}' in line {} is an unrecognized unit\n"
                               "  Line = '{}'".format(f[1], linenum, line))
                        Error(msg)
                else:
                    Error("Line {} in data file is bad: Line = '{}'".format(
                        linenum, line))
                d[f[0]] = value
            else:
                msg = "Software bug:  '{}' is an unimplemented control command"
                raise RuntimeError(msg.format(f[0]))
        else:
            # This could be an assignment line such as 'a, b = 1, 2' or
            # some other valid python expression.  We'll exec the line and
            # if we get an exception, then we'll declare the line invalid.
            try:
                exec(line, globals(), d["vars"])
            except Exception:
                msg = "'{}' in line {} is an unrecognized command:\n  Line = '{}'"
                Error(msg.format(f[0], linenum, line))
def Get(msg, default):
    s = input(msg).strip()
    if s.lower() == "q":
        exit(0)
    return default if not s else s
def GetLinearDimension(msg, d, allow_zero=False):
    '''Return the dimension in m.
    '''
    while True:
        s = input(msg)
        try:
            val, unit = ParseUnit(s, allow_quit=True)
            try:
                value = float(val)
            except ValueError:
                print("'{}' is not a number, try again.".format(val))
                continue
            try:
                conv_factor = u(d["length_units"])
            except NameError:
                print("'{}' is not a recognized unit, try again".format(d["length_units"]))
                continue
            if allow_zero:
                if value < 0:
                    print("Value must be >= 0; try again.")
                    continue
                return value*conv_factor
            else:
                if value <= 0:
                    print("Value must be > 0; try again.")
                    continue
                return value*conv_factor
        except ValueError:
            print("Couldn't parse number and unit; try again.")
def PrintObjectSummary(d):
    print("Object summary:")
    kw = {"rho": 1, "un": "in", "L": 1, "a": 1}
    for i in ("L a b c w h t t1 t2 r R A d D h1 h2 theta A1 A2 s "
              "theta_ac theta_ab theta_bc nsides n V".split()):
        kw[i] = 1
    objects = (
        Rect(0, 0, d, **kw),
        Cyl(0, 0, d, **kw),
        Gcyl(0, 0, d, **kw),
        Pipe(0, 0, d, **kw),
        Us2x4(0, 0, d, **kw),
        Us2x6(0, 0, d, **kw),
        Us2x8(0, 0, d, **kw),
        Us2x10(0, 0, d, **kw),
        Us2x12(0, 0, d, **kw),
        Us4x4(0, 0, d, **kw),
        Cap(0, 0, d, **kw),
        Sph(0, 0, d, **kw),
        Hex(0, 0, d, **kw),
        Poly(0, 0, d, **kw),
        Cone(0, 0, d, **kw),
        Pyr(0, 0, d, **kw),
        Frust(0, 0, d, **kw),
        Oct(0, 0, d, **kw),
        Bbl(0, 0, d, **kw),
        Cwedge(0, 0, d, **kw),
        Ell(0, 0, d, **kw),
        Lune(0, 0, d, **kw),
        Par(0, 0, d, **kw),
        Rev(0, 0, d, **kw),
        Sphs(0, 0, d, **kw),
        Torus(0, 0, d, **kw),
        User(0, 0, d, **kw),
        Wedge(0, 0, d, **kw),
    )
    for o in objects:
        a, b = o.doc.split(":")
        print("  {:8s}".format(a + ":"), b)
def Interactive(opts):
    '''Prompt for a geometry and material; print the volume and mass.
    '''
    # Length unit
    du = "inch"
    du = "mm"
    while True:
        opts["length_units"] = Get("Default length unit [{}]?  ".format(du), du)
        try:
            u(opts["length_units"])
            break
        except NameError:
            print("'{}' is not a recognized unit.\n".format(opts["length_units"]))
    # Shape
    allowed_shapes = "box cylinder frustum sphere cap pipe bar torus".split()
    default_shape = "cylinder"
    print("Shape:\n ", ' '.join(allowed_shapes))
    cmd = CommandDecode(allowed_shapes)
    while True:
        shape = input("Choose the shape (default = '{}'): ".format(default_shape)).strip()
        if not shape:
            shape = default_shape
            break
        elif len(shape) == 1 and shape[0].lower() == "q":
            exit(0)
        else:
            choice = cmd(shape)
            if len(choice) == 1:
                shape = choice[0].lower()
                break
            elif len(choice) > 1:
                print("Ambiguous choice; it could be:\n  {}".format(' '.join(choice)))
            else:
                print("'{}' not a recognized shape; try again.".format(choice))
    if shape == "box":
        L = GetLinearDimension("What is length?  ", opts)
        W = GetLinearDimension("What is width?  ", opts)
        H = GetLinearDimension("What is height?  ", opts)
        volume_m3 = L*W*H
    elif shape == "cylinder":
        D = GetLinearDimension("What is diameter?  ", opts)
        L = GetLinearDimension("What is length?  ", opts)
        volume_m3 = pi/4*D**2*L
    elif shape == "frustum":  # Right circular frustum
        print("(Note this is a right circular frustum)")
        D = GetLinearDimension("What is large diameter?  ", opts)
        d = GetLinearDimension("What is small diameter (zero OK)?  ", opts,
                               allow_zero=True)
        H = GetLinearDimension("What is height?  ", opts)
        A0, A1 = pi/4*d**2, pi/4*D**2
        volume_m3 = H/3*(A1 + A0 + sqrt(A1*A0))
    elif shape == "sphere":
        D = GetLinearDimension("What is sphere diameter?  ", opts)
        volume_m3 = 4/3*pi*(D/2)**3
    elif shape == "cap":
        D = GetLinearDimension("What is sphere diameter?  ", opts)
        H = GetLinearDimension("What is cap height?  ", opts)
        volume_m3 = pi*H**2*(D/2 - H/3)
    elif shape == "pipe":
        D = GetLinearDimension("What is outside diameter?  ", opts)
        d = GetLinearDimension("What is inside diameter?  ", opts)
        L = GetLinearDimension("What is length?  ", opts)
        volume_m3 = pi/4*(D**2 - d**2)*L
    elif shape == "bar":
        nsides = GetNumber("How many sides to the regular polygon?  ",
                           numtype=int, low=3, default=6)
        D = GetLinearDimension("What is inscribed diameter?  ", opts)
        L = GetLinearDimension("What is length?  ", opts)
        r = D/2
        A = nsides*r**2*tan(pi/nsides)
        volume_m3 = A*L
    elif shape == "torus":
        D = GetLinearDimension("What is inside diameter?  ", opts,
                               allow_zero=True)
        d = GetLinearDimension("What is the torus cross-section's diameter?  ", opts)
        r = d/2
        R = D/2 + r
        volume_m3 = 2*pi**2*R*r**2
    # Get the material
    GetMaterialDictionary(opts)
    materials = set(opts["materials"].keys())
    cmd, specific_gravity = CommandDecode(materials, ignore_case=True), None
    while True:
        choice = None
        s = "What is the material or specific gravity (use '?' for list)?  "
        material = input(s)
        if not material:
            # Default choice is no material, so don't print mass
            break
        if material.lower() in set("qQ"):
            exit(0)
        # See if it's a number
        try:
            specific_gravity = float(material)
            break
        except ValueError:
            pass
        if material == "?":
            m = [" "*2+i for i in sorted(list(materials))]
            for i in Columnize(m):
                print(i)
            continue
        else:
            choice = cmd(material)
            if len(choice) == 1:
                material = choice[0].lower()
                break
            elif not choice:
                print("'{}' not recognized; try again".format(material))
                continue
            else:
                print("Ambiguous material choice:")
                m = opts["materials"]
                for i in choice:
                    print("  ", i, "= {} [{:.2f} g/cc]".format(*m[i]))
                continue
            break
    print()
    if choice is not None:
        print("Material choice =", material, "= {} [{:.2f} g/cc]".format(
              *opts["materials"][choice[0]]))
    # Print volume
    v = volume_m3/u(opts["length_units"] + "3")
    if opts["-d"] is None:
        opts["-d"] = 4
        sig.digits = opts["-d"]
    s = "Volume ="
    indent = " "*len(s)
    print(s)
    print(indent, "{} m3".format(sig(volume_m3)))
    print(indent, "{} mm3".format(sig(volume_m3*1000**3)))
    print(indent, "{} cc".format(sig(volume_m3*100**3)))
    print(indent, "{} gal".format(sig(volume_m3*264.172)))
    print(indent, "{} ft3".format(sig(volume_m3*35.3147)))
    print(indent, "{} {}3".format(sig(v), opts["length_units"]))
    # Print mass
    if choice is not None:
        if specific_gravity is None:
            name, specific_gravity = opts["materials"][material]
        mass_kg = 1000*specific_gravity*volume_m3
        mass_lb = 2.20462*mass_kg
        print("Mass =")
        print(indent, "{} kg".format(sig(mass_kg)))
        print(indent, "{} tonne".format(sig(mass_kg/1000)))
        print(indent, "{} g".format(sig(1000*mass_kg)))
        print(indent, "{} lbm".format(sig(mass_lb)))
        print(indent, "{} oz".format(sig(mass_lb*16)))
        print(indent, "{} ton".format(sig(mass_lb/2000)))
        print("Mass = {} kg = {} g = {} lbm".format(sig(mass_kg), 
              sig(1000*mass_kg), sig(mass_lb)))
    exit(0)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] datafile
      Calculate the mass and volume of the composite object defined in the
      datafile.  See the mass.pdf file for usage details.
    Options:
      -c    Print a commented datafile example
      -d n  Set the number of significant digits in the output.  Defaults
            to 3 and overrides the digits setting in the datafile.
      -h    Print out the supported keywords
      -i    Interactively prompt for a geometric shape and material, then
            print the resulting mass.
      -L n  Set the level number n (an integer > 0) that determines
            which materials are shown.  The default is 1; this shows the
            most basic materials.  As the number increases, more materials
            are shown and used.  You can edit the materials dictionary to
            determine the types and levels of different materials.
      -l    Print a list of the materials.  Use the -L option to see more
            materials.
      -n    Don't print the header
      -s    Print a summary of the geometric objects and their parameters
      -v    Before printing the report, print out the strings that
            represent the components defined in the datafile in the order
            they are encountered.
    '''))
    exit(status)
if __name__ == "__main__":
    d = {}          # Options dictionary
    GetShapes(d)    # Populate d["shapes"] with allowed shape IDs
    d["datafile"] = ParseCommandLine(d)
    if d["-l"]:
        PrintMaterials(d)
    elif d["-i"]:
        Interactive(d)
    elif d["-s"]:
        PrintObjectSummary(d)
    else:
        GetMaterialDictionary(d)
        ReadDatafile(d)
        Report(d)
