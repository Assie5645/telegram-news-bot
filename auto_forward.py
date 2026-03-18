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

SESSION = "1BJWap1sBu0re5WoWyJVkIkiZdhwfqv9sqWyQBSYwTQKknVzC2helZHC-IoE53fDDJc3eemQPryodXj5_eXDQKJXXmSZTsxfeoP_kchWB34iAWVnVZGPAYp6gjmDCLpXhJrOlJTP-_G__XRxOJxMc8eco1HZODkXNyyWxBJWWpUpxMns3BvSyJ0mhqqpLQ_wOAj9CNOQlkNqQK5kXijGV0swWOurqMDp8PQd09_KtCv4vDv3bJAeibuca2SWeZt7YKvrpADvms9oEyA53OLHsbgqp4L2jjYgOwOIsajt4lzFxuE_2AZGBt8ntdd6JyqkZ3FzqBQMRp2A8WIFwBUgNX7HHU4i6GRo="

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
client.start()
client.run_until_disconnected()
