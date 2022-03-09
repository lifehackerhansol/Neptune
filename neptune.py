#!/usr/bin/env python3

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

import os
import json
import discord
import aiohttp
import asyncio

from discord.ext import commands
from tortoise import Tortoise
from aerich import Command
from utils.utils import create_error_embed
from tortoiseconf import TORTOISE_ORM


async def init():
    print('Initializing SQLite DB...')
    if os.path.isfile("neptune.db") and os.path.isdir("migrations/models"):
        print("Updating SQLite DB...")
        command = Command(tortoise_config=TORTOISE_ORM, app='models')
        await command.init()
        await command.upgrade()
    await Tortoise.init(config=TORTOISE_ORM)
    # Generate the schema
    await Tortoise.generate_schemas()


class Neptune(commands.Bot):
    def __init__(self, command_prefix):
        intents = discord.Intents(guilds=True, members=True, bans=True, messages=True, message_content=True)
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False)
        super().__init__(
            command_prefix=command_prefix,
            intents=intents,
            allowed_mentions=allowed_mentions,
            status=discord.Status.online,
            case_insensitive=True
        )
        self.session = aiohttp.ClientSession()

    def load_cogs(self):
        cog = ""
        for filename in os.listdir("./cogs"):
            try:
                if filename.endswith(".py"):
                    cog = f"cogs.{filename[:-3]}"
                    self.load_extension(cog)
                    print(f"Loaded cog cogs.{filename[:-3]}")
            except Exception as e:
                exc = "{}: {}".format(type(e).__name__, e)
                print("Failed to load cog {}\n{}".format(cog, exc))
        try:
            cog = "jishaku"
            self.load_extension("jishaku")
            print("Loaded cog jishaku")
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load cog {}\n{}".format(cog, exc))

    async def close(self):
        await self.session.close()
        await super().close()

    async def on_ready(self):
        print("Neptune ready.")

    async def on_command_error(self, ctx: commands.Context, exc: commands.CommandInvokeError):
        author: discord.Member = ctx.author
        command: commands.Command = ctx.command or '<unknown cmd>'
        exc = getattr(exc, 'original', exc)
        channel = ctx.channel

        if isinstance(exc, commands.CommandNotFound):
            return

        elif isinstance(exc, commands.ArgumentParsingError):
            await ctx.send_help(ctx.command)

        elif isinstance(exc, commands.NoPrivateMessage):
            await ctx.send(f'`{command}` cannot be used in direct messages.')

        elif isinstance(exc, commands.MissingPermissions):
            await ctx.send(f"{author.mention} You don't have permission to use `{command}`.")

        elif isinstance(exc, commands.CheckFailure):
            await ctx.send(f'{author.mention} You cannot use `{command}`.')

        elif isinstance(exc, commands.BadArgument):
            await ctx.send(f'{author.mention} A bad argument was given: `{exc}`\n')
            await ctx.send_help(ctx.command)

        elif isinstance(exc, commands.BadUnionArgument):
            await ctx.send(f'{author.mention} A bad argument was given: `{exc}`\n')

        elif isinstance(exc, commands.BadLiteralArgument):
            await ctx.send(f'{author.mention} A bad argument was given, expected one of {", ".join(exc.literals)}')

        elif isinstance(exc, commands.MissingRequiredArgument):
            await ctx.send(f'{author.mention} You are missing required argument {exc.param.name}.\n')
            await ctx.send_help(ctx.command)

        elif isinstance(exc, discord.NotFound):
            await ctx.send("ID not found.")

        elif isinstance(exc, discord.Forbidden):
            await ctx.send(f"💢 I can't help you if you don't let me!\n`{exc.text}`.")

        elif isinstance(exc, commands.CommandInvokeError):
            await ctx.send(f'{author.mention} `{command}` raised an exception during usage')
            embed = create_error_embed(ctx, exc)
            await channel.send(embed=embed)
        else:
            await ctx.send(f'{author.mention} Unexpected exception occurred while using the command `{command}`')
            embed = create_error_embed(ctx, exc)
            await channel.send(embed=embed)


async def mainprocess():
    await init()
    f = open("config.json")
    configuration = json.load(f)
    f.close()
    bot = Neptune([x for x in configuration['PREFIX']])
    bot.help_command = commands.DefaultHelpCommand()
    print('Starting Neptune...')
    bot.load_cogs()
    await bot.start(configuration['TOKEN'])
    await Tortoise.close_connections()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mainprocess())
