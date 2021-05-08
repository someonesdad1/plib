'''
no_tests:ignore
ToDo:

    * Look at what it would take to produce mirror image scales by just
      setting a Boolean.  This would be quite handy to allow
      laser-printed stuff to be ironed onto a substrate.  For example,
      see http://content.photojojo.com/diy/diy-photo-transfers-on-wood/.
      Others recommend transfer pens, which appear to be felt with
      xylene, so all that's really needed is a bit of cotton and shop
      xylene (the polystyrene dissolves in it).  Wet the cotton, rub on
      the back of the paper (keep thin), and then rub things off with a
      burnisher or spoon.

      Get some spray white latex paint and put on a few thin coats and
      sand smooth.  Then the laser printing should transfer on OK
      without disturbing the white substrate.

    * Instead of a settings dictionary, make all the things like
      index_function, label_angle, tick1_length, etc. be attributes of
      the instance.  This would make source code look a little cleaner.
      It might also allow computed forms for the attributes that aren't
      defined; this would be easy to handle in __getattr__.

----------------------------------------------------------------------

This module contains the Scale object which uses the g library to draw
linear scales with tick marks and labels.

How to use:
    Get a default settings dictionary:
        settings = DefaultSettings()
 
    Change things as needed:
        settings["index_function"] = log10
        settings["label_angle"] = 180
        settings["label1_y"] = -base_font_size
        settings["label_right"] = 1
        settings["tick_right"] = 1
        settings["font1_size"] = 0.08
        settings["font2_size"] = 0.7
        settings["label2_y"] = -0.02
        settings["tick1_length"] = 0.08
        settings["tick2_length"] = 0.8   Note 2-4 are relative to tick1
        settings["tick3_length"] = 0.6
        settings["tick4_length"] = 0.4
 
        Note:  the index function determines how the points are distributed
 
    Generate the values and strings
        values = map(lambda x: x/10., range(15, 76, 10))
        settings["unlabelled1"] = [8.5, 9.5]   # These points don't plot
        tmp = map(lambda x: x*scale, values)
        strings = map(lambda x: nFmt(scale, 1) % x, tmp)
        settings["labelled1"] = [values, strings]
 
    Draw the scale from (x0, y0) to (x1, y1)
        s = Scale(x0, y0, x1, y1, settings)
        s.Draw()
 
        Note that the values passed to the Scale object should have x values
        from 0 to 1.
 
    Label the scale
    push()
    y = y0 - 0.1
    x = x0 - 1.3*line_label_offset
    move(x, y)
    text("AWG")
    move(x, y0 + 0.05)
    textSize(base_font_size)
    text("D, in")
    if not print_slide_rule_scale:
        NumberScale(x1, y1)  # Print a number to the right of the scale

'''

from __future__ import print_function, division
import sys
import g
import math

from pdb import set_trace as xx
if len(sys.argv) > 1:
    import debug as DEBUG
    DEBUG.SetDebugger()
debug = 0

wrap_in_PJL = 0
in_color = True
d2r = math.pi/180
 
# For applying a number to a scale on the RHS
scale_count = 1
scale_count_offset_x =  0.15
scale_count_offset_y = -0.05
 
# Font sizes are all relative to the base font size
base_font_size      = 8/72.27
footer_font_size    = 1
title_font_size     = 1
exponent_font       = 0.8
line_width          = 0.005
tick_length         = 0.1
line_label_offset   = 0.25
base_font           = g.Sans
base_font_bold      = g.SansBold

# Whether we should print the slide rule scale name to the right
print_slide_rule_scale = 0
slide_rule_scale_x_offset = 1.0  # Fraction of base font size
slide_rule_scale_y_offset = 0.4  # Fraction of base font size

if in_color:
    page_background_color  = g.black
    table_background_color = g.black
    title_color            = g.red
    entry_color            = g.green
    bounding_box_color     = g.blue
    bounding_box_thickness = 0.02
    table_line_thickness   = 0.005
    line_color             = g.black
    grid_color             = g.cyan
    major_tick_color       = g.red
    medium_tick_color      = g.magenta
    minor_tick_color       = g.black
    number_color           = g.blue
    footer_color           = g.black
