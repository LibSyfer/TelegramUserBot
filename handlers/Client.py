from create_connect import app

from pyrogram.handlers import MessageHandler
from pyrogram import filters

from fuzzywuzzy import fuzz

chat_ids = {'канал1' : -1001550540287,
            'канал2' : -1001762067846,
            'канал3' : -1001114238891,
            'канал4' : -1001731298588,
            'канал5' : -1001719976055}

storage_channel_id = -1001623116703
#storage_channel_id = -0 # test

def channel_name_filter():
    async def func(flt, Client, message):
        if message.chat.title in list(chat_ids):
            for word in message.text.lower().split(' '):
                if fuzz.ratio("mumcfm", word) > 80 or fuzz.ratio("мумцфм", word) > 80:
                    return True
    return filters.create(func)

async def listener(client, message):
    try:
        await message.forward(storage_channel_id)
    except:
        print("Error: Не удается переслать сообщение в выбранный канал.")

# Добавить новый канал в пул прослушивания
async def add_channel():
     return

# Вывести список прослушиваемых каналов и их id
async def show_channel_pool():
    return

def register_handlers(app):
    app.add_handler(MessageHandler(listener, channel_name_filter()))
    #app.add_handler(MessageHandler(frwrd, (filters.chat(chat_ids["канал1"]) | filters.chat(chat_ids["канал2"])) & filters.regex("MUMCFM")))
