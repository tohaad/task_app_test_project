from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import UserRegisterSerializer, UserLoginSerializer, UserLoginResponseSerializer, \
    EmptyBodySerializer


class UserRegisterAPIView(APIView):
    permission_classes = (AllowAny, )

    @extend_schema(
        request=UserRegisterSerializer,
        responses={201: UserRegisterSerializer}
    )
    def post(self, request, *_args, **_kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginAPIView(APIView):
    permission_classes = (AllowAny, )

    def get_serializer_context(self):
        return {'request': self.request}

    @extend_schema(
        request=UserLoginSerializer,
        responses={200: UserLoginResponseSerializer}
    )
    def post(self, request, *_args, **_kwargs):
        serializer = UserLoginSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        token, _ = Token.objects.get_or_create(user=serializer.validated_data['user'])
        response_data = {
            'token': token.key
        }
        response_serializer = UserLoginResponseSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class UserLogoutAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    @extend_schema(
        request=EmptyBodySerializer,
        responses={200: EmptyBodySerializer}
    )
    def post(self, request, *_args, **_kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_200_OK)


class UserAuthenticationCheckAPIView(APIView):
    """Returns 200 if user is authenticated."""
    permission_classes = (IsAuthenticated, )

    @extend_schema(responses={200: EmptyBodySerializer})
    def get(self, *_args, **_kwargs):
        return Response(status=status.HTTP_200_OK)
