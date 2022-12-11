import lightbulb
import hikari

import src.hikari_bot.bot as bot

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Join", description="Join the game.")

# Creates a command in the plugin
@plugin.command
@lightbulb.option("color", description="Color.", choices=["Blue", "White", "Orange", "Red", "Purple"], required=True)
@lightbulb.command("join", description="Join the game")
@lightbulb.implements(lightbulb.SlashCommand)
async def join(ctx: lightbulb.Context) -> None:
    """Join the game.

    Called via the discord command '/join <color>'.
    """

    name = str(ctx.author).split("#")[0]

    # Verify the game has not started yet
    if bot.started:
        await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=f"Cannot use /join. The game has already started.")
        return

    for player in bot.ctrl.players:
        # Verify the player has not already joined
        if player.name == name:
            await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=hikari.Embed(
                title="Error!",
                description=f"You have already joined the game.",
                color=hikari.Color(0xFF0000)))
            return

        # Verify the color has not already been used
        if player.color == ctx.options.color:
            await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=hikari.Embed(
                title="Error!",
                description=f"{ctx.options.color} has already been used.",
                color=hikari.Color(0xFF0000)))
            return

    if len(bot.ctrl.players) < 4:
        bot.ctrl.add_player(name, ctx.options.color)
        await ctx.respond(content=f"{name} has joined the game as {ctx.options.color}.")
    elif len(bot.ctrl.players) == 4:
        await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=f"Cannot use /join. There are already 4 players.")


# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)