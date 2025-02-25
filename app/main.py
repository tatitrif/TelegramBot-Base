import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import common
from core.config import settings

logger = logging.getLogger(__name__)


async def create_bot(token: str) -> Bot:
    """Create and validate bot instance."""
    session = AiohttpSession()
    default = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=token, session=session, default=default)

    try:
        # Test bot token by getting bot info
        bot_info = await bot.get_me()
        logger.info(f"Successfully initialized bot: {bot_info.full_name}")
        return bot
    except TelegramAPIError as err:
        await session.close()
        error_msg = f"Failed to initialize bot: {str(err)}"
        logger.error(error_msg)
        raise ValueError(error_msg)


async def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    bot = None
    try:
        bot = await create_bot(settings.telegram.bot_token.get_secret_value())
        dp = Dispatcher(storage=MemoryStorage())

        dp.include_router(common.router)

        logger.info("Remove webhook integration")
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Start polling")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    except Exception as err:
        logger.error(f"Startup error: {str(err)}")
        raise
    finally:
        if bot is not None:
            await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
