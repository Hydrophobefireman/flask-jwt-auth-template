from secrets import token_urlsafe


def gen_id():
    return token_urlsafe(8)
