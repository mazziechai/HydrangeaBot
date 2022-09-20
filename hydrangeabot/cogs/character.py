import json

from discord import ApplicationContext, Attachment, Option, SlashCommandGroup
from discord.ext import commands

from ..bot import HydrangeaBot
from ..db import Character, CharacterSchema, db_get_user
from ..ui import CharacterCreationModal


class CharacterCog(commands.Cog):
    def __init__(self, bot: HydrangeaBot):
        self.bot = bot

    character_group = SlashCommandGroup("character", "Manage character sheets")
    schema_group = SlashCommandGroup("schema", "Manage character sheet schemas")
    schema_new_group = schema_group.create_subgroup(
        name="new", description="Create a new schema"
    )

    # @commands.dm_only()
    @character_group.command(name="new", description="Creates a new character")
    async def character_new(self, ctx: ApplicationContext):
        modal = CharacterCreationModal(title="Basic character information")

        # Send the prompt for the name and description
        await ctx.send_modal(modal)
        await modal.wait()

        Character(
            creator=db_get_user(snowflake=ctx.user.id),
            name=modal.children[0].value,
            description=modal.children[1].value,
        ).save()

    @character_group.command(name="list", description="Lists your characters")
    async def character_list(self, ctx: ApplicationContext):
        # TODO: Properly implement this
        await ctx.respond(f"{[character.name for character in Character.objects(creator=ctx.user.id)]}")  # type: ignore

    @schema_new_group.command(
        name="file", description="Creates a new character schema with a JSON file"
    )
    async def schema_new_file(self, ctx: ApplicationContext, name: Option(str), file: Option(Attachment)):  # type: ignore
        if file.size > 4096:
            await ctx.respond("This file is exceeds the file size limit of 4kb.")
            return

        # Get the JSON file as bytes
        json_bytes = await file.read()

        CharacterSchema(
            creator=db_get_user(snowflake=ctx.user.id),
            name=name,
            json=json_bytes,
            schema=json.loads(json_bytes),
        ).save()

        await ctx.respond(
            f"Created a new schema `{name}`!\n"
            f"You can view the schema with `/schema view {name}`."
        )


def setup(bot: HydrangeaBot):
    bot.add_cog(CharacterCog(bot))
