from discord import Embed
from discord.ui import View

# The base class for all objects
class BaseObject():
    pass

# The base table exists to represent a SQLite table instead of a 2D list because all of the info from 
# each row of a table will be put into its own object instead of being kept as just a list, so there's
# no need to have that extra overhead. However, we need to know the names of each column in the table
# to get an attribute dynamically with __getattribute__(), so thats why column names exist.
class BaseTable[O: BaseObject](list[O]):
    def __init__(self, column_names: list[str]):
        self.column_names = column_names

# A view that holds an embed
class BaseView(View):
    def __init__(self, embed: Embed):
        self.embed = embed

    # MAYBE: add refresh() which generates an embed based on data inputted.