import discord


class CharacterCreationModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Name", max_length=50))
        self.add_item(
            discord.ui.InputText(
                label="Description",
                style=discord.InputTextStyle.long,
                max_length=1000,
                required=False,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            content=f"Created a new character named {self.children[0].value}!"
            "Use the commands under `/character field` to manage properties of your character.",
            ephemeral=True,
        )
        self.stop()
