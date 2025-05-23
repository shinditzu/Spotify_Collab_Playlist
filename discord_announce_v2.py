import discord
import logging
from pathlib import Path
import os
import json
import asyncio

#home_dir=Path.home()
#script_dir=os.path.dirname(os.path.abspath(__file__))
#log_output_dir=home_dir / "spotify_cycle_outputs"
#log_file = open(home_dir / "spotify_cycle_outputs" / "discordbot.log", "w")

#handler = logging.FileHandler(filename=str(log_file), encoding='utf-8', mode='a')
app_dir=os.path.join(Path.home(), 'spotify_cycle')
config_file=os.path.join(app_dir, 'config.json')
with open(config_file) as f:
    config = json.load(f)


class DiscordBot:
    def __init__(self):
        token=(config['DISCORD_BOT_TOKEN'])
        """
        Initialize the Discord bot with the provided token.
        """
        self.token = token
        self.client = discord.Client(intents=discord.Intents.default())

    async def send_message(self, channel_id, message):
        """
        Send a message to a specific Discord channel using a temporary client.
        """
        intents = discord.Intents.default()

        class TempClient(discord.Client):
            async def on_ready(self_):
                print(f"Logged in as {self_.user}")
                channel = self_.get_channel(channel_id)
                if channel is None:
                    print("Channel not found. Check the channel ID.")
                else:
                    await channel.send(message)
                    print("Message sent!")
                await self_.close()

        async with TempClient(intents=intents) as client:
            await client.start(self.token)

    def send(self, channel_id, message):
        """
        Entry point to send a message (runs the asyncio loop).
        :param channel_id: The ID of the channel to send the message to.
        :param message: The message content to send.
        """
        asyncio.run(self.send_message(channel_id, message))

def main():
    
    client = DiscordBot()
    client.send(1309330887888080947, "Feed Me a Bubble Butt")
    
if __name__ == '__main__':
    main()       