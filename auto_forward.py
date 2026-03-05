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
# create client session
client = TelegramClient("session", api_id, api_hash)

# connect
client.start()

print("🚀 USER CLIENT RUNNING...")

# detect new posts
@client.on(events.NewMessage(chats=source_channels))
async def handler(event):

    message = event.message

    print("🔥 NEW MESSAGE DETECTED")

    try:
        await client.send_message(destination_channel, message)
        print("✅ Message forwarded")

    except Exception as e:
        print("❌ Error:", e)


client.run_until_disconnected()
