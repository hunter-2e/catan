import lightbulb
import hikari
import src.draw as draw

import src.hikari_bot.bot as bot

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Hand", description="Get your current hand.")

# Creates a command in the plugin
@plugin.command
@lightbulb.command("hand", description="Get yorur current hand", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def hand(ctx: lightbulb.Context) -> None:
    """Get your current hand.

    Called via the discord command '/hand'.
    """

    name = str(ctx.author).split("#")[0]
    player = bot.ctrl.get_player_by_name(name)

    response = hikari.Embed(
        title="Hand:",
        description=f"Victory Points: {player.victoryPoints}\n\nUsed Knights: {player.usedDevelopmentCards['Knight']}\nLargest Army: {player.largestArmy}\nLongest Road: {player.longestRoad}\n",
        color=hikari.Color(0x0000FF))

    draw.drawHand(player)
    response.set_image(hikari.File("images/playerHand.jpg"))

    await ctx.respond(content=response)

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)