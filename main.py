intents = discord.Intents.default()
intents.messages = True 
intents.messages_content = True 
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
