'''
Plot shoe size graphs
    https://en.wikipedia.org/wiki/Shoe_size

Shoe size is a mess because of multiple "standards", different units, and
unclear meaning of what shoe size really means.  My opinion is that the
size should mean a person's foot sizes, but then this puts the burden of
fitting the shoes to the person's size on the manufacturers, which they
don't want.  Instead, the usual practice is to mean the last size, which is
the tooling around which the shoe is constructed.  This then tells the
consumer nothing about whether that shoe will fit them or not.  

    Table from above wikipedia link for US adult sizes
        Last length          US sizes
        (mm)           Men's            Women's
        203.2                             1
        207.43                            1.5
        211.6            1                2
        215.9            1.5              2.5
        220.13           2                3
        224.36           2.5              3.5
        228.6            3                4
        232.83           3.5              4.5
        237.06           4                5
        241.3            4.5              5.5
        245.53           5                6
        249.76           5.5              6.5
        254.0            6                7
        258.23           6.5              7.5
        262.46           7                8
        266.7            7.5              8.5
        270.93           8                9
        275.16           8.5              9.5
        279.4            9                10
        283.63           9.5              10.5
        287.86           10               11
        292.1            10.5             11.5
        296.3            11               12
        300.56           11.5             12.5
        304.8            12               13
        309.03           12.5             13.5
        313.26           13               14
        317.5            13.5             14.5
        321.73           14               15
        325.97           14.5             15.5
        330.2            15               16
        334.43           15.5             16.5
        338.67           16               17
        342.9            16.5             17.5
        347.13           17               18
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Plot shoe size graphs (needs matplotlib)
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import sys
    if 1:   # Custom imports
        from pylab import *
    if 1:   # Global variables
        # Set dbg to True to see individual plots to screen
        dbg = len(sys.argv) > 1
        if 1: # SafeWorkWear data:  https://safeworkwears.com/measure-foot-size
            # Women's sizes
            sww_women = '''
                True Length	US/CA Size	UK Size	EU Size	Narrow Width	Standard Width	Wide Width
                22.5	6	4	36-37	7.1	7.3	7.8
                23	6.5	4.5	37	7.1	7.6	8.1
                23.5	7	5	37-38	7.3	7.8	8.3
                23.8	7.5	5.5	38	7.3	7.8	8.3
                24	8	6	38-39	7.6	8.1	8.6
                24.6	8.5	6.5	39	7.8	8.3	8.6
                25	9	7	39-40	7.8	8.3	8.8
                25.4	9.5	7.5	40	8.1	8.6	9.1
                25.9	10	8	40-41	8.3	8.6	9.1
                26.2	10.5	8.5	41	8.3	8.8	9.3
                26.7	11	9	41-42	8.6	8.8	9.3'''
            # Men's sizes
            sww_men = '''
                True Length	US/CA Size	UK Size	EU Size	Narrow Width	Standard Width	Wide Width
                24.4	7	6	40	8.6	9.1	9.6
                24.8	7.5	6.5	40-41	8.6	9.3	9.9
                25.2	8	7	41	8.8	9.6	9.9
                25.7	8.5	7.5	41-42	9.1	9.6	10.1
                26	9	8	42	9.1	9.9	10.4
                26.5	9.5	8.5	42-43	9.3	9.9	10.4
                26.8	10	9	43	9.6	10.1	10.6
                27.3	10.5	9.5	43-44	9.6	10.4	10.9
                27.8	11	10	44	9.9	10.4	10.9
                28.3	11.5	10.5	44-45	9.9	10.6	11.1
                28.6	12	11	45	10.1	10.9	11.1
                29.2	12.5	11.5	45-46	10.4	10.9	11.4
                29.4	13	12	46	10.4	11.1	11.6'''
        if 1: # Wikipedia adult sizes https://en.wikipedia.org/wiki/Shoe_size#Conversion_between_US_and_UK_sizing
            # Note length is in mm
            # Women's sizes
            wp_women = '''
                Last length    Size
                    203.2       1
                    207.43      1.5
                    211.6       2
                    215.9       2.5
                    220.13      3
                    224.36      3.5
                    228.6       4
                    232.83      4.5
                    237.06      5
                    241.3       5.5
                    245.53      6
                    249.76      6.5
                    254.0       7
                    258.23      7.5
                    262.46      8
                    266.7       8.5
                    270.93      9
                    275.16      9.5
                    279.4       10
                    283.63      10.5
                    287.86      11
                    292.1       11.5
                    296.3       12
                    300.56      12.5
                    304.8       13
                    309.03      13.5
                    313.26      14
                    317.5       14.5
                    321.73      15
                    325.97      15.5
                    330.2       16
                    334.43      16.5
                    338.67      17
                    342.9       17.5
                    347.13      18'''
            # Men's sizes
            wp_men = '''
                Last length    Size
                    211.6       1
                    215.9       1.5
                    220.13      2
                    224.36      2.5
                    228.6       3
                    232.83      3.5
                    237.06      4
                    241.3       4.5
                    245.53      5
                    249.76      5.5
                    254.0       6
                    258.23      6.5
                    262.46      7
                    266.7       7.5
                    270.93      8
                    275.16      8.5
                    279.4       9
                    283.63      9.5
                    287.86      10
                    292.1       10.5
                    296.3       11
                    300.56      11.5
                    304.8       12
                    309.03      12.5
                    313.26      13
                    317.5       13.5
                    321.73      14
                    325.97      14.5
                    330.2       15
                    334.43      15.5
                    338.67      16
                    342.9       16.5
                    347.13      17'''
if 1:   # Plotting
    def Vector(s):
        'Return a list of floats from the string s'
        return [float(i) for i in s.split()]
    def Length():
        def Nike():
            if dbg:
                clf()
            # Nike data https://www.nike.com/a/how-to-measure-foot-size
            # Women's data
            length = [float(i) for i in 
                    "8.5 8.8 8.9 9.1 9.3 9.4 9.5 9.7 9.9 10 10.2 10.3 10.5 10.7 10.9".split()]
            size = [float(i) for i in
                    "5 5.5 6 6.5 7 7.5 8 8.5 9 9.5 10 10.5 11 11.5 12".split()]
            plot(length, size, "o-", label="Women, Nike")
            # Men's data
            length = [float(i) for i in 
                    " 9.9 10.1 10.3 10.4 10.6 10.8 10.9 11.1 11.3 11.5 11.7 11.8 12 12.2 12.3".split()]
            size = [float(i) for i in
                    "8 8.5 9 9.5 10 10.5 11 11.5 12 12.5 13 13.5 14 14.5 15".split()]
            plot(length, size, "o-", label="Men, Nike")
            if dbg:
                xlabel("Length, inches")
                ylabel("US Shoe Size")
                title("Length in inches to US Shoe Size")
                legend()
                grid()
                show()
        def SafeWorkWears():
            # https://safeworkwears.com/measure-foot-size
            # Measurements in cm, tab-separated
            if dbg:
                clf()
            # Women's sizes
            length, size = [], []
            lines = []
            for line in sww_women.split("\n"):
                line = line.strip()
                if not line:
                    continue
                f = line.split("\t")
                if f[0] != "True Length":
                    lines.append(f)
            for line in lines:
                length.append(float(line[0])/2.54)
                size.append(float(line[1]))
            plot(length, size, "o-", label="Women, SafeWorkWears")
            # Men's sizes
            length, size = [], []
            lines = []
            for line in sww_men.split("\n"):
                line = line.strip()
                if not line:
                    continue
                f = line.split("\t")
                if f[0] != "True Length":
                    lines.append(f)
            for line in lines:
                length.append(float(line[0])/2.54)
                size.append(float(line[1]))
            plot(length, size, "o-", label="Men, SafeWorkWears")
            if dbg:
                xlabel("Length, inches")
                ylabel("US Shoe Size")
                title("Length in inches to US Shoe Size")
                legend()
                grid()
                show()
        def Wikipedia():
            if dbg:
                clf()
            # Women's sizes
            length, size = [], []
            lines = []
            s = "Last"
            for line in wp_women.split("\n"):
                line = line.strip()
                if not line:
                    continue
                f = line.split()
                if not f[0].startswith(s):
                    lines.append(f)
            for line in lines:
                length.append(float(line[0])/25.4)
                size.append(float(line[1]))
            plot(length, size, "o-", label="Women, Wikipedia")
            # Men's sizes
            length, size = [], []
            lines = []
            for line in wp_men.split("\n"):
                line = line.strip()
                if not line:
                    continue
                f = line.split()
                if not f[0].startswith(s):
                    lines.append(f)
            for line in lines:
                length.append(float(line[0])/25.4)
                size.append(float(line[1]))
            plot(length, size, "o-", label="Men, Wikipedia")
            if dbg:
                xlabel("Length, inches")
                ylabel("US Shoe Size")
                title("Length in inches to US Shoe Size")
                legend()
                grid()
                show()
            text(10, 2, "Wikipedia length is the size of the last")
        clf()
        Nike()
        SafeWorkWears()
        Wikipedia()
        if not dbg:
            xlabel("Length, inches")
            ylabel("US Shoe Size")
            title("Length in inches to US Shoe Size")
            legend()
            grid(True, which="both")
            savefig("shoesize_length.png")
    def Width():
        def Nike():
            # Women's:  US shoe size vs. width in inches
            size = Vector("5 6 7 8 9 10 11 12")
            narrow = Vector("2.8 2.9 3.1 3.2 3.3 3.4 3.6 3.7")
            medium = Vector("3.2 3.3 3.4 3.6 3.7 3.8 3.9 4.1")
            wide = Vector("3.5 3.7 3.8 3.9 4.1 4.2 4.3 4.4")
            plot(narrow, size, "o-", label="Women, Nike, narrow")
            plot(medium, size, "o-", label="Women, Nike, medium")
            plot(wide, size, "o-", label="Women, Nike, wide")
            # Men's:  US shoe size vs. width in inches
            size = Vector("8 9 10 11 12 13 14 15")
            narrow = Vector("3.6 3.7 3.8 3.9 4.1 4.2 4.3 4.4")
            medium = Vector("3.8 3.9 4.0 4.1 4.3 4.4 4.6 4.6")
            wide = Vector("3.9 4.1 4.2 4.3 4.4 4.6 4.8 4.8")
            plot(narrow, size, "s-", label="Men, Nike, narrow")
            plot(medium, size, "s-", label="Men, Nike, medium")
            plot(wide, size, "s-", label="Men, Nike, wide")
            if dbg:
                xlabel("Length, inches")
                ylabel("US Shoe Size")
                title("Length in inches to US Shoe Size")
                legend()
                grid()
                show()

        #def SafeWorkWears():
        clf()
        Nike()
        #SafeWorkWears()
        if not dbg:
            xlabel("Width, inches")
            ylabel("US Shoe Size")
            title("Width in inches to US Shoe Size")
            legend()
            grid(True, which="both")
            savefig("shoesize_width.png")

if __name__ == "__main__":
    Length()
    #Width()
