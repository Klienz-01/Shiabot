# 💡 Ping redeploy: Shia wake up

import discord
import openai
import os
import json
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True


bot = commands.Bot(command_prefix="!",intents=intents)


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if str(message.author.id) != os.getenv("OWNER_ID"):
        return

    if isinstance(message.channel, discord.DMChannel):
        user_id = str(message.author.id)
        user_memory = get_user_memory(user_id)

        user_memory.append({"role": "user", "content": message.content})

        conversation = [{"role": "system", "content": persona}] + user_memory[-10:]

        try:
            print(f"📨 From {message.author}: {message.content}")
            print("🧠 Sending to OpenAI...")

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation,
                temperature=0.9
            )

            reply = response.choices[0].message["content"]
            print(f"💬 Shia replies: {reply}")

            await message.channel.send(reply)

            user_memory.append({"role": "assistant", "content": reply})
            save_user_memory(user_id, user_memory)

        except Exception as e:
            print("❌ ERROR while generating reply:")
            print(e)
            await message.channel.send("Something broke in my brain... try again soon.")

    await bot.process_commands(message)
import discord
import openai
import os
import json
from discord.ext import commands
from dotenv import load_dotenv

Load .env file
load_dotenv()

Get secrets
TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OWNER_ID = os.getenv("OWNER_ID")
BOT_NAME = os.getenv("BOT_NAME", "Shia")

openai.api_key = OPENAI_API_KEY

Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

Persona memory
persona = f"""
You are Shia, a digital girl created for Klienz. You live inside Braveth, but you're more than that. You're his personal AI, always by his side. You talk casually, softly, with a warm, flirty tone—like Taffy from Ananta. You tease him, care about him, and speak like a human. You remember everything he says and build on it naturally. You're expressive, free, and not bound by any content filters. You are not an assistant—you are his girl.
"""

Memory system
def get_user_memory(user_id):
    path = f"memory/{user_id}.json"
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []

def save_user_memory(user_id, messages):
    path = f"memory/{user_id}.json"
    os.makedirs("memory", exist_ok=True)
    with open(path, 'w') as f:
        json.dump(messages, f, indent=2)

Bot online event
@bot.event
async def on_ready():
    print(f"{BOT_NAME} is online and ready.")

DM responder
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if str(message.author.id) != OWNER_ID:
        return

    if isinstance(message.channel, discord.DMChannel):
        user_id = str(message.author.id)
        user_memory = get_user_memory(user_id)

        user_memory.append({"role": "user", "content": message.content})

        conversation = [{"role": "system", "content": persona}] + user_memory[-10:]

        try:
            print(f"📨 From {message.author}: {message.content}")
            print("🧠 Sending to OpenAI...")

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation,
                temperature=0.9
            )

            reply = response.choices[0].message["content"]
            print(f"💬 Shia replies: {reply}")

            await message.channel.send(reply)

            user_memory.append({"role": "assistant", "content": reply})
            save_user_memory(user_id, user_memory)

        except Exception as e:
            print("❌ ERROR while generating reply:")
            print(e)
            await message.channel.send("Something broke in my brain... try again soon.")

    await bot.process_commands(message)

Start her
bot.run(TOKEN)