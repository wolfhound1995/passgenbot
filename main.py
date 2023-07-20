import telebot
import requests
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv
from telebot import types
def get_from_env(key):
    dotenv_path = join(dirname(__file__), 'token.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)
token = get_from_env('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup2 = types.InlineKeyboardButton("Generate", callback_data="generate")
    markup.add(markup2)
    bot.send_message(message.chat.id, "Press button below to generate new 10 passwords", reply_markup=markup)
@bot.message_handler()
def echo_all(message):
    if message.text == 'Tip the author':
        bot.send_message(message.chat.id, 'https://www.buymeacoffee.com//wolfhoundt6')
@bot.callback_query_handler(func=lambda call: True)
def test_callback(call): # <- passes a CallbackQuery type object to your function
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    try:
        response = requests.get("https://www.passwordrandom.com/query?command=password&format=json&count=10")
        tip = types.KeyboardButton('Tip the author')
        data = json.loads(response.content)
        items = ""
        for item in data.get('char'):
            items += f"\n{str(item)}"
        markup.add(tip)
        bot.send_message(call.message.chat.id, f"List of your new passwords:\n{items}", reply_markup=markup)
        send_welcome(call.message)
    except:
        bot.send_message(call.message.chat.id, f"Error, try again please", reply_markup=markup)
        send_welcome(call.message)

bot.infinity_polling()