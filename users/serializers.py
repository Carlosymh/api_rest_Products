from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.Serializer):
    id= serializers.ReadOnlyField()
    first_name =serializers.CharField()
    last_name =serializers.CharField()
    username =serializers.CharField()
    email =serializers.EmailField()
    password =serializers.CharField()
    is_staff =serializers.BooleanField()
    is_superuser =serializers.BooleanField()
    is_active =serializers.BooleanField()

    def create(self, validate_data):
        isinstance=User()
        isinstance.first_name = validate_data.get('first_name')
        isinstance.last_name = validate_data.get('last_name')
        isinstance.username = validate_data.get('username')
        isinstance.email = validate_data.get('email')
        isinstance.is_staff = validate_data.get('is_staff')
        isinstance.is_superuser = validate_data.get('is_superuser')
        isinstance.is_active = validate_data.get('is_active')
        isinstance.set_password(validate_data.get('password'))

        isinstance.save()
        return isinstance
    
    def validate_username(self, data):
        users = User.objects.filter(username = data)
        if len(users) != 0:
            raise serializers.ValidationError("Este nombre de usuario ya existe")
        else:
            return data
        


