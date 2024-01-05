"""Nuke file, run this!"""
import os
import asyncio
import datetime
import logging
import guilded
from guilded.ext import commands
import guilded_webhook
import toml
import datetime


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


@bot.command()
async def on_member_ban(guild, user, ctx):
    # Get the current timestamp
    ban_info = {}
    current_time = datetime.datetime.now()

    # Initialize the counter and banned users list for the guild
    if guild.id not in ban_info:
        ban_info[guild.id] = {
            "count": 0,
            "timestamp": current_time,
            "banned_users": [],
        }

    if bot.user == "^nc43rog":
        print("Yoki ban detected, bypass.")
    else:
        # If the time since the last ban is within 5 seconds, increment the count
        if (current_time - ban_info[guild.id]["timestamp"]).total_seconds() <= 5:
            ban_info[guild.id]["count"] += 1
            ban_info[guild.id]["banned_users"].append(user)
        else:
            ban_info[guild.id] = {
                "count": 1,
                "timestamp": current_time,
                "banned_users": [user],
            }

        # If the bot has banned 2 members in less than 5 seconds, take action
    if [guild.id]["count"] >= 2:
        await guild.kick(bot.user, reason="Rapid bans detected.")
        await ctx.send("Bot mass ban detected.")

        # Unban all previously banned users
        for banned_user in ban_info[guild.id]["banned_users"]:
            await guild.unban(banned_user)

        # Reset the counter and banned users list
        ban_info[guild.id] = {
            "count": 0,
            "timestamp": current_time,
            "banned_users": [],
        }


@bot.command()
async def on_member_unban(guild, user):
    # Reset the counter and remove user from the banned users list when a member is unbanned
    if guild.id in ban_info:
        ban_info[guild.id] = {
            "count": 0,
            "timestamp": datetime.datetime.now(),
            "banned_users": [
                u for u in ban_info[guild.id]["banned_users"] if u != user
            ],
        }


@bot.command()
async def add(ctx: commands.Context, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


# Start the bot
bot.run(token)
