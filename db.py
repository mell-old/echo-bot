
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
            username    TEXT NOT NULL,
            callback    TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS test (
            id          INTEGER PRIMARY KEY,
            username    TEXT NOT NULL,
            count       integer DEFAULT 0,
            true        integer DEFAULT 0,
            false       integer DEFAULT 0
        )
    ''')

    conn.commit()

def add_callback(username: str, callback: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO users (username, callback) VALUES (?,?)', (username, callback))
    
    c.execute('SELECT * FROM users')

    log.info('Success insert to callback table')
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
    log.info('Success get from db')
    return (count, users)

def get_count_by_user(username: str):
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        SELECT count, true, false FROM test
        WHERE username = ?
        ORDER BY id DESC
        LIMIT 1
    ''', (username, ))

    res = c.fetchall()
    conn.commit()
    
    if res:
        print(res[0])
        return res[0]

    print(0)
    return (0,0,0)

def update_count_by_user(username:str, answer: str):
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        UPDATE test
        SET count = count + 1, {0} = {0} + 1
        WHERE username = ?
        ORDER BY id DESC
        LIMIT 1
    '''.format(answer), (username, ))

    log.info('Success update to test table')
    conn.commit()

def add_user_to_test(username: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO test (username) VALUES (?)', (username,))

    log.info('Success insert to test table')
    conn.commit()
 
if __name__ == '__main__':
    init_db()
    username = 'testuser'
    update_count_by_user(username, 'true')
    update_count_by_user(username, 'false')
    get_count_by_user(username)