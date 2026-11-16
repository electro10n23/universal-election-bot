from __future__ import annotations

from discord import Embed, Color
from discord.ui import View

from aiosqlite import connect

from system.ids import path
from system.base_classes import BaseObject, BaseView, ObjectNotFound

class Nation(BaseObject): 
    def __init__(self, nation_id: int, nation_name: str) -> None:
        super().__init__()
        self.nation_id = nation_id
        self.nation_name = nation_name

    @classmethod
    async def create(cls, *, nation_id: int, nation_name: str) -> Nation:
        return cls(nation_id, nation_name)

    async def add_election(self):
        pass

class NationView(BaseView):
    def __init__(self, nation: Nation) -> None:
        embed = Embed()
        super().__init__(embed=Embed(title="Election Database (TEST)",
                                     description="A table of all nation servers using the Universal Election Bot", 
                                     color=Color.blue()))
        self.nation = nation

class NationNotFound(ObjectNotFound):
    def __init__(self, nation_id: int) -> None:
        super().__init__(msg=f"The nation with the ID {nation_id} could not be found")