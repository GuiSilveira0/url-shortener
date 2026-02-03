import random
import string

class ShortenerUsecase:
    def __init__(
            self, 
        ):
        None

    def generate_short_code(self, length: int = 6) -> str:
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))