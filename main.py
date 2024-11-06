from telethon import TelegramClient, events, Button
import random
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# API credentials
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Initializing the Telegram bot client
bot = TelegramClient('SoundAI_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Sample responses for sound categories
sound_samples = {
    "Natural Sounds": "🌲 Sample: Gentle rainforest ambiance with birds chirping and light rainfall.",
    "Industrial Sounds": "🔧 Sample: A busy factory floor with rhythmic machinery sounds.",
    "Film and TV Sounds": "🎬 Sample: Dramatic footsteps and subtle suspense tones.",
    "Household Sounds": "🏠 Sample: Kitchen sounds, with sizzling and clinking dishes.",
    "Scientific Sounds": "🔬 Sample: High-frequency lab signals and electronic beeps."
}

# Fun facts related to sound and AI (SoundAI)
fun_facts = [
    "SoundAI's algorithms can generate unique soundscapes within seconds!",
    "Did you know? Sound frequency can affect our emotions and mood.",
    "SoundAI uses deep learning to recreate sounds from textual descriptions."
]

### Helper function to show the main menu ###
async def show_main_menu(event, message):
    """Displays the main menu with commands as buttons."""
    await event.respond(
        message,
        buttons=[
            [Button.text('🔊 Generate Sample'), Button.text('📜 Help')],
            [Button.text('💬 Fun Fact'), Button.text('ℹ️ About')]
        ]
    )

### Command Handlers ###

# /start command - Welcoming the user
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_name = event.sender.first_name
    welcome_message = f"Welcome {user_name} to SoundAI Bot! 🎶\nExplore sound generation and fun sound-related features with me."
    await show_main_menu(event, welcome_message)

# /help command - Display available commands
@bot.on(events.NewMessage(pattern='/help|📜 Help'))
async def help(event):
    help_message = (
        "Here are the commands you can use:\n\n"
        "🎵 /start - Start chatting with me\n"
        "🔊 /generate - Generate a sound sample\n"
        "📜 /help - Display all commands\n"
        "ℹ️ /about - Learn more about me\n"
        "💬 /fact - Discover something fun about sounds!"
    )
    await show_main_menu(event, help_message)

# /generate command - Select sound category to generate a sample
@bot.on(events.NewMessage(pattern='/generate|🔊 Generate Sample'))
async def choose_category(event):
    await event.respond(
        "Select a sound category for a sample suggestion:",
        buttons=[
            [Button.text('Natural Sounds'), Button.text('Industrial Sounds')],
            [Button.text('Film and TV Sounds'), Button.text('Household Sounds')],
            [Button.text('Scientific Sounds'), Button.text('🔙 Back to Start')]
        ]
    )

# Respond based on selected sound category
@bot.on(events.NewMessage(pattern='Natural Sounds|Industrial Sounds|Film and TV Sounds|Household Sounds|Scientific Sounds'))
async def generate_sample(event):
    category = event.message.message
    response = sound_samples.get(category, "Explore a unique sound experience!")
    await event.respond(
        f"🔊 Here’s a {category} sample suggestion:\n\n{response}",
        buttons=[[Button.text('🔙 Back to Start')]]
    )

# Fun Fact command - Sends a random fun fact
@bot.on(events.NewMessage(pattern='/fact|💬 Fun Fact'))
async def fun_fact(event):
    fact = random.choice(fun_facts)
    await event.respond(f"🎉 Sound Fact:\n\n{fact}", buttons=[[Button.text('🔙 Back to Start')]])

# /about command - Provides information about the bot
@bot.on(events.NewMessage(pattern='/about|ℹ️ About'))
async def about(event):
    about_message = (
        "I’m SoundAI Bot, here to help you explore sound-related insights and sample generation! "
        "I'm inspired by SoundAI's AI tools in sound design and production."
    )
    await show_main_menu(event, about_message)

# Back to Start button - Return to the main menu
@bot.on(events.NewMessage(pattern='🔙 Back to Start'))
async def back_to_start(event):
    await show_main_menu(event, "Back to the main menu.")

# Main function to setup commands and start bot
async def main():
    print("Bot is now active and running...")

    await bot.run_until_disconnected()

# Start the bot and keep running
with bot:
    bot.loop.run_until_complete(main())
