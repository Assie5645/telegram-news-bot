from telethon import TelegramClient, events

# ===== API DETAILS =====
api_id = 30133788         # your api_id
api_hash = "1f2d2d024eaafe22909fbb1131e1f084" # your api_hash

# =======================
# 📡 SOURCE CHANNELS
# =======================
source_channels = [
    "@AAUMEREJA",
    "@AAU_GENERAL",
    "@PECCAAiT",
    "@AAUNews11"
]

# =======================
# 🎯 DESTINATION CHANNEL
# =======================
destination_channel = "@AAUCentral"

client = TelegramClient("session", api_id, api_hash)

# =======================
# 🛑 DUPLICATE STORAGE
# =======================
processed_ids = {}
# format:
# { unique_key : destination_message_id }

print("🚀 BOT STARTED — PRO VERSION")


# =====================================================
# 📸 HANDLE ALBUMS
# =====================================================
@client.on(events.Album(chats=source_channels))
async def handle_album(event):

    album_id = event.grouped_id

    if album_id in processed_ids:
        # duplicate found → delete old post
        try:
            msg_id = processed_ids[album_id]
            await client.delete_messages(destination_channel, msg_id)
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

    processed_ids[album_id] = sent.id

    print("📸 Album forwarded with delete protection")


# =====================================================
# ✍ HANDLE NORMAL POSTS
# =====================================================
@client.on(events.NewMessage(chats=source_channels))
async def handle_message(event):

    message = event.message

    # Ignore album messages (already handled)
    if message.grouped_id:
        return

    text = message.text or ""
    unique_key = f"{message.chat_id}_{message.id}"

    # If duplicate exists → delete old one
    if unique_key in processed_ids:
        try:
            old_msg_id = processed_ids[unique_key]
            await client.delete_messages(destination_channel, old_msg_id)
            print("🗑 Deleted duplicate post")
        except:
            pass

    # Send new message
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

    processed_ids[unique_key] = sent.id

    print("✅ Message forwarded with auto-delete duplicate")

print("🚀 BOT STARTED — PRO VERSION")

client.start()
client.run_until_disconnected()
