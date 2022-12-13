import lightbulb
import hikari

import src.hikari_bot.bot as bot

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Discard", description="Discard resource cards.")

# Creates a command in the plugin
@plugin.command
@lightbulb.option("brick", description="Brick cards to discard", default=0, type=int)
@lightbulb.option("wood", description="Wood cards to discard", default=0, type=int)
@lightbulb.option("rock", description="Rock cards to discard", default=0, type=int)
@lightbulb.option("wheat", description="Wheat cards to discard", default=0, type=int)
@lightbulb.option("sheep", description="Sheep cards to discard", default=0, type=int)
@lightbulb.command("discard", description="Discard resource cards.", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def discard(ctx: lightbulb.Context) -> None:
    name = str(ctx.author).split("#")[0]

    cards_to_dict = {
        "brick": int(ctx.options.brick),
        "wood": int(ctx.options.wood),
        "rock": int(ctx.options.rock),
        "wheat": int(ctx.options.wheat),
        "sheep": int(ctx.options.sheep)
    }
    total = sum(cards_to_dict.values())
    
    # must be in the discard phase to use /discard
    if bot.ctrl.cur_phase != 3:
        await ctx.respond(flags=hikari.MessageFlag.EPHEMERAL, content=hikari.Embed(
                title="Error!",
                description=f"You cannot discard cards right now.",
                color=hikari.Color(0xFF0000)))
        return

    # prevent player from discarding incorrect # of cards
    if total != bot.ctrl.get_player_by_name(name).cardsToDiscard:
        await ctx.respond(content=hikari.Embed(
                title="Error!",
                description=f"You need to discard {bot.ctrl.get_player_by_name(name).cardsToDiscard} cards.",
                color=hikari.Color(0xFF0000)))

        return

    # prevent discarding negative cards and cards you don't have
    for card, val in cards_to_dict.items():
        if val < 0:
            await ctx.respond(content=hikari.Embed(
                title="Error!",
                description=f"You cannot discard negative cards.",
                color=hikari.Color(0xFF0000)))

            return

        if bot.ctrl.get_player_by_name(name).currentResources[card] < val:
            await ctx.respond(content=hikari.Embed(
                title="Error!",
                description=f"You do not have {val} {card} cards to discard.",
                color=hikari.Color(0xFF0000)))

            return

    for card, val in cards_to_dict.items():
        bot.ctrl.resource_bank[card] += val
        bot.ctrl.get_player_by_name(name).currentResources[card] -= val

    bot.ctrl.get_player_by_name(name).cardsToDiscard = 0

    await ctx.respond(content=f"Successfully discarded {total} cards.")

    all_discarded = True
    for player in bot.ctrl.players:
        if player.cardsToDiscard > 0:
            all_discarded = False
            break

    if all_discarded:
        bot.ctrl.flag.set()

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)