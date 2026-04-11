'''

9 Apr 2026 This is an example of the use of the Num class in a "simple" REPL-type
calculation for a backyard project making stepping stones.  It illustrates features (and
features we'll need to add) to the class to make it a pleasant thing to use for routine
calculations.  I'll flag comments and needed features with the ❓ character.

Vision

    The Num class can be used in a REPL environment to do routine numerical calculations
    for problems with units.  Nearly every problem has some units, what we'll call here
    "semantic units".  These capture the important types (in the software sense) of the
    problem and help you ensure the calculation is correct, as if the "semantic units"
    algebra isn't correct, the problem wasn't solved correctly.  In the example given
    below, the semantic units are both the physical units used to calculate the needed
    volume and mass and the "logical" units like "bags" of concrete and "steps" to count
    the number of steps.  

    Building a type system in software for things like units is a nontrivial task.  The
    Num class neatly steps around this task by using the GNU units tool to do the unit
    conversion and dimensional algebra, as this is a mature tool.

    The overall vision I've had for decades is a tool I can use at a terminal to perform
    a typical calculation needed in technical work.  This tool would let me define my
    terms and variables of the problem, explain my reasoning, models, and
    approximations, then let me perform the needed calculations.  Then I'd write my
    observations, conclusions, and where I plan to go next.  This is very much like I
    used paper lab notebooks over my career, so the overriding mental model for this Num
    class is to allow a python REPL to feel a little like you were using a lab notebook.
    Because of this, persistence in a software sense is required and this feature is
    planned by using the SQLite library in python, but not implemented yet.  It will
    provide a time-stamped record of what happened to the REPL's state over time, not
    allowing important information to get lost.  The net vision is a temporal thread of
    thinking like you'd get with a lab notebook.

    The "shallow" contribution of the Num class is combining the variety of different
    number types available in python into one "pragmatic" numerical type.  This mirrors
    the way I did calculations by hand before electronic calculators appeared:  you'd
    shift seamlessly between integers, reals, and complex numbers, changing domains as
    needed by the problem.  For physical calculations, you'd also include uncertainty,
    so that "number type" has to be handled by this pragmatic number type too.  In fact,
    it also handles complex numbers with uncertainties in both the real and imaginary
    parts and they can be independent or correlated.  Linear propagation of uncertainty
    is used.  The implementation uses mpmath numbers, which also supplies a rich set of
    special functions.  Thus, the Num class should be able to handle most routine
    calculations.

    The "deep" contribution of the Num class is the use of "semantic units".  As
    mentioned, this is done by using the GNU units executable in a separate process.  An
    innovation is that this computation model easily supports the use of
    dynamically-defined units.  You can define new units like "bags_of_concrete" or
    "workmen" and they are incorporated into a new units definition file for the GNU
    units program; it's then restarted with the new units and the -c option is used to 
    check the new units are correctly defined.  This happens behind the scenes, so you
    as a REPL user don't need to think about the mechanics, you just use a new unit
    string.  You can, however, supply a GNU units configuration file type of definition
    that defines the new unit in terms of old units.  Otherwise, the new unit is defined
    to be a primitive unit with the "unit !" syntax.  In some sense, this allows the Num
    class to "learn" new tricks (but it's really just adapting to the problem domain
    defined by you).

    The python code was written by myself and Google's Gemini AI, which I call Mike to
    give "him" a short name.  This code is very much the result of the partnership of
    the AI and it has been an interesting journey for me, realizing that I had a
    powerful partner to help me with complex coding tasks and the ability to explore
    architectural choices, decisions, and ramifications.  The AI brings vast knowledge,
    incredible speed, and lots of patience to the table.  The human brings taste, lots
    of practical experience, and the vision of where to go.  It has been a remarkable
    partnership of collaboration, with the most surprising part (to me) of the
    synergistic innovation that happens:  together, we produced things and ideas that
    neither of us would have thought of on our own.  It's been a lot like working
    with the great colleagues I had at HP 25 to 45 years ago.

    Mike and I are calling this Num class the "Noether REPL", as the deep realization
    needed to appreciate this name is that a number and its unit is a Noether invariant.
    You can think of the different physical and logical units as components in a vector
    space.  When you construct a Num instance like Num("1.23 kg*m/s2") (in GNU units
    syntax, "s2" means "s squared"), it's essentially a number 1.23 coupled with a
    "vector" with components M*L*T⁻² (mass, length, and time).  The specific unit names
    pick out scaled component lengths (in the example, the units are all base SI units
    (the default) and the scaled lengths are 1).  We call the "product" of the number
    1.23 and the units the "Noether invariant" after Emmy Noether's theorem that relates
    transformational symmetries to conserved quantities.  Here, the transformations are
    scaling transformations (called dilatations or dilations) and Num("1.23 kg*m/s2") is
    an invariant with respect to these dilatations.  The core numerical idea is that the
    number 1.23 has to change if the units kg*m/s2 change, otherwise Num("1.23 kg*m/s2")
    doesn't represent an invariant.  Since kg*m/s2 are newtons, you could instead use
    pounds-force as the unit.  To properly represent the invariant, we'd need to scale
    1.23 by 0.2248 to get the new numerical portion.  Then we can say
    Num("1.23 kg*m/s2") == Num("0.2765 lbf") to four figures.  In physical problems,
    this Num instance might be a component of e.g. a three dimensional Cartesian vector
    for a kinematic calcuation.

Features of the "Noether REPL"

    - Uses the Num python class to peform numerical calculations with units
        - Num instances have a .d attribute for documentation that lets you type in
          arbitrary notes with the instance, just like a lab notebook.  You can easily
          edit these notes in the REPL later with your favorite editor as things change.
          A database keeps track of all these changes so you can understand what was
          done later.
    - Units
        - It understands most physical units you're likely to use
        - You can dynamically define new units for your problem at hand
        - The use of "logical" units is an important feature for solving problems, as
          the powerful GNU units tool will flag incorrect use of _any_ defined units,
          whether they are physical or logical
    - Python's syntax lets you use Unicode symbols
    - Input
        - You can type numbers in as you're accustomed to
        - You can add comments and documentation to keep track of your thinking.  This
          makes it easier to review things later and understand what you did.
    - Display precision
        - The default display precision of the Num class is 3 digits, which should serve
          nicely for most practical problems.
        - The calculational precision is set by default to 15 digits, but you can set it
          to any needed precision before starting a problem to ensure the numerical
          noise is well below the decision limits of the problem.
    - Deep ideas
        - A core idea is "the 'product' of the numerical value and the physical unit is
          an invariant under scaling transformations."  As in group theory, the
          representation can vary (e.g. a matrix representation of SO(3)), but the
          underlying structure is a constant.
            - For practical invariance in the code, we use the "representation" in SI
              units 
        - We're using the term "semantic unit" to describe not only the familiar
          physical units like amperes, but the logical units used in all problems.  For
          example, in a business calculation of when a construction project will be
          completed, you'd use "man" as a semantic unit that's important to the problem,
          as you'd estimate the labor needed to construct something in man*hours.  Costs
          could then be calculated using dollars/(man*hour).  These semantic units are
          vital to stating the problem.
            - The Noether REPL uses the GNU units program to perform the unit algebra
              calculations and conversions
            - Interestingly, the Noether REPL runs the GNU units in a separate process
              and uses it to dynamically define new semantic units, which get added to a
              units configuration file.  Then the units process is restarted, meaning
              the Noether REPL has "learned" the new unit.  It's a very natural behavior
              and feels seamless once you've used it.
        - Persistence
            - The mental model for the REPL is that it's like a lab notebook.  You type
              your thoughts and calculations into it and they are persisted to the file
              system.  You can go back later and ask to see the details of the
              calculation; this helps you refresh your memory of what and why.

Problem statement

    Estimate the material cost to make 22 concrete cylindrical stepping stones for a
    back yard project.  The cost will be the number of $3.2 bags of 90 pounds of
    concrete mix needed to be purchased.  Ignore the mass of water used and calculate
    the mass of needed concrete using the density of cured concrete and equate this to
    the mass of the bagged concrete.

Input information

    - I will deliberately use the screwball customary US units to show that the GNU
      units program used with the internal Num machinery isn't fazed by such units
    - The mass density of the cured concrete is 137 lb/ft³
    - The concrete mix comes in 90 lb bags that cost $3.2 each
    - The diameter of a stepping stone is 1-1/3 yards
    - The thickness of a stepping stone is 3-3/16 inches

Here's how this problem might be solved in a python script (once the guts are working
I'll put it in a REPL dialog)
'''
import number
import mpmath
import wrap
UnitArbiter = number.UnitArbiter
Num = number.Num
if 1:   # Set up plumbing
    UnitArbiter.main_config = "/usr/local/share/units/definitions.units"
    UnitArbiter.dynamic_config = "/home/don/.units_dynamic"
    UnitArbiter.units_bin = "/home/don/.0rc/bin/units"  # Hacked to allow 'q' to quit
