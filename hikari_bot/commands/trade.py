import lightbulb
import hikari

from hikari_bot import bot

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Trade", description="Offer a trade.")

# Creates a command in the plugin
@plugin.command
@lightbulb.option("brick_out", description="# Brick to give.", type=int, default=0, min_value=0)
@lightbulb.option("wood_out", description="# Wood to give.", type=int, default=0, min_value=0)
@lightbulb.option("rock_out", description="# Rock to give.", type=int, default=0, min_value=0)
@lightbulb.option("grain_out", description="# Grain to give.", type=int, default=0, min_value=0)
@lightbulb.option("wool_out", description="# Sheep to give.", type=int, default=0, min_value=0)
@lightbulb.option("brick_in", description="# Brick to get.", type=int, default=0, min_value=0)
@lightbulb.option("sheep_in", description="# Wood to get.", type=int, default=0, min_value=0)
@lightbulb.option("rock_in", description="# Rock to get.", type=int, default=0, min_value=0)
@lightbulb.option("grain_in", description="# Grain to get.", type=int, default=0, min_value=0)
@lightbulb.option("sheep_in", description="# Sheep to get.", type=int, default=0, min_value=0)
@lightbulb.command("trade", description="Offer a trade.", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def trade(ctx: lightbulb.Context) -> None:
    """Offer a trade.

    Called via the discord command '/trade <type of material number for both giving and recieving...>'.
    Anyone can offer a trade regardless of whether or not it is their turn.
    """

    #TODO: Delete trade messages from channel at end of each turn??

    name = str(ctx.author).split("#")[0]
    ctrl = bot.ctrl

    player1_resources = {}
    player2_resources = {}

    # split resources where out = giving, in = recieving
    for key, value in ctx.options._options.items():
        if "out" in key:
            player1_resources[key.split("_")[0]] = value 
        if "in" in key:
            player2_resources[key.split("_")[0]] = value 

    ctrl.active_trades.append({
        "name": name, 
        "p1_out": player1_resources, 
        "p2_in": player2_resources
    })

    await bot.bot.rest.create_message(ctx.channel_id, content=hikari.Embed(
                title=f"Trade #{len(ctrl.active_trades)}!",
                description=f"{name} wants to give: {player1_resources} for {player2_resources}",
                color=hikari.Color(0xFFFF00)))
    
    await ctx.respond(content="Trade offer successfully created!")

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)
