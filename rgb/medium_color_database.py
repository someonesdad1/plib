import sys
if 1:
    import debug
    debug.SetDebugger()
attr = f'''
file = {sys.argv[0]}
from http://www.two4u.com/color/medium-txt.html
Downloaded Sat 04 Oct 2014 10:53:39 AM
Verified Wed 16 Mar 2022 02:15:37 PM
'''.strip()
data = '''
White                     #FFFFFF     255  255  255
Red                       #FF0000     255    0    0
Green                     #00FF00       0  255    0
Blue                      #0000FF       0    0  255
Magenta                   #FF00FF     255    0  255
Cyan                      #00FFFF       0  255  255
Yellow                    #FFFF00     255  255    0
Black                     #000000       0    0    0
Aquamarine                #70DB93     112  219  147
Baker's Chocolate         #5C3317      92   51   23
Blue Violet               #9F5F9F     159   95  159
Brass                     #B5A642     181  166   66
Bright Gold               #D9D919     217  217   25
Brown                     #A62A2A     166   42   42
Bronze                    #8C7853     140  120   83
Bronze II                 #A67D3D     166  125   61
Cadet Blue                #5F9F9F      95  159  159
Cool Copper               #D98719     217  135   25
Copper                    #B87333     184  115   51
Coral                     #FF7F00     255  127    0
Corn Flower Blue          #42426F      66   66  111
Dark Brown                #5C4033      92   64   51
Dark Green                #2F4F2F      47   79   47
Dark Green Copper         #4A766E      74  118  110
Dark Olive Green          #4F4F2F      79   79   47
Dark Orchid               #9932CD     153   50  205
Dark Purple               #871F78     135   31  120
Dark Slate Blue           #6B238E     107   35  142
Dark Slate Grey           #2F4F4F      47   79   79
Dark Tan                  #97694F     151  105   79
Dark Turquoise            #7093DB     112  147  219
Dark Wood                 #855E42     133   94   66
Dim Grey                  #545454      84   84   84
Dusty Rose                #856363     133   99   99
Feldspar                  #D19275     209  146  117
Firebrick                 #8E2323     142   35   35
Flesh                     #F5CCB0     245  204  176
Forest Green              #238E23      35  142   35
Gold                      #CD7F32     205  127   50
Goldenrod                 #DBDB70     219  219  112
Grey                      #C0C0C0     192  192  192
Green Copper              #527F76      82  127  118
Green Yellow              #93DB70     147  219  112
Hunter Green              #215E21      33   94   33
Indian Red                #4E2F2F      78   47   47
Khaki                     #9F9F5F     159  159   95
Light Blue                #C0D9D9     192  217  217
Light Grey                #A8A8A8     168  168  168
Light Steel Blue          #8F8FBD     143  143  189
Light Wood                #E9C2A6     233  194  166
Lime Green                #32CD32      50  205   50
Mandarian Orange          #E47833     228  120   51
Maroon                    #8E236B     142   35  107
Medium Aquamarine         #32CD99      50  205  153
Medium Blue               #3232CD      50   50  205
Medium Forest Green       #6B8E23     107  142   35
Medium Goldenrod          #EAEAAE     234  234  174
Medium Orchid             #9370DB     147  112  219
Medium Sea Green          #426F42      66  111   66
Medium Slate Blue         #7F00FF     127    0  255
Medium Spring Green       #7FFF00     127  255    0
Medium Turquoise          #70DBDB     112  219  219
Medium Violet Red         #DB7093     219  112  147
Medium Wood               #A68064     166  128  100
Midnight Blue             #2F2F4F      47   47   79
Navy Blue                 #23238E      35   35  142
Neon Blue                 #4D4DFF      77   77  255
Neon Pink                 #FF6EC7     255  110  199
New Midnight Blue         #00009C       0    0  156
New Tan                   #EBC79E     235  199  158
Old Gold                  #CFB53B     207  181   59
Orange                    #FF7F00     255  127    0
Orange Red                #FF2400     255   36    0
Orchid                    #DB70DB     219  112  219
Pale Green                #8FBC8F     143  188  143
Pink                      #BC8F8F     188  143  143
Plum                      #EAADEA     234  173  234
Quartz                    #D9D9F3     217  217  243
Rich Blue                 #5959AB      89   89  171
Salmon                    #6F4242     111   66   66
Scarlet                   #8C1717     140   23   23
Sea Green                 #238E68      35  142  104
Semi-Sweet Chocolate      #6B4226     107   66   38
Sienna                    #8E6B23     142  107   35
Silver                    #E6E8FA     230  232  250
Sky Blue                  #3299CC      50  153  204
Slate Blue                #007FFF       0  127  255
Spicy Pink                #FF1CAE     255   28  174
Spring Green              #00FF7F       0  255  127
Steel Blue                #236B8E      35  107  142
Summer Sky                #38B0DE      56  176  222
Tan                       #DB9370     219  147  112
Thistle                   #D8BFD8     216  191  216
Turquoise                 #ADEAEA     173  234  234
Very Dark Brown           #5C4033      92   64   51
Very Light Grey           #CDCDCD     205  205  205
Violet                    #4F2F4F      79   47   79
Violet Red                #CC3299     204   50  153
Wheat                     #D8D8BF     216  216  191
Yellow Green              #99CC32     153  204   50
'''.strip()
print(f"""'''{attr}'''""")
for i, line in enumerate(data.split("\n")):
    name, color = line.split("#")
    color = color.split()[0].lower()
    name = name.strip()
    print(f"{name}, #{color}")
print()
