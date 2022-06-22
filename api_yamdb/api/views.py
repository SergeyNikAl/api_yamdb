from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from reviews.models import User

from .permissions import IsAdmin
from .serializers import UserSerializer

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    filter_backends = (filters.SearchFilter,)
    serach_fileds = ('username')

    @action(
        methods=['get', 'patch'],
        url_path='me',
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def user_profile(self, request):
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'PATCH':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        serializer = UserSerializer(
            user,
            context={'request': request},
            data=request.data,
            partial=True,
        )
        serializer.is_valid()
        if self.request.user.role == ADMIN or self.request.user.is_superuser:
            serializer.save()
        else:
            serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
