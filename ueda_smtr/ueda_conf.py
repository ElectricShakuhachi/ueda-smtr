CATEGORIES = ["solo", "duo", "trio", "more", "other", "strings"]
TEMPLATE_DIR = "templates"
LINE_LENGHT = 50 # check
FONTSIZE = 16
FONT_SPACING = 1
DIVIDER = 2
SPACE_ON_FIRST_EP = 20
SPACE_ON_OTHER_EP = 15
FILENAME_SPACER = "_"
MAPPINGS = {
    "price_mapping" : {
        200: "5,70",
        300: "6,60",
        400: "7,30",
        500: "8,00",
        600: "8,75",
        700: "9,50",
        800: "10,30"
    },
# the date mapping is incomplete - get back to this
    "date_mapping" : [
        (1980, {# at least 4.1980 5.1998
            "print" : "Kashimura Kazuichi",
            "print_location" : "Shimane-ken Hamada-shi Aioi-chō 1437",
            "rights" : "Ueda Kimio",
            "rights_loc" : "Ōsaka-fu Toyonaka-shi Hama 1-chōme-1-33",
            "payment_acc" : "52370"
        }),
        (1999, {# at least 9.1999
            "print" : "Kashimura Kazuichi",
            "print_location" : "Shimane-ken Hamada-shi Aioi-chō 3889",
            "rights" : "Ueda Kimio",
            "rights_loc" : "Ōsaka-fu Toyonaka-shi Hama 1-chōme-1-33",
            "payment_acc" : "52370"
        }),
        (2004, {# at least 9.2004 to 8.2006
            "print" : "Kashimura Kazuichi",
            "print_location" : "Shimane-ken Hamada-shi Aioi-chō 3889",
            "rights" : "Ueda Hōsei",
            "rights_loc" : "Ōsaka-fu Toyonaka-shi Hama 1-chōme-1-1",
            "payment_acc" : "00930-8-191019"
        }),
        (2012, {# at least 12.2012 to 9.2015
            "print" : "Kashimura Hideo",
            "print_location" : "Shimane-ken Hamada-shi Aioi-chō 3889",
            "rights" : "Ueda Hōsei",
            "rights_loc" : "Ōsaka-fu Toyonaka-shi Hama 1-chōme-1-1",
            "payment_acc" : "00930-8-191019"
        })
    ],
    "markings_mapping": {
        1: "Slow", # 徐
        2: "Very slow", # 緩
        3: "Slowing down", # 漸次徐
        4: "Speeding up", # 漸次速
        5: "Speeding up", # 徐々速
        6: "A bit heavily", # 稍重く
        7: "A bit lightly", # 淡泊に
        8: "Easy going, light", # 少し経快に
        9: "Note repeated by hitting 1st hole", # 一打
        10: "First part", # 第一部
        11: "Second part", # 第二部（赤）
        12: "Same pitch as 2nd part", # 替手合調
        13: "Same pitch as 1st part", # 本手合調（赤）
        14: "Instrumental section", # 手事
        15: "Second part (Kaete)", # 替手（赤）
        16: "Same pitch as previous section", # 前段と合調
        17: "Same pitch as next section", # 後段と合調
        18: "Silently", # 静かに
        19: "Lightheartedly, happily", # 心うれしく
        20: "3 counts long note", # 3 notes lenght under note
        21: "trioli", # trioli with regular 3
        22: "piano", # p
        23: "mezzoforte", # mf
        24: "forte", # f
        25: "forte fortissimo", # ff
        26: "fermata", # fermata
        27: "A bit fast", # 少早
        28: "Regular tempo", # 中唐？
        29: "TBD!!!", ########################################
        30: "diminuendo", # dim
        31: "TBD!!", # #######################################
        32: "Note repeated by hitting 5th hole", # 
        33: "trioli",  # trioli with 三 in kanji
        34: "A bit fast", # 小速
        35: "Daikan (third octave)", # 大甲
        36: "Repeat the previous notes", # ./.
        37: "Fast", # 速
        38: "Nayashi (start low and raise up to the nominal pitch)", # nayashi
        39: "Merikomi (start at nominal pitch, go down lower and back up)", # merikomi
        40: "Note repeated by hitting 3rd hole", # 三打
        41: "Note repeated by hitting 2nd and 4th holes", # 二四打
        42: "Note repeated by hitting 2nd hole", # 二打
        43: "Note repeated by hitting 1st and 3rd hole", # 一三打
        44: "Tamabuki (uvular trill / throat gargling)", # 玉吹き
        45: "Silent cold night", # 寒夜静寂
        46: "Hit finger hole", # 打
        47: "Late night snowfall", # 深夜降雪
        48: "Press third hole", # 三押
        49: "Bird cry at daybreak", # 黎明鳥聲
        50: "4 beats long note", # 4 notes lenght under note
        51: "Slide up", # スル
        52: "Karu (play note higher than nominal pitch)", # カル
        53: "The whiteness of snow", # 白雪皚々
        54: "Speeding up", # 漸次早く
        55: "Close 2nd hole instead of 3rd", # 二 beside レ
    }
}
INPUT_DIR = "input"
OUTPUT_DIR = "output"
