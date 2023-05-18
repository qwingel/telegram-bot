import telebot
import calendar
import schedule
from multiprocessing import *
from random import randint
from time import sleep
from threading import Thread
from database import get_user_lessons
#from database import save_ids
from datetime import date

bot = telebot.TeleBot('6232931993:AAG-fax5xiFD0HSiNn59S2C8Z1pSr9hGLx0')

isVoting = False
chat_usernames = ['klushka66', 'girlsarethesame', 'nxmrx3sxrrxvv', 'Klnr099', 'dasha_chernykh0',
                   'AAKotelmakh', 'imready2die', 'sonechko_Q', 'alexqqe', 'thevosim', 'huevei','georgegeorgev123123']

ids = ['' for i in range(30)]
chat_id = '-1001860613804'

dayOfWeek = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
rus_dayOfWeek = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота")

muted = ['' for i in range(30)]

@bot.message_handler(commands=['today'])
def today_timeTable(message):
    thisDate = str(date.today()).split('-')
    today = int(calendar.weekday(int(thisDate[0]), int(thisDate[1]), int(thisDate[2])))
    mess = '' 
    if today == 6:
        bot.send_message(chat_id, 'Отдохни, крошка =3')
    else:
        for i in range(1, len(get_user_lessons(dayOfWeek[today]))):
            if not get_user_lessons(dayOfWeek[today])[i]:
                break
            mess += '-' + get_user_lessons(dayOfWeek[today])[i] + '\n'
        bot.send_message(chat_id, f'<b>[{rus_dayOfWeek[today]}]</b> \n\n' + mess + f'\n<b>[{rus_dayOfWeek[today]}]</b>', parse_mode='html')

@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'])
def timeTable(message):
    mess=''
    if len(message.text[1:]) > 9:
        list = message.text.split('@')
        message.text = list[0]

    for i in range(1, len(get_user_lessons(message.text[1:].title()))):
        if not get_user_lessons(message.text[1:].title())[i]:
            break
        mess += '-' + get_user_lessons(message.text[1:].title())[i] + '\n'
    bot.send_message(chat_id, f'<b>[{rus_dayOfWeek[dayOfWeek.index(message.text[1:].title())]}]</b> \n\n' + mess + f'\n<b>[{rus_dayOfWeek[dayOfWeek.index(message.text[1:].title())]}]</b>', parse_mode='html')

@bot.message_handler(commands=['mute', 'unmute', 'clear', 'mutelist'])
def mute_handler(message):
    list = message.text[1:].split()
    cmd = list[0]
    
    if not isUserMuted(message.from_user.username):
        if bot.get_chat_member(chat_id, message.from_user.id).status == 'member' and message.from_user.username != 'girlsarethesame':
            if cmd == 'mutelist':
                mute_list()
            else:
                bot.send_message(chat_id, 'Недостаточно прав')
        else:
            if(len(list) < 2):
                if cmd != 'clear' and cmd != 'mutelist':
                    bot.send_message(chat_id, f'Впишите имя пользователя\nExample: /mute @{message.from_user.username}')
                elif cmd == 'clear':
                    clear_mute()
                else:
                    mute_list()
            else:
                username = list[1]
                if cmd == 'mute':
                    add_mute(username)
                else:
                    remove_mute(username)

@bot.message_handler(commands=['lox'])
def random_lox(message):
    bot.send_message(chat_id, f'@{chat_usernames[randint(0, len(chat_usernames) - 1)]} лох хаха')

# @bot.message_handler(commands=['votekick', 'kick'])
# def kick_user_handler(message):
#     if bot.get_chat_member(chat_id, message.from_user.id).status == 'member' and message.from_user.username != 'girlsarethesame':
#         return None
    
# #     # if message.text != 'kick':
# #     #     return None
# #     #     # start_vote_for_kick(message.reply_to_message.from_user.id)
# #     # else:
#     bot.ban_chat_member(chat_id, message.reply_to_message.from_user.id, 60)

@bot.message_handler(content_types='text')
def check_mute(message):
    username = message.from_user.username
    if '@' + username in muted:
        bot.delete_message(chat_id, message.message_id)

    for i in range(len(ids)):
        if ids[i] == message.from_user.id:
            break
        
        if ids[i] == '':
            ids[i] = message.from_user.id
            break



# @bot.message_handler(commands=['vote'])
# def kick_vote(message):
#     victim = message.text.split()[1]
#     if bot.get_chat_member(chat_id, message.from_user.id).status == 'member' and message.from_user.username != 'girlsarethesame':
#         bot.send_message(chat_id, 'Недостаточно прав')
#     else:
#         random_lox()
# def start_vote_for_kick(id: int):

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)
        
def add_mute(username: str):
    for i in range(len(muted)):
        if muted[i] == username:
            bot.send_message(chat_id, 'Пользователь уже заглушен')
            break

        if muted[i] == '':
            muted[i] = username
            bot.send_message(chat_id, f'Пользователь {username} заглушен')
            break
    
def remove_mute(username: str):
    for i in range(len(muted)):
        if username not in muted:
            bot.send_message(chat_id, f'Пользователь {username} не заглушен')
            break

        if(muted[i]) == username:
            muted[i] = ''
            bot.send_message(chat_id, f'Пользователь {username} снова может говорить')
            break

def clear_mute():
    for i in range(len(muted)):
        muted[i] = ''
    bot.send_message(chat_id, 'Список мутов был очищен')

def mute_list():
    mess = ''
    i = 0
    for i in range(len(muted)):
        if muted[i] != '':
            mess += f'({i + 1}) ' + muted[i] + '\n'
    if mess == '':
       return bot.send_message(chat_id, 'Никого не заткнули :3')
    else:
       return bot.send_message(chat_id, f'Список немых:\n{mess}')

def isUserMuted(username: str):
    for i in range(len(muted)):
        if muted[i] == username:
            return True
    return False

def good_morning():
    bot.send_message(chat_id, 'Доброе утро, котятки :3')
    today_timeTable()

def good_night():
    bot.send_message(chat_id, 'Пора спать, зайчики.\nВсем сладких снов)')

def main():
    schedule.every().day.at('06:00').do(good_morning)
    schedule.every().day.at('23:30').do(good_night)

    bot.polling(none_stop=True)

    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()