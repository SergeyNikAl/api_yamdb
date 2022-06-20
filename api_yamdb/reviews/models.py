from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = [
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin'),
]
TEXT_SCOPE = 15  # потом перенесу в setiings


class User(AbstractUser):
    """
    Берем не от модели Model, а наследуем от абстрактной модели пользователя AbstractUser и
    переопределяем ее, так как есть опциональный метод валидации по username.
    Везде обязательно пишем verbose_name, чтобы было представление, что поле значит.
    """
    username_validator = RegexValidator(
        "Для определния доступных символов при выборе"
        r'^[\w.@+-]+'
    )
    username = models.CharField(
        max_length=,
        unique=True,
        validators=[username_validator]
    )
    email =
    first_name =
    last_name =
    role = ('Для определения статуса пользователя')
    # role = models.CharField(
    #  'Роль',
    # max_length = max([len(x[0]) for x in ROLES]),
    # default = USER,
    # choices = ROLES
    # )
    password =

    REQUIRED_FIELDS = ['email']

    # Роли можно определить с помощью декоратора @ property
    # 'is_admin' и 'is_moderator_or_admin'
    # Например:

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff

    def ..

    .

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'  # данное значение я сгенерирую в setiings


class Category(models.Model):
    """
    Схоже с моделями группы в Posts
    """
    name =
    slug =

    class Meta:
        ordering =
        verbose_name =
        verbose_name_plural =

    def __str__(self):
        return self.name[:TEXT_SCOPE]


class Genre(models.Model):
    """
    Схоже с моделями группы в Posts
    """
    name =
    slug =

    class Meta:
        ordering =
        verbose_name =
        verbose_name_plural =

    def __str__(self):
        return self.name[:TEXT_SCOPE]


class Title(models.Model):
    name =
    year =
    description =
    genre =
    category = ...(
        ...
    on_delete = models.SET_NULL,
                ...
    )

    class Meta:
        ordering =
        verbose_name =
        verbose_name_plural =

    def __str__(self):
        return self.name[:TEXT_SCOPE]


class Review(models.Model):
    text =
    rating =
    pub_date =
    author = ...(
        ...
    on_delete = models.CASCADE,
                ...
    )
    title = ...(
        ...
    on_delete = models.CASCADE,
                ...
    )

    class Meta:
        ordering =
        constraints =
        verbose_name =
        verbose_name_plural =

    def __str__(self):
        return self.text[:TEXT_SCOPE]


class Comment(models.Model):
    review = ...(
        ...
    on_delete = models.CASCADE,
                ...
    )
    author = ...(
        ...
    on_delete = models.CASCADE,
                ...
    )
    pub_date =
    text =

    class Meta:
        ordering =
        verbose_name =
        verbose_name_plural =

    def __str__(self):
        return self.text[:TEXT_SCOPE]
