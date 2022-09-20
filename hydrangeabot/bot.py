import logging
import traceback
import uuid

import discord

from .db import Users


class HydrangeaBot(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.log = logging.getLogger("hydrangeabot")

        # Loading every cog in the cogs folder
        cogs = ["roll"]

        for cog in cogs:
            self.load_extensions(f"hydrangeabot.cogs.{cog}")

    async def on_ready(self):
        self.log.info("Logged in!")

    async def on_application_command(self, ctx: discord.ApplicationContext):
        # Create a new User for first time command runners.
        if Users.objects(snowflake=ctx.user.id).count() == 0:  # type: ignore
            Users(snowflake=ctx.user.id).save()

    async def on_application_command_error(
        self, ctx: discord.ApplicationContext, error
    ):
        # Prints traceback info to the user.
        if isinstance(error, discord.ApplicationCommandError):
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
