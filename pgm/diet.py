'''
Information relevant to a diet.
'''
 
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Information relevant to a diet
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        from pprint import pprint as pp
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from columnize import Columnize
        import u
        import get
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Utility
    def GetColors():
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''
        There is no magic to losing weight, just as there is no magic to gaining it.  If you
        consider the body as a closed system, then what you breathe and eat are closely related to
        what you put on, take off, and excrete on a daily basis.  In my opinion, the keys are

            - Get the motivation to lose weight
            - Figure out how to keep that motivation over the long term
            - Eat the proper mixture of nutrients to stay healthy
            - Change your eating habits to avoid the behaviors that made you gain too much weight

        Unfortunately, most dietary information uses the screwball "food calorie", which is a kcal
        if you've got a technical background.  A regular calorie is 4.18 J.  I will use the food
        calorie as the basic unit, call it Calorie, and denote it by the symbol C.  I will also
        use pounds for weight because it is the most common unit used by non-technical people in
        the US.

        An important constant is 3500 C/lb.  This is the energy content of fat that your body
        collects when it has too much food, storing it for later when food isn't plentiful.  The
        basic strategy of weight loss is that you have a target value for the weight WL you want to
        lose and you decide on how much energy to reduce in your daily intake, which I'll call ED
        for energy deficit in Calories/day.

        If you can maintain the daily energy deficit, the simple arithmetic gives the number of
        days it will take to lose your target weight:  (3500 C/lb)*(WL in lb)/(ED in C/day).  If
        you cancel out the units, you'll see you're left with days.  More importantly, I can tell
        you from real experience that it works exactly as written.

            Suppose you choose ED = 500 C/day.  Then in 7 days you'll lose 1 pound of fat.  Thus,
            you can probably do the arithmetic in your head to see how long this weight loss is
            going to take.  If it's, say, 25 pounds, then it's going to take you 25 weeks or about
            6 months.  50 pounds will take about a year.  You see why I stated keeping the
            motivation of the long term is important -- it's going to take a goodly amount of
            time.  That shouldn't surprise you, as you probably put the weight on at about the
            same leisurely pace.  Alas, it's painless to put it on, but takes willpower and
            commitment to take it off.

        There are various formulas to estimate your daily energy need based on your height, age,
        gender, weight, and activity level.  You can look up things like the Harris-Benedict
        formula or the Institute of Medicine equation (published in 2002; see
        https://en.wikipedia.org/wiki/Institute_of_Medicine_Equation).  I've used both equations.

        Once you know your daily energy need, discuss with your doctor

            - What a reasonable weight goal should be for you.  The doc will probably base this on
              both your current BMI and what you both agree would be a good target BMI.
            - What daily energy deficit ED is reasonable for you.  

        Example:  My starting BMI (body mass index, see below) was 25.5 and my BMI goal was 22,
        which is right in the middle of the "normal" range.  This required me losing 25 lb of
        weight.  My daily energy need is about 2000 C.  My original planning goal was to have a
        deficit of between 500 C and 1000 C.  
            - Results:  Over 84 days, I lost 17 lb, meaning my daily deficit was 708 C/day.  I was
              within 3 lb of my target weight for that day; believe it or not the uncertainty is
              because I wasn't sure of what exactly my starting weight was.  To reach my target
              weight required another 40 days, so I put the target date on the calendar.  My
              doctor suggested a way to keep my motivation is that in 6 months from my 3 month
              checkup, if my weight has stayed off and my A1c measurement is good, he'll take me
              off two of the three diabetes medicines he has me on.  He was emphatic about this
              because one of these medicines is something he's not fond of, having seen
              complications with it.

        Your daily weight flucuates quite a bit because of the air, water, and food you take in
        and the stuff you excrete out.  It's not meaningful to measure your weight every day
        because of these fluctuations.  Walker in the "Hacker's Diet" suggest a moving average to
        filter out these fluctuations, but I think that's more work than needed.  I measured my
        weight once per week and always made the measurement just after getting up in the morning
        and urinating.  It told me what I needed to know and I didn't need to write the weight
        down, as it was easy to remember.  It was also easy to see if I was making progress by the
        measurement made a week later.

        My core tactic once I had committed to weight loss was to rigidly follow this rule:  after
        I've eaten the allowed amount of food for my planned meal, stop.  Do not eat anything else
        until at least an hour after I've finished my meal.

        The surprising result of doing this is that I was never hungry after I waited that hour.
        My key faulty habit over a lifetime was over-eating because I didn't feel full.  

        Other tactics I use:
            - I take a multivitamin and a single vitamin C tablet once per week.  Make sure you're
              also getting proper levels of protein, fiber, and other nutrients.
            - I mostly eat salads for lunch, which include cabbage, broccoli, cauliflower,
              garbanzo beans, pickled beets and other things we have on-hand (varies around the
              year because of what's grown in our garden).  I put on about half a teaspoon of
              sesame or olive oil and perhaps 50 ml of apple cider vinegar.  Sometimes I'll put in
              an apple, pickled or hard-boiled egg, or other things on-hand.  My wife chops up
              lean ham and puts in in a plastic bag, which lets me add a small amount for protein,
              which also comes from the beans.  I stay away from adding any carbohydrates like
              croutons, dry noodles, etc.  A few peanuts work well too, giving both fats and
              proteins.
            - A simple but good breakfast for me is either a Wasa cracker (35 C) with some cream
              cheese with chopped jalapenos (about 90 C).  This gives me 125 C.  I'll also eat
              about 350 ml of whole milk yogurt with some no-calorie sweetener and some sugar-free
              jam.  This winds up being about 200 C.  I have this with a cup of coffee or tea.
              Occasionally I'll have a toasted sesame bagel with the jalapeno cream cheese and
              it's around 300 C.
            - When I'm trying to achieve a 1000 C daily deficit, I'll often have the jalapeno &
              cream cheese + Wasa cracker for dinner.  I always think I'll be hungry later, but
              I'm not.  I've become a fan of the Wasa crackers, as they store fine on the shelf
              for years past their use by date.
            - I drink a lot of tea and coffee during the day in winter along with Crystal Lite
              iced tea during the hot summer months.  My coffee mug holds about 400 ml and I
              estimate I'll drink 1.5 to 2.5 liters of water per day.  I'll also drink hot water
              and boullion.
            - I've always loved bread, crackers, and other such snacks, but these things are often
              loaded with carbs and fat, so read the labels and limit your intake.  Better, teach
              yourself how to get out of the habit of eating them.
            - Find interesting things to do to keep your mind occupied so you think less about
              eating.

        Meal "planning" is mostly about knowing the food energy content of foods.  I prefer to put
        everything in a specific energy form, which allows comparison and estimation of how
        much energy I'm getting in a serving.  Here, the specific energy measure I use is food
        calories per unit mass, specifically Calories per 100 grams.  You'll want to have a small
        scale and use it to be able to judge about 100 g of food by eye.  This script prints out a
        table of specific energy and you'll want to modify it to fit your choices.

        During the holidays and when we eat at restaurants or other people's houses, I try to be
        sensible, but I don't bend overboard to follow my strict diet.  One day of
        over-consumption while dieting isn't going to kill your gradual weight loss program as
        long as you don't make it a habit.

        John Walker published on the web his book "The Hacker's Diet", which is freely-available
        from http://www.fourmilab.ch/hackdiet.  For my tastes, the content is excellent, but the
        presentation is a bit wordy.  The American Heart Association has some good basic
        information on a healthy diet at
        https://www.heart.org/-/media/AHA/H4GM/PDF-Files/How-much-should-i-eat-Infographic-PDF.pdf.

        BMI is calculated from m/h² where m is mass in kg and h is height in m.  General guidelines for
        BMI are
            Underweight		< 18.5
            Normal		    18.5 to 25
            Overweight		25 to 30
            Obese 		    > 30

        '''))
        exit(0)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [cmd]
          Print out information relevant to a diet.
          e     Estimate daily food energy need
          h     General information
          b     Breakfast info
          l     Lunch info
          d     Dinner info
          m     Metabolism info
          f     Specific energy list of common foods
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    Error(f"-d option's argument must be an integer between 1 and 15")
            elif o == "-h":
                Usage()
        x = flt(0)
        x.N = d["-d"]
        x.rtz = True
        return args
if 1:   # Core functionality
    def GetData():
        'Return a dict of food name to specific energy'
        data = '''
            apple 52
            banana 89
            bell pepper 26
            black beans 92
            blackberries 43
            blackberry jam 250   # Smuckers
            blueberries 57
            broccoli 34
            butter 717
            cabbage 24
            carrots 41
            cauliflower 25
            cheddar cheese 403
            Cheetos 536
            Cheez-Its 500
            chicken, canned 83
            chicken breast, skinless 110
            corn chips 495  # Doritos
            cucumber 12
            pretzels, Dot's 500
            Fritos 571
            garbanzo beans 92
            green beans 31
            hot dog, turkey 353
            kidney beans 82
            mayonnaise 643
            mushrooms 22
            noodles 137
            olive oil 884
            onions 42
            orange 47
            peach 39
            pear 58
            pinto beans 85
            pork tenderloin 136
            raspberries 52
            refried beans 94
            Ritz crackers 500
            sesame oil 884
            Spam 321
            spinach 23
            strawberry 32
            sugar 387
            tomato 18
            tortilla 300    # Mission
            vegetable oil 884
            Wheat Thins 452
            white bread 231 # 60 C in one slice
            yellow squash 16
        '''
        fd = {}
        for i in data.split("\n"):
            i = i.strip()
            if not i:
                continue
            k = i.find("#")
            if k != -1:
                i = i[:k]
            j = i.split()
            fd[' '.join(j[:-1])] = int(j[-1])
        return fd
    g.low = 60
    g.med = 100
    g.hi = 400
    def ColorCoding(energy):
        if energy > g.hi:
            return t.ornl
        elif energy > g.med:
            return t.yell
        elif energy > g.low:
            return t.grnl
        else:
            return t.whtl
    def ColorKey():
        C = ColorCoding
        print(f"{t.n}Color key:  {C(g.low)}< {g.low}, {C(g.med)}< {g.med}, "
              f"{C(g.hi)}< {g.hi}, {t.n}else {C(500)}this")
    def PrintTable():
        fd = GetData()
        d = list(fd.items())
        w = max(len(i) for i in d)
        # Alphabetically sorted
        t.print(f"{t.purl}Calories/100 grams sorted alphabetically")
        o = []
        for name, energy in sorted(d, key=lambda x: x[0].lower()):
            c = ColorCoding(energy)
            o.append(f"{c}{energy:>4d} {name:{w}s}")
        for i in Columnize(o):
            t.print(i)
        # Sorted by specific energy
        t.print(f"\n{t.purl}Calories/100 grams sorted by specific energy")
        o = []
        for name, energy in sorted(d, key=lambda x: x[1]):
            c = ColorCoding(energy)
            o.append(f"{c}{energy:>4d} {name:{w}s}{t.n}")
        for i in Columnize(o):
            print(i)
        ColorKey()
    def Breakfast():
        print(dedent(f'''
        '''))
    def Lunch():
        print(dedent(f'''
        '''))
    def Dinner():
        print(dedent(f'''
        '''))
    def Metabolism():
        print(dedent(f'''
        The Harris-Benedict formula for basal metabolic rate from the early 1900's is (revised by
        Mifflin and St Jeor in 1990)
        
            Men:    BMR in Calories = 10*m + 6.25*h - 5*y + 5
            Women:  BMR in Calories = 10*m + 6.25*h - 5*y - 161
        
        where m is mass in kg, h is height in cm, and y is age in years.  Here are some scaling
        constants to convert BMR to daily energy needs:
        
            Activity Level  Men     Women
            Sedentary       1.3     1.3     Inactive in both work and leisure.
            Light           1.6     1.5     Daily routine includes some walking or intense
                                            exercise once or twice per week.
            Moderate        1.7     1.6     Intense exercise lasting 20-45 minutes at least 
                                            three times per week, or a job with a lot of walking,
                                            or a moderate-intensity job.
            Very            2.1     1.9     Intense exercise lasting at least an hour per day, or 
                                            a heavy physical job, such as a mail carrier or an
                                            athlete in training.
            Extreme         2.4     2.2     A very demanding job, such as working in the armed 
                                            forces or shoveling coal.
        
        The Institute of Medicine equation (published 2002) is 
        
            Men:    EER in Calories = 662 - 9.53*y + 15.91*m*p + 539.6*h
            Women:  EER in Calories = 354 - 6.91*y + 9.36*m*p + 726*h
        
        where
        
            EER = estimate energy requirement in Calories
            m = mass in kg
            h = height in m
            y = age in years
            p = physical activity level:
        
                Activity level      Adult men       Adult women
                Sedentary               1               1
                Moderately active      1.11            1.12
                Active                 1.25            1.27
                Very active            1.48            1.45
        
        Example:  assume a moderately active male with 
        
            m = 70 kg
            h = 1.75 m
            y = 70 years
            p = 1.11
        
        The equation is 662 - 9.53(70) + 15.91(70)(1.11) + 539.6(1.75), which is 662 - 667.1 +
        1236.2 + 994.3 or 2225.4 Calories.  I'd round this to 2200 Calories per day.
        
        '''))
    def GetDailyEnergyNeed():
        '''Show daily Calories needed given mass, height, and age.  The calculation is based on
        the Institute of Medicine equation published in 2002.
        '''
        print("You'll be prompted for mass, height, and age.  Enter different units if desired.")
        # Get m, the mass in kg
        done = False
        nodbg = False
        while nodbg and not done:
            s = "What is mass in lb?"
            mass, unit = get.GetNumber(s, default=150, use_unit=True)
            if unit:
                if u.u(unit, dim=True)[1] != u.u("m", dim=True)[1]:
                    print("You must use a mass unit")
                    continue
                m = mass*u.u(unit)  # Mass in kg
            else:
                m = mass*u.u("lbm")
                mass = f"{mass} lb"
            done = True
        # Get h, the height in m
        done = False
        while nodbg and not done:
            s = "What is height in inches?"
            try:
                height, unit = get.GetNumber(s, default=69.3, use_unit="inches")
            except TypeError:
                print("You must use a length unit")
                continue
            else:
                # Convert to m
                if unit:
                    h = height*u.u(unit)
                    height = f"{height} {unit}"
                else:
                    h = height*u.u("inch")
                    height = f"{height} inches"
                done = True
        # Get y, the age in years
        done = False
        while nodbg and not done:
            y = get.GetNumber("What is age in years? ", default=75, low=18, high=100)
            years = f"{y} years"

        if not nodbg:
            mass = "150 lb"
            m = flt(150)*u.u("lbm")
            height = "69.3 inches"
            h = flt(69.3)*u.u("inch")
            y = flt(75) #xx
            years = f"{y} years" #xx
        # Activity levels and factors
        levels = {
            # Description, factor for males, factor for females
            0: ("Sedentary", 1, 1),
            1: ("Moderately active", 1.11, 1.12),
            2: ("Active", 1.25, 1.27),
            3: ("Very active", 1.48, 1.45),
        }
        # Print report
        i = " "*2
        t.print(f"\n{t.purl}Institute of Medicine daily food energy need in Calories (2002)")
        print(f"{i}Mass   = {mass} = {m} kg")  
        print(f"{i}Height = {height} = {h} m")  
        print(f"{i}Age    = {y} years")  
        w, w1, w2, w3 = 5, 17, 8, 8
        s = " "*w
        print(f"{i}{'Activity level':^{w1}s}{s}{'Male':^{w2}s}{s}{'Female':^{w3}s}")
        print(f"{i}{'-'*w1:{w1}s}{s}{'-'*w2:{w2}s}{s}{'-'*w3:^{w3}s}")
        for j in levels:
            level, pmen, pwomen = levels[j]
            eer_men = 662 - 9.53*y + 15.91*m*pmen + 539.6*h
            eer_women= 354 - 6.91*y + 9.36*m*pwomen + 726*h
            print(f"{i}{level:{w1}s}{' '*w}{eer_men!s:^{w2}s}{' '*w}{eer_women!s:^{w3}s}")
            

if 1:
    GetDailyEnergyNeed()
    exit()
        

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    cmd = args[0].lower()
    if cmd == "h":
        Manpage()
    elif cmd == "e":
        GetDailyEnergyNeed()
    elif cmd == "b":
        Breakfast()
    elif cmd == "l":
        Lunch()
    elif cmd == "r":
        Dinner()
    elif cmd == "m":
        Metabolism()
    elif cmd == "f":
        PrintTable()
