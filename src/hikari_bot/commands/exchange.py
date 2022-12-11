import lightbulb
import hikari

import src.hikari_bot.bot as bot

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Exchange", description="Exchange resource cards.")

# Creates a command in the plugin
@plugin.command
@lightbulb.option("want", description="card wanted", choices=["Brick", "Wood", "Rock", "Wheat", "Sheep"], type=str)
@lightbulb.option("give", description="cards to give", choices=["Brick", "Wood", "Rock", "Wheat", "Sheep"], type=str)
@lightbulb.option("exchange_type", description="exchange_type", choices=["2for1", "3for1", "4for1"], type=str)
@lightbulb.command("exchange", description="Exchange resource cards.")
@lightbulb.implements(lightbulb.SlashCommand)
async def exchange(ctx: lightbulb.Context) -> None:
    """Exchange resource cards."""

    name = str(ctx.author).split("#")[0]
    ctrl = bot.ctrl
    player_obj = ctrl.get_player(name)
    hasAccess = None

    port_types = ["2for1", "3for1", "4for1"]
    amount_to_trade = port_types.index(ctx.options.exchange_type) + 2

    if ctx.options.exchange_type == "2for1":
        hasAccess = ctrl.board.postAccess(player_obj, ctx.options.give)
    else:
        hasAccess = ctrl.board.postAccess(player_obj, ctx.options.exchange_type)

    if not hasAccess:
        await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=hikari.Embed(
                title="Error!",
                description=f"You do not have access to this port: {ctx.options.exchange_type}",
                color=hikari.Color(0xFF0000)))
        return

    if player_obj.currentResources[ctx.options.give.lower()] >= amount_to_trade and ctrl.resource_bank[ctx.options.want.lower()] >= 1:
        player_obj.currentResources[ctx.options.give.lower()] -= amount_to_trade
        ctrl.resource_bank[ctx.options.give.lower()] += amount_to_trade

        player_obj.currentResources[ctx.options.want.lower()] += 1
        ctrl.resource_bank[ctx.options.want.lower()] -= 1
    else:
        await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=hikari.Embed(
            title="Error!",
            description=f"You or the bank do not have the necessary resources to use this port.",
            color=hikari.Color(0xFF0000)))
        return

    await ctx.respond(content=f"Player {name} exchanged {amount_to_trade} {ctx.options.give} for 1 {ctx.options.want}")


# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)
