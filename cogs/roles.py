#
# Copyright (C) 2021-present lifehackerhansol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import discord

from discord.ext import commands


class Roles(commands.Cog):
    """
    Toggle roles!
    """
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        return True

    async def managerole(self, ctx, role=""):
        role = discord.utils.get(ctx.guild.roles, name=role)
        if role in ctx.author.roles:
            await ctx.author.remove_roles(role)
            return await ctx.send(f"You no longer have the role `{role}`!")
        else:
            await ctx.author.add_roles(role)
            return await ctx.send(f"You now have the role `{role}`!")

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def togglerole(self, ctx):
        """Toggle roles"""
        await ctx.send_help(ctx.command)

    @togglerole.command()
    async def amongus(self, ctx):
        """Among Us event ping"""
        await self.managerole(ctx, "Among us")

    @togglerole.command()
    async def minecraft(self, ctx):
        """Minecraft event ping"""
        await self.managerole(ctx, "Minecraft")

    @togglerole.command(name="skribbl.io")
    async def skribblio(self, ctx):
        """Skribbl.io event ping"""
        await self.managerole(ctx, "Skribbl.io")

    @togglerole.command()
    async def events(self, ctx):
        """General event ping"""
        await self.managerole(ctx, "Events")


def setup(bot):
    bot.add_cog(Roles(bot))
