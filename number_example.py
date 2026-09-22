'''

9 Apr 2026 This contains examples of the use of the "Noether REPL" (number.py)

'''
import number
import mpmath
import trm
import wrap
import sys

UnitArbiter = number.UnitArbiter
Num = number.Num
t = trm.TrmDP()
t.err = t("whtl", "red")
if 1:   # Set up plumbing
    UnitArbiter.main_config = "/usr/local/share/units/definitions.units"
    UnitArbiter.dynamic_config = "/home/don/.units_dynamic"
    UnitArbiter.units_bin = "/home/don/.0rc/bin/units"  # Hacked to allow 'q' to quit
if 1:   # Functions containing examples
    def ConcreteExample():
        '''This example estimates the material cost to make 22 concrete cylindrical stepping
        stones for a back yard project.  The cost will be the number of $3.2 bags of 90
        pounds of concrete mix needed to be purchased.  Ignore the mass of water used and
        calculate the mass of needed concrete using the density of cured concrete and equate
        this to the mass of the bagged concrete.
        
        - I will deliberately use the screwball customary US units to show that the GNU
        units program used with the internal Num machinery isn't fazed by such units
        - The mass density of the cured concrete is 137 lb/ft³
        - The concrete mix comes in 90 lb bags that cost $3.2 each
        - The diameter of a stepping stone is 1-1/3 yards
        - The thickness of a stepping stone is 3-3/16 inches
        '''
        pi = Num(mpmath.pi)
        pi.fmt.n = 4
        if 1:   # Define our semantic units first
            x = Num(0)
            x.base("step")
            x.base("Bag")
        if 1:   # Define the input quantities
            number_of_steps = Num("22 steps")   # Note GNU units accepts this plural
            density_concrete = Num("137 lb/ft³")    # 137 lb/ft³
            mass_per_bag = Num("90 lb/Bag")
            cost_per_bag = Num("3.2 dollar/Bag")
            dia = Num("3-1/3 yd")
            thickness = Num("3-3/16 inch")
        if 1:   # Print out our problem to show things are correct
            print(f"number_of_steps = {number_of_steps}")
            print(f"density_concrete = {density_concrete} = {density_concrete.to('kg/m3')}")
            print(f"mass_per_bag = {mass_per_bag} = {mass_per_bag.to('kg/Bag')}")
            print(f"cost_per_bag = {cost_per_bag}")
            print(f"dia = {dia}")
            print(f"thickness = {thickness}") 
            print()
        if 1:   # Perform the calculation
            step = Num("1 step")    # A unit step
            # Calculate the volume of a cylinder 
            vol = pi*dia**2/4*thickness
            # Calculate the volume per step to help us keep the units consistent
            vol_per_step = vol/step
            print(f"+ vol_per_step = {vol_per_step}")
            # Document what we just did
            vol_per_step.d = "Divided vol by a unit step to get units of volume/step"
            # Get the mass per step
            mass_per_step = vol_per_step*density_concrete
            print(f"+ mass_per_step = {mass_per_step}")
            # Get total mass of steps
            mass = mass_per_step*number_of_steps
            if 1:
                mass.unit = "lb"
            print(f"+ mass = {mass}")
            # Calculate number of bags needed
            number_of_bags = mass/mass_per_bag
            print(f"+ number_of_bags = {number_of_bags}")
            n = (mass/mass_per_bag).num   # .num gets just number
            total_cost = cost_per_bag*number_of_bags
        # Print report
        print(wrap.dedent(f'''
            Cost to make {number_of_steps} concrete steps:
                diameter  = {dia}
                thickness = {thickness}
                total concrete mass = {mass}
                number of bags = {number_of_bags}
                total cost = ${total_cost}
        '''))
    def DogsAndCats(no_programming_error=True):
        '''Each dog gets 0.2 kg of food and cats get 0.1 kg of the same food.  We have to
        feed 7 dogs and 12 cats.  How much food do we need?
        '''
        # Define semantic units
        x = Num("1 m")
        breakpoint() # ∞∞ 
        x.base("dog")         # Create a new semantic unit
        x.base("cat")
        # Define the input quantities
        num_dogs = Num("7 dog")
        num_cats = Num("12 cat")
        dog_food_rate = Num("0.2 kg/dog")
        cat_food_rate = Num("0.1 kg/cat")
        # Solve the problem
        if no_programming_error:
            food_mass = num_dogs*dog_food_rate + num_cats*cat_food_rate
        else:
            food_mass = num_cats*dog_food_rate + num_dogs*cat_food_rate
        # Print results
        print(f"number of dogs = {num_dogs}")
        print(f"number of cats = {num_cats}")
        print(f"dog food rate  = {dog_food_rate}")
        print(f"cat food rate  = {cat_food_rate}")
        print(f"amount of food = {food_mass}")

if __name__ == "__main__":  
    if 1:
        ConcreteExample()
    else:
        if len(sys.argv) > 1:
            DogsAndCats(False)
        else:
            DogsAndCats(True)
