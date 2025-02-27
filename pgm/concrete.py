"""
Script to help with mixing concrete
    See concrete.pdf for details.  Run the script; you'll be prompted
    for the requisite input.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Script to help with mixing concrete
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    # from math import pi, acos, sqrt
if 1:  # Custom imports
    from wrap import dedent
    from f import flt, pi, acos, sqrt
    from get import GetNumber
    from u import ParseUnit, ParseUnitString
    from color import C
if 1:  # Global variables
    # Set to True to debug the script
    Debug = 1
    # Constants
    m3_per_ft3 = flt(0.0283168)
    lb_per_kg = flt(2.20462)
    gal_per_L = flt(0.264172)
    in_per_m = flt(39.37)
    ft_per_m = flt(12 / in_per_m)

    class G:
        pass

    g = G()
    g.digits = 2
if 1:  # Component mixing info
    # Note:  in the following, specific gravities are always given in
    # g/cc units.  Multiply by 1000 to get kg/m3.
    #
    # The standard recommended ratio is 1:2:3 for cement:sand:gravel.
    # This is technically supposed to be the mass ratio, not the volume
    # ratio.  However, the specific gravities are cement:1.6,
    # sand(dry):1.6, and gravel(dry):1.6, so if these conditions are
    # met, then it also works for volume.
    vol_ratio_cement = flt(1 / 6)
    vol_ratio_sand = flt(2 / 6)
    vol_ratio_gravel = flt(3 / 6)

    # Value to multiply a cured concrete volume to get the required dried
    # components volume.  This is also sometimes called the "make sure
    # you have enough factor".  Typical values range from 1.5 to 2.
    # You can empirically determine a good value by starting with 1.5
    # and keeping track of the discrepancy from the desired volume.
    dry_components_factor = flt(1.5)

    # The density of concrete with sand and gravel.  Modify by
    # experience.  A density of 2.5 corresponds to 156 lbm/ft3; many
    # folks use 150 lb/ft3 as a round number.
    concrete_specific_gravity = flt(2.5)

    # The amount of water is determined by the mass of cement.  The
    # Quikrete 1101 datasheet suggests 2.8 L (3/4 gal) per 80 lb bag
    # and adjust upwards as needed to a maximum of 4.3 L (1.1 gal).
    # If this bag has 1/6th of its mass as cement, then there are 13.3
    # lbs = 6.05 kg of cement in the bag.  For a 0.25 water/cement
    # mass ratio, this would mean you need to add 1.5 L of water.
    # Thus, the 2.8 L value given means the water/cement ratio is
    # (2.8/1.5)0.25 = 0.47, right about the 0.45 level I've seen that
    # people deem as quite practical.  So we'll use 0.45 as the target
    # value of the water_to_cement_mass_ratio.  Note the 4.3 L means
    # it can go up to (4.3/2.8)0.46 = 0.72.
    #
    # To calculate the amount of water needed, we will first calculate
    # the required cement volume.  To turn this into a mass, we need
    # the specific gravity of the cement powder.  A 90 lb bag of
    # cement is 1 cubic foot, which means the specific gravity is 1.44
    # g/cc.  Glover gives it as 1.6, so we're not far off (there are
    # values more than double this on the web, but these are compacted
    # forms) -- and the lower value is more likely when shoveling from
    # a loose pile.  I've rounded it down to 1.4.  The best thing you
    # can do is to measure the actual mass and volume when you're
    # making some concrete and use the measured density.
    water_to_cement_mass_ratio = flt(0.45)
    cement_specific_gravity = flt(1.4)

    # To estimate the total mass of the finished concrete, we need the
    # estimated specific gravities of the sand and gravel.  Obviously,
    # you'll get the best results if you measured these values.
    sand_specific_gravity = flt(1.6)  # Assumes dry sand, Glover
    gravel_specific_gravity = flt(1.7)  # Glover
if 1:  # Premix info
    # Data taken from Quikrete 1101 data sheet.
    #
    # The premix yield is calculated from the fact that an 80 lb bag
    # of premixed concrete yields 0.6 of a cubic foot of cured
    # concrete.  Note this is not a density, as it implicitly contains
    # the water of hydration.
    premix_yield_kg_per_m3 = flt(2135.8)

    # Recommended amount of water is 2.8 L per 80 lb bag of concrete.
    # From the notes above, this is a 0.47 water/cement mass ratio.
    # The data sheet indicates you can go to a maximum of 4.3 L per 80
    # lb bag.
    water_L_per_kg_of_concrete = flt(0.0771618)
if 1:  # Other info
    # Compressive strength, typical
    strength_28_days_MPa = 27.6  # (4000 psi)

    # Standard #2 shovel volume.  Of course, this is approximate and is
    # best measured using the shovel and materials you're measuring.
    shovel_per_m3 = 158.916  # From 4.5 shovels equals 1 cubic foot

    # Allowed length units.  The values convert the unit to m.
    default_unit = "inches"
    allowed_length_units = {
        "": flt(1),
        "m": flt(1),
        "in": flt(1 / in_per_m),
        "inch": flt(1 / in_per_m),
        "inches": flt(1 / in_per_m),
        "foot": flt(12 / in_per_m),
        "feet": flt(12 / in_per_m),
        "ft": flt(12 / in_per_m),
        "yard": flt(36 / in_per_m),
        "yd": flt(36 / in_per_m),
    }
    allowed_length_units[""] = allowed_length_units[default_unit]

    # The following is the factor by which the volume of a 5 gallon bucket
    # filled to the brim is different from 5 gallons.
    # with its top.  This comes from measurements of a few actual
    # buckets.
    bucket_ratio = flt(5.6 / 5)
if 1:  # Shapes

    class FormShape(object):
        def GetDescription(self):
            """Return a number indicating the order in the listing and the
            string to display.
            """
            raise Exception("Virtual method")

        def GetVolume(self):
            """Return volume in cubic m."""
            raise Exception("Virtual method")

        def GetDimensions(self):
            """Prompt the user for the required dimensions."""
            raise Exception("Virtual method")

        def __str__(self):
            return self.name

        def Characteristics(self):
            """Return a string array describing this object's dimensions."""
            raise Exception("Virtual method")
            s = []

    class Slab(FormShape):
        def __init__(self):
            self.name = "Rectangular slab"

        def GetDescription(self):
            return 1, "Rectangular slab"

        def GetVolume(self):
            return self.length * self.width * self.height * self.how_many

        def GetDimensions(self):
            self.length, self.length_orig = GetLength("Length of slab? ")
            self.width, self.width_orig = GetLength("Width of slab? ")
            self.height, self.height_orig = GetLength("Height of slab? ")
            self.how_many = GetNumber(
                "How many of them? ", numtype=int, low=1, default=1, allow_quit=True
            )

        def Characteristics(self):
            return (
                "Length = %s" % self.length_orig,
                "Width  = %s" % self.width_orig,
                "Height = %s" % self.height_orig,
            )

    class Cylinder(FormShape):
        def __init__(self):
            self.name = "Cylinder"

        def GetDescription(self):
            return 2, "Cylinder"

        def GetVolume(self):
            return pi * (self.diameter / 2) ** 2 * self.length * self.how_many

        def GetDimensions(self):
            self.diameter, self.diameter_orig = GetLength("Diameter of cylinder? ")
            self.length, self.length_orig = GetLength("Length of cylinder? ")
            self.how_many = GetNumber(
                "How many of them? ", numtype=int, low=1, default=1, allow_quit=True
            )

        def Characteristics(self):
            return (
                "Diameter = %s" % self.diameter_orig,
                "Length   = %s" % self.length_orig,
            )

    class HorizontalCylinder(FormShape):
        def __init__(self):
            self.name = "Horizontal cylinder"

        def GetDescription(self):
            return 3, "Partially-filled horizontal cylinder"

        def GetVolume(self):
            """Formula from
            http://mathworld.wolfram.com/HorizontalCylindricalSegment.html
            """
            h = self.percent / 100 * self.diameter
            r, L = self.diameter / 2, self.length
            a = r - h
            return (
                L * (r * r * acos(a / r) - a * sqrt(2 * r * h - h * h)) * self.how_many
            )

        def GetDimensions(self):
            self.diameter, self.diameter_orig = GetLength("Diameter of cylinder? ")
            self.length, self.length_orig = GetLength("Length of cylinder? ")
            self.percent, self.percent_orig = GetNumber(
                "Filled to percent of height? ",
                low=0,
                low_open=True,
                high=100,
                use_unit=False,
            )
            self.how_many = GetNumber(
                "How many of them? ", numtype=int, low=1, default=1, allow_quit=True
            )

        def Characteristics(self):
            return (
                "Diameter = %s" % self.diameter_orig,
                "Length   = %s" % self.length_orig,
                "Percent  = %s" % self.percent_orig,
            )

    class Sphere(FormShape):
        def __init__(self):
            self.name = "Sphere"

        def GetDescription(self):
            return 4, "Partially-filled sphere"

        def GetVolume(self):
            """See http://mathworld.wolfram.com/SphericalCap.html and
            http://mathworld.wolfram.com/SphericalSegment.html.
            """
            r = self.diameter / 2
            if self.percent >= 50:
                h = self.diameter * (self.percent - 50) / 100
                Vhalf = (4 / 3 * pi * r**3) / 2
                # Sph. cap volume from MH, 19th ed., pg 160
                c1 = 2 * sqrt(r * r - h * h)
                c2 = 2 * r
                V = pi / 6 * h * (3 / 4 * (c1 * c1 + c2 * c2) + h * h)
                return (V + Vhalf) * self.how_many
            else:
                h = r * self.percent / 100
                d = r - h
                a = sqrt(r * r - d * d)
                # Wolfram sph. cap page equation 14 with b = 0
                return pi * h * (3 * a * a + h * h) * self.how_many

        def GetDimensions(self):
            self.diameter, self.diameter_orig = GetLength("Diameter of sphere? ")
            self.percent, self.percent_orig = GetNumber(
                "Filled to percent of diameter? ",
                low=0,
                low_open=True,
                high=100,
                use_unit=False,
            )
            self.how_many = GetNumber(
                "How many of them? ", numtype=int, low=1, default=1, allow_quit=True
            )

        def Characteristics(self):
            return (
                "Diameter = %s" % self.diameter_orig,
                "Percent  = %s" % self.percent_orig,
            )


