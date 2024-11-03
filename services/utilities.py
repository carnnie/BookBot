from state.state import STATE


def get_page(user: int) -> str:
    page_num = STATE[user].page
    return STATE[user].book[page_num]
