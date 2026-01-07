import discord
from discord.ext import commands, tasks
from datetime import datetime, time
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Shrek 5 release date - June 1, 2027
SHREK_RELEASE = datetime(2027, 6, 1, 0, 0, 0)

# Channel to post daily countdown
CHANNEL_ID = 611280538535329860

def get_countdown_message():
    now = datetime.now()
    remaining = SHREK_RELEASE - now

    if remaining.total_seconds() <= 0:
        return "Shrek 5 is out! Go watch it!"

    days = remaining.days
    hours, remainder = divmod(remaining.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    return f"Time until Shrek 5 (June 2027): **{days} days, {hours} hours, {minutes} minutes**"

@tasks.loop(time=time(hour=12, minute=0))  # Posts at 12:00 PM daily
async def daily_countdown():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(get_countdown_message())

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    daily_countdown.start()

@bot.command(name="shrek")
async def shrek_countdown(ctx):
    await ctx.send(get_countdown_message())

bot.run(os.getenv("DISCORD_TOKEN"))
