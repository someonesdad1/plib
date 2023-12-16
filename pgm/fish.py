'''
This script does a brute-force search for the solutions to the fish
puzzle:
 
    There are 5 houses in five different colors.  In each house lives a
    person with a different nationality.  These 5 owners drink a certain
    drink, smoke a certain brand of tobacco and keep a certain pet.  No
    owners have the same pet, smoke the same tobacco, or drink the same
    drink.
 
    The question is:  Who owns the fish?
 
    Hints:
 
    1.  The Brit lives in the red house.
    2.  The Swede keeps dogs as pets.
    3.  The Dane drinks tea.
    4.  The green house is on the left of the white house.
    5.  The green house owner drinks coffee.
    6.  The person who smokes Pall Mall raises birds.
    7.  The owner of the yellow house smokes Dunhill.
    8.  The man living in the house right in the center drinks milk.
    9.  The Norwegian lives in the first house.
    10. The man who smokes Blends lives next to the one who keeps cats.
    11. The man who keeps horses lives next to the one who smokes Dunhill.
    12. The owner who smokes Bluemaster drinks beer.
    13. The German smokes Prince.
    14. The Norwegian lives next to the blue house.
    15. The man who smokes Blends has a neighbor who drinks water.
 
Here are the major steps in solving the problem:
 
    1.  Generate the 5^5 = 3125 possible combinations of the characteristics.
        Use the hints to reduce this set to the 51 combinations that meet
        these constraints.  (See the function ListCombinations()).
 
    2.  There are 51 choose 5 combinations of the remaining possibilities.
        Generate each of these combinations, then examine each of the 5!
        = 120 permutations of this choice for solutions.
 
Note:  this script was originally written in python 1.5.2 during a
weekend in 2000 when my wife and daughter went to the Winter Olympics in
Utah.  It took about 120 minutes to solve the problem.

Fri 19 Feb 2016 10:01:57 AM Search time on Intel Quad running Ubuntu
    14.04 (machine Jimmy built in Feb 2011):
        Search time = 620.7 sec = 10.3 minutes

Tue 28 Nov 2017 08:37:46 PM
    Run on newer Windows computer with RAM disks that Jimmy built me
    around mid-2016.  Time to solve = 357.7 s = 5.9 minutes

Thu 06 May 2021 07:29:43 PM
    Same Windows computer with python 3.7.7 in 300 s = 5.0 minutes.

Fri 15 Dec 2023 03:00:02 PM
    Same Windows computer with python 3.9.10 in 246 s = 4.1 minutes.

---------------------------------------------------------------------------

I've analyzed a copy of this script and it's pretty clear that it would be
difficult to speed up because it's going through 2.3e6 iterations of a
function in the main while loop and this function takes around 0.12 ms,
which gives about 300 s execution time.  The search rate is 939k
permutations checked per second.  Note there were 281887200 permutations
checked, which is (51 choose 5)*5! or 51*50*49*48*47 = 281887200.

The only strategies for more speed would be
    - Reduce the number of combinations that need to be checked
    - Reduce the time that CheckCombination() takes
    - Use multiple threads


'''
 
# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
import re
import sys
import time
import comb_perm

###########################Global Variables ##################################

colors = ["red", "green", "white", "yellow", "blue"]
nations = ["Swede", "Dane", "Brit", "Norwegian", "German"]
drinks = ["tea", "coffee", "milk", "beer", "water"]
pets = ["dogs", "birds", "cats", "fish", "horses"]
tobaccos = ["PallMall", "Dunhill", "Blends", "Prince", "Bluemaster"]

# The following tuple contains the allowed 51 lines as generated by
# the GenerateCombinationsList function.
allowed_combinations = []

# Indexes for house color, nationality, drink, pet, and tobacco
C, N, D, P, T = 0, 1, 2, 3, 4

always_print = 0   # For debugging; print out every comb/perm checked

# Keep track of how many possibilities we look at.  This should be
# equal to (51 choose 5) * 5! = 281887200 at the end of calculation.
total_examined = 0

# perms will contain the 120 permutations of 5.  The numbers are 0-based
# to allow easy indexing into a sequence.  We'll use these elements to
# get the 120 permutations of the selected combination of 5 lines.

perms = ()

############################## Functions #####################################

def ListCombinations(A1, A2, A3, A4, A5):
    '''Return a list of all possible combinations of the sets of elements.
    Each combinations is a tuple of the five characteristics.  The output
    list is:
        [('red', 'Swede', 'tea', 'dogs', 'PallMall'),
         ('red', 'Swede', 'tea', 'dogs', 'Dunhill'),
         ('red', 'Swede', 'tea', 'dogs', 'Blends'),
         ('red', 'Swede', 'tea', 'dogs', 'Prince'),
         ('red', 'Swede', 'tea', 'dogs', 'Bluemaster'),
         ('red', 'Swede', 'tea', 'birds', 'PallMall'),
         etc.
    '''
    list = [
        (a1, a2, a3, a4, a5)
        for a1 in A1 for a2 in A2 for a3 in A3 for a4 in A4 for a5 in A5
    ]
    assert(len(list) == 5**5)   # 5**5 = 3125
    return list

