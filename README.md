# Discord Bot

A powerful Discord bot with multiple features including music playback, moderation, fun commands, and automated encouragement responses.

## Features
- 🎵 **Music Player**: Play YouTube audio in a voice channel.
- ⚙️ **Moderation**: Kick and ban users with commands.
- 🤖 **AI Responses**: Sends encouraging messages when detecting sad words.
- 🎭 **Fun Commands**: Fetches memes, tells jokes, and plays rock-paper-scissors.

## Prerequisites
Ensure you have the following installed:
- Python 3.12+
- [FFmpeg](https://ffmpeg.org/) (for music playback)
- [Discord Developer Application](https://discord.com/developers/applications) (for bot token)

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/your-username/discord-bot.git
   cd discord-bot
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Create a `.env` file and add your bot token:
   ```
   DISCORD_BOT_TOKEN=your-bot-token-here
   ```

## Running the Bot
To start the bot, use:
```sh
python main.py
```

## Commands
- `!play <url>` - Plays audio from a YouTube video.
- `!hello` - Sends a random bot greeting.
- `!kick @user` - Kicks a user (requires permissions).
- `!ban @user` - Bans a user (requires permissions).
- `!reddit_meme` - Fetches a random meme from Reddit.
- `!joke` - Tells a random joke.
- `!rps <choice>` - Play Rock-Paper-Scissors.

## Troubleshooting
### SSL Certificate Error
If you face an SSL error, install certificates manually:
```sh
python -m certifi
```

### Voice Commands Not Working
Make sure `PyNaCl` is installed:
```sh
pip install pynacl
```

### Bot Not Responding
- Check if the bot is online in your server.
- Ensure the bot has the necessary permissions.
- Verify the token in `.env` is correct.

## License
This project is licensed under the MIT License.

