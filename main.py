import discord
from discord.ext import commands, tasks
import os
import json
from prettytable import PrettyTable
import asyncio


with open('./config.json', 'r') as f:
    config = json.load(f)


class sumbot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=config["prefix"],
            intents=discord.Intents.all()
    )
        self.remove_command('help')
        if config["token"] == "" or config["token"] == "token":
            self.token = os.environ['token']
        else:
            self.token = config["token"]
        self.load_extension('cogs.welcome')

    async def on_ready(self):
        tap = PrettyTable(
            ['Name Bot', 'Id', 'prefix', 'commands', 'users'])
        tap.add_row([
            self.user.display_name,
            str(self.user.id),
            self.command_prefix,
            len(self.commands),
            len(self.users),
        ])
        print(tap)

    def run(self):
        super().run(self.token, reconnect=True)


if __name__ == '__main__':
    client = sumbot()
    client.run()