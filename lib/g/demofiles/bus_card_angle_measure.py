'''
Draw a sheet containing scales for estimating sizes of distant objects
or measuring their angular extent.

    Eye measurements in cm:
    dp    65
    gp    55.9

Instructions
    - Hold the card vertically in your hand extended and have someone measure the
      distance from your eye to the card.
    - Use the card that is has the closest eye-to-card distance for you.
    - Use the deg scale to measure the angular extent of an object.  Example:  the moon
      will measure about 0.5 degrees width.
    - To estimate the height of something, put the Ref line on the bottom of the object
      and adjacent to the top of the object, read the approximate multiplier distance.
    - Multiply the multiplier distance by the height of the object to get how far away
      it is from you.
    - Example:  the flag in the hole on a golf green is 72 inches high; call it 1.8 m.
      You measure the height of the flag is "x" units as 37.  Therefore you are about
      37(1.8) = 37(1 + 0.8) = 37 + 30 = 67 m from the flag.  You can do the approximate
      arithmetic in your head:  8 times 37 is 8(30 + 7) = 240 + 56 or 296; divide by 10
      to get 29.6 as the exact answer, which nicely rounds to 30.

'''
import sys
from g import *
from math import sin, cos, tan, pi, sqrt, atan
debug = 0
wrap_in_PJL = 0
d2r = pi/180
mm2in = 1/25.4
t0, t1, t2, t3 = 0.5, 0.75, 1.25, 2
mark_dict = {
    # key is eye distance in mm
    # value is (location_point, num_tenth_degrees, marks)
    # marks is (factor, label_string, tick_length, text_height_factor)
    525: ( (0, 0), 89, (
            (7, "x7", t1, 1),
            (7.5, "", t0, 1),
            (8, "x8", t1, 1),
            (8.5, "", t0, 1),
            (9, "x9", t1, 1),
            (9.5, "", t0, 1),
            (10, "x10", t3, 1),
            (11, "", t1, 1),
            (12, "x12", t1, 1),
            (13, "", t1, 1),
            (14, "", t1, 1),
            (15, "x15", t2, 1),
            (16, "", t1, 1),
            (17, "", t1, 1),
            (18, "", t1, 1),
            (19, "", t1, 1),
            (20, "x20", t3, 1),
            (21, "", t1, 1),
            (22, "", t1, 1),
            (23, "", t1, 1),
            (24, "", t1, 1),
            (25, "x25", t2, 1),
            (26, "", t1, 1),
            (27, "", t1, 1),
            (28, "", t1, 1),
            (29, "", t1, 1),
            (30, "x30", t3, 1),
            (31, "", t1, 1),
            (32, "", t1, 1),
            (33, "", t1, 1),
            (34, "", t1, 1),
            (35, "", t2, 1),
            (36, "", t1, 1),
            (37, "", t1, 1),
            (38, "", t1, 1),
            (39, "", t1, 1),
            (40, "x40", t3, 1),
            (45, "", t1, 1),
            (50, "x50", t3, 0.9),
            (60, "", t1, 1),
            (70, "", t1, 1),
            (80, "", t1, 1),
            (90, "", t1, 1),
            (100, "x100", t3, 1),
            (150, "", t2, 1),
            (200, "x200", t3, 0.7),
            (500, "x500", t3, 0.5))),
    550: ( (1, 0), 84, (
            (7, "x7", t1, 1),
            (7.5, "", t0, 1),
            (8, "x8", t1, 1),
            (8.5, "", t0, 1),
            (9, "x9", t1, 1),
            (9.5, "", t0, 1),
            (10, "x10", t3, 1),
            (11, "", t1, 1),
            (12, "x12", t1, 1),
            (13, "", t1, 1),
            (14, "", t1, 1),
            (15, "x15", t2, 1),
            (16, "", t1, 1),
            (17, "", t1, 1),
            (18, "", t1, 1),
            (19, "", t1, 1),
            (20, "x20", t3, 1),
            (21, "", t1, 1),
            (22, "", t1, 1),
            (23, "", t1, 1),
            (24, "", t1, 1),
            (25, "x25", t2, 1),
            (26, "", t1, 1),
            (27, "", t1, 1),
            (28, "", t1, 1),
            (29, "", t1, 1),
            (30, "x30", t3, 1),
            (31, "", t1, 1),
            (32, "", t1, 1),
            (33, "", t1, 1),
            (34, "", t1, 1),
            (35, "", t2, 1),
            (36, "", t1, 1),
            (37, "", t1, 1),
            (38, "", t1, 1),
            (39, "", t1, 1),
            (40, "x40", t3, 1),
            (45, "", t1, 1),
            (50, "x50", t3, 0.9),
            (60, "", t1, 1),
            (70, "", t1, 1),
            (80, "", t1, 1),
            (90, "", t1, 1),
            (100, "x100", t3, 1),
            (150, "", t2, 1),
            (200, "x200", t3, 0.7),
            (500, "x500", t3, 0.5))),
    575: ( (2, 0), 80, (
            (7.5, "7.5", t0, 1),
            (8, "x8", t1, 1),
            (8.5, "", t0, 1),
            (9, "x9", t1, 1),
            (9.5, "", t0, 1),
            (10, "x10", t3, 1),
            (11, "", t1, 1),
            (12, "x12", t1, 1),
            (13, "", t1, 1),
            (14, "", t1, 1),
            (15, "x15", t2, 1),
            (16, "", t1, 1),
            (17, "", t1, 1),
            (18, "", t1, 1),
            (19, "", t1, 1),
            (20, "x20", t3, 1),
            (21, "", t1, 1),
            (22, "", t1, 1),
            (23, "", t1, 1),
            (24, "", t1, 1),
            (25, "x25", t2, 1),
            (26, "", t1, 1),
            (27, "", t1, 1),
            (28, "", t1, 1),
            (29, "", t1, 1),
            (30, "x30", t3, 1),
            (31, "", t1, 1),
            (32, "", t1, 1),
            (33, "", t1, 1),
            (34, "", t1, 1),
            (35, "", t2, 1),
            (36, "", t1, 1),
            (37, "", t1, 1),
            (38, "", t1, 1),
            (39, "", t1, 1),
            (40, "x40", t3, 1),
            (45, "", t1, 1),
            (50, "x50", t3, 0.9),
            (60, "", t1, 1),
            (70, "", t1, 1),
            (80, "", t1, 1),
            (90, "", t1, 1),
            (100, "x100", t3, 1),
            (150, "", t2, 1),
            (200, "x200", t3, 0.7),
            (500, "x500", t3, 0.5))),
    600: ( (3, 0), 77, (
            (8, "x8", t1, 1),
            (8.5, "", t0, 1),
            (9, "x9", t1, 1),
            (9.5, "", t0, 1),
            (10, "x10", t3, 1),
            (11, "", t1, 1),
            (12, "x12", t1, 1),
            (13, "", t1, 1),
            (14, "", t1, 1),
            (15, "x15", t2, 1),
            (16, "", t1, 1),
            (17, "", t1, 1),
            (18, "", t1, 1),
            (19, "", t1, 1),
            (20, "x20", t3, 1),
            (21, "", t1, 1),
            (22, "", t1, 1),
            (23, "", t1, 1),
            (24, "", t1, 1),
            (25, "x25", t2, 1),
            (26, "", t1, 1),
            (27, "", t1, 1),
            (28, "", t1, 1),
            (29, "", t1, 1),
            (30, "x30", t3, 1),
            (31, "", t1, 1),
            (32, "", t1, 1),
            (33, "", t1, 1),
            (34, "", t1, 1),
            (35, "", t2, 1),
            (36, "", t1, 1),
            (37, "", t1, 1),
            (38, "", t1, 1),
            (39, "", t1, 1),
            (40, "x40", t3, 1),
            (45, "", t1, 1),
            (50, "x50", t3, 0.9),
            (60, "", t1, 1),
            (70, "", t1, 1),
            (80, "", t1, 1),
            (90, "", t1, 1),
            (100, "x100", t3, 1),
            (150, "", t2, 1),
            (200, "x200", t3, 0.7),
            (500, "x500", t3, 0.5))),
    625: ( (4, 0), 74, (
            (8, "x8", t1, 1),
            (8.5, "", t0, 1),
            (9, "x9", t1, 1),
            (9.5, "", t0, 1),
            (10, "x10", t3, 1),
            (11, "", t1, 1),
            (12, "x12", t1, 1),
            (13, "", t1, 1),
            (14, "", t1, 1),
            (15, "x15", t2, 1),
            (16, "", t1, 1),
            (17, "", t1, 1),
            (18, "", t1, 1),
            (19, "", t1, 1),
            (20, "x20", t3, 1),
            (21, "", t1, 1),
            (22, "", t1, 1),
            (23, "", t1, 1),
            (24, "", t1, 1),
            (25, "x25", t2, 1),
            (26, "", t1, 1),
            (27, "", t1, 1),
            (28, "", t1, 1),
            (29, "", t1, 1),
            (30, "x30", t3, 1),
            (31, "", t1, 1),
            (32, "", t1, 1),
            (33, "", t1, 1),
            (34, "", t1, 1),
            (35, "", t2, 1),
            (36, "", t1, 1),
            (37, "", t1, 1),
            (38, "", t1, 1),
            (39, "", t1, 1),
            (40, "x40", t3, 1),
            (45, "", t1, 1),
            (50, "x50", t3, 0.9),
            (60, "", t1, 1),
            (70, "", t1, 1),
            (80, "", t1, 1),
            (90, "", t1, 1),
            (100, "x100", t3, 1),
            (150, "", t2, 1),
            (200, "x200", t3, 0.7),
            (500, "x500", t3, 0.5))),
    650: ( (0, 1), 72, (
            (8.5, "8.5", t0, 1),
            (9, "x9", t1, 1),
            (9.5, "", t0, 1),
            (10, "x10", t3, 1),
            (11, "", t1, 1),
            (12, "x12", t1, 1),
            (13, "", t1, 1),
            (14, "", t1, 1),
            (15, "x15", t2, 1),
            (16, "", t1, 1),
            (17, "", t1, 1),
            (18, "", t1, 1),
            (19, "", t1, 1),
            (20, "x20", t3, 1),
            (21, "", t1, 1),
            (22, "", t1, 1),
            (23, "", t1, 1),
            (24, "", t1, 1),
            (25, "x25", t2, 1),
            (26, "", t1, 1),
            (27, "", t1, 1),
            (28, "", t1, 1),
            (29, "", t1, 1),
            (30, "x30", t3, 1),
            (31, "", t1, 1),
            (32, "", t1, 1),
            (33, "", t1, 1),
            (34, "", t1, 1),
            (35, "", t2, 1),
            (36, "", t1, 1),
            (37, "", t1, 1),
            (38, "", t1, 1),
            (39, "", t1, 1),
            (40, "x40", t3, 1),
            (45, "", t1, 1),
            (50, "x50", t3, 1),
            (60, "", t1, 1),
            (70, "", t1, 1),
            (80, "", t1, 1),
            (90, "", t1, 1),
            (100, "x100", t3, 1),
            (150, "", t2, 1),
            (200, "x200", t3, 0.8),
            (500, "x500", t3, 0.6))),
    675: ( (1, 1), 68, (
            (9, "x9", t1, 1),
            (9.5, "", t0, 1),
            (10, "x10", t3, 1),
            (11, "", t1, 1),
            (12, "x12", t1, 1),
            (13, "", t1, 1),
            (14, "", t1, 1),
            (15, "x15", t2, 1),
            (16, "", t1, 1),
            (17, "", t1, 1),
            (18, "", t1, 1),
            (19, "", t1, 1),
            (20, "x20", t3, 1),
            (21, "", t1, 1),
            (22, "", t1, 1),
            (23, "", t1, 1),
            (24, "", t1, 1),
            (25, "x25", t2, 1),
            (26, "", t1, 1),
            (27, "", t1, 1),
            (28, "", t1, 1),
            (29, "", t1, 1),
            (30, "x30", t3, 1),
            (31, "", t1, 1),
            (32, "", t1, 1),
            (33, "", t1, 1),
            (34, "", t1, 1),
            (35, "", t2, 1),
            (36, "", t1, 1),
            (37, "", t1, 1),
            (38, "", t1, 1),
            (39, "", t1, 1),
            (40, "x40", t3, 1),
            (45, "", t1, 1),
            (50, "x50", t3, 0.9),
            (60, "", t1, 1),
            (70, "", t1, 1),
            (80, "", t1, 1),
            (90, "", t1, 1),
            (100, "x100", t3, 1),
            (150, "", t2, 1),
            (200, "x200", t3, 0.7),
            (500, "x500", t3, 0.5))),
    700: ( (2, 1), 66, (
            (9, "x9", t1, 1),
            (9.5, "", t0, 1),
            (10, "x10", t3, 1),
            (11, "", t1, 1),
            (12, "x12", t1, 1),
            (13, "", t1, 1),
            (14, "", t1, 1),
            (15, "x15", t2, 1),
            (16, "", t1, 1),
            (17, "", t1, 1),
            (18, "", t1, 1),
            (19, "", t1, 1),
            (20, "x20", t3, 1),
            (21, "", t1, 1),
            (22, "", t1, 1),
            (23, "", t1, 1),
            (24, "", t1, 1),
            (25, "x25", t2, 1),
            (26, "", t1, 1),
            (27, "", t1, 1),
            (28, "", t1, 1),
            (29, "", t1, 1),
            (30, "x30", t3, 1),
            (31, "", t1, 1),
            (32, "", t1, 1),
            (33, "", t1, 1),
            (34, "", t1, 1),
            (35, "", t2, 1),
            (36, "", t1, 1),
            (37, "", t1, 1),
            (38, "", t1, 1),
            (39, "", t1, 1),
            (40, "x40", t3, 1),
            (45, "", t1, 1),
            (50, "x50", t3, 0.9),
            (60, "", t1, 1),
            (70, "", t1, 1),
            (80, "", t1, 1),
            (90, "", t1, 1),
            (100, "x100", t3, 1),
            (150, "", t2, 1),
            (200, "x200", t3, 0.7),
            (500, "x500", t3, 0.5))),
    725: ( (3, 1), 64, (
            (10, "x10", t3, 1),
            (11, "", t1, 1),
            (12, "x12", t1, 1),
            (13, "", t1, 1),
            (14, "", t1, 1),
            (15, "x15", t2, 1),
            (16, "", t1, 1),
            (17, "", t1, 1),
            (18, "", t1, 1),
            (19, "", t1, 1),
            (20, "x20", t3, 1),
            (21, "", t1, 1),
            (22, "", t1, 1),
            (23, "", t1, 1),
            (24, "", t1, 1),
            (25, "x25", t2, 1),
            (26, "", t1, 1),
            (27, "", t1, 1),
            (28, "", t1, 1),
            (29, "", t1, 1),
            (30, "x30", t3, 1),
            (31, "", t1, 1),
            (32, "", t1, 1),
            (33, "", t1, 1),
            (34, "", t1, 1),
            (35, "", t2, 1),
            (36, "", t1, 1),
            (37, "", t1, 1),
            (38, "", t1, 1),
            (39, "", t1, 1),
            (40, "x40", t3, 1),
            (45, "", t1, 1),
            (50, "x50", t3, 0.9),
            (60, "", t1, 1),
            (70, "", t1, 1),
            (80, "", t1, 1),
            (90, "", t1, 1),
            (100, "x100", t3, 1),
            (150, "", t2, 1),
            (200, "x200", t3, 0.7),
            (500, "x500", t3, 0.5))),
    750: ( (4, 1), 61, (
            (10, "x10", t3, 1),
            (11, "", t1, 1),
            (12, "x12", t1, 1),
            (13, "", t1, 1),
            (14, "", t1, 1),
            (15, "x15", t2, 1),
            (16, "", t1, 1),
            (17, "", t1, 1),
            (18, "", t1, 1),
            (19, "", t1, 1),
            (20, "x20", t3, 1),
            (21, "", t1, 1),
            (22, "", t1, 1),
            (23, "", t1, 1),
            (24, "", t1, 1),
            (25, "x25", t2, 1),
            (26, "", t1, 1),
            (27, "", t1, 1),
            (28, "", t1, 1),
            (29, "", t1, 1),
            (30, "x30", t3, 1),
            (31, "", t1, 1),
            (32, "", t1, 1),
            (33, "", t1, 1),
            (34, "", t1, 1),
            (35, "", t2, 1),
            (36, "", t1, 1),
            (37, "", t1, 1),
            (38, "", t1, 1),
            (39, "", t1, 1),
            (40, "x40", t3, 1),
            (45, "", t1, 1),
            (50, "x50", t3, 0.9),
            (60, "", t1, 1),
            (70, "", t1, 1),
            (80, "", t1, 1),
            (90, "", t1, 1),
            (100, "x100", t3, 1),
            (150, "", t2, 1),
            (200, "x200", t3, 0.7),
            (500, "x500", t3, 0.5))),
}
def SetUp(file, orientation=landscape, units=inches):
    '''Convenience function to set up the drawing environment and return a
    file object to the output stream.
    '''
    ofp = open(file, "w")
    ginitialize(ofp)
    setOrientation(orientation, units)
    return ofp
