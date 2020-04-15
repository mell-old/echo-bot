
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
        c.execute('DROP TABLE IF EXISTS test')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY,
            user_id     TEXT NOT NULL,
            username    TEXT,
            name        TEXT,
            callback    TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS test (
            id          INTEGER PRIMARY KEY,
            user_id     TEXT NOT NULL,
            username    TEXT,
            name        TEXT,
            count       integer DEFAULT 0,
            true        integer DEFAULT 0,
            false       integer DEFAULT 0
        )
    ''')

    conn.commit()

def add_callback(user_id: str, username: str, name: str, callback: str):
    conn = get_connection()
    c = conn.cursor()
    user = username
    if user == None:
        user = 'anonymous'
    c.execute('INSERT INTO users (user_id, username, name, callback) VALUES (?,?,?,?)', (user_id, user, name, callback))
    
    c.execute('SELECT * FROM users')

    log.info('Success insert to callback table')
    conn.commit()

def get_users_by_callback(callback: str):
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        SELECT DISTINCT username, name FROM users
        WHERE callback = ?
    ''', (callback, ))
    
    users = c.fetchall()

    c.execute('''
        SELECT COUNT(*) FROM users
        WHERE callback = ?
    ''', (callback, ))
    
    count = c.fetchall()[0][0]

    conn.commit()
    log.info('Success get from db')
    return (count, users)

def get_count_by_user_id(user_id: str):
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        SELECT count, true, false FROM test
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
    ''', (user_id, ))

    res = c.fetchall()
    conn.commit()
    
    if res:
        print(res[0])
        return res[0]

    print(0)
    return (0,0,0)

def update_count_by_user_id(user_id:str, answer: str):
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        UPDATE test
        SET count = count + 1, {0} = {0} + 1
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
    '''.format(answer), (user_id, ))

    log.info('Success update to test table')
    conn.commit()

def add_user_to_test(user_id: str, username: str, name: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO test (user_id, username, name) VALUES (?,?,?)', (user_id, username, name))

    log.info('Success insert to test table')
    conn.commit()

ADMIN_CALLBACK = [
    'callback_button1_info',
    'callback_button1_video',
    'callback_button_one',
    'callback_button_two',
    'callback_button_security',
    'callback_button_build',
    'callback_button_teams',
    'callback_button_test',
    'callback_info',
    'callback_challenge',
    'callback_test'
]
 
if __name__ == '__main__':
    init_db()
    n = 0
    username = [ 'olehmell', 'romanenkooleg', 'anonymous', 'sipliy0y', 'kryzhanovskyi13', 'Interscur', 'Ich0ke', 'Poplavavskyy' ]
    name = [ 'Oleh Mell', 'Oleg', 'Evgen', 'Павел', 'Володимир', 'Sasha', 'Den', 'Sergiy Poplavskyi' ]
    while n != 8:
        for x in ADMIN_CALLBACK:
            add_user_to_test('11111', username[n], name[n])
            add_callback('11111', username[n], name[n], x)
        n = n + 1
    
    print('Finish')