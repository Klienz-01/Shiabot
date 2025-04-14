import discord
import os
import json
from discord.ext import commands
from dotenv import load_dotenv
import openai

# Load .env file
load_dotenv()

# Fetch and validate required environment variables
TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OWNER_ID = os.getenv("OWNER_ID")
BOT_NAME = os.getenv("BOT_NAME", "Shia")

if not all([TOKEN, OPENAI_API_KEY, OWNER_ID]):
    raise EnvironmentError("Missing one or more required environment variables: DISCORD_TOKEN, OPENAI_API_KEY, OWNER_ID")

openai.api_key = OPENAI_API_KEY

# Setup intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

# Persona memory
persona = """
            import traceback
            print("❌ ERROR while generating reply:")
            traceback.print_exc()
            await message.channel.send(f"My brain crashed:\n```{e}```")

    await bot.process_commands(message)

# Start the bot
print("🟢 Attempting to start Shia...")
bot.run(TOKEN)