def CardLabel(width, height, eye_distance_mm, text_height):
    push()
    translate(width/2, height/2)
    rotate(-90)
    ctext(f"{eye_distance_mm} mm eye-to-card distance")
    pop()
def DegreeScale(tenth_degrees, eye_distance_mm, text_height):
    push()
    d = float(eye_distance_mm)*mm2in
    y0 = 0.08
    dx = 0.25
    translate(0, y0)
    move(0, 0)
    for theta in range(tenth_degrees + 1):
        y = 2*d*tan(theta/(10*2)*d2r)
        move(0, y)
        label = False
        if theta % 10 == 0:
            tick = dx
            label = True
        elif theta and theta % 5 == 0:
            tick = dx/1.25
        else:
            tick = dx/3
        rline(tick, 0)
        if label:
            move(dx*1.1, y - text_height/3.5)
            text("%d deg" % (theta/10))
    pop()
def TimesScale(marks, eye_distance_mm, text_height):
    '''marks is a list of tick marks:
        (factor, label_string, tick_lengths)
    where factor is a number, label_string is what to label the tick with,
    and tick_lengths is how many lengths to make the tick.
    
    Math:  1/factor is the ratio of the height to the distance.  Thus, the
    y distance plotted should be in the same ratio to the eye distance.
    '''
    push()
    d = float(eye_distance_mm)*mm2in
    y0 = 0.15
    dx = 0.1
    translate(0, y0)
    move(0, 0)
    rline(5*dx, 0)
    move(5*dx*1.05, -text_height/3.5)
    text("Ref")
    for factor, label, tick_length, text_height_factor in marks:
        y = d/factor
        move(0, y)
        x = tick_length*dx
        rline(x, 0)
        if label:
            move(2.5*dx, y - text_height/3.5)
            textSize(text_height*text_height_factor)
            text(label)
    pop()
