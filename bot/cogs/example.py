from discord.ext import commands
from utils import Bot


class Example(commands.Cog):
    __slots__ = ('bot')

    def __init__(self, bot: Bot) -> None:
        bot = Bot()

    @commands.slash_command(description='Test command')
    async def test(self, ctx) -> None:
        await ctx.respond('Some text...')


def setup(bot: Bot) -> None:
    bot.add_cog(Example(bot))