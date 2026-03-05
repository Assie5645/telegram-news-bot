from telethon import TelegramClient, events

api_id = 30133788
api_hash = "1f2d2d024eaafe22909fbb1131e1f084"

# ===== CHANNELS =====
source_channels = [
    "@AAUMEREJA",
    "@AAU_GENERAL",
    "@PECCAAiT",
    "@AAUNews11"
]

destination_channel = "@AAUCentral"

# ===== MEMORY FOR DUPLICATES =====
processed_messages = set()

# ===== TELEGRAM CLIENT =====
client = TelegramClient("session", api_id, api_hash)

@client.on(events.NewMessage(chats=source_channels))
async def repost(event):

    message_id = event.message.id
    chat_id = event.chat_id
    unique_id = f"{chat_id}_{message_id}"

    # Duplicate protection
    if unique_id in processed_messages:
        print("⚠ Duplicate skipped")
        return

    processed_messages.add(unique_id)

    try:
        await client.send_message(
            destination_channel,
            event.message
        )

        print("✅ Message copied")

    except Exception as e:
        print("❌ Error:", e)

# ===== START CLIENT =====
client.start()
print("🚀 AUTO NEWS SYSTEM RUNNING...")
client.run_until_disconnected()
