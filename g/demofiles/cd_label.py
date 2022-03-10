'''
This example constructs a letter-sized drawing that could be used to
print CD labels.  Two CD labels will be drawn on the sheet.  The top
left one demonstrates writing text along a circle.  The bottom right
one demonstrates writing text along a path and filling the CD area 
with a picture.

This examples requires that you have the PIL module installed.
'''
import sys
from g import *
# Set the following variable to nonzero if you want to send the generated
# files directly to a PostScript printer.  Otherwise, set it to zero.
def DrawPlainCD(x_center, y_center):
    '''Draws a CD label around the indicated point.  Fill the CD with a
    plain color.  Assumes the units are mm.
    '''
    push()
    translate(x_center, y_center)
    lineWidth(0.1)
    move(0, 0)
    # Set a path that contains the inside of the CD label area
    newPath()
    pathAdd((0, 0, 130.0 / 2, 0, 360), path_arc_ccw)
    pathClose()
    pathAdd((0, 0, 40.0 / 2, 0, 360), path_arc_ccw)
    pathClose()
    p = getPath()
    # Fill the path with a gradient fill
    fillOn()
    fillType(gradient_fill)
    color1 = hsv2rgb(0.8, 0.5, 0.95)
    color2 = hsv2rgb(0.1, 0.5, 0.95)
    fillColor(color1)
    gradientFill(color2, 45)
    eofillPath(p)
    # Label with some strings
    textColor(blue)
    textName(SansBold)
    textSize(10)
    textCircle("Placing text on a circle", 85)
    textName(Sans)
    textSize(8)
    textCircle(
        "Use the textCircle() command", 80, center_angle=270, inside=yes
    )
    # Put a small string all the way around at the ID
    str = "You can also put text in a small font practically all the way "
    str = str + "around the ID if the string is long enough..."
    textName(Sans)
    textSize(3)
    textCircle(str, 42)
    pop()
def DrawPictureCD(picture_file, x_center, y_center):
    '''Draw a CD label by first filling with the indicated picture, then
    writing some text, using both text on a circle and text on a path.
    Note that the positioning and size of the picture will have to be
    hand-tweaked; see the comments below.
    '''
    od = 130.0
    id = 40.0
    push()
    translate(x_center, y_center)
    scale(-1, -1)  # Make the image right-side up
    lineWidth(0.1)
    move(0, 0)
    # Set a path that contains the inside of the CD label area
    newPath()
    pathAdd((0, 0, od / 2, 0, 360), path_arc_ccw)
    pathClose()
    pathAdd((0, 0, id / 2, 0, 360), path_arc_ccw)
    pathClose()
    p = getPath()
    newPath()
    # Clip to this path and fill it with the picture.  Note we have to
    # use even-odd clipping to remove the center region from the path.
    # You'll find that you'll have to fiddle with the positioning and
    # size of the picture to get it to fit the way you want in the
    # annular region.  I recommend you turn clipping off to show the
    # whole picture in relation to the annular area -- set debug to
    # yes to do this.
    debug = no
    if debug == no:
        eoclip(p)
    # Darken the image
    from PIL import Image, ImageEnhance
    im = Image.open(picture_file)
    enh = ImageEnhance.Brightness(im)
    new_image = enh.enhance(0.5)
    # Place the image within the CD area
    move(-65, -72)
    c = od * 1.3
    picture(new_image, c, c)
    # A hack needed for python 2.2.  I haven't figured out what broke
    # yet.  Note you may also need to remove the gsize command from
    # the PIL file PSDraw.py (I had to so that ghostscript would not
    # generate an error on the output).
    print("cd_label.py:  Warning - hacked for python 2.2...")
    print("  You may need to remove gsize from the PIL file PSDraw.py.")
    translate(72, 205)
    rotate(180)
    # Fill it with a 1 cm cross hatching
    fillOn()
    fillColor(grey(0.4))
    fillType(line_fill)
    lineFillWidth(0.05)
    sep = 10
    lineFill(45, sep)
    fillPath(p)
    lineFill(135, sep)
    fillPath(p)
    drawPath(p)
    # Draw some text along a bezier
    newPath()
    move(-50, 0)
    pathAdd((-40, 50, 0, 25, 50, 50), path_bezier)
    p = getPath()
    textColor(yellow)
    textName(SansBold)
    textSize(6)
    textPath("This is some text along a bezier curve", p)
    newPath()
    move(0, 0)
    textCircle(
        "Use the textPath() command for text on a path",
        100,
        center_angle=270,
        inside=yes,
    )
    pop()
def DrawBoxes():
    '''Draw some boxes with text in them.'''
    push()
    translate(20, 20)
    rotate(90)
    textSize(6)
    textColor(red)
    lines = [
        "Shows gradient fills, text along a path,",
        "clipping to a path, and bitmap manipulations.",
    ]
    move(0, 0)
    textLines(lines)
    lineColor(navy)
    lineWidth(2)
    move(-3, -12)
    roundedRectangle(125, 20, 5)
    pop()
def CD_Label(file):
    '''Show the use of drawing text in a circle by making a simple label
    for a CD.  A CD is 40 mm inside diameter and 130 mm outside
    diameter.  On the labels that I use, the center of the upper CD
    label is at the position(72, 205); there are two CD labels on each
    8.5 inch by 11 inch sheet and they are in opposite diagonal corners.
    My first way of plotting these labels was to plot the first one at
    the indicated position, then plot the second one at the center
    (8.5"-72 mm, 11"-205 mm).  This assumes the page is exactly
    letter-sized (8.5 inch by 11 inch).

    A little thought showed me I could reduce the location uncertainty a
    bit by plotting the second label in inverse portrait mode; this
    makes the label upside-down with respect to the first image.  This
    is fixed by a reflection in both the x and y axes.  This scheme
    locates the labels consistently with respect to the left edge of the
    paper, but the vertical location of the centers is dependent on how
    close the label stock is to the assumed 11 inch height.
    '''
    s = Setup(file, portrait, mm)  # Note units are mm
    x_label_center, y_label_center = 72, 205
    DrawBoxes()
    DrawPlainCD(x_label_center, y_label_center)
    setOrientation(inversePortrait, mm)
    file = "pics/face1.jpg"
    DrawPictureCD(file, x_label_center, y_label_center)
    s.close()
CD_Label("out/cd_label.ps")
