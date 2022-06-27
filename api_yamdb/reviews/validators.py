import re
from datetime import datetime as dt
from django.core.validators import ValidationError

INVALID_USERNAME = ('Недопустимое имя пользователя: "{username}". '
                    'Придумайте другое.')
USERNAME_SYMBOLS = re.compile(r'[\w.@+-@./+-]+')
INVALID_USERNAME_SYMBOLS = 'Недопустимые символы. Придумайте другое username. '


class UsernameValidation:
    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(INVALID_USERNAME.format(username=value))
        if not re.match(USERNAME_SYMBOLS, value):
            raise ValidationError(INVALID_USERNAME_SYMBOLS)
        return value


def get_now_year():
    return dt.now().year
