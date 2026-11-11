from __future__ import annotations

from aiosqlite import connect

from system.ids import path
from system.base_classes import BaseObject

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