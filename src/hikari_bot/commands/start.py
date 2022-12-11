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
        await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=hikari.Embed(
                title="Error!",
                description=f"Cannot use /start. The game has already started.",
                color=hikari.Color(0xFF0000)))
        return

    await ctx.respond(content=f"Game starting.")
    bot.started = True
    asyncio.create_task(controller.run(ctrl, asyncio.Event(), ctx.options.drawing_mode))


# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)