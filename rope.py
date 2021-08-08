'''
Print table of strength of Samson double braid polyester rope
'''

if 1:   # Imports
    from fractions import Fraction
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
    from f import flt
    from get import GetFraction

def GetData(metric=False, use_fractions=False):
    '''Return a list of 
    [
        diameter_inches,
        mass_lbm_per_100_feet,
        average_strength_klb,
        minimum_strength_klb
    ]
    If use_fractions is True, the diameter_inches will be a fraction.
    Otherwise, it will be a floating point number rounded to two decimal
    places.
    
    If metric is True, return the list
    [
        diameter_mm,
        weight_lb_per_100_feet,
        mass_kg_per_100_m,
        average_strength_kN,
        minimum_strength_kN
    ]
    '''
    dia_in = '''1/4 5/16 3/8 7/16 1/2 9/16 5/8 3/4 7/8 1 1-1/8 1-1/4 1-5/16
                1-1/2 1-5/8 1-3/4 2 2-1/8 2-1/4 2-1/2 2-5/8 2-3/4 3 3-1/4
                3-5/8 4 4-1/4 4-5/8 5'''.split()
    wt_100_ft_lb = '''2.1 3.2 4.5 6.1 8.2 11 14 18 27.1 34 45.3 53.9 60.8 73.3
                   85.9 104 124 147 173 196 225 246 300 375 450 525 589 689
                   788'''.split()
    strength_avg_klb = '''2.3 3.6 5.6 7.7 10.4 13.3 16.3 20.4 29.9 39.2 48.2
                          57.3 64.7 75.1 87.2 104 124 145 166 190 212 234
                          278 343 407 470 533 616 698'''.split()
    strength_min_klb = '''2 3.1 4.8 6.5 8.8 11.3 13.9 17.3 25.4 33.3 41 48.7 55
                          63.8 74.1 88.4 105 123 141 162 180 199 236 292
                          346 400 453 524 593'''.split()
    data = list(zip(dia_in, wt_100_ft_lb, strength_avg_klb, strength_min_klb))
    # Convert first term to a fraction
    for i, item in enumerate(data):
        item = list(item)
        a = item[0]
        item[0] = GetFraction(a)
        if item[0] is None:
            item[0] = Fraction(int(a), 1)
        for j in range(1, 4):
            item[j] = flt(item[j])
        data[i] = item
    flt(0).rtz = flt(0).rtdp = True
    # Convert first element to decimal inches if wanted
    if not use_fractions:
        for i in range(len(data)):
            data[i][0] = round(float(data[i][0]), 2)
    # Convert to metric if wanted
    if metric:
        for i in range(len(data)):
            data[i][0] = flt(round(float(data[i][0])*25.4, 1))
            data[i][1] = flt(round(float(data[i][1])*0.453592, 2))
            data[i][2] = flt(round(float(data[i][2])*4.44822, 2))
            data[i][3] = flt(round(float(data[i][3])*4.44822, 2))
    # xx
    for i in data:
        for j in i:
            print(j, end= " ")
        print()
GetData(metric=1)
