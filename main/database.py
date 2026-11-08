from __future__ import annotations

# Outside packages/libraries
from discord import Embed
from discord.ui import View
from aiosqlite import Connection, connect
from typing import Any, NewType

# From within project
from system.base_classes import BaseView, BaseTable
from system.ids import path

from nation_essentials.nation import Nation

class DatabaseTable(BaseTable[Nation]): 
    """
    The list representation of a table in the SQLite table "Database" for the bot. It contains
    Nation objects which each represent a row in the table, and which attribute names correspond
    to the names of the columns in the table
    
    **How the table is set up in the SQLite database:**

    ```
    DATABASE TABLE
    +-----------------------------------------+
    | nation_id   |   nation_name             |
    | (server id) |   (given name for nation) |
    | ----------------------------------------|
    | [INTEGER]   |   [TEXT]                  |
    | ...         |   ...                     |
    +-----------------------------------------+
    ```

    Attributes:
        column_names(list[str]): A list containing the names of all columns in the Database table, listed in the same order they appear in the SQLite table.
    """
    
    def __init__(self):
        super().__init__(column_names=["nation_id", "nation_name"])

# Container for methods that query and modify nations within the SQLite database
class Database():
    """
    Container class for methods that query and modify tables given to each nation Discord server that
    has the Universal Election Bot added within the table Database, a table containing entires for
    all nation Discord servers which have the bot and which points to nation tables, in the SQLite
    database attached to the bot.
    """

    """
    FOR REFERENCE WHEN DEALING WITH Database TABLE!!!

    TABLE SETUP

    nation_id    nation_name
    (server id)  (given name for nation)
    ========================
    [INTEGER]    [TEXT]
    """

    @classmethod
    async def gather_table(cls) -> DatabaseTable:
        """
        A class method that gathers all rows from the Database table and returns them in a list

        Returns:
            list(DatabaseTable): A list of Nations representing the Database table in the SQLite database.
        """
        connection = await connect(path)
        database_table = DatabaseTable()

        async with connection.execute("SELECT * FROM Database") as cursor:
            async for row in cursor:
                nation_id: int = row[0]
                nation_name: str = row[1]

                nation = await Nation.create(nation_id=nation_id, nation_name=nation_name)
                database_table.append(nation)

        return database_table

    # Class method that adds a nation's Discord server to the database
    @classmethod
    async def add_nation(cls, server_id: int, nation_name: str) -> None:
        """
        A class method that adds a entry for a nation server in the Database table and creates
        a new table for the nation server.

        Parameters:
            server_id(int): The ID of the server that will be added.
            nation_name(str): The name of the server given by the server owner upon bot joining server in DMs
        """
        connection = await connect(path)

        await connection.execute(f"""INSERT INTO Database (nation_id, nation_name) 
                            VALUES ({server_id}, {nation_name})""")
        await connection.commit()

        # Election parameters will hold extra setting to customize how a election system operates in
        # a JSON string specific to each system. Status will hold a string which corresponds to a enum
        # value.

        # MAYBE: election_system holds enum value, which then leads to class for electoral system
        # Ex: gets ElectoralSystemEnum.FPTP, then creates an FPTP() object or uses a method in
        # container class FPTP()
        await connection.execute(f"""CREATE TABLE IF NOT EXISTS {nation_name}_{server_id}
                                    (INTEGER election_id NOT NULL UNIQUE,
                                     TEXT election_name NOT NULL,
                                     TEXT election_system NOT NULL,
                                     TEXT election_parameters NOT NULL,
                                     TEXT run_status NOT NULL,
                                     TEXT start_date,
                                     TEXT end_date,
                                     PRIMARY KEY("election_id") 
                                    )""")
        await connection.close()

# A view that shows all the nations in the database via an embed in attributes
class DatabaseView(BaseView):
    def __init__(self, embed: Embed):
        super().__init__(embed)