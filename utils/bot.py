import discord
from discord.ext import commands

from pathlib import Path

import config


class Bot(commands.Bot):
    __slots__ = ('extensions')
    def __init__(self, *args) -> None:
        self.ready = False
        self.extensions = [p.stem for p in Path('./cogs/').glob('*.py')]

        super().__init__(
            command_prefix=commands.when_mentioned_or('/'),
            case_insensitive=True,
            intents=discord.Intents.all(),
            owner_id=config.OWNER_ID,
            help_command=None,
            activity=discord.Activity(
                name=f'/help',
                type=discord.ActivityType.watching,
            )
        )

    def setup(self) -> None:
        print('Installation of cogs begins...')
        for ext in self.extensions:
            self.load_extension(f'cogs.{ext}')
            print(f'- `{ext}` cog loaded.')

    def run(self) -> None:
        print('Bot running...')
        self.setup()
        super().run(config.TOKEN, reconnect=True)

    async def on_ready(self) -> None:
        if self.ready:
            return

        self.ready = True
        self.guild = self.get_guild(config.MAIN_GUILD_ID)
        self.infout = self.guild.get_channel(config.INFORMATION_CHANNEL_ID)

        await self.infout.send('Bot start!')
        print(f'- Connected as {self.user.name} with ID: {self.user.id}')
        print('Have a nice day!')

    async def close(self) -> None:
        print('Shutdown...')
        await self.infout.send('Shutdown....')
        await super().close()

    async def on_connect(self) -> None:
        print(f'- Discord WebSocket Latency: {self.latency * 1000:,.0f} ms')

    async def on_disconnect(self) -> None:
        print('- Bot disconnected.')


    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or isinstance(message.channel, discord.DMChannel):
            return

        if self.user.mention in message.content:
            await message.channel.send('Yes, yes, I\'m listening. If you need help, write /help')
            return

        await self.process_commands(message)

    async def process_commands(self, message: discord.Message) -> None:
        ctx = await self.get_context(message, cls=commands.Context)

        if ctx.command is None:
            return

        await self.invoke(ctx)