import lightbulb
import hikari
import string
import asyncio

import src.hikari_bot.bot as bot
import src.controller as controller

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Start", description="Start the game.")

# Creates a command in the plugin
@plugin.command
@lightbulb.option("drawing_mode", description="The mode the board will be drawn in.", required=True, choices=["normal", "minecraft"])
@lightbulb.command("start", description="Start the game.")
@lightbulb.implements(lightbulb.SlashCommand)
async def start(ctx: lightbulb.Context) -> None:
    """Start the game.

    Called via the discord command '/start <drawing mode> '.
    """

    ctrl = bot.ctrl

    # Verify the game has not started yet
    if bot.started:
        await ctx.respond(content=f"Cannot use /start. The game has already started.")
        return

    # TODO: TEMP TESTING
    for p in ctrl.players:
            p.modCurrResource("wood", 1)
            p.modCurrResource("brick", 1)
            p.modCurrResource("wheat", 1)
            p.modCurrResource("sheep", 1)
            p.modCurrResource("rock", 1)
            p.unusedDevelopmentCards["KnightCard"] += 1
            p.unusedDevelopmentCards["VictoryPointCard"] += 1
            p.unusedDevelopmentCards["Monopoly"] += 1
            p.unusedDevelopmentCards["YearOfPlenty"] += 1
            p.unusedDevelopmentCards["RoadBuilding"] += 1

    await ctx.respond(content=f"Game starting.")
    bot.started = True
    asyncio.create_task(controller.run(ctrl, asyncio.Event(), ctx.options.drawing_mode))


# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)