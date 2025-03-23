import discord
import asyncio
import random
from datetime import datetime

# Your values
USER_TOKEN = "ur_token_here" # Replace with your own token
SERVER_ID = 390628544369393664  # r/CryptoCurrency server ID
CHANNEL_ID = 983014987696078888  # Target channel ID

# Starting point (e.g., today or earlier)
START_TIME = datetime(2024, 12, 31, 0, 0, 0)  # Today, adjust as needed

# Initialize client
client = discord.Client()

async def scrape_history(channel, before_time, max_batches=5):
    """Scrape historical messages in batches until done or limit reached."""
    total_messages = 0
    batch_count = 0
    
    while batch_count < max_batches:  # Limit batches to avoid over-scraping
        print(f"Batch {batch_count + 1}: Scraping before {before_time}")
        messages_scraped = 0
        with open("crypto_discord_raw.txt", "a", encoding="utf-8") as f:
            async for message in channel.history(limit=1000, before=before_time):
                messages_scraped += 1
                total_messages += 1
                f.write(f"{message.created_at} | {message.author} | {message.content}\n")
                f.flush()
                if messages_scraped % 100 == 0:
                    print(f"Batch {batch_count + 1}: Scraped {messages_scraped} messages (Total: {total_messages})")
                await asyncio.sleep(random.uniform(1, 3))
            # Update before_time to the oldest message in this batch
            if messages_scraped > 0:
                before_time = message.created_at
            else:
                print("No more messages to scrape.")
                break
        print(f"Batch {batch_count + 1} complete. Scraped {messages_scraped} messages.")
        batch_count += 1
        if messages_scraped < 1000:  # Less than limit means we hit the start
            print("Reached the beginning of the channel history.")
            break
        await asyncio.sleep(random.uniform(10, 50))  # Pause between batches to avoid rate limits
    
    print(f"Scraping complete. Total messages scraped: {total_messages}")

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
    if channel:
        await scrape_history(channel, START_TIME, max_batches=5)  # Adjust max_batches as needed
    else:
        print("Invalid CHANNEL_ID. Check and try again.")
    await client.close()

# Run the client
try:
    client.run(USER_TOKEN, bot=False)
except Exception as e:
    print(f"Error: {e}")