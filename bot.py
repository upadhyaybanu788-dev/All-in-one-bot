import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded {filename}")

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    await load_cogs()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="🎵 Music | !help"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param}")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use !help for available commands.")
    else:
        await ctx.send(f"❌ An error occurred: {error}")

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        print("❌ DISCORD_TOKEN not found in .env file")
    else:
        bot.run(TOKEN)