from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models

from api_yamdb.settings import TEXT_SCOPE
from reviews.validators import UsernameValidation, get_now_year

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = (
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin'),
)
RATE_CHOICES = (
    (1, 'Отвратительно'),
    (2, 'Ужасно'),
    (3, 'Плохо'),
    (4, 'Не интересно'),
    (5, 'Средне'),
    (6, 'OK'),
    (7, 'Сойдет'),
    (8, 'Хорошо'),
    (9, 'Удивительно'),
    (10, 'Невероятно'),
)



class User(AbstractUser, UsernameValidation):
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта'
    )
    first_name = models.CharField(
        'Имя пользователя',
        max_length=150,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=150,
        blank=True,
        null=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=max([len(role[0]) for role in ROLES]),
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=6,
        blank=True
    )

    REQUIRED_FIELDS = ['email']

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ("role",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class CategoryGenre(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
    )
    slug = models.SlugField(
        'Адрес',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name[:TEXT_SCOPE]


class Category(CategoryGenre):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenre):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.TextField(
        'Произведение',
    )
    year = models.IntegerField(
        'Дата выхода',
        validators=[MaxValueValidator(get_now_year),]
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
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:TEXT_SCOPE]


class ReviewComments(models.Model):
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата записи',
        auto_now_add=True,
        db_index=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='%(class)ss'
    )

    class Meta:
        ordering = ('-pub_date',)
        abstract = True

    def __str__(self):
        return self.text[:TEXT_SCOPE]


class Review(ReviewComments):
    score = models.PositiveSmallIntegerField(
        'Оценка',
        choices=RATE_CHOICES,
        null=True,
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta:
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


class Comments(ReviewComments):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='comments',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
