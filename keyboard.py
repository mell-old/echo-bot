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

# INLINE KEYBOARD FOR CHALLENGE

CALLBACK_BUTTON_ONE = 'callback_button_one'
CALLBACK_BUTTON_TWO = 'callback_button_two'

# titles for inline button

TITLES = {
    CALLBACK_BUTTON_INFO: 'Що таке RedBull Flugtag?',
    CALLBACK_BUTTON_VIDEO: 'Як це було в 2013?',
    CALLBACK_BUTTON_SEND: 'Хочу прийняти участь',
    CALLBACK_BUTTON_ONE: '1. Креативний костюм',
    CALLBACK_BUTTON_TWO: '2. Міні-літальний апарат',
}

def get_inline_keyboard_info():
    markup = InlineKeyboardMarkup(row_width=1)
    info_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_INFO], callback_data=CALLBACK_BUTTON_INFO)
    video_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_VIDEO], callback_data=CALLBACK_BUTTON_VIDEO)
    send_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_SEND], callback_data=CALLBACK_BUTTON_SEND)
    markup.add(info_btn, video_btn, send_btn)
    return markup

def get_inline_keyboard_challenge():
    markup = InlineKeyboardMarkup(row_width=1)
    one_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_ONE], callback_data=CALLBACK_BUTTON_ONE)
    two_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_TWO], callback_data=CALLBACK_BUTTON_TWO)
    markup.add(one_btn,two_btn)
    return markup

# INLINE KEYBOARD FOR ADMIN
ADMIN_CALLBACK = [
    'callback_button1_info_res',
    'callback_button1_video_res',
    'callback_button1_send_res',
    'callback_button_one_res',
    'callback_button_two_res'
]


def get_inline_keyboard_admin():
    markup = InlineKeyboardMarkup(row_width=2)
    info_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_INFO], callback_data=ADMIN_CALLBACK[0])
    video_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_VIDEO], callback_data=ADMIN_CALLBACK[1])
    send_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_SEND], callback_data=ADMIN_CALLBACK[2])
    one_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_ONE], callback_data=ADMIN_CALLBACK[3])
    two_btn = InlineKeyboardButton(TITLES[CALLBACK_BUTTON_TWO], callback_data=ADMIN_CALLBACK[4])
    markup.add(info_btn,video_btn,send_btn, one_btn, two_btn)
    return markup
