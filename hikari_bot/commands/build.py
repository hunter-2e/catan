import lightbulb
import hikari

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Build", description="Build something.")

# Creates a command in the plugin
@plugin.command
@lightbulb.option("building", description="The building to create.")
@lightbulb.option("location", description="The location of the building.")
@lightbulb.command("build", description="Build something", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def build(ctx: lightbulb.Context) -> None:
    """Build something.

    Called via the discord command '/build <building> <location>'.
    """

    print("CRN: " + ctx.options.crn)
    print("subject: " + ctx.options.subject)
    print("sendername: " + str(ctx.author))

    

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)