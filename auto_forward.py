import os
import asyncio
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# 1. Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2. Credentials
API_ID = 30133788
API_HASH = "1f2d2d024eaafe22909fbb1131e1f084" 
# Use the Railway Variable Name here
SESSION_STRING = os.getenv("TELEGRAM_SESSION")

source_channels = ["@AAUMEREJA", "@AAU_GENERAL", "@PECCAAiT", "@AAUNews11"]
destination_channel = "@AAUCentral"

# 3. Initialize without starting
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    if event.message.grouped_id: return
    try:
        await client.send_message(destination_channel, event.message)
        logger.info("✅ Forwarded!")
    except Exception as e:
        logger.error(f"❌ Error: {e}")

async def main():
    # 🔥 THE DELAY: Wait 30 seconds for Railway to settle
    logger.info("⏳ Container starting... waiting 30 seconds to clear old sessions...")
    await asyncio.sleep(30)
    
    logger.info("📡 Attempting connection...")
    await client.connect()
    
    if not await client.is_user_authorized():
        logger.error("❌ SESSION EXPIRED! Generate a new string on your laptop.")
        return

    logger.info("🚀 BOT IS ONLINE AND STABLE!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Run the loop manually instead of 'with client:'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
