import discord
import asyncio
import random
from datetime import datetime, timedelta, timezone

# Your values
USER_TOKEN = "ur_token_here" # Replace with your own token
SERVER_ID = 390628544369393664  # r/CryptoCurrency server ID
CHANNEL_ID = 983014987696078888  # Target channel ID

# Define EST timezone (UTC-5, no DST adjustment here)
EST = timezone(timedelta(hours=-5))

# Target time: 9:30 AM EST, with a 1-hour window (9:00-10:00 AM)
TARGET_HOUR = 9
TARGET_MINUTE = 30
WINDOW_MINUTES = 60  # 1-hour window

# Date range: Last 7 days from today (March 22, 2025)
START_DATE = datetime(2025, 3, 16, 0, 0, 0, tzinfo=EST)  # 7 days ago
END_DATE = datetime(2025, 3, 22, 0, 0, 0, tzinfo=EST)    # Today

# Initialize client
client = discord.Client()

async def scrape_time_window(channel, start_time, end_time):
    """Scrape all messages in a specific time window."""
    print(f"Scraping from {start_time} to {end_time}")
    total_messages = 0
    with open("crypto_discord_time.txt", "a", encoding="utf-8") as f:
        async for message in channel.history(limit=1000, after=start_time, before=end_time):
            total_messages += 1
            f.write(f"{message.created_at} | {message.author} | {message.content}\n")
            f.flush()
            if total_messages % 100 == 0:
                print(f"Scraped {total_messages} messages")
            await asyncio.sleep(random.uniform(1, 3))
    print(f"Window complete. Scraped {total_messages} messages.")
    return total_messages

@client.event
async def on_ready():
    """Runs when the bot logs in."""
    print(f"Logged in as {client.user}")
    
    guild = client.get_guild(SERVER_ID)
    if guild is None:
        print("Not in the target server. Check SERVER_ID or join the server.")
        await client.close()
        return
    
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        print("Invalid CHANNEL_ID. Check and try again.")
        await client.close()
        return
    
    # Loop through each day
    current_date = START_DATE
    total_scraped = 0
    while current_date <= END_DATE:
        start_time = current_date.replace(hour=TARGET_HOUR, minute=TARGET_MINUTE-30, second=0, microsecond=0)
        end_time = start_time + timedelta(minutes=WINDOW_MINUTES)
        daily_count = await scrape_time_window(channel, start_time, end_time)
        total_scraped += daily_count
        current_date += timedelta(days=1)
        await asyncio.sleep(10)  # Pause between days
    
    print(f"All days complete. Total messages scraped: {total_scraped}")
    await client.close()

# Run the client
try:
    client.run(USER_TOKEN, bot=False)
except Exception as e:
    print(f"Error: {e}")