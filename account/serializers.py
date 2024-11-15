from rest_framework import serializers
from account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'email',
                  'first_name', 'last_name', 'is_active']
