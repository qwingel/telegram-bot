import sqlite3
# from datetime import time

db = sqlite3.connect('database.db', 10.0, check_same_thread=False)

def get_user_lessons(day: str):
    user_class = '10б'
    # req = 'SELECT * FROM ' + day + ' ' + 'WHERE class = ' + user_class
    # print(req)
    if day == 'Monday': res = db.execute("""SELECT * FROM Monday WHERE class = ?""", (user_class, ))
    if day == 'Tuesday': res = db.execute("""SELECT * FROM Tuesday WHERE class = ?""", (user_class, ))
    if day == 'Wednesday': res = db.execute("""SELECT * FROM Wednesday WHERE class = ?""", (user_class, ))
    if day == 'Thursday': res = db.execute("""SELECT * FROM Thursday WHERE class = ?""", (user_class, ))
    if day == 'Friday': res = db.execute("""SELECT * FROM Friday WHERE class = ?""", (user_class, ))
    if day == 'Saturday': res = db.execute("""SELECT * FROM Saturday WHERE class = ?""", (user_class, ))
    if not res:
        return 'Неверная команда'
    
    lessons = res.fetchone()
    
    if lessons is None:
        return None
    
    return lessons

# def save_ids( username: str, id: int):
#     db.execute("""INSERT INTO saved_ids (id, username, saved_id) VALUES (1, ?, ?);""", 
#               ( username, id, ))