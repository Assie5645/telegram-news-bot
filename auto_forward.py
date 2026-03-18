from telethon import TelegramClient, events
from telethon.sessions import StringSession
import json
import os
import asyncio
import logging

# ==========================
# ⚙️ CONFIGURATION
# ==========================
logging.basicConfig(level=logging.INFO)

api_id = 30133788
api_hash = "1f2d2d024eaafe22909fbb1131e1f084" 
SESSION_STRING = "1BJWap1sBuxAN1KcK2ytWjOSmjNffzwvqrs0f-MRoyiEsOLXk5SZ_2KHDmMPWhdEBwHdxTZfZxcU973exvMU2isI5SzuSKQmfl5gIsuWXeCnPzW_yGjJDoqq1BsEM-Wk1S_yGc0a5HMMCvuqppYC1dhtv1JKPDS-oalZl03wHHlb3P2YURlz91igl8UDran8adY0r9wuSofXgVx6bP8RK5txE0D_JH_MhImcR63NodM5sXGWbT1_3kQs4q-QjFIRM_J_DtMRSjorzxz91aVm_jC3TqNUZutp8cBDiaL3FnTDZwYoZQ0DG7UsvgnfYi0DLCwS5roFno3rX5mDAiSxfCexV5zrXdGU="

source_channels = ["@AAUMEREJA", "@AAU_GENERAL", "@PECCAAiT", "@AAUNews11"]
destination_channel = "@AAUCentral"

# Initialize
client = TelegramClient(StringSession(SESSION_STRING), api_id, api_hash)

# ==========================
# 🛑 DUPLICATE PROTECTION
# ==========================
DATA_FILE = "processed.json"
processed_ids = {}

if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f: processed_ids = json.load(f)
    except: pass

def save_data():
    with open(DATA_FILE, "w") as f: json.dump(processed_ids, f)

# ==========================
# 🔄 FORWARDING LOGIC
# ==========================
@client.on(events.Album(chats=source_channels))
async def handle_album(event):
    album_id = str(event.grouped_id)
    if album_id in processed_ids: return 
    
    files = [msg.media for msg in event.messages]
    caption = event.messages[0].text or ""
    sent = await client.send_file(destination_channel, files, caption=caption)
    
    processed_ids[album_id] = sent.id
    save_data()
    print("📸 Album Forwarded")

@client.on(events.NewMessage(chats=source_channels))
async def handle_message(event):
    if event.message.grouped_id: return
    unique_key = f"{event.chat_id}_{event.message.id}"
    if unique_key in processed_ids: return

    if event.message.media:
        sent = await client.send_file(destination_channel, event.message.media, caption=event.message.text)
    else:
        sent = await client.send_message(destination_channel, event.message.text)

    processed_ids[unique_key] = sent.id
    save_data()
    print("✅ Message Forwarded")

# ==========================
# 🚀 START BOT
# ==========================
async def main():
    print("🚀 BOT IS LIVE ON RAILWAY!")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
