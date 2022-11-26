import lightbulb
import hikari

import src.hikari_bot.bot as bot

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Discard", description="Discard resource cards.")

# Creates a command in the plugin
@plugin.command
@lightbulb.option("cards", description="Resource cards to discard", required=True)
@lightbulb.command("discard", description="Discard resource cards.", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def discard(ctx: lightbulb.Context) -> None:
    name = str(ctx.author).split("#")[0]
    ctrl = bot.ctrl

    cards_to_list = ctx.options.cards.split()
    
    if len(cards_to_list) != ctrl.get_player(name).cardsToDiscard:
        await ctx.respond(content=hikari.Embed(
                title="Error!",
                description=f"You need to discard {ctrl.get_player(name).cardsToDiscard} cards.",
                color=hikari.Color(0xFF0000)))

        return

    for card in cards_to_list:
        if card not in ctrl.resource_bank:
            await ctx.respond(content=hikari.Embed(
                title="Error!",
                description=f"Invalid input: {card}.",
                color=hikari.Color(0xFF0000)))

            return

    for card in cards_to_list:
        ctrl.resource_bank[card] += 1
        ctrl.get_player(name).currentResources[card] -= 1

    ctrl.get_player(name).cardsToDiscard = 0

    await ctx.respond(content=f"Success.")

    all_discarded = True
    for player in ctrl.players:
        if player.cardsToDiscard > 0:
            all_discarded = False
            break

    if all_discarded:
        ctrl.flag.set()

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)