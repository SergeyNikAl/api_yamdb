import re
from datetime import datetime as dt

from django.core.validators import ValidationError

INVALID_USERNAME = 'Недопустимое имя пользователя: "{value}".'
USERNAME_SYMBOLS = re.compile(r'[\w.@+-@./+-]+')
INVALID_USERNAME_SYMBOLS = 'Недопустимые символы: {value}'
YEAR_OVER_CURRENT = 'Год не может быть больше текущего.'


class UsernameValidation:
    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(INVALID_USERNAME.format(value=value))
        if not re.match(USERNAME_SYMBOLS, value):
            raise ValidationError(
                INVALID_USERNAME_SYMBOLS.format(
                    value=[
                        symbol for symbol in value if symbol not in ''.join(
                            re.findall(USERNAME_SYMBOLS, value)
                        )
                    ]
                )
            )
        return value


def get_now_year():
    return dt.now().year
