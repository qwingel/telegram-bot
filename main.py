import telebot
import calendar
from database import get_user_lessons
from datetime import date
from datetime import time

token = telebot.TeleBot('6232931993:AAG-fax5xiFD0HSiNn59S2C8Z1pSr9hGLx0')

thisDate = str(date.today()).split('-')
today = int(calendar.weekday(int(thisDate[0]), int(thisDate[1]), int(thisDate[2])))
current_time = str(time.hour) + str(time.minute) + str(time.second)

dayOfWeek = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
rus_dayOfWeek = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота")

@token.message_handler(commands=['today'])
def today_timeTable(message):
    mess = '' 
    for i in range(1, len(get_user_lessons(dayOfWeek[today]))):
        if not get_user_lessons(dayOfWeek[today])[i]:
            break
        mess += '-' + get_user_lessons(dayOfWeek[today])[i] + '\n'
    token.send_message(message.chat.id, f'<b>[{rus_dayOfWeek[today]}]</b> \n\n' + mess + f'\n<b>[{rus_dayOfWeek[today]}]</b>', parse_mode='html')

@token.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'])
def timeTable(message):
    mess=''
    if len(message.text[1:]) > 9:
        list = message.text.split('@')
        message.text = list[0]

    for i in range(1, len(get_user_lessons(message.text[1:].title()))):
        if not get_user_lessons(message.text[1:].title())[i]:
            break
        mess += '-' + get_user_lessons(message.text[1:].title())[i] + '\n'
    token.send_message(message.chat.id, f'<b>[{rus_dayOfWeek[dayOfWeek.index(message.text[1:].title())]}]</b> \n\n' + mess + f'\n<b>[{rus_dayOfWeek[dayOfWeek.index(message.text[1:].title())]}]</b>', parse_mode='html')

if __name__ == '__main__':
    token.polling(none_stop=True)