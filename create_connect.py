from pyrogram import Client

import os

app = Client("valli", api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"))