def Error(msg, status=1):
    print(msg, stream=sys.stderr)
    exit(status)


def Initialization():
    if len(sys.argv) == 3 and sys.argv[1] == "-d":
        try:
            g.digits = int(sys.argv[2])
        except Exception:
            Error("Bad argument for -d option (must be integer)")
        else:
            if not (1 <= g.digits <= 15):
                Error("-d argument must be between 1 and 15")
    x = flt(0)
    x.N = g.digits


def HeaderInfo():
    if Debug:
        return
    u = allowed_length_units.keys()
    u.sort()
    units = " ".join(u)
    print(
        dedent(f"""
    This script will help with the following concrete mixing problems:
        1.  Using premixed bags of concrete mix.
        2.  Mixing cement, sand, and aggregate.
     
    The following form shapes are supported:
        1.  Rectangular slab
        2.  Cylinder
        3.  Partially-filled horizontal cylinder
        4.  Partially-filled sphere
     
    You'll be prompted for the relevant dimensions of the form.  You can use the
    following units (along with any valid SI prefix):
        {units}
    '{default_unit}' is the default unit if no unit string is appended.
    """)
    )


def GetProblem():
    default = 1
    while True:
        print(
            dedent(
                """
        Specify problem:
            1.  Calculate number of bags of ready-mix
            2.  Calculate cement, sand, gravel mixture
        [Default is {default}] --> """,
                end="",
            )
        )
        s = input("").strip()
        if s.lower() == "q":
            exit(0)
        try:
            if s:
                num = int(s)
            else:
                num = default
        except Exception:
            print(f"'{s}' is not an integer")
        else:
            if num in (1, 2):
                return num
            print("Number must be 1 or 2\n")


