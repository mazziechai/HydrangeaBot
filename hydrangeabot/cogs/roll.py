import xdice
from discord import ApplicationContext, Option, SlashCommandGroup
from discord.ext import commands

from ..bot import HydrangeaBot
from ..db import db_get_user


async def _roll(ctx: ApplicationContext, string: str):
    try:
        result = xdice.roll(string)

        await ctx.respond(f"Result: `{result.format()} = {result}`")
    except TypeError:
        await ctx.respond("That is not a valid dice roll!")


class RollCog(commands.Cog):
    def __init__(self, bot: HydrangeaBot):
        self.bot = bot

    macro_group = SlashCommandGroup("macro", "Managing and using rolling macros")

    @commands.slash_command(description="Rolls a dice using the XdY format.")
    async def roll(
        self, ctx: ApplicationContext, *, string: Option(str, "The roll in XdY format.")  # type: ignore
    ):  # type: ignore
        await _roll(ctx, string)

    @macro_group.command(description="Create a macro")
    async def new(
        self,
        ctx: ApplicationContext,
        name: Option(str, "The name of the macro."),  # type: ignore
        macro: Option(str, "The roll to make when using this macro."),  # type: ignore
    ):
        # Test the macro if it's a valid roll
        try:
            xdice.Pattern.compile(macro)
        except Exception:
            await ctx.respond("That is not a valid dice roll!", ephemeral=True)
            return

        # Add the macro to the user's macros dict
        user = db_get_user(snowflake=ctx.user.id)
        user.macros[name] = macro
        user.save()

        await ctx.respond(f"Successfully created macro `{macro}` as `{name}`!")

    @macro_group.command(description="Run a macro")
    async def run(
        self, ctx: ApplicationContext, name: Option(str, "The name of the macro.")  # type: ignore
    ):
        # Grab the macro from the user's document
        user = db_get_user(snowflake=ctx.user.id)
        try:
            macro = user.macros[name]
        except KeyError:
            await ctx.respond("That is not a valid macro!", ephemeral=True)
            return

        await _roll(ctx, macro)

    @macro_group.command(description="Delete a macro")
    async def delete(
        self, ctx: ApplicationContext, name: Option(str, "The name of the macro.")  # type: ignore
    ):
        # Grab the macro from the user's document
        user = db_get_user(snowflake=ctx.user.id)
        try:
            user.macros.pop(name)
            user.save()
        except KeyError:
            await ctx.respond("That is not a valid macro!", ephemeral=True)
            return

        await ctx.respond(f"Macro `{name}` deleted!")


def setup(bot: HydrangeaBot):
    bot.add_cog(RollCog(bot))