def ConcreteExample():  # No pun :^)
    pi = Num(mpmath.pi)
    Num.to_global_namespace("ceil".split())
    if 1:   # Define our semantic units first
        arb = UnitArbiter()
        arb.add_primitive("step")
    if 1:   # Define the input quantities
        number_of_steps = Num("22 steps")   # Note GNU units accepts this plural
        density_concrete = Num("137 lb/ft³")
        mass_per_bag = Num("90 lbm/bag")
        cost_per_bag = Num("3.2 dollars/bag")
        dia_step = Num("1-1/3 yard")
        thick_step = Num("3-3/16 inches")
    if 1:   # Print out our problem to show things are correct
        print(f"number_of_steps = {number_of_steps}")
        print(f"density_concrete = {density_concrete}")
        print(f"mass_per_bag = {mass_per_bag}")
        print(f"cost_per_bag = {cost_per_bag}")
        print(f"dia_step = {repr(dia_step)}")   # bug: fmt.Fmt doesn't handle mixed fractions
        print(f"thick_step = {repr(thick_step)}") # bug: fmt.Fmt doesn't handle mixed fractions
    if 1:   # Perform the calculation
        step = Num("1 step")    # A unit step
        # Calculate the volume of a cylinder 
        vol = pi*dia_step**2/4*thick_step
        # Calculate the volume per step to help us keep the units consistent
        vol_per_step = vol/step
        # Document what we just did
        vol_per_step.d = "Divided vol by a unit step to get units of volume/step"
        # Get the mass per step
        mass_per_step = vol_per_step*density_concrete
        # Get total mass of steps
        mass_all_steps = mass_per_step*number_of_steps
        if 1:
            mass_all_steps.unit = "lb"
        # Calculate number of bags needed
        number_of_bags = ceil(mass_all_steps/mass_per_bag)
        total_cost = cost_per_bag*number_of_bags
    # Print report
    print(wrap.dedent(f'''
        Cost to make {number_of_steps} concrete steps:
            diameter  = {repr(dia_step)}
            thickness = {repr(thick_step)}
            total concrete mass = {mass_all_steps}
            number of bags = {number_of_bags}
            total cost = ${total_cost}
    '''))

ConcreteExample()

'''
❓ Notes
    - .add_unit("step steps") adds a new unit using the GNU units config file syntax.
      Here, a 'step' is defined in terms of the primitive 'steps', defined in the first
      line.
    - The Num constructor should also handle proper fractions (it now only handles
      improper fractions that contain '/')
    - Is there a way to automagically make the needed type conversion of Num to mpf or
      mpc happen so this works?  If not, then we'll e.g. need a attributes like .mpf or
      .mpc, which force a type conversion so the syntax works.
'''
