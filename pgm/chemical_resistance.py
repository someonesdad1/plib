if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2015 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Chemical resistance of plastics
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    import re
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    plastic_details = {
        "ABS": "Acrylonitrile butadiene styrene",
        "Acetal": "Delrin",
        "Acrylic": "Polymethylmethacrylate (e.g., Lucite, Plexiglas)",
        "CAB": "Cellulose acetate butyrate",
        "CPVC": "Chlorinated polyvinyl chloride",
        "ECTFE (Halar)": "Ethylene chlorotrifluoroethylene",
        "Fluorosint": "Enhanced PTFE",
        "HDPE": "High-density polyethylene",
        "Nylon 6/6": "Polyamide",
        "PEEK": "Polyether ether ketone",
        "PET": "Polyethylene terephthalate",
        "Polycarbonate": "Lexan is one trade name",
        "Polypropylene": "",
        "Polysulfone": "",
        "PPS": "Polyphenylene sulfide",
        "PVC Type 1": "Polyvinyl chloride",
        "PVC Type 2": "Polyvinyl chloride, more impact resistant",
        "PVDF": "Polyvinylidene fluoride",
        "PTFE": "Polytetrafluoroethylene (Teflon)",
        "Tecalor/Torlon": "",
        "UHMW": "Ultra-high molecular weight polyethylene",
    }
