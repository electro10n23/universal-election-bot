# Outside packages/libraries
from discord import Embed
from discord.ui import View
from aiosqlite import Connection, connect

# From within project
from system.base_view import BaseView
from system.ids import path

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
    async def gather_table(cls): # -> some sort of list, not sure yet.
        """
        A class method that gathers all rows from the Database table and returns them in a list

        Returns:
            list: Some sort of list
        """
        connection = await connect(path)

        async with connection.execute("SELECT * FROM Database") as cursor:
            async for row in cursor:
                pass

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
        await connection.execute(f"""CREATE TABLE IF NOT EXISTS Nation_{server_id}
                                    (INTEGER election_id,
                                     TEXT election_name
                                     TEXT election_system
                                     TEXT election_parameters
                                     TEXT run_status
                                     TEXT start_date
                                     TEXT end_date 
                                    )""")
        await connection.close()

# A view that shows all the nations in the database via an embed in attributes
class DatabaseView(BaseView):
    def __init__(self, embed: Embed):
        super().__init__(embed)