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
from utils.modutil import autorole_enabled
from utils.sql import get_autoroles


class Newcomers(commands.Cog):
    """
    Automatic roles!
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if await autorole_enabled(member.guild.id):
            roles = await get_autoroles(member.guild.id)
            for role in roles:
                await member.add_roles(member.guild.get_role(role.id))


def setup(bot):
    bot.add_cog(Newcomers(bot))
