from collections import namedtuple
from color import t
from get import GetTextLines
from dpprint import PP

pp = PP()
from pdb import set_trace as xx
import iso
import sys
import time

if 0:
    import debug

    debug.SetDebugger()

# Fields are
#   0   Title
#   1   Artist
#   2   URL
#   3   Comment

Entry = namedtuple("Entry", "name artist url comment")
S = "|"  # Field separator

favorites = f"""

Angie {S} Rolling Stones {S} oWRr03VcA-0 {S}
Beethoven's 7th {S} Bernstein {S} Rw-KtQLdRT4 {S} 2nd movement 14:33 is best
Beethoven's 9th, 2nd movement (1824) {S} {S} iwIvS4yIThU {S} Genius
Bad Romance {S} PMJ, Sarah Reich, Ariana Savalas {S} VCTOpdlZJ8U {S} 
Catharsis {S} Sally {S} h3hlFAVV6aI {S} My favorite fiddle song
Crazy {S} Patsy Cline {S} MbnrdCS57d0 {S} 
Diamonds and Rust {S} Joan Baez {S} IrVD0bP_ybg {S} Baez's best
Don't Cry For Me Argentina {S} Karen Carpenter {S} _n8mq7sedP4 {S} A masterpiece
Fast Freight {S} Eliza Gilkyson {S} Sin3FeAQAws {S}  Singer is song writer's daughter
Hit the Road Jack {S} Becca Krueger {S} OfUDsHtSv88 {S} (skip first 20 seconds)
Ievan Polkka {S} Loituma {S} 4om1rQKPijI {S} A masterpiece of a capella, 2008
Ievan Polkka {S} Loituma {S} Zcg66Qcwjw8 {S} 13 years later, 2021
I'll Never Find Another You {S} Seekers {S} KmactMIhrRM {S} How I feel about Glenda
Korobushka {S} {S} Pr3ZgN8onRA {S} 
Korobushka {S} Bond {S} E5NByiEIbD8 {S} 
Midnight In Moscow {S} Kenny Ball {S} o744d4mwOgQ {S} Dixieland from England
Papillon (waltz arrangement) {S} {S} FKrmozFh5ww {S} 
Potato Head Blues {S} Louis Armstrong {S} EfGZB78R7uw {S} Famous trumpet solo
Scheherazade (1st movement) {S} Rimsky-Korsakov {S} 6dDk6aft4JU {S} von Karajan on Deutsche Grammophone
Stairway to Heaven {S} Led Zeppelin {S} QkF3oxziUI4 {S} 
This is a Man's World {S} PMJ, Morgan James {S} mPimt0Zu_To {S} 
Vltava (The Moldau) {S} Smetana {S} l6kqu2mk-Kw {S} 
Volga Boatmen {S} {S} qsovBF4N27Q {S}

"""

