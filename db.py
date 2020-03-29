
import sqlite3

from logger import new_logger

log = new_logger('db')

__connection = None

def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('admin.db',check_same_thread=False)
    return __connection


def init_db(force: bool = False):


    conn = get_connection()
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS users')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY,
            username    TEXT NOT NULL,
            callback    TEXT NOT NULL
        )
    ''')

    conn.commit()

def add_callback(username: str, callback: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO users (username, callback) VALUES (?,?)', (username, callback))
    
    c.execute('SELECT * FROM users')

    res = c.fetchall()
    log.info('Success insert to db')
    conn.commit()

def get_users_by_callback(callback: str):
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        SELECT DISTINCT username FROM users
        WHERE callback = ?
    ''', (callback, ))
    
    users = c.fetchall()

    c.execute('''
        SELECT COUNT(*) FROM users
        WHERE callback = ?
    ''', (callback, ))
    
    count = c.fetchall()[0][0]

    conn.commit()
    cout_text = ('Усього {0} раз натиснули на кнопку').format(count)
    users_text = ''.join('@{}\n'.format(str(x[0])) for x in users)
    log.info('Success get from db')
    return (count, users)


if __name__ == '__main__':
    init_db()
    add_callback('tetsnet', 'callback_button_two')
    get_users_by_callback('callback_button_two')