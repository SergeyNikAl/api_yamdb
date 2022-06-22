import datetime as dt

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title, User

MORE_THAN_ONE_REVIEW = (
    'Нельзя оставить больше одного отзыва '
    'на выбранное произведение.'
)
WRONG_YEAR_CREATION = 'Проверьте год создания произведения.'
WRONG_USERNAME = 'Имя пользователя указано неверно.'


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all()
        )]
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role')


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all()
        )]
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(WRONG_USERNAME)
        return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['id']


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.DecimalField(
        max_digits=3,
        decimal_places=2,
        required=False,
    )

    class Meta:
        model = Title
        read_only_fields = '__all__'
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category',
        )


class TitlePostEditSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    year = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_creation_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(WRONG_YEAR_CREATION)
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('author', 'title')

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        title = get_object_or_404(
            Title,
            id=self.context['view'].kwargs.get('title_id')
        )
        if Review.objects.filter(title=title, author=request.user):
            raise ValidationError(MORE_THAN_ONE_REVIEW)
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='author',
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'review')
