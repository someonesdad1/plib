"""
Show the sprinkler watering schedule.
"""

if __name__ == "__main__":
    print(
        """
A = our controller's A program
B = our controller's B program
F = flood irrigators' times
. = anyone can water
4 = our watering time
We can also water during the time of any number less than 4 because
we are downstream of these folks.

            Mon     Tue     Wed     Thu     Fri     Sat     Sun
            ---     ---     ---     ---     ---     ---     ---
12 am        6       .       6       .       6       .       .
 1 am        6       .       6       .       6       .       .
 2 am        6       .       6       .       6       .       .
 3 am        6       .       6       .       6       .       .
 4 am        6       .       6       .       6       .       .

 5 am        6       .       6F      .       6       .       .
 6 am        1       2       5F      .       1       7F      .
 7 am        1      A2       5F     A.       1       7F      .
 8 am        1      A2       5F     A.       1       7F      .
 9 am        1      A2       5F     A.       1       7F      .

10 am        3      A4       5F     A2       3       8F      5F
11 am        3      A4       5F     A2       3       8F      5F
12 pm        3      A4       5F     A2       3       8F      5F
 1 pm        3      A4       5F     A2       3       8F      5F

 2 pm        5F     A.       1      A4       5F      2       7F
 3 pm        5F      .       1       4       5F      2       7F
 4 pm        5F      .       1       4       5F     B2       7F
 5 pm        5F      .       1       4       5F     B2       7F

 6 pm        .       .       3       .       5F     B4       8F
 7 pm        .       .       3       .       5F     B4       8F
 8 pm        .       .       3       .       5F     B4       8F
 9 pm        .       .       3       .       5F     B4       8F

10 pm        6       .       6       .       6      B.       . 
11 pm        6       .       6       .       6      B.       . 

Circuit times in minutes        Total run time = 140 + 320 = 460 minutes
    1/3, 7/8        70                         = 7 hr 40 min = 7.7 hr
    4, 5, 6, 9      80
Total watering time = 3(70) + 4(80) = 210 + 320 = 530 = 8:50 = 8.83 hr
Ditch pump time     = 3(70) + 3(80) = 210 + 240 = 450 = 7:30 = 7.5  hr
    (because #9 runs from the well)
""".strip()
    )
