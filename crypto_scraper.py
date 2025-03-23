import discord
import asyncio
import re
from textblob import TextBlob
import random

# this allows you to scrap with keywords directly from discord

# Your values
USER_TOKEN = "ur_token_here"  # Replace with your own token
SERVER_ID = 390628544369393664  # r/CryptoCurrency server ID
CHANNEL_ID = 983014987696078888  # Target channel ID

# List of coins to track
COINS = ["BTC", "ETH", "DOGE", "XRP", "ADA"]

# Initialize client (no intents needed in 1.7.3)
client = discord.Client()

async def scrape_history(channel):
    """Scrape historical messages with delays to avoid detection."""
    print(f"Scraping history from channel: {channel.name}")
    with open("crypto_discord_data.txt", "a", encoding="utf-8") as f:
        async for message in channel.history(limit=1000):
            sentiment = TextBlob(message.content).sentiment.polarity
            mentioned_coins = [coin for coin in COINS if re.search(rf"\b{coin}\b", message.content, re.IGNORECASE)]
            if mentioned_coins:
                f.write(f"{message.created_at} | {message.author} | {mentioned_coins} | {sentiment} | {message.content}\n")
            await asyncio.sleep(random.uniform(1, 3))
    print("Historical scrape complete")

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
        await scrape_history(channel)
    else:
        print("Invalid CHANNEL_ID. Check and try again.")
    await client.close()

# Run the client as a self-bot
try:
    client.run(USER_TOKEN, bot=False)  # bot=False for self-bot
except Exception as e:
    print(f"Error: {e}")