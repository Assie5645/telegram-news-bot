from telethon import TelegramClient, events
import json
import os

# ==========================
# 🔑 API CREDENTIALS
# ==========================
api_id = 30133788
api_hash = "1f2d2d024eaafe22909fbb1131e1f084"

# ==========================
# 📡 SOURCE CHANNELS
# ==========================
source_channels = [
    "@AAUMEREJA",
    "@AAU_GENERAL",
    "@PECCAAiT",
    "@AAUNews11"
]

# ==========================
# 🎯 DESTINATION CHANNEL
# ==========================
destination_channel = "@AAUCentral"

from telethon.sessions import StringSession

SESSION = "1BJWap1sBu1MxRTsmpLWMwkuL8yhXURnptSryrEOLLZLJRpxZc1EBxqQR7q9Xoza1K7eeWYhMUHrV8pMwMOzjxc2U1OAJJrSVAaP7OI-Vrm7DJ-pxObxa6i2sjxXe3gsH_e_TjFsVNyAWOGsx6d0d6iwFHhpTVWaytOaNOxGwHyMslVWdChG7xeVNEfDepbOQo9036296sEW5hsm9mK9p8y0fVzEzVMsAn-FRjgsiTSqiuF9ZHJ1BbPAfOe7O1uumnuePwBUbo01JllKIo60-ksoIrxnOrqQG7AyjfuU7H2KU6E4FRG2kEFsQXwDzSEuZdlfHidFFRw9LtxSLxOqstxZVKnliNDg="

client = TelegramClient(StringSession(SESSION), api_id, api_hash)
# ==========================
# 🛑 PERSISTENT DUPLICATE STORAGE
# ==========================
DATA_FILE = "processed.json"

# Load old data if exists
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f:
            processed_ids = json.load(f)
    except:
        processed_ids = {}
else:
    processed_ids = {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(processed_ids, f)


print("🚀 BOT STARTED — PROFESSIONAL MODE")


# =====================================================
# 📸 HANDLE PHOTO / VIDEO ALBUMS
# =====================================================
@client.on(events.Album(chats=source_channels))
async def handle_album(event):

    album_id = str(event.grouped_id)

    # If duplicate found → delete old post
    if album_id in processed_ids:
        try:
            old_msg_id = processed_ids[album_id]
            await client.delete_messages(destination_channel, old_msg_id)
            print("🗑 Deleted duplicate album from destination")
        except:
            pass

    files = [msg.media for msg in event.messages]
    caption = event.messages[0].text or ""

    sent = await client.send_file(
        destination_channel,
        files,
        caption=caption
    )

    # Save new message id
    processed_ids[album_id] = sent.id
    save_data()

    print("📸 Album forwarded with protection")


# =====================================================
# ✍ HANDLE NORMAL POSTS
# =====================================================
@client.on(events.NewMessage(chats=source_channels))
async def handle_message(event):

    message = event.message

    # Ignore messages that belong to albums
    if message.grouped_id:
        return

    unique_key = f"{message.chat_id}_{message.id}"

    # If duplicate exists → delete old post
    if unique_key in processed_ids:
        try:
            old_msg_id = processed_ids[unique_key]
            await client.delete_messages(destination_channel, old_msg_id)
            print("🗑 Deleted duplicate post")
        except:
            pass

    text = message.text or ""

    # Send message
    if message.media:
        sent = await client.send_file(
            destination_channel,
            message.media,
            caption=text
        )
    else:
        sent = await client.send_message(
            destination_channel,
            text
        )

    # Save message id
    processed_ids[unique_key] = sent.id
    save_data()

    print("✅ Message forwarded with full protection")


# ==========================
# 🚀 RUN BOT
# ==========================
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    print("🚀 BOT STARTED — STABLE MODE")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
