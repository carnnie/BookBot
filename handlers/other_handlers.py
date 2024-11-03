from aiogram import Router
from aiogram.types import Message


other_router = Router()

@other_router.message()
async def process_other_answer(message: Message):
    await message.answer(message.text)
