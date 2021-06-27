if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Translation of old C code program for areacodes
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    import getopt
    from collections import defaultdict
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    import states
if 1:   # Global variables
    # NOTE:  it would probably make sense to rewrite this to use the
    # data from
    # https://en.wikipedia.org/wiki/List_of_North_American_Numbering_Plan_area_codes
    
    # Original data from ac.c; unattributed.  I likely found this on the
    # web in the early-to-mid 1990's while working in the controller
    # section and wrote it as a C application.
    olddata = '''
        # ';' separated fields:
        #
        # Fields are:
        #   AreaCode
        #   StateAbbrev
        #   State
        #   DescriptionOfMajorAreas
        #   TimeZoneNumber
        #
        201;NJ;New Jersey;Hackensack, Jersey City and northeast New Jersey;6
        202;DC;District of Columbia;all of Washington, DC;6
        203;CT;Connecticut;Fairfield, Bridgeport, New Haven, Stamford and sw Connecticut;6
        204;MB;Manitoba;all of Manitoba;5
        205;AL;Alabama;Birmingham and northern Alabama;5
        206;WA;Washington;Seattle area;12
        207;ME;Maine;all of Maine;6
        208;ID;Idaho;all of Idaho;9
        209;CA;California;Stockton, Fresno, Modesto and central California;12
        210;TX;Texas;San Antonio area;5
        212;NY;New York;Manhattan area, overlays with 646;6
        213;CA;California;Downtown Los Angeles area only;12
        214;TX;Texas;Dallas area, overlays with 469 and 972;5
        215;PA;Pennsylvania;Philadelphia only, overlays with 267;6
        216;OH;Ohio;Cleveland and northeastern Ohio;6
        217;IL;Illinois;Champaign, Urbana, Springfield and central Illinois;5
        218;MN;Minnesota;Duluth and northern Minnesota;5
        219;IN;Indiana;Gary, Hammond, Michigan City, South Bend and northern Indiana;2
        224;IL;Illinois;Extreme ne Illinois and nw Chicago suburbs, overlays with 847;5
        225;LA;Louisiana;Baton Rouge and central eastern Louisiana;5
        228;MS;Mississippi;Gulfport, Biloxi and extreme southern Mississippi;5
        231;MI;Michigan;Traverse City, Muskegon and northwestern Michigan;6
        240;MD;Maryland;Hagerstown, Rockville and western Maryland, overlays with 301;6
        248;MI;Michigan;Oakland County only, including Pontiac, Southfield, Rochester Hills;6
        250;BC;British Columbia;all except Vancouver area;9
        252;NC;North Carolina;northeastern North Carolina including Rocky Mount;6
        253;WA;Washington;Tacoma and south Seattle suburbs including Auburn;12
        254;TX;Texas;north central Texas including Waco;5
        256;AL;Alabama;Huntsville and northern Alabama surrounding and excluding Birmingham;5
        262;WI;Wisconsin;Menomonee Falls, Waukesha, Racine and southeastern Wisconsin;5
        267;PA;Pennsylvania;Philadelphia only, overlays with 215;6
        270;KY;Kentucky;Paducah, Bowling Green and western Kentucky;5
        281;TX;Texas;Houston area, overlays with 713 and 832;5
        301;MD;Maryland;Hagerstown, Rockville and western Maryland, overlays with 240;6
        302;DE;Delaware;all of Delaware;6
        303;CO;Colorado;Boulder, Longmont, Aurora, Denver areas, overlays with 720;10
        304;WV;West Virginia;all of West Virginia;6
        305;FL;Florida;Miami, Key West and southeastern Florida, overlays with 786;6
        306;SK;Saskatchewan;all of Saskatchewan;4
        307;WY;Wyoming;all of Wyoming;10
        308;NE;Nebraska;North Platte, Scottsbluff and western Nebraska;4
        309;IL;Illinois;Peoria, Rock Island and central western Illinois;5
        310;CA;California;Malibu, Torrance, Beverley Hills, West LA suburbs, overlays with 424;12
        312;IL;Illinois;downtown central Chicago area;5
        313;MI;Michigan;Dearborn, Detroit and inner Detroit suburbs;6
        314;MO;Missouri;St Louis and northern, central and southern St Louis suburbs;5
        315;NY;New York;Syracuse and northwestern New York;6
        316;KS;Kansas;Dodge City, Wichita and southern Kansas;3
        317;IN;Indiana;Indianapolis area;6
        318;LA;Louisiana;Shreveport, Monroe, Alexandria and northern Louisiana;5
        319;IA;Iowa;Davenport, Dubuque and eastern Iowa;5
        320;MN;Minnesota;St Cloud and central Minnesota excluding Minneapolis/St Paul;5
        321;FL;Florida;Orlando and central eastern Florida, overlays with 407;6
        323;CA;California;Los Angeles excluding downtown Los Angeles;12
        330;OH;Ohio;northeastern Ohio except Cleveland;6
        334;AL;Alabama;Mobile, Montgomery and southern Alabama;5
        336;NC;North Carolina;Winston-Salem, Greensboro and northwest North Carolina;6
        337;LA;Louisiana;Leesville, Lake Charles, Lafayette and southwestern Louisiana;5
        340;US;VIRGIN ISLANDS;all of the US Virgin Islands;1
        341;CA;California;Berkeley, Oakland and Fremont areas, overlays with 510;12
        347;NY;New York;Brooklyn, Staten Island, Bronx and Queens, overlays with 718;6
        352;FL;Florida;Gainesville and central Florida;6
        360;WA;Washington;western Washington except Seattle and surrounding areas;12
        361;TX;Texas;Corpus Christi and southeastern Texas;5
        401;RI;Rhode Island;all of Rhode Island;6
        402;NE;Nebraska;Lincoln, Omaha and eastern Nebraska;5
        403;AB;Alberta;Calgary, Banff, Red Deer, Medicine Hat, Lethbridge and s Alberta;10
        404;GA;Georgia;central Atlanta area, overlays with 678;6
        405;OK;Oklahoma;Oklahoma City and central Oklahoma;5
        406;MT;Montana;all of Montana;10
        407;FL;Florida;Orlando and central eastern Florida, overlays with 321;6
        408;CA;California;San Jose, Milpitas, Sunnyvale, Cupertino, overlays with 669;12
        409;TX;Texas;Beaumont and southeastern Texas except Houston;5
        410;MD;Maryland;Annapolis, Baltimore and eastern Maryland, overlays with 443;6
        412;PA;Pennsylvania;Pittsburgh area only;6
        413;MA;Massachusetts;Pittsfield, Springfield and western Massachusetts;6
        414;WI;Wisconsin;Milwaukee, Greenfield, Oak Creek and Milwaukee suburbs;5
        415;CA;California;San Francisco and bay area, overlays with 628;12
        416;ON;Ontario;Toronto area;6
        417;MO;Missouri;Joplin, Springfield and southwestern Missouri;5
        418;PQ;Quebec;Quebec and eastern Quebec;6
        419;OH;Ohio;Toledo and northwestern Ohio;6
        423;TN;Tennessee;Chattanooga, Johnson City and southern and eastern Tennessee;2
        424;CA;California;West LA suburbs including Malibu and Torrance, overlays with 310;12
        425;WA;Washington;north Seattle suburbs including Everett;12
        435;UT;Utah;all of Utah excluding Salt Lake City, Ogden and Provo areas;10
        440;OH;Ohio;northeastern Ohio excluding Cleveland;6
        442;CA;California;Barstow, Palm Springs and southeastern California, overlays with 760;12
        443;MD;Maryland;Annapolis, Baltimore and eastern Maryland, overlays with 410;6
        450;PQ;Quebec;central southern Quebec excluding Montreal;6
        469;TX;Texas;Dallas area, overlays with 214 and 972;5
        473;GR;Grenada;all of Grenada;1
        480;AZ;Arizona;Eastern Phoenix area and eastern Phoenix suburbs only;10
        484;PA;Pennsylvania;southeastern Pennsylvania, overlays with 610;6
        501;AR;Arkansas;Little Rock, Fayetteville and northwestern Arkansas;5
        502;KY;Kentucky;Louisville, Frankfort, Shelbyville and north central Kentucky;6
        503;OR;Oregon;Portland, Salem and northwestern Oregon, overlays with 971;12
        504;LA;Louisiana;New Orleans and southeastern Louisiana;5
        505;NM;New Mexico;all of New Mexico;10
        506;NB;New Brunswick;all of New Brunswick;1
        507;MN;Minnesota;Rochester and southern Minnesota;5
        508;MA;Massachusetts;Worcester, New Bedford, Fall River and southern Massachusetts;6
        509;WA;Washington;Spokane and eastern Washington;12
        510;CA;California;Berkeley, Oakland and Fremont areas, overlays with 341;12
        512;TX;Texas;Austin and central southern Texas;5
        513;OH;Ohio;Cincinnati area;6
        514;PQ;Quebec;Montreal area;6
        515;IA;Iowa;Des Moines and central Iowa;5
        516;NY;New York;Nassau County, Levittown, Hicksville, Massapequa and w Long Island;6
        517;MI;Michigan;Bay City, Jackson, Lansing and central Michigan;6
        518;NY;New York;northeastern New York;6
        519;ON;Ontario;London and southwestern Ontario;6
        520;AZ;Arizona;all of Arizona except the Phoenix area;10
        530;CA;California;Chico, Redding and northeastern California excluding Sacramento;12
        540;VA;Virginia;Roanoke and western and northern Virginia excluding Arlington;6
        541;OR;Oregon;all of Oregon except Portland and Salem areas;9
        559;CA;California;Fresno and central California;12
        561;FL;Florida;West Palm Beach, Boca Raton and central eastern Florida;6
        562;CA;California;Long Beach area;12
        570;PA;Pennsylvania;Scranton and northeastern Pennsylvania;6
        571;VA;Virginia;Washington DC suburbs and Arlington area, overlays with 703;6
        573;MO;Missouri;Jefferson City, Columbia and eastern Missouri excluding St Louis;5
        580;OK;Oklahoma;southern and western Oklahoma;5
        586;MI;Michigan;Flint, Flushing, Warren and southeastern Michigan, overlays with 810;6
        601;MS;Mississippi;Jackson, Meridian and central Mississippi;5
        602;AZ;Arizona;Central Phoenix only;10
        603;NH;New Hampshire;all of New Hampshire;6
        604;BC;British Columbia;Vancouver area;12
        605;SD;South Dakota;all of South Dakota;4
        606;KY;Kentucky;Covington, Ashland, Winchester and eastern Kentucky;6
        607;NY;New York;Binghamton and central southern New York;6
        608;WI;Wisconsin;Madison and southwestern Wisconsin;5
        609;NJ;New Jersey;Atlantic City, Trenton, and central & southeastern New Jersey;6
        610;PA;Pennsylvania;southeastern Pennsylvania excluding Philadelphia, overlays with 484;6
        612;MN;Minnesota;Minneapolis and western suburbs;5
        613;ON;Ontario;Ottawa and southeastern Ontario;6
        614;OH;Ohio;Columbus and surrounding area;6
        615;TN;Tennessee;Nashville area;5
        616;MI;Michigan;Battle Creek, Grand Rapids, Kalamazoo and southwestern Michigan;6
        617;MA;Massachusetts;central Boston;6
        618;IL;Illinois;Alton, Centralia, Mount Vernon and southern Illinois;5
        619;CA;California;Central San Diego;12
        623;AZ;Arizona;Western Phoenix area and western Phoenix suburbs only;10
        626;CA;California;Pasadena Area;12
        628;CA;California;San Francisco and bay area, overlays with 415;12
        630;IL;Illinois;central Chicago suburbs;5
        631;NY;New York;Huntington, Lindenhurst, Islip, Deer Park and Eastern Long Island;6
        636;MO;Missouri;W St Louis suburbs, Warren, St Charles, Franklin & Jefferson counties;5
        646;NY;New York;Manhattan area, overlays with 212;6
        650;CA;California;San Mateo, Palo Alto and s San Francisco suburbs, overlays with 764;12
        651;MN;Minnesota;Saint Paul and eastern suburbs;5
        657;CA;California;northern Orange County including Santa Ana, overlays with 714;12
        660;MO;Missouri;Marshall and northern Missouri excluding Kansas City and St Joseph;5
        661;CA;California;Bakersfield and south central California;12
        662;MS;Mississippi;Greenville, Tupelo and northern Mississippi;5
        669;CA;California;San Jose, Milpitas, Sunnyvale, Cupertino, overlays with 408;12
        678;GA;Georgia;Atlanta area, overlays 404 and 770;6
        701;ND;North Dakota;all of North Dakota;8
        702;NV;Nevada;Las Vegas and extreme southern Nevada;12
        703;VA;Virginia;Washington DC suburbs and Arlington area, overlays with 571;6
        704;NC;North Carolina;Charlotte and south central North Carolina;6
        705;ON;Ontario;North Bay and northeastern Ontario;6
        706;GA;Georgia;Augusta, Columbus, Rome and northern Georgia except Atlanta;6
        707;CA;California;Santa Rosa, Eureka and northwestern California;12
        708;IL;Illinois;southern Chicago suburbs;5
        709;NF;Newfoundland;all of Newfoundland;11
        712;IA;Iowa;Council Bluffs, Sioux City and western Iowa;5
        713;TX;Texas;Houston area, overlays with 281 and 832;5
        714;CA;California;Anaheim, Santa Ana and northern Orange County, overlays with 657;12
        715;WI;Wisconsin;northern Wisconsin;5
        716;NY;New York;Buffalo and western New York;6
        717;PA;Pennsylvania;Harrisburg and south central Pennsylvania;6
        718;NY;New York;Brooklyn, Staten Island, Bronx and Queens, overlays with 347;6
        719;CO;Colorado;Leadville, Pueblo, Colorado Springs and southeastern Colorado;10
        720;CO;Colorado;Denver area, overlays with 303;10
        724;PA;Pennsylvania;western Pennsylvania excluding Pittsburgh;6
        727;FL;Florida;Clearwater and the w c Florida coast, Pinellas and wPasco counties;6
        732;NJ;New Jersey;New Brunswick, Piscataway, & Middlesex, Monmouth and Ocean counties;6
        734;MI;Michigan;Ann Arbor, Livonia, Wayne, Ypsilanti and Detroit outer suburbs;6
        740;OH;Ohio;southeastern Ohio excluding Columbus;6
        752;CA;California;Ontario, Pomona, Chino and San Bernardino areas, overlays with 909;12
        757;VA;Virginia;Hampton, Norfolk and southeastern Virginia;6
        758;ST;LUCIA;all of St Lucia;1
        760;CA;California;Barstow, Palm Springs and southeastern California, overlays with 442;12
        764;CA;California;San Mateo, Palo Alto and s San Francisco suburbs, overlays with 650;12
        765;IN;Indiana;Kokomo and central Indiana excluding Indianapolis;6
        770;GA;Georgia;Marietta, Norcross, Atlanta area except c Atlanta, overlays with 678;6
        773;IL;Illinois;Chicago area excluding downtown Chicago;5
        775;NV;Nevada;All of Nevada, excluding Las Vegas and extreme southern Nevada;12
        780;AB;Alberta;Edmonton, Jasper, Grande Prairie, Peace River and northern Alberta;10
        781;MA;Massachusetts;Waltham, Lexington and Boston suburbs;6
        784;ST;Vincent and the Grenadines;all of St Vincent and the Grenadines;1
        785;KS;Kansas;Topeka, Lawrence and northern Kansas excluding the Kansas City area;8
        786;FL;Florida;Miami and southeastern Florida, overlays with 305;6
        801;UT;Utah;Salt Lake City, Ogden, and Provo areas;10
        802;VT;Vermont;all of Vermont;6
        803;SC;South Carolina;central South Carolina including Columbia;6
        804;VA;Virginia;Richmond, Lynchburg and central Virginia;6
        805;CA;California;Santa Barbara, Bakersfield and central western California;12
        806;TX;Texas;Amarillo and northern Texas;5
        807;ON;Ontario;Thunder Bay and western Ontario;2
        808;HI;Hawaii;all of Hawaii;7
        810;MI;Michigan;Flint, Flushing, Warren and southeastern Michigan, overlays with 586;6
        812;IN;Indiana;Evansville and southern Indiana;2
        813;FL;Florida;Tampa, Hillsborough and East Pasco counties;6
        814;PA;Pennsylvania;Altoona and central and northwestern Pennsylvania;6
        815;IL;Illinois;La Salle, Rockford and northern Illinois except Chicago;5
        816;MO;Missouri;Kansas City and St Joseph area;5
        817;TX;Texas;Fort Worth and Arlington;5
        818;CA;California;Burbank and Glendale areas;12
        819;PQ;Quebec;Western Quebec;6
        828;NC;North Carolina;western North Carolina including Asheville;6
        830;TX;Texas;Uvalde, New Braunfels, Kerrville and southwest Texas;5
        831;CA;California;Monterey, Santa Cruz and c w California excl San Jose;12
        832;TX;Texas;Houston area, overlays with 281 and 713;5
        843;SC;South Carolina;coastal South Carolina including Charleston and Florence;6
        847;IL;Illinois;Northeastern Illinois and nw Chicago suburbs, overlays with 224;5
        850;FL;Florida;northwestern Florida including Pensacola and Tallahassee;2
        856;NJ;New Jersey;Vineland, Camden, Millville, and southwestern New Jersey;6
        858;CA;California;Southwestern California, including northern San Diego and Del Mar;12
        860;CT;Connecticut;Hartford and north and east Connecticut;6
        863;FL;Florida;Lakeland, Bartow, Sebring and south central Florida;6
        864;SC;South Carolina;Greenville and western South Carolina;6
        865;TN;Tennessee;Knoxville, Jefferson City, Oak Ridge and east central Tennessee;6
        867;YK;Yukon and Northwest Territories;Yukon and Northwest Territories;13
        870;AR;Arkansas;All of Arkansas excluding Little Rock and northwestern Arkansas;5
        901;TN;Tennessee;Memphis and western Tennessee;5
        902;NS;Nova Scotia;all of Nova Scotia and Prince Edward Island;1
        903;TX;Texas;Tyler and northeastern Texas;5
        904;FL;Florida;Jacksonville, Daytona and northeastern Florida;6
        905;ON;Ontario;Hamilton and central southeastern Ontario;6
        906;MI;Michigan;Marquette, Sault Ste Marie, Escanaba and upper Michigan;2
        907;AK;Alaska;all of Alaska;0
        908;NJ;New Jersey;Elizabeth, Warren, Plainfield and northwest New Jersey;6
        909;CA;California;Ontario, Pomona, Chino and San Bernardino areas, overlays with 752;12
        910;NC;North Carolina;Fayetteville and southeastern North Carolina;6
        912;GA;Georgia;Albany, Savannah and southern Georgia;6
        913;KS;Kansas;Extreme Eastern Kansas and the Kansas City area;5
        914;NY;New York;Albany and southeastern New York except New York City;6
        915;TX;Texas;El Paso and western Texas;8
        916;CA;California;Sacramento area;12
        917;NY;New York;Brooklyn, Staten Island, Bronx, Queens;6
        918;OK;Oklahoma;Tulsa and northeastern Oklahoma;5
        919;NC;North Carolina;Raleigh and northeast central North Carolina;6
        920;WI;Wisconsin;southeastern Wisconsin excluding the Milwaukee area;5
        925;CA;California;Martinez, Concord, Livermore, Walnut Creek and Dublin areas;12
        931;TN;Tennessee;central Tennessee excluding the Nashville area;5
        935;CA;California;Extreme southwestern California, including southern San Diego;12
        937;OH;Ohio;southwestern Ohio excluding Cincinnati;6
        940;TX;Texas;north central Texas including Wichita Falls and Denton;5
        941;FL;Florida;Fort Myers, Bradenton, Sarasota and southwestern Florida;6
        949;CA;California;Anaheim, Irvine, Costa Mesa and southern Orange County;12
        951;CA;California;Temecula, Riverside, Hemet, San Jacinto, Sun City and Corona areas;12
        954;FL;Florida;Fort Lauderdale area;6
        956;TX;Texas;Laredo, Brownsville, McAllen and southern Texas;5
        970;CO;Colorado;Aspen, Durango, Grand Junction and northern and western Colorado;10
        971;OR;Oregon;Portland, Salem and northwestern Oregon, overlays with 503;12
        972;TX;Texas;Dallas area, overlays with 214 and 469;5
        973;NJ;New Jersey;Newark, Paterson & Morris, Sussex and Essex counties;6
        978;MA;Massachusetts;Lowell, Salem and northern Massachusetts;6
    
        # Other non-US locations
        242;other;Bahamas;1
        246;other;Barbados;1
        264;other;Anguilla;1
        268;other;Antigua and Barbuda;1
        284;other;British Virgin Islands;1
        311;other;Non-emergency access;15
        345;other;Cayman Islands;6
        411;other;Local directory assistance;15
        441;other;Bermuda;1
        456;other;International inbound;15
        500;other;Personal communications services;15
        900;other;900 services;15
        600;other;Canada/Services;15
        611;other;Repair service;15
        649;other;Turks & Caicos;6
        664;other;Montserrat;1
        670;other;Northern Mariana Islands;14
        671;other;Guam;14
        700;other;IC services;15
        710;other;US Government;15
        711;other;TRS accesS;15
        767;other;Dominica;1
        787;other;Puerto Rico;1
        800;other;800 services;15
        809;other;Dominican Republic;1
        811;other;Business office;15
        868;other;Trinidad and Tobago;1
        869;other;St Kitts and Nevis;1
        876;other;Jamaica;6
        877;other;800 services;15
        880;other;Paid 800 service;15
        881;other;Paid 888 service;15
        882;other;Paid 877 service;15
        888;other;800 services;15
        911;other;Emergency;15
    '''
    timezones = {
        0 : "Aleutian & Alaskans",
        1 : "Atlantic",
        2 : "Central & Eastern",
        3 : "Central & Mountain",
        4 : "Central & Mountain",
        5 : "Central",
        6 : "Eastern",
        7 : "Hawaiian",
        8 : "Mountain & Central",
        9 : "Mountain & Pacific",
        10 : "Mountain",
        11 : "Newfoundland",
        12 : "Pacific",
        13 : "Pacific through the Atlantic",
        14 : "Pacific Guam",
        15 : "None",
    }

    # From https://area-codes.org/areacode.htm downloaded 27 Jun 2021
    # Fields are separated by ';'
    # Fields:
    #   Area Code
    #   State
    #   Area/City
    #   Country
    #   In Service Date
    #   Time Zone
    #   Prior Code
    newdata = '''
        201;New Jersey;Hackensack;United States;01/01/1947;E; 
        202;District of Columbia;Washington;United States;01/01/1947;E; 
        203;Connecticut;New Haven;United States;01/01/1947;E; 
        204;Manitoba;;Canada;01/01/1947;C; 
        205;Alabama;Birmingham;United States;01/01/1947;C; 
        206;Washington;Seattle;United States;01/01/1947;P; 
        207;Maine;;United States;01/01/1947;E; 
        208;Idaho;;United States;01/01/1947;M, P; 
        209;California;Modesto;United States;01/01/1958;P;916
        210;Texas;San Antonio;United States;11/01/1992;C;512
        212;New York;New York City;United States;01/01/1947;E; 
        213;California;Los Angeles;United States;01/01/1947;P; 
        214;Texas;Dallas;United States;01/01/1947;C; 
        215;Pennsylvania;Philadelphia;United States;01/01/1947;E; 
        216;Ohio;Cleveland;United States;01/01/1947;E; 
        217;Illinois;Springfield;United States;01/01/1947;C; 
        218;Minnesota;Duluth;United States;01/01/1947;C; 
        219;Indiana;Gary;United States;01/01/1947;E, C; 
        224;Illinois;Waukegan;United States;01/05/2002;C;847
        225;Louisiana;Baton Rouge;United States;08/17/1998;C;504
        226;Ontario;London;Canada;10/21/2006;E;519
        228;Mississippi;Biloxi;United States;09/15/1997;C;601
        229;Georgia;Albany;United States;08/01/2000;E;912
        231;Michigan;Traverse City;United States;06/05/1999;E;616
        234;Ohio;Akron;United States;10/30/2000;E;330
        239;Florida;Fort Myers;United States;03/11/2002;E;941
        240;Maryland;Bethesda;United States;06/01/1997;E;301
        242;Bahamas;;Bahamas;10/01/1996;E;809
        246;Barbados;;Barbados;07/01/1996;A;809
        248;Michigan;Pontiac;United States;05/10/1997;E;810
        249;Ontario;Sault Ste Marie;Canada;03/19/2011;E;705
        250;British Columbia;Prince Rupert;Canada;10/19/1996;P;604
        251;Alabama;Mobile;United States;06/18/2001;C;334
        252;North Carolina;Rocky Mount;United States;03/22/1998;E;919
        253;Washington;Tacoma;United States;04/27/1997;P;206
        254;Texas;Waco;United States;05/25/1997;C;817
        256;Alabama;Huntsville;United States;03/23/1998;C;205
        260;Indiana;Fort Wayne;United States;01/15/2002;E;219
        262;Wisconsin;Racine;United States;09/25/1999;C;414
        264;Anguilla;;United Kingdom;03/31/1997;A;809
        267;Pennsylvania;Philadelphia;United States;07/01/1999;E;215
        268;Antigua and Barbuda;;Antigua and Barbuda;04/01/1996;A;809
        269;Michigan;Battle Creek;United States;07/13/2002;E;616
        270;Kentucky;Bowling Green;United States;04/19/1999;E, C;502
        276;Virginia;Abington;United States;09/01/2001;E;540
        281;Texas;Houston;United States;11/02/1996;C;713
        284;British Virgin Islands;;United Kingdom;10/01/1997;A;809
        289;Ontario;Hamilton;Canada;06/09/2001;E;905
        301;Maryland;Cumberland;United States;01/01/1947;E; 
        302;Delaware;;United States;01/01/1947;E; 
        303;Colorado;Denver;United States;01/01/1947;M; 
        304;West Virginia;;United States;01/01/1947;E; 
        305;Florida;Key West;United States;01/01/1947;E; 
        306;Saskatchewan;;Canada;01/01/1947;C; 
        307;Wyoming;;United States;01/01/1947;M; 
        308;Nebraska;North Platte;United States;01/01/1955;C, M; 
        309;Illinois;Peoria;United States;01/01/1957;C; 
        310;California;Malibu;United States;11/02/1991;P;213
        312;Illinois;Chicago;United States;01/01/1947;C; 
        313;Michigan;Detroit;United States;01/01/1947;E; 
        314;Missouri;Saint Louis;United States;01/01/1947;C; 
        315;New York;Syracuse;United States;01/01/1947;E; 
        316;Kansas;Wichita;United States;01/01/1947;C; 
        317;Indiana;Indianapolis;United States;01/01/1947;E; 
        318;Louisiana;Shreveport;United States;01/01/1957;C; 
        319;Iowa;Cedar Rapids;United States;01/01/1947;C; 
        320;Minnesota;Saint Cloud;United States;03/17/1996;C;612
        321;Florida;Orlando;United States;11/01/1999;E;407
        323;California;Florence;United States;06/13/1998;P;213
        325;Texas;San Angelo;United States;04/05/2003;C;915
        330;Ohio;Akron;United States;03/09/1996;E;216
        331;Illinois;Aurora;United States;10/07/2007;C;630
        334;Alabama;Montgomery;United States;01/15/1995;C;205
        336;North Carolina;Winston Salem;United States;12/15/1997;E;910
        337;Louisiana;Lake Charles;United States;10/11/1999;C;318
        339;Massachusetts;Waltham;United States;05/02/2001;E;781
        340;United States;Virgin Islands;United States;06/01/1997;A;809
        343;Ontario;Ottawa;Canada;05/17/2010;E;613
        345;Cayman Islands;;United Kingdom;09/01/1996;E;809
        347;New York;New York City;United States;10/01/1999;E;718
        351;Massachusetts;Salem;United States;05/02/2001;E;978
        352;Florida;Gainesville;United States;12/03/1995;E;904
        360;Washington;Olympia;United States;01/15/1995;P;206
        361;Texas;Corpus Christi;United States;02/13/1999;C;512
        385;Utah;Salt Lake City;United States;03/29/2009;M;801
        386;Florida;Daytona Beach;United States;02/15/2001;E;904
        401;Rhode Island;;United States;01/01/1947;E; 
        402;Nebraska;Lincoln;United States;01/01/1947;C; 
        403;Alberta;Calgary;Canada;01/01/1947;M; 
        404;Georgia;Atlanta;United States;01/01/1947;E; 
        405;Oklahoma;Oklahoma City;United States;01/01/1947;C; 
        406;Montana;;United States;01/01/1947;M; 
        407;Florida;Orlando;United States;04/16/1988;E;305
        408;California;San Jose;United States;01/01/1959;P;415
        409;Texas;Galveston;United States;11/01/1982;C;713
        410;Maryland;Annapolis;United States;10/06/1991;E;301
        412;Pennsylvania;Pittsburgh;United States;01/01/1947;E; 
        413;Massachusetts;Springfield;United States;01/01/1947;E; 
        414;Wisconsin;Milwaukee;United States;01/01/1947;C; 
        415;California;San Francisco;United States;01/01/1947;P; 
        416;Ontario;Toronto;Canada;01/01/1947;E; 
        417;Missouri;Springfield;United States;01/01/1950;C; 
        418;Quebec;Quebec;Canada;01/01/1947;E; 
        419;Ohio;Toledo;United States;01/01/1947;E; 
        423;Tennessee;Chattanooga;United States;09/11/1995;E, C;615
        424;California;Santa Monica;United States;08/26/2006;P;310
        425;Washington;Everett;United States;04/27/1997;P;206
        430;Texas;Tyler;United States;02/15/2003;C;903
        432;Texas;Midland;United States;04/05/2003;C;915
        434;Virginia;Lynchburg;United States;06/01/2001;E;804
        435;Utah;Cedar City;United States;09/21/1997;M;801
        438;Quebec;Montreal;Canada;11/04/2006;E;514
        440;Ohio;Ashtabula;United States;08/16/1997;E;216
        441;Bermuda;;United Kingdom;10/01/1995;A;809
        442;California;Escondido;United States;11/21/2009;P;760
        443;Maryland;Baltimore;United States;06/01/1997;E;410
        450;Quebec;Saint Lambert;Canada;06/13/1998;E;514
        458;Oregon;Eugene;United States;02/10/2010;P;541
        469;Texas;Dallas;United States;07/01/1999;C;214
        470;Georgia;Atlanta;United States;02/26/2010;E;678
        473;Grenada;;Grenada;10/31/1997;A;809
        475;Connecticut;Bridgeport;United States;12/12/2009;E;203
        478;Georgia;Macon;United States;08/01/2000;E;912
        479;Arkansas;Fort Smith;United States;01/19/2002;C;501
        480;Arizona;Tempe;United States;03/01/1999;M;602
        484;Pennsylvania;Allentown;United States;06/05/1999;E;610
        501;Arkansas;Little Rock;United States;01/01/1947;C; 
        502;Kentucky;Frankfort;United States;01/01/1947;E; 
        503;Oregon;Astoria;United States;01/01/1947;P; 
        504;Louisiana;New Orleans;United States;01/01/1947;C; 
        505;New Mexico;;United States;01/01/1947;M; 
        506;New Brunswick;;Canada;01/01/1955;A; 
        507;Minnesota;Rochester;United States;01/01/1954;C; 
        508;Massachusetts;Brockton;United States;07/16/1988;E;617
        509;Washington;Spokane;United States;01/01/1957;P; 
        510;California;Oakland;United States;09/02/1991;P;415
        512;Texas;Austin;United States;01/01/1947;C; 
        513;Ohio;Cincinnati;United States;01/01/1947;E; 
        514;Quebec;Montreal;Canada;01/01/1947;E; 
        515;Iowa;Des Moines;United States;01/01/1947;C; 
        516;New York;Hempstead;United States;01/01/1951;E; 
        517;Michigan;Lansing;United States;01/01/1947;E; 
        518;New York;Albany;United States;01/01/1947;E; 
        519;Ontario;London;Canada;01/01/1953;E; 
        520;Arizona;Tucson;United States;03/19/1995;M;602
        530;California;Chico;United States;11/01/1997;P;916
        534;Wisconsin;Eau Claire;United States;08/14/2010;C;715
        539;Oklahoma;Tulsa;United States;04/01/2011;C;918
        540;Virginia;Harrisonburg;United States;07/15/1995;E;703
        541;Oregon;Medford;United States;11/05/1995;M, P;503
        551;New Jersey;Hackensack;United States;12/29/2001;E;201
        559;California;Fresno;United States;11/14/1998;P;209
        561;Florida;West Palm Beach;United States;05/13/1996;E;407
        562;California;Long Beach;United States;01/25/1997;P;310
        563;Iowa;Dubuque;United States;03/25/2001;C;319
        567;Ohio;Toledo;United States;01/01/2002;E;419
        570;Pennsylvania;Scranton;United States;12/05/1998;E;717
        571;Virginia;Arlington;United States;03/01/2000;E;703
        573;Missouri;Jefferson City;United States;01/07/1996;C;314
        574;Indiana;South Bend;United States;01/15/2002;E;219
        575;New Mexico;Las Cruces;United States;10/07/2007;M;505
        579;Quebec;Terrebone;Canada;08/21/2010;E;450
        580;Oklahoma;Lawton;United States;11/01/1997;C;405
        581;Quebec;Quebec City;Canada;09/19/2008;E;418
        585;New York;Rochester;United States;11/15/2001;E;716
        586;Michigan;Port Huron;United States;09/22/2001;E;810
        587;Alberta;Calgary;Canada;09/19/2008;M;780
        600;Canadian Services;;Canada;01/01/1993;; 
        601;Mississippi;Jackson;United States;01/01/1947;C; 
        602;Arizona;Phoenix;United States;01/01/1947;M; 
        603;New Hampshire;;United States;01/01/1947;E; 
        604;British Columbia;Vancouver;Canada;01/01/1947;P; 
        605;South Dakota;;United States;01/01/1947;C, M; 
        606;Kentucky;Ashland;United States;01/01/1955;E, C; 
        607;New York;Binghamton;United States;01/01/1954;E; 
        608;Wisconsin;Madison;United States;01/01/1955;C; 
        609;New Jersey;Trenton;United States;01/01/1957;E; 
        610;Pennsylvania;Allentown;United States;01/08/1994;E;215
        612;Minnesota;Minneapolis;United States;01/01/1947;C; 
        613;Ontario;Ottawa;Canada;01/01/1947;E; 
        614;Ohio;Columbus;United States;01/01/1947;E; 
        615;Tennessee;Nashville;United States;01/01/1954;C; 
        616;Michigan;Grand Rapids;United States;01/01/1947;E; 
        617;Massachusetts;Boston;United States;01/01/1947;E; 
        618;Illinois;Centralia;United States;01/01/1947;C; 
        619;California;San Diego;United States;01/01/1982;P;714
        620;Kansas;Dodge City;United States;02/03/2001;C, M;316
        623;Arizona;Sun City;United States;03/01/1999;M;602
        626;California;Pasadena;United States;06/14/1997;P;818
        630;Illinois;Aurora;United States;08/03/1996;C;708
        631;New York;Suffolk County;United States;11/01/1999;E;516
        636;Missouri;Saint Charles;United States;05/22/1999;C;314
        641;Iowa;Mason City;United States;07/09/2000;C;515
        646;New York;New York City;United States;07/01/1999;E;212
        647;Ontario;Toronto;Canada;03/05/2001;E;416
        649;Turks and Caicos Islands;;United Kingdom;06/01/1997;E;809
        650;California;Palo Alto;United States;08/02/1997;P;415
        651;Minnesota;Saint Paul;United States;07/12/1998;C;612
        657;California;Anaheim;United States;09/23/2008;P;714
        660;Missouri;Marshall;United States;10/12/1997;C;816
        661;California;Bakersfield;United States;02/13/1999;P;805
        662;Mississippi;Greenville;United States;04/19/1999;C;601
        664;Montserrat;;Montserrat;07/01/1996;A;809
        670;Northern Mariana Islands;;United States;07/01/1997;(UTC + 10); 
        671;Guam;;United States;07/01/1997;(UTC + 10); 
        678;Georgia;Atlanta;United States;01/06/1998;E;770
        681;West Virginia;Charleston;United States;03/28/2009;E;304
        682;Texas;Fort Worth;United States;10/07/2000;C;817
        684;American Samoa;;United States;10/02/2004;(UTC - 11); 
        700;Interexchange Carrier Services;; ;01/01/1984;; 
        701;North Dakota;;United States;01/01/1947;C, M; 
        702;Nevada;Las Vegas;United States;01/01/1947;P; 
        703;Virginia;Arlington;United States;01/01/1947;E; 
        704;North Carolina;Charlotte;United States;01/01/1947;E; 
        705;Ontario;North Bay;Canada;01/01/1957;E; 
        706;Georgia;Columbus;United States;05/03/1992;E;404
        707;California;Santa Rosa;United States;01/01/1959;P;415
        708;Illinois;Melrose Park;United States;11/11/1989;C;312
        709;Newfoundland and Labrador;;Canada;01/01/1962;N, A; 
        710;United States Government;;United States;01/01/1984;; 
        712;Iowa;Sioux City;United States;01/01/1947;C; 
        713;Texas;Houston;United States;01/01/1947;C; 
        714;California;Santa Ana;United States;01/01/1951;P;213
        715;Wisconsin;Eau Claire;United States;01/01/1947;C; 
        716;New York;Buffalo;United States;01/01/1947;E; 
        717;Pennsylvania;Harrisburg;United States;01/01/1947;E; 
        718;New York;New York City;United States;09/01/1984;E;212
        719;Colorado;Pueblo;United States;03/05/1988;M;303
        720;Colorado;Denver;United States;06/01/1998;M;303
        721;Sint Maarten;;Sint Maarten;09/30/2011;A; 
        724;Pennsylvania;New Castle;United States;02/01/1998;E;412
        727;Florida;Saint Petersburg;United States;07/01/1998;E;813
        731;Tennessee;Jackson;United States;02/12/2001;C;901
        732;New Jersey;New Brunswick;United States;06/01/1997;E;908
        734;Michigan;Ann Arbor;United States;12/13/1997;E;313
        740;Ohio;Portsmouth;United States;12/06/1997;E;614
        747;California;Burbank;United States;05/18/2009;P;818
        754;Florida;Fort Lauderdale;United States;08/01/2001;E;954
        757;Virginia;Virginia Beach;United States;07/01/1996;E;804
        758;Saint Lucia;;Saint Lucia;07/01/1996;A;809
        760;California;Palm Springs;United States;03/22/1997;P;619
        762;Georgia;Augusta;United States;05/16/2006;E;706
        763;Minnesota;Maple Grove;United States;02/27/2000;C;612
        765;Indiana;Kokomo;United States;02/01/1997;E;317
        767;Dominica;;Dominica;10/01/1997;A;809
        769;Mississippi;Jackson;United States;03/14/2005;C;601
        770;Georgia;Atlanta;United States;08/01/1995;E;404
        772;Florida;Vero Beach;United States;02/11/2002;E;561
        773;Illinois;Chicago;United States;10/12/1996;C;312
        774;Massachusetts;Brockton;United States;05/02/2001;E;508
        775;Nevada;Carson City;United States;12/12/1998;P;702
        778;British Columbia;Victoria;Canada;11/03/2001;P;604
        779;Illinois;Rockford;United States;03/17/2007;C;815
        780;Alberta;Edmonton;Canada;05/18/1999;M;403
        781;Massachusetts;Waltham;United States;09/01/1997;E;617
        784;St Vincent and the Grenadines;;St Vincent and the Grenadines;06/01/1998;A;809
        785;Kansas;Topeka;United States;07/20/1997;C, M;913
        786;Florida;Miami;United States;03/01/1998;E;305
        787;Puerto Rico;;United States;03/01/1996;A;809
        800;Toll-Free Service;; ;01/01/1966;; 
        801;Utah;Salt Lake City;United States;01/01/1947;M; 
        802;Vermont;;United States;01/01/1947;E; 
        803;South Carolina;Columbia;United States;01/01/1947;E; 
        804;Virginia;Richmond;United States;06/24/1973;E; 
        805;California;Ventura;United States;01/01/1957;P;415
        806;Texas;Amarillo;United States;01/01/1957;C; 
        807;Ontario;Thunder Bay;Canada;01/01/1962;E, C; 
        808;Hawaii;;United States;01/01/1957;(UTC - 10); 
        809;Dominican Republic;;Dominican Republic;01/01/1958;E; 
        810;Michigan;Flint;United States;12/01/1993;E;313
        812;Indiana;Evansville;United States;01/01/1947;E, C; 
        813;Florida;Tampa;United States;01/01/1953;E; 
        814;Pennsylvania;Erie;United States;01/01/1947;E; 
        815;Illinois;Joliet;United States;01/01/1947;C; 
        816;Missouri;Kansas City;United States;01/01/1947;C; 
        817;Texas;Fort Worth;United States;01/01/1953;C; 
        818;California;Burbank;United States;01/07/1984;P;213
        819;Quebec;Sherbrooke;Canada;01/01/1957;E; 
        828;North Carolina;Asheville;United States;03/22/1998;E;704
        829;Dominican Republic;;Dominican Republic;08/01/2005;E;809
        830;Texas;Del Rio;United States;07/07/1997;C;210
        831;California;Monterey;United States;07/11/1998;P;408
        832;Texas;Houston;United States;01/16/1999;C;713
        843;South Carolina;Charleston;United States;03/22/1998;E;803
        845;New York;Poughkeepsie;United States;06/05/2000;E;914
        847;Illinois;Evanston;United States;01/20/1996;C;708
        848;New Jersey;New Brunswick;United States;12/29/2001;E;732
        849;Dominican Republic;Santo Domingo;Dominican Republic;07/01/2009;E;809
        850;Florida;Tallahassee;United States;06/23/1997;E, C;904
        855;Toll-Free Service;; ;10/09/2010;;800
        856;New Jersey;Vineland;United States;06/12/1999;E;609
        857;Massachusetts;Boston;United States;05/02/2001;E;617
        858;California;San Diego;United States;06/12/1999;P;619
        859;Kentucky;Lexington;United States;04/01/2000;E;606
        860;Connecticut;Hartford;United States;08/28/1995;E;203
        862;New Jersey;Newark;United States;12/29/2001;E;973
        863;Florida;Lakeland;United States;09/20/1999;E;941
        864;South Carolina;Greenville;United States;12/03/1995;E;803
        865;Tennessee;Knoxville;United States;11/01/1999;E;423
        866;Toll-Free Service;; ;07/29/2000;;800
        867;Northwest Territories, Nunavut, Yukon;;Canada;10/21/1997;C, M, P;403
        868;Trinidad and Tobago;;Trinidad and Tobago;06/01/1997;A;809
        869;Saint Kitts and Nevis;;Saint Kitts and Nevis;10/01/1996;A;809
        870;Arkansas;Pine Bluff;United States;04/14/1997;C;501
        872;Illinois;Chicago;United States;11/07/2009;C;312
        876;Jamaica;;Jamaica;05/01/1997;E;809
        877;Toll-Free Service;; ;04/04/1998;;800
        878;Pennsylvania;New Castle;United States;08/17/2001;E;412
        888;Toll-Free Service;; ;03/01/1996;;800
        900;Premium Services;; ;01/01/1971;; 
        901;Tennessee;Memphis;United States;01/01/1947;C; 
        902;Nova Scotia, Prince Edward Island;;Canada;01/01/1947;A; 
        903;Texas;Tyler;United States;11/04/1990;C;214
        904;Florida;Jacksonville;United States;07/11/1965;E; 
        905;Ontario;Hamilton;Canada;10/04/1993;E;416
        906;Michigan;Escanaba;United States;01/01/1961;E, C; 
        907;Alaska;;United States;01/01/1957;(UTC - 9); 
        908;New Jersey;Elizabeth;United States;11/01/1990;E;201
        909;California;San Bernardino;United States;11/14/1992;P;714
        910;North Carolina;Fayetteville;United States;11/14/1993;E;919
        912;Georgia;Savannah;United States;01/01/1954;E; 
        913;Kansas;Kansas City;United States;01/01/1947;C; 
        914;New York;White Plains;United States;01/01/1947;E; 
        915;Texas;El Paso;United States;01/01/1947;C, M; 
        916;California;Sacramento;United States;01/01/1947;P; 
        917;New York;New York City;United States;01/01/1992;E;212
        918;Oklahoma;Tulsa;United States;01/01/1953;C; 
        919;North Carolina;Raleigh;United States;01/01/1954;E; 
        920;Wisconsin;Green Bay;United States;07/26/1997;C;414
        925;California;Concord;United States;03/14/1998;P;510
        928;Arizona;Flagstaff;United States;06/23/2001;M;520
        929;New York;New York City;United States;04/16/2011;E;347
        931;Tennessee;Columbia;United States;09/15/1997;E, C;615
        936;Texas;Huntsville;United States;02/19/2000;C;409
        937;Ohio;Dayton;United States;09/28/1996;E;513
        938;Alabama;Huntsville;United States;07/10/2010;C;256
        939;Puerto Rico;;United States;09/15/2001;A;787
        940;Texas;Wichita Falls;United States;05/25/1997;C;817
        941;Florida;Bradenton;United States;05/28/1995;E;813
        947;Michigan;Pontiac;United States;09/07/2002;E;248
        949;California;Irvine;United States;04/18/1998;P;714
        951;California;Temecula;United States;07/17/2004;P;909
        952;Minnesota;Bloomington;United States;02/27/2000;C;612
        954;Florida;Fort Lauderdale;United States;09/11/1995;E;305
        956;Texas;Brownsville;United States;07/07/1997;C;210
        970;Colorado;Aspen;United States;04/02/1995;M;303
        971;Oregon;Salem;United States;10/01/2000;P;503
        972;Texas;Dallas;United States;09/14/1996;C;214
        973;New Jersey;Newark;United States;06/01/1997;E;201
        978;Massachusetts;Salem;United States;09/01/1997;E;508
        979;Texas;Bryan;United States;02/19/2000;C;409
        980;North Carolina;Charlotte;United States;04/01/2001;E;704
        985;Louisiana;Houma;United States;02/12/2001;C;504
        989;Michigan;Saginaw;United States;04/07/2001;E;517
        '''
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    name = sys.argv[0]
    if old:
        print(dedent(f'''
        Usage:  {name} [options] cmd
            cmd         Result
          ------        ----------------------------------------------
          Number        The description of that area code.
          String        Area codes with that string (case-insensitive)
          2 letters     Show area codes for that state
          all           See everything
        Options
            -t      Show timezone(s) of given areacode
        '''))
    else:
        print(dedent(f'''
        Usage:  {name} [options] cmd
            cmd         Result
          ------        ----------------------------------------------
          Number        The description of that area code.
          String        Area codes with that string (case-insensitive)
          2 letters     Show area codes for that state
          all           See everything
        '''))
    exit(status)
