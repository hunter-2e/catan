import lightbulb
import hikari
import string

from src.hikari_bot.bot import bot
import src.controller as controller

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Rob", description="Move the robber and steal from someone.")

# Creates a command in the plugin
@plugin.command
@lightbulb.option("location", description="The location to move the robber.", required=True)
@lightbulb.option("player", description="The player to steal from.", required=True)
@lightbulb.command("rob", description="Move the robber and steal from someone.", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def rob(ctx: lightbulb.Context) -> None:
    """Move the robber and steal from someone.

    Called via the discord command '/rob <location> <player>'.
    """

    name = str(ctx.author).split("#")[0]
    location = (list(string.ascii_uppercase).index(ctx.options.location[0].upper()), float(ctx.options.location[1:]))
    ctrl = bot.ctrl
    resource_stolen = None

    # Verify the player moving the robber is the current player
    if ctrl.players[ctrl.current_player].name != name:
        await ctx.respond(content=hikari.Embed(
                title="Error!",
                description=f"You cannot rob on someone elses turn.",
                color=hikari.Color(0xFF0000)))

        return

    # Verify the player rolled a 7
    if ctrl.cur_dice != 7:
        await ctx.respond(content=hikari.Embed(
                title="Error!",
                description=f"You cannot rob unless you rolled a 7.",
                color=hikari.Color(0xFF0000)))

        return

    # Verify the robber has not been moved yet this turn
    if ctrl.has_robber_moved:
        await ctx.respond(content=hikari.Embed(
                title="Error!",
                description=f"You can only move the robber once per turn.",
                color=hikari.Color(0xFF0000)))

        return

    try:
        resource_stolen = ctrl.move_robber(location, ctx.options.player)
    except Exception as e:
        await ctx.respond(content=hikari.Embed(
                title="Error!",
                description=e,
                color=hikari.Color(0xFF0000)))

        return

    await ctx.respond(content=f"Successfully stole {resource_stolen} from {ctx.options.player}.")
    await bot.bot.rest.create_message(ctx.channel_id, content=f"{name} moved the robber to {location} and stole from {ctx.options.player}.")

    bot.ctrl.flag.set()



# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)