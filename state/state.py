# имитация бд
from dataclasses import dataclass


@dataclass
class UserState:
    book: dict[int, str]
    book_name: str
    book_length: int
    page: int
    bookmarks: set[int]


STATE: dict[int, UserState] = {
    958064532: UserState(book={}, book_name="", book_length=0, page=0, bookmarks=set())
}
