from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('categories', ViewSet, basename='categories')
router_v1.register('genres', ViewSet, basename='genres')
router_v1.register('titles', ViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/'
    r'(?P<review_id>\d+)/comments',
    ViewSet, basename='comments'
)
router_v1.register('users/', ViewSet, basename='users')
router_v1.register('auth/signup', ViewSet, basename='signup')
router_v1.register('auth/token', ViewSet, basename='active_token')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
