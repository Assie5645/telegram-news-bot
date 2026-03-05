from telethon import TelegramClient, events

# ===== API DETAILS =====
api_id = 30133788         # your api_id
api_hash = "1f2d2d024eaafe22909fbb1131e1f084" # your api_hash

# ===== CHANNELS =====
source_channels = [
    "@AAUMEREJA",
    "@AAU_GENERAL",
    "@PECCAAiT",
    "@AAUNews11"
]

destination_channel = "@AAUCentral"

# ===== TELEGRAM CLIENT =====
client = TelegramClient("session", api_id, api_hash)

# ===== START CLIENT =====
client.start()

print("🚀 USER CLIENT RUNNING...")

# ===== DUPLICATE PROTECTION =====
copied_messages = set()

# ===== DETECT NEW POSTS =====
@client.on(events.NewMessage(chats=source_channels))
async def handler(event):

    message = event.message

    message_id = message.id
    message_text = message.text

    unique_key = f"{message_id}_{message_text}"

    if unique_key in copied_messages:
        print("⚠ Duplicate skipped")
        return

    copied_messages.add(unique_key)

    print("🔥 NEW MESSAGE DETECTED")

    try:
        await client.send_message(destination_channel, message)
        print("✅ Message copied to destination channel")

    except Exception as e:
        print("❌ Error:", e)


client.run_until_disconnected()
