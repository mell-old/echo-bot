import telebot

from keyboard import ADMIN_CALLBACK, TITLES, TEST_BUTTONS
from keyboard import get_inline_keyboard_test_finish, get_inline_keyboard_test_start, get_base_reply_keyboard, get_inline_keyboard_challenge, get_inline_keyboard_info, get_inline_keyboard_admin, get_inline_keyboard_regulations, get_inline_keyboard_test
from keyboard import CALLBACK_BUTTON_BACK_TEST, CALLBACK_BUTTON_REGULATIONS, BUTTON_INFO, BUTTON_CHALLENGE, CALLBACK_BUTTON_INFO, CALLBACK_BUTTON_VIDEO, CALLBACK_BUTTON_ONE, CALLBACK_BUTTON_TWO, CALLBACK_BUTTON_SECURITY, CALLBACK_BUTTON_BACK_INFO, CALLBACK_BUTTON_BUILD, CALLBACK_BUTTON_TEAMS, CALLBACK_BUTTON_TEST
from db import add_callback, get_users_by_callback, init_db, get_count_by_user, add_user_to_test, update_count_by_user

from json_content import content
from json_content import test
from telegram.parsemode import ParseMode

from logger import new_logger

log = new_logger('bot')

init_db()

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
    username = message.from_user.username
    if message.text == BUTTON_INFO:
        text = content['msg']['fgt']
        add_callback(username, 'callback_info')
        bot.send_message(chat_id, text, reply_markup=get_inline_keyboard_info())
    elif message.text == BUTTON_CHALLENGE:
        text = content['msg']['challenge']
        add_callback(username, 'callback_challenge')
        bot.send_message(chat_id, text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_inline_keyboard_challenge())
    elif message.text == 'Перевір себе':
        text = content['test']
        add_callback(username, 'callback_test')
        bot.send_message(chat_id, text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_inline_keyboard_test_start())
    else:
        bot.send_message(chat_id, text='Немає відповіді на ваш текст, використовуй кнопки, щоб швидко знайти потрібну інформацію', reply_markup=get_base_reply_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    callback = call.data
    chat_id = call.message.chat.id
    current_text = call.message.text
    def send_message(current_text, text, keyboard):
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            parse_mode=ParseMode.MARKDOWN,
            text=current_text
        )
        bot.send_message(
            chat_id=chat_id,
            parse_mode=ParseMode.MARKDOWN,
            text=text,
            reply_markup=keyboard
        )
    if callback in ADMIN_CALLBACK:
        new_callback = str(callback).split('_res')[0]
        (count, users) = get_users_by_callback(new_callback)
        btn_name = TITLES[new_callback]
        cout_text = ('Усього натисків на кнопку: {0}').format(count)
        users_text = ''.join('@{}\n'.format(str(x[0])) for x in users)
        text='Користувачі які написнули на кнопку "{0}":\n{1}{2}'.format(btn_name, users_text, cout_text)
        print(text)
        if text != current_text:
            send_message(current_text=current_text, text=text, keyboard=get_inline_keyboard_admin())
    else:
        log.debug('Add new callback: {0}'.format(callback))
        username = call.from_user.username
        add_callback(username, callback)
        print(callback)    
        if callback == CALLBACK_BUTTON_REGULATIONS:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=call.message.message_id,
                    parse_mode=ParseMode.MARKDOWN,
                    text=current_text,
                    reply_markup=get_inline_keyboard_regulations(CALLBACK_BUTTON_BACK_TEST)
                )

        if callback == CALLBACK_BUTTON_BACK_TEST:
            send_message(current_text=current_text, text=current_text, keyboard=get_inline_keyboard_test_start())

        if callback == CALLBACK_BUTTON_INFO:
            text=content['info']['info']
            if text != current_text:
                send_message(current_text=current_text, text=text, keyboard=get_inline_keyboard_regulations(CALLBACK_BUTTON_BACK_INFO))
        
        if callback == CALLBACK_BUTTON_VIDEO:
            text='Відео не вдалось завантажити, ти можеш глянути його за посиланням:\n' + content['info']['video']
            if text not in current_text:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=call.message.message_id,
                    parse_mode=ParseMode.MARKDOWN,
                    text=current_text
                )
                try:  
                    video = open('what_flugtag.mp4', 'rb')
                    log.info('Send video welcome')
                    bot.send_video(
                        call.message.chat.id,
                        video
                    )
                    bot.send_message(
                        call.message.chat.id,
                        '☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️☝️\nТримай підбірку драйвого контенту',
                        reply_markup=get_inline_keyboard_info()
                    )
                except IOError: 
                    log.info('Send message welcome')
                    bot.send_message(
                        call.message.chat.id,
                        text,
                        reply_markup=get_inline_keyboard_info()
                    )
        # if callback == CALLBACK_BUTTON_SEND:
        #     text=content['info']['registration']
        #     if text != current_text:
        #         bot.edit_message_text(
        #             chat_id=chat_id,
        #             message_id=call.message.message_id,
        #             parse_mode=ParseMode.MARKDOWN,
        #             text=text,
        #             reply_markup=get_inline_keyboard_info()
        #         )

        if callback == CALLBACK_BUTTON_ONE:
            text=content['info']['challenge_one']
            if text != current_text:
                send_message(current_text=current_text, text=text, keyboard=get_inline_keyboard_challenge())
        
        if callback == CALLBACK_BUTTON_TWO:
            text=content['info']['challenge_two']
            if text != current_text:
                send_message(current_text=current_text, text=text, keyboard=get_inline_keyboard_challenge())
        
        if callback == CALLBACK_BUTTON_SECURITY:
            text=content['regulations']['security']
            if text != current_text:
                bot.send_message(
                    chat_id=chat_id,
                    parse_mode=ParseMode.MARKDOWN,
                    text=text,
                    reply_markup=get_inline_keyboard_regulations(CALLBACK_BUTTON_BACK_INFO)
                )
        
        if callback == CALLBACK_BUTTON_BUILD:
            text=content['regulations']['build']
            if text != current_text:
                bot.send_message(
                    chat_id=chat_id,
                    parse_mode=ParseMode.MARKDOWN,
                    text=text,
                    reply_markup=get_inline_keyboard_regulations(CALLBACK_BUTTON_BACK_INFO)
                )

        if callback == CALLBACK_BUTTON_TEAMS:
            text=content['regulations']['teams']
            if text != current_text:
                bot.send_message(
                    chat_id=chat_id,
                    parse_mode=ParseMode.MARKDOWN,
                    text=text,
                    reply_markup=get_inline_keyboard_regulations(CALLBACK_BUTTON_BACK_INFO)
                )

        if callback == CALLBACK_BUTTON_TEST:
            text = test[0]['quesion']
            add_user_to_test(username)
            send_message(current_text=current_text, text=text, keyboard=get_inline_keyboard_test(0))
        
        if callback == CALLBACK_BUTTON_BACK_INFO:
            text = content['msg']['challenge']
            if text != current_text:
                text = content['msg']['fgt']
                send_message(current_text=current_text, text=text, keyboard=get_inline_keyboard_info())
        
        if callback in TEST_BUTTONS:
            number, win, lose = get_count_by_user(username=username)
            next_quesion_number = number + 1
            print(number, win, lose, callback)
            current_content_test = test[number]
            answer = current_content_test['answer']
            current_msg = ''
            text_answer = '"{0}"'.format(current_content_test['buttons'][answer])
            if callback == answer:
                current_msg = '*Молодець!* Так тримати, твоя відповідь {0} правильна'.format(text_answer) 
                update_count_by_user(username, 'true')
            else:
                current_msg = 'Нажаль ти помилився. Правильна відповідь: {0}'.format(text_answer)
                update_count_by_user(username, 'false')
            if next_quesion_number >= 5:
                number, win, lose = get_count_by_user(username=username)
                finish_msg = 'Вітаю, ти закінчив випробування.\nОсь твої результати:\nПравильних відповідей: *{0}*\nНеправильних відповідей: *{1}*'.format(win, lose)
                send_message(current_text=current_msg, text=finish_msg, keyboard=get_inline_keyboard_test_finish())
            else:
                next_content_test = test[next_quesion_number]
                quesion = next_content_test['quesion']
                send_message(current_text=current_msg, text=quesion, keyboard=get_inline_keyboard_test(next_quesion_number))

if __name__ == '__main__':
    bot.polling(none_stop=True)