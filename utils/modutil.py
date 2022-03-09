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

from utils import sql


async def is_muted(ctx, member):
    muterole = await sql.get_muterole(ctx.guild.id)
    for role in member.roles:
        if muterole.id == role.id:
            return True
    return False


async def mute_role_exists(ctx):
    muterole = await sql.get_muterole(ctx.guild.id)
    if muterole:
        return True
    return False


async def mute_member(ctx, member):
    muterole = await sql.get_muterole(ctx.guild.id)
    role = ctx.guild.get_role(muterole.id)
    return await member.add_roles(role)


async def unmute_member(ctx, member):
    muterole = await sql.get_muterole(ctx.guild.id)
    role = ctx.guild.get_role(muterole.id)
    return await member.remove_roles(role)


async def check_if_staff(ctx, member):
    if member == ctx.guild.owner:
        return True
    else:
        modroles = await sql.get_modroles(ctx.guild.id)
        modroleid = []
        for role in modroles:
            modroleid.append(role.id)
        for role in member.roles:
            if role.id in modroleid:
                return True
    return False


async def autorole_enabled(guild_id):
    guild = await sql.get_guild(guild_id)
    if not guild:
        guild = await sql.add_guild(guild_id)
    if guild.autorole:
        autorole = await sql.get_autoroles(guild_id)
        if autorole:
            return True
    return False