def Card(x, y, marks, eye_distance_mm, width, height, tenth_degrees):
    push()
    translate(x*width, y*height)
    text_height = 0.14
    textSize(text_height)
    textName(SansBold)
    move(0, 0)
    rectangle(width, height)
    CardLabel(width, height, eye_distance_mm, text_height)
    DegreeScale(tenth_degrees, eye_distance_mm, text_height)
    translate(width, height)
    rotate(180)
    TimesScale(marks, eye_distance_mm, text_height)
    pop()
def Label():
    # Expect to be at (1, 1) in landscape
    push()
    translate(9.00, 6.5)
    rotate(-90)
    text_height = 0.14
    text_height = 0.14
    textSize(text_height)
    move(0, 0)
    text("https://github.com/someonesdad1/plib/lib/g/demofiles/bus_card_angle_measure.py")
    move(0, -text_height)
    text("My eye-to-card distance is 650 mm")
    pop()

if __name__ == "__main__":
    f = SetUp("out/bus_card_angle_measure.ps")
    translate(1, 1)
    if debug:
        scale(2, 2)
    width = 1.75
    height = 3.32
    for eye_dist_mm in mark_dict:
        d = mark_dict[eye_dist_mm]
        x, y = d[0]
        tenth_degrees, marks = d[1:]
        Card(x, y, marks, eye_dist_mm, width, height, tenth_degrees)
    Label()
