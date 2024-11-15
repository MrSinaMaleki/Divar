
from account.serializers import UserSerializer
from account.utils import generate_access_token, generate_refresh_token
from rest_framework.views import APIView
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from account.utils import generate_access_token


@api_view(['GET'])
def profile(request):
    user = request.user
    print("user => ",user)
    serialized_user = UserSerializer(user).data
    return Response({'user': serialized_user })


# @ensure_csrf_cookie
class Login(APIView):
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer

    def post(self, request):
        User = get_user_model()
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()
        if (email is None) or (password is None) or (user is None) or (not user.check_password(password)):
            return Response({'Message': 'Invalid Username or Password'}, status=401)

        serialized_user = self.serializer_class(user).data
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        Response().set_cookie(key='refreshtoken', value=refresh_token, httponly=True)

        return Response({
            'access_token': access_token,
            # 'user': serialized_user,
        })


# @csrf_protect
class RefreshToken(APIView):
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer

    """
        To obtain a new access_token this view expects 2 important things:
            1. a cookie that contains a valid refresh_token
            2. a header 'X-CSRFTOKEN' with a valid csrf token, client app can get it from cookies "csrftoken"
    """

    def get(self, request):

        User = get_user_model()
        refresh_token = request.COOKIES.get('refreshtoken')
        print(refresh_token)

        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.')
        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'expired refresh token, please login again.')

        user = User.objects.filter(id=payload.get('user_id')).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        access_token = generate_access_token(user)
        return Response({'access_token': access_token})


