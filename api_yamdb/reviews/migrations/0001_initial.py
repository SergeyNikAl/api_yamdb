from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import reviews.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта')),
                ('first_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Имя пользователя')),
                ('last_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Фамилия пользователя')),
                ('role', models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default='user', max_length=9, verbose_name='Роль')),
                ('bio', models.TextField(blank=True, verbose_name='Биография')),
                ('confirmation_code', models.CharField(blank=True, max_length=6, verbose_name='Код подтверждения')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['role'],
            },
            bases=(models.Model, reviews.validators.UsernameValidation),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CategoryGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='Адрес')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Произведение')),
                ('year', models.IntegerField(validators=[django.core.validators.MaxValueValidator(reviews.validators.get_now_year)], verbose_name='Дата выхода')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание произведения')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('categorygenre_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reviews.CategoryGenre')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
            bases=('reviews.categorygenre',),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('categorygenre_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reviews.CategoryGenre')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
            bases=('reviews.categorygenre',),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата записи')),
                ('score', models.PositiveSmallIntegerField(choices=[(1, 'Отвратительно'), (2, 'Ужасно'), (3, 'Плохо'), (4, 'Не интересно'), (5, 'Средне'), (6, 'OK'), (7, 'Сойдет'), (8, 'Хорошо'), (9, 'Удивительно'), (10, 'Невероятно')], null=True, verbose_name='Оценка')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.Title', verbose_name='Произведение')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата записи')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentss', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.Review', verbose_name='Отзыв')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.AddField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.Category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(to='reviews.Genre', verbose_name='Жанр'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='reviews_per_title'),
        ),
    ]