def GetLength(prompt):
    """Prompt the user and get the required length.  Return (L, s)
    where L is the length in m and s is the original string the user
    typed in.
    """
    while True:
        num, unit = GetNumber(prompt, low=0, low_open=True, use_unit=True)
        if not unit.strip():
            unit = default_unit
        prefix, u = ParseUnitString(unit, allowed_length_units, strict=False)
        if u in allowed_length_units:
            return (
                flt(num) * flt(prefix) * flt(allowed_length_units[u]),
                str(flt(num)) + " " + unit,
            )
        else:
            print(f"'{unit}' is unrecognized unit -- try again.")


def GetFormGeometry():
    default = 1
    form = {
        1: Slab(),
        2: Cylinder(),
        3: HorizontalCylinder(),
        4: Sphere(),
    }
    while True:
        print(
            dedent(
                f"""
        Specify the geometry of the form you'll pour the concrete into:
            1.  Rectangular slab
            2.  Cylinder
            3.  Partial horizontal cylinder
            4.  Partial sphere
        [Default is {default}] --> """,
                end="",
            )
        )
        s = input("").strip()
        if s.lower() == "q":
            exit(0)
        try:
            if s:
                num = int(s)
            else:
                num = default
        except Exception:
            print(f"'{s}' is not an integer")
        else:
            if num in (1, 2, 3, 4):
                return form[num]
            print("Number must be {min(form)} to {max(form)}, inclusive")


