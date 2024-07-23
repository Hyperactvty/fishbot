# cog.py
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import main as M

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="test")
    async def _test(self, ctx: SlashContext):
        embed = discord.Embed(title="embed test")
        await ctx.send(content="test", embeds=[embed])

    #@cog_ext.cog_slash(name="fish", description="You start fishing")
    #async def _fish(ctx: SlashContext):
    #    await M.fish(ctx)

def setup(bot):
    bot.add_cog(Slash(bot))