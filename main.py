import discord
from discord.ext import commands
import yt_dlp
import random
import google.generativeai as genai
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
# Load API Key from environment variable
genai.configure(api_key=os.getenv("GEMINI_TOKEN"))
def split_message(text, limit=2000):
    return [text[i:i+limit] for i in range(0, len(text), limit)] #This error happens because Discord messages have a 2000-character limit, but Gemini sometimes returns long responses.
# Modify your bot to split the response into smaller parts before sending.

# Load API keys
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGING_TOKEN")
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "upset"]
resp=["Hello! How can I assist you today?","Hey there! Hope you're having a great day! 😊","Hello I am your bot","Hey! Need any help",]
# Encouraging responses
encouragements = [
    "Cheer up! 😊",
    "Stay strong! 💪",
    "You got this! 🌟",
    "Everything will be okay! ❤️",
    "Keep going, you're amazing! 😇"
]
# 🔥 Roasts List
roasts = [
    "You're like a cloud. When you disappear, it’s a beautiful day! 🌞",
    "Your secrets are safe with me. I never even listen when you tell me them. 🤷‍♂️",
    "You're proof that even AI can be smarter than humans. 🤖😂",
    "You bring everyone so much joy… when you leave the room! 🚪",
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
@bot.command()
async def suggest(ctx, *, suggestion: str):
    with open("suggestions.txt", "a") as file:
        file.write(f"{ctx.author}: {suggestion}\n")
    await ctx.send(f"Thanks for your suggestion, {ctx.author.mention}! 💡")
# 🔥 Roast Command
@bot.command()
async def roast(ctx, member: discord.Member = None):  # Allow no mention
    if member is None:
        await ctx.send("❌ Please mention a user to roast! Example: `!roast @user`")
        return

    roast_message = random.choice(roasts)
    await ctx.send(f"{member.mention}, {roast_message}")
@bot.command()
async def chat(ctx, *, message: str):
    """Chat with Google Gemini AI (1.5 Pro)"""
    await ctx.send("🤖 Thinking...")

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")  # ✅ Use the correct model
        response = model.generate_content([message])  # ✅ Input as a list

        if hasattr(response, "text"):
            reply = response.text
        else:
            reply = "⚠️ No response from AI."

        # Split the message if it's too long
        for part in split_message(reply):
            await ctx.send(part)

    except Exception as e:
        await ctx.send("⚠️ Error communicating with Google Gemini.")
        print(e)
@bot.command()
async def imagine(ctx, *, prompt: str):
    """Generate an AI image using Stable Diffusion"""
    await ctx.send(f"🎨 Generating an image for: **{prompt}**...")

    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": prompt}

    response = requests.post(
        "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        with open("generated_image.png", "wb") as f:
            f.write(response.content)
        await ctx.send(file=discord.File("generated_image.png"))
    else:
        await ctx.send("⚠️ Error generating the image. Try again!")

# Run the bot
if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Fetch token from .env
    if TOKEN is None:
        print("⚠️ ERROR: Bot token not found! Make sure your .env file is set up correctly.")
    else:
        bot.run(TOKEN)  # Ensures no extra spaces or newlines
