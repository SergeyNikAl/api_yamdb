import re
from datetime import datetime as dt

from django.core.validators import ValidationError

INVALID_USERNAME = ('Недопустимое имя пользователя: "{username}". '
                    'Придумайте другое.')
USERNAME_SYMBOLS = re.compile(r'[\w.@+-@./+-]+')
INVALID_USERNAME_SYMBOLS = ('Недопустимые символы: {wrong_symbols}. '
                            'Придумайте другое username.')
YEAR_OVER_CURRENT = 'Год не может быть больше текущего.'


class UsernameValidation:
    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(INVALID_USERNAME.format(username=value))
        if not re.match(USERNAME_SYMBOLS, value):
            raise ValidationError(
                INVALID_USERNAME_SYMBOLS.format(
                    [
                        symbol for symbol in value if symbol not in
                        USERNAME_SYMBOLS
                    ]
                )
            )
        return value


def get_now_year():
    return dt.now().year
