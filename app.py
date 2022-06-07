from flask import Flask, request, abort
from dotenv import dotenv_values

from bot import setWebhook, removeWebhook

SECRET = dotenv_values('./.env')['SECRET']

app = Flask(__name__)

@app.route('/'+ SECRET, methods=['POST'])
def webhook():
    if request.method == 'POST':
        print("Data received from Webhook is: ", request.json)
        return "Webhook received!"

    abort(403)

@app.route('/start', methods=['GET'])
def start():
    removeWebhook()
    setWebhook()
    return 'ok'

@app.route('/remove-webhooks', methods=['GET'])
def remove_webhooks():
    removeWebhook()
    return 'Webhooks removed'

if __name__ == '__main__':
    app.run()