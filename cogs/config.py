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

from discord.ext import commands
from utils import sql
from utils.utils import is_staff, is_guild_owner


class Config(commands.Cog):
    """
    Bot configuration
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.check_any(commands.is_owner(), is_staff())
    async def config(self, ctx):
        """Set server configs for the bot"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @config.group()
    @commands.check_any(commands.is_owner(), is_guild_owner())
    async def modrole(self, ctx):
        """Set moderator roles for this server"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @modrole.command(name='add')
    async def modrole_add(self, ctx, roleid: int):
        """Add moderator roles for this server"""
        for role in ctx.guild.roles:
            if role.id == roleid:
                modrole = await sql.get_modroles(ctx.guild.id)
                modroleid = []
                for mod in modrole:
                    modroleid.append(mod.id)
                if roleid in modroleid:
                    return await ctx.send(f"{role.name} is already a moderator role!")
                await sql.add_modrole(ctx.guild.id, roleid)
                return await ctx.send(f"Success! `{role.name}` is now a moderator role.")
        await ctx.send("Role does not exist. Please try again.")

    @modrole.command(name='remove')
    async def modrole_remove(self, ctx, roleid: int):
        """Remove moderator roles for this server"""
        for role in ctx.guild.roles:
            if role.id == roleid:
                err = await sql.remove_modrole(ctx.guild.id, roleid)
                if err == 1:
                    return await ctx.send("There are no moderator roles set for this server!")
                if err == 2:
                    return await ctx.send(f"`{role.name}` is not a moderator role!")
                if err == 0:
                    return await ctx.send(f"Success! `{role.name}` is no longer a moderator role.")
        await ctx.send("Role does not exist. Please try again.")

    @config.group()
    async def muterole(self, ctx):
        """Set mute roles for this server"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @muterole.command(name='add')
    async def muterole_add(self, ctx, roleid: int):
        """Add mute role for this server"""
        for role in ctx.guild.roles:
            if role.id == roleid:
                muterole = await sql.get_muterole(ctx.guild.id)
                if muterole:
                    return await ctx.send("A mute role already exists!")
                await sql.add_muterole(ctx.guild.id, roleid)
                return await ctx.send(f"Success! `{role.name}` is now a mute role.")
        await ctx.send("Role does not exist. Please try again.")

    @muterole.command(name='remove')
    async def muterole_remove(self, ctx, roleid: int):
        """Remove mute role for this server"""
        for role in ctx.guild.roles:
            if role.id == roleid:
                err = await sql.remove_muterole(ctx.guild.id, roleid)
                if err == 1:
                    return await ctx.send("There is no mute role set for this server!")
                if err == 2:
                    return await ctx.send(f"`{role.name}` is not a mute role!")
                if err == 0:
                    return await ctx.send(f"Success! `{role.name}` is no longer a mute role.")
        await ctx.send("Role does not exist. Please try again.")

    @config.group()
    async def probaterole(self, ctx):
        """Set probation roles for this server"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @probaterole.command(name='add')
    async def probaterole_add(self, ctx, roleid: int):
        """Add a probation role for this server"""
        for role in ctx.guild.roles:
            if role.id == roleid:
                probaterole = await sql.get_probationrole(ctx.guild.id)
                if probaterole:
                    return await ctx.send("A probation role already exists!")
                await sql.add_probationrole(ctx.guild.id, roleid)
                return await ctx.send(f"Success! `{role.name}` is now a probation role.")
        await ctx.send("Role does not exist. Please try again.")

    @probaterole.command(name='remove')
    async def probaterole_remove(self, ctx, roleid: int):
        """Remove a probation role for this server"""
        for role in ctx.guild.roles:
            if role.id == roleid:
                err = await sql.remove_probationrole(ctx.guild.id, roleid)
                if err == 1:
                    return await ctx.send("There is no probation role set for this server!")
                if err == 2:
                    return await ctx.send(f"`{role.name}` is not a probation role!")
                if err == 0:
                    return await ctx.send(f"Success! `{role.name}` is no longer a probation role.")
        await ctx.send("Role does not exist. Please try again.")

    @config.group()
    async def autorole(self, ctx):
        """Enable/disable/add autorole for this server"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @autorole.command(name='enable')
    async def autorole_enable(self, ctx):
        """Enable automatic roles on join."""
        await sql.set_guild_config(ctx.guild.id, "autorole", True)
        await ctx.send("Success! Automatic roles are now enabled.")

    @autorole.command(name='disable')
    async def autorole_disable(self, ctx):
        """Disable automatic roles."""
        await sql.set_guild_config(ctx.guild.id, "autorole", False)
        await ctx.send("Success! Automatic roles are now disabled.")

    @autorole.command(name='add')
    async def autorole_add(self, ctx, roleid: int):
        """Add mute role for this server"""
        for role in ctx.guild.roles:
            if role.id == roleid:
                autoroles = await sql.get_autoroles(ctx.guild.id)
                autoroleid = []
                for auto in autoroles:
                    autoroleid.append(auto.id)
                if roleid in autoroleid:
                    return await ctx.send(f"{role.name} is already set as an automatic role!")
                await sql.add_autorole(ctx.guild.id, roleid)
                return await ctx.send(f"Success! `{role.name}` will now be added automatically on join.")
        await ctx.send("Role does not exist. Please try again.")

    @autorole.command(name='remove')
    async def autorole_remove(self, ctx, roleid: int):
        """Remove mute role for this server"""
        for role in ctx.guild.roles:
            if role.id == roleid:
                err = await sql.remove_autorole(ctx.guild.id, roleid)
                if err == 1:
                    return await ctx.send("There is no automatic role set for this server!")
                if err == 2:
                    return await ctx.send(f"`{role.name}` is not an automatic role!")
                if err == 0:
                    return await ctx.send(f"Success! `{role.name}` will no longer be added automatically.")
        await ctx.send("Role does not exist. Please try again.")


def setup(bot):
    bot.add_cog(Config(bot))
