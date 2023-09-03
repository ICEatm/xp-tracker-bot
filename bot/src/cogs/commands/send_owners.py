import discord
from discord.ext import commands
from discord import app_commands
from src.util.logger import Logger
from src.helper.config import Config
from src.helper.datetime import DateTime

class SendOwners(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = Config()
        self.logger = Logger()
        self.datetime_helper = DateTime()

    # Send owners bot command  
    @app_commands.command(name="send_owners", description="Sends a message to every guild owner.")
    @app_commands.describe(
        message="The message you want to send to every guild owner.",
    )
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guilds(Config().dev_guild_id)
    async def send_owners_command(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer(ephemeral=True)

        request_msg = await interaction.followup.send(f"{self.config.green_tick_emoji_id} Trying to send broadcast to all users!", ephemeral=True)

        try:
            await self.logger.dm_guild_owners(message)
        except Exception as e:
            await request_msg.edit(content=f"{self.config.red_cross_emoji_id} Error broadcasting to all users! Check the logs for more information.", ephemeral=True)
            self.logger.log("ERROR", f"Error broadcasting to all users! Error: {e}")
            await self.logger.discord_log(f"Error broadcasting to all users! Error: {e}")
            return

        await request_msg.edit(content=f"{self.config.green_tick_emoji_id} Broadcast sent to all users!", ephemeral=True)

    @send_owners_command.error
    async def send_owners_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"{self.config.red_cross_emoji_id} You don't have permissions to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(SendOwners(bot))
    return Logger().log("INFO", "Send owners command loaded!")