else:
    page_background_color  = g.white
    table_background_color = g.white
    title_color            = g.black
    entry_color            = g.black
    bounding_box_color     = g.black
    bounding_box_thickness = 0.02
    table_line_thickness   = 0.005
    line_color             = g.black
    grid_color             = g.black
    major_tick_color       = g.black
    medium_tick_color      = g.black
    minor_tick_color       = g.black
    number_color           = g.black
    footer_color           = g.black

# The following global is used to correct a base 10 log to the interval
# [0, 1].
log_correction = 0

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
        self.s["label_angle"]              = 0
        self.s["label_color"]              = None
        self.s["label_right"]              = 0
        self.s["label_height_above_tick"]  = 0
        self.s["tick_right"]               = 0
        self.s["line_width"]               = None
        self.s["line_color"]               = None
        self.s["draw_line"]                = 1
        self.s["omit_first_label"]         = 0
        self.s["omit_last_label"]          = 0
        self.s["index_function"]           = None
        # Containers that describe labels and ticks to draw.  A
        # labelled container is a sequence of two sequences.  The
        # first is the values where a label/tick is and the second is
        # the string name of the label.  The two sequences must be the
        # same size.  An unlabelled container is just a sequence of
        # values to put ticks at.
        self.N = 6  # Number of containers for labels and ticks
        for n in range(1, self.N+1):
            self.s["labelled%d" % n]          = None
            self.s["unlabelled%d" % n]        = None
            self.s["label%d_x" % n]           = 0
            self.s["label%d_y" % n]           = 0
            self.s["font%d_color" % n]        = None
            self.s["tick%d_color" % n]        = None
            self.s["tick%d_width" % n]        = None
            self.s["tick%d_line_type" % n]    = None
            self.s["tick%d_start_offset" % n] = 0
        # We'll set default Font sizes
        self.s["font1_size"] = None   # User must pass in
        self.s["font2_size"] = 0.8    # All are relative to font1
        self.s["font3_size"] = 0.6
        self.s["font4_size"] = 0.5
        self.s["font5_size"] = 0.4
        self.s["font6_size"] = 0.3
        # Tick data
        self.s["tick1_length"] = None # User must pass in
        self.s["tick2_length"] = 0.9  # All are relative to tick1 length
        self.s["tick3_length"] = 0.8
        self.s["tick4_length"] = 0.6
        self.s["tick5_length"] = 0.45
        self.s["tick6_length"] = 0.35
        # Now add settings the user passed in
        self.Settings(settings)
        # Make sure we have needed settings
        if not self.s["font1_size"]:
            raise Exception("Need 'font1_size' setting")
        if not self.s["tick1_length"]:
            raise Exception("Need 'tick1_length' setting")
        if not self.s["index_function"]:
            raise Exception("Need 'index_function' setting")
        # Check labelled containers for proper form
        for num in range(1, 6):
            container = self.s["labelled%s" % num]
            if not container:
                continue
            if len(container[0]) != len(container[1]):
                raise Exception("Labelled container %d improper" % num)
        # Get length and angle
        self.length =      Distance(self.x0, self.y0, self.x1, self.y1)
        self.angle_degrees  = Angle(self.x0, self.y0, self.x1, self.y1)
    def Settings(self, settings):
        if debug:
            print("Settings:")
            keys = settings.keys()
            for key in sorted(keys):
                print("  %-20s : %s" % (key, repr(settings[key])))
            print("-"*70)
        for key in settings:
            if key in self.s:
                self.s[key] = settings[key]
            else:
                raise Exception("'" + key + "' key not in settings")
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
        g.push()
        tick_right = 1
        if self.s["tick_right"]:
            tick_right = -1
        if self.s[t + "_color"]:
            g.lineColor(self.s[t + "_color"])
        if self.s[t + "_width"]:
            g.lineColor(self.s[t + "_width"])
        if self.s[t + "_line_type"]:
            g.lineType(self.s[t + "_line_type"])
        tick_length = self.s["tick1_length"]
        if number != 1:
            tick_length *= self.s[t + "_length"]
        for value in values:
            x = self.s["index_function"](value)*self.length
            y = self.s[t + "_start_offset"]
            g.line(x, y, x, tick_right*(y + tick_length))
            if debug:
                print("Tick at (%g, %g), len = %g" % (x, y, tick_length))
        g.pop()
    def DrawLabel(self, number):
        container = self.s["labelled%d" % number]
        if not container:
            return
        f = "font%d" % number
        t = "tick%d" % number
        l = "label%d" % number
        g.push()
        tick_length = self.s["tick1_length"]
        if number != 1:
            tick_length *= self.s[t + "_length"]
            font_height = self.s[f + "_size"] * self.s["font1_size"]
        else:
            font_height = self.s["font1_size"]
        g.textSize(font_height)
        fc = self.s["font{}_color".format(number)]
        if fc is not None:
            g.TextColor(fc)
        tick_right  = 1
        label_right = 1
        if self.s["tick_right"]:
            tick_right = -1
        if self.s["label_right"]:
            label_right = -1
        for i in range(len(container[0])):
            value = container[0][i]
            label = container[1][i]
            g.push()
            x = self.s["index_function"](value) * self.length
            y = self.s[t + "_start_offset"] + tick_length
            if tick_right == -1:
                # The 1/4 is a phenomenological correction to get the
                # label a default pleasing distance from the tick
                # mark.
                y += tick_length - 1/4*font_height
            y *= tick_right
            g.translate(x, y)
            g.rotate(self.s["label_angle"])
            x = self.s[l + "_x"]
            y = self.s[l + "_y"] + font_height/10
            y *= label_right
            g.move(x, y)
            g.ctext(label)
            g.pop()
        g.pop()
    def Draw(self):
        g.push()
        g.translate(self.x0, self.y0)
        g.rotate(self.angle_degrees)
        if self.s["draw_line"]:
            if self.s["line_color"]:
                g.lineColor(self.s["line_color"])
            if self.s["line_width"]:
                g.lineWidth(self.s["line_width"])
            g.line(0, 0, self.length, 0)
        # Draw in reverse ordering to numbering so that major ticks
        # are on top of minor ticks.
        for i in range(self.N, 0, -1):
            self.DrawTick(i)
        for i in range(self.N, 0, -1):
            self.DrawLabel(i)
        g.pop()

