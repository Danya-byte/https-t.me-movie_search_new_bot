import sqlite3

def init_db():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            user_id INTEGER,
            query TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            user_id INTEGER,
            imdbID TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_to_history(user_id, query):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO history (user_id, query) VALUES (?, ?)', (user_id, query))
    conn.commit()
    conn.close()

def get_history(user_id):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT query FROM history WHERE user_id = ?', (user_id,))
    history = [row[0] for row in cursor.fetchall()]
    conn.close()
    return history

def add_to_likes(user_id, imdbID):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO likes (user_id, imdbID) VALUES (?, ?)', (user_id, imdbID))
    conn.commit()
    conn.close()

def remove_from_likes(user_id, imdbID):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM likes WHERE user_id = ? AND imdbID = ?', (user_id, imdbID))
    conn.commit()
    conn.close()

def get_likes(user_id):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT imdbID FROM likes WHERE user_id = ?', (user_id,))
    likes = [row[0] for row in cursor.fetchall()]
    conn.close()
    return likes