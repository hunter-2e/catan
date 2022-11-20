import lightbulb
import hikari

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

    ctrl = bot.ctrl
    name = str(ctx.author).split("#")[0]
    player = ctrl.get_player(name)

    response = hikari.Embed(
        title="Hand:",
        description=f"{player.currentResources}\n{player.unusedDevelopmentCards}",
        color=hikari.Color(0x0000FF))
    response.set_image("images/buildCosts")

    await ctx.respond(content=hikari.Embed(
                title="Hand:",
                description=f"{player.currentResources}\n{player.unusedDevelopmentCards}",
                color=hikari.Color(0x0000FF)))

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)