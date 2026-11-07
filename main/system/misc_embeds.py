from discord import Embed, Color
from discord.ui import View, Button

# Creates an embed that displays something has gone wrong with the program to the user.
class ErrorEmbed(Embed):
    def __init__(self, *, title: str, msg: str):
        super().__init__(color=Color.red(), title=f"⚠️ {title} ⚠️")
        self.add_field(name="", value=msg)