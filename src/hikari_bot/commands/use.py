import lightbulb

import src.hikari_bot.bot as bot
import src.hikari_bot.modals as modals

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Use", description="Use a development card.")

# Creates a command in the plugin
@plugin.command
@lightbulb.option("development_card", description="Play a development card.", choices=["Knight", "Year of Plenty", "Monopoly", "Road Builder"], required=True)
@lightbulb.command("use", description="Use a development card.", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def use(ctx: lightbulb.Context) -> None:

    #TODO: Delete use messages from channel at end of each turn??

    name = str(ctx.author).split("#")[0]

    if ctx.options.development_card == "Knight":
        if bot.ctrl.get_player(name).unusedDevelopmentCards["KnightCard"] == 0:
            await ctx.respond(content="Error: You do not have any Knight cards to play.")
            return

        modal = modals.KnightModal(bot.ctrl, title="Use Knight Card")
        await modal.send(ctx.interaction)
        
    elif ctx.options.development_card == "Year of Plenty":
        if bot.ctrl.get_player(name).unusedDevelopmentCards["YearOfPlenty"] == 0:
            await ctx.respond(content="Error: You do not have any Year Of Plenty cards to play.")
            return

        modal = modals.YOPModal(bot.ctrl, title="Use Year Of Plenty Card")
        await modal.send(ctx.interaction)
    elif ctx.options.development_card == "Monopoly":
        if bot.ctrl.get_player(name).unusedDevelopmentCards["Monopoly"] == 0:
            await ctx.respond(content="Error: You do not have any Monopoly cards to play.")
            return

        modal = modals.MonopolyModal(bot.ctrl, title="Use Monopoly Card")
        await modal.send(ctx.interaction)
    else:
        if bot.ctrl.get_player(name).unusedDevelopmentCards["RoadBuilding"] == 0:
            await ctx.respond(content="Error: You do not have any Road Building cards to play.")
            return

        modal = modals.RoadBuildingModal(bot.ctrl, title="Use Road Building Card")
        await modal.send(ctx.interaction)

        

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)