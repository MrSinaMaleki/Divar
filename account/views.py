
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from account.serializers import UserSerializer
from account.utils import generate_access_token, generate_refresh_token
from rest_framework.views import APIView
from rest_framework.response import Response


@api_view(['GET'])
def profile(request):
    user = request.user
    serialized_user = UserSerializer(user).data
    return Response({'user': serialized_user })


# @ensure_csrf_cookie
class Login(APIView):
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer

    def post(self, request):
        print("hello ?")
        print(request.data)
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

