from state.state import STATE


PAGE_SIZE = 1050


def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    last_index = min((start + page_size - 1), (len(text) - 1))

    for i in range(last_index, start, -1):
        if text[i] in ",.!:;?":
            if i < len(text) - 1 and text[i + 1] in ",.!:;?":
                continue

            return text[start : i + 1], len(text[start : i + 1])

    return text[start : last_index + 1], len(text[start : last_index + 1])


def prepare_book(name: str, user: int) -> None:
    with open(f"books/books/{name}.txt", "r", encoding="utf-8") as file:
        text = file.read()
        i = 0
        key = 1
        text_length = len(text)

        while i < text_length:
            part, part_length = _get_part_text(text, i, PAGE_SIZE)
            STATE[user].book[key] = part.lstrip()
            key += 1
            i += part_length

    STATE[user].book_name = name
    STATE[user].book_length = len(STATE[user].book)
    STATE[user].page = 0
    STATE[user].bookmarks = set()
