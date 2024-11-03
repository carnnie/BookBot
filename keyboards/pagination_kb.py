from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_BUTTONS_RU


def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        *[
            InlineKeyboardButton(text=LEXICON_BUTTONS_RU.get(button, button), callback_data=button)
            for button in buttons
        ]
    )
    
    return kb_builder.as_markup()
