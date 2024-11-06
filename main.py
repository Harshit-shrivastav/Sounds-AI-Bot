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

# Sample responses for music-related queries(copied from Google)
music_samples = {
    "Rock": "🎸 Here’s a dynamic rock sample: Imagine electrifying riffs and powerful drums!",
    "Jazz": "🎷 Jazz sample: Mellow saxophone backed by smooth piano chords.",
    "Classical": "🎻 Classical vibe: A grand orchestral performance with strings in harmony.",
    "Ambient": "🎶 Ambient tones: Relaxing, flowing soundscapes to set the mood."
}

# Fun music-related facts to keep the conversation engaging(copied from Google) 
fun_facts = [
    "Did you know? Music can boost workout performance by up to 15%!",
    "🎶 The world's longest piece of music will end in 2640!",
    "Mozart wrote over 600 compositions in his short life of 35 years."
]

### Helper function to show the main menu ###
async def show_main_menu(event, message):
    """Displays the main menu with commands as buttons."""
    await event.respond(
        message,
        buttons=[
            [Button.text('🎹 Generate Sample'), Button.text('📜 Help')],
            [Button.text('💬 Fun Fact'), Button.text('ℹ️ About')]
        ]
    )

### Setup commands using set_bot_commands telethon function ###
async def setup_commands():
    """Set bot commands for easy access through menu button of bot."""
    await bot(functions.bots.SetBotCommandsRequest(
        commands=[
            types.BotCommand(command="start", description="Start and welcome message"),
            types.BotCommand(command="help", description="Display all available commands"),
            types.BotCommand(command="generate", description="Generate a music sample"),
        ]
    ))

### Command Handlers ###

# /start command - Welcoming the user
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_name = event.sender.first_name
    welcome_message = f"Welcome {user_name} to SoundAI Bot! 🎶\nPerform AI actions on your sounds with me."
    await show_main_menu(event, welcome_message)

# /help command - Display available commands
@bot.on(events.NewMessage(pattern='/help'))
async def help(event):
    help_message = (
        "Here are the commands you can use:\n\n"
        "🎵 /start - Start chatting with me\n"
        "🎹 /generate - Generate a music sample\n"
        "📜 /help - Display all commands\n"
        "ℹ️ /about - Learn more about me\n"
        "💬 /Fact - Discover something fun about sound!"
    )
    await show_main_menu(event, help_message)

# /generate command - Select sound to generate a sample
@bot.on(events.NewMessage(pattern='/generate|🎹 Generate Sample'))
async def choose_genre(event):
    await event.respond(
        "Select a music genre for a sample suggestion:",
        buttons=[
            [Button.text('Rock'), Button.text('Classical')],
            [Button.text('Jazz'), Button.text('Ambient')],
            [Button.text('🔙 Back to Start')]
        ]
    )

# Respond based on selected genre and hide reply markup
@bot.on(events.NewMessage(pattern='Rock|Classical|Jazz|Ambient'))
async def generate_sample(event):
    genre = event.message.message
    response = music_samples.get(genre, "Enjoy this unique sound experience!")
    await event.respond(
        f"🎼 Here’s a {genre} sample suggestion:\n\n{response}",
        buttons=[[Button.text('🔙 Back to Start')]]
    )

# Fun Fact command - Sends a random fun fact
@bot.on(events.NewMessage(pattern='💬 Fun Fact'))
async def fun_fact(event):
    fact = random.choice(fun_facts)
    await event.respond(f"🎉 Did you know?\n\n{fact}", buttons=[[Button.text('🔙 Back to Start')]])

# /about command - Provides information about the bot
@bot.on(events.NewMessage(pattern='/about'))
async def about(event):
    about_message = (
        "I’m SoundAI Bot, created to help you perform actions on sound and "
        "provide sound-related insights!"
    )
    await show_main_menu(event, about_message)

# Back to Start button - Return to the main menu
@bot.on(events.NewMessage(pattern='🔙 Back to Start'))
async def back_to_start(event):
    await show_main_menu(event, "Back to the main menu.")

# Main function to setup commands and start bot
async def main():
    await setup_commands()
    print("Bot is now active and running...")
    await bot.run_until_disconnected()

# Start the bot
with bot:
    bot.loop.run_until_complete(main())
