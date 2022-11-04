import lightbulb
import hikari

import controller
from hikari_bot import bot

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Accept", description="Accept a trade.")

# Creates a command in the plugin
@plugin.command
@lightbulb.option("trade_num", description="# of the trade to accept.", type=int)
@lightbulb.command("accept", description="Accept a trade.", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def accept(ctx: lightbulb.Context) -> None:
    """Accept a trade.

    Called via the discord command '/accept <trade number>.
    The player whose turn it is can accept any trade OR any player can accept a trade from the player whose turn it is.
    """

    # Invalid trade offer to accept
    if ctx.options.trade_num > len(bot.game.active_trades):
        await ctx.respond(content=hikari.Embed(
                title="Error!",
                description=f"Trade Offer #: {ctx.options.trade_num} is invalid!",
                color=hikari.Color(0xFF0000)))

        return

    name = str(ctx.author).split("#")[0]
    print(bot.game.players)
    print(bot.game.active_trades)

    active_trades = bot.game.active_trades

    try:
        controller.trade(bot.game, bot.game.get_player(active_trades[ctx.options.trade_num - 1]["name"]), bot.game.get_player(name), active_trades[ctx.options.trade_num - 1]["p1_out"], active_trades[ctx.options.trade_num - 1]["p2_in"])
    except controller.Resource:
        await ctx.respond(content=hikari.Embed(
                title="Error!",
                description=f"A player does not have the necessary resources to complete the trade.",
                color=hikari.Color(0xFF0000)))
    except:
        raise Exception("Failed to do the trade.")
    

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)