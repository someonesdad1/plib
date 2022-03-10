'''
Show rounded rectangles
'''
from g import *
import random
import sys
rand = random.random() # Convenience name for a random number generator that 
                       # returns a uniformly-distributed random number between
                       # 0.0 and 1.0.
def RoundedRectangle(file):
    '''Show rectangles with rounded corners.  Vary the corner diameter and
    print it in the center of the rectangle.
    '''
    s = SetUp(file, portrait, inches)
    lineWidth(0.05)
    fillColor(lightblue)
    lineColor(navy)
    textColor(red)
    fillOn()
    # Print a title
    textName(HelveticaBold)
    text_size = 0.2
    textSize(text_size)
    y = 10.5
    move(0.5, y)
    text(
        "Rounded rectangles:  the number in the box is the corner diameter"
    )
    move(0.5, y - text_size * 1.2)
    text("as a percentage of the box height.")
    text_size = 0.4
    textSize(text_size)
    num_rows = 5
    num_columns = 3
    num_boxes = num_rows * num_columns
    page_width = 8.5  # Letter size paper
    page_height = 11
    left_margin = 0.5
    right_margin = 0
    top_margin = 0.5
    bottom_margin = 0.5
    x_box_sep = 0.5
    y_box_sep = 0.5
    column_width = (page_width - left_margin - right_margin) / float(
        num_columns
    )
    row_height = (page_height - bottom_margin - top_margin) / float(
        num_rows
    )
    box_width = column_width - x_box_sep
    box_height = row_height - y_box_sep
    max_corner_diameter = box_height
    for row in range(num_rows):
        for column in range(num_columns):
            boxnum = column * num_rows + row
            x_corner = left_margin + column * column_width
            y_corner = bottom_margin + row * row_height
            x_text = x_corner + 0.35 * box_width
            y_text = y_corner + 0.43 * box_height
            move(x_corner, y_corner)
            corner_diameter = (
                max_corner_diameter * boxnum / (num_boxes - 1)
            )
            roundedRectangle(box_width, box_height, corner_diameter)
            move(x_text, y_text)
            percent = int(100.0 * corner_diameter / max_corner_diameter)
            text("%3d" % percent)
    s.close()
RoundedRectangle("out/rounded_rect.ps")
