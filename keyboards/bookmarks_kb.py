from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_BUTTONS_RU
from state.state import STATE


def create_bookmarks_keyboard(user: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    for page in sorted(STATE[user].bookmarks):
        kb_builder.row(
            InlineKeyboardButton(text=f"{page} - {STATE[user].book[page][:100]}", callback_data=str(page))
        )

    kb_builder.row(
        InlineKeyboardButton(text=LEXICON_BUTTONS_RU["edit_bm"], callback_data="edit_bm"),
        InlineKeyboardButton(text=LEXICON_BUTTONS_RU["quit_bm"], callback_data="quit_bm"),
        width=2,
    )

    return kb_builder.as_markup()


def create_edit_keyboard(user: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    for page in sorted(STATE[user].bookmarks):
        kb_builder.row(
            InlineKeyboardButton(
                text=f"❌ {page} - {STATE[user].book[page][:100]}", callback_data=f"del_{page}"
            )
        )

    kb_builder.row(InlineKeyboardButton(text=LEXICON_BUTTONS_RU["quit_bm"], callback_data="quit_bm"))

    return kb_builder.as_markup()
