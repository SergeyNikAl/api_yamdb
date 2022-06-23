from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CommentsViewSet,
    ReviewViewSet,
    SingUpViewSet,
    TokenViewSet,
    UserViewSet,
)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('categories', ViewSet, basename='categories')
router_v1.register('genres', ViewSet, basename='genres')
router_v1.register('titles', ViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/'
    r'(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
)
router_v1.register('users/', UserViewSet, basename='users')
router_v1.register('auth/signup', SingUpViewSet, basename='signup')
router_v1.register('auth/token', TokenViewSet, basename='active_token')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