def ParseCommandLine(d):
    d["-i"] = False     # Case-sensitive search
    d["-t"] = False     # Show time zones instead
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "it")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-i":
            d["-i"] = True
        if opt[0] == "-t":
            d["-t"] = True
    if not old and d["-t"]:
        Error("Time zones not supported in new version")
    if not args:
        Usage(d)
    return args
def GetOldData(d):
    '''Return a dictionary keyed by the areacode.  The values
    will be (state, string to display, time zone integer).
    '''
    lines = [i.strip() for i in data.split("\n")]
    ac = {}
    for i in lines:
        if not i or i[0] == "#":
            continue
        f = i.split(";")
        if len(f) not in (4, 5):
            raise Exception("'%s' is bad line" % i)
        areacode = int(f[0])
        if len(f) == 5:
            s = (f[1], "%s:  %s" % (f[1], f[3]), int(f[4]))
        else:
            s = (None, "%s" % f[2], int(f[3]))
        ac[areacode] = s
    BuildStates(d)
def BuildStates(d):
    # Build d["states"], a dictionary indexed by the state's two
    # letters and whose values are a list of the areacode numbers
    # associated with that state.
    st = defaultdict(list)
    ac = d["ac"]
    for areacode in ac:
        state = ac[areacode][0]
        if state is not None:
            st[state.upper()].append(areacode)
    d["states"] = st
