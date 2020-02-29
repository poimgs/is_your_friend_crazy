import json
import requests
import time
import urllib

TOKEN = '1116205707:AAHxdH5GKgzHhbGmxi8ez3IiIbOTYr1rftE'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    chat_to_texts = {}
    response = ''

    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]

        if chat not in chat_to_texts:
            chat_to_texts[chat] = [text]
        else:
            chat_to_texts[chat].append(text)

    for chat, texts in chat_to_texts.items():
        word_count = len(' '.join(texts).split(' '))
        if word_count > 100:
            response = 'Result: Psychopath'
        else:
            response = 'Result: Not a Psychopath'

        send_message(response, chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(2)


if __name__ == '__main__':
    main()