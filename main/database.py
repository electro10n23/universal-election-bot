from __future__ import annotations

# Outside packages/libraries
from discord import Embed, Color
from discord.ui import View
from aiosqlite import Connection, connect, Row
from typing import Any, NewType, cast

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

                print(f"ID: {nation_id}, Name: {nation_name}")

                nation = await Nation.create(nation_id=nation_id, nation_name=nation_name)

                print(f"(from nation obj) ID: {nation.nation_id}, Name: {nation.nation_name}")
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

        await connection.execute(f"INSERT INTO Database VALUES ({server_id}, \"{nation_name}\")")
        await connection.commit()

        # Election parameters will hold extra setting to customize how a election system operates in
        # a JSON string specific to each system. Status will hold a string which corresponds to a enum
        # value.

        # MAYBE: election_system holds enum value, which then leads to class for electoral system
        # Ex: gets ElectoralSystemEnum.FPTP, then creates an FPTP() object or uses a method in
        # container class FPTP()
        await connection.execute(f"""CREATE TABLE IF NOT EXISTS "{nation_name}_{server_id}"
                                    (election_id INTEGER NOT NULL UNIQUE,
                                     election_name TEXT NOT NULL,
                                     election_system TEXT NOT NULL,
                                     election_parameters TEXT NOT NULL,
                                     run_status TEXT NOT NULL,
                                     start_date TEXT,
                                     end_date TEXT,
                                     PRIMARY KEY("election_id") 
                                    )""")
        await connection.close()

        @classmethod
        async def get_nation(cls, server_id: int) -> Nation:
            """
            A class method that uses the server_id to query the Database table for the needed row, then uses
            column values of the row to make a Nation object.
    
            Parameters:
                server_id(int): The ID of the server being looked for.

            Returns:
                A Nation object representing the row in the Database table.
            """
            connection = connect(path)

            cursor = await connection.execute(f"SELECT * FROM Database WHERE id = {server_id}")
            row = cast(Row, await cursor.fetchone())

            nation_id: int = row[0]
            nation_name: str = row[1]

            nation = await Nation.create(nation_id=nation_id, nation_name=nation_name)
            return nation

# A view that shows all the nations in the database via an embed in attributes
class DatabaseView(BaseView):
    def __init__(self, database_table: DatabaseTable):
        self.database_table = database_table
        # Usually I would add a separate int variable to move between columns, but that isnt neccessary here 
        # since there will only be 2 columns, below the mininum amount of inline fields Discord allows in an
        # embed, 3.
        self.page_number = 1
        super().__init__(embed=Embed(title="Nation Database (ONLY FOR DEVS)",
                                     description="A table of all nation servers using the Universal Election Bot", 
                                     color=Color.blue()))
        self.refresh_page()

    def refresh_page(self):
        self.embed.clear_fields()
        self.embed.add_field(name=f"Page {self.page_number}", value="", inline=False)

        page_start = 25 * (self.page_number-1)

        if len(self.database_table) < 25 * self.page_number:
            page_stop = len(self.database_table)
        else:
            page_stop = 25 * self.page_number

        field_value = ""

        for column in self.database_table.column_names:
            for i in range(page_start, page_stop):
                nation = self.database_table[i]
                field_value += str(nation.__getattribute__(column))

            self.embed.add_field(name=column, value=field_value, inline=True)
            field_value = ""