def GetData():
    '''Return (plastics, chemicals) where plastics is a list of the
    plastics' names and chemicals is a list of lists:
    [
        ["Chemical name", conc, a, b, ..., z],
        ["Chemical name", conc, a, b, ..., z],
        ...
    ]
    where conc is the concentration in weight percent and a,..., z are the
    ratings for each of the plastics.  The ratings are in the set of
    strings A, B, C, D, or *.
    '''
    # The following data came from
    # http://www.plasticsintl.com/plastics_chemical_resistence_chart.html and
    # was probably copied from some British web page; the British spellings
    # have been changed to US English, as well as a few of the chemical names
    # converted to US usage.  Minor editing has been done to fix small
    # problems.  Data downloaded 27 Jun 2015.
    #
 
    # Legend:
    # A = No Attack, possibly slight absorption.  Negligible effect on
    #     mechanical properties.
    # B = Slight attack by absorption.  Some swelling and a small reduction in
    #     mechanical likely.
    # C = Moderate attack of appreciable absorption.  Material will have
    #     limited life.
    # D = Material will decompose or dissolve in a short period of time.
    # * = No data available
    #
    # (aq) = aqueous solution
    # SAT  = saturated aqueous solution
    #
    # Where aqueous solutions are shown the concentration as a weight %
    # is given.
 
    data = dedent('''
    Material;Concentration (weight %);ABS;Acetal;Acrylic;CAB;CPVC;ECTFE (Halar);Fluorosint;HDPE;Nylon 6/6;PEEK;PET;Polycarbonate;Polypropylene;Polysulfone;PPS;PVC Type 1;PVC Type 2;PVDF;PTFE;Tecalor/Torlon;UHMW
    Acetaldehyde (aq);40;D;A;D;*;D;*;A;C;B;A;A;*;C;*;A;D;D;D;A;A;A
    Acetic acid (aq);10;*;B;B;C;A;A;A;*;C;A;B;D;*;A;A;A;A;B;A;A;A
    Acetone;;D;B;D;*;D;A;A;A;A;B;B;C;A;B;A;D;D;D;A;*;*
    Alcohols, aliphatic;;*;A;D;*;*;A;A;*;B;A;A;*;*;*;A;*;*;A;A;A;A
    Aluminum chloride (aq);10;*;*;*;A;A;*;A;B;*;A;A;A;A;*;A;A;A;A;A;A;A
    Aluminum sulfate (aq);10;*;*;*;A;A;A;A;A;*;A;*;A;A;*;A;A;A;A;A;A;A
    Ammonia gas;;*;*;*;*;A;A;A;A;C;A;A;*;A;*;*;A;A;D;A;*;*
    Ammonium carbonate (aq);10;*;*;*;*;A;A;A;A;A;A;A;D;A;*;A;A;A;A;A;*;*
    Ammonium chloride (aq);10;*;*;*;A;A;A;A;A;A;A;A;C;A;*;A;A;A;A;A;A;A
    Amyl acetate;;D;*;D;*;*;*;A;D;A;A;*;*;D;*;A;D;D;B;A;A;A
    Aniline;;*;A;D;*;D;A;A;A;C;A;A;*;C;*;A;D;D;C;A;A;A
    Antimony trichoride (aq);10;*;*;A;*;A;A;A;A;C;A;*;*;A;*;*;A;A;*;A;*;*
    Barlium chloride (aq);10;*;*;A;*;A;A;A;A;A;A;*;*;A;*;A;A;A;A;A;A;A
    Barlium sulfate (aq);10;*;*;*;*;A;A;A;A;*;A;*;*;A;*;*;A;A;*;A;*;*
    Benzene;;D;A;D;D;D;A;A;D;A;A;A;D;D;D;A;D;D;C;A;*;*
    Benzene sulfonic acid;10;*;*;*;*;*;A;A;A;D;A;*;*;*;*;A;*;*;B;A;C;C
    Bleaching lye;10;C;*;*;*;A;A;A;B;C;A;*;*;B;*;*;A;A;A;A;A;A
    Boric acid (aq);10;*;*;*;*;A;A;A;A;A;A;A;*;A;*;A;A;A;A;A;*;*
    Boron trifluoride;;*;*;*;*;A;*;A;A;D;*;*;*;A;*;*;A;A;A;*;*;*
    Bromine (aq);30;*;*;*;*;D;A;*;D;D;B;*;*;D;*;A;A;D;A;*;A;A
    Butanol;;*;*;*;*;A;*;A;A;B;A;B;*;*;C;A;A;D;*;A;A;A
    Butyric acid (aq);20;*;*;C;*;*;*;A;D;B;A;*;*;D;*;A;*;*;A;A;*;*
    Butyric acid;concentrated;D;*;D;*;*;*;A;D;C;A;*;*;D;*;A;A;D;A;A;*;*
    Calcium hypochlorite;;*;*;*;C;*;A;A;A;D;A;A;C;A;*;A;A;A;A;A;*;*
    Camphor;;*;*;*;*;*;*;A;*;A;A;*;*;*;*;A;*;*;*;A;*;*
    Carbon tetrachloride;;D;A;*;C;C;A;A;D;A;A;A;*;D;A;A;C;D;A;A;A;A
    Chloral hydrate;;*;*;*;*;A;*;A;D;D;A;*;*;D;*;*;A;A;A;A;*;*
    Chlorine (aq);10;*;*;*;*;A;*;A;C;D;A;*;*;B;D;*;A;A;B;A;*;*
    Chloroform;;D;*;*;D;D;A;A;C;D;A;D;D;D;D;A;D;D;B;A;A;A
    Chlorosulfonic acid (aq);10;*;*;D;*;*;A;A;D;D;A;*;*;C;*;D;C;C;D;A;*;*
    Chrome alum (aq);10;*;*;*;*;*;*;A;*;A;A;*;*;*;*;*;A;A;A;A;*;*
    Chromic acid (aq);10;*;*;D;A;A;A;A;A;C;A;A;C;A;D;B;A;D;B;A;A;A
    Citric acid (aq);10;B;*;C;B;A;A;A;A;C;A;A;A;A;A;A;A;A;A;A;*;*
    Creosote;;*;*;*;*;*;*;A;*;A;A;*;*;*;*;*;*;*;A;A;*;*
    Cresylic acid;;*;*;*;*;A;A;A;D;D;A;*;*;D;*;*;A;C;A;A;*;*
    Cyclohexanol;;*;*;*;*;D;A;A;D;B;A;A;*;D;*;A;D;D;A;A;A;A
    Cyclohexanone;;*;*;*;D;D;A;A;D;A;A;A;*;D;D;*;D;D;A;A;A;A
    Detergents, organic;;*;*;*;*;A;A;A;*;A;A;A;*;*;*;A;A;A;*;A;*;A
    Dibutylphthalate;;*;*;*;*;*;*;A;*;A;A;*;*;*;*;*;*;*;D;A;A;A
    Diesel oil;;*;*;A;*;*;A;A;*;A;A;A;*;*;*;A;*;*;*;A;A;A
    Dioxan;;*;A;*;*;*;A;A;*;A;A;A;*;*;*;*;*;*;*;A;A;A
    Edible oils;;*;A;*;*;*;*;A;*;A;A;A;*;*;*;A;*;*;A;A;A;A
    Ether, diethyl;;*;A;*;*;*;*;A;*;A;A;A;*;*;*;A;*;*;*;A;A;A
    Ethyl acetate;;D;*;D;*;*;A;A;C;A;A;*;D;A;*;A;D;D;D;A;A;A
    Ethylene dichloride;;D;*;*;*;D;A;A;D;B;A;A;*;D;*;A;D;D;A;A;A;*
    Ethylene glycol (aq);96;*;*;A;D;A;A;A;A;B;A;*;C;A;A;A;A;A;A;A;A;A
    Ferrous chloride (aq);10;*;*;A;*;A;A;A;*;C;A;*;*;*;*;A;A;A;A;A;*;*
    Fluorine;;*;*;*;*;A;A;C;C;D;D;*;*;C;*;*;A;A;A;C;*;C
    Fluosilicic acid (aq);10;*;*;*;A;*;A;*;A;D;*;*;*;A;*;A;*;*;A;*;*;A
    Freon 12 (Arcton 12);;*;*;*;B;A;A;A;A;A;A;A;A;A;*;B;A;A;*;A;*;*
    Formaldehyde (aq);40;*;A;A;A;A;A;A;A;B;A;A;C;A;A;A;A;B;A;A;A;A
    Formic acid (aq);3;*;D;D;*;A;A;A;*;B;B;B;A;*;*;A;A;A;A;A;D;A
    Fruit juices;concentrated;A;*;*;*;A;A;A;A;B;A;A;C;A;*;A;A;A;A;A;A;A
    Gasoline;;*;A;*;*;*;A;A;A;A;A;A;*;*;*;A;*;*;A;A;A;A
    Glycerine;;A;*;A;B;A;A;A;A;A;A;A;A;A;A;A;A;A;A;A;A;A
    Heptane;;*;A;*;*;*;A;A;*;A;A;A;C;*;A;A;A;A;A;A;A;A
    Hydrobromic acid (aq);10;A;*;*;*;*;A;A;*;D;D;*;*;C;A;A;A;A;A;A;*;A
    Hydrochloric acid (aq);0.4;*;*;A;B;A;A;A;A;*;A;A;A;A;A;A;A;A;A;A;*;A
    Hydrofluoric acid Aq;4;*;D;C;C;*;A;A;B;C;D;B;B;A;B;D;A;A;A;*;A;A
    Hydrogenated vegetable oils;;*;*;*;*;*;*;A;*;A;A;A;*;*;*;A;*;*;A;A;A;A
    Hydrogen peroxide (aq);0.5;*;*;*;A;*;A;A;A;C;A;A;A;A;A;A;A;A;B;A;*;A
    Hydrogen peroxide (aq);1;*;*;*;*;*;A;A;*;*;A;A;A;*;A;A;*;*;B;A;*;A
    Hydrogen peroxide (aq);3;*;D;*;*;*;A;A;*;D;A;A;A;*;A;A;*;*;B;A;*;A
    Hydrogen sulfide (aq);saturated;*;C;A;A;A;A;A;A;B;A;C;*;A;*;A;A;A;A;A;*;A
    Hydroquinone;;*;*;*;B;*;A;A;A;B;A;*;*;A;*;*;A;A;A;A;*;*
    Iodine (in alcohol);;*;*;*;*;*;A;A;D;D;A;*;*;B;*;*;*;*;B;A;*;A
    Iodine (in pot iodine) (aq);3;*;*;*;*;*;A;A;D;D;A;*;*;B;*;*;*;*;A;A;*;A
    Isopropyl alcohol;;C;A;*;C;*;A;A;A;B;A;A;*;A;*;A;*;*;A;A;*;A
    Lactic acid (aq);10;*;B;*;A;*;A;A;A;C;A;A;A;A;*;A;A;A;A;A;A;A
    Lactic acid (aq);90;*;*;*;*;*;A;A;*;*;A;*;*;*;*;A;*;*;A;A;A;A
    Lead acetate (aq);10;*;*;*;*;A;A;A;A;B;A;*;*;A;*;A;A;A;A;A;*;A
    Linseed oil;;*;A;*;*;A;A;A;D;A;A;*;A;*;A;A;A;A;A;*;A;A
    Lubricating oils (petroleum);;*;A;*;*;A;*;A;C;A;A;A;B;C;*;A;A;A;A;A;A;A
    Magnesium chloride (aq);10;*;A;*;*;A;A;A;A;A;A;A;A;A;*;A;A;A;A;A;A;A
    Maleics acid;concentrated;*;*;*;*;A;A;A;A;*;A;*;*;A;*;*;A;A;A;*;*;*
    Malonic acid (aq);concentrated;*;*;*;*;*;*;A;*;*;A;*;*;*;A;*;*;*;*;A;*;A
    Mercuric chloride (aq);6;*;B;A;*;A;A;A;A;C;A;*;*;A;*;*;A;A;A;A;*;B
    Methyl acetate;;*;B;*;D;*;*;A;*;A;A;A;*;*;*;A;*;*;A;A;*;A
    Methyl ethyl ketone;;D;B;D;D;D;A;A;D;A;A;A;D;D;D;A;D;D;D;A;A;A
    Methyl chloride;;*;C;*;D;D;A;A;D;C;A;D;D;D;D;A;D;D;A;A;*;A
    Milk;;B;A;*;*;A;A;A;A;A;A;A;A;A;*;A;A;A;A;A;*;A
    Mineral oils;;*;A;*;*;A;A;A;B;A;A;*;C;C;*;A;A;A;A;A;A;A
    Naphthalene;;D;*;*;*;D;A;A;B;A;A;A;*;B;*;A;D;D;C;A;*;A
    Nickel sulfate (aq);10;*;*;A;*;A;A;A;A;A;A;*;A;A;*;A;A;A;A;A;*;A
    Nitric acid (aq);0.1;B;D;A;D;A;A;A;A;C;A;*;A;A;A;*;A;A;A;A;*;A
    Nitric acid (aq);10;*;D;*;*;A;A;A;*;D;A;C;*;*;A;A;A;A;B;A;*;B
    Oleic acid;;*;C;*;A;*;A;A;A;A;A;*;C;B;A;A;A;A;A;A;*;A
    Oxalic acid (aq);10;*;C;A;*;A;A;A;A;C;A;*;*;A;A;A;A;A;C;A;*;A
    Ozone;;*;C;*;B;A;A;A;D;C;A;A;D;C;A;*;A;A;B;A;*;A
    Paraffin;;*;A;*;*;*;A;A;;A;A;A;*;*;*;A;A;;A;A;A;A
    Perchloric acid (aq);10;*;C;*;*;A;A;A;B;D;A;A;*;C;*;*;A;A;A;A;*;A
    Phenol (aq);75;*;D;*;*;*;A;A;*;D;D;C;*;*;*;*;*;*;C;A;*;A
    Phosphoric acid (aq);0.3;*;*;A;A;A;A;A;A;*;A;A;C;A;A;A;A;A;A;A;A;A
    Phosphoric acid (aq);3;*;C;*;*;A;A;A;*;*;A;A;*;*;A;A;A;A;A;A;A;A
    Phosphoric acid (aq);10;*;C;*;*;A;A;A;*;D;A;B;*;*;A;A;A;A;A;A;A;A
    Phthalic acid (aq);saturated;*;*;*;*;*;*;A;*;B;A;*;*;*;*;*;*;*;B;A;*;*
    Potassium bicarb. (aq);60;*;*;*;*;A;*;A;A;A;A;A;*;A;*;A;A;A;A;A;*;A
    Potassium chloride (aq);90;A;*;A;A;A;A;A;A;A;A;A;A;A;*;A;A;A;A;A;*;*
    Potassium ferrocyanide (aq);30;*;*;A;*;A;A;A;*;A;A;*;*;*;*;*;A;A;A;A;*;A
    Propane gas;;*;*;*;A;A;A;A;D;A;B;A;*;C;*;A;A;A;A;A;*;A
    Salicylic acid;;*;*;*;*;*;A;A;*;A;A;A;*;*;*;*;*;*;A;A;*;A
    Silicone fluids;;D;*;*;*;*;A;A;*;A;A;A;*;*;*;A;*;*;A;A;A;A
    Silver nitrate;;*;A;*;A;A;A;A;A;A;A;A;*;A;*;A;A;A;A;A;*;A
    Soap solutions;;B;A;*;*;A;A;A;A;A;A;A;*;A;*;A;A;A;A;A;*;A
    Sodium acetate (aq);60;*;*;A;A;A;A;A;A;B;A;A;*;A;*;A;A;A;A;A;*;A
    Sodium bicarbonate (aq);50;*;A;A;A;A;A;A;A;A;A;A;A;B;*;A;A;A;A;A;A;A
    Sodium hypochlorite 15% (chlorine bleach);;*;C;A;*;*;A;A;A;D;A;A;A;A;A;B;A;A;A;A;A;A
    Sodium nitrate (aq);50;*;A;A;*;A;A;A;A;A;A;A;*;A;*;A;A;A;A;A;*;A
    Stannic chloride (aq);10;*;*;*;*;*;*;A;A;C;A;*;*;A;*;A;*;*;A;A;*;*
    Stearic acid;;*;*;*;*;A;A;A;A;A;A;*;*;A;*;*;A;A;A;A;*;A
    Styrene (monomer);;*;*;*;D;*;A;A;*;A;A;C;*;*;*;A;*;*;A;A;*;*
    Sulfur dioxide (dry gas);100;D;B;A;C;A;A;A;A;B;A;B;*;A;*;A;A;A;B;A;A;A
    Sulfuric acid (aq);2;B;D;D;*;A;A;A;A;C;A;A;A;A;A;A;A;A;B;A;A;A
    Sulfuric acid (aq);5;*;D;*;*;*;A;A;*;D;A;A;*;*;A;A;A;A;B;A;A;A
    Sulfurous acid (aq);10;*;C;A;*;A;A;A;A;D;A;C;*;A;*;*;A;A;*;A;*;A
    Tallow;;*;*;*;*;*;*;A;A;A;A;*;*;*;*;A;*;*;A;A;A;A
    Tar;;*;*;*;*;*;A;A;*;B;A;*;*;*;*;A;*;*;A;A;A;*
    Toluene;;D;A;*;D;D;*;A;D;A;A;A;D;D;D;A;D;D;B;A;A;B
    Transformer oil;;*;*;D;*;*;A;A;*;A;A;*;*;*;*;A;*;*;A;A;A;A
    Trichlorethylene;;*;B;*;D;D;A;A;D;B;A;B;*;D;D;A;D;D;A;A;A;B
    Triethanolamine;;*;*;*;*;*;A;A;A;A;A;B;*;A;*;A;A;A;A;A;D;A
    Turpentine;;D;A;*;*;A;A;A;D;A;A;*;D;D;B;A;A;C;A;A;A;A
    Trisodium phosphate (aq);95;*;*;A;*;A;A;A;A;*;A;A;*;A;*;A;A;A;*;A;*;*
    Urea;;*;A;*;*;A;A;A;A;A;A;A;*;A;*;A;A;A;A;A;*;A
    Vaseline;;B;A;*;*;A;A;A;A;A;A;A;A;*;*;A;A;A;A;A;A;A
    Vegetable oils;;C;A;*;*;*;A;A;*;A;A;A;*;*;*;A;*;*;A;A;A;A
    Vinegar;;A;B;*;*;A;A;A;A;C;A;A;*;A;*;A;A;A;A;A;A;A
    Vinyl chloride;;*;*;*;*;*;*;A;*;A;A;*;*;*;*;A;*;*;A;A;*;*
    Water;;A;A;*;*;A;A;A;A;A;A;A;A;A;A;A;A;A;A;A;A;A
    Wax (molten);;C;A;*;*;*;A;A;*;A;A;A;*;*;*;A;*;*;*;A;A;A
    Mineral spirits;;*;A;*;*;A;A;A;*;A;A;*;*;*;*;A;*;*;A;A;*;A
    Wines and spirits;;B;*;*;*;A;A;A;*;B;A;A;A;*;*;A;A;A;A;A;A;A
    Xylene;;D;*;D;D;D;A;A;D;D;A;A;*;D;D;A;D;D;A;A;A;B
    Xylenol;;*;*;*;*;A;*;A;*;D;A;*;*;*;*;*;*;*;*;A;A;*
    Zinc chloride (aq);10;*;*;A;A;A;*;A;A;C;A;*;C;A;A;A;A;A;A;A;*;A
    ''')
    chemicals = []
    for i, s in enumerate(data.split("\n")):
        d = s.split(";")
        assert(len(d) == 23)
        if i:
            chemicals.append(d)
        else:
            plastics = d[2:]
    return plastics, chemicals
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    name = sys.argv[0]
    print(dedent(f'''
    Usage:  {name} [options] cmd [cmd options]
        Print the chemical resistance of various plastics.  The regexp regular
        expression in the following commands is used to find the relevant
        chemical names (case-insensitive).
      Commands:
        chem regexp
            Show the matching chemical names.
        a regexp
            Show the plastics that are not attacked.  Possibly slight absorption
            and negligible effect on mechanical properties.
        b regexp
            Show plastics that have slight attack; some swelling and a small
            reduction in mechanical properties are likely.
        c regexp
            Show the plastics that have moderate attack with appreciable
            absorption.  Material will have limited life.
        d regexp
            Show the plastics that will decompose or dissolve in a short period
            of time.
        nd regexp
            Show the plastics with no data available for the indicated
            chemicals.
        pl
            Show the list of plastics.
    Example:
        {name} a acetone
            will show plastics suitable for containing acetone.
    Notes:
      The data are from
      http://www.plasticsintl.com/plastics_chemical_resistence_chart.html
      downloaded 27 Jun 2015.  The data are assumed to be for room temperature
      resistances and should be considered for reference only.
    '''))
    exit(status)
