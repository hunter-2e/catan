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

    ctrl = bot.ctrl

    active_trades = ctrl.active_trades
    player1_name = ctrl.get_player(active_trades[ctx.options.trade_num - 1]["name"])
    player2_name = str(ctx.author).split("#")[0]

    # Cannot accept your own trade
    if player1_name == player2_name:
        await ctx.respond(content=hikari.Embed(
                title="Error!",
                description=f"You cannot accept your own trade.",
                color=hikari.Color(0xFF0000)))

        return

    # Player whose turn it is must be one of the player's involved in the trade
    if player1_name != ctrl.current_player and player2_name != ctrl.current_player:
        await ctx.respond(content=hikari.Embed(
                title="Error!",
                description=f"Player {ctrl.current_player} must be involved in the trade.",
                color=hikari.Color(0xFF0000)))

        return

    # Invalid trade offer to accept
    if ctx.options.trade_num > len(ctrl.active_trades):
        await ctx.respond(content=hikari.Embed(
                title="Error!",
                description=f"Trade Offer #: {ctx.options.trade_num} is invalid.",
                color=hikari.Color(0xFF0000)))

        return

    try:
        ctrl.trade(ctx.options.trade_num, player2_name)

        await bot.bot.rest.create_message(ctx.channel_id, content=f"Trade # {ctx.options.trade_num} from {player1_name} accepted by {player2_name}.")
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