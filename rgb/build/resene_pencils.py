import sys
if 1:
    import debug
    debug.SetDebugger()
attr = f'''
file = {sys.argv[0]}
These pencil color definitions were downloaded from the Excel file
https://www.resene.co.nz/swatches/download_pencils.xls.  This was
converted to Open Office, the columns for name and RGB colors saved, and
then was saved as a CSV file.  Downloaded Wed 16 Mar 2022 04:59:10 PM.
After deleting names that had '-' for colors, this information was the
same as the file I loaded from this site on 1 Jun 2021.
'''.strip()
data = '''
A B Sea,51,80,131
ASAP,192,187,29
Ab Fab,50,27,47
Abacus,118,137,147
Abanakee,146,138,109
Abbey Road,175,168,188
Abbey,73,81,84
Abel Tasman,103,89,46
Abercrombie,236,220,227
Abracadabra,86,73,133
Acadia,53,49,44
Acapulco,117,170,148
Acorn,115,99,48
Acropolis,206,198,181
Adore,203,107,103
Adrenalin Junkie,127,49,54
Adrenalin,255,82,0
Adventure,65,64,98
Aero Blue,192,232,213
Affair,116,80,133
Afficionado,69,54,56
Afghan Tan,144,94,38
Afterburner,152,61,57
Afterglow,206,151,50
Ajay,176,172,174
Akaroa,190,178,154
Alabaster,242,240,230
Alamo,186,140,102
Alaska,178,185,205
Albescent White,225,218,203
Alcatraz,90,80,75
Alert Tan,149,78,44
Alfresco,52,102,79
Alibi,152,132,34
All Black,24,24,24
Allegro,36,46,59
Alloy,145,129,94
Allports,31,106,125
Alluring,196,171,185
Allusive,139,150,149
Almond Frost,154,134,120
Alo Alo,209,203,27
Aloha,197,128,25
Alpaca,211,192,170
Alpine,173,138,59
Alter Ego,171,76,72
Altitude,188,212,226
Alto,205,198,197
Aluminium,118,115,111
Aluminium,132,135,137
Always,209,195,195
Amazon,56,123,84
Amber Grey,146,150,152
Ameile,144,73,71
Americano,138,125,114
Amethyst Smoke,149,135,156
Amour,245,230,234
Amulet,125,157,114
Anakiwa,140,206,234
Anchor,82,109,178
Anemone Green,136,140,108
Anglaise,238,222,196
Anise,167,214,125
Anticipation,168,138,142
Antidote,193,176,159
Antique Brass,108,70,31
Anzac,198,142,63
Apache,211,169,92
Aphrodisiac,166,77,78
Apollo Blue,22,57,104
Apple Blossom,169,82,73
Apple Green,222,234,220
Apple,102,179,72
Apricot White,247,240,219
Apricot,228,143,103
April Sun,253,152,0
Aqua Haze,217,221,213
Aqua Spring,232,243,232
Aqua Squeeze,219,228,220
Aqua,146,211,202
AquaShield Acropolis,206,198,181
AquaShield Akaroa,190,178,154
AquaShield Astra,237,213,166
AquaShield Canterbury Clay,198,174,131
AquaShield Half Tapa,146,146,136
AquaShield Spanish White,222,209,183
AquaShield Stonewall,128,118,97
AquaShield Tasman,186,192,179
Aquamarine,32,89,72
Aquarium,37,60,72
Aquarius,67,168,197
Arabella,133,99,110
Arapawa,39,74,93
Archive Grey,154,153,145
Area 51,60,128,67
Armadillo,72,74,70
Army,48,52,45
Arrowroot,231,226,197
Arrowtown,130,122,103
Artefact,93,82,80
Arthouse,77,32,46
Ash Brown,73,63,47
Ash,190,186,167
Ashanti,166,187,179
Ashen Lavender,177,169,177
Asphalt,42,41,34
Aspiring,187,187,161
Asteroid,165,150,146
Astra,237,213,166
Astral,55,111,137
Astronaut Blue,33,69,89
Astronaut,68,81,114
Athens Grey,220,221,221
Aths Special,213,203,178
Atlantis,156,208,59
Atlas,17,55,55
Atmosphere,168,170,166
Atoll,43,121,122
Atom,55,58,60
Atomic,61,75,82
Attitude,83,43,50
Au Chico,158,103,89
Aubergine,55,37,40
Aurora,90,77,96
Australian Mint,239,248,170
Authentic,138,104,67
Avalanche,53,65,82
Avant Garde,92,44,48
Avatar,139,143,142
Avenger,47,40,58
Aviator,42,48,87
Avocado,149,152,107
Awash,115,156,169
Awol,136,140,77
Axis,132,108,85
Axolotl,99,119,90
Ayers Rock,174,69,29
Azalea,249,192,196
Aztec,41,52,50
Azure,78,105,154
Bach,131,146,112
Backcountry,171,142,107
Bahama Blue,37,89,127
Bahia,169,192,28
Baja White,240,223,187
Baked Earth,73,48,40
Balance,187,174,177
Balderdash,70,86,89
Bali Hai,132,156,169
Ballerina,232,153,190
Balloon,193,77,54
Baltic Sea,60,61,62
Bambina,233,213,211
Bamboo,186,111,63
Banana Split,241,204,43
Bandicoot,135,132,102
Bandit,114,98,79
Banjul,52,50,45
Barbecue,54,48,48
Barberry,210,198,31
Bardot,243,199,98
Barely There,223,221,213
Barista,69,56,55
Bark,62,47,40
Barley Corn,182,147,92
Barley White,247,229,183
Barmy Army,96,118,64
Barn Red,96,40,33
Barometer,17,57,76
Baroque,202,146,116
Barossa,69,46,57
Basalt,82,78,80
Bastille,44,44,50
Bathurst,60,64,39
Battleship Grey,81,87,79
Bauhaus,169,174,213
Bavarian Cream,229,214,167
Bay Leaf,123,177,141
Bay Of Many,53,62,100
Bazaar,143,119,119
Beachcomber,199,186,149
Bean  ,74,53,49
Beaten Track,114,103,86
Beatnik,31,79,84
Beauty Bush,235,185,179
Bedazzle,156,67,103
Bedrock,179,172,156
Beeswax,233,215,171
Beethoven,209,148,108
Bel Air,173,181,170
Believe,53,47,119
Belladonna,119,44,104
Bellbottom Blue,44,76,109
Berlin,85,74,88
Bermuda Grey,111,140,159
Bermuda,134,210,193
Beryl Green,188,191,168
Beyond,128,138,172
Bianca,244,239,224
Big Bang,255,80,60
Big Stone,51,64,70
Bilbao,62,128,39
Billabong,23,49,65
Billy T,193,185,67
Biloba Flower,174,153,210
Bingo,0,116,96
Birch,63,55,38
Bird Flower,208,193,23
Birdcage,157,156,183
Birthday Suit,212,167,152
Biscay,47,60,83
Biscotti,210,193,169
Biscuit Brown,187,139,103
Bismark,72,108,122
Bison Hide,181,172,148
Bisque,214,205,184
Bite Me,235,197,37
Bitter Lemon,210,219,50
Bitter,136,137,108
Bittersweet,194,154,77
Bivouac Green,64,50,37
Bizarre,231,210,200
Black Bean,35,46,38
Black Forest,44,50,39
Black Haze,224,222,215
Black Magic,51,44,34
Black Marlin,56,55,64
Black Pearl,30,39,44
Black Pepper,60,55,49
Black Rock,44,45,60
Black Rose,83,41,52
Black Russian,36,37,43
Black Sheep,62,57,58
Black Squeeze,229,230,223
Black White,229,228,219
Black,30,30,30
Blackadder,56,45,50
Blackberry,67,24,47
Blackcurrant,46,24,59
Blackjack,29,32,32
Blackout,33,25,22
Blackwood,63,55,46
Blake,136,167,200
Blanc,217,208,193
Blanched Pink,208,187,181
Blank Canvas,221,199,165
Blast Grey 1,61,60,58
Blast Grey 2,84,81,77
Blast Grey 3,113,110,107
Blast Grey 3,80,78,75
Blast Off,38,40,87
Blast Yellow,126,91,63
Blaze,190,65,35
Bleach White,235,225,206
Bleached Cedar,69,70,71
Bleached Riverstone,130,122,113
Bledisloe,25,40,43
Bling Bling,127,114,74
Bliss,179,57,62
Blondee,244,227,187
Bloom,111,91,108
Blossom,223,177,182
Blue Bark,30,39,44
Blue Bayoux,98,119,126
Blue Bell,57,45,115
Blue Chalk,227,214,233
Blue Charcoal,38,43,47
Blue Chill,64,143,144
Blue Clouds,39,60,90
Blue Diamond,75,45,114
Blue Dianne,53,81,79
Blue Gem,75,60,142
Blue Haze,189,186,206
Blue Jeans,78,101,144
Blue Lagoon,0,98,111
Blue Marguerite,106,91,177
Blue Moon,114,150,171
Blue Night,31,38,59
Blue Romance,216,240,210
Blue Smoke,120,133,122
Blue Stone,22,100,97
Blue Whale,30,52,66
Blue Zodiac,60,67,84
Bluegrass,131,151,131
Blueprint,42,49,63
Bluff,113,129,135
Blumine,48,92,113
Blush,181,80,103
Boardwalk,159,131,83
Bokara Grey,42,39,37
Bombay,174,174,173
Bombshell,174,47,62
Bon Jour,223,215,210
Bona Fide,151,119,123
Bonanza,183,125,110
Bondi Blue,38,65,107
Bone White,184,183,166
Bone,219,194,171
Bonfire,166,42,32
Boogie Wonderland,132,87,155
Boomerang,121,78,51
Boomtown,52,102,114
Bootleg,60,36,27
Bordeaux,76,28,36
Bordello,151,68,98
Bossanova,76,61,78
Boston Blue,67,142,172
Botanic,33,64,43
Botany Bay,55,56,55
Botticelli,146,172,180
Bottle Green,37,70,54
Boulder,124,129,124
Boulevard,142,165,160
Bounce,103,147,148
Bounty,145,159,160
Bouquet,167,129,153
Bourbon,175,108,62
Boutique,223,172,183
Bowie,0,132,172
Bowman,213,177,133
Bracken,91,61,39
Brandy Punch,192,124,64
Brandy Rose,182,133,122
Brandy,220,182,138
Brazil,129,91,40
Breaker Bay,81,123,120
Breakfree,101,25,42
Breakwater,83,104,147
Breathless,193,200,210
Breeze,204,219,217
Bridal Heath,248,235,221
Bridesmaid,250,230,223
Brie,227,218,178
Bright Charcoal,51,52,53
Bright Grey,87,89,93
Bright Lights,233,215,37
Bright Red,146,42,49
Bright Spark,243,190,51
Bright Sun,236,189,44
Bring It On,195,66,59
Broadway,85,49,70
Bronco,167,151,129
Bronze Olive,88,76,37
Bronze,73,59,47
Bronzetone,67,76,40
Broom,238,204,36
Brown Bramble,83,51,30
Brown Derby,89,69,55
Brown Pod,60,36,27
Brown Sugar,142,101,64
Brownie Points,110,66,51
Brunette,99,64,65
Bubble White,220,215,198
Bubblegum,131,120,199
Bubbles,230,242,234
Buccaneer,110,81,80
Bud,165,168,143
Buddha Gold,188,155,27
Buff,179,140,88
Buffalo,118,95,87
Bulgarian Rose,72,36,39
Bull Shot,117,68,43
Bullion,149,106,62
Bullitt,39,37,60
Bullseye,125,34,43
Bullwhip,143,112,64
Bungy,172,113,60
Bunker,41,44,47
Bunting,43,52,73
Burgundy,101,37,37
Burnham,35,69,55
Burning Sand,208,131,99
Burnished Orange,146,84,58
Burnt Crimson,88,33,36
Burnt Sienna,104,51,50
Burnt Umber,64,53,44
Bush,37,70,54
Bushtrack,58,49,42
Butter,222,203,129
Buttercup,218,148,41
Buttered Rum,157,112,46
Butterfly Bush,104,87,140
Butterfly Creek,60,73,47
Butterfly,164,107,155
Buttermilk,246,224,164
Buttery White,241,235,218
Buzz,251,235,80
Cab Sav,74,46,50
Cabaret,205,82,108
Cabbage Pont,76,85,68
Cactus,91,111,85
Cadillac,152,73,97
Caesar,27,103,103
Cafe Royale,106,73,40
Caffeine,60,49,53
Cajun,102,47,43
Calibre,195,148,109
Calico,213,177,133
California,233,140,58
Calm Green,81,87,79
Calypso,61,113,136
Camarone,32,105,55
Camelot,128,58,75
Cameo,204,164,131
Camouflage,79,77,50
Campground,51,60,32
Can Can,208,138,155
Canary,226,230,77
Candlelight,224,157,55
Candy Floss,159,38,61
Cannon Black,51,44,34
Cannon Pink,142,81,100
Canopy,53,51,44
Canterbury Clay,198,174,131
Canvas,163,153,119
Canyon,67,78,70
Cape Cod,78,85,82
Cape Honey,254,224,165
Cape Palliser,117,72,47
Caper,175,193,130
Cappuccino,193,145,86
Capri,48,67,106
Captain Cook,0,104,155
Caramel,255,213,154
Cararra,235,229,213
Carat,134,125,96
Caraway,199,191,168
Cardin Green,27,52,39
Cardinal,138,36,78
Carefree,209,221,213
Careys Pink,201,154,160
Cargo,155,143,117
Carissma,230,128,149
Carla,245,249,203
Carnaby Tan,91,58,36
Carnival,126,42,101
Carousel Pink,248,219,224
Carpe Diem,228,148,61
Casablanca,240,178,83
Casal,63,84,90
Cascade,140,168,160
Cashmere,209,179,153
Casper,170,181,184
Castaway,174,154,122
Castle Rock,133,132,119
Castlepoint,173,149,105
Castro,68,35,47
Catalina Blue,39,60,90
Catalyst,200,82,65
Catapult,104,81,67
Catch 22,52,52,60
Cathedral,75,77,74
Catskill White,224,228,220
Catwalk,61,62,76
Cave Rock,55,44,44
Cavern Pink,224,184,177
Ce Soir,146,113,167
Cedar,101,57,44
Cedar,70,52,48
Celebrate,224,161,40
Celery,180,192,76
Celeste,210,210,192
Celestial Blue,26,32,47
Cello,58,78,95
Celtic,43,63,54
Cement,133,113,88
Centaurian,110,89,119
Centre Stage,131,49,116
Ceramic,223,221,214
Cest La Vie,228,215,209
Cha Cha,140,63,66
Chablis,253,233,224
Chain Gang,85,82,82
Chain Reaction,108,105,90
Chalet Green,90,110,65
Chalk Dust,238,232,221
Chalk Lavender,228,222,231
Chalky,223,194,129
Chambray,71,88,119
Chameleon,152,183,79
Chamois,230,204,154
Chamois,232,205,154
Champagne,238,217,182
Chandelier,237,223,184
Chantilly,237,184,199
Chaos,146,42,49
Chapta And Verse,87,76,94
Charade,57,64,67
Charcoal,25,24,24
Chardon,248,234,223
Chardonnay,255,200,120
Charger,249,194,78
Charisma,133,73,38
Charlotte,164,220,230
Charm,208,116,139
Chateau Green,65,159,89
Chatelle,179,171,182
Chathams Blue,44,89,113
Checkmate,47,50,74
Cheeky,204,95,89
Cheers,145,106,45
Chelsea Cucumber,136,169,91
Chelsea Gem,149,83,47
Chenin,222,195,113
Cherish,198,171,169
Cherokee,245,205,130
Cherry Pie,55,45,82
Cherrywood,78,49,46
Cherub,245,215,220
Chetwode Blue,102,111,180
Chi,159,191,194
Chicago,91,93,86
Chicane ,104,103,101
Chiffon,240,245,187
Chilean Fire,208,94,52
Chilean Heath,249,247,222
Chill Out,226,231,186
Chimney Sweep,28,29,31
China Ivory,251,243,211
Chino,184,173,138
Chinook,157,211,168
Chocolate Brownie,60,36,27
Chocolate Fish,58,40,51
Chocolate Lounge,69,60,67
Chocolate,61,35,39
Christalle,56,33,97
Christi,113,169,29
Christine,191,101,46
Chrome White,202,199,183
Ciderhouse,145,165,118
Cigar,125,78,56
Cincinnati,165,64,63
Cinder,36,42,46
Cinderella,251,215,204
Cinnamon,123,72,43
Cioccolato,93,59,46
Circus,255,215,160
Citrine White,222,221,203
Citron,142,154,33
Citrus,159,183,10
City Limits,12,58,55
Clairvoyant,104,59,125
Clam Shell,210,179,169
Claret,110,34,51
Classic Rose,244,200,219
Classius,179,141,66
Clay Creek,137,126,89
Claypot,171,105,80
Clear Day,223,239,234
Clementine Orange,222,115,72
Clementine,193,79,59
Cliff Face Grey,108,110,109
Cliffhanger,74,79,70
Climate,110,109,94
Clinker,70,54,35
Clockwork Orange,191,96,49
Clotted Cream,245,234,208
Cloud Burst,53,62,79
Cloud Nine,235,247,228
Cloud,194,188,177
Clouded Blue,137,146,150
Cloudy,176,169,159
Clover,71,86,47
Clowning Around,56,33,97
Coast,36,52,66
Coastal Blue,170,183,187
Cobalt,39,60,90
Cobblestone,128,127,115
Cocktail,47,29,37
Coco,104,40,40
Cocoa Bean,79,56,53
Cocoa Brown,53,40,30
Coconut Cream,225,218,187
Cocoon,218,195,159
Cod Grey,45,48,50
Code Red,136,0,37
Coffee Bean,54,45,38
Coffee Break,121,105,94
Coffee,114,103,81
Cognac,154,70,61
Cola,60,47,35
Cold Purple,157,138,191
Cold Turkey,202,181,178
Colins Wicket,149,130,93
Colonial White,233,215,171
Colour Me Pink,169,12,80
Comet,99,99,115
Comfort Zone,162,185,210
Como,76,120,92
Compass,75,87,97
Conch,160,177,174
Concord,130,127,121
Concrete,210,209,205
Condor,91,96,92
Confederate Grey,203,203,222
Confetti,221,203,70
Confidante,35,49,103
Congo Brown,101,77,73
Conifer,177,221,82
Consuela,253,183,109
Contessa,193,111,104
Contraband,70,36,41
Conundrum,60,32,44
Cooled Green,196,211,180
Copper Canyon,119,66,44
Copper Fire,146,83,69
Copper Rust,149,82,76
Copperhead,117,81,72
Copyrite,180,178,166
Coral Candy,245,208,201
Coral Tree,171,110,103
Coral,192,176,147
Cordite,109,70,88
Corduroy,64,77,73
Coriander,187,181,141
Cork,90,76,66
Corkscrew,189,182,165
Corn Field,248,243,196
Corn Harvest,141,112,42
Corn,223,170,40
Cornflower,255,171,160
Coromandel,185,168,115
Corvette,233,186,129
Cosmic,121,77,96
Cosmonaut,38,33,31
Cosmos,252,213,207
Costa Del Sol,98,93,42
Cotton Seed,191,186,175
Cotton Wool,242,240,230
Cougar,170,160,141
Countdown,146,47,29
County Green,27,75,53
Courage,75,37,42
Couture,73,55,64
Cove Grey,52,63,92
Covert,100,89,119
Cowabunga,0,95,91
Cowboy,68,55,54
Coyote,221,183,123
Crab Apple,135,56,47
Cracker,150,49,40
Craigieburn,146,136,116
Crail,166,86,72
Cranberry,180,56,100
Crash Hot,175,46,64
Crater Brown,77,62,60
Cream Brulee,255,227,155
Cream Can,238,192,81
Creme De Banane,224,193,97
Creole,57,50,39
Crescendo,34,47,68
Crescent,131,149,150
Crete,119,113,43
Crisp Green,149,149,82
Crocodile,112,105,80
Cross Country,104,127,69
Crossroads,115,73,73
Crown Of Thorns,118,60,51
Crowshead,50,49,46
Cruise,180,226,213
Cruising,95,121,160
Crusade,205,182,146
Crusoe,22,91,49
Crusta,243,134,83
Cuban Tan,54,45,38
Cumin,120,68,48
Cumulus,245,244,193
Cupid,245,178,197
Curiosity,211,229,104
Curious Blue,61,133,184
Cut Glass,201,219,220
Cutty Sark,92,129,115
Cyprus,15,70,69
DNA,51,54,51
Daintree,39,63,65
Dairy Cream,237,210,164
Daisy Bush,91,62,144
Daisy Chain,248,243,196
Dakota,116,93,85
Dalek,71,87,105
Dali,32,194,158
Dallas,102,74,45
Dancing Girl,148,112,196
Dancing Queen,74,45,104
Danube,91,137,192
Daredevil,203,72,59
Dark Buff,151,102,56
Dark Crimson,64,35,39
Dark Ebony,55,49,43
Dark Ginger,71,48,41
Dark Knight,35,45,54
Dark Oak,85,52,43
Dark Rimu,112,65,40
Dark Rum,69,54,43
Dark Side,42,53,64
Dark Slate,70,83,82
Dark Tan,97,45,45
Dauntless,22,111,127
Dawn Chorus,225,168,144
Dawn Pink,230,214,205
Dawn,159,157,145
Dawnbreaker,129,49,37
Daybreak Yellow,252,191,102
Daydream,222,220,195
Daytona,30,34,44
De Janeiro,133,102,132
De York,133,202,135
Decadence,49,54,105
Deco,204,207,130
Deep Blush,227,111,138
Deep Bronze,81,65,45
Deep Chocolate,60,36,27
Deep Cove,58,78,88
Deep Fir,25,57,37
Deep Impact,103,39,41
Deep Khaki,61,64,49
Deep Koamaru,52,52,103
Deep Oak,61,50,44
Deep Purple,69,35,80
Deep Sea,22,126,101
Deep South,0,72,83
Deep Space,76,73,69
Deep Teal,25,68,60
Deja Vu,215,174,129
Del Rio,181,153,142
Del Toro,177,29,32
Dell,72,101,49
Delta Blue,124,154,205
Delta Grey,165,163,149
Delta,153,155,149
Deluge,130,114,164
Derby,249,228,198
Desert Sand,173,152,122
Desert Storm,237,231,224
Desert Yellow,202,141,22
Desert,161,95,59
Designer White,215,217,226
Desire,234,60,83
Desperado,117,57,41
Destiny,136,158,157
Detroit,120,119,116
Devoted,232,205,208
Dew,231,242,233
Di Serria,212,145,93
Diesel,50,44,43
Digeridoo,69,41,36
Digital Blue,62,65,99
Dimension,113,112,86
Dingley,96,124,71
Disco,137,45,79
Discover,0,103,137
Ditto,231,226,228
Divine,228,206,236
Dixie Chick,196,143,42
Dixie,205,132,49
Dizzy Lizzy,129,202,43
Doeskin,182,160,129
Dolly,245,241,113
Dolphin,106,104,115
Domino,108,91,76
Don Juan,90,79,81
Donkey Brown,129,110,92
Dorado,110,95,86
Dotcom,65,65,93
Double Akaroa,177,165,137
Double Alabaster,243,243,237
Double Arrowtown,113,103,83
Double Ash,167,163,146
Double Barbecue,40,32,32
Double Barely There,228,226,216
Double Barista,57,44,42
Double Bianca,255,245,225
Double Biscotti,213,186,158
Double Bison Hide,161,151,129
Double Black White,228,226,218
Double Blanc,216,206,186
Double Buffalo,100,78,70
Double Caffeine,51,39,41
Double Canterbury Clay,184,159,111
Double Chandelier,229,215,173
Double Cod Grey,29,32,32
Double Colins Wicket,130,111,76
Double Colonial White,228,207,153
Double Concrete,197,197,195
Double Cougar,153,143,128
Double Delta,131,133,127
Double Diesel,40,32,29
Double Doeskin,172,145,110
Double Drought,172,152,125
Double Dutch White,247,225,183
Double Felix,69,55,50
Double Fossil,194,184,158
Double Foundry,40,42,44
Double Friar Grey,117,111,98
Double Gravel,58,60,57
Double Grey Olive,148,138,108
Double Haystack,214,184,138
Double Hillary,151,142,105
Double House White,209,206,200
Double Joanna,201,197,176
Double Joss,166,147,128
Double Kalgoorie Sands,168,114,78
Double Lemon Grass,139,139,116
Double Linen,169,167,144
Double Lumberjack,99,62,54
Double Malta,147,128,108
Double Masala,69,65,57
Double Merino,237,228,216
Double Milestone,177,160,156
Double Mondo,74,66,55
Double Napa,138,127,107
Double Nullarbor,125,102,75
Double Oilskin,80,69,58
Double Otter,121,96,83
Double Parchment,199,187,163
Double Pavlova,169,152,119
Double Pearl Lusta,233,220,190
Double Perfect Taupe,152,139,128
Double Pravda,118,108,92
Double Putty,192,155,89
Double Rakaia,169,165,165
Double Resolution Blue,30,41,82
Double Revolver,41,39,47
Double Rice Cake,231,226,211
Double Rickshaw,157,127,101
Double Schooner,114,105,98
Double Sea Fog,223,221,212
Double Sidewinder,71,63,64
Double Sisal,178,162,134
Double Solitaire,228,210,182
Double Spanish White,210,195,163
Double Stack,111,113,110
Double Stonehenge,112,103,91
Double Stonewall,108,99,78
Double Surrender,168,170,171
Double Tana,168,164,140
Double Tapa,106,106,95
Double Tea,178,168,148
Double Thorndon Cream,205,200,181
Double Travertine,219,213,186
Double Trojan,101,102,100
Double Truffle,165,159,147
Double Tuna,47,50,55
Double Villa White,230,220,197
Double Wheatfield,217,207,179
Double White Pointer,209,204,193
Dove Grey,119,118,114
Dover White,201,191,187
Downriver,42,52,74
Downy,111,210,190
Drab,213,177,133
Dragon,102,94,76
Dreamer,211,229,239
Dreamweaver,220,213,222
Driftwood,143,111,72
Drop Dead Gorgeous,204,40,82
Drought,184,168,143
Drover,251,235,155
Drumbeat,100,67,47
Dry Creek,154,127,124
Duck Egg Blue,183,193,188
Dune,81,79,74
Dusky Pink,146,117,113
Dust Storm,229,202,192
Dusted Blue,146,159,162
Dusted Grey,167,166,157
Dusty Grey,172,155,155
Dusty Road,151,126,102
Dutch White,240,223,187
Dynamite,111,40,43
Eagle,176,172,148
Earls Green,184,167,34
Early Dawn,251,242,219
Earlybird,81,57,57
Earth Green,46,52,43
Earthsong,42,62,51
Earthstone,181,175,139
East Bay,71,82,110
East Side,170,140,188
Eastern Blue,0,135,159
Easy Rider,83,94,86
Ebb,230,216,212
Ebony Clay,50,52,56
Ebony,49,51,55
Echidna,116,95,82
Echo Blue,164,175,205
Echo,72,60,58
Eclipse,63,57,57
Ecru White,214,209,192
Ecstasy,201,97,56
Eden,38,98,85
Edgewater,193,216,197
Edward,151,164,154
Effervescent,168,152,142
Effortless,160,150,167
Egg Sour,249,228,197
Egg White,224,200,141
Eighth Akaroa,230,221,208
Eighth Arrowtown,186,181,168
Eighth Ash,227,226,218
Eighth Barista,116,100,102
Eighth Biscotti,241,232,221
Eighth Bison Hide,222,215,203
Eighth Black White,246,244,238
Eighth Blanc,240,235,228
Eighth Buffalo,177,160,156
Eighth Canterbury Clay,227,215,191
Eighth Castle Rock,190,189,180
Eighth Colins Wicket,196,181,156
Eighth Drought,227,219,206
Eighth Dutch White,249,244,231
Eighth Felix,137,124,121
Eighth Fossil,237,230,221
Eighth Friar Grey,193,188,180
Eighth Gravel,136,138,132
Eighth Hillary,214,211,190
Eighth Joss,224,216,204
Eighth Kalgoorie Sands,215,189,166
Eighth Lemon Grass,199,201,191
Eighth Malta,216,210,200
Eighth Masala,138,137,132
Eighth Mondo,147,138,125
Eighth Napa,212,205,194
Eighth Nullarbor,194,180,160
Eighth Oilskin,146,138,130
Eighth Parchment,237,233,220
Eighth Pavlova,234,224,199
Eighth Pearl Lusta,249,248,240
Eighth Pravda,195,188,176
Eighth Putty,232,216,177
Eighth Rice Cake,244,243,240
Eighth Sidewinder,176,172,174
Eighth Sisal,235,226,209
Eighth Spanish White,246,238,226
Eighth Stack,192,193,191
Eighth Stonehenge,189,185,178
Eighth Stonewall,178,173,158
Eighth Tana,224,222,209
Eighth Tapa,183,184,178
Eighth Tea,226,222,216
Eighth Thorndon Cream,240,238,229
Eighth Truffle,230,225,218
Eighth Tuna,122,127,133
Eighth Wheatfield,244,241,230
El Nino,146,160,172
El Paso,57,57,44
El Salva,143,78,69
Electric,85,83,79
Element,44,47,47
Elephant,36,54,64
Elevate,96,118,139
Elf Green,27,138,107
Elixir,164,170,126
Elm,41,123,118
Elvis,22,72,155
Embers,140,63,48
Emerald Green,0,108,70
Emerge,173,186,181
Eminence,110,57,116
Emperor,80,73,74
Empress,124,113,115
Enchante,238,213,186
Enchanted,146,58,100
Encore,84,22,44
Endeavour,41,89,139
Endorphin,65,144,173
Energise,241,110,0
Energy Yellow,245,215,82
English Holly,39,66,52
English Sage,125,157,114
English Walnut,71,59,47
Enigma,81,80,114
Entourage,181,107,60
Envy,139,165,143
Epiphany,106,154,98
Equator,218,177,96
Equilibrium,119,110,91
Erica,129,51,45
Erotic,148,65,76
Escapade,102,124,145
Escape,158,192,202
Eskimo,162,180,186
Espirit,53,78,81
Espresso,78,49,45
Essence,195,191,212
Essential Cream,220,182,111
Eternity,45,47,40
Eucalyptus,50,151,96
Eunry,205,165,156
Eureka,65,91,78
Evening Sea,38,96,79
Everest,76,72,80
Everglade,38,67,52
Evergreen,40,55,47
Evermore,190,106,63
Evolution,103,100,85
Explorer,55,78,89
Exponent,136,143,152
Extrovert,117,38,66
Fahrenheit,103,46,43
Fair Pink,243,229,220
Fairground,72,58,121
Fairylight,213,199,232
Fairytale,198,196,219
Falcon,110,90,91
Fandango,90,56,81
Fantail,186,174,169
Fantasy,242,230,221
Fascinator,79,64,129
Fast Lane,137,36,49
Fawn  ,199,189,149
Fawn Green,188,184,143
Fedora,98,86,101
Feijoa,165,215,133
Felix,83,69,65
Fern Frond,87,94,46
Fern,54,92,52
Ferra,135,106,104
Ferris Wheel,114,74,161
Fertile Mind,185,214,194
Fervent Green,57,79,43
Festival,234,204,74
Feta,219,224,208
Feverpitch,45,67,37
Fiddlesticks,125,100,29
Fiery Orange,177,89,47
Fiesta,189,126,45
Fifty Shades,147,139,125
Fiji Green,99,111,34
FilmPro Black,40,40,40
FilmPro Burnt Sienna,82,44,43
FilmPro Burnt Umber,58,48,44
FilmPro Chrome Green,47,69,44
FilmPro Deep Red,144,36,58
FilmPro Digital Blue,45,36,128
FilmPro Digital Green,68,197,83
FilmPro Emerald Green,44,129,57
FilmPro Fire Red,165,51,60
FilmPro Golden Yellow,247,181,45
FilmPro Lemon Yellow,243,213,44
FilmPro Magenta,170,48,93
FilmPro Orange,212,80,60
FilmPro Pthalo Blue,43,56,96
FilmPro Pthalo Green,0,86,69
FilmPro Purple,54,42,77
FilmPro Raw Sienna,102,89,46
FilmPro Raw Umber,63,57,48
FilmPro Reduction Base,241,240,233
FilmPro Sky Blue,53,93,144
FilmPro Ultramarine Blue,44,62,107
FilmPro White,249,246,237
FilmPro Yellow Oxide,185,128,54
Finch,117,120,90
Finlandia,97,117,91
Finn,105,69,84
Fiord,75,90,98
Fire Bush,224,152,66
Fire,143,63,42
Fireball,204,92,57
Firefly,49,70,67
First Light,229,225,172
Fish N Chips,220,171,75
Fizz,245,204,35
Flair,185,75,66
Flame Pea,190,92,72
Flame Red,134,40,46
Flamenco,234,134,69
Flamingo,225,99,79
Flash Point,147,44,49
Flashback,223,128,62
Flax,130,133,98
Fleece,233,227,210
Fleetwood,185,158,86
Flesh,204,164,131
Flint,113,110,97
Flintstone,126,111,89
Flirt,122,46,77
Float,76,129,195
Florentine Pink,208,131,99
Flotsam,200,196,192
Flourish,173,177,94
Flower Power,222,183,217
Floyd,218,156,166
Foam,208,234,232
Fog,213,199,232
Foggy Grey,167,166,157
Footloose,164,97,58
Forbidden,176,70,64
Forcefield,137,150,148
Forecast,162,170,177
Forest Green,51,66,49
Forget Me Not,253,239,219
Fortune,146,128,83
Fossil,213,203,178
Foundry,44,46,50
Fountain Blue,101,173,178
Foxtrot,182,112,111
Frangipani,255,215,160
Free Spirit,0,119,123
Freedom,0,98,70
Freefall,29,149,201
Freelance,85,191,173
Freestyling,164,168,176
French Grey,191,189,193
French Lilac,222,183,217
French Pass,164,210,224
Frenzee,247,162,51
Fresh,202,228,149
Friar Grey,134,131,122
Fringy Flower,180,225,187
Frizzell,173,129,47
Froly,229,109,117
Frontier,153,157,122
Frost,225,228,197
Frosted Mint,226,242,228
Frostee,219,229,210
Froth Green,202,199,183
Frozen,157,182,198
Fruit Salad,75,163,81
Fuchsia,123,92,183
Fudge,106,62,42
Fuego,194,214,46
Fuel Yellow,209,144,51
Fugitive,182,57,58
Full Monty,57,32,62
Fun Blue,51,80,131
Fun Fair,119,44,104
Fun Green,21,99,61
Funk,198,170,36
Funtasia,76,51,113
Fuscous Grey,60,59,60
Fusion,152,70,62
Gable Green,44,70,65
Galactica,48,54,85
Galaxy,99,70,75
Gallery,220,215,209
Galliano,216,167,35
Gannet Grey,142,145,143
Gargoyle,144,126,105
Gateway,94,113,117
Gauntlet,113,111,105
Gecko,69,99,75
Geebung,197,131,46
Gelato,219,183,190
Geneva,210,224,158
Genie,131,62,119
Genoa,49,121,109
Geraldine,231,123,117
Geronimo,136,33,60
Get Reddy,173,53,57
Geyser,203,208,207
Ghost,192,191,199
Gigas,86,71,134
Giggle,105,50,110
Gimblet,185,173,97
Gin Fizz,248,234,202
Gin,217,223,205
Gingko,165,156,85
Givry,235,212,174
Glacier,120,177,191
Glade Green,95,129,81
Glamour Puss,248,116,139
Glistening White,244,244,236
Glitter,65,58,93
Glitterati,179,173,151
Glitterbug,169,42,55
Globe,37,103,97
Glorious,240,119,113
Go Ben,120,110,76
Go Go Go,118,173,76
Goblin,52,83,61
Gobstopper,88,53,128
Goddess,251,171,143
Gold Coast,179,139,94
Gold Drop,213,108,48
Gold Dust,146,119,72
Gold Rush,162,138,100
Gold Tips,226,178,39
Gold,159,143,83
Golden Bell,202,129,54
Golden Dream,241,204,43
Golden Fizz,235,222,49
Golden Glow,249,215,126
Golden Sand,234,206,106
Golden Tainoi,255,193,82
Goldie,179,155,105
Goldmine,155,129,96
Gondola,55,51,50
Gondwana,91,117,92
Good As Gold,200,155,75
Good Life,105,163,102
Good Morning,225,161,89
Gooseberry,191,194,152
Gordons Green,41,51,43
Gorse,253,227,54
Gossamer,57,159,134
Gossip,159,211,133
Gotham,48,59,68
Gothic,105,136,144
Governor Bay,81,85,155
Graceland,135,116,130
Grain Brown,202,184,162
Grandis,255,205,115
Granite Green,139,130,101
Granny Apple,197,231,205
Granny Smith,123,148,140
Grape,65,61,75
Grapevine,67,37,79
Graphite,56,52,40
Grass Hopper,122,114,41
Grass Stain,22,91,49
Grasslands,61,61,46
Gravel,74,75,70
Gravity,61,64,64
Green Fields,62,99,52
Green House,62,99,52
Green Kelp,57,61,42
Green Leaf,82,107,45
Green Meets Blue,69,91,88
Green Mist,191,194,152
Green Pea,38,98,66
Green Room,56,129,96
Green Smoke,156,166,100
Green Spring,169,175,153
Green Vogue,35,65,78
Green Waterloo,44,45,36
Green White,222,221,203
Greenback,68,88,59
Greenstone,36,108,70
Greige,137,132,120
Grenadier,193,77,54
Grey Chateau,159,163,167
Grey Friars,49,52,54
Grey Granite,128,135,130
Grey Green,82,86,54
Grey Nickel,189,186,174
Grey Nurse,209,211,204
Grey Olive,161,154,127
Grey Suit,147,145,160
Greywacke,188,184,190
Groovy,92,163,69
Groundbreaker,90,79,64
Guardsman Red,149,46,49
Guggenheim,255,142,89
Gulf Blue,52,63,92
Gulf Stream,116,178,168
Gull Grey,164,173,176
Gum Leaf,172,201,178
Gumbo,113,143,138
Gumboot,49,51,55
Gun Powder,72,71,83
Gunmetal,44,53,57
Gunsmoke,122,124,118
Gurkha,152,145,113
Guru,21,76,101
Gypsy Queen,78,86,172
Haast Shale,81,86,100
Hacienda,158,128,34
Hairy Heath,99,53,40
Haiti,44,42,53
Haka,57,51,40
Half Akaroa,203,194,173
Half Alabaster,240,238,235
Half Albescent White,229,223,212
Half And Half,237,231,200
Half Arrowtown,152,144,127
Half Ash,203,200,186
Half Astra,245,225,186
Half Athens Grey,228,228,223
Half Atmosphere,190,191,183
Half Aubergine,64,44,53
Half Baked,85,143,147
Half Baltic Sea,86,86,87
Half Barbecue,60,53,55
Half Barely There,237,236,228
Half Barista,81,63,63
Half Beryl Green,215,218,200
Half Bianca,246,243,233
Half Biscotti,217,204,187
Half Bison Hide,199,189,171
Half Black White,240,238,234
Half Blanc,229,222,212
Half Bokara Grey,53,51,51
Half Breathless,224,227,234
Half Buffalo,137,117,111
Half Buttermilk,247,229,183
Half Canterbury Clay,211,191,153
Half Cararra,233,226,210
Half Caraway,215,206,187
Half Carefree,225,232,227
Half Chandelier,243,233,203
Half Chicago,119,119,112
Half Chill Out,234,241,208
Half Cloud,212,205,195
Half Cloudy,198,190,183
Half Cobblestone,146,143,132
Half Colins Wicket,164,147,111
Half Colonial White,242,229,191
Half Concrete,226,225,224
Half Copyrite,200,198,188
Half Coriander,201,202,176
Half Cougar,188,181,166
Half Craigieburn,169,161,143
Half Cut Glass,211,228,228
Half Delta,174,176,170
Half Diesel,53,49,49
Half Dizzy Lizzy,146,211,51
Half Doeskin,193,175,147
Half Drought,202,189,169
Half Duck Egg Blue,198,204,202
Half Dusted Blue,171,182,183
Half Dutch White,251,240,214
Half Ecru White,224,220,204
Half Emerge,206,213,207
Half Escape,186,218,229
Half Eskimo,181,200,206
Half Evolution,130,125,107
Half Felix,98,83,78
Half Flotsam,217,213,209
Half Fog,230,222,243
Half Foggy Grey,184,183,175
Half Forest Green,64,83,65
Half Fossil,218,209,192
Half Foundry,62,65,69
Half Friar Grey,152,149,141
Half Fuscous Grey,73,70,72
Half Gargoyle,163,146,126
Half Gauntlet,139,138,136
Half Gin Fizz,248,239,217
Half Gravel,92,93,86
Half Grey Chateau,186,189,193
Half Grey Friars,79,82,85
Half Grey Olive,177,171,149
Half Gull Grey,182,190,192
Half Gunsmoke,148,151,148
Half Hairy Heath,129,70,57
Half Hammerhead,94,103,125
Half Haystack,230,211,179
Half Hillary,185,179,152
Half House White,226,227,223
Half Innocence,138,151,148
Half Inside Back,156,167,162
Half Iron,213,215,216
Half Ironsand,67,64,60
Half Joanna,228,223,206
Half Joss,198,185,171
Half Jumbo,157,157,156
Half Kalgoorie Sands,193,150,118
Half Karaka,51,53,47
Half Kumutoto,156,200,202
Half Lemon Grass,172,173,158
Half Lignite,86,73,64
Half Limerick,152,190,29
Half Linen,205,202,185
Half Lumberjack,132,90,83
Half Mako,97,105,107
Half Malta,181,166,149
Half Masala,103,99,92
Half Melting Moment,249,231,180
Half Merino,236,234,226
Half Milestone,209,196,193
Half Milk Punch,250,238,213
Half Milk White,232,228,220
Half Mischka,186,190,196
Half Mondo,98,89,77
Half Moonbeam,244,233,170
Half Mountain Mist,183,180,176
Half Napa,180,173,158
Half New Denim Blue,83,92,100
Half Nocturnal,67,67,69
Half Nomad,183,175,160
Half Nullarbor,157,137,114
Half Oilskin,114,100,89
Half Opal,183,210,206
Half Orchid White,247,244,234
Half Pale Rose,247,224,228
Half Parchment,224,218,195
Half Pavlova,203,191,160
Half Pearl Lusta,241,234,215
Half Perfect Taupe,187,178,169
Half Periglacial Blue,191,200,196
Half Pohutukawa,139,35,53
Half Popcorn,243,227,193
Half Pot Pourri,248,232,226
Half Pravda,160,153,138
Half Putty,216,191,139
Half Rakaia,204,201,200
Half Raven,131,138,144
Half Regent Grey,147,157,161
Half Reservoir,204,234,229
Half Resolution Blue,29,78,163
Half Rice Cake,242,240,231
Half Rickshaw,189,167,147
Half Rivergum,98,117,100
Half Robin Egg Blue,181,192,181
Half Sail,191,225,240
Half Sandcastle,194,180,161
Half Sandspit Brown,218,210,198
Half Sandstone,139,129,118
Half Sauvignon,249,237,234
Half Scarpa Flow,129,131,134
Half Scotch Mist,249,240,217
Half Sea Fog,239,238,231
Half Secrets,230,228,213
Half Shark,69,72,76
Half Sidewinder,111,103,108
Half Silver Chalice,183,186,182
Half Sisal,213,201,174
Half Smalt Blue,94,124,128
Half Soapstone,240,235,228
Half Solitaire,241,229,209
Half Sour Dough,220,199,177
Half Spanish White,230,219,199
Half Spindle,194,212,225
Half Splash,250,226,182
Half Stack,152,156,153
Half Stonehenge,150,144,136
Half Stonewall,147,141,123
Half Stonewashed,158,148,137
Half Surrender,202,204,204
Half Talisman,125,116,102
Half Tana,204,201,182
Half Tapa,146,146,136
Half Tasman,208,213,205
Half Taupe Grey,157,153,143
Half Tea,206,198,181
Half Thorndon Cream,229,225,211
Half Titania,224,220,206
Half Truffle,205,201,190
Half Tuna,85,88,92
Half Turbo,253,215,35
Half Vienna,243,229,195
Half Villa White,243,238,223
Half Vista White,238,234,230
Half Wan White,233,232,226
Half Washed Green,161,168,148
Half Wheatfield,234,228,208
Half White Pointer,226,225,219
Half White Rock,223,219,198
Half Whiteout,235,228,224
Half Wood Bark,69,58,55
Hammerhead,81,87,105
Hampton,232,212,162
Happy Hour,169,201,73
Happy,255,215,0
Harlequin,106,57,104
Harp,203,206,192
Harvest Gold,234,183,106
Hashtag,150,202,0
Hathaway,247,222,148
Hauraki,58,77,73
Havana,59,43,44
Havelock Blue,87,132,193
Haven,158,170,158
Havoc,173,53,57
Hawaiian Tan,153,82,43
Hawkes Blue,210,218,237
Haystack,222,199,161
Hazard,163,83,42
Hazy Lavender,164,149,145
Headlights,236,215,0
Heartbreaker,193,194,218
Heartwood,166,96,47
Heath,79,42,44
Heather,174,187,193
Heathered Grey,148,140,126
Heatwave,110,38,32
Heavy Metal,70,71,62
Heirloom,157,139,124
Helium,216,217,200
Helter Skelter,51,51,45
Hemisphere,78,147,186
Hemlock,105,104,75
Hemp,152,125,115
Hendrix,76,86,124
Hermitage,177,185,180
Hero,211,124,57
Hi Jinx,229,127,61
Hibernate,90,85,57
Hibiscus,179,54,84
Hideaway,173,170,124
High Country,64,99,38
High Five,178,111,44
High Noon,188,127,12
High Society,105,91,124
High Tea,161,140,144
High Tide,50,55,63
Highball,146,140,60
Highland,122,148,97
Highlight,131,56,89
Hillary,167,160,126
Himalaya,115,99,48
Hinau,72,42,37
Hint Of Green,223,241,214
Hint Of Grey (Sea Fog),223,221,214
Hint Of Grey,223,221,214
Hint Of Red,245,239,235
Hint Of Yellow,246,245,215
Hip Hop,42,37,81
Hippie Blue,73,136,154
Hippie Green,96,138,90
Hippie Pink,171,73,92
Hit Grey,161,169,168
Hit Pink,253,164,112
Hitchhiker,208,199,168
Hive,239,189,0
Hokey Pokey,187,142,52
Hoki,100,125,134
Holiday,245,235,79
Holly,37,52,43
Home Run,0,190,120
Homegrown,54,97,84
Honey Flower,92,60,109
Honey,252,237,197
Honeymoon,244,225,175
Honeysuckle,232,237,105
Hopbush,205,109,147
Hope,101,163,163
Hopskotch,205,109,147
Horizon,100,136,148
Horoscope,67,55,58
Horses Neck,109,86,44
Hot August,154,70,59
Hot Chile,107,37,44
Hot Chocolate,61,38,34
Hot Curry,129,91,40
Hot N Spicy,107,35,32
Hot Purple,78,46,83
Hot Spot,178,40,51
Hot Stuff,135,71,72
Hot Toddy,167,117,44
Hot Wired,111,38,55
House White,223,221,217
Howlin Wolf,183,159,129
Howzat,0,158,89
Hukanui,87,42,35
Hullabaloo,0,139,151
Humming Bird,206,239,228
Hunter Green,47,49,37
Hurricane,139,126,119
Husk,178,153,75
Hyperactive,227,108,54
Hypnotic,209,225,130
I C Red,122,32,49
I Do,204,188,198
I Spy,230,242,234
Ice Cold,175,227,214
Iceberg,202,225,217
Icebreaker,169,183,201
Icon,46,56,45
Identity,110,103,103
Ignition,139,115,90
Iko Iko,179,171,110
Illusion,239,149,174
Imagine,163,152,148
Imprint,92,118,112
Impromptu,155,177,35
Impulse,137,73,97
In The Mauve,206,203,209
Incognito,142,124,110
Indian Ink,35,39,50
Indian Tan,79,48,31
Indochine,156,91,52
Industrial Silver,124,125,121
Infinity,106,115,118
Innocence,109,119,115
Innuendo,119,105,111
Inside Back,132,142,136
Instinct,140,151,157
Internet,115,112,98
Into The Blue,25,55,102
Intrepid,171,132,57
Intrigue,129,71,67
Ipanema,220,198,75
Irish Coffee,98,66,43
Iroko,91,82,68
Iron,203,205,205
Ironbark,109,77,44
Ironhide,143,132,118
Ironsand,57,55,53
Ironside Grey,112,110,102
Ironstone,134,80,64
Irresistible,185,0,76
Island Spice,248,237,219
Isobar,55,72,70
Isotonic,140,139,116
Ivanhoe,59,76,87
Ivy Green,35,53,45
Jacaranda,54,45,56
Jacarta,61,50,93
Jack In The Box,61,63,125
Jacko Bean,65,54,40
Jackpot,20,83,70
Jacksons Purple,61,63,125
Jade,64,114,109
Jaffa,226,121,69
Jagged Ice,202,231,226
Jagger,63,46,76
Jaguar,41,41,47
Jalapeno,112,28,40
Jambalaya,103,72,52
Jandal,183,130,57
Janna,222,209,183
Japanese Laurel,47,117,50
Japanese Maple,103,47,48
Japonica,206,114,89
Jarrah Stain,87,51,44
Jarrah Tree,82,49,47
Jarrah,59,43,44
Jasper,78,101,144
Java,37,151,151
Jazz,95,44,47
Jeepers Creepers,41,169,139
Jelly Bean,68,121,142
Jelly,62,50,103
Jet Stream,187,208,201
Jetsam Brown,148,133,117
Jetsetter,64,80,90
Jewel,19,104,67
Jewelled Yellow,154,136,62
Jigsaw,142,164,103
Jimmy Dean,81,83,93
Jive,205,88,81
Joanna,214,209,192
Joie De Vivre,207,101,72
Jon,70,61,62
Jonquil,238,242,147
Jordy Blue,122,170,224
Joss,185,168,150
Judge Grey,93,83,70
Juicy,255,139,0
Jumbo,135,135,133
Jumpstart,62,32,37
Jungle Green,41,41,36
Jungle Juice,47,117,50
Jungle Mist,176,196,196
Juniper,116,145,142
Jupiter,106,81,119
Jurassic,55,68,62
Just Right,220,191,172
Kabul,108,94,83
Kachow,162,58,52
Kaitoke Green,36,83,54
Kakadu,85,65,35
Kakapo,92,150,37
Kakaramea,110,44,37
Kalgoorie Sands,187,139,103
Kamikaze,164,63,48
Kandinsky,195,216,189
Kangaroo,197,195,176
Karaka,45,45,36
Karens Pewter,102,97,86
Karma,182,162,55
Karry,254,220,193
Kashmir Blue,87,109,142
Kea,40,62,42
Kelp,77,80,60
Kensington Grey,157,159,154
Kenyan Copper,108,50,46
Keppel,95,182,156
Kereru,40,62,35
Kermadec,29,44,42
Kermit,54,129,54
Kidman,204,183,185
Kidnapper,191,192,171
Kilamanjaro,58,53,50
Killarney,73,118,79
Kimberly,105,93,135
Kina Brown,67,61,56
Kingfisher Blue,89,106,139
Kingfisher Daisy,88,53,128
Kitsch,0,108,127
Kiwi,107,90,79
Knave,80,83,76
Knock Out,200,22,65
Kobi,224,147,171
Kokoda,123,120,90
Komakorau,100,53,42
Kombi,131,137,49
Kookaburra,129,131,146
Korma,128,78,44
Koromiko,254,181,82
Koru,119,142,70
Kournikova,249,208,84
Kowhai,192,147,74
Krakatoa,157,82,59
Kubrick,142,116,113
Kudos,53,58,139
Kumera,117,91,39
Kumutoto,120,175,178
Kwila,109,51,42
La Bamba,164,63,72
La Luna,255,216,122
La Palma,66,137,41
La Rioja,186,192,14
Labyrinth,120,106,127
Landmark,62,152,137
Landscape Green,47,71,50
Landscape Grey,85,87,89
Las Palmas,198,218,54
Laser,198,169,94
Last Chance,216,210,200
Latte,237,213,166
Lattitude,109,114,108
Laurel,110,141,113
Lava,89,31,37
Lavender,159,144,208
Leap Year,40,139,109
Leather,144,106,84
Left Field,0,128,42
Legend,140,86,59
Lemon Ginger,150,132,40
Lemon Grass,153,154,134
Lemon Twist,215,207,140
Lemon,217,178,32
Lemoncello,231,169,62
Leprechaun,54,98,67
Lexington,104,62,55
Lichen,122,112,85
Lickety Split,163,217,45
Licorice,46,55,73
Lifesaver,83,94,127
Light Beige,221,194,131
Light Tan,175,108,62
Light Year,70,60,66
Lighthouse,209,204,195
Lightning Yellow,247,162,51
Lignite,66,52,41
Lilac Bush,148,112,196
Lily White,233,238,235
Lily,193,159,179
Lima,122,172,33
Lime White,234,236,214
Lime,183,197,44
Limeade,95,151,39
Limed Ash,103,109,99
Limed Gum,107,91,61
Limed Oak,140,114,84
Limed Spruce,78,96,94
Limelight,153,173,37
Limerick,137,172,39
Limitless,37,75,117
Linen,186,183,162
Link Water,199,205,216
Lip Service,101,21,56
Lipstick,150,44,84
Liquid Metal,62,65,71
Lisbon Brown,84,79,58
Livewire,109,28,39
Livid Brown,49,42,41
Loafer,219,217,194
Loblolly,179,187,183
Loch Ness,7,47,55
Lochinvar,72,144,132
Lochmara,49,110,160
Locust,162,165,128
Lodestar,138,114,82
Log Cabin,57,62,46
Logan,157,156,180
Lola,185,172,187
Lollipop,127,40,56
Lolly Scramble,233,155,65
London Hue,174,148,171
Lone Ranger,135,97,79
Lonestar,82,36,38
Long Shot,135,118,182
Longbush,65,57,34
Longitude,174,183,192
Lotus,139,80,75
Loulou,76,51,71
Loyal,40,25,29
Lucifer,46,80,96
Lucky Break,62,118,45
Lucky Dip,209,239,159
Lucky Point,41,45,79
Lucky,171,154,28
Lullaby,226,205,213
Lumberjack,114,75,67
Lunar Green,78,85,65
Lure,47,119,169
Lush,53,76,40
Lusty,120,46,44
Luxor Gold,171,141,63
Lynch,105,125,137
Mabel,203,232,232
Madagascar,23,46,44
Madam M,97,12,29
Madang,183,227,168
Madison,45,60,84
Madras,71,62,35
Maestro,0,94,109
Magic Carpet,139,152,216
Magik,62,76,122
Magma,135,86,57
Magnetic,85,90,76
Magnolia,238,232,235
Magnum,17,35,49
Mahogany,72,50,48
Mahogany,73,38,37
Mai Tai,165,101,49
Maire,42,41,34
Maize,227,185,130
Majestic Blue,54,67,74
Makara,105,95,80
Mako,80,85,85
Malachite Green,151,151,111
Malarkey,226,121,0
Malibu,102,183,225
Mallard,58,69,49
Malta,165,151,132
Maltese,88,86,96
Mamba,118,109,124
Mamma Mia,213,164,168
Mandalay,181,123,46
Mandrake,176,169,148
Mandy,205,82,91
Mandys Pink,245,183,153
Mangrove,72,78,69
Manhattan,226,175,128
Manilla,213,195,172
Mantis,127,193,92
Mantle,150,167,147
Manuka Honey,222,192,131
Manyana,242,240,232
Manz,228,219,85
Marathon,48,85,99
Marbaroda,61,49,45
Marble,230,228,216
Mardi Gras,53,34,53
Marigold,184,138,61
Mariner,66,99,159
Marionette,171,148,179
Marlin,54,45,38
Maroon,64,35,39
Marsh Green,139,165,143
Marshland,43,46,38
Marshmallow,252,219,210
Martini,183,168,163
Martinique,60,55,72
Marzipan,235,200,129
Masala,87,83,75
Mash,90,76,66
Masquerade,114,133,188
Matai,118,76,44
Matakana,104,93,99
Matchmaker,109,53,64
Matchstick,195,179,141
Material Girl,232,85,96
Matisse,54,92,125
Matrix,142,77,69
Matterhorn,82,75,75
Maverick,200,177,192
Maxwell Smart,42,37,37
Mayhem,77,27,37
McKenzie,140,99,56
Mediterranean Olive,53,63,42
Melanie,224,183,194
Melanzane,52,41,49
Mellow Yellow,234,216,149
Melodic,127,103,134
Melon Orange,226,121,69
Melrose,195,185,221
Melting Moment,244,222,158
Meltwater,110,174,192
Memory,124,91,99
Memphis Belle,202,47,67
Meranti,107,52,42
Mercury,213,210,209
Meridian,124,126,126
Merino,225,219,208
Merlin,79,78,72
Merlot,115,52,58
Mesmerise,181,152,163
Metallic Bronze,85,74,60
Metallic Copper,110,61,52
Metamorphis,128,157,150
Meteor,187,116,49
Meteorite,74,59,106
Metro,172,175,177
Mexican Red,155,61,61
Mexican Wave,182,74,50
Mica,60,69,67
Mid Green,36,83,54
Mid Grey,102,106,109
Mid Grey,113,116,118
Middle Earth,67,78,67
Midnight Express,33,38,58
Midnight Moss,36,46,40
Midnight Oil,40,56,84
Midnight,33,48,62
Midwinter Mist,204,206,206
Mighty,90,37,35
Mikado,63,54,35
Milan,246,244,147
Milano Red,158,51,50
Milestone,190,177,172
Milford Green,51,78,57
Milk Chocolate,76,52,41
Milk Punch,243,229,192
Milk White,220,217,205
Milky Way,142,127,104
Millbrook,89,86,72
Mimosa,245,245,204
Mindaro,218,234,111
Mine Shaft,55,62,65
Mineral Green,80,99,85
Ming,64,117,119
Minnelli,177,107,121
Minsk,62,50,103
Mint Julep,224,216,167
Mint Tulip,198,234,221
Minx,104,83,91
Mirage,55,63,67
Mischief,203,105,70
Mischka,165,169,178
Miso,210,204,168
Miss Hussy,196,71,98
Mission Brown,68,48,40
Mist Grey,186,185,169
Misty Lavender,182,181,185
Mobster,96,90,103
Moby,142,178,190
Moccaccino,88,47,43
Mocha,111,55,45
Modular Green,76,78,63
Mojito,152,135,98
Mojo,151,70,60
Moleskin,198,170,151
Mollusc,67,70,75
Momentum,120,78,44
Mona Lisa,255,152,137
Monarch,107,37,44
Mondo,85,77,66
Mongoose,165,139,111
Monkey,53,46,40
Monsoon,122,118,121
Montana,57,59,60
Monte Carlo,122,197,180
Montoya,119,121,114
Monza,134,40,46
Moody Blue,131,120,199
Moody Lavender,80,67,73
Moon Glow,245,243,206
Moon Mist,206,205,184
Moon Raker,192,178,215
Moon Yellow,240,196,32
Moonbeam,242,226,137
Morepork,184,181,194
Morning Glory,158,209,211
Moroccan Palm,40,51,44
Moroccan Spice,152,89,52
Morocco Brown,68,45,33
Mortar,86,80,81
Mosaic,41,55,65
Moscato,222,186,142
Moscow Mule,158,120,83
Mosque,0,95,91
Mother Earth,0,143,105
Moulin Rouge,173,70,63
Mountain Mist,160,159,156
Moxie,0,111,60
Mozart,189,161,194
Muddy Waters,169,132,79
Muesli,158,126,83
Muka,210,172,125
Mulberry,94,42,64
Mule Fawn,136,79,64
Mulled Wine,82,77,91
Muse,46,105,109
Mustang,127,53,46
Mustard,124,103,32
My Pink,214,139,128
My Sin,253,174,69
Mystic,216,221,218
Nala,65,47,40
Nandor,78,93,78
Napa,163,154,135
Narvik,233,230,220
Native,161,144,75
Natural,136,89,49
Nauti,108,162,189
Navarone,185,165,132
Navigate,48,78,94
Nebula,184,198,190
Negroni,238,199,162
Nelson Red,79,37,37
Nemo,177,185,211
Nepal,147,170,185
Neptune,119,168,171
Nero,37,37,37
Nest Egg,77,69,58
Neutral Bay,133,141,153
Neutral Green,170,165,131
Neva,198,214,13
Nevada,102,111,111
New Amber,109,59,36
New Denim Blue,57,65,73
New Orleans,228,195,133
New York Pink,221,131,116
Niagara,41,169,139
Night Moves,69,76,115
Night Owl,72,51,53
Night Rider,51,46,46
Night Shadz,162,61,84
Nightclub,106,31,68
Nikau,42,64,50
Nile Blue,37,63,78
Ninja,53,44,49
Nirvana,195,191,139
Nite Life,29,33,52
Nitro,151,131,149
Nobel,169,157,157
Nocturnal,47,49,49
Nomad,161,153,134
Noosa,183,128,56
Nordic,29,57,60
Norway,164,184,143
Norwegian Blue,88,100,131
Norwester,72,121,138
Nougat,214,193,171
Nude Brown,188,158,130
Nugget,188,146,41
Nullarbor,144,124,100
Nutmeg,126,74,59
Nutmeg,95,66,45
Oak,120,81,45
Oasis,252,237,197
Obelisk,97,114,116
Observatory,0,143,112
Ocean Green,76,169,115
Odyssey,79,109,105
Off Green,223,240,226
Off Piste,175,172,160
Off Yellow,250,243,220
Oh Behave,190,82,63
Oil,49,51,48
Oiled Cedar,102,54,45
Oilskin,85,83,73
Okey Dokey,188,161,132
Old Brick,138,51,53
Old Copper,115,80,59
Olive Green,53,63,42
Olive Haze,136,128,100
Olivetone,116,112,40
Omega,181,101,25
On Track,128,83,47
Onahau,194,230,236
Onepoto,129,211,209
Onion,72,65,43
Ooh La La,160,136,166
Oopsy Daisy,255,214,123
Opal,168,195,188
Opium,152,126,126
Optimist,43,104,141
Oracle,57,85,85
Orang-atan,197,79,51
Orange Roughy,168,83,53
Orange White,234,227,205
Orbit,135,71,72
Orchid White,241,235,217
Oregon,177,108,57
Organic,150,157,128
Orient,37,91,119
Oriental Pink,194,142,136
Origin,0,156,138
Orinoco,210,211,179
Oscar,244,213,172
Oslo Grey,129,137,136
Otter,143,123,112
Ottoman,211,219,203
Outback,149,130,108
Outer Space,31,38,59
Outpost,189,168,103
Outrageous,255,118,0
Overland,178,170,148
Oxford Blue,40,53,58
Oxley,109,154,120
Oxygen,187,198,213
Oxymoron,156,191,227
Oyster Bay,209,234,234
Oyster Pink,212,181,176
Ozone,71,99,75
Paarl,134,75,54
Pablo,122,113,92
Pacifika,102,112,40
Pacify,187,198,213
Paco,79,64,55
Paddock,102,113,86
Padua,126,179,148
Pale Leaf,189,202,168
Pale Oyster,156,141,114
Pale Prim,249,245,159
Pale Rose,239,214,218
Pale Sky,99,109,112
Pale Slate,195,190,187
Palm Green,32,57,44
Palm Leaf,54,72,47
Palm Sugar,121,85,56
Pampas,234,228,220
Panache,235,247,228
Pancho,223,185,146
Panda,84,79,58
Panorama,89,116,153
Panzano,91,98,78
Paper Doll,223,175,173
Paperback,179,161,144
Papier Mache,183,148,93
Paprika,124,45,55
Parachute,101,184,209
Paradise,106,156,149
Paradiso,72,128,132
Parchment,208,200,176
Paris Daisy,251,235,80
Paris M,49,39,96
Paris White,191,205,192
Parsley,48,93,53
Party Animal,219,146,65
Party Dress,174,72,112
Party Mix,225,197,58
Party Pink,151,131,149
Passion,59,42,57
Passport,131,129,102
Patina,99,146,131
Patio Red,109,51,49
Patriot,79,146,146
Pattens Blue,211,229,239
Paua,42,37,81
Pavlova,186,171,135
Pea Soup,185,184,128
Peach Schnapps,198,128,89
Peach,251,229,194
Peanut,122,68,52
Pearl  ,230,204,154
Pearl Bush,222,209,198
Pearl Lavender,216,201,189
Pearl Lusta,234,224,200
Peat,118,109,82
Pebble Grey,180,179,164
PeekABlue,172,185,232
Pelorous,37,153,178
Pencarrow,227,191,126
Pendragon,178,114,62
Peppermint,215,231,208
Pepperwood,84,47,39
Perano,172,185,232
Perfect Taupe,170,159,148
Perfume,194,169,219
Periglacial Blue,172,182,178
Periwinkle,236,214,183
Permanent Green,37,68,47
Persian Plum,104,51,50
Persian Red,79,33,42
Persimmon,239,115,94
Peru Tan,115,61,31
Pesto,122,114,41
Petanque,46,62,52
Petite Orchid,218,151,144
Pewter,145,160,146
Pharlap,130,102,99
Phoenix,216,108,55
Picasso,248,234,151
Pickled Aspen,91,100,82
Pickled Bean,115,85,62
Pickled Bluewood,79,90,95
Picton Blue,91,160,208
Pigeon Post,119,132,142
Piha Sand,183,160,119
Pine Cone,117,101,86
Pine Glade,189,192,126
Pine Tree,42,47,35
Pink Flare,216,180,182
Pink Lace,246,204,215
Pink Lady,243,215,182
Pink Panther,180,56,100
Pink Swan,191,179,178
Pink Terrace,245,209,202
Pioneer Red,100,38,32
Pioneer,57,69,65
Piper,157,84,50
Pipi,245,230,196
Pippin,252,219,210
Pirate Gold,186,120,42
Pirate,144,47,55
Pistachio,103,105,39
Piston,140,132,109
Pitch Black,44,43,44
Pixie Green,187,205,165
Pizazz,229,127,61
Pizza,191,141,60
Plantation,62,89,76
Planter,98,93,42
Platinum,165,160,131
Platypus,61,51,52
Plum,56,26,56
Poet,192,188,212
Pohutukawa,101,28,38
Point Break,53,101,185
Polar,229,242,231
Polo Blue,138,167,204
Pompadour,106,31,68
Pompeii,220,209,181
Popcorn,234,215,170
Poppy,172,0,25
Poprock,192,201,117
Popstar,190,78,98
Porcelain,221,220,219
Porsche,223,157,91
Port Gore,59,67,108
Port Phillip,100,116,100
Portafino,244,240,155
Portage,139,152,216
Portica,240,213,85
Portland,132,126,113
Possessed,55,59,56
Pot Pourri,239,220,212
Potters Clay,132,92,64
Powder Blue,146,159,162
Prairie Sand,136,60,50
Pravda,136,128,113
Prelude,202,180,212
Pretty In Pink,239,214,218
Prim,226,205,213
Primetime,57,115,169
Primrose,228,222,142
Princess,237,184,199
Pristine Lavender,178,164,155
Promenade,248,246,223
Promise,147,105,98
Proton,150,152,140
Provincial Pink,246,227,218
Prussian Blue,25,47,65
Pueblo,110,51,38
Puerto Rico,89,186,163
Pukeko,58,40,96
Pulse,164,29,25
Pumice,186,192,180
Pumpkin,171,107,53
Punch,168,50,57
Punga,83,73,49
Pure Pewter,102,97,86
Pursuit,217,37,29
Push Play,33,88,76
Putty,205,174,112
Quadrant Grey,89,94,107
Quantum Leap,79,105,139
Quarry Stone,123,116,94
Quarter Akaroa,217,210,191
Quarter Alabaster,247,246,242
Quarter Albescent White,238,232,221
Quarter Arrowtown,168,162,147
Quarter Ash,217,214,202
Quarter Atmosphere,195,201,202
Quarter Baltic Sea,96,100,103
Quarter Barista,97,79,79
Quarter Beryl Green,217,217,202
Quarter Bianca,249,248,240
Quarter Biscotti,227,215,199
Quarter Bison Hide,208,202,186
Quarter Black White,242,241,237
Quarter Blanc,236,229,218
Quarter Bokara Grey,83,79,79
Quarter Buffalo,153,134,130
Quarter Canterbury Clay,229,210,175
Quarter Cararra,243,239,227
Quarter Caraway,225,219,204
Quarter Chicago,130,133,129
Quarter Cloud,225,220,212
Quarter Cloudy,208,201,195
Quarter Colins Wicket,183,167,134
Quarter Concrete,232,229,224
Quarter Coriander,215,215,191
Quarter Cougar,202,193,181
Quarter Craigieburn,191,183,166
Quarter Crisp Green,184,180,123
Quarter Delta,191,192,187
Quarter Doeskin,209,191,169
Quarter Drought,218,206,189
Quarter Duck Egg Blue,213,217,213
Quarter Dutch White,251,244,223
Quarter Ecru White,226,222,211
Quarter Evolution,152,146,128
Quarter Felix,116,103,101
Quarter Foggy Grey,196,195,188
Quarter Fossil,228,220,203
Quarter Foundry,82,85,87
Quarter Friar Grey,169,167,160
Quarter Frozen,198,214,225
Quarter Fuscous Grey,89,90,94
Quarter Gargoyle,178,164,149
Quarter Gravel,113,114,106
Quarter Grey Friars,94,98,103
Quarter Grey Olive,194,188,171
Quarter Haystack,238,220,196
Quarter Heathered Grey,194,186,173
Quarter Hillary,202,197,172
Quarter Imagine,201,191,187
Quarter Iron,229,230,223
Quarter Ironsand,80,78,75
Quarter Joanna,234,230,218
Quarter Joss,206,195,184
Quarter Kalgoorie Sands,205,170,143
Quarter Karaka,80,85,76
Quarter Lemon Grass,186,190,175
Quarter Lignite,107,91,82
Quarter Linen,216,213,200
Quarter Lumberjack,150,112,107
Quarter Malta,198,184,166
Quarter Masala,116,115,111
Quarter Merino,242,238,233
Quarter Milestone,219,208,203
Quarter Milk White,237,233,227
Quarter Mondo,130,120,103
Quarter Moonbeam,244,238,193
Quarter Napa,199,194,181
Quarter New Denim Blue,101,113,123
Quarter Nullarbor,178,159,136
Quarter Oilskin,130,119,110
Quarter Parchment,230,225,207
Quarter Pavlova,222,211,180
Quarter Pearl Lusta,242,237,221
Quarter Perfect Taupe,204,195,187
Quarter Periglacial Blue,204,210,206
Quarter Pohutukawa,148,37,60
Quarter Popcorn,245,234,206
Quarter Powder Blue,190,198,200
Quarter Pravda,180,171,158
Quarter Putty,224,203,159
Quarter Rakaia,215,214,211
Quarter Regent Grey,164,173,176
Quarter Rice Cake,246,244,237
Quarter Rickshaw,203,185,168
Quarter Robin Egg Blue,198,208,198
Quarter Sandspit Brown,225,218,207
Quarter Sandstone,157,150,141
Quarter Scarpa Flow,152,153,155
Quarter Sidewinder,156,151,155
Quarter Silver Chalice,199,200,198
Quarter Silver Sand,211,208,202
Quarter Sisal,228,218,196
Quarter Solitaire,245,237,223
Quarter Sorrell Brown,193,160,125
Quarter Spanish White,235,226,210
Quarter Stack,175,178,175
Quarter Stonehenge,171,165,158
Quarter Stonewall,166,159,142
Quarter Stonewashed,178,169,157
Quarter Surrender,214,216,216
Quarter Talisman,142,135,123
Quarter Tana,217,214,198
Quarter Tapa,163,164,156
Quarter Tasman,216,220,213
Quarter Taupe Grey,175,173,163
Quarter Tea,224,218,208
Quarter Thorndon Cream,233,230,218
Quarter Titania,233,230,218
Quarter Truffle,216,211,203
Quarter Tuna,101,106,112
Quarter Turbo,254,224,65
Quarter Villa White,245,241,231
Quarter Wan White,237,236,230
Quarter Wheatfield,240,236,222
Quarter White Pointer,234,232,225
Quarterback,40,43,60
Quartz,81,72,79
Quasar,161,125,96
Quayside,66,79,113
Quicksand,195,152,139
Quicksilver,136,154,151
Quickstep,167,97,95
Quill Grey,203,201,192
Quincy,106,84,69
Racing Green,35,47,44
Radiance,143,87,67
Raffia,220,198,160
Ragamuffin,232,227,211
Raging Bull,127,47,42
Raglan,41,51,49
Rain Forest,102,112,40
Raincloud,163,152,129
Rainee,179,193,177
Rajah,252,174,96
Rakaia,186,183,181
Rambler,83,71,61
Rampart,79,78,74
Ranger,109,128,99
Rangitoto Rock,67,56,49
Rangitoto,58,65,51
Rangoon Green,43,46,37
Raptor,88,88,71
Rapture,246,72,76
Rascal,181,142,123
Raspberry,127,40,56
Rasputin,47,39,53
Rata,93,31,30
Rattlesnake,70,56,53
Raven,111,116,123
Ravine,132,138,125
Ravishing,64,26,34
Razzamatazz,112,31,40
Rebel,69,52,48
Red Baron,81,29,34
Red Beech,161,98,59
Red Berry,112,31,40
Red Damask,203,111,74
Red Devil,102,42,44
Red Earth,70,32,40
Red Hot,149,43,50
Red It,117,29,40
Red Letter,117,22,49
Red Ochre,97,45,45
Red Oxide,93,31,30
Red Pepper,187,17,42
Red Planet,90,32,25
Red Red Red,131,43,41
Red Robin,125,65,56
Red Sienna,95,49,42
Red Stage,173,82,46
Red Tape,179,0,47
Redemption Blue,35,37,69
Redwood,91,52,46
Reef Gold,169,141,54
Reef,209,239,159
Reflection,131,183,208
Refresh,113,184,202
Regal Blue,32,63,88
Regatta,25,44,73
Regent Grey,121,132,136
Regent St Blue,160,205,217
Relax,153,174,208
Relic,75,72,66
Remy,246,222,218
Renaissance,136,90,100
Rendezvous,86,20,38
Renegade,89,34,40
Renew,140,215,197
Reno Sand,178,110,51
Reservoir,191,226,220
Resolution Blue,50,63,117
Retreat,57,144,155
Retro,27,82,86
Revolution,126,132,139
Revolver,55,54,63
Rhapsody,173,96,60
Rhino,61,70,83
Rhythm,120,118,151
Rialto,76,35,34
Ribbon,113,51,60
Rice Cake,239,236,222
Rice Flower,239,245,209
Rice Paper,210,214,156
Rich Cream,255,215,160
Rich Gold,161,82,38
Rickshaw,170,145,123
Ricochet,132,132,132
Rimutaka,75,60,35
Ringo,102,44,64
Rio Grande,183,198,26
Riptide,137,217,200
Rising Star,247,229,183
Rivendell,169,189,182
River Bed,85,96,97
Rivergum,73,89,71
Riverstone,121,112,103
Road Trip,131,107,72
Roadster,159,44,55
Roasted Orange,166,119,71
Rob Roy,221,173,86
Robin Egg Blue,158,170,158
Robin Hood,22,112,87
Robins Egg Blue,158,170,158
Rock Blue,147,162,186
Rock N Roll,157,0,47
Rock Salt,230,214,184
Rock Spray,157,68,45
Rock,90,77,65
Rockbottom,162,154,142
Rocket,134,40,46
Rockpool Green,49,51,44
Rockstar,61,58,60
Rocky Road,87,70,58
Rodeo Dust,199,163,132
Roller Coaster,146,56,48
Rolling Fog,218,215,223
Rolling Stone,109,120,118
Roman Coffee,125,103,87
Roman,216,98,91
Romance,244,240,230
Romantic,255,198,158
Ronchi,234,184,82
Roof Terracotta,161,71,67
Root Beer,129,77,48
Rope,142,89,60
Rose Bud Cherry,138,45,82
Rose Bud,254,171,154
Rose Of Sharon,172,81,45
Rose White,251,238,232
Rose,211,161,148
Rosehip,132,33,57
Rosewood,143,62,63
Roti,182,150,66
Rouge,169,64,100
Rough N Tumble,91,76,72
Roulette,42,77,62
Routeburn,165,153,130
Roxy,223,136,80
Royal Heath,181,75,115
Rubber Duck,255,180,55
Ruby Tuesday,249,122,89
Ruck N Maul,35,42,35
Rugged Lavender,128,129,139
Rum Swizzle,241,237,212
Rum,113,102,117
Rumour Has It,158,73,22
Russett,125,101,92
Rust,139,66,53
Rustic Red,58,24,26
Rusty Nail,141,95,44
Rutherford,127,123,89
Sabbatical,84,115,119
Saddle Brown,80,56,30
Saddle,93,78,70
Safari,192,164,105
Saffron,220,159,69
Sage,152,159,122
Sahara,183,152,38
Sail,165,206,236
Sakura,233,183,169
Salem,23,123,77
Salomie,255,214,123
Saloon,213,191,152
Salsa,119,12,37
Salt Box,105,98,104
Saltpan,238,243,229
Sambuca,59,46,37
San Felix,44,110,49
San Juan,68,87,97
San Marino,78,108,157
Sanctuary,166,132,89
Sand Dune,134,118,101
Sand,220,197,159
Sand,220,198,160
Sandal,163,135,106
Sandbar,226,195,133
Sandcastle,178,159,137
Sandrift,175,147,125
Sandspit Brown,210,198,182
Sandstone,120,109,95
Sandwisp,222,203,129
Sandy Beach,254,219,183
Sangria,130,42,50
Sanguine Brown,108,55,54
Santas Grey,153,152,167
Sante Fe,169,106,80
Sapling,225,213,166
Sapphire,63,82,129
Saratoga,85,91,44
Sargent Pepper,163,64,83
Sassy,126,42,101
Satellite,85,66,68
Satin Orange,198,64,32
Sauvignon,244,234,228
Sazerac,245,222,196
Scampi,111,99,160
Scandal,173,217,209
Scandi (Double Solitude),218,228,243
Scaramanga,96,120,108
Scarlet Gum,74,45,87
Scarlett,126,37,48
Scarpa Flow,107,106,108
Schist,135,135,111
Schooner,141,132,120
Scooter,48,142,160
Scorched Clay,126,60,45
Scoria,83,38,32
Scorpion,106,100,102
Scotch Mist,238,231,200
Scotty Silver,117,138,156
Scrub,61,64,49
Scrumptious,183,29,98
Sea Buckthorn,239,149,72
Sea Crest,32,134,143
Sea Fog,223,221,214
Sea Green,31,99,97
Sea Mist,194,213,196
Sea Nymph,138,174,164
Sea Pink,219,129,126
Sea World,50,63,117
Seachange,78,110,129
Seagrass,134,164,117
Seagull,119,183,208
Seance,105,50,110
Seashell,227,225,224
Seaweed,55,65,42
Sebedee,233,97,57
Secret Garden,109,109,38
Secret Road,157,130,97
Secrets,198,202,187
Seeker,0,146,165
Seismic,156,125,103
Selago,230,223,231
Sensual Red,144,39,66
Sentimental,255,225,212
Sentry,28,39,40
Sepia,58,47,45
Serenade,252,233,215
Serendipity,177,185,211
Serene,189,176,163
Serenity,141,191,163
Settlement,161,152,139
Shadow Green,154,192,182
Shadow Match,49,47,44
Shadowland,38,39,44
Shadowy Blue,35,53,70
Shadowy Lavender,78,74,78
Shady Lady,159,155,157
Shakespeare,96,154,184
Shalimar,248,246,168
Shapeshifter,64,70,83
Shark,52,54,58
She'll Be Right,0,124,141
Sheer Black,51,47,47
Shelter,180,161,131
Sherbert,210,224,158
Sherpa Blue,0,73,78
Sherwood Green,27,70,54
Shilo,230,178,166
Shingle Fawn,116,89,55
Shinto,166,181,198
Ship Cove,121,136,171
Ship Grey,78,78,76
Shipshape,33,66,95
Shiraz,132,40,51
Shirley Temple,255,131,65
Shocking,232,153,190
Shooting Star,253,227,54
Short Black,66,35,27
Showtime,47,38,58
Shuttle Grey,97,102,107
Siam,104,107,80
Sidecar,233,217,169
Sidewinder,85,77,79
Sienna,158,103,89
Siesta,165,154,168
Silhouette,42,37,44
Silk,187,173,161
Silver Aluminium,158,160,161
Silver Chalice,172,174,169
Silver Fern,153,147,140
Silver Grey,133,136,133
Silver Lining,127,127,125
Silver Sand,190,189,182
Silver Steel,135,135,134
Silver Streak,80,78,75
Silver Tree,103,190,144
Silvered Grey,86,91,100
Simply Red,155,42,44
Sinbad,166,213,208
Sing Song,246,224,164
Siren,105,41,59
Sirocco,104,118,110
Sisal,197,186,160
Skeptic,157,180,170
Skydiver,70,119,200
Skywater,64,70,83
Slate Brown,125,103,87
Slate,53,54,53
Slipper,244,234,228
Slugger,66,52,43
Smalt Blue,73,98,103
Smashing,173,0,32
Smiles,251,240,115
Smitten,200,64,134
Smoke Tree,187,95,52
Smokescreen,147,162,183
Smokey Ash,93,89,82
Smoky Green,121,134,124
Smoky,96,93,107
Smooch,126,32,86
Smooth Cream,218,199,156
Smooth Operator,210,184,138
Snap,91,160,208
Snapshot,80,95,103
Snow Drift,227,227,220
Snow Flurry,234,247,201
Snowy Mint,214,240,205
Snuff,228,215,229
So Cool,158,160,161
Soapstone,236,229,218
Socrates,113,109,89
Sofisticata,78,45,33
Soft Amber,207,190,165
Soft Apple,184,202,157
Soft Mint,223,240,226
Soft Peach,238,223,222
Soft Pink,242,205,187
Soft Whisper,248,234,202
Softly Softly,241,235,217
Soho,90,70,58
Solar Flare,105,62,64
Solid Gold,146,119,72
Solid Pink,133,73,76
Solitaire,234,218,194
Solitude,233,236,241
Somerset,223,221,120
Sonic Boom,37,32,66
Sonique,213,206,226
Soothe,208,187,181
Sooty,40,29,25
Sorbus,221,107,56
Sorrell Brown,157,127,97
Sorrento,154,176,172
Souffle,213,193,113
Soul,193,167,139
Soulmate,205,181,175
Sour Dough,201,181,154
Southern Cross,255,215,0
Soya Bean,111,99,75
Space Cadet,30,41,82
Space Shuttle,75,67,59
Space Station,138,140,142
Spanish Green,123,137,118
Spanish White,222,209,183
Spark,105,83,65
Spectra,55,93,79
Speed Demon,85,27,36
Spellbound,109,74,78
Spice,108,79,63
Spicy Mix,139,95,77
Spicy Pink,137,117,120
Spindle,179,196,216
Spinnaker,47,77,102
Spirulina,104,140,96
Spitfire,56,25,33
Splash,241,215,158
Splat,165,206,236
Splish Splash,41,89,139
Sponge,220,219,205
Sports Star,61,133,184
Spotlight,248,191,0
Spray Drift,45,88,119
Spray,126,205,221
Spring Fever,227,223,110
Spring Green,92,138,100
Spring Rain,163,189,156
Spring Sun,241,241,198
Spring Wood,233,225,217
Spritzer,194,226,37
Sprout,184,202,157
Spun Pearl,162,161,172
Sputnik,55,62,84
Squall,58,59,53
Squirrel,143,125,107
Squirt,164,175,205
St Kilda,0,69,89
St Tropaz,50,84,130
Stack,133,136,133
Star Dust,160,161,151
Starbell,235,193,85
Stark White,210,198,182
Starship,227,221,57
Starstruck,230,172,0
Steam Roller,95,101,110
Steel Blue,96,124,154
Steel Grey,67,70,75
Sterling,139,139,126
Stetson,119,76,73
Sticky Fingers,239,115,94
Stiletto,131,61,62
Stinger,141,112,42
Stingray,69,53,51
Stone Age,182,178,133
Stonehenge,130,122,113
Stonewall,128,118,97
Stonewashed,141,128,114
Storm Dust,101,100,95
Storm Grey,116,120,128
Storm,54,54,93
Stowaway,125,93,57
Stratos,33,38,58
Stratosphere,151,160,206
Straw,218,190,130
Streetwise,79,105,113
Strikemaster,148,106,129
Strobe,121,115,92
Stromboli,64,99,86
Studio,114,74,161
Stun,167,172,139
Style Pasifika Black Light,37,37,37
Style Pasifika Black Tan,58,47,45
Style Pasifika Blue Whale,61,77,120
Style Pasifika Brown Earth,69,41,36
Style Pasifika Burnt Charcoal,50,44,43
Style Pasifika Coconut Crab,92,60,109
Style Pasifika Dark Moss,79,77,50
Style Pasifika Dark Soil,54,45,38
Style Pasifika Dark Stone,45,45,36
Style Pasifika Dark Sun,182,162,55
Style Pasifika Dry Bamboo,136,136,91
Style Pasifika Fallen Gold,198,170,36
Style Pasifika Hibiscus Blood,101,28,38
Style Pasifika Lagoon Blue,78,105,154
Style Pasifika Lagoon Spray,147,162,183
Style Pasifika Night Fox,44,44,50
Style Pasifika Ocean Clam,106,57,104
Style Pasifika Ocean Deep,30,47,60
Style Pasifika Orange Wood,187,95,52
Style Pasifika Palm Green,102,112,40
Style Pasifika Pink Night,205,174,112
Style Pasifika Purple Deep,42,37,81
Style Pasifika Purple Flax,105,50,110
Style Pasifika Red Frangipani,131,43,41
Style Pasifika Red Pineapple,152,61,57
Style Pasifika Red Soil,78,39,40
Style Pasifika Sand Frond,179,171,110
Style Pasifika Sandalwood,183,130,57
Style Pasifika Shore Sand,165,101,49
Style Pasifika Sky White,217,208,193
Style Pasifika Turquoise Sea,39,74,93
Style Pasifika Volcanic Rock,45,47,40
Style Pasifika Whirlpool,64,99,86
Style Pasifika White Cloud,223,221,214
Sublime,205,230,93
Submarine,140,156,156
Submerge,17,55,117
Suburban,72,64,44
Subzero,91,141,189
Such Fun,72,158,168
Sugar And Spice,155,98,139
Sugar Cane,238,239,223
Sugar Loaf,204,194,171
Sulu,198,234,128
Summer Fun,234,247,201
Summer Green,143,182,156
Sumptuous,57,37,47
Sun,239,142,56
Sundance,196,170,77
Sundial,221,177,44
Sundown,248,175,169
Sunflower,218,192,26
Sunglo,199,97,85
Sunkissed,230,181,83
Sunrise,222,115,72
Sunset,192,81,74
Sunshade,250,157,73
Sunshine,156,101,49
Sunspot,126,55,46
Super Duper,66,99,159
Super Sonic,55,68,103
Superhero,55,78,136
Supernova,255,180,55
Surf Crest,195,214,189
Surf Spray Grey,200,196,197
Surf,184,212,187
Surfie Green,0,123,119
Surfs Up,31,33,66
Surrender,181,183,183
Sushi,124,159,47
Suva Grey,139,134,133
Suzie Q,221,126,143
Swamp,37,47,47
Swans Down,218,230,221
Sweet As,219,184,180
Sweet Corn,249,225,118
Sweet Dreams,249,215,126
Sweet Pink,238,145,141
Sweet Spot,234,183,183
Sweetwaters,195,209,223
Swirl,215,206,197
Swiss Coffee,219,208,202
Switched On,237,206,0
Sword,128,130,132
Swordfish,167,166,156
Sycamore,146,140,60
Symphony,196,211,180
Synchronise,121,117,100
Tabac,88,80,68
Tabasco,142,58,54
Tabby,197,178,152
Tacao,246,174,120
Tacha,210,185,96
Taffeta,153,110,158
Tahiti Gold,220,114,42
Tahuna Sands,216,204,155
Takaka,61,77,120
Talisman,101,93,80
Tall Poppy,133,53,52
Tallow,163,153,119
Tamarillo,117,43,47
Tamarind,62,47,46
Tana,184,181,161
Tandoori,141,69,50
Tangaroa,30,47,60
Tangerine,205,93,52
Tango,212,111,49
Tao Grey,50,52,54
Tapa,124,124,114
Tapestry,179,112,132
Tara,222,241,221
Tarawera,37,60,72
Tarmac,111,111,110
Tarot,56,41,61
Tasman,186,192,179
Taupe Grey,137,132,120
Tawny Port,100,58,72
Tax Break,73,101,105
Te Papa Green,43,75,64
Tea,191,181,162
Teak Stain,78,53,41
Teak,171,137,83
Teal Blue,37,72,85
Techno,142,136,110
Teddy,239,199,65
Templestone,107,114,104
Tempo,70,43,49
Tempt,154,57,69
Temptress,60,33,38
Tequila,244,208,164
Teranova,122,58,43
Terracotta Hit,142,80,55
Terracotta Pink,155,61,61
Terrain,173,173,153
Texas Rose,252,176,87
Texas,236,230,126
Thatch Green,84,78,49
Thatch,177,148,143
Thistle,199,189,149
Thor,105,127,121
Thorndon Cream,220,215,198
Three Wishes,210,218,237
Thriller,75,70,75
Thunder,77,77,75
Thunderbird,146,56,48
Tia Maria,151,66,45
Tiara,185,195,190
Tiber,24,67,67
Tickled Pink,150,44,84
Tidal,240,245,144
Tide,190,180,171
Tiebreaker,142,151,171
Tiger Lily,221,229,116
Tiki Tour,35,64,64
Tile Green,38,67,58
Timber Green,50,67,54
Timberland,76,51,42
Timbuktu,127,108,67
Time Machine,143,127,108
Time Out,170,194,227
Time Warp,55,68,103
Timekeeper,65,89,90
Tinkerbell,252,215,99
Tinpan Alley ,92,91,89
Tipping Point,97,44,37
Tiri,70,65,62
Titan White,221,214,225
Titania,202,199,185
Toast,159,113,95
Toasted Green,101,85,53
Tobacco Brown,109,88,67
Tobago,68,54,45
Toffee ,142,89,60
Toffee,142,89,60
Toi Toi,183,173,139
Toledo,62,38,49
Tolopea,45,37,65
Tom Thumb,79,99,72
Tom Tom,146,130,127
Tomahawk,82,67,64
Tonto,159,149,150
Tonys Pink,231,158,136
Toorak,57,37,35
Top Gear,36,34,26
Top Secret,122,172,33
Topaz,129,124,135
Topspin,66,113,32
Topsy Turvy,49,54,105
Torea Bay,53,61,117
Tornado,39,45,60
Torque,90,87,85
Tory Blue,55,78,136
Tosca,116,64,66
Totem Pole,136,53,49
Toto,81,157,175
Touch Wood,58,55,46
Touche,255,165,85
Touchstone,82,79,70
Tower Grey,156,172,165
Traccia,42,51,53
Tradewind,109,175,167
Traffic Light,205,93,52
Traffic,108,109,104
Trailblazer,95,76,39
Trainspotter,68,73,63
Tranquil,221,237,233
Transformer,79,72,75
Transmission,159,161,158
Travertine,226,221,199
Travis,183,158,103
Treasure Chest,155,142,110
Treasure,117,138,156
Tree Frog,80,167,67
Tree Poppy,226,129,59
Treehouse,60,52,46
Treetops,166,162,143
Trendy Green,126,132,36
Trendy Pink,128,93,128
Trinidad,197,79,51
Triple Akaroa,164,151,122
Triple Arrowtown,97,88,71
Triple Ash,159,155,134
Triple Athens Grey,194,197,198
Triple Bison Hide,154,143,119
Triple Black White,215,213,204
Triple Blanc,206,195,175
Triple Canterbury Clay,181,148,101
Triple Colins Wicket,122,100,65
Triple Concrete,183,182,181
Triple Delta,120,121,115
Triple Doeskin,159,132,96
Triple Drought,164,141,112
Triple Dune,58,56,51
Triple Dutch White,243,218,169
Triple Fossil,190,178,145
Triple Friar Grey,102,97,86
Triple Grey Olive,134,123,93
Triple Hillary,131,122,83
Triple Joss,156,135,115
Triple Lemon Grass,129,128,104
Triple Lumberjack,90,55,47
Triple Malta,140,118,98
Triple Masala,65,62,55
Triple Merino,213,207,195
Triple Milestone,165,149,145
Triple Mondo,64,55,42
Triple Napa,128,115,97
Triple Nullarbor,114,90,65
Triple Parchment,189,175,150
Triple Pavlova,159,137,107
Triple Pearl Lusta,235,223,195
Triple Perfect Taupe,134,122,111
Triple Pravda,103,92,76
Triple Putty,183,139,75
Triple Rakaia,161,154,152
Triple Rice Cake,229,222,205
Triple Rickshaw,144,115,89
Triple Sandcastle,163,138,109
Triple Sea Fog,216,213,206
Triple Sisal,165,149,120
Triple Solitaire,228,203,171
Triple Spanish White,213,196,161
Triple Stack,101,102,96
Triple Stonehenge,102,92,82
Triple Stonewall,97,90,71
Triple Surrender,153,156,157
Triple Tana,159,155,130
Triple Tapa,91,90,80
Triple Tea,170,159,139
Triple Thorndon Cream,197,189,170
Triple Truffle,163,155,142
Triple Wheatfield,209,198,166
Triple White Pointer,200,195,181
Triumph,137,96,58
Trojan,117,120,120
Tropical Blue,174,201,235
Troubadour,86,34,90
Trouble,87,22,32
Trout,76,83,86
True Blue,51,61,87
True V,142,114,199
Truffle,190,185,173
Tsunami,107,131,147
Tuatara,69,70,66
Tuft Bush,249,211,190
Tulip Tree,227,172,61
Tumbleweed,75,65,42
Tuna,70,73,78
Tundora,88,84,82
Turbo,245,204,35
Turkish Delight,195,126,139
Turkish Rose,165,110,117
Turmeric,174,144,65
Turtle Green,54,62,29
Tuscany,173,98,66
Tusk,227,229,177
Tussock,191,145,75
Tutti Frutti,159,211,133
Tutu,248,228,227
Tweet,212,188,0
Twentyfourseven,250,212,67
Twilight Blue,244,246,236
Twilight,218,192,205
Twine,193,145,86
Twister,147,130,85
Twizel,142,80,55
Uhi,37,37,37
Uluru,191,155,103
Umber White,237,232,223
Undercover,100,137,133
Undercurrent,54,92,108
Unicorn,159,144,208
Unwind,152,183,175
Upstage,51,32,51
Urban Legend,66,51,58
Urbane,217,209,207
Valencia,212,87,78
Valentino,56,44,56
Valhalla,42,43,65
Van Cleef,82,57,54
Vanilla Ice,235,210,209
Vanilla,204,182,155
Vanquish,99,39,47
Varden,253,239,211
Vault,86,87,64
Vegas,252,179,88
Velocity,75,64,66
Venetian Red,91,31,34
Venice Blue,44,87,120
Ventura,144,124,56
Venus,139,125,130
Verdigris,98,96,62
Verdun Green,72,83,26
Vermilion,146,42,49
Vermont,178,190,97
Verve,93,46,60
Vesuvius,168,85,51
Viaduct,169,159,151
Vibe,172,49,66
Victoria,86,73,133
Vida Loca,95,146,40
Vienna,232,216,175
Viking,77,177,200
Viktor,85,94,83
Villa White,240,233,214
Vin Rouge,149,82,100
Vindaloo,167,79,32
Vintage,167,128,135
Viola,197,143,157
Violent Violet,46,34,73
Violet,47,38,60
Viridian Green,75,95,86
Vis Vis,249,228,150
Vision,160,155,178
Vista Blue,151,213,179
Vista White,227,223,217
Vitality,61,179,136
Vitra,161,220,199
Vixen,129,52,43
Volcano,78,39,40
Voltage,141,144,148
Voodoo,68,50,64
Vortex,58,56,91
Vroom,53,61,117
Vulcan,54,56,60
Wafer,212,187,177
Waikawa Grey,91,110,145
Waiouru,76,78,49
Waiwherowhero,134,73,44
Walnut,121,77,46
Wan White,228,226,220
Wanaka,40,73,98
Wanderlust,136,132,60
Wanted,126,25,40
Waratah,85,105,139
Warhol,155,97,95
Warlord,69,64,79
Warm Kwila,117,58,42
Warmed Brown,74,48,43
Warrior,45,59,66
Wasabi,132,145,55
Washed Green,144,151,130
Water Leaf,182,236,222
Watercourse,0,110,78
Waterfront,62,127,157
Waterloo ,114,114,130
Wattle,214,202,61
Watusi,242,205,187
Wave Rider,65,63,110
Wavelength,60,104,134
Wax Flower,238,179,158
Wazzup,188,148,37
We Peep,253,215,216
Weathered Blue,103,117,131
Weathered Grey,119,111,111
Weathered Orange,193,108,32
Weathered Yellow,224,218,159
Wedgewood,76,107,136
Well Read,142,53,55
Wellywood,163,217,45
West Coast,92,81,47
West Side,229,130,58
Westar,212,207,197
Western Red Cedar,122,55,42
Western Red,107,37,44
Westwood,144,155,103
Wet N Wild,37,67,117
Wewak,241,145,154
Whale Tail,0,57,103
Wham,95,179,58
Wheatfield,223,215,189
Wheel Of Fortune,42,123,67
Whipped Cream,241,236,214
Whirlwind,107,140,146
Whiskey Sour,212,145,93
Whiskey,210,144,98
Whisper,239,230,230
White Ice,215,238,228
White Lilac,231,229,232
White Linen,238,231,220
White Metal,148,149,148
White Nectar,248,246,216
White Pointer,218,214,204
White Rock,212,207,180
White Thunder,213,215,216
White,245,245,242
Whiteout,206,202,200
Whitewash,239,236,222
Whitewater,225,225,220
Whizz Bang,162,58,52
Wicked,54,47,80
Wild Rice,227,212,116
Wild Sand,231,228,222
Wild Thing,250,212,67
Wild West,154,84,64
Wild Willow,190,202,96
Wilderness,136,136,91
Wildflower,241,226,201
William,83,115,111
Willow Brook,223,230,207
Willow Grove,105,117,92
Wimbledon,83,109,51
Winchester,81,78,74
Wind Talker,58,72,89
Windblown Green,126,134,123
Windfall,0,133,117
Windsor,70,44,119
Windswept,67,65,65
Wine Berry,82,44,53
Wine Trail,39,41,45
Winter Hazel,208,195,131
Wireless,85,83,80
Wishing Well,17,55,85
Wishlist,101,146,149
Wisp Pink,249,232,226
Wisteria,164,135,139
Wistful,162,158,205
Witch Haze,251,240,115
Wolverine,101,89,85
Wombat,103,87,68
Wonderland,187,151,187
Wood Bark,48,38,33
Woodburn,70,54,41
Woodland,98,103,70
Woodrush,69,64,43
Woodsmoke,43,50,48
Woodstock,131,156,96
Woody Bay,51,52,58
Woody Brown,85,69,69
Wot Eva,68,149,164
Wow,52,52,103
Wrangler,128,103,90
X Factor,104,27,43
Xanadu,117,135,110
Xotic,134,51,54
Yabbadabbadoo,0,139,151
Yarra,32,96,142
Yasna,84,74,80
Yeehaa,0,108,152
Yellow Metal,115,99,62
Yellow Sea,244,159,53
Yellow Submarine,232,210,51
Ying Yang,218,220,190
Your Pink,255,197,187
Yucca,104,120,107
Yukon Gold,130,106,33
Yuma,199,184,130
Zambezi,107,90,90
Zanah,178,198,177
Zappo,196,192,226
Zeal,145,224,183
Zen,210,208,174
Zephyr,128,154,198
Zeppelin,56,42,52
Zest,198,114,59
Zeus,59,60,56
Zibibbo,81,36,43
Ziggurat,129,166,170
Zinc White,225,219,208
Zinger,135,61,66
Zinzan,25,42,65
Zion,172,121,17
Zircon,222,227,227
Zodiac,65,58,93
Zombie,221,194,131
Zomp,57,167,141
Zoop De Loop,37,70,131
Zorba,162,149,137
Zuccini,23,70,46
Zulu,88,81,86
Zumthor,205,213,213
Zydeco,32,72,63
'''.strip()
comma = ","
print(f"""'''{attr}'''""")
for i, line in enumerate(data.split("\n")):
    loc = line.find(comma)
    name = line[:loc]
    color = line[loc + 1:].split(comma)
    r, g, b = [int(i) for i in color]
    h = f"#{r:02x}{g:02x}{b:02x}"
    print(f"{name}, #{r:02x}{g:02x}{b:02x}")
print()