def ParseCommandLine(d):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-h", "--help"):
            Usage(d, status=0)
    if not args:
        Usage(d)
    return args
def GetChemicals(regexp, d):
    '''Return a list of the chemicals whose name matches the regexp.
    '''
    try:
        s = re.compile(regexp, re.I)
    except Exception:
        Error("'{}' is an invalid regular expression".format(regexp))
    found = []
    for i in d["chemicals"]:
        mo = s.search(i[0])
        if mo:
            found.append(i)
    return found
def FindChemRes(cmd, regexp, d):
    '''cmd is a, b, c, or d.  Print the plastics that are resistant to the
    chemicals that match the regexp.
    '''
    plastics = d["plastics"]
    letter = cmd.upper()
    matching_chemicals = GetChemicals(regexp, d)
    header_not_printed = True
    for item in matching_chemicals:
        name, found = item[0], []
        if item[1]:
            name += " " + item[1]
        for number, r in enumerate(item[2:]):
            if r == letter or (letter == "ND" and r == "*"):
                found.append(number)
        if found:
            if header_not_printed:
                print("Plastics with a rating of '{}':".format(letter))
                print(d["ratings"][letter])
                header_not_printed = False
            print(name)
            for i in found:
                print("  {}".format(plastics[i]))
def ShowChemicals(args, d):
    if len(args) > 1:
        matching_chemicals = GetChemicals(args[1], d)
    else:
        matching_chemicals = GetChemicals(".", d)
    for i in matching_chemicals:
        name, conc = i[0], i[1]
        if conc:
            try:
                float(conc)
                # It's a number
                name = "{} {}%".format(name, conc)
            except Exception:
                # It's a string
                name = "{} {}".format(name, conc)
        print(name)
def ShowPlastics(d):
    for i in d["plastics"]:
        print(i)
        details = plastic_details[i]
        if details:
            print("  {}".format(details))
if __name__ == "__main__":
    d = {}  # Options dictionary
    d["ratings"] = {
        "A":
'''    Not attacked.  Possibly slight absorption and negligible effect
    on mechanical properties.''',
        "B":
'''    Slight attack; some swelling and a small reduction in mechanical
    properties are likely.''',
        "C":
'''    Moderate attack with appreciable absorption.  Material will have
    limited life.''',
        "D": "    Will decompose or dissolve in a short period of time.",
        "ND": "    No data available.",
    }
    d["plastics"], d["chemicals"] = GetData()
    args = ParseCommandLine(d)
    cmd = args[0]
    if cmd == "chem":
        ShowChemicals(args, d)
    elif cmd.lower() in set(("a", "b", "c", "d", "nd")):
        FindChemRes(cmd, args[1], d)
    elif cmd == "pl":
        ShowPlastics(d)
    else:
        Error("Command '{}' is unrecognized".format(cmd))
