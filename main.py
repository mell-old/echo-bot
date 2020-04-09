import telebot

from keyboard import ADMIN_CALLBACK, TITLES, TEST_BUTTONS
from keyboard import get_inline_keyboard_test_finish, get_inline_keyboard_test_start, get_base_reply_keyboard, get_inline_keyboard_challenge, get_inline_keyboard_info, get_inline_keyboard_admin, get_inline_keyboard_regulations, get_inline_keyboard_test
from keyboard import CALLBACK_BUTTON_BACK_TEST, CALLBACK_BUTTON_REGULATIONS, BUTTON_INFO, BUTTON_CHALLENGE, CALLBACK_BUTTON_INFO, CALLBACK_BUTTON_VIDEO, CALLBACK_BUTTON_ONE, CALLBACK_BUTTON_TWO, CALLBACK_BUTTON_SECURITY, CALLBACK_BUTTON_BACK_INFO, CALLBACK_BUTTON_BUILD, CALLBACK_BUTTON_TEAMS, CALLBACK_BUTTON_TEST
from db import add_callback, add_user_to_test, get_count_by_user_id, get_users_by_callback, init_db, update_count_by_user_id

from json_content import content
from json_content import test
from telegram.parsemode import ParseMode

from logger import new_logger

log = new_logger('bot')

init_db(True)

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
    user_id = message.from_user.id
    if message.text == BUTTON_INFO:
        text = content['msg']['fgt']
        add_callback(user_id, username, 'callback_info')
        bot.send_message(chat_id, text, reply_markup=get_inline_keyboard_info())
    elif message.text == BUTTON_CHALLENGE:
        text = content['msg']['challenge']
        add_callback(user_id, username, 'callback_challenge')
        bot.send_message(chat_id, text, parse_mode=ParseMode.HTML, reply_markup=get_inline_keyboard_challenge())
    elif message.text == 'Перевір себе':
        text = content['test']
        add_callback(user_id, username, 'callback_test')
        bot.send_message(chat_id, text, parse_mode=ParseMode.HTML, reply_markup=get_inline_keyboard_test_start())
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
            parse_mode=ParseMode.HTML,
            text=current_text
        )
        bot.send_message(
            chat_id=chat_id,
            parse_mode=ParseMode.HTML,
            text=text,
            reply_markup=keyboard
        )
    def send_photo(current_caption, photo, caption, keyboard):
        bot.edit_message_caption(
            chat_id=chat_id,
            message_id=call.message.message_id,
            parse_mode=ParseMode.HTML,
            caption=current_caption
        )
        bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            parse_mode=ParseMode.HTML,
            caption=caption,
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
        user_id = call.from_user.id
        add_callback(user_id, username, callback)
        print(callback)    
        if callback == CALLBACK_BUTTON_REGULATIONS:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=call.message.message_id,
                    parse_mode=ParseMode.HTML,
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
                    parse_mode=ParseMode.HTML,
                    text='Завантаження...'
                )
                try:  
                    video1 = open('what_flugtag_1.mp4', 'rb')
                    video2 = open('what_flugtag_2.mp4', 'rb')
                    log.info('Send video welcome')
                    bot.send_video(
                        call.message.chat.id,
                        video1
                    )
                    bot.send_video(
                        call.message.chat.id,
                        video2
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
        #             parse_mode=ParseMode.HTML,
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
                    parse_mode=ParseMode.HTML,
                    text=text,
                    reply_markup=get_inline_keyboard_regulations(CALLBACK_BUTTON_BACK_INFO)
                )
        
        if callback == CALLBACK_BUTTON_BUILD:
            text=content['regulations']['build']
            if text != current_text:
                bot.send_message(
                    chat_id=chat_id,
                    parse_mode=ParseMode.HTML,
                    text=text,
                    reply_markup=get_inline_keyboard_regulations(CALLBACK_BUTTON_BACK_INFO)
                )

        if callback == CALLBACK_BUTTON_TEAMS:
            text=content['regulations']['teams']
            if text != current_text:
                bot.send_message(
                    chat_id=chat_id,
                    parse_mode=ParseMode.HTML,
                    text=text,
                    reply_markup=get_inline_keyboard_regulations(CALLBACK_BUTTON_BACK_INFO)
                )

        if callback == CALLBACK_BUTTON_TEST:
            text = test[0]['quesion']
            add_user_to_test(user_id, username)
            photo = open('vic0.jpg', 'rb')
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=call.message.message_id,
                parse_mode=ParseMode.HTML,
                text=current_text
            )
            bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                parse_mode=ParseMode.HTML,
                caption=text,
                reply_markup=get_inline_keyboard_test(0)
            )
        
        if callback == CALLBACK_BUTTON_BACK_INFO:
            text = content['msg']['challenge']
            if text != current_text:
                text = content['msg']['fgt']
                send_message(current_text=current_text, text=text, keyboard=get_inline_keyboard_info())
        
        if callback in TEST_BUTTONS:
            number, win, lose = get_count_by_user_id(user_id)
            next_quesion_number = number + 1
            print(number, win, lose, callback)
            current_content_test = test[number]
            answer = current_content_test['answer']
            current_msg = ''
            text_answer = '"{0}"'.format(current_content_test['buttons'][answer])
            if callback == answer:
                current_msg = '<b>Молодець!</b> Так тримати, твоя відповідь {0} правильна'.format(text_answer) 
                update_count_by_user_id(user_id, 'true')
            else:
                current_msg = 'Нажаль ти помилився. Правильна відповідь: {0}'.format(text_answer)
                update_count_by_user_id(user_id, 'false')
            if next_quesion_number >= 5:
                number, win, lose = get_count_by_user_id(user_id)
                photo = open('finish.jpg'.format(str(next_quesion_number)), 'rb')
                finish_msg = 'Вітаю, ти закінчив випробування.\nОсь твої результати:\nПравильних відповідей: <b>{0}</b>\nНеправильних відповідей: <b>{1}</b>'.format(win, lose)
                send_photo(current_caption=current_msg, caption=finish_msg, photo=photo, keyboard=get_inline_keyboard_test_finish())
            else:
                next_content_test = test[next_quesion_number]
                quesion = next_content_test['quesion']
                photo = open('vic{0}.jpg'.format(str(next_quesion_number)), 'rb')
                send_photo(current_caption=current_msg, caption=quesion, photo=photo, keyboard=get_inline_keyboard_test(next_quesion_number))

if __name__ == '__main__':
    bot.polling(none_stop=True)