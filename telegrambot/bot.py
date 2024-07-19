

import os
import django
from asgiref.sync import sync_to_async
import openai
import asyncio
from aiogram import Bot, Dispatcher, types

# Set Django settings and initialize
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegrambot.settings')
django.setup()

from bot.models import Bot as BotModel  # Import your Bot model

# OpenAI API key setup
 # Use the environment variable for API keys

async def ask_gpt(prompt, bot_instructions, token):
    # Combine the user's message with the bot's specific instructions
    openai.api_key = token
    full_prompt = f"{bot_instructions}\n\n{prompt}"

    try:
        response = await sync_to_async(openai.chat.completions.create)(
           model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": bot_instructions},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50
        )
    except Exception as e:
        print(f"Error querying OpenAI: {e}")
        return "I encountered an error while generating a response. Please try again."

    if response.choices:
        
        return str(response.choices[0].message.content)
    return "Sorry, I couldn't generate a response."

async def start_bot(token, instructions, api):
    bot = Bot(token=token)
    dp = Dispatcher()

    @dp.message()
    async def handle_message(message: types.Message):
        response = await ask_gpt(message.text, instructions, api)
        await message.reply(response)

    await dp.start_polling(bot)

async def check_and_start_bots():
    global bots  # Use the global 'bots' set
    while True:
        bot_tokens = await sync_to_async(list)(BotModel.objects.all())
        for bot_token in bot_tokens:
            if bot_token.token not in bots:
                asyncio.create_task(start_bot(bot_token.token, bot_token.instructions, bot_token.api))
                bots.add(bot_token.token)
        await asyncio.sleep(60)  # Check for new tokens every 60 seconds

bots = set()  # Track started bots

async def main():
    await check_and_start_bots()

if __name__ == '__main__':
    asyncio.run(main())