if __name__ == "__main__":
    indent = " " * 4
    Initialization()
    HeaderInfo()
    problem = GetProblem() if not Debug else 2
    if not Debug:
        form = GetFormGeometry()
        form.GetDimensions()
    else:
        # Run debug example
        case = 1
        if case == 1:
            form = Slab()
        elif case == 2:
            form = Cylinder()
        elif case == 3:
            form = HorizontalCylinder()
        elif case == 4:
            form = Sphere()
        else:
            raise Exception("Unknown case")
        a, sa, b, sb = 2, "2 m", 1, "1 m"
        # Set up the desired dimensions
        length, s_length = ft_per_m, "1 ft"
        dia, s_dia = flt(2 * ft_per_m), "2 ft"
        pct, s_pct = flt(100), "100"
        number = 1
        if isinstance(form, Slab):
            form.length, form.length_orig = length, s_length
            form.width, form.width_orig = length, s_length
            form.height, form.height_orig = length, s_length
            form.how_many = number
        elif isinstance(form, Cylinder):
            form.length, form.length_orig = length, s_length
            form.diameter, form.diameter_orig = dia, s_dia
            form.how_many = number
        elif isinstance(form, HorizontalCylinder):
            form.length, form.length_orig = length, s_length
            form.diameter, form.diameter_orig = dia, s_dia
            form.how_many = number
            if 0:
                form.percent, form.percent_orig = flt(100), "100"
            else:
                form.percent, form.percent_orig = flt(50), "50"
                form.percent, form.percent_orig = flt(0), "0"
        elif isinstance(form, Sphere):
            form.diameter, form.diameter_orig = dia, s_dia
            form.how_many = number
            if 0:
                form.percent, form.percent_orig = flt(100), "100"
            else:
                form.percent, form.percent_orig = flt(50), "50"
        else:
            raise Exception("Bad geometry")
    # Calculate results
    volume_m3 = flt(form.GetVolume())
    v_m = volume_m3
    v_ft = flt(volume_m3 / m3_per_ft3)
    v_yd = flt(volume_m3 / (27 * m3_per_ft3))
    # Print answer
    if problem == 1:  # Ready-mix
        print("For the concrete form of:")
        print("%s%s" % (indent, form.name))
        for i in form.Characteristics():
            print("%s%s" % (indent, i))
        s = "{indent}Volume = {v_m} m3 = {v_ft} ft3 = {v_yd} yd3".format(**locals())
        print(s)
        M_kg = flt(volume_m3 * premix_yield_kg_per_m3)
        M_lb = flt(M_kg * lb_per_kg)
        n_60, n_80 = str(M_lb / 60), str(M_lb / 80)
        m_kg, m_lb = [str(i) for i in (M_kg, M_lb)]
        w_L = flt(M_kg * water_L_per_kg_of_concrete)
        v_water_L = str(w_L)
        v_water_gal = str(gal_per_L * w_L)
        v_water_qt = str(gal_per_L * w_L * 4)
        print(f"""
    This is {m_kg} kg = {m_lb} lb of cured concrete.
    Water required is {v_water_L} liters = {v_water_gal} gal = {v_water_qt} qt
    Number of bags of premix needed:
        60 lb:  {n_60}
        80 lb:  {n_80}""")
    elif problem == 2:  # Cement, sand, and gravel
        print("For the concrete form of:")
        print("%s%s" % (indent, form.name))
        for i in form.Characteristics():
            print("%s%s" % (indent, i))
        v_sh = str(volume_m3 * shovel_per_m3)
        print(
            dedent(f"""
        {indent}Volume of finished concrete
        {indent}{indent}= {v_m} m3 = {v_ft} ft3 = {v_yd} yd3 = {v_sh} shovels
        """)
        )
        wcmr = str(water_to_cement_mass_ratio)
        v_mix_m3 = flt(volume_m3 * dry_components_factor)
        v_cement_m3 = flt(v_mix_m3 * vol_ratio_cement)
        v_sand_m3 = flt(v_mix_m3 * vol_ratio_sand)
        v_gravel_m3 = flt(v_mix_m3 * vol_ratio_gravel)
        # Calculate the total mass of cured concrete
        k = flt(1000)  # Because sp gr is in g/cc
        M_cement_kg = flt(k * v_mix_m3 * vol_ratio_cement * cement_specific_gravity)
        M_sand_kg = flt(k * v_mix_m3 * vol_ratio_sand * sand_specific_gravity)
        M_gravel_kg = flt(k * v_mix_m3 * vol_ratio_gravel * gravel_specific_gravity)
        M_water_kg = flt(water_to_cement_mass_ratio * M_cement_kg)
        M_kg = flt(M_cement_kg + M_sand_kg + M_gravel_kg + M_water_kg)
        M_lb = flt(M_kg * lb_per_kg)
        m_kg = str(M_kg)
        m_lb = str(M_lb)
        w_L = str(M_water_kg)
        w_gal = str(M_water_kg * gal_per_L)
        w_b = str(M_water_kg * gal_per_L / (5 * bucket_ratio))
        # Liters
        c_L = str(k * v_mix_m3 * vol_ratio_cement)
        s_L = str(k * v_mix_m3 * vol_ratio_sand)
        g_L = str(k * v_mix_m3 * vol_ratio_gravel)
        # Cubic feet
        k = flt(35.3147)  # Converts m3 to ft3
        c_ft3 = str(k * v_mix_m3 * vol_ratio_cement)
        s_ft3 = str(k * v_mix_m3 * vol_ratio_sand)
        g_ft3 = str(k * v_mix_m3 * vol_ratio_gravel)
        # 5 gallon bucket
        k = flt(264.172 / (5 * bucket_ratio))  # m3 to gal, then scaled by bucket volume
        c_b = str(k * v_mix_m3 * vol_ratio_cement)
        s_b = str(k * v_mix_m3 * vol_ratio_sand)
        g_b = str(k * v_mix_m3 * vol_ratio_gravel)
        # #2 shovel
        k = flt(shovel_per_m3)
        c_sh = str(k * v_mix_m3 * vol_ratio_cement)
        s_sh = str(k * v_mix_m3 * vol_ratio_sand)
        g_sh = str(k * v_mix_m3 * vol_ratio_gravel)
        # Sums
        S_L = str(sum([flt(i) for i in (c_L, s_L, g_L)]))
        S_ft3 = str(sum([flt(i) for i in (c_ft3, s_ft3, g_ft3)]))
        S_b = str(sum([flt(i) for i in (c_b, s_b, g_b)]))
        S_sh = str(sum([flt(i) for i in (c_sh, s_sh, g_sh)]))
        w1, w2 = 10, 12
        print(f"""
    Results are to {g.digits} significant figures
    This is {m_kg} kg = {m_lb} lb of cured concrete.
 
    Component volumes needed:
                 liters          cu. ft.       5 gal bucket    #2 shovel
                ----------     ----------      ------------    -----------
    Cement      {c_L:^{w1}s}     {c_ft3:^{w1}s}      {c_b:^{w2}s}   {c_sh:^{w2}s}
    Sand        {s_L:^{w1}s}     {s_ft3:^{w1}s}      {s_b:^{w2}s}   {s_sh:^{w2}s}
    Gravel      {g_L:^{w1}s}     {g_ft3:^{w1}s}      {g_b:^{w2}s}   {g_sh:^{w2}s}
                ----------     ----------      ------------    -----------
    Sum         {S_L:^{w1}s}     {S_ft3:^{w1}s}      {S_b:^{w2}s}   {S_sh:^{w2}s}
 
    Water needed = {w_L} liters = {w_gal} gallons = {w_b} five gal buckets
    Water/cement mass ratio = {wcmr}
    """)
    else:
        raise Exception("Bug:  bad problem number")
    # Print out the compressive strength
    print(
        """
    Nominal compressive strength after 1 month:
        27.6 MPa = 2.8e6 kgf/m2 = 4000 lbf/in2 = 5.8e5 lbf/ft2"""[1:]
    )