def ApplyEqConstraint(list, index1, value1, index2, value2):
    '''For each item in the list of tuples, check that the item
    satisfies the constraint; if not, remove it from the list.  The Eq
    constraint is where if a combination contains either value 1 or
    value 2, it must contain the pair.  Example: the red house must
    contain the Brit.  Note we start at the end of the list and work
    backwards (this avoids "chopping off the limb you're standing on").
    '''
    for ix in range(len(list)-1, -1, -1):
        item = list[ix]
        if item[index1] == value1 and item[index2] != value2:
            del list[ix]
        if item[index2] == value2 and item[index1] != value1:
            del list[ix]

def ApplyNotEqConstraint(list, index1, value1, index2, value2):
    '''For each item in the list of tuples, check that the item satisfies
    the constraint; if not, remove it from the list.  Note we work backwards
    from the end of the list.  The NotEq constraint is where the combination
    must not contain the value1/value2 pair.  Example:  a particular house
    cannot use Blends tobacco and keep cats.
    '''
    for ix in range(len(list)-1, -1, -1):
        item = list[ix]
        if item[index1] == value1 and item[index2] == value2:
            del list[ix]

def GenerateCombinationsList():
    combinations = ListCombinations(colors, nations, drinks, pets, tobaccos)
    # Apply the constraints where both items must be present
    ApplyEqConstraint(combinations, C, "red", N, "Brit")            # Hint 1
    ApplyEqConstraint(combinations, N, "Swede", P, "dogs")          # Hint 2
    ApplyEqConstraint(combinations, N, "Dane", D, "tea")            # Hint 3
    ApplyEqConstraint(combinations, C, "green", D, "coffee")        # Hint 5
    ApplyEqConstraint(combinations, P, "birds", T, "PallMall")      # Hint 6
    ApplyEqConstraint(combinations, C, "yellow", T, "Dunhill")      # Hint 7
    ApplyEqConstraint(combinations, D, "beer", T, "Bluemaster")     # Hint 12
    ApplyEqConstraint(combinations, N, "German", T, "Prince")       # Hint 13
    # Apply the constraints where both items must not be present at same time
    ApplyNotEqConstraint(combinations, P, "cats", T, "Blends")      # Hint 10
    ApplyNotEqConstraint(combinations, P, "horses", T, "Dunhill")   # Hint 11
    ApplyNotEqConstraint(combinations, C, "blue", N, "Norwegian")   # Hint 14
    ApplyNotEqConstraint(combinations, D, "water", T, "Blends")     # Hint 15
    combinations.sort()
    return combinations

def GreenNotLeftOfWhite(candidate):
    white_found = 0
    green_found = 0
    for ix in range(len(candidate)):
        possibility = candidate[ix]
        if possibility[C] == "white":
            white_found = 1
        if possibility[C] == "green":
            green_found = 1
        if white_found and not green_found:
            return 1
        if green_found and not white_found:
            return 0
    print("\nError in following candidate:")
    PrintCandidate(candidate, "  ")
    raise Exception("Green and white not found")   # Should never reach here

def PrintCandidate(candidate, prefix):
    for item in candidate:
        if prefix != "":
            print(prefix, end="")
        print(("%-12s " * 5) % item)

def BlendsFailed(candidate):
    '''Hint 10 says Blends must be next to cats and water.  Find the index
    of Blends and then check these two statements.
    '''
    blends = -1
    for ix in range(len(candidate)):
        if candidate[ix][T] == "Blends":
            blends = ix
    if blends == 0:
        if candidate[1][P] != "cats":
            return 1
        if candidate[1][D] != "water":
            return 1
    elif blends == 1:
        if candidate[0][P] != "cats" and candidate[2][P] != "cats":
            return 1
        if candidate[0][D] != "water" and candidate[2][D] != "water":
            return 1
    elif blends == 2:
        if candidate[1][P] != "cats" and candidate[3][P] != "cats":
            return 1
        if candidate[1][D] != "water" and candidate[3][D] != "water":
            return 1
    elif blends == 3:
        if candidate[2][P] != "cats" and candidate[4][P] != "cats":
            return 1
        if candidate[2][D] != "water" and candidate[4][D] != "water":
            return 1
    elif blends == 4:
        if candidate[3][P] != "cats":
            return 1
        if candidate[3][D] != "water":
            return 1
    else:
        raise Exception("Blends not found")
    return 0

def DunhillFailed(candidate):
    '''Hint 11 says Dunhill must be next to horses.  Find the index of
    Dunhill and then check this statement.
    '''
    dunhill = -1
    for ix in range(len(candidate)):
        if candidate[ix][T] == "Dunhill":
            dunhill = ix
    if dunhill == -1:
        raise Exception("Dunhill not found")
    elif dunhill == 0:
        if candidate[1][P] != "horses":
            return 1
    elif dunhill == 4:
        if candidate[3][P] != "horses":
            return 1
    else:
        if (candidate[dunhill-1][P] != "horses" and
                candidate[dunhill+1][P] != "horses"):
            return 1
    return 0

