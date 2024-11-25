import discord
import logging
from pathlib import Path
import os
import json
import asyncio
#import earp_cycle_monthly
import logging

#home_dir=Path.home()
#script_dir=os.path.dirname(os.path.abspath(__file__))
#log_output_dir=home_dir / "spotify_cycle_outputs"
#log_file = open(home_dir / "spotify_cycle_outputs" / "discordbot.log", "w")

#handler = logging.FileHandler(filename=str(log_file), encoding='utf-8', mode='a')
app_dir=os.path.join(Path.home(), 'spotify_cycle')
config_file=os.path.join(app_dir, 'config.json')
output_dir=os.path.join(Path.home(), app_dir, "outputs")
handler=logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')




class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hello'):
            await message.reply('Hello!', mention_author=True)

        # if message.content.startswith('!cycle'):
        #     await message.reply('imma cycle that playlist for you!', mention_author=True)
        #     #earp_cycle_monthly.cycle()
        #     await message.reply('i cycled that playlist for you!', mention_author=True)

            

def main():

    with open(config_file) as f:
        config = json.load(f)

    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(config['DISCORD_BOT_TOKEN'], log_handler=handler, log_level=logging.DEBUG)
    
if __name__ == '__main__':
    main()       