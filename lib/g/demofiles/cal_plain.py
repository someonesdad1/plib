"""
Generate monthly calendars
    You must set the variables start_month, start_year, end_month, and
    end_year.  Then the program will produce one monthly calendar per page.

    The program works by finding the day of the week of the first day of
    the month.  Dummy days of 0 are prefixed to the list of days of the
    month.  When the box drawing routine finds a zero, it doesn't print a
    day for that box.

    The dictionary birthdays indicates special days to color in the
    calendar.  The keys are date strings of the form "14 Dec".  The
    dictionary's values are:

        value[0]  = a list of one or more colors to color the box.  If more
                    than one color is given, the colors are printed from top
                    to bottom.  Note these colors are given indirectly by
                    using the string for the relationship of the people in
                    the box.  Thus, specifying "Child" will cause the program
                    to get the color associated with "Child" in the legend
                    dictionary.

        value[1:] = Names of the people to print in this box.

    If you set birthdays to the empty dictionary, no birthday information
    will be printed.

    Note:  the default values cause the current year to be output.  The range
    goes to January of the following year because GSView has a bug that causes
    the last page to not be put in the PDF file when converting the Postscript
    file to PDF.
"""

import pdb, sys, string, time
from g import *

# The values are a list of the colors to print in each box (indexes into
# the dictionary legend) and the names of the people to print in that box.
# A birthdate has to be written with the day number, one space character,
# then the month with the first character capitalized.
birthdays = {}
# The following dictionary helps us print a legend at the bottom
# of each page that ties color to relationship.  The colors should
# be chosen along with font_color so that the names can all be read
# against the colored backgrounds.
legend = {}
# The names will be printed in this color
font_color = black
# Specify the starting and ending months
start_month = 1
start_year = int(time.strftime("%Y"))
end_month = 1
end_year = start_year + 1
# This assumes letter size paper in landscape
page_width = 11
page_height = 8.5
# Colors
page_background = white
title_color = black
weekday_color = black
day_font_color = black
birthday_color = red
box_line_color = black
box_fill_color = white
box_font_color = black
# Title characteristics
x_title = 4.5
y_title = 7.7
title_size = 0.4
title_font = HelveticaBold
weekday_font = HelveticaBold
weekday_font_size = 0.3
# The following point defines the upper left corner of the calendar box
x_margin = 0.65
y_margin = 1.5
day_font = HelveticaBold
day_font_size = 0.2
box_width = 11.0 / 8
box_height = 1.2
x_day_offset = 0.1
y_day_offset = 0.2
day_size = 0.3
y_day_names = 7.5
box_line_width = 0.01
if 1:  # Date routines

    def JulianAstro(month, day, year):
        """Julian day routine from Meeus, "Astronomical Formulae for Calculators".
        Also in Meeus, "Astronomical Algorithms", 2nd ed., Willman-Bell, 1998.
        """
        if not IsValidDate(month, day, year):
            raise "Invalid date"
        if month < 3:
            year = year - 1
            month = month + 12
        julian = int(365.25 * year) + int(30.6001 * (month + 1)) + day + 1720994.5
        tmp = year + month / 100.0 + day / 10000.0
        if tmp >= 1582.1015:
            A = year // 100
            B = 2 - A + A // 4
            julian = julian + B
        return julian * 1.0

    def DayOfWeek(month, day, year):
        """Sunday = 0"""
        julian = int(JulianAstro(month, int(day), year) + 1.5)
        return julian % 7

    def IsLeapYear(year):
        if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
            return 1
        else:
            return 0

    def IsValidDate(month, day, year):
        """Returns true if the year is later than 1752 and the month and day
        numbers are valid.
        """
        if month < 1 or month > 12:
            return 0
        if int(month) != month:
            return 0
        if year < 1753:
            return 0
        if day < 1.0:
            return 0
        if int(day) != day:
            if month == 2:
                if IsLeapYear(year):
                    if day >= 30.0:
                        return 0
                else:
                    if day >= 29.0:
                        return 0
            elif month == 9 or month == 4 or month == 6 or month == 11:
                if day >= 31.0:
                    return 0
            else:
                if day >= 32.0:
                    return 0
        else:
            if month == 2:
                if IsLeapYear(year):
                    if day >= 29:
                        return 0
                else:
                    if day >= 28:
                        return 0
            elif month == 9 or month == 4 or month == 6 or month == 11:
                if day >= 30:
                    return 0
            else:
                if day >= 31:
                    return 0
        return 1

    def NumDaysInMonth(month, year):
        days = {
            1: 31,
            2: 28,
            3: 31,
            4: 31,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }
        days_in_month = days[month]
        if month == 2 and IsLeapYear(year):
            days_in_month = days_in_month + 1
        return days_in_month


def GetDays(month, year):
    """Return a list of the days in the month, padded by leading zeroes,
    which represent empty boxes in the first week.
    """
    days = list(range(1, NumDaysInMonth(month, year) + 1))
    for ix in range(DayOfWeek(month, 1, year)):
        days = [0] + days
    return days


def FillBirthdayColors(color_list, width, height):
    """color_list is a list of strings that name the color to use in
    the legend dictionary.  The box is assumed to go from (0, 0) to (-1, -1).
    Fill it with len(color_list) different colors.
    """
    push()
    assert len(color_list) > 0
    num_boxes = float(len(color_list))
    fillOn()
    lineOff()
    for ix in range(len(color_list)):
        color = legend[color_list[ix]]
        x = 0
        y = ix / num_boxes
        fillColor(color)
        move(x, -y)
        rectangle(1.0, -1.0 / num_boxes)
    pop()


