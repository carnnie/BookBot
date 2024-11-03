import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config.config import Config, load_config
from handlers.user_handlers import user_router
from handlers.other_handlers import other_router
from keyboards.set_menu import set_main_menu

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
        level=logging.INFO,
    )
    logger.info("Starting bot")

    config: Config = load_config()

    bot = Bot(token=config.tgBot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(user_router)
    dp.include_router(other_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
