import lightbulb
import hikari
import string

import controller
from hikari_bot import bot

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Build", description="Build something.")

# Creates a command in the plugin
@plugin.command
@lightbulb.option("building", description="The building to create.", choices=["Road", "Settlement", "City", "Development Card"], required=True)
@lightbulb.option("location", description="The location of the building.", required=True)
@lightbulb.option("location_2_road", description="2nd point if building a road.", required=False)
@lightbulb.command("build", description="Build something", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def build(ctx: lightbulb.Context) -> None:
    """Build something.

    Called via the discord command '/build <building> <location>'.
    """

    ctrl = bot.ctrl

    location_1 = (list(string.ascii_uppercase).index(ctx.options.location[0]), int(ctx.options.location[1:]))
    location_2 = None
    print(location_1)

    # Must input 2 locations if building a road
    if ctx.options.building == "Road" and ctx.options.location_2_road == None:
        await ctx.respond(content=hikari.Embed(
                title="Error!",
                description=f"You must input 2 locations when building a road.",
                color=hikari.Color(0xFF0000)))

        return
    else:
        location_2 = (list(string.ascii_uppercase).index(ctx.options.location_2_road[0]), int(ctx.options.location_2_road[1:]))
        print(location_2)

    try:
        ctrl.build(str(ctx.author).split("#")[0], ctx.options.building, location_1, location_2)
        await bot.bot.rest.create_message(ctx.channel_id, content=f"ADDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
    except controller.Resource:
        await ctx.respond(content=hikari.Embed(
                title="Error!",
                description=f"You do not have the necessary resources to build a {ctx.options.building}.",
                color=hikari.Color(0xFF0000)))
    except:
        raise Exception(f"Failed to build {ctx.options.building}.")
    

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)