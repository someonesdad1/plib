'''
From RJN's 'ESD_Resistivities.pdf' document (unattributed)

Note:  R = ρ*L/A where L is length and A is cross sectional area.  Since
A is W*t where W is the width and t is the thickness, this can be written
R = (ρ/t)*L/W = Rs*L/W.  Rs is the surface resistivity, also called the
sheet resistance and is usually given as "Ω/square", where "square" implies
the length dimension that L and W are measured in.  A thin sheet square has
the same resistance between two sides, regardless of the size.

The sheet resistance Rs can be multiplied by the film's thickness to get
the volume resistivity.
'''
from wrap import dedent
if 1:   
    data = dedent('''
    # Units:  Ω·m, value is base 10 logarithm
    # First number is log10 of volume resistivity in Ω·m
    # Second number is log10 of surface resistivity in Ω/square
 
    Beeswax (fresh surface) ; 12-13 ; ~14
    Boron ; 10 
    Ceramics
        Alumina ; 9-12 
        Porcelain, glazed ; 10-12 ; 11
        Porcelain, unglazed ; 10-12 ; 9
        Pyrophyllite ; 10-13
        Special H.F. ; 14
        Steatite ; 11-13
        Titanates ; 6-13
    Diamond ; 10-11
    Glass
        Soda-lime ; 9-11 ; 10-12
        Borosilicate (Pyrex) ; 12
        Plate ; 11.3 ; 10.7
    Gutta-percha ; 7
    Hard rubber (Ebonite, etc.) ; 13-15 ; 10-18
    Iodine ; 13
    Ivory ; 6 ; 9
    Marble ; 7-9 ; 9
    Mica, sheet ; 11-15 ; 10-13
    Mica, molded ; 13 ; 13.7
    Mineral oil ; >10
    Mineral insulating oil ; 11-15
    Paper, dry ; ~10 ; 9-10
    Kerosene ; 11-12
    Paraffin wax ; 13-17 ; 15
    Plastics
        Acrylic ; >13 ; >14
        Polyester (no filler) ; 12-13 ; 13-14
        Melamines (cellulose) ; >9 ; 12-14
        Melamines (mineral) ; 9 ; 12-14
        Casein ; 7-8 ; 10-11
        Cellulose acetate ; 8-11 ; 11-12
        Epoxy resin, cast (no filler) ; 12-13 ; 7.5->14
        Phenolics ; 6-12 ; 8-14
        Nylon (polyamides) ; 8-13 ; 11-15
        Polychlorotrifluoroethylene ; 16 ; 12-13
        Polyethylene terephthalate ; 15-17
        Polyformaldehyde ; ~12.8; >13.3
        Polypropylene ; 13-15 ; >15
        Polystyrene (general purpose) ; 15-19 ; >14
        Polystyrene (toughened) ; 10-15 ; >14
        Teflon ; 15-19 ; 12.6-17
        Polyethylene, high density ; 14-15 ; 12-17
        Polyethylene, low density ; 14-18 ; >14
        Polyurethanes ; 9-12 ; 13-15
        PVC, rigid ; 12.7-13 ; 12-15
        PVC, flexible ; 6.7-12.7 ; >14
        Silicone (glass) ; 8-12 ; >11
    Qartz, par. to opt. axis ; 12
    Qartz, perp. to opt. axis ; 14
    Shellac ; 7 ; 13.7
    Silicone oil ; 12
    Silicone rubber ; 9
    Slate ; 5-6 ; 7
    Soil ; 2-4
    Sulfur ; 14-15 ; 15.8
    Wood (paraffined) ; 8-11 ; 12
    Water, distilled ; 2-5
    ''')

o = []
w = [35, 12, 12]
print(dedent('''
    Resistivity data
        Column 1:  log10(volume resistivity in Ω·m)
        Column 2:  log10(sheet resistivity in Ω)
        Multiply sheet resistivity by thickness to get volume resistivity

    '''))
for line in data.split("\n"):
    line = line.rstrip()
    if not line or line.startswith("#"):
        continue
    if ";" not in line:
        print(line)
    else:
        f = line.split(";")
        f[1] = f[1].strip().replace("-", " to ")
        if len(f) > 2:
            f[2] = f[2].strip().replace("-", " to ")
        print(f"{f[0]:{w[0]}s} {f[1]:^{w[1]}s}", end="")
        if len(f) > 2:
            print(f"{f[2]:^{w[2]}s}")
        else:
            print()
