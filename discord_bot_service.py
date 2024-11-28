import discord
from discord.ext import commands
import os
import json
from pathlib import Path
import logging
from earp_cycle_monthly import listContributers


app_dir=os.path.join(Path.home(), 'spotify_cycle')
config_file=os.path.join(app_dir, 'config.json')
output_dir=os.path.join(Path.home(), app_dir, "outputs")
handler=logging.FileHandler(filename=os.path.join(output_dir,'discord.log'), encoding='utf-8', mode='w')


with open(config_file) as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# @bot.event
# async def on_message(message):
#     print(f'Message from {message.author}: {message.content}')

#     if message.author == bot.user:
#         return

#     if message.content.startswith('!hello'):
#         await message.reply('Hello!', mention_author=True)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}! 👋")

@bot.command()
async def bubblebutt(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.name} did a bubblebutt")

@bot.command()
async def sync(ctx):
    try:
        # Sync the commands with Discord
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Error syncing commands: {e}")

#Slash Commands
@bot.tree.command(name="hello", description="I say hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.name}!")

@bot.tree.command(name="contributors", description="I'm Working on this")
async def contributors(interaction: discord.Interaction):
    await interaction.response.send_message(listContributers())

@bot.tree.command(name="penis", description="I call jack a penis")
async def penis(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.name} called Jack a Penis!")

@bot.tree.command(name="bubblebutt", description="I do bubblebutt")
async def bubblebutt(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.name} did a bubblebutt")
# @bot.hybrid_command()
# async def contributors(ctx):
#     await ctx.send(listContributers())




def main():
    #print(listContributers)
    bot.run(config['DISCORD_BOT_TOKEN'], log_handler=handler, log_level=logging.DEBUG)

if __name__ == '__main__':
    main()     




