from __future__ import annotations

from discord import Embed, Color, ButtonStyle, Interaction, Guild, Member
from discord.ui import View, button, Button, Modal, Label, TextInput

from typing import cast

from system.base_classes import BaseView
from database import Database

class NameAskModal(Modal, title="Set nation name for bot"):
    """
    This modal is where the server owner submits the name they want to give to their nation in the bot's
    database. It then adds the nation into the database.

    Attributes:
        nation_name(discord.ui.Label): The container for the question in which the server owner inputs the name of their nation
    """

    def __init__(self, guild_id: int):
        super().__init__()
        self.guild_id = guild_id

    nation_name = Label(text="Nation Name", component=TextInput())

    async def on_submit(self, interaction: Interaction) -> None:
        guild = cast(Guild, interaction.guild)
        question = cast(TextInput, self.nation_name.component)
        answer: str = question.value

        await Database.add_nation(server_id=self.guild_id, nation_name=answer)

        result_embed = Embed(title="Nation added to the Election Bot!", color=Color.green())
        result_embed.add_field(name="", value=f"The nation {answer} has been added to the database.")
        await interaction.response.send_message(embed=result_embed)

class NameAskView(BaseView):
    """
    This view is where the server owner can submit their nation's name so that their nation can be
    added to the bot.

    Attributes:
        embed(discord.Embed): The embed that is shown to server owner along with the view.
    """
    def __init__(self, guild_id: int):
        embed = Embed(title="Before you can use the Universal Election Bot....", color=Color.red())
        embed.add_field(name="You have to set a name for your nation that the bot will use for its operations.",
                        value="Click the \"Set Name\" button to give the bot a name for your nation.")
        super().__init__(embed=embed)
        self.guild_id = guild_id

    @button(label="Set Name", style=ButtonStyle.blurple)
    async def set_nation_name(self, interaction: Interaction, button: Button):
        await interaction.response.send_modal(NameAskModal(self.guild_id))