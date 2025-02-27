"""
Design a socket holder block.  See socket_holder.pdf documentation.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2020 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Design a socket holder block
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import os
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
if 1:  # Global variables
    # The following string defines your socket data and block design.
    # Dimensions are in mils.  The fields are
    #   Socket size string (size in following table is in mm)
    #   Diameter of socket
    #   S (measured height of socket)
    #   z (additional offset of special sockets)
    #   D (drill diameter you'll use for this socket)
    # Note the diameter isn't used except it helps you pick the drill diameter.
    if 1:
        data = """
            9   680     2100    0       750
           10   680     2100    250     750
           11   680     2100    0       750
           12   680     2100    0       750
           13   680     2100    250     875
           14   802     2380    0       875
           15   833     2380    250     875
           16   895     2380    0       1000
           17   958     2620    0       1000
           18   991     2620    0       1000
           19   1052    2620    250     1125
        """
        # Other variables needed
        Δ = 700  # Height of normal sockets above block
        H = 2000  # Height of block (not used, but documents the design)
        a = 200  # Distance from bottom of longest hole to block bottom
        b = 200  # Distance between hole edges
        project = "Snap-On 3/8 drive 6 point deep impact socket set 6 Mar 2020"
        edge_offset = 250  # Distance from block edge to first hole's nearest edge


def ReadData():
    d = []
    # Convert globals from mils to inches
    global Δ, H, a, b, edge_offset
    Δ /= 1000
    H /= 1000
    a /= 1000
    b /= 1000
    edge_offset /= 1000
    # Read in data
    for line in data.strip().split("\n"):
        name, dia, S, z, drill = line.split()
        dia, S, z, drill = [float(i) / 1000 for i in (dia, S, z, drill)]
        d.append((name, dia, S, z, drill))
    return d


def Report(holes):
    print(
        dedent(f"""
    Socket block design (dimensions in inches)
      Project:  {project}
      Variables:
        Δ = {Δ} = height of normal sockets above block
        H = {H} = height of block (not used, but documents the design)
        a = {a} = distance from bottom of longest hole to block bottom
        b = {b} = distance between hole edges
    
    Output:
        x = distance of hole center from edge of block
        Δx = distance from previous hole center
    """)
    )
    x = edge_offset
    last_x = 0
    print(
        dedent("""             
                                        Drill    Drill
      Socket         x          Δx      depth   Diameter
    ----------    -------    -------    -----   --------""")
    )
    for name, dia, S, z, drill in holes:
        radius = drill / 2
        x += radius  # Center of current hole
        rel_x = x - last_x
        depth = S - Δ - z
        print(
            f"{name:^10s}   {x:^10.2f}  {x - last_x:^8.2f}   "
            f"{depth:^7.2f}  {drill:^7.3f}"
        )
        last_x = x
        x += radius + b


if __name__ == "__main__":
    holes = ReadData()
    Report(holes)
