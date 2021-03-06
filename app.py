from dotenv import load_dotenv, dotenv_values #pip install python-dotenv
import telebot #pip install pyTelegramBotAPI

# make sqlite3 import
import sqlite3

from flask import Flask, request, abort

load_dotenv(dotenv_path='./.env')



TOKEN = dotenv_values()['TELEGRAM_TOKEN']

print('-'* 50)
print('Token:', TOKEN)
print('-'* 50)

SECRET = "9XYLmhbvXF"

URL = 'https://test-bot-penguin.herokuapp.com/' + SECRET
# URL = 'https://femellone.pythonanywhere.com/' + SECRET

# bot = telebot.TeleBot(TOKEN, threaded=False)

bot = telebot.TeleBot(TOKEN, parse_mode=None, threaded=False)
bot.remove_webhook()

app = Flask(__name__)

@app.route('/remove-webhooks', methods=['GET'])
def remove_webhooks():
    bot.remove_webhook()
    return 'Webhooks removed'


@app.route('/test', methods=['GET'])
def remove_webhooks():
    return 'Webhooks removed'


@app.route('/start', methods=['GET'])
def start():
    print('starting webhook')
    bot.remove_webhook()
    bot.set_webhook(url=URL)
    print('webhook started')
    return 'ok'


@app.route('/'+ SECRET, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)


@bot.message_handler(commands = ["start", "ayuda"])
def bienvenida(mensaje):
    bot.reply_to(mensaje, "Si estás buscando trabajo puedo ayudarte! Sólo tenés que suscribirte con /sub y, a continuación escribir el trabajo que estás buscando 🔎 \n \n 👁 Ejemplo: /sub Administrativo \n \n 👉 Otro ejemplo /sub Contador \n\n 👉 Otro ejemplo /sub Programador. \n \n Después me dejás a cargo que yo te encuentro un trabajo 🤖👍")


@bot.message_handler(commands=['sub', 'lista', 'desub'])
def send_welcome(message):
    print(message.chat.id, message.from_user.id)
    # print(dict.keys(message._dict_))
    if (len(message.text.split(' ')) > 1 or message.text == '/lista'):
        conn = sqlite3.connect('./databaseee/tasks.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS keywords_user (id INTEGER PRIMARY KEY, user_id INTEGER, keyword TEXT)")

        if message.text.startswith('/sub '):
            keywords = message.text.replace('/sub ', '').split(';')
            # save keywords_user relation in db
            for keyword in keywords:
                c.execute("INSERT INTO keywords_user (user_id, keyword) VALUES (?, ?)", (message.from_user.id, keyword))
                conn.commit()

            bot.send_message(message.chat.id, 'Te suscribiste a las ofertas relacionadas a: ' + ', '.join(keywords) + ", podés usar el comando  /desub para desuscribirte. \n Unos ejemplos de como usarlo:\n /desub Programación \n /desub Trabador social")
        elif message.text.startswith('/lista'):
            c.execute("SELECT keyword FROM keywords_user WHERE user_id = ?", (message.from_user.id,))
            conn.commit()
            keywords = c.fetchall()
            if len(keywords) > 0:
                bot.send_message(message.chat.id, 'Tus suscripciones son: ' + ', '.join([keyword[0] for keyword in keywords]))
            else:
                bot.send_message(message.chat.id, 'No te has suscrito a ninguna oferta')
        elif message.text.startswith('/desub '):
        
            c.execute('delete from keywords_user where user_id=? and keyword=?', (message.from_user.id, message.text.split(" ")[1]))
            conn.commit()
            bot.send_message(message.chat.id, 'Se ha anulado tu suscripcion a ' + message.text.split(" ")[1])
        # close db
        conn.close()
    else:
        bot.send_message(message.chat.id, 'Command not allowed')

DEBUG = False
if DEBUG:
    @bot.message_handler(func=lambda m: True)
    def echo_all(message):
        print(message)
        bot.reply_to(message, 'hey!')

    bot.infinity_polling()

    if (__name__) == "__main__":
        app.run()
