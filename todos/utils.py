import random
import string

chars = string.ascii_letters + string.digits


def unique_code_generator(size=5):
    unique_code = "".join(random.choice(chars) for _ in range(size))
    return unique_code
