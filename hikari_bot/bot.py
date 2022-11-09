"""Controls core functionality of the Discord Bot."""

import os
import dotenv

import hikari
import lightbulb

import controller

dotenv.load_dotenv()    # Load environment variables

# Creates a bot instance
bot = lightbulb.BotApp(
    os.environ["DISCORD_BOT_TOKEN"],
    intents=hikari.Intents.ALL,
    default_enabled_guilds=(833429143672717315),     # commenting this out makes slash commands available in DMs, uncommenting this is useful for testing since it instantly loads slash commands to the listed servers
    help_class=None,
    logs="INFO"    #DEBUG
)

def setup() -> None:
    """Startup the bot."""

    bot.load_extensions("hikari_bot.commands.build", "hikari_bot.commands.trade", "hikari_bot.commands.accept", "hikari_bot.commands.hand")
    bot.run(activity=hikari.Activity(name="Catan", type=hikari.ActivityType.PLAYING))

async def shutdown() -> None:
    """Shutdown the bot."""

    await bot.close()

@bot.listen()
async def bot_connected(event: hikari.StartedEvent) -> None:
    """Called once the bot has started."""

    global ctrl
    ctrl = controller.setup()
    global started
    started = False
    #asyncio.create_task(controller.run(ctrl))

@bot.listen()
async def bot_disconnected(event: hikari.StoppedEvent) -> None:
    """Called once the bot has disconnected from Discord."""

    print("The bot has disconnected from Discord!")

async def send_image(image: str):
    """Sends the most updated version of the game board to a discord channel."""

    chnl = None

    async for i, guild in bot.rest.fetch_my_guilds().enumerate():
        for j, channel in bot.cache.get_guild(guild.id).get_channels().items():
            if channel.name == "bot-commands":
                chnl = channel

    if chnl is None:
        print("Failed to send image!")
        return

    await bot.rest.create_message(channel=chnl, content=hikari.File(image))