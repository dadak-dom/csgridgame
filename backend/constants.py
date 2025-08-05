import os
from dotenv import load_dotenv

load_dotenv()

# Database connection details
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),   # Change to your MySQL host
    "user": os.getenv("DB_USER"),        # Change to your MySQL username
    "password": os.getenv("DB_PASS"), # Change to your MySQL password
    "database": os.getenv("DB_NAME")   # Change to your database name
}

'''
    Parser rules breakdown:
    under [NUM]= all prices must be under specified [NUM]
    over = '' over price (same as above)
    has [PROP]= one of the elements of a list must be equal to [PROP] - diffent from IS because it expects a list
    is [PROP]= strings are equal (e.g. the value of a query would return it) - expects a string, compares the two
    canbe [PROP] = PROP expected to be true
    cannotbe [PROP] = PROP expected to be false
    equals [VALUE] = float, expected to be equal to value
    startswith [LETTER]= like '[letter]%'
'''
LANGUAGE = {
    'PRICE' : {
        'under' : 'Price under ',
        'over' : 'Price over ',
    },
    'STARTSWITH' : {
        'startswith' : 'Name starts with '
    },
    'COLOR' : {
        'has' : "Has the color "
    },
    'WEAPON' : {
        'is' : 'For the '
    },
    'RARITY' : {
        'is' : 'Rarity is '
    },
    'FINISH' : {
        'is' : 'Skin finish: '
    },
    'STATTRAK' : {
        # 'canbe' : 'Can be StatTrak',
        # 'cannotbe' : 'Cannot be StatTrak',
        'canbe' : 'Can be ',
        'cannotbe' : 'Cannot be '
    },
    'SOUVENIR' : {
        # 'canbe' : 'Can be Souvenir',
        # 'cannotbe' : 'Cannot be Souvenir'
        'canbe' : 'Can be ',
        'cannotbe' : 'Cannot be '
    },
    'FLAVOR_TEXT' : {
        'canbe' : 'Has flavor text',
        'cannotbe' : 'Doesn\'t have flavor text',
    },
    'VALVE' : {
        'canbe' : 'Made by',
        'cannotbe' : 'Not made by',
    },
    'MINWEAR' : {
        'equals' : 'Min. float is ',
        'over' : 'Min. float greater than ',
        'under' : 'Min. float less than ',
    },
    'MAXWEAR' : {
        'equals' : 'Max. float is ',
        'over' : 'Max. float greater than ', 
        'under' : 'Max. float less than ',
    },
    'YEAR' : {
        'equals' : 'Released in ',
    }
}

QUESTIONS = {
    'PRICE' : [
        'under 1',
        # 'under 10',
        # 'over 10',
        # 'under 50',
        'over 50',
        # 'under 100',
        'over 100',
        # 'over 1000',
    ],
    'STARTSWITH' : [
        'startswith C',
        'startswith B',
        'startswith A',
        'startswith D',
        'startswith E',
        'startswith F',
        'startswith P',
    ],
    'COLOR' : [
        # 'has green',
        # 'has blue',
        'has red',
        # 'has yellow',
        'has purple',
    ],
    'WEAPON' : [
        "is AK-47",
        "is AUG",
        "is AWP",
        "is CZ75-Auto",
        "is Desert-Eagle",
        "is Dual-Berettas",
        "is FAMAS",
        "is Five-SeveN",
        "is G3SG1",
        "is Galil-AR",
        "is Glock-18",
        "is M249",
        "is M4A1-S",
        "is M4A4",
        "is MAC-10",
        "is MAG-7",
        "is MP5-SD",
        "is MP7",
        "is MP9",
        "is Negev",
        "is Nova",
        "is P2000",
        "is P250",
        "is PP-Bizon",
        "is R8-Revolver",
        "is Sawed-Off",
        "is SCAR-20",
        "is SG-553",
        "is SSG-08",
        "is Tec-9",
        "is UMP-45",
        "is USP-S",
        "is XM1014"
    ],
    # 'WEAPON_CAT' : [ # I'm gonna keep knives out for now... maybe add them later?
    #     "is Rifle",
    #     "is Sniper-Rifle",
    #     "is Pistol",
    #     "is Machine-Gun",
    #     "is SMG",
    #     "is Shotgun"

    # ],
    'RARITY' : [
        # 'is consumer',
        # 'is industrial',
        # 'is mil-spec',
        # 'is restricted',
        'is classified',
        'is covert',
    ],
    'FINISH' : [
        'is custom',
        'is hydro',
        'is patina',
        'is anomulti',
        'is spray',
        'is ano',
        'is solid',
        'is anoair',
        'is gunsmith',  
    ],
    'STATTRAK' : [
        # 'canbe stattrak',
        'cannotbe stattrak',
    ],
    'SOUVENIR' : [
        # 'canbe souvenir',
        'cannotbe souvenir',
    ],
    'FLAVOR_TEXT' : [
        # 'canbe flavor',
        'cannotbe flavor',
    ],
    'VALVE' : [
        'canbe valve',
        'cannotbe valve',
    ],
    'MINWEAR' : [
        'equals 0',
        # 'over 0',
        'over 0.1',
        # 'over 0.2',
        # 'under 0.1',
    ],
    'MAXWEAR' : [
        'equals 1',
        # 'under 1',
        'under 0.5',
    ],
    'YEAR' : [
        'equals 2024',
        'equals 2023',
        'equals 2022',
        'equals 2021',
        'equals 2020',
        'equals 2019',
        'equals 2018',
        'equals 2017',
        'equals 2016',
        'equals 2015',
        'equals 2014',
        'equals 2013',                
    ]
}
    
VAR_MAPPING = {
    'PRICE' : 'prices',
    'COLOR' : 'colors',
    'WEAPON' : 'weapon',
    'WEAPON_CAT': 'weapon_category',
    'RARITY' : 'rarity',
    'FINISH' : 'finish',
    'STATTRAK' : 'stattrak',
    'SOUVENIR' : 'souvenir',
    'FLAVOR_TEXT' : 'flavor_text',
    'VALVE' : 'by_valve',
    'MINWEAR' : 'minwear',
    'MAXWEAR' : 'maxwear',
    'YEAR' : 'year_added',
    'STARTSWITH' : 'skin_name',
}

VALUE_MAPPING = {
    'consumer' : 'Consumer Grade',
    'industrial' : 'Industrial Grade',
    'mil-spec' : 'Mil-Spec',
    'restricted' : "Restricted",
    'classified' : 'Classified',
    'covert' : 'Covert',
    'custom' : 'Custom Paint Job',
    'hydro' : 'Hydrographic',
    'patina' : 'Patina',
    'anomulti' : 'Anodized Multicolored',
    'spray' : 'Spray-Paint',
    'ano' : 'Anodized',
    'solid' : 'Solid Color',
    'anoair' : 'Anodized Airbrushed',
    'gunsmith' : 'Gunsmith',
    'Desert-Eagle' : 'Desert Eagle',
    'Dual-Berettas' : 'Dual Berettas',
    'Galil-AR' : 'Galil AR',
    'R8-Revolver' : 'R8 Revolver',
    'SG-553' : 'SG 553',
    'SSG-08' : 'SSG 08',
    'Sniper-Rifle' : 'Sniper Rifle',
    'Machine-Gun' : 'Machine Gun',
}
