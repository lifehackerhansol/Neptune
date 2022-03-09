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

from tortoise import fields
from tortoise.models import Model


class Member(Model):
    id = fields.BigIntField(pk=True)

    class Meta:
        table = "members"


class Guild(Model):
    id = fields.BigIntField(pk=True)
    autorole = fields.BooleanField(default=False)

    class Meta:
        table = "guild"


class Warn(Model):
    id = fields.IntField(pk=True)
    guild = fields.ForeignKeyField('models.Guild')
    user = fields.ForeignKeyField('models.Member', related_name="user")
    issuer = fields.ForeignKeyField('models.Member', related_name="issuer")
    reason = fields.CharField(1024)

    class Meta:
        table = "warn"


class ModRole(Model):
    id = fields.BigIntField(pk=True)
    guild = fields.ForeignKeyField('models.Guild')

    class Meta:
        table = "modrole"


class MuteRole(Model):
    id = fields.BigIntField(pk=True)
    guild = fields.ForeignKeyField('models.Guild')

    class Meta:
        table = "muterole"


class AutoRole(Model):
    id = fields.BigIntField(pk=True)
    guild = fields.ForeignKeyField('models.Guild')

    class Meta:
        table = "autorole"


class ProbationRole(Model):
    id = fields.BigIntField(pk=True)
    guild = fields.ForeignKeyField('models.Guild')

    class Meta:
        table = "probationrole"
