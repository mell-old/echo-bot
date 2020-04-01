from telebot.types import ReplyKeyboardMarkup
from telebot.types import KeyboardButton
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

BUTTON_INFO = 'Детальніше про Flugtag'
BUTTON_CHALLENGE = 'Challange'

def get_base_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(BUTTON_INFO),KeyboardButton(BUTTON_CHALLENGE))
    return markup

# INLINE CALLBACKS FOR BUTTON

CALLBACK_BUTTON_INFO = 'callback_button1_info'
CALLBACK_BUTTON_VIDEO = 'callback_button1_video'
CALLBACK_BUTTON_SEND = 'callback_button1_send'
CALLBACK_BUTTON_VIEWER = 'callback_button_viewer'

# INLINE KEYBOARD FOR CHALLENGE

CALLBACK_BUTTON_ONE = 'callback_button_one'
CALLBACK_BUTTON_TWO = 'callback_button_two'

# INLINE KEYBOARD FOR REGULATIONS

CALLBACK_BUTTON_SECURITY =  'callback_button_security'
CALLBACK_BUTTON_BUILD = 'callback_button_build'
CALLBACK_BUTTON_TEAMS = 'callback_button_teams'

CALLBACK_BUTTON_BACK_INFO = 'callback_button_back_info'

# titles for inline button

TITLES = {
    CALLBACK_BUTTON_INFO: 'Що таке RedBull Flugtag?',
    CALLBACK_BUTTON_VIDEO: 'Як це було в 2013?',
    CALLBACK_BUTTON_SEND: 'Хочу прийняти участь',
    CALLBACK_BUTTON_VIEWER: 'Хочу бути глядачем!',
    CALLBACK_BUTTON_ONE: '1. #некласичнийкостюм',
    CALLBACK_BUTTON_TWO: '2. #самсобідавінчі',
    CALLBACK_BUTTON_SECURITY: '1. Безпека',
    CALLBACK_BUTTON_BUILD: '2. Будівництво',
    CALLBACK_BUTTON_TEAMS: '3. Команди'
}

def get_inline_keyboard_info():
    markup = InlineKeyboardMarkup(row_width=1)
    info_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_INFO], callback_data=CALLBACK_BUTTON_INFO)
    video_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_VIDEO], callback_data=CALLBACK_BUTTON_VIDEO)
    send_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_SEND], url='https://bit.ly/flugtagregistrations') #callback_data=CALLBACK_BUTTON_SEND)
    viewer_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_VIEWER], url='https://bit.ly/facebookFlugtag')
    markup.add(info_btn, video_btn, send_btn, viewer_btn)
    return markup

def get_inline_keyboard_challenge():
    markup = InlineKeyboardMarkup(row_width=1)
    one_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_ONE], callback_data=CALLBACK_BUTTON_ONE)
    two_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_TWO], callback_data=CALLBACK_BUTTON_TWO)
    markup.add(one_btn,two_btn)
    return markup

def get_inline_keyboard_regulations():
    markup = InlineKeyboardMarkup(row_width=1)
    security_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_SECURITY], callback_data=CALLBACK_BUTTON_SECURITY)
    build_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_BUILD], callback_data=CALLBACK_BUTTON_BUILD)
    teams_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_TEAMS], callback_data=CALLBACK_BUTTON_TEAMS)
    back_btn = InlineKeyboardButton('Повернутись назад', callback_data=CALLBACK_BUTTON_BACK_INFO)
    markup.add(security_btn, build_btn, teams_btn, back_btn)
    return markup

# INLINE KEYBOARD FOR ADMIN
ADMIN_CALLBACK = [
    'callback_button1_info_res',
    'callback_button1_video_res',
    'callback_button1_send_res',
    'callback_button_one_res',
    'callback_button_two_res',
    'callback_button_security_res',
    'callback_button_build_res',
    'callback_button_teams_res'
]


def get_inline_keyboard_admin():
    markup = InlineKeyboardMarkup(row_width=2)
    info_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_INFO], callback_data=ADMIN_CALLBACK[0])
    video_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_VIDEO], callback_data=ADMIN_CALLBACK[1])
    send_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_SEND], callback_data=ADMIN_CALLBACK[2]) # not using
    one_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_ONE], callback_data=ADMIN_CALLBACK[3])
    two_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_TWO], callback_data=ADMIN_CALLBACK[4])
    security_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_SECURITY], callback_data=ADMIN_CALLBACK[5])
    build_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_BUILD], callback_data=ADMIN_CALLBACK[6])
    teams_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_TEAMS], callback_data=ADMIN_CALLBACK[7])
    markup.add(info_btn, video_btn, one_btn, two_btn, security_btn, build_btn, teams_btn)
    return markup
