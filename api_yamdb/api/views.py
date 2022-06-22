from rest_framework import viewsets

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, TitlePostEditSerializer
from .permissions import IsAdminOrReadOnly
from reviews.models import Category, Genre, Title


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
