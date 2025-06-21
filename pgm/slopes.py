'''
Prints out slopes of 1 in x for various angles.
'''
if 1:   # Header
    #from math import tan, atan, pi
    #from fpformat import FPFormat as FP
    from wrap import dedent
    from get import GetNumbers
    from f import flt, tan, atan, pi, degrees, radians
    import termtables as tt
    from color import t
    t.f = t.skyl
if 1:   # Core functionality
    def Slopes():
        angles = GetNumbers("1 2 3 4 5 6 7 8 9 10 12.5 14 15 17.5 20 22.5 25 30 35 40 45")
        print(dedent('''
        Slopes for various angles in degrees.  Slope is given as 1 in X.
        The relationship is angle = atan(1/X).'''))
        slopes = range(1, len(angles) + 2)
        a, b = "Angle, °", "Slope, 1 in X"
        c, d = "--------", "-------------"
        o = [
            [a, b, b, a],
            [c, d, d, d],
        ]
        for angle, slope in zip(angles, slopes):
            a = angle
            b = 1/tan(radians(angle))
            c = slope
            d = degrees(atan(1/c))
            o.append([str(i) for i in (a, b, c, d)])
        tt.print(o, style=" "*15, alignment="c"*4)
    def Rationals(complement=False):
        max_denom = 12
        R = range(1, max_denom + 1)
        s = ("Complement of atan(N/D) in °" if complement else 
            "atan(N/D) in °")
        print(dedent(f'''
        {s}
                                N = numerator
        D'''), end=" ")
        for x in R:
            print(f"{x:4d} ", end=" ")
        print()
        print("--", end=" ")
        for x in R:
            print(" " + "-"*4, end=" ")
        print()
        for x in R:
            print(f"{x:2d}", end=" ")
            for y in R:
                theta = degrees(atan(y/x))
                if complement:
                    theta = 90 - theta
                s = f"{theta:5.1f}"
                if x == y:
                    print(f"{t.f}{s}{t.n}", end=" ")
                else:
                    print(f"{s}", end=" ")
            print()
if __name__ == "__main__":  
    Slopes()
    print()
    Rationals()
    print()
    Rationals(complement=True)
