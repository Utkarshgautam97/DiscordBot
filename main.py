import discord
from discord.ext import commands
import yt_dlp
import random
import asyncio
import json
import os
import requests
from dotenv import load_dotenv
import ssl
import certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())

import discord
import ctypes
import os

opus_path = "/opt/homebrew/lib/libopus.dylib"  # Path to Opus

if not discord.opus.is_loaded():
    try:
        discord.opus.load_opus(opus_path)
        print("✅ Opus loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load Opus: {e}") # Let Discord.py find the default Opus library
# Bot Configuration
PREFIX = "!"
intents = discord.Intents.all()
class MyBot(commands.Bot):
    async def on_ready(self):
        print(f'✅ Logged in as {self.user}')

bot = MyBot(command_prefix=PREFIX, intents=intents)
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "upset"]
resp=["BEEP BOOPP!","Hello I am your bot","I am powered by 99%",]
# Encouraging responses
encouragements = [
    "Cheer up! 😊",
    "Stay strong! 💪",
    "You got this! 🌟",
    "Everything will be okay! ❤️",
    "Keep going, you're amazing! 😇"
]
@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Prevent bot from responding to itself

    # Check if message contains sad words
    if any(word in message.content.lower() for word in sad_words):
        response = random.choice(encouragements)
        await message.channel.send(response)

    await bot.process_commands(message)  # Allow commands to work properly
# Music Player
@bot.command(name='play')
async def play(ctx, url: str):
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send("❌ You must join a voice channel first!")
        return
    
    voice_channel = ctx.author.voice.channel

    # Connect to the voice channel if not already connected
    if ctx.voice_client:  # If bot is already in a voice channel
        vc = ctx.voice_client
    else:
        vc = await voice_channel.connect()

    # Download audio from YouTube
    ydl_opts = {'format': 'bestaudio'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['url']
    
    # Stop current audio if playing and play new one
    if vc.is_playing():
        vc.stop()
    
    vc.play(discord.FFmpegPCMAudio(url2))
    await ctx.send(f'🎶 Now playing: **{info["title"]}**')
@bot.command()
async def hello(ctx):
        await ctx.send(random.choice(resp))
# Moderation Commands
@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')

@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

# Fun Commands
@bot.command(name="reddit_meme")
async def reddit_meme(ctx):
    """Fetches a random meme from Reddit."""
    try:
        response = requests.get(
            "https://www.reddit.com/r/memes/random/.json", 
            headers={"User-Agent": "Mozilla/5.0"}, 
            verify=certifi.where()  # <-- Ensures proper SSL verification
        )
        data = response.json()
        meme_url = data[0]["data"]["children"][0]["data"]["url"]
        meme_title = data[0]["data"]["children"][0]["data"]["title"]

        embed = discord.Embed(title=meme_title, color=discord.Color.green())
        embed.set_image(url=meme_url)

        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send("⚠️ Error fetching meme. Try again later.")
        print(f"Reddit API error: {e}")
@bot.command(name='joke')
async def joke(ctx):
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts!", 
        "I told my wife she was drawing her eyebrows too high. She looked surprised!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I'm afraid for the calendar. Its days are numbered."
    ]
    await ctx.send(random.choice(jokes))

@bot.command(name='rps')
async def rps(ctx, choice: str):
    choices = ['rock', 'paper', 'scissors']
    bot_choice = random.choice(choices)
    result = "You win!" if (
        (choice == 'rock' and bot_choice == 'scissors') or 
        (choice == 'paper' and bot_choice == 'rock') or 
        (choice == 'scissors' and bot_choice == 'paper')
    ) else "You lose!" if choice != bot_choice else "It's a tie!"
    await ctx.send(f'Bot chose {bot_choice}. {result}')

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client is None:
        await ctx.send("❌ I'm not in a voice channel!")
        return

    await ctx.voice_client.disconnect()
    await ctx.send("👋 Left the voice channel!")
# Run the bot
if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Fetch token from .env
    if TOKEN is None:
        print("⚠️ ERROR: Bot token not found! Make sure your .env file is set up correctly.")
    else:
        bot.run(TOKEN)  # Ensures no extra spaces or newlines
