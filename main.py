import telebot
from telebot import types
import urllib

from keyboard import ADMIN_CALLBACK, TITLES
from keyboard import get_base_reply_keyboard, get_inline_keyboard_challenge, get_inline_keyboard_info, get_inline_keyboard_admin, get_inline_keyboard_regulations
from keyboard import BUTTON_INFO, BUTTON_CHALLENGE, CALLBACK_BUTTON_INFO, CALLBACK_BUTTON_VIDEO, CALLBACK_BUTTON_SEND, CALLBACK_BUTTON_ONE, CALLBACK_BUTTON_TWO, CALLBACK_BUTTON_SECURITY, CALLBACK_BUTTON_BACK_INFO, CALLBACK_BUTTON_BUILD, CALLBACK_BUTTON_TEAMS
from db import add_callback, get_users_by_callback

from content import content

import datetime
from telegram.parsemode import ParseMode

from logger import new_logger

log = new_logger('bot')

bot = telebot.TeleBot(content['token'])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:  
        video = open('welcome.mp4', 'rb')
        log.info('Send video welcome')
        bot.send_video(
            message.chat.id,
            video,
            caption=content['msg']['welcome'],
            reply_markup=get_base_reply_keyboard()
        )
    except IOError: 
        log.info('Send message welcome')
        bot.send_message(
            message.chat.id,
            content['msg']['welcome'],
            reply_markup=get_base_reply_keyboard()
        )

@bot.message_handler(commands=['admin'])
def send_admin(message):
    log.info('Open admin panel by: {0}'.format(message.from_user.username))
    bot.send_message(
        message.chat.id,
        content['msg']['admin'],
        reply_markup=get_inline_keyboard_admin()
    )

@bot.message_handler(content_types=['text'])
def send_anytext(message):
    chat_id = message.chat.id
    if message.text == BUTTON_INFO:
        text = content['msg']['fgt']
        bot.send_message(chat_id, text, reply_markup=get_inline_keyboard_info())
    elif message.text == BUTTON_CHALLENGE:
        text = content['msg']['challenge'],
        bot.send_message(chat_id, text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_inline_keyboard_challenge())
    else:
        bot.send_message(chat_id, text='Немає відповіді на ваш текст, використовуй клавіатуру, щоб швидко знайти потрібну інформацію', reply_markup=get_base_reply_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    callback = call.data
    now = datetime.datetime.now()
    chat_id = call.message.chat.id
    current_text = call.message.text
    if callback in ADMIN_CALLBACK:
        new_callback = str(callback).split('_res')[0]
        (count, users) = get_users_by_callback(new_callback)
        btn_name = TITLES[new_callback]
        cout_text = ('Усього натисків на кнопку: {0}').format(count)
        users_text = ''.join('@{}\n'.format(str(x[0])) for x in users)
        text='Користувачі які написнули на кнопку "{0}":\n'.format(btn_name) + users_text + cout_text
        if text != current_text:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=call.message.message_id,
                parse_mode=ParseMode.MARKDOWN,
                text=text,
                reply_markup=get_inline_keyboard_admin()
            )
    else:
        log.debug('Add new callback: {0}'.format(callback))
        add_callback(call.from_user.username, callback)

        if callback == CALLBACK_BUTTON_INFO:
            text=content['info']['info']
            if text != current_text:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=call.message.message_id,
                    parse_mode=ParseMode.MARKDOWN,
                    text=text,
                    reply_markup=get_inline_keyboard_regulations()
                )
        if callback == CALLBACK_BUTTON_VIDEO:
            text=content['info']['video']
            if text != current_text:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=call.message.message_id,
                    parse_mode=ParseMode.MARKDOWN,
                    text=text,
                    reply_markup=get_inline_keyboard_info()
                )
        if callback == CALLBACK_BUTTON_SEND:
            text=content['info']['registration']
            if text != current_text:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=call.message.message_id,
                    parse_mode=ParseMode.MARKDOWN,
                    text=text,
                    reply_markup=get_inline_keyboard_info()
                )
        if callback == CALLBACK_BUTTON_ONE:
            text=content['info']['challenge_one']
            if text != current_text:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=call.message.message_id,
                    parse_mode=ParseMode.MARKDOWN,
                    text=text,
                    reply_markup=get_inline_keyboard_challenge()
                )
        if callback == CALLBACK_BUTTON_TWO:
            text=content['info']['challenge_two']
            if text != current_text:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=call.message.message_id,
                    parse_mode=ParseMode.MARKDOWN,
                    text=text,
                    reply_markup=get_inline_keyboard_challenge()
                )
        if callback == CALLBACK_BUTTON_SECURITY:
            text=content['regulations']['security']
            if text != current_text:
                bot.send_message(
                    chat_id=chat_id,
                    parse_mode=ParseMode.MARKDOWN,
                    text=text,
                    reply_markup=get_inline_keyboard_regulations()
                )
        if callback == CALLBACK_BUTTON_BUILD:
            text=content['regulations']['build']
            if text != current_text:
                bot.send_message(
                    chat_id=chat_id,
                    parse_mode=ParseMode.MARKDOWN,
                    text=text,
                    reply_markup=get_inline_keyboard_regulations()
                )
        if callback == CALLBACK_BUTTON_TEAMS:
            text=content['regulations']['teams']
            if text != current_text:
                bot.send_message(
                    chat_id=chat_id,
                    parse_mode=ParseMode.MARKDOWN,
                    text=text,
                    reply_markup=get_inline_keyboard_regulations()
                )
        if callback == CALLBACK_BUTTON_BACK_INFO:
            text = content['msg']['challenge'],
            if text != current_text:
                text = content['msg']['fgt']
                bot.send_message(chat_id, text, reply_markup=get_inline_keyboard_info())

if __name__ == '__main__':
    bot.polling(none_stop=True)