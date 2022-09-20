import logging
import traceback
import uuid

import discord
from discord.ext import commands

from .db import User


class HydrangeaBot(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.log = logging.getLogger("hydrangeabot")

        # Loading every cog in the cogs folder
        cogs = ["roll", "character"]

        for cog in cogs:
            self.load_extensions(f"hydrangeabot.cogs.{cog}")

    async def on_ready(self):
        self.log.info("Logged in!")

    async def on_application_command(self, ctx: discord.ApplicationContext):
        # Create a new User for first time command runners.
        if User.objects(snowflake=ctx.user.id).first() is None:  # type: ignore
            User(snowflake=ctx.user.id).save()

    async def on_application_command_error(
        self, ctx: discord.ApplicationContext, error
    ):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.respond(
                "This command can only be used in a DM with the bot.", ephemeral=True
            )

        # Lets us know if it's an invoke error with an error ID.
        if isinstance(error, discord.ApplicationCommandInvokeError):
            error_id = uuid.uuid4()

            self.log.exception(
                f"Exception from {ctx.command.qualified_name}!\n"
                f"{''.join(traceback.format_exception(type(error), error, error.__traceback__))}"
                f"Error ID: {error_id}"
            )

            await ctx.respond(
                f"Exception `{error.args}` from {ctx.command.qualified_name}!\n"
                f"Error ID: `{error_id}`\n"
                "Please direct the error ID to `nano ferret#8613` for debugging."
            )