dead_urls = f"""
Hot Rod Lincoln {S} {S} 3R7l7nDuj1o {S} 
White Rabbit {S} Jefferson Airplane {S} EUY2kJE0AZE {S} 
Mack the Knife {S} Bobby Darin {S} SEllHMWkXEU {S} 
Georgia On My Mind {S} Ray Charles {S} QL3EZwSJAh0 {S} 
Fever {S} Peggy Lee {S} JGb5IweiYG8 {S} 
The Night the Lights Went Out in Georgia {S} Vicki Lawrence {S} wMD5nBcPrCk {S} 
I Will Survive {S} {S} ARt9HV9T0w8 {S} 
Bad Bad Leroy Brown {S} Jim Croce {S} CIiVindRSTA {S} 
"""
songs = f"""

100 lbs of Clay {S} Gene McDaniels {S} rUGonj90b5I {S}
16 Tons {S} Tennessee Ernie Ford {S} jIfu2A0ezq0 {S} 
25 Or 6 To 4 {S} Chicago {S} iUAYeN3Rp2E {S} Great horns and guitar
A Horse With No Name {S} America {S} mSZXWdKSQNM {S} 
A World of our Own {S} Seekers {S} PSxwqBJLU8A {S} 
Africa {S} Toto {S} qDLJ3pUZm9A {S} 
All Out of Love {S} Air Supply {S} https://www.youtube.com/watch?v=tH2w6Oxx0kQ {S} 
American Pie {S} Don Maclean {S} iX_TFkut1PM {S} 
Angel of the Morning {S} {S} https://www.youtube.com/watch?v=HTzGMEfbnAw {S} 
Aquarius {S} Fifth Dimension {S} oPK7ZF6jfJE&t=8 {S} 
Ballad Of Cat Ballou {S} Nat King Cole and Stubby Kaye{S} -ghnpUNTR1I {S} 
Barracuda {S} Heart {S} PeMvMNpvB5M {S} 
Bay Of Mexico {S} Kingston Trio {S} -16OczraVi4 {S} 
Beat It {S} Michael Jackson {S} oRdxUFDoQe0 {S} 
Big John {S} {S} KnnHprUGKF0 {S} 
Blowin' in the Wind {S} Peter, Paul, and Mary {S} Ld6fAO4idaI {S} 
Blue World {S} Moody Blues {S} 8a9bfvNuTw0 {S} With lyrics
Blue World {S} Moody Blues {S} oosjl8wNLJU {S} 
Boogie Woogie Bugle Boy {S} Andrew Sisters {S} 8of3uhG1tCI {S} 
Both Sides Now {S} Judy Collins {S} 8L1UngfqojI {S} 
Brandy {S} Looking Glass {S} CFhFyvk0yS8 {S}
Bucket drummer {S} ? {S} FqJdzYY_Fas {S} 
Build Me Up Buttercup {S} The Foundations {S} w0kLkDCoRXc {S}
Bus Stop {S} Hollies {S} It75wQ0JypA {S} 
Carpool karaoke {S} Paul McCartney {S} QjvzCTqkBDQ {S} 
Charles:  Cincinnati Kid {S} Ray Charles {S} rfn1YrwG2Oc {S} 
Classical Gas {S} Mason Williams {S} PRZkc88uNXo {S} 
Country Roads {S} John Denver {S} 1vrEljMfXYo {S} 
Country Roads {S} Petersens {S} qap9Qm-Q894 {S} Petersens
Crocodile Rock {S} Elton John {S} 75r0nQu-hMs {S} 
Darin:  Dream Lover {S} Bobby Darin {S} wVHAQX5sSaU {S} 
Different Drum {S} Stone Pony {S} w9qsDgA1q8Y {S} 
Doc & San Miguel 5 {S} Doc Severinsen and Arturo Sandoval {S} s53B0PyAEOE {S} Great trumpets & guitar, but the violin is best
Downtown {S} Petula Clark {S} Zx06XNfDvk0 {S} 
Dreams {S} Fleetwood Mac {S} O5ugW4-BstE {S} 
Drive My Car {S} Beatles {S} kfSQkZuIx84 {S} 
Dueling Banjos {S} Deliverance movie {S} myhnAZFR1po {S} 
Dust in the Wind {S} Kansas {S} tH2w6Oxx0kQ {S} 
Early In The Morning {S} Vanity Fare {S} 9hN9YRo7y1s {S}
Easy Lover {S} Phil Collins {S} 2aJ2Vh_e2dQ {S} 
El Condor Pasa {S} Simon & Garfunkel {S} pey29CLID3I {S} 
El Paso {S} Marty Robbins {S} -zBzZJd-nfw {S} 
Eli's coming {S} Three Dog Night {S} 1A2eet1bttY {S} Also look up writer's Laura Nyro's version.
End of the World {S} Skeeter Davis {S} sonLd-32ns4 {S} 
Even the Nights Are Better {S} Air Supply {S} https://www.youtube.com/watch?v=BRx58DgOxeg {S} 
Everybody's Somebody's Fool {S} Connie Francis {S} ECOthzFvUXY {S} 
Exodus {S} Ferranti & Teicher {S} xhXZ3eXJIFc {S} 
Eye Of The Tiger {S} Survivor {S} btPJPFnesV4 {S} 
Eye in the Sky {S} Alan Parsons Project {S} 56hqrlQxMMI {S} 
Fast Freight {S} Kingston Trio {S} Oy_NkJOwRqE {S} 
Flight of the Condor {S} BBC TV show {S} 66KVAhNE_rQ {S} This was a 1982 BBC TV show and had great pan pipe music from South America.
Foggy Mountain Breakdown {S} Flatt & Scruggs {S} z_Y3mnj-8lA {S} 
For What It's Worth {S} Buffalo Springfield {S} gp5JCrSXkJY {S} 
Für Elise {S} {S} 2fcX2dWmR6g {S} 
Games People Play {S} Alan Parsons Project {S} SLi7Ljcy6n8 {S} 
Ghost Riders In the Sky {S} Burl Ives {S} j2klh2cTa_Q {S} 
Ghost Riders In the Sky {S} Frankie Laine {S} ZwAPa0qHmLo {S} 
Ghost Riders In the Sky {S} Highwaymen {S} nOWjX4BpC24 {S} 
Ghost Riders In the Sky {S} Marty Robbins {S} fD5kS3G1Jkk {S} 
Ghost Riders In the Sky {S} Roy Clark & Glen Campbell {S} v_kbgjsuCec {S} 
Ghost Riders In the Sky {S} Roy Clark {S} 8o2w1zhBKzk {S} 
Girl drummer {S} {S} L-So4DLDvGc {S} 
Gypsy Waltz {S} Sally {S} eDGE6ah-e4Y {S} 
Gypsy {S} Fleetwood Mac {S} mwgg1Pu6cNg {S} 
Hair {S} Cowsills {S} BFy-yzj02FE {S} 
Hallelujah {S} Lucy Thomas {S} dLk9pzmaFHY {S}
Hang 'Em High {S} Movie theme {S} 0gscut1p4kY {S} 
Hava Nagila {S} Dalida {S} YBj2PZ1IeIc {S} 
Hawaii 50 {S} TV show theme {S} AepyGm9Me6w {S} 
Heart Full of Soul {S} Yardbirds {S} pM1qZBFiOLU {S} 
Heart of Gold {S} Neil Young {S} X3IA6pIVank {S} 
Hey Jude {S} Beatles {S} mQER0A0ej0M {S} 
Hit the Road Jack {S} Ray Charles {S} SrnWp5O0DEs {S}
Hotel California {S} Eagles {S} BciS5krYL80 {S} 
House Of The Rising Sun {S} Animals {S} MJkr0DWbhTk {S} 
How Blue Can You Get? {S} B.B. King {S} LWLAAzOBoBI {S} A masterpiece
I Am A Man Of Constant Sorrow {S} Movie song {S} OdYGnAFaeHU {S} 
I Left My Heart in San Francisco {S} Tony Bennett {S} SC73kdOL5hk {S} 
I love the flower girl {S} Cowsills {S} dZMc0-ZAUeY {S} 
I was Born Under a Wandering Star {S} Lee Marvin {S} NTymtAbaG08 {S} 
I'm Just A Singer in a Rock And Roll Band {S} Moody Blues {S} 5UZWXE76ELU {S} Album
I'm Just a Singer in a Rock and Roll Band {S} Moody Blues {S} s5tb25TqXYU {S} Concert
I'm Still Standing {S} Elton John {S} Ye9hGotPPVk {S} 
In Hell I'll be in Good Company {S} Dead South {S} B9FzVhw8_bY {S} 
In The Year 2525 {S} Zager &  Evans {S} yesyhQkYrQM {S} 
Indian Lake {S} Cowsills {S} 3Xup3HSZLIQ {S} Bubble rock
Isn't Life Strange {S} Moody Blues {S} 9WZZjXgJ4W8 {S} 
It Was A Very Good Year {S} Frank Sinatra {S} CJARjwzmceg {S} 
It's a Heartache {S} Bonnie Tyler {S} bEOl38y8Nj8 {S} 
Jailhouse Rock {S} Elvis Presley {S} A99sV18J0mk {S} 
Johnny B. Goode {S} Chuck Berry {S} Uf4rxCB4lys {S} 
Journey to Kilimanjaro {S} Nova TV show {S} 5ZFJWIGN9zQ {S} 1994 Melodically simple but haunting music:  0:48, 6:43, 9:28, 10:44, 30:07, 35:27, 37:33, 38:14*, 43:45, 50:42, 53:00(credits),
Judy Blue Eyes (1969) {S} Crosby, Stills, and Nash {S} cMJug2iz3NA {S} 1969
Judy Blue Eyes (2012) {S} Crosby, Stills, and Nash {S} XWvw_uZPGDA {S} 
Jumpin' Jack Flash {S} Rolling Stones {S} -rIG2POqtV8 {S} 
Kisses Sweeter Than Wine {S} Marty Robbins {S} iulmZAz8XfY {S} 
Kodachrome {S} Paul Simon {S} 8rlDTK6QI-w {S} 
Korobushka {S} Bond {S} vvC2vjtmUX8 {S} 
Land Down Under {S} Men at Work {S} 8jHXu86O01w {S} 
Les Bicyclettes De Belsize {S} Englebert Humperdinck {S} Qe_1B1P9Bw4 {S} 
Light My Fire {S} Doors {S} LY1l8T2Lcl0 {S} 
Listen To Your Heart {S} Roxette {S} yCC_b5WHLX0 {S} 
Long Cool Woman {S} Hollies {S} g8XiNKsKyVk {S} 
Love Me With All Your Heart {S} Ray Charles Singers {S} k3nfqH4YDDM {S} 
Love is Blue {S} Paul Muriat {S} YYf_hb-jsGo {S} 
MTA {S} Kingston Trio {S} MbtkL5_f6-4 {S} 
MacArthur Park {S} Richard Harris {S} iplpKwxFH2I {S} 
Maggie May {S} Rod Steward {S} EOl7dh7a-6g {S} 
Magnificent Seven {S} Movie theme {S} 8XDB7GMnbUQ {S} 
Making Love Out of Nothing at All {S} Air Supply {S} https://www.youtube.com/watch?v=JMKi9qVrGWM {S} 
Mambo Italiano {S} Rosemary Clooney {S} 9prJXEhNhPA {S} 
Me & Bobby McGee {S} Janis Joplin {S} WXV_QjenbDw {S} 
Memories (from Cats){S} Barbra Streisand {S} MWoQW-b6Ph8 {S} 
Memories (from Cats){S} Betty Buckley {S} 5mlllRdIfqw {S} 
Memories (from Cats){S} Elaine Paige {S} mdBVJbzkoqo {S} 
Midnight In Moscow {S} Sweet & Hot 2011 {S} FY3Zr5Tj5zw {S} 2011
Morningtown Ride {S} Seekers {S} M-RkC6MYT2E {S} 1964
Morningtown Ride {S} Seekers {S} wqdaCOt51Dk {S} 2014
Mr. Roboto {S} Styx {S} 51ybp_YFo7I {S} 
Mrs. Robinson {S} Simon & Garfunkel {S} _C2vqI9FVwg {S} 
My Sweet Lord {S} George Harrison {S} AR4lpQWcT5g {S} 
Nancy Sinatra and Lee Hazelwood: Lady Bird {S} Nancy Sinatra and Lee Hazelwood {S} FIPQVpw-zkk {S} 
Nancy Sinatra and Lee Hazelwood: Summer Wine {S} Nancy Sinatra and Lee Hazelwood {S} Ib_eW9VSUwM {S} 
North to Alaska (1960) {S} Johnny Horton {S} RO6IU9RpjS8 {S} 
Nothing Else Matters {S} Metallica {S} tAGnKpE4NCI {S} 
Nothing Else Matters {S} PMJ, 15 year old girl singer {S} KSSa0-oAnIo {S} 
Nothing Else Matters: Banjo & Mandolin {S} {S} 3JFb_aOn6rc {S} 
Nothing Else Matters: Guitar & cello {S} {S} pxoW-00Zyho {S} 
Nothing Else Matters: Guitar {S} {S} WlGiOiRQNhI {S} 
Nothing Else Matters: Hammered dulcimer {S} {S} 8KK0-9Moz5Q {S} 
Nothing Else Matters: Hardpan {S} {S} 32v8ARqaBas {S} She makes it look easy
Nothing Else Matters: Harp {S} {S} KMX2bmtS_TE {S} 
Nothing Else Matters: Piano {S} {S} DmL12NRE4hQ {S} 
Old Man {S} Neil Young {S} rAtDrFdomN4 {S} 
Old and Wise {S} Alan Parsons Project {S} ZmzqqdVFw8g {S} 
One {S} Three Dog Night {S} UiKcd7yPLdU {S} 
Orange Blossom Special {S} Sally {S} 6-5xPixiCkI {S} 
Paint It Black {S} Rolling Stones {S} O4irXQhgMqg {S} 
Papa Was a Rollin' Stone {S} Temptations {S} 71l85z2bXAs {S} 
Paperback Writer {S} Beatles {S} yYvkICbTZIQ {S} 
Papillon {S} Movie theme {S} Js69DkyaDVQ {S} 
Patricia {S} {S} rTXIXkeWnEo {S} 
Penny Lane {S} Beatles {S} S-rB0pHI9fU {S} 
People {S} Barbra Streisand {S} fPlQ6EtArSc {S} 
Pirates of the Caribbean {S} Auckland Symphony {S} 6zTc2hD2npA {S}
Pirates of the Caribbean {S} Movie theme {S} 27mB8verLK8 {S} 
Popcorn Song {S} {S} DBYjZTdrJlA {S} 
Purple People Eater {S} Sheb Wooley {S} Rx47qrH1GRs {S} 
Push It To The Limit {S} Movie theme {S} 9D-QD_HIfjA {S} 
Puttin' on the Ritz {S} Berlin Brass Quintet {S} oQVR-fnyM3o {S}
Que Sera Sera {S} Doris Day {S} xZbKHDPPrrc {S} 
Queen of Hearts {S} Juice Newton {S} P0DK-0fIKCw {S} 
Question {S} Moody Blues {S} tmOZFAYeurY {S} 
Rainy Days and Monday {S} Carpenters {S} PjFoQxjgbrs {S} 
Rainy Night in Georgia {S} Brook Benton {S} bDRbF80NKDU {S} 
Rawhide {S} Frankie Laine {S} _EjbzCX3enA {S} 
Ride My See-saw {S} Moody Blues {S} GXHMTuoK060 {S} 
Rocket Man {S} Elton John {S} BdEe5SpdIuo {S} 
Run Through The Jungle {S} Creedence Clearwater {S} EbI0cMyyw_M {S} 
Runaround Sue {S} Dion {S} nFch8vH81ks {S}
Sally Goodin {S} Sally {S} nbYBBeylfGk {S} My second-favorite fiddle song
Scarborough Fair {S} Simon & Garfunkel {S} -BakWVXHSug {S} 
Scat singing {S} Ella Fitzgerald & Mel Torme {S} 9CbVy1NnB4g {S} 
She Works Hard for the Money {S} Donna Summers {S} 09ZSKE38lTU {S} 
She's Got You {S} Peterson {S} 7nXPQbKZBbw {S} 
Shrek Hallelujah {S} Rufus Wainright {S} EbO6P-_Zx0Y {S} 
Silver Threads and Golden Needles {S} Dusty Springfield {S} uz6HB9HYQz4 {S} Dusty Springfield
Sounds of Silence {S} Simon & Garfunkel {S} 4zLfCnGVeL4 {S} 
Stairway to Heaven (concert) {S} Led Zeppelin {S} BciS5krYL80e {S} 
Stairway to Heaven {S} Heart {S} 2cZ_EFAmj08 {S} 
Stairway to Heaven: Harp {S} {S} wLiH6F82t_U {S} 
Struttin' With Some Barbecue {S} Louis Armstrong {S} yl-2R_Pb7dk {S} 
Sunrise, Sunset {S}  {S} 03rzUoyq9K0 {S}
Sunrise, Sunset {S} Bette Midler {S} QD8u-fjQnFs {S}
Superstar {S} Carpenters {S} SJmmaIGiGBg {S} 
Suzy Q {S} Creedence Clearwater {S} 7x60p7UNLnQ {S} 
Sweet Dreams {S} Eurythmics {S} qeMFqkcPYcg {S} 
Take Five {S} Dave Clark Five {S} vmDDOFXSgAs {S} 
The Boxer {S} Simon & Garfunkel {S} C1VUWDcp5Sg {S} 
The Crystal Ship {S} Doors {S} bU1sLx1tjPY {S} 
The Gambler {S} Kenny Rogers {S} 7hx4gdlfamo {S} 
The Little Nash Rambler {S} Playmates {S} enqNl7tdLR4 {S} 
The Night They Drove Old Dixie Down {S} Joan Baez {S} wanJQC5KAfo {S} 
The Thrill is Gone {S} B.B. King {S} Nu4tjTyqbho {S} 
The Voice {S} Moody Blues {S} -umqM9R8cnI {S} 
The Wreck of the Edmund Fitzgerald {S} Gordon Lightfoot {S} 9vST6hVRj2A {S} 
Theme From Shaft {S} Isaac Hayes {S} Q429AOpL_ds {S} 
These Boots Are Made for Walkin' {S} Nancy Sinatra {S} rypT2qMO1RY {S} 
They Call the Wind Mariah {S} Harv Presnel {S} ByqYEzugleE {S}
They Call the Wind Mariah {S} Smothers Brothers {S} wFHh0Rs34v0 {S}
This is a Man's World {S} James Brown {S} wd1-HM234DE {S} 
Those Were The Days {S} Mary Hopkins {S} y3KEhWTnWvE {S} 
Time Won't Let Me {S} Outsiders {S} 3yQERVphWhY {S} 
Today (1964) {S} Christy Minstrels {S} 3cELsUMcQdc {S} 
Torn Between Two Lovers {S} {S} TzGbvTl4mpg {S} 
Total Eclipse of the Heart {S} Bonnie Tyler {S} lcOxhH8N3Bo {S} 
Tuxedo Junction {S} Mary MacGregor {S} iBTYcqtaOjg {S} 
Two Faces Have I {S} Lou Christie {S} w05w1XbZTG8 {S} 
Unchained Melody {S} Righteous Brothers {S} m0EBs6uRgtw {S} 
Unforgettable {S} Nat King Cole {S} Fy_JRGjc1To {S} 
Unknown song {S} Sally {S} ob44BR1Hurg {S} 
Unsquare Dance {S} Dave Clark Five {S} lbdEzRfbeH4 {S} 
Victory {S} Bond {S} j3nBuwOPu8A&list=RDE5NByiEIbD8 {S} 
Volga Boatmen  {S} Red Army Choir & Band {S} yfO0ADduEr8 {S} 1996
Volga Boatmen {S} L. Kharitonov {S} 0tw3g88JtWA {S} 1965 
Walk On the Wild Side {S} Walk on the Wild Side {S} 5O82y59h7MI {S} 
Walking in the Air {S} Walking In the Air movie {S} upH1QZU4Z0Y {S} Movie theme sung by a 13 year old choirboy Aled Jones
Walking in the Air {S} Malakai Bayoh & Aled Jones {S} Lq8kqsI3hCo {S} Movie theme sung by a 13 year old choirboy
Wanderer {S} Dion {S} SbYa7NBYyRc {S}
Washington Square {S} Village Stompers {S} ihenbyTzQ2A {S} 
White Silver Sands {S} Don Rondo {S} mOqbjENGN7s {S} 
Who's on First {S} Abbott & Costello {S} jIGRgmxRfiE {S} Genius comedy
Woman in Love {S} Barbra Streisand {S} hQLGCX8D-1Y {S} 
Yesterday When I was Young {S} Roy Clark {S} GQIAcztYjbc {S} 
You Only Live Twice {S} Nancy Sinatra {S} XgFtQPgHyek {S} 
You Were On My Mind {S} We Five {S} c7YSANg8vgw {S} 
You'll Never Know {S} Ralna English {S} 4HU8I9BY1H0 {S} 
You're So Vain {S} Carly Simon {S} cleCtBP0o5Y {S} 
Your Wildest Dreams {S} Moody Blues {S} kmmPFrkuPq0 {S} 

Rimsky-Korsakov:  Scheherazade {S} {S} 1i6TsIVKByM {S} Excellent youth orchestra
Barber of Seville (1821) {S} {S} OloXRhesab0 {S} Most of us probably heard this first by watching Saturday morning cartoons.
Ravel: Bolero {S} {S} 8KsXPq3nedY {S} 
Beethoven: Moonlight Sonata (3rd) {S} {S} o6rBK0BqL2w {S} 17 year old girl (Tina S)
Beethoven: Moonlight Sonata (3rd) {S} {S} zucBfXpCA6s {S} Valentina Lisitsa
Beethoven:  2nd movement 9th {S} {S} p5favl2Qtx0 {S} Player-piano type visual
Beethoven: Für Elise {S} {S} _mVW8tgGY_w {S} 
Beethoven: Moonlight Sonata {S} {S} 4Tr0otuiQuU {S} 
Beethoven's 9th {S} {S} fRZaX6-dsn8 {S} 
Beethoven's 5th {S} {S} 1lHOYvIhLxo {S} 
Beethoven's 5th {S} {S} Zev0ran0iuU {S} NY Philharmonic
Beethoven's 7th {S} {S} W5NsPOgyALI {S} 
Dvorak:  New World Symphony (Dvorak's 9th 1893) {S} {S} VuaTY3zHO8Q {S} London Symphony Orchestra
New World Symphony and The Moldau {S} {S} Qut5e3OfCvg {S} Slovak Philharmonic
Tchaikovsky:  1812 Overture (1888) {S} {S} QUpuAvQQrC0 {S} 

Bach: Toccata and Fugue in D Minor: Violin {S} {S} JL0PCLMSQms {S} Violin
Bach: Toccata and Fugue in D Minor: Brass {S} Canadian Brass {S} _Cst9lV5PPg {S} Superb
Bach: Toccata and Fugue in D Minor {S} {S} eDFFUIGoBUc {S} Accordion
Bach: Toccata and Fugue in D Minor {S} {S} ho9rZjlsyYY {S} Organ
Bach: Toccata and Fugue in D Minor {S} {S} i9UQ61EbdO0 {S} Orchestra
Bach: Toccata and Fugue in D Minor {S} {S} ipzR9bhei_o {S} Organ with bar graph score
Bach: Toccata and Fugue in D Minor {S} {S} oPmKRtWta4E {S} Harp (a masterpiece)
Bach: Toccata and Fugue in D Minor {S} {S} ojBYW3ycVTE {S} Guitar
Bach: Toccata and Fugue in D Minor {S} {S} zhH53UODLEM {S} Piano with visual score

"""


