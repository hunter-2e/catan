import lightbulb
import hikari
import miru

from src.hikari_bot.bot import bot

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
    ctrl = bot.ctrl

    if ctx.options.development_card == "Knight":
        print("knight card used")
    elif ctx.options.development_card == "Year of Plenty":
            print("YEP used")
    elif ctx.options.development_card == "Monopoly":
            print("monop card used")
    else:
        print("Road Builder used")

    #view = MyView(timeout=60)  # Create a new view
    #message = await ctx.respond("Rock Paper Scissors!", components=view.build())
    #await view.start(message)  # Start listening for interactions
    #await view.wait() # Wait until the view times out or gets stopped
    #await ctx.respond("Thank you for playing!")

    modal = KnightModal(title="Example Title")

    await modal.send(ctx.interaction )

    await bot.bot.rest.create_message(ctx.channel_id, content=hikari.Embed(
                title=f"{name} has used the {ctx.options.development_card} Card!",
                color=hikari.Color(0xFFFF00)))
    
    await ctx.respond(content="Use successful")

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

class KnightModal(miru.Modal):
    location = miru.TextInput(label="Name", placeholder="Type your name!", required=True)
    bio = miru.TextInput(label="Biography", value="Pre-filled content!", style=hikari.TextInputStyle.PARAGRAPH)

    # The callback function is called after the user hits 'Submit'
    async def callback(self, ctx: miru.ModalContext) -> None:
        # You can also access the values using ctx.values, Modal.values, or use ctx.get_value_by_id()
        await ctx.respond(f"Your name: `{self.name.value}`\nYour bio: ```{self.bio.value}```")