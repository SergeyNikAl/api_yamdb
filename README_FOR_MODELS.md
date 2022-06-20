# Проект "YaMDb"
Проект "YaMDb" позволяет собирать отзывы пользователей на книги, фильмы, музыку.

### Авторы:
- Sergey Nikulin (SergeyNikAl) https://https://github.com/SergeyNikAl
- Tatayna (belkalev) https://github.com/belkalev
- Alibek Ubaidullayev (alibekubaidullayev) https://github.com/alibekubaidullayev

### Технологии:
- Python
- Django
- DRF
- SQLite3

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/SergeyNikAl/api_yamdb.git
```

```
cd api_yambd
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```


# Предложение по началу разработки
Создаем приложения "api" и "reviews" в директории api_yamdb/api_yamdb

```
.../api_yamdb/api_yamdb/api
.../api_yamdb/api_yamdb/reviews
```
Создаем приложение:
```
python manage.py startapp api
```
```
python manage.py startapp reviews
```

### reviews/models.py
В первую очередь начинаем с моделей
Они будут в приложении "reviews"
По заданию необходимо разработать модели для Пользователя, Категории, Жанра,
Заголовка, Произведение, Отзыв, Комментарии

Предварительная организация:
Все переменные организовываем в фикстурах файла
Например:

```
USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = [
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin'),
]
TEXT_SCOPE = 15 - потом перенесу в setiings
```
### User
```
class User(AbstractUser):
"""
Берем не от модели Model, а наследуем от абстрактной модели пользователя AbstractUser и
переопределяем ее, так как есть опциональный метод валидации по username.
Везде обязательно пишем verbose_name, чтобы было представление, что поле значит.
"""
    username_validator = models.RegexValidator(
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
    role = (Для определения статуса пользователя)
    #role = models.CharField(
        'Роль',
        max_length=max([len(x[0]) for x in ROLES]),
        default=USER,
        choices=ROLES
    )
    password = 
    
    REQUIRED_FIELDS = ['email']

Роли можно определить с помощью декоратора @property
'is_admin' и 'is_moderator_or_admin'
Например:
    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff
    ...
    ...
    
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL' - данное значение я сгенерирую в setiings
```
### Category
```
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
```
### Genre
```
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
```
### Title
```
class Title(models.Model):
    name = 
    year = 
    description = m
    genre = 
    category = ...(
        ...
        on_delete=models.SET_NULL,
        ...
    )

    class Meta:
        ordering = 
        verbose_name = 
        verbose_name_plural = 


    def __str__(self):
        return self.name[:TEXT_SCOPE]
```
### Review
```
class Review(models.Model):
    text = 
    score = 
    pub_date = 
    author = ...(
        ...
        on_delete=models.CASCADE,
        ...
    )
    title = ...(
        ...
        on_delete=models.CASCADE,
        ...
    )

    class Meta:
        ordering = 
        constraints = 
        verbose_name = 
        verbose_name_plural = 

    def __str__(self):
        return self.text[:TEXT_SCOPE]
```
### Comment
```
class Comment(models.Model):
    review = ...(
        ...
        on_delete=models.CASCADE,
        ...
    )
    author = ...(
        ...
        on_delete=models.CASCADE,
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
```

Данный скелет залил на гитхаб в модели