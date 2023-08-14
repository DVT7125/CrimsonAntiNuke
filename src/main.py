"""Nuke file, run this!"""
import os
import asyncio
import datetime
import logging
import guilded
from guilded.ext import commands
import guilded_webhook
import toml


# Set up logging with a dynamic timestamped filename
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = "bot.log"
logging.basicConfig(
    level=logging.INFO,
    filename=log_filename,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

try:
    config = toml.load(open("./config/config.toml", "r", encoding="utf-8"))
except FileNotFoundError:
    exit("ERROR: Unable to 'find config/config.toml'")

webhook = config["guilded"]["settings"]["webhook"]
token = config["guilded"]["settings"]["token"]
prefix = config["guilded"]["settings"]["prefix"]

bot = commands.Bot(command_prefix=prefix, help_command=None)


@bot.event
async def on_ready():
    """When the bot is online, show in console."""
    print(
        f"Logged in as {bot.user.name} (ID: {bot.user.id}) and is ready to stop nukes!"
    )

# Load all cogs from the cogs folder
for filename in os.listdir('./modules'):
    try:
        if filename.endswith('.py'):
            bot.load_extension(f'modules.{filename[:-3]}')
    except Exception as error:
        print(
            f"ERROR: Unable to load {filename}: {error}"
        )

# Start the bot
bot.run(token)
