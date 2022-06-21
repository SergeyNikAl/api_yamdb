from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'review',  'pub_date',)
    search_fields = ('author', 'review', 'name', 'pub_date',)
    list_filter = ('author', 'review', 'pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'pub_date', 'score',)
    search_fields = ('title', 'author', 'pub_date', 'score',)
    list_filter = ('title', 'author', 'pub_date', 'score',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'year',)
    search_fields = ('name', 'category', 'genre', 'year',)
    list_filter = ('name', 'category', 'genre', 'year',)
    empty_value_display = '-пусто-'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'first_name', 'last_name', 'email', 'role'
    )
    search_fields = ('username', 'email', 'role',)
    empty_value_display = '-пусто-'
