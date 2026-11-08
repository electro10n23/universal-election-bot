from __future__ import annotations

from discord import Embed, Color, ButtonStyle, Interaction, Guild, Member
from discord.ui import View, button, Button, Modal, Label, TextInput

from typing import cast

from base_classes import BaseView
from database import Database

class NameAskModal(Modal, title="Set nation name for bot"):
    nation_name = Label(text="Nation Name", component=TextInput())

    async def on_submit(self, interaction: Interaction) -> None:
        guild = cast(Guild, interaction.guild)
        question = cast(TextInput, self.nation_name.component)
        answer: str = question.value

        await Database.add_nation(server_id=guild.id, nation_name=answer)

        result_embed = Embed(title="Nation added to the Election Bot!", color=Color.green())
        result_embed.add_field(name="", value=f"The nation {answer} has been added to the database.")
        await interaction.response.send_message(embed=result_embed)

class NameAskView(BaseView):
    def __init__(self):
        embed = Embed(title="Before you can use the Universal Election Bot....", color=Color.red())
        embed.add_field(name="You have to set a name for your nation that the bot will use for its operations.",
                        value="Click the \"Set Name\" button to give the bot a name for your nation.")
        super().__init__(embed=embed)

    @button(label="Set Name", style=ButtonStyle.blurple)
    async def set_nation_name(self, interaction: Interaction, button: Button):
        await interaction.response.send_modal(NameAskModal())