def GetData(d):
    '''Return a dictionary keyed by the areacode.  The values
    will be (state, city).
    '''
    ac = {}
    for line in newdata.split("\n"):
        if not line.strip():
            continue
        f = line.strip().split(";")
        assert(len(f) == 7)
        areacode = int(f[0])
        try:
            state = states.n2l[f[1]]
        except Exception:
            state = f[1]
        city = f[2]
        ac[areacode] = (state, city)
    d["ac"] = ac
    BuildStates(d)
    return ac
def PrintAreacodeOld(ac, d):
    '''Print the entry associated with the number ac.
    '''
    assert isinstance(ac, int)
    state, descr, tz = d["ac"][ac]
    print("%3d:  %s" % (ac, descr))
def PrintAreacode(ac, d):
    '''Print the entry associated with the number ac.
    '''
    assert isinstance(ac, int)
    state, descr = d["ac"][ac]
    print(f"{ac:3d} {state} {descr}")
def DetermineCommandType(cmd, d):
    e = "'%s' is not a valid areacode" % cmd
    if cmd == "all":
        return "all"
    # See if it's an integer
    try:
        c = int(cmd)
        if not (201 <= c <= 999):
            Error(e)
        if str(c) == cmd:
            return "integer"
    except ValueError:
        pass
    # See if it's a two-character state name.  Build a dictionary of
    # state names that link to area code numbers.
    if cmd.upper() in d["states"]:
        return "state"
    # Otherwise, it's a string to search for
    return "search"
if __name__ == "__main__": 
    d = {}  # Options dictionary
    old = False
    d["ac"] = ac = GetData(d)
    args = ParseCommandLine(d)
    for cmd in args:
        cmd = cmd.strip()
        if not cmd:
            Error("Can't have empty commands")
        cmdtype = DetermineCommandType(cmd, d)
        if cmdtype == "all":
            for i in ac:
                if old:
                    PrintAreacodeOld(i, d)
                else:
                    PrintAreacode(i, d)
        elif cmdtype == "integer":
            if int(cmd) in ac:
                if old:
                    PrintAreacodeOld(int(cmd), d)
                else:
                    PrintAreacode(int(cmd), d)
            else:
                Error(f"Area code '{cmd}' not in database")
        elif cmdtype == "state":
            for ac in d["states"][cmd.upper()]:
                if old:
                    PrintAreacodeOld(ac, d)
                else:
                    PrintAreacode(ac, d)
        elif cmdtype == "search":
            for i in ac:
                state, descr, tz = ac[i]
                if descr.lower().find(cmd.lower()) != -1:
                    if old:
                        PrintAreacodeOld(i, d)
                    else:
                        PrintAreacode(i, d)
        else:
            Error("Program bug:  bad cmdtype")
