import lightbulb
import hikari

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Trade", description="Offer a trade.")

# Creates a command in the plugin
@plugin.command
@lightbulb.option("brick_out", description="# Brick to give.")
@lightbulb.option("lumber_out", description="# Lumber to give.")
@lightbulb.option("ore_out", description="# Ore to give.")
@lightbulb.option("grain_out", description="# Grain to give.")
@lightbulb.option("wool_out", description="# Wool to give.")
@lightbulb.option("brick_in", description="# Brick to get.")
@lightbulb.option("lumber_in", description="# Lumber to get.")
@lightbulb.option("ore_in", description="# Ore to get.")
@lightbulb.option("grain_in", description="# Grain to get.")
@lightbulb.option("wool_in", description="# Wool to get.")
@lightbulb.command("trade", description="Offer a trade.", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def trade(ctx: lightbulb.Context) -> None:
    """Offer a trade.

    Called via the discord command '/trade <building> <location>'.
    Anyone can offer a trade regardless of whether or not it is their turn.
    """

    print("CRN: " + ctx.options)

    

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)