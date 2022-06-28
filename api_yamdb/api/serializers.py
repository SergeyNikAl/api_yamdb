from django.core.validators import MaxValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import (
    Category, Comments, Genre, Review, Title, User,
    USERNAME_LENGTH, EMAIL_LENGTH, CONFIRMATION_CODE_LENGTH
)
from reviews.validators import (
    UsernameValidation, get_now_year, YEAR_OVER_CURRENT
)

MORE_THAN_ONE_REVIEW = (
    'Нельзя оставить больше одного отзыва '
    'на выбранное произведение.'
)


class UserSerializer(serializers.ModelSerializer, UsernameValidation):
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'role', 'bio'
        )


class SignUpSerializer(serializers.Serializer, UsernameValidation):
    username = serializers.CharField(max_length=USERNAME_LENGTH,)
    email = serializers.EmailField(max_length=EMAIL_LENGTH,)


class TokenSerializer(serializers.Serializer, UsernameValidation):
    username = serializers.CharField(max_length=USERNAME_LENGTH,)
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_LENGTH
    )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        read_only_fields = ('__all__',)
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
    year = serializers.IntegerField(validators=(MaxValueValidator(
        get_now_year, YEAR_OVER_CURRENT
    ),))

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

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


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
