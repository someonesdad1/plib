'''
Plots slide-rule type scales

    Other scales to consider:
        Cutting speed for 100 sfpm vs diameter
        Weights of bar stock
        Melting points
        Boiling points
        Normal distribution CDF
        Tap drills
        Time value of money
        10, 20, 40, 50 engineering scales
        Architectural scales
        Metric scales
        Map scales

    P scale is sqrt(1-x*x) from 0.1 to 1.  The apparent reason for its
    existence is to allow calculation of cosines for angles near 90
    degrees.

    Some scale nomenclature from
    http://dspace.dial.pipex.com/town/square/gd86/slidlist.shtml

        (Pickett rules)
        LL0+ exp(0.001*x) (Faber LL0)
        LL0- exp(-0.001*x) (Faber LL00)
        LL1+ exp(0.01*x)
        LL1- exp(-0.01*x)
        LL2+ exp(0.1*x)
        LL2- exp(-0.1*x)
        LL3+ exp(x)
        LL3- exp(-x)

    Algorithm for placing points:

        Let x0 and x1 be the endpoints of the 1 decade log scale.
        Let y = f(x) be the function being plotted.
        Let x = F(y) be the inverse function of f.

        Give a set of y's that we want to place:  [yi; 1 <= i <= n]
        To place yi:

            xi = F(yi)
            Then plot at the x location give by

                log(xi) + alpha

            where alpha is an integer such that

                0 <= log(xi) + alpha <= 1
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Plot slide-rule type scales
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import string
    import sys
    import re
    import math
    import time
    if 0:
        from math import *
    else:
        import math
if 1:   # Custom imports
    from g import *
    from wrap import dedent
if 1:   # Global variables
    debug = 0
    wrap_in_PJL = 0
    in_color = 0
    d2r = math.pi/180
    # The following is needed to work in python 3
    def MP(x, y):
        return list(map(x, y))
    # For applying a number to a scale on the RHS
    scale_count = 1
    scale_count_offset_x = 0.15
    scale_count_offset_y = -0.05
    # Font sizes are all relative to the base font size
    base_font_size = 8/72.27
    footer_font_size = 0.75
    title_font_size = 1
    exponent_font = 0.8
    line_width = 0.005
    tick_length = 0.1
    line_label_offset = 0.25
    base_font = Sans
    base_font_bold = SansBold
    # Whether we should print the slide rule scale name to the right
    print_slide_rule_scale = 0
    slide_rule_scale_x_offset = 1.0  # Fraction of base font size
    slide_rule_scale_y_offset = 0.4  # Fraction of base font size
    if in_color:
        page_background_color = black
        table_background_color = black
        title_color = red
        entry_color = white
        bounding_box_color = blue
        bounding_box_thickness = 0.02
        table_line_thickness = 0.005
        line_color = white
        grid_color = cyan
        major_tick_color = red
        medium_tick_color = magenta
        minor_tick_color = white
        number_color = white
        footer_color = white
    else:
        page_background_color = white
        table_background_color = white
        title_color = black
        entry_color = black
        bounding_box_color = black
        bounding_box_thickness = 0.02
        table_line_thickness = 0.005
        line_color = black
        grid_color = black
        major_tick_color = black
        medium_tick_color = black
        minor_tick_color = black
        number_color = black
        footer_color = black
    # The following global is used to correct a base 10 log to the interval
    # [0, 1].
    log_correction = 0
    tap_drills = (
        ("2-56", 0.067),
        ("3-48", 0.076),
        ("4-40", 0.086),
        ("6-32", 0.107),
        ("8-32", 0.129),
        ("10-24", 0.150),
        ("10-32", 0.159),
        ("12-24", 0.173),
        ("1/4-20", 0.201),
        ("1/4-28", 0.213),
        ("5/16-18", 0.257),
        ("3/8-16", 0.313),
        ("7/16-14", 0.368),
        ("1/2-13", 0.425),
        ("5/8-11", 0.531),
        ("3/4-10", 0.656),
        ("7/8-9", 0.766),
        ("1-8", 0.875))
def Range(a, b=None, c=None):
    'Needed to work under python 3'
    if b is None and c is None:
        return list(range(a))
    elif b is not None and c is None:
        return list(range(a, b, 1))
    else:
        return list(range(a, b, c))
def CorrectedLog10(x):
    if x <= 0:
        print("%.3f is < 0; can't take log" % x)
        sys.exit(1)
    y = math.log10(x)
    if log_correction:
        if y < 0:
            y += log_correction
        if y > 1:
            y -= log_correction
    else:
        while y < 0:
            y += 1
        while y > 1:
            y -= 1
    assert(0 <= y <= 1)
    return y
def Identity(x):
    return x
def NumberScale(x, y):
    '''Apply a number to the right of the scale.
    '''
    global scale_count
    push()
    textSize(1.5*base_font_size)
    textName(base_font_bold)
    move(x + scale_count_offset_x, y + scale_count_offset_y)
    ctext(repr(scale_count))
    pop()
    scale_count += 1
def Distance(x0, y0, x1, y1):
    x = x0 - x1
    y = y0 - y1
    return math.sqrt(x*x + y*y)
def Angle(x0, y0, x1, y1):
    '''Return the angle in degrees.
    '''
    return math.atan2(y1 - y0, x1 - x0)/d2r
def Trim0(s):
    '''Remove any trailing 0's from a string (including the decimal
    point if appropriate).
    '''
    while s[-1] == "0":
        s = s[:-1]
    if s[-1] == ".":
        s = s[:-1]
    return s
def DefaultSettings(index_function=None):
    return {
        "line_width": line_width,
        "font1_size": base_font_size,
        "tick1_length": tick_length,
        "index_function": index_function,
    }
def Dump(sequence, n=3):
    fmt = "%%.%df" % n
    print(map(lambda x: fmt % x, sequence))
def lngamma(xin):
    '''Routine to calculate the logarithm of the gamma function.
    Translated from C.  See page 160 of "Numerical Recipes".  This is
    Lanczos' remarkable formula.  |error| < 2E-10 everywhere Re x > 0.
    '''
    stp = 2.50662827465
    x = xin - 1
    tmp = x + 5.5
    tmp = (x + 0.5)*math.log(tmp) - tmp
    ser = (1 + 76.18009173/(x + 1) -
           86.50532033/(x + 2) +
           24.01409822/(x + 3) -
           1.231739516/(x + 4) +
           0.120858003e-2/(x + 5) -
           0.536382e-5/(x + 6))
    return tmp + math.log(stp*ser)
def loggamma(xin):
    return lngamma(xin)/math.log(10)
def DrawEandPi(x0, y0, x1, y1, s, right):
    '''Used to put e and pi on a log scale.  s is a settings dictionary
    and right is true of the labels and ticks are on the right of the
    line looking from (x0, y0) to (x1, y1).
    '''
    font_height = s.s["font1_size"] * s.s["font2_size"]
    tick4_length = s.s["tick4_length"] * s.s["tick1_length"]
    y_offset = tick4_length/1.5
    y = tick4_length * 1.1
    reverse = 1
    if right:
        reverse = -1
    # Put e on the scale
    push()
    translate(x0, y0)
    rotate(Angle(x0, y0, x1, y1))
    x = math.log10(math.exp(1)) * Distance(x0, y0, x1, y1)
    line(x, y*reverse, x, (y + y_offset) * reverse)
    Y = y + y_offset*1.1
    if right:
        Y = y + y_offset*2.7
    move(x, Y*reverse)
    textSize(font_height)
    ctext("e")
    pop()
    # Put pi on the scale
    push()
    translate(x0, y0)
    rotate(Angle(x0, y0, x1, y1))
    x = math.log10(math.pi) * Distance(x0, y0, x1, y1)
    y = tick4_length * 1.1
    line(x, y*reverse, x, (y + y_offset) * reverse)
    Y = y + y_offset*1.1
    if right:
        Y = y + y_offset*2.7
    x_offset = font_height/4
    move(x - x_offset, Y*reverse)
    textSize(font_height)
    stext("\\70")
    pop()
class Scale:
    def __init__(self, x0, y0, x1, y1, settings={}):
        '''Draw a scale from point (x0, y0) to (x1, y1).  The dictionary
        settings contains all of the adjustable parameters of a scale.
        Most settings have default values, but a few will cause an
        exception if the user doesn't set them.
        '''
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        # Set the default settings.
        self.s = {}
        self.s["label_angle"] = 0
        self.s["label_color"] = None
        self.s["label_right"] = 0
        self.s["label_height_above_tick"] = 0
        self.s["tick_right"] = 0
        self.s["line_width"] = None
        self.s["line_color"] = None
        self.s["draw_line"] = 1
        self.s["omit_first_label"] = 0
        self.s["omit_last_label"] = 0
        self.s["index_function"] = None
        # Containers that describe labels and ticks to draw.  A
        # labelled container is a sequence of two sequences.  The
        # first is the values where a label/tick is and the second is
        # the string name of the label.  The two sequences must be the
        # same size.  An unlabelled container is just a sequence of
        # values to put ticks at.
        self.N = 6  # Number of containers for labels and ticks
        for n in range(1, self.N+1):
            self.s["labelled%d" % n] = None
            self.s["unlabelled%d" % n] = None
            self.s["label%d_x" % n] = 0
            self.s["label%d_y" % n] = 0
            self.s["font%d_color" % n] = None
            self.s["tick%d_color" % n] = None
            self.s["tick%d_width" % n] = None
            self.s["tick%d_line_type" % n] = None
            self.s["tick%d_start_offset" % n] = 0
        # We'll set default Font sizes
        self.s["font1_size"] = None   # User must pass in
        self.s["font2_size"] = 0.8    # All are relative to font1
        self.s["font3_size"] = 0.6
        self.s["font4_size"] = 0.5
        self.s["font5_size"] = 0.4
        self.s["font6_size"] = 0.3
        # Tick data
        self.s["tick1_length"] = None   # User must pass in
        self.s["tick2_length"] = 0.9    # All are relative to tick1 length
        self.s["tick3_length"] = 0.8
        self.s["tick4_length"] = 0.6
        self.s["tick5_length"] = 0.45
        self.s["tick6_length"] = 0.35
        # Now add settings the user passed in
        self.Settings(settings)
        # Make sure we have needed settings
        if not self.s["font1_size"]:
            raise "Need 'font1_size' setting"
        if not self.s["tick1_length"]:
            raise "Need 'tick1_length' setting"
        if not self.s["index_function"]:
            raise "Need 'index_function' setting"
        # Check labelled containers for proper form
        for num in range(1, 6):
            try:
                container = self.s["labelled%s" % num]
                if not container:
                    continue
                if len(container[0]) != len(container[1]):
                    raise ""
            except Exception:
                    raise "Labelled container %d improper" % num
        # Get length and angle
        self.length = Distance(self.x0, self.y0, self.x1, self.y1)
        self.angle_degrees = Angle(self.x0, self.y0, self.x1, self.y1)
    def Settings(self, settings):
        if debug:
            print("Settings:")
            keys = settings.keys()
            keys.sort()
            for key in keys:
                print("  %-20s : %s" % (key, settings[key]))
            print("-"*70)
        for key in settings:
            if key in self.s:
                self.s[key] = settings[key]
            else:
                raise "'" + key + "' key not in settings"
    def DrawTick(self, number):
        values = []
        l = "labelled%d" % number
        if self.s[l]:
            values += self.s[l][0]
        if self.s["un" + l]:
            values += self.s["un" + l]
        if len(values) == 0:
            return
        t = "tick%d" % number
        push()
        tick_right = 1
        if self.s["tick_right"]:
            tick_right = -1
        if self.s[t + "_color"]:
            lineColor(self.s[t + "_color"])
        if self.s[t + "_width"]:
            lineColor(self.s[t + "_width"])
        if self.s[t + "_line_type"]:
            lineType(self.s[t + "_line_type"])
        tick_length = self.s["tick1_length"]
        if number != 1:
            tick_length *= self.s[t + "_length"]
        for value in values:
            x = self.s["index_function"](value) * self.length
            y = self.s[t + "_start_offset"]
            line(x, y, x, tick_right*(y + tick_length))
            if debug:
                print("Tick at (%g, %g), len = %g" % (x, y, tick_length))
        pop()
    def DrawLabel(self, number):
        container = self.s["labelled%d" % number]
        if not container:
            return
        f = "font%d" % number
        t = "tick%d" % number
        l = "label%d" % number
        push()
        tick_length = self.s["tick1_length"]
        if number != 1:
            tick_length *= self.s[t + "_length"]
            font_height = self.s[f + "_size"] * self.s["font1_size"]
        else:
            font_height = self.s["font1_size"]
        textSize(font_height)
        tick_right = 1
        label_right = 1
        if self.s["tick_right"]:
            tick_right = -1
        if self.s["label_right"]:
            label_right = -1
        for ix in range(len(container[0])):
            value = container[0][ix]
            label = container[1][ix]
            push()
            x = self.s["index_function"](value) * self.length
            y = self.s[t + "_start_offset"] + tick_length
            if tick_right == -1:
                # The 1/4 is a phenomenological correction to get the
                # label a default pleasing distance from the tick
                # mark.
                y += tick_length - 1/4*font_height
            y *= tick_right
            translate(x, y)
            rotate(self.s["label_angle"])
            x = self.s[l + "_x"]
            y = self.s[l + "_y"] + font_height/10
            y *= label_right
            move(x, y)
            ctext(label)
            pop()
        pop()
    def Draw(self):
        push()
        translate(self.x0, self.y0)
        rotate(self.angle_degrees)
        if self.s["draw_line"]:
            if self.s["line_color"]:
                lineColor(self.s["line_color"])
            if self.s["line_width"]:
                lineWidth(self.s["line_width"])
            line(0, 0, self.length, 0)
        # Draw in reverse ordering to numbering so that major ticks
        # are on top of minor ticks.
        for ix in range(self.N, 0, -1):
            self.DrawTick(ix)
        for ix in range(self.N, 0, -1):
            self.DrawLabel(ix)
        pop()
def SetUp(file, orientation=portrait, units=inches):
    '''Convenience function to set up the drawing environment and return a
    file object to the output stream.
    '''
    ofp = open(file, "w")
    ginitialize(ofp, wrap_in_PJL)
    setOrientation(orientation, units)
    return ofp
def nFmt(scale, n=0):
    '''Returns a format string based on scale.  If scale is
    greater than 1 and n is 0, then all we need is integer
    formatting.  If scale is < 1 or n > 0, then we want real
    formatting.  Example:  scale = 1/10:  if n == 0, then we're
    interested in the level 1 labels, so we'd get fmt = "%.1f".
    If n == 2, then we want level 2 labels, so we'd get "%.2f".
    '''
    if scale > 1:
        return "%d"
    return "%%.%df" % int(-math.log10(scale) + n)
def Log10inch(x0, y0, x1, y1, scale=1, omit_first=0, omit_last=0,
              right=0, settings=None):
    '''The scale goes from (x0, y0) to (x1, y1).  When scale is 1,
    then the scale goes from 1 to 10.  Use 1/10 to have the scale go
    from 0.1 to 1, etc.  Use the omit variables to omit the first and
    last labels, which is used for making joined log scales.  If right
    is true, the labels and ticks go on the right of the line, looking
    from (x0, y0) to (x1, y1).
    '''
    # The Log10inch function is used to construct a log scale about 10
    # inches long.  Write another function if the length is to be much
    # different than 10 inches, as the minor and tertiary tick marks will
    # probably need to be adjusted.
    push()
    if not settings:
        settings = DefaultSettings(math.log10)
    if right:
        settings["label_right"] = 1
        settings["tick_right"] = 1
    # Level 1 tick marks and labels
    n = 1
    m = 11
    if omit_first:
        n = 2
    if omit_last:
        m = 10
    values = Range(n, m)
    tmp = MP(lambda x: x*scale, values)
    strings = MP(lambda x: nFmt(scale) % x, tmp)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    values = MP(lambda x: x/10, Range(15, 96, 10))
    tmp = MP(lambda x: x*scale, values)
    strings = MP(lambda x: nFmt(scale, 1) % x, tmp)
    settings["labelled2"] = [values, strings]
    # Level 3 tick marks and labels
    values = MP(lambda x: x/10, Range(11, 30))
    tmp = MP(lambda x: x*scale, values)
    strings = MP(lambda x: nFmt(scale, 1) % x, tmp)
    for i in [4, 8, 12]:
        del values[i]
        del strings[i]
    if scale == 1:
        del values[13]
        del strings[13]
    settings["labelled3"] = [values, strings]
    values = MP(lambda x: x/10, Range(31, 100))
    settings["unlabelled3"] = values + [2.7]
    if scale == 1:
        settings["unlabelled3"] += [2.7]
    # Level 4 tick marks
    values = MP(lambda x: x/100, Range(202, 500, 2))
    values += MP(lambda x: x/100, Range(100, 200, 5))
    settings["unlabelled4"] = values
    # Level 5 tick marks
    values = MP(lambda x: x/100, Range(101, 200))
    settings["unlabelled5"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    if scale == 1:
        DrawEandPi(x0, y0, x1, y1, s, right)
    pop()
def Log10inchBack(x0, y0, x1, y1, scale=1, omit_first=0, omit_last=0,
                  right=0, settings=None):
    '''The scale goes from (x0, y0) to (x1, y1).  When scale is 1,
    then the scale goes from 1 to 10.  Use 1/10 to have the scale go
    from 0.1 to 1, etc.  Use the omit variables to omit the first and
    last labels, which is used for making joined log scales.  If right
    is true, the labels and ticks go on the right of the line, looking
    from (x0, y0) to (x1, y1).
 
    Same as Log10Inch, but is intended to go from right to left.
    '''
    # Note:  this is definitely code duplication between the above and
    # below function.  It is ultimately caused by not being able to find
    # what the font sizes are.  If there were a way to get font metrics,
    # this problem could be fixed.
    push()
    if not settings:
        settings = DefaultSettings(math.log10)
    if right:
        settings["label_right"] = 1
        settings["tick_right"] = 1
    else:
        settings["label_angle"] = 180
        settings["label1_y"] = -0.1
        settings["label2_y"] = -0.095
        settings["label3_y"] = -0.075
    # Level 1 tick marks and labels
    n = 1
    m = 11
    if omit_first:
        n = 2
    if omit_last:
        m = 10
    values = Range(n, m)
    tmp = MP(lambda x: x*scale, values)
    strings = MP(lambda x: nFmt(scale) % x, tmp)
    if scale <= 1:
        strings = MP(Trim0, strings)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    values = MP(lambda x: x/10, Range(15, 96, 10))
    tmp = MP(lambda x: x*scale, values)
    strings = MP(lambda x: nFmt(scale, 1) % x, tmp)
    settings["labelled2"] = [values, strings]
    # Level 3 tick marks and labels
    values = MP(lambda x: x/10, Range(11, 30))
    tmp = MP(lambda x: x*scale, values)
    strings = MP(lambda x: nFmt(scale, 1) % x, tmp)
    for i in [4, 8, 12]:
        del values[i]
        del strings[i]
    if scale == 1:
        del values[13]
        del strings[13]
    settings["labelled3"] = [values, strings]
    values = MP(lambda x: x/10, Range(31, 100))
    settings["unlabelled3"] = values + [2.7]
    if scale == 1:
        settings["unlabelled3"] += [2.7]
    # Level 4 tick marks
    values = MP(lambda x: x/100, Range(202, 500, 2))
    values += MP(lambda x: x/100, Range(100, 200, 5))
    settings["unlabelled4"] = values
    # Level 5 tick marks
    values = MP(lambda x: x/100, Range(101, 200))
    settings["unlabelled5"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
def Log5inch(x0, y0, x1, y1, scale=1, omit_first=0, omit_last=0,
             right=0, settings=None):
    '''The scale goes from (x0, y0) to (x1, y1).  When scale is 1,
    then the scale goes from 1 to 10.  Use 1/10 to have the scale go
    from 0.1 to 1, etc.  Use the omit variables to omit the first and
    last labels, which is used for making joined log scales.  If right
    is true, the labels and ticks go on the right of the line, looking
    from (x0, y0) to (x1, y1).
    '''
    push()
    if not settings:
        settings = DefaultSettings(math.log10)
    if right:
        settings["label_right"] = 1
        settings["tick_right"] = 1
    if right and not settings:
        settings["font2_size"] = 0.7
        settings["label2_y"] = -0.02
    # Level 1 tick marks and labels
    n = 1
    m = 11
    if omit_first:
        n = 2
    if omit_last:
        m = 10
    values = Range(n, m)
    tmp = MP(lambda x: x*scale, values)
    strings = MP(lambda x: nFmt(scale) % x, tmp)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    values = MP(lambda x: x/10, Range(15, 86, 10))
    tmp = MP(lambda x: x*scale, values)
    strings = MP(lambda x: nFmt(scale, 1) % x, tmp)
    settings["labelled2"] = [values, strings]
    settings["unlabelled2"] = [9.5]
    # Level 3 tick marks and labels
    values = MP(lambda x: x/10, Range(11, 20))
    tmp = MP(lambda x: x*scale, values)
    strings = MP(lambda x: nFmt(scale, 1) % x, tmp)
    del values[4]
    del strings[4]
    settings["labelled3"] = [values, strings]
    values = MP(lambda x: x/10, Range(21, 100))
    settings["unlabelled3"] = values
    # Level 4 tick marks
    values = MP(lambda x: x/100, Range(202, 400, 2))
    values += MP(lambda x: x/100, Range(100, 200, 5))
    settings["unlabelled4"] = values
    # Level 5 tick marks
    values = MP(lambda x: x/100, Range(101, 200))
    settings["unlabelled5"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    if scale == 1:
        DrawEandPi(x0, y0, x1, y1, s, right)
    pop()
def Log3inch(x0, y0, x1, y1, scale=1, omit_first=0, omit_last=0,
             right=0, settings=None):
    push()
    if not settings:
        settings = DefaultSettings(math.log10)
    if right:
        settings["label_right"] = 1
        settings["tick_right"] = 1
        settings["font1_size"] = 0.08
        settings["font2_size"] = 0.7
        settings["label2_y"] = -0.02
    # Level 1 tick marks and labels
    n = 1
    m = 11
    if omit_first:
        n = 2
    if omit_last:
        m = 10
    values = Range(n, m)
    tmp = MP(lambda x: x*scale, values)
    strings = MP(lambda x: nFmt(scale) % x, tmp)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    if scale >= 100:
        values = MP(lambda x: x/10, Range(15, 76, 10))
        settings["unlabelled2"] = [8.5, 9.5]
    else:
        values = MP(lambda x: x/10, Range(15, 96, 10))
    tmp = MP(lambda x: x*scale, values)
    strings = MP(lambda x: nFmt(scale, 1) % x, tmp)
    settings["labelled2"] = [values, strings]
    # Level 3 tick marks and labels
    values = MP(lambda x: x/10, Range(11, 20))
    tmp = MP(lambda x: x*scale, values)
    strings = MP(lambda x: nFmt(scale, 1) % x, tmp)
    del values[4]
    del strings[4]
    settings["labelled3"] = [values, strings]
    values = MP(lambda x: x/10, Range(21, 100))
    settings["unlabelled3"] = values
    # Level 4 tick marks
    values = MP(lambda x: x/100, Range(102, 200, 2))
    values += MP(lambda x: x/100, Range(200, 300, 5))
    settings["unlabelled4"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    if scale == 1:
        DrawEandPi(x0, y0, x1, y1, s, right)
    pop()
def Sin10inch(x0, y0, x1, y1, right=0, settings=None):
    push()
    if not settings:
        settings = DefaultSettings(math.log10)
    if right:
        settings["label_right"] = 1
        settings["tick_right"] = 1
        #settings["label2_y"] = -0.02
        settings["index_function"] = CorrectedLog10
    # Level 1 tick marks and labels
    tmp = Range(6, 30)
    tmp += Range(30, 90, 10)
    del tmp[29]     # Delete the 80
    strings = MP(lambda x: "%d" % x, tmp)
    strings += ["90"]
    tmp += [90 - 1e-6]
    values = MP(lambda x: math.sin(x*d2r), tmp)
    settings["labelled1"] = [values, strings]
    settings["unlabelled1"] = [math.sin(80*d2r)]
    # Level 2 tick marks and labels
    tmp1 = Range(35, 76, 10)
    strings = MP(lambda x: "%d" % x, tmp1)
    values = MP(lambda x: math.sin(x*d2r), tmp1)
    settings["labelled2"] = [values, strings]
    tmp = MP(lambda x: math.sin(x/10*d2r), Range(65, 300, 5))
    tmp += [math.sin(85*d2r)]
    settings["unlabelled2"] = tmp
    # Level 3 tick marks and labels
    tmp = Range(57, 200)
    tmp += Range(300, 800, 10)
    values = MP(lambda x: math.sin(x/10*d2r), tmp)
    settings["unlabelled3"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
def SinTan10inch(x0, y0, x1, y1, right=0, settings=None):
    push()
    if not settings:
        settings = DefaultSettings(math.log10)
    if right:
        settings["label_right"] = 1
        settings["tick_right"] = 1
        settings["index_function"] = CorrectedLog10
        settings["tick4_length"] = 0.5
    # Level 1 tick marks and labels
    tmp = Range(1, 6)
    strings = MP(lambda x: "%d" % (x), tmp)
    values = MP(lambda x: math.sin(x*d2r), tmp)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    tmp = Range(6, 10) + Range(11, 20) + Range(21, 30) + [35, 45, 55]
    strings = MP(lambda x: "%.1f" % (x/10), tmp)
    values = MP(lambda x: math.sin(x/10*d2r), tmp)
    settings["labelled2"] = [values, strings]
    settings["unlabelled2"] = MP(lambda x: math.sin(x/100*d2r), tmp)
    # Level 3 tick marks and labels
    tmp = Range(65, 300, 5) + Range(300, 571, 10)
    values = MP(lambda x: math.sin(x/100*d2r), tmp)
    settings["unlabelled3"] = values
    # Level 4 tick marks and labels
    tmp = Range(58, 300)
    values = MP(lambda x: math.sin(x/100*d2r), tmp)
    settings["unlabelled4"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
def Tan1_10inch(x0, y0, x1, y1, right=0, settings=None):
    push()
    if not settings:
        settings = DefaultSettings(math.log10)
    if right:
        settings["label_right"] = 1
        settings["tick_right"] = 1
        settings["font1_size"] = 0.8*base_font_size
        settings["index_function"] = CorrectedLog10
    # Level 1 tick marks and labels
    tmp = Range(6, 46)
    strings = MP(lambda x: "%d" % x, tmp)
    values = MP(lambda x: math.tan(x*d2r), tmp)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    tmp = Range(65, 446, 10)
    values = MP(lambda x: math.tan(x/10*d2r), tmp)
    settings["unlabelled2"] = values
    # Level 3 tick marks and labels
    tmp = Range(57, 450)
    values = MP(lambda x: math.tan(x/10*d2r), tmp)
    settings["unlabelled3"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
def Tan2_10inch(x0, y0, x1, y1, right=0, settings=None):
    push()
    if not settings:
        settings = DefaultSettings(math.log10)
    if right:
        settings["label_right"] = 1
        settings["tick_right"] = 1
        settings["font1_size"] = 0.8*base_font_size
        settings["index_function"] = CorrectedLog10
    # Level 1 tick marks and labels
    n = int(math.atan(10)/d2r + 1)
    tmp = Range(45, n)
    strings = MP(lambda x: "%d" % x, tmp)
    values = MP(lambda x: math.tan(x*d2r), tmp)
    values[0] = math.tan(45*d2r) + 1e-8  # Hack to get to left of scale
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    tmp = Range(455, 840, 10)
    values = MP(lambda x: math.tan(x/10*d2r), tmp)
    settings["unlabelled2"] = values
    # Level 3 tick marks and labels
    tmp = Range(451, 844)
    values = MP(lambda x: math.tan(x/10*d2r), tmp)
    settings["unlabelled3"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
def Tan3_10inch(x0, y0, x1, y1, right=0, settings=None):
    push()
    if not settings:
        settings = DefaultSettings(math.log10)
    if right:
        settings["label_right"] = 1
        settings["tick_right"] = 1
        settings["index_function"] = CorrectedLog10
    # Level 1 tick marks and labels
    tmp = Range(85, 90)
    strings = MP(lambda x: "%d" % x, tmp)
    values = MP(lambda x: math.tan(x*d2r)/100, tmp)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    tmp = Range(845, 886, 10)
    strings = MP(lambda x: "%.1f" % (x/10), tmp)
    values = MP(lambda x: math.tan(x/10*d2r)/10, tmp)
    settings["labelled2"] = [values, strings]
    # Level 3 tick marks and labels
    tmp = []
    for ix in Range(871, 895):
        if ix % 5 == 0:
            continue
        tmp.append(ix)
    strings = MP(lambda x: "%.1f" % (x/10), tmp)
    values = MP(lambda x: math.tan(x/10*d2r)/10, tmp)
    settings["labelled3"] = [values, strings]
    # Level 4 tick marks
    tmp = Range(843, 870)
    values = MP(lambda x: math.tan(x/10*d2r)/10, tmp)
    tmp = Range(8705, 8940, 10)
    values += MP(lambda x: math.tan(x/100*d2r)/10, tmp)
    settings["unlabelled4"] = values
    # Level 5 tick marks
    tmp = Range(8705, 8945, 5)
    values += MP(lambda x: math.tan(x/100*d2r)/10, tmp)
    settings["unlabelled5"] = values
    # Level 6 tick marks
    tmp = Range(8605, 8700, 5)
    tmp += Range(8701, 8944)
    values = MP(lambda x: math.tan(x/100*d2r)/10, tmp)
    settings["unlabelled6"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
def Log(x0, y0, x1, y1, right=0, settings=None):
    def DivideBy10(x):
        return x/10
    push()
    if not settings:
        settings = DefaultSettings(math.log10)
    if right:
        settings["label_right"] = 1
        settings["tick_right"] = 1
        settings["tick4_length"] = 0.4
        settings["index_function"] = DivideBy10
    # Level 1 tick marks and labels
    values = Range(0, 11)
    strings = MP(lambda x: "%.1f" % (x/10), values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    values = Range(5, 96, 10)
    strings = MP(lambda x: "%.2f" % (x/100), values)
    values = MP(lambda x: x/10, values)
    settings["labelled2"] = [values, strings]
    # Level 3 tick marks
    values = MP(lambda x: x/10, Range(1, 100))
    settings["unlabelled3"] = values
    # Level 4 tick marks
    values = MP(lambda x: x/100, Range(2, 1000, 2))
    settings["unlabelled4"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
def Footer(xleft, xright, y):
    push()
    textSize(footer_font_size*base_font_size)
    textColor(footer_color)
    textName(Sans)
    # Left
    move(xleft, y)
    textLines(("Peet Cheet Sheet", "See http://www.gdssw.com/peet"))
    # Middle
    fudge = 0.6     # Guess to center.  Can't use ctext because I need the
                    # copyright symbol.
    move((xleft+xright)/2 - fudge, y)
    text("Copyright ")
    textName(Symbol)
    text(chr(227))
    textName(Sans)
    text(" 2005 Don Peterson, ")
    text("All rights reserved")
    # Right
    t = time.strftime("Version %d %b %Y %I:%M")
    t += string.lower(time.strftime(" %p"))
    move(xright, y)
    rtext(t)
    pop()
def CI(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1)
    Log10inchBack(x1, y1, x0, y0, scale=1/10, right=0)
    # Label the scales
    push()
    textSize(title_font_size*base_font_size)
    move(x0 - line_label_offset, y0 + 0.05)
    text("x")
    x = x0 - line_label_offset - 0.4*base_font_size
    y = y0 - 1.2*base_font_size
    move(x, y)
    textSize(1.5*title_font_size*base_font_size)
    textFraction("1", "x")
    textSize(base_font_size)
    if print_slide_rule_scale:
        x = x1 + slide_rule_scale_x_offset * base_font_size
        y = y1 - slide_rule_scale_y_offset * base_font_size
        move(x, y)
        text("CI")
    else:
        NumberScale(x1, y1)
    pop()
    print("CI ", end=" ")
def A(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1)
    xmiddle = x0 + 0.5*(x1 - x0)
    Log5inch(x0, y0, xmiddle, (y0+y1)/2, right=1)
    Log5inch(xmiddle, (y0+y1)/2, x1, y1, scale=10, right=1, omit_first=1)
    # Label the scales
    push()
    textSize(title_font_size*base_font_size)
    move(x0-line_label_offset, y0+0.05)
    text("x")
    move(x0-line_label_offset, y0-0.15)
    text("x")
    textSize(base_font_size)
    rmove(0.06, 0.05)
    textSize(exponent_font*base_font_size)
    text("2")
    if print_slide_rule_scale:
        x = x1 + slide_rule_scale_x_offset * base_font_size
        y = y1 - slide_rule_scale_y_offset * base_font_size
        move(x, y)
        text("A")
    else:
        NumberScale(x1, y1)
    pop()
    print("A ", end=" ")
def K(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1)
    xthird = (x1 - x0)/3
    ythird = (y1 - y0)/3
    Log3inch(x0, y0, x0 + xthird, y0 + ythird, right=1, omit_last=1)
    x = x0 + xthird
    y = y0 + ythird
    Log3inch(x, y, x + xthird, y + ythird, scale=10, right=1, omit_last=1)
    x = x0 + 2*xthird
    y = y0 + 2*ythird
    Log3inch(x, y, x + xthird, y + ythird, scale=100, right=1)
    # Put a box around 60.  Note this may not be portable.
    push()
    translate(x0 + xthird, y0 + ythird)
    translate(math.log10(6)*xthird, 0)
    lineWidth(2*line_width)
    d = tick_length
    move(-d/2, -d)
    rectangle(d, -1.2*d)
    line(0, -d, 0, 0)
    pop()
    # Label the scales
    push()
    textSize(title_font_size*base_font_size)
    move(x0-line_label_offset, y0+0.05)
    text("x")
    move(x0-line_label_offset, y0-0.15)
    text("x")
    textSize(base_font_size)
    rmove(0.06, 0.05)
    textSize(exponent_font*base_font_size)
    text("3")
    if print_slide_rule_scale:
        x = x1 + slide_rule_scale_x_offset * base_font_size
        y = y1 - slide_rule_scale_y_offset * base_font_size
        move(x, y)
        text("K")
    else:
        NumberScale(x1, y1)
    pop()
    print("K ", end=" ")
def D2R(x0, y0, x1, y1):
    # Degree scale
    push()
    settings = DefaultSettings(Identity)
    # Level 1 tick marks and labels
    values = Range(0, 91, 10)
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda x: x/90, values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    values = []
    for ix in Range(5, 90, 5):
        if ix % 10 == 0:
            continue
        values.append(ix)
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda x: x/90, values)
    settings["labelled2"] = [values, strings]
    # Level 3 tick marks and labels
    values = MP(lambda x: x/90, Range(1, 90))
    settings["unlabelled3"] = values
    # Level 4 tick marks
    values = MP(lambda x: x/900, Range(2, 900, 2))
    settings["unlabelled4"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    # Radian scale
    settings = DefaultSettings(Identity)
    settings["label_right"] = 1
    settings["tick_right"] = 1
    settings["tick2_length"] = 0.7
    settings["tick3_length"] = 0.5
    # Level 1 tick marks and labels
    values = Range(0, 16)
    values = MP(lambda x: x/10, values)
    strings = MP(lambda x: "%.1f" % x, values)
    values = MP(lambda x: x/(math.pi/2), values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    values = Range(5, 156, 10)
    strings = MP(lambda x: "%.2f" % (x/100), values)
    values = MP(lambda x: x/(100*math.pi/2), values)
    settings["labelled2"] = [values, strings]
    # Level 3 tick marks and labels
    values = MP(lambda x: x/(100*math.pi/2), Range(1, 158))
    settings["unlabelled3"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    # Label the scales
    push()
    textSize(title_font_size*base_font_size)
    bfs = base_font_size
    move(x0 - line_label_offset, y0 + 0.5*bfs)
    stext("x, \\b0")
    move(x0 - line_label_offset - 0.4*bfs, y0 - 1.0*bfs)
    text("rad")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    pop()
    print("D2R ", end=" ")
def S(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1, scale=1/10)
    Sin10inch(x0, y0, x1, y1, right=1)
    # Label the scales
    push()
    textSize(title_font_size*base_font_size)
    move(x0-line_label_offset, y0 - 0.15)
    stext("x, \\b0")
    move(x0-line_label_offset - 0.8*base_font_size, y0 + 0.05)
    text("sin(x)")
    if print_slide_rule_scale:
        x = x1 + slide_rule_scale_x_offset * base_font_size
        y = y1 - slide_rule_scale_y_offset * base_font_size
        move(x, y)
        text("S")
    else:
        NumberScale(x1, y1)
    pop()
    print("S ", end=" ")
def ST(x0, y0, x1, y1):
    settings = DefaultSettings(math.log10)
    settings["font3_size"] = 0.5
    Log10inch(x0, y0, x1, y1, scale=1/100, settings=settings)
    SinTan10inch(x0, y0, x1, y1, right=1)
    # Label the scales
    push()
    textSize(title_font_size*base_font_size)
    move(x0-line_label_offset, y0 - 0.15)
    stext("x, \\b0")
    move(x0-line_label_offset - 1.7*base_font_size, y0 + 0.05)
    text("sin, tan")
    if print_slide_rule_scale:
        x = x1 + slide_rule_scale_x_offset * base_font_size
        y = y1 - slide_rule_scale_y_offset * base_font_size
        move(x, y)
        text("ST")
    else:
        NumberScale(x1, y1)
    pop()
    print("ST ", end=" ")
def T1(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1, scale=1/10)
    Tan1_10inch(x0, y0, x1, y1, right=1)
    # Label the scales
    push()
    textSize(title_font_size*base_font_size)
    move(x0-line_label_offset, y0 - 0.15)
    stext("x, \\b0")
    move(x0-line_label_offset - 1.0*base_font_size, y0 + 0.05)
    text("tan(x)")
    if print_slide_rule_scale:
        x = x1 + slide_rule_scale_x_offset * base_font_size
        y = y1 - slide_rule_scale_y_offset * base_font_size
        move(x, y)
        text("T1")
    else:
        NumberScale(x1, y1)
    pop()
    print("T1 ", end=" ")
def T2(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1)
    Tan2_10inch(x0, y0, x1, y1, right=1)
    # Label the scales
    push()
    textSize(title_font_size*base_font_size)
    move(x0-line_label_offset, y0 - 0.15)
    stext("x, \\b0")
    move(x0-line_label_offset - 1.0*base_font_size, y0 + 0.05)
    text("tan(x)")
    if print_slide_rule_scale:
        x = x1 + slide_rule_scale_x_offset * base_font_size
        y = y1 - slide_rule_scale_y_offset * base_font_size
        move(x, y)
        text("T2")
    else:
        NumberScale(x1, y1)
    pop()
    print("T2 ", end=" ")
def T3(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1, scale=10)
    Tan3_10inch(x0, y0, x1, y1, right=1)
    # Label the scales
    push()
    textSize(title_font_size*base_font_size)
    move(x0-line_label_offset, y0 - 0.15)
    stext("x, \\b0")
    move(x0-line_label_offset - 1.0*base_font_size, y0 + 0.05)
    text("tan(x)")
    if print_slide_rule_scale:
        x = x1 + slide_rule_scale_x_offset * base_font_size
        y = y1 - slide_rule_scale_y_offset * base_font_size
        move(x, y)
        text("T3")
    else:
        NumberScale(x1, y1)
    pop()
    print("T3 ", end=" ")
def L(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1)
    Log(x0, y0, x1, y1, right=1)
    # Label the scales
    push()
    textSize(title_font_size*base_font_size)
    move(x0-line_label_offset - 1.0*base_font_size, y0 - 0.15)
    text("log(x)")
    move(x0-line_label_offset, y0 + 0.05)
    stext("x")
    if print_slide_rule_scale:
        x = x1 + slide_rule_scale_x_offset * base_font_size
        y = y1 - slide_rule_scale_y_offset * base_font_size
        move(x, y)
        text("L")
    else:
        NumberScale(x1, y1)
    pop()
    print("L ", end=" ")
def LL1(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1, scale=1/10)
    # Label the scales
    push()
    settings = DefaultSettings(math.log10)
    settings["label_right"] = 1
    settings["tick_right"] = 1
    settings["index_function"] = CorrectedLog10
    # Level 1 tick marks and labels
    values = MP(lambda x: x/10, range(12, 28))
    strings = MP(lambda x: "%.1f" % x, values)
    strings = MP(Trim0, strings)
    values = MP(math.log, values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    values = MP(lambda x: x/100, Range(111, 120))
    values += MP(lambda x: x/100, Range(122, 130, 2) + Range(132, 140, 2))
    strings = MP(lambda x: "%.2f" % x, values)
    strings = MP(Trim0, strings)
    values = MP(math.log, values)
    settings["labelled2"] = [values, strings]
    values = MP(lambda x: math.log(x/100), Range(145, 270, 10))
    settings["unlabelled2"] = values
    # Level 3 tick marks and labels
    values = MP(lambda x: x/1000, Range(1115, 1200, 10))
    values += MP(lambda x: x/100, Range(121, 140))
    values = MP(math.log, values)
    settings["unlabelled3"] = values
    # Level 4 tick marks and labels
    values = MP(lambda x: math.log(x/1000), Range(1106, 1200))
    values += MP(lambda x: math.log(x/1000), Range(1202, 1400, 2))
    values += MP(lambda x: math.log(x/100), Range(141, 272))
    settings["unlabelled4"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    push()
    textSize(title_font_size*base_font_size)
    move(x0-1.1*line_label_offset, y0 - 0.15)
    text("e")
    push()
    move(x0-0.9*line_label_offset, y0 - 0.10)
    textSize(0.8*base_font_size)
    text("x")
    pop()
    move(x0-line_label_offset, y0 + 0.05)
    stext("x")
    if print_slide_rule_scale:
        x = x1 + slide_rule_scale_x_offset * base_font_size
        y = y1 - slide_rule_scale_y_offset * base_font_size
        move(x, y)
        text("LL1")
    else:
        NumberScale(x1, y1)
    pop()
    print("LL1 ", end=" ")
def LL2(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1, scale=1)
    # Label the scales
    push()
    settings = DefaultSettings(math.log10)
    settings["label_right"] = 1
    settings["tick_right"] = 1
    settings["tick3_length"] = 0.7
    settings["tick3_length"] = 0.5
    settings["font1_size"] = 0.8*base_font_size
    settings["index_function"] = CorrectedLog10
    # Level 1 tick marks and labels
    values = Range(3, 11)
    values += Range(20, 81, 10)
    values += [100]
    values += MP(lambda x: x, Range(200, 501, 100))
    values += [700, 1000, 2000, 3000, 5000, 10000, 20000]
    strings = MP(lambda x: "%.1f" % x, values)
    strings = MP(Trim0, strings)
    values = MP(math.log, values)
    settings["labelled1"] = [values, strings]
    values = [90, 600, 800, 900, 4000, 6000, 7000, 8000, 9000]
    settings["unlabelled1"] = MP(math.log, values)
    # Level 2 tick marks and labels
    values = MP(lambda x: x/10, Range(35, 100, 10))
    values += MP(lambda x: x, Range(15, 100, 10))
    values += MP(lambda x: x, Range(150, 1000, 100))
    values += MP(lambda x: x, Range(1500, 10000, 1000))
    values += [15000]
    strings = MP(lambda x: "%.2f" % x, values)
    values = MP(math.log, values)
    settings["unlabelled2"] = values
    # Level 3 tick marks and labels
    values = MP(lambda x: x/10, Range(28, 100))
    values += MP(lambda x: x, Range(11, 100))
    values += MP(lambda x: x, Range(110, 500, 10))
    values += MP(lambda x: x, Range(1100, 5000, 100))
    values += MP(lambda x: x, Range(11000, 20000, 1000))
    values = MP(math.log, values)
    settings["unlabelled3"] = values
    # Level 4 tick marks and labels
    values = MP(lambda x: x/100, Range(272, 500, 2))
    values += MP(lambda x: x/10, Range(102, 200, 2))
    values = MP(math.log, values)
    settings["unlabelled4"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    push()
    textSize(title_font_size*base_font_size)
    move(x0-1.1*line_label_offset, y0 - 0.15)
    text("e")
    push()
    move(x0-0.9*line_label_offset, y0 - 0.10)
    textSize(0.8*base_font_size)
    text("x")
    pop()
    move(x0-line_label_offset, y0 + 0.05)
    stext("x")
    if print_slide_rule_scale:
        x = x1 + slide_rule_scale_x_offset * base_font_size
        y = y1 - slide_rule_scale_y_offset * base_font_size
        move(x, y)
        text("LL2")
    else:
        NumberScale(x1, y1)
    pop()
    print("LL2 ", end=" ")
def LL3(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1, scale=10)
    # Label the scales
    push()
    settings = DefaultSettings(math.log10)
    settings["label_right"] = 1
    settings["tick_right"] = 1
    settings["font1_size"] = 0.8*base_font_size
    settings["tick3_length"] = 0.7
    settings["tick4_length"] = 0.5
    settings["index_function"] = Identity
    # Level 1 tick marks and labels
    values = Range(5, 44)
    strings = MP(lambda x: "%d" % x, values)
    const = math.log10(math.exp(10))
    values = MP(lambda x: x/const, values)
    values = MP(math.log10, values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    values = MP(lambda x: x/10, Range(45, 300, 10))
    strings = MP(lambda x: "%.1f" % x, values)
    values = MP(lambda x: x/const, values)
    values = MP(math.log10, values)
    settings["unlabelled2"] = values
    # Level 3 tick marks and labels
    values = MP(lambda x: x/10, Range(44, 300))
    values += MP(lambda x: x/10, Range(302, 435, 2))
    values = MP(lambda x: x/const, values)
    values = MP(math.log10, values)
    settings["unlabelled3"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    push()
    textSize(title_font_size*base_font_size)
    move(x0-1.5*line_label_offset, y0 - 0.15)
    text("log(e")
    push()
    move(x0-0.7*line_label_offset, y0 - 0.10)
    textSize(0.8*base_font_size)
    text("x")
    pop()
    move(x0-0.5*line_label_offset, y0 - 0.15)
    text(")")
    move(x0-line_label_offset, y0 + 0.05)
    stext("x")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    pop()
    print("LL3 ", end=" ")
def LL0minus(x0, y0, x1, y1):
    def BackwardCorrectedLog10(x):
        return 1 - CorrectedLog10(x)
    def Inverse(y):
        x = -math.log(y)
        return x
    Log10inch(x0, y0, x1, y1, scale=1/10)
    # Label the scales
    push()
    settings = DefaultSettings(math.log10)
    settings["label_angle"] = 180
    settings["label1_y"] = -0.1
    settings["label2_y"] = -0.09
    settings["label3_y"] = -0.08
    settings["index_function"] = BackwardCorrectedLog10
    # Level 1 tick marks and labels
    values = Range(4, 10)
    strings = MP(lambda x: "%.2f" % (x/10), values)
    values = MP(lambda y: Inverse(y/10), values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    values = MP(lambda x: x/100, Range(45, 90, 10))
    strings = MP(lambda x: "%.2f" % x, values)
    values = MP(lambda y: Inverse(y), values)
    settings["labelled2"] = [values, strings]
    # Level 3 tick marks and labels
    values = []
    for i in Range(61, 91):
        if i % 5 == 0:
            continue
        values.append(i/100)
    strings = MP(lambda x: "%.2f" % x, values)
    values = MP(lambda y: Inverse(y), values)
    settings["labelled3"] = [values, strings]
    # Level 4 tick marks
    values = MP(lambda x: x/1000, Range(370, 600, 10))
    values += MP(lambda x: x/1000, Range(605, 896, 10))
    values = MP(lambda y: Inverse(y), values)
    settings["unlabelled4"] = values
    # Level 5 tick marks
    values = MP(lambda x: x/1000, Range(601, 905))
    values += MP(lambda x: x/1000, Range(368, 600, 2))
    values = MP(lambda y: Inverse(y), values)
    settings["unlabelled5"] = values
    # Note the reversal of the points
    s = Scale(x1, y1, x0, y0, settings)
    s.Draw()
    pop()
    push()
    textSize(title_font_size*base_font_size)
    move(x0-1.1*line_label_offset, y0 - 0.15)
    text("e")
    push()
    move(x0-0.9*line_label_offset, y0 - 0.10)
    textSize(0.8*base_font_size)
    text("-x")
    pop()
    move(x0-line_label_offset, y0 + 0.05)
    stext("x")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    pop()
    print("LL/0 ", end=" ")
def LL1minus(x0, y0, x1, y1):
    def BackwardCorrectedLog10(x):
        return 1 - CorrectedLog10(x)
    def Inverse(y):
        x = -math.log(y)
        return x
    def Fmt(x):
        "Remove any 0's in the exponent"
        if x >= 0.1:
            return "%.1f" % x
        else:
            s = "%.0e" % x
            t = ""
            found = 0
            for c in s:
                if c == "-":
                    found = 1
                if found:
                    if c != "0":
                        t += c
                else:
                    t += c
            return t
    Log10inch(x0, y0, x1, y1)
    # Label the scales
    push()
    settings = DefaultSettings(math.log10)
    settings["label_angle"] = 180
    settings["label1_y"] = -0.1
    settings["label2_y"] = -0.09
    settings["label3_y"] = -0.08
    settings["tick3_length"] = 0.7
    settings["tick4_length"] = 0.5
    settings["index_function"] = BackwardCorrectedLog10
    # Level 1 tick marks and labels
    values = [0.3, 0.2, 0.1, 1e-2, 1e-3, 1e-4]
    strings = MP(lambda x: Fmt(x), values)
    values = MP(lambda y: Inverse(y), values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    v = Range(2, 9)
    s = MP(lambda x: "%d" % x, v)
    values = MP(lambda x: x/100, v + [9])
    values += MP(lambda x: x/1e3, v)
    values += MP(lambda x: x/1e4, v)
    values += [0.15, 0.25, 0.35, 7e-5, 6e-5, 5e-5]
    strings = s + ["9"]
    strings += s*2
    strings += ["0.15", "0.25", ".35", "7", "6", "5"]
    values = MP(lambda y: Inverse(y), values)
    settings["labelled2"] = [values, strings]
    values = MP(lambda y: Inverse(y), [9e-3, 9e-4, 9e-5, 8e-5])
    settings["unlabelled2"] = values
    # Level 3 tick marks
    values = MP(lambda x: x/1e5, [5.5, 6.5, 7.5, 8.5, 9.5])
    values += MP(lambda x: x/(1e4*10), Range(15, 100, 10))
    values += MP(lambda x: x/(1e3*10), Range(15, 100, 10))
    values += MP(lambda x: x/(1e2*10), Range(15, 100, 10))
    values += MP(lambda x: x/(1e2*10), Range(110, 370, 10))
    values = MP(lambda y: Inverse(y), values)
    settings["unlabelled3"] = values
    # Level 4 tick marks
    values = MP(lambda x: x/1000, Range(102, 367, 2))
    values += MP(lambda x: x/(1e2*10), Range(11, 100))
    values += MP(lambda x: x/(1e3*10), Range(11, 100))
    values += MP(lambda x: x/(1e4*10), Range(11, 50))
    values = MP(lambda y: Inverse(y), values)
    settings["unlabelled4"] = values
    if 0:
        # Level 5 tick marks
        values = MP(lambda x: x/1000, Range(601, 905))
        values += MP(lambda x: x/1000, Range(368, 600, 2))
        values = MP(lambda y: Inverse(y), values)
        settings["unlabelled5"] = values
    # Note the reversal of the points
    s = Scale(x1, y1, x0, y0, settings)
    s.Draw()
    pop()
    push()
    textSize(title_font_size*base_font_size)
    move(x0-1.1*line_label_offset, y0 - 0.15)
    text("e")
    push()
    move(x0-0.9*line_label_offset, y0 - 0.10)
    textSize(0.8*base_font_size)
    text("-x")
    pop()
    move(x0-line_label_offset, y0 + 0.05)
    stext("x")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    pop()
    print("LL/1 ", end=" ")
def AreaCircle(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1)
    def Inverse(y):
        return math.sqrt(4 * y/math.pi)
    # Label the scales
    push()
    settings = DefaultSettings(math.log10)
    settings["label_right"] = 1
    settings["tick_right"] = 1
    settings["index_function"] = CorrectedLog10
    # Level 1 tick marks and labels
    values = MP(lambda x: x, Range(1, 10))
    values += MP(lambda x: x, Range(10, 80, 10))
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda y: Inverse(y), values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    values = MP(lambda x: x/10, Range(8, 10))
    strings = MP(lambda x: "%.1f" % x, values)
    tmp = MP(lambda x: x/10, Range(15, 100, 10))
    strings += MP(lambda x: "%.1f" % x, tmp)
    values += tmp
    tmp = MP(lambda x: x, Range(15, 80, 10))
    strings += MP(lambda x: "%d" % x, tmp)
    values += tmp
    values = MP(lambda y: Inverse(y), values)
    settings["labelled2"] = [values, strings]
    # Level 3 tick marks and labels
    values = [.85, .95]
    values += MP(lambda x: x/10, Range(11, 100))
    values += MP(lambda x: x, Range(11, 79))
    values = MP(lambda y: Inverse(y), values)
    settings["unlabelled3"] = values
    # Level 4 tick marks
    values = MP(lambda x: x/100, Range(78, 100))
    values += MP(lambda x: x/100, Range(100, 200, 2))
    values += MP(lambda x: x/10, Range(100, 400, 2))
    values = MP(lambda y: Inverse(y), values)
    settings["unlabelled4"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    push()
    textSize(title_font_size*base_font_size)
    y = y0 - 0.15
    move(x0-1.35*line_label_offset, y)
    stext("\\70")
    move(x0-1.05*line_label_offset, y)
    text("D")
    push()
    move(x0-0.75*line_label_offset, y + 0.05)
    textSize(0.8*base_font_size)
    text("2")
    pop()
    move(x0-0.6*line_label_offset, y)
    text("/4")
    move(x0-line_label_offset, y0 + 0.05)
    text("D")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    pop()
    print("CirArea ", end=" ")
def VolumeSphere(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1)
    def Inverse(y):
        return pow(3*y/(4*math.pi), 1/3)
    # Label the scales
    push()
    settings = DefaultSettings(math.log10)
    settings["label_right"] = 1
    settings["tick_right"] = 1
    settings["index_function"] = CorrectedLog10
    # Level 1 tick marks and labels
    values = MP(lambda x: x, Range(5, 10))
    values += MP(lambda x: x, Range(10, 100, 10))
    values += MP(lambda x: x, Range(100, 900, 100))
    values += MP(lambda x: x, Range(1000, 5000, 1000))
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda y: Inverse(y), values)
    settings["labelled1"] = [values, strings]
    values = [Inverse(900)]
    settings["unlabelled1"] = values
    # Level 2 tick marks and labels
    values = MP(lambda x: x, Range(15, 70, 10))
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda y: Inverse(y), values)
    settings["labelled2"] = [values, strings]
    values = MP(lambda x: Inverse(x/10), Range(45, 100, 10))
    values += MP(lambda x: Inverse(x), Range(75, 100, 10))
    values += MP(lambda x: Inverse(x), Range(150, 1000, 100))
    values += MP(lambda x: Inverse(x), Range(1500, 5000, 1000))
    settings["unlabelled2"] = values
    # Level 3 tick marks and labels
    values = MP(lambda x: x/10, Range(42, 100))
    values += MP(lambda x: x, Range(10, 100))
    values += MP(lambda x: x, Range(110, 1000, 10))
    values += MP(lambda x: x, Range(1100, 4200, 100))
    values = MP(lambda y: Inverse(y), values)
    settings["unlabelled3"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    push()
    textSize(title_font_size*base_font_size)
    y = y0 - 0.15
    move(x0-1.40*line_label_offset, y)
    stext("4\\70")
    move(x0-0.95*line_label_offset, y)
    text("r")
    push()
    move(x0-0.75*line_label_offset, y + 0.05)
    textSize(0.8*base_font_size)
    text("3")
    pop()
    move(x0-0.6*line_label_offset, y)
    text("/3")
    move(x0-line_label_offset, y0 + 0.05)
    text("r")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    pop()
    print("VolSph ", end=" ")
def AreaSphere(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1)
    def Inverse(y):
        return math.sqrt(y/(4*math.pi))
    # Label the scales
    push()
    settings = DefaultSettings(math.log10)
    settings["label_right"] = 1
    settings["tick_right"] = 1
    settings["tick2_length"] = 0.7
    settings["tick3_length"] = 0.5
    settings["tick4_length"] = 0.35
    settings["tick5_length"] = 0.25
    settings["index_function"] = CorrectedLog10
    # Level 1 tick marks and labels
    values = Range(20, 100, 10)
    values += Range(100, 1001, 100)
    values += [1200]
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda y: Inverse(y), values)
    settings["labelled1"] = [values, strings]
    values = MP(lambda y: Inverse(y), [1100])
    settings["unlabelled1"] = values
    # Level 2 tick marks and labels
    values = MP(lambda x: x, Range(13, 20))
    values += MP(lambda x: x, Range(25, 70, 10))
    values += MP(lambda x: x, Range(150, 651, 100))
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda y: Inverse(y), values)
    settings["labelled2"] = [values, strings]
    values = MP(lambda x: Inverse(x/10), Range(45, 100, 10))
    values += MP(lambda x: Inverse(x), Range(75, 100, 10))
    values += MP(lambda x: Inverse(x), Range(150, 1300, 100))
    #values += MP(lambda x: Inverse(x), Range(1500, 5000, 1000))
    settings["unlabelled2"] = values
    # Level 3 tick marks and labels
    values = MP(lambda x: x/10, Range(42, 100))
    values += MP(lambda x: x, Range(10, 100))
    values += MP(lambda x: x, Range(110, 1000, 10))
    values += MP(lambda x: x, Range(1000, 1250, 10))
    values = MP(lambda y: Inverse(y), values)
    settings["unlabelled3"] = values
    # Level 4 tick marks and labels
    values = MP(lambda x: x/10, Range(135, 200, 5))
    values += MP(lambda x: x, Range(102, 300, 2))
    values = MP(lambda y: Inverse(y), values)
    settings["unlabelled4"] = values
    # Level 5 tick marks and labels
    values = MP(lambda x: x/10, Range(126, 200))
    values = MP(lambda y: Inverse(y), values)
    settings["unlabelled5"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    push()
    textSize(title_font_size*base_font_size)
    y = y0 - 0.15
    move(x0-1.20*line_label_offset, y)
    stext("4\\70")
    move(x0-0.75*line_label_offset, y)
    text("r")
    push()
    move(x0-0.55*line_label_offset, y + 0.05)
    textSize(0.8*base_font_size)
    text("2")
    pop()
    move(x0-line_label_offset, y0 + 0.05)
    text("r")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    pop()
    print("AreaSph ", end=" ")
def Pi(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1)
    def Inverse(y):
        return y/math.pi
    # Label the scales
    push()
    settings = DefaultSettings(math.log10)
    settings["label_right"] = 1
    settings["tick_right"] = 1
    settings["index_function"] = CorrectedLog10
    # Level 1 tick marks and labels
    values = MP(lambda x: x, Range(4, 10))
    values += MP(lambda x: x, Range(10, 40, 10))
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda y: Inverse(y), values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    values = MP(lambda x: x/10, Range(35, 100, 10))
    strings = MP(lambda x: "%.1f" % x, values)
    tmp = MP(lambda x: x, Range(11, 32))
    del tmp[9]
    del tmp[-2]
    strings += MP(lambda x: "%d" % x, tmp)
    values += tmp
    values = MP(lambda y: Inverse(y), values)
    settings["labelled2"] = [values, strings]
    # Level 3 tick marks
    values = MP(lambda x: x/10, Range(32, 100))
    values += MP(lambda x: x/10, Range(105, 315, 10))
    values = MP(lambda y: Inverse(y), values)
    settings["unlabelled3"] = values
    # Level 4 tick marks
    values = MP(lambda x: x/100, Range(316, 1000, 2))
    values += MP(lambda x: x/100, Range(101, 315))
    values = MP(lambda y: Inverse(y), values)
    settings["unlabelled4"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    push()
    textSize(title_font_size*base_font_size)
    y = y0 - 0.15
    move(x0-1.20*line_label_offset, y)
    stext("\\70")
    move(x0-0.85*line_label_offset, y)
    text("x")
    move(x0-line_label_offset, y0 + 0.05)
    text("x")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    pop()
    print("Pi ", end=" ")
def InvLogGamma(y):
    # Newton-Raphson to find x given y
    assert(0 <= y <= loggamma(100))
    if y <= loggamma(10):
        x = 5         # First guess
        xlast = x
        eps = 1e-5    # Iteration stopping point
        delta = 1e-5  # Offset to calculate derivative
    else:
        x = 80        # First guess
        xlast = x
        eps = 1e-3    # Iteration stopping point
        delta = 1e-3  # Offset to calculate derivative
    done = 0
    count = 0
    def F(x):
        return loggamma(x) - y
    while not done:
        Fx = F(x)
        deriv = (Fx - F(x - delta))/delta
        x = xlast - Fx/deriv
        if math.fabs(F(x)) < eps:
            done = 1
        count += 1
        if count > 20:
            raise "Too many iterations"
        xlast = x
    return x
def Loggamma1(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1)
    push()
    settings = DefaultSettings(math.log10)
    settings["label_right"] = 1
    settings["tick_right"] = 1
    settings["index_function"] = CorrectedLog10
    # Level 1 tick marks and labels
    values = MP(lambda x: x, Range(6))
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda y: InvLogGamma(y), values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    values = MP(lambda x: x/10, Range(1, 10))
    values += MP(lambda x: x/10, Range(15, 56, 10))
    strings = MP(lambda x: "%.1f" % x, values)
    values = MP(lambda y: InvLogGamma(y), values)
    settings["labelled2"] = [values, strings]
    # Level 3 tick marks
    values = MP(lambda x: x/100, Range(15, 100, 10))
    values = MP(lambda x: x/10, Range(11, 55))
    values = MP(lambda y: InvLogGamma(y), values)
    settings["unlabelled3"] = values
    # Level 4 tick marks
    values = MP(lambda x: x/100, Range(5, 100, 10))
    values += MP(lambda x: x/100, Range(102, 300, 2))
    values = MP(lambda y: InvLogGamma(y), values)
    settings["unlabelled4"] = values
    # Level 5 tick marks
    values = MP(lambda x: x/100, Range(1, 100))
    values = MP(lambda y: InvLogGamma(y), values)
    settings["unlabelled5"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    push()
    textSize(title_font_size*base_font_size)
    y = y0 - 0.1
    move(x0-1.80*line_label_offset, y)
    stext("log(\\47(x))")
    move(x0-0.95*line_label_offset, y)
    move(x0-line_label_offset, y0 + 0.05)
    text("x")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    # Now put in a box to indicate no function values (between 1 and
    # 2, the loggamma function is not monotonic).
    translate(x0, y0)
    move(0, 0)
    lineOff()
    width = (x1-x0)/3.35
    height = -tick_length
    separation = width/30
    lineFill(45, separation)
    fillColor(gray(0.5))
    fillOn()
    fillType(line_fill)
    lineFillWidth(line_width)
    rectangle(width, height)
    if 0:
        # Make it a cross hatching
        lineFill(135, separation, phase=1.0)
        rectangle(width, height)
    pop()
    print("Lngamma1 ", end=" ")
def Loggamma2(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1, scale=10)
    push()
    settings = DefaultSettings(math.log10)
    settings["label_right"] = 1
    settings["tick_right"] = 1
    settings["tick3_length"] = 0.7
    settings["tick4_length"] = 0.5
    settings["index_function"] = CorrectedLog10
    # Level 1 tick marks and labels
    values = MP(lambda x: x, Range(10, 160, 10))
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda y: InvLogGamma(y), values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    values = MP(lambda x: x, Range(6, 10))
    values += MP(lambda x: x, Range(11, 20))
    values += MP(lambda x: x, Range(25, 100, 10))
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda y: InvLogGamma(y), values)
    settings["labelled2"] = [values, strings]
    values = MP(lambda x: x, Range(105, 156, 10))
    values = MP(lambda y: InvLogGamma(y), values)
    settings["unlabelled2"] = values
    # Level 3 tick marks
    values = MP(lambda x: x/10, Range(65, 200, 10))
    values += MP(lambda x: x/10, Range(210, 1550, 10))
    values = MP(lambda y: InvLogGamma(y), values)
    settings["unlabelled3"] = values
    # Level 4 tick marks
    values = MP(lambda x: x/10, Range(56, 200))
    values += MP(lambda x: x/10, Range(202, 500, 2))
    values = MP(lambda y: InvLogGamma(y), values)
    settings["unlabelled4"] = values
    if 0:
        # Level 5 tick marks
        values = MP(lambda x: x/100, Range(1, 100))
        values = MP(lambda y: InvLogGamma(y), values)
        settings["unlabelled5"] = values
    # Note the reversal of the points
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    push()
    textSize(title_font_size*base_font_size)
    y = y0 - 0.1
    move(x0-1.80*line_label_offset, y)
    stext("log(\\47(x))")
    move(x0-0.95*line_label_offset, y)
    move(x0-line_label_offset, y0 + 0.05)
    text("x")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    pop()
    print("Lngamma2 ", end=" ")
def Temp1(x0, y0, x1, y1):
    # -40 to 120 deg C to deg F
    push()
    settings = DefaultSettings(math.log10)
    settings["tick3_length"] = 0.5
    settings["index_function"] = Identity
    low = -40
    high = 120
    def Frac(x):
        return (x - low)/(high - low)
    # Level 1 tick marks and labels
    values = MP(lambda x: x, Range(low, high+1, 10))
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda x: Frac(x), values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks
    values = MP(lambda x: Frac(x), Range(low+5, high, 10))
    settings["unlabelled2"] = values
    # Level 3 tick marks
    values = MP(lambda x: x, Range(low+5, high, 10))
    values = MP(lambda x: Frac(x), Range(low+1, high))
    settings["unlabelled3"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    # deg F scale
    push()
    settings = DefaultSettings(math.log10)
    settings["label_right"] = 1
    settings["tick_right"] = 1
    settings["tick3_length"] = 0.5
    settings["index_function"] = Identity
    def ToC(F):
        return Frac((F-32)/1.8)
    # Level 1 tick marks and labels
    values = MP(lambda x: x, Range(-40, 250, 10))
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda y: ToC(y), values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks
    values = MP(lambda x: x, Range(-35, 250, 10))
    values = MP(lambda y: ToC(y), values)
    settings["unlabelled2"] = values
    # Level 3 tick marks
    values = MP(lambda x: x, Range(-39, 249))
    values = MP(lambda y: ToC(y), values)
    settings["unlabelled3"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    push()
    textSize(title_font_size*base_font_size)
    y = y0 - 0.15
    move(x0-line_label_offset, y)
    stext("\\b0F")
    move(x0-line_label_offset, y0 + 0.05)
    stext("\\b0C")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    pop()
    print("Temp1 ", end=" ")
def Temp2(x0, y0, x1, y1):
    # 0 to 2000 deg C to deg F
    push()
    settings = DefaultSettings(math.log10)
    settings["tick3_length"] = 0.5
    settings["index_function"] = Identity
    low = 0
    high = 2000
    def Frac(x):
        return (x - low)/(high - low)
    # Level 1 tick marks and labels
    values = MP(lambda x: x, Range(low, high+1, 100))
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda x: Frac(x), values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks
    values = MP(lambda x: Frac(x), Range(low+50, high, 100))
    settings["unlabelled2"] = values
    # Level 3 tick marks
    values = MP(lambda x: Frac(x), Range(low+1, high, 10))
    settings["unlabelled3"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    # deg F scale
    push()
    settings = DefaultSettings(math.log10)
    settings["label_right"] = 1
    settings["font1_size"] = 0.8*base_font_size
    settings["tick_right"] = 1
    settings["tick3_length"] = 0.5
    settings["index_function"] = Identity
    def ToC(F):
        return Frac((F-32)/1.8)
    # Level 1 tick marks and labels
    values = MP(lambda x: x, Range(100, 3700, 100))
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda y: ToC(y), values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks
    values = MP(lambda y: ToC(y), Range(50, 3600, 100))
    settings["unlabelled2"] = values
    # Level 3 tick marks
    values = MP(lambda y: ToC(y), Range(40, 3640, 10))
    settings["unlabelled3"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    push()
    textSize(title_font_size*base_font_size)
    y = y0 - 0.15
    move(x0-line_label_offset, y)
    stext("\\b0F")
    move(x0-line_label_offset, y0 + 0.05)
    stext("\\b0C")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    pop()
    print("Temp2 ", end=" ")
def In2mm(x0, y0, x1, y1):
    # 0 to 10 inches
    push()
    settings = DefaultSettings(math.log10)
    settings["tick3_length"] = 0.5
    settings["font2_size"] = 0.5
    settings["index_function"] = Identity
    low = 0
    high = 10
    def Frac(x):
        return (x - low)/(high - low)
    # Level 1 tick marks and labels
    values = MP(lambda x: x, Range(low, high+1))
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda x: Frac(x), values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks
    values = []
    for i in Range(low+1, high*10):
        if i % 10 == 0:
            continue
        values.append(i)
    values = MP(lambda x: x/10, values)
    strings = MP(lambda x: "%.1f" % x, values)
    values = MP(lambda x: Frac(x), values)
    settings["labelled2"] = [values, strings]
    # Level 3 tick marks
    values = MP(lambda x: Frac(x/100), Range(low+2, high*100, 2))
    settings["unlabelled3"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    # mm scale
    push()
    settings = DefaultSettings(math.log10)
    settings["label_right"] = 1
    settings["font1_size"] = 0.8*base_font_size
    settings["tick_right"] = 1
    settings["tick2_length"] = 0.7
    settings["tick3_length"] = 0.5
    settings["tick4_length"] = 0.3
    settings["index_function"] = Identity
    def mm_to_in(mm):
        return Frac(mm/25.4)
    # Level 1 tick marks and labels
    values = MP(lambda x: x, Range(0, 260, 10))
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda y: mm_to_in(y), values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks
    values = MP(lambda y: mm_to_in(y), Range(5, 250, 10))
    settings["unlabelled2"] = values
    # Level 3 tick marks
    values = MP(lambda y: mm_to_in(y), Range(1, 255))
    settings["unlabelled3"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    push()
    textSize(title_font_size*base_font_size)
    y = y0 - 0.15
    move(x0-line_label_offset, y)
    text("mm")
    move(x0-line_label_offset, y0 + 0.05)
    text("in")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    pop()
    print("In2mm ", end=" ")
def Fractions(x0, y0, x1, y1):
    # 0 to 1 inch
    push()
    settings = DefaultSettings(math.log10)
    settings["tick3_length"] = 0.6
    settings["tick4_length"] = 0.4
    settings["index_function"] = Identity
    low = 0
    high = 10
    def Frac(x):
        return (x - low)/(high - low)
    # Level 1 tick marks and labels
    values = MP(lambda x: x/10, Range(low, high+1))
    strings = MP(lambda x: "%.1f" % x, values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks
    values = Range(5, 100, 10)
    values = MP(lambda x: x/100, values)
    strings = MP(lambda x: "%.2f" % x, values)
    settings["labelled2"] = [values, strings]
    # Level 3 tick marks
    values = MP(lambda x: x/100, Range(0, 100))
    settings["unlabelled3"] = values
    # Level 4 tick marks
    values = MP(lambda x: x/1000, Range(2, 1000, 2))
    settings["unlabelled4"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    # Fractions
    push()
    textSize(0.9*base_font_size)
    def Reduce(num, denom):
        "Return tuple of (num, denom) reduced to lowest terms."
        while (num % 2 == 0) and (denom % 2 == 0):
            num = num//2
            denom = denom//2
        return (num, denom)
    N = 64
    for i in range(1, N):
        num, denom = Reduce(i, N)
        num_digits = len(str(num) + str(denom))
        x = x0 + (x1 - x0)*i/N
        dY = 0.3
        if denom <= 8:
            dy = 0
        elif denom == 16:
            dy = dY*base_font_size
        elif denom == 32:
            dy = 2*dY*base_font_size
        else:
            dy = 3*dY*base_font_size
        y = y0 - 0.5*base_font_size
        line(x, y0, x, y - dy)
        y = y0 - 2*base_font_size
        dx = num_digits * 0.1 * base_font_size
        move(x - dx, y - dy + 0.6*base_font_size)
        textFraction(num, denom)
    pop()
    push()
    textSize(title_font_size*base_font_size)
    y = y0 - 0.15
    move(x0-1.5*line_label_offset, y)
    text("Fraction")
    move(x0-line_label_offset, y0 + 0.05)
    text("in")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    pop()
    print("Fractions ", end=" ")
number_drills = (
    (1, 0.2280), (2, 0.2210), (3, 0.2130), (4, 0.2090), (5, 0.2055),
    (6, 0.2040), (7, 0.2010), (8, 0.1990), (9, 0.1960), (10, 0.1935),
    (11, 0.1910), (12, 0.1890), (13, 0.1850), (14, 0.1820), (15, 0.1800),
    (16, 0.1770), (17, 0.1730), (18, 0.1695), (19, 0.1660), (20, 0.1610),
    (21, 0.1590), (22, 0.1570), (23, 0.1540), (24, 0.1520), (25, 0.1495),
    (26, 0.1470), (27, 0.1440), (28, 0.1405), (29, 0.1360), (30, 0.1285),
    (31, 0.1200), (32, 0.1160), (33, 0.1130), (34, 0.1110), (35, 0.1100),
    (36, 0.1065), (37, 0.1040), (38, 0.1015), (39, 0.0995), (40, 0.0980),
    (41, 0.0960), (42, 0.0935), (43, 0.0890), (44, 0.0860), (45, 0.0820),
    (46, 0.0810), (47, 0.0785), (48, 0.0760), (49, 0.0730), (50, 0.0700),
    (51, 0.0670), (52, 0.0635), (53, 0.0595), (54, 0.0550), (55, 0.0520),
    (56, 0.0465), (57, 0.0430), (58, 0.0420), (59, 0.0410), (60, 0.0400),
    (61, 0.0390), (62, 0.0380), (63, 0.0370), (64, 0.0360), (65, 0.0350),
    (66, 0.0330), (67, 0.0320), (68, 0.0310), (69, 0.0293), (70, 0.0280),
    (71, 0.0260), (72, 0.0250), (73, 0.0240), (74, 0.0225), (75, 0.0210),
    (76, 0.0200), (77, 0.0180), (78, 0.0160), (79, 0.0145), (80, 0.0135),
)
letter_drills = (
    ("A", 0.234), ("B", 0.238), ("C", 0.242), ("D", 0.246), ("E", 0.250),
    ("F", 0.257), ("G", 0.261), ("H", 0.266), ("I", 0.272), ("J", 0.277),
    ("K", 0.281), ("L", 0.290), ("M", 0.295), ("N", 0.302), ("O", 0.316),
    ("P", 0.323), ("Q", 0.332), ("R", 0.339), ("S", 0.348), ("T", 0.358),
    ("U", 0.368), ("V", 0.377), ("W", 0.386), ("X", 0.397), ("Y", 0.404),
    ("Z", 0.413)
)
def Drills(x0, y0, x1, y1):
    # 0 to 1 inch
    push()
    settings = DefaultSettings(math.log10)
    settings["tick3_length"] = 0.6
    settings["tick4_length"] = 0.5
    settings["tick5_length"] = 0.3
    settings["index_function"] = Identity
    low = 0
    high = 0.44
    def DrillScale(x):
        return (x - low)/(high - low)
    # Level 1 tick marks and labels
    values = MP(lambda x: x/10, Range(0, 5))
    strings = MP(lambda x: "%.1f" % x, values)
    values = MP(lambda x: DrillScale(x), values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks
    values = MP(lambda x: x/100, Range(5, 40, 10))
    strings = MP(lambda x: "%.2f" % x, values)
    values = MP(lambda x: DrillScale(x), values)
    settings["labelled2"] = [values, strings]
    # Level 3 tick marks
    values = []
    for i in range(10, 450, 10):
        if i % 50 == 0 or i % 100 == 0:
            continue
        values.append(i)
    values = MP(lambda x: x/1000, values)
    strings = MP(lambda x: "%.2f" % x, values)
    values = MP(lambda x: DrillScale(x), values)
    settings["labelled3"] = [values, strings]
    # Level 4 tick marks
    values = MP(lambda x: x/1000, Range(5, 440, 10))
    values = MP(lambda x: DrillScale(x), values)
    settings["unlabelled4"] = values
    # Level 5 tick marks
    values = MP(lambda x: x/1000, Range(1, 440))
    values = MP(lambda x: DrillScale(x), values)
    settings["unlabelled5"] = values
    s = Scale(x0, y0, x1, y1, settings)
    s.Draw()
    pop()
    # Label with drill numbers and letters
    push()
    for num, diam in number_drills:
        x = x0 + (x1-x0)*DrillScale(diam)
        y = y0 - base_font_size
        if num >= 57:
            textSize(0.35*base_font_size)
            dx = -0.15*base_font_size
            if num % 2 == 0:
                y -= base_font_size/2
            line(x, y + 0.35*base_font_size, x, y1)
        else:
            textSize(0.5*base_font_size)
            dx = -0.22*base_font_size
            if len(str(num)) == 1:
                dx = -0.11*base_font_size
            if num % 2 == 0:
                y -= base_font_size/2
            line(x, y + 0.45*base_font_size, x, y1)
        move(x + dx, y)
        text(str(num))
    textSize(0.5*base_font_size)
    for letter, diam in letter_drills:
        x = x0 + (x1-x0)*DrillScale(diam)
        y = y0 - base_font_size
        line(x, y + 0.45*base_font_size, x, y1)
        move(x + dx, y - 0.1*base_font_size)
        text(letter)
    pop()
    # Label the scale
    push()
    textSize(title_font_size*base_font_size)
    y = y0 - 0.15
    move(x0-1.2*line_label_offset, y)
    text("Drill")
    move(x0-line_label_offset, y0 + 0.05)
    text("in")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    pop()
    print("Drills ", end=" ")
def SFPM(x0, y0, x1, y1):
    Log10inch(x0, y0, x1, y1, scale=1/10)
    def D(rpm):
        s = 1200/(math.pi*rpm)
        return s
    def Inverse(rpm):
        # Convert rpm to diam, then map it back to the log of the range
        # 0.1 to 10, ultimately mapping onto [0, 1].  Return 1 - object
        # to reverse the sense of the line.
        diam = D(rpm)
        assert(0.1 <= diam <= 1)
        return -math.log10(diam)
    # Scale for RPM to get 100 SFPM
    settings = DefaultSettings()
    settings["index_function"] = Identity
    settings["label_angle"] = 180
    settings["label1_y"] = -base_font_size
    settings["label2_y"] = -0.8*base_font_size
    # Level 1 tick marks and labels
    values = MP(lambda x: x, Range(400, 1000, 100))
    values += MP(lambda x: x, Range(1000, 4000, 1000))
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda x: Inverse(x), values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    values = MP(lambda x: x, Range(450, 1000, 100))
    values += MP(lambda x: x, Range(1100, 2000, 100))
    values += MP(lambda x: x, Range(2200, 3000, 200))
    values += MP(lambda x: x, Range(3200, 3800, 200))
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda x: Inverse(x), values)
    settings["labelled2"] = [values, strings]
    # Level 3 tick marks
    values = MP(lambda x: x, Range(390, 1000, 10))
    values += MP(lambda x: x, Range(1100, 3801, 100))
    values = MP(lambda x: Inverse(x), values)
    settings["unlabelled3"] = values
    # Level 4 tick marks
    values = MP(lambda x: x, Range(1050, 2000, 100))
    values += MP(lambda x: x, Range(2020, 3820, 20))
    values = MP(lambda x: Inverse(x), values)
    settings["unlabelled4"] = values
    # Level 5 tick marks
    values = MP(lambda x: x, Range(1010, 2000, 10))
    values = MP(lambda x: Inverse(x), values)
    settings["unlabelled5"] = values
    s = Scale(x1, y1, x0, y0, settings)
    s.Draw()
    # Label the scale
    push()
    y = y0 - 0.1
    textSize(0.7*base_font_size)
    move(x0-1.4*line_label_offset, y)
    textLines(("RPM for", "100 SFPM"))
    move(x0-1.3*line_label_offset, y0 + 0.05)
    textSize(base_font_size)
    text("D, in")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    pop()
    print("SFPM ", end=" ")
def MetersPerSecond(x0, y0, x1, y1):
    # Same as SFPM but in mm and m/s cutting speed
    Log10inch(x0, y0, x1, y1, scale=10)
    def D(rpm):
        s = 60000/(math.pi*rpm)
        return s
    def Inverse(rpm):
        # Convert rpm to diam, then map it back to the log of the range
        # 0.1 to 10, ultimately mapping onto [0, 1].  Return 1 - object
        # to reverse the sense of the line.
        diam = D(rpm)
        assert(10 <= diam <= 100)
        return 2 - math.log10(diam)
    settings = DefaultSettings()
    settings["index_function"] = Identity
    settings["label_angle"] = 180
    settings["label1_y"] = -base_font_size
    settings["tick3_length"] = 0.6
    settings["tick4_length"] = 0.4
    # Level 1 tick marks and labels
    values = MP(lambda x: x, Range(200, 2000, 100))
    strings = MP(lambda x: "%d" % x, values)
    values = MP(lambda x: Inverse(x), values)
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks and labels
    values = MP(lambda x: x, Range(250, 1900, 100))
    values = MP(lambda x: Inverse(x), values)
    settings["unlabelled2"] = values
    # Level 3 tick marks
    values = MP(lambda x: x, Range(200, 1900, 10))
    values = MP(lambda x: Inverse(x), values)
    settings["unlabelled3"] = values
    # Level 4 tick marks
    values = MP(lambda x: x, Range(192, 600, 2))
    values = MP(lambda x: Inverse(x), values)
    settings["unlabelled4"] = values
    s = Scale(x1, y1, x0, y0, settings)
    s.Draw()
    # Label the scale
    push()
    y = y0 - 0.1
    textSize(0.7*base_font_size)
    move(x0-1.4*line_label_offset, y)
    textLines(("RPM for", "1 m/s"))
    move(x0-1.3*line_label_offset, y0 + 0.05)
    textSize(base_font_size)
    text("D, mm")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    pop()
    print("m/s ", end=" ")
def AWG(x0, y0, x1, y1):
    def Awg(num):
        return 0.324425*math.exp(-0.115877508*num)
    # Label the scale
    push()
    y = y0 - 0.1
    x = x0 - 1.3*line_label_offset
    move(x, y)
    text("AWG")
    move(x, y0 + 0.05)
    textSize(base_font_size)
    text("D, in")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)
    pop()
    print("AWG ", end=" ")
def Arithmetic(x0, x1, y, dy):
    CI(x0, y, x1, y)
    y += dy
    A(x0, y, x1, y)
    y += dy
    K(x0, y, x1, y)
    y += dy
    return y
def Trig(x0, x1, y, dy):
    D2R(x0, y, x1, y)
    y += dy
    S(x0, y, x1, y)
    y += dy
    ST(x0, y, x1, y)
    y += dy
    T1(x0, y, x1, y)
    y += dy
    T2(x0, y, x1, y)
    y += dy
    T3(x0, y, x1, y)
    y += dy
    return y
def LogExp(x0, x1, y, dy):
    L(x0, y, x1, y)
    y += dy
    LL1(x0, y, x1, y)
    y += dy
    LL2(x0, y, x1, y)
    y += dy
    LL3(x0, y, x1, y)
    y += dy
    LL0minus(x0, y, x1, y)
    y += dy
    LL1minus(x0, y, x1, y)
    y += dy
    return y
def Mensuration(x0, x1, y, dy):
    AreaCircle(x0, y, x1, y)
    y += dy
    AreaSphere(x0, y, x1, y)
    y += dy
    VolumeSphere(x0, y, x1, y)
    y += dy
    return y
def Misc(x0, x1, y, dy):
    Pi(x0, y, x1, y)
    y += dy
    Loggamma1(x0, y, x1, y)
    y += dy
    Loggamma2(x0, y, x1, y)
    y += dy
    Temp1(x0, y, x1, y)
    y += dy
    Temp2(x0, y, x1, y)
    y += dy
    In2mm(x0, y, x1, y)
    y += dy
    return y
def Shop(x0, x1, y, dy):
    Fractions(x0, y, x1, y)
    y += dy
    Drills(x0, y, x1, y)
    y += dy
    SFPM(x0, y, x1, y)
    y += dy
    MetersPerSecond(x0, y, x1, y)
    y += dy
    #AWG(x0, y, x1, y)
    #y += dy
    #DD(x0, y, x1, y)
    #y += dy
    return y
if __name__ == "__main__":
    s = SetUp("0scale.ps", landscape)
    lineWidth(line_width)
    lineColor(line_color)
    textName(HelveticaNarrow)
    textColor(number_color)
    textSize(base_font_size)
    footer_margin = 0.5
    #Footer(footer_margin, 11-footer_margin, .3)
    y = 0.7
    dy = 0.5
    x0 = 0.75
    x1 = 10.5
    if 0:
        # Vertical line to line up labels
        line(x0 - line_label_offset, 0, x0 - line_label_offset, 10)
    show1 = 1
    if show1:
        y = Arithmetic(x0, x1, y, dy)
        y = Trig(x0, x1, y, dy)
        y = LogExp(x0, x1, y, dy)
        newPage()
    y = 0.7
    show2 = 1
    if show2:
        y = Mensuration(x0, x1, y, dy)
        y = Misc(x0, x1, y, dy)
        y = Shop(x0, x1, y, dy)