def Check(line):
    """Split on the field separator and check the that line has the requisite fields."""
    f = line.split(S)
    if len(f) != 4:
        print(f"Bad line:\n{line!r}")
        exit(1)


def Validate():
    "Check that all the lines have the proper form"
    for item in (favorites, songs):
        for line in GetTextLines(item):
            if not line or line.strip()[0] == "#":
                continue
            Check(line)


def Print(s):
    link = "https://www.youtube.com/watch?v="
    song_list = []
    # Process each line
    for line in s.split("\n"):
        line = line.strip()
        if not line or line[0] == "#":
            continue
        f = [i.strip() for i in line.split(S)]
        i = 2
        if not f[i].startswith("https://"):
            f[i] = link + f[i]
        entry = Entry(*f)
        song_list.append(entry)
    # Output the HTML data.  The Entry namedtuple is
    # namedtuple("Entry", "name artist url comment").
    for i in sorted(song_list):
        artist = f"[{i.artist}]" if i.artist else ""
        print(f'<a href="{i.url}">{i.name}</a> {artist} {i.comment} <br>')


def Notation():
    print(
        dedent("""
    """)
    )


if __name__ == "__main__":
    now = iso.ISO()
    Validate()
    long = len(sys.argv) > 1
    print(f"Favorites:</p>")
    Print(favorites)
    print(f"<p>Others:</p>")
    Print(songs)
    print(f"<p>Updated {now.date}<p>")

# vim: tw=0 wm=0
