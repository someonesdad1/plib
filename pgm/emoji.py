_pgminfo = '''
<oo 
    Emojis used in github markdown
    Fri 03 Oct 2025 11:52:02 AM
    From https://gist.github.com/rxaviers/7360908 (Download ZIP button)
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat oo>
<oo test none oo>
<oo todo oo>
'''

if 1:  # Header
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from columnize import Columnize
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Data
    # emojis listed by category
    emoji = {
        "people":    '''
            bowtie smile laughing blush smiley relaxed smirk heart_eyes kissing_heart
            kissing_closed_eyes flushed relieved satisfied grin wink
            stuck_out_tongue_winking_eye stuck_out_tongue_closed_eyes grinning kissing
            kissing_smiling_eyes stuck_out_tongue sleeping worried frowning anguished
            open_mouth grimacing confused hushed expressionless unamused sweat_smile
            sweat disappointed_relieved weary pensive disappointed confounded fearful
            cold_sweat persevere cry sob joy astonished scream neckbeard tired_face
            angry rage triumph sleepy yum mask sunglasses dizzy_face imp smiling_imp
            neutral_face no_mouth innocent alien yellow_heart blue_heart purple_heart
            heart green_heart broken_heart heartbeat heartpulse two_hearts
            revolving_hearts cupid sparkling_heart sparkles star star2 dizzy boom
            collision anger exclamation question grey_exclamation grey_question zzz dash
            sweat_drops notes musical_note fire hankey poop shit +1 thumbsup -1
            thumbsdown ok_hand punch facepunch fist v wave hand raised_hand open_hands
            point_up point_down point_left point_right raised_hands pray point_up_2 clap
            muscle metal fu walking runner running couple family two_men_holding_hands
            two_women_holding_hands dancer dancers ok_woman no_good
            information_desk_person raising_hand bride_with_veil
            person_with_pouting_face person_frowning bow couplekiss couple_with_heart
            massage haircut nail_care boy girl woman man baby older_woman older_man
            person_with_blond_hair man_with_gua_pi_mao man_with_turban
            construction_worker cop angel princess smiley_cat smile_cat heart_eyes_cat
            kissing_cat smirk_cat scream_cat crying_cat_face joy_cat pouting_cat
            japanese_ogre japanese_goblin see_no_evil hear_no_evil speak_no_evil
            guardsman skull feet lips kiss droplet ear eyes nose tongue love_letter
            bust_in_silhouette busts_in_silhouette speech_balloon thought_balloon
            feelsgood finnadie goberserk godmode hurtrealbad rage1 rage2 rage3 rage4
            suspect trollface
            '''.split(),
        "nature":    '''
            sunny umbrella cloud snowflake snowman zap cyclone foggy ocean cat dog mouse
            hamster rabbit wolf frog tiger koala bear pig pig_nose cow boar monkey_face
            monkey horse racehorse camel sheep elephant panda_face snake bird baby_chick
            hatched_chick hatching_chick chicken penguin turtle bug honeybee ant beetle
            snail octopus tropical_fish fish whale whale2 dolphin cow2 ram rat
            water_buffalo tiger2 rabbit2 dragon goat rooster dog2 pig2 mouse2 ox
            dragon_face blowfish crocodile dromedary_camel leopard cat2 poodle
            paw_prints bouquet cherry_blossom tulip four_leaf_clover rose sunflower
            hibiscus maple_leaf leaves fallen_leaf herb mushroom cactus palm_tree
            evergreen_tree deciduous_tree chestnut seedling blossom ear_of_rice shell
            globe_with_meridians sun_with_face full_moon_with_face new_moon_with_face
            new_moon waxing_crescent_moon first_quarter_moon waxing_gibbous_moon
            full_moon waning_gibbous_moon last_quarter_moon waning_crescent_moon
            last_quarter_moon_with_face first_quarter_moon_with_face moon earth_africa
            earth_americas earth_asia volcano milky_way partly_sunny octocat squirrel
            '''.split(),
        "objects":    '''
            bamboo gift_heart dolls school_satchel mortar_board flags fireworks sparkler
            wind_chime rice_scene jack_o_lantern ghost santa christmas_tree gift bell
            no_bell tanabata_tree tada confetti_ball balloon crystal_ball cd dvd
            floppy_disk camera video_camera movie_camera computer tv iphone phone
            telephone telephone_receiver pager fax minidisc vhs sound speaker mute
            loudspeaker mega hourglass hourglass_flowing_sand alarm_clock watch radio
            satellite loop mag mag_right unlock lock lock_with_ink_pen
            closed_lock_with_key key bulb flashlight high_brightness low_brightness
            electric_plug battery calling email mailbox postbox bath bathtub shower
            toilet wrench nut_and_bolt hammer seat moneybag yen dollar pound euro
            credit_card money_with_wings e-mail inbox_tray outbox_tray envelope
            incoming_envelope postal_horn mailbox_closed mailbox_with_mail
            mailbox_with_no_mail door smoking bomb gun hocho pill syringe page_facing_up
            page_with_curl bookmark_tabs bar_chart chart_with_upwards_trend
            chart_with_downwards_trend scroll clipboard calendar date card_index
            file_folder open_file_folder scissors pushpin paperclip black_nib pencil2
            straight_ruler triangular_ruler closed_book green_book blue_book orange_book
            notebook notebook_with_decorative_cover ledger books bookmark name_badge
            microscope telescope newspaper football basketball soccer baseball tennis
            8ball rugby_football bowling golf mountain_bicyclist bicyclist horse_racing
            snowboarder swimmer surfer ski spades hearts clubs diamonds gem ring trophy
            musical_score musical_keyboard violin space_invader video_game black_joker
            flower_playing_cards game_die dart mahjong clapper memo pencil book art
            microphone headphones trumpet saxophone guitar shoe sandal high_heel
            lipstick boot shirt tshirt necktie womans_clothes dress
            running_shirt_with_sash jeans kimono bikini ribbon tophat crown womans_hat
            mans_shoe closed_umbrella briefcase handbag pouch purse eyeglasses
            fishing_pole_and_fish coffee tea sake baby_bottle beer beers cocktail
            tropical_drink wine_glass fork_and_knife pizza hamburger fries poultry_leg
            meat_on_bone spaghetti curry fried_shrimp bento sushi fish_cake rice_ball
            rice_cracker rice ramen stew oden dango egg bread doughnut custard icecream
            ice_cream shaved_ice birthday cake cookie chocolate_bar candy lollipop
            honey_pot apple green_apple tangerine lemon cherries grapes watermelon
            strawberry peach melon banana pear pineapple sweet_potato eggplant tomato
            corn
            '''.split(),
        "places":    '''
            house house_with_garden school office post_office hospital bank
            convenience_store love_hotel hotel wedding church department_store
            european_post_office city_sunrise city_sunset japanese_castle
            european_castle tent factory tokyo_tower japan mount_fuji
            sunrise_over_mountains sunrise stars statue_of_liberty bridge_at_night
            carousel_horse rainbow ferris_wheel fountain roller_coaster ship speedboat
            boat sailboat rowboat anchor rocket airplane helicopter steam_locomotive
            tram mountain_railway bike aerial_tramway suspension_railway
            mountain_cableway tractor blue_car oncoming_automobile car red_car taxi
            oncoming_taxi articulated_lorry bus oncoming_bus rotating_light police_car
            oncoming_police_car fire_engine ambulance minibus truck train station train2
            bullettrain_front bullettrain_side light_rail monorail railway_car
            trolleybus ticket fuelpump vertical_traffic_light traffic_light warning
            construction beginner atm slot_machine busstop barber hotsprings
            checkered_flag crossed_flags izakaya_lantern moyai circus_tent
            performing_arts round_pushpin triangular_flag_on_post jp kr cn us fr es it
            ru gb uk de corn
            '''.split(),
        "symbols":    '''
            one two three four five six seven eight nine keycap_ten 1234 zero hash
            symbols arrow_backward arrow_down arrow_forward arrow_left capital_abcd abcd
            abc arrow_lower_left arrow_lower_right arrow_right arrow_up arrow_upper_left
            arrow_upper_right arrow_double_down arrow_double_up arrow_down_small
            arrow_heading_down arrow_heading_up leftwards_arrow_with_hook
            arrow_right_hook left_right_arrow arrow_up_down arrow_up_small
            arrows_clockwise arrows_counterclockwise rewind fast_forward
            information_source ok twisted_rightwards_arrows repeat repeat_one new top up
            cool free ng cinema koko signal_strength u5272 u5408 u55b6 u6307 u6708 u6709
            u6e80 u7121 u7533 u7a7a u7981 sa restroom mens womens baby_symbol no_smoking
            parking wheelchair metro baggage_claim accept wc potable_water
            put_litter_in_its_place secret congratulations m passport_control
            left_luggage customs ideograph_advantage cl sos id no_entry_sign underage
            no_mobile_phones do_not_litter non-potable_water no_bicycles no_pedestrians
            children_crossing no_entry eight_spoked_asterisk eight_pointed_black_star
            heart_decoration vs vibration_mode mobile_phone_off chart currency_exchange
            aries taurus gemini cancer leo virgo libra scorpius sagittarius capricorn
            aquarius pisces ophiuchus six_pointed_star negative_squared_cross_mark a b
            ab o2 diamond_shape_with_a_dot_inside recycle end on soon clock1 clock130
            clock10 clock1030 clock11 clock1130 clock12 clock1230 clock2 clock230 clock3
            clock330 clock4 clock430 clock5 clock530 clock6 clock630 clock7 clock730
            clock8 clock830 clock9 clock930 heavy_dollar_sign copyright registered tm x
            heavy_exclamation_mark bangbang interrobang o heavy_multiplication_x
            heavy_plus_sign heavy_minus_sign heavy_division_sign white_flower 100
            heavy_check_mark ballot_box_with_check radio_button link curly_loop
            wavy_dash part_alternation_mark trident black_square white_square
            white_check_mark black_square_button white_square_button black_circle
            white_circle red_circle large_blue_circle large_blue_diamond
            large_orange_diamond small_blue_diamond small_orange_diamond
            small_red_triangle small_red_triangle_down shipit
        '''.split(),
    }
    if 0:   # Print out the data
        # The following are names that are not supported in pandoc 3.8
        remove = set('''
            bowtie neckbeard person_with_pouting_face person_frowning person_with_blond_hair
            feelsgood finnadie goberserk godmode hurtrealbad rage1 rage2 rage3 rage4 suspect
            trollface octocat squirrel black_square white_square shipit
        '''.split())
        for i in emoji:
            print(f"## {i}")
            for j in emoji[i]:
                if j in remove:
                    continue
                print(f"{j} :{j}:<br>")
        exit()
    if 1:   # Here's a list of the previous data rendered by Firefox 143.0.1
        FirefoxSymbols = '''
            :people
            smile 😄
            laughing 😆
            blush 😊
            smiley 😃
            relaxed ☺️
            smirk 😏
            heart_eyes 😍
            kissing_heart 😘
            kissing_closed_eyes 😚
            flushed 😳
            relieved 😌
            satisfied 😆
            grin 😁
            wink 😉
            stuck_out_tongue_winking_eye 😜
            stuck_out_tongue_closed_eyes 😝
            grinning 😀
            kissing 😗
            kissing_smiling_eyes 😙
            stuck_out_tongue 😛
            sleeping 😴
            worried 😟
            frowning 😦
            anguished 😧
            open_mouth 😮
            grimacing 😬
            confused 😕
            hushed 😯
            expressionless 😑
            unamused 😒
            sweat_smile 😅
            sweat 😓
            disappointed_relieved 😥
            weary 😩
            pensive 😔
            disappointed 😞
            confounded 😖
            fearful 😨
            cold_sweat 😰
            persevere 😣
            cry 😢
            sob 😭
            joy 😂
            astonished 😲
            scream 😱
            tired_face 😫
            angry 😠
            rage 😡
            triumph 😤
            sleepy 😪
            yum 😋
            mask 😷
            sunglasses 😎
            dizzy_face 😵
            imp 👿
            smiling_imp 😈
            neutral_face 😐
            no_mouth 😶
            innocent 😇
            alien 👽
            yellow_heart 💛
            blue_heart 💙
            purple_heart 💜
            heart ❤️
            green_heart 💚
            broken_heart 💔
            heartbeat 💓
            heartpulse 💗
            two_hearts 💕
            revolving_hearts 💞
            cupid 💘
            sparkling_heart 💖
            sparkles ✨
            star ⭐
            star2 🌟
            dizzy 💫
            boom 💥
            collision 💥
            anger 💢
            exclamation ❗
            question ❓
            grey_exclamation ❕
            grey_question ❔
            zzz 💤
            dash 💨
            sweat_drops 💦
            notes 🎶
            musical_note 🎵
            fire 🔥
            hankey 💩
            poop 💩
            shit 💩
            +1 👍
            thumbsup 👍
            -1 👎
            thumbsdown 👎
            ok_hand 👌
            punch 👊
            facepunch 👊
            fist ✊
            v ✌️
            wave 👋
            hand ✋
            raised_hand ✋
            open_hands 👐
            point_up ☝️
            point_down 👇
            point_left 👈
            point_right 👉
            raised_hands 🙌
            pray 🙏
            point_up_2 👆
            clap 👏
            muscle 💪
            metal 🤘
            fu 🖕
            walking 🚶
            runner 🏃
            running 🏃
            couple 👫
            family 👪
            two_men_holding_hands 👬
            two_women_holding_hands 👭
            dancer 💃
            dancers 👯
            ok_woman 🙆‍♀️
            no_good 🙅
            information_desk_person 💁
            raising_hand 🙋
            bride_with_veil 👰‍♀️
            bow 🙇
            couplekiss 💏
            couple_with_heart 💑
            massage 💆
            haircut 💇
            nail_care 💅
            boy 👦
            girl 👧
            woman 👩
            man 👨
            baby 👶
            older_woman 👵
            older_man 👴
            man_with_gua_pi_mao 👲
            man_with_turban 👳‍♂️
            construction_worker 👷
            cop 👮
            angel 👼
            princess 👸
            smiley_cat 😺
            smile_cat 😸
            heart_eyes_cat 😻
            kissing_cat 😽
            smirk_cat 😼
            scream_cat 🙀
            crying_cat_face 😿
            joy_cat 😹
            pouting_cat 😾
            japanese_ogre 👹
            japanese_goblin 👺
            see_no_evil 🙈
            hear_no_evil 🙉
            speak_no_evil 🙊
            guardsman 💂‍♂️
            skull 💀
            feet 🐾
            lips 👄
            kiss 💋
            droplet 💧
            ear 👂
            eyes 👀
            nose 👃
            tongue 👅
            love_letter 💌
            bust_in_silhouette 👤
            busts_in_silhouette 👥
            speech_balloon 💬
            thought_balloon 💭
            :nature
            sunny ☀️
            umbrella ☔
            cloud ☁️
            snowflake ❄️
            snowman ⛄
            zap ⚡
            cyclone 🌀
            foggy 🌁
            ocean 🌊
            cat 🐱
            dog 🐶
            mouse 🐭
            hamster 🐹
            rabbit 🐰
            wolf 🐺
            frog 🐸
            tiger 🐯
            koala 🐨
            bear 🐻
            pig 🐷
            pig_nose 🐽
            cow 🐮
            boar 🐗
            monkey_face 🐵
            monkey 🐒
            horse 🐴
            racehorse 🐎
            camel 🐫
            sheep 🐑
            elephant 🐘
            panda_face 🐼
            snake 🐍
            bird 🐦
            baby_chick 🐤
            hatched_chick 🐥
            hatching_chick 🐣
            chicken 🐔
            penguin 🐧
            turtle 🐢
            bug 🐛
            honeybee 🐝
            ant 🐜
            beetle 🪲
            snail 🐌
            octopus 🐙
            tropical_fish 🐠
            fish 🐟
            whale 🐳
            whale2 🐋
            dolphin 🐬
            cow2 🐄
            ram 🐏
            rat 🐀
            water_buffalo 🐃
            tiger2 🐅
            rabbit2 🐇
            dragon 🐉
            goat 🐐
            rooster 🐓
            dog2 🐕
            pig2 🐖
            mouse2 🐁
            ox 🐂
            dragon_face 🐲
            blowfish 🐡
            crocodile 🐊
            dromedary_camel 🐪
            leopard 🐆
            cat2 🐈
            poodle 🐩
            paw_prints 🐾
            bouquet 💐
            cherry_blossom 🌸
            tulip 🌷
            four_leaf_clover 🍀
            rose 🌹
            sunflower 🌻
            hibiscus 🌺
            maple_leaf 🍁
            leaves 🍃
            fallen_leaf 🍂
            herb 🌿
            mushroom 🍄
            cactus 🌵
            palm_tree 🌴
            evergreen_tree 🌲
            deciduous_tree 🌳
            chestnut 🌰
            seedling 🌱
            blossom 🌼
            ear_of_rice 🌾
            shell 🐚
            globe_with_meridians 🌐
            sun_with_face 🌞
            full_moon_with_face 🌝
            new_moon_with_face 🌚
            new_moon 🌑
            waxing_crescent_moon 🌒
            first_quarter_moon 🌓
            waxing_gibbous_moon 🌔
            full_moon 🌕
            waning_gibbous_moon 🌖
            last_quarter_moon 🌗
            waning_crescent_moon 🌘
            last_quarter_moon_with_face 🌜
            first_quarter_moon_with_face 🌛
            moon 🌔
            earth_africa 🌍
            earth_americas 🌎
            earth_asia 🌏
            volcano 🌋
            milky_way 🌌
            partly_sunny ⛅
            :objects
            bamboo 🎍
            gift_heart 💝
            dolls 🎎
            school_satchel 🎒
            mortar_board 🎓
            flags 🎏
            fireworks 🎆
            sparkler 🎇
            wind_chime 🎐
            rice_scene 🎑
            jack_o_lantern 🎃
            ghost 👻
            santa 🎅
            christmas_tree 🎄
            gift 🎁
            bell 🔔
            no_bell 🔕
            tanabata_tree 🎋
            tada 🎉
            confetti_ball 🎊
            balloon 🎈
            crystal_ball 🔮
            cd 💿
            dvd 📀
            floppy_disk 💾
            camera 📷
            video_camera 📹
            movie_camera 🎥
            computer 💻
            tv 📺
            iphone 📱
            phone ☎️
            telephone ☎️
            telephone_receiver 📞
            pager 📟
            fax 📠
            minidisc 💽
            vhs 📼
            sound 🔉
            speaker 🔈
            mute 🔇
            loudspeaker 📢
            mega 📣
            hourglass ⌛
            hourglass_flowing_sand ⏳
            alarm_clock ⏰
            watch ⌚
            radio 📻
            satellite 📡
            loop ➿
            mag 🔍
            mag_right 🔎
            unlock 🔓
            lock 🔒
            lock_with_ink_pen 🔏
            closed_lock_with_key 🔐
            key 🔑
            bulb 💡
            flashlight 🔦
            high_brightness 🔆
            low_brightness 🔅
            electric_plug 🔌
            battery 🔋
            calling 📲
            email 📧
            mailbox 📫
            postbox 📮
            bath 🛀
            bathtub 🛁
            shower 🚿
            toilet 🚽
            wrench 🔧
            nut_and_bolt 🔩
            hammer 🔨
            seat 💺
            moneybag 💰
            yen 💴
            dollar 💵
            pound 💷
            euro 💶
            credit_card 💳
            money_with_wings 💸
            e-mail 📧
            inbox_tray 📥
            outbox_tray 📤
            envelope ✉️
            incoming_envelope 📨
            postal_horn 📯
            mailbox_closed 📪
            mailbox_with_mail 📬
            mailbox_with_no_mail 📭
            door 🚪
            smoking 🚬
            bomb 💣
            gun 🔫
            hocho 🔪
            pill 💊
            syringe 💉
            page_facing_up 📄
            page_with_curl 📃
            bookmark_tabs 📑
            bar_chart 📊
            chart_with_upwards_trend 📈
            chart_with_downwards_trend 📉
            scroll 📜
            clipboard 📋
            calendar 📆
            date 📅
            card_index 📇
            file_folder 📁
            open_file_folder 📂
            scissors ✂️
            pushpin 📌
            paperclip 📎
            black_nib ✒️
            pencil2 ✏️
            straight_ruler 📏
            triangular_ruler 📐
            closed_book 📕
            green_book 📗
            blue_book 📘
            orange_book 📙
            notebook 📓
            notebook_with_decorative_cover 📔
            ledger 📒
            books 📚
            bookmark 🔖
            name_badge 📛
            microscope 🔬
            telescope 🔭
            newspaper 📰
            football 🏈
            basketball 🏀
            soccer ⚽
            baseball ⚾
            tennis 🎾
            8ball 🎱
            rugby_football 🏉
            bowling 🎳
            golf ⛳
            mountain_bicyclist 🚵
            bicyclist 🚴
            horse_racing 🏇
            snowboarder 🏂
            swimmer 🏊
            surfer 🏄
            ski 🎿
            spades ♠️
            hearts ♥️
            clubs ♣️
            diamonds ♦️
            gem 💎
            ring 💍
            trophy 🏆
            musical_score 🎼
            musical_keyboard 🎹
            violin 🎻
            space_invader 👾
            video_game 🎮
            black_joker 🃏
            flower_playing_cards 🎴
            game_die 🎲
            dart 🎯
            mahjong 🀄
            clapper 🎬
            memo 📝
            pencil 📝
            book 📖
            art 🎨
            microphone 🎤
            headphones 🎧
            trumpet 🎺
            saxophone 🎷
            guitar 🎸
            shoe 👞
            sandal 👡
            high_heel 👠
            lipstick 💄
            boot 👢
            shirt 👕
            tshirt 👕
            necktie 👔
            womans_clothes 👚
            dress 👗
            running_shirt_with_sash 🎽
            jeans 👖
            kimono 👘
            bikini 👙
            ribbon 🎀
            tophat 🎩
            crown 👑
            womans_hat 👒
            mans_shoe 👞
            closed_umbrella 🌂
            briefcase 💼
            handbag 👜
            pouch 👝
            purse 👛
            eyeglasses 👓
            fishing_pole_and_fish 🎣
            coffee ☕
            tea 🍵
            sake 🍶
            baby_bottle 🍼
            beer 🍺
            beers 🍻
            cocktail 🍸
            tropical_drink 🍹
            wine_glass 🍷
            fork_and_knife 🍴
            pizza 🍕
            hamburger 🍔
            fries 🍟
            poultry_leg 🍗
            meat_on_bone 🍖
            spaghetti 🍝
            curry 🍛
            fried_shrimp 🍤
            bento 🍱
            sushi 🍣
            fish_cake 🍥
            rice_ball 🍙
            rice_cracker 🍘
            rice 🍚
            ramen 🍜
            stew 🍲
            oden 🍢
            dango 🍡
            egg 🥚
            bread 🍞
            doughnut 🍩
            custard 🍮
            icecream 🍦
            ice_cream 🍨
            shaved_ice 🍧
            birthday 🎂
            cake 🍰
            cookie 🍪
            chocolate_bar 🍫
            candy 🍬
            lollipop 🍭
            honey_pot 🍯
            apple 🍎
            green_apple 🍏
            tangerine 🍊
            lemon 🍋
            cherries 🍒
            grapes 🍇
            watermelon 🍉
            strawberry 🍓
            peach 🍑
            melon 🍈
            banana 🍌
            pear 🍐
            pineapple 🍍
            sweet_potato 🍠
            eggplant 🍆
            tomato 🍅
            corn 🌽
            :places
            house 🏠
            house_with_garden 🏡
            school 🏫
            office 🏢
            post_office 🏣
            hospital 🏥
            bank 🏦
            convenience_store 🏪
            love_hotel 🏩
            hotel 🏨
            wedding 💒
            church ⛪
            department_store 🏬
            european_post_office 🏤
            city_sunrise 🌇
            city_sunset 🌆
            japanese_castle 🏯
            european_castle 🏰
            tent ⛺
            factory 🏭
            tokyo_tower 🗼
            japan 🗾
            mount_fuji 🗻
            sunrise_over_mountains 🌄
            sunrise 🌅
            stars 🌠
            statue_of_liberty 🗽
            bridge_at_night 🌉
            carousel_horse 🎠
            rainbow 🌈
            ferris_wheel 🎡
            fountain ⛲
            roller_coaster 🎢
            ship 🚢
            speedboat 🚤
            boat ⛵
            sailboat ⛵
            rowboat 🚣
            anchor ⚓
            rocket 🚀
            airplane ✈️
            helicopter 🚁
            steam_locomotive 🚂
            tram 🚊
            mountain_railway 🚞
            bike 🚲
            aerial_tramway 🚡
            suspension_railway 🚟
            mountain_cableway 🚠
            tractor 🚜
            blue_car 🚙
            oncoming_automobile 🚘
            car 🚗
            red_car 🚗
            taxi 🚕
            oncoming_taxi 🚖
            articulated_lorry 🚛
            bus 🚌
            oncoming_bus 🚍
            rotating_light 🚨
            police_car 🚓
            oncoming_police_car 🚔
            fire_engine 🚒
            ambulance 🚑
            minibus 🚐
            truck 🚚
            train 🚋
            station 🚉
            train2 🚆
            bullettrain_front 🚅
            bullettrain_side 🚄
            light_rail 🚈
            monorail 🚝
            railway_car 🚃
            trolleybus 🚎
            ticket 🎫
            fuelpump ⛽
            vertical_traffic_light 🚦
            traffic_light 🚥
            warning ⚠️
            construction 🚧
            beginner 🔰
            atm 🏧
            slot_machine 🎰
            busstop 🚏
            barber 💈
            hotsprings ♨️
            checkered_flag 🏁
            crossed_flags 🎌
            izakaya_lantern 🏮
            moyai 🗿
            circus_tent 🎪
            performing_arts 🎭
            round_pushpin 📍
            triangular_flag_on_post 🚩
            jp 🇯🇵
            kr 🇰🇷
            cn 🇨🇳
            us 🇺🇸
            fr 🇫🇷
            es 🇪🇸
            it 🇮🇹
            ru 🇷🇺
            gb 🇬🇧
            uk 🇬🇧
            de 🇩🇪
            corn 🌽
            :symbols
            one 1️⃣
            two 2️⃣
            three 3️⃣
            four 4️⃣
            five 5️⃣
            six 6️⃣
            seven 7️⃣
            eight 8️⃣
            nine 9️⃣
            keycap_ten 🔟
            1234 🔢
            zero 0️⃣
            hash #️⃣
            symbols 🔣
            arrow_backward ◀️
            arrow_down ⬇️
            arrow_forward ▶️
            arrow_left ⬅️
            capital_abcd 🔠
            abcd 🔡
            abc 🔤
            arrow_lower_left ↙️
            arrow_lower_right ↘️
            arrow_right ➡️
            arrow_up ⬆️
            arrow_upper_left ↖️
            arrow_upper_right ↗️
            arrow_double_down ⏬
            arrow_double_up ⏫
            arrow_down_small 🔽
            arrow_heading_down ⤵️
            arrow_heading_up ⤴️
            leftwards_arrow_with_hook ↩︎️
            arrow_right_hook ↪️
            left_right_arrow ↔︎️
            arrow_up_down ↕️
            arrow_up_small 🔼
            arrows_clockwise 🔃
            arrows_counterclockwise 🔄
            rewind ⏪
            fast_forward ⏩
            information_source ℹ️
            ok 🆗
            twisted_rightwards_arrows 🔀
            repeat 🔁
            repeat_one 🔂
            new 🆕
            top 🔝
            up 🆙
            cool 🆒
            free 🆓
            ng 🆖
            cinema 🎦
            koko 🈁
            signal_strength 📶
            u5272 🈹
            u5408 🈴
            u55b6 🈺
            u6307 🈯
            u6708 🈷️
            u6709 🈶
            u6e80 🈵
            u7121 🈚
            u7533 🈸
            u7a7a 🈳
            u7981 🈲
            sa 🈂️
            restroom 🚻
            mens 🚹
            womens 🚺
            baby_symbol 🚼
            no_smoking 🚭
            parking 🅿️
            wheelchair ♿
            metro 🚇
            baggage_claim 🛄
            accept 🉑
            wc 🚾
            potable_water 🚰
            put_litter_in_its_place 🚮
            secret ㊙️
            congratulations ㊗️
            m Ⓜ️
            passport_control 🛂
            left_luggage 🛅
            customs 🛃
            ideograph_advantage 🉐
            cl 🆑
            sos 🆘
            id 🆔
            no_entry_sign 🚫
            underage 🔞
            no_mobile_phones 📵
            do_not_litter 🚯
            non-potable_water 🚱
            no_bicycles 🚳
            no_pedestrians 🚷
            children_crossing 🚸
            no_entry ⛔
            eight_spoked_asterisk ✳️
            eight_pointed_black_star ✴️
            heart_decoration 💟
            vs 🆚
            vibration_mode 📳
            mobile_phone_off 📴
            chart 💹
            currency_exchange 💱
            aries ♈
            taurus ♉
            gemini ♊
            cancer ♋
            leo ♌
            virgo ♍
            libra ♎
            scorpius ♏
            sagittarius ♐
            capricorn ♑
            aquarius ♒
            pisces ♓
            ophiuchus ⛎
            six_pointed_star 🔯
            negative_squared_cross_mark ❎
            a 🅰️
            b 🅱️
            ab 🆎
            o2 🅾️
            diamond_shape_with_a_dot_inside 💠
            recycle ♻️
            end 🔚
            on 🔛
            soon 🔜
            clock1 🕐
            clock130 🕜
            clock10 🕙
            clock1030 🕥
            clock11 🕚
            clock1130 🕦
            clock12 🕛
            clock1230 🕧
            clock2 🕑
            clock230 🕝
            clock3 🕒
            clock330 🕞
            clock4 🕓
            clock430 🕟
            clock5 🕔
            clock530 🕠
            clock6 🕕
            clock630 🕡
            clock7 🕖
            clock730 🕢
            clock8 🕗
            clock830 🕣
            clock9 🕘
            clock930 🕤
            heavy_dollar_sign 💲
            copyright ©️
            registered ®️
            tm ™️
            x ❌
            heavy_exclamation_mark ❗
            bangbang ‼️
            interrobang ⁉️
            o ⭕
            heavy_multiplication_x ✖️
            heavy_plus_sign ➕
            heavy_minus_sign ➖
            heavy_division_sign ➗
            white_flower 💮
            100 💯
            heavy_check_mark ✔️
            ballot_box_with_check ☑️
            radio_button 🔘
            link 🔗
            curly_loop ➰
            wavy_dash 〰️
            part_alternation_mark 〽️
            trident 🔱
            white_check_mark ✅
            black_square_button 🔲
            white_square_button 🔳
            black_circle ⚫
            white_circle ⚪
            red_circle 🔴
            large_blue_circle 🔵
            large_blue_diamond 🔷
            large_orange_diamond 🔶
            small_blue_diamond 🔹
            small_orange_diamond 🔸
            small_red_triangle 🔺
            small_red_triangle_down 🔻
            '''
        symbols = {}
        for line in FirefoxSymbols.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line[0] == ":":
                if 0:
                    print(f"Group:  {line[1:]}")
            else:
                name, symbol = line.strip().split()
                symbols[name] = symbol
                # Note some of these "symbols" are actually two character strings.  Most
                # end in U+FE0F, the VARIATION SELECTOR-16.
                if 0:   # Print to screen
                    try:
                        print(f"{line!r} {hex(ord(symbol))} {chr(ord(symbol))}")
                    except TypeError:
                        print(f"{t.ornl}{line!r}{t.n}", end=" ")
                        for c in symbol:
                            print(f"{hex(ord(c))}({c})", end=" ")
                        print()
        if 0:
            for i in symbols:
                print(f"{i} {symbols[i]}")
            exit()
if 1:   # Utility
    def GetColors():
        t.stuff = t.lill
        t.err = t.redl
        t.dbg = t.lill if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Warn(*msg, status=1):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] regex1 [regex2...]
          Search for github markdown emojis supported by pandoc 3.8.  You can also list
          the categories (or print them all with "all"):
            people nature objects places symbols
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        GetColors()
        return args
if 1:   # Core functionality
    def PrintCategory(category):
        o = []
        for i in emoji[category]:
            try:
                o.append(f"{symbols[i]} {i}")
            except KeyError:
                pass
        for i in Columnize(o):
            print(i)
    def FindEmojis(regex):
        r = re.compile(regex, re.I)
        for i in symbols:
            mo = r.search(i)
            if mo:
                print(f"{i} {symbols[i]}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    for arg in args:
        if arg == "all":
            for arg in "people nature objects places symbols".split():
                t.print(f"{t.ornl}{arg}")
                PrintCategory(arg)
        elif arg in "people nature objects places symbols".split():
            PrintCategory(arg)
        else:
            FindEmojis(arg)
