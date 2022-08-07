'''
This module defines an object CircularScale that can be used to generate
things like circular slide rules.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2011 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Generate circular scales with g library
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    from math import pi, sin, cos, hypot, fmod, atan2, log10 as log, modf
if 1:   # Custom imports
    from wrap import dedent
    from g import *
if 1:   # Global variables
    version = "23 Nov 2011"
    dbg = sys.stderr.write
    mm2in = 1/25.4
    d2r = pi/180
    esc = chr(0x1b)
def GetDefaultSettings(tick_levels_supported=6):
    '''Return a default settings dictionary.  This also serves to document
    the settings.
    '''
    n = tick_levels_supported
    settings = {
        # If out is true, the tick starts from the arc and goes
        # outwards.
        "out": True,
        # draw_baseline True means the circular arc making up the scale
        # is drawn.
        "draw_baseline": False,
        # This is the color of the arc's baseline if it is drawn
        "line_color": black,
        # This is the width of the line the arc is drawn with; if it is
        # None, then the default linewidth is used.
        "line_width": None,
        # The normal direction of increasing angle is counterclockwise,
        # just as in the polar coordinate angle.  Set clockwise to True to
        # reverse the direction.  Example:  if clockwise is True, then an
        # angle of 45 degrees will be at the normal 315 degrees in the
        # fourth quadrant.
        "clockwise": False,
        # polar_angle_offset sets the location of the zero angle.  If it's
        # zero, then it's along the horizontal x axis as in the polar
        # coordinate angle.  If it's 90 degrees, then it's pointing
        # north like a compass rose.
        "polar_angle_offset": 0,
        # draw_center, if nonzero, means to draw two crossed lines at
        # the center of the scale; the line length from the origin to
        # the tip is draw_center.
        "draw_center": 0.02,
        #
        "tick_color": [black]*n,
        "tick_line_type": [solid_line]*n,
        "tick_line_cap": [cap_butt]*n,
        "font_color": [black]*n,
        "fill_color": [black]*n,
        "font_name": [Sans]*n,
        "cross_linewidth": 0.001,  # Fraction of D
        #----------------------------------------------------------
        # The following settings are such that the first element is a
        # fraction of the scale diameter D and the subsequent settings are
        # fractions of the first element's resulting value.  The elements
        # correspond to level 0 ticks, level 1 ticks, etc.  You can define
        # as many tick levels as you need.
        #
        # This ensures the whole drawing can be scaled to any size.
        "tick_length": [0.03, 0.8, 0.4, 0.2],
        "tick_linewidth": [0.002, 0.8, 0.7, 0.6],
        "font_size": [0.03, 0.8, 0.6, 0.4],
        # radial_offset determines the radial offset of the label from its
        # calculated position (this is for fine tuning the position).
        "radial_offset": [0.0, 1, 1, 1],
        # angle_offset determines the angular offset of the label from its
        # calculated position (this is for fine tuning things).  Note these
        # are NOT relative values, but just angles.
        "angle_offset": [0]*n,
        # Arrows are drawn in a radial direction.  The tip style controls
        # the size and type of arrow tip.
        # xx Arrows are not working yet
        "arrow_linewidth": [0.01, 0.8, 0.7, 0.6],
        "arrow_color": [black]*n,
        "arrow_tip_style": [0]*n,
    }
    return settings
class CircularScale:
    '''A general class to allow you to create a circular scale.  Note that
    all font sizes, tick lenths, tick widths, etc. are fractions of the
    diameter of the scale.  This allows the scale to be printed at any
    desired size.
    '''
    def __init__(self, x, y, D, arc_start, arc_end, settings, degrees=1):
        '''The degrees setting is used to define angle units; the default is
        to use degrees.  The numerical value is what angles are multiplied by
        to get degrees.  Example:  to use radians, set degrees=180/pi.  The
        reason for using degrees is because the g library uses degrees for
        angle measure.
 
        (x, y) is the center of the circle.
 
        D is the diameter of the circle.
 
        arc_start, arc_end are in degrees and define the extent of the arc
        and are in the usual polar angle measurement scheme (note that the
        polar_angle_offset setting can change the angular location of the polar
        axis.
 
        settings is a dictionary that overrides the mappings given in the
        self.s object.  This is used to allow you to define the settings
        you like in self.s and override them when needed.
        '''
        self.origin = (x, y)
        self.D = D
        self.radius = D/2
        self.arc_start = arc_start
        self.arc_end = arc_end
        self.settings = settings
        self.degrees = degrees
        self.debug = False
        self.s = GetDefaultSettings()
        if settings is not None:
            self.s.update(settings)
        # Set up graphical stuff
        translate(x, y)
        if self.s["draw_center"]:
            d = D*self.s["draw_center"]
            push()
            lw = self.s["cross_linewidth"]*self.D
            LineWidth(lw)
            line(0, 0, d, 0)
            line(0, 0, 0, -d)
            line(0, 0, 0, d)
            line(0, 0, -d, 0)
            pop()
        if self.s["draw_baseline"]:
            to_degrees = self.degrees
            ao_deg = self.s["polar_angle_offset"]*to_degrees
            # Make sure angles are in degrees (because the g library uses
            # degrees for angle measure).
            start = fmod(arc_start*to_degrees + ao_deg, 360)
            stop = fmod(arc_end*to_degrees + ao_deg, 360)
            if self.s["clockwise"]:
                start, stop = stop, start
            if self.s["line_width"] is not None:
                LineWidth(self.s["line_width"])
            move(0, 0)
            if start == stop:
                # If the angles are the same, then make the arc a whole
                # circle.
                circle(2*self.radius)
            else:
                arc(2*self.radius, start, stop)
    def Debug(self, state=True):
        '''You can turn debugging on and off to have debugging information
        printed to stdout.
        '''
        self.debug = state
    def GetDimension(self, level, key):
        '''Return the appropriate dimension for the indicated key.  Note
        the units are in physical drawing units; they're not relative to
        the scale diameter.
        '''
        dim = self.s[key][0]*2*self.radius
        return self.s[key][level]*dim if level else dim
    def DrawUnlabeledTicks(self, level, tick_angles):
        '''level is 0, 1, 2, ... to define the tick length.  tick_angles is
        a sequence of numbers (angles in degrees) to draw the tick at.
        '''
        # We're assuming the origin of the polar coordinate system is at
        # the Cartesian Postscript origin.
        LineColor(self.s["tick_color"][level])
        LineType(self.s["tick_line_type"][level])
        LineCap(self.s["tick_line_cap"][level])
        lw = self.GetDimension(level, "tick_linewidth")
        LineWidth(lw)
        ao_deg = self.s["polar_angle_offset"]*self.degrees
        for angle in tick_angles:
            if not (self.arc_start <= angle <= self.arc_end):
                msg = "Bad tick angle = %s" % str(angle)
                print("tick_angles =", tick_angles)
                raise ValueError(msg)
            # Convert angle to radians
            angle_rad = (angle + ao_deg)*d2r
            angle_rad *= -1 if self.s["clockwise"] else 1
            c, s = cos(angle_rad), sin(angle_rad)
            x1, y1 = c*self.radius, s*self.radius  # First point of line
            length = self.GetDimension(level, "tick_length")
            if self.s["out"]:
                r = self.radius + length
            else:
                r = self.radius - length
            x2, y2 = c*r, s*r  # Second point of line
            line(x1, y1, x2, y2)
            if self.debug:
                dbg("level %d tick line at %s deg: " % (level, angle))
                dbg("(%.2g, %.2g) to (%.2g, %.2g)\n" %
                    (x1, y1, x2, y2))
    def DrawLabeledTicks(self, level, ticks, no_tick=False, font=None):
        '''level is 0, 1, 2, ... to define the tick length.  ticks is a
        dictionary with the key being the angle in degrees and the value
        being the string to place at that location:
 
            ticks = {
                angle1 : string1,
                angle2 : [string2, radius_offset, angle_offset],
            }
 
        The second form is used to relocate the label for a tick.
        radius_offset is a fraction of the circle's diameter, as usual.
 
        Note the strings are plotted along a circular arc starting at the
        indicated angle.  For the second form, the starting angle of the
        label is angle2 + angle_offset.
 
        If no_tick is True, the tick marks aren't made.
 
        If font is given, it will be used as an alternative font (e.g.,
        used to print gauge marks).  It must be of the form
        (font_name, size, color).
        '''
        push()
        s, D = self.s, self.D
        to_degrees = self.degrees
        ao_deg = self.s["polar_angle_offset"]*to_degrees
        if font is not None:
            TextName(font[0])
            TextColor(font[2])
            T = font[1]
        else:
            TextName(s["font_name"][level])
            TextColor(s["font_color"][level])
            T = self.GetDimension(level, "font_size")
        TextSize(T)
        # The following offsets are defined in the settings.  They apply
        # in addition to the offsets defined if ticks[tick] is a 3-tuple.
        r = s["radial_offset"][0]*D
        constant_radial_offset = r*s["radial_offset"][level] if level else r
        constant_angle_offset = s["angle_offset"][level]*to_degrees
        for tick in ticks:
            tick_angle = tick
            radial_offset = constant_radial_offset
            angle_offset = constant_angle_offset
            if isinstance(ticks[tick], str):
                tick_label = ticks[tick]
                r_offset, a_offset = 0, 0
            else:
                tick_label, r_offset, a_offset = ticks[tick]
            radial_offset = constant_radial_offset + r_offset
            angle_offset = constant_angle_offset + a_offset*to_degrees
            if not no_tick:
                self.DrawUnlabeledTicks(level, [tick_angle])
            # Now draw the label by putting the text on a circular arc.
            theta_deg = tick_angle + angle_offset + ao_deg
            # The radial location of the label is determined by the length
            # of the tick.
            tick_length = self.GetDimension(level, "tick_length")
            gap = tick_length/10  # So label doesn't touch tick
            if s["out"]:
                r = self.radius + tick_length + gap + radial_offset
            else:
                r = self.radius - tick_length - gap - radial_offset
                # The following is an empirical correction to get the
                # inside labels to cuddle against the baseline when the
                # radial offset is zero.
                r -= T*0.724
            assert(r > 0)
            diameter = 2*r
            move(0, 0)
            theta_deg *= -1 if s["clockwise"] else 1
            # If string starts with the escape character, switch to the
            # Symbol font.
            if tick_label and tick_label[0] == esc:
                t = tick_label[1:]
                push()
                TextName(Symbol)
                TextCircle(t, diameter, theta_deg)
                pop()
            else:
                TextCircle(tick_label, diameter, theta_deg)
        pop()
# xx DrawArrow is not working yet
#    def DrawArrow(self, level, point1, point2, size, style, polar=True,
#                  filled=True):
#        '''Draw an arrow starting at point1 = (r1, theta1) and going to
#        point2 = (r2, theta2).  The arrow is at point2.  The arrow's size
#        is controlled by the size parameter which is a tuple of (width,
#        length); both width and length are fractions of the scale's
#        diameter.  The current line and fill colors are used, as is the
#        linewidth setting.  The style parameter is an integer >= 0 and
#        controls the type of arrowhead drawn.  The level parameter is used
#        to get line widths and colors.  The arrowhead is filled if filled
#        is True.
#
#        The arrows are drawn so that the arrowhead can be filled or
#        unfilled (as the settings dictate).  Thus, if all you want is an
#        arrowhead, just make sure that point2 is inside the arrowhead (the
#        best way is to make it equal to point1).
#
#        If polar is False, then the points are in Cartesian coordinates
#        with the x coordinate first and the y coordinate second.
#
#        Styles:
#            0   Standard triangular arrow; base is size[0] and height is
#                size[1].
#            1   Same as 0 except end is open.
#            2   Circle on the end.
#        '''
#        raise Exception("Not working yet")
#        push()
#        if polar:
#            r, theta = point1
#            theta *= self.angle_to_radians
#            x1, y1 = r*cos(theta), r*sin(theta)
#            r, theta = point2
#            theta *= self.angle_to_radians
#            x2, y2 = r*cos(theta), r*sin(theta)
#        else:
#            x1, y1 = point1
#            x2, y2 = point2
#        distance, only_draw_arrowhead = hypot(x1 - x2, y1 - y2), False
#        theta_in_degrees = atan2(y2 - y1, x2 - x1)*180/pi
#        width, length = size
#        if distance < length:
#            only_draw_arrowhead = True
#        # Draw the arrowhead.  We do this by first translating to point2
#        # and rotating to make the arrow lie along the x axis.  Then we
#        # construct the appropriate path.
#        push()
#        translate(x2, y2)
#        rotate(theta_in_degrees)
#        if style == 0:  # Plain arrow
#            NewPath()
#            PathAdd(point2)
#            PathAdd((-length, -width/2))
#            PathAdd((-length, width/2))
#            PathClose()
#            p = GetPath()
#            DrawPath()
#            if filled:
#                FillColor(self.s["fill_color"][level])
#                FillPath(p)
#        elif style == 1:    # Open-end arrow
#            line(0, 0, -length, -width/2)
#            line(0, 0, -length, width/2)
#        elif style == 2:    # Circle
#            move(-length/2, 0)
#            push()
#            if filled:
#                FillOn()
#                FillColor(self.s["fill_color"][level])
#            circle(length/2)
#            pop()
#        else:
#            msg = "%d is bad style for arrowhead" % style
#            raise ValueError(msg)
#        pop()
#        if only_draw_arrowhead:
#            line(x1, y1, x2, y2)
#        pop()
#---------------------------------------------------------------------------
if __name__ == "__main__":
    'Run unit tests'
    def SetUp(file, orientation=landscape, units=mm):
        '''Convenience function to set up the drawing environment and
        return a file object to the output stream.
        '''
        ofp = open(file, "w")
        ginitialize(ofp, wrap_in_PJL=0)
        setOrientation(orientation, units)
        return ofp
    def DegreeScale(x, y, diameter, settings=None):
        push()
        translate(x, y)
        rotate(90)
        if settings is None:
            settings = GetDefaultSettings()
        cs = CircularScale(0, 0, diameter, 0, 360, settings)
        # Labeled ticks
        ticks, level, n, include_end = {}, 0, 360, 0
        for i in range(n//10 + include_end):
            ticks[10*i] = [str(10*i), 0.04, 0]
        cs.DrawLabeledTicks(0, ticks)
        # Unlabeled ticks every 5 degrees
        ticks, level = [], 1
        for i in range(0, n + include_end, 5):
            if i % 10 == 5:
                ticks.append(i)
        cs.DrawUnlabeledTicks(level, ticks)
        # Unlabeled ticks every degree
        ticks, level = [], 2
        for i in range(0, n + include_end, 1):
            if i and i % 10 not in (0, 5):
                ticks.append(i)
        cs.DrawUnlabeledTicks(level, ticks)
        # Draw an arrow for a demo
        #cs.DrawArrow(1, (-1, -1), (2, 2), (0.1, 0.2), 2)
        pop()
    ofp = SetUp("degree.ps")
    x, y, D = 140, 108, 150     # Dimensions in mm
    s = GetDefaultSettings()
    s["clockwise"] = True
    DegreeScale(x, y, D, s)
