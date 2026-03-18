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
SESSION_STRING = "1BJWap1sBu7U94z6NYtPpLNxMAMOV61kg20oE4Yh4iCEl1R5PWP9Z_ECFZQS3jZh2TB-CxyahDAvRa82UoWxYISFYVnhHuqhDnZ6eyRPA1Xx8ZTzwppsXX32GVQcgN4y6FmJgQ546otuWkM198hpSpTS0MO8opxr5kzo5sYUo2oedcNmRKGIlKRUTxl62o4x_I0w7lAC9vlggXC-d_68vK9e7DoJLxhwOI8hrHFNMIVL3o3T8UjAZ9jZflY0ulDIroS6cN_kgMmzB6mLNeCuU1znFLPawi8KlHiXcaRnkNTV3UPRg-KNwqjViPe73PtviQNaohf4ITFxnW6Mn4Esfz_yUJQjrJ6g="

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
