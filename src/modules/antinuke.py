from guilded.ext import commands
import datetime

class antinuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        # Get the current timestamp
        ban_info = {}
        current_time = datetime.datetime.now()

        # Initialize the counter and banned users list for the guild
        if guild.id not in ban_info:
            ban_info[guild.id] = {"count": 0, "timestamp": current_time, "banned_users": []}

        # If the time since the last ban is within 5 seconds, increment the count
        if (current_time - ban_info[guild.id]["timestamp"]).total_seconds() <= 5:
            ban_info[guild.id]["count"] += 1
            ban_info[guild.id]["banned_users"].append(user)
        else:
            ban_info[guild.id] = {"count": 1, "timestamp": current_time, "banned_users": [user]}

        # If the bot has banned 5 members in less than 5 seconds, take action
        if [guild.id]["count"] >= 5:
            await guild.kick(bot.user, reason="Rapid bans detected")
            
            # Unban all previously banned users
            for banned_user in ban_info[guild.id]["banned_users"]:
                await guild.unban(banned_user)

            # Reset the counter and banned users list
            ban_info[guild.id] = {"count": 0, "timestamp": current_time, "banned_users": []}

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        # Reset the counter and remove user from the banned users list when a member is unbanned
        if guild.id in ban_info:
            ban_info[guild.id] = {"count": 0, "timestamp": datetime.datetime.now(), "banned_users": [u for u in ban_info[guild.id]["banned_users"] if u != user]}

    @commands.command()
    async def add(self, ctx: commands.Context, left: int, right: int):
        """Adds two numbers together."""
        await ctx.send(left + right)

def setup(bot):
    bot.add_cog(antinuke(bot))