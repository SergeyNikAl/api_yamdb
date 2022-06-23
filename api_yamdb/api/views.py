from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from reviews.models import User

from .permissions import IsAdmin
from .serializers import UserSerializer, TokenSerializer, SignUpSerializer
from django.core.mail import send_mail


USERNAME_ALREADY_EXISTS = 'Такое имя уже занято.'
EMAIL_ALREADY_EXISTS = 'Такая почта уже зарегестрирована'
CORRECT_CODE_EMAIL_MESSAGE = 'Код подтверждения: {code}'
INVALID_CODE = 'Неизвестный запрос'

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


class SingUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializers = SignUpSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        username = serializers.validated_data.get('username')
        email = serializers.validated_data.get('email')
        try:
            user = User.objects.get(
                username=username,
                email=email
            )
        except User.DoesNotExist:
            if User.objects.filter(username=username).exists():
                return Response(USERNAME_ALREADY_EXISTS, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response(EMAIL_ALREADY_EXISTS, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(username=username, email=email)
        user.save()
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='YaMDb registration code',
            message=CORRECT_CODE_EMAIL_MESSAGE.format(code=confirmation_code),
            from_email=None,
            recipient_list=[user.email],
        )
        return Response(serializers.data, status=status.HTTP_200_OK)

        
class TokenViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializers = TokenSerializer
        serializers.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializers.validated_data.get('username'))
        confirmation_code = serializers.validated_data.get('confirmation_code')
        if not default_token_generator.check_token(user=user, token=confirmation_code):
            return Response(
                INVALID_CODE,
                status=status.HTTP_400_BAD_REQUEST
            )
        user.save()
        jwt_payload_hendler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODEHANDLER
        payload = jwt_payload_hendler(request.user)
        token = jwt_encode_handler(payload)
        return Response({'token': token}, status=status.HTTP_200_OK)