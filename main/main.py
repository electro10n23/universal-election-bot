from __future__ import annotations

# Imports from packages/libraries.
from discord import Intents, Embed, Color, Interaction, Guild, Member
from discord.app_commands import AppCommand
from discord.ext.commands import AutoShardedBot, Context

# Imports from within project.
from system.misc_embeds import ErrorEmbed
from system.ids import dev_ids, TEST_SERVER_ID
from tests.test_embeds import test_sync_error_embed, MismatchError
from system.misc_views import NameAskView

from typing import cast

from database import Database, DatabaseView

bot = AutoShardedBot(command_prefix="!", intents=Intents.all())

# When the bot joins the guild, it will ask the server owner for the name of the nation before the
# nation is added to the database.
@bot.event
async def on_guild_join(guild: Guild):
    owner = cast(Member, guild.owner) # Done so line after doesn't error since it would think owner was None

    name_ask_view = NameAskView(guild_id=guild.id)
    await owner.send(view=name_ask_view, embed=name_ask_view.embed)

# Creates a string from a list of application commands that were just synced.
def gather_command_names(synced_commands: list[AppCommand]) -> str:
    command_name_holder = "Synced commands:"

    for command in synced_commands:
        if synced_commands[len(synced_commands) - 1] == command:
            command_name_holder += f" and '{command.name}'"
        else:
            command_name_holder += f" '{command.name},'"

    return command_name_holder

# Syncs the bot's command tree with Discord.
@bot.command(name="sync")
async def sync(ctx: Context):
    guild_id: int = ctx.guild.id #type: ignore
    user_id: int = ctx.author.id

    if guild_id == TEST_SERVER_ID and user_id in dev_ids:
        embed = Embed(color=Color.green(), title="Commands synced!")

        commands = await bot.tree.sync()
        sync_result_message = gather_command_names(commands)

        embed.add_field(name="", value=sync_result_message)

        await ctx.send(embed=embed)
    else:
        embed = ErrorEmbed(title="Cannot sync application commands!", 
                            msg="You do not have permission to sync commands.")
    
        try:
            test_sync_error_embed(embed)
            await ctx.send(embed=embed)
        except MismatchError as exception:
            mismatched_attributes = ""
            for expected_result, actual_result in exception.mismatch_dict.items():
                mismatched_attributes += f"{expected_result} | {actual_result}\n"
            await ctx.send(content=f"{exception.msg}\n{mismatched_attributes}")


# TO DO FOR FUNCTIONS BELOW, add exceptions in SQLITE backend classes and in these to handle when
# nation hasn't been set up yet (probably just exceptions that pop up when the nation hasn't been
# found in database.)

# Command that allows user to see all nation databases within the wider SQLite database. It also provides actions for
# the user to use for each nation and allows them edit stuff within a nation's database. (ONLY FOR DEVELOPERS, MUST BE
# MADE VERY SECURE!!!!!!!!). Will be done only in development server
@bot.tree.command(name="show_nations", description="DEVELOPER ONLY COMMAND!!!!")
async def show_nations(interaction: Interaction):
    view = await DatabaseView.create()
    await interaction.response.send_message(view=view, embed=view.embed)

# Command that allows any user to see a nation's database within that nation's Discord 
# server. It also provides actions for the user to do on nation database.
@bot.tree.command(name="show_database")
async def show_elections(interaction: Interaction):
    pass

with open(r"main\xan_nara\token.txt") as file:
    token: str = file.read()

bot.run(token=token)