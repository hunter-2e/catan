import lightbulb
import asyncio
import hikari

import src.hikari_bot.bot as bot
import src.controller as controller

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("End Turn", description="End your turn.")

# Creates a command in the plugin
@plugin.command
@lightbulb.command("endturn", description="End your turn")
@lightbulb.implements(lightbulb.SlashCommand)
async def endturn(ctx: lightbulb.Context) -> None:
    """Join the game.

    Called via the discord command '/endturn'.
    """

    name = str(ctx.author).split("#")[0]

    # cannot end someone else's turn
    if bot.ctrl.players[bot.ctrl.current_player].name != name:
        await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=hikari.Embed(
                title="Error!",
                description=f"You cannot end someone elses turn.",
                color=hikari.Color(0xFF0000)))

        return

    # cannot end turn before moving the robber
    if bot.ctrl.cur_dice == 7 and bot.ctrl.has_robber_moved is False:
        await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=hikari.Embed(
                title="Error!",
                description=f"You need to move the robber before ending your turn.",
                color=hikari.Color(0xFF0000)))

        return

    player_obj = bot.ctrl.players[bot.ctrl.current_player]

    # verify player has built the necessary road and settlement in the beginning sequence
    if (bot.ctrl.cur_phase == 0 and len(player_obj.roadsPlaced) == 0) or (bot.ctrl.cur_phase == 1 and len(player_obj.roadsPlaced) == 1):
        await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=hikari.Embed(
                title="Error!",
                description=f"You need to build a road before you end your turn.",
                color=hikari.Color(0xFF0000)))

        return
    if (bot.ctrl.cur_phase == 0 and len(player_obj.settlementSpots) == 0) or (bot.ctrl.cur_phase == 1 and len(player_obj.settlementSpots) == 1):
        await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=hikari.Embed(
                title="Error!",
                description=f"You need to build a settlement before you end your turn.",
                color=hikari.Color(0xFF0000)))

        return

    await ctx.respond(content=f"{name} has ended their turn.")

    bot.ctrl.flag.set()



# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)