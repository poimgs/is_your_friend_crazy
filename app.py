from flask import Flask, request 
import telegram 
from telebot.credentials import bot_token, bot_user_name, URL
# from telebot.psychopath import model
import pickle
import sklearn

model = pickle.load(open('psychopath_model.sav', 'rb'))
text_transform = pickle.load(open('text_transformation.sav', 'rb'))

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

# receives telegram updates whenever a user sends a message
@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    
    # for debugging purposes only
    print("got text message :", text)

    # simple logic flow 
    if text == '/start':
        bot.sendMessage(chat_id=chat_id, text='Hello! Type in what your friend recently sent to you to check if he/she is a psychopath!')
    else:
        text = text_transform.transform([text.lower()])
        probability = round(model.predict_proba(text)[0][1], 2)
        prediction = model.predict(text)[0]
        if prediction == 1:
            bot.sendMessage(chat_id=chat_id, text='Your friend is a psychopath! RUN AWAY!')
            bot.sendMessage(chat_id=chat_id, text=f'He has a score of {probability*100}%')
        else:
            bot.sendMessage(chat_id=chat_id, text='Your friend is not a psychopath! Phew!')
            bot.sendMessage(chat_id=chat_id, text=f'He has a score of {probability*100}%')
    return 'ok'

# To set webhook for telegram to send POST requests to 
@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    app.run(threaded=True)