import telebot
import calendar
import time
from multiprocessing import *
from database import get_user_lessons
#from database import save_ids
from datetime import date
from datetime import time

bot = telebot.TeleBot('6232931993:AAG-fax5xiFD0HSiNn59S2C8Z1pSr9hGLx0')

isVoting = False

user_count = 0

thisDate = str(date.today()).split('-')
today = int(calendar.weekday(int(thisDate[0]), int(thisDate[1]), int(thisDate[2])))
current_time = str(time.hour) + str(time.minute) + str(time.second)

dayOfWeek = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
rus_dayOfWeek = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота")

muted = ['' for i in range(30)]

@bot.message_handler(commands=['today'])
def today_timeTable(message):
    mess = '' 
    for i in range(1, len(get_user_lessons(dayOfWeek[today]))):
        if not get_user_lessons(dayOfWeek[today])[i]:
            break
        mess += '-' + get_user_lessons(dayOfWeek[today])[i] + '\n'
    print(message.chat.id)
    bot.send_message(message.chat.id, f'<b>[{rus_dayOfWeek[today]}]</b> \n\n' + mess + f'\n<b>[{rus_dayOfWeek[today]}]</b>', parse_mode='html')

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
    bot.send_message(message.chat.id, f'<b>[{rus_dayOfWeek[dayOfWeek.index(message.text[1:].title())]}]</b> \n\n' + mess + f'\n<b>[{rus_dayOfWeek[dayOfWeek.index(message.text[1:].title())]}]</b>', parse_mode='html')

@bot.message_handler(commands=['mute', 'unmute', 'clear', 'mutelist'])
def mute_handler(message):
    list = message.text[1:].split()
    cmd = list[0]
    if bot.get_chat_member(message.chat.id, message.from_user.id).status == 'member' and message.from_user.username != 'girlsarethesame':
        if cmd == 'mutelist':
            mute_list(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Недостаточно прав')
    else:
        if(len(list) < 2):
            if cmd != 'clear' and cmd != 'mutelist':
                bot.send_message(message.chat.id, f'Впишите имя пользователя\nExample: /mute @{message.from_user.username}')
            elif cmd == 'clear':
                clear_mute(message.chat.id)
            else:
                mute_list(message.chat.id)
        else:
            username = list[1]
            if cmd == 'mute':
                add_mute(username, message.chat.id)
            else:
                remove_mute(username, message.chat.id)

@bot.message_handler(content_types='text')
def check_mute(message):
    username = message.from_user.username
    # id = message.from_user.id
    # save_ids( username, id)
    if '@' + username in muted:
        bot.delete_message(message.chat.id, message.message_id)

# @bot.message_handler(commands=['vote'])
# def kick_vote(message):
#     victim = message.text.split()[1]
#     if bot.get_chat_member(message.chat.id, message.from_user.id).status == 'member' and message.from_user.username != 'girlsarethesame':
#         bot.send_message(message.chat.id, 'Недостаточно прав')
#     else:
#         vote_handler()
# @bot.message_handler(commands=['lox'])
# def random_lox(message):
#     bot.get_fu
    


def add_mute(username: str, chat_id: str):
    for i in range(len(muted)):
        if muted[i] == username:
            bot.send_message(chat_id, 'Пользователь уже заглушен')
            break

        if muted[i] == '':
            muted[i] = username
            bot.send_message(chat_id, f'Пользователь {username} заглушен')
            break
    
def remove_mute(username: str, chat_id: str):
    for i in range(len(muted)):
        if(muted[i]) == username:
            muted[i] = ''
            bot.send_message(chat_id, f'Пользователь {username} снова может говорить')
            break

def clear_mute(chat_id: str):
    for i in range(len(muted)):
        muted[i] = ''
    bot.send_message(chat_id, 'Список мутов был очищен')

def mute_list(chat_id: str):
    mess = ''
    i = 0
    for i in range(len(muted)):
        if muted[i] != '':
            mess += f'({i + 1}) ' + muted[i] + '\n'
    if mess == '':
        bot.send_message(chat_id, 'Никого не заткнули :3')
    else:
        bot.send_message(chat_id, f'Список немых:\n{mess}')

# def vote_handler():
#     bot.kick_chat_member

if __name__ == '__main__':
    bot.polling(none_stop=True)