def IsSolution(candidate):
    '''candidate is a tuple of 5 of the lines of the following form:
        (
            (s1, s2, s3, s4, s5),
            (s1, s2, s3, s4, s5),
            (s1, s2, s3, s4, s5),
            (s1, s2, s3, s4, s5),
            (s1, s2, s3, s4, s5),
        )
    Check to see if it satisfies the constraints of the problem.  We first
    check the three constraints (I'm using 0-based numbering here)
        - House 0 must contain the Norwegian
        - House 1 must be blue
        - House 2 must contain the milk drinker
    since not meeting these will weed out most candidates.  If this
    hurdle is passed, then the remaining constraints are checked.
 
    The assumption here is that houses are numbered from left to right
    so that the house number on the left is number 1, the next one is 2,
    etc.
    '''
    # Make the easy checks for the first 3 houses
    if candidate[0][N] != "Norwegian":
        return 0
    if candidate[1][C] != "blue":
        return 0
    if candidate[2][D] != "milk":
        return 0
    # Next most easy checks:  verify that each item in each position is
    # unique.
    for first_item in range(5):
        candidate1 = candidate[first_item]
        for second_item in range(first_item + 1, 5):
            candidate2 = candidate[second_item]
            for characteristic in range(5):
                if candidate1[characteristic] == candidate2[characteristic]:
                    return 0
    # Test the remaining constraints
    if GreenNotLeftOfWhite(candidate):
        return 0
    if BlendsFailed(candidate):
        return 0
    if DunhillFailed(candidate):
        return 0
    # If reach here, we've found a solution, so return true
    return 1

def GeneratePermutations(possibility):
    '''possibility is a tuple of 5 tuples; each tuple represents one of the
    combinations of the 51 possibilities.  This function will generate a
    tuple of 120 tuples, each containing a permutation of the original
    tuple.
    '''
    candidates = []
    for permutation in perms:
        candidate = []
        for ix in range(5):
            candidate.append(possibility[permutation[ix]])
        candidates.append(tuple(candidate))
    return tuple(candidates)

def CheckCombination(comb):
    '''comb is a tuple of 5 0-based indexes chosen from the numbers 0-51
    inclusive.  Use it to get the 5 tuples indicated, then generate each
    permutation of these 5 tuples and check them as possible solutions.
    '''
    global total_examined
    possible_lines = (
        allowed_combinations[comb[0]],
        allowed_combinations[comb[1]],
        allowed_combinations[comb[2]],
        allowed_combinations[comb[3]],
        allowed_combinations[comb[4]],
    )
    candidates = GeneratePermutations(possible_lines)
    for ix in range(len(candidates)):
        candidate = candidates[ix]
        total_examined = total_examined + 1
        if IsSolution(candidate):
            # Print the solution just found
            for item in candidate:
                print(("%-12s " * 5) % item)
            print()
        else:
            if always_print:
                for item in candidate:
                    print("+    ", end="")
                    print(("%-12s " * 5) % item)
                print()

def GetPerms():
    '''Fill the perms sequence, which will contain tuples of the permutations
    of (0, 1, 2, 3, 4).
    '''
    global perms
    array = []
    array.append(tuple(comb_perm.GetPermutation(5, init=1, zero_based=1)))
    p = comb_perm.GetPermutation(5)
    while p:
        array.append(tuple(p))
        p = comb_perm.GetPermutation(5)
    perms = tuple(array)

if __name__ == "__main__":
    start_time = time.time()
    allowed_combinations = GenerateCombinationsList()
    GetPerms()
    # From an earlier version of this program, we know this should be a
    # list of 51 combinations.
    assert(len(allowed_combinations) == 51)
    # Now generate the 51 choose 5 combinations of these possible lines
    # and examine each combination as a possible solution.
    current_combination = comb_perm.GetCombination(51, 5, init=1, zero_based=1)
    # The first combination is (0, 1, 2, 3, 4)
    count = 1  # Number of combinations examined
    total_expected = 51*50*49*48*47/(5*4*3*2)    # (51 choose 5)
    last_printed = -1
    while current_combination:
        CheckCombination(current_combination)
        # Print percent done in 10% increments to stderr
        pct = int(100.*count/total_expected)
        if pct % 10 == 0 and pct > 0 and pct != last_printed:
            sys.stderr.write("%d%% finished\n" % pct)
            last_printed = pct
        count = count + 1
        current_combination = comb_perm.GetCombination(51, 5)
    count = count - 1   # Last one is None
    finish_time = time.time()
    total_time = finish_time - start_time
    print("Search time = %.1f" % total_time, "sec")
    print("Search rate = %.0f permutations/sec" % (total_examined/total_time))
    print("Total number of permutations checked =", total_examined)
    print("(51 choose 5) * 5!                   =", total_examined)
