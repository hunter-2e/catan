import lightbulb
import asyncio

from hikari_bot import bot
import controller

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

    await ctx.respond(content=f"{name} has ended their turn.")
    
    bot.ctrl.flag.set()



# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)