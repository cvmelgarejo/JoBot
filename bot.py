from telegram import Bot, Update
from telegram.ext import CommandHandler, Updater, CallbackContext

from database import DataBase
from dotenv import dotenv_values

import os

TOKEN = dotenv_values('./.env')['TELEGRAM_BOT_TOKEN']
SECRET = dotenv_values('./.env')['SECRET']
URL = dotenv_values('./.env')['URL'] + SECRET
PORT = int(os.environ.get('PORT', '443'))

def start(update, context):
    update.message.reply_text("""Si estás buscando trabajo puedo ayudarte! Sólo tenés que suscribirte con /sub y seguido escribir el trabajo que estás buscando

👁 Ejemplo: /sub Administrativo

👉 Otro ejemplo /sub Contador

👉 Otro ejemplo /sub Programador.

Después me dejás a cargo que yo te encuentro un trabajo 🤖👍""")

def sub(update, context):
    keywords = update.message.text.replace('/sub', '').strip()

    if len(keywords) == 0:
        update.message.reply_text('Vaya, parece que nos has leido los ejemplos de uso de este comando. Para hacerlo digita /help')
    else:
        db = DataBase()
        is_sub = db.read(update.message.from_user.id)

        if len(is_sub) == 0:
            db.write(user_id=update.message.from_user.id, keyword=keywords)
        else:
            db.write(user_id=update.message.from_user.id, keyword=f"{is_sub[0][0]} {keywords}", update=True)

        keywords = keywords.replace(' ', '\n')
        message = f"""Te suscribiste a las ofertas relacionadas a: 
{keywords}
Podés usar el comando  /desub para desuscribirte.
Unos ejemplos de como usarlo:
    👉 /desub Programación
    👉 /desub Trabajador social"""
        update.message.reply_text(message)

def desub(update, context):
    keywords_message = update.message.text.replace('/desub', '').strip()
    db = DataBase()

    if len(keywords_message) == 0:
        db.delete(user_id=update.message.from_user.id)
        update.message.reply_text('Se han anulado tus suscripciones.')
    else:
        keywords = db.read(update.message.from_user.id)[0][0]
        for key in keywords_message.split():
            keywords = ' '.join(keywords.replace(key, '').split()).strip()
        db.write(user_id=update.message.from_user.id, keyword=keywords, update=True)
        keywords = keywords_message.replace(' ', '\n')
        update.message.reply_text(f'Se ha anulado tu suscripcion de: \n{keywords}')

    
def lista(update, context):
    db = DataBase()
    keywords = db.read(user_id=update.message.from_user.id)
    if len(keywords) == 0:
        update.message.reply_text('No tienes suscripciones.')
    else:
        keywords = keywords[0][0].replace(' ', '\n')
        update.message.reply_text(f'Tus suscripciones: \n{keywords}')

def setWebhook():
    """ Start Webhook """
    bot = Bot(TOKEN)
    bot.delete_webhook()

    updater.start_webhook(listen="0.0.0.0",
                           port=PORT,
                           url_path=TOKEN,
                           webhook_url=URL)

def removeWebhook():
    """ Remove Webhook """
    bot = Bot(TOKEN)
    bot.delete_webhook()

def main():
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler(['start', 'ayuda', 'help'], start))
    updater.dispatcher.add_handler(CommandHandler('sub', sub))
    updater.dispatcher.add_handler(CommandHandler('desub', desub))
    updater.dispatcher.add_handler(CommandHandler('lista', lista))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print('I\'m live.')
    main()