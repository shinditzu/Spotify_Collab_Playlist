import discord
import os
import json
from pathlib import Path
import logging


app_dir=os.path.join(Path.home(), 'spotify_cycle')
config_file=os.path.join(app_dir, 'config.json')
output_dir=os.path.join(Path.home(), app_dir, "outputs")
handler=logging.FileHandler(filename=os.path.join(output_dir,'discord.log'), encoding='utf-8', mode='w')

with open(config_file) as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')

    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.reply('Hello!', mention_author=True)

def main():
    client.run(config['DISCORD_BOT_TOKEN'], log_handler=handler, log_level=logging.DEBUG)

if __name__ == '__main__':
    main()     




