"""Controls core functionality of the Discord Bot."""

import os
import dotenv
from typing import Union

import hikari
import lightbulb
import miru

import src.controller as controller

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

    bot.load_extensions("src.hikari_bot.commands.build", "src.hikari_bot.commands.trade", "src.hikari_bot.commands.accept", "src.hikari_bot.commands.hand", "src.hikari_bot.commands.join", "src.hikari_bot.commands.endturn", "src.hikari_bot.commands.use", "src.hikari_bot.commands.rob")

    miru.install(bot)
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

    miru.uninstall()

async def send_image_or_message(image: Union[str, None], message: Union[str, hikari.Embed, None]) -> None:
    """Sends the most updated version of the game board to a discord channel OR a message."""

    chnl = None
    try:
        chnl = await get_channel()
    except Exception as e:
        print(e)
        return

    if image is None and message is not None:
        await bot.rest.create_message(channel=chnl, content=message)
    elif image is not None and message is None:
        await bot.rest.create_message(channel=chnl, content=hikari.File(image))
    else:
        print("bot.send_image_or_message(): invalid parameters!")

async def get_channel() -> hikari.GuildChannel:
    """Returns the channel to send messages to."""

    chnl = None

    async for i, guild in bot.rest.fetch_my_guilds().enumerate():
        for j, channel in bot.cache.get_guild(guild.id).get_channels().items():
            if channel.name == "bot-commands":
                chnl = channel

    if chnl is None:
        raise Exception("Failed to find channel.")
    
    return chnl