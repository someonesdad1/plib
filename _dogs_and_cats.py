def DogsAndCats(no_programming_error=True):
    '''Each dog gets 0.2 kg of food and cats get 0.1 kg of the same food.  We have to
    feed 7 dogs and 12 cats.  How much food do we need?
    '''
    from number import Num
    # Define semantic units
    x = Num("1 m")          # New utility number instance
    x.base("dog")           # Create a new semantic unit
    x.base("cat")
    # Define the input quantities
    num_dogs = Num("7 dogs")    # Num instances can include units
    num_cats = Num("12 cats")
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
    import sys
    if len(sys.argv) > 1:
        DogsAndCats(False)
    else:
        DogsAndCats(True)
