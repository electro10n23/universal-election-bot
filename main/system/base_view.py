from discord import Embed
from discord.ui import View

# A view that holds an embed
class BaseView(View):
    def __init__(self, embed):
        self.embed = embed

    # MAYBE: add refresh() which generates an embed based on data inputted.