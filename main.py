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
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation,
                temperature=0.9
            )

            reply = response.choices[0].message.content
            print(f"💬 Shia replies: {reply}")

            await message.channel.send(reply)

            user_memory.append({"role": "assistant", "content": reply})
            save_user_memory(user_id, user_memory)

        except Exception as e:
            print("❌ ERROR while generating reply:")
            print(e)
            await message.channel.send("Something broke in my brain... try again soon.")

    await bot.process_commands(message)

# Start the bot
print("🟢 Attempting to start Shia...")
bot.run(TOKEN)
