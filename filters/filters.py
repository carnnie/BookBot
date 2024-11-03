from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsDigitCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()


class IsPageNumCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return "/" in callback.data and callback.data.replace("/", "").isdigit()


class IsDelBookmarkCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith("del") and callback.data[4:].isdigit()
