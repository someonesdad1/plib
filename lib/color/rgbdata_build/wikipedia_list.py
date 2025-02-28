"""
This script will get rid of the cruft and print out a table of the color
names and six digit hex number for the RGB values.
"""

import sys

if 1:
    import debug

    debug.SetDebugger()
import re

attr = f"""
file = {sys.argv[0]}
Text of the first three web pages at
https://en.wikipedia.org/wiki/Lists_of_colors
Downloaded Tue 01 Jun 2021 07:08:24 PM
""".strip()
data = """
Absolute Zero
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Extreme_Twistables_colors>
	#0048BA 	0% 	28% 	73% 	217° 	100% 	37% 	100% 	73%
Acid green <https://en.wikipedia.org/wiki/Acid_green> 	#B0BF1A 	69%
75% 	10% 	65° 	76% 	43% 	76% 	43%
Aero <https://en.wikipedia.org/wiki/Air_Force_blue#Aero> 	#7CB9E8
49% 	73% 	91% 	206° 	70% 	70% 	47% 	91%
Aero blue <https://en.wikipedia.org/wiki/Aero_blue> 	#C0E8D5 	75%
91% 	84% 	151.5° 	47% 	83% 	17.2% 	91%
African violet <https://en.wikipedia.org/wiki/African_violet_(color)>
#B284BE 	70% 	52% 	75% 	288° 	31% 	63% 	31% 	75%
Air superiority blue
<https://en.wikipedia.org/wiki/Air_Force_blue#Air_superiority_blue/PRU_blue>
	#72A0C1 	45% 	63% 	76% 	205° 	39% 	60% 	41% 	76%
Alabaster <https://en.wikipedia.org/wiki/Shades_of_white#Alabaster>
#EDEAE0 	93% 	92% 	88% 	50° 	27% 	90% 	6% 	93%
Alice blue <https://en.wikipedia.org/wiki/Alice_blue> 	#F0F8FF 	94%
97% 	100% 	208° 	100% 	97% 	6% 	100%
Alloy orange
<https://en.wikipedia.org/wiki/Shades_of_orange#Alloy_orange>
#C46210 	77% 	38% 	6% 	27° 	85% 	42% 	92% 	77%
Almond <https://en.wikipedia.org/wiki/Almond_(color)> 	#EFDECD 	94%
87% 	80% 	30° 	52% 	87% 	14% 	94%
Amaranth <https://en.wikipedia.org/wiki/Amaranth_(color)> 	#E52B50
90% 	17% 	31% 	348° 	78% 	53% 	81% 	90%
Amaranth (M&P)
<https://en.wikipedia.org/wiki/Amaranth_(color)#Amaranth_deep_purple>
#9F2B68 	62% 	17% 	41% 	328° 	57% 	40% 	73% 	62%
Amaranth pink
<https://en.wikipedia.org/wiki/Amaranth_(color)#Amaranth_pink>
#F19CBB 	95% 	61% 	73% 	338° 	75% 	78% 	35% 	95%
Amaranth purple
<https://en.wikipedia.org/wiki/Amaranth_(color)#Amaranth_purple>
#AB274F 	67% 	15% 	31% 	342° 	63% 	41% 	77% 	67%
Amaranth red <https://en.wikipedia.org/wiki/Amaranth_(color)>
#D3212D 	83% 	13% 	18% 	356° 	73% 	48% 	84% 	83%
Amazon <https://en.wikipedia.org/wiki/Amazon_(color)> 	#3B7A57 	23%
48% 	34% 	147° 	35% 	36% 	52% 	48%
Amber <https://en.wikipedia.org/wiki/Amber_(color)> 	#FFBF00 	100%
75% 	0% 	45° 	100% 	50% 	100% 	100%
Amber (SAE/ECE)
<https://en.wikipedia.org/wiki/Amber_(color)#SAE/ECE_amber> 	#FF7E00
100% 	49% 	0% 	30° 	100% 	50% 	100% 	100%
Amethyst <https://en.wikipedia.org/wiki/Amethyst_(color)> 	#9966CC
60% 	40% 	80% 	270° 	50% 	60% 	50% 	80%
Android green <https://en.wikipedia.org/wiki/Android_green> 	#3DDC84
24% 	86% 	53% 	148° 	69% 	55% 	72% 	86%
Antique brass <https://en.wikipedia.org/wiki/Antique_brass> 	#CD9575
80% 	58% 	46% 	22° 	47% 	63% 	43% 	80%
Antique bronze <https://en.wikipedia.org/wiki/Antique_bronze>
#665D1E 	40% 	36% 	12% 	53° 	55% 	26% 	71% 	40%
Antique fuchsia
<https://en.wikipedia.org/wiki/Fuchsia_(color)#Antique_fuchsia>
#915C83 	57% 	36% 	51% 	316° 	22% 	46% 	37% 	57%
Antique ruby <https://en.wikipedia.org/wiki/Ruby_(color)#Antique_ruby>
#841B2D 	52% 	11% 	18% 	350° 	66% 	31% 	80% 	52%
Antique white
<https://en.wikipedia.org/wiki/Shades_of_white#Antique_white>
#FAEBD7 	98% 	92% 	84% 	34° 	78% 	91% 	14% 	98%
Ao (English) <https://en.wikipedia.org/wiki/Ao_(color)> 	#008000 	0%
50% 	0% 	120° 	100% 	25% 	100% 	50%
Apple green
<https://en.wikipedia.org/wiki/Chartreuse_(color)#Apple_green>
#8DB600 	55% 	71% 	0% 	74° 	100% 	36% 	100% 	71%
Apricot <https://en.wikipedia.org/wiki/Apricot_(color)> 	#FBCEB1
98% 	81% 	69% 	24° 	90% 	84% 	29% 	98%
Aqua <https://en.wikipedia.org/wiki/Aqua_(color)> 	#00FFFF 	0% 	100%
100% 	180° 	100% 	50% 	100% 	100%
Aquamarine <https://en.wikipedia.org/wiki/Aquamarine_(color)>
#7FFFD4 	50% 	100% 	83% 	160° 	100% 	75% 	50% 	100%
Arctic lime <https://en.wikipedia.org/wiki/Lime_(color)#Arctic_lime>
#D0FF14 	82% 	100% 	8% 	72° 	100% 	54% 	92% 	100%
Army green <https://en.wikipedia.org/wiki/Shades_of_green#Army_green>
#4B5320 	29% 	33% 	13% 	69° 	44% 	23% 	61% 	33%
Artichoke <https://en.wikipedia.org/wiki/Shades_of_green#Artichoke>
#8F9779 	56% 	59% 	47% 	76° 	13% 	53% 	20% 	59%
Arylide yellow <https://en.wikipedia.org/wiki/Arylide_yellow>
#E9D66B 	91% 	84% 	42% 	51° 	74% 	67% 	54% 	91%
Ash gray <https://en.wikipedia.org/wiki/Shades_of_gray#Ash_gray>
#B2BEB5 	70% 	75% 	71% 	135° 	8% 	72% 	6% 	75%
Asparagus <https://en.wikipedia.org/wiki/Shades_of_green#Asparagus>
#87A96B 	53% 	66% 	42% 	93° 	26% 	54% 	37% 	66%
Atomic tangerine
<https://en.wikipedia.org/wiki/Shades_of_orange#Atomic_tangerine>
#FF9966 	100% 	60% 	40% 	20° 	100% 	70% 	60% 	100%
Auburn <https://en.wikipedia.org/wiki/Auburn_(color)> 	#A52A2A 	65%
16% 	16% 	0° 	59% 	41% 	75% 	65%
Aureolin <https://en.wikipedia.org/wiki/Aureolin> 	#FDEE00 	99% 	93%
0% 	56° 	100% 	50% 	100% 	99%
Avocado <https://en.wikipedia.org/wiki/Chartreuse_(color)#Avocado>
#568203 	34% 	51% 	1% 	81° 	95% 	26% 	98% 	51%
Azure <https://en.wikipedia.org/wiki/Azure_(color)> 	#007FFF 	0%
50% 	100% 	210° 	100% 	50% 	100% 	100%
Azure (X11/web color)
<https://en.wikipedia.org/wiki/Shades_of_azure#Azure_(web_color)>
#F0FFFF 	94% 	100% 	100% 	180° 	100% 	97% 	6% 	100%
Baby blue <https://en.wikipedia.org/wiki/Baby_blue> 	#89CFF0 	54%
81% 	94% 	199° 	77% 	74% 	43% 	94%
Baby blue eyes
<https://en.wikipedia.org/wiki/Baby_blue#Baby_blue_eyes> 	#A1CAF1
63% 	79% 	95% 	209° 	74% 	79% 	33% 	95%
Baby pink <https://en.wikipedia.org/wiki/Shades_of_pink#Baby_pink>
#F4C2C2 	96% 	76% 	76% 	0° 	69% 	86% 	20% 	96%
Baby powder
<https://en.wikipedia.org/wiki/Shades_of_white#Baby_powder> 	#FEFEFA
100% 	100% 	98% 	60° 	67% 	99% 	2% 	100%
Baker-Miller pink <https://en.wikipedia.org/wiki/Baker-Miller_pink>
#FF91AF 	100% 	57% 	69% 	344° 	100% 	78% 	43% 	100%
Banana Mania
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#FAE7B5 	98% 	91% 	71% 	43° 	87% 	85% 	28% 	98%
Barbie Pink <https://en.wikipedia.org/wiki/Shades_of_pink#Barbie_pink>
#DA1884 	85% 	9% 	52% 	327° 	80% 	48% 	89% 	85%
Barn red <https://en.wikipedia.org/wiki/Shades_of_red#Barn_red>
#7C0A02 	49% 	4% 	1% 	4° 	97% 	25% 	98% 	49%
Battleship grey <https://en.wikipedia.org/wiki/Battleship_grey>
#848482 	52% 	52% 	51% 	60° 	1% 	51% 	2% 	52%
Beau blue <https://en.wikipedia.org/wiki/Baby_blue#Beau_blue>
#BCD4E6 	74% 	83% 	90% 	206° 	46% 	82% 	18% 	90%
Beaver <https://en.wikipedia.org/wiki/Shades_of_brown#Beaver>
#9F8170 	62% 	51% 	44% 	22° 	20% 	53% 	30% 	62%
Beige <https://en.wikipedia.org/wiki/Beige> 	#F5F5DC 	96% 	96% 	86%
60° 	56% 	91% 	10% 	96%
B'dazzled blue
<https://en.wikipedia.org/wiki/Sapphire_(color)#B'dazzled_blue>
#2E5894 	18% 	35% 	58% 	215° 	53% 	38% 	69% 	58%
Big dip o’ruby
<https://en.wikipedia.org/wiki/Ruby_(color)#Big_dip_o'ruby> 	#9C2542
61% 	15% 	26% 	345° 	62% 	38% 	76% 	61%
Bisque
<https://en.wikipedia.org/wiki/X11_color_names#Color_name_charts>
#FFE4C4 	100% 	89% 	77% 	33° 	100% 	88% 	23% 	100%
Bistre <https://en.wikipedia.org/wiki/Bistre> 	#3D2B1F 	24% 	17%
12% 	24° 	33% 	18% 	49% 	24%
Bistre brown <https://en.wikipedia.org/wiki/Bistre#Bistre_brown>
#967117 	59% 	44% 	9% 	43° 	73% 	34% 	85% 	59%
Bitter lemon
<https://en.wikipedia.org/wiki/Lemon_(color)#Bitter_lemon> 	#CAE00D
79% 	88% 	5% 	66° 	89% 	46% 	94% 	88%
Bitter lime <https://en.wikipedia.org/wiki/Lime_(color)> 	#BFFF00 	75%
100% 	0% 	75° 	100% 	50% 	100% 	100%
Bittersweet
<https://en.wikipedia.org/wiki/Shades_of_orange#Bittersweet>
#FE6F5E 	100% 	44% 	37% 	6° 	99% 	68% 	63% 	100%
Bittersweet shimmer
<https://en.wikipedia.org/wiki/Shades_of_orange#Bittersweet_shimmer>
#BF4F51 	75% 	31% 	32% 	359° 	47% 	53% 	59% 	75%
Black <https://en.wikipedia.org/wiki/Black> 	#000000 	0% 	0% 	0% 	—°
0% 	0% 	0% 	0%
Black bean <https://en.wikipedia.org/wiki/Shades_of_black#Black_bean>
#3D0C02 	24% 	5% 	1% 	10° 	94% 	12% 	97% 	24%
Black chocolate
<https://en.wikipedia.org/wiki/Shades_of_black#Black_chocolate>
#1B1811 	11% 	9% 	7% 	42° 	23% 	9% 	37% 	11%
Black coffee
<https://en.wikipedia.org/wiki/Shades_of_black#Black_coffee>
#3B2F2F 	23% 	18% 	18% 	0° 	11% 	21% 	20% 	23%
Black coral
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Pearl_Brite>
#54626F 	33% 	38% 	44% 	209° 	14% 	38% 	24% 	44%
Black olive <https://en.wikipedia.org/wiki/Olive_(color)#Black_olive>
#3B3C36 	23% 	24% 	21% 	70° 	5% 	22% 	10% 	24%
Black Shadows
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Heads_'n_Tails>
	#BFAFB2 	75% 	69% 	70% 	349° 	11% 	72% 	8% 	75%
Blanched almond <https://en.wikipedia.org/wiki/X11_color_names>
#FFEBCD 	100% 	92% 	80% 	36° 	100% 	90% 	20% 	100%
Blast-off bronze
<https://en.wikipedia.org/wiki/Bronze_(color)#Blast-off_bronze>
#A57164 	65% 	44% 	39% 	12° 	27% 	52% 	39% 	65%
Bleu de France <https://en.wikipedia.org/wiki/Bleu_de_France_(colour)>
#318CE7 	19% 	55% 	91% 	210° 	79% 	55% 	79% 	91%
Blizzard blue
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Fluorescent_crayons>
	#ACE5EE 	67% 	90% 	93% 	188° 	66% 	80% 	28% 	93%
Blond <https://en.wikipedia.org/wiki/Blond> 	#FAF0BE 	98% 	94% 	75%
50° 	86% 	86% 	24% 	98%
Blood red <https://en.wikipedia.org/wiki/Blood_red> 	#660000 	40%
0% 	0% 	0° 	100% 	20% 	100% 	40%
Blue <https://en.wikipedia.org/wiki/Blue> 	#0000FF 	0% 	0% 	100% 	240°
100% 	50% 	100% 	100%
Blue (Crayola)
<https://en.wikipedia.org/wiki/Shades_of_blue#Blue_(Crayola)>
#1F75FE 	12% 	46% 	100% 	217° 	99% 	56% 	88% 	100%
Blue (Munsell)
<https://en.wikipedia.org/wiki/Shades_of_blue#Blue_(Munsell)>
#0093AF 	0% 	58% 	69% 	190° 	100% 	34% 	100% 	69%
Blue (NCS)
<https://en.wikipedia.org/wiki/Shades_of_blue#Blue_(NCS)_(psychological_primary_blue)>
	#0087BD 	0% 	53% 	74% 	197° 	100% 	37% 	100% 	74%
Blue (Pantone)
<https://en.wikipedia.org/wiki/Shades_of_blue#Blue_(Pantone)>
#0018A8 	0% 	9% 	66% 	231° 	100% 	33% 	100% 	66%
Blue (pigment)
<https://en.wikipedia.org/wiki/Shades_of_blue#Blue_(CMYK)_(pigment_blue)>
#333399 	20% 	20% 	60% 	240° 	50% 	40% 	67% 	60%
Blue (RYB) <https://en.wikipedia.org/wiki/RYB_color_model> 	#0247FE
1% 	28% 	100% 	224° 	99% 	50% 	99% 	100%
Blue bell
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#A2A2D0 	64% 	64% 	82% 	240° 	33% 	73% 	22% 	82%
Blue-gray <https://en.wikipedia.org/wiki/Blue-gray> 	#6699CC 	40%
60% 	80% 	210° 	50% 	60% 	50% 	80%
Blue-green <https://en.wikipedia.org/wiki/Blue-green> 	#0D98BA 	5%
60% 	73% 	192° 	87% 	39% 	93% 	73%
Blue-green (color wheel)
<https://en.wikipedia.org/wiki/Blue-green#Blue-green_(color_wheel)>
#064E40 	2% 	31% 	25% 	168° 	86% 	17% 	92% 	31%
Blue jeans
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Heads_'n_Tails>
	#5DADEC 	36% 	68% 	93% 	206° 	79% 	65% 	61% 	93%
Blue sapphire
<https://en.wikipedia.org/wiki/Sapphire_(color)#Blue_sapphire>
#126180 	7% 	38% 	50% 	197° 	75% 	29% 	86% 	50%
Blue-violet
<https://en.wikipedia.org/wiki/Indigo#Deep_indigo_(web_color_blue-violet)>
	#8A2BE2 	54% 	17% 	89% 	271° 	76% 	53% 	81% 	89%
Blue-violet (Crayola) <https://en.wikipedia.org/wiki/Violet_(color)>
#7366BD 	45% 	40% 	74% 	249° 	40% 	57% 	46% 	74%
Blue-violet (color wheel)
<https://en.wikipedia.org/wiki/Violet_(color)> 	#4D1A7F 	30% 	10% 	50%
270° 	66% 	30% 	46% 	74%
Blue yonder <https://en.wikipedia.org/wiki/Air_Force_blue#Blue_yonder>
#5072A7 	31% 	45% 	65% 	217° 	35% 	48% 	52% 	65%
Bluetiful
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors>
#3C69E7 	24% 	41% 	91% 	224° 	78% 	57% 	74% 	91%
Blush <https://en.wikipedia.org/wiki/Red-violet#Blush> 	#DE5D83 	87%
36% 	51% 	342° 	66% 	62% 	58% 	87%
Bole <https://en.wikipedia.org/wiki/Bole_(color)> 	#79443B 	47% 	27%
23% 	9° 	34% 	35% 	51% 	47%
Bone <https://en.wikipedia.org/wiki/Shades_of_white#Bone> 	#E3DAC9
89% 	85% 	79% 	39° 	32% 	84% 	11% 	89%
Bottle green
<https://en.wikipedia.org/wiki/Shades_of_green#Bottle_green>
#006A4E 	0% 	42% 	31% 	164° 	100% 	21% 	100% 	42%
Brandy <https://en.wikipedia.org/wiki/Shades_of_brown#Brandy>
#87413F 	53% 	25% 	25% 	2° 	36% 	39% 	53% 	53%
Brick red
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#CB4154 	80% 	25% 	33% 	352° 	57% 	53% 	68% 	80%
Bright green
<https://en.wikipedia.org/wiki/Shades_of_green#Bright_green>
#66FF00 	40% 	100% 	0% 	96° 	100% 	50% 	100% 	100%
Bright lilac
<https://en.wikipedia.org/wiki/Lilac_(color)#Bright_lilac> 	#D891EF
85% 	57% 	94% 	285° 	75% 	75% 	39% 	94%
Bright maroon <https://en.wikipedia.org/wiki/Maroon#Bright_maroon>
#C32148 	76% 	13% 	28% 	346° 	71% 	45% 	83% 	76%
Bright navy blue
<https://en.wikipedia.org/wiki/Navy_blue#Bright_navy_blue> 	#1974D2
10% 	45% 	82% 	210° 	79% 	46% 	88% 	82%
Bright yellow (Crayola)
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Heads_'n_Tails>
	#FFAA1D 	100% 	67% 	11% 	37° 	100% 	56% 	89% 	100%
Brilliant rose
<https://en.wikipedia.org/wiki/Rose_(color)#Brilliant_rose> 	#FF55A3
100% 	33% 	64% 	332° 	100% 	67% 	67% 	100%
Brink pink <https://en.wikipedia.org/wiki/Rose_(color)#Brink_pink>
#FB607F 	98% 	38% 	50% 	348° 	95% 	68% 	62% 	98%
British racing green
<https://en.wikipedia.org/wiki/British_racing_green> 	#004225 	0%
26% 	15% 	154° 	100% 	13% 	100% 	26%
Bronze <https://en.wikipedia.org/wiki/Bronze_(color)> 	#CD7F32 	80%
50% 	20% 	30° 	61% 	50% 	76% 	80%
Brown <https://en.wikipedia.org/wiki/Brown> 	#88540B 	53% 	33% 	4%
35° 	85% 	29% 	92% 	53%
Brown sugar
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Heads_'n_Tails>
	#AF6E4D 	69% 	43% 	30% 	20° 	39% 	49% 	56% 	69%
Brunswick green
<https://en.wikipedia.org/wiki/Shades_of_green#Brunswick_green>
#1B4D3E 	11% 	30% 	24% 	162° 	48% 	20% 	65% 	30%
Bud green <https://en.wikipedia.org/wiki/Spring_bud#Bud_green>
#7BB661 	48% 	71% 	38% 	102° 	37% 	55% 	47% 	71%
Buff <https://en.wikipedia.org/wiki/Buff_(colour)> 	#FFC680 	100%
78% 	50% 	33° 	100% 	75% 	50% 	100%
Burgundy <https://en.wikipedia.org/wiki/Burgundy_(color)> 	#800020
50% 	0% 	13% 	345° 	100% 	25% 	100% 	50%
Burlywood
<https://en.wikipedia.org/wiki/X11_color_names#Color_name_charts>
#DEB887 	87% 	72% 	53% 	34° 	57% 	70% 	39% 	87%
Burnished brown
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Silver_Swirls>
	#A17A74 	63% 	48% 	45% 	8° 	19% 	54% 	28% 	63%
Burnt orange
<https://en.wikipedia.org/wiki/Shades_of_orange#Burnt_orange>
#CC5500 	80% 	33% 	0% 	25° 	100% 	40% 	100% 	80%
Burnt sienna <https://en.wikipedia.org/wiki/Burnt_sienna> 	#E97451
91% 	45% 	32% 	14° 	78% 	62% 	65% 	91%
Burnt umber <https://en.wikipedia.org/wiki/Burnt_umber> 	#8A3324
54% 	20% 	14% 	9° 	59% 	34% 	74% 	54%
Byzantine <https://en.wikipedia.org/wiki/Byzantium_(color)#Byzantine>
#BD33A4 	74% 	20% 	64% 	311° 	58% 	47% 	73% 	74%
Byzantium <https://en.wikipedia.org/wiki/Byzantium_(color)> 	#702963
44% 	16% 	39% 	311° 	46% 	30% 	63% 	44%
Cadet <https://en.wikipedia.org/wiki/Cadet_grey#Cadet> 	#536872 	33%
41% 	45% 	199° 	16% 	39% 	27% 	45%
Cadet blue <https://en.wikipedia.org/wiki/Cadet_grey#Cadet_blue>
#5F9EA0 	37% 	62% 	63% 	182° 	25% 	50% 	41% 	63%
Cadet blue (Crayola)
<https://en.wikipedia.org/wiki/Cadet_grey#Cadet_blue_(Crayola)>
#A9B2C3 	66% 	70% 	76% 	219° 	18% 	71% 	13% 	76%
Cadet grey <https://en.wikipedia.org/wiki/Cadet_grey> 	#91A3B0 	57%
64% 	69% 	205° 	16% 	63% 	18% 	69%
Cadmium green <https://en.wikipedia.org/wiki/Cadmium_pigments>
#006B3C 	0% 	42% 	24% 	154° 	100% 	21% 	100% 	42%
Cadmium orange <https://en.wikipedia.org/wiki/Cadmium_pigments>
#ED872D 	93% 	53% 	18% 	28° 	84% 	55% 	81% 	93%
Cadmium red <https://en.wikipedia.org/wiki/Cadmium_pigments>
#E30022 	89% 	0% 	13% 	351° 	100% 	45% 	100% 	89%
Cadmium yellow <https://en.wikipedia.org/wiki/Cadmium_pigments>
#FFF600 	100% 	96% 	0% 	58° 	100% 	50% 	100% 	100%
Café au lait
<https://en.wikipedia.org/wiki/Coffee_(color)#Caf%C3%A9_au_Lait>
#A67B5B 	65% 	48% 	36% 	26° 	30% 	50% 	45% 	65%
Café noir
<https://en.wikipedia.org/wiki/Coffee_(color)#Caf%C3%A9_Noir>
#4B3621 	29% 	21% 	13% 	30° 	39% 	21% 	56% 	29%
Cambridge blue <https://en.wikipedia.org/wiki/Cambridge_Blue_(colour)>
#A3C1AD 	64% 	76% 	68% 	140° 	19% 	70% 	16% 	76%
Camel <https://en.wikipedia.org/wiki/Camel_(color)#Camel> 	#C19A6B
76% 	60% 	42% 	33° 	41% 	59% 	45% 	76%
Cameo pink <https://en.wikipedia.org/wiki/Shades_of_pink#Cameo_pink>
#EFBBCC 	94% 	73% 	80% 	340° 	62% 	84% 	22% 	94%
Canary
<https://en.wikipedia.org/wiki/History_of_Crayola_crayons#Crayola_No._64>
#FFFF99 	100% 	100% 	60% 	60° 	100% 	80% 	40% 	100%
Canary yellow
<https://en.wikipedia.org/wiki/Shades_of_yellow#Yellow_(CMYK)_(process_yellow)_(canary_yellow)>
	#FFEF00 	100% 	94% 	0% 	56° 	100% 	50% 	100% 	100%
Candy apple red <https://en.wikipedia.org/wiki/Candy_apple_red>
#FF0800 	100% 	3% 	0% 	2° 	100% 	50% 	100% 	100%
Candy pink <https://en.wikipedia.org/wiki/Candy_apple_red#Candy_pink>
#E4717A 	89% 	44% 	48% 	355° 	68% 	67% 	50% 	89%
Capri <https://en.wikipedia.org/wiki/Sky_blue#Deep_sky_blue>
#00BFFF 	0% 	75% 	100% 	195° 	100% 	50% 	100% 	100%
Caput mortuum <https://en.wikipedia.org/wiki/Caput_mortuum_(pigment)>
#592720 	35% 	15% 	13% 	7° 	47% 	24% 	64% 	35%
Cardinal <https://en.wikipedia.org/wiki/Cardinal_(color)> 	#C41E3A
77% 	12% 	23% 	350° 	74% 	44% 	85% 	77%
Caribbean green
<https://en.wikipedia.org/wiki/Spring_green#Caribbean_green>
#00CC99 	0% 	80% 	60% 	165° 	100% 	40% 	100% 	80%
Carmine <https://en.wikipedia.org/wiki/Carmine_(color)> 	#960018
59% 	0% 	9% 	350° 	100% 	29% 	100% 	59%
Carmine (M&P)
<https://en.wikipedia.org/wiki/Carmine_(color)#Rich_carmine>
#D70040 	84% 	0% 	25% 	342° 	100% 	42% 	100% 	84%
Carnation pink <https://en.wikipedia.org/wiki/Carnation_pink> 	#FFA6C9
100% 	65% 	79% 	336° 	100% 	83% 	35% 	100%
Carnelian <https://en.wikipedia.org/wiki/Carnelian_(color)> 	#B31B1B
70% 	11% 	11% 	0° 	74% 	40% 	85% 	70%
Carolina blue <https://en.wikipedia.org/wiki/Carolina_blue> 	#56A0D3
34% 	63% 	83% 	204° 	59% 	58% 	59% 	83%
Carrot orange
<https://en.wikipedia.org/wiki/Shades_of_orange#Carrot_orange>
#ED9121 	93% 	57% 	13% 	33° 	85% 	53% 	86% 	93%
Castleton green
<https://en.wikipedia.org/wiki/Shades_of_green#Castleton_green>
#00563F 	0% 	34% 	25% 	164° 	100% 	17% 	100% 	34%
Catawba
<https://en.wikipedia.org/wiki/Catawba_(grape)#Catawba_(color)>
#703642 	44% 	21% 	26% 	348° 	35% 	33% 	52% 	44%
Cedar Chest
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Magic_Scent>
#C95A49 	79% 	35% 	29% 	8° 	54% 	54% 	64% 	79%
Celadon <https://en.wikipedia.org/wiki/Shades_of_green#Celadon>
#ACE1AF 	67% 	88% 	69% 	123° 	47% 	78% 	24% 	88%
Celadon blue <https://en.wikipedia.org/wiki/Shades_of_cyan#Cerulean>
#007BA7 	0% 	48% 	65% 	196° 	100% 	33% 	100% 	65%
Celadon green
<https://en.wikipedia.org/wiki/Shades_of_green#Celadon_green>
#2F847C 	18% 	52% 	49% 	174° 	47% 	35% 	64% 	52%
Celeste <https://en.wikipedia.org/wiki/Sky_blue#Celeste> 	#B2FFFF 	70%
100% 	100% 	180° 	100% 	85% 	30% 	100%
Celtic blue <https://en.wikipedia.org/wiki/Isatis_tinctoria>
#246BCE 	14% 	42% 	81% 	215° 	70% 	48% 	83% 	81%
Cerise <https://en.wikipedia.org/wiki/Cerise_(color)> 	#DE3163 	87%
19% 	39% 	343° 	72% 	53% 	78% 	87%
Cerulean <https://en.wikipedia.org/wiki/Cerulean> 	#007BA7 	0% 	48%
65% 	196° 	100% 	33% 	100% 	65%
Cerulean blue <https://en.wikipedia.org/wiki/Cerulean#Cerulean_blue>
#2A52BE 	16% 	32% 	75% 	224° 	64% 	45% 	78% 	75%
Cerulean frost <https://en.wikipedia.org/wiki/Cerulean#Cerulean_frost>
#6D9BC3 	43% 	61% 	76% 	208° 	42% 	60% 	44% 	76%
Cerulean (Crayola)
<https://en.wikipedia.org/wiki/Cerulean#Cerulean_(Crayola)> 	#1DACD6
11% 	67% 	84% 	194° 	76% 	48% 	86% 	84%
CG blue <https://en.wikipedia.org/wiki/CG_Blue> 	#007AA5 	0% 	48% 	65%
196° 	100% 	32% 	100% 	65%
CG red <https://en.wikipedia.org/wiki/CG_Red> 	#E03C31 	88% 	24%
19% 	4° 	74% 	54% 	78% 	88%
Champagne <https://en.wikipedia.org/wiki/Champagne_(color)#Champagne>
#F7E7CE 	97% 	91% 	81% 	37° 	72% 	89% 	17% 	97%
Champagne pink
<https://en.wikipedia.org/wiki/Shades_of_pink#Other_notable_pink_colors> 	#F1DDCF
	95% 	87% 	81% 	25° 	55% 	88% 	14% 	95%
Charcoal <https://en.wikipedia.org/wiki/Shades_of_gray#Charcoal>
#36454F 	21% 	27% 	31% 	204° 	19% 	26% 	32% 	31%
Charleston green
<https://en.wikipedia.org/wiki/Shades_of_black_(colors)#Charleston_green>
#232B2B 	14% 	17% 	17% 	180° 	10% 	15% 	19% 	17%
Charm pink <https://en.wikipedia.org/wiki/Shades_of_pink#Charm_pink>
#E68FAC 	90% 	56% 	67% 	340° 	64% 	73% 	38% 	90%
Chartreuse (traditional)
<https://en.wikipedia.org/wiki/Chartreuse_(color)> 	#DFFF00 	87%
100% 	0% 	68° 	100% 	50% 	100% 	100%
Chartreuse (web) <https://en.wikipedia.org/wiki/Chartreuse_(color)>
#7FFF00 	50% 	100% 	0% 	90° 	100% 	50% 	100% 	100%
Cherry blossom pink
<https://en.wikipedia.org/wiki/Shades_of_pink#Cherry_blossom_pink>
#FFB7C5 	100% 	72% 	77% 	348° 	100% 	86% 	28% 	100%
Chestnut <https://en.wikipedia.org/wiki/Chestnut_(color)> 	#954535
58% 	27% 	21% 	10° 	48% 	40% 	64% 	58%
Chili red <https://en.wikipedia.org/wiki/Shades_of_red#Chili_red>
#E23D28 	89% 	24% 	16% 	5° 	76% 	52% 	183% 	125%
China pink <https://en.wikipedia.org/wiki/Shades_of_pink#China_pink>
#DE6FA1 	87% 	44% 	63% 	333° 	63% 	65% 	50% 	87%
China rose <https://en.wikipedia.org/wiki/Rose_(color)#China_rose>
#A8516E 	66% 	32% 	43% 	340° 	35% 	49% 	52% 	66%
Chinese red <https://en.wikipedia.org/wiki/Vermilion#Chinese_red_2>
#AA381E 	67% 	22% 	12% 	11° 	70% 	39% 	82% 	67%
Chinese violet
<https://en.wikipedia.org/wiki/Shades_of_violet#Chinese_violet>
#856088 	52% 	38% 	53% 	296° 	17% 	46% 	29% 	53%
Chinese yellow
<https://en.wikipedia.org/wiki/Shades_of_yellow#Chinese_yellow>
#FFB200 	100% 	70% 	0% 	42° 	100% 	50% 	100% 	100%
Chocolate (traditional)
<https://en.wikipedia.org/wiki/Chocolate_(color)> 	#7B3F00 	48% 	25%
0% 	31° 	100% 	24% 	100% 	48%
Chocolate (web)
<https://en.wikipedia.org/wiki/Chocolate_(color)#Variations_of_chocolate>
#D2691E 	82% 	41% 	12% 	25° 	75% 	47% 	86% 	82%
Chocolate Cosmos
<https://en.wikipedia.org/wiki/Shades_of_red#Chocolate_cosmos>
#58111A 	35% 	7% 	10% 	352° 	68% 	21% 	80% 	34%
Chrome yellow <https://en.wikipedia.org/wiki/Chrome_yellow> 	#FFA700
100% 	65% 	0% 	39° 	100% 	50% 	100% 	100%
Cinereous <https://en.wikipedia.org/wiki/Cinereous> 	#98817B 	60%
51% 	48% 	12° 	12% 	54% 	19% 	60%
Cinnabar <https://en.wikipedia.org/wiki/Vermilion> 	#E34234 	89%
26% 	20% 	5° 	76% 	55% 	77% 	89%
Cinnamon Satin
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Silver_Swirls>
	#CD607E 	80% 	38% 	49% 	343° 	52% 	59% 	53% 	80%
Citrine <https://en.wikipedia.org/wiki/Citrine_(colour)> 	#E4D00A
89% 	82% 	4% 	54° 	92% 	47% 	96% 	89%
Citron <https://en.wikipedia.org/wiki/Lemon_(color)#Citron> 	#9FA91F
62% 	66% 	12% 	64° 	69% 	39% 	82% 	66%
Claret <https://en.wikipedia.org/wiki/Wine_(color)#Claret> 	#7F1734
50% 	9% 	20% 	343° 	69% 	29% 	82% 	50%
Cobalt blue <https://en.wikipedia.org/wiki/Cobalt_blue> 	#0047AB 	0%
28% 	67% 	215° 	100% 	34% 	100% 	67%
Cocoa brown
<https://en.wikipedia.org/wiki/Chocolate_(color)#Variations_of_chocolate>
#D2691E 	82% 	41% 	12% 	25° 	75% 	47% 	86% 	82%
Coffee <https://en.wikipedia.org/wiki/Coffee_(color)> 	#6F4E37 	44%
31% 	22% 	25° 	34% 	33% 	50% 	44%
Columbia Blue <https://en.wikipedia.org/wiki/Columbia_Blue> 	#B9D9EB
73% 	85% 	92% 	202° 	56% 	82% 	21% 	92%
Congo pink <https://en.wikipedia.org/wiki/Shades_of_pink#Congo_pink>
#F88379 	97% 	51% 	47% 	5° 	90% 	72% 	51% 	97%
Cool grey <https://en.wikipedia.org/wiki/Shades_of_gray#Cool_gray>
#8C92AC 	55% 	57% 	67% 	229° 	16% 	61% 	19% 	67%
Copper <https://en.wikipedia.org/wiki/Copper_(color)> 	#B87333 	72%
45% 	20% 	29° 	57% 	46% 	72% 	72%
Copper (Crayola)
<https://en.wikipedia.org/wiki/Copper_(color)#Variations_of_copper>
#DA8A67 	85% 	54% 	40% 	18° 	61% 	63% 	53% 	85%
Copper penny
<https://en.wikipedia.org/wiki/Copper_(color)#Copper_penny> 	#AD6F69
68% 	44% 	41% 	5° 	29% 	55% 	39% 	68%
Copper red <https://en.wikipedia.org/wiki/Copper_(color)#Copper_red>
#CB6D51 	80% 	43% 	32% 	14° 	54% 	56% 	60% 	80%
Copper rose <https://en.wikipedia.org/wiki/Copper_(color)#Copper_rose>
#996666 	60% 	40% 	40% 	0° 	20% 	50% 	33% 	60%
Coquelicot <https://en.wikipedia.org/wiki/Coquelicot> 	#FF3800 	100%
22% 	0% 	13° 	100% 	50% 	100% 	100%
Coral <https://en.wikipedia.org/wiki/Coral_(color)> 	#FF7F50 	100%
50% 	31% 	16° 	100% 	66% 	69% 	100%
Coral pink <https://en.wikipedia.org/wiki/Coral_(color)#Coral_pink>
#F88379 	97% 	51% 	47% 	5° 	90% 	72% 	51% 	97%
Cordovan <https://en.wikipedia.org/wiki/Cordovan_(color)> 	#893F45
54% 	25% 	27% 	355° 	37% 	39% 	54% 	54%
Corn <https://en.wikipedia.org/wiki/Corn_(color)> 	#FBEC5D 	98% 	93%
36% 	54° 	95% 	68% 	63% 	98%
Cornell red <https://en.wikipedia.org/wiki/Shades_of_red#Cornell_red>
#B31B1B 	70% 	11% 	11% 	0° 	74% 	40% 	85% 	70%
Cornflower blue <https://en.wikipedia.org/wiki/Cornflower_blue>
#6495ED 	39% 	58% 	93% 	219° 	79% 	66% 	58% 	93%
Cornsilk <https://en.wikipedia.org/wiki/Shades_of_white#Cornsilk>
#FFF8DC 	100% 	97% 	86% 	48° 	100% 	93% 	14% 	100%
Cosmic cobalt
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Silver_Swirls>
	#2E2D88 	18% 	18% 	53% 	241° 	50% 	36% 	67% 	53%
Cosmic latte <https://en.wikipedia.org/wiki/Cosmic_latte> 	#FFF8E7
100% 	97% 	91% 	43° 	100% 	95% 	9% 	100%
Coyote brown <https://en.wikipedia.org/wiki/Coyote_brown> 	#81613C
51% 	38% 	24% 	32° 	37% 	37% 	52% 	51%
Cotton candy
<https://en.wikipedia.org/wiki/Shades_of_pink#Cotton_candy> 	#FFBCD9
100% 	74% 	85% 	334° 	100% 	87% 	26% 	100%
Cream <https://en.wikipedia.org/wiki/Cream_(colour)> 	#FFFDD0 	100%
99% 	82% 	57° 	100% 	91% 	18% 	100%
Crimson <https://en.wikipedia.org/wiki/Crimson> 	#DC143C 	86% 	8% 	24%
348° 	83% 	47% 	91% 	86%
Crimson (UA) <https://en.wikipedia.org/wiki/Crimson#School_colors>
#9E1B32 	62% 	11% 	20% 	349° 	71% 	36% 	83% 	62%
Crystal <https://en.wikipedia.org/wiki/Crystal> 	#A7D8DE 	65% 	85%
87% 	187° 	46% 	76% 	45% 	87%
Cultured
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Pearl_Brite>
#F5F5F5 	96% 	96% 	96% 	—° 	0% 	96% 	0% 	96%
Cyan <https://en.wikipedia.org/wiki/Cyan> 	#00FFFF 	0% 	100% 	100%
180° 	100% 	50% 	100% 	100%
Cyan (process) <https://en.wikipedia.org/wiki/Cyan#Process_cyan>
#00B7EB 	0% 	72% 	92% 	193° 	100% 	46% 	100% 	92%
Cyber grape
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Metallic_FX>
#58427C 	35% 	26% 	49% 	263° 	31% 	37% 	47% 	49%
Cyber yellow
<https://en.wikipedia.org/wiki/Shades_of_yellow#Cyber_yellow> 	#FFD300
100% 	83% 	0% 	50° 	100% 	50% 	100% 	100%
Cyclamen <https://en.wikipedia.org/wiki/Cyclamen_(color)> 	#F56FA1
96% 	44% 	63% 	338° 	87% 	70% 	54% 	96%
Dark blue-gray
<https://en.wikipedia.org/wiki/Blue-gray#Dark_blue-gray> 	#666699
40% 	40% 	60% 	240° 	20% 	50% 	33% 	60%
Dark brown <https://en.wikipedia.org/wiki/Shades_of_brown#Dark_brown>
#654321 	40% 	26% 	13% 	30° 	51% 	26% 	67% 	40%
Dark byzantium
<https://en.wikipedia.org/wiki/Byzantium_(color)#Dark_byzantium>
#5D3954 	36% 	22% 	33% 	315° 	24% 	29% 	39% 	36%
Dark cornflower blue
<https://en.wikipedia.org/wiki/Cornflower_blue#Dark_cornflower_blue>
#26428B 	15% 	26% 	55% 	223° 	57% 	35% 	73% 	55%
Dark cyan <https://en.wikipedia.org/wiki/Shades_of_cyan#Dark_cyan>
#008B8B 	0% 	55% 	55% 	180° 	100% 	27% 	100% 	55%
Dark electric blue
<https://en.wikipedia.org/wiki/Electric_blue_(color)#Dark_electric_blue> 	#536878
	33% 	41% 	47% 	206° 	18% 	40% 	31% 	47%
Dark goldenrod
<https://en.wikipedia.org/wiki/Goldenrod_(color)#Dark_goldenrod>
#B8860B 	72% 	53% 	4% 	43° 	89% 	38% 	94% 	72%
Dark green <https://en.wikipedia.org/wiki/Shades_of_green#Dark_green>
#013220 	0% 	20% 	13% 	158° 	96% 	10% 	98% 	20%
Dark green (X11)
<https://en.wikipedia.org/wiki/Shades_of_green#Dark_green_(X11)>
#006400 	0% 	39% 	0% 	120° 	100% 	20% 	100% 	39%
Dark jungle green
<https://en.wikipedia.org/wiki/Jungle_green#Dark_jungle_green>
#1A2421 	10% 	14% 	13% 	162° 	16% 	12% 	28% 	14%
Dark khaki <https://en.wikipedia.org/wiki/Khaki_(color)#Dark_khaki>
#BDB76B 	74% 	72% 	42% 	56° 	38% 	58% 	43% 	74%
Dark lava <https://en.wikipedia.org/wiki/Lava_(color)#Dark_lava>
#483C32 	28% 	24% 	20% 	27° 	18% 	24% 	31% 	28%
Dark liver
<https://en.wikipedia.org/wiki/Liver_(color)#Dark_liver_(web)>
#534B4F 	33% 	29% 	31% 	330° 	5% 	31% 	10% 	33%
Dark liver (horses)
<https://en.wikipedia.org/wiki/Liver_(color)#Dark_liver_(horses)>
#543D37 	33% 	24% 	22% 	12° 	21% 	27% 	35% 	33%
Dark magenta
<https://en.wikipedia.org/wiki/Shades_of_magenta#Dark_magenta>
#8B008B 	55% 	0% 	55% 	300° 	100% 	27% 	100% 	55%
Dark moss green
<https://en.wikipedia.org/wiki/Shades_of_green#Dark_moss_green>
#4A5D23 	29% 	36% 	14% 	80° 	45% 	25% 	62% 	36%
Dark olive green
<https://en.wikipedia.org/wiki/Olive_(color)#Dark_olive_green>
#556B2F 	33% 	42% 	18% 	82° 	39% 	30% 	56% 	42%
Dark orange
<https://en.wikipedia.org/wiki/Shades_of_orange#Dark_orange_(web_color)> 	#FF8C00
	100% 	55% 	0% 	33° 	100% 	50% 	100% 	100%
Dark orchid <https://en.wikipedia.org/wiki/Orchid_(color)#Dark_orchid>
#9932CC 	60% 	20% 	80% 	280° 	61% 	50% 	75% 	80%
Dark pastel green
<https://en.wikipedia.org/wiki/Shades_of_green#Dark_pastel_green>
#03C03C 	1% 	75% 	24% 	138° 	97% 	38% 	98% 	75%
Dark purple <https://en.wikipedia.org/wiki/Dark_purple> 	#301934
19% 	10% 	20% 	291° 	35% 	15% 	51% 	20%
Dark red <https://en.wikipedia.org/wiki/Maroon_(color)#Dark_red>
#8B0000 	55% 	0% 	0% 	0° 	100% 	27% 	100% 	55%
Dark salmon <https://en.wikipedia.org/wiki/Salmon_(color)#Dark_salmon>
#E9967A 	91% 	59% 	48% 	15° 	72% 	70% 	48% 	91%
Dark sea green
<https://en.wikipedia.org/wiki/X11_color_names#Color_name_charts>
#8FBC8F 	56% 	74% 	56% 	120° 	25% 	65% 	24% 	74%
Dark sienna <https://en.wikipedia.org/wiki/Sienna> 	#3C1414 	24% 	8%
8% 	0° 	50% 	16% 	67% 	24%
Dark sky blue <https://en.wikipedia.org/wiki/Sky_blue#Dark_sky_blue>
#8CBED6 	55% 	75% 	84% 	199° 	47% 	69% 	35% 	84%
Dark slate blue
<https://en.wikipedia.org/wiki/X11_color_names#Color_name_charts>
#483D8B 	28% 	24% 	55% 	248° 	39% 	39% 	56% 	55%
Dark slate gray
<https://en.wikipedia.org/wiki/Slate_gray#Dark_slate_gray> 	#2F4F4F
18% 	31% 	31% 	180° 	25% 	25% 	41% 	31%
Dark spring green
<https://en.wikipedia.org/wiki/Spring_green#Dark_spring_green>
#177245 	9% 	45% 	27% 	150° 	66% 	27% 	80% 	45%
Dark turquoise
<https://en.wikipedia.org/wiki/Turquoise_(color)#Dark_Turquoise>
#00CED1 	0% 	81% 	82% 	181° 	100% 	41% 	100% 	82%
Dark violet
<https://en.wikipedia.org/wiki/Shades_of_violet#Pigment_violet_(web_color_dark_violet)>
	#9400D3 	58% 	0% 	83% 	282° 	100% 	41% 	100% 	83%
Dartmouth green
<https://en.wikipedia.org/wiki/Shades_of_green#Dartmouth_green>
#00703C 	0% 	44% 	24% 	152° 	100% 	22% 	100% 	44%
Davy's grey <https://en.wikipedia.org/wiki/Davy%27s_grey> 	#555555
33% 	33% 	33% 	—° 	0% 	33% 	0% 	33%
Deep cerise <https://en.wikipedia.org/wiki/Cerise_(color)#Deep_cerise>
#DA3287 	85% 	20% 	53% 	330° 	69% 	53% 	77% 	85%
Deep champagne
<https://en.wikipedia.org/wiki/Champagne_(color)#Deep_champagne>
#FAD6A5 	98% 	84% 	65% 	35° 	90% 	81% 	34% 	98%
Deep chestnut
<https://en.wikipedia.org/wiki/Chestnut_(color)#Deep_chestnut>
#B94E48 	73% 	31% 	28% 	3° 	45% 	50% 	61% 	73%
Deep jungle green
<https://en.wikipedia.org/wiki/Jungle_green#Deep_jungle_green>
#004B49 	0% 	29% 	29% 	178° 	100% 	15% 	100% 	29%
Deep pink <https://en.wikipedia.org/wiki/Shades_of_pink#Deep_pink>
#FF1493 	100% 	8% 	58% 	328° 	100% 	54% 	92% 	100%
Deep saffron
<https://en.wikipedia.org/wiki/Saffron_(color)#India_saffron_or_deep_saffron>
	#FF9933 	100% 	60% 	20% 	30° 	100% 	60% 	80% 	100%
Deep sky blue <https://en.wikipedia.org/wiki/Sky_blue#Deep_sky_blue>
#00BFFF 	0% 	75% 	100% 	195° 	100% 	50% 	100% 	100%
Deep Space Sparkle
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Metallic_FX>
#4A646C 	29% 	39% 	42% 	194° 	19% 	36% 	31% 	42%
Deep taupe <https://en.wikipedia.org/wiki/Taupe#Deep_taupe> 	#7E5E60
49% 	37% 	38% 	356° 	15% 	43% 	25% 	49%
Denim
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#1560BD 	8% 	38% 	74% 	213° 	80% 	41% 	89% 	74%
Denim blue
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Heads_'n_Tails>
	#2243B6 	13% 	26% 	71% 	227° 	69% 	42% 	81% 	71%
Desert <https://en.wikipedia.org/wiki/Desert_sand_(color)#Desert>
#C19A6B 	76% 	60% 	42% 	33° 	41% 	59% 	45% 	76%
Desert sand <https://en.wikipedia.org/wiki/Desert_sand_(color)>
#EDC9AF 	93% 	79% 	69% 	25° 	63% 	81% 	26% 	93%
Dim gray <https://en.wikipedia.org/wiki/Grey#Web_colors> 	#696969
41% 	41% 	41% 	—° 	0% 	41% 	0% 	41%
Dodger blue <https://en.wikipedia.org/wiki/Dodger_blue> 	#1E90FF
12% 	56% 	100% 	210° 	100% 	56% 	88% 	100%
Dogwood rose <https://en.wikipedia.org/wiki/Rose_(color)#Dogwood_rose>
#D71868 	84% 	9% 	41% 	335° 	80% 	47% 	89% 	84%
Drab
<https://en.wikipedia.org/wiki/Desert_sand_(color)#Sand_dune_(Drab)>
#967117 	59% 	44% 	9% 	43° 	73% 	34% 	85% 	59%
Duke blue <https://en.wikipedia.org/wiki/Duke_blue> 	#00009C 	0% 	0%
61% 	240° 	100% 	31% 	100% 	61%
Dutch white
<https://en.wikipedia.org/wiki/Shades_of_white#Dutch_white> 	#EFDFBB
94% 	87% 	73% 	42° 	62% 	84% 	22% 	94%
Earth yellow
<https://en.wikipedia.org/wiki/Desert_sand_(color)#Earth_yellow>
#E1A95F 	88% 	66% 	37% 	34° 	68% 	63% 	58% 	88%
Ebony <https://en.wikipedia.org/wiki/Shades_of_black_(colors)#Ebony>
#555D50 	33% 	36% 	31% 	97° 	8% 	34% 	14% 	36%
Ecru <https://en.wikipedia.org/wiki/Ecru> 	#C2B280 	76% 	70% 	50%
45° 	35% 	63% 	34% 	76%
Eerie black
<https://en.wikipedia.org/wiki/Shades_of_black#Eerie_black> 	#1B1B1B
11% 	11% 	11% 	—° 	0% 	11% 	0% 	11%
Eggplant <https://en.wikipedia.org/wiki/Eggplant_(color)> 	#614051
38% 	25% 	32% 	329° 	20% 	32% 	34% 	38%
Eggshell <https://en.wikipedia.org/wiki/Eggshell_(color)> 	#F0EAD6
94% 	92% 	84% 	46° 	46% 	89% 	11% 	94%
Egyptian blue <https://en.wikipedia.org/wiki/Egyptian_blue> 	#1034A6
6% 	20% 	65% 	226° 	82% 	36% 	90% 	65%
Eigengrau <https://en.wikipedia.org/wiki/Eigengrau> 	#16161D 	9% 	9%
11% 	240° 	14% 	10% 	24% 	11%
Electric blue <https://en.wikipedia.org/wiki/Electric_blue_(color)>
#7DF9FF 	49% 	98% 	100% 	183° 	100% 	75% 	51% 	100%
Electric green <https://en.wikipedia.org/wiki/Electric_green>
#00FF00 	0% 	100% 	0% 	120° 	100% 	50% 	100% 	100%
Electric indigo <https://en.wikipedia.org/wiki/Indigo#Electric_indigo>
#6F00FF 	44% 	0% 	100% 	266° 	100% 	50% 	100% 	100%
Electric lime
<https://en.wikipedia.org/wiki/Lime_(color)#Electric_lime> 	#CCFF00
80% 	100% 	0% 	72° 	100% 	50% 	100% 	100%
Electric purple
<https://en.wikipedia.org/wiki/Shades_of_purple#Electric_purple:_2000s> 	#BF00FF
	75% 	0% 	100% 	285° 	100% 	50% 	100% 	100%
Electric violet
<https://en.wikipedia.org/wiki/Shades_of_violet#Electric_violet>
#8F00FF 	56% 	0% 	100% 	274° 	100% 	50% 	100% 	100%
Emerald <https://en.wikipedia.org/wiki/Shades_of_green#Emerald>
#50C878 	31% 	78% 	47% 	140° 	52% 	55% 	60% 	78%
Eminence <https://en.wikipedia.org/wiki/Shades_of_purple#Eminence>
#6C3082 	42% 	19% 	51% 	284° 	46% 	35% 	63% 	51%
English green
<https://en.wikipedia.org/wiki/Shades_of_green#Brunswick_green>
#1B4D3E 	11% 	30% 	24% 	162° 	48% 	20% 	65% 	30%
English lavender
<https://en.wikipedia.org/wiki/Lavender_(color)#English_lavender>
#B48395 	71% 	51% 	58% 	338° 	25% 	61% 	27% 	71%
English red
<https://en.wikipedia.org/wiki/Indian_red_(color)#English_red>
#AB4B52 	67% 	29% 	32% 	356° 	39% 	48% 	56% 	67%
English vermillion
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors>
#CC474B 	80% 	28% 	29% 	358° 	57% 	54% 	65% 	80%
English violet
<https://en.wikipedia.org/wiki/Shades_of_violet#English_violet>
#563C5C 	34% 	24% 	36% 	289° 	21% 	30% 	35% 	36%
Erin <https://en.wikipedia.org/wiki/Erin_(color)> 	#00FF40 	0% 	100%
25% 	135° 	100% 	50% 	100% 	100%
Eton blue <https://en.wikipedia.org/wiki/Eton_blue#Eton_blue>
#96C8A2 	59% 	78% 	64% 	134° 	31% 	69% 	25% 	78%
Fallow <https://en.wikipedia.org/wiki/Fallow_(color)> 	#C19A6B 	76%
60% 	42% 	33° 	41% 	59% 	45% 	76%
Falu red <https://en.wikipedia.org/wiki/Falu_red> 	#801818 	50%
9% 	9% 	0° 	68% 	30% 	81% 	50%
Fandango <https://en.wikipedia.org/wiki/Fuchsia_(color)#Fandango>
#B53389 	71% 	20% 	54% 	320° 	56% 	45% 	72% 	71%
Fandango pink
<https://en.wikipedia.org/wiki/Shades_of_pink#Fandango_pink>
#DE5285 	87% 	32% 	52% 	338° 	68% 	60% 	63% 	87%
Fashion fuchsia
<https://en.wikipedia.org/wiki/Fuchsia_(color)#Fashion_fuchsia>
#F400A1 	96% 	0% 	63% 	320° 	100% 	48% 	100% 	96%
Fawn <https://en.wikipedia.org/wiki/Fawn_(colour)> 	#E5AA70 	90%
67% 	44% 	30° 	69% 	67% 	51% 	90%
Feldgrau <https://en.wikipedia.org/wiki/Shades_of_green#Feldgrau>
#4D5D53 	30% 	36% 	33% 	143° 	9% 	33% 	17% 	36%
Fern green <https://en.wikipedia.org/wiki/Shades_of_green#Fern_green>
#4F7942 	31% 	47% 	26% 	106° 	29% 	37% 	45% 	47%
Field drab
<https://en.wikipedia.org/wiki/Desert_sand_(color)#Field_drab>
#6C541E 	42% 	33% 	12% 	42° 	57% 	27% 	72% 	42%
Fiery rose
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Extreme_Twistables_colors>
	#FF5470 	100% 	33% 	44% 	350° 	100% 	67% 	67% 	100%
Firebrick
<https://en.wikipedia.org/wiki/X11_color_names#Color_name_charts>
#B22222 	70% 	13% 	13% 	0° 	68% 	42% 	81% 	70%
Fire engine red <https://en.wikipedia.org/wiki/Fire_engine_red>
#CE2029 	81% 	13% 	16% 	357° 	73% 	47% 	84% 	81%
Fire opal <https://en.wikipedia.org/wiki/Shades_of_orange#Fire_opal>
#E95C4B 	91% 	36% 	29% 	6° 	78% 	60% 	68% 	91%
Flame <https://en.wikipedia.org/wiki/Flame_(color)> 	#E25822 	89%
35% 	13% 	17° 	77% 	51% 	85% 	89%
Flax <https://en.wikipedia.org/wiki/Flax_(color)> 	#EEDC82 	93% 	86%
51% 	50° 	76% 	72% 	45% 	93%
Flirt <https://en.wikipedia.org/wiki/Red-violet#Flirt> 	#A2006D 	64%
0% 	43% 	320° 	100% 	32% 	100% 	64%
Floral white
<https://en.wikipedia.org/wiki/Shades_of_white#Floral_white>
#FFFAF0 	100% 	98% 	94% 	40° 	100% 	97% 	6% 	100%
Fluorescent blue
<https://en.wikipedia.org/wiki/Shades_of_blue#Fluorescent_blue>
#15F4EE 	8% 	96% 	93% 	178° 	91% 	52% 	91% 	96%
Forest green (Crayola)
<https://en.wikipedia.org/wiki/Shades_of_green#Forest_Green_(Crayola)>
#5FA777 	37% 	65% 	47% 	140° 	29% 	51% 	43% 	65%
Forest green (traditional)
<https://en.wikipedia.org/wiki/Shades_of_green#UP_forest_green>
#014421 	0% 	27% 	13% 	149° 	97% 	14% 	99% 	27%
Forest green (web)
<https://en.wikipedia.org/wiki/Shades_of_green#Forest_green>
#228B22 	13% 	55% 	13% 	120° 	61% 	34% 	76% 	55%
French beige <https://en.wikipedia.org/wiki/Beige#French_beige>
#A67B5B 	65% 	48% 	36% 	26° 	30% 	50% 	45% 	65%
French bistre <https://en.wikipedia.org/wiki/Bistre#French_bistre>
#856D4D 	52% 	43% 	30% 	34° 	27% 	41% 	42% 	52%
French blue
<https://en.wikipedia.org/wiki/Shades_of_azure#French_blue> 	#0072BB
0% 	45% 	73% 	203° 	100% 	37% 	100% 	73%
French fuchsia
<https://en.wikipedia.org/wiki/Fuchsia_(color)#French_fuchsia>
#FD3F92 	99% 	25% 	57% 	334° 	98% 	62% 	75% 	99%
French lilac
<https://en.wikipedia.org/wiki/Lilac_(color)#French_lilac> 	#86608E
53% 	38% 	56% 	290° 	19% 	47% 	32% 	56%
French lime <https://en.wikipedia.org/wiki/Lime_(color)#French_lime>
#9EFD38 	62% 	99% 	22% 	89° 	98% 	61% 	78% 	99%
French mauve
<https://en.wikipedia.org/wiki/Mauve#French_mauve_(deep_mauve)>
#D473D4 	83% 	45% 	83% 	300° 	53% 	64% 	46% 	83%
French pink <https://en.wikipedia.org/wiki/Shades_of_pink#French_pink>
#FD6C9E 	99% 	42% 	62% 	339° 	97% 	71% 	57% 	99%
French raspberry
<https://en.wikipedia.org/wiki/Raspberry_(color)#French_raspberry>
#C72C48 	78% 	17% 	28% 	349° 	64% 	48% 	78% 	78%
French rose <https://en.wikipedia.org/wiki/Rose_(color)#French_rose>
#F64A8A 	96% 	29% 	54% 	338° 	91% 	63% 	70% 	96%
French sky blue
<https://en.wikipedia.org/wiki/Sky_blue#French_sky_blue> 	#77B5FE
47% 	71% 	100% 	212° 	99% 	73% 	53% 	100%
French violet
<https://en.wikipedia.org/wiki/Shades_of_violet#French_violet>
#8806CE 	53% 	2% 	81% 	279° 	94% 	42% 	97% 	81%
Frostbite
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Extreme_Twistables_colors>
	#E936A7 	91% 	21% 	65% 	322° 	80% 	56% 	77% 	91%
Fuchsia <https://en.wikipedia.org/wiki/Fuchsia_(color)> 	#FF00FF
100% 	0% 	100% 	300° 	100% 	50% 	100% 	100%
Fuchsia (Crayola)
<https://en.wikipedia.org/wiki/Fuchsia_(color)#Deep_fuchsia>
#C154C1 	76% 	33% 	76% 	300° 	47% 	54% 	56% 	76%
Fuchsia purple
<https://en.wikipedia.org/wiki/Fuchsia_(color)#Fuchsia_purple>
#CC397B 	80% 	22% 	48% 	333° 	59% 	51% 	72% 	80%
Fuchsia rose <https://en.wikipedia.org/wiki/Rose_(color)#Fuchsia_rose>
#C74375 	78% 	26% 	46% 	337° 	54% 	52% 	66% 	78%
Fulvous <https://en.wikipedia.org/wiki/Fulvous> 	#E48400 	89% 	52%
0% 	35° 	100% 	45% 	100% 	89%
Fuzzy Wuzzy
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#87421F 	53% 	26% 	12% 	20° 	63% 	33% 	77% 	53%
Gainsboro
<https://en.wikipedia.org/wiki/X11_colour_names#Color_names_identical_between_X11_and_HTML/CSS>
	#DCDCDC 	86% 	86% 	86% 	—° 	0% 	86% 	0% 	86%
Gamboge <https://en.wikipedia.org/wiki/Gamboge> 	#E49B0F 	89% 	61%
6% 	39° 	88% 	48% 	93% 	89%
Generic viridian
<https://en.wikipedia.org/wiki/Viridian#Generic_viridian> 	#007F66
0% 	50% 	40% 	168° 	100% 	25% 	100% 	50%
Ghost white
<https://en.wikipedia.org/wiki/Shades_of_white#Ghost_white> 	#F8F8FF
97% 	97% 	100% 	240° 	100% 	99% 	3% 	100%
Glaucous <https://en.wikipedia.org/wiki/Glaucous> 	#6082B6 	38% 	51%
71% 	216° 	37% 	55% 	47% 	71%
Glossy grape
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Silver_Swirls>
	#AB92B3 	67% 	57% 	70% 	285° 	18% 	64% 	18% 	70%
GO green
<https://en.wikipedia.org/wiki/Shades_of_green#GO_Transit_green>
#00AB66 	0% 	67% 	40% 	156° 	100% 	34% 	100% 	67%
Gold <https://en.wikipedia.org/wiki/Gold_(color)#Gold> 	#A57C00 	65%
49% 	0% 	46° 	100% 	32% 	100% 	65%
Gold (metallic)
<https://en.wikipedia.org/wiki/Gold_(color)#Gold_(metallic_gold)>
#D4AF37 	83% 	69% 	22% 	46° 	65% 	52% 	74% 	83%
Gold (web) (Golden) <https://en.wikipedia.org/wiki/Gold_(color)>
#FFD700 	100% 	84% 	0% 	51° 	100% 	50% 	100% 	100%
Gold (Crayola) <https://en.wikipedia.org/wiki/Gold_(color)#Pale_gold>
#E6BE8A 	90% 	75% 	54% 	34° 	65% 	72% 	40% 	90%
Gold Fusion
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Metallic_FX>
#85754E 	52% 	46% 	31% 	43° 	26% 	41% 	41% 	52%
Golden brown <https://en.wikipedia.org/wiki/Gold_(color)#Golden_brown>
#996515 	60% 	40% 	8% 	36° 	76% 	34% 	86% 	60%
Golden poppy <https://en.wikipedia.org/wiki/Gold_(color)#Golden_poppy>
#FCC200 	99% 	76% 	0% 	46° 	100% 	49% 	100% 	99%
Golden yellow
<https://en.wikipedia.org/wiki/Gold_(color)#Golden_yellow> 	#FFDF00
100% 	87% 	0% 	52° 	100% 	50% 	100% 	100%
Goldenrod <https://en.wikipedia.org/wiki/Goldenrod_(color)> 	#DAA520
85% 	65% 	13% 	43° 	74% 	49% 	85% 	85%
Granite gray
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Silver_Swirls>
	#676767 	40% 	40% 	40% 	—° 	0% 	40% 	0% 	40%
Granny Smith apple
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors>
#A8E4A0 	66% 	89% 	63% 	113° 	56% 	76% 	30% 	89%
Gray (web) <https://en.wikipedia.org/wiki/Shades_of_gray#Gray>
#808080 	50% 	50% 	50% 	—° 	0% 	50% 	0% 	50%
Gray (X11 gray)
<https://en.wikipedia.org/wiki/X11_color_names#Color_names> 	#BEBEBE
75% 	75% 	75% 	—° 	0% 	75% 	0% 	75%
Green <https://en.wikipedia.org/wiki/Green> 	#00FF00 	0% 	100% 	0%
120° 	100% 	50% 	100% 	100%
Green (Crayola)
<https://en.wikipedia.org/wiki/Shades_of_green#Green_(Crayola)>
#1CAC78 	11% 	67% 	47% 	158° 	72% 	39% 	84% 	67%
Green (web)
<https://en.wikipedia.org/wiki/Shades_of_green#Green_(HTML/CSS_color)>
#008000 	0% 	50% 	0% 	120° 	100% 	25% 	100% 	50%
Green (Munsell)
<https://en.wikipedia.org/wiki/Shades_of_green#Green_(Munsell)>
#00A877 	0% 	66% 	47% 	163° 	100% 	33% 	100% 	66%
Green (NCS)
<https://en.wikipedia.org/wiki/Shades_of_green#Green_(NCS)> 	#009F6B
0% 	62% 	42% 	160° 	100% 	31% 	100% 	62%
Green (Pantone)
<https://en.wikipedia.org/wiki/Shades_of_green#Green_(Pantone)>
#00AD43 	0% 	68% 	26% 	143° 	100% 	34% 	100% 	68%
Green (pigment)
<https://en.wikipedia.org/wiki/Shades_of_green#Green_(CMYK)_(pigment_green)>
	#00A550 	0% 	65% 	31% 	149° 	100% 	32% 	100% 	65%
Green (RYB) <https://en.wikipedia.org/wiki/RYB_color_model> 	#66B032
40% 	69% 	20% 	95° 	56% 	44% 	72% 	69%
Green-blue <https://en.wikipedia.org/wiki/Blue-green> 	#1164B4 	7%
39% 	71% 	209° 	83% 	39% 	91% 	71%
Green-blue (Crayola)
<https://en.wikipedia.org/wiki/Blue-green#Blue-green_(Crayola)>
#2887C8 	16% 	53% 	78% 	204° 	67% 	47% 	80% 	78%
Green-cyan <https://en.wikipedia.org/wiki/Shades_of_cyan> 	#009966
0% 	60% 	40% 	160° 	100% 	30% 	100% 	60%
Green Lizard
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Heads_'n_Tails>
	#A7F432 	65% 	96% 	20% 	84° 	90% 	58% 	80% 	96%
Green Sheen
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Silver_Swirls>
	#6EAEA1 	43% 	68% 	63% 	168° 	28% 	56% 	37% 	68%
Green-yellow
<https://en.wikipedia.org/wiki/Shades_of_green#Yellow-green>
#ADFF2F 	68% 	100% 	18% 	84° 	100% 	59% 	82% 	100%
Green-yellow (Crayola)
<https://en.wikipedia.org/wiki/Shades_of_green#Green-yellow_(Crayola)>
#F0E891 	94% 	91% 	57% 	55° 	76% 	76% 	40% 	94%
Grullo <https://en.wikipedia.org/wiki/Grullo> 	#A99A86 	66% 	60%
53% 	34° 	17% 	59% 	21% 	66%
Gunmetal <https://en.wikipedia.org/wiki/Shades_of_gray#Gunmetal>
#2a3439 	16% 	20% 	22% 	200° 	15% 	19% 	15% 	19%
Han blue <https://en.wikipedia.org/wiki/Han_blue> 	#446CCF 	27% 	42%
81% 	223° 	59% 	54% 	67% 	81%
Han purple <https://en.wikipedia.org/wiki/Han_purple> 	#5218FA 	32%
9% 	98% 	255° 	96% 	54% 	90% 	98%
Hansa yellow <https://en.wikipedia.org/wiki/Hansa_yellow> 	#E9D66B
91% 	84% 	42% 	51° 	74% 	67% 	54% 	91%
Harlequin <https://en.wikipedia.org/wiki/Shades_of_green#Harlequin>
#3FFF00 	25% 	100% 	0% 	105° 	100% 	50% 	100% 	100%
Harvest gold <https://en.wikipedia.org/wiki/Gold_(color)#Harvest_gold>
#DA9100 	85% 	57% 	0% 	40° 	100% 	43% 	100% 	85%
Heat Wave
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Extreme_Twistables_colors>
	#FF7A00 	100% 	48% 	0% 	29° 	100% 	50% 	100% 	100%
Heliotrope <https://en.wikipedia.org/wiki/Heliotrope_(color)>
#DF73FF 	87% 	45% 	100% 	286° 	100% 	73% 	55% 	100%
Heliotrope gray
<https://en.wikipedia.org/wiki/Heliotrope_(color)#Heliotrope_gray>
#AA98A9 	67% 	60% 	66% 	303° 	10% 	63% 	11% 	67%
Hollywood cerise
<https://en.wikipedia.org/wiki/Cerise_(color)#Hollywood_cerise>
#F400A1 	96% 	0% 	63% 	320° 	100% 	48% 	100% 	96%
Honeydew <https://en.wikipedia.org/wiki/Spring_green_(color)#Honeydew>
#F0FFF0 	94% 	100% 	94% 	120° 	100% 	97% 	6% 	100%
Honolulu blue
<https://en.wikipedia.org/wiki/Shades_of_azure#Honolulu_blue>
#006DB0 	0% 	43% 	69% 	203° 	100% 	35% 	100% 	69%
Hooker's green
<https://en.wikipedia.org/wiki/Shades_of_green#Hooker's_green>
#49796B 	29% 	47% 	42% 	163° 	25% 	38% 	40% 	47%
Hot magenta
<https://en.wikipedia.org/wiki/Shades_of_magenta#Hot_magenta> 	#FF1DCE
100% 	11% 	81% 	313° 	100% 	56% 	89% 	100%
Hot pink <https://en.wikipedia.org/wiki/Shades_of_pink#Hot_pink>
#FF69B4 	100% 	41% 	71% 	330° 	100% 	71% 	59% 	100%
Hunter green
<https://en.wikipedia.org/wiki/Shades_of_green#Hunter_green>
#355E3B 	21% 	37% 	23% 	129° 	28% 	29% 	44% 	37%
Iceberg <https://en.wikipedia.org/wiki/Blue-gray#Iceberg> 	#71A6D2
44% 	65% 	82% 	207° 	52% 	63% 	46% 	82%
Icterine <https://en.wikipedia.org/wiki/Icterine> 	#FCF75E 	99% 	97%
37% 	58° 	96% 	68% 	63% 	99%
Illuminating emerald
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Metallic_FX>
#319177 	19% 	57% 	47% 	164° 	49% 	38% 	66% 	57%
Imperial red
<https://en.wikipedia.org/wiki/Shades_of_red#Imperial_Red> 	#ED2939
93% 	16% 	22% 	355° 	84% 	55% 	83% 	93%
Inchworm
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#B2EC5D 	70% 	93% 	36% 	84° 	79% 	65% 	61% 	93%
Independence
<https://en.wikipedia.org/wiki/Shades_of_blue#Independence> 	#4C516D
30% 	32% 	43% 	231° 	18% 	36% 	30% 	43%
India green
<https://en.wikipedia.org/wiki/Shades_of_green#India_green> 	#138808
7% 	53% 	3% 	115° 	89% 	28% 	94% 	53%
Indian red <https://en.wikipedia.org/wiki/Indian_red_(color)>
#CD5C5C 	80% 	36% 	36% 	0° 	53% 	58% 	55% 	80%
Indian yellow <https://en.wikipedia.org/wiki/Indian_yellow> 	#E3A857
89% 	66% 	34% 	35° 	71% 	62% 	62% 	89%
Indigo <https://en.wikipedia.org/wiki/Indigo> 	#4B0082 	29% 	0% 	51%
266° 	100% 	26% 	100% 	51%
Indigo dye <https://en.wikipedia.org/wiki/Indigo#Indigo_dye>
#00416A 	0% 	25% 	42% 	203° 	100% 	21% 	100% 	42%
International orange (aerospace)
<https://en.wikipedia.org/wiki/International_orange> 	#FF4F00 	100%
31% 	0% 	19° 	100% 	50% 	100% 	100%
International orange (engineering)
<https://en.wikipedia.org/wiki/International_orange#International_orange_(Engineering)>
	#BA160C 	73% 	9% 	5% 	3° 	88% 	39% 	94% 	73%
International orange (Golden Gate Bridge)
<https://en.wikipedia.org/wiki/International_orange#Golden_Gate_Bridge> 	#C0362C
	75% 	21% 	17% 	4° 	63% 	46% 	77% 	75%
Iris <https://en.wikipedia.org/wiki/Iris_(color)> 	#5A4FCF 	35% 	31%
81% 	245° 	57% 	56% 	62% 	81%
Irresistible
<https://en.wikipedia.org/wiki/Cerise_(color)#Irresistible> 	#B3446C
70% 	27% 	42% 	338° 	45% 	48% 	62% 	70%
Isabelline <https://en.wikipedia.org/wiki/Isabelline_(colour)>
#F4F0EC 	96% 	94% 	93% 	30° 	27% 	94% 	3% 	96%
Italian sky blue <https://en.wikipedia.org/wiki/Sky_blue#Celeste>
#B2FFFF 	70% 	100% 	100% 	180° 	100% 	85% 	30% 	100%
Ivory <https://en.wikipedia.org/wiki/Ivory_(color)> 	#FFFFF0 	100%
100% 	94% 	60° 	100% 	97% 	6% 	100%
Jade <https://en.wikipedia.org/wiki/Shades_of_green#Jade> 	#00A86B
0% 	66% 	42% 	158° 	100% 	33% 	100% 	66%
Japanese carmine
<https://en.wikipedia.org/wiki/Carmine_(color)#Japanese_carmine>
#9D2933 	62% 	16% 	20% 	355° 	59% 	39% 	74% 	62%
Japanese violet
<https://en.wikipedia.org/wiki/Shades_of_violet#Japanese_violet>
#5B3256 	36% 	20% 	34% 	307° 	29% 	28% 	45% 	36%
Jasmine <https://en.wikipedia.org/wiki/Jasmine_(color)> 	#F8DE7E
97% 	87% 	49% 	47° 	90% 	73% 	49% 	97%
Jazzberry jam <https://en.wikipedia.org/wiki/Red-violet#Jazzberry_jam>
#A50B5E 	65% 	4% 	37% 	328° 	88% 	35% 	93% 	65%
Jet <https://en.wikipedia.org/wiki/Shades_of_black_(colors)#Jet>
#343434 	20% 	20% 	20% 	—° 	0% 	20% 	0% 	20%
Jonquil <https://en.wikipedia.org/wiki/Jonquil_(color)> 	#F4CA16
96% 	79% 	9% 	49° 	91% 	52% 	91% 	96%
June bud <https://en.wikipedia.org/wiki/Spring_bud#June_bud>
#BDDA57 	74% 	85% 	34% 	73° 	64% 	60% 	60% 	85%
Jungle green <https://en.wikipedia.org/wiki/Jungle_green> 	#29AB87
16% 	67% 	53% 	163° 	61% 	42% 	76% 	67%
Kelly green
<https://en.wikipedia.org/wiki/Shades_of_green#Kelly_green> 	#4CBB17
30% 	73% 	9% 	101° 	78% 	41% 	88% 	73%
Keppel <https://en.wikipedia.org/wiki/Shades_of_cyan#Keppel>
#3AB09E 	23% 	69% 	62% 	171° 	50% 	46% 	67% 	69%
Key lime
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Pearl_Brite>
#E8F48C 	91% 	96% 	55% 	67° 	83% 	75% 	43% 	96%
Khaki (web) <https://en.wikipedia.org/wiki/Khaki_(color)#Khaki>
#C3B091 	76% 	69% 	57% 	37° 	29% 	67% 	26% 	76%
Khaki (X11) (Light khaki)
<https://en.wikipedia.org/wiki/Khaki_(color)#Light_khaki> 	#F0E68C
94% 	90% 	55% 	54° 	77% 	75% 	42% 	94%
Kobe <https://en.wikipedia.org/wiki/Indian_red_(color)#Kobe>
#882D17 	53% 	18% 	9% 	12° 	71% 	31% 	83% 	53%
Kobi <https://en.wikipedia.org/wiki/Red-violet#Kobi> 	#E79FC4 	91%
62% 	77% 	329° 	60% 	76% 	31% 	91%
Kobicha <https://en.wikipedia.org/wiki/Kobicha> 	#6B4423 	42% 	27%
14% 	28° 	51% 	28% 	67% 	42%
Kombu green
<https://en.wikipedia.org/wiki/Chartreuse_(color)#Kombu_green>
#354230 	21% 	26% 	19% 	103° 	16% 	22% 	27% 	26%
KSU purple <https://en.wikipedia.org/wiki/Shades_of_purple#KSU_Purple>
#512888 	31% 	15% 	51% 	266° 	55% 	33% 	71% 	53%
Languid lavender
<https://en.wikipedia.org/wiki/Lavender_(color)#Languid_lavender>
#D6CADD 	84% 	79% 	87% 	278° 	22% 	83% 	9% 	87%
Lapis lazuli
<https://en.wikipedia.org/wiki/Shades_of_azure#Lapis_lazuli>
#26619C 	15% 	38% 	61% 	210° 	61% 	38% 	76% 	61%
Laser lemon <https://en.wikipedia.org/wiki/Lemon_(color)#Laser_lemon>
#FFFF66 	100% 	100% 	40% 	60° 	100% 	70% 	60% 	100%
Laurel green
<https://en.wikipedia.org/wiki/Shades_of_green#Laurel_green>
#A9BA9D 	66% 	73% 	62% 	95° 	17% 	67% 	16% 	73%
Lava <https://en.wikipedia.org/wiki/Lava_(color)> 	#CF1020 	81% 	6%
13% 	355° 	86% 	44% 	92% 	81%
Lavender (floral)
<https://en.wikipedia.org/wiki/Lavender_(color)#Lavender_(floral)>
#B57EDC 	71% 	49% 	86% 	275° 	57% 	68% 	43% 	86%
Lavender (web) <https://en.wikipedia.org/wiki/Lavender_(color)>
#E6E6FA 	90% 	90% 	98% 	240° 	67% 	94% 	8% 	98%
Lavender blue
<https://en.wikipedia.org/wiki/Lavender_(color)#Lavender_blue>
#CCCCFF 	80% 	80% 	100% 	240° 	100% 	90% 	20% 	100%
Lavender blush
<https://en.wikipedia.org/wiki/Lavender_(color)#Lavender_blush>
#FFF0F5 	100% 	94% 	96% 	340° 	100% 	97% 	6% 	100%
Lavender gray
<https://en.wikipedia.org/wiki/Lavender_(color)#Lavender_gray>
#C4C3D0 	77% 	76% 	82% 	245° 	12% 	79% 	6% 	82%
Lawn green
<https://en.wikipedia.org/wiki/Chartreuse_(color)#Lawn_green>
#7CFC00 	49% 	99% 	0% 	90° 	100% 	49% 	100% 	99%
Lemon <https://en.wikipedia.org/wiki/Lemon_(color)> 	#FFF700 	100%
97% 	0% 	58° 	100% 	50% 	100% 	100%
Lemon chiffon <https://en.wikipedia.org/wiki/Lemon_chiffon> 	#FFFACD
100% 	98% 	80% 	54° 	100% 	90% 	20% 	100%
Lemon curry <https://en.wikipedia.org/wiki/Lemon_(color)#Lemon_curry>
#CCA01D 	80% 	63% 	11% 	45° 	75% 	46% 	86% 	80%
Lemon glacier
<https://en.wikipedia.org/wiki/Lemon_(color)#Lemon_glacier> 	#FDFF00
99% 	100% 	0% 	60° 	100% 	50% 	100% 	100%
Lemon meringue
<https://en.wikipedia.org/wiki/Lemon_(color)#Lemon_meringue>
#F6EABE 	96% 	92% 	75% 	47° 	76% 	85% 	23% 	96%
Lemon yellow
<https://en.wikipedia.org/wiki/Lemon_(color)#Lemon_yellow> 	#FFF44F
100% 	96% 	31% 	56° 	100% 	65% 	69% 	100%
Lemon yellow (Crayola)
<https://en.wikipedia.org/wiki/Lemon_(color)#Lemon_yellow_(Crayola)>
#FFFF9F 	100% 	100% 	62% 	60° 	100% 	81% 	38% 	100%
Liberty <https://en.wikipedia.org/wiki/Shades_of_blue#Liberty>
#545AA7 	33% 	35% 	65% 	236° 	33% 	49% 	50% 	65%
Light blue <https://en.wikipedia.org/wiki/Light_blue> 	#ADD8E6 	68%
85% 	90% 	195° 	53% 	79% 	25% 	90%
Light coral <https://en.wikipedia.org/wiki/Coral_(color)#Light_coral>
#F08080 	94% 	50% 	50% 	0° 	79% 	72% 	47% 	94%
Light cornflower blue
<https://en.wikipedia.org/wiki/Cornflower_blue#Crayola> 	#93CCEA
58% 	80% 	92% 	201° 	67% 	75% 	37% 	92%
Light cyan <https://en.wikipedia.org/wiki/Shades_of_cyan#Light_cyan>
#E0FFFF 	88% 	100% 	100% 	180° 	100% 	94% 	12% 	100%
Light French beige
<https://en.wikipedia.org/wiki/Beige#Light_French_beige> 	#C8AD7F
78% 	68% 	50% 	38° 	40% 	64% 	37% 	78%
Light goldenrod yellow
<https://en.wikipedia.org/wiki/Goldenrod_(color)#Light_goldenrod_yellow> 	#FAFAD2
	98% 	98% 	82% 	60° 	80% 	90% 	16% 	98%
Light gray <https://en.wikipedia.org/wiki/Grey#Web_colors> 	#D3D3D3
83% 	83% 	83% 	—° 	0% 	83% 	0% 	83%
Light green
<https://en.wikipedia.org/wiki/X11_color_names#Color_names> 	#90EE90
56% 	93% 	56% 	120° 	73% 	75% 	39% 	93%
Light orange
<https://en.wikipedia.org/wiki/Shades_of_orange#Light_orange> 	#FED8B1
100% 	85% 	69% 	30° 	98% 	85% 	30% 	100%
Light periwinkle
<https://en.wikipedia.org/wiki/Periwinkle_(color)#Light_periwinkle>
#C5CBE1 	77% 	80% 	88% 	228° 	32% 	83% 	12% 	88%
Light pink <https://en.wikipedia.org/wiki/Shades_of_pink#Light_pink>
#FFB6C1 	100% 	71% 	76% 	351° 	100% 	86% 	29% 	100%
Light salmon
<https://en.wikipedia.org/wiki/Salmon_(color)#Light_salmon> 	#FFA07A
100% 	63% 	48% 	17° 	100% 	74% 	52% 	100%
Light sea green
<https://en.wikipedia.org/wiki/Shades_of_cyan#Light_sea_green>
#20B2AA 	13% 	70% 	67% 	177° 	70% 	41% 	82% 	70%
Light sky blue <https://en.wikipedia.org/wiki/Sky_blue#Light_sky_blue>
#87CEFA 	53% 	81% 	98% 	203° 	92% 	75% 	46% 	98%
Light slate gray
<https://en.wikipedia.org/wiki/Slate_gray#Light_slate_gray> 	#778899
47% 	53% 	60% 	210° 	14% 	53% 	22% 	60%
Light steel blue
<https://en.wikipedia.org/wiki/Steel_blue#Light_steel_blue> 	#B0C4DE
69% 	77% 	87% 	214° 	41% 	78% 	21% 	87%
Light yellow
<https://en.wikipedia.org/wiki/Shades_of_yellow#Light_yellow> 	#FFFFE0
100% 	100% 	88% 	60° 	100% 	94% 	12% 	100%
Lilac <https://en.wikipedia.org/wiki/Lilac_(color)> 	#C8A2C8 	78%
64% 	78% 	300° 	26% 	71% 	19% 	78%
Lilac Luster
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Silver_Swirls>
	#AE98AA 	68% 	60% 	67% 	311° 	12% 	64% 	13% 	68%
Lime (color wheel) <https://en.wikipedia.org/wiki/Lime_(color)>
#BFFF00 	75% 	100% 	0% 	75° 	100% 	50% 	100% 	100%
Lime (web) (X11 green)
<https://en.wikipedia.org/wiki/Lime_(color)#Web_color_%22lime%22_(X11_Green)>
	#00FF00 	0% 	100% 	0% 	120° 	100% 	50% 	100% 	100%
Lime green <https://en.wikipedia.org/wiki/Lime_(color)#Lime_green>
#32CD32 	20% 	80% 	20% 	120° 	61% 	50% 	76% 	80%
Lincoln green <https://en.wikipedia.org/wiki/Lincoln_green> 	#195905
10% 	35% 	2% 	106° 	89% 	18% 	94% 	35%
Linen <https://en.wikipedia.org/wiki/Linen_(color)> 	#FAF0E6 	98%
94% 	90% 	30° 	67% 	94% 	8% 	98%
Lion <https://en.wikipedia.org/wiki/Lion_(color)> 	#C19A6B 	76% 	60%
42% 	33° 	41% 	59% 	45% 	76%
Liseran purple
<https://en.wikipedia.org/wiki/Shades_of_purple#Liseran_purple>
#DE6FA1 	87% 	44% 	63% 	333° 	63% 	65% 	50% 	87%
Little boy blue
<https://en.wikipedia.org/wiki/Baby_blue#Little_boy_blue> 	#6CA0DC
42% 	63% 	86% 	212° 	62% 	64% 	51% 	86%
Liver <https://en.wikipedia.org/wiki/Liver_(color)> 	#674C47 	40%
30% 	28% 	9° 	18% 	34% 	31% 	40%
Liver (dogs) <https://en.wikipedia.org/wiki/Liver_(color)#In_dogs>
#B86D29 	72% 	43% 	16% 	29° 	64% 	44% 	78% 	72%
Liver (organ)
<https://en.wikipedia.org/wiki/Liver_(color)#Liver_(organ)> 	#6C2E1F
42% 	18% 	12% 	12° 	55% 	27% 	71% 	42%
Liver chestnut <https://en.wikipedia.org/wiki/Liver_(color)>
#987456 	60% 	45% 	34% 	27° 	28% 	47% 	43% 	60%
Livid <https://en.wikipedia.org/wiki/Blue-gray> 	#6699CC 	40% 	60%
80% 	210° 	50% 	60% 	50% 	80%
Macaroni and Cheese
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors> 	#FFBD88
100% 	74% 	53% 	27° 	100% 	77% 	47% 	100%
Madder Lake
<https://en.wikipedia.org/wiki/History_of_Crayola_crayons#1903:_the_original_Crayola_colors>
	#CC3336 	80% 	20% 	21% 	359° 	60% 	50% 	75% 	80%
Magenta <https://en.wikipedia.org/wiki/Magenta> 	#FF00FF 	100% 	0%
100% 	300° 	100% 	50% 	100% 	100%
Magenta (Crayola)
<https://en.wikipedia.org/wiki/Shades_of_magenta#Magenta_(Crayola)>
#F653A6 	96% 	33% 	65% 	329° 	90% 	65% 	66% 	97%
Magenta (dye)
<https://en.wikipedia.org/wiki/Shades_of_magenta#Magenta_dye_(original_variation)_(1860)>
	#CA1F7B 	79% 	12% 	48% 	328° 	73% 	46% 	85% 	79%
Magenta (Pantone)
<https://en.wikipedia.org/wiki/Shades_of_magenta#Magenta_(Pantone)>
#D0417E 	82% 	25% 	49% 	334° 	60% 	54% 	69% 	82%
Magenta (process)
<https://en.wikipedia.org/wiki/Magenta#Process_magenta_(pigment_magenta;_printer's_magenta)_(1890s)>
	#FF0090 	100% 	0% 	56% 	326° 	100% 	50% 	100% 	100%
Magenta haze
<https://en.wikipedia.org/wiki/Shades_of_magenta#Magenta_haze>
#9F4576 	62% 	27% 	46% 	327° 	39% 	45% 	57% 	62%
Magic mint
<https://en.wikipedia.org/wiki/Spring_green_(color)#Magic_mint>
#AAF0D1 	67% 	94% 	82% 	153° 	70% 	80% 	29% 	94%
Magnolia <https://en.wikipedia.org/wiki/Magnolia_(color)> 	#F2E8D7
95% 	91% 	84% 	38° 	51% 	90% 	11% 	95%
Mahogany <https://en.wikipedia.org/wiki/Mahogany_(color)> 	#C04000
75% 	25% 	0% 	20° 	100% 	38% 	100% 	75%
Maize <https://en.wikipedia.org/wiki/Maize_(color)> 	#FBEC5D 	98%
93% 	36% 	54° 	95% 	67% 	63% 	98%
Maize (Crayola)
<https://en.wikipedia.org/wiki/Maize_(color)#Maize_(Crayola)>
#F2C649 	95% 	78% 	29% 	44° 	87% 	62% 	70% 	95%
Majorelle blue <https://en.wikipedia.org/wiki/Majorelle_Blue>
#6050DC 	38% 	31% 	86% 	247° 	67% 	59% 	64% 	86%
Malachite <https://en.wikipedia.org/wiki/Shades_of_green#Malachite>
#0BDA51 	4% 	85% 	32% 	140° 	90% 	45% 	95% 	85%
Manatee
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#979AAA 	59% 	60% 	67% 	231° 	10% 	63% 	11% 	67%
Mandarin
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Pearl_Brite>
#F37A48 	95% 	48% 	28% 	18° 	88% 	62% 	70% 	95%
Mango <https://en.wikipedia.org/wiki/Shades_of_yellow#Mango>
#FDBE02 	99% 	75% 	1% 	46° 	98% 	50% 	99% 	99%
Mango Tango
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#FF8243 	100% 	51% 	26% 	20° 	100% 	63% 	74% 	100%
Mantis <https://en.wikipedia.org/wiki/Shades_of_green#Mantis>
#74C365 	45% 	76% 	40% 	110° 	44% 	58% 	48% 	76%
Mardi Gras <https://en.wikipedia.org/wiki/Shades_of_purple#Mardi_Gras>
#880085 	53% 	0% 	52% 	301° 	100% 	27% 	100% 	53%
Marigold <https://en.wikipedia.org/wiki/Marigold_(color)> 	#EAA221
92% 	64% 	13% 	39° 	83% 	52% 	85% 	91%
Maroon (Crayola) <https://en.wikipedia.org/wiki/Maroon#Bright_maroon>
#C32148 	76% 	13% 	28% 	346° 	71% 	45% 	83% 	76%
Maroon (web) <https://en.wikipedia.org/wiki/Maroon> 	#800000 	50%
0% 	0% 	0° 	100% 	25% 	100% 	50%
Maroon (X11)
<https://en.wikipedia.org/wiki/Maroon#Rich_maroon_(maroon_(X11))>
#B03060 	69% 	19% 	38% 	338° 	57% 	44% 	73% 	69%
Mauve <https://en.wikipedia.org/wiki/Mauve> 	#E0B0FF 	88% 	69% 	100%
276° 	100% 	85% 	31% 	100%
Mauve taupe <https://en.wikipedia.org/wiki/Taupe#Mauve_taupe>
#915F6D 	57% 	37% 	43% 	343° 	21% 	47% 	34% 	57%
Mauvelous
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#EF98AA 	94% 	60% 	67% 	348° 	73% 	77% 	36% 	94%
Maximum blue
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#47ABCC 	28% 	67% 	80% 	195° 	57% 	54% 	65% 	80%
Maximum blue green
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#30BFBF 	19% 	75% 	75% 	180° 	60% 	47% 	75% 	75%
Maximum blue purple
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#ACACE6 	67% 	67% 	90% 	240° 	54% 	79% 	25% 	90%
Maximum green
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#5E8C31 	37% 	55% 	19% 	90° 	48% 	37% 	65% 	55%
Maximum green yellow
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#D9E650 	85% 	90% 	31% 	65° 	75% 	61% 	65% 	90%
Maximum purple
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#733380 	45% 	20% 	50% 	290° 	43% 	35% 	60% 	50%
Maximum red
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#D92121 	85% 	13% 	13% 	0° 	74% 	49% 	85% 	85%
Maximum red purple
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#A63A79 	65% 	23% 	47% 	325° 	48% 	44% 	65% 	65%
Maximum yellow
<https://en.wikipedia.org/wiki/Shades_of_yellow#Maximum_yellow>
#FAFA37 	98% 	98% 	22% 	60° 	95% 	60% 	78% 	98%
Maximum yellow red
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#F2BA49 	95% 	73% 	29% 	40° 	87% 	62% 	70% 	95%
May green <https://en.wikipedia.org/wiki/Spring_bud#May_green>
#4C9141 	30% 	57% 	25% 	112° 	38% 	41% 	55% 	57%
Maya blue <https://en.wikipedia.org/wiki/Maya_blue> 	#73C2FB 	45%
76% 	98% 	205° 	94% 	72% 	54% 	98%
Medium aquamarine <https://en.wikipedia.org/wiki/Aquamarine_(color)>
#66DDAA 	40% 	87% 	67% 	154° 	64% 	63% 	54% 	87%
Medium blue <https://en.wikipedia.org/wiki/Shades_of_blue#Medium_blue>
#0000CD 	0% 	0% 	80% 	240° 	100% 	40% 	100% 	80%
Medium candy apple red
<https://en.wikipedia.org/wiki/Candy_apple_red_(color)#Medium_candy_apple_red>
	#E2062C 	89% 	2% 	17% 	350° 	95% 	45% 	97% 	89%
Medium carmine
<https://en.wikipedia.org/wiki/Carmine_(color)#Medium_Carmine>
#AF4035 	69% 	25% 	21% 	5° 	54% 	45% 	70% 	69%
Medium champagne
<https://en.wikipedia.org/wiki/Champagne_(color)#Medium_champagne>
#F3E5AB 	95% 	90% 	67% 	48° 	75% 	81% 	30% 	95%
Medium orchid
<https://en.wikipedia.org/wiki/X11_color_names#Color_names> 	#BA55D3
73% 	33% 	83% 	288° 	59% 	58% 	60% 	83%
Medium purple
<https://en.wikipedia.org/wiki/Shades_of_purple#Medium_purple_(X11)>
#9370DB 	58% 	44% 	86% 	260° 	60% 	65% 	49% 	86%
Medium sea green
<https://en.wikipedia.org/wiki/Spring_green_(color)#Medium_sea_green>
#3CB371 	24% 	70% 	44% 	147° 	50% 	47% 	66% 	70%
Medium slate blue
<https://en.wikipedia.org/wiki/X11_color_names#Color_names> 	#7B68EE
48% 	41% 	93% 	249° 	80% 	67% 	56% 	93%
Medium spring green
<https://en.wikipedia.org/wiki/Spring_green_(color)#Medium_spring_green> 	#00FA9A
	0% 	98% 	60% 	157° 	100% 	49% 	100% 	98%
Medium turquoise
<https://en.wikipedia.org/wiki/Turquoise_(color)#Medium_turquoise>
#48D1CC 	28% 	82% 	80% 	178° 	60% 	55% 	66% 	82%
Medium violet-red <https://en.wikipedia.org/wiki/Red-violet>
#C71585 	78% 	8% 	52% 	322° 	81% 	43% 	89% 	78%
Mellow apricot
<https://en.wikipedia.org/wiki/Apricot_(color)#Mellow_apricot>
#F8B878 	97% 	72% 	47% 	30° 	90% 	72% 	52% 	97%
Mellow yellow
<https://en.wikipedia.org/wiki/Shades_of_yellow#Mellow_yellow>
#F8DE7E 	97% 	87% 	49% 	47° 	90% 	73% 	49% 	97%
Melon <https://en.wikipedia.org/wiki/Shades_of_orange#Melon>
#FEBAAD 	100% 	73% 	68% 	10° 	98% 	84% 	32% 	100%
Metallic gold
<https://en.wikipedia.org/wiki/Gold_(color)#Metallic_gold> 	#D3AF37
83% 	69% 	22% 	46° 	64% 	52% 	74% 	83%
Metallic Seaweed
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Metallic_FX>
#0A7E8C 	4% 	49% 	55% 	186° 	87% 	29% 	93% 	55%
Metallic Sunburst
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Metallic_FX>
#9C7C38 	61% 	49% 	22% 	41° 	47% 	42% 	64% 	61%
Mexican pink <https://en.wikipedia.org/wiki/Mexican_pink> 	#E4007C
89% 	0% 	49% 	327° 	100% 	45% 	100% 	89%
Middle blue
<https://en.wikipedia.org/wiki/History_of_Crayola_crayons#Munsell_Crayola,_1926%E2%80%931944>
	#7ED4E6 	49% 	83% 	90% 	190° 	68% 	70% 	45% 	90%
Middle blue green
<https://en.wikipedia.org/wiki/History_of_Crayola_crayons#Munsell_Crayola,_1926%E2%80%931944>
	#8DD9CC 	55% 	85% 	80% 	170° 	50% 	70% 	35% 	85%
Middle blue purple
<https://en.wikipedia.org/wiki/History_of_Crayola_crayons#Munsell_Crayola,_1926%E2%80%931944>
	#8B72BE 	55% 	45% 	75% 	260° 	37% 	60% 	40% 	75%
Middle grey
<https://en.wikipedia.org/wiki/History_of_Crayola_crayons#Munsell_Crayola,_1926%E2%80%931944>
	#8B8680 	55% 	53% 	50% 	33° 	5% 	52% 	8% 	55%
Middle green
<https://en.wikipedia.org/wiki/History_of_Crayola_crayons#Munsell_Crayola,_1926%E2%80%931944>
	#4D8C57 	30% 	55% 	34% 	130° 	29% 	43% 	45% 	55%
Middle green yellow
<https://en.wikipedia.org/wiki/History_of_Crayola_crayons#Munsell_Crayola,_1926%E2%80%931944>
	#ACBF60 	67% 	75% 	38% 	72° 	43% 	56% 	50% 	75%
Middle purple
<https://en.wikipedia.org/wiki/History_of_Crayola_crayons#Munsell_Crayola,_1926%E2%80%931944>
	#D982B5 	85% 	51% 	71% 	325° 	53% 	68% 	40% 	85%
Middle red
<https://en.wikipedia.org/wiki/History_of_Crayola_crayons#Munsell_Crayola,_1926%E2%80%931944>
	#E58E73 	90% 	56% 	45% 	15° 	69% 	68% 	50% 	90%
Middle red purple
<https://en.wikipedia.org/wiki/History_of_Crayola_crayons#Munsell_Crayola,_1926%E2%80%931944>
	#A55353 	65% 	33% 	33% 	0° 	33% 	49% 	50% 	65%
Middle yellow
<https://en.wikipedia.org/wiki/History_of_Crayola_crayons#Munsell_Crayola,_1926%E2%80%931944>
	#FFEB00 	100% 	92% 	0% 	55° 	100% 	50% 	100% 	100%
Middle yellow red
<https://en.wikipedia.org/wiki/History_of_Crayola_crayons#Munsell_Crayola,_1926%E2%80%931944>
	#ECB176 	93% 	69% 	46% 	30° 	76% 	69% 	50% 	93%
Midnight
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Pearl_Brite>
#702670 	44% 	15% 	44% 	300° 	49% 	29% 	66% 	44%
Midnight blue <https://en.wikipedia.org/wiki/Midnight_blue> 	#191970
10% 	10% 	44% 	240° 	64% 	27% 	78% 	44%
Midnight green (eagle green)
<https://en.wikipedia.org/wiki/Shades_of_green#Midnight_green>
#004953 	0% 	29% 	33% 	187° 	100% 	16% 	100% 	33%
Mikado yellow <https://en.wikipedia.org/wiki/Mikado_yellow> 	#FFC40C
100% 	77% 	5% 	45° 	100% 	52% 	95% 	100%
Mimi pink <https://en.wikipedia.org/wiki/Shades_of_pink#Mimi_Pink>
#FFDAE9 	100% 	85% 	91% 	336° 	100% 	93% 	15% 	100%
Mindaro <https://en.wikipedia.org/wiki/Chartreuse_(color)#Mindaro>
#E3F988 	89% 	98% 	53% 	72° 	90% 	75% 	45% 	98%
Ming <https://en.wikipedia.org/wiki/Blue-green#Ming> 	#36747D 	21%
45% 	49% 	188° 	40% 	35% 	56% 	49%
Minion yellow <https://en.wikipedia.org/wiki/Minions_(film)#Marketing>
#F5E050 	96% 	86% 	31% 	52° 	89% 	64% 	67% 	96%
Mint <https://en.wikipedia.org/wiki/Spring_green_(color)#Mint>
#3EB489 	24% 	71% 	54% 	158° 	49% 	47% 	66% 	71%
Mint cream
<https://en.wikipedia.org/wiki/Spring_green_(color)#Mint_cream>
#F5FFFA 	96% 	100% 	98% 	150° 	100% 	98% 	4% 	100%
Mint green
<https://en.wikipedia.org/wiki/Spring_green_(color)#Mint_green>
#98FF98 	60% 	100% 	60% 	120° 	100% 	80% 	40% 	100%
Misty moss
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Silver_Swirls>
	#BBB477 	73% 	71% 	47% 	54° 	33% 	60% 	36% 	73%
Misty rose <https://en.wikipedia.org/wiki/Rose_(color)#Misty_rose>
#FFE4E1 	100% 	89% 	88% 	6° 	100% 	94% 	12% 	100%
Mode beige <https://en.wikipedia.org/wiki/Beige#Mode_beige> 	#967117
59% 	44% 	9% 	43° 	73% 	34% 	85% 	59%
Morning blue
<https://en.wikipedia.org/wiki/Shades_of_blue#Morning_blue> 	#8DA399
55% 	64% 	60% 	153° 	11% 	60% 	14% 	64%
Moss green <https://en.wikipedia.org/wiki/Shades_of_green#Moss_green>
#8A9A5B 	54% 	60% 	36% 	75° 	26% 	48% 	41% 	60%
Mountain Meadow
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#30BA8F 	19% 	73% 	56% 	161° 	59% 	46% 	74% 	73%
Mountbatten pink <https://en.wikipedia.org/wiki/Mountbatten_pink>
#997A8D 	60% 	48% 	55% 	323° 	13% 	54% 	20% 	60%
MSU green <https://en.wikipedia.org/wiki/Shades_of_green#MSU_green>
#18453B 	9% 	27% 	23% 	167° 	48% 	18% 	65% 	27%
Mulberry <https://en.wikipedia.org/wiki/Shades_of_purple#Mulberry>
#C54B8C 	77% 	29% 	55% 	328° 	51% 	53% 	62% 	77%
Mulberry (Crayola)
<https://en.wikipedia.org/wiki/Shades_of_purple#Mulberry_(Crayola)>
#C8509B 	78% 	31% 	61% 	323° 	52% 	55% 	60% 	78%
Mustard <https://en.wikipedia.org/wiki/Mustard_(color)> 	#FFDB58
100% 	86% 	35% 	47° 	100% 	67% 	65% 	100%
Myrtle green
<https://en.wikipedia.org/wiki/Shades_of_green#Myrtle_green>
#317873 	19% 	47% 	45% 	176° 	42% 	33% 	59% 	47%
Mystic
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Pearl_Brite>
#D65282 	84% 	32% 	51% 	338° 	62% 	58% 	62% 	84%
Mystic maroon
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Silver_Swirls>
	#AD4379 	68% 	26% 	47% 	329° 	44% 	47% 	62% 	68%
Nadeshiko pink <https://en.wikipedia.org/wiki/Shades_of_pink>
#F6ADC6 	96% 	68% 	78% 	339° 	80% 	82% 	80% 	82%
Naples yellow <https://en.wikipedia.org/wiki/Naples_yellow> 	#FADA5E
98% 	85% 	37% 	48° 	94% 	67% 	62% 	98%
Navajo white <https://en.wikipedia.org/wiki/Navajo_white> 	#FFDEAD
100% 	87% 	68% 	36° 	100% 	84% 	32% 	100%
Navy blue <https://en.wikipedia.org/wiki/Navy_blue> 	#000080 	0% 	0%
50% 	240° 	100% 	25% 	100% 	50%
Navy blue (Crayola)
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#1974D2 	10% 	45% 	82% 	210° 	79% 	46% 	88% 	82%
Neon blue <https://en.wikipedia.org/wiki/Shades_of_blue#Neon_blue>
#4666FF 	27% 	40% 	100% 	230° 	100% 	64% 	73% 	100%
Neon Carrot <https://en.wikipedia.org/wiki/Neon_Carrot> 	#FFA343
100% 	64% 	26% 	31° 	100% 	63% 	74% 	100%
Neon green <https://en.wikipedia.org/wiki/Shades_of_green#Neon_green>
#39FF14 	22% 	100% 	8% 	111° 	100% 	54% 	92% 	100%
Neon fuchsia
<https://en.wikipedia.org/wiki/Fuchsia_(color)#Neon_fuchsia>
#FE4164 	100% 	25% 	39% 	349° 	99% 	63% 	74% 	100%
New York pink
<https://en.wikipedia.org/wiki/Shades_of_pink#New_York_pink>
#D7837F 	84% 	51% 	50% 	3° 	52% 	67% 	41% 	84%
Nickel <https://en.wikipedia.org/wiki/Shades_of_gray#Nickel>
#727472 	45% 	45% 	45% 	120° 	1% 	45% 	2% 	46%
Non-photo blue <https://en.wikipedia.org/wiki/Non-photo_blue>
#A4DDED 	64% 	87% 	93% 	193° 	67% 	79% 	31% 	93%
Nyanza <https://en.wikipedia.org/wiki/Chartreuse_(color)#Nyanza>
#E9FFDB 	91% 	100% 	86% 	97° 	100% 	93% 	14% 	100%
Ocean Blue <https://en.wikipedia.org/wiki/Turquoise_Pearl> 	#4F42B5
31% 	26% 	71% 	247° 	47% 	48% 	64% 	71%
Ocean green <https://en.wikipedia.org/wiki/Turquoise_Pearl> 	#48BF91
28% 	75% 	57% 	157° 	48% 	52% 	62% 	75%
Ochre <https://en.wikipedia.org/wiki/Ochre> 	#CC7722 	80% 	47% 	13%
30° 	71% 	47% 	83% 	80%
Old burgundy
<https://en.wikipedia.org/wiki/Burgundy_(color)#Old_burgundy>
#43302E 	26% 	19% 	18% 	6° 	19% 	22% 	31% 	26%
Old gold <https://en.wikipedia.org/wiki/Old_gold> 	#CFB53B 	81% 	71%
23% 	49° 	61% 	52% 	71% 	81%
Old lace <https://en.wikipedia.org/wiki/Shades_of_white#Old_lace>
#FDF5E6 	99% 	96% 	90% 	39° 	85% 	95% 	9% 	99%
Old lavender
<https://en.wikipedia.org/wiki/Lavender_(color)#Old_lavender>
#796878 	47% 	41% 	47% 	304° 	8% 	44% 	14% 	47%
Old mauve <https://en.wikipedia.org/wiki/Mauve#Old_mauve> 	#673147
40% 	19% 	28% 	336° 	36% 	30% 	52% 	40%
Old rose <https://en.wikipedia.org/wiki/Rose_(color)#Old_rose>
#C08081 	75% 	50% 	51% 	359° 	34% 	63% 	33% 	75%
Old silver <https://en.wikipedia.org/wiki/Silver_(color)#Old_silver>
#848482 	52% 	52% 	51% 	60° 	1% 	51% 	2% 	52%
Olive <https://en.wikipedia.org/wiki/Olive_(color)> 	#808000 	50%
50% 	0% 	60° 	100% 	25% 	100% 	50%
Olive Drab (∞3) <https://en.wikipedia.org/wiki/Olive_drab> 	#6B8E23
42% 	56% 	14% 	80° 	61% 	35% 	75% 	56%
Olive Drab ∞7 <https://en.wikipedia.org/wiki/Olive_drab> 	#3C341F
24% 	20% 	12% 	43° 	32% 	18% 	48% 	24%
Olive green <https://en.wikipedia.org/wiki/Olive_(color)#Olive_green>
#B5B35C 	71% 	70% 	36% 	59° 	38% 	54% 	49% 	71%
Olivine <https://en.wikipedia.org/wiki/Olive_(color)#Olivine>
#9AB973 	60% 	73% 	45% 	87° 	33% 	59% 	38% 	73%
Onyx <https://en.wikipedia.org/wiki/Shades_of_black_(colors)#Onyx>
#353839 	21% 	22% 	22% 	195° 	4% 	22% 	7% 	22%
Opal <https://en.wikipedia.org/wiki/Shades_of_gray#Opal> 	#A8C3BC
66% 	76% 	74% 	164° 	18% 	71% 	14% 	76%
Opera mauve <https://en.wikipedia.org/wiki/Mauve#Opera_mauve>
#B784A7 	72% 	52% 	65% 	319° 	26% 	62% 	28% 	72%
Orange <https://en.wikipedia.org/wiki/Orange_(colour)> 	#FF7F00
100% 	50% 	0% 	30° 	100% 	50% 	100% 	100%
Orange (Crayola)
<https://en.wikipedia.org/wiki/Shades_of_orange#Orange_(Crayola)>
#FF7538 	100% 	46% 	22% 	18° 	100% 	61% 	78% 	100%
Orange (Pantone)
<https://en.wikipedia.org/wiki/Shades_of_orange#Orange_(Pantone)>
#FF5800 	100% 	35% 	0% 	21° 	100% 	50% 	100% 	100%
Orange (web)
<https://en.wikipedia.org/wiki/Shades_of_orange#Orange_(web_color)>
#FFA500 	100% 	65% 	0% 	39° 	100% 	50% 	100% 	100%
Orange peel <https://en.wikipedia.org/wiki/Orange_peel_(color)>
#FF9F00 	100% 	62% 	0% 	37° 	100% 	50% 	100% 	100%
Orange-red <https://en.wikipedia.org/wiki/Vermilion#Orange-red>
#FF681F 	100% 	41% 	12% 	20° 	100% 	56% 	88% 	100%
Orange-red (Crayola) <https://en.wikipedia.org/wiki/Vermilion>
#FF5349 	100% 	33% 	29% 	4° 	100% 	64% 	71% 	100%
Orange soda
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Heads_'n_Tails>
	#FA5B3D 	98% 	36% 	24% 	10° 	95% 	61% 	76% 	98%
Orange-yellow
<https://en.wikipedia.org/wiki/Marigold_(color)#Orange-yellow>
#F5BD1F 	96% 	74% 	12% 	44° 	92% 	54% 	87% 	96%
Orange-yellow (Crayola)
<https://en.wikipedia.org/wiki/Marigold_(color)#Orange-yellow_(Crayola)> 	#F8D568
	97% 	84% 	41% 	45° 	91% 	69% 	58% 	97%
Orchid <https://en.wikipedia.org/wiki/Orchid_(color)> 	#DA70D6 	85%
44% 	84% 	302° 	59% 	65% 	49% 	85%
Orchid pink <https://en.wikipedia.org/wiki/Orchid_(color)#Orchid_pink>
#F2BDCD 	95% 	74% 	80% 	342° 	67% 	85% 	22% 	95%
Orchid (Crayola) <https://en.wikipedia.org/wiki/Orchid_(color)>
#E29CD2 	89% 	61% 	82% 	314° 	55% 	75% 	31% 	89%
Outer space (Crayola)
<https://en.wikipedia.org/wiki/Shades_of_black#Outer_space_(Crayola)>
#2D383A 	18% 	22% 	23% 	189° 	13% 	20% 	22% 	23%
Outrageous Orange
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Fluorescent_crayons>
	#FF6E4A 	100% 	43% 	29% 	12° 	100% 	65% 	71% 	100%
Oxblood <https://en.wikipedia.org/wiki/Oxblood> 	#4A0000 	29% 	0%
0% 	0° 	100% 	15% 	100% 	29%
Oxford blue <https://en.wikipedia.org/wiki/Oxford_Blue_(colour)>
#002147 	0% 	13% 	28% 	212° 	100% 	14% 	100% 	28%
OU Crimson red
<https://en.wikipedia.org/wiki/Shades_of_red#OU_crimson> 	#841617
52% 	9% 	9% 	360° 	71% 	30% 	83% 	52%
Pacific blue
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#1CA9C9 	11% 	66% 	79% 	191° 	76% 	45% 	86% 	79%
Pakistan green
<https://en.wikipedia.org/wiki/Shades_of_green#Pakistan_green>
#006600 	0% 	40% 	0% 	120° 	100% 	20% 	100% 	40%
Palatinate purple <https://en.wikipedia.org/wiki/Palatinate_(colour)>
#682860 	41% 	16% 	38% 	308° 	44% 	28% 	62% 	41%
Pale aqua <https://en.wikipedia.org/wiki/Aqua_(color)#Pale_aqua>
#BCD4E6 	74% 	83% 	90% 	206° 	46% 	82% 	18% 	90%
Pale cerulean <https://en.wikipedia.org/wiki/Cerulean#Pale_cerulean>
#9BC4E2 	61% 	77% 	89% 	205° 	55% 	75% 	31% 	89%
Pale Dogwood
<https://en.wikipedia.org/wiki/Shades_of_pink#Pale_Dogwood> 	#ED7A9B
93% 	48% 	61% 	334° 	76% 	70% 	48% 	92%
Pale pink <https://en.wikipedia.org/wiki/Shades_of_pink#Pale_pink>
#FADADD 	98% 	85% 	87% 	354° 	76% 	92% 	13% 	98%
Pale purple (Pantone)
<https://en.wikipedia.org/wiki/Shades_of_purple#Pale_purple>
#FAE6FA 	98% 	90% 	98% 	300° 	67% 	94% 	8% 	98%
Pale silver <https://en.wikipedia.org/wiki/Silver_(color)#Pale_silver>
#C9C0BB 	79% 	75% 	73% 	21° 	12% 	76% 	7% 	79%
Pale spring bud
<https://en.wikipedia.org/wiki/Spring_bud#Pale_spring_bud> 	#ECEBBD
93% 	92% 	74% 	59° 	55% 	83% 	20% 	93%
Pansy purple
<https://en.wikipedia.org/wiki/Shades_of_purple#Pansy_purple>
#78184A 	47% 	9% 	29% 	329° 	67% 	28% 	80% 	47%
Paolo Veronese green
<https://en.wikipedia.org/wiki/Viridian#Paolo_Veronese_green>
#009B7D 	0% 	61% 	49% 	168° 	100% 	30% 	100% 	61%
Papaya whip <https://en.wikipedia.org/wiki/Papaya_whip> 	#FFEFD5
100% 	94% 	84% 	37° 	100% 	92% 	16% 	100%
Paradise pink
<https://en.wikipedia.org/wiki/Shades_of_pink#Paradise_pink>
#E63E62 	90% 	24% 	38% 	347° 	77% 	57% 	73% 	90%
Parchment <https://en.wikipedia.org/wiki/Shades_of_white#Parchment>
#F1E9D2 	95% 	91% 	82% 	45° 	53% 	88% 	13% 	95%
Paris Green <https://en.wikipedia.org/wiki/Paris_green> 	#50C878
31% 	78% 	47% 	140° 	52% 	55% 	60% 	78%
Pastel pink <https://en.wikipedia.org/wiki/Shades_of_pink#Pastel_pink>
#DEA5A4 	87% 	65% 	64% 	1° 	47% 	76% 	26% 	87%
Patriarch
<https://en.wikipedia.org/wiki/Shades_of_purple#Purple_(HTML/CSS_color)_(patriarch)>
	#800080 	50% 	0% 	50% 	300° 	100% 	25% 	100% 	50%
Payne's grey <https://en.wikipedia.org/wiki/Payne%27s_grey> 	#536878
33% 	41% 	47% 	206° 	18% 	40% 	31% 	47%
Peach <https://en.wikipedia.org/wiki/Peach_(color)> 	#FFE5B4 	100%
90% 	71% 	39° 	100% 	85% 	29% 	100%
Peach (Crayola) <https://en.wikipedia.org/wiki/Peach_(color)#Peach>
#FFCBA4 	100% 	80% 	64% 	26° 	100% 	82% 	36% 	100%
Peach puff <https://en.wikipedia.org/wiki/Peach_(color)#Peach_puff>
#FFDAB9 	100% 	85% 	73% 	28° 	100% 	86% 	27% 	100%
Pear <https://en.wikipedia.org/wiki/Chartreuse_(color)#Pear>
#D1E231 	82% 	89% 	19% 	66° 	75% 	54% 	78% 	89%
Pearly purple
<https://en.wikipedia.org/wiki/Shades_of_purple#Pearly_purple>
#B768A2 	72% 	41% 	64% 	316° 	35% 	56% 	43% 	72%
Periwinkle <https://en.wikipedia.org/wiki/Periwinkle_(color)>
#CCCCFF 	80% 	80% 	100% 	240° 	100% 	90% 	20% 	100%
Periwinkle (Crayola)
<https://en.wikipedia.org/wiki/Periwinkle_(color)#Periwinkle_(Crayola)> 	#C3CDE6
	76% 	80% 	90% 	223° 	41% 	83% 	15% 	90%
Permanent Geranium Lake
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#E12C2C 	88% 	17% 	17% 	0° 	75% 	53% 	80% 	88%
Persian blue <https://en.wikipedia.org/wiki/Persian_blue> 	#1C39BB
11% 	22% 	73% 	229° 	74% 	42% 	85% 	73%
Persian green
<https://en.wikipedia.org/wiki/Shades_of_green#Persian_green>
#00A693 	0% 	65% 	58% 	173° 	100% 	33% 	100% 	65%
Persian indigo
<https://en.wikipedia.org/wiki/Persian_blue#Persian_indigo> 	#32127A
20% 	7% 	48% 	258° 	74% 	27% 	85% 	48%
Persian orange
<https://en.wikipedia.org/wiki/Shades_of_orange#Persian_orange>
#D99058 	85% 	56% 	35% 	26° 	63% 	60% 	59% 	85%
Persian pink <https://en.wikipedia.org/wiki/Rose_(color)#Persian_pink>
#F77FBE 	97% 	50% 	75% 	329° 	88% 	73% 	49% 	97%
Persian plum
<https://en.wikipedia.org/wiki/Plum_(color)#Persian_plum_(prune)>
#701C1C 	44% 	11% 	11% 	0° 	60% 	27% 	75% 	44%
Persian red <https://en.wikipedia.org/wiki/Persian_red> 	#CC3333
80% 	20% 	20% 	0° 	60% 	50% 	75% 	80%
Persian rose <https://en.wikipedia.org/wiki/Rose_(color)#Persian_rose>
#FE28A2 	100% 	16% 	64% 	326° 	99% 	58% 	84% 	100%
Persimmon <https://en.wikipedia.org/wiki/Shades_of_orange#Persimmon>
#EC5800 	93% 	35% 	0% 	22° 	100% 	46% 	100% 	93%
Pewter Blue
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Silver_Swirls>
	#8BA8B7 	55% 	66% 	72% 	200° 	23% 	63% 	24% 	72%
Phlox
<https://en.wikipedia.org/wiki/Shades_of_purple#Psychedelic_purple_(phlox)>
	#DF00FF 	87% 	0% 	100% 	292° 	100% 	50% 	100% 	100%
Phthalo blue <https://en.wikipedia.org/wiki/Phthalocyanine_Blue_BN>
#000F89 	0% 	6% 	54% 	233° 	100% 	27% 	100% 	54%
Phthalo green <https://en.wikipedia.org/wiki/Phthalocyanine_Green_G>
#123524 	7% 	21% 	14% 	151° 	49% 	14% 	66% 	21%
Picotee blue
<https://en.wikipedia.org/wiki/Shades_of_blue#Picotee_blue> 	#2E2787
18% 	15% 	53% 	244° 	55% 	34% 	71% 	53%
Pictorial carmine
<https://en.wikipedia.org/wiki/Carmine_(color)#Pictorial_carmine>
#C30B4E 	76% 	4% 	31% 	338° 	89% 	40% 	94% 	76%
Piggy pink <https://en.wikipedia.org/wiki/Shades_of_pink#Piggy_pink>
#FDDDE6 	99% 	87% 	90% 	343° 	89% 	93% 	13% 	99%
Pine green <https://en.wikipedia.org/wiki/Shades_of_green#Pine_green>
#01796F 	0% 	47% 	44% 	175° 	98% 	24% 	99% 	47%
Pine tree <https://en.wikipedia.org/wiki/Shades_of_green#Pine_tree>
#2A2F23 	16% 	18% 	14% 	85° 	15% 	16% 	26% 	18%
Pink <https://en.wikipedia.org/wiki/Pink> 	#FFC0CB 	100% 	75% 	80%
350° 	100% 	88% 	25% 	100%
Pink (Pantone)
<https://en.wikipedia.org/wiki/Shades_of_pink#Pink_(Pantone)>
#D74894 	84% 	28% 	58% 	328° 	64% 	56% 	67% 	84%
Pink flamingo <https://en.wikipedia.org/wiki/Manatee_(color)>
#FC74FD 	99% 	45% 	99% 	300° 	97% 	72% 	54% 	99%
Pink lace <https://en.wikipedia.org/wiki/Shades_of_pink#Pink_lace>
#FFDDF4 	100% 	87% 	96% 	319° 	100% 	93% 	13% 	100%
Pink lavender
<https://en.wikipedia.org/wiki/Shades_of_pink#Pink_lavender>
#D8B2D1 	85% 	70% 	82% 	311° 	33% 	77% 	18% 	85%
Pink Sherbet
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors>
#F78FA7 	97% 	56% 	65% 	346° 	87% 	76% 	42% 	97%
Pistachio <https://en.wikipedia.org/wiki/Chartreuse_(color)#Pistachio>
#93C572 	58% 	77% 	45% 	96° 	42% 	61% 	42% 	77%
Platinum <https://en.wikipedia.org/wiki/Platinum_(color)> 	#E5E4E2
90% 	89% 	89% 	40° 	6% 	89% 	1% 	90%
Plum <https://en.wikipedia.org/wiki/Plum_(color)> 	#8E4585 	56% 	27%
52% 	307° 	35% 	41% 	51% 	56%
Plum (web) <https://en.wikipedia.org/wiki/Plum_(color)#Pale_plum>
#DDA0DD 	87% 	63% 	87% 	300° 	47% 	75% 	28% 	87%
Plump Purple
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Heads_'n_Tails>
	#5946B2 	35% 	27% 	70% 	251° 	44% 	49% 	61% 	70%
Polished Pine
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Silver_Swirls>
	#5DA493 	36% 	64% 	58% 	166° 	28% 	50% 	43% 	64%
Pomp and Power
<https://en.wikipedia.org/wiki/Shades_of_purple#Pomp_and_Power>
#86608E 	53% 	38% 	56% 	290° 	19% 	47% 	32% 	56%
Popstar <https://en.wikipedia.org/wiki/Red-violet#Popstar> 	#BE4F62
75% 	31% 	38% 	350° 	46% 	53% 	58% 	75%
Portland Orange <https://en.wikipedia.org/wiki/Portland_Orange>
#FF5A36 	100% 	35% 	21% 	11° 	100% 	61% 	79% 	100%
Powder blue <https://en.wikipedia.org/wiki/Powder_blue> 	#B0E0E6
69% 	88% 	90% 	187° 	52% 	80% 	23% 	90%
Princeton orange
<https://en.wikipedia.org/wiki/Shades_of_orange#Princeton_orange>
#F58025 	96% 	50% 	15% 	26° 	91% 	55% 	85% 	96%
Process yellow
<https://en.wikipedia.org/wiki/Shades_of_yellow#Yellow_(CMYK)_(process_yellow)_(canary_yellow)>
	#FFEF00 	100% 	94% 	0% 	56° 	100% 	50% 	100% 	100%
Prune
<https://en.wikipedia.org/wiki/Plum_(color)#Persian_plum_(prune)>
#701C1C 	44% 	11% 	11% 	0° 	60% 	27% 	75% 	44%
Prussian blue <https://en.wikipedia.org/wiki/Prussian_blue> 	#003153
0% 	19% 	33% 	205° 	100% 	16% 	100% 	33%
Psychedelic purple <https://en.wikipedia.org/wiki/Psychedelic_purple>
#DF00FF 	87% 	0% 	100% 	292° 	100% 	50% 	100% 	100%
Puce <https://en.wikipedia.org/wiki/Puce> 	#CC8899 	80% 	53% 	60%
345° 	40% 	67% 	33% 	80%
Pullman Brown (UPS Brown)
<https://en.wikipedia.org/wiki/Brown#Business> 	#644117 	39% 	25%
9% 	33° 	63% 	24% 	77% 	39%
Pumpkin <https://en.wikipedia.org/wiki/Shades_of_orange#Pumpkin>
#FF7518 	100% 	46% 	9% 	24° 	100% 	55% 	91% 	100%
Purple <https://en.wikipedia.org/wiki/Shades_of_purple#Purple>
#6A0DAD 	38% 	0% 	50% 	275° 	100% 	37% 	92% 	68%
Purple (web)
<https://en.wikipedia.org/wiki/Shades_of_purple#Purple_(HTML/CSS_color)_(patriarch)>
	#800080 	50% 	0% 	50% 	300° 	100% 	25% 	100% 	50%
Purple (Munsell)
<https://en.wikipedia.org/wiki/Shades_of_purple#Purple_(Munsell)>
#9F00C5 	62% 	0% 	77% 	288° 	100% 	39% 	100% 	77%
Purple (X11)
<https://en.wikipedia.org/wiki/Shades_of_purple#Purple_(X11_color)_(veronica)>
	#A020F0 	63% 	13% 	94% 	277° 	87% 	53% 	87% 	94%
Purple mountain majesty
<https://en.wikipedia.org/wiki/Lavender_(color)#Lavender_purple_(purple_mountain_majesty)>
	#9678B6 	59% 	47% 	71% 	269° 	30% 	59% 	34% 	71%
Purple navy <https://en.wikipedia.org/wiki/Navy_blue#Purple_navy>
#4E5180 	31% 	32% 	50% 	236° 	24% 	40% 	39% 	50%
Purple pizzazz
<https://en.wikipedia.org/wiki/Shades_of_magenta#Purple_pizzazz>
#FE4EDA 	100% 	31% 	85% 	312° 	99% 	65% 	69% 	100%
Purple Plum
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Heads_'n_Tails>
	#9C51B6 	61% 	32% 	71% 	285° 	41% 	52% 	56% 	71%
Purpureus <https://en.wikipedia.org/wiki/Shades_of_purple#Purpureus>
#9A4EAE 	60% 	31% 	68% 	288° 	38% 	49% 	55% 	68%
Queen blue <https://en.wikipedia.org/wiki/Royal_blue#Queen_blue>
#436B95 	26% 	42% 	58% 	211° 	38% 	42% 	55% 	58%
Queen pink <https://en.wikipedia.org/wiki/Shades_of_pink#Queen_pink>
#E8CCD7 	91% 	80% 	84% 	336° 	38% 	85% 	12% 	91%
Quick Silver
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Silver_Swirls>
	#A6A6A6 	65% 	65% 	65% 	—° 	0% 	65% 	0% 	65%
Quinacridone magenta
<https://en.wikipedia.org/wiki/Shades_of_magenta#Quinacridone_magenta>
#8E3A59 	56% 	23% 	35% 	338° 	42% 	39% 	59% 	56%
Radical Red
<https://en.wikipedia.org/wiki/Amaranth_(color)#Radical_red_(bright_amaranth_pink)>
	#FF355E 	100% 	21% 	37% 	348° 	100% 	60% 	79% 	100%
Raisin black <https://en.wikipedia.org/wiki/Raisin_black> 	#242124
14% 	13% 	14% 	300° 	4% 	14% 	8% 	14%
Rajah <https://en.wikipedia.org/wiki/Saffron_(color)#Rajah> 	#FBAB60
98% 	67% 	38% 	29° 	95% 	68% 	62% 	98%
Raspberry <https://en.wikipedia.org/wiki/Raspberry_(color)> 	#E30B5D
89% 	4% 	36% 	337° 	91% 	47% 	95% 	89%
Raspberry glace
<https://en.wikipedia.org/wiki/Raspberry_(color)#Raspberry_glace>
#915F6D 	57% 	37% 	43% 	343° 	21% 	47% 	34% 	57%
Raspberry rose
<https://en.wikipedia.org/wiki/Raspberry_(color)#Raspberry_rose>
#B3446C 	70% 	27% 	42% 	338° 	45% 	48% 	62% 	70%
Raw sienna
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#D68A59 	84% 	54% 	35% 	24° 	60% 	59% 	58% 	84%
Raw umber <https://en.wikipedia.org/wiki/Umber#Raw_umber> 	#826644
51% 	40% 	27% 	33° 	31% 	39% 	48% 	51%
Razzle dazzle rose
<https://en.wikipedia.org/wiki/Rose_(color)#Razzle_dazzle_rose>
#FF33CC 	100% 	20% 	80% 	315° 	100% 	60% 	80% 	100%
Razzmatazz <https://en.wikipedia.org/wiki/Rose_(color)#Razzmatazz>
#E3256B 	89% 	15% 	42% 	338° 	77% 	52% 	84% 	89%
Razzmic Berry
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Metallic_FX>
#8D4E85 	55% 	31% 	52% 	308° 	29% 	43% 	45% 	55%
Rebecca Purple <https://en.wikipedia.org/wiki/Eric_A._Meyer>
#663399 	40% 	20% 	60% 	270° 	49% 	40% 	67% 	60%
Red <https://en.wikipedia.org/wiki/Red> 	#FF0000 	100% 	0% 	0% 	0°
100% 	50% 	100% 	100%
Red (Crayola)
<https://en.wikipedia.org/wiki/Shades_of_red#Red_(Crayola)> 	#EE204D
93% 	13% 	30% 	347° 	86% 	53% 	87% 	93%
Red (Munsell)
<https://en.wikipedia.org/wiki/Shades_of_red#Red_(Munsell)> 	#F2003C
95% 	0% 	24% 	345° 	100% 	47% 	100% 	95%
Red (NCS)
<https://en.wikipedia.org/wiki/Shades_of_red#Red_(NCS)_(psychological_primary_red)>
	#C40233 	77% 	1% 	20% 	345° 	98% 	39% 	99% 	77%
Red (Pantone)
<https://en.wikipedia.org/wiki/Shades_of_red#Red_(Pantone)> 	#ED2939
93% 	16% 	22% 	355° 	85% 	55% 	83% 	93%
Red (pigment)
<https://en.wikipedia.org/wiki/Shades_of_red#Red_(CMYK)_(pigment_red)>
#ED1C24 	93% 	11% 	14% 	358° 	85% 	52% 	88% 	93%
Red (RYB) <https://en.wikipedia.org/wiki/RYB_color_model> 	#FE2712
100% 	15% 	7% 	5° 	99% 	53% 	93% 	100%
Red-orange <https://en.wikipedia.org/wiki/Red-orange> 	#FF5349 	100%
33% 	29% 	3° 	100% 	64% 	71% 	100%
Red-orange (Crayola)
<https://en.wikipedia.org/wiki/Vermilion#Red-orange> 	#FF681F 	100%
41% 	12% 	20° 	100% 	56% 	88% 	100%
Red-orange (Color wheel) <https://en.wikipedia.org/wiki/Vermilion>
#FF4500 	100% 	27% 	0% 	16° 	100% 	50% 	100% 	100%
Red-purple <https://en.wikipedia.org/wiki/Red-violet#Red-purple>
#E40078 	89% 	0% 	47% 	328° 	100% 	45% 	100% 	89%
Red Salsa
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Heads_'n_Tails>
	#FD3A4A 	99% 	23% 	29% 	355° 	98% 	61% 	77% 	99%
Red-violet <https://en.wikipedia.org/wiki/Red-violet> 	#C71585 	78%
8% 	52% 	322° 	81% 	43% 	89% 	78%
Red-violet (Crayola)
<https://en.wikipedia.org/wiki/Red-violet#Red-violet_(Crayola)>
#C0448F 	75% 	27% 	56% 	324° 	50% 	51% 	65% 	75%
Red-violet (Color wheel)
<https://en.wikipedia.org/wiki/Red-violet#Red-violet_(Color_wheel)>
#922B3E 	57% 	17% 	24% 	350° 	55% 	37% 	71% 	57%
Redwood <https://en.wikipedia.org/wiki/Shades_of_red#Redwood>
#A45A52 	64% 	35% 	32% 	6° 	33% 	48% 	50% 	64%
Resolution blue
<https://en.wikipedia.org/wiki/Shades_of_blue#Resolution_blue>
#002387 	0% 	14% 	53% 	224° 	100% 	26% 	100% 	53%
Rhythm <https://en.wikipedia.org/wiki/Blue-gray#Rhythm> 	#777696
47% 	46% 	59% 	242° 	13% 	53% 	21% 	59%
Rich black <https://en.wikipedia.org/wiki/Rich_black> 	#004040 	0%
25% 	25% 	180° 	100% 	13% 	100% 	25%
Rich black (FOGRA29) <https://en.wikipedia.org/wiki/Rich_black>
#010B13 	0% 	4% 	7% 	207° 	90% 	4% 	95% 	8%
Rich black (FOGRA39) <https://en.wikipedia.org/wiki/Rich_black>
#010203 	0% 	1% 	1% 	210° 	50% 	1% 	67% 	1%
Rifle green
<https://en.wikipedia.org/wiki/Shades_of_green#Rifle_green> 	#444C38
27% 	30% 	22% 	84° 	15% 	26% 	26% 	30%
Robin egg blue <https://en.wikipedia.org/wiki/Robin_egg_blue>
#00CCCC 	0% 	80% 	80% 	180° 	100% 	40% 	100% 	80%
Rocket metallic
<https://en.wikipedia.org/wiki/Shades_of_gray#Rocket_metallic>
#8A7F80 	54% 	50% 	50% 	355° 	5% 	52% 	8% 	54%
Rojo Spanish red
<https://en.wikipedia.org/wiki/Shades_of_red#Spanish_red> 	#A91101
66% 	7% 	0% 	6° 	99% 	33% 	99% 	66%
Roman silver
<https://en.wikipedia.org/wiki/Silver_(color)#Roman_silver> 	#838996
51% 	54% 	59% 	221° 	8% 	55% 	13% 	59%
Rose <https://en.wikipedia.org/wiki/Rose_(color)> 	#FF007F 	100% 	0%
50% 	330° 	100% 	50% 	100% 	100%
Rose bonbon <https://en.wikipedia.org/wiki/Rose_(color)#Rose_bonbon>
#F9429E 	98% 	26% 	62% 	330° 	94% 	62% 	73% 	98%
Rose Dust
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Silver_Swirls>
	#9E5E6F 	62% 	37% 	44% 	344° 	25% 	49% 	41% 	62%
Rose ebony <https://en.wikipedia.org/wiki/Rose_(color)#Rose_ebony>
#674846 	40% 	28% 	27% 	4° 	19% 	34% 	32% 	40%
Rose madder <https://en.wikipedia.org/wiki/Alizarin> 	#E32636 	89%
15% 	21% 	355° 	77% 	52% 	83% 	89%
Rose pink <https://en.wikipedia.org/wiki/Rose_(color)#Rose_pink>
#FF66CC 	100% 	40% 	80% 	320° 	100% 	70% 	60% 	100%
Rose Pompadour
<https://en.wikipedia.org/wiki/Shades_of_pink#Rose_Pompadour>
#ED7A9B 	93% 	48% 	61% 	334° 	76% 	70% 	48% 	92%
Rose quartz <https://en.wikipedia.org/wiki/Rose_(color)#Rose_quartz>
#AA98A9 	67% 	60% 	66% 	303° 	10% 	63% 	11% 	67%
Rose red <https://en.wikipedia.org/wiki/Rose_(color)#Rose_red>
#C21E56 	76% 	12% 	34% 	340° 	73% 	44% 	85% 	76%
Rose taupe <https://en.wikipedia.org/wiki/Taupe#Rose_taupe> 	#905D5D
56% 	36% 	36% 	0° 	22% 	46% 	35% 	56%
Rose vale <https://en.wikipedia.org/wiki/Rose_(color)#Rose_vale>
#AB4E52 	67% 	31% 	32% 	357° 	37% 	49% 	54% 	67%
Rosewood <https://en.wikipedia.org/wiki/Rose_(color)#Rosewood>
#65000B 	40% 	0% 	4% 	353° 	100% 	20% 	100% 	40%
Rosso corsa <https://en.wikipedia.org/wiki/Rosso_corsa> 	#D40000
83% 	0% 	0% 	0° 	100% 	42% 	100% 	83%
Rosy brown <https://en.wikipedia.org/wiki/Rose_(color)#Rosy_brown>
#BC8F8F 	74% 	56% 	56% 	0° 	25% 	65% 	24% 	74%
Royal blue (dark) <https://en.wikipedia.org/wiki/Royal_blue>
#002366 	0% 	14% 	40% 	219° 	100% 	20% 	100% 	40%
Royal blue (light) <https://en.wikipedia.org/wiki/Royal_blue>
#4169E1 	25% 	41% 	88% 	225° 	73% 	57% 	71% 	88%
Royal purple
<https://en.wikipedia.org/wiki/Shades_of_purple#Royal_purple:_17th_century>
	#7851A9 	47% 	32% 	66% 	267° 	35% 	49% 	52% 	66%
Royal yellow
<https://en.wikipedia.org/wiki/Shades_of_yellow#Royal_yellow>
#FADA5E 	98% 	85% 	37% 	48° 	94% 	67% 	62% 	98%
Ruber <https://en.wikipedia.org/wiki/Ruby_(color)#Ruber> 	#CE4676
81% 	27% 	46% 	339° 	58% 	54% 	66% 	81%
Rubine red <https://en.wikipedia.org/wiki/Ruby_(color)#Rubine_red>
#D10056 	82% 	0% 	34% 	335° 	100% 	41% 	100% 	82%
Ruby <https://en.wikipedia.org/wiki/Ruby_(color)> 	#E0115F 	88% 	7%
37% 	337° 	86% 	47% 	92% 	88%
Ruby red <https://en.wikipedia.org/wiki/Ruby_(color)#Ruby_red>
#9B111E 	61% 	7% 	12% 	354° 	80% 	34% 	89% 	61%
Rufous <https://en.wikipedia.org/wiki/Rufous> 	#A81C07 	66% 	11% 	3%
8° 	92% 	34% 	96% 	66%
Russet <https://en.wikipedia.org/wiki/Russet_(color)> 	#80461B 	50%
27% 	11% 	26° 	65% 	30% 	79% 	50%
Russian green
<https://en.wikipedia.org/wiki/Shades_of_green#Russian_green>
#679267 	40% 	57% 	40% 	120° 	17% 	49% 	29% 	57%
Russian violet
<https://en.wikipedia.org/wiki/Shades_of_violet#Russian_violet>
#32174D 	20% 	9% 	30% 	270° 	54% 	20% 	70% 	30%
Rust <https://en.wikipedia.org/wiki/Rust_(color)> 	#B7410E 	72% 	25%
5% 	18° 	86% 	39% 	92% 	72%
Rusty red <https://en.wikipedia.org/wiki/Shades_of_red#Rusty_red>
#DA2C43 	85% 	17% 	26% 	352° 	70% 	51% 	80% 	85%
Sacramento State green
<https://en.wikipedia.org/wiki/Shades_of_green#Sacramento_State_green>
#043927 	2% 	22% 	15% 	160° 	87% 	12% 	93% 	22%
Saddle brown
<https://en.wikipedia.org/wiki/X11_color_names#Color_name_charts>
#8B4513 	55% 	27% 	7% 	25° 	76% 	31% 	86% 	55%
Safety orange <https://en.wikipedia.org/wiki/Safety_orange> 	#FF7800
100% 	47% 	0% 	28° 	100% 	50% 	100% 	100%
Safety orange (blaze orange)
<https://en.wikipedia.org/wiki/Safety_orange> 	#FF6700 	100% 	40%
0% 	24° 	100% 	50% 	100% 	100%
Safety yellow
<https://en.wikipedia.org/wiki/Shades_of_yellow#Safety_yellow>
#EED202 	93% 	82% 	1% 	53° 	98% 	47% 	99% 	93%
Saffron <https://en.wikipedia.org/wiki/Saffron_(color)> 	#F4C430
96% 	77% 	19% 	45° 	90% 	57% 	80% 	96%
Sage <https://en.wikipedia.org/wiki/Sage_(color)> 	#BCB88A 	74% 	72%
54% 	55° 	27% 	64% 	27% 	74%
St. Patrick's blue
<https://en.wikipedia.org/wiki/St._Patrick%27s_blue> 	#23297A 	14%
16% 	48% 	236° 	55% 	31% 	71% 	48%
Salmon <https://en.wikipedia.org/wiki/Salmon_(color)> 	#FA8072 	98%
50% 	45% 	6° 	93% 	71% 	54% 	98%
Salmon pink <https://en.wikipedia.org/wiki/Salmon_(color)#Salmon_pink>
#FF91A4 	100% 	57% 	64% 	350° 	100% 	78% 	43% 	100%
Sand <https://en.wikipedia.org/wiki/Sand_(color)> 	#C2B280 	76% 	70%
50% 	45° 	35% 	63% 	34% 	76%
Sand dune
<https://en.wikipedia.org/wiki/Desert_sand_(color)#Sand_dune_(Drab)>
#967117 	59% 	44% 	9% 	43° 	73% 	34% 	85% 	59%
Sandy brown
<https://en.wikipedia.org/wiki/Shades_of_brown#Sandy_brown> 	#F4A460
96% 	64% 	38% 	28° 	87% 	67% 	61% 	96%
Sap green <https://en.wikipedia.org/wiki/Shades_of_green#Sap_green>
#507D2A 	31% 	49% 	16% 	93° 	50% 	33% 	66% 	49%
Sapphire <https://en.wikipedia.org/wiki/Sapphire_(color)#Sapphire>
#0F52BA 	6% 	32% 	73% 	216° 	85% 	39% 	92% 	73%
Sapphire blue
<https://en.wikipedia.org/wiki/Sapphire_(color)#Sapphire_blue>
#0067A5 	0% 	40% 	65% 	203° 	100% 	32% 	100% 	65%
Sapphire (Crayola) <https://en.wikipedia.org/wiki/Sapphire_(color)>
#0067A5 	18% 	36% 	63% 	215° 	56% 	40% 	72% 	35%
Satin sheen gold
<https://en.wikipedia.org/wiki/Gold_(color)#Satin_sheen_gold>
#CBA135 	80% 	63% 	21% 	43° 	59% 	50% 	74% 	80%
Scarlet <https://en.wikipedia.org/wiki/Scarlet_(color)> 	#FF2400
100% 	14% 	0% 	8° 	100% 	50% 	100% 	100%
Schauss pink <https://en.wikipedia.org/wiki/Baker-Miller_Pink>
#FF91AF 	100% 	57% 	69% 	344° 	100% 	78% 	43% 	100%
School bus yellow <https://en.wikipedia.org/wiki/School_bus_yellow>
#FFD800 	100% 	85% 	0% 	51° 	100% 	50% 	100% 	100%
Screamin' Green
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Fluorescent_crayons>
	#66FF66 	40% 	100% 	40% 	120° 	100% 	70% 	60% 	100%
Sea green <https://en.wikipedia.org/wiki/Shades_of_green#Sea_green>
#2E8B57 	18% 	55% 	34% 	146° 	50% 	36% 	67% 	55%
Sea green (Crayola) <https://en.wikipedia.org/wiki/Shades_of_green>
#00FFCD 	0% 	100% 	80% 	168° 	100% 	50% 	100% 	100%
Seal brown <https://en.wikipedia.org/wiki/Seal_brown> 	#59260B
20% 	8% 	8% 	0° 	43% 	14% 	60% 	20%
Seashell <https://en.wikipedia.org/wiki/Seashell_(color)> 	#FFF5EE
100% 	96% 	93% 	25° 	100% 	97% 	7% 	100%
Selective yellow <https://en.wikipedia.org/wiki/Selective_yellow>
#FFBA00 	100% 	73% 	0% 	44° 	100% 	50% 	100% 	100%
Sepia <https://en.wikipedia.org/wiki/Sepia_(color)> 	#704214 	44%
26% 	8% 	30° 	70% 	26% 	82% 	44%
Shadow
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#8A795D 	54% 	47% 	36% 	37° 	20% 	45% 	33% 	54%
Shadow blue <https://en.wikipedia.org/wiki/Blue-gray#Shadow_blue>
#778BA5 	47% 	55% 	65% 	214° 	20% 	56% 	28% 	65%
Shamrock green
<https://en.wikipedia.org/wiki/Shades_of_green#Shamrock_green>
#009E60 	0% 	62% 	38% 	156° 	100% 	31% 	100% 	62%
Sheen green
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Metallic_FX>
#8FD400 	56% 	83% 	0% 	80° 	100% 	42% 	100% 	83%
Shimmering Blush
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Metallic_FX>
#D98695 	85% 	53% 	58% 	349° 	52% 	69% 	38% 	85%
Shiny Shamrock
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Silver_Swirls>
	#5FA778 	37% 	65% 	47% 	141° 	29% 	51% 	43% 	66%
Shocking pink
<https://en.wikipedia.org/wiki/Shades_of_pink#Shocking_pink>
#FC0FC0 	99% 	6% 	75% 	315° 	98% 	52% 	94% 	99%
Shocking pink (Crayola)
<https://en.wikipedia.org/wiki/Shades_of_magenta#Shocking_pink_(Crayola)>
#FF6FFF 	100% 	44% 	100% 	300° 	100% 	72% 	56% 	100%
Sienna <https://en.wikipedia.org/wiki/Sienna> 	#882D17 	53% 	18% 	9%
12° 	71% 	31% 	83% 	53%
Silver <https://en.wikipedia.org/wiki/Silver_(color)> 	#C0C0C0 	75%
75% 	75% 	—° 	0% 	75% 	0% 	75%
Silver (Crayola)
<https://en.wikipedia.org/wiki/Silver_(color)#Silver_(Crayola)>
#C9C0BB 	79% 	75% 	73% 	21° 	12% 	76% 	7% 	79%
Silver (Metallic)
<https://en.wikipedia.org/wiki/Silver_(color)#Silver_(Metallic)>
#AAA9AD 	67% 	66% 	68% 	255° 	2% 	67% 	2% 	68%
Silver chalice
<https://en.wikipedia.org/wiki/Silver_(color)#Silver_chalice>
#ACACAC 	67% 	67% 	67% 	—° 	0% 	67% 	0% 	67%
Silver pink <https://en.wikipedia.org/wiki/Shades_of_pink#Silver_pink>
#C4AEAD 	77% 	68% 	68% 	3° 	16% 	72% 	12% 	77%
Silver sand <https://en.wikipedia.org/wiki/Silver_(color)#Silver_sand>
#BFC1C2 	75% 	76% 	76% 	200° 	2% 	75% 	2% 	76%
Sinopia <https://en.wikipedia.org/wiki/Sinopia> 	#CB410B 	80% 	25%
4% 	17° 	90% 	42% 	95% 	80%
Sizzling Red
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Heads_'n_Tails>
	#FF3855 	100% 	22% 	33% 	351° 	100% 	61% 	78% 	100%
Sizzling Sunrise
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Extreme_Twistables_colors>
	#FFDB00 	100% 	86% 	0% 	52° 	100% 	50% 	100% 	100%
Skobeloff <https://en.wikipedia.org/wiki/Spring_green#Skobeloff>
#007474 	0% 	45% 	45% 	180° 	100% 	23% 	100% 	45%
Sky blue <https://en.wikipedia.org/wiki/Sky_blue> 	#87CEEB 	53% 	81%
92% 	197° 	71% 	73% 	43% 	92%
Sky blue (Crayola)
<https://en.wikipedia.org/wiki/Sky_blue#Medium_sky_blue> 	#76D7EA
46% 	84% 	92% 	190° 	73% 	69% 	50% 	92%
Sky magenta
<https://en.wikipedia.org/wiki/Shades_of_magenta#Sky_magenta>
#CF71AF 	81% 	44% 	69% 	320° 	50% 	63% 	45% 	81%
Slate blue <https://en.wikipedia.org/wiki/X11_color_names#Color_names>
#6A5ACD 	42% 	35% 	80% 	248° 	54% 	58% 	56% 	80%
Slate gray <https://en.wikipedia.org/wiki/Slate_gray> 	#708090 	44%
50% 	56% 	210° 	13% 	50% 	22% 	56%
Slimy green
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Heads_'n_Tails>
	#299617 	16% 	59% 	9% 	111° 	73% 	34% 	85% 	59%
Smitten <https://en.wikipedia.org/wiki/Red-violet#Smitten> 	#C84186
78% 	25% 	53% 	329° 	55% 	52% 	68% 	78%
Smoky black <https://en.wikipedia.org/wiki/Smoky_black> 	#100C08 	6%
5% 	3% 	30° 	33% 	5% 	50% 	6%
Snow <https://en.wikipedia.org/wiki/Shades_of_white#Snow> 	#FFFAFA
100% 	98% 	98% 	0° 	100% 	99% 	2% 	76%
Solid pink <https://en.wikipedia.org/wiki/Shades_of_pink#Solid_pink>
#893843 	54% 	22% 	26% 	352° 	42% 	38% 	59% 	54%
Sonic silver
<https://en.wikipedia.org/wiki/Silver_(color)#Sonic_silver> 	#757575
46% 	46% 	46% 	—° 	0% 	46% 	0% 	46%
Space cadet <https://en.wikipedia.org/wiki/Cadet_grey#Space_cadet>
#1D2951 	11% 	16% 	32% 	226° 	47% 	22% 	64% 	32%
Spanish bistre <https://en.wikipedia.org/wiki/Bistre#Spanish_bistre>
#807532 	50% 	46% 	20% 	52° 	44% 	35% 	61% 	50%
Spanish blue
<https://en.wikipedia.org/wiki/Shades_of_blue#Spanish_blue> 	#0070B8
0% 	44% 	72% 	203° 	100% 	36% 	100% 	72%
Spanish carmine
<https://en.wikipedia.org/wiki/Carmine_(color)#Spanish_carmine>
#D10047 	82% 	0% 	28% 	340° 	100% 	41% 	100% 	82%
Spanish gray
<https://en.wikipedia.org/wiki/Shades_of_gray#Spanish_gray> 	#989898
60% 	60% 	60% 	—° 	0% 	60% 	0% 	60%
Spanish green
<https://en.wikipedia.org/wiki/Shades_of_green#Spanish_green>
#009150 	0% 	57% 	31% 	153° 	100% 	28% 	100% 	57%
Spanish orange
<https://en.wikipedia.org/wiki/Shades_of_orange#Spanish_orange>
#E86100 	91% 	38% 	0% 	25° 	100% 	45% 	100% 	91%
Spanish pink
<https://en.wikipedia.org/wiki/Shades_of_pink#Spanish_pink> 	#F7BFBE
97% 	75% 	75% 	1° 	78% 	86% 	23% 	97%
Spanish red <https://en.wikipedia.org/wiki/Shades_of_red#Spanish_red>
#E60026 	90% 	0% 	15% 	350° 	100% 	45% 	100% 	90%
Spanish sky blue
<https://en.wikipedia.org/wiki/Sky_blue#Spanish_sky_blue> 	#00FFFF 	0%
100% 	100% 	180° 	100% 	50% 	100% 	100%
Spanish violet
<https://en.wikipedia.org/wiki/Shades_of_violet#Spanish_violet>
#4C2882 	30% 	16% 	51% 	264° 	53% 	33% 	69% 	51%
Spanish viridian
<https://en.wikipedia.org/wiki/Viridian#Spanish_viridian> 	#007F5C
0% 	50% 	36% 	163° 	100% 	25% 	100% 	50%
Spring bud <https://en.wikipedia.org/wiki/Spring_bud> 	#A7FC00 	65%
99% 	0% 	80° 	100% 	49% 	100% 	99%
Spring Frost
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Extreme_Twistables_colors>
	#87FF2A 	53% 	100% 	16% 	94° 	100% 	58% 	84% 	100%
Spring green <https://en.wikipedia.org/wiki/Spring_green_(color)>
#00FF7F 	0% 	100% 	50% 	150° 	100% 	50% 	100% 	100%
Spring green (Crayola)
<https://en.wikipedia.org/wiki/Spring_green_(color)#Spring_green_(Crayola)>
	#ECEBBD 	93% 	92% 	74% 	59° 	55% 	83% 	20% 	93%
Star command blue
<https://en.wikipedia.org/wiki/Cadet_grey#Star_command_blue>
#007BB8 	0% 	48% 	72% 	200° 	100% 	36% 	100% 	72%
Steel blue <https://en.wikipedia.org/wiki/Steel_blue> 	#4682B4 	27%
51% 	71% 	207° 	44% 	49% 	61% 	71%
Steel pink <https://en.wikipedia.org/wiki/Shades_of_pink#Steel_pink>
#CC33CC 	80% 	20% 	80% 	300° 	60% 	50% 	75% 	80%
Steel Teal <https://en.wikipedia.org/wiki/Shiny_Shamrock> 	#5F8A8B
37% 	54% 	55% 	181° 	19% 	46% 	32% 	55%
Stil de grain yellow
<https://en.wikipedia.org/wiki/Stil_de_grain_yellow> 	#FADA5E 	98%
85% 	37% 	48° 	94% 	67% 	62% 	98%
Straw <https://en.wikipedia.org/wiki/Straw_(colour)> 	#E4D96F 	89%
85% 	44% 	54° 	68% 	66% 	51% 	89%
Strawberry <https://en.wikipedia.org/wiki/Strawberry> 	#FA5053 	98%
31% 	33% 	359° 	94% 	65% 	68% 	98%
Strawberry Blonde
<https://en.wikipedia.org/wiki/Strawberry_blonde_(hair_color)>
#ff9361 	100% 	58% 	38% 	19° 	100% 	69% 	62% 	100%
Sugar Plum
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Silver_Swirls>
	#914E75 	57% 	31% 	46% 	325° 	30% 	44% 	46% 	57%
Sunglow <https://en.wikipedia.org/wiki/Sunset_(color)#Sunglow>
#FFCC33 	100% 	80% 	20% 	45° 	100% 	60% 	80% 	100%
Sunray <https://en.wikipedia.org/wiki/Sunset_(color)#Sunray>
#E3AB57 	89% 	67% 	34% 	36° 	71% 	62% 	62% 	89%
Sunset <https://en.wikipedia.org/wiki/Sunset_(color)> 	#FAD6A5 	98%
84% 	65% 	35° 	90% 	81% 	34% 	98%
Super pink <https://en.wikipedia.org/wiki/Shades_of_pink#Super_pink>
#CF6BA9 	81% 	42% 	66% 	323° 	51% 	62% 	48% 	81%
Sweet Brown
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Heads_'n_Tails>
	#A83731 	66% 	22% 	19% 	3° 	55% 	43% 	71% 	66%
Syracuse Orange
<https://en.wikipedia.org/wiki/Shades_of_orange#Syracuse_Orange>
#D44500 	83% 	27% 	0% 	9° 	100% 	42% 	72% 	100%
Tan <https://en.wikipedia.org/wiki/Tan_(color)> 	#D2B48C 	82% 	71%
55% 	25° 	44% 	69% 	33% 	82%
Tan (Crayola)
<https://en.wikipedia.org/wiki/Tan_(color)#Tan_(Crayola)> 	#D99A6C
85% 	60% 	42% 	34° 	59% 	64% 	50% 	85%
Tangerine <https://en.wikipedia.org/wiki/Tangerine_(color)> 	#F28500
95% 	52% 	0% 	33° 	100% 	47% 	100% 	95%
Tango pink <https://en.wikipedia.org/wiki/Shades_of_pink#Tango_pink>
#E4717A 	89% 	44% 	48% 	355° 	68% 	67% 	50% 	89%
Tart Orange
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Heads_'n_Tails>
	#FB4D46 	98% 	30% 	27% 	2° 	96% 	63% 	72% 	98%
Taupe <https://en.wikipedia.org/wiki/Taupe> 	#483C32 	28% 	24% 	20%
27° 	18% 	24% 	31% 	28%
Taupe gray <https://en.wikipedia.org/wiki/Taupe#Taupe_gray> 	#8B8589
55% 	52% 	54% 	320° 	3% 	53% 	4% 	55%
Tea green <https://en.wikipedia.org/wiki/Shades_of_green#Tea_green>
#D0F0C0 	82% 	94% 	75% 	100° 	62% 	85% 	20% 	94%
Tea rose <https://en.wikipedia.org/wiki/Shades_of_orange#Tea_rose>
#F88379 	97% 	51% 	47% 	5° 	90% 	72% 	51% 	97%
Tea rose <https://en.wikipedia.org/wiki/Rose_(color)#Tea_rose>
#F4C2C2 	96% 	76% 	76% 	0° 	69% 	86% 	20% 	96%
Teal <https://en.wikipedia.org/wiki/Teal_(color)> 	#008080 	0% 	50%
50% 	180° 	100% 	25% 	100% 	50%
Teal blue <https://en.wikipedia.org/wiki/Teal_(color)#Teal_blue>
#367588 	21% 	46% 	53% 	194° 	43% 	37% 	60% 	53%
Telemagenta
<https://en.wikipedia.org/wiki/Shades_of_magenta#Telemagenta>
#CF3476 	81% 	20% 	46% 	334° 	62% 	51% 	75% 	81%
Tenné <https://en.wikipedia.org/wiki/Tawny_(color)> (tawny) 	#CD5700
80% 	34% 	0% 	25° 	100% 	40% 	100% 	80%
Terra cotta <https://en.wikipedia.org/wiki/Terra_cotta_(color)>
#E2725B 	89% 	45% 	36% 	10° 	70% 	62% 	60% 	89%
Thistle <https://en.wikipedia.org/wiki/Shades_of_purple#Thistle>
#D8BFD8 	85% 	75% 	85% 	300° 	24% 	80% 	12% 	85%
Thulian pink <https://en.wikipedia.org/wiki/Rose_(color)#Thulian_pink>
#DE6FA1 	87% 	44% 	63% 	333° 	63% 	65% 	50% 	87%
Tickle Me Pink
<https://en.wikipedia.org/wiki/Rose_(color)#Tickle_me_pink> 	#FC89AC
99% 	54% 	67% 	342° 	95% 	76% 	46% 	99%
Tiffany Blue <https://en.wikipedia.org/wiki/Tiffany_Blue#Tiffany_Blue>
#0ABAB5 	4% 	73% 	71% 	178° 	90% 	38% 	95% 	73%
Timberwolf
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors>
#DBD7D2 	86% 	84% 	82% 	33° 	11% 	84% 	4% 	86%
Titanium yellow <https://en.wikipedia.org/wiki/Titanium_yellow>
#EEE600 	93% 	90% 	0% 	58° 	100% 	47% 	100% 	93%
Tomato <https://en.wikipedia.org/wiki/Shades_of_orange#Tomato>
#FF6347 	100% 	39% 	28% 	9° 	100% 	64% 	72% 	100%
Tropical rainforest
<https://en.wikipedia.org/wiki/Jungle_green#Tropical_rainforest>
#00755E 	0% 	46% 	37% 	168° 	100% 	23% 	100% 	46%
True Blue <https://en.wikipedia.org/wiki/True_Blue_(color)> 	#2D68C4
0% 	45% 	81% 	207° 	100% 	41% 	100% 	81%
Trypan Blue <https://en.wikipedia.org/wiki/Trypan_Blue> 	#1C05B3
11% 	2% 	70% 	248° 	95% 	36% 	95% 	70%
Tufts blue <https://en.wikipedia.org/wiki/Tufts_blue> 	#3E8EDE 	24%
56% 	87% 	210° 	71% 	56% 	70.7% 	87.1%
Tumbleweed
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors>
#DEAA88 	87% 	67% 	53% 	24° 	57% 	70% 	39% 	87%
Turquoise <https://en.wikipedia.org/wiki/Turquoise_(color)> 	#40E0D0
25% 	88% 	82% 	174° 	72% 	56% 	71% 	88%
Turquoise blue
<https://en.wikipedia.org/wiki/Turquoise_(color)#Turquoise_Blue>
#00FFEF 	0% 	100% 	94% 	176° 	100% 	50% 	100% 	100%
Turquoise green
<https://en.wikipedia.org/wiki/Turquoise_(color)#Turquoise_Green>
#A0D6B4 	63% 	84% 	71% 	142° 	40% 	73% 	25% 	84%
Turtle green
<https://en.wikipedia.org/wiki/Chartreuse_(color)#Turtle_green>
#8A9A5B 	54% 	60% 	36% 	75° 	26% 	48% 	41% 	60%
Tuscan <https://en.wikipedia.org/wiki/Beige#Tuscan> 	#FAD6A5 	98%
84% 	65% 	35° 	90% 	81% 	34% 	98%
Tuscan brown <https://en.wikipedia.org/wiki/Tuscan_red#Tuscan_brown>
#6F4E37 	44% 	31% 	22% 	25° 	34% 	33% 	50% 	44%
Tuscan red <https://en.wikipedia.org/wiki/Tuscan_red> 	#7C4848 	49%
28% 	28% 	0° 	27% 	38% 	42% 	49%
Tuscan tan <https://en.wikipedia.org/wiki/Tan_(color)#Tuscan_tan>
#A67B5B 	65% 	48% 	36% 	26° 	30% 	50% 	45% 	65%
Tuscany <https://en.wikipedia.org/wiki/Tuscan_red#Tuscany> 	#C09999
75% 	60% 	60% 	0° 	24% 	68% 	20% 	75%
Twilight lavender
<https://en.wikipedia.org/wiki/Lavender_(color)#Twilight_lavender>
#8A496B 	54% 	29% 	42% 	329° 	31% 	41% 	47% 	54%
Tyrian purple
<https://en.wikipedia.org/wiki/Tyrian_purple#Tyrian_purple> 	#66023C
40% 	1% 	24% 	325° 	96% 	20% 	98% 	40%
UA blue
<https://en.wikipedia.org/wiki/University_of_Arizona#School_colors>
#0033AA 	0% 	20% 	67% 	222° 	100% 	33% 	100% 	67%
UA red
<https://en.wikipedia.org/wiki/University_of_Arizona#School_colors>
#D9004C 	85% 	0% 	30% 	339° 	100% 	43% 	100% 	85%
Ultramarine <https://en.wikipedia.org/wiki/Ultramarine> 	#3F00FF 	7%
4% 	56% 	244° 	87% 	30% 	93% 	56%
Ultramarine blue
<https://en.wikipedia.org/wiki/Ultramarine#Ultramarine_blue>
#4166F5 	25% 	40% 	96% 	228° 	90% 	61% 	73% 	96%
Ultra pink
<https://en.wikipedia.org/wiki/Shades_of_magenta#Shocking_pink_(Crayola)>
#FF6FFF 	100% 	44% 	100% 	300° 	100% 	72% 	56% 	100%
Ultra red <https://en.wikipedia.org/wiki/Carmine_(color)#Ultra_red>
#FC6C85 	99% 	42% 	52% 	350° 	96% 	71% 	57% 	99%
Umber <https://en.wikipedia.org/wiki/Umber> 	#635147 	39% 	32% 	28%
21° 	17% 	33% 	28% 	39%
Unbleached silk <https://en.wikipedia.org/wiki/Beige#Unbleached_silk>
#FFDDCA 	100% 	87% 	79% 	22° 	100% 	90% 	21% 	100%
United Nations blue
<https://en.wikipedia.org/wiki/Shades_of_azure#United_Nations_blue>
#5B92E5 	36% 	57% 	90% 	216° 	73% 	63% 	60% 	90%
University of Pennsylvania red
<https://en.wikipedia.org/wiki/Shades_of_red#Penn_red> 	#A50021 	65%
0% 	13% 	348° 	100% 	32% 	100% 	65%
Unmellow yellow
<https://en.wikipedia.org/wiki/Shades_of_yellow#Unmellow_yellow>
#FFFF66 	100% 	100% 	40% 	60° 	100% 	70% 	60% 	100%
UP Forest green
<https://en.wikipedia.org/wiki/Shades_of_green#UP_forest_green>
#014421 	0% 	27% 	13% 	149° 	97% 	14% 	99% 	27%
UP maroon <https://en.wikipedia.org/wiki/Maroon_(color)#UP_maroon>
#7B1113 	48% 	7% 	7% 	359° 	76% 	27% 	86% 	48%
Upsdell red <https://en.wikipedia.org/wiki/Upsdell_red> 	#AE2029
68% 	13% 	16% 	356° 	69% 	40% 	82% 	68%
Uranian blue
<https://en.wikipedia.org/wiki/Shades_of_blue#Uranian_blue> 	#AFDBF5
69% 	86% 	96% 	202° 	78% 	82% 	29% 	96%
USAFA blue <https://en.wikipedia.org/wiki/Air_Force_blue#USAFA_blue>
#004F98 	0% 	31% 	60% 	209° 	100% 	30% 	100% 	60%
Van Dyke brown <https://en.wikipedia.org/wiki/Van_Dyke_brown>
#664228 	40% 	26% 	16% 	25° 	44% 	28% 	60% 	0%
Vanilla <https://en.wikipedia.org/wiki/Vanilla_(color)> 	#F3E5AB
95% 	90% 	67% 	48° 	75% 	81% 	30% 	95%
Vanilla ice
<https://en.wikipedia.org/wiki/Vanilla_(color)#Vanilla_ice> 	#F38FA9
95% 	56% 	66% 	344° 	81% 	76% 	41% 	95%
Vegas gold <https://en.wikipedia.org/wiki/Gold_(color)#Vegas_gold>
#C5B358 	77% 	70% 	35% 	50° 	48% 	56% 	55% 	77%
Venetian red <https://en.wikipedia.org/wiki/Venetian_red> 	#C80815
78% 	3% 	8% 	356° 	92% 	41% 	96% 	78%
Verdigris <https://en.wikipedia.org/wiki/Verdigris> 	#43B3AE 	26%
70% 	68% 	177° 	46% 	48% 	63% 	70%
Vermilion <https://en.wikipedia.org/wiki/Vermilion> 	#E34234 	89%
26% 	20% 	5° 	76% 	55% 	77% 	89%
Vermilion <https://en.wikipedia.org/wiki/Vermilion#Medium_vermilion>
#D9381E 	85% 	22% 	12% 	8° 	76% 	48% 	86% 	85%
Veronica
<https://en.wikipedia.org/wiki/Shades_of_purple#Purple_(X11_color)_(veronica)>
	#A020F0 	63% 	13% 	94% 	277° 	87% 	53% 	87% 	94%
Violet <https://en.wikipedia.org/wiki/Violet_(color)> 	#8F00FF 	56%
0% 	100% 	274° 	100% 	50% 	100% 	100%
Violet (color wheel)
<https://en.wikipedia.org/wiki/Shades_of_violet#Color_wheel_violet>
#7F00FF 	50% 	0% 	100% 	270° 	100% 	50% 	100% 	100%
Violet (crayola)
<https://en.wikipedia.org/wiki/Shades_of_violet#Violet_(crayola)>
#963D7F 	59% 	24% 	50% 	316° 	42% 	41% 	59% 	59%
Violet (RYB) <https://en.wikipedia.org/wiki/RYB_color_model>
#8601AF 	53% 	0% 	69% 	286° 	99% 	35% 	99% 	69%
Violet (web)
<https://en.wikipedia.org/wiki/Shades_of_violet#Web_color_%22violet%22> 	#EE82EE
	93% 	51% 	93% 	300° 	76% 	72% 	45% 	93%
Violet-blue <https://en.wikipedia.org/wiki/Violet-blue> 	#324AB2
20% 	29% 	70% 	229° 	56% 	45% 	72% 	70%
Violet-blue (Crayola)
<https://en.wikipedia.org/wiki/Violet-blue#Violet-blue_(Crayola)>
#766EC8 	46% 	43% 	78% 	246° 	45% 	61% 	45% 	78%
Violet-red <https://en.wikipedia.org/wiki/Red-violet#Violet-red>
#F75394 	97% 	33% 	58% 	336° 	91% 	65% 	66% 	97%
Viridian <https://en.wikipedia.org/wiki/Viridian> 	#40826D 	25% 	51%
43% 	161° 	34% 	38% 	51% 	51%
Viridian green <https://en.wikipedia.org/wiki/Viridian#Viridian_green>
#009698 	0% 	59% 	60% 	181° 	100% 	30% 	100% 	60%
Vivid burgundy
<https://en.wikipedia.org/wiki/Burgundy_(color)#Vivid_burgundy>
#9F1D35 	62% 	11% 	21% 	349° 	69% 	37% 	82% 	62%
Vivid sky blue <https://en.wikipedia.org/wiki/Sky_blue#Vivid_sky_blue>
#00CCFF 	0% 	80% 	100% 	192° 	100% 	50% 	100% 	100%
Vivid tangerine
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#FFA089 	100% 	63% 	54% 	12° 	100% 	77% 	46% 	100%
Vivid violet
<https://en.wikipedia.org/wiki/Shades_of_violet#Vivid_violet>
#9F00FF 	62% 	0% 	100% 	277° 	100% 	50% 	100% 	100%
Volt <https://en.wikipedia.org/wiki/Lime_(color)#Volt> 	#CEFF00 	80%
100% 	0% 	72° 	100% 	50% 	100% 	100%
Warm black <https://en.wikipedia.org/wiki/Rich_black> 	#004242 	0%
26% 	26% 	180° 	100% 	13% 	100% 	25%
Wheat <https://en.wikipedia.org/wiki/Wheat_(color)> 	#F5DEB3 	96%
87% 	70% 	39° 	77% 	83% 	27% 	96%
White <https://en.wikipedia.org/wiki/White> 	#FFFFFF 	100% 	100%
100% 	—° 	0% 	100% 	0% 	100%
Wild blue yonder
<https://en.wikipedia.org/wiki/Air_Force_blue#Wild_blue_yonder>
#A2ADD0 	64% 	68% 	82% 	226° 	33% 	73% 	22% 	82%
Wild orchid <https://en.wikipedia.org/wiki/Orchid_(color)#Wild_orchid>
#D470A2 	83% 	44% 	64% 	330° 	54% 	64% 	47% 	83%
Wild Strawberry
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Standard_colors>
	#FF43A4 	100% 	26% 	64% 	329° 	100% 	63% 	74% 	100%
Wild watermelon
<https://en.wikipedia.org/wiki/Carmine_(color)#Wild_watermelon>
#FC6C85 	99% 	42% 	52% 	350° 	96% 	71% 	57% 	99%
Windsor tan <https://en.wikipedia.org/wiki/Tan_(color)#Windsor_tan>
#A75502 	65% 	33% 	1% 	30° 	98% 	33% 	99% 	65%
Wine <https://en.wikipedia.org/wiki/Wine_(color)> 	#722F37 	45% 	18%
22% 	353° 	42% 	32% 	59% 	45%
Wine dregs <https://en.wikipedia.org/wiki/Wine_(color)#Wine_dregs>
#673147 	40% 	19% 	28% 	336° 	36% 	30% 	52% 	40%
Winter Sky
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Extreme_Twistables_colors>
	#FF007C 	100% 	0% 	49% 	331° 	100% 	50% 	100% 	100%
Wintergreen Dream
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Silver_Swirls>
	#56887D 	34% 	53% 	49% 	167° 	23% 	44% 	37% 	53%
Wisteria
<https://en.wikipedia.org/wiki/Lavender_(color)#Light_lavender_(wisteria)>
	#C9A0DC 	79% 	63% 	86% 	281° 	46% 	75% 	27% 	86%
Wood brown <https://en.wikipedia.org/wiki/Shades_of_brown#Wood_brown>
#C19A6B 	76% 	60% 	42% 	33° 	41% 	59% 	45% 	76%
Xanadu <https://en.wikipedia.org/wiki/Shades_of_gray#Xanadu>
#738678 	45% 	53% 	47% 	136° 	8% 	49% 	14% 	53%
Xanthic <https://en.wikipedia.org/wiki/Shades_of_yellow#Xanthic>
#EEED09 	93% 	93% 	4% 	60° 	93% 	48% 	97% 	93%
Xanthous <https://en.wikipedia.org/wiki/Shades_of_yellow#Xanthous>
#F1B42F 	95% 	71% 	18% 	41° 	87% 	57% 	80% 	95%
Yale Blue <https://en.wikipedia.org/wiki/Yale_Blue> 	#00356B 	0%
21% 	42% 	210° 	100% 	21% 	100% 	42%
Yellow <https://en.wikipedia.org/wiki/Yellow> 	#FFFF00 	100% 	100%
0% 	60° 	100% 	50% 	100% 	100%
Yellow (Crayola)
<https://en.wikipedia.org/wiki/Shades_of_yellow#Yellow_(Crayola)>
#FCE883 	99% 	91% 	51% 	50° 	95% 	75% 	48% 	99%
Yellow (Munsell)
<https://en.wikipedia.org/wiki/Shades_of_yellow#Yellow_(Munsell)>
#EFCC00 	94% 	80% 	0% 	51° 	100% 	47% 	100% 	94%
Yellow (NCS)
<https://en.wikipedia.org/wiki/Shades_of_yellow#Yellow_(NCS)_(psychological_primary_yellow)>
	#FFD300 	100% 	83% 	0% 	50° 	100% 	50% 	100% 	100%
Yellow (Pantone)
<https://en.wikipedia.org/wiki/Shades_of_yellow#Yellow_(Pantone)>
#FEDF00 	100% 	87% 	0% 	53° 	100% 	50% 	100% 	100%
Yellow (process)
<https://en.wikipedia.org/wiki/Shades_of_yellow#Yellow_(CMYK)_(process_yellow)_(canary_yellow)>
	#FFEF00 	100% 	94% 	0% 	56° 	100% 	50% 	100% 	100%
Yellow (RYB) <https://en.wikipedia.org/wiki/RYB_color_model>
#FEFE33 	100% 	100% 	20% 	60° 	99% 	60% 	80% 	100%
Yellow-green <https://en.wikipedia.org/wiki/Yellow-green> 	#9ACD32
60% 	80% 	20% 	80° 	61% 	50% 	76% 	80%
Yellow-green (Crayola)
<https://en.wikipedia.org/wiki/Yellow-green#Yellow-green_(Crayola)>
#C5E384 	77% 	89% 	52% 	79° 	63% 	70% 	42% 	89%
Yellow-green (Color Wheel)
<https://en.wikipedia.org/wiki/Yellow-green#Yellow-green_(Color_Wheel)> 	#30B21A
	19% 	70% 	10% 	112° 	75% 	40% 	85% 	70%
Yellow Orange
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors> 	#FFAE42
100% 	68% 	26% 	34° 	100% 	63% 	74% 	100%
Yellow Orange (Color Wheel)
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors> 	#FF9505
100% 	58% 	2% 	36° 	100% 	51% 	98% 	100%
Yellow Sunshine
<https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors#Heads_'n_Tails>
	#FFF700 	100% 	97% 	0% 	58° 	100% 	50% 	100% 	100%
YInMn Blue <https://en.wikipedia.org/wiki/YInMn_Blue> 	#2E5090 	18%
31% 	56% 	219° 	52% 	37% 	68% 	56%
Zaffre <https://en.wikipedia.org/wiki/Zaffre> 	#0014A8 	0% 	8% 	66%
233° 	100% 	33% 	100% 	66%
Zomp <https://en.wikipedia.org/wiki/Spring_green#Zomp> 	#39A78E 	22%
65% 	56% 	166° 	49% 	44% 	66% 	65%
"""

out = []
for line in data.strip().split("\n"):
    # Get rid of https links
    line = re.sub(r"<https://en.wikipedia.*?>", "", line)
    # Remove e.g. '97%' and '58°'
    line = re.sub(r"[0-9\.]+[%°]", "", line)
    out.append(line)
newdata = " ".join(out)
# Get rid of tab character just before # of hex number.  This will let
# us split the fields on tab characters.
newdata = newdata.replace("\t#", " #")
# Remove empty data
newdata = newdata.replace("—°", "")

# Now the elements are separated by tab characters
print(f"""'''{attr}'''""")
for item in newdata.split("\t"):
    item = item.strip()
    if not item:
        continue
    name, color = item.split("#")
    name = name.replace("∞", "#")
    print(f"{name.strip()}, #{color.lower()}")
print()
