import string
import traceback

import lightbulb
import hikari

import src.controller as controller
import src.hikari_bot.bot as bot

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Build", description="Build something.")

# Creates a command in the plugin
@plugin.command
@lightbulb.option("location_2", description="2nd point if building a road.", default=None)
@lightbulb.option("location_1", description="The location of the building.", default=None)
@lightbulb.option("building", description="The building to create.", choices=["Road", "Settlement", "City", "Development Card"], required=True)
@lightbulb.command("build", description="Build something")
@lightbulb.implements(lightbulb.SlashCommand)
async def build(ctx: lightbulb.Context) -> None:
    """Build something.

    Called via the discord command '/build <building> <location>'.
    """

    ctrl = bot.ctrl
    name = str(ctx.author).split("#")[0]

    location_1 = None
    location_2 = None

    # must be in the game to build
    try:
        ctrl.get_player(name)
    except Exception:
        await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=hikari.Embed(
                title="Error!",
                description=f"You are not in the game.",
                color=hikari.Color(0xFF0000)))
        return

    # must be your turn to move
    if ctrl.players[ctrl.current_player].name != name:
        await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=hikari.Embed(
                title="Error!",
                description=f"You cannot build on someone elses turn.",
                color=hikari.Color(0xFF0000)))
        return

    # Must input location_1 if building a road, settlement, or city
    if ctx.options.building != "Development Card" and ctx.options.location_1 is None:
        await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=hikari.Embed(
                title="Error!",
                description=f"You must input location_1 when building a road, settlement, or city.",
                color=hikari.Color(0xFF0000)))
        return
    elif ctx.options.building != "Development Card":
        location_1 = (list(string.ascii_uppercase).index(ctx.options.location_1[0].upper()), int(ctx.options.location_1[1:]))

    # Must input location_2 if building a road
    if ctx.options.building == "Road" and ctx.options.location_2 is None:
        await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=hikari.Embed(
                title="Error!",
                description=f"You must input location_2 when building a road.",
                color=hikari.Color(0xFF0000)))
        return
    elif ctx.options.building == "Road":
        location_2 = (list(string.ascii_uppercase).index(ctx.options.location_2[0].upper()), int(ctx.options.location_2[1:]))

    try:
        bought_card = ctrl.build(str(ctx.author).split("#")[0], ctx.options.building, location_1, location_2)

        await ctx.respond(content=f"{name} built a {ctx.options.building}.")
        if bought_card is not None:
            await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=f"You recieved a {bought_card} development card.")
    except controller.Resource:
        await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=hikari.Embed(
                title="Error!",
                description=f"You do not have the necessary resources to build a {ctx.options.building}.",
                color=hikari.Color(0xFF0000)))
    except Exception as e:
        print(traceback.print_exc())
        await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=hikari.Embed(
                title="Error!",
                description=f"Failed to build {ctx.options.building} with exception: {e}.",
                color=hikari.Color(0xFF0000)))
    

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)