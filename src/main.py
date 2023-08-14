# Imports
import guilded
from guilded.ext import commands
import toml
import os

# Get configuration from "configuration.toml"
try:
    config = toml.load(open("configuration.toml", "r"))
except FileNotFoundError:
    exit("ERROR: Unable to 'find configuration.toml'")

# Define bot
bot = commands.Bot(command_prefix="")

# Pull cogs and load them
for file in os.listdir("./cogs"):
    try:
        bot.load_extension(f".cogs.{file.removesuffix('.py')}")
    except Exception as e:
        print(f"ERROR: Unable to load '{file}', check 'errors/TO-BE-ADDED!' for error logs.")

# Start the bot
bot.run("")