def Distance(x0, y0, x1, y1):
    x, y = x0 - x1, y0 - y1
    return math.sqrt(x*x + y*y)

def Angle(x0, y0, x1, y1):
    '''Return the angle in degrees.
    '''
    return math.atan2(y1 - y0, x1 - x0)/d2r

def DefaultSettings(index_function=None):
    return {
        "line_width" : line_width,
        "font1_size" : base_font_size,
        "tick1_length" : tick_length,
        "index_function" : index_function,
        "tick2_length" : 1,
        "tick3_length" : 0.7,
        "tick4_length" : 0.4,
    }

def SetUp(file, orientation=g.landscape, units=g.inches):
    '''Convenience function to set up the drawing environment and return a
    file object to the output stream.
    '''
    ofp = open(file, "w")
    g.ginitialize(ofp)
    g.setOrientation(orientation, units)
    return ofp

if __name__ == "__main__":
    # When run as a script, this will create an output file
    # "linscale.ps" that contains a simple scale from 0 to 10 with
    # middle unlabelled tick marks.
    x0, x1 = 1, 10      # Left and right limits of scale, inches
    y = 7               # Scale vertical location
    # Get the default settings dictionary.  The index function needs to
    # map the x values onto [0, 1], because that's the parameter's range
    # for the whole scale.
    settings = DefaultSettings(index_function=lambda x: x/10)
    # Add some colors 
    settings = DefaultSettings(index_function=lambda x: x/10)
    settings["line_color"] = g.blue
    settings["font1_color"] = g.red

    SetUp("linscale.ps", orientation=g.landscape, units=g.inches)
    # Level 1 tick marks and labels
    values = list(range(0, 11))
    strings = [str(i) for i in values]
    settings["labelled1"] = [values, strings]
    # Level 2 tick marks
    settings["unlabelled2"] = [i + 1/2 for i in values if i < 10]
    s = Scale(x0, y, x1, y, settings)
    s.Draw()
    # Add a scale label
    x = (x0 + x1)/2
    yl, dy = y - 2*base_font_size, 1.5*base_font_size
    g.move(x, yl)
    g.ctext("Sample")
    g.move(x, yl - dy)
    g.ctext("scale")
    # Show that the origin is at the lower left corner
    g.move(0, 0)
    g.rline(1, 1)
    g.move(1.1, 1.1)
    g.text("Origin is at corner")
    g.FillOn()
    g.FillColor(g.black)
    g.move(0, 0)
    g.circle(0.5)
