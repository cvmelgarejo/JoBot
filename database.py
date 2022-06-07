import psycopg2
from dotenv import dotenv_values

DATABASE = dotenv_values('./.env')['DB']
HOST = dotenv_values('./.env')['DB_HOST']
USER = dotenv_values('./.env')['DB_USER']
PASSWORD = dotenv_values('./.env')['DB_PASSWORD']

class DataBase():
    def __init__(self):
        self.open()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS KEYWORDS_USERS(
                             ID SERIAL PRIMARY KEY, 
                             USER_ID INTEGER, 
                             KEYWORD TEXT)''')
        self.save_close()

    def open(self) -> None:
        self.conn = psycopg2.connect(
                host=HOST,
                database=DATABASE,
                user=USER,
                password=PASSWORD)
        self.cur = self.conn.cursor()
    
    def write(self, user_id, keyword, update=False) -> None:
        self.open()

        if update:
            self.cur.execute('''UPDATE KEYWORDS_USERS SET KEYWORD=%s WHERE USER_ID=%s;''', 
                             (keyword, user_id))
        else:
            self.cur.execute('''INSERT INTO KEYWORDS_USERS(USER_ID, KEYWORD) VALUES(%s, %s);''', 
                             (user_id, keyword))
        self.save_close()

    def delete(self, user_id) -> None:
        self.open()

        self.cur.execute('''DELETE FROM KEYWORDS_USERS * WHERE USER_ID=%s;''',
                         (user_id, ))
        self.save_close()

    def read(self, user_id) -> str:
        self.open()
        self.cur.execute('''SELECT KEYWORD FROM KEYWORDS_USERS WHERE USER_ID=%s;''', (user_id,))
        # Con fetchall traemos todas las filas
        data = self.cur.fetchall()
        self.save_close()
        return data

    def save_close(self) -> None:
        self.conn.commit()
        self.conn.close()

#a = DataBase()
#print(a.read(1))
#print(a.write("Hello", 1))
#print(a.read())