def WriteNamesInBox(names, width, height):
    """names is a list of strings to print in a box that goes from (0, 0)
    to (width, -height).
    """
    push()
    assert len(names) > 0
    # Set font height to be a fraction of what we drew the day number with
    textSize(0.6 * day_font_size)
    for ix in range(len(names)):
        x = x_day_offset
        y = 1.5 * y_day_offset + ix * day_font_size * 0.75
        move(x, -y)
        text(names[ix])
    pop()


def PrintDay(x, y, day, month, width, height, day_fill_color, box_fill_color):
    """Draw the box for this day number and place the day number in the
    top left corner of the box.  The point (x, y) is the upper left
    corner of the box and we have a right-handed coordinate system.

    Return a dictionary of the color keys used to fill the box, so that
    we can make sure we print a legend for these colors at the bottom of
    the page.
    """
    push()
    translate(x, y)  # Make upper left corner of box the origin
    move(0, -height)
    fillOn()
    lineOn()
    lineWidth(box_line_width)
    colors_used = {}
    day_color = day_font_color
    # If it's a birthday day, change the fill color
    birthday = repr(day) + " " + month
    if birthday in birthdays:
        push()
        color_list = birthdays[birthday][0]
        for color in color_list:
            colors_used[color] = 0
        num_colors = len(color_list)
        assert num_colors > 0
        names = birthdays[birthday][1:]
        # Fill the box with the different colors given.  We scale to make
        # the box go from (0,0) to (-1, -1).
        scale(width, height)
        FillBirthdayColors(color_list, width, height)
        WriteNamesInBox(names, width, height)
        pop()
        # Make sure the box has a line around it
        lineOn()
        fillOff()
        lineColor(box_line_color)
        move(0, 0)
        rectangle(width, -height)
        day_color = birthday_color
    else:
        fillColor(box_fill_color)
        rectangle(width, height)
    move(x_day_offset, -y_day_offset)
    textColor(day_color)
    if day != 0:
        text(repr(day))
    pop()
    return colors_used


def ProcessMonth(month, year):
    """Generate a calendar page."""
    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    days = GetDays(month, year)
    # Color the background of the page
    fillColor(page_background)
    move(0, 0)
    lineOff()
    fillOn()
    rectangle(page_width, page_height)
    lineOn()
    # Title
    fillOn()
    textColor(title_color)
    textName(title_font)
    textSize(title_size)
    move(x_title, y_title)
    month_name = months[month - 1]
    text(month_name + " " + repr(year))
    # Weekday names
    textName(weekday_font)
    textSize(weekday_font_size)
    textColor(weekday_color)
    for ix in range(7):
        x = x_margin + ix * box_width + 0.5
        y = y_day_names - 0.4
        move(x, y)
        text(day_names[ix])
    # If we're going to have 6 rows of boxes, then we need to reduce the
    # box height a little.
    height = box_height
    num_days = len(days)
    num_rows = num_days // 7 + 1
    if num_rows == 6 and num_days % 7 != 0:
        height = height * 5.0 / 6
    # Print each day
    fillColor(box_fill_color)
    lineColor(box_line_color)
    textName(day_font)
    textColor(box_font_color)
    textSize(day_font_size)
    colors = {}  # Keep track of colors used in this month for legend
    for day_index in range(len(days)):
        row, col = divmod(day_index, 7)
        day = days[day_index]
        x = x_margin + box_width * (day_index % 7)
        y = page_height - y_margin - height * (day_index // 7)
        colors_used = PrintDay(
            x,
            y,
            day,
            month_name,
            box_width,
            height,
            day_font_color,
            box_fill_color,
        )
        for key in colors_used.keys():
            colors[key] = 0
    # DrawLegend(colors)


def DrawLegend(colors):
    """Put a legend at the bottom of the page for the colors in the colors
    dictionary.
    """
    for key in colors.keys():
        colors[key] = legend[key]
    legends = list(colors.keys())
    legends.sort()
    column_spacing = 1.5
    num_columns = 6
    row_spacing = 0.25
    width = 0.3
    height = 0.2
    x_offset = 0.8
    y_offset = 0.8
    font_size = 0.15
    lineColor(black)
    textColor(black)
    textSize(font_size)
    lineWidth(box_line_width)
    for ix in range(len(legends)):
        row, column = divmod(ix, num_columns)
        relationship = legends[ix]
        color = legend[relationship]
        x = x_margin + x_offset + column * float(column_spacing)
        y = y_margin - y_offset - row * row_spacing
        move(x, y)
        fillColor(color)
        rectangle(width, height)
        move(x + 1.1 * width, y + height / 2.0 - font_size / 3.0)
        text(relationship)


if __name__ == "__main__":
    assert end_year >= start_year
    year = start_year
    month = start_month
    done = 0
    os = open("out/cal_plain.ps", "w")
    ginitialize(os)
    setOrientation(landscape, inches)
    while not done:
        if (year == end_year) and (month == end_month):
            done = 1
        ProcessMonth(month, year)
        if not done:
            newPage()
        month = month + 1
        if month > 12:
            month = 1
            year = year + 1
