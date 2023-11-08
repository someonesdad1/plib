'''
Description of program
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import re
        import sys
    if 1:   # Custom imports
        from columnize import Columnize
        from wrap import dedent, HangingIndent
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        class G:
            pass
        g = G()
        g.di = {
            201: 'NJ Bergen County and Hudson County',
            202: 'Washington, D.C',
            203: 'CT Bridgeport, Danbury, New Haven, Waterbury, and southwestern Connecticut',
            204: 'Manitoba',
            205: 'AL Birmingham, Tuscaloosa, and parts of western and central Alabama',
            206: 'WA Seattle area',
            207: 'ME all except Estcourt Station',
            208: 'ID',
            209: 'CA Stockton, Modesto, Merced, Tracy, San Andreas, and a part of central California extending into central Yosemite National Park',
            210: 'TX San Antonio metropolitan area',
            211: 'Not assignable; N11 code for community services, local/regional information service',
            212: 'NY New York City: Manhattan only, except for Marble Hill',
            213: 'CA central area of Los Angeles',
            214: 'TX Dallas metropolitan area',
            215: 'PA Philadelphia area, including all of Philadelphia and its suburbs in eastern Montgomery County, most of Bucks County, and a very small portion of Berks County around the Hereford area, which is served by the Pennsburg 679 exchange',
            216: 'OH Cleveland area',
            217: 'IL Springfield, Champaign, Decatur, Urbana, Lincoln, and parts of central Illinois',
            218: 'MN Duluth, Moorhead, Thief River Falls, Bemidji, Brainerd, International Falls, and most of northern Minnesota',
            219: 'IN Gary area',
            220: 'OH suburban Columbus, central Ohio outside of Franklin County',
            223: 'PA Harrisburg, Gettysburg, Lancaster, York, and most of south-central Pennsylvania',
            224: 'IL North and northwest suburbs of Chicago',
            225: 'LA Baton Rouge area and east-central Louisiana',
            226: 'Ontario:  London, Windsor, Kitchener-Waterloo, Cambridge, and most of southwestern Ontario',
            227: 'MD Silver Spring; Washington, D.C., suburbs; all counties which touch the Potomac River; Hagerstown, Frederick, Rockville, Cumberland; and fixed-line telephones in western Maryland',
            228: 'MS Gulfport, Biloxi, Pascagoula, Bay St. Louis, and southmost Mississippi',
            229: 'GA Albany, Valdosta, Bainbridge, Americus, Fitzgerald, and most of southwestern Georgia',
            231: 'MI Muskegon, Traverse City, Ludington, Petoskey, and a part of northwestern Michigan',
            234: 'OH Akron, Canton, Youngstown, Warren, and most of northeastern Ohio',
            235: 'MO Columbia, Jefferson City, Hannibal, Cape Girardeau, Farmington, Lake of the Ozarks, Poplar Bluff, and most of eastern Missouri excluding the St. Louis metropolitan area',
            236: 'British Columbia:  all, and the isolated border town of Hyder, Alaska, USA',
            239: 'FL southwest coast: all of Lee County, Collier County, the mainland part of Monroe County, including Cape Coral, Fort Myers, Naples, and Everglades',
            240: 'MD Silver Spring; Washington, D.C., suburbs; all counties which touch the Potomac River; Hagerstown, Frederick, Rockville, Cumberland; and landline telephones in western Maryland',
            242: 'The Bahamas:  all',
            246: 'Barbados:  all',
            248: 'MI Oakland County',
            249: 'Ontario:  Northeastern Ontario and Central Ontario: Greater Sudbury, Sault Ste. Marie, North Bay, etc.',
            460: 'reserved as a fourth area code for the region.',
            250: 'British Columbia:  Victoria: Prince George, Prince Rupert, Kelowna, all areas except for Metro Vancouver and the Fraser Valley; and the isolated border town of Hyder, Alaska, USA',
            251: 'AL Mobile County, Baldwin County, Bay Minette, Jackson, Brewton, Citronelle, and a part of southwestern Alabama',
            252: 'NC Greenville, New Bern, Elizabeth City, Kinston, Outer Banks, Rocky Mount',
            253: 'WA Tacoma, Lakewood, Auburn, Puyallup, Enumclaw, Spanaway, and the southern suburbs of Seattle',
            254: 'TX Waco, Killeen, Temple, Belton, and Stephenville',
            256: 'AL Huntsville, Decatur, Cullman, Gadsden, Madison, Florence, Sheffield, Tuscumbia, Fort Payne, Scottsboro, and most of northern Alabama',
            257: 'will overlay 778/236/672:  British Columbia',
            260: 'IN Fort Wayne, New Haven, Decatur, Angola, Huntington, Wabash, and most of northeastern Indiana',
            262: 'WI Racine, Kenosha, Menomonee Falls, Waukesha, and most of southeastern Wisconsin excluding Milwaukee County',
            263: 'Quebec:  Montreal metropolitan area',
            264: 'Anguilla:  all',
            267: 'PA Philadelphia and surrounding suburban area',
            268: 'Antigua and Barbuda:  all',
            269: 'MI Battle Creek, Kalamazoo, Benton Harbor, Allegan, Hastings, St. Joseph, and most of southwestern Michigan',
            270: 'KY Owensboro, Paducah, Bowling Green, Hopkinsville, Henderson, Elizabethtown, and most of western Kentucky',
            272: 'PA northeastern',
            274: 'WI Appleton, Sheboygan, Oshkosh, Green Bay, Manitowoc, Marquette, Fond du Lac, and parts of eastern Wisconsin-but not in Milwaukee County',
            276: 'VA Bristol, Abingdon, Wytheville, Martinsville, Bluefield, Big Stone Gap, and the remainder of southwestern Virginia',
            279: 'CA the Sacramento Metropolitan Area',
            281: 'TX Houston area',
            283: 'OH Cincinnati, Middletown, Hamilton, Lebanon, and parts of southern and southwestern Ohio',
            284: 'British Virgin Islands:  all',
            289: 'Ontario:  Oshawa-Hamilton and Golden Horseshoe, excluding Toronto 416 but including its adjacent suburbs',
            537: 'reserved as a fifth area code for the region.',
            301: 'MD Silver Spring; Washington, D.C., suburbs; all counties which touch the Potomac River; Hagerstown, Frederick, Rockville, Cumberland; and land line telephones in western Maryland',
            302: 'DE all',
            303: 'CO Denver, Boulder, Longmont, Aurora, Golden, Limon, Littleton, Centennial; central Colorado',
            304: 'WV',
            305: 'FL all of Miami-Dade County and the Florida Keys',
            306: 'Saskatchewan',
            307: 'WY all',
            308: 'NE North Platte, Scottsbluff, McCook, Kearney, Grand Island; western Nebraska',
            309: 'IL Peoria, Bloomington, Moline, Rock Island, Galesburg; west-central Illinois',
            310: 'CA southwestern coastal and coastal-adjacent areas of Los Angeles County, including Beverly Hills, Brentwood, Malibu, Pacific Palisades, Redondo Beach, Santa Monica, Torrance, and Santa Catalina Island',
            311: 'Not assignable; N11 code for non-emergency calls to local government, or to reach the city or county hall',
            312: 'IL downtown Chicago',
            313: "MI Dearborn, the Grosse Pointes, Detroit, and the latter's enclaves of Hamtramck and Highland Park",
            314: 'MO St. Louis, St. Louis County, Florissant, Crestwood, Hazelwood, Kirkwood, and surrounding suburbs of St. Louis',
            315: 'NY Syracuse, Utica, Watertown; north-central New York',
            316: 'KS Wichita metropolitan area, McConnell Air Force Base, Augusta, El Dorado, and Mulvane',
            317: 'IN Indianapolis and immediate metro area including Carmel, Fishers, Noblesville, Westfield, Greenwood, Mooresville, Beech Grove, Plainfield, Avon, Brownsburg, and Zionsville',
            318: 'LA Shreveport-Bossier City, Monroe, Alexandria, Fisher, Tallulah, and most of northern Louisiana',
            319: 'IA Cedar Rapids, Waterloo, Burlington, Iowa City; parts of eastern Iowa',
            320: 'MN St. Cloud, Alexandria, Morris, Hutchinson, Sandstone, Appleton, Willmar; central Minnesota',
            321: 'FL Orlando, Cocoa, Melbourne, Rockledge, Titusville, St Cloud, and east-central Florida',
            323: 'CA Downtown Los Angeles and surrounding areas',
            324: 'FL Jacksonville, St. Augustine, Starke, and most of northeastern Florida',
            325: 'TX Abilene, San Angelo, Sweetwater, Snyder',
            326: 'OH Dayton, Springfield, and southwestern Ohio north and east of the Cincinnati metropolitan area',
            327: 'AR Texarkana, Jonesboro, Pine Bluff; southern, eastern, and northeastern Arkansas',
            329: 'NY Dutchess, Orange, Putnam, Rockland, Sullivan, and Ulster counties',
            330: 'OH Akron, Canton, Youngstown, Warren, and most of northeastern Ohio',
            331: 'IL Aurora, Naperville, Oswego; western suburbs of Chicago',
            332: 'NY New York City: Manhattan only, except for Marble Hill',
            334: 'AL Montgomery, Auburn, Dothan, Enterprise, Eufaula, Opelika, Phenix City, Selma, Tuskegee, and most of southeastern Alabama',
            336: 'NC the Piedmont Triad, Wilkesboro, Roxboro, and most of northwestern North Carolina',
            337: 'LA Lafayette, Lake Charles, Leesville, New Iberia, Opelousas, and most of southwestern Louisiana',
            339: 'MA Canton, Hanson, Lincoln, Nahant, Plympton, Revere, Stoughton, Winchester, and east-central Massachusetts',
            340: 'U.S. Virgin Islands:  all',
            341: 'CA coastal regions of the East Bay-Oakland, Fremont, Hayward, Richmond, Berkeley, and Alameda',
            343: 'Ontario:  Ottawa metropolitan area and southeastern Ontario',
            345: 'the Cayman Islands:  all',
            346: 'TX Houston area',
            347: 'NY New York City: The Bronx, Brooklyn, Queens, Staten Island, and Marble Hill',
            350: 'CA Stockton, Modesto, Merced, Tracy, San Andreas, and a part of central California extending into central Yosemite National Park',
            351: 'MA Ashby, Barre, Boxborough, Carlisle, Groveland, Rowley, Wendell, Wenham, and northeastern Massachusetts',
            352: 'FL Gainesville, Ocala, Inverness, Dunnellon, and a part of central Florida',
            353: 'WI Madison, La Crosse, Platteville, Beloit, and most of southwestern Wisconsin',
            354: 'Quebec:  central southern Quebec; surrounding City of Montreal',
            360: 'WA Olympia, Vancouver, Bellingham, Bremerton, Port Angeles, Aberdeen, and most of western Washington, except the Seattle metropolitan area',
            361: 'TX Corpus Christi, Victoria, George West, and much of south Texas',
            363: 'NY Nassau County, including Hempstead and Mineola',
            364: 'KY Owensboro, Paducah, Bowling Green, Hopkinsville, Henderson, Elizabethtown, and most of western Kentucky',
            365: "Ontario:  Oshawa-Hamilton and the Golden Horseshoe, excluding Toronto's 416 but including its adjacent suburbs",
            367: 'Quebec:  Quebec City, Saguenay, the Gaspé Peninsula, Côte-Nord, Chibougamau, St-Georges',
            368: 'Alberta:  all',
            568: 'reserved as a fifth area code for the region.',
            369: 'CA Vallejo, Crescent City, Eureka, Redwoods National Park, Santa Rosa, Ukiah, and most of northwestern California',
            380: 'OH Columbus and Franklin County',
            382: 'Ontario:  London, Windsor, Kitchener-Waterloo, Cambridge, and most of southwestern Ontario',
            385: 'UT Counties of Davis; Morgan; Salt Lake; Utah; and Weber along the Wasatch Front, including the cities of Salt Lake City, Ogden, and Provo',
            386: 'FL Daytona Beach, Lake City, Live Oak, Crescent City, and parts of northeastern Florida',
            401: 'RI all',
            402: 'NE Omaha, Lincoln, Norfolk, Superior, and most of eastern Nebraska',
            403: 'Alberta:  Calgary, Banff, Red Deer, Medicine Hat, Lethbridge, Brooks, and most of southern Alberta',
            404: 'GA Atlanta and the Atlanta metropolitan area inside of the Interstate 285 perimeter highway',
            405: 'OK Oklahoma City, Stillwater, Edmond, Norman, Shawnee, and most of central Oklahoma',
            406: 'MT all',
            407: 'FL Orlando, Sanford, St. Cloud, Kissimmee, and a part of east-central Florida',
            408: 'CA San Jose, Cupertino, Los Altos, Los Altos Hills, Los Gatos, Milpitas, Mountain View, Santa Clara, Sunnyvale, and Silicon Valley',
            409: 'TX Beaumont, Galveston, Orange, Port Arthur, and Texas Cit',
            410: "MD except for St. Mary's County, all counties and cities which touch the Chesapeake Bay, the Atlantic Ocean, or Delaware,",
            411: 'Not assignable; N11 code for local information, local directory assistance',
            412: 'PA Pittsburgh region',
            413: 'MA western part',
            414: 'WI Milwaukee County includes cities of Milwaukee, West Allis, Oak Creek, and others',
            415: 'CA San Francisco, Daly City, Brisbane, and most of Marin County',
            416: 'Ontario:  the City of Toronto',
            417: 'MO Springfield, Joplin, Branson, Lamar, Lebanon, and most of southwestern Missouri',
            418: 'Quebec:  Quebec City, Saguenay, the Gaspé Peninsula, Côte-Nord, Chibougamau, St-Georges',
            419: 'OH Toledo area and most of northwestern Ohio',
            420: 'overlay for area code 928 in Arizona',
            423: 'TN two discontiguous portions of East Tennessee in the northeast and in the southeast',
            424: 'CA southwestern coastal and coastal-adjacent areas of Los Angeles County; also Santa Catalina Island',
            425: 'WA northern and eastern suburbs of Seattle',
            428: 'New Brunswick',
            430: 'TX',
            431: 'Manitoba',
            432: 'TX West Texas: Midland, Odessa, Big Spring, Alpine, Fort Stockton',
            434: 'VA Charlottesville, Lynchburg, Danville, and south-central Virginia',
            435: 'UT Most of Utah outside the Salt Lake City, Ogden, and Provo metropolitan areas in northern Utah',
            436: 'OH surrounding Cleveland on three sides, including: Elyria, Lorain, Oberlin, Ashtabula, and most of north-central Ohio',
            437: 'Ontario:  Toronto metropolitan area',
            438: 'Quebec:  Montreal metropolitan area',
            440: 'OH surrounding Cleveland on three sides, including: Elyria, Lorain, Oberlin, Ashtabula, and most of north-central Ohio',
            441: 'Bermuda:  all',
            442: 'CA most of the desert and mountain portions of the southeastern two-thirds of California',
            443: 'MD',
            445: 'overlay of 215 and 267:  Philadelphia, Pennsylvania',
            447: 'IL Springfield, Champaign, Decatur, Urbana, Lincoln, and parts of central Illinois',
            448: 'FL Panhandle',
            450: 'Quebec:  central southern Quebec; surrounds City of Montreal',
            456: 'not in use; became available for geographic assignment in 2023',
            457: 'LA Shreveport-Bossier City, Monroe, Alexandria, Fisher, Tallulah, and most of northern Louisiana',
            458: 'OR Eugene, Medford, Bend, Pendleton, Corvallis, Ontario, Burns; excludes the Portland metropolitan area',
            463: 'IN Indianapolis and immediate metro area including Carmel, Fishers, Noblesville, Westfield, Greenwood, Mooresville, Beech Grove, Plainfield, Avon, Brownsburg, and Zionsville',
            464: 'IL western and southern portions of suburban Cook County and far eastern sections of Will County and southern and near western suburbs of Chicago',
            468: 'Quebec:  Western Québec, except Montréal 514 and surrounding area 450: a large area including Abitibi-Témiscamingue, Estrie, Mauricie, Outaouais, Sherbrooke, and Trois-Rivières',
            469: 'TX Dallas metropolitan area',
            470: 'GA Metro Atlanta',
            472: 'NC Fayetteville, Wilmington, Fort Liberty, Seymour Johnson Air Force Base, Jacksonville, Lumberton, and much of southeastern North Carolina',
            473: 'Grenada:  all',
            474: 'Saskatchewan',
            475: 'CT Bridgeport, Danbury, New Haven, Waterbury, and southwestern Connecticut',
            478: 'GA Macon, Warner Robins, Swainsboro, Milledgeville, Perry, and a part of central Georgia',
            479: 'AR Fort Smith, Fayetteville, Rogers, and most of northwestern Arkansas',
            480: 'AZ Phoenix metropolitan area; primarily the East Valley',
            484: 'PA Chester, Lehigh Valley, Norristown, Reading; parts of southeastern Pennsylvania',
            500: 'personal communications services',
            501: 'AR Little Rock, Hot Springs, and much of central Arkansas, but not Pine Bluff',
            502: 'KY Louisville, Frankfort, Shelbyville, Bardstown, and most of north-central Kentucky',
            503: 'OR Portland, Salem, Hillsboro, Beaverton, St. Helens, Tillamook, Astoria, and most of northwestern Oregon',
            504: 'LA New Orleans metropolitan area',
            505: 'NM Albuquerque, Santa Fe, Farmington, Gallup, and all of northwestern New Mexico, and a part of central New Mexico',
            506: 'New Brunswick:  all',
            507: 'MN Rochester, Mankato, Austin, Marshall, Winona, and most of southern Minnesota',
            508: 'MA Berkley, Dennis, Douglas, Easton, Edgartown, Oakham, Oxford, Upton, and southeastern Massachusetts',
            509: 'WA all of eastern Washington, including Spokane, Ellensburg, Pullman, the Tri-Cities area, Walla Walla, Wenatchee, and Yakima',
            510: 'CA coastal regions of the East Bay: Oakland, Fremont, Hayward, Richmond, Berkeley, and Alameda',
            511: 'Not assignable; N11 code for local information for transportation and road conditions, local police non-emergency services',
            512: 'TX Austin, San Marcos, and parts of central Texas',
            513: 'OH Cincinnati, Middletown, Hamilton, Lebanon, and parts of southern and southwestern Ohio; this area code used to also include Dayton',
            514: 'Quebec:  Montreal metropolitan area',
            515: 'IA Des Moines, Ames, Fort Dodge, Jefferson, Indianola, and most of north-central Iowa',
            516: 'NY Nassau County, including Hempstead and Mineola',
            517: 'MI Lansing, Jackson, Charlotte, Deerfield, Addison, and most of south-central Michigan',
            518: 'NY Albany, Schenectady, Plattsburgh, Saranac Lake, Lake George, Westport, and most of northeastern New York',
            519: 'Ontario:  London, Windsor, Kitchener-Waterloo, Cambridge, Brantford, Guelph, and most of southwestern Ontario',
            520: 'AZ Tucson, Nogales, Fort Huachuca, and most of southeastern Arizona',
            521: 'personal communications services',
            522: 'personal communications services',
            523: 'personal communications services',
            524: 'personal communications services',
            525: 'personal communications services',
            526: 'personal communications services',
            527: 'personal communications services',
            528: 'personal communications services',
            529: 'personal communications services',
            530: 'CA Redding, Auburn, Chico, Davis, the California shore of Lake Tahoe, Placerville, Susanville, Truckee, Yreka, and most of northeastern California',
            531: 'NE Omaha, Lincoln, Norfolk, Superior, and most of eastern Nebraska',
            533: 'personal communications services',
            534: 'WI',
            539: 'OK Tulsa, Bartlesville, McAlester, Muskogee, Henryetta, and northeastern Oklahoma',
            540: 'VA Fredericksburg, Roanoke, Blacksburg, Harrisonburg, Lexington, Staunton, Winchester, and parts of north-central Virginia',
            541: 'OR Eugene, Bend, Corvallis, Medford, Pendleton, and all of Oregon, except metropolitan northwestern Oregon, including Portland, Salem, Astoria, etc.',
            544: 'personal communications services',
            548: 'Ontario:  London, Windsor, Kitchener-Waterloo, Cambridge, and most of southwestern Ontario',
            551: 'NJ Bergen County and Hudson County',
            555: 'not in use; code is reserved for directory assistance applications',
            557: 'MO St. Louis, St. Louis County, Florissant, Crestwood, Hazelwood, Kirkwood, and surrounding suburbs of St. Louis',
            559: 'CA Fresno, Hanford, Madera, Tulare, Visalia, and parts of the San Joaquin Valle',
            561: 'FL Palm Beach County, including Palm Beach, West Palm Beach, Boca Raton, Boynton Beach, etc.',
            562: 'CA Downey, Long Beach, Whittier, Norwalk, La Habra, Lakewood, Pico Rivera, and most of southeastern Los Angeles County',
            563: 'IA Davenport, Dubuque, Clinton, Bettendorf, and most of eastern and northeastern Iowa',
            564: 'WA Olympia, Vancouver, Bellingham, Bremerton, Port Angeles, Aberdeen, and all of western Washington',
            566: 'personal communications services',
            567: 'OH Northwest',
            570: 'PA the Wyoming Valley, including Scranton and Wilkes-Barre; Bloomsburg; Danville; Nanticoke; Williamsport; and most of northeastern Pennsylvania',
            571: 'VA Washington, D.C. suburbs, including Arlington and Alexandria',
            572: 'OK Oklahoma City, Stillwater, Edmond, Norman, Shawnee, and most of central Oklahoma',
            573: 'MO Columbia, Jefferson City, Hannibal, Cape Girardeau, Farmington, Lake of the Ozarks, Poplar Bluff, and most of eastern Missouri excluding the St. Louis metropolitan area',
            574: 'IN South Bend, Elkhart, Goshen, Logansport, and most of north-central Indiana',
            575: 'NM Las Cruces, Roswell, Carlsbad Caverns National Park, Socorro, Taos, and Truth or Consequences; excludes central (Albuquerque and its suburbs',
            577: 'personal communications services',
            579: 'Quebec:  central southern Quebec; surrounds City of Montreal',
            580: 'OK Ponca City, Ada, Ardmore, Enid, Lawton, Elk City, and most of southern and western Oklahoma',
            581: 'Quebec:  Quebec City, Saguenay, the Gaspé Peninsula, Côte-Nord, Chibougamau, St-Georges',
            582: 'PA Erie, State College, Altoona, Clearfield, Emporium, Johnsonburg, Johnstown, Meyersdale, Ridgway, Somerset, and most of northwestern and parts of central Pennsylvania',
            584: 'Manitoba',
            585: 'NY Rochester, Batavia, and much of western New York',
            586: 'MI Macomb County',
            587: 'Alberta:  all',
            588: 'personal communications services',
            600: 'Canadian non-geographic tariffed: teleprinter, caller-pays mobile, etc.',
            601: 'MS Jackson, Hattiesburg, Meridian, Natchez, Vicksburg, and most of central Mississippi',
            602: 'AZ Phoenix metropolitan area; primarily the city of Phoenix',
            603: 'NH all',
            604: 'British Columbia:  Metro Vancouver Regional District, Fraser Valley Regional District, Whistler, and the remaining portion of 604 not part of an overlay complex',
            605: 'SD all',
            606: 'KY Ashland, Pikeville, Hazard, Somerset, London, Corbin, Maysville, and much of eastern Kentucky',
            607: 'NY Binghamton, Elmira, Cortland, Norwich, Ithaca, and most of south-central New York',
            608: 'WI Madison, La Crosse, Platteville, Beloit, and most of southwestern Wisconsin',
            609: 'NJ Trenton, Atlantic City, Princeton, and most of central & southeastern New Jersey',
            610: 'PA Chester, Lehigh Valley, Norristown, Reading; parts of southeastern Pennsylvania',
            611: 'Not assignable; N11 code for repair service for land-line telephones, customer service for wireless carriers',
            612: 'MN Minneapolis, Fort Snelling, St. Anthony, and Richfield',
            613: 'Ontario:  Ottawa metropolitan area and southeastern Ontario',
            614: 'OH Columbus and Franklin County',
            615: 'TN Northern Middle Tennessee including Nashville',
            616: 'MI Grand Rapids, Greenville, Holland, Ionia, Zeeland, and most of southwestern Michigan',
            617: 'MA Belmont, Brookline, Chelsea, Everett, Milton, Quincy, Watertown, Winthrop, and close-in Boston suburbs',
            618: 'IL Carbondale, Alton, Belleville, Cahokia, Centralia, Edwardsville, Marion, Metropolis, Vandalia, and most of southern Illinois',
            619: 'CA San Diego and suburbs',
            620: 'KS southern Kansas not including the Wichita Metropolitan Area',
            621: 'TX Houston',
            622: 'Canadian non-geographic',
            623: 'AZ Phoenix metropolitan area; primarily the West Valley',
            624: 'NY Wester portion:  Buffalo, Niagara Falls, Olean',
            626: 'CA San Gabriel Valley',
            628: 'CA San Francisco',
            629: 'TN Middle Tennessee, including Nashville and surrounding area',
            630: 'IL western suburbs of Chicago, including DuPage, central and southern Kane, northern Kendall, far northern Will, and small portions of Cook counties',
            631: 'NY Suffolk County on Long Island',
            636: 'MO St. Charles, Chesterfield, Union, Troy, and parts of east-central Missouri',
            639: 'Saskatchewan',
            640: 'NJ Trenton, Atlantic City, Princeton, and most of central & southeastern New Jersey',
            641: 'IA Mason City, Oskaloosa, Creston, Pella, Ottumwa, Britt, Clear Lake, Fairfield, and parts of central Iowa',
            645: 'FL Miami-Dade County and the Florida Keys',
            646: 'NY New York City: Manhattan only, except for Marble Hill',
            647: 'Ontario:  Toronto',
            649: 'The Turks and Caicos Islands:  all',
            650: 'CA Daly City, South San Francisco, Palo Alto, Redwood City, Menlo Park, Mountain View, San Mateo, Santa Clara',
            651: 'MN St. Paul, Eagan, Lindstrom, Red Wing, Hastings, Stillwater, and a part of east-central Minnesota',
            656: 'FL all of Hillsborough County, including Tampa and its suburbs, MacDill Air Force Base, and Plant City, and also the inland areas of Pasco County and Oldsmar in Pinellas County',
            657: 'CA Northern Orange County: Anaheim, Fullerton, Garden Grove, Huntington Beach, Orange, Santa Ana, and portions Newport Beach and Costa Mesa',
            658: 'Jamaica',
            659: 'AL Birmingham, Tuscaloosa, and parts of western and central Alabama',
            660: 'MO Sedalia, Kirksville, Maryville, Mexico, Whiteman Air Force Base, and a part of north-central Missouri',
            661: 'CA Northern Los Angeles County, including Lancaster, Palmdale, and Santa Clarita; and most of Kern County, including Bakersfield, Mojave, and Edwards Air Force Base',
            662: 'MS Tupelo, Columbus, Corinth, Greenville, Greenwood, Starkville, and most of northern Mississippi',
            664: 'Montserrat:  all',
            667: 'MD',
            669: 'CA San Jose',
            670: 'was the former country code for the islands',
            671: 'was the former country code for the island',
            672: 'British Columbia, and the isolated border town of Hyder, Alaska, USA',
            678: 'GA Metro Atlanta',
            679: 'a planned overlay of 313, but has not been scheduled',
            680: 'NY Syracuse, Utica, Watertown, and north-central New York',
            681: 'WV',
            682: 'TX Fort Worth area',
            683: 'Ontario:  Northeastern Ontario and Central Ontario: Greater Sudbury, Sault Ste. Marie, North Bay, etc.',
            684: 'American Samoa:  the former country code for this possession and unorganized territory of the United States',
            686: 'VA the Richmond Metropolitan Area, including Petersburg and the Northern Neck and Middle Peninsula',
            689: 'FL Orlando, Sanford, St. Cloud, Kissimmee, and a part of east-central Florida',
            700: 'Implemented for carrier internal use 1984',
            701: 'ND all',
            702: 'NV almost all of Clark County, including all of the Las Vegas Valley, including Henderson and Boulder City',
            703: 'VA Northern Virginia: mostly the suburbs of Washington, D.C., including Alexandria, Arlington County, Fairfax County, Prince William County, and eastern Loudoun County',
            704: 'NC Charlotte, Concord, Gastonia, Salisbury, and much of south-central North Carolina',
            705: 'Ontario:  Northeastern Ontario and Central Ontario: Greater Sudbury, Sault Ste. Marie, North Bay, etc.',
            706: 'GA Athens, Augusta, Columbus, Calhoun, Dalton, Rome, and much of northwestern, northeastern and eastern Georgia, with an exclave in midwestern Georgia',
            707: 'CA Vallejo, Crescent City, Eureka, Redwoods National Park, Santa Rosa, Ukiah, and most of northwestern California',
            708: 'IL western and southern portions of suburban Cook County and far eastern sections of Will Count',
            709: 'Newfoundland and Labrador:  all',
            710: 'US Government special services',
            711: 'Not assignable; N11 code for telecommunications device for the deaf',
            712: 'IA Sioux City, Council Bluffs, Denison, and most of western Iowa',
            713: 'and 281 were later merged into an overlay',
            714: 'CA Northern Orange County: Anaheim, Fullerton, Garden Grove, Huntington Beach, Orange, Santa Ana, and portions of Newport Beach, Costa Mesa, and Tustin',
            715: 'WI Wausau, Eau Claire, Rhinelander, and most of northern Wisconsin',
            716: 'NY Buffalo, Niagara Falls, Olean, and parts of western New York',
            717: 'PA Harrisburg, Gettysburg, Lancaster, York, and most of south-central Pennsylvania',
            718: 'NY New York City: The Bronx, Brooklyn, Queens, Staten Island, and Marble Hill',
            719: 'CO Colorado Springs, Pueblo, Florence, Leadville, Limon, Trinidad, La Junta, and most of southeastern Colorado',
            720: 'CO Denver, Boulder, Longmont, Aurora, Golden, Limon, Centennial; central Colorado',
            721: 'Sint Maarten:  all',
            724: "PA Washington, Greensburg, Indiana, New Castle, Uniontown, Butler, and the majority of Southwestern Pennsylvania outside of Pittsburgh's Allegheny County",
            725: 'NV almost all of Clark County, including all of the Las Vegas Valley, including Henderson, and Boulder City',
            726: 'TX San Antonio metropolitan area',
            727: 'FL all of Pinellas County (except Oldsmar which uses area codes 656 and 813',
            728: 'FL Palm Beach County, including Palm Beach, West Palm Beach, Boca Raton, Boynton Beach, etc.',
            730: 'IL Carbondale, Alton, Belleville, Cahokia, Centralia, Edwardsville, Marion, Metropolis, Vandalia, and most of southern Illinois',
            731: 'TN most of West Tennessee, excluding Metropolitan Memphis and Shelby County (area code 901',
            732: 'NJ New Brunswick, Lakewood, Neptune, Fort Dix, and most of east-central New Jersey',
            734: 'MI Ann Arbor, Hell, Monroe, Plymouth, Romulus, Wayne, Ypsilanti, and the southwestern suburbs of Detroit',
            737: 'TX Austin and suburbs',
            738: 'CA nearly the entire city of Los Angeles outside of the San Fernando Valley and smaller cities and unincorporated areas of Los Angeles County immediately to the south or east',
            740: 'OH suburban Columbus, central Ohio outside of Franklin County, excluding the Marysville area, together with southeastern Ohio: Athens, Lancaster, Cambridge, Delaware, Ironton, Marietta, Mt. Vernon, Newark, Portsmouth, Steubenville, Washington Court House, and Zanesville',
            742: 'Ontario:  Niagara Falls Region, Hamilton, St. Catharines, suburbs of the Greater Toronto Area, and southeastern Ontario',
            743: 'NC',
            747: 'CA the San Fernando Valley portion of Los Angeles County, including Burbank, Canoga Park, Encino, Glendale, North Hollywood, Northridge, Panorama City, Reseda, San Fernando, Sylmar, Tarzana, Van Nuys, and Woodland Hills',
            753: 'Ontario:  Ottawa metropolitan area and southeastern Ontario',
            754: 'FL',
            757: 'VA Part of Hampton Roads and the Eastern Shore of Virginia',
            758: 'Saint Lucia:  all',
            760: 'CA most of the desert and mountain portions of the southeastern two-thirds of California',
            762: 'GA',
            763: 'MN Brooklyn Park, Plymouth, Maple Grove, Monticello, Elk River, Fridley, Blaine, and the northwest suburban area of Minneapolis',
            765: 'IN Kokomo, Lafayette, Marion, Muncie, Richmond, West Lafayette, and most of central Indiana excluding Indianapolis and immediate suburbs',
            767: 'Commonwealth of Dominica:  all',
            769: 'MS',
            770: "GA Marietta, Carrollton, Gainesville, Jonesboro, Lawrenceville, Roswell, Stone Mountain, Snellville, Cartersville, and much of north-central Georgia outside of Atlanta's Interstate 285 Perimeter Highway",
            771: 'Washington, D.C.:  all',
            772: 'FL Fort Pierce, Port Saint Lucie, Sebastian, Stuart, Vero Beach, all of Indian River County, and Martin County',
            773: 'IL City of Chicago, excluding downtown',
            774: 'MA Berkley, Dennis, Douglas, Easton, Edgartown, Oakham, Oxford, Upton, and southeastern Massachusetts',
            775: 'NV Carson City, Reno, Elko, Ely, Sparks, Winnemucca, Great Basin National Park, Naval Air Station Fallon, and all of Nevada, except for most of Clark County in southernmost Nevada',
            778: 'British Columbia:  all, and the isolated border town of Hyder, Alaska, USA',
            779: 'IL',
            780: 'Alberta:  Edmonton, Jasper, Grande Prairie, Peace River, and all of northern Alberta',
            781: 'MA Canton, Hanson, Lincoln, Nahant, Plympton, Revere, Stoughton, Winchester, and east-central Massachusetts',
            782: 'Nova Scotia and Prince Edward Island',
            851: 'reserved as a third area code for the region.',
            784: 'Saint Vincent and the Grenadines:  all',
            785: 'KS Topeka, Salina, Colby, Lawrence, Manhattan, and all of northern and central Kansas not including the Kansas City Metropolitan Area',
            786: 'FL Miami-Dade County and the Florida Keys',
            787: 'Puerto Rico',
            800: 'toll-free telephone service',
            801: 'UT Counties of Davis, Morgan, Salt Lake, Utah, and Weber along the Wasatch Front, including the cities of Salt Lake City, Ogden, and Provo',
            802: 'VT all',
            803: 'SC Columbia, Rock Hill, Sumter, Aiken, and most of central South Carolina',
            804: 'VA the Richmond Metropolitan Area, including Petersburg and the Northern Neck and Middle Peninsula',
            805: 'CA Ventura, San Luis Obispo, and Santa Barbara Counties',
            806: 'TX Lubbock, Amarillo, Canadian, Canyon, Dalhart, and the entire Texas Panhandle',
            807: 'Ontario:  Northwestern Ontario: Thunder Bay, Kenora, Dryden, Greenstone',
            808: 'HI all of the Hawaiian Islands to Midway Atoll and major Hawaiian cities including Honolulu, Kailua, Mililani, Haleiwa, Hilo, Kahului, Lihue, etc.; plus Wake Island',
            809: 'Dominican Republic',
            810: 'MI Port Huron, Flint, Lapeer, and the Michigan "Thumb"',
            811: 'Not assignable; N11 code for regional information',
            812: 'IN Southern Indiana, including Bloomington, Evansville, Terre Haute, Columbus, Jeffersonville, Lawrenceburg, Madison, and New Albany',
            813: 'FL all of Hillsborough County, including Tampa and its suburbs, MacDill Air Force Base, and Plant City; and the inland areas of Pasco County and Oldsmar in Pinellas County',
            814: 'PA Erie, State College, Altoona, Clearfield, Emporium, Johnsonburg, Johnstown, Meyersdale, Ridgway, Somerset, and most of northwestern and parts of central Pennsylvania',
            815: 'IL much of northern Illinois outside Chicago and its immediate surrounding suburbs: Rockford and its suburbs, Belvidere, La Salle, Peru, DeKalb, Sycamore, Freeport, Dixon, Sterling, Rock Falls, Ottawa, Morris, Princeton, Mendota, Rochelle, Sandwich, Streator, Pontiac, Kankakee, and some outlying Chicago suburbs such as Harvard, McHenry, Crystal Lake, Woodstock, Plainfield, Joliet, Romeoville, Lockport, New Lenox, Frankfort, Minooka, Channahon, and Shorewood',
            816: 'MO Kansas City, St Joseph, Independence, Harrisonville, and parts of west-central Missouri',
            817: 'TX Fort Worth, Arlington, Grand Prairie, Grandview, Weatherford',
            818: 'CA the San Fernando Valley portion of Los Angeles County, including Burbank, Canoga Park, Encino, Glendale, North Hollywood, Northridge, Panorama City, Reseda, San Fernando, Sylmar, Tarzana, Van Nuys, and Woodland Hills',
            819: 'Quebec:  Western Québec, except Montréal 514 and surrounding area 450: a large area including Abitibi-Témiscamingue, Estrie, Mauricie, Outaouais, Sherbrooke, and Trois-Rivieres',
            820: 'CA Ventura, San Luis Obispo, and Santa Barbara Counties',
            821: 'SC The Upstate, including Greenville, Spartanburg, Anderson, Clemson, and most of northwestern South Carolina',
            825: 'Alberta:  all',
            826: 'VA Fredericksburg, Roanoke, Blacksburg, Harrisonburg, Lexington, Staunton, Winchester, and parts of north-central Virginia',
            828: 'NC Asheville, Franklin, Hickory, Murphy, Waynesville, and parts of western North Carolina',
            829: 'Dominican Republic',
            830: 'TX Del Rio, Kerrville, Eagle Pass, Fredericksburg, New Braunfels, and a part of the Rio Grande Valley',
            831: 'CA Monterey County, including Salinas and Monterey',
            832: 'TX Houston Metropolitan Area and suburbs',
            833: 'toll-free telephone service',
            835: 'PA Chester, Lehigh Valley, Norristown, Reading; parts of southeastern Pennsylvania',
            837: 'CA Redding, Auburn, Chico, Davis, the California shore of Lake Tahoe, Placerville, Susanville, Truckee, Yreka, and most of northeastern California',
            838: 'NY Albany, Schenectady, Plattsburgh, Saranac Lake, Lake George, Westport, and most of northeastern New York',
            839: 'SC',
            840: 'CA southwestern San Bernardino County and a small portion of Los Angeles and Riverside counties, including Fontana, Pomona, Chino Hills, Claremont, Chino, Ontario, and Redlands',
            843: 'SC Charleston, Florence, Hilton Head Island, Myrtle Beach, Charleston Air Force Base, and most of southeastern South Carolina',
            844: 'toll-free telephone service',
            845: 'NY Dutchess, Orange, Putnam, Rockland, Sullivan, and Ulster counties',
            847: 'IL North and northwest suburbs of Chicago, including Lake, northern Cook, northern Kane, and extreme southeastern McHenry Counties; includes Evanston, Skokie, Niles, Park Ridge, Des Plaines, Mount Prospect, Arlington Heights, Palatine, Wheeling, Buffalo Grove, Barrington, Elk Grove Village, Schaumburg, Hoffman Estates, Elgin, Carpentersville, Algonquin, Lake in the Hills, Huntley, Hampshire, Cary, Lake Zurich, Fox Lake, Round Lake Beach, Antioch, Gurnee, Waukegan, Zion, Lake Forest, Vernon Hills, Libertyville, Mundelein, Northbrook, Glenview, Deerfield, Highland Park, Wilmette, Winnetka',
            848: 'NJ New Brunswick, Lakewood, Neptune, Fort Dix, and most of east-central New Jersey',
            849: 'Dominican Republic',
            850: 'FL Northwestern Florida:  Appalachicola, Pensacola, Tallahassee, Quincy, Panama City, Naval Air Station Pensacola, Eglin Air Force Base and all of the Florida Panhandle',
            854: 'SC Charleston, Florence, Hilton Head Island, Myrtle Beach, Charleston Air Force Base, and most of southeastern South Carolina',
            855: 'toll-free telephone service',
            856: 'NJ Cherry Hill, Camden, Millville, Vineland, and most of southwestern New Jersey',
            857: 'MA Belmont, Brookline, Chelsea, Everett, Milton, Quincy, Watertown, Winthrop, and close-in Boston suburbs',
            858: 'CA San Diego and suburbs',
            859: 'KY Lexington, Richmond, Danville, Covington, Florence, and northernmost Kentucky',
            860: 'CT Hartford, Bristol, Norwich, and northern and eastern Connecticut',
            861: 'IL Peoria, Bloomington, Moline, Rock Island, Galesburg; west-central Illinois',
            862: 'NJ',
            863: 'FL Lakeland, Bartow, Sebring, Winter Haven in south central Florida',
            864: 'SC The Upstate, including Greenville, Spartanburg, Anderson, Clemson, and most of northwestern South Carolina',
            865: 'TN Knoxville, Alcoa, Athens, Clinton, Crossville, Dayton, Gatlinburg, Loudon, Maryville, Newport, Oak Ridge, Oliver Springs, Pigeon Forge, Rockwood, Sweetwater, etc., in east Tennessee',
            866: 'toll-free telephone service',
            867: 'the Canadian Territories: Yukon, Northwest Territories, and Nunavut',
            868: 'Trinidad and Tobago:  all',
            869: 'Saint Kitts and Nevis:  all',
            870: 'AR Texarkana, Jonesboro, Pine Bluff, and southern, eastern, and northeastern Arkansas',
            872: 'IL Chicago',
            873: 'Quebec:  Western Québec, except Montréal 514 and surrounding area 450: a large area including Abitibi-Témiscamingue, Estrie, Mauricie, Outaouais, Sherbrooke, and Trois-Rivières',
            876: 'Jamaica',
            877: 'toll-free telephone service',
            878: 'PA Pittsburgh',
            879: 'Newfoundland:  all',
            888: 'toll-free telephone service',
            900: 'premium-rate telephone numbers',
            901: 'TN Memphis, Covington, Germantown, Somerville, and extreme southwestern Tennessee, mostly in Shelby County',
            902: 'Nova Scotia and Prince Edward Island',
            903: 'TX Tyler, Sherman, Longview, Marshall, Palestine, Jacksonville, Carthage, and Northeast Texas',
            904: 'FL Jacksonville, St. Augustine, Starke, and most of northeastern Florida',
            905: 'Ontario:  Niagara Falls Region (including St. Catharines',
            906: 'MI Upper Peninsula: Sault Ste. Marie, Escanaba, Houghton, Iron Mountain, Marquette, Menominee, etc.',
            907: 'AK all, except the lone border town of Hyder which uses the BC, Canada area codes of 236, 250, 672, or 778 depending on its assigned number',
            908: 'NJ Alpha, Washington, Elizabeth, Warren, Plainfield, and west-central New Jersey',
            909: 'CA southwestern San Bernardino County and a small portion of Los Angeles and Riverside Counties, including Fontana, Pomona, Chino Hills, Claremont, Chino, Ontario, and Redlands',
            910: 'NC Fayetteville, Wilmington, Fort Liberty, Seymour Johnson Air Force Base, Jacksonville, Lumberton, and much of southeastern North Carolina',
            911: 'Not assignable; N11 code for emergency services',
            912: 'GA Savannah, Statesboro, Vidalia, Waycross, Brunswick, Douglas, and southeastern Georgia',
            913: 'KS Kansas City, Kansas, Overland Park, Olathe, Lenexa, Leavenworth, Bonner Springs, De Soto, parts of eastern Kansas',
            914: 'NY Westchester County',
            915: 'TX all of El Paso County and portions of Hudspeth County',
            916: 'CA the Sacramento Metropolitan Area',
            917: 'NY New York City: all; mainly cell phones',
            918: 'OK Tulsa, Bartlesville, McAlester, Muskogee, Henryetta, and northeastern Oklahoma',
            919: 'NC the Research Triangle, including Raleigh, the state capital city; Durham, Cary, and Chapel Hill; and Goldsboro and other parts of north-central North Carolina',
            920: 'WI Appleton, Sheboygan, Oshkosh, Green Bay, Manitowoc, Marquette, Fond du Lac, and parts of eastern Wisconsin, but not Milwaukee County',
            924: 'MN Rochester, Mankato, Austin, Marshall, Winona, and most of southern Minnesota',
            925: 'CA inland regions of the East Bay: Livermore, Concord, Pleasant Hill, Walnut Creek, Martinez, Pleasanton, and Dublin, just east of the hills that ring San Francisco Bay',
            928: 'AZ except for Phoenix metropolitan area, Tucson metropolitan area, and some areas west and south of Tucson',
            929: 'NY New York City: The Bronx, Brooklyn, Queens, Staten Island, and Marble Hill',
            930: 'IN Southern Indiana, including Bloomington, Evansville, Terre Haute, Columbus, Jeffersonville, Lawrenceburg, Madison, and New Albany',
            931: 'TN Southern Middle Tennessee',
            934: 'NY Suffolk County on Long Island',
            936: 'TX Nacogdoches, Lufkin, Conroe, Huntsville, Center, and Southeast Texas',
            937: 'OH Dayton, Springfield, and southwestern Ohio north and east of the Cincinnati metropolitan area',
            938: 'AL Huntsville, Anniston, Cullman, Decatur, Florence, Fort Payne, Gadsden, Madison, Sheffield, Tuscumbia',
            939: 'Puerto Rico',
            940: 'TX the area immediately north of the Dallas-Fort Worth metroplex: Denton, Wichita Falls, Decatur, Gainesville, Vernon, etc.',
            941: 'FL Gulf Coast immediately south of Tampa Bay: all of Manatee County, Sarasota County, and Charlotte County; includes Bradenton, Port Charlotte, Sarasota, and Punta Gorda',
            942: 'will overlay 416/647/437:  Toronto metropolitan area',
            943: 'GA Metro Atlanta',
            945: 'TX Dallas-Fort Worth metroplex',
            947: 'MI Oakland County',
            948: 'VA Part of Hampton Roads and the Eastern Shore of Virginia',
            949: 'CA Southern Orange County: Irvine, Lake Forest, Mission Viejo, Corona del Mar, San Clemente, Laguna Beach, Dana Point, San Juan Capistrano, Rancho Santa Margarita, and parts of Newport Beach and Costa Mesa',
            950: 'not assignable as an area code',
            951: 'CA western Riverside County, including Riverside, Corona, California, Lake Elsinore, Mira Loma, Moreno Valley, Sun City, Temecula, Winchester, Lakeview, etc.',
            952: 'MN Bloomington, Eden Prairie, Edina, Minnetonka, Chaska, and the southwest suburban Minneapolis area',
            954: 'FL all of Broward County: Fort Lauderdale, Hollywood, Coral Springs, etc.',
            956: 'TX Laredo, Harlingen, Brownsville, McAllen, and southmost Texas',
            959: 'CT Hartford, Bristol, Norwich, and northern and eastern Connecticut',
            970: 'CO Grand Junction, Aspen, Durango, Estes Park, Fort Collins, Frisco, Glenwood Springs, Greeley, Purgatory, Steamboat Springs, Telluride, Vail, Rocky Mountain National Park, Dinosaur National Monument, and most of north-central, south-central, and western Colorado',
            971: 'OR Portland, Salem, Hillsboro, Beaverton, and most of northwestern Oregon',
            972: 'TX Dallas metropolitan area',
            973: 'NJ Newark, Paterson, and most of northeastern New Jersey',
            975: 'MO Kansas City, St Joseph, Independence, Harrisonville, and parts of west-central Missouri',
            978: 'MA Ashby, Barre, Boxborough, Carlisle, Groveland, Rowley, Wendell, Wenham, and northeastern Massachusetts',
            979: 'TX Wharton, Bryan, Bay City, College Station, Lake Jackson, La Grange, and southeastern Texas',
            980: 'NC',
            983: 'CO Denver',
            984: 'NC',
            985: 'LA Houma, Slidell, and southeastern Louisiana excluding New Orleans',
            986: 'ID',
            988: 'an N11 short code for the Suicide & Crisis Lifeline; not assignable as an area code',
            989: 'MI Alpena, Mt. Pleasant, Bay City, Saginaw, Midland, Owosso, and a part of central Michigan',
        }
        g.lines = [f"{i!s} {j}" for i, j in g.di.items()]
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] regex1 [regex2...]
          Search for areacodes with a regular expression (expressions are
          OR'd together).  All North American codes from 200-999 are present.
        Examples:
            '234' will show the area code is from Ohio.
            '.66' will show area codes with 66 in them.
            'CA' will show California area codes (use the two letter
                 abbreviations for states).
            'N11' will show the N11 codes.
        Options:
            -a      Show all area code data
            -i      Do not ignore case
            -m      Show missing codes
        Information screen-scraped from
        https://en.wikipedia.org/wiki/List_of_North_American_Numbering_Plan_area_codes
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Show all area codes
        d["-i"] = True      # Ignore case
        d["-m"] = False     # Show missing codes
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "aim") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("aim"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
        if d["-a"]:
            for i in g.lines:
                Print(i)
            exit(0)
        if d["-m"]:
            ShowMissing()
            exit(0)
        return args
if 1:   # Core functionality
    def Print(s):
        'Print lines with hanging indent'
        print(HangingIndent(s, indent=" "*4))
    def FindRegex(regex):
        'Given the regex, find lines that match'
        r = re.compile(regex)
        found = []
        for i in g.lines:
            if r.search(i):
                found.append(i)
        return found
    def ShowMissing():
        # Find the numbers not present
        all = set(range(200, 1000))
        have = set(g.di)
        missing = sorted(list(all - have))
        print("Missing area codes:")
        if 0:
            # Print in columns
            for i in Columnize(missing, indent=" "*2):
                print(i)
        else:
            # Collapse into ranges
            items = [missing[0]]
            while missing:
                item = items.pop(0)
                

if __name__ == "__main__":
    d = {}      # Options dictionary
    regexps = ParseCommandLine(d)
    found = []
    for regex in regexps:
        found.extend(FindRegex(regex))
    for i in sorted(set(found)):
        Print(i)
