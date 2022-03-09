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

from typing import Optional
from datetime import datetime
from discord.utils import time_snowflake
from utils import models


def generate_id() -> int:
    return time_snowflake(datetime.now())


async def get_member(user_id: int) -> Optional[models.Member]:
    return await models.Member.get_or_none(id=user_id)


async def add_member(user_id: int) -> Optional[models.Member]:
    return await models.Member.create(id=user_id)


async def get_guild(guild_id: int) -> Optional[models.Guild]:
    return await models.Guild.get_or_none(id=guild_id)


async def add_guild(guild_id: int) -> Optional[models.Guild]:
    return await models.Guild.create(id=guild_id)


async def get_warns(user_id: int, guild_id: int) -> list[models.Warn]:
    return await models.Warn.filter(user_id=user_id, guild_id=guild_id).all()


async def add_warn(user_id: int, issuer_id: int, guild_id: int, reason: str):
    member = await get_member(user_id)
    if not member:
        await models.Member.create(id=user_id)
    issuer = await get_member(issuer_id)
    if not issuer:
        await models.Member.create(id=issuer_id)
    guild = await get_guild(guild_id)
    if not guild:
        await models.Guild.create(id=guild_id)
    await models.Warn.create(id=generate_id(), guild_id=guild_id, user_id=user_id, issuer_id=issuer_id, reason=reason)


async def remove_warn(user_id: int, guild_id: int, index: int):
    warn = await models.Warn.filter(user_id=user_id, guild_id=guild_id).offset(index - 1).first()
    await warn.delete()


async def add_modrole(guild_id: int, role_id: int) -> Optional[models.ModRole]:
    guild = await get_guild(guild_id)
    if not guild:
        await models.Guild.create(id=guild_id)
    return await models.ModRole.create(id=role_id, guild_id=guild_id)


async def remove_modrole(guild_id: int, role_id: int) -> int:
    modroles = await get_modroles(guild_id)
    if not modroles:
        return 1
    for role in modroles:
        if role_id == role.id:
            await role.delete()
            return 0
    return 2


async def get_modroles(guild_id: int) -> list[models.ModRole]:
    return await models.ModRole.filter(guild_id=guild_id).all()


async def add_muterole(guild_id: int, role_id: int) -> Optional[models.MuteRole]:
    guild = await get_guild(guild_id)
    if not guild:
        await models.Guild.create(id=guild_id)
    return await models.MuteRole.create(id=role_id, guild_id=guild_id)


async def remove_muterole(guild_id: int, role_id: int) -> int:
    muterole = await get_muterole(guild_id)
    if not muterole:
        return 1
    if muterole.id == role_id:
        await muterole.delete()
        return 0
    return 2


async def get_muterole(guild_id: int) -> Optional[models.MuteRole]:
    return await models.MuteRole.filter(guild_id=guild_id).first()


async def set_guild_config(guild_id: int, configtype: str, setval: bool):
    guild = await get_guild(guild_id)
    if not guild:
        guild = await models.Guild.create(id=guild_id)
    if configtype == "autorole":
        guild.autorole = setval
    return await guild.save()


async def get_guild_config(guild_id: int, configtype: str) -> bool:
    guild = await get_guild(guild_id)
    if not guild:
        guild = await models.Guild.create(id=guild_id)
    if configtype == "autorole":
        return guild.autorole


async def add_autorole(guild_id: int, role_id: int) -> Optional[models.AutoRole]:
    guild = await get_guild(guild_id)
    if not guild:
        await models.Guild.create(id=guild_id)
    return await models.AutoRole.create(id=role_id, guild_id=guild_id)


async def remove_autorole(guild_id: int, role_id: int) -> int:
    autorole = await get_autoroles(guild_id)
    if not autorole:
        return 1
    for role in autorole:
        if role_id == role.id:
            await role.delete()
            return 0
        return 0
    return 2


async def get_autoroles(guild_id: int) -> list[models.AutoRole]:
    return await models.AutoRole.filter(guild_id=guild_id).all()


async def add_probationrole(guild_id: int, role_id: int) -> Optional[models.ProbationRole]:
    guild = await get_guild(guild_id)
    if not guild:
        await models.Guild.create(id=guild_id)
    return await models.ProbationRole.create(id=role_id, guild_id=guild_id)


async def remove_probationrole(guild_id: int, role_id: int) -> int:
    probationrole = await get_probationrole(guild_id)
    if not probationrole:
        return 1
    if role_id == probationrole.id:
        await probationrole.delete()
        return 0
    return 2


async def get_probationrole(guild_id: int) -> list[models.ProbationRole]:
    return await models.ProbationRole.filter(guild_id=guild_id).first()
