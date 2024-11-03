import logging
from mailbox import Message
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery

from books.books_info import BOOK_NAMES
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData, IsPageNumCallbackData
from keyboards.bookmarks_kb import create_bookmarks_keyboard, create_edit_keyboard
from keyboards.keyboards import create_inline_kb
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon_ru import ALERTS, LEXICON_RU
from services.file_handling import prepare_book
from services.utilities import get_page
from state.state import STATE, UserState

logger = logging.getLogger(__name__)
user_router = Router()


@user_router.message(CommandStart())
async def process_start_command(message: Message):
    STATE[message.chat.id] = UserState(book={}, book_name="", book_length=0, page=0, bookmarks=set())
    prepare_book(name="martian_chronicles", user=message.chat.id)
    await message.answer(LEXICON_RU["/start"])


@user_router.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer(LEXICON_RU["/help"])


# choose book handlers


@user_router.message(Command(commands=["choose"]))
async def process_choose_command(message: Message):
    keyboard = create_inline_kb(width=1, **BOOK_NAMES)
    await message.answer(LEXICON_RU["/choose"], reply_markup=keyboard)


@user_router.callback_query(F.data.in_(BOOK_NAMES.keys()))
async def book_choose_button_pressed(callback: CallbackQuery):
    user = callback.message.chat.id
    if user not in STATE:
        STATE[user] = UserState(book={}, book_name="", book_length=0, page=0, bookmarks=set())

    try:
        prepare_book(name=callback.data, user=user)
        await callback.message.edit_text(text=LEXICON_RU["book_chosen"].format(BOOK_NAMES[callback.data]))
    except (KeyError, FileNotFoundError):
        logger.error(f"Книга с названием {callback.data} не найдена в базе.")
        await callback.answer(text=ALERTS["no_book"], show_alert=True)


# main handlers


@user_router.message(Command(commands=["beginning"]))
async def process_beginning_command(message: Message):
    user = message.chat.id
    if user not in STATE:
        STATE[user] = UserState(book={}, book_name="", book_length=0, page=0, bookmarks=set())

    STATE[user].page = 1

    text = get_page(user)
    keyboard = create_pagination_keyboard(
        "previous", f"{STATE[user].page}/{STATE[user].book_length}", "next"
    )

    await message.answer(text=text, reply_markup=keyboard)


@user_router.message(Command(commands=["continue"]))
async def process_command_continue(message: Message):
    user = message.chat.id
    if user not in STATE:
        STATE[user] = UserState(book={}, book_name="", book_length=0, page=0, bookmarks=set())

    text = get_page(user)
    keyboard = create_pagination_keyboard(
        "previous", f"{STATE[user].page}/{STATE[user].book_length}", "next"
    )

    await message.answer(text=text, reply_markup=keyboard)


@user_router.callback_query(F.data == "next")
async def process_next_page(callback: CallbackQuery):
    user = callback.message.chat.id

    if STATE[user].page < STATE[user].book_length:
        STATE[user].page += 1

        text = get_page(user)
        keyboard = create_pagination_keyboard(
            "previous", f"{STATE[user].page}/{STATE[user].book_length}", "next"
        )

        await callback.message.edit_text(text=text, reply_markup=keyboard)
    else:
        await callback.answer("Вы на последней странице")


@user_router.callback_query(F.data == "previous")
async def process_previous_page(callback: CallbackQuery):
    user = callback.message.chat.id

    if STATE[user].page > 0:
        STATE[user].page -= 1

        text = get_page(user)
        keyboard = create_pagination_keyboard(
            "previous", f"{STATE[user].page}/{STATE[user].book_length}", "next"
        )

        await callback.message.edit_text(text=text, reply_markup=keyboard)
    else:
        await callback.answer("Вы на первой странице")


# bookmarks handlers


@user_router.callback_query(IsPageNumCallbackData())
async def process_add_to_bookmarks(callback: CallbackQuery):
    user = callback.message.chat.id

    STATE[user].bookmarks.add(STATE[user].page)

    await callback.answer(text=ALERTS["add_to_bookmarks"])


@user_router.message(Command(commands=["bookmarks"]))
async def process_bookmarks_command(message: Message):
    user = message.chat.id
    if user not in STATE:
        STATE[user] = UserState(book={}, book_name="", book_length=0, page=0, bookmarks=set())

    pages = sorted(STATE[user].bookmarks)
    if pages:
        keyboard = create_bookmarks_keyboard(user)
        await message.answer(text=LEXICON_RU["/bookmarks"], reply_markup=keyboard)
    else:
        await message.answer(text=LEXICON_RU["no_bookmarks"])


@user_router.callback_query(IsDigitCallbackData())
async def process_bookmark_select(callback: CallbackQuery):
    user = callback.message.chat.id

    STATE[user].page = int(callback.data)

    text = get_page(user)
    keyboard = create_pagination_keyboard(
        "previous", f"{STATE[user].page}/{STATE[user].book_length}", "next"
    )

    await callback.message.answer(text=text, reply_markup=keyboard)


@user_router.callback_query(F.data == "edit_bm")
async def process_edit_bookmark(callback: CallbackQuery):
    user = callback.message.chat.id

    pages = sorted(STATE[user].bookmarks)
    keyboard = create_edit_keyboard(user)

    await callback.message.edit_text(text=LEXICON_RU["edit_bm"], reply_markup=keyboard)


@user_router.callback_query(IsDelBookmarkCallbackData())
async def process_delete_bookmark(callback: CallbackQuery):
    user = callback.message.chat.id

    bookmark = int(callback.data.split("_")[-1])
    STATE[user].bookmarks.remove(bookmark)

    pages = sorted(STATE[user].bookmarks)
    if pages:
        keyboard = create_edit_keyboard(user)

        await callback.message.edit_text(text=LEXICON_RU["edit_bm"], reply_markup=keyboard)
    else:
        await callback.message.edit_text(text=LEXICON_RU["no_bookmarks"])


@user_router.callback_query(F.data == "quit_bm")
async def process_quit_bookmarks(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU["quit_bm"])
