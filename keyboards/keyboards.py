from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_BUTTONS_RU


def create_inline_kb(width: int, *args: str, last_row: list[str] | None = None, **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = []

    if args:
        for callback_data in args:
            buttons.append(
                InlineKeyboardButton(
                    text=LEXICON_BUTTONS_RU.get(callback_data, callback_data),
                    callback_data=callback_data,
                )
            )

    for callback_data, text in kwargs.items():
        buttons.append(InlineKeyboardButton(text=text, callback_data=callback_data))

    kb_builder.row(*buttons, width=width)

    if last_row:
        last_row_buttons = [
            InlineKeyboardButton(text=LEXICON_BUTTONS_RU[callback_data], callback_data=callback_data)
            for callback_data in last_row
        ]

        kb_builder.row(*last_row_buttons, width=len(last_row_buttons))

    return kb_builder.as_markup()
