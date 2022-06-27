from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import (
    Category, Genre, Review, Title, User
)
from .filtres import TitleFilter
from .permissions import (
    IsAdmin, IsAuthorORModeratorOrReadOnly, IsAdminOrReadOnly
)
from .serializers import (
    CategorySerializer,
    CommentsSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleSerializer,
    TitlePostEditSerializer,
    TokenSerializer,
    UserSerializer,
)

USERNAME_ALREADY_EXISTS = 'Такое имя уже занято.'
EMAIL_ALREADY_EXISTS = 'Такая почта уже зарегестрирована.'
CORRECT_CODE_EMAIL_MESSAGE = 'Код подтверждения: {code}.'
INVALID_CODE = 'Неверный код подтверждения.'


@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username')
    )
    if user.confirmation_code != serializer.validated_data.get(
            'confirmation_code'
    ):
        return Response(INVALID_CODE, status=status.HTTP_400_BAD_REQUEST)
    user.confirmation_code = ''
    user.save()
    token = str(AccessToken.for_user(user))
    return Response(token, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination

    @action(
        methods=['get', 'patch'],
        url_path='me',
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def user_profile(self, request):
        if request.method != 'PATCH':
            return Response(UserSerializer(request.user, partial=True).data)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filterset_class = TitleFilter
    ordering_fields = ('name',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitlePostEditSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorORModeratorOrReadOnly,
    )

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            title=self.get_title(),
            author=self.request.user
        )


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorORModeratorOrReadOnly,
    )
    pagination_class = LimitOffsetPagination

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
