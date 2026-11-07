from discord import Embed
from discord.ui import View

# The base class for all objects
class BaseObject():
    pass

class BaseTable[O: BaseObject](list[O]):
    pass

# A view that holds an embed
class BaseView(View):
    def __init__(self, embed):
        self.embed = embed

    # MAYBE: add refresh() which generates an embed based on data inputted.