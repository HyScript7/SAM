from contextlib import asynccontextmanager
from typing import AsyncGenerator

import discord
from discord.ext import commands

from ...internal import database, logger_config
from .services import WarnService

logger = logger_config.logger.getChild("warnings")


DEFAULT_REASON_WHEN_MISSING = "No reason specified."


class Warnings(commands.Cog):
    def __init__(
        self, bot: commands.Bot, warn_service: type[WarnService] = WarnService
    ):
        self.bot = bot
        self.svc = warn_service

    @asynccontextmanager
    async def get_service(self) -> AsyncGenerator[WarnService, None]:
        async with database.get_session() as session:
            yield WarnService(session)

    @commands.hybrid_group(
        name="warnings",
        usage="warnings ((add <user> [reason]|remove <user> <case_id> [reason])|(list|clear <user>)|view <case_id>)",
        description="description",
    )
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def root(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @root.command("add")
    @commands.guild_only()
    async def _add(
        self, ctx: commands.Context, user: discord.User, *, reason: str | None = None
    ):
        assert ctx.guild is not None
        if reason is None:
            reason = DEFAULT_REASON_WHEN_MISSING

        async with self.get_service() as svc:
            await svc.issue_warning(user.id, ctx.guild.id, ctx.author.id, reason)
        # TODO: Embed
        await ctx.send(f"Warned {user.mention} for `{reason}`")
        # TODO: Message moderated user

    @root.command("remove")
    @commands.guild_only()
    async def _remove(
        self,
        ctx: commands.Context,
        user: discord.User,
        case_id: int,
        *,
        reason: str | None = None,
    ):
        assert ctx.guild is not None
        if reason is None:
            reason = DEFAULT_REASON_WHEN_MISSING
        try:
            async with self.get_service() as svc:
                await svc.recall_warning(case_id, ctx.guild.id, ctx.author.id, reason)
        except ValueError as e:
            # TODO: Embed
            await ctx.send(f"Cannot remove this warning: {e}")
        else:
            # TODO: Embed
            await ctx.send(
                f"Removed warning from {user.mention} with reason `{reason}`"
            )
            # TODO: Message moderated user

    @root.command("list")
    @commands.guild_only()
    async def _list(self, ctx: commands.Context, user: discord.User):
        assert ctx.guild is not None
        async with self.get_service() as svc:
            warnings = await svc.get_warnings_for_user(user.id, ctx.guild.id)
        # TODO: Embed, pagination
        await ctx.send("\n".join(map(str, warnings)))

    @root.command("clear")
    @commands.guild_only()
    async def _clear(
        self, ctx: commands.Context, user: discord.User, *, reason: str | None = None
    ):
        assert ctx.guild is not None
        async with self.get_service() as svc:
            await svc.clear_warnings_for_user(
                user.id,
                ctx.guild.id,
                ctx.author.id,
                reason or DEFAULT_REASON_WHEN_MISSING,
            )
        # TODO: Embed
        await ctx.send(f"Cleared warnings for {user.mention} with note `{reason}`")
        # TODO: Message moderated user

    @root.command("view")
    @commands.guild_only()
    async def _view(self, ctx: commands.Context, case_id: int):
        assert ctx.guild is not None
        try:
            async with self.get_service() as svc:
                warning = await svc.get_warning(case_id, ctx.guild.id)
        except ValueError as e:
            # TODO: Embed
            await ctx.send(f"Cannot view this warning: {e}")
        else:
            # TODO: Embed
            await ctx.send(str(warning))
