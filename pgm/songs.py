import time
 
favorites = '''

2nd movement Beethoven's 9th (written 1824)|iwIvS4yIThU|Genius
Bad Romance|VCTOpdlZJ8U|PMJ & tap dancing (Sarah Reich) (singer is Telly Savalas' daughter)
Catharsis (2013)|h3hlFAVV6aI|My beloved Sa-Sa
Crazy (1961)|MbnrdCS57d0|
Diamonds and Rust (1975)|2MSwBM_CbyY|Baez's best
Don't Cry For Me Argentina (1977)|_n8mq7sedP4|A masterpiece
I'll Never Find Another You (1963)|KmactMIhrRM|How I feel about Glenda
Midnight In Moscow (1961)|o744d4mwOgQ|Dixieland from England
Potato Head Blues (1927)|EfGZB78R7uw|Famous trumpet solo
Scheherezade (1st movement, written 1888)|6dDk6aft4JU|von Karajan on Deutsche Grammophone (I bought this record in about 1970 and was mesmerized by it)
Stairway to Heaven (1971)|QkF3oxziUI4|
The Moldau (written 1875)|l6kqu2mk-Kw|Such accomplished young musicians

'''

songs = '''

16 Tons|jIfu2A0ezq0|
1812 Overture (1888)|QUpuAvQQrC0|Real cannons & church bells
25 Or 6 To 4|iUAYeN3Rp2E|Great horns and guitar
2nd movement Beethoven's 9th|p5favl2Qtx0|Player-piano type visual
A Horse With No Name|mSZXWdKSQNM|
A World of our Own|PSxwqBJLU8A|
Africa|qDLJ3pUZm9A|
American Pie|iX_TFkut1PM|
Angie|S7sigwbqEj8|
Aquarius|oPK7ZF6jfJE&t=8|
Bad Bad Leroy Brown|CIiVindRSTA|
Barber of Seville (1821)|OloXRhesab0|
Barracuda|PeMvMNpvB5M|
Bay Of Mexico|-16OczraVi4|
Beat It|oRdxUFDoQe0|
Big John|KnnHprUGKF0|
Blowin' in the Wind|Ld6fAO4idaI|
Bolero|8KsXPq3nedY|
Boogie Woogie Bugle Boy|8of3uhG1tCI|
Both Sides Now|8L1UngfqojI|
Bucket drummer|FqJdzYY_Fas|
Bus Stop|It75wQ0JypA|
Cincinnati Kid|rfn1YrwG2Oc|
Classical Gas|PRZkc88uNXo|
Country Roads|1vrEljMfXYo|John Denver
Country Roads|qap9Qm-Q894|Petersens
Crocodile Rock|75r0nQu-hMs|
Different Drum|w9qsDgA1q8Y|
Doc Severinsen and Arturo Sandoval|s53B0PyAEOE|Great trumpets & guitar, but the violin is best
Downtown|Zx06XNfDvk0|
Dream Lover|wVHAQX5sSaU|
Dreams|O5ugW4-BstE|
Drive My Car|kfSQkZuIx84|
Dueling Banjos|myhnAZFR1po|
Dust in the Wind|tH2w6Oxx0kQ|
Early In The Morning|9hN9YRo7y1s|
Easy Lover|2aJ2Vh_e2dQ|
El Condor Pasa|pey29CLID3I|
El Paso|-zBzZJd-nfw|
Eli's coming|1A2eet1bttY|Also look up writer's Laura Nyro's version.
Ella Fitzgerald scat singing|9CbVy1NnB4g|
End of the World|sonLd-32ns4|
Everybody's Somebody's Fool|ECOthzFvUXY|
Exodus|xhXZ3eXJIFc|
Eye Of The Tiger|btPJPFnesV4|
Fast Freight|Oy_NkJOwRqE|
Fast Freight|Sin3FeAQAws| Eliza Gilkyson (song writer's daughter)
Fever|JGb5IweiYG8|
Flight of the Condor|66KVAhNE_rQ|1982
Foggy Mountain Breakdown|z_Y3mnj-8lA|
For What It's Worth|gp5JCrSXkJY|
Georgia On My Mind|QL3EZwSJAh0|
Ghost Riders In the Sky|ZwAPa0qHmLo|Frankie Laine
Ghost Riders In the Sky|fD5kS3G1Jkk|Marty Robbins
Ghost Riders In the Sky|j2klh2cTa_Q|Burl Ives (1949)
Ghost Riders In the Sky|nOWjX4BpC24|Highwaymen (1990)
Girl drummer|L-So4DLDvGc|
Gypsy|mwgg1Pu6cNg|
Hair|BFy-yzj02FE|
Hang 'Em High Theme|0gscut1p4kY|
Hawaii 50 Theme|AepyGm9Me6w|
Heart Full of Soul|pM1qZBFiOLU|
Heart of Gold|X3IA6pIVank|
Hey Jude|mQER0A0ej0M|
Hit the Road Jack|OfUDsHtSv88|Becca Krueger (skip first 20 seconds)
Hit the Road Jack|SrnWp5O0DEs|
Hot Rod Lincoln|3R7l7nDuj1o|
Hotel California|811QZGDysx0|
House Of The Rising Sun|MJkr0DWbhTk|
How Blue Can You Get?|LWLAAzOBoBI|A masterpiece
I Am A Man Of Constant Sorrow|OdYGnAFaeHU|
I Left My Heart in San Francisco|SC73kdOL5hk|
I Will Survive|ARt9HV9T0w8|
I love the flower girl|dZMc0-ZAUeY|
I'm Still Standing|Ye9hGotPPVk|
Ievan Polkka|4om1rQKPijI|A masterpiece of a capella -- I love the scat singing of the girl in the red dress around 1:30
In The Year 2525|yesyhQkYrQM|
Indian Lake|3Xup3HSZLIQ|Bubble rock
It Was A Very Good Year|CJARjwzmceg|
Journey to Kilimanjaro|e0DpZ3WVowY|1994 Nova show.  Melodically simple but haunting music:  1:20, 4:15, 8:10, 12:03, 19:40, 22:08, 36:50, 38:46, *39:34, 44:58, 51:57, 54:15 (credits)
Judy Blue Eyes|XWvw_uZPGDA|2012
Judy Blue Eyes|cMJug2iz3NA|1969
Jumpin' Jack Flash|-rIG2POqtV8|
Kisses Sweeter Than Wine|iulmZAz8XfY|
Kodachrome|8rlDTK6QI-w|
Korobushka|E5NByiEIbD8|Bond live at Albert Hall
Korobushka|Pr3ZgN8onRA|Mikhail Smirnov
Korobushka|vvC2vjtmUX8|Bond live at Albert Hall
Lady Bird|FIPQVpw-zkk|
Land Down Under|8jHXu86O01w|
Light My Fire|LY1l8T2Lcl0|
Listen To Your Heart|yCC_b5WHLX0|
Long Cool Woman|X3sU_q1GH-4|
Love Me With All Your Heart|k3nfqH4YDDM|
Love is Blue|YYf_hb-jsGo|
MTA|MbtkL5_f6-4|
MacArthur Park|iplpKwxFH2I|
Mack the Knife|SEllHMWkXEU|
Maggie May|EOl7dh7a-6g|
Magnificent Seven (1960)|8XDB7GMnbUQ|
Mambo Italiano|9prJXEhNhPA|
Me & Bobby McGee|WXV_QjenbDw|
Memories (from Cats)|5mlllRdIfqw|Betty Buckley
Memories (from Cats)|MWoQW-b6Ph8|Streisand
Memories (from Cats)|mdBVJbzkoqo|Elaine Paige
Midnight In Moscow|FY3Zr5Tj5zw|2011
Moody Blues:  Blue World|8a9bfvNuTw0|With lyrics
Moody Blues:  Blue World|oosjl8wNLJU|
Moody Blues:  I'm Just A Singer in a Rock And Roll Band|5UZWXE76ELU|Album
Moody Blues:  I'm Just a Singer in a Rock and Roll Band|s5tb25TqXYU|Concert
Moody Blues:  Isn't Life Strange|9WZZjXgJ4W8|
Moody Blues:  Ride My See-saw|GXHMTuoK060|
Moody Blues:  Your Wildest Dreams|kmmPFrkuPq0|
Moonlight Sonata (3rd)|o6rBK0BqL2w|17 year old girl (Tina S)
Moonlight Sonata (3rd)|zucBfXpCA6s|Valentina Lisitsa
Morningtown Ride|M-RkC6MYT2E|1964
Morningtown Ride|wqdaCOt51Dk|2014
Mr. Roboto|51ybp_YFo7I|
Mrs. Robinson|_C2vqI9FVwg|
New World Symphony (Dvorak's 9th 1893)|VuaTY3zHO8Q|London Symphony Orchestra
New World Symphony and The Moldau|Qut5e3OfCvg|Slovak Philharmonic
North to Alaska (1960)|RO6IU9RpjS8|
Nothing Else Matters|8KK0-9Moz5Q| Hammered dulcimer
Nothing Else Matters|KSSa0-oAnIo| PMJ:  15 year old girl singer
Nothing Else Matters|tAGnKpE4NCI|
Old Man|rAtDrFdomN4|
One|UiKcd7yPLdU|
Paint It Black|O4irXQhgMqg|
Papa Was a Rollin' Stone|71l85z2bXAs|
Paperback Writer|yYvkICbTZIQ|
Papillon|Js69DkyaDVQ|
Patricia|rTXIXkeWnEo|
Paul McCartney carpool karaoke|QjvzCTqkBDQ|
Penny Lane|S-rB0pHI9fU|
People|fPlQ6EtArSc|
Pirates of the Caribbean|27mB8verLK8|
Pirates of the Caribbean|6zTc2hD2npA|Auckland Symphony
Popcorn Song|DBYjZTdrJlA|
Purple People Eater|Rx47qrH1GRs|
Push It To The Limit|9D-QD_HIfjA|
Question|tmOZFAYeurY|
Rainy Days and Monday|PjFoQxjgbrs|
Rainy Night in Georgia|bDRbF80NKDU|
Rawhide|_EjbzCX3enA|
Rocket Man|BdEe5SpdIuo|
Run Through The Jungle|EbI0cMyyw_M|
Sally:  Gypsy Waltz|eDGE6ah-e4Y|
Sally:  Orange Blossom Special|6-5xPixiCkI|
Sally:  Sally Goodin|nbYBBeylfGk|
Sally:  Unknown song|ob44BR1Hurg|
Scarborough Fair|-BakWVXHSug|
Scheherezade|1i6TsIVKByM|Excellent youth orchestra
She Works Hard for the Money|09ZSKE38lTU|
She's Got You|7nXPQbKZBbw|Petersens
Silver Threads and Golden Needles|uz6HB9HYQz4|Dusty Springfield
Sounds of Silence|4zLfCnGVeL4|
Stairway to Heaven|2cZ_EFAmj08| Heart at Kennedy Center; great production
Struttin' With Some Barbecue|yl-2R_Pb7dk|
Summer Wine|Ib_eW9VSUwM|
Sunrise, Sunset (Mantovani)|EzEHI1alPZ8|
Sunrise, Sunset|lRsciuPOWW4|
Superstar|SJmmaIGiGBg|
Suzy Q|7x60p7UNLnQ|
Sweet Dreams|qeMFqkcPYcg|
Take Five|vmDDOFXSgAs|
The Ballad Of Cat Ballou|Sw16X_9XtuE|
The Boxer|C1VUWDcp5Sg|
The Crystal Ship|bU1sLx1tjPY|
The Little Nash Rambler|enqNl7tdLR4|
The Night They Drove Old Dixie Down|wanJQC5KAfo|
The Night the Lights Went Out in Georgia|wMD5nBcPrCk|
The Thrill is Gone|Nu4tjTyqbho|
The Voice|-umqM9R8cnI|
The Wreck of the Edmund Fitzgerald|9vST6hVRj2A|
Theme From Shaft|Q429AOpL_ds|
These Boots Are Made for Walkin'|rypT2qMO1RY|
They Call the Wind Mariah|ByqYEzugleE|Harve Presnell
This is a Man's World|mPimt0Zu_To|PMJ with woman singer
This is a Man's World|wd1-HM234DE|James Brown 1960's
Those Were The Days|y3KEhWTnWvE|
Time Won't Let Me|3yQERVphWhY|
Toccata and Fugue in D Minor|JL0PCLMSQms|Violin
Toccata and Fugue in D Minor|_Cst9lV5PPg|Brass
Toccata and Fugue in D Minor|eDFFUIGoBUc|Accordion
Toccata and Fugue in D Minor|ho9rZjlsyYY|Organ
Toccata and Fugue in D Minor|i9UQ61EbdO0|Orchestra
Toccata and Fugue in D Minor|ipzR9bhei_o|Organ with bar graph score
Toccata and Fugue in D Minor|oPmKRtWta4E|Harp (a masterpiece)
Toccata and Fugue in D Minor|ojBYW3ycVTE|Guitar
Toccata and Fugue in D Minor|zhH53UODLEM|Piano with visual score
Today (1964)|3cELsUMcQdc|
Torn Between Two Lovers|TzGbvTl4mpg|
Total Eclipse of the Heart|lcOxhH8N3Bo|
Tuxedo Junction|iBTYcqtaOjg|
Two Faces Have I|w05w1XbZTG8|
Unchained Melody|zrK5u5W8afc|
Unforgettable|Fy_JRGjc1To|
Unsquare Dance|lbdEzRfbeH4|
Victory|j3nBuwOPu8A&list=RDE5NByiEIbD8| Bond
Volga Boatmen|0tw3g88JtWA|Leonid Kharitonov 1965
Volga Boatmen (1866)|qsovBF4N27Q|
Walk On the Wild Side|5O82y59h7MI|
Washington Square|ihenbyTzQ2A|
White Rabbit|EUY2kJE0AZE|
White Silver Sands|mOqbjENGN7s|First 45 rpm record I ever bought in 1957
Who's on First|kTcRRaXV-fg|Genius comedy
Woman in Love|hQLGCX8D-1Y|
Yesterday when I was young|GQIAcztYjbc|
You Only Live Twice|XgFtQPgHyek|
You Were On My Mind|c7YSANg8vgw|
You're So Vain|cleCtBP0o5Y|
My Sweet Lord|AR4lpQWcT5g|

'''

def Print(lst):
    link = "https://www.youtube.com/watch?v="
    song_list = []
    for line in lst.split("\n"):
        line = line.strip()
        if not line or line[0] == "#":
            continue
        f = [i.strip() for i in line.split("|")]
        f[1] = link + f[1]
        song_list.append(f)
    for f in sorted(song_list):
        print(f"[{f[0]}]({f[1]}) {f[2]} <br>")

if __name__ == "__main__": 
    print(f"<p>{time.asctime()}</p><p>Favorites:</p>")
    Print(favorites)
    print(f"<p>Others:</p>")
    Print(songs)
 
# vim: wm=0
