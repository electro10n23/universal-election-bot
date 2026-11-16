from discord import Embed
from discord.ui import View

from typing import Any

# The base class for all objects
class BaseObject():
    pass

# Table is a dictionary with string keys and list values that is used only to parse the contents of
# a table in the SQLite database to a format that can be put into a embed and shown to the user. The 
# string keys contains the names of the columns in the SQLite database. The list value the key
# corresponds to contains the value each row in a table has in the column the key represents.
type Table = (dict[str, list[Any]])

# A view that holds an embed.
class BaseView(View):
    def __init__(self, embed: Embed):
        super().__init__()
        self.embed = embed

# An exception that is raised when an object in the bot is not found in the SQLite database.
class ObjectNotFound(ValueError):
    def __init__(self, msg) -> None:
        self.msg = msg
        super().__init__(msg)