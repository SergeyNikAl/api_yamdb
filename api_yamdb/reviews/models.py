from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MaxValueValidator
from django.db import models

from api_yamdb.settings import TEXT_SCOPE

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
YEAR_OVER_CURRENT = 'Год не может быть больше текущего.'

ROLES = (
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin'),
)
RATE_CHOICES = (
    (1, 'OK'),
    (2, 'Fine'),
    (3, 'Good'),
    (4, 'Amazing'),
    (5, 'Incredible'),
)


class User(AbstractUser):
    username_validator = RegexValidator(r'^[\w.@+-]+')
    username = models.CharField(
        max_length=100,
        unique=True,
        validators=[username_validator]
    )
    email = models.EmailField(
        blank=True,
        unique=True,
        verbose_name='Электронная почта'
    )
    first_name = models.CharField(
        'Имя пользователя',
        max_length=100,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=100,
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=30,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    password = models.CharField(max_length=150, blank=True)

    REQUIRED_FIELDS = ['email']

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == MODERATOR or self.is_admin


    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Category(models.Model):
    name = models.CharField(
        'Категория произведения',
        max_length=50,
    )
    slug = models.SlugField(
        'Адрес',
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:TEXT_SCOPE]


class Genre(models.Model):
    name = models.CharField(
        'Жанр произведения',
        max_length=50,
    )
    slug = models.SlugField(
        'Адрес',
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:TEXT_SCOPE]


class Title(models.Model):
    name = models.CharField(
        'Произведение',
        max_length=50
    )
    year = models.IntegerField(
        'Дата выхода',
        validators=(MaxValueValidator(
            timezone.now().year,
            message=YEAR_OVER_CURRENT),)
    )
    description = models.TextField(
        'Описание произведения',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        blank=True,
        null=True,
        on_delete = models.SET_NULL,
        related_name='titles'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:TEXT_SCOPE]


class Review(models.Model):
    text = models.CharField(
        verbose_name='Отзыв',
        max_length=250,
    )
    score = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True,
        db_index=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews',
        db_index=True,
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='reviews_per_title'
            )
        ]

    def __str__(self):
        return (
            f'{self.author} оставил отзыв на {self.title}'
        )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        db_index=True,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата создания комментария',
        auto_now_add=True,
        db_index=True,
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:TEXT_SCOPE]
