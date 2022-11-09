import lightbulb
import asyncio

from hikari_bot import bot
import controller

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Join", description="Join the game.")

# Creates a command in the plugin
@plugin.command
@lightbulb.option("color", description="Color.", choices=["Blue", "White", "Orange", "Red"], required=True)
@lightbulb.command("join", description="Join the game")
@lightbulb.implements(lightbulb.SlashCommand)
async def join(ctx: lightbulb.Context) -> None:
    """Join the game.

    Called via the discord command '/join <color>'.
    """

    ctrl = bot.ctrl
    name = str(ctx.author).split("#")[0]

    # Start the game
    if len(ctrl.players) < 4:
        # If game has not been started yet
        ctrl.add_player(name, ctx.options.color)

        #await bot.bot.rest.create_message(ctx.channel_id, content=f"{name} has joined the game as {ctx.options.color}.")

        await ctx.respond(content=f"{name} has joined the game as {ctx.options.color}.")
    
    if len(ctrl.players) == 4 and not bot.started:
        #await bot.bot.rest.create_message(ctx.channel_id, content=f"Game starting.")

        for p in ctrl.players:
            p.modCurrResource("wood", 1)
            p.modCurrResource("brick", 1)
            p.modCurrResource("wheat", 1)
            p.modCurrResource("sheep", 1)

        await ctx.respond(content=f"Game starting.")
        asyncio.create_task(controller.run(ctrl, asyncio.Event()))



# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)