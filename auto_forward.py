from telethon import TelegramClient, events

# ===== API DETAILS =====
api_id = 30133788         # your api_id
api_hash = "1f2d2d024eaafe22909fbb1131e1f084" # your api_hash

source_channels = [
    "@AAUMEREJA",
    "@AAU_GENERAL",
    "@PECCAAiT",
    "@AAUNews11"
]

destination_channel = "@AAUCentral"

# store duplicates
posted_messages = set()

client = TelegramClient("session", api_id, api_hash)

print("🚀 USER CLIENT RUNNING...")

# -------- HANDLE PHOTO ALBUMS --------
@client.on(events.Album(chats=source_channels))
async def album_handler(event):

    album_id = event.grouped_id

    if album_id in posted_messages:
        print("⚠ Duplicate album skipped")
        return

    posted_messages.add(album_id)

    try:
        files = [msg.media for msg in event.messages]

        caption = ""
        if event.messages[0].text:
            caption = event.messages[0].text

        await client.send_file(
            destination_channel,
            files,
            caption=caption
        )

        print("📸 Album copied")

    except Exception as e:
        print("❌ Album error:", e)


# -------- HANDLE NORMAL MESSAGES --------
@client.on(events.NewMessage(chats=source_channels))
async def message_handler(event):

    message = event.message
    text = message.text or ""

    # unique key to detect duplicates
    key = text.strip()

    if key in posted_messages:
        print("⚠ Duplicate text skipped")
        return

    posted_messages.add(key)

    try:

        if message.media:
            await client.send_file(destination_channel, message.media, caption=text)

        else:
            await client.send_message(destination_channel, text)

        print("✅ Message copied")

    except Exception as e:
        print("❌ Error:", e)


client.start()
client.run_until_disconnected()
