from create_connect import app

from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.enums import ChatType

from fuzzywuzzy import fuzz

import sqlite3
from database import sqlite_connection

import time

chat_ids = {'канал1' : -1001550540287,
            'канал2' : -1001762067846,
            'канал3' : -1001114238891,
            'канал4' : -1001731298588,
            'канал5' : -1001719976055}

storage_channel_id = -1001623116703
#storage_channel_id = -0 # test

admin_users = {}

def channel_name_filter():
    async def func(flt, Client, message):
        if message.chat.title in list(chat_ids):
            if message.text != None: # заменить на if message.type == TEXT, по правилам
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
async def add_channel(client, message): # в pyrogram нет машины состояний, можно будет реализовать простую самостоятельно
    print(message)
    if message.chat.type == ChatType.CHANNEL:
        sqlite_connection.cursor.execute("INSERT INTO listened_channels VALUES(?, ?);", (message.forward_from_chat.title, message.forward_from_chat.id))
        sqlite_connection.conn.commit()
    else:
        print("Можно добавить только канал")
    # try:
    #     sqlite_connection.cursor.execute("INSERT INTO listened_channels VALUES(?, ?);", (message.forward_from_chat.title, message.forward_from_chat.id))
    #     sqlite_connection.conn.commit()
    # except:
    #     await message.reply("Канал уже в пуле")
    # else:
    #     await message.reply("Успешно")

# Вывести список прослушиваемых каналов и их id
async def show_channel_pool(client, message):
    try:
        sqlite_connection.cursor.execute("SELECT * FROM listened_channels;")
        result = sqlite_connection.cursor.fetchall()
    except:
        await message.reply("Ошибка")
    else:
        if len(result) == 0:
            await message.reply_text("Каналов нет")
        else:
            await message.reply_text(result)

async def remove_channel(client, message):
    channels_to_remove = message.text.split(' ')[1:]
    if len(channels_to_remove):
        for channel in channels_to_remove:
            try:
                sqlite_connection.cursor.execute(f"DELETE FROM listened_channels WHERE name='{channel}';")
                sqlite_connection.conn.commit()
            except:
                await message.reply(f"Не удалось удалить канал {channel} из пула")
            else:
                await message.reply("Успешно")
    else:
        print("knkfnfknfkef")

async def remove_all_channels(client, message):
    try:
        sqlite_connection.cursor.execute("DELETE FROM listened_channels;")
    except:
        await message.reply("Ошибка при удалении каналов")
    else:
        await message.reply("Успешно")

def register_handlers(app):
    app.add_handler(MessageHandler(listener, channel_name_filter()))
    app.add_handler(MessageHandler(add_channel, filters.forwarded & filters.incoming))
    app.add_handler(MessageHandler(show_channel_pool, filters.command(commands=["show_channels"], prefixes="!") & filters.incoming))
    app.add_handler(MessageHandler(remove_channel, filters.command(commands=["remove_channel"], prefixes="!") & filters.incoming))
    app.add_handler(MessageHandler(remove_all_channels, filters.command(commands=["remove_all"], prefixes="!") & filters.incoming))
