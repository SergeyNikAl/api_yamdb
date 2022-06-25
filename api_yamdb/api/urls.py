from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views

from api.views import (
    CommentsViewSet,
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    SingUpViewSet,
    TitleViewSet,
    TokenViewSet,
    UserViewSet,
)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/'
    r'(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
)
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('auth/signup', SingUpViewSet, basename='signup')
router_v1.register('auth/token', TokenViewSet, basename='active_token')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
