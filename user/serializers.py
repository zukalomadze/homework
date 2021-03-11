from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